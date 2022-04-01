%global srcname astring

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Summary:        Alternative String module for OCaml
Name:           ocaml-%{srcname}
Version:        0.8.5
Release:        6%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://erratique.ch/software/astring
Source0:        https://github.com/dbuenzli/%{srcname}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.05.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-topkg-devel

%description
Astring exposes an alternative `String` module for OCaml.  This module
tries to balance minimality and expressiveness for basic, index-free,
string processing and provides types and functions for substrings,
string sets and string maps.

Remaining compatible with the OCaml `String` module is a non-goal.  The
`String` module exposed by Astring has exception safe functions,
removes deprecated and rarely used functions, alters some signatures
and names, adds a few missing functions and fully exploits OCaml's
newfound string immutability.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{srcname}-%{version}

# Topkg does watermark replacements only if run inside a git checkout.  Github
# tarballs do not come with a .git directory.  Therefore, we do the watermark
# replacement manually.
for fil in $(find . -type f); do
  sed -e 's,%%%%NAME%%%%,%{srcname},' \
      -e 's,%%%%PKG_HOMEPAGE%%%%,%{url},' \
      -e 's,%%%%VERSION%%%%,v%{version},' \
      -e 's,%%%%VERSION_NUM%%%%,%{version},' \
      -i.orig $fil
  touch -r $fil.orig $fil
  rm $fil.orig
done

%build
# Build the library and the tests
ocaml pkg/pkg.ml build --tests true

# Build the documentation
mkdir html
ocamldoc -html -d html -I +compiler-libs -I _build/src \
  -css-style doc/style.css _build/src/astring.mli

%install
# Install the library
mkdir -p %{buildroot}%{_libdir}/ocaml/astring
cp -p _build/{opam,pkg/META} %{buildroot}%{_libdir}/ocaml/astring
%ifarch %{ocaml_native_compiler}
cp -a _build/src/*.{a,cma,cmi,cmt,cmti,cmx,cmxa,cmxs,mli} \
  %{buildroot}%{_libdir}/ocaml/astring
%else
cp -a _build/src/*.{cma,cmi,cmt,cmti,mli} %{buildroot}%{_libdir}/ocaml/astring
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
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.5-6
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.8.5-5
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-2
- OCaml 4.11.0 rebuild

* Wed Aug 19 2020 Jerry James <loganjerry@gmail.com> - 0.8.5-1
- Version 0.8.5

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 0.8.4-1
- New upstream release 0.8.4 (rhbz#1849120)

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-7
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-6
- OCaml 4.11.0 pre-release

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-2
- OCaml 4.10.0+beta1 rebuild.

* Wed Jan  8 2020 Jerry James <loganjerry@gmail.com> - 0.8.3-1
- Initial RPM
