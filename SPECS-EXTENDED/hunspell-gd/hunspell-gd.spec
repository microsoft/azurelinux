Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-gd
Summary: Scots Gaelic hunspell dictionaries
Version: 2.6
Release: 15%{?dist}
Source: https://downloads.sourceforge.net/project/aoo-extensions/4587/8/hunspell-gd-2.6.oxt
URL: https://extensions.services.openoffice.org/en/project/faclair-afb
License: GPLv2+ and GPLv3+
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-gd)

%description
Scots Gaelic hunspell dictionaries.

%prep
%setup -q -c hunspell-gd-%{version}

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p dictionaries/gd_GB.dic dictionaries/gd_GB.aff $RPM_BUILD_ROOT/%{_datadir}/myspell


%files
%doc dictionaries/README_gd_GB.txt LICENSES-en.txt
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6-15
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 2.6-7
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Caolán McNamara <caolanm@redhat.com> - 2.6-2
- clarify license. The .aff still says GPLv2+ while the LICENSES-en.txt etc say
  GPLv3+

* Mon May 20 2013 Caolán McNamara <caolanm@redhat.com> - 2.6-1
- latest version

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 2.5-1
- latest version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 2.3-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 08 2011 Caolán McNamara <caolanm@redhat.com> - 2.1-1
- latest version

* Wed Nov 16 2011 Caolán McNamara <caolanm@redhat.com> - 2.0-1
- latest version

* Wed Jun 29 2011 Caolán McNamara <caolanm@redhat.com> - 1.3-1
- latest version

* Sat Apr 02 2011 Caolán McNamara <caolanm@redhat.com> - 1.2-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.4.rc.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.3.rc.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 1.0.0-0.2.rc.1
- tidy spec

* Mon Jun 15 2009 Caolán McNamara <caolanm@redhat.com> - 1.0.0-0.1.rc.1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Mar 27 2008 Caolán McNamara <caolanm@redhat.com> - 0.1.1-1
- initial version
