Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: mythes-hu
Summary: Hungarian thesaurus
%global upstreamid 20101019
Version: 0.%{upstreamid}
Release: 20%{?dist}
Source: https://downloads.sourceforge.net/project/aoo-extensions/1283/9/dict-hu.oxt
URL: https://extensions.services.openoffice.org/project/hu_dicts
#bundled but unused spell-checking stuff is under GPLv2+ or LGPLv2+ or MPLv1.1
#base for bundled but unused hyphenation stuff is under GPLv2
#additional patch to unused hyphenation stuff is MPL/GPL/LGPL
License: GPLv2+ and (GPLv2+ or LGPLv2+ or MPLv1.1) and GPLv2 and (GPL+ or LGPLv2+ or MPLv1.1)
BuildArch: noarch
Requires: mythes
Supplements: (mythes and langpacks-hu)

%description
Hungarian thesaurus.

%prep
%setup -q -c

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_hu_HU_v2.* $RPM_BUILD_ROOT/%{_datadir}/mythes


%files
%license README_th_hu_HU_v2.txt
%{_datadir}/mythes/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20101019-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20101019-15
- Update for Source tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20101019-11
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20101019-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101019-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101019-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101019-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 0.20101019-6
- Resolves: rhbz#905964 nemeth hates version control, or versions :-)

* Tue Nov 06 2012 Caolán McNamara <caolanm@redhat.com> - 0.20101019-5
- clarify license

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101019-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101019-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101019-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Oct 20 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101019-1
- latest version

* Sat May 15 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100512-1
- latest version

* Sun Apr 04 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100329-2
- mythes now owns /usr/share/mythes

* Wed Mar 31 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100329-1
- latest version

* Sun Feb 14 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100213-1
- latest version

* Fri Sep 18 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090918-1
- latest version

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090203-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 14 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090203-1
- initial version
