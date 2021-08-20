#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

echo "jdk8-build-raw.sh"

cd /sources

echo sanity check - jdk8-build-raw.sh
gcc -v
ls -la /sources

echo Installing xorg libraries and dependencies

# Setting up the Xorg Build Environment
echo Setting up Xorg build env
export XORG_PREFIX=/usr
case $(uname -m) in
    x86_64)
        export XORG_CONFIG="--prefix=$XORG_PREFIX --sysconfdir=/etc --localstatedir=/var --disable-static"
    ;;
    aarch64)
        BUILD_TARGET=aarch64-unknown-linux-gnu
        export XORG_CONFIG="--prefix=$XORG_PREFIX --sysconfdir=/etc --localstatedir=/var --disable-static --build=$BUILD_TARGET"
    ;;
esac

# util-macros
echo util-macros-1.19.1
tar xf util-macros-1.19.1.tar.bz2
pushd util-macros-1.19.1
./configure $XORG_CONFIG
make install
popd
rm -rf util-macros-1.19.1

# xorg-protocol-headers
echo xorg-protocol-headers
cat > proto-7.md5 << "EOF"
1a05fb01fa1d5198894c931cf925c025  bigreqsproto-1.1.2.tar.bz2
98482f65ba1e74a08bf5b056a4031ef0  compositeproto-0.4.2.tar.bz2
998e5904764b82642cc63d97b4ba9e95  damageproto-1.2.1.tar.bz2
4ee175bbd44d05c34d43bb129be5098a  dmxproto-2.3.1.tar.bz2
b2721d5d24c04d9980a0c6540cb5396a  dri2proto-2.8.tar.bz2
a3d2cbe60a9ca1bf3aea6c93c817fee3  dri3proto-1.0.tar.bz2
e7431ab84d37b2678af71e29355e101d  fixesproto-5.0.tar.bz2
36934d00b00555eaacde9f091f392f97  fontsproto-2.1.3.tar.bz2
5565f1b0facf4a59c2778229c1f70d10  glproto-1.4.17.tar.bz2
b290a463af7def483e6e190de460f31a  inputproto-2.3.2.tar.bz2
94afc90c1f7bef4a27fdd59ece39c878  kbproto-1.0.7.tar.bz2
92f9dda9c870d78a1d93f366bcb0e6cd  presentproto-1.1.tar.bz2
a46765c8dcacb7114c821baf0df1e797  randrproto-1.5.0.tar.bz2
1b4e5dede5ea51906f1530ca1e21d216  recordproto-1.14.2.tar.bz2
a914ccc1de66ddeb4b611c6b0686e274  renderproto-0.11.1.tar.bz2
cfdb57dae221b71b2703f8e2980eaaf4  resourceproto-1.2.0.tar.bz2
edd8a73775e8ece1d69515dd17767bfb  scrnsaverproto-1.2.2.tar.bz2
fe86de8ea3eb53b5a8f52956c5cd3174  videoproto-2.3.3.tar.bz2
5f4847c78e41b801982c8a5e06365b24  xcmiscproto-1.2.2.tar.bz2
70c90f313b4b0851758ef77b95019584  xextproto-7.3.0.tar.bz2
120e226ede5a4687b25dd357cc9b8efe  xf86bigfontproto-1.2.0.tar.bz2
a036dc2fcbf052ec10621fd48b68dbb1  xf86dgaproto-2.1.tar.bz2
1d716d0dac3b664e5ee20c69d34bc10e  xf86driproto-2.1.1.tar.bz2
e793ecefeaecfeabd1aed6a01095174e  xf86vidmodeproto-2.3.1.tar.bz2
9959fe0bfb22a0e7260433b8d199590a  xineramaproto-1.2.1.tar.bz2
16791f7ca8c51a20608af11702e51083  xproto-7.0.31.tar.bz2
EOF

md5sum -c ./proto-7.md5
for package in $(grep -v '^#' ./proto-7.md5 | awk '{print $2}')
do
  packagedir=${package%.tar.bz2}
  tar -xf $package
  pushd $packagedir
  ./configure $XORG_CONFIG
  make install
  popd
  rm -rf $packagedir
done

cd /sources

# libXau
echo libXau
tar xf libXau-1.0.8.tar.bz2
pushd libXau-1.0.8
./configure $XORG_CONFIG
make
make install
popd
rm -rf libXau-1.0.8

# xcb-proto
echo xcb-proto
tar xf xcb-proto-1.12.tar.bz2
pushd xcb-proto-1.12
patch -Np1 -i ../xcb-proto-1.12-python3-1.patch
./configure $XORG_CONFIG
make install
popd
rm -rf xcb-proto-1.12

# libxcb
echo libxcb-1.12
tar xf libxcb-1.12.tar.bz2
pushd libxcb-1.12
patch -Np1 -i ../libxcb-1.12-python3-1.patch
sed -i "s/pthread-stubs//" configure &&
./configure $XORG_CONFIG      \
            --enable-xinput   \
            --without-doxygen \
            --docdir='${datadir}'/doc/libxcb-1.12 &&
make
make install
popd
rm -rf libxcb-1.12

# freetype 2
echo freetype-2.9.1
tar xf freetype-2.9.1.tar.gz
pushd freetype-2.9.1
sed -ri "s:.*(AUX_MODULES.*valid):\1:" modules.cfg
sed -r "s:.*(#.*SUBPIXEL_RENDERING) .*:\1:" \
    -i include/freetype/config/ftoption.h
./configure --prefix=/usr --disable-static
make
make install
install -v -m755 -d /usr/share/doc/freetype-2.9.1
cp -v -R docs/*     /usr/share/doc/freetype-2.9.1
popd
rm -rf freetype-2.9.1

# fontconfig
echo fontconfig-2.13.91
tar xf fontconfig-2.13.91.tar.gz
pushd fontconfig-2.13.91
rm -f src/fcobjshash.h
./configure --prefix=/usr        \
            --sysconfdir=/etc    \
            --localstatedir=/var \
            --disable-docs       \
            --docdir=/usr/share/doc/fontconfig-2.13.91
make
make install
popd
rm -rf fontconfig-2.13.91

# Xorg Libraries
echo Xorg Libraries
cat > lib-7.md5 << "EOF"
c5ba432dd1514d858053ffe9f4737dd8  xtrans-1.3.5.tar.bz2
0f618db70c4054ca67cee0cc156a4255  libX11-1.6.5.tar.bz2
52df7c4c1f0badd9f82ab124fb32eb97  libXext-1.3.3.tar.bz2
d79d9fe2aa55eb0f69b1a4351e1368f7  libFS-1.0.7.tar.bz2
addfb1e897ca8079531669c7c7711726  libICE-1.0.9.tar.bz2
499a7773c65aba513609fe651853c5f3  libSM-1.2.2.tar.bz2
7a773b16165e39e938650bcc9027c1d5  libXScrnSaver-1.2.2.tar.bz2
8f5b5576fbabba29a05f3ca2226f74d3  libXt-1.1.5.tar.bz2
41d92ab627dfa06568076043f3e089e4  libXmu-1.1.2.tar.bz2
20f4627672edb2bd06a749f11aa97302  libXpm-3.5.12.tar.bz2
e5e06eb14a608b58746bdd1c0bd7b8e3  libXaw-1.0.13.tar.bz2
07e01e046a0215574f36a3aacb148be0  libXfixes-5.0.3.tar.bz2
f7a218dcbf6f0848599c6c36fc65c51a  libXcomposite-0.4.4.tar.bz2
802179a76bded0b658f4e9ec5e1830a4  libXrender-0.9.10.tar.bz2
1e7c17afbbce83e2215917047c57d1b3  libXcursor-1.1.14.tar.bz2
0cf292de2a9fa2e9a939aefde68fd34f  libXdamage-1.1.4.tar.bz2
0920924c3a9ebc1265517bdd2f9fde50  libfontenc-1.1.3.tar.bz2
0d9f6dd9c23bf4bcbfb00504b566baf5  libXfont2-2.0.1.tar.bz2
331b3a2a3a1a78b5b44cfbd43f86fcfe  libXft-2.3.2.tar.bz2
1f0f2719c020655a60aee334ddd26d67  libXi-1.7.9.tar.bz2
9336dc46ae3bf5f81c247f7131461efd  libXinerama-1.1.3.tar.bz2
28e486f1d491b757173dd85ba34ee884  libXrandr-1.5.1.tar.bz2
45ef29206a6b58254c81bea28ec6c95f  libXres-1.0.7.tar.bz2
ef8c2c1d16a00bd95b9fdcef63b8a2ca  libXtst-1.2.3.tar.bz2
210b6ef30dda2256d54763136faa37b9  libXv-1.0.11.tar.bz2
4cbe1c1def7a5e1b0ed5fce8e512f4c6  libXvMC-1.0.10.tar.bz2
d7dd9b9df336b7dd4028b6b56542ff2c  libXxf86dga-1.1.4.tar.bz2
298b8fff82df17304dfdb5fe4066fe3a  libXxf86vm-1.1.4.tar.bz2
ba983eba5a9f05d152a0725b8e863151  libdmx-1.1.3.tar.bz2
d810ab17e24c1418dedf7207fb2841d4  libpciaccess-0.13.5.tar.bz2
4a4cfeaf24dab1b991903455d6d7d404  libxkbfile-1.0.9.tar.bz2
66662e76899112c0f99e22f2fc775a7e  libxshmfence-1.2.tar.bz2
EOF

md5sum -c ./lib-7.md5

for package in $(grep -v '^#' ./lib-7.md5 | awk '{print $2}')
do
  packagedir=${package%.tar.bz2}
  tar -xf $package
  pushd $packagedir
  case $packagedir in
    libxshmfence* )
      ./configure $XORG_CONFIG CFLAGS="$CFLAGS -D_GNU_SOURCE"
    ;;

    libICE* )
      ./configure $XORG_CONFIG ICE_LIBS=-lpthread
    ;;

    libXfont2-[0-9]* )
      ./configure $XORG_CONFIG --disable-devel-docs
    ;;

    libXt-[0-9]* )
      ./configure $XORG_CONFIG \
                  --with-appdefaultdir=/etc/X11/app-defaults
    ;;

    * )
      ./configure $XORG_CONFIG
    ;;
  esac
  make
  make install
  popd
  rm -rf $packagedir
  /sbin/ldconfig
done

# Cups
echo Cups-2.2.4
tar xf cups-2.2.4-source.tar.gz
pushd cups-2.2.4
sed -i '2062,2069d' cups/dest.c
sed -i 's:444:644:' Makedefs.in
sed -i '/MAN.EXT/s:.gz::' configure config-scripts/cups-manpages.m4
sed -i '/LIBGCRYPTCONFIG/d' config-scripts/cups-ssl.m4
aclocal  -I config-scripts
autoconf -I config-scripts
CC=gcc \
./configure --libdir=/usr/lib            \
            --disable-systemd            \
            --with-rcdir=/tmp/cupsinit   \
            --with-system-groups=lpadmin \
            --with-docdir=/usr/share/cups/doc-2.2.4
make
make install
rm -rf /tmp/cupsinit
ln -svnf ../cups/doc-2.2.4 /usr/share/doc/cups-2.2.4
popd
rm -rf cups-2.2.4

# cacerts
mkdir -pv /etc/ssl/certs/java

touch /logs/status_openjdk_raw_dependencies_complete