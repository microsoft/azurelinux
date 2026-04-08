#!/usr/bin/env python3
#
# generates Provides: bundled(npm(...)) = ... lines for each declared dependency and devDependency of package.json
#
import sys
import json
import re
from packaging import version


def read_declared_pkgs(package_json_path):
    with open(package_json_path) as f:
        package_json = json.load(f)
        return list(package_json['dependencies'].keys()) + list(package_json['devDependencies'].keys())


def read_installed_pkgs(yarn_lock_path):
    with open(yarn_lock_path) as f:
        lockfile = f.read()
        return re.findall(r'^"?'  # can start with a "
                          r'(.+?)@.+(?:,.*)?:\n'  # characters up to @
                          r'  version "(.+)"',  # and the version
                          lockfile, re.MULTILINE)


def list_provides(declared_pkgs, installed_pkgs):
    for declared_pkg in declared_pkgs:
        # there can be multiple versions installed of one package (transitive dependencies)
        # but rpm doesn't support Provides: with a single package and multiple versions
        # so let's declare the oldest version here
        versions = [version.parse(pkg_version)
                    for pkg_name, pkg_version in installed_pkgs if pkg_name == declared_pkg]
        oldest_version = sorted(versions)[0]
        yield f"Provides: bundled(npm({declared_pkg})) = {oldest_version}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} package-X.Y.Z/", file=sys.stdout)
        sys.exit(1)

    package_dir = sys.argv[1]
    declared_pkgs = read_declared_pkgs(f"{package_dir}/package.json")
    installed_pkgs = read_installed_pkgs(f"{package_dir}/yarn.lock")
    provides = list_provides(declared_pkgs, installed_pkgs)
    for provide in sorted(provides):
        print(provide)
