Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           hyphen-it
Summary:        Italian hyphenation rules
Version:        5.1.1
Release:        7%{?dist}
# The license text is embedded within the README files
# Here we specify the thesaurus license only as other files are not packaged 
License:        LGPL-2.1-only
URL:            https://pagure.io/dizionario_italiano
Source:         %{url}/archive/%{version}/dizionario_italiano-%{version}.tar.gz

BuildArch:      noarch
Requires:       hyphen
Supplements:    (hyphen and langpacks-it)
Provides:       hyphen-la = %{version}

%description
Italian hyphenation rules.

%prep
%autosetup -n dizionario_italiano-%{version}

%build
# Nothing to do

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_it_IT.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen
pushd $RPM_BUILD_ROOT/%{_datadir}/hyphen/
#http://extensions.services.openoffice.org/project/dict-la uses the it_IT for Latin
#so we'll do the same
it_IT_aliases="it_CH la_VA"
for lang in $it_IT_aliases; do
        ln -s hyph_it_IT.dic "hyph_"$lang".dic"
done

%files
%license LICENSES/lgpl-2.1.txt
%doc CHANGELOG.txt README.md README_hyph_it_IT.txt
%{_datadir}/hyphen/hyph_it_IT.dic
%{_datadir}/hyphen/hyph_it_CH.dic
%{_datadir}/hyphen/hyph_la_VA.dic

%changelog
* Wed Nov 06 2024 Sreenivasulu Malavathula <v-smalavathu@microsoft.com> - 5.1.1-7
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 04 2023 Mattia Verga <mattia.verga@proton.me> - 5.1.1-2
- Use sources from pagure.io project

* Sun Jun 04 2023 Mattia Verga <mattia.verga@proton.me> - 5.1.1-1
- Switch to libreoffice dictionaries from libreitalia.org

* Thu Feb 23 2023 Caolán McNamara <caolanm@redhat.com> - 0.20071127-29
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20071127-18
- Update Source tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20071127-14
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20071127-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071127-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 02 2008 Caolán McNamara <caolanm@redhat.com> - 0.20071127-3
- add Latin alias

* Thu Nov 29 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071127-2
- add switz italian alias

* Tue Nov 27 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071127-1
- latest version

* Fri Nov 23 2007 Caolán McNamara <caolanm@redhat.com> - 0.20030809-1
- initial version
