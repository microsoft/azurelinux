#!/bin/bash -x

QT_BRANCH=6.9.1
QT_VERSION=6.9.1

# Install fedora deps for qt6-qtbase, qt6-qttools
#sudo dnf builddep qt6-qtbase qt6-qttools qt6-qtwebengine -y
#sudo dnf install qt6-qtbase qt6-doctools -y
sudo dnf install -y cmake ninja-build clang-devel llvm-devel libdrm-devel dbus-devel python3-html5lib


# Clone full qt tree
#git clone -b $QT_BRANCH git://code.qt.io/qt/qt5.git qt6
git clone -b v$QT_VERSION git://code.qt.io/qt/qt5.git qt6

# Configure using fedora configure basic options
cd qt6 || return
#git submodule foreach "git checkout $QT_BRANCH || :"
git submodule foreach "git checkout v$QT_VERSION || :"
git submodule foreach "git fetch"
git submodule foreach "git pull"

# Init the base source
./init-repository

# Apply qtbase-tell-the-truth-about-private-API.patch from rpms/qt6-qtbase
pushd qtbase
patch -p1 < ../../qtbase-tell-the-truth-about-private-API.patch
popd

# hard-code docdir for now, rpm --eval %{_qt6_docdir} yields unexpanded %{_docdir}/qt6 , wtf -- rex
./configure -confirm-license -opensource -prefix $(rpm --eval "%{_qt6_prefix}") \
    -archdatadir $(rpm --eval "%{_qt6_archdatadir}") -bindir $(rpm --eval "%{_qt6_bindir}") \
    -libdir $(rpm --eval "%{_qt6_libdir}") -libexecdir $(rpm --eval "%{_qt6_libexecdir}") \
    -datadir $(rpm --eval "%{_qt6_datadir}") -docdir /usr/share/doc/qt6 \
    -examplesdir $(rpm --eval "%{_qt6_examplesdir}") -headerdir $(rpm --eval "%{_qt6_headerdir}") \
    -plugindir $(rpm --eval "%{_qt6_plugindir}") \
    -sysconfdir $(rpm --eval "%{_qt6_sysconfdir}") -translationdir $(rpm --eval "%{_qt6_translationdir}") \
    -platform linux-g++ -release -shared \
    -nomake examples -nomake tests -no-rpath -no-separate-debug-info -no-strip \
    -no-directfb 

cmake --build . --parallel
cmake --build . --target docs

# Install docs on tmp directory
DEST=${PWD}/install
rm -rf $DEST/ && mkdir -p ${DEST}

DESTDIR=$DEST cmake --build . --target install_docs

XZ_OPT="-T 2"
tar -C $DEST -cJf ../qt-doc-opensource-src-${QT_VERSION}.tar.xz .
