Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-si
Summary: Sinhala hunspell dictionaries
Version: 0.2.1
Release: 21%{?dist}
Source: https://www.sandaru1.com/si-LK.tar.gz
#Following URL is down since few months informed to upstream
URL: https://www.sandaru1.com/2009/08/29/sinhala-spell-checker-for-firefox/
License: GPLv2+
BuildArch: noarch
Requires: hunspell
Supplements: (hunspell and langpacks-si)

%description
Sinhala hunspell dictionaries.

%prep
%setup -q -c -n hunspell-si

%build
#nothing to build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dictionaries/si-LK.aff $RPM_BUILD_ROOT/%{_datadir}/myspell/si_LK.aff
cp -p dictionaries/si-LK.dic $RPM_BUILD_ROOT/%{_datadir}/myspell/si_LK.dic

%files
%doc LICENSE README
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.1-21
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.2.1-13
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Parag Nemade <pnemade AT redhat.com> - 0.2.1-7
- Resolves:rh#879152 - spec cleanup for recent packaging guidelines 

* Thu Aug 23 2012 Parag Nemade <pnemade AT redhat.com> - 0.2.1-6
- Resolves:rh#848847:-Source URL not working

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Mar 09 2010 Parag Nemade <pnemade AT redhat.com> - 0.2.1-2
- Resolves: rh#571710: Fix license tag in spec file with new upstream release
- Removed CREDITS file as upstream provides now README and LICENSE files.

* Wed Feb 24 2010 Parag Nemade <pnemade AT redhat.com> - 0.2.1-1
- Resolves: rh#567895: Fix license tag in spec file with new upstream release

* Wed Nov 25 2009 Caolan McNamara <caolanm@redhat.com> - 0.2-1
- initial version
