%global srcname ocaml-compiler-libs

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%bcond_with docs

Summary:        OCaml compiler libraries repackaged
Name:           %{srcname}-janestreet
Version:        0.12.3
Release:        4%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/janestreet/%{srcname}
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.04.1
BuildRequires:  ocaml-dune >= 1.5.1

%if %{with docs}
BuildRequires:  ocaml-odoc
%endif

%description
This package exposes the OCaml compiler libraries repackaged under
the toplevel names Ocaml_common, Ocaml_bytecomp, Ocaml_optcomp, etc.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and
signature files for developing applications that use
%{name}.

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

# We do not want the dune markers
%if %{with docs}
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
%doc README.org
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%dir %{_libdir}/ocaml/%{srcname}/bytecomp/
%dir %{_libdir}/ocaml/%{srcname}/common/
%dir %{_libdir}/ocaml/%{srcname}/optcomp/
%dir %{_libdir}/ocaml/%{srcname}/shadow/
%dir %{_libdir}/ocaml/%{srcname}/toplevel/
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

%if %{with docs}
%files doc
%doc _build/default/_doc/_html/
%doc _build/default/_doc/_mlds/
%doc _build/default/_doc/_odoc/
%license LICENSE.md
%endif

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.12.3-4
- Cleaning-up spec. License verified.

* Mon Aug 09 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.12.3-3
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Remove test, docs circular dependencies

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 0.12.3-1
- Version 0.12.3

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.12.1-5
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.12.1-4
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu May  7 2020 Jerry James <loganjerry@gmail.com> - 0.12.1-1
- Initial RPM
