%global openssl_flags -DOPENSSL_NO_SSL3 -DOPENSSL_NO_SSL2 -DOPENSSL_NO_COMP

Summary:        A high-level scripting language
Name:           python2
Version:        2.7.18
Release:        12%{?dist}
License:        PSF
URL:            http://www.python.org/
Group:          System Environment/Programming
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        http://www.python.org/ftp/python/%{version}/Python-%{version}.tar.xz
Patch0:         cgi.patch
Patch1:         added-pyopenssl-ipaddress-certificate-validation.patch
Patch2:         python2-support-mariner-platform.patch
Patch3:         Replace-unsupported-TLS-methods.patch
Patch4:         CVE-2019-20907.patch
Patch5:         CVE-2020-26116.patch
Patch6:         CVE-2017-18207.patch
# Ignore CVE-2015-5652 because it only applies to Windows
Patch7:         CVE-2015-5652.nopatch
# Ignore CVE-2017-17522 as Upstream, Red Hat, Debian, and Ubuntu all agree it is not exploitable
# and is not a security issue
Patch8:         CVE-2017-17522.nopatch
# Ignore CVE-2019-9674 since the community agreed it shouldn't be patched and upstream
# documentation is updated
Patch9:         CVE-2019-9674.nopatch
# Ignore CVE-2007-4559 since upstream community agreed it shouldn't be patched
Patch10:        CVE-2007-4559.nopatch
# Ignore CVE-2019-18348 since it is patched in Python 2.7
Patch11:        CVE-2019-18348.nopatch
# CVE-2020-27619 patch backported from 3.6
Patch12:        CVE-2020-27619.patch
# CVE-2021-23336 patch backported from 3.6 courtesy of Gentoo
# https://gitweb.gentoo.org/repo/gentoo.git/commit/?id=f2a53a94f3b6b6395ef4541051a02d80c61442d0
Patch13:        CVE-2021-23336.patch
# CVE-2022-0391 patch backported from 3.7 courtesy of openSUSE
# https://build.opensuse.org/package/view_file/openSUSE:Factory/python/CVE-2022-0391-urllib_parse-newline-parsing.patch?expand=1
Patch14:        CVE-2022-0391.patch
# CVE-2021-3733 patch backported from 3.11 courtesy of openSUSE
# https://build.opensuse.org/package/view_file/openSUSE:Factory/python/CVE-2021-3733-fix-ReDoS-in-request.patch?expand=1
Patch15:        CVE-2021-3733.patch
# CVE-2015-20107 patch backported from 3.10:
# https://github.com/python/cpython/commit/96739bccf220689a54ef33341f431eda19c287fa#diff-fddb3f7b76dfc3150d9c270d0adf6464078858e34d33614feff7b3edfaac162d
Patch16:        CVE-2015-20107.patch
# CVE-2023-24329 patch backported from 3.11:
# https://github.com/python/cpython/pull/99421
Patch17:        CVE-2023-24329.patch
BuildRequires:  pkg-config >= 0.28
BuildRequires:  bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:  expat-devel >= 2.1.0
BuildRequires:  libffi-devel >= 3.0.13
BuildRequires:  sqlite-devel
BuildRequires:  ncurses-devel
BuildRequires:  readline-devel
Requires:       openssl
Requires:       python2-libs = %{version}-%{release}
Provides:       python-sqlite = %{version}-%{release}
Provides:       python(abi) = %{version}-%{release}
Provides:       /bin/python2

%description
The Python 2 package contains the Python development environment. It
is useful for object-oriented programming, writing scripts,
prototyping large programs or developing entire applications. This
version is for backward compatibility with other dependent packages.

%package libs
Summary: The libraries for python runtime
Group: Applications/System
Requires:       sqlite-libs
Requires:       expat >= 2.1.0
Requires:       libffi >= 3.0.13
Requires:       ncurses
Requires:       gdbm
Requires:       bzip2-libs
%global __requires_exclude ^(/usr/bin/python|python\\(abi\\) = 2\\.7)$

# Needed for ctypes, to load libraries, worked around for Live CDs size
# Requires: binutils

%description libs
The python interpreter can be embedded into applications wanting to
use python as an embedded scripting language.  The python-libs package
provides the libraries needed for this.

%package -n python-xml
Summary: XML libraries for python runtime
Group: Applications/System
Requires: python2-libs = %{version}-%{release}

%description -n python-xml
The python-xml package provides the libraries needed for XML manipulation.

%package -n python-curses
Summary: Python module interface for NCurses Library
Group: Applications/System
Requires: python2-libs = %{version}-%{release}
Requires: ncurses

%description -n python-curses
The python-curses package provides interface for ncurses library.

%package devel
Summary: The libraries and header files needed for Python development.
Group: Development/Libraries
Requires: python2 = %{version}-%{release}
Requires: expat-devel >= 2.1.0
# Needed here because of the migration of Makefile from -devel to the main
# package
Conflicts: python2 < %{version}-%{release}

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

Install python-devel if you want to develop Python extensions.  The
python package will also need to be installed.  You'll probably also
want to install the python-docs package, which contains Python
documentation.

%package tools
Summary: A collection of development tools included with Python.
Group: Development/Tools
Requires: python2 = %{version}-%{release}

%description tools
The Python package includes several development tools that are used
to build python programs.

%package test
Summary: Regression tests package for Python.
Group: Development/Tools
Requires: python2 = %{version}-%{release}

%description test
The test package contains all regression tests for Python as well as the modules test.support and test.regrtest. test.support is used to enhance your tests while test.regrtest drives the testing suite.

%prep
%autosetup -p1 -n Python-%{version}

%build
export OPT="${CFLAGS} %{openssl_flags}"
%configure \
    CFLAGS="%{optflags} %{openssl_flags}" \
    CXXFLAGS="%{optflags} %{openssl_flags}" \
    --enable-shared \
    --with-ssl \
    --with-system-expat \
    --with-system-ffi \
    --enable-unicode=ucs4 \
    --with-dbmliborder=gdbm:ndbm
make %{?_smp_mflags}
%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
chmod -v 755 %{buildroot}%{_libdir}/libpython2.7.so.1.0
%{_fixperms} %{buildroot}/*

# Remove unused stuff
find $RPM_BUILD_ROOT/ -name "*~"|xargs rm -f
find $RPM_BUILD_ROOT/ -name ".cvsignore"|xargs rm -f
find . -name "*~"|xargs rm -f
find . -name ".cvsignore"|xargs rm -f
#zero length
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.7/site-packages/modulator/Templates/copyright
rm -f $RPM_BUILD_ROOT%{_libdir}/python2.7/LICENSE.txt

find %{buildroot}%{_libdir} -name '*.pyc' -delete
find %{buildroot}%{_libdir} -name '*.pyo' -delete

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%check
make test

%files
%defattr(-, root, root)
%license LICENSE
%doc LICENSE README
%{_bindir}/pydoc*
%{_bindir}/python*
%{_mandir}/*/*

%dir %{_libdir}/python2.7
%dir %{_libdir}/python2.7/site-packages

%exclude %{_libdir}/python2.7/bsddb/test
%exclude %{_libdir}/python2.7/ctypes/test
%exclude %{_libdir}/python2.7/distutils/tests
%exclude %{_libdir}/python2.7/email/test
%exclude %{_libdir}/python2.7/json/tests
%exclude %{_libdir}/python2.7/sqlite3/test
%exclude %{_libdir}/python2.7/idlelib/idle_test
%exclude %{_libdir}/python2.7/test
#%exclude %{_libdir}/python2.7/unittest
%exclude %{_libdir}/python2.7/lib-dynload/_ctypes_test.so


%files libs
%defattr(-,root,root)
%doc LICENSE README
/usr/lib/python2.7
%{_libdir}/libpython2.7.so.*
%exclude %{_libdir}/python2.7/bsddb/test
%exclude %{_libdir}/python2.7/ctypes/test
%exclude %{_libdir}/python2.7/distutils/tests
%exclude %{_libdir}/python2.7/distutils/command/wininst*exe
%exclude %{_libdir}/python2.7/email/test
%exclude %{_libdir}/python2.7/json/tests
%exclude %{_libdir}/python2.7/sqlite3/test
%exclude %{_libdir}/python2.7/idlelib/idle_test
%exclude %{_libdir}/python2.7/test
%exclude %{_libdir}/python2.7/lib-dynload/_ctypes_test.so
%exclude %{_libdir}/python2.7/config
%exclude %{_libdir}/python2.7/config/*
%exclude %{_libdir}/libpython2.7.so
%exclude %{_libdir}/python2.7/xml
%exclude %{_libdir}/python2.7/lib-dynload/pyexpat.so

%files -n python-xml
%{_libdir}/python2.7/xml
%{_libdir}/python2.7/lib-dynload/pyexpat.so

%files -n python-curses
%{_libdir}/python2.7/curses
%{_libdir}/python2.7/lib-dynload/_curses*.so

%files devel
%defattr(-,root,root)
/usr/include/*
%doc Misc/README.valgrind Misc/valgrind-python.supp Misc/gdbinit
%dir %{_libdir}/python2.7/config
%{_libdir}/python2.7/config/*
%exclude %{_libdir}/python2.7/config/python.o
%{_libdir}/libpython2.7.so
%{_libdir}/pkgconfig/python-2.7.pc
%{_libdir}/pkgconfig/python.pc
%{_libdir}/pkgconfig/python2.pc
%exclude %{_bindir}/smtpd*.py*
%exclude %{_bindir}/2to3*
%exclude %{_bindir}/idle*

%files tools
%defattr(-,root,root,755)
#%doc Tools/modulator/README.modulator
#%{_libdir}/python2.7/lib2to3
#%{_libdir}/python2.7/site-packages/modulator
%{_bindir}/2to3*
%exclude %{_bindir}/smtpd.py
%exclude %{_bindir}/idle*

%files test
%{_libdir}/python2.7/test/*

%changelog
* Wed Mar 01 2023 Mitch Zhu <mitchzhu@microsoft.com> - 2.7.18-12
- Patch CVE-2023-24329.

* Wed Oct 05 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.7.18-11
- Patch CVE-2015-20107.

* Fri Jul 15 2022 Mandeep Plaha <mandeepplaha@microsoft.com> - 2.7.18-10
- Patch CVE-2021-3733

* Fri Feb 18 2022 Cameron Baird <cameronbaird@microsoft.com> - 2.7.18-9
- Patch CVE-2022-0391

* Mon Oct 25 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 2.7.18-8
- Specify version and release number for "Provides: python(abi)" to avoid mixing with Python 3.
- Removing "Provides: /bin/python" as this is satisfied by Python 3.

* Tue Mar 23 2021 Daniel Burgener <daburgen@microsoft.com> 2.7.18-7
- Remove coreutils dependency to remove circular dependency with libselinux

* Mon Mar 01 2021 Thomas Crain <thcrain@microsoft.com> - 2.7.18-6
- Add backported patch for CVE-2021-23336

* Tue Nov 03 2020 Thomas Crain <thcrain@microsoft.com> - 2.7.18-5
- Patch CVE-2020-27619

* Thu Oct 22 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.7.18-4
- Use autosetup
- Remove CVE-2013-1753 no patch
- Ignore CVE-2019-9674
- Fix CVE-2019-20907
- Fix CVE-2020-26116
- Ignore CVE-2007-4559
- Fix CVE-2017-18207
- Ignore CVE-2019-18348

* Thu Sep 10 2020 Thomas Crain <thcrain@microsoft.com> - 2.7.18-3
- Ignore CVE-2017-17522 because it is widely agreed upon to not be a security vulnerability
- Ignore CVE-2013-1753 because NVD erroneously lists this version as being vulnerable

* Tue Jun 09 2020 Paul Monson <paulmon@microsoft.com> - 2.7.18-2
- Ignore CVE-2015-5652 because it only applies to Windows

* Thu May 21 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.7.18-1
- Upgrade to version 2.7.18, which fixes CVE-2020-8492.

* Tue May 19 2020 Paul Monson <paulmon@microsoft.com> - 2.7.15-12
- Fix TLS methods patch.

* Wed May 13 2020 Nick Samson <nisamson@microsoft.com> - 2.7.15-11
- Added %%license line automatically

* Mon May 11 2020 Paul Monson <paulmon@microsoft.com> - 2.7.15-10
- Replace unsupported TLS methods with a patch.

* Thu Apr 09 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.7.15-9
- Remove toybox and only use coreutils in requires.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.7.15-8
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed May 22 2019 Tapas Kundu <tkundu@vmware.com> - 2.7.15-7
- Patched reworked changes for CVE-2019-9948
- Patch for CVE-2019-9740
- Fix for CVE-2019-10160

* Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> - 2.7.15-6
- Fix for CVE-2019-9948

* Tue Mar 12 2019 Tapas Kundu <tkundu@vmware.com> - 2.7.15-5
- Added fix for CVE-2019-9636

* Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.7.15-4
- Mode libpython2.7.so to python2-libs
- Remove python2 dependency from python2-libs

* Fri Dec 21 2018 Tapas Kundu <tkundu@vmware.com> - 2.7.15-3
- Fix for CVE-2018-14647

* Mon Sep 17 2018 Dweep Advani <dadvani@vmware.com> - 2.7.15-2
- Remove vulnerable Windows installers from python-libs rpm

* Mon Aug 20 2018 Dweep Advani <dadvani@vmware.com> - 2.7.15-1
- Update to version 2.7.15

* Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.7.13-12
- Fix CVE-2017-1000030

* Mon Dec 04 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.7.13-11
- Fix CVE-2017-1000158

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.7.13-10
- Requires coreutils or toybox
- Requires bzip2-libs

* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> - 2.7.13-9
- Remove devpts mount in check

* Mon Aug 28 2017 Chang Lee <changlee@vmware.com> - 2.7.13-8
- Add %check with pty

* Wed Jul 12 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.7.13-7
- Add python2-test package.

* Sun Jun 04 2017 Bo Gan <ganb@vmware.com> - 2.7.13-6
- Fix dependency for libs

* Tue May 16 2017 Kumar Kaushik <kaushikk@vmware.com> - 2.7.13-5
- Fixing python issue 29188, backport random.c from 3.5 to 2.7.

* Fri Apr 28 2017 Harish Udaiya <hudaiyakumar@vmware.com> - 2.7.13-4
- Excluded unwanted binaries from python2-tools.

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.7.13-3
- Python2-devel requires expat-devel.

* Fri Mar 24 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.7.13-2
- Provides /bin/python2.

* Wed Mar 22 2017 Divya Thaluru <dthaluru@vmware.com> - 2.7.13-1
- Updated to version 2.7.13

* Fri Jan 20 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.7.11-11
- Added patch to support Photon OS

* Wed Nov 16 2016 Alexey Makhalov <ppadmavilasom@vmware.com> - 2.7.11-10
- Use sqlite-{devel,libs}

* Thu Oct 27 2016 Anish Swaminathan <anishs@vmware.com> - 2.7.11-9
- Patch for CVE-2016-5636

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> - 2.7.11-8
- Modified %check

* Wed Sep 14 2016 Divya Thaluru <dthaluru@vmware.com> - 2.7.11-7
- Improvised pyopenssl patch

* Wed Sep 7 2016 Divya Thaluru <dthaluru@vmware.com> - 2.7.11-6
- Added patch to python openssl to validate certificates by ipaddress

* Mon Jun 20 2016 Divya Thaluru <dthaluru@vmware.com> - 2.7.11-5
- Added stack-protector flag for ncurses module

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.7.11-4
- GA - Bump release of all rpms

* Tue Apr 26 2016 Nick Shi <nshi@vmware.com> - 2.7.11-3
- Adding readline module into python2-libs

* Wed Apr 13 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.7.11-2
- update python to require python-libs

* Thu Jan 28 2016 Anish Swaminathan <anishs@vmware.com> - 2.7.11-1
- Upgrade version

* Fri Jan 22 2016 Divya Thaluru <dthaluru@vmware.com> - 2.7.9-5
- Seperate python-curses package from python-libs package

* Thu Oct 29 2015 Mahmoud Bassiouny <mbassiouny@vmware.com> - 2.7.9-4
- Seperate python-xml package from python-libs package

* Fri Jun 19 2015 Alexey Makhalov <amakhalov@vmware.com> - 2.7.9-3
- Provide /bin/python

* Wed Jun 3 2015 Divya Thaluru <dthaluru@vmware.com> - 2.7.9-2
- Adding coreutils package to run time required package

* Mon Apr 6 2015 Divya Thaluru <dthaluru@vmware.com> - 2.7.9-1
- Initial build.  First version
