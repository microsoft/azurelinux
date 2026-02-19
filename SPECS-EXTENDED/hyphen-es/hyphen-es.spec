Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hyphen-es
Summary: Spanish hyphenation rules
Version: 2.8
Release: 1%{?dist}
Source: https://github.com/sbosio/rla-es/releases/download/v%{version}/es.oxt
URL: https://github.com/sbosio/rla-es/tree/master/separacion
License: LGPLv3+ or GPLv3+ or MPLv1.1
BuildArch: noarch
Requires: hyphen
Supplements: (hyphen and langpacks-es)

%description
Spanish hyphenation rules.

%prep
%setup -q -c -n %{name}

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_es.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen/hyph_es.dic

pushd $RPM_BUILD_ROOT/%{_datadir}/hyphen/
es_aliases="es_AR es_BO es_CL es_CO es_CR es_CU es_DO es_EC es_ES es_GT es_HN es_MX es_NI es_PA es_PE es_PR es_PY es_SV es_US es_UY es_VE"

for lang in $es_aliases; do
        ln -s hyph_es.dic hyph_$lang.dic
done
popd

%files
%doc README_hyph_es.txt
%license GPLv3.txt LGPLv3.txt MPL-1.1.txt
%{_datadir}/hyphen/*

%changelog
* Wed Oct 30 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 2.8-1
- Update CBL-Mariner to verion 2.8 (License: LGPLv3+ or GPLv3+ or MPLv1.1).
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jan 27 2019 Caolán McNamara <caolanm@redhat.com> - 2.3-4
- Resolves: rhbz#1669895 wrong file name

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 8 2018 Ismael Olea <ismael@olea.org> - 2.3-1
- update to v2.3

* Fri Jan 5 2018 Ismael Olea <ismael@olea.org> - 2.2-1
- updating to v2.2
- upstream changed to github
- detailing licensing

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110222svn-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110222svn-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20110222svn-8
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110222svn-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110222svn-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110222svn-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110222svn-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110222svn-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110222svn-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jul 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110222svn-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20040810-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20040810-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20040810-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20040810-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 06 2008 Caolán McNamara <caolanm@redhat.com> - 0.20040810-1
- initial version
