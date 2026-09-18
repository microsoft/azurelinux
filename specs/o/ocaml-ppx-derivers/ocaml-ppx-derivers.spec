# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-ppx-derivers
Version:        1.2.1
Release:        42%{?dist}
Summary:        Deriving plugin registry

License:        BSD-3-Clause
URL:            https://github.com/ocaml-ppx/ppx_derivers
VCS:            git:%{url}.git
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  ocaml
BuildRequires:  ocaml-dune

%description
Ppx_derivers is a tiny package whose sole purpose is to allow
ppx_deriving and ppx_type_conv to inter-operate gracefully when
linked as part of the same ocaml-migrate-parsetree driver.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%prep
%autosetup -n ppx_derivers-%{version}


%build
%dune_build


%install
%dune_install


%check
%dune_check


%files -f .ofiles
%doc README.md CHANGES.md
%license LICENSE.md


%files devel -f .ofiles-devel
%doc README.md CHANGES.md
%license LICENSE.md


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 1.2.1-41
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 1.2.1-39
- OCaml 5.3.0 rebuild for Fedora 42
- Add VCS field

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-37
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-36
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-33
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-32
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-31
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-29
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.2.1-28
- OCaml 5.0.0 rebuild
- Convert License tag to SPDX
- Use new dune macros

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-27
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-24
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-23
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 05 2021 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-21
- Bump release and rebuild.

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-20
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar  1 12:17:32 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-18
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-16
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-15
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-14
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-12
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-11
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-10
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-9
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-7
- OCaml 4.10.0+beta1 rebuild.

* Thu Dec 19 2019 Andy Li <andy@onthewings.net> - 1.2.1-6
- Rebuild against the latest OCaml.
- Remove unneeded BuildRequires on opam-installer.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-5
- OCaml 4.08.1 (final) rebuild.

* Thu Aug 01 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-4
- OCaml 4.08.1 (rc2) rebuild.

* Sat Jul 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-3
- Bump and rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Andy Li <andy@onthewings.net> - 1.2.1-1
- Initial RPM release.

