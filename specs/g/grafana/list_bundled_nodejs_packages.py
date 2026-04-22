#!/usr/bin/env python3
#
# generates Provides: bundled(npm(...)) = ... lines for each declared dependency and devDependency of package.json
#
import os
import sys
import json
import yaml
from packaging import version


def scan_package_json(package_dir):
    for root, dirs, files in os.walk(package_dir, topdown=True):
        dirs[:] = [d for d in dirs if d not in ["node_modules", "vendor"]]
        if "package.json" in files:
            yield os.path.join(root, "package.json")


def read_declared_pkgs(package_json_path):
    with open(package_json_path) as f:
        package_json = json.load(f)
        return list(package_json.get("dependencies", {}).keys()) + list(
            package_json.get("devDependencies", {}).keys()
        )


def read_installed_pkgs(yarn_lock_path):
    bad_version_strings = ['0.0.0-use.local', '7.0.1-patch.1']
    with open(yarn_lock_path) as f:
        lockfile = yaml.safe_load(f)
        for pkg_decl, meta in lockfile.items():
            for pkg in pkg_decl.split(", "):
                if ":" not in pkg:
                    continue
                pkg_name = pkg[: pkg.index("@", 1)]
                pkg_version = meta["version"]
                if pkg_version not in bad_version_strings:
                    yield (pkg_name, pkg_version)


def list_provides(declared_pkgs, installed_pkgs):
    for declared_pkg in declared_pkgs:
        # there can be multiple versions installed of one package (transitive dependencies)
        # but rpm doesn't support Provides: with a single package and multiple versions
        # so let's declare the oldest version here
        versions = [
            version.parse(pkg_version)
            for pkg_name, pkg_version in installed_pkgs
            if pkg_name == declared_pkg
        ]

        if not versions:
            print(f"warning: {declared_pkg} missing in yarn.lock", file=sys.stderr)
            continue

        oldest_version = sorted(versions)[0]
        yield f"Provides: bundled(npm({declared_pkg})) = {oldest_version}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} package-X.Y.Z/", file=sys.stdout)
        sys.exit(1)

    package_dir = sys.argv[1]
    declared_pkgs = set()
    for package_json_path in scan_package_json(package_dir):
        declared_pkgs.update(read_declared_pkgs(package_json_path))
    installed_pkgs = list(read_installed_pkgs(f"{package_dir}/yarn.lock"))
    provides = list_provides(declared_pkgs, installed_pkgs)
    for provide in sorted(provides):
        print(provide)
