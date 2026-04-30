## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%undefine __cmake_in_source_build

# State Nov 11 2020, LTO causes
# TestXMLHyperTreeGridIO.cxx.o (symbol from plugin): undefined reference to symbol
# '_ZZNSt8__detail18__to_chars_10_implIjEEvPcjT_E8__digits@@LLVM_11'
%global _lto_cflags %{nil}

# OSMesa and X support are mutually exclusive.
# TODO - buid separate OSMesa version if desired
%bcond_with OSMesa
# No more Java on i686
%ifarch %{java_arches}
%bcond_without java
%else
%bcond_with java
%endif
%if 0%{?flatpak}
%bcond_with mpich
%bcond_with openmpi
%else
%bcond_without mpich
# No openmpi on i668 with openmpi 5 in Fedora 40+
%if 0%{?fedora} >= 40
%ifarch %{ix86}
%bcond_with openmpi
%else
%bcond_without openmpi
%endif
%else
%bcond_without openmpi
%endif
%endif
# s390x on EL8 does not have xorg-x11-drv-dummy
%if 0%{?rhel}
%ifarch s390x
%bcond_with    xdummy
%else
%bcond_without xdummy
%endif
%else
%bcond_without xdummy
%endif

%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%bcond_without flexiblas
%endif

# VTK currently is carrying local modifications to gl2ps
%bcond_with gl2ps

# VTK currently requires unreleased fmt 8.1.0
%bcond_with fmt

Summary: The Visualization Toolkit - A high level 3D visualization library
Name: vtk
Version: 9.2.6
Release: %autorelease -b 41
License: BSD-3-Clause
Source0: https://www.vtk.org/files/release/9.2/VTK-%{version}.tar.gz
Source1: https://www.vtk.org/files/release/9.2/VTKData-%{version}.tar.gz
Source2: xorg.conf
# Patch required libharu version (Fedora 33+ contains the needed VTK patches)
Patch0: vtk-libharu.patch
# Fix issue with Mayavi
Patch1: https://gitlab.kitware.com/vtk/vtk/-/merge_requests/9616.patch
# Add missing includes for gcc 13
# https://gitlab.kitware.com/vtk/vtk/-/issues/18782
Patch2: vtk-include.patch
# Fix segfault with Python 3.13
# https://bugzilla.redhat.com/show_bug.cgi?id=2310520
# Backport of https://gitlab.kitware.com/vtk/vtk/-/merge_requests/11486
Patch3: vtk-python3.13.patch
# Fix build
Patch4: vtk-build.patch

URL: https://vtk.org/

BuildRequires:  cmake
# Allow for testing with different cmake generators.
# make still seems to be faster than ninja, but has failed at times.
%global cmake_gen %{nil}
BuildRequires:  gcc-c++
%if %{with java}
BuildRequires: java-devel
%else
Obsoletes:     %{name}-java < %{version}-%{release}
Obsoletes:     %{name}-java-devel < %{version}-%{release}
%endif
%if %{with flexiblas}
BuildRequires:  flexiblas-devel
%else
BuildRequires:  blas-devel
BuildRequires:  lapack-devel
%endif
BuildRequires:  boost-devel
BuildRequires:  cgnslib-devel
BuildRequires:  cli11-devel
BuildRequires:  double-conversion-devel
BuildRequires:  eigen3-devel
BuildRequires:  expat-devel
%if %{with fmt}
BuildRequires:  fmt-devel >= 8.1.0
%endif
BuildRequires:  freetype-devel
BuildRequires:  gdal-devel
%if %{with gl2ps}
BuildRequires:  gl2ps-devel
%endif
BuildRequires:  glew-devel
BuildRequires:  hdf5-devel
BuildRequires:  json-devel
BuildRequires:  jsoncpp-devel
BuildRequires:  libarchive-devel
BuildRequires:  libGL-devel
BuildRequires:  libharu-devel >= 2.4.0
BuildRequires:  libICE-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libpq-devel
BuildRequires:  libtheora-devel
BuildRequires:  libtiff-devel
BuildRequires:  libxml2-devel
BuildRequires:  libX11-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXext-devel
BuildRequires:  libXt-devel
BuildRequires:  lz4-devel
BuildRequires:  mariadb-connector-c-devel
%{?with_OSMesa:BuildRequires: mesa-libOSMesa-devel}
BuildRequires:  motif-devel
BuildRequires:  netcdf-cxx-devel
BuildRequires:  openslide-devel
BuildRequires:  PEGTL-devel
BuildRequires:  proj-devel
BuildRequires:  pugixml-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-qt5
BuildRequires:  cmake(Qt5)
BuildRequires:  cmake(Qt5UiPlugin)
BuildRequires:  cmake(Qt5X11Extras)
BuildRequires:  qt5-qtwebkit-devel
BuildRequires:  R-devel
BuildRequires:  sqlite-devel
BuildRequires:  tcl-devel
BuildRequires:  tk-devel
BuildRequires:  utf8cpp-devel
BuildRequires:  zlib-devel
BuildRequires:  chrpath
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  gnuplot
BuildRequires:  wget
%if %{with mpich}
BuildRequires:  mpich-devel
%ifnarch %{ix86}
BuildRequires:  python%{?python3_pkgversion}-mpi4py-mpich
%endif
BuildRequires:  netcdf-mpich-devel
%endif
%if %{with openmpi}
BuildRequires:  openmpi-devel
BuildRequires:  python%{?python3_pkgversion}-mpi4py-openmpi
BuildRequires:  netcdf-openmpi-devel
%endif
# For %check
%if %{with xdummy}
BuildRequires:  xorg-x11-drv-dummy
BuildRequires:  mesa-dri-drivers
%endif
Requires: hdf5 = %{_hdf5_version}

# Almost every BR needs to be required by the -devel packages
%global vtk_devel_requires \
Requires: cmake \
%if %{with flexiblas} \
Requires: flexiblas-devel%{?_isa} \
%else \
Requires: blas-devel%{?_isa} \
Requires: lapack-devel%{?_isa} \
%endif \
Requires: blas-devel%{?_isa} \
Requires: boost-devel%{?_isa} \
Requires: cgnslib-devel%{?_isa} \
# cli11 is noarch and header-only \
Requires: cli11-static \
Requires: double-conversion-devel%{?_isa} \
# eigen3 is noarch and header-only \
Requires: eigen3-static \
Requires: expat-devel%{?_isa} \
%if %{with fmt} \
Requires: fmt-devel%{?_isa} \
%endif \
Requires: freetype-devel%{?_isa} \
Requires: gdal-devel%{?_isa} \
%if %{with gl2ps} \
Requires: gl2ps-devel%{?_isa} \
%endif \
Requires: glew-devel%{?_isa} \
Requires: json-devel%{?_isa} \
Requires: jsoncpp-devel%{?_isa} \
Requires: lapack-devel%{?_isa} \
Requires: libarchive-devel%{?_isa} \
Requires: libGL-devel%{?_isa} \
Requires: libharu-devel%{?_isa} >= 2.3.0-9 \
Requires: libjpeg-devel%{?_isa} \
Requires: libogg-devel%{?_isa} \
Requires: libpng-devel%{?_isa} \
Requires: libpq-devel%{?_isa} \
Requires: libtheora-devel%{?_isa} \
Requires: libtiff-devel%{?_isa} \
Requires: libxml2-devel%{?_isa} \
Requires: libX11-devel%{?_isa} \
Requires: libXcursor-devel%{?_isa} \
Requires: libXext-devel%{?_isa} \
Requires: libXt-devel%{?_isa} \
Requires: lz4-devel%{?_isa} \
Requires: mariadb-connector-c-devel%{?_isa} \
%if %{with OSMesa} \
Requires: mesa-libOSMesa-devel%{?_isa} \
%endif \
Requires: netcdf-cxx-devel%{?_isa} \
Requires: openslide-devel%{?_isa} \
Requires: PEGTL-devel%{?_isa} \
Requires: proj-devel%{?_isa} \
Requires: pugixml-devel%{?_isa} \
# bz #1183210 + #1183530 \
Requires: python%{python3_pkgversion}-devel \
Requires: sqlite-devel%{?_isa} \
Requires: cmake(Qt5) \
Requires: cmake(Qt5UiPlugin) \
Requires: cmake(Qt5X11Extras) \
Requires: qt5-qtwebkit-devel%{?_isa} \
Requires: utf8cpp-devel \
Requires: zlib-devel%{?_isa} \

# Bundled KWSys
# https://fedorahosted.org/fpc/ticket/555
# Components used are specified in Utilities/KWSys/CMakeLists.txt
Provides: bundled(kwsys-base64)
Provides: bundled(kwsys-commandlinearguments)
Provides: bundled(kwsys-directory)
Provides: bundled(kwsys-dynamicloader)
Provides: bundled(kwsys-encoding)
Provides: bundled(kwsys-fstream)
Provides: bundled(kwsys-fundamentaltype)
Provides: bundled(kwsys-glob)
Provides: bundled(kwsys-md5)
Provides: bundled(kwsys-process)
Provides: bundled(kwsys-regularexpression)
Provides: bundled(kwsys-status)
Provides: bundled(kwsys-system)
Provides: bundled(kwsys-systeminformation)
Provides: bundled(kwsys-systemtools)
# Other bundled libraries
Provides: bundled(diy2)
Provides: bundled(exodusII) = 2.0.0
Provides: bundled(exprtk) = 2.71
%if !%{with fmt}
Provides: bundled(fmt) = 8.1.0
%endif
Provides: bundled(ftgl) = 1.32
%if !%{with gl2ps}
Provides: bundled(gl2ps) = 1.4.0
%endif
Provides: bundled(ioss) = 20210512
Provides: bundled(kissfft)
Provides: bundled(metaio)
Provides: bundled(verdict) = 1.4.0
Provides: bundled(vpic)
Provides: bundled(xdmf2) = 2.1
Provides: bundled(xdmf3)

Obsoletes: %{name}-tcl < 8.2.0-1
Obsoletes: %{name}-qt-tcl < 8.2.0-1

%description
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

NOTE: The version in this package has NOT been compiled with MPI support.
%if %{with mpich}
Install the %{name}-mpich package to get a version compiled with mpich.
%endif
%if %{with openmpi}
Install the %{name}-openmpi package to get a version compiled with openmpi.
%endif

%package devel
Summary: VTK header files for building C++ code
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{with java}
Requires: %{name}-java%{?_isa} = %{version}-%{release}
%endif
Requires: python%{python3_pkgversion}-%{name}%{?_isa} = %{version}-%{release}
Requires: hdf5-devel%{?_isa}
Requires: netcdf-cxx-devel%{?_isa}
%{vtk_devel_requires}

%description devel
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

%package -n python%{python3_pkgversion}-%{name}
Summary: Python 3 bindings for VTK
Requires: vtk%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-vtk}
Provides: %{py3_dist vtk} = %{version}
Provides: python%{python3_version}dist(vtk) = %{version}
Obsoletes: python3-vtk-qt < 8.2.0-27
Provides:  python%{python3_pkgversion}-vtk-qt = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}
Python 3 bindings for VTK.

%if %{with java}
%package java
Summary: Java bindings for VTK
Requires: %{name}%{?_isa} = %{version}-%{release}

%description java
Java bindings for VTK.

%package java-devel
Summary: Java development for VTK
Requires: %{name}-java%{?_isa} = %{version}-%{release}
Requires: java-devel

%description java-devel
Java development for VTK.
%endif

%package qt
Summary: Qt bindings for VTK
Requires: %{name}%{?_isa} = %{version}-%{release}

%description qt
Qt bindings for VTK.

%global mpi_list %{nil}

%if %{with mpich}
%global mpi_list %mpi_list mpich
%package mpich
Summary: The Visualization Toolkit - mpich version

Obsoletes: %{name}-mpich-tcl < 8.2.0-1
Obsoletes: %{name}-mpich-qt-tcl < 8.2.0-1
%if %{without java}
Obsoletes:     %{name}-mpich-java < %{version}-%{release}
Obsoletes:     %{name}-mpich-java-devel < %{version}-%{release}
%endif

%description mpich
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

NOTE: The version in this package has been compiled with mpich support.

%package mpich-devel
Summary: VTK header files for building C++ code with mpich
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
%if %{with java}
Requires: %{name}-mpich-java%{?_isa} = %{version}-%{release}
%endif
Requires: python%{python3_pkgversion}-%{name}-mpich%{?_isa} = %{version}-%{release}
Requires: mpich-devel
Requires: hdf5-mpich-devel%{?_isa}
Requires: netcdf-mpich-devel%{?_isa}
%{vtk_devel_requires}

%description mpich-devel
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

NOTE: The version in this package has been compiled with mpich support.

%package -n python%{python3_pkgversion}-%{name}-mpich
Summary: Python 3 bindings for VTK with mpich
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}
Obsoletes: python3-vtk-mpich-qt < 8.2.0-15
Provides:  python%{python3_pkgversion}-vtk-mpich-qt = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}-mpich
python 3 bindings for VTK with mpich.

%if %{with java}
%package mpich-java
Summary: Java bindings for VTK with mpich
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}

%description mpich-java
Java bindings for VTK with mpich.

%package mpich-java-devel
Summary: Java development for VTK with mpich
Requires: %{name}-mpich-java%{?_isa} = %{version}-%{release}
Requires: java-devel

%description mpich-java-devel
Java development for VTK with mpich.
%endif

%package mpich-qt
Summary: Qt bindings for VTK with mpich
Requires: %{name}-mpich%{?_isa} = %{version}-%{release}

%description mpich-qt
Qt bindings for VTK with mpich.
%endif

%if %{with openmpi}
%global mpi_list %mpi_list openmpi
%package openmpi
Summary: The Visualization Toolkit - openmpi version

Obsoletes: %{name}-openmpi-tcl < 8.2.0-1
Obsoletes: %{name}-openmpi-qt-tcl < 8.2.0-1
%if %{without java}
Obsoletes:     %{name}-mpich-java < %{version}-%{release}
Obsoletes:     %{name}-mpich-java-devel < %{version}-%{release}
%endif

%description openmpi
VTK is an open-source software system for image processing, 3D
graphics, volume rendering and visualization. VTK includes many
advanced algorithms (e.g., surface reconstruction, implicit modeling,
decimation) and rendering techniques (e.g., hardware-accelerated
volume rendering, LOD control).

NOTE: The version in this package has been compiled with openmpi support.

%package openmpi-devel
Summary: VTK header files for building C++ code with openmpi
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
%if %{with java}
Requires: %{name}-openmpi-java%{?_isa} = %{version}-%{release}
%endif
Requires: python%{python3_pkgversion}-%{name}-openmpi%{?_isa} = %{version}-%{release}
Requires: openmpi-devel
Requires: hdf5-openmpi-devel%{?_isa}
Requires: netcdf-openmpi-devel%{?_isa}
%{vtk_devel_requires}

%description openmpi-devel
This provides the VTK header files required to compile C++ programs that
use VTK to do 3D visualization.

NOTE: The version in this package has been compiled with openmpi support.

%package -n python%{python3_pkgversion}-%{name}-openmpi
Summary: Python 3 bindings for VTK with openmpi
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}
Obsoletes: python3-vtk-openmpi-qt < 8.2.0-15
Provides:  python%{python3_pkgversion}-vtk-openmpi-qt = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{name}-openmpi
Python 3 bindings for VTK with openmpi.

%if %{with java}
%package openmpi-java
Summary: Java bindings for VTK with openmpi
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-java
Java bindings for VTK with openmpi.

%package openmpi-java-devel
Summary: Java development for VTK with openmpi
Requires: %{name}-openmpi-java%{?_isa} = %{version}-%{release}
Requires: java-devel

%description openmpi-java-devel
Java development for VTK with openmpi.
%endif

%package openmpi-qt
Summary: Qt bindings for VTK with openmpi
Requires: %{name}-openmpi%{?_isa} = %{version}-%{release}

%description openmpi-qt
Qt bindings for VTK with openmpi.
%endif

%package data
Summary: VTK data files for tests/examples
BuildArch: noarch
Obsoletes: vtkdata < 6.1.0-3

%description data
VTK data files for tests and examples.

%package doc
Summary: API documentation for VTK
BuildArch: noarch

%description doc
Generated API documentation for VTK

%package testing
Summary: Testing programs for VTK
Requires: %{name}%{?_isa} = %{version}-%{release}, %{name}-data = %{version}

%description testing
Testing programs for VTK

%package examples
Summary: Examples for VTK
Requires: %{name}%{?_isa} = %{version}-%{release}, %{name}-data = %{version}

%description examples
This package contains many well-commented examples showing how to use
VTK. Examples are available in the C++, Tcl, Python and Java
programming languages.


%prep
%autosetup -p1 -b 1 -n VTK-%{version}
# Remove included thirdparty sources just to be sure
# TODO - diy2 - not yet packaged
# TODO - exodusII - not yet packaged
# TODO - verdict - not yet packaged
# TODO - VPIC - not yet packaged
# TODO - xdmf2 - not yet packaged
# TODO - xdmf3 - not yet packaged
for x in vtk{cli11,doubleconversion,eigen,expat,%{?with_fmt:fmt,}freetype,%{?with_gl2ps:gl2ps,}glew,hdf5,jpeg,jsoncpp,libharu,libproj,libxml2,lz4,lzma,mpi4py,netcdf,ogg,pegtl,png,pugixml,sqlite,theora,tiff,utf8,zfp,zlib}
do
  rm -r ThirdParty/*/${x}
done

# Remove unused KWSys items
find Utilities/KWSys/vtksys/ -name \*.[ch]\* | grep -vE '^Utilities/KWSys/vtksys/([a-z].*|Configure|SharedForward|Status|String\.hxx|Base64|CommandLineArguments|Directory|DynamicLoader|Encoding|FStream|FundamentalType|Glob|MD5|Process|RegularExpression|System|SystemInformation|SystemTools)(C|CXX|UNIX)?\.' | xargs rm

# Save an unbuilt copy of the Example's sources for %doc
mkdir vtk-examples
cp -a Examples vtk-examples
find vtk-examples -type f | xargs chmod -R a-x


%global vtk_cmake_options \\\
 -DCMAKE_POLICY_VERSION_MINIMUM=3.5 \\\
 -DCMAKE_INSTALL_DOCDIR=share/doc/%{name} \\\
 -DCMAKE_INSTALL_JARDIR=share/java \\\
 -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \\\
 -DCMAKE_INSTALL_JNILIBDIR:PATH=%{_lib}/%{name} \\\
 -DCMAKE_INSTALL_LICENSEDIR:PATH=share/licenses/%{name} \\\
 -DCMAKE_INSTALL_QMLDIR:PATH=%{_lib}/qt5/qml \\\
 -DVTK_CUSTOM_LIBRARY_SUFFIX="" \\\
 -DVTK_VERSIONED_INSTALL:BOOL=OFF \\\
 -DVTK_GROUP_ENABLE_Imaging:STRING=YES \\\
 -DVTK_GROUP_ENABLE_Qt:STRING=YES \\\
 -DVTK_GROUP_ENABLE_Rendering:STRING=YES \\\
 -DVTK_GROUP_ENABLE_StandAlone:STRING=YES \\\
 -DVTK_GROUP_ENABLE_Views:STRING=YES \\\
 -DVTK_GROUP_ENABLE_Web:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_CommonArchive:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_DomainsMicroscopy:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_GeovisGDAL:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_ImagingOpenGL2:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_InfovisBoost:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_InfovisBoostGraphAlgorithms:STRING=YES \\\
 -DVTK_MODULE_ENABLE_VTK_IOMySQL:STRING=YES \\\
 -DVTK_PYTHON_OPTIONAL_LINK:BOOL=OFF \\\
 -DVTK_PYTHON_VERSION=3 \\\
%if %{with OSMesa} \
 -DVTK_OPENGL_HAS_OSMESA:BOOL=ON \\\
%endif \
%if %{with java} \
 -DVTK_WRAP_JAVA:BOOL=ON \\\
 -DVTK_JAVA_SOURCE_VERSION=8 \\\
 -DVTK_JAVA_TARGET_VERSION=8 \\\
 -DJAVA_INCLUDE_PATH:PATH=$JAVA_HOME/include \\\
 -DJAVA_INCLUDE_PATH2:PATH=$JAVA_HOME/include/linux \\\
 -DJAVA_AWT_INCLUDE_PATH:PATH=$JAVA_HOME/include \\\
 -DJAVA_AWT_LIBRARY:PATH=$JAVA_HOME/lib/libjawt.so \\\
 -DJAVA_JNI_INCLUDE_PATH:PATH=$JAVA_HOME/include \\\
 -DJAVA_JVM_LIBRARY:PATH=$JAVA_HOME/lib/libjava.so \\\
%else \
 -DVTK_WRAP_JAVA:BOOL=OFF \\\
%endif \
 -DVTK_WRAP_PYTHON:BOOL=ON \\\
 -DVTK_USE_EXTERNAL=ON \\\
%if !%{with fmt} \
 -DVTK_MODULE_USE_EXTERNAL_VTK_fmt:BOOL=OFF \\\
%endif \
%if !%{with gl2ps} \
 -DVTK_MODULE_USE_EXTERNAL_VTK_gl2ps:BOOL=OFF \\\
%endif \
 -DVTK_MODULE_USE_EXTERNAL_VTK_exprtk:BOOL=OFF \\\
 -DVTK_MODULE_USE_EXTERNAL_VTK_ioss:BOOL=OFF \\\
 -DVTK_MODULE_USE_EXTERNAL_VTK_verdict:BOOL=OFF \\\
 -DVTK_USE_TK=ON \\\
  %{?with_flexiblas:-DBLA_VENDOR=FlexiBLAS}
# https://gitlab.kitware.com/cmake/cmake/issues/17223
#-DVTK_MODULE_ENABLE_VTK_IOPostgreSQL:STRING=YES \\\

# $mpi will be evaluated in the loops below
%global _vpath_builddir %{_vendor}-%{_target_os}-build-${mpi:-serial}

%build
export CFLAGS="%{optflags} -D_UNICODE -DHAVE_UINTPTR_T"
export CXXFLAGS="%{optflags} -D_UNICODE -DHAVE_UINTPTR_T"
export CPPFLAGS=-DACCEPT_USE_OF_DEPRECATED_PROJ_API_H
%if %{with java}
export JAVA_HOME=%{_prefix}/lib/jvm/java
%ifarch %{arm} s390x riscv64
# getting "java.lang.OutOfMemoryError: Java heap space" during the build
export JAVA_TOOL_OPTIONS=-Xmx2048m
%endif
%ifarch %{arm} riscv64
# Likely running out of memory during build
%global _smp_ncpus_max 2
%endif
%endif

%cmake %{cmake_gen} \
 %{vtk_cmake_options} \
 -DVTK_BUILD_DOCUMENTATION:BOOL=ON \
 -DVTK_BUILD_EXAMPLES:BOOL=ON \
 -DVTK_BUILD_TESTING:BOOL=ON
%cmake_build -- --output-sync
%cmake_build --target DoxygenDoc


export CC=mpicc
export CXX=mpic++
for mpi in %{mpi_list}
do
  module load mpi/$mpi-%{_arch}
  #CMAKE_INSTALL_LIBDIR -> ARCHIVE_DESTINATION must not be an absolute path
  %cmake %{cmake_gen} \
   %{vtk_cmake_options} \
   -DCMAKE_PREFIX_PATH:PATH=$MPI_HOME \
   -DCMAKE_INSTALL_PREFIX:PATH=$MPI_HOME \
   -DCMAKE_INSTALL_LIBDIR:PATH=lib \
   -DCMAKE_INSTALL_JNILIBDIR:PATH=lib/%{name} \
   -DCMAKE_INSTALL_QMLDIR:PATH=lib/qt5/qml \
   -DVTK_USE_MPI:BOOL=ON
  %cmake_build -- --output-sync
  module purge
done

# Remove executable bits from sources (some of which are generated)
find . -name \*.c -or -name \*.cxx -or -name \*.h -or -name \*.hxx -or \
       -name \*.gif | xargs chmod -x


%install
%cmake_install

pushd %{_vpath_builddir}
# Gather list of non-java/python/qt libraries
ls %{buildroot}%{_libdir}/*.so.* \
  | grep -Ev '(Java|Qt|Python)' | sed -e's,^%{buildroot},,' > libs.list

# List of executable test binaries
find bin \( -name \*Tests -o -name Test\* -o -name VTKBenchMark \) \
         -printf '%f\n' > testing.list

# Install examples too, need to remove buildtime runpath manually
for file in `cat testing.list`; do
  install -p bin/$file %{buildroot}%{_bindir}
  chrpath -l -d %{buildroot}%{_bindir}/$file
done

# Fix up filelist paths
perl -pi -e's,^,%{_bindir}/,' testing.list

# Install data
mkdir -p %{buildroot}%{_datadir}/vtkdata
cp -alL ExternalData/* %{buildroot}%{_datadir}/vtkdata/

popd

for mpi in %{mpi_list}
do
  module load mpi/$mpi-%{_arch}
  %cmake_install

  # Gather list of non-java/pythonl/qt libraries
  ls %{buildroot}%{_libdir}/${mpi}/lib/*.so.* \
    | grep -Ev '(Java|Python|Qt)' | sed -e's,^%{buildroot},,' > %{_vpath_builddir}/libs.list

  # Move licenses since we cannot install them outside of CMAKE_INSTALL_PREFIX (MPI_HOME)
  mv %{buildroot}%{_libdir}/${mpi}/share/licenses/vtk %{buildroot}%{_defaultlicensedir}/%{name}-${mpi}
  module purge
done

# Remove exec bit from non-scripts and %%doc
for file in `find %{buildroot} -type f -perm 0755 \
  | xargs -r file | grep ASCII | awk -F: '{print $1}'`; do
  head -1 $file | grep '^#!' > /dev/null && continue
  chmod 0644 $file
done
find Utilities/Upgrading -type f -print0 | xargs -0 chmod -x

# Setup Wrapping docs tree
mkdir -p _docs
cp -pr --parents Wrapping/*/README* _docs/

# Make noarch data sub-package the same on all arches
# At the moment this only contains Java/Testing/Data/Baseline
rm -rf %{buildroot}%{_datadir}/vtkdata/Wrapping

# The fixed FindHDF5.cmake is patch of CMake now
rm -v %{buildroot}/%{_libdir}/cmake/%{name}/patches/99/FindHDF5.cmake
%if %{with mpich}
rm -v %{buildroot}/%{_libdir}/mpich/lib/cmake/%{name}/patches/99/FindHDF5.cmake
%endif
%if %{with openmpi}
rm -v %{buildroot}/%{_libdir}/openmpi/lib/cmake/%{name}/patches/99/FindHDF5.cmake
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1902729
#  contains the $ORIGIN runpath specifier at the wrong position in [/usr/lib64/mpich/lib:$ORIGIN:$ORIGIN/../]
#  0x0008 ... the special '$ORIGIN' RPATHs are appearing after other
#             RPATHs; this is just a minor issue but usually unwanted
# The paths are equivalent and "this is just a minor issue", so we are allowing it below
#  0x0010 ... the RPATH is empty; there is no reason for such RPATHs
#             and they cause unneeded work while loading libraries
# This is appearing on mpi libraries, no idea why.
export QA_RPATHS=18


%check
cp %SOURCE2 .
%if %{with xdummy}
if [ -x /usr/libexec/Xorg ]; then
   Xorg=/usr/libexec/Xorg
else
   Xorg=/usr/libexec/Xorg.bin
fi
$Xorg -noreset +extension GLX +extension RANDR +extension RENDER -logfile ./xorg.log -config ./xorg.conf -configdir . :99 &
export DISPLAY=:99
%endif
export FLEXIBLAS=netlib
%ctest --verbose || :
%if %{with xdummy}
kill %1 || :
cat xorg.log
%endif


%files -f %{_vendor}-%{_target_os}-build-serial/libs.list
%license %{_defaultlicensedir}/%{name}/
%doc README.md _docs/Wrapping

%files devel
%doc Utilities/Upgrading
%{_bindir}/vtkParseJava
%{_bindir}/vtkProbeOpenGLVersion
%{_bindir}/vtkWrapHierarchy
%{_bindir}/vtkWrapJava
%{_includedir}/%{name}
%{_libdir}/*.so
%{_libdir}/cmake/%{name}/
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/hierarchy/

%files -n python%{python3_pkgversion}-vtk
%{python3_sitearch}/*
%{_libdir}/*Python*.so.*
%{_bindir}/vtkpython
%{_bindir}/vtkWrapPython
%{_bindir}/vtkWrapPythonInit

%if %{with java}
%files java
%{_libdir}/*Java.so.*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/*Java.so
%{_javadir}/vtk.jar
%endif

%files qt
%{_libdir}/lib*Qt*.so.*
%exclude %{_libdir}/*Python*.so.*
%{_libdir}/qt5/qml/*

%if %{with mpich}
%files mpich -f %{_vendor}-%{_target_os}-build-mpich/libs.list
%license %{_defaultlicensedir}/%{name}-mpich/
%doc README.md _docs/Wrapping

%files mpich-devel
%{_libdir}/mpich/bin/vtkParseJava
%{_libdir}/mpich/bin/vtkProbeOpenGLVersion
%{_libdir}/mpich/bin/vtkWrapHierarchy
%{_libdir}/mpich/bin/vtkWrapJava
%{_libdir}/mpich/include/
%{_libdir}/mpich/lib/*.so
%{_libdir}/mpich/lib/cmake/
%dir %{_libdir}/mpich/lib/%{name}
%{_libdir}/mpich/lib/%{name}/hierarchy/

%files -n python%{python3_pkgversion}-vtk-mpich
%{_libdir}/mpich/lib/python%{python3_version}/
%{_libdir}/mpich/lib/*Python*.so.*
%{_libdir}/mpich/bin/pvtkpython
%{_libdir}/mpich/bin/vtkpython
%{_libdir}/mpich/bin/vtkWrapPython
%{_libdir}/mpich/bin/vtkWrapPythonInit

%if %{with java}
%files mpich-java
%{_libdir}/mpich/lib/*Java.so.*
%dir %{_libdir}/mpich/lib/%{name}
%{_libdir}/mpich/lib/%{name}/*Java.so
%{_libdir}/mpich/share/java/vtk.jar
%endif

%files mpich-qt
%{_libdir}/mpich/lib/lib*Qt*.so.*
%exclude %{_libdir}/mpich/lib/*Python*.so.*
%{_libdir}/mpich/lib/qt5/
%endif

%if %{with openmpi}
%files openmpi -f %{_vendor}-%{_target_os}-build-openmpi/libs.list
%license %{_defaultlicensedir}/%{name}-openmpi/
%doc README.md _docs/Wrapping

%files openmpi-devel
%{_libdir}/openmpi/bin/vtkParseJava
%{_libdir}/openmpi/bin/vtkProbeOpenGLVersion
%{_libdir}/openmpi/bin/vtkWrapHierarchy
%{_libdir}/openmpi/bin/vtkWrapJava
%{_libdir}/openmpi/include/
%{_libdir}/openmpi/lib/*.so
%{_libdir}/openmpi/lib/cmake/
%dir %{_libdir}/openmpi/lib/%{name}
%{_libdir}/openmpi/lib/%{name}/hierarchy/

%files -n python%{python3_pkgversion}-vtk-openmpi
%{_libdir}/openmpi/lib/python%{python3_version}/
%{_libdir}/openmpi/lib/*Python*.so.*
%{_libdir}/openmpi/bin/pvtkpython
%{_libdir}/openmpi/bin/vtkpython
%{_libdir}/openmpi/bin/vtkWrapPython
%{_libdir}/openmpi/bin/vtkWrapPythonInit

%if %{with java}
%files openmpi-java
%{_libdir}/openmpi/lib/*Java.so.*
%dir %{_libdir}/openmpi/lib/%{name}
%{_libdir}/openmpi/lib/%{name}/*Java.so
%{_libdir}/openmpi/share/java/vtk.jar
%endif

%files openmpi-qt
%{_libdir}/openmpi/lib/lib*Qt*.so.*
%exclude %{_libdir}/openmpi/lib/*Python*.so.*
%{_libdir}/openmpi/lib/qt5/
%endif

%files data
%{_datadir}/vtkdata

%files doc
%{_docdir}/%{name}/

%files testing -f %{_vendor}-%{_target_os}-build-serial/testing.list

%files examples
%doc vtk-examples/Examples


%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 9.2.6-44
- test: add initial lock files

* Sun Sep 21 2025 Python Maint <python-maint@redhat.com> - 9.2.6-43
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 9.2.6-42
- Rebuilt for Python 3.14.0rc2 bytecode

* Sat Aug 09 2025 Orion Poplawski <orion@nwra.com> - 9.2.6-41
- Rebuild for libharu 2.4.5

* Tue Jul 29 2025 Sandro Mani <manisandro@gmail.com> - 9.2.6-40
- Rebuild (gdal)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.6-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 9.2.6-38
- Rebuilt for Python 3.14

* Sun Mar 02 2025 Christoph Junghans <junghans@votca.org> - 9.2.6-37
- Remove obsolete FindHDF5.cmake

* Thu Feb 27 2025 Björn Esser <besser82@fedoraproject.org> - 9.2.6-36
- Explicitly set CMAKE_POLICY_VERSION_MINIMUM=3.5

* Thu Feb 27 2025 Björn Esser <besser82@fedoraproject.org> - 9.2.6-35
- Rebuild (jsoncpp)

* Thu Feb 13 2025 Orion Poplawski <orion@nwra.com> - 9.2.6-26
- Rebuild with hdf5 1.14.6

* Tue Jan 28 2025 Sandro Mani <manisandro@gmail.com> - 9.2.6-25
- Rebuild for cgnslib built with scoped enums

* Mon Jan 27 2025 Sandro Mani <manisandro@gmail.com> - 9.2.6-24
- Rebuild (cgnslib)

* Fri Jan 24 2025 Sandro Mani <manisandro@gmail.com> - 9.2.6-23
- Rebuild (cgnslib)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.6-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 08 2024 Sandro Mani <manisandro@gmail.com> - 9.2.6-21
- Rebuild (gdal)

* Thu Oct 31 2024 Christoph Junghans <junghans@votca.org> - 9.2.6-20
- Add missing dep to mpi-devel packages

* Fri Oct 25 2024 Orion Poplawski <orion@nwra.com> - 9.2.6-19
- Rebuild for hdf5 1.14.5

* Tue Oct 08 2024 Orion Poplawski <orion@nwra.com> - 9.2.6-18
- Add upstream patch to fix segmentation fault on import with Python 3.13
  (rhbz#2310520)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.6-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 9.2.6-16
- Rebuilt for Python 3.13

* Mon May 13 2024 Sandro Mani <manisandro@gmail.com> - 9.2.6-15
- Rebuild (gdal)

* Wed Apr 10 2024 Orion Poplawski <orion@nwra.com> - 9.2.6-14
- Set Java source/target version to 8 (FTBFS bz#2272954)

* Sat Feb 24 2024 David Abdurachmanov <davidlt@rivosinc.com> - 9.2.6-13
- Reduce memory and ncpu usage during riscv64 builds

* Wed Jan 24 2024 Orion Poplawski <orion@nwra.com> - 9.2.6-12
- Drop mpi4py-mpich BR on i686 (bz#2259594)

* Wed Jan 17 2024 Jonathan Wakely <jwakely@redhat.com> - 9.2.6-12
- Rebuilt for Boost 1.83

* Wed Nov 15 2023 Sandro Mani <manisandro@gmail.com> - 9.2.6-11
- Rebuild (gdal)

* Thu Nov 02 2023 Philip Matura <pfed@tura-home.de> - 9.2.6-10
- Move API docs to separate doc sub-package (bz#2247327)

* Wed Oct 11 2023 Orion Poplawski <orion@nwra.com> - 9.2.6-9
- Rebuild for openslide 4.0.0

* Sun Sep 17 2023 Orion Poplawski <orion@nwra.com> - 9.2.6-8
- Use loops for mpi builds/intalls

* Sun Sep 10 2023 Orion Poplawski <orion@nwra.com> - 9.2.6-7
- Fix -devel deps on netcdf-*-devel

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Sandro Mani <manisandro@gmail.com> - 9.2.6-5
- Rebuild (cgnslib)

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 9.2.6-4
- Rebuilt for Python 3.12

* Thu May 11 2023 Sandro Mani <manisandro@gmail.com> - 9.2.6-3
- Rebuild (gdal)

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 9.2.6-2
- Rebuilt for Boost 1.81

* Sun Feb 19 2023 Orion Poplawski <orion@nwra.com> - 9.2.6-1
- Update to 9.2.6

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Orion Poplawski <orion@nwra.com> - 9.2.5-1
- Update to 9.2.5
- Use SPDX License tag

* Sat Nov 12 2022 Sandro Mani <manisandro@gmail.com> - 9.1.0-18
- Rebuild (gdal)

* Thu Jul 28 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-17
- Remove all of vtkdata/Wrapping to keep vtk-data noarch

* Thu Jul 28 2022 Mamoru TASAKA <mtasaka@fedoraproject.org> - 9.1.0-16
- Make -data subpackage arch-dependent for now due to
  java removal (bz#2104109)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 10 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-14
- Drop java for i686 (bz#2104109)

* Tue Jun 28 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-13
- Add patch to support netcdf 4.9.0

* Fri Jun 24 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-12
- Set VTK_PYTHON_OPTIONAL_LINK=OFF (bz#1979611)
- Link libvtkkissfft.so.1 against libm (bz#2100573)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 9.1.0-11
- Rebuilt for Python 3.11

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 9.1.0-10
- Rebuild for gdal-3.5.0 and/or openjpeg-2.5.0

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 9.1.0-9
- Rebuilt for Boost 1.78

* Tue Mar 22 2022 Sandro Mani <manisandro@gmail.com> - 9.1.0-8
- Rebuild for cgnslib-4.3.0

* Thu Mar 03 2022 Sandro Mani <manisandro@gmail.com> - 9.1.0-7
- Rebuild for proj-9.0.0

* Thu Feb 10 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-6
- Rebuild for glew 2.2

* Sat Feb 05 2022 Jiri Vanek <jvanek@redhat.com> - 9.1.0-5
- Rebuilt for java-17-openjdk as system jdk

* Sat Jan 29 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-4
- Use export CC/CXX to set MPI compiler

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 20 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-3
- Use %%global to define __cc/__cxx

* Fri Jan 07 2022 Orion Poplawski <orion@nwra.com> - 9.1.0-2
- Make java-devel only be brought in by vtk-java-devel

* Sun Nov 21 2021 Orion Poplawski <orion@nwra.com> - 9.1.0-1
- Update to 9.1.0

* Thu Nov 11 2021 Sandro Mani <manisandro@gmail.com> - 9.0.3-4
- Rebuild (gdal)

* Wed Nov 03 2021 Björn Esser <besser82@fedoraproject.org> - 9.0.3-3
- Rebuild (jsoncpp)

* Sun Sep 26 2021 Orion Poplawski <orion@nwra.com> - 9.0.3-2
- Cleanup rpath handling (bz#1902729)

* Wed Sep 15 2021 Orion Poplawski <orion@nwra.com> - 9.0.3-1
- Update to 9.0.3
- Add upstream patch to fix Mayavi crash (bz#1966135)

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 9.0.2-6
- Rebuild for hdf5 1.10.7/netcdf 4.8.0

* Tue Aug 10 2021 Orion Poplawski <orion@nwra.com> - 9.0.2-5
- More rpath cleanup

* Sat Aug 07 2021 Jonathan Wakely <jwakely@redhat.com> - 9.0.2-4
- Rebuilt for Boost 1.76

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Björn Esser <besser82@fedoraproject.org> - 9.0.2-2
- Properly set BLA_VENDOR to FlexiBLAS for cmake >= 3.19

* Thu Jul 01 2021 Orion Poplawski <orion@nwra.com> - 9.0.2-1
- Update to 9.0.2

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 9.0.1-9
- Rebuilt for Python 3.10

* Fri May 21 2021 Sandro Mani <manisandro@gmail.com> - 9.0.1-8
- Rebuild (gdal)

* Thu May 20 2021 Richard Shaw <hobbes1069@gmail.com> - 9.0.1-7
- Rebuild for gdal 3.3.0.

* Fri May 07 2021 Sandro Mani <manisandro@gmail.com> - 9.0.1-6
- Rebuild (gdal)

* Fri Apr 02 2021 Orion Poplawski <orion@nwra.com> - 9.0.1-5
- Make vtk-devel package require vtk-java

* Sat Mar 13 2021 Orion Poplawski <orion@nwra.com> - 9.0.1-4
- Add upstream patch for proj 5 support

* Sun Mar 07 2021 Sandro Mani <manisandro@gmail.com> - 9.0.1-4
- Rebuild (proj)

* Mon Feb 15 2021 Orion Poplawski <orion@nwra.com> - 9.0.1-3
- Bump python3-vtk-qt obsoletes

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 9.0.1-2
- rebuild for libpq ABI fix rhbz#1908268

* Sat Jan 30 2021 Orion Poplawski <orion@nwra.com> - 9.0.1-1
- Update to 9.0.1
- Disable OSMesa - conflicts with X support
- Build against Fedora gl2ps, libharu, utf8cpp
- Drop python3-vtk-qt packages
- No longer ship compiled examples
- Install jar file into /usr/share/java
- Fix JNI install location
- Drop Qt4 build option

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov  5 20:45:48 CET 2020 Sandro Mani <manisandro@gmail.com> - 8.2.0-25
- Rebuild (proj)

* Thu Sep 17 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-24
- Add patch to fix build with Qt 5.15

* Thu Aug 27 2020 Iñaki Úcar <iucar@fedoraproject.org> - 8.2.0-23
- https://fedoraproject.org/wiki/Changes/FlexiBLAS_as_BLAS/LAPACK_manager

* Sun Aug  9 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-22
- Fix ExternalData in vtk-data (bz#1783622)

* Tue Aug  4 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-21
- Use new cmake macros

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 8.2.0-19
- Use __cmake_in_source_build

* Sat Jul 11 2020 Jiri Vanek <jvanek@redhat.com> - 8.2.0-18
- Rebuilt for JDK-11, see https://fedoraproject.org/wiki/Changes/Java11

* Thu Jun 25 2020 Orion Poplawski <orion@cora.nwra.com> - 8.2.0-17
- Rebuild for hdf5 1.10.6

* Sat Jun 20 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-16
- Drop _python_bytecompile_extra, python2 conditionals

* Sat May 30 2020 Björn Esser <besser82@fedoraproject.org> - 8.2.0-15
- Rebuild (jsoncpp)

* Wed May 27 2020 Orion Poplawski <orion@nwra.com> - 8.2.0-14
- Add patch to fix building with GCC 10 (bz#1800240)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 8.2.0-14
- Rebuilt for Python 3.9

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 14 2019 Björn Esser <besser82@fedoraproject.org> - 8.2.0-12
- Rebuild (jsoncpp)

* Sat Nov  9 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-11
- Drop BR on sip-devel (python2)

* Sun Sep 22 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-10
- Rebuild for double-conversion 3.1.5

* Mon Sep 09 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-9
- Rebuild for proj 6.2.0
- Add patch and flags for proj 6 support

* Tue Aug 20 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-8
- Add upstream patch to support Python 3.8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 8.2.0-7
- Rebuilt for Python 3.8

* Wed Jul 31 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-6
- BR motif-devel instead of /usr/include/Xm (bugz#1731728)

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Björn Esser <besser82@fedoraproject.org> - 8.2.0-4
- Rebuild (jsoncpp)

* Thu Apr 18 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-3
- Provide starndard python 3.Y dist name (bugz#1700307)

* Tue Apr 16 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-2
- Provide standard python 3 dist name (bugz#1700307)

* Sat Mar 16 2019 Orion Poplawski <orion@nwra.com> - 8.2.0-1
- Update to 8.2.0
- TCL wrapping has been dropped upstream
- Build with system glew

* Fri Feb 15 2019 Orion Poplawski <orion@nwra.com> - 8.1.1-3
- Rebuild for openmpi 3.1.3

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 26 2018 Orion Poplawski <orion@cora.nwra.com> - 8.1.1-1
- Update to 8.1.1 (bug #1460059)
- Use Qt 5 (bug #1319504)
- Use Python 3 for Fedora 30+ (bug #1549034)

* Thu Sep 06 2018 Pavel Raiskup <praiskup@redhat.com> - 7.1.1-13
- rebuild against libpq (rhbz#1618698, rhbz#1623764)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 7.1.1-11
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 26 2017 Björn Esser <besser82@fedoraproject.org> - 7.1.1-9
- Rebuilt for jsoncpp.so.20

* Mon Dec 18 2017 Orion Poplawski <orion@nwra.com> - 7.1.1-8
- Enable mysql and postgresql support
- Use mariadb BR for F28+ (Bug #1494054)

* Fri Sep 01 2017 Björn Esser <besser82@fedoraproject.org> - 7.1.1-7
- Rebuilt for jsoncpp-1.8.3

* Sat Aug 12 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.1.1-6
- Python 2 binary packages renamed to python2-vtk and python2-vtk-qt
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Tue May 9 2017 Orion Poplawski <orion@cora.nwra.com> - 7.1.1-2
- Enable tests on s390x

* Mon May 8 2017 Orion Poplawski <orion@cora.nwra.com> - 7.1.1-1
- Update to 7.1.1

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 3 2017 Dan Horák <dan[at]danny.cz> - 7.1.0-5
- s390x needs increased Java heap size

* Thu Dec 29 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1.0-4
- Drop setting java heap size

* Thu Dec 8 2016 Dan Horák <dan[at]danny.cz> - 7.1.0-3
- Enable openmpi on s390(x)
- Add missing conditions for mpich/openmpi subpackages

* Thu Dec 8 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1.0-2
- Fix MPI library install location

* Mon Dec 5 2016 Orion Poplawski <orion@cora.nwra.com> - 7.1.0-1
- Update to 7.1.0
- Enable OSMesa
- Build MPI versions
- Use bundled glew

* Wed Nov 2 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-12
- Rebuild for R openblas changes

* Mon Oct 03 2016 Björn Esser <fedora@besser82.io> - 6.3.0-11
- Rebuilt for libjsoncpp.so.11

* Thu Jul 28 2016 Than Ngo <than@redhat.com> - 6.3.0-10
- %%check: make non-fatal as temporary workaround for build on s390x

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-8
- Rebuild for hdf5 1.8.17

* Fri Mar 25 2016 Björn Esser <fedora@besser82.io> - 6.3.0-7
- Rebuilt for libjsoncpp.so.1

* Mon Feb 8 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-6
- Add patch for gcc 6 support

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-4
- Rebuild for netcdf 4.4.0

* Sat Jan 16 2016 Jonathan Wakely <jwakely@redhat.com> - 6.3.0-3
- Rebuilt for Boost 1.60

* Wed Oct 21 2015 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-2
- Note bundled libraries

* Tue Sep 15 2015 Orion Poplawski <orion@cora.nwra.com> - 6.3.0-1
- Update to 6.3.0

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 6.2.0-10
- Rebuilt for Boost 1.59

* Fri Aug 21 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-9
- Note bundled kwsys, remove unused kwsys files

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 6.2.0-7
- rebuild for Boost 1.58

* Tue Jul 7 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-6
- Drop glext patch, no longer needed

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 23 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-4
- Add requires netcdf-cxx-devel to vtk-devel (bug #1224512)

* Sun May 17 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-3
- Rebuild for hdf5 1.8.15

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 6.2.0-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Mar 18 2015 Orion Poplawski <orion@cora.nwra.com> - 6.2.0-1
- Update to 6.2.0
- Remove type, system, install, and netcdf patches applied upstream
- Integrate and replace vtkdata
- Build and run tests again
- Generate testing.list based on executable name

* Thu Mar 05 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-26
- Add needed vtk-*-devel requires to vtk-devel (bug #1199310)

* Wed Mar 04 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-25
- Rebuild for jsoncpp

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 6.1.0-24
- Bump for rebuild.

* Tue Feb 3 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-23
- Add patch to fix tcl library loading

* Mon Jan 26 2015 Petr Machata <pmachata@redhat.com> - 6.1.0-22
- Rebuild for boost 1.57.0

* Mon Jan 19 2015 François Cami <fcami@fedoraproject.org> - 6.1.0-21
- Switch to non-explicit arch requires for now (bugs #1183210 #1183530)

* Sat Jan 17 2015 François Cami <fcami@fedoraproject.org> - 6.1.0-20
- Add jsoncpp-devel and python2-devel to vtk-devel Requires (bug #1183210)

* Thu Jan 08 2015 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-19
- Rebuild for hdf5 1.8.14
- Add patch to fix compilation error

* Thu Nov 20 2014 Dan Horák <dan[at]danny.cz> - 6.1.0-18
- Don't override Java memory settings on s390 (related to bug #1115920)

* Wed Nov 19 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-17
- Add patch to fix compilation with mesa 10.4 (bug #1138466)

* Fri Oct 31 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-16
- No longer need cmake28 on RHEL6

* Thu Sep 4 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-15
- Increase java heap space for builds (bug #1115920)

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jun 10 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-13
- Rebuild for hdf 1.8.13

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun 5 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-11
- Add requires on blas-devel and lapack-devel to vtk-devel (bug #1105004)

* Tue May 27 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-10
- Rebuild for Tcl 8.6

* Fri May 23 2014 Petr Machata <pmachata@redhat.com> - 6.1.0-9
- Rebuild for boost 1.55.0

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 6.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Tue May  6 2014 Tom Callaway <spot@fedoraproject.org> - 6.1.0-7
- rebuild against R 3.1.0 (without bundled blas/lapack)

* Wed Mar 26 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-5
- Add Requires: qtwebkit-devel and hdf5-devel to vtk-devel (bug #1080781)

* Tue Jan 28 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-4
- Really fix requires freetype-devel

* Mon Jan 27 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-3
- Fix requires freetype-devel

* Sun Jan 26 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-2
- Add Requires: libfreetype-devel; libxml2-devel to vtk-devel (bug #1057924)

* Thu Jan 23 2014 Orion Poplawski <orion@cora.nwra.com> - 6.1.0-1
- Update to 6.1.0
- Rebase patches, drop vtkpython patch
- Disable BUILD_TESTING for now until we can provide test data

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-10
- Add patch to use system netcdf

* Sun Dec 22 2013 Kevin Fenzi <kevin@scrye.com> 6.0.0-9
- Add BuildRequires on blas-devel and lapack-devel

* Sun Dec 22 2013 François Cami <fcami@fedoraproject.org> - 6.0.0-8
* Rebuild for rawhide.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 6.0.0-6
- Rebuild for boost 1.54.0

* Mon Jul 29 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-5
- Enable VTK_WRAP_PYTHON_SIP

* Fri Jul 26 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-4
- Add patch to install vtkpython

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 6.0.0-3
- Perl 5.18 rebuild

* Mon Jul 15 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-2
- Install vtkMakeInstantiator files for gdcm build

* Fri Jul 12 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-1
- Add BR on R-devel

* Thu Jun 27 2013 Orion Poplawski <orion@cora.nwra.com> - 6.0.0-1
- Update to 6.0.0

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 5.10.1-5
- Rebuild for hdf5 1.8.11

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 5.10.1-3
- rebuild due to "jpeg8-ABI" feature drop

* Mon Dec 03 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.1-2
- Rebuild for hdf5 1.8.10
- Change doc handling

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.1-1
- Update to 5.10.1

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu May 24 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.0-2
- Add patch to add soname to libvtkNetCDF_cxx

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 5.10.0-1
- Update to 5.10.0

* Tue May 15 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 5.8.0-6
- Add cmake28 usage when building for EL6
- Disable -java build on PPC64 as it fails to build

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.8.0-5
- Rebuilt for c++ ABI breakage

* Sun Jan 8 2012 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-4
- Rebuild with gcc 4.7

* Fri Nov 18 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-3
- Rebuild for hdf5 1.8.8, add explicit requires

* Tue Nov 1 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-2
- Keep libraries in %%{_libdir}/vtk, use ld.so.conf.d

* Fri Oct 7 2011 Orion Poplawski <orion@cora.nwra.com> - 5.8.0-1
- Update to 5.8.0
- Drop version from directory names
- Use VTK_PYTHON_SETUP_ARGS instead of patch to set python install dir
- Drop several patches fixed upstream
- Remove rpaths from all hand installed binaries (Bug 744437)
- Don't link against OSMesa (Bug 744434)

* Thu Jun 23 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-10
- Add BR qtwebkit-devel, fixes FTBS bug 715770

* Thu May 19 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-9
- Update soversion patch to add soversion to libvtkNetCDF.so

* Mon Mar 28 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-8
- Rebuild for new mysql

* Thu Mar 17 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-7
- Add needed requires to vtk-devel

* Wed Mar 16 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-6
- Turn on boost, mysql, postgres, ogg theora, and text analysis support,
  bug 688275.

* Wed Mar 16 2011 Marek Kasik <mkasik@redhat.com> - 5.6.1-5
- Add backslashes to VTK_INSTALL_LIB_DIR and
- VTK_INSTALL_INCLUDE_DIR (#687895)

* Tue Mar 15 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-4
- Set VTK_INSTALL_LIB_DIR, fix bug 687895

* Fri Feb 18 2011 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-3
- Add patch to support gcc 4.6
- Add patch to make using system libraries easier
- Update pythondestdir patch to use --prefix and --root
- Use system gl2ps and libxml2
- Use standard cmake build macro, out of tree builds
- Add patch from upstream to add sonames to libCosmo and libVPIC (bug #622840)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 7 2010 Orion Poplawski <orion@cora.nwra.com> - 5.6.1-1
- Update to 5.6.1
- Enable qt4 support, drop qt3 support

* Wed Oct 20 2010 Adam Jackson <ajax@redhat.com> 5.6.0-37
- Rebuild for new libOSMesa soname

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 5.6.0-36
- add python 2.7 compat patch

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 5.6.0-35
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Jul  5 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.6.0-34
- Update to 5.6.0.

* Sat Jun  6 2009 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.4.2-30
- Update to 5.4.2.

* Thu Mar 12 2009 Orion Poplawski <orion@cora.nwra.com> - 5.2.1-29
- Update to 5.2.1

* Fri Mar 06 2009 Jesse Keating <jkeating@redhat.com> - 5.2.0-28
- Remove chmod on examples .so files, none are built.  This needs
  more attention.

* Sun Oct  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.2.0-26
- Update to 5.2.0.

* Wed Oct 1 2008 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-25
- Fix patch fuzz

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-24
- Change java build dependencies from java-devel to gcj.

* Sun Aug 24 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-23
- %%check || : does not work anymore.
- enable java by default.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.0.4-22
- fix license tag

* Sat Apr 12 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-21
- Fixes for gcc 4.3 by Orion Poplawski.

* Sat Apr  5 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-20
- Change BR to qt-devel to qt3-devel.

* Sat Feb 23 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.4-19
- Update to 5.0.4.

* Mon May 28 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-18
- Move headers to %%{_includedir}/vtk.
- Remove executable bit from sources.

* Mon Apr 16 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-17
- Make java build conditional.
- Add ldconfig %%post/%%postun for java/qt subpackages.

* Sun Apr 15 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.3-16
- Remove %%ghosting pyc/pyo.

* Wed Apr 04 2007 Paulo Roma <roma@lcg.ufrj.br> - 5.0.3-15
- Update to 5.0.4.
- Added support for qt4 plugin.

* Wed Feb  7 2007 Orion Poplawski <orion@cora.nwra.com> - 5.0.2-14
- Enable Java, Qt, GL2PS, OSMESA

* Mon Sep 11 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.2-13
- Update to 5.0.2.

* Sun Aug  6 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-12
- cmake needs to be >= 2.0.4.

* Fri Aug  4 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-11
- Fix some python issues including pyo management.

* Sun Jul 23 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-10
- Embed feedback from bug 199405 comment 5.
- Fix some Group entries.
- Remove redundant dependencies.
- Use system libs.
- Comment specfile more.
- Change buildroot handling with CMAKE_INSTALL_PREFIX.
- Enable qt designer plugin.

* Wed Jul 19 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-7
- Fix some permissions for rpmlint and debuginfo.

* Sun Jul 16 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-7
- Remove rpath and some further rpmlint warnings.

* Thu Jul 13 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 5.0.1-6
- Update to 5.0.1.

* Wed May 31 2006 Axel Thimm <Axel.Thimm@ATrpms.net>
- Update to 5.0.

* Mon Apr 05 2004 Intrinsic Spin <spin@freakbait.com> 2.mr
- built on a machine with a stock libGL.so

* Sun Apr 04 2004 Intrinsic Spin <spin@freakbait.com>
- little cleanups
- Built for FC1

* Sun Jan 11 2004 Intrinsic Spin <spin@freakbait.com>
- Built against a reasonably good (according to dashboard) CVS version so-as
 to get GL2PS support.
- Rearranged. Cleaned up. Added some comments.

* Sat Jan 10 2004 Intrinsic Spin <spin@freakbait.com>
- Blatently stole this spec file for my own nefarious purposes.
- Removed Java (for now). Merged the Python and Tcl stuff into
 the main rpm.

* Fri Dec 05 2003 Fabrice Bellet <Fabrice.Bellet@creatis.insa-lyon.fr>
- (See Fabrice's RPMs for any more comments --Spin)

## END: Generated by rpmautospec
