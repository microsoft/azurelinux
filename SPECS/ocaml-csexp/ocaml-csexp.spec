%global srcname csexp

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

# This package is needed to build dune.  To avoid circular dependencies, this
# package cannot depend on dune, or any package that depends on dune.
# Therefore, we:
# - hack up our own build, rather than using dune to do the build
# - bypass the need for ocaml-result (which requires dune to build)
# - skip tests, which require ppx_expect, which is built with dune
# - skip building documentation, which requires odoc, which is built with dune
# If you know what you are doing, build with dune anyway using this conditional.
%bcond_with dune

Summary:        Parsing and printing of S-expressions in canonical form
Name:           ocaml-%{srcname}
Version:        1.5.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ocaml-dune/csexp
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
# Fix an optimization annotation
Patch0:         07eb898.patch

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
%autosetup -n %{srcname}-%{version} -p1

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
(lang dune 3.12)
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
* Tue Apr 30 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.5.2-4
- Converted spec file to match with Fedora 41.
- Upgraded to 1.5.2.

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.2-4
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.2-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 18 2020 Jerry James <loganjerry@gmail.com> - 1.3.2-1
- Version 1.3.2

* Thu Sep 10 2020 Jerry James <loganjerry@gmail.com> - 1.3.1-1
- Initial RPM
