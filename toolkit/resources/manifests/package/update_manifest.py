#!/usr/bin/env python3

import os
import sys


def usage():
    print("Usage: " + sys.argv[0] + " <arch>")
    sys.exit(1)


# If number of arguments is not 2, call usage()
if len(sys.argv) != 2:
    usage()

arch = sys.argv[1]
toolchain_file = "toolchain_" + arch + ".txt"
pkggen_file = "pkggen_core_" + arch + ".txt"
toolchain_file_new = "toolchain_" + arch + ".txt.new"
pkggen_file_new = "pkggen_core_" + arch + ".txt.new"

# for each line in toolchain_file
# split the line by last hypen and store it as the pkgname
# get version using yum
# get release using yum
# generate complete rpm name by combining pkgname, version and release
# append the complete rpm name to the new file
with open(toolchain_file, "r") as f:
    with open(toolchain_file_new, "w") as f_new:
        for line in f:
            pkgname = line.rsplit("-", 1)[0]
            version = os.popen("yum info " + pkgname + " | grep Version | cut -d : -f 2").read().strip()
            release = os.popen("yum info " + pkgname + " | grep Release | cut -d : -f 2").read().strip()
            rpm_name = pkgname + "-" + version + "-" + release + "-" + arch + ".rpm"
            print(rpm_name)
            f_new.write(rpm_name + "\n")
