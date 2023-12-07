%global srcname topkg

# BOOTSTRAP NOTE: currently we do not build the optional topkg-care part.
# It has dependencies which do not yet exist in Mariner, and which themselves
# depend on the main part of this package.
%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Summary:        The transitory OCaml software packager
Name:           ocaml-%{srcname}
Version:        1.0.7
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://erratique.ch/software/topkg/
Source0:        https://github.com/dbuenzli/topkg/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.03.0
BuildRequires:  ocaml-findlib >= 1.6.1
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-result-devel

%description
Topkg is a packager for distributing OCaml software.  It provides an
API to describe the files a package installs in a given build
configuration and to specify information about the package's
distribution, creation and publication procedures.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-result-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-%{version}

# This package can replace "watermarks" in software that it builds.  However,
# we are building from scratch, rather than using topkg to build itself, so we
# have to do the job manually.
for fil in $(find . -type f); do
  sed -e 's,%%%%NAME%%%%,%{srcname},' \
      -e 's,%%%%PKG_DOC%%%%,%{url}doc/,' \
      -e 's,%%%%PKG_HOMEPAGE%%%%,%{url},' \
      -e 's,%%%%VERSION%%%%,v%{version},' \
      -e 's,%%%%VERSION_NUM%%%%,%{version},' \
      -i.orig $fil
  touch -r $fil.orig $fil
  rm $fil.orig
done

%build
# Build the library and the tests
ocaml pkg/pkg.ml build --pkg-name topkg --tests true

# Build the command line tool
%ifarch %{ocaml_native_compiler}
ocamlbuild topkg.native
%else
ocamlbuild topkg.byte
%endif

# Build the documentation.  It is meant to be built with odoc, but odoc
# transitively depends on this package, so we do it manually for bootstrap
# builds.  Once a non-bootstrap build is possible, use odoc instead.
mkdir html
ocamldoc -html -d html -I _build/src _build/src/*.{mli,ml}

%install
# Install the library
mkdir -p %{buildroot}%{_libdir}/ocaml/topkg
cp -p _build/topkg.opam %{buildroot}%{_libdir}/ocaml/topkg/opam
cp -p _build/pkg/META %{buildroot}%{_libdir}/ocaml/topkg/META
%ifarch %{ocaml_native_compiler}
cp -a _build/src/*.{a,cma,cmi,cmt,cmti,cmx,cmxa,cmxs,mli} \
  %{buildroot}%{_libdir}/ocaml/topkg
%else
cp -a _build/src/*.{cma,cmi,cmt,cmti,mli} %{buildroot}%{_libdir}/ocaml/topkg
%endif

# Install the command line tool
mkdir -p %{buildroot}%{_bindir}
%ifarch %{ocaml_native_compiler}
cp -p _build/src/topkg.native %{buildroot}%{_bindir}/topkg
%else
cp -p _build/src/topkg.byte %{buildroot}%{_bindir}/topkg
%endif

%check
ocaml pkg/pkg.ml test

%files
%doc CHANGES.md README.md
%license LICENSE.md
%{_bindir}/%{srcname}
%dir %{_libdir}/ocaml/%{srcname}/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/%{srcname}.cma
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}.a
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmx
%{_libdir}/ocaml/%{srcname}/%{srcname}.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmt
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmti
%{_libdir}/ocaml/%{srcname}/%{srcname}*.mli

%files doc
%doc html/*

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.7-1
- Auto-upgrade to 1.0.7 - Azure Linux 3.0 - package upgrades

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-4
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.3-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec  1 2020 Jerry James <loganjerry@gmail.com> - 1.0.3-1
- Version 1.0.3

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-2
- OCaml 4.11.1 rebuild

* Tue Sep  1 2020 Jerry James <loganjerry@gmail.com> - 1.0.2-1
- Version 1.0.2

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-11
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-7
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-6
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan  9 2020 Jerry James <loganjerry@gmail.com> - 1.0.1-1
- Initial RPM
