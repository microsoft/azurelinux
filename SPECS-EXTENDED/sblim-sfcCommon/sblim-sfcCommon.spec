Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		sblim-sfcCommon
Version:	1.0.1
Release:	16%{?dist}
Summary:	Common functions for SBLIM Small Footprint CIM Broker and CIM Client Library.

License:	EPL
URL:		https://sourceforge.net/projects/sblim/
Source0:	https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2

BuildRequires:	sblim-cmpi-devel
BuildRequires:	gcc gcc-c++

%description
This package provides a common library for functions
shared between Small Footprint CIM Broker (sblim-sfcb)
Small Footprint CIM Client (and sblim-sfcc).


%package	devel
Summary:	Sblim-sfcCommon Development Files
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description devel
Sblim-sfcCommon Development Files.


%prep
%setup -q


%build
%configure
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot}
# remove unused static libraries
rm -f %{buildroot}/%{_libdir}/libsfcUtil.a
rm -f %{buildroot}/%{_libdir}/libsfcUtil.la


%ldconfig_scriptlets


%files
%doc AUTHORS README COPYING NEWS ChangeLog
%{_libdir}/libsfcUtil.so.*


%files devel
%{_includedir}/sfcCommon
%{_libdir}/libsfcUtil.so



%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.1-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.0.1-11
- Add BuildRequires gcc and gcc-c++
- Remove Group tag

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.0.1-1
- Initial support
- Fix -devel requires
- Fix Summary and URL
