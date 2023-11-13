#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

#
# Perform sanity checks during raw toolchain build for validation
#
# usage: sanity_check.sh "1"
#    Performs the first sanity check

set -x

echo "sanity check script running"
LFS_TGT=$(uname -m)-lfs-linux-gnu
echo "LFS root is: '$LFS', LFS_TGT is '$LFS_TGT'"

if [[ "$1" == "1" ]]; then
    echo "sanity check 1"
    echo "sanity check 1 (temptoolchain - glibc)"
    set +e
    $LFS_TGT-gcc -v
    echo 'int main(){}' | $LFS_TGT-gcc -xc -
    readelf -l a.out | grep ld-linux
    case $(uname -m) in
    x86_64)
        echo Expected: '[Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]'
    ;;
    aarch64)
        echo Expected: '[Requesting program interpreter: /tools/lib/ld-linux-aarch64.so.1]'
    ;;
    esac
    rm -v a.out
    set -e
    echo "End sanity check 1"
    touch $LFS/logs/temptoolchain/status_sanity_check_1_complete
fi

if [[ "$1" == "2" ]]; then
    echo "sanity check 2"
fi

if [[ "$1" == "3" ]]; then
    echo "sanity check 3"
    echo Printing debug info
    echo Path: $PATH
    ls -la /bin/bash
    ls -la /bin/sh
    ls -la /bin
    ls -la /tools
    ls -la /tools/bin
    ls -la /tools/lib
    ls -la /lib64
    ls /tools/bin
    ls /tools/sbin
    ls /bin
    ls /
    ls /usr/bin
    ls /usr/sbin
    ls -la /usr/sbin
    ls -la /usr/bin
    ls -la /bin/bash
    ls -la /bin/sh

    echo "sanity check 3 (raw toolchain - before building gcc)"
    find / -name ld-linux-x86-64.so.2
    ls -la /lib64/ld-linux-x86-64.so.2
    ls -la /tools/lib/ld-linux-x86-64.so.2
    ls -la /lib64
    ls -la /lib64/ld-lsb-x86-64.so.3
    ls -la /lib64/ld-linux-x86-64.so.2
    file /tools/bin/gcc
    gcc -v
    echo "End sanity check 3"
    echo Finished printing debug info
fi

if [[ "$1" == "4" ]]; then
    echo "sanity check 4"
fi

if [[ "$1" == "5" ]]; then
    echo "sanity check 5"
    set +e
    echo "sanity check 5 (raw toolchain - gcc)"
    ldconfig -v
    ldconfig -p
    ldconfig
    gcc -dumpmachine
    sync
    echo 'int main(){}' > dummy.c
    cc dummy.c -v -Wl,--verbose &> dummy.log
    cat dummy.log
    readelf -l a.out | grep ld-linux
    echo Expected output: '[Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]'
    # Expected output:
    # [Requesting program interpreter: /lib64/ld-linux-x86-64.so.2]
    grep -o '/usr/lib.*/crt[1in].*succeeded' dummy.log
    # Expected output:
    # /usr/lib/gcc/x86_64-pc-linux-gnu/11.2.0/../../../../lib/crt1.o succeeded
    # /usr/lib/gcc/x86_64-pc-linux-gnu/11.2.0/../../../../lib/crti.o succeeded
    # /usr/lib/gcc/x86_64-pc-linux-gnu/11.2.0/../../../../lib/crtn.o succeeded
    grep -B4 '^ /usr/include' dummy.log
    # Expected output:
    # #include <...> search starts here:
    #  /usr/lib/gcc/x86_64-pc-linux-gnu/11.2.0/include
    #  /usr/local/include
    #  /usr/lib/gcc/x86_64-pc-linux-gnu/11.2.0/include-fixed
    #  /usr/include
    grep 'SEARCH.*/usr/lib' dummy.log |sed 's|; |\n|g'
    # Expected output:
    # SEARCH_DIR("/usr/x86_64-pc-linux-gnu/lib64")
    # SEARCH_DIR("/usr/local/lib64")
    # SEARCH_DIR("/lib64")
    # SEARCH_DIR("/usr/lib64")
    # SEARCH_DIR("/usr/x86_64-pc-linux-gnu/lib")
    # SEARCH_DIR("/usr/local/lib")
    # SEARCH_DIR("/lib")
    # SEARCH_DIR("/usr/lib");
    grep "/lib.*/libc.so.6 " dummy.log
    echo Expected output: 'attempt to open /lib/libc.so.6 succeeded'
    # Expected output:
    # attempt to open /lib/libc.so.6 succeeded
    grep found dummy.log
    echo Expected output: 'found ld-linux-x86-64.so.2 at /lib/ld-linux-x86-64.so.2'
    # Expected output:
    # found ld-linux-x86-64.so.2 at /lib/ld-linux-x86-64.so.2
    rm -v dummy.c a.out dummy.log
    echo "End sanity check 5"
    set -e
fi

if [[ "$1" == "6" ]]; then
    echo "sanity check 6"
    echo "sanity check 6 (raw toolchain - after build complete)"
    gcc -v
    echo "End sanity check 6"
fi
