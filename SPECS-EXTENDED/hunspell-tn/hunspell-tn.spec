Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: hunspell-tn
Summary: Tswana hunspell dictionaries
%global upstreamid 20150904
Version: 0.%{upstreamid}
Release: 6%{?dist}
Source: https://addons.mozilla.org/firefox/downloads/file/347396/tswana_spell_checker-%{upstreamid}-sm+tb+fx+an+fn.xpi
URL: https://addons.mozilla.org/en-US/firefox/addon/tswana-spell-checker/
License: GPLv3+
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-tn)

%description
Tswana hunspell dictionaries.

%prep
%autosetup -c -n hunspell-tn

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dictionaries/tn-ZA.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/tn_ZA.aff
cp -p dictionaries/tn-ZA.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/tn_ZA.dic
pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
tn_ZA_aliases="tn_BW"
for lang in $tn_ZA_aliases; do
        ln -s tn_ZA.aff $lang.aff
        ln -s tn_ZA.dic $lang.dic
done
popd


%files
%license dictionaries/README_tn_ZA.txt
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20150904-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150904-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150904-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150904-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150904-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20150904-1
- Update to new upstream release 20150904

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20091101-10
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.20091101-1
- latest version

* Wed Jan 06 2010 Caolán McNamara <caolanm@redhat.com> - 0.20060123-5
- README says was derived from GPL work -> GPL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20060123-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20060123-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Sep 30 2008 Caolán McNamara <caolanm@redhat.com> - 0.20060123-2
- add Botswana alias

* Tue Sep 09 2008 Caolán McNamara <caolanm@redhat.com> - 0.20060123-1
- initial version
