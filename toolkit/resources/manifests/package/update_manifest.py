#!/usr/bin/env python3

import os
import sys


# Check /etc/os-release for ID=mariner. Otherwise exit
with open("/etc/os-release", "r") as f:
    for line in f:
        if "ID=mariner" in line:
            break
    else:
        print("This script runs only on Mariner")
        sys.exit(1)


def usage():
    print("Usage: " + sys.argv[0] + " <arch>")
    sys.exit(1)


def update_manifest_pkg_version(old_file, new_file):
    # Remove the toolchain new files if they exist
    if os.path.exists(new_file):
        os.remove(new_file)
    # Remove the pkggen new files if they exist
    if os.path.exists(pkggen_file_new):
        os.remove(pkggen_file_new)

    # for each line in old_file
    # split the line by last hypen and store it as the pkgname
    # get version using yum
    # get release using yum
    # generate complete rpm name by combining pkgname, version and release
    # append the complete rpm name to the new file
    with open(old_file, "r") as f:
        with open(new_file, "w") as f_new:
            for line in f:
                if "msopenjdk" in line:
                    pkgname = line.rsplit("-", 3)[0]
                else:
                    pkgname = line.rsplit("-", 2)[0]

                # Check if package available in yum
                if os.popen("yum info " + pkgname + " | grep Name | cut -d : -f 2 | head -1").read().strip() == "":
                    print("Package " + pkgname + " not available in yum")

                version = os.popen("yum info " + pkgname + " | grep Version | cut -d : -f 2 | head -1").read().strip()
                release = os.popen("yum info " + pkgname + " | grep Release | cut -d : -f 2 | head -1").read().strip()
                rpm_name = pkgname + "-" + version + "-" + release + "-" + arch + ".rpm"
                # print(rpm_name)
                f_new.write(rpm_name + "\n")


# If number of arguments is not 2, call usage()
if len(sys.argv) != 2:
    usage()

arch = sys.argv[1]
toolchain_file = "toolchain_" + arch + ".txt"
pkggen_file = "pkggen_core_" + arch + ".txt"
toolchain_file_new = "toolchain_" + arch + ".txt.new"
pkggen_file_new = "pkggen_core_" + arch + ".txt.new"

update_manifest_pkg_version(toolchain_file, toolchain_file_new)
update_manifest_pkg_version(pkggen_file, pkggen_file_new)
