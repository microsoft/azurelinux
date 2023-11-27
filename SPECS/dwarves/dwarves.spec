%define libname libdwarves
%define libver 1
Summary:        Debugging Information Manipulation Tools (pahole & friends)
Name:           dwarves
Version:        1.25
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://acmel.wordpress.com
Source:         https://fedorapeople.org/~acme/dwarves/%{name}-%{version}.tar.xz
BuildRequires:  cmake >= 2.8.12
BuildRequires:  elfutils-devel >= 0.130
BuildRequires:  gcc
BuildRequires:  zlib-devel
Requires:       %{libname}%{libver} = %{version}-%{release}

%description
dwarves is a set of tools that use the debugging information inserted in
ELF binaries by compilers such as GCC, used by well known debuggers such as
GDB, and more recent ones such as systemtap.

Utilities in the dwarves suite include pahole, that can be used to find
alignment holes in structs and classes in languages such as C, C++, but not
limited to these.

It also extracts other information such as CPU cacheline alignment, helping
pack those structures to achieve more cache hits.

These tools can also be used to encode and read the BTF type information format
used with the Linux kernel bpf syscall, using 'pahole -J' and 'pahole -F btf'.

A diff like tool, codiff can be used to compare the effects changes in source
code generate on the resulting binaries.

Another tool is pfunct, that can be used to find all sorts of information about
functions, inlines, decisions made by the compiler about inlining, etc.

One example of pfunct usage is in the fullcircle tool, a shell that drivers
pfunct to generate compileable code out of a .o file and then build it using
gcc, with the same compiler flags, and then use codiff to make sure the
original .o file and the new one generated from debug info produces the same
debug info.

Pahole also can be used to use all this type information to pretty print raw data
according to command line directions.

Headers can have its data format described from debugging info and offsets from
it can be used to further format a number of records.

The btfdiff utility compares the output of pahole from BTF and DWARF to make
sure they produce the same results.

%package -n %{libname}%{libver}
Summary:        Debugging information  processing library

%description -n %{libname}%{libver}
Debugging information processing library.

%package -n %{libname}%{libver}-devel
Summary:        Debugging information library development files
Requires:       %{libname}%{libver} = %{version}-%{release}

%description -n %{libname}%{libver}-devel
Debugging information processing library development files.

%prep
%autosetup -p1

%build
%cmake -DCMAKE_BUILD_TYPE=Release .
%cmake_build

%install
rm -Rf %{buildroot}
%cmake_install

%ldconfig_scriptlets -n %{libname}%{libver}

%files
%doc README.ctracer
%doc README.btf
%doc changes-v1.21
%doc NEWS
%{_bindir}/btfdiff
%{_bindir}/codiff
%{_bindir}/ctracer
%{_bindir}/dtagnames
%{_bindir}/fullcircle
%{_bindir}/pahole
%{_bindir}/pdwtags
%{_bindir}/pfunct
%{_bindir}/pglobal
%{_bindir}/prefcnt
%{_bindir}/scncopy
%{_bindir}/syscse
%{_bindir}/ostra-cg
%dir %{_datadir}/dwarves/
%dir %{_datadir}/dwarves/runtime/
%dir %{_datadir}/dwarves/runtime/python/
%defattr(0644,root,root,0755)
%{_mandir}/man1/pahole.1*
%{_datadir}/dwarves/runtime/Makefile
%{_datadir}/dwarves/runtime/linux.blacklist.cu
%{_datadir}/dwarves/runtime/ctracer_relay.c
%{_datadir}/dwarves/runtime/ctracer_relay.h
%attr(0755,root,root) %{_datadir}/dwarves/runtime/python/ostra.py*

%files -n %{libname}%{libver}
%{_libdir}/%{libname}.so.*
%{_libdir}/%{libname}_emit.so.*
%{_libdir}/%{libname}_reorganize.so.*

%files -n %{libname}%{libver}-devel
%doc MANIFEST README
%{_includedir}/dwarves/btf_encoder.h
%{_includedir}/dwarves/config.h
%{_includedir}/dwarves/ctf.h
%{_includedir}/dwarves/dutil.h
%{_includedir}/dwarves/dwarves.h
%{_includedir}/dwarves/dwarves_emit.h
%{_includedir}/dwarves/dwarves_reorganize.h
%{_includedir}/dwarves/elfcreator.h
%{_includedir}/dwarves/elf_symtab.h
%{_includedir}/dwarves/gobuffer.h
%{_includedir}/dwarves/hash.h
%{_includedir}/dwarves/libctf.h
%{_includedir}/dwarves/list.h
%{_includedir}/dwarves/rbtree.h
%{_libdir}/%{libname}.so
%{_libdir}/%{libname}_emit.so
%{_libdir}/%{libname}_reorganize.so

%changelog
* Thu Nov 16 2023 Rachel Menge <rachelmenge@microsoft.com> - 1.25-1
- Update to version 1.25
- License verified

* Fri Aug 20 2021 Chris Co <chrco@microsoft.com> - 1.21-4
- Initial CBL-Mariner import from Fedora 35 (license: MIT).

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 10 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.21-2 
- Backport 0001-btf-Remove-ftrace-filter.patch from upstream

* Fri Apr 9 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.21-1
- New release: v1.21
- DWARF loader:
- Handle DWARF5 DW_OP_addrx properly
- Handle subprogram ret type with abstract_origin properly
- Check .notes section for LTO build info
- Check .debug_abbrev for cross-CU references
- Permit merging all DWARF CU's for clang LTO built binary
- Factor out common code to initialize a cu
- Permit a flexible HASHTAGS__BITS
- Use a better hashing function, from libbpf
- btf_encoder:
- Add --btf_gen_all flag
- Match ftrace addresses within ELF functions
- Funnel ELF error reporting through a macro
- Sanitize non-regular int base type
- Add support for the floating-point types
- Pretty printer:
- Honour conf_fprintf.hex when printing enumerations

* Tue Feb 2 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.20-1
- New release: v1.20
- btf_encoder:
- Improve ELF error reporting using elf_errmsg(elf_errno())
- Improve objcopy error handling.
- Fix handling of 'restrict' qualifier, that was being treated as a 'const'.
- Support SHN_XINDEX in st_shndx symbol indexes
- Cope with functions without a name
- Fix BTF variable generation for kernel modules
- Fix address size to match what is in the ELF file being processed.
- Use kernel module ftrace addresses when finding which functions to encode.
- libbpf:
- Allow use of packaged version.
- dwarf_loader:
- Support DW_AT_data_bit_offset
- DW_FORM_implicit_const in attr_numeric() and attr_offset()
- Support DW_TAG_GNU_call_site, standardized rename of DW_TAG_GNU_call_site.
- build:
- Fix compilation on 32-bit architectures.

* Fri Nov 20 2020 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.19-1
- New release: 1.19
- Split BTF
- DWARF workarounds for DW_AT_declaration
- Support cross-compiled ELF binaries with different endianness
- Support showing typedefs for anonymous types
- Speedups using libbpf algorithms
- See changes-v1.19 for a complete and more detailed list of changes

* Fri Oct 02 2020 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.18-1
- New release: 1.18
- Use debugging info to pretty print raw data
- Store percpu variables in vmlinux BTF.
- Fixes to address segfaults on the gdb testsuite binaries
- Bail out on partial units for now, avoiding segfaults and providing warning to user.

* Mon Aug 31 2020 - Zamir SUN <sztsian@gmail.com> - 1.17-4
- Fix FTBFS
- Resolves: bug 1863459

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 13 2020 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.17-1
- New release: 1.17
- Support raw BTF as available in /sys/kernel/btf/vmlinux.
- When the sole argument passed isn't a file, take it as a class name:
- Do not require a class name to operate without a file name.
- Make --find_pointers_to consider unions:
- Make --contains and --find_pointers_to honour --unions
- Add support for finding pointers to void:
- Make --contains and --find_pointers_to to work with base types:
- Make --contains look for more than just unions, structs:
- Consider unions when looking for classes containing some class:
- Introduce --unions to consider just unions:
- Fix -m/--nr_methods - Number of functions operating on a type pointer

* Wed Feb 12 2020 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.16-1
- New release: 1.16
- BTF encoder: Preserve and encode exported functions as BTF_KIND_FUNC.
- BTF loader: Add support for BTF_KIND_FUNC
- Pretty printer: Account inline type __aligned__ member types for spacing
- Pretty printer: Fix alignment of class members that are structs/enums/unions
- Pretty printer: Avoid infinite loop trying to determine type with static data member of its own type.
- RPM spec file:  Add dwarves dependency on libdwarves1.
- pfunct: type->type == 0 is void, fix --compile for that
- pdwtags: Print DW_TAG_subroutine_type as well
- core: Fix ptr_table__add_with_id() handling of pt->nr_entries
- pglobal: Allow passing the format path specifier, to use with BTF
- Tree wide: Fixup issues pointed out by various coverity reports.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul  1 2019 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.15-2
- Fix bug when processing classes without members

* Thu Jun 27 2019 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.15-1
- New release: 1.15
- Fix --expand_types/-E segfault
- Fixup endless printing named structs inside structs in --expand_types
- Avoid NULL deref with num config in __class__fprintf()

* Tue Apr 23 2019 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.13-1
- New release: 1.13
- Infer __packed__ attributes, i.e. __attribute__((__packed__))
- Support DW_AT_alignment, i.e. __attribute__((__aligned__(N)))
- Decode BTF type format and pretty print it
- BTF encoding fixes
- Use libbpf's BTF deduplication
- Support unions as arguments to -C/--class
- New 'pfunct --compile' generates compilable output with type definitions

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 31 2018 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.12-1
- New release: 1.12
- union member cacheline boundaries for all inner structs
- print union member offsets
- Document 'pahole --hex'
- Encode BTF type format for use with eBPF

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 03 2016 Cole Robinson <crobinso@redhat.com> - 1.10-9%{?dist}
- pdwtags: don't fail on unhandled tags (bz 1348200)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 1.10-7
- backport removal of DW_TAG_mutable_type

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 30 2012 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.10-1
- New release

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 20 2010 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.9-1
- New release

* Mon Feb 08 2010 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec  4 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.8-1
- New release

* Fri Feb 13 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.7-2
- Own /usr/share/dwarves, fixes #473645 

* Fri Feb 13 2009 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.7-1
- A CTF decoder based on work done by David S. Miller
- Handle DW_TAG_class_type,
- Add support for showing classes with a prefix
- Add support to DW_TAG_ptr_to_member_type
- Handle typedef definitions in functions
- Print the number of members in a struct/class
- Handle the empty base optimization trick (Zero sized C++ class)
- codiff detect changes in the prototype even when function size doesn't change
- pfunct: Implement --expand_types
- Reduce memory consumption by using a strings table
- Speed up struct search by name
- Several minor bug fixes and infrastructure improvements.
- Initial man page for pahole

* Mon Feb 11 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.6-1
- c83d935a4fd561a3807f520c126c2a61ae1f4d83
- [DWARVES]: Use a hash table for the tags in a CU

* Thu Feb  7 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.5-1
- c4e49add9e48ff08a8ba4187ea43d795af995136
- PAHOLE: Introduce --defined_in
- DWARVES: Another fix for DW_TAG_base_type entries without DW_AT_name
- PAHOLE: Cope with DW_TAG_basic_type entries without DW_AT_name
- CODIFF: Allow passing /dev/null as one of the files to compare
- DWARVES: Allow passing NULL as self to cu__find_
- DWARVES: Fixup usage messages
- DWARVES: Find holes in inner, nameless structs
- DWARVES: Adopt tag__follow_typedef from pahole
- DWARVES: Add some destructors: tag, cu, namespace
- CODIFF: Check if the objects are the same when we have build-id
- DWARVES: Introduce cu__same_build_id
- DWARVES_REORGANIZE: Proper tail padding fixup
- DWARVES: Don't search in empty structs
- DWARVES: Follow const and volatile tags to its ultimate types
- PAHOLE: Add a newline after the --class_dwarf_offset output
- PAHOLE: Expose type__find_first_biggest_size_base_type_member
- DWARVES: Introduce type__find_first_biggest_size_base_type_member
- PAHOLE: Account arrays properly when changing word-size
- PAHOLE: Follow typedefs too when resizing unions
- PAHOLE: Follow typedefs to find if they are resized structs/unions
- PAHOLE: Check if types of struct and union members were already resized
- DWARVES_REORGANIZE: Fixup class__fixup_alingment
- PAHOLE: Allow changing the architecture word-size
- DWARVES_REORGANIZE: Adopt class__add_offsets_from and class__fixup_alignment from ctracer
- DWARVES: build id support requires a recent elfutils package

* Sat Jan  5 2008 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.4-1
- 8e099cf5d1f204e9ea1a9c8c0f1a09a43458d9d3
- codiff fixes

* Sun Dec  9 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.3-2
- c6c71398cd2481e219ea3ef63f32c6479ba4f08f
- SPEC file adjustments to follow http://fedoraproject.org/wiki/Packaging/cmake

* Sat Dec  8 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.3-1
- c4ee21aa122f51f2601893b2118b7f7902d2f410
- Fixed bitfield byte offset handling, now there are no
  more BRAIN FART alerts on a x86_64 linux kernel and on
  an old openbsd kernel image.

* Thu Dec  6 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.2-1
- 07e0974f2c3798acb8e9a2d06f6b2ece7a01c508
- Fix a patological bitfield case

* Thu Dec  6 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.1-1
- 2c01420b51e889196b42a204910b46811ab22f1a
- ctracer now generates systemtap scripts
- Lots of other fixes, see git changelog.

* Tue May  8 2007 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.0-1
- 161c6712f4ae1b7e2ea50df3a0d5c28310905cec
- handle --help, -? --usage on with_executable_option()

* Tue May  8 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- b8eb5eb214f3897ea6faa3272879baa8bf2573c0
- Fix cus__loadfl detection of --executable

* Sun May  6 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- 05351ece16e5203717dd21a6fc1ad2e6ff87c203
- libdwarves_emit

* Tue Apr  3 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- f3c4f527f70053e39b402005107ead6cb10e0b4a
- Fix some --reorganize bugs

* Mon Apr  2 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- 1ec66565a12ce7f197cd40e3901ed6be84935781
- --reorganize improvements
- --packable uses --reorganize code to show structs that can be packed by
  reorganization done with --reorganize.

* Fri Mar 30 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- fd3542317508d04e8178c5d391385d2aa50d6fb7
- Use libdwfl in all tools that handle just one file, codiff and ctracer
  still need work and are still using plain libdw.

* Sun Feb 25 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- 3c148cd84b74b89663febdefab23356952906502
- _snprintf routines changed to _fprintf
- codiff shows diffs in number and total size of inline expansions
- codiff shows diffs in the number of lexblocks
- better alignment in the --expand_types case
- CMake improvements

* Fri Feb  2 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- d37f41df58c375412badf827e24dfc346cea2ff2
- ostra-cg
- relay/debugfs
- mini-structs
- ctracer2ostra
- All this in the Makefile

* Fri Feb  2 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- b7cad1782d683571ffb2601b429ab151bddad5d7
- pglobal, by Davi Arnaut
- pahole --show_reorg_steps
- Reorganize bitfields in pahole --reorganize

* Tue Jan 30 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- 8e236f4ca37b8a3d2057f4ede5a14ab1fa99f73c
- x86-64 lib install fixes

* Tue Jan 30 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- 4a4b75e75a6d7f34215d320cc4a9f669b6ba4075
- pahole --reorganize

* Mon Jan 29 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- 2de67fcaf401ac1e20feca5fa88dfc63fbc4203e
- Type expansion!

* Sat Jan 27 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- 6bf2d2d7707b65e7ca21a13706d8d07824cd6f2f
- ctracer improvements, /usr/lib/ctracer/, etc

* Fri Jan 26 2007 Arnaldo Carvalho de Melo <acme@redhat.com>
- c49f2c963425d5c09c429370e10d9af3d7d7fe32
- Emit typedefs of typedef arrays
- Detect typedef loops
- Fix emission of arrays of structs, unions, etc
- use sysconf for the default cacheline size

* Thu Jan 18 2007 Arnaldo Carvalho de Melo <acme@ghostprotocols.net>
- fab0db03ea9046893ca110bb2b7d71b764f61033
- pdwtags added

* Wed Jan 17 2007 Arnaldo Carvalho de Melo <acme@ghostprotocols.net>
- e3786105c007a39ff3dbfb36a3037e786021e0c6
- First Fedora native build
- struct, enum, enum, void typedefs

* Sat Jan 13 2007 Arnaldo Carvalho de Melo <acme@ghostprotocols.net>
- 9a413e60a3875980d99817722bf019cba3a24573
- pahole --nr_methods, improvements in tag__print, better support for unions

* Fri Jan 12 2007 Arnaldo Carvalho de Melo <acme@ghostprotocols.net>
- a1f5422656a91568a8b4edbcebaae9c1837b5cbd
- Support a DW_TAG_reference_type

* Fri Jan 12 2007 Arnaldo Carvalho de Melo <acme@ghostprotocols.net>
- 0ad467a32187e1929c14054a0fc7326bc4d235c8 
- Added a description

* Thu Jan 11 2007 Arnaldo Carvalho de Melo <acme@ghostprotocols.net>
- new release with type not found asserts replaced by error messages

* Thu Jan 11 2007 Arnaldo Carvalho de Melo <acme@ghostprotocols.net>
- package created
