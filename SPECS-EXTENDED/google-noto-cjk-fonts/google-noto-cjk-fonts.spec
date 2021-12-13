%global commit0 be6c059ac1587e556e2412b27f5155c8eb3ddbe6
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%global fontname google-noto-cjk
%global fontconf google-noto
%global fontconf2 65-%{fontconf}-cjk-fonts.conf

%global common_desc \
Noto CJK fonts, supporting Simplified Chinese, Traditional Chinese, \
Japanese, and Korean. The supported scripts are Han, Hiragana, Katakana, \
Hangul, and Bopomofo. Latin, Greek, Cyrllic, and various symbols are also \
supported for compatibility with CJK standards. \
%{nil}

Name:           google-noto-cjk-fonts
Version:        20190416
Release:        7%{?dist}
Summary:        Google Noto Sans CJK Fonts

License:        OFL
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/googlei18n/noto-cjk
Source0:        https://github.com/googlei18n/noto-cjk/archive/%{commit0}.tar.gz#/noto-cjk-%{shortcommit0}.tar.gz
Source1:        genfontconf.py
Source2:        genfontconf.sh
Source3:        %{fontconf2}

BuildArch:      noarch
BuildRequires:  fontpackages-devel
BuildRequires:  python3
BuildRequires:  /usr/bin/xmllint
Requires:       fontpackages-filesystem
Requires:       google-noto-sans-cjk-ttc-fonts
Requires:       google-noto-serif-cjk-ttc-fonts



Obsoletes:      google-noto-sans-cjk-fonts < 20150617
Provides:       google-noto-sans-cjk-fonts = 20150617

# notocjkrep Package Name
%define notocjkrep(:)\
%define pname %(echo %{*} | tr "A-Z " "a-z-")\
Obsoletes:      google-noto-%{pname}-fonts < 20150617\
Provides:       google-noto-%{pname}-fonts = 20150617\
Obsoletes:      google-noto-cjk-%{pname}-fonts < %{version}-%{release}\
Provides:       google-noto-cjk-%{pname}-fonts = %{version}-%{release}\


%notocjkrep Sans Simplified Chinese
%notocjkrep Sans Traditional Chinese
%notocjkrep Sans Japanese
%notocjkrep Sans Korean




%description
%common_desc

%package common
Summary:        Common files for Noto CJK fonts

%description common
%common_desc

Common files for Google Noto CJK fonts.


# notocjkpkg [-n sub-package-name] [-f font-file] [-p priority] Font Name
# -n sub package name
# -f font file name
# -p overrides fontconfig .conf priority (default 66)
%define notocjkpkg(n:f:p:) \
# override _font_pkg_name to avoid name changes in _font_pkg \
%define _font_pkg_name() %1 \
%define subpkgname %{-n:%{-n*}} \
%define fontfiles %{-f:%{-f*}}\
%define fconf %{-p*}%{!-p:66}-%{fontconf}-%{subpkgname}.conf\
%package -n     google-noto-%subpkgname-fonts \
Summary:        %* font files for %{name} \
Requires:       %{name}-common = %{version}-%{release} \
\
%description -n google-noto-%subpkgname-fonts \
%common_desc \
\
The google-noto-%subpkgname-fonts package contains %* fonts. \
\
%if 0%{?_font_pkg:1} \
%_font_pkg -n google-noto-%subpkgname-fonts -f %{fconf} %fontfiles \
%else \
%files -n google-noto-%subpkgname-fonts \
%endif \
\
%{nil}


%notocjkpkg -n sans-cjk-ttc -f NotoSansCJK-*.ttc -p 65-0 Sans OTC


%notocjkpkg -n serif-cjk-ttc -f NotoSerifCJK-*.ttc -p 65-0 Serif OTC


%notocjkpkg -n sans-cjk-jp -f NotoSansCJKjp-*.otf Japanese Multilingual Sans OTF


%notocjkpkg -n serif-cjk-jp -f NotoSerifCJKjp-*.otf Japanese Multilingual Serif OTF


%notocjkpkg -n sans-mono-cjk-jp -f NotoSansMonoCJKjp-*.otf Japanese Multilingual Sans Mono OTF


%notocjkpkg -n sans-cjk-kr -f NotoSansCJKkr-*.otf Korean Multilingual Sans OTF


%notocjkpkg -n serif-cjk-kr -f NotoSerifCJKkr-*.otf Korean Multilingual Serif OTF


%notocjkpkg -n sans-mono-cjk-kr -f NotoSansMonoCJKkr-*.otf Korean Multilingual Sans Mono OTF


%notocjkpkg -n sans-cjk-sc -f NotoSansCJKsc-*.otf Simplified Chinese Multilingual Sans OTF


%notocjkpkg -n serif-cjk-sc -f NotoSerifCJKsc-*.otf Simplified Chinese Multilingual Serif OTF


%notocjkpkg -n sans-mono-cjk-sc -f NotoSansMonoCJKsc-*.otf Simplified Chinese Multilingual Sans Mono OTF


%notocjkpkg -n sans-cjk-tc -f NotoSansCJKtc-*.otf Traditional Chinese Multilingual Sans OTF


%notocjkpkg -n serif-cjk-tc -f NotoSerifCJKtc-*.otf Traditional Chinese Multilingual Serif OTF


%notocjkpkg -n sans-mono-cjk-tc -f NotoSansMonoCJKtc-*.otf Traditional Chinese Multilingual Sans Mono OTF


%notocjkpkg -n sans-cjk-hk -f NotoSansCJKhk-*.otf Traditional Chinese Multilingual Sans OTF


%notocjkpkg -n sans-mono-cjk-hk -f NotoSansMonoCJKhk-*.otf Traditional Chinese Multilingual Sans Mono OTF


%notocjkpkg -n sans-jp -f NotoSansJP-*.otf Japanese Region-specific Sans OTF


%notocjkpkg -n serif-jp -f NotoSerifJP-*.otf Japanese Region-specific Serif OTF


%notocjkpkg -n sans-kr -f NotoSansKR-*.otf Korean Region-specific Sans OTF


%notocjkpkg -n serif-kr -f NotoSerifKR-*.otf Korean Region-specific Serif OTF


%notocjkpkg -n sans-sc -f NotoSansSC-*.otf Simplified Chinese Region-specific Sans OTF


%notocjkpkg -n serif-sc -f NotoSerifSC-*.otf Simplified Chinese Region-specific Serif OTF


%notocjkpkg -n sans-tc -f NotoSansTC-*.otf Traditional Chinese Region-specific Sans OTF


%notocjkpkg -n serif-tc -f NotoSerifTC-*.otf Traditional Chinese Region-specific Serif OTF


%notocjkpkg -n sans-hk -f NotoSansHK-*.otf Traditional Chinese Region-specific Sans OTF


%prep
%setup -q -n noto-cjk-%{commit0}
cp -p %{SOURCE1} %{SOURCE2} .
# generate the font conf files
bash -x ./genfontconf.sh


%build


%install
install -m 0755 -d %{buildroot}%{_fontdir}

# copy OTC files
install -m 0644 -p NotoSansCJK-*.ttc %{buildroot}%{_fontdir}
install -m 0644 -p NotoSerifCJK-*.ttc %{buildroot}%{_fontdir}

# copy Multilingual OTF files
install -m 0644 -p NotoSansCJK{jp,kr,sc,tc,hk}-*.otf %{buildroot}%{_fontdir}
install -m 0644 -p NotoSerifCJK{jp,kr,sc,tc}-*.otf %{buildroot}%{_fontdir}
install -m 0644 -p NotoSansMonoCJK{jp,kr,sc,tc,hk}-*.otf %{buildroot}%{_fontdir}

# copy Region-specific OTF
install -m 0644 -p NotoSans{JP,KR,SC,TC,HK}-*.otf %{buildroot}%{_fontdir}
install -m 0644 -p NotoSerif{JP,KR,SC,TC}-*.otf %{buildroot}%{_fontdir}


install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
            %{buildroot}%{_fontconfig_confdir}

for f in sans-cjk-ttc serif-cjk-ttc \
    sans-cjk-jp serif-cjk-jp sans-mono-cjk-jp \
    sans-cjk-kr serif-cjk-kr sans-mono-cjk-kr \
    sans-cjk-sc serif-cjk-sc sans-mono-cjk-sc \
    sans-cjk-tc serif-cjk-tc sans-mono-cjk-tc \
    sans-cjk-hk sans-mono-cjk-hk \
    sans-jp serif-jp \
    sans-kr serif-kr \
    sans-sc serif-sc \
    sans-tc serif-tc \
    sans-hk;
do
    fconf=$(basename -a *-%{fontconf}-$f.conf)
    if [ "$(echo $fconf | wc -w)" -ne 1 ]; then
       echo "Did not find unique \*-%{fontconf}-$f.conf file"
       exit 1
    fi

    install -m 0644 -p ${fconf} \
                %{buildroot}%{_fontconfig_templatedir}/${fconf}

    ln -s %{_fontconfig_templatedir}/${fconf} \
         %{buildroot}%{_fontconfig_confdir}/${fconf}
done

install -m 0644 -p %{SOURCE3} \
            %{buildroot}%{_fontconfig_templatedir}/%{fontconf2}

ln -s %{_fontconfig_templatedir}/%{fontconf2} \
     %{buildroot}%{_fontconfig_confdir}/%{fontconf2}


%files


%files common
%doc NEWS HISTORY README.formats README.third_party
%license LICENSE
%{_fontconfig_templatedir}/%{fontconf2}
%config(noreplace) %{_fontconfig_confdir}/%{fontconf2}


%changelog
* Tue Feb 09 2021 Joe Schmitt <joschmit@microsoft.com> - 20190416-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Define %%files section when %%_font_pkg is not defined

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20190416-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Peng Wu <pwu@redhat.com> - 20190416-5
- Update 65-google-noto-cjk-fonts.conf for HK

* Thu Aug  1 2019 Peng Wu <pwu@redhat.com> - 20190416-4
- Correct lang property of fontconfig in Noto Sans CJK fonts

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20190416-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 14 2019 Peng Wu <pwu@redhat.com> - 20190416-2
- Include HongKong fonts

* Wed Apr 17 2019 Peng Wu <pwu@redhat.com> - 20190416-1
- Update to git commit be6c059

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20170602-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Peng Wu <pwu@redhat.com> - 20170602-9
- Support Macau locale

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170602-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 16 2018 Peng Wu <pwu@redhat.com> - 20170602-7
- Make Noto CJK OTC files as default CJK fonts

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20170602-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Akira TAGOH <tagoh@redhat.com> - 20170602-5
- Update the priority to change the default font to Noto.

* Mon Dec 11 2017 Peng Wu <pwu@redhat.com> - 20170602-4
- Simplify spec file

* Thu Dec  7 2017 Peng Wu <pwu@redhat.com> - 20170602-3
- Include more fonts and sub package fonts

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20170602-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun  7 2017 Peng Wu <pwu@redhat.com> - 20170602-1
- Include Serif fonts

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.004-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec  2 2016 Peng Wu <pwu@redhat.com> - 1.004-7
- Rebuilt to fixes the spec file

* Fri Dec  2 2016 Peng Wu <pwu@redhat.com> - 1.004-6
- Disable Obsoletes for epel: for google-noto-sans-cjk-fonts (rh#1396260)
- Disable notocjkrep macro definition for epel

* Fri Apr 29 2016 Peng Wu <pwu@redhat.com> - 1.004-5
- Replace google-noto-sans-cjk-fonts package

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Nov 13 2015 Peng Wu <pwu@redhat.com> - 1.004-3
- Use TTC Files

* Mon Oct 26 2015 Peng Wu <pwu@redhat.com> - 1.004-2
- Fixes Spec

* Mon Oct 26 2015 Peng Wu <pwu@redhat.com> - 1.004-1
- Initial Version
