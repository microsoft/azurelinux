# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# rmpbuild parameters:
# --with docs: Build pre-generated documentation.

%global __cmake_in_source_build 1

Name: libipt
Version: 2.1.2
Release: 3%{?dist}
Summary: Intel Processor Trace Decoder Library
License: BSD-3-Clause
URL: https://github.com/intel/libipt
Source0: https://github.com/intel/libipt/archive/v%{version}.tar.gz
Source1: doc-v%{version}.tar.xz
Patch1: libipt-cmake40-compat.patch
# c++ is required only for -DPTUNIT test "ptunit-cpp".
BuildRequires: gcc-c++ cmake
%if 0%{?_with_docs:1}
# pandoc is for -DMAN.
BuildRequires: pandoc
%endif
BuildRequires: make
ExclusiveArch: %{ix86} x86_64

%description
The Intel Processor Trace (Intel PT) Decoder Library is Intel's reference
implementation for decoding Intel PT.  It can be used as a standalone library
or it can be partially or fully integrated into your tool.

%ldconfig_scriptlets 

%package devel
Summary: Header files and libraries for Intel Processor Trace Decoder Library
Requires: %{name}%{?_isa} = %{version}-%{release}
ExclusiveArch: %{ix86} x86_64

%description devel
The %{name}-devel package contains the header files and libraries needed to
develop programs that use the Intel Processor Trace (Intel PT) Decoder Library.

%prep
%setup -q -n libipt-%{version}
%patch -P 1 -p1

%build
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo \
       -DPTUNIT:BOOL=ON \
%if 0%{?_with_docs:1}
       -DMAN:BOOL=ON \
%endif
       -DDEVBUILD:BOOL=ON \
       .
%cmake_build

%install
%cmake_install
%global develdocs howto_libipt.md
(cd doc;cp -p %{develdocs} ..)

# If not building documentation, copy the pre-generated man pages
# to the appropriate place. Otherwise, tar up the generated
# documentation for use in subsequent builds.
%if 0%{?_with_docs:1}
(cd $RPM_BUILD_ROOT%{_mandir}/..; %__tar cJf %{SOURCE1} .)
%else
mkdir -p $RPM_BUILD_ROOT%{_mandir}
(cd $RPM_BUILD_ROOT%{_mandir}/..; %__tar xJf %{SOURCE1})
%endif

%check
ctest -V %{?_smp_mflags}

%files
%doc README
%license LICENSE
%{_libdir}/%{name}.so.*

%files devel
%doc %{develdocs}
%{_includedir}/*
%{_libdir}/%{name}.so
%{_mandir}/*/*.gz

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 22 2025 Kevin Buettner <kevinb@redhat.com> - 2.1.2-2
- Updates for CMake4.0 and use of ninja generator (RHBZ 2380726,
  RHBZ 2381041).

* Tue Jan 21 2025 Keith Seitz keiths@redhat.com> - 2.1.2-1
- Update to 2.1.2.

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Mar  8 2024 Keith Seitz <keiths@redhat.com> - 2.1.1-1
- Update to v2.1.1.

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 18 2023 Keith Seitz <keiths@redhat.com> - 2.1-1
- Update to v2.1.

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Keith Seitz <keiths@redhat.com> - 2.0.6-1
- Import v2.0.6 and regenerate documentation.

* Tue Mar 07 2023 Keith Seitz <keiths@redhat.com>
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 27 2022 Keith Seitz <keiths@redhat.com> - 2.0.5-1
- Import v2.0.5 and regenerate documentation.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 30 2021 Keith Seitz <keiths@redhat.com> - 2.0.4-2
- Add support for pre-generated documenation, allowing removal
  of pandoc dependency. (RHBZ 1943531, Keith Seitz)

* Wed Mar 10 2021 Kevin Buettner <kevinb@redhat.com> - 2.0.4-1
- Release v2.0.4.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 Jeff Law <law@redhat.com> - 2.0.2-2
- Fix uninitialized variable in testsuite

* Tue Aug 04 2020 Keith Seitz <keiths@redhat.com> - 2.0.2-1
- Upgrade to 2.0.2.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 2.0.1-4
- Use __cmake_in_source_build

* Wed Jul 22 2020 Tom Stellard <tstellar@redhat.com> - 2.0.1-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 16 2019 Sergio Durigan Junior <sergiodj@redhat.com> - 2.0.1-1
- Release v2.0.1.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug  8 2018 Sergio Durigan Junior <sergiodj@redhat.com> - 2.0-1
- Release v2.0.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar  5 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-8
- Enable tests (PTUNIT) and man pages (MAN).
- Change BuildRequires: gcc -> gcc-c++ as PTUNIT tests require C++.

* Sat Mar  3 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-7
- Add: BuildRequires: gcc
  https://fedoraproject.org/wiki/Packaging:C_and_C%2B%2B#BuildRequires_and_Requires

* Fri Mar  2 2018 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-6
- Fix v1.6.1-implicit-fallthrough.patch compatibility with gcc < 7.
- Use %%ldconfig_scriptlets.
  https://fedoraproject.org/wiki/Packaging:Scriptlets#Shared_Libraries

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-2
- Fix [-Werror=implicit-fallthrough=] with gcc-7.1.1.

* Fri Jun  9 2017 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.6.1-1
- Rebase to upstream 1.6.1.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Apr 11 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.5-1
- Rebase to upstream 1.5.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.4.4-1
- Rebase to upstream 1.4.4.

* Wed Oct 14 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.4.3-1
- Rebase to upstream 1.4.3.

* Mon Aug 31 2015 Jan Kratochvil <jan.kratochvil@redhat.com> - 1.4.2-1
- Initial Fedora packaging.
