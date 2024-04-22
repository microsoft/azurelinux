#!/usr/bin/python3

# Script that updates the pkggen_core_*.txt and toolchain_*.txt files from a toolchain archive tarball.

import argparse
import os
import re
import subprocess
import sys
from typing import List, Dict

# Regex for parsing the package filename.
# e.g. "ca-certificates-2.0.0-16.cm2.noarch.rpm"
PACKAGE_NAME_REGEX = re.compile(r'^([\w\+-]+)-([\w\.~]+)-(\d+)(\.(\w+))?\.(\w+)\.rpm$')

# Get the list of package filenames from the toolchain archive tarball.
def getToolchainArchivePackageFileNames(toolchainArchive: str) -> List[str]:
    tarProc = subprocess.run(['tar', '-tf', toolchainArchive], check=True, text=True, capture_output=True)
    lines = tarProc.stdout.split('\n')

    packageFileNames = []
    for line in lines:
        if not line.startswith('built_rpms_all/'):
            continue

        packageFileName = line.removeprefix('built_rpms_all/').strip()
        if packageFileName == "":
            continue

        packageFileNames.append(packageFileName)

    return packageFileNames

# Create a map from package names to package file names.
def createPackagesMap(packageFileNames: List[str]) -> Dict[str, str]:
    packagesMap = dict()
    
    for packageFileName in packageFileNames:
        match = PACKAGE_NAME_REGEX.match(packageFileName)
        if not match:
            print(f"Bad package filename: {packageFileName}", file=sys.stderr)
            continue

        name, version, release, _, osVersion, arch = match.groups()
        packagesMap[name] = packageFileName

    return packagesMap

# Read a toolchain manifest file.
def readManifestFile(filename: str) -> List[str]:
    with open(filename, 'r') as fd:
        lines = fd.readlines()

    return lines

# Write a toolchain manifest file.
def writeManifestFile(lines: List[str], filename: str) -> List[str]:
    with open(filename, 'w') as fd:
        for line in lines:
            print(line, file=fd)

# Update a toolchain manifest file.
def updateManifestFile(manifestFileName: str, packagesMap: Dict[str, str], checkMissingPackages: bool):
    lines = readManifestFile(manifestFileName)

    newLines = []
    manifestPackages = []
    for i in range(len(lines)):
        packageFileName = lines[i]

        match = PACKAGE_NAME_REGEX.match(packageFileName)
        if not match:
            print(f"Bad manifest filename: {packageFileName}", file=sys.stderr)
            continue

        name, version, release, _, osVersion, arch = match.groups()
        manifestPackages.append(name)

        if name not in packagesMap:
            print(f"Package missing from toolchain tarball: {name}", file=sys.stderr)
            continue

        newLines.append(packagesMap[name])

    if checkMissingPackages:
        # Check if there are any packages in the toolchain archive tarball that aren't in the toolchain manifest.
        newPackages = sorted(set(packagesMap.keys()) - set(manifestPackages))
        if len(newPackages) > 0:
            for newPackage in newPackages:
                print(f"Package missing from manifest: {newPackage}", file=sys.stderr)

    # Write the new manifest file.
    writeManifestFile(newLines, manifestFileName)

def updateManifests(arch: str, toolchainArchive: str):
    packageFileNames = getToolchainArchivePackageFileNames(toolchainArchive)
    packagesMap = createPackagesMap(packageFileNames)

    scriptDirectory = os.path.dirname(os.path.realpath(__file__))
    pkggenCoreManifestPath = os.path.join(scriptDirectory, f'pkggen_core_{arch}.txt')
    toolchainManifestPath = os.path.join(scriptDirectory, f'toolchain_{arch}.txt')

    updateManifestFile(pkggenCoreManifestPath, packagesMap, False)
    updateManifestFile(toolchainManifestPath, packagesMap, True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('arch', choices=['x86_64', 'aarch64'], help='CPU archiecture (x86_64, aarch64)')
    parser.add_argument('toolchain_archive', help='Path to toolchain archive tarball')
    args = parser.parse_args()

    updateManifests(args.arch, args.toolchain_archive)

if __name__ == '__main__':
    main()
