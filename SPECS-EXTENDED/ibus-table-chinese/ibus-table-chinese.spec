Vendor:         Microsoft Corporation
Distribution:   Mariner
%global message_level 6
%global ibus_tables_dir %{_datadir}/ibus-table/tables
%global ibus_icons_dir %{_datadir}/ibus-table/icons
%global createdb ibus-table-createdb
Name:           ibus-table-chinese
Version:        1.8.3
Release:        3%{?dist}
Summary:        Chinese input tables for IBus
Summary(zh_CN): 中文码表输入法
Summary(zh_TW): 中文碼表輸入法
License:        GPLv3+
URL:            https://github.com/definite/ibus-table-chinese
Source0:        https://github.com/definite/ibus-table-chinese/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 2.6.2
BuildRequires:  cmake-fedora
BuildRequires:  ibus-table-devel >= 1.10.0
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
License:       Freely redistributable without restriction
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
License:       Freely redistributable without restriction
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
License:       GPLv2 and GPLv3+ and Freely redistributable without restriction
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
License:        GPLv2
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
License:       GPLv2+
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
License:       Freely redistributable without restriction
Requires:       %{name} = %{version}-%{release}
Provides:       ibus-table-quick = %{version}-%{release}
Obsoletes:      ibus-table-quick < 1.3

%description quick
Quick-to-learn is based on Cangjie input method,
but only need Canjie's first and last word-root
to form a character.

Includes:
Quick3, Quick5 and Quick-Classic,
and Smart Cangjie 6.

%description -l zh_TW quick
速成輸入法，又稱簡易輸入法，為倉頡輸入法之簡化版本。
只取倉頡碼的首尾兩碼，所以一字最長只有兩碼。

包含：
速成三代、速成五代以及速成古典版。

%package scj
Summary: Smart Cangjie
Summary(zh_CN): 快速仓颉输入法
Summary(zh_TW): 快速倉頡輸入法
License:       GPLv3+
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
License:        GPLv3+
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
License:        GPLv2+
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
License:        BSD
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
License:       Freely redistributable without restriction
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
License:        GPLv3
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
License:        GPLv2
Requires:       %{name} = %{version}-%{release}

%description cantonyale
Cantonese input method based on yale romanization

%prep
%setup -q -n %{name}-%{version}
%{__sed} -i 's/\r//' tables/wubi-haifeng/COPYING

%build
sed -i '49 a LIST(INSERT CMAKE_MODULE_PATH 0 %{_datadir}/cmake/Modules/)' CMakeLists.txt
# $RPM_OPT_FLAGS should be loaded from cmake macro.
%cmake -DMANAGE_MESSAGE_LEVEL=%{message_level} -DCMAKE_FEDORA_ENABLE_FEDORA_BUILD=1 .
%__make VERBOSE=1  %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}

# Register as AppStream components to be visible in the software center
#
# NOTE: It would be *awesome* if these files were maintained by the upstream
# project, translated and installed into the right place during `make install`.
#
# See http://www.freedesktop.org/software/appstream/docs/ for more details.
#
mkdir -p $RPM_BUILD_ROOT%{_datadir}/appdata
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/stroke5.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="inputmethod">
  <id>stroke5.db</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>Stroke 5</name>
  <summary>Chinese input method</summary>
  <description>
    <p>
      Stroke 5 is a very simple stroke-based Chinese input method.
      It was designed specifically for people with limited hand mobility or computer
      literacy, like the elderly or disabled.
    </p>
    <p>
      Input methods are typing systems allowing users to input complex languages.
      They are necessary because these contain too many characters to simply be laid
      out on a traditional keyboard.
    </p>
  </description>
  <url type="homepage">https://code.google.com/p/ibus/</url>
  <url type="bugtracker">https://code.google.com/p/ibus/issues/list</url>
  <url type="help">https://code.google.com/p/ibus/wiki/FAQ</url>
  <languages>
    <lang percentage="100">zh_CN</lang>
    <lang percentage="100">zh_HK</lang>
    <lang percentage="100">zh_SG</lang>
    <lang percentage="100">zh_TW</lang>
  </languages>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/wubi-haifeng86.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="inputmethod">
  <id>wubi-haifeng86.db</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>HaiFeng Wubi 86</name>
  <summary>Simplified Chinese input method</summary>
  <description>
    <p>
      The HaiFeng Wubi 86 input method is designed for entering Simplified Chinese text.
    </p>
    <p>
      Input methods are typing systems allowing users to input complex languages.
      They are necessary because these contain too many characters to simply be laid
      out on a traditional keyboard.
    </p>
  </description>
  <url type="homepage">http://code.google.com/p/ibus/</url>
  <url type="bugtracker">https://code.google.com/p/ibus/issues/list</url>
  <url type="help">https://code.google.com/p/ibus/wiki/FAQ</url>
  <languages>
    <lang percentage="100">zh_CN</lang>
    <lang percentage="100">zh_HK</lang>
    <lang percentage="100">zh_SG</lang>
    <lang percentage="100">zh_TW</lang>
  </languages>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/wubi-jidian86.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="inputmethod">
  <id>wubi-jidian86.db</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>Jidian Wubi 86</name>
  <summary>Simplified Chinese input method</summary>
  <description>
    <p>
      The Jidian Wubi 86 input method is designed for entering Simplified Chinese text.
    </p>
    <p>
      Input methods are typing systems allowing users to input complex languages.
      They are necessary because these contain too many characters to simply be laid
      out on a traditional keyboard.
    </p>
  </description>
  <url type="homepage">http://code.google.com/p/ibus/</url>
  <url type="bugtracker">https://code.google.com/p/ibus/issues/list</url>
  <url type="help">https://code.google.com/p/ibus/wiki/FAQ</url>
  <languages>
    <lang percentage="100">zh_CN</lang>
    <lang percentage="100">zh_HK</lang>
    <lang percentage="100">zh_SG</lang>
    <lang percentage="100">zh_TW</lang>
  </languages>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF
cat > $RPM_BUILD_ROOT%{_datadir}/appdata/cantonyale.appdata.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<component type="inputmethod">
  <id>cantonyale.db</id>
  <metadata_license>CC0-1.0</metadata_license>
  <name>cantonyale</name>
  <summary>Cantonese input method based on yale romanization</summary>
  <description>
    <p>
      The cantonyale input method is designed to enter Chinese text using yale romanization.
    </p>
    <p>
      Input methods are typing systems allowing users to input complex languages.
      They are necessary because these contain too many characters to simply be laid
      out on a traditional keyboard.
    </p>
  </description>
  <url type="homepage">http://code.google.com/p/ibus/</url>
  <url type="bugtracker">https://code.google.com/p/ibus/issues/list</url>
  <url type="help">https://code.google.com/p/ibus/wiki/FAQ</url>
  <languages>
    <lang percentage="100">zh_CN</lang>
    <lang percentage="100">zh_HK</lang>
    <lang percentage="100">zh_SG</lang>
    <lang percentage="100">zh_TW</lang>
  </languages>
  <update_contact><!-- upstream-contact_at_email.com --></update_contact>
</component>
EOF

# We install document using doc 
rm -fr %{buildroot}%{_docdir}/*



%post array
%{createdb} -i -n %{ibus_tables_dir}/array30.db
%{createdb} -i -n %{ibus_tables_dir}/array30-big.db

%post cangjie
%{createdb} -i -n %{ibus_tables_dir}/cangjie3.db
%{createdb} -i -n %{ibus_tables_dir}/cangjie5.db
%{createdb} -i -n %{ibus_tables_dir}/cangjie-big.db

%post cantonese
%{createdb} -i -n %{ibus_tables_dir}/cantonese.db
%{createdb} -i -n %{ibus_tables_dir}/cantonhk.db
%{createdb} -i -n %{ibus_tables_dir}/jyutping.db

%post easy
%{createdb} -i -n %{ibus_tables_dir}/easy-big.db

%post erbi
%{createdb} -i -n %{ibus_tables_dir}/erbi.db
%{createdb} -i -n %{ibus_tables_dir}/erbi-qs.db

%post quick
%{createdb} -i -n %{ibus_tables_dir}/quick3.db
%{createdb} -i -n %{ibus_tables_dir}/quick5.db
%{createdb} -i -n %{ibus_tables_dir}/quick-classic.db

%post scj
%{createdb} -i -n %{ibus_tables_dir}/scj6.db

%post stroke5
%{createdb} -i -n %{ibus_tables_dir}/stroke5.db

%post wu
%{createdb} -i -n %{ibus_tables_dir}/wu.db

%post wubi-haifeng
%{createdb} -i -n %{ibus_tables_dir}/wubi-haifeng86.db

%post wubi-jidian
%{createdb} -i -n %{ibus_tables_dir}/wubi-jidian86.db

%post yong
%{createdb} -i -n %{ibus_tables_dir}/yong.db

%post cantonyale
%{createdb} -i -n %{ibus_tables_dir}/cantonyale.db

%files
%doc 

%files array
%{ibus_icons_dir}/array30.*
%verify(not size md5 mtime) %{ibus_tables_dir}/array30.db
%{ibus_icons_dir}/array30-big.*
%verify(not size md5 mtime) %{ibus_tables_dir}/array30-big.db

%files cangjie
%{ibus_icons_dir}/cangjie3.*
%verify(not size md5 mtime) %{ibus_tables_dir}/cangjie3.db
%{ibus_icons_dir}/cangjie5.*
%verify(not size md5 mtime) %{ibus_tables_dir}/cangjie5.db
%{ibus_icons_dir}/cangjie-big.*
%verify(not size md5 mtime) %{ibus_tables_dir}/cangjie-big.db

%files cantonese
%{ibus_icons_dir}/cantonese.*
%verify(not size md5 mtime) %{ibus_tables_dir}/cantonese.db
%{ibus_icons_dir}/cantonhk.*
%verify(not size md5 mtime) %{ibus_tables_dir}/cantonhk.db
%{ibus_icons_dir}/jyutping.*
%verify(not size md5 mtime) %{ibus_tables_dir}/jyutping.db

%files easy
%{ibus_icons_dir}/easy-big.*
%verify(not size md5 mtime) %{ibus_tables_dir}/easy-big.db

%files erbi
%{ibus_icons_dir}/erbi.*
%verify(not size md5 mtime) %{ibus_tables_dir}/erbi.db
%{ibus_icons_dir}/erbi-qs.*
%verify(not size md5 mtime) %{ibus_tables_dir}/erbi-qs.db

%files quick
%{ibus_icons_dir}/quick3.*
%verify(not size md5 mtime) %{ibus_tables_dir}/quick3.db
%{ibus_icons_dir}/quick5.*
%verify(not size md5 mtime) %{ibus_tables_dir}/quick5.db
%{ibus_icons_dir}/quick-classic.*
%verify(not size md5 mtime) %{ibus_tables_dir}/quick-classic.db

%files scj
%{ibus_icons_dir}/scj6.*
%verify(not size md5 mtime) %{ibus_tables_dir}/scj6.db

%files stroke5
%{_datadir}/appdata/stroke5.appdata.xml
%{ibus_icons_dir}/stroke5.*
%verify(not size md5 mtime) %{ibus_tables_dir}/stroke5.db

%files wu
%{ibus_icons_dir}/wu.*
%verify(not size md5 mtime) %{ibus_tables_dir}/wu.db

%files wubi-haifeng
%{_datadir}/appdata/wubi-haifeng86.appdata.xml
%doc tables/wubi-haifeng/COPYING tables/wubi-haifeng/README
%{ibus_icons_dir}/wubi-haifeng86.*
%verify(not size md5 mtime) %{ibus_tables_dir}/wubi-haifeng86.db

%files wubi-jidian
%{_datadir}/appdata/wubi-jidian86.appdata.xml
%{ibus_icons_dir}/wubi-jidian86.*
%verify(not size md5 mtime) %{ibus_tables_dir}/wubi-jidian86.db

%files yong
%{ibus_icons_dir}/yong.*
%{ibus_tables_dir}/yong.db

%files cantonyale
%{_datadir}/appdata/cantonyale.appdata.xml
%{ibus_icons_dir}/cantonyale.*
%verify(not size md5 mtime) %{ibus_tables_dir}/cantonyale.db

%changelog
* Thu Jun 17 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.8.3-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Supplement CMake module search path with the location of cmake-fedora's modules

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

