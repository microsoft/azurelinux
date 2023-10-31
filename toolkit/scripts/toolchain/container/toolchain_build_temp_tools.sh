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
cd build
../configure \
    --prefix=/tools \
    --with-sysroot=$LFS \
    --with-lib-path=/tools/lib \
    --target=$LFS_TGT \
    --disable-nls \
    --disable-werror \
    --enable-gprofng=no
make -j$(nproc)
mkdir -v /tools/lib && ln -sv lib /tools/lib64
make install
popd
rm -rf binutils-2.41

touch $LFS/logs/temptoolchain/status_binutils_pass1_complete

echo GCC-11.2.0 - Pass 1
tar xf gcc-11.2.0.tar.xz
pushd gcc-11.2.0
tar xf ../mpfr-4.2.1.tar.xz
mv -v mpfr-4.2.1 mpfr
tar xf ../gmp-6.3.0.tar.xz
mv -v gmp-6.3.0 gmp
tar xf ../mpc-1.3.1.tar.gz
mv -v mpc-1.3.1 mpc
case $(uname -m) in
    x86_64)
      for file in gcc/config/{linux,i386/linux{,64}}.h
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
    aarch64)
      for file in $(find gcc/config -name linux64.h -o -name linux.h -o -name sysv4.h -o -name linux-eabi.h -o -name linux-elf.h -o -name aarch64-linux.h)
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
esac
case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
  ;;
  aarch64)
    sed -e '/mabi.lp64=/s/lib64/lib/' -i.orig gcc/config/aarch64/t-aarch64-linux
  ;;
esac
patch -Np1 -i /tools/CVE-2023-4039.patch
mkdir -v build
cd       build
../configure                                       \
    --target=$LFS_TGT                              \
    --prefix=/tools                                \
    --with-glibc-version=2.11                      \
    --with-sysroot=$LFS                            \
    --with-newlib                                  \
    --without-headers                              \
    --with-local-prefix=/tools                     \
    --with-native-system-header-dir=/tools/include \
    --disable-nls                                  \
    --disable-shared                               \
    --disable-multilib                             \
    --disable-decimal-float                        \
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
popd
rm -rf gcc-11.2.0

touch $LFS/logs/temptoolchain/status_gcc_pass1_complete

KERNEL_VERSION="5.15.48.1"
echo Linux-${KERNEL_VERSION} API Headers
tar xf kernel-${KERNEL_VERSION}.tar.gz
pushd CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-${KERNEL_VERSION}
make mrproper
make headers
cp -rv usr/include/* /tools/include
popd
rm -rf CBL-Mariner-Linux-Kernel-rolling-lts-mariner-2-${KERNEL_VERSION}

touch $LFS/logs/temptoolchain/status_kernel_headers_complete

echo glibc-2.35
tar xf glibc-2.35.tar.xz
pushd glibc-2.35
patch -Np1 -i ../glibc-2.35-fhs-1.patch
mkdir -v build
cd       build
../configure                             \
      --prefix=/tools                    \
      --disable-werror                   \
      --host=$LFS_TGT                    \
      --build=$(../scripts/config.guess) \
      --enable-kernel=3.2                \
      --with-headers=/tools/include      \
      libc_cv_forced_unwind=yes          \
      libc_cv_c_cleanup=yes
make -j$(nproc)
make install
popd
rm -rf glibc-2.35

touch $LFS/logs/temptoolchain/status_glibc_complete

echo "Sanity check 1 (temptoolchain - glibc)"
set +e
echo 'int main(){}' > dummy.c
$LFS_TGT-gcc dummy.c
readelf -l a.out | grep ld-linux
case $(uname -m) in
  x86_64)
    echo Expected: '[Requesting program interpreter: /tools/lib64/ld-linux-x86-64.so.2]'
  ;;
  aarch64)
    echo Expected: '[Requesting program interpreter: /tools/lib/ld-linux-aarch64.so.1]'
  ;;
esac
rm -v dummy.c a.out
set -e
echo "End sanity check 1"

touch $LFS/logs/temptoolchain/status_sanity_check_1_complete

echo Libstdc++ from GCC-11.2.0
tar xf gcc-11.2.0.tar.xz
pushd gcc-11.2.0
mkdir -v build
cd       build
../libstdc++-v3/configure           \
    --host=$LFS_TGT                 \
    --prefix=/tools                 \
    --disable-multilib              \
    --disable-nls                   \
    --disable-libstdcxx-threads     \
    --disable-libstdcxx-pch         \
    --with-gxx-include-dir=/tools/$LFS_TGT/include/c++/11.2.0
make -j$(nproc)
make install
popd
rm -rf gcc-11.2.0

touch $LFS/logs/temptoolchain/status_libstdc++_complete

echo Binutils-2.41 - Pass 2
tar xf binutils-2.41.tar.xz
pushd binutils-2.41
mkdir -v build
cd build
CC=$LFS_TGT-gcc                  \
AR=$LFS_TGT-ar                   \
RANLIB=$LFS_TGT-ranlib           \
../configure                       \
        --prefix=/tools            \
        --disable-nls              \
        --disable-werror           \
        --with-lib-path=/tools/lib \
        --with-sysroot             \
        --enable-gprofng=no
make -j$(nproc)
make install
make -C ld clean
make -C ld LIB_PATH=/usr/lib:/lib
cp -v ld/ld-new /tools/bin
popd
rm -rf binutils-2.41

touch $LFS/logs/temptoolchain/status_binutils_pass2_complete

echo GCC-11.2.0 - Pass 2
tar xf gcc-11.2.0.tar.xz
pushd gcc-11.2.0
# fix issue compiling with glibc 2.34
sed -e '/static.*SIGSTKSZ/d' \
    -e 's/return kAltStackSize/return SIGSTKSZ * 4/' \
    -i libsanitizer/sanitizer_common/sanitizer_posix_libcdep.cpp
cat gcc/limitx.h gcc/glimits.h gcc/limity.h > \
  `dirname $($LFS_TGT-gcc -print-libgcc-file-name)`/include-fixed/limits.h
case $(uname -m) in
    x86_64)
      for file in gcc/config/{linux,i386/linux{,64}}.h
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
    aarch64)
      for file in $(find gcc/config -name linux64.h -o -name linux.h -o -name sysv4.h -o -name linux-eabi.h -o -name linux-elf.h -o -name aarch64-linux.h)
      do
        cp -uv $file{,.orig}
        sed -e 's@/lib\(64\)\?\(32\)\?/ld@/tools&@g' \
            -e 's@/usr@/tools@g' $file.orig > $file
        echo '
      #undef STANDARD_STARTFILE_PREFIX_1
      #undef STANDARD_STARTFILE_PREFIX_2
      #define STANDARD_STARTFILE_PREFIX_1 "/tools/lib/"
      #define STANDARD_STARTFILE_PREFIX_2 ""' >> $file
        touch $file.orig
      done
    ;;
esac
case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' \
        -i.orig gcc/config/i386/t-linux64
  ;;
  aarch64)
    sed -e '/mabi.lp64=/s/lib64/lib/' -i.orig gcc/config/aarch64/t-aarch64-linux
  ;;
esac
tar -xf ../mpfr-4.2.1.tar.xz
mv -v mpfr-4.2.1 mpfr
tar -xf ../gmp-6.3.0.tar.xz
mv -v gmp-6.3.0 gmp
tar -xf ../mpc-1.3.1.tar.gz
mv -v mpc-1.3.1 mpc
patch -Np1 -i /tools/CVE-2023-4039.patch
mkdir -v build
cd       build
CC=$LFS_TGT-gcc                                    \
CXX=$LFS_TGT-g++                                   \
AR=$LFS_TGT-ar                                     \
RANLIB=$LFS_TGT-ranlib                             \
../configure                                       \
    --prefix=/tools                                \
    --with-local-prefix=/tools                     \
    --with-native-system-header-dir=/tools/include \
    --enable-languages=c,c++                       \
    --disable-libstdcxx-pch                        \
    --disable-multilib                             \
    --disable-bootstrap                            \
    --disable-libgomp
make -j$(nproc)
make install
ln -sv gcc /tools/bin/cc
popd
rm -rf gcc-11.2.0

touch $LFS/logs/temptoolchain/status_gcc_pass2_complete

echo "Sanity check 2 (temptoolchain - gcc pass2)"
set +e
echo 'int main(){}' > dummy.c
cc dummy.c
readelf -l a.out | grep ld-linux
case $(uname -m) in
  x86_64)
    echo Expected: '[Requesting program interpreter: /tools/lib64/ld-linux-x86-64.so.2]'
  ;;
  aarch64)
    echo Expected: '[Requesting program interpreter: /tools/lib/ld-linux-aarch64.so.1]'
  ;;
esac
rm -v dummy.c a.out
set -e
echo "End sanity check 2"

touch $LFS/logs/temptoolchain/status_sanity_check_2_complete

echo M4-1.4.19
tar xf m4-1.4.19.tar.gz
pushd m4-1.4.19
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf m4-1.4.19

touch $LFS/logs/temptoolchain/status_m4_complete

echo Ncurses-6.4
tar xf ncurses-6.4.tar.gz
pushd ncurses-6.4
sed -i s/mawk// configure
./configure --prefix=/tools \
            --with-shared   \
            --without-debug \
            --without-ada   \
            --enable-widec  \
            --enable-overwrite
make -j$(nproc)
make install
echo "INPUT(-lncursesw)" > /tools/lib/libncurses.so
popd
rm -rf ncurses-6.4

touch $LFS/logs/temptoolchain/status_ncurses_complete

echo Bash-5.1.8
tar xf bash-5.1.8.tar.gz
pushd bash-5.1.8
./configure --prefix=/tools --without-bash-malloc
make -j$(nproc)
make install
ln -sv bash /tools/bin/sh
popd
rm -rf bash-5.1.8

touch $LFS/logs/temptoolchain/status_bash_complete

echo Bison-3.8.2
tar xf bison-3.8.2.tar.xz
pushd bison-3.8.2
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf bison-3.8.2

touch $LFS/logs/temptoolchain/status_bison_complete

echo Coreutils-8.32
tar xf coreutils-8.32.tar.xz
pushd coreutils-8.32
case $(uname -m) in
    aarch64)
        patch -Np1 -i /tools/coreutils-fix-get-sys_getdents-aarch64.patch
    ;;
esac
./configure --prefix=/tools --enable-install-program=hostname
make -j$(nproc)
make install
popd
rm -rf coreutils-8.32

touch $LFS/logs/temptoolchain/status_coreutils_complete

echo Diffutils-3.10
tar xf diffutils-3.10.tar.xz
pushd diffutils-3.10
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf diffutils-3.10

touch $LFS/logs/temptoolchain/status_diffutils_complete

echo File-5.45
tar xf file-5.45.tar.gz
pushd file-5.45
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf file-5.45

touch $LFS/logs/temptoolchain/status_file_complete

# "bzip2" should build after "file" to prevent error:
#/temptoolchain/lfs/tools/bin/../lib/gcc/x86_64-pc-linux-gnu/11.2.0/../../../../lib/libbz2.a(blocksort.o): warning: relocation against `stderr@@GLIBC_2.2.5' in read-only section `.text'
#collect2: error: ld returned 1 exit status
#Makefile:499: recipe for target 'libmagic.la' failed
echo Bzip2-1.0.8
tar xf bzip2-1.0.8.tar.gz
pushd bzip2-1.0.8
make -j$(nproc)
make PREFIX=/tools install
popd
rm -rf bzip2-1.0.8

touch $LFS/logs/temptoolchain/status_bzip2_complete

echo Findutils-4.9.0
tar xf findutils-4.9.0.tar.xz
pushd findutils-4.9.0
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf findutils-4.9.0

touch $LFS/logs/temptoolchain/status_findutils_complete

echo Gawk-5.2.2
tar xf gawk-5.2.2.tar.xz
pushd gawk-5.2.2
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf gawk-5.2.2

touch $LFS/logs/temptoolchain/status_gawk_complete

echo Gettext-0.22
tar xf gettext-0.22.tar.xz
pushd gettext-0.22
./configure --disable-shared
make -j$(nproc)
cp -v gettext-tools/src/{msgfmt,msgmerge,xgettext} /tools/bin
popd
rm -rf gettext-0.22

touch $LFS/logs/temptoolchain/status_gettext_complete

echo Grep-3.11
tar xf grep-3.11.tar.xz
pushd grep-3.11
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf grep-3.11

touch $LFS/logs/temptoolchain/status_grep_complete

echo Gzip-1.13
tar xf gzip-1.13.tar.xz
pushd gzip-1.13
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf gzip-1.13

touch $LFS/logs/temptoolchain/status_gzip_complete

echo Make-4.3
tar xf make-4.3.tar.gz
pushd make-4.3
./configure --prefix=/tools --without-guile
make -j$(nproc)
make install
popd
rm -rf make-4.3

touch $LFS/logs/temptoolchain/status_make_complete

echo Patch-2.7.6
tar xf patch-2.7.6.tar.xz
pushd patch-2.7.6
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf patch-2.7.6

touch $LFS/logs/temptoolchain/status_patch_complete

echo Perl-5.32.0
tar xf perl-5.32.0.tar.xz
pushd perl-5.32.0
sh Configure -des -Dprefix=/tools -Dlibs=-lm -Uloclibpth -Ulocincpth
# Using locally-built version of 'make' to avoid mismatch between the build machine's version
# and the version we've built above. During its build, Perl runs 'make' from within its 'Makefile', so
# we used to end up with the build machine's 4.2.1 version running a 4.3 version causing build errors.
/tools/bin/make -j$(nproc)
cp -v perl cpan/podlators/scripts/pod2man /tools/bin
mkdir -pv /tools/lib/perl5/5.32.0
cp -Rv lib/* /tools/lib/perl5/5.32.0
popd
rm -rf perl-5.32.0

touch $LFS/logs/temptoolchain/status_perl_complete

echo Python-3.9.13
tar xf Python-3.9.13.tar.xz
pushd Python-3.9.13
sed -i '/def add_multiarch_paths/a \        return' setup.py
./configure --prefix=/tools --without-ensurepip --enable-shared
make -j$(nproc)
make install
popd
rm -rf Python-3.9.13

touch $LFS/logs/temptoolchain/status_python_complete

echo Sed-4.9
tar xf sed-4.9.tar.xz
pushd sed-4.9
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf sed-4.9

touch $LFS/logs/temptoolchain/status_sed_complete

echo Tar-1.35
tar xf tar-1.35.tar.xz
pushd tar-1.35
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf tar-1.35

touch $LFS/logs/temptoolchain/status_tar_complete

echo Texinfo-7.0.3
tar xf texinfo-7.0.3.tar.xz
pushd texinfo-7.0.3
# fix issue building with glibc 2.34:
sed -e 's/__attribute_nonnull__/__nonnull/' \
    -i gnulib/lib/malloc/dynarray-skeleton.c
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf texinfo-7.0.3

touch $LFS/logs/temptoolchain/status_texinfo_complete

echo Xz-5.4.4
tar xf xz-5.4.4.tar.xz
pushd xz-5.4.4
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf xz-5.4.4

touch $LFS/logs/temptoolchain/status_xz_complete

echo Flex-2.6.4
tar xf flex-2.6.4.tar.gz
pushd flex-2.6.4
sed -i "/math.h/a #include <malloc.h>" src/flexdef.h
HELP2MAN=/tools/bin/true \
./configure --prefix=/tools
make -j$(nproc)
make install
popd
rm -rf flex-2.6.4

touch $LFS/logs/temptoolchain/status_flex_complete

touch $LFS/logs/temptoolchain/status_temp_toolchain_complete

echo Done with script
