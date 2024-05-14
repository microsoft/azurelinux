Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hyphen-hu
Summary: Hungarian hyphenation rules
%global upstreamid 20090612
Version: 0.%{upstreamid}
Release: 26%{?dist}
# Source URL is dead now
# Source: https://download.github.com/nagybence-huhyphn-aa3fc85.tar.gz
Source: %{_distro_sources_url}/nagybence-huhyphn-aa3fc85.tar.gz
URL: https://www.tipogral.hu/
License: GPLv2
BuildArch: noarch
Requires: hyphen
Supplements: (hyphen and langpacks-hu)

%description
Hungarian hyphenation rules.

%prep
%setup -q -n nagybence-huhyphn-aa3fc85
#disable for now as built-in patgen has too small a limit to rebuild
#ln -sf /usr/bin/patgen patgen
#touch words/*.txt

%build
make

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_hu.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen/hyph_hu_HU.dic


%files
%doc README doc/huhyphn.pdf
%license gpl.txt
%{_datadir}/hyphen/*

%changelog
* Thu Feb 22 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20090612-26
- Updating naming for 3.0 version of Azure Linux.

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20090612-25
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20090612-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jul 07 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20090612-19
- Mark Source as dead now

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20090612-15
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20090612-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Caolan McNamara <caolanm@redhat.com> - 0.20090612-13
- Resolves: rhbz#1275688 wrong country code for Hungary

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 06 2012 Caolan McNamara <caolanm@redhat.com> - 0.20090612-8
- clarify license

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 05 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090612-4
- new source location

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090612-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 24 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090612-2
- vanilla patgen's limit is too small

* Mon Jun 15 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090612-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20081106-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 09 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081106-1
- latest version

* Fri Nov 23 2007 Caolan McNamara <caolanm@redhat.com> - 0.20070907-1
- initial version
