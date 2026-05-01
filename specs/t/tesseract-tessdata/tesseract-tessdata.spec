# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global commit 7274cfad453d770f36b53ec5a2294ddd6d905703
#global shortcommit %(c=%{commit}; echo ${c:0:7})

#global pre beta.1

Name:          tesseract-tessdata
Version:       4.1.0
Release:       11%{?pre:.%pre}%{?commit:.git%{shortcommit}}%{?dist}
Summary:       Trained models for the Tesseract Open Source OCR Engine
BuildArch:     noarch

License:       Apache-2.0
URL:           https://github.com/tesseract-ocr/tessdata_fast
%if 0%{?commit:1}
Source0:       https://github.com/tesseract-ocr/tessdata_fast/archive/%{commit}/tessdata_fast-%{shortcommit}.tar.gz
%else
Source0:       https://github.com/tesseract-ocr/tessdata_fast/archive/%{version}%{?pre:-%pre}/tessdata_fast-%{version}%{?pre:-%pre}.tar.gz
%endif


%description
This package contains fast integer versions of trained models for the Tesseract
Open Source OCR Engine.

These models only work with the LSTM OCR engine of Tesseract 4.


%package        doc
Summary:        Documentation for %{name}

%description    doc
The %{name}-doc package contains the documentation for %{name}.


%package -n tesseract-osd
Summary:       Orientation & Script Detection Data for tesseract
BuildArch:     noarch
Requires:      tesseract
Requires:      %{name}-doc = %{version}-%{release}

%description -n tesseract-osd
Orientation & Script Detection data for the Tesseract Open Source OCR Engine.


%package -n tesseract-equ
Summary:       Equation traineddata for tesseract
BuildArch:     noarch
Requires:      tesseract
Requires:      %{name}-doc = %{version}-%{release}

%description -n tesseract-equ
Data for processing images of mathematics with the Tesseract Open Source OCR Engine.


# define lang_subpkg macro
# m: 3 letter macrolanguage code
# l: langcode used in Provides and Supplements tags
# n: language name
# -m and -n is needed for subpackages, -l is optional
#
%define lang_subpkg(l:m:n:) \
%define macrolang %{-m:%{-m*}}%{!-m:%{error:3 letter Language code not defined}} \
%define langcode %{-l:%{-l*}}%{!-l:%{error:Language code not defined}} \
%define langname %{-n:%{-n*}}%{!-n:%{error:Language name not defined}} \
\
%package -n tesseract-langpack-%{macrolang}\
Summary:       %{langname} language data for %{name}\
BuildArch:     noarch\
Requires:      tesseract-common\
Requires:      %{name}-doc = %{version}-%{release}\
%{-l:Provides:      %{name}-langpack-%{langcode} = %{version}-%{release}\
Supplements:   (tesseract and langpacks-%{langcode})}\
\
%description -n tesseract-langpack-%{macrolang}\
This package contains the fast integer version of the %{langname} language \
trained models for the Tesseract Open Source OCR Engine.\
\
%files -n tesseract-langpack-%{macrolang}\
%{_datadir}/tesseract/tessdata/%{macrolang}.*

# define script_subpkg macro
# s: script name
# n: package name
#
%define script_subpkg(s:n:) \
%define scriptname %{-s:%{-s*}}%{!-s:%{error:Script name defined}} \
%define filename %{-n:%{-n*}}%{!-n:%{error:Package name not defined}} \
%define pkgname %(echo %filename | tr '[:upper:]' '[:lower:]') \
\
%package -n tesseract-script-%{pkgname}\
Summary:       %{scriptname} script data for %{name}\
BuildArch:     noarch\
Requires:      tesseract-common\
Requires:      %{name}-doc = %{version}-%{release}\
\
%description -n tesseract-script-%{pkgname}\
This package contains the fast integer version of the %{scriptname} script \
trained models for the Tesseract Open Source OCR Engine.\
\
%files -n tesseract-script-%{pkgname}\
%dir %{_datadir}/tesseract/tessdata/script/\
%{_datadir}/tesseract/tessdata/script/%{filename}.*

# see https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
# and https://en.wikipedia.org/wiki/List_of_ISO_639-2_codes
%lang_subpkg -m afr -l af -n Afrikaans
%lang_subpkg -m amh -l an -n Amharic
%lang_subpkg -m ara -l ar -n Arabic
%lang_subpkg -m asm -l as -n Assamese
%lang_subpkg -m aze -l az -n Azerbaijani
%lang_subpkg -m aze_cyrl -n %{quote:Azerbaijani (Cyrillic)}
%lang_subpkg -m bel -l bel -n Belarusian
%lang_subpkg -m ben -l bn -n Bengali
%lang_subpkg -m bod -l bo -n %{quote:Tibetan (Standard)}
%lang_subpkg -m bos -l bs -n Bosnian
%lang_subpkg -m bre -l br -n Breton
%lang_subpkg -m bul -l bg -n Bulgarian
%lang_subpkg -m cat -l ca -n Catalan
%lang_subpkg -m ceb -n Cebuano
%lang_subpkg -m ces -l cs -n Czech
%lang_subpkg -m chi_sim -l zh_CN -n %{quote:Chinese (Simplified)}
%lang_subpkg -m chi_sim_vert -l zh_CN -n %{quote:Chinese (Simplified, Vertical)}
%lang_subpkg -m chi_tra -l zh_TW -n %{quote:Chinese (Traditional)}
%lang_subpkg -m chi_tra_vert -l zh_TW -n %{quote:Chinese (Traditional, Vertical)}
%lang_subpkg -m chr -n Cherokee
%lang_subpkg -m cos -l co -n Corsican
%lang_subpkg -m cym -l cy -n Welsh
%lang_subpkg -m dan -l da -n Danish
%lang_subpkg -m deu -l de -n German
%lang_subpkg -m div -l dv -n %{quote:Dhivehi; Maldivian}
%lang_subpkg -m dzo -n Dzongkha
%lang_subpkg -m ell -l el -n Greek
%lang_subpkg -m eng -n English
%lang_subpkg -m enm -n %{quote:Middle English (1100-1500)}
%lang_subpkg -m epo -l eo -n Esperanto
%lang_subpkg -m est -l et -n Estonian
%lang_subpkg -m eus -l eu -n Basque
%lang_subpkg -m fao -l fo -n %{quote:Faroese}
%lang_subpkg -m fas -l fa -n %{quote:Persian (Farsi)}
%lang_subpkg -m fil -n %{quote:Filipino; Pilipino}
%lang_subpkg -m fin -l fi -n Finnish
%lang_subpkg -m fra -l fr -n French
%lang_subpkg -m frk -n Fraktur
%lang_subpkg -m frm -n %{quote:Middle French (ca. 1400-1600)}
%lang_subpkg -m fry -l fy -n %{quote:Western Frisian}
%lang_subpkg -m gla -l gd -n %{quote:Gaelic; Scottish Gaelic}
%lang_subpkg -m gle -l ga -n Irish
%lang_subpkg -m glg -l gl -n Galician
%lang_subpkg -m grc -n %{quote:Ancient Greek}
%lang_subpkg -m guj -l gu -n Gujarati
%lang_subpkg -m hat -l ht -n Haitian
%lang_subpkg -m heb -l he -n Hebrew
%lang_subpkg -m hin -l hi -n Hindi
%lang_subpkg -m hrv -l hr -n Croatian
%lang_subpkg -m hun -l hu -n Hungarian
%lang_subpkg -m hye -l hy -n Armenian
%lang_subpkg -m iku -l iu -n Inuktitut
%lang_subpkg -m ind -l id -n Indonesian
%lang_subpkg -m isl -l is -n Icelandic
%lang_subpkg -m ita -l it -n Italian
%lang_subpkg -m ita_old -n %{quote:Italian (Old)}
%lang_subpkg -m jav -l jav -n Javanese
%lang_subpkg -m jpn -l ja -n Japanese
%lang_subpkg -m jpn_vert -l ja -n "Japanese (Vertical)"
%lang_subpkg -m kan -l kn -n Kannada
%lang_subpkg -m kat -l ka -n Georgian
%lang_subpkg -m kat_old -n %{quote:Georgian (Old)}
%lang_subpkg -m kaz -l kk -n Kazakh
%lang_subpkg -m khm -l km -n Khmer
%lang_subpkg -m kir -l ky -n Kyrgyz
%lang_subpkg -m kor -l ko -n Korean
%lang_subpkg -m kor_vert -l ko -n "Korean (Vertical)"
%lang_subpkg -m kmr -l ku -n Kurmanji
%lang_subpkg -m lao -l lo -n Lao
%lang_subpkg -m lat -l lat -n Latin
%lang_subpkg -m lav -l lv -n Latvian
%lang_subpkg -m lit -l lt -n Lithuanian
%lang_subpkg -m ltz -l lb -n Luxembourgish
%lang_subpkg -m mal -l ml -n Malayalam
%lang_subpkg -m mar -l mr -n Marathi
%lang_subpkg -m mkd -l mk -n Macedonian
%lang_subpkg -m mlt -l mt -n Maltese
%lang_subpkg -m mon -l mn -n Mongolian
%lang_subpkg -m mri -l mi -n Maori
%lang_subpkg -m msa -l ms -n Malay
%lang_subpkg -m mya -l my -n Burmese
%lang_subpkg -m nep -l ne -n Nepali
%lang_subpkg -m nld -l nl -n Dutch
%lang_subpkg -m nor -l no -n Norwegian
%lang_subpkg -m oci -l oc -n Occitan
%lang_subpkg -m ori -l or -n Oriya
%lang_subpkg -m pan -l pa -n Panjabi
%lang_subpkg -m pol -l pl -n Polish
%lang_subpkg -m por -l pt -n Portuguese
%lang_subpkg -m pus -l ps -n Pashto
%lang_subpkg -m que -l qu -n Quechuan
%lang_subpkg -m ron -l ro -n Romanian
%lang_subpkg -m rus -l ru -n Russian
%lang_subpkg -m san -l sa -n Sanskrit
%lang_subpkg -m sin -l si -n Sinhala
%lang_subpkg -m slk -l sk -n Slovakian
%lang_subpkg -m slv -l sl -n Slovenian
%lang_subpkg -m snd -l sd -n Sindhi
%lang_subpkg -m spa -l es -n Spanish
%lang_subpkg -m spa_old -n %{quote:Spanish (Old)}
%lang_subpkg -m sqi -l sq -n Albanian
%lang_subpkg -m srp -l sr -n Serbian
%lang_subpkg -m srp_latn -n %{quote:Serbian (Latin)}
%lang_subpkg -m sun -l su -n Sundanese
%lang_subpkg -m swa -l sw -n Swahili
%lang_subpkg -m swe -l sv -n Swedish
%lang_subpkg -m syr -l ar_SY -n Syriac
%lang_subpkg -m tam -l ta -n Tamil
%lang_subpkg -m tat -l tt -n Tatar
%lang_subpkg -m tel -l te -n Telugu
%lang_subpkg -m tgk -l tg -n Tajik
%lang_subpkg -m tha -l th -n Thai
%lang_subpkg -m tir -l ti -n Tigrinya
%lang_subpkg -m ton -l to -n Tongan
%lang_subpkg -m tur -l tr -n Turkish
%lang_subpkg -m uig -l ug -n Uyghur
%lang_subpkg -m ukr -l uk -n Ukrainian
%lang_subpkg -m urd -l ur -n Urdu
%lang_subpkg -m uzb -l uz -n Uzbek
%lang_subpkg -m uzb_cyrl -n %{quote:Uzbek (Cyrillic)}
%lang_subpkg -m vie -l vi -n Vietnamese
%lang_subpkg -m yid -l yi -n Yiddish
%lang_subpkg -m yor -l yo -n Yoruba

%script_subpkg -n Arabic -s Arabic
%script_subpkg -n Armenian -s Armenian
%script_subpkg -n Bengali -s Bengali
%script_subpkg -n Canadian_Aboriginal -s %{quote:Canadian (Aboriginal)}
%script_subpkg -n Cherokee -s Cherokee
%script_subpkg -n Cyrillic -s Cyrillic
%script_subpkg -n Devanagari -s Devanagari
%script_subpkg -n Ethiopic -s Ethiopic
%script_subpkg -n Fraktur -s Fraktur
%script_subpkg -n Georgian -s Georgian
%script_subpkg -n Greek -s Greek
%script_subpkg -n Gujarati -s Gujarati
%script_subpkg -n Gurmukhi -s Gurmukhi
%script_subpkg -n HanS -s %{quote:Han (Simplified)}
%script_subpkg -n HanS_vert -s %{quote:Han (Simplified, Vertical)}
%script_subpkg -n HanT -s %{quote:Han (Traditional)}
%script_subpkg -n HanT_vert -s %{quote:Han (Traditional, Vertical)}
%script_subpkg -n Hangul -s Hangul
%script_subpkg -n Hangul_vert -s %{quote:Hangul (Vertical)}
%script_subpkg -n Hebrew -s Hebrew
%script_subpkg -n Japanese -s Japanese
%script_subpkg -n Japanese_vert -s %{quote:Japanese (Vertical)}
%script_subpkg -n Kannada -s Kannada
%script_subpkg -n Khmer -s Khmer
%script_subpkg -n Lao -s Lao
%script_subpkg -n Latin -s Latin
%script_subpkg -n Malayalam -s Malayalam
%script_subpkg -n Myanmar -s Myanmar
%script_subpkg -n Oriya -s Oriya
%script_subpkg -n Sinhala -s Sinhala
%script_subpkg -n Syriac -s Syriac
%script_subpkg -n Tamil -s Tamil
%script_subpkg -n Telugu -s Telugu
%script_subpkg -n Thaana -s Thaana
%script_subpkg -n Thai -s Thai
%script_subpkg -n Tibetan -s Tibetan
%script_subpkg -n Vietnamese -s Vietnamese


%prep
%if 0%{?commit:1}
%autosetup -p1 -n tessdata_fast-%{commit}
%else
%autosetup -p1 -n tessdata_fast-%{version}%{?pre:-%pre}
%endif


%build
# Nothing to build


%install
mkdir -p %{buildroot}/%{_datadir}/tesseract/tessdata/
cp -a * %{buildroot}/%{_datadir}/tesseract/tessdata/

# Install these through %%license and %%doc
rm -f %{buildroot}/%{_datadir}/tesseract/tessdata/LICENSE
rm -f %{buildroot}/%{_datadir}/tesseract/tessdata/README.md

# https://github.com/tesseract-ocr/tessdata_fast/issues/27
rm -f %{buildroot}/%{_datadir}/tesseract/tessdata/configs
rm -f %{buildroot}/%{_datadir}/tesseract/tessdata/pdf.ttf



%files doc
%license LICENSE
%doc README.md

%files -n tesseract-osd
%{_datadir}/tesseract/tessdata/osd.traineddata

%files -n tesseract-equ
%{_datadir}/tesseract/tessdata/equ.traineddata


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon May 12 2025 Sandro Mani <manisandro@gmail.com> - 4.1.0-10
- Require tesseract-common from langpack/script packages

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Feb 17 2021 Sandro Mani <manisandro@gmail.com> - 4.1.0-1
- Update to 4.1.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 29 2020 Sandro Mani <manisandro@gmail.com> - 4.0.0-9
- Fix supplements

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Sandro Mani <manisandro@gmail.com> - 4.0.0-5
- Improve subpackage descriptions
- Make script subpackages own the script directory
- Bump release to -5

* Wed Jul 17 2019 Sandro Mani <manisandro@gmail.com> - 4.0.0-2
- Make all langpack / script subpackages require tesseract for tessdata dir ownership
- Fix tesseract-osd requires
- Fix typo cirilic -> cyrillic

* Tue Jul 16 2019 Sandro Mani <manisandro@gmail.com> - 4.0.0-1
- Initial package split from the tesseract package
