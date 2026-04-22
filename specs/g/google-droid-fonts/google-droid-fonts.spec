# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
BuildArch: noarch

# No sane versionning upstream, use git clone timestamp
Version: 20200215
Release: 24%{?dist}
License: Apache-2.0
URL:     https://android.googlesource.com/

%global source_name       google-droid-fonts

%global foundry           Google
%global fontlicenses      NOTICE
%global fontdocs          *.txt

%global common_description %{expand:
The Droid font family was designed in the fall of 2006 by Ascender’s Steve
Matteson, as a commission from Google to create a set of system fonts for its
Android platform. The goal was to provide optimal quality and comfort on a
mobile handset when rendered in application menus, web browsers and for other
screen text.

The family was later extended in collaboration with other designers such as
Pascal Zoghbi of 29ArabicLetters.}

%global fontfamily1       Droid Sans
%global fontsummary1      Droid Sans, a humanist sans-serif font family
%global fontpkgheader1   %{expand:
Obsoletes: google-droid-kufi-fonts < %{version}-%{release}
Suggests: font(notosans)
}
%global fonts1            DroidSans*ttf DroidKufi*ttf
%global fontsex1          DroidSansMono*ttf DroidSansFallback.ttf DroidSansHebrew.ttf
%global fontconfs1      %{SOURCE11} %{SOURCE14} %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24}
%global fontdescription1  %{expand:
%{common_description}

Droid Sans is a humanist sans serif font family designed for user interfaces and electronic communication.

The Arabic block was initially designed by Steve Matteson of Ascender under the
Droid Kufi name, with consulting by Pascal Zoghbi of 29ArabicLetters to
finalize the font family.}

%global fontfamily2       Droid Sans Mono
%global fontsummary2      Droid Sans Mono, a humanist mono-space sans-serif font family
%global fontpkgheader2    %{expand:
Suggests: font(notosansmono)
}
%global fonts2            DroidSansMono*ttf
%global fontconfs2      %{SOURCE12}
%global fontdescription2  %{expand:
%{common_description}

Droid Sans Mono is a humanist mono-space sans serif font family designed for
user interfaces and electronic communication.}

%global fontfamily3       Droid Serif
%global fontsummary3      Droid Serif, a contemporary serif font family
%global fontpkgheader3    %{expand:
Suggests: font(notoserif)
}
%global fonts3            DroidSerif*ttf DroidNaskh*ttf
%global fontsex3          DroidNaskhUI-Regular.ttf DroidNaskh-Regular-Shift.ttf
%global fontconfs3      %{SOURCE13} %{SOURCE15}
%global fontdescription3  %{expand:
%{common_description}

Droid Serif is a contemporary serif typeface family designed for comfortable
reading on screen. Droid Serif is slightly condensed to maximize the amount of
text displayed on small screens. Vertical stress and open forms contribute to
its readability while its proportion and overall design complement its
companion Droid Sans.

The Arabic block was designed by Pascal Zoghbi of 29ArabicLetters under the
Droid Naskh name.}

%global archivename google-droid-fonts-%{version}
%global googledroid google-droid
%global googledroidsans %{googledroid}-sans


Source0:  %{archivename}.tar.xz
# Brutal script used to pull sources from upstream git
# Needs at least 2 Gib of space in /var/tmp
Source1:  getdroid.sh
Source11: 66-%{fontpkgname1}.conf
Source12: 60-%{fontpkgname2}.conf
Source13: 66-%{fontpkgname3}.conf
Source14: 69-%{googledroid}-arabic-kufi-fonts.conf
Source15: 69-%{googledroid}-arabic-naskh-fonts.conf
Source16: 69-%{googledroidsans}-armenian-fonts.conf
Source17: 69-%{googledroidsans}-devanagari-fonts.conf
Source18: 69-%{googledroidsans}-ethiopic-fonts.conf
Source19: 69-%{googledroidsans}-georgian-fonts.conf
Source20: 69-%{googledroidsans}-hebrew-fonts.conf
Source21: 69-%{googledroidsans}-japanese-fonts.conf
Source22: 69-%{googledroidsans}-tamil-fonts.conf
Source23: 69-%{googledroidsans}-thai-fonts.conf
Source24: 69-%{googledroidsans}-fallback-fonts.conf

Name:     google-droid-fonts
Summary:  A set of general-purpose font families released by Google as part of Android
%description
%wordwrap -v common_description

%fontpkg -a

%fontmetapkg

%prep
%setup -q -n %{archivename}

%build
%fontbuild -a

%install
%fontinstall -a

%check
%fontcheck -a

%fontfiles -a

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jul 11 2024 Akira TAGOH <tagoh@redhat.com> - 20200215-20
- Fix missing config files

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 28 2023 Akira TAGOH <tagoh@redhat.com> - 20200215-16
- Convert License tag to SPDX.

* Wed May 10 2023 Akira TAGOH <tagoh@redhat.com> - 20200215-15
- Drop the font unification which causes a lot of problems.
  Resolves: rhbz#2186711, rhbz#2144373, rhbz#2096153, rhbz#517789

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 28 2022 Akira TAGOH <tagoh@redhat.com> - 20200215-12
- Adjust a number of the priority for fontconfig config.
  because 65 is supposed to be the default fonts for non-Latin languages.
  Resolves: rhbz#1938205, rhbz#1571522
- Drop fallback config for Noto Sans.
  This breaks some languages which Droid Sans Fallback can covers.
  This is also required for https://fedoraproject.org/wiki/Changes/DefaultToNotoFonts
  Resolves: rhbz#1820166

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20200215-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Parag Nemade <pnemade AT redhat DOT com>
- 20200215-8
- Fix this spec file to build for F33+

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 27 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 20200215-6
🐞 Workaround Fedora problems created by rpm commit 93604e2

* Thu Apr 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 20200215-5
💥 Actually rebuild with fonts-rpm-macros 2.0.4 to make sure fontconfig files are
  valid

* Thu Apr 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 20200215-4
👻 Rebuild with fonts-rpm-macros 2.0.4 to make sure fontconfig files are valid

* Mon Mar 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 20200215-3
✅ Lint, lint, lint and lint again

* Sat Feb 22 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 20200215-2
✅ Rebuild with fonts-rpm-macros 2.0.2

* Sat Feb 15 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 20200215-1
✅ Convert to fonts-rpm-macros use

* Sun Nov 23 2008 Nicolas Mailhot <nim@fedoraproject.org>
- 1.0.107-1
✅ Initial packaging
