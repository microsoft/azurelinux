%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           not-ocamlfind
Version:        0.14
Release:        6%{?dist}
Summary:        Front-end to ocamlfind that adds a few new commands
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        MIT
URL:            https://github.com/chetmurthy/not-ocamlfind
VCS:            git:%{url}.git
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch:    %{ix86}

BuildRequires:  m4
BuildRequires:  ocaml
BuildRequires:  ocaml-camlp-streams-devel
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-findlib-devel >= 1.8.0
BuildRequires:  ocaml-fmt-devel >= 0.8.8
BuildRequires:  ocaml-ocamlgraph-devel >= 2.0.0
BuildRequires:  ocaml-rresult-devel >= 0.6.0
BuildRequires:  which

Requires:       ocaml-findlib%{?_isa}

Recommends:     %{py3_dist xdot}

%description
The command not-ocamlfind is a pass-thru to ocamlfind, but adds three
new commands: preprocess, reinstall-if-diff and package-graph.

- reinstall-if-diff does what it says on the label: only reinstalls
  (remove then install) if the file-content of the package has changed.

- preprocess produces the source and does not attempt to compile it; as
  an added benefit, it prints (to stderr) the commands it executed to
  produce that source.   So you can use this for debugging multi-stage
  PPX rewriter sequences.

- package-graph outputs a graph in the format accepted by the dot
  command of graphviz.  By default you get the package-dependency graph,
  with sizes of the archives for each packages as part of the
  node-label.  If you add -dominator-from <node>, it will compute the
  dominator-tree from that node, and if you add -xdot, it will
  automatically invoke xdot on the graph.

%prep
%autosetup

%build
# The build wants us to use a patched vendored version of findlib.  However,
# the findlib in Fedora already has the patches, and is a later version.  Do
# not use the configure script or Makefile until it is possible to build
# without the vendored findlib.
%ifarch %{ocaml_native_compiler}
ocamlfind ocamlopt \
  -I +findlib findlib.cmxa \
%else
ocamlfind ocamlc \
  -I +findlib findlib.cma \
%endif
  -g \
  -package str,unix,fmt,rresult,ocamlgraph,camlp-streams \
  -linkall \
  -linkpkg \
  fsmod.ml frontend.ml main.ml \
  -o not-ocamlfind

%ifarch %{ocaml_native_compiler}
ocamlfind ocamlopt \
  -I +findlib findlib.cmxa \
%else
ocamlfind ocamlc \
  -I +findlib findlib.cma \
%endif
  -g \
  -package str,unix,compiler-libs.common \
  -linkall \
  -linkpkg \
  papr_official.ml \
  -o papr_official.exe

%install
# The makefile ignores DESTDIR, and there are only 4 files to install anyway...
mkdir -p %{buildroot}%{_bindir}
cp -p not-ocamlfind %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{ocamldir}/not-ocamlfind
cp -p META opam papr_official.exe %{buildroot}%{ocamldir}/not-ocamlfind

%check
# Upstream provides no tests, so we just check that simple usage gives us a
# zero exit code
./not-ocamlfind package-graph -predicates true -package findlib

%files
%doc CHANGES README.md
%license LICENSE
%{_bindir}/not-ocamlfind
%{ocamldir}/not-ocamlfind/

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 0.14-6
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Tue Oct 14 2025 Richard W.M. Jones <rjones@redhat.com> - 0.14-5
- OCaml 5.4.0 rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James <loganjerry@gmail.com> - 0.14-3
- Rebuild to fix OCaml dependencies

* Tue Apr 15 2025 Jerry James <loganjerry@gmail.com> - 0.14-2
- Rebuild for ocaml-ocamlgraph 2.2.0

* Fri Mar 21 2025 Jerry James <loganjerry@gmail.com> - 0.14-1
- Version 0.14

* Mon Mar 10 2025 Jerry James <loganjerry@gmail.com> - 0.13-7
- Rebuild for ocaml-fmt 0.10.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 10 2025 Jerry James <loganjerry@gmail.com> - 0.13-5
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 17 2024 Jerry James <loganjerry@gmail.com> - 0.13-3
- Add VCS field

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.13-2
- OCaml 5.2.0 ppc64le fix

* Fri Jun 07 2024 Jerry James <loganjerry@gmail.com> - 0.13-1
- Version 0.13

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.12-7
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12-4
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12-3
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.12-2
- OCaml 5.1 rebuild for Fedora 40

* Thu Oct 05 2023 Jerry James <loganjerry@gmail.com> - 0.12-1
- Version 0.12

* Sun Sep 10 2023 Jerry James <loganjerry@gmail.com> - 0.11-2
- Rebuild for ocaml-ocamlgraph 2.1.0

* Fri Sep 01 2023 Jerry James <loganjerry@gmail.com> - 0.11-1
- Version 0.11

* Tue Aug 15 2023 Jerry James <loganjerry@gmail.com> - 0.10-2
- Do not build for i386

* Tue Aug 15 2023 Jerry James <loganjerry@gmail.com> - 0.10-1
- Initial RPM

