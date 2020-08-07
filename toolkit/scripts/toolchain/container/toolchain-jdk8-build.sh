#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -x
set -e

if [[ -z "$LFS" ]]; then
        echo "Must define LFS in environment" 1>&2
        exit 1
fi
echo "toolchain-jdk8-build.sh - LFS root is: $LFS"

cd ${LFS}/sources

export PATH=/bin:/usr/bin:/sbin:/usr/sbin
# Set CPATH, BOOT_JDK_VERSION and FREETYPE_LIB_PATH
case $(uname -m) in
    x86_64)
        version=212-b04
        bootstrapjdkversion=8
        export CPATH=/usr/include:/usr/include/x86_64-linux-gnu
        BOOT_JDK_VERSION=/usr/lib/jvm/java-${bootstrapjdkversion}-openjdk-amd64
        FREETYPE_LIB_PATH=/usr/lib/x86_64-linux-gnu
    ;;
    aarch64)
        version_install=1.8.0.181
        version=181-b13
        bootstrapjdkversion=8
        export CPATH=/usr/include:/usr/include/aarch64-linux-gnu
        BOOT_JDK_VERSION=/usr/lib/jvm/java-${bootstrapjdkversion}-openjdk-arm64
        FREETYPE_LIB_PATH=/usr/lib/aarch64-linux-gnu
    ;;
esac

echo Building bootstrap openjdk8

case $(uname -m) in
    x86_64)

    if [ -d jdk8u${version} ]; then
    rm -rf jdk8u${version}
    fi

    mkdir -pv jdk8u${version}
    tar -xvjf jdk8u212-b04.tar.bz2 --strip-components=1 -C jdk8u${version}
    for subproject in corba hotspot jaxp jaxws langtools jdk nashorn; do
        if [ ! -f jdk8u${version}/${subproject}.tar.bz2 ]; then
            cp jdk8u${version}-${subproject}.tar.bz2 jdk8u${version}/${subproject}.tar.bz2
        fi
    done

    pushd jdk8u${version}

    for subproject in corba hotspot jaxp jaxws langtools jdk nashorn; do
        if [ ! -d ${subproject} ]; then
            mkdir -pv ${subproject} &&
            tar -xf ${subproject}.tar.bz2 --strip-components=1 -C ${subproject}
        fi
    done

    patch -Np1 -i ${LFS}/tools/Awt_build_headless_only.patch
    patch -Np1 -i ${LFS}/tools/check-system-ca-certs.patch

    chmod a+x ./configure
    unset JAVA_HOME &&
    ./configure \
        --prefix=${LFS}/usr \
        --with-sysroot=$LFS \
        --with-target-bits=64 \
        --with-boot-jdk=${BOOT_JDK_VERSION} \
        --disable-headful \
        --with-cacerts-file=/etc/ssl/certs/java/cacerts \
        --with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
        --with-extra-cflags="-std=gnu++98 -fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
        --with-freetype-include=/usr/include/freetype2 \
        --with-freetype-lib=${FREETYPE_LIB_PATH} \
        --with-stdc++lib=dynamic \
        --disable-zip-debug-info

    make \
        DEBUG_BINARIES=true \
        BUILD_HEADLESS_ONLY=1 \
        OPENJDK_TARGET_OS=linux \
        JAVAC_FLAGS=-g \
        STRIP_POLICY=no_strip \
        DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
        CLASSPATH=${BOOT_JDK_VERSION}/jre \
        POST_STRIP_CMD="" \
        LOG=trace \
        SCTP_WERROR=

    _libdir=/usr/lib
    _bindir=/usr/bin

    make DESTDIR=${LFS} install \
        BUILD_HEADLESS_ONLY=yes \
        OPENJDK_TARGET_OS=linux \
        DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
        CLASSPATH=${BOOT_JDK_VERSION}/jre

    install -vdm755 ${LFS}${_libdir}/jvm/OpenJDK-${version}-bootstrap
    chown -R root:root ${LFS}${_libdir}/jvm/OpenJDK-${version}-bootstrap
    install -vdm755 ${LFS}${_bindir}
    find /usr/lib/jvm/java-1.8.0-openjdk-amd64/jre/lib/amd64 -iname \*.diz -delete
    mv /temptoolchain/lfs/usr/jvm/openjdk-1.8.0-internal/* ${LFS}${_libdir}/jvm/OpenJDK-${version}-bootstrap/

    popd
    rm -rf jdk8u${version}
    ;;

############
    aarch64)

    if [ -d aarch64-jdk8u${version} ]; then
    rm -rf aarch64-jdk8u${version}
    fi

    mkdir -pv aarch64-jdk8u${version}
    tar -xvjf aarch64-jdk8u181-b13.tar.bz2 --strip-components=1 -C aarch64-jdk8u${version}
    for subproject in corba hotspot jaxp jaxws langtools jdk nashorn; do
        if [ ! -f aarch64-jdk8u${version}/${subproject}.tar.bz2 ]; then
            cp aarch64-jdk8u${version}-${subproject}.tar.bz2 aarch64-jdk8u${version}/${subproject}.tar.bz2
        fi
    done

    pushd aarch64-jdk8u${version}

    for subproject in corba hotspot jaxp jaxws langtools jdk nashorn; do
        if [ ! -d ${subproject} ]; then
            mkdir -pv ${subproject} &&
            tar -xf ${subproject}.tar.bz2 --strip-components=1 -C ${subproject}
        fi
    done


    patch -Np1 -i ${LFS}/tools/Awt_build_headless_only.patch
    patch -Np1 -i ${LFS}/tools/check-system-ca-certs.patch

    rm jdk/src/solaris/native/sun/awt/CUPSfuncs.c
    sed -i "s#\"ft2build.h\"#<ft2build.h>#g" jdk/src/share/native/sun/font/freetypeScaler.c
    sed -i '0,/BUILD_LIBMLIB_SRC/s/BUILD_LIBMLIB_SRC/BUILD_HEADLESS_ONLY := 1\nOPENJDK_TARGET_OS := linux\n&/' jdk/make/lib/Awt2dLibraries.gmk

    echo check freetype lib
    ls -la /usr/lib
    ls -la ${FREETYPE_LIB_PATH}

    chmod a+x ./configure
    unset JAVA_HOME
    ./configure \
        --prefix=${LFS}/usr \
        --with-target-bits=64 \
        --with-boot-jdk=${BOOT_JDK_VERSION} \
        --disable-headful \
        --with-cacerts-file=/etc/ssl/certs/java/cacerts \
        --with-extra-cxxflags="-Wno-error -std=gnu++98 -fno-delete-null-pointer-checks -fno-lifetime-dse" \
        --with-extra-cflags="-std=gnu++98 -fno-delete-null-pointer-checks -Wno-error -fno-lifetime-dse" \
        --with-freetype-include=/usr/include/freetype2 \
        --with-freetype-lib=${FREETYPE_LIB_PATH} \
        --with-stdc++lib=dynamic

    make \
        DEBUG_BINARIES=true \
        BUILD_HEADLESS_ONLY=1 \
        OPENJDK_TARGET_OS=linux \
        JAVAC_FLAGS=-g \
        STRIP_POLICY=no_strip \
        DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
        CLASSPATH=${BOOT_JDK_VERSION}/jre \
        POST_STRIP_CMD="" \
        LOG=trace \
        SCTP_WERROR=

    _libdir=/usr/lib
    _bindir=/usr/bin

    make DESTDIR=${LFS} install \
        BUILD_HEADLESS_ONLY=yes \
        OPENJDK_TARGET_OS=linux \
        DISABLE_HOTSPOT_OS_VERSION_CHECK=ok \
        CLASSPATH=${BOOT_JDK_VERSION}/jre

    install -vdm755 ${LFS}${_libdir}/jvm/OpenJDK-${version_install}-bootstrap
    chown -R root:root ${LFS}${_libdir}/jvm/OpenJDK-${version_install}-bootstrap
    install -vdm755 ${LFS}${_bindir}
    find /usr/lib/jvm/java-1.8.0-openjdk-arm64/jre/lib/aarch64 -iname \*.diz -delete
    mv /temptoolchain/lfs/usr/jvm/openjdk-1.8.0-internal/* ${LFS}${_libdir}/jvm/OpenJDK-${version_install}-bootstrap/

    popd
    rm -rf openjdk-aarch64-jdk8u-aarch64-jdk8u181-b13
    ;;
esac

touch $LFS/logs/status_openjdk8_complete