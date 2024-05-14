Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-ca
Summary: Catalan hunspell dictionaries
Version: 2.3
Release: 16%{?dist}
Source: https://www.softcatala.org/diccionaris/actualitzacions/OOo/catalan.oxt
URL: https://www.softcatala.org/wiki/Projectes/Corrector_ortogràfic
License: GPLv2+
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-ca)

%description
Catalan hunspell dictionaries.

%prep
%setup -q -c

%build
tr -d '\r' < dictionaries/catalan.aff > ca_ES.aff
touch -r dictionaries/catalan.aff ca_ES.aff
tr -d '\r' < dictionaries/catalan.dic > ca_ES.dic
touch -r dictionaries/catalan.dic ca_ES.dic

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p ca_ES.dic ca_ES.aff $RPM_BUILD_ROOT/%{_datadir}/myspell
pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
ca_ES_aliases="ca_AD ca_FR ca_IT"
for lang in $ca_ES_aliases; do
        ln -s ca_ES.aff $lang.aff
        ln -s ca_ES.dic $lang.dic
done
popd


%files
%doc LICENSES-en.txt LLICENCIES-ca.txt       
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
