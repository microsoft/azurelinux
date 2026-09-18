# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%global dict_dirname hunspell 
%else
%global dict_dirname myspell
%endif

Name: hunspell-si
Summary: Sinhala hunspell dictionaries
Version: 0.2.1
Release: 35%{?dist}
Source: http://www.sandaru1.com/si-LK.tar.gz
#Following URL is down since few months informed to upstream
URL: http://www.sandaru1.com/2009/08/29/sinhala-spell-checker-for-firefox/
License: GPL-2.0-or-later
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
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p dictionaries/si-LK.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}/si_LK.aff
cp -p dictionaries/si-LK.dic $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}/si_LK.dic

%files
%doc LICENSE README
%{_datadir}/%{dict_dirname}/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 03 2024 Parag Nemade <pnemade AT redhat DOT com> - 0.2.1-33
- Add conditional for RHEL for using hunspell directory
- Add tmt CI tests

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.2.1-27
- Update license tag to SPDX format

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Feb 11 2022 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 0.2.1-25
- rename install directory name from myspell to hunspell
- https://fedoraproject.org/wiki/Changes/Hunspell_dictionary_dir_change

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
