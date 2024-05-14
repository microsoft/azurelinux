Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-ru
Summary: Russian hunspell dictionaries
Version: 0.99g5
Release: 19%{?dist}
# Upstream source is gone now and recent alternative don't have license
# Source: https://releases.mozilla.org/pub/mozilla.org/addons/3703/russian_spellchecking_dictionary-0.4.4-fx+tb+sm.xpi
Source: russian_spellchecking_dictionary-0.4.4-fx+tb+sm.xpi
URL: https://scon155.phys.msu.su/eng/lebedev.html
License: BSD
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-ru)

%description
Russian hunspell dictionaries.

%prep
%autosetup -c -n hunspell-ru

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dictionaries/ru.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/ru_RU.dic
cp -p dictionaries/ru.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/ru_RU.aff
pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
ru_RU_aliases="ru_UA"
for lang in $ru_RU_aliases; do
        ln -s ru_RU.aff $lang.aff
        ln -s ru_RU.dic $lang.dic
done

%files
%doc dictionaries/Changelog dictionaries/LICENSE dictionaries/README
%{_datadir}/myspell/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> -0.99g5-19
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.99g5-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 1:0.99g5-13
- Update Source tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1:0.99g5-9
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.99g5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99g5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99g5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99g5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99g5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99g5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99g5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 12 2011 Caolán McNamar <caolanm@redhat.com> 1:0.99g5-1
- Resolves: rhbz#716594 use 0.99g5 ff conversion, take 2

* Fri Jul 01 2011 Caolán McNamar <caolanm@redhat.com> 1:0.99f7-6
- Resolves: rhbz#716594 use yo variant

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99f7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99f7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.99f7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 21 2009 Caolán McNamara <caolanm@redhat.com> - 1:0.99f7-2
- add alias

* Tue Aug 21 2007 Caolán McNamara <caolanm@redhat.com> - 1:0.99f7-1
- clarify licence
- canonical upstream source

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20040406-1
- initial version
