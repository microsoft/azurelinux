# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

BuildRequires: fontforge

Version: 2.000
Release: 42%{?dist}
URL: http://madanpuraskar.org/

%global fontlicense       GPL-1.0-or-later
%global fontlicenses      license.txt

%global fontfamily        Madan
%global fontsummary       Font for Nepali language
%global fonts             madan.ttf
%global fontconfs         %{SOURCE1}
%global fontdescription   %{expand:
This package provides the Madan font for Nepali made by the
Madan Puraskar Pustakalaya project.}

# Found new following working Source URL. Use wget to download this archive
Source0: http://ltk.org.np/downloads/fonts.zip
Source1: 65-0-%{fontpkgname}.conf
# Extract from font info
Source2: license.txt
Source3: sfd2ttf.pe
# Below files will make sure "fc-scan madan.ttf |grep lang:" will show ne
Source4: madan.py
Source5: madan_u0970_glyph.svg

%fontpkg

%prep
%autosetup -c
cp -p %{SOURCE2} %{SOURCE3} \
      %{SOURCE4} %{SOURCE5} .

%linuxtext license.txt

chmod 755 sfd2ttf.pe madan.py 
./madan.py madan.ttf madan_u0970_glyph.svg
./sfd2ttf.pe madan.sfd

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-41
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Parag Nemade <pnemade AT redhat DOT com> - 2.000-34
- Update license tag to SPDX format

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.000-28
- Update fontconfig DTD id in conf file

* Wed Mar 18 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.000-27
- Update CI script for new installed font path 

* Tue Mar 10 2020 Parag Nemade <pnemade AT redhat DOT com> - 2.000-26
- Convert to new fonts packaging guidelines

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 30 2019 Parag Nemade <pnemade AT redhat DOT com> - 2.000-24
- Fix adding U0970 based on Vishal Vijayraghavan's fix

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.000-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 03 2015 Parag Nemade <pnemade AT redhat DOT com> - 2.000-16
- Rebase patch0 against fontforge2 build (Thanks PravinS)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 22 2014 Parag Nemade <pnemade AT redhat DOT com> - 2.000-14
- Rebase patch0 against fontforge2 build

* Thu Oct 16 2014 Parag Nemade <pnemade AT redhat DOT com> - 2.000-13
- Add metainfo file to show this font in gnome-software

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 26 2012 Parag <pnemade AT redhat DOT com> - 2.000-9
- Resolves:rh#880037 - Update Source URL in spec file

* Fri Aug 03 2012 Parag <pnemade AT redhat DOT com> - 2.000-8
- Resolves: rh#842965, added character u0970
- Enabled autohint in fontconf file

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 28 2011 Parag <pnemade AT redhat DOT com> - 2.000-5
- Rebuild for rh#757105 - no font(:lang=blahblah) generated for Provides

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.000-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue May 18 2010 Parag <pnemade AT redhat.com> - 2.000-3
- Resolves: rh#586765 - Rename 65-madan.conf to 65-0-madan.conf    

* Tue Apr 20 2010 Parag <pnemade AT redhat.com> - 2.000-2
- Resolves: rh#578041-lang-specific overrides rule doesn't work as expected

* Tue Feb 23 2010 Parag <pnemade AT redhat.com> - 2.000-1
- Update to next upstream release
- Resolves: rh#335851-[ne_NP] Add license text file to madan-fonts package
- Resolves: rh#520047-[ne_NP] Need fontconfig rules for Madan font

* Tue Aug 11 2009 Parag <pnemade@redhat.com> - 1.0-11
- Fix source audit 2009-08-10

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 08 2009 Pravin Satpute <psatpute@redhat.com> - 1.0-9
- updated spec as per new packaging guideline

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0-7
- fix license tag

* Mon Oct 15 2007 Rahul Bhalerao <rbhalera@redhat.com> - 1.0-6.fc8
- Spec update as per review

* Thu Oct 11 2007 Rahul Bhalerao <rbhalera@redhat.com> - 1.0-5.fc8
- Spec update as per reveiw

* Wed Sep 26 2007 Rahul Bhalerao <rbhalera@redhat.com> - 1.0-4.fc8
- Spec update as per review

* Fri Sep 21 2007 Rahul Bhalerao <rbahlera@redhat.com> - 1.0-3.fc8
- Added LICENSE as Source1

* Thu Sep 20 2007 Rahul Bhalerao <rbhalera@redhat.com> - 1.0-2.fc8
- Removed use of tarball and ghost files

* Thu Sep 13 2007 Rahul Bhalerao <rbhalera@redhat.com> - 1.0-1.fc8
- Initial packaging
