import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest


GENERATOR = Path(sys.argv.pop(1)).read_text()


class AutologinGeneratorTests(unittest.TestCase):
    def run_generator(self, core_shell, users, cmdline):
        core = f"core:x:500:500::/:{core_shell}" if core_shell else ""
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            if users is not None:
                (root / "passwd").write_text((core + "\n" if core else "") + users)
            (root / "cmdline").write_text(cmdline + "\n")
            (root / "active").write_text("ttyS0\n")
            (root / "getent").write_text(
                "#!/bin/sh\n"
                + ("printf '%s\\n' " + shlex.quote(core) if core else "exit 2")
                + "\n"
            )
            (root / "getent").chmod(0o755)
            # Redirect host inputs only; execute the complete packaged generator.
            script = GENERATOR.replace("/etc/passwd", str(root / "passwd"))
            script = script.replace("/proc/cmdline", str(root / "cmdline"))
            script = script.replace("/sys/class/tty/console/active", str(root / "active"))
            (root / "generator").write_text(script)
            output = root / "output"
            output.mkdir()
            result = subprocess.run(
                ["bash", str(root / "generator"), str(output), str(output), str(output)],
                env={**os.environ, "PATH": f"{root}:" + os.environ["PATH"]},
                capture_output=True,
                text=True,
            )
            overrides = {
                str(path.relative_to(output)): path.read_text()
                for path in output.rglob("*.conf")
            }
            return result, overrides

    def test_no_eligible_user_exits_successfully(self):
        for core_shell in (None, "/sbin/nologin"):
            for cmdline in ("quiet", "flatcar.autologin"):
                with self.subTest(core_shell=core_shell, cmdline=cmdline):
                    result, overrides = self.run_generator(
                        core_shell, "disabled:x:1000:1000::/:/bin/false\n", cmdline
                    )
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(overrides, {})

    def test_empty_user_search_exits_successfully(self):
        for cmdline in ("quiet", "flatcar.autologin"):
            with self.subTest(cmdline=cmdline):
                result, overrides = self.run_generator(None, "", cmdline)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(overrides, {})

    def test_missing_passwd_file_reports_failure(self):
        for core_shell in (None, "/sbin/nologin"):
            for cmdline in ("quiet", "flatcar.autologin"):
                with self.subTest(core_shell=core_shell, cmdline=cmdline):
                    result, overrides = self.run_generator(core_shell, None, cmdline)
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("passwd", result.stderr)
                    self.assertIn("No such file or directory", result.stderr)
                    self.assertEqual(overrides, {})

    def test_existing_user_selection_is_preserved(self):
        users = "disabled:x:1000:1000::/:/bin/false\nalice:x:1001:1001::/:/bin/bash\n"
        for core_shell, expected in (
            ("/bin/bash", "core"),
            ("/sbin/nologin", "alice"),
            (None, "alice"),
        ):
            with self.subTest(core_shell=core_shell):
                result, overrides = self.run_generator(core_shell, users, "flatcar.autologin")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    set(overrides),
                    {
                        "getty@.service.d/10-autologin.conf",
                        "serial-getty@.service.d/10-autologin.conf",
                        "emergency.service.d/10-autologin.conf",
                    },
                )
                for unit in ("getty@.service", "serial-getty@.service"):
                    contents = overrides[f"{unit}.d/10-autologin.conf"]
                    self.assertIn(f"--autologin {expected} ", contents)
                    self.assertIn("$TERM", contents)
                self.assertIn("login -f root", overrides["emergency.service.d/10-autologin.conf"])

    def test_eligible_user_without_opt_in_emits_no_overrides(self):
        result, overrides = self.run_generator(
            "/sbin/nologin", "alice:x:1000:1000::/:/bin/bash\n", "quiet"
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(overrides, {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
