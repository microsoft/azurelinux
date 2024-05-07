Summary:        OCaml lightweight thread library
Name:           ocaml-lwt
Version:        5.7.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://ocsigen.org/lwt
Source0:        https://github.com/ocsigen/lwt/archive/refs/tags/%{version}.tar.gz#/lwt-%{version}.tar.gz
# Fix GCC 14 incompatibilites: https://github.com/ocsigen/lwt/pull/1004
Patch0:         0001-Prepare-for-stricter-checking-in-GCC-14.patch

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-dune >= 1.8.0
BuildRequires:  ocaml-dune-configurator-devel
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-cppo >= 1.1.0
BuildRequires:  ocaml-ocplib-endian-devel
 
# lwt_react dependencies.
BuildRequires:  ocaml-react-devel >= 1.0.0
 
# lwt_ppx dependencies.
BuildRequires:  ocaml-ppxlib-devel >= 0.30.0
BuildRequires:  ocaml-ppx-let-devel
 
# optional dependencies.
BuildRequires:  libev-devel

%description
Lwt is a lightweight thread library for Objective Caml.  This library
is part of the Ocsigen project.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-ocplib-endian-devel%{?_isa}
Requires:       libev-devel%{?_isa}

# This can be removed when F43 reaches EOL
Obsoletes:      ocaml-lwt-luv-devel < 5.7.0

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        react
Summary:        Helpers for using React with Lwt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    react
Helpers for using React with Lwt.

%package        react-devel
Summary:        Development files for ocaml-lwt-react

Requires:       %{name}-react%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-react-devel%{?_isa}

%description    react-devel
The %{name}-react-devel package contains libraries and signature files for
developing applications that use %{name}-react.

%package        ppx
Summary:        PPX syntax for Lwt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    ppx
PPX syntax for Lwt, providing something similar to async/await from JavaScript.

%package        ppx-devel
Summary:        Development files for ocaml-lwt-ppx

Requires:       %{name}-ppx%{?_isa} = %{version}-%{release}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       ocaml-ppxlib-devel%{?_isa}

%description    ppx-devel
The %{name}-ppx-devel package contains libraries and signature files for
developing applications that use %{name}-ppx.

%prep
%autosetup -n lwt-%{version} -p1

# It looks like one test fails.
# Actually, it looks like all the "mcast" tests fail in koji.
# They should probably be disabled via a patch, but this works for now.
sed 's,test_mcast "mcast-join-loop" true true;,(*test_mcast "mcast-join-loop" true true;*),' -i test/unix/test_mcast.ml
sed 's,test_mcast "mcast-join-noloop" true false;,(*test_mcast "mcast-join-noloop" true false;*),' -i test/unix/test_mcast.ml
sed 's,test_mcast "mcast-nojoin-loop" false true;,(*test_mcast "mcast-nojoin-loop" false true;*),' -i test/unix/test_mcast.ml
sed 's,test_mcast "mcast-nojoin-noloop" false false;,(*test_mcast "mcast-nojoin-noloop" false false;*),' -i test/unix/test_mcast.ml

%build
# Enable libev and pthread.
dune exec src/unix/config/discover.exe -- --save \
     --use-libev true --use-pthread true
%dune_build

%install
%dune_install -s

# Remove test-only directory
rm -rf %{buildroot}%{ocamldir}/lwt_ppx_let

%check
# Disable this test on s390x.
# https://bugzilla.redhat.com/show_bug.cgi?id=1826511
%ifnarch s390x
%dune_check
%endif

%files -f .ofiles-lwt
%doc CHANGES README.md
%license LICENSE.md

%files devel -f .ofiles-lwt-devel
%doc CHANGES README.md
%license LICENSE.md

%files react -f .ofiles-lwt_react
%doc CHANGES README.md
%license LICENSE.md

%files react-devel -f .ofiles-lwt_react-devel
%doc CHANGES README.md

%files ppx -f .ofiles-lwt_ppx
%doc CHANGES README.md

%files ppx-devel -f .ofiles-lwt_ppx-devel
%doc CHANGES README.md


%changelog
* Wed May 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 5.7.0-1
- Upgrade to 5.7.0

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 5.4.1-9
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.4.1-8
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 5.4.1-7
- Initial CBL-Mariner import from Fedora 35 (license: MIT).

* Fri Aug  6 2021 Jerry James <loganjerry@gmail.com> - 5.4.1-6
- Rebuild for ocaml-luv 0.5.10

* Thu Jul 29 2021 Jerry James <loganjerry@gmail.com> - 5.4.1-5
- Rebuild for ocaml-ppxlib 0.22.2 and ocaml-luv 0.5.9

* Tue Jul 27 2021 Richard W.M. Jones <rjones@redhat.com> - 5.4.1-4
- Rebuild for changed ocamlx(Dynlink)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Jerry James <loganjerry@gmail.com> - 5.4.1-2
- Rebuild for ocaml-ppxlib 0.22.1

* Mon May 31 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 5.4.1-1
- Update to 5.4.1 (#1811637)

* Mon May 10 2021 Jerry James <loganjerry@gmail.com> - 5.4.0-3
- Rebuild for ocaml-luv 0.5.8

* Mon Mar  1 17:16:08 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 5.4.0-2
- OCaml 4.12.0 build

* Sat Feb 20 2021 Jerry James <loganjerry@gmail.com> - 5.4.0-1
- New upstream version 5.4.0
- Add luv subpackage

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 5.3.0-9
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 5.3.0-7
- Rebuild for ocaml-migrate-parsetree 1.8.0

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 5.3.0-6
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 5.3.0-5
- OCaml 4.11.0 rebuild

* Mon Aug 03 2020 Richard W.M. Jones <rjones@redhat.com> - 5.3.0-4
- Bump and rebuild to fix Dynlink dependency.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Richard W.M. Jones <rjones@redhat.com> - 5.3.0-2
- Rebuild to resolve build order symbol problems.

* Mon Jun 15 2020 Jerry James <loganjerry@gmail.com> - 5.3.0-1
- New upstream version 5.3.0

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 5.2.0-3
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 5.2.0-2
- OCaml 4.11.0 pre-release attempt 2

* Thu Apr 16 2020 Jerry James <loganjerry@gmail.com> - 5.2.0-1
- New upstream version 5.2.0
- Remove upstreamed lwt-5.1.2-bytes.patch
- Remove unneeded BRs
- Require ocaml-bisect-ppx-devel from ocaml-lwt-react-devel

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 5.1.2-4
- Update all OCaml dependencies for RPM 4.16.

* Thu Mar  5 2020 Jerry James <loganjerry@gmail.com> - 5.1.2-3
- Link the stublib with RPM_LD_FLAGS
- Add the executable bit to cmxs files
- Require libev-devel from the devel subpackage
- Require ocaml-lwt-devel from ocaml-lwt-{react,ppx}-devel
- Refactor the %files lists

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 5.1.2-2
- OCaml 4.10.0 final.

* Tue Feb 25 2020 Richard W.M. Jones <rjones@redhat.com> - 5.1.2-1
- New upstream version 5.1.2.
- Add trivial patch to fix OCaml 4.10 build.
- +BR ocaml-bisect-ppx-devel.

* Fri Jan 31 2020 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-7
- Bump release and rebuild.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-5
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-4
- Bump release and rebuild.

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 4.4.0-3
- OCaml 4.10.0+beta1 rebuild.

* Sun Jan 12 2020 Robert-André Mauchin <zebob.m@gmail.com> - 4.4.0-2
- OCaml 4.09.0 (final) rebuild.

* Tue Oct 15 2019 Ben Rosser <rosser.bjr@gmail.com> - 4.4.0-1
- Update to latest upstream release, 4.4.0 (rhbz#1755859).

* Tue Oct 01 2019 Ben Rosser <rosser.bjr@gmail.com> - 4.3.1-1
- Update to latest upstream release; reenable tests.

* Wed Aug 21 2019 Richard W.M. Jones <rjones@redhat.com> - 4.3.0-1
- New upstream version 4.3.0.
- Remove patches from git which were unused and unapplied.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-6
- Fix previous commit.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-5
- Add Requires: ocaml-seq-devel to devel subpackage.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-4
- OCaml 4.08.1 (final) rebuild.

* Wed Aug 07 2019 Ben Rosser <rosser.bjr@gmail.com> - 4.2.1-3
- Add BuildRequires on ocaml-mmap.

* Thu Aug 01 2019 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-2
- OCaml 4.08.1 (rc2) rebuild.

* Sun Jul 28 2019 Richard W.M. Jones <rjones@redhat.com> - 4.2.1-1
- New upstream version 4.2.1.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Sep 27 2018 Ben Rosser <rosser.bjr@gmail.com> - 4.1.0-1
- Updated to 4.1.0, using jbuilder/dune as buildsystem. (rhbz#1289549).
- lwt_react and lwt_ppx are now separate opam packages, built from this tarball.
- Split lwt_react and lwt_ppx into ocaml-lwt-react and ocaml-lwt-ppx subpackages.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-20
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-19
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-17
- OCaml 4.06.0 rebuild.

* Tue Oct 03 2017 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-16
- Rebuild against new ocaml-ssl.

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-15
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-11
- Bump release and rebuild.

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-10
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-9
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 2.5.0-7
- rebuild for s390x codegen bug

* Mon Nov 07 2016 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-6
- Rebuild for OCaml 4.04.0.
- Add explicit dependency on ocamlbuild.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug  2 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 2.5.0-4
- Re-enable React (fixes bz# 1249307)

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-3
- OCaml 4.02.3 rebuild.

* Fri Jul 24 2015 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-2
- Enable building the syntax extension.
- Fix Source URL.

* Wed Jul 22 2015 Richard W.M. Jones <rjones@redhat.com> - 2.5.0-1
- New version 2.5.0.
- Enable bytecode builds.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 2.4.5-6
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2.4.5-5
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 2.4.5-4
- ocaml-4.02.1 rebuild.

* Sun Aug 31 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.5-3
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.5-2
- ocaml-4.02.0+rc1 rebuild.

* Mon Aug 18 2014 Scott Tsai <scottt.tw@gmail.com> 2.4.5-1
- New upstream version 2.4.5 (tarball created from tag through github https://github.com/ocsigen/lwt/tags)
- Remove patches which are now upstream.
- Disable ocaml-react support since it breaks the build (https://github.com/ocsigen/lwt/issues/77)
- Remove manual.pdf for now since tarballs from git tags don't include the pre-built documentation

* Mon Aug 18 2014 Scott Tsai <scottt.tw@gmail.com> - 2.4.3-12
- Add lwt-fix-ocaml-camlp4-19.patch to fix OCaml 4.02+ build failure
- Rebuild for ocaml-4.02.0-0.8.git10e45753.fc22.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 09 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-10
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-9
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-7
- Remove ocaml_arches macro (RHBZ#1087794).

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-6
- Remove ocaml_arches macro (RHBZ#1087794).

* Fri Jan  3 2014 Richard W.M. Jones <rjones@redhat.com> - 2.4.3-5
- Enable lwt.react support, and check it gets enabled (RHBZ#1048367).
- Remove libev patch since headers are back to normal location
  in libev >= 4.15-3.

* Wed Sep 18 2013 Jerry James <loganjerry@gmail.com> - 2.4.3-4
- Rebuild for OCaml 4.01.0, and add -ocaml41 patch to adapt to changes
- Enable debuginfo
- Enable glib integration
- Add check script
- Add manual to -devel subpackage
- Minor spec file cleanups

* Sat Sep 14 2013 Scott Tsai <scottt.tw@gmail.com> - 2.4.3-3
- New upstream version 2.4.3

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.4.2-1
- New upstream version 2.4.2.
- Rebuild for OCaml 4.00.1.
- Remove patches which are now upstream.
- Clean up spec file.

* Mon Jul 30 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-7
- Rebuild for OCaml 4.00.0 official.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Scott Tsai <scottt.tw@gmail.com> - 2.3.2-5
- Patch myocamlobuild.ml in lwt-2.3.2-ocaml-4.patch to
  add compiler-libs to search patch for "Toploop".
- Add oasis-common.patch to make setup.ml work on OCaml 4.00.0
- Both patches from https://sympa.inria.fr/sympa/arc/caml-list/2012-05/msg00223.html

* Mon Jun 11 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-4
- Patch for OCaml 4.00.0.

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-3
- Rebuild for OCaml 4.00.0.

* Sat Jan 07 2012 Richard W.M. Jones <rjones@redhat.com> - 2.3.2-2
- Rebuild for OCaml 3.12.1.

* Thu Dec 08 2011 Scott Tsai scottt.tw@gmail.com - 2.3.2-1
- New upstream version 2.3.2. 

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 2.2.0-1
- New upstream version 2.2.0.
- Rebuild for OCaml 3.12.0.
- Add BR libev-devel.
- Patch <ev.h> -> <libev/ev.h>
- *.cmx files are no longer being distributed.
- No VERSION file.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-0.3.rc1
- Rebuild for OCaml 3.11.2.

* Mon Oct 12 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-0.2.rc1.fc13
- ocaml-react is now in Fedora, so build this package.
- Missing BR on camlp4.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 2.0.0-0.rc1.fc13
- New upstream version 2.0.0+rc1.
- NB. This cannot be built as it depends on new package ocaml-react
  (RHBZ#527971).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-5
- Rebuild for OCaml 3.11.1

* Thu Apr 16 2009 S390x secondary arch maintainer <fedora-s390x@lists.fedoraproject.org>
- ExcludeArch sparc64, s390, s390x as we don't have OCaml on those archs
  (added sparc64 per request from the sparc maintainer)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-3
- Rebuild.

* Wed Sep  3 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-2
- Rebuild with higher EVR than F-9 branch.

* Mon Sep  1 2008 Richard W.M. Jones <rjones@redhat.com> - 1.1.0-1
- Initial RPM release.
