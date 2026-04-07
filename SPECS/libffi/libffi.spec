# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with bootstrap

%global multilib_arches %{ix86} x86_64

Name:		libffi
Version:	3.5.2
Release:	1%{?dist}
Summary:	A portable foreign function interface library
# No license change for 3.5.2
# No license change for 3.5.1
# No license change for 3.4.8
# No license change for 3.4.7
# No license change for 3.4.6
# The following SPDX licenses are extracted from the sources using
# ScanCode 32.0.8 on build libffi-3.4.4-7.fc40:
#
# MIT - Most of the project sources (Required)
# CC-PDDC - src/dlmalloc.c (Required)
# mit OR gpl-3.0 - ltmain.sh (Ignored)
# mit OR gpl-1.0-plus - ltmain.sh (Ignored)
# gpl-2.0-plus WITH libtool-exception-2.0 - ltmain.sh, libtool.m4, configure (Ignored, not shipped)
# warranty-disclaimer - ltmain.sh (Ignored)
# unknown-license-reference - ltmain.sh (Ignored)
# gpl-2.0-plus - Used by build system only (Ignored)
# gpl-2.0 - Used by build system only (Ignored)
# free-unknown - config.guess, config.sub (Ignored)
# fsf-ap - Used by build system only (Ignored)
# fsf-free - Used by build system only (Ignored)
# fsf-unlimited - Used by build system only (Ignored)
# fsf-unlimited-no-warranty - Used by build system only (Ignored)
# gpl-1.0-plus - False positive in texinfo.tex (Ignored)
# gpl-3.0-plus WITH tex-exception - texinfo.tex used in libffi-devel docs (Required)
# gpl-2.0-plus WITH autoconf-simple-exception-2.0 - Used by build system only (Ignored)
# gpl-3.0 - Used by build system only (Ignored)
# gpl-3.0-plus - Used by the testsuite only (Ignored)
# gpl-3.0-plus WITH autoconf-exception-2.0 - Used by build system only (Ignored)
# gpl-3.0-plus WITH autoconf-simple-exception - Used by build system only (Ignored)
# mpl-1.1 OR gpl-2.0-plus OR lgpl-2.1-plus - Not used in build (Ignored)
# public-domain - Used by build system only (Ignored)
# x11-xconsortium - Used by build system only (Ignored)
License:	MIT AND CC-PDDC AND (GPL-3.0-or-later WITH Texinfo-exception)
URL:		http://sourceware.org/libffi

Source0:	https://github.com/libffi/libffi/releases/download/v%{version}/libffi-%{version}.tar.gz
Source1:	ffi-multilib.h
Source2:	ffitarget-multilib.h

BuildRequires: make
BuildRequires: gcc
%if %{without bootstrap}
BuildRequires: gcc-c++
BuildRequires: dejagnu
%endif

%description
Compilers for high level languages generate code that follow certain
conventions.  These conventions are necessary, in part, for separate
compilation to work.  One such convention is the "calling convention".
The calling convention is a set of assumptions made by the compiler
about where function arguments will be found on entry to a function.  A
calling convention also specifies where the return value for a function
is found.  

Some programs may not know at the time of compilation what arguments
are to be passed to a function.  For instance, an interpreter may be
told at run-time about the number and types of arguments used to call a
given function.  `Libffi' can be used in such programs to provide a
bridge from the interpreter program to compiled code.

The `libffi' library provides a portable, high level programming
interface to various calling conventions.  This allows a programmer to
call any function specified by a call interface description at run time.

FFI stands for Foreign Function Interface.  A foreign function
interface is the popular name for the interface that allows code
written in one language to call code written in another language.  The
`libffi' library really only provides the lowest, machine dependent
layer of a fully featured foreign function interface.  A layer must
exist above `libffi' that handles type conversions for values passed
between the two languages.  

%package	devel
Summary:	Development files for %{name}
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description	devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -p1

%build
# --disable-multi-os-directory is used because otherwise, on riscv64, the
# library is installed under ${_libdir}/lp64d, which we don't want. Other
# architectures don't have the same problem so they're unaffected.
%configure --disable-static --disable-multi-os-directory
%make_build

%check
%if %{without bootstrap}
%make_build check
%endif

%install
%make_install

find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Determine generic arch target name for multilib wrapper
basearch=%{_arch}
%ifarch %{ix86}
basearch=i386
%endif

mkdir -p $RPM_BUILD_ROOT%{_includedir}
%ifarch %{multilib_arches}
# Do header file switcheroo to avoid file conflicts on systems where you
# can have both a 32- and 64-bit version of the library, and they each need
# their own correct-but-different versions of the headers to be usable.
for i in ffi ffitarget; do
  mv $RPM_BUILD_ROOT%{_includedir}/$i.h $RPM_BUILD_ROOT%{_includedir}/$i-${basearch}.h
done
install -m644 %{SOURCE1} $RPM_BUILD_ROOT%{_includedir}/ffi.h
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/ffitarget.h
%endif

%ldconfig_scriptlets

%files
%license LICENSE
%doc README.md
%{_libdir}/libffi.so.8
%{_libdir}/libffi.so.8.2.0

%files devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/ffi*.h
%{_libdir}/*.so
%{_mandir}/man3/*.gz
%{_infodir}/libffi.info.*

%changelog
* Fri Sep  5 2025 DJ Delorie <dj@redhat.com> - 3.5.2-1
- Rebase to libffi 3.5.1.

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 13 2025 DJ Delorie <dj@redhat.com> - 3.5.1-1
- Rebase to libffi 3.5.1.

* Wed May 07 2025 DJ Delorie <dj@redhat.com> - 3.4.8-1
- Rebase to libffi 3.4.8.

* Fri Apr 04 2025 Andrea Bolognani <abologna@redhat.com> - 3.4.7-4
- Fix riscv64 build (thanks David Abdurachmanov and Rich Jones)

* Thu Mar 27 2025 DJ Delorie <dj@redhat.com> - 3.4.7-3
- Regenerate configure for previous patch(#2313598)

* Thu Mar 06 2025 DJ Delorie <dj@redhat.com> - 3.4.7-2
- Add PPC64 static trampoline support (#2313598)

* Tue Feb 18 2025 DJ Delorie <dj@redhat.com> - 3.4.7-1
- Rebase to libffi 3.4.7.

* Wed Jan 22 2025 DJ Delorie <dj@redhat.com> - 3.4.6-5
- Fix FTBFS due to C23 compiler (#2340729)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug 21 2024 Carlos O'Donell <carlos@redhat.com> 3.4.6-3
- Fix AArch64 BTI enablement issues (#2305877)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 18 2024 DJ Delorie <dj@redhat.com> - 3.4.6-1
- Rebase to libffi 3.4.6.

* Thu Feb 29 2024 Carlos O'Donell <carlos@redhat.com> - 3.4.4-8
- Analyze libffi-3.4.4-7.fc40 sources for license information
- Migrate License field to SPDX identifiers for
  https://docs.fedoraproject.org/en-US/legal/allowed-licenses/
  https://docs.fedoraproject.org/en-US/legal/update-existing-packages
  (#2222084)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 02 2024 Florian Weimer <fweimer@redhat.com> - 3.4.4-5
- Add missing declaration of open_temp_exec_file

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 DJ Delorie <dj@redhat.com> - 3.4.4-3
- Enable static trampolines

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Oct 28 2022 DJ Delorie <dj@redhat.com> - 3.4.4-1
- Rebase to libffi 3.4.4.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jan 31 2022 Dan Horák <dan[at]danny.cz> - 3.4.2-8
- Fix handling Float128 structs on ppc64le (#2045797)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Jan 08 2022 Miro Hrončok <mhroncok@redhat.com> - 3.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Wed Sep 15 2021 Carlos O'Donell <codonell@redhat.com> - 3.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/LIBFFI34

* Wed Sep 15 2021 Carlos O'Donell <carlos@redhat.com> - 3.4.2-4
- Harmonize spec file layout with downstream.

* Wed Aug 11 2021 Carlos O'Donell <carlos@redhat.com> - 3.4.2-3
- Rebuild package and bump NEVRA.

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Carlos O'Donell <carlos@redhat.com> - 3.4.2-1
- Rebase to libffi 3.4.2.
 
* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Carlos O'Donell <carlos@redhat.com> - 3.1-27
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Apr 30 2020 DJ Delorie <idj@redhat.com> - 3.1-25
- Add $LIBFFI_TMPDIR environment variable support (#1667620)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul  9 2019 Florian Weimer <fweimer@redhat.com> - 3.1-22
- Run test suite during build (#1727088)

* Wed Jun 19 2019 Anthony Green <green@redhat.com> - 3.1-21
- Fix license tag

* Wed Apr 24 2019 Björn Esser <besser82@fedoraproject.org> - 3.1-20
- Remove hardcoded gzip suffix from GNU info pages

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Jul 22 2018 Peter Robinson <pbrobinson@fedoraproject.org> 3.1-28
- Fix FTBFS

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.1-15
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul  5 2017 Jens Petersen <petersen@redhat.com> - 3.1-12
- protect install-info in the rpm scriptlets
  https://fedoraproject.org/wiki/Packaging:Scriptlets#Texinfo

* Tue Jun 20 2017 Anthony Green <green@redhat.com> - 3.1-11
- fix exec stack problem on aarch64 build

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jan 15 2015 Peter Robinson <pbrobinson@fedoraproject.org> 3.1-7
- Add patch to fix issues on aarch64 (rhbz 1174037)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Tom Callaway <spot@fedoraproject.org> - 3.1-5
- fix license handling

* Sun Jun 29 2014 Anthony Green <green@redhat.com> - 3.1-4
- fix exec stack problem on 32-bit build

* Thu Jun 12 2014 Dan Horák <dan[at]danny.cz> - 3.1-3
- fix header path in pkgconfig file

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Anthony Green <green@redhat.com> - 3.1-1
- fix non-multiarch builds (arm).

* Mon May 19 2014 Anthony Green <green@redhat.com> - 3.1-0
- update to 3.1.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 28 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.13-4
- fix typos in wrapper headers

* Mon May 27 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.13-3
- make header files multilib safe

* Sat May 25 2013 Tom Callaway <spot@fedoraproject.org> - 3.0.13-2
- fix incorrect header pathing (and .pc file)

* Wed Mar 20 2013 Anthony Green <green@redhat.com> - 3.0.13-1
- update to 3.0.13

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jan 14 2013 Dennis Gilmore <dennis@ausil.us> - 3.0.11-1
- update to 3.0.11

* Fri Nov 02 2012 Deepak Bhole <dbhole@redhat.com> - 3.0.10-4
- Fixed source location

* Fri Aug 10 2012 Dennis Gilmore <dennis@ausil.us> - 3.0.10-3
- drop back to 3.0.10, 3.0.11 was never pushed anywhere as the soname bump broke buildroots
- as 3.0.11 never went out no epoch needed.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 13 2012 Anthony Green <green@redhat.com> - 3.0.11-1
- Upgrade to 3.0.11.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 23 2011 Anthony Green <green@redhat.com> - 3.0.10-1
- Upgrade to 3.0.10. 

* Fri Mar 18 2011 Dan Horák <dan[at]danny.cz> - 3.0.9-3
- added patch for being careful when defining relatively generic symbols

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 29 2009 Anthony Green <green@redhat.com> - 3.0.9-1
- Upgrade

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jul 08 2008 Anthony Green <green@redhat.com> 3.0.5-1
- Upgrade to 3.0.5

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 3.0.1-1
- Upgrade to 3.0.1

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 2.99.9-1
- Upgrade to 2.99.9
- Require pkgconfig for the devel package.
- Update summary.

* Fri Feb 15 2008 Anthony Green <green@redhat.com> 2.99.8-1
- Upgrade to 2.99.8

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.7-1
- Upgrade to 2.99.7

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.6-1
- Upgrade to 2.99.6

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.4-1
- Upgrade to 2.99.4

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.3-1
- Upgrade to 2.99.3

* Thu Feb 14 2008 Anthony Green <green@redhat.com> 2.99.2-1
- Created.
