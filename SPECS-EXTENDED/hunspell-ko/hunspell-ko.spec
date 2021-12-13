Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: hunspell-ko
Summary: Korean hunspell dictionaries
Version: 0.7.0
Release: 9%{?dist}
Source: https://github.com/spellcheck-ko/hunspell-dict-ko/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
URL: https://github.com/spellcheck-ko/hunspell-dict-ko
License: MPLv1.1 or GPLv2 or LGPLv2
BuildArch: noarch
BuildRequires: python3
BuildRequires: hunspell
Requires: hunspell
Supplements: (hunspell and langpacks-ko)

%description
Korean hunspell dictionaries.

%prep
%setup -q -n hunspell-dict-ko-%{version}

%build
make

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p ko.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/ko_KR.aff
cp -p ko.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/ko_KR.dic

%check
make test

%files
%doc README.md
%license LICENSE LICENSE.GPL LICENSE.LGPL LICENSE.MPL
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.7.0-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.7.0-5
- Remove unneeded BuildRequires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 16 2018 Parag Nemade <pnemade AT redhat DOT com> - 0.7.0-3
- Spec cleanup and correct the BR: python to BR:python3

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 11 2017 Caolán McNamara <caolanm@redhat.com> - 0.7.0-1
- Resolves: rhbz#1523628 latest version

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 Caolán McNamara <caolanm@redhat.com> - 0.5.6-1
- latest version

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.5.5-9
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 0.5.5-1
- latest version

* Mon Aug 08 2011 Caolán McNamara <caolanm@redhat.com> - 0.5.4-1
- latest version

* Sun May 22 2011 Caolán McNamara <caolanm@redhat.com> - 0.5.3-1
- latest version

* Mon Apr 04 2011 Caolán McNamara <caolanm@redhat.com> - 0.5.2-1
- latest version

* Mon Mar 21 2011 Caolán McNamara <caolanm@redhat.com> - 0.5.1-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Caolán McNamara <caolanm@redhat.com> - 0.5.0-1
- latest version

* Sat Aug 07 2010 Caolán McNamara <caolanm@redhat.com> - 0.4.3-1
- latest version
- drop integrated hunspell-dict-ko-0.4.2-1278333282.fixtests.patch

* Mon Jul 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.4.2-2
- enable make check now that hunspell is fixed to know about
  hangul syllables

* Mon Jul 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.4.2-1
- latest version

* Tue Jun 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.4.1-1
- latest version

* Mon Mar 01 2010 Caolán McNamara <caolanm@redhat.com> - 0.4.0-1
- latest version

* Tue Nov 03 2009 Caolán McNamara <caolanm@redhat.com> - 0.3.5-1
- latest version

* Sun Aug 30 2009 Caolán McNamara <caolanm@redhat.com> - 0.3.3-1
- latest version

* Sun Jul 26 2009 Caolán McNamara <caolanm@redhat.com> - 0.3.2-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jul 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.3.1-1
- latest version

* Mon Jun 22 2009 Caolán McNamara <caolanm@redhat.com> - 0.3.0-1
- latest version

* Wed Jun 17 2009 Caolán McNamara <caolanm@redhat.com> - 0.2.4-2
- build from source

* Mon Jun 15 2009 Caolán McNamara <caolanm@redhat.com> - 0.2.4-1
- initial version
