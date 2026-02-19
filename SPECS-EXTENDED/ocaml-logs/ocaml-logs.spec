# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-logs
Version:        0.10.0
Release:        2%{?dist}
Summary:        Logging infrastructure for OCaml
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        ISC
URL:            https://erratique.ch/software/logs
VCS:            git:https://erratique.ch/repos/logs.git
Source:         %{url}/releases/logs-%{version}.tbz#/%{name}-%{version}.tbz

BuildRequires:  ocaml >= 4.14.0
BuildRequires:  ocaml-cmdliner-devel >= 1.3.0
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-fmt-devel >= 0.9.0
BuildRequires:  ocaml-lwt-devel
BuildRequires:  ocaml-mtime-devel
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-rpm-macros
BuildRequires:  ocaml-topkg-devel >= 1.1.0

# Do not require ocaml-compiler-libs at runtime
%global __ocaml_requires_opts -i Asttypes -i Build_path_prefix_map -i Cmi_format -i Env -i Format_doc -i Ident -i Identifiable -i Load_path -i Location -i Longident -i Misc -i Outcometree -i Parsetree -i Path -i Primitive -i Shape -i Subst -i Toploop -i Type_immediacy -i Types -i Warnings

%description
Logs provides a logging infrastructure for OCaml.  Logging is performed
on sources whose reporting level can be set independently.  The log
message report is decoupled from logging and is handled by a reporter.

A few optional log reporters are distributed with the base library and
the API lets you easily implement your own.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-cmdliner-devel%{?_isa}
Requires:       ocaml-fmt-devel%{?_isa}
Requires:       ocaml-lwt-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n logs-%{version} -p1

%build
ocaml pkg/pkg.ml build \
  --dev-pkg false \
  --tests true \
  --with-js_of_ocaml-compiler false \
  --with-fmt true \
  --with-cmdliner true \
  --with-lwt true \
  --with-base-threads true

%install
%ocaml_install

%check
ocaml pkg/pkg.ml test

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.10.0-2
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Tue Oct 14 2025 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-4
- OCaml 5.4.0 rebuild

* Mon Aug 25 2025 Jerry James <loganjerry@gmail.com> - 0.9.0-3
- Rebuild for ocaml-fmt 0.11.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James <loganjerry@gmail.com> - 0.9.0-1
- Version 0.9.0

* Tue Mar 18 2025 Jerry James <loganjerry@gmail.com> - 0.8.0-1
- Version 0.8.0
- Drop all patches and workarounds

* Mon Mar 10 2025 Jerry James <loganjerry@gmail.com> - 0.7.0-26
- Rebuild for ocaml-fmt 0.10.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 0.7.0-24
- OCaml 5.3.0 rebuild for Fedora 42

* Tue Oct 08 2024 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-23
- Rebuild for ocaml-lwt 5.8.0

* Thu Sep 12 2024 Jerry James <loganjerry@gmail.com> - 0.7.0-22
- Rebuild for ocaml-mtime 2.1.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-20
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-19
- OCaml 5.2.0 for Fedora 41

* Mon Jan 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-18
- Bump and rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-15
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-14
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-13
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 0.7.0-12
- Add patch to fix building tests with OCaml 5.1.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-11
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.7.0-10
- OCaml 5.0.0 rebuild
- Add patch to adapt to ocaml-mtime 2.0.0

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-9
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 20 2022 Jerry James <loganjerry@gmail.com> - 0.7.0-7
- Rebuild for ocaml-cmdliner 1.1.1

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 0.7.0-6
- Rebuild for ocaml-lwt 5.6.1
- Add patch to fix the tests

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 0.7.0-4
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-4
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.7.0-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec  6 2021 Jerry James <loganjerry@gmail.com> - 0.7.0-1
- Initial RPM

