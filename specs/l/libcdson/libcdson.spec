# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: libcdson
Version: 1.0.0
Release: 10%{?dist}
Summary: Pure C parsing/serialization for the DSON data format, for humans
License: MPL-2.0
URL: https://github.com/frozencemetery/cdson
Source0: https://github.com/frozencemetery/cdson/releases/download/v%{version}/cdson-%{version}.tar.xz

BuildRequires: gcc
BuildRequires: git
BuildRequires: meson

Patch0001: 0001-tests-fix-build-on-legacy-32-bit-machines.patch
Patch0002: 0002-build-version-the-shared-objects.patch

%global desc \
A pure C parsing and serialization library for the DSON data serialization \
format, for humans. cdson is believed to have complete spec coverage, though \
as with any project, there may still be bugs. \
%{nil}
%description %{desc}

%package devel
Summary: Development headers for libcdson
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
%desc

%prep
%autosetup -S git_am -n cdson-%{version}

%build
export CFLAGS="%{build_cflags} -Wno-error=unused-result"
%meson
%meson_build

%check
%meson_test

%install
%meson_install

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/*.so.*

%files devel
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc
%{_libdir}/*.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jan 16 2023 Robbie Harwood <rharwood@redhat.com> - 1.0.0-3
- Packaging changes for Fedora review

* Sat Jan 14 2023 Robbie Harwood <rharwood@redhat.com> - 1.0.0-2
- Add 32-bit support.  In 2023.

* Thu Jun 09 2022 Robbie Harwood <rharwood@redhat.com> - 1.0.0-1
- Initial import to COPR (1.0.0)
