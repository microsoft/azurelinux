%global openssl_flags -DOPENSSL_NO_SSL3 -DOPENSSL_NO_SSL2 -DOPENSSL_NO_COMP
%global __brp_python_bytecompile %{nil}
Summary:        A high-level scripting language
Name:           python3
Version:        3.7.11
Release:        1%{?dist}
License:        PSF
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Programming
URL:            https://www.python.org/
Source0:        https://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Patch0:         cgi3.patch
Patch1:         python3-support-mariner-platform.patch
Patch2:         Replace-unsupported-TLS-methods.patch
Patch3:         fix_broken_mariner_ssl_tests.patch
# Upstream patch to fix XML tests with expat >= 2.4.5
Patch5:         fix-xml-tests-expat.patch
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
Requires:       python3-libs = %{version}-%{release}
Requires:       readline
Requires:       xz
Provides:       python = %{version}-%{release}
Provides:       python-sqlite = %{version}-%{release}
Provides:       python(abi) = %{version}-%{release}
Provides:       %{_bindir}/python
Provides:       /bin/python
Provides:       /bin/python3
Provides:       %{name}-docs = %{version}-%{release}
Provides:       %{_bindir}/pathfix.py
%if %{with_check}
BuildRequires:  iana-etc
BuildRequires:  tzdata
%endif

%description
The Python 3 package contains a new version of Python development environment.
Python 3 brings more efficient ways of handling dictionaries, better unicode
strings support, easier and more intuitive syntax, and removes the deprecated
code. It is incompatible with Python 2.x releases.

%package libs
Summary:        The libraries for python runtime
Group:          Applications/System
Requires:       bzip2-libs
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:       sqlite-libs

%description    libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for python 3 applications.

%package        xml
Summary:        XML libraries for python3 runtime
Group:          Applications/System
Requires:       python3 = %{version}-%{release}
Requires:       python3-libs = %{version}-%{release}

%description    xml
The python3-xml package provides the libraries needed for XML manipulation.

%package        curses
Summary:        Python module interface for NCurses Library
Group:          Applications/System
Requires:       ncurses
Requires:       python3-libs = %{version}-%{release}

%description    curses
The python3-curses package provides interface for ncurses library.

%package        devel
Summary:        The libraries and header files needed for Python development.
Group:          Development/Libraries
Requires:       expat-devel >= 2.1.0
Requires:       python3 = %{version}-%{release}
Requires:       python3-setuptools = %{version}-%{release}
Requires:       python3-xml = %{version}-%{release}
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts:      python3 < %{version}-%{release}

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
Requires:       python3 = %{version}-%{release}

%description    tools
The Python package includes several development tools that are used
to build python programs.

%package        pip
Summary:        The PyPA recommended tool for installing Python packages.
Group:          Development/Tools
Requires:       python3 = %{version}-%{release}
Requires:       python3-xml = %{version}-%{release}
Provides:       python3dist(pip) = %{version}-%{release}
Provides:       python3.7dist(pip) = %{version}-%{release}
BuildArch:      noarch

%description    pip
The PyPA recommended tool for installing Python packages.

%package        setuptools
Summary:        Download, build, install, upgrade, and uninstall Python packages.
Group:          Development/Tools
Requires:       python3 = %{version}-%{release}
Requires:       python3-xml
Provides:       python3dist(setuptools) = %{version}-%{release}
Provides:       python3.7dist(setuptools) = %{version}-%{release}
BuildArch:      noarch

%description    setuptools
setuptools is a collection of enhancements to the Python distutils that allow you to more easily build and distribute Python packages, especially ones that have dependencies on other packages.

%package test
Summary:        Regression tests package for Python.
Group:          Development/Tools
Requires:       python3 = %{version}-%{release}

%description test
The test package contains all regression tests for Python as well as the modules test.support and test.regrtest. test.support is used to enhance your tests while test.regrtest drives the testing suite.

%prep
%autosetup -p1 -n Python-%{version}

%build
export OPT="%{optflags} %{openssl_flags}"
%configure \
    CFLAGS="%{optflags} %{openssl_flags}" \
    CXXFLAGS="%{optflags} %{openssl_flags}" \
    --enable-shared \
    --with-system-expat \
    --with-system-ffi \
    --with-dbmliborder=gdbm:ndbm \
    --with-ensurepip=yes
make %{?_smp_mflags}

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
chmod -v 755 %{buildroot}%{_libdir}/libpython3.7m.so.1.0
%{_fixperms} %{buildroot}/*
ln -sf libpython3.7m.so %{buildroot}%{_libdir}/libpython3.7.so

# Install pathfix.py to bindir
cp -p Tools/scripts/pathfix.py %{buildroot}%{_bindir}/pathfix3.7.py
ln -s ./pathfix3.7.py %{buildroot}%{_bindir}/pathfix.py

# Remove unused stuff
find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete
find %{buildroot}%{_libdir} -name '*.o' -delete
rm %{buildroot}%{_bindir}/2to3
rm -rf %{buildroot}%{_bindir}/__pycache__

%check
make  %{?_smp_mflags} test

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-, root, root)
%license LICENSE
%doc README.rst
%{_bindir}/pydoc*
%{_bindir}/pyvenv*
%{_bindir}/python3
%{_bindir}/python3.7
%{_bindir}/python3.7m
%{_mandir}/*/*

%dir %{_libdir}/python3.7
%dir %{_libdir}/python3.7/site-packages

%{_libdir}/libpython3.so
%{_libdir}/libpython3.7m.so.1.0

%exclude %{_libdir}/python3.7/ctypes/test
%exclude %{_libdir}/python3.7/distutils/tests
%exclude %{_libdir}/python3.7/sqlite3/test
%exclude %{_libdir}/python3.7/idlelib/idle_test
%exclude %{_libdir}/python3.7/test
%exclude %{_libdir}/python3.7/lib-dynload/_ctypes_test.*.so

%files libs
%defattr(-,root,root)
%license LICENSE
%doc README.rst
%{_libdir}/python3.7
%{_libdir}/python3.7/site-packages/easy_install.py
%{_libdir}/python3.7/site-packages/README.txt
%exclude %{_libdir}/python3.7/site-packages/
%exclude %{_libdir}/python3.7/ctypes/test
%exclude %{_libdir}/python3.7/distutils/tests
%exclude %{_libdir}/python3.7/sqlite3/test
%exclude %{_libdir}/python3.7/idlelib/idle_test
%exclude %{_libdir}/python3.7/test
%exclude %{_libdir}/python3.7/lib-dynload/_ctypes_test.*.so
%exclude %{_libdir}/python3.7/xml
%exclude %{_libdir}/python3.7/lib-dynload/pyexpat*.so
%exclude %{_libdir}/python3.7/curses
%exclude %{_libdir}/python3.7/lib-dynload/_curses*.so
%exclude %{_libdir}/python3.7/distutils/command/wininst-*.exe

%files xml
%{_libdir}/python3.7/xml/*
%{_libdir}/python3.7/lib-dynload/pyexpat*.so

%files curses
%{_libdir}/python3.7/curses/*
%{_libdir}/python3.7/lib-dynload/_curses*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/python-3.7.pc
%{_libdir}/pkgconfig/python-3.7m.pc
%{_libdir}/pkgconfig/python3.pc
%{_libdir}/libpython3.7.so
%{_libdir}/libpython3.7m.so
%{_bindir}/python3-config
%{_bindir}/python3.7-config
%{_bindir}/python3.7m-config
%{_bindir}/pathfix.py
%{_bindir}/pathfix3.7.py
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
%doc Tools/README
%{_libdir}/python3.7/lib2to3
%{_bindir}/2to3-3.7
%exclude %{_bindir}/idle*

%files pip
%defattr(-,root,root,755)
%{_libdir}/python3.7/site-packages/pip/*
%{_libdir}/python3.7/site-packages/pip-20.1.1.dist-info/*
%{_bindir}/pip*

%files setuptools
%defattr(-,root,root,755)
%{_libdir}/python3.7/site-packages/pkg_resources/*
%{_libdir}/python3.7/site-packages/setuptools/*
%{_libdir}/python3.7/site-packages/setuptools-47.1.0.dist-info/*
%{_bindir}/easy_install-3.7

%files test
%{_libdir}/python3.7/test/*

%changelog
* Mon Mar 21 2022 Andrew Phelps <anphel@microsoft.com> - 3.7.11-1
- Upgrade to 3.7.11 to fix CVE-2021-3737

* Tue Mar 01 2022 Thomas Crain <thcrain@microsoft.com> - 3.7.10-7
- Add patch to fix tests with expat >= 2.4.5

* Fri Feb 18 2022 Cameron Baird <cameronbaird@microsoft.com> - 3.7.10-6
- Patch CVE-2022-0391

* Mon Aug 30 2021 Bala <balakumaran.kannan@microsoft.com> - 3.7.10-5
- Add explicit provides for pathfix.py
- Add version for provides

* Fri Aug 20 2021 Rachel Menge <rachelmenge@microsoft.com> 3.7.10-4
- Move libpython3.7.so to devel files to resolve broken symlink 

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
