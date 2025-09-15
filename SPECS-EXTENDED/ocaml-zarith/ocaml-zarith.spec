Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global pkgname zarith


Name:           ocaml-%{pkgname}
Version:        1.14
Release:        3%{?dist}
Summary:        OCaml interface to GMP

License:        LGPL-2.1-only WITH OCaml-LGPL-linking-exception
URL:            https://github.com/ocaml/Zarith
Source:         https://github.com/ocaml/Zarith/archive/release-%{version}.tar.gz

BuildRequires:  gcc
BuildRequires:  gmp-devel
BuildRequires:  make
BuildRequires:  ocaml >= 4.04.0
BuildRequires:  ocaml-findlib
BuildRequires:  ocaml-ocamldoc
BuildRequires:  ocaml-rpm-macros
BuildRequires:  perl-interpreter

# Replace config.guess with a more up to date version which knows about POWER.
BuildRequires:  redhat-rpm-config

# Do not require ocaml-compiler-libs at runtime
%global __ocaml_requires_opts -i Asttypes -i Build_path_prefix_map -i Cmi_format -i Env -i Ident -i Identifiable -i Load_path -i Location -i Longident -i Misc -i Outcometree -i Parsetree -i Path -i Primitive -i Shape -i Subst -i Toploop -i Type_immediacy -i Types -i Warnings

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
sed -i "s|^ccdef=''|ccdef='%{build_cflags}'|" configure
sed -i "s/-shared/-g &/" project.mak

%build
export CC="gcc"
# This is NOT an autoconf-generated configure script; %%configure doesn't work
./configure
# %%{?_smp_mflags} is not safe; same action performed by multiple CPUs
make
make doc

%install
mkdir -p %{buildroot}%{ocamldir}/stublibs
make install INSTALLDIR=%{buildroot}%{ocamldir}

# Install missing files
cp -p {big_int_Z,q,z}.cmt zarith_version.cm{i,t} zarith_top.{cm{i,t},ml} \
      z_mlgmpidl.mli %{buildroot}%{ocamldir}/zarith
cp -p zarith.opam %{buildroot}%{ocamldir}/zarith/opam

%ocaml_files

%ifarch %{ocaml_native_compiler}
# The tests assume the availability of ocamlopt
%check
export LD_LIBRARY_PATH=$PWD
make tests
%endif

%files -f .ofiles
%doc README.md
%license LICENSE

%files devel -f .ofiles-devel
%doc Changes html

%changelog
* Fri Jan 03 2025 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 1.14-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Jerry James <loganjerry@gmail.com> - 1.14-1
- Version 1.14

* Wed Jun 19 2024 Richard W.M. Jones <rjones@redhat.com> - 1.13-8
- OCaml 5.2.0 ppc64le fix

* Wed May 29 2024 Richard W.M. Jones <rjones@redhat.com> - 1.13-7
- OCaml 5.2.0 for Fedora 41

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Richard W.M. Jones <rjones@redhat.com> - 1.13-4
- OCaml 5.1.1 + s390x code gen fix for Fedora 40

* Tue Dec 12 2023 Richard W.M. Jones <rjones@redhat.com> - 1.13-3
- OCaml 5.1.1 rebuild for Fedora 40

* Thu Oct 05 2023 Richard W.M. Jones <rjones@redhat.com> - 1.13-2
- OCaml 5.1 rebuild for Fedora 40

* Thu Jul 27 2023 Jerry James <loganjerry@gmail.com> - 1.13-1
- Version 1.13

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Richard W.M. Jones <rjones@redhat.com> - 1.12-11
- OCaml 5.0 rebuild for Fedora 39

* Mon Jul 10 2023 Jerry James <loganjerry@gmail.com> - 1.12-10
- OCaml 5.0.0 rebuild
- Install missing files
- Do not require ocaml-compiler-libs at runtime

* Tue Jan 24 2023 Richard W.M. Jones <rjones@redhat.com> - 1.12-9
- Rebuild OCaml packages for F38

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Jerry James <loganjerry@gmail.com> - 1.12-7
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Jerry James <loganjerry@gmail.com> - 1.12-6
- Use new OCaml macros

* Sat Jun 18 2022 Richard W.M. Jones <rjones@redhat.com> - 1.12-6
- OCaml 4.14.0 rebuild

* Fri Feb 04 2022 Richard W.M. Jones <rjones@redhat.com> - 1.12-5
- OCaml 4.13.1 rebuild to remove package notes

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct 04 2021 Richard W.M. Jones <rjones@redhat.com> - 1.12-3
- OCaml 4.13.1 build

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar  3 2021 Jerry James <loganjerry@gmail.com> - 1.12-1
- Version 1.12

* Mon Mar  1 13:12:07 GMT 2021 Richard W.M. Jones <rjones@redhat.com> - 1.11-3
- OCaml 4.12.0 build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 16 2020 Jerry James <loganjerry@gmail.com> - 1.11-1
- Version 1.11

* Sun Sep 13 2020 Dan Čermák <dan.cermak@cgc-instruments.com> - 1.10-1
- New upstream release 1.10

* Tue Sep 01 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-14
- OCaml 4.11.1 rebuild

* Fri Aug 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-13
- OCaml 4.11.0 rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 04 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-11
- OCaml 4.11.0+dev2-2020-04-22 rebuild

* Tue Apr 21 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-10
- OCaml 4.11.0 pre-release attempt 2

* Fri Apr 17 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-9
- OCaml 4.11.0 pre-release

* Thu Apr 02 2020 Richard W.M. Jones <rjones@redhat.com> - 1.9.1-8
- Update all OCaml dependencies for RPM 4.16.

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
