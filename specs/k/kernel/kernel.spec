# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# All Azure Linux specs with overlays include this macro file, irrespective of whether new macros have been added.
%{load:%{_sourcedir}/kernel.azl.macros}

# All Global changes to build and install go here.
# Per the below section about __spec_install_pre, any rpm
# environment changes that affect %%install need to go
# here before the %%install macro is pre-built.

# Disable frame pointers
%undefine _include_frame_pointers

# Disable LTO in userspace packages.
%global _lto_cflags %{nil}

# Option to enable compiling with clang instead of gcc.
%bcond_with toolchain_clang

%if %{with toolchain_clang}
%global toolchain clang
%endif

# Compile the kernel with LTO (only supported when building with clang).
%bcond_with clang_lto

%if %{with clang_lto} && %{without toolchain_clang}
{error:clang_lto requires --with toolchain_clang}
%endif

# RPM macros strip everything in BUILDROOT, either with __strip
# or find-debuginfo.sh. Make use of __spec_install_post override
# and save/restore binaries we want to package as unstripped.
%define buildroot_unstripped %{_builddir}/root_unstripped
%define buildroot_save_unstripped() \
(cd %{buildroot}; cp -rav --parents -t %{buildroot_unstripped}/ %1 || true) \
%{nil}
%define __restore_unstripped_root_post \
    echo "Restoring unstripped artefacts %{buildroot_unstripped} -> %{buildroot}" \
    cp -rav %{buildroot_unstripped}/. %{buildroot}/ \
%{nil}

# The kernel's %%install section is special
# Normally the %%install section starts by cleaning up the BUILD_ROOT
# like so:
#
# %%__spec_install_pre %%{___build_pre}\
#     [ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "${RPM_BUILD_ROOT}"\
#     mkdir -p `dirname "$RPM_BUILD_ROOT"`\
#     mkdir "$RPM_BUILD_ROOT"\
# %%{nil}
#
# But because of kernel variants, the %%build section, specifically
# BuildKernel(), moves each variant to its final destination as the
# variant is built.  This violates the expectation of the %%install
# section.  As a result we snapshot the current env variables and
# purposely leave out the removal section.  All global wide changes
# should be added above this line otherwise the %%install section
# will not see them.
%global __spec_install_pre %{___build_pre}

# Replace '-' with '_' where needed so that variants can use '-' in
# their name.
%define uname_suffix() %{lua:
	local flavour = rpm.expand('%{?1:+%{1}}')
	flavour = flavour:gsub('-', '_')
	if flavour ~= '' then
		print(flavour)
	end
}

# This returns the main kernel tied to a debug variant. For example,
# kernel-debug is the debug version of kernel, so we return an empty
# string. However, kernel-64k-debug is the debug version of kernel-64k,
# in this case we need to return "64k", and so on. This is used in
# macros below where we need this for some uname based requires.
%define uname_variant() %{lua:
	local flavour = rpm.expand('%{?1:%{1}}')
	_, _, main, sub = flavour:find("(%w+)-(.*)")
	if main then
		print("+" .. main)
	end
}


# At the time of this writing (2019-03), RHEL8 packages use w2.xzdio
# compression for rpms (xz, level 2).
# Kernel has several large (hundreds of mbytes) rpms, they take ~5 mins
# to compress by single-threaded xz. Switch to threaded compression,
# and from level 2 to 3 to keep compressed sizes close to "w2" results.
#
# NB: if default compression in /usr/lib/rpm/redhat/macros ever changes,
# this one might need tweaking (e.g. if default changes to w3.xzdio,
# change below to w4T.xzdio):
#
# This is disabled on i686 as it triggers oom errors

%ifnarch i686
%define _binary_payload w3T.xzdio
%endif

Summary: The Linux kernel
%if 0%{?fedora}
%define secure_boot_arch x86_64
%else
%define secure_boot_arch x86_64 aarch64 s390x ppc64le
%endif

# Signing for secure boot authentication
%ifarch %{secure_boot_arch}
%global signkernel 1
%else
%global signkernel 0
%endif

# RHEL/CentOS specific .SBAT entries
%if 0%{?centos}
%global sbat_suffix centos
%else
%if 0%{?fedora}
%global sbat_suffix fedora
%else
%global sbat_suffix rhel
%endif
%endif

# Sign modules on all arches
%global signmodules 1

# Add additional rhel certificates to system trusted keys.
%global rhelkeys 1

# Compress modules only for architectures that build modules
%ifarch noarch
%global zipmodules 0
%else
%global zipmodules 1
%endif

# Default compression algorithm
%global compression xz
%global compression_flags --compress --check=crc32 --lzma2=dict=1MiB
%global compext xz

%if 0%{?fedora}
%define primary_target fedora
%else
%define primary_target rhel
%endif

#
# genspec.sh variables
#

# kernel package name
%global package_name kernel
%global gemini 0
# Include Fedora files
%global include_fedora 1
# Include RHEL files
%global include_rhel 1
# Include RT files
%global include_rt 1
# Include Automotive files
%global include_automotive 0
# Provide Patchlist.changelog file
%global patchlist_changelog 1
# Set released_kernel to 1 when the upstream source tarball contains a
#  kernel release. (This includes prepatch or "rc" releases.)
# Set released_kernel to 0 when the upstream source tarball contains an
#  unreleased kernel development snapshot.
%global released_kernel 1
# Set debugbuildsenabled to 1 to build separate base and debug kernels
#  (on supported architectures). The kernel-debug-* subpackages will
#  contain the debug kernel.
# Set debugbuildsenabled to 0 to not build a separate debug kernel, but
#  to build the base kernel using the debug configuration. (Specifying
#  the --with-release option overrides this setting.)
%define debugbuildsenabled 1
# define buildid .local
%define specrpmversion 6.18.5
%define specversion %{specrpmversion}
%define patchversion 6.18
%define pkgrelease %{azl_pkgrelease}
%define kversion 6
%define tarfile_release %{specrpmversion}
# This is needed to do merge window version magic
%define patchlevel 18
# This allows pkg_release to have configurable %%{?dist} tag
%define specrelease %{kextraversion}.%{azl_pkgrelease}%{?buildid}%{?dist}
# This defines the kabi tarball version
%define kabiversion 6.18.13

# If this variable is set to 1, a bpf selftests build failure will cause a
# fatal kernel package build error
%define selftests_must_build 0

#
# End of genspec.sh variables
#

%define pkg_release %{specrelease}

# libexec dir is not used by the linker, so the shared object there
# should not be exported to RPM provides
%global __provides_exclude_from ^%{_libexecdir}/kselftests

# The following build options are (mostly) enabled by default, but may become
# enabled/disabled by later architecture-specific checks.
# Where disabled by default, they can be enabled by using --with <opt> in the
# rpmbuild command, or by forcing these values to 1.
# Where enabled by default, they can be disabled by using --without <opt> in
# the rpmbuild command, or by forcing these values to 0.
#
# standard kernel
%define with_up        %{?_without_up:        0} %{?!_without_up:        1}
# build the base variants
%define with_base      %{?_without_base:      0} %{?!_without_base:      1}
# build also debug variants
%define with_debug     %{?_without_debug:     0} %{?!_without_debug:     1}
# kernel-zfcpdump (s390 specific kernel for zfcpdump)
%define with_zfcpdump  %{?_without_zfcpdump:  0} %{?!_without_zfcpdump:  1}
# kernel-16k (aarch64 kernel with 16K page_size)
%define with_arm64_16k %{?_with_arm64_16k:    1} %{?!_with_arm64_16k:    0}
# kernel-64k (aarch64 kernel with 64K page_size)
%define with_arm64_64k %{?_without_arm64_64k: 0} %{?!_without_arm64_64k: 1}
# we default reatime builds to off for fedora and on for rhel/centos/eln
%if 0%{?fedora}
# kernel-rt (x86_64 and aarch64 only PREEMPT_RT enabled kernel)
%define with_realtime  %{?_with_realtime:  1} %{?!_with_realtime:  0}
# kernel-rt-64k (aarch64 RT kernel with 64K page_size)
%define with_realtime_arm64_64k %{?_with_realtime_arm64_64k: 1} %{?!_with_realtime_arm64_64k: 0}
%else
# kernel-rt (x86_64 and aarch64 only PREEMPT_RT enabled kernel)
%define with_realtime  %{?_without_realtime:  0} %{?!_without_realtime:  1}
# kernel-rt-64k (aarch64 RT kernel with 64K page_size)
%define with_realtime_arm64_64k %{?_without_realtime_arm64_64k: 0} %{?!_without_realtime_arm64_64k: 1}
%endif
# kernel-automotive (x86_64 and aarch64 with PREEMPT_RT enabled - currently off by default)
%define with_automotive %{?_with_automotive:  1} %{?!_with_automotive:   0}

# Supported variants
#            with_base with_debug    with_gcov
# up         X         X             X
# zfcpdump   X                       X
# arm64_16k  X         X             X
# arm64_64k  X         X             X
# realtime   X         X             X
# automotive X         X             X

# kernel-doc
%define with_doc       %{?_without_doc:       0} %{?!_without_doc:       1}
# kernel-headers
%define with_headers   %{?_without_headers:   0} %{?!_without_headers:   1}
%define with_cross_headers   %{?_without_cross_headers:   0} %{?!_without_cross_headers:   1}
# perf
%define with_perf      %{?_without_perf:      0} %{?!_without_perf:      1}
# libperf
%define with_libperf   %{?_without_libperf:   0} %{?!_without_libperf:   1}
# tools
%define with_tools     %{?_without_tools:     0} %{?!_without_tools:     1}
# ynl
%define with_ynl      %{?_without_ynl:      0} %{?!_without_ynl:      1}
# kernel-debuginfo
%define with_debuginfo %{?_without_debuginfo: 0} %{?!_without_debuginfo: 1}
# kernel-abi-stablelists
%define with_kernel_abi_stablelists %{?_without_kernel_abi_stablelists: 0} %{?!_without_kernel_abi_stablelists: 1}
# internal samples and selftests
%define with_selftests %{?_without_selftests: 0} %{?!_without_selftests: 1}
#
# Additional options for user-friendly one-off kernel building:
#
# Only build the base kernel (--with baseonly):
%define with_baseonly  %{?_with_baseonly:     1} %{?!_with_baseonly:     0}
# Only build the debug variants (--with dbgonly):
%define with_dbgonly   %{?_with_dbgonly:      1} %{?!_with_dbgonly:      0}
# Only build the realtime kernel (--with rtonly):
%define with_rtonly    %{?_with_rtonly:       1} %{?!_with_rtonly:       0}
# Only build the automotive variant of the kernel (--with automotiveonly):
%define with_automotiveonly %{?_with_automotiveonly:       1} %{?!_with_automotiveonly:       0}
# Build the automotive kernel (--with automotive_build), this builds base variant with automotive config/options:
%define with_automotive_build %{?_with_automotive_build:   1} %{?!_with_automotive_build:     0}
# Only build the tools package
%define with_toolsonly %{?_with_toolsonly:    1} %{?!_with_toolsonly:    0}
# Control whether we perform a compat. check against published ABI.
%define with_kabichk   %{?_without_kabichk:   0} %{?!_without_kabichk:   1}
# Temporarily disable kabi checks until RC.
%define with_kabichk 0
# Control whether we perform a compat. check against DUP ABI.
%define with_kabidupchk %{?_with_kabidupchk:  1} %{?!_with_kabidupchk:   0}
#
# Control whether to run an extensive DWARF based kABI check.
# Note that this option needs to have baseline setup in SOURCE300.
%define with_kabidwchk %{?_without_kabidwchk: 0} %{?!_without_kabidwchk: 1}
%define with_kabidw_base %{?_with_kabidw_base: 1} %{?!_with_kabidw_base: 0}
#
# Control whether to install the vdso directories.
%define with_vdso_install %{?_without_vdso_install: 0} %{?!_without_vdso_install: 1}
#
# should we do C=1 builds with sparse
%define with_sparse    %{?_with_sparse:       1} %{?!_with_sparse:       0}
#
# Cross compile requested?
%define with_cross    %{?_with_cross:         1} %{?!_with_cross:        0}
#
# build a release kernel on rawhide
%define with_release   %{?_with_release:      1} %{?!_with_release:      0}

# verbose build, i.e. no silent rules and V=1
%define with_verbose %{?_with_verbose:        1} %{?!_with_verbose:      0}

#
# check for mismatched config options
%define with_configchecks %{?_without_configchecks:        0} %{?!_without_configchecks:        1}

#
# gcov support
%define with_gcov %{?_with_gcov:1}%{?!_with_gcov:0}

# Want to build a vanilla kernel build without any non-upstream patches?
%define with_vanilla %{?_with_vanilla: 1} %{?!_with_vanilla: 0}

%ifarch x86_64 aarch64 riscv64
%define with_efiuki %{?_without_efiuki: 0} %{?!_without_efiuki: 1}
%else
%define with_efiuki 0
%endif

%if 0%{?fedora}
# Kernel headers are being split out into a separate package
%define with_headers 0
%define with_cross_headers 0
# no stablelist
%define with_kernel_abi_stablelists 0
%define with_arm64_64k 0
%define with_automotive 0
%endif

%if %{with_verbose}
%define make_opts V=1
%else
%define make_opts -s
%endif

%if %{with toolchain_clang}
%ifarch s390x ppc64le
%global llvm_ias 0
%else
%global llvm_ias 1
%endif
%global clang_make_opts HOSTCC=clang CC=clang LLVM_IAS=%{llvm_ias} LLVM=1
%global make_opts %{make_opts} %{clang_make_opts}
%endif

# turn off debug kernel and kabichk for gcov builds
%if %{with_gcov}
%define with_debug 0
%define with_kabichk 0
%define with_kabidupchk 0
%define with_kabidwchk 0
%define with_kabidw_base 0
%define with_kernel_abi_stablelists 0
%endif

# turn off kABI DWARF-based check if we're generating the base dataset
%if %{with_kabidw_base}
%define with_kabidwchk 0
%endif

%define make_target bzImage
%define image_install_path boot

%define KVERREL %{specversion}-%{release}.%{_target_cpu}
%define KVERREL_RE %(echo %KVERREL | sed 's/+/[+]/g')
%define hdrarch %_target_cpu
%define asmarch %_target_cpu

%if 0%{!?nopatches:1}
%define nopatches 0
%endif

%if %{with_vanilla}
%define nopatches 1
%endif

%if %{with_release}
%define debugbuildsenabled 1
%endif

%if !%{with_debuginfo}
%define _enable_debug_packages 0
%endif
%define debuginfodir /usr/lib/debug
# Needed because we override almost everything involving build-ids
# and debuginfo generation. Currently we rely on the old alldebug setting.
%global _build_id_links alldebug

# if requested, only build base kernel
%if %{with_baseonly}
%define with_debug 0
%define with_realtime 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%endif

# if requested, only build debug kernel
%if %{with_dbgonly}
%define with_base 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%endif

# if requested, only build realtime kernel
%if %{with_rtonly}
%define with_realtime 1
%define with_realtime_arm64_64k 1
%define with_automotive 0
%define with_up 0
%define with_debug 0
%define with_debuginfo 0
%define with_vdso_install 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_headers 0
%define with_efiuki 0
%define with_zfcpdump 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%endif

# if requested, only build the automotive variant of the kernel
%if %{with_automotiveonly}
%define with_automotive 1
%define with_realtime 0
%define with_up 0
%define with_debug 0
%define with_debuginfo 0
%define with_vdso_install 0
%define with_selftests 1
%endif

# if requested, build kernel-automotive
%if %{with_automotive_build}
%define with_automotive 1
%define with_selftests 1
%endif

# if requested, only build tools
%if %{with_toolsonly}
%define with_tools 1
%define with_up 0
%define with_base 0
%define with_debug 0
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_automotive 0
%define with_cross_headers 0
%define with_doc 0
%define with_selftests 0
%define with_headers 0
%define with_efiuki 0
%define with_zfcpdump 0
%define with_vdso_install 0
%define with_kabichk 0
%define with_kabidwchk 0
%define with_kabidw_base 0
%define with_kernel_abi_stablelists 0
%define with_selftests 0
%define with_vdso_install 0
%define with_configchecks 0
%endif

# RT and Automotive kernels are only built on x86_64 and aarch64
%ifnarch x86_64 aarch64
%define with_realtime 0
%define with_automotive 0
%endif

%if %{with_automotive}
# overrides compression algorithms for automotive
%global compression zstd
%global compression_flags --rm
%global compext zst

# automotive does not support the following variants
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_efiuki 0
%define with_doc 0
%define with_headers 0
%define with_cross_headers 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_kabichk 0
%define with_kernel_abi_stablelists 0
%define with_kabidw_base 0
%define signkernel 0
%define signmodules 1
%define rhelkeys 0
%endif


%if %{zipmodules}
%global zipsed -e 's/\.ko$/\.ko.%compext/'
# for parallel xz processes, replace with 1 to go back to single process
%endif

# turn off kABI DUP check and DWARF-based check if kABI check is disabled
%if !%{with_kabichk}
%define with_kabidupchk 0
%define with_kabidwchk 0
%endif

%if %{with_vdso_install}
%define use_vdso 1
%endif

%ifnarch noarch
%define with_kernel_abi_stablelists 0
%endif

# Overrides for generic default options

# only package docs noarch
%ifnarch noarch
%define with_doc 0
%define doc_build_fail true
%endif

%if 0%{?fedora}
# don't do debug builds on anything but aarch64 and x86_64
%ifnarch aarch64 x86_64
%define with_debug 0
%endif
%endif

%define all_configs %{name}-%{specrpmversion}-*.config

# don't build noarch kernels or headers (duh)
%ifarch noarch
%define with_up 0
%define with_realtime 0
%define with_automotive 0
%define with_headers 0
%define with_cross_headers 0
%define with_tools 0
%define with_perf 0
%define with_libperf 0
%define with_selftests 0
%define with_debug 0
%endif

# sparse blows up on ppc
%ifnarch ppc64le
%define with_sparse 0
%endif

# zfcpdump mechanism is s390 only
%ifnarch s390x
%define with_zfcpdump 0
%endif

# 16k and 64k variants only for aarch64
%ifnarch aarch64
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_realtime_arm64_64k 0
%endif

%if 0%{?fedora}
# This is not for Fedora
%define with_zfcpdump 0
%endif

# Per-arch tweaks

%ifarch i686
%define asmarch x86
%define hdrarch i386
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch x86_64
%define asmarch x86
%define kernel_image arch/x86/boot/bzImage
%endif

%ifarch ppc64le
%define asmarch powerpc
%define hdrarch powerpc
%define make_target vmlinux
%define kernel_image vmlinux
%define kernel_image_elf 1
%define use_vdso 0
%endif

%ifarch s390x
%define asmarch s390
%define hdrarch s390
%define kernel_image arch/s390/boot/bzImage
%define vmlinux_decompressor arch/s390/boot/vmlinux
%endif

%ifarch aarch64
%define asmarch arm64
%define hdrarch arm64
%define make_target vmlinuz.efi
%define kernel_image arch/arm64/boot/vmlinuz.efi
%endif

%ifarch riscv64
%define asmarch riscv
%define hdrarch riscv
%define make_target vmlinuz.efi
%define kernel_image arch/riscv/boot/vmlinuz.efi
%endif

# Should make listnewconfig fail if there's config options
# printed out?
%if %{nopatches}
%define with_configchecks 0
%endif

# To temporarily exclude an architecture from being built, add it to
# %%nobuildarches. Do _NOT_ use the ExclusiveArch: line, because if we
# don't build kernel-headers then the new build system will no longer let
# us use the previous build of that package -- it'll just be completely AWOL.
# Which is a BadThing(tm).

# We only build kernel-headers on the following...
%if 0%{?fedora}
%define nobuildarches i386
%else
%define nobuildarches i386 i686
%endif

%ifarch %nobuildarches
# disable BuildKernel commands
%define with_up 0
%define with_debug 0
%define with_zfcpdump 0
%define with_arm64_16k 0
%define with_arm64_64k 0
%define with_realtime 0
%define with_realtime_arm64_64k 0
%define with_automotive 0

%define with_debuginfo 0
%define with_perf 0
%define with_libperf 0
%define with_tools 0
%define with_selftests 0
%define _enable_debug_packages 0
%endif

# Architectures we build tools/cpupower on
%if 0%{?fedora}
%define cpupowerarchs %{ix86} x86_64 ppc64le aarch64 riscv64
%else
%define cpupowerarchs i686 x86_64 ppc64le aarch64 riscv64
%endif

%if 0%{?use_vdso}
%define _use_vdso 1
%else
%define _use_vdso 0
%endif

# If build of debug packages is disabled, we need to know if we want to create
# meta debug packages or not, after we define with_debug for all specific cases
# above. So this must be at the end here, after all cases of with_debug or not.
%define with_debug_meta 0
%if !%{debugbuildsenabled}
%if %{with_debug}
%define with_debug_meta 1
%endif
%define with_debug 0
%endif

# short-hand for "are we building base/non-debug variants of ...?"
%if %{with_up} && %{with_base}
%define with_up_base 1
%else
%define with_up_base 0
%endif
%if %{with_realtime} && %{with_base}
%define with_realtime_base 1
%else
%define with_realtime_base 0
%endif
%if %{with_automotive} && %{with_base} && !%{with_automotive_build}
%define with_automotive_base 1
%else
%define with_automotive_base 0
%endif
%if %{with_arm64_16k} && %{with_base}
%define with_arm64_16k_base 1
%else
%define with_arm64_16k_base 0
%endif
%if %{with_arm64_64k} && %{with_base}
%define with_arm64_64k_base 1
%else
%define with_arm64_64k_base 0
%endif
%if %{with_realtime_arm64_64k} && %{with_base}
%define with_realtime_arm64_64k_base 1
%else
%define with_realtime_arm64_64k_base 0
%endif

#
# Packages that need to be installed before the kernel is, because the %%post
# scripts use them.
#
%define kernel_prereq  coreutils, systemd >= 203-2, /usr/bin/kernel-install
%define initrd_prereq  dracut >= 027


Name: %{package_name}
License: ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-2-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-only WITH Linux-syscall-note) OR CDDL-1.0) AND ((GPL-2.0-only WITH Linux-syscall-note) OR Linux-OpenIB) AND ((GPL-2.0-only WITH Linux-syscall-note) OR MIT) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR BSD-3-Clause) AND ((GPL-2.0-or-later WITH Linux-syscall-note) OR MIT) AND 0BSD AND BSD-2-Clause AND (BSD-2-Clause OR Apache-2.0) AND BSD-3-Clause AND BSD-3-Clause-Clear AND CC0-1.0 AND GFDL-1.1-no-invariants-or-later AND GPL-1.0-or-later AND (GPL-1.0-or-later OR BSD-3-Clause) AND (GPL-1.0-or-later WITH Linux-syscall-note) AND GPL-2.0-only AND (GPL-2.0-only OR Apache-2.0) AND (GPL-2.0-only OR BSD-2-Clause) AND (GPL-2.0-only OR BSD-3-Clause) AND (GPL-2.0-only OR CDDL-1.0) AND (GPL-2.0-only OR GFDL-1.1-no-invariants-or-later) AND (GPL-2.0-only OR GFDL-1.2-no-invariants-only) AND (GPL-2.0-only OR GFDL-1.2-no-invariants-or-later) AND (GPL-2.0-only WITH Linux-syscall-note) AND GPL-2.0-or-later AND (GPL-2.0-or-later OR BSD-2-Clause) AND (GPL-2.0-or-later OR BSD-3-Clause) AND (GPL-2.0-or-later OR CC-BY-4.0) AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (GPL-2.0-or-later WITH Linux-syscall-note) AND ISC AND LGPL-2.0-or-later AND (LGPL-2.0-or-later OR BSD-2-Clause) AND (LGPL-2.0-or-later WITH Linux-syscall-note) AND LGPL-2.1-only AND (LGPL-2.1-only OR BSD-2-Clause) AND (LGPL-2.1-only WITH Linux-syscall-note) AND LGPL-2.1-or-later AND (LGPL-2.1-or-later WITH Linux-syscall-note) AND (Linux-OpenIB OR GPL-2.0-only) AND (Linux-OpenIB OR GPL-2.0-only OR BSD-2-Clause) AND Linux-man-pages-copyleft AND MIT AND (MIT OR Apache-2.0) AND (MIT OR GPL-2.0-only) AND (MIT OR GPL-2.0-or-later) AND (MIT OR LGPL-2.1-only) AND (MPL-1.1 OR GPL-2.0-only) AND (X11 OR GPL-2.0-only) AND (X11 OR GPL-2.0-or-later) AND Zlib AND (copyleft-next-0.3.1 OR GPL-2.0-or-later)
URL: https://www.kernel.org/
Version: %{specrpmversion}
Release: %{pkg_release}
# DO NOT CHANGE THE 'ExclusiveArch' LINE TO TEMPORARILY EXCLUDE AN ARCHITECTURE BUILD.
# SET %%nobuildarches (ABOVE) INSTEAD
%if 0%{?fedora}
ExclusiveArch: noarch x86_64 s390x aarch64 ppc64le riscv64
%else
ExclusiveArch: noarch i386 i686 x86_64 s390x aarch64 ppc64le riscv64
%endif
ExclusiveOS: Linux
%ifnarch %{nobuildarches}
Requires: %{name}-core-uname-r = %{KVERREL}
Requires: %{name}-modules-uname-r = %{KVERREL}
Requires: %{name}-modules-core-uname-r = %{KVERREL}
Requires: ((%{name}-modules-extra-uname-r = %{KVERREL}) if %{name}-modules-extra-matched)
Provides: installonlypkg(kernel)
%endif


#
# List the packages used during the kernel build
#
BuildRequires: kmod, bash, coreutils, tar, git-core, which
BuildRequires: bzip2, xz, findutils, m4, perl-interpreter, perl-Carp, perl-devel, perl-generators, make, diffutils, gawk, %compression
# Kernel EFI/Compression set by CONFIG_KERNEL_ZSTD
%ifarch x86_64 aarch64 riscv64
BuildRequires: zstd
%endif
BuildRequires: gcc, binutils, redhat-rpm-config, hmaccalc, bison, flex, gcc-c++
BuildRequires: rust, rust-src, bindgen, rustfmt, clippy
BuildRequires: net-tools, hostname, bc, elfutils-devel
BuildRequires: dwarves
BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-pyyaml
BuildRequires: kernel-rpm-macros
# glibc-static is required for a consistent build environment (specifically
# CONFIG_CC_CAN_LINK_STATIC=y).
BuildRequires: glibc-static
%if %{with_headers} || %{with_cross_headers}
BuildRequires: rsync
%endif
%if %{with_doc}
BuildRequires: xmlto, asciidoc, python3-sphinx, python3-sphinx_rtd_theme
%endif
%if %{with_sparse}
BuildRequires: sparse
%endif
%if %{with_perf}
BuildRequires: zlib-devel binutils-devel newt-devel perl(ExtUtils::Embed) bison flex xz-devel
BuildRequires: audit-libs-devel python3-setuptools
BuildRequires: capstone-devel
BuildRequires: elfutils-debuginfod-client-devel
BuildRequires: java-devel
BuildRequires: libbabeltrace-devel
BuildRequires: libpfm-devel
BuildRequires: libtraceevent-devel
%ifnarch s390x
BuildRequires: numactl-devel
%endif
%ifarch aarch64
BuildRequires: opencsd-devel >= 1.0.0
%endif
%endif
%if %{with_tools}
BuildRequires: python3-docutils
BuildRequires: gettext ncurses-devel
BuildRequires: libcap-devel libcap-ng-devel
# The following are rtla requirements
BuildRequires: python3-docutils
BuildRequires: libtraceevent-devel
BuildRequires: libtracefs-devel
BuildRequires: libbpf-devel
BuildRequires: bpftool
BuildRequires: clang

%ifarch %{cpupowerarchs}
# For libcpupower bindings
BuildRequires: swig
%endif

%ifnarch s390x
BuildRequires: pciutils-devel
%endif
%ifarch i686 x86_64
BuildRequires: libnl3-devel
%endif
%endif

%if %{with_tools} && %{with_ynl}
BuildRequires: python3-pyyaml python3-jsonschema python3-pip python3-setuptools >= 61
BuildRequires: (python3-wheel if python3-setuptools < 70)
%endif

BuildRequires: openssl-devel

%if %{with_selftests}
BuildRequires: clang llvm-devel fuse-devel zlib-devel binutils-devel python3-docutils python3-jsonschema
%ifarch x86_64 riscv64
BuildRequires: lld
%endif
BuildRequires: libasan-static
BuildRequires: libcap-devel libcap-ng-devel rsync libmnl-devel libxml2-devel
BuildRequires: liburing-devel
BuildRequires: libubsan
BuildRequires: numactl-devel
BuildRequires: xxd
%endif
BuildConflicts: rhbuildsys(DiskFree) < 500Mb
%if %{with_debuginfo}
BuildRequires: rpm-build, elfutils
BuildConflicts: rpm < 4.13.0.1-19
BuildConflicts: dwarves < 1.13
# Most of these should be enabled after more investigation
%undefine _include_minidebuginfo
%undefine _find_debuginfo_dwz_opts
%undefine _unique_build_ids
%undefine _unique_debug_names
%undefine _unique_debug_srcs
%undefine _debugsource_packages
%undefine _debuginfo_subpackages

# Remove -q option below to provide 'extracting debug info' messages
%global _find_debuginfo_opts -r -q

%global _missing_build_ids_terminate_build 1
%global _no_recompute_build_ids 1
%endif
%if %{with_kabidwchk} || %{with_kabidw_base}
BuildRequires: kabi-dw
%endif

%if %{signkernel}%{signmodules}
BuildRequires: openssl
%if %{signkernel}
# ELN uses Fedora signing process, so exclude
%if 0%{?rhel}%{?centos} && !0%{?eln}
BuildRequires: system-sb-certs
%endif
%ifarch x86_64 aarch64 riscv64
BuildRequires: nss-tools
BuildRequires: pesign >= 0.10-4
%endif
%endif
%endif

%if %{with_cross}
BuildRequires: binutils-%{_build_arch}-linux-gnu, gcc-%{_build_arch}-linux-gnu
%define cross_opts CROSS_COMPILE=%{_build_arch}-linux-gnu-
%define __strip %{_build_arch}-linux-gnu-strip

%if 0%{?fedora} && 0%{?fedora} <= 41
# Work around find-debuginfo for cross builds.
# find-debuginfo doesn't support any of CROSS options (RHEL-21797),
# and since debugedit > 5.0-16.el10, or since commit
#   dfe1f7ff30f4 ("find-debuginfo.sh: Exit with real exit status in parallel jobs")
# it now aborts on failure and build fails.
# debugedit-5.1-5 in F42 added support to override tools with target versions.
%undefine _include_gdb_index
%endif

%if 0%{?rhel}%{?centos}
%ifarch riscv64
# Temporary workaround to avoid using find-debuginfo and gdb.minimal.
# The current c10s version of gdb-minimal (14.2-4.el10) crashes when given some
# riscv64 kernel modules (see RHEL-91586). Not building the gdb index avoids
# breaking CI for now.
%undefine _include_gdb_index
%endif
%endif
%endif

# These below are required to build man pages
%if %{with_perf}
BuildRequires: xmlto
%endif
%if %{with_perf} || %{with_tools}
BuildRequires: asciidoc
%endif

%if %{with toolchain_clang}
BuildRequires: clang
%endif

%if %{with clang_lto}
BuildRequires: llvm
BuildRequires: lld
%endif

%if %{with_efiuki}
BuildRequires: dracut
# For dracut UEFI uki binaries
BuildRequires: binutils
# For the initrd
BuildRequires: lvm2
BuildRequires: systemd-boot-unsigned
# For systemd-stub and systemd-pcrphase
BuildRequires: systemd-udev >= 252-1
# For systemd-repart
BuildRequires: xfsprogs e2fsprogs dosfstools
# For UKI kernel cmdline addons
BuildRequires: systemd-ukify
# For TPM operations in UKI initramfs
BuildRequires: tpm2-tools
# For UKI sb cert
%if 0%{?rhel}%{?centos} && !0%{?eln}
%if 0%{?centos}
BuildRequires: centos-sb-certs >= 9.0-23
%else
BuildRequires: redhat-sb-certs >= 9.4-0.1
%endif
%endif
%endif

# Because this is the kernel, it's hard to get a single upstream URL
# to represent the base without needing to do a bunch of patching. This
# tarball is generated from a src-git tree. If you want to see the
# exact git commit you can run
#
# xzcat -qq ${TARBALL} | git get-tar-commit-id
Source0: kernel-%{specrpmversion}.%{kextraversion}.tar.gz

Source1: Makefile.rhelver
Source2: %{package_name}.changelog

Source10: redhatsecurebootca5.cer
Source13: redhatsecureboot501.cer

%if %{signkernel}
# Name of the packaged file containing signing key
%ifarch ppc64le
%define signing_key_filename kernel-signing-ppc.cer
%endif
%ifarch s390x
%define signing_key_filename kernel-signing-s390.cer
%endif

# Fedora/ELN pesign macro expects to see these cert file names, see:
# https://github.com/rhboot/pesign/blob/main/src/pesign-rpmbuild-helper.in#L216
%if 0%{?fedora}%{?eln}
%define pesign_name_0 redhatsecureboot501
%define secureboot_ca_0 %{SOURCE10}
%define secureboot_key_0 %{SOURCE13}
%endif

# RHEL/centos certs come from system-sb-certs
%if 0%{?rhel} && !0%{?eln}
%define secureboot_ca_0 %{_datadir}/pki/sb-certs/secureboot-ca-%{_arch}.cer
%define secureboot_key_0 %{_datadir}/pki/sb-certs/secureboot-kernel-%{_arch}.cer

%if 0%{?centos}
%define pesign_name_0 centossecureboot201
%else
%ifarch x86_64 aarch64
%define pesign_name_0 redhatsecureboot501
%endif
%ifarch s390x
%define pesign_name_0 redhatsecureboot302
%endif
%ifarch ppc64le
%define pesign_name_0 redhatsecureboot701
%endif
%endif
# rhel && !eln
%endif

# signkernel
%endif

Source20: mod-denylist.sh
Source21: mod-sign.sh
Source22: filtermods.py

%define modsign_cmd %{SOURCE21}

%if 0%{?include_rhel}
Source24: %{name}-aarch64-rhel.config
Source25: %{name}-aarch64-debug-rhel.config
Source27: %{name}-ppc64le-rhel.config
Source28: %{name}-ppc64le-debug-rhel.config
Source29: %{name}-s390x-rhel.config
Source30: %{name}-s390x-debug-rhel.config
Source31: %{name}-s390x-zfcpdump-rhel.config
Source32: %{name}-x86_64-rhel.config
Source33: %{name}-x86_64-debug-rhel.config
# ARM64 64K page-size kernel config
Source42: %{name}-aarch64-64k-rhel.config
Source43: %{name}-aarch64-64k-debug-rhel.config

Source44: %{name}-riscv64-rhel.config
Source45: %{name}-riscv64-debug-rhel.config
%endif

%if %{include_rhel} || %{include_automotive}
Source23: x509.genkey.rhel
Source34: def_variants.yaml.rhel
Source41: x509.genkey.centos
%endif

%if 0%{?include_fedora}
Source50: x509.genkey.fedora

Source52: %{name}-aarch64-fedora.config
Source53: %{name}-aarch64-debug-fedora.config
Source54: %{name}-aarch64-16k-fedora.config
Source55: %{name}-aarch64-16k-debug-fedora.config
Source56: %{name}-ppc64le-fedora.config
Source57: %{name}-ppc64le-debug-fedora.config
Source58: %{name}-s390x-fedora.config
Source59: %{name}-s390x-debug-fedora.config
Source60: %{name}-x86_64-fedora.config
Source61: %{name}-x86_64-debug-fedora.config
Source700: %{name}-riscv64-fedora.config
Source701: %{name}-riscv64-debug-fedora.config

Source62: def_variants.yaml.fedora
%endif

Source70: partial-kgcov-snip.config
Source71: partial-kgcov-debug-snip.config
Source72: partial-clang-snip.config
Source73: partial-clang-debug-snip.config
Source74: partial-clang_lto-x86_64-snip.config
Source75: partial-clang_lto-x86_64-debug-snip.config
Source76: partial-clang_lto-aarch64-snip.config
Source77: partial-clang_lto-aarch64-debug-snip.config
Source80: generate_all_configs.sh
Source81: process_configs.sh

Source83: uki.sbat.template
Source84: uki-addons.sbat.template
Source85: kernel.sbat.template

Source86: dracut-virt.conf

Source87: flavors

Source151: uki_create_addons.py
Source152: uki_addons.json

Source100: rheldup3.x509
Source101: rhelkpatch1.x509
Source102: nvidiagpuoot001.x509
Source103: rhelimaca1.x509
Source104: rhelima.x509
Source105: rhelima_centos.x509
Source106: fedoraimaca.x509

%if 0%{?fedora}%{?eln}
%define ima_ca_cert %{SOURCE106}
%endif

%if 0%{?rhel} && !0%{?eln}
%define ima_ca_cert %{SOURCE103}
# rhel && !eln
%endif

%if 0%{?centos}
%define ima_signing_cert %{SOURCE105}
%else
%define ima_signing_cert %{SOURCE104}
%endif

%define ima_cert_name ima.cer

Source200: check-kabi

Source201: Module.kabi_aarch64
Source202: Module.kabi_ppc64le
Source203: Module.kabi_s390x
Source204: Module.kabi_x86_64
Source205: Module.kabi_riscv64

Source210: Module.kabi_dup_aarch64
Source211: Module.kabi_dup_ppc64le
Source212: Module.kabi_dup_s390x
Source213: Module.kabi_dup_x86_64
Source214: Module.kabi_dup_riscv64

Source300: kernel-abi-stablelists-%{kabiversion}.tar.xz
Source301: kernel-kabi-dw-%{kabiversion}.tar.xz

%if 0%{include_rt}
%if 0%{include_rhel}
Source474: %{name}-aarch64-rt-rhel.config
Source475: %{name}-aarch64-rt-debug-rhel.config
Source476: %{name}-aarch64-rt-64k-rhel.config
Source477: %{name}-aarch64-rt-64k-debug-rhel.config
Source478: %{name}-x86_64-rt-rhel.config
Source479: %{name}-x86_64-rt-debug-rhel.config
%endif
%if 0%{include_fedora}
Source480: %{name}-aarch64-rt-fedora.config
Source481: %{name}-aarch64-rt-debug-fedora.config
Source482: %{name}-aarch64-rt-64k-fedora.config
Source483: %{name}-aarch64-rt-64k-debug-fedora.config
Source484: %{name}-x86_64-rt-fedora.config
Source485: %{name}-x86_64-rt-debug-fedora.config
Source486: %{name}-riscv64-rt-fedora.config
Source487: %{name}-riscv64-rt-debug-fedora.config
%endif
%endif

%if %{include_automotive}
%if %{with_automotive_build}
Source488: %{name}-aarch64-rhel.config
Source489: %{name}-aarch64-debug-rhel.config
Source490: %{name}-x86_64-rhel.config
Source491: %{name}-x86_64-debug-rhel.config
%else
Source488: %{name}-aarch64-automotive-rhel.config
Source489: %{name}-aarch64-automotive-debug-rhel.config
Source490: %{name}-x86_64-automotive-rhel.config
Source491: %{name}-x86_64-automotive-debug-rhel.config
%endif
%endif


# Sources for kernel-tools
Source2002: kvm_stat.logrotate

# Some people enjoy building customized kernels from the dist-git in Fedora and
# use this to override configuration options. One day they may all use the
# source tree, but in the mean time we carry this to support the legacy workflow
Source3000: merge.py
Source3001: kernel-local
%if %{patchlist_changelog}
Source3002: Patchlist.changelog
%endif

Source4000: README.rst
Source4001: rpminspect.yaml
Source4002: gating.yaml
Source9999: kernel.azl.macros
Source5000: 6.18-x86_64-azl.config
Source5001: 6.18-aarch64-azl.config
Source5002: azurelinux-ca-20230216.pem

## Patches needed for building this package

%if !%{nopatches}

# Patch1: patch-%{patchversion}-redhat.patch (disabled for AzureLinux)
%endif

# empty final patch to facilitate testing of kernel patches
Patch999999: linux-kernel-test.patch

# END OF PATCH DEFINITIONS

%description
The %{package_name} meta package

# This macro does requires, provides, conflicts, obsoletes for a kernel package.
#	%%kernel_reqprovconf [-o] <subpackage>
# It uses any kernel_<subpackage>_conflicts and kernel_<subpackage>_obsoletes
# macros defined above.
# -o: Skips main "Provides" that would satisfy general kernel requirements that
#     special-purpose kernels shouldn't include.
#     For example, used for zfcpdump-core to *not* provide kernel-core. (BZ 2027654)
#
%define kernel_reqprovconf(o) \
%if %{-o:0}%{!-o:1}\
Provides: kernel = %{specversion}-%{pkg_release}\
Provides: %{name} = %{specversion}-%{pkg_release}\
%endif\
Provides: %{name}-%{_target_cpu} = %{specrpmversion}-%{pkg_release}%{uname_suffix %{?1}}\
Provides: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): %{initrd_prereq}\
Requires(pre): ((linux-firmware >= 20150904-56.git6ebf5d57) if linux-firmware)\
Recommends: linux-firmware\
Requires(preun): systemd >= 200\
Conflicts: xfsprogs < 4.3.0-1\
Conflicts: xorg-x11-drv-vmmouse < 13.0.99\
%{expand:%%{?kernel%{?1:_%{1}}_conflicts:Conflicts: %%{kernel%{?1:_%{1}}_conflicts}}}\
%{expand:%%{?kernel%{?1:_%{1}}_obsoletes:Obsoletes: %%{kernel%{?1:_%{1}}_obsoletes}}}\
%{expand:%%{?kernel%{?1:_%{1}}_provides:Provides: %%{kernel%{?1:_%{1}}_provides}}}\
# We can't let RPM do the dependencies automatic because it'll then pick up\
# a correct but undesirable perl dependency from the module headers which\
# isn't required for the kernel proper to function\
AutoReq: no\
AutoProv: yes\
%{nil}


%package doc
Summary: Various documentation bits found in the kernel source
Group: Documentation
%description doc
This package contains documentation files from the kernel
source. Various bits of information about the Linux kernel and the
device drivers shipped with it are documented in these files.

You'll want to install this package if you need a reference to the
options that can be passed to Linux kernel modules at load time.

%if %{with_headers}
%package headers
Summary: Header files for the Linux kernel for use by glibc
Obsoletes: glibc-kernheaders < 3.0-46
Provides: glibc-kernheaders = 3.0-46
%if 0%{?gemini}
Provides: %{name}-headers = %{specversion}-%{release}
Obsoletes: kernel-headers < %{specversion}
%endif
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.
%endif

%if %{with_cross_headers}
%package cross-headers
Summary: Header files for the Linux kernel for use by cross-glibc
%if 0%{?gemini}
Provides: %{name}-cross-headers = %{specversion}-%{release}
Obsoletes: kernel-cross-headers < %{specversion}
%endif
%description cross-headers
Kernel-cross-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
cross-glibc package.
%endif

%package debuginfo-common-%{_target_cpu}
Summary: Kernel source files used by %{name}-debuginfo packages
Provides: installonlypkg(kernel)
%description debuginfo-common-%{_target_cpu}
This package is required by %{name}-debuginfo subpackages.
It provides the kernel source files common to all builds.

%if %{with_perf}
%package -n perf
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Performance monitoring for the Linux kernel
Requires: bzip2
%description -n perf
This package contains the perf tool, which enables performance monitoring
of the Linux kernel.

%package -n perf-debuginfo
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Debug information for package perf
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{specrpmversion}-%{release}
AutoReqProv: no
%description -n perf-debuginfo
This package provides debug information for the perf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_bindir}/perf(\.debug)?|.*%%{_libexecdir}/perf-core/.*|.*%%{_libdir}/libperf-jvmti.so(\.debug)?|XXX' -o perf-debuginfo.list}

%package -n python3-perf
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Python bindings for apps which will manipulate perf events
%description -n python3-perf
The python3-perf package contains a module that permits applications
written in the Python programming language to use the interface
to manipulate perf events.

%package -n python3-perf-debuginfo
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Debug information for package perf python bindings
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{specrpmversion}-%{release}
AutoReqProv: no
%description -n python3-perf-debuginfo
This package provides debug information for the perf python bindings.

# the python_sitearch macro should already be defined from above
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{python3_sitearch}/perf.*so(\.debug)?|XXX' -o python3-perf-debuginfo.list}

# with_perf
%endif

%if %{with_libperf}
%package -n libperf
Summary: The perf library from kernel source
%description -n libperf
This package contains the kernel source perf library.

%package -n libperf-devel
Summary: Developement files for the perf library from kernel source
Requires: libperf = %{version}-%{release}
%description -n libperf-devel
This package includes libraries and header files needed for development
of applications which use perf library from kernel source.

%package -n libperf-debuginfo
Summary: Debug information for package libperf
Group: Development/Debug
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n libperf-debuginfo
This package provides debug information for the libperf package.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_libdir}/libperf.so.*(\.debug)?|XXX' -o libperf-debuginfo.list}
# with_libperf
%endif

%if %{with_tools}
%package -n %{package_name}-tools
Summary: Assortment of tools for the Linux kernel
%ifarch %{cpupowerarchs}
Provides:  cpupowerutils = 1:009-0.6.p1
Obsoletes: cpupowerutils < 1:009-0.6.p1
Provides:  cpufreq-utils = 1:009-0.6.p1
Provides:  cpufrequtils = 1:009-0.6.p1
Obsoletes: cpufreq-utils < 1:009-0.6.p1
Obsoletes: cpufrequtils < 1:009-0.6.p1
Obsoletes: cpuspeed < 1:1.5-16
Requires: %{package_name}-tools-libs = %{specrpmversion}-%{release}
%endif
%define __requires_exclude ^%{_bindir}/python
%description -n %{package_name}-tools
This package contains the tools/ directory from the kernel source
and the supporting documentation.

%package -n %{package_name}-tools-libs
Summary: Libraries for the kernels-tools
%description -n %{package_name}-tools-libs
This package contains the libraries built from the tools/ directory
from the kernel source.

%package -n %{package_name}-tools-libs-devel
Summary: Assortment of tools for the Linux kernel
Requires: %{package_name}-tools = %{version}-%{release}
%ifarch %{cpupowerarchs}
Provides:  cpupowerutils-devel = 1:009-0.6.p1
Obsoletes: cpupowerutils-devel < 1:009-0.6.p1
%endif
Requires: %{package_name}-tools-libs = %{version}-%{release}
Provides: %{package_name}-tools-devel
%description -n %{package_name}-tools-libs-devel
This package contains the development files for the tools/ directory from
the kernel source.

%package -n %{package_name}-tools-debuginfo
Summary: Debug information for package %{package_name}-tools
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{version}-%{release}
AutoReqProv: no
%description -n %{package_name}-tools-debuginfo
This package provides debug information for package %{package_name}-tools.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_bindir}/bootconfig(\.debug)?|.*%%{_bindir}/centrino-decode(\.debug)?|.*%%{_bindir}/powernow-k8-decode(\.debug)?|.*%%{_bindir}/cpupower(\.debug)?|.*%%{_libdir}/libcpupower.*|.*%%{python3_sitearch}/_raw_pylibcpupower.*|.*%%{_bindir}/turbostat(\.debug)?|.*%%{_bindir}/x86_energy_perf_policy(\.debug)?|.*%%{_bindir}/tmon(\.debug)?|.*%%{_bindir}/lsgpio(\.debug)?|.*%%{_bindir}/gpio-hammer(\.debug)?|.*%%{_bindir}/gpio-event-mon(\.debug)?|.*%%{_bindir}/gpio-watch(\.debug)?|.*%%{_bindir}/iio_event_monitor(\.debug)?|.*%%{_bindir}/iio_generic_buffer(\.debug)?|.*%%{_bindir}/lsiio(\.debug)?|.*%%{_bindir}/intel-speed-select(\.debug)?|.*%%{_bindir}/page_owner_sort(\.debug)?|.*%%{_bindir}/slabinfo(\.debug)?|.*%%{_sbindir}/intel_sdsi(\.debug)?|XXX' -o %{package_name}-tools-debuginfo.list}

%package -n rtla
%if 0%{gemini}
Epoch: %{gemini}
%endif
Summary: Real-Time Linux Analysis tools
Requires: libtraceevent
Requires: libtracefs
Requires: libbpf
%ifarch %{cpupowerarchs}
Requires: %{package_name}-tools-libs = %{version}-%{release}
%endif
%description -n rtla
The rtla meta-tool includes a set of commands that aims to analyze
the real-time properties of Linux. Instead of testing Linux as a black box,
rtla leverages kernel tracing capabilities to provide precise information
about the properties and root causes of unexpected results.

%package -n rv
Summary: RV: Runtime Verification
%description -n rv
Runtime Verification (RV) is a lightweight (yet rigorous) method that
complements classical exhaustive verification techniques (such as model
checking and theorem proving) with a more practical approach for
complex systems.
The rv tool is the interface for a collection of monitors that aim
analysing the logical and timing behavior of Linux.

# with_tools
%endif

%if %{with_selftests}

%package selftests-internal
Summary: Kernel samples and selftests
Requires: binutils, bpftool, fuse-libs, iproute-tc, iputils, keyutils, nmap-ncat, python3
%description selftests-internal
Kernel sample programs and selftests.

# Note that this pattern only works right to match the .build-id
# symlinks because of the trailing nonmatching alternation and
# the leading .*, because of find-debuginfo.sh's buggy handling
# of matching the pattern against the symlinks file.
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} -p '.*%%{_libexecdir}/(ksamples|kselftests)/.*|XXX' -o selftests-debuginfo.list}

%define __requires_exclude ^liburandom_read.so.*$

# with_selftests
%endif

%define kernel_gcov_package() \
%package %{?1:%{1}-}gcov\
Summary: gcov graph and source files for coverage data collection.\
%description %{?1:%{1}-}gcov\
%{?1:%{1}-}gcov includes the gcov graph and source files for gcov coverage collection.\
%{nil}

%if %{with_kernel_abi_stablelists}
%package -n %{package_name}-abi-stablelists
Summary: The Red Hat Enterprise Linux kernel ABI symbol stablelists
AutoReqProv: no
%description -n %{package_name}-abi-stablelists
The kABI package contains information pertaining to the Red Hat Enterprise
Linux kernel ABI, including lists of kernel symbols that are needed by
external Linux kernel modules, and a yum plugin to aid enforcement.
%endif

%if %{with_kabidw_base}
%package kernel-kabidw-base-internal
Summary: The baseline dataset for kABI verification using DWARF data
Group: System Environment/Kernel
AutoReqProv: no
%description kernel-kabidw-base-internal
The package contains data describing the current ABI of the Red Hat Enterprise
Linux kernel, suitable for the kabi-dw tool.
%endif

#
# This macro creates a kernel-<subpackage>-debuginfo package.
#	%%kernel_debuginfo_package <subpackage>
#
# Explanation of the find_debuginfo_opts: We build multiple kernels (debug,
# rt, 64k etc.) so the regex filters those kernels appropriately. We also
# have to package several binaries as part of kernel-devel but getting
# unique build-ids is tricky for these userspace binaries. We don't really
# care about debugging those so we just filter those out and remove it.
%define kernel_debuginfo_package() \
%package %{?1:%{1}-}debuginfo\
Summary: Debug information for package %{name}%{?1:-%{1}}\
Requires: %{name}-debuginfo-common-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-debuginfo-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
%description %{?1:%{1}-}debuginfo\
This package provides debug information for package %{name}%{?1:-%{1}}.\
This is required to use SystemTap with %{name}%{?1:-%{1}}-%{KVERREL}.\
%{expand:%%global _find_debuginfo_opts %{?_find_debuginfo_opts} --keep-section '.BTF' -p '.*\/usr\/src\/kernels/.*|XXX' -o ignored-debuginfo.list -p '/.*/%%{KVERREL_RE}%{?1:[+]%{1}}/.*|/.*%%{KVERREL_RE}%{?1:\+%{1}}(\.debug)?' -o debuginfo%{?1}.list}\
%{nil}

#
# This macro creates a kernel-<subpackage>-devel package.
#	%%kernel_devel_package [-m] <subpackage> <pretty-name>
#
%define kernel_devel_package(m) \
%package %{?1:%{1}-}devel\
Summary: Development package for building kernel modules to match the %{?2:%{2} }kernel\
Provides: %{name}%{?1:-%{1}}-devel-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}-devel-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: kernel-devel-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Provides: %{name}-devel-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel)\
AutoReqProv: no\
Requires(pre): findutils\
Requires: findutils\
Requires: perl-interpreter\
Requires: openssl-devel\
Requires: elfutils-libelf-devel\
Requires: bison\
Requires: flex\
Requires: make\
Requires: gcc\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-devel-uname-r = %{KVERREL}%{uname_variant %{?1}}\
%endif\
%description %{?1:%{1}-}devel\
This package provides kernel headers and makefiles sufficient to build modules\
against the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates an empty kernel-<subpackage>-devel-matched package that
# requires both the core and devel packages locked on the same version.
#	%%kernel_devel_matched_package [-m] <subpackage> <pretty-name>
#
%define kernel_devel_matched_package(m) \
%package %{?1:%{1}-}devel-matched\
Summary: Meta package to install matching core and devel packages for a given %{?2:%{2} }kernel\
Requires: %{package_name}%{?1:-%{1}}-devel = %{specrpmversion}-%{release}\
Requires: %{package_name}%{?1:-%{1}}-core = %{specrpmversion}-%{release}\
%description %{?1:%{1}-}devel-matched\
This meta package is used to install matching core and devel packages for a given %{?2:%{2} }kernel.\
%{nil}

%define kernel_modules_extra_matched_package(m) \
%package modules-extra-matched\
Summary: Meta package which requires modules-extra to be installed for all kernels.\
%description modules-extra-matched\
This meta package provides a single reference that other packages can Require to have modules-extra installed for all kernels.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-internal package.
#	%%kernel_modules_internal_package <subpackage> <pretty-name>
#
%define kernel_modules_internal_package() \
%package %{?1:%{1}-}modules-internal\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: %{name}%{?1:-%{1}}-modules-internal-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-modules-internal-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}%{?1:-%{1}}-modules-internal = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-internal-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-internal\
This package provides kernel modules for the %{?2:%{2} }kernel package for Red Hat internal usage.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-extra package.
#	%%kernel_modules_extra_package [-m] <subpackage> <pretty-name>
#
%define kernel_modules_extra_package(m) \
%package %{?1:%{1}-}modules-extra\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Provides: %{name}%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-modules-extra-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}%{?1:-%{1}}-modules-extra = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-extra-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-modules-extra-uname-r = %{KVERREL}%{uname_variant %{?1}}\
%endif\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-extra\
This package provides less commonly used kernel modules for the %{?2:%{2} }kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules package.
#	%%kernel_modules_package [-m] <subpackage> <pretty-name>
#
%define kernel_modules_package(m) \
%package %{?1:%{1}-}modules\
Summary: kernel modules to match the %{?2:%{2}-}core kernel\
Provides: %{name}%{?1:-%{1}}-modules-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}-modules-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}-modules = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-modules-uname-r = %{KVERREL}%{uname_variant %{?1}}\
%endif\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules\
This package provides commonly used kernel modules for the %{?2:%{2}-}core kernel package.\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-core package.
#	%%kernel_modules_core_package [-m] <subpackage> <pretty-name>
#
%define kernel_modules_core_package(m) \
%package %{?1:%{1}-}modules-core\
Summary: Core kernel modules to match the %{?2:%{2}-}core kernel\
Provides: %{name}%{?1:-%{1}}-modules-core-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}-modules-core-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}-modules-core = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-modules-core-uname-r = %{KVERREL}%{uname_variant %{?1}}\
%endif\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-core\
This package provides essential kernel modules for the %{?2:%{2}-}core kernel package.\
%{nil}

#
# this macro creates a kernel-<subpackage> meta package.
#	%%kernel_meta_package <subpackage>
#
%define kernel_meta_package() \
%package %{1}\
summary: kernel meta-package for the %{1} kernel\
Requires: %{name}-%{1}-core-uname-r = %{KVERREL}%{uname_suffix %{1}}\
Requires: %{name}-%{1}-modules-uname-r = %{KVERREL}%{uname_suffix %{1}}\
Requires: %{name}-%{1}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{1}}\
Requires: ((%{name}-%{1}-modules-extra-uname-r = %{KVERREL}%{uname_suffix %{1}}) if %{name}-modules-extra-matched)\
%if "%{1}" == "rt" || "%{1}" == "rt-debug" || "%{1}" == "rt-64k" || "%{1}" == "rt-64k-debug"\
Requires: realtime-setup\
%endif\
Provides: installonlypkg(kernel)\
%description %{1}\
The meta-package for the %{1} kernel\
%{nil}

#
# This macro creates a kernel-<subpackage> and its -devel and -debuginfo too.
#	%%define variant_summary The Linux kernel compiled for <configuration>
#	%%kernel_variant_package [-n <pretty-name>] [-m] [-o] <subpackage>
# -m: Used with debugbuildsenabled==0 to create a "meta" debug variant that
#     depends on base variant and skips debug/internal/partner packages.
# -o: Skips main "Provides" that would satisfy general kernel requirements that
#     special-purpose kernels shouldn't include.
#
%define kernel_variant_package(n:mo) \
%package %{?1:%{1}-}core\
Summary: %{variant_summary}\
Provides: %{name}-%{?1:%{1}-}core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel)\
%if %{-m:1}%{!-m:0}\
Requires: %{name}-core-uname-r = %{KVERREL}%{uname_variant %{?1}}\
Requires: %{name}-%{?1:%{1}-}-modules-core-uname-r = %{KVERREL}%{uname_variant %{?1}}\
%endif\
%{expand:%%kernel_reqprovconf %{?1:%{1}} %{-o:%{-o}}}\
%if %{?1:1} %{!?1:0} \
%{expand:%%kernel_meta_package %{?1:%{1}}}\
%endif\
%{expand:%%kernel_devel_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_devel_matched_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_modules_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_modules_core_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%{expand:%%kernel_modules_extra_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}} %{-m:%{-m}}}\
%if %{-m:0}%{!-m:1}\
%{expand:%%kernel_modules_internal_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%if 0%{!?fedora:1}\
%{expand:%%kernel_modules_partner_package %{?1:%{1}} %{!?{-n}:%{1}}%{?{-n}:%{-n*}}}\
%endif\
%{expand:%%kernel_debuginfo_package %{?1:%{1}}}\
%endif\
%if %{with_efiuki} && ("%{1}" != "rt" && "%{1}" != "rt-debug" && "%{1}" != "rt-64k" && "%{1}" != "rt-64k-debug")\
%package %{?1:%{1}-}uki-virt\
Summary: %{variant_summary} unified kernel image for virtual machines\
Provides: installonlypkg(kernel)\
Provides: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires(pre): %{kernel_prereq}\
Requires(pre): systemd >= 254-1\
Recommends: uki-direct\
%package %{?1:%{1}-}uki-virt-addons\
Summary: %{variant_summary} unified kernel image addons for virtual machines\
Provides: installonlypkg(kernel)\
Requires: %{name}%{?1:-%{1}}-uki-virt = %{specrpmversion}-%{release}\
Requires(pre): systemd >= 254-1\
%endif\
%if %{with_gcov}\
%{expand:%%kernel_gcov_package %{?1:%{1}}}\
%endif\
%{nil}

#
# This macro creates a kernel-<subpackage>-modules-partner package.
#	%%kernel_modules_partner_package <subpackage> <pretty-name>
#
%define kernel_modules_partner_package() \
%package %{?1:%{1}-}modules-partner\
Summary: Extra kernel modules to match the %{?2:%{2} }kernel\
Group: System Environment/Kernel\
Provides: %{name}%{?1:-%{1}}-modules-partner-%{_target_cpu} = %{specrpmversion}-%{release}\
Provides: %{name}%{?1:-%{1}}-modules-partner-%{_target_cpu} = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: %{name}%{?1:-%{1}}-modules-partner = %{specrpmversion}-%{release}%{uname_suffix %{?1}}\
Provides: installonlypkg(kernel-module)\
Provides: %{name}%{?1:-%{1}}-modules-partner-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
Requires: %{name}%{?1:-%{1}}-modules-core-uname-r = %{KVERREL}%{uname_suffix %{?1}}\
AutoReq: no\
AutoProv: yes\
%description %{?1:%{1}-}modules-partner\
This package provides kernel modules for the %{?2:%{2} }kernel package for Red Hat partners usage.\
%{nil}

# Now, each variant package.
%if %{with_zfcpdump}
%define variant_summary The Linux kernel compiled for zfcpdump usage
%kernel_variant_package -o zfcpdump
%description zfcpdump-core
The kernel package contains the Linux kernel (vmlinuz) for use by the
zfcpdump infrastructure.
# with_zfcpdump
%endif

%if %{with_arm64_16k_base}
%define variant_summary The Linux kernel compiled for 16k pagesize usage
%kernel_variant_package 16k
%description 16k-core
The kernel package contains a variant of the ARM64 Linux kernel using
a 16K page size.
%endif

%if %{with_arm64_16k} && %{with_debug}
%define variant_summary The Linux kernel compiled with extra debugging enabled
%if !%{debugbuildsenabled}
%kernel_variant_package -m 16k-debug
%else
%kernel_variant_package 16k-debug
%endif
%description 16k-debug-core
The debug kernel package contains a variant of the ARM64 Linux kernel using
a 16K page size.
This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_arm64_64k_base}
%define variant_summary The Linux kernel compiled for 64k pagesize usage
%kernel_variant_package 64k
%description 64k-core
The kernel package contains a variant of the ARM64 Linux kernel using
a 64K page size.
%endif

%if %{with_arm64_64k} && %{with_debug}
%define variant_summary The Linux kernel compiled with extra debugging enabled
%if !%{debugbuildsenabled}
%kernel_variant_package -m 64k-debug
%else
%kernel_variant_package 64k-debug
%endif
%description 64k-debug-core
The debug kernel package contains a variant of the ARM64 Linux kernel using
a 64K page size.
This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_debug} && %{with_realtime}
%define variant_summary The Linux PREEMPT_RT kernel compiled with extra debugging enabled
%kernel_variant_package rt-debug
%description rt-debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_realtime_base}
%define variant_summary The Linux kernel compiled with PREEMPT_RT enabled
%kernel_variant_package rt
%description rt-core
This package includes a version of the Linux kernel compiled with the
PREEMPT_RT real-time preemption support
%endif

%if %{with_realtime_arm64_64k_base}
%define variant_summary The Linux PREEMPT_RT kernel compiled for 64k pagesize usage
%kernel_variant_package rt-64k
%description rt-64k-core
The kernel package contains a variant of the ARM64 Linux PREEMPT_RT kernel using
a 64K page size.
%endif

%if %{with_realtime_arm64_64k} && %{with_debug}
%define variant_summary The Linux PREEMPT_RT kernel compiled with extra debugging enabled
%if !%{debugbuildsenabled}
%kernel_variant_package -m rt-64k-debug
%else
%kernel_variant_package rt-64k-debug
%endif
%description rt-64k-debug-core
The debug kernel package contains a variant of the ARM64 Linux PREEMPT_RT kernel using
a 64K page size.
This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_debug} && %{with_automotive} && !%{with_automotive_build}
%define variant_summary The Linux Automotive kernel compiled with extra debugging enabled
%kernel_variant_package automotive-debug
%description automotive-debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_automotive_base}
%define variant_summary The Linux kernel compiled with PREEMPT_RT enabled
%kernel_variant_package automotive
%description automotive-core
This package includes a version of the Linux kernel compiled with the
PREEMPT_RT real-time preemption support, targeted for Automotive platforms
%endif

%if %{with_up} && %{with_debug}
%if !%{debugbuildsenabled}
%kernel_variant_package -m debug
%else
%kernel_variant_package debug
%endif
%description debug-core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system:  memory allocation, process allocation, device
input and output, etc.

This variant of the kernel has numerous debugging options enabled.
It should only be installed when trying to gather additional information
on kernel bugs, as some of these options impact performance noticably.
%endif

%if %{with_up_base}
# And finally the main -core package

%define variant_summary The Linux kernel
%kernel_variant_package
%description core
The kernel package contains the Linux kernel (vmlinuz), the core of any
Linux operating system.  The kernel handles the basic functions
of the operating system: memory allocation, process allocation, device
input and output, etc.
%endif

%if %{with_up} && %{with_debug} && %{with_efiuki}
%description debug-uki-virt
Prebuilt debug unified kernel image for virtual machines.

%description debug-uki-virt-addons
Prebuilt debug unified kernel image addons for virtual machines.
%endif

%if %{with_up_base} && %{with_efiuki}
%description uki-virt
Prebuilt default unified kernel image for virtual machines.

%description uki-virt-addons
Prebuilt default unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_16k} && %{with_debug} && %{with_efiuki}
%description 16k-debug-uki-virt
Prebuilt 16k debug unified kernel image for virtual machines.

%description 16k-debug-uki-virt-addons
Prebuilt 16k debug unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_16k_base} && %{with_efiuki}
%description 16k-uki-virt
Prebuilt 16k unified kernel image for virtual machines.

%description 16k-uki-virt-addons
Prebuilt 16k unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_64k} && %{with_debug} && %{with_efiuki}
%description 64k-debug-uki-virt
Prebuilt 64k debug unified kernel image for virtual machines.

%description 64k-debug-uki-virt-addons
Prebuilt 64k debug unified kernel image addons for virtual machines.
%endif

%if %{with_arm64_64k_base} && %{with_efiuki}
%description 64k-uki-virt
Prebuilt 64k unified kernel image for virtual machines.

%description 64k-uki-virt-addons
Prebuilt 64k unified kernel image addons for virtual machines.
%endif

%ifnarch noarch %{nobuildarches}
%kernel_modules_extra_matched_package
%endif

%define log_msg() \
	{ set +x; } 2>/dev/null \
	_log_msglineno=$(grep -n %{*} %{_specdir}/${RPM_PACKAGE_NAME}.spec | grep log_msg | cut -d":" -f1) \
	echo "kernel.spec:${_log_msglineno}: %{*}" \
	set -x

%prep
%{log_msg "Start of prep stage"}

%{log_msg "Sanity checks"}

# do a few sanity-checks for --with *only builds
%if %{with_baseonly}
%if !%{with_up}
%{log_msg "Cannot build --with baseonly, up build is disabled"}
exit 1
%endif
%endif

%if %{with_automotive}
%if 0%{?fedora}
%{log_msg "Cannot build automotive with a fedora baseline, must be rhel/centos/eln"}
exit 1
%endif
%endif

# more sanity checking; do it quietly
if [ "%{patches}" != "%%{patches}" ] ; then
  for patch in %{patches} ; do
    if [ ! -f $patch ] ; then
	%{log_msg "ERROR: Patch  ${patch##/*/}  listed in specfile but is missing"}
      exit 1
    fi
  done
fi 2>/dev/null

patch_command='git --work-tree=. apply'
ApplyPatch()
{
  local patch=$1
  shift
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  if ! grep -E "^Patch[0-9]+: $patch\$" %{_specdir}/${RPM_PACKAGE_NAME}.spec ; then
    if [ "${patch:0:8}" != "patch-%{kversion}." ] ; then
	%{log_msg "ERROR: Patch  $patch  not listed as a source patch in specfile"}
      exit 1
    fi
  fi 2>/dev/null
  case "$patch" in
  *.bz2) bunzip2 < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.gz)  gunzip  < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *.xz)  unxz    < "$RPM_SOURCE_DIR/$patch" | $patch_command ${1+"$@"} ;;
  *) $patch_command ${1+"$@"} < "$RPM_SOURCE_DIR/$patch" ;;
  esac
}

# don't apply patch if it's empty
ApplyOptionalPatch()
{
  local patch=$1
  shift
  %{log_msg "ApplyOptionalPatch: $1"}
  if [ ! -f $RPM_SOURCE_DIR/$patch ]; then
    exit 1
  fi
  local C=$(wc -l $RPM_SOURCE_DIR/$patch | awk '{print $1}')
  if [ "$C" -gt 9 ]; then
    ApplyPatch $patch ${1+"$@"}
  fi
}

%{log_msg "Untar kernel tarball"}
%setup -q -n kernel-%{tarfile_release} -c
mv CBL-Mariner-Linux-Kernel-rolling-lts-mariner-%{azurelinux_version}-%{specrpmversion}.%{kextraversion} linux-%{KVERREL}

cd linux-%{KVERREL}
# cp -a %{SOURCE1} . (disabled for AzureLinux — Makefile.rhelver is Red Hat-specific)

%{log_msg "Start of patch applications"}
%if !%{nopatches}

# ApplyOptionalPatch patch-%{patchversion}-redhat.patch (disabled for AzureLinux)
%endif

ApplyOptionalPatch linux-kernel-test.patch

%{log_msg "End of patch applications"}
# END OF PATCH APPLICATIONS

# Any further pre-build tree manipulations happen here.
%{log_msg "Pre-build tree manipulations"}
chmod +x scripts/checkpatch.pl
mv COPYING COPYING-%{specrpmversion}-%{release}

# on linux-next prevent scripts/setlocalversion from mucking with our version numbers
rm -f localversion-next localversion-rt

# Mangle /usr/bin/python shebangs to /usr/bin/python3
# Mangle all Python shebangs to be Python 3 explicitly
# -p preserves timestamps
# -n prevents creating ~backup files
# -i specifies the interpreter for the shebang
# This fixes errors such as
# *** ERROR: ambiguous python shebang in /usr/bin/kvm_stat: #!/usr/bin/python. Change it to python3 (or python2) explicitly.
# We patch all sources below for which we got a report/error.
%{log_msg "Fixing Python shebangs..."}
%py3_shebang_fix \
	tools/kvm/kvm_stat/kvm_stat \
	scripts/show_delta \
	scripts/diffconfig \
	scripts/bloat-o-meter \
	scripts/jobserver-exec \
	tools \
	Documentation \
	scripts/clang-tools 2> /dev/null

# SBAT data
sed -e s,@KVER,%{KVERREL}, -e s,@SBAT_SUFFIX,%{sbat_suffix}, %{SOURCE83} > uki.sbat
sed -e s,@KVER,%{KVERREL}, -e s,@SBAT_SUFFIX,%{sbat_suffix}, %{SOURCE84} > uki-addons.sbat
sed -e s,@KVER,%{KVERREL}, -e s,@SBAT_SUFFIX,%{sbat_suffix}, %{SOURCE85} > kernel.sbat

# only deal with configs if we are going to build for the arch
%ifnarch %nobuildarches

if [ -L configs ]; then
	rm -f configs
fi
mkdir configs
cd configs

%{log_msg "Copy additional source files into buildroot"}
# Drop some necessary files from the source dir into the buildroot
cp $RPM_SOURCE_DIR/%{name}-*.config .
cp %{SOURCE80} .
# merge.py
cp %{SOURCE3000} .
# kernel-local - rename and copy for partial snippet config process
cp %{SOURCE3001} partial-kernel-local-snip.config
cp %{SOURCE3001} partial-kernel-local-debug-snip.config
FLAVOR=%{primary_target} SPECPACKAGE_NAME=%{name} SPECVERSION=%{specversion} SPECRPMVERSION=%{specrpmversion} ./generate_all_configs.sh %{debugbuildsenabled}

# Collect custom defined config options
%{log_msg "Collect custom defined config options"}
PARTIAL_CONFIGS=""
%if %{with_gcov}
PARTIAL_CONFIGS="$PARTIAL_CONFIGS %{SOURCE70} %{SOURCE71}"
%endif
%if %{with toolchain_clang}
PARTIAL_CONFIGS="$PARTIAL_CONFIGS %{SOURCE72} %{SOURCE73}"
%endif
%if %{with clang_lto}
PARTIAL_CONFIGS="$PARTIAL_CONFIGS %{SOURCE74} %{SOURCE75} %{SOURCE76} %{SOURCE77}"
%endif
PARTIAL_CONFIGS="$PARTIAL_CONFIGS partial-kernel-local-snip.config partial-kernel-local-debug-snip.config"

GetArch()
{
  case "$1" in
  *aarch64*) echo "aarch64" ;;
  *ppc64le*) echo "ppc64le" ;;
  *s390x*) echo "s390x" ;;
  *x86_64*) echo "x86_64" ;;
  *riscv64*) echo "riscv64" ;;
  # no arch, apply everywhere
  *) echo "" ;;
  esac
}

# Merge in any user-provided local config option changes
%{log_msg "Merge in any user-provided local config option changes"}
%ifnarch %nobuildarches
for i in %{all_configs}
do
  kern_arch="$(GetArch $i)"
  kern_debug="$(echo $i | grep -q debug && echo "debug" || echo "")"

  for j in $PARTIAL_CONFIGS
  do
    part_arch="$(GetArch $j)"
    part_debug="$(echo $j | grep -q debug && echo "debug" || echo "")"

    # empty arch means apply to all arches
    if [ "$part_arch" == "" -o "$part_arch" == "$kern_arch" ] && [ "$part_debug" == "$kern_debug" ]
    then
      mv $i $i.tmp
      ./merge.py $j $i.tmp > $i
    fi
  done
  rm -f $i.tmp
done
%endif

%if %{signkernel}%{signmodules}

# Add DUP and kpatch certificates to system trusted keys for RHEL
truncate -s0 ../certs/rhel.pem
%if 0%{?rhel}
%if %{rhelkeys}
%{log_msg "Add DUP and kpatch certificates to system trusted keys for RHEL"}
openssl x509 -inform der -in %{SOURCE100} -out rheldup3.pem
openssl x509 -inform der -in %{SOURCE101} -out rhelkpatch1.pem
openssl x509 -inform der -in %{SOURCE102} -out nvidiagpuoot001.pem
cat rheldup3.pem rhelkpatch1.pem nvidiagpuoot001.pem >> ../certs/rhel.pem
# rhelkeys
%endif
%if %{signkernel}
%ifarch s390x ppc64le
openssl x509 -inform der -in %{secureboot_ca_0} -out secureboot.pem
cat secureboot.pem >> ../certs/rhel.pem
%endif
%endif

# rhel
%endif

openssl x509 -inform der -in %{ima_ca_cert} -out imaca.pem
cat imaca.pem >> ../certs/rhel.pem

for i in *.config; do
  sed -i 's@CONFIG_SYSTEM_TRUSTED_KEYS=""@CONFIG_SYSTEM_TRUSTED_KEYS="certs/rhel.pem"@' $i
  sed -i 's@CONFIG_EFI_SBAT_FILE=""@CONFIG_EFI_SBAT_FILE="kernel.sbat"@' $i
done
%endif

%{log_msg "Set process_configs.sh $OPTS"}
cp %{SOURCE81} .
OPTS="-w -n -c"
%if !%{with_configchecks}
	OPTS="$OPTS -i"
%endif
%if %{with clang_lto}
for opt in %{clang_make_opts}; do
  OPTS="$OPTS -m $opt"
done
%endif
%{log_msg "Generate redhat configs"}
RHJOBS=$RPM_BUILD_NCPUS SPECPACKAGE_NAME=%{name} ./process_configs.sh $OPTS %{specrpmversion}

# We may want to override files from the primary target in case of building
# against a flavour of it (eg. centos not rhel), thus override it here if
# necessary
update_scripts() {
	TARGET="$1"

	for i in "$RPM_SOURCE_DIR"/*."$TARGET"; do
		NEW=${i%."$TARGET"}
		cp "$i" "$(basename "$NEW")"
	done
}

%{log_msg "Set scripts/SOURCES targets"}
update_target=%{primary_target}
if [ "%{primary_target}" == "rhel" ]; then
: # no-op to avoid empty if-fi error
%if 0%{?centos}
  update_scripts $update_target
  %{log_msg "Updating scripts/sources to centos version"}
  update_target=centos
%endif
fi
update_scripts $update_target

%endif

%{log_msg "End of kernel config"}
cd ..
# # End of Configs stuff

# get rid of unwanted files resulting from patch fuzz
find . \( -name "*.orig" -o -name "*~" \) -delete >/dev/null

# remove unnecessary SCM files
find . -name .gitignore -delete >/dev/null

cd ..

###
### build
###
# AZL: Copy mariner.pem signing CA cert into kernel source tree
%ifnarch noarch %nobuildarches
cp %{SOURCE5002} linux-%{KVERREL}/certs/mariner.pem
# AZL: Overwrite Fedora-generated configs with complete AZL kernel configs
%{log_msg "AZL: Overwrite configs with AZL kernel configs"}
cd linux-%{KVERREL}/configs
# Remove all Fedora-generated configs — we replace with AZL configs for build arch only
rm -f %{name}-%{specrpmversion}-*.config
%ifarch x86_64
cp %{SOURCE5000} %{name}-%{specrpmversion}-x86_64.config
%endif
%ifarch aarch64
cp %{SOURCE5001} %{name}-%{specrpmversion}-aarch64.config
%endif
# Re-run process_configs.sh to validate AZL configs (make olddefconfig + listnewconfig)
OPTS="-w -n -c"
RHJOBS=$RPM_BUILD_NCPUS SPECPACKAGE_NAME=%{name} ./process_configs.sh $OPTS %{specrpmversion}
cd ../..
%endif
%build
%{log_msg "Start of build stage"}

%{log_msg "General arch build configuration"}
rm -rf %{buildroot_unstripped} || true
mkdir -p %{buildroot_unstripped}

%if %{with_sparse}
%define sparse_mflags	C=1
%endif

cp_vmlinux()
{
  eu-strip --remove-comment -o "$2" "$1"
}

# Note we need to disable these flags for cross builds because the flags
# from redhat-rpm-config assume that host == target so target arch
# flags cause issues with the host compiler.
%if !%{with_cross}
%define build_hostcflags  %{?build_cflags}
%define build_hostldflags %{?build_ldflags}
%endif

%define make %{__make} %{?cross_opts} %{?make_opts} HOSTCFLAGS="%{?build_hostcflags}" HOSTLDFLAGS="%{?build_hostldflags}"

InitBuildVars() {
    %{log_msg "InitBuildVars for $1"}

    %{log_msg "InitBuildVars: Initialize build variables"}
    # Initialize the kernel .config file and create some variables that are
    # needed for the actual build process.

    Variant=$1

    # Pick the right kernel config file
    Config=%{name}-%{specrpmversion}-%{_target_cpu}${Variant:+-${Variant}}.config
    DevelDir=/usr/src/kernels/%{KVERREL}${Variant:++${Variant}}

    KernelVer=%{specversion}-%{release}.%{_target_cpu}${Variant:++${Variant}}

    %{log_msg "InitBuildVars: Update Makefile"}
    # make sure EXTRAVERSION says what we want it to say
    # Trim the release if this is a CI build, since KERNELVERSION is limited to 64 characters
    ShortRel=$(perl -e "print \"%{release}\" =~ s/\.pr\.[0-9A-Fa-f]{32}//r")
    perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -${ShortRel}.%{_target_cpu}${Variant:++${Variant}}/" Makefile

    # if pre-rc1 devel kernel, must fix up PATCHLEVEL for our versioning scheme
    # if we are post rc1 this should match anyway so this won't matter
    perl -p -i -e 's/^PATCHLEVEL.*/PATCHLEVEL = %{patchlevel}/' Makefile

    %{log_msg "InitBuildVars: Copy files"}
    %{make} %{?_smp_mflags} mrproper
    cp configs/$Config .config

    %if %{signkernel}%{signmodules}
    cp configs/x509.genkey certs/.
    %endif

%if %{with_debuginfo} == 0
    sed -i 's/^\(CONFIG_DEBUG_INFO.*\)=y/# \1 is not set/' .config
%endif

    Arch=`head -1 .config | cut -b 3-`
    %{log_msg "InitBuildVars: USING ARCH=$Arch"}

    KCFLAGS="%{?kcflags}"
}

#Build bootstrap bpftool
BuildBpftool(){
    export BPFBOOTSTRAP_CFLAGS=$(echo "%{__global_compiler_flags}" | sed -r "s/\-specs=[^\ ]+\/redhat-annobin-cc1//")
    export BPFBOOTSTRAP_LDFLAGS=$(echo "%{__global_ldflags}" | sed -r "s/\-specs=[^\ ]+\/redhat-annobin-cc1//")
    CFLAGS="" LDFLAGS="" make EXTRA_CFLAGS="${BPFBOOTSTRAP_CFLAGS}" EXTRA_CXXFLAGS="${BPFBOOTSTRAP_CFLAGS}" EXTRA_LDFLAGS="${BPFBOOTSTRAP_LDFLAGS}" %{?make_opts} %{?clang_make_opts} V=1 -C tools/bpf/bpftool bootstrap
}

BuildKernel() {
    %{log_msg "BuildKernel for $4"}
    MakeTarget=$1
    KernelImage=$2
    DoVDSO=$3
    Variant=$4
    InstallName=${5:-vmlinuz}

    %{log_msg "Setup variables"}
    DoModules=1
    if [ "$Variant" = "zfcpdump" ]; then
	    DoModules=0
    fi

    # When the bootable image is just the ELF kernel, strip it.
    # We already copy the unstripped file into the debuginfo package.
    if [ "$KernelImage" = vmlinux ]; then
      CopyKernel=cp_vmlinux
    else
      CopyKernel=cp
    fi

%if %{with_gcov}
    %{log_msg "Setup build directories"}
    # Make build directory unique for each variant, so that gcno symlinks
    # are also unique for each variant.
    if [ -n "$Variant" ]; then
        ln -s $(pwd) ../linux-%{KVERREL}-${Variant}
    fi
    %{log_msg "GCOV - continuing build in: $(pwd)"}
    pushd ../linux-%{KVERREL}${Variant:+-${Variant}}
    pwd > ../kernel${Variant:+-${Variant}}-gcov.list
%endif

    %{log_msg "Calling InitBuildVars for $Variant"}
    InitBuildVars $Variant

    %{log_msg "BUILDING A KERNEL FOR ${Variant} %{_target_cpu}..."}

    %{make} ARCH=$Arch olddefconfig >/dev/null

    %{log_msg "Setup build-ids"}
    # This ensures build-ids are unique to allow parallel debuginfo
    perl -p -i -e "s/^CONFIG_BUILD_SALT.*/CONFIG_BUILD_SALT=\"%{KVERREL}\"/" .config
    %{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} $MakeTarget %{?sparse_mflags} %{?kernel_mflags}
    if [ $DoModules -eq 1 ]; then
	%{make} ARCH=$Arch KCFLAGS="$KCFLAGS" WITH_GCOV="%{?with_gcov}" %{?_smp_mflags} modules %{?sparse_mflags} || exit 1
    fi

    %{log_msg "Setup RPM_BUILD_ROOT directories"}
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/systemtap
%if %{with_debuginfo}
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/%{image_install_path}
%endif

%ifarch aarch64 riscv64
    %{log_msg "Build dtb kernel"}
    mkdir -p $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    %{make} ARCH=$Arch dtbs INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    %{make} ARCH=$Arch dtbs_install INSTALL_DTBS_PATH=$RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer
    cp -r $RPM_BUILD_ROOT/%{image_install_path}/dtb-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/dtb
    find arch/$Arch/boot/dts -name '*.dtb' -type f -delete
%endif

    %{log_msg "Cleanup temp btf files"}
    # Remove large intermediate files we no longer need to save space
    # (-f required for zfcpdump builds that do not enable BTF)
    rm -f vmlinux.o .tmp_vmlinux.btf

    %{log_msg "Install files to RPM_BUILD_ROOT"}

    # Comment out specific config settings that may use resources not available
    # to the end user so that the packaged config file can be easily reused with
    # upstream make targets
    %if %{signkernel}%{signmodules}
      for configopt in SYSTEM_TRUSTED_KEYS EFI_SBAT_FILE; do
        sed -i -e '/^CONFIG_'"${configopt}"'/{
          i\# The kernel was built with
          s/^/# /
          a\# We are resetting this value to facilitate local builds
          a\CONFIG_'"${configopt}"'=""
          }' .config
      done
    %endif

    # Start installing the results
    install -m 644 .config $RPM_BUILD_ROOT/boot/config-$KernelVer
    install -m 644 .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/config
    install -m 644 System.map $RPM_BUILD_ROOT/boot/System.map-$KernelVer
    install -m 644 System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/System.map

    %{log_msg "Reserving 40MB in boot for initramfs"}
    # We estimate the size of the initramfs because rpm needs to take this size
    # into consideration when performing disk space calculations. (See bz #530778)
    dd if=/dev/zero of=$RPM_BUILD_ROOT/boot/initramfs-$KernelVer.img bs=1M count=40

    if [ -f arch/$Arch/boot/zImage.stub ]; then
      %{log_msg "Copy zImage.stub to RPM_BUILD_ROOT"}
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/%{image_install_path}/zImage.stub-$KernelVer || :
      cp arch/$Arch/boot/zImage.stub $RPM_BUILD_ROOT/lib/modules/$KernelVer/zImage.stub-$KernelVer || :
    fi

    %if %{signkernel}
    %{log_msg "Copy kernel for signing"}
    if [ "$KernelImage" = vmlinux ]; then
        # We can't strip and sign $KernelImage in place, because
        # we need to preserve original vmlinux for debuginfo.
        # Use a copy for signing.
        $CopyKernel $KernelImage $KernelImage.tosign
        KernelImage=$KernelImage.tosign
        CopyKernel=cp
    fi

    SignImage=$KernelImage

    %ifarch x86_64 aarch64
    %{log_msg "Sign kernel image"}
    %pesign -s -i $SignImage -o vmlinuz.signed -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
    %endif
    %ifarch s390x ppc64le
    if [ -x /usr/bin/rpm-sign ]; then
	rpm-sign --key "%{pesign_name_0}" --lkmsign $SignImage --output vmlinuz.signed
    elif [ "$DoModules" == "1" -a "%{signmodules}" == "1" ]; then
	chmod +x scripts/sign-file
	./scripts/sign-file -p sha256 certs/signing_key.pem certs/signing_key.x509 $SignImage vmlinuz.signed
    else
	mv $SignImage vmlinuz.signed
    fi
    %endif

    if [ ! -s vmlinuz.signed ]; then
	%{log_msg "pesigning failed"}
        exit 1
    fi
    mv vmlinuz.signed $SignImage
    # signkernel
    %endif

    %{log_msg "copy signed kernel"}
    $CopyKernel $KernelImage \
                $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    chmod 755 $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    cp $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer $RPM_BUILD_ROOT/lib/modules/$KernelVer/$InstallName

    # hmac sign the kernel for FIPS
    %{log_msg "hmac sign the kernel for FIPS"}
    %{log_msg "Creating hmac file: $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac"}
    ls -l $RPM_BUILD_ROOT/%{image_install_path}/$InstallName-$KernelVer
    (cd $RPM_BUILD_ROOT/%{image_install_path} && sha512hmac $InstallName-$KernelVer) > $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac;
    cp $RPM_BUILD_ROOT/%{image_install_path}/.vmlinuz-$KernelVer.hmac $RPM_BUILD_ROOT/lib/modules/$KernelVer/.vmlinuz.hmac

    if [ $DoModules -eq 1 ]; then
	%{log_msg "Install modules in RPM_BUILD_ROOT"}
	# Override $(mod-fw) because we don't want it to install any firmware
	# we'll get it from the linux-firmware package and we don't want conflicts
	%{make} %{?_smp_mflags} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT %{?_smp_mflags} modules_install KERNELRELEASE=$KernelVer mod-fw=
    fi

%if %{with_gcov}
    %{log_msg "install gcov-needed files to $BUILDROOT/$BUILD/"}
    # install gcov-needed files to $BUILDROOT/$BUILD/...:
    #   gcov_info->filename is absolute path
    #   gcno references to sources can use absolute paths (e.g. in out-of-tree builds)
    #   sysfs symlink targets (set up at compile time) use absolute paths to BUILD dir
    find . \( -name '*.gcno' -o -name '*.[chS]' \) -exec install -D '{}' "$RPM_BUILD_ROOT/$(pwd)/{}" \;
%endif

    %{log_msg "Add VDSO files"}
    # add an a noop %%defattr statement 'cause rpm doesn't like empty file list files
    echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-ldsoconf.list
    if [ $DoVDSO -ne 0 ]; then
        %{make} ARCH=$Arch INSTALL_MOD_PATH=$RPM_BUILD_ROOT vdso_install KERNELRELEASE=$KernelVer
        if [ -s ldconfig-kernel.conf ]; then
             install -D -m 444 ldconfig-kernel.conf \
                $RPM_BUILD_ROOT/etc/ld.so.conf.d/kernel-$KernelVer.conf
	     echo /etc/ld.so.conf.d/kernel-$KernelVer.conf >> ../kernel${Variant:+-${Variant}}-ldsoconf.list
        fi

        rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/vdso/.build-id
    fi

    %{log_msg "Save headers/makefiles, etc. for kernel-headers"}
    # And save the headers/makefiles etc for building modules against
    #
    # This all looks scary, but the end result is supposed to be:
    # * all arch relevant include/ files
    # * all Makefile/Kconfig files
    # * all script/ files

    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/source
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    (cd $RPM_BUILD_ROOT/lib/modules/$KernelVer ; ln -s build source)
    # dirs for additional modules per module-init-tools, kbuild/modules.txt
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/updates
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/weak-updates
    # CONFIG_KERNEL_HEADER_TEST generates some extra files in the process of
    # testing so just delete
    find . -name *.h.s -delete
    # first copy everything
    cp --parents `find  -type f -name "Makefile*" -o -name "Kconfig*"` $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ ! -e Module.symvers ]; then
        touch Module.symvers
    fi
    cp Module.symvers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp System.map $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    if [ -s Module.markers ]; then
      cp Module.markers $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi

    # create the kABI metadata for use in packaging
    # NOTENOTE: the name symvers is used by the rpm backend
    # NOTENOTE: to discover and run the /usr/lib/rpm/fileattrs/kabi.attr
    # NOTENOTE: script which dynamically adds exported kernel symbol
    # NOTENOTE: checksums to the rpm metadata provides list.
    # NOTENOTE: if you change the symvers name, update the backend too
    %{log_msg "GENERATING kernel ABI metadata"}
    %compression --stdout %compression_flags < Module.symvers > $RPM_BUILD_ROOT/boot/symvers-$KernelVer.%compext
    cp $RPM_BUILD_ROOT/boot/symvers-$KernelVer.%compext $RPM_BUILD_ROOT/lib/modules/$KernelVer/symvers.%compext

%if %{with_kabichk}
    %{log_msg "kABI checking is enabled in kernel SPEC file."}
    chmod 0755 $RPM_SOURCE_DIR/check-kabi
    if [ -e $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Variant ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_%{_target_cpu}$Variant $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
	%{log_msg "NOTE: Cannot find reference Module.kabi file."}
    fi
%endif

%if %{with_kabidupchk}
    %{log_msg "kABI DUP checking is enabled in kernel SPEC file."}
    if [ -e $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Variant ]; then
        cp $RPM_SOURCE_DIR/Module.kabi_dup_%{_target_cpu}$Variant $RPM_BUILD_ROOT/Module.kabi
        $RPM_SOURCE_DIR/check-kabi -k $RPM_BUILD_ROOT/Module.kabi -s Module.symvers || exit 1
        # for now, don't keep it around.
        rm $RPM_BUILD_ROOT/Module.kabi
    else
	%{log_msg "NOTE: Cannot find DUP reference Module.kabi file."}
    fi
%endif

%if %{with_kabidw_base}
    # Don't build kabi base for debug kernels
    if [ "$Variant" != "zfcpdump" -a "$Variant" != "debug" ]; then
        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf
        tar -xvf %{SOURCE301} -C $RPM_BUILD_ROOT/kabi-dwarf

        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf/stablelists
        tar -xvf %{SOURCE300} -C $RPM_BUILD_ROOT/kabi-dwarf/stablelists

	%{log_msg "GENERATING DWARF-based kABI baseline dataset"}
        chmod 0755 $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh
        $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh generate \
            "$RPM_BUILD_ROOT/kabi-dwarf/stablelists/kabi-current/kabi_stablelist_%{_target_cpu}" \
            "$(pwd)" \
            "$RPM_BUILD_ROOT/kabidw-base/%{_target_cpu}${Variant:+.${Variant}}" || :

        rm -rf $RPM_BUILD_ROOT/kabi-dwarf
    fi
%endif

%if %{with_kabidwchk}
    if [ "$Variant" != "zfcpdump" ]; then
        mkdir -p $RPM_BUILD_ROOT/kabi-dwarf
        tar -xvf %{SOURCE301} -C $RPM_BUILD_ROOT/kabi-dwarf
        if [ -d "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}" ]; then
            mkdir -p $RPM_BUILD_ROOT/kabi-dwarf/stablelists
            tar -xvf %{SOURCE300} -C $RPM_BUILD_ROOT/kabi-dwarf/stablelists

	    %{log_msg "GENERATING DWARF-based kABI dataset"}
            chmod 0755 $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh generate \
                "$RPM_BUILD_ROOT/kabi-dwarf/stablelists/kabi-current/kabi_stablelist_%{_target_cpu}" \
                "$(pwd)" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}.tmp" || :

	    %{log_msg "kABI DWARF-based comparison report"}
            $RPM_BUILD_ROOT/kabi-dwarf/run_kabi-dw.sh compare \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}" \
                "$RPM_BUILD_ROOT/kabi-dwarf/base/%{_target_cpu}${Variant:+.${Variant}}.tmp" || :
	    %{log_msg "End of kABI DWARF-based comparison report"}
        else
	    %{log_msg "Baseline dataset for kABI DWARF-BASED comparison report not found"}
        fi

        rm -rf $RPM_BUILD_ROOT/kabi-dwarf
    fi
%endif

   %{log_msg "Cleanup Makefiles/Kconfig files"}
    # then drop all but the needed Makefiles/Kconfig files
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    cp .config $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    rm -rf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/tracing
    rm -f $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts/spdxcheck.py

%ifarch s390x
    # CONFIG_EXPOLINE_EXTERN=y produces arch/s390/lib/expoline/expoline.o
    # which is needed during external module build.
    %{log_msg "Copy expoline.o"}
    if [ -f arch/s390/lib/expoline/expoline.o ]; then
      cp -a --parents arch/s390/lib/expoline/expoline.o $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
%endif

    %{log_msg "Copy additional files for make targets"}
    # Files for 'make scripts' to succeed with kernel-devel.
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/security/selinux/include
    cp -a --parents security/selinux/include/classmap.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents security/selinux/include/initial_sid_to_string.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/include/tools
    cp -a --parents tools/include/tools/be_byteshift.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/tools/le_byteshift.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    # Files for 'make prepare' to succeed with kernel-devel.
    cp -a --parents tools/include/linux/compiler* $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/linux/types.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/build/Build.include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/build/fixdep.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/sync-check.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/bpf/resolve_btfids $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    cp --parents security/selinux/include/policycap_names.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents security/selinux/include/policycap.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    cp -a --parents tools/include/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/asm-generic $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/linux $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/uapi/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/uapi/asm-generic $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/uapi/linux $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/include/vdso $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/scripts/utilities.mak $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/lib/subcmd $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/lib/*.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/*.[ch] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/Build $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/objtool/include/objtool/*.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/lib/bpf $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp --parents tools/lib/bpf/Build $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

    if [ -f tools/objtool/objtool ]; then
      cp -a tools/objtool/objtool $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
    fi
    if [ -f tools/objtool/fixdep ]; then
      cp -a tools/objtool/fixdep $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/objtool/ || :
    fi
    if [ -d arch/$Arch/scripts ]; then
      cp -a arch/$Arch/scripts $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch} || :
    fi
    if [ -f arch/$Arch/*lds ]; then
      cp -a arch/$Arch/*lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/arch/%{_arch}/ || :
    fi
    if [ -f arch/%{asmarch}/kernel/module.lds ]; then
      cp -a --parents arch/%{asmarch}/kernel/module.lds $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/scripts \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +
%ifarch ppc64le
    cp -a --parents arch/powerpc/lib/crtsavres.[So] $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    if [ -d arch/%{asmarch}/include ]; then
      cp -a --parents arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    fi
    if [ -d tools/arch/%{asmarch}/include ]; then
      cp -a --parents tools/arch/%{asmarch}/include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    fi
%ifarch aarch64
    # arch/arm64/include/asm/xen references arch/arm
    cp -a --parents arch/arm/include/asm/xen $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    # arch/arm64/include/asm/opcodes.h references arch/arm
    cp -a --parents arch/arm/include/asm/opcodes.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
%endif
    cp -a include $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include
    # Cross-reference from include/perf/events/sof.h
    cp -a sound/soc/sof/sof-audio.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/sound/soc/sof
%ifarch i686 x86_64
    # files for 'make prepare' to succeed with kernel-devel
    cp -a --parents arch/x86/entry/syscalls/syscall_32.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/entry/syscalls/syscall_64.tbl $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_32.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_64.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs_common.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/tools/relocs.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/purgatory.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/stack.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/setup-x86_64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/purgatory/entry64.S $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/string.c $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents arch/x86/boot/ctype.h $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/

    cp -a --parents scripts/syscalltbl.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/
    cp -a --parents scripts/syscallhdr.sh $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/

    cp -a --parents tools/arch/x86/include/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/arch/x86/include/uapi/asm $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/objtool/arch/x86/lib $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/arch/x86/lib/ $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/arch/x86/tools/gen-insn-attr-x86.awk $RPM_BUILD_ROOT/lib/modules/$KernelVer/build
    cp -a --parents tools/objtool/arch/x86/ $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

%endif
    %{log_msg "Clean up intermediate tools files"}
    # Clean up intermediate tools files
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools \( -iname "*.o" -o -iname "*.cmd" \) -exec rm -f {} +

    # Make sure the Makefile, version.h, and auto.conf have a matching
    # timestamp so that external modules can be built
    touch -r $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile \
        $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/generated/uapi/linux/version.h \
        $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/include/config/auto.conf

%if %{with_debuginfo}
    eu-readelf -n vmlinux | grep "Build ID" | awk '{print $NF}' > vmlinux.id
    cp vmlinux.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.id

    %{log_msg "Copy additional files for kernel-debuginfo rpm"}
    #
    # save the vmlinux file for kernel debugging into the kernel-debuginfo rpm
    # (use mv + symlink instead of cp to reduce disk space requirements)
    #
    mkdir -p $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    mv vmlinux $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    ln -s $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux vmlinux
    if [ -n "%{?vmlinux_decompressor}" ]; then
	    eu-readelf -n  %{vmlinux_decompressor} | grep "Build ID" | awk '{print $NF}' > vmlinux.decompressor.id
	    # Without build-id the build will fail. But for s390 the build-id
	    # wasn't added before 5.11. In case it is missing prefer not
	    # packaging the debuginfo over a build failure.
	    if [ -s vmlinux.decompressor.id ]; then
		    cp vmlinux.decompressor.id $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/vmlinux.decompressor.id
		    cp %{vmlinux_decompressor} $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux.decompressor
	    fi
    fi

    # build and copy the vmlinux-gdb plugin files into kernel-debuginfo
    %{make} ARCH=$Arch %{?_smp_mflags} scripts_gdb
    cp -a --parents scripts/gdb/{,linux/}*.py $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer
    # this should be a relative symlink (Kbuild creates an absolute one)
    ln -s scripts/gdb/vmlinux-gdb.py $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/vmlinux-gdb.py
    %py_byte_compile %{python3} $RPM_BUILD_ROOT%{debuginfodir}/lib/modules/$KernelVer/scripts/gdb
%endif

    %{log_msg "Create modnames"}
    find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name "*.ko" -type f >modnames

    # mark modules executable so that strip-to-file can strip them
    xargs --no-run-if-empty chmod u+x < modnames

    # Generate a list of modules for block and networking.
    %{log_msg "Generate a list of modules for block and networking"}
    grep -F /drivers/ modnames | xargs --no-run-if-empty nm -upA |
    sed -n 's,^.*/\([^/]*\.ko\):  *U \(.*\)$,\1 \2,p' > drivers.undef

    collect_modules_list()
    {
      sed -r -n -e "s/^([^ ]+) \\.?($2)\$/\\1/p" drivers.undef |
        LC_ALL=C sort -u > $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      if [ ! -z "$3" ]; then
        sed -r -e "/^($3)\$/d" -i $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.$1
      fi
    }

    collect_modules_list networking \
      'register_netdev|ieee80211_register_hw|usbnet_probe|phy_driver_register|rt(l_|2x00)(pci|usb)_probe|register_netdevice'
    collect_modules_list block \
      'ata_scsi_ioctl|scsi_add_host|scsi_add_host_with_dma|blk_alloc_queue|blk_init_queue|register_mtd_blktrans|scsi_esp_register|scsi_register_device_handler|blk_queue_physical_block_size' 'pktcdvd.ko|dm-mod.ko'
    collect_modules_list drm \
      'drm_open|drm_init'
    collect_modules_list modesetting \
      'drm_crtc_init'

    %{log_msg "detect missing or incorrect license tags"}
    # detect missing or incorrect license tags
    ( find $RPM_BUILD_ROOT/lib/modules/$KernelVer -name '*.ko' | xargs /sbin/modinfo -l | \
        grep -E -v 'GPL( v2)?$|Dual BSD/GPL$|Dual MPL/GPL$|GPL and additional rights$' ) && exit 1


    if [ $DoModules -eq 0 ]; then
        %{log_msg "Create empty files for RPM packaging"}
        # Ensure important files/directories exist to let the packaging succeed
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-core.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-extra.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-internal.list
        echo '%%defattr(-,-,-)' > ../kernel${Variant:+-${Variant}}-modules-partner.list
        mkdir -p $RPM_BUILD_ROOT/lib/modules/$KernelVer/kernel
        # Add files usually created by make modules, needed to prevent errors
        # thrown by depmod during package installation
        touch $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.order
        touch $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.builtin
    fi

    # Copy the System.map file for depmod to use
    cp System.map $RPM_BUILD_ROOT/.

    if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" || "$Variant" == "rt-64k" || "$Variant" == "rt-64k-debug" || "$Variant" == "automotive" || "$Variant" == "automotive-debug" ]]; then
	%{log_msg "Skipping efiuki build"}
    else
%if %{with_efiuki}
        %{log_msg "Setup the EFI UKI kernel"}
	KernelUnifiedImageDir="$RPM_BUILD_ROOT/lib/modules/$KernelVer"
    	KernelUnifiedImage="$KernelUnifiedImageDir/$InstallName-virt.efi"
	KernelUnifiedInitrd="$KernelUnifiedImageDir/$InstallName-virt.img"

    	mkdir -p $KernelUnifiedImageDir

    	dracut --conf=%{SOURCE86} \
           --confdir=$(mktemp -d) \
           --no-hostonly \
           --verbose \
           --kver "$KernelVer" \
           --kmoddir "$RPM_BUILD_ROOT/lib/modules/$KernelVer/" \
           --logfile=$(mktemp) \
	   $KernelUnifiedInitrd

	ukify build --linux $(realpath $KernelImage) --initrd $KernelUnifiedInitrd \
	   --sbat @uki.sbat --os-release @/etc/os-release --uname $KernelVer \
	   --cmdline 'console=tty0 console=ttyS0' --output $KernelUnifiedImage

	rm -f $KernelUnifiedInitrd

  KernelAddonsDirOut="$KernelUnifiedImage.extra.d"
  mkdir -p $KernelAddonsDirOut
  python3 %{SOURCE151} %{SOURCE152} $KernelAddonsDirOut virt %{primary_target} %{_target_cpu} @uki-addons.sbat

%if %{signkernel}
	%{log_msg "Sign the EFI UKI kernel"}
%if 0%{?fedora}%{?eln}
        %pesign -s -i $KernelUnifiedImage -o $KernelUnifiedImage.signed -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
%else
%if 0%{?centos}
        UKI_secureboot_name=centossecureboot204
%else
        UKI_secureboot_name=redhatsecureboot504
%endif
        UKI_secureboot_cert=%{_datadir}/pki/sb-certs/secureboot-uki-virt-%{_arch}.cer

        %pesign -s -i $KernelUnifiedImage -o $KernelUnifiedImage.signed -a %{secureboot_ca_0} -c $UKI_secureboot_cert -n $UKI_secureboot_name
# 0%{?fedora}%{?eln}
%endif
        if [ ! -s $KernelUnifiedImage.signed ]; then
            echo "pesigning failed"
            exit 1
        fi
        mv $KernelUnifiedImage.signed $KernelUnifiedImage

      for addon in "$KernelAddonsDirOut"/*; do
        %pesign -s -i $addon -o $addon.signed -a %{secureboot_ca_0} -c %{secureboot_key_0} -n %{pesign_name_0}
        rm -f $addon
        mv $addon.signed $addon
      done

# signkernel
%endif

    # hmac sign the UKI for FIPS
    KernelUnifiedImageHMAC="$KernelUnifiedImageDir/.$InstallName-virt.efi.hmac"
    %{log_msg "hmac sign the UKI for FIPS"}
    %{log_msg "Creating hmac file: $KernelUnifiedImageHMAC"}
    (cd $KernelUnifiedImageDir && sha512hmac $InstallName-virt.efi) > $KernelUnifiedImageHMAC;

# with_efiuki
%endif
	:  # in case of empty block
    fi # "$Variant" == "rt" || "$Variant" == "rt-debug" || "$Variant" == "automotive" || "$Variant" == "automotive-debug"


    #
    # Generate the modules files lists
    #
    move_kmod_list()
    {
        local module_list="$1"
        local subdir_name="$2"

        mkdir -p "$RPM_BUILD_ROOT/lib/modules/$KernelVer/$subdir_name"

        set +x
        while read -r kmod; do
            local target_file="$RPM_BUILD_ROOT/lib/modules/$KernelVer/$subdir_name/$kmod"
            local target_dir="${target_file%/*}"
            mkdir -p "$target_dir"
            mv "$RPM_BUILD_ROOT/lib/modules/$KernelVer/kernel/$kmod" "$target_dir"
        done < <(sed -e 's|^kernel/||' "$module_list")
        set -x
    }

    create_module_file_list()
    {
        # subdirectory within /lib/modules/$KernelVer where kmods should go
        local module_subdir="$1"
        # kmod list with relative paths produced by filtermods.py
        local relative_kmod_list="$2"
        # list with absolute paths to kmods and other files to be included
        local absolute_file_list="$3"
        # if 1, this adds also all kmod directories to absolute_file_list
        local add_all_dirs="$4"
        local run_mod_deny="$5"

        if [ "$module_subdir" != "kernel" ]; then
            # move kmods into subdirs if needed (internal, partner, extra,..)
            move_kmod_list $relative_kmod_list $module_subdir
        fi

        # make kmod paths absolute
        sed -e 's|^kernel/|/lib/modules/'$KernelVer'/'$module_subdir'/|' $relative_kmod_list > $absolute_file_list

	if [ "$run_mod_deny" -eq 1 ]; then
            # run deny-mod script, this adds blacklist-* files to absolute_file_list
            %{SOURCE20} "$RPM_BUILD_ROOT" lib/modules/$KernelVer $absolute_file_list
	fi

%if %{zipmodules}
        # deny-mod script works with kmods as they are now (not compressed),
        # but if they will be we need to add compext to all
        sed -i %{?zipsed} $absolute_file_list
%endif
        # add also dir for the case when there are no kmods
        # "kernel" subdir is covered in %files section, skip it here
        if [ "$module_subdir" != "kernel" ]; then
                echo "%dir /lib/modules/$KernelVer/$module_subdir" >> $absolute_file_list
        fi

        if [ "$add_all_dirs" -eq 1 ]; then
            (cd $RPM_BUILD_ROOT; find lib/modules/$KernelVer/kernel -mindepth 1 -type d | sort -n) > ../module-dirs.list
            sed -e 's|^lib|%dir /lib|' ../module-dirs.list >> $absolute_file_list
        fi
    }

    if [ $DoModules -eq 1 ]; then
        # save modules.dep for debugging
        cp $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.dep ../

        %{log_msg "Create module list files for all kernel variants"}
        variants_param=""
        if [[ "$Variant" == "rt" || "$Variant" == "rt-debug" ]]; then
            variants_param="-r rt"
        fi
        if [[ "$Variant" == "rt-64k" || "$Variant" == "rt-64k-debug" ]]; then
            variants_param="-r rt-64k"
        fi
        if [[ "$Variant" == "automotive" || "$Variant" == "automotive-debug" ]]; then
            variants_param="-r automotive"
        fi
        # this creates ../modules-*.list output, where each kmod path is as it
        # appears in modules.dep (relative to lib/modules/$KernelVer)
        ret=0
        %{SOURCE22} -l "../filtermods-$KernelVer.log" sort -d $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.dep -c configs/def_variants.yaml $variants_param -o .. || ret=$?
        if [ $ret -ne 0 ]; then
            echo "8< --- filtermods-$KernelVer.log ---"
            cat "../filtermods-$KernelVer.log"
            echo "--- filtermods-$KernelVer.log --- >8"

            echo "8< --- modules.dep ---"
            cat $RPM_BUILD_ROOT/lib/modules/$KernelVer/modules.dep
            echo "--- modules.dep --- >8"
            exit 1
        fi

        create_module_file_list "kernel" ../modules-core.list ../kernel${Variant:+-${Variant}}-modules-core.list 1 0
        create_module_file_list "kernel" ../modules.list ../kernel${Variant:+-${Variant}}-modules.list 0 0
        create_module_file_list "internal" ../modules-internal.list ../kernel${Variant:+-${Variant}}-modules-internal.list 0 1
        create_module_file_list "kernel" ../modules-extra.list ../kernel${Variant:+-${Variant}}-modules-extra.list 0 1
%if 0%{!?fedora:1}
        create_module_file_list "partner" ../modules-partner.list ../kernel${Variant:+-${Variant}}-modules-partner.list 1 1
%endif
    fi # $DoModules -eq 1

    remove_depmod_files()
    {
        # remove files that will be auto generated by depmod at rpm -i time
        pushd $RPM_BUILD_ROOT/lib/modules/$KernelVer/
            # in case below list needs to be extended, remember to add a
            # matching ghost entry in the files section as well
            rm -f modules.{alias,alias.bin,builtin.alias.bin,builtin.bin} \
                  modules.{dep,dep.bin,devname,softdep,symbols,symbols.bin,weakdep}
        popd
    }

    # Cleanup
    %{log_msg "Cleanup build files"}
    rm -f $RPM_BUILD_ROOT/System.map
    %{log_msg "Remove depmod files"}
    remove_depmod_files

%if %{with_cross}
    make -C $RPM_BUILD_ROOT/lib/modules/$KernelVer/build M=scripts clean
    make -C $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/tools/bpf/resolve_btfids clean
    sed -i 's/REBUILD_SCRIPTS_FOR_CROSS:=0/REBUILD_SCRIPTS_FOR_CROSS:=1/' $RPM_BUILD_ROOT/lib/modules/$KernelVer/build/Makefile
%endif

    # Move the devel headers out of the root file system
    %{log_msg "Move the devel headers to RPM_BUILD_ROOT"}
    mkdir -p $RPM_BUILD_ROOT/usr/src/kernels
    mv $RPM_BUILD_ROOT/lib/modules/$KernelVer/build $RPM_BUILD_ROOT/$DevelDir

    # This is going to create a broken link during the build, but we don't use
    # it after this point.  We need the link to actually point to something
    # when kernel-devel is installed, and a relative link doesn't work across
    # the F17 UsrMove feature.
    ln -sf $DevelDir $RPM_BUILD_ROOT/lib/modules/$KernelVer/build

%if %{with_debuginfo}
    # Generate vmlinux.h and put it to kernel-devel path
    # zfcpdump build does not have btf anymore
    if [ "$Variant" != "zfcpdump" ]; then
	%{log_msg "Build the bootstrap bpftool to generate vmlinux.h"}
        # Build the bootstrap bpftool to generate vmlinux.h
        BuildBpftool
        tools/bpf/bpftool/bootstrap/bpftool btf dump file vmlinux format c > $RPM_BUILD_ROOT/$DevelDir/vmlinux.h
    fi
%endif

    %{log_msg "Cleanup kernel-devel and kernel-debuginfo files"}
    # prune junk from kernel-devel
    find $RPM_BUILD_ROOT/usr/src/kernels -name ".*.cmd" -delete
    # prune junk from kernel-debuginfo
    find $RPM_BUILD_ROOT/usr/src/kernels -name "*.mod.c" -delete

    # Red Hat UEFI Secure Boot CA cert, which can be used to authenticate the kernel
    %{log_msg "Install certs"}
    mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer
%if %{signkernel}
    install -m 0644 %{secureboot_ca_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
    %ifarch s390x ppc64le
    if [ -x /usr/bin/rpm-sign ]; then
        install -m 0644 %{secureboot_key_0} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
    fi
    %endif
%endif

%if 0%{?rhel}
    # Red Hat IMA code-signing cert, which is used to authenticate package files
    install -m 0644 %{ima_signing_cert} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{ima_cert_name}
%endif

%if %{signmodules}
    if [ $DoModules -eq 1 ]; then
        # Save the signing keys so we can sign the modules in __modsign_install_post
        cp certs/signing_key.pem certs/signing_key.pem.sign${Variant:++${Variant}}
        cp certs/signing_key.x509 certs/signing_key.x509.sign${Variant:++${Variant}}
        %ifarch s390x ppc64le
        if [ ! -x /usr/bin/rpm-sign ]; then
            install -m 0644 certs/signing_key.x509.sign${Variant:++${Variant}} $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/kernel-signing-ca.cer
            openssl x509 -in certs/signing_key.pem.sign${Variant:++${Variant}} -outform der -out $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
            chmod 0644 $RPM_BUILD_ROOT%{_datadir}/doc/kernel-keys/$KernelVer/%{signing_key_filename}
        fi
        %endif
    fi
%endif

%if %{with_gcov}
    popd
%endif
}

###
# DO it...
###

# prepare directories
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/boot
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}

cd linux-%{KVERREL}

%if %{with_debug}
%if %{with_realtime}
BuildKernel %make_target %kernel_image %{_use_vdso} rt-debug
%endif

%if %{with_realtime_arm64_64k}
BuildKernel %make_target %kernel_image %{_use_vdso} rt-64k-debug
%endif

%if %{with_automotive} && !%{with_automotive_build}
BuildKernel %make_target %kernel_image %{_use_vdso} automotive-debug
%endif

%if %{with_arm64_16k}
BuildKernel %make_target %kernel_image %{_use_vdso} 16k-debug
%endif

%if %{with_arm64_64k}
BuildKernel %make_target %kernel_image %{_use_vdso} 64k-debug
%endif

%if %{with_up}
BuildKernel %make_target %kernel_image %{_use_vdso} debug
%endif
%endif

%if %{with_zfcpdump}
BuildKernel %make_target %kernel_image %{_use_vdso} zfcpdump
%endif

%if %{with_arm64_16k_base}
BuildKernel %make_target %kernel_image %{_use_vdso} 16k
%endif

%if %{with_arm64_64k_base}
BuildKernel %make_target %kernel_image %{_use_vdso} 64k
%endif

%if %{with_realtime_base}
BuildKernel %make_target %kernel_image %{_use_vdso} rt
%endif

%if %{with_realtime_arm64_64k_base}
BuildKernel %make_target %kernel_image %{_use_vdso} rt-64k
%endif

%if %{with_automotive_base}
BuildKernel %make_target %kernel_image %{_use_vdso} automotive
%endif

%if %{with_up_base}
BuildKernel %make_target %kernel_image %{_use_vdso}
%endif

%ifnarch noarch i686 %{nobuildarches}
%if !%{with_debug} && !%{with_zfcpdump} && !%{with_up} && !%{with_arm64_16k} && !%{with_arm64_64k} && !%{with_realtime} && !%{with_realtime_arm64_64k} && !%{with_automotive}
# If only building the user space tools, then initialize the build environment
# and some variables so that the various userspace tools can be built.
%{log_msg "Initialize userspace tools build environment"}
InitBuildVars
# Some tests build also modules, and need Module.symvers
if ! [[ -e Module.symvers ]] && [[ -f $DevelDir/Module.symvers ]]; then
    %{log_msg "Found Module.symvers in DevelDir, copying to ."}
    cp "$DevelDir/Module.symvers" .
fi
%endif
%endif

%ifarch aarch64
%global perf_build_extra_opts CORESIGHT=1
%endif
%global perf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${RPM_OPT_FLAGS}" EXTRA_CXXFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags} -Wl,-E" %{?cross_opts} -C tools/perf V=1 NO_PERF_READ_VDSO32=1 NO_PERF_READ_VDSOX32=1 WERROR=0 NO_LIBUNWIND=1 HAVE_CPLUS_DEMANGLE=1 NO_GTK2=1 NO_STRLCPY=1 NO_BIONIC=1 LIBTRACEEVENT_DYNAMIC=1 %{?perf_build_extra_opts} prefix=%{_prefix} PYTHON=%{__python3}
%if %{with_perf}
%{log_msg "Build perf"}
# perf
# make sure check-headers.sh is executable
chmod +x tools/perf/check-headers.sh
%{perf_make} DESTDIR=$RPM_BUILD_ROOT all
%endif

%if %{with_libperf}
%global libperf_make \
  %{__make} %{?make_opts} EXTRA_CFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags}" %{?cross_opts} -C tools/lib/perf V=1
  %{log_msg "build libperf"}
%{libperf_make} DESTDIR=$RPM_BUILD_ROOT
%endif

%global tools_make \
  CFLAGS="${RPM_OPT_FLAGS}" LDFLAGS="%{__global_ldflags}" EXTRA_CFLAGS="${RPM_OPT_FLAGS}" %{make} %{?make_opts}

%ifarch %{cpupowerarchs}
    # link against in-tree libcpupower for idle state support
    %global rtla_make %{tools_make} LDFLAGS="%{__global_ldflags} -L../../power/cpupower" INCLUDES="-I../../power/cpupower/lib"
    # Build libcpupower Python bindings
    %global libcpupower_python_bindings_make %{tools_make} LDFLAGS="-L%{buildroot}%{_libdir} -lcpupower"
%else
    %global rtla_make %{tools_make}
%endif

%if %{with_tools}

%if %{with_ynl}
pushd tools/net/ynl
export PIP_CONFIG_FILE=/tmp/pip.config
cat <<EOF > $PIP_CONFIG_FILE
[install]
no-index = true
no-build-isolation = false
EOF
%{tools_make} %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
popd
%endif

%ifarch %{cpupowerarchs}
# cpupower
# make sure version-gen.sh is executable.
chmod +x tools/power/cpupower/utils/version-gen.sh
%{log_msg "build cpupower"}
%{tools_make} %{?_smp_mflags} -C tools/power/cpupower CPUFREQ_BENCH=false DEBUG=false
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    %{log_msg "build centrino-decode powernow-k8-decode"}
    %{tools_make} %{?_smp_mflags} centrino-decode powernow-k8-decode
    popd
%endif
%ifarch x86_64
   pushd tools/power/x86/x86_energy_perf_policy/
   %{log_msg "build x86_energy_perf_policy"}
   %{tools_make}
   popd
   pushd tools/power/x86/turbostat
   %{log_msg "build turbostat"}
   %{tools_make}
   popd
   pushd tools/power/x86/intel-speed-select
   %{log_msg "build intel-speed-select"}
   %{tools_make}
   popd
   pushd tools/arch/x86/intel_sdsi
   %{log_msg "build intel_sdsi"}
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}"
   popd
%endif
%endif
pushd tools/thermal/tmon/
%{log_msg "build tmon"}
%{tools_make}
popd
pushd tools/bootconfig/
%{log_msg "build bootconfig"}
%{tools_make}
popd
pushd tools/iio/
%{log_msg "build iio"}
%{tools_make}
popd
pushd tools/gpio/
%{log_msg "build gpio"}
%{tools_make}
popd
# build VM tools
pushd tools/mm/
%{log_msg "build slabinfo page_owner_sort"}
%{tools_make} slabinfo page_owner_sort
popd
pushd tools/verification/rv/
%{log_msg "build rv"}
%{tools_make}
popd
pushd tools/tracing/rtla
%{log_msg "build rtla"}
%{rtla_make}
popd
%endif

#set RPM_VMLINUX_H
if [ -f $RPM_BUILD_ROOT/$DevelDir/vmlinux.h ]; then
  RPM_VMLINUX_H=$RPM_BUILD_ROOT/$DevelDir/vmlinux.h
elif [ -f $DevelDir/vmlinux.h ]; then
  RPM_VMLINUX_H=$DevelDir/vmlinux.h
fi
echo "${RPM_VMLINUX_H}" > ../vmlinux_h_path

%if %{with_selftests}
%{log_msg "start build selftests"}
# Unfortunately, samples/bpf/Makefile expects that the headers are installed
# in the source tree. We installed them previously to $RPM_BUILD_ROOT/usr
# but there's no way to tell the Makefile to take them from there.
%{log_msg "install headers for selftests"}
%{make} %{?_smp_mflags} headers_install

# If we re building only tools without kernel, we need to generate config
# headers and prepare tree for modules building. The modules_prepare target
# will cover both.
if [ ! -f include/generated/autoconf.h ]; then
   %{log_msg "modules_prepare for selftests"}
   %{make} %{?_smp_mflags} modules_prepare
fi

# Build BPFtool for samples/bpf
if [ ! -f tools/bpf/bpftool/bootstrap/bpftool ]; then
  BuildBpftool
fi

%{log_msg "build samples/bpf"}
%{make} %{?_smp_mflags} EXTRA_CXXFLAGS="${RPM_OPT_FLAGS}" ARCH=$Arch BPFTOOL=$(pwd)/tools/bpf/bpftool/bootstrap/bpftool V=1 M=samples/bpf/ VMLINUX_H="${RPM_VMLINUX_H}" || true

pushd tools/testing/selftests
# We need to install here because we need to call make with ARCH set which
# doesn't seem possible to do in the install section.
%if %{selftests_must_build}
  force_targets="FORCE_TARGETS=1"
%else
  force_targets=""
%endif

%{log_msg "main selftests compile"}

# Some selftests (especially bpf) do not build with source fortification.
# Since selftests are not shipped, disable source fortification for them.
%global _fortify_level_bak %{_fortify_level}
%undefine _fortify_level
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"

%{make} %{?_smp_mflags} EXTRA_CFLAGS="${RPM_OPT_FLAGS}" EXTRA_CXXFLAGS="${RPM_OPT_FLAGS}" EXTRA_LDFLAGS="%{__global_ldflags}" ARCH=$Arch V=1 TARGETS="bpf cgroup kmod mm net net/can net/forwarding net/hsr net/mptcp net/netfilter net/packetdrill tc-testing memfd drivers/net drivers/net/hw iommu cachestat pid_namespace rlimits timens pidfd capabilities clone3 exec filesystems firmware landlock mount mount_setattr move_mount_set_group nsfs openat2 proc safesetid seccomp tmpfs uevent vDSO" SKIP_TARGETS="" $force_targets INSTALL_PATH=%{buildroot}%{_libexecdir}/kselftests VMLINUX_H="${RPM_VMLINUX_H}" install

# Restore the original level of source fortification
%define _fortify_level %{_fortify_level_bak}
export CFLAGS="%{build_cflags}"
export CXXFLAGS="%{build_cxxflags}"

# 'make install' for bpf is broken and upstream refuses to fix it.
# Install the needed files manually.
%{log_msg "install selftests"}
for dir in bpf bpf/no_alu32 bpf/progs; do
	# In ARK, the rpm build continues even if some of the selftests
	# cannot be built. It's not always possible to build selftests,
	# as upstream sometimes dependens on too new llvm version or has
	# other issues. If something did not get built, just skip it.
	test -d $dir || continue
	mkdir -p %{buildroot}%{_libexecdir}/kselftests/$dir
	find $dir -maxdepth 1 -type f \( -executable -o -name '*.py' -o -name settings -o \
		-name 'btf_dump_test_case_*.c' -o -name '*.ko' -o \
		-name '*.o' -exec sh -c 'readelf -h "{}" | grep -q "^  Machine:.*BPF"' \; \) -print0 | \
	xargs -0 cp -t %{buildroot}%{_libexecdir}/kselftests/$dir || true
done
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/test_progs"
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/test_progs-no_alu32"

# The urandom_read binary doesn't pass the check-rpaths check and upstream
# refuses to fix it. So, we save it to buildroot_unstripped and delete it so it
# will be hidden from check-rpaths and will automatically get restored later.
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/urandom_read"
%buildroot_save_unstripped "usr/libexec/kselftests/bpf/no_alu32/urandom_read"
rm -f %{buildroot}/usr/libexec/kselftests/bpf/urandom_read
rm -f %{buildroot}/usr/libexec/kselftests/bpf/no_alu32/urandom_read

# Copy bpftool to kselftests so selftests is packaged with
# the full bpftool instead of bootstrap bpftool
cp ./bpf/tools/sbin/bpftool %{buildroot}%{_libexecdir}/kselftests/bpf/bpftool

popd
%{log_msg "end build selftests"}
%endif

%if %{with_doc}
%{log_msg "start install docs"}
# Make the HTML pages.
%{log_msg "build html docs"}
%{__make} PYTHON=/usr/bin/python3 htmldocs || %{doc_build_fail}

# sometimes non-world-readable files sneak into the kernel source tree
chmod -R a=rX Documentation
find Documentation -type d | xargs chmod u+w
%{log_msg "end install docs"}
%endif

# Module signing (modsign)
#
# This must be run _after_ find-debuginfo.sh runs, otherwise that will strip
# the signature off of the modules.
#
# Don't sign modules for the zfcpdump variant as it is monolithic.

%define __modsign_install_post \
  if [ "%{signmodules}" -eq "1" ]; then \
    %{log_msg "Signing kernel modules ..."} \
    modules_dirs="$(shopt -s nullglob; echo $RPM_BUILD_ROOT/lib/modules/%{KVERREL}*)" \
    for modules_dir in $modules_dirs; do \
        variant_suffix="${modules_dir#$RPM_BUILD_ROOT/lib/modules/%{KVERREL}}" \
        [ "$variant_suffix" == "+zfcpdump" ] && continue \
	%{log_msg "Signing modules for %{KVERREL}${variant_suffix}"} \
        %{modsign_cmd} certs/signing_key.pem.sign${variant_suffix} certs/signing_key.x509.sign${variant_suffix} $modules_dir/ \
    done \
  fi \
  if [ "%{zipmodules}" -eq "1" ]; then \
    %{log_msg "Compressing kernel modules ..."} \
    find $RPM_BUILD_ROOT/lib/modules/ -type f -name '*.ko' | xargs -n 16 -P${RPM_BUILD_NCPUS} -r %compression %compression_flags; \
  fi \
%{nil}

###
### Special hacks for debuginfo subpackages.
###

# This macro is used by %%install, so we must redefine it before that.
%define debug_package %{nil}

%if %{with_debuginfo}

%ifnarch noarch %{nobuildarches}
%global __debug_package 1
%files -f debugfiles.list debuginfo-common-%{_target_cpu}
%endif

%endif

# We don't want to package debuginfo for self-tests and samples but
# we have to delete them to avoid an error messages about unpackaged
# files.
# Delete the debuginfo for kernel-devel files
%define __remove_unwanted_dbginfo_install_post \
  if [ "%{with_selftests}" -ne "0" ]; then \
    rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/libexec/ksamples; \
    rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/libexec/kselftests; \
  fi \
  rm -rf $RPM_BUILD_ROOT/usr/lib/debug/usr/src; \
%{nil}

# Make debugedit and gdb-add-index use target versions of tools
# when cross-compiling. This is supported since debugedit-5.1-5.fc42
# https://inbox.sourceware.org/debugedit/20250220153858.963312-1-mark@klomp.org/
%if %{with_cross}
%define __override_target_tools_for_debugedit \
	export OBJCOPY=%{_build_arch}-linux-gnu-objcopy \
	export NM=%{_build_arch}-linux-gnu-nm \
	export READELF=%{_build_arch}-linux-gnu-readelf \
%{nil}
%endif

#
# Disgusting hack alert! We need to ensure we sign modules *after* all
# invocations of strip occur, which is in __debug_install_post if
# find-debuginfo.sh runs, and __os_install_post if not.
#
%define __spec_install_post \
  %{?__override_target_tools_for_debugedit:%{__override_target_tools_for_debugedit}}\
  %{?__debug_package:%{__debug_install_post}}\
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__remove_unwanted_dbginfo_install_post}\
  %{__restore_unstripped_root_post}\
  %{__modsign_install_post}

###
### install
###

%install

cd linux-%{KVERREL}

# re-define RPM_VMLINUX_H, because it doesn't carry over from %build
RPM_VMLINUX_H="$(cat ../vmlinux_h_path)"

%if %{with_doc}
docdir=$RPM_BUILD_ROOT%{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}

# copy the source over
mkdir -p $docdir
tar -h -f - --exclude=man --exclude='.*' -c Documentation | tar xf - -C $docdir
cat %{SOURCE2} | xz > $docdir/kernel.changelog.xz
chmod 0644 $docdir/kernel.changelog.xz

# with_doc
%endif

# We have to do the headers install before the tools install because the
# kernel headers_install will remove any header files in /usr/include that
# it doesn't install itself.

%if %{with_headers}
# Install kernel headers
%{__make} ARCH=%{hdrarch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr headers_install

find $RPM_BUILD_ROOT/usr/include \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

%endif

%if %{with_cross_headers}
HDR_ARCH_LIST='arm64 powerpc s390 x86 riscv'
mkdir -p $RPM_BUILD_ROOT/usr/tmp-headers

for arch in $HDR_ARCH_LIST; do
	mkdir $RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch}
	%{__make} ARCH=${arch} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch} headers_install
done

find $RPM_BUILD_ROOT/usr/tmp-headers \
     \( -name .install -o -name .check -o \
        -name ..install.cmd -o -name ..check.cmd \) -delete

# Copy all the architectures we care about to their respective asm directories
for arch in $HDR_ARCH_LIST ; do
	mkdir -p $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include
	mv $RPM_BUILD_ROOT/usr/tmp-headers/arch-${arch}/include/* $RPM_BUILD_ROOT/usr/${arch}-linux-gnu/include/
done

rm -rf $RPM_BUILD_ROOT/usr/tmp-headers
%endif

%if %{with_kernel_abi_stablelists}
# kabi directory
INSTALL_KABI_PATH=$RPM_BUILD_ROOT/lib/modules/
mkdir -p $INSTALL_KABI_PATH

# install kabi releases directories
tar -xvf %{SOURCE300} -C $INSTALL_KABI_PATH
# with_kernel_abi_stablelists
%endif

%if %{with_perf}
# perf tool binary and supporting scripts/binaries
%{perf_make} DESTDIR=$RPM_BUILD_ROOT lib=%{_lib} install-bin
# remove the 'trace' symlink.
rm -f %{buildroot}%{_bindir}/trace

# For both of the below, yes, this should be using a macro but right now
# it's hard coded and we don't actually want it anyway right now.
# Whoever wants examples can fix it up!

# remove examples
rm -rf %{buildroot}/usr/lib/perf/examples
rm -rf %{buildroot}/usr/lib/perf/include

# python-perf extension
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-python_ext

# perf man pages (note: implicit rpm magic compresses them later)
mkdir -p %{buildroot}/%{_mandir}/man1
%{perf_make} DESTDIR=$RPM_BUILD_ROOT install-man

# remove any tracevent files, eg. its plugins still gets built and installed,
# even if we build against system's libtracevent during perf build (by setting
# LIBTRACEEVENT_DYNAMIC=1 above in perf_make macro). Those files should already
# ship with libtraceevent package.
rm -rf %{buildroot}%{_libdir}/traceevent
%endif

%if %{with_libperf}
%{libperf_make} DESTDIR=%{buildroot} prefix=%{_prefix} libdir=%{_libdir} install install_headers
# This is installed on some arches and we don't want to ship it
rm -rf %{buildroot}%{_libdir}/libperf.a
%endif

%if %{with_tools}
%ifarch %{cpupowerarchs}
%{make} -C tools/power/cpupower DESTDIR=$RPM_BUILD_ROOT libdir=%{_libdir} libexecdir=%{_libexecdir} mandir=%{_mandir} unitdir=%{_unitdir} CPUFREQ_BENCH=false install
%find_lang cpupower
mv cpupower.lang ../
%ifarch x86_64
    pushd tools/power/cpupower/debug/x86_64
    install -m755 centrino-decode %{buildroot}%{_bindir}/centrino-decode
    install -m755 powernow-k8-decode %{buildroot}%{_bindir}/powernow-k8-decode
    popd
%endif
chmod 0755 %{buildroot}%{_libdir}/libcpupower.so*
%{log_msg "Build libcpupower Python bindings"}
pushd tools/power/cpupower/bindings/python
%{libcpupower_python_bindings_make}
%{log_msg "Install libcpupower Python bindings"}
%{make} INSTALL_DIR=$RPM_BUILD_ROOT%{python3_sitearch} install
popd
%endif
%ifarch x86_64
   mkdir -p %{buildroot}%{_mandir}/man8
   pushd tools/power/x86/x86_energy_perf_policy
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/turbostat
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/power/x86/intel-speed-select
   %{tools_make} DESTDIR=%{buildroot} install
   popd
   pushd tools/arch/x86/intel_sdsi
   %{tools_make} CFLAGS="${RPM_OPT_FLAGS}" DESTDIR=%{buildroot} BINDIR=%{_sbindir} install
   popd
%endif
pushd tools/thermal/tmon
%{tools_make} INSTALL_ROOT=%{buildroot} install
popd
pushd tools/bootconfig
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/iio
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/gpio
%{tools_make} DESTDIR=%{buildroot} install
popd
install -m644 -D %{SOURCE2002} %{buildroot}%{_sysconfdir}/logrotate.d/kvm_stat
pushd tools/kvm/kvm_stat
%{__make} INSTALL_ROOT=%{buildroot} install-tools
%{__make} INSTALL_ROOT=%{buildroot} install-man
install -m644 -D kvm_stat.service %{buildroot}%{_unitdir}/kvm_stat.service
popd
# install VM tools
pushd tools/mm/
install -m755 slabinfo %{buildroot}%{_bindir}/slabinfo
install -m755 page_owner_sort %{buildroot}%{_bindir}/page_owner_sort
popd
pushd tools/verification/rv/
%{tools_make} DESTDIR=%{buildroot} install
popd
pushd tools/tracing/rtla/
%{tools_make} DESTDIR=%{buildroot} install
rm -f %{buildroot}%{_bindir}/hwnoise
rm -f %{buildroot}%{_bindir}/osnoise
rm -f %{buildroot}%{_bindir}/timerlat
(cd %{buildroot}

        ln -sf rtla ./%{_bindir}/hwnoise
        ln -sf rtla ./%{_bindir}/osnoise
        ln -sf rtla ./%{_bindir}/timerlat
)
popd
%endif

%if %{with_selftests}
pushd samples
install -d %{buildroot}%{_libexecdir}/ksamples
# install bpf samples
pushd bpf
install -d %{buildroot}%{_libexecdir}/ksamples/bpf
find -type f -executable -exec install -m755 {} %{buildroot}%{_libexecdir}/ksamples/bpf \;
install -m755 *.sh %{buildroot}%{_libexecdir}/ksamples/bpf
# test_lwt_bpf.sh compiles test_lwt_bpf.c when run; this works only from the
# kernel tree. Just remove it.
rm %{buildroot}%{_libexecdir}/ksamples/bpf/test_lwt_bpf.sh
install -m644 *_kern.o %{buildroot}%{_libexecdir}/ksamples/bpf || true
install -m644 tcp_bpf.readme %{buildroot}%{_libexecdir}/ksamples/bpf
popd
# install pktgen samples
pushd pktgen
install -d %{buildroot}%{_libexecdir}/ksamples/pktgen
find . -type f -executable -exec install -m755 {} %{buildroot}%{_libexecdir}/ksamples/pktgen/{} \;
find . -type f ! -executable -exec install -m644 {} %{buildroot}%{_libexecdir}/ksamples/pktgen/{} \;
popd
popd
# install mm selftests
pushd tools/testing/selftests/mm
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/mm/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/mm/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/mm/{} \;
popd
# install cgroup selftests
pushd tools/testing/selftests/cgroup
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/cgroup/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/cgroup/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/cgroup/{} \;
popd
# install drivers/net selftests
pushd tools/testing/selftests/drivers/net
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/{} \;
popd
# install drivers/net/mlxsw selftests
pushd tools/testing/selftests/drivers/net/mlxsw
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/mlxsw/{} \;
popd
# install drivers/net/hw selftests
pushd tools/testing/selftests/drivers/net/hw
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/hw/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/hw/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/hw/{} \;
popd
# install drivers/net/netdevsim selftests
pushd tools/testing/selftests/drivers/net/netdevsim
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/netdevsim/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/netdevsim/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/netdevsim/{} \;
popd
# install drivers/net/bonding selftests
pushd tools/testing/selftests/drivers/net/bonding
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/drivers/net/bonding/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/bonding/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/drivers/net/bonding/{} \;
popd
# install net/can selftests
pushd tools/testing/selftests/net/can
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/can/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/can/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/can/{} \;
popd
# install net/forwarding selftests
pushd tools/testing/selftests/net/forwarding
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/forwarding/{} \;
popd
# install net/hsr selftests
pushd tools/testing/selftests/net/hsr
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/hsr/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/hsr/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/hsr/{} \;
popd
# install net/mptcp selftests
pushd tools/testing/selftests/net/mptcp
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/mptcp/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/mptcp/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/mptcp/{} \;
popd
# install tc-testing selftests
pushd tools/testing/selftests/tc-testing
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/tc-testing/{} \;
popd
# install net/netfilter selftests
pushd tools/testing/selftests/net/netfilter
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/netfilter/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/netfilter/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/netfilter/{} \;
popd
# install net/packetdrill selftests
pushd tools/testing/selftests/net/packetdrill
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/net/packetdrill/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/net/packetdrill/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/net/packetdrill/{} \;
popd

# install memfd selftests
pushd tools/testing/selftests/memfd
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/memfd/{} \;
popd
# install iommu selftests
pushd tools/testing/selftests/iommu
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/iommu/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/iommu/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/iommu/{} \;
popd
# install rlimits selftests
pushd tools/testing/selftests/rlimits
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/rlimits/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/rlimits/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/rlimits/{} \;
popd
# install pid_namespace selftests
pushd tools/testing/selftests/pid_namespace
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/pid_namespace/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/pid_namespace/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/pid_namespace/{} \;
popd
# install timens selftests
pushd tools/testing/selftests/timens
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/timens/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/timens/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/timens/{} \;
popd
# install pidfd selftests
pushd tools/testing/selftests/pidfd
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/pidfd/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/pidfd/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/pidfd/{} \;
popd
# install capabilities selftests
pushd tools/testing/selftests/capabilities
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/capabilities/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/capabilities/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/capabilities/{} \;
popd
# install clone3 selftests
pushd tools/testing/selftests/clone3
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/clone3/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/clone3/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/clone3/{} \;
popd
# install exec selftests
pushd tools/testing/selftests/exec
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/exec/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/exec/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/exec/{} \;
popd
# install filesystems selftests
pushd tools/testing/selftests/filesystems
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/filesystems/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/filesystems/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/filesystems/{} \;
popd
# install firmware selftests
pushd tools/testing/selftests/firmware
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/firmware/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/firmware/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/firmware/{} \;
popd
# install landlock selftests
pushd tools/testing/selftests/landlock
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/landlock/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/landlock/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/landlock/{} \;
popd
# install mount selftests
pushd tools/testing/selftests/mount
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/mount/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/mount/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/mount/{} \;
popd
# install mount_setattr selftests
pushd tools/testing/selftests/mount_setattr
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/mount_setattr/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/mount_setattr/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/mount_setattr/{} \;
popd
# install move_mount_set_group selftests
pushd tools/testing/selftests/move_mount_set_group
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/move_mount_set_group/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/move_mount_set_group/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/move_mount_set_group/{} \;
popd
# install nsfs selftests
pushd tools/testing/selftests/nsfs
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/nsfs/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/nsfs/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/nsfs/{} \;
popd
# install openat2 selftests
pushd tools/testing/selftests/openat2
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/openat2/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/openat2/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/openat2/{} \;
popd
# install proc selftests
pushd tools/testing/selftests/proc
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/proc/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/proc/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/proc/{} \;
popd
# install safesetid selftests
pushd tools/testing/selftests/safesetid
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/safesetid/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/safesetid/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/safesetid/{} \;
popd
# install seccomp selftests
pushd tools/testing/selftests/seccomp
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/seccomp/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/seccomp/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/seccomp/{} \;
popd
# install tmpfs selftests
pushd tools/testing/selftests/tmpfs
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/tmpfs/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/tmpfs/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/tmpfs/{} \;
popd
# install uevent selftests
pushd tools/testing/selftests/uevent
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/uevent/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/uevent/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/uevent/{} \;
popd
# install vDSO selftests
pushd tools/testing/selftests/vDSO
find -type d -exec install -d %{buildroot}%{_libexecdir}/kselftests/vDSO/{} \;
find -type f -executable -exec install -D -m755 {} %{buildroot}%{_libexecdir}/kselftests/vDSO/{} \;
find -type f ! -executable -exec install -D -m644 {} %{buildroot}%{_libexecdir}/kselftests/vDSO/{} \;
popd
%endif

###
### clean
###

###
### scripts
###

%if %{with_tools}
%post -n %{package_name}-tools-libs
/sbin/ldconfig

%postun -n %{package_name}-tools-libs
/sbin/ldconfig
%endif

#
# This macro defines a %%post script for a kernel*-devel package.
#	%%kernel_devel_post [<subpackage>]
# Note we don't run hardlink if ostree is in use, as ostree is
# a far more sophisticated hardlink implementation.
# https://github.com/projectatomic/rpm-ostree/commit/58a79056a889be8814aa51f507b2c7a4dccee526
#
# The deletion of *.hardlink-temporary files is a temporary workaround
# for this bug in the hardlink binary (fixed in util-linux 2.38):
# https://github.com/util-linux/util-linux/issues/1602
#
%define kernel_devel_post() \
%{expand:%%post %{?1:%{1}-}devel}\
if [ -f /etc/sysconfig/kernel ]\
then\
    . /etc/sysconfig/kernel || exit $?\
fi\
if [ "$HARDLINK" != "no" -a -x /usr/bin/hardlink -a ! -e /run/ostree-booted ] \
then\
    (cd /usr/src/kernels/%{KVERREL}%{?1:+%{1}} &&\
     /usr/bin/find . -type f | while read f; do\
       hardlink -c /usr/src/kernels/*%{?dist}.*/$f $f > /dev/null\
     done;\
     /usr/bin/find /usr/src/kernels -type f -name '*.hardlink-temporary' -delete\
    )\
fi\
%if %{with_cross}\
    echo "Building scripts and resolve_btfids"\
    env --unset=ARCH make -C /usr/src/kernels/%{KVERREL}%{?1:+%{1}} prepare_after_cross\
%endif\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-extra package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_modules_extra_post [<subpackage>]
#
%define kernel_modules_extra_post() \
%{expand:%%post %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-extra}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-internal package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_modules_internal_post [<subpackage>]
#
%define kernel_modules_internal_post() \
%{expand:%%post %{?1:%{1}-}modules-internal}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-internal}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-partner package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_modules_partner_post [<subpackage>]
#
%define kernel_modules_partner_post() \
%{expand:%%post %{?1:%{1}-}modules-partner}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules-partner}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules package.
# It also defines a %%postun script that does the same thing.
#	%%kernel_modules_post [<subpackage>]
#
%define kernel_modules_post() \
%{expand:%%post %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
if [ ! -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL}%{?1:+%{1}} ]; then\
	mkdir -p %{_localstatedir}/lib/rpm-state/%{name}\
	touch %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}%{?1:+%{1}}\
fi\
%{nil}\
%{expand:%%postun %{?1:%{1}-}modules}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}\
%{expand:%%posttrans %{?1:%{1}-}modules}\
if [ -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}%{?1:+%{1}} ]; then\
	rm -f %{_localstatedir}/lib/rpm-state/%{name}/need_to_run_dracut_%{KVERREL}%{?1:+%{1}}\
	echo "Running: dracut -f --kver %{KVERREL}%{?1:+%{1}}"\
	dracut -f --kver "%{KVERREL}%{?1:+%{1}}" || exit $?\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel*-modules-core package.
#	%%kernel_modules_core_post [<subpackage>]
#
%define kernel_modules_core_post() \
%{expand:%%posttrans %{?1:%{1}-}modules-core}\
/sbin/depmod -a %{KVERREL}%{?1:+%{1}}\
%{nil}

# This macro defines a %%posttrans script for a kernel package.
#	%%kernel_variant_posttrans [-v <subpackage>] [-u uki-suffix]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_posttrans(v:u:) \
%{expand:%%posttrans %{?-v:%{-v*}-}%{!?-u*:core}%{?-u*:uki-%{-u*}}}\
%if 0%{!?fedora:1}\
%if !%{with_automotive}\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --add-kernel %{KVERREL}%{?-v:+%{-v*}} || exit $?\
fi\
%endif\
%endif\
rm -f %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL}%{?-v:+%{-v*}}\
/bin/kernel-install add %{KVERREL}%{?-v:+%{-v*}} /lib/modules/%{KVERREL}%{?-v:+%{-v*}}/vmlinuz%{?-u:-%{-u*}.efi} || exit $?\
if [[ ! -e "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext" ]]; then\
    cp "/lib/modules/%{KVERREL}%{?-v:+%{-v*}}/symvers.%compext" "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext"\
    if command -v restorecon &>/dev/null; then\
        restorecon "/boot/symvers-%{KVERREL}%{?-v:+%{-v*}}.%compext"\
    fi\
fi\
%{nil}

#
# This macro defines a %%post script for a kernel package and its devel package.
#	%%kernel_variant_post [-v <subpackage>] [-r <replace>]
# More text can follow to go at the end of this variant's %%post.
#
%define kernel_variant_post(v:r:) \
%{expand:%%kernel_devel_post %{?-v*}}\
%{expand:%%kernel_modules_post %{?-v*}}\
%{expand:%%kernel_modules_core_post %{?-v*}}\
%{expand:%%kernel_modules_extra_post %{?-v*}}\
%{expand:%%kernel_modules_internal_post %{?-v*}}\
%if 0%{!?fedora:1}\
%{expand:%%kernel_modules_partner_post %{?-v*}}\
%endif\
%{expand:%%kernel_variant_posttrans %{?-v*:-v %{-v*}}}\
%{expand:%%post %{?-v*:%{-v*}-}core}\
%{-r:\
if [ `uname -i` == "x86_64" -o `uname -i` == "i386" ] &&\
   [ -f /etc/sysconfig/kernel ]; then\
  /bin/sed -r -i -e 's/^DEFAULTKERNEL=%{-r*}$/DEFAULTKERNEL=kernel%{?-v:-%{-v*}}/' /etc/sysconfig/kernel || exit $?\
fi}\
mkdir -p %{_localstatedir}/lib/rpm-state/%{name}\
touch %{_localstatedir}/lib/rpm-state/%{name}/installing_core_%{KVERREL}%{?-v:+%{-v*}}\
%{nil}

#
# This macro defines a %%preun script for a kernel package.
#	%%kernel_variant_preun [-v <subpackage>] -u [uki-suffix] -e
# Add kernel-install's --entry-type=type1|type2|all option (if supported) to limit removal
# to a specific boot entry type.
#
%define kernel_variant_preun(v:u:e) \
%{expand:%%preun %{?-v:%{-v*}-}%{!?-u*:core}%{?-u*:uki-%{-u*}}}\
entry_type=""\
%{-e: \
/bin/kernel-install --help|grep -q -- '--entry-type=' &&\
    entry_type="--entry-type %{!?-u:type1}%{?-u:type2}" \
}\
/bin/kernel-install remove %{KVERREL}%{?-v:+%{-v*}} $entry_type || exit $?\
%if !%{with_automotive}\
if [ -x %{_sbindir}/weak-modules ]\
then\
    %{_sbindir}/weak-modules --remove-kernel %{KVERREL}%{?-v:+%{-v*}} || exit $?\
fi\
%endif\
%{nil}

%if %{with_up_base} && %{with_efiuki}
%kernel_variant_posttrans -u virt
%kernel_variant_preun -u virt -e
%endif

%if %{with_up_base}
%kernel_variant_preun -e
%kernel_variant_post
%endif

%if %{with_zfcpdump}
%kernel_variant_preun -v zfcpdump
%kernel_variant_post -v zfcpdump
%endif

%if %{with_up} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v debug -u virt
%kernel_variant_preun -v debug -u virt -e
%endif

%if %{with_up} && %{with_debug}
%kernel_variant_preun -v debug -e
%kernel_variant_post -v debug
%endif

%if %{with_arm64_16k_base}
%kernel_variant_preun -v 16k -e
%kernel_variant_post -v 16k
%endif

%if %{with_debug} && %{with_arm64_16k}
%kernel_variant_preun -v 16k-debug -e
%kernel_variant_post -v 16k-debug
%endif

%if %{with_arm64_16k} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v 16k-debug -u virt
%kernel_variant_preun -v 16k-debug -u virt -e
%endif

%if %{with_arm64_16k_base} && %{with_efiuki}
%kernel_variant_posttrans -v 16k -u virt
%kernel_variant_preun -v 16k -u virt -e
%endif

%if %{with_arm64_64k_base}
%kernel_variant_preun -v 64k -e
%kernel_variant_post -v 64k
%endif

%if %{with_debug} && %{with_arm64_64k}
%kernel_variant_preun -v 64k-debug -e
%kernel_variant_post -v 64k-debug
%endif

%if %{with_arm64_64k} && %{with_debug} && %{with_efiuki}
%kernel_variant_posttrans -v 64k-debug -u virt
%kernel_variant_preun -v 64k-debug -u virt -e
%endif

%if %{with_arm64_64k_base} && %{with_efiuki}
%kernel_variant_posttrans -v 64k -u virt
%kernel_variant_preun -v 64k -u virt -e
%endif

%if %{with_realtime_base}
%kernel_variant_preun -v rt
%kernel_variant_post -v rt -r kernel
%endif

%if %{with_automotive_base}
%kernel_variant_preun -v automotive
%kernel_variant_post -v automotive -r kernel
%endif

%if %{with_realtime} && %{with_debug}
%kernel_variant_preun -v rt-debug
%kernel_variant_post -v rt-debug
%endif

%if %{with_realtime_arm64_64k_base}
%kernel_variant_preun -v rt-64k
%kernel_variant_post -v rt-64k
%kernel_kvm_post rt-64k
%endif

%if %{with_debug} && %{with_realtime_arm64_64k}
%kernel_variant_preun -v rt-64k-debug
%kernel_variant_post -v rt-64k-debug
%kernel_kvm_post rt-64k-debug
%endif

%if %{with_automotive} && %{with_debug} && !%{with_automotive_build}
%kernel_variant_preun -v automotive-debug
%kernel_variant_post -v automotive-debug
%endif

###
### file lists
###

%if %{with_headers}
%files headers
/usr/include/*
%exclude %{_includedir}/cpufreq.h
%if %{with_ynl}
%exclude %{_includedir}/ynl
%endif
%endif

%if %{with_cross_headers}
%files cross-headers
/usr/*-linux-gnu/include/*
%endif

%if %{with_kernel_abi_stablelists}
%files -n %{package_name}-abi-stablelists
/lib/modules/kabi-*
%endif

%if %{with_kabidw_base}
%ifarch x86_64 s390x ppc64 ppc64le aarch64 riscv64
%files kernel-kabidw-base-internal
%defattr(-,root,root)
/kabidw-base/%{_target_cpu}/*
%endif
%endif

# only some architecture builds need kernel-doc
%if %{with_doc}
%files doc
%defattr(-,root,root)
%{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}/Documentation/*
%dir %{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}/Documentation
%dir %{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}
%{_datadir}/doc/kernel-doc-%{specversion}-%{pkgrelease}/kernel.changelog.xz
%endif

%if %{with_perf}
%files -n perf
%{_bindir}/perf
%{_libdir}/libperf-jvmti.so
%dir %{_libexecdir}/perf-core
%{_libexecdir}/perf-core/*
%{_mandir}/man[1-8]/perf*
%{_sysconfdir}/bash_completion.d/perf
%doc linux-%{KVERREL}/tools/perf/Documentation/examples.txt
%{_docdir}/perf-tip/tips.txt
%{_includedir}/perf/perf_dlfilter.h

%files -n python3-perf
%{python3_sitearch}/perf*

%if %{with_debuginfo}
%files -f perf-debuginfo.list -n perf-debuginfo

%files -f python3-perf-debuginfo.list -n python3-perf-debuginfo
%endif
# with_perf
%endif

%if %{with_libperf}
%files -n libperf
%{_libdir}/libperf.so.0
%{_libdir}/libperf.so.0.0.1

%files -n libperf-devel
%{_libdir}/libperf.so
%{_libdir}/pkgconfig/libperf.pc
%{_includedir}/internal/*.h
%{_includedir}/perf/bpf_perf.h
%{_includedir}/perf/core.h
%{_includedir}/perf/cpumap.h
%{_includedir}/perf/event.h
%{_includedir}/perf/evlist.h
%{_includedir}/perf/evsel.h
%{_includedir}/perf/mmap.h
%{_includedir}/perf/threadmap.h
%{_mandir}/man3/libperf.3.gz
%{_mandir}/man7/libperf-counting.7.gz
%{_mandir}/man7/libperf-sampling.7.gz
%{_docdir}/libperf/examples/sampling.c
%{_docdir}/libperf/examples/counting.c
%{_docdir}/libperf/html/libperf.html
%{_docdir}/libperf/html/libperf-counting.html
%{_docdir}/libperf/html/libperf-sampling.html

%if %{with_debuginfo}
%files -f libperf-debuginfo.list -n libperf-debuginfo
%endif

# with_libperf
%endif


%if %{with_tools}
%ifnarch %{cpupowerarchs}
%files -n %{package_name}-tools
%else
%files -n %{package_name}-tools -f cpupower.lang
%{_bindir}/cpupower
%{_libexecdir}/cpupower
%{_unitdir}/cpupower.service
%config(noreplace) %{_sysconfdir}/cpupower-service.conf
%{_datadir}/bash-completion/completions/cpupower
%ifarch x86_64
%{_bindir}/centrino-decode
%{_bindir}/powernow-k8-decode
%endif
%{_mandir}/man[1-8]/cpupower*
%ifarch x86_64
%{_bindir}/x86_energy_perf_policy
%{_mandir}/man8/x86_energy_perf_policy*
%{_bindir}/turbostat
%{_mandir}/man8/turbostat*
%{_bindir}/intel-speed-select
%{_sbindir}/intel_sdsi
%endif
# cpupowerarchs
%endif
%{_bindir}/tmon
%{_bindir}/bootconfig
%{_bindir}/iio_event_monitor
%{_bindir}/iio_generic_buffer
%{_bindir}/lsiio
%{_bindir}/lsgpio
%{_bindir}/gpio-hammer
%{_bindir}/gpio-event-mon
%{_bindir}/gpio-watch
%{_mandir}/man1/kvm_stat*
%{_bindir}/kvm_stat
%{_unitdir}/kvm_stat.service
%config(noreplace) %{_sysconfdir}/logrotate.d/kvm_stat
%{_bindir}/page_owner_sort
%{_bindir}/slabinfo
%if %{with_ynl}
%{_bindir}/ynl*
%{_docdir}/ynl
%{_datadir}/ynl
%{python3_sitelib}/pyynl*
%endif

%if %{with_debuginfo}
%files -f %{package_name}-tools-debuginfo.list -n %{package_name}-tools-debuginfo
%endif

%files -n %{package_name}-tools-libs
%ifarch %{cpupowerarchs}
%{_libdir}/libcpupower.so.1
%{_libdir}/libcpupower.so.1.0.1
%endif

%files -n %{package_name}-tools-libs-devel
%ifarch %{cpupowerarchs}
%{_libdir}/libcpupower.so
%{_includedir}/cpufreq.h
%{_includedir}/cpuidle.h
%{_includedir}/powercap.h
# libcpupower Python bindings
%{python3_sitearch}/_raw_pylibcpupower.so
%{python3_sitearch}/raw_pylibcpupower.py
%{python3_sitearch}/__pycache__/raw_pylibcpupower*

%endif
%if %{with_ynl}
%{_libdir}/libynl*
%{_includedir}/ynl
%endif

%files -n rtla
%{_bindir}/rtla
%{_bindir}/hwnoise
%{_bindir}/osnoise
%{_bindir}/timerlat
%{_mandir}/man1/rtla-hwnoise.1.gz
%{_mandir}/man1/rtla-osnoise-hist.1.gz
%{_mandir}/man1/rtla-osnoise-top.1.gz
%{_mandir}/man1/rtla-osnoise.1.gz
%{_mandir}/man1/rtla-timerlat-hist.1.gz
%{_mandir}/man1/rtla-timerlat-top.1.gz
%{_mandir}/man1/rtla-timerlat.1.gz
%{_mandir}/man1/rtla.1.gz

%files -n rv
%{_bindir}/rv
%{_mandir}/man1/rv-list.1.gz
%{_mandir}/man1/rv-mon-wip.1.gz
%{_mandir}/man1/rv-mon-wwnr.1.gz
%{_mandir}/man1/rv-mon.1.gz
%{_mandir}/man1/rv-mon-sched.1.gz
%{_mandir}/man1/rv.1.gz

# with_tools
%endif

%if %{with_selftests}
%files selftests-internal
%{_libexecdir}/ksamples
%{_libexecdir}/kselftests
%endif

# empty meta-package
%if %{with_up_base}
%ifnarch %nobuildarches noarch
%files
%endif
%endif

# This is %%{image_install_path} on an arch where that includes ELF files,
# or empty otherwise.
%define elf_image_install_path %{?kernel_image_elf:%{image_install_path}}

#
# This macro defines the %%files sections for a kernel package
# and its devel and debuginfo packages.
#	%%kernel_variant_files [-k vmlinux] <use_vdso> <condition> <subpackage>
#
%define kernel_variant_files(k:) \
%if %{2}\
%{expand:%%files %{?1:-f kernel-%{?3:%{3}-}ldsoconf.list} %{?3:%{3}-}core}\
%{!?_licensedir:%global license %%doc}\
%%license linux-%{KVERREL}/COPYING-%{version}-%{release}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}\
%ghost /%{image_install_path}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/.vmlinuz.hmac \
%ghost /%{image_install_path}/.vmlinuz-%{KVERREL}%{?3:+%{3}}.hmac \
%ifarch aarch64 riscv64\
/lib/modules/%{KVERREL}%{?3:+%{3}}/dtb \
%ghost /%{image_install_path}/dtb-%{KVERREL}%{?3:+%{3}} \
%endif\
/lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
%ghost /boot/System.map-%{KVERREL}%{?3:+%{3}}\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/symvers.%compext\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin*\
%ghost %attr(0644, root, root) /boot/symvers-%{KVERREL}%{?3:+%{3}}.%compext\
%ghost %attr(0600, root, root) /boot/initramfs-%{KVERREL}%{?3:+%{3}}.img\
%ghost %attr(0644, root, root) /boot/config-%{KVERREL}%{?3:+%{3}}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-core.list %{?3:%{3}-}modules-core}\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}/kernel\
/lib/modules/%{KVERREL}%{?3:+%{3}}/build\
/lib/modules/%{KVERREL}%{?3:+%{3}}/source\
/lib/modules/%{KVERREL}%{?3:+%{3}}/updates\
/lib/modules/%{KVERREL}%{?3:+%{3}}/weak-updates\
/lib/modules/%{KVERREL}%{?3:+%{3}}/systemtap\
%{_datadir}/doc/kernel-keys/%{KVERREL}%{?3:+%{3}}\
%if %{1}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/vdso\
%endif\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.block\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.drm\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.modesetting\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.networking\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.order\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.alias\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.alias.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin.alias.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.dep\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.dep.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.devname\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.softdep\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.symbols\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.symbols.bin\
%ghost %attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/modules.weakdep\
%{expand:%%files -f kernel-%{?3:%{3}-}modules.list %{?3:%{3}-}modules}\
%{expand:%%files %{?3:%{3}-}devel}\
%defverify(not mtime)\
/usr/src/kernels/%{KVERREL}%{?3:+%{3}}\
%{expand:%%files %{?3:%{3}-}devel-matched}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-extra.list %{?3:%{3}-}modules-extra}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-internal.list %{?3:%{3}-}modules-internal}\
%if 0%{!?fedora:1}\
%{expand:%%files -f kernel-%{?3:%{3}-}modules-partner.list %{?3:%{3}-}modules-partner}\
%endif\
%if %{with_debuginfo}\
%ifnarch noarch\
%{expand:%%files -f debuginfo%{?3}.list %{?3:%{3}-}debuginfo}\
%endif\
%endif\
%if %{with_efiuki} && "%{3}" != "rt" && "%{3}" != "rt-debug" && "%{3}" != "rt-64k" && "%{3}" != "rt-64k-debug"\
%{expand:%%files %{?3:%{3}-}uki-virt}\
%dir /lib/modules\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}\
/lib/modules/%{KVERREL}%{?3:+%{3}}/System.map\
/lib/modules/%{KVERREL}%{?3:+%{3}}/symvers.%compext\
/lib/modules/%{KVERREL}%{?3:+%{3}}/config\
/lib/modules/%{KVERREL}%{?3:+%{3}}/modules.builtin*\
%attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi\
%attr(0644, root, root) /lib/modules/%{KVERREL}%{?3:+%{3}}/.%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi.hmac\
%ghost /%{image_install_path}/efi/EFI/Linux/%{?-k:%{-k*}}%{!?-k:*}-%{KVERREL}%{?3:+%{3}}.efi\
%{expand:%%files %{?3:%{3}-}uki-virt-addons}\
%dir /lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi.extra.d/ \
/lib/modules/%{KVERREL}%{?3:+%{3}}/%{?-k:%{-k*}}%{!?-k:vmlinuz}-virt.efi.extra.d/*.addon.efi\
%endif\
%if %{?3:1} %{!?3:0}\
%{expand:%%files %{3}}\
%endif\
%if %{with_gcov}\
%ifnarch %nobuildarches noarch\
%{expand:%%files -f kernel-%{?3:%{3}-}gcov.list %{?3:%{3}-}gcov}\
%endif\
%endif\
%endif\
%{nil}

%kernel_variant_files %{_use_vdso} %{with_up_base}
%if %{with_up}
%kernel_variant_files %{_use_vdso} %{with_debug} debug
%endif
%if %{with_arm64_16k}
%kernel_variant_files %{_use_vdso} %{with_debug} 16k-debug
%endif
%if %{with_arm64_64k}
%kernel_variant_files %{_use_vdso} %{with_debug} 64k-debug
%endif
%kernel_variant_files %{_use_vdso} %{with_realtime_base} rt
%if %{with_realtime}
%kernel_variant_files %{_use_vdso} %{with_debug} rt-debug
%endif
%kernel_variant_files %{_use_vdso} %{with_automotive_base} automotive
%if %{with_automotive} && !%{with_automotive_build}
%kernel_variant_files %{_use_vdso} %{with_debug} automotive-debug
%endif

%if %{with_debug_meta}
%files debug
%files debug-core
%files debug-devel
%files debug-devel-matched
%files debug-modules
%files debug-modules-core
%files debug-modules-extra
%if %{with_arm64_16k}
%files 16k-debug
%files 16k-debug-core
%files 16k-debug-devel
%files 16k-debug-devel-matched
%files 16k-debug-modules
%files 16k-debug-modules-extra
%endif
%if %{with_arm64_64k}
%files 64k-debug
%files 64k-debug-core
%files 64k-debug-devel
%files 64k-debug-devel-matched
%files 64k-debug-modules
%files 64k-debug-modules-extra
%endif
%endif
%kernel_variant_files %{_use_vdso} %{with_zfcpdump} zfcpdump
%kernel_variant_files %{_use_vdso} %{with_arm64_16k_base} 16k
%kernel_variant_files %{_use_vdso} %{with_arm64_64k_base} 64k
%kernel_variant_files %{_use_vdso} %{with_realtime_arm64_64k_base} rt-64k
%if %{with_realtime_arm64_64k}
%kernel_variant_files %{_use_vdso} %{with_debug} rt-64k-debug
%endif

%ifnarch noarch %{nobuildarches}
%files modules-extra-matched
%endif

# plz don't put in a version string unless you're going to tag
# and build.
#
#
%changelog
* Thu Feb 19 2026 Augusto Caringi <acaringi@redhat.com> [6.18.13-0]
- Linux v6.18.13

* Mon Feb 16 2026 Justin M. Forbes <jforbes@fedoraproject.org> [6.18.12-0]
- Linux v6.18.12

* Wed Feb 11 2026 Augusto Caringi <acaringi@redhat.com> [6.18.10-0]
- Linux v6.18.10

* Fri Feb 06 2026 Augusto Caringi <acaringi@redhat.com> [6.18.9-0]
- Add a couple of bzs to be fixed with the 6.18.9 build (Justin M. Forbes)
- media: ipu-bridge: Add DMI quirk for Dell XPS laptops with upside down sensors (Hans de Goede)
- media: ov02c10: Remove unnecessary hflip and vflip pointers (Hans de Goede)
- media: ov02c10: Fix the horizontal flip control (Hans de Goede)
- media: ov02c10: Adjust x-win/y-win when changing flipping to preserve bayer-pattern (Hans de Goede)
- media: ov02c10: Fix bayer-pattern change after default vflip change (Hans de Goede)
- media: ov02c10: Support hflip and vflip (Sebastian Reichel)
- media: ov02c10: Fix default vertical flip (Sebastian Reichel)
- Linux v6.18.9

* Fri Jan 30 2026 Augusto Caringi <acaringi@redhat.com> [6.18.8-0]
- Linux v6.18.8

* Fri Jan 23 2026 Augusto Caringi <acaringi@redhat.com> [6.18.7-0]
- Fix up the configs for CONFIG_DEVICE_PRIVATE (Justin M. Forbes)
- Linux v6.18.7

* Sun Jan 18 2026 Justin M. Forbes <jforbes@fedoraproject.org> [6.18.6-0]
- Conifg update for 6.18.6 backports (Justin M. Forbes)
- fedora: aarch64: Enable TI_SCI_INTR_IRQCHIP as built-in (Ayush Singh)
- Backport of Intel ISH HID patches to support sensors on Lenovo platforms (Vishnu Sankar) [2428677]
- Backport of Intel ISH HID patches to support sensors on Lenovo platforms (Vishnu Sankar) [2428677]
- Linux v6.18.6

* Sun Jan 11 2026 Justin M. Forbes <jforbes@fedoraproject.org> [6.18.5-0]
- erofs: fix file-backed mounts no longer working on EROFS partitions (Gao Xiang)
- erofs: don't bother with s_stack_depth increasing for now (Gao Xiang)
- Linux v6.18.5

* Thu Jan 08 2026 Justin M. Forbes <jforbes@fedoraproject.org> [6.18.4-0]
- Linux v6.18.4

* Fri Jan 02 2026 Justin M. Forbes <jforbes@fedoraproject.org> [6.18.3-0]
- Config update due to stable patches (Justin M. Forbes)
- wifi: iwlwifi: Fix firmware version handling (Ville Syrjälä)
- Linux v6.18.3

* Thu Dec 18 2025 Justin M. Forbes <jforbes@fedoraproject.org> [6.18.2-0]
- Add new configs for 6.18.2 (Justin M. Forbes)
- Linux v6.18.2

* Sat Dec 13 2025 Justin M. Forbes <jforbes@fedoraproject.org> [6.18.1-0]
- Initial setup for stable Fedora releases (Justin M. Forbes)
- Reset RHEL_RELEASE for the 6.19 cycle (Justin M. Forbes)
- add libasan-static and libubsan as BR for selftests (Thorsten Leemhuis)
- add liburing-devel as BR for selftests (Thorsten Leemhuis)
- add a few optional BRs for perf (Thorsten Leemhuis)
- Linux v6.18.1

* Mon Dec 01 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-64]
- Linux v6.18.0

* Sun Nov 30 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc7.6bda50f4333f.63]
- Consolidate configs into common for 6.18 (Justin M. Forbes)
- Linux v6.18.0-0.rc7.6bda50f4333f

* Sat Nov 29 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc7.19eef1d98eed.62]
- Linux v6.18.0-0.rc7.19eef1d98eed

* Fri Nov 28 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc7.e538109ac71d.61]
- Linux v6.18.0-0.rc7.e538109ac71d

* Thu Nov 27 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc7.765e56e41a5a.60]
- redhat/configs: make CONFIG_DRM_CLIENT_LIB=y (Jocelyn Falempe)
- Linux v6.18.0-0.rc7.765e56e41a5a

* Wed Nov 26 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc7.30f09200cc4a.59]
- Linux v6.18.0-0.rc7.30f09200cc4a

* Tue Nov 25 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc7.58]
- fedora: arm: minor config updates (Peter Robinson)

* Mon Nov 24 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc7.57]
- Linux v6.18.0-0.rc7

* Sun Nov 23 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc6.d13f3ac64efb.56]
- Linux v6.18.0-0.rc6.d13f3ac64efb

* Sat Nov 22 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc6.2eba5e05d9bc.55]
- Linux v6.18.0-0.rc6.2eba5e05d9bc

* Fri Nov 21 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc6.fd95357fd8c6.54]
- Change RZ_DMAC from m to y for Fedora (Justin M. Forbes)
- redhat/configs: automotive: enable CAN_FLEXCAN (Jared Kangas)
- Linux v6.18.0-0.rc6.fd95357fd8c6

* Thu Nov 20 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc6.23cb64fb7625.53]
- Revert "Removing Obsolete hba pci-ids from rhel8" (Scott Weaver)
- rh_messages.h: add missing lpfc devices (Scott Weaver)
- redhat/configs: Enable CONFIG_NFSD_V4_2_INTER_SSC in RHEL (Scott Mayhew)
- redhat: Package net/hsr selftests (Felix Maurer)
- Remove redundant Fedora VFIO overrides (Daniel P. Berrangé)
- Enable CONFIG_VFIO_DEVICE_CDEV on Fedora (Daniel P. Berrangé)
- redhat/configs: automotive: enable I2C_IMX and dependencies (Jared Kangas)
- Linux v6.18.0-0.rc6.23cb64fb7625

* Wed Nov 19 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc6.8b690556d8fe.52]
- Set some late arrival config options for Fedora 6.18 (Justin M. Forbes)
- Linux v6.18.0-0.rc6.8b690556d8fe

* Tue Nov 18 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc6.e7c375b18160.51]
- Linux v6.18.0-0.rc6.e7c375b18160

* Mon Nov 17 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc6.50]
- Linux v6.18.0-0.rc6

* Sun Nov 16 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc5.f824272b6e3f.49]
- redhat/configs: enable Micel PHY for NXP Automotive SoCs S32G2xx/S32G3xx/S32R45 (Alessandro Carminati)
- redhat/configs: enable Synopsis DWMAC IP on NXP Automotive SoCs S32G2xx/S32G3xx/S32R45 (Alessandro Carminati)
- Linux v6.18.0-0.rc5.f824272b6e3f

* Sat Nov 15 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc5.7a0892d2836e.48]
- Linux v6.18.0-0.rc5.7a0892d2836e

* Fri Nov 14 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc5.6da43bbeb691.47]
- Linux v6.18.0-0.rc5.6da43bbeb691

* Thu Nov 13 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc5.6fa9041b7177.46]
- redhat/configs: Move CONFIG_MICROCODE_DBG to common/generic/x86 (Waiman Long)
- redhat/configs: Set CONFIG_SCHED_PROXY_EXEC=n (Waiman Long)
- Linux v6.18.0-0.rc5.6fa9041b7177

* Wed Nov 12 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc5.24172e0d7990.45]
- Add loongarch to kernel-headers for Fedora (Justin M. Forbes)
- Linux v6.18.0-0.rc5.24172e0d7990

* Tue Nov 11 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc5.4427259cc7f7.44]
- Turn on SYNTH_EVENTS for RISCV RHEL to avoid a mismatch (Justin M. Forbes)
- Turn on PCI_PWRCTRL_SLOT for aarch64 in RHEL (Justin M. Forbes)
- redhat/kernel.spec.template: add net/can kselftests (Davide Caratti)
- redhat/configs: Enable CONFIG_OVMF_DEBUG_LOG in RHEL (Lenny Szubowicz) [RHEL-100104]
- Linux v6.18.0-0.rc5.4427259cc7f7

* Mon Nov 10 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc5.43]
- Linux v6.18.0-0.rc5

* Sun Nov 09 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc4.439fc29dfd3b.42]
- Linux v6.18.0-0.rc4.439fc29dfd3b

* Sat Nov 08 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc4.e811c33b1f13.41]
- Linux v6.18.0-0.rc4.e811c33b1f13

* Fri Nov 07 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc4.4a0c9b339199.40]
- Linux v6.18.0-0.rc4.4a0c9b339199

* Thu Nov 06 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc4.dc77806cf3b4.39]
- merge-linux-next: use gitlab remote (Scott Weaver)
- Linux v6.18.0-0.rc4.dc77806cf3b4

* Wed Nov 05 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc4.1c353dc8d962.38]
- redhat: use RELEASE_LOCALVERSION also for dist-get-tag (Jan Stancek)
- Linux v6.18.0-0.rc4.1c353dc8d962

* Tue Nov 04 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc4.c9cfc122f037.37]
- redhat: configs: rhel: Enable OV08X40 sensor to support Intel MIPI camera (Kate Hsuan)
- redhat: configs: rhel: Enable usbio-drivers to supower Intel MIPI camera (Kate Hsuan)
- Linux v6.18.0-0.rc4.c9cfc122f037

* Mon Nov 03 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc4.36]
- redhat: configs: Enable DWC3 Generic Platform Driver on RHEL automotive (Desnes Nunes) [RHEL-119326]
- redhat: configs: Enable OV08X40 sensor driver on RHEL (Desnes Nunes) [RHEL-119326]
- redhat: configs: Enable USBIO Bridge support on RHEL x86 (Desnes Nunes) [RHEL-119326]
- gitlab-ci: testing (Scott Weaver)
- ark-linux-next: check for git hooks directory (Scott Weaver)
- gitlab-ci: merge-linux-next: workaround pydantic-core build error (Scott Weaver)
- Linux v6.18.0-0.rc4

* Sun Nov 02 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc3.691d401c7e0e.35]
- Linux v6.18.0-0.rc3.691d401c7e0e

* Sat Nov 01 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc3.ba36dd5ee6fd.34]
- redhat: remove EARLY ystream bits (Jan Stancek)
- Linux v6.18.0-0.rc3.ba36dd5ee6fd

* Fri Oct 31 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc3.d127176862a9.33]
- redhat/configs:  configure CONFIG_ATH12K_AHB for rhel (Jose Ignacio Tornos Martinez)
- Final configs for Fedora 6.18 (Justin M. Forbes)
- Linux v6.18.0-0.rc3.d127176862a9

* Thu Oct 30 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc3.e53642b87a4f.32]
- redhat/configs: Enable additional RV monitors on debug kernels (Gabriele Monaco)
- redhat/configs: Enable sched and rtapp RV monitors (Gabriele Monaco)
- redhat/configs: Move CONFIG_RV_PER_TASK_MONITORS to common/generic (Gabriele Monaco)
- properly reset CONFIG_EFI_SBAT_FILE value (Thorsten Leemhuis)

* Wed Oct 29 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc3.e53642b87a4f.31]
- kernel: extend rh_waived to cope better with the CVE mitigations case (Ricardo Robaina) [RHEL-122979]
- Linux v6.18.0-0.rc3.e53642b87a4f

* Tue Oct 28 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc3.fd57572253bc.30]
- Linux v6.18.0-0.rc3.fd57572253bc

* Mon Oct 27 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc3.29]
- Linux v6.18.0-0.rc3

* Sun Oct 26 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc2.72761a7e3122.28]
- Linux v6.18.0-0.rc2.72761a7e3122

* Sat Oct 25 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc2.566771afc7a8.27]
- uki-virt: add systemd-repart module (Emanuele Giuseppe Esposito)
- fedora: cleanup/de-dupe the USB configfs options (Peter Robinson)
- fedora: cleanup/de-dupe the USB Device/Gadget config (Peter Robinson)
- fedora: Disable the remanents of legacy USB gadget (Peter Robinson)
- fedora: i3c: enable more i3c (Peter Robinson)
- Configs: Mark SCHED_MC as enabled for powerpc (Phil Auld)
- redhat: update self-test-data for RELEASE_LOCALVERSION (Jan Stancek)
- redhat: introduce RELEASE_LOCALVERSION variable (Jan Stancek)
- Turn on CONFIG_DEBUG_INFO_COMPRESSED_ZLIB (Lianbo Jiang)
- Linux v6.18.0-0.rc2.566771afc7a8

* Fri Oct 24 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc2.6fab32bb6508.26]
- Linux v6.18.0-0.rc2.6fab32bb6508

* Thu Oct 23 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc2.43e9ad0c55a3.25]
- Linux v6.18.0-0.rc2.43e9ad0c55a3

* Wed Oct 22 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc2.552c50713f27.24]
- Linux v6.18.0-0.rc2.552c50713f27

* Tue Oct 21 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc2.6548d364a3e8.23]
- redhat/kernel.spec: make python3-perf glob more specific (Jan Stancek)
- Linux v6.18.0-0.rc2.6548d364a3e8

* Mon Oct 20 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc2.22]
- Linux v6.18.0-0.rc2

* Sun Oct 19 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc1.1c64efcb083c.21]
- Linux v6.18.0-0.rc1.1c64efcb083c

* Sat Oct 18 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc1.f406055cb18c.20]
- Linux v6.18.0-0.rc1.f406055cb18c

* Fri Oct 17 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc1.98ac9cc4b445.19]
- fedora: arm64: Updates for AMD Xilinx devices (Peter Robinson)
- Linux v6.18.0-0.rc1.98ac9cc4b445

* Thu Oct 16 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc1.7ea30958b305.18]
- redhat/configs: Re-enable Raspberry Pi support in automotive (Radu Rendec)
- Linux v6.18.0-0.rc1.7ea30958b305

* Wed Oct 15 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc1.9b332cece987.17]
- redhat/configs: automotive: enable FSL_EDMA (Jared Kangas)
- Trim changelog of dupes for the 6.18 reset (Justin M. Forbes)
- Linux v6.18.0-0.rc1.9b332cece987

* Tue Oct 14 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc1.16]
- fedora: aarch64: Enable arm MHUv2 driver (Peter Robinson)
- redhat/configs: automotive: enable RTC_DRV_S32G (Jared Kangas)
- redhat/configs: automotive: switch ufs-qcom to module (Eric Chanudet)
- redhat/configs: automotive: switch geni-se and serial-qcom-geni to modules (Eric Chanudet)
- redhat/configs: automotive: switch pinctrl_msm and pinctrl_sa8775p to modules (Eric Chanudet)
- redhat: add all namespace-dependent selftests to kernel-selftests-internal (Joel Savitz)
- fedora: Minor QCom configs cleanup (Peter Robinson)
- fedora: cleanup now removed BCACHEFS options (Peter Robinson)
- fedora: Last updates for 6.18 (Peter Robinson)

* Mon Oct 13 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc1.15]
- Turn on X86_FRED for Fedora (Justin M. Forbes)
- Linux v6.18.0-0.rc1

* Sun Oct 12 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.0739473694c4.14]
- Fix up HYPERV configs for 6.18 (Justin M. Forbes)
- add xxd to as BuildRequire for bpf selftests (Thorsten Leemhuis)

* Sat Oct 11 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.0739473694c4.13]
- Linux v6.18.0-0.rc0.0739473694c4

* Fri Oct 10 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.5472d60c129f.12]
- Flip HID_HAPTIC to inline for Fedora due to symbol errors (Justin M. Forbes)
- Linux v6.18.0-0.rc0.5472d60c129f

* Thu Oct 09 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.ec714e371f22.11]
- fedora: updates for 6.18 (Peter Robinson)
- Linux v6.18.0-0.rc0.ec714e371f22

* Wed Oct 08 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.0d97f2067c16.10]
- redhat/configs: automotive: enable SPI_OMAP24XX as a module (Jared Kangas)
- Linux v6.18.0-0.rc0.0d97f2067c16

* Tue Oct 07 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.c746c3b51698.9]
- Fix up mismatch with PCI_PWRCTRL_SLOT on arm (Justin M. Forbes)
- Linux v6.18.0-0.rc0.c746c3b51698

* Tue Oct 07 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.fd94619c4336.8]
- Turn on DRM_ACCEL_ROCKET FOR Fedora (Justin M. Forbes)

* Mon Oct 06 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.fd94619c4336.7]
- Linux v6.18.0-0.rc0.fd94619c4336

* Sat Oct 04 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.cbf33b8e0b36.6]
- redhat: rpminspect: update emptyrpm list for kernel variants (Patrick Talbert)
- Linux v6.18.0-0.rc0.cbf33b8e0b36

* Fri Oct 03 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.e406d57be7bd.5]
- Linux v6.18.0-0.rc0.e406d57be7bd

* Thu Oct 02 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.7f7072574127.4]
- redhat: ark-linux-next.sh: initial commit (Scott Weaver)
- redhat: prepare-commit-msg: initial commit (Scott Weaver)
- redhat: ark-merge-driver: initial commit (Scott Weaver)
- redhat/Makefile: add dist-configs-commit-mismatches (Scott Weaver)
- Linux v6.18.0-0.rc0.7f7072574127

* Wed Oct 01 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.50c19e20ed2e.3]
- Flip SCHED_MC for RHEL ppc to avoid a mismatch (Justin M. Forbes)
- Linux v6.18.0-0.rc0.50c19e20ed2e

* Wed Oct 01 2025 Fedora Kernel Team <kernel-team@fedoraproject.org> [6.18.0-0.rc0.755fa5b4fb36.2]
- Revert "Merge branch 'add_next_sched_job' into 'os-build'" (Justin M. Forbes)
- Fix up a merge window mismatch for riscv RHEL (Justin M. Forbes)
- Reset RHEL_RELEASE for the 6.18 cycle (Justin M. Forbes)
- Turn on USB_FUNCTIONFS for Fedora (Justin M. Forbes)
- redhat/configs: Disable CONFIG_EFI_MIXED in RHEL (Lenny Szubowicz)
- Revert "Merge branch 'tmp2' into 'os-build'" (Justin M. Forbes)
- Always set LLVM=1 when building with clang (Tom Stellard)
- redhat/configs: Move CONFIG_MITIGATION_VMSCAPE to common/generic/x86 (Waiman Long)
- redhat/Makefile: Update the make target dist-configs-check to fail (Alexandra Hájková)
- Consolidate configs to common for 6.17 (Justin M. Forbes)
- Add 1010-config-newlines-test.bats self test. (Alexandra Hájková)
- os-build: Remove dead CONFIG_SCHED_DEBUG files (Phil Auld)
- redhat/configs: automotive: Disable COMPAT_32BIT_TIME SGETMASK_SYSCALL and IA32_EMULATION configs (Dorinda Bassey)
- Revert "redhat/configs: automotive: Disable NetLabel subsystem support" (Dorinda Bassey)
- redhat: ark-linux-next.sh: initial commit (Scott Weaver)
- redhat: prepare-commit-msg: initial commit (Scott Weaver)
- redhat: ark-merge-driver: initial commit (Scott Weaver)
- redhat/Makefile: add dist-configs-commit-mismatches (Scott Weaver)
- Turn on PINCTRL_SM8550_LPASS_LPI for Fedora (Justin M. Forbes)
- redhat: configs: drop TI_K3_UDMA & TI_K3_UDMA_GLUE_LAYER from RHEL (Eric Chanudet)
- redhat: configs: move TI_SCI_PROTOCOL and TI_MESSAGE_MANAGER to common (Eric Chanudet)
- Set CONFIG_MITIGATION_VMSCAPE for Fedora (Justin M. Forbes)
- redhat/Makefile: update dist-vr-check (Scott Weaver)
- gitlab-ci: add kcidb_tree_name to trees (Tales da Aparecida)
- Fix packaging for libcpupower python binding debuginfo (Justin M. Forbes)
- redhat/configs: automotive: enable TI K3 R5F remoteproc driver (Jared Kangas)
- Move CONFIG_SCHED_PROXY_EXEC to the zfcpdump directory (Justin M. Forbes)
- Set Fedora configs for 6.17 (Justin M. Forbes)
- redhat: scripts: ignore incorrect shellcheck 2329 in trap function (Simone Tollardo)
- Turn on PHY_ROCKCHIP_SAMSUNG_DCPHY for Fedora (Justin M. Forbes)
- rh_messages.h: add missing aacraid device (Scott Weaver)
- rh_messages.h: update unmaintained drivers (Scott Weaver)
- arm64: enable Tegra264 SoC components in RHEL (Marcin Juszkiewicz)
- redhat: export only selected variables (Jan Stancek)
- gitlab-ci: set HOME in maintenance jobs (Tales da Aparecida)
- gitlab-ci: remove fetch of linux-rt-devel (Scott Weaver)
- redhat/Makefile: auto select -z-test-pesign target for z-stream (Jan Stancek)
- redhat/configs: Move RHEL/Fedora lockdown configs to common (Jeremy Cline)
- Enable building libcpupower bindings for ELN/Rawhide (John B. Wyatt IV)
- redhat: Explicitly disable 'hostonly' mode on the dracut cmdline (Vitaly Kuznetsov)
- redhat: Directly use 'ukify' for building the UKI (Vitaly Kuznetsov)
- redhat: Temporary stop adding 'kernel' component to SBAT (Vitaly Kuznetsov)
- redhat/configs: Remove obsolete CONFIG files - part 1 (Waiman Long)
- redhat/Makefile: add dist-spec (Scott Weaver)
- redhat: Switch to implicit enablement of CONFIG_EFI_SBAT_FILE (Vitaly Kuznetsov)
- redhat/configs: Enable early lockdown for Arm (Mark Salter) [RHEL-1927]
- arm64: add early lockdown for secure boot (Mark Salter) [RHEL-1927]
- efi: pass secure boot mode to kernel proper (Mark Salter) [RHEL-1927]
- Disable Nova Core until it is useful (Justin M. Forbes)
- Turn off LIBBPF_DYNAMIC for perf builds (Justin M. Forbes)
- redhat: Add SBAT information to Linux kernel (Vitaly Kuznetsov)
- redhat: Add SBAT to the UKI unconditionally (Vitaly Kuznetsov)
- Enable PHY drivers required for automotive board (Radu Rendec)
- fedora: more updates for 6.17 (Peter Robinson)
- specfile: change conditionals for realtime for fedora (Clark Williams)
- redhat/configs: Disable TPM2 HMAC sessions (Štěpán Horáček) [RHEL-82779]
- redhat/script: Fix instructions for dist-cross-setup (Thomas Huth)
- redhat/configs: Fix location of the S390_MODULES_SANITY_TEST switch (Thomas Huth)
- redhat/configs: Fix location of the CONFIG_S390_KPROBES_SANITY_TEST switch (Thomas Huth)
- redhat/configs: Remove superfluous generic CONFIG_TUNE_Z16 switch (Thomas Huth)
- redhat/configs: Consolidate the CONFIG_TUNE_Z17 switch (Thomas Huth)
- redhat/configs: Consolidate the CONFIG_RANDOMIZE_IDENTITY_BASE switch (Thomas Huth)
- Fix up some networking configs to make docker work again (Justin M. Forbes)
- rename CONFIG_PAGE_BLOCK_ORDER to CONFIG_PAGE_BLOCK_MAX_ORDER (Justin M. Forbes)
- kernel.spec: add '-e' option to %%preun for kernel-core and kernel-uki-virt (Xuemin Li)
- Remove CONFIG_TEST_MISC_MINOR as deps are no longer met (Justin M. Forbes)
- Add to pending to fix precendence and avoid mismatch (Justin M. Forbes)
- CONFIG_PAGE_BLOCK_ORDER is now CONFIG_PAGE_BLOCK_MAX_ORDER (Justin M. Forbes)
- redhat/kernel.spec: fix leftover typo in Provides line (Jan Stancek)
- fedora: Updates for 6.17 merge (Peter Robinson)
- Fix a mismatch, needs further investigation (Justin M. Forbes)
- Turn off TEST_MISC_MINOR as its deps are no longer met (Justin M. Forbes)
- redhat/configs: Disable CRYPTO_KRB5 for zfcpdump (Vladis Dronov)
- Trim changelog after rebase (Justin M. Forbes)
- Flip TEGRA124_CPUFREQ to m for config mismatch (Justin M. Forbes)
- Reset RHEL_RELEASE for the 6.17 cycle (Justin M. Forbes)
- redhat/kernel.spec: fix uname_variant call sites (Jan Stancek) [RHEL-104231]
- redhat/kernel.spec: fix uname_suffix call sites (Jan Stancek) [RHEL-104231]
- redhat/configs: Add evaluate_configs.py and documentation (Prarit Bhargava)
- redhat: Remove old evaluate_configs (Prarit Bhargava)
- redhat/spec: package full bpftool in selftests (Gregory Bell)
- selftests/bpf: Remove ksyms_weak_lskel test (Artem Savkov)
- redhat/spec: Add libxml2-devel dependency for selftests build (Viktor Malik)
- redhat/spec: Bypass check-rpaths for kselftests/bpf/urandom_read (Viktor Malik)
- redhat/spec: Do not use source fortification for C++ selftest binaries (Viktor Malik)
- redhat/spec: Do not use source fortification for selftests (Viktor Malik)
- redhat/spec: Fix BPF selftests build with PIE (Viktor Malik)
- redhat/spec: Add EXTRA_CXXFLAGS to bpf samples and selftests make (Artem Savkov)
- fedora: minor cleanups (Peter Robinson)
- fedora: aarch64: enable a couple of brcmstb reset drivers (Peter Robinson)
- rhel/aarch64: enable CONFIG_TCG_ARM_CRB_FFA as a module (Marcin Juszkiewicz)
- redhat/configs: Move CONFIG_MITIGATION_TSA under common/generic/x86 (Waiman Long)
- Set CONFIG_TEST_VMALLOC to off for s390 zfcpdump (Justin M. Forbes)
- Revert "redhat/configs: automotive: Turn off ACPI Processor package for aarch64" (Enric Balletbo i Serra)
- redhat/configs: automotive: Disable CONFIG_NUMA config (Dorinda Bassey)
- Consolidate configs to common for 6.16 (Justin M. Forbes)
- arm64: enable SND_HDA_ACPI as a module (Marcin Juszkiewicz)
- kernel.spec: always provide kernel-devel-uname-r (Scott Weaver)
- kernel.spec: always provide kernel (Scott Weaver)
- kernel.spec: dynamically set provides/requires name (Scott Weaver)
- kernel.spec: use %%{name} in partner/internal modules (Scott Weaver)
- kernel.spec: introduce with_automotive_build (Scott Weaver)
- kernel.spec: fix kernel-automotive packaging (Scott Weaver)
- kernel.spec: add a few macro option comments (Scott Weaver)
- kernel.spec: add conditional to include rhel trusted certificates (Eric Chanudet)
- kernel.spec: Always BuildRequire openssl-devel (Eric Chanudet)
- kernel.spec: automotive: disable kernel signature by default (Eric Chanudet)
- redhat/configs: automotive: enable extra system cert (Eric Chanudet)
- redhat/configs: automotive: Disable module signature with modules_install (Eric Chanudet)
- kernel.spec: honor packaging flags (Scott Weaver)
- Fix FIPS mode for Fedora (Justin M. Forbes)
- Turn on TSA Mitigation for Fedora (Justin M. Forbes)
- redhat/configs: Enable CONFIG_AMD_HSMP_ACPI and CONFIG_AMD_HSMP_PLAT on RHEL (David Arcari)
- redhat/configs: CONFIG_WWAN enough as a module (Jose Ignacio Tornos Martinez)
- redhat/configs: Enable CONFIG_NET_SCH_BPF on RHEL (Viktor Malik)
- config: new config in drivers/phy (Izabela Bakollari)
- livepatch: no need to build kselftests with kernel (Radomir Vrbovsky)
- redhat: Restore the status quo wrt memory onlining (Vitaly Kuznetsov) [2375049]
- redhat/spec: Disable gdb index for riscv cross-compile (Jennifer Berringer)
- gitlab-ci: Enable CI for riscv64 on centos/eln (Jennifer Berringer)
- redhat: Enable RISC-V arch for centos/eln (Jennifer Berringer)
- redhat/kernel.spec.template: add drivers/net and drivers/net/hw selftest (Hangbin Liu)
- uki: enable FIPS mode (Vitaly Kuznetsov)
- redhat/configs: Move CONFIG_MITIGATION_ITS to common/generic/x86 (Waiman Long)
- redhat/configs: enable fwctl for RHEL (Michal Schmidt) [RHEL-96987]
- Fedora configs for 6.16 (Justin M. Forbes)
- aarch64: Switch TI_SCI_CLK and TI_SCI_PM_DOMAINS symbols to built-in (Peter Robinson)
- redhat/configs: enable CONFIG_TCG_SVSM (Stefano Garzarella)
- redhat: enable CONFIG_CRASH_DM_CRYPT and CONFIG_KEXEC_HANDOVER for all (Coiby Xu)
- Simplify include Makefile.rhelver (Don Zickus)
- redhat/configs/common/generic: enable vgem module via CONFIG_DRM_VGEM (Alexander Kanavin)
- redhat/configs: enable IWLMLD for rhel (Jose Ignacio Tornos Martinez)
- kernel.spec: fedora automotive build is not supported (Scott Weaver)
- gitignore: kernel-automotive generated files (Scott Weaver)
- gitlab-ci: use AUTOMOTIVE_BUILD with dist-srpm (Scott Weaver)
- redhat/self-test: update for new automotive variables (Scott Weaver)
- redhat/Makefile: introduce AUTOMOTIVE_BUILD (Scott Weaver)
- kernel.spec: updates for automotive-only build (Scott Weaver)
- fedora: Updates for the 6.16 merge window (Peter Robinson)
- redhat/kernel.spec: drop modules-extra-matched for noarch (Jan Stancek)
- redhat/configs: fedora: set some qcom clk, icc, and pinctrl drivers to built in (Brian Masney)
- fedora: disable SND_OSSEMUL (Peter Robinson)
- fedora: disable OSS sound for real HW (Peter Robinson)
- gitlab-ci: disable merge-rt-automotive (Scott Weaver)
- redhat/configs: automotive: enable j784s4evm DSP remoteproc configs (Jared Kangas) [RHEL-95436]
- redhat/configs: add LED kernel configs (Rupinderjit Singh)
- redhat: enable test_kmod, test_module and install kmod selftests (Herton R. Krzesinski)
- package the newly added cpupower.service (Thorsten Leemhuis)
- process_configs: always print errors (Thorsten Leemhuis)
- redhat/configs: disable RZ/V2N in automotive (Eric Chanudet)
- redhat/configs: Move RZ/G3E config to automotive (Eric Chanudet)
- redhat: add more namespace selftests to kernel-modules-internal package (Joel Savitz) [RHEL-94503]
- redhat/configs: Enable CONFIG_PCIE_TPH (Ivan Vecera)
- spec: fix spec warning for /usr/include/ynl (Jan Stancek)
- redhat/configs: Move CONFIG_PPC_FTRACE_OUT_OF_LINE_NUM_RESERVE to powerpc (Viktor Malik)
- Fix up powerpc mismatch (Justin M. Forbes)
- Fix another mismatch for 6.16 (Justin M. Forbes)
- Fix up a mismatch for Fedora aarch64 (Justin M. Forbes)
- Fix up mismatches for RHEL s390 zfpcdump (Justin M. Forbes)
- More mismatch fixes for 6.16 (Justin M. Forbes)
- Turn CROS_EC_PROTO to m for Fedora to avoid mismatch (Justin M. Forbes)
- Reset changelog for 6.16 cycle (Justin M. Forbes)
- Fix up CRYPTO_SHA256 configs for mismatch (Justin M. Forbes)
- Reset RHEL_RELEASE for the 6.16 cycle (Justin M. Forbes)
- fedora: add 'fedora' SBAT suffix for UKI addons (Li Tian)
- redhat: add downstream SBAT for UKI addons (Emanuele Giuseppe Esposito)
- uki_addons: provide custom SBAT as input parameter (Emanuele Giuseppe Esposito)
- uki_addons: remove completely sbat/sbat.conf (Emanuele Giuseppe Esposito)
- Consolidate configs to common for 6.15 (Justin M. Forbes)
- redhat/configs: automotive: enable MHI_BUS_EP (Eric Chanudet)
- Fix PHYSICAL_ALIGN for x86 Fedora (Justin M. Forbes)
- Switch ZSWAP_ZPOOL_DEFAULT to ZSMALLOC as ZBUD has been removed (Justin M. Forbes)
- redhat: configs: rhel: Enable CX231XX drivers (Kate Hsuan)
- configs: add redhat/configs/common/generic/CONFIG_OBJTOOL_WERROR (Ryan Sullivan) [RHEL-85301]
- redhat: make ENABLE_WERROR also enable OBJTOOL_WERROR (Ryan Sullivan) [RHEL-85301]
- redhat/configs: Enable CONFIG_X86_POSTED_MSI (Jerry Snitselaar)
- redhat/configs: remove CRC16 config files (Scott Weaver)
- Revert CONFIG_GENKSYMS in pending for x86 (Justin M. Forbes)
- Flip GENKSYMS for RHEL (Justin M. Forbes)
- Move MITIGATION_ITS to the x86 directory (Justin M. Forbes)
- Set MITIGATION_ITS for Fedora (Justin M. Forbes)
- Fedora: arm: Updates for QCom devices (Souradeep Chowdhury)
- redhat/configs: Explicitly disable CONFIG_VIRTIO_MEM on powerpc in RHEL (Thomas Huth)
- redhat/configs: Consolidate the CONFIG_AP_DEBUG config switch (Thomas Huth)
- Set Fedora configs for 6.15 (Justin M. Forbes)
- Shorten the uname for git snapshots (Justin M. Forbes)
- nvme: explicitly enable the nvme keyring (Maurizio Lombardi)
- Enable the gs_usb CAN bus driver in RHEL (Radu Rendec)
- Stop disabling some modules needed to run on Azure (Pierre-Yves Chibon)
- redhat/configs: enable ACPI_DEBUG on non-debug kernels (Mark Langsdorf)
- specfile:  add with_toolsonly variable to build only tools packages (Clark Williams)
- redhat/configs: Enable CONFIG_TYPEC_TBT_ALTMODE in RHEL (Desnes Nunes) [RHEL-78931]
- Turn on ACPI_DEBUG for Fedora (Justin M. Forbes)
- redhat: fix kernel-rt-kvm package removal for Fedora (Thorsten Leemhuis)
- redhat/configs: aarch64: Enable Apple touchbar display driver for Fedora (Neal Gompa)
- redhat: remove kernel-rt-kvm package (Clark Williams)
- redhat: introduce modules-extra-matched meta package (Jan Stancek)
- Fix up some Netfilter configs for Fedora (Justin M. Forbes)
- Turn NF_CT_NETLINK_TIMEOUT for Fedora (Justin M. Forbes)
- Turn on NF_CONNTRACK_TIMEOUT for Fedora (Justin M. Forbes)
- redhat/configs: Adjust CONFIG_TUNE for s390x (Mete Durlu)
- redhat/spec: fix selftests dependencies (Gregory Bell) [RHEL-88228]
- redhat: add namespace selftests to kernel-modules-internal package (Joel Savitz) [RHEL-88635]
- Turn off CONFIG_PCI_REALLOC_ENABLE_AUTO for Fedora (Justin M. Forbes)
- gitlab-ci: enable pipelines for rt-64k (Clark Williams)
- rt-64k:  Enable building 64k page-size RT kernel (Clark Williams)
- redhat: drop Y issues from changelog (Jan Stancek)
- redhat/configs: Update the CONFIG_KERNEL_IMAGE_BASE kernel config option (Thomas Huth)
- redhat/configs: Remove the obsolete CONFIG_ZCRYPT_DEBUG switches (Thomas Huth)
- redhat/configs: Consolidate the CONFIG_AP switch (Thomas Huth)
- fedora: updates for 6.15 (Peter Robinson)
- redhat/configs: Disable CONFIG_COMPAT option on s390 (Mete Durlu) [RHEL-24047]
- uki: Add weak dependency on 'uki-direct' (Vitaly Kuznetsov)
- redhat/kernel.spec: fix duplicate packaging of ynl headers (Jan Stancek)
- Enable FunctionFS on aarch64 + x86 (Sam Day)
- Turn on USB Gadget for Fedora x86 (Justin M. Forbes)
- redhat: enable drm panic screen with a QR code (Scott Weaver)
- redhat: enable Rust code in ELN (Scott Weaver)
- redhat: strip leading '(' in dist-get-buildreqs (Jan Stancek)
- Fix up CONFIG_CRC_ITU_T mismatch (Scott Weaver)
- Fix up CONFIG_CRC16 mismatch (Scott Weaver)
- redhat: remove kernel-ipaclones-internal package (Joe Lawrence)
- redhat/kernel.spec.template: add net packetdrill selftests (Hangbin Liu)
- redhat/kernel.spec.template: Build rtla with BPF sample collection (Tomas Glozar)
- redhat/configs: automotive: Enable CONFIG_BOOTPARAM_HUNG_TASK_PANIC config (Dorinda Bassey)
- samples/bpf: fix build (Gregory Bell)
- redhat: create 'systemd-volatile-overlay' addon for UKI (Emanuele Giuseppe Esposito)
- fedora: arm64: move some TI drivers to modular (Peter Robinson)
- fedora: minor cleanups for 6.14 (Peter Robinson)
- redhat/configs: enable CONFIG_I2C_MUX_PCA954x on x86 (Michal Schmidt)
- redhat: bump RHEL_MAJOR (Jan Stancek)
- redhat/configs: enable CONFIG_AMD_3D_VCACHE for x86 on RHEL (David Arcari)
- Switch ZSWAP_ZPOOL_DEFAULT to ZSMALLOC as ZBUD has been removed (Justin M. Forbes)
- redhat/kernel.spec: list python3-wheel explicitly for Fedora<42 (Jan Stancek)
- handle man-page for rv-mon-sched in redhat/kernel.spec.template (Thorsten Leemhuis)
- redhat: find-debuginfo workaround is no longer needed on F42 (Jan Stancek)
- redhat/kernel.spec: use target versions of tools for debugedit and gdb-add-index (Jan Stancek)
- redhat: make ENABLE_WERROR enable also KVM_WERROR (Jan Stancek)
- kernel.spec.template: cpupower: adjust lib versioning (Thorsten Leemhuis)
- redhat/configs: automotive: builtin virtio-mmio (Eric Chanudet)
- Fix up mismatches in the 6.15 merge window (Scott Weaver)
- Reset log for 6.15 cycle (Justin M. Forbes)
- Reset RHEL_RELEASE for 6.15 cycle (Justin M. Forbes)
- arm64: cleanup and de-dupe erratum (Peter Robinson)
- arm64: cleanup and de-dupe configs (Peter Robinson)
- cleanup: x86: cleanup some x86_32 leftovers (Peter Robinson)
- all: cleanup CAN_ROCKCHIP_CANFD (Peter Robinson)
- aarch64: Options required for UEFI HTTP boot on SystemReady-DT (Peter Robinson)
- common: Move ZONE_DEVICE to generic (Peter Robinson)
- common: Cleanup BTT (Peter Robinson)
- cleanup: move DEV_DAX_PMEM to common/generic (Peter Robinson)
- generic: cleanup the NVDIMM options (Peter Robinson)
- cleanup: move OF_PMEM to common/generic (Peter Robinson)
- cleanup: Remove DEV_DAX_PMEM_COMPAT option (Peter Robinson)
- Consolidate configs into common for 6.14 (Justin M. Forbes)
- Turn VIRTIO_BLK and VIRTIO_CONSOLE inline for Fedora (Justin M. Forbes)
- redhat: configs: fedora: enable CONFIG_I2C_HID_OF=m on x86 (Hans de Goede)
- redhat: move dist-relase-check behind new variable (Jan Stancek)
- Set last minute config item for 6.14 for Fedora (Justin M. Forbes)
- redhat/configs: automotive: Disable CONFIG_USERFAULTFD config (Dorinda Bassey)
- redhat/configs: automotive: Disable VLAN_8021Q_GVRP config (Dorinda Bassey)
- redhat/configs: automotive: Disable DCB and MPLS configs (Dorinda Bassey)
- redhat/configs: automotive: Disable IEEE 802.15.4 config (Dorinda Bassey)
- redhat/configs: automotive: Disable various network classification features (Dorinda Bassey)
- redhat/configs: automotive: Disable the SMBFS file system (Dorinda Bassey)
- redhat/configs: automotive: Disable Myricom network adapters (Dorinda Bassey)
- redhat/configs: automotive: Disable USB4 Ethernet config (Dorinda Bassey)
- redhat/configs: automotive: Disable the Mellanox SwitchX core driver (Dorinda Bassey)
- redhat/configs: automotive: Disable network storage related protocols (Dorinda Bassey)
- redhat/configs: automotive: Disable lightweight tunneling with BPF (Dorinda Bassey)
- redhat/configs: automotive: Disable RADOS block device configs (Dorinda Bassey)
- redhat/configs: automotive: Disable switchdev driver framework (Dorinda Bassey)
- redhat/configs: automotive: Disable network packet generator (Dorinda Bassey)
- redhat/configs: automotive: Disable NET_CLS_ACT and PSAMPLE configs (Dorinda Bassey)
- redhat/configs: automotive: Disable BPF STREAM_PARSER (Dorinda Bassey)
- redhat/configs: automotive: Disable Open vSwitch and NET_NSH configs (Dorinda Bassey)
- redhat/configs: automotive: Disable IP Virtual Server configs (Dorinda Bassey)
- redhat/configs: automotive: Disable IP set support (Dorinda Bassey)
- redhat/configs: automotive: Disable NetLabel subsystem support (Dorinda Bassey)
- redhat/configs: automotive: Disable TLS Protocol (Dorinda Bassey)
- redhat/configs: automotive: Disable Advanced TCP Congestion Control (Dorinda Bassey)
- redhat/configs: automotive: Disable XDP Socket Protocol (Dorinda Bassey)
- redhat/configs: delete CONFIG_USB_ONBOARD_HUB and use CONFIG_USB_ONBOARD_DEV instead (Desnes Nunes)
- redhat: check release commit is present for dist-{release-tag,git} (Jan Stancek)
- Re-enable vxcan (CONFIG_CAN_VXCAN) for automotive (Radu Rendec)
- Turn on CONFIG_PACKING for RHEL (Justin M. Forbes)
- main.c: fix initcall blacklisted (Tomas Henzl)
- redhat/configs: automotive: Disable IPsec Protocols and XFRM (Dorinda Bassey)
- redhat: Update CONFIG_STRICT_DEVMEM settings (enable it on s390x) (Thomas Huth)
- redhat: Consolidate CONFIG_VIRTIO_MEM and enable it also for s390x (Thomas Huth)
- Remove no longer necessary pending entry (Justin M. Forbes)
- Fedora configs for 6.14 (Justin M. Forbes)
- redhat/configs: Disable rest of the CONFIG_PKEY_ options on s390 (Mete Durlu) [RHEL-78341]
- Fix up some debug module loading issues due to BTF mismatch (Justin M. Forbes)
- Revert "redhat/configs: automotive: disable CONFIG_AIO" (Davide Caratti)
- redhat/configs: automotive disable ARCH_TEGRA_241_SOC (Eric Chanudet)
- rhel_files: ensure all qdiscs are in modules-core (Davide Caratti) [RHEL-79818]
- redhat/configs: automotive: Disable MRP/8021Q_MVRP Protocol (Dorinda Bassey)
- redhat/configs: enable CONFIG_ARM_SMMU_MMU_500_CPRE_ERRATA (Jerry Snitselaar)
- redhat/configs: enable CONFIG_ARM_SMMU_V3_IOMMUFD (Jerry Snitselaar)
- redhat: configs: remove CONFIG_DMA_API_DEBUG_SG (Kate Hsuan)
- kernel.spec: add missing tools-libs on s390x (Jan Stancek)
- arch/x86/kernel/setup.c: fix rh_check_supported (Tomas Henzl)
- kernel.spec: add minimum version of setuptools for ynl (Jan Stancek)
- Revert "Merge: redhat/configs: automotive: Disable POSIX_MQUEUE config (Dorinda Bassey)
- redhat/configs: enable in kernel compression/decompression of compressed modules (Herton R. Krzesinski)
- redhat: change compression flags for xz (Herton R. Krzesinski)
- redhat/configs: automotive: Turn off ACPI Processor package for aarch64 (Enric Balletbo i Serra)
- redhat/configs: automotive: Disable L2TP Protocol (Dorinda Bassey)
- redhat/configs: automotive: Disable TIPC Protocol (Dorinda Bassey)
- redhat/configs: Enable Mediatek Bluetooth USB drivers (Bastien Nocera)
- redhat/configs: Disable CONFIG_PKEY for zfcpdump configs (Mete Durlu) [RHEL-78341]
- redhat/configs: automotive: disable VFIO_PLATFORM (Eric Chanudet)
- Revert "Merge: redhat/configs: automotive: Disable SYSIPC config" (Dorinda Bassey)
- redhat/configs: Enable CONFIG_KASAN_INLINE for RT debug kernel (Waiman Long)
- redhat/configs: Move CONFIG_PROVE_RAW_LOCK_NESTING to common/debug (Waiman Long)
- redhat/configs: Move all the lock debugging Kconfig's to common (Waiman Long)
- redhat/configs: Enable CONFIG_BLK_CGROUP_PUNT_BIO for RHEL (Neal Gompa) [RHEL-79711]
- fedora: pending: drop USB_ONBOARD_DEV_USB5744 (Peter Robinson)
- efi,lockdown: fix kernel lockdown on Secure Boot (Ondrej Mosnacek) {CVE-2025-1272}
- fedora: Update vbox drivers (Peter Robinson)
- Drop the s390x CONFIG_REGMAP from RHEL pending as upstream removed the dep (Justin M. Forbes)
- fedora: arm64: enable RT5616 codec (Marcin Juszkiewicz)
- Revert "nvme: Return BLK_STS_TARGET if the DNR bit is set" (Benjamin Marzinski)
- Revert "nvme: allow local retry and proper failover for REQ_FAILFAST_TRANSPORT" (Benjamin Marzinski)
- Revert "nvme: decouple basic ANA log page re-read support from native multipathing" (Benjamin Marzinski)
- Revert "nvme: nvme_mpath_init remove multipath check" (Benjamin Marzinski)
- redhat/configs: automotive: Disable CONFIG_FS_DAX config (Dorinda Bassey)
- config: update CONFIG_LSM to match upstream (Ryan Sullivan)
- redhat: configs: enable CONFIG_INTEL_ISH_FIRMWARE_DOWNLOADER for RHEL (David Arcari)
- redhat/Makefile: Add help text for target dist-dump-variables (Eder Zulian)
- redhat: update self-test-data for new default RHJOBS value (Patrick Talbert)
- set a more reasonable default for number of jobs (Thorsten Leemhuis)
- redhat: automotive: define CONFIG_RH_AUTOMOTIVE (Scott Weaver)
- redhat/configs: disable CONFIG_TCP_AO on RHEL (Sabrina Dubroca)
- redhat/configs: amend USB_ONBOARD_DEV_USB5744 (Eric Chanudet)
- redhat/configs: automotive: Disable SYSIPC and MQUEUE configs (Dorinda Bassey)
- redhat: kernel.spec: add ynl to kernel-tools (Jan Stancek)
- fedora: enable USB device USB5744 (Peter Robinson)
- rhel: enable FW_CACHE on RHEL (Dave Airlie)
- redhat/configs: automotive: Disable the SCTP Protocol (Dorinda Bassey)
- redhat: generalize rule for kunit and test kmod placement (Jan Stancek)
- Move CONFIG_PCI_REALLOC_ENABLE_AUTO out of common as they have diverged (Justin M. Forbes)
- fedora: arm64: enable Silicon Mitus SM5502 Extcon driver (Sam Day)
- fedora: arm64: enable Richtek RT5033 MFD+charger+regulator modules (Sam Day)
- configs/fedora: Enable CONFIG_PCI_REALLOC_ENABLE_AUTO (Yanko Kaneti)
- Enable CONFIG_INTEL_MEI_PXP and CONFIG_DRM_I915_PXP on rhel (Jocelyn Falempe)
- Enable Intel Xe Graphics (Mika Penttilä)
- Turn on CONFIG_DRM_ACCEL_AMDXDNA for Fedora (Justin M. Forbes)
- redhat/configs: disable CONFIG_AF_UNIX_OOB on RHEL (Marcelo Ricardo Leitner)
- redhat/configs: automotive: Disable wireless network and it's dependencies (Dorinda Bassey)
- redhat/kernel.spec: work around find-debuginfo aborting cross builds (Jan Stancek)
- redhat/configs: Default to batched invalidation on s390 (Jerry Snitselaar)
- redhat/configs: automotive: set CONFIG_TIMEOUT_PANIC (Enric Balletbo i Serra)
- drop %%{_datadir}/perf-core/* from kernel.spec (Thorsten Leemhuis)
- put new misc_minor_kunit in modules-internal (Thorsten Leemhuis)
- put new cirrus kunit tests in modules-internal (Thorsten Leemhuis)
- redhat/configs: enable iBFT parsing on aarch64 (Chris Leech)
- redhat: kernel.spec: fix build with merged-sbin (Zbigniew Jędrzejewski-Szmek)
- Fix up CONFIG_REGMAP mismatch (Scott Weaver)
- redhat: fix modules.order target (Scott Weaver)
- Fix up CONFIG_CRC_T10DIF_IMPL_GENERIC mismatch (Justin M. Forbes)
- Fix mismatches for 6.13 merge window (Justin M. Forbes)
- Reset rhelver and trim changelog for 6.14 (Justin M. Forbes)
- Turn off CONFIG_ARM_TIMER_SP804 for automotive (Justin M. Forbes)
- Set ARM_TIMER_SP804 (Justin M. Forbes)
- redhat/configs: enable addtional sa8775 related Kconfigs (Brian Masney)
- redhat: Add rustfmt to deps (Peter Robinson)
- redhat/configs: Disable deprecated CONFIG_LCS option on s390 (Mete Durlu) [RHEL-68296]
- redhat/configs: make modular/disable NFS support (Dorinda Bassey)
- redhat/configs: Disable unsafe queuing disciplines (Dorinda Bassey)
- configs: move pending RT configs into rhel/rt/generic (Clark Williams)
- Turn on PROVE_RAW_LOCK_NESTING for RHEL debug builds (Justin M. Forbes)
- redhat/Makefile: Fix long dist-full-help execution time (Prarit Bhargava)
- redhat/self-test: Update data to add HELP_TYPES variable (Prarit Bhargava)
- redhat/Makefile: Add new dist-help functionality (Prarit Bhargava)
- Makefile: Do not output LOCALVERSION message for help commands (Prarit Bhargava)
- Fedora 6.13 configs part 2 (Justin M. Forbes)
- Fedora 6.13 configs part 1 (Justin M. Forbes)
- redhat/configs: enable CONFIG_VFAT_FS as a module (Dorinda Bassey)
- redhat: create 'debug' addon for UKI (Li Tian)
- kernel.spec: Build cpupower on riscv64 (Yanko Kaneti)
- RHEL: Set correct config option for CRYPTO_HMAC_S390 (Mete Durlu) [RHEL-24137]
- redhat/kernel.spec: add iputils to the requires list for selftests-internal (Brian Masney)
- redhat/kernel.spec.template: Require kernel-tools-libs in rtla (Tomas Glozar)
- redhat: make kernel-debug-uki-virt installable without kernel-debug-core (Vitaly Kuznetsov)
- redhat/configs: enable CONFIG_USB_XHCI_PCI_RENESAS on RHEL (Desnes Nunes) [RHEL-72093]
- redhat/configs: Re-enable ZRAM backends and unify configuration (Neal Gompa)
- redhat/configs: automotive: disable CONFIG_AIO (Davide Caratti)
- redhat/configs: Re-enable CONFIG_INFINIBAND_VMWARE_PVRDMA (Vitaly Kuznetsov)
- redhat/configs: PREEMPT_NOTIFIERS does not need to be explicitly listed (Michal Schmidt)
- redhat/configs: delete all CONFIG_PREEMPT_*BEHAVIOUR (Michal Schmidt)
- redhat/configs: automotive: disable CONFIG_NET_DROP_MONITOR (Davide Caratti)
- redhat/configs: Enable the CS42L84 driver on Fedora (Neal Gompa)
- generic: Remove and cleanups from staging 6.13 (Peter Robinson)
- redhat: configs: Clean up DVB settings in RHEL (Kate Hsuan)
- Move CONFIG_ARCH_TEGRA_241_SOC config/common so that it is enabled for RHEL as well as Fedora. Get rid of uneeded CONFIG_TEGRA241_CMDQV in configs/fedora while we're at it. (Mark Salter)
- fedora: arm64: Enable the rockchip HDMI QP support (Peter Robinson)
- crypto: rng - Fix extrng EFAULT handling (Herbert Xu)
- redhat: configs: rhel: aarch64: Support NV Jetson MIPI camera (Kate Hsuan)
- gitlab-ci: disable clang CI pipelines (Scott Weaver)
- redhat/configs: Remove obsolete arch64/64k/CONFIG_FORCE_MAX_ZONEORDER (Waiman Long)
- Fix up QCOM_EMAC config for Fedora (Justin M. Forbes)
- redhat/configs: automotive: disable CONFIG_IO_URING (Ian Mullins)
- redhat/kernel.spec.template: Link rtla against in-tree libcpupower (Tomas Glozar)
- redhat: configs: enable INTEL_PLR_TPMI for RHEL (David Arcari)
- configs: Enable CONFIG_NETKIT for RHEL (Toke Høiland-Jørgensen)
- redhat: fix build/install targets in netfilter kselftest (Davide Caratti)
- RHEL: disable the btt driver (Jeff Moyer)
- redhat/configs: default to PREEMPT_LAZY on x86, riscv (Michal Schmidt)
- redhat/configs: New config CONFIG_PREEMPT_LAZY (Michal Schmidt)
- crypto: sig - Disable signing (Herbert Xu)
- redhat/configs: enable SERIAL_AMBA_PL011 for automotive (Radu Rendec)
- c10s: disable tests in CKI pipelines (Michael Hofmann)
- redhat: Drop bpftool from kernel spec (Viktor Malik)
- Better fixes for the fedora mismatch (Justin M. Forbes)
- Mismatch fix ups for Fedora (Justin M. Forbes)
- redhat/configs: Enable Intel Bluetooth PCIE drivers (Bastien Nocera)
- One more pending to fix a mismatch (Justin M. Forbes)
- redhat: fix RT PREEMPT configs for Fedora and RHEL (Clark Williams)
- Pending fixes to avoid mismatch for 6.13 (Justin M. Forbes)
- Reset changelog for 6.13 (Justin M. Forbes)
- Reset RHEL_RELEASE for 6.13 (Justin M. Forbes)
- redhat: Move perf_dlfilter.h from libperf-devel to perf (Akihiko Odaki)
- Consolidate configs to common for 6.12 (Justin M. Forbes)
- redhat/configs: cleanup CONFIG_DEV_DAX (David Hildenbrand)
- redhat/configs: cleanup CONFIG_TRANSPARENT_HUGEPAGE_MADVISE for Fedora (David Hildenbrand)
- redhat/configs: cleanup CONFIG_TRANSPARENT_HUGEPAGE (David Hildenbrand)
- redhat/configs: enable CONFIG_TRANSPARENT_HUGEPAGE on s390x in Fedora (David Hildenbrand)
- redhat/configs: automotive: Enable j784s4evm am3359 tscadc configs (Joel Slebodnick)
- redhat/configs: delete renamed CONFIG_MLX5_EN_MACSEC (Michal Schmidt)
- rhel: disable DELL_RBU and cleanup related deps (Peter Robinson)
- crypto: rng - Ensure stdrng is tested before user-space starts (Herbert Xu)
- gitlab-ci: Add CKI_RETRIGGER_PIPELINE (Tales da Aparecida)
- redhat: configs: disable the qla4xxx iSCSI driver (Chris Leech) [RHEL-1242]
- Remove duplicated CONFIGs between automotive and RHEL (Julio Faracco)
- redhat: update self-test data for addition of automotive (Scott Weaver)
- gitlab-ci: enable automotive pipeline (Scott Weaver)
- automotive: move pending configs to automotive/generic (Scott Weaver)
- redhat/configs: change Renesas eMMC driver and dependencies to built-in (Radu Rendec)
- redhat/configs: automotive: Remove automotive specific override CONFIG_OMAP2PLUS_MBOX By removing this automotive-specific override, the configuration will default to the common configuration (CONFIG_OMAP2PLUS_MBOX=m), which enables the driver as a module. (Martin McConnell)
- Config enablement of the Renesas R-Car S4 SoC (Radu Rendec) [RHEL-44306]
- redhat/configs: automotive: Enable USB_CDNS3_TI for TI platforms (Andrew Halaney)
- redhat/configs: automotive: Enable j784s4evm SPI configs (Joel Slebodnick)
- redhat/configs: automotive: Enable TPS6594 MFD (Joel Slebodnick)
- redhat/configs: automotive: stop overriding CRYPTO_ECDH (Andrew Halaney)
- redhat/configs: automotive: Enable PCI_J721E (Andrew Halaney)
- redhat/configs: change some TI platform drivers to built-in (Enric Balletbo i Serra)
- redhat/configs: automotive: Enable TI j784s4evm display dependencies (Andrew Halaney)
- redhat/configs: automotive: match ark configs to cs9 main-automotive (Shawn Doherty) [RHEL-35995]
- redhat/configs: automotive: Enable TI's watchdog driver (Andrew Halaney)
- redhat/configs: automotive: Enable TI's UFS controller (Andrew Halaney)
- redhat/configs: automotive: Enable networking on the J784S4EVM (Andrew Halaney) [RHEL-29245]
- Disable unsupported kernel variants for automotive (Don Zickus)
- Disable CONFIG_RTW88_22BU (Don Zickus)
- redhat: Delete CONFIG_EFI_ZBOOT to use the common CONFIG (Julio Faracco)
- redhat: Update automotive SPEC file with new standards (Julio Faracco)
- redhat: Disable WERROR for automotive temporarily (Julio Faracco)
- redhat: Update spec file with automotive macros (Julio Faracco)
- redhat: Add automotive CONFIGs (Julio Faracco)
- Fedora configs for 6.12 (Justin M. Forbes)
- redhat/configs: Add CONFIG_CRYPTO_HMAC_S390 config (Mete Durlu) [RHEL-50799]
- redhat: configs: common: generic: Clean up EM28XX that are masked behind CONFIG_VIDEO_EM28XX (Kate Hsuan)
- redhat/configs: Update powerpc NR_CPUS config (Mamatha Inamdar)
- redhat: use stricter rule for kunit.ko (Jan Stancek)
- filtermod: fix clk kunit test and kunit location (Nico Pache)
- redhat/configs: enable xr_serial on rhel (Desnes Nunes)
- redhat/configs: enable ATH12K for rhel (Jose Ignacio Tornos Martinez)
- redhat: configs: rhel: generic: x86: Enable IPU6 based MIPI cameras (Kate Hsuan)
- os-build: enable CONFIG_SCHED_CLASS_EXT for RHEL (Phil Auld)
- Fedora 6.12 configs part 1 (Justin M. Forbes)
- redhat: set new gcov configs (Jan Stancek)
- Don't ignore gitkeep files for ark-infra (Don Zickus)
- redhat/kernel.spec: don't clear entire libdir when building tools (Jan Stancek)
- redhat/configs: enable usbip for rhel (Jose Ignacio Tornos Martinez)
- redhat: create 'crashkernel=' addons for UKI (Vitaly Kuznetsov)
- redhat: avoid superfluous quotes in UKI cmdline addones (Vitaly Kuznetsov)
- fedora: arm: updates for 6.12 (Peter Robinson)
- redhat/configs: add bootconfig to kernel-tools package (Brian Masney)
- Enable CONFIG_SECURITY_LANDLOCK for RHEL (Zbigniew Jędrzejewski-Szmek) [RHEL-8810]
- redhat: configs: Drop CONFIG_MEMSTICK_REALTEK_PCI config option (Desnes Nunes)
- Update the RHEL_DIFFERENCES help string (Don Zickus)
- Put build framework for RT kernel in place for Fedora (Clark Williams)
- generic: enable RPMB for all configs that enable MMC (Peter Robinson)
- fedora: riscv: Don't override MMC platform defaults (Peter Robinson)
- common: only enable on MMC_DW_BLUEFIELD (Peter Robinson)
- fedora: aarch64: Stop overriding CONFIG_MMC defaults (Peter Robinson)
- commong: The KS7010 driver has been removed (Peter Robinson)
- Trim Changelog for 6.12 (Justin M. Forbes)
- Enable CONFIG_SECURITY_IPE for Fedora (Zbigniew Jędrzejewski-Szmek)
- redhat: allow to override VERSION_ON_UPSTREAM from command line (Jan Stancek)
- redhat: configs: Enable CONFIG_SECURITY_TOMOYO in Fedora kernels (Tetsuo Handa)
- Revert "Merge branch 'enablement/gpio-expander' into 'os-build'" (Justin M. Forbes)
- redhat: configs: decrease CONFIG_PCP_BATCH_SCALE_MAX (Rafael Aquini)
- redhat/configs: Enable CONFIG_RCU_TRACE in Fedora/REHL kernels (Waiman Long)
- fedora: distable RTL8192E wifi driver (Peter Robinson)
- common: arm64: Fixup and cleanup some SCMI options (Peter Robinson)
- common: Cleanup ARM_SCMI_TRANSPORT options (Peter Robinson)
- configs: fedora/x86: Set CONFIG_CRYPTO_DEV_CCP_DD=y (Hans de Goede)
- Turn on ZRAM_WRITEBACK for Fedora (Justin M. Forbes)
- configs: rhel: Fix designware I2C controllers related config settings (Hans de Goede)
- Enable CONFIG_DMA_NUMA_CMA for x86_64 and aarch64 (Chris von Recklinghausen)
- new config in drivers/phy (Izabela Bakollari)
- configs: fedora: Unset CONFIG_I2C_DESIGNWARE_CORE on s390x (Hans de Goede)
- configs: fedora: Drop duplicate CONFIG_I2C_DESIGNWARE_CORE for x86_64 and aarch64 (Hans de Goede)
- Enable DESIGNWARE_CORE for ppc as well (Justin M. Forbes)
- Fix up I2C_DESIGNWARE_CORE config for Fedora (Justin M. Forbes)
- configs for RT deps (Clark Williams)
- CONFIG_OF_OVERLAY: enable for aarch64 and powerpc (Scott Weaver)
- redhat: enable changes to build rt variants (Clark Williams)
- redhat: clean up pending-rhel (Patrick Talbert)
- Enable CONFIG_SCHED_CLASS_EXT for Fedora (Jose Fernandez)
- redhat/configs: new config in arch/s390 (Izabela Bakollari)
- redhat: ignore rpminspect runpath report on selftests/bpf/cpuv4/urandom_read (Viktor Malik)
- [fedora] configs: add end of file newline to CONFIG_DMADEVICES_VDEBUG (Patrick Talbert)
- unset CONFIG_DMADEVICES_VDEBUG (cmurf)
- stop installing tools/build/Build, gone with ea974028a049f (Thorsten Leemhuis)
- redhat/configs: Update LOCKDEP configs (Waiman Long)
- uki-virt: Add i18n module (Vitaly Kuznetsov)
- uki-virt: Drop DBUS support from initramfs (Vitaly Kuznetsov)
- uki-virt: Drop redundant modules from dracut-virt.conf (Vitaly Kuznetsov)
- uki-virt: Drop usrmount dracut module (Vitaly Kuznetsov)
- redhat: new AMCC_QT2025_PHY config in drivers/net/phy (Patrick Talbert)
- redhat: change schedule jobs image from cki-tools to builder-rawhide (Patrick Talbert)
- Add CONFIG_SND_SOC_RT1320_SDW to pending-rhel for mismatch (Justin M. Forbes)
- Turn on CONFIG_SND_SOC_RT1320_SDW in pending rhel (Justin M. Forbes)
- configs: disable CONFIG_AMCC_QT2025_PHY in pending (Patrick Talbert)
- fedora: turn on CONFIG_FDMA for powerpc (Patrick Talbert)
- Turn on CONFIG_FDMA in pending for Fedora arm and riscv to avoid a mismatch (Justin M. Forbes)
- Reset RHEL_RELEASE for 6.12 (Justin M. Forbes)
- Consolidate configs into common for 6.11 kernels (Justin M. Forbes)
- uki-virt: add systemd-cryptsetup module (Vitaly Kuznetsov)
- redhat/docs: fix command to install missing build dependencies (Davide Cavalca)
- spec: Respect rpmbuild --without debuginfo (Orgad Shaneh)
- fedora/configs: enable GPIO expander drivers (Rupinderjit Singh)
- redhat/configs: Switch to the Rust implementation of AX88796B_PHY driver for Fedora (Neal Gompa)
- redhat: Turn on support for Rust code in Fedora (Neal Gompa)
- Turn off RUST for risc-v (Justin M. Forbes)
- gitlab-ci: allow failure of clang LTO pipelines (Michael Hofmann)
- redhat/configs: Consolidate the CONFIG_KVM_BOOK3S_HV_P*_TIMING switches (Thomas Huth)
- redhat/configs: Consolidate the CONFIG_KVM_SW_PROTECTED_VM switch (Thomas Huth)
- redhat/configs: Consolidate the CONFIG_KVM_HYPERV switch (Thomas Huth)
- redhat/configs: Consolidate the CONFIG_KVM_AMD_SEV switch (Thomas Huth)
- Cleanup some riscv CONFIG locations (Justin M. Forbes)
- Fix up pending riscv Fedora configs post merge (Justin M. Forbes)
- fedora/configs: Enable SCMI configuration (Rupinderjit Singh)
- Remove S390 special config for PHYLIB (Justin M. Forbes)
- Disable ELN for riscv64 (Isaiah Stapleton)
- redhat: add checks to ensure only building riscv64 on fedora (Isaiah Stapleton)
- redhat: Add missing riscv fedora configs (Isaiah Stapleton)
- Add riscv64 to the CI pipelines (Isaiah Stapleton)
- redhat: Regenerate dist-self-test-data for riscv64 (Isaiah Stapleton)
- redhat: Add riscv config changes for fedora (David Abdurachmanov)
- redhat: Add support for riscv (David Abdurachmanov)
- redhat: Do not include UKI addons twice (Vitaly Kuznetsov)
- redhat: update gating.yml (Michael Hofmann)
- Remove CONFIG_FSCACHE_DEBUG as it has been renamed (Justin M. Forbes)
- Set Fedora configs for 6.11 (Justin M. Forbes)
- redhat/configs: Microchip lan743x driver (Izabela Bakollari)
- redhat: include resolve_btfids in kernel-devel (Jan Stancek)
- redhat: workaround CKI cross compilation for scripts (Jan Stancek)
- spec: fix "unexpected argument to non-parametric macro" warnings (Jan Stancek)
- Add weakdep support to the kernel spec (Justin M. Forbes)
- redhat: configs: disable PF_KEY in RHEL (Sabrina Dubroca)
- crypto: akcipher - Disable signing and decryption (Vladis Dronov) [RHEL-54183] {CVE-2023-6240}
- crypto: dh - implement FIPS PCT (Vladis Dronov) [RHEL-54183]
- crypto: ecdh - disallow plain "ecdh" usage in FIPS mode (Vladis Dronov) [RHEL-54183]
- crypto: seqiv - flag instantiations as FIPS compliant (Vladis Dronov) [RHEL-54183]
- [kernel] bpf: set default value for bpf_jit_harden (Artem Savkov) [RHEL-51896]
- fedora: disable CONFIG_DRM_WERROR (Patrick Talbert)
- redhat/configs: Disable dlm in rhel configs (Andrew Price)
- rhel: aarch64: enable required PSCI configs (Peter Robinson)
- fedora: Enable AF8133J Magnetometer driver (Peter Robinson)
- redhat: spec: add cachestat kselftest (Eric Chanudet)
- redhat: hmac sign the UKI for FIPS (Vitaly Kuznetsov)
- not upstream: Disable vdso getrandom when FIPS is enabled (Herbert Xu)
- kernel: config: enable erofs lzma compression (Ian Kent)
- fedora: disable RTL8192CU in Fedora (Peter Robinson)
- redhat: Fix the ownership of /lib/modules/<kversion> directory (Vitaly Kuznetsov)
- new configs in drivers/phy (Izabela Bakollari)
- Add support to rh_waived cmdline boot parameter (Ricardo Robaina) [RHEL-26170]
- redhat/configs: Disable gfs2 in rhel configs (Andrew Price)
- redhat/uki_addons/virt: add common FIPS addon (Emanuele Giuseppe Esposito)
- redhat/kernel.spec: add uki_addons to create UKI kernel cmdline addons (Emanuele Giuseppe Esposito)
- rh_flags: fix failed when register_sysctl_sz rh_flags_table to kernel (Ricardo Robaina) [RHEL-52629]
- redhat/dracut-virt.conf: add systemd-veritysetup module (Emanuele Giuseppe Esposito)
- redhat/configs: enable CONFIG_LOCK_STAT on the debug kernels for aarch64 (Brian Masney)
- redhat/configs: enable CONFIG_KEYBOARD_GPIO_POLLED for RHEL on aarch64 (Luiz Capitulino)
- redhat/configs: fedora: Enable new Qualcomm configs (Andrew Halaney)
- redhat/configs/fedora: set CONFIG_CRYPTO_CURVE25519_PPC64 (Dan Horák)
- fedora: Updates for 6.11 merge (Peter Robinson)
- fedora: enable new mipi sensors and devices (Peter Robinson)
- arm64: enable CRYPTO_DEV_TEGRA on RHEL (Peter Robinson)
- redhat/kernel.spec: fix file listed twice warning for "kernel" subdir (Jan Stancek)
- redhat/configs: Double MAX_LOCKDEP_ENTRIES for RT debug kernels (Waiman Long) [RHEL-43425]
- Support the first day after a rebase (Don Zickus)
- Support 2 digit versions properly (Don Zickus)
- Automation cleanups for rebasing rt-devel and automotive-devel (Don Zickus)
- fedora: set CONFIG_REGULATOR_RZG2L_VBCTRL as a module for arm64 (Patrick Talbert)
- gitlab-ci: restore bot pipeline behavior (Michael Hofmann)
- redhat/kernel.spec: drop extra right curly bracket in kernel_kvm_package (Jan Stancek)
- redhat/configs: enable gpio_keys driver for RHEL on aarch64 (Luiz Capitulino)
- Move NET_VENDOR_MICROCHIP from common to rhel (Justin M. Forbes)
- redhat/configs: enable some RTCs for RHEL on aarch64 (Luiz Capitulino)
- redhat/configs: enable some regulators for RHEL (Luiz Capitulino)
- redhat/config: disable CXL and CXLFLASH drivers (Dan Horák)
- Fix up config mismatches in pending (Justin M. Forbes)
- redhat/configs: Enable watchdog devices modelled by qemu (Richard W.M. Jones) [RHEL-40937]
- rhel: cleanup unused media tuner configs (Peter Robinson)
- all: cleanup MEDIA_CONTROLLER options (Peter Robinson)
- redhat: kernel.spec: add s390x to livepatching kselftest builds (Joe Lawrence)
- Flip CONFIG_DIMLIB back to inline (Justin M. Forbes)
- Add vfio/nvgrace-gpu driver CONFIG to RHEL-9.5 ARM64 (Donald Dutile)
- Enable CONFIG_RTC_DRV_TEGRA for RHEL (Luiz Capitulino)
- redhat: rh_flags: declare proper static methods when !CONFIG_RHEL_DIFFERENCES (Rafael Aquini)
- redhat: configs: enable CONFIG_TMPFS_QUOTA for both Fedora and RHEL (Rafael Aquini)
- Fix up mismatches in the 6.11 merge window. (Justin M. Forbes)
- Reset Changelog after rebase (Justin M. Forbes)
- Reset RHEL_RELEASE for the 6.11 cycle (Justin M. Forbes)
- redhat/configs: Enable CONFIG_VMWARE_VMCI/CONFIG_VMWARE_VMCI_VSOCKETS for RHEL (Vitaly Kuznetsov)
- Consolidate configs to common for 6.10 (Justin M. Forbes)
- redhat/configs: Enable CONFIG_PTP_1588_CLOCK_MOCK in kernel-modules-internal (Davide Caratti)
- fedora: enabled XE GPU drivers on all arches (Peter Robinson)
- Flip SND_SOC_CS35L56_SPI from off to module for RHEL (Justin M. Forbes)
- Flip DIMLIB from built-in to module for RHEL (Justin M. Forbes)
- Also remove the zfcpdump BASE_SMALL config (Justin M. Forbes)
- redhat: Add cgroup kselftests to kernel-selftests-internal (Waiman Long) [RHEL-43556]
- Revert "redhat/configs: Disable CONFIG_INFINIBAND_HFI1 and CONFIG_INFINIBAND_RDMAVT" (Kamal Heib)
- Remove new for GITLAB_TOKEN (Don Zickus)
- Set Fedora configs for 6.10 (Justin M. Forbes)
- Fedora: minor driver updates (Peter Robinson)
- redhat/configs: Remove obsolete x86 CPU mitigations config files (Waiman Long)
- redhat/configs: increase CONFIG_DEFAULT_MMAP_MIN_ADDR from 32K to 64K for aarch64 (Brian Masney)
- redhat/configs: Re-enable CONFIG_KEXEC for Fedora (Philipp Rudo)
- disable LR_WPAN for RHEL10 (Chris von Recklinghausen) [RHEL-40251]
- Turn on USB_SERIAL_F81232 for Fedora (Justin M. Forbes)
- redhat/scripts/filtermods.py: show all parent/child kmods in report (Jan Stancek)
- redhat/kernel.spec: capture filtermods.py return code (Jan Stancek)
- redhat/kernel.spec: fix run of mod-denylist (Jan Stancek)
- gitlab-ci: remove unused RHMAINTAINERS variable (Michael Hofmann)
- gitlab-ci: use environments for jobs that need access to push/gitlab secrets (Michael Hofmann)
- gitlab-ci: default to os-build for all maintenance jobs (Michael Hofmann)
- gitlab-ci: use the common git repo setup cki-gating as well (Michael Hofmann)
- gitlab-ci: help maintenance jobs to cope with missing private key (Michael Hofmann)
- gitlab-ci: use a common git repo setup for all maintenance jobs (Michael Hofmann)
- gitlab-ci: move repo setup script into script template holder (Michael Hofmann)
- gitlab-ci: move maintenance job DIST variable into common template (Michael Hofmann)
- gitlab-ci: move maintenance job rules into common template (Michael Hofmann)
- gitlab-ci: move maintenance job retry field into common template (Michael Hofmann)
- gitlab-ci: provide common non-secret schedule trigger variables (Michael Hofmann)
- gitlab-ci: rename .scheduled_setup to .git_setup (Michael Hofmann)
- gitlab-ci: move script snippets into separate template (Michael Hofmann)
- gitlab-ci: rename maintenance jobs (Michael Hofmann)
- gitlab-ci: introduce job template for maintenance jobs (Michael Hofmann)
- Turn on KASAN_HW_TAGS for Fedora aarch64 debug kernels (Justin M. Forbes)
- redhat: kernel.spec: add missing sound/soc/sof/sof-audio.h to kernel-devel package (Jaroslav Kysela)
- redhat/kernel.spec: fix attributes of symvers file (Jan Stancek)
- redhat: add filtermods rule for iommu tests (Jan Stancek)
- fedora: arm: Enable basic support for S32G-VNP-RDB3 board (Enric Balletbo i Serra)
- redhat: make bnx2xx drivers unmaintained in rhel-10 (John Meneghini) [RHEL-36646 RHEL-41231]
- redhat/configs: Disable CONFIG_NFP (Kamal Heib) [RHEL-36647]
- Enable CONFIG_PWRSEQ_{SIMPLIE,EMMC} on aarch64 (Charles Mirabile)
- Fix SERIAL_SC16IS7XX configs for Fedora (Justin M. Forbes)
- Enable ALSA (CONFIG_SND) on aarch64 (Charles Mirabile) [RHEL-40411]
- redhat: Remove DIST_BRANCH variable (Eder Zulian)
- gitlab-ci: merge ark-latest before tagging cki-gating (Michael Hofmann)
- gitlab-ci: do not merge ark-latest for gating pipelines for Rawhide (Michael Hofmann)
- disable CONFIG_KVM_INTEL_PROVE_VE (Paolo Bonzini)
- redhat: remove the merge subtrees script (Derek Barbosa)
- redhat: rhdocs: delete .get_maintainer.conf (Derek Barbosa)
- redhat: rhdocs: Remove the rhdocs directory (Derek Barbosa)
- redhat/configs: Disable CONFIG_QLA3XXX (Kamal Heib) [RHEL-36646]
- redhat/configs: fedora: Enable some drivers for IPU6 support (Hans de Goede)
- redhat: add missing UKI_secureboot_cert hunk (Patrick Talbert)
- redhat/kernel.spec: keep extra modules in original directories (Jan Stancek)
- redhat/configs: Move CONFIG_BLK_CGROUP_IOCOST=y to common/generic (Waiman Long)
- Turn on CONFIG_MFD_QCOM_PM8008 for Fedora aarch64 (Justin M. Forbes)
- redhat: Build IMA CA certificate into the Fedora kernel (Coiby Xu)
- Move CONFIG_RAS_FMPM to the proper location (Aristeu Rozanski)
- redhat/configs: Remove CONFIG_NET_ACT_IPT (Ivan Vecera)
- gitlab-ci: add kernel-automotive pipelines (Michael Hofmann)
- Enable CEC support for TC358743 (Peter Robinson)
- fedora: arm: Enable ARCH_R9A09G057 (Peter Robinson)
- fedora: updates for the 6.10 kernel (Peter Robinson)
- fedora: arm: Enable the MAX96706 GMSL module (Peter Robinson)
- redhat: Switch UKI to using its own SecureBoot cert (from system-sb-certs) (Jan Stancek)
- redhat: Add RHEL specifc .sbat section to UKI (Jan Stancek)
- kernel.spec: add iommu selftests to kernel-selftests-internal (Eder Zulian) [RHEL-32895]
- redhat/configs: fedora: aarch64: Re-enable CUSE (Neal Gompa)
- redhat: pass correct RPM_VMLINUX_H to bpftool install (Jan Stancek)
- rh_flags: Rename rh_features to rh_flags (Ricardo Robaina) [RHEL-32987]
- kernel: rh_features: fix reading empty feature list from /proc (Ricardo Robaina) [RHEL-32987]
- rh_features: move rh_features entry to sys/kernel (Ricardo Robaina) [RHEL-32987]
- rh_features: convert to atomic allocation (Ricardo Robaina) [RHEL-32987]
- add rh_features to /proc (Ricardo Robaina) [RHEL-32987]
- add support for rh_features (Ricardo Robaina) [RHEL-32987]
- Drop kexec_load syscall support (Baoquan He)
- New configs in lib/kunit (Fedora Kernel Team)
- Turn off KUNIT_FAULT_TEST as it causes problems for CI (Justin M. Forbes)
- Add a config entry in pending for CONFIG_DRM_MSM_VALIDATE_XML (Justin M. Forbes)
- Flip CONFIG_SND_SOC_CS35L56_SPI in pending to avoid a mismatch (Justin M. Forbes)
- Fix up a mismatch for RHEL (Justin M. Forbes)
- Reset changelog after rebase (Justin M. Forbes)
- Reset RHEL_RELEASE to 0 for 6.10 (Justin M. Forbes)
- configs: move CONFIG_BLK_DEV_UBLK into rhel/configs/generic (Ming Lei)
- configs: move CONFIG_BLK_SED_OPAL into redhat/configs/common/generic (Ming Lei)
- RHEL-21097: rhel: aarch64 stop blocking a number of HW sensors (Peter Robinson)
- redhat/configs: enable RTL8822BU for rhel (Jose Ignacio Tornos Martinez)
- redhat/configs: remove CONFIG_DMA_PERNUMA_CMA and switch CONFIG_DMA_NUMA_CMA off (Jerry Snitselaar)
- redhat: add IMA certificates (Jan Stancek)
- redhat/kernel.spec: fix typo in move_kmod_list() variable (Jan Stancek)
- redhat: make filtermods.py less verbose by default (Jan Stancek)
- scsi: sd: condition probe_type under RHEL_DIFFERENCES (Eric Chanudet)
- scsi: sd: remove unused sd_probe_types (Eric Chanudet)
- Turn on INIT_ON_ALLOC_DEFAULT_ON for Fedora (Justin M. Forbes)
- Consolidate configs to common for 6.9 (Justin M. Forbes)
- redhat/rhel_files: move tipc.ko and tipc_diag.ko to modules-extra (Xin Long) [RHEL-23931]
- redhat: move amd-pstate-ut.ko to modules-internal (Jan Stancek)
- redhat/configs: enable CONFIG_LEDS_TRIGGER_NETDEV also for RHEL (Michal Schmidt) [RHEL-32110]
- redhat/configs: Remove CONFIG_AMD_IOMMU_V2 (Jerry Snitselaar)
- Set DEBUG_INFO_BTF_MODULES for Fedora (Justin M. Forbes)
- redhat: Use redhatsecureboot701 for ppc64le (Jan Stancek)
- redhat: switch the kernel package to use certs from system-sb-certs (Jan Stancek)
- redhat: replace redhatsecureboot303 signing key with redhatsecureboot601 (Jan Stancek)
- redhat: drop certificates that were deprecated after GRUB's BootHole flaw (Jan Stancek)
- redhat: correct file name of redhatsecurebootca1 (Jan Stancek)
- redhat: align file names with names of signing keys for ppc and s390 (Jan Stancek)
- redhat/configs: Enable CONFIG_DM_VDO in RHEL (Benjamin Marzinski)
- redhat/configs: Enable DRM_NOUVEAU_GSP_DEFAULT everywhere (Neal Gompa)
- kernel.spec: adjust for livepatching kselftests (Joe Lawrence)
- redhat/configs: remove CONFIG_TEST_LIVEPATCH (Joe Lawrence)
- Turn on CONFIG_RANDOM_KMALLOC_CACHES for Fedora (Justin M. Forbes)
- Set Fedora configs for 6.9 (Justin M. Forbes)
- gitlab-ci: enable pipelines with c10s buildroot (Michael Hofmann)
- Turn on ISM for Fedora (Justin M. Forbes)
- redhat/configs: enable CONFIG_TEST_LOCKUP for non-debug kernels (Čestmír Kalina)
- redhat/rhel_files: add test_lockup.ko to modules-extra (Čestmír Kalina)
- Turn off some Fedora UBSAN options to avoid false positives (Justin M. Forbes)
- fedora: aarch64: Enable a QCom Robotics platforms requirements (Peter Robinson)
- fedora: updates for 6.9 merge window (Peter Robinson)
- gitlab-ci: rename GitLab jobs ark -> rawhide (Michael Hofmann)
- gitlab-ci: harmonize DataWarehouse tree names (Michael Hofmann)
- redhat/configs: Enable CONFIG_INTEL_IOMMU_SCALABLE_MODE_DEFAULT_ON for rhel (Jerry Snitselaar)
- spec: make sure posttrans script doesn't fail if /boot is non-POSIX (glb)
- Turn on UBSAN for Fedora (Justin M. Forbes)
- Turn on XEN_BALLOON_MEMORY_HOTPLUG for Fedora (Justin M. Forbes)
- docs: point out that python3-pyyaml is now required (Thorsten Leemhuis)
- Use LLVM=1 for clang_lto build (Nikita Popov)
- redhat: fix def_variants.yaml check (Jan Stancek)
- redhat: sanity check yaml files (Jan Stancek)
- spec: rework filter-mods and mod-denylist (Jan Stancek)
- redhat/configs: remove CONFIG_INTEL_MENLOW as it is obsolete. (David Arcari)
- arch/x86: Fix XSAVE check for x86_64-v2 check (Prarit Bhargava)
- redhat/Makefile.variables: unquote a variable (Thorsten Leemhuis)
- redhat/configs: build in Tegra210 SPI driver (Mark Salter)
- redhat/configs: aarch64: Enable ARM_FFA driver (Mark Salter)
- Base automotive-devel on rt-devel (Don Zickus)
- redhat/configs: Enable CONFIG_AMDTEE for x86 (David Arcari)
- redhat/configs: enable CONFIG_TEST_LOCKUP for debug kernel (Čestmír Kalina)
- kernel.spec: fix libperf-debuginfo content (Jan Stancek)
- Turn on DM_VDO for Fedora (Justin M. Forbes)
- redhat: make libperf-devel require libperf %%{version}-%%{release} (Jan Stancek)
- kernel.spec: drop custom mode also for System.map ghost entry (Jan Stancek)
- Octopus merges are too conservative, serialize instead (Don Zickus)
- Add tracking branches for rt-devel (Don Zickus)
- all: clean-up i915 (Peter Robinson)
- Turn on CONFIG_READ_ONLY_THP_FOR_FS for Fedora (Justin M. Forbes)
- redhat/kernel.spec.template: fix rtonly build (Jan Stancek)
- redhat/kernel.spec.template: add extra flags for tools build (Scott Weaver)
- Add iio-test-gts to mod-internal.list (Thorsten Leemhuis)
- redhat/kernel.spec.template: update license (Scott Weaver)
- Fix typo in maintaining.rst file (Augusto Caringi)
- Enable DRM_CDNS_DSI_J721E for fedora (Andrew Halaney)
- gitlab-ci: do not merge ark-latest for gating pipelines (Michael Hofmann)
- fedora: Enable MCP9600 (Peter Robinson)
- redhat/configs: Enable & consolidate BF-3 drivers config (Luiz Capitulino)
- redhat: Fix RT kernel kvm subpackage requires (Juri Lelli)
- Add new of_test module to mod-internal.list (Thorsten Leemhuis)
- Add new string kunit modules to mod-internal.list (Thorsten Leemhuis)
- redhat/kernel.spec.template: enable cross for base/RT (Peter Robinson)
- redhat/kernel.spec.template: Fix cross compiling (Peter Robinson)
- arch/x86/kernel/setup.c: fixup rh_check_supported (Scott Weaver)
- Enable CONFIG_USB_ONBOARD_HUB for RHEL (Charles Mirabile)
- redhat/Makefile.cross: Add CROSS_BASEONLY (Prarit Bhargava)
- gitlab-ci: fix ark-latest merging for parent pipelines running in forks (Michael Hofmann)
- lsm: update security_lock_kernel_down (Scott Weaver)
- Fix changelog after rebase (Augusto Caringi)
- redhat: remove "END OF CHANGELOG" marker from kernel.changelog (Herton R. Krzesinski)
- gitlab-ci: enable all variants for rawhide/eln builder image gating (Michael Hofmann)
- Fedora: enable Microchip and their useful drivers (Peter Robinson)
- spec: suppress "set +x" output (Jan Stancek)
- redhat/configs: Disable CONFIG_RDMA_SIW (Kamal Heib)
- redhat/configs: Disable CONFIG_RDMA_RXE (Kamal Heib)
- redhat/configs: Disable CONFIG_MLX4 (Kamal Heib)
- redhat/configs: Disable CONFIG_INFINIBAND_HFI1 and CONFIG_INFINIBAND_RDMAVT (Kamal Heib)
- Consolidate 6.8 configs to common (Justin M. Forbes)
- Remove rt-automated and master-rt-devel logic (Don Zickus)
- Add support for CI octopus merging (Don Zickus)
- redhat/configs: Disable CONFIG_INFINIBAND_VMWARE_PVRDMA (Kamal Heib)
- gitlab-ci: fix merge tree URL for gating pipelines (Michael Hofmann)
- Revert "net: bump CONFIG_MAX_SKB_FRAGS to 45" (Marcelo Ricardo Leitner)
- uki: use systemd-pcrphase dracut module (Gerd Hoffmann)
- Add libperf-debuginfo subpackage (Justin M. Forbes)
- redhat/kernel.spec.template: Add log_msg macro (Prarit Bhargava)
- redhat/configs: Disable CONFIG_INFINIBAND_USNIC (Kamal Heib)
- Enable CONFIG_BMI323_I2C=m for Fedora x86_64 builds (Hans de Goede)
- gitlab-ci: drop test_makefile job (Scott Weaver)
- Enable merge-rt pipeline (Don Zickus)
- kernel.spec: include the GDB plugin in kernel-debuginfo (Ondrej Mosnacek)
- Turn on DRM_NOUVEAU_GSP_DEFAULT for Fedora (Justin M. Forbes)
- Set late new config HDC3020 for Fedora (Justin M. Forbes)
- redhat/self-test: Update CROSS_DISABLED_PACKAGES (Prarit Bhargava)
- redhat: Do not build libperf with cross builds (Prarit Bhargava)
- redhat/configs: enable CONFIG_PINCTRL_INTEL_PLATFORM for RHEL (David Arcari)
- redhat/configs: enable CONFIG_PINCTRL_METEORPOINT for RHEL (David Arcari)
- redhat/configs: intel pinctrl config cleanup (David Arcari)
- redhat/configs: For aarch64/RT, default kstack randomization off (Jeremy Linton)
- redhat/Makefile: remove an unused target (Ondrej Mosnacek)
- redhat/Makefile: fix setup-source and document its caveat (Ondrej Mosnacek)
- redhat/Makefile: fix race condition when making the KABI tarball (Ondrej Mosnacek)
- redhat/Makefile: refactor KABI tarball creation (Ondrej Mosnacek)
- Turn XFS_SUPPORT_V4 back on for Fedora (Justin M. Forbes)
- Add xe to drm module filters (Justin M. Forbes)
- Turn off the DRM_XE_KUNIT_TEST for Fedora (Justin M. Forbes)
- Flip secureboot signature order (Justin M. Forbes)
- all: clean up some removed configs (Peter Robinson)
- redhat: add nvidia oot signing key (Dave Airlie)
- gitlab-ci: support CI for zfcpdump kernel on ELN (Michael Hofmann)
- Fedora configs for 6.8 (Justin M. Forbes)
- Turn off CONFIG_INTEL_VSC for Fedora (Justin M. Forbes)
- redhat/configs: rhel wireless requests (Jose Ignacio Tornos Martinez)
- spec: Set EXTRA_CXXFLAGS for perf demangle-cxx.o (Josh Stone) [2233269]
- Flip values for FSCACHE and NETFS_SUPPORT to avoid mismatch (Justin M. Forbes)
- Turn on SECURITY_DMESG_RESTRICT (Justin M. Forbes)
- redhat: forward-port genlog.py updates from c9s (Jan Stancek)
- arch/x86: mark x86_64-v1 and x86_64-v2 processors as deprecated (Prarit Bhargava)
- fedora: Enable more Renesas RZ platform drivers (Peter Robinson)
- fedora: a few aarch64 drivers and cleanups (Peter Robinson)
- fedora: cavium nitrox cnn55xx (Peter Robinson)
- Fix dist-get-buildreqs breakage around perl(ExtUtils::Embed) (Don Zickus)
- gitlab-ci: merge ark-latest fixes when running ELN pipelines (Michael Hofmann)
- gitlab-ci: use all arches for container image gating (Michael Hofmann)
- Add new os-build targets: rt-devel and automotive-devel (Don Zickus)
- Remove defines forcing tools on, they override cmdline (Justin M. Forbes)
- Remove separate license tag for libperf (Justin M. Forbes)
- Don't use upstream bpftool version for Fedora package (Justin M. Forbes)
- Don't ship libperf.a in libperf-devel (Justin M. Forbes)
- add libperf packages and enable perf, libperf, tools and bpftool packages (Thorsten Leemhuis)
- Add scaffolding to build the kernel-headers package for Fedora (Justin M. Forbes)
- redhat/spec: use distro CFLAGS when building bootstrap bpftool (Artem Savkov)
- spec: use just-built bpftool for vmlinux.h generation (Yauheni Kaliuta) [2120968]
- gitlab-ci: enable native tools for Rawhide CI (Michael Hofmann)
- Revert "Merge branch 'fix-kabi-build-race' into 'os-build'" (Justin M. Forbes)
- redhat: configs: fedora: Enable sii902x bridge chip driver (Erico Nunes)
- Enable CONFIG_TCP_CONG_ILLINOIS for RHEL (Davide Caratti)
- redhat/Makefile: fix setup-source and document its caveat (Ondrej Mosnacek)
- redhat/Makefile: fix race condition when making the KABI tarball (Ondrej Mosnacek)
- redhat/Makefile: refactor KABI tarball creation (Ondrej Mosnacek)
- redhat/configs: Remove HOTPLUG_CPU0 configs (Prarit Bhargava)
- gitlab-ci: merge ark-latest before building in MR pipelines (Michael Hofmann)
- CI: include aarch64 in CKI container image gating (Tales Aparecida)
- redhat: spec: Fix update_scripts run for CentOS builds (Neal Gompa)
- New configs in drivers/crypto (Fedora Kernel Team)
- net: bump CONFIG_MAX_SKB_FRAGS to 45 (Marcelo Ricardo Leitner)
- Enable CONFIG_MARVELL_88Q2XXX_PHY (Izabela Bakollari)
- Remove CONFIG_NET_EMATCH_STACK file for RHEL (Justin M. Forbes)
- CONFIG_NETFS_SUPPORT should be m after the merge (Justin M. Forbes)
- Turn FSCACHE and NETFS from m to y in pending (Justin M. Forbes)
- Turn on CONFIG_TCP_AO for Fedora (Justin M. Forbes)
- Turn on IAA_CRYPTO_STATS for Fedora (Justin M. Forbes)
- fedora: new drivers and cleanups (Peter Robinson)
- Turn on Renesas RZ for Fedora IOT rhbz2257913 (Justin M. Forbes)
- redhat: filter-modules.sh.rhel: add dell-smm-hwmon (Scott Weaver)
- Add CONFIG_INTEL_MEI_GSC_PROXY=m for DRM 9.4 stable backport (Mika Penttilä)
- Set configs for ZRAM_TRACK_ENTRY_ACTIME (Justin M. Forbes)
- Add python3-pyyaml to buildreqs for kernel-docs (Justin M. Forbes)
- Add nb7vpq904m to singlemods for ppc64le (Thorsten Leemhuis)
- include drm bridge helpers in kernel-core package (Thorsten Leemhuis)
- Add dell-smm-hwmon to singlemods (Thorsten Leemhuis)
- Add drm_gem_shmem_test to mod-internal.list (Thorsten Leemhuis)
- redhat: kABI: add missing RH_KABI_SIZE_ALIGN_CHECKS Kconfig option (Sabrina Dubroca)
- redhat: rh_kabi: introduce RH_KABI_EXCLUDE_WITH_SIZE (Sabrina Dubroca)
- redhat: rh_kabi: move semicolon inside __RH_KABI_CHECK_SIZE (Sabrina Dubroca)
- Fix up ZRAM_TRACK_ENTRY_ACTIME in pending (Justin M. Forbes)
- random: replace import_single_range() with import_ubuf() (Justin M. Forbes)
- Flip CONFIG_INTEL_PMC_CORE to m for Fedora (Justin M. Forbes)
- Add CONFIG_ZRAM_TRACK_ENTRY_ACTIME=y to avoid a mismatch (Justin M. Forbes)
- common: cleanup MX3_IPU (Peter Robinson)
- all: The Octeon MDIO driver is aarch64/mips (Peter Robinson)
- common: rtc: remove bq4802 config (Peter Robinson)
- common: de-dupe MARVELL_GTI_WDT (Peter Robinson)
- all: Remove CAN_BXCAN (Peter Robinson)
- common: cleanup SND_SOC_ROCKCHIP (Peter Robinson)
- common: move RHEL DP83867_PHY to common (Peter Robinson)
- common: Make ASYMMETRIC_KEY_TYPE enable explicit (Peter Robinson)
- common: Disable aarch64 ARCH_MA35 universally (Peter Robinson)
- common: arm64: enable Tegra234 pinctrl driver (Peter Robinson)
- rhel: arm64: Enable qoriq thermal driver (Peter Robinson)
- common: aarch64: Cleanup some i.MX8 config options (Peter Robinson)
- all: EEPROM_LEGACY has been removed (Peter Robinson)
- all: rmeove AppleTalk hardware configs (Peter Robinson)
- all: cleanup: remove references to SLOB (Peter Robinson)
- all: cleanup: Drop unnessary BRCMSTB configs (Peter Robinson)
- all: net: remove retired network schedulers (Peter Robinson)
- all: cleanup removed CONFIG_IMA_TRUSTED_KEYRING (Peter Robinson)
- BuildRequires: lld for build with selftests for x86 (Jan Stancek)
- spec: add keyutils to selftest-internal subpackage requirements (Artem Savkov) [2166911]
- redhat/spec: exclude liburandom_read.so from requires (Artem Savkov) [2120968]
- rtla: sync summary text with upstream and update Requires (Jan Stancek)
- uki-virt: add systemd-sysext dracut module (Gerd Hoffmann)
- uki-virt: add virtiofs dracut module (Gerd Hoffmann)
- common: disable the FB device creation (Peter Robinson)
- s390x: There's no FB on Z-series (Peter Robinson)
- fedora: aarch64: enable SM_VIDEOCC_8350 (Peter Robinson)
- fedora: arm64: enable ethernet on newer TI industrial (Peter Robinson)
- fedora: arm64: Disable VIDEO_IMX_MEDIA (Peter Robinson)
- fedora: use common config for Siemens Simatic IPC (Peter Robinson)
- fedora: arm: enable Rockchip SPI flash (Peter Robinson)
- fedora: arm64: enable DRM_TI_SN65DSI83 (Peter Robinson)
- kernel.spec: remove kernel-smp reference from scripts (Jan Stancek)
- redhat: do not compress the full kernel changelog in the src.rpm (Herton R. Krzesinski)
- Auto consolidate configs for the 6.7 cycle (Justin M. Forbes)
- Enable sound for a line of Huawei laptops (TomZanna)
- fedora: a few cleanups and driver enablements (Peter Robinson)
- fedora: arm64: cleanup Allwinner Pinctrl drivers (Peter Robinson)
- fedora: aarch64: Enable some DW drivers (Peter Robinson)
- redhat: ship all the changelog from source git into kernel-doc (Herton R. Krzesinski)
- redhat: create an empty changelog file when changing its name (Herton R. Krzesinski)
- redhat/self-test: Remove --all from git query (Prarit Bhargava)
- Disable accel drivers for Fedora x86 (Kate Hsuan)
- redhat: scripts: An automation script for disabling unused driver for x86 (Kate Hsuan)
- Fix up Fedora LJCA configs and filters (Justin M. Forbes)
- Fedora configs for 6.7 (Justin M. Forbes)
- Some Fedora config updates for MLX5 (Justin M. Forbes)
- Turn on DRM_ACCEL drivers for Fedora (Justin M. Forbes)
- redhat: enable the kfence test (Nico Pache)
- redhat/configs: Enable UCLAMP_TASK for PipeWire and WirePlumber (Neal Gompa)
- Turn on CONFIG_SECURITY_DMESG_RESTRICT for Fedora (Justin M. Forbes)
- Turn off shellcheck for the fedora-stable-release script (Justin M. Forbes)
- Add some initial Fedora stable branch script to redhat/scripts/fedora/ (Justin M. Forbes)
- redhat: disable iptables-legacy compatibility layer (Florian Westphal)
- redhat: disable dccp conntrack support (Florian Westphal)
- configs: enable netfilter_netlink_hook in fedora too (Florian Westphal)
- ext4: Mark mounting fs-verity filesystems as tech-preview (Alexander Larsson)
- erofs: Add tech preview markers at mount (Alexander Larsson)
- Enable fs-verity (Alexander Larsson)
- Enable erofs (Alexander Larsson)
- aarch64: enable uki (Gerd Hoffmann)
- redhat: enable CONFIG_SND_SOC_INTEL_SOF_DA7219_MACH as a module for x86 (Patrick Talbert)
- Turn CONFIG_MFD_CS42L43_SDW on for RHEL (Justin M. Forbes)
- Enable cryptographic acceleration config flags for PowerPC (Mamatha Inamdar)
- Also make vmlinuz-virt.efi world readable (Zbigniew Jędrzejewski-Szmek)
- Drop custom mode for System.map file (Zbigniew Jędrzejewski-Szmek)
- Add drm_exec_test to mod-internal.list for depmod to succeed (Mika Penttilä)
- RHEL 9.4 DRM backport (upto v6.6 kernel), sync Kconfigs (Mika Penttilä)
- Turn on USB_DWC3 for Fedora (rhbz 2250955) (Justin M. Forbes)
- redhat/configs: Move IOMMUFD to common (Alex Williamson)
- redhat: Really remove cpupower files (Prarit Bhargava)
- redhat: remove update_scripts.sh (Prarit Bhargava)
- Fix s390 zfcpfdump bpf build failures for cgroups (Don Zickus)
- Flip CONFIG_NVME_AUTH to m in pending (Justin M. Forbes)
- Turn CONFIG_SND_SOC_INTEL_AVS_MACH_RT5514 on for Fedora x86 (Jason Montleon)
- kernel/rh_messages.c: Mark functions as possibly unused (Prarit Bhargava)
- Add snd-hda-cirrus-scodec-test to mod-internal.list (Scott Weaver)
- Turn off BPF_SYSCALL in pending for zfcpdump (Justin M. Forbes)
- Add mean_and_variance_test to mod-internal.list (Justin M. Forbes)
- Add cfg80211-tests and mac80211-tests to mod-internal.list (Justin M. Forbes)
- Turn on CONFIG_MFD_CS42L43_SDW for RHEL in pending (Justin M. Forbes)
- Turn on bcachefs for Fedora (Justin M. Forbes)
- redhat: configs: fedora: Enable QSEECOM and friends (Andrew Halaney)
- Add clk-fractional-divider_test to mod-internal.list (Thorsten Leemhuis)
- Add gso_test to mod-internal.list (Thorsten Leemhuis)
- Add property-entry-test to mod-internal.list (Thorsten Leemhuis)
- Fedora 6.7 configs part 1 (Justin M. Forbes)
- [Scheduled job] Catch config mismatches early during upstream merge (Don Zickus)
- redhat/self-test: Update data for KABI xz change (Prarit Bhargava)
- redhat/scripts: Switch KABI tarballs to xz (Prarit Bhargava)
- redhat/kernel.spec.template: Switch KABI compression to xz (Prarit Bhargava)
- redhat: self-test: Use a more complete SRPM file suffix (Andrew Halaney)
- redhat: makefile: remove stray rpmbuild --without (Eric Chanudet)
- Consolidate configs into common for 6.6 (Justin M. Forbes)
- Updated Fedora configs (Justin M. Forbes)
- Turn on UFSHCD for Fedora x86 (Justin M. Forbes)
- redhat: configs: generic: x86: Disable CONFIG_VIDEO_OV01A10 for x86 platform (Hans de Goede)
- redhat: remove pending-rhel CONFIG_XFS_ASSERT_FATAL file (Patrick Talbert)
- New configs in fs/xfs (Fedora Kernel Team)
- crypto: rng - Override drivers/char/random in FIPS mode (Herbert Xu)
- random: Add hook to override device reads and getrandom(2) (Herbert Xu)
- redhat/configs: share CONFIG_ARM64_ERRATUM_2966298 between rhel and fedora (Mark Salter)
- configs: Remove S390 IOMMU config options that no longer exist (Jerry Snitselaar)
- redhat: docs: clarify where bugs and issues are created (Scott Weaver)
- redhat/scripts/rh-dist-git.sh does not take any arguments: fix error message (Denys Vlasenko)
- Add target_branch for gen_config_patches.sh (Don Zickus)
- redhat: disable kunit by default (Nico Pache)
- redhat/configs: enable the AMD_PMF driver for RHEL (David Arcari)
- Make CONFIG_ADDRESS_MASKING consistent between fedora and rhel (Chris von Recklinghausen)
- CI: add ark-latest baseline job to tag cki-gating for successful pipelines (Michael Hofmann)
- CI: provide child pipelines for CKI container image gating (Michael Hofmann)
- CI: allow to run as child pipeline (Michael Hofmann)
- CI: provide descriptive pipeline name for scheduled pipelines (Michael Hofmann)
- CI: use job templates for variant variables (Michael Hofmann)
- redhat/kernel.spec.template: simplify __modsign_install_post (Jan Stancek)
- Fedora filter updates after configs (Justin M. Forbes)
- Fedora configs for 6.6 (Justin M. Forbes)
- redhat/configs: Freescale Layerscape SoC family (Steve Best)
- Add clang MR/baseline pipelines (Michael Hofmann)
- CI: Remove unused kpet_tree_family (Nikolai Kondrashov)
- Add clang config framework (Don Zickus)
- Apply partial snippet configs to all configs (Don Zickus)
- Remove unpackaged kgcov config files (Don Zickus)
- redhat/configs: enable missing Kconfig options for Qualcomm RideSX4 (Brian Masney)
- enable CONFIG_ADDRESS_MASKING for x86_64 (Chris von Recklinghausen)
- common: aarch64: enable NXP Flex SPI (Peter Robinson)
- fedora: Switch TI_SCI_CLK and TI_SCI_PM_DOMAINS symbols to built-in (Javier Martinez Canillas)
- kernel.spec: adjust build option comment (Michael Hofmann)
- kernel.spec: allow to enable arm64_16k variant (Michael Hofmann)
- gitlab-ci: enable build-only pipelines for Rawhide/16k/aarch64 (Michael Hofmann)
- kernel.spec.template: Fix --without bpftool (Prarit Bhargava)
- redhat/configs: NXP BBNSM Power Key Driver (Steve Best)
- redhat/self-test: Update data for cross compile fields (Prarit Bhargava)
- redhat/Makefile.cross: Add message for disabled subpackages (Prarit Bhargava)
- redhat/Makefile.cross: Update cross targets with disabled subpackages (Prarit Bhargava)
- Remove XFS_ASSERT_FATAL from pending-fedora (Justin M. Forbes)
- Change default pending for XFS_ONLINE_SCRUB_STATSas it now selects XFS_DEBUG (Justin M. Forbes)
- gitlab-ci: use --with debug/base to select kernel variants (Michael Hofmann)
- kernel.spec: add rpmbuild --without base option (Michael Hofmann)
- redhat: spec: Fix typo for kernel_variant_preun for 16k-debug flavor (Neal Gompa)
- Turn off appletalk for fedora (Justin M. Forbes)
- New configs in drivers/media (Fedora Kernel Team)
- redhat/docs: Add a mention of bugzilla for bugs (Prarit Bhargava)
- Fix the fixup of Fedora release (Don Zickus)
- Fix Fedora release scheduled job (Don Zickus)
- Move squashfs to kernel-modules-core (Justin M. Forbes)
- redhat: Explicitly disable CONFIG_COPS (Vitaly Kuznetsov)
- redhat: Add dist-check-licenses target (Vitaly Kuznetsov)
- redhat: Introduce "Verify SPDX-License-Identifier tags" selftest (Vitaly Kuznetsov)
- redhat: Use kspdx-tool output for the License: field (Vitaly Kuznetsov)
- Rename pipeline repo branch and DW tree names (Michael Hofmann)
- Adjust comments that refer to ARK in a Rawhide context (Michael Hofmann)
- Rename variable names starting with ark- to rawhide- (Michael Hofmann)
- Rename trigger-ark to trigger-rawhide (Michael Hofmann)
- Fix up config mismatches for Fedora (Justin M. Forbes)
- redhat/configs: Texas Instruments Inc. K3 multicore SoC architecture (Steve Best)
- Flip CONFIG_VIDEO_V4L2_SUBDEV_API in pending RHEL due to mismatch (Justin M. Forbes)
- CONFIG_HW_RANDOM_HISI: move to common and set to m (Scott Weaver)
- Turn off CONFIG_MEMORY_HOTPLUG_DEFAULT_ONLINE for Fedora s390x (Justin M. Forbes)
- Disable tests for ELN realtime pipelines (Michael Hofmann)
- New configs in mm/Kconfig (Fedora Kernel Team)
- Flip CONFIG_SND_SOC_CS35L56_SDW to m and clean up (Justin M. Forbes)
- Add drm_exec_test to mod-internal.list (Thorsten Leemhuis)
- Add new pending entry for CONFIG_SND_SOC_CS35L56_SDW to fix mismatch (Justin M. Forbes)
- Fix tarball creation logic (Don Zickus)
- redhat: bump libcpupower soname to match upstream (Patrick Talbert)
- Turn on MEMFD_CREATE in pending as it is selected by CONFIG_TMPFS (Justin M. Forbes)
- redhat: drop unneeded build-time dependency gcc-plugin-devel (Coiby Xu)
- all: x86: move wayward x86 specific config home (Peter Robinson)
- all: de-dupe non standard config options (Peter Robinson)
- all: x86: clean up microcode loading options (Peter Robinson)
- common: remove unnessary CONFIG_SND_MESON_AXG* (Peter Robinson)
- redhat: Fix UKI install with systemd >= 254 (Vitaly Kuznetsov)
- redhat: Use named parameters for kernel_variant_posttrans()/kernel_variant_preun() (Vitaly Kuznetsov)
- redhat/kernel.spec.template: update compression variables to support zstd (Brian Masney)
- Consolidate configs to common for 6.5 (Justin M. Forbes)
- Remove unused config entry for Fedora (Justin M. Forbes)
- redhat/self-test: Remove rpmlint test (Prarit Bhargava)
- Remove the armv7 config directory from Fedora again (Justin M. Forbes)
- Enable CONFIG_EXPERT for both RHEL and Fedora (Justin M. Forbes)
- redhat/configs: Enable CONFIG_DEVICE_PRIVATE on aarch64 (David Hildenbrand) [2231407]
- redhat/configs: disable CONFIG_ROCKCHIP_ERRATUM_3588001 for RHEL (Mark Salter)
- redhat: shellcheck fixes (Prarit Bhargava)
- redhat/configs: enable tegra114 SPI (Mark Salter)
- all: properly cleanup firewire once and for all (Peter Robinson)
- Fix up filters for Fedora (Justin M. Forbes)
- New configs in arch/x86 (Fedora Kernel Team)
- Add an armv7 directory back for the Fedora configs (Justin M. Forbes)
- Fedora 6.5 config updates (Justin M. Forbes)
- Turn off DMABUF_SYSFS_STATS (Justin M. Forbes)
- CI: rawhide_release: switch to using script to push (Don Zickus)
- redhat/self-test: Update self-test data (Prarit Bhargava)
- redhat/scripts/cross-compile: Update download_cross.sh (Prarit Bhargava)
- redhat/Makefile.cross: Remove ARCH selection code (Prarit Bhargava)
- redhat/Makefile.cross: Update script (Prarit Bhargava)
- Fix interruptible non MR jobs (Michael Hofmann)
- all: run evaluate_configs to de-dupe merged aarch64 (Peter Robinson)
- all: arm: merge the arm and arm/aarch64 (Peter Robinson)
- fedora: remove ARMv7 AKA armhfp configurations (Peter Robinson)
- fedora: remove ARMv7 AKA armhfp support (Peter Robinson)
- redhat/configs: enable CONFIG_VIRTIO_MEM on aarch64 (David Hildenbrand) [2044155]
- redhat/configs: enable CONFIG_MEMORY_HOTREMOVE aarch64 (David Hildenbrand) [2062054]
- redhat: Add arm64-16k kernel flavor scaffold for 16K page-size'd AArch64 (Neal Gompa)
- fedora: enable i3c on aarch64 (Peter Robinson)
- redhat/configs: Remove `CONFIG_HZ_1000 is not set` for aarch64 (Enric Balletbo i Serra)
- redhat/configs: turn on the framework for SPI NOR for ARM (Steve Best)
- configs: add new ChromeOS UART driver (Mark Langsdorf)
- configs: add new ChromeOS Human Presence Sensor (Mark Langsdorf)
- redhat/configs: Enable CONFIG_NVIDIA_WMI_EC_BACKLIGHT for both Fedora and RHEL (Kate Hsuan)
- redhat/configs: Texas Instruments INA3221 driver (Steve Best)
- arm: i.MX: Some minor NXP i.MX cleanups (Peter Robinson)
- Description: Set config for Tegra234 pinctrl driver (Joel Slebodnick)
- Update RPM Scriptlet for kernel-install Changes (Jonathan Steffan)
- [CI] add exit 0 to the end of CI scripts (Don Zickus)
- redhat: configs: Disable CONFIG_CRYPTO_STATS since performance issue for storage (Kate Hsuan) [2227793]
- Remove obsolete variable from gitlab-ci.yml (Ondrej Kinst)
- redhat/configs: Move GVT-g to Fedora only (Alex Williamson)
- [CI] Make sure we are on correct branch before running script (Don Zickus)
- CI: ark-update-configs: sync push command and output (Don Zickus)
- CI: ark-update-configs: misc changes (Don Zickus)
- CI: sync ark-create-release push commands with output (Don Zickus)
- CI: ark-create-release: Add a robust check if nothing changed (Don Zickus)
- CI: Remove legacy tag check cruft (Don Zickus)
- CI: Introduce simple environment script (Don Zickus)
- redhat/configs: Disable FIREWIRE for RHEL (Prarit Bhargava)
- redhat/scripts/rh-dist-git.sh: print list of uploaded files (Denys Vlasenko)
- redhat/scripts/expand_srpm.sh: add missing function, robustify (Denys Vlasenko)
- redhat: Enable HSR and PRP (Felix Maurer)
- redhat/scripts/rh-dist-git.sh: fix outdated message and comment (Denys Vlasenko)
- redhat/configs: Disable CONFIG_I8K (Prarit Bhargava)
- Make sure posttrans script doesn't fail if restorecon is not installed (Daan De Meyer)
- Update filters for new config items (Justin M. Forbes)
- More Fedora 6.5 configs (Justin M. Forbes)
- redhat/configs: disable pre-UVC cameras for RHEL on aarch64 (Dean Nelson)
- redhat/configs: enable CONFIG_MEDIA_SUPPORT for RHEL on aarch64 (Dean Nelson)
- move ownership of /lib/modules/<ver>/ to kernel-core (Thorsten Leemhuis)
- Let kernel-modules-core own the files depmod generates. (Thorsten Leemhuis)
- redhat: configs: Enable CONFIG_TYPEC_STUSB160X for rhel on aarch64 (Desnes Nunes)
- Add filters for ptp_dfl_tod on Fedora (Justin M. Forbes)
- Fedora 6.5 configs part 1 (Justin M. Forbes)
- fedora: enable CONFIG_ZYNQMP_IPI_MBOX as a builtin in pending-fedora (Patrick Talbert)
- fedora: arm: some minor updates (Peter Robinson)
- fedora: bluetooth: enable AOSP extensions (Peter Robinson)
- fedora: wifi: tweak ZYDAS WiFI config options (Peter Robinson)
- scsi: sd: Add "probe_type" module parameter to allow synchronous probing (Ewan D. Milne) [2140017]
- redhat/configs: allow IMA to use MOK keys (Coiby Xu)
- Simplify documentation jobs (Michael Hofmann)
- Auto-cancel pipelines only on MRs (Michael Hofmann)
- CI: Call script directly (Don Zickus)
- CI: Remove stale TAG and Makefile cruft (Don Zickus)
- CI: Move os-build tracking to common area (Don Zickus)
- redhat: use the eln builder for daily jobs (Patrick Talbert)
- redhat: set CONFIG_XILINX_WINDOW_WATCHDOG as disabled in pending (Patrick Talbert)
- Add baseline ARK/ELN pipelines (Michael Hofmann)
- Simplify job rules (Michael Hofmann)
- Build ELN srpm for bot changes (Michael Hofmann)
- Run RH selftests for ELN (Michael Hofmann)
- Simplify job templates (Michael Hofmann)
- Extract rules to allow orthogonal configuration (Michael Hofmann)
- Require ELN pipelines if started automatically (Michael Hofmann)
- Add ARK debug pipeline (Michael Hofmann)
- Extract common parts of child pipeline job (Michael Hofmann)
- Move ARK pipeline variables into job template (Michael Hofmann)
- Simplify ARK pipeline rules (Michael Hofmann)
- Change pathfix.py to %%py3_shebang_fix (Justin M. Forbes)
- Turn on NET_VENDOR_QUALCOMM for Fedora to enable rmnet (Justin M. Forbes)
- redhat: add intel-m10-bmc-hwmon to filter-modules singlemods list (Patrick Talbert)
- fedira: enable pending-fedora CONFIG_CPUFREQ_DT_PLATDEV as a module (Patrick Talbert)
- redhat: fix the 'eln BUILD_TARGET' self-test (Patrick Talbert)
- redhat: update the self-test-data (Patrick Talbert)
- redhat: remove trailing space in dist-dump-variables output (Patrick Talbert)
- Allow ELN pipelines failures (Michael Hofmann)
- Enable cs-like CI (Michael Hofmann)
- Allow to auto-cancel redundant pipelines (Michael Hofmann)
- Remove obsolete unused trigger variable (Michael Hofmann)
- Fix linter warnings in .gitlab-ci.yml (Michael Hofmann)
- config: wifi: debug options for ath11k, brcm80211 and iwlwifi (Íñigo Huguet)
- redhat: allow dbgonly cross builds (Jan Stancek)
- redhat/configs: Clean up x86-64 call depth tracking configs (Waiman Long)
- redhat: move SND configs from pending-rhel to rhel (Patrick Talbert)
- Fix up armv7 configs for Fedora (Justin M. Forbes)
- redhat: Set pending-rhel x86 values for various SND configs (Patrick Talbert)
- redhat: update self-test data (Patrick Talbert)
- redhat: ignore SPECBPFTOOLVERSION/bpftoolversion in self-test create-data.sh (Patrick Talbert)
- fedora/rhel: Move I2C_DESIGNWARE_PLATFORM, I2C_SLAVE, & GPIOLIB from pending (Patrick Talbert)
- redhat/filter-modules.sh.rhel: add needed deps for intel_rapl_tpmi (Jan Stancek)
- fedora: Enable CONFIG_SPI_SLAVE (Patrick Talbert)
- fedora/rhel: enable I2C_DESIGNWARE_PLATFORM, I2C_SLAVE, and GPIOLIB (Patrick Talbert)
- fedora: Enable CONFIG_SPI_SLAVE in fedora-pending (Patrick Talbert)
- redhat: remove extra + (plus) from meta package Requires definitions (Patrick Talbert)
- Add intel-m10-bmc-hwmon to singlemods (Thorsten Leemhuis)
- Add hid-uclogic-test to mod-internal.list (Thorsten Leemhuis)
- Add checksum_kunit.ko to mod-internal.list (Thorsten Leemhuis)
- Add strcat_kunit to mod-internal.list (Thorsten Leemhuis)
- Add input_test to mod-intenal.list (Thorsten Leemhuis)
- Revert "Remove EXPERT from ARCH_FORCE_MAX_ORDER for aarch64" (Justin M. Forbes)
- Fix up rebase issue with CONFIG_ARCH_FORCE_MAX_ORDER (Justin M. Forbes)
- redhat/kernel.spec.template: Disable 'extracting debug info' messages (Prarit Bhargava)
- kernel/rh_messages.c: Another gcc12 warning on redundant NULL test (Florian Weimer) [2216678]
- redhat: fix signing for realtime and arm64_64k non-debug variants (Jan Stancek)
- redhat: treat with_up consistently (Jan Stancek)
- redhat: make with_realtime opt-in (Jan Stancek)
- redhat/configs: Disable qcom armv7 drippings in the aarch64 tree (Jeremy Linton)
- kernel.spec: drop obsolete ldconfig (Jan Stancek)
- Consolidate config items to common for 6.4 cycle (Justin M. Forbes)
- Turn on CO?NFIg_RMNET for Fedora (Justin M. Forbes)
- redhat/configs: enable CONFIG_MANA_INFINIBAND=m for ARK (Vitaly Kuznetsov)
- redhat/config: common: Enable CONFIG_GPIO_SIM for software development (Kate Hsuan)
- redhat: fix problem with RT kvm modules listed twice in rpm generation (Clark Williams)
- redhat: turn off 64k kernel builds with rtonly (Clark Williams)
- redhat: turn off zfcpdump for rtonly (Clark Williams)
- redhat: don't allow with_rtonly to turn on unsupported arches (Clark Williams)
- redhat: update self-test data for addition of RT and 64k-page variants (Clark Williams)
- redhat: fix realtime and efiuki build conflict (Jan Stancek)
- arm64-64k: Add new kernel variant to RHEL9/CS9 for 64K page-size'd ARM64 (Donald Dutile) [2153073]
- redhat: TEMPORARY set configs to deal with PREEMPT_RT not available (Clark Williams)
- redhat: TEMPORARY default realtime to off (Clark Williams)
- redhat: moved ARM errata configs to arm dir (Clark Williams)
- redhat: RT packaging changes (Clark Williams)
- redhat: miscellaneous commits needed due to CONFIG_EXPERT (Clark Williams)
- redhat: realtime config entries (Clark Williams)
- common: remove deleted USB PCCARD drivers (Peter Robinson)
- fedora: further cleanup of pccard/cardbus subsystem (Peter Robinson)
- common: properly disable PCCARD subsystem (Peter Robinson)
- redhat/configs: arm: enable SERIAL_TEGRA UART for RHEL (Mark Salter)
- redhat/configs: enable CONFIG_X86_AMD_PSTATE_UT (David Arcari)
- redhat/configs: Enable CONFIG_TCG_VTPM_PROXY for RHEL (Štěpán Horáček)
- redhat: do not package *.mod.c generated files (Denys Vlasenko)
- ALSA configuration changes for ARK/RHEL 9.3 (Jaroslav Kysela)
- spec: remove resolve_btfids from kernel-devel (Viktor Malik)
- Fix typo in filter-modules (Justin M. Forbes)
- redhat/configs: Enable CONFIG_INIT_STACK_ALL_ZERO for RHEL (Josh Poimboeuf)
- Remove CONFIG_ARCH_FORCE_MAX_ORDER for aarch64 (Justin M. Forbes)
- Fix up config and filter for PTP_DFL_TOD (Justin M. Forbes)
- redhat/configs: IMX8ULP pinctrl driver (Steve Best)
- redhat/configs: increase CONFIG_FRAME_WARN for Fedora on aarch64 (Brian Masney)
- redhat/configs: add two missing Kconfig options for the Thinkpad x13s (Brian Masney)
- Fedora configs for 6.4 (Justin M. Forbes)
- Change aarch64 CONFIG_ARCH_FORCE_MAX_ORDER to 10 for 4K pages (Justin M. Forbes)
- kernel.spec: remove "RPM_VMLINUX_H=$DevelDir/vmlinux.h" code chunk in %%install (Denys Vlasenko)
- redhat/configs: aarch64: Turn on Display for OnePlus 6 (Eric Curtin)
- redhat/configs: NXP i.MX93 pinctrl, clk, analog to digital converters (Steve Best)
- redhat/configs: Enable CONFIG_SC_GPUCC_8280XP for fedora (Andrew Halaney)
- redhat/configs: Enable CONFIG_QCOM_IPCC for fedora (Andrew Halaney)
- Add rv subpackage for kernel-tools (John Kacur) [2188441]
- redhat/configs: NXP i.MX9 family (Steve Best)
- redhat/genlog.py: add support to list/process zstream Jira tickets (Herton R. Krzesinski)
- redhat: fix duplicate jira issues in the resolves line (Herton R. Krzesinski)
- redhat: add support for Jira issues in changelog (Herton R. Krzesinski)
- redhat/configs: turn on IMX8ULP CCM Clock Driver (Steve Best)
- redhat: update filter-modules fsdrvs list to reference smb instead of cifs (Patrick Talbert)
- Turn off some debug options found to impact performance (Justin M. Forbes)
- wifi: rtw89: enable RTL8852BE card in RHEL (Íñigo Huguet)
- redhat/configs: enable TEGRA186_GPC_DMA for RHEL (Mark Salter)
- Move imx8m configs from fedora to common (Mark Salter)
- redhat/configs: turn on lpuart serial port support Driver (Steve Best) [2208834]
- Turn off DEBUG_VM for non debug Fedora kernels (Justin M. Forbes)
- Enable CONFIG_BT on aarch64 (Charles Mirabile)
- redhat/configs: turn on CONFIG_MARVELL_CN10K_TAD_PMU (Michal Schmidt) [2042240]
- redhat/configs: Fix enabling MANA Infiniband (Kamal Heib)
- Fix file listing for symvers in uki (Justin M. Forbes)
- Fix up some Fedora config items (Justin M. Forbes)
- enable efifb for Nvidia (Justin M. Forbes)
- kernel.spec: package unstripped test_progs-no_alu32 (Felix Maurer)
- Turn on NFT_CONNLIMIT for Fedora (Justin M. Forbes)
- Include the information about builtin symbols into kernel-uki-virt package too (Vitaly Kuznetsov)
- redhat/configs: Fix incorrect configs location and content (Vladis Dronov)
- redhat/configs: turn on CONFIG_MARVELL_CN10K_DDR_PMU (Michal Schmidt) [2042241]
- redhat: configs: generic: x86: Disable CONFIG_VIDEO_OV2740 for x86 platform (Kate Hsuan)
- Enable IO_URING for RHEL (Justin M. Forbes)
- Turn on IO_URING for RHEL in pending (Justin M. Forbes)
- redhat: Remove editconfig (Prarit Bhargava)
- redhat: configs: fix CONFIG_WERROR replace in build_configs (Jan Stancek)
- redhat/configs: enable Maxim MAX77620 PMIC for RHEL (Mark Salter)
- kernel.spec: skip kernel meta package when building without up (Jan Stancek)
- redhat/configs: enable RDMA_RXE for RHEL (Kamal Heib) [2022578]
- redhat/configs: update RPCSEC_GSS_KRB5 configs (Scott Mayhew)
- redhat/Makefile: Support building linux-next (Thorsten Leemhuis)
- redhat/Makefile: support building stable-rc versions (Thorsten Leemhuis)
- redhat/Makefile: Add target to print DISTRELEASETAG (Thorsten Leemhuis)
- Remove EXPERT from ARCH_FORCE_MAX_ORDER for aarch64 (Justin M. Forbes)
- Revert "Merge branch 'unstripped-no_alu32' into 'os-build'" (Patrick Talbert)
- configs: Enable CONFIG_PAGE_POOL_STATS for common/generic (Patrick Talbert)
- redhat/configs: enable CONFIG_DELL_WMI_PRIVACY for both RHEL and Fedora (David Arcari)
- kernel.spec: package unstripped test_progs-no_alu32 (Felix Maurer)
- bpf/selftests: fix bpf selftests install (Jerome Marchand)
- kernel.spec: add bonding selftest (Hangbin Liu)
- Change FORCE_MAX_ORDER for ppc64 to be 8 (Justin M. Forbes)
- kernel.spec.template: Add global compression variables (Prarit Bhargava)
- kernel.spec.template: Use xz for KABI (Prarit Bhargava)
- kernel.spec.template: Remove gzip related aarch64 code (Prarit Bhargava)
- Add apple_bl to filter-modules (Justin M. Forbes)
- Add handshake-test to mod-intenal.list (Justin M. Forbes)
- Add regmap-kunit to mod-internal.list (Justin M. Forbes)
- configs: set CONFIG_PAGE_POOL_STATS (Patrick Talbert)
- Add apple_bl to fedora module_filter (Justin M. Forbes)
- Fix up some config mismatches in new Fedora config items (Justin M. Forbes)
- redhat/configs: disable CONFIG_USB_NET_SR9700 for aarch64 (Jose Ignacio Tornos Martinez)
- Fix up the RHEL configs for xtables and ipset (Justin M. Forbes)
- ark: enable wifi on aarch64 (Íñigo Huguet)
- fedora: wifi: hermes: disable 802.11b driver (Peter Robinson)
- fedora: wifi: libertas: use the LIBERTAS_THINFIRM driver (Peter Robinson)
- fedora: wifi: disable Zydas vendor (Peter Robinson)
- redhat: fix python ValueError in error path of merge.py (Clark Williams)
- fedora: arm: minor updates (Peter Robinson)
- kernel.spec: Fix UKI naming to comply with BLS (Philipp Rudo)
- redhat/kernel.spec.template: Suppress 'extracting debug info' noise in build log (Prarit Bhargava)
- Fedora 6.3 configs part 2 (Justin M. Forbes)
- redhat/configs: Enable CONFIG_X86_KERNEL_IBT for Fedora and ARK (Josh Poimboeuf)
- kernel.spec: gcov: make gcov subpackages per variant (Jan Stancek)
- kernel.spec: Gemini: add Epoch to perf and rtla subpackages (Jan Stancek)
- kernel.spec: Gemini: fix header provides for upgrade path (Jan Stancek)
- redhat: introduce Gemini versioning (Jan Stancek)
- redhat: separate RPM version from uname version (Jan Stancek)
- redhat: introduce GEMINI and RHEL_REBASE_NUM variable (Jan Stancek)
- ipmi: ssif_bmc: Add SSIF BMC driver (Tony Camuso)
- common: minor de-dupe of parallel port configs (Peter Robinson)
- Fedora 6.3 configs part 1 (Justin M. Forbes)
- redhat: configs: Enable CONFIG_MEMTEST to enable memory test (Kate Hsuan)
- Update Fedora arm filters after config updates (Nicolas Chauvet)
- redhat/kernel.spec.template: Fix kernel-tools-libs-devel dependency (Prarit Bhargava)
- redhat: fix the check for the n option (Patrick Talbert)
- common: de-dupe some options that are the same (Peter Robinson)
- generic: remove deleted options (Peter Robinson)
- redhat/configs: enable CONFIG_INTEL_TCC_COOLING for RHEL (David Arcari)
- Update Fedora ppc filters after config updates (Justin M. Forbes)
- Update Fedora aarch64 filters after config updates (Justin M. Forbes)
- fedora: arm: Updates for 6.3 (Peter Robinson)
- redhat: kunit: cleanup NITRO config and enable rescale test (Nico Pache)
- kernel.spec: use %%{package_name} to fix kernel-devel-matched Requires (Jan Stancek)
- kernel.spec: use %%{package_name} also for abi-stablelist subpackages (Jan Stancek)
- kernel.spec: use %%{package_name} also for tools subpackages (Jan Stancek)
- generic: common: Parport and paride/ata cleanups (Peter Robinson)
- CONFIG_SND_SOC_CS42L83 is no longer common (Justin M. Forbes)
- configs: arm: bring some configs in line with rhel configs in c9s (Mark Salter)
- arm64/configs: Put some arm64 configs in the right place (Mark Salter)
- cleanup removed R8188EU config (Peter Robinson)
- Make RHJOBS container friendly (Don Zickus)
- Remove scmversion from kernel.spec.template (Don Zickus)
- redhat/configs: Enable CONFIG_SND_SOC_CS42L83 (Neal Gompa)
- Use RHJOBS for create-tarball (Don Zickus)
- Enable CONFIG_NET_SCH_FQ_PIE for Fedora (Justin M. Forbes)
- Make Fedora debug configs more useful for debug (Justin M. Forbes)
- redhat/configs: enable Octeon TX2 network drivers for RHEL (Michal Schmidt) [2040643]
- redhat/kernel.spec.template: fix installonlypkg for meta package (Jan Stancek)
- redhat: version two of Makefile.rhelver tweaks (Clark Williams)
- redhat/configs: Disable CONFIG_GCC_PLUGINS (Prarit Bhargava)
- redhat/kernel.spec.template: Fix typo for process_configs.sh call (Neal Gompa)
- redhat/configs: CONFIG_CRYPTO_SM3_AVX_X86_64 is x86 only (Vladis Dronov)
- redhat/configs: Enable CONFIG_PINCTRL_METEORLAKE in RHEL (Prarit Bhargava)
- fedora: enable new image sensors (Peter Robinson)
- redhat/self-test: Update self-test data (Prarit Bhargava)
- redhat/kernel.spec.template: Fix hardcoded "kernel" (Prarit Bhargava)
- redhat/configs/generate_all_configs.sh: Fix config naming (Prarit Bhargava)
- redhat/kernel.spec.template: Pass SPECPACKAGE_NAME to generate_all_configs.sh (Prarit Bhargava)
- kernel.spec.template: Use SPECPACKAGE_NAME (Prarit Bhargava)
- redhat/Makefile: Copy spec file (Prarit Bhargava)
- redhat: Change PACKAGE_NAME to SPECPACKAGE_NAME (Prarit Bhargava)
- redhat/configs: Support the virtio_mmio.device parameter in Fedora (David Michael)
- Revert "Merge branch 'systemd-boot-unsigned' into 'os-build'" (Patrick Talbert)
- redhat/Makefile: fix default values for dist-brew's DISTRO and DIST (Íñigo Huguet)
- Remove cc lines from automatic configs (Don Zickus)
- Add rtla-hwnoise files (Justin M. Forbes)
- redhat/kernel.spec.template: Mark it as a non-executable file (Neal Gompa)
- fedora: arm: Enable DRM_PANEL_HIMAX_HX8394 (Javier Martinez Canillas)
- redhat/configs: CONFIG_HP_ILO location fix (Vladis Dronov)
- redhat: Fix build for kselftests mm (Nico Pache)
- fix tools build after vm to mm rename (Justin M. Forbes)
- redhat/spec: Update bpftool versioning scheme (Viktor Malik)
- redhat/configs: CONFIG_CRYPTO_SM4_AESNI_AVX*_X86_64 is x86 only (Prarit Bhargava)
- redhat:  adapt to upstream Makefile change (Clark Williams)
- redhat:  modify efiuki specfile changes to use variants convention (Clark Williams)
- Turn off DEBUG_INFO_COMPRESSED_ZLIB for Fedora (Justin M. Forbes)
- redhat/kernel.spec.template: Fix RHEL systemd-boot-unsigned dependency (Prarit Bhargava)
- Add hashtable_test to mod-internal.list (Justin M. Forbes)
- Add more kunit tests to mod-internal.list for 6.3 (Justin M. Forbes)
- Flip CONFIG_I2C_ALGOBIT to m (Justin M. Forbes)
- Flip I2C_ALGOBIT to m to avoid mismatch (Justin M. Forbes)
- kernel.spec: move modules.builtin to kernel-core (Jan Stancek)
- Turn on IDLE_INJECT for x86 (Justin M. Forbes)
- Flip CONFIG_IDLE_INJECT in pending (Justin M. Forbes)
- redhat/configs: Enable CONFIG_V4L_TEST_DRIVERS related drivers (Enric Balletbo i Serra)
- redhat/configs: Enable UCSI_CCG support (David Marlin)
- Fix underline mark-up after text change (Justin M. Forbes)
- Turn on CONFIG_XFS_RT for Fedora (Justin M. Forbes)
- Consolidate common configs for 6.2 (Justin M. Forbes)
- aarch64: enable zboot (Gerd Hoffmann)
- redhat: remove duplicate pending-rhel config items (Patrick Talbert)
- Disable frame pointers (Justin M. Forbes)
- redhat/configs: update scripts and docs for ark -> rhel rename (Clark Williams)
- redhat/configs: rename ark configs dir to rhel (Clark Williams)
- Turn off CONFIG_DEBUG_INFO_COMPRESSED_ZLIB for ppc64le (Justin M. Forbes)
- kernel.spec: package unstripped kselftests/bpf/test_progs (Jan Stancek)
- kernel.spec: allow to package some binaries as unstripped (Jan Stancek)
- redhat/configs: Make merge.py portable for older python (Desnes Nunes)
- Fedora configs for 6.2 (Justin M. Forbes)
- redhat: Repair ELN build broken by the recent UKI changes (Vitaly Kuznetsov)
- redhat/configs: enable CONFIG_INET_DIAG_DESTROY (Andrea Claudi)
- Enable TDX Guest driver (Vitaly Kuznetsov)
- redhat/configs: Enable CONFIG_PCIE_PTM generically (Corinna Vinschen)
- redhat: Add sub-RPM with a EFI unified kernel image for virtual machines (Vitaly Kuznetsov)
- redhat/Makefile: Remove GIT deprecated message (Prarit Bhargava)
- Revert "redhat: configs: Disable xtables and ipset" (Phil Sutter)
- redhat/configs: Enable CONFIG_SENSORS_LM90 for RHEL (Mark Salter)
- Fix up SQUASHFS decompression configs (Justin M. Forbes)
- redhat/configs: enable CONFIG_OCTEON_EP as a module in ARK (Michal Schmidt) [2041990]
- redhat: ignore rpminspect runpath report on urandom_read selftest binaries (Herton R. Krzesinski)
- kernel.spec: add llvm-devel build requirement (Scott Weaver)
- Update self-test data to not expect debugbuildsenabled 0 (Justin M. Forbes)
- Turn off forced debug builds (Justin M. Forbes)
- Turn on debug builds for aarch64 Fedora (Justin M. Forbes)
- redhat/configs:  modify merge.py to match old overrides input (Clark Williams)
- redhat:  fixup pylint complaints (Clark Williams)
- redhat: remove merge.pl and references to it (Clark Williams)
- redhat: update merge.py to handle merge.pl corner cases (Clark Williams)
- Revert "redhat: fix elf got hardening for vm tools" (Don Zickus)
- Update rebase notes for Fedora (Justin M. Forbes)
- Update CONFIG_LOCKDEP_CHAINS_BITS to 19 (cmurf)
- redhat/configs: Turn on CONFIG_SPI_TEGRA210_QUAD for RHEL (Mark Salter)
- ark: aarch64: drop CONFIG_SMC911X (Peter Robinson)
- all: cleanup and de-dupe CDROM_PKTCDVD options. (Peter Robinson)
- all: remove CRYPTO_GF128MUL (Peter Robinson)
- all: cleanup UEFI options (Peter Robinson)
- common: arm64: Enable Ampere Altra SMpro Hardware Monitoring (Peter Robinson)
- fedora: enable STACKPROTECTOR_STRONG (Peter Robinson)
- fedora: enable STACKPROTECTOR on arm platforms (Peter Robinson)
- redhat/self-test: Update data with ENABLE_WERROR (Prarit Bhargava)
- redhat/Makefile.variables: Add ENABLE_WERROR (Prarit Bhargava)
- makefile: Add -Werror support for RHEL (Prarit Bhargava)
- redhat/Makefile.variables: Remove mention of Makefile.rhpkg (Prarit Bhargava)
- redhat/Makefile.variables: Alphabetize variables (Prarit Bhargava)
- gitlab-ci: use CI templates from production branch (Michael Hofmann)
- redhat/kernel.spec.template: Fix internal "File listed twice" errors (Prarit Bhargava)
- redhat: Remove stale .tmp_versions code and comments (Prarit Bhargava)
- redhat/kernel.spec.template: Fix vmlinux_decompressor on !s390x (Prarit Bhargava)
- redhat/kernel.spec.template: Remove unnecessary output from pathfix.py (Prarit Bhargava)
- Modularize CONFIG_ARM_CORESIGHT_PMU_ARCH_SYSTEM_PMU (Mark Salter)
- redhat/kernel.spec.template: Parallelize compression (Prarit Bhargava)
- config: Enable Security Path (Ricardo Robaina)
- redhat/self-test/data: Regenerate self-test data for make change (Prarit Bhargava)
- Update module filters for nvmem_u-boot-env (Justin M. Forbes)
- fedora: Updates for 6.2 merge (Peter Robinson)
- fedora: Updates for 6.1 merge (Peter Robinson)
- modules-core: use %%posttrans (Gerd Hoffmann)
- split sub-rpm kernel-modules-core from kernel-core (Gerd Hoffmann)
- Turn off CONFIG_MTK_T7XX for S390x (Justin M. Forbes)
- CI: add variable for variant handling (Veronika Kabatova)
- Fix up configs with SND_SOC_NAU8315 mismatch (Justin M. Forbes)
- CI: Do a full build for non-bot runs (Veronika Kabatova)
- Fix up configs with SND_SOC_NAU8315 mismatch (Justin M. Forbes)
- kernel/rh_messages.c: gcc12 warning on redundant NULL test (Eric Chanudet) [2142658]
- redhat/configs: Enable CRYPTO_CURVE25519 in ark (Prarit Bhargava)
- general: arm: cleanup ASPEED options (Peter Robinson)
- redhat/configs: ALSA - cleanups for the AMD Pink Sardine DMIC driver (Jaroslav Kysela)
- redhat/docs: Add FAQ entry for booting between Fedora & ELN/RHEL kernels (Prarit Bhargava)
- spec: add missing BuildRequires: python3-docutils for tools (Ondrej Mosnacek)
- config: enable RCU_TRACE for debug kernels (Wander Lairson Costa)
- Add siphash_kunit and strscpy_kunit to mod-internal.list (Justin M. Forbes)
- Add drm_kunit_helpers to mod-internal.list (Justin M. Forbes)
- Fix up configs for Fedora so we don't have a mismatch (Justin M. Forbes)
- Turn on CONFIG_SQUASHFS_DECOMP_SINGLE in pending (Justin M. Forbes)
- redhat/kernel.spec.template: Fix cpupower file error (Prarit Bhargava)
- redhat/configs: aarhc64: clean up some erratum configs (Mark Salter)
- More Fedora configs for 6.1 as deps were switched on (Justin M. Forbes)
- redhat/configs: make SOC_TEGRA_CBB a module (Mark Salter)
- redhat/configs: aarch64: reorganize tegra configs to common dir (Mark Salter)
- Enforces buildroot if cross_arm (Nicolas Chauvet)
- Handle automated case when config generation works correctly (Don Zickus)
- Turn off CONFIG_CRYPTO_ARIA_AESNI_AVX_X86_64 (Justin M. Forbes)
- Turn off CONFIG_EFI_ZBOOT as it makes CKI choke (Justin M. Forbes)
- Fedora config updates for 6.1 (Justin M. Forbes)
- redhat: Remove cpupower files (Prarit Bhargava)
- redhat/configs: update CXL-related options to match what RHEL will use (John W. Linville)
- Clean up the config for the Tegra186 timer (Al Stone)
- redhat/configs: move CONFIG_TEGRA186_GPC_DMA config (Mark Salter)
- Check for kernel config git-push failures (Don Zickus)
- redhat: genlog.sh failures should interrupt the recipe (Patrick Talbert)
- Turn CONFIG_GNSS back on for Fedora (Justin M. Forbes)
- redhat/configs: enable CONFIG_GNSS for RHEL (Michal Schmidt)
- Turn off NVMEM_U_BOOT_ENV for fedora (Justin M. Forbes)
- Consolidate matching fedora and ark entries to common (Justin M. Forbes)
- Empty out redhat/configs/common (Justin M. Forbes)
- Adjust path to compressed vmlinux kernel image for s390x (Justin M. Forbes) [2149273]
- Fedora config updates for 6.1 (Justin M. Forbes)
- redhat: genlog.sh should expect genlog.py in the current directory (Patrick Talbert)
- redhat/configs: consolidate CONFIG_TEST_LIVEPATCH=m (Joe Lawrence)
- redhat/configs: enable CONFIG_TEST_LIVEPATCH=m for s390x (Julia Denham)
- Revert "Merge branch 'ark-make-help' into 'os-build'" (Scott Weaver)
- Remove recommendation to use 'common' for config changes. (Don Zickus)
- Update config to add i3c support for AArch64 (Mark Charlebois)
- redhat: Move cross-compile scripts into their own directory (Prarit Bhargava)
- redhat: Move yaml files into their own directory (Prarit Bhargava)
- redhat: Move update_scripts.sh into redhat/scripts (Prarit Bhargava)
- redhat: Move kernel-tools scripts into their own directory (Prarit Bhargava)
- redhat: Move gen-* scripts into their own directory (Prarit Bhargava)
- redhat: Move mod-* scripts into their own directory (Prarit Bhargava)
- redhat/Makefile: Fix RHJOBS grep warning (Prarit Bhargava)
- redhat: Force remove tmp file (Prarit Bhargava)
- redhat/configs: ALSA - cleanups for the CentOS 9.2 update (Jaroslav Kysela)
- CI: Use CKI container images from quay.io (Veronika Kabatova)
- redhat: clean up the partial-kgcov-snip.config file (Patrick Talbert)
- redhat: avoid picking up stray editor backups when processing configs (Clark Williams)
- CI: Remove old configs (Veronika Kabatova)
- redhat: override `make help` to include dist-help (Jonathan Toppins)
- redhat: make RHTEST stricter (Jonathan Toppins)
- redhat: Enable support for SN2201 system (Ivan Vecera)
- redhat/docs/index.rst: Add FLAVOR information to generate configs for local builds (Enric Balletbo i Serra)
- redhat: fix selftest git command so it picks the right commit (Patrick Talbert)
- redhat/configs: enable HP_WATCHDOG for aarch64 (Mark Salter)
- redhat: disable Kfence Kunit Test (Nico Pache)
- configs: enable CONFIG_LRU_GEN_ENABLED everywhere (Patrick Talbert)
- redhat: Enable WWAN feature and support for Intel, Qualcomm and Mediatek devices (Jose Ignacio Tornos Martinez)
- Turn on dln2 support (RHBZ 2110372) (Justin M. Forbes)
- Enable configs for imx8m PHYs (Al Stone)
- configs/fedora: Build some SC7180 clock controllers as modules (Javier Martinez Canillas)
- redhat/configs: Disable fbdev drivers and use simpledrm everywhere (Javier Martinez Canillas) [1986223]
- redhat: fix the branch we pull from the documentation tree (Herton R. Krzesinski)
- redhat/configs: change so watchdog is module versus builtin (Steve Best)
- redhat/configs: move CONFIG_ACPI_VIDEO to common/generic (Mark Langsdorf)
- enable imx8xm I2C configs properly (Al Stone)
- configs/fedora: Enable a few more drivers needed by the HP X2 Chromebook (Javier Martinez Canillas)
- enable the rtc-rv8803 driver on RHEL and Fedora (David Arcari)
- redhat/Makefile: Remove BUILD_SCRATCH_TARGET (Prarit Bhargava)
- configs: move CONFIG_INTEL_TDX_GUEST to common directory (Wander Lairson Costa)
- redhat/Makefile: Use new BUILD_TARGET for RHEL dist[g]-brew target (Prarit Bhargava)
- redhat: method.py: change the output loop to use 'values' method (Patrick Talbert)
- redhat: use 'update' method in merge.py (Patrick Talbert)
- redhat: Use a context manager in merge.py for opening the config file for reading (Patrick Talbert)
- redhat: automatically strip newlines in merge.py (Clark Williams)
- redhat: python replacement for merge.pl (Clark Williams)
- redhat/docs: Update with DISTLOCALVERSION (Prarit Bhargava)
- redhat/Makefile: Rename LOCALVERSION to DISTLOCALVERSION (Akihiko Odaki)
- Adjust FIPS module name in RHEL (Vladis Dronov)
- spec: prevent git apply from searching for the .git directory (Ondrej Mosnacek)
- redhat: Remove parallel_xz.sh (Prarit Bhargava)
- Turn on Multi-Gen LRU for Fedora (Justin M. Forbes)
- Add kasan_test to mod-internal.list (Justin M. Forbes)
- redhat/Makefile.variables: Fix typo with RHDISTGIT_TMP (Prarit Bhargava)
- spec: fix path to `installing_core` stamp file for subpackages (Jonathan Lebon)
- Remove unused ci scripts (Don Zickus)
- Rename rename FORCE_MAX_ZONEORDER to ARCH_FORCE_MAX_ORDER in configs (Justin M. Forbes)
- redhat: Add new fortify_kunit & is_signed_type_kunit to mod-internal.list (Patrick Talbert)
- Rename rename FORCE_MAX_ZONEORDER to ARCH_FORCE_MAX_ORDER in pending (Justin M. Forbes)
- Add acpi video to the filter_modules.sh for rhel (Justin M. Forbes)
- Change acpi_bus_get_acpi_device to acpi_get_acpi_dev (Justin M. Forbes)
- Turn on ACPI_VIDEO for arm (Justin M. Forbes)
- Turn on CONFIG_PRIME_NUMBERS as a module (Justin M. Forbes)
- Add new drm kunit tests to mod-internal.list (Justin M. Forbes)
- redhat: fix elf got hardening for vm tools (Frantisek Hrbata)
- kernel.spec.template: remove some temporary files early (Ondrej Mosnacek)
- kernel.spec.template: avoid keeping two copies of vmlinux (Ondrej Mosnacek)
- Add fortify_kunit to mod-internal.list (Justin M. Forbes)
- Add module filters for Fedora as acpi video has new deps (Justin M. Forbes)
- One more mismatch (Justin M. Forbes)
- Fix up pending for mismatches (Justin M. Forbes)
- Forgot too remove this from pending, it is set properly in ark (Justin M. Forbes)
- redhat/Makefile: Add DIST to git tags for RHEL (Prarit Bhargava)
- redhat/configs: Move CONFIG_ARM_SMMU_QCOM_DEBUG to common (Jerry Snitselaar)
- Common config cleanup for 6.0 (Justin M. Forbes)
- Allow selftests to fail without killing the build (Justin M. Forbes)
- redhat: Remove redhat/Makefile.rhpkg (Prarit Bhargava)
- redhat/Makefile: Move RHDISTGIT_CACHE and RHDISTGIT_TMP (Prarit Bhargava)
- redhat/Makefile.rhpkg: Remove RHDISTGIT_USER (Prarit Bhargava)
- redhat/Makefile: Move RHPKG_BIN to redhat/Makefile (Prarit Bhargava)
- common: clean up Android option with removal of CONFIG_ANDROID (Peter Robinson)
- redhat/configs: Remove x86_64 from priority files (Prarit Bhargava)
- redhat/configs/pending-ark: Remove x86_64 directory (Prarit Bhargava)
- redhat/configs/pending-fedora: Remove x86_64 directory (Prarit Bhargava)
- redhat/configs/fedora: Remove x86_64 directory (Prarit Bhargava)
- redhat/configs/common: Remove x86_64 directory (Prarit Bhargava)
- redhat/configs/ark: Remove x86_64 directory (Prarit Bhargava)
- redhat/configs/custom-overrides: Remove x86_64 directory (Prarit Bhargava)
- configs: use common CONFIG_ARM64_SME for ark and fedora (Mark Salter)
- redhat/configs: Add a warning message to priority.common (Prarit Bhargava)
- redhat/configs: Enable INIT_STACK_ALL_ZERO for Fedora (Miko Larsson)
- redhat: Set CONFIG_MAXLINEAR_GPHY to =m (Petr Oros)
- redhat/configs enable CONFIG_INTEL_IFS (David Arcari)
- redhat: Remove filter-i686.sh.rhel (Prarit Bhargava)
- redhat/Makefile: Set PATCHLIST_URL to none for RHEL/cs9 (Prarit Bhargava)
- redhat: remove GL_DISTGIT_USER, RHDISTGIT and unify dist-git cloning (Prarit Bhargava)
- redhat/Makefile.variables: Add ADD_COMMITID_TO_VERSION (Prarit Bhargava)
- kernel.spec: disable vmlinux.h generation for s390 zfcpdump config (Prarit Bhargava)
- perf: Require libbpf 0.6.0 or newer (Prarit Bhargava)
- kabi: add stablelist helpers (Prarit Bhargava)
- Makefile: add kabi targets (Prarit Bhargava)
- kabi: add support for symbol namespaces into check-kabi (Prarit Bhargava)
- kabi: ignore new stablelist metadata in show-kabi (Prarit Bhargava)
- redhat/Makefile: add dist-assert-tree-clean target (Prarit Bhargava)
- redhat/kernel.spec.template: Specify vmlinux.h path when building samples/bpf (Prarit Bhargava) [2041365]
- spec: Fix separate tools build (Prarit Bhargava) [2054579]
- redhat/scripts: Update merge-subtrees.sh with new subtree location (Prarit Bhargava)
- redhat/kernel.spec.template: enable dependencies generation (Prarit Bhargava)
- redhat: build and include memfd to kernel-selftests-internal (Prarit Bhargava) [2027506]
- redhat/kernel.spec.template: Link perf with --export-dynamic (Prarit Bhargava)
- redhat: kernel.spec: selftests: abort on build failure (Prarit Bhargava)
- redhat: configs: move CONFIG_SERIAL_MULTI_INSTANTIATE=m settings to common/x86 (Jaroslav Kysela)
- configs: enable CONFIG_HP_ILO for aarch64 (Mark Salter)
- all: cleanup dell config options (Peter Robinson)
- redhat: Include more kunit tests (Nico Pache)
- common: some minor cleanups/de-dupe (Peter Robinson)
- common: enable INTEGRITY_MACHINE_KEYRING on all configuraitons (Peter Robinson)
- Fedora 6.0 configs update (Justin M. Forbes)
- redhat/self-test: Ignore .rhpkg.mk files (Prarit Bhargava)
- redhat/configs: Enable CONFIG_PRINTK_INDEX on Fedora (Prarit Bhargava)
- redhat/configs: Cleanup CONFIG_X86_KERNEL_IBT (Prarit Bhargava)
- Fix up SND_CTL debug options (Justin M. Forbes)
- redhat: create /boot symvers link if it doesn't exist (Jan Stancek)
- redhat: remove duplicate kunit tests in mod-internal.list (Nico Pache)
- configs/fedora: Make Fedora work with HNS3 network adapter (Zamir SUN)
- redhat/configs/fedora/generic: Enable CONFIG_BLK_DEV_UBLK on Fedora (Richard W.M. Jones) [2122595]
- fedora: disable IWLMEI (Peter Robinson)
- redhat/configs: enable UINPUT on aarch64 (Benjamin Tissoires)
- Fedora 6.0 configs part 1 (Justin M. Forbes)
- redhat/Makefile: Always set UPSTREAM (Prarit Bhargava)
- redhat/configs: aarch64: Turn on Apple Silicon configs for Fedora (Eric Curtin)
- Add cpumask_kunit to mod-internal.list (Justin M. Forbes)
- config - consolidate disabled MARCH options on s390x (Dan Horák)
- move the baseline arch to z13 for s390x in F-37+ (Dan Horák)
- redhat/scripts/rh-dist-git.sh: Fix outdated cvs reference (Prarit Bhargava)
- redhat/scripts/expand_srpm.sh: Use Makefile variables (Prarit Bhargava)
- redhat/scripts/clone_tree.sh: Use Makefile variables (Prarit Bhargava)
- Fedora: arm changes for 6.0, part 1, with some ACPI (Peter Robinson)
- redhat/self-test: Fix shellcheck errors (Prarit Bhargava)
- redhat/docs: Add dist-brew BUILD_FLAGS information (Prarit Bhargava)
- redhat: change the changelog item for upstream merges (Herton R. Krzesinski)
- redhat: fix dist-release build number test (Herton R. Krzesinski)
- redhat: fix release number bump when dist-release-changed runs (Herton R. Krzesinski)
- redhat: use new genlog.sh script to detect changes for dist-release (Herton R. Krzesinski)
- redhat: move changelog addition to the spec file back into genspec.sh (Herton R. Krzesinski)
- redhat: always add a rebase entry when ark merges from upstream (Herton R. Krzesinski)
- redhat: drop merge ark patches hack (Herton R. Krzesinski)
- redhat: don't hardcode temporary changelog file (Herton R. Krzesinski)
- redhat: split changelog generation from genspec.sh (Herton R. Krzesinski)
- redhat: configs: Disable FIE on arm (Jeremy Linton) [2012226]
- redhat/Makefile: Clean linux tarballs (Prarit Bhargava)
- redhat/configs: Cleanup CONFIG_ACPI_AGDI (Prarit Bhargava)
- spec: add cpupower daemon reload on install/upgrade (Jarod Wilson)
- redhat: properly handle binary files in patches (Ondrej Mosnacek)
- Add python3-setuptools buildreq for perf (Justin M. Forbes)
- Add cros_kunit to mod-internal.list (Justin M. Forbes)
- Add new tests to mod-internal.list (Justin M. Forbes)
- Turn off some Kunit tests in pending (Justin M. Forbes)
- Clean up a mismatch in Fedora configs (Justin M. Forbes)
- redhat/configs: Sync up Retbleed configs with centos-stream (Waiman Long)
- Change CRYPTO_BLAKE2S_X86 from m to y (Justin M. Forbes)
- Leave CONFIG_ACPI_VIDEO on for x86 only (Justin M. Forbes)
- Fix BLAKE2S_ARM and BLAKE2S_X86 configs in pending (Justin M. Forbes)
- Fix pending for ACPI_VIDEO (Justin M. Forbes)
- redhat/configs: Fix rm warning on config warnings (Eric Chanudet)
- redhat/Makefile: Deprecate PREBUILD_GIT_ONLY variable (Prarit Bhargava)
- redhat/Makefile: Deprecate SINGLE_TARBALL variable (Prarit Bhargava)
- redhat/Makefile: Deprecate GIT variable (Prarit Bhargava)
- Update CONFIG_LOCKDEP_CHAINS_BITS to 18 (cmurf)
- Add new FIPS module name and version configs (Vladis Dronov)
- redhat/configs/fedora: Make PowerPC's nx-gzip buildin (Jakub Čajka)
- omit unused Provides (Dan Horák)
- self-test: Add test for DIST=".eln" (Prarit Bhargava)
- redhat: Enable CONFIG_LZ4_COMPRESS on Fedora (Prarit Bhargava)
- fedora: armv7: enable MMC_STM32_SDMMC (Peter Robinson)
- .gitlab-ci.yaml: Add test for dist-get-buildreqs target (Prarit Bhargava)
- redhat/docs: Add information on build dependencies (Prarit Bhargava)
- redhat/Makefile: Add better pass message for dist-get-buildreqs (Prarit Bhargava)
- redhat/Makefile: Provide a better message for system-sb-certs (Prarit Bhargava)
- redhat/Makefile: Change dist-buildreq-check to a non-blocking target (Prarit Bhargava)
- create-data: Parallelize spec file data (Prarit Bhargava)
- create-data.sh: Store SOURCES Makefile variable (Prarit Bhargava)
- redhat/Makefile: Split up setup-source target (Prarit Bhargava)
- create-data.sh: Redefine varfilename (Prarit Bhargava)
- create-data.sh: Parallelize variable file creation (Prarit Bhargava)
- redhat/configs: Enable CONFIG_LZ4_COMPRESS (Prarit Bhargava)
- redhat/docs: Update brew information (Prarit Bhargava)
- redhat/Makefile: Fix eln BUILD_TARGET (Prarit Bhargava)
- redhat/Makefile: Set BUILD_TARGET for dist-brew (Prarit Bhargava)
- kernel.spec.template: update (s390x) expoline.o path (Joe Lawrence)
- fedora: enable BCM_NET_PHYPTP (Peter Robinson)
- Fedora 5.19 configs update part 2 (Justin M. Forbes)
- redhat/Makefile: Change fedora BUILD_TARGET (Prarit Bhargava)
- New configs in security/keys (Fedora Kernel Team)
- Fedora: arm: enable a pair of drivers (Peter Robinson)
- redhat: make kernel-zfcpdump-core to not provide kernel-core/kernel (Herton R. Krzesinski)
- redhat/configs: Enable QAT devices for arches other than x86 (Vladis Dronov)
- Fedora 5.19 configs pt 1 (Justin M. Forbes)
- redhat: Exclude cpufreq.h from kernel-headers (Patrick Talbert)
- Add rtla subpackage for kernel-tools (Justin M. Forbes)
- fedora: arm: enable a couple of QCom drivers (Peter Robinson)
- redhat/Makefile: Deprecate BUILD_SCRATCH_TARGET (Prarit Bhargava)
- redhat: enable CONFIG_DEVTMPFS_SAFE (Mark Langsdorf)
- redhat/Makefile: Remove deprecated variables and targets (Prarit Bhargava)
- Split partner modules into a sub-package (Alice Mitchell)
- Enable kAFS and it's dependancies in RHEL (Alice Mitchell)
- Enable Marvell OcteonTX2 crypto device in ARK (Vladis Dronov)
- redhat/Makefile: Remove --scratch from BUILD_TARGET (Prarit Bhargava)
- redhat/Makefile: Fix dist-brew and distg-brew targets (Prarit Bhargava)
- fedora: arm64: Initial support for TI Keystone 3 (ARCH_K3) (Peter Robinson)
- fedora: arm: enable Hardware Timestamping Engine support (Peter Robinson)
- fedora: wireless: disable SiLabs and PureLiFi (Peter Robinson)
- fedora: updates for 5.19 (Peter Robinson)
- fedora: minor updates for Fedora configs (Peter Robinson)
- configs/fedora: Enable the pinctrl SC7180 driver built-in (Enric Balletbo i Serra)
- redhat/configs: enable CONFIG_DEBUG_NET for debug kernel (Hangbin Liu)
- redhat/Makefile: Add SPECKABIVERSION variable (Prarit Bhargava)
- redhat/self-test: Provide better failure output (Prarit Bhargava)
- redhat/self-test: Reformat tests to kernel standard (Prarit Bhargava)
- redhat/self-test: Add purpose and header to each test (Prarit Bhargava)
- Drop outdated CRYPTO_ECDH configs (Vladis Dronov)
- Brush up crypto SHA512 and USER configs (Vladis Dronov)
- Brush up crypto ECDH and ECDSA configs (Vladis Dronov)
- redhat/self-test: Update data set (Prarit Bhargava)
- create-data.sh: Reduce specfile data output (Prarit Bhargava)
- redhat/configs: restore/fix core INTEL_LPSS configs to be builtin again (Hans de Goede)
- Enable CKI on os-build MRs only (Don Zickus)
- self-test: Fixup Makefile contents test (Prarit Bhargava)
- redhat/self-test: self-test data update (Prarit Bhargava)
- redhat/self-test: Fix up create-data.sh to not report local variables (Prarit Bhargava)
- redhat/configs/fedora: Enable a set of modules used on some x86 tablets (Hans de Goede)
- redhat/configs: Make INTEL_SOC_PMIC_CHTDC_TI builtin (Hans de Goede)
- redhat/configs/fedora: enable missing modules modules for Intel IPU3 camera support (Hans de Goede)
- Common: minor cleanups (Peter Robinson)
- fedora: some minor Fedora cleanups (Peter Robinson)
- fedora: drop X86_PLATFORM_DRIVERS_DELL dupe (Peter Robinson)
- redhat: change tools_make macro to avoid full override of variables in Makefile (Herton R. Krzesinski)
- Fix typo in Makefile for Fedora Stable Versioning (Justin M. Forbes)
- Remove duplicates from ark/generic/s390x/zfcpdump/ (Vladis Dronov)
- Move common/debug/s390x/zfcpdump/ configs to ark/debug/s390x/zfcpdump/ (Vladis Dronov)
- Move common/generic/s390x/zfcpdump/ configs to ark/generic/s390x/zfcpdump/ (Vladis Dronov)
- Drop RCU_EXP_CPU_STALL_TIMEOUT to 0, we are not really android (Justin M. Forbes)
- redhat/configs/README: Update the README (Prarit Bhargava)
- redhat/docs: fix hyperlink typo (Patrick Talbert)
- all: net: remove old NIC/ATM drivers that use virt_to_bus() (Peter Robinson)
- Explicitly turn off CONFIG_KASAN_INLINE for ppc (Justin M. Forbes)
- redhat/docs: Add a description of kernel naming (Prarit Bhargava)
- Change CRYPTO_CHACHA_S390 from m to y (Justin M. Forbes)
- enable CONFIG_NET_ACT_CTINFO in ark (Davide Caratti)
- redhat/configs: enable CONFIG_SP5100_TCO (David Arcari)
- redhat/configs: Set CONFIG_VIRTIO_IOMMU on x86_64 (Eric Auger) [2089765]
- Turn off KASAN_INLINE for RHEL ppc in pending (Justin M. Forbes)
- redhat/kernel.spec.template: update selftest data via "make dist-self-test-data" (Denys Vlasenko)
- redhat/kernel.spec.template: remove stray *.hardlink-temporary files, if any (Denys Vlasenko)
- Fix up ZSMALLOC config for s390 (Justin M. Forbes)
- Turn on KASAN_OUTLINE for ppc debug (Justin M. Forbes)
- Turn on KASAN_OUTLINE for PPC debug to avoid mismatch (Justin M. Forbes)
- Fix up crypto config mistmatches (Justin M. Forbes)
- Fix up config mismatches (Justin M. Forbes)
- generic/fedora: cleanup and disable Lightning Moutain SoC (Peter Robinson)
- redhat: Set SND_SOC_SOF_HDA_PROBES to =m (Patrick Talbert)
- Fix versioning on stable Fedora (Justin M. Forbes)
- Enable PAGE_POOL_STATS for arm only (Justin M. Forbes)
- Revert "Merge branch 'fix-ci-20220523' into 'os-build'" (Patrick Talbert)
- Flip CONFIG_RADIO_ADAPTERS to module for Fedora (Justin M. Forbes)
- redhat/Makefile: Drop quotation marks around string definitions (Prarit Bhargava)
- Fedora: arm: Updates for QCom devices (Peter Robinson)
- Fedora arm and generic updates for 5.17 (Peter Robinson)
- enable COMMON_CLK_SI5341 for Xilinx ZYNQ-MP (Peter Robinson)
- Turn on CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG_SECONDARY_KEYRING for Fedora (Justin M. Forbes)
- redhat/self-test/data: Update data set (Prarit Bhargava)
- Revert variable switch for lasttag (Justin M. Forbes)
- redhat: Add self-tests to .gitlab-ci.yml (Prarit Bhargava)
- redhat/self-test: Update data (Prarit Bhargava)
- redhat/self-test: Unset Makefile variables (Prarit Bhargava)
- redhat/self-test: Omit SHELL variable from test data (Prarit Bhargava)
- Add CONFIG_EFI_DXE_MEM_ATTRIBUTES (Justin M. Forbes)
- Update filter-modules for mlx5-vfio-pci (Justin M. Forbes)
- Fedora configs for 5.18 (Justin M. Forbes)
- self-test/data/create-data.sh: Avoid SINGLE_TARBALL warning (Prarit Bhargava)
- redhat/Makefile: Rename PREBUILD to UPSTREAMBUILD (Prarit Bhargava)
- redhat/Makefile: Rename BUILDID to LOCALVERSION (Prarit Bhargava)
- redhat/Makefile: Fix dist-brew & distg-brew targets (Prarit Bhargava)
- redhat/Makefile: Reorganize MARKER code (Prarit Bhargava)
- redhat/scripts/new_release.sh: Use Makefile variables (Prarit Bhargava)
- redhat/Makefile: Rename __YSTREAM and __ZSTREAM (Prarit Bhargava)
- redhat/genspec.sh: Add comment about SPECBUILDID variable (Prarit Bhargava)
- redhat/kernel.spec.template: Move genspec variables into one section (Prarit Bhargava)
- redhat/kernel.spec.template: Remove kversion (Prarit Bhargava)
- redhat/Makefile: Add SPECTARFILE_RELEASE comment (Prarit Bhargava)
- redhat/Makefile: Rename RPMVERSION to BASEVERSION (Prarit Bhargava)
- redhat/Makefile: Target whitespace cleanup (Prarit Bhargava)
- redhat/Makefile: Move SPECRELEASE to genspec.sh (Prarit Bhargava)
- redhat/Makefile: Add kernel-NVR comment (Prarit Bhargava)
- redhat/Makefile: Use SPECFILE variable (Prarit Bhargava)
- redhat/Makefile: Remove KEXTRAVERSION (Prarit Bhargava)
- redhat: Enable VM kselftests (Nico Pache) [1978539]
- redhat: enable CONFIG_TEST_VMALLOC for vm selftests (Nico Pache)
- redhat: Enable HMM test to be used by the kselftest test suite (Nico Pache)
- redhat/Makefile.variables: Change git hash length to default (Prarit Bhargava)
- redhat/Makefile: Drop quotation marks around string definitions (Prarit Bhargava)
- Turn on INTEGRITY_MACHINE_KEYRING for Fedora (Justin M. Forbes)
- redhat/configs: fix CONFIG_INTEL_ISHTP_ECLITE (David Arcari)
- redhat/configs: Fix rm warning on error (Prarit Bhargava)
- Fix nightly merge CI (Don Zickus)
- redhat/kernel.spec.template: fix standalone tools build (Jan Stancek)
- Add system-sb-certs for RHEL-9 (Don Zickus)
- Fix dist-buildcheck-reqs (Don Zickus)
- move DAMON configs to correct directory (Chris von Recklinghausen)
- redhat: indicate HEAD state in tarball/rpm name (Jarod Wilson)
- Fedora 5.18 config set part 1 (Justin M. Forbes)
- fedora: arm: Enable new Rockchip 356x series drivers (Peter Robinson)
- fedora: arm: enable DRM_I2C_NXP_TDA998X on aarch64 (Peter Robinson)
- redhat/self-test: Add test to verify Makefile declarations. (Prarit Bhargava)
- redhat/Makefile: Add RHTEST (Prarit Bhargava)
- redhat: shellcheck cleanup (Prarit Bhargava)
- redhat/self-test/data: Cleanup data (Prarit Bhargava)
- redhat/self-test: Add test to verify SPEC variables (Prarit Bhargava)
- redhat/Makefile: Add 'duplicate' SPEC entries for user set variables (Prarit Bhargava)
- redhat/Makefile: Rename TARFILE_RELEASE to SPECTARFILE_RELEASE (Prarit Bhargava)
- redhat/genspec: Rename PATCHLIST_CHANGELOG to SPECPATCHLIST_CHANGELOG (Prarit Bhargava)
- redhat/genspec: Rename DEBUG_BUILDS_ENABLED to SPECDEBUG_BUILDS_ENABLED (Prarit Bhargava)
- redhat/Makefile: Rename PKGRELEASE to SPECBUILD (Prarit Bhargava)
- redhat/genspec: Rename BUILDID_DEFINE to SPECBUILDID (Prarit Bhargava)
- redhat/Makefile: Rename CHANGELOG to SPECCHANGELOG (Prarit Bhargava)
- redhat/Makefile: Rename RPMKEXTRAVERSION to SPECKEXTRAVERSION (Prarit Bhargava)
- redhat/Makefile: Rename RPMKSUBLEVEL to SPECKSUBLEVEL (Prarit Bhargava)
- redhat/Makefile: Rename RPMKPATCHLEVEL to SPECKPATCHLEVEL (Prarit Bhargava)
- redhat/Makefile: Rename RPMKVERSION to SPECKVERSION (Prarit Bhargava)
- redhat/Makefile: Rename KVERSION to SPECVERSION (Prarit Bhargava)
- redhat/Makefile: Deprecate some simple targets (Prarit Bhargava)
- redhat/Makefile: Use KVERSION (Prarit Bhargava)
- redhat/configs: Set GUP_TEST in debug kernel (Joel Savitz)
- enable DAMON configs (Chris von Recklinghausen) [2004233]
- redhat: add zstream switch for zstream release numbering (Herton R. Krzesinski)
- redhat: change kabi tarballs to use the package release (Herton R. Krzesinski)
- redhat: generate distgit changelog in genspec.sh as well (Herton R. Krzesinski)
- redhat: make genspec prefer metadata from git notes (Herton R. Krzesinski)
- redhat: use tags from git notes for zstream to generate changelog (Herton R. Krzesinski)
- ARK: Remove code marking devices unmaintained (Peter Georg)
- rh_message: Fix function name (Peter Georg) [2019377]
- Turn on CONFIG_RANDOM_TRUST_BOOTLOADER (Justin M. Forbes)
- redhat/configs: aarch64: enable CPU_FREQ_GOV_SCHEDUTIL (Mark Salter)
- Move CONFIG_HW_RANDOM_CN10K to a proper place (Vladis Dronov)
- redhat/self-test: Clean up data set (Prarit Bhargava)
- redhat/Makefile.rhpkg: Remove quotes for RHDISTGIT (Prarit Bhargava)
- redhat/scripts/create-tarball.sh: Use Makefile variables (Prarit Bhargava)
- redhat/Makefile: Deprecate SINGLE_TARBALL (Prarit Bhargava)
- redhat/Makefile: Move SINGLE_TARBALL to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Use RPMVERSION (Prarit Bhargava)
- redhat/scripts/rh-dist-git.sh: Use Makefile variables (Prarit Bhargava)
- redhat/configs/build_configs.sh: Use Makefile variables (Prarit Bhargava)
- redhat/configs/process_configs.sh: Use Makefile variables (Prarit Bhargava)
- redhat/kernel.spec.template: Use RPM_BUILD_NCPUS (Prarit Bhargava)
- redhat/configs/generate_all_configs.sh: Use Makefile variables (Prarit Bhargava)
- redhat/configs: enable nf_tables SYNPROXY extension on ark (Davide Caratti)
- fedora: Disable fbdev drivers missed before (Javier Martinez Canillas)
- Redhat: enable Kfence on production servers (Nico Pache)
- redhat: ignore known empty patches on the patches rpminspect test (Herton R. Krzesinski)
- kernel-ark: arch_hw Update CONFIG_MOUSE_VSXXXAA=m (Tony Camuso) [2062909]
- spec: keep .BTF section in modules for s390 (Yauheni Kaliuta) [2071969]
- kernel.spec.template: Ship arch/s390/lib/expoline.o in kernel-devel (Ondrej Mosnacek)
- redhat: disable tv/radio media device infrastructure (Jarod Wilson)
- redhat/configs: clean up INTEL_LPSS configuration (David Arcari)
- Have to rename the actual contents too (Justin M. Forbes)
- The CONFIG_SATA_MOBILE_LPM_POLICY rebane was reverted (Justin M. Forbes)
- redhat: Enable KASAN on all ELN debug kernels (Nico Pache)
- redhat: configs: Enable INTEL_IOMMU_DEBUGFS for debug builds (Jerry Snitselaar)
- generic: can: disable CAN_SOFTING everywhere (Peter Robinson)
- redhat/configs: Enable CONFIG_DM_ERA=m for all (Yanko Kaneti)
- redhat/configs: enable CONFIG_SAMPLE_VFIO_MDEV_MTTY (Patrick Talbert)
- Build intel_sdsi with %%{tools_make} (Justin M. Forbes)
- configs: remove redundant Fedora config for INTEL_IDXD_COMPAT (Jerry Snitselaar)
- redhat/configs: enable CONFIG_RANDOMIZE_KSTACK_OFFSET_DEFAULT (Joel Savitz) [2026319]
- configs: enable CONFIG_RMI4_F3A (Benjamin Tissoires)
- redhat: configs: Disable TPM 1.2 specific drivers (Jerry Snitselaar)
- redhat/configs: Enable cr50 I2C TPM interface (Akihiko Odaki)
- spec: make HMAC file encode relative path (Jonathan Lebon)
- redhat/kernel.spec.template: Add intel_sdsi utility (Prarit Bhargava)
- Spec fixes for intel-speed-select (Justin M. Forbes)
- Add Partner Supported taint flag to kAFS (Alice Mitchell) [2038999]
- Add Partner Supported taint flag (Alice Mitchell) [2038999]
- Enabled INTEGRITY_MACHINE_KEYRING for all configs. (Peter Robinson)
- redhat/configs: Enable CONFIG_RCU_SCALE_TEST & CONFIG_RCU_REF_SCALE_TEST (Waiman Long)
- Add clk_test and clk-gate_test to mod-internal.list (Justin M. Forbes)
- redhat/self-tests: Ignore UPSTREAM (Prarit Bhargava)
- redhat/self-tests: Ignore RHGITURL (Prarit Bhargava)
- redhat/Makefile.variables: Extend git hash length to 15 (Prarit Bhargava)
- redhat/self-test: Remove changelog from spec files (Prarit Bhargava)
- redhat/genspec.sh: Rearrange genspec.sh (Prarit Bhargava)
- redhat/self-test: Add spec file data (Prarit Bhargava)
- redhat/self-test: Add better dist-dump-variables test (Prarit Bhargava)
- redhat/self-test: Add variable test data (Prarit Bhargava)
- redhat/config: Remove obsolete CONFIG_MFD_INTEL_PMT (David Arcari)
- redhat/configs: enable CONFIG_INTEL_ISHTP_ECLITE (David Arcari)
- Avoid creating files in $RPM_SOURCE_DIR (Nicolas Chauvet)
- Flip CRC64 from off to y (Justin M. Forbes)
- New configs in lib/Kconfig (Fedora Kernel Team)
- disable redundant assignment of CONFIG_BQL on ARK (Davide Caratti)
- redhat/configs: remove unnecessary GPIO options for aarch64 (Brian Masney)
- redhat/configs: remove viperboard related Kconfig options (Brian Masney)
- redhat/configs/process_configs.sh: Avoid race with find (Prarit Bhargava)
- redhat/configs/process_configs.sh: Remove CONTINUEONERROR (Prarit Bhargava)
- Remove i686 configs and filters (Justin M. Forbes)
- redhat/configs: Set CONFIG_X86_AMD_PSTATE built-in on Fedora (Prarit Bhargava)
- Fix up mismatch with CRC64 (Justin M. Forbes)
- Fedora config updates to fix process_configs (Justin M. Forbes)
- redhat: Fix release tagging (Prarit Bhargava)
- redhat/self-test: Fix version tag test (Prarit Bhargava)
- redhat/self-test: Fix BUILD verification test (Prarit Bhargava)
- redhat/self-test: Cleanup SRPM related self-tests (Prarit Bhargava)
- redhat/self-test: Fix shellcheck test (Prarit Bhargava)
- redhat/configs: Disable watchdog components (Prarit Bhargava)
- redhat/README.Makefile: Add a Makefile README file (Prarit Bhargava)
- redhat/Makefile: Remove duplicated code (Prarit Bhargava)
- Add BuildRequires libnl3-devel for intel-speed-select (Justin M. Forbes)
- Add new kunit tests for 5.18 to mod-internal.list (Justin M. Forbes)
- Fix RHDISTGIT for Fedora (Justin M. Forbes)
- redhat/configs/process_configs.sh: Fix race with tools generation (Prarit Bhargava)
- New configs in drivers/dax (Fedora Kernel Team)
- Fix up CONFIG_SND_AMD_ACP_CONFIG files (Patrick Talbert)
- Remove CONFIG_SND_SOC_SOF_DEBUG_PROBES files (Patrick Talbert)
- SATA_MOBILE_LPM_POLICY is now SATA_LPM_POLICY (Justin M. Forbes)
- Define SNAPSHOT correctly when VERSION_ON_UPSTREAM is 0 (Justin M. Forbes)
- redhat/Makefile: Fix dist-git (Prarit Bhargava)
- Change the pending-ark CONFIG_DAX to y due to mismatch (Justin M. Forbes)
- Enable net reference count trackers in all debug kernels (Jiri Benc)
- redhat/Makefile: Reorganize variables (Prarit Bhargava)
- redhat/Makefile: Add some descriptions (Prarit Bhargava)
- redhat/Makefile: Move SNAPSHOT check (Prarit Bhargava)
- redhat/Makefile: Deprecate BREW_FLAGS, KOJI_FLAGS, and TEST_FLAGS (Prarit Bhargava)
- redhat/genspec.sh: Rework RPMVERSION variable (Prarit Bhargava)
- redhat/Makefile: Remove dead comment (Prarit Bhargava)
- redhat/Makefile: Cleanup KABI* variables. (Prarit Bhargava)
- redhat/Makefile.variables: Default RHGITCOMMIT to HEAD (Prarit Bhargava)
- redhat/scripts/create-tarball.sh: Use Makefile TARBALL variable (Prarit Bhargava)
- redhat/Makefile: Remove extra DIST_BRANCH (Prarit Bhargava)
- redhat/Makefile: Remove STAMP_VERSION (Prarit Bhargava)
- redhat/Makefile: Move NO_CONFIGCHECKS to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Move RHJOBS to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Move RHGIT* variables to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Move PREBUILD_GIT_ONLY to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Move BUILD to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Move BUILD_FLAGS to Makefile.variables. (Prarit Bhargava)
- redhat/Makefile: Move BUILD_PROFILE to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Move BUILD_TARGET and BUILD_SCRATCH_TARGET to Makefile.variables (Prarit Bhargava)
- redhat/Makefile: Remove RHPRODUCT variable (Prarit Bhargava)
- redhat/Makefile: Cleanup DISTRO variable (Prarit Bhargava)
- redhat/Makefile: Move HEAD to Makefile.variables. (Prarit Bhargava)
- redhat: Combine Makefile and Makefile.common (Prarit Bhargava)
- redhat/koji/Makefile: Decouple koji Makefile from Makefile.common (Prarit Bhargava)
- Set CONFIG_SND_SOC_SOF_MT8195 for Fedora and turn on VDPA_SIM_BLOCK (Justin M. Forbes)
- Add asus_wmi_sensors modules to filters for Fedora (Justin M. Forbes)
- redhat: spec: trigger dracut when modules are installed separately (Jan Stancek)
- Last of the Fedora 5.17 configs initial pass (Justin M. Forbes)
- redhat/Makefile: Silence dist-clean-configs output (Prarit Bhargava)
- Fedora 5.17 config updates (Justin M. Forbes)
- Setting CONFIG_I2C_SMBUS to "m" for ark (Gopal Tiwari)
- Print arch with process_configs errors (Justin M. Forbes)
- Pass RHJOBS to process_configs for dist-configs-check as well (Justin M. Forbes)
- redhat/configs/process_configs.sh: Fix issue with old error files (Prarit Bhargava)
- redhat/configs/build_configs.sh: Parallelize execution (Prarit Bhargava)
- redhat/configs/build_configs.sh: Provide better messages (Prarit Bhargava)
- redhat/configs/build_configs.sh: Create unique output files (Prarit Bhargava)
- redhat/configs/build_configs.sh: Add local variables (Prarit Bhargava)
- redhat/configs/process_configs.sh: Parallelize execution (Prarit Bhargava)
- redhat/configs/process_configs.sh: Provide better messages (Prarit Bhargava)
- redhat/configs/process_configs.sh: Create unique output files (Prarit Bhargava)
- redhat/configs/process_configs.sh: Add processing config function (Prarit Bhargava)
- redhat: Unify genspec.sh and kernel.spec variable names (Prarit Bhargava)
- redhat/genspec.sh: Remove options and use Makefile variables (Prarit Bhargava)
- Add rebase note for 5.17 on Fedora stable (Justin M. Forbes)
- More Fedora config updates for 5.17 (Justin M. Forbes)
- redhat/configs: Disable CONFIG_MACINTOSH_DRIVERS in RHEL. (Prarit Bhargava)
- redhat: Fix "make dist-release-finish" to use the correct NVR variables (Neal Gompa) [2053836]
- Build CROS_EC Modules (Jason Montleon)
- redhat: configs: change aarch64 default dma domain to lazy (Jerry Snitselaar)
- redhat: configs: disable ATM protocols (Davide Caratti)
- configs/fedora: Enable the interconnect SC7180 driver built-in (Enric Balletbo i Serra)
- configs: clean up CONFIG_PAGE_TABLE_ISOLATION files (Ondrej Mosnacek)
- redhat: configs: enable CONFIG_INTEL_PCH_THERMAL for RHEL x86 (David Arcari)
- redhat/Makefile: Fix dist-dump-variables target (Prarit Bhargava)
- redhat/configs: Enable DEV_DAX and DEV_DAX_PMEM modules on aarch64 for fedora (D Scott Phillips)
- redhat/configs: Enable CONFIG_TRANSPARENT_HUGEPAGE on aarch64 for fedora (D Scott Phillips)
- configs/process_configs.sh: Remove orig files (Prarit Bhargava)
- redhat: configs: Disable CONFIG_MPLS for s390x/zfcpdump (Guillaume Nault)
- Fedora 5.17 configs round 1 (Justin M. Forbes)
- redhat: configs: disable the surface platform (David Arcari)
- redhat: configs: Disable team driver (Hangbin Liu) [1945477]
- configs: enable LOGITECH_FF for RHEL/CentOS too (Benjamin Tissoires)
- redhat/configs: Disable CONFIG_SENSORS_NCT6683 in RHEL for arm/aarch64 (Dean Nelson) [2041186]
- redhat: fix make {distg-brew,distg-koji} (Andrea Claudi)
- [fedora] Turn on CONFIG_VIDEO_OV5693 for sensor support (Dave Olsthoorn)
- Cleanup 'disabled' config options for RHEL (Prarit Bhargava)
- redhat: move CONFIG_ARM64_MTE to aarch64 config directory (Herton R. Krzesinski)
- Change CONFIG_TEST_BPF to a module (Justin M. Forbes)
- Change CONFIG_TEST_BPF to module in pending MR coming for proper review (Justin M. Forbes)
- redhat/configs: Enable CONFIG_TEST_BPF (Viktor Malik)
- Enable KUNIT tests for testing (Nico Pache)
- Makefile: Check PKGRELEASE size on dist-brew targets (Prarit Bhargava)
- kernel.spec: Add glibc-static build requirement (Prarit Bhargava)
- Enable iSER on s390x (Stefan Schulze Frielinghaus)
- redhat/configs: Enable CONFIG_ACER_WIRELESS (Peter Georg) [2025985]
- kabi: Add kABI macros for enum type (Čestmír Kalina) [2024595]
- kabi: expand and clarify documentation of aux structs (Čestmír Kalina) [2024595]
- kabi: introduce RH_KABI_USE_AUX_PTR (Čestmír Kalina) [2024595]
- kabi: rename RH_KABI_SIZE_AND_EXTEND to AUX (Čestmír Kalina) [2024595]
- kabi: more consistent _RH_KABI_SIZE_AND_EXTEND (Čestmír Kalina) [2024595]
- kabi: use fixed field name for extended part (Čestmír Kalina) [2024595]
- kabi: fix dereference in RH_KABI_CHECK_EXT (Čestmír Kalina) [2024595]
- kabi: fix RH_KABI_SET_SIZE macro (Čestmír Kalina) [2024595]
- kabi: expand and clarify documentation (Čestmír Kalina) [2024595]
- kabi: make RH_KABI_USE replace any number of reserved fields (Čestmír Kalina) [2024595]
- kabi: rename RH_KABI_USE2 to RH_KABI_USE_SPLIT (Čestmír Kalina) [2024595]
- kabi: change RH_KABI_REPLACE2 to RH_KABI_REPLACE_SPLIT (Čestmír Kalina) [2024595]
- kabi: change RH_KABI_REPLACE_UNSAFE to RH_KABI_BROKEN_REPLACE (Čestmír Kalina) [2024595]
- kabi: introduce RH_KABI_ADD_MODIFIER (Čestmír Kalina) [2024595]
- kabi: Include kconfig.h (Čestmír Kalina) [2024595]
- kabi: macros for intentional kABI breakage (Čestmír Kalina) [2024595]
- kabi: fix the note about terminating semicolon (Čestmír Kalina) [2024595]
- kabi: introduce RH_KABI_HIDE_INCLUDE and RH_KABI_FAKE_INCLUDE (Čestmír Kalina) [2024595]
- spec: don't overwrite auto.conf with .config (Ondrej Mosnacek)
- New configs in drivers/crypto (Fedora Kernel Team)
- Add test_hash to the mod-internal.list (Justin M. Forbes)
- configs: disable CONFIG_CRAMFS (Abhi Das) [2041184]
- spec: speed up "cp -r" when it overwrites existing files. (Denys Vlasenko)
- redhat: use centos x509.genkey file if building under centos (Herton R. Krzesinski)
- Revert "[redhat] Generate a crashkernel.default for each kernel build" (Coiby Xu)
- spec: make linux-firmware weak(er) dependency (Jan Stancek)
- rtw89: enable new driver rtw89 and device RTK8852AE (Íñigo Huguet)
- Config consolidation into common (Justin M. Forbes)
- Add packaged but empty /lib/modules/<kver>/systemtap/ (Justin M. Forbes)
- filter-modules.sh.rhel: Add ntc_thermistor to singlemods (Prarit Bhargava)
- Move CONFIG_SND_SOC_TLV320AIC31XX as it is now selected by CONFIG_SND_SOC_FSL_ASOC_CARD (Justin M. Forbes)
- Add dev_addr_lists_test to mod-internal.list (Justin M. Forbes)
- configs/fedora: Enable CONFIG_NFC_PN532_UART for use PN532 NFC module (Ziqian SUN (Zamir))
- redhat: ignore ksamples and kselftests on the badfuncs rpminspect test (Herton R. Krzesinski)
- redhat: disable upstream check for rpminspect (Herton R. Krzesinski)
- redhat: switch the vsyscall config to CONFIG_LEGACY_VSYSCALL_XONLY=y (Herton R. Krzesinski) [1876977]
- redhat: configs: increase CONFIG_DEBUG_KMEMLEAK_MEM_POOL_SIZE (Rafael Aquini)
- move CONFIG_STRICT_SIGALTSTACK_SIZE to the appropriate directory (David Arcari)
- redhat/configs: Enable CONFIG_DM_MULTIPATH_IOA for fedora (Benjamin Marzinski)
- redhat/configs: Enable CONFIG_DM_MULTIPATH_HST (Benjamin Marzinski) [2000835]
- redhat: Pull in openssl-devel as a build dependency correctly (Neal Gompa) [2034670]
- redhat/configs: Migrate ZRAM_DEF_* configs to common/ (Neal Gompa)
- redhat/configs: Enable CONFIG_CRYPTO_ZSTD (Neal Gompa) [2032758]
- Turn CONFIG_DEVMEM back off for aarch64 (Justin M. Forbes)
- Clean up excess text in Fedora config files (Justin M. Forbes)
- Fedora config updates for 5.16 (Justin M. Forbes)
- redhat/configs: enable CONFIG_INPUT_KEYBOARD for AARCH64 (Vitaly Kuznetsov)
- Fedora configs for 5.16 pt 1 (Justin M. Forbes)
- redhat/configs: NFS: disable UDP, insecure enctypes (Benjamin Coddington) [1952863]
- Update rebase-notes with dracut 5.17 information (Justin M. Forbes)
- redhat/configs: Enable CONFIG_CRYPTO_BLAKE2B (Neal Gompa) [2031547]
- Enable CONFIG_BPF_SYSCALL for zfcpdump (Jiri Olsa)
- Enable CONFIG_CIFS_SMB_DIRECT for ARK (Ronnie Sahlberg)
- mt76: enable new device MT7921E in CentOs/RHEL (Íñigo Huguet) [2004821]
- Disable CONFIG_DEBUG_PREEMPT on normal builds (Phil Auld)
- redhat/configs: Enable CONFIG_PCI_P2PDMA for ark (Myron Stowe)
- pci.h: Fix static include (Prarit Bhargava)
- Enable CONFIG_VFIO_NOIOMMU for Fedora (Justin M. Forbes)
- redhat/configs: enable CONFIG_NTB_NETDEV for ark (John W. Linville)
- drivers/pci/pci-driver.c: Fix if/ifdef typo (Prarit Bhargava)
- common: arm64: ensure all the required arm64 errata are enabled (Peter Robinson)
- kernel/rh_taint.c: Update to new messaging (Prarit Bhargava) [2019377]
- redhat/configs: enable CONFIG_AMD_PTDMA for ark (John W. Linville)
- redhat/configs: enable CONFIG_RD_ZSTD for rhel (Tao Liu) [2020132]
- fedora: build TEE as a module for all arches (Peter Robinson)
- common: build TRUSTED_KEYS in everywhere (Peter Robinson)
- redhat: make Patchlist.changelog generation conditional (Herton R. Krzesinski)
- redhat/configs: Add two new CONFIGs (Prarit Bhargava)
- redhat/configs: Remove dead CONFIG files (Prarit Bhargava)
- redhat/configs/evaluate_configs: Add find dead configs option (Prarit Bhargava)
- Add more rebase notes for Fedora 5.16 (Justin M. Forbes)
- Fedora: Feature: Retire wireless Extensions (Peter Robinson)
- fedora: arm: some SoC enablement pieces (Peter Robinson)
- fedora: arm: enable PCIE_ROCKCHIP_DW for rk35xx series (Peter Robinson)
- fedora: enable RTW89 802.11 WiFi driver (Peter Robinson)
- fedora: arm: Enable DRM_PANEL_EDP (Peter Robinson)
- fedora: sound: enable new sound drivers (Peter Robinson)
- redhat/configs: unset KEXEC_SIG for s390x zfcpdump (Coiby Xu)
- spec: Keep .BTF section in modules (Jiri Olsa)
- Fix up PREEMPT configs (Justin M. Forbes)
- New configs in drivers/media (Fedora Kernel Team)
- New configs in drivers/net/ethernet/litex (Fedora Kernel Team)
- spec: add bpf_testmod.ko to kselftests/bpf (Viktor Malik)
- New configs in drivers/net/wwan (Fedora Kernel Team)
- New configs in drivers/i2c (Fedora Kernel Team)
- redhat/docs/index.rst: Add local build information. (Prarit Bhargava)
- Fix up preempt configs (Justin M. Forbes)
- Turn on CONFIG_HID_NINTENDO for controller support (Dave Olsthoorn)
- Fedora: Enable MediaTek bluetooth pieces (Peter Robinson)
- Add rebase notes to check for PCI patches (Justin M. Forbes)
- redhat: configs: move CONFIG_ACCESSIBILITY from fedora to common (John W. Linville)
- Filter updates for hid-playstation on Fedora (Justin M. Forbes)
- Enable CONFIG_VIRT_DRIVERS for ARK (Vitaly Kuznetsov)
- redhat/configs: Enable Nitro Enclaves on aarch64 (Vitaly Kuznetsov)
- Enable e1000 in rhel9 as unsupported (Ken Cox) [2002344]
- Turn on COMMON_CLK_AXG_AUDIO for Fedora rhbz 2020481 (Justin M. Forbes)
- Fix up fedora config options from mismatch (Justin M. Forbes)
- Add nct6775 to filter-modules.sh.rhel (Justin M. Forbes)
- Enable PREEMPT_DYNAMIC for all but s390x (Justin M. Forbes)
- Add memcpy_kunit to mod-internal.list (Justin M. Forbes)
- New configs in fs/ksmbd (Fedora Kernel Team)
- Add nct6775 to Fedora filter-modules.sh (Justin M. Forbes)
- New configs in fs/ntfs3 (Fedora Kernel Team)
- Make CONFIG_IOMMU_DEFAULT_DMA_STRICT default for all but x86 (Justin M. Forbes)
- redhat/configs: enable  KEXEC_IMAGE_VERIFY_SIG for RHEL (Coiby Xu)
- redhat/configs: enable KEXEC_SIG for aarch64 RHEL (Coiby Xu) [1994858]
- Fix up fedora and pending configs for PREEMPT to end mismatch (Justin M. Forbes)
- Enable binder for fedora (Justin M. Forbes)
- redhat: configs: Update configs for vmware (Kamal Heib)
- Fedora configs for 5.15 (Justin M. Forbes)
- redhat/kernel.spec.template: don't hardcode gcov arches (Jan Stancek)
- redhat/configs: create a separate config for gcov options (Jan Stancek)
- Update documentation with FAQ and update frequency (Don Zickus)
- Document force pull option for mirroring (Don Zickus)
- Ignore the rhel9 kabi files (Don Zickus)
- Remove legacy elrdy cruft (Don Zickus)
- redhat/configs/evaluate_configs: walk cfgvariants line by line (Jan Stancek)
- redhat/configs/evaluate_configs: insert EMPTY tags at correct place (Jan Stancek)
- redhat: make dist-srpm-gcov add to BUILDOPTS (Jan Stancek)
- Build CONFIG_SPI_PXA2XX as a module on x86 (Justin M. Forbes)
- redhat/configs: enable CONFIG_BCMGENET as module (Joel Savitz)
- Fedora config updates (Justin M. Forbes)
- Enable CONFIG_FAIL_SUNRPC for debug builds (Justin M. Forbes)
- fedora: Disable fbdev drivers and use simpledrm instead (Javier Martinez Canillas)
- spec: Don't fail spec build if ksamples fails (Jiri Olsa)
- Enable CONFIG_QCOM_SCM for arm (Justin M. Forbes)
- redhat: Disable clang's integrated assembler on ppc64le and s390x (Tom Stellard)
- redhat/configs: enable CONFIG_IMA_WRITE_POLICY (Bruno Meneguele)
- Fix dist-srpm-gcov (Don Zickus)
- redhat: configs: add CONFIG_NTB and related items (John W. Linville)
- Add kfence_test to mod-internal.list (Justin M. Forbes)
- Enable KUNIT tests for redhat kernel-modules-internal (Nico Pache)
- redhat: add *-matched meta packages to rpminspect emptyrpm config (Herton R. Krzesinski)
- Use common config for NODES_SHIFT (Mark Salter)
- redhat: fix typo and make the output more silent for dist-git sync (Herton R. Krzesinski)
- Fedora NTFS config updates (Justin M. Forbes)
- Fedora 5.15 configs part 1 (Justin M. Forbes)
- Fix ordering in genspec args (Justin M. Forbes)
- redhat/configs: Enable Hyper-V guests on ARM64 (Vitaly Kuznetsov) [2007430]
- redhat: configs: Enable CONFIG_THINKPAD_LMI (Hans de Goede)
- redhat/docs: update Koji link to avoid redirect (Joel Savitz)
- redhat: add support for different profiles with dist*-brew (Herton R. Krzesinski)
- redhat: configs: Disable xtables and ipset (Phil Sutter) [1945179]
- redhat: Add mark_driver_deprecated() (Phil Sutter) [1945179]
- Change s390x CONFIG_NODES_SHIFT from 4 to 1 (Justin M. Forbes)
- Build CRYPTO_SHA3_*_S390 inline for s390 zfcpdump (Justin M. Forbes)
- redhat: move the DIST variable setting to Makefile.variables (Herton R. Krzesinski)
- redhat/kernel.spec.template: Cleanup source numbering (Prarit Bhargava)
- redhat/kernel.spec.template: Reorganize RHEL and Fedora specific files (Prarit Bhargava)
- redhat/kernel.spec.template: Add include_fedora and include_rhel variables (Prarit Bhargava)
- redhat/Makefile: Make kernel-local global (Prarit Bhargava)
- redhat/Makefile: Use flavors file (Prarit Bhargava)
- Turn on CONFIG_CPU_FREQ_GOV_SCHEDUTIL for x86 (Justin M. Forbes)
- redhat/configs: Remove CONFIG_INFINIBAND_I40IW (Kamal Heib)
- cleanup CONFIG_X86_PLATFORM_DRIVERS_INTEL (David Arcari)
- redhat: rename usage of .rhel8git.mk to .rhpkg.mk (Herton R. Krzesinski)
- Manually add pending items that need to be set due to mismatch (Justin M. Forbes)
- Clean up pending common (Justin M. Forbes)
- redhat/configs: Enable CONFIG_BLK_CGROUP_IOLATENCY & CONFIG_BLK_CGROUP_FC_APPID (Waiman Long) [2006813]
- redhat: remove kernel.changelog-8.99 file (Herton R. Krzesinski)
- redhat/configs: enable CONFIG_SQUASHFS_ZSTD which is already enabled in Fedora 34 (Tao Liu) [1998953]
- redhat: bump RHEL_MAJOR and add the changelog file for it (Herton R. Krzesinski)
- redhat: add documentation about the os-build rebase process (Herton R. Krzesinski)
- redhat/configs: enable SYSTEM_BLACKLIST_KEYRING which is already enabled in rhel8 and Fedora 34 (Coiby Xu)
- Build kernel-doc for Fedora (Justin M. Forbes)
- x86_64: Enable Elkhart Lake Quadrature Encoder Peripheral support (Prarit Bhargava)
- Update CONFIG_WERROR to disabled as it can cause issue with out of tree modules. (Justin M. Forbes)
- Fixup IOMMU configs in pending so that configs are sane again (Justin M. Forbes)
- Some initial Fedora config items for 5.15 (Justin M. Forbes)
- arm64: use common CONFIG_MAX_ZONEORDER for arm kernel (Mark Salter)
- Create Makefile.variables for a single point of configuration change (Justin M. Forbes)
- rpmspec: drop traceevent files instead of just excluding them from files list (Herton R. Krzesinski) [1967640]
- redhat/config: Enablement of CONFIG_PAPR_SCM for PowerPC (Gustavo Walbon) [1962936]
- Attempt to fix Intel PMT code (David Arcari)
- CI: Enable realtime branch testing (Veronika Kabatova)
- CI: Enable realtime checks for c9s and RHEL9 (Veronika Kabatova)
- ark: wireless: enable all rtw88 pcie wirless variants (Peter Robinson)
- wireless: rtw88: move debug options to common/debug (Peter Robinson)
- fedora: minor PTP clock driver cleanups (Peter Robinson)
- common: x86: enable VMware PTP support on ark (Peter Robinson)
- Disable liquidio driver on ark/rhel (Herton R. Krzesinski) [1993393]
- More Fedora config updates (Justin M. Forbes)
- Fedora config updates for 5.14 (Justin M. Forbes)
- CI: Rename ARK CI pipeline type (Veronika Kabatova)
- CI: Finish up c9s config (Veronika Kabatova)
- CI: Update ppc64le config (Veronika Kabatova)
- CI: use more templates (Veronika Kabatova)
- Filter updates for aarch64 (Justin M. Forbes)
- increase CONFIG_NODES_SHIFT for aarch64 (Chris von Recklinghausen) [1890304]
- redhat: configs: Enable CONFIG_WIRELESS_HOTKEY (Hans de Goede)
- redhat/configs: Update CONFIG_NVRAM (Desnes A. Nunes do Rosario) [1988254]
- common: serial: build in SERIAL_8250_LPSS for x86 (Peter Robinson)
- powerpc: enable CONFIG_FUNCTION_PROFILER (Diego Domingos) [1831065]
- redhat/configs: Disable Soft-RoCE driver (Kamal Heib)
- redhat/configs/evaluate_configs: Update help output (Prarit Bhargava)
- redhat/configs: Double MAX_LOCKDEP_CHAINS (Justin M. Forbes)
- fedora: configs: Fix WM5102 Kconfig (Hans de Goede)
- powerpc: enable CONFIG_POWER9_CPU (Diego Domingos) [1876436]
- redhat/configs: Fix CONFIG_VIRTIO_IOMMU to 'y' on aarch64 (Eric Auger) [1972795]
- filter-modules.sh: add more sound modules to filter (Jaroslav Kysela)
- redhat/configs: sound configuration cleanups and updates (Jaroslav Kysela)
- common: Update for CXL (Compute Express Link) configs (Peter Robinson)
- redhat: configs: disable CRYPTO_SM modules (Herton R. Krzesinski) [1990040]
- Remove fedora version of the LOCKDEP_BITS, we should use common (Justin M. Forbes)
- Re-enable sermouse for x86 (rhbz 1974002) (Justin M. Forbes)
- Fedora 5.14 configs round 1 (Justin M. Forbes)
- redhat: add gating configuration for centos stream/rhel9 (Herton R. Krzesinski)
- x86: configs: Enable CONFIG_TEST_FPU for debug kernels (Vitaly Kuznetsov) [1988384]
- redhat/configs: Move CHACHA and POLY1305 to core kernel to allow BIG_KEYS=y (root) [1983298]
- kernel.spec: fix build of samples/bpf (Jiri Benc)
- Enable OSNOISE_TRACER and TIMERLAT_TRACER (Jerome Marchand) [1979379]
- rpmspec: switch iio and gpio tools to use tools_make (Herton R. Krzesinski) [1956988]
- configs/process_configs.sh: Handle config items with no help text (Patrick Talbert)
- fedora: sound config updates for 5.14 (Peter Robinson)
- fedora: Only enable FSI drivers on POWER platform (Peter Robinson)
- The CONFIG_RAW_DRIVER has been removed from upstream (Peter Robinson)
- fedora: updates for 5.14 with a few disables for common from pending (Peter Robinson)
- fedora: migrate from MFD_TPS68470 -> INTEL_SKL_INT3472 (Peter Robinson)
- fedora: Remove STAGING_GASKET_FRAMEWORK (Peter Robinson)
- Fedora: move DRM_VMWGFX configs from ark -> common (Peter Robinson)
- fedora: arm: disabled unused FB drivers (Peter Robinson)
- fedora: don't enable FB_VIRTUAL (Peter Robinson)
- redhat/configs: Double MAX_LOCKDEP_ENTRIES (Waiman Long) [1940075]
- rpmspec: fix verbose output on kernel-devel installation (Herton R. Krzesinski) [1981406]
- Build Fedora x86s kernels with bytcr-wm5102 (Marius Hoch)
- Deleted redhat/configs/fedora/generic/x86/CONFIG_FB_HYPERV (Patrick Lang)
- rpmspec: correct the ghost initramfs attributes (Herton R. Krzesinski) [1977056]
- rpmspec: amend removal of depmod created files to include modules.builtin.alias.bin (Herton R. Krzesinski) [1977056]
- configs: remove duplicate CONFIG_DRM_HYPERV file (Patrick Talbert)
- CI: use common code for merge and release (Don Zickus)
- rpmspec: add release string to kernel doc directory name (Jan Stancek)
- redhat/configs: Add CONFIG_INTEL_PMT_CRASHLOG (Michael Petlan) [1880486]
- redhat/configs: Add CONFIG_INTEL_PMT_TELEMETRY (Michael Petlan) [1880486]
- redhat/configs: Add CONFIG_MFD_INTEL_PMT (Michael Petlan) [1880486]
- redhat/configs: enable CONFIG_BLK_DEV_ZONED (Ming Lei) [1638087]
- Add --with clang_lto option to build the kernel with Link Time Optimizations (Tom Stellard)
- common: disable DVB_AV7110 and associated pieces (Peter Robinson)
- Fix fedora-only config updates (Don Zickus)
- Fedor config update for new option (Justin M. Forbes)
- redhat/configs: Enable stmmac NIC for x86_64 (Mark Salter)
- all: hyperv: use the DRM driver rather than FB (Peter Robinson)
- all: hyperv: unify the Microsoft HyperV configs (Peter Robinson)
- all: VMWare: clean up VMWare configs (Peter Robinson)
- Update CONFIG_ARM_FFA_TRANSPORT (Patrick Talbert)
- CI: Handle all mirrors (Veronika Kabatova)
- Turn on CONFIG_STACKTRACE for s390x zfpcdump kernels (Justin M. Forbes)
- arm64: switch ark kernel to 4K pagesize (Mark Salter)
- Disable AMIGA_PARTITION and KARMA_PARTITION (Prarit Bhargava) [1802694]
- all: unify and cleanup i2c TPM2 modules (Peter Robinson)
- redhat/configs: Set CONFIG_VIRTIO_IOMMU on aarch64 (Eric Auger) [1972795]
- redhat/configs: Disable CONFIG_RT_GROUP_SCHED in rhel config (Phil Auld)
- redhat/configs: enable KEXEC_SIG which is already enabled in RHEL8 for s390x and x86_64 (Coiby Xu) [1976835]
- rpmspec: do not BuildRequires bpftool on noarch (Herton R. Krzesinski)
- redhat/configs: disable {IMA,EVM}_LOAD_X509 (Bruno Meneguele) [1977529]
- redhat: add secureboot CA certificate to trusted kernel keyring (Bruno Meneguele)
- redhat/configs: enable IMA_ARCH_POLICY for aarch64 and s390x (Bruno Meneguele)
- redhat/configs: Enable CONFIG_MLXBF_GIGE on aarch64 (Alaa Hleihel) [1858599]
- common: enable STRICT_MODULE_RWX everywhere (Peter Robinson)
- COMMON_CLK_STM32MP157_SCMI is bool and selects COMMON_CLK_SCMI (Justin M. Forbes)
- kernel.spec: Add kernel{,-debug}-devel-matched meta packages (Timothée Ravier)
- Turn off with_selftests for Fedora (Justin M. Forbes)
- Don't build bpftool on Fedora (Justin M. Forbes)
- Fix location of syscall scripts for kernel-devel (Justin M. Forbes)
- fedora: arm: Enable some i.MX8 options (Peter Robinson)
- Enable Landlock for Fedora (Justin M. Forbes)
- Filter update for Fedora aarch64 (Justin M. Forbes)
- rpmspec: only build debug meta packages where we build debug ones (Herton R. Krzesinski)
- rpmspec: do not BuildRequires bpftool on nobuildarches (Herton R. Krzesinski)
- redhat/configs: Consolidate CONFIG_HMC_DRV in the common s390x folder (Thomas Huth) [1976270]
- redhat/configs: Consolidate CONFIG_EXPOLINE_OFF in the common folder (Thomas Huth) [1976270]
- redhat/configs: Move CONFIG_HW_RANDOM_S390 into the s390x/ subfolder (Thomas Huth) [1976270]
- redhat/configs: Disable CONFIG_HOTPLUG_PCI_SHPC in the Fedora settings (Thomas Huth) [1976270]
- redhat/configs: Remove the non-existent CONFIG_NO_BOOTMEM switch (Thomas Huth) [1976270]
- redhat/configs: Compile the virtio-console as a module on s390x (Thomas Huth) [1976270]
- redhat/configs: Enable CONFIG_S390_CCW_IOMMU and CONFIG_VFIO_CCW for ARK, too (Thomas Huth) [1976270]
- Revert "Merge branch 'ec_fips' into 'os-build'" (Vladis Dronov) [1947240]
- Fix typos in fedora filters (Justin M. Forbes)
- More filtering for Fedora (Justin M. Forbes)
- Fix Fedora module filtering for spi-altera-dfl (Justin M. Forbes)
- Fedora 5.13 config updates (Justin M. Forbes)
- fedora: cleanup TCG_TIS_I2C_CR50 (Peter Robinson)
- fedora: drop duplicate configs (Peter Robinson)
- More Fedora config updates for 5.13 (Justin M. Forbes)
- redhat/configs: Enable needed drivers for BlueField SoC on aarch64 (Alaa Hleihel) [1858592 1858594 1858596]
- redhat: Rename mod-blacklist.sh to mod-denylist.sh (Prarit Bhargava)
- redhat/configs: enable CONFIG_NET_ACT_MPLS (Marcelo Ricardo Leitner)
- configs: Enable CONFIG_DEBUG_KERNEL for zfcpdump (Jiri Olsa)
- kernel.spec: Add support to use vmlinux.h (Don Zickus)
- spec: Add vmlinux.h to kernel-devel package (Jiri Olsa)
- Turn off DRM_XEN_FRONTEND for Fedora as we had DRM_XEN off already (Justin M. Forbes)
- Fedora 5.13 config updates pt 3 (Justin M. Forbes)
- all: enable ath11k wireless modules (Peter Robinson)
- all: Enable WWAN and associated MHI bus pieces (Peter Robinson)
- spec: Enable sefltests rpm build (Jiri Olsa)
- spec: Allow bpf selftest/samples to fail (Jiri Olsa)
- kvm: Add kvm_stat.service file and kvm_stat logrotate config to the tools (Jiri Benc)
- kernel.spec: Add missing source files to kernel-selftests-internal (Jiri Benc)
- kernel.spec: selftests: add net/forwarding to TARGETS list (Jiri Benc)
- kernel.spec: selftests: add build requirement on libmnl-devel (Jiri Benc)
- kernel.spec: add action.o to kernel-selftests-internal (Jiri Benc)
- kernel.spec: avoid building bpftool repeatedly (Jiri Benc)
- kernel.spec: selftests require python3 (Jiri Benc)
- kernel.spec: skip selftests that failed to build (Jiri Benc)
- kernel.spec: fix installation of bpf selftests (Jiri Benc)
- redhat: fix samples and selftests make options (Jiri Benc)
- kernel.spec: enable mptcp selftests for kernel-selftests-internal (Jiri Benc)
- kernel.spec: Do not export shared objects from libexecdir to RPM Provides (Jiri Benc)
- kernel.spec: add missing dependency for the which package (Jiri Benc)
- kernel.spec: add netfilter selftests to kernel-selftests-internal (Jiri Benc)
- kernel.spec: move slabinfo and page_owner_sort debuginfo to tools-debuginfo (Jiri Benc)
- kernel.spec: package and ship VM tools (Jiri Benc)
- configs: enable CONFIG_PAGE_OWNER (Jiri Benc)
- kernel.spec: add coreutils (Jiri Benc)
- kernel.spec: add netdevsim driver selftests to kernel-selftests-internal (Jiri Benc)
- redhat/Makefile: Clean out the --without flags from the baseonly rule (Jiri Benc)
- kernel.spec: Stop building unnecessary rpms for baseonly builds (Jiri Benc)
- kernel.spec: disable more kabi switches for gcov build (Jiri Benc)
- kernel.spec: Rename kabi-dw base (Jiri Benc)
- kernel.spec: Fix error messages during build of zfcpdump kernel (Jiri Benc)
- kernel.spec: perf: remove bpf examples (Jiri Benc)
- kernel.spec: selftests should not depend on modules-internal (Jiri Benc)
- kernel.spec: build samples (Jiri Benc)
- kernel.spec: tools: sync missing options with RHEL 8 (Jiri Benc)
- redhat/configs: nftables: Enable extra flowtable symbols (Phil Sutter)
- redhat/configs: Sync netfilter options with RHEL8 (Phil Sutter)
- Fedora 5.13 config updates pt 2 (Justin M. Forbes)
- Move CONFIG_ARCH_INTEL_SOCFPGA up a level for Fedora (Justin M. Forbes)
- fedora: enable the Rockchip rk3399 pcie drivers (Peter Robinson)
- Fedora 5.13 config updates pt 1 (Justin M. Forbes)
- Fix version requirement from opencsd-devel buildreq (Justin M. Forbes)
- configs/ark/s390: set CONFIG_MARCH_Z14 and CONFIG_TUNE_Z15 (Philipp Rudo) [1876435]
- configs/common/s390: Clean up CONFIG_{MARCH,TUNE}_Z* (Philipp Rudo)
- configs/process_configs.sh: make use of dummy-tools (Philipp Rudo)
- configs/common: disable CONFIG_INIT_STACK_ALL_{PATTERN,ZERO} (Philipp Rudo)
- configs/common/aarch64: disable CONFIG_RELR (Philipp Rudo)
- redhat/config: enable STMICRO nic for RHEL (Mark Salter)
- redhat/configs: Enable ARCH_TEGRA on RHEL (Mark Salter)
- redhat/configs: enable IMA_KEXEC for supported arches (Bruno Meneguele)
- redhat/configs: enable INTEGRITY_SIGNATURE to all arches (Bruno Meneguele)
- configs: enable CONFIG_LEDS_BRIGHTNESS_HW_CHANGED (Benjamin Tissoires)
- RHEL: disable io_uring support (Jeff Moyer) [1964537]
- all: Changing CONFIG_UV_SYSFS to build uv_sysfs.ko as a loadable module. (Frank Ramsay)
- Enable NITRO_ENCLAVES on RHEL (Vitaly Kuznetsov)
- Update the Quick Start documentation (David Ward)
- redhat/configs: Set PVPANIC_MMIO for x86 and PVPANIC_PCI for aarch64 (Eric Auger) [1961178]
- bpf: Fix unprivileged_bpf_disabled setup (Jiri Olsa)
- Enable CONFIG_BPF_UNPRIV_DEFAULT_OFF (Jiri Olsa)
- configs/common/s390: disable CONFIG_QETH_{OSN,OSX} (Philipp Rudo) [1903201]
- nvme: nvme_mpath_init remove multipath check (Mike Snitzer)
- Make CRYPTO_EC also builtin (Simo Sorce) [1947240]
- Do not hard-code a default value for DIST (David Ward)
- Override %%{debugbuildsenabled} if the --with-release option is used (David Ward)
- Improve comments in SPEC file, and move some option tests and macros (David Ward)
- configs: enable CONFIG_EXFAT_FS (Pavel Reichl) [1943423]
- Revert s390x/zfcpdump part of a9d179c40281 and ecbfddd98621 (Vladis Dronov)
- Embed crypto algos, modes and templates needed in the FIPS mode (Vladis Dronov) [1947240]
- configs: Add and enable CONFIG_HYPERV_TESTING for debug kernels (Mohammed Gamal)
- configs: enable CONFIG_CMA on x86_64 in ARK (David Hildenbrand) [1945002]
- rpmspec: build debug-* meta-packages if debug builds are disabled (Herton R. Krzesinski)
- UIO: disable unused config options (Aristeu Rozanski) [1957819]
- ARK-config: Make amd_pinctrl module builtin (Hans de Goede)
- rpmspec: revert/drop content hash for kernel-headers (Herton R. Krzesinski)
- rpmspec: fix check that calls InitBuildVars (Herton R. Krzesinski)
- fedora: enable zonefs (Damien Le Moal)
- redhat: load specific ARCH keys to INTEGRITY_PLATFORM_KEYRING (Bruno Meneguele)
- redhat: enable INTEGRITY_TRUSTED_KEYRING across all variants (Bruno Meneguele)
- redhat: enable SYSTEM_BLACKLIST_KEYRING across all variants (Bruno Meneguele)
- redhat: enable INTEGRITY_ASYMMETRIC_KEYS across all variants (Bruno Meneguele)
- Remove unused boot loader specification files (David Ward)
- redhat/configs: Enable mlx5 IPsec and TLS offloads (Alaa Hleihel) [1869674 1957636]
- common: disable Apple Silicon generally (Peter Robinson)
- cleanup Intel's FPGA configs (Peter Robinson)
- common: move PTP KVM support from ark to common (Peter Robinson)
- Enable CONFIG_DRM_AMDGPU_USERPTR for everyone (Justin M. Forbes)
- redhat: add initial rpminspect configuration (Herton R. Krzesinski)
- fedora: arm updates for 5.13 (Peter Robinson)
- fedora: Enable WWAN and associated MHI bits (Peter Robinson)
- Update CONFIG_MODPROBE_PATH to /usr/sbin (Justin Forbes)
- Fedora set modprobe path (Justin M. Forbes)
- Keep sctp and l2tp modules in modules-extra (Don Zickus)
- Fix ppc64le cross build packaging (Don Zickus)
- Fedora: Make amd_pinctrl module builtin (Hans de Goede)
- Keep CONFIG_KASAN_HW_TAGS off for aarch64 debug configs (Justin M. Forbes)
- New configs in drivers/bus (Fedora Kernel Team)
- RHEL: Don't build KVM PR module on ppc64 (David Gibson) [1930649]
- Flip CONFIG_USB_ROLE_SWITCH from m to y (Justin M. Forbes)
- Set valid options for CONFIG_FW_LOADER_USER_HELPER (Justin M. Forbes)
- Clean up CONFIG_FB_MODE_HELPERS (Justin M. Forbes)
- Turn off CONFIG_VFIO for the s390x zfcpdump kernel (Justin M. Forbes)
- Delete unused CONFIG_SND_SOC_MAX98390 pending-common (Justin M. Forbes)
- Update pending-common configs, preparing to set correctly (Justin M. Forbes)
- Update fedora filters for surface (Justin M. Forbes)
- Build CONFIG_CRYPTO_ECDSA inline for s390x zfcpdump (Justin M. Forbes)
- Replace "flavour" where "variant" is meant instead (David Ward)
- Drop the %%{variant} macro and fix --with-vanilla (David Ward)
- Fix syntax of %%kernel_variant_files (David Ward)
- Change description of --without-vdso-install to fix typo (David Ward)
- Config updates to work around mismatches (Justin M. Forbes)
- CONFIG_SND_SOC_FSL_ASOC_CARD selects CONFIG_MFD_WM8994 now (Justin M. Forbes)
- wireguard: disable in FIPS mode (Hangbin Liu) [1940794]
- Enable mtdram for fedora (rhbz 1955916) (Justin M. Forbes)
- Remove reference to bpf-helpers man page (Justin M. Forbes)
- Fedora: enable more modules for surface devices (Dave Olsthoorn)
- Fix Fedora config mismatch for CONFIG_FSL_ENETC_IERB (Justin M. Forbes)
- hardlink is in /usr/bin/ now (Justin M. Forbes)
- Ensure CONFIG_KVM_BOOK3S_64_PR stays on in Fedora, even if it is turned off in RHEL (Justin M. Forbes)
- Set date in package release from repository commit, not system clock (David Ward)
- Use a better upstream tarball filename for snapshots (David Ward)
- Don't create empty pending-common files on pending-fedora commits (Don Zickus)
- nvme: decouple basic ANA log page re-read support from native multipathing (Mike Snitzer)
- nvme: allow local retry and proper failover for REQ_FAILFAST_TRANSPORT (Mike Snitzer)
- nvme: Return BLK_STS_TARGET if the DNR bit is set (Mike Snitzer)
- Add redhat/configs/pending-common/generic/s390x/zfcpdump/CONFIG_NETFS_SUPPORT (Justin M. Forbes)
- Create ark-latest branch last for CI scripts (Don Zickus)
- Replace /usr/libexec/platform-python with /usr/bin/python3 (David Ward)
- Turn off ADI_AXI_ADC and AD9467 which now require CONFIG_OF (Justin M. Forbes)
- Export ark infrastructure files (Don Zickus)
- docs: Update docs to reflect newer workflow. (Don Zickus)
- Use upstream/master for merge-base with fallback to master (Don Zickus)
- Fedora: Turn off the SND_INTEL_BYT_PREFER_SOF option (Hans de Goede)
- filter-modules.sh.fedora: clean up "netprots" (Paul Bolle)
- filter-modules.sh.fedora: clean up "scsidrvs" (Paul Bolle)
- filter-*.sh.fedora: clean up "ethdrvs" (Paul Bolle)
- filter-*.sh.fedora: clean up "driverdirs" (Paul Bolle)
- filter-*.sh.fedora: remove incorrect entries (Paul Bolle)
- filter-*.sh.fedora: clean up "singlemods" (Paul Bolle)
- filter-modules.sh.fedora: drop unused list "iiodrvs" (Paul Bolle)
- Update mod-internal to fix depmod issue (Nico Pache)
- Turn on CONFIG_VDPA_SIM_NET (rhbz 1942343) (Justin M. Forbes)
- New configs in drivers/power (Fedora Kernel Team)
- Turn on CONFIG_NOUVEAU_DEBUG_PUSH for debug configs (Justin M. Forbes)
- Turn off KFENCE sampling by default for Fedora (Justin M. Forbes)
- Fedora config updates round 2 (Justin M. Forbes)
- New configs in drivers/soc (Jeremy Cline)
- filter-modules.sh: Fix copy/paste error 'input' (Paul Bolle)
- Update module filtering for 5.12 kernels (Justin M. Forbes)
- Fix genlog.py to ensure that comments retain "%%" characters. (Mark Mielke)
- New configs in drivers/leds (Fedora Kernel Team)
- Limit CONFIG_USB_CDNS_SUPPORT to x86_64 and arm in Fedora (David Ward)
- Fedora: Enable CHARGER_GPIO on aarch64 too (Peter Robinson)
- Fedora config updates (Justin M. Forbes)
- configs: enable CONFIG_WIREGUARD in ARK (Hangbin Liu) [1613522]
- Remove duplicate configs acroos fedora, ark and common (Don Zickus)
- Combine duplicate configs across ark and fedora into common (Don Zickus)
- common/ark: cleanup and unify the parport configs (Peter Robinson)
- iommu/vt-d: enable INTEL_IDXD_SVM for both fedora and rhel (Jerry Snitselaar)
- REDHAT: coresight: etm4x: Disable coresight on HPE Apollo 70 (Jeremy Linton)
- configs/common/generic: disable CONFIG_SLAB_MERGE_DEFAULT (Rafael Aquini)
- Remove _legacy_common_support (Justin M. Forbes)
- redhat/mod-blacklist.sh: Fix floppy blacklisting (Hans de Goede)
- New configs in fs/pstore (CKI@GitLab)
- New configs in arch/powerpc (Fedora Kernel Team)
- configs: enable BPF LSM on Fedora and ARK (Ondrej Mosnacek)
- configs: clean up LSM configs (Ondrej Mosnacek)
- New configs in drivers/platform (CKI@GitLab)
- New configs in drivers/firmware (CKI@GitLab)
- New configs in drivers/mailbox (Fedora Kernel Team)
- New configs in drivers/net/phy (Justin M. Forbes)
- Update CONFIG_DM_MULTIPATH_IOA (Augusto Caringi)
- New configs in mm/Kconfig (CKI@GitLab)
- New configs in arch/powerpc (Jeremy Cline)
- New configs in arch/powerpc (Jeremy Cline)
- New configs in drivers/input (Fedora Kernel Team)
- New configs in net/bluetooth (Justin M. Forbes)
- New configs in drivers/clk (Fedora Kernel Team)
- New configs in init/Kconfig (Jeremy Cline)
- redhat: allow running fedora-configs and rh-configs targets outside of redhat/ (Herton R. Krzesinski)
- all: unify the disable of goldfish (android emulation platform) (Peter Robinson)
- common: minor cleanup/de-dupe of dma/dmabuf debug configs (Peter Robinson)
- common/ark: these drivers/arches were removed in 5.12 (Peter Robinson)
- Correct kernel-devel make prepare build for 5.12. (Paulo E. Castro)
- redhat: add initial support for centos stream dist-git sync on Makefiles (Herton R. Krzesinski)
- redhat/configs: Enable CONFIG_SCHED_STACK_END_CHECK for Fedora and ARK (Josh Poimboeuf) [1856174]
- CONFIG_VFIO now selects IOMMU_API instead of depending on it, causing several config mismatches for the zfcpdump kernel (Justin M. Forbes)
- Turn off weak-modules for Fedora (Justin M. Forbes)
- redhat: enable CONFIG_FW_LOADER_COMPRESS for ARK (Herton R. Krzesinski) [1939095]
- Fedora: filters: update to move dfl-emif to modules (Peter Robinson)
- drop duplicate DEVFREQ_GOV_SIMPLE_ONDEMAND config (Peter Robinson)
- efi: The EFI_VARS is legacy and now x86 only (Peter Robinson)
- common: enable RTC_SYSTOHC to supplement update_persistent_clock64 (Peter Robinson)
- generic: arm: enable SCMI for all options (Peter Robinson)
- fedora: the PCH_CAN driver is x86-32 only (Peter Robinson)
- common: disable legacy CAN device support (Peter Robinson)
- common: Enable Microchip MCP251x/MCP251xFD CAN controllers (Peter Robinson)
- common: Bosch MCAN support for Intel Elkhart Lake (Peter Robinson)
- common: enable CAN_PEAK_PCIEFD PCI-E driver (Peter Robinson)
- common: disable CAN_PEAK_PCIEC PCAN-ExpressCard (Peter Robinson)
- common: enable common CAN layer 2 protocols (Peter Robinson)
- ark: disable CAN_LEDS option (Peter Robinson)
- Fedora: Turn on SND_SOC_INTEL_SKYLAKE_HDAUDIO_CODEC option (Hans de Goede)
- Fedora: enable modules for surface devices (Dave Olsthoorn)
- Turn on SND_SOC_INTEL_SOUNDWIRE_SOF_MACH for Fedora again (Justin M. Forbes)
- common: fix WM8804 codec dependencies (Peter Robinson)
- Build SERIO_SERPORT as a module (Peter Robinson)
- input: touchscreen: move ELO and Wacom serial touchscreens to x86 (Peter Robinson)
- Sync serio touchscreens for non x86 architectures to the same as ARK (Peter Robinson)
- Only enable SERIO_LIBPS2 on x86 (Peter Robinson)
- Only enable PC keyboard controller and associated keyboard on x86 (Peter Robinson)
- Generic: Mouse: Tweak generic serial mouse options (Peter Robinson)
- Only enable PS2 Mouse options on x86 (Peter Robinson)
- Disable bluetooth highspeed by default (Peter Robinson)
- Fedora: A few more general updates for 5.12 window (Peter Robinson)
- Fedora: Updates for 5.12 merge window (Peter Robinson)
- Fedora: remove dead options that were removed upstream (Peter Robinson)
- redhat: remove CONFIG_DRM_PANEL_XINGBANGDA_XBD599 (Herton R. Krzesinski)
- New configs in arch/powerpc (Fedora Kernel Team)
- Turn on CONFIG_PPC_QUEUED_SPINLOCKS as it is default upstream now (Justin M. Forbes)
- Update pending-common configs to address new upstream config deps (Justin M. Forbes)
- rpmspec: ship gpio-watch.debug in the proper debuginfo package (Herton R. Krzesinski)
- Removed description text as a comment confuses the config generation (Justin M. Forbes)
- New configs in drivers/dma-buf (Jeremy Cline)
- Fedora: ARMv7: build for 16 CPUs. (Peter Robinson)
- Fedora: only enable DEBUG_HIGHMEM on debug kernels (Peter Robinson)
- process_configs.sh: fix find/xargs data flow (Ondrej Mosnacek)
- Fedora config update (Justin M. Forbes)
- fedora: minor arm sound config updates (Peter Robinson)
- Fix trailing white space in redhat/configs/fedora/generic/CONFIG_SND_INTEL_BYT_PREFER_SOF (Justin M. Forbes)
- Add a redhat/rebase-notes.txt file (Hans de Goede)
- Turn on SND_INTEL_BYT_PREFER_SOF for Fedora (Hans de Goede)
- CI: Drop MR ID from the name variable (Veronika Kabatova)
- redhat: add DUP and kpatch certificates to system trusted keys for RHEL build (Herton R. Krzesinski)
- The comments in CONFIG_USB_RTL8153_ECM actually turn off CONFIG_USB_RTL8152 (Justin M. Forbes)
- Update CKI pipeline project (Veronika Kabatova)
- Turn off additional KASAN options for Fedora (Justin M. Forbes)
- Rename the master branch to rawhide for Fedora (Justin M. Forbes)
- Makefile targets for packit integration (Ben Crocker)
- Turn off KASAN for rawhide debug builds (Justin M. Forbes)
- New configs in arch/arm64 (Justin Forbes)
- Remove deprecated Intel MIC config options (Peter Robinson)
- redhat: replace inline awk script with genlog.py call (Herton R. Krzesinski)
- redhat: add genlog.py script (Herton R. Krzesinski)
- kernel.spec.template - fix use_vdso usage (Ben Crocker)
- redhat: remove remaining references of CONFIG_RH_DISABLE_DEPRECATED (Herton R. Krzesinski)
- Turn off vdso_install for ppc (Justin M. Forbes)
- Remove bpf-helpers.7 from bpftool package (Jiri Olsa)
- New configs in lib/Kconfig.debug (Fedora Kernel Team)
- Turn off CONFIG_VIRTIO_CONSOLE for s390x zfcpdump (Justin M. Forbes)
- New configs in drivers/clk (Justin M. Forbes)
- Keep VIRTIO_CONSOLE on s390x available. (Jakub Čajka)
- New configs in lib/Kconfig.debug (Jeremy Cline)
- Fedora 5.11 config updates part 4 (Justin M. Forbes)
- Fedora 5.11 config updates part 3 (Justin M. Forbes)
- Fedora 5.11 config updates part 2 (Justin M. Forbes)
- Update internal (test) module list from RHEL-8 (Joe Lawrence) [1915073]
- Fix USB_XHCI_PCI regression (Justin M. Forbes)
- fedora: fixes for ARMv7 build issue by disabling HIGHPTE (Peter Robinson)
- all: s390x: Increase CONFIG_PCI_NR_FUNCTIONS to 512 (#1888735) (Dan Horák)
- Fedora 5.11 configs pt 1 (Justin M. Forbes)
- redhat: avoid conflict with mod-blacklist.sh and released_kernel defined (Herton R. Krzesinski)
- redhat: handle certificate files conditionally as done for src.rpm (Herton R. Krzesinski)
- specfile: add %%{?_smp_mflags} to "make headers_install" in tools/testing/selftests (Denys Vlasenko)
- specfile: add %%{?_smp_mflags} to "make samples/bpf/" (Denys Vlasenko)
- Run MR testing in CKI pipeline (Veronika Kabatova)
- Reword comment (Nicolas Chauvet)
- Add with_cross_arm conditional (Nicolas Chauvet)
- Redefines __strip if with_cross (Nicolas Chauvet)
- fedora: only enable ACPI_CONFIGFS, ACPI_CUSTOM_METHOD in debug kernels (Peter Robinson)
- fedora: User the same EFI_CUSTOM_SSDT_OVERLAYS as ARK (Peter Robinson)
- all: all arches/kernels enable the same DMI options (Peter Robinson)
- all: move SENSORS_ACPI_POWER to common/generic (Peter Robinson)
- fedora: PCIE_HISI_ERR is already in common (Peter Robinson)
- all: all ACPI platforms enable ATA_ACPI so move it to common (Peter Robinson)
- all: x86: move shared x86 acpi config options to generic (Peter Robinson)
- All: x86: Move ACPI_VIDEO to common/x86 (Peter Robinson)
- All: x86: Enable ACPI_DPTF (Intel DPTF) (Peter Robinson)
- All: enable ACPI_BGRT for all ACPI platforms. (Peter Robinson)
- All: Only build ACPI_EC_DEBUGFS for debug kernels (Peter Robinson)
- All: Disable Intel Classmate PC ACPI_CMPC option (Peter Robinson)
- cleanup: ACPI_PROCFS_POWER was removed upstream (Peter Robinson)
- All: ACPI: De-dupe the ACPI options that are the same across ark/fedora on x86/arm (Peter Robinson)
- Enable the vkms module in Fedora (Jeremy Cline)
- Fedora: arm updates for 5.11 and general cross Fedora cleanups (Peter Robinson)
- Add gcc-c++ to BuildRequires (Justin M. Forbes)
- Update CONFIG_KASAN_HW_TAGS (Justin M. Forbes)
- fedora: arm: move generic power off/reset to all arm (Peter Robinson)
- fedora: ARMv7: build in DEVFREQ_GOV_SIMPLE_ONDEMAND until I work out why it's changed (Peter Robinson)
- fedora: cleanup joystick_adc (Peter Robinson)
- fedora: update some display options (Peter Robinson)
- fedora: arm: enable TI PRU options (Peter Robinson)
- fedora: arm: minor exynos plaform updates (Peter Robinson)
- arm: SoC: disable Toshiba Visconti SoC (Peter Robinson)
- common: disable ARCH_BCM4908 (NFC) (Peter Robinson)
- fedora: minor arm config updates (Peter Robinson)
- fedora: enable Tegra 234 SoC (Peter Robinson)
- fedora: arm: enable new Hikey 3xx options (Peter Robinson)
- Fedora: USB updates (Peter Robinson)
- fedora: enable the GNSS receiver subsystem (Peter Robinson)
- Remove POWER_AVS as no longer upstream (Peter Robinson)
- Cleanup RESET_RASPBERRYPI (Peter Robinson)
- Cleanup GPIO_CDEV_V1 options. (Peter Robinson)
- fedora: arm crypto updates (Peter Robinson)
- CONFIG_KASAN_HW_TAGS for aarch64 (Justin M. Forbes)
- Fedora: cleanup PCMCIA configs, move to x86 (Peter Robinson)
- New configs in drivers/rtc (Fedora Kernel Team)
- redhat/configs: Enable CONFIG_GCC_PLUGIN_STRUCTLEAK_BYREF_ALL (Josh Poimboeuf) [1856176]
- redhat/configs: Enable CONFIG_GCC_PLUGIN_STRUCTLEAK (Josh Poimboeuf) [1856176]
- redhat/configs: Enable CONFIG_GCC_PLUGINS on ARK (Josh Poimboeuf) [1856176]
- redhat/configs: Enable CONFIG_KASAN on Fedora (Josh Poimboeuf) [1856176]
- New configs in init/Kconfig (Fedora Kernel Team)
- build_configs.sh: Fix syntax flagged by shellcheck (Ben Crocker)
- genspec.sh: Fix syntax flagged by shellcheck (Ben Crocker)
- mod-blacklist.sh: Fix syntax flagged by shellcheck (Ben Crocker)
- Enable Speakup accessibility driver (Justin M. Forbes)
- New configs in init/Kconfig (Fedora Kernel Team)
- Fix fedora config mismatch due to dep changes (Justin M. Forbes)
- New configs in drivers/crypto (Jeremy Cline)
- Remove duplicate ENERGY_MODEL configs (Peter Robinson)
- This is selected by PCIE_QCOM so must match (Justin M. Forbes)
- drop unused BACKLIGHT_GENERIC (Peter Robinson)
- Remove cp instruction already handled in instruction below. (Paulo E. Castro)
- Add all the dependencies gleaned from running `make prepare` on a bloated devel kernel. (Paulo E. Castro)
- Add tools to path mangling script. (Paulo E. Castro)
- Remove duplicate cp statement which is also not specific to x86. (Paulo E. Castro)
- Correct orc_types failure whilst running `make prepare` https://bugzilla.redhat.com/show_bug.cgi?id=1882854 (Paulo E. Castro)
- redhat: ark: enable CONFIG_IKHEADERS (Jiri Olsa)
- Add missing '$' sign to (GIT) in redhat/Makefile (Augusto Caringi)
- Remove filterdiff and use native git instead (Don Zickus)
- New configs in net/sched (Justin M. Forbes)
- New configs in drivers/mfd (CKI@GitLab)
- New configs in drivers/mfd (Fedora Kernel Team)
- New configs in drivers/firmware (Fedora Kernel Team)
- Temporarily backout parallel xz script (Justin M. Forbes)
- redhat: explicitly disable CONFIG_IMA_APPRAISE_SIGNED_INIT (Bruno Meneguele)
- redhat: enable CONFIG_EVM_LOAD_X509 on ARK (Bruno Meneguele)
- redhat: enable CONFIG_EVM_ATTR_FSUUID on ARK (Bruno Meneguele)
- redhat: enable CONFIG_EVM in all arches and flavors (Bruno Meneguele)
- redhat: enable CONFIG_IMA_LOAD_X509 on ARK (Bruno Meneguele)
- redhat: set CONFIG_IMA_DEFAULT_HASH to SHA256 (Bruno Meneguele)
- redhat: enable CONFIG_IMA_SECURE_AND_OR_TRUSTED_BOOT (Bruno Meneguele)
- redhat: enable CONFIG_IMA_READ_POLICY on ARK (Bruno Meneguele)
- redhat: set default IMA template for all ARK arches (Bruno Meneguele)
- redhat: enable CONFIG_IMA_DEFAULT_HASH_SHA256 for all flavors (Bruno Meneguele)
- redhat: disable CONFIG_IMA_DEFAULT_HASH_SHA1 (Bruno Meneguele)
- redhat: enable CONFIG_IMA_ARCH_POLICY for ppc and x86 (Bruno Meneguele)
- redhat: enable CONFIG_IMA_APPRAISE_MODSIG (Bruno Meneguele)
- redhat: enable CONFIG_IMA_APPRAISE_BOOTPARAM (Bruno Meneguele)
- redhat: enable CONFIG_IMA_APPRAISE (Bruno Meneguele)
- redhat: enable CONFIG_INTEGRITY for aarch64 (Bruno Meneguele)
- kernel: Update some missing KASAN/KCSAN options (Jeremy Linton)
- kernel: Enable coresight on aarch64 (Jeremy Linton)
- Update CONFIG_INET6_ESPINTCP (Justin Forbes)
- New configs in net/ipv6 (Justin M. Forbes)
- fedora: move CONFIG_RTC_NVMEM options from ark to common (Peter Robinson)
- configs: Enable CONFIG_DEBUG_INFO_BTF (Don Zickus)
- fedora: some minor arm audio config tweaks (Peter Robinson)
- Ship xpad with default modules on Fedora and RHEL (Bastien Nocera)
- Fedora: Only enable legacy serial/game port joysticks on x86 (Peter Robinson)
- Fedora: Enable the options required for the Librem 5 Phone (Peter Robinson)
- Fedora config update (Justin M. Forbes)
- Fedora config change because CONFIG_FSL_DPAA2_ETH now selects CONFIG_FSL_XGMAC_MDIO (Justin M. Forbes)
- redhat: generic  enable CONFIG_INET_MPTCP_DIAG (Davide Caratti)
- Fedora config update (Justin M. Forbes)
- Enable NANDSIM for Fedora (Justin M. Forbes)
- Re-enable CONFIG_ACPI_TABLE_UPGRADE for Fedora since upstream disables this if secureboot is active (Justin M. Forbes)
- Ath11k related config updates (Justin M. Forbes)
- Fedora config updates for ath11k (Justin M. Forbes)
- Turn on ATH11K for Fedora (Justin M. Forbes)
- redhat: enable CONFIG_INTEL_IOMMU_SVM (Jerry Snitselaar)
- More Fedora config fixes (Justin M. Forbes)
- Fedora 5.10 config updates (Justin M. Forbes)
- Fedora 5.10 configs round 1 (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Allow kernel-tools to build without selftests (Don Zickus)
- Allow building of kernel-tools standalone (Don Zickus)
- redhat: ark: disable CONFIG_NET_ACT_CTINFO (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_TEQL (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_SFB (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_QFQ (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_PLUG (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_PIE (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_HHF (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_DSMARK (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_DRR (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_CODEL (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_CHOKE (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_CBQ (Davide Caratti)
- redhat: ark: disable CONFIG_NET_SCH_ATM (Davide Caratti)
- redhat: ark: disable CONFIG_NET_EMATCH and sub-targets (Davide Caratti)
- redhat: ark: disable CONFIG_NET_CLS_TCINDEX (Davide Caratti)
- redhat: ark: disable CONFIG_NET_CLS_RSVP6 (Davide Caratti)
- redhat: ark: disable CONFIG_NET_CLS_RSVP (Davide Caratti)
- redhat: ark: disable CONFIG_NET_CLS_ROUTE4 (Davide Caratti)
- redhat: ark: disable CONFIG_NET_CLS_BASIC (Davide Caratti)
- redhat: ark: disable CONFIG_NET_ACT_SKBMOD (Davide Caratti)
- redhat: ark: disable CONFIG_NET_ACT_SIMP (Davide Caratti)
- redhat: ark: disable CONFIG_NET_ACT_NAT (Davide Caratti)
- arm64/defconfig: Enable CONFIG_KEXEC_FILE (Bhupesh Sharma) [1821565]
- redhat/configs: Cleanup CONFIG_CRYPTO_SHA512 (Prarit Bhargava)
- New configs in drivers/mfd (Fedora Kernel Team)
- Fix LTO issues with kernel-tools (Don Zickus)
- Point pathfix to the new location for gen_compile_commands.py (Justin M. Forbes)
- configs: Disable CONFIG_SECURITY_SELINUX_DISABLE (Ondrej Mosnacek)
- [Automatic] Handle config dependency changes (Don Zickus)
- configs/iommu: Add config comment to empty CONFIG_SUN50I_IOMMU file (Jerry Snitselaar)
- New configs in kernel/trace (Fedora Kernel Team)
- Fix Fedora config locations (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- configs: enable CONFIG_CRYPTO_CTS=y so cts(cbc(aes)) is available in FIPS mode (Vladis Dronov) [1855161]
- Partial revert: Add master merge check (Don Zickus)
- Update Maintainers doc to reflect workflow changes (Don Zickus)
- WIP: redhat/docs: Update documentation for single branch workflow (Prarit Bhargava)
- Add CONFIG_ARM64_MTE which is not picked up by the config scripts for some reason (Justin M. Forbes)
- Disable Speakup synth DECEXT (Justin M. Forbes)
- Enable Speakup for Fedora since it is out of staging (Justin M. Forbes)
- Modify patchlist changelog output (Don Zickus)
- process_configs.sh: Fix syntax flagged by shellcheck (Ben Crocker)
- generate_all_configs.sh: Fix syntax flagged by shellcheck (Ben Crocker)
- redhat/self-test: Initial commit (Ben Crocker)
- arch/x86: Remove vendor specific CPU ID checks (Prarit Bhargava)
- redhat: Replace hardware.redhat.com link in Unsupported message (Prarit Bhargava) [1810301]
- x86: Fix compile issues with rh_check_supported() (Don Zickus)
- KEYS: Make use of platform keyring for module signature verify (Robert Holmes)
- Input: rmi4 - remove the need for artificial IRQ in case of HID (Benjamin Tissoires)
- ARM: tegra: usb no reset (Peter Robinson)
- arm: make CONFIG_HIGHPTE optional without CONFIG_EXPERT (Jon Masters)
- redhat: rh_kabi: deduplication friendly structs (Jiri Benc)
- redhat: rh_kabi add a comment with warning about RH_KABI_EXCLUDE usage (Jiri Benc)
- redhat: rh_kabi: introduce RH_KABI_EXTEND_WITH_SIZE (Jiri Benc)
- redhat: rh_kabi: Indirect EXTEND macros so nesting of other macros will resolve. (Don Dutile)
- redhat: rh_kabi: Fix RH_KABI_SET_SIZE to use dereference operator (Tony Camuso)
- redhat: rh_kabi: Add macros to size and extend structs (Prarit Bhargava)
- Removing Obsolete hba pci-ids from rhel8 (Dick Kennedy) [1572321]
- mptsas: pci-id table changes (Laura Abbott)
- mptspi: pci-id table changes (Laura Abbott)
- qla2xxx: Remove PCI IDs of deprecated adapter (Jeremy Cline)
- hpsa: remove old cciss-based smartarray pci ids (Joseph Szczypek) [1471185]
- kernel: add SUPPORT_REMOVED kernel taint (Tomas Henzl) [1602033]
- Rename RH_DISABLE_DEPRECATED to RHEL_DIFFERENCES (Don Zickus)
- s390: Lock down the kernel when the IPL secure flag is set (Jeremy Cline)
- efi: Lock down the kernel if booted in secure boot mode (David Howells)
- efi: Add an EFI_SECURE_BOOT flag to indicate secure boot mode (David Howells)
- security: lockdown: expose a hook to lock the kernel down (Jeremy Cline)
- Make get_cert_list() use efi_status_to_str() to print error messages. (Peter Jones)
- Add efi_status_to_str() and rework efi_status_to_err(). (Peter Jones)
- Add support for deprecating processors (Laura Abbott) [1565717 1595918 1609604 1610493]
- arm: aarch64: Drop the EXPERT setting from ARM64_FORCE_52BIT (Jeremy Cline)
- iommu/arm-smmu: workaround DMA mode issues (Laura Abbott)
- rh_kabi: introduce RH_KABI_EXCLUDE (Jakub Racek) [1652256]
- ipmi: do not configure ipmi for HPE m400 (Laura Abbott) [1670017]
- kABI: Add generic kABI macros to use for kABI workarounds (Myron Stowe) [1546831]
- add pci_hw_vendor_status() (Maurizio Lombardi) [1590829]
- ahci: thunderx2: Fix for errata that affects stop engine (Robert Richter) [1563590]
- Vulcan: AHCI PCI bar fix for Broadcom Vulcan early silicon (Robert Richter) [1563590]
- bpf: set unprivileged_bpf_disabled to 1 by default, add a boot parameter (Eugene Syromiatnikov) [1561171]
- add Red Hat-specific taint flags (Eugene Syromiatnikov) [1559877]
- tags.sh: Ignore redhat/rpm (Jeremy Cline)
- put RHEL info into generated headers (Laura Abbott) [1663728]
- aarch64: acpi scan: Fix regression related to X-Gene UARTs (Mark Salter) [1519554]
- ACPI / irq: Workaround firmware issue on X-Gene based m400 (Mark Salter) [1519554]
- modules: add rhelversion MODULE_INFO tag (Laura Abbott)
- ACPI: APEI: arm64: Ignore broken HPE moonshot APEI support (Al Stone) [1518076]
- Add Red Hat tainting (Laura Abbott) [1565704 1652266]
- Introduce CONFIG_RH_DISABLE_DEPRECATED (Laura Abbott)
- Stop merging ark-patches for release (Don Zickus)
- Fix path location for ark-update-configs.sh (Don Zickus)
- Combine Red Hat patches into single patch (Don Zickus)
- New configs in drivers/misc (Jeremy Cline)
- New configs in drivers/net/wireless (Justin M. Forbes)
- New configs in drivers/phy (Fedora Kernel Team)
- New configs in drivers/tty (Fedora Kernel Team)
- Set SquashFS decompression options for all flavors to match RHEL (Bohdan Khomutskyi)
- configs: Enable CONFIG_ENERGY_MODEL (Phil Auld)
- New configs in drivers/pinctrl (Fedora Kernel Team)
- Update CONFIG_THERMAL_NETLINK (Justin Forbes)
- Separate merge-upstream and release stages (Don Zickus)
- Re-enable CONFIG_IR_SERIAL on Fedora (Prarit Bhargava)
- Create Patchlist.changelog file (Don Zickus)
- Filter out upstream commits from changelog (Don Zickus)
- Merge Upstream script fixes (Don Zickus)
- kernel.spec: Remove kernel-keys directory on rpm erase (Prarit Bhargava)
- Add mlx5_vdpa to module filter for Fedora (Justin M. Forbes)
- Add python3-sphinx_rtd_theme buildreq for docs (Justin M. Forbes)
- redhat/configs/process_configs.sh: Remove *.config.orig files (Prarit Bhargava)
- redhat/configs/process_configs.sh: Add process_configs_known_broken flag (Prarit Bhargava)
- redhat/Makefile: Fix '*-configs' targets (Prarit Bhargava)
- dist-merge-upstream: Checkout known branch for ci scripts (Don Zickus)
- kernel.spec: don't override upstream compiler flags for ppc64le (Dan Horák)
- Fedora config updates (Justin M. Forbes)
- Fedora confi gupdate (Justin M. Forbes)
- mod-sign.sh: Fix syntax flagged by shellcheck (Ben Crocker)
- Swap how ark-latest is built (Don Zickus)
- Add extra version bump to os-build branch (Don Zickus)
- dist-release: Avoid needless version bump. (Don Zickus)
- Add dist-fedora-release target (Don Zickus)
- Remove redundant code in dist-release (Don Zickus)
- Makefile.common rename TAG to _TAG (Don Zickus)
- Fedora config change (Justin M. Forbes)
- Fedora filter update (Justin M. Forbes)
- Config update for Fedora (Justin M. Forbes)
- enable PROTECTED_VIRTUALIZATION_GUEST for all s390x kernels (Dan Horák)
- redhat: ark: enable CONFIG_NET_SCH_TAPRIO (Davide Caratti)
- redhat: ark: enable CONFIG_NET_SCH_ETF (Davide Caratti)
- More Fedora config updates (Justin M. Forbes)
- New config deps (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- First half of config updates for Fedora (Justin M. Forbes)
- Updates for Fedora arm architectures for the 5.9 window (Peter Robinson)
- Merge 5.9 config changes from Peter Robinson (Justin M. Forbes)
- Add config options that only show up when we prep on arm (Justin M. Forbes)
- Config updates for Fedora (Justin M. Forbes)
- fedora: enable enery model (Peter Robinson)
- Use the configs/generic config for SND_HDA_INTEL everywhere (Peter Robinson)
- Enable ZSTD compression algorithm on all kernels (Peter Robinson)
- Enable ARM_SMCCC_SOC_ID on all aarch64 kernels (Peter Robinson)
- iio: enable LTR-559 light and proximity sensor (Peter Robinson)
- iio: chemical: enable some popular chemical and partical sensors (Peter Robinson)
- More mismatches (Justin M. Forbes)
- Fedora config change due to deps (Justin M. Forbes)
- CONFIG_SND_SOC_MAX98390 is now selected by SND_SOC_INTEL_DA7219_MAX98357A_GENERIC (Justin M. Forbes)
- Config change required for build part 2 (Justin M. Forbes)
- Config change required for build (Justin M. Forbes)
- Fedora config update (Justin M. Forbes)
- Add ability to sync upstream through Makefile (Don Zickus)
- Add master merge check (Don Zickus)
- Replace hardcoded values 'os-build' and project id with variables (Don Zickus)
- redhat/Makefile.common: Fix MARKER (Prarit Bhargava)
- gitattributes: Remove unnecesary export restrictions (Prarit Bhargava)
- Add new certs for dual signing with boothole (Justin M. Forbes)
- Update secureboot signing for dual keys (Justin M. Forbes)
- fedora: enable LEDS_SGM3140 for arm configs (Peter Robinson)
- Enable CONFIG_DM_VERITY_VERIFY_ROOTHASH_SIG (Justin M. Forbes)
- redhat/configs: Fix common CONFIGs (Prarit Bhargava)
- redhat/configs: General CONFIG cleanups (Prarit Bhargava)
- redhat/configs: Update & generalize evaluate_configs (Prarit Bhargava)
- fedora: arm: Update some meson config options (Peter Robinson)
- redhat/docs: Add Fedora RPM tagging date (Prarit Bhargava)
- Update config for renamed panel driver. (Peter Robinson)
- Enable SERIAL_SC16IS7XX for SPI interfaces (Peter Robinson)
- s390x-zfcpdump: Handle missing Module.symvers file (Don Zickus)
- Fedora config updates (Justin M. Forbes)
- redhat/configs: Add .tmp files to .gitignore (Prarit Bhargava)
- disable uncommon TCP congestion control algorithms (Davide Caratti)
- Add new bpf man pages (Justin M. Forbes)
- Add default option for CONFIG_ARM64_BTI_KERNEL to pending-common so that eln kernels build (Justin M. Forbes)
- redhat/Makefile: Add fedora-configs and rh-configs make targets (Prarit Bhargava)
- redhat/configs: Use SHA512 for module signing (Prarit Bhargava)
- genspec.sh: 'touch' empty Patchlist file for single tarball (Don Zickus)
- Fedora config update for rc1 (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- redhat/Makefile.common: fix RPMKSUBLEVEL condition (Ondrej Mosnacek)
- redhat/Makefile: silence KABI tar output (Ondrej Mosnacek)
- One more Fedora config update (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Fix PATCHLEVEL for merge window (Justin M. Forbes)
- Change ark CONFIG_COMMON_CLK to yes, it is selected already by other options (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- More module filtering for Fedora (Justin M. Forbes)
- Update filters for rnbd in Fedora (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Fix up module filtering for 5.8 (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- More Fedora config work (Justin M. Forbes)
- RTW88BE and CE have been extracted to their own modules (Justin M. Forbes)
- Set CONFIG_BLK_INLINE_ENCRYPTION_FALLBACK for Fedora (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Arm64 Use Branch Target Identification for kernel (Justin M. Forbes)
- Change value of CONFIG_SECURITY_SELINUX_CHECKREQPROT_VALUE (Justin M. Forbes)
- Fedora config updates (Justin M. Forbes)
- Fix configs for Fedora (Justin M. Forbes)
- Add zero-commit to format-patch options (Justin M. Forbes)
- Copy Makefile.rhelver as a source file rather than a patch (Jeremy Cline)
- Move the sed to clear the patch templating outside of conditionals (Justin M. Forbes)
- Match template format in kernel.spec.template (Justin M. Forbes)
- Break out the Patches into individual files for dist-git (Justin M. Forbes)
- Break the Red Hat patch into individual commits (Jeremy Cline)
- Fix update_scripts.sh unselective pattern sub (David Howells)
- Add cec to the filter overrides (Justin M. Forbes)
- Add overrides to filter-modules.sh (Justin M. Forbes)
- redhat/configs: Enable CONFIG_SMC91X and disable CONFIG_SMC911X (Prarit Bhargava) [1722136]
- Include bpftool-struct_ops man page in the bpftool package (Jeremy Cline)
- Add sharedbuffer_configuration.py to the pathfix.py script (Jeremy Cline)
- Use __make macro instead of make (Tom Stellard)
- Sign off generated configuration patches (Jeremy Cline)
- Drop the static path configuration for the Sphinx docs (Jeremy Cline)
- redhat: Add dummy-module kernel module (Prarit Bhargava)
- redhat: enable CONFIG_LWTUNNEL_BPF (Jiri Benc)
- Remove typoed config file aarch64CONFIG_SM_GCC_8150 (Justin M. Forbes)
- Add Documentation back to kernel-devel as it has Kconfig now (Justin M. Forbes)
- Copy distro files rather than moving them (Jeremy Cline)
- kernel.spec: fix 'make scripts' for kernel-devel package (Brian Masney)
- Makefile: correct help text for dist-cross-<arch>-rpms (Brian Masney)
- redhat/Makefile: Fix RHEL8 python warning (Prarit Bhargava)
- redhat: Change Makefile target names to dist- (Prarit Bhargava)
- configs: Disable Serial IR driver (Prarit Bhargava)
- Fix "multiple %%files for package kernel-tools" (Pablo Greco)
- Introduce a Sphinx documentation project (Jeremy Cline)
- Build ARK against ELN (Don Zickus)
- Drop the requirement to have a remote called linus (Jeremy Cline)
- Rename 'internal' branch to 'os-build' (Don Zickus)
- Only include open merge requests with "Include in Releases" label (Jeremy Cline)
- Package gpio-watch in kernel-tools (Jeremy Cline)
- Exit non-zero if the tag already exists for a release (Jeremy Cline)
- Adjust the changelog update script to not push anything (Jeremy Cline)
- Drop --target noarch from the rh-rpms make target (Jeremy Cline)
- Add a script to generate release tags and branches (Jeremy Cline)
- Set CONFIG_VDPA for fedora (Justin M. Forbes)
- Add a README to the dist-git repository (Jeremy Cline)
- Provide defaults in ark-rebase-patches.sh (Jeremy Cline)
- Default ark-rebase-patches.sh to not report issues (Jeremy Cline)
- Drop DIST from release commits and tags (Jeremy Cline)
- Place the buildid before the dist in the release (Jeremy Cline)
- Sync up with Fedora arm configuration prior to merging (Jeremy Cline)
- Disable CONFIG_PROTECTED_VIRTUALIZATION_GUEST for zfcpdump (Jeremy Cline)
- Add RHMAINTAINERS file and supporting conf (Don Zickus)
- Add a script to test if all commits are signed off (Jeremy Cline)
- Fix make rh-configs-arch (Don Zickus)
- Drop RH_FEDORA in favor of the now-merged RHEL_DIFFERENCES (Jeremy Cline)
- Sync up Fedora configs from the first week of the merge window (Jeremy Cline)
- Migrate blacklisting floppy.ko to mod-blacklist.sh (Don Zickus)
- kernel packaging: Combine mod-blacklist.sh and mod-extra-blacklist.sh (Don Zickus)
- kernel packaging: Fix extra namespace collision (Don Zickus)
- mod-extra.sh: Rename to mod-blacklist.sh (Don Zickus)
- mod-extra.sh: Make file generic (Don Zickus)
- Fix a painfully obvious YAML syntax error in .gitlab-ci.yml (Jeremy Cline)
- Add in armv7hl kernel header support (Don Zickus)
- Disable all BuildKernel commands when only building headers (Don Zickus)
- Drop any gitlab-ci patches from ark-patches (Jeremy Cline)
- Build the srpm for internal branch CI using the vanilla tree (Jeremy Cline)
- Pull in the latest ARM configurations for Fedora (Jeremy Cline)
- Fix xz memory usage issue (Neil Horman)
- Use ark-latest instead of master for update script (Jeremy Cline)
- Move the CI jobs back into the ARK repository (Jeremy Cline)
- Sync up ARK's Fedora config with the dist-git repository (Jeremy Cline)
- Pull in the latest configuration changes from Fedora (Jeremy Cline)
- configs: enable CONFIG_NET_SCH_CBS (Marcelo Ricardo Leitner)
- Drop configuration options in fedora/ that no longer exist (Jeremy Cline)
- Set RH_FEDORA for ARK and Fedora (Jeremy Cline)
- redhat/kernel.spec: Include the release in the kernel COPYING file (Jeremy Cline)
- redhat/kernel.spec: add scripts/jobserver-exec to py3_shbang_opts list (Jeremy Cline)
- redhat/kernel.spec: package bpftool-gen man page (Jeremy Cline)
- distgit-changelog: handle multiple y-stream BZ numbers (Bruno Meneguele)
- redhat/kernel.spec: remove all inline comments (Bruno Meneguele)
- redhat/genspec: awk unknown whitespace regex pattern (Bruno Meneguele)
- Improve the readability of gen_config_patches.sh (Jeremy Cline)
- Fix some awkward edge cases in gen_config_patches.sh (Jeremy Cline)
- Update the CI environment to use Fedora 31 (Jeremy Cline)
- redhat: drop whitespace from with_gcov macro (Jan Stancek)
- configs: Enable CONFIG_KEY_DH_OPERATIONS on ARK (Ondrej Mosnacek)
- configs: Adjust CONFIG_MPLS_ROUTING and CONFIG_MPLS_IPTUNNEL (Laura Abbott)
- New configs in lib/crypto (Jeremy Cline)
- New configs in drivers/char (Jeremy Cline)
- Turn on BLAKE2B for Fedora (Jeremy Cline)
- kernel.spec.template: Clean up stray *.h.s files (Laura Abbott)
- Build the SRPM in the CI job (Jeremy Cline)
- New configs in net/tls (Jeremy Cline)
- New configs in net/tipc (Jeremy Cline)
- New configs in lib/kunit (Jeremy Cline)
- Fix up released_kernel case (Laura Abbott)
- New configs in lib/Kconfig.debug (Jeremy Cline)
- New configs in drivers/ptp (Jeremy Cline)
- New configs in drivers/nvme (Jeremy Cline)
- New configs in drivers/net/phy (Jeremy Cline)
- New configs in arch/arm64 (Jeremy Cline)
- New configs in drivers/crypto (Jeremy Cline)
- New configs in crypto/Kconfig (Jeremy Cline)
- Add label so the Gitlab to email bridge ignores the changelog (Jeremy Cline)
- Temporarily switch TUNE_DEFAULT to y (Jeremy Cline)
- Run config test for merge requests and internal (Jeremy Cline)
- Add missing licensedir line (Laura Abbott)
- redhat/scripts: Remove redhat/scripts/rh_get_maintainer.pl (Prarit Bhargava)
- configs: Take CONFIG_DEFAULT_MMAP_MIN_ADDR from Fedra (Laura Abbott)
- configs: Turn off ISDN (Laura Abbott)
- Add a script to generate configuration patches (Laura Abbott)
- Introduce rh-configs-commit (Laura Abbott)
- kernel-packaging: Remove kernel files from kernel-modules-extra package (Prarit Bhargava)
- configs: Enable CONFIG_DEBUG_WX (Laura Abbott)
- configs: Disable wireless USB (Laura Abbott)
- Clean up some temporary config files (Laura Abbott)
- configs: New config in drivers/gpu for v5.4-rc1 (Jeremy Cline)
- configs: New config in arch/powerpc for v5.4-rc1 (Jeremy Cline)
- configs: New config in crypto for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/usb for v5.4-rc1 (Jeremy Cline)
- AUTOMATIC: New configs (Jeremy Cline)
- Skip ksamples for bpf, they are broken (Jeremy Cline)
- configs: New config in fs/erofs for v5.4-rc1 (Jeremy Cline)
- configs: New config in mm for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/md for v5.4-rc1 (Jeremy Cline)
- configs: New config in init for v5.4-rc1 (Jeremy Cline)
- configs: New config in fs/fuse for v5.4-rc1 (Jeremy Cline)
- merge.pl: Avoid comments but do not skip them (Don Zickus)
- configs: New config in drivers/net/ethernet/pensando for v5.4-rc1 (Jeremy Cline)
- Update a comment about what released kernel means (Laura Abbott)
- Provide both Fedora and RHEL files in the SRPM (Laura Abbott)
- kernel.spec.template: Trim EXTRAVERSION in the Makefile (Laura Abbott)
- kernel.spec.template: Add macros for building with nopatches (Laura Abbott)
- kernel.spec.template: Add some macros for Fedora differences (Laura Abbott)
- kernel.spec.template: Consolodate the options (Laura Abbott)
- configs: Add pending direcory to Fedora (Laura Abbott)
- kernel.spec.template: Don't run hardlink if rpm-ostree is in use (Laura Abbott)
- configs: New config in net/can for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/net/phy for v5.4-rc1 (Jeremy Cline)
- configs: Increase x86_64 NR_UARTS to 64 (Prarit Bhargava) [1730649]
- configs: turn on ARM64_FORCE_52BIT for debug builds (Jeremy Cline)
- kernel.spec.template: Tweak the python3 mangling (Laura Abbott)
- kernel.spec.template: Add --with verbose option (Laura Abbott)
- kernel.spec.template: Switch to using %%install instead of %%__install (Laura Abbott)
- kernel.spec.template: Make the kernel.org URL https (Laura Abbott)
- kernel.spec.template: Update message about secure boot signing (Laura Abbott)
- kernel.spec.template: Move some with flags definitions up (Laura Abbott)
- kernel.spec.template: Update some BuildRequires (Laura Abbott)
- kernel.spec.template: Get rid of %%clean (Laura Abbott)
- configs: New config in drivers/char for v5.4-rc1 (Jeremy Cline)
- configs: New config in net/sched for v5.4-rc1 (Jeremy Cline)
- configs: New config in lib for v5.4-rc1 (Jeremy Cline)
- configs: New config in fs/verity for v5.4-rc1 (Jeremy Cline)
- configs: New config in arch/aarch64 for v5.4-rc4 (Jeremy Cline)
- configs: New config in arch/arm64 for v5.4-rc1 (Jeremy Cline)
- Flip off CONFIG_ARM64_VA_BITS_52 so the bundle that turns it on applies (Jeremy Cline)
- New configuration options for v5.4-rc4 (Jeremy Cline)
- Correctly name tarball for single tarball builds (Laura Abbott)
- configs: New config in drivers/pci for v5.4-rc1 (Jeremy Cline)
- Allow overriding the dist tag on the command line (Laura Abbott)
- Allow scratch branch target to be overridden (Laura Abbott)
- Remove long dead BUILD_DEFAULT_TARGET (Laura Abbott)
- Amend the changelog when rebasing (Laura Abbott)
- configs: New config in drivers/platform for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/pinctrl for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/net/wireless for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/net/ethernet/mellanox for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/net/can for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/hid for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/dma-buf for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/crypto for v5.4-rc1 (Jeremy Cline)
- configs: New config in arch/s390 for v5.4-rc1 (Jeremy Cline)
- configs: New config in block for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/cpuidle for v5.4-rc1 (Jeremy Cline)
- redhat: configs: Split CONFIG_CRYPTO_SHA512 (Laura Abbott)
- redhat: Set Fedora options (Laura Abbott)
- Set CRYPTO_SHA3_*_S390 to builtin on zfcpdump (Jeremy Cline)
- configs: New config in drivers/edac for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/firmware for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/hwmon for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/iio for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/mmc for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/tty for v5.4-rc1 (Jeremy Cline)
- configs: New config in arch/s390 for v5.4-rc1 (Jeremy Cline)
- configs: New config in drivers/bus for v5.4-rc1 (Jeremy Cline)
- Add option to allow mismatched configs on the command line (Laura Abbott)
- configs: New config in drivers/crypto for v5.4-rc1 (Jeremy Cline)
- configs: New config in sound/pci for v5.4-rc1 (Jeremy Cline)
- configs: New config in sound/soc for v5.4-rc1 (Jeremy Cline)
- gitlab: Add CI job for packaging scripts (Major Hayden)
- Speed up CI with CKI image (Major Hayden)
- Disable e1000 driver in ARK (Neil Horman)
- configs: Fix the pending default for CONFIG_ARM64_VA_BITS_52 (Jeremy Cline)
- configs: Turn on OPTIMIZE_INLINING for everything (Jeremy Cline)
- configs: Set valid pending defaults for CRYPTO_ESSIV (Jeremy Cline)
- Add an initial CI configuration for the internal branch (Jeremy Cline)
- New drop of configuration options for v5.4-rc1 (Jeremy Cline)
- New drop of configuration options for v5.4-rc1 (Jeremy Cline)
- Pull the RHEL version defines out of the Makefile (Jeremy Cline)
- Sync up the ARK build scripts (Jeremy Cline)
- Sync up the Fedora Rawhide configs (Jeremy Cline)
- Sync up the ARK config files (Jeremy Cline)
- configs: Adjust CONFIG_FORCE_MAX_ZONEORDER for Fedora (Laura Abbott)
- configs: Add README for some other arches (Laura Abbott)
- configs: Sync up Fedora configs (Laura Abbott)
- [initial commit] Add structure for building with git (Laura Abbott)
- [initial commit] Add Red Hat variables in the top level makefile (Laura Abbott)
- [initial commit] Red Hat gitignore and attributes (Laura Abbott)
- [initial commit] Add changelog (Laura Abbott)
- [initial commit] Add makefile (Laura Abbott)
- [initial commit] Add files for generating the kernel.spec (Laura Abbott)
- [initial commit] Add rpm directory (Laura Abbott)
- [initial commit] Add files for packaging (Laura Abbott)
- [initial commit] Add kabi files (Laura Abbott)
- [initial commit] Add scripts (Laura Abbott)
- [initial commit] Add configs (Laura Abbott)
- [initial commit] Add Makefiles (Laura Abbott)
- Linux v6.18.0-0.rc0.755fa5b4fb36

###
# The following Emacs magic makes C-c C-e use UTC dates.
# Local Variables:
# rpm-change-log-uses-utc: t
# End:
###
