#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
TEMPLATES = REPO_ROOT / ".pipelines" / "templates"
BASH = os.environ.get("BASH") or shutil.which("bash")
INDEX = "https://test-user:test-password-long@example.invalid/simple/"


def load_template(name):
    return yaml.safe_load((TEMPLATES / name).read_text(encoding="utf-8"))


def find_step(steps, display_name):
    for step in steps:
        if step.get("displayName") == display_name:
            return step
        for value in step.values():
            if isinstance(value, list):
                found = find_step(value, display_name)
                if found is not None:
                    return found
    return None


def render(script, parameters):
    script = re.sub(
        r"\$\{\{ join\(' ', parameters\.(\w+)\) \}\}",
        lambda match: " ".join(parameters[match[1]]),
        script,
    )

    def replace(match):
        value = parameters[match[1]]
        return str(value).lower() if isinstance(value, bool) else str(value)

    return re.sub(r"\$\{\{ parameters\.(\w+) \}\}", replace, script)


def run_bash(script, variables=None):
    environment = dict(os.environ)
    environment.pop("PIP_INDEX_URL", None)
    environment.pop("OTHER_CHECK_ENV", None)
    environment.update(variables or {})
    prefix = f'python3() {{ "{Path(sys.executable).as_posix()}" "$@"; }}\n'
    return subprocess.run(
        [BASH, "-c", prefix + script],
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )


@unittest.skipUnless(BASH, "Bash is required to execute pipeline scripts")
class TestPackageCheckPip(unittest.TestCase):
    def authenticate(self, outcome, previous_index=INDEX):
        variables = {"PIP_INDEX_URL": previous_index}
        output = ""
        for step in load_template("PipAuthenticateCheckFeed.yml")["steps"]:
            if step.get("task") == "PipAuthenticate@1":
                if outcome == "succeeded":
                    variables["PIP_INDEX_URL"] = INDEX
                elif outcome == "failed" and not step.get("continueOnError"):
                    return 1, variables, output
                continue
            result = run_bash(
                step["bash"],
                {"CHECK_FEED_INDEX_URL": variables.get("PIP_INDEX_URL", "$(PIP_INDEX_URL)")},
            )
            output += result.stdout + result.stderr
            for value in re.findall(
                r"##vso\[task.setvariable variable=PIP_INDEX_URL;issecret=true\](.*)",
                result.stdout,
            ):
                variables["PIP_INDEX_URL"] = value
            if result.returncode:
                return result.returncode, variables, output
        return 0, variables, output

    def build(self, index=None, names=None, exit_code=0, root=REPO_ROOT, extra_variables=None):
        template = load_template("PackageBuild.yml")
        parameters = {
            parameter["name"]: parameter.get("default", "")
            for parameter in template["parameters"]
        }
        parameters.update(
            buildRepoRoot=root.as_posix(),
            isCheckBuild=True,
            checkEnvPassthrough=names or ["PIP_INDEX_URL"],
        )
        script = render(find_step(template["steps"], "Build packages")["script"], parameters)
        mock = """
sudo() {
    echo BUILD_RAN
    printf 'ARG:%s\\n' "$@"
    return "$BUILD_RESULT"
}
"""
        variables = {"BUILD_RESULT": str(exit_code), **(extra_variables or {})}
        if index is not None:
            variables["PIP_INDEX_URL"] = index
        return run_bash(mock + script, variables)

    def test_unavailable_authentication_drops_previous_job_credential(self):
        for outcome in ("skipped", "failed"):
            with self.subTest(outcome=outcome):
                status, variables, output = self.authenticate(outcome)
                self.assertEqual(status, 0, output)
                self.assertEqual(variables["PIP_INDEX_URL"], "")
                self.assertIn("##[warning]", output)
                self.assertNotIn(INDEX, output)

    def test_missing_index_still_runs_package_checks(self):
        for index in (None, "", "$(PIP_INDEX_URL)"):
            with self.subTest(index=index):
                result = self.build(index)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("BUILD_RAN", result.stdout)
                self.assertIn("ARG:RUN_CHECK=y", result.stdout)
                self.assertNotIn("ARG:CHECK_ENV_PASSTHROUGH=", result.stdout)
                self.assertIn("##[warning]", result.stdout)

    def test_other_forwarded_variables_remain_required(self):
        result = self.build(names=["PIP_INDEX_URL", "OTHER_CHECK_ENV"])
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("OTHER_CHECK_ENV", result.stderr)
        self.assertNotIn("BUILD_RAN", result.stdout)
        result = self.build(
            names=["PIP_INDEX_URL", "OTHER_CHECK_ENV"],
            extra_variables={"OTHER_CHECK_ENV": "test-value-long"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ARG:CHECK_ENV_PASSTHROUGH=OTHER_CHECK_ENV", result.stdout)
        self.assertNotIn("ARG:CHECK_ENV_PASSTHROUGH=PIP_INDEX_URL", result.stdout)

    def test_actual_build_failure_is_not_masked(self):
        result = self.build(exit_code=17)
        self.assertEqual(result.returncode, 17)
        self.assertIn("BUILD_RAN", result.stdout)
        self.assertIn("ARG:RUN_CHECK=y", result.stdout)

    def test_available_credential_is_masked_forwarded_and_redacted(self):
        status, variables, output = self.authenticate("succeeded")
        self.assertEqual(status, 0, output)
        self.assertEqual(variables["PIP_INDEX_URL"], INDEX)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            scripts = root / "toolkit" / "scripts"
            scripts.mkdir(parents=True)
            shutil.copyfile(
                REPO_ROOT / "toolkit/scripts/redact_env_values.py",
                scripts / "redact_env_values.py",
            )
            logs = root / "build" / "logs"
            logs.mkdir(parents=True)
            log = logs / "failed-test.log"
            log.write_text(INDEX, encoding="utf-8")
            result = self.build(INDEX, exit_code=17, root=root)
            self.assertEqual(result.returncode, 17, result.stderr)
            self.assertIn("ARG:--preserve-env=PIP_INDEX_URL", result.stdout)
            self.assertIn("ARG:CHECK_ENV_PASSTHROUGH=PIP_INDEX_URL", result.stdout)
            self.assertNotIn(INDEX, result.stdout + result.stderr)
            template = load_template("PackageBuild.yml")
            script = render(
                find_step(template["steps"], "Redact forwarded check variables from logs")["bash"],
                {"buildRepoRoot": root.as_posix(), "checkEnvPassthrough": ["PIP_INDEX_URL"]},
            )
            result = run_bash(
                'sudo() { shift; "$@"; }\n' + script,
                {"PIP_INDEX_URL": INDEX},
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(log.read_text(encoding="utf-8"), "***")

    def test_unset_macro_warns_but_invalid_index_fails(self):
        step = find_step(
            load_template("PipAuthenticateCheckFeed.yml")["steps"],
            "Mask package-check pip feed credential",
        )
        missing = run_bash(step["bash"], {"CHECK_FEED_INDEX_URL": "$(PIP_INDEX_URL)"})
        self.assertEqual(missing.returncode, 0, missing.stderr)
        self.assertIn("##[warning]", missing.stdout)
        invalid = run_bash(step["bash"], {"CHECK_FEED_INDEX_URL": "not-a-valid-index"})
        self.assertNotEqual(invalid.returncode, 0)
        self.assertIn("must use HTTPS", invalid.stderr)


if __name__ == "__main__":
    unittest.main()
