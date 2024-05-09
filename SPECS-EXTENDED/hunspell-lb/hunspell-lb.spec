Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-lb
Summary: Luxembourgish hunspell dictionaries
%global upstreamid 20121128
Version: 0.%{upstreamid}
Release: 14%{?dist}
Source: https://downloads.spellchecker.lu/packages/OOo3/SpellcheckerLu.oxt
URL: https://spellchecker.lu
License: EUPL 1.1
BuildArch: noarch
Requires: hunspell
Supplements: (hunspell and langpacks-lb)

%description
Luxembourgish hunspell dictionaries.

%package -n mythes-lb
Summary: Luxembourgish thesaurus
Requires: mythes
Supplements: (mythes and langpacks-lb)

%description -n mythes-lb
Luxembourgish thesaurus.

%prep
%setup -q -c

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/myspell
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_lb_LU_v2.* $RPM_BUILD_ROOT/%{_datadir}/mythes


%files
%license registration/README_lb_LU.txt
%{_datadir}/myspell/*

%files -n mythes-lb
%license registration/README_lb_LU.txt
%{_datadir}/mythes/th_lb_LU_v2.*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20121128-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20121128-6
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20121128-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121128-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121128-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121128-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 0.20110821-1
- Resolves: rhbz#905966 latest version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110821-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110821-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Aug 26 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110821-1
- latest version

* Mon Aug 08 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110709-1
- latest version

* Sat Apr 16 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110412-1
- latest version

* Mon Apr 11 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110411-1
- latest version

* Tue Mar 1 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110313-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110107-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 09 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110107-1
- latest version

* Wed Sep 15 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100914-1
- latest version

* Mon Jul 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100704-1
- latest version

* Tue Jun 29 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100628-1
- latest version

* Tue May 11 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100509-1
- latest version

* Thu Apr 22 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100420-1
- latest version

* Mon Apr 12 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100408-1
- latest version

* Thu Apr 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100407-2
- latest version

* Sun Apr 04 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100301-2
- mythes now owns /usr/share/mythes

* Tue Mar 02 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100301-1
- latest version

* Wed Feb 17 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100216-1
- latest version

* Wed Jan 27 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100120-1
- initial version
