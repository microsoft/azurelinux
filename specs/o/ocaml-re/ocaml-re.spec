# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

# This package is needed to build lwt, which is used to build ounit, but this
# package needs ounit to run its tests.  Break the dependency cycle here.
%bcond test 0

Name:           ocaml-re
Version:        1.13.3
Release: 6%{?dist}
Summary:        A regular expression library for OCaml

License:        LGPL-2.1-or-later WITH OCaml-LGPL-linking-exception
URL:            https://github.com/ocaml/ocaml-re
VCS:            git:%{url}.git
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# Fedora's OCaml is new enough that we don't need the seq compatibility library
Patch:          ocaml-re-remove-seq.patch

BuildRequires:  ocaml
BuildRequires:  ocaml-dune

%if %{with test}
BuildRequires:  ocaml-ounit-devel
%endif

%description
A pure OCaml regular expression library. Supports Perl-style regular
expressions, Posix extended regular expressions, Emacs-style regular
expressions, and shell-style file globbing.  It is also possible to
build regular expressions by combining simpler regular expressions.
There is also a subset of the PCRE interface available in the Re.pcre
library.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
%dune_build

%install
%dune_install

%if %{with test}
%check
%dune_check
%endif

%files -f .ofiles
%doc CHANGES.md
%doc README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 1.13.3-4
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 1.13.3-2
- OCaml 5.3.0 rebuild for Fedora 42
- Add VCS field
- Use %%bcond instead of %%bcond_with

* Thu Oct 03 2024 Richard W.M. Jones <rjones@redhat.com> - 1.13.3-1
- Rebase to 1.13.3 (RHBZ#2316157)

* Wed Oct 02 2024 Richard W.M. Jones <rjones@redhat.com> - 1.13.0-1
- Rebase to 1.13.0 (RHBZ#2232846)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-8
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-7
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-4
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-3
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.11.0-2
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 1.11.0-1
- Version 1.11.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.10.4-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.10.4-1
- Version 1.10.4
- Convert License tag to SPDX
- Use new dune macros

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.10.3-8
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.10.3-5
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.10.3-4
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.10.3-2
- OCaml 4.13.1 build

* Mon Oct  4 2021 Richard W.M. Jones <rjones@redhat.com> - 1.10.3-1
- New upstream version 1.10.3

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar  1 13:18:58 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-20
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-18
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-17
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-16
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-14
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-13
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-12
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-11
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-9
- OCaml 4.10.0+beta1 rebuild.

* Fri Jan 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-8
- Make devel subpackage depend on ocaml-seq-devel (RHBZ#1792031).

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-7
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-6
- OCaml 4.08.1 (final) rebuild.

* Thu Aug  1 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-5
- Add BR ocaml-seq (RHBZ#1735476).

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.0-3
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Ben Rosser <rosser.bjr@gmail.com> - 1.9.0-1
- Updated to latest upstream release (rhbz#1550761).

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-4
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7.3-3
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Ben Rosser <rosser.bjr@gmail.com> - 1.7.3-1
- Update to 1.7.3, switch to jbuilder.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.1-5
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7.1-4
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 02 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7.1-2
- OCaml 4.06.0 rebuild.

* Tue Aug 15 2017 Ben Rosser <rosser.bjr@gmail.com> - 1.7.1-1
- Update to latest ocaml-re release.
- Use configure script directly in build section.
- Do parallel build using smp_flags macro.

* Thu Sep 3 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.4.1-1
- New upstream release
- Remove upstreamed patch

* Tue Feb 24 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.2.2-4
- Fix missing 'isa' macro in devel depends

* Sat Jan 24 2015 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.2.2-3
- Change patch filename to have .patch suffix
- Remove whitespace

* Fri Dec 12 2014 Jon Ludlam <jonathan.ludlam@citrix.com> - 1.2.2-2
- Minor updates to the SPEC file. Now rpmlint gives no errors.

* Sat Jun  7 2014 David Scott <dave.scott@citrix.com> - 1.2.2-1
- Update to 1.2.2

* Fri May 30 2014 Euan Harris <euan.harris@citrix.com> - 1.2.1-2
- Split files correctly between base and devel packages

* Thu May 30 2013 David Scott <dave.scott@eu.citrix.com> - 1.2.1-1
- Initial package

