%global srcname fmt

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Summary:        OCaml Format pretty-printer combinators
Name:           ocaml-%{srcname}
Version:        0.9.0
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://erratique.ch/software/fmt
Source0:        https://github.com/dbuenzli/fmt/archive/v%{version}/%{srcname}-%{version}.tar.gz
# We neither need nor want the stdlib-shims package.  It is a forward
# compatibility package for older OCaml installations.  Patch it out instead.
# Upstream does not want this patch until stdlib-shims is obsolete.
#Patch0:         %{name}-stdlib-shims.patch

BuildRequires:  ocaml >= 4.05.0
BuildRequires:  ocaml-cmdliner-devel >= 0.9.8
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-seq-devel
BuildRequires:  ocaml-topkg-devel >= 0.9.0

%description
Fmt exposes combinators to devise `Format` pretty-printing functions.

Fmt depends only on the OCaml standard library.  The optional Fmt_tty
library that enables setting up formatters for terminal color output
depends on the Unix library.  The optional Fmt_cli library that provides
command line support for Fmt depends on Cmdliner.

%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-seq-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{srcname}-%{version} -p1

# Topkg does watermark replacements only if run inside a git checkout.  Github
# tarballs do not come with a .git directory.  Therefore, we do the watermark
# replacement manually.
for fil in $(find . -type f); do
  sed -e 's,%%%%NAME%%%%,%{srcname},' \
      -e 's,%%%%VERSION%%%%,v%{version},' \
      -e 's,%%%%VERSION_NUM%%%%,%{version},' \
      -i.orig $fil
  touch -r $fil.orig $fil
  rm $fil.orig
done

%build
# Build the library and the tests
ocaml pkg/pkg.ml build --tests true --with-base-unix true --with-cmdliner true

# Build the documentation
mkdir html
ocamldoc -html -d html -I +cmdliner -I _build/src _build/src/*.mli

%install
# Install the library
mkdir -p %{buildroot}%{_libdir}/ocaml/fmt
cp -p _build/{opam,pkg/META} %{buildroot}%{_libdir}/ocaml/fmt
%ifarch %{ocaml_native_compiler}
cp -a _build/src/*.{a,cma,cmi,cmt,cmti,cmx,cmxa,cmxs,mli} \
  %{buildroot}%{_libdir}/ocaml/fmt
%else
cp -a _build/src/*.{cma,cmi,cmt,cmti,mli} %{buildroot}%{_libdir}/ocaml/fmt
%endif

%check
ocaml pkg/pkg.ml test

%files
%doc CHANGES.md README.md
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cma
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxs
%endif

%files devel
%doc html/*
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.a
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmx
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmt
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmti
%{_libdir}/ocaml/%{srcname}/%{srcname}*.mli

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.9-4
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.9-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov  3 2020 Jerry James <loganjerry@gmail.com> - 0.8.9-1
- Version 0.8.9

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-12
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-11
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-7
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-6
- OCaml 4.11.0 pre-release

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.8-2
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan  9 2020 Jerry James <loganjerry@gmail.com> - 0.8.8-1
- Initial RPM
