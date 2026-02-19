Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%if 0%{?fedora} > 35
%global dict_dirname hunspell 
%else
%global dict_dirname myspell
%endif
Name: hunspell-pl
Summary: Polish hunspell dictionaries
%global upstreamid 20240901
Version: 0.%{upstreamid}
Release: 2%{?dist}
Source: https://sjp.pl/sl/ort/sjp-myspell-pl-%{upstreamid}.zip
URL: https://sjp.pl/sl/ort/
License: LGPL-2.1-or-later OR GPL-1.0-or-later OR MPL-1.1 OR Apache-2.0 OR CC-BY-SA-4.0
BuildArch: noarch
 
Requires: hunspell
Supplements: (hunspell and langpacks-pl)
 
%description
Polish hunspell dictionaries.
 
%prep
%autosetup -c hunspell-pl
 
%build
unzip pl_PL.zip
 
%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/%{dict_dirname}
 
 
%files
%doc README_pl_PL.txt
%{_datadir}/%{dict_dirname}/*
 
%changelog
* Tue Dec 17 2024 Akarsh Chaudhary <v-akarshc@microsoft.com> - 0.20240901-2
- AzureLinux import from Fedora 41 .
- License verified

* Sun Sep 01 2024 Artur Frenszek-Iwicki <fedora@svgames.pl> - 0.20240901-1
- Update to new upstream release (2024-09-01)
 
* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20240301-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild
 
* Tue Mar 19 2024 Parag Nemade <pnemade AT redhat DOT com> - 0.20240301-1
- Update to new upstream release 20240301 (#2270165)
 
* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20230601-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20230601-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild
 
* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20230601-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild
 
* Thu Jun 08 2023 Paweł Marciniak <sunwire+repo@gmail.com> - 0.20230601-1
- Update to the latest version
 
* Wed Feb 22 2023 Caolán McNamara <caolanm@redhat.com> - 0.20160720-13
- migrated to SPDX license
 
* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
 
* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild
 
* Fri Feb 11 2022 Vishal Vijayraghavan <vishalvvr@fedoraproject.org> - 0.20180707-10
- rename install directory name from myspell to hunspell
- https://fedoraproject.org/wiki/Changes/Hunspell_dictionary_dir_change
 
* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild
 
* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild
 
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild
 
* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
 
* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
 
* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
 
* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
 
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180707-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
 
* Sun Jul 08 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20180707-1
- Update to new upstream release
 
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160720-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
 
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160720-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
 
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160720-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
 
* Wed Jul 20 2016 Caolán McNamara <caolanm@redhat.com> - 0.20160720-1
- Resolves: rhbz#1358280 latest version
 
* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20130130-6
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines
 
* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild
 
* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130130-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
 
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130130-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
 
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130130-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
 
* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 0.20130130-1
- latest version
 
* Fri Nov 02 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120912-2
- add CC-BY-SA to license field
 
* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120912-1
- latest version
 
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120613-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
 
* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120613-1
- latest version
 
* Fri Mar 09 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120309-1
- latest version
 
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20111017-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
 
* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 0.20111017-1
- latest version
 
* Mon Aug 08 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110808-1
- latest version
 
* Thu Jun 09 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110609-1
- latest version
 
* Fri Mar 18 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110318-1
- latest version
 
* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101221-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
 
* Tue Dec 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101221-1
- latest version
 
* Thu Oct 28 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101028-1
- latest version
 
* Fri Sep 24 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100924-1
- latest version
 
* Mon Aug 23 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100823-1
- latest version
 
* Tue Jul 20 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100720-1
- latest version
 
* Sat Jun 19 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100619-1
- latest version
 
* Wed May 19 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100519-1
- latest version
 
* Mon Apr 19 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100419-1
- latest version
 
* Fri Mar 19 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100319-1
- latest version
 
* Thu Feb 18 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100218-1
- latest version
 
* Mon Jan 18 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100118-1
- latest version
 
* Thu Dec 17 2009 Caolán McNamara <caolanm@redhat.com> - 0.20091217-1
- latest version
 
* Tue Nov 17 2009 Caolán McNamara <caolanm@redhat.com> - 0.20091117-1
- latest version
 
* Tue Sep 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090908-1
- latest version
 
* Sat Aug 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090808-1
- latest version
 
* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090708-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
 
* Wed Jul 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090708-1
- latest version
 
* Mon Jun 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090608-1
- latest version
 
* Sun Apr 19 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090419-1
- latest version
 
* Sun Mar 15 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090315-1
- latest version
 
* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090215-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
 
* Sun Feb 15 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090215-1
- latest version
 
* Wed Jan 14 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090114-1
- latest version
 
* Sat Aug 23 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080823-1
- latest version
 
* Tue Jul 15 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080715-1
- latest version
 
* Sat Jun 14 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080614-1
- latest version
 
* Tue May 13 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080513-1
- latest version
 
* Mon Apr 07 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080407-1
- latest version
 
* Tue Mar 04 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080304-1
- source file name changed, update to latest version
 
* Wed Feb 13 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080213-1
- new version
 
* Wed Jan 09 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080109-1
- new version
 
* Sat Dec 08 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071208-1
- new version
 
* Thu Nov 15 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071114-1
- new version
 
* Fri Oct 05 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071004-1
- new version
 
* Mon Sep 03 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070903-1
- new version
 
* Thu Aug 09 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070803-1
- clarify that is tri-licensed
 
* Sun Jul 01 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070701-1
- latest version
- near daily updates => move to a pick it up the 1st of the month cycle
 
* Fri Jun 29 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070629-1
- latest version
 
* Fri Jun 22 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070622-1
- latest version