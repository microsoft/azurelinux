Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: mythes-sl
Summary: Slovenian thesaurus
%global upstreamid 20130130
Version: 0.%{upstreamid}
Release: 16%{?dist}
Source: https://88.200.20.8:85/download/thes_sl_SI_v2.zip
URL: https://www.tezaver.si/
License: LGPLv2+
BuildArch: noarch
Requires: mythes
Supplements: (mythes and langpacks-sl)

%description
Slovenian thesaurus.

%prep
%autosetup -c

%build
chmod -x *
for i in README_th_sl_SI_v2.txt; do
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done


%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_sl_SI_v2.* $RPM_BUILD_ROOT/%{_datadir}/mythes


%files
%license README_th_sl_SI_v2.txt
%{_datadir}/mythes/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20130130-16
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20130130-11
- Remove unneeded BuildRequires:
- Update Source URL

* Mon Mar 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.20130130-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130130-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

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
- Resolves: rhbz#905955 latest version

* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120912-1
- latest version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120613-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120613-1
- latest version

* Wed Apr 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120413-1
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

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101221-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101221-1
- latest version

* Sun Oct 31 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101031-1
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

* Sun Apr 04 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100319-2
- mythes now owns /usr/share/mythes

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

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090708-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090708-2
- tidy spec

* Wed Jul 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090708-1
- latest version

* Mon Jun 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090608-1
- latest version

* Sat Mar 28 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090328-1
- latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 22 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090222-1
- latest version

* Wed Jan 21 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090121-1
- initial version
