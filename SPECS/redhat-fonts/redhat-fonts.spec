# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global fontname redhat
%global fontconf 64-%{fontname}
%global asfontname com.redhat.%{fontname}

%global projname RedHatFont

%global desc \
Red Hat Typeface is a fresh take on the geometric sans genre, \
taking inspiration from a range of American sans serifs \
including Tempo and Highway Gothic. \
 \
The Display styles, made for headlines and big statements, \
are low contrast and spaced tightly, with a large x-height and open counters. \
 \
The Text styles have a slightly smaller x-height and narrower width \
for better legibility, are spaced more generously, and have thinned joins \
for better performance at small sizes. \
 \
The Mono styles are similar to the Text styles, but are adapted \
for better performance to render code and similar text. \
 \
The three families can be used together seamlessly at a range of sizes. \
 \
The fonts were originally commissioned by Paula Scher / Pentagram \
and designed by Jeremy Mickel / MCKL for the new Red Hat identity.

Name:           %{fontname}-fonts
Version:        4.1.0
Release:        2%{?dist}
Summary:        Red Hat Typeface fonts
# Only the metainfo files are CC-BY-SA
License:        OFL-1.1-RFN AND CC-BY-SA-4.0
URL:            https://github.com/RedHatOfficial/%{projname}

Source0:        %{url}/archive/%{version}/%{projname}-%{version}.tar.gz
Source1:        %{fontconf}-display-fontconfig.conf
Source2:        %{fontconf}-text-fontconfig.conf
Source3:        %{fontconf}-mono-fontconfig.conf
Source4:        %{fontconf}-display-vf-fontconfig.conf
Source5:        %{fontconf}-text-vf-fontconfig.conf
Source6:        %{fontconf}-mono-vf-fontconfig.conf

BuildArch:      noarch
BuildRequires:  %{_bindir}/appstream-util
BuildRequires:  fontpackages-devel

%description %{desc}


%package -n %{fontname}-display-fonts
Summary:        Red Hat Display fonts
Requires:       fontpackages-filesystem

%description -n %{fontname}-display-fonts %{desc}

This package provides the Display fonts variant.

%package -n %{fontname}-text-fonts
Summary:        Red Hat Text fonts
Requires:       fontpackages-filesystem

%description -n %{fontname}-text-fonts %{desc}

This package provides the Text fonts variant.

%package -n %{fontname}-mono-fonts
Summary:        Red Hat Mono fonts
Requires:       fontpackages-filesystem

%description -n %{fontname}-mono-fonts %{desc}

This package provides the Monospace fonts variant.

%package -n %{fontname}-display-vf-fonts
Summary:        The variable font of Red Hat Display fonts
Requires:       fontpackages-filesystem
Provides:	font(redhatdisplayvf)

%description -n %{fontname}-display-vf-fonts %{desc}

This package provides the variable font version of the Display fonts variant.

%package -n %{fontname}-text-vf-fonts
Summary:        The variable font of Red Hat Text fonts
Requires:       fontpackages-filesystem
Provides:	font(redhattextvf)

%description -n %{fontname}-text-vf-fonts %{desc}

This package provides the variable font version of the Text fonts variant.

%package -n %{fontname}-mono-vf-fonts
Summary:        The Variable font of Red Hat Mono fonts
Requires:       fontpackages-filesystem
Provides:	font(redhatmonovf)

%description -n %{fontname}-mono-vf-fonts %{desc}

This package provides the variable font version of the Monospace fonts variant.

%prep
%autosetup -n %{projname}-%{version} -p1


%build
# Nothing to build

%install

# Install fonts
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0755 -d %{buildroot}%{_fontdir}-vf
## Mono
install -m 0644 -p fonts/Mono/otf/*.otf %{buildroot}%{_fontdir}
## Mono VF
install -m 0644 -p fonts/Mono/variable/*.ttf %{buildroot}%{_fontdir}-vf
## Display/Text
install -m 0644 -p fonts/Proportional/*/otf/*.otf %{buildroot}%{_fontdir}
## Display/Text VF
install -m 0644 -p fonts/Proportional/*/variable/*.ttf %{buildroot}%{_fontdir}-vf

# Drop duplicate
rm -f %{buildroot}%{_fontdir}-vf/*VF*.ttf
# workaround to address crash issue/unexpected italic rendering with variable fonts
rm -f %{buildroot}%{_fontdir}-vf/*-Italic*.ttf

# Install fontconfig data
install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-display.conf
install -m 0644 -p %{SOURCE2} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-text.conf
install -m 0644 -p %{SOURCE3} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono.conf

install -m 0644 -p %{SOURCE4} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-display-vf.conf
install -m 0644 -p %{SOURCE5} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-text-vf.conf
install -m 0644 -p %{SOURCE6} \
        %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-mono-vf.conf

for fconf in %{fontconf}-display %{fontconf}-text %{fontconf}-mono; do
  ln -s %{_fontconfig_templatedir}/${fconf}.conf %{buildroot}%{_fontconfig_confdir}/${fconf}.conf
  ln -s %{_fontconfig_templatedir}/${fconf}-vf.conf %{buildroot}%{_fontconfig_confdir}/${fconf}-vf.conf
done

# Install AppStream metadata
install -m 0755 -d %{buildroot}%{_datadir}/metainfo
for f in metainfo/*.metainfo.xml; do
    sed -e 's/\(com\.redhat\..*\)</\1-vf</' $f > ${f/.metainfo.xml/-vf.metainfo.xml}
    touch -r $f ${f/.metainfo.xml/-vf.metainfo.xml}
done
install -m 0644 -p metainfo/*.metainfo.xml %{buildroot}%{_datadir}/metainfo

%check
# Validate AppStream metadata
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.metainfo.xml


%_font_pkg -n display -f %{fontconf}-display.conf RedHatDisplay*.otf
%license LICENSE metainfo/LICENSE-METAINFO
%doc README.md CHANGELOG.md *.png
%{_datadir}/metainfo/%{asfontname}-display.metainfo.xml

%_font_pkg -n text -f %{fontconf}-text.conf RedHatText*.otf
%license LICENSE metainfo/LICENSE-METAINFO
%doc README.md CHANGELOG.md *.png
%{_datadir}/metainfo/%{asfontname}-text.metainfo.xml

%_font_pkg -n mono -f %{fontconf}-mono.conf RedHatMono*.otf
%license LICENSE metainfo/LICENSE-METAINFO
%doc README.md CHANGELOG.md *.png
%{_datadir}/metainfo/%{asfontname}-mono.metainfo.xml

%global _fontdir %{_fontdir}-vf

%_font_pkg -n display-vf -f %{fontconf}-display-vf.conf RedHatDisplay*.ttf
%license LICENSE metainfo/LICENSE-METAINFO
%doc README.md CHANGELOG.md *.png
%{_datadir}/metainfo/%{asfontname}-display-vf.metainfo.xml

%_font_pkg -n text-vf -f %{fontconf}-text-vf.conf RedHatText*.ttf
%license LICENSE metainfo/LICENSE-METAINFO
%doc README.md CHANGELOG.md *.png
%{_datadir}/metainfo/%{asfontname}-text-vf.metainfo.xml

%_font_pkg -n mono-vf -f %{fontconf}-mono-vf.conf RedHatMono*.ttf
%license LICENSE metainfo/LICENSE-METAINFO
%doc README.md CHANGELOG.md *.png
%{_datadir}/metainfo/%{asfontname}-mono-vf.metainfo.xml


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Mar  7 2025 Akira TAGOH <tagoh@redhat.com> - 4.1.0-1
- New upstream release.
  Resolves: rhbz#2350415

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 21 2024 Akira TAGOH <tagoh@redhat.com> - 4.0.3-13
- Remove Italic variable fonts to workaround a crash issue
  and unexpected italic rendering.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun  4 2024 Akira TAGOH <tagoh@redhat.com> - 4.0.3-11
- Add a provide line of font(redhatdisplayvf), font(redhattextvf),
  and font(redhatmonovf) to each sub-packages for backward compatibility.
- Fix invalid License field.

* Mon May 27 2024 Akira TAGOH <tagoh@redhat.com> - 4.0.3-9
- Fix wrong comment in conf.

* Tue May 14 2024 Akira TAGOH <tagoh@redhat.com> - 4.0.3-8
- Use no VF in family name version of ttf for -vf packages.
- Adjust properties in VF to avoid confusion.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 01 2023 Akira TAGOH <tagoh@redhat.com> - 4.0.3-5
- Split packages for variable fonts.
- Drop unnecessary/duplicate fonts from packages.
- Worked around broken family name in variable fonts.

* Wed Aug 09 2023 Parag Nemade <pnemade AT redhat DOT com> - 4.0.3-4
- Use SPDX license expression

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 03 2022 Neal Gompa <ngompa@fedoraproject.org> - 4.0.3-1
- Update to 4.0.3 (RH#1955487)

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Apr 23 2021 Neal Gompa <ngompa13@gmail.com> - 4.0.1-1
- Rebase to 4.0.1 (RH#1917996)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jul 29 2019 Neal Gompa <ngompa13@gmail.com> - 2.3.2-1
- Update to 2.3.2
- Fix typos in the changelog

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Ben Cotton <bcotton@fedoraproject.org> - 2.2.0-2
- Add TrueType font files (RHBZ #1709922)

* Sun May  5 2019 Neal Gompa <ngompa13@gmail.com> - 2.2.0-1
- Initial packaging
