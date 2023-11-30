%global srcname ounit

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

# -doc subpackage requires ocaml-odoc which has rather a lot of
# dependencies.  This flag allows the non-essential subpackage to be
# enabled.
%bcond_with doc

Summary:        Unit test framework for OCaml
Name:           ocaml-%{srcname}
Version:        2.2.2
Release:        7%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/gildor478/ounit
Source0:        %{url}/releases/download/v%{version}/%{srcname}-v%{version}.tbz
# We neither need nor want the stdlib-shims package.  It is a forward
# compatibility package for older OCaml installations.  Patch it out instead.
# Upstream does not want this patch until stdlib-shims is obsolete.
Patch0:         %{name}-stdlib-shims.patch
# Enable ocaml 4.13 compatibility. Source: Fedora 35
# https://src.fedoraproject.org/rpms/ocaml-ounit/blob/f35/f/ounit-v2.2.4-remove-Thread-kill.patch
Patch1:         remove-thread-kill.patch
# Fix backtrace parsing with ocaml>=4.11. Source: Upstreamed in 2.2.3
# https://github.com/gildor478/ounit/commit/2a9acf70aeb0f47de5a7c7c07129235a5f2ac0f0
Patch2:         fix-backtrace-parser.patch

# I believe this is actually caused by a missing Requires in another
# package (perhaps lwt?).  In any case without this the tests fail to
# compile with:
# /usr/bin/ld: cannot find -lev
BuildRequires:  libev-devel
BuildRequires:  ocaml >= 4.02.3
BuildRequires:  ocaml-dune >= 1.11.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-lwt-devel
BuildRequires:  ocaml-mmap-devel
BuildRequires:  ocaml-ocplib-endian-devel
BuildRequires:  ocaml-result-devel

%if %{with doc}
BuildRequires:  ocaml-odoc
%endif

# The ounit name is now just an alias for ounit2
Provides:       %{name}2 = %{version}-%{release}

%description
OUnit is a unit test framework for OCaml.  It allows one to easily create
unit-tests for OCaml code.  It is loosely based on HUnit, a unit testing
framework for Haskell.  It is similar to JUnit, and other xUnit testing
frameworks.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}2-devel = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        lwt
Summary:        Helper functions for building Lwt tests using OUnit
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}2-lwt = %{version}-%{release}

%description    lwt
This package contains helper functions for building Lwt tests using
OUnit.

%package        lwt-devel
Summary:        Development files for %{name}-lwt
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-lwt = %{version}-%{release}
Requires:       ocaml-lwt-devel%{?_isa}
Provides:       %{name}2-lwt-devel = %{version}-%{release}

%description    lwt-devel
The %{name}-lwt-devel package contains libraries and signature
files for developing applications that use %{name}-lwt.

%package        doc
Summary:        Documentation for %{name}
BuildArch:      noarch

%description    doc
Documentation for %{name}.

%prep
%autosetup -n %{srcname}-v%{version} -p1

%build
dune build %{?_smp_mflags}
%if %{with doc}
dune build %{?_smp_mflags} @doc
%endif

%check
dune runtest

%install
dune install --destdir=%{buildroot}

%if %{with doc}
# We do not want the dune markers
find _build/default/_doc/_html -name .dune-keep -delete
%endif

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%ifarch %{ocaml_native_compiler}
# Add missing executable bits
find %{buildroot}%{_libdir}/ocaml -name \*.cmxs -exec chmod a+x {} \+
%endif

%files
%doc CHANGES.md README.md
%license LICENSE.txt
%dir %{_libdir}/ocaml/%{srcname}/
%dir %{_libdir}/ocaml/%{srcname}2/
%dir %{_libdir}/ocaml/%{srcname}2/advanced/
%dir %{_libdir}/ocaml/%{srcname}2/threads/
%{_libdir}/ocaml/%{srcname}2/threads/.private/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}2/META
%{_libdir}/ocaml/%{srcname}2/*.cma
%{_libdir}/ocaml/%{srcname}2/*.cmi
%{_libdir}/ocaml/%{srcname}2/*/*.cma
%{_libdir}/ocaml/%{srcname}2/*/*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}2/*.cmxs
%{_libdir}/ocaml/%{srcname}2/*/*.cmxs
%endif

%files devel
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%{_libdir}/ocaml/%{srcname}2/dune-package
%{_libdir}/ocaml/%{srcname}2/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}2/*.a
%{_libdir}/ocaml/%{srcname}2/*.cmx
%{_libdir}/ocaml/%{srcname}2/*.cmxa
%{_libdir}/ocaml/%{srcname}2/*/*.a
%{_libdir}/ocaml/%{srcname}2/*/*.cmx
%{_libdir}/ocaml/%{srcname}2/*/*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}2/*.cmt
%{_libdir}/ocaml/%{srcname}2/*.cmti
%{_libdir}/ocaml/%{srcname}2/*.ml
%{_libdir}/ocaml/%{srcname}2/*.mli
%{_libdir}/ocaml/%{srcname}2/*/*.cmt
%{_libdir}/ocaml/%{srcname}2/*/*.cmti
%{_libdir}/ocaml/%{srcname}2/*/*.ml
%{_libdir}/ocaml/%{srcname}2/*/*.mli

%files lwt
%dir %{_libdir}/ocaml/%{srcname}-lwt/
%dir %{_libdir}/ocaml/%{srcname}2-lwt/
%{_libdir}/ocaml/%{srcname}-lwt/META
%{_libdir}/ocaml/%{srcname}2-lwt/META
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.cma
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.cmxs
%endif

%files lwt-devel
%{_libdir}/ocaml/%{srcname}-lwt/dune-package
%{_libdir}/ocaml/%{srcname}-lwt/opam
%{_libdir}/ocaml/%{srcname}2-lwt/dune-package
%{_libdir}/ocaml/%{srcname}2-lwt/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.a
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.cmx
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.cmxa
%endif
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.cmt
%{_libdir}/ocaml/%{srcname}2-lwt/oUnitLwt.ml

%if %{with doc}
%files doc
%doc _build/default/_doc/_html/
%doc _build/default/_doc/_mlds/
%doc _build/default/_doc/_odoc/
%license LICENSE.txt
%endif

%changelog
* Thu Nov 30 2023 Olivia Crain <oliviacrain@microsoft.com> - 2.2.2-7
- Add upstream patch to fix backtrace parser test

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.2-6
- Cleaning-up spec. License verified.

* Tue Jan 18 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.2.2-5
- Take Fedora patch (license: MIT) to fix building with OCaml 4.13.0
- License verified

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.2.2-4
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 28 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-3.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-3
- OCaml 4.10.0 final.
- Make -doc subpackage optional, disabled for now.

* Fri Feb  7 2020 Jerry James <loganjerry@gmail.com> - 2.2.2-1
- New upstream version 2.2.2
- New URLs

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-13
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-12
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-11
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-10
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-9
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-7
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-6
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-3
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 2.0.8-2
- OCaml 4.07.0-rc1 rebuild.

* Tue Apr 10 2018 Ding-Yi Chen <dchen@redhat.com> - 2.0.8-1
- New upstream version 2.0.8.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 2.0.6-1
- New upstream version 2.0.6.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-28
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-27
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-24
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-23
- Bump release and rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-22
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 2.0.0-20
- rebuild for s390x codegen bug

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-19
- Add dependency on ocamlbuild.

* Mon Sep 12 2016 Dan Horák <dan[at]danny.cz> - 2.0.0-18
- disable debuginfo subpackage on interpreted builds

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-16
- OCaml 4.02.3 rebuild.

* Mon Jul 27 2015 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-15
- Remove ExcludeArch since bytecode build should now work.

* Tue Jun 23 2015 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-14
- Bump release and rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-13
- ocaml-4.02.2 rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-12
- Bump release and rebuild.

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-11
- ocaml-4.02.1 rebuild.

* Mon Jan 26 2015 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-10
- Fix Source URL.
- Rebuild against OCaml to fix "make inconsistent assumptions over
  implementation Arg".

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-9
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-8
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-6
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Thu Jul 17 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-5
- OCaml 4.02.0 beta rebuild.

* Mon Jul 14 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-4
- Remove workaround for code gen bug and try building against
  possibly fixed compiler.

* Sun Jul 13 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-3
- Add workaround for code generator bug on ARM (RHBZ#1119049).

* Sat Jul 12 2014 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-1
- New upstream version 2.0.0.
- Remove BR on camlp4.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Feb 14 2014 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-8
- Rebuild for updated Arg module (RHBZ#1065447).

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-7
- Rebuild for OCaml 4.01.0.
- Enable debuginfo.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 19 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-4
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-3
- Bump and rebuild against new OCaml 4.00.0 official release.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 30 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- New upstream version 1.1.2, fixed for OCaml 4.00.0.

* Sat Jun 09 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-6
- Rebuild for OCaml 4.00.0.

* Mon May 14 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-5
- Bump release and rebuild for new OCaml on ARM.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-4
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- New upstream version 1.1.0.
- Project has moved to new upstream URL and Source0.
- Rebuild for OCaml 3.12.0.
- New build system:
    + doesn't need 'make allopt'
    + DESTDIR logic changed (see OASIS bug 852)
    + docdir moved
- LICENSE and README files renamed.
- BR camlp4.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-7
- Rebuild for OCaml 3.11.2.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-3
- Rebuild for OCaml 3.11.0+rc1.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- Rebuild for OCaml 3.11.0

* Sun Aug 31 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-1
- New upstream version 1.0.3.

* Mon May 12 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-2
- License is MIT.

* Sat May  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-1
- Initial RPM release.
