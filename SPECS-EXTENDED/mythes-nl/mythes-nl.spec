Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: mythes-nl
Summary: Dutch thesaurus
%global upstreamid 20130131
Version: 0.%{upstreamid}
Release: 14%{?dist}
Source: https://data.opentaal.org/opentaalbank/thesaurus/download/thes_nl.oxt
URL: https://data.opentaal.org/opentaalbank/thesaurus
License: BSD or CC-BY
BuildArch: noarch
Requires: mythes
Supplements: (mythes and langpacks-nl)

%description
Dutch thesaurus.

%prep
%setup -q -c

%build
for i in README_th_nl.txt; do
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
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_nl_v2.dat $RPM_BUILD_ROOT/%{_datadir}/mythes/th_nl_NL_v2.dat
cp -p th_nl_v2.idx $RPM_BUILD_ROOT/%{_datadir}/mythes/th_nl_NL_v2.idx

pushd $RPM_BUILD_ROOT/%{_datadir}/mythes/
nl_NL_aliases="nl_AW nl_BE"
for lang in $nl_NL_aliases; do
        ln -s th_nl_NL_v2.dat "th_"$lang"_v2.dat"
        ln -s th_nl_NL_v2.idx "th_"$lang"_v2.idx"
done


%files
%license README_th_nl.txt
%{_datadir}/mythes/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20130131-14
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20130131-6
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20130131-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130131-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130131-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20130131-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jan 31 2013 Caolán McNamara <caolanm@redhat.com> - 0.20130131-1
- Resolves: rhbz#905991 latest version

* Wed Sep 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120912-1
- latest version

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120613-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120613-1
- latest version

* Fri Apr 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120413-1
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

* Wed Nov 10 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101110-1
- latest version

* Fri Oct 01 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100930-1
- latest version

* Sun Apr 04 2010 Caolán McNamara <caolanm@redhat.com> - 0.20090731-2
- mythes now owns /usr/share/mythes

* Fri Jan 22 2010 Caolán McNamara <caolanm@redhat.com> - 0.20090731-1
- latest version

* Tue Jan 05 2010 Caolán McNamara <caolanm@redhat.com> - 0.20090708-4
- Wrong license

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090708-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090708-2
- tidy spec

* Wed Jul 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090708-1
- latest version

* Fri Jun 12 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090608-2
- extend coverage

* Mon Jun 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090608-1
- latest version

* Wed Mar 25 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090325-1
- initial version
