# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global archivename %{name}-ttf-%{version}
%define catalogue %{_sysconfdir}/X11/fontpath.d

BuildArch: noarch
BuildRequires:    mkfontscale mkfontdir

Epoch:      1
Version:    2.1.5
Release:    14%{?dist}
License:    OFL-1.1-RFN
URL:        https://github.com/liberationfonts/liberation-fonts

%global     fontlicenses    LICENSE
%global     fontdocs        AUTHORS ChangeLog README.md TODO
%global     fontdocsex      %{fontlicenses}

%global common_description %{expand:
The Liberation Fonts are intended to be replacements for the 3 most commonly\
used fonts on Microsoft systems: Times New Roman, Arial, and Courier New.}

%global fontpkgheaderall  %{expand:
Obsoletes: %{name} < %{epoch}:%{version}-%{release}
Provides:  %{name} = %{epoch}:%{version}-%{release}
}

%global fontfamily1       Liberation Sans
%global fontsummary1      Sans-serif fonts to replace commonly used Microsoft Arial
%global fontpkgheader1    %{expand:
Obsoletes: %{name}-common < %{epoch}:%{version}-%{release}
Provides:  %{name}-common = %{epoch}:%{version}-%{release}
}
%global fonts1            LiberationSans*.ttf
%global fontconfs1        %{SOURCE2}
%global fontdescription1  %{expand:
This package provides Sans-serif TrueType fonts that replace commonly used
Microsoft Arial.

%{common_description} }

%global fontfamily2       Liberation Serif
%global fontsummary2      Serif fonts to replace commonly used Microsoft Times New Roman
%global fontpkgheader2    %{expand:
Obsoletes: %{name}-common < %{epoch}:%{version}-%{release}
Provides:  %{name}-common = %{epoch}:%{version}-%{release}
}
%global fonts2            LiberationSerif*.ttf
%global fontconfs2        %{SOURCE3}
%global fontdescription2  %{expand:
This package provides Serif TrueType fonts that replace commonly used
Microsoft Times New Roman.

%{common_description} }

%global fontfamily3       Liberation Mono
%global fontsummary3      Monospace fonts to replace commonly used Microsoft Courier New
%global fontpkgheader3    %{expand:
Obsoletes: %{name}-common < %{epoch}:%{version}-%{release}
Provides:  %{name}-common = %{epoch}:%{version}-%{release}
}
%global fonts3            LiberationMono*.ttf
%global fontconfs3        %{SOURCE4}
%global fontdescription3  %{expand:
This package provides Monospace TrueType fonts that replace commonly used
Microsoft Courier New.

%{common_description} }

Source2:    59-%{fontpkgname1}.conf
Source3:    59-%{fontpkgname2}.conf
Source4:    59-%{fontpkgname3}.conf

Name:       liberation-fonts
Summary:    Fonts to replace commonly used Microsoft Windows fonts
Source0:    %{url}/files/7261482/%{archivename}.tar.gz

%description
%wordwrap -v common_description

%fontpkg -a

%fontmetapkg

%prep
%autosetup -n %{archivename}

%build
%fontbuild -a

%install
%fontinstall 
# fonts .ttf
# catalogue
install -m 0755 -d %{buildroot}%{catalogue}
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

%fontinstall -z 1
mkfontscale %{buildroot}%{fontdir1}
mkfontdir %{buildroot}%{fontdir1}
ln -sf $(realpath --relative-to=%{buildroot}%{catalogue} %{buildroot}%{_fontbasedir})/%{fontpkgname1} %{buildroot}%{catalogue}/%{fontpkgname1}
install -m 0644 -p %{SOURCE2} %{buildroot}%{_fontconfig_templatedir}/59-%{fontpkgname1}.conf
ln -sf $(realpath --relative-to=%{_fontconfig_confdir} %{_fontconfig_templatedir})/59-%{fontpkgname1}.conf %{buildroot}%{_fontconfig_confdir}/59-%{fontpkgname1}.conf

%fontinstall -z 2
mkfontscale %{buildroot}%{fontdir2}
mkfontdir %{buildroot}%{fontdir2}
ln -sf $(realpath --relative-to=%{buildroot}%{catalogue} %{buildroot}%{_fontbasedir})/%{fontpkgname2} %{buildroot}%{catalogue}/%{fontpkgname2}
install -m 0644 -p %{SOURCE3} %{buildroot}%{_fontconfig_templatedir}/59-%{fontpkgname2}.conf
ln -sf $(realpath --relative-to=%{_fontconfig_confdir} %{_fontconfig_templatedir})/59-%{fontpkgname2}.conf %{buildroot}%{_fontconfig_confdir}/59-%{fontpkgname2}.conf

%fontinstall -z 3
mkfontscale %{buildroot}%{fontdir3}
mkfontdir %{buildroot}%{fontdir3}
ln -sf $(realpath --relative-to=%{buildroot}%{catalogue} %{buildroot}%{_fontbasedir})/%{fontpkgname3} %{buildroot}%{catalogue}/%{fontpkgname3}
install -m 0644 -p %{SOURCE4} %{buildroot}%{_fontconfig_templatedir}/59-%{fontpkgname3}.conf
ln -sf $(realpath --relative-to=%{_fontconfig_confdir} %{_fontconfig_templatedir})/59-%{fontpkgname3}.conf %{buildroot}%{_fontconfig_confdir}/59-%{fontpkgname3}.conf


%check
%fontcheck -a

%fontfiles -z 1
%{catalogue}/%{fontpkgname1}
%verify(not md5 size mtime) %{fontdir1}/fonts.dir
%verify(not md5 size mtime) %{fontdir1}/fonts.scale
%ghost %attr(644, root, root) %{fontdir1}/.uuid

%fontfiles -z 2
%{catalogue}/%{fontpkgname2}
%verify(not md5 size mtime) %{fontdir2}/fonts.dir
%verify(not md5 size mtime) %{fontdir2}/fonts.scale
%ghost %attr(644, root, root) %{fontdir2}/.uuid

%fontfiles -z 3
%{catalogue}/%{fontpkgname3}
%verify(not md5 size mtime) %{fontdir3}/fonts.dir
%verify(not md5 size mtime) %{fontdir3}/fonts.scale
%ghost %attr(644, root, root) %{fontdir3}/.uuid



%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Parag Nemade <pnemade AT redhat DOT com> - 1:2.1.5-11
- Fix upgrade path for liberation-fonts binary rpm
  Thanks to Akira for his fix in fonts-rpm-macros

* Mon Jun 17 2024 Parag Nemade <pnemade AT redhat DOT com> - 1:2.1.5-10
- Convert SPEC to new fonts packaging guidelines
- Use binary fonts to build packages instead source sfd files
  this will drop the need of BR:fonttools and fontforge packages

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 25 2023 Akira TAGOH <tagoh@redhat.com> - 1:2.1.5-7
- Add a rule to use Liberation Sans as a fallback of ArialMT.
  Resolves: rhbz#1490184

* Mon Aug 21 2023 Parag Nemade <pnemade AT fedoraproject DOT org> - 1:2.1.5-6
- Migrate to SPDX license expression

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 06 2021 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.1.5-1
- New release of liberation-fonts 2.1.5

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 31 2021 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.1.4-1
- New release of liberation-fonts 2.1.4

* Thu Mar 04 2021 Peter Hutterer <peter.hutterer@redhat.com> 1:2.1.3-2
- Require mkfontscale and mkfontdir directly, not xorg-x11-font-utils
  (#1933539)

* Mon Mar 01 2021 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.1.3-1
- New release of liberation-fonts 2.1.3
- Resolves:rh#1464310 : Tilded G not works with Liberation Sans and Serif

* Tue Feb 02 2021 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.1.2-1
- New release of liberation-fonts 2.1.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 10 2020 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.1.0-1
- New release of liberation-fonts 2.1.0 

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.00.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.00.5-7
- update .uuid file permission in ghost macro

* Fri Sep 13 2019 Jens Petersen <petersen@redhat.com> - 1:2.00.5-6
- base package now pulls in subpackages (#1748803)
- improve descriptions

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.00.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 1 2019 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.00.5-4
- Updated CI test

* Mon Jun 24 2019 Vishal Vijayraghavan <vvijayra AT redhat DOT com> - 1:2.00.5-3
- Remove Obsoletes and Provides for liberation-narrow-fonts (#1707712)
- Splitted the font family(mono, sans and serif) into diferrent root font directories   

* Mon Apr 15 2019 Vishal Vijayraghavan <vishalvijayraghavan AT gmail DOT com> - 1:2.00.5-2
- Added CI Test

* Wed Mar 6 2019 Vishal Vijayraghavan <vishalvijayraghavan AT gmail DOT com> - 1:2.00.5-1
- New release of liberation-fonts 2.00.5 

* Tue Dec 11 2018 Vishal Vijayraghavan <vishalvijayraghavan AT gmail DOT com> - 1:2.00.4-1
- Resolves:rh#1490184 - ArialMT fonts should be replaced by Liberation Sans (instead of default "Dejavu Sans" "Book")
- Update to 2.00.4

* Thu Aug 16 2018 Vishal Vijayraghavan <vishalvijayraghavan AT gmail DOT com> - 1:2.00.3-2
- Updated License from Liberation to OFL 

* Wed Jul 25 2018 Vishal Vijayraghavan <vishalvijayraghavan AT gmail DOT com> - 1:2.00.3-1
- Updated the BuildRequires to python3 and using latest build
- Changed the upstream URL

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.00.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 17 2018 Björn Esser <besser82@fedoraproject.org> - 1:2.00.1-2
- Add proper Obsoletes/Provides for liberation-narrow-fonts

* Wed Mar 14 2018 Parag Nemade <pnemade AT redhat DOT com> - 1:2.00.1-1
- Update to 2.00.1

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.07.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 18 2017 Parag Nemade <pnemade AT fedoraproject DOT org> - 1:1.07.4-10
- Resolves:rh#1526510 - USE_TYPO_METRICS set in Fedora 2X but not set in RHEL7 or in ttf binary release
- some spec cleanups

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.07.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.07.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.07.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Aug 12 2015 Pravin Satpute <psatpute@redhat.com> - 1:1.07.4-6
- Resolves #1252564: Enabled Meta packages for installing mono, narrow, sans and serif.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.07.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 15 2014 Richard Hughes <richard@hughsie.com> - 1:1.07.4-4
- Add a MetaInfo file for the software center; this is a font we want to show.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.07.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 21 2014 Pravin Satpute <psatpute@redhat.com> - 1:1.07.4-2
- resolved md5sum mismatch issue

* Fri Apr 18 2014 Pravin Satpute <psatpute@redhat.com> - 1:1.07.4-1
- Upstream release of 1.07.4
- Restored Liberation Sans Bold 'u' instructions
- Resolved #1009650, renames serbian shapes as per AGL
- Added new glyph for "imacron" and "g"
- Added Correct shape for uni266B in all Liberation variants #1014357
- Resolved Problematic shapes for macedonian alphabet #1013949

* Wed Aug 28 2013 Pravin Satpute <psatpute@redhat.com> - 1:1.07.3-2
- Resolved #715309: Improved Bold 'u' hinting

* Fri Aug 23 2013 Pravin Satpute <psatpute@redhat.com> - 1:1.07.3-1
- Upstream release 1.07.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.07.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.07.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 15 2013 Pravin Satpute <psatpute@redhat.com> - 1:1.07.2-12
- Corrected font conf priority from 30-0 to 59
- building from f18 to rawhide

* Fri Dec 07 2012 Pravin Satpute <psatpute@redhat.com> - 1:1.07.2-11
- Decided to defer Liberation 2.0 feature in Fedora 18.
- Reverting to Liberation 1.07.2. 
- Using 11 release to match with Liberation Sans Narrow

* Wed Nov 21 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-4
- Improved spec file

* Tue Nov 20 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-3
- Resolved bug 878305

* Tue Nov 20 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-2
- Resolved issues of md5sum

* Thu Oct 04 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.1-1
- Upstream release of 2.00.1 version

* Wed Sep 12 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.0-2
- Removed fontconf files of 59 priority, now only has 30-0 alias file

* Thu Jul 26 2012 Pravin Satpute <psatpute@redhat.com> - 2.00.0-1
- First upstream release with OFL license
- Added conf files with 59 priority

* Tue Jun 26 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-6
- Resolves bug 835182

* Tue Jun 26 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-5
- Resolves bug 835182

* Thu May 10 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-4
- Resolves bug 799384

* Sat Feb 18 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-3
- Resolved bug 714191

* Mon Feb 13 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-2
- Resolved #715309

* Thu Feb 09 2012 Pravin Satpute <psatpute@redhat.com> - 1.07.2-1
- Upstream release 1.07.2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.07.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.1-3
- Resolved bug 753572, removed hint of cent sign

* Fri Oct 14 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.1-2
- Resolved bug 657849, added support in Sans and Serif

* Wed Sep 21 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.1-1
- Upstream Release 1.07.1
- Resolved bug 738264, 729989

* Mon May 30 2011 Pravin Satpute <psatpute@redhat.com> - 1.07.0-1
- Upstream Release 1.07.0
- Resolved bug 659214, 708330, 707973 

* Thu Feb 24 2011 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-5
- bug 659214: added bulgarian characters

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.06.0.20100721-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 13 2010 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-3
- bug 642493: use consistent ttf names

* Tue Oct 12 2010 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-2
- Building from sources
- Applying Monospace font patch bug 620273

* Thu Jul 22 2010 Pravin Satpute <psatpute@redhat.com> - 1.06.0.20100721-1
- Upstream New Release
- Added New Family Narrow

* Wed Jun 16 2010 Caius 'kaio' Chance <cchance@redhat.com> - 1.05.3.20100510-2
- Updated Source URL to FedoraHosted and repackaged.

* Mon May 10 2010 Caius 'kaio' Chance <me at kaio.net> - 1.05.3.20100510-1
- Updated from upstream.
- Fixed correct Romanian glyphs in Liberation Fonts. (rhbz#440992)

* Fri May 07 2010 Caius 'kaio' Chance <me at kaio.net> - 1.05.3.20100506-2
- Updated package URL and source URL.

* Thu May 06 2010 Caius 'kaio' Chance <me at kaio.net> - 1.05.3.20100506-1
- Updated from upstream.
- Cleaned up points and auto-instructed hinting of 'u', 'v', 'w', 'y'.
(rhbz#463036)

* Wed May 05 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100505-2
- Made 0x00A2 cent sign be coressed in Sans Narrow.

* Wed May 05 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100505-1
- Updated from upstream.
- Resolves: rhbz#474522 - Incorrect cent sign glyph (U+00A2) in Sans and Mono style in Liberation fonts.

* Wed Apr 28 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100428-1
- rhbz#510174: Corrected version number of all SFD files.
- Corrected license exceptions to GPLv2.
- Updated README file.

* Tue Apr 27 2010 Caius 'kaio' Chance <k at kaio.net> - 1.05.3.20100427-1
- Updated source from upstream.
- Introduced Sans Narrow by upstream.

* Wed Jan 13 2010 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-5.fc13
- Removed 'Provides liberation-fonts and liberation-fonts-compat by
  liberation-fonts-common.'

* Tue Jan 12 2010 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-4.fc13
- Rebuilt w/ macro fixes.

* Tue Jan 12 2010 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-3.fc13
- Removed full stop in Summary.
- Set default file permission in files.
- Provides liberation-fonts and liberation-fonts-compat by 
  liberation-fonts-common.
- Macro as much as possible in .spec.

* Mon Oct 19 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-2.fc13
- Rebuilt.

* Mon Oct 19 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.2.20091019-1.fc13
- Resolves: rhbz#525498 - wrongly encoded glyphs after U+10000.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.05.1.20090721-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090721-1.fc12
- Fixed fontforge scripting of sfd -> ttf generation.
- Checked existance of traditionat kern table in Sans and Serif.

* Tue Jul 14 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090713-2.fc12
- Required fontforge ver 20090408 which supports generation with traditional
  kern table. (rhbz#503430)

* Mon Jul 13 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090713-1.fc12
- Updated to upstream 1.05.1.20090713.
- Generate TTFs with traditional kern table via fontforge scripts. (rh#503430)

* Mon Jul 06 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090706-1.fc12
- Updated to upstream 1.05.1.20090706.
- Reconverted from original TTF with traditional kern table. (rh#503430)

* Tue Jun 30 2009 Caius 'kaio' Chance <k at kaio.me> - 1.05.1.20090630-1.fc12
- Updated to upstream 1.05.1.20090630.
- Reconverted from original TTF with better procedures of data conservation.

* Tue May 19 2009 Jens Petersen <petersen@redhat.com> - 1.04.93-11
- remove redundant obsoletes, provides and conflicts from new subpackages

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.04.93-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 05 2009 Caius Chance <cchance@redhat.com> - 1.04.93-9.fc11
- Fixed inter-subpackage dependencies with reference of dejavu.

* Wed Feb 04 2009 Caius Chance <cchance@redhat.com> - 1.04.93-8.fc11
- Fixed inter-subpackage dependencies.

* Wed Feb 04 2009 Caius Chance <cchance@redhat.com> - 1.04.93-7.fc11
- Create -compat subpackage as meta-package for installing all font families.

* Tue Jan 20 2009 Matthias Clasen <mclasen@redhat.com> - 1.04.93-6.fc11
- Fix busted inter-subpackage dependencies

* Tue Jan 20 2009 Caius Chance <cchance@redhat.com> - 1.04.93-5.fc11
- Resolved: rhbz#477410
- Refined .spec file based on Mailhot's review on rhbz.

* Mon Jan 19 2009 Caius Chance <cchance@redhat.com> - 1.04.93-4.fc11
- Resolves: thbz#477410
- Package renaming for post-1.13 fontpackages macros.

* Fri Jan 09 2009 Caius Chance <cchance@redhat.com> - 1.04.93-3.fc11
- Resolves: rhbz#477410 (Convert to new font packaging guidelines.)

* Tue Dec 09 2008 Caius Chance <cchance@redhat.com> - 1.04.93-2.fc11
- Resolves: rhbz#474522 (Cent sign is not coressed in Sans & Mono.)

* Wed Dec 03 2008 Caius Chance <cchance@redhat.com> - 1.04.93-1.fc11
- Resolves: rhbz#473481
  (Blurriness of Greek letter m (U+03BC) in Liberation Sans Regular.)

* Thu Jul 17 2008 Caius Chance <cchance@redhat.com> - 1.04.90-1.fc10
- Resolves: rhbz#258592
  (Incorrect glyph points and missing hinting instructions for U+0079, U+03BC,
   U+0431, U+2010..2012.)

* Thu Jul 17 2008 Caius Chance <cchance@redhat.com> - 1.04-1.fc10
- Resolves: rhbz#455717 (Update sources to version 1.04.)
- Improved .spec file.

* Thu Jun 12 2008 Caius Chance <cchance@redhat.com> - 1.04-0.1.beta2.fc10
- Updated source version to 1.04.beta2.
- Removed License.txt and COPYING as already included in sources.

* Thu Apr 10 2008 Caius Chance <cchance@redhat.com> - 1.03-1.fc9
- Resolves: rhbz#251890 (Exchanged and incomplete glyphs.)
- Repack source tarball and re-align source version number.

* Mon Mar 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.02-2
- correct license tag, license explanation added

* Tue Mar 25 2008 Caius Chance <cchance@redhat.com> - 1.02-1.fc9
- Resolves: rhbz#240525 (Alignment mismatch of dot accents.)

* Wed Jan 16 2008 Caius Chance <cchance@redhat.com> - 1.01-1.fc9
- Moved source tarball from cvs to separated storage.

* Mon Jan 14 2008 Caius Chance <cchance@redhat.com> - 1.0-1.fc9
- Resolves: rhbz#428596 (Liberation fonts need to be updated to latest font.)

* Wed Nov 28 2007 Caius Chance <cchance@redhat.com> - 0.2-4.fc9
- Resolves: rhbz#367791 (remove 59-liberation-fonts.conf)

* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.2-3.fc8
- add fontdir macro
- create fonts.dir and fonts.scale (reported by Mark Alford, #245961)
- add catalogue symlink

* Wed Sep 12 2007 Jens Petersen <petersen@redhat.com> - 0.2-2.fc8
- update license field to GPLv2

* Thu Jun 14 2007 Caius Chance <cchance@redhat.com> 0.2-1.fc8
- Updated new source tarball from upstream: '-3' (version 0.2).

* Tue May 15 2007 Matthias Clasen <mclasen@redhat.com> 0.1-9
- Bump revision

* Tue May 15 2007 Matthias Clasen <mclasen@redhat.com> 0.1-8
- Change the license tag to "GPL + font exception"

* Mon May 14 2007 Matthias Clasen <mclasen@redhat.com> 0.1-7
- Correct the source url

* Mon May 14 2007 Matthias Clasen <mclasen@redhat.com> 0.1-6
- Incorporate package review feedback

* Fri May 11 2007 Matthias Clasen <mclasen@redhat.com> 0.1-5
- Bring the package in sync with Fedora packaging standards

* Wed Apr 25 2007 Meethune Bhowmick <bhowmick@redhat.com> 0.1-4
- Require fontconfig package for post and postun

* Tue Apr 24 2007 Meethune Bhowmick <bhowmick@redhat.com> 0.1-3
- Bump version to fix issue in RHEL4 RHN

* Thu Mar 29 2007 Richard Monk <rmonk@redhat.com> 0.1-2rhis
- New license file

* Thu Mar 29 2007 Richard Monk <rmonk@redhat.com> 0.1-1rhis
- Inital packaging
