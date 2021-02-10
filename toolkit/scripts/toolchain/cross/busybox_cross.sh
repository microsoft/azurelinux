# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Docs used to create this script:
# http://clfs.org/view/clfs-embedded/x86/final-system/busybox.html

installDir="/opt/cross"
busyboxInstallDir="/opt/cross/aarch64-linux-gnu/sysroot"
buildDir="$HOME/cross"
scriptDir="$( cd "$( dirname "$0" )" && pwd )"

# Update the username based on your environment
# sudo chown username ${busyboxInstallDir}

export PATH="${installDir}/bin":$PATH

cd ${buildDir}

# Download source tarballs
wget https://www.busybox.net/downloads/busybox-1.32.0.tar.bz2

# Unzip source tarballs
tar xf busybox-1.32.0.tar.bz2

# Cross Compile Busybox
cd busybox-1.32.0


# Use the default busybox configuration
make ARCH=arm64 defconfig

make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu-
make ARCH=arm64 CROSS_COMPILE=aarch64-linux-gnu- CONFIG_PREFIX=${busyboxInstallDir} install