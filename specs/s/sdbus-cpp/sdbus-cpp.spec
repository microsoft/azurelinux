# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libso_major 2

Name:           sdbus-cpp
Version:        2.1.0
Release: 4%{?dist}
Summary:        High-level C++ D-Bus library

License:        LGPL-2.1-only
URL:            https://github.com/Kistler-Group/sdbus-cpp
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake >= 3.14
BuildRequires:  gcc-c++
BuildRequires:  pkgconfig(libsystemd) >= 238
BuildRequires:  pkgconfig(gmock) >= 1.10.0

# temporary bundle sdbus-cpp-1 to allow dnf5 rebuild
BuildRequires: sdbus-cpp

%description
High-level C++ D-Bus library for Linux designed to provide easy-to-use
yet powerful API in modern C++


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for %{name}.


%package devel-doc
Summary:        Developer documentation for %{name}
BuildArch:      noarch
BuildRequires:  doxygen

%description devel-doc
Developer documentation for %{name}


%package tools
Summary:        Stub code generator for sdbus-c++
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildRequires:  pkgconfig(expat)
Obsoletes:      %{name}-xml2cpp < %{version}-%{release}

%description tools
The stub code generator for generating the adapter and proxy interfaces
out of the D-Bus IDL XML description.


%package tests
Summary:        Tests for %{name}
Requires:       %{name}

%description tests
%{summary}


%prep
%autosetup -p1


%build
%cmake \
    -DCMAKE_BUILD_TYPE=Release \
    -DSDBUSCPP_BUILD_CODEGEN=ON \
    -DSDBUSCPP_BUILD_DOCS=ON \
    -DSDBUSCPP_BUILD_DOXYGEN_DOCS=ON \
    -DSDBUSCPP_BUILD_TESTS=ON \
    -DSDBUSCPP_TESTS_INSTALL_PATH=%{_libexecdir}/installed-tests/
%cmake_build
%cmake_build --target doc


%check
%ctest -E "sdbus-c\+\+-integration-tests"


%install
%cmake_install
mkdir -p %{buildroot}%{_datadir}/dbus-1/system.d/
mv %{buildroot}%{_sysconfdir}/dbus-1/system.d/org.sdbuscpp.integrationtests.conf %{buildroot}%{_datadir}/dbus-1/system.d/
rm -rf %{buildroot}%{_sysconfdir}

# temporary bundle sdbus-cpp-1 to allow dnf5 rebuild
cp %{_libdir}/libsdbus-c++.so.1.* %{buildroot}%{_libdir}


%files
%license %{_docdir}/sdbus-c++/COPYING
%dir %{_docdir}/sdbus-c++
%doc %{_docdir}/sdbus-c++/AUTHORS
%doc %{_docdir}/sdbus-c++/ChangeLog
%doc %{_docdir}/sdbus-c++/NEWS
%doc %{_docdir}/sdbus-c++/README.md
%{_libdir}/libsdbus-c++.so.%{libso_major}{,.*}

# temporary bundle sdbus-cpp-1 to allow dnf5 rebuild
%{_libdir}/libsdbus-c++.so.1{,.*}


%files devel
%{_libdir}/pkgconfig/sdbus-c++.pc
%{_libdir}/pkgconfig/sdbus-c++-tools.pc
%{_libdir}/libsdbus-c++.so
%{_includedir}/sdbus-c++/
%dir %{_libdir}/cmake/sdbus-c++
%{_libdir}/cmake/sdbus-c++/*.cmake


%files devel-doc
%dir %{_docdir}/sdbus-c++
%doc %{_docdir}/sdbus-c++/*


%files tools
%{_bindir}/sdbus-c++-xml2cpp
%dir %{_libdir}/cmake/sdbus-c++-tools
%{_libdir}/cmake/sdbus-c++-tools/*.cmake


%files tests
%{_datadir}/dbus-1/system.d/org.sdbuscpp.integrationtests.conf
%{_libexecdir}/installed-tests/sdbus*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Apr 11 2025 Marek Blaha <mblaha@redhat.com> - 2.1.0-2
- Temoporarily bundle libsdbus-c++.so.1

* Fri Apr 04 2025 Jonathan Wright <jonathan@almalinux.org> - 2.1.0-1
- update to 2.1.0 rhbz#2277126
- include actual readme rhbz#2268443

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 12 2024 Marek Blaha <mblaha@redhat.com> - 1.5.0-2
- Invoke unit tests after the build

* Mon Feb 26 2024 Marek Blaha <mblaha@redhat.com> - 1.5.0-1
- Update to release 1.5.0

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 11 2023 Marek Blaha <mblaha@redhat.com> - 1.4.0-1
- Update to release 1.4.0

* Tue Sep 12 2023 Neal Gompa <ngompa@fedoraproject.org> - 1.3.0-2
- Move sdbus-c++ CMake module to devel package

* Mon Aug 21 2023 Marek Blaha <mblaha@redhat.com> - 1.3.0-1
- Update to release 1.3.0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Mar 30 2023 Marek Blaha <mblaha@redhat.com> - 1.2.0-3
- migrated to SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 10 2022 Marek Blaha <mblaha@redhat.com> - 1.2.0-1
- Update to release 1.2.0

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Marek Blaha <mblaha@redhat.com> - 1.1.0-1
- Update to release 1.1.0

* Tue Oct 26 2021 Marek Blaha <mblaha@redhat.com> - 1.0.0-1
- Update to release 1.0.0
- Change source tarball name to <name>-<version>.tar.gz

* Tue Oct 19 2021 Marek Blaha <mblaha@redhat.com> - 0.9.0-1
- Update to release 0.9.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Marek Blaha <mblaha@redhat.com> - 0.8.3-1
- Update to release 0.8.3

* Tue Oct 06 2020 Marek Blaha <mblaha@redhat.com> - 0.8.1-5
- Switch from make_build to cmake_build

* Tue Sep 22 2020 Jeff Law <law@redhat.com> - 0.8.1-4
- Use cmake_in_source_build to fix FTBFS due to recent cmake macro changes

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Feb 7 2020 Marek Blaha <mblaha@redhat.com> - 0.8.1-1
- Update to release 0.8.1

* Fri Jan 24 2020 Marek Blaha <mblaha@redhat.com> - 0.7.8-1
- Initial release 0.7.8
