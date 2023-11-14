#!/bin/sh
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e
set -x
if [[ -z "$LFS" ]]; then
    echo "Must define LFS in environment" 1>&2
    exit 1
fi
echo LFS root is: $LFS
cd $LFS/sources

touch $LFS/logs/temptoolchain/status_temp_toolchain_build_started

cat /home/lfs/.bashrc
LFS_TGT=$(uname -m)-lfs-linux-gnu

echo Binutils-2.41 - Pass 1
tar xf binutils-2.41.tar.xz
pushd binutils-2.41
mkdir -v build
cd       build
../configure \
    --prefix=$LFS/tools \
    --with-sysroot=$LFS \
    --target=$LFS_TGT \
    --disable-nls \
    --disable-werror \
    --without-zstd \
    --enable-gprofng=no
make -j$(nproc)
make install
popd
rm -rf binutils-2.41

touch $LFS/logs/temptoolchain/status_binutils_pass1_complete

echo GCC-13.2.0 - Pass 1
tar xf gcc-13.2.0.tar.xz
pushd gcc-13.2.0
tar xf ../mpfr-4.2.1.tar.xz
mv -v mpfr-4.2.1 mpfr
tar xf ../gmp-6.3.0.tar.xz
mv -v gmp-6.3.0 gmp
tar xf ../mpc-1.3.1.tar.gz
mv -v mpc-1.3.1 mpc
case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64
  ;;
  aarch64)
    sed -e '/mabi.lp64=/s/lib64/lib/' -i.orig gcc/config/aarch64/t-aarch64-linux
  ;;
esac
# TODO: patch -Np1 -i /tools/CVE-2023-4039.patch
mkdir -v build
cd       build
../configure                                       \
    --target=$LFS_TGT                              \
    --prefix=$LFS/tools                            \
    --with-glibc-version=2.38                      \
    --with-sysroot=$LFS                            \
    --with-newlib                                  \
    --without-headers                              \
    --enable-default-pie                           \
    --enable-default-ssp                           \
    --disable-nls                                  \
    --disable-shared                               \
    --disable-multilib                             \
    --disable-threads                              \
    --disable-libatomic                            \
    --disable-libgomp                              \
    --disable-libquadmath                          \
    --disable-libssp                               \
    --disable-libvtv                               \
    --disable-libstdcxx                            \
    --enable-languages=c,c++
make -j$(nproc)
make install
cd ..
cat gcc/limitx.h gcc/glimits.h gcc/limity.h > \
  `dirname $($LFS_TGT-gcc -print-libgcc-file-name)`/include/limits.h
popd
rm -rf gcc-13.2.0

touch $LFS/logs/temptoolchain/status_gcc_pass1_complete

KERNEL_VERSION="6.1.58.1"
echo Linux-${KERNEL_VERSION} API Headers
tar xf kernel-${KERNEL_VERSION}.tar.gz
pushd CBL-Mariner-Linux-Kernel-rolling-lts-mariner-3-${KERNEL_VERSION}
make mrproper
make headers
find usr/include -type f ! -name '*.h' -delete
mkdir -pv $LFS/usr/include
cp -rv usr/include/* $LFS/usr/include
popd
rm -rf CBL-Mariner-Linux-Kernel-rolling-lts-mariner-3-${KERNEL_VERSION}

touch $LFS/logs/temptoolchain/status_kernel_headers_complete

echo glibc-2.38
tar xf glibc-2.38.tar.xz
pushd glibc-2.38
case $(uname -m) in
    x86_64) ln -sfv ../lib/ld-linux-x86-64.so.2 $LFS/lib64
            ln -sfv ../lib/ld-linux-x86-64.so.2 $LFS/lib64/ld-lsb-x86-64.so.3
    ;;
esac
patch -Np1 -i ../glibc-2.38-fhs-1.patch
patch -Np1 -i ../glibc-2.38-memalign_fix-1.patch
mkdir -v build
cd       build
echo "rootsbindir=/usr/sbin" > configparms
../configure                             \
      --prefix=/usr                      \
      --host=$LFS_TGT                    \
      --build=$(../scripts/config.guess) \
      --enable-kernel=4.14               \
      --with-headers=$LFS/usr/include    \
      libc_cv_slibdir=/usr/lib
make -j$(nproc)
make DESTDIR=$LFS install
# Fix a hard coded path to the executable loader in the ldd script:
sed '/RTLDLIST=/s@/usr@@g' -i $LFS/usr/bin/ldd
popd
rm -rf glibc-2.38

touch $LFS/logs/temptoolchain/status_glibc_complete

# sanity check 1
sh /tools/sanity_check.sh "1"

echo Libstdc++ from GCC-13.2.0
tar xf gcc-13.2.0.tar.xz
pushd gcc-13.2.0
# TODO: patch -Np1 -i /tools/CVE-2023-4039.patch
mkdir -v build
cd       build
../libstdc++-v3/configure           \
    --host=$LFS_TGT                 \
    --build=$(../config.guess)      \
    --prefix=/usr                   \
    --disable-multilib              \
    --disable-nls                   \
    --disable-libstdcxx-pch         \
    --with-gxx-include-dir=/tools/$LFS_TGT/include/c++/13.2.0
make -j$(nproc)
make DESTDIR=$LFS install
rm -v $LFS/usr/lib/lib{stdc++,stdc++fs,supc++}.la
popd
rm -rf gcc-13.2.0

touch $LFS/logs/temptoolchain/status_libstdc++_complete

# Cross compile temp tools

echo M4-1.4.19
tar xf m4-1.4.19.tar.gz
pushd m4-1.4.19
./configure --prefix=/usr \
            --host=$LFS_TGT \
            --build=$(build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf m4-1.4.19

touch $LFS/logs/temptoolchain/status_m4_complete

echo Ncurses-6.4
tar xf ncurses-6.4.tar.gz
pushd ncurses-6.4
sed -i s/mawk// configure
mkdir build
pushd build
  ../configure
  make -C include
  make -C progs tic
popd
./configure --prefix=/usr                \
            --host=$LFS_TGT              \
            --build=$(./config.guess)    \
            --with-shared                \
            --with-manpage-format=normal \
            --without-normal             \
            --with-cxx-shared            \
            --without-debug              \
            --without-ada                \
            --disable-stripping          \
            --enable-widec
make -j$(nproc)
make DESTDIR=$LFS install
make DESTDIR=$LFS TIC_PATH=$(pwd)/build/progs/tic install
echo "INPUT(-lncursesw)" > $LFS/usr/lib/libncurses.so
popd
rm -rf ncurses-6.4

touch $LFS/logs/temptoolchain/status_ncurses_complete

echo Bash-5.2.15
tar xf bash-5.2.15.tar.gz
pushd bash-5.2.15
./configure --prefix=/usr \
            --build=$(sh support/config.guess) \
            --host=$LFS_TGT                    \
            --without-bash-malloc
make -j$(nproc)
make DESTDIR=$LFS install
ln -sv bash $LFS/bin/sh
popd
rm -rf bash-5.2.15

touch $LFS/logs/temptoolchain/status_bash_complete

echo Coreutils-9.4
tar xf coreutils-9.4.tar.xz
pushd coreutils-9.4
./configure --prefix=/usr                     \
            --host=$LFS_TGT                   \
            --build=$(build-aux/config.guess) \
            --enable-install-program=hostname \
            --enable-no-install-program=kill,uptime \
            gl_cv_macro_MB_CUR_MAX_good=y
make -j$(nproc)
make DESTDIR=$LFS install
mv -v $LFS/usr/bin/chroot              $LFS/usr/sbin
popd
rm -rf coreutils-9.4

touch $LFS/logs/temptoolchain/status_coreutils_complete

echo Diffutils-3.10
tar xf diffutils-3.10.tar.xz
pushd diffutils-3.10
./configure --prefix=/usr   \
            --host=$LFS_TGT \
            --build=$(./build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf diffutils-3.10

touch $LFS/logs/temptoolchain/status_diffutils_complete

echo File-5.45
tar xf file-5.45.tar.gz
pushd file-5.45
mkdir build
pushd build
  ../configure --disable-bzlib      \
               --disable-libseccomp \
               --disable-xzlib      \
               --disable-zlib
  make
popd
./configure --prefix=/usr --host=$LFS_TGT --build=$(./config.guess)
make -j$(nproc) FILE_COMPILE=$(pwd)/build/src/file
make DESTDIR=$LFS install
rm -v $LFS/usr/lib/libmagic.la
popd
rm -rf file-5.45

touch $LFS/logs/temptoolchain/status_file_complete

echo Findutils-4.9.0
tar xf findutils-4.9.0.tar.xz
pushd findutils-4.9.0
./configure --prefix=/usr                   \
            --localstatedir=/var/lib/locate \
            --host=$LFS_TGT                 \
            --build=$(build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf findutils-4.9.0

touch $LFS/logs/temptoolchain/status_findutils_complete

echo Gawk-5.2.2
tar xf gawk-5.2.2.tar.xz
pushd gawk-5.2.2
sed -i 's/extras//' Makefile.in
./configure --prefix=/usr   \
            --host=$LFS_TGT \
            --build=$(build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf gawk-5.2.2

touch $LFS/logs/temptoolchain/status_gawk_complete

echo Grep-3.11
tar xf grep-3.11.tar.xz
pushd grep-3.11
./configure --prefix=/usr   \
            --host=$LFS_TGT \
            --build=$(./build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf grep-3.11

touch $LFS/logs/temptoolchain/status_grep_complete

echo Gzip-1.13
tar xf gzip-1.13.tar.xz
pushd gzip-1.13
./configure --prefix=/usr --host=$LFS_TGT
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf gzip-1.13

touch $LFS/logs/temptoolchain/status_gzip_complete

echo Make-4.4.1
tar xf make-4.4.1.tar.gz
pushd make-4.4.1
./configure --prefix=/usr   \
            --without-guile \
            --host=$LFS_TGT \
            --build=$(build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf make-4.4.1

touch $LFS/logs/temptoolchain/status_make_complete

echo Patch-2.7.6
tar xf patch-2.7.6.tar.xz
pushd patch-2.7.6
./configure --prefix=/usr   \
            --host=$LFS_TGT \
            --build=$(build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf patch-2.7.6

touch $LFS/logs/temptoolchain/status_patch_complete

echo Sed-4.9
tar xf sed-4.9.tar.xz
pushd sed-4.9
./configure --prefix=/usr   \
            --host=$LFS_TGT \
            --build=$(./build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf sed-4.9

touch $LFS/logs/temptoolchain/status_sed_complete

echo Tar-1.35
tar xf tar-1.35.tar.xz
pushd tar-1.35
./configure --prefix=/usr                     \
            --host=$LFS_TGT                   \
            --build=$(build-aux/config.guess)
make -j$(nproc)
make DESTDIR=$LFS install
popd
rm -rf tar-1.35

touch $LFS/logs/temptoolchain/status_tar_complete

echo Xz-5.4.4
tar xf xz-5.4.4.tar.xz
pushd xz-5.4.4
./configure --prefix=/usr                     \
            --host=$LFS_TGT                   \
            --build=$(build-aux/config.guess) \
            --disable-static                  \
            --docdir=/usr/share/doc/xz-5.4.4
make -j$(nproc)
make DESTDIR=$LFS install
rm -v $LFS/usr/lib/liblzma.la
popd
rm -rf xz-5.4.4

touch $LFS/logs/temptoolchain/status_xz_complete

# Binutils pass 2
echo Binutils-2.41 - Pass 2
tar xf binutils-2.41.tar.xz
pushd binutils-2.41
sed '6009s/$add_dir//' -i ltmain.sh
mkdir -v build
cd       build
../configure                   \
    --prefix=/usr              \
    --build=$(../config.guess) \
    --host=$LFS_TGT            \
    --disable-nls              \
    --enable-shared            \
    --enable-gprofng=no        \
    --disable-werror           \
    --enable-64-bit-bfd
make -j$(nproc)
make DESTDIR=$LFS install
rm -v $LFS/usr/lib/lib{bfd,ctf,ctf-nobfd,opcodes,sframe}.{a,la}
popd
rm -rf binutils-2.41

touch $LFS/logs/temptoolchain/status_binutils_pass2_complete

# Gcc pass 2
echo GCC-13.2.0 - Pass 2
tar xf gcc-13.2.0.tar.xz
pushd gcc-13.2.0
tar -xf ../mpfr-4.2.1.tar.xz
mv -v mpfr-4.2.1 mpfr
tar -xf ../gmp-6.3.0.tar.xz
mv -v gmp-6.3.0 gmp
tar -xf ../mpc-1.3.1.tar.gz
mv -v mpc-1.3.1 mpc
case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64
  ;;
  aarch64)
    sed -e '/mabi.lp64=/s/lib64/lib/' -i.orig gcc/config/aarch64/t-aarch64-linux
  ;;
esac
sed '/thread_header =/s/@.*@/gthr-posix.h/' \
    -i libgcc/Makefile.in libstdc++-v3/include/Makefile.in
# TODO: patch -Np1 -i /tools/CVE-2023-4039.patch
mkdir -v build
cd       build
../configure                                       \
    --build=$(../config.guess)                     \
    --host=$LFS_TGT                                \
    --target=$LFS_TGT                              \
    LDFLAGS_FOR_TARGET=-L$PWD/$LFS_TGT/libgcc      \
    --prefix=/usr                                  \
    --with-build-sysroot=$LFS                      \
    --enable-default-pie                           \
    --enable-default-ssp                           \
    --disable-nls                                  \
    --disable-multilib                             \
    --disable-libatomic                            \
    --disable-libgomp                              \
    --disable-libquadmath                          \
    --disable-libsanitizer                         \
    --disable-libssp                               \
    --disable-libvtv                               \
    --enable-languages=c,c++
make -j$(nproc)
make DESTDIR=$LFS install
ln -sv gcc $LFS/usr/bin/cc
popd
rm -rf gcc-13.2.0

touch $LFS/logs/temptoolchain/status_gcc_pass2_complete

touch $LFS/logs/temptoolchain/status_temp_toolchain_complete

echo Done with script
