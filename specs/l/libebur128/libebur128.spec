# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Tests require a "EBU R128 test vector" suite of wav files behind a paywall:
%bcond tests 0

Name:           libebur128
Version:        1.2.6
Release: 15%{?dist}
Summary:        A library that implements the EBU R 128 standard for loudness normalization
License:        MIT
URL:            https://github.com/jiixyj/%{name}

Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  cmake >= 2.8.11
BuildRequires:  make
%if %{with tests}
BuildRequires:  pkgconfig(sndfile)
%endif

%description
A library that implements the EBU R 128 standard for loudness normalization.

It implements M, S and I modes, loudness range measurement (EBU - TECH 3342),
true peak scanning and all sample-rates by recalculation of the filter
coefficients.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup

%build
%cmake -DENABLE_TESTS:BOOL=%{?_with_tests:ON}%{!?_with_tests:OFF} -DCMAKE_POLICY_VERSION_MINIMUM=3.5
%cmake_build

%if %{with tests}
%check
pushd %{_vpath_builddir}/test
make
LD_LIBRARY_PATH=. ./r128-test-library
%endif

%install
%cmake_install

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.1
%{_libdir}/%{name}.so.%{version}

%files devel
%{_includedir}/ebur128.h
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Gwyn Ciesla <gwync@protonmail.com> - 1.2.6-13
- Cmake fix

* Wed Mar 26 2025 Simone Caronni <negativo17@gmail.com> - 1.2.6-12
- Drop ldconfig scriptlets.
- Be more explicit for files.
- Use cmake macros everywhere.
- Small cleanups.
- Trim changelog.
- Adjust tests properly.

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Mar 03 2023 Gwyn Ciesla <gwync@protonmail.com> - 1.2.6-6
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild
