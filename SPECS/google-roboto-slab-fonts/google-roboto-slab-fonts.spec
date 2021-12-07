%global fontconf 64-%{fontname}
%global fontname google-roboto-slab

Summary:        Google Roboto Slab fonts
Name:           google-roboto-slab-fonts
Version:        1.100263
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.google.com/fonts/specimen/Roboto+Slab
# Fonts archive retrieved on 2021-12-06.
Source0:        https://fonts.google.com/download?family=Roboto%20Slab#/%{name}-%{version}.zip
Source5:        %{fontname}-fontconfig.conf
Source6:        %{fontname}.metainfo.xml

BuildArch:      noarch

BuildRequires:  fontpackages-devel
BuildRequires:  unzip

%description
Roboto has a dual nature. It has a mechanical skeleton and the forms are
largely geometric. At the same time, the font features friendly and open
curves. While some grotesks distort their letterforms to force a rigid
rhythm, Roboto doesn't compromise, allowing letters to be settled into
their natural width. This makes for a more natural reading rhythm more
commonly found in humanist and serif types.

This is the Roboto Slab family, which can be used alongside the normal
Roboto family and the Roboto Condensed family.

%prep
unzip %{SOURCE0}

%build
# nothing to build here

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p RobotoSlab-*.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}
install -m 0644 -p %{SOURCE5} \
         %{buildroot}%{_fontconfig_templatedir}/%{fontconf}-fontconfig.conf
ln -s %{_fontconfig_templatedir}/%{fontconf}-fontconfig.conf \
      %{buildroot}%{_fontconfig_confdir}/%{fontconf}-fontconfig.conf

install -m 0755 -d %{buildroot}%{_datadir}/appdata
install -m 0644 -p %{SOURCE6} %{buildroot}%{_datadir}/appdata

%_font_pkg -f %{fontconf}-fontconfig.conf RobotoSlab-*.ttf
%{_datadir}/appdata/%{fontname}.metainfo.xml
%license LICENSE.txt

%changelog
* Mon Dec 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.100263-2
- License verified.
- Switched to using an official zip archive instead of checked-in files.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.100263-1
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Tue Feb 09 2021 Joe Schmitt <joschmit@microsoft.com> - 1.100263-0.12.20150923git
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Define %%files section when %%_font_pkg is not defined

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.11.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.10.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.9.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.8.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.7.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.6.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.5.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.100263-0.4.20150923git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 23 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.100263-0.3.20150923git
- Follow https://fedoraproject.org/wiki/Packaging:SourceURL#Commit_Revision

* Wed Sep 23 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.100263-0.2.20150923
- Fix metainfo file validation by adding <p> </p>
- use %%license macro

* Wed Sep 23 2015 Parag Nemade <pnemade AT redhat DOT com> - 1.100263-0.1.20150923
- Initial package
