Summary:        Scripts for converting XML to roff or HTML
Name:           xmltoman
Version:        0.4
Release:        23%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://sourceforge.net/projects/xmltoman/
Source0:        https://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Patch0:         xmltoman-0.3-timestamps.patch
BuildRequires:  perl-generators
BuildRequires:  perl(XML::Parser)
BuildArch:      noarch

%description
This package provides xmltoman and xmlmantohtml scripts, to compile
the xml representation of manual page to either roff source, or HTML
(while providing the CSS stylesheet for eye-candy look). XSL stylesheet
for doing rougly the same job is provided.

%prep
%setup -q
%patch0 -p1 -b .timestamps

%build
%make_build PREFIX=%{_prefix}

%install
%make_install PREFIX=%{_prefix}
mkdir -p %{buildroot}%{_mandir}/man1
cp -p *.1 %{buildroot}%{_mandir}/man1

%files
%license COPYING
%{_bindir}/xmltoman
%{_bindir}/xmlmantohtml
%{_datadir}/xmltoman
%{_mandir}/*/*
%doc README

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.4-23
- License verified
- Lint spec
- Specify prefix dir

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.4-22
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 24 2013 Lubomir Rintel <lkundrak@v3.sk> - 0.4-11
- Bulk sad and useless attempt at consistent SPEC file formatting

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 24 2013 Petr Pisar <ppisar@redhat.com> - 0.4-9
- Perl 5.18 rebuild

* Thu Mar 21 2013 Ondrej Vasik <ovasik@redhat.com>
- Ship manpages

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu May 29 2008 Lubomir Rintel <lkundrak@v3.sk> - 0.4-1
- New upstream release

* Wed Mar 12 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.3-2
- Preserve timestamps, sanitize requires (thanks to Parag AN)

* Sun Mar 09 2008 Lubomir Kundrak <lkundrak@redhat.com> - 0.3-1
- Initial packaging attempt
