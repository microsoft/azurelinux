# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define libname libdwarves
%define libver 1

Name: dwarves
Version: 1.32
Release: 5%{?dist}
License: GPL-2.0-only
Summary: Debugging Information Manipulation Tools (pahole & friends)
URL: http://acmel.wordpress.com
Source: http://fedorapeople.org/~acme/dwarves/%{name}-%{version}.tar.xz
Source: http://fedorapeople.org/~acme/dwarves/%{name}-%{version}.tar.sign
Requires: %{libname}%{libver} = %{version}-%{release}
BuildRequires: gcc
BuildRequires: cmake >= 2.8.12
BuildRequires: zlib-devel
BuildRequires: elfutils-devel >= 0.130

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
Summary: Debugging information  processing library

%description -n %{libname}%{libver}
Debugging information processing library.

%package -n %{libname}%{libver}-devel
Summary: Debugging information library development files
Requires: %{libname}%{libver} = %{version}-%{release}

%description -n %{libname}%{libver}-devel
Debugging information processing library development files.

%prep
%setup -q

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
%doc changes-v1.32
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
%{_mandir}/man1/pfunct.1*
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
* Sat Sep 12 2026 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.32-1
- Regression tests: from 6 in v1.31 to 74
- New coverage work, 16 csets
- Add pfunct split BTF test to btf_split
- Verify the downloaded perf tarball checksum before extracting
- Use a portable high-resolution timestamp
- Build the test_bin fixture in the per-test tmpdir
- Use POSIX [ instead of [[ in test_lib.sh
- btf_type_tag_order.sh: Use gawk for capture-group match()
- Fix coverage build by respecting build-coverage/ in PATH
- Add automatic perf building for cross-distro compatibility
- Check minimum perf metadata records instead of exact counts
- Fix perf tests for container environments
- Force DWARF 5 in atomic_types test for _Atomic support
- Skip tests gracefully on old bpftool versions
- Skip instead of fail when old toolchains lack feature support
- Fix gcc_true_signatures.sh compiler detection and awk syntax
- Add prototype expression parsing and prettify test
- Add codiff_multi_cu.sh to cover __cus__find_cu_by_name
- Add BTF vmlinux encoding test
- Add typedef chain display test
- Add _Atomic type compile emission test
- Add pahole scattered option paths coverage test
- Add pahole --header_type, --range and --seek_bytes prettify test
- Add codiff member type change and function prototype diff test
- Add dwarf_loader.c bitfield recode and inlining edge case test
- Add dwarves.c core API coverage test
- Add prefcnt type reference counting coverage test
- Add elf_symtab, gobuffer, dutil and pglobal coverage test
- Add dwarves_emit and dwarves_reorganize coverage test
- Add bitfield, cross-boundary and mixed member type test
- Add BTF encoder coverage test for vars, floats and multi-CU
- Add codiff terse, verbose and multi-CU diff test
- Add pfunct CLI option coverage
- Add pglobal variable and function listing test
- Add multi-file loading test
- Add 5 btf_encoder.c targeted coverage tests
- Add medium-effort coverage tests for 5 uncovered code paths
- Add CLI display, BTF encoding options and auxiliary tools tests
- Add enumerator search test, in 2 csets
- Add type containment and pointer search test, in 2 csets
- Add coverage-diff.sh workflow and coverage_table.py reporter
- Add LLVM source-based code coverage support
- Add split BTF encoding test (vmlinux base + kernel module)
- Add BTF_KIND_FWD encoding and loading round-trip test
- Add BTF bitfield encoding/loading round-trip test
- Add BTF FLOAT and ENUM64 type encoding tests
- Add BTF VAR and DATASEC encoding test
- Add expand_pointers, pfunct_stats and class_list_file tests
- Add BTF arena type tag encoding test
- Add pdwtags DWARF tag display test
- Add codiff struct comparison test
- Add bitfield layout and data member filtering test
- Add sort output and separator test
- Add display format options test
- Add class name filtering test
- Add compilable output and type filtering test
- Add type expansion and anonymous struct test
- Add sizes and holes display test
- Fix mktemp suffix portability for Alpine Linux
- Add emit_atomic.sh test and fix pfunct-btf-decl-tags.sh quoting
- Reduce reproducible_build thread count iterations
- Add --dump-artifacts to capture DWARF/BTF from binaries
- Add --jobs/-j option to limit parallel test execution
- Show referenced log file contents in verbose mode
- Add --verbose/-v option for better failure diagnosis
- Add PERF_BIN support and preserve build logs on failure
- Add test number filtering and waiting status line
- Add dynamic test timing and reordering to avoid slow tests blocking
  results
- Add --vmlinux option to specify vmlinux file for tests
- Run test scripts in parallel
- Fix test_lib.sh and test scripts to run from any directory
- Guard cleanup() against empty outdir to prevent rm /*
- Add BTF_FUNCTIONS_QUICK mode for fast CI iteration
- Skip and find vmlinux tests when the running kernel vmlinux is not
  available
- Add inter-CU type reference comparison test
- Add GCC default-BTF optimized parameter coverage
- Add BTF true_signature encoding tests
- Add btf_type_tag ordering test
- Support GCC in pfunct-btf-decl-tags test
- add gcc true signature test
- Support DW_FORM_GNU_ref_alt references to dwz alternate debug files
- Add cu parameter to tag__set_spec() and dwarf_tag__set_attr_type()
- Fix cus__merging_cu failing to detect DW_FORM_ref_addr
- Support DW_TAG_imported_unit for same-file partial units
- Allow forcing the merge of CUs for solving inter CU tag references
- Initial support for DW_TAG_subprogram in DW_TAG_enumeration
- Initial support for DW_TAG_variant_part
- Replace stale FIXME/XXX comments with explanations
- Fix data race in tag__init() decl_file string cache
- Skip libdw__lock when elfutils is built thread-safe
- Fix --fixup_silly_bitfields condition check
- Fix annotation failure leaks in variable and typedef creation
- Allocate type_dcu via dwarf_cu__new to fix dangling stack pointer
- Analyze per-parameter information for true signatures
- Collect per-parameter information
- Detect aggregate ABI register usage and signature changes
- Add support for DW_TAG_GNU_annotation
- Extract die__add_btf_type_tag() helper [NFC]
- Detect reordered parameters
- Handle DW_AT_location attrs containing DW_OP_plus_uconst
- Fix multi-dimensional array encoding
- Fall back to objcopy when llvm-objcopy is not available
- Add elf_strptr NULL checks and fix kfunc bounds
- Fix early cleanup crashes in btf_encoder__new/delete
- Use btf_encoder__tag_type() for all type ID computations
- Fix interior pointer free and missing NULL check
- Ensure the first same-name function has a non-zero address
- Add O_TRUNC to btf_encoder__write_raw_file()
- Only skip optimized parms when ABI changed
- Emit true function signatures
- Prefer strong function definitions for BTF generation
- Add true_signature feature support for "."-suffixed functions
- Fix a verbose output issue
- Factor out BPF kfunc emission
- Refactor btf_encoder__add_func_proto
- Remove encoder pointer from btf_encoder_func_state
- Fix -C -T segfault
- Fix option name in the -m/-C error message
- Apply the struct-only filters to unions
- Don't match unions with --with_flexible_array
- Fix --unions --packable segfault
- Guard pipe_seek() against negative offsets
- Use fseek for seekable files in --prettify and --seek_bytes
- Skip inline expansions during BTF encoding
- Fix parse_btf_features("all") being a silent no-op
- Fix --errno typo that decrements instead of negating
- Fix instance memory leak on early returns in
  prototype__stdio_fprintf_value
- Fix BTF function parameter type match check
- Add "layout" BTF encoding feature
- Fix discarded-qualifiers for strchr/strstr.
- Refactor selftests
- Automate the steps needed to release a new version
- Add build-check-series.sh for bisectability verification
- Add tarball targets similar to kernel's perf-tar-src-pkg
- Add git SHA tracking via --devel_version option
- Add test, coverage and list-targets make targets
- Warn loudly when coverage instrumentation is enabled
- Add vmlinux_comparison.py for DWARF/BTF analysis
- Update minimum required version from 3.5 to 3.10
- Remove 11 dead functions found via coverage analysis, in 2 csets
- Add exec_objcopy() shell-injection-safe helper
- Fix variable shadowing in __cus__find_struct_by_name()
- Fix heap buffer overflow in languages__parse realloc
- Don't search for holes before member byte sizes are cached
- Fix missing list head initialization in type__clone_members
- libbpf sync with 1.8
- Fix NULL dereference in remove_dyn()
- Improve language and formatting
- Fix incorrect command line argument in documentation
- describe layout BTF feature
- document true_signature btf_feature
- Update LLVM version to 22
- Add clang+aarch64 to matrix
- build/install bpftool from kernel tree
- Support building kernel with LLVM
- Add man page
- Add support for split BTF
- Mark file-local functions as static
- build-and-test-cmd.sh: Move build-dir detection to test_lib.sh, fix
  container PATH
- build-and-test-cmd.sh: Add CI build+test script
- Fix -Wsign-compare warnings across the codebase
- Fix multi-dimensional array loading
- Handle decl tag component_idx for parameters
- Fix warnings due to type permutation
- Remove leftover comment about --flat_arrays usage
- Remove --flat_arrays now that pahole encodes multi dim arrays in BTF
- Fix error path resource leaks
- Fix error handling when opening file

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri May 16 2025 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.30-1
- New release: 1.30
- Better detection of abort during DWARF loader thread processing
- pahole now detects presence of libbpf APIs and BTF features using weak function
  declarations when built using a shared library libbpf
- Type tags are emitted for BPF arena pointers with new BTF "attributes" feature

* Wed Jan 15 2025 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.29-1
- New release: 1.29
- Multithreading is now in the DWARF loader using a jobs queue and a pool of worker threads.
- The BTF encoding now is always reproducible, and as fast/faster than before.
- The memory consumption is reduced.
- Support for multiple BTF_DECL_TAGs pointing to same tag.
- Verify that pfunct prints btf_decl_tags read from BTF.
- Don't print functions twice when using 'pfunct -f function_name'.

* Fri Dec  6 2024 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.28-1
- New release: 1.28
- Various improvements to reduce the memory footprint of pahole, notably when doing BTF encoding.
- Show flexible arrays statistics
- Add '--padding N' and '--padding_ge N' to show structs with paddings
- Introduce --running_kernel_vmlinux to find a vmlinux that matches the build-id of the running kernel.
- Don't stop pfunct output at the first function that matches a filter, show all of them
- Allow encoding data about all global variables, not just per CPU ones
- Handle .BTF_ids section endianness, fully supporting cross builds
- Generate decl tags for bpf_fastcall for eligible kfuncs
- Add "distilled_base" BTF feature to split BTF generation.
- Use the ELF_C_READ_MMAP mode with libelf, reducing peak memory utilization
- Allow overriding /sys/kernel/btf/vmlinux via the PAHOLE_VMLINUX_BTF_FILENAME env var
- Allow setting the list of compile units via PAHOLE_LANG_EXCLUDE env var
- Serialize access to elfutils dwarf_getlocation().
- Honour --lang_exclude when merging LTO built CUs.
- Add the debuginfod client cache directory to the vmlinux search path.
- Print the CU's language when a tag isn't supported.
- Initial support for GNU_formal_parameter_pack, GNU_template_parameter_pack, template_value_param and template_type_param DWARF tags.
- Improve the parameter parsing by checking DW_OP_[GNU_]entry_value
- Introduce a tests/ directory with regression tests

* Tue Jun 11 2024 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.27-1
- New release: v1.27
- Reproducible parallel builds: multiple runs with different number of loading/encoding threads produce the same result.
- Inject kfunc decl tags into BTF from the BTF IDs ELF section in the Linux kernel vmlinux file.
- Sanitize unsupported DWARF int type with greater-than-16 byte, as BTF doesn't support it.
- Initial support for BTF_KIND_DECL_TAG in the BTF loader, adding support in pfunct output.
- Fix hole discovery with inheritance in C++.

* Tue Feb 27 2024 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.26-1
- New release: v1.26
- When expanding types using 'pahole -E' do it for union and struct typedefs and for enums too.
- Print number of holes, bit holes and bit paddings in class member types.
- Introduce --contains_enumerator=ENUMERATOR_NAME:
- Fix pretty printing using DWARF, waiting for a CU with both class (-C) and a specified "type_enum".
- Add support for DW_TAG_constant in the DWARF loader, first seen in Go DWARF.
- Fix loading DW_TAG_subroutine_type generated by the Go compiler.
- Fix loading of 32-bit signed enums from BTF.
- Add 'pahole --btf_features' to allow consumers to specify an opt-in set of features they want to use in BTF encoding.
- Parallelize loading BTF and DWARF, speeding up a bit btfdiff.
- Do type expansion to cover "private" types and enumerations in btfdiff.

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 11 2023 Viktor Malik <vmalik@redhat.com> - 1.25-3
- Migrate license to SPDX

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Apr  8 2023 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.25-1
- New release: v1.25
- Support for DW_TAG_unspecified_type more generally.
- Make sure struct member offsets are in ascending order. Rust BTF needs this.
- Support C atomic types (DW_TAG_atomic_type).
- Initial support for DW_TAG_LLVM_annotation, used for BTF type tags, for __rcu, __user, etc
- Exclude functions with the same name (static functions in different CUs), inconsistent prototypes or not following calling convention.
- Allow generation of BTF for optimized functions, those that end with a .isra*, .constprop*.
- Support 'pahole --lang=/--lang_exclude=asm'
- Support --compile from DWARF in addition to from BTF.
- Exclude RUST CUs in 'btfdiff', as those are not yet being BTF encoded.

* Fri Feb 17 2023 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.24-3
- Backport the DW_TAG_unspecified_type support while 1.25 gets ready wrt optimized functions support

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 17 2022 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.24-1
- New release: v1.24
- Add support to BTF_KIND_ENUM64.
- Support multithreaded BTF encoding.
- Encode char type as signed in BTF.
- Introduce --lang and --lang_exclude to pahole.
- Introduce --compile to pahole.
- Don't segfault when processing bogus files.

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec  8 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.23-1
- New release: v1.23
- Process DW_TAG_LLVM_annotation tags.
- Initial support for DW_TAG_skeleton_unit.
- Encode BTF_KIND_TYPE_TAG and BTF_KIND_DECL_TAG
- Fix handling of percpu symbols on s390.
- Use cacheline size to infer struct member alignment from BTF.
- Add --skip_missing to not stop when not finding one of -C arguments.
- Fix __attribute__((__aligned__(N)) printing alignment for struct members.
- Fix nested __attribute__(__aligned__(N)) struct printing order.

* Mon Aug 23 2021 Arnaldo Carvalho de Melo <acme@redhat.com> - 1.22-1
- New release: v1.22
- Introduce -j/--jobs option to specify the number of threads to use.
- Multithreaded DWARF loading, requires elfutils >= 0.178.
- Preparatory work for multithreaded BTF encoding, the focus for 1.23.
- Allow encoding BTF to a separate file.
- Show all different types with the same name, not just the first one found.
- Stop assuming that reading from stdin means pretty, add --prettify.
- Improve type resolution for the --header command line option.
- Do not consider the ftrace filter when encoding BTF for kernel functions.
- Lock calls to non-thread safe elfutils' dwarf_decl_file() and dwarf_decl_line().
- Change hash table size to one that performs better with current typical vmlinux files.
- Allow tweaking the hash table size from the command line.
- Add --kabi_prefix to avoid deduplication woes when using _RH_KABI_REPLACE().
- Add --with_flexible_array to show just types with flexible arrays.
- Support btfdiff with a detached BTF file.
- Introduce sorted type output (--sort).
- Disable incomplete CTF encoder.

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
