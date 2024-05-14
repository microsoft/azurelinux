%global upstream_commit ee22323218150388abdeb36184ad5861e3669b65
%global upstreamid 20110620

Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hyphen-tk
Summary: Turkmen hyphenation rules
Version: 0.%{upstreamid}
Release: 18%{?dist}
Source: https://github.com/hyphenation/tex-hyphen/blob/%{upstream_commit}/hyph-utf8/tex/generic/hyph-utf8/patterns/tex/hyph-tk.tex
URL: https://tug.org/tex-hyphen
License: Public Domain
BuildArch: noarch
BuildRequires: hyphen-devel
Requires: hyphen
Supplements: (hyphen and langpacks-tk)
Patch0: hyphen-tk-cleantex.patch

%description
Turkmen hyphenation rules.

%prep
%setup -T -q -c -n hyphen-tk
cp -p %{SOURCE0} .
%patch 0 -p0 -b .clean

%build
substrings.pl hyph-tk.tex hyph_tk_TM.dic UTF-8
echo "Created with substring.pl by substrings.pl hyph-tk.tex hyph_tk_TM.dic UTF-8" > README
echo "Original in-line credits were:" >> README
echo "" >> README
head -n 15 hyph-tk.tex >> README

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/hyphen
cp -p hyph_tk_TM.dic $RPM_BUILD_ROOT/%{_datadir}/hyphen


%files
%license README
%{_datadir}/hyphen/hyph_tk_TM.dic

%changelog
* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20110620-18
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.20110620-17
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.20110620-9
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.20110620-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110620-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110620-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110620-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110620-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110620-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20110620-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 17 2011 Caolán McNamara <caolanm@redhat.com> - 0.20110620-1
- latest version

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20100531-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jun 01 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100531-1
- latest version

* Sat Apr 03 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100319-1
- latest version

* Tue Mar 16 2010 Caolán McNamara <caolanm@redhat.com> - 0.20100315-1
- initial version
