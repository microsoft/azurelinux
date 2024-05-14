Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		sblim-indication_helper
Version:	0.5.0
Release:	4%{?dist}
Summary:	Toolkit for CMPI indication providers

License:	EPL-1.0
URL:		https://sourceforge.net/projects/sblim/
Source0:	https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
BuildRequires:	sblim-cmpi-devel 
BuildRequires:	gcc gcc-c++

%description
This package contains a developer library for helping out when writing
CMPI providers. This library polls the registered functions for data
and, if it changes, a CMPI indication is set with the values of the
indication class properties (also set by the developer).

%Package	devel
Summary:	Toolkit for CMPI indication providers (Development Files)
Requires:	%{name} = %{version}-%{release} sblim-cmpi-devel glibc-devel

%description devel
This package contain developer library for helping out when writing
CMPI providers. This library polls the registered functions for data
and if they change an CMPI indication is set with the values of the
indication class properties (also set by the developer).

This package holds the development files for sblim-indication_helper.

%prep
%setup -q

%build
%configure --disable-static --with-pic
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/libind_helper.la

%ldconfig_scriptlets

%files
%license COPYING
%doc README ChangeLog TODO
%{_libdir}/libind_helper.so.*

%files devel
%{_includedir}/sblim
%{_libdir}/libind_helper.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.5.0-1
- Update to latest upstream version
- Change license to Eclipse Public License 1.0
- Use %%license
- Fix URL

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.4.2-20
- Add BuildRequires gcc and gcc-c++
- Remove Group tag
- Minor spec fixes

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.4.2-9
- Fix mixed use of spaces and tabs in specfile

* Thu Sep 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 0.4.2-8
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec  7 2009 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.4.2-4
-  fixed the build failure because of missing definition of stderr

* Fri Jul 31 2009 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.4.2-3
- fixed the rpmlint message. Removed Requries for glibc-devel.

* Tue Jun 30 2009 Praveen K Paladugu <praveen_paladugu@dell.com> - 0.4.2-1
- Standardized the spec file and changed the build number to 1 

* Thu Oct 23 2008 Matt Domsch <Matt_Domsch@dell.com> - 0.4.2-134
- update for Fedora packaging guidelines

* Fri May 30 2008 npaxton@novell.com
- Change openwbem-devel dependency to sblim-cmpi-devel, to be
  cimom neutral

* Wed Feb 27 2008 crrodriguez@suse.de
- fix library-without-ldconfig* errors
- disable static libraries

* Wed Mar 01 2006 mrueckert@suse.de
- update to 0.4.2
  ind_helper.c, ind_helper.h:
  Bugs: 1203849 (side effect) made a lot of function arguments
  const in order to remove the cmpi-base warnings.
  added sblim-indication_helper-0.4.2_warnings.patch
  fixes a small warning regarding pointer size

* Wed Jan 25 2006 mls@suse.de
- created the package
