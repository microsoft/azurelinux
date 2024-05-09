Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           ykclient
Version:        2.15
Release:        11%{?dist}
Summary:        Yubikey management library and client

License:        BSD
URL:            https://opensource.yubico.com/yubico-c-client/
Source0:	https://opensource.yubico.com/yubico-c-client/releases/ykclient-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  curl-devel, chrpath, help2man

%description
commandline for yubikeys

%package devel

Summary:  Development headers and libraries for ykclient
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
development files for ykclient  needed to build applications to
take advantage of yubikey authentication.

%prep
%setup -q

%build
%configure --enable-static=no
%make_build

%install
%make_install
rm $RPM_BUILD_ROOT%{_libdir}/libykclient.la
chrpath -d $RPM_BUILD_ROOT%{_bindir}/ykclient

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS NEWS README
%{_bindir}/ykclient
%{_libdir}/libykclient.so.3*
%{_mandir}/man1/ykclient.1.gz

%files devel
%{_includedir}/*.h
%{_libdir}/libykclient.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.15-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Aug 1 2019 Orion Poplawski <orion@nwra.com> - 2.15-9
- Modernize spec

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 03 2016 Nick Bebout <nb@fedoraproject.org> - 2.15-1
- Update to 2.15

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Nick Bebout <nb@fedoraproject.org> - 2.14-1
- Update to 2.14

* Wed Nov 26 2014 Nick Bebout <nb@fedoraproject.org> - 2.13-1
- Update to 2.13

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 13 2014 Nick Bebout <nb@fedoraproject.org> - 2.12-1
- Update to 2.12

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb 8 2012 Nick Bebout <nb@fedoraproject.org> - 2.7-1
- Update to 2.7

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 07 2011 Dennis Gilmore <dennis@ausil.us> - 2.6-1
- update to 2.6 release.
- include all .h  header files

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Dennis Gilmore <dennis@ausil.us> - 2.3-1
- update to 2.3 release

* Wed Apr 29 2009 Dennis Gilmore <dennis@ausil.us> - 2.2-1
- initial packaging
