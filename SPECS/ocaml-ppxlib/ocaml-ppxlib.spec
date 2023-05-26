%global srcname ppxlib

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

# This package is a transitive dependency of odoc, but needs odoc to build its
# documentation.  Break the circular dependency here.
%bcond_with doc

Summary:        Base library and tools for ppx rewriters
Name:           ocaml-%{srcname}
Version:        0.24.0
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ocaml-ppx/ppxlib
Source0:        https://github.com/ocaml-ppx/ppxlib/releases/download/%{version}/%{srcname}-%{version}.tbz
# We do not have 'stdlib-shims'.
Patch0:         %{name}-stdlib-shims.patch
Patch1:         test-fix-sexplib0-0.15.0.patch

BuildRequires:  ocaml >= 4.04.1
BuildRequires:  ocaml-base-devel
BuildRequires:  ocaml-cinaps-devel >= 0.12.1
BuildRequires:  ocaml-compiler-libs-janestreet-devel >= 0.11.0
BuildRequires:  ocaml-dune >= 2.7
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-migrate-parsetree-devel >= 2.1.0
BuildRequires:  ocaml-ppx-derivers-devel >= 1.0
BuildRequires:  ocaml-re-devel >= 1.9.0
BuildRequires:  ocaml-sexplib0-devel >= 0.15.0
BuildRequires:  ocaml-stdio-devel

%if %{with doc}
BuildRequires:  ocaml-odoc
%endif

%description
The ppxlib project provides the basis for the ppx system, which is
currently the officially supported method for meta-programming in Ocaml.
It offers a principled way to generate code at compile time in OCaml
projects.  It features:
- an OCaml AST / parser/ pretty-printer snapshot, to create a full
  frontend independent of the version of OCaml;
- a library for ppx rewriters in general, and type-driven code generators
  in particular;
- a full-featured driver for OCaml AST transformers;
- a quotation mechanism for writing values representing OCaml AST in the
  OCaml syntax;
- a generator of open recursion classes from type definitions.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-compiler-libs-janestreet-devel%{?_isa}
Requires:       ocaml-migrate-parsetree-devel%{?_isa}
Requires:       ocaml-ppx-derivers-devel%{?_isa}
Requires:       ocaml-sexplib0-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use
%{name}.

%if %{with doc}
%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
Documentation for %{name}.
%endif

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
dune build %{?_smp_mflags}

%if %{with doc}
dune build %{?_smp_mflags} @doc
%endif

%install
dune install --destdir=%{buildroot}

%if %{with doc}
# We do not want the dune markers
find _build/default/_doc/_html -name .dune-keep -delete
%endif

# We do not want the ml files
find %{buildroot}%{_libdir}/ocaml -name \*.ml -delete

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%ifarch %{ocaml_native_compiler}
# Add missing executable bits
find %{buildroot}%{_libdir}/ocaml -name \*.cmxs -exec chmod a+x {} \+
%endif

# We do not want to install the test binaries
rm -fr %{buildroot}%{_bindir}

%check
dune runtest

%files
%doc CHANGES.md HISTORY.md README.md
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%dir %{_libdir}/ocaml/%{srcname}/ast/
%dir %{_libdir}/ocaml/%{srcname}/metaquot/
%dir %{_libdir}/ocaml/%{srcname}/metaquot_lifters/
%dir %{_libdir}/ocaml/%{srcname}/print_diff/
%dir %{_libdir}/ocaml/%{srcname}/runner/
%dir %{_libdir}/ocaml/%{srcname}/runner_as_ppx/
%dir %{_libdir}/ocaml/%{srcname}/traverse/
%dir %{_libdir}/ocaml/%{srcname}/traverse_builtins/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/*.cma
%{_libdir}/ocaml/%{srcname}/*.cmi
%{_libdir}/ocaml/%{srcname}/*/*.cma
%{_libdir}/ocaml/%{srcname}/*/*.cmi
%{_libdir}/ocaml/%{srcname}/*/*.exe
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*.cmxs
%{_libdir}/ocaml/%{srcname}/*/*.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*.a
%{_libdir}/ocaml/%{srcname}/*.cmx
%{_libdir}/ocaml/%{srcname}/*.cmxa
%{_libdir}/ocaml/%{srcname}/*/*.a
%{_libdir}/ocaml/%{srcname}/*/*.cmx
%{_libdir}/ocaml/%{srcname}/*/*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/*.cmt
%{_libdir}/ocaml/%{srcname}/*.cmti
%{_libdir}/ocaml/%{srcname}/*.mli
%{_libdir}/ocaml/%{srcname}/*/*.cmt
%{_libdir}/ocaml/%{srcname}/*/*.cmti
%{_libdir}/ocaml/%{srcname}/*/*.mli

%if %{with doc}
%files doc
%doc _build/default/_doc/_html/
%doc _build/default/_doc/_mlds/
%doc _build/default/_doc/_odoc/
%license LICENSE.md
%endif

%changelog
* Fri May 19 2023 Olivia Crain <oliviacrain@microsoft.com> - 0.24.0-3
- Add upstream patch to fix tests with ocaml-sexplib0-0.15.0
- Remove %%{arm} arch gating on tests (not supported by Mariner)

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.24.0-2
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.24.0-1
- Upgrade to latest version
- License verified

* Thu Dec 2 2021 Muhammad Falak <mwani@microsoft.com> - 0.22.0-3
- Remove epoch.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:0.22.0-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 1:0.22.0-1
- Version 0.22.0
- Drop upstreamed -longident-parse patch
- Do not build documentation by default due to circular dependency

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1:0.15.0-3
- Bump and rebuild for updated ocaml Dynlink dependency.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 1:0.15.0-1
- Version 0.15.0
- Drop upstreamed patches: -execption-format and -whitespace
- Add -stdlib-shims patch

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-6
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1:0.13.0-5
- OCaml 4.11.0 rebuild

* Fri Aug  7 2020 Jerry James <loganjerry@gmail.com> - 1:0.13.0-4
- Add Epoch to Requires from -devel to main package

* Fri Aug  7 2020 Jerry James <loganjerry@gmail.com> - 1:0.13.0-3
- Some ppx rewriters do not work with version 0.14.0 or 0.15.0, so revert to
  version 0.13.0 until they can be updated

* Thu Aug  6 2020 Jerry James <loganjerry@gmail.com> - 0.15.0-1
- Version 0.15.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 0.14.0-1
- New upstream release 0.14.0

* Thu Jun 18 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-2
- Rebuild for ocaml-stdio 0.14.0

* Thu May  7 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-1
- Initial RPM
