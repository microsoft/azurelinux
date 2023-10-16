%define _gnu %{nil}
%define _programprefix eu-

Summary:        A collection of utilities and DSOs to handle compiled objects
Name:           elfutils
Version:        0.189
Release:        1%{?dist}
License:        GPLv3+ AND (GPLv2+ OR LGPLv3+)
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://sourceware.org/elfutils
Source0:        https://sourceware.org/elfutils/ftp/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:  bison >= 1.875
BuildRequires:  bzip2-devel
BuildRequires:  flex >= 2.5.4a
BuildRequires:  gcc >= 4.1.2-33
BuildRequires:  gettext
BuildRequires:  glibc >= 2.7
BuildRequires:  m4

Requires:       %{name}-default-yama-scope = %{version}-%{release}
Requires:       %{name}-libelf = %{version}-%{release}
Requires:       bzip2-libs
Requires:       glibc >= 2.7

Provides:       %{name}-libs = %{version}-%{release}

Obsoletes:      libelf
Obsoletes:      libelf-devel

%description
Elfutils is a collection of utilities, including ld (a linker),
nm (for listing symbols from object files), size (for listing the
section sizes of an object or archive file), strip (for discarding
symbols), readelf (to see the raw ELF file structures), and elflint
(to check for well-formed ELF files).  Also included are numerous
helper libraries which implement DWARF, ELF, and machine-specific ELF
handling.

%package default-yama-scope
Summary:        Default yama attach scope sysctl setting
License:        GPLv2+ OR LGPLv3+
# For the sysctl_apply macro we need systemd as build requires.
# We also need systemd-sysctl in post to apply the default kernel config.
# But this creates a circular requirement (see below). And it would always
# pull in systemd even in build containers that don't really need it.
# Luckily systemd is normally always installed already. The only times it
# might not is when we do an initial install (and the cyclic dependency
# chain might be broken) or when installing into a container. In the first
# case we'll reboot soon to apply the default kernel config. In the second
# case we really require that the host has the correct kernel config so it
# also is available inside the container. So if we have weak dependencies
# use Recommends (sadly Recommends(post) doesn't exist). This works because
# in all cases that really matter systemd will already be installed. #1599083
Recommends:     systemd
Provides:       default-yama-scope = %{version}-%{release}
BuildArch:      noarch

%description default-yama-scope
Yama sysctl setting to enable default attach scope settings
enabling programs to use ptrace attach, access to
/proc/PID/{mem,personality,stack,syscall}, and the syscalls
process_vm_readv and process_vm_writev which are used for
interprocess services, communication and introspection
(like synchronisation, signaling, debugging, tracing and
profiling) of processes.

%package devel
Summary:        Development libraries to handle compiled objects.
License:        GPLv2+ OR LGPLv3+
Group:          Development/Tools

Requires:       %{name} = %{version}-%{release}
Requires:       %{name}-libelf-devel = %{version}-%{release}

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects.  libebl provides some
higher-level ELF access functionality.  libdw provides access to
the DWARF debugging information.  libasm provides a programmable
assembler interface.

%package devel-static
Summary:        Static archives to handle compiled objects.
License:        GPLv2+ OR LGPLv3+
Group:          Development/Tools

Requires:       %{name}-devel = %{version}-%{release}

%description devel-static
The elfutils-devel-static archive contains the static archives
with the code the handle compiled objects.

%package libelf
Summary:        Library to read and write ELF files.
License:        GPLv2+ OR LGPLv3+
Group:          Development/Tools

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%package libelf-devel
Summary:        Development support for libelf
License:        GPLv2+ OR LGPLv3+
Group:          Development/Tools

Requires:       %{name}-libelf = %{version}-%{release}

Conflicts:      libelf-devel

%description libelf-devel
The elfutils-libelf-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%package libelf-devel-static
Summary:        Static archive of libelf
License:        GPLv2+ OR LGPLv3+
Group:          Development/Tools

Requires:       %{name}-libelf-devel = %{version}-%{release}

Conflicts:      libelf-devel

%description libelf-devel-static
The elfutils-libelf-static package contains the static archive
for libelf.

%package libelf-lang
Summary:        Additional language files for elfutils
License:        GPLv3+ AND (GPLv2+ OR LGPLv3+)
Group:          Development/Tools

Requires:       %{name}-libelf = %{version}-%{release}

%description libelf-lang
These are the additional language files of elfutils.

%prep
%setup -q

%build
%configure \
    --program-prefix=%{_programprefix} \
    --disable-debuginfod \
    --enable-libdebuginfod=dummy
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}%{_prefix}

%makeinstall

chmod +x %{buildroot}%{_libdir}/lib*.so*
#chmod +x %{buildroot}%{_libdir}/elfutils/lib*.so*

install -Dm0644 config/10-default-yama-scope.conf %{buildroot}%{_sysconfdir}/sysctl.d/10-default-yama-scope.conf

# XXX Nuke unpackaged files
{
  pushd %{buildroot}
  rm -f .%{_bindir}/eu-ld
  rm -f .%{_includedir}/elfutils/libasm.h
  rm -f .%{_libdir}/libasm.so
  rm -f .%{_libdir}/libasm.a
  popd
}

%find_lang %{name}

%check
# Disable tests "run-strip-strmerge.sh" and "run-elflint-self.sh".
# These tests are expected to fail with "unknown program header entry type 0x6474e553" errors.
# Root cause appears to be a program header from binutils which our version of elfutils is unaware of.
sed -i 's/run-strip-groups.sh run-strip-reloc.sh run-strip-strmerge.sh/run-strip-groups.sh run-strip-reloc.sh/g' ./tests/Makefile.am
sed -i 's/run-elflint-test.sh run-elflint-self.sh run-ranlib-test.sh/run-elflint-test.sh run-ranlib-test.sh/g' ./tests/Makefile.am
sed -i 's/run-strip-reloc.sh run-strip-strmerge.sh/run-strip-reloc.sh/g' ./tests/Makefile.in
sed -i 's/run-elflint-test.sh run-elflint-self.sh run-ranlib-test.sh/run-elflint-test.sh run-ranlib-test.sh/g' ./tests/Makefile.in

# As per the comment in the test "run-reverse-sections-self.sh"; these tests really make sense for ET_REL files and not any file.
# The test which specifically checks for files for reversal in sections passes.
# Skip this test Temporarily for CBL-Mariner
sed -i 's/run-reverse-sections.sh run-reverse-sections-self.sh/run-reverse-sections.sh/g' ./tests/Makefile.am
sed -i 's/run-reverse-sections-self.sh run-copyadd-sections.sh/run-copyadd-sections.sh/g' ./tests/Makefile.in

make %{?_smp_mflags} check


%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post default-yama-scope
# Due to circular dependencies might not be installed yet, so double check.
# (systemd -> elfutils-libs -> default-yama-scope -> systemd)
if [ -x %{_libdir}/systemd/systemd-sysctl ] ; then
%if 0%{?sysctl_apply}
  %{sysctl_apply} 10-default-yama-scope.conf
%else
  %{_libdir}/systemd/systemd-sysctl %{_sysconfdir}/sysctl.d/10-default-yama-scope.conf > /dev/null 2>&1 || :
%endif
fi

%post libelf -p /sbin/ldconfig

%postun libelf -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING COPYING-GPLV2 COPYING-LGPLV3
%doc README TODO CONTRIBUTING
%{_bindir}/eu-*
%{_bindir}/debuginfod-find
%{_libdir}/libasm-%{version}.so
%{_libdir}/libdw-%{version}.so
%{_libdir}/libasm.so.*
%{_libdir}/libdw.so.*
%{_mandir}/man1/*
%exclude %{_mandir}/man7/*

%files default-yama-scope
%{_sysconfdir}/sysctl.d/10-default-yama-scope.conf

%files devel
%defattr(-,root,root)
%{_includedir}/dwarf.h
/etc/profile.d/debuginfod.csh
/etc/profile.d/debuginfod.sh
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwfl.h
%{_includedir}/elfutils/known-dwarf.h
%{_includedir}/elfutils/libdwelf.h
%{_includedir}/elfutils/debuginfod.h
%{_libdir}/libdw.so
%{_libdir}/libdebuginfod*
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%files devel-static
%{_libdir}/libdw.a
#%{_libdir}/libasm.a

%files libelf
%defattr(-,root,root)
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf.so.*

%files libelf-devel
%defattr(-,root,root)
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%{_includedir}/elfutils/version.h
%{_libdir}/libelf.so

%files libelf-devel-static
%{_libdir}/libelf.a

%files libelf-lang -f %{name}.lang
%defattr(-,root,root)

%changelog
* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.189-1
- Auto-upgrade to 0.189 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.186-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Feb 16 2022 Muhammad Falak <mwani@microsoft.com> - 0.186-1
- Bump version to 0.186
- Skip a test which can fail 'run-reverse-sections-self'

* Fri Oct 22 2021 Andrew Phelps <anphel@microsoft.com> - 0.185-1
- Update to version 0.185

* Tue Aug 31 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.176-5
- Adding "*-default-yama-scope" subpackage using Fedora 32 (license: MIT) specs as guidance.
- Providing subpackage '*-libs' from the default package.

* Tue Dec 22 2020 Andrew Phelps <anphel@microsoft.com> - 0.176-4
- Skip 2 tests that are expected to fail. License verified. Removed %%define sha1

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.176-3
- Added %%license line automatically

* Thu Feb 06 2020 Andrew Phelps <anphel@microsoft.com> - 0.176-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Jun 10 2019 Sujay G <gsujay@vmware.com> - 0.176-1
- Updated to version 0.176 to fix CVE-2019-{7148, 7149, 7150}'s
- Removed cve-2014-0172.patch, CVE-2018-18310.patch, CVE-2018-18520.patch,
  CVE-2018-18521.patch patch files.

* Mon May 20 2019 Sujay G <gsujay@vmware.com> - 0.174-3
- Fix for CVE-2018-18520 & CVE-2018-18521

* Thu Jan 24 2019 Keerthana K <keerthanak@vmware.com> - 0.174-2
- Fix for CVE-2018-18310

* Mon Oct 01 2018 Alexey Makhalov <amakhalov@vmware.com> - 0.174-1
- Version update

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> - 0.169-2
- Requires bzip2-libs

* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> - 0.169-1
- Updated to 0.169

* Mon Apr 03 2017 Chang Lee <changlee@vmware.com> - 0.168-1
- Updated to 0.168

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> - 0.165-3
- Added -libelf-lang subpackage

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 0.165-2
- GA - Bump release of all rpms

* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> - 0.165-1
- Updated to version 0.165

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 0.158-4
- Handled locale files with macro find_lang

* Sat Aug 15 2015 Sharath George <sharathg@vmware.com> - 0.158-3
- Add in patch for CVE-2014-0172

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> - 0.158-2
- Update according to UsrMove.

* Fri Jan  3 2014 Mark Wielaard <mjw@redhat.com> - 0.158-1
- libdwfl: dwfl_core_file_report has new parameter executable.
  New functions dwfl_module_getsymtab_first_global,
  dwfl_module_getsym_info and dwfl_module_addrinfo.
  Added unwinder with type Dwfl_Thread_Callbacks, opaque types
  Dwfl_Thread and Dwfl_Frame and functions dwfl_attach_state,
  dwfl_pid, dwfl_thread_dwfl, dwfl_thread_tid, dwfl_frame_thread,
  dwfl_thread_state_registers, dwfl_thread_state_register_pc,
  dwfl_getthread_frames, dwfl_getthreads, dwfl_thread_getframes
  and dwfl_frame_pc.
- addr2line: New option -x to show the section an address was found in.
- stack: New utility that uses the new unwinder for processes and cores.
- backends: Unwinder support for i386, x86_64, s390, s390x, ppc and ppc64.
  aarch64 support.

* Mon Sep 30 2013 Mark Wielaard <mjw@redhat.com> - 0.157-1
- libdw: Add new functions dwarf_getlocations, dwarf_getlocation_attr
         and dwarf_getlocation_die.
- readelf: Show contents of NT_SIGINFO and NT_FILE core notes.
- addr2line: Support -i, --inlines output option.
- backends: abi_cfi hook for arm, ppc and s390.

* Thu Jul 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> - 0.156-1
- lib: New macro COMPAT_VERSION_NEWPROTO.
- libdw: Handle GNU extension opcodes in dwarf_getlocation.
- libdwfl: Fix STB_GLOBAL over STB_WEAK preference in
  dwfl_module_addrsym.          Add minisymtab support.          Add
  parameter add_p_vaddr to dwfl_report_elf.          Use DT_DEBUG
  library search first.
- libebl: Handle new core note types in EBL.
- backends: Interpret NT_ARM_VFP.           Implement core file
  registers parsing for s390/s390x.
- readelf: Add --elf-section input option to inspect an embedded ELF
  file.          Add -U, --unresolved-address-offsets output control.
         Add --debug-dump=decodedline support.          Accept version
  8 .gdb_index section format.          Adjust output formatting width.
           When highpc is in constant form print it also as address.
        Display raw .debug_aranges. Use libdw only for decodedaranges.
- elflint: Add __bss_start__ to the list of allowed symbols.
- tests: Add configure --enable-valgrind option to run all tests
  under valgrind.        Enable automake parallel-tests for make check.
- translations: Updated Polish translation.
- Updates for Automake 1.13.

* Fri Aug 24 2012 Mark Wielaard <mjw@redhat.com> - 0.155-1
- libelf: elf*_xlatetomd now works for cross-endian ELF note data.
       elf_getshdr now works consistently on non-mmaped ELF files after
          calling elf_cntl(ELF_C_FDREAD).         Implement support for
  ar archives with 64-bit symbol table.
- libdw: dwarf.h corrected the DW_LANG_ObjC constant name (was
  DW_LANG_Objc).        Any existing sources using the old name will
  have to be updated.        Add DW_MACRO_GNU .debug_macro type
  encodings constants, DW_ATE_UTF        and DW_OP_GNU_parameter_ref to
  dwarf.h.        Experimental support for DWZ multifile forms
  DW_FORM_GNU_ref_alt        and DW_FORM_GNU_strp_alt.  Disabled by
  default.  Use configure        --enable-dwz to test it.
- readelf: Add .debug_macro parsing support.          Add .gdb_index
  version 7 parsing support.          Recognize DW_OP_GNU_parameter_ref.
- backends: Add support for Tilera TILE-Gx processor.
- translations: Updated Ukrainian translation.

* Fri Jun 22 2012 Mark Wielaard <mjw@redhat.com> - 0.154-1
- libelf: [g]elf[32|64]_offscn() do not match SHT_NOBITS sections at
  OFFSET.
- libdw: dwarf_highpc function now handles DWARF 4 DW_AT_high_pc
  constant form.        Fix bug using dwarf_next_unit to iterate over
  .debug_types.
- elflint: Now accepts gold linker produced executables.
- The license is now GPLv2/LGPLv3+ for the libraries and GPLv3+ for
  stand-alone programs. There is now also a formal CONTRIBUTING
  document describing how to submit patches.

* Thu Feb 23 2012 Mark Wielaard <mjw@redhat.com> - 0.153-1
- libdw: Support reading .zdebug_* DWARF sections compressed via zlib.
- libdwfl: Speed up dwfl_module_addrsym.
- nm: Support C++ demangling.
- ar: Support D modifier for "deterministic output" with no
  uid/gid/mtime info.     The U modifier is the inverse.     elfutils
  can be configured with the --enable-deterministic-archives     option
  to make the D behavior the default when U is not specified.
- ranlib: Support -D and -U flags with same meaning.
- readelf: Improve output of -wline. Add support for printing SDT elf
  notes.          Add printing of .gdb_index section. 	 Support for
  typed DWARF stack, call_site and entry_value.
- strip: Add --reloc-debug-sections option.        Improved SHT_GROUP
  sections handling.

* Tue Feb 15 2011  <drepper@gmail.com> - 0.152-1
- Various build and warning nits fixed for newest GCC and Autoconf.
- libdwfl: Yet another prelink-related fix for another regression.
  	 Look for Linux kernel images in files named with compression
  suffixes.
- elfcmp: New flag --ignore-build-id to ignore differing build ID
  bits. 	New flag -l/--verbose to print all differences.

* Wed Jan 12 2011  <drepper@gmail.com> - 0.151-1
- libdwfl: Fix for more prelink cases with separate debug file.
- strip: New flag --strip-sections to remove section headers entirely.

* Mon Nov 22 2010  <drepper@gmail.com> - 0.150-1
- libdw: Fix for handling huge .debug_aranges section.
- libdwfl: Fix for handling prelinked DSO with separate debug file.
- findtextrel: Fix diagnostics to work with usual section ordering.
- libebl: i386 backend fix for multi-register integer return value
  location.

* Mon Sep 13 2010  <drepper@redhat.com> - 0.149-1
- libdw: Decode new DW_OP_GNU_implicit_pointer operation;        new
  function dwarf_getlocation_implicit_pointer.
- libdwfl: New function dwfl_dwarf_line.
- addr2line: New flag -F/--flags to print more DWARF line information
  details.
- strip: -g recognizes .gdb_index as a debugging section.

* Mon Jun 28 2010  <drepper@redhat.com> - 0.148-1
- libdw: Accept DWARF 4 format: new functions dwarf_next_unit,
  dwarf_offdie_types.        New functions dwarf_lineisa,
  dwarf_linediscriminator, dwarf_lineop_index.
- libdwfl: Fixes in core-file handling, support cores from PIEs.
  	 When working from build IDs, don't open a named file that
  mismatches.
- readelf: Handle DWARF 4 formats.

* Mon May  3 2010 Ulrich Drepper <drepper@redhat.com> - 0.147-1
- libdw: Fixes in CFI handling, best possible handling of bogus CFA
  ops.
- libdwfl: Ignore R_*_NONE relocs, works around old (binutils) ld -r
  bugs.

* Wed Apr 21 2010  <drepper@redhat.com> - 0.146-1
- libdwfl: New function dwfl_core_file_report.

* Tue Feb 23 2010 Ulrich Drepper <drepper@redhat.com> - 0.145-1
- Fix build with --disable-dependency-tracking.
- Fix build with most recent glibc headers.
- libelf: More robust to bogus section headers.
- libdw: Fix CFI decoding.
- libdwfl: Fix address bias returned by CFI accessors. 	 Fix core
  file module layout identification.
- readelf: Fix CFI decoding.

* Thu Jan 14 2010  <drepper@redhat.com> - 0.144-1
- libelf: New function elf_getphdrnum. 	Now support using more than
  65536 program headers in a file.
- libdw: New function dwarf_aggregate_size for computing (constant)
  type        sizes, including array_type cases with nontrivial
  calculation.
- readelf: Don't give errors for missing info under -a.
  Handle Linux "VMCOREINFO" notes under -n.

* Mon Sep 21 2009  <drepper@redhat.com> - 0.143-1
- libdw: Various convenience functions for individual attributes now
  use dwarf_attr_integrate to look up indirect inherited
  attributes.  Location expression handling now supports
  DW_OP_implicit_value.
- libdwfl: Support automatic decompression of files in XZ format,
  and of Linux kernel images made with bzip2 or LZMA (as well
  as gzip).

* Mon Jun 29 2009  <drepper@redhat.com> - 0.142-1
- libelf: Add elf_getshdrnum alias for elf_getshnum and elf_getshdrstrndx alias
  for elf_getshstrndx and deprecate original names.  Sun screwed up
  their implementation and asked for a solution.
- libebl: Add support for STB_GNU_UNIQUE.
- elflint: Add support for STB_GNU_UNIQUE.
- readelf: Add -N option, speeds up DWARF printing without address->name lookups.
- libdw: Add support for decoding DWARF CFI into location description form.
  Handle some new DWARF 3 expression operations previously omitted.
  Basic handling of some new encodings slated for DWARF

* Thu Apr 23 2009 Ulrich Drepper <drepper@redhat.com> - 0.141-1
- libebl: sparc backend fixes; 	some more arm backend support
- libdwfl: fix dwfl_module_build_id for prelinked DSO case;
  fixes in core file support; 	 dwfl_module_getsym interface
  improved for non-address symbols
- strip: fix infinite loop on strange inputs with -f
- addr2line: take -j/--section=NAME option for binutils compatibility
  	   (same effect as '(NAME)0x123' syntax already supported)

* Mon Feb 16 2009 Ulrich Drepper <drepper@redhat.com> - 0.140-1
- libelf: Fix regression in creation of section header
- libdwfl: Less strict behavior if DWARF reader ist just used to
  display data

* Thu Jan 22 2009 Ulrich Drepper <drepper@redhat.com> - 0.139-1
- libcpu: Add Intel SSE4 disassembler support
- readelf: Implement call frame information and exception handling
  dumping.          Add -e option.  Enable it implicitly for -a.
- elflint: Check PT_GNU_EH_FRAME program header entry.
- libdwfl: Support automatic gzip/bzip2 decompression of ELF files.

* Wed Dec 31 2008 Roland McGrath <roland@redhat.com> - 0.138-1
- Install <elfutils/version.h> header file for applications to use in
  source version compatibility checks.
- libebl: backend fixes for i386 TLS relocs; backend support for
  NT_386_IOPERM
- libcpu: disassembler fixes
- libdwfl: bug fixes
- libelf: bug fixes
- nm: bug fixes for handling corrupt input files

* Tue Aug 26 2008 Ulrich Drepper <drepper@redhat.com> - 0.137-1
- Minor fixes for unreleased 0.136 release.

* Mon Aug 25 2008 Ulrich Drepper <drepper@redhat.com> - 0.136-1
- libdwfl: bug fixes; new segment interfaces;	 all the libdwfl-based
 tools now support --core=COREFILE option

* Mon May 12 2008 Ulrich Drepper <drepper@redhat.com> - 0.135-1
- libdwfl: bug fixes
- strip: changed handling of ET_REL files wrt symbol tables and relocs

* Tue Apr  8 2008 Ulrich Drepper <drepper@redhat.com> - 0.134-1
- elflint: backend improvements for sparc, alpha
- libdwfl, libelf: bug fixes

* Sat Mar  1 2008 Ulrich Drepper <drepper@redhat.com> - 0.133-1
- readelf, elflint, libebl: SHT_GNU_ATTRIBUTE section handling (readelf -A)
- readelf: core note handling for NT_386_TLS, NT_PPC_SPE, Alpha NT_AUXV
- libdwfl: bug fixes and optimization in relocation handling
- elfcmp: bug fix for non-allocated section handling
- ld: implement newer features of binutils linker.

* Mon Jan 21 2008 Ulrich Drepper <drepper@redhat.com> - 0.132-1
- libcpu: Implement x86 and x86-64 disassembler.
- libasm: Add interface for disassembler.
- all programs: add debugging of branch prediction.
- libelf: new function elf_scnshndx.

* Sun Nov 11 2007 Ulrich Drepper <drepper@redhat.com> - 0.131-1
- libdw: DW_FORM_ref_addr support; dwarf_formref entry point now depreca
ted;       bug fixes for oddly-formatted DWARF
- libdwfl: bug fixes in offline archive support, symbol table handling;
	 apply partial relocations for dwfl_module_address_section on
ET_REL
- libebl: powerpc backend support for Altivec registers

* Mon Oct 15 2007 Ulrich Drepper <drepper@redhat.com> - 0.130-1
- readelf: -p option can take an argument like -x for one section,
	 or no argument (as before) for all SHF_STRINGS sections;
	 new option --archive-index (or -c);	 improved -n output fo
r core files, on many machines
- libelf: new function elf_getdata_rawchunk, replaces gelf_rawchunk;
	new functions gelf_getnote, gelf_getauxv, gelf_update_auxv
- readelf, elflint: handle SHT_NOTE sections without requiring phdrs
- elflint: stricter checks on debug sections
- libdwfl: new functions dwfl_build_id_find_elf, dwfl_build_id_find_debu
ginfo,	 dwfl_module_build_id, dwfl_module_report_build_id;	 suppo
rt dynamic symbol tables found via phdrs;	 dwfl_standard_find_de
buginfo now uses build IDs when available
- unstrip: new option --list (or -n)
- libebl: backend improvements for sparc, alpha, powerpc

* Tue Aug 14 2007 Ulrich Drepper <drepper@redhat.com> - 0.129-1
- readelf: new options --hex-dump (or -x), --strings (or -p)
- addr2line: new option --symbols (or -S)

* Wed Apr 18 2007 Ulrich Drepper <drepper@redhat.com> - 0.127-1
- libdw: new function dwarf_getsrcdirs
- libdwfl: new functions dwfl_module_addrsym, dwfl_report_begin_add,
	 dwfl_module_address_section

* Mon Feb  5 2007 Ulrich Drepper <drepper@redhat.com> - 0.126-1
- new program: ar

* Mon Dec 18 2006 Ulrich Drepper <drepper@redhat.com> - 0.125-1
- elflint: Compare DT_GNU_HASH tests.
- move archives into -static RPMs
- libelf, elflint: better support for core file handling

* Tue Oct 10 2006 Ulrich Drepper <drepper@redhat.com> - 0.124-1
- libebl: sparc backend support for return value location
- libebl, libdwfl: backend register name support extended with more info
- libelf, libdw: bug fixes for unaligned accesses on machines that care
- readelf, elflint: trivial bugs fixed

* Mon Aug 14 2006 Roland McGrath <roland@redhat.com> - 0.123-1
- libebl: Backend build fixes, thanks to Stepan Kasal.
- libebl: ia64 backend support for register names, return value location
- libdwfl: Handle truncated linux kernel module section names.
- libdwfl: Look for linux kernel vmlinux files with .debug suffix.
- elflint: Fix checks to permit --hash-style=gnu format.

* Wed Jul 12 2006 Ulrich Drepper <drepper@redhat.com> - 0.122-1
- libebl: add function to test for relative relocation
- elflint: fix and extend DT_RELCOUNT/DT_RELACOUNT checks
- elflint, readelf: add support for DT_GNU_HASHlibelf: add elf_gnu_hash
- elflint, readelf: add support for 64-bit SysV-style hash tables
- libdwfl: new functions dwfl_module_getsymtab, dwfl_module_getsym.

* Wed Jun 14 2006  <drepper@redhat.com> - 0.121-1
- libelf: bug fixes for rewriting existing files when using mmap.
- make all installed headers usable in C++ code.
- readelf: better output format.
- elflint: fix tests of dynamic section content.
- ld: Implement --as-needed, --execstack, PT_GNU_STACK.  Many small patc
hes.
- libdw, libdwfl: handle files without aranges info.

* Tue Apr  4 2006 Ulrich Drepper <drepper@redhat.com> - 0.120-1
- Bug fixes.
- dwarf.h updated for DWARF 3.0 final specification.
- libdwfl: New function dwfl_version.
- The license is now GPL for most files.  The libelf, libebl, libdw,and
libdwfl libraries have additional exceptions.  Add reference toOIN.

* Thu Jan 12 2006 Roland McGrath <roland@redhat.com> - 0.119-1
- elflint: more tests.
- libdwfl: New function dwfl_module_register_names.
- libebl: New backend hook for register names.

* Tue Dec  6 2005 Ulrich Drepper <drepper@redhat.com> - 0.118-1
- elflint: more tests.
- libdwfl: New function dwfl_module_register_names.
- libebl: New backend hook for register names.

* Thu Nov 17 2005 Ulrich Drepper <drepper@redhat.com> - 0.117-1
- libdwfl: New function dwfl_module_return_value_location.
- libebl: Backend improvements for several CPUs.

* Mon Oct 31 2005 Ulrich Drepper <drepper@redhat.com> - 0.116-1
- libdw: New functions dwarf_ranges, dwarf_entrypc, dwarf_diecu,       d
warf_entry_breakpoints.  Removed Dwarf_Func type and functions       d
warf_func_name, dwarf_func_lowpc, dwarf_func_highpc,       dwarf_func_
entrypc, dwarf_func_die; dwarf_getfuncs callback now uses       Dwarf_
Die, and dwarf_func_file, dwarf_func_line, dwarf_func_col       replac
ed by dwarf_decl_file, dwarf_decl_line, dwarf_decl_column;       dwarf
_func_inline, dwarf_func_inline_instances now take Dwarf_Die.       Ty
pe Dwarf_Loc renamed to Dwarf_Op; dwarf_getloclist,       dwarf_addrlo
clists renamed dwarf_getlocation, dwarf_getlocation_addr.

* Fri Sep  2 2005 Ulrich Drepper <drepper@redhat.com> - 0.115-1
- libelf: speed-ups of non-mmap reading.
- strings: New program.
- Implement --enable-gcov option for configure.
- libdw: New function dwarf_getscopes_die.

* Wed Aug 24 2005 Ulrich Drepper <drepper@redhat.com> - 0.114-1
- libelf: new function elf_getaroff
- libdw: Added dwarf_func_die, dwarf_func_inline, dwarf_func_inline_inst
ances.
- libdwfl: New functions dwfl_report_offline, dwfl_offline_section_addre
ss,	 dwfl_linux_kernel_report_offline.
- ranlib: new program

* Mon Aug 15 2005 Ulrich Drepper <drepper@redhat.com> - 0.114-1
- libelf: new function elf_getaroff
- ranlib: new program

* Wed Aug 10 2005 Ulrich Drepper <@redhat.com> - 0.113-1
- elflint: relax a bit. Allow version definitions for defined symbols ag
ainstDSO versions also for symbols in nobits sections.  Allow .rodata
sectionto have STRINGS and MERGE flag set.
- strip: add some more compatibility with binutils.

* Sat Aug  6 2005 Ulrich Drepper <@redhat.com> - 0.113-1
- elflint: relax a bit. Allow version definitions for defined symbols ag
ainstDSO versions also for symbols in nobits sections.  Allow .rodata
sectionto have STRINGS and MERGE flag set.

* Sat Aug  6 2005 Ulrich Drepper <@redhat.com> - 0.113-1
- elflint: relax a bit. Allow version definitions for defined symbols ag
ainstDSO versions also for symbols in nobits sections.

* Fri Aug  5 2005 Ulrich Drepper <@redhat.com> - 0.112-1
- elfcmp: some more relaxation.
- elflint: many more tests, especially regarding to symbol versioning.
- libelf: Add elfXX_offscn and gelf_offscn.
- libasm: asm_begin interface changes.
- libebl: Add three new interfaces to directly access machine, class, an
ddata encoding information.
- objdump: New program.  Just the beginning.

* Thu Jul 28 2005 Ulrich Drepper <@redhat.com> - 0.111-1
- libdw: now contains all of libdwfl.  The latter is not installed anymore.
- elfcmp: little usability tweak, name and index of differing section is
 printed.

* Sun Jul 24 2005 Ulrich Drepper <@redhat.com> - 0.110-1
- libelf: fix a numbe rof problems with elf_update
- elfcmp: fix a few bugs.  Compare gaps.
- Fix a few PLT problems and mudflap build issues.
- libebl: Don't expose Ebl structure definition in libebl.h.  It's now p
rivate.

* Thu Jul 21 2005 Ulrich Drepper <@redhat.com> - 0.109-1
- libebl: Check for matching modules.
- elflint: Check that copy relocations only happen for OBJECT or NOTYPE
symbols.
- elfcmp: New program.
- libdwfl: New library.

* Mon May  9 2005 Ulrich Drepper <@redhat.com> - 0.108-1
- strip: fix bug introduced in last change
- libdw: records returned by dwarf_getsrclines are now sorted by address

* Sun May  8 2005 Ulrich Drepper <@redhat.com> - 0.108-1
- strip: fix bug introduced in last change

* Sun May  8 2005 Ulrich Drepper <@redhat.com> - 0.107-1
- readelf: improve DWARF output format
- strip: support Linux kernel modules

* Fri Apr 29 2005 Ulrich Drepper <drepper@redhat.com> - 0.107-1
- readelf: improve DWARF output format

* Mon Apr  4 2005 Ulrich Drepper <drepper@redhat.com> - 0.106-1
- libdw: Updated dwarf.h from DWARF3 speclibdw: add new funtions dwarf_f
unc_entrypc, dwarf_func_file, dwarf_func_line,dwarf_func_col, dwarf_ge
tsrc_file

* Fri Apr  1 2005 Ulrich Drepper <drepper@redhat.com> - 0.105-1
- addr2line: New program
- libdw: add new functions: dwarf_addrdie, dwarf_macro_*, dwarf_getfuncs
,dwarf_func_*.
- findtextrel: use dwarf_addrdie

* Mon Mar 28 2005 Ulrich Drepper <drepper@redhat.com> - 0.104-1
- findtextrel: New program.

* Mon Mar 21 2005 Ulrich Drepper <drepper@redhat.com> - 0.103-1
- libdw: Fix using libdw.h with gcc < 4 and C++ code.  Compiler bug.

* Tue Feb 22 2005 Ulrich Drepper <drepper@redhat.com> - 0.102-1
- More Makefile and spec file cleanups.

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> - 0.94-1
- upgrade to 0.94

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> - 0.93-1
- upgrade to 0.93

* Thu Jan  8 2004 Jakub Jelinek <jakub@redhat.com> - 0.92-1
- full version
- macroized spec file for GPL or OSL builds
- include only libelf under GPL plus wrapper scripts

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> - 0.91-2
- macroized spec file for GPL or OSL builds

* Wed Jan  7 2004 Ulrich Drepper <drepper@redhat.com>
- split elfutils-devel into two packages.

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> - 0.91-1
- include only libelf under GPL plus wrapper scripts

* Tue Dec 23 2003 Jeff Johnson <jbj@redhat.com> - 0.89-3
- readelf, not readline, in %%description (#111214).

* Fri Sep 26 2003 Bill Nottingham <notting@redhat.com> - 0.89-1
- update to 0.89 (fix eu-strip)

* Tue Sep 23 2003 Jakub Jelinek <jakub@redhat.com> - 0.86-3
- update to 0.86 (fix eu-strip on s390x/alpha)
- libebl is an archive now; remove references to DSO

* Mon Jul 14 2003 Jeff Johnson <jbj@redhat.com> - 0.84-3
- upgrade to 0.84 (readelf/elflint improvements, rawhide bugs fixed).

* Fri Jul 11 2003 Jeff Johnson <jbj@redhat.com> - 0.83-3
- upgrade to 0.83 (fix invalid ELf handle on *.so strip, more).

* Wed Jul  9 2003 Jeff Johnson <jbj@redhat.com> - 0.82-3
- upgrade to 0.82 (strip tests fixed on big-endian).

* Tue Jul  8 2003 Jeff Johnson <jbj@redhat.com> - 0.81-3
- upgrade to 0.81 (strip excludes unused symtable entries, test borked).

* Thu Jun 26 2003 Jeff Johnson <jbj@redhat.com> - 0.80-3
- upgrade to 0.80 (debugedit changes for kernel in progress).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Jeff Johnson <jbj@redhat.com> - 0.79-2
- upgrade to 0.79 (correct formats for size_t, more of libdw "works").

* Mon May 19 2003 Jeff Johnson <jbj@redhat.com> - 0.78-2
- upgrade to 0.78 (libdwarf bugfix, libdw additions).

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Thu Feb 20 2003 Jeff Johnson <jbj@redhat.com> - 0.76-2
- use the correct way of identifying the section via the sh_info link.

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> - 0.75-2
- update to 0.75 (eu-strip -g fix)

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> - 0.74-2
- update to 0.74 (fix for writing with some non-dirty sections)

* Thu Feb  6 2003 Jeff Johnson <jbj@redhat.com> - 0.73-3
- another -0.73 update (with sparc fixes).
- do "make check" in %%check, not %%install, section.

* Mon Jan 27 2003 Jeff Johnson <jbj@redhat.com> - 0.73-2
- update to 0.73 (with s390 fixes).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Jakub Jelinek <jakub@redhat.com> - 0.72-4
- fix arguments to gelf_getsymshndx and elf_getshstrndx
- fix other warnings
- reenable checks on s390x

* Sat Jan 11 2003 Karsten Hopp <karsten@redhat.de> - 0.72-3
- temporarily disable checks on s390x, until someone has
  time to look at it

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> - 0.72-2
- update to 0.72

* Wed Dec 11 2002 Jakub Jelinek <jakub@redhat.com> - 0.71-2
- update to 0.71

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> - 0.69-4
- update to 0.69.
- add "make check" and segfault avoidance patch.
- elfutils-libelf needs to run ldconfig.

* Tue Dec 10 2002 Jeff Johnson <jbj@redhat.com> - 0.68-2
- update to 0.68.

* Fri Dec  6 2002 Jeff Johnson <jbj@redhat.com> - 0.67-2
- update to 0.67.

* Tue Dec  3 2002 Jeff Johnson <jbj@redhat.com> - 0.65-2
- update to 0.65.

* Mon Dec  2 2002 Jeff Johnson <jbj@redhat.com> - 0.64-2
- update to 0.64.

* Sun Dec 1 2002 Ulrich Drepper <drepper@redhat.com> - 0.64
- split packages further into elfutils-libelf

* Sat Nov 30 2002 Jeff Johnson <jbj@redhat.com> - 0.63-2
- update to 0.63.

* Fri Nov 29 2002 Ulrich Drepper <drepper@redhat.com> - 0.62
- Adjust for dropping libtool

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> - 0.59-2
- update to 0.59

* Thu Nov 14 2002 Jeff Johnson <jbj@redhat.com> - 0.56-2
- update to 0.56

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> - 0.54-2
- update to 0.54

* Sun Oct 27 2002 Jeff Johnson <jbj@redhat.com> - 0.53-2
- update to 0.53
- drop x86_64 hack, ICE fixed in gcc-3.2-11.

* Sat Oct 26 2002 Jeff Johnson <jbj@redhat.com> - 0.52-3
- get beehive to punch a rhpkg generated package.

* Wed Oct 23 2002 Jeff Johnson <jbj@redhat.com> - 0.52-2
- build in 8.0.1.
- x86_64: avoid gcc-3.2 ICE on x86_64 for now.

* Tue Oct 22 2002 Ulrich Drepper <drepper@redhat.com> - 0.52
- Add libelf-devel to conflicts for elfutils-devel

* Mon Oct 21 2002 Ulrich Drepper <drepper@redhat.com> - 0.50
- Split into runtime and devel package

* Fri Oct 18 2002 Ulrich Drepper <drepper@redhat.com> - 0.49
- integrate into official sources

* Wed Oct 16 2002 Jeff Johnson <jbj@redhat.com> - 0.46-1
- Swaddle.
