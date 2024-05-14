Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-dsb
Summary: Lower Sorbian hunspell dictionaries
Version: 1.4.8
Release: 6%{?dist}
Source: https://downloads.sourceforge.net/project/aoo-extensions/3045/14/lower_sorbian_spelling_dictionary-%{version}.oxt
URL: https://dsb-spell.sourceforge.net
License: GPLv2+
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-dsb)

%description
Lower Sorbian hunspell dictionaries.

%prep
%autosetup -c

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dsb_DE.* $RPM_BUILD_ROOT/%{_datadir}/myspell


%files
%doc description/desc_de.txt description/desc_en.txt description/desc_pl.txt
%license registration/license_en.txt  

%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.8-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 1.4.8-1
- Update to new upstream 1.4.8

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.4.6-8
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Caolán McNamara <caolanm@redhat.com> - 1.4.6-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Aug 08 2011 Caolán McNamara <caolanm@redhat.com> - 1.4.5-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 04 2011 Caolán McNamara <caolanm@redhat.com> - 1.4.4-1
- latest version

* Thu Dec 02 2010 Caolán McNamara <caolanm@redhat.com> - 1.4.3-1
- latest version

* Mon May 24 2010 Caolán McNamara <caolanm@redhat.com> - 1.4.2-1
- latest version

* Sun Apr 11 2010 Caolán McNamara <caolanm@redhat.com> - 1.4.1-1
- latest version

* Wed Mar 31 2010 Caolán McNamara <caolanm@redhat.com> - 1.4.0-1
- latest version

* Thu Mar 04 2010 Caolán McNamara <caolanm@redhat.com> - 1.3.0-1
- latest version

* Wed Jan 06 2010 Caolán McNamara <caolanm@redhat.com> - 1.2.0-1
- latest version

* Fri Dec 11 2009 Caolán McNamara <caolanm@redhat.com> - 1.1.3-1
- latest version

* Tue Nov 03 2009 Caolán McNamara <caolanm@redhat.com> - 1.1.2-1
- latest version

* Wed Oct 14 2009 Caolán McNamara <caolanm@redhat.com> - 1.1.1-1
- initial version
