Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-it
Summary: Italian hunspell dictionaries
Version: 2.4
Release: 1%{?dist}
Source: https://downloads.sourceforge.net/sourceforge/linguistico/italiano_2_4_2007_09_01.zip
URL: https://linguistico.sourceforge.net
License: GPLv3+
BuildArch: noarch
Requires: hunspell
Supplements: (hunspell and langpacks-it)
#dic contains free-form text inside the .dic, i.e. "error: line 3: bad flagvector"
#  https://sourceforge.net/tracker/?func=detail&aid=2994177&group_id=128318&atid=711333
Patch0: hunspell-it-sf2994177.cleandic.patch

%description
Italian hunspell dictionaries.

%prep
%setup -q -c -n hunspell-it
%patch 0 -p0 -b .cleandic

%build
chmod -x *

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/myspell
pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
it_IT_aliases="it_CH"
for lang in $it_IT_aliases; do
        ln -s it_IT.aff $lang.aff
        ln -s it_IT.dic $lang.dic
done



%files
%doc it_IT_README.txt it_IT_COPYING it_IT_AUTHORS it_IT_license.txt it_IT_notes.txt
%{_datadir}/myspell/*

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4-1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Converting the 'Release' tag to the '[number].[distribution]' format.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.21.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.20.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.19.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.18.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.17.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.16.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.15.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 2.4-0.14.20070901
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-0.13.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.12.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.11.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.10.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.9.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.8.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.7.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.6.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Apr 29 2010 Caolan McNamara <caolanm@redhat.com> - 2.4-0.5.20070901
- remove spurious text from .dic

* Tue Jan 05 2010 Caolan McNamara <caolanm@redhat.com> - 2.4-0.4.20070901
- it_IT_README.1st says GPLv2+, but it_IT_README.txt says GPLv3+ -> 
  change license field to GPLv3+

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.3.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-0.2.20070901
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 03 2007 Caolan McNamara <caolanm@redhat.com> - 2.4-0.1.20070901
- latest version

* Fri Aug 03 2007 Caolan McNamara <caolanm@redhat.com> - 2.3-0.2.20060723
- clarify license version

* Thu Dec 07 2006 Caolan McNamara <caolanm@redhat.com> - 2.3-0.1.20060723
- initial version
