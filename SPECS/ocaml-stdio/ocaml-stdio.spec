%global srcname stdio

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%bcond_with docs

Summary:        Jane Street Standard I/O library for OCaml
Name:           ocaml-%{srcname}
Version:        0.15.0
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/janestreet/%{srcname}
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.04.2
BuildRequires:  ocaml-base-devel >= 0.14
BuildRequires:  ocaml-dune-devel >= 2.0.0

%if %{with docs}
BuildRequires:  ocaml-odoc
%endif

%description
Stdio provides input/output functions for OCaml.  It re-exports the
buffered channels of the stdlib distributed with OCaml but with some
improvements.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-base-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%if %{with docs}
%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
Documentation for %{name}.
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
dune build %{?_smp_mflags}
%if %{with docs}
dune build %{?_smp_mflags} @doc
%endif

%install
dune install --destdir=%{buildroot}

%if %{with docs}
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

%files
%doc CHANGES.md
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/*.cma
%{_libdir}/ocaml/%{srcname}/*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/*.a
%{_libdir}/ocaml/%{srcname}/*.cmx
%{_libdir}/ocaml/%{srcname}/*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/*.cmt
%{_libdir}/ocaml/%{srcname}/*.cmti
%{_libdir}/ocaml/%{srcname}/*.mli

%if %{with docs}
%files doc
%doc _build/default/_doc/_html/
%doc _build/default/_doc/_mlds/
%doc _build/default/_doc/_odoc/
%license LICENSE.md
%endif

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.15.0-2
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.15.0-1
- Upgrade to latest version
- License verified

* Mon Aug 09 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.14.0-10
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Remove docs circular dependencies

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 0.14.0-9
- Bump and rebuild

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 0.14.0-8
- Rebuild for ocaml-base 0.14.1

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-7
- Bump and rebuild for updated ocaml Dynlink dependency.

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

* Thu Jun 18 2020 Jerry James <loganjerry@gmail.com> - 0.14.0-1
- Version 0.14.0

* Thu May  7 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-1
- Initial RPM
