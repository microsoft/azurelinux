# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-ounit
Version:        2.2.7
Release:        16%{?dist}
Summary:        Unit test framework for OCaml

License:        MIT
URL:            https://github.com/gildor478/ounit
VCS:            git:%{url}.git
Source0:        %{url}/releases/download/v%{version}/ounit-%{version}.tbz

# Remove seq and stdlib-shims downstream.  Not needed in Fedora.
Patch0001:      0001-Remove-stdlib-shims.patch

BuildRequires:  ocaml >= 4.04.0
BuildRequires:  ocaml-dune >= 3.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-lwt-devel >= 2.5.2

# The ounit name is now just an alias for ounit2
Provides:       %{name}2 = %{version}-%{release}

%description
OUnit is a unit test framework for OCaml.  It allows one to easily create
unit-tests for OCaml code.  It is loosely based on HUnit, a unit testing
framework for Haskell.  It is similar to JUnit, and other xUnit testing
frameworks.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}2-devel = %{version}-%{release}


%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.


%package        lwt
Summary:        Helper functions for building Lwt tests using OUnit
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       %{name}2-lwt = %{version}-%{release}


%description    lwt
This package contains helper functions for building Lwt tests using
OUnit.


%package        lwt-devel
Summary:        Development files for %{name}-lwt
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-lwt%{?_isa} = %{version}-%{release}
Requires:       ocaml-lwt-devel%{?_isa}
Provides:       %{name}2-lwt-devel = %{version}-%{release}


%description    lwt-devel
The %{name}-lwt-devel package contains libraries and signature
files for developing applications that use %{name}-lwt.


%prep
%autosetup -n ounit-%{version} -p1


%build
%dune_build


%check
%dune_check


%install
%dune_install -s


%files -f .ofiles-ounit2
%doc CHANGES.md README.md
%license LICENSE.txt
%dir %{ocamldir}/ounit/
%{ocamldir}/ounit/META


%files devel -f .ofiles-ounit2-devel
%{ocamldir}/ounit/dune-package
%{ocamldir}/ounit/opam


%files lwt -f .ofiles-ounit2-lwt
%dir %{ocamldir}/ounit-lwt/
%{ocamldir}/ounit-lwt/META


%files lwt-devel -f .ofiles-ounit2-lwt-devel
%{ocamldir}/ounit-lwt/dune-package
%{ocamldir}/ounit-lwt/opam


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James  <loganjerry@gmail.com> - 2.2.7-15
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 2.2.7-13
- OCaml 5.3.0 rebuild for Fedora 42

* Tue Oct 08 2024 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-12
- Rebuild for ocaml-lwt 5.8.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-10
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-9
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-6
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-5
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-4
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 2.2.7-3
- Enable tests for s390x, since timeout was increased in 2.2.3

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 2.2.7-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 2.2.7-1
- Version 2.2.7
- Verify License tag is valid SPDX
- Remove dependency on seq as well as stdlib-shims

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 2.2.6-4
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 2.2.6-2
- Bump and rebuild

* Mon Aug  8 2022 Jerry James <loganjerry@gmail.com> - 2.2.6-1
- Version 2.2.6
- Trim BRs
- Give up on using odoc to generate documentation
- Use new OCaml macros

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 2.2.4-8
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 2.2.4-7
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 05 2021 Richard W.M. Jones <rjones@redhat.com> - 2.2.4-5
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun  3 2021 Richard W.M. Jones <rjones@redhat.com> - 2.2.4-3
- Rebuild for new ocaml-lwt.

* Mon Mar  1 21:21:01 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.2.4-2
- Bump release and rebuild.

* Mon Mar  1 17:33:35 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 2.2.4-1
- New upstream version 2.2.4.
- Update patches.
- OCaml 4.12.0 build

* Mon Feb 22 2021 Jerry James <loganjerry@gmail.com> - 2.2.2-14
- Rebuild for ocaml-lwt 5.4.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-12
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-11
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-8
- Rebuild to resolve build order symbol problems.

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-7
- Patch out a failing test.
- Disable tests on s390x.

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-6
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-5
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 04 2020 Richard W.M. Jones <rjones@redhat.com> - 2.2.2-4
- Update all OCaml dependencies for RPM 4.16.

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
