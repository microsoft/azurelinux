# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global fontname paktype-naskh-basic
%global release_date 20231228

Version:       7.0
Release: 4.%{release_date}%{?dist}
URL:           https://sourceforge.net/projects/paktype/

%global foundry           paktype
%global fontlicense       GPL-2.0-only WITH Font-exception-2.0
%global fontlicenses      PakType_Naskh_Basic_License.txt
%global fontdocs          PakTypeNaskhBasicFeatures.pdf

%global fontfamily        PakType Naskh Basic
%global fontsummary       Fonts for Arabic, Farsi, Urdu and Sindhi from PakType
%global fonts             PakTypeNaskhBasic*.ttf
%global fontconfs         %{SOURCE10}

%global fontdescription   %{expand:
The paktype-naskh-basic-fonts package contains fonts for the display of \
Arabic, Farsi, Urdu and Sindhi from PakType by Lateef Sagar.
}

Source0:        https://downloads.sourceforge.net/project/paktype/PakType-Release-2023-12-28.tar.gz
Source10:       55-0-%{fontpkgname}.conf

%fontpkg

%prep
%autosetup -c
pwd
pushd License\ files/
%linuxtext -e ascii "PakType Naskh Basic License.txt"
popd

mv License\ files/PakType\ Naskh\ Basic\ License.txt PakType_Naskh_Basic_License.txt
mv Features/PakType\ Naskh\ Basic\ Features.pdf PakTypeNaskhBasicFeatures.pdf
chmod 644 PakTypeNaskhBasicFeatures.pdf

%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-3.20231228
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0-2.20231228
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 30 2024 Parag Nemade <pnemade AT redhat DOT com> - 7.0-1.20231228
- Update to new upstream source archive 20231228 (rhbz#2213602)

* Tue Jun 18 2024 Sudip Shil <sshil@redhat.com> - 6.0-12
- increase priority of paktype-naskh-basic-fonts for urdu

* Mon Jun 17 2024 Parag Nemade <pnemade AT redhat DOT com> - 6.0-11
- Drop unnecessary BuildRequires: on make and fontforge

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Sudip Shil <sshil@redhat.com> - 6.0-7
- Convert to new fonts packaging guidelines and SPDX license
- Update the fonts package
- https://fedoraproject.org/wiki/Changes/New_Fonts_Packaging

* Fri Jun  9 2023 Jens Petersen <petersen@redhat.com> - 6.0-6
- rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar 01 2021 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 6.0-1
- Upstream release 6.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 13 2020 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 5.0-1
- Upstream 5.0 Release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Feb 06 2014 Pravin Satpute <psatpute@redhat.com> - 4.1-3
- Resolves bz:1062128 : Making default font for Urdu language

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 22 2013 Pravin Satpute <psatpute@redhat.com> - 4.1-1
- Upstream 4.1 Release

* Tue Feb 05 2013 Pravin Satpute <psatpute@redhat.com> - 4.0-2
- Upstream changed tarball

* Wed Nov 21 2012 Pravin Satpute <psatpute@redhat.com> - 4.0-1
- Upstream 4.0 release. Now no language specific ttf

* Mon Sep 03 2012 Naveen Kumar <nkumar@redhat.com> - 3.1-1
- Upstream 3.1 release

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jun 21 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-8
- add ur-in, ur-pk & pa-pk locale-specific overrides rule in 67-paktype-naskh-basic.conf
- add ur-in, ur-pk & pa-pk locale-specific overrides rule in 67-paktype-naskh-basic-sa.conf
- resolves bug #586789

* Thu May 6 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-7
- remove binding="same" from all *.conf files

* Fri Mar 12 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-6
- Changes in summary and description

* Fri Mar 12 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-5
- changed the name of package from paktype-nashk-basic to paktype-naskh-basic

* Tue Mar 9 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-4
- removed redundant  BuildRequires from specfile
- removed unnecessary rm/rmdir's from specfile
- Sane updates in docs.

* Fri Mar 5 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-3
- removed all cd's
- changes w.r.t sed in prep section
- added .conf file for PakTypeNaskhBasic.ttf
- files section added for common
- removed space from 67-*-sindhi.conf

* Mon Feb 15 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-2
- Re-packing with updated License information.
- Changes in Spec file with new upstream source.
- Added conf files

* Mon Feb 15 2010 Naveen Kumar <nkumar@redhat.com> - 3.0-1
- Initial packaging for version-3.0
