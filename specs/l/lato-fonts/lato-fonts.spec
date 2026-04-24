# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version: 2.015
Release: 25%{?dist}
URL:     http://www.latofonts.com/

%global fontlicense       OFL-1.1
%global fontlicenses      OFL.txt
%global fontdocs          README.txt
%global fontdocsex        %{fontlicenses}

%global fontfamily        Lato
%global fontsummary       A san-serif typeface family
%global fonts             Lato-*.ttf
%global fontconfs         %{SOURCE10}

%global fontdescription   %{expand:
Lato is a sanserif typeface family designed in the Summer 2010 by Warsaw-based
designer Łukasz Dziedzic ("Lato" means "Summer" in Polish). In December 2010 the
Lato family was published under the open-source Open Font License by his foundry
tyPoland, with support from Google.

When working on Lato, Łukasz tried to carefully balance some potentially
conflicting priorities. He wanted to create a typeface that would seem quite
"transparent" when used in body text but would display some original treats when
used in larger sizes. He used classical proportions (particularly visible in the
uppercase) to give the letterforms familiar harmony and elegance. At the same
time, he created a sleek sanserif look, which makes evident the fact that Lato
was designed in 2010 - even though it does not follow any current trend.

The semi-rounded details of the letters give Lato a feeling of warmth, while the
strong structure provides stability and seriousness. "Male and female, serious
but friendly. With the feeling of the Summer," says Łukasz.

Lato consists of nine weights (plus corresponding italics), including a
beautiful hairline style. It covers 2300+ glyphs per style and supports 100+
Latin-based languages, 50+ Cyrillic-based languages as well as Greek and IPA
phonetics.
}

# Fonts retrieved 2015-08-07 from http://www.latofonts.com/download/Lato2OFL.zip
Source0:  %{name}-%{version}.zip
Source10: 61-%{fontpkgname0}.conf

%fontpkg

%prep
%setup -q -n Lato2OFL

# Fix wrong end-of-lines encoding
%linuxtext OFL.txt

# Fix permissions
chmod 0644 OFL.txt README.txt

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Akira TAGOH <tagoh@redhat.com> - 2.015-21
- Fix a typo in fontconfig config.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 28 2023 Akira TAGOH <tagoh@redhat.com> - 2.015-18
- Convert License tag to SPDX.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jun 26 2023 Parag Nemade <pnemade AT fedoraproject DOT org> - 2.015-16
- Convert to new fonts packaging guidelines
- Migrate to SPDX license expression
- Drop very very old obsoletes for google-lato-fonts
- Add gating CI tests in Fedora

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 07 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.015-1
- Update to 2.015

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 15 2014 Richard Hughes <richard@hughsie.com> - 2.010-2
- Add a MetaInfo file for the software center; this is a font we want to show.

* Thu Sep 04 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.010-1
- Update to 2.010

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 02 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.007-1
- Update to 2.007

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.105-1
- Update to 1.105

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 29 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.014-2
- Drop useless Buildroot cleaning

* Sun Sep 23 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.014-1
- Initial release, to replace google-lato-fonts package
