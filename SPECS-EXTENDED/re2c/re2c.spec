Summary: 	Tool for generating C, C++, and go recognizers from regular expressions
Name: 		re2c
Version: 	3.1
Release: 	4%{?dist}
License: 	Public Domain
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL: 		https://re2c.org/
Source: 	https://github.com/skvadrik/re2c/releases/download/%{version}/%{name}-%{version}.tar.xz

BuildRequires: 	gcc
BuildRequires: 	gcc-c++
BuildRequires: 	make
BuildRequires: 	python3

%description
re2c is a tool for writing very fast and very flexible scanners. Unlike any
other such tool, re2c focuses on generating high efficient code for regular
expression matching. As a result this allows a much broader range of use than
any traditional lexer offers. And Last but not least re2c generates warning
free code that is equal to hand-written code in terms of size, speed and
quality.

%prep
%setup -q

%build
%configure --disable-silent-rules
%make_build

%install
%make_install

%check
make tests

%files
%license LICENSE
%doc CHANGELOG README.md examples/ doc/*
%{_bindir}/re2c
%{_bindir}/re2go
%{_bindir}/re2rust
%{_datadir}/re2c/
%{_mandir}/man1/re2c.1*
%{_mandir}/man1/re2go.1*
%{_mandir}/man1/re2rust.1*

%changelog
* Thu Dec 19 2024 Akhila Guruju <v-guakhila@microsoft.com> - 3.1-4
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 26 2024 Orion Poplawski <orion@nwra.com> - 3.1-1
- Update to 3.1

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 13 2021 Kyle Lexmond <fedora@kyl191.net> - 2.1.1-1
- Update to 2.1.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep  9 21:15:59 MDT 2020 Orion Poplawski <orion@nwra.com> - 2.0.3-1
- Update to 2.0.3

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 7 2018 Orion Poplawski <orion@nwra.com> - 1.1.1-1
- Update to 1.1.1 (bugz #1607177, 1606091)
- Run tests

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Apr 13 2016 Ben Boeckel <mathstuf@gmail.com> - 0.16-1
- update to 0.16
- replace %%{__foo} usage

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 06 2015 Ben Boeckel <mathstuf@gmail.com> - 0.14.3-1
- update to 0.14.3
- clean out old and unnecessary bits

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.13.5-10
- Rebuilt for GCC 5 C++11 ABI change

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-4
- Rebuilt for c++ ABI breakage

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 12 2010 Matthias Saou <http://freshrpms.net/> 0.13.5-1
- Update to 0.13.5.
- Update URL to the one used in the included spec file.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.12.3-2
- Autorebuild for GCC 4.3

* Thu Sep 13 2007 Matthias Saou <http://freshrpms.net/> 0.12.3-1
- Update to 0.12.3.

* Thu Aug 23 2007 Matthias Saou <http://freshrpms.net/> 0.12.2-1
- Update to 0.12.2.
- Update URL location.

* Wed Jun 20 2007 Matthias Saou <http://freshrpms.net/> 0.12.1-2
- Fix license tag to "Public Domain".
- Update description with most recent text from the website.

* Wed Jun 20 2007 Matthias Saou <http://freshrpms.net/> 0.12.1-1
- Spec file changes.

* Wed May 23 2007 Dag Wieers <dag@wieers.com> - 0.12.1-1
- Updated to release 0.12.1.

* Thu May 03 2007 Dag Wieers <dag@wieers.com> - 0.12.0-1
- Initial version.

