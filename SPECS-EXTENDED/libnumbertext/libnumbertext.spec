Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:      libnumbertext
Version:   1.0.11
Release:   1%{?dist}
Summary:   Number to number name and money text conversion library

#The entire source code is dual license LGPLv3+ or BSD, except for
#the data files hr.sor, sr.sor and sh.sor which are tri license
#CC-BY-SA or LGPLv3+ or BSD
License:   ( LGPL-3.0-or-later OR BSD 3-Clause ) AND ( LGPL-3.0-or-later OR CC-BY-SA-3.0 )
URL:       https://github.com/Numbertext/libnumbertext
Source:    https://github.com/Numbertext/libnumbertext/releases/download/%{version}/libnumbertext-%{version}.tar.xz

BuildRequires: autoconf, automake, libtool, gcc-c++
BuildRequires: make

%description
Language-neutral NUMBERTEXT and MONEYTEXT functions for LibreOffice Calc

%package devel
Requires: libnumbertext = %{version}-%{release}
Summary: Files for developing with libnumbertext

%description devel
Includes and definitions for developing with libnumbertext

%prep
%autosetup -p1

%build
autoreconf -v --install --force
%configure --disable-silent-rules --disable-static --disable-werror --with-pic
%make_build

%check
make check

%install
rm -rf $RPM_BUILD_ROOT
%make_install
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

%ldconfig_scriptlets

%files
%doc AUTHORS ChangeLog NEWS THANKS
%license COPYING
%{_bindir}/spellout
%{_libdir}/*.so.*
%{_datadir}/libnumbertext

%files devel
%{_includedir}/libnumbertext
%{_libdir}/pkgconfig/libnumbertext.pc
%{_libdir}/*.so

%changelog
* Wed Nov 20 2024 Akarsh Chaudhary  <v-akarshc@microsoft.com> -1.0.11-1
- Upgrade to version 1.0.11
-License Verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.5-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 16 2018 Caolán McNamara <caolanm@redhat.com> - 1.0.5-1
- latest version

* Thu Aug 16 2018 Caolán McNamara <caolanm@redhat.com> - 1.0.3-1
- latest version

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 12 2018 Caolán McNamara <caolanm@redhat.com> - 1.0.2-3
- fix changelog order
- remove clean section
- set COPYING as license
- use LT_INIT

* Mon Jun 11 2018 Caolán McNamara <caolanm@redhat.com> - 1.0.2-2
- clarify extra license option of the sh/sr/hr data files

* Mon Jun 11 2018 Caolán McNamara <caolanm@redhat.com> - 1.0.2-1
- initial version
