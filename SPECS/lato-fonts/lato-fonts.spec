%global fontname lato
%global fontconf 61-%{fontname}.conf

Summary:        A sanserif typeface family
Name:           %{fontname}-fonts
Version:        2.015
Release:        11%{?dist}
License:        OFL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.latofonts.com/
# Fonts retrieved 2015-08-07.
Source0:        https://www.latofonts.com/download/Lato2OFL.zip#/%{name}-%{version}.zip
Source1:        %{name}-fontconfig.conf
Source2:        %{fontname}.metainfo.xml

BuildArch:      noarch

BuildRequires:  fontpackages-devel

Requires:       fontpackages-filesystem

Obsoletes:      google-lato-fonts < 1.014-1
Provides:       google-lato-fonts = %{version}-%{release}

%description
Lato is a sanserif typeface family designed in the Summer 2010 by Warsaw-based
designer Łukasz Dziedzic ("Lato" means "Summer" in Polish). In December 2010 the
Lato family was published under the open-source Open Font License by his foundry
tyPoland, with support from Google.

When working on Lato, Łukasz tried to carefully balance some potentially
conflicting priorities. He wanted to create a typeface that would seem quite
"transparent" when used in body text but would display some original treats when
used in larger sizes. He used classical proportions (particularly visible in the
uppercase) to give the letterforms familiar harmony and elegance. At the same
time, he created a sleek sanserif look, which makes evident the fact that Lato
was designed in 2010 - even though it does not follow any current trend.

The semi-rounded details of the letters give Lato a feeling of warmth, while the
strong structure provides stability and seriousness. "Male and female, serious
but friendly. With the feeling of the Summer," says Łukasz.

Lato consists of nine weights (plus corresponding italics), including a
beautiful hairline style. It covers 2300+ glyphs per style and supports 100+
Latin-based languages, 50+ Cyrillic-based languages as well as Greek and IPA
phonetics.

%prep
%setup -q -c

# Fix wrong end-of-lines encoding
sed "s/\r//" Lato2OFL/OFL.txt > Lato2OFL/OFL.txt.new
touch -r Lato2OFL/OFL.txt Lato2OFL/OFL.txt.new
mv Lato2OFL/OFL.txt.new Lato2OFL/OFL.txt

# Fix permissions
chmod 0644 Lato2OFL/{OFL.txt,README.txt}

%build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p Lato2OFL/*.ttf %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE1} %{buildroot}%{_fontconfig_templatedir}/%{fontconf}
ln -s %{_fontconfig_templatedir}/%{fontconf} %{buildroot}%{_fontconfig_confdir}/%{fontconf}

# Add AppStream metadata
install -Dm 0644 -p %{SOURCE2} \
        %{buildroot}%{_datadir}/appdata/%{fontname}.metainfo.xml

%_font_pkg -f %{fontconf} *.ttf
%doc Lato2OFL/README.txt
%license Lato2OFL/OFL.txt
%{_datadir}/appdata/%{fontname}.metainfo.xml


%changelog
* Mon Dec 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.015-11
- License verified.
- Back to using %%_font_pkg.

* Tue Feb 09 2021 Joe Schmitt <joschmit@microsoft.com> - 2.015-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Define %%files section when %%_font_pkg is not defined

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.015-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 07 2015 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.015-1
- Update to 2.015

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.010-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 15 2014 Richard Hughes <richard@hughsie.com> - 2.010-2
- Add a MetaInfo file for the software center; this is a font we want to show.

* Thu Sep 04 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.010-1
- Update to 2.010

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.007-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 02 2014 Mohamed El Morabity <melmorabity@fedoraproject.org> - 2.007-1
- Update to 2.007

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 06 2013 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.105-1
- Update to 1.105

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.014-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Sep 29 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.014-2
- Drop useless Buildroot cleaning

* Sun Sep 23 2012 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.014-1
- Initial release, to replace google-lato-fonts package
