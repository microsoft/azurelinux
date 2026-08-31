# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifarch %{ocaml_native_compiler}
%undefine _debugsource_packages
%else
%global debug_package %{nil}
%endif

Name:           ocaml-compiler-libs-janestreet
Version:        0.17.0
Release:        8%{?dist}
Summary:        OCaml compiler libraries repackaged

License:        MIT
URL:            https://github.com/janestreet/ocaml-compiler-libs
VCS:            git:%{url}.git
Source:         %{url}/archive/v%{version}/ocaml-compiler-libs-%{version}.tar.gz

BuildRequires:  ocaml >= 5.2.0
BuildRequires:  ocaml-dune >= 1.5.1

%description
This package exposes the OCaml compiler libraries repackaged under
the toplevel names Ocaml_common, Ocaml_bytecomp, Ocaml_optcomp, etc.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use
%{name}.

%prep
%autosetup -n ocaml-compiler-libs-%{version}

%build
%dune_build

%install
%dune_install

%files -f .ofiles
%doc README.org
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 0.17.0-7
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 0.17.0-5
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.17.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.17.0-3
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.17.0-2
- OCaml 5.2.0 for Fedora 41

* Thu May 23 2024 Jerry James <loganjerry@gmail.com> - 0.17.0-1
- Version 0.17.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-16
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-15
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-14
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-12
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.12.4-11
- OCaml 5.0.0 rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-10
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 0.12.4-7
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-7
- OCaml 4.14.0 rebuild

* Mon Feb 28 2022 Jerry James <loganjerry@gmail.com> - 0.12.4-6
- Build in release mode

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-5
- Bump release and rebuild.

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-4
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 0.12.4-2
- OCaml 4.13.1 build

* Wed Aug 25 2021 Jerry James <loganjerry@gmail.com> - 0.12.4-1
- Version 0.12.4

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar  1 12:17:33 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.12.3-3
- OCaml 4.12.0 build
- Make the -doc subpackage conditional.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 0.12.3-1
- Version 0.12.3

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.12.1-5
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.12.1-4
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May  7 2020 Jerry James <loganjerry@gmail.com> - 0.12.1-1
- Initial RPM
