# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%global dict_dirname hunspell
%else
%global dict_dirname myspell
%endif

Name: hunspell-bn
Summary: Bengali hunspell dictionaries
Version: 1.0.0
Release: 28%{?dist}
Epoch: 1
Source: http://anishpatil.fedorapeople.org/bn_in.%{version}.tar.gz
URL: https://gitorious.org/hunspell_dictionaries/hunspell_dictionaries.git
License: GPL-2.0-or-later
BuildArch: noarch

Requires: hunspell-filesystem
Supplements: (hunspell and langpacks-bn)

%description
Bengali hunspell dictionaries.

%prep
%autosetup -c -n bn_IN
# fix file permissions
chmod 644 bn_IN/*

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p bn_IN/*.dic bn_IN/*.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
pushd $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
bn_IN_aliases="bn_BD"
for lang in ${bn_IN_aliases}; do
    ln -s bn_IN.aff $lang.aff
    ln -s bn_IN.dic $lang.dic
done
popd


%files
%doc bn_IN/README
%license bn_IN/COPYING bn_IN/Copyright
%{_datadir}/%{dict_dirname}/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 23 2022 Parag Nemade <pnemade AT redhat DOT com> - 1:1.0.0-21
- Update license tag to SPDX format

* Mon Sep 05 2022 Mike FABIAN <mfabian@redhat.com> - 1:1.0.0-20
- Add symlinks from bn_IN.{dic,aff} -> bn_BD.{dic,aff}

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 22 2022 Parag Nemade <pnemade AT redhat DOT com> - 1:1.0.0-18
- Add conditional for new hunspell dir path and update to Requires:
  hunspell-filesystem

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

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
