# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          iniparser
Version:       4.2.6
Release: 4%{?dist}
Summary:       C library for parsing "INI-style" files

License:       MIT
URL:           https://gitlab.com/%{name}/%{name}
Source0:       https://gitlab.com/%{name}/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.gz

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: cmake
BuildRequires: doxygen

%description
iniParser is an ANSI C library to parse "INI-style" files, often used to
hold application configuration information.

%package devel
Summary:       Header files, libraries and development documentation for %{name}
Requires:      %{name} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for %{name}. If you like to develop programs using %{name},
you will need to install %{name}-devel.

%prep
%autosetup -n %{name}-v%{version}

%build
%cmake -DBUILD_TESTS=ON -DBUILD_EXAMPLES=ON
%cmake_build

%install
%cmake_install
rm -rf %{buildroot}%{_bindir}/testrun
rm -rf %{buildroot}%{_bindir}/ressources
rm -rf %{buildroot}%{_docdir}/%{name}/examples

%check
%ctest
%{_vpath_builddir}/iniexample
%{_vpath_builddir}/parse test/ressources/good_ini/twisted.ini

%ldconfig_scriptlets

%files
%doc AUTHORS FAQ*md INSTALL README.md
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/libiniparser.so.*

%files devel
%{_libdir}/libiniparser.a
%{_libdir}/libiniparser.so
%{_includedir}/%{name}
%{_libdir}/cmake/%{name}
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Aug 05 2025 David Cantrell <dcantrell@redhat.com> - 4.2.6-3
- Merge the 'static' package in to the 'devel' package (#2375287)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 18 2025 David Cantrell <dcantrell@redhat.com> - 4.2.6-1
- Upgrade to iniparser-4.2.6 (#2345965)
- Upstream moved to gitlab.com

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 David Cantrell <dcantrell@redhat.com> - 4.2.5-1
- Upgrade to iniparser-4.2.5 (#2335945)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 David Cantrell <dcantrell@redhat.com> - 4.2.4-1
- Upgrade to iniparser-4.2.4 (#2292511)

* Tue May 28 2024 David Cantrell <dcantrell@redhat.com> - 4.2.2-1
- Upgrade to iniparser-4.2.2 (#2277613)
- Switch to building with cmake (include in a subpackage)
- Enable static library in addition to shared library
- De-conditionalize the test suite and run that via %%check
- Build and include the API documentation in the devel package

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 David Cantrell <dcantrell@redhat.com> - 4.1-14
- Minor spec file updates
- Verify the License tag carries an SPDX expression

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 David Cantrell <dcantrell@redhat.com> - 4.1-12
- Fix for CVE-2023-33461 (BZ#2211622)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Nov  8 2018 Robin Lee <cheeselee@fedoraproject.org> - 4.1-2
- Add symlinks for headers to be compitable with Debian (BZ#1635706)

* Fri Aug 31 2018 Robin Lee <cheeselee@fedoraproject.org> - 4.1-1
- Update to 4.1 (BZ#1508863)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-6.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-5.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-4.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-2.20160821git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Aug 21 2016 Jaromír Cápík <jaromir.capik@email.cz> - 4.0-1.20160821git
- Update to 4.0 [git e24843b] (#1346451)
- Spec file maintenance

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jan 10 2014 - Andreas Schneider <asn@redhat.com> - 3.1-4
- resolves: #1031119 - Fix possible crash with crafted ini files.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug 10 2012 Jaromir Capik <jcapik@redhat.com> - 3.1-1
- Update to 3.1
- Minor spec file changes according to the latest guidelines

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Simo Sorce <ssorce@redhat.com> - 3.0-1
- Final 3.0 release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.4.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.3.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0-0.2.b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jan 26 2009 Alex Hudson <fedora@alexhudson.com> - 3.0-0.1.b
- change version number to reflect "pre-release" status

* Mon Jan 19 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-3
- ensure LICENSE file is installed

* Wed Jan 14 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-2
- respond to review: added -fPIC to cflags, used 'install'

* Tue Jan 13 2009 Alex Hudson <fedora@alexhudson.com> - 3.0b-1
- Initial packaging attempt
