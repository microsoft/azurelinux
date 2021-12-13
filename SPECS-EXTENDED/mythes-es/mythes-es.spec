Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: mythes-es
Summary: Spanish thesaurus
Version: 2.3
Release: 7%{?dist}
Source: https://github.com/sbosio/rla-es/releases/download/v%{version}/es_ANY.oxt
URL: https://github.com/sbosio/rla-es/tree/master/sinonimos
License: LGPLv2+
BuildArch: noarch
Requires: mythes
Supplements: (mythes and langpacks-es)

%description
Spanish thesaurus.

%prep
%setup -q -c -n %{name}


%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_es_ES_v2.* $RPM_BUILD_ROOT/%{_datadir}/mythes

pushd $RPM_BUILD_ROOT/%{_datadir}/mythes/
es_aliases="es_AR es_BO es_CL es_CO es_CR es_CU es_DO es_EC es_GT es_HN es_MX es_NI es_PA es_PE es_PR es_PY es_SV es_US es_UY es_VE"

for lang in $es_aliases; do
        ln -s th_es_ES_v2.dat "th_"$lang"_v2.dat"
        ln -s th_es_ES_v2.idx "th_"$lang"_v2.idx"
done
popd

mv COPYING_th_es_ES COPYING

%files
%doc README_th_es_ES.txt
%license COPYING
%{_datadir}/mythes/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3-7
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Ismael Olea <ismael@olea.org> - 2.3-1
- update to v2.3

* Fri Jan 5 2018 Ismael Olea <ismael@olea.org> - 2.2-1
- updating to v2.2
- upstream changed to github
- cleaning obsolete SPEC conventions

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150304-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150304-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20150304-4
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20150304-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20150304-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 04 2015 Caolán McNamara <caolanm@redhat.com> - 0.20150304-1
- Resolves: rhbz#1197184 berlios has disappeared, but rla-es seems
  active, and using e.g. "a priori" as an example LibreOffice suggests
  a non-corrupted set of suggestions

* Wed Mar 04 2015 Caolán McNamara <caolanm@redhat.com> - 0.20140516-1
- Related: rhbz#1197184 latest version

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130102-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130102-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 0.20130102-1
- Resolves: rhbz#905972 latest version

* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120902-1
- latest version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120602-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120602-1
- latest version

* Fri Apr 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120402-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20111002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 0.20111002-1
- latest version

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20101002-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 11 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101002-1
- latest version

* Fri Sep 24 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100902-1
- latest version

* Fri Jul 02 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100701-1
- latest version

* Sat Jun 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100601-1
- latest version

* Tue Apr 06 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100401-3
- add COPYING to doc

* Sat Apr 03 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100401-2
- mythes now owns /usr/share/mythes

* Fri Apr 02 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100401-1
- latest version

* Mon Mar 01 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100301-1
- latest version

* Tue Feb 02 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100201-1
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

* Mon Apr 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090406-1
- latest version

* Fri Mar 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090306-1
- latest version

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090206-1
- initial version
