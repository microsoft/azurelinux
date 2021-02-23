# This script assumes that gcc_cross.sh has been run with the gcc extracted sources at $HOME/cross/gcc-9.1.0 and the gcc cross compilation binaries at /opt/cross/bin
scriptDir="$( cd "$( dirname "$0" )" && pwd )"
gccDir=$HOME/cross/gcc-9.1.0
gccBuildDir=$HOME/cross/build-gcc
cd ${gccDir}

# delete previous test results
rm -rf ${gccBuildDir}/gcc/testsuite

# version 2021a installed via apt-get
# version 2019c in tzdata spec file
DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

# version 1.6.1-1 installed via apt-get
# version 1.6.2 in dejagnu spec file
sudo apt-get install -y dejagnu

# version 6.5 installed via apt-get and texinfo spec file
sudo apt install -y texinfo
./contrib/download_prerequisites
cd ${gccBuildDir}
export PATH="/opt/cross/bin":$PATH

# Run the compile only tests
# for less verbose output, remove the "-v -v"
make -j$(nproc) -k check-gcc RUNTESTFLAGS="-v -v compile.exp"

# version 2.7.15 installed via apt-get
# version 2.7.18 in python spec file
sudo apt-get install -y python
if ${gccDir}/contrib/testsuite-management/validate_failures.py; then
    echo "compile.exp tests passed"
else
    echo "compile.exp tests failed. Stopping..."
    exit 1
fi

# Run the execution tests via qemu user mode emulation

# version 2.11 installed via apt-get
# version 4.2 in qemu-kvm SPEC file
sudo apt-get install -y qemu qemu-user-static
export LD_LIBRARY_PATH="/opt/cross/aarch64-linux-gnu/lib64"
export QEMU_LD_PREFIX="/opt/cross/aarch64-linux-gnu/sysroot"

make -j$(nproc) -k check-gcc RUNTESTFLAGS="-v -v aarch64.exp execute.exp dg.exp ieee.exp builtins.exp"
cp ${scriptDir}/aarch64-linux-gnu.xfail ${gccDir}/contrib/testsuite-management
if ${gccDir}/contrib/testsuite-management/validate_failures.py; then
    echo "aarch64.exp execute.exp dg.exp ieee.exp builtins.exp tests passed"
else
    echo "aarch64.exp execute.exp dg.exp ieee.exp builtins.exp tests failed. Stopping..."
    exit 2
fi
