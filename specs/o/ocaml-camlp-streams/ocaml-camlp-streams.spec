# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-camlp-streams
Version:        5.0.1
Release: 20%{?dist}
Summary:        Stream and Genlex libraries for OCaml

License:        LGPL-2.1-only WITH OCaml-LGPL-linking-exception
URL:            https://github.com/ocaml/camlp-streams
VCS:            git:%{url}.git
Source:         %{url}/archive/v%{version}/camlp-streams-%{version}.tar.gz

BuildRequires:  ocaml >= 4.02.3
BuildRequires:  ocaml-dune >= 2.7

%description
The camlp-streams package provides two library modules:
- Stream: imperative streams, with in-place update and memoization of
  the latest element produced.
- Genlex: a small parameterized lexical analyzer producing streams of
  tokens from streams of characters.

The two modules are designed for use with Camlp4 and Camlp5:
- The stream patterns and stream expressions of Camlp4/Camlp5 consume
  and produce data of type `'a Stream.t`.
- The Genlex tokenizer can be used as a simple lexical analyzer for
  Camlp4/Camlp5-generated parsers.

The Stream module can also be used by hand-written recursive-descent
parsers, but is not very convenient for this purpose.

The Stream and Genlex modules have been part of the OCaml standard
library for a long time, and have been distributed as part of the core
OCaml system.  They will be removed from the OCaml standard library at
some future point, but will be maintained and distributed separately in
this camlp-streams package.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n camlp-streams-%{version}

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE

%files devel -f .ofiles-devel

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 5.0.1-18
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 5.0.1-16
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 5.0.1-14
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 5.0.1-13
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 5.0.1-10
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 5.0.1-9
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 5.0.1-8
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 5.0.1-6
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 5.0.1-5
- OCaml 5.0.0 rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 5.0.1-4
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Jerry James <loganjerry@gmail.com> - 5.0.1-2
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul  5 2022 Jerry James <loganjerry@gmail.com> - 5.0.1-1
- Initial RPM (rhbz#2104283)
