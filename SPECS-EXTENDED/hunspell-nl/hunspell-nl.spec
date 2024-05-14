Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-nl
Summary: Dutch hunspell dictionaries
Version: 2.10
Release: 17%{?dist}
#https://www.opentaal.org/bestanden/doc_download/20-woordenlijst-v-210g-voor-openofficeorg-3
#annoying click through makes direct link apparently impossible
Source: OpenTaal-210G-LO.oxt
URL: https://www.opentaal.org/english.php
License: BSD or CC-BY
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-nl)

%description
Dutch hunspell dictionaries.

%prep
%setup -q -c

%build
chmod -x nl_NL.*

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p nl_NL.aff nl_NL.dic $RPM_BUILD_ROOT/%{_datadir}/myspell

pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
nl_NL_aliases="nl_AW nl_BE"
for lang in $nl_NL_aliases; do
        ln -s nl_NL.aff $lang.aff
        ln -s nl_NL.dic $lang.dic
done


%files
%doc description/desc_en_US.txt description/desc_nl_NL.txt README_nl_NL.txt license_en_EN.txt licentie_nl_NL.txt
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.10-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 2.10-9
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 2.10-1
- latest version

* Tue Aug 30 2011 Caolán McNamara <caolanm@redhat.com> - 2.00-4
- Resolves: rhbz#734218 remove executable flags

* Thu May 12 2011 Caolán McNamara <caolanm@redhat.com> - 2.00-3
- hyph dict incorrectly installed in spell dir

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.00-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 26 2010 Caolán McNamara <caolanm@redhat.com> - 2.00-1
- latest version

* Thu Jan 07 2010 Caolán McNamara <caolanm@redhat.com> - 1.10-2
- fix License tag

* Tue Aug 25 2009 Caolán McNamara <caolanm@redhat.com> - 1.10-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00g-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 1.00g-5
- retain timestamp

* Mon Jun 22 2009 Caolán McNamara <caolanm@redhat.com> - 1.00g-4
- extend coverage

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.00g-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 09 2007 Caolán McNamara <caolanm@redhat.com> - 1.00g-2
- clarify license version

* Fri Jun 08 2007 Caolán McNamara <caolanm@redhat.com> - 1.00g-1
- OpenTaal project publishes Dutch Language Union approved dictionary

* Wed Feb 14 2007 Caolán McNamara <caolanm@redhat.com> - 0.20050720-1
- update to match upstream id

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20050617-1
- initial version
