%global opt %(test -x %{_bindir}/ocamlopt && echo 1 || echo 0)

%if !%{opt}
%global debug_package %{nil}
%endif

%define libname %(sed -e 's/^ocaml-//' <<< %{name})

Summary:        Equivalent of the C preprocessor for OCaml programs
Name:           ocaml-cppo
Version:        1.6.9
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/ocaml-community/cppo
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-dune
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamlbuild

%description
Cppo is an equivalent of the C preprocessor targeted at the OCaml
language and its variants.

The main purpose of cppo is to provide a lightweight tool for simple
macro substitution (＃define) and file inclusion (＃include) for the
occasional case when this is useful in OCaml. Processing specific
sections of files by calling external programs is also possible via
＃ext directives.

The implementation of cppo relies on the standard library of OCaml and
on the standard parsing tools Ocamllex and Ocamlyacc, which contribute
to the robustness of cppo across OCaml versions.


%package ocamlbuild
Summary:        Preprocessing plugin for ocamlbuild
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-ocamlbuild%{?_isa}
# There is no devel subpackage because this package IS for development purposes


%description ocamlbuild
This package contains a plugin for ocamlbuild that enables calling cppo
at build time.  To use it, call ocamlbuild with the argument
`-plugin-tag package(cppo_ocamlbuild)`.

%prep
%autosetup -n cppo-%{version}

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files
%license LICENSE.md
%doc Changes.md README.md
%{_bindir}/cppo
%{_libdir}/ocaml/cppo


%files ocamlbuild
%{_libdir}/ocaml/cppo_ocamlbuild/

%changelog
* Fri May 03 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsft.com> - 1.6.9-1
- Upgrade to 1.6.9

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.6-5
- Cleaning-up spec. License verified.

* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.6.6-4
- Switching to using full number for the 'Release' tag.
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Feb 28 2020 Richard W.M. Jones <rjones@redhat.com> - 1.6.6-3.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.6.6-3
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.6.6-1
- New upstream version 1.6.6.
- Change build system from jbuilder to dune.
- Remove patch for fix which is now upstream.
- OCaml 4.10.0+beta1 rebuild.

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.6.5-6
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.6.5-5
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.6.5-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.6.5-2
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.6.5-1
- New upstream version 1.6.5.
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-2
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.6.4-1
- New upstream version 1.6.4.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-8
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-6
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-5
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-2
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1.5.0-1
- New upstream version 1.5.0 (for OCaml 4.04.1).

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Nov 05 2016 Richard W.M. Jones <rjones@redhat.com> - 1.4.0-1
- New upstream version 1.4.0.
- Fix download source URL.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-2
- OCaml 4.02.3 rebuild.

* Fri Jul 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.1.2-1
- New upstream release 1.1.2.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-4
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-3
- ocaml-4.02.2 rebuild.

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.0.1-2
- ocaml-4.02.1 rebuild.

* Mon Nov  3 2014 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-9
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-8
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-6
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 28 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.3-5
- Rebuild for OCaml 4.02.0 beta.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 24 2014 Jaromir Capik <jcapik@redhat.com> - 0.9.3-3
- Removing ExclusiveArch

* Mon Jan 27 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.3-2
- Incorporate review feedback

* Mon Jan 20 2014 Michel Salim <salimma@fedoraproject.org> - 0.9.3-1
- Initial package
