# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global giturl  https://github.com/ocurrent/ocaml-version

Name:           ocaml-version
Version:        4.0.3
Release:        3%{?dist}
Summary:        Manipulate, parse and generate OCaml compiler version strings
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        ISC
URL:            https://ocurrent.github.io/ocaml-version/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.07.0
BuildRequires:  ocaml-alcotest-devel
BuildRequires:  ocaml-dune >= 3.6

%description
This library provides facilities to parse version numbers of the OCaml
compiler, and enumerates the various official OCaml releases and
configuration variants.

OCaml version numbers are of the form `major.minor.patch+extra`, where
the `patch` and `extra` fields are optional.  This library offers the
following functionality:

- Functions to parse and serialize OCaml compiler version numbers
- Enumeration of official OCaml compiler version releases
- Test compiler versions for a particular feature (e.g. the `bytes`
  type)
- opam compiler switch enumeration

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 4.0.3-3
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 4.0.3-2
- OCaml 5.4.0 rebuild

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 4.0.3-1
- New upstream version 4.0.3 (RHBZ#2402310)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James <loganjerry@gmail.com> - 4.0.1-1
- Version 4.0.1

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Jerry James <loganjerry@gmail.com> - 3.7.3-1
- OCaml 5.3.0 rebuild for Fedora 42
- Version 3.7.3

* Sun Oct 06 2024 Jerry James <loganjerry@gmail.com> - 3.6.9-1
- Version 3.6.9

* Thu Sep 26 2024 Jerry James <loganjerry@gmail.com> - 3.6.8-1
- Version 3.6.8

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 3.6.7-3
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 3.6.7-2
- OCaml 5.2.0 for Fedora 41

* Thu May 23 2024 Jerry James <loganjerry@gmail.com> - 3.6.7-1
- Version 3.6.7

* Fri Feb  2 2024 Jerry James <loganjerry@gmail.com> - 3.6.4-1
- Version 3.6.4

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 3.6.3-3
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 3.6.3-2
- OCaml 5.1.1 rebuild for Fedora 40

* Mon Dec 11 2023 Jerry James <loganjerry@gmail.com> - 3.6.3-1
- Version 3.6.3

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 3.6.2-2
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 3.6.2-1
- Version 3.6.2

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 3.6.1-3
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 3.6.1-2
- OCaml 5.0.0 rebuild

* Tue Mar 21 2023 Jerry James <loganjerry@gmail.com> - 3.6.1-1
- Version 3.6.1
- Re-enable debuginfo generation now that dune is fixed

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 3.6.0-2
- Rebuild OCaml packages for F38

* Fri Jan 20 2023 Jerry James <loganjerry@gmail.com> - 3.6.0-1
- Version 3.6.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul  8 2022 Jerry James <loganjerry@gmail.com> - 3.5.0-1
- Version 3.5.0
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 3.4.0-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 3.4.0-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Jerry James <loganjerry@gmail.com> - 3.4.0-1
- Initial RPM
