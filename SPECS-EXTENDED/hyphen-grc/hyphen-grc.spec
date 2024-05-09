Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hyphen-grc
Summary: Ancient Greek hyphenation rules
%global upstreamid 20110913
Version: 0.%{upstreamid}
Release: 18%{?dist}
#Source0: https://tug.org/svn/texhyphen/trunk/hyph-utf8/tex/generic/hyph-utf8/patterns/tex/hyph-grc.tex?view=co
Source0: hyph-grc.tex
Source1: %{name}-LICENSE.txt
URL: https://tug.org/tex-hyphen
License: LPPL
BuildArch: noarch
BuildRequires: hyphen-devel

Requires: hyphen
Supplements: (hyphen and langpacks-grc)
Patch0: hyphen-grc-cleantex.patch

%description
Ancient Greek hyphenation rules.

%prep
%setup -T -q -c -n hyphen-grc
cp -p %{SOURCE0} hyph-grc.tex
%patch 0 -p0 -b .clean
cp %{SOURCE1} ./LICENSE.txt

%build
grep -v "^%" hyph-grc.tex | tr ' ' '\n' > temp.tex
substrings.pl temp.tex temp.dic UTF-8
LANG=el_GR.utf8 uniq temp.dic > hyph_grc_GR.dic
echo "created with substring.pl by substrings.pl hyph-grc.tex hyph_grc_GR.dic UTF-8" > README
echo "---" >> README
head -n 37 hyph-grc.tex >> README

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_grc_GR.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen


%files
%license LICENSE.txt
%doc README
%{_datadir}/hyphen/*

%changelog
* Fri Jul 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20110913-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing unused BR on 'glibc-langpack-el'.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.20110913-14
- Add BR:glibc-langpack-el
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20110913-9
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110913-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110913-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110913-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110913-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110913-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110913-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110913-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110913-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100531-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100531-1
- latest version

* Wed Oct 14 2009 Caolán McNamara <caolanm@redhat.com> - 0.20080616-1
- initial version
