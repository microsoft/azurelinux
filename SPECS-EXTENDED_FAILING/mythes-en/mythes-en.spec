Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: mythes-en
Summary: English thesaurus
Version: 3.0
Release: 30%{?dist}
Source: http://www.danielnaber.de/wn2ooo/wn2ooo20050723.tgz#/%{name}-%{version}.tar.gz
URL: http://www.danielnaber.de/wn2ooo/
BuildRequires: python3-devel
BuildRequires: perl-interpreter
BuildRequires: wordnet = %{version}
# License BSD is for the th_gen_idx.pl file
# License Artistic Clarified is for python files
License: BSD and Artistic clarified
BuildArch: noarch
Requires: mythes
Supplements: (mythes and langpacks-en)

Patch0: mythes-en.python3.patch

%description
English thesaurus.

%prep
%setup -q -c %{name}-%{version}
%patch0 -p1 -b .python3

%build
export WNHOME=/usr/share/wordnet-%{version}
python3 wn2ooo/wn2ooo.py > th_en_US_v2.dat
cat th_en_US_v2.dat | perl wn2ooo/th_gen_idx.pl > th_en_US_v2.idx


%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/mythes
cp -p th_en_US_v2.* $RPM_BUILD_ROOT/%{_datadir}/mythes

pushd $RPM_BUILD_ROOT/%{_datadir}/mythes/
en_US_aliases="en_AG en_AU en_BS en_BW en_BZ en_CA en_DK en_GB en_GH en_IE en_IN en_JM en_MW en_NA en_NG en_NZ en_PH en_SG en_TT en_ZA en_ZM en_ZW"
for lang in $en_US_aliases; do
        ln -s th_en_US_v2.idx "th_"$lang"_v2.idx"
        ln -s th_en_US_v2.dat "th_"$lang"_v2.dat"
done
popd


%files
%doc wn2ooo/LICENSE_th_gen_idx.txt wn2ooo/README.txt
%{_datadir}/mythes/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.0-30
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 05 2019 Stephan Bergmann <sbergman@redhat.com> - 3.0-27
- Use /usr/share instead of _datadir macro for build dependencies

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 17 2018 Parag Nemade <pnemade AT redhat DOT com> - 3.0-24
- Fix the License tag

* Mon Jul 30 2018 Caolán McNamara <caolanm@redhat.com> - 3.0-24
- Related: rhbz#1604911 convert python2 to python3, verified
  that output th_en_US_v2.dat and th_en_US_v2.idx are identical
  before and after

* Fri Jul 20 2018 Caolán McNamara <caolanm@redhat.com> - 3.0-23
- Resolves: rhbz#1604911 FTBFS

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.0-21
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 3.0-17
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Apr 12 2012 Caolán McNamara <caolanm@redhat.com> - 3.0-10
- add some aliases

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Apr 07 2010 Caolán McNamara <caolanm@redhat.com> - 3.0-7
- clarify licence of tools

* Sat Apr 03 2010 Caolán McNamara <caolanm@redhat.com> - 3.0-6
- mythes now owns /usr/share/mythes

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 12 2009 Caolán McNamara <caolanm@redhat.com> - 3.0-4
- extend coverage

* Wed Jun 10 2009 Caolán McNamara <caolanm@redhat.com> - 3.0-3
- rebuild against wordnet package

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 28 2007 Caolán McNamara <caolanm@redhat.com> - 3.0-1
- initial version
