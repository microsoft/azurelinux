Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: hunspell-de
Summary: German hunspell dictionaries
%global upstreamid 20161207
Version: 0.%{upstreamid}
Release: 6%{?dist}
Source: https://www.j3e.de/ispell/igerman98/dict/igerman98-%{upstreamid}.tar.bz2
URL: https://www.j3e.de/ispell/igerman98
License: GPLv2 or GPLv3
BuildArch: noarch
BuildRequires: aspell, hunspell, perl-interpreter

Requires: hunspell
Supplements: (hunspell and langpacks-de)

%description
German (Germany, Switzerland, etc.) hunspell dictionaries.

%prep
%setup -q -n igerman98-%{upstreamid}
sed -i -e "s/AFFIX_EXPANDER = ispell/AFFIX_EXPANDER = aspell/g" Makefile

%build
LC_ALL=C make hunspell/de_AT.dic hunspell/de_AT.aff \
     hunspell/de_CH.dic hunspell/de_CH.aff \
     hunspell/de_DE.dic hunspell/de_DE.aff
cd hunspell
for i in README_*.txt; do
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
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cd hunspell
cp -p de_??.dic de_??.aff $RPM_BUILD_ROOT/%{_datadir}/myspell

pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
de_DE_aliases="de_BE de_LU"
for lang in $de_DE_aliases; do
	ln -s de_DE.aff $lang.aff
	ln -s de_DE.dic $lang.dic
done
de_CH_aliases="de_LI"
for lang in $de_CH_aliases; do
	ln -s de_CH.aff $lang.aff
	ln -s de_CH.dic $lang.dic
done
popd


%files
%doc hunspell/README_de_??.txt hunspell/COPYING_GPLv2 hunspell/COPYING_GPLv3 hunspell/Copyright
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20161207-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20161207-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Michael Stahl <mstahl@redhat.com> - 0.20161207-1
- Resolves: rhbz#1549640 upgrade to latest release

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160407-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160407-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20160407-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jul 20 2016 Michael Stahl <mstahl@redhat.com> - 0.20160407-1
- Resolves: rhbz#1344662 upgrade to latest release
- switch source URL to https
- revert the GNU grep 2.23 LANG=C bug workaround
- added explicit build dependency on perl, now required on rawhide

* Fri Apr 01 2016 Michael Stahl <mstahl@redhat.com> - 0.20151222-4
- Resolves: rhbz#1316359 grep 2.23 broke the build

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20151222-3
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20151222-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Michael Stahl <mstahl@redhat.com> - 0.20151222-1
- upgrade to latest version
- upstream removed "OASIS distribution license agreement 0.1", only GPLv2/v3 now
- remove needless use of percent-defattr

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20131206-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20131206-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Mar 10 2014 Michael Stahl <mstahl@redhat.com> - 0.20131206-1
- latest version
- sed refuses to execute bin/dic2iso and iso2dic unless run in ISO8859 locale

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120607-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120607-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20120607-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Caolán McNamara <caolanm@redhat.com> - 0.20120607-1
- latest version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110609-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 09 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110609-1
- latest version

* Mon Mar 21 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110321-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100727-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 30 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100727-1
- latest version

* Thu Oct 08 2009 Caolán McNamara <caolanm@redhat.com> - 0.20091006-1
- latest version
- drop integrated igerman98-20090107-useaspell.patch

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090107-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jul 11 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090107-3
- tidy spec

* Thu Apr 23 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090107-2
- fix dictionaries

* Thu Feb 26 2009 Caolán McNamara <caolanm@redhat.com> - 0.20090107-1
- latest version

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20071211-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 11 2007 Caolán McNamara <caolanm@redhat.com> - 0.20071211-1
- latest version

* Thu Aug 30 2007 Caolán McNamara <caolanm@redhat.com> - 0.20070829-1
- latest version
- build from canonical source

* Fri Aug 03 2007 Caolán McNamara <caolanm@redhat.com> - 0.20051213-2
- clarify license version

* Thu Dec 07 2006 Caolán McNamara <caolanm@redhat.com> - 0.20051213-1
- initial version
