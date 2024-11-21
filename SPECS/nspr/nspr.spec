Summary:        Platform-neutral API
Name:           nspr
Version:        4.35
Release:        2%{?dist}
License:        MPLv2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://firefox-source-docs.mozilla.org/nspr
Source0:	https://ftp.mozilla.org/pub/nspr/releases/v%{version}/src/nspr-%{version}.tar.gz
BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers
BuildRequires:  make

%description
Netscape Portable Runtime (NSPR) provides a platform-neutral API
for system level and libc like functions.

%package        devel
Summary:        Header and development files for nspr
Requires:       %{name} = %{version}-%{release}

%description    devel
It contains the libraries and header files to create applications

%prep
%autosetup
cd nspr
sed -ri 's#^(RELEASE_BINS =).*#\1#' pr/src/misc/Makefile.in
sed -i 's#$(LIBRARY) ##' config/rules.mk

%build
cd nspr
%configure \
    --disable-debug \
    --enable-optimize \
    --with-pthreads \
    --enable-64bit \
    --disable-silent-rules

%make_build

%install
cd nspr
%make_install

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license nspr/LICENSE
%{_bindir}/*
%{_libdir}/*.so

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_datarootdir}/aclocal/*

%changelog
* Wed Feb 07 2024 Dan Streetman <ddstreet@ieee.org> - 4.35-2
- add build deps

* Tue Feb 06 2024 Kanika nema <kanikanema@microsoft.com> - 4.35-1
- Upgrade to release version 4.35
- Added disable-debug and enable-optimize config options as suggested
  by the official NSPR page

* Tue Jan 23 2024 Archana Choudhary <archana1@microsoft.com> - 4.9.6-1
- Upgrade to 4.9.6

* Tue Jun 14 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.30-2
- Add explicit build requirements
- Lint spec

* Wed Feb 23 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 4.30-1
- Upgrading to v4.30 for nss

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 4.21-2
- Added %%license line automatically

* Tue Mar 17 2020 Andrew Phelps <anphel@microsoft.com> - 4.21-1
- Update version to 4.21. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 4.20-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 4.20-1
- Upgrade to 4.20.

* Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 4.15-1
- Upgrade to 4.15.

* Fri May 05 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.14-2
- Fix error - binary packed in devel.

* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.14-1
- Update to 4.14

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 4.12-3
- Added -devel subpackage

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 4.12-2
- GA - Bump release of all rpms

* Thu Feb 25 2016 Kumar Kaushik <kaushikk@vmware.com> - 4.12-1
- Updated to version 4.12

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> - 4.11-1
- Updated to version 4.11

* Fri May 29 2015 Alexey Makhalov <amakhalov@vmware.com> - 4.10.8-1
- Version update. Firefox requirement.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 4.10.3-1
- Initial build. First version
