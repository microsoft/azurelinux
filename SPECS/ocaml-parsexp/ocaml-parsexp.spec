%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global srcname parsexp

Name:           ocaml-%{srcname}
Version:        0.16.0
Release:        1%{?dist}
Summary:        S-expression parsing library
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/janestreet/parsexp
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-dune >= 2.0.0
BuildRequires:  ocaml-sexplib0-devel >= 0.16

%description
This library provides generic parsers for parsing S-expressions from
strings or other media.

The library is focused on performance but still provides full generic
parsers that can be used effortlessly with strings, bigstrings, lexing
buffers, character streams or any other source.

It provides three different classes of parsers:
- the normal parsers, producing [Sexp.t] or [Sexp.t list] values;
- the parsers with positions, building compact position sequences so
  that one can recover original positions in order to properly report
  error locations at little cost; and
- the Concrete Syntax Tree parsers, producing values of type
  [Parsexp.Cst.t] which record the concrete layout of the s-expression
  syntax, including comments.

This library is portable and doesn't provide I/O functions.  To read
s-expressions from files or other external sources, you should use
parsexp_io.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-sexplib0-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n parsexp-%{version}

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%doc CHANGES.md README.org
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Thu May 02 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.16.0-1
- Converted spec file to match with Fedora 41.
- Upgraded to version 0.16.0

* Tue Jan 18 2022 Thomas Crain <thcrain@microsoft.com> - 0.15.0-1
- Upgrade to latest version
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.14.0-9
- Initial CBL-Mariner import from Fedora 34 (license: MIT).

* Mon Feb 22 2021 Jerry James <loganjerry@gmail.com> - 0.14.0-8
- Rebuild for ocaml-base 0.14.1

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-7
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-5
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.14.0-4
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 17 2020 Jerry James <loganjerry@gmail.com> - 0.14.0-1
- Version 0.14

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-7
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 03 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-6
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-5
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.13.0-3
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 16 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-2
- Change -devel subpackage Requires to ocaml-base-devel
- Build in parallel

* Fri Jan 10 2020 Jerry James <loganjerry@gmail.com> - 0.13.0-1
- Initial RPM
