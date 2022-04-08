%global libname ocplib-endian
%global debug_package %{nil}

Summary:        Functions to read/write int16/32/64 from strings, bigarrays
Name:           ocaml-ocplib-endian
Version:        1.1
Release:        8%{?dist}
# License is LGPL 2.1 with standard OCaml exceptions
License:        LGPLv2+ WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/OCamlPro/ocplib-endian
Source0:        https://github.com/OCamlPro/ocplib-endian/archive/%{version}/ocplib-endian-%{version}.tar.gz

BuildRequires:  ocaml >= 4.02.3
BuildRequires:  ocaml-cppo >= 1.1.0
BuildRequires:  ocaml-dune >= 1.0

%description
Optimised functions to read and write int16/32/64 from strings,
bytes and bigarrays, based on primitives added in version 4.01.

The library implements three modules:

EndianString works directly on strings, and provides submodules
BigEndian and LittleEndian, with their unsafe counter-parts;
EndianBytes works directly on bytes, and provides submodules
BigEndian and LittleEndian, with their unsafe counter-parts;
EndianBigstring works on bigstrings (Bigarrays of chars),
and provides submodules BigEndian and LittleEndian, with their
unsafe counter-parts;

%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use %{name}.

%prep
%autosetup -n %{libname}-%{version}

%build
dune build %{?_smp_mflags}

%install
dune install --destdir=%{buildroot}

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

# We do not want the ml files
find %{buildroot}%{_libdir}/ocaml -name \*.ml -delete

# The tests currently fail, showing allocation of 54 words for all 3 tests.
# The issue is known, but upstream's remedy does not work with OCaml 4.11.
# See https://github.com/OCamlPro/ocplib-endian/issues/18
#
#%%check
#dune runtest

%files
%license COPYING.txt
%doc README.md CHANGES.md
%dir %{_libdir}/ocaml/%{libname}/
%dir %{_libdir}/ocaml/%{libname}/bigstring/
%{_libdir}/ocaml/%{libname}/META
%{_libdir}/ocaml/%{libname}/*.cma
%{_libdir}/ocaml/%{libname}/*.cmi
%{_libdir}/ocaml/%{libname}/bigstring/*.cma
%{_libdir}/ocaml/%{libname}/bigstring/*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{libname}/*.cmxs
%{_libdir}/ocaml/%{libname}/bigstring/*.cmxs
%endif

%files devel
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{libname}/*.a
%{_libdir}/ocaml/%{libname}/*.cmxa
%{_libdir}/ocaml/%{libname}/*.cmx
%{_libdir}/ocaml/%{libname}/bigstring/*.a
%{_libdir}/ocaml/%{libname}/bigstring/*.cmxa
%{_libdir}/ocaml/%{libname}/bigstring/*.cmx
%endif
%{_libdir}/ocaml/%{libname}/*.mli
%{_libdir}/ocaml/%{libname}/*.cmt
%{_libdir}/ocaml/%{libname}/*.cmti
%{_libdir}/ocaml/%{libname}/bigstring/*.mli
%{_libdir}/ocaml/%{libname}/bigstring/*.cmt
%{_libdir}/ocaml/%{libname}/bigstring/*.cmti
%{_libdir}/ocaml/%{libname}/dune-package
%{_libdir}/ocaml/%{libname}/opam

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-8
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1-7
- Initial CBL-Mariner import from Fedora 35 (license: MIT).

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jerry James <loganjerry@gmail.com> - 1.1-5
- Move META to the main package
- Drop obsolete workaround for dune bug

* Mon Mar  1 12:17:35 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1-5
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1-2
- OCaml 4.11.0 rebuild

* Wed Aug 19 2020 Jerry James <loganjerry@gmail.com> - 1.1-1
- Version 1.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-12
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-10
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-9
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-8
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-7
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0-5
- OCaml 4.10.0+beta1 rebuild.

* Sun Jan 12 2020 Robert-André Mauchin <zebob.m@gmail.com> - 1.0-4
- OCaml 4.09.0 (final) rebuild.

* Mon Oct 14 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.0-3
- Disable tests on s390x for now.

* Mon Oct 14 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.0-2
- Fix devel package Requires; switch to make_build macro.

* Mon Oct 14 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.0-1
- Initial package.
