#!/usr/bin/python3
# SPDX-License-Identifier: GPL-3.0-or-later
# SPDX-FileCopyrightText 2022 Maxwell G <gotmax@e.email>

"""
This script uses Ansible Collection metadata from galaxy.yml to figure out the
namespace, name, and version of the collection being packaged.

``ansible_collection.py install`` (used by %ansible_collecton_install) uses
this information to find and install the collection artifact that was just
built with %ansible_collection_build. It also generates a files list for use
with `%files -f`.

``ansible_collection.py test`` (used by %ansible_test_unit) parses galaxy.yml
to determine the collection namespace and name that's needed to create the
directory structure that ansible-test expects. After creating a temporary build
directory with the needed structure, the script runs ansible-test units with
the provided arguments.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from itertools import chain
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any, Dict, Optional, Sequence, Tuple, Union

from yaml import CSafeLoader, load


class CollectionError(Exception):
    pass


class AnsibleCollection:
    def __init__(self, collection_srcdir: Optional[Path] = None) -> None:
        self.collection_srcdir = collection_srcdir or Path.cwd()
        self.data = self._load_data()
        self.namespace = self.data["namespace"]
        self.name = self.data["name"]
        self.version = self.data["version"]

    def _load_data(self) -> Dict[str, Any]:
        path = self.collection_srcdir / "galaxy.yml"
        if not path.exists():
            raise CollectionError(f"{path} does not exist!")
        print(f"Loading collection metadata from {path}")

        with open(path, encoding="utf-8") as file:
            return load(file, Loader=CSafeLoader)

    def install(self, destdir: Union[str, Path]) -> None:
        artifact = self.collection_srcdir / Path(
            f"{self.namespace}-{self.name}-{self.version}.tar.gz"
        )
        if not artifact.exists() and not artifact.is_file():
            raise CollectionError(
                f"{artifact} does not exist! Did you run %ansible_collection_build?"
            )

        args = (
            "ansible-galaxy",
            "collection",
            "install",
            "--force",
            "-n",
            "-p",
            str(destdir),
            str(artifact),
        )
        print(f"Running: {args}")
        print()
        # Without this, the print statements are shown after the command
        # output when building in mock.
        sys.stdout.flush()
        subprocess.run(args, check=True, cwd=self.collection_srcdir)
        print()

    def write_filelist(self, filelist: Path) -> None:
        filelist.parent.mkdir(parents=True, exist_ok=True)
        contents = "%{ansible_collections_dir}/" + self.namespace
        print(f"Writing filelist to {filelist}")
        with open(filelist, "w", encoding="utf-8") as file:
            file.write(contents)

    def unit_test(
        self,
        extra_args: Sequence[str],
        extra_paths: Sequence[Path],
        collections: Sequence[str],
    ) -> None:
        with TemporaryDirectory() as _temp:
            temp = Path(_temp)
            temppath = temp / "ansible_collections" / self.namespace / self.name
            shutil.copytree(
                self.collection_srcdir,
                temppath,
            )
            collection_paths = (
                self._get_collection_path(collection) for collection in collections
            )
            for extra in chain(collection_paths, extra_paths):
                self._handle_extra_path(temp, extra)
            args = ("ansible-test", "units", *extra_args)
            print(f"Running: {args}")
            print()
            # Without this, the print statements are shown after the command
            # output when building in mock.
            sys.stdout.flush()
            subprocess.run(
                args,
                cwd=temppath,
                check=True,
                env={**os.environ, "ANSIBLE_GALAXY_COLLECTIONS_PATH_WARNING": "0"},
            )

    def _get_collection_path(self, collection: str) -> Path:
        proc = subprocess.run(
            ["ansible-galaxy", "collection", "list", "--format=json", collection],
            check=True,
            universal_newlines=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        # {
        #   "/usr/share/ansible/collections/ansible_collections": {
        #     "community.general": {
        #       "version": "8.2.0"
        #     }
        #   }
        # }
        data: Dict[str, Dict[str, Any]] = json.loads(proc.stdout)
        for path, collection_part in data.items():
            version = collection_part[collection]["version"]
            print(f"Using locally-installed version {version} of {collection}")
            return Path(path, *collection.split(".", 1))
        raise CollectionError(f"Failed to add {collection} to the test tree")

    def _handle_extra_path(self, collection_tree: Path, extra_path: Path) -> None:
        namespace_name = _get_namespace_name(extra_path)
        if namespace_name == (self.namespace, self.name):
            raise CollectionError(
                f"{extra_path} is the same collection as {self.collection_srcdir}"
            )
        new_path = Path(collection_tree, "ansible_collections", *namespace_name)
        if new_path.is_dir():
            raise CollectionError(
                f"Cannot copy {extra_path}."
                f" Collection {namespace_name} was already added."
            )
        print(
            f"Copying {extra_path} ({'.'.join(namespace_name)}) to the collection tree"
        )
        shutil.copytree(extra_path, new_path)


def _get_namespace_name(extra_path: Path) -> Tuple[str, str]:
    data_file = extra_path / "MANIFEST.json"
    data_file2 = extra_path / "galaxy.yml"
    if data_file.is_file():
        with data_file.open("r", encoding="utf-8") as fp:
            data = json.load(fp)["collection_info"]
    elif data_file2.is_file():
        data_file = data_file2
        with data_file2.open("r", encoding="utf-8") as fp:
            data = load(fp, Loader=CSafeLoader)
    else:
        raise CollectionError(f"No metadata file found for collection in {extra_path}")
    expected_keys = {"namespace", "name"}
    if set(data) & expected_keys != expected_keys:
        raise CollectionError(f"Invalid metadata file: {data_file}")
    return data["namespace"], data["name"]


def parseargs() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install and test Ansible Collections in an rpmbuild environment"
    )
    subparsers = parser.add_subparsers(dest="action")
    install_parser = subparsers.add_parser(
        "install",
        help="Run ansible-galaxy collection install and write filelist",
    )
    install_parser.add_argument(
        "--collections-dir",
        required=True,
        help="Collection destination directory",
        type=Path,
    )
    install_parser.add_argument(
        "--filelist",
        type=Path,
        required=True,
        help="%%{ansible_collection_filelist}",
    )

    test_parser = subparsers.add_parser(
        "test",
        help="Run ansible-test unit after creating the necessary directory structure",
    )
    test_parser.add_argument(
        "-p",
        "--extra-path",
        dest="extra_paths",
        action="append",
        help="Path to an extra collection include in the test ansible_collection tree",
        type=Path,
    )
    test_parser.add_argument(
        "-c",
        "--collection",
        action="append",
        dest="collections",
        help="Add a collection from the collection path to the test tree",
    )
    test_parser.set_defaults(allow_extra_args=True)
    args, extra_args = parser.parse_known_args()
    # add_subparsers does not support required on Python 3.6
    if not args.action:
        parser.print_usage()
        sys.exit(2)
    if extra_args:
        if not getattr(args, "allow_extra_args", False):
            parser.error(f"unrecognized arguments: {' '.join(extra_args)}")
        if extra_args and extra_args[0] == "--":
            extra_args = extra_args[1:]
        args.extra_args = extra_args
    vars(args).pop("allow_extra_args", None)
    return args


def main():
    args = parseargs()
    collection = AnsibleCollection()
    if args.action == "install":
        collection.install(args.collections_dir)
        collection.write_filelist(args.filelist)
    elif args.action == "test":
        collection.unit_test(
            args.extra_args,
            (args.extra_paths or ()),
            (args.collections or ()),
        )


if __name__ == "__main__":
    try:
        main()
    except (CollectionError, subprocess.CalledProcessError) as err:
        sys.exit(str(err))
