# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
%if 0%{?rhel} > 10
%bcond build_from_src 0
%else
%bcond build_from_src 1
%endif

BuildArch: noarch

%global forgeurl    https://github.com/dejavu-fonts/dejavu-fonts
Version: 2.37
%global tag         %{lua:t=string.gsub(rpm.expand("version %{version}"), "[%p%s]+", "_");print(t)}
%forgemeta

%if %{with build_from_src}
%global source_name dejavu-fonts
BuildRequires: fontforge
BuildRequires: perl-interpreter
BuildRequires: perl(Font::TTF)
BuildRequires: unicode-ucd
BuildRequires: make
%else
%global source_name dejavu-fonts-ttf
%global forgesetupargs -n %{source_name}-%{version}
%endif

Release: 29%{?dist}
# original bitstream glyphs are Bitstream Vera
# glyphs modifications by dejavu project are Public Domain
# glyphs imported from Arev fonts are under BitStream Vera compatible license
License: Bitstream-Vera AND LicenseRef-Fedora-Public-Domain
URL:     https://dejavu-fonts.github.io/

%global common_description %{expand:
The DejaVu font set is based on the “Bitstream Vera” fonts, release 1.10. Its
purpose is to provide a wider range of characters, while maintaining the
original style, using an open collaborative development process.}

%global foundry           DejaVu
%global fontlicenses      LICENSE
%global fontdocs          AUTHORS BUGS NEWS README.md

%global fontfamily1       DejaVu Sans
%global fontsummary1      DejaVu Sans, a variable-width sans-serif font family
%global fontpkgheader1    %{expand:
Obsoletes: dejavu-fonts-common < %{version}-%{release}
Obsoletes: compat-f32-dejavu-sans-fonts
Suggests:  font(dejavusansmono)
}
%if %{with build_from_src}
%global fonts1            DejaVuSans.ttf DejaVuSans-*.ttf DejaVuSansCondensed*.ttf
%else
%global fonts1            ttf/DejaVuSans.ttf ttf/DejaVuSans-*.ttf ttf/DejaVuSansCondensed*.ttf
%endif

%global fontconfs1        fontconfig/20*-dejavu-sans.conf
%global fontconfngs1      %{SOURCE11}
%global fontdescription1  %{expand:
%{common_description}

This package consists of the DejaVu sans-serif variable-width font faces, in
their unabridged version.
}

%global fontfamily2       DejaVu Serif
%global fontsummary2      DejaVu Serif, a variable-width serif font family
%global fontpkgheader2    %{expand:
Obsoletes: dejavu-math-tex-gyre-fonts < %{version}-%{release}
Obsoletes: compat-f32-dejavu-serif-fonts
}
%if %{with build_from_src}
%global fonts2            DejaVuSerif.ttf DejaVuSerif-*.ttf DejaVuSerifCondensed*.ttf DejaVuMathTeXGyre.ttf
%else
%global fonts2            ttf/DejaVuSerif.ttf ttf/DejaVuSerif-*.ttf ttf/DejaVuSerifCondensed*.ttf ttf/DejaVuMathTeXGyre.ttf
%endif
%global fontconfs2        fontconfig/20*-dejavu-serif.conf
%global fontconfngs2      %{SOURCE12}
%global fontdescription2  %{expand:
%{common_description}

This package consists of the DejaVu serif variable-width font faces, in their
unabridged version.

It includes the Mathematics extension, that was contributed to the project by
B. Jackowski, P. Strzelczyk and P. Pianowski, on behalf of TeX user groups.}

%global fontfamily3       DejaVu Sans Mono
%global fontsummary3      DejaVu Sans Mono, a mono-space sans-serif font family
%global fontpkgheader3    %{expand:
Obsoletes: compat-f32-dejavu-sans-mono-fonts
}
%if %{with build_from_src}
%global fonts3            DejaVuSansMono*.ttf
%else
%global fonts3            ttf/DejaVuSansMono*.ttf
%endif
%global fontconfs3        fontconfig/20*-dejavu-sans-mono.conf
%global fontconfngs3      %{SOURCE13}
%global fontdescription3  %{expand:
%{common_description}

This package consists of the DejaVu sans-serif mono-space font faces, in their
unabridged version.}

%global fontfamily4       DejaVu LGC Sans
%global fontsummary4      A variable-width Latin-Greek-Cyrillic sans-serif font family
%global fontpkgheader4    %{expand:
Suggests:  font(dejavusans)
}
%if %{with build_from_src}
%global fonts4            DejaVuLGCSans.ttf DejaVuLGCSans-*.ttf DejaVuLGCSansCondensed*.ttf
%global fontconfs4        fontconfig/20*-dejavu-lgc-sans.conf
%else
%global fonts4            dejavu-lgc-fonts-ttf-2.37/ttf/DejaVuLGCSans.ttf dejavu-lgc-fonts-ttf-2.37/ttf/DejaVuLGCSans-*.ttf dejavu-lgc-fonts-ttf-2.37/ttf/DejaVuLGCSansCondensed*.ttf
%global fontconfs4        dejavu-lgc-fonts-ttf-2.37/fontconfig/20*-dejavu-lgc-sans.conf
%endif
%global fontconfngs4      %{SOURCE14}
%global fontdescription4  %{expand:
%{common_description}

This package consists of the DejaVu sans-serif variable-width font faces, with
Unicode coverage restricted to Latin, Greek and Cyrillic.}

%global fontfamily5       DejaVu LGC Serif
%global fontsummary5      A variable-width Latin-Greek-Cyrillic serif font family
%global fontpkgheader5    %{expand:
Suggests:  font(dejavuserif)
}
%if %{with build_from_src}
%global fonts5            DejaVuLGCSerif.ttf DejaVuLGCSerif-*.ttf DejaVuLGCSerifCondensed*.ttf
%global fontconfs5        fontconfig/20*-dejavu-lgc-serif.conf
%else
%global fonts5            dejavu-lgc-fonts-ttf-2.37/ttf/DejaVuLGCSerif.ttf dejavu-lgc-fonts-ttf-2.37/ttf/DejaVuLGCSerif-*.ttf dejavu-lgc-fonts-ttf-2.37/ttf/DejaVuLGCSerifCondensed*.ttf
%global fontconfs5        dejavu-lgc-fonts-ttf-2.37/fontconfig/20*-dejavu-lgc-serif.conf
%endif
%global fontconfngs5      %{SOURCE15}
%global fontdescription5  %{expand:
%{common_description}

This package consists of the DejaVu serif variable-width font faces, with
Unicode coverage restricted to Latin, Greek and Cyrillic.}

%global fontfamily6       DejaVu LGC Sans Mono
%global fontsummary6      A variable-width Latin-Greek-Cyrillic mono-space font family
%global fontpkgheader6    %{expand:
Suggests:  font(dejavusansmono)
}
%if %{with build_from_src}
%global fonts6            DejaVuLGCSansMono*.ttf
%global fontconfs6        fontconfig/20*-dejavu-lgc-sans-mono.conf
%else
%global fonts6            dejavu-lgc-fonts-ttf-2.37/ttf/DejaVuLGCSansMono*.ttf
%global fontconfs6        dejavu-lgc-fonts-ttf-2.37/fontconfig/20*-dejavu-lgc-sans-mono.conf
%endif
%global fontconfngs6      %{SOURCE16}
%global fontdescription6  %{expand:
%{common_description}

This package consists of the DejaVu sans-serif mono-space font faces, with
Unicode coverage restricted to Latin, Greek and Cyrillic.}

Source0:  %{forgeurl}/archive/version_2_37/dejavu-fonts-version_2_37.tar.gz
Source1:  %{forgeurl}/releases/download/%{tag}/dejavu-fonts-ttf-%{version}.tar.bz2
Source2:  %{forgeurl}/releases/download/%{tag}/dejavu-lgc-fonts-ttf-%{version}.tar.bz2
Source11: 57-%{fontpkgname1}.xml
Source12: 57-%{fontpkgname2}.xml
Source13: 57-%{fontpkgname3}.xml
Source14: 58-%{fontpkgname4}.xml
Source15: 58-%{fontpkgname5}.xml
Source16: 58-%{fontpkgname6}.xml
Patch0:   dejavu-fonts-ttf-urn-dtd.patch
Patch1:   dejavu-lgc-fonts-ttf-urn-dtd.patch
Patch2:   dejavu-fonts-urn-dtd.patch

Name:     dejavu-fonts
Summary:  The DejaVu font families
%description
%wordwrap -v common_description

%fontpkg -a

%fontmetapkg -z 1,2,3

%global lgcmetasummary All the font packages, generated from %{source_name}, Latin-Greek-Cyrillic subset
%global lgcmetadescription %{expand:
This meta-package installs all the font packages, generated from the %{source_name}
source package, in a version restricted to coverage of Latin, Greek and
Cyrillic.
}

%fontmetapkg -n dejavu-lgc-fonts-all -s lgcmetasummary -d lgcmetadescription -z 4,5,6

%package   doc
Summary:   Optional documentation files of %{source_name}
BuildArch: noarch
%description doc
This package provides optional documentation files shipped with
%{source_name}.

%prep
%if %{with build_from_src}
%setup -n %{name}-%{tag}
%patch -P2 -p1
%else
%setup -c -T -b1 -a2 %{forgesetupargs}
%patch -P0 -p1
%patch -P1 -p1
%endif

%build
%if %{with build_from_src}
make %{?_smp_mflags} VERSION=%{version} FC-LANG="" \
     BLOCKS=/usr/share/unicode/ucd/Blocks.txt \
     UNICODEDATA=/usr/share/unicode/ucd/UnicodeData.txt \
     BUILDDIR=.
xz -9 *.txt
%endif
%fontbuild -a

%install
%fontinstall -a

%check
%if %{with build_from_src}
make check
%endif
%fontcheck -a

%fontfiles -a

%files doc
%defattr(644, root, root, 0755)
%license LICENSE
%if %{with build_from_src}
%doc *.txt.xz
%endif

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Mon Nov 03 2025 Parag Nemade <pnemade AT redhat DOT com> - 2.37-27
- Moving to use binary ttf as a Source for RHEL > 10 releases as we want
  to drop fontforge dependency from RHEL

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 12 2023 Akira TAGOH <tagoh@redhat.com> - 2.37-21
- Convert License tag to SPDX.

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.37-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 04 2020 Parag Nemade <pnemade AT redhat DOT com>
- 2.37-15
- Fix this spec file to build for F33+

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Apr 27 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.37-13
🐞 Workaround Fedora problems created by rpm commit 93604e2

* Thu Apr 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.37-12
👻 Rebuild with fonts-rpm-macros 2.0.4 to make sure fontconfig files are valid

* Mon Mar 09 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.37-7
✅ Remove F32 compatibility packages

* Mon Mar 02 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.37-6
✅ Lint, lint, lint and lint again

* Sat Feb 22 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.37-5
✅ Rebuild with fonts-rpm-macros 2.0.2

* Sat Feb 15 2020 Nicolas Mailhot <nim@fedoraproject.org>
- 2.27-4
✅ Convert to fonts-rpm-macros use
✅ Merge math extension into serif

* Sat Feb 19 2005 Nicolas Mailhot <nim@fedoraproject.org>
- 1.7-1
✅ initial build – using vera as template
