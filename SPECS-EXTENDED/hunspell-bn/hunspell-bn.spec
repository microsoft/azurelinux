Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-bn
Summary: Bengali hunspell dictionaries
Version: 1.0.0
Release: 15%{?dist}
Source: https://anishpatil.fedorapeople.org/bn_in.%{version}.tar.gz
URL: https://gitorious.org/hunspell_dictionaries/hunspell_dictionaries.git
License: GPLv2+
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-bn)

%description
Bengali hunspell dictionaries.

%prep
%autosetup -c -n bn_IN
# fix file permissions
chmod 644 bn_IN/*

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p bn_IN/*.dic bn_IN/*.aff $RPM_BUILD_ROOT/%{_datadir}/myspell


%files
%doc bn_IN/README
%license bn_IN/COPYING bn_IN/Copyright
%{_datadir}/myspell/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.0.0-15
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.0.0-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Sep 28 2017 Parag Nemade <pnemade AT redhat DOT com> - 1:1.0.0-8
- Fix the upstream URL (rh#1294622)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1:1.0.0-5
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 17 2014 Anish Patil<apatil@redhat.com> - 1:1.0.0-1
- Upstream has changed and built with new tarball

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.06-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.06-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Parag <pnemade@redhat.com> - 1:0.06-1
- Update to 0.06 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.04-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Mar 25 2010 Parag <pnemade AT redhat.com> - 1:0.04-2
- Resolves:rh#576774  - newer release 0.04 made symlink to bn_BD nonexistent

* Tue Mar 09 2010 Parag <pnemade AT redhat.com> - 1:0.04-1
- Resolves:rh#571712 - Should use correct version what upstream provides by adding epoch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080201-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080201-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 08 2008 Parag <pnemade@redhat.com> - 20080201-1
- update to latest release.

* Tue Sep 02 2008 Caolán McNamara <caolanm@redhat.com> - 20050726-3
- add bn_BD alias

* Sun Jan 06 2008 Parag <pnemade@redhat.com> - 20050726-2
- Added Copyright and corrected changelog version.

* Thu Jan 03 2008 Parag <pnemade@redhat.com> - 20050726-1
- Initial Fedora release
