Vendor:         Microsoft Corporation
Distribution:   Mariner
%ifnarch %{ocaml_native_compiler}
%global debug_package %{nil}
%endif

%global srcname markup
%bcond_with tests
%bcond_with docs

Name:           ocaml-%{srcname}
Version:        1.0.0
Release:        5%{?dist}
Summary:        Error-recovering streaming HTML5 and XML parsers for OCaml

License:        MIT
URL:            http://aantron.github.io/markup.ml/
Source0:        https://github.com/aantron/markup.ml/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  ocaml >= 4.02.0
BuildRequires:  ocaml-bisect-ppx-devel >= 2.0.0
BuildRequires:  ocaml-dune >= 2.7.0
BuildRequires:  ocaml-lwt-devel
BuildRequires:  ocaml-uutf-devel >= 1.0.0
%if %{with tests}
BuildRequires:  ocaml-ounit-devel
%endif
%if %{with docs}
BuildRequires:  ocaml-ocamldoc
%endif

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
Requires:       ocaml-bisect-ppx-devel%{?_isa}
Requires:       ocaml-lwt-devel%{?_isa}

%description    lwt-devel
The %{name}-lwt-devel package contains libraries and signature files for
developing applications that use %{name}-lwt.

%prep
%autosetup -n %{srcname}.ml-%{version} -p1

# The uchar package is a forward compatibility package for OCaml versions prior
# to 4.03.  We have a later OCaml in Fedora; uchar is in the standard library.
# Nothing in this package directly refers to uchar (only indirectly via uutf),
# so just remove the reference to it.
sed -i '/uchar/d' markup.opam

%build
dune build %{?_smp_mflags} @install

%if %{with docs}
# Build the documentation.  Unfortunately, ocamldoc is not smart enough to
# figure out that Kstream is Markup.Kstream.  I have not been able to figure
# out how to convince it, so the temporary hacked-up copy of markup.mli is
# my way of working around the problem.  We should really build documentation
# with odoc, but this package is a build dependency of odoc.
mkdir tmp
sed '/Kstream/d' _build/default/src/markup.mli > tmp/markup.mli

mkdir html
ocamldoc -html -d html -css-style doc/style.css -I +lwt -I +lwt/unix \
  -I _build/install/default/lib/markup \
  -I _build/install/default/lib/markup-lwt \
  -I _build/install/default/lib/markup-lwt/unix \
  tmp/markup.mli \
  _build/default/src/lwt/markup_lwt.mli \
  _build/default/src/lwt_unix/markup_lwt_unix.mli
%endif

%install
dune install --destdir=%{buildroot}

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%ifarch %{ocaml_native_compiler}
# Add missing executable bits
find %{buildroot}%{_libdir}/ocaml -name \*.cmxs -exec chmod 0755 {} \+
%endif

%check
%if %{with tests}
dune runtest
%endif

%files
%doc README.md
%license LICENSE.md
%dir %{_libdir}/ocaml/%{srcname}/
%{_libdir}/ocaml/%{srcname}/META
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cma
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxs
%endif

%files devel
%if %{with docs}
%doc html/*
%endif
%{_libdir}/ocaml/%{srcname}/dune-package
%{_libdir}/ocaml/%{srcname}/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}/%{srcname}*.a
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmx
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmxa
%endif
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmt
%{_libdir}/ocaml/%{srcname}/%{srcname}*.cmti
%{_libdir}/ocaml/%{srcname}/*.ml
%{_libdir}/ocaml/%{srcname}/*.mli

%files lwt
%dir %{_libdir}/ocaml/%{srcname}-lwt/
%dir %{_libdir}/ocaml/%{srcname}-lwt/unix/
%{_libdir}/ocaml/%{srcname}-lwt/META
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.cma
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.cmi
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.cma
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.cmxs
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.cmxs
%endif

%files lwt-devel
%{_libdir}/ocaml/%{srcname}-lwt/dune-package
%{_libdir}/ocaml/%{srcname}-lwt/opam
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.a
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.cmx
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.cmxa
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.a
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.cmx
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.cmxa
%endif
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.cmt
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.cmti
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.ml
%{_libdir}/ocaml/%{srcname}-lwt/%{srcname}_lwt.mli
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.cmt
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.cmti
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.ml
%{_libdir}/ocaml/%{srcname}-lwt/unix/%{srcname}_lwt_unix.mli

%changelog
* Mon Aug 09 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.0.0-5
- Initial CBL-Mariner import from Fedora 34 (license: MIT).
- Remove test, docs circular dependencies

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
