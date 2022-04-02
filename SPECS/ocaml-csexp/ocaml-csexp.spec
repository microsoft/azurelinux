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
Version:        1.3.2
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ocaml-dune/csexp
Source0:        %{url}/releases/download/%{version}/%{srcname}-%{version}.tbz
# Depend on Stdlib.Result instead of ocaml-result.  See comment above.
# This patch is not appropriate for upstream, which needs to keep compatibility
# with older OCaml versions.
Patch0:         %{name}-result.patch

BuildRequires:  ocaml >= 4.02.3
%if %{with dune}
BuildRequires:  ocaml-dune >= 1.11
BuildRequires:  ocaml-odoc
BuildRequires:  ocaml-result-devel >= 1.5
%endif

%description
This project provides minimal support for parsing and printing
S-expressions in canonical form, which is a very simple and canonical
binary encoding of S-expressions.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if %{with dune}
Requires:       ocaml-result-devel%{?_isa}
%endif

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -N -n %{srcname}-%{version}
%if %{without dune}
%autopatch -p1
%endif

%build
%if %{with dune}
dune build %{?_smp_mflags} --display=verbose @install
dune build %{?_smp_mflags} @doc
%else
OFLAGS="-strict-sequence -strict-formats -short-paths -keep-locs -g -opaque"
OCFLAGS="$OFLAGS -bin-annot"
cd src
ocamlc $OCFLAGS -output-obj csexp.mli
ocamlc $OCFLAGS -a -o csexp.cma csexp.ml
%ifarch %{ocaml_native_compiler}
ocamlopt $OFLAGS -ccopt "%{optflags}" -cclib "$RPM_LD_FLAGS" -a \
  -o csexp.cmxa csexp.ml
ocamlopt $OFLAGS -ccopt "%{optflags}" -cclib "$RPM_LD_FLAGS" -shared \
  -o csexp.cmxs csexp.ml
%endif
cd -
%endif

%install
%if %{with dune}
dune install --destdir=%{buildroot}

# We do not want the dune markers
find _build/default/_doc/_html -name .dune-keep -delete

# We do not want the ml files
find %{buildroot}%{_libdir}/ocaml -name \*.ml -delete

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%ifarch %{ocaml_native_compiler}
# Add missing executable bits
find %{buildroot}%{_libdir}/ocaml -name \*.cmxs -exec chmod a+x {} \+
%endif
%else
# Install without dune.  See comment at the top.
mkdir -p %{buildroot}%{_libdir}/ocaml/%{srcname}
cp -p src/csexp.{cma,cmi,cmt,cmti,mli} %{buildroot}%{_libdir}/ocaml/%{srcname}
%ifarch %{ocaml_native_compiler}
cp -p src/csexp.{a,cmx,cmxa,cmxs} %{buildroot}%{_libdir}/ocaml/%{srcname}
%endif
cp -p csexp.opam %{buildroot}%{_libdir}/ocaml/%{srcname}/opam

cat >> %{buildroot}%{_libdir}/ocaml/%{srcname}/META << EOF
version = "%{version}"
description = "Parsing and printing of S-expressions in canonical form"
archive(byte) = "csexp.cma"
%ifarch %{ocaml_native_compiler}
archive(native) = "csexp.cmxa"
%endif
plugin(byte) = "csexp.cma"
%ifarch %{ocaml_native_compiler}
plugin(native) = "csexp.cmxs"
%endif
EOF

cat >> %{buildroot}%{_libdir}/ocaml/%{srcname}/dune-package << EOF
(lang dune 2.5)
(name csexp)
(version %{version})
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
  (singleton (name Csexp) (obj_name csexp) (visibility public) (impl) (intf))))
EOF
%endif

# Cannot do this until ocaml-ppx-expect is available.
#%%if %%{with dune}
#%%check
#dune runtest
#%%endif

%files
%doc README.md
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/*.cma
%{_libdir}/ocaml/%{srcname}/*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*.a
%{_libdir}/ocaml/%{srcname}/*.cmx
%{_libdir}/ocaml/%{srcname}/*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/*.cmt
%{_libdir}/ocaml/%{srcname}/*.cmti
%{_libdir}/ocaml/%{srcname}/*.mli

%changelog
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
