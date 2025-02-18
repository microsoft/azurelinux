# SPDX-License-Identifier: MIT

Epoch:   1
Version: 2.004
Release: 8%{?dist}
URL:     https://github.com/googlefonts/noto-cjk

%global foundry           Google
%global fontlicense       OFL-1.1
%global fontlicenses      LICENSE

%global common_description %{expand:
Noto CJK fonts, supporting Simplified Chinese, Traditional Chinese, \
Japanese, and Korean. The supported scripts are Han, Hiragana, Katakana, \
Hangul, and Bopomofo. Latin, Greek, Cyrllic, and various symbols are also \
supported for compatibility with CJK standards.
}

%global obsoletes_epoch_version_release 0:20201206-8

%global obsoletes_pkg()\
%define subpkgname %1\
Obsoletes:      %{subpkgname} < %{obsoletes_epoch_version_release}\
Provides:       %{subpkgname} = %{epoch}:%{version}-%{release}\


%global fontfamily0       Noto Sans CJK VF
%global fontsummary0      Google Noto Sans CJK Variable Fonts
%global fontpkgheader0    %{expand:
Recommends: google-noto-sans-mono-cjk-vf-fonts = %{epoch}:%{version}-%{release}


%obsoletes_pkg google-noto-cjk-fonts
%obsoletes_pkg google-noto-cjk-fonts-common
%obsoletes_pkg google-noto-sans-cjk-ttc-fonts

%obsoletes_pkg google-noto-sans-cjk-sc-fonts
%obsoletes_pkg google-noto-sans-cjk-tc-fonts
%obsoletes_pkg google-noto-sans-cjk-hk-fonts
%obsoletes_pkg google-noto-sans-cjk-jp-fonts
%obsoletes_pkg google-noto-sans-cjk-kr-fonts
}
%global fonts0            NotoSansCJK-VF.ttc
%global fontconfs0        %{SOURCE10} 65-0-%{fontpkgname0}.conf
%global fontdescription0  %{expand:
%{common_description}

The google-noto-sans-cjk-vf-fonts package contains Google Noto Sans CJK Variable fonts.}

%global fontfamily1       Noto Sans Mono CJK VF
%global fontsummary1      Google Noto Sans Mono CJK Variable Fonts
%global fontpkgheader1    %{expand:
%obsoletes_pkg google-noto-sans-mono-cjk-sc-fonts
%obsoletes_pkg google-noto-sans-mono-cjk-tc-fonts
%obsoletes_pkg google-noto-sans-mono-cjk-hk-fonts
%obsoletes_pkg google-noto-sans-mono-cjk-jp-fonts
%obsoletes_pkg google-noto-sans-mono-cjk-kr-fonts
}
%global fonts1            NotoSansMonoCJK-VF.ttc
%global fontconfs1        %{SOURCE11} 65-0-%{fontpkgname1}.conf
%global fontdescription1  %{expand:
%{common_description}

The google-noto-sans-mono-cjk-vf-fonts package contains Google Noto Sans Mono CJK Variable fonts.}

Source0:  https://github.com/googlefonts/noto-cjk/releases/download/Sans%{version}/01_NotoSansCJK-OTF-VF.zip
Source1:  genfontconf.py
Source10: 65-%{fontpkgname0}.conf
Source11: 65-%{fontpkgname1}.conf

%fontpkg -a

%prep
%autosetup -c

cp -p Variable/OTC/NotoSansCJK-VF.otf.ttc NotoSansCJK-VF.ttc
cp -p Variable/OTC/NotoSansMonoCJK-VF.otf.ttc NotoSansMonoCJK-VF.ttc

cp %{SOURCE1} .

python3 genfontconf.py "ja" "sans-serif" "Noto Sans CJK JP" \
        "ko" "sans-serif" "Noto Sans CJK KR" \
        "zh-cn:zh-sg" "sans-serif" "Noto Sans CJK SC" \
        "zh-tw:cmn:hak:lzh:nan" "sans-serif" "Noto Sans CJK TC" \
        "zh-hk:zh-mo:yue" "sans-serif" "Noto Sans CJK HK" \
    | xmllint --format - |tee 65-0-google-noto-sans-cjk-vf-fonts.conf


python3 genfontconf.py "ja" "monospace" "Noto Sans Mono CJK JP" \
        "ko" "monospace" "Noto Sans Mono CJK KR" \
        "zh-cn:zh-sg" "monospace" "Noto Sans Mono CJK SC" \
        "zh-tw:cmn:hak:lzh:nan" "monospace" "Noto Sans Mono CJK TC" \
        "zh-hk:zh-mo:yue" "monospace" "Noto Sans Mono CJK HK" \
    | xmllint --format - |tee 65-0-google-noto-sans-mono-cjk-vf-fonts.conf

%build
%fontbuild -a

%install
%fontinstall -a

%check
%fontcheck -a

%fontfiles -a

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Oct  6 2023 Akira TAGOH <tagoh@redhat.com> - 1:2.004-5
- Drop Conflict: google-noto-sans-cjk-fonts to get them installed together.
  fontconfig basically estimate same score for both but static font still has
  a priority because of path name. This works as a workaround for some issues
  related to variable fonts.
  Resolves: rhbz #2240646

* Wed Jul 26 2023 Peng Wu <pwu@redhat.com> - 1:2.004-4
- Add google-noto-sans-mono-cjk-vf-fonts sub package
- Resolves: RHBZ#2215475

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.004-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May  4 2023 Peng Wu <pwu@redhat.com> - 1:2.004-2
- Fix obsoletes_sans macro

* Fri Feb  3 2023 Peng Wu <pwu@redhat.com> - 1:2.004-1
- Initial Packaging
- Migrate to SPDX license
