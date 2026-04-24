# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global libjit_soversion 3
Name:           jitterentropy
Version:        3.6.0
Release: 4%{?dist}
Summary:        Library implementing the jitter entropy source

License:        BSD-3-Clause OR GPL-2.0-only
URL:            https://github.com/smuellerDD/jitterentropy-library
Source0:        %{url}/archive/v%{version}/%{name}-library-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: make

# Disable Upstream Makefiles debuginfo strip on install
Patch0: jitterentropy-rh-makefile.patch

%description
Library implementing the CPU jitter entropy source

%package devel
Summary: Development headers for jitterentropy library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development headers and libraries for jitterentropy

%prep
%autosetup -p0 -n %{name}-library-%{version}

%build
%set_build_flags
%make_build

%install
mkdir -p %{buildroot}/usr/include/
%make_install PREFIX=/usr LIBDIR=%{_lib}

%files
%doc README.md CHANGES.md
%license LICENSE LICENSE.bsd LICENSE.gplv2
%{_libdir}/libjitterentropy.so.%{libjit_soversion}*

%files devel
%{_includedir}/*
%{_libdir}/libjitterentropy.so
%{_mandir}/man3/*

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 25 2024 Vladis Dronov <vdronov@redhat.com> - 3.6.0-1
- Update to the upstream v3.6.0 @ 11829386

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 31 2024 Vladis Dronov <vdronov@redhat.com> - 3.5.0-3
- Update to the upstream v3.5.0 @ 48b2ffc1

* Wed Feb 07 2024 Vladis Dronov <vdronov@redhat.com> - 3.5.0-1
- Update to the upstream v3.5.0 @ 54cbe828
- Use proper SPDX license identifiers

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 27 2022 Vladis Dronov <vdronov@redhat.com> - 3.4.1-3
- Update to the upstream v3.4.1 @ 7bf9f85d
- Fix a stack corruption on s390x

* Tue Sep 06 2022 Vladis Dronov <vdronov@redhat.com> - 3.4.1-1
- Update to the upstream v3.4.1 @ 4544e113

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Mar 24 2022 Vladis Dronov <vdronov@redhat.com> - 3.4.0-2
- Update to the upstream v3.4.0 @ 2e5019cf

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 16 2021 Vladis Dronov <vdronov@redhat.com> - 3.3.1-1
- Update to the upstream v3.3.1

* Thu Sep 16 2021 Vladis Dronov <vdronov@redhat.com> - 3.3.0-1
- Update to the upstream v3.3.0
- Add small fixes which have missed the v3.3.0 release
  https://github.com/smuellerDD/jitterentropy-library/pull/71

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-3.git.409828cf
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Vladis Dronov <vdronov@redhat.com> - 3.0.2-2.git.409828cf
- Update to the latest upstream commits upto 409828cf
- Add clock_gettime() software time source
- Add a code for choosing between software and hardware time sources
  https://github.com/smuellerDD/jitterentropy-library/pull/57
  https://bugzilla.redhat.com/show_bug.cgi?id=1974132

* Tue Jul 06 2021 Vladis Dronov <vdronov@redhat.com> - 3.0.2.git.d18d5863-1
- Update to the upstream v3.0.2 + tip of origin/master
  with fixes for an important issue:
  https://github.com/nhorman/rng-tools/pull/123
  https://github.com/smuellerDD/jitterentropy-library/issues/37
- Add important upstream fixes for the one CPU case (bz 1974132)

* Fri Jun 18 2021 Vladis Dronov <vdronov@redhat.com> - 3.0.2-1
- Update to the upstream v3.0.2
- Remove ldconfig_scriptlets

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 26 2019 Neil Horman <nhorman@redhat.com> - 2.2.0-1
- Update to latest upstream

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Sep 21 2018 Neil Horman <nhorman@tuxdriver.com> - 2.1.2-3
- Drop static library
- Fix up naming
- Add gcc buildrequires
- Fix files glob

* Thu Sep 13 2018 Neil Horman <nhorman@tuxdriver.com> - 2.1.2-2
- Fixed license
- Fixed up some macro usage in spec file
- Documented patches
- Modified makefile to use $(INSTALL) macro

* Thu Sep 06 2018 Neil Horman <nhorman@tuxdriver.com> - 2.1.2-1
- Initial import
