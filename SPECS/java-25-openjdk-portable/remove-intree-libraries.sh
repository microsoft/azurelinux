#!/bin/sh

# Arguments: <JDK TREE> <MINIMAL|FULL>
TREE=${1}
TYPE=${2}

ZIP_SRC=src/java.base/share/native/libzip/zlib/
FREETYPE_SRC=src/java.desktop/share/native/libfreetype/
JPEG_SRC=src/java.desktop/share/native/libjavajpeg/
GIF_SRC=src/java.desktop/share/native/libsplashscreen/giflib/
PNG_SRC=src/java.desktop/share/native/libsplashscreen/libpng/
LCMS_SRC=src/java.desktop/share/native/liblcms/

if test "x${TREE}" = "x"; then
    echo "$0 <JDK_TREE> (MINIMAL|FULL)";
    exit 1;
fi

if test "x${TYPE}" = "x"; then
    TYPE=minimal;
fi

if test "x${TYPE}" != "xminimal" -a "x${TYPE}" != "xfull"; then
    echo "Type must be minimal or full";
    exit 2;
fi

echo "Removing in-tree libraries from ${TREE}"
echo "Cleansing operation: ${TYPE}";

cd ${TREE}

echo "Removing built-in libs (they will be linked)"

# On full runs, allow for zlib & freetype having already been deleted by minimal
echo "Removing zlib"
if [ "x${TYPE}" = "xminimal" -a ! -d ${ZIP_SRC} ]; then
	echo "${ZIP_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -rvf ${ZIP_SRC}
echo "Removing freetype"
if [ "x${TYPE}" = "xminimal" -a ! -d ${FREETYPE_SRC} ]; then
	echo "${FREETYPE_SRC} does not exist. Refusing to proceed."
	exit 1
fi
rm -rvf ${FREETYPE_SRC}

# Minimal is limited to just zlib and freetype so finish here
if test "x${TYPE}" = "xminimal"; then
    echo "Finished.";
    exit 0;
fi

echo "Removing libjpeg"
if [ ! -f ${JPEG_SRC}/jdhuff.c ]; then # some file that should definitely exist
	echo "${JPEG_SRC} does not contain jpeg sources. Refusing to proceed."
	exit 1
fi	

rm -vf ${JPEG_SRC}/jcomapi.c
rm -vf ${JPEG_SRC}/jdapimin.c
rm -vf ${JPEG_SRC}/jdapistd.c
rm -vf ${JPEG_SRC}/jdcoefct.c
rm -vf ${JPEG_SRC}/jdcolor.c
rm -vf ${JPEG_SRC}/jdct.h
rm -vf ${JPEG_SRC}/jddctmgr.c
rm -vf ${JPEG_SRC}/jdhuff.c
rm -vf ${JPEG_SRC}/jdhuff.h
rm -vf ${JPEG_SRC}/jdinput.c
rm -vf ${JPEG_SRC}/jdmainct.c
rm -vf ${JPEG_SRC}/jdmarker.c
rm -vf ${JPEG_SRC}/jdmaster.c
rm -vf ${JPEG_SRC}/jdmerge.c
rm -vf ${JPEG_SRC}/jdphuff.c
rm -vf ${JPEG_SRC}/jdpostct.c
rm -vf ${JPEG_SRC}/jdsample.c
rm -vf ${JPEG_SRC}/jerror.c
rm -vf ${JPEG_SRC}/jerror.h
rm -vf ${JPEG_SRC}/jidctflt.c
rm -vf ${JPEG_SRC}/jidctfst.c
rm -vf ${JPEG_SRC}/jidctint.c
rm -vf ${JPEG_SRC}/jidctred.c
rm -vf ${JPEG_SRC}/jinclude.h
rm -vf ${JPEG_SRC}/jmemmgr.c
rm -vf ${JPEG_SRC}/jmemsys.h
rm -vf ${JPEG_SRC}/jmemnobs.c
rm -vf ${JPEG_SRC}/jmorecfg.h
rm -vf ${JPEG_SRC}/jpegint.h
rm -vf ${JPEG_SRC}/jpeglib.h
rm -vf ${JPEG_SRC}/jquant1.c
rm -vf ${JPEG_SRC}/jquant2.c
rm -vf ${JPEG_SRC}/jutils.c
rm -vf ${JPEG_SRC}/jcapimin.c
rm -vf ${JPEG_SRC}/jcapistd.c
rm -vf ${JPEG_SRC}/jccoefct.c
rm -vf ${JPEG_SRC}/jccolor.c
rm -vf ${JPEG_SRC}/jcdctmgr.c
rm -vf ${JPEG_SRC}/jchuff.c
rm -vf ${JPEG_SRC}/jchuff.h
rm -vf ${JPEG_SRC}/jcinit.c
rm -vf ${JPEG_SRC}/jconfig.h
rm -vf ${JPEG_SRC}/jcmainct.c
rm -vf ${JPEG_SRC}/jcmarker.c
rm -vf ${JPEG_SRC}/jcmaster.c
rm -vf ${JPEG_SRC}/jcparam.c
rm -vf ${JPEG_SRC}/jcphuff.c
rm -vf ${JPEG_SRC}/jcprepct.c
rm -vf ${JPEG_SRC}/jcsample.c
rm -vf ${JPEG_SRC}/jctrans.c
rm -vf ${JPEG_SRC}/jdtrans.c
rm -vf ${JPEG_SRC}/jfdctflt.c
rm -vf ${JPEG_SRC}/jfdctfst.c
rm -vf ${JPEG_SRC}/jfdctint.c
rm -vf ${JPEG_SRC}/jversion.h
rm -vf ${JPEG_SRC}/README

echo "Removing giflib"
if [ ! -d ${GIF_SRC} ]; then
	echo "${GIF_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -rvf ${GIF_SRC}

echo "Removing libpng"
if [ ! -d ${PNG_SRC} ]; then
	echo "${PNG_SRC} does not exist. Refusing to proceed."
	exit 1
fi	
rm -rvf ${PNG_SRC}

echo "Removing lcms"
if [ ! -d ${LCMS_SRC} ]; then
	echo "${LCMS_SRC} does not exist. Refusing to proceed."
	exit 1
fi
rm -vf ${LCMS_SRC}/cmscam02.c
rm -vf ${LCMS_SRC}/cmscgats.c
rm -vf ${LCMS_SRC}/cmscnvrt.c
rm -vf ${LCMS_SRC}/cmserr.c
rm -vf ${LCMS_SRC}/cmsgamma.c
rm -vf ${LCMS_SRC}/cmsgmt.c
rm -vf ${LCMS_SRC}/cmshalf.c
rm -vf ${LCMS_SRC}/cmsintrp.c
rm -vf ${LCMS_SRC}/cmsio0.c
rm -vf ${LCMS_SRC}/cmsio1.c
rm -vf ${LCMS_SRC}/cmslut.c
rm -vf ${LCMS_SRC}/cmsmd5.c
rm -vf ${LCMS_SRC}/cmsmtrx.c
rm -vf ${LCMS_SRC}/cmsnamed.c
rm -vf ${LCMS_SRC}/cmsopt.c
rm -vf ${LCMS_SRC}/cmspack.c
rm -vf ${LCMS_SRC}/cmspcs.c
rm -vf ${LCMS_SRC}/cmsplugin.c
rm -vf ${LCMS_SRC}/cmsps2.c
rm -vf ${LCMS_SRC}/cmssamp.c
rm -vf ${LCMS_SRC}/cmssm.c
rm -vf ${LCMS_SRC}/cmstypes.c
rm -vf ${LCMS_SRC}/cmsvirt.c
rm -vf ${LCMS_SRC}/cmswtpnt.c
rm -vf ${LCMS_SRC}/cmsxform.c
rm -vf ${LCMS_SRC}/lcms2.h
rm -vf ${LCMS_SRC}/lcms2_internal.h
rm -vf ${LCMS_SRC}/lcms2_plugin.h
