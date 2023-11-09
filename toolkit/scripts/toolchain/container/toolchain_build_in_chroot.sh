#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

#
# Building packages in chroot with temporary toolchain packages
#

set -x

echo Calling script to create files:

sh /tools/toolchain_initial_chroot_setup.sh

echo Now, running the final build steps in chroot inside container

# Set BUILD_TARGET
case $(uname -m) in
    x86_64)
        BUILD_TARGET=x86_64-pc-linux-gnu
    ;;
    aarch64)
        BUILD_TARGET=aarch64-unknown-linux-gnu
    ;;
esac

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

echo "Sanity check 3 (raw toolchain - before building gcc)"
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

set -e
#
# Start building packages
#
cd /sources

touch /logs/status_building_temp_tools_in_chroot

echo Gettext-0.22
tar xf gettext-0.22.tar.xz
pushd gettext-0.22
./configure --disable-shared
make -j$(nproc)
cp -v gettext-tools/src/{msgfmt,msgmerge,xgettext} /usr/bin
popd
rm -rf gettext-0.22
touch /logs/status_gettext_complete

echo Bison-3.8.2
tar xf bison-3.8.2.tar.xz
pushd bison-3.8.2
./configure --prefix=/usr --docdir=/usr/share/doc/bison-3.8.2
make -j$(nproc)
make install
popd
rm -rf bison-3.8.2
touch /logs/status_bison_complete

echo Perl-5.38.0
tar xf perl-5.38.0.tar.xz
pushd perl-5.38.0
sh Configure -des                                        \
             -Dprefix=/usr                               \
             -Dvendorprefix=/usr                         \
             -Duseshrplib                                \
             -Dprivlib=/usr/lib/perl5/5.38/core_perl     \
             -Darchlib=/usr/lib/perl5/5.38/core_perl     \
             -Dsitelib=/usr/lib/perl5/5.38/site_perl     \
             -Dsitearch=/usr/lib/perl5/5.38/site_perl    \
             -Dvendorlib=/usr/lib/perl5/5.38/vendor_perl \
             -Dvendorarch=/usr/lib/perl5/5.38/vendor_perl
make -j$(nproc)
make install
popd
rm -rf perl-5.38.0
touch /logs/status_perl_complete

echo Python-3.9.13
tar xf Python-3.9.13.tar.xz
pushd Python-3.9.13
./configure --prefix=/usr   \
            --enable-shared \
            --without-ensurepip
make -j$(nproc)
make install
popd
rm -rf Python-3.9.13
touch /logs/status_python39_complete

echo Texinfo-7.0.3
tar xf texinfo-7.0.3.tar.xz
pushd texinfo-7.0.3
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf texinfo-7.0.3
touch /logs/status_texinfo_complete

echo util-linux-2.39.2
tar xf util-linux-2.39.2.tar.xz
pushd util-linux-2.39.2
mkdir -pv /var/lib/hwclock
./configure ADJTIME_PATH=/var/lib/hwclock/adjtime \
            --libdir=/usr/lib    \
            --runstatedir=/run   \
            --docdir=/usr/share/doc/util-linux-2.39.2 \
            --disable-chfn-chsh  \
            --disable-login      \
            --disable-nologin    \
            --disable-su         \
            --disable-setpriv    \
            --disable-runuser    \
            --disable-pylibmount \
            --disable-static     \
            --without-python
make -j$(nproc)
make install
popd
rm -rf util-linux-2.39.2
touch /logs/status_util-linux_complete

# 7.13. Cleaning up and Saving the Temporary System
rm -rf /usr/share/{info,man,doc}/*
find /usr/{lib,libexec} -name \*.la -delete
# do not delete /tools yet, contains rpm patch file
#rm -rf /tools

touch /logs/status_build_cross_temp_tools_done

echo glibc-2.38
tar xf glibc-2.38.tar.xz
pushd glibc-2.38
patch -Np1 -i ../glibc-2.38-fhs-1.patch
patch -Np1 -i ../glibc-2.38-memalign_fix-1.patch
mkdir -v build
cd       build
echo "rootsbindir=/usr/sbin" > configparms
../configure --prefix=/usr                          \
             --disable-werror                       \
             --enable-kernel=4.14                   \
             --enable-stack-protector=strong        \
             --with-headers=/usr/include            \
             libc_cv_slibdir=/usr/lib
make -j$(nproc)
touch /etc/ld.so.conf
sed '/test-installation/s@$(PERL)@echo not running@' -i ../Makefile
make install
sed '/RTLDLIST=/s@/usr@@g' -i /usr/bin/ldd
cp -v ../nscd/nscd.conf /etc/nscd.conf
mkdir -pv /var/cache/nscd
cat > /etc/ld.so.conf << "EOF"
# Begin /etc/ld.so.conf
/usr/local/lib
/opt/lib
# Add an include directory
include /etc/ld.so.conf.d/*.conf
EOF
mkdir -pv /etc/ld.so.conf.d
popd
rm -rf glibc-2.38

touch /logs/status_glibc_complete

echo Zlib-1.3
tar xf zlib-1.3.tar.xz
pushd zlib-1.3
./configure --prefix=/usr
make -j$(nproc)
make install
rm -fv /usr/lib/libz.a
popd
rm -rf zlib-1.3
touch /logs/status_zlib_complete

echo Bzip2-1.0.8
tar xf bzip2-1.0.8.tar.gz
pushd bzip2-1.0.8
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile
make -f Makefile-libbz2_so
make clean
make -j$(nproc)
make PREFIX=/usr install
cp -av libbz2.so.* /usr/lib
ln -sv libbz2.so.1.0.8 /usr/lib/libbz2.so
cp -v bzip2-shared /usr/bin/bzip2
for i in /usr/bin/{bzcat,bunzip2}; do
  ln -sfv bzip2 $i
done
rm -fv /usr/lib/libbz2.a
popd
rm -rf bzip2-1.0.8
touch /logs/status_bzip2_complete

echo Xz-5.4.4
tar xf xz-5.4.4.tar.xz
pushd xz-5.4.4
./configure --prefix=/usr    \
            --disable-static \
            --docdir=/usr/share/doc/xz-5.4.4
make -j$(nproc)
make install
popd
rm -rf xz-5.4.4
touch /logs/status_xz_complete

echo zstd-1.5.5
tar xf zstd-1.5.5.tar.gz
pushd zstd-1.5.5
make -j$(nproc) prefix=/usr
make prefix=/usr install
rm -v /usr/lib/libzstd.a
popd
rm -rf zstd-1.5.5
touch /logs/status_zstd_complete

echo File-5.45
tar xf file-5.45.tar.gz
pushd file-5.45
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf file-5.45
touch /logs/status_file_complete

echo Readline-8.2
tar xf readline-8.2.tar.gz
pushd readline-8.2
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install
patch -Np1 -i ../readline-8.2-upstream_fix-1.patch
./configure --prefix=/usr    \
            --disable-static \
            --with-curses    \
            --docdir=/usr/share/doc/readline-8.2
make SHLIB_LIBS="-lncursesw"
make SHLIB_LIBS="-lncursesw" install
popd
rm -rf readline-8.2
touch /logs/status_readline_complete

echo M4-1.4.19
tar xf m4-1.4.19.tar.gz
pushd m4-1.4.19
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf m4-1.4.19
touch /logs/status_m4_complete

echo Flex-2.6.4
tar xf flex-2.6.4.tar.gz
pushd flex-2.6.4
./configure --prefix=/usr --docdir=/usr/share/doc/flex-2.6.4 --disable-static
make -j$(nproc)
make install
ln -sv flex /usr/bin/lex
popd
rm -rf flex-2.6.4
touch /logs/status_flex_complete

echo Binutils-2.41
tar xf binutils-2.41.tar.xz
pushd binutils-2.41
mkdir -v build
cd build
../configure --prefix=/usr       \
             --sysconfdir=/etc   \
             --enable-gold       \
             --enable-ld=default \
             --enable-plugins    \
             --enable-shared     \
             --disable-werror    \
             --enable-64-bit-bfd \
             --with-system-zlib
#             --enable-install-libiberty
# libiberty.a used to be in binutils. Now it is in GCC.
make -j$(nproc) tooldir=/usr
make tooldir=/usr install
rm -fv /usr/lib/lib{bfd,ctf,ctf-nobfd,gprofng,opcodes,sframe}.a
popd
rm -rf binutils-2.41
touch /logs/status_binutils_complete

echo GMP-6.3.0
tar xf gmp-6.3.0.tar.xz
pushd gmp-6.3.0
# Remove optimizations
cp -v configfsf.guess config.guess
cp -v configfsf.sub   config.sub
./configure --prefix=/usr    \
            --enable-cxx     \
            --disable-static \
            --docdir=/usr/share/doc/gmp-6.3.0
make -j$(nproc)
make install
popd
rm -rf gmp-6.3.0
touch /logs/status_gmp_complete

echo MPFR-4.2.1
tar xf mpfr-4.2.1.tar.xz
pushd mpfr-4.2.1
./configure --prefix=/usr        \
            --disable-static     \
            --enable-thread-safe \
            --docdir=/usr/share/doc/mpfr-4.2.1
make -j$(nproc)
make install
popd
rm -rf mpfr-4.2.1
touch /logs/status_mpfr_complete

echo MPC-1.3.1
tar xf mpc-1.3.1.tar.gz
pushd mpc-1.3.1
./configure --prefix=/usr    \
            --disable-static \
            --docdir=/usr/share/doc/mpc-1.3.1
make -j$(nproc)
make install
popd
rm -rf mpc-1.3.1
touch /logs/status_libmpc_complete

echo libcap-2.69
tar xf libcap-2.69.tar.xz
pushd libcap-2.69
sed -i '/install -m.*STA/d' libcap/Makefile
make -j$(nproc) prefix=/usr lib=lib
make prefix=/usr lib=lib install
popd
rm -rf libcap-2.69
touch /logs/status_libcap_complete

echo GCC-13.2.0
tar xf gcc-13.2.0.tar.xz
pushd gcc-13.2.0
case $(uname -m) in
  x86_64)
    sed -e '/m64=/s/lib64/lib/' -i.orig gcc/config/i386/t-linux64
  ;;
  aarch64)
    sed -e '/mabi.lp64=/s/lib64/lib/' -i.orig gcc/config/aarch64/t-aarch64-linux
  ;;
esac
mkdir -v build
cd       build
../configure --prefix=/usr            \
             LD=ld                    \
             --enable-languages=c,c++ \
             --enable-default-pie     \
             --enable-default-ssp     \
             --disable-multilib       \
             --disable-bootstrap      \
             --disable-fixincludes    \
             --disable-libsanitizer                         \
             --with-system-zlib
make -j$(nproc)
make install
ln -svr /usr/bin/cpp /usr/lib
ln -sfv ../../libexec/gcc/$(gcc -dumpmachine)/13.2.0/liblto_plugin.so \
        /usr/lib/bfd-plugins/

# Sanity check
set +e
echo "Sanity check 5 (raw toolchain - gcc)"
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

mkdir -pv /usr/share/gdb/auto-load/usr/lib
mv -v /usr/lib/*gdb.py /usr/share/gdb/auto-load/usr/lib
popd
rm -rf gcc-13.2.0

touch /logs/status_gcc_complete

echo Pkgconf-2.0.2
tar xf pkgconf-2.0.2.tar.xz
pushd pkgconf-2.0.2
./configure --prefix=/usr              \
            --disable-static           \
            --docdir=/usr/share/doc/pkgconf-2.0.2
make -j$(nproc)
make install
# create symlinks for compatability with pkg-config
ln -sv pkgconf   /usr/bin/pkg-config
popd
rm -rf pkgconf-2.0.2
touch /logs/status_pkgconf_complete

echo Ncurses-6.4
tar xf ncurses-6.4.tar.gz
pushd ncurses-6.4
sed -i '/LIBTOOL_INSTALL/d' c++/Makefile.in
./configure --prefix=/usr           \
            --mandir=/usr/share/man \
            --with-shared           \
            --without-debug         \
            --without-normal        \
            --with-cxx-shared       \
            --enable-pc-files       \
            --enable-widec          \
            --with-pkg-config-libdir=/usr/lib/pkgconfig
make -j$(nproc)
make DESTDIR=$PWD/dest install
install -vm755 dest/usr/lib/libncursesw.so.6.4 /usr/lib
rm -v  dest/usr/lib/libncursesw.so.6.4
cp -av dest/* /
for lib in ncurses form panel menu ; do
    rm -vf                    /usr/lib/lib${lib}.so
    echo "INPUT(-l${lib}w)" > /usr/lib/lib${lib}.so
    ln -sfv ${lib}w.pc        /usr/lib/pkgconfig/${lib}.pc
done
rm -vf                     /usr/lib/libcursesw.so
echo "INPUT(-lncursesw)" > /usr/lib/libcursesw.so
ln -sfv libncurses.so      /usr/lib/libcurses.so
popd
rm -rf ncurses-6.4
touch /logs/status_ncurses_complete

echo Sed-4.9
tar xf sed-4.9.tar.xz
pushd sed-4.9
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf sed-4.9
touch /logs/status_sed_complete

echo Gettext-0.22
tar xf gettext-0.22.tar.xz
pushd gettext-0.22
./configure --prefix=/usr    \
            --disable-static \
            --docdir=/usr/share/doc/gettext-0.22
make -j$(nproc)
make install
chmod -v 0755 /usr/lib/preloadable_libintl.so
popd
rm -rf gettext-0.22
touch /logs/status_gettext_complete

echo Bison-3.8.2
tar xf bison-3.8.2.tar.xz
pushd bison-3.8.2
./configure --prefix=/usr --docdir=/usr/share/doc/bison-3.8.2
make -j$(nproc)
make install
popd
rm -rf bison-3.8.2
touch /logs/status_bison_complete

echo Grep-3.11
tar xf grep-3.11.tar.xz
pushd grep-3.11
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf grep-3.11
touch /logs/status_grep_complete

echo Bash-5.2.15
tar xf bash-5.2.15.tar.gz
pushd bash-5.2.15
./configure --prefix=/usr             \
            --without-bash-malloc     \
            --with-installed-readline \
            --docdir=/usr/share/doc/bash-5.2.15
make -j$(nproc)
make install
popd
rm -rf bash-5.2.15
touch /logs/status_bash_complete

# Login again to use new bash?
#exec /usr/bin/bash --login

echo Libtool-2.4.7
tar xf libtool-2.4.7.tar.xz
pushd libtool-2.4.7
./configure --prefix=/usr
make -j$(nproc)
make install
rm -fv /usr/lib/libltdl.a
popd
rm -rf libtool-2.4.7
touch /logs/status_libtool_complete

echo GDBM-1.23
tar xf gdbm-1.23.tar.gz
pushd gdbm-1.23
./configure --prefix=/usr    \
            --disable-static \
            --enable-libgdbm-compat
make -j$(nproc)
make install
popd
rm -rf gdbm-1.23
touch /logs/status_gdbm_complete

echo gperf-3.1
tar xf gperf-3.1.tar.gz
pushd gperf-3.1
./configure --prefix=/usr --docdir=/usr/share/doc/gperf-3.1
make -j$(nproc)
make install
popd
rm -rf gperf-3.1
touch /logs/status_gperf_complete

echo Expat-2.4.8
tar xf expat-2.4.8.tar.bz2
pushd expat-2.4.8
./configure --prefix=/usr    \
            --disable-static \
            --docdir=/usr/share/doc/expat-2.4.8
make -j$(nproc)
make install
popd
rm -rf expat-2.4.8
touch /logs/status_expat_complete

echo Perl-5.38.0
tar xf perl-5.38.0.tar.xz
pushd perl-5.38.0
export BUILD_ZLIB=False
export BUILD_BZIP2=0
sh Configure -des                                         \
             -Dprefix=/usr                                \
             -Dvendorprefix=/usr                          \
             -Dprivlib=/usr/lib/perl5/5.38/core_perl      \
             -Darchlib=/usr/lib/perl5/5.38/core_perl      \
             -Dsitelib=/usr/lib/perl5/5.38/site_perl      \
             -Dsitearch=/usr/lib/perl5/5.38/site_perl     \
             -Dvendorlib=/usr/lib/perl5/5.38/vendor_perl  \
             -Dvendorarch=/usr/lib/perl5/5.38/vendor_perl \
             -Dman1dir=/usr/share/man/man1                \
             -Dman3dir=/usr/share/man/man3                \
             -Dpager="/usr/bin/less -isR"                 \
             -Duseshrplib                                 \
             -Dusethreads
make -j$(nproc)
make install
unset BUILD_ZLIB BUILD_BZIP2
popd
rm -rf perl-5.38.0
touch /logs/status_perl_complete

echo Autoconf-2.71
tar xf autoconf-2.71.tar.xz
pushd autoconf-2.71
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf autoconf-2.71
touch /logs/status_autoconf_complete

echo Automake-1.16.5
tar xf automake-1.16.5.tar.gz
pushd automake-1.16.5
./configure --prefix=/usr --docdir=/usr/share/doc/automake-1.16.5
make -j$(nproc)
make install
popd
rm -rf automake-1.16.5
touch /logs/status_automake_complete

echo OpenSSL-1.1.1k
tar xf openssl-1.1.1k.tar.gz
pushd openssl-1.1.1k
sslarch=
./config --prefix=/usr \
         --openssldir=/etc/pki/tls \
         --libdir=lib \
         enable-ec_nistp_64_gcc_128 \
         shared \
         zlib-dynamic \
         ${sslarch} \
         no-mdc2 \
         no-sm2 \
         no-sm4 \
         '-DDEVRANDOM="\"/dev/urandom\""'
perl ./configdata.pm -d
make all -j$(nproc)
sed -i '/INSTALL_LIBS/s/libcrypto.a libssl.a//' Makefile
make MANSUFFIX=ssl install
popd
rm -rf openssl-1.1.1k
touch /logs/status_openssl_complete

echo Elfutils-0.189
tar xjf elfutils-0.189.tar.bz2
pushd elfutils-0.189
./configure \
    --prefix=/usr \
    --disable-debuginfod \
    --enable-libdebuginfod=dummy
make -j$(nproc)
make -C libelf install
install -vm644 config/libelf.pc /usr/lib/pkgconfig
rm /usr/lib/libelf.a
# Need to also install (libdw.so.1) to satisfy rpmbuild
make -C libdw install
# Need to install (eu-strip) as well
make install
popd
rm -rf elfutils-0.189
touch /logs/status_libelf_complete

echo Libffi-3.4.4
tar xf libffi-3.4.4.tar.gz
pushd libffi-3.4.4
# TODO: set generic build to avoid optimizations causing illegal operation errors on other processors
# options: https://gcc.gnu.org/onlinedocs/gcc-9.2.0/gcc/x86-Options.html
#          https://gcc.gnu.org/onlinedocs/gcc-9.2.0/gcc/AArch64-Options.html#AArch64-Options
# export CFLAGS
# export CXXFLAGS
# By default all package built using '-O2 -march=x86-64 -pipe' for CFLAGS and CXXFLAGS,
sed -e '/^includesdir/ s/$(libdir).*$/$(includedir)/' \
    -i include/Makefile.in
sed -e '/^includedir/ s/=.*$/=@includedir@/' \
    -e 's/^Cflags: -I${includedir}/Cflags:/' \
    -i libffi.pc.in
# Set GCC_ARCH
case $(uname -m) in
    x86_64)
        GCC_ARCH=x86-64
    ;;
    aarch64)
        GCC_ARCH=native
    ;;
esac
./configure \
    --prefix=/usr \
    --bindir=/bin \
    --libdir=/usr/lib \
    --disable-static \
    --with-gcc-arch=$GCC_ARCH
unset GCC_ARCH
#	CFLAGS="-O2 -g" \
#	CXXFLAGS="-O2 -g" \
# Libffi is causing error building: find: '/usr/src/mariner/BUILDROOT/libffi-3.4.2-1.cm1.x86_64//usr/lib64': No such file or directory
make -j$(nproc)
make install
popd
rm -rf libffi-3.4.4
touch /logs/status_libffi_complete

echo Python-3.9.13
tar xf Python-3.9.13.tar.xz
pushd Python-3.9.13
./configure --prefix=/usr       \
            --enable-shared     \
            --with-system-expat \
            --with-system-ffi
make -j$(nproc)
make install
chmod -v 755 /usr/lib/libpython3.9.so.1.0
chmod -v 755 /usr/lib/libpython3.so
ln -sfv pip3.9 /usr/bin/pip3
popd
rm -rf Python-3.9.13
touch /logs/status_python39_complete

echo Coreutils-9.4
tar xf coreutils-9.4.tar.xz
pushd coreutils-9.4
patch -Np1 -i ../coreutils-9.4-i18n-1.patch
autoreconf -fiv
FORCE_UNSAFE_CONFIGURE=1 ./configure \
            --prefix=/usr            \
            --enable-no-install-program=kill,uptime
make -j$(nproc)
make install
mv -v /usr/bin/chroot /usr/sbin
popd
rm -rf coreutils-9.4
touch /logs/status_coreutils_complete

echo Diffutils-3.10
tar xf diffutils-3.10.tar.xz
pushd diffutils-3.10
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf diffutils-3.10
touch /logs/status_diffutils_complete

echo Gawk-5.2.2
tar xf gawk-5.2.2.tar.xz
pushd gawk-5.2.2
sed -i 's/extras//' Makefile.in
./configure --prefix=/usr
make -j$(nproc)
make LN='ln -f' install
popd
rm -rf gawk-5.2.2
touch /logs/status_gawk_complete

echo Findutils-4.9.0
tar xf findutils-4.9.0.tar.xz
pushd findutils-4.9.0
./configure --prefix=/usr --localstatedir=/var/lib/locate
make -j$(nproc)
make install
popd
rm -rf findutils-4.9.0
touch /logs/status_findutils_complete

# Groff is only needed for perl and we might be able to remove it.
echo Groff-1.23.0
tar xf groff-1.23.0.tar.gz
pushd groff-1.23.0
PAGE=letter ./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf groff-1.23.0
touch /logs/status_groff_complete

echo Gzip-1.13
tar xf gzip-1.13.tar.xz
pushd gzip-1.13
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf gzip-1.13
touch /logs/status_gzip_complete

echo Libpipeline-1.5.7
tar xf libpipeline-1.5.7.tar.gz
pushd libpipeline-1.5.7
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf libpipeline-1.5.7
touch /logs/status_libpipeline_complete

echo Make-4.4.1
tar xf make-4.4.1.tar.gz
pushd make-4.4.1
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf make-4.4.1
touch /logs/status_make_complete

echo Patch-2.7.6
tar xf patch-2.7.6.tar.xz
pushd patch-2.7.6
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf patch-2.7.6
touch /logs/status_patch_complete

echo Tar-1.35
tar xf tar-1.35.tar.xz
pushd tar-1.35
FORCE_UNSAFE_CONFIGURE=1  \
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf tar-1.35
touch /logs/status_tar_complete

echo Texinfo-7.0.3
tar xf texinfo-7.0.3.tar.xz
pushd texinfo-7.0.3
./configure --prefix=/usr
make -j$(nproc)
make install
popd
rm -rf texinfo-7.0.3
touch /logs/status_texinfo_complete

echo Procps-ng-4.0.4
tar xf procps-ng-4.0.4.tar.xz
pushd procps-ng-4.0.4
./configure --prefix=/usr                            \
            --docdir=/usr/share/doc/procps-ng-4.0.4  \
            --disable-static                         \
            --disable-kill
make -j$(nproc)
make install
popd
rm -rf procps-ng-4.0.4
touch /logs/status_procpsng_complete

echo util-linux-2.39.2
tar xf util-linux-2.39.2.tar.xz
pushd util-linux-2.39.2
./configure ADJTIME_PATH=/var/lib/hwclock/adjtime \
            --bindir=/usr/bin    \
            --libdir=/usr/lib    \
            --runstatedir=/run   \
            --sbindir=/usr/sbin  \
            --disable-chfn-chsh  \
            --disable-login      \
            --disable-nologin    \
            --disable-su         \
            --disable-setpriv    \
            --disable-runuser    \
            --disable-pylibmount \
            --disable-static     \
            --without-python     \
            --without-systemd    \
            --without-systemdsystemunitdir \
            --docdir=/usr/share/doc/util-linux-2.39.2
make -j$(nproc)
make install
popd
rm -rf util-linux-2.39.2
touch /logs/status_util-linux_complete

#
# These next packages include rpm/rpmbuild and dependencies
#
echo Building RPM related packages
cd /sources

echo sqlite-autoconf-3360000
tar xf sqlite-autoconf-3360000.tar.gz
pushd sqlite-autoconf-3360000
./configure --prefix=/usr     \
        --disable-static  \
        --enable-fts5     \
        CFLAGS="-g -O2                    \
        -DSQLITE_ENABLE_FTS3=1            \
        -DSQLITE_ENABLE_FTS4=1            \
        -DSQLITE_ENABLE_COLUMN_METADATA=1 \
        -DSQLITE_ENABLE_UNLOCK_NOTIFY=1   \
        -DSQLITE_ENABLE_DBSTAT_VTAB=1     \
        -DSQLITE_SECURE_DELETE=1          \
        -DSQLITE_ENABLE_FTS3_TOKENIZER=1"
make -j$(nproc)
make install
popd
rm -rf sqlite-autoconf-3360000
touch /logs/status_sqlite-autoconf_complete

echo popt-1.19
tar xf popt-1.19.tar.gz
pushd popt-1.19
./configure --prefix=/usr \
        --disable-static \
        --build=$BUILD_TARGET
make -j$(nproc)
make install
popd
rm -rf popt-1.19
touch /logs/status_popt_complete

echo cpio-2.14
tar xjf cpio-2.14.tar.bz2
pushd cpio-2.14
./configure --prefix=/usr \
        --bindir=/bin \
        --enable-mt   \
        --with-rmt=/usr/libexec/rmt \
        --build=$BUILD_TARGET
make -j$(nproc)
make install
popd
rm -rf cpio-2.14
touch /logs/status_cpio_complete

echo libarchive-3.7.1
tar xf libarchive-3.7.1.tar.gz
pushd libarchive-3.7.1
./configure --prefix=/usr --disable-static
make -j$(nproc)
make install
popd
rm -rf libarchive-3.7.1
touch /logs/status_libarchive_complete

echo lua-5.4.6
tar xf lua-5.4.6.tar.gz
pushd lua-5.4.6
cat > lua.pc << "EOF"
V=5.4
R=5.4.6
prefix=/usr
INSTALL_BIN=${prefix}/bin
INSTALL_INC=${prefix}/include
INSTALL_LIB=${prefix}/lib
INSTALL_MAN=${prefix}/share/man/man1
INSTALL_LMOD=${prefix}/share/lua/${V}
INSTALL_CMOD=${prefix}/lib/lua/${V}
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include
Name: Lua
Description: An Extensible Extension Language
Version: ${R}
Requires:
Libs: -L${libdir} -llua -lm -ldl
Cflags: -I${includedir}
EOF
patch -Np1 -i ../lua-5.4.6-shared_library-1.patch
make linux
make INSTALL_TOP=/usr                \
     INSTALL_DATA="cp -d"            \
     INSTALL_MAN=/usr/share/man/man1 \
     TO_LIB="liblua.so liblua.so.5.4 liblua.so.5.4.6" \
     install
install -v -m644 -D lua.pc /usr/lib/pkgconfig/lua.pc
popd
rm -rf lua-5.4.6
touch /logs/status_lua_complete

DEBUGEDIT_WITH_VERSION=debugedit-5.0
echo $DEBUGEDIT_WITH_VERSION
tar xf "$DEBUGEDIT_WITH_VERSION".tar.xz
pushd "$DEBUGEDIT_WITH_VERSION"
./configure --prefix=/usr
make
make install
popd
rm -rf "$DEBUGEDIT_WITH_VERSION"
touch /logs/status_debugedit_complete

RPM_WITH_VERSION=rpm-4.17.0
RPM_FOLDER="$RPM_WITH_VERSION"-release
echo $RPM_WITH_VERSION
tar xf "$RPM_WITH_VERSION"-release.tar.gz
mv rpm-"$RPM_WITH_VERSION"-release "$RPM_FOLDER"
pushd "$RPM_FOLDER"

# Still not in the upstream
patch -Np1 -i /tools/rpm-define-RPM-LD-FLAGS.patch

# Do not build docs - pandoc dependency is not supplied in the toolchain.
sed -iE '/SUBDIRS/ s/docs //' Makefile.am
sed -iE '/Always build/,+16 d' Makefile.am

./autogen.sh --noconfigure
./configure --prefix=/usr \
        --enable-ndb \
        --without-selinux \
        --with-crypto=openssl \
        --with-vendor=mariner

make -j$(nproc)
make install
install -d /var/lib/rpm

rpm --initdb --root=/ --dbpath /var/lib/rpm
popd

rm -rf "$RPM_FOLDER"

# Fix the interpreter path for python replacing the first line
sed -i '1 s:.*:#!/usr/bin/python3:' pythondistdeps.py
install -p pythondistdeps.py /usr/lib/rpm/pythondistdeps.py
install -p pythondeps.sh /usr/lib/rpm/pythondeps.sh
install -p python.attr /usr/lib/rpm/fileattrs/python.attr

touch /logs/status_rpm_complete

# Cleanup
rm -rf /tmp/*
find /usr/lib /usr/libexec -name \*.la -delete
find /usr -depth -name $(uname -m)-lfs-linux-gnu\* | xargs rm -rf

echo "Sanity check 6 (raw toolchain - after build complete)"
gcc -v
echo "End sanity check 6"

touch /logs/status_building_in_chroot_complete
