%global srcname bisect-ppx

%global upname  bisect_ppx
%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Summary:        Code coverage for OCaml and Reason
Name:           ocaml-%{srcname}
Version:        2.6.3
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://aantron.github.io/bisect_ppx/
Source0:        https://github.com/aantron/%{upname}/archive/%{version}/%{upname}-%{version}.tar.gz

BuildRequires:  git-core
BuildRequires:  ocaml >= 4.02.0
BuildRequires:  ocaml-cmdliner-devel >= 1.0.0
BuildRequires:  ocaml-dune >= 2.7.0
BuildRequires:  ocaml-ppxlib-devel >= 0.21.0

Provides:       %{name}-doc = %{version}-%{release}

%description
Bisect_ppx is a code coverage tool for OCaml.  It helps you test
thoroughly by showing which parts of your code are *not* tested.  It is
a small preprocessor that inserts instrumentation at places in your
code, such as if-then-else and match expressions.  After you run tests,
Bisect_ppx gives a nice HTML report showing which places were visited
and which were missed.

Usage is simple - add package bisect_ppx when building tests, run your
tests, then run the Bisect_ppx report tool on the generated visitation
files.

%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-ppxlib-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{upname}-%{version}

%build
dune build %{?_smp_mflags} @install

%install
dune install --destdir=%{buildroot}

# Install the man page
mkdir -p %{buildroot}%{_mandir}/man1
_build/install/default/bin/bisect-ppx-report --help groff > \
  %{buildroot}%{_mandir}/man1/bisect-ppx-report.1

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

# We do not want the ml files
find %{buildroot}%{_libdir}/ocaml -name \*.ml -delete

%files
%doc doc/advanced.md doc/CHANGES README.md
%license LICENSE.md
%{_bindir}/bisect-ppx-report
%{_mandir}/man1/bisect-ppx-report.1*
%dir %{_libdir}/ocaml/%{upname}/
%dir %{_libdir}/ocaml/%{upname}/common/
%dir %{_libdir}/ocaml/%{upname}/runtime/
%{_libdir}/ocaml/%{upname}/META
%{_libdir}/ocaml/%{upname}/ppx.exe
%{_libdir}/ocaml/%{upname}/%{upname}.cma
%{_libdir}/ocaml/%{upname}/%{upname}*.cmi
%{_libdir}/ocaml/%{upname}/common/bisect_common.cma
%{_libdir}/ocaml/%{upname}/common/bisect_common.cmi
%{_libdir}/ocaml/%{upname}/runtime/bisect.cma
%{_libdir}/ocaml/%{upname}/runtime/bisect*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{upname}/%{upname}.cmxs
%{_libdir}/ocaml/%{upname}/common/bisect_common.cmxs
%{_libdir}/ocaml/%{upname}/runtime/bisect.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{upname}/dune-package
%{_libdir}/ocaml/%{upname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{upname}/%{upname}.a
%{_libdir}/ocaml/%{upname}/%{upname}*.cmx
%{_libdir}/ocaml/%{upname}/%{upname}.cmxa
%{_libdir}/ocaml/%{upname}/common/bisect_common.a
%{_libdir}/ocaml/%{upname}/common/bisect_common.cmx
%{_libdir}/ocaml/%{upname}/common/bisect_common.cmxa
%{_libdir}/ocaml/%{upname}/runtime/bisect.a
%{_libdir}/ocaml/%{upname}/runtime/bisect*.cmx
%{_libdir}/ocaml/%{upname}/runtime/bisect.cmxa
%endif
%{_libdir}/ocaml/%{upname}/%{upname}*.cmt
%{_libdir}/ocaml/%{upname}/%{upname}*.cmti
%{_libdir}/ocaml/%{upname}/*.mli
%{_libdir}/ocaml/%{upname}/common/bisect_common.cmt
%{_libdir}/ocaml/%{upname}/common/bisect_common.cmti
%{_libdir}/ocaml/%{upname}/common/bisect_common.mli
%{_libdir}/ocaml/%{upname}/runtime/bisect*.cmt
%{_libdir}/ocaml/%{upname}/runtime/bisect*.cmti
%{_libdir}/ocaml/%{upname}/runtime/*.mli

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.3-3
- Cleaning-up spec. License verified.

* Mon Aug 09 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.6.3-2
- Initial CBL-Mariner import from Fedora 35 (license: MIT).
- Remove test, docs circular dependencies

* Thu Jul 29 2021 Jerry James <loganjerry@gmail.com> - 2.6.3-1
- Version 2.6.3

* Tue Jul 27 2021 Richard W.M. Jones <rjones@redhat.com> - 2.6.2-3
- Rebuild for changed ocamlx(Dynlink)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 20 2021 Jerry James <loganjerry@gmail.com> - 2.6.2-1
- Version 2.6.2

* Tue Jun 22 2021 Jerry James <loganjerry@gmail.com> - 2.6.1-2
- Rebuild for ocaml-ppxlib 0.22.1

* Tue May  4 2021 Jerry James <loganjerry@gmail.com> - 2.6.1-1
- Version 2.6.1

* Mon Mar  1 16:58:04 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.6.0-2
- OCaml 4.12.0 build

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 2.6.0-1
- Version 2.6.0

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-4
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 2.5.0-2
- Rebuild for ocaml-migrate-parsetree 1.8.0

* Fri Oct 23 2020 Jerry James <loganjerry@gmail.com> - 2.5.0-1
- Version 2.5.0
- Building documentation with ocamldoc no longer works

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-6
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-5
- OCaml 4.11.0 rebuild

* Mon Aug 03 2020 Richard W.M. Jones <rjones@redhat.com> - 2.4.1-4
- Bump and rebuild to fix Location dependency.

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 2.4.1-1
- New upstream release 2.4.1

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-3
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-2
- OCaml 4.11.0 pre-release attempt 2

* Sun Apr 19 2020 Jerry James <loganjerry@gmail.com> - 2.3.2-1
- Version 2.3.2

* Thu Apr 16 2020 Jerry James <loganjerry@gmail.com> - 2.3.1-1
- Version 2.3.1
- Add conditional for building documentation with odoc

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-5.20200106.b2661bf
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-4.20200106.b2661bf
- OCaml 4.10.0 final.
- Disable the tests to avoid circular dependency.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3.20200106.b2661bf
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-2.20200106.b2661bf
- OCaml 4.10.0+beta1 rebuild.

* Wed Jan  8 2020 Jerry James <loganjerry@gmail.com> - 1.4.1-1.20200106.b2661bf
- Initial RPM
