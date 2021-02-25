# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

kernelVersion="5.4.83"
kernelTargetArch="arm64"
toolchainTuple="aarch64-mariner-linux-gnu"

installDir="/opt/cross"
sysrootDir="/opt/cross/${toolchainTuple}/sysroot"
buildDir="$HOME/cross"
kernelBuildDir=${buildDir}/kernel
kernelStandaloneInstallDir=${installDir}/kernel

sudo rm -rf ${kernelBuildDir}
sudo rm -rf ${kernelStandaloneInstallDir}

mkdir -p ${kernelBuildDir}
mkdir -p ${kernelStandaloneInstallDir}

export PATH="${installDir}/bin":$PATH

cd ${kernelBuildDir}
wget https://github.com/microsoft/WSL2-Linux-Kernel/archive/linux-msft-${kernelVersion}.tar.gz
tar xf linux-msft-${kernelVersion}.tar.gz

cd WSL2-Linux-Kernel-linux-msft-${kernelVersion}
make ARCH=${kernelTargetArch} defconfig

make ARCH=${kernelTargetArch} CROSS_COMPILE=${toolchainTuple}- -j$(nproc)

mkdir -p ${sysrootDir}/boot
make ARCH=${kernelTargetArch} CROSS_COMPILE=${toolchainTuple}- INSTALL_PATH=${sysrootDir}/boot install
make ARCH=${kernelTargetArch} CROSS_COMPILE=${toolchainTuple}- INSTALL_MOD_PATH=${sysrootDir} modules_install

# Also install the kernel binary outside of the sysroot. Useful for running with QEMU
make ARCH=${kernelTargetArch} CROSS_COMPILE=${toolchainTuple}- INSTALL_PATH=${kernelStandaloneInstallDir} install