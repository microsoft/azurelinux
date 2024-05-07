# OCaml packages not built on i686 since OCaml 5 / Fedora 39.
ExcludeArch: %{ix86}

Name:           ocaml-ppx-let
Version:        0.16.0
Release:        9%{?dist}
Summary:        Monadic let-bindings for OCaml

License:        MIT
URL:            https://github.com/janestreet/ppx_let
Source0:        %{url}/archive/v%{version}/ppx_let-%{version}.tar.gz

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-base-devel >= 0.16
BuildRequires:  ocaml-dune >= 2.0.0
BuildRequires:  ocaml-ppx-here-devel >= 0.16
BuildRequires:  ocaml-ppxlib-devel >= 0.31.0

%description
Ppx_let is a ppx rewriter for monadic and applicative let bindings,
match expressions, and if expressions.

The aim of this rewriter is to make monadic and applicative code look
nicer by writing custom binders the same way that we normally bind
variables.  In OCaml, the common way to bind the result of a computation
to a variable is:

  let VAR = EXPR in BODY

ppx_let simply adds two new binders: let%%bind and let%%map.  These are
rewritten into calls to the bind and map functions respectively.  These
functions are expected to have

  val map  : 'a t -> f:('a -> 'b)   -> 'b t
  val bind : 'a t -> f:('a -> 'b t) -> 'b t

for some type t, as one might expect.

These functions are to be provided by the user, and are generally
expected to be part of the signatures of monads and applicatives
modules.  This is the case for all monads and applicatives defined by
the Jane Street's Core suite of libraries.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-base-devel%{?_isa}
Requires:       ocaml-ppx-here-devel%{?_isa}
Requires:       ocaml-ppxlib-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature
files for developing applications that use %{name}.

%prep
%autosetup -n ppx_let-%{version}

%build
%dune_build

%install
%dune_install

%check
%dune_check

%files -f .ofiles
%doc CHANGES.md README.md
%license LICENSE.md

%files devel -f .ofiles-devel

%changelog
* Wed May 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.16.0-9
- Initial Import from Fedora
- License Verified

* Mon Jan 29 2024 Richard W.M. Jones <rjones@redhat.com> - 0.16.0-9
- Bump and rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 0.16.0-6
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 0.16.0-5
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 0.16.0-4
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 0.16.0-2
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 0.16.0-1
- Version 0.16.0

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 0.15.0-10
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov  1 2022 Jerry James <loganjerry@gmail.com> - 0.15.0-8
- Rebuild for ocaml-ppxlib 0.28.0

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 0.15.0-7
- Rebuild for ocaml-ppxlib 0.27.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 0.15.0-5
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 0.15.0-5
- OCaml 4.14.0 rebuild

* Mon Feb 28 2022 Jerry James <loganjerry@gmail.com> - 0.15.0-4
- Version 0.15.0 rerelease

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 0.15.0-3
- OCaml 4.13.1 rebuild to remove package notes

* Thu Feb  3 2022 Jerry James <loganjerry@gmail.com> - 0.15.0-2
- Conditionally build docs to avoid circular dependency on odoc

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 31 2021 Jerry James <loganjerry@gmail.com> - 0.15.0-1
- Initial RPM