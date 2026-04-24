%global openssl_flags -DOPENSSL_NO_SSL3 -DOPENSSL_NO_SSL2 -DOPENSSL_NO_COMP
%global __brp_python_bytecompile %{nil}
%define majmin %(echo %{version} | cut -d. -f1-2)
%define majmin_nodots %(echo %{majmin} | tr -d .)

Summary:        A high-level scripting language (version 3.14)
Name:           python3.14
Version:        3.14.4
Release:        1%{?dist}
License:        PSF
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Programming
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
# pathfix.py was provided by the previous Python source bundle (Python-3.9.14.tar.xz)
# It has been removed in later source bundles, but as our packages still require it, we will still provide for now.
Source1:        https://github.com/python/cpython/blob/3.9/Tools/scripts/pathfix.py
Patch0:         CVE-2026-0672.patch
Patch1:         CVE-2026-0865.patch
Patch2:         CVE-2026-1299.patch
Patch3:         CVE-2026-4519.patch

BuildRequires:  bzip2-devel
BuildRequires:  expat-devel >= 2.1.0
BuildRequires:  libffi-devel >= 3.0.13
BuildRequires:  ncurses-devel
BuildRequires:  openssl-devel
BuildRequires:  pkg-config >= 0.28
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  xz-devel
Requires:       ncurses
Requires:       openssl
Requires:       %{name}-libs = %{version}-%{release}
Requires:       readline
Requires:       xz
# Only versioned provides. The unversioned "python", "python3", "/bin/python",
# "/bin/python3" names remain owned by the default "python3" package so that
# python3.14 installs strictly side-by-side.
Provides:       python(abi) = %{majmin}
Provides:       %{name}-docs = %{version}-%{release}
Provides:       python%{majmin_nodots} = %{version}-%{release}

%if 0%{?with_check}
BuildRequires:  iana-etc
BuildRequires:  tzdata
%endif

%description
Python 3.14 installed side-by-side with the system python3. The interpreter
is available as /usr/bin/python3.14 and the standard library lives under
/usr/lib/python3.14/. This package does not change the system default python3.

%package        libs
Summary:        The libraries for python 3.14 runtime
Group:          Applications/System
Requires:       bzip2-libs
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:       sqlite-libs
Provides:       %{name}-xml = %{version}-%{release}
Provides:       python%{majmin_nodots}-libs = %{version}-%{release}

%description    libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python3.14-libs package
provides the libraries needed for python 3.14 applications.

%package        curses
Summary:        Python 3.14 module interface for NCurses Library
Group:          Applications/System
Requires:       ncurses
Requires:       %{name}-libs = %{version}-%{release}
Provides:       python%{majmin_nodots}-curses = %{version}-%{release}

%description    curses
The python3.14-curses package provides interface for ncurses library.

%package        devel
Summary:        The libraries and header files needed for Python 3.14 development.
Group:          Development/Libraries
Requires:       expat-devel >= 2.1.0
Requires:       %{name} = %{version}-%{release}
Provides:       python%{majmin_nodots}-devel = %{version}-%{release}

%description    devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks against Python 3.14.

%package        test
Summary:        Regression tests package for Python 3.14.
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Provides:       python%{majmin_nodots}-test = %{version}-%{release}

%description test
The test package contains all regression tests for Python 3.14 as well as the
modules test.support and test.regrtest. test.support is used to enhance your
tests while test.regrtest drives the testing suite.

%prep
%autosetup -p1 -n Python-%{version}

%build
# Remove GCC specs and build environment linker scripts
# from the flags used when compiling outside of an RPM environment
# https://fedoraproject.org/wiki/Changes/Python_Extension_Flags
export CFLAGS="%{extension_cflags} %{openssl_flags}"
export CFLAGS_NODIST="%{build_cflags} %{openssl_flags}"
export CXXFLAGS="%{extension_cxxflags} %{openssl_flags}"
export LDFLAGS="%{extension_ldflags}"
export LDFLAGS_NODIST="%{build_ldflags}"
export OPT="%{extension_cflags} %{openssl_flags}"

%configure \
    --enable-shared \
    --with-platlibdir=%{_lib} \
    --with-system-expat \
    --with-system-ffi \
    --with-dbmliborder=gdbm:ndbm \
    --with-ensurepip=no \
    --enable-optimizations
%make_build

%install
%make_install
%{_fixperms} %{buildroot}/*

# Windows executables get installed by pip - we don't need these.
find %{buildroot}%{_libdir}/python%{majmin}/site-packages -name '*.exe' -delete -print

# Install pathfix.py to bindir under the versioned name only.
# The unversioned /usr/bin/pathfix.py is owned by the default python3 package.
cp -pv %{SOURCE1} %{buildroot}%{_bindir}/pathfix%{majmin}.py

# Remove unversioned filesystem entries that belong to the default python3
# (3.12) package. Python 3.14 installs strictly side-by-side under versioned
# paths, so these unversioned symlinks / stable-ABI files must not be shipped
# by this package.
rm -f %{buildroot}%{_bindir}/python3
rm -f %{buildroot}%{_bindir}/python3-config
rm -f %{buildroot}%{_bindir}/pydoc3
rm -f %{buildroot}%{_bindir}/idle3
rm -f %{buildroot}%{_libdir}/libpython3.so
rm -f %{buildroot}%{_libdir}/pkgconfig/python3.pc
rm -f %{buildroot}%{_libdir}/pkgconfig/python3-embed.pc
rm -f %{buildroot}%{_mandir}/man1/python3.1*

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
rm -rf %{buildroot}%{_bindir}/__pycache__

%check
# vsock_loopback module needed by `test_socket` is not loaded by default in AzureLinux.
%{buildroot}%{_bindir}/python%{majmin} -m test --exclude test_socket

%ldconfig_scriptlets

%files
%defattr(-, root, root)
%license LICENSE
%doc README.rst
%{_bindir}/pydoc%{majmin}
%{_bindir}/python%{majmin}
%{_mandir}/man1/python%{majmin}.1*

%dir %{_libdir}/python%{majmin}
%dir %{_libdir}/python%{majmin}/site-packages

%exclude %{_libdir}/python%{majmin}/test/test_ctypes
%exclude %{_libdir}/python%{majmin}/test/test_sqlite3
%exclude %{_libdir}/python%{majmin}/idlelib/idle_test
%exclude %{_libdir}/python%{majmin}/test
%exclude %{_libdir}/python%{majmin}/lib-dynload/_ctypes_test.*.so

%files libs
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_libdir}/libpython%{majmin}.so.1.0
%{_libdir}/python%{majmin}
%exclude %{_libdir}/python%{majmin}/site-packages/
%exclude %{_libdir}/python%{majmin}/test/test_ctypes
%exclude %{_libdir}/python%{majmin}/test/test_sqlite3
%exclude %{_libdir}/python%{majmin}/idlelib/idle_test
%exclude %{_libdir}/python%{majmin}/test
%exclude %{_libdir}/python%{majmin}/lib-dynload/_ctypes_test.*.so
%exclude %{_libdir}/python%{majmin}/curses
%exclude %{_libdir}/python%{majmin}/lib-dynload/_curses*.so

%files curses
%{_libdir}/python%{majmin}/curses/*
%{_libdir}/python%{majmin}/lib-dynload/_curses*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/python-%{majmin}.pc
%{_libdir}/pkgconfig/python-%{majmin}-embed.pc
%{_libdir}/libpython%{majmin}.so
%{_bindir}/python%{majmin}-config
%{_bindir}/pathfix%{majmin}.py
%doc Misc/README.valgrind Misc/valgrind-python.supp
%exclude %{_bindir}/idle*

%files test
%{_libdir}/python%{majmin}/test/*

%changelog
* Thu Apr 23 2026 Ihar Voitka <ihvoitka@microsoft.com> - 3.14.4-1
- Original version for Azure Linux.
- License verified.
- Side-by-side with the default python3 (3.12). Ships only versioned paths
  (/usr/bin/python3.14, /usr/lib/python3.14/, libpython3.14.so.1.0).
- Carries post-3.14.4 CVE patches CVE-2026-0672, CVE-2026-0865, CVE-2026-1299,
  CVE-2026-4519. All prior CVE-2025-* patches on python3-3.12 are upstream in
  3.14.4; cgi3.patch is dropped because the cgi module was removed in 3.13
  (PEP 594).
- Drops the lib2to3-based tools subpackage since lib2to3 and /usr/bin/2to3
  were removed in Python 3.13.
