# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with  tests
%bcond_without  compat_openvc_pc
%if %{without tests}
%bcond_with     extras_tests
%else
%bcond_without  extras_tests
%endif
# linters are enabled by default if BUILD_DOCS OR BUILD_EXAMPLES
%bcond_with     linters
%bcond_without  ffmpeg
%bcond_without  gstreamer
%bcond_with     eigen2
%bcond_without  eigen3
%bcond_without  opencl
%ifarch x86_64 %{arm}
%bcond_without  openni
%else
# we dont have openni in other archs
%bcond_with     openni
%endif
%bcond_without  tbb
%bcond_with     cuda
%bcond_without  xine
# Atlas need (missing: Atlas_CLAPACK_INCLUDE_DIR Atlas_CBLAS_LIBRARY Atlas_BLAS_LIBRARY Atlas_LAPACK_LIBRARY)
# LAPACK may use atlas or openblas since now it detect openblas, atlas is not used anyway, more info please
# check OpenCVFindLAPACK.cmake
%bcond_with     atlas
%bcond_without  openblas
%bcond_without  gdcm
%if 0%{?rhel} >= 8
%bcond_with     vtk
%else
%bcond_without  vtk
%endif

%ifarch x86_64
%bcond_without  libmfx
%else
%bcond_with     libmfx
%endif
%if 0%{?rhel} >= 8
%bcond_with  clp
%else
%bcond_without  clp
%endif
%ifarch %{java_arches}
%bcond_without  java
%else
%bcond_with  java
%endif

%if 0%{?fedora}
%bcond_without openexr
%else
%bcond_with openexr
%endif

%bcond_without  libva
%bcond_without  vulkan

%define _lto_cflags %{nil}

# If _cuda_version is unset
%if 0%{!?_cuda_version:1} && 0%{?with_cuda:1}
%global _cuda_version 11.2
%global _cuda_rpm_version 11-2
%global _cuda_prefix /usr/local/cuda-%{_cuda_version}
%bcond_without dnn_cuda
%endif

Name:           opencv
Version:        4.11.0
%global javaver %(foo=%{version}; echo ${foo//./})
%global majorver %(foo=%{version}; a=(${foo//./ }); echo ${a[0]} )
%global minorver %(foo=%{version}; a=(${foo//./ }); echo ${a[1]} )
%global padding  %(digits=00; num=%{minorver}; echo ${digits:${#num}:${#digits}} )
%global abiver   %(echo %{majorver}%{padding}%{minorver} )
Release:        12%{?dist}
Summary:        Collection of algorithms for computer vision
# This is normal three clause BSD.
License:        BSD-3-Clause AND Apache-2.0 AND ISC
URL:            https://opencv.org
# TO PREPARE TARBALLS FOR FEDORA
# Edit opencv-clean.sh and set VERSION, save file and run opencv-clean.sh
#
# Need to remove copyrighted lena.jpg images (rhbz#1295173)
# and SIFT/SURF (module xfeatures2d) from tarball, due to legal concerns.
#
Source0:        %{name}-clean-%{version}.tar.gz
Source1:        %{name}_contrib-clean-%{version}.tar.gz
%{?with_extras_tests:
#Source2:        %{name}_extra-clean-%{version}.tar.gz
}
Source3:        face_landmark_model.dat.xz
# SRC=v0.1.2d.zip ; wget https://github.com/opencv/ade/archive/$SRC; mv $SRC $(md5sum $SRC | cut -d' ' -f1)-$SRC
Source4:        962ce79e0b95591f226431f7b5f152cd-v0.1.2e.zip
Source5:        xorg.conf
%global wechat_commit 3487ef7cde71d93c6a01bb0b84aa0f22c6128f6b
%global wechat_shortcommit %(c=%{wechat_commit}; echo ${c:0:7})
%global wechat_gitdate 20230712
Source6:        https://github.com/WeChatCV/opencv_3rdparty/archive/%{wechat_commit}/wechat-%{wechat_gitdate}.git%{wechat_shortcommit}.tar.gz

Patch0:         opencv-4.1.0-install_3rdparty_licenses.patch
Patch3:         opencv.python.patch
Patch4:         https://github.com/opencv/opencv/pull/26750.patch
Patch5:         https://github.com/opencv/opencv/pull/26786.patch
# backport all PNG patches from 4.11.0 to 45aa502549 - fixes issues
# including complete failure to read PNGs on s390x (big-endian)
# https://bugzilla.redhat.com/show_bug.cgi?id=2345306
# https://github.com/opencv/opencv/issues/26913
Patch6:         0001-Merge-pull-request-26739-from-vrabaud-png_leak.patch
Patch7:         0002-Fix-remaining-bugs-in-PNG-reader.patch
Patch8:         0003-Merge-pull-request-26782-from-vrabaud-png_leak.patch
Patch9:         0004-Move-the-checks-to-read_chunk.patch
Patch10:        0005-minor-improvement-for-better-code-readibility.patch
Patch11:        0006-Merge-pull-request-26835-from-sturkmen72-patch-4.patch
Patch12:        0007-fix-for-large-tEXt-chunk.patch
Patch13:        0008-Merge-pull-request-26854-from-vrabaud-png_leak.patch
Patch14:        0009-Merge-pull-request-26872-from-sturkmen72-ImageEncode.patch
Patch15:        0010-Merge-pull-request-26915-from-mshabunin-fix-png-be.patch
# Fix build with Qt 6.9, by Atri Bhattacharya (thanks)
# https://github.com/opencv/opencv/issues/27223#issuecomment-2797750952
Patch16:        qt69.patch

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 2.6.3
BuildRequires:  chrpath
%{?with_cuda:
BuildRequires:  cuda-minimal-build-%{?_cuda_rpm_version}
BuildRequires:  pkgconfig(cublas-%{?_cuda_version})
BuildRequires:  pkgconfig(cufft-%{?_cuda_version})
BuildRequires:  pkgconfig(nppc-%{?_cuda_version})
%{?with_dnn_cuda:BuildRequires: libcudnn8-devel}
}
%{?with_eigen2:BuildRequires:  eigen2-devel}
%{?with_eigen3:BuildRequires:  eigen3-devel}
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
%if 0%{?fedora}
%ifnarch s390 s390x
BuildRequires:  libraw1394-devel
BuildRequires:  libdc1394-devel
%endif
%endif
BuildRequires:  jasper-devel
BuildRequires:  pkgconfig(libavif)
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libGL-devel
BuildRequires:  libv4l-devel
%{?with_openexr:
BuildRequires:  OpenEXR-devel
}
%{?with_openni:
BuildRequires:  openni-devel
%if 0%{?fedora}
BuildRequires:  openni-primesense
%endif
}
%{?with_tbb:
BuildRequires:  tbb-devel
}
BuildRequires:  zlib-devel
BuildRequires:  pkgconfig
BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-setuptools
%{?with_linters:
BuildRequires:  pylint
BuildRequires:  python3-flake8
}
BuildRequires:  swig >= 1.3.24
%{?with_ffmpeg:
BuildRequires:  pkgconfig(libavcodec)
BuildRequires:  pkgconfig(libavformat)
BuildRequires:  pkgconfig(libavutil)
BuildRequires:  pkgconfig(libswscale)
BuildRequires:  pkgconfig(libavdevice)
}
%if 0%{?fedora} || 0%{?rhel} > 7
%{?with_gstreamer:BuildRequires:  gstreamer1-devel gstreamer1-plugins-base-devel}
%else
%{?with_gstreamer:BuildRequires:  gstreamer-devel gstreamer-plugins-base-devel}
%endif
%{?with_xine:BuildRequires:  xine-lib-devel}
%{?with_opencl:BuildRequires:  opencl-headers}
BuildRequires:  libgphoto2-devel
BuildRequires:  libwebp-devel
BuildRequires:  tesseract-devel
BuildRequires:  protobuf-devel
BuildRequires:  gdal-devel
BuildRequires:  glog-devel
#BuildRequires:  doxygen
BuildRequires:  python3-beautifulsoup4
#for doc/doxygen/bib2xhtml.pl
#BuildRequires:  perl-open
BuildRequires:  gflags-devel
BuildRequires:  qt6-qtbase-devel
BuildRequires:  qt6-qt5compat-devel
BuildRequires:  libGL-devel
BuildRequires:  libGLU-devel
BuildRequires:  hdf5-devel
BuildRequires:  openjpeg2-devel
BuildRequires:  freetype-devel
BuildRequires:  harfbuzz-devel
# Module opencv_ovis disabled because of incompatible OGRE3D version < 1.11.5
# BuildRequires:  ogre-devel
%{?with_vtk:BuildRequires: vtk-devel}
%{?with_vtk:
  %{?with_java:
BuildRequires:  vtk-java
   }
}
%{?with_atlas:BuildRequires: atlas-devel}
#ceres-solver-devel push eigen3-devel and tbb-devel
%{?with_tbb:
  %{?with_eigen3:
# CERES support is disabled. Ceres Solver for reconstruction API is required.
# seems that ceres-solver is only needed for SFM algorithms but SFM algorithms are disabled because needs xfeatures2d
# BuildRequires:  ceres-solver-devel
  }
}
%{?with_openblas:
BuildRequires:  openblas-devel
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
}
%{?with_gdcm:BuildRequires: gdcm-devel}
%{?with_libmfx:BuildRequires:  libvpl-devel}
%{?with_clp:BuildRequires:  coin-or-Clp-devel}
%{?with_libva:BuildRequires:   libva-devel}
%{?with_java:
BuildRequires:  ant
BuildRequires:  java-devel
}
%{?with_vulkan:BuildRequires:  vulkan-headers}
#BuildRequires: flatbuffers-devel
%if %{with tests}
BuildRequires:  xorg-x11-drv-dummy
BuildRequires:  mesa-dri-drivers
%endif

Requires:       opencv-core%{_isa} = %{version}-%{release}
Requires:       opencv-data = %{version}-%{release}

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package        core
Summary:        OpenCV core libraries
Provides:       bundled(quirc) = 1.0
Obsoletes:      python2-%{name} < %{version}
# any removed modules should be listed here
Obsoletes:      %{name}-core < 4.8.0-2
Obsoletes:      %{name}-contrib < 4.8.0-2

%description    core
This package contains the OpenCV C/C++ core libraries.


%package        data
Summary:        OpenCV data
BuildArch:      noarch

%description    data
This package contains OpenCV data.


%global opencv_devel_requires %{name}-core%{_isa} = %{version}-%{release}

%define opencv_module_subpkg(m:d:) \
%global opencv_devel_requires %{opencv_devel_requires} %{name}-%{-m*}%{_isa} = %{version}-%{release}\
%define modulename %{-m:%{-m*}}%{!-m:%{error:Module name not defined}}\
%define moduledesc %{-d:%{-d*}}%{!-d:%{-m*}}\
%package %{modulename}\
Summary:  OpenCV module: %{moduledesc}\
Requires: %{name}-core%{_isa} = %{version}-%{release}\
\
%description %{modulename}\
This package contains the OpenCV %{moduledesc} module runtime.\
\
%files %{modulename}\
%{_libdir}/libopencv_%{modulename}.so.{%{abiver},%{version}}

# main modules
%opencv_module_subpkg -m calib3d -d %{quote:Camera Calibration and 3D Reconstruction}
%opencv_module_subpkg -m dnn -d %{quote:Deep Neural Network}
%opencv_module_subpkg -m features2d -d %{quote:2D Feature Detection}
%opencv_module_subpkg -m flann -d %{quote:Clustering and Search in Multi-dimensional Space}
%opencv_module_subpkg -m gapi -d %{quote:Graph API}
%opencv_module_subpkg -m highgui -d %{quote:High-level GUI}
%opencv_module_subpkg -m imgcodecs -d %{quote:Image Encoding/Decoding}
%opencv_module_subpkg -m imgproc -d %{quote:Image Processing}
%opencv_module_subpkg -m ml -d %{quote:Machine Learning}
%opencv_module_subpkg -m objdetect -d %{quote:Object Detection}
%opencv_module_subpkg -m photo -d %{quote:Computational Photography}
%opencv_module_subpkg -m stitching -d %{quote:Images stitching}
%opencv_module_subpkg -m video -d %{quote:Video Analysis}
%opencv_module_subpkg -m videoio -d %{quote:Video I/O}
# contrib/extra modules
%opencv_module_subpkg -m alphamat -d %{quote:Alpha Matting}
%opencv_module_subpkg -m aruco -d %{quote:Aruco Markers}
%opencv_module_subpkg -m bgsegm -d %{quote:Background Segmentation}
%opencv_module_subpkg -m bioinspired -d %{quote:Biologically-inspired Vision Models}
%opencv_module_subpkg -m ccalib -d %{quote:Custom Calibration Pattern}
%if %{with cuda}
%opencv_module_subpkg -m cudaarithm -d %{quote:CUDA Matrix Arithmatic}
%opencv_module_subpkg -m cudabgsegm -d %{quote:CUDA Background Segmentation}
%opencv_module_subpkg -m cudacodec -d %{quote:CUDA Video Encoding/Decoding}
%opencv_module_subpkg -m cudafeatures2d -d %{quote:CUDA 2D Feature Detection}
%opencv_module_subpkg -m cudafilters -d %{quote:CUDA Image Filtering}
%opencv_module_subpkg -m cudaimgproc -d %{quote:CUDA Image Processing}
%opencv_module_subpkg -m cudalegacy -d %{quote:CUDA Legacy Support}
%opencv_module_subpkg -m cudaobjdetect -d %{quote:CUDA Object Detection}
%opencv_module_subpkg -m cudaoptflow -d %{quote:CUDA Optical Flow}
%opencv_module_subpkg -m cudastereo -d %{quote:CUDA Stereo Correspondance}
%opencv_module_subpkg -m cudawarping -d %{quote:CUDA Image Warping}
%opencv_module_subpkg -m cudev -d %{quote:CUDA Device Layer}
%endif
%opencv_module_subpkg -m cvv -d %{quote:Interactive Computer Vision Visual Debugging}
%opencv_module_subpkg -m datasets -d %{quote:Datasets Framework}
%opencv_module_subpkg -m dnn_objdetect -d %{quote:Deep Neural Network Object Detection}
%opencv_module_subpkg -m dnn_superres -d %{quote:Deep Neural Network Super Resolution}
%opencv_module_subpkg -m dpm -d %{quote:Deformable Part-based Models}
%opencv_module_subpkg -m face -d %{quote:Face Analysis}
%opencv_module_subpkg -m freetype -d %{quote:Freetype/Harfbuzz UTF-8 Strings}
%opencv_module_subpkg -m fuzzy -d %{quote:Fuzzy Math-based Image Processing}
%opencv_module_subpkg -m hdf -d %{quote:HDF Data Format I/O}
%opencv_module_subpkg -m hfs -d %{quote:Heirarchical Feature Selection}
%opencv_module_subpkg -m img_hash -d %{quote:Image Hashing}
%opencv_module_subpkg -m intensity_transform -d %{quote:Intensity Transformation}
%opencv_module_subpkg -m line_descriptor -d %{quote:Extracted Line Binary Descriptor}
%opencv_module_subpkg -m mcc -d %{quote:Macbeth Chart}
%opencv_module_subpkg -m optflow -d %{quote:Optical Flow Algorithms}
#opencv_module_subpkg -m ovis -d %%{quote:OGRE 3D Visualiser}
%opencv_module_subpkg -m phase_unwrapping -d %{quote:Phase Unwrapping}
%opencv_module_subpkg -m plot -d %{quote:2D Plotting}
%opencv_module_subpkg -m quality -d %{quote:Image Quality Analysis}
%opencv_module_subpkg -m rapid -d %{quote:Silhouette based 3D Object Tracking}
%opencv_module_subpkg -m reg -d %{quote:Image Registration}
%opencv_module_subpkg -m rgbd -d %{quote:RGB-Depth Processing}
%opencv_module_subpkg -m saliency -d %{quote:Saliency}
%opencv_module_subpkg -m shape -d %{quote:Shape Distance and Matching}
%opencv_module_subpkg -m signal -d %{quote:Signal processing algorithms}
%opencv_module_subpkg -m stereo -d %{quote:Stereo Correspondance}
%opencv_module_subpkg -m structured_light -d %{quote:Structed Light}
%opencv_module_subpkg -m superres -d %{quote:Super Resolution}
%opencv_module_subpkg -m surface_matching -d %{quote:Surface Matching}
%opencv_module_subpkg -m text -d %{quote:Text Detection and Recognition}
%opencv_module_subpkg -m tracking -d %{quote:Tracking}
%opencv_module_subpkg -m videostab -d %{quote:Video Stabilization}
%if %{with vtk}
%opencv_module_subpkg -m viz -d %{quote:3D Visualizer}
%endif
%opencv_module_subpkg -m wechat_qrcode -d %{quote:WeChat QR code detector}
%opencv_module_subpkg -m ximgproc -d %{quote:Extended Image Processing}
%opencv_module_subpkg -m xobjdetect -d %{quote:Extended Object Detection}
%opencv_module_subpkg -m xphoto -d %{quote:Extended Photo Processing}


%package        devel
Summary:        Development files for using the OpenCV library
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}
Requires:       %{opencv_devel_requires}

%description    devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. You should consider installing opencv-doc
package.


%package        doc
Summary:        Documentation files
Requires:       opencv-devel = %{version}-%{release}
# Doc dependes on architecture, specifically whether the va_intel sample is installed depends on HAVE_VA
# BuildArch:      noarch
Provides:       %{name}-devel-docs = %{version}-%{release}
Obsoletes:      %{name}-devel-docs < %{version}-%{release}

%description    doc
This package contains the OpenCV documentation, samples and examples programs.


%package        -n python3-opencv
Summary:        Python3 bindings for apps which use OpenCV
Requires:       opencv%{_isa} = %{version}-%{release}
Requires:       python3-numpy
%{?%py_provides:%py_provides python3-%{name}}

%description    -n python3-opencv
This package contains Python3 bindings for the OpenCV library.


%package    java
Summary:    Java bindings for apps which use OpenCV
Requires:   java-headless
Requires:   javapackages-filesystem
Requires:   %{name}-core%{_isa} = %{version}-%{release}

%description java
This package contains Java bindings for the OpenCV library.


%prep
# autosetup doesn't work with 2 sources
# https://github.com/rpm-software-management/rpm/issues/1204
%setup -q -a1 %{?with_extras_tests:-a2} -a6

# we don't use pre-built contribs except quirc
pushd 3rdparty
shopt -s extglob
#rm -r !(openexr|openvx|quirc)
rm -r !(openvx|quirc|flatbuffers)
shopt -u extglob
popd &>/dev/null

%patch -P 0 -p1 -b .install_3rdparty_licenses
%patch -P 3 -p1 -b .python_install_binary
%patch -P 4 -p1 -b .VSX_intrinsics
%patch -P 5 -p1 -b .GCC15
%patch -P 6 -p1 -b .png1
%patch -P 7 -p1 -b .png2
%patch -P 8 -p1 -b .png3
%patch -P 9 -p1 -b .png4
%patch -P 10 -p1 -b .png5
%patch -P 11 -p1 -b .png6
%patch -P 12 -p1 -b .png7
%patch -P 13 -p1 -b .png8
%patch -P 14 -p1 -b .png9
%patch -P 15 -p1 -b .png10
%patch -P 16 -p1 -b .qt69


pushd %{name}_contrib-%{version}
#patch1 -p1 -b .install_cvv
popd

# Install face_landmark_model
mkdir -p .cache/data
install -pm 0644 %{S:3} .cache/data
pushd .cache/data
  xz -d face_landmark_model.dat.xz
  mv face_landmark_model.dat 7505c44ca4eb54b4ab1e4777cb96ac05-face_landmark_model.dat
popd
mkdir -p .cache/wechat_qrcode
mv opencv_3rdparty-%{wechat_commit}/detect.caffemodel .cache/wechat_qrcode/238e2b2d6f3c18d6c3a30de0c31e23cf-detect.caffemodel
mv opencv_3rdparty-%{wechat_commit}/detect.prototxt .cache/wechat_qrcode/6fb4976b32695f9f5c6305c19f12537d-detect.prototxt
mv opencv_3rdparty-%{wechat_commit}/sr.caffemodel .cache/wechat_qrcode/cbfcd60361a73beb8c583eea7e8e6664-sr.caffemodel
mv opencv_3rdparty-%{wechat_commit}/sr.prototxt .cache/wechat_qrcode/69db99927a70df953b471daaba03fbef-sr.prototxt

# Install ADE, needed for opencv_gapi
mkdir -p .cache/ade
install -pm 0644 %{S:4} .cache/ade/

%build
# enabled by default if libraries are presents at build time:
# GTK, GSTREAMER, 1394, V4L, eigen3
# non available on Fedora: FFMPEG, XINE
# disabling IPP because it is closed source library from intel

%cmake \
%if 0%{?fedora} > 38
 -DCMAKE_CXX_STANDARD=17 \
%endif
 -DCV_TRACE=OFF \
 -DWITH_IPP=OFF \
 -DWITH_ITT=OFF \
 -DWITH_QT=ON \
 -DWITH_OPENGL=ON \
%if ! %{with tests}
 -DBUILD_TESTS=OFF \
%endif
 -DOpenGL_GL_PREFERENCE=GLVND \
 -DWITH_GDAL=ON \
%{?with_openexr: -DWITH_OPENEXR=ON} \
%{!?with_openexr: -DWITH_OPENEXR=OFF} \
 -DCMAKE_SKIP_RPATH=ON \
 -DWITH_CAROTENE=OFF \
%ifarch x86_64 %{ix86}
 -DCPU_BASELINE=SSE2 \
%endif
 -DCMAKE_BUILD_TYPE=Release \
 %{?with_java: -DBUILD_opencv_java=ON \
 -DOPENCV_JAR_INSTALL_PATH=%{_jnidir} } \
 %{!?with_java: -DBUILD_opencv_java=OFF } \
 %{?with_tbb: -DWITH_TBB=ON } \
 %{!?with_gstreamer: -DWITH_GSTREAMER=OFF } \
 %{!?with_ffmpeg: -DWITH_FFMPEG=OFF } \
 %{?with_cuda: \
 -DWITH_CUDA=ON \
 -DCUDA_TOOLKIT_ROOT_DIR=%{?_cuda_prefix} \
 -DCUDA_VERBOSE_BUILD=ON \
 -DCUDA_PROPAGATE_HOST_FLAGS=OFF \
 -DCUDA_NVCC_FLAGS="-Xcompiler -fPIC" \
 %{?with_dnn_cuda:-DOPENCV_DNN_CUDA=ON} \
 } \
 %{?with_openni: -DWITH_OPENNI=ON } \
 %{!?with_xine: -DWITH_XINE=OFF } \
 -DBUILD_DOCS=ON \
 -DBUILD_EXAMPLES=ON \
 -DBUILD_opencv_python2=OFF \
 -DINSTALL_C_EXAMPLES=ON \
 -DINSTALL_PYTHON_EXAMPLES=ON \
 -DPYTHON3_EXECUTABLE=%{__python3} \
 -DPYTHON3_PACKAGES_PATH=%{python3_sitearch} \
 -DOPENCV_GENERATE_SETUPVARS=OFF \
 %{!?with_linters: \
 -DENABLE_PYLINT=OFF \
 -DENABLE_FLAKE8=OFF \
 } \
 -DBUILD_PROTOBUF=OFF \
 -DPROTOBUF_UPDATE_FILES=ON \
%{?with_opencl: -DOPENCL_INCLUDE_DIR=%{_includedir}/CL -DOPENCV_DNN_OPENCL=ON} \
%{!?with_opencl: -DWITH_OPENCL=OFF } \
 -DOPENCV_EXTRA_MODULES_PATH=opencv_contrib-%{version}/modules \
 -DWITH_LIBV4L=ON \
 -DWITH_OPENMP=ON \
 -DOPENCV_CONFIG_INSTALL_PATH=%{_lib}/cmake/OpenCV \
 -DOPENCV_GENERATE_PKGCONFIG=ON \
%{?with_extras_tests: -DOPENCV_TEST_DATA_PATH=opencv_extra-%{version}/testdata} \
 %{?with_gdcm: -DWITH_GDCM=ON } \
 -DWITH_IMGCODEC_GIF=ON \
 %{?with_libmfx: -DWITH_MFX=ON  -DWITH_GAPI_ONEVPL=ON} \
 %{?with_clp: -DWITH_CLP=ON } \
 %{?with_libva: -DWITH_VA=ON } \
 %{!?with_vtk: -DWITH_VTK=OFF} \
 %{?with_vulkan: -DWITH_VULKAN=ON -DVULKAN_INCLUDE_DIRS=%{_includedir}/vulkan }

%cmake_build


%install
%cmake_install
cd %{__cmake_builddir}/python_loader/
%py3_install -- --install-lib %{python3_sitearch}

rm -rf %{buildroot}%{_datadir}/OpenCV/licenses/
%if %{with java}
ln -s -r %{buildroot}%{_jnidir}/libopencv_java%{javaver}.so %{buildroot}%{_jnidir}/libopencv_java.so
ln -s -r %{buildroot}%{_jnidir}/opencv-%{javaver}.jar %{buildroot}%{_jnidir}/opencv.jar
%endif

# For compatibility with existing opencv.pc application
%{?with_compat_openvc_pc:
  ln -s opencv4.pc %{buildroot}%{_libdir}/pkgconfig/opencv.pc
}


%check
#ifnarch ppc64
%if %{with tests}
    cp %{S:5} %{__cmake_builddir}
    if [ -x /usr/libexec/Xorg ]; then
       Xorg=/usr/libexec/Xorg
    else
       Xorg=/usr/libexec/Xorg.bin
    fi
    $Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xorg.log -config ./xorg.conf -configdir . :99 &
    export DISPLAY=:99
    export LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/%{__cmake_builddir}/lib:$LD_LIBARY_PATH
    %ctest || :
%endif
#endif


%files
%doc README.md
%{_bindir}/opencv_*

%files data
%license LICENSE
%dir %{_datadir}/opencv4
%{_datadir}/opencv4/haarcascades
%{_datadir}/opencv4/lbpcascades
%{_datadir}/opencv4/valgrind*
%{_datadir}/opencv4/quality

%files core
%license LICENSE
%{_datadir}/licenses/opencv4/
%{_libdir}/libopencv_core.so.{%{abiver},%{version}}

%files devel
%dir %{_includedir}/opencv4
%{_includedir}/opencv4/opencv2
%{_libdir}/lib*.so
%{?with_compat_openvc_pc:
%{_libdir}/pkgconfig/opencv.pc
}
%{_libdir}/pkgconfig/opencv4.pc
%{_libdir}/cmake/OpenCV/*.cmake

%files doc
%{_datadir}/opencv4/samples

%files -n python3-opencv
%{python3_sitearch}/cv2
%{python3_sitearch}/opencv-*.egg-info

%if %{with java}
%files java
%{_jnidir}/libopencv_java%{javaver}.so
%{_jnidir}/opencv-%{javaver}.jar
%{_jnidir}/libopencv_java.so
%{_jnidir}/opencv.jar
%endif


%changelog
* Tue Feb 03 2026 Nicolas Chauvet <kwizart@gmail.com> - 4.11.0-12
- Backport patch for CVE-2025-53644

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.11.0-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Sun Aug 24 2025 Orion Poplawski <orion@nwra.com> - 4.11.0-10
- Rebuild for VTK 9.5

* Wed Aug 20 2025 Jerry James <loganjerry@gmail.com> - 4.11.0-9
- Rebuild for tbb 2022.2.0

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.11.0-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Adam Williamson <awilliam@redhat.com> - 4.11.0-7
- Rebuild for new gdal

* Tue Jul 29 2025 Nicolas Chauvet <kwizart@gmail.com> - 4.11.0-6
- Add missing BR libavif

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Adam Williamson <awilliam@redhat.com> - 4.11.0-4
- Rebuilt for Python 3.14
- Add patch from Atri Bhattacharya to fix build with Qt 6.9

* Tue Mar 11 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 4.11.0-3
- Use Qt6 in highgui and cvv

* Tue Feb 18 2025 Adam Williamson <awilliam@redhat.com> - 4.11.0-2
- Backport all post-4.11.0 PNG fixes, including big-endian fix
- Resolves: rhbz#2345306

* Mon Feb 03 2025 Sérgio Basto <sergio@serjux.com> 4.11.0-1
- Update to version 4.11.0
- Resolves: rhbz#2336422
- Add upstream patch to fix build on PPC64LE

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild
- Add upstream patch to fix build on PPC64LE with GCC 15

* Mon Dec 23 2024 Orion Poplawski <orion@nwra.com> - 4.10.0-8
- Rebuild with numpy 2.x (rhbz#2333781)

* Tue Nov 12 2024 Sandro Mani <manisandro@gmail.com> - 4.10.0-7
- Rebuild (tesseract)

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 4.10.0-6
- Rebuild (gdal)

* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 4.10.0-5
- Rebuild for hdf5 1.14.5

* Wed Sep 25 2024 Michel Lind <salimma@fedoraproject.org> - 4.10.0-4
- Rebuild for tesseract-5.4.1-3 (soversion change from 5.4.1 to just 5.4)

* Mon Sep 23 2024 Fabio Valentini <decathorpe@gmail.com> - 4.10.0-3
- Rebuild for ffmpeg 7

* Thu Jul 25 2024 Sérgio Basto <sergio@serjux.com> - 4.10.0-2
- Rebuild for opencv 4.10.0

* Thu Jul 25 2024 Packit <hello@packit.dev> - 4.10.0-1
- Update to version 4.10.0
- Resolves: rhbz#2290312

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 13 2024 Sandro Mani <manisandro@gmail.com> - 4.9.0-7
- Rebuild for tesseract-5.4.1

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 4.9.0-6
- Rebuilt for Python 3.13

* Tue May 14 2024 Sandro Mani <manisandro@gmail.com> - 4.9.0-5
- Rebuild (gdal)

* Tue Apr 23 2024 Josef Ridky <jridky@redhat.com> - 4.9.0-4
- Rebuild for openexr

* Fri Feb 23 2024 Jerry James <loganjerry@gmail.com> - 4.9.0-3
- Rebuild (coin-or-Clp)
- Use uppercase connectives in SPDX expression

* Mon Feb 05 2024 Sérgio Basto <sergio@serjux.com> - 4.9.0-2
- Revert "drop compat symlink to opencv.pc"

* Sun Jan 28 2024 Sérgio Basto <sergio@serjux.com> - 4.9.0-1
- Update opencv to 4.9.0 (#2256160)
- Enable ffmpeg and xine (now they are available on Fedora)
- Really drop compat symlink for includes - rhbz#1830266
  Note: conditional builds with underscrore don't have _without option
  https://github.com/rpm-software-management/rpm/issues/1929

* Sun Jan 28 2024 Sandro Mani <manisandro@gmail.com> - 4.8.1-8
- Rebuild (tesseract)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 4.8.1-5
- Rebuilt for TBB 2021.11

* Thu Jan 11 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 4.8.1-4
- Backport support for protobuf v22 and later from opencv 4.9.0

* Thu Nov 16 2023 Sandro Mani <manisandro@gmail.com> - 4.8.1-3
- Rebuild (gdal)

* Sat Oct 07 2023 Sandro Mani <manisandro@gmail.com> - 4.8.1-2
- Rebuild (tesseract)

* Fri Sep 29 2023 Sérgio Basto <sergio@serjux.com> - 4.8.1-1
- Update opencv to 4.8.1

* Thu Sep 14 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 4.8.0-2
- Separate per-module subpackages (#1878320)

* Mon Aug 07 2023 Sérgio Basto <sergio@serjux.com> - 4.8.0-1
- Update opencv to 4.8.0
- Use bundle flatbuffers, tried build with flatbuffers from system but doesn't build
- Use oneVPL instead libmfx
- Add WeChat QRCode
- https://src.fedoraproject.org/rpms/opencv/pull-request/23 , upgrade C++ standard to C++17 for protobuf v4 (23.x etc.)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 19 2023 Josef Ridky <jridky@redhat.com> - 4.7.0-14
- Migrate to SPDX license format

* Fri Jul 14 2023 Sandro Mani <manisandro@gmail.com> - 4.7.0-13
- Rebuild (tesseract)

* Fri Jul 07 2023 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.7.0-12
- Drop openni support on i686 as it is no longer available

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 4.7.0-11
- Rebuilt for Python 3.12

* Mon Jun 12 2023 Nicolas Chauvet <kwizart@gmail.com> - 4.7.0-10
- Rebuilt for libdc1394

* Mon Jun 12 2023 Nicolas Chauvet <kwizart@gmail.com> - 4.7.0-9
- Upstream commit to fix rhbz#2190013

* Sat May 13 2023 Sérgio Basto <sergio@serjux.com> - 4.7.0-8
- The %%ldconfig_scriptlets macro can be removed on all Fedoras. Possibly also on
  EPEL 8. But it is required on EPEL 7.
- Install egg-info in python3_sitearch to stay in same location as the rest of python

* Sat May 13 2023 Sérgio Basto <sergio@serjux.com> - 4.7.0-7
- Install python egg-info
- Fix patch warning
- Obsolete python2 < %{version} (if someone want use an external python2 version}

* Thu May 11 2023 Sandro Mani <manisandro@gmail.com> - 4.7.0-6
- Rebuild (gdal)
- Disable tests, even only tests, fail to build and generate build.log with millions of logs lines saying:
    *** stack smashing detected ***: terminated
    cat build.log | grep smashing | wc -l
    118308609
- Disable extra tests on builds

* Thu Apr 13 2023 Sérgio Basto <sergio@serjux.com> - 4.7.0-5
- if without tests also disable 500MB of extra tests

* Mon Apr 03 2023 Sandro Mani <manisandro@gmail.com> - 4.7.0-4
- Rebuild (tesseract)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Jan 15 2023 Orion Poplawski <orion@nwra.com> - 4.7.0-2
- Rebuild for vtk 9.2.5

* Fri Jan 13 2023 Sérgio Basto <sergio@serjux.com> - 4.7.0-1
- Update opencv to 4.7.0 (#2157121)

* Fri Dec 23 2022 Sandro Mani <manisandro@gmail.com> - 4.6.0-10
- Rebuild (tesseract)

* Fri Dec 23 2022 Nicolas Chauvet <kwizart@gmail.com> - 4.6.0-9
- Rebuilt for tesseract

* Sat Nov 12 2022 Sandro Mani <manisandro@gmail.com> - 4.6.0-8
- Rebuild (gdal)

* Wed Sep 28 2022 Tom Rix <trix@redhat.com> - 4.6.0-7
- Remove Unicap

* Fri Jul 29 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.6.0-6
- BR vte-java only on %%java_arches

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Sandro Mani <manisandro@gmail.com> - 4.6.0-4
- Rebuild (tesseract)

* Wed Jul 06 2022 Sérgio Basto <sergio@serjux.com> - 4.6.0-3
- (#2104082) only build Java sub package on arches that java is supported

* Mon Jun 20 2022 Sérgio Basto <sergio@serjux.com> - 4.6.0-2
- Rebuilt for Python 3.11 (is just arrived to rawhide)

* Fri Jun 17 2022 Sérgio Basto <sergio@serjux.com> - 4.6.0-1
- Update opencv to 4.6.0 (#2094603)
- Remove hack to keep old so version
- Adapt spec to new so version ${OPENCV_VERSION_MAJOR}${OPENCV_VERSION_MINOR_2DIGITS}
  and drop OPENCV_VERSION_PATCH

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 4.5.5-9
- Rebuilt for Python 3.11

* Sat May 21 2022 Sandro Mani <manisandro@gmail.com> - 4.5.5-8
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Sun Mar 20 2022 Sérgio Basto <sergio@serjux.com> - 4.5.5-7
- Switch to new Python loader, doesn't fix rhbz #2054951 but can be a step

* Thu Mar 10 2022 Sandro Mani <manisandro@gmail.com> - 4.5.5-6
- Rebuild for tesseract 5.1.0

* Tue Feb 15 2022 Sérgio Basto <sergio@serjux.com> - 4.5.5-5
- The upstream fix https://github.com/opencv/opencv/pull/21614
  and remove the previous workaround

* Sun Feb 13 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 4.5.5-4
- Disable some altivec vectorization optimization on ppc64le (bug 2051193)

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 4.5.5-3
- Rebuilt for java-17-openjdk as system jdk

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 27 2021 Sérgio Basto <sergio@serjux.com> - 4.5.5-1
- Update opencv to 4.5.5 (#2035628)

* Sun Dec 19 2021 Sandro Mani <manisandro@gmail.com> - 4.5.4-8
- Rebuild (tesseract)

* Tue Dec 14 2021 Sandro Mani <manisandro@gmail.com> - 4.5.4-7
- Rebuild (tesseract)

* Mon Nov 22 2021 Orion Poplawski <orion@nwra.com> - 4.5.4-6
- Rebuild for hdf5 1.12.1

* Thu Nov 11 2021 Sandro Mani <manisandro@gmail.com> - 4.5.4-5
- Rebuild (gdal)

* Sat Nov 06 2021 Adrian Reber <adrian@lisas.de> - 4.5.4-4
- Rebuilt for protobuf 3.19.0

* Fri Nov 05 2021 Adrian Reber <adrian@lisas.de> - 4.5.4-3
- Rebuilt for protobuf 3.19.0

* Mon Oct 25 2021 Adrian Reber <adrian@lisas.de> - 4.5.4-2
- Rebuilt for protobuf 3.18.1

* Sun Oct 10 2021 Sérgio Basto <sergio@serjux.com> - 4.5.4-1
- Update to 4.5.4

* Fri Aug 20 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.3-6
- Rebuild for OpenEXR/Imath 3.1.

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 4.5.3-5
- Rebuild for hdf5 1.10.7

* Sat Jul 31 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.3-4
- Rebuild for OpenEXR/Imath 3.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.3-2
- Rebuild for openexr 3.

* Thu Jul 15 2021 Sérgio Basto <sergio@serjux.com> - 4.5.3-1
- Update to 4.5.3

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.5.2-6
- Rebuilt for Python 3.10

* Fri May 21 2021 Sandro Mani <manisandro@gmail.com> - 4.5.2-5
- Rebuild (gdal)

* Thu May 20 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.2-4
- Rebuild for gdal 3.3.0.

* Fri May 07 2021 Sandro Mani <manisandro@gmail.com> - 4.5.2-3
- Rebuild (gdal)

* Thu Apr 29 2021 Sérgio Basto <sergio@serjux.com> - 4.5.2-2
- Upstream fixed GCC11 issues, so we can re-enable the tests

* Sat Apr 03 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.5.2-1
- Update to 4.5.2

* Wed Mar 31 2021 Nicolas Chauvet <kwizart@gmail.com> - 4.5.1-8
- Disable tests for now

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 4.5.1-7
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Feb 10 2021 Jiri Kucera <jkucera@redhat.com> - 4.5.1-6
- Fix file lists
  Based on comparison of `opencv-4.5.1/modules/` and
  `opencv-4.5.1/opencv_contrib-4.5.1/modules/`, move some *.so's between core
  and contrib rpms

* Sun Jan 31 2021 Orion Poplawski <orion@nwra.com> - 4.5.1-5
- Rebuild for VTK 9

* Wed Jan 27 2021 Tomas Popela <tpopela@redhat.com> - 4.5.1-4
- Drop unused BR on SFML and disable VTK support on RHEL 8+

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 12 14:20:57 CET 2021 Adrian Reber <adrian@lisas.de> - 4.5.1-2
- Rebuilt for protobuf 3.14

* Sat Jan 02 2021 Sérgio Basto <sergio@serjux.com> - 4.5.1-1
- Update to 4.5.1

* Fri Jan 01 2021 Richard Shaw <hobbes1069@gmail.com> - 4.5.0-4
- Rebuild for OpenEXR 2.5.3.

* Sat Dec  5 2020 Jeff Law <law@redhat.com> - 4.5.0-3
- Fix missing #include for gcc-11

* Fri Nov  6 22:47:45 CET 2020 Sandro Mani <manisandro@gmail.com> - 4.5.0-2
- Rebuild (proj, gdal)

* Thu Oct 15 2020 Sérgio Basto <sergio@serjux.com> - 4.5.0-1
- Update 4.5.0

* Wed Oct 07 2020 Sérgio Basto <sergio@serjux.com> - 4.4.0-1
- Update 4.4.0
- opencv_vulkan.patch already applied in upstream

* Thu Sep 24 2020 Adrian Reber <adrian@lisas.de> - 4.3.0-9
- Rebuilt for protobuf 3.13

* Fri Jul 24 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.3.0-8
- Rebuilt
- Fix cmake build
- Disable LTO on ppc64le
- Add undefine __cmake_in_source_build to allow build on Fedora < 33

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 4.3.0-7
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Fri Jun 26 2020 Orion Poplawski <orion@nwra.com> - 4.3.0-6
- Rebuild for hdf5 1.10.6

* Tue Jun 23 2020 Adrian Reber <adrian@lisas.de> - 4.3.0-5
- Rebuilt for protobuf 3.12

* Sun Jun 21 2020 Sérgio Basto <sergio@serjux.com> - 4.3.0-4
- Readd flake8 build requirement
- Fix build because pangox has been retired for F33 so we need remove the BR
  gtkglext
- Also remove all gtk stuff (we have to choose between gtk or qt when build opencv)
  https://answers.opencv.org/question/215066/gtk-or-qt-when-build-opencv/
- Doxygen requires gtk2, disabling for now

* Sun Jun 14 2020 Adrian Reber <adrian@lisas.de>
- Rebuilt for protobuf 3.12

* Tue Jun 02 2020 Orion Poplawski <orion@nwra.com> - 4.3.0-3
- Run tests

* Tue Jun 02 2020 Orion Poplawski <orion@nwra.com> - 4.3.0-2
- Add upstream patches for VTK 9.0 support (bz#1840977)

* Thu May 28 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.3.0-1
- Update to 4.3.0

* Thu May 28 2020 Charalampos Stratakis <cstratak@redhat.com> - 4.2.0-9
- Remove flake8 build requirement

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-8
- Rebuilt for Python 3.9

* Thu May 21 2020 Sandro Mani <manisandro@gmail.com> - 4.2.0-7
- Rebuild (gdal)

* Fri May 08 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-6
- Drop compat symlink for includes - rhbz#1830266

* Thu Mar 26 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-5
- Add without_compat_opencv_pc with conditional - rhbz#1816439

* Tue Mar 03 2020 Sandro Mani <manisandro@gmail.com> - 4.2.0-4
- Rebuild (gdal)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 29 2020 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-2
- Backport patch for ppc64le

* Tue Dec 31 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.2.0-1
- Update to 4.2.0

* Sat Dec 28 2019 Sandro Mani <manisandro@gmail.com> - 4.1.2-3
- Rebuild (tesseract)

* Thu Dec 19 2019 Orion Poplawski <orion@nwra.com> - 4.1.2-2
- Rebuild for protobuf 3.11

* Thu Oct 17 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1.1
- Fix include path
- Drop CPU baseline to SSE2 for x86
- Add missing directory ownership
- Add symlinks for compatibility with older versions
- Restore deprecated headers for compat

* Sat Oct 12 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.1.2-1
- Update to 4.1.2

* Fri Sep 13 2019 Nicolas Chauvet <kwizart@gmail.com> - 4.1.1-1
- Update to 4.1.1

* Fri Sep 13 2019 Sérgio Basto <sergio@serjux.com> - 4.1.0-1
- Update opencv to 4.1.0

* Fri Sep 13 2019 Christopher N. Hesse <raymanfx@gmail.com> - 4.1.0-0
- Enable vulkan compute backend

* Fri Sep 13 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-9
- Reenable pylint and vtk, they are working now.
* Wed Sep 11 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 3.4.6-8
- F-32: remove vtk gcdm dependency for now because they have broken dependency
  (bug 1751406)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4.6-7
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Jerry James <loganjerry@gmail.com> - 3.4.6-5
- Rebuild for coin-or package updates

* Tue Jun 25 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-4
- cmake: use relative PATH on OPENCV_CONFIG_INSTALL_PATH, fixes rhbz #1721876
- cmake: don't set ENABLE_PKG_CONFIG

* Wed Jun 12 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-3
- Remove Obsoletes/Provides libopencv_java.so and use OPENCV_JAR_INSTALL_PATH

* Sun Jun 09 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-2
- Fix cmakes location
- add BR: python3-beautifulsoup4

* Thu May 23 2019 Sérgio Basto <sergio@serjux.com> - 3.4.6-1
- Update to 3.4.6

* Mon May 20 2019 Sérgio Basto <sergio@serjux.com> - 3.4.4-10
- Try improve Java Bindings

* Sun May 12 2019 Sérgio Basto <sergio@serjux.com> - 3.4.4-9
- Enable Java Bindings (contribution of Ian Wallace)
- Obsoletes python2-opencv to fix upgrade path

* Wed Apr 10 2019 Richard Shaw <hobbes1069@gmail.com> - 3.4.4-8
- Rebuild for OpenEXR 2.3.0.

* Mon Mar 18 2019 Orion Poplawski <orion@nwra.com>
- Rebuild for vtk 8.2

* Sun Mar 03 2019 Sérgio Basto <sergio@serjux.com> - 3.4.4-6
- Reenable build with gdcm
- Opencl is fixed for ppc64le on F30

* Thu Feb 21 2019 Josef Ridky <jridky@redhat.com> - 3.4.4-5
- build without gdcm to fix FTBFS in F30+ (#1676289)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.4.4-3
- Subpackage python2-opencv has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Dec 03 2018 Sérgio Basto <sergio@serjux.com> - 3.4.4-2
- Add the correct and upstreamed fix for support_YV12_too, pull request 13351
  which is merged

* Sat Dec 01 2018 Sérgio Basto <sergio@serjux.com> - 3.4.4-1
- Update to 3.4.4

* Wed Nov 21 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.4.3-7
- Rebuild for protobuf 3.6

* Tue Nov 13 2018 Sandro Mani <manisandro@gmail.com> - 3.4.3-6
- Rebuild (tesseract)

* Tue Oct 30 2018 Sérgio Basto <sergio@serjux.com> - 3.4.3-5
- Enable vtk should work with vtk-8.1.1
- Add BR python Flake8

* Tue Oct 23 2018 Felix Kaechele <heffer@fedoraproject.org> - 3.4.3-4
- enable building of dnn

* Sat Oct 13 2018 Jerry James <loganjerry@gmail.com> - 3.4.3-3
- Rebuild for tbb 2019_U1

* Sun Sep 30 2018 Sérgio Basto <sergio@serjux.com> - 3.4.3-2
- Use GLVND libraries for OpenGL and GLX, setting OpenGL_GL_PREFERENCE=GLVND

* Wed Sep 26 2018 Sérgio Basto <sergio@serjux.com> - 3.4.3-1
- Update to 3.4.3
- Fix build on arm and s390x

* Wed Sep 26 2018 Sérgio Basto <sergio@serjux.com> - 3.4.2-1
- Update to 3.4.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Sérgio Basto <sergio@serjux.com> - 3.4.1-5
- Small fix to build with Pyhton-3.7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.4.1-4
- Rebuilt for Python 3.7

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.4.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Mar 08 2018 Sérgio Basto <sergio@serjux.com> - 3.4.1-2
- Enable VA
- Do not use -f on rm because it silences errors
- Opencv sub-package don't need ldconfig because don't have any so

* Thu Mar 01 2018 Josef Ridky <jridky@redhat.com> - 3.4.1-1
- Spec clean up (remove Group tag, add ldconfig scriptlets, escape macros in comments)
- Remove unused patch
- Add gcc and gcc-c++ requirements
- Rebase to version 3.4.1

* Sun Feb 18 2018 Sérgio Basto <sergio@serjux.com> - 3.3.1-7
- Rebuild for gdcm-2.8

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.3.1-6
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Sérgio Basto <sergio@serjux.com> - 3.3.1-4
- Enable Pylint
- Enable Clp (COIN-OR Linear Program Solver)
- Enable VA (Video Acceleration API for Linux)
- Enable OpenMP
- Provides and obsoletes for opencv-devel-docs
- BuildRequires perl-local do generate documentation without errors

* Thu Jan 25 2018 Sérgio Basto <sergio@serjux.com> - 3.3.1-3
- Rename sub-package opencv-python3 to python3-opencv and other minor fixes in
  python packaging
- Generate documentation
- Rename sub-package devel-docs to doc
- Cleanup some comments from opencv 2.4 packaging

* Wed Jan 24 2018 Troy Dawson <tdawson@redhat.com> - 3.3.1-2
- Update conditionals

* Tue Nov 14 2017 Sérgio Basto <sergio@serjux.com> - 3.3.1-1
- Update to 3.3.1
- Fix WARNING: Option ENABLE_SSE='OFF' is deprecated and should not be used anymore
-          Behaviour of this option is not backward compatible
-          Refer to 'CPU_BASELINE'/'CPU_DISPATCH' CMake options documentation
- Fix WARNING: Option ENABLE_SSE2='OFF' is deprecated and should not be used anymore
-          Behaviour of this option is not backward compatible
-          Refer to 'CPU_BASELINE'/'CPU_DISPATCH' CMake options documentation
- Update opencv to 3.3.0
- Patch3 is already in source code
- Fix WARNING: Option ENABLE_SSE3='OFF' is deprecated and should not be used anymore
- Enable openblas
- Add conditonal to build with_gdcm
- Disable "Intel ITT support" because source is in 3rdparty/ directory

* Sat Oct 28 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-13
- Require python3-numpy instead numpy for opencv-python3 (#1504555)

* Sat Sep 02 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-12
- Fix 2 rpmlint errors

* Sat Sep 02 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-11
- Enable libv4l1 to fix open a video (#1487816)

* Mon Aug 28 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-10
- Better conditionals to enable openni only available in ix86, x86_64 and arm

* Sun Aug 20 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-9
- Enable openni.
- Enable eigen3 except in ppc64le because fails to build in OpenCL headers.
- Documented why is not enabled atlas, openblas and vtk.

* Sun Aug 20 2017 Sérgio Basto <sergio@serjux.com> - 3.2.0-8
- Reenable gstreamer
- Remove architecture checks for tbb and enable it, inspired on (#1262788)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.0-7
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.2.0-6
- Python 2 binary package renamed to python2-opencv
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Orion Poplawski <orion@cora.nwra.com> - 3.2.0-3
- Rebuild for protobuf 3.3.1

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Mon Feb 27 2017 Josef Ridky <jridky@redhat.com> - 3.2.0-1
- Rebase to the latest version (3.2.0) - #1408880
- Remove unused BuildRequires and patches
- Remove copyrighted lena.jpg images and SIFT/SURF from tarball, due to legal concerns.
- Disable dnn module from opencv_contrib, due missing BuildRequired package in Fedora (protobuf-cpp)
- Disable tracking module from opencv_contrib, due disabling dnn module (is required by this module)
- Disable CAROTENE in compilation (caused error on arm and ppc64le)
- Fix syntax error in opencv_contrib test file (opencv-3.2.0-test-file-fix.patch)

* Tue Feb 21 2017 Sandro Mani <manisandro@gmail.com> - 3.1.0-15
- Rebuild (tesseract)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 01 2017 Sandro Mani <manisandro@gmail.com> - 3.1.0-13
- Rebuild (libwebp)

* Thu Jan 26 2017 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-12
- Rebuild for protobuf 3.2.0

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-11
- Rebuild for Python 3.6

* Sat Dec 03 2016 Rex Dieter <rdieter@fedoraproject.org> - 3.1.0-10
- rebuild (jasper)

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 3.1.0-9
- Rebuild for protobuf 3.1.0

* Tue Jul 26 2016 Nicolas Chauvet <kwizart@gmail.com> - 3.1.0-8
- Clean uneeded symbols until fixed upstream

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.0-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri May 27 2016 Till Maas <opensource@till.name> - 3.1.0-6
- Define %%srcname for python subpackages
- Fix whitespace

* Mon May 09 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-5
- Don't clean unneeded symbols (as recommended by fedora-review), fix undefined
  symbol: cvLoadImage in Unknown on line 0 on php-facedetect package.

* Sat May 07 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-4
- Put all idefs and ifarchs outside the scope of rpm conditional builds, rather
  than vice versa, as had organized some time ago, it seems to me more correct.
- Remove SIFT/SURF from source tarball in opencv_contrib, due to legal concerns
- Redo and readd OpenCV-2.4.4-pillow.patch .
- Add OpenCV-3.1-pillow.patch to apply only opencv_contrib .
- Add the %%python_provide macro (Packaging:Python guidelines). 

* Fri Apr 22 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-3
- Use always ON and OFF instead 0 and 1 in cmake command.
- Remove BUILD_TEST and TBB_LIB_DIR variables not used by cmake.
- Add BRs: tesseract-devel, protobuf-devel, glog-devel, doxygen,
  gflags-devel, SFML-devel, libucil-devel, qt5-qtbase-devel, mesa-libGL-devel,
  mesa-libGLU-devel and hdf5-devel.
- Remove BR: vtk-devel because VTK support is disabled. Incompatible 
  combination: OpenCV + Qt5 and VTK ver.6.2.0 + Qt4
- Enable build with Qt5.
- Enable build with OpenGL.
- Enable build with UniCap.
- Also requires opencv-contrib when install opencv-devel (#1329790).

* Wed Apr 20 2016 Sérgio Basto <sergio@serjux.com> - 3.1.0-2
- Add BR:libwebp-devel .
- Merge from 2.4.12.3 package: 
  Add aarch64 and ppc64le to list of architectures where TBB is supported (#1262788).
  Use bcond tags to easily enable or disable modules.
  Fix unused-direct-shlib-dependency in cmake with global optflags.
  Added README.md with references to online documentation.
  Investigation on the documentation, added a few notes.
- Update to 3.1.0 (Fri Mar 25 2016 Pavel Kajaba <pkajaba@redhat.com> - 3.1.0-1)
- Added opencv_contrib (Thu Jul 09 2015 Sérgio Basto <sergio@serjux.com> -
  3.0.0-2)
- Update to 3.0.0 (Fri Jun 05 2015 Jozef Mlich <jmlich@redhat.com> - 3.0.0-1)

* Tue Mar 01 2016 Yaakov Selkowitz <yselkowi@redhat.com> - 2.4.12.3-3
- Fix FTBFS with GCC 6 (#1307821)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Dec 02 2015 Sérgio Basto <sergio@serjux.com> - 2.4.12.3-1
- Update opencv to 2.4.12.3 (#1271460).
- Add aarch64 and ppc64le to list of architectures where TBB is supported (#1262788).

* Tue Jul 14 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-5
- Use bcond tags to easily enable or disable modules.
- Package review, more cleaning in the spec file.
- Fixed unused-direct-shlib-dependency in cmake with global optflags.
- Added README.md index.rst with references to online documentation.
- Investigation on the documentation, added a few notes.

* Mon Jul 06 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-4
- Enable-gpu-module, rhbz #1236417, thanks to Rich Mattes.
- Deleted the global gst1 because it is no longer needed.

* Thu Jun 25 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-3
- Fix license tag

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 11 2015 Sérgio Basto <sergio@serjux.com> - 2.4.11-1
- Update to 2.4.11 .
- Dropped patches 0, 10, 11, 12, 13 and 14 .

* Sat Apr 11 2015 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-6
- rebuild (gcc5)

* Mon Feb 23 2015 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-5
- rebuild (gcc5)

* Tue Nov 25 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-4
- rebuild (openexr)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 25 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.9-2
- backport support for GStreamer 1 (#1123078)

* Thu Jul 03 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4.9-1
- Update to 2.4.9

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Apr 26 2014 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-6
- revert pkgcmake2 patch (#1070428)

* Fri Jan 17 2014 Nicolas Chauvet <kwizart@gmail.com> - 2.4.7-5
- Fix opencv_ocl isn't part of -core

* Thu Jan 16 2014 Christopher Meng <rpm@cicku.me> - 2.4.7-4
- Enable OpenCL support.
- SPEC small cleanup.

* Wed Nov 27 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-3
- rebuild (openexr)

* Mon Nov 18 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.7-2
- OpenCV cmake configuration broken (#1031312)

* Wed Nov 13 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.7-1
- Update to 2.4.7

* Sun Sep 08 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.6.1-2
- rebuild (openexr)

* Wed Jul 24 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.6.1-1
- Update to 2.4.6.1

* Thu May 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.5-1
- Update to 2.4.5-clean
- Spec file clean-up
- Split core libraries into a sub-package

* Sat May 11 2013 François Cami <fcami@fedoraproject.org> - 2.4.4-3
- change project URL.

* Tue Apr 02 2013 Tom Callaway <spot@fedoraproject.org> - 2.4.4-2
- make clean source without SIFT/SURF

* Sat Mar 23 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-1
- Update to 2.4.4a
- Fix tbb-devel architecture conditionals

* Sun Mar 10 2013 Rex Dieter <rdieter@fedoraproject.org> 2.4.4-0.2.beta
- rebuild (OpenEXR)

* Mon Feb 18 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.4-0.1.beta
- Update to 2.4.4 beta
- Drop python-imaging also from requires
- Drop merged patch for additionals codecs
- Disable the java binding for now (untested)

* Fri Jan 25 2013 Honza Horak <hhorak@redhat.com> - 2.4.3-7
- Do not build with 1394 libs in rhel

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 2.4.3-6
- rebuild due to "jpeg8-ABI" feature drop

* Sun Jan 20 2013 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-5
- Add more FourCC for gstreamer - rhbz#812628
- Allow to use python-pillow - rhbz#895767

* Mon Nov 12 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-3
- Switch Build Type to ReleaseWithDebInfo to avoid -03

* Sun Nov 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.3-2
- Disable SSE3 and allow --with sse3 build conditional.
- Disable gpu module as we don't build cuda
- Update to 2.4.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jul 09 2012 Honza Horak <hhorak@redhat.com> - 2.4.2-1
- Update to 2.4.2

* Fri Jun 29 2012 Honza Horak <hhorak@redhat.com> - 2.4.1-2
- Fixed cmake script for generating opencv.pc file
- Fixed OpenCVConfig script file

* Mon Jun 04 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.4.1-1
- Update to 2.4.1
- Rework dependencies - rhbz#828087
  Re-enable using --with tbb,openni,eigen2,eigen3

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-8
- Rebuilt for c++ ABI breakage

* Mon Jan 16 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-7
- Update gcc46 patch for ARM FTBFS

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Adam Jackson <ajax@redhat.com> 2.3.1-5
- Rebuild for new libpng

* Thu Oct 20 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-4
- Rebuilt for tbb silent ABI change

* Mon Oct 10 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-3
- Update to 2.3.1a

* Mon Sep 26 2011 Dan Horák <dan[at]danny.cz> - 2.3.1-2
- openni is exclusive for x86/x86_64

* Fri Aug 19 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.3.1-1
- Update to 2.3.1
- Add BR openni-devel python-sphinx
- Remove deprecated cmake options
- Add --with cuda conditional (wip)
- Disable make test (unavailable)

* Thu May 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-6
- Backport fixes from branch 2.2 to date

* Tue May 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-5
- Re-enable v4l on f15
- Remove unused cmake options

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-2
- Fix with gcc46
- Disable V4L as V4L1 is disabled for Fedora 15

* Thu Jan 06 2011 Nicolas Chauvet <kwizart@gmail.com> - 2.2.0-1
- Update to 2.2.0
- Disable -msse and -msse2 on x86_32

* Wed Aug 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 2.1.0-5
- -devel: include OpenCVConfig.cmake (#627359)

* Thu Jul 22 2010 Dan Horák <dan[at]danny.cz> - 2.1.0-4
- TBB is available only on x86/x86_64 and ia64

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 25 2010 Nicolas Chauvet <kwizart@gmail.com> - 2.1.0-2
- Move samples from main to -devel
- Fix spurious permission
- Add BR tbb-devel
- Fix CFLAGS

* Fri Apr 23 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Update libdir patch

* Tue Apr 13 2010 Karel Klic <kklic@redhat.com> - 2.0.0-10
- Fix nonstandard executable permissions

* Tue Mar 09 2010 Karel Klic <kklic@redhat.com> - 2.0.0-9
- apply the previously added patch

* Mon Mar 08 2010 Karel Klic <kklic@redhat.com> - 2.0.0-8
- re-enable testing on CMake build system
- fix memory corruption in the gaussian random number generator

* Sat Feb 27 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-7
- replaced BR unicap-devel by libucil-devel (unicap split)

* Thu Feb 25 2010 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-6
- use cmake build system
- applications renamed to opencv_xxx instead of opencv-xxx
- add devel-docs subpackage #546605
- add OpenCVConfig.cmake
- enable openmp build
- enable old SWIG based python wrappers
- opencv package is a good boy and use global instead of define

* Tue Feb 16 2010 Karel Klic <kklic@redhat.com> - 2.0.0-5
- Set CXXFLAXS without -match=i386 for i386 architecture #565074

* Sat Jan 09 2010 Rakesh Pandit <rakesh@fedoraproject.org> - 2.0.0-4
- Updated opencv-samples-Makefile (Thanks Scott Tsai) #553697

* Wed Jan 06 2010 Karel Klic <kklic@redhat.com> - 2.0.0-3
- Fixed spec file issues detected by rpmlint

* Sun Dec 06 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-2
- Fix autotools scripts (missing LBP features) - #544167

* Fri Nov 27 2009 Haïkel Guémar <karlthered@gmail.com> - 2.0.0-1
- Updated to 2.0.0
- Removed upstream-ed patches
- Ugly hack (added cvconfig.h)
- Disable %%check on ppc64

* Thu Sep 10 2009 Karsten Hopp <karsten@redhat.com> - 1.1.0-0.7.pre1
- fix build on s390x where we don't have libraw1394 and devel

* Thu Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.6.pre1
- Fix typo I introduced that prevented build on i386/i586

* Thu Jul 30 2009 Haïkel Guémar <karlthered@gmail.com> - 1.1.0.0.5.pre1
- Added 1394 libs and unicap support

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.4.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.3.pre1
- Build with gstreamer support - #491223
- Backport gcc43 fix from trunk

* Thu Jul 16 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.2.pre1
- Fix FTBFS #511705

* Fri Apr 24 2009 kwizart < kwizart at gmail.com > - 1.1.0-0.1.pre1
- Update to 1.1pre1
- Disable CXXFLAGS hardcoded optimization
- Add BR: python-imaging, numpy
- Disable make check failure for now

* Wed Apr 22 2009 kwizart < kwizart at gmail.com > - 1.0.0-14
- Fix for gcc44
- Enable BR jasper-devel
- Disable ldconfig run on python modules (uneeded)
- Prevent timestamp change on install

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Rakesh Pandit <rakesh@fedoraproject.org> - 1.0.0-12
- fix URL field

* Fri Dec 19 2008 Ralf Corsépius <corsepiu@fedoraproject.org> - 1.0.0-11
- Adopt latest python spec rules.
- Rebuild for Python 2.6 once again.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0.0-10
- Rebuild for Python 2.6

* Thu May 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.0-9
- fix license tag

* Sun May 11 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-8
- Adjust library order in opencv.pc.in (BZ 445937).

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.0-7
- Autorebuild for GCC 4.3

* Sun Feb 10 2008 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-6
- Rebuild for gcc43.

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.0.0-5
- Rebuild for selinux ppc32 issue.

* Wed Aug 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-4
- Mass rebuild.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-3
- Fix %%{_datadir}/opencv/samples ownership.
- Adjust timestamp of cvconfig.h.in to avoid re-running autoheader.

* Thu Mar 22 2007 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-2
- Move all of the python module to pyexecdir (BZ 233128).
- Activate the testsuite.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 1.0.0-1
- Upstream update.

* Mon Dec 11 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-4
- Remove python-abi.

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 0.9.9-3
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-2
- Stop configure.in from hacking CXXFLAGS.
- Activate testsuite.
- Let *-devel require pkgconfig.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.9-1
- Upstream update.
- Don't BR: autotools.
- Install samples' Makefile as GNUmakefile.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-18
- Un'%%ghost *.pyo.
- Separate %%{pythondir} from %%{pyexecdir}.

* Thu Sep 21 2006 Ralf Corsépius <rc040203@freenet.de> - 0.9.7-17
- Rebuild for FC6.
- BR: libtool.

* Fri Mar 17 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-16
- Rebuild.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-15
- Force a re-run of Autotools by calling autoreconf.

* Wed Mar  8 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-14
- Added build dependency on Autotools.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-13
- Changed intrinsics patch so that it matches upstream.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-12
- More intrinsics patch fixing.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-11
- Don't do "make check" because it doesn't run any tests anyway.
- Back to main intrinsics patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-10
- Using simple intrinsincs patch.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-9
- Still more fixing of intrinsics patch for Python bindings on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-8
- Again fixed intrinsics patch so that Python modules build on x86_64.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-7
- Fixed intrinsics patch so that it works.

* Tue Mar  7 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-6
- Fixed Python bindings location on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-5
- SSE2 support on x86_64.

* Mon Mar  6 2006 Simon Perreault <nomis80@nomis80.org> - 0.9.7-4
- Rebuild

* Sun Oct 16 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-3
- Removed useless sample compilation makefiles/project files and replaced them
  with one that works on Fedora Core.
- Removed shellbang from Python modules.

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-2
- Made FFMPEG dependency optional (needs to be disabled for inclusion in FE).

* Mon Oct 10 2005 Simon Perreault <nomis80@nomis80.org> - 0.9.7-1
- Initial package.
