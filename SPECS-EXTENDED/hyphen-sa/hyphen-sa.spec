Vendor:         Microsoft Corporation
Distribution:   Mariner
%global upstreamid 20110915

Name: hyphen-sa
Summary: Sanskrit hyphenation rules
Version: 0.%{upstreamid}
Release: 18%{?dist}
#Source0: http://tug.org/svn/texhyphen/trunk/hyph-utf8/tex/generic/hyph-utf8/patterns/tex/hyph-sa.tex?view=co
Source0: hyph-sa.tex
Source1: %{name}-LICENSE.txt
URL: http://tug.org/tex-hyphen
License: LPPL
BuildArch: noarch
BuildRequires: hyphen-devel
Requires: hyphen
Supplements: (hyphen and langpacks-sa)
Patch0: hyphen-sa-cleantex.patch

%description
Sanskrit hyphenation rules.

%prep
%setup -T -q -c -n hyphen-sa
cp -p %{SOURCE0} .
%patch0 -p0 -b .clean
cp %{SOURCE1} ./LICENSE.txt

%build
substrings.pl hyph-sa.tex hyph_sa_IN.dic UTF-8
echo "Created with substring.pl by substrings.pl hyph-sa.tex hyph_sa_IN.dic UTF-8" > README
echo "Original in-line credits were:" >> README
echo "" >> README
head -n 17 hyph-sa.tex >> README

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_sa_IN.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen

%files
%license LICENSE.txt
%doc README
%{_datadir}/hyphen/hyph_sa_IN.dic

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20110915-18
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20110915-10
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110915-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 25 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.20110915-8
- Clean the spec as per current packaging guidelines

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110915-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110915-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110915-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110915-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110915-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110915-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Caolan McNamara <caolanm@redhat.com> - 0.20110915-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100531-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Caolan McNamara <caolanm@redhat.com> - 0.20100531-1
- latest version

* Thu Mar 04 2010 Caolan McNamara <caolanm@redhat.com> - 0.20100304-1
- latest version

* Wed Aug 19 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090412-3
- Related: rhbz#517821 drop hyphen-bn alias

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20090412-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 03 2009 Caolan McNamara <caolanm@redhat.com> - 0.20090412-1
- latest version

* Mon Apr 06 2009 Caolan McNamara <caolanm@redhat.com> - 0.20081010-1
- initial version
