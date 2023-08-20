Summary:        URI parsing library - RFC 3986
Name:           uriparser
Version:        0.9.7
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://uriparser.github.io/
Source0:        https://github.com/%{name}/%{name}/releases/download/%{name}-%{version}/%{name}-%{version}.tar.bz2
BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  graphviz
BuildRequires:  gtest-devel
BuildRequires:  make

%description
Uriparser is a strictly RFC 3986 compliant URI parsing library written
in C. uriparser is cross-platform, fast, supports Unicode and is
licensed under the New BSD license.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary:        HTML documentation for %{name}
BuildArch:      noarch

%description doc
The %{name}-doc package contains HTML documentation files for %{name}.

%prep
%autosetup -p1

# Remove qhelpgenerator dependency by commenting Doxygen.in:
sed -i 's/GENERATE_QHP\ =\ yes/GENERATE_QHP\ =\ no/g' doc/Doxyfile.in


%build
# Native build
%cmake
%cmake_build


%install
%cmake_install


%check
%ctest


%files
%doc THANKS AUTHORS ChangeLog
%license COPYING
%{_bindir}/uriparse
%{_libdir}/lib%{name}.so.1*
%{_libdir}/cmake/%{name}-%{version}/

%files devel
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%files doc
%license COPYING
%doc %{_docdir}/%{name}/html

%changelog
* Wed Aug 16 2023 Archana Choudhary <archana1@microsoft.com> - 0.9.7-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

* Fri Oct 07 2022 Sandro Mani <manisandro@gmail.com> - 0.9.7-1
- Update to 0.9.7

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 0.9.6-5
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 0.9.6-4
- Make mingw subpackages noarch

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 0.9.6-1
- Add mingw subpackages

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Sandro Mani <manisandro@gmail.com> - 0.9.6-1
- Update to 0.9.6

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 24 2021 Sandro Mani <manisandro@gmail.com> - 0.9.5-1
- Update to 0.9.5

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 31 2020 Sandro Mani <manisandro@gmail.com> - 0.9.4-1
- Update to 0.9.4

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 29 2019 Sandro Mani <manisandro@gmail.com> - 0.9.3-1
- Update to 0.9.3

* Tue Apr 23 2019 Sandro Mani <manisandro@gmail.com> - 0.9.2-1
- Update to 0.9.2

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 07 2019 Sandro Mani <manisandro@gmail.com> - 0.9.1-1
- Update to 0.9.1

* Sat Oct 27 2018 Sandro Mani <manisandro@gmail.com> - 0.9.0-1
- Update to 0.9.0

* Mon Aug 20 2018 Sandro Mani <manisandro@gmail.com> - 0.8.6-1
- Update to 0.8.6

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar 07 2018 Sandro Mani <manisandro@gmail.com> - 0.8.5-2
- BR: gcc-c++

* Wed Feb 07 2018 Sandro Mani <manisandro@gmail.com> - 0.8.5-1
- Update to 0.8.5

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue May 10 2016 Sandro Mani <manisandro@gmail.com> - 0.8.4-3
- Drop unused requires on cpptest
- Modernize spec

* Sun Mar 27 2016 François Cami <fcami@fedoraproject.org> - 0.8.4-2
- Add -doc subpackage.

* Wed Mar 02 2016 François Cami <fcami@fedoraproject.org> - 0.8.4-1
- Update to latest upstream.

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Jul 12 2015 François Cami <fcami@fedoraproject.org> - 0.8.2-1
- Update to latest upstream.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 29 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.8.1-4
- Modernise spec

* Wed Jan 28 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.8.1-3
- Make uriCompareRangeA() return -1/0/1 like tests assume it does
  so package will build on aarch64.

* Fri Jan 09 2015 François Cami <fcami@fedoraproject.org> - 0.8.1-2
- Use PIC.

* Mon Jan 05 2015 François Cami <fcami@fedoraproject.org> - 0.8.1-1
- Update to latest upstream.

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Sep 06 2013 François Cami <fcami@fedoraproject.org> - 0.8.0-1
- Update to latest upstream.

* Fri Sep 06 2013 François Cami <fcami@fedoraproject.org> - 0.7.9-1
- Update to latest upstream.

* Tue Aug 06 2013 François Cami <fcami@fedoraproject.org> - 0.7.8-2
- Fix FTBS due to https://fedoraproject.org/wiki/Changes/UnversionedDocdirs

* Tue Jul 30 2013 François Cami <fcami@fedoraproject.org> - 0.7.8-1
- Update to 0.7.8

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 07 2010 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.5-3
- Fixed FTBFS

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Mar 06 2009 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.5-1
- Upgrade to 0.7.5:
-  Improved docs
-  Test suite
- 0.7.4
-  Cleaned up code and fixed memory leaks
- 0.7.3
-  Builds for Cygwin, minor bug fix
-  Changes in build system.
-  Added: Qt Assistant documentation output
- 0.7.2
-  Improved and cleaned API

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Sep 06 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-6
- changed document file handling in spec, used better method - %%doc

* Fri Sep 05 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-5
- fixed group, removed redundant args for %%setup
- included ChangeLog, fixed html folder path in %%files
- fixed automated autotool calls

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-4
- changed name according to naming guidelines

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-3
- fixed buildrequires tag

* Sun Aug 10 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-2
- added documentation

* Sat Aug 9 2008 Rakesh Pandit <rakesh@fedoraproject.org> 0.7.1-1
- Initial build
