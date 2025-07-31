Name:           google-noto-serif-cjk-fonts
epoch:          1
Version:        2.003
Release:        4%{?dist}
Summary:        google-noto-serif-cjk-fonts for fonts
License:        OFL
Vendor:         Microsoft Corporation
Distribution:   Azure Linux


BuildRequires:   python3
BuildRequires:   unzip
URL:             https://github.com/googlefonts/noto-cjk
Source0:         https://github.com/googlefonts/noto-cjk/releases/download/Serif%{version}/04_NotoSerifCJKOTC.zip#/%{name}-%{version}.zip
Source1:         genfontconf.py
Source10:        65-%{name}.conf

%description
Noto CJK fonts, supporting Simplified Chinese, Traditional Chinese, \
Japanese, and Korean. The supported scripts are Han, Hiragana, Katakana, \
Hangul, and Bopomofo. Latin, Greek, Cyrllic, and various symbols are also \
supported for compatibility with CJK standards.
The google-noto-serif-cjk-fonts package contains Google Noto Serif CJK fonts.

%prep
unzip %{SOURCE0}
cp %{SOURCE1} .

python3 genfontconf.py "ja" "serif" "Noto Serif CJK JP" \
        "ko" "serif" "Noto Serif CJK KR" \
        "zh-cn:zh-sg" "serif" "Noto Serif CJK SC" \
        "zh-tw:cmn:hak:lzh:nan" "serif" "Noto Serif CJK TC" \
        "zh-hk:zh-mo:yue" "serif" "Noto Serif CJK HK" \
    | xmllint --format - |tee 65-1-google-noto-serif-cjk-fonts.conf

%build
# no build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p OTC/*.ttc %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE10} %{buildroot}%{_fontconfig_templatedir}/65-%{name}.conf
install -m 0644 -p 65-1-google-noto-serif-cjk-fonts.conf %{buildroot}%{_fontconfig_templatedir}/65-1-%{name}.conf

ln -s %{_fontconfig_templatedir}/65-%{name}.conf \
      %{buildroot}%{_fontconfig_confdir}/65-%{name}.conf
ln -s %{_fontconfig_templatedir}/65-1-%{name}.conf \
      %{buildroot}%{_fontconfig_confdir}/65-1-%{name}.conf

%files
%{_fontdir}/*.ttc
%{_fontconfig_templatedir}/65-%{name}.conf
%{_fontconfig_templatedir}/65-1-%{name}.conf
%{_fontconfig_confdir}/65-%{name}.conf
%{_fontconfig_confdir}/65-1-%{name}.conf
%license LICENSE

%changelog
* Wed Jul 30 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 1:2.003-4
- License verified
- Initial Azure Linux import from Fedora 43 (license: MIT).

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.003-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.003-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug  1 2024 Peng Wu <pwu@redhat.com> - 1:2.003-1
- Update to 2.003

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.002-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.002-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.002-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 10 2023 Peng Wu <pwu@redhat.com> - 1:2.002-2
- Drop some Conflicts from the Noto Serif CJK fonts

* Tue Aug 22 2023 Peng Wu <pwu@redhat.com> - 1:2.002-1
- Update to 2.002

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.001-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 24 2023 Peng Wu <pwu@redhat.com> - 1:2.001-3
- Fix dnf upgrade issue

* Thu Mar 16 2023 Peng Wu <pwu@redhat.com> - 1:2.001-2
- Update the spec file with some Obsoletes and Provides

* Fri Feb  3 2023 Peng Wu <pwu@redhat.com> - 1:2.001-1
- Initial Packaging
- Migrate to SPDX license
