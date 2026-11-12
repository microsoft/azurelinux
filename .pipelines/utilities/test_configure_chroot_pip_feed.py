# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import configparser
import netrc
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

from configure_chroot_pip_feed import cleanup_feed, configure_feed


FEED = "https://pkgs.dev.azure.com/mariner-org/mariner/_packaging/Mariner-Pypi-Feed/pypi/simple/"
AUTHENTICATED_FEED = FEED.replace("https://", "https://build:job-token%25value@")


class ConfigureChrootPipFeedTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.worker = Path(self.temporary.name) / "worker"
        self.root = self.worker / "worker_chroot"
        self.root.mkdir(parents=True)

    def test_supports_prcheck_and_fasttrack_feed_names_and_ids(self):
        for path in (
            "mariner-org/_packaging/MarinerFeed/pypi/simple/",
            "mariner-org/_packaging/3a751d8b-0b69-4afc-a438-9487dba86628/pypi/simple",
            "mariner-org/mariner/_packaging/Mariner-Pypi-Feed/pypi/simple/",
            "mariner-org/36d030d6-1d99-4ebd-878b-09af1f4f722f/_packaging/ca2ce712-f15f-4dd0-b8c8-518db39ff9ec/pypi/simple/",
        ):
            with self.subTest(path=path):
                feed = "https://pkgs.dev.azure.com/" + path
                configure_feed(self.root, feed.replace("https://", "https://build:job-token@"))
                self.assertIn(feed, (self.root / "etc/pip.conf").read_text())
                cleanup_feed(self.root)

    def test_on_demand_feed_config_survives_without_environment_and_preserves_trust(self):
        bundle = self.root / "etc/pki/tls/certs/ca-bundle.crt"
        bundle.parent.mkdir(parents=True)
        bundle.write_text("original worker CA bundle", encoding="ascii")

        configure_feed(self.root, AUTHENTICATED_FEED)

        config = configparser.ConfigParser(interpolation=None)
        config.read(self.root / "etc/pip.conf")
        self.assertEqual(config["global"]["index-url"], FEED)
        self.assertEqual(config["global"]["extra-index-url"], "")
        self.assertEqual(config["global"]["cert"], "/etc/pki/tls/certs/ca-bundle.crt")
        self.assertNotIn("job-token", (self.root / "etc/pip.conf").read_text())
        auth = self.root / "root/.netrc"
        with mock.patch.dict(
            os.environ,
            {"HOME": str(auth.parent), "USERPROFILE": str(auth.parent)},
            clear=True,
        ):
            self.assertEqual(
                netrc.netrc().authenticators("pkgs.dev.azure.com"),
                ("build", "", "job-token%value"),
            )
        if os.name != "nt":
            self.assertEqual(auth.stat().st_mode & 0o777, 0o600)
        self.assertEqual(bundle.read_text(), "original worker CA bundle")

    def test_rejects_unapproved_or_malformed_feeds_before_writing(self):
        for feed in (
            AUTHENTICATED_FEED.replace("https:", "http:"),
            AUTHENTICATED_FEED.replace("pkgs.dev.azure.com", "pypi.org"),
            AUTHENTICATED_FEED.replace("Mariner-Pypi-Feed", "Another-Feed"),
            AUTHENTICATED_FEED.replace("mariner-org/mariner", "another-org/mariner"),
            AUTHENTICATED_FEED.replace("mariner-org/mariner", "mariner-org/another-project"),
            AUTHENTICATED_FEED.replace("Mariner-Pypi-Feed", "MarinerFeed"),
            AUTHENTICATED_FEED.replace("/mariner/_packaging/", "/_packaging/"),
            AUTHENTICATED_FEED + "?secret=value",
            AUTHENTICATED_FEED + "\ntrusted-host = pypi.org",
            AUTHENTICATED_FEED.replace("job-token%25value", "token%0Ainjection"),
            FEED,
        ):
            with self.subTest(feed=feed):
                with self.assertRaises(ValueError):
                    configure_feed(self.root, feed)
                self.assertFalse((self.root / "etc/pip.conf").exists())
                self.assertFalse((self.root / "root/.netrc").exists())

    def test_refuses_to_overwrite_existing_configuration_or_authentication(self):
        for relative in ("etc/pip.conf", "root/.netrc"):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("existing configuration", encoding="ascii")
            with self.assertRaises(FileExistsError):
                configure_feed(self.root, AUTHENTICATED_FEED)
            self.assertEqual(path.read_text(), "existing configuration")
            path.unlink()

    def test_cleanup_removes_credentials_from_template_retained_chroots_and_archive(self):
        configure_feed(self.root, AUTHENTICATED_FEED)
        retained = self.worker / "chroot/package_TEST_BUILD"
        shutil.copytree(self.root, retained)
        archive = self.worker / "worker_chroot.tar.gz"
        archive.write_bytes(b"job-local archive")

        cleanup_feed(self.root)
        cleanup_feed(self.root)

        for root in (self.root, retained):
            self.assertFalse((root / "root/.netrc").exists())
            self.assertFalse((root / "etc/pip.conf").exists())
        self.assertFalse(archive.exists())

    def test_cleanup_preserves_unmanaged_files_and_archive(self):
        auth = self.root / "root/.netrc"
        auth.parent.mkdir()
        auth.write_text("existing authentication", encoding="ascii")
        archive = self.worker / "worker_chroot.tar.gz"
        archive.write_bytes(b"original archive")

        cleanup_feed(self.root)

        self.assertEqual(auth.read_text(), "existing authentication")
        self.assertEqual(archive.read_bytes(), b"original archive")

    @unittest.skipIf(os.name == "nt", "Creating symlinks requires elevated Windows privileges.")
    def test_rejects_symlinked_destination_without_modifying_external_file(self):
        outside = Path(self.temporary.name) / "outside"
        outside.mkdir()
        (self.root / "root").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            configure_feed(self.root, AUTHENTICATED_FEED)
        self.assertFalse((outside / ".netrc").exists())


if __name__ == "__main__":
    unittest.main()
