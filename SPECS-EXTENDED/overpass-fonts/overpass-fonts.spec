Vendor:         Microsoft Corporation
Distribution:   Mariner
%global fontname overpass
%global fontconf 60-%{fontname}.conf
%global monofontconf 60-%{fontname}-mono.conf

Name:		%{fontname}-fonts
Version:	3.0.4
Release:	4%{?dist}
Summary:	Typeface based on the U.S. interstate highway road signage type system
License:	OFL or LGPLv2+
URL:		https://github.com/RedHatBrand/overpass/
Source0:	https://github.com/RedHatBrand/Overpass/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:	%{name}-fontconfig.conf
Source2:	%{fontname}.metainfo.xml
Source3:	%{fontname}-mono-fonts-fontconfig.conf
Source4:	%{fontname}-mono.metainfo.xml

BuildArch:	noarch
BuildRequires:	fontpackages-devel
Requires:	fontpackages-filesystem

%description
Free and open source typeface based on the U.S. interstate highway road signage
type system; it is sans-serif and suitable for both body and titling text.

%package -n %{fontname}-mono-fonts
Summary:	Monospace version of overpass fonts

%description -n %{fontname}-mono-fonts
Free and open source typeface based on the U.S. interstate highway road signage
type system. This is the monospace family variant.

%prep
%setup -q -n Overpass-%{version}

%build
# Nothing to do here.

%install
install -m 0755 -d %{buildroot}%{_fontdir}

install -m 0644 -p desktop-fonts/overpass*/*.otf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
		%{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} \
		%{buildroot}%{_fontconfig_templatedir}/%{fontconf}

install -m 0644 -p %{SOURCE3} \
		%{buildroot}%{_fontconfig_templatedir}/%{monofontconf}

ln -s %{_fontconfig_templatedir}/%{fontconf} \
		%{buildroot}%{_fontconfig_confdir}/%{fontconf}

ln -s %{_fontconfig_templatedir}/%{monofontconf} \
                %{buildroot}%{_fontconfig_confdir}/%{monofontconf}

# I do not think this is useful to package, but if it is...
%if 0
mkdir -p %{buildroot}/usr/lib/node_modules/overpass/
cp -a bower.json package.json %{buildroot}/usr/lib/node_modules/overpass/
%endif

# Add AppStream metadata
install -Dm 0644 -p %{SOURCE2} \
	%{buildroot}%{_datadir}/appdata/%{fontname}.metainfo.xml

install -Dm 0644 -p %{SOURCE4} \
        %{buildroot}%{_datadir}/appdata/%{fontname}-mono.metainfo.xml

%_font_pkg -f %{fontconf} overpass-bold*.otf overpass-extra*.otf overpass-heavy*.otf overpass-italic*.otf overpass-light*.otf overpass-regular*.otf overpass-semibold*.otf overpass-thin*.otf
%doc README.md overpass-specimen.pdf
%license LICENSE.md
%{_datadir}/appdata/%{fontname}.metainfo.xml
%if 0
/usr/lib/node_modules/overpass/
%endif

%_font_pkg -n overpass-mono -f %{monofontconf} overpass-mono-*.otf
%doc README.md overpass-mono-specimen.pdf
%license LICENSE.md
%{_datadir}/appdata/%{fontname}-mono.metainfo.xml

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec  6 2019 Tom Callaway <spot@fedoraproject.org> - 3.0.4-2
- fix incorrect fontconfig file (thanks to lazybvr)

* Tue Nov 26 2019 Tom Callaway <spot@fedoraproject.org> - 3.0.4-1
- update to 3.0.4

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Tom Callaway <spot@fedoraproject.org> - 3.0.3-1
- update to 3.0.3

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun  1 2017 Tom Callaway <spot@fedoraproject.org> - 3.0.2-1
- update to 3.0.2
- move to otf files

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 16 2016 Tom Callaway <spot@fedoraproject.org> - 3.0-1
- update to 3.0
- add mono subpackage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Pravin Satute <psatute AT redhat DOT com> - 2.1-1
- Upstream new release with ttfautohint
- Changed url to https://github.com/RedHatBrand/overpass/, https://overpassfont.org looks dead.

* Tue Aug 25 2015 Tom Callaway <spot@fedoraproject.org> - 1.01-11
- update to new overpass fonts (they now claim to be 1.000, but we're not going backwards)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 03 2014 Parag Nemade <pnemade AT redhat DOT com> - 1.01-9
- Fix metainfo file error (rh#1159700)

* Sat Oct 18 2014 Parag Nemade <pnemade AT redhat DOT com> - 1.01-8
- Add metainfo file to show this font in gnome-software

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Feb 12 2014 Tom Callaway <spot@fedoraproject.org> - 1.01-6
- add Light variant font

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.01-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Dec 11 2012 Tom Callaway <spot@fedoraproject.org>
- License is now OFL or ASL 2.0

* Mon Sep 24 2012 Tom Callaway <spot@fedoraproject.org> - 1.01-2
- fix spaces vs tabs issue

* Mon Aug 27 2012 Tom Callaway <spot@fedoraproject.org> - 1.01-1
- initial package
