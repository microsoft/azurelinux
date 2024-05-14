Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-sk
Summary: Slovak hunspell dictionaries
%global upstreamid 20110228
Version: 0.%{upstreamid}
Release: 18%{?dist}
Source: https://www.sk-spell.sk.cx/files/hunspell-sk-%{upstreamid}.zip
URL: https://www.sk-spell.sk.cx/
License: LGPLv2 or GPLv2 or MPLv1.1
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-sk)

%description
Slovak hunspell dictionaries.

%prep
%setup -q -n %{name}-%{upstreamid}

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/myspell


%files
%license doc/Copyright doc/GPL doc/LGPL doc/MPL
%doc doc/AUTHORS doc/Flagy.AUTHORS doc/Flagy.Changelog doc/Flagy.README doc/Flagy.TODO
%{_datadir}/myspell/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 0.20110228-18
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.20110228-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1:0.20110228-9
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.20110228-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110228-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110228-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110228-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110228-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110228-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20110228-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 18 2011 Caolán McNamara <caolanm@redhat.com> - 1:0.20110228-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20091213-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 14 2009 Caolán McNamara <caolanm@redhat.com> - 1:0.20091213-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20090330-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Apr 01 2009 Caolán McNamara <caolanm@redhat.com> - 1:0.20090330-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.20090106-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 11 2009 Caolán McNamara <caolanm@redhat.com> - 1:0.20090106-1
- latest version

* Wed Dec 03 2008 Caolán McNamara <caolanm@redhat.com> - 1:0.20080525-1
- latest version

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 1:0.5.6-2
- clarify that tri-licensed

* Wed Jul 11 2007 Caolán McNamara <caolanm@redhat.com> - 1:0.5.6-1
- canonical upstream version

* Wed Feb 14 2007 Caolán McNamara <caolanm@redhat.com> - 0.20050911-1
- upstream id

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20050228-1
- initial version
