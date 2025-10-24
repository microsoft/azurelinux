Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global upstreamid 20250916

Summary:        German thesaurus
Name:           mythes-de
Version:        0.%{upstreamid}
Release:        1%{?dist}
License:        LGPL-2.1-or-later OR CC-BY-SA-4.0
URL:            https://www.openthesaurus.de/
Source0:        https://www.openthesaurus.de/export/Deutscher-Thesaurus.oxt#/Deutscher-Thesaurus-%{version}.oxt
Source1:        https://www.openthesaurus.de/export/Schweizer-Thesaurus.oxt#/Schweizer-Thesaurus-%{version}.oxt
BuildArch:      noarch
Requires:       mythes

Supplements:    (mythes and langpacks-de)

%description
German thesaurus.

%prep
%autosetup -c
rm -rf mythes-ch-%{upstreamid}
mkdir mythes-ch-%{upstreamid}
cd mythes-ch-%{upstreamid}
unzip -q %{SOURCE1}

%build
for i in README.txt; do
  if ! iconv -f utf-8 -t utf-8 -o /dev/null $i > /dev/null 2>&1; then
    iconv -f ISO-8859-1 -t UTF-8 $i > $i.new
    touch -r $i $i.new
    mv -f $i.new $i
  fi
  tr -d '\r' < $i > $i.new
  touch -r $i $i.new
  mv -f $i.new $i
done

%install
mkdir -p $RPM_BUILD_ROOT%{_datadir}/mythes/
cp -p th_de_DE_v2.* $RPM_BUILD_ROOT%{_datadir}/mythes/
cp -p mythes-ch-%{upstreamid}/th_de_DE_v2.idx $RPM_BUILD_ROOT%{_datadir}/mythes/th_de_CH_v2.idx
cp -p mythes-ch-%{upstreamid}/th_de_DE_v2.dat $RPM_BUILD_ROOT%{_datadir}/mythes/th_de_CH_v2.dat

pushd $RPM_BUILD_ROOT%{_datadir}/mythes/
  de_DE_aliases="de_AT de_BE de_LI de_LU"
  for lang in $de_DE_aliases; do
    ln -s th_de_DE_v2.idx "th_"$lang"_v2.idx"
    ln -s th_de_DE_v2.dat "th_"$lang"_v2.dat"
  done
popd

%files
%doc README.txt
%{_datadir}/mythes/*

%changelog
* Fri Dec 20 2024 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.20250916-1
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License Verified.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20240601-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 02 2024 Robert Scheck <robert@fedoraproject.org> 0.20240601-1
- Upgrade to latest daily snapshot release

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20230601-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20230601-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20230601-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 02 2023 Robert Scheck <robert@fedoraproject.org> 0.20230601-1
- Upgrade to latest daily snapshot release

* Thu Feb 23 2023 Caolán McNamara <caolanm@redhat.com> - 0.20220716-4
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20220716-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20220716-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sun Jul 17 2022 Robert Scheck <robert@fedoraproject.org> 0.20220716-1
- Upgrade to latest daily snapshot release

* Mon Apr 18 2022 Robert Scheck <robert@fedoraproject.org> 0.20220417-1
- Upgrade to latest daily snapshot release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.20220115-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Jan 16 2022 Robert Scheck <robert@fedoraproject.org> 0.20220115-1
- Upgrade to latest daily snapshot release

* Wed Sep 01 2021 Robert Scheck <robert@fedoraproject.org> 0.20210831-1
- Upgrade to latest daily snapshot release

* Sat Jul 24 2021 Robert Scheck <robert@fedoraproject.org> 0.20210723-1
- Upgrade to latest daily snapshot release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20210302-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Robert Scheck <robert@fedoraproject.org> 0.20210302-1
- Upgrade to latest daily snapshot release

* Sun Jan 31 2021 Robert Scheck <robert@fedoraproject.org> 0.20210130-1
- Upgrade to latest daily snapshot release

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.20201226-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Dec 27 2020 Robert Scheck <robert@fedoraproject.org> 0.20201226-1
- Upgrade to latest daily snapshot release

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20190325-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20190325-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20190325-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 26 2019 Robert Scheck <robert@fedoraproject.org> 0.20190325-1
- Upgrade to latest daily snapshot release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20180226-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20180226-3
- Remove unneeded BuildRequires:

* Mon Mar 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.20180226-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 27 2018 Michael Stahl <mstahl@redhat.com> - 0.20180226-1
- upgrade to latest daily snapshot release

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20151216-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20151216-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20151216-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20151216-3
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20151216-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Michael Stahl <mstahl@redhat.com> - 0.20151216-1
- upgrade to latest daily snapshot release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20140309-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20140309-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Michael Stahl <mstahl@redhat.com> - 0.20140309-1
- upgrade to latest version

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 06 2013 Caolán McNamara <caolanm@redhat.com> - 0.20130206-1
- Resolves: rhbz#905994 upgrade to latest version

* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120911-1
- upgrade to latest version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120612-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120612-1
- upgrade to latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20111124-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 25 2011 Michael Stahl <mstahl@redhat.com> - 0.20111124-2
- add the de_CH variant for Swiss people and people with ß allergy

* Fri Nov 25 2011 Michael Stahl <mstahl@redhat.com> - 0.20111124-1
- upgrade to latest version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090708-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Apr 03 2010 Caolan McNamara <caolanm@redhat.com> - 0.20090708-4
- mythes now owns /usr/share/mythes

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090708-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090708-2
- tidy spec

* Wed Jul 08 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090708-1
- latest version

* Mon Jun 08 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090608-1
- latest version

* Thu Apr 02 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090402-1
- latest version

* Mon Mar 02 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090302-1
- latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090202-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090202-1
- latest version

* Tue Dec 23 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081223-1
- latest version

* Sun Nov 23 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081123-1
- latest version

* Thu Oct 16 2008 Caolan McNamara <caolanm@redhat.com> - 0.20081016-1
- latest version

* Mon Sep 01 2008 Caolan McNamara <caolanm@redhat.com> - 0.20080901-1
- latest version

* Thu Jul 31 2008 Caolan McNamara <caolanm@redhat.com> - 0.20080731-1
- latest version
