Vendor:         Microsoft Corporation
Distribution:   Mariner
%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global srcname odoc

Name:           ocaml-%{srcname}
Version:        1.5.2
Release:        5%{?dist}
Summary:        Documentation compiler for OCaml and Reason

License:        MIT
URL:            https://github.com/ocaml/odoc
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.02.0
BuildRequires:  ocaml-alcotest-devel >= 0.8.3
BuildRequires:  ocaml-astring-devel
BuildRequires:  ocaml-bisect-ppx-devel >= 1.3.0
BuildRequires:  ocaml-cmdliner-devel
BuildRequires:  ocaml-cppo
BuildRequires:  ocaml-dune
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-fpath-devel
BuildRequires:  ocaml-markup-devel >= 1.0.0
BuildRequires:  ocaml-result-devel
BuildRequires:  ocaml-sexplib-devel >= 0.14.0
BuildRequires:  ocaml-tyxml-devel >= 4.3.0
BuildRequires:  tidy

%description
This package contains odoc, a documentation generator for OCaml.  It
reads doc comments, delimited with `(** ... *)`, and outputs HTML.  Text
inside doc comments is marked up in ocamldoc syntax.

Odoc's main advantage over ocamldoc is an accurate cross-referencer,
which handles the complexity of the OCaml module system.  Odoc also
offers a good opportunity to improve HTML output compared to ocamldoc,
but this is very much a work in progress.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-astring-devel%{?_isa}
Requires:       ocaml-fpath-devel%{?_isa}
Requires:       ocaml-result-devel%{?_isa}
Requires:       ocaml-tyxml-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version} -p1

# The opam file has not been updated since the great renumbering.
sed -i 's/113\.33\.00/0.14.0/' odoc.opam

# Replace version markers
for fil in src/html/tree.ml $(find test -name index.html -o -name mld.html); do
  sed -i.orig 's,%%%%VERSION%%%%,%{version},' $fil
  touch -r $fil.orig $fil
  rm $fil.orig
done

%build
dune build %{?_smp_mflags}
dune build %{?_smp_mflags} @doc

%install
dune install --destdir=%{buildroot}

# We do not want the test files
rm -fr %{buildroot}%{_libdir}/ocaml/dune_odoc_test

# We do not want the dune markers
find _build/default/_doc/_html -name .dune-keep -delete

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

# Install the man page
mkdir -p %{buildroot}%{_mandir}/man1
_build/install/default/bin/odoc --help groff > %{buildroot}%{_mandir}/man1/odoc.1

%check
dune runtest

%files
%doc CHANGES.md README.md
%license LICENSE.md
%{_bindir}/odoc
%{_datadir}/odoc/
%{_mandir}/man1/odoc.1*
%dir %{_libdir}/ocaml/%{srcname}/
%dir %{_libdir}/ocaml/%{srcname}/compat/
%dir %{_libdir}/ocaml/%{srcname}/html/
%dir %{_libdir}/ocaml/%{srcname}/loader/
%dir %{_libdir}/ocaml/%{srcname}/model/
%dir %{_libdir}/ocaml/%{srcname}/odoc/
%dir %{_libdir}/ocaml/%{srcname}/parser/
%dir %{_libdir}/ocaml/%{srcname}/xref/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/*/*.cma
%{_libdir}/ocaml/%{srcname}/*/*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*/*.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*/*.a
%{_libdir}/ocaml/%{srcname}/*/*.cmx
%{_libdir}/ocaml/%{srcname}/*/*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/*/*.cmt
%{_libdir}/ocaml/%{srcname}/*/*.cmti
%{_libdir}/ocaml/%{srcname}/*/*.ml
%{_libdir}/ocaml/%{srcname}/*/*.mli

%files doc
%doc _build/default/_doc/_html/*
%license LICENSE.md

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.5.2-5
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Fri Apr 23 2021 Jerry James <loganjerry@gmail.com> - 1.5.2-4
- Rebuild for ocaml-tyxml 4.5.0

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1.5.2-3
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec  2 2020 Jerry James <loganjerry@gmail.com> - 1.5.2-1
- Version 1.5.2

* Fri Oct 23 2020 Jerry James <loganjerry@gmail.com> - 1.5.1-5
- Rebuild for ocaml-markup 1.0.0

* Fri Sep 25 2020 Jerry James <loganjerry@gmail.com> - 1.5.1-4
- Rebuild for ocaml-fpath 0.7.3

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.5.1-2
- OCaml 4.11.0 rebuild

* Wed Aug  5 2020 Jerry James <loganjerry@gmail.com> - 1.5.1-1
- Version 1.5.1
- Drop upstreamed odoc-1.5.0-ocaml411.patch

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-5
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Wed Apr 22 2020 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-4
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-3
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-2
- OCaml 4.10.0 final.

* Fri Feb  7 2020 Jerry James <loganjerry@gmail.com> - 1.5.0-1
- Version 1.5.0
- Drop all patches

* Sat Feb  1 2020 Jerry James <loganjerry@gmail.com> - 1.4.2-3
- Add 3 patches for OCaml 4.10 compatibility

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 16 2020 Jerry James <loganjerry@gmail.com> - 1.4.2-2
- Remove some BRs needed only for transitive dependencies
- Add ocaml-astring-devel and ocaml-fpath-devel Rs to -devel
- Build in parallel

* Fri Jan 10 2020 Jerry James <loganjerry@gmail.com> - 1.4.2-1
- Initial RPM
