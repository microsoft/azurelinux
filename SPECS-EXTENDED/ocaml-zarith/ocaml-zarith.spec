Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pkgname zarith

Name:           ocaml-%{pkgname}
Version:        1.9.1
Release:        9%{?dist}
Summary:        OCaml interface to GMP

# The license has a static linking exception
License:        LGPLv2 with exceptions
URL:            https://github.com/ocaml/Zarith/
Source0:        https://github.com/ocaml/Zarith/archive/release-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  ocaml
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  perl-interpreter

%description
This library implements arithmetic and logical operations over
arbitrary-precision integers.  

The module is simply named "Z".  Its interface is similar to that of the
Int32, Int64 and Nativeint modules from the OCaml standard library, with
some additional functions.  See the file z.mlip for documentation.

The implementation uses GMP (the GNU Multiple Precision arithmetic
library) to compute over big integers.  However, small integers are
represented as unboxed Caml integers, to save space and improve
performance.  Big integers are allocated in the Caml heap, bypassing
GMP's memory management and achieving better GC behavior than e.g. the
MLGMP library.  Computations on small integers use a special, faster
path (coded in assembly for some platforms and functions) eschewing
calls to GMP, while computations on large integers use the low-level
MPN functions from GMP.

Arbitrary-precision integers can be compared correctly using OCaml's
polymorphic comparison operators (=, <, >, etc.).

Additional features include:
- a module Q for rationals, built on top of Z (see q.mli)
- a compatibility layer Big_int_Z that implements the same API as Big_int,
  but uses Z internally

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and signature files for
developing applications that use %{name}.

%prep
%autosetup -n Zarith-release-%{version}

# Fix compilation flags
sed -i "s|^ccdef=''|ccdef='%{optflags}'|" configure
sed -ri "s/(-ccopt|-shared|-failsafe)/-g &/" project.mak
sed -i "s/+compiler-libs/& -g/;s/\(\$(OCAMLC)\) -o/\1 -g -o/" project.mak

%build
export CC="gcc"
# This is NOT an autoconf-generated configure script; %%configure doesn't work
./configure
# %%{?_smp_mflags} is not safe; same action performed by multiple CPUs
make
make doc

%install
mkdir -p %{buildroot}%{_libdir}/ocaml/stublibs
make install INSTALLDIR=%{buildroot}%{_libdir}/ocaml

%check
export LD_LIBRARY_PATH=$PWD
make tests

%files
%doc README.md
%license LICENSE
%{_libdir}/ocaml/%{pkgname}/
%ifarch %{ocaml_native_compiler}
%exclude %{_libdir}/ocaml/%{pkgname}/*.a
%exclude %{_libdir}/ocaml/%{pkgname}/*.cmx
%exclude %{_libdir}/ocaml/%{pkgname}/*.cmxa
%endif
%exclude %{_libdir}/ocaml/%{pkgname}/*.mli
%exclude %{_libdir}/ocaml/%{pkgname}/*.h
%{_libdir}/ocaml/stublibs/*.so
%{_libdir}/ocaml/stublibs/*.so.owner

%files devel
%doc Changes html
%ifarch %{ocaml_native_compiler}
%{_libdir}/ocaml/%{pkgname}/*.a
%{_libdir}/ocaml/%{pkgname}/*.cmx
%{_libdir}/ocaml/%{pkgname}/*.cmxa
%endif
%{_libdir}/ocaml/%{pkgname}/*.mli
%{_libdir}/ocaml/%{pkgname}/*.h

%changelog
* Thu Oct 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.1-9
- Switching to using full number for the 'Release' tag.

* Mon Jan 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.9.1-8.1
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Red Hat guess file

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-7.1
- OCaml 4.10.0 final (Fedora 32).

* Wed Feb 26 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-7
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-5
- OCaml 4.10.0+beta1 rebuild.

* Fri Jan 10 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-4
- Bump release and rebuild.

* Thu Jan 09 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-3
- OCaml 4.09.0 for riscv64

* Fri Dec 06 2019 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-2
- OCaml 4.09.0 (final) rebuild.

* Tue Oct 29 2019 Jerry James <loganjerry@gmail.com> - 1.9.1-1
- New upstream version

* Tue Sep  3 2019 Jerry James <loganjerry@gmail.com> - 1.9-1
- New upstream version

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8-5
- OCaml 4.08.1 (final) rebuild.

* Wed Jul 31 2019 Richard W.M. Jones <rjones@redhat.com> - 1.8-4
- OCaml 4.08.1 (rc2) rebuild.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul  4 2019 Jerry James <loganjerry@gmail.com> - 1.8-2
- Rebuild for ocaml 4.08.0

* Wed May  1 2019 Jerry James <loganjerry@gmail.com> - 1.8-1
- New upstream version

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-9
- Bump release and rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-8
- Bump release and rebuild.

* Mon Apr 29 2019 Richard W.M. Jones <rjones@redhat.com> - 1.7-7
- OCaml 4.08.0 (beta 3) rebuild.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7-4
- OCaml 4.07.0 (final) rebuild.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 1.7-3
- OCaml 4.07.0-rc1 rebuild.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 08 2017 Richard W.M. Jones <rjones@redhat.com> - 1.7
- New upstream version 1.7.

* Tue Nov 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-12
- OCaml 4.06.0 rebuild.

* Mon Aug 07 2017 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-11
- OCaml 4.05.0 rebuild.

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-8
- OCaml 4.04.2 rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-7
- Bump release and rebuild.

* Thu May 11 2017 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-6
- OCaml 4.04.1 rebuild.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 09 2016 Dan Horák <dan@danny.cz> - 1.4.1-4
- rebuild for s390x codegen bug

* Mon Nov 07 2016 Richard W.M. Jones <rjones@redhat.com> - 1.4.1-3
- Rebuild for OCaml 4.04.0.
- Add a fix/workaround for undefined behaviour (RHBZ#1392247).
- Fix config.guess.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 25 2015 Jerry James <loganjerry@gmail.com> - 1.4.1-1
- New upstream release

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3-6
- OCaml 4.02.3 rebuild.

* Wed Jun 24 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3-5
- ocaml-4.02.2 final rebuild.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3-4
- Bump release and rebuild.
- Fix 'sed' expressions to use a different separator character.

* Wed Jun 17 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3-3
- ocaml-4.02.2 rebuild.

* Wed Feb 18 2015 Richard W.M. Jones <rjones@redhat.com> - 1.3-2
- ocaml-4.02.1 rebuild.

* Tue Oct 14 2014 Jerry James <loganjerry@gmail.com> - 1.3-1
- New upstream release
- Drop -fix-ints.patch
- Fix license handling

* Tue Sep  2 2014 Jerry James <loganjerry@gmail.com> - 1.2.1-14
- Add -fix-ints patch to adapt to changed integer type names

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-14
- ocaml-4.02.0 final rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-13
- Bump release and rebuild.

* Sat Aug 23 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-12
- ocaml-4.02.0+rc1 rebuild.

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-10
- ocaml-4.02.0-0.8.git10e45753.fc22 rebuild.

* Mon Jul 21 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-9
- Bump release and rebuild.

* Mon Jul 21 2014 Jerry James <loganjerry@gmail.com> - 1.2.1-8
- OCaml 4.02.0 beta rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-6
- Remove ocaml_arches macro (RHBZ#1087794).

* Mon Mar 24 2014 Jerry James <loganjerry@gmail.com> - 1.2.1-5
- Fix bytecode build
- Build and install ocamldoc documentation
- BR ocaml-findlib instead of ocaml-findlib-devel
- The -devel subpackage needs gmp-devel for _libdir/libgmp.so
- Move zarith.h to the -devel subpackage

* Thu Sep 19 2013 Richard W.M. Jones <rjones@redhat.com> - 1.2.1-4
- Typo in changelog which confused my autorebuild scripts.

* Mon Sep 16 2013 Jerry James <loganjerry@gmail.com> - 1.2.1-3
- Rebuild for OCaml 4.01.0.
- Enable debuginfo

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 21 2013 Jerry James <loganjerry@gmail.com> - 1.2.1-1
- New upstream release

* Thu May 23 2013 Jerry James <loganjerry@gmail.com> - 1.2-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Jerry James <loganjerry@gmail.com> - 1.1-3
- Rebuild for OCaml 4.00.1

* Wed Oct 31 2012 Jerry James <loganjerry@gmail.com> - 1.1-2
- The -devel subpackage Requires need %%{?_isa}
- Try a different approach to keep the execstack flag off

* Fri Oct 26 2012 Jerry James <loganjerry@gmail.com> - 1.1-1
- Initial RPM
