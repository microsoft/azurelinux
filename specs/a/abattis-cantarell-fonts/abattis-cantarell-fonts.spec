# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Version: 0.301
Release: 16%{?dist}
URL: https://gitlab.gnome.org/GNOME/cantarell-fonts/

%global	common_description	%{expand:
The Cantarell font family is a contemporary Humanist sans serif
designed for on-screen reading. The fonts were originally designed
by Dave Crossland.}

%global	foundry		abattis
%global	fontlicense	OFL-1.1
%global	fontlicenses	COPYING
%global	fontdocs	NEWS README.md
%global	fontdocsex	%{fontlicenses}

%global	fontfamily0	Cantarell
%global	fontsummary0	Humanist sans serif font
%global	fonts0		prebuilt/Cantarell-*.otf
%global	fontsex0	prebuilt/Cantarell-VF.otf
%global	fontconfs0	%{SOURCE1}
%global	fontdescription1	%{expand:
%{common_description}

This package contains the non-variable font version of the Cantarell font.}

%global	fontfamily1	Cantarell-VF
%global	fontsummary1	Humanist sans serif font (variable)
%global	fonts1		prebuilt/Cantarell-VF.otf
%global	fontconfs1	%{SOURCE2}
%global fontdescription1	%{expand:
%{common_description}

This package contains the variable font version of the Cantarell font.}

Source0: http://download.gnome.org/sources/cantarell-fonts/0.301/cantarell-fonts-%{version}.tar.xz
Source1: 31-cantarell.conf
Source2: 31-cantarell-vf.conf

BuildRequires: gettext
BuildRequires: meson

%fontpkg -a

%prep
%autosetup -n cantarell-fonts-%{version}

%build
%meson
%meson_build
%fontbuild -a

%install
%fontinstall -a

%check
%fontcheck -a

%fontfiles -a

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 26 2022 Akira TAGOH <tagoh@redhat.com> - 0.301-7
- Add a sub-package for variable font, abattis-cantarell-vf-fonts.
  Resolves: rhbz#2045012
- Convert the spec file to the latest font packaging guidelines.

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Akira TAGOH <tagoh@redhat.com> - 0.301-5
- Drop the fontconfig config to change the binding to weak.
  This causes a trouble for languages where Cantarell doesn't cover.
  Let's simply drop and rely on applications to fallback.
  Resolves: rhbz#2013083

* Fri Dec 10 2021 Kalev Lember <klember@redhat.com> - 0.301-4
- Update upstream URL

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.301-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan  5 2021 Kalev Lember <klember@redhat.com> - 0.301-1
- Update to 0.301

* Fri Jul 31 2020 Akira TAGOH <tagoh@redhat.com> - 0.201-4
- Add the substitution rule for system-ui in fontconfig config.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.201-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.201-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Kalev Lember <klember@redhat.com> - 0.201-1
- Update to 0.201

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.111-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.111-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 0.111-1
- Update to 0.111

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 15 2018 Kalev Lember <klember@redhat.com> - 0.101-1
- Update to 0.101

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 0.100-1
- Update to 0.100
- Switch to the meson build system
- Use upstream appdata
- Validate appdata file
- Include fontconfig file in packaging as it's no longer included upstream
- Update package summary and description from appdata
- Many thanks to Parag Nemade <pnemade@fedoraproject.org> for the help
  with updating the package!

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 19 2016 Kalev Lember <klember@redhat.com> - 0.0.25-1
- Update to 0.0.25

* Tue Mar 01 2016 Richard Hughes <rhughes@redhat.com> - 0.0.24-1
- Update to 0.0.24

* Fri Feb 26 2016 Adam Williamson <awilliam@redhat.com> - 0.0.23-1
- Update to 0.0.23

* Wed Feb 17 2016 Richard Hughes <rhughes@redhat.com> - 0.0.22-1
- Update to 0.0.22

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Kalev Lember <klember@redhat.com> - 0.0.21-1
- Update to 0.0.21

* Mon Jan 11 2016 Kalev Lember <klember@redhat.com> - 0.0.20.1-1
- Update to 0.0.20.1

* Mon Nov 02 2015 Kalev Lember <klember@redhat.com> - 0.0.18-1
- Update to 0.0.18

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 0.0.17.2-1
- Update to 0.0.17.2

* Mon Oct 12 2015 Kalev Lember <klember@redhat.com> - 0.0.17.1-1
- Update to 0.0.17.1

* Mon Oct 05 2015 Kalev Lember <klember@redhat.com> - 0.0.17-2
- s: provide anchors for accents

* Sun Oct 04 2015 Kalev Lember <klember@redhat.com> - 0.0.17-1
- Update to 0.0.17

* Tue Sep 08 2015 Kalev Lember <klember@redhat.com> - 0.0.16-4
- Fix 'r' hinting
- Use upstream build system rules when regenerating otf files
- Use license macro

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 17 2014 Pravin Satpute <psatpute@redhat.com> - 0.0.16-2
- Added metainfo for gnome-software.

* Tue Sep 23 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.16-1
- Update to 0.0.16

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Sep 25 2013 Richard Hughes <rhughes@redhat.com> - 0.0.15-1
- Update to 0.0.15

* Fri Aug 23 2013 Kalev Lember <kalevlember@gmail.com> - 0.0.14-1
- Update to 0.0.14

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 20 2013 Kalev Lember <kalevlember@gmail.com> - 0.0.13-1
- Update to 0.0.13

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 20 2012 Kalev Lember <kalevlember@gmail.com> - 0.0.12-1
- Update to 0.0.12

* Tue Nov 20 2012 Richard Hughes <hughsient@gmail.com> - 0.0.11-1
- Update to 0.0.11

* Tue Sep 25 2012 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.10.1-1
- Update to 0.0.10.1

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 0.0.10-1
- Update to 0.0.10

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Richard Hughes <hughsient@gmail.com> - 0.0.9-1
- Update to 0.0.9

* Wed Mar 28 2012 Richard Hughes <hughsient@gmail.com> - 0.0.8-1
- Update to 0.0.8

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 18 2011 Matthias Clasen <mclasen@redhat.com> - 0.0.7-1
- Update to 0.0.7

* Fri Oct 07 2011 Matěj Cepl <mcepl@redhat.com> - 0.0.6-2
- Making the build EL-6 compatible.

* Wed Jul 6 2011 Matthias Clasen <mclasen@redhat.com> - 0.0.6-1
- Update to 0.0.6

* Mon Feb 21 2011 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.3-1
- Update to 0.0.3

* Fri Feb 18 2011 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.1-4
- Include upstream patch for the fontconfig snippet

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb  8 2011 Stephen Smoogen <ssmoogen@redhat.com> - 0.0.1-2
- Fixed to meet review standards

* Tue Feb  8 2011 Cosimo Cecchi <cosimoc@redhat.com> - 0.0.1-1
- Initial packaging of abattis-cantarell-fonts

