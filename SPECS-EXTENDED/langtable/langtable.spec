Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           langtable
Version:        0.0.68
Release:        3%{?dist}
Summary:        Guessing reasonable defaults for locale, keyboard layout, territory, and language.
# the translations in languages.xml and territories.xml are (mostly)
# imported from CLDR and are thus under the Unicode license, the
# short name for this license is "MIT", see:
# https://fedoraproject.org/wiki/Licensing:MIT?rd=Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29
License:        GPL-3.0-or-later
URL:            https://github.com/mike-fabian/langtable
Source0:        https://github.com/mike-fabian/langtable/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl-interpreter
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description
langtable is used to guess reasonable defaults for locale, keyboard layout,
territory, and language, if part of that information is already known. For
example, guess the territory and the keyboard layout if the language
is known or guess the language and keyboard layout if the territory is
already known.

%package -n python3-langtable
Summary:        Python module to query the langtable-data
License:        GPL-3.0-or-later
Requires:       %{name} = %{version}-%{release}
Obsoletes:      %{name}-data < %{version}-%{release}
Provides:       %{name}-data = %{version}-%{release}
%{?python_provide:%python_provide python3-%{name}}

%description -n python3-langtable
This package contains a Python module to query the data
from langtable-data.

%prep
%setup -q

%build
perl -pi -e "s,_DATADIR = '(.*)',_DATADIR = '%{_datadir}/langtable'," langtable/langtable.py

%py3_build

%install

%py3_install

%check
(cd $RPM_BUILD_DIR/%{name}-%{version}/langtable; %{__python3} langtable.py)
(cd $RPM_BUILD_DIR/%{name}-%{version}; %{__python3} test_cases.py)
xmllint --noout --relaxng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/schemas/keyboards.rng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/data/keyboards.xml
xmllint --noout --relaxng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/schemas/languages.rng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/data/languages.xml
xmllint --noout --relaxng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/schemas/territories.rng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/data/territories.xml
xmllint --noout --relaxng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/schemas/timezoneidparts.rng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/data/timezoneidparts.xml
xmllint --noout --relaxng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/schemas/timezones.rng \
        $RPM_BUILD_DIR/%{name}-%{version}/langtable/data/timezones.xml

%files
%license COPYING unicode-license.txt
%doc README* ChangeLog test_cases.py langtable/schemas/*.rng

%files -n python3-langtable
%dir %{python3_sitelib}/langtable
%{python3_sitelib}/langtable/*
%dir %{python3_sitelib}/langtable-*.egg-info
%{python3_sitelib}/langtable-*.egg-info/*

%changelog
* Mon Apr 07 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.0.68-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.68-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Mike FABIAN <mfabian@redhat.com> - 0.0.68-1
- Update to 0.0.68
- Reorder ibus/chewing as the default inputmethod for TW or Hant. Resolves:
  https://github.com/mike-fabian/langtable/pull/22 See:
  https://fedoraproject.org/wiki/Changes/IBusChewingForZhTW
- Add ltg_LV.UTF-8

* Tue Jun 11 2024 Python Maint <python-maint@redhat.com> - 0.0.67-2
- Rebuilt for Python 3.13

* Tue Jun 11 2024 Mike FABIAN <mfabian@redhat.com> - 0.0.67-1
- Update to 0.0.67
- Add tool to check which languages, scripts, and territories available in
  CLDR are missing in langtable
- Add all missing scripts and languages: yrl, xnr, wbp, vmw, vec, trw, trv,
  skr, sdh, quc, pis, pcm, myv, mus, moh, mic, mhn, ltg, lmo, lld, kxv,
  kpe, kgp, ken, kcg, kaj, jbo, gaa, cic, cho, ceb, cch, cad, bss, blt,
  Tavt blo, bgn, bgc, rhg, Rohg hnj, Hmnp Shaw, Dsrt bew, bal, arn, apc,
  ann, scn
- Drop Python < 3 support (using pyupgrade --py3-plus langtable.py)
- Fix some ruff and pylint warnings

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.0.66-2
- Rebuilt for Python 3.13

* Tue May 07 2024 Mike FABIAN <mfabian@redhat.com> - 0.0.66-1
- Update to 0.0.66
- Fix syntax error in a keyboard layout name for th (Resolves:
  https://github.com/mike-fabian/langtable/issues/21xs)
- Add mdf
- Use “in(eng)” keyboard layout instead of “us” for BD to get AltGr enabled
- Get translation changes from CLDR
- Add option to include changed translations as well to the script getting
  translations from CLDR
- Add reference to the the PyPI package to the README.md. And add a
  README.html and README generated from the README.md.
- Make test outputs somewhat more verbose, even when all tests pass
  (Resolves: https://github.com/mike-fabian/langtable/pull/20). Thanks to
  Sebastian <seb128@ubuntu.com> for the pull request.
- Fix Makefile twine-upload target for new authentification

* Thu Feb 08 2024 Mike FABIAN <mfabian@redhat.com> - 0.0.65-1
- Update to 0.0.65
- Add wuu, tok, glk, gbm, ssy
- Remove aa_ER.UTF-8@saaho
- Add kv_RU.UTF-8, chr_RU.UTF-8
- Add EU, EZ
- Improve README and Makefile (Resolves: https://github.com/mike-
  fabian/langtable/issues/19)
- Add more translations from CLDR
- Get translation changes from CLDR

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.64-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Mike FABIAN <mfabian@redhat.com> - 0.0.64-1
- Update to 0.0.64
- Add new public functions list_all_{languages,locales,keyboards,territories,timezones,scripts,input_methods,console_fonts}
  (See also the discussion at: https://gitlab.gnome.org/GNOME/gnome-desktop/-/merge_requests/159)

* Mon Aug 28 2023 Mike FABIAN <mfabian@redhat.com> - 0.0.63-1
- Update to 0.0.63
- Add more translations from CLDR
- Get translation changes from CLDR
- Japanese: prefer anthy over kkc
  (Thanks to adam Williamson: https://github.com/mike-fabian/langtable/pull/17)
- Use skipTerritory also in list_keyboards(), list_consolefonts(), and list_timezones()
  (Resolves: https://github.com/mike-fabian/langtable/issues/18)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.0.62-2
- Rebuilt for Python 3.12

* Tue May 02 2023 Mike FABIAN <mfabian@redhat.com> - 0.0.62-1
- Update to 0.0.62
- Get translation changes from CLDR
- Add more translations from CLDR
- Add Norwegian keyboard layout to keyboards.xml
  (Resolves: https://github.com/mike-fabian/langtable/issues/16)
- Add Hang script to Southern Aymara

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.61-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 28 2022 Mike FABIAN <mfabian@redhat.com> - 0.0.61-2
- Migrate license tag of python3-langtable to SPDX as well

* Thu Nov 24 2022 Mike FABIAN <mfabian@redhat.com> - 0.0.61-1
- Update to 0.0.61
- Add mnw_MM.UTF-8 and ckb_IQ.UTF-8
- Do not run test cases using Python2 anymore
- Add bih
- Add more translations from CLDR
- Migrate license tag to SPDX

* Wed Sep 21 2022 Mike FABIAN <mfabian@redhat.com> - 0.0.60-1
- Update to 0.0.60
- Add list_common_locales() function
  (Resolves: https://github.com/mike-fabian/langtable/issues/15)
- For ar_IN locale, langtable should give the 'ara' keyboard layout as the first choice
  (Resolves: Resolves: https://github.com/mike-fabian/langtable/issues/14)

* Tue Sep 06 2022 Mike FABIAN <mfabian@redhat.com> - 0.0.59-1
- Update to 0.0.59
- Add ibus/m17n:ar:kbd as input method for Arabic and fix iso639-1 code for Arabic
- Get translation changes from CLDR
- Add more translations from CLDR

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.58-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.0.58-2
- Rebuilt for Python 3.11

* Thu Apr 21 2022 Mike FABIAN <mfabian@redhat.com> - 0.0.58-1
- Update to 0.0.58
- Add syr locale
- Get translation changes from CLDR
- Add more translations from CLDR
- Fix names for keyboard layouts which have changed
- Add ab_GE locale
- Add rif language

* Tue Jan 25 2022 Mike FABIAN <mfabian@redhat.com> - 0.0.57-1
- Update to 0.0.57
- Get translation changes from CLDR
- Add more translations from CLDR
- Replace “ibus/cangjie” with “ibus/table:cangjie5”
- Updates for Sami languages (from Marko Myllynen)
- Updates for Finnish keyboard layouts (from Marko Myllynen)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 16 2021 Mike FABIAN <mfabian@redhat.com> - 0.0.56-1
- Update to 0.0.56
- Fallback to translations in “xx” from “xx_Zzzz”
  only if “Zzzz” is the main script of “xx”
  (Resolves: https://github.com/mike-fabian/langtable/issues/13)
- Get translation changes for mt from CLDR

* Wed Aug 11 2021 Mike FABIAN <mfabian@redhat.com> - 0.0.55-1
- Update to 0.0.55
- Get translation changes from CLDR
- Add more translations from CLDR
- Make inscript2 instead of inscript input methods the default
  (See: https://fedoraproject.org/wiki/Changes/Enhanced_Inscript_as_default_Indic_IM)
- Make ibus/m17n:vi:telex the default input method for Vietnamese

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.54-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.0.54-3
- Rebuilt for Python 3.10

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.54-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 29 2020 Mike FABIAN <mfabian@redhat.com> - 0.0.54-1
- Update to 0.0.54
- add list_common_languages derived from gnome-control-center
  by Sundeep ANAND <suanand@redhat.com>

* Tue Sep 15 2020 Mike FABIAN <mfabian@redhat.com> - 0.0.53-1
- Update to 0.0.53
- Capitalize the return values of language_name() and territory_name()
  (See: https://github.com/rhinstaller/anaconda/pull/2837).
- Add more translations from CLDR
- Get translation changes from CLDR

* Tue Aug 18 2020 Mike FABIAN <mfabian@redhat.com> - 0.0.52-1
- Update to 0.0.52
- add list_common_keyboards() to public api by Sundeep ANAND <suanand@redhat.com>

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.51-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.51-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.51-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Mike FABIAN <mfabian@redhat.com> - 0.0.51-1
- Parse stuff in glibc locale names after @ which is not a script as a variant
- Add ckb_IQ.UTF-8 locale

* Fri Dec 20 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.50-1
- Make parse_locale() return something reasonable for
  C, POSIX, en_US_POSIX, and C.UTF-8
- Fix exception in language_name() when called with languageId=''
  (noticed by Marco Myllynen, thank you!)

* Fri Dec 13 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.49-1
- Add new public function parse_locale()
- Let info() print a bit more stuff

* Tue Nov 05 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.48-1
- Fix typo in mo entry
- Add mnw
- Fix translation of IN in te

* Sun Sep 29 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.47-1
- Three changed translations into sr_Latn from CLDR
- Add translations of PL in csb and szl (from native speakers)
- Add tools/compare_with_glib_source.py script to compare stuff with glibc
- Add translation of DZ in ber
- Add translation for MA in ber, ber_Tfng, ber_MA
- Add translation of MX in nah and nhn
- Add translation of NP in the
- Add translation for PH in tl
- Fix translation of IN in te
- Add translation of MM in shn
- Add translation of IN in sat
- Add translation of IR in az_Arab, az_IR
- Add translation for NU in niu
- Add translation of PE in ayc (from glibc)
- Add translation of PE in agr (from glibc)
- Fix translation of RU into tt
- Fix translation of ZA in xh
- Add translation of IN in mni (from glibc)
- Add translation of CA in iu (from glibc)
- Add translation of ET in sid (from glibc)
- Add translations of ER and ET in gez (from glibc)
- Add translation of ZA in nr, nso, ss, st, tn, ts, ve (from glibc)
- Add translation of MV in dv (from glibc)
- Add translation of CA in ik (from glibc)
- Add translation of IN in mjw (from glibc)
- Add translations of TW in cmn, hak, nan, nan_Latn (from glibc)
- Fix translation of BY in be_Latn to agree with glibc
- Add translation of NP in bho
- Add translation of IN in bhb, bho, doi, hif, hne, ks_Deva, mag, raj, sa, sd_Deva
- Use "Crimean Tatar" instead of "Crimean Turkish" as English translation for crh
- Use Shuswap instead of "Shuswap langauge" as the English translation of shs
- Correct capitalization of endonym for ss
- Fix translations of sr_Latn and sr_Cyrl into sr_Latn
- Use standard translations of zh and yue from cldr, not the alt='menu' variant
- Fix endonym of uz_Cyrl to agree with glibc and cldr
- Change endonym for tcy to agree with glibc (cldr does not have tcy)
- Change endonym for sid to agree with glibc (cldr does not have sid)
- Change endonym for sgs to agree with glibc (cldr does not have sgs)
- Give Olck higher priority than Deva for sat
- Change endonym for lzh to agree with glibc
- Change endonym for csb to agree with glibc
- Change endonym for cmn_Hans from 官话 to 汉语官话 and for cmn_Hant from 官話 to 漢語官話
- Add endonym for ber_MA
- Add endonym for az_Arab, az_IR (from az_IR in glibc)
- Add endonym for fy_NL
- Fix endonym for nhn and add English name for nhn
- Fix endonym for pa_Arab (agrees with CLDR now)

* Wed Sep 04 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.46-1
- Add some documentation about the parsing of languageId
- Adapt test cases to translation changes from CLDR
- Get translation changes from CLDR
- Add more translations from CLDR
- More test cases
- Add optional boolean parameter “fallback” in language_name() and territory_name()
- Add translation of ES in an
- Add dummy translation of IN in ks_Deva
- Add endonyms for ik, iu, cv, csb, crh, an, ayc, ber, bho
- Add translation of IT in lij
- Add endonym for nan_Latn
- Add endonym for oc and translation of FR in oc
- Add translations of AW and CW in pap
- Add endonyms for sat, sa, quz
- Add translation of IT in sc
- Add dummy translation of IN in sd_Deva
- Add endonyms for sid, the
- Add translations of “Tok Pisin” and “Papua New Guinea” in the Tok Pisin language
- Add translations of “Walloon” and “Belgium” in the Walloon language
- Some comments in Makefile

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.45-4
- Rebuilt for Python 3.8

* Tue Jul 30 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.45-3
- Add “Provides: langtable-data”

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.45-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.45-1
- Add python_provide macro to make the switch from Python 2 to
  Python 3 automatic (Resolves: rhbz#1717341)
- Use “us(intl)” keyboard instead of “us” as the default for af and ZA
  (Resolves: https://github.com/mike-fabian/langtable/issues/9)
- Add za keyboard layout for nso, tn, ve
  (Resolves: https://github.com/mike-fabian/langtable/issues/10)
- “us” is a possible layout for “ZA”, it is used by default for “zu” for example
- Return number of failed tests in test_cases.py doctests.

* Fri May 31 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.44-2
- Obsolete langtable-data

* Fri May 31 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.44-1
- Use setuptools instead of distutils
- Add a version() function and an info() function.
- Restructure langtable project a bit to be able to upload to PyPi
- Increase the rank of zh_SG.UTF-8 back to 10 again for languageId="zh"
- Remove old provides and obsoletes

* Fri May 10 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.43-1
- Get translation changes from CLDR
- Add some new translations from CLDR
- Add dsb_DE.UTF-8 sah_RU.UTF-8 locales
- Fix ranks for "en" and "zh" in "SG", English should be the default for "SG"
- Reduce the rank of cmn_TW.UTF-8 and zh_SG.UTF-8 to 0 for languageId="zh"
  (Resolves: https://github.com/mike-fabian/langtable/issues/8)

* Mon Apr 08 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.42-1
- Add special support for languageId ca_ES_VALENCIA (Resolves: rhbz#1698984)

* Fri Mar 08 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.41-3
- Remove python2-langtable subpackage (Resolves: rhbz#1686395)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.41-1
- The territory can be 2 upper case letters *or* 3 digits
- Get translation changes from CLDR
- Add many languages and territories and also add new translations from CLDR

* Mon Jan 07 2019 Mike FABIAN <mfabian@redhat.com> - 0.0.40-1
- Add Esperanto locale and test case
  (Thanks to Carmen Bianca Bakker <carmen@carmenbianca.eu>).
- Add sel

* Thu Nov 08 2018 Mike FABIAN <mfabian@redhat.com> - 0.0.39-2
- Remove unnecessary LC_CTYPE=en_US.UTF-8 in check section.

* Mon Oct 15 2018 Mike FABIAN <mfabian@redhat.com> - 0.0.39-1
- Add the new keyboard layout "au" for Australia (same as "us")
- Add locales missing in languages.xml, territiories.xml or in both.
- Add ibus/libzhuyin and make it the default for TW.
- Add cmn_TW.UTF-8 to the Chinese locales
- Add several missing  languages (Resolves: rhbz#1631214):
  ab av bin bm bua ch co cu ee fat gn ho hz ie ii io kaa ki kj kr kum
  kwm lah lez mh mo na ng nqo nv ota rm rn sco sg sh sma smn sms sn su
  syr tw ty tyv vo vot wen yap za

* Tue Jul 17 2018 Miro Hrončok <mhroncok@redhat.com> - 0.0.38-8
- Update Python macros to new packaging standards
  (See https://fedoraproject.org/wiki/Changes/Move_usr_bin_python_into_separate_package)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.38-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.0.38-6
- Rebuilt for Python 3.7

* Tue Apr 10 2018 Pete Walter <pwalter@fedoraproject.org> - 0.0.38-5
- Conditionally add back Python 2 subpackage on Fedora
- Rename Python 3 subpackage to python3-langtable to follow guidelines
- Resolves: rhbz#1559099

* Wed Apr 04 2018 Mike FABIAN <mfabian@redhat.com> - 0.0.38-4
- Drop Python 2 subpackage
- Resolves: rhbz#1559099

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.38-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 06 2017 Mike FABIAN <mfabian@redhat.com> - 0.0.38-2
- Make "tw" the default keyboard layout for zh_TW and cmn_TW
- Resolves: rhbz#1387825

* Mon Nov 06 2017 Mike FABIAN <mfabian@redhat.com> - 0.0.38-1
- Add some new translations from CLDR
- Add agr, bi, hif, kab, mfe, miq, mjw, shn, sm, to, tpi_PG, yuw, AS, MU, SC, TO, VU, WS

* Wed Sep 27 2017 Troy Dawson <tdawson@redhat.com> - 0.0.37-4
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.0.37-3
- Python 2 binary package renamed to python2-langtable
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Feb 08 2017 Mike FABIAN <mfabian@redhat.com> - 0.0.37-1
- Add some new translations from CLDR
- Add sgs
- Add chr
- Add Hung script

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.0.36-3
- Rebuild for Python 3.6

* Thu Jul 21 2016 Mike FABIAN <mfabian@redhat.com> - 0.0.36-2
- add BuildRequires: perl

* Wed Jul 20 2016 Mike FABIAN <mfabian@redhat.com> - 0.0.36-1
- Add LI (a de_LI locale has recently been added to glibc)
- Add some translations for LI from CLDR

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.35-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun 24 2016 Mike FABIAN <mfabian@redhat.com> - 0.0.35-1
- Add some translations from CLDR
- Translation fix for Cyprus in Turkish (Resolves: rhbz#1349245)
- Fix script entries for ID and BA
- Add khb, osa, new, xzh and Bhks and Marc scripts

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.34-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Feb 3 2016 Orion Poplawski <orion@cora.nwra.com> - 0.0.34-3
- Modernize spec
- Fix python3 package file ownership

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 0.0.34-2
- Rebuilt for Python3.5 rebuild

* Wed Jul 01 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.34-1
- Add a function list_scripts() to list scripts used for a language or in a territory
- Translation fix from CLDR
- Add Sphinx markup to public functions

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 13 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.33-1
- Translation fix for Tagalog <-> Filipino
- Resolves: rhbz#1220775
- Translation fixes from Wikipedia and CLDR
- fix build with Python 3.4.3 (in current rawhide)

* Tue May 12 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.32-1
- Add language endonym for tl
- Resolves: rhbz#1220783

* Tue Apr 28 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.31-2
- Do not package the files in /usr/share/langtable/ twice
- Resolves: rhbz#1216913

* Thu Mar 05 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.31-1
- Fix keyboard for sr_ME ('rs', not 'sr'), by David Shea (Resolves: rhbz#1190078)
- Add tcy and bhb
- Add some new translations from CLDR
- Some translation fixes  from CLDR

* Tue Jan 27 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.30-1
- Make “eurlatgr” the default console font for languages and regions which
  do not need Arabic or Cyrillic or Hebrew script.
- add ce, raj

* Wed Jan 14 2015 Mike FABIAN <mfabian@redhat.com> - 0.0.29-1
- add CW, cmn, hak, lzh, quz, the

* Wed Sep 24 2014 Mike FABIAN <mfabian@redhat.com> - 0.0.28-1
- Do not used translations tagged with 'variant' in CLDR
- Rename Uyghur keyboard cn(uig) → cn(ug)
  (for xkeyboard-config >= 2.12, shipped with Fedora 21 Alpha)

* Wed Aug 27 2014 Mike FABIAN <mfabian@redhat.com> - 0.0.27-1
- Use Hindi again as the default language for India (Resolves: rhbz#1133188)
- Some translation updates from CLDR.

* Mon Aug 25 2014 Mike FABIAN <mfabian@redhat.com> - 0.0.26-1
- Use English as the default language for India (Resolves: rhbz#1133188)

* Wed Jul 09 2014 Mike FABIAN <mfabian@redhat.com> - 0.0.25-1
- Add fi(classic) keyboard layout (Resolves: rhbz#1117860)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu May 22 2014 Mike FABIAN <mfabian@redhat.com> - 0.0.24-2
- Resolves: rhbz#1100230 - Unowned dir /usr/share/langtable

* Mon Feb 24 2014 Mike FABIAN <mfabian@redhat.com> - 0.0.24-1
- mark Bengali (bd) and its Probhat variant layout as not ASCII-capable (by Adam Williamson)
- Also validate timezones.xml and timezoneidparts.xml in .spec file
- List list_inputmethods() as public API
- Fall back to returning untranslated timezone id if translation for the requested language does not exist (Resolves: rhbz#1032848)

* Tue Dec 10 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.23-1
- Change English translation for or from “Oriya” to “Odia” (Resolves: rhbz#1039496)
- Some new translations and translation fixes from CLDR

* Wed Dec 04 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.22-1
- Fix typo in territory and locale for ms (Resolves: rhbz#1038109)
- add ba, chm, kv, sah, syc, udm, xal
- add entries for more keyboard layouts known to be non-ASCII

* Thu Nov 21 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.21-1
- Make America/New_York the highest ranked timezone for US and yi (Resolves: rhbz#1031319)

* Wed Nov 20 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.20-1
- add entries for several layouts known to be non-ASCII by systemd/s-c-k (patch by Adam Williamson)

* Mon Nov 11 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.19-1
- Add SS
- More translations for anp from CLDR
- Add information about default input methods and a query function

* Mon Nov 04 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.18-1
- Add anp
- Do not fail if a timezone id part cannot be found in the database (Vratislav Podzimek reported that error)

* Tue Oct 22 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.17-1
- Add “be(oss)” as a possible keyboard layout for language nl (Resolves: rhbz#885345)

* Tue Oct 08 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.16-1
- Make it work with python3 (and keep it working with python2) (Resolves: rhbz#985317)

* Mon Sep 16 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.15-1
- Update to 0.0.15
- Add keyboards "ara", "ara(azerty)", "iq", and "sy" (Resolves: rhbz#1008389)

* Sun Sep 15 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.14-1
- Update to 0.0.14
- add some more languages: ay, ayc, ayr, niu, szl, nhn
- make languageId() work even if the name of the language or the territory contain spaces (Resolves: rhbz#1006718)
- Add the default script if not specified in queries for Chinese
- Import improved translations from CLDR
- Always return the territory name as well if queried in language_name()
- Add timezones.xml and timezoneidparts.xml to be able to offer translations for timezone ids
- Import translations for timezone cities from CLDR
- Add some more territories and translations
- test cases for timezone id translations

* Thu Sep 05 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.13-1
- Update to 0.0.13
- Serbian keyboards are 'rs' not 'sr' (by Vratislav Podzimek)

* Wed Aug 28 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.12-1
- Update to 0.0.12
- Match case insensitively in languageId() (Resolves: rhbz#1002000 (case insensitive languageId function needed))

* Mon Aug 19 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.11-1
- Update to 0.0.11
- Add translations for DE and NL territories in nds (reported by Vratislav Podzimek)

* Tue Aug 13 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.10-1
- Update to 0.0.10
- Add translations for Belarusian and Belarus in Latin script (reported by Vratislav Podzimek)

* Sat Aug 03 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.9-1
- Update to 0.0.9
- Add endonyms for pa_Arab (and pa_PK) and translation of country name for Pakistan for pa_Arab
- make languageId() return something even if a language name like "language (territory)" is given (Resolves: rhbz#986659 - some language name to its locale code failed)

* Tue Jul 30 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.8-1
- Update to 0.0.8
- Add endonym for Maithili
- Return True by default from supports_ascii (by Vratislav Podzimek)
- Add grc, eo, ak, GH, cop, dsb, fj, FJ, haw, hil, la, VA, ln, kg, CD, CG, AO, mos, BF, ny, MW, smj, tet, TL, tpi, PG (Resolves: rhbz#985332 - some language codes are missing)
- Import more translations from CLDR
- Give pa_IN.UTF-8 higher weight than pa_PK.UTF-8 (Resolves: rhbz#986658, rhbz#986155)

* Thu Jul 04 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.7-1
- Update to 0.0.7
- Add examples for list_consolefonts()
- Add a list_timezones() function
- Add functions languageId() and territoryId()
- Fix some translations of language names to get unique results returned by languageId()

* Wed Jun 12 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.6-1
- Update to 0.0.6
- Add RelaxNG schemas for the XML files (Vratislav Podzimek <vpodzime@redhat.com>)
- Use SAX instead of the ElementTree (Vratislav Podzimek <vpodzime@redhat.com>)
- Use 'trName' instead of 'name' for translated names (Vratislav Podzimek <vpodzime@redhat.com>)

* Fri Jun 07 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.5-1
- Update to 0.0.5
- Accept script names as used by glibc locales as well
- Support reading gzipped xml files
- Set ASCII support to “True” for cz and sk keyboard layouts

* Mon May 27 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.4-1
- Update to 0.0.4
- Remove backwards compatibility init() function
- Add ia (Interlingua), see https://bugzilla.redhat.com/show_bug.cgi?id=872423

* Thu May 16 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.3-1
- Update to 0.0.3
- Move the examples from the README to the source code
- Some tweaks for the translation of Serbian
- Prefix all global functions and global variables which are internal with “_”
- Rename country → territory, countries → territories in keyboards.xml
- Add keyboard “in(eng)” and make it the default for all Indian languages
- Add a comment stating which functions should be considered public API
- Add a supports_ascii() function
- Run Python’s doctest also on langtable.py, not only the extra test_cases.txt

* Fri May 10 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.2-1
- update to 0.0.2
- Prefer values for language, script, and territory found in languageId over those found in the other parameters

* Tue May 07 2013 Mike FABIAN <mfabian@redhat.com> - 0.0.1-1
- initial package
