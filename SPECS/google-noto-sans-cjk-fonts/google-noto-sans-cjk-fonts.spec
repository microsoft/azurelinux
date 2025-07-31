Name:           google-noto-sans-cjk-fonts
epoch:          1
Version:        2.004
Release:        11%{?dist}
Summary:        google-noto-sans-cjk-fonts for fonts
License:        OFL
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

URL:      https://github.com/googlefonts/noto-cjk
Source0:  https://github.com/googlefonts/noto-cjk/releases/download/Sans%{version}/03_NotoSansCJK-OTC.zip#/%{name}-%{version}.zip
Source1:  %{name}-%{version}-genfontconf.py
Source10: 65-google-noto-sans-cjk-fonts.conf
Source11: 65-google-noto-sans-cjk-mono-fonts.conf

BuildRequires:   python3
BuildRequires:   unzip

%description
Noto CJK fonts, supporting Simplified Chinese, Traditional Chinese, \
Japanese, and Korean. The supported scripts are Han, Hiragana, Katakana, \
Hangul, and Bopomofo. Latin, Greek, Cyrllic, and various symbols are also \
supported for compatibility with CJK standards.

The google-noto-sans-cjk-fonts package contains Google Noto Sans CJK fonts.

%prep
unzip %{SOURCE0}
cp %{SOURCE1} .

python3 genfontconf.py "ja" "monospace" "Noto Sans Mono CJK JP" \
        "ja" "sans-serif" "Noto Sans CJK JP" \
        "ko" "monospace" "Noto Sans Mono CJK KR" \
        "ko" "sans-serif" "Noto Sans CJK KR" \
        "zh-cn:zh-sg" "monospace" "Noto Sans Mono CJK SC" \
        "zh-cn:zh-sg" "sans-serif" "Noto Sans CJK SC" \
        "zh-tw:cmn:hak:lzh:nan" "monospace" "Noto Sans Mono CJK TC" \
        "zh-tw:cmn:hak:lzh:nan" "sans-serif" "Noto Sans CJK TC" \
        "zh-hk:zh-mo:yue" "monospace" "Noto Sans Mono CJK HK" \
        "zh-hk:zh-mo:yue" "sans-serif" "Noto Sans CJK HK" \
    | xmllint --format - |tee 65-1-google-noto-sans-cjk-fonts.conf


%build
# no build

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0644 -p *.ttc %{buildroot}%{_fontdir}

install -m 0755 -d %{buildroot}%{_fontconfig_templatedir} \
                   %{buildroot}%{_fontconfig_confdir}

install -m 0644 -p %{SOURCE10} %{buildroot}%{_fontconfig_templatedir}/65-%{name}.conf
install -m 0644 -p %{SOURCE11} %{buildroot}%{_fontconfig_templatedir}/65-google-noto-sans-cjk-mono-fonts.conf
install -m 0644 -p 65-1-%{name}.conf %{buildroot}%{_fontconfig_templatedir}/65-1-%{name}.conf


ln -s %{_fontconfig_templatedir}/65-%{name}.conf \
      %{buildroot}%{_fontconfig_confdir}/65-%{name}.conf
ln -s %{_fontconfig_templatedir}/65-google-noto-sans-cjk-mono-fonts.conf \
      %{buildroot}%{_fontconfig_confdir}/65-google-noto-sans-cjk-mono-fonts.conf
ln -s %{_fontconfig_templatedir}/65-1-%{name}.conf %{buildroot}%{_fontconfig_confdir}/65-1-%{name}.conf

%files
%{_fontdir}/*.ttc
%{_fontconfig_templatedir}/65-%{name}.conf
%{_fontconfig_templatedir}/65-google-noto-sans-cjk-mono-fonts.conf
%{_fontconfig_templatedir}/65-1-google-noto-sans-cjk-fonts.conf
%{_fontconfig_confdir}/65-%{name}.conf
%{_fontconfig_confdir}/65-google-noto-sans-cjk-mono-fonts.conf
%{_fontconfig_confdir}/65-1-%{name}.conf
%license LICENSE

%changelog
* Wed Jul 30 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 1:2.004-11
- License verified
- Initial Azure Linux import from Fedora 43 (license: MIT).

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct  6 2023 Akira TAGOH <tagoh@redhat.com> - 1:2.004-5
- Drop Conflict: google-noto-sans-cjk-vf-fonts to get them installed together.
  fontconfig basically estimate same score for both but static font still has
  a priority because of path name. This works as a workaround for some issues
  related to variable fonts.
  Resolves: rhbz #2240646

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 24 2023 Peng Wu <pwu@redhat.com> - 1:2.004-3
- Fix dnf upgrade issue
- Resolves: RHBZ#2181349

* Thu Mar 16 2023 Peng Wu <pwu@redhat.com> - 1:2.004-2
- Update the spec file with some Obsoletes and Provides

* Fri Feb  3 2023 Peng Wu <pwu@redhat.com> - 1:2.004-1
- Initial Packaging
- Migrate to SPDX license
 