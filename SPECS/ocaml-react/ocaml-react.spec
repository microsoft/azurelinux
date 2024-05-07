Summary:        OCaml framework for Functional Reactive Programming (FRP)
Name:           ocaml-react
Version:        1.2.2
Release:        1%{?dist}
License:        ISC
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://erratique.ch/software/react
Source0:        %{url}/releases/react-%{version}.tbz

BuildRequires:  ocaml >= 5.1.1
BuildRequires:  ocaml-ocamlbuild
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-rpm-macros
BuildRequires:  ocaml-topkg-devel >= 1.0.3

# Do not require ocaml-compiler-libs at runtime
%global __ocaml_requires_opts -i Asttypes -i Build_path_prefix_map -i Cmi_format -i Env -i Ident -i Identifiable -i Load_path -i Location -i Longident -i Misc -i Outcometree -i Parsetree -i Path -i Primitive -i Shape -i Subst -i Toploop -i Type_immediacy -i Types -i Warnings
 
 
%description
React is an OCaml module for functional reactive programming (FRP). It
provides support to program with time varying values : declarative
events and signals. React doesn't define any primitive event or
signal; it lets the client choose the concrete timeline.
 
React is made of a single, independent module and distributed under
the ISC license.
 
Given an absolute notion of time Rtime helps you to manage a timeline
and provides time stamp events, delayed events and delayed signals.
 
 
%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
 
 
%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.
 
 
%prep
%autosetup -n react-%{version}
 
# require debug info
echo $'\ntrue: debug' >> _tags
 
# expose a math library dependency to RPM
echo $'\ntrue: cclib(-lm)' >> _tags
 
 
%build
ocaml pkg/pkg.ml build --tests true
 
 
%install
%ocaml_install
 
%check
ocaml pkg/pkg.ml test
 
 
%files -f .ofiles
%license LICENSE.md
 
 
%files devel -f .ofiles-devel
%doc CHANGES.md README.md

%changelog
* Mon May 06 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsft.com> - 1.2.2-1
- Upgrade to 1.2.2
- Use ocaml 5.1.1 to build and update other build requirements

* Thu Mar 31 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-8
- Cleaning-up spec. License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.1-7
- Initial CBL-Mariner import from Fedora 35 (license: MIT).

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Jerry James <loganjerry@gmail.com> - 1.2.1-5
- Move META to the main package

* Mon Mar  1 13:12:20 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-5
- OCaml 4.12.0 build

* Tue Feb  2 2021 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-4
- Bump and rebuild for updated ocaml-camomile dep (RHBZ#1923853).

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-2
- OCaml 4.11.1 rebuild

* Tue Sep  1 2020 Jerry James <loganjerry@gmail.com> - 1.2.1-1
- Version 1.2.1
- License is now ISC
- Build with topkg
- Drop upstreamed safe string patch

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-33
- OCaml 4.11.0 rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-32
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-30
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-29
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-28
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-27
- Update all OCaml dependencies for RPM 4.16.

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-26
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-24
- OCaml 4.10.0+beta1 rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-23
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-22
- OCaml 4.09.0 (final) rebuild.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-21
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-20
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-18
- OCaml 4.08.0 (final) rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-17
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-14
- OCaml 4.07.0 (final) rebuild.

* Wed Jun 20 2018 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-13
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-11
- OCaml 4.06.0 rebuild.
- Small safe-string fix.

* Tue Aug 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-10
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-7
- OCaml 4.04.2 rebuild.

* Fri May 12 2017 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-6
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 1.2.0-4
- rebuild for s390x codegen bug

* Mon Nov 07 2016 Richard W.M. Jones <rjones@redhat.com> - 1.2.0-3
- Rebuild for OCaml 4.04.0.
- Add explicit BR on ocamlbuild.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Aug  2 2015 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-16
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-15
- ocaml-4.02.2 final rebuild.

* Thu Jun 18 2015 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-14
- ocaml-4.02.2 rebuild.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 17 2015 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-12
- ocaml-4.02.1 rebuild.

* Sun Aug 31 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-11
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-10
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-8
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Tue Jul 22 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-7
- OCaml 4.02.0 beta rebuild.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-5
- Remove ocaml_arches macro (RHBZ#1087794).

* Wed Sep 18 2013 Jerry James <loganjerry@gmail.com>
- Rebuild for OCaml 4.01.0
- Enable debuginfo
- Add missing ExclusiveArch
- Minor spec file cleanups

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 30 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.4-1
- New upstream version 0.9.4.
- Rebuild for OCaml 4.00.1.
- Clean up the spec file.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-4
- Rebuild for OCaml 4.00.0.

* Fri Jan 06 2012 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-3
- Rebuild for OCaml 3.12.1.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Richard W.M. Jones <rjones@redhat.com> - 0.9.2-1
- Rebuild for OCaml 3.12.0.

* Wed Dec 30 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-3
- Rebuild for OCaml 3.11.2.

* Thu Oct  8 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.0-2
- Initial RPM release.
- Use global instead of define (Till Maas).
