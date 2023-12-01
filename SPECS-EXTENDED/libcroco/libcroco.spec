Summary:        A CSS2 parsing library
Name:           libcroco
Version:        0.6.13
Release:        6%{?dist}
License:        LGPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.gnome.org/Archive/libcroco
Source:         https://gitlab.gnome.org/Archive/libcroco/-/archive/%{version}/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.xz
BuildRequires:  gcc
BuildRequires:  glib2-devel
BuildRequires:  libxml2-devel
BuildRequires:  pkgconfig

%description
CSS2 parsing and manipulation library for GNOME

%package devel
Summary:        Libraries and include files for developing with libcroco
Requires:       %{name}%{_isa} = %{version}-%{release}

%description devel
This package provides the necessary development libraries and include
files to allow you to develop with libcroco.

%prep
%autosetup

%build
%configure --disable-static
make %{?_smp_mflags} CFLAGS="$CFLAGS -fno-strict-aliasing"

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%check
make check

%ldconfig_scriptlets

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%{_bindir}/csslint-0.6
%{_libdir}/*.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/libcroco-0.6
%{_bindir}/croco-0.6-config
%{_libdir}/pkgconfig/libcroco-0.6.pc
%{_datadir}/gtk-doc/html/libcroco

%changelog
* Wed Oct 19 2022 Muhammad Falak <mwani@microsoft.com> - 0.6.13-6
- Drop fedora specific patch

* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.6.13-5
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.13-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Apr 06 2019 Kalev Lember <klember@redhat.com> - 0.6.13-1
- Update to 0.6.13

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 06 2017 Kalev Lember <klember@redhat.com> - 0.6.12-1
- Update to 0.6.12

* Thu Feb 09 2017 Kalev Lember <klember@redhat.com> - 0.6.11-3
- Disable strict aliasing, since the code is not strict-aliasing-clean

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Kalev Lember <klember@redhat.com> - 0.6.11-1
- Update to 0.6.11

* Mon Dec 14 2015 Kalev Lember <klember@redhat.com> - 0.6.10-1
- Update to 0.6.10

* Sat Oct 31 2015 Kalev Lember <klember@redhat.com> - 0.6.9-1
- Update to 0.6.9
- Use make_install macro
- Mark COPYING and COPYING.LIB as %%license
- Tighten -devel subpackage deps

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.6.8-6
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.8-1
- Update to 0.6.8

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.7-1
- Update to 0.6.7

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 0.6.6-1
- Update to 0.6.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.5-1
- Update to 0.6.5
- Dropped unused configure options

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 0.6.4-1
- Update to 0.6.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.3-1
- Update to 0.6.3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Parag Nemade <paragn AT fedoraproject.org> 0.6.2-5
- Merge-review cleanup (#225994)

* Tue Dec  8 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.2-4
- Add source url

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Tue Apr  1 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.1-5
- Clean up dependencies

* Fri Feb  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.1-4
- Rebuild for gcc 4.3

* Wed Oct 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.1-3
- Rebuild
- Update license tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.1-2.1
- rebuild

* Tue May 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.1-2
- Make config script a pkg-config wrapper to fix multilib conflict

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.1-1
- Update to 0.6.1
- Drop upstreamed patches

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.0-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.6.0-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- link shared lib against -lglib-2.0 and -lxml2

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 0.6.0-5
- Rebuild with gcc4

* Wed Sep 22 2004 Matthias Clasen <mclasen@redhat.com> - 0.6.0-4
- Move croco-config to the devel package

* Mon Sep 20 2004 Matthias Clasen <mclasen@redhat.com> - 0.6-3
- Don't memset() stack variables

* Tue Aug 31 2004 Matthias Clasen <mclasen@redhat.com> - 0.6-2
- Add missing ldconfig calls (#131279)

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> - 0.6-1
- Update to 0.6

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 10 2004 Warren Togami <wtogami@redhat.com>
- BR and -devel req libgnomeui-devel

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jonathan Blandford <jrb@redhat.com> 0.4.0-1
- new version

* Wed Aug 13 2003 Jonathan Blandford <jrb@redhat.com> 0.3.0-1
- initial import into the tree.  Based on the spec file in the package
