Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           liboauth
Version:        1.0.3
Release:        15%{?dist}
Summary:        OAuth library functions

License:        MIT
URL:            https://liboauth.sourceforge.net/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
%if 0%{?el5}
%endif

BuildRequires:  gcc
BuildRequires:  curl-devel nss-devel
#Requires:       

%description
liboauth is a collection of POSIX-c functions implementing the OAuth
Core RFC 5849 standard. liboauth provides functions to escape and
encode parameters according to OAuth specification and offers
high-level functionality to sign requests or verify OAuth signatures
as well as perform HTTP requests.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
%if 0%{?el5}
Requires:       pkgconfig curl-devel nss-devel
%endif

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q


%build
%configure --disable-static --enable-nss
make %{?_smp_mflags}


%install
%if 0%{?el5}
rm -rf $RPM_BUILD_ROOT
%endif
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'



%ldconfig_scriptlets


%files
%doc AUTHORS COPYING.MIT README 
%{_libdir}/*.so.*

%files devel
%doc ChangeLog
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/oauth.pc
%{_mandir}/man3/oauth.*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Debarshi Ray <rishi@fedoraproject.org> - 1.0.3-11
- Update Source0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Michel Salim <salimma@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 15 2013 Michel Salim <salimma@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Sep  2 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.7-1
- Update to 0.9.7

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jan 31 2012 Michel Salim <salimma@fedoraproject.org> - 0.9.6-1
- Update to 0.9.6

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Mar 12 2011 Michel Salim <salimma@fedoraproject.org> - 0.9.4-1
- Update to 0.9.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.9.0-3.1
- Rebuilt for gcc bug 634757

* Fri Sep 17 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.0-2.1
- [EL5] development package explicitly requires pkgconfig, {curl,nss}-devel

* Fri Sep 10 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.0-2
- Move oauth.3 to devel subpackage

* Wed Sep  8 2010 Michel Salim <salimma@fedoraproject.org> - 0.9.0-1
- Initial package

