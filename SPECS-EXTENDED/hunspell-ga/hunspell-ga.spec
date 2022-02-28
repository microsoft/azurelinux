Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: hunspell-ga
Summary: Irish hunspell dictionaries
Version: 5.0
Release: 7%{?dist}
Source0: https://github.com/kscanne/gaelspell/releases/download/v%{version}/ispell-gaeilge-%{version}.tar.gz
Source1: myspell-header
Source2: hunspell-header
URL: https://github.com/kscanne/gaelspell
License: GPLv2+
BuildArch: noarch
BuildRequires: hunspell-devel
Patch1: ispell-gaeilge-5.0-buildhunspell.patch

Requires: hunspell
Supplements: (hunspell and langpacks-ga)

%description
Irish hunspell dictionaries.

%prep
%autosetup -n ispell-gaeilge-%{version}

%build
make
cat %{SOURCE1} %{SOURCE2} > header
export LANG=C.UTF-8
iconv -f utf-8 -t iso-8859-1 < gaeilge.aff > gaeilge.aff.iso-8859-1
ispellaff2myspell gaeilge.aff.iso-8859-1 --myheader header | sed -e "s/\"\"/0/g" | sed -e "s/\"//g" > ga_IE.aff

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p ga_IE.dic ga_IE.aff $RPM_BUILD_ROOT/%{_datadir}/myspell


%files
%doc README ChangeLog
%license COPYING
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.0-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 5.0-3
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 5.0-1
- Update Source tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Sep 12 2016 Caolán McNamara <caolanm@redhat.com> - 4.6-12
- Resolves: rhbz#1373537 rebuild to fix problem caused by earlier grep

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 4.6-11
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Caolán McNamara <caolanm@redhat.com> - 4.6-6
- Resolves: rhbz#967637 encoding bustage

* Mon May 27 2013 Caolán McNamara <caolanm@redhat.com> - 4.6-5
- Resolves: rhbz#967637 empty ga.aff

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jun 29 2011 Caolán McNamara <caolanm@redhat.com> - 4.6-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 Caolán McNamara <caolanm@redhat.com> - 4.5-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug 05 2008 Caolán McNamara <caolanm@redhat.com> - 4.4-1
- latest version

* Wed Mar 05 2008 Caolán McNamara <caolanm@redhat.com> - 4.3-3
- build the .aff from gaeilge.aff and ispellaff2myspell

* Tue Mar 04 2008 Caolán McNamara <caolanm@redhat.com> - 4.3-2
- update to latest .aff

* Mon Nov 05 2007 Caolán McNamara <caolanm@redhat.com> - 4.3-1
- latest version

* Mon Aug 20 2007 Caolán McNamara <caolanm@redhat.com> - 4.2-1
- bump to latest upstream

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 0.20060731-2
- clarify license version

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20060731-1
- initial version
