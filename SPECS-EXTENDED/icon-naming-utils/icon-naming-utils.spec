Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:		icon-naming-utils
Version:	0.8.90
Release:	23%{?dist}
Summary: 	A script to handle icon names in desktop icon themes

License:	GPLv2
BuildArch:	noarch
URL:		https://tango.freedesktop.org/Standard_Icon_Naming_Specification
Source0:	https://tango.freedesktop.org/releases/%{name}-%{version}.tar.bz2

BuildRequires:	perl-generators
BuildRequires:	perl(XML::Simple)
BuildRequires:	automake

Patch0:		icon-naming-utils-0.8.7-paths.patch

%description
A script for creating a symlink mapping for deprecated icon names to
the new Icon Naming Specification names, for desktop icon themes.

%prep
%setup -q
%patch 0 -p1 -b .paths


%build
# the paths patch patches Makefile.am
autoreconf
%configure
make %{?_smp_mflags}


%install
%{make_install}

# hmm, it installs an -uninstalled.pc file ...
rm -f $RPM_BUILD_ROOT%{_datadir}/pkgconfig/icon-naming-utils-uninstalled.pc


%files
%doc AUTHORS README
%license COPYING
%{_bindir}/icon-name-mapping
%{_datadir}/icon-naming-utils/
%{_datadir}/pkgconfig/icon-naming-utils.pc

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.90-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.90-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jul 13 2015 Leigh Scott <leigh123linux@googlemail.com> - 0.8.90-14
- spec file clean up

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.8.90-10
- Perl 5.18 rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 19 2012 Matthias Clasen <mclasen@redhat.com> - 0.8.90-8
- Fix spec file syntax (#878232)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 11 2009 Ville Skyttä <ville.skytta@iki.fi> - 0.8.90-4
- Use bzipped upstream tarball.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 22 2009 Matthias Clasen <mclasen@redhat.com> - 0.8.90-1
- Update to 0.8.90

* Wed Jan 14 2009 Parag <pnemade@redhat.com> - 0.8.7-2
- spec file cleanup as suggested in merge-review rh#225894

* Tue Jul 22 2008 Matthias Clasen <mclasen@redhat.com> - 0.8.7-1
- Update to 0.8.7

* Sun Nov 18 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.6-2
- Use a standard group to placate rpmlint

* Mon Sep 17 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.6-1
- Update to 0.8.6

* Tue Aug 14 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Mon Feb 26 2007 Matthias Clasen <mclasen@redhat.com> - 0.8.2-1
- Update to 0.8.2
- Small spec file cleanups

* Mon Aug 21 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.1-1.fc6
- Update to 0.8.1

* Thu Aug  3 2006 Matthias Clasen <mclasen@redhat.com> - 0.8.0-1.fc6
- Update to 0.8.0

* Wed Aug 02 2006 Warren Togami <wtogami@redhat.com> - 0.7.3-1
- add disttag

* Wed Jul 12 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.3-1
- Update to 0.7.3

* Thu Jun  8 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.2-2
- Rebuild

* Tue May  9 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.2-1
- Update to 0.7.2

* Tue Apr 25 2006 Matthias Clasen <mclasen@redhat.com> - 0.7.1-1
- Update to 0.7.1

* Mon Feb  6 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.7-1
- Update to 0.6.7

* Tue Jan 17 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.5-1
- Initial import
