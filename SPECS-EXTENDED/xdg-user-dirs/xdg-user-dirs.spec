%global _changelog_trimtime %(date +%s -d "1 year ago")


Name:		xdg-user-dirs
Version:	0.17
Release:	6%{?dist}
Summary:	Handles user special directories

License:	GPLv2+ and MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:		http://freedesktop.org/wiki/Software/xdg-user-dirs
Source0:	http://user-dirs.freedesktop.org/releases/%{name}-%{version}.tar.gz

# use fuzzy translations (for Downloads)
# https://bugzilla.redhat.com/show_bug.cgi?id=532399
Patch0:		use-fuzzy.patch

BuildRequires:  gcc
BuildRequires:	gettext
BuildRequires:  docbook-style-xsl
BuildRequires:  libxslt
Requires:      %{_sysconfdir}/xdg/autostart

%description
Contains xdg-user-dirs-update that updates folders in a users
homedirectory based on the defaults configured by the administrator.

%prep
%setup -q
%patch0 -p1 -b .use-fuzzy

%build
%configure
%make_build

cd po
touch *.po
make update-gmo

%install
%make_install

%find_lang %name


%files -f %{name}.lang
%license COPYING
%doc NEWS AUTHORS README
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.conf
%config(noreplace) %{_sysconfdir}/xdg/user-dirs.defaults
%{_sysconfdir}/xdg/autostart/*
%{_mandir}/man1/*
%{_mandir}/man5/*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.17-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 0.17-1
- Update to 0.17

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Aug 21 2017 Kalev Lember <klember@redhat.com> - 0.16-1
- Update to 0.16
- Use license macro for COPYING
- Use make_build and make_install macros

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep  9 2015 Rui Matos <rmatos@redhat.com> - 0.15-7
- Change the xinit.d script to an xdg autostart file
Resolves: #1259896

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.15-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 Matthias Clasen <mclasen@redhat.com> - 0.15-1
- Man pages
- Translation updates
- Trim %%changelog

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue May  3 2011 Alexander Larsson <alexl@redhat.com> - 0.14-1
- Update to 0.14 (new translations)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 0.13-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Alexander Larsson <alexl@redhat.com> - 0.13-1
- Update to 0.13 with new translations

* Wed Mar 24 2010 Tomas Bzatek <tbzatek@redhat.com> - 0.12-1
- Update to 0.12 which only has a few new translations of Downloads
- Use fuzzy translations (for Downloads)  (#532399)
- Fix a typo in README

* Fri Sep 25 2009 Alexander Larsson <alexl@redhat.com> - 0.11-1
- Update to 0.11

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun May  4 2008 Matthias Clasen <mclasen@redhat.com> - 0.10-3
- Fix source url again
- Fix license tag

* Mon Mar 17 2008 Matthias Clasen <mclasen@redhat.com> - 0.10-2
- Fix Source URL

* Tue Feb 12 2008 Alexander Larsson <alexl@redhat.com> - 0.10-1
- Update to 0.10 (new translations)

* Tue Aug 21 2007 Alexander Larsson <alexl@redhat.com> - 0.9-1
- Update to 0.9 (new translations)

* Tue May 29 2007 Matthias Clasen <mclasen@redhat.com> - 0.8-2
- Fix a possible crash.

* Wed May 16 2007  <alexl@redhat.com> - 0.8-1
- Update to 0.8, (only) fixing bug that always recreated deleted directories (#240139)

* Wed Apr 11 2007 Alexander Larsson <alexl@redhat.com> - 0.6-1
- Update to 0.6 (minor fixes)

* Mon Mar 26 2007 Alexander Larsson <alexl@redhat.com> - 0.5-1
- update to 0.5 (more translations)

* Wed Mar  7 2007 Alexander Larsson <alexl@redhat.com> - 0.4-1
- Update to 0.4

* Thu Mar  1 2007 Alexander Larsson <alexl@redhat.com> - 0.3-1
- Update to 0.3

* Fri Feb 23 2007 Alexander Larsson <alexl@redhat.com> - 0.2-1
- initial version
