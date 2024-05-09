Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# for other future directories from https://www.unicode.org/Public
%global unicodedir %{_datadir}/unicode
%global ucddir %{unicodedir}/ucd

Name:           unicode-ucd
Version:        13.0.0
Release:        2%{?dist}
Summary:        Unicode Character Database

# https://fedoraproject.org/wiki/Licensing/MIT#Modern_Style_without_sublicense_.28Unicode.29
License:        MIT
URL:            https://www.unicode.org/ucd/
Source0:        https://www.unicode.org/Public/zipped/%{version}/UCD.zip
# https://www.unicode.org/terms_of_use.html referenced in ReadMe.txt redirects to:
# curl https://www.unicode.org/copyright.html | dos2unix > copyright.html
Source1:        https://www.unicode.org/copyright.html
Source2:        https://www.unicode.org/Public/zipped/%{version}/Unihan.zip
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
cp -p %{SOURCE2} %{buildroot}%{ucddir}

cp -p %{SOURCE1} .


%files
%doc copyright.html
%dir %{unicodedir}
%{ucddir}
%exclude %{ucddir}/Unihan.zip

%files unihan
%{ucddir}/Unihan.zip


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 13.0.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
