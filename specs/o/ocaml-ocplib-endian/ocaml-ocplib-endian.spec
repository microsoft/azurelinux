# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-ocplib-endian
Version:        1.2
Release:        22%{?dist}
Summary:        Functions to read/write int16/32/64 from strings, bigarrays

License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:            https://github.com/OCamlPro/ocplib-endian
VCS:            git:%{url}.git
Source0:        %{url}/archive/%{version}/ocplib-endian-%{version}.tar.gz
# Remove dependency on base-bytes
Patch0:         https://github.com/OCamlPro/ocplib-endian/pull/26.patch

BuildRequires:  ocaml >= 4.03.0
BuildRequires:  ocaml-cppo >= 1.1.0
BuildRequires:  ocaml-dune >= 1.0

%description
Optimized functions to read and write int16/32/64 from strings,
bytes and bigarrays, based on primitives added in version 4.01.

The library implements three modules:

- EndianString works directly on strings, and provides submodules
  BigEndian and LittleEndian, with their unsafe counterparts;
- EndianBytes works directly on bytes, and provides submodules
  BigEndian and LittleEndian, with their unsafe counterparts;
- EndianBigstring works on bigstrings (Bigarrays of chars),
  and provides submodules BigEndian and LittleEndian, with their
  unsafe counterparts.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use %{name}.

%prep
%autosetup -n ocplib-endian-%{version} -p1

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%license COPYING.txt
%doc README.md CHANGES.md

%files devel -f .ofiles-devel

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 1.2-21
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 1.2-19
- OCaml 5.3.0 rebuild for Fedora 42
- Add VCS field

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.2-17
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.2-16
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2-13
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2-12
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2-11
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2-9
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.2-8
- OCaml 5.0.0 rebuild
- Convert License tag to SPDX
- Use new dune macros

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2-7
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.2-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.2-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Jerry James <loganjerry@gmail.com> - 1.2-1
- Version 1.2
- Build in release mode so that inlining works
- Reenable the tests

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1-7
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jerry James <loganjerry@gmail.com> - 1.1-5
- Move META to the main package
- Drop obsolete workaround for dune bug

* Mon Mar  1 12:17:35 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1-5
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1-2
- OCaml 4.11.0 rebuild

* Wed Aug 19 2020 Jerry James <loganjerry@gmail.com> - 1.1-1
- Version 1.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-10
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-9
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-8
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-7
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-5
- OCaml 4.10.0+beta1 rebuild.

* Sun Jan 12 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.0-4
- OCaml 4.09.0 (final) rebuild.

* Mon Oct 14 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.0-3
- Disable tests on s390x for now.

* Mon Oct 14 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.0-2
- Fix devel package Requires; switch to make_build macro.

* Mon Oct 14 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.0-1
- Initial package.
