# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global fontname fontawesome4
%global fontconf 60-fontawesome.conf
%global _fontdir %{_fontbasedir}/fontawesome

Name:		fontawesome4-fonts
Epoch:		1
Version:	4.7.0
Release:	25%{?dist}

Summary:	Iconic font set
License:	OFL-1.1-RFN
URL:		http://fontawesome.io
Source0:	http://fontawesome.io/assets/font-awesome-%{version}.zip
Source1:	%{name}-fontconfig.conf
Source2:	README-Trademarks.txt
BuildArch:	noarch
BuildRequires:	fontpackages-devel
BuildRequires:	ttembed
Requires:	fontpackages-filesystem

# This can be removed when F42 reaches EOL
Obsoletes:      fontawesome-fonts < 1:4.7.0-16
Provides:       fontawesome-fonts = 1:%{version}-%{release}

%description
Font Awesome gives you scalable vector icons that can instantly be
customized — size, color, drop shadow, and anything that can be done with the
power of CSS.

This package contains OpenType and TrueType font files which are typically used
locally.

%package web
License:	OFL-1.1-RFN AND MIT
Requires:	%{fontname}-fonts = %{?epoch:%{epoch}:}%{version}-%{release}
Summary:	Iconic font set, web files

%description web
Font Awesome gives you scalable vector icons that can instantly be
customized — size, color, drop shadow, and anything that can be done with the
power of CSS.

This package contains CSS, SCSS and LESS style files as well as Web Open Font
Format versions 1 and 2, Embedded OpenType and SVG font files which are
typically used on the web.

%prep
%autosetup -n font-awesome-%{version}
cp -p %SOURCE2 .

%build
ttembed fonts/*.ttf fonts/*.otf

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.ttf fonts/*.otf fonts/*.woff fonts/*.svg \
		fonts/*.woff2 fonts/*.eot %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
		%{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
		%{buildroot}%{_fontconfig_templatedir}/%{fontconf}

ln -s %{_fontconfig_templatedir}/%{fontconf} \
		%{buildroot}%{_fontconfig_confdir}/%{fontconf}

mkdir -p %{buildroot}%{_datadir}/font-awesome-web/
cp -a css less scss %{buildroot}%{_datadir}/font-awesome-web/

# files:
%_font_pkg -f %{fontconf} *.ttf *.otf
%exclude %{_fontdir}/fontawesome-webfont.svg
%exclude %{_fontdir}/fontawesome-webfont.woff
%exclude %{_fontdir}/fontawesome-webfont.woff2
%exclude %{_fontdir}/fontawesome-webfont.eot

%doc README-Trademarks.txt

%files web
%{_datadir}/font-awesome-web/
%{_fontdir}/fontawesome-webfont.svg
%{_fontdir}/fontawesome-webfont.woff
%{_fontdir}/fontawesome-webfont.woff2
%{_fontdir}/fontawesome-webfont.eot

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 20 2024 Jerry James <loganjerry@gmail.com> - 1:4.7.0-22
- Fix SPDX expression in web subpackage

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Jerry James <loganjerry@gmail.com> - 1:4.7.0-19
- Obsolete the fontawesome-fonts package (bz 2239785)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 10 2023 Jerry James <loganjerry@gmail.com> - 1:4.7.0-17
- Move fonts back to /usr/share/fonts/fontawesome

* Fri Feb 24 2023 Jerry James <loganjerry@gmail.com> - 1:4.7.0-16
- Name change to fontawesome4-fonts
- Convert License tags to SPDX

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Miro Hrončok <mhroncok@redhat.com> - 1:4.7.0-9
- Add epoch to inter-subpackages requirement

* Wed Jul 08 2020 Fabio Alessandro Locati <fale@fedoraproject.org> - 1:4.7.0-8
- Rollback to FA4

* Tue Jul 07 2020 Fabio Alessandro Locati <fale@fedoraproject.org> - 5.13.1-2
- Provide the right font configuration
- Drop ttf format since upstream affirms that otf is to be preferred

* Sun Jul 05 2020 Fabio Alessandro Locati <fale@fedoraproject.org> - 5.13.1-1
- Update to 5.13.1

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Oct 27 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0

* Sun May 22 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 4.6.3-1
- Update to 4.6.3
- Update the brand icons list using the script

* Thu May 05 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 4.6.2-1
- Update to 4.6.1
- Update the brand icons list using a new script
- Add the script to create brand icons list

* Wed Apr 13 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 4.6.1-1
- Update to 4.6.0
- Update the brand list with the icons new in 4.6.0

* Tue Mar 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 4.5.0-1
- Update to 4.5.0
- Update the brand list with the icons new in 4.5.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 04 2015 Nils Philippsen <nils@redhat.com> - 4.4.0-2
- include .eot files
- amend -web license and summary, and descriptions

* Thu Sep 17 2015 Matthias Runge <mrunge@redhat.com> - 4.4.0-1
- update to 4.4.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 04 2014 Matthias Runge <mrunge@redhad.com> - 4.1.0-2
- include .woff and .svg files (rhbz#1110646)

* Tue Jul 08 2014 Petr Vobornik <pvoborni@redhat.com> - 4.1.0-1
- update to version 4.1.0
- renamed web packaged dir from font-awesome-$version to font-awesome-web

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 02 2014 Petr Vobornik <pvoborni@redhat.com> - 4.0.3-1
- embeddable flag set to installable by ttembed
- web package license updated to MIT
- README-Trademarks.txt added

* Mon Nov 04 2013 Ryan Lerch <ryanlerch@fedoraproject.org> - 4.0.3-0
- initial package based off spot's package
