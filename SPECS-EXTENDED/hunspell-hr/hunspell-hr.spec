Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-hr
Summary: Croatian hunspell dictionaries
%global upstreamid 20040608
Version: 0.%{upstreamid}
Release: 23%{?dist}
Source0: https://cvs.linux.hr/spell/myspell/hr_HR.zip
Source1: %{name}-LICENSE.txt
URL: https://cvs.linux.hr/spell/
License: LGPLv2+ or SISSL
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-hr)

%description
Croatian hunspell dictionaries.

%package -n hyphen-hr
Requires: hyphen
Summary: Croatian hyphenation rules
Supplements: (hyphen and langpacks-hr)

%description -n hyphen-hr
Croatian hyphenation rules.

%prep
%setup -q -c -n hunspell-hr
cp %{SOURCE1} ./LICENSE.txt

%build
chmod -x *

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p hr_HR.dic hr_HR.aff $RPM_BUILD_ROOT/%{_datadir}/myspell
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_hr.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen/hyph_hr_HR.dic


%files
%license LICENSE.txt
%doc README_hr_HR.txt
%{_datadir}/myspell/*

%files -n hyphen-hr
%license LICENSE.txt
%doc README_hr_HR.txt
%{_datadir}/hyphen/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.20040608-23
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.20040608-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1:0.20040608-14
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20040608-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 08 2010 Caolán McNamara <caolanm@redhat.com> - 1:0.20040608-5
- add licence notice to all subpackages

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20040608-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Nov 22 2007 Caolán McNamara <caolanm@redhat.com> - 1:0.20040608-2
- package hyphenation rules

* Tue Aug 21 2007 Caolán McNamara <caolanm@redhat.com> - 1:0.20040608-1
- clarify license
- canonical upstream version

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20060607-1
- initial version
