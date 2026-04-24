# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

# This package is needed to build ppx_jane, but its tests require ppx_jane.
# Break the dependency cycle here.
%bcond test 0

Name:           ocaml-cinaps
Version:        0.15.1
Release: 26%{?dist}
Summary:        Trivial Metaprogramming tool using the OCaml toplevel

License:        MIT
URL:            https://github.com/ocaml-ppx/cinaps
VCS:            git:%{url}.git
Source:         %{url}/archive/v%{version}/cinaps-%{version}.tar.gz

BuildRequires:  help2man
BuildRequires:  ocaml >= 4.04.0
BuildRequires:  ocaml-dune >= 2.0.0
BuildRequires:  ocaml-re-devel >= 1.8.0

%if %{with test}
BuildRequires:  ocaml-ppx-jane-devel
%endif

%description
Cinaps is a trivial Metaprogramming tool for OCaml using the OCaml
toplevel.

It is intended for two purposes:
- when you want to include a bit of generated code in a file, but writing
  a proper generator/ppx rewriter is not worth it;
- when you have many repeated blocks of similar code in your program, to
  help writing and maintaining them.

It is not intended as a general preprocessor, and in particular can only
be used to generate static code that is independent of the system.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n cinaps-%{version}

%build
%dune_build

%install
%dune_install

# Generate the man page
mkdir -p %{buildroot}%{_mandir}/man1
help2man -N --version-string=%{version} \
  -n 'Trivial Metaprogramming tool using the OCaml toplevel' \
  %{buildroot}%{_bindir}/cinaps > %{buildroot}%{_mandir}/man1/cinaps.1

%if %{with test}
%check
%dune_check
%endif

%files -f .ofiles
%doc README.org
%license LICENSE.md
%{_mandir}/man1/cinaps.1*

%files devel -f .ofiles-devel

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 11 2025 Jerry James  <loganjerry@gmail.com> - 0.15.1-24
- Rebuild to fix OCaml dependencies

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan  9 2025 Jerry James <loganjerry@gmail.com> - 0.15.1-22
- OCaml 5.3.0 rebuild for Fedora 42

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-20
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-19
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-16
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-15
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-14
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-12
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.15.1-11
- OCaml 5.0.0 rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-10
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 0.15.1-7
- Optionally run tests
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-7
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-6
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-4
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Mar  1 12:17:30 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 0.15.1-2
- OCaml 4.12.0 build

* Sat Feb 13 2021 Jerry James <loganjerry@gmail.com> - 0.15.1-1
- Version 0.15.1

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Jerry James <loganjerry@gmail.com> - 0.15.0-1
- Version 0.15.0
- New URLs

* Mon Dec  7 2020 Jerry James <loganjerry@gmail.com> - 0.14.0-6
- Add missing ocaml-re-devel R to the -devel subpackage

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-5
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-4
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Jerry James <loganjerry@gmail.com> - 0.14.0-1
- Version 0.14.0

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-7
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-6
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-5
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-4
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-2
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan  2 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-1
- Initial RPM
