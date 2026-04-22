# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global lcname muparser
%global owner beltoforion
Name:           muParser
Summary:        A fast math parser library
Version:        2.3.5
Release: 4%{?dist}
BuildRequires:  cmake
BuildRequires:  dos2unix
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
License:        MIT
URL:            https://beltoforion.de/en/muparser/
Source0:        https://github.com/%{owner}/%{lcname}/archive/v%{version}/%{lcname}-%{version}.tar.gz


%package devel
Summary:        Development and doc files for %{name}
Requires:       %{name} = %{version}-%{release} pkgconfig

%description
Many applications require the parsing of mathematical expressions.
The main objective of this project is to provide a fast and easy way
of doing this. muParser is an extensible high performance math parser
library. It is based on transforming an expression into a bytecode
and precalculating constant parts of it.

%description devel
Development files and the documentation

%prep
%autosetup -n %{lcname}-%{version}

%build
%cmake .. -DENABLE_SAMPLES=ON -DENABLE_OPENMP=ON -DBUILD_SHARED_LIBS=ON -DCMAKE_POLICY_VERSION_MINIMUM=3.5
# -DENABLE_WIDE_CHAR=ON
%cmake_build

%install
%cmake_install
%ldconfig_scriptlets

%files
%doc CHANGELOG README*
%license LICENSE
%{_libdir}/lib%{lcname}.so.*

%files devel
%{_includedir}/*
%{_libdir}/lib%{lcname}.so
%{_libdir}/pkgconfig/muparser.pc
%{_libdir}/cmake/muparser/*.cmake

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.3.5-2
- Cmake 4 fix

* Fri May 23 2025 Gwyn Ciesla <gwync@protonmail.com> - 2.3.5-1
- 2.3.5

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 07 2023 Christoph Junghans <junghans@lanl.gov> - 2.3.4-1
- Version bump to v2.3.4 (bug #2143538)
- Fix url (bug #2138095)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 01 2022 Filipe Rosset <rosset.filipe@gmail.com> - 2.3.3-2
- rebuilt without WIDE_CHAR support

* Sat Sep 24 2022 Filipe Rosset <rosset.filipe@gmail.com> - 2.3.3-1
- Update to 2.3.3 fixes rhbz#2043980

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Filipe Rosset <rosset.filipe@gmail.com> - 2.3.2-1
- Update to 2.3.2 fixes rhbz#1846718

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Filipe Rosset <rosset.filipe@gmail.com> - 2.2.6-1
- new upstream release 2.2.6

* Tue Nov 20 2018 Filipe Rosset <rosset.filipe@gmail.com> - 2.2.5-8
- rebuilt to fix FTBFS rhbz #1604900 #1316595 and #1448721

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 08 2016 Filipe Rosset <rosset.filipe@gmail.com> - 2.2.5-1
- Rebuilt for new upstream release 2.2.5, fixes rhbz #1316595

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.2.3-7
- Rebuilt for GCC 5 C++11 ABI change

* Thu Feb 26 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/GCC5

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Oct 12 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 2.2.3-3
- Fixed typo in summary of -devel package.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jun 04 2013 Eric Smith <brouhaha@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Mar 09 2012 Eric Smith <eric@brouhaha.com> - 2.2.2-1
- Update to 2.2.2
- Upstream source distribution is now a .zip file
- Upstream version number policy is now that the release version matches
  the .so versioning
- Clean up spec to modern standards (no clean section or BuildRoot tag, etc.)

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-3
- Rebuilt for c++ ABI breakage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 23 2011 Fabian Deutsch <fabiand@fedoraproject.org> - 1.34-1
- Update to 1.34

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.32-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 10 2010 Frank Büttner <frank-buettner@gmx.net> - 1.32-1
- update to 1.32

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Apr 08 2008 Jesse Keating <jkeating@redhat.com> - 1.28-4
- Fix the gcc4.3 errors.

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.28-3
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.28-2
- Rebuild for selinux ppc32 issue.

* Sat Jul 14 2007 Frank Büttner <frank-buettner@gmx.net> - 1.28-1
 - update to 1.28
* Fri Jun 15 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-5%{?dist}
 - fix bug #244309
* Fri Jun 08 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-4%{?dist}
 - fix depend on pkgconfig
* Wed Jun 06 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-3%{?dist}
 - clean build root before run install part
 - fix missing pkconfig file
* Thu May 17 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-2%{?dist}
  - fix missing post -p /sbin/ldconfig
  - fix the double doc files
  - fix missing compiler flags
  - fix wrong file encoding of the doc files
* Wed May 16 2007 Frank Büttner <frank-buettner@gmx.net> - 1.27-1%{?dist}
  - start
