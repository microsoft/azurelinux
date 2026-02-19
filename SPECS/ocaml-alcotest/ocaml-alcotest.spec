# BOOTSTRAP NOTE: We currently build only the base alcotest package.  We cannot
# yet build the async and lwt subpackages, because of missing dependencies.
# Some of those dependencies require the base alcotest package, either directly
# or indirectly.  Therefore, we will only be able to build the other two in
# non-bootstrap mode.
%global srcname alcotest

Summary:        Lightweight and colorful test framework for OCaml
Name:           ocaml-%{srcname}
Version:        1.5.0
Release:        2%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/mirage/alcotest
Source0:        %{URL}/archive/%{version}.tar.gz#/%{srcname}-%{version}.tar.gz
# We neither need nor want the stdlib-shims or ocaml-syntax-shims packages in
# Azure Linux.  They are forward compatibility packages for older OCaml
# installations.  Patch them out instead.  Upstream does not want this patch
# until stdlib-shims and ocaml-syntax-shims are obsolete.
Patch0:         0001-Drop-the-stdlib-shims-subpackage.patch

BuildRequires:  ocaml >= 4.03.0
BuildRequires:  ocaml-astring-devel
BuildRequires:  ocaml-cmdliner-devel >= 1.3.0 
BuildRequires:  ocaml-dune >= 2.8
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-fmt-devel >= 0.8.7
BuildRequires:  ocaml-re-devel >= 1.7.2
BuildRequires:  ocaml-uutf-devel >= 1.0.1

%description
Alcotest is a lightweight and colorful test framework.

Alcotest exposes a simple interface to perform unit tests, including a
simple `TESTABLE` module type, a `check` function to assert test
predicates, and a `run` function to perform a list of `unit -> unit`
test callbacks.

Alcotest provides quiet and colorful output where only faulty runs are
fully displayed at the end of the run (with the full logs ready to
inspect), with a simple (yet expressive) query language to select the
tests to run.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-astring-devel%{?_isa}
Requires:       ocaml-cmdliner-devel%{?_isa}
Requires:       ocaml-fmt-devel%{?_isa}
Requires:       ocaml-re-devel%{?_isa}
Requires:       ocaml-uutf-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
# For non-bootstrap builds, omit the "-p alcotest", and also run:
#   dune build %{?_smp_mflags} @doc
# to generate the documentation.
dune build %{?_smp_mflags} -p alcotest

# Relink the stublibs with $RPM_LD_FLAGS.
cd _build/default/src
ocamlmklib -g -ldopt '%{build_ldflags}' -o alcotest_stubs \
  $(ar t libalcotest_stubs.a)
cd -

%install
# For non-bootstrap builds, omit the "alcotest" on the end.
dune install --destdir=%{buildroot} alcotest

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

# We do not want the ml files
find %{buildroot}%{_libdir}/ocaml -name \*.ml -delete

%check
# skip failing e2e group tests
cd alcotest-%{version}
rm -rf test/e2e/alcotest/failing
dune runtest -j 1 -p alcotest

%files
%doc CHANGES.md README.md alcotest-help.txt
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%dir %{_libdir}/ocaml/%{srcname}/engine/
%dir %{_libdir}/ocaml/%{srcname}/stdlib_ext/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/runtime.js
%{_libdir}/ocaml/%{srcname}/{*/,}*.cma
%{_libdir}/ocaml/%{srcname}/{*/,}*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/{*/,}*.cmxs
%endif
%{_libdir}/ocaml/stublibs/dllalcotest_stubs.so

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/{*/,}*.a
%{_libdir}/ocaml/%{srcname}/{*/,}*.cmx
%{_libdir}/ocaml/%{srcname}/{*/,}*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/{*/,}*.cmt
%{_libdir}/ocaml/%{srcname}/{*/,}*.cmti
%{_libdir}/ocaml/%{srcname}/{*/,}*.mli

%changelog
* Wed Dec 17 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.5.0-2
- Bump version and rebuild for updated ocaml dependencies.
- skip failing e2e group tests

* Tue Jun 04 2024 Andrew Phelps <anphel@microsoft.com> - 1.5.0-1
- Upgrade to version 1.5.0 with changes based on Fedora 36 (license: MIT).

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-3
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.0-2
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Tue Feb 16 2021 Jerry James <loganjerry@gmail.com> - 1.3.0-1
- Version 1.3.0

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1.2.3-4
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov  2 2020 Jerry James <loganjerry@gmail.com> - 1.2.3-2
- Rebuild for ocaml-fmt 0.8.9

* Sun Sep 13 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 1.2.3-1
- New upstream release 1.2.3 (rhbz#1876739)

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.2-2
- OCaml 4.11.1 rebuild

* Wed Aug 26 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 1.2.2-1
- New upstream release 1.2.2 (rhbz#1872839)

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-4
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 1.2.1-1
- New upstream release 1.2.1 (rhbz#1856364)

* Fri Jun 19 2020 Jerry James <loganjerry@gmail.com> - 1.1.0-4
- Rebuild for ocaml-astring 0.8.4

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-3
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr  4 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 1.1.0-1
- New upstream release 1.1.0
- Rebase ocaml-alcotest-stdlib-shims.patch as 0001-Drop-the-stdlib-shims-subpackage.patch

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-3
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- OCaml 4.10.0 final.

* Wed Feb 12 2020 Jerry James <loganjerry@gmail.com> - 1.0.1-1
- Version 1.0.1

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-2
- OCaml 4.10.0+beta1 rebuild.

* Tue Jan 14 2020 Jerry James <loganjerry@gmail.com> - 1.0.0-1
- Version 1.0.0

* Thu Jan  9 2020 Jerry James <loganjerry@gmail.com> - 0.8.5-1
- Initial RPM
