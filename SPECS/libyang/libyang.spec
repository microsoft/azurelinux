# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global run_valgrind_tests ON
# valgrind finds invalid writes in libcmocka on arm and power
# see bug #1699304 for more information
%ifarch %{arm} ppc64le %{ix86}
%global run_valgrind_tests OFF
%endif
# Turn off valgrind unilaterally on all arches which don't have
# valgrind at all, like riscv64.
%ifnarch %{valgrind_arches}
%global run_valgrind_tests OFF
%endif

Name: libyang
Version: 3.12.2
Release: 2%{?dist}
Summary: YANG data modeling language library
Url: https://github.com/CESNET/libyang
Source: %{url}/archive/%{name}-%{version}.tar.gz
License: BSD-3-Clause

# disable tests failing on s390x
Patch1: disable-test_structure.patch

BuildRequires:  cmake
BuildRequires:  doxygen
BuildRequires:  gcc
BuildRequires:  cmake(cmocka) >= 1.0.1
BuildRequires:  make
BuildRequires:  git-core
BuildRequires:  pkgconfig(libpcre2-8) >= 10.21
%ifarch %{valgrind_arches}
BuildRequires:  valgrind
%endif

Conflicts:      %{name} < 1.0.225-3

%package devel
Summary:    Development files for libyang
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   pcre2-devel

%package devel-doc
Summary:    Documentation of libyang API
Requires:   %{name}%{?_isa} = %{version}-%{release}

%package tools
Summary:        YANG validator tools
Requires:       %{name}%{?_isa} = %{version}-%{release}
# This was not properly split out before
Conflicts:      %{name} < 1.0.225-3 

%description devel
Headers of libyang library.

%description devel-doc
Documentation of libyang API.

%description tools
YANG validator tools.

%description
Libyang is YANG data modeling language parser and toolkit
written (and providing API) in C.

%prep
%autosetup -p1 -S git

%build
%cmake \
   -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} \
   -DCMAKE_BUILD_TYPE=RELWITHDEBINFO \
   -DENABLE_LYD_PRIV=ON \
   -DENABLE_VALGRIND_TESTS=%{run_valgrind_tests}
%cmake_build

%cmake_build -t doc

%check
pushd redhat-linux-build
ctest --output-on-failure -V %{?_smp_mflags}
popd

%install
%cmake_install

mkdir -m0755 -p %{buildroot}/%{_docdir}/libyang
cp -a doc/html %{buildroot}/%{_docdir}/libyang/html

%files
%license LICENSE
%{_libdir}/libyang.so.3
%{_libdir}/libyang.so.3.*
%{_datadir}/yang/modules/libyang/*.yang
%dir %{_datadir}/yang/
%dir %{_datadir}/yang/modules/
%dir %{_datadir}/yang/modules/libyang/

%files tools
%{_bindir}/yanglint
%{_bindir}/yangre
%{_datadir}/man/man1/yanglint.1.gz
%{_datadir}/man/man1/yangre.1.gz

%files devel
%{_libdir}/libyang.so
%{_libdir}/pkgconfig/libyang.pc
%{_includedir}/libyang/*.h
%dir %{_includedir}/libyang/

%files devel-doc
%{_docdir}/libyang

%changelog
* Wed Jul 30 2025 Michal Ruprich <mruprich@redhat.com> - 3.12.2-2
- Opting-out from the default ninja build due to docs

* Mon Jul 28 2025 Michal Ruprich <mruprich@redhat.com> - 3.12.2-1
- New version 3.12.2

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 30 2025 Michal Ruprich <mruprich@redhat.com> - 3.7.8-1
- New version 3.7.8

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.148-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.148-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Apr 03 2024 Tomas Korbar <tkorbar@redhat.com> - 2.1.148-1
- Rebase to version 2.1.148
- Resolves: rhbz#2232832

* Sat Mar 02 2024 David Abdurachmanov <davidlt@rivosinc.com> - 2.1.80-5
- Properly check valgrind arches

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.80-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 23 2023 Tomas Korbar <tkorbar@redhat.com> - 2.1.80-1
- Rebase to version 2.1.80
- Resolves: rhbz#2209212

* Sun Mar 19 2023 Tomas Korbar <tkorbar@redhat.com> - 2.1.55-1
- Rebase to version 2.1.55
- Resolves: rhbz#2179481

* Fri Mar 10 2023 Tomas Korbar <tkorbar@redhat.com> - 2.1.30-2
- Change the License tag to the SPDX format

* Thu Jan 19 2023 Tomas Korbar <tkorbar@redhat.com> - 2.1.30-1
- Rebase to version 2.1.30
- Resolves: rhbz#2162362

* Wed Nov 09 2022 Jakub Ružička <jakub.ruzicka@nic.cz> - 2.1.4-1
- Rebase to version 2.1.4 (Resolves: rhbz#2141228)
- Add patch to disable tests failing on s390x

* Mon Aug 01 2022 Tomas Korbar <tkorbar@redhat.com> - 2.0.231-2
- Clean specfile and remove obsolete tag that is not relevant

* Wed Jul 27 2022 Jakub Ružička <jakub.ruzicka@nic.cz> - 2.0.231-1
- Rebase to version 2.0.231 (Resolves: rhbz#2111304)
- Own yang modules (Resolves: rhbz#2094371)
- Use proper CMAKE_BUILD_TYPE

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.194-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon May 09 2022 Tomas Korbar <tkorbar@redhat.com> - 2.0.194-1
- Rebase to version 2.0.194
- Resolves: rhbz#2082735

* Tue Mar 15 2022 Jakub Ružička <jakub.ruzicka@nic.cz> - 2.0.164-1
- Rebase to version 2.0.164

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.112-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Tomas Korbar <tkorbar@redhat.com> - 2.0.112-2
- Fix building of libyang 2 on fedora 34

* Tue Nov 30 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.112-1
- Rebase to version 2.0.112
- Resolves: rhbz#2022586

* Mon Oct 11 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.97-1
- Rebase to version 2.0.97
- Resolves: rhbz#2012348

* Thu Sep 30 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.88-1
- Rebase to version 2.0.88
- Resolves: rhbz#2007673

* Fri Aug 06 2021 Tomas Korbar <tkorbar@redhat.com> - 2.0.7-1
- Rebase to version 2.0.7
- Resolves: rhbz#1959645

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.225-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Neal Gompa <ngompa@datto.com> - 1.0.225-3
- Clean up the spec file for legibility and modern spec standards
- Split out tools into their own subpackage
- Remove archfulness from the build path to fix documentation build

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.225-2
- Rebuilt for Python 3.10

* Tue Mar 09 2021 Tomas Korbar <tkorbar@redhat.com> - 1.0.225-1
- Rebase to version 1.0.225
- Resolves: rhbz#1936718

* Wed Feb 03 2021 Tomas Korbar <tkorbar@redhat.com> - 1.0.215-1
- Rebase to version 1.0.215
- Resolves: rhbz#1921779

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.184-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Sep 02 2020 Merlin Mathesius <mmathesi@redhat.com> - 1.0.184-3
- Fix FTBFS by disabling valgrind on power since it finds bogus invalid
  writes in libcmocka

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.184-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.184-1
- Update to 1.0.184
- Fix build

* Fri Jun 19 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.176-1
- Update to 1.0.176

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.167-2
- Rebuilt for Python 3.9

* Mon May 18 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.167-1
- Update to 1.0.167

* Fri Feb 07 2020 Tomas Korbar <tkorbar@redhat.com> - 1.0.130-1
- Rebase to version 1.0.130 (#1797495)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.101-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 09 2019 Tomas Korbar <tkorbar@redhat.com> - 1.0.101-1
- Rebase to version 1.0.101
- Fix CVE-2019-19333 (#1780495)
- Fix CVE-2019-19334 (#1780494)

* Fri Oct 25 2019 Tomas Korbar <tkorbar@redhat.com> - 1.0.73-1
- Rebase to version 1.0.73 (#1758512)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.105-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.105-3
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Initial import (#1699846).

* Fri Apr 26 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Change specfile accordingly to mosvald's review
- Remove obsolete ldconfig scriptlets
- libyang-devel-doc changed to noarch package
- Add python_provide macro to python3-libyang subpackage
- Remove obsolete Requires from libyang-cpp-devel
- Start using cmake with smp_mflags macro

* Wed Apr 03 2019 Tomas Korbar <tkorbar@redhat.com> - 0.16.105-1
- Initial commit of package after editation of specfile
