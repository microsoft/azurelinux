%global srcname luv

# Documentation adds a circular dependency, so by
# default we build without.
%bcond_with doc

Summary:        OCaml binding to libuv for cross-platform asynchronous I/O
Name:           ocaml-%{srcname}
Version:        0.5.10
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/aantron/luv
Source0:        %{url}/releases/download/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.02.0
BuildRequires:  ocaml-alcotest-devel >= 0.8.1
BuildRequires:  ocaml-ctypes-devel >= 0.14.0
BuildRequires:  ocaml-dune >= 2.0.0
BuildRequires:  ocaml-result-devel
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(libuv)

%if %{with doc}
BuildRequires:  ocaml-odoc
%endif

%description
Luv is a binding to libuv, the cross-platform C library that does
asynchronous I/O in Node.js and runs its main loop.

Besides asynchronous I/O, libuv also supports multiprocessing and
multithreading.  Multiple event loops can be run in different threads.
Libuv also exposes a lot of other functionality, amounting to a full OS
API, and an alternative to the standard module Unix.

%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-ctypes-devel%{?_isa}
Requires:       ocaml-result-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%if %{with doc}
%package        doc
Summary:        Documentation for %{name}

BuildArch:      noarch

%description    doc
The %{name}-doc package contains developer documentation for
%{name}.
%endif

%prep
%autosetup -n %{srcname}-%{version}

# Remove spurious executable bits
find . -type f -exec chmod 0644 {} +

%build
export LUV_USE_SYSTEM_LIBUV=yes
dune build %{?_smp_mflags}
%if %{with doc}
dune build %{?_smp_mflags} @doc
%endif

# Relink the stublibs with Mariner flags
cd _build/default/src/c
ocamlmklib -g -ldopt "%{build_ldflags}" -o luv_c_stubs \
  $(ar t libluv_c_stubs.a) -luv
cd -
cd _build/default/src/unix
ocamlmklib -g -ldopt "%{build_ldflags}" -o luv_unix_stubs \
  $(ar t libluv_unix_stubs.a)
cd -

%install
dune install --destdir=%{buildroot}

%if %{with doc}
# We do not want the dune markers
find _build/default/_doc/_html -name .dune-keep -delete
%endif

# We do not want the ml files
find %{buildroot}%{_libdir}/ocaml -name \*.ml -delete

# We do not want the bundled libuv headers
rm -fr %{buildroot}%{_libdir}/ocaml/luv/uv{,.h}

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%check
dune runtest

%files
%license LICENSE.md
%doc README.md
%dir %{_libdir}/ocaml/luv/
%dir %{_libdir}/ocaml/luv/c/
%dir %{_libdir}/ocaml/luv/c_function_descriptions/
%dir %{_libdir}/ocaml/luv/c_type_descriptions/
%dir %{_libdir}/ocaml/luv_unix/
%{_libdir}/ocaml/luv{,_unix}/META
%{_libdir}/ocaml/luv{,_unix}/{,*/}*.cma
%{_libdir}/ocaml/luv{,_unix}/{,*/}*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/luv{,_unix}/{,*/}*.cmxs
%endif
%{_libdir}/ocaml/stublibs/dllluv_c_stubs.so
%{_libdir}/ocaml/stublibs/dllluv_unix_stubs.so

%files devel
%{_libdir}/ocaml/luv{,_unix}/dune-package
%{_libdir}/ocaml/luv{,_unix}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/luv{,_unix}/{,*/}*.a
%{_libdir}/ocaml/luv{,_unix}/{,*/}*.cmx
%{_libdir}/ocaml/luv{,_unix}/{,*/}*.cmxa
%endif
%{_libdir}/ocaml/luv{,_unix}/{,*/}*.cmt
%{_libdir}/ocaml/luv{,_unix}/*.cmti
%{_libdir}/ocaml/luv{,_unix}/*.mli

%if %{with doc}
%files doc
%doc _build/default/_doc/*
%endif

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.10-3
- Cleaning-up spec. License verified.

* Mon Aug 09 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.5.10-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Remove docs circular dependency by building docs conditionally

* Fri Aug  6 2021 Jerry James <loganjerry@gmail.com> - 0.5.10-1
- Version 0.5.10
- Drop -32bit patch, fixed upstream

* Thu Jul 29 2021 Jerry James <loganjerry@gmail.com> - 0.5.9-1
- Version 0.5.9
- ESOCKTNOSUPPORT is unavailable on 32-bit systems due to integer overflow

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 26 2021 Jerry James <loganjerry@gmail.com> - 0.5.8-2
- Rebuild for ocaml-ctypes 0.19.1

* Mon May 10 2021 Jerry James <loganjerry@gmail.com> - 0.5.8-1
- Version 0.5.8

* Mon Mar  1 15:16:17 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.5.7-2
- OCaml 4.12.0 build
- Make the -doc subpackage conditional.

* Wed Feb 17 2021 Jerry James <loganjerry@gmail.com> - 0.5.7-1
- Version 0.5.7

* Tue Feb 09 2021 Jerry James <loganjerry@gmail.com> - 0.5.6-1
- Initial package
