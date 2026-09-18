# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%if 0%{?fedora} >= 36 || 0%{?rhel} > 9
%global dict_dirname hunspell
%else
%global dict_dirname myspell
%endif

Name: hunspell-da
Summary: Danish hunspell dictionaries
Version: 1.7.42
Release: 27%{?dist}
Source: http://da.speling.org/filer/myspell-da-%{version}.tar.bz2
URL: http://da.speling.org/
License: GPL-2.0-or-later
BuildArch: noarch

Requires: hunspell-filesystem
Supplements: (hunspell and langpacks-da)

%description
Danish hunspell dictionaries.

%prep
%setup -q -n myspell-da-%{version}

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}


%files
%doc README Copyright contributors COPYING
%{_datadir}/%{dict_dirname}/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 22 2023 Caolán McNamara <caolanm@redhat.com> - 1.7.42-21
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Mar 22 2022 Parag Nemade <pnemade AT redhat DOT com> - 1.7.42-18
- Add conditional for new hunspell dir path and update to Requires:
  hunspell-filesystem

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 1.7.42-6
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.42-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.42-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.42-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 1.7.42-1
- latest version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 1.7.41-1
- latest version

* Mon Mar 12 2012 Caolán McNamara <caolanm@redhat.com> - 1.7.40-1
- latest version

* Fri Mar 09 2012 Caolán McNamara <caolanm@redhat.com> - 1.7.39-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Apr 04 2011 Caolán McNamara <caolanm@redhat.com> - 1.7.37-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 28 2010 Caolán McNamara <caolanm@redhat.com> - 1.7.36-1
- latest version

* Tue Sep 28 2010 Caolán McNamara <caolanm@redhat.com> - 1.7.35-1
- latest version

* Wed Jul 28 2010 Caolán McNamara <caolanm@redhat.com> - 1.7.34-1
- latest version

* Sun Mar 28 2010 Caolán McNamara <caolanm@redhat.com> - 1.7.33-1
- latest version

* Thu Mar 11 2010 Caolán McNamara <caolanm@redhat.com> - 1.7.32-1
- latest version

* Thu Dec 10 2009 Caolán McNamara <caolanm@redhat.com> - 1.7.31-1
- latest version

* Thu Nov 05 2009 Caolán McNamara <caolanm@redhat.com> - 1.7.30-1
- latest version

* Fri Sep 04 2009 Caolán McNamara <caolanm@redhat.com> - 1.7.29-1
- latest version

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 19 2009 Caolán McNamara <caolanm@redhat.com> - 1.7.28-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 02 2009 Caolán McNamara <caolanm@redhat.com> - 1.7.27-1
- latest version

* Sun Nov 23 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.26-1
- latest version

* Tue Oct 14 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.25-1
- latest version

* Mon Sep 08 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.24-1
- latest version

* Thu Aug 07 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.23-1
- latest version

* Mon Jul 07 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.22-1
- latest version

* Fri May 30 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.21-1
- latest version

* Thu Apr 24 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.20-1
- latest version

* Mon Mar 17 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.19-1
- latest version

* Wed Feb 13 2008 Caolán McNamara <caolanm@redhat.com> - 1.7.18-1
- latest version

* Wed Nov 28 2007 Caolán McNamara <caolanm@redhat.com> - 1.7.17-1
- latest version

* Fri Oct 05 2007 Caolán McNamara <caolanm@redhat.com> - 1.7.16-1
- latest version

* Thu Aug 30 2007 Caolán McNamara <caolanm@redhat.com> - 1.7.15-1
- latest version

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 1.7.14-2
- clarify license version

* Mon Jul 30 2007 Caolán McNamara <caolanm@redhat.com> - 1.7.14-1
- latest version

* Mon Jul 09 2007 Caolán McNamara <caolanm@redhat.com> - 1.7.13-1
- latest version

* Tue Feb 13 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070106-1
- new upstream dictionaries

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20050330-1
- initial version
