%global srcname uuidm

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Summary:        Universally unique identifiers (UUIDs) for OCaml
Name:           ocaml-%{srcname}
Version:        0.9.7
Release:        15%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://erratique.ch/software/uuidm
Source0:        https://github.com/dbuenzli/uuidm/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.03.0
BuildRequires:  ocaml-cmdliner-devel
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-topkg-devel

%description
Uuidm is an OCaml module implementing 128 bit universally unique
identifiers, versions 3, 5 (named based with MD5, SHA-1 hashing) and 4
(random based); see RFC 4122: http://tools.ietf.org/html/rfc4122.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{srcname}-%{version}

# The META file mistakenly uses the wrong version tag
sed -i 's/VERSION/VERSION_NUM/' pkg/META

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
ocaml pkg/pkg.ml build --tests true --with-cmdliner true

# Build the documentation
mkdir html
ocamldoc -html -d html -I _build/src _build/src/uuidm.mli

%install
# Install the library
mkdir -p %{buildroot}%{_libdir}/ocaml/uuidm
cp -p _build/{opam,pkg/META} %{buildroot}%{_libdir}/ocaml/uuidm
%ifarch %{ocaml_native_compiler}
cp -a _build/src/*.{a,cma,cmi,cmt,cmti,cmx,cmxa,cmxs,mli} \
  %{buildroot}%{_libdir}/ocaml/uuidm
%else
cp -a _build/src/*.{cma,cmi,cmt,cmti,mli} %{buildroot}%{_libdir}/ocaml/uuidm
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
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.7-15
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.9.7-14
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-12
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-11
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-7
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-6
- OCaml 4.11.0 pre-release

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.9.7-2
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan  9 2020 Jerry James <loganjerry@gmail.com> - 0.9.7-1
- Initial RPM