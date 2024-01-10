%define sourcever 3390200
Summary:        A portable, high level programming interface to various calling conventions
Name:           sqlite
Version:        3.39.2
Release:        3%{?dist}
License:        Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/GeneralLibraries
URL:            https://www.sqlite.org
Source0:        https://www.sqlite.org/2022/%{name}-autoconf-%{sourcever}.tar.gz
# CVE-2015-3717 applies to versions shipped in iOS and OS X
Patch0:         CVE-2015-3717.nopatch
Patch1:         CVE-2022-46908.patch
Patch2:         CVE-2023-7104.patch
Requires:       sqlite-libs = %{version}-%{release}
Provides:       sqlite3

%description
This package contains most of the static files that comprise the
www.sqlite.org website including all of the SQL Syntax and the
C/C++ interface specs and other miscellaneous documentation.

%package devel
Summary:        sqlite3 link library & header files
Group:          Development/Libraries
# Requires:       %{name} = %{version}-%{release}
%description    devel
The sqlite devel package include the needed library link and
header files for development.

%package libs
Summary:        sqlite3 library
Group:          Libraries

%description libs
The sqlite3 library.

%prep
%autosetup -p1 -n %{name}-autoconf-%{sourcever}

%build
%configure \
    CFLAGS="%{optflags}"                \
    CXXFLAGS="%{optflags}               \
    -DSQLITE_ENABLE_FTS3=1              \
    -DSQLITE_ENABLE_COLUMN_METADATA=1   \
    -DSQLITE_ENABLE_UNLOCK_NOTIFY=1     \
    -DSQLITE_SECURE_DELETE=1"           \
    --disable-static
make

%install
[ %{buildroot} != "/"] && rm -rf %{buildroot}/*
make DESTDIR=%{buildroot} install
install -D -m644 sqlite3.1 %{buildroot}/%{_mandir}/man1/sqlite3.1
find %{buildroot} -type f -name "*.la" -delete -print
rm -rf %{buildroot}/%{_infodir}
%{_fixperms} %{buildroot}/*

%check
make %{?_smp_mflags} check

%postun devel -p /sbin/ldconfig
%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license tea/license.terms
%{_bindir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/libsqlite3.so
%{_libdir}/libsqlite3.so.0
%{_libdir}/pkgconfig/*
%{_includedir}/*

%files libs
%defattr(-,root,root)
%{_libdir}/libsqlite3.so.0.8.6

%changelog
* Tue Jan 09 2023 Henry Li <lihl@microsoft.com> - 3.39.2-3
- Address CVE-2023-7104

* Tue Dec 13 2022 Daniel McIlvaney <damcilva@microsoft.com> - 3.39.2-2
- Address CVE-2022-46908

* Tue Aug 16 2022 Muhammad Falak <mwani@microsoft.com> - 3.39.2-1
- Bump version to address CVE-2022-35737

* Wed Apr 20 2022 Chris Co <chrco@microsoft.com> - 3.36.0-3
- Address CVE-2021-36690

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 3.36.0-2
- Remove manual pkgconfig(*) provides in toolchain specs

* Wed Jan 26 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 3.36.0-1
- Update to version 3.36.0.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.34.1-2
- Removing the explicit %%clean stage.
- License verified.

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 3.34.1-1
- Update to 3.34.1 to fix CVE-2021-20227
- Remove Obsoletes tags

* Thu Oct 22 2020 Ruying Chen <v-ruyche@microsoft.com> - 3.32.3-2
- Nopatch CVE-2015-3717. Applies to versions shipped in iOS and OS X.

* Tue Jul 07 2020 Joe Schmitt <joschmit@microsoft.com> - 3.32.3-1
- Update to version 3.32.3 to fix CVE-2020-15358.
- Update URL to use https.

* Thu May 28 2020 Andrew Phelps <anphel@microsoft.com> - 3.32.1-1
- Update to version 3.32.1 to fix CVEs.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.26.0-5
- Added %%license line automatically

* Tue Apr 21 2020 Nicolas Ontiveros <niontive@microsoft.com> - 3.26.0-4
- Fix CVE-2019-8457.
- Remove sha1 macro.

* Wed Jan 22 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.26.0-3
- Adding 'ldconfig' call in 'sqlite-devel' %postun.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.26.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Feb 3 2019 Michelle Wang <michellew@vmware.com> - 3.26.0-1
- Upgrade to 3.26.0 for a critical Vulnerability named 'Magallan'.

* Fri Sep 21 2018 Srinidhi Rao <srinidhir@vmware.com> - 3.25.1-1
- Upgrade to version 3.25.1

* Tue Feb 20 2018 Xiaolin Li <xiaolinl@vmware.com> - 3.22.0-1
- Upgrade to version 3.22.0

* Fri Nov 10 2017 Xiaolin Li <xiaolinl@vmware.com> - 3.21.0-1
- Upgrade to version 3.21.0

* Fri Jul 14 2017 Dheeraj Shetty <dheerajs@vmware.com> - 3.19.3-1
- Upgrading to version 3.19.0 and adding patch for CVE-2017-10989

* Thu Jun 29 2017 Divya Thaluru <dthaluru@vmware.com> - 3.18.0-2
- Added obseletes for deprecated sqlite-autoconf package

* Fri Apr 7 2017 Alexey Makhalov <amakhalov@vmware.com> - 3.18.0-1
- Version update
- Package rename: sqlite-autoconf -> sqlite

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> - 3.11.0-4
- Added -devel and -libs subpackages

* Tue Oct 04 2016 ChangLee <changlee@vmware.com> - 3.11.0-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.11.0-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.11.0-1
- Updated to version 3.11.0

* Wed Feb 03 2016 Anish Swaminathan <anishs@vmware.com> - 3.8.3.1-2
- Fix versioning

* Tue Oct 7 2014 Divya Thaluru <dthaluru@vmware.com> - 3080301-1
- Initial build. First version
