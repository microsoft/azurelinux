%global dict_dirname hunspell
%global upstreamid 20201207
Summary:        English hunspell dictionaries
Name:           hunspell-en
Version:        0.%{upstreamid}
Release:        1%{?dist}
# README_en_GB.txt has specified just LGPL which mean LGPLv2+
# scowl/speller/aspell/en_affix.dat is BSD
# scowl/speller/aspell/en_phonet.dat is LGPLv2
License:        LGPLv2+ AND LGPLv2 AND BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://wordlist.sourceforge.net/
Source0:        https://github.com/en-wl/wordlist/archive/refs/tags/rel-2020.12.07.tar.gz#/%{name}-%{version}.tar.gz
Source1:        http://download.services.openoffice.org/contrib/dictionaries/en_GB.zip
#See http://mxr.mozilla.org/mozilla/source/extensions/spellcheck/locales/en-US/hunspell/mozilla_words.diff?raw=1
Patch0:         mozilla_words.patch
Patch1:         en_GB-singleletters.patch
Patch2:         en_GB.two_initial_caps.patch
#See https://github.com/en-wl/wordlist/issues/15
#filter removes words with "." in them
Patch3:         en_US-strippedabbrevs.patch
#See https://sourceforge.net/p/hunspell/patches/35
#to allow "didn't" instead of suggesting change to typographical apostrophe
Patch4:         hunspell-en-allow-non-typographical.marks.patch
#See https://bugzilla.redhat.com/show_bug.cgi?id=619577 add SI and IEC prefixes
Patch5:         hunspell-en-SI_and_IEC.patch
#See https://github.com/en-wl/wordlist/issues/46 obscure Calender hides misspelling of Calendar
Patch6:         hunspell-en-calender.patch
#valid English words that are archaic or rare in en-GB but not in en-IE
Patch7:         en_IE.supplemental.patch
#call git to get the release hash, but this is a tarball
Patch8:         hunspell-en-dont-call-git-during-build.patch
#rhbz#1492306 for better or worse treat etc the same in US and GB
Patch9:         en_GB.etc.patch
Patch10:        hunspell-en-buildfix.patch
BuildRequires:  aspell
BuildRequires:  dos2unix
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  perl-Getopt-Long
BuildRequires:  zip
Requires:       hunspell
Requires:       hunspell-en-US = %{version}-%{release}
Requires:       hunspell-en-GB = %{version}-%{release}
Supplements:    langpacks-en
BuildArch:      noarch

%description
English (US, UK, etc.) hunspell dictionaries

%package US
Summary:        US English hunspell dictionaries
Requires:       hunspell

%description US
US English hunspell dictionaries

%package GB
Summary:        UK English hunspell dictionaries
Requires:       hunspell
Supplements:    (hunspell and langpacks-en_GB)

%description GB
UK English hunspell dictionaries

%prep
%setup -q -n wordlist-rel-2020.12.07
%setup -q -T -D -a 1 -n wordlist-rel-2020.12.07
%patch -P 0 -p0 -b .mozilla
%patch -P 1 -p1 -b .singleletters
%patch -P 2 -p1 -b .two_initial_cap
%patch -P 3 -p0 -b .strippedabbrevs
%patch -P 4 -p0 -b .allow-non-typographical
%patch -P 5 -p0 -b .SI_and_IEC
%patch -P 6 -p1 -b .calender
%patch -P 7 -p1 -b .en_IE
%patch -P 8 -p1 -b .nogit
%patch -P 9 -p1 -b .etc
%patch -P 10 -p1 -b .buildfix

%build
export PERL5LIB=`pwd`/scowl/r/varcon${PERL5LIB:+:${PERL5LIB}}
make
cd scowl/speller
make hunspell
for i in README_en_CA.txt README_en_US.txt; do
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
mkdir -p %{buildroot}/%{_datadir}/%{dict_dirname}
cp -p en_??.dic en_??.aff %{buildroot}/%{_datadir}/%{dict_dirname}
cd scowl/speller
cp -p en_??.dic en_??.aff %{buildroot}/%{_datadir}/%{dict_dirname}

pushd %{buildroot}/%{_datadir}/%{dict_dirname}/
en_GB_aliases="en_AG en_BS en_BW en_BZ en_DK en_GH en_HK en_IE en_IN en_JM en_MW en_NA en_NG en_NZ en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_GB_aliases; do
	ln -s en_GB.aff $lang.aff
	ln -s en_GB.dic $lang.dic
done
en_US_aliases="en_PH"
for lang in $en_US_aliases; do
	ln -s en_US.aff $lang.aff
	ln -s en_US.dic $lang.dic
done
popd

%files
%doc scowl/speller/README_en_CA.txt
%{_datadir}/%{dict_dirname}/*
%exclude %{_datadir}/%{dict_dirname}/en_GB.*
%exclude %{_datadir}/%{dict_dirname}/en_US.*

%files US
%doc scowl/speller/README_en_US.txt
%{_datadir}/%{dict_dirname}/en_US.*

%files GB
%doc README_en_GB.txt
%{_datadir}/%{dict_dirname}/en_GB.*

%changelog
* Thu Feb 01 2024 Sumedh Sharma <sumsharma@microsoft.com> - 0.20201207-1
- Bump version to 0.20201207

* Fri Sep 16 2022 Osama Esmail <osamaesmail@microsoft.com> - 0.20140811.1-18
- Moved from SPECS-EXTENDED to SPECS
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20140811.1-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 08 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 0.20140811.1-12
- Update Source tag

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Nov 20 2017 Peter Oliver <rpm@mavit.org.uk> - 0.20140811.1-10
- Have hunspell-en-GB installed when langpacks-en_GB is installed.
  Resolves: rhbz#1409136.

* Mon Sep 25 2017 Caolán McNamara <caolanm@redhat.com> - 0.20140811.1-9
- Resolves: rhbz#1494968 perl regex rule changes result in broken en_US dict

* Thu Sep 21 2017 Caolán McNamara <caolanm@redhat.com> - 0.20140811.1-8
- Resolves: rhbz#1492306 for better or worse treat etc the same in US and GB

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20140811.1-5
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Mon Feb 15 2016 Caolán McNamara <caolanm@redhat.com> - 0.20140811.1-4
- Resolves: rhbz#1307627 FTBFS

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20140811.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20140811.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 08 2014 Caolán McNamara <caolanm@redhat.com> - 0.20140811-1
- bump to latest version

* Wed Oct 08 2014 Caolán McNamara <caolanm@redhat.com> - 0.20121024-9
- Resolves: rhbz#1149720 add BitTorrent as a word

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121024-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 07 2014 Caolán McNamara <caolanm@redhat.com> - 0.20121024-7
- en-ZM different to the other locale ids

* Thu Oct 24 2013 Caolán McNamara <caolanm@redhat.com> - 0.20121024-6
- bump n-v-r to ensure rhbz#1022628 is resolved

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121024-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 12 2013 Caolán McNamara <caolanm@redhat.com> - 0.20121024-4
- Resolves: rhbz#980604 wordlist tarball unreproducible, use svn export and xz

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20121024-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 02 2012 Caolán McNamara <caolanm@redhat.com> - 0.20121024-2
- wordlist/scowl/speller/aspell/en_phonet.dat under bare LGPLv2

* Wed Oct 24 2012 Caolán McNamara <caolanm@redhat.com> - 0.20121024-1
- latest version
- drop integrated hunspell-en-irregular-plural-possessive.patch

* Thu Oct 11 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-9
- add possessive forms of irregular plurals for en-US, e.g. men's, women's

* Mon Aug 27 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-8
- Related: rhbz#850709 fix requires

* Mon Aug 27 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-7
- Resolves: rhbz#850709 allow installation of en-US and en-GB standalone

* Wed Aug 1 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-6
- Related: rhbz#573516 we don't need hunspell to build hunspell-en

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110318-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-4
- add Malawian alias

* Tue Apr 10 2012 Caolán McNamara <caolanm@redhat.com> - 0.20110318-3
- making a hames of it
- add Zambian alias

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110318-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar 18 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110318-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110112-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Feb 08 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110112-3
- Resolves: rhbz#675550 add Haskell as a known proper noun

* Thu Jan 13 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110112-1
- latest version

* Sun Jan 09 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110108-1
- latest version

* Tue Jan 04 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110104-1
- latest version

* Tue Dec 21 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101221-1
- latest version

* Tue Dec 14 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101211-1
- latest version

* Wed Dec 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.20101207-1
- latest version

* Fri Jul 30 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-6
- Resolves: rhbz#619577 add JEDEC prefixes

* Fri Jul 30 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-5
- Resolves: rhbz#619577 add SI and IEC prefixes

* Mon Jun 14 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-4
- Resolves: rhbz#603773 allow just non-typographical apostrophes

* Sun Jun 06 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-3
- Resolves: rhbz#600860 generate a higher level en-US dict

* Thu Apr 15 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-2
- allow non-typographical apostrophes

* Wed Mar 31 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100322-1
- latest version

* Mon Mar 08 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100308-1
- latest version

* Sat Jul 25 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-7
- add extra mozilla REPs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090216-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-5
- tidy spec

* Fri Jun 12 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-4
- extend coverage

* Sat Jun 06 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-3
- Change two suspicious words with two initial capitals in en_GB
  from ADte TEirtza to ADTe Teirtza

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090216-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090216-1
- fix upstreamed

* Mon Feb 16 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090208-1
- latest version

* Wed Jan 14 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090114-1
- latest version

* Sun Jan 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090110-1
- latest version

* Thu Dec 18 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081216-1
- latest version

* Sat Dec 06 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081205-1
- latest version

* Tue Dec 02 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081202-1
- latest version

* Sat Nov 29 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081129-1
- mozilla blog ... webmistresses signature range integrated

* Thu Nov 27 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081127-2
- abbrevs are always stripped out from US/CA dicts
- some single characters are missing from en_GB

* Thu Nov 27 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081127-1
- hardcoded path dropped upstream

* Tue Nov 25 2008 Caolán McNamara <caolanm@redhat.com> - 0.20081124-1
- latest version, i.e +Barack +Obama and co.

* Fri Aug 29 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080829-1
- latest version

* Fri Feb 08 2008 Caolán McNamara <caolanm@redhat.com> - 0.20080207-1
- canonical upstream source

* Thu Feb 07 2008 Caolán McNamara <caolanm@redhat.com> - 0.20061130-5
- apply mozilla word diff

* Tue Jan 15 2008 Caolán McNamara <caolanm@redhat.com> - 0.20061130-4
- clean up spec

* Mon Sep 17 2007 Caolán McNamara <caolanm@redhat.com> - 0.20061130-3
- new varient alias

* Thu Aug 09 2007 Caolán McNamara <caolanm@redhat.com> - 0.20061130-2
- clarify licence

* Fri Jun 01 2007 Caolán McNamara <caolanm@redhat.com> - 0.20061130-1
- update to latest dictionaries

* Thu Feb 08 2007 Caolán McNamara <caolanm@redhat.com> - 0.20040623-2
- update to new spec guidelines

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20040623-1
- initial version
