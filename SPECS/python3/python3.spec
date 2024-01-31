%global openssl_flags -DOPENSSL_NO_SSL3 -DOPENSSL_NO_SSL2 -DOPENSSL_NO_COMP
%global __brp_python_bytecompile %{nil}
# Automating the extraction of these alternate version strings has proven to be tricky,
# with regards to tooling available in the toolchain build environment.
# These will be manually maintained for the time being.
%global majmin 3.12
%global majmin_nodots 312
# See Lib/ensurepip/__init__.py in Source0 for these version numbers
%global pip_version 23.2.1
%global setuptools_version 67.6.1

Summary:        A high-level scripting language
Name:           python3
Version:        3.12.0
Release:        1%{?dist}
License:        PSF
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Programming
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Patch0:         cgi3.patch
Patch1:         CVE-2015-20107.patch
# Backport https://github.com/python/cpython/commit/069fefdaf42490f1e00243614fb5f3d5d2614b81 from 3.10 to 3.9
Patch2:         0001-gh-95231-Disable-md5-crypt-modules-if-FIPS-is-enable.patch
Patch3:         CVE-2022-37454.patch
Patch4:         CVE-2022-45061.patch
Patch5:         CVE-2022-42919.patch
Patch6:         CVE-2023-24329.patch
# Patch for setuptools, resolved in 65.5.1
Patch1000:      CVE-2022-40897.patch

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
Provides:       python
Provides:       python-sqlite
Provides:       python(abi)
Provides:       %{_bindir}/python
Provides:       /bin/python
Provides:       /bin/python3
Provides:       %{name}-docs = %{version}-%{release}
Provides:       python%{majmin} = %{version}-%{release}
Provides:       python%{majmin_nodots} = %{version}-%{release}
%if %{with_check}
BuildRequires:  iana-etc
BuildRequires:  tzdata
%endif

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package        libs
Summary:        The libraries for python runtime
Group:          Applications/System
Requires:       bzip2-libs
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:       sqlite-libs
# python3-xml was provided as a separate package in Mariner 1.0
# We fold this into the libs subpackage in Mariner 2.0
Provides:       %{name}-xml = %{version}-%{release}
Provides:       python%{majmin}-libs = %{version}-%{release}
Provides:       python%{majmin_nodots}-libs = %{version}-%{release}

%description    libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for python 3 applications.

%package        curses
Summary:        Python module interface for NCurses Library
Group:          Applications/System
Requires:       ncurses
Requires:       %{name}-libs = %{version}-%{release}
Provides:       python%{majmin}-curses = %{version}-%{release}
Provides:       python%{majmin_nodots}-curses = %{version}-%{release}

%description    curses
The python3-curses package provides interface for ncurses library.

%package        devel
Summary:        The libraries and header files needed for Python development.
Group:          Development/Libraries
Requires:       expat-devel >= 2.1.0
Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-setuptools = %{version}-%{release}
Provides:       python%{majmin}-devel = %{version}-%{release}
Provides:       python%{majmin_nodots}-devel = %{version}-%{release}

%description    devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package        tools
Summary:        A collection of development tools included with Python.
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Provides:       python%{majmin}-tools = %{version}-%{release}
Provides:       python%{majmin_nodots}-tools = %{version}-%{release}

%description    tools
The Python package includes several development tools that are used
to build python programs.

%package        pip
Summary:        The PyPA recommended tool for installing Python packages.
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Provides:       python3dist(pip) = %{version}-%{release}
Provides:       python%{majmin}dist(pip) = %{version}-%{release}
BuildArch:      noarch

%description    pip
The PyPA recommended tool for installing Python packages.

%package        setuptools
Summary:        Download, build, install, upgrade, and uninstall Python packages.
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Provides:       python3dist(setuptools) = %{version}-%{release}
Provides:       python%{majmin}dist(setuptools) = %{version}-%{release}
BuildArch:      noarch

%description    setuptools
setuptools is a collection of enhancements to the Python distutils that allow you to more easily build and distribute Python packages, especially ones that have dependencies on other packages.

%package        test
Summary:        Regression tests package for Python.
Group:          Development/Tools
Requires:       %{name} = %{version}-%{release}
Provides:       python%{majmin}-test = %{version}-%{release}
Provides:       python%{majmin_nodots}-test = %{version}-%{release}

%description test
The test package contains all regression tests for Python as well as the modules test.support and test.regrtest. test.support is used to enhance your tests while test.regrtest drives the testing suite.

%prep
# We need to patch setuptools later, so manually manage patches with -N
%autosetup -p1 -n Python-%{version} -N

# Ideally we would use '%%autopatch -p1 -M 999', but unfortunately the GitHub CI pipelines use a very old version of rpm which doesn't support it.
# We use the CI to validate the toolchain manifests, which means we need to parse this .spec file
#%%patch0 -p1
#%%patch1 -p1
#%%patch2 -p1
#%%patch3 -p1
#%%patch4 -p1
#%%patch5 -p1
#%%patch6 -p1

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

# Bootstrap `pip3` which casues ptest build failure.
# The manual installation of pip in the RPM buildroot requires pip
# to be already present in the chroot.
# For toolchain builds, `pip3` requirement is staisfied by raw-toolchain's
# version of python, so it does not do anything.
# For builds other than toolchain, we would require pip to be present.
# The line below install pip in the build chroot using the recently
# compiled python3.
# NOTE: This is a NO-OP for the toolchain build.
python3 Lib/ensurepip

# Installing pip/setuptools via ensurepip fails in our toolchain.
# The versions of these tools from the raw toolchain are detected,
# and install fails. We will install these two bundled wheels manually.
# https://github.com/pypa/pip/issues/3063
# https://bugs.python.org/issue31916
pip3 install --no-cache-dir --no-index --ignore-installed \
    --root %{buildroot} \
    ./Lib/test/setuptools-%{setuptools_version}-py3-none-any.whl \
    ./Lib/ensurepip/_bundled/pip-%{pip_version}-py3-none-any.whl

# Manually patch CVE-2022-40897 which is a bundled wheel. We can only update the source code after install
#echo 'Patching CVE-2022-40897 in bundled wheel file %{_libdir}/python%{majmin}/site-packages/setuptools/package_index.py'
#patch %{buildroot}%{_libdir}/python%{majmin}/site-packages/setuptools/package_index.py < %{PATCH1000}

# Windows executables get installed by pip and setuptools- we don't need these.
find %{buildroot}%{_libdir}/python%{majmin}/site-packages -name '*.exe' -delete -print

# Install pathfix.py to bindir
#cp -p Tools/scripts/pathfix.py %{buildroot}%{_bindir}/pathfix%{majmin}.py
#ln -s ./pathfix%{majmin}.py %{buildroot}%{_bindir}/pathfix.py

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
rm %{buildroot}%{_bindir}/2to3
rm -rf %{buildroot}%{_bindir}/__pycache__

# %check
# make  %{?_smp_mflags} test

%ldconfig_scriptlets

%files
%defattr(-, root, root)
%license LICENSE
%doc README.rst
%{_bindir}/pydoc*
%{_bindir}/python3
%{_bindir}/python%{majmin}
%{_mandir}/*/*

%dir %{_libdir}/python%{majmin}
%dir %{_libdir}/python%{majmin}/site-packages

%exclude %{_libdir}/python%{majmin}/test/test_ctypes
%exclude %{_libdir}/python%{majmin}/test/test_sqlite3
%exclude %{_libdir}/python%{majmin}/idlelib/idle_test
%exclude %{_libdir}/python%{majmin}/test
%exclude %{_libdir}/python%{majmin}/lib-dynload/_ctypes_test.*.so

%exclude %{_libdir}/python3.9

%files libs
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_libdir}/libpython3.so
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
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/pkgconfig/%{name}-embed.pc
%{_libdir}/libpython%{majmin}.so
%{_bindir}/python3-config
%{_bindir}/python%{majmin}-config
%doc Misc/README.valgrind Misc/valgrind-python.supp
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
%doc Tools/README
%{_libdir}/python%{majmin}/lib2to3
%{_bindir}/2to3-%{majmin}
%exclude %{_bindir}/idle*

%files pip
%defattr(-,root,root,755)
%{_bindir}/pip*

%files setuptools
%defattr(-,root,root,755)

%files test
%{_libdir}/python%{majmin}/test/*

%changelog
* Tue Jan 30 2024 Andrew Phelps <anphel@microsoft.com> - 3.12.0-1
- Upgrade to version 3.12.0

* Wed Oct 11 2023 Amrita Kohli <amritakohli@microsoft.com> - 3.9.14-8
- Patch for CVE-2023-24329

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.9.14-7
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 02 2023 Daniel McIlvaney <damcilva@microsoft.com> - 3.9.14-6
- Patch CVE-2022-40897 in the bundled setuptools wheel

* Wed Dec 07 2022 Henry Beberman <henry.beberman@microsoft.com> - 3.9.14-5
- Add CVE-2022-42919 patch from upstream.

* Tue Dec 06 2022 Henry Beberman <henry.beberman@microsoft.com> - 3.9.14-4
- Add CVE-2022-45061 patch from upstream.

* Mon Dec 05 2022 Henry Beberman <henry.beberman@microsoft.com> - 3.9.14-3
- Add CVE-2022-37454 patch from upstream.
- Vulnerability not currently exposed because we use openssl sha3 implementation, but patching built-in sha3 regardless.

* Fri Oct 07 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.9.14-2
- Backport patch which allows cloud-init (among other programs) to use `import crypt` sucessfully when in FIPS mode

* Wed Sep 07 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.9.14-1
- Update to 3.9.14 to resolve security issues including CVE-2020-10735

* Wed Aug 31 2022 Henry Beberman <henry.beberman@microsoft.com> - 3.9.13-5
- Add CVE-2021-28861 patch from upstream

* Tue Aug 30 2022 Henry Beberman <henry.beberman@microsoft.com> - 3.9.13-4
- Add CVE-2015-20107 patch from upstream

* Tue Jul 12 2022 Olivia Crain <oliviacrain> - 3.9.13-3
- Update cgi3 patch to use versioned python shebang

* Fri Jul 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.9.13-2
- Remove Windows executables from pip, setuptools subpackages
- Add provides in the style of python39-%%{subpackage}, python3.9-%%{subpackage} for all packages except pip, setuptools

* Mon Jun 20 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.9.13-1
- Upgrade to latest maintenance release for the 3.9 series

* Tue Apr 26 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.9.12-1
- Upgrade to latest maintenance release for the 3.9 series

* Tue Jan 25 2022 Thomas Crain <thcrain@microsoft.com> - 3.9.10-1
- Upgrade to latest bugfix release for the 3.9 series

* Mon Jan 10 2022 Muhammad Falak <mwani@microsoft.com> - 3.9.9-3
- Fix pip3 bootstrap which causes a build break in ptest

* Wed Dec 22 2021 Thomas Crain <thcrain@microsoft.com> - 3.9.9-2
- Use filtered flags when compiling extensions

* Mon Nov 29 2021 Thomas Crain <thcrain@microsoft.com> - 3.9.9-1
- Upgrade to latest release in 3.9 series
- Add profile guided optimization to configuration
- Fold xml subpackage into libs subpackage and add compatibility provides
- Align libpython*.so* file packaging with other distros
- Manually install pip/setuptools wheels
- Remove irrelevant patches
- License verified

* Fri May 07 2021 Daniel Burgener <daburgen@microsoft.com> 3.7.10-3
- Remove coreutils dependency to remove circular dependency with libselinux

* Wed Apr 28 2021 Andrew Phelps <anphel@microsoft.com> - 3.7.10-2
- Add patch to fix test_ssl tests.

* Tue Apr 27 2021 Thomas Crain <thcrain@microsoft.com> - 3.7.10-1
- Merge the following releases from 1.0 to dev branch
- thcrain@microsoft.com, 3.7.9-1: Update to 3.7.9, the latest security release for 3.7
- thcrain@microsoft.com, 3.7.9-2: Patch CVE-2020-27619
- pawelw@microsoft.com, 3.7.9-3: Adding explicit runtime dependency on 'python3-xml' for the 'python3-setuptool' subpackage.
- nisamson@microsoft.com, 3.7.9-4: Patched CVE-2021-3177 with backported patch. Moved to autosetup.
- thcrain@microsoft.com, 3.7.10-1: Update to 3.7.10, the latest security release for 3.7, to fix CVE-2021-23336
-   Remove backported patches for CVE-2020-27619, CVE-2021-3177
- anphel@microsoft.com, 3.7.10-2: Add patch to fix test_ssl tests

* Tue Apr 20 2021 Henry Li <lihl@microsoft.com> - 3.7.7-11
- Provides python from python3

* Tue Mar 09 2021 Henry Li <lihl@microsoft.com> - 3.7.7-10
- Remove 2to3 binaries from python3-devel

* Wed Mar 03 2021 Henry Li <lihl@microsoft.com> - 3.7.7-9
- Fix python3-devel file section to include 2to3-3.7 and 2to3
- Provides python3-docs

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 3.7.7-8
- Turn off byte compilation since it requires this package to already be built and present.

* Mon Jan 04 2021 Ruying Chen <v-ruyche@microsoft.com> - 3.7.7-7
- Add python3 dist provides.

* Fri Dec 11 2020 Joe Schmitt <joschmit@microsoft.com> - 3.7.7-6
- Ship pathfix.py.
- pathfix.py spec changes imported from Fedora 32 (license: MIT)
- Provide python3dist(setuptools).

* Thu Oct 15 2020 Joe Schmitt <joschmit@microsoft.com> 3.7.7-5
- Add OPENSSL_NO_COMP flag to configuration.

* Mon Sep 28 2020 Joe Schmitt <joschmit@microsoft.com> 3.7.7-4
- Comment out check section to avoid unmet dependencies.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> 3.7.7-3
- Add Requires for python3-xml and python3-setuptools in python3-devel.

* Mon Jul 06 2020 Henry Beberman <henry.beberman@microsoft.com> 3.7.7-2
- Add BuildRequires for iana-etc and tzdata for check section.

* Wed Jun 10 2020 Paul Monson <paulmon@microsoft.com> 3.7.7-1
- Update to Python 3.7.7 to fix CVEs

* Thu May 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 3.7.3-10
- Fix CVE-2019-16056.

* Wed May 20 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.7.3-9
- Fix CVE-2020-8492.

* Wed May 20 2020 Paul Monson <paulmon@microsoft.com> 3.7.3-8
- Fix variable use.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.7.3-7
- Added %%license line automatically

* Wed May 06 2020 Paul Monson <paulmon@microsoft.com> 3.7.3-6
- Replace unsupported TLS methods with a patch.

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.7.3-5
- Remove toybox and only use coreutils for requires.

* Mon Nov 25 2019 Andrew Phelps <anphel@microsoft.com> 3.7.3-4
- Remove duplicate libpython3.so from devel package

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.7.3-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jun 17 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-2
- Fix for CVE-2019-10160

* Mon Jun 10 2019 Tapas Kundu <tkundu@vmware.com> 3.7.3-1
- Update to Python 3.7.3 release

* Thu May 23 2019 Tapas Kundu <tkundu@vmware.com> 3.7.0-6
- Fix for CVE-2019-5010
- Fix for CVE-2019-9740

* Tue Mar 12 2019 Tapas Kundu <tkundu@vmware.com> 3.7.0-5
- Fix for CVE-2019-9636

* Mon Feb 11 2019 Taps Kundu <tkundu@vmware.com> 3.7.0-4
- Fix for CVE-2018-20406

* Fri Dec 21 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-3
- Fix for CVE-2018-14647

* Tue Dec 04 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-2
- Excluded windows installer from python3 libs packaging.

* Wed Sep 26 2018 Tapas Kundu <tkundu@vmware.com> 3.7.0-1
- Updated to version 3.7.0

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 3.6.1-9
- Requires coreutils or toybox
- Requires bzip2-libs

* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> 3.6.1-8
- Remove devpts mount in check

* Mon Aug 28 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-7
- Add pty for tests to pass

* Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-6
- Add python3-test package.

* Fri Jun 30 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.6.1-5
- Remove the imaplib tests.

* Mon Jun 05 2017 Xiaolin Li <xiaolinl@vmware.com> 3.6.1-4
- Added pip, setuptools, xml, and curses sub packages.

* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> 3.6.1-3
- Fix symlink and script

* Wed May 10 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.6.1-2
- Exclude idle3.

* Wed Apr 26 2017 Siju Maliakkal <smaliakkal@vmware.com> 3.6.1-1
- Updating to latest

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> 3.5.3-3
- Python3-devel requires expat-devel.

* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-2
- Provides /bin/python3.

* Tue Feb 28 2017 Xiaolin Li <xiaolinl@vmware.com> 3.5.3-1
- Updated to version 3.5.3.

* Fri Jan 20 2017 Dheeraj Shetty <dheerajs@vmware.com> 3.5.1-10
- Added patch to support Photon OS

* Tue Dec 20 2016 Xiaolin Li <xiaolinl@vmware.com> 3.5.1-9
- Move easy_install-3.5 to devel subpackage.

* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> 3.5.1-8
- Use sqlite-{devel,libs}

* Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-7
- Patch for CVE-2016-5636

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 3.5.1-6
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-5
- GA - Bump release of all rpms

* Wed May 04 2016 Anish Swaminathan <anishs@vmware.com> 3.5.1-4
- Edit scriptlets.

* Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.5.1-3
- update python to require python-libs

* Thu Apr 07 2016 Mahmoud Bassiouny <mbassiouny@vmware.com> 3.5.1-2
- Providing python3 binaries instead of the minor versions.

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.5.1-1
- Updated to version 3.5.1

* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> 3.4.3-3
- Edit post script.

* Mon Aug 17 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3-2
- Remove python.o file, and minor cleanups.

* Wed Jul 1 2015 Vinay Kulkarni <kulkarniv@vmware.com> 3.4.3
- Add Python3 package to Photon.
