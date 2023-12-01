%global srcname sexplib0

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Summary:        Definition of S-expressions and some base converters
Name:           ocaml-%{srcname}
Version:        0.15.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/janestreet/sexplib0
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.04.2
BuildRequires:  ocaml-dune >= 2.0.0
BuildRequires:  ocaml-findlib

%description
This package contains a library with the definition of S-expressions and
some base converters.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{srcname}-%{version}

%build
dune build %{?_smp_mflags}

# TODO: Once odoc is available, BR it and run this to generate documentation:
# dune build @doc

%install
dune install --destdir=%{buildroot}

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%ifarch %{ocaml_native_compiler}
# Add missing executable bits
chmod a+x %{buildroot}%{_libdir}/ocaml/%{srcname}/%{srcname}.cmxs
%endif

%files
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cma
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.a
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmx
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmt
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmti
%{_libdir}/ocaml/%{srcname}/*.ml
%{_libdir}/ocaml/%{srcname}/*.mli

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.15.0-2
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.15.0-1
- Upgrade to latest version
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.0-8
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-7
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-5
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-4
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 17 2020 Jerry James <loganjerry@gmail.com> - 0.14.0-1
- Version 0.14.0

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-7
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-6
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-2
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan  2 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-1
- Initial RPM
