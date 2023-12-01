%global __ocaml_requires_opts -c -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo.byte'
%global __ocaml_provides_opts -f '%{buildroot}%{_bindir}/ocamlrun %{buildroot}%{_bindir}/ocamlobjinfo.byte'
%global majmin %(echo %{version} | cut -d. -f1-2)
Summary:        OCaml compiler and programming environment
Name:           ocaml
Version:        4.13.1
Release:        2%{?dist}
License:        QPL and (LGPLv2+ with exceptions)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.ocaml.org
Source0:        https://caml.inria.fr/pub/distrib/%{name}-%{majmin}/%{name}-%{version}.tar.xz
Patch0001:      0001-Don-t-add-rpaths-to-libraries.patch
Patch0002:      0002-configure-Allow-user-defined-C-compiler-flags.patch
Patch0003:      0003-configure-Remove-incorrect-assumption-about-cross-co.patch
Patch0004:      0004-remove-unused-var-in-alloc_aync_stubs.patch
BuildRequires:  autoconf
BuildRequires:  binutils-devel
BuildRequires:  chrpath
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gdbm-devel
BuildRequires:  git
BuildRequires:  make
BuildRequires:  ncurses-devel
BuildRequires:  perl-interpreter
BuildRequires:  util-linux
%if %{with_check}
BuildRequires:  diffutils
%endif
# ocamlopt runs gcc to link binaries.  Because Mariner includes
# hardening flags automatically, mariner-rpm-macros is also required.
Requires:       gcc
Requires:       mariner-rpm-macros
# Because we pass -c flag to ocaml-find-requires (to avoid circular
# dependencies) we also have to explicitly depend on the right version
# of ocaml-runtime.
Requires:       ocaml-runtime = %{version}-%{release}
# Bundles an MD5 implementation in byterun/md5.{c,h}
Provides:       bundled(md5-plumb)
Provides:       ocaml(compiler) = %{version}

%description
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package comprises two batch compilers (a fast bytecode compiler
and an optimizing native-code compiler), an interactive toplevel system,
parsing tools (Lex,Yacc), a replay debugger, a documentation generator,
and a comprehensive library.

%package        runtime
Summary:        OCaml runtime environment
Requires:       util-linux
Provides:       ocaml(runtime) = %{version}

%description runtime
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains the runtime environment needed to run OCaml
bytecode.

%package        source
Summary:        Source code for OCaml libraries
Requires:       ocaml = %{version}-%{release}

%description source
Source code for OCaml libraries.

%package        ocamldoc
Summary:        Documentation generator for OCaml
Requires:       ocaml = %{version}-%{release}
Provides:       ocamldoc = %{version}-%{release}

%description ocamldoc
Documentation generator for OCaml.

%package        docs
Summary:        Documentation for OCaml
Requires:       ocaml = %{version}-%{release}

%description docs
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains man pages.

%package        compiler-libs
Summary:        Compiler libraries for OCaml
Requires:       ocaml = %{version}-%{release}

%description compiler-libs
OCaml is a high-level, strongly-typed, functional and object-oriented
programming language from the ML family of languages.

This package contains some modules used internally by the OCaml
compilers, useful for the development of some OCaml applications.
Note that this exposes internal details of the OCaml compiler which
may not be portable between versions.

%prep
%autosetup -p1
# Patches touch configure.ac, so rebuild it:
autoconf --force

%build
# We set --libdir to the unusual directory because we want OCaml to
# install its libraries and other files into a subdirectory.
#
# Force --host because of:
# https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/2O4HBOK6PTQZAFAVIRDVMZGG2PYB2QHM/
# (see also https://github.com/ocaml/ocaml/issues/8647)
#
# OC_CFLAGS/OC_LDFLAGS control what flags OCaml passes to the linker
# when doing final linking of OCaml binaries.  Setting these is
# necessary to ensure that generated binaries have Mariner hardening
# features.
%configure \
    OC_CFLAGS="$CFLAGS" \
    OC_LDFLAGS="$LDFLAGS" \
%if %{with_check}
    --enable-ocamltest \
%endif
    --libdir=%{_libdir}/ocaml \
    --host=`./build-aux/config.guess`

%make_build world
%make_build opt
%make_build opt.opt

%install
%make_install
perl -pi -e "s|^%{buildroot}||" %{buildroot}%{_libdir}/ocaml/ld.conf

echo %{version} > %{buildroot}%{_libdir}/ocaml/fedora-ocaml-release

# Remove rpaths from stublibs .so files.
chrpath --delete %{buildroot}%{_libdir}/ocaml/stublibs/*.so

find %{buildroot} -type f -name "*.la" -delete -print

# Remove .cmt and .cmti files, for now.  We could package them later.
# See also: http://www.ocamlpro.com/blog/2012/08/20/ocamlpro-and-4.00.0.html
find %{buildroot} \( -name '*.cmt' -o -name '*.cmti' \) -a -delete -print

%check
cd testsuite
make -j1 all

%files
%license LICENSE
%{_bindir}/ocaml

%{_bindir}/ocamlcmt
%{_bindir}/ocamldebug
%{_bindir}/ocamlyacc

# symlink to either .byte or .opt version
%{_bindir}/ocamlc
%{_bindir}/ocamlcp
%{_bindir}/ocamldep
%{_bindir}/ocamllex
%{_bindir}/ocamlmklib
%{_bindir}/ocamlmktop
%{_bindir}/ocamlobjinfo
%{_bindir}/ocamloptp
%{_bindir}/ocamlprof

# bytecode versions
%{_bindir}/ocamlc.byte
%{_bindir}/ocamlcp.byte
%{_bindir}/ocamldep.byte
%{_bindir}/ocamllex.byte
%{_bindir}/ocamlmklib.byte
%{_bindir}/ocamlmktop.byte
%{_bindir}/ocamlobjinfo.byte
%{_bindir}/ocamloptp.byte
%{_bindir}/ocamlprof.byte

# native code versions
%{_bindir}/ocamlc.opt
%{_bindir}/ocamlcp.opt
%{_bindir}/ocamldep.opt
%{_bindir}/ocamllex.opt
%{_bindir}/ocamlmklib.opt
%{_bindir}/ocamlmktop.opt
%{_bindir}/ocamlobjinfo.opt
%{_bindir}/ocamloptp.opt
%{_bindir}/ocamlprof.opt
%{_bindir}/ocamlopt
%{_bindir}/ocamlopt.byte
%{_bindir}/ocamlopt.opt

%{_libdir}/ocaml/camlheader
%{_libdir}/ocaml/camlheader_ur
%{_libdir}/ocaml/expunge
%{_libdir}/ocaml/eventlog_metadata
%{_libdir}/ocaml/extract_crc
%{_libdir}/ocaml/ld.conf
%{_libdir}/ocaml/Makefile.config
%{_libdir}/ocaml/*.a
%{_libdir}/ocaml/*.cmxs
%{_libdir}/ocaml/*.cmxa
%{_libdir}/ocaml/*.cmx
%{_libdir}/ocaml/*.o
%{_libdir}/ocaml/libasmrun_shared.so
%{_libdir}/ocaml/*.mli
%{_libdir}/ocaml/libcamlrun_shared.so
%{_libdir}/ocaml/threads/*.mli
%{_libdir}/ocaml/threads/*.a
%{_libdir}/ocaml/threads/*.cmxa
%{_libdir}/ocaml/threads/*.cmx
%{_libdir}/ocaml/caml

%files runtime
%license LICENSE
%doc README.adoc Changes
%{_bindir}/ocamlrun
%{_bindir}/ocamlrund
%{_bindir}/ocamlruni
%dir %{_libdir}/ocaml
%{_libdir}/ocaml/*.cmo
%{_libdir}/ocaml/*.cmi
%{_libdir}/ocaml/*.cma
%{_libdir}/ocaml/camlheaderd
%{_libdir}/ocaml/camlheaderi
%{_libdir}/ocaml/stublibs
%dir %{_libdir}/ocaml/threads
%{_libdir}/ocaml/threads/*.cmi
%{_libdir}/ocaml/threads/*.cma
%{_libdir}/ocaml/fedora-ocaml-release

%files source
%license LICENSE
%{_libdir}/ocaml/*.ml

%files ocamldoc
%license LICENSE
%doc ocamldoc/Changes.txt
%{_bindir}/ocamldoc*
%{_libdir}/ocaml/ocamldoc

%files docs
%{_mandir}/man1/*
%{_mandir}/man3/*

%files compiler-libs
%license LICENSE
%dir %{_libdir}/ocaml/compiler-libs
%{_libdir}/ocaml/compiler-libs/*.mli
%{_libdir}/ocaml/compiler-libs/*.cmi
%{_libdir}/ocaml/compiler-libs/*.cmo
%{_libdir}/ocaml/compiler-libs/*.cma
%{_libdir}/ocaml/compiler-libs/*.a
%{_libdir}/ocaml/compiler-libs/*.cmxa
%{_libdir}/ocaml/compiler-libs/*.cmx
%{_libdir}/ocaml/compiler-libs/*.o

%changelog
* Mon Feb 28 2022 Muhammad Falak <mwani@microsoft.com> - 4.13.1-2
- Introduce a patch to remove unused vars in test to enable ptest

* Mon Jan 10 2022 Olivia Crain <oliviacrain@microsoft.com> - 4.13.1-1
- Upgrade to latest upstream release and rebase relevant patches
- Remove arch-specific gating- only applies to arches Mariner does not support
- License verified

* Wed Nov 11 2020 Joe Schmitt <joschmit@microsoft.com> - 4.10.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove annobin integration.

* Thu Feb 27 2020 Richard W.M. Jones <rjones@redhat.com> - 4.10.0-2.fc33
- Add dist tag.

* Tue Feb 25 2020 Richard W.M. Jones <rjones@redhat.com> - 4.10.0-1
- OCaml 4.10.0 final.

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-0.beta1.0.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Richard W.M. Jones <rjones@redhat.com> - 4.10.0-0.beta1
- OCaml 4.10.0+beta1.

* Tue Jan 07 2020 Richard W.M. Jones <rjones@redhat.com> - 4.09.0-13
- Bump release and rebuild.

* Tue Jan 07 2020 Richard W.M. Jones <rjones@redhat.com> - 4.09.0-4
- OCaml 4.09.0 for riscv64

* Tue Dec 10 2019 Richard W.M. Jones <rjones@redhat.com> - 4.09.0-3
- Require redhat-rpm-config to get hardening flags when linking.

* Thu Dec 05 2019 Richard W.M. Jones <rjones@redhat.com> - 4.09.0-2
- OCaml 4.09.0 final.
- Use autosetup, remove old setup line.
- Remove ocamloptp binaries.
- Rename target_camlheader[di] -> camlheader[di] files.
- Remove vmthreads - old threading library which is no longer built.
- Remove x11 subpackage which is obsolete.
- Further fixes to CFLAGS and annobin.

* Fri Aug 16 2019 Richard W.M. Jones <rjones@redhat.com> - 4.08.1-1
- OCaml 4.08.1 final.

* Tue Jul 30 2019 Richard W.M. Jones <rjones@redhat.com> - 4.08.1-0.rc2.1
- OCaml 4.08.1+rc2.
- Include fix for miscompilation of off_t on 32 bit architectures.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.08.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 27 2019 Richard W.M. Jones <rjones@redhat.com> - 4.08.0-1
- OCaml 4.08.0 (RHBZ#1673688).

* Fri Apr 26 2019 Richard W.M. Jones <rjones@redhat.com> - 4.08.0-0.beta3.1
- OCaml 4.08.0 beta 3 (RHBZ#1673688).
- emacs subpackage has been dropped (from upstream):
  https://github.com/ocaml/ocaml/pull/2078#issuecomment-443322613
  https://github.com/Chris00/caml-mode
- Remove ocamlbyteinfo and ocamlpluginfo, neither can be compiled.
- Disable tests on all architectures, temporarily hopefully.
- Package threads/*.mli files.

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.07.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 17 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-3
- Bootstrap from previously build Fedora compiler by default.

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.07.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-1
- OCaml 4.07.0 (RHBZ#1536734).

* Tue Jun 26 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-0.rc1.3
- Enable emacs again on riscv64.

* Tue Jun 19 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-0.rc1.2
- OCaml 4.07.0-rc1 (RHBZ#1536734).

* Tue Jun  5 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-0.beta2.1
- Add RISC-V patch to add debuginfo (DWARF) generation.

* Thu Apr 26 2018 Richard W.M. Jones <rjones@redhat.com> - 4.07.0-0.beta2.0
- OCaml 4.07.0-beta2 (RHBZ#1536734).

* Sun Feb 25 2018 Richard W.M. Jones <rjones@redhat.com> - 4.06.0-5
- Add another couple of RISC-V patches from nojb branch.

* Sat Feb 24 2018 Richard W.M. Jones <rjones@redhat.com> - 4.06.0-4
- Remove mesa* dependencies which are not needed.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.06.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Richard W.M. Jones <rjones@redhat.com> - 4.06.0-2
- Drop non-free documentation (RHBZ#1530647).

* Mon Nov 06 2017 Richard W.M. Jones <rjones@redhat.com> - 4.06.0-1
- New upstream version 4.06.0.
- Enable parallel builds again.
- Rebase patches.
- New binary ocamlcmt.

* Wed Sep 13 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-4
- Add final upstream fix for aarch64/binutils relocation problems.
  https://github.com/ocaml/ocaml/pull/1330

* Wed Sep 06 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-3
- Include interim fix for aarch64/binutils relocation problems.

* Sat Aug 05 2017 Richard W.M. Jones <rjones@redhat.com> - 4.05.0-2
- New upstream version 4.05.0.
- Disable parallel builds for now.
- *.mli files are now included in ocaml-compiler-libs.
- Add possible fix for aarch64 with new binutils.

* Sat Aug 05 2017 Richard W.M. Jones <rjones@redhat.com> - 4.04.2-4
- Disable tests on aarch64 (https://caml.inria.fr/mantis/view.php?id=7602)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.04.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 26 2017 Richard W.M. Jones <rjones@redhat.com> - 4.04.2-1
- New upstream version 4.04.2.
- Fix: ocaml: Insufficient sanitisation allows privilege escalation for
  setuid binaries (CVE-2017-9772) (RHBZ#1464920).

* Wed May 10 2017 Richard W.M. Jones <rjones@redhat.com> - 4.04.1-1
- New upstream version 4.04.1.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.04.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 4.04.0-8
- Rebuild for readline 7.x

* Wed Nov 23 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-7
- riscv: Further fixes for https://github.com/nojb/riscv-ocaml/issues/2

* Tue Nov 22 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-5
- Update RISC-V support to fix
  https://github.com/nojb/riscv-ocaml/issues/2

* Fri Nov 11 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-4
- riscv64: Fix intermediate operands.
  (https://github.com/nojb/riscv-ocaml/issues/1)
- Temporarily disable emacs subpackage on riscv64.

* Wed Nov 09 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-3
- s390x: Fix address of caml_raise_exn in native dynlink modules.
  (https://caml.inria.fr/mantis/view.php?id=7405)

* Tue Nov 08 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-2
- Add support for RISC-V using out of tree support from:
  https://github.com/nojb/riscv-ocaml

* Fri Nov 04 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-1
- New upstream version 4.04.0.

* Thu Nov 03 2016 Richard W.M. Jones <rjones@redhat.com> - 4.04.0-0.1.beta2
- New upstream version 4.04.0+beta2.
- Remove our downstream ppc64 backends, and switch to upstream power backend.
- Use autopatch instead of git for patching.
- Allow parallel builds again.
- Restore ppc stack limits.
- Remove ocamlbuild.
- Add *.byte bytecode binaries.

* Wed May 04 2016 Richard W.M. Jones <rjones@redhat.com> - 4.02.3-3
- CVE-2015-8869 ocaml: sizes arguments are sign-extended from
  32 to 64 bits (RHBZ#1332090)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.02.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jul 28 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.3-1
- New upstream version: 4.02.3.

* Mon Jun 29 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.2-4
- Couple of minor build fixes for ppc64 and ppc64le.
- ppc64/ppc64le: Fix behaviour of Int64.max_int ÷ -1 (RHBZ#1236615).

* Fri Jun 26 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.2-2
- Enable the test suite during the build.  Currently the results are
  only advisory.

* Tue Jun 23 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.2-1
- New upstream version: 4.02.2.
- No need for a mass rebuild, since this version is identical to RC1.

* Tue Jun 16 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.2-0.rc1.1
- New upstream version: 4.02.2+rc1.
- Dropped two aarch64 patches which are now included upstream.
- Includes libasmrun_shared.so (RHBZ#1195025).

* Wed Jun 10 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-7
- aarch64: Use upstream version of patch that fixes RHBZ#1224815.

* Tue Jun 09 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-6
- aarch64: AArch64 backend generates invalid asm: conditional branch
  out of range (RHBZ#1224815).

* Thu May 28 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-5
- ppc64le: Fix calling convention of external functions with > 8 parameters
  (RHBZ#1225995).

* Wed May  6 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-4
- Fix gdb stack traces on aarch64 (upstream PR6490).  Thanks: Mark Shinwell.

* Thu Apr 23 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-3
- ppc, ppc64, ppc64le: Properly mark stack as non-executable.
  The upstream fix was not applied completely.

* Thu Feb 26 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-2
- Kill dependency on rpm-build.  Added in 2009, apparently by accident.
  (Thanks: Jon Ludlam)

* Mon Feb 16 2015 Richard W.M. Jones <rjones@redhat.com> - 4.02.1-1
- New upstream version 4.02.1.
- Rebase patches on top.

* Fri Oct 24 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-6
- Fixes for ppc64/ppc64le (RHBZ#1156300).

* Mon Oct 20 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-4
- ocaml-emacs should require emacs(bin) (RHBZ#1154513).

* Thu Sep 11 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-3
- Use -fno-strict-aliasing when building the compiler (RHBZ#990540).
- ppc, ppc64, ppc64le: Mark stack as non-executable.

* Tue Sep  9 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-2
- Fix bug in argument parsing (RHBZ#1139790).

* Sat Aug 30 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-1
- New upstream OCaml 4.02.0 final.
- Add patch for ocaml-camlimages
  (see http://caml.inria.fr/mantis/view.php?id=6517)

* Fri Aug 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.11.gitc48fc015
- Rebase on top of OCaml 4.02+rc1 (same as git commit c48fc015).

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.02.0-0.10.git10e45753
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 08 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.9
- Add fix for Coq build issue:
  http://caml.inria.fr/mantis/view.php?id=6507

* Fri Aug 01 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.8
- Rebase on top of 4.02.0 beta commit 10e45753.

* Sat Jul 19 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.7
- Rebase on top of 4.02.0 beta commit c4f3a6c7.
- Remove the patch to disable CSE, since that problem is fixed upstream.
- Remove the patch fixing caml_callback2 on aarch64 since that patch is
  now upstream.
- Make the compiler depend on ocaml-runtime explicitly.

* Tue Jul 15 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.5
- Disable CSE optimization which is broken on armv7hl and aarch64.
- Fix broken caml_callback2 on aarch64
  http://caml.inria.fr/mantis/view.php?id=6489

* Sat Jul 12 2014 Richard W.M. Jones <rjones@redhat.com> - 4.02.0-0.1
- Update to 4.02.0-beta1 + patches from the upstream 4.02 branch.
- REMOVED labltk and camlp4 packages, since these are now packaged
  separately upstream.
- Upstream includes fix for stack alignment issues on i686, so remove hack.
- Upstream now uses mkstemp where available, so patch removed.
- Upstream includes Aarch64 backend, so remove our own backport.
- Drop BR on ocaml-srpm-macros, since it is now included in Fedora.

* Thu Jun 26 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-20
- BR binutils-devel so ocamlobjinfo supports *.cmxs files (RHBZ#1113735).

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.01.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.01.0-18
- Rebuilt for https://fedoraproject.org/wiki/Changes/f21tcl86

* Sat May 10 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-17
- Mark stack as non-executable on ARM (32 bit) and Aarch64.

* Tue Apr 22 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-16
- Remove ocaml-srpm-macros subpackage.
  This is now a separate package, see RHBZ#1087893.

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-15
- Fix s390x builds (no native compiler).

* Tue Apr 15 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-14
- Remove ExclusiveArch.
- Add ocaml-srpm-macros subpackage containing arch macros.
- See: RHBZ#1087794

* Mon Apr 14 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-13
- Fix aarch64 relocation problems again.
  Earlier patch was dropped accidentally.

* Wed Apr  9 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-12
- Add ppc64le support (thanks: Michel Normand) (RHBZ#1077767).

* Tue Apr  1 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-11
- Fix --flag=arg patch (thanks: Anton Lavrik, Ignas Vyšniauskas).

* Mon Mar 24 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-10
- Include a fix for aarch64 relocation problems
  http://caml.inria.fr/mantis/view.php?id=6283

* Wed Jan  8 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-8
- Don't use ifarch around Patch lines, as it means the patch files
  don't get included in the spec file.

* Mon Jan  6 2014 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-7
- Work around gcc stack alignment issues, see
  http://caml.inria.fr/mantis/view.php?id=5700

* Tue Dec 31 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-6
- Add aarch64 (arm64) code generator.

* Thu Nov 21 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-4
- Add bundled(md5-plumb) (thanks: Tomas Mraz).
- Add NON-upstream (but being sent upstream) patch to allow --flag=arg
  as an alternative to --flag arg (RHBZ#1028650).

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-3
- Disable -lcurses.  This is not actually used, just linked with unnecessarily.

* Sat Sep 14 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-2
- Fix the build on ppc64.

* Fri Sep 13 2013 Richard W.M. Jones <rjones@redhat.com> - 4.01.0-1
- Update to new major version OCaml 4.01.0.
- Rebase patches.
- Remove bogus Requires 'ncurses-devel'.  The base ocaml package already
  pulls in the library implicitly.
- Remove bogus Requires 'gdbm-devel'.  Nothing in the source mentions gdbm.
- Use mkstemp instead of mktemp in ocamlyacc.
- Add LICENSE as doc to some subpackages to keep rpmlint happy.
- Remove .ignore file from some packages.
- Remove period from end of Summary.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 16 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.1-1
- Update to upstream version 4.00.1.
- Clean up the spec file further.

* Thu Aug 16 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-2
- ppc supports natdynlink.

* Sat Jul 28 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-1
- Upgrade to OCaml 4.00.0 official release.
- Remove one patch (add -lpthread) which went upstream.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.00.0-0.6.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 10 2012 Richard W.M. Jones <rjones@redhat.com> - 4.00.0-0.5.beta2
- No change, just fix up changelog.

* Thu Jun  7 2012 Richard W.M. Jones <rjones@redhat.com> 4.00.0-0.3.beta2
- Upgrade to OCaml 4.00.0 beta 2.
- The language is now officially called OCaml (not Objective Caml, O'Caml etc)
- Rebase patches on top:
  . New ARM backend patch no longer required, since upstream.
  . Replacement config.guess, config.sub no longer required, since upstream
    versions are newer.
- PPC64 backend rebased and fixed.
  . Increase the default size of the stack when compiling.
- New tool: ocamloptp (ocamlopt profiler).
- New VERSION file in ocaml-runtime package.
- New ocaml-compiler-libs subpackage.
- Rearrange ExclusiveArch alphanumerically.
- alpha, ia64 native backends have been removed upstream, so they are
  no longer supported as native compiler targets.
- Remove defattr.
- Make OCaml dependency generator self-contained so it doesn't need
  previous version of OCaml around.

* Wed Jun  6 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-12
- ppc64: Include fix for minor heap corruption because of unaligned
  minor heap register (RHBZ#826649).
- Unset MAKEFLAGS before running build.

* Wed Jun  6 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-11
- ppc64: Fix position of stack arguments to external C functions
  when there are more than 8 parameters.

* Tue Jun  5 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-10
- Include patch to link dllthreads.so with -lpthread explicitly, to
  fix problem with 'pthread_atfork' symbol missing (statically linked)
  on ppc64.

* Sun Jun  3 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-9
- Include svn rev 12548 to fix invalid generation of Thumb-2 branch
  instruction TBH (upstream PR#5623, RHBZ#821153).

* Wed May 30 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-8
- Modify the ppc64 patch to reduce the delta between power64 and
  upstream power backends.
- Clean up the spec file and bring it up to modern standards.
  * Remove patch fuzz directive.
  * Remove buildroot directive.
  * Rearrange source unpacking.
  * Remove chmod of GNU config.* files, since git does it.
  * Don't need to remove buildroot in install section.
  * Remove clean section.
  * git am </dev/null to avoid hang (thanks Adam Jackson).
- Note there is no functional change in the above.

* Tue May 29 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-6
- Move patches to external git repo:
  http://git.fedorahosted.org/git/?p=fedora-ocaml.git
  There should be no change introduced here.

* Tue May 15 2012 Karsten Hopp <karsten@redhat.com> 3.12.1-4
- ppc64 got broken by the new ARM backend, add a minor patch

* Sat Apr 28 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-3
- New ARM backend by Benedikt Meurer, backported to OCaml 3.12.1.
  This has several advantages, including enabling natdynlink on ARM.
- Provide updated config.guess and config.sub (from OCaml upstream tree).

* Thu Jan 12 2012 Richard W.M. Jones <rjones@redhat.com> 3.12.1-2
- add back ocaml-ppc64.patch for ppc secondary arch, drop .cmxs files
  from file list on ppc (cherry picked from F16 - this should have
  gone into Rawhide originally then been cherry picked back to F16)

* Fri Jan  6 2012 Richard W.M. Jones <rjones@redhat.com> - 3.12.1-1
- New upstream version 3.12.1.  This is a bugfix update.

* Thu Dec  8 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-7
- Allow this package to be compiled on platforms without native
  support and/or natdynlink, specifically ppc64.  This updates (and
  hopefully does not break) DJ's previous *.cmxs change for arm.

* Fri Sep 23 2011 DJ Delorie <dj@redhat.com> - 3.12.0-6
- Add arm type directive patch.
- Allow more arm arches.
- Don't package *.cmxs on arm.

* Wed Mar 30 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-5
- Fix for invalid assembler generation (RHBZ#691896).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan  5 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-3
- Rebuild with self.

* Tue Jan  4 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-2
- Try depending on OCaml BR to fix:
  /usr/lib/rpm/ocaml-find-provides.sh: /builddir/build/BUILDROOT/ocaml-3.12.0-1.fc15.i386/usr/bin/ocamlobjinfo: /usr/bin/ocamlrun: bad interpreter: No such file or directory

* Tue Jan  4 2011 Richard W.M. Jones <rjones@redhat.com> - 3.12.0-1
- New upstream version 3.12.0.
  http://fedoraproject.org/wiki/Features/OCaml3.12
- Remove ppc64 support patch.
- Rebase rpath removal patch.
- ocamlobjinfo is now an official tool, so no need to compile it by hand.
  Add objinfo_helper.
- Disable ocamlplugininfo.
- Remove addlabels, scrapelabels.
- Remove ocaml/stublibs/dlltkanim.so.

* Fri Jan 29 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-2
- Update reference manual to latest version from website.

* Wed Jan 20 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-1
- Update to 3.11.2 official release.

* Tue Jan  5 2010 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-0.rc1.2
- ocaml-labltk-devel should require tcl-devel and tk-devel.

* Tue Dec 29 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.2-0.rc1.1
- Update to (release candidate) 3.11.2+rc1.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-8
- Use __ocaml_requires_opts / __ocaml_provides_opts.

* Wed Dec 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-7
- Remove ocaml-find-{requires,provides}.sh from this package.  These are
  now in upstream RPM 4.8 (RHBZ#545116).
- define -> global in a few places.

* Thu Nov 05 2009 Dennis Gilmore <dennis@ausil.us> - 3.11.1-6
- include sparcv9 in the arch list

* Tue Oct 27 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-5
- Install ocaml.info files correctly (RHBZ#531204).

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-4
- Set includes so building the *info programs works without
  having OCaml already installed.

* Fri Oct 16 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-3
- Add ocamlbyteinfo and ocamlplugininfo programs from Debian.

* Sun Oct  4 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-2
- ocaml-find-requires.sh: Calculate runtime version using ocamlrun
  -version instead of fedora-ocaml-release file.

* Wed Sep 30 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-1
- OCaml 3.11.1 (this is virtually the same as the release candidate
  that we were using for Fedora 12).

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.1-0.rc1.2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun  3 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc1.2
- Remember to upload the source this time.

* Wed Jun  3 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc1.1
- New upstream release candidate 3.11.1+rc1.
- Remove ocamlbuild -where patch (now upstream).

* Tue Jun  2 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.3
- Move dllgraphics.so into runtime package (RHBZ#468506).

* Tue May 26 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.2
- Backport ocamlbuild -where fix.

* Fri May 22 2009 Richard W.M. Jones <rjones@redhat.com> - 3.11.1-0.rc0.1
- 3.11.1 release candidate 0.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-1
- Official release of 3.11.0.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.6.rc1
- Fixed sources file.

* Thu Dec  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.5.rc1
- New upstream version 3.11.0+rc1.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0-0.4.beta1
- Rebuild.

* Thu Nov 20 2008 Rex Dieter <rdieter@fedoraproject.org> - 3.11.0-0.3.beta1
- fix NVR to match packaging guidelines

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-2
- Fix Invalid_argument("String.index_from") with patch from upstream.

* Tue Nov 18 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11.0+beta1-1
- Rebuild for major new upstream release of 3.11.0 for Fedora 11.

* Fri Aug 29 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-5
- Rebuild with patch fuzz.

* Mon Jun  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-4
- Add ocaml-3.11-dev12-no-executable-stack.patch (bz #450551).

* Wed Jun  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-3
- ocaml-ocamldoc provides ocamldoc (bz #449931).
- REMOVED provides of labltk, camlp4.  Those are libraries and all
  packages should now depend on ocaml-labltk / ocaml-camlp4 / -devel
  as appropriate.

* Thu May  8 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-2
- Pass MAP_32BIT to mmap (bz #445545).

* Mon Apr 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.2-1
- New upstream version 3.10.2 for Fedora 10.
- Cleaned up several rpmlint errors & warnings.

* Fri Feb 29 2008 David Woodhouse <dwmw2@infradead.org> - 3.10.1-2
- ppc64 port

* Tue Feb 12 2008 Richard W.M. Jones <rjones@redhat.com> - 3.10.1-1
- new upstream version 3.10.1

* Fri Jan  4 2008 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-8
- patch for building with tcl/tk 8.5

* Thu Sep  6 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-7
- Run chrpath to delete rpaths used on some of the stublibs.
- Ignore Parsetree module in dependency calculation.
- Fixed ocaml-find-{requires,provides}.sh regexp calculation so it doesn't
  over-match module names.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-6
- ocaml-runtime provides ocaml(runtime) = 3.10.0, and
  ocaml-find-requires.sh modified so that it adds this requires
  to other packages.  Now can upgrade base ocaml packages without
  needing to rebuild everything else.

* Mon Sep  3 2007 Richard W.M. Jones <rjones@redhat.com> - 3.10.0-5
- Don't include the release number in fedora-ocaml-release file, so
  that packages built against this won't depend on the Fedora release.

* Wed Aug 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-4
- added BR util-linux-ng

* Wed Aug 29 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-3
- added BR gawk

* Tue Aug 28 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 3.10.0-2
- Rebuild for selinux ppc32 issue.

* Sat Jun  2 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.10.0-1
- new version 3.10.0
- split off devel packages
- rename subpackages to use ocaml- prefix

* Thu May 24 2007 Gerard Milmeister <gemi@bluewin.ch> - 3.09.3-2
- added ocamlobjinfo

* Sat Dec  2 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.3-1
- new version 3.09.3

* Mon Aug 28 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-2
- Rebuild for FE6

* Sun Apr 30 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.2-1
- new version 3.09.2

* Fri Feb 17 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-2
- Rebuild for Fedora Extras 5

* Thu Jan  5 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.1-1
- new version 3.09.1

* Sun Jan  1 2006 Gerard Milmeister <gemi@bluewin.ch> - 3.09.0-1
- new version 3.09.0

* Sun Sep 11 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.4-1
- New Version 3.08.4

* Wed May 25 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-5
- Bump and re-release as last build failed due to rawhide syncing.

* Sun May 22 2005 Toshio Kuratomi <toshio-tiki-lounge.com> - 3.08.3-4
- Fix for gcc4 and the 32 bit assembly in otherlibs/num.
- Fix to allow compilation with RPM_OPT_FLAG defined -O level.

* Sun May 22 2005 Jeremy Katz <katzj@redhat.com> - 3.08.3-3
- rebuild on all arches

* Fri Apr  8 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Mar 26 2005 Gerard Milmeister <gemi@bluewin.ch> - 3.08.3-1
- New Version 3.08.3

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-2
- Added patch for removing rpath from shared libs

* Sat Feb 12 2005 Gerard Milmeister <gemi@bluewin.ch> - 0:3.08.2-1
- New Version 3.08.2

* Thu Dec 30 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> - 0:3.07-6
- add -x11lib _prefix/X11R6/_lib to configure; fixes labltk build
  on x86_64

* Tue Dec  2 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.5
- ocamldoc -> ocaml-ocamldoc
- ocaml-doc -> ocaml-docs

* Fri Nov 28 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.4
- Make separate packages for labltk, camlp4, ocamldoc, emacs and documentation

* Thu Nov 27 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.2
- Changed license tag
- Register info files
- Honor RPM_OPT_FLAGS
- New Patch

* Fri Oct 31 2003 Gerard Milmeister <gemi@bluewin.ch> - 0:3.07-0.fdr.1
- First Fedora release

* Mon Oct 13 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Updated to 3.07.

* Wed Apr  9 2003 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Rebuilt for Red Hat 9.

* Tue Nov 26 2002 Axel Thimm <Axel.Thimm@physik.fu-berlin.de>
- Added _mandir/mano/* entry
