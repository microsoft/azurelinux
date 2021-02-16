# This script assumes that gcc_cross.sh has been run with the gcc extracted sources at $HOME/cross/gcc-9.1.0 and the gcc cross compilation binaries at /opt/cross/bin

cd $HOME/cross/gcc-9.1.0

# version 2021a installed via apt-get
# version 2019c in tzdata spec file
DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata

# version 1.6.1-1 installed via apt-get
# version 1.6.2 in dejagnu spec file
sudo apt-get install -y dejagnu

# version 6.5 installed via apt-get and texinfo spec file
sudo apt install -y texinfo
./contrib/download_prerequisites
cd ../build-gcc
export PATH="/opt/cross/bin":$PATH

# for less verbose output, remove the "-v -v"
make -j$(nproc) -k check-gcc RUNTESTFLAGS="-v -v compile.exp"

# version 2.7.15 installed via apt-get
# version 2.7.18 in python spec file
sudo apt-get install -y python
if ../gcc-9.1.0/contrib/testsuite-management/validate_failures.py; then
    echo "compile.exp tests passed"
else
    echo "compile.exp tests failed. Stopping..."
    exit 1
fi
