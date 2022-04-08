%global debug_package %{nil}

Summary:        Compatibility package for OCaml's standard iterator type
Name:           ocaml-seq
Version:        0.2.2
Release:        7%{?dist}
License:        LGPLv2+ WITH exceptions
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/c-cube/seq
Source0:        %{url}/archive/%{version}/seq-%{version}.tar.gz

BuildRequires:  ocaml
BuildRequires:  ocaml-dune >= 1.1.0

%description
Compatibility package for OCaml's standard iterator type starting from 4.07.

%package        devel
Summary:        Development files for %{name}

Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n seq-%{version}

%build
dune build %{?_smp_mflags}

%install
dune install --destdir=%{buildroot}

# We do not want the ml files
find %{buildroot}%{_libdir}/ocaml -name \*.ml -delete

# We install the documentation with the doc macro
rm -fr %{buildroot}%{_prefix}/doc

%files
%doc README.md
%license LICENSE
%dir %{_libdir}/ocaml/seq/
%{_libdir}/ocaml/seq/META
%{_libdir}/ocaml/seq/seq.cma
%{_libdir}/ocaml/seq/seq.cmi
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/seq/seq.cmxs
%endif

%files devel
%license LICENSE
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/seq/seq.a
%{_libdir}/ocaml/seq/seq.cmxa
%{_libdir}/ocaml/seq/seq.cmx
%endif
%{_libdir}/ocaml/seq/seq.mli
%{_libdir}/ocaml/seq/seq.cmt
%{_libdir}/ocaml/seq/seq.cmti
%{_libdir}/ocaml/seq/dune-package
%{_libdir}/ocaml/seq/opam

%changelog
* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.2-7
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.2-6
- Initial CBL-Mariner import from Fedora 35 (license: MIT).

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jerry James <loganjerry@gmail.com> - 0.2.2-4
- Move META to the main package
- Drop obsolete workaround for a dune bug

* Mon Mar  1 2021 Richard W.M. Jones <rjones@redhat.com> - 0.2.2-4
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 0.2.2-2
- OCaml 4.11.1 rebuild

* Tue Sep  1 2020 Jerry James <loganjerry@gmail.com> - 0.2.2-1
- Version 0.2.2
- Drop all patches
- Build with dune

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-17
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-16
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-14
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-13
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-12
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-11
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-10
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-8
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 0.1-7
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1-6
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1-5
- OCaml 4.08.1 (final) rebuild.

* Thu Aug 01 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Aug  1 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1-3
- Add license file from upstream.

* Thu Aug  1 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1-2
- Add a link to upstream bug about the license.
- Don't install seq.ml file.
- Don't package META twice.

* Thu Aug  1 2019 Richard W.M. Jones <rjones@redhat.com> - 0.1-1
- Initial version.
