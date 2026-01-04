# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-bos
Version:        0.2.1
Release:        32%{?dist}
Summary:        Basic OS interaction for OCaml
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        ISC
URL:            https://erratique.ch/software/bos
VCS:            git:https://erratique.ch/repos/bos.git
Source:         %{url}/releases/bos-%{version}.tbz#/%{name}-%{version}.tbz

BuildRequires:  ocaml >= 4.08.0
BuildRequires:  ocaml-astring-devel
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-fmt-devel >= 0.8.10
BuildRequires:  ocaml-fpath-devel >= 0.7.3
BuildRequires:  ocaml-logs-devel
BuildRequires:  ocaml-mtime-devel
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-rpm-macros
BuildRequires:  ocaml-rresult-devel >= 0.7.0
BuildRequires:  ocaml-topkg-devel >= 1.0.3

# Do not require ocaml-compiler-libs at runtime
%global __ocaml_requires_opts -i Asttypes -i Build_path_prefix_map -i Cmi_format -i Env -i Format_doc -i Ident -i Identifiable -i Load_path -i Location -i Longident -i Misc -i Oprint -i Outcometree -i Parsetree -i Path -i Primitive -i Shape -i Subst -i Toploop -i Type_immediacy -i Types -i Unit_info -i Warnings

%description
Bos provides support for basic and robust interaction with the operating
system in OCaml.  It has functions to access the process environment,
parse command line arguments, interact with the file system and run
command line programs.  Bos works equally well on POSIX and Windows
operating systems.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-astring-devel%{?_isa}
Requires:       ocaml-fmt-devel%{?_isa}
Requires:       ocaml-fpath-devel%{?_isa}
Requires:       ocaml-logs-devel%{?_isa}
Requires:       ocaml-rresult-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n bos-%{version}

%build
ocaml pkg/pkg.ml build --dev-pkg false --tests true

%install
%ocaml_install

%check
ocaml pkg/pkg.ml test

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE.md

%files devel -f .ofiles-devel
%if %{with docs}
%doc _build/default/_doc/*
%endif

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.2.1-32
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Tue Oct 14 2025 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-31
- OCaml 5.4.0 rebuild

* Mon Aug 25 2025 Jerry James <loganjerry@gmail.com> - 0.2.1-30
- Rebuild for ocaml-fmt 0.11.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James  <loganjerry@gmail.com> - 0.2.1-28
- Rebuild to fix OCaml dependencies

* Tue Mar 18 2025 Jerry James <loganjerry@gmail.com> - 0.2.1-27
- Rebuild for ocaml-logs 0.8.0

* Mon Mar 10 2025 Jerry James <loganjerry@gmail.com> - 0.2.1-26
- Rebuild for ocaml-fmt 0.10.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 0.2.1-24
- OCaml 5.3.0 rebuild for Fedora 42

* Tue Oct 08 2024 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-23
- Rebuild for ocaml-lwt 5.8.0

* Thu Sep 12 2024 Jerry James <loganjerry@gmail.com> - 0.2.1-22
- Rebuild for ocaml-mtime 2.1.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-20
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-19
- OCaml 5.2.0 for Fedora 41

* Mon Jan 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-18
- Bump and rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-15
- Bump release and rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-14
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-13
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-12
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 0.2.1-11
- Use the %%ocaml_install macro

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-10
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.2.1-9
- OCaml 5.0.0 rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-8
- Bump release and rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-7
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 0.2.1-4
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.2.1-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 10 2021 Jerry James <loganjerry@gmail.com> - 0.2.1-1
- Initial RPM
