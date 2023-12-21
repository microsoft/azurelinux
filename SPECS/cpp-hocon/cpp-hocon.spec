## START: Set by rpmautospec
## (rpmautospec version 0.2.5)
%define autorelease(e:s:pb:) %{?-p:0.}%{lua:
    release_number = 16;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{?dist}
## END: Set by rpmautospec

# Makes sure an SONAME bump does not catch us by surprise. Currently, there is
# no ABI stability even across patch releases, and the SONAME comes from the
# complete version number.
%global so_version 0.3.0

%global min_boost 1.54
%global min_cmake 3.2.2

Name:           cpp-hocon
Version:        0.3.0
Release:        17%{?dist}
Summary:        C++ support for the HOCON configuration file format
Vendor:		Microsoft Corporation
Distribution:	Mariner
License:        ASL 2.0
URL:            https://github.com/puppetlabs/cpp-hocon
Source0:        https://github.com/puppetlabs/cpp-hocon/archive/%{version}/cpp-hocon-%{version}.tar.gz

BuildRequires:  cmake >= %{min_cmake}
BuildRequires:  gcc
BuildRequires:  libgcc
BuildRequires:  libstdc++
# Our choice; the make backend would work fine too
BuildRequires:  ninja-build
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  boost-devel >= %{min_boost}
BuildRequires:  leatherman
BuildRequires:  leatherman-devel
BuildRequires:  gettext

# Tests
BuildRequires:  catch1-devel

# Documentation
BuildRequires:  doxygen

# See facter, which has the same workaround.
# autoreq is not picking this one up so be specific
Requires:       leatherman

%description
This is a port of the TypesafeConfig library to C++.

The library provides C++ support for the HOCON configuration file format.


%package devel
Summary:        Development files for the cpp-hocon library
Requires:       cpp-hocon = %{version}-%{release}
Requires:       boost-devel >= %{min_boost}
Requires:       leatherman-devel

%description devel
Libraries and headers to link against cpp-hocon.


%package doc
Summary:        Documentation for the cpp-hocon library

BuildArch:      noarch

%description doc
Documentation for the cpp-hocon library.


%prep
%autosetup

# Do not use the obsolete vendored copy of the Catch unit testing library
# included with leatherman.
sed -r -i 's/(LEATHERMAN_COMPONENTS)(\b.+)?(\bcatch\b)/\1\2/' CMakeLists.txt
sed -r -i 's|\$\{LEATHERMAN_CATCH_INCLUDE\}|"%{_includedir}/catch"|' \
    lib/tests/CMakeLists.txt

%build
mkdir build
pushd build
%cmake .. \
    -DLeatherman_DIR=%{_libdir}/cmake/leatherman \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -GNinja
popd

%ninja_build -C build

%install
cd build
DESTDIR=%{buildroot}/ ninja install


%check
cd build
ninja test

%files
%license LICENSE
%{_libdir}/libcpp-hocon.so.%{so_version}


%files devel
%{_libdir}/libcpp-hocon.so
%{_includedir}/hocon


%files doc
%license LICENSE
%doc CONTRIBUTING.md
%doc README.md


%changelog
* Thu Dec 21 2023 Sindhu Karri <lakarri@microsoft.com> - 0.3.0-17
- Promote package to Mariner Base repo

* Tue Oct 19 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> 0.3.0-16
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified
- Removed building doc pdf not needed.

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-15
- Rename PDF documentation file

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-14
- Drop explicit License on -doc; same as main

* Mon Sep 27 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-13
- Package PDF documentation in lieu of HTML.

* Sun Sep 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-12
- Improve documentation packaging

* Sun Sep 26 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-11
- Reduce macro indirection in the spec file

* Fri Sep 24 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-10
- BR cmake(leatherman) instead of leatherman-devel

* Fri Sep 24 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-9
- Use ninja backend for CMake

* Tue Aug 10 2021 Benjamin A. Beasley <code@musicinmybrain.net> 0.3.0-8
- Rebuild for Boost 1.76 (fix RHBZ#1991863)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> 0.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 09 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-4
- Trivial simplification in the %%build section
- BR catch1-devel, and patch the build system to use it instead of the vendored
  copy in leatherman-devel; this fixes FTBFS due to SIGSTKSZ no longer being a
  preprocessor macro constant in glibc 2.34

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 0.3.0-2
- Rebuilt for Boost 1.75

* Sat Jan  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3.0-1
- Update to 0.3.0 (SONAME bump)
- Drop EPEL7 conditionals in Fedora spec file
- Drop missing header patch, now upstreamed
  (https://github.com/puppetlabs/cpp-hocon/pull/124)

* Sat Jan  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.2-1
- Update to 0.2.2 (SONAME bump)
- Drop patch for upstream commit caab275509826dc5fe5ab2632582abb8f83ea2b3, now
  released

* Sat Jan  9 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.1-7
- Drop downstream pkg-config support (no .pc file)

* Fri Jan  8 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 0.2.1-6
- Use %%{name} macro in several places
- Use %%cmake_* macros consistently
- Add a %%check section to run the tests
- Build HTML documentation with Doxygen, and add a new -doc subpackage
- Add top-level documentation files (README.md etc.)
- Try to add necessary libs to the .pc file, and remove unnecessary -I

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Jonathan Wakely <jwakely@redhat.com> - 0.2.1-4
- Rebuilt for leatherman-1.12.0
- Link tests to libboost_filesystem

* Wed Jun 03 2020 Jonathan Wakely <jwakely@redhat.com> - 0.2.1-3
- Rebuild for Boost 1.73.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 23 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.1.6-7
- Disable tests (fails on x86)

* Thu Feb 15 2018 Filipe Rosset <rosset.filipe@gmail.com> - 0.1.6-6
- fix FTBFS

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Jonathan Wakely <jwakely@redhat.com> - 0.1.6-4
- Rebuilt for Boost 1.66

* Wed Oct 25 2017 James Hogarth <james.hogarth@gmail.com> - 0.1.6-3
- Point to correct location on epel7 for leatherman cmake3 files

* Thu Oct 19 2017 James Hogarth <james.hogarth@gmail.com> - 0.1.6-2
- rebuilt

* Wed Oct 04 2017 James Hogarth <james.hogarth@gmail.com> - 0.1.6-1
- Initial packaging
