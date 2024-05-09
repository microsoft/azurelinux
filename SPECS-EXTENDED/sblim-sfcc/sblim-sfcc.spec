Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# $Id: sblim-sfcc.spec,v 1.4 2010/03/03 07:57:28 vcrhonek Exp $
#
# Package spec for sblim-sfcc
#

Summary: Small Footprint CIM Client Library
Name: sblim-sfcc
Version: 2.2.8
Release: 15%{?dist}
License: EPL-1.0
URL: https://www.sblim.org
Source0: https://downloads.sourceforge.net/project/sblim/%{name}/%{name}-%{version}.tar.bz2
# Patch0: fixes docdir name and removes install of COPYING with license
#   which is included through %%license
Patch0: sblim-sfcc-2.2.8-docdir-license.patch
BuildRequires: curl-devel chrpath
BuildRequires: gcc gcc-c++

%Description
Small Footprint CIM Client Library Runtime Libraries

%package devel
Summary: Small Footprint CIM Client Library
Requires: %{name} = %{version}-%{release}

%Description devel
Small Footprint CIM Client Library Header Files and Link Libraries


%prep

%setup -q
%patch 0 -p1 -b .docdir-license

%build
chmod a-x backend/cimxml/*.[ch]

%configure
make %{?_smp_flags}

%install
make DESTDIR=%{buildroot} install
# remove unused libtool files
rm -rf %{buildroot}/%{_libdir}/*a
# remove rpath
chrpath --delete $RPM_BUILD_ROOT%{_libdir}/libcmpisfcc.so.1.0.0

%ldconfig_scriptlets


%files
%license COPYING
%{_libdir}/*.so.*
%{_libdir}/libcimcClientXML.so
%{_mandir}/man3/*.3.gz
%{_docdir}/*

%files devel
%{_includedir}/CimClientLib/*
%{_includedir}/cimc/*
%{_libdir}/libcimcclient.so
%{_libdir}/libcmpisfcc.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.8-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.8-11
- Use %%license for file which contains the text of the license
- Change versioned docdir to unversioned and rename the docdir to match
  the package name
- Fix license tag

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.8-9
- Add BuildRequires gcc and gcc-c++

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 31 2017 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.8-7
- Remove Group tag from spec file

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Dec 03 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.8-1
- Update to sblim-sfcc-2.2.8

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 31 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.7-1
- Update to sblim-sfcc-2.2.7

* Thu Jan 30 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.6-3
- Fix -devel requires

* Wed Jan 29 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.6-2
- Move libcimcClientXML.so from -devel to main package - it's needed for proper function

* Tue Oct 15 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.6-1
- Update to sblim-sfcc-2.2.6

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.5-3
- Remove rpath from libcmpisfcc library again

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 08 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.5-1
- Update to sblim-sfcc-2.2.5

* Mon Nov 19 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-4
- Remove rpath from libcmpisfcc library

* Thu Sep 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-3
- Fix issues found by fedora-review utility in the spec file

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.4-1
- Update to sblim-sfcc-2.2.4
- Fix source link, remove build root tag

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.3-1
- Update to sblim-sfcc-2.2.3

* Tue May 24 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.2-1
- Update to sblim-sfcc-2.2.2

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Mar  3 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.2.1-1
- Update to sblim-sfcc-2.2.1
- Fix Source field
- Move documentation files from -devel to main package

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild


* Tue Aug 19 2008  <srinivas_ramanatha@dell.com> - 2.1.0-0%{?dist}
- Modified the spec file to adhere to fedora packaging guidelines.

* Fri Feb 16 2007  <mihajlov@dyn-9-152-143-45.boeblingen.de.ibm.com> - 2.0.0-0
- Initial Version

