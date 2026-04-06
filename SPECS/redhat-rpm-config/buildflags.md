This document contains documentation of the individual compiler flags
and how to use them.

[TOC]

# Using RPM build flags

The `%set_build_flags` macro sets the environment variables `CFLAGS`,
`CXXFLAGS`, `FFLAGS`, `FCFLAGS`, `VALAFLAGS`, `LDFLAGS` and `LT_SYS_LIBRARY_PATH` to
the value of their corresponding rpm macros. `%set_build_flags` is automatically
called prior to the `%build`, `%check`, and `%install` phases so these flags can be
used by makefiles and other build tools.

You can opt out of this behavior by doing:

    %undefine _auto_set_build_flags

If you do opt out of this behavior, you can still manually use `%set_build_flags`
by adding it to the `%build` section of your spec file or by using one of the
build system helper macros like `%configure`, `%cmake`, and `%meson`.

For packages which use autoconf to set up the build environment, use
the `%configure` macro to obtain the full complement of flags, like
this:

    %configure

This will invoke `./configure` with arguments (such as
`--prefix=/usr`) to adjust the paths to the packaging defaults. Prior
to that, some common problems in autotools scripts are automatically
patched across the source tree.

Individual build flags are also available through RPM macros:

* `%{build_cc}` for the command name of the C compiler.
* `%{build_cxx}` for the command name of the C++ compiler.
* `%{build_cpp}` for the command name of the C-compatible preprocessor.
* `%{build_cflags}` for the C compiler flags (also known as the
  `CFLAGS` variable).
* `%{build_cxxflags}` for the C++ compiler flags (usually assigned to
  the `CXXFLAGS` shell variable).
* `%{build_fflags}` for `FFLAGS` (the Fortran compiler flags, also
  known as the `FCFLAGS` variable).
* `%{build_valaflags}` for `VALAFLAGS` (the Vala compiler flags)
* `%{build_ldflags}` for the linker (`ld`) flags, usually known as
  `LDFLAGS`. Note that the contents quote linker arguments using
  `-Wl`, so this variable is intended for use with the `gcc` compiler
  driver. At the start of the `%build` section, the environment
  variable `RPM_LD_FLAGS` is set to this value.

The C and C++ compiler flags are historically available as the
`%{optflags}` macro.  These flags may not contain flags that work with
certain languagues or compiler front ends, so the language-specific
`%build_*` are more precise.  At the start of the `%build` section,
the environment variable `RPM_OPT_FLAGS` is set to the `%{optflags}`
value; similar limitations apply.

The variable `LT_SYS_LIBRARY_PATH` is defined here to prevent the `libtool`
script (v2.4.6+) from hardcoding `%_libdir` into the binaries' `RPATH`.

These RPM macros do not alter shell environment variables.

For some other build tools separate mechanisms exist:

* CMake builds use the the `%cmake` macro from the `cmake-rpm-macros`
  package.

Care must be taking not to compile the current selection of compiler
flags into any RPM package besides `redhat-rpm-config`, so that flag
changes are picked up automatically once `redhat-rpm-config` is
updated.

# Flag selection for the build type

The default flags are suitable for building applications.

For building shared objects, you must compile with `-fPIC` in
(`CFLAGS` or `CXXFLAGS`) and link with `-shared` (in `LDFLAGS`).

For other considerations involving shared objects, see:

* [Fedora Packaging Guidelines: Shared Libraries](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_shared_libraries)

# Customizing compiler and other build flags

It is possible to set RPM macros to change some aspects of the
compiler flags.  Changing these flags should be used as a last
recourse if other workarounds are not available.

### Toolchain selection

The default toolchain uses GCC, and the `%toolchain` macro is defined
as `gcc`.

It is enough to override `toolchain` macro and all relevant macro for C/C++
compilers will be switched. Either in the spec or in the command-line.

    %global toolchain clang

or:

    rpmbuild -D "toolchain clang" …

Inside a spec file it is also possible to determine which toolchain is in use
by testing the same macro. For example:

    %if "%{toolchain}" == "gcc"
    BuildRequires: gcc
    %endif

or:

    %if "%{toolchain}" == "clang"
    BuildRequires: clang compiler-rt
    %endif

### Controlling Type Safety

The macro `%build_type_safety_c` can be set to change the C type
safety level.  The default level is 3, see below.  It can be set to 0
to get historic levels of type safety.  Changing the type safety level
may depend on correct `CFLAGS` propagation during the build.  The
`%build_type_safety_c` macro needs to be set before `CFLAGS`-related
macros are expanded by RPM (that is, earlier in the file works
better).

Packages can set `%build_type_safety_c` to higher values to adopt
future distribution-wide type-safety increases early.  When changing
the `%build_type_safety_c` level to increase it, spec file should use
a construct like this to avoid *lowering* a future default:

```
%if %build_type_safety_c < 4
%global build_type_safety_c 4
%endif
```

At level 0, all C constructs that GCC accepts for backwards
compatibility with obsolete language standards are accepted during
package builds.  This is achieved by passing `-fpermissive` to GCC.

At level 1, the following additional error categories are enabled:

* `-Werror=implicit-int`: Reject declarations and definitions that
  omit a type name where one is required.  Examples are:
  `extern int_variable;`, `extern int_returning_function (void);`,
  and missing separate parameter type declarations in old-style
  function definitions.
* `-Werror=implicit-function-declaration`: Reject calls to functions
  to undeclared functions such as `function_not_defined_anywhere ()`.
  Previously, such expressions where we compiled as if a declaration
  `extern int function_not_defined_anywhere ();` (a prototype-less
  function declaration) were in scope.
* `-Werror=return-mismatch`: Reject `return` statements with missing
  or extra expressions, based on the declared return type of the
  function.
* `-Wdeclaration-missing-parameter-type`: Reject function declarations
  that contain unknown type names (which used to be treated as ignored
  identifier names).

At level 2, the following error category is enabled in addition:

* `-Werror=int-conversion`: Reject the use of integer expressions
  where a pointer type expected, and pointer expressions where an
  integer type is expected.  Without this option, GCC may produce an
  executable, but often, there are failures at run time because not
  the full 64 bits of pointers are preserved.

The additional level 3 error category is:

* `-Werror=incompatible-pointer-types`: An expression of one pointer
  type is used where different pointer type is expected.  (This does
  not cover signed/unsigned mismatches in the pointer target type.)

Clang errors out on more obsolete and invalid C constructs than C, so
the type safety is higher by default than with the GCC toolchain.

### Disable autotools compatibility patching

By default, the invocation of the `%configure` macro replaces
`config.guess` files in the source tree with the system version.  To
disable that, define this macro:

    %global _configure_gnuconfig_hack 0

`%configure` also patches `ltmain.sh` scripts, so that linker flags
are set as well during libtool-.  This can be switched off using:

    %global _configure_libtool_hardening_hack 0

Further patching happens in LTO mode, see below.

### Other autotools compatibility settings

During `%configure`, `--runstatedir` is automatically passed to the
`configure` script if support for this option is detected.  This
detection can fail if the package has multiple `configure` scripts
that invoke each other, and only some of them support `--runstatedir`.
To disable passing `--runstatedir`, use:

    %undefine _configure_use_runstatedir

### Disabling Link-Time Optimization

By default, builds use link-time optimization.  In this build mode,
object code is generated at the time of the final link, by combining
information from all available translation units, and taking into
account which symbols are exported.

To disable this optimization, include this in the spec file:

    %global _lto_cflags %{nil}

If LTO is enabled, `%configure` applies some common required fixes to
`configure` scripts.  To disable that, define the RPM macro
`_fix_broken_configure_for_lto` as `true` (sic; it has to be a shell
command).

### Lazy binding

If your package depends on the semantics of lazy binding (e.g., it has
plugins which load additional plugins to complete their dependencies,
before which some referenced functions are undefined), you should put
`-Wl,-z,lazy` at the end of the `LDFLAGS` setting when linking objects
which have such requirements.  Under these circumstances, it is
unnecessary to disable hardened builds (and thus lose full ASLR for
executables), or link everything without `-Wl,z,now` (non-lazy
binding).

### Hardened builds

By default, the build flags enable fully hardened builds.  To change
this, include this in the RPM spec file:

    %undefine _hardened_build

This turns off certain hardening features, as described in detail
below.  The main difference is that executables will be
position-dependent (no full ASLR) and use lazy binding.

### Source Fortification

By default, the build flags include `-Wp,-D_FORTIFY_SOURCE=3`: Source
fortification activates various hardening features in glibc:

* String functions such as `memcpy` attempt to detect buffer lengths
  and terminate the process if a buffer overflow is detected.
* `printf` format strings may only contain the `%n` format specifier
  if the format string resides in read-only memory.
* `open` and `openat` flags are checked for consistency with the
  presence of a *mode* argument.
* Plus other minor hardening changes.

These changes can, on rare occasions, break valid programs. The source
fortification level can be overridden by adding this in the RPM spec file:

    %define _fortify_level 2

to reduce source fortification level to 2 or:

    %undefine _fortify_level

to disable fortification altogether.

### Annotated builds/watermarking

By default, the build flags cause a special output section to be
included in ELF files which describes certain aspects of the build.
To change this for all compiler invocations, include this in the RPM
spec file:

    %undefine _annotated_build

Be warned that this turns off watermarking, making it impossible to do
full hardening coverage analysis for any binaries produced.

It is possible to disable annotations for individual compiler
invocations, using the `-fplugin-arg-annobin-disable` flag.  However,
the annobin plugin must still be loaded for this flag to be
recognized, so it has to come after the hardening flags on the command
line (it has to be added at the end of `CFLAGS`, or specified after
the `CFLAGS` variable contents).

### Keeping dependencies on unused shared objects

By default, ELF shared objects which are listed on the linker command
line, but which have no referencing symbols in the preceding objects,
are not added to the output file during the final link.

In order to keep dependencies on shared objects even if none of
their symbols are used, include this in the RPM spec file:

    %undefine _ld_as_needed

For example, this can be required if shared objects are used for their
side effects in ELF constructors, or for making them available to
dynamically loaded plugins.

### Switching to legacy relative relocations

By default, ELF objects use the architecture-independent `DT_RELR`
mechanism for relative relocations.  To switch to the older,
architecture-specific relocation scheme, add this to the RPM spec file:

    %undefine _ld_pack_relocs

This adds `-Wl,-z,pack-relative-relocs` to the linker flags (`LDFLAGS`).

### Specifying the build-id algorithm

If you want to specify a different build-id algorithm for your builds, you
can use the `%_build_id_flags` macro:

    %_build_id_flags -Wl,--build-id=sha1

### Strict symbol checks in the link editor (ld)

Optionally, the link editor will refuse to link shared objects which
contain undefined symbols.  Such symbols lack symbol versioning
information and can be bound to the wrong (compatibility) symbol
version at run time, and not the actual (default) symbol version which
would have been used if the symbol definition had been available at
static link time.  Furthermore, at run time, the dynamic linker will
not have complete dependency information (in the form of DT_NEEDED
entries), which can lead to errors (crashes) if IFUNC resolvers are
executed before the shared object containing them is fully relocated.

To switch on these checks, define this macro in the RPM spec file:

    %global _strict_symbol_defs_build 1

If this RPM spec option is active, link failures will occur if the
linker command line does not list all shared objects which are needed.
In this case, you need to add the missing DSOs (with linker arguments
such as `-lm`).  As a result, the link editor will also generated the
necessary DT_NEEDED entries.

In some cases (such as when a DSO is loaded as a plugin and is
expected to bind to symbols in the main executable), undefined symbols
are expected.  In this case, you can add

    %undefine _strict_symbol_defs_build

to the RPM spec file to disable these strict checks.  Alternatively,
you can pass `-z undefs` to ld (written as `-Wl,-z,undefs` on the gcc
command line).  The latter needs binutils 2.29.1-12.fc28 or later.

### Legacy -fcommon

Since version 10, [gcc defaults to `-fno-common`](https://gcc.gnu.org/gcc-10/porting_to.html#common).
Builds may fail with `multiple definition of ...` errors.

As a short term workaround for such failure,
it is possible to add `-fcommon` to the flags by defining `%_legacy_common_support`.

    %global _legacy_common_support 1

Properly fixing the failure is always preferred!

### Package note on ELF objects

A note that describes the package name, version, and architecture is
inserted via a linker script (`%_package_note_file`). The script is
generated when `%set_build_flags` is called. The linker option that
injects the linker script is added to `%{build_ldflags}` via the
`%{_package_note_flags}` macro.

To opt out of the use of this feature completely, the best way is to
undefine the first macro. Include this in the spec file:

    %undefine _package_note_file

The other macros can be undefined too to replace parts of the functionality.
If `%_generate_package_note_file` is undefined, the linker script will not
be generated, but the link flags may still refer to it. This may be useful
if the default generation method is insufficient and a different mechanism
will be used to generate `%_package_note_file`. If `%_package_note_flags`
is undefined, the linker argument that injects the script will not be added
to `%build_ldfags`, but the linker script would still be generated.

### Frame pointers

Frame pointers will be included by default via the `%_include_frame_pointers`
macro. To opt out, the best way is to undefine the macro. Include this in the
spec file:

    %undefine _include_frame_pointers

Note that opting out might still result in frame pointers being included on
architectures where they are part of the ABI (e.g. aarch64) depending on
compiler defaults.

### Post-build ELF object processing

By default, DWARF debugging information is separated from installed
ELF objects and put into `-debuginfo` subpackages.  To disable most
debuginfo processing (and thus the generation of these subpackages),
undefine `_enable_debug_packages`:

    %undefine _enable_debug_packages

Processing of debugging information is controlled using the
`find-debuginfo` tool from the `debugedit` package.  Several aspects
of its operation can be controlled at the RPM level.

* Creation of `-debuginfo` subpackages is enabled by default.
  To disable, undefine `_debuginfo_subpackages`.
* Likewise, `-debugsource` subpackages are automatically created.
  To disable, undefine `_debugsource_subpackages`.
  See [Separate Subpackage and Source Debuginfo](https://fedoraproject.org/wiki/Changes/SubpackageAndSourceDebuginfo)
  for background information.
* `_build_id_links`, `_unique_build_ids`, `_unique_debug_names`,
  `_unique_debug_srcs` control how debugging information and
  corresponding source files are represented on disk.
  See `/usr/lib/rpm/macros` for details.  The defaults
  enable parallel installation of `-debuginfo` packages for
  different package versions, as described in
  [Parallel Installable Debuginfo](https://fedoraproject.org/wiki/Changes/ParallelInstallableDebuginfo).
* By default, a compressed symbol table is preserved in the
  `.gnu_debugdata` section.  To disable that, undefine
  `_include_minidebuginfo`.
* To speed up debuggers, a `.gdb_index` section is created.  It can be
  disabled by undefining `_include_gdb_index`.
* Missing build IDs result in a build failure.  To ignore such
  problems, undefine `_missing_build_ids_terminate_build`.
* During processing, build IDs are recomputed to match the binary
  content.  To skip this step, define `_no_recompute_build_ids` as `1`.
* By default, the options in `_find_debuginfo_dwz_opts` turn on `dwz`
  (DWARF compression) processing.  Undefine this macro to disable this
  step.
* Additional options can be passed by defining the
  `_find_debuginfo_opts` macro.

After separation of debugging information, additional transformations
are applied, most of them also related to debugging information.
These steps can be skipped by undefining the corresponding macros:

* `__brp_strip`: Removal of leftover debugging information.  The tool
  specified by the `__strip` macro is invoked with the `-g` option on
  ELF object (`.o`) files.
* `__brp_strip_static_archive`: This is similar to `__brp_strip`, but
  processes static `.a` archives instead.  This operation is disabled
  by default, so DWARF is preserved in static libraries for the benefit
  of programs that link to them.  This may be disabled with a
  `%undefine _preserve_static_debuginfo` setting.
* `__brp_strip_comment_note`: This step removes unallocated `.note`
  sections, and `.comment` sections from ELF files.
* `__brp_strip_lto`: This step removes GCC LTO intermediate representation
  in ELF sections starting with `.gnu.lto_` and `.gnu.debuglto_`.  Skipping
  this step is strongly discouraged because the tight coupling of LTO
  data with the GCC version.  The underlying tool is again determined by the
  `__strip` macro.
* `__brp_llvm_compile_lto_elf`: This step replaces LLVM bitcode files
  with object files, thereby removing LLVM bitcode from the installed
  files.  This transformation is applied to object files in static `.a`
  archives, too.
* `__brp_ldconfig`: For each shared object on the library search path
  whose soname does not match its file name, a symbolic link from the
  soname to the file name is created.  This way, these shared objects
  are loadable immediately after installation, even if they are not yet
  listed in the `/etc/ld.so.cache` file (because `ldconfig` has not been
  invoked yet).
* `__brp_remove_la_files`: This step removes libtool-generated `.la`
  files from the installed files.

### Adding package-specific flags

In the case you only want to append to the existing flags, use:

* `%_pkg_extra_cflags` to append to the `%{build_cflags}` macro
* `%_pkg_extra_cxxflags` to append to the `%{build_cxxflags}` macro
* `%_pkg_extra_fflags` to append to the `%{build_fflags}` macro
* `%_pkg_extra_ldflags` to append to the `%{build_ldflags}` macro

This approach has a significant benefit over editing and re-exporting the
shell variables "by hand". And that is that it is propagated to all calls
of the `%set_build_flags` macro, in every section, in the whole SPECfile.
(instead of just the lines after the "export CFLAGS" etc. call until the end
of the current section)

### Adding distribution-specific flags

For the specific use-case of distributions forked from Fedora, there is a
set of macros nearly identical to the package-specific macros, that allows
for setting an extra set of distibution-wide flags, without changing the
existing ones:

* `%_distro_extra_cflags` to append to the `%{build_cflags}` macro
* `%_distro_extra_cxxflags` to append to the `%{build_cxxflags}` macro
* `%_distro_extra_fflags` to append to the `%{build_fflags}` macro
* `%_distro_extra_ldflags` to append to the `%{build_ldflags}` macro

These macros are never intended to be used by individual package maintainers.
The distribution-specific flags are applied before the package-specific flags.

# Individual compiler flags

Compiler flags end up in the environment variables `CFLAGS`,
`CXXFLAGS`, `FFLAGS`, and `FCFLAGS`.

The general (architecture-independent) build flags are:

* `-O2`: Turn on various GCC optimizations. See the
  [GCC manual](https://gcc.gnu.org/onlinedocs/gcc/Optimize-Options.html#index-O2).
  Optimization improves performance, the accuracy of warnings, and the
  reach of toolchain-based hardening, but it makes debugging harder.
* `-g`: Generate debugging information (DWARF). In Fedora, this data
  is separated into `-debuginfo` RPM packages whose installation is
  optional, so debuging information does not increase the size of
  installed binaries by default.
* `-pipe`: Run compiler and assembler in parallel and do not use a
  temporary file for the assembler input.  This can improve
  compilation performance.  (This does not affect code generation.)
* `-Wall`: Turn on various GCC warnings.
  See the [GCC manual](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#index-Wall).
* `-Wno-complain-wrong-lang`: Do not warn about front end mismatches
  (e.g, using `-Werror=format-security` with Fortran).  Only included
  in `%optflags`, and not the front-end-specific `%build_*` macros.
* `-Werror=format-security`: Turn on format string warnings and treat
  them as errors.
  See the [GCC manual](https://gcc.gnu.org/onlinedocs/gcc/Warning-Options.html#index-Wformat-security).
  This can occasionally result in compilation errors. In that case,
  the best option is to rewrite the source code so that only constant
  format strings (string literals) are used.
* Other `-Werror=` options.  See **Controlling C Type Safety**.
* `-U_FORTIFY_SOURCE, -Wp,-U_FORTIFY_SOURCE -Wp,-D_FORTIFY_SOURCE=3`:
  See the Source Fortification section above and the `%_fortify_level`
  override.
* `-fexceptions`: Provide exception unwinding support for C programs.
  See the [`-fexceptions` option in the GCC
  manual](https://gcc.gnu.org/onlinedocs/gcc/Code-Gen-Options.html#index-fexceptions)
  and the [`cleanup` variable
  attribute](https://gcc.gnu.org/onlinedocs/gcc/Common-Variable-Attributes.html#index-cleanup-variable-attribute).
  This also hardens cancellation handling in C programs because
  it is not required to use an on-stack jump buffer to install
  a cancellation handler with `pthread_cleanup_push`.  It also makes
  it possible to unwind the stack (using C++ `throw` or Rust panics)
  from C callback functions if a C library supports non-local exits
  from them (e.g., via `longjmp`).
* `-fasynchronous-unwind-tables`: Generate full unwind information
  covering all program points.  This is required for support of
  asynchronous cancellation and proper unwinding from signal
  handlers.  It also makes performance and debugging tools more
  useful because unwind information is available without having to
  install (and load) debugging information.  (Not enabled on armhfp
  due to architectural differences in stack management.)
* `-Wp,-D_GLIBCXX_ASSERTIONS`: Enable lightweight assertions in the
  C++ standard library, such as bounds checking for the subscription
  operator on vectors.  (This flag is added to both `CFLAGS` and
  `CXXFLAGS`; C compilations will simply ignore it.)
* `-fstack-protector-strong`: Instrument functions to detect
  stack-based buffer overflows before jumping to the return address on
  the stack.  The *strong* variant only performs the instrumentation
  for functions whose stack frame contains addressable local
  variables.  (If the address of a variable is never taken, it is not
  possible that a buffer overflow is caused by incorrect pointer
  arithmetic involving a pointer to that variable.)
* `-fstack-clash-protection`: Turn on instrumentation to avoid
  skipping the guard page in large stack frames.  (Without this flag,
  vulnerabilities can result where the stack overlaps with the heap,
  or thread stacks spill into other regions of memory.)  This flag is
  fully ABI-compatible and has adds very little run-time overhead.
  This flag is currently not available on armhfp (both `gcc` and `clang`
  toolchains).
* `-flto=auto`: Enable link-time optimization (LTO), using `make` job server
  integration for parallel processing.  (`gcc` toolchain only)
* `-ffat-lto-objects`: Generate EFL object files which contain both
  object code and LTO intermediate representation.  (`gcc` toolchain only)
* `-flto`: Enable link-time optimization. (`clang` toolchain only)
* `-grecord-gcc-switches`: Include select GCC command line switches in
  the DWARF debugging information.  This is useful for detecting the
  presence of certain build flags and general hardening coverage.
* `-fcommon`: This optional flag is used to build legacy software
  which relies on C tentative definitions.  It is disabled by default.

For hardened builds (which are enabled by default, see above for how
to disable them), the flag
`-specs=/usr/lib/rpm/redhat/redhat-hardened-cc1` is added to the
command line.  It adds the following flag to the command line:

* `-fPIE`: Compile for a position-independent executable (PIE),
  enabling full address space layout randomization (ASLR).  This is
  similar to `-fPIC`, but avoids run-time indirections on certain
  architectures, resulting in improved performance and slightly
  smaller executables.  However, compared to position-dependent code
  (the default generated by GCC), there is still a measurable
  performance impact.

  If the command line also contains `-r` (producing a relocatable
  object file), `-fpic` or `-fPIC`, this flag is automatically
  dropped.  (`-fPIE` can only be used for code which is linked into
  the main program.) Code which goes into static libraries should be
  compiled with `-fPIE`, except when this code is expected to be
  linked into DSOs, when `-fPIC` must be used.

  To be effective, `-fPIE` must be used with the `-pie` linker flag
  when producing an executable, see below.

To support [binary watermarks for ELF
objects](https://fedoraproject.org/wiki/Toolchain/Watermark) using
annobin, the `-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1` flag is
added by default (with the `gcc` toolchain).  This can be switched off
by undefining the `%_annotated_build` RPM macro (see above).  Binary
watermarks are currently disabled on armhpf, and with the `clang`
toolchain.

If frame pointers are enabled by default (via `%_include_frame_pointers`),
the `-fno-omit-frame-pointer` will be added on all architectures except i686
and s390x. Additional flags will be added on specific architectures:

* `-mno-omit-leaf-frame-pointer` on x86_64 and aarch64

### Architecture-specific compiler flags

These compiler flags are enabled for all builds (hardened/annotated or
not), but their selection depends on the architecture:

* `-fcf-protection`: Instrument binaries to guard against
  ROP/JOP exploitation techniques.  Used on x86_64.
* `-mbranch-protection=standard`: Instrument binaries to guard against
   ROP/JOP exploitation techniques.  Used on aarch64.
* `-m64` and `-m32`: Some GCC builds support both 32-bit and 64-bit in
  the same compilation.  For such architectures, the RPM build process
  explicitly selects the architecture variant by passing this compiler
  flag.

In addition, `redhat-rpm-config` re-selects the built-in default
tuning in the `gcc` package.  These settings are:

* **armhfp**: `-march=armv7-a -mfpu=vfpv3-d16 -mfloat-abi=hard`
  selects an Arm subarchitecture based on the ARMv7-A architecture
  with 16 64-bit floating point registers.  `-mtune=cortex-8a` selects
  tuning for the Cortex-A8 implementation (while preserving
  compatibility with other ARMv7-A implementations).
  `-mabi=aapcs-linux` switches to the AAPCS ABI for GNU/Linux.
* **i686**: `-march=i686` is used to select a minmum support CPU level
  of i686 (corresponding to the Pentium Pro).  SSE2 support is enabled
  with `-msse2` (so only CPUs with SSE2 support can run the compiled
  code; SSE2 was introduced first with the Pentium 4).
  `-mtune=generic` activates tuning for a current blend of CPUs (under
  the assumption that most users of i686 packages obtain them through
  an x86_64 installation on current hardware).  `-mfpmath=sse`
  instructs GCC to use the SSE2 unit for floating point math to avoid
  excess precision issues.  `-mstackrealign` avoids relying on the
  stack alignment guaranteed by the current version of the i386 ABI.
* **ppc64le**: `-mcpu=power8 -mtune=power8` selects a minimum
  supported CPU level of POWER8 (the first CPU with ppc64le support)
  and tunes for POWER8.
* **s390x**: `-march=zEC12 -mtune=z13` specifies a minimum supported
  CPU level of zEC12, while optimizing for a subsequent CPU generation
  (z13).
* **x86_64**: `-mtune=generic` selects tuning which is expected to
   beneficial for a broad range of current CPUs.  Distribution-specific
   defaults for `-march=x86-64-v2` or `-march=x86-64-v3` may be
   applied.  The default can be overriden (for any distribution)
   by specifying `--target x86_64_v2`, `--target x86_64_v3`,
   `--target x86_64_v4` in the `rpmbuild` invocation.
   TLS descriptors are enabled using `-mtls-dialect=gnu2`.
* **aarch64** does not have any architecture-specific tuning.

### Vala-specific compiler flags

 * `-g`: causes valac to emit `#line` directives in the generated C
   source code. This improves backtrace generation by causing gdb to
   point to Vala source file and line number instead of the generated C
   source when possible.

# Individual linker flags

Linker flags end up in the environment variable `LDFLAGS`.

The linker flags listed below are injected.  Note that they are
prefixed with `-Wl` because it is expected that these flags are passed
to the compiler driver `gcc`, and not directly to the link editor
`ld`.

* `-z relro`: Activate the *read-only after relocation* feature.
  Constant data and relocations are placed on separate pages, and the
  dynamic linker is instructed to revoke write permissions after
  dynamic linking.  Full protection of relocation data requires the
  `-z now` flag (see below).
* `--as-needed`: In the final link, only generate ELF dependencies
  for shared objects that actually provide symbols required by the link.
  Shared objects which are not needed to fulfill symbol dependencies
  are essentially ignored due to this flag.
* `-z pack-relative-relocs`: Use the portable `DT_RELR` scheme for
  relative relocations, resulting in reduced startup time compared to
  legacy architecture-specific relocations.  (`-z pack-relative-relocs`
  is currently disabled on s390x due to toolchain limitations.)
* `-z defs`: Refuse to link shared objects (DSOs) with undefined symbols
  (optional, see above).

For hardened builds, some more linker options are added to the
compiler driver command line.  These can be disabled by undefining the
`%_hardened_build` macro - see above.

* `-pie`: Produce a PIE binary.  This is only activated for the main
  executable, and only if it is dynamically linked.  This requires
  that all objects which are linked in the main executable have been
  compiled with `-fPIE` or `-fPIC` (or `-fpie` or `-fpic`; see above).
  By itself, `-pie` has only a slight performance impact because it
  disables some link editor optimization, however the `-fPIE` compiler
  flag has some overhead.
  Note: this option is added via adding a spec file to the compiler
  driver command line (`-specs=/usr/lib/rpm/redhat/redhat-hardened-ld`)
  rather than using the `-Wl` mechanism mentioned above.  As a result
  this option is only enabled if the compiler driver is gcc.
* `-z now`: Disable lazy binding and turn on the `BIND_NOW` dynamic
  linker feature.  Lazy binding involves an array of function pointers
  which is writable at run time (which could be overwritten as part of
  security exploits, redirecting execution).  Therefore, it is
  preferable to turn of lazy binding, although it increases startup
  time.

In addition hardened builds default to converting a couple of linker
warning messages into errors, because they represent potential
missed hardening opportunities, and warnings in the linker's output are
often ignored.  This behaviour can be turned off by undefining the
`%_hardened_build` macro as mentioned above, or by undefining the
`%_hardened_linker_errors` macro.  The linker options enabled by this
feature are:

* `--error-rwx-segments`: Generates an error if an output binary would
  contain a loadable memory segment with read, write and execute
  permissions.  It will also generate an error if a thread local
  storage (TLS) segment is created with execute permission.  The
  error can be disabled on an individual basis by adding the
  `--no-warn-rwx-segments` option to the linker command line.
* `--error-execstack`: Generates an error if an output binary would
  contain a stack that is held in memory with execute permission.
  If a binary is being intentionally created with an executable stack
  then the linker command line option `-z execstack` can be used to
  indicate this.

Note: these options are added via a spec file on the compiler driver
command line (`-specs=/usr/lib/rpm/redhat/redhat-hardened-ld-errors`)
rather than using the `-Wl` mechanism mentioned above.  As a result
these options are only enabled if the compiler driver is gcc.  In
addition the spec file only adds the options if the `-fuse-ld=...`
option has not been enabled.  This prevents the options from being
used when the gold or lld linkers are enabled.
  
# Support for extension builders

Some packages include extension builders that allow users to build
extension modules (which are usually written in C and C++) under the
control of a special-purpose build system.  This is a common
functionality provided by scripting languages such as Python and Perl.
Traditionally, such extension builders captured the Fedora build flags
when these extension were built.  However, these compiler flags are
adjusted for a specific Fedora release and toolchain version and
therefore do not work with a custom toolchain (e.g., different C/C++
compilers), and users might want to build their own extension modules
with such toolchains.

The macros `%{extension_cflags}`, `%{extension_cxxflags}`,
`%{extension_fflags}`, `%{extension_ldflags}` contain a subset of
flags that have been adjusted for compatibility with alternative
toolchains.

Currently the -fexceptions, -fcf-protection (on x86_64) and
-mbranch-protection=standard (on aarch64) flags are preserved
for binary compatibility with the languages the extensions are
built against.

Extension builders should detect whether they are performing a regular
RPM build (e.g., by looking for an `RPM_OPT_FLAGS` variable).  In this
case, they should use the *current* set of Fedora build flags (that
is, the output from `rpm --eval '%{build_cflags}'` and related
commands).  Otherwise, when not performing an RPM build, they can
either use hard-coded extension builder flags (thus avoiding a
run-time dependency on `redhat-rpm-config`), or use the current
extension builder flags (with a run-time dependency on
`redhat-rpm-config`).

As a result, extension modules built for Fedora will use the official
Fedora build flags, while users will still be able to build their own
extension modules with custom toolchains.
