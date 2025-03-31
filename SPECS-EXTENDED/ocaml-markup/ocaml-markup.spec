Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global srcname markup
%global giturl  https://github.com/aantron/markup.ml

Name:           ocaml-%{srcname}
Version:        1.0.3
Release:        18%{?dist}
Summary:        Error-recovering streaming HTML5 and XML parsers for OCaml

License:        MIT
URL:            https://aantron.github.io/markup.ml/
Source0:        https://github.com/aantron/markup.ml/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.03.0
BuildRequires:  ocaml-bisect-ppx-devel >= 2.5.0
BuildRequires:  ocaml-dune >= 2.7.0
BuildRequires:  ocaml-lwt-devel
BuildRequires:  ocaml-ounit-devel
BuildRequires:  ocaml-uutf-devel >= 1.0.0

%description
Markup.ml is a pair of parsers implementing the HTML5 and XML
specifications, including error recovery.  Usage is simple, because each
parser is a function from byte streams to parsing signal streams.

In addition to being error-correcting, the parsers are:
- **streaming**: parsing partial input and emitting signals while more
  input is still being received;
- **lazy**: not parsing input unless you have requested the next parsing
  signal, so you can easily stop parsing part-way through a document;
- **non-blocking**: they can be used with Lwt, but still provide a
  straightforward synchronous interface for simple usage; and
- **one-pass**: memory consumption is limited since the parsers don't
  build up a document representation, nor buffer input beyond a small
  amount of lookahead.

The parsers detect character encodings automatically, and emit everything
in UTF-8.  The HTML parser understands SVG and MathML, in addition to
HTML5.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       ocaml-uutf-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%package        lwt
Summary:        Adapter between ocaml-markup and ocaml-lwt
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    lwt
This package contains an adapter between Markup.ml and Lwt.

%package        lwt-devel
Summary:        Development files for %{name}-lwt
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       %{name}-lwt%{?_isa} = %{version}-%{release}
Requires:       ocaml-lwt-devel%{?_isa}

%description    lwt-devel
The %{name}-lwt-devel package contains libraries and signature files for
developing applications that use %{name}-lwt.

%prep
%autosetup -n markup.ml-%{version} -p1

# The uchar package is a forward compatibility package for OCaml versions prior
# to 4.03.  We have a later OCaml in Fedora; uchar is in the standard library.
# Nothing in this package directly refers to uchar (only indirectly via uutf),
# so just remove the reference to it.
sed -i '/uchar/d' markup.opam

%build
%dune_build

%install
%dune_install -s

%check
%dune_check

%files -f .ofiles-markup
%doc README.md
%license LICENSE.md

%files devel -f .ofiles-markup-devel

%files lwt -f .ofiles-markup-lwt

%files lwt-devel -f .ofiles-markup-lwt-devel

%changelog
* Wed Jan 08 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.0.3-18
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-16
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-15
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-12
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-11
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-10
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-8
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.0.3-7
- OCaml 5.0.0 rebuild

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-6
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 18 2022 Jerry James <loganjerry@gmail.com> - 1.0.3-4
- Rebuild for ocaml-lwt 5.6.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 1.0.3-2
- Use new OCaml macros

* Sun Jun 19 2022 Richard W.M. Jones <rjones@redhat.com> - 1.0.3-2
- OCaml 4.14.0 rebuild

* Wed Apr 27 2022 Jerry James <loganjerry@gmail.com> - 1.0.3-1
- Version 1.0.3
- Drop upstreamed patch for OCaml 4.13.1 compatibility

* Mon Feb 28 2022 Jerry James <loganjerry@gmail.com> - 1.0.2-7
- Rebuild for ocaml-uutf 1.0.3

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-6
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan  3 2022 Jerry James <loganjerry@gmail.com> - 1.0.2-4
- Rebuild for changed ocaml-lwt hashes

* Tue Oct 05 2021 Richard W.M. Jones <rjones@redhat.com> - 1.0.2-3
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul  5 2021 Jerry James <loganjerry@gmail.com> - 1.0.2-1
- Version 1.0.2

* Tue Jun 22 2021 Jerry James <loganjerry@gmail.com> - 1.0.1-1
- Version 1.0.1

* Thu Jun  3 2021 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-6
- Rebuild for new ocaml-lwt.

* Mon Mar  1 21:30:59 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.0.0-5
- OCaml 4.12.0 build

* Mon Feb 22 2021 Jerry James <loganjerry@gmail.com> - 1.0.0-4
- Rebuild for ocaml-lwt 5.4.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec  2 2020 Jerry James <loganjerry@gmail.com> - 1.0.0-2
- Upstream re-released version 1.0.0

* Fri Oct 23 2020 Jerry James <loganjerry@gmail.com> - 1.0.0-1
- Version 1.0.0

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.2-12
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.2-11
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 05 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.2-8
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.2-7
- OCaml 4.11.0 pre-release attempt 2

* Sat Apr 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.2-6
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.8.2-5
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 22 2020 Jerry James <loganjerry@gmail.com> - 0.8.2-3
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 16 2020 Jerry James <loganjerry@gmail.com> - 0.8.2-2
- Add ocaml-uutf-devel R to -devel
- Add ocaml-bisect-ppx-devel R to -lwt-devel
- Build in parallel

* Fri Jan 10 2020 Jerry James <loganjerry@gmail.com> - 0.8.2-1
- Initial RPM
