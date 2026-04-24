# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version:        0.003
Release: 45%{?dist}

URL: https://fonts.google.com/specimen/Jomolhari

%global fontlicense       OFL-1.1
%global fontlicenses      OFL.txt
%global fontdocs          *.txt
%global fontdocsex        %{fontlicenses}

%global fontfamily        Jomolhari
%global fontsummary       Jomolhari a Bhutanese style font for Tibetan and Dzongkha
%global archivename       jomolhari-alpha003c
%global fonts             *.ttf
%global fontconfs         %{SOURCE1}
%global fontdescription   %{expand:
Jomolhari is an TrueType OpenType Bhutanese style font for Dzongkha and
Tibetan text. It is based on Bhutanese manuscript examples, supports the
Unicode and the Chinese encoding for Tibetan.
The font supports the standard combinations used in most texts.}

Source0: http://chris.fynn.googlepages.com/%{archivename}.zip
Source1:        65-0-%{fontpkgname}.conf 

%fontpkg

%prep
%setup -q -c
%linuxtext FONTLOG.txt OFL-FAQ.txt OFL.txt

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.003-37
- Update license tag to SPDX format

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat May 15 2021 Parag Nemade <pnemade AT redhat DOT com> - 0.003-33
- Update for relevant active URL: tag but keep Source0: as it is

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Parag Nemade <pnemade AT redhat DOT com> - 0.003-30
- Update fontconfig DTD id in conf file

* Fri Mar 13 2020 Parag Nemade <pnemade AT redhat DOT com> - 0.003-29
- Convert to new fonts packaging guidelines

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.003-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Oct 17 2014 Parag Nemade <pnemade AT redhat DOT com> - 0.003-19
- Add metainfo file to show this font in gnome-software

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Parag <pnemade AT redhat DOT com> - 0.003-15
- Resolves:rh#879544: upstream source url not active

* Thu Aug 16 2012 Parag <pnemade AT redhat DOT com> - 0.003-14
- Resolves:rh#847627 - Malformed fontconfig config file

* Tue Aug 14 2012 Parag <pnemade AT redhat DOT com> - 0.003-13
- Resolves:rh#847621 - better enabling autohinting by default
- Resolves:rh#847623 - fontconfig file isn't shipped in rpm
- Resolves:rh#847627 - Malformed fontconfig config file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 Parag <pnemade AT redhat.com> - 0.003-9
- Resolves:rh#586241  - No fontconfig config files provided

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar 15 2009 Marcin Garski <mgarski[AT]post.pl> 0.003-7
- Update to new fonts guidelines, thanks to Rajeesh K Nambiar (#477403)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.003-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 29 2008 Marcin Garski <mgarski[AT]post.pl> 0.003-5
- Update URL

* Fri Aug 31 2007 Marcin Garski <mgarski[AT]post.pl> 0.003-4
- Fix license tag

* Fri Apr 06 2007 Marcin Garski <mgarski[AT]post.pl> 0.003-3
- Update to 0.003c
- Change license from GPL to OFL

* Fri Mar 23 2007 Marcin Garski <mgarski[AT]post.pl> 0.003-2
- Extend description section

* Mon Mar 12 2007 Marcin Garski <mgarski[AT]post.pl> 0.003-1
- Initial specfile
