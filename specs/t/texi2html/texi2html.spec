# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: texi2html
Version: 5.0
Release: 26%{?dist}
# GPLv2+ is for the code
# OFSFDL (Old FSF Documentation License) for the documentation
# CC-BY-SA or GPLv2 for the images
License: GPL-2.0-or-later AND LicenseRef-OFSFDL AND (CC-BY-SA-3.0 OR GPL-2.0-only)
Summary: A highly customizable texinfo to HTML and other formats translator
Source0: http://download.savannah.nongnu.org/releases/%{name}/%{name}-%{version}.tar.bz2
# Do not install bundled Unicode-EastAsianWidth, bug #1154436,
# <https://savannah.nongnu.org/bugs/?43456>
Patch0: texi2html-5.0-Do-not-install-Unicode-EastAsianWidth-if-external-is.patch
# Do not install bundled libintl-perl, <https://savannah.nongnu.org/bugs/?43457>
Patch1: texi2html-5.0-Do-not-install-libintl-perl-if-external-is-used.patch
URL: http://www.nongnu.org/texi2html/
Requires: perl-interpreter >= 5.004
Requires: latex2html
# autotools for the unbundling patches
BuildRequires: make
BuildRequires: autoconf automake
BuildRequires: gcc-c++
BuildRequires: latex2html texlive-tex4ht gettext
BuildRequires: perl-generators
BuildRequires: perl(Data::Dumper)
BuildRequires: perl(Locale::Messages)
BuildRequires: perl(Text::Unidecode)
BuildRequires: perl(Unicode::EastAsianWidth)
# not detected automatically because it is required at runtime based on
# user configuration
Requires: perl(Locale::Messages)
Requires: perl(Text::Unidecode)
Requires: perl(Unicode::EastAsianWidth)
BuildArch: noarch

%description
The basic purpose of texi2html is to convert Texinfo documents into HTML, 
and other formats.  Configuration files written in perl provide fine degree 
of control over the final output, allowing most every aspect of the final 
output not specified in the Texinfo input file to be specified.  

%prep
%setup -q
%patch -P0 -p1
%patch -P1 -p1
# Remove bundled modules
rm -r lib
# Regenerate build script because of the patch
aclocal -I m4
automake --add-missing
autoconf

%build
%configure --with-external-libintl-perl=yes \
    --with-external-Unicode-EastAsianWidth=yes
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT 
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# directories shared by all the texinfo implementations for common
# config files, like htmlxref.cnf
mkdir -p $RPM_BUILD_ROOT%{_datadir}/texinfo $RPM_BUILD_ROOT%{_sysconfdir}/texinfo

%find_lang %{name}
%find_lang %{name}_document

%check
#make check

%files -f %{name}.lang -f %{name}_document.lang
%doc AUTHORS COPYING ChangeLog NEWS README TODO %{name}.init
%{_bindir}/%{name}
%{_datadir}/texinfo/html/%{name}.html
%{_mandir}/man*/%{name}*
%{_infodir}/%{name}.info*
%{_datadir}/texinfo/init/*.init
%dir %{_datadir}/%{name}/i18n/
%{_datadir}/%{name}/i18n/*
%dir %{_datadir}/%{name}/images/
%{_datadir}/%{name}/images/*
%dir %{_datadir}/texinfo
%dir %{_sysconfdir}/texinfo

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Than Ngo <than@redhat.com> - 5.0-20
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 08 2019 Troy Dawson <tdawson@redhat.com> - 5.0-11
- tetex-tex4ht changed to texlive-tex4ht
- BuildRequire gcc-c++

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 13 2017 Petr Pisar <ppisar@redhat.com> - 5.0-6
- perl dependency renamed to perl-interpreter
  <https://fedoraproject.org/wiki/Changes/perl_Package_to_Install_Core_Modules>

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 22 2014 Petr Pisar <ppisar@redhat.com> - 5.0-2
- Unbundle Unicode-EastAsianWidth (bug #1154436)
- Unbundle libintl-perl

* Mon Sep 08 2014 Phil Knirsch <pknirsch@redhat.com> - 5.0-1
- Update to texi2html-5.0 (#820697)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 1.82-10
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 11 2009 Jindrich Novy <jnovy@redhat.com> 1.82-5
- don't complain if installing with --excludedocs (#516010)
- disable tests for now

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.82-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan  9 2009 Jindrich Novy <jnovy@redhat.com> 1.82-2
- run tests after build

* Fri Jan  9 2009 Jindrich Novy <jnovy@redhat.com> 1.82-1
- update to 1.82

* Tue Jan  6 2009 Jindrich Novy <jnovy@redhat.com> 1.80-1
- update to 1.80

* Tue Aug 28 2007 Patrice Dumas <pertusus@free.fr> 1.78-3
- use the right license tag for the documentation

* Tue Aug 28 2007 Patrice Dumas <pertusus@free.fr> 1.78-2
- Requires latex2html and perl(Text::Unidecode)
- add ownership for directories common for the texinfo implementations
- correct license

* Wed Jun  6 2007 Jindrich Novy <jnovy@redhat.com> 1.78-1
- update to 1.78

* Wed Feb 14 2007 Jindrich Novy <jnovy@redhat.com> 1.77-0.1.20070214cvs
- update to 1.77 release candidate (#226487)

* Fri Jan  5 2007 Jindrich Novy <jnovy@redhat.com> 1.76-6
- fix post/preun scriptlets so that they won't fail with docs disabled
  (thanks to Ville Skyttä)

* Wed Nov 29 2006 Jindrich Novy <jnovy@redhat.com> 1.76-5
- replace PreReq, fix BuildRoot

* Thu Aug 24 2006 Jindrich Novy <jnovy@redhat.com> 1.76-4.fc6
- correct URLs, name patch backups correctly

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.76-3.1
- rebuild

* Sat Feb 25 2006 Jindrich Novy <jnovy@redhat.com> 1.76-3
- PreReq info (#182888)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Mar 08 2005 Jindrich Novy <jnovy@redhat.com> 1.76-2
- replace %%configure with ./configure to prevent definition of
  target, build and host for noarch package

* Fri Feb 18 2005 Jindrich Novy <jnovy@redhat.com> 1.76-1
- we have separate texi2html package now (#121889)
- fix Source0
- BuildArchitectures -> BuildArch
- create backups for patches

* Thu Feb 10 2005 MATSUURA Takanori <t-matsuu@estyle.ne.jp> - 1.76-0
- updated to 1.76

* Mon Jan 10 2005 MATSUURA Takanori <t-matsuu@estyle.ne.jp> - 1.72-1.fc3
- initial build for Fedora Core 3 based on spec file in source tarball

* Tue Mar 23 2004 Patrice Dumas <pertusus@free.fr> 0:1.69-0.fdr.1
- Initial build.
