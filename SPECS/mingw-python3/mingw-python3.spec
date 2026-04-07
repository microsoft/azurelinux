# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

# https://src.fedoraproject.org/rpms/redhat-rpm-config/pull-request/166#comment-95032
%undefine _auto_set_build_flags

%global pkgname python3
%global py_ver 3.11
%global py_ver_nodots 311
%global mingw32_py3_libdir       %{mingw32_libdir}/python%{py_ver}
%global mingw64_py3_libdir       %{mingw64_libdir}/python%{py_ver}
%global mingw32_py3_hostlibdir   %{_prefix}/%{mingw32_target}/lib/python%{py_ver}
%global mingw64_py3_hostlibdir   %{_prefix}/%{mingw64_target}/lib/python%{py_ver}
%global mingw32_py3_incdir       %{mingw32_includedir}/python%{py_ver}
%global mingw64_py3_incdir       %{mingw64_includedir}/python%{py_ver}
%global mingw32_python3_sitearch %{mingw32_libdir}/python%{py_ver}/site-packages
%global mingw64_python3_sitearch %{mingw64_libdir}/python%{py_ver}/site-packages

# Some of the files below /usr/lib/pythonMAJOR.MINOR/test  (e.g. bad_coding.py)
# are deliberately invalid, leading to SyntaxError exceptions if they get
# byte-compiled.
%global _python_bytecompile_errors_terminate_build 0

#global pre rc2

Name:          mingw-%{pkgname}
Version:       3.11.14
Release:       7%{?dist}
Summary:       MinGW Windows %{pkgname}

BuildArch:     noarch
License:       Python-2.0.1
URL:           https://www.python.org/
Source0:       http://www.python.org/ftp/python/%{version}/Python-%{version}%{?pre}.tar.xz

Source1:       macros.mingw32-python3
Source2:       macros.mingw64-python3
Source3:       mingw32_python3.attr
Source4:       mingw64_python3.attr


# Add support for building with mingw
Patch1:        mingw-python3_platform-mingw.patch
# Implement setenv for mingw
Patch2:        mingw-python3_setenv.patch
# Ignore main program for frozen scripts
Patch3:        mingw-python3_frozenmain.patch
# Link resource files and build pythonw.exe
Patch4:        mingw-python3_pythonw.patch
# Implement PyThread_get_thread_native_id for mingw-win-pthread
Patch5:        mingw-python3_pthread_threadid.patch
# Output list of failed modules to mods_failed.txt so that we can abort the build
Patch6:        mingw-python3_mods-failed.patch
# Adapt distutils for cross-compiling
Patch7:        mingw-python3_distutils.patch
# Make sysconfigdata.py relocatable
Patch8:        mingw-python3_make-sysconfigdata.py-relocatable.patch
# Fix module builds: select, ssl, multiprocessing
# Disable modules which do not build
# Fix broken parallel make
Patch9:        mingw-python3_modules.patch
# Use POSIX layout
Patch10:       mingw-python3_posix-layout.patch
# Enable some modules needed on Windows
Patch11:       mingw-python3_win-modules.patch
# Enable the socket module
Patch12:       mingw-python3_module-socket.patch
# MinGW fix for select module
Patch13:       mingw-python3_module-select.patch
# Add -lpython<VER> to Libs: in pkgconfig (windows extensions need to be linked against libpython)
Patch14:       mingw-python3_pkgconfig.patch
# Backport: Fix build with tcl9
Patch15:       https://github.com/python/cpython/commit/e0799352823289fafb8131341abd751923ee9c08.patch
# Backport fix for CVE-2025-6075
Patch16:       https://github.com/python/cpython/commit/5dceb93486176e6b4a6d9754491005113eb23427.patch
# Backport fix for CVE-2025-12084
# https://github.com/python/cpython/pull/142212
Patch17:       CVE-2025-12084.patch
# Backport proposed fix for CVE-2025-13836
# https://github.com/python/cpython/pull/142141
Patch18:       CVE-2025-13836.patch
# Backport fix for CVE-2025-11468
# https://github.com/python/cpython/commit/e9970f077240c7c670e8a6fc6662f2b30d3b6ad0
Patch19:       CVE-2025-11468.patch
# Backport fix for CVE-2026-0672
# https://github.com/python/cpython/commit/b1869ff648bbee0717221d09e6deff46617f3e85
Patch20:       CVE-2026-0672.patch
# Backport fix for CVE-2026-0865
# https://github.com/python/cpython/commit/e4846a93ac07a8ae9aa18203af0dd13d6e7a6995
Patch21:       CVE-2026-0865.patch
# Backport fix for CVE-2025-15282
# https://github.com/python/cpython/commit/3f396ca9d7bbe2a50ea6b8c9b27c0082884d9f80
Patch22:       CVE-2025-15282.patch
# Backport fix for CVE-2026-1299
# https://github.com/python/cpython/commit/842ce19a0c0b58d61591e8f6a708c38db1fb94e4
Patch23:       CVE-2026-1299.patch


BuildRequires: make
BuildRequires: automake autoconf libtool
BuildRequires: autoconf-archive
BuildRequires: python%{py_ver}-devel

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc
# Needed for correct value of CXX in _sysconfigdata.py
BuildRequires: mingw32-gcc-c++
BuildRequires: mingw32-bzip2
BuildRequires: mingw32-dlfcn
BuildRequires: mingw32-expat
BuildRequires: mingw32-libffi
BuildRequires: mingw32-openssl
BuildRequires: mingw32-sqlite
BuildRequires: mingw32-tcl
BuildRequires: mingw32-tk

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc
# Needed for correct value of CXX in _sysconfigdata.py
BuildRequires: mingw64-gcc-c++
BuildRequires: mingw64-bzip2
BuildRequires: mingw64-dlfcn
BuildRequires: mingw64-expat
BuildRequires: mingw64-libffi
BuildRequires: mingw64-openssl
BuildRequires: mingw64-sqlite
BuildRequires: mingw64-tcl
BuildRequires: mingw64-tk


%description
MinGW Windows %{pkgname}


%package -n mingw32-%{pkgname}
Summary:       MinGW Windows %{pkgname}
Requires:      python%{py_ver}
Requires:      python%{py_ver}-devel
Requires:      python-rpm-macros
Requires:      python3-rpm-generators
Requires:      mingw32-dlfcn
Provides:      mingw32(python(abi)) = %{py_ver}

%description -n mingw32-%{pkgname}
MinGW Windows %{pkgname}.


%package -n mingw32-%{pkgname}-test
Summary:       MinGW Windows %{pkgname} - native testsuite
Requires:      mingw32-python3

%description -n mingw32-%{pkgname}-test
MinGW Windows %{pkgname} - native testsuite.


%package -n mingw32-%{pkgname}-tkinter
Summary:       MinGW Windows %{pkgname} - GUI toolkit
Requires:      mingw32-python3

%description -n mingw32-%{pkgname}-tkinter
MinGW Windows %{pkgname} - GUI toolkit.


%package -n mingw32-%{pkgname}-idle
Summary:       MinGW Windows %{pkgname} - development environment
Requires:      mingw32-python3

%description -n mingw32-%{pkgname}-idle
MinGW Windows %{pkgname} - development environment.


%package -n mingw64-%{pkgname}
Summary:       MinGW Windows %{pkgname}
Requires:      python%{py_ver}
Requires:      python%{py_ver}-devel
Requires:      python-rpm-macros
Requires:      python3-rpm-generators
Requires:      mingw64-dlfcn
Provides:      mingw64(python(abi)) = %{py_ver}

%description -n mingw64-%{pkgname}
MinGW Windows %{pkgname}.


%package -n mingw64-%{pkgname}-test
Summary:       MinGW Windows %{pkgname} - native testsuite
Requires:      mingw64-python3

%description -n mingw64-%{pkgname}-test
MinGW Windows %{pkgname} - native testsuite.


%package -n mingw64-%{pkgname}-tkinter
Summary:       MinGW Windows %{pkgname} - GUI toolkit
Requires:      mingw64-python3

%description -n mingw64-%{pkgname}-tkinter
MinGW Windows %{pkgname} - GUI toolkit.


%package -n mingw64-%{pkgname}-idle
Summary:       MinGW Windows %{pkgname} - development environment
Requires:      mingw64-python3

%description -n mingw64-%{pkgname}-idle
MinGW Windows %{pkgname} - development environment.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n Python-%{version}%{?pre}
autoreconf -vfi

# Ensure that we are using the system copy of various libraries rather than copies shipped in the tarball
rm -r Modules/expat
rm -r Modules/_ctypes/{darwin,libffi}*

# Just to be sure that we are using the wanted thread model
rm -f Python/thread_nt.h


%build
# FIXME: avoid incompatible-pointer-types errors
export MINGW32_CFLAGS="%{mingw32_cflags} -fpermissive"
export MINGW64_CFLAGS="%{mingw64_cflags} -fpermissive"
export MINGW32_MAKE_ARGS="WINDRES=%{mingw32_target}-windres LD=%{mingw32_target}-ld DLLWRAP=%{mingw32_target}-dllwrap"
export MINGW64_MAKE_ARGS="WINDRES=%{mingw64_target}-windres LD=%{mingw64_target}-ld DLLWRAP=%{mingw64_target}-dllwrap"

CONFIG_SITE=$PWD/config.site-mingw \
%mingw_configure \
--enable-shared \
--with-build-python=%{_bindir}/python3.11 \
--with-system-expat \
--with-suffix=.exe \
--enable-loadable-sqlite-extensions \
--with-ensurepip=no

# Create directories needed by build
mkdir -p build_win32/PC/icons build_win64/PC/icons

%mingw_make_build

# Abort build if not explicitly disabled modules failed to build
if [ -e build_win32/mods_failed.txt ]; then
    echo "The following modules failed to build for win32"
    cat build_win32/mods_failed.txt
fi
if [ -e build_win64/mods_failed.txt ]; then
    echo "The following modules failed to build for win64"
    cat build_win64/mods_failed.txt
fi
if [ -e build_win32/mods_failed.txt ] || [ -e build_win64/mods_failed.txt ]; then
    exit 1;
fi


%install
%mingw_make_install

# Link import library to libdir
ln -s %{mingw32_py3_libdir}/config-%{py_ver}/libpython%{py_ver}.dll.a %{buildroot}%{mingw32_libdir}/libpython%{py_ver}.dll.a
ln -s %{mingw64_py3_libdir}/config-%{py_ver}/libpython%{py_ver}.dll.a %{buildroot}%{mingw64_libdir}/libpython%{py_ver}.dll.a

# Copy some useful "stuff"
install -dm755 %{buildroot}%{mingw32_py3_libdir}/Tools/{i18n,scripts}
install -dm755 %{buildroot}%{mingw64_py3_libdir}/Tools/{i18n,scripts}
install -pm755 Tools/i18n/{msgfmt,pygettext}.py %{buildroot}%{mingw32_py3_libdir}/Tools/i18n/
install -pm755 Tools/i18n/{msgfmt,pygettext}.py %{buildroot}%{mingw64_py3_libdir}/Tools/i18n/
install -pm755 Tools/scripts/{README,*py} %{buildroot}%{mingw32_py3_libdir}/Tools/scripts/
install -pm755 Tools/scripts/{README,*py} %{buildroot}%{mingw64_py3_libdir}/Tools/scripts/

# Cleanup shebangs
find %{buildroot}%{mingw32_py3_libdir}/ -name '*.py' | xargs sed -i "s|#[ ]*![ ]*/usr/bin/env python$|#!/usr/bin/python3|"
find %{buildroot}%{mingw64_py3_libdir}/ -name '*.py' | xargs sed -i "s|#[ ]*![ ]*/usr/bin/env python$|#!/usr/bin/python3|"

# Remove references to build directory
for file in config-%{py_ver}/Makefile _sysconfigdata__win32_.py; do
    sed -i "s|%{_builddir}|/build|g" %{buildroot}%{mingw32_py3_libdir}/$file
    sed -i "s|%{_builddir}|/build|g" %{buildroot}%{mingw64_py3_libdir}/$file
done

# Fix permissons
find %{buildroot} -type f | xargs chmod 0644
find %{buildroot} -type f \( -name "*.dll" -o -name "*.exe" \) | xargs chmod 0755

# Don't ship manpages
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}

# Host site-packages skeleton
mkdir -p %{buildroot}%{mingw32_py3_hostlibdir}/site-packages
mkdir -p %{buildroot}%{mingw64_py3_hostlibdir}/site-packages

# Hackishly faked distutils/sysconfig.py
mkdir -p %{buildroot}%{mingw32_py3_hostlibdir}/distutils
mkdir -p %{buildroot}%{mingw64_py3_hostlibdir}/distutils
pushd %{buildroot}%{mingw32_libdir}/python%{py_ver}/distutils/
for file in *.py; do
    ln -s %{mingw32_libdir}/python%{py_ver}/distutils/$file %{buildroot}%{mingw32_py3_hostlibdir}/distutils/$file
done
popd
pushd %{buildroot}%{mingw64_libdir}/python%{py_ver}/distutils/
for file in *.py; do
    ln -s %{mingw64_libdir}/python%{py_ver}/distutils/$file %{buildroot}%{mingw64_py3_hostlibdir}/distutils/$file
done
popd
ln -s %{mingw32_py3_libdir}/distutils/command %{buildroot}%{mingw32_py3_hostlibdir}/distutils/command
ln -s %{mingw64_py3_libdir}/distutils/command %{buildroot}%{mingw64_py3_hostlibdir}/distutils/command
rm %{buildroot}%{mingw32_py3_hostlibdir}/distutils/sysconfig.py
rm %{buildroot}%{mingw64_py3_hostlibdir}/distutils/sysconfig.py

cat > %{buildroot}%{mingw32_py3_hostlibdir}/distutils/sysconfig.py <<EOF
import imp
import os
_sysconfig = imp.load_source('distutils.sysconfig', '%{mingw32_py3_libdir}/distutils/sysconfig.py')
from distutils.sysconfig import *
# Overwrite methods from sysconfig
if "mingw32" in os.getenv("CC"):
    get_python_inc = lambda plat_specific=0, prefix=None: "%{mingw32_py3_incdir}"
    get_python_lib = lambda plat_specific=0, standard_lib=0, prefix=None: "%{mingw32_python3_sitearch}"
else:
    get_python_inc = lambda plat_specific=0, prefix=None: "%{_includedir}/python%{py_ver}"
    get_python_lib = lambda plat_specific=0, standard_lib=0, prefix=None: "%{_libdir}/python%{py_ver}/site-packages"
EOF

cat > %{buildroot}%{mingw64_py3_hostlibdir}/distutils/sysconfig.py <<EOF
import imp
import os
_sysconfig = imp.load_source('distutils.sysconfig', '%{mingw64_py3_libdir}/distutils/sysconfig.py')
from distutils.sysconfig import *
# Overwrite methods from sysconfig
if "mingw32" in os.getenv("CC"):
    get_python_inc = lambda plat_specific=0, prefix=None: "%{mingw64_py3_incdir}"
    get_python_lib = lambda plat_specific=0, standard_lib=0, prefix=None: "%{mingw64_python3_sitearch}"
else:
    get_python_inc = lambda plat_specific=0, prefix=None: "%{_includedir}/python%{py_ver}"
    get_python_lib = lambda plat_specific=0, standard_lib=0, prefix=None: "%{_libdir}/python%{py_ver}/site-packages"
EOF

# Install macros
install -Dpm 0644 %{SOURCE1} %{buildroot}%{_rpmconfigdir}/macros.d/macros.mingw32-python3
install -Dpm 0644 %{SOURCE2} %{buildroot}%{_rpmconfigdir}/macros.d/macros.mingw64-python3
sed -i 's|@PY_VER@|%{py_ver}|g; s|@PY_VER_NODOTS@|%{py_ver_nodots}|g' \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.mingw32-python3 \
  %{buildroot}%{_rpmconfigdir}/macros.d/macros.mingw64-python3

# Install dependency generators
install -Dpm 0644 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/fileattrs/mingw32_python3.attr
install -Dpm 0644 %{SOURCE4} %{buildroot}%{_rpmconfigdir}/fileattrs/mingw64_python3.attr

# Wrappers
mkdir -p %{buildroot}%{_bindir}
ln -s %{_libexecdir}/mingw-scripts %{buildroot}%{_bindir}/mingw32-python3
ln -s %{_libexecdir}/mingw-scripts %{buildroot}%{_bindir}/mingw64-python3

mkdir -p %{buildroot}%{_prefix}/%{mingw32_target}/bin
cat > %{buildroot}%{_prefix}/%{mingw32_target}/bin/python3 <<EOF
#!/bin/sh
%{_bindir}/mingw32-python3 "\$@"
EOF
chmod +x %{buildroot}%{_prefix}/%{mingw32_target}/bin/python3

mkdir -p %{buildroot}%{_prefix}/%{mingw64_target}/bin
cat > %{buildroot}%{_prefix}/%{mingw64_target}/bin/python3 <<EOF
#!/bin/sh
%{_bindir}/mingw64-python3 "\$@"
EOF
chmod +x %{buildroot}%{_prefix}/%{mingw64_target}/bin/python3

# TODO: These cause unsatisfyable requires on msvcr71.dll
rm -f %{buildroot}%{mingw32_py3_libdir}/distutils/command/wininst-7.1.exe
rm -f %{buildroot}%{mingw64_py3_libdir}/distutils/command/wininst-7.1.exe

# Drop unversioned 2to3
rm %{buildroot}%{mingw32_bindir}/2to3
rm %{buildroot}%{mingw64_bindir}/2to3

# Drop pip stuff installed to native dirs
rm -f %{buildroot}%{_bindir}/pip*
rm -rf %{buildroot}%{_prefix}/lib/python%{py_ver}/site-packages/pip*

# Ensure config scripts are executable
chmod +x %{buildroot}%{mingw32_bindir}/python3-config
chmod +x %{buildroot}%{mingw64_bindir}/python3-config


%files -n mingw32-%{pkgname}
%license LICENSE
%{_bindir}/mingw32-python3
%{_rpmconfigdir}/macros.d/macros.mingw32-python3
%{_rpmconfigdir}/fileattrs/mingw32_python3.attr
%{_prefix}/%{mingw32_target}/bin/python3
%{mingw32_py3_hostlibdir}/
%{mingw32_bindir}/2to3-%{py_ver}
%{mingw32_bindir}/idle3*
%{mingw32_bindir}/pydoc3*
%{mingw32_bindir}/python3.exe
%{mingw32_bindir}/python3-config
%{mingw32_bindir}/python%{py_ver}.exe
%{mingw32_bindir}/python%{py_ver}-config
%{mingw32_bindir}/python3w.exe
%{mingw32_bindir}/libpython%{py_ver}.dll
%{mingw32_py3_incdir}/
%{mingw32_libdir}/libpython%{py_ver}.dll.a
%{mingw32_py3_libdir}/
%{mingw32_libdir}/pkgconfig/*.pc
# Part of mingw32-python3-tkinter
%exclude %{mingw32_py3_libdir}/tkinter/
%exclude %{mingw32_py3_libdir}/lib-dynload/_tkinter.cpython-%{py_ver_nodots}.dll
%exclude %{mingw32_py3_libdir}/turtle.py
%exclude %{mingw32_py3_libdir}/__pycache__/turtle*
%exclude %{mingw32_py3_libdir}/turtledemo
# Part of mingw32-python3-idle
%exclude %{mingw32_bindir}/idle3
%exclude %{mingw32_bindir}/idle%{py_ver}
%exclude %{mingw32_py3_libdir}/idlelib/
# Part of mingw32-python3-test
%exclude %{mingw32_py3_libdir}/ctypes/test/
%exclude %{mingw32_py3_libdir}/distutils/tests/
%exclude %{mingw32_py3_libdir}/lib2to3/tests/
%exclude %{mingw32_py3_libdir}/test/
%exclude %{mingw32_py3_libdir}/tkinter/test/
%exclude %{mingw32_py3_libdir}/unittest/test/
%exclude %{mingw32_py3_libdir}/lib-dynload/_ctypes_test.cpython-%{py_ver_nodots}.dll
%exclude %{mingw32_py3_libdir}/lib-dynload/_testbuffer.cpython-%{py_ver_nodots}.dll
%exclude %{mingw32_py3_libdir}/lib-dynload/_testcapi.cpython-%{py_ver_nodots}.dll
%exclude %{mingw32_py3_libdir}/lib-dynload/_testimportmultiple.cpython-%{py_ver_nodots}.dll
%exclude %{mingw32_py3_libdir}/lib-dynload/_testinternalcapi.cpython-%{py_ver_nodots}.dll
%exclude %{mingw32_py3_libdir}/lib-dynload/_testmultiphase.cpython-%{py_ver_nodots}.dll
%exclude %{mingw32_py3_libdir}/lib-dynload/_xxtestfuzz.cpython-%{py_ver_nodots}.dll

%files -n mingw32-%{pkgname}-test
%{mingw32_py3_libdir}/ctypes/test/
%{mingw32_py3_libdir}/distutils/tests/
%{mingw32_py3_libdir}/lib2to3/tests/
%{mingw32_py3_libdir}/test/
%{mingw32_py3_libdir}/tkinter/test/
%{mingw32_py3_libdir}/unittest/test/
%{mingw32_py3_libdir}/lib-dynload/_ctypes_test.cpython-%{py_ver_nodots}.dll
%{mingw32_py3_libdir}/lib-dynload/_testbuffer.cpython-%{py_ver_nodots}.dll
%{mingw32_py3_libdir}/lib-dynload/_testcapi.cpython-%{py_ver_nodots}.dll
%{mingw32_py3_libdir}/lib-dynload/_testimportmultiple.cpython-%{py_ver_nodots}.dll
%{mingw32_py3_libdir}/lib-dynload/_testinternalcapi.cpython-%{py_ver_nodots}.dll
%{mingw32_py3_libdir}/lib-dynload/_testmultiphase.cpython-%{py_ver_nodots}.dll
%{mingw32_py3_libdir}/lib-dynload/_xxtestfuzz.cpython-%{py_ver_nodots}.dll

%files -n mingw32-%{pkgname}-tkinter
%{mingw32_py3_libdir}/tkinter/
%exclude %{mingw32_py3_libdir}/tkinter/test/
%{mingw32_py3_libdir}/lib-dynload/_tkinter.cpython-%{py_ver_nodots}.dll
%{mingw32_py3_libdir}/turtle.py
%{mingw32_py3_libdir}/__pycache__/turtle*
%{mingw32_py3_libdir}/turtledemo

%files -n mingw32-%{pkgname}-idle
%{mingw32_bindir}/idle3
%{mingw32_bindir}/idle%{py_ver}
%{mingw32_py3_libdir}/idlelib/

%files -n mingw64-%{pkgname}
%license LICENSE
%{_bindir}/mingw64-python3
%{_rpmconfigdir}/macros.d/macros.mingw64-python3
%{_rpmconfigdir}/fileattrs/mingw64_python3.attr
%{_prefix}/%{mingw64_target}/bin/python3
%{mingw64_py3_hostlibdir}/
%{mingw64_bindir}/2to3-%{py_ver}
%{mingw64_bindir}/idle3*
%{mingw64_bindir}/pydoc3*
%{mingw64_bindir}/python3.exe
%{mingw64_bindir}/python3-config
%{mingw64_bindir}/python%{py_ver}.exe
%{mingw64_bindir}/python%{py_ver}-config
%{mingw64_bindir}/python3w.exe
%{mingw64_bindir}/libpython%{py_ver}.dll
%{mingw64_py3_incdir}/
%{mingw64_libdir}/libpython%{py_ver}.dll.a
%{mingw64_py3_libdir}/
%{mingw64_libdir}/pkgconfig/*.pc
# Part of mingw64-python3-tkinter
%exclude %{mingw64_py3_libdir}/tkinter/
%exclude %{mingw64_py3_libdir}/lib-dynload/_tkinter.cpython-%{py_ver_nodots}.dll
%exclude %{mingw64_py3_libdir}/turtle.py
%exclude %{mingw64_py3_libdir}/__pycache__/turtle*
%exclude %{mingw64_py3_libdir}/turtledemo
# Part of mingw64-python3-idle
%exclude %{mingw64_bindir}/idle3
%exclude %{mingw64_bindir}/idle%{py_ver}
%exclude %{mingw64_py3_libdir}/idlelib/
# Part of mingw64-python3-test
%exclude %{mingw64_py3_libdir}/ctypes/test/
%exclude %{mingw64_py3_libdir}/distutils/tests/
%exclude %{mingw64_py3_libdir}/lib2to3/tests/
%exclude %{mingw64_py3_libdir}/test/
%exclude %{mingw64_py3_libdir}/tkinter/test/
%exclude %{mingw64_py3_libdir}/unittest/test/
%exclude %{mingw64_py3_libdir}/lib-dynload/_ctypes_test.cpython-%{py_ver_nodots}.dll
%exclude %{mingw64_py3_libdir}/lib-dynload/_testbuffer.cpython-%{py_ver_nodots}.dll
%exclude %{mingw64_py3_libdir}/lib-dynload/_testcapi.cpython-%{py_ver_nodots}.dll
%exclude %{mingw64_py3_libdir}/lib-dynload/_testimportmultiple.cpython-%{py_ver_nodots}.dll
%exclude %{mingw64_py3_libdir}/lib-dynload/_testinternalcapi.cpython-%{py_ver_nodots}.dll
%exclude %{mingw64_py3_libdir}/lib-dynload/_testmultiphase.cpython-%{py_ver_nodots}.dll
%exclude %{mingw64_py3_libdir}/lib-dynload/_xxtestfuzz.cpython-%{py_ver_nodots}.dll

%files -n mingw64-%{pkgname}-test
%{mingw64_py3_libdir}/ctypes/test/
%{mingw64_py3_libdir}/distutils/tests/
%{mingw64_py3_libdir}/lib2to3/tests/
%{mingw64_py3_libdir}/test/
%{mingw64_py3_libdir}/tkinter/test/
%{mingw64_py3_libdir}/unittest/test/
%{mingw64_py3_libdir}/lib-dynload/_ctypes_test.cpython-%{py_ver_nodots}.dll
%{mingw64_py3_libdir}/lib-dynload/_testbuffer.cpython-%{py_ver_nodots}.dll
%{mingw64_py3_libdir}/lib-dynload/_testcapi.cpython-%{py_ver_nodots}.dll
%{mingw64_py3_libdir}/lib-dynload/_testimportmultiple.cpython-%{py_ver_nodots}.dll
%{mingw64_py3_libdir}/lib-dynload/_testinternalcapi.cpython-%{py_ver_nodots}.dll
%{mingw64_py3_libdir}/lib-dynload/_testmultiphase.cpython-%{py_ver_nodots}.dll
%{mingw64_py3_libdir}/lib-dynload/_xxtestfuzz.cpython-%{py_ver_nodots}.dll

%files -n mingw64-%{pkgname}-tkinter
%{mingw64_py3_libdir}/tkinter/
%exclude %{mingw64_py3_libdir}/tkinter/test/
%{mingw64_py3_libdir}/lib-dynload/_tkinter.cpython-%{py_ver_nodots}.dll
%{mingw64_py3_libdir}/turtle.py
%{mingw64_py3_libdir}/__pycache__/turtle*
%{mingw64_py3_libdir}/turtledemo

%files -n mingw64-%{pkgname}-idle
%{mingw64_bindir}/idle3
%{mingw64_bindir}/idle%{py_ver}
%{mingw64_py3_libdir}/idlelib/


%changelog
* Mon Feb 09 2026 Sandro Mani <manisandro@gmail.com> - 3.11.14-7
- Backport fixes for CVE-2025-11468, CVE-2026-0672, CVE-2026-0865,
  CVE-2025-15282, CVE-2026-1299

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.14-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 Sandro Mani <manisandro@gmail.com> - 3.11.14-5
- Backport proposed fix for CVE-2025-13836

* Sun Dec 14 2025 Sandro Mani <manisandro@gmail.com> - 3.11.14-4
- Backport patch for CVE-2025-12084

* Sun Nov 23 2025 Sandro Mani <manisandro@gmail.com> - 3.11.14-3
- Backport fix for CVE-2025-6075

* Sun Oct 12 2025 Sandro Mani <manisandro@gmail.com> - 3.11.14-2
- Rebuild (tcl9)

* Thu Oct 09 2025 Sandro Mani <manisandro@gmail.com> - 3.11.14-1
- Update to 3.11.14

* Sun Aug 03 2025 Sandro Mani <manisandro@gmail.com> - 3.11.13-4
- Backport upstream fix for CVE-2025-8194

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Sandro Mani <manisandro@gmail.com> - 3.11.13-2
- Backport fix for CVE-2025-6069

* Sat Jun 14 2025 Sandro Mani <manisandro@gmail.com> - 3.11.13-1
- Update to 3.11.13

* Wed Apr 16 2025 Sandro Mani <manisandro@gmail.com> - 3.11.12-1
- Update to 3.11.12

* Fri Apr 04 2025 Sandro Mani <manisandro@gmail.com> - 3.11.11-5
- Add host bindir to PATH when invoking mingwXX_python3_host

* Fri Apr 04 2025 Sandro Mani <manisandro@gmail.com> - 3.11.11-4
- Add mingw-python3_pkgconfig.patch

* Sun Mar 23 2025 Sandro Mani <manisandro@gmail.com> - 3.11.11-3
- Ensure LIBPYTHON is set

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 04 2024 Sandro Mani <manisandro@gmail.com> - 3.11.11-1
- Update to 3.11.11

* Mon Nov 18 2024 Sandro Mani <manisandro@gmail.com> - 3.11.10-2
- Backport fix for CVE-2024-9287

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 3.11.10-1
- Update to 3.11.10

* Wed Aug 28 2024 Sandro Mani <manisandro@gmail.com> - 3.11.9-2
- Backport patch for CVE-2024-8088

* Mon Aug 26 2024 Sandro Mani <manisandro@gmail.com> - 3.11.9-1
- Update to 3.11.9

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 03 2024 Sandro Mani <manisandro@gmail.com> - 3.11.8-2
- Backport patch for CVE-2024-4032

* Fri Feb 16 2024 Sandro Mani <manisandro@gmail.com> - 3.11.8-1
- Update to 3.11.8
- Backport patch for CVE-2023-27043

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 08 2023 Sandro Mani <manisandro@gmail.com> - 3.11.6-1
- Update to 3.11.6

* Thu Aug 31 2023 Sandro Mani <manisandro@gmail.com> - 3.11.5-1
- Update to 3.11.5

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Sandro Mani <manisandro@gmail.com> - 3.11.4-1
- Update to 3.11.4

* Fri Apr 07 2023 Sandro Mani <manisandro@gmail.com> - 3.11.3-1
- Update to 3.11.3

* Sun Feb 12 2023 Sandro Mani <manisandro@gmail.com> - 3.11.2-1
- Update to 3.11.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Dec 08 2022 Sandro Mani <manisandro@gmail.com> - 3.11.1-2
- Fix broken select and socket modules

* Thu Dec 08 2022 Sandro Mani <manisandro@gmail.com> - 3.11.1-1
- Update to 3.11.1

* Mon Nov 21 2022 Sandro Mani <manisandro@gmail.com> - 3.11.0-4
- Backport patch for CVE-2022-45061

* Tue Nov 01 2022 Sandro Mani <manisandro@gmail.com> - 3.11.0-3
- Enable socket and mmap modules, enable missing pieces of os and ctypes modules

* Mon Oct 31 2022 Sandro Mani <manisandro@gmail.com> - 3.11.0-2
- Fix %%mingw_python3_host macros

* Tue Oct 25 2022 Sandro Mani <manisandro@gmail.com> - 3.11.0-1
- Update to 3.11.0

* Fri Oct 21 2022 Sandro Mani <manisandro@gmail.com> - 3.11.0-0.1.rc2
- Update to 3.11.0-rc2

* Thu Oct 20 2022 Sandro Mani <manisandro@gmail.com> - 3.10.7-3
- Add %%mingw{32,64}_python3_hostsitearch

* Tue Sep 13 2022 Sandro Mani <manisandro@gmail.com> - 3.10.7-2
- Fix lib-dynload path computation in mingw-python3 macros

* Tue Sep 13 2022 Sandro Mani <manisandro@gmail.com> - 3.10.7-1
- Update to 3.10.7

* Thu Aug 04 2022 Sandro Mani <manisandro@gmail.com> - 3.10.6-1
- Update to 3.10.6

* Wed Aug 03 2022 Sandro Mani <manisandro@gmail.com> - 3.10.5-3
- Add host build macros

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 11 2022 Sandro Mani <manisandro@gmail.com> - 3.10.5-1
- Update to 3.10.5

* Mon Mar 28 2022 Sandro Mani <manisandro@gmail.com> - 3.10.4-1
- Update to 3.10.4

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.10.3-2
- Rebuild with mingw-gcc-12

* Sun Mar 20 2022 Sandro Mani <manisandro@gmail.com> - 3.10.3-1
- Update to 3.10.3

* Mon Feb 28 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-14
- Re-add wrapper scripts under mingw host bin dir

* Sun Feb 27 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-13
- Require python%%{py_ver} rather than python(abi) = %%{py_ver}

* Wed Feb 23 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-12
- Rework macros

* Thu Feb 17 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-11
- Rebuild (openssl)

* Fri Feb 11 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-10
- Override runtime_library_dir_option in distutils Mingw32Compiler to prevent
  unsupported -Wl,--enable-new-dtags getting added to ldflags

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-9
- Rebuild for new python dependency generator (take two)

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-8
- Bump release

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-7
- Add missing dependency generator namespace for provides

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-6
- Rebuild for new python dependency generator

* Thu Feb 10 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-5
- Install dependency generators

* Sat Jan 22 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-4
- Also set CFLAGS/CXX/CXXFLAGS/LDFLAGS in mingw-python wrappers

* Fri Jan 21 2022 Tom Stellard <tstellar@redhat.com> - 3.10.2-3
- Build fix for https://fedoraproject.org/wiki/Changes/SetBuildFlagsBuildCheck

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Sandro Mani <manisandro@gmail.com> - 3.10.2-1
- Update to 3.10.2

* Sun Dec 12 2021 Sandro Mani <manisandro@gmail.com> - 3.10.1-1
- Update to 3.10.1

* Tue Oct 05 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-1
- Update to 3.10.0

* Tue Sep 14 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.9.rc2
- Update to 3.10.0-rc2

* Wed Aug 04 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.8.rc1
- Update to 3.10.0-rc1

* Fri Jul 30 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.7.b4
- Rebuild (libffi)

* Sat Jul 24 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.6.b4
- Drop _WIN32_WINNT define, mingw-9.0 defaults to _WIN32_WINNT=0xA00

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.10.0-0.5.b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 12 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.4.b4
- Update to 3.10.0-b4

* Thu Jun 24 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.3.b3
- Fix _POSIX_BUILD use before declaration in sysconfig

* Tue Jun 22 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.2.b3
- Update to 3.10.0-b3

* Thu Jun 10 2021 Sandro Mani <manisandro@gmail.com> - 3.10.0-0.1.b2
- Update to 3.10.0-b2

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.9.5-2
- Rebuilt for Python 3.10

* Wed May 05 2021 Sandro Mani <manisandro@gmail.com> - 3.9.5-1
- Update to 3.9.5

* Tue Apr 06 2021 Sandro Mani <manisandro@gmail.com> - 3.9.4-1
- Update to 3.9.4

* Sun Apr 04 2021 Sandro Mani <manisandro@gmail.com> - 3.9.3-1
- Update to 3.9.3

* Sat Feb 27 2021 Sandro Mani <manisandro@gmail.com> - 3.9.2-2
- Pass --enable-loadable-sqlite-extensions

* Mon Feb 22 2021 Sandro Mani <manisandro@gmail.com> - 3.9.2-1
- Update to 3.9.2

* Mon Feb 15 2021 Sandro Mani <manisandro@gmail.com> - 3.9.1-4
- MACHDEP=win32

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Sandro Mani <manisandro@gmail.com> - 3.9.1-2
- Backport fix for CVE-2021-3177

* Thu Dec 10 2020 Sandro Mani <manisandro@gmail.com> - 3.9.1-1
- Update to 3.9.1

* Sun Nov 08 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-4
- More mingw32,64_py3_build,install macro fixes

* Sun Nov 08 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-3
- Fix mingw32,64_py3_build macros

* Fri Nov 06 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-2
- Add %%mingw{32,64}_py3_{build,install} macros

* Tue Oct 06 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-1
- Update to 3.9.0

* Fri Sep 18 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.12-rc2
- Update to 3.9.0-rc2

* Wed Aug 12 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.11.rc1
- Update to 3.9.0-rc1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.0-0.10.b5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.9.b5
- Update to 3.9.0-beta5

* Tue Jul 14 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.8.b4
- Backport patch for CVE-2019-20907

* Sun Jul 12 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.7.b4
- Update to 3.9.0-beta4

* Wed Jun 24 2020 Robert-André Mauchin <zebob.m@gmail.com> - 3.9.0-0.6.b3
- Add mingw32/64_python3_version_nodots

* Thu Jun 11 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.5.b3
- Update to 3.9.0-beta3
- Set PYTHONPLATLIBDIR=lib

* Sat May 30 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.2.b1
- Add mingw-python3_platlibdir.patch

* Thu May 28 2020 Sandro Mani <manisandro@gmail.com> - 3.9.0-0.1.b1
- Update to 3.9.0-beta1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.3-2
- Rebuilt for Python 3.9

* Sun May 17 2020 Sandro Mani <manisandro@gmail.com> - 3.8.3-1
- Update to 3.8.3

* Mon Mar 02 2020 Sandro Mani <manisandro@gmail.com> - 3.8.2-1
- Update to 3.8.2

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 20 2019 Sandro Mani <manisandro@gmail.com> - 3.8.1-1
- Update to 3.8.1

* Wed Dec 04 2019 Sandro Mani <manisandro@gmail.com> - 3.8.0-2
- Exclude debug files

* Thu Oct 17 2019 Sandro Mani <manisandro@gmail.com> - 3.8.0-1
- Update to 3.8.0

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 3.8.0-0.5.rc1
- Rebuild (Changes/Mingw32GccDwarf2)

* Fri Oct 04 2019 Sandro Mani <manisandro@gmail.com> - 3.8.0-0.4.rc1
- Update to 3.8.0-rc1

* Fri Sep 27 2019 Sandro Mani <manisandro@gmail.com> - 3.8.0-0.3.b4
- Remove gettext dependency
- Remove dlfcn dependency
- Update mingw-python3_adapt-cygwinccompiler.patch to ensure native gcc is not invoked

* Fri Sep 27 2019 Sandro Mani <manisandro@gmail.com> - 3.8.0-0.2.b4
- Adapt host wrappers
- Don't strip extensions

* Thu Sep 26 2019 Sandro Mani <manisandro@gmail.com> - 3.8.0-0.1.b4
- Update to 3.8.0b4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 09 2019 Sandro Mani <manisandro@gmail.com> - 3.7.4-1
- Update to 3.7.4

* Wed May 01 2019 Sandro Mani <manisandro@gmail.com> - 3.7.3-3
- %%define -> %%global

* Wed Apr 24 2019 Sandro Mani <manisandro@gmail.com> - 3.7.3-2
- Set _PYTHON_SYSCONFIGDATA_NAME in host wrapper

* Tue Apr 23 2019 Sandro Mani <manisandro@gmail.com> - 3.7.3-1
- Initial package
