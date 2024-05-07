%global srcname ppxlib

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

# This package is a transitive dependency of odoc, but needs odoc to build its
# documentation.  Break the circular dependency here.
%bcond_with doc

Summary:        Base library and tools for ppx rewriters
Name:           ocaml-%{srcname}
Version:        0.31.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ocaml-ppx/ppxlib
Source0:        https://github.com/ocaml-ppx/ppxlib/archive/refs/tags/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
# We do not have stdlib-shims
Patch0:         %{name}-stdlib-shims.patch
 
BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-cinaps-devel >= 0.12.1
BuildRequires:  ocaml-compiler-libs-janestreet-devel >= 0.11.0
BuildRequires:  ocaml-dune >= 2.7
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ppx-derivers-devel >= 1.0
BuildRequires:  ocaml-re-devel >= 1.9.0
BuildRequires:  ocaml-sexplib0-devel >= 0.15

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
Requires:       ocaml-ppx-derivers-devel%{?_isa}
Requires:       ocaml-sexplib0-devel%{?_isa}
 
%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use
%{name}.
 
%prep
%autosetup -n ppxlib-%{version} -p1
 
%build
%dune_build
%install
%dune_install
%check
%dune_check
%files -f .ofiles
%doc CHANGES.md HISTORY.md README.md
%license LICENSE.md
 
%files devel -f .ofiles-devel

%changelog
* Wed May 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.31.0-1
- Upgrade to 0.31.0

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
