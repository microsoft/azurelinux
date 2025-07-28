Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# for other future directories from http://www.unicode.org/Public
%global unicodedir %{_datadir}/unicode
%global ucddir %{unicodedir}/ucd

Name:           unicode-ucd
Version:        16.0.0
Release:        2%{?dist}
Summary:        Unicode Character Database

# http://www.unicode.org/terms_of_use.html in ReadMe.txt redirects to:
# http://www.unicode.org/copyright.html
# which links to https://www.unicode.org/license.txt
# https://github.com/spdx/license-list-XML/issues/2105
License:        Unicode-3.0
URL:            https://www.unicode.org/ucd/
# update with fbrnch update-version -f
Source0:        https://www.unicode.org/Public/zipped/%{version}/UCD.zip
Source1:        https://www.unicode.org/Public/zipped/%{version}/Unihan.zip
Source2:        https://www.unicode.org/license.txt
BuildArch:      noarch

%description
The Unicode Character Database (UCD) consists of a number of data files listing
Unicode character properties and related data. It also includes data files
containing test data for conformance to several important Unicode algorithms.


%package unihan
Summary:        Unicode Han Database
# for the license and dirs
Requires:       %{name} = %{version}-%{release}

%description unihan
This package contains Unihan.zip which contains the data files for the Unified
Han database of Hanzi/Kanji/Hanja Chinese characters.


%prep
%setup -q -c

grep -q "%{version}" ReadMe.txt || (echo "zip file seems not %{version}" ; exit 1)


%build
%{nil}


%install
mkdir -p %{buildroot}%{ucddir}
cp -ar . %{buildroot}%{ucddir}
cp -p %{SOURCE1} %{buildroot}%{ucddir}
cp %{SOURCE2} .


%files
%license license.txt
%dir %{unicodedir}
%{ucddir}
%exclude %{ucddir}/Unihan.zip

%files unihan
%{ucddir}/Unihan.zip


%changelog
* Thu Jan 16 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 16.0.0-2
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- change the URL and Source0 from http to https
- License verified

* Thu Sep 19 2024 Jens Petersen <petersen@redhat.com> - 16.0.0-1
- update for https://unicode.org/versions/Unicode16.0.0/

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Parag Nemade <pnemade AT redhat DOT com> - 15.1.0-3
- Update the license tag to Unicode-3.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 15.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Sep 16 2023 Jens Petersen <petersen@redhat.com> - 15.1.0-1
- Unicode 15.1 released

* Thu Aug 31 2023 Jens Petersen <petersen@redhat.com> - 15.1.0-0.2
- add license.txt

* Thu Aug 31 2023 Jens Petersen <petersen@redhat.com> - 15.1.0-0.1
- update to draft 15.1.0: https://unicode.org/versions/Unicode15.1.0/
- do not add copyright.html file from website
- add missing Unicode-TOU license tag

* Mon Aug 21 2023 Parag Nemade <pnemade AT fedoraproject DOT org> - 15.0.0-4
- Migrate to SPDX license expression

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Sep 14 2022 Jens Petersen <petersen@redhat.com> - 15.0.0-1
- https://www.unicode.org/versions/Unicode15.0.0/ (#2126234)
- http://blog.unicode.org/2022/09/announcing-unicode-standard-version-150.html

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 14.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 20 2021 Jens Petersen <petersen@redhat.com> - 14.0.0-1
- update to Unicode 14
- https://www.unicode.org/versions/Unicode14.0.0/

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 11 2020 Jens Petersen <petersen@redhat.com> - 13.0.0-1
- update to Unicode 13
- https://www.unicode.org/versions/Unicode13.0.0/

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 12.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 fedora-toolbox <petersen@redhat.com> - 12.1.0-1
- update to Unicode 12.1

* Fri Mar  8 2019 Jens Petersen <petersen@redhat.com> - 12.0.0-1
- update to Unicode 12

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 21 2018 Jens Petersen <petersen@redhat.com> - 11.0.0-1
- update to Unicode 11

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Jens Petersen <petersen@redhat.com> - 10.0.0-1
- update to Unicode 10 (#1463030)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 26 2016 Jens Petersen <petersen@redhat.com> - 9.0.0-2
- add unihan subpackage (#1357769)

* Tue Jun 21 2016 Jens Petersen <petersen@redhat.com> - 9.0.0-1
- update to Unicode 9.0

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Jens Petersen <petersen@redhat.com> - 8.0.0-1
- version 8.0

* Wed Jun 18 2014 Jens Petersen <petersen@redhat.com> - 7.0.0-1
- update to 7.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 24 2014 Jens Petersen <petersen@redhat.com> - 6.3.0-2
- only install one copy of copyright.html
- update to latest 2014 copyright.html from website

* Tue Oct  1 2013 Jens Petersen <petersen@redhat.com>
- add a version check to prevent packaging a version mismatch

* Mon Sep 30 2013 Jens Petersen <petersen@redhat.com> - 6.3.0-1
- update to 6.3

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 24 2012 Jens Petersen <petersen@redhat.com> - 6.2.0-3
- do not use macro in comment

* Wed Oct 24 2012 Jens Petersen <petersen@redhat.com> - 6.2.0-2
- update to latest copyright file from the website

* Wed Sep 26 2012 Jens Petersen <petersen@redhat.com> - 6.2.0-1
- update to Unicode 6.2

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar  2 2012 Jens Petersen <petersen@redhat.com> - 6.1.0-1
- update to Unicode 6.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Jens Petersen <petersen@redhat.com> - 6.0.0-3
- do not duplicate ReadMe.txt in doc files

* Tue Nov 29 2011 Jens Petersen <petersen@redhat.com> - 6.0.0-2
- fix duplicate copyright file (#757290)
- drop superfluous BR on unzip

* Sat Nov 26 2011 Jens Petersen <petersen@redhat.com> - 6.0.0-1
- package Unicode 6.0 UCD
- MIT license
