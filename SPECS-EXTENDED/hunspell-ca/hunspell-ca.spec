Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%global dict_dirname hunspell
%else
%global dict_dirname myspell
%endif

Name: hunspell-ca
Summary: Catalan hunspell dictionaries
Version: 3.0.8
Release: 1%{?dist}
Source: https://github.com/Softcatala/catalan-dict-tools/releases/download/v%{version}/ca.%{version}-hunspell.zip
URL: https://www.softcatala.org/projectes/corrector-ortografic/
License: GPL-2.0-or-later OR LGPL-2.1-or-later
BuildArch: noarch

Requires: hunspell-filesystem
Supplements: (hunspell and langpacks-ca)

%description
Catalan hunspell dictionaries.

%prep
%setup -q -c

%build
tr -d '\r' < catalan.aff > ca_ES.aff
touch -r catalan.aff ca_ES.aff
tr -d '\r' < catalan.dic > ca_ES.dic
touch -r catalan.dic ca_ES.dic

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p ca_ES.dic ca_ES.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
pushd $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}/
ca_ES_aliases="ca_AD ca_FR ca_IT"
for lang in $ca_ES_aliases; do
        ln -s ca_ES.aff $lang.aff
        ln -s ca_ES.dic $lang.dic
done
popd


%files
%doc README.txt release-notes_en.txt
%license LICENSE gpl-2.0.txt lgpl-2.1.txt
%{_datadir}/%{dict_dirname}/*

%changelog
* Tue Mar 18 2025 Akarsh Chaudhary <v-akarshc@microsoft.com> - 3.0.8-1
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 10 2023 Parag Nemade <pnemade AT redhat DOT com> - 3.0.8-1
- Resolves:rh#2230531 - Update to new Upstream Source

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 22 2023 Caolán McNamara <caolanm@redhat.com> - 2.3-23
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 22 2022 Parag Nemade <pnemade AT redhat DOT com> - 2.3-20
- Add conditional for new hunspell dir path and update to Requires:
  hunspell-filesystem

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 2.3-8
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 09 2012 Caolán McNamara <caolanm@redhat.com> - 2.3-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 15 2010 Caolán McNamara <caolanm@redhat.com> - 2.2.0-1
- latest version

* Thu Oct 08 2009 Caolan McNamara <caolanm@redhat.com> - 2.1.5-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090630-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090630-1
- latest version

* Wed Mar 11 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090311-1
- latest version

* Tue Mar 10 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090309-1
- latest version

* Tue Mar 03 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090302-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20081027-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 28 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081027-1
- latest version

* Mon Oct 20 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081019-1
- latest version

* Sun Oct 05 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081005-1
- latest version

* Tue Sep 30 2008 Caolan McNamara <caolanm@redhat.com> - 0.20080918-1
- latest version

* Mon Sep 15 2008 Caolan McNamara <caolanm@redhat.com> - 0.20080915-1
- latest version

* Tue Jul 08 2008 Caolan McNamara <caolanm@redhat.com> - 0.20080706-2
- Catalan is spoken in Andora, France and Italy as well

* Mon Jul 07 2008 Caolan McNamara <caolanm@redhat.com> - 0.20080706-1
- latest version

* Wed Jul 02 2008 Caolan McNamara <caolanm@redhat.com> - 0.20080620-1
- latest version

* Fri Aug 03 2007 Caolan McNamara <caolanm@redhat.com> - 0.20060508-2
- clarify license version

* Mon Jul 09 2007 Caolan McNamara <caolanm@redhat.com> - 0.20060508-1
- latest version

* Thu Dec 07 2006 Caolan McNamara <caolanm@redhat.com> - 0.20021015-1
- initial version