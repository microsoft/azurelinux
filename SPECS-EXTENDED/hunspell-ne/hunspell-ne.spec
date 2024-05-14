Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name: hunspell-ne
Summary: Nepali hunspell dictionaries
Version: 20080425
Release: 22%{?dist}
# Upstream Source and URL is down now, please don't report FTBFS bugs
Source0: https://nepalinux.org/downloads/ne_NP_dict.zip
Source1: %{name}-LICENSE.txt
URL: https://nepalinux.org/downloads
# License is given in README_ne_NP.txt file
License: LGPLv2
BuildArch: noarch

Requires: hunspell
Supplements: (hunspell and langpacks-ne)

%description
Nepali hunspell dictionaries.

%prep
%autosetup -c -n ne_NP_dict
sed -i 's|चलन/चल्ती/15,22|चलनचल्ती/15,22|g' ne_NP.dic
sed -i 's|निजामती/I15,22|निजामती/15,22|g' ne_NP.dic

# Remove ^M and trailing whitespace characters
sed -i 's/\r//;s/[ \t]*$//' ne_NP.dic

cp %{SOURCE1} ./LICENSE.txt

%build

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/myspell
cp -p *.dic *.aff $RPM_BUILD_ROOT/%{_datadir}/myspell

pushd $RPM_BUILD_ROOT/%{_datadir}/myspell/
ne_NP_aliases="ne_IN"
for lang in $ne_NP_aliases; do
        ln -s ne_NP.aff $lang.aff
        ln -s ne_NP.dic $lang.dic
done
popd

%files
%license LICENSE.txt
%doc README_ne_NP.txt 
%{_datadir}/myspell/*

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20080425-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jul 01 2018 Parag Nemade <pnemade AT fedoraproject DOT org> - 20080425-17
- Add comment that Source and URL links are dead now

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 19 2016 Parag Nemade <pnemade AT redhat DOT com> - 20080425-13
- Add Supplements: tag for langpacks naming guidelines
- Clean the specfile to follow current packaging guidelines

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 20080425-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080425-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080425-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080425-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Parag <pnemade AT redhat DOT com> - 20080425-8
- Removed BR:dos2unix and instead use sed (rh# 967638)

* Tue May 28 2013 Parag <pnemade AT redhat DOT com> - 20080425-7
- Resolves:rh#959987: Error message: “0 is wrong flag id” occurs when using hunspell-ne
- Resolves:rh#967638: ne_NP.dic contains both CRLF and LF line terminators

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080425-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080425-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Parag <pnemade AT redhat DOT com> - 20080425-4
- spec cleanup

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080425-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20080425-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 11 2009 Parag <pnemade@redhat.com> - 20080425-1
- Update to next upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20061217-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 20061217-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Parag <pnemade@redhat.com> - 20061217-3
- Resolves:rh#475982 - Perhaps hunspell-ne suffices for ne_IN as well as ne_NP 

* Mon Jan 21 2008 Parag <pnemade@redhat.com> - 20061217-2
- Corrected License tag.

* Thu Jan 03 2008 Parag <pnemade@redhat.com> - 20061217-1
- Initial Fedora release
