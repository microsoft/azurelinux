Name:           libmicrohttpd
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Version:        0.9.77
Release:        3%{?dist}
Summary:        Lightweight library for embedding a webserver in applications

# * COPYING says that some main sources are only under LGPL-2.1-or-later
#   and the rest is dual licensed under LGPL-2.1-or-later OR GPL-2.0-or-later WITH eCos-exception-2.0.
# * Some docs are under GFDL-1.3-no-invariants-or-later.
# * Tests and some parts of the build system are under other licenses but they are NOT shipped.
License:        LGPL-2.1-or-later AND (LGPL-2.1-or-later OR GPL-2.0-or-later WITH eCos-exception-2.0) AND GFDL-1.3-no-invariants-or-later

URL:            https://www.gnu.org/software/libmicrohttpd/
Source0:        https://ftp.gnu.org/gnu/libmicrohttpd/%{name}-%{version}.tar.gz
Patch0:         gnutls-utilize-system-crypto-policy.patch

BuildRequires:  libtool
BuildRequires:  texinfo
BuildRequires:  gnutls-devel
BuildRequires:  doxygen
# Needed only for doc/doxygen 'full' build including dependency graphs
#BuildRequires:  graphviz
BuildRequires:  make
Requires(post): info
Requires(preun): info

%description
GNU libmicrohttpd is a small C library that is supposed to make it
easy to run an HTTP server as part of another application.
Key features that distinguish libmicrohttpd from other projects are:

* C library: fast and small
* API is simple, expressive and fully reentrant
* Implementation is http 1.1 compliant
* HTTP server can listen on multiple ports
* Support for IPv6
* Support for incremental processing of POST data
* Creates binary of only 25k (for now)
* Three different threading models

%package devel
Summary:        Development files for libmicrohttpd
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for libmicrohttpd

%package doc
Summary:        Documentation for libmicrohttpd
Requires:       %{name} = %{version}-%{release}
BuildArch:      noarch

%description doc
Doxygen documentation for libmicrohttpd and some example source code

%prep
%autosetup -p1

%build
%configure --disable-static --with-gnutls --enable-https=yes
%make_build
# Using 'fast' to avoid BuildRequires on graphviz; when/if graphviz is available,
# this can be switched to 'full' to build dependency graphs
make -C doc/doxygen fast

%check
%make_build check

%install
%make_install

rm -f %{buildroot}%{_libdir}/*.la
rm -f %{buildroot}%{_infodir}/dir
rm -f %{buildroot}%{_bindir}/demo

# Install some examples in /usr/share/doc/libmicrohttpd-doc/examples
mkdir examples
install -m 644 src/examples/*.c examples
install -m 644 doc/examples/*.c examples

cp -R doc/doxygen/html html

%post doc
install-info %{_infodir}/libmicrohttpd.info.gz %{_infodir}/dir || :
install-info %{_infodir}/libmicrohttpd-tutorial.info.gz %{_infodir}/dir || :

%preun doc
if [ $1 = 0 ] ; then
install-info --delete %{_infodir}/libmicrohttpd.info.gz %{_infodir}/dir || :
install-info --delete %{_infodir}/libmicrohttpd-tutorial.info.gz %{_infodir}/dir || :
fi

%files
%doc README NEWS
%license COPYING
%{_libdir}/libmicrohttpd.so.*

%files devel
%{_includedir}/microhttpd.h
%{_libdir}/libmicrohttpd.so
%{_libdir}/pkgconfig/libmicrohttpd.pc

%files doc
%{_mandir}/man3/libmicrohttpd.3.gz
%{_infodir}/libmicrohttpd.info.*
%{_infodir}/libmicrohttpd-tutorial.info.*
%{_infodir}/libmicrohttpd_performance_data.png.gz
%doc AUTHORS README ChangeLog
%doc examples
%doc html

%changelog
* Thu Feb 01 2024 Dan Streetman <ddstreet@ieee.org> - 0.9.77-3
- Update to version from Fedora 39.
- Next line is present only to avoid tooling failures, and does not indicate the actual package license.
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- license verified
- drop epoch
- remove prefix from install-info calls
- change doc/doxygen build from 'full' to 'fast' to avoid (currently missing) graphviz build dep

* Mon Aug 07 2023 Lukáš Zaoral <lzaoral@redhat.com> - 1:0.9.77-2
- migrate to SPDX license format

* Fri Jul 28 2023 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.77-1
- Update to 1:0.9.77

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.76-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 28 2023 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.76-1
- Update to 1:0.9.76

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.75-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.75-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.75-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Dec 28 2021 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.75-2
- Cleanup specfile

* Mon Dec 27 2021 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.75-1
- Update to 1:0.9.75

* Mon Dec 20 2021 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.74-1
- Update to 1:0.9.74

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 26 2021 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.73-1
- Update to 1:0.9.73

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 29 2020 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.72-1
- Update to 1:0.9.72

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.71-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 29 2020 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.71-1
- Update to 1:0.9.71

* Sun Feb 09 2020 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.70-1
- Update to 1:0.9.70

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.69-1
- Update to 1:0.9.69

* Mon Oct 28 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.68-1
- Update to 1:0.9.68

* Fri Oct 18 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.67-1
- Update to 1:0.9.67

* Sat Aug 17 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.66-1
- Update to 1:0.9.66

* Fri Jul 05 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.65-1
- Update to 1:0.9.65

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 1:0.9.64-1
- Update to 1:0.9.64

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 1:0.9.63-2
- Remove hardcoded gzip suffix from GNU info pages

* Mon Feb 11 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.63-1
- Update to 1:0.9.63

* Thu Jan 24 2019 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.62-1
- Update to 1:0.9.62

* Fri Dec 07 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1:0.9.61-1
- Update to latest version
- Drop obsolete scriptlets

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.59-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Feb 02 2018 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.59-1
- Update to 0.9.59

* Fri Dec 08 2017 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.58-1
- Update to 0.9.58 (#1523429)
- Add BR graphviz

* Wed Dec 06 2017 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.57-2
- enable tests

* Mon Dec 04 2017 Martin Gansser <martinkg@fedoraproject.org> - 1:0.9.57-1
- Update to 0.9.57
- Dropped dependency on libgcrypt
- Dropped dependency on openssl
- Update tarball link to "https:"
- Add examples from doc/examples

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.55-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.9.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 29 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.55-1
- Add BR texinfo
- Update to 0.9.55 (#1456304)

* Wed May 03 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.54-1
- Update to 0.9.54 (#1447476)

* Sun Jan 29 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.53-1
- Update to 0.9.53 (#1288676)
- Adjust gnutls-utilize-system-crypto-policy.patch

* Sun Jan 29 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.52-3
- Enable HTTPS with --enable-https=yes
- Re-add gnutls-utilize-system-crypto-policy.patch
- Add epoch to allow update of higher release version

* Thu Jan 26 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.52-2
- Dropped gnutls-utilize-system-crypto-policy.patch

* Fri Jan 13 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.52-1
- Update to 0.9.52
- Dropped subpkg microspdy2http because it's dead
- Adjust gnutls-utilize-system-crypto-policy.patch
- Use %%make_build
- Use %%make_install
- Use %%license
- Cleanup Specfile
- Add BR gettext-devel

* Thu Jan 12 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.46-4
- roolback to release 0.9.46 again, because 0.9.52 does not work

* Wed Jan 11 2017 Martin Gansser <martinkg@fedoraproject.org> - 0.9.46-3
- Add epoch to allow update of higher release version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.9.46-1
- Update to 0.9.46 (#1279862)

* Sun Nov 01 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.9.45-1
- Update to 0.9.45 (#1276892)

* Fri Oct 02 2015 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.9.44-1
- Update to 0.9.44 (#1209288)

* Wed Sep 16 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 0.9.42-1
- Update to 0.9.42 (#1209288)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.39-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.39-2
- Utilize system crypto policy (#1179314)

* Mon Jan 05 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 0.9.39-1
- Update to latest upstream release 0.9.39 (#1094435)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.34-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Tim Niemueller <tim@niemueller.de> - 0.9.34-2
- Add missing BR openssl-devel (required for libmicrospdy)

* Thu Mar 13 2014 Tim Niemueller <tim@niemueller.de> - 0.9.34-1
- Update to latest uptsream release 0.9.34
- Create sub-packages for libmicrospdy which is now enabled by default

* Thu Jan 02 2014 Václav Pavlín <vpavlin@redhat.com> - 0.9.33-1
- Update to latest upstream release 0.9.33

* Wed Dec 04 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.32-1
- Update to latest upstream release 0.9.32

* Mon Oct 21 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.31-1
- Update to latest upstream release 0.9.31

* Tue Sep 10 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.30-1
- Update to latest upstream release 0.9.30

* Tue Aug 06 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.28-3
- Correct comments about the doc location (#993819)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 23 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.28-1
- Update to latest uptsream release 0.9.28

* Mon May 6 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.27-1
- Update to latest uptsream release 0.9.27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 8 2013 Václav Pavlín <vpavlin@redhat.com> - 0.9.24-1
- Update to latest uptsream release 0.9.24

* Thu Sep 27 2012 Tim Niemueller <tim@niemueller.de> - 0.9.22-1
- Update to latest uptsream release 0.9.22

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Feb 27 2011 Tim Niemueller <tim@niemueller.de> - 0.9.7-1
- Update to new upstream release 0.9.7
- Remove upstreamed patches

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 26 2011 Tim Niemueller <tim@niemueller.de> - 0.9.6-1
- Update to new upstream release 0.9.6

* Mon Jan 24 2011 Tim Niemueller <tim@niemueller.de> - 0.9.5-1
- Update to new upstream release 0.9.5

* Tue Nov 16 2010 Tim Niemueller <tim@niemueller.de> - 0.9.2-3
- Add missing BR gnutls-devel and libgcrypt-devel
- Added patch to fix test apps (NSS instead of GnuTLS/OpenSSL curl,
  implicit DSO linking)
- Disable test cases for now due to false errors, reported upstream

* Tue Nov 16 2010 Tim Niemueller <tim@niemueller.de> - 0.9.2-2
- Re-enable HTTPS, configure flags had unexpected result

* Sun Nov 7 2010 Tim Niemueller <tim@niemueller.de> - 0.9.2-1
- Update to 0.9.2

* Fri Jun 4 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.4.6-1
- Update to 0.4.6

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.4.2-1
- Update to version 0.4.2
- Drop upstreamed patch

* Fri Feb 27 2009 Erik van Pienbroek <info@nntpgrab.nl> - 0.4.0a-1
- Update to version 0.4.0a
- Drop upstreamed patch
- Added a new patch to fix a 64bit issue
- The -devel package now contains a pkgconfig file
- The configure script is now run with '--enable-messages --enable-https'
- Made the -doc subpackage noarch (F11+)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Erik van Pienbroek <info@nntpgrab.nl> - 0.4.0-1
- Update to version 0.4.0
- This version introduces a API bump (which is required for
  supporting large files on 32bit environments)
- The license issues we had with version 0.3.1 of this package (as
  discussed in #457924) are resolved in this version. The license
  of this package is now changed to LGPLv2+
- Added a patch to fix two testcases on 64bit environments (upstream bug #1454)

* Sat Sep 6 2008 Erik van Pienbroek <info@nntpgrab.nl> - 0.3.1-3
- Changed license to GPLv3+ and added some comments
  regarding the license issues with this package

* Sun Aug 10 2008 Erik van Pienbroek <info@nntpgrab.nl> - 0.3.1-2
- Changed license to LGPLv2+
- Moved the COPYING file to the main package

* Tue Aug 5 2008 Erik van Pienbroek <info@nntpgrab.nl> - 0.3.1-1
- Initial release
