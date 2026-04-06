# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

Name:           ocaml-astring
Version:        0.8.5
Release:        30%{?dist}
Summary:        Alternative String module for OCaml

License:        ISC
URL:            https://erratique.ch/software/astring
VCS:            git:https://erratique.ch/repos/astring/.git
Source:         https://github.com/dbuenzli/astring/archive/v%{version}/astring-%{version}.tar.gz

# Adapt to changed behavior of Char.compare in OCaml 5.
# This affects x86_64, but not bytecode-only architectures.
Patch:          %{name}-ocaml5.patch

BuildRequires:  ocaml >= 4.05.0
BuildRequires:  ocaml-compiler-libs
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-rpm-macros
BuildRequires:  ocaml-topkg-devel

# Do not require ocaml-compiler-libs at runtime
%global __ocaml_requires_opts -i Asttypes -i Build_path_prefix_map -i Cmi_format -i Env -i Format_doc -i Ident -i Identifiable -i Load_path -i Location -i Longident -i Misc -i Oprint -i Outcometree -i Parsetree -i Path -i Primitive -i Shape -i Subst -i Toploop -i Type_immediacy -i Types -i Unit_info -i Warnings

%description
Astring exposes an alternative `String` module for OCaml.  This module
tries to balance minimality and expressiveness for basic, index-free,
string processing and provides types and functions for substrings,
string sets and string maps.

Remaining compatible with the OCaml `String` module is a non-goal.  The
`String` module exposed by Astring has exception safe functions,
removes deprecated and rarely used functions, alters some signatures
and names, adds a few missing functions and fully exploits OCaml's
newfound string immutability.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -N -n astring-%{version}
%ifarch %{ocaml_native_compiler}
%autopatch -p1
%endif

%conf
# Topkg does watermark replacements only if run inside a git checkout.  Github
# tarballs do not come with a .git directory.  Therefore, we do the watermark
# replacement manually.
for fil in $(find . -type f); do
  sed -e 's,%%%%NAME%%%%,astring,' \
      -e 's,%%%%PKG_HOMEPAGE%%%%,%{url},' \
      -e 's,%%%%VERSION%%%%,v%{version},' \
      -e 's,%%%%VERSION_NUM%%%%,%{version},' \
      -i.orig $fil
  touch -r $fil.orig $fil
  rm $fil.orig
done

%build
# Build the library and the tests
ocaml pkg/pkg.ml build --tests true

%install
%ocaml_install

%check
ocaml pkg/pkg.ml test

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 0.8.5-29
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 0.8.5-27
- OCaml 5.3.0 rebuild for Fedora 42
- Update __ocaml_requires_opts for OCaml 5.3.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-25
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-24
- OCaml 5.2.0 for Fedora 41

* Mon Jan 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-23
- Bump and rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-20
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-19
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-18
- Bump release and rebuild

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-17
- OCaml 5.1 rebuild for Fedora 40

* Wed Oct  4 2023 Jerry James <loganjerry@gmail.com> - 0.8.5-16
- Use the %%ocaml_install macro

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-15
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.8.5-14
- OCaml 5.0.0 rebuild
- Add patch to adapt tests to OCaml 5.0
- Do not require ocaml-compiler-libs at runtime

* Mon Jan 23 2023 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-13
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 0.8.5-10
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-10
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-9
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-7
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar  1 10:09:49 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-5
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-3
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.5-2
- OCaml 4.11.0 rebuild

* Wed Aug 19 2020 Jerry James <loganjerry@gmail.com> - 0.8.5-1
- Version 0.8.5

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 0.8.4-1
- New upstream release 0.8.4 (rhbz#1849120)

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-7
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 18 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-6
- OCaml 4.11.0 pre-release

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.3-2
- OCaml 4.10.0+beta1 rebuild.

* Wed Jan  8 2020 Jerry James <loganjerry@gmail.com> - 0.8.3-1
- Initial RPM
