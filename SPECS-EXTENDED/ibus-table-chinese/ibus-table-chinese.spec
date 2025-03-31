%global message_level 6
%global ibus_tables_dir %{_datadir}/ibus-table/tables
%global ibus_icons_dir %{_datadir}/ibus-table/icons
Name:           ibus-table-chinese
Version:        1.8.12
Release:        6%{?dist}
Summary:        Chinese input tables for IBus
Summary(zh_CN): 中文码表输入法
Summary(zh_TW): 中文碼表輸入法
License:        GPL-3.0-or-later
URL:            https://github.com/mike-fabian/ibus-table-chinese
Source0:        https://github.com/mike-fabian/ibus-table-chinese/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.0.0
BuildRequires:  ibus-table-devel >= 1.10.0
BuildRequires: make
Requires:       ibus-table >= 1.10.0
Obsoletes:      ibus-table-yinma < 1.3
Obsoletes:      ibus-table-xingma < 1.3

BuildArch:      noarch

%description
ibus-table-chinese is provides the infrastructure for Chinese input methods.
Input tables themselves are in subpackages.

%description -l zh_TW
ibus-table-chinese 提供了中文碼表輸入法的基礎架構。
    輸入法本身則在子套件裡。

%package array
Summary:       Array input methods
Summary(zh_CN): 行列输入法
Summary(zh_TW): 行列輸入法
License:        LicenseRef-Fedora-UltraPermissive
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-array30 = %{version}-%{release}
Obsoletes:      ibus-table-array30 < 1.3

%description array
Array input method is a free, open-minded character-structured
input method. Includes:
array30: 27489 characters.
array30-big: 27489 characters + Unicode ExtB.

%description -l zh_TW array
行列輸入法是一套免費授權、具有開放理念的字根式
中文輸入法，發明人是行列科技負責人廖明德。

行列輸入法除了可以輸入繁體中文和簡體中文之外，
亦可輸入Unicode當中的中日韓統一表意文字。

包含了：
行列30: 27489 字
行列30大字集: 27489 字 + Unicode ExtB.

%package cangjie
Summary:       Cangjie based input methods
Summary(zh_TW): 倉頡輸入法
Summary(zh_CN): 仓颉输入法
License:        LicenseRef-Fedora-UltraPermissive AND GPL-2.0-only
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-cangjie = %{version}-%{release}
Obsoletes:      ibus-table-cangjie < 1.3

%description cangjie
Cangjie based input methods, includes:
Cangjie3, Canjie5, and Cangjie big tables.

%description -l zh_TW cangjie
倉頡以及其衍生輸入法，包含：
倉頡三代、倉頡五代以及倉頡大字集。

%package cantonese
Summary:        Cantonese input methods
Summary(zh_TW): 粵語輸入法
License:        GPL-2.0-only AND GPL-3.0-or-later AND MIT
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-cantonese = %{version}-%{release}
Obsoletes:      ibus-table-cantonese < 1.3

%description cantonese
Cantonese input methods, includes:
Cantonese, Hong-Kong version of Cantonese,
and jyutping.

%description -l zh_TW cantonese
粵語輸入法。包含：
廣東拼音、港式廣東話、
以及粵語拼音。

%package easy
Summary:        Easy input method
Summary(zh_CN): 轻松输入法
Summary(zh_TW): 輕鬆輸入法
License:        GPL-2.0-only
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-easy = %{version}-%{release}
Obsoletes:      ibus-table-easy < 1.3

%description easy
Easy phrase-wise input method.

%description -l zh_CN  easy
轻松大词库

%description -l zh_TW  easy
輕鬆大詞庫

%package erbi
Summary: Erbi input method
Summary(zh_CN): 二笔输入法
Summary(zh_TW): 二筆輸入法
License:        GPL-2.0-or-later
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-erbi = %{version}-%{release}
Obsoletes:      ibus-table-erbi < 1.3

%description erbi
Erbi input methods. Includes:
Super Erbi (as erbi)
and  Erbi Qin-Song (erbi-qs)

%description -l zh_CN erbi
包含：
小林子二笔 (erbi)
以及青松二笔 (erbi-qs)

%description -l zh_TW erbi
包含：
小林子二筆 (erbi)
以及青松二筆 (erbi-qs)

%package quick
Summary:       Quick-to-learn input methods
Summary(zh_CN): 速成输入法
Summary(zh_TW): 速成輸入法
License:        LicenseRef-Fedora-UltraPermissive
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-quick = %{version}-%{release}
Obsoletes:      ibus-table-quick < 1.3

%description quick
Quick-to-learn is based on Cangjie input method,
but only need Canjie's first and last word-root
to form a character.

Includes:
Quick3, Quick5 and Quick-Classic.

%description -l zh_TW quick
速成輸入法，又稱簡易輸入法，為倉頡輸入法之簡化版本。
只取倉頡碼的首尾兩碼，所以一字最長只有兩碼。

包含：
速成三代、速成五代以及速成古典版。

%package scj
Summary: Smart Cangjie
Summary(zh_CN): 快速仓颉输入法
Summary(zh_TW): 快速倉頡輸入法
License:        GPL-3.0-or-later
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-cangjie = %{version}-%{release}
Obsoletes:      ibus-table-cangjie < 1.3

%description scj
Smart Cangjie is an improved Cangjie base input method
which handles Cangjie, Quick, Cantonese, Chinese punctuation,
Japanese, 3000 frequent words by Hong Kong government,
both Traditional and Simplified Chinese.

This package includes the Smart Cangjie 6.

%description -l zh_CN scj
快速仓颉输入法第六代（快仓六）是一个多功能和多任务的
输入法系统。在功能方面，它不但拥有多种不同版本的仓颉
输入法、速成输入法、广东话输入法、高效率的标点、特殊
符号和数字编码、日文编码、香港政府三千常用字编码、简
码和容错码，而且还能够处理繁体和简体文字。在任务方面
，它不但承袭了传统仓颉的「中文输入、输出、辨识和释义
」等功能，而且还能肩负起促进「资讯科技教育、母语教育
和特殊教育」等多重任务。

%description -l zh_TW scj
快速倉頡輸入法第六代（快倉六）是一個多功能和多任務的
輸入法系統。在功能方面，它不但擁有多種不同版本的倉頡
輸入法、速成輸入法、廣東話輸入法、高效率的標點、特殊
符號和數字編碼、日文編碼、香港政府三千常用字編碼、簡
碼和容錯碼，而且還能夠處理繁體和簡體文字。在任務方面
，它不但承襲了傳統倉頡的「中文輸入、輸出、辨識和釋義
」等功能，而且還能肩負起促進「資訊科技教育、母語教育
和特殊教育」等多重任務。

%package stroke5
Summary: Stroke 5 input method
Summary(zh_CN): 笔顺五码输入法
Summary(zh_TW): 筆順五碼輸入法
License:        GPL-3.0-or-later
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-stroke5 = %{version}-%{release}
Obsoletes:      ibus-table-stroke5 < 1.3
Obsoletes:      ibus-table-yinma < 1.3

%description stroke5
Stroke5 input method.

%description -l zh_CN stroke5
笔顺五码。

%description -l zh_TW stroke5
筆順五碼。

%package wu
Summary: Wu pronunciation input method
Summary(zh_CN): 上海吳语注音输入法
Summary(zh_TW): 上海吳語注音輸入法
License:        GPL-2.0-or-later
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-wu = %{version}-%{release}
Obsoletes:      ibus-table-wu < 1.3

%description wu
Wu pronunciation input method.
URL: http://input.foruto.com/wu/

%description -l zh_CN wu
上海吳语注音输入法。
URL: http://input.foruto.com/wu/

%description -l zh_TW wu
上海吳語注音輸入法以現代吳語中有代表性的上海吳語（又稱上海話、滬語）的讀音、詞語為基礎。
本輸入法適用於母語為上海話的用戶，也能作為學習上海話的輔助工具。
URL: http://input.foruto.com/wu/

%package wubi-haifeng
Summary: Haifeng Wubi input method
Summary(zh_CN): 海峰五笔输入法
Summary(zh_TW): 海峰五筆輸入法
License:        0BSD
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-wubi = %{version}-%{release}
Obsoletes:      ibus-table-wubi < 1.3

%description wubi-haifeng
Haifeng Wubi input methods. Current includes:
Haifeng Wubi 86.

%description -l zh_CN wubi-haifeng
海峰五笔输入法。包含：海峰五笔86。

%description -l zh_TW wubi-haifeng
海峰五筆輸入法。包含：海峰五筆86。

%package wubi-jidian
Summary: Jidian Wubi 86 input method, JiShuang 6.0
Summary(zh_CN): 极点五笔86输入法 极爽词库 6.0
Summary(zh_TW): 極點五筆86輸入法 極爽詞庫 6.0
License:        LicenseRef-Fedora-UltraPermissive
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-wubi = %{version}-%{release}
Obsoletes:      ibus-table-wubi < 1.3

%description wubi-jidian
Jidian Wubi input methods. Current includes:
Wubi 86.

%description -l zh_CN wubi-jidian
使用极爽字库之极点五笔输入法。

%description -l zh_TW wubi-jidian
使用極爽字庫極點五筆輸入法

%package yong
Summary: YongMa input method
Summary(zh_CN): 永码输入法
Summary(zh_TW): 永碼輸入法
License:        GPL-3.0-only
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-yong = %{version}-%{release}
Obsoletes:      ibus-table-yong < 1.3

%description yong
YongMa input method.

%description -l zh_CN yong
永码输入法。

%description -l zh_TW yong
永碼輸入法。

%package cantonyale
Summary:        Cantonese input method based on yale romanization
License:        GPL-2.0-only
Requires:       %{name} = %{version}-%{release}

%description cantonyale
Cantonese input method based on yale romanization

%prep
%setup -q -n %{name}-%{version}

%build
cmake -B build-noarch -S .
make -C build-noarch

%install
rm -rf %{buildroot}
make -C build-noarch install DESTDIR=%{buildroot}

# Register as AppStream components to be visible in the software center
mkdir -p $RPM_BUILD_ROOT%{_datadir}/metainfo
cp metainfo/*.appdata.xml $RPM_BUILD_ROOT%{_datadir}/metainfo

# We install document using doc 
rm -fr %{buildroot}%{_docdir}/*

%files
%doc AUTHORS README ChangeLog COPYING

%files array
%{_datadir}/metainfo/ibus-table-chinese-array.appdata.xml
%{ibus_icons_dir}/array30.*
%{ibus_tables_dir}/array30.db
%{ibus_icons_dir}/array30-big.*
%{ibus_tables_dir}/array30-big.db

%files cangjie
%{_datadir}/metainfo/ibus-table-chinese-cangjie.appdata.xml
%{ibus_icons_dir}/cangjie3.*
%{ibus_tables_dir}/cangjie3.db
%{ibus_icons_dir}/cangjie5.*
%{ibus_tables_dir}/cangjie5.db
%{ibus_icons_dir}/cangjie-big.*
%{ibus_tables_dir}/cangjie-big.db

%files cantonese
%{_datadir}/metainfo/ibus-table-chinese-cantonese.appdata.xml
%{ibus_icons_dir}/cantonese.*
%{ibus_tables_dir}/cantonese.db
%{ibus_icons_dir}/cantonhk.*
%{ibus_tables_dir}/cantonhk.db
%{ibus_icons_dir}/jyutping.*
%{ibus_tables_dir}/jyutping.db

%files easy
%{_datadir}/metainfo/ibus-table-chinese-easy.appdata.xml
%{ibus_icons_dir}/easy-big.*
%{ibus_tables_dir}/easy-big.db

%files erbi
%{_datadir}/metainfo/ibus-table-chinese-erbi.appdata.xml
%{ibus_icons_dir}/erbi.*
%{ibus_tables_dir}/erbi.db
%{ibus_icons_dir}/erbi-qs.*
%{ibus_tables_dir}/erbi-qs.db

%files quick
%{_datadir}/metainfo/ibus-table-chinese-quick.appdata.xml
%{ibus_icons_dir}/quick3.*
%{ibus_tables_dir}/quick3.db
%{ibus_icons_dir}/quick5.*
%{ibus_tables_dir}/quick5.db
%{ibus_icons_dir}/quick-classic.*
%{ibus_tables_dir}/quick-classic.db

%files scj
%{_datadir}/metainfo/ibus-table-chinese-scj.appdata.xml
%{ibus_icons_dir}/scj6.*
%{ibus_tables_dir}/scj6.db

%files stroke5
%{_datadir}/metainfo/ibus-table-chinese-stroke5.appdata.xml
%{ibus_icons_dir}/stroke5.*
%{ibus_tables_dir}/stroke5.db

%files wu
%{_datadir}/metainfo/ibus-table-chinese-wu.appdata.xml
%{ibus_icons_dir}/wu.*
%{ibus_tables_dir}/wu.db

%files wubi-haifeng
%{_datadir}/metainfo/ibus-table-chinese-wubi-haifeng86.appdata.xml
%doc tables/wubi-haifeng/COPYING tables/wubi-haifeng/README
%{ibus_icons_dir}/wubi-haifeng86.*
%{ibus_tables_dir}/wubi-haifeng86.db

%files wubi-jidian
%{_datadir}/metainfo/ibus-table-chinese-wubi-jidian86.appdata.xml
%{ibus_icons_dir}/wubi-jidian86.*
%{ibus_tables_dir}/wubi-jidian86.db

%files yong
%{_datadir}/metainfo/ibus-table-chinese-yong.appdata.xml
%{ibus_icons_dir}/yong.*
%{ibus_tables_dir}/yong.db

%files cantonyale
%{_datadir}/metainfo/ibus-table-chinese-cantonyale.appdata.xml
%{ibus_icons_dir}/cantonyale.*
%{ibus_tables_dir}/cantonyale.db

%changelog
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.12-1
- Update to 1.8.12
- appdata.xml files are now included upstream, remove from the .spec file
- Migrate license tags to SPDX format

* Sun Oct 30 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.11-1
- Update to 1.8.11
- Improve punctuation support in jyutping.txt, cantonese.txt, cantonhk.txt, cantonyale.txt
  (Resolves: https://github.com/mike-fabian/ibus-table-chinese/issues/7)
- Improve “improve_jyutping.py” to allow comments in the table
- Update of jyutping.txt for Unicode 15.0.0 final release

* Tue Oct 25 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.10-1
- Update to 1.8.10
- Improve punctuation support in cangjie5.txt, cangjie3.txt, cangjie-big.txt,
  quick5.txt, quick3.txt, quick-classic.txt
  (Resolves: https://github.com/kaio/ibus-table/issues/73)
- Remove obsolete patch: Make-build-outside-of-the-source-tree-possible.patch

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.9-1
- Update to 1.8.9
- Add tones to Jyutping.txt table
  (Resolves: https://github.com/mike-fabian/ibus-table-chinese/issues/6)
  Tonal markers according to
  https://github.com/rime/rime-cantonese/blob/main/README-en.md#tonal-markers
  were added:
  1. v: High level, e.g. siv → 詩; High level checked, e.g. sikv → 色
  2. x: Medium rising, e.g. six → 史
  3. q: Medium level, e.g. siq→ 試; Medium level checked, e.g. sekq → 錫
  4. vv: Low falling, e.g. sivv → 時
  5. xx: Low rising, e.g. sixx → 市
  6. qq: Low level, e.g. siqq→ 事; Low level checked, e.g. sikqq → 食
 
* Wed Feb 09 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.8-1
- Update to 1.8.8
- Add PINYIN_MODE = TRUE to cangjie-big.txt, quick-classic.txt, and erbi.txt
- Make “Traditional Chinese only” the default for quick5
- Improve the quick5.txt table in a similar way the cangjie5.txt
  table was recently improved
  (Resolves: https://github.com/mike-fabian/ibus-table-chinese/issues/4)
- Build outside of the source tree
  (Resolves: https://github.com/mike-fabian/ibus-table-chinese/issues/2)

* Sat Jan 29 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.7-2
- Don’t index the databases in the post install

* Mon Jan 24 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.7-1
- Update to 1.8.7
- Make “Traditional Chinese only” the default for cangjie5
  (Resolves: https://github.com/mike-fabian/ibus-table-chinese/issues/2)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.6-1
- Update to 1.8.6
- Increase serial number of cangjie5.txt and erbi-qs.txt

* Tue Jan 11 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.5-1
- Update to 1.8.5
- erbi-qs.txt: add table_extra tag for auxiliary code
  (Resolves: https://github.com/definite/ibus-table-chinese/pull/18)

* Mon Jan 10 2022 Mike FABIAN <mfabian@redhat.com> - 1.8.4-1
- Update to 1.8.4
- Another improvement for cangjie5.txt
- Change URLs in .spec file to point to new upstream repo
- Remove patches which are included upstream.

* Thu Dec 30 2021 Mike FABIAN <mfabian@redhat.com> - 1.8.3-11
- Improve cangjie5.txt
- Resolves: https://github.com/mike-fabian/ibus-table/issues/76

* Tue Dec 28 2021 Mike FABIAN <mfabian@redhat.com> - 1.8.3-10
- Add appdata.xml files for the subpackages where they were missing
- Fix URLs in existing appdata.xml files
- Resolves: rhbz#2035337

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 16 2021 Mike FABIAN <mfabian@redhat.com> - 1.8.3-8
- Correct misplaced non-alphabetic symbol in wubi-jidian table
- Resolves: https://github.com/definite/ibus-table-chinese/pull/16

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 03 2020 Mike FABIAN <mfabian@redhat.com> - 1.8.3-6
- Remove BuildRequirement of cmake-fedora

* Thu Jul 30 2020 Mike FABIAN <mfabian@redhat.com> - 1.8.3-5
- Fix build on rawhide

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 16 2020 Mike FABIAN <mfabian@redhat.com> - 1.8.3-2
- bump release number to force a rebuild with newer ibus-table >= 1.10.0

* Thu Jul 09 2020 Mike FABIAN <mfabian@redhat.com> - 1.8.3-1
- Update to 1.8.3
- Turned cangjie 3 and 5's DYNAMIC_ADJUST to FALSE
  Resolves: https://github.com/definite/ibus-table-chinese/pull/14
- Add SUGGESTION_MODE = TRUE to the wubi tables
  Resolves: https://github.com/definite/ibus-table-chinese/pull/15
- Support pinyin mode also for stroke5 table
  Resolves: https://github.com/definite/ibus-table-chinese/pull/12
- Use nicer values for symbol and status prompt
  Resolves: https://github.com/definite/ibus-table-chinese/pull/8
- update jyutping table; add cantonyale table
  Resolves: https://github.com/definite/ibus-table-chinese/pull/11
- Update jyutping and cantonese tables
  Resolves: https://github.com/definite/ibus-table-chinese/pull/9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 02 2019 Mike FABIAN <mfabian@redhat.com> - 1.8.2-14
- Fix description of Stroke5 input method
- Resolves: rhbz#1418565

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Peng Wu <pwu@redhat.com> - 1.8.2-10
- Fixes URL

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Richard Hughes <rhughes@redhat.com> - 1.8.2-5
- Increase AppStream search result weighting when using various 'zh' locales.

* Mon Jun 22 2015 Richard Hughes <rhughes@redhat.com> - 1.8.2-4
- Fix the License format for ibus-table-chinese-cantonese

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 25 2015 Richard Hughes <rhughes@redhat.com> - 1.8.2-2
- Register as AppStream components.

* Tue Jun 10 2014 Ding-Yi Chen <dchen@redhat.com> - 1.8.2-1
- Built for ibus-table-1.8.1

* Sun Jun 08 2014 Ding-Yi Chen <dchen@redhat.com> - 1.8.1-1
- Add summary and description translation back.

* Sat Jun 07 2014 Ding-Yi Chen <dchen@redhat.com> - 1.8.0-1
- Update for ibus-table-1.8.0
- Fixed Bug 1099380 - The stroke5 table should not use 
  "AUTO_SELECT = TRUE" but "AUTO_SELECT = FALSE"

* Tue May 27 2014 Mike FABIAN <mfabian@redhat.com> - 1.4.6-3
- bump release number to build against updated ibus-table

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Ding-Yi Chen <dchen@redhat.com> - 1.4.6-1
- Fixed IBus Google issue 1126: An error in ChineseTableLicenseAuditing
- Complete LICENSE tag for all of the tables.

* Mon Nov 26 2012 Ding-Yi Chen <dchen@redhat.com> - 1.4.5-1
- Table build scripts has been refactored.
- cmake-fedora is added as submodule.
- Fixed Bug 855250 - Change the default filtering for Quick and Cangjie by
  merging maxiaojun's repository
- Fixed Google Issue 1405: failed to build ibus-table-chinese due to missing db files
- Fixed Google issue 1507: Add CJKV Extension C/D support for Array30
- Merge GitHub Pull request 3: Added the inter punct
- Merge GitHub Pull request 4: Give Cangjie and Quick users 9 candidates per page

* Fri Sep 07 2012 Ding-Yi Chen <dchen@redhat.com> - 1.4.0-1
- Table build scripts has been refactored.
- cmake-fedora is added as submodule.
- Fixed Bug 855250 - Change the default filtering for Quick and Cangjie by
  merging maxiaojun's repository
- Fixed Google Issue 1405: failed to build ibus-table-chinese due to missing db files

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 28 2011 Ding-Yi Chen <dchen@redhat.com> - 1.3.5-1
- Merge Caius Chance's branch for DYNAMIC_ADJUST
- Dependency update to cmake-0.8.1

* Wed Aug 31 2011 Ding-Yi Chen <dchen@redhat.com> - 1.3.4-1
- Fixed Bug 715707 - FTBFS ibus-table-chinese-1.3.0.20110114-2.fc15
- Fixed Bug 629212 - bad candidate orders in ibus-table-quick
- Merged patch from sagara @ github, which address IBus issue 787
- Make it compatible with cmake-fedora-0.7.994
- Move the cmake policies to the front
- Suppress the misleading warning from rpm -V

* Fri Jan 14 2011 Ding-Yi Chen <dchen@redhat.com> - 1.3.0.20110114-1
- Fix Bug 667877: ibus-table-yinma and ibus-table-xingma have been obsoleted.
- Now depends on cmake-fedora

* Mon Dec 06 2010 Ding-Yi Chen <dchen@redhat.com> - 1.3.0.20101206-1
- New tables which was not include in original:
  + array30, array30-big, wubi-haifeng
- Table removed from original version because of license issues:
  + zhengma, ziranma
- Add package review ID
- Add build tag for el6

* Fri Dec 03 2010 Ding-Yi Chen <dchen@redhat.com> - 1.3.0.20101201-1
- Support out-of-source build
- Remove ibus-table-chinese-all

* Wed Jan 06 2010 Caius 'kaio' Chance <k at kaio.me> - 1.3.0.20100527-3
- Added Quick 3, 5, Classic tables and icons.
- Added Easy (big) table and icon.
- Updated AUTHORS, COPYING, license and its declarations.

* Mon Aug 31 2009 Caius 'kaio' Chance <k at kaio.me> - 1.3.0.20100527-2
- Added CangJie (big) table.

* Tue Aug 19 2008 Yu Yuwei <acevery@gmail.com> - 1.3.0.20100527-1
- The first version.

