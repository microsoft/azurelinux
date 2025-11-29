# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

# To build all parts of alcotest requires the async, js_of_ocaml, and lwt
# packages.  The async package in particular requires many packages that test
# with alcotest.  We build only the base alcotest package to break the circular
# dependency.
%bcond async 0

%global srcname alcotest
%global giturl  https://github.com/mirage/alcotest

Name:           ocaml-%{srcname}
Version:        1.9.1
Release:        3%{?dist}
Summary:        Lightweight and colorful test framework for OCaml
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        ISC
URL:            https://mirage.github.io/alcotest/
VCS:            git:%{giturl}.git
Source:         %{giturl}/archive/%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
# We neither need nor want the stdlib-shims or ocaml-syntax-shims packages in
# Fedora.  They are forward compatibility packages for older OCaml
# installations.  Patch them out instead.  Upstream does not want this patch
# until stdlib-shims and ocaml-syntax-shims are obsolete.
Patch:          0001-Drop-the-stdlib-shims-subpackage.patch

BuildRequires:  ocaml >= 4.08.0
BuildRequires:  ocaml-astring-devel
BuildRequires:  ocaml-cmdliner-devel >= 1.2.0
BuildRequires:  ocaml-dune >= 3.0
BuildRequires:  ocaml-fmt-devel >= 0.8.7
BuildRequires:  ocaml-re-devel >= 1.7.2
BuildRequires:  ocaml-uutf-devel >= 1.0.1

%if %{with async}
BuildRequires:  js-of-ocaml-compiler-devel >= 3.11.0
BuildRequires:  ocaml-async-devel >= 0.16.0
BuildRequires:  ocaml-async-kernel-devel
BuildRequires:  ocaml-async-unix-devel >= 0.16.0
BuildRequires:  ocaml-base-devel
BuildRequires:  ocaml-core-devel >= 0.16.0
BuildRequires:  ocaml-core-unix-devel >= 0.16.0
BuildRequires:  ocaml-logs-devel
BuildRequires:  ocaml-lwt-devel
%endif

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

%if %{with async}
Requires:       ocaml-async-devel
Requires:       ocaml-lwt-devel
%endif

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
%dune_build %{!?with_async:-p alcotest}

%install
%dune_install %{!?with_async:alcotest}

%check
%dune_check %{!?with_async:-p alcotest}

%files -f .ofiles
%doc CHANGES.md README.md alcotest-help.txt
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Fri Nov 28 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.9.1-3
- Initial Azure Linux import from Fedora 44 (license: MIT)
- License Verified

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-2
- OCaml 5.4.0 rebuild

* Mon Oct 13 2025 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-1
- ocaml alcotest 1.9.1 (RHBZ#2400687)

* Mon Aug 25 2025 Jerry James <loganjerry@gmail.com> - 1.9.0-4
- Rebuild for ocaml-fmt 0.11.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jul 12 2025 Jerry James <loganjerry@gmail.com> - 1.9.0-2
- Rebuild to fix OCaml dependencies

* Thu Mar 20 2025 Jerry James <loganjerry@gmail.com> - 1.9.0-1
- Version 1.9.0

* Fri Mar 14 2025 Jerry James <loganjerry@gmail.com> - 1.8.0-7
- Rebuild for ocaml-uutf 1.0.4

* Mon Mar 10 2025 Jerry James <loganjerry@gmail.com> - 1.8.0-6
- Rebuild for ocaml-fmt 0.10.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Jerry James <loganjerry@gmail.com> - 1.8.0-4
- OCaml 5.3.0 rebuild for Fedora 42

* Tue Oct 08 2024 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-3
- Rebuild for ocaml-lwt 5.8.0

* Thu Oct 03 2024 Richard W.M. Jones <rjones@redhat.com> - 1.8.0-2
- Rebuild against ocaml-re 1.13.3

* Thu Jul 25 2024 Jerry James <loganjerry@gmail.com> - 1.8.0-1
- Version 1.8.0
- Drop upstreamed bytecode-only and OCaml 5.2 patches

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-11
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-10
- OCaml 5.2.0 for Fedora 41

* Thu May 23 2024 Jerry James <loganjerry@gmail.com> - 1.7.0-9
- Add upstream patch to adapt tests to OCaml 5.2.0 output
- Minor spec file cleanups

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-7
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-6
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-5
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.7.0-3
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.7.0-2
- OCaml 5.0.0 rebuild
- Add upstream patch to fix bytecode build

* Tue Mar 21 2023 Jerry James <loganjerry@gmail.com> - 1.7.0-1
- Version 1.7.0

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.6.0-3
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 20 2022 Jerry James <loganjerry@gmail.com> - 1.6.0-1
- Version 1.6.0
- Optionally build with lwt, js, and async support

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 1.5.0-5
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-5
- OCaml 4.14.0 rebuild

* Mon Feb 28 2022 Jerry James <loganjerry@gmail.com> - 1.5.0-4
- Rebuild for ocaml-uutf 1.0.3
- Drop unnecessary ocaml-uuidm BR

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 12 2021 Jerry James <loganjerry@gmail.com> - 1.5.0-1
- Version 1.5.0

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-3
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Apr 14 2021 Jerry James <loganjerry@gmail.com> - 1.4.0-1
- Version 1.4.0

* Mon Mar  1 14:32:28 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.3.0-2
- OCaml 4.12.0 build

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

