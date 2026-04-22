# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

# This package is needed to build dune.  To avoid circular dependencies, this
# package cannot depend on dune, or any package that depends on dune.
# Therefore, we:
# - hack up our own build, rather than using dune to do the build
# - skip tests, which require ppx_expect, which is built with dune
# If you know what you are doing, build with dune anyway using this conditional.
%bcond dune 0

%global giturl  https://github.com/ocaml-dune/csexp

Name:           ocaml-csexp
Version:        1.5.2
Release: 17%{?dist}
Summary:        Parsing and printing of S-expressions in canonical form

License:        MIT
URL:            https://ocaml-dune.github.io/csexp/
VCS:            git:%{giturl}.git
Source:         %{giturl}/releases/download/%{version}/csexp-%{version}.tbz
# Fix an optimization annotation
Patch:          %{giturl}/commit/07eb898.patch

BuildRequires:  ocaml >= 4.03.0
%if %{with dune}
BuildRequires:  ocaml-dune >= 1.11
%else
BuildRequires:  ocaml-rpm-macros
%endif

%description
This project provides minimal support for parsing and printing
S-expressions in canonical form, which is a very simple and canonical
binary encoding of S-expressions.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n csexp-%{version} -p1

%build
%if %{with dune}
%dune_build
%else
OFLAGS="-w -40 -g"
OCFLAGS="$OFLAGS -bin-annot"
cd src
ocamlc $OCFLAGS -no-alias-deps -o csexp.cmi -c -intf csexp.mli
ocamlc $OCFLAGS -intf-suffix .ml -no-alias-deps -o csexp.cmo -c -impl csexp.ml
ocamlc $OFLAGS -a -o csexp.cma csexp.cmo
%ifarch %{ocaml_native_compiler}
ocamlopt $OFLAGS -intf-suffix .ml -no-alias-deps -o csexp.cmx -c -impl csexp.ml
ocamlopt $OFLAGS -a -o csexp.cmxa csexp.cmx
ocamlopt $OFLAGS -shared -linkall -I . -o csexp.cmxs csexp.cmxa
%endif
%endif

%install
%if %{with dune}
%dune_install
%else
# Install without dune.  See comment at the top.
mkdir -p %{buildroot}%{ocamldir}/csexp
cp -p src/csexp.{cma,cmi,cmt,cmti,mli} %{buildroot}%{ocamldir}/csexp
%ifarch %{ocaml_native_compiler}
cp -p src/csexp.{a,cmx,cmxa,cmxs} %{buildroot}%{ocamldir}/csexp
%endif
cp -p csexp.opam %{buildroot}%{ocamldir}/csexp/opam

cat >> %{buildroot}%{ocamldir}/csexp/META << EOF
version = "%{version}"
description = "Parsing and printing of S-expressions in canonical form"
requires = ""
archive(byte) = "csexp.cma"
%ifarch %{ocaml_native_compiler}
archive(native) = "csexp.cmxa"
%endif
plugin(byte) = "csexp.cma"
%ifarch %{ocaml_native_compiler}
plugin(native) = "csexp.cmxs"
%endif
EOF

cat >> %{buildroot}%{ocamldir}/csexp/dune-package << EOF
(lang dune 3.19)
(name csexp)
(version %{version})
(sections (lib .) (libexec .) (doc ../../doc/csexp))
(files
 (lib
  (META
   csexp.a
   csexp.cma
   csexp.cmi
   csexp.cmt
   csexp.cmti
   csexp.cmx
%ifarch %{ocaml_native_compiler}
   csexp.cmxa
%endif
   csexp.ml
   csexp.mli
   dune-package
   opam))
%ifarch %{ocaml_native_compiler}
 (libexec (csexp.cmxs))
%endif
 (doc (CHANGES.md LICENSE.md README.md)))
(library
 (name csexp)
 (kind normal)
%ifarch %{ocaml_native_compiler}
 (archives (byte csexp.cma) (native csexp.cmxa))
 (plugins (byte csexp.cma) (native csexp.cmxs))
 (native_archives csexp.a)
%else
 (archives (byte csexp.cma))
 (plugins (byte csexp.cma))
%endif
 (main_module_name Csexp)
%ifarch %{ocaml_native_compiler}
 (modes byte native)
%else
 (modes byte)
%endif
 (modules
  (singleton
   (obj_name csexp)
   (visibility public)
   (source (path Csexp) (intf (path csexp.mli)) (impl (path csexp.ml))))))
EOF

%ocaml_files
%endif

%files -f .ofiles
%doc README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 1.5.2-15
- Rebuild to fix OCaml dependencies
- Bump the dune lang up to 3.19

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 1.5.2-13
- OCaml 5.3.0 rebuild for Fedora 42
- Bump the dune lang up to 3.17

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-12
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-11
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-8
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-7
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-6
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 1.5.2-5
- Add patch for typo in optimization annotation

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-3
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.5.2-2
- OCaml 5.0.0 rebuild

* Fri Mar 24 2023 Jerry James <loganjerry@gmail.com> - 1.5.2-1
- Version 1.5.2

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-10
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 1.5.1-7
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-7
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-6
- OCaml 4.13.1 rebuild to remove package notes

* Thu Feb  3 2022 Jerry James <loganjerry@gmail.com> - 1.5.1-5
- Update non-dune build instructions to match dune 2.9

* Wed Jan 26 2022 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-5
- Don't add -Wl,-dT,<build dir> to build flags

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 31 2021 Jerry James <loganjerry@gmail.com> - 1.5.1-1
- Version 1.5.1
- Drop upstreamed -result patch

* Sun Feb 28 22:16:45 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-3
- Bump release and rebuild.

* Sun Feb 28 22:08:24 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-2
- OCaml 4.12.0 build

* Wed Feb 24 2021 Jerry James <loganjerry@gmail.com> - 1.4.0-1
- Version 1.4.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 18 2020 Jerry James <loganjerry@gmail.com> - 1.3.2-1
- Version 1.3.2

* Thu Sep 10 2020 Jerry James <loganjerry@gmail.com> - 1.3.1-1
- Initial RPM
