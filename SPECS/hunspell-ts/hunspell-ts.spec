# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%global dict_dirname hunspell
%else
%global dict_dirname myspell
%endif

Name: hunspell-ts
Summary: Tsonga hunspell dictionaries
%global upstreamid 20110323.1
Version: 0.%{upstreamid}
Release: 19%{?dist}
Source:https://addons.mozilla.org/firefox/downloads/file/376225/tsonga_spell_checker-20110323.1-typefix-fn+sm+tb+fx.xpi 
URL: https://addons.mozilla.org/en-US/firefox/addon/tsonga-spell-checker/
License: LGPL-2.1-or-later
BuildArch: noarch

Requires: hunspell-filesystem
Supplements: (hunspell and langpacks-ts)

%description
Tsonga hunspell dictionaries.

%prep
%autosetup -c -n hunspell-ts

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p dictionaries/ts-ZA.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}/ts_ZA.aff
cp -p dictionaries/ts-ZA.dic $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}/ts_ZA.dic


%files
%doc README-ts-ZA.txt
%{_datadir}/%{dict_dirname}/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 23 2023 Caolán McNamara <caolanm@redhat.com> - 0.20091101-13
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 22 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.20110323.1-10
- Add conditional for new hunspell dir path and update to Requires:
  hunspell-filesystem

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110323.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20110323.1-1
- Update to new upstream 20110323.1-typefix

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20091101-10
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20091101-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20091101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 20 2010 Caolán McNamara <caolanm@redhat.com> - 0.20091101-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20060123-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20060123-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Caolán McNamara <caolanm@redhat.com> - 0.20060123-1
- initial version
