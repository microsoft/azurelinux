# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT

Epoch:   1
Version: 2.003
Release: 4%{?dist}
URL:     https://github.com/googlefonts/noto-cjk

BuildRequires:            python3

%global foundry           Google
%global fontlicense       OFL-1.1
%global fontlicenses      LICENSE

%global fontfamily        Noto Serif CJK VF
%global fontsummary       Google Noto Serif CJK Variable Fonts
%global fonts             *.ttc
%global fontconfs         65-0-%{fontpkgname}.conf %{SOURCE10}
%global fontdescription   %{expand:
Noto CJK fonts, supporting Simplified Chinese, Traditional Chinese, \
Japanese, and Korean. The supported scripts are Han, Hiragana, Katakana, \
Hangul, and Bopomofo. Latin, Greek, Cyrllic, and various symbols are also \
supported for compatibility with CJK standards.

The google-noto-serif-cjk-vf-fonts package contains Google Noto Serif CJK Variable fonts.
}

Source0:  https://github.com/googlefonts/noto-cjk/releases/download/Serif%{version}/02_NotoSerifCJK-OTF-VF.zip
Source1:  genfontconf.py
Source10: 65-%{fontpkgname}.conf

%global obsoletes_epoch_version_release 0:20201206-8

%global obsoletes_pkg()\
%define subpkgname %1\
Obsoletes:      %{subpkgname} < %{obsoletes_epoch_version_release}\
Provides:       %{subpkgname} = %{epoch}:%{version}-%{release}\

%global obsoletes_serif()\
%define langname %1\
%obsoletes_pkg google-noto-serif-cjk-%{langname}-fonts\
%obsoletes_pkg google-noto-serif-%{langname}-fonts\

%global fontpkgheader     %{expand:

%obsoletes_pkg google-noto-serif-cjk-ttc-fonts

%obsoletes_serif sc
%obsoletes_serif tc
%obsoletes_serif jp
%obsoletes_serif kr

}

%fontpkg

%prep
%autosetup -c

cp -p Variable/OTC/NotoSerifCJK-VF.otf.ttc NotoSerifCJK-VF.ttc

cp %{SOURCE1} .

python3 genfontconf.py "ja" "serif" "Noto Serif CJK JP" \
        "ko" "serif" "Noto Serif CJK KR" \
        "zh-cn:zh-sg" "serif" "Noto Serif CJK SC" \
        "zh-tw:cmn:hak:lzh:nan" "serif" "Noto Serif CJK TC" \
        "zh-hk:zh-mo:yue" "serif" "Noto Serif CJK HK" \
    | xmllint --format - |tee 65-0-google-noto-serif-cjk-vf-fonts.conf


%build
%fontbuild

%install
%fontinstall

%check
%fontcheck

%fontfiles

%changelog
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

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.001-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May  4 2023 Peng Wu <pwu@redhat.com> - 1:2.001-2
- Fix obsoletes_serif macro (rhbz #2190290)

* Fri Feb  3 2023 Peng Wu <pwu@redhat.com> - 1:2.001-1
- Initial Packaging
- Migrate to SPDX license
