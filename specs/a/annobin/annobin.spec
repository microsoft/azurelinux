# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


Name:    annobin
Summary: Annotate and examine compiled binary files
Version: 12.99
Release: 2%{?dist}
License: GPL-3.0-or-later AND LGPL-2.0-or-later AND (GPL-2.0-or-later WITH GCC-exception-2.0) AND (LGPL-2.0-or-later WITH GCC-exception-2.0) AND GFDL-1.3-or-later
URL: https://sourceware.org/annobin/
# Maintainer: nickc@redhat.com
# Web Page: https://sourceware.org/annobin/
# Watermark Protocol: https://fedoraproject.org/wiki/Toolchain/Watermark

#---------------------------------------------------------------------------------

# Use "--without tests" to disable the testsuite.
%bcond_without tests

# Use "--without annocheck" to disable the installation of the annocheck program.
%bcond_without annocheck

# Use "--with debuginfod" to force support for debuginfod to be compiled into
# the annocheck program.  By default the configure script will check for
# availablilty at build time, but this might not match the run time situation.
# FIXME: Add a --without debuginfod option to forcefully disable the configure
# time check for debuginfod support.
%bcond_with debuginfod

# Use "--without clangplugin" to disable the building of the annobin plugin for Clang.
%bcond_without clangplugin

# Use "--without gccplugin" to disable the building of the annobin plugin for GCC.
%bcond_without gccplugin

# Use "--without llvmplugin" to disable the building of the annobin plugin for LLVM.
%bcond_without llvmplugin

# Set this to zero to disable the requirement for a specific version of gcc.
# This should only be needed if there is some kind of problem with the version
# checking logic or when building on RHEL-7 or earlier.
#
# Update: now that we have gcc version checking support in redhat-rpm-config
# there is no longer a great need for a hard gcc version check here.  Not
# enabling this check greatly simplifies the process of installing a new major
# version of gcc into the buildroot.
%global with_hard_gcc_version_requirement 0

%bcond_without plugin_rebuild
# Allow the building of annobin without using annobin itself.
# This is because if we are bootstrapping a new build environment we can have
# a new version of gcc installed, but without a new of annobin installed.
# (i.e. we are building the new version of annobin to go with the new version
# of gcc).  If the *old* annobin plugin is used whilst building this new
# version, the old plugin will complain that version of gcc for which it
# was built is different from the version of gcc that is now being used, and
# then it will abort.
#
# The default is to use plugin during rebuilds (cf BZ 1630550) but this can
# be changed because of the need to be able to rebuild annobin when a change
# to gcc breaks the version installed into the buildroot.  Note however that
# uncommenting the lines below will result in annocheck not passing the rpminspect
# tests....
# %%if %%{without plugin_rebuild}
# %%undefine _annotated_build
# %%endif

#---------------------------------------------------------------------------------

%global annobin_sources annobin-%{version}.tar.xz
Source: https://nickc.fedorapeople.org/%{annobin_sources}
# For the latest sources use:  git clone git://sourceware.org/git/annobin.git

# This is where a copy of the sources will be installed.
%global annobin_source_dir %{_usrsrc}/annobin

# Insert patches here, if needed.  Eg:
# Patch01: annobin-plugin-default-string-notes.patch

#---------------------------------------------------------------------------------

# Make sure that the necessary sub-packages are built.

%if %{with gccplugin}
Requires: %{name}-plugin-gcc
%endif

%if %{with llvmplugin}
Requires: %{name}-plugin-llvm
%endif

%if %{with clangplugin}
Requires: %{name}-plugin-clang
%endif

#---------------------------------------------------------------------------------

%description
This package contains the tools needed to annotate binary files created by
compilers, and also the tools needed to examine those annotations.

%if %{with gccplugin}
One of the tools is a plugin for GCC that records information about the
security options that were in effect when the binary was compiled.

Note - the plugin is automatically enabled in gcc builds via flags
provided by the redhat-rpm-macros package.
%endif

%if %{with clangplugin}
One of the tools is a plugin for Clang that records information about the
security options that were in effect when the binary was compiled.
%endif

%if %{with llvmplugin}
One of the tools is a plugin for LLVM that records information about the
security options that were in effect when the binary was compiled.
%endif

%if %{with annocheck}
One of the tools is a security checker which analyses the notes present in
annotated files and reports on any missing security options.
%endif

#---------------------------------------------------------------------------

# Now that we have sub-packages for all of the plugins and for annocheck,
# there are no executables left to go into the "annobin" rpm.  But top-level
# packages cannot have "BuildArch: noarch" if sub-packages do have
# architecture requirements, and rpmlint generates an error if an
# architecture specific rpm does not contain any binaries.  So instead all of
# the documentation has been moved into an architecture neutral sub-package,
# and there no longer is a top level annobin rpm at all.

%package docs
Summary: Documentation and shell scripts for use with annobin
BuildArch: noarch
# The documentation uses pod2man...
BuildRequires: perl-interpreter perl-podlators gawk make sharutils

%description docs
Provides the documentation files and example shell scripts for use with annobin.

#----------------------------------------------------------------------------
%if %{with tests}

%package tests
Summary: Test scripts and binaries for checking the behaviour and output of the annobin plugin
Requires: %{name}-docs = %{version}-%{release}
BuildRequires: make sharutils
%if %{with debuginfod}
BuildRequires: elfutils-debuginfod-client-devel
%endif

%description tests
Provides a means to test the generation of annotated binaries and the parsing
of the resulting files.

%endif

#----------------------------------------------------------------------------
%if %{with annocheck}

%package annocheck
Summary: A tool for checking the security hardening status of binaries

BuildRequires: gcc elfutils elfutils-devel elfutils-libelf-devel rpm-devel make

%if %{with debuginfod}
BuildRequires: elfutils-debuginfod-client-devel
%endif

Requires: %{name}-docs = %{version}-%{release}
Requires: cpio rpm

%description annocheck
Installs the annocheck program which uses the notes generated by annobin to
check that the specified files were compiled with the correct security
hardening options.

%package libannocheck
Summary: A library for checking the security hardening status of binaries

BuildRequires: gcc elfutils elfutils-devel elfutils-libelf-devel rpm-devel make

%if %{with debuginfod}
BuildRequires: elfutils-debuginfod-client-devel
%endif

Requires: %{name}-docs = %{version}-%{release}

%description libannocheck
Installs the libannocheck library which uses the notes generated by the
annobin plugins to check that the specified files were compiled with the
correct security hardening options.

%endif

#----------------------------------------------------------------------------
%if %{with gccplugin}

%package plugin-gcc
Summary: annobin gcc plugin

Requires: %{name}-docs = %{version}-%{release}
Conflicts: %{name} <= 9.60-1
BuildRequires: gcc-c++ gcc-plugin-devel

# [Stolen from gcc-python-plugin]
# GCC will only load plugins that were built against exactly that build of GCC
# We thus need to embed the exact GCC version as a requirement within the
# metadata.
#
# Define "gcc_vr", a variable to hold the VERSION-RELEASE string for the gcc
# we are being built against.
#
# Unfortunately, we can't simply run:
#   rpm -q --qf="%%{version}-%%{release}"
# to determine this, as there's no guarantee of a sane rpm database within
# the chroots created by our build system
#
# So we instead query the version from gcc's output.
#
# gcc.spec has:
#   Version: %%{gcc_version}
#   Release: %%{gcc_release}%%{?dist}
#   ...snip...
#   echo 'Red Hat %%{version}-%%{gcc_release}' > gcc/DEV-PHASE
#
# So, given this output:
#
#   $ gcc --version
#   gcc (GCC) 4.6.1 20110908 (Red Hat 4.6.1-9)
#   Copyright (C) 2011 Free Software Foundation, Inc.
#   This is free software; see the source for copying conditions.  There is NO
#   warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# we can scrape out the "4.6.1" from the version line.
#
# The following implements the above:

%global gcc_vr %(gcc --version | head -n 1 | sed -e 's|.*(Red\ Hat\ ||g' -e 's|)$||g')

# We need the major version of gcc.
%global gcc_major %(echo "%{gcc_vr}" | cut -f1 -d".")
%global gcc_next  %(v="%{gcc_major}"; echo $((++v)))

# Needed when building the srpm.
%if 0%{?gcc_major} == 0
%global gcc_major 0
%endif

# For a gcc plugin gcc is required.
%if %{with_hard_gcc_version_requirement}
# BZ 1607430 - There is an exact requirement on the major version of gcc.
Requires: (gcc >= %{gcc_major} with gcc < %{gcc_next})
%else
Requires: gcc
%endif

# Information about the gcc plugin is recorded in this file.
%global aver annobin-plugin-version-info

%description plugin-gcc
Installs an annobin plugin that can be used by gcc.

%endif

#---------------------------------------------------------------------------------
%if %{with llvmplugin}

%package plugin-llvm
Summary: annobin llvm plugin

Requires: %{name}-docs = %{version}-%{release}
Requires: llvm-libs
Conflicts: %{name} <= 9.60-1
BuildRequires: clang clang-devel llvm llvm-devel compiler-rt

%description plugin-llvm
Installs an annobin plugin that can be used by LLVM tools.

%endif

#---------------------------------------------------------------------------------
%if %{with clangplugin}

%package plugin-clang
Summary: annobin clang plugin

Requires: %{name}-docs = %{version}-%{release}
Requires: llvm-libs
Conflicts: %{name} <= 9.60-1
BuildRequires: clang clang-devel llvm llvm-devel compiler-rt

%description plugin-clang
Installs an annobin plugin that can be used by Clang.

%endif

#---------------------------------------------------------------------------------

# Decide where the plugins will live.  Change if necessary.

%global ANNOBIN_GCC_PLUGIN_DIR %(gcc --print-file-name=plugin)

%{!?llvm_plugin_dir:%global  llvm_plugin_dir  %{_libdir}/llvm/plugins}
%{!?clang_plugin_dir:%global clang_plugin_dir %{_libdir}/clang/plugins}

#---------------------------------------------------------------------------------

%prep
if [ -z "%{gcc_vr}" ]; then
    echo "*** Missing gcc_vr spec file macro, cannot continue." >&2
    exit 1
fi

echo "Requires: (gcc >= %{gcc_major} and gcc < %{gcc_next})"

%autosetup -p1

# The plugin has to be configured with the same arcane configure
# scripts used by gcc.  Hence we must not allow the Fedora build
# system to regenerate any of the configure files.
touch aclocal.m4 gcc-plugin/config.h.in
touch configure */configure Makefile.in */Makefile.in
# Similarly we do not want to rebuild the documentation.
touch doc/annobin.info

# Generate a source tarball for installation later with all the patches
# applied.  This must be the last step in the prep section.
tar -C ../ -cJf ../latest-annobin.tar.xz %{name}-%{version}

#---------------------------------------------------------------------------------

%build

CONFIG_ARGS="--quiet"

%if %{with debuginfod}
CONFIG_ARGS="$CONFIG_ARGS --with-debuginfod"
%else
# Note - we explicitly disable debuginfod support if it was not configured.
# This is because by default annobin's configue script will assume --with-debuginfod=auto
# and then run a build time test to see if debugingfod is available.  It
# may well be, but the build time environment may not match the run time
# environment, and the rpm will not have a Requirement on the debuginfod
# client.
CONFIG_ARGS="$CONFIG_ARGS --without-debuginfod"
%endif

%if %{without clangplugin}
CONFIG_ARGS="$CONFIG_ARGS --without-clang-plugin"
%endif

%if %{without gccplugin}
CONFIG_ARGS="$CONFIG_ARGS --without-gcc-plugin"
%else
CONFIG_ARGS="$CONFIG_ARGS --with-gcc-plugin-dir=%{ANNOBIN_GCC_PLUGIN_DIR}"
%endif

%if %{without llvmplugin}
CONFIG_ARGS="$CONFIG_ARGS --without-llvm-plugin"
%endif

%if %{without tests}
CONFIG_ARGS="$CONFIG_ARGS --without-tests"
%endif

%if %{without annocheck}
CONFIG_ARGS="$CONFIG_ARGS --without-annocheck"
%else
export CFLAGS="$CFLAGS -DAARCH64_BRANCH_PROTECTION_SUPPORTED=1"
%endif

%set_build_flags

export CFLAGS="$CFLAGS $RPM_OPT_FLAGS %build_cflags"
export LDFLAGS="$LDFLAGS %build_ldflags"

# Set target-specific options to be used when building the Clang and LLVM plugins.
# FIXME: There should be a better way to do this.
%ifarch %{ix86} x86_64
export CLANG_TARGET_OPTIONS="-fcf-protection"
%endif
%ifarch aarch64
export CLANG_TARGET_OPTIONS="-mbranch-protection=standard"
%endif
%ifnarch riscv64
export CLANG_TARGET_OPTIONS="$CLANG_TARGET_OPTIONS -flto"
%endif

# Override the default fortification level used by the Clang and LLVM plugins.
export PLUGIN_FORTIFY_OPTION="-D_FORTIFY_SOURCE=3"

CFLAGS="$CFLAGS" LDFLAGS="$LDFLAGS" CXXFLAGS="$CFLAGS" %configure ${CONFIG_ARGS} || cat config.log

%make_build

%if %{with plugin_rebuild}
# Rebuild the plugin(s), this time using the plugin itself!  This
# ensures that the plugin works, and that it contains annotations
# of its own.

%if %{with gccplugin}
cp gcc-plugin/.libs/annobin.so.0.0.0 %{_tmppath}/tmp_annobin.so
make -C gcc-plugin clean
BUILD_FLAGS="-fplugin=%{_tmppath}/tmp_annobin.so"

# Disable the standard annobin plugin so that we do get conflicts.
# Note - rpm-4.10 uses a different way of evaluating macros.
%if 0%{?rhel} && 0%{?rhel} < 7
OPTS="$(rpm --eval '%undefine _annotated_build %build_cflags %build_ldflags')"
%else
OPTS="$(rpm --undefine=_annotated_build --eval '%build_cflags %build_ldflags')"
%endif

# If building on systems with an assembler that does not support the
# .attach_to_group pseudo op (eg RHEL-7) then enable the next line.
# BUILD_FLAGS="$BUILD_FLAGS -fplugin-arg-tmp_annobin-no-attach"

make -C gcc-plugin CXXFLAGS="$OPTS $BUILD_FLAGS"
rm %{_tmppath}/tmp_annobin.so
%endif

%if %{with clangplugin}
cp clang-plugin/annobin-for-clang.so %{_tmppath}/tmp_annobin.so
# To enable verbose more in the plugin append the following: ANNOBIN="verbose"
make -C clang-plugin clean all CLANG_TARGET_OPTIONS="$CLANG_TARGET_OPTIONS $BUILD_FLAGS" PLUGIN_INSTALL_DIR=%{clang_plugin_dir}
%endif

%if %{with llvmplugin}
cp llvm-plugin/annobin-for-llvm.so %{_tmppath}/tmp_annobin.so
# To enable verbose more in the plugin append the following: ANNOBIN_VERBOSE="true"
make -C llvm-plugin clean all CLANG_TARGET_OPTIONS="$CLANG_TARGET_OPTIONS $BUILD_FLAGS" PLUGIN_INSTALL_DIR=%{llvm_plugin_dir}
%endif

# endif for %%if {with_plugin_rebuild}
%endif

#---------------------------------------------------------------------------------

%install

# PLUGIN_INSTALL_DIR is used by the Clang and LLVM makefiles...
%make_install PLUGIN_INSTALL_DIR=%{buildroot}/%{llvm_plugin_dir}

%if %{with clangplugin}
# Move the clang plugin to a seperate directory.
mkdir -p %{buildroot}/%{clang_plugin_dir}
mv %{buildroot}/%{llvm_plugin_dir}/annobin-for-clang.so %{buildroot}/%{clang_plugin_dir}
%endif

%if %{with gccplugin}
# Record the version of gcc that built this plugin.
# Note - we cannot just store %%{gcc_vr} as sometimes the gcc rpm version changes
# without the NVR being altered.  See BZ #2030671 for more discussion on this.
mkdir -p                             %{buildroot}/%{ANNOBIN_GCC_PLUGIN_DIR}
cat `gcc --print-file-name=rpmver` > %{buildroot}/%{ANNOBIN_GCC_PLUGIN_DIR}/%{aver}

# Also install a copy of the sources into the build tree.
mkdir -p                            %{buildroot}%{annobin_source_dir}
cp ../latest-annobin.tar.xz         %{buildroot}%{annobin_source_dir}/latest-annobin.tar.xz
%endif

rm -f %{buildroot}%{_infodir}/dir

# When annocheck is disabled, annocheck.1.gz will still be generated, remove it.
%if %{without annocheck}
rm -f %{_mandir}/man1/annocheck.1.gz
%endif

#---------------------------------------------------------------------------------

%if %{with tests}
%check
# The first "make check" is run with "|| :" so that we can capture any logs
# from failed tests.  The second "make check" is there so that the build
# will fail if any of the tests fail.
make check || :
if [ -f tests/test-suite.log ]; then
    cat tests/test-suite.log
fi
# If necessary use uuencode to preserve test binaries here.  For example:
#   uuencode tests/tmp_atexit/atexit.strip atexit.strip

make check
%endif

#---------------------------------------------------------------------------------

%files docs
%license COPYING3 LICENSE
%dir %{_datadir}/doc/annobin-plugin
%exclude %{_datadir}/doc/annobin-plugin/COPYING3
%exclude %{_datadir}/doc/annobin-plugin/LICENSE
%doc %{_datadir}/doc/annobin-plugin/annotation.proposal.txt
%{_infodir}/annobin.info*
%{_mandir}/man1/annobin.1*
%exclude %{_mandir}/man1/built-by.1*
%exclude %{_mandir}/man1/check-abi.1*
%exclude %{_mandir}/man1/hardened.1*
%exclude %{_mandir}/man1/run-on-binaries-in.1*

%if %{with llvmplugin}
%files plugin-llvm
%dir %{llvm_plugin_dir}
%{llvm_plugin_dir}/annobin-for-llvm.so
%endif

%if %{with clangplugin}
%files plugin-clang
%dir %{clang_plugin_dir}
%{clang_plugin_dir}/annobin-for-clang.so
%endif

%if %{with gccplugin}
%files plugin-gcc
%dir %{ANNOBIN_GCC_PLUGIN_DIR}
%{ANNOBIN_GCC_PLUGIN_DIR}/annobin.so
%{ANNOBIN_GCC_PLUGIN_DIR}/annobin.so.0
%{ANNOBIN_GCC_PLUGIN_DIR}/annobin.so.0.0.0
%{ANNOBIN_GCC_PLUGIN_DIR}/%{aver}
%dir %{annobin_source_dir}
%{annobin_source_dir}/latest-annobin.tar.xz
%endif

%if %{with annocheck}
%files annocheck
%{_bindir}/annocheck
%{_mandir}/man1/annocheck.1*

%files libannocheck
%{_includedir}/libannocheck.h
%{_libdir}/libannocheck.*
%{_libdir}/pkgconfig/libannocheck.pc
%endif

#---------------------------------------------------------------------------------

%changelog
* Wed Aug 06 2025 Nick Clifton  <nickc@redhat.com> - 12.99-1
- Annocheck: Improve detection of glibc static maths libraries.  (RHEL-107470)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 04 2025 Tulio Magno Quites Machado Filho  <tuliom@redhat.com> - 12.98-1
- Improve configure and meson files for consistent builds.

* Thu Jun 19 2025 Nick Clifton  <nickc@redhat.com> - 12.97-1
- Annocheck: Delete the temporary debug info directory after the tests have finished.

* Wed Jun 04 2025 Nick Clifton  <nickc@redhat.com> - 12.96-1
- Annocheck: Fix bugs in debug rpm location code.  Add more glibc exceptions.  (RHEL-95216)

* Thu May 15 2025 Nick Clifton  <nickc@redhat.com> - 12.95-1
- Annocheck: Improve performance with multiple debug info files and multiple files to scan.  (#2366180)

* Tue May 13 2025 Nick Clifton  <nickc@redhat.com> - 12.94-1
- Annocheck: Update heuristic for detecting gcc files to cope with gcc 15.  (#2365824)

* Mon Mar 17 2025 Nick Clifton  <nickc@redhat.com> - 12.93-1
- Annocheck: Fix test for GO revision.  (RHEL-56031)

* Fri Feb 14 2025 Nick Clifton  <nickc@redhat.com> - 12.92-1
- Annocheck: Do not rely upon libelf's ability to detect links to separate debuginfo files.  (RHEL-79264)

* Thu Feb 13 2025 Nick Clifton  <nickc@redhat.com> - 12.91-1
- Annocheck: Fix resource leak.  (RHEL-79253)

* Wed Feb 12 2025 Nick Clifton  <nickc@redhat.com> - 12.90-1
- Annocheck: Fix double free. Add special handling for COMBOOT modules.

* Tue Feb 11 2025 Nick Clifton  <nickc@redhat.com> - 12.89-1
- Annocheck: Improve diagnostics when a separate debug info file cannot be found.

* Mon Feb 03 2025 Nick Clifton  <nickc@redhat.com> - 12.88-1
- Annocheck: Look for -fstack-clash-protection in DW_AT_producer string.  (RHEL-77328)

* Tue Jan 28 2025 Nick Clifton  <nickc@redhat.com> - 12.87-1
- Annocheck: Fix locating string notes (again).  Add exception for glibc benchmark tests.  (RHEL-76456)

* Mon Jan 27 2025 Nick Clifton  <nickc@redhat.com> - 12.86-1
- Annocheck: Add crtoffloadtableS.o to list of known gcc binaries.  (RHEL-760404)

* Mon Jan 27 2025 Nick Clifton  <nickc@redhat.com> - 12.85-1
- Annocheck: Fix the --debug-dir option.

* Thu Jan 23 2025 Nick Clifton  <nickc@redhat.com> - 12.84-1
- Annocheck: Fix corrupt warning message when unable to locate separate debug info files.

* Wed Jan 22 2025 Nick Clifton  <nickc@redhat.com> - 12.83-1
- Annocheck: Remove spurious debugging messages.

* Wed Jan 22 2025 Nick Clifton  <nickc@redhat.com> - 12.82-1
- Annocheck: Always look for annobin notes in separate debug info files.  (RHEL-75778)

* Thu Jan 16 2025 Nick Clifton  <nickc@redhat.com> - 12.81-1
- Annocheck: Support multiple --debug-rpm and --debug-file options.  (RHEL-73349)

* Sat Jan 11 2025 Jakub Jelinek  <jakub@redhat.com> - 12.80-2
- NVR bump to allow rebuild for new GCC in a side-tag.

* Fri Dec 13 2024 Nick Clifton  <nickc@redhat.com> - 12.80-1
- Annocheck: Add support for sys-root'ed glibc packages.  (RHEL-71296)

* Tue Dec 10 2024 Nick Clifton  <nickc@redhat.com> - 12.79-1
- GCC Plugin: Tidy up use of gcc's diagnoatic headers.  (#32429)
- Testsuite: Use configured compiler when running tests.

* Mon Dec 09 2024 Nick Clifton  <nickc@redhat.com> - 12.78-1
- GCC Plugin: Fix building with gcc 15.  (#32429)

* Fri Nov 15 2024 Nick Clifton  <nickc@redhat.com> - 12.77-1
- Annocheck: Fix overly long debug messages.

* Fri Nov 15 2024 Nick Clifton  <nickc@redhat.com> - 12.76-1
- Annocheck: Rename rwx-seg test to load-segments.  Add more checks.  Add check for gaps as a future fail.
- Annocheck: Add --no-allow-excpetions to disable exceptions for known special binaries.
- Annocheck: Add --enable-future to enable future fail components in normal tests.
- Annocheck: Fix bug preventing the inclusion of the rpm name in reports.

* Tue Nov 12 2024 Nick Clifton  <nickc@redhat.com> - 12.75-1
- Annocheck: Add more exceptions for gcc binaries.  (RHEL-33365)
- Annocheck: Add --skip-passes option.

* Wed Nov 06 2024 Nick Clifton  <nickc@redhat.com> - 12.74-1
- Annocheck: Add exceptions for gcc binaries.  (RHEL-33365)

* Tue Nov 05 2024 Nick Clifton  <nickc@redhat.com> - 12.73-1
- Annocheck: Skip property note test for i386 binaries created by LLVM.  (#2323797)

* Fri Nov 01 2024 Nick Clifton  <nickc@redhat.com> - 12.72-1
- Annocheck: Skip FORTIFY and GLIBC_ASSERTIONS tests for LLVM produced binaries with unparseable DW_AT_producer attributes in their DWARF debug info.  (RHEL-65411)

* Mon Oct 14 2024 Nick Clifton  <nickc@redhat.com> - 12.71-1
- GCC Plugin: Change type of the .annobin.notes section from SHT_STRTAB to SHT_PROGBITS.

* Tue Aug 13 2024 Nick Clifton  <nickc@redhat.com> - 12.70-1
- Clang & LLVM Plugins: Include install directory in binary.  (RHEL-54069)

* Mon Aug 12 2024 Nick Clifton  <nickc@redhat.com> - 12.69-1
- BuiltBy: Fix seg-fault when comparing language version strings.  (RHEL-53497)

* Wed Aug 07 2024 Nick Clifton  <nickc@redhat.com> - 12.67-1
- Annocheck: Stop spurious assembler warnings.  (RHEL-53213)
- Annocheck: Stop warnings about known gaps.    (RHEL-53218)

* Fri Aug 02 2024 Nick Clifton  <nickc@redhat.com> - 12.66-1
- Annocheck: Fix stack realign test.  (#2302427)

* Mon Jul 29 2024 Nick Clifton  <nickc@redhat.com> - 12.65-1
- Annocheck: Fix recording arguments for later re-use.  (RHEL-50802)

* Fri Jul 26 2024 Nick Clifton  <nickc@redhat.com> - 12.64-1
- GCC Plugin: Fix building AArch64 components with gcc earlier than 11.3.

* Mon Jul 22 2024 Nick Clifton  <nickc@redhat.com> - 12.63-1
- Annocheck: Add improvements to the builtby utility.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.62-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Nick Clifton  <nickc@redhat.com> - 12.62-1
- Annocheck: Add support for ADA binaries.
- Annocheck: Add support for binaries built from more than two high level source languages.
- Annocheck: Add support for object files containing no executable code.
- Annocheck: Do not FAIL LLVM compiled binaries that have not been built with sanitize-cfi and/or sanitize-safe-stack.

* Wed Jun 26 2024 Nick Clifton  <nickc@redhat.com> - 12.60-1
- Annocheck: Add support for Fortran binaries.

* Tue Jun 11 2024 Nick Clifton  <nickc@redhat.com> - 12.59-1
- Annocheck: Add heuristic for detecting parts of the CGO runtime library.

* Mon Jun 10 2024 Nick Clifton  <nickc@redhat.com> - 12.58-1
- Annocheck: Add improvements for handling Clang runtime binaries.

* Tue Jun 04 2024 Nick Clifton  <nickc@redhat.com> - 12.57-1
- Annocheck: Add tweaks for mixed Rust/C binaries.  (#2284605)
- Annocheck: Add more glibc source file names.

* Mon May 20 2024 Nick Clifton  <nickc@redhat.com> - 12.55-1
- Annocheck: Skip GAPS test for GO binaries.  (RHEL-36308)

* Mon May 20 2024 Nick Clifton  <nickc@redhat.com> - 12.54-2
- Spec File: Add annobin plugin document directory to the files section.  (#2279779)

* Tue May 14 2024 Nick Clifton  <nickc@redhat.com> - 12.54-1
- Annocheck: Remove some false positives for Rust binaries.  (#2280239)

* Thu May 09 2024 Nick Clifton  <nickc@redhat.com> - 12.53-2
- Spec File: Add the annobin source directory to the files section.  (#2279779)

* Thu May 09 2024 Nick Clifton  <nickc@redhat.com> - 12.53-1
- Annocheck: Defer passing the branch protection test until all notes have been checked.
- GCC Plugin: Add extra code for detecting the branch protection setting.  (RHEL-35958)

* Thu Apr 25 2024 Nick Clifton  <nickc@redhat.com> - 12.52-1
- Annocheck: Add OpenSSL Engine test.  (PTG-319)

* Tue Apr 23 2024 Nick Clifton  <nickc@redhat.com> - 12.51-1
- Annocheck: Test for gaps even when only one note is present.

* Mon Apr 22 2024 Nick Clifton  <nickc@redhat.com> - 12.50-1
- Annocheck: Skip AArch64 branch protection test for GO binaries.

* Thu Apr 18 2024 Nick Clifton  <nickc@redhat.com> - 12.49-1
- GCC Plugin: Disable active check for -Wimplicit-int for non-C sources.  (#2275884)
- Annocheck: Ignore stack checks for AMD GPU binaries.
- Annocheck: Do not produce FAIL result for i686 binaries in the RHEL-10 profile.
- Annocheck: Test for __stack_chk_guard being writeable.

* Tue Apr 02 2024 Nick Clifton  <nickc@redhat.com> - 12.48-1
- Annocheck: Update heuristics for detecting glibc code in executables.  (RHEL-30579)

* Wed Mar 27 2024 Nick Clifton  <nickc@redhat.com> - 12.47-1
- Clang & LLVM Plugins: Allow environment to override fortification level.  (RHEL-30579)
- Spec File: Override fortification level and set it to 3.

* Mon Mar 25 2024 Tulio Magno Quites Machado Filho  <tuliom@redhat.com> - 12.46-1
- Annocheck: Improve detection of -mbranch-protection option.
- Clang Plugin: Add global-file-syms option.
- LLVM Plugin: Add global-file-syms option.
- Plugins: Add support for ANNOBIN environment variable.

* Thu Mar 21 2024 Nick Clifton  <nickc@redhat.com> - 12.45-1
- GCC Plugin: Fix bug extracing the value of target specific command line options.

* Wed Mar 06 2024 Nick Clifton  <nickc@redhat.com> - 12.44-1
- Configure: Remove check for FrontendPluginRegistry.h header as it is stored in a non-standard location on Debian systems.
- Debuginfod test: Allow for the libdwfl library silently contacting the debuginfod server.

* Tue Mar 05 2024 Nick Clifton  <nickc@redhat.com> - 12.43-1
- LLVM Plugin: Use llvm-config to get the correct paths and options for building executables.
- Clang Plugin: Likewise.
- Enable silent rules for most building.
- Annocheck: Correctly extract DWARF attributes from DT_REL files.

* Fri Mar 01 2024 Nick Clifton  <nickc@redhat.com> - 12.42-1
- Annocheck: Improve heuristics for locating debug info files.  (#2267097)
- Configure: Harmonize configure options.    

* Tue Feb 27 2024 Nick Clifton  <nickc@redhat.com> - 12.41-1
- Clang Plugin: Fix building with Clang 18.  (#31414)
- GCC Plugin: Add support for MIPS specific target functions.
- GCC Plugin: Use .dc.a for address expressions in 64-bit ELF format notes.

* Tue Feb 20 2024 Tulio Magno Quites Machado Filho  <tuliom@redhat.com> - 12.40-2
- Spec File: Remove a workaround for ppc64le.

* Tue Feb 13 2024 Nick Clifton  <nickc@redhat.com> - 12.40-1
- Annocheck: Improve heuristic for skipping LTO and FORTIFY tests.  (#2264000)

* Fri Feb 09 2024 Nick Clifton  <nickc@redhat.com> - 12.39-1
- Annocheck: Also skip property note test for i686 binaries. (#2258571)

* Tue Jan 23 2024 Nick Clifton  <nickc@redhat.com> - 12.38-1
- Annocheck: Also skip the entry point test for i686 binaries. (#2258571)

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.37-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.37-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 17 2024 Nick Clifton  <nickc@redhat.com> - 12.37-1
- GCC Plugin: Do not use section groups with string format notes.

* Tue Jan 16 2024 Nick Clifton  <nickc@redhat.com> - 12.36-2
- Spec File: NVR bump in order to allow building in side tag.

* Tue Jan 16 2024 Nick Clifton  <nickc@redhat.com> - 12.36-1
- Annocheck: Disable cf-protection test for i686 architecture. (#2258571)

* Mon Jan 15 2024 Nick Clifton  <nickc@redhat.com> - 12.35-4
- Spec File: NVR bump in order to allow building in side tag.

* Mon Jan 15 2024 Nick Clifton  <nickc@redhat.com> - 12.35-3
- Spec File: Disable hard gcc check in order to allow builds with new version of gcc.

* Thu Jan 11 2024 Songsong Zhang  <U2FsdGVkX1@gmail.com> - 12.35-2
- Spec File: Do not install annocheck.1.gz when annocheck is disabled.

* Thu Jan 04 2024 Nick Clifton  <nickc@redhat.com> - 12.35-1
- Annocheck: Improve detection of FIPS compliant GO binaries.

* Fri Dec 15 2023 Nick Clifton  <nickc@redhat.com> - 12.34-1
- GCC Plugin: Fix recording of the -Wimplicit-int and -Wimplicit-function-declaration warnings.  Add active checks for when they are deliberately disabled.

* Mon Dec 11 2023 Nick Clifton  <nickc@redhat.com> - 12.33-1
- Tests: Fix implicit-values test so that it will compile with gcc 14+.

* Fri Nov 24 2023 Nick Clifton  <nickc@redhat.com> - 12.32-1
- GCC Plugin: Add support for -fhardended.

* Wed Nov 15 2023 Nick Clifton  <nickc@redhat.com> - 12.31-1
- Update glibc detection heuristics for PPC64.  (RHEL-16453)

* Wed Nov 01 2023 Nick Clifton  <nickc@redhat.com> - 12.30-1
- Fix another atexit test failure.  (#2247481)

* Mon Oct 30 2023 Nick Clifton  <nickc@redhat.com> - 12.29-1
- Fix atexit test failure.
- Notes: Add support for string format notes.

* Fri Oct 06 2023 Nick Clifton  <nickc@redhat.com> - 12.28-1
- GCC Plugin: Record settings of -Wstrict-flex-arrays and -fstrict-flex-arrays
- Annobin: Add future test of these options.

* Tue Sep 26 2023 Nick Clifton  <nickc@redhat.com> - 12.27-1
- GCC Plugin: Record settings of -Wimplicit-int and -Wimplicit-function-declaration.
- Annobin: Add test for these warnings.

* Wed Sep 06 2023 Nick Clifton  <nickc@redhat.com> - 12.26-1
- LLVM Plugin: Fix building with LLVM version 17.

* Wed Aug 30 2023 Nick Clifton  <nickc@redhat.com> - 12.25-1
- GCC Plugin: Enable string note format by default.

* Fri Aug 04 2023 Nick Clifton  <nickc@redhat.com> - 12.24-1
- Annocheck: Change GO FIPS test to look for CGO_ENABLED markers.

* Mon Jul 31 2023 Nick Clifton  <nickc@redhat.com> - 12.23-1
- Annocheck: Add test for FIPS compliant GO binaries.

* Wed Jul 26 2023 Nick Clifton  <nickc@redhat.com> - 12.22-1
- Annocheck: Fix double free.  (#2226749)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 12.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Nick Clifton  <nickc@redhat.com> - 12.21-1
- Spec File: migrated to SPDX license.  (#2222112)

* Mon Jul 17 2023 Nick Clifton  <nickc@redhat.com> - 12.20-2
- Spec File: Change License field to use SPDX notation.  (#2222112)

* Mon Jul 17 2023 Nick Clifton  <nickc@redhat.com> - 12.20-1
- Annocheck: Ignore AArch64 $x and $d symbols.  (#2221192)

* Wed Jul 05 2023 Nick Clifton  <nickc@redhat.com> - 12.19-1
- GCC Plugin: Suppress active checks for fortran sources.  Improve scanning of COLLECT_GCC_OPTIONS.

* Thu Jun 29 2023 Nick Clifton  <nickc@redhat.com> - 12.18-1
- Annocheck: Remove dependency upon binutils-devel.

* Thu Jun 29 2023 Nick Clifton  <nickc@redhat.com> - 12.17-1
- Annocheck: Add detection of known parts of libstdc++-nonshared.a that contain gaps.  (#2217864)

* Tue Jun 27 2023 Nick Clifton  <nickc@redhat.com> - 12.16-1
- Annocheck: Ignore weak/undef function symbols when checking to see if a binary contains code.  (#2217840)

* Mon Jun 26 2023 Nick Clifton  <nickc@redhat.com> - 12.15-1
- Annocheck: Add --suppress-version-warnings option.

* Thu Jun 22 2023 Nick Clifton  <nickc@redhat.com> - 12.14-1
- Annocheck: Do not ignore separate debuginfo files that do not contain any DWARF.  (#2144553)

* Tue Jun 20 2023 Nick Clifton  <nickc@redhat.com> - 12.13-1
- Annocheck: Ignore /dev/null filename in string notes.
- Annocheck: More tweaks to glibc detection heuristics.  (#2215968)

* Thu Jun 01 2023 Nick Clifton  <nickc@redhat.com> - 12.12-1
- Annocheck: Check for string notes in separate debug info files.  (#2211694)

* Fri May 26 2023 Petr Pisar <ppisar@redhat.com> - 12.11-1
- Annocheck: Add support for el10 and rhel-10 profiles.  (RHEL-526)

* Mon May 22 2023 Petr Pisar <ppisar@redhat.com> - 12.10-3
- Rebuild against rpm-4.19 (https://fedoraproject.org/wiki/Changes/RPM-4.19)

* Fri May 05 2023 Nick Clifton  <nickc@redhat.com> - 12.10-2
- GCC Plugin: Default to generating string format notes.  (Experimental)

* Fri Apr 28 2023 Nick Clifton  <nickc@redhat.com> - 12.10-1
- Annocheck: Suppress more tests for Rust binaries.

* Tue Apr 25 2023 Nick Clifton  <nickc@redhat.com> - 12.09-1
- Annocheck: Fix detection of missing plugin options.  (#2189492)

* Tue Apr 25 2023 Nick Clifton  <nickc@redhat.com> - 12.08-1
- Fix generation of auto-generated files.
- Fix covscan reported errors.

* Fri Apr 21 2023 Nick Clifton  <nickc@redhat.com> - 12.07-1
- gcc-plugin: generate warnings about misspelt -D_FORTIFY_SOURCE and/or -D_GLIBCXX_ASSERTIONS options.

* Thu Apr 20 2023 Nick Clifton  <nickc@redhat.com> - 12.06-1
- gcc-plugin: use a bigger buffer for constructing notes.

* Wed Apr 19 2023 Nick Clifton  <nickc@redhat.com> - 12.05-1
- llvm-plugin: Fix detection of optimization level.  Improve test.
- clang-plugin: Improve test.

* Mon Apr 17 2023 Nick Clifton  <nickc@redhat.com> - 12.04-1
- configure: More improvements.
- annocheck: Fix seg-fault when checking for glibc components in string format notes.

* Thu Apr 13 2023 Nick Clifton  <nickc@redhat.com> - 12.03-1
- configure: Simplify.

* Tue Apr 11 2023 Nick Clifton  <nickc@redhat.com> - 12.02-1
- gcc plugin: Add filenames to string notes.  Allow use of ANNOBIN environment variable.
- llvm plugin: Add workaround for building with LLVM-16.
- clang plugin: Fix for building with Clang-16.

* Thu Mar 30 2023 Nick Clifton  <nickc@redhat.com> - 12.01-1
- gcc plugin: Keep ELF notes at protocol version 3.

* Tue Mar 28 2023 Nick Clifton  <nickc@redhat.com> - 12.00-1
- Protocol Version 4: String format notes.

* Mon Mar 13 2023 Nick Clifton  <nickc@redhat.com> - 11.14-1
- Annocheck: Update message for LTO tests.  (#2177140)

* Wed Mar 08 2023 Nick Clifton  <nickc@redhat.com> - 11.13-1
- Annocheck: Add even more code to handle another glibc function built without LTO.

* Fri Mar 03 2023 Nick Clifton  <nickc@redhat.com> - 11.12-1
- Annocheck: Add code to handle another glibc function built without LTO.

* Tue Feb 28 2023 Nick Clifton  <nickc@redhat.com> - 11.11-1
- GCC Plugin: Do not run if other plugins are active.  (#2162746)

* Thu Feb 23 2023 Nick Clifton  <nickc@redhat.com> - 11.10-1
- Annocheck: Add code to handle glibc functions built without LTO.

* Thu Feb 02 2023 Nick Clifton  <nickc@redhat.com> - 11.09-1
- Libannocheck: Fix thinko in debugging code.
- Annocheck: Fix LTO test.
- Notes: Display notes held in separate dbeuginfo files.

* Tue Jan 31 2023 Nick Clifton  <nickc@redhat.com> - 11.08-1
- Annocheck: Fix atexit test.  Fix recording of version numbers.  (#2165528)

* Wed Jan 25 2023 Nick Clifton  <nickc@redhat.com> - 11.07-2
- LLVM & Clang Plugins: Build with branch protection on AArch64.  (#2164364)
- Fix gating tests.

* Fri Jan 20 2023 Nick Clifton  <nickc@redhat.com> - 11.07-1
- Libannocheck: Fix bug causing infinite looping when running tests.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.06-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Jakub Jelinek  <jakub@redhat.com> - 11.06-2
- Rebuilt against GCC 13.

* Fri Jan 13 2023 Nick Clifton  <nickc@redhat.com> - 11.06-1
- Annocheck: Fix handling of file built by multiple versions of gcc.  (#2160700)

* Mon Jan 09 2023 Nick Clifton  <nickc@redhat.com> - 11.05-1
- Annocheck: Fix handling of empty files.  (#2159292)

* Fri Jan 06 2023 Nick Clifton  <nickc@redhat.com> - 11.04-1
- Annocheck: Add crti.o and crtn.o to the list of known glibc special files.  (#2158740)

* Fri Jan 06 2023 Nick Clifton  <nickc@redhat.com> - 11.03-1
- Annocheck: Fix memory leaks.

* Wed Jan 04 2023 Nick Clifton  <nickc@redhat.com> - 11.02-1
- Annocheck: Do not assume that object files contain no code simply because they do not have an executable segment.  (#2158182)

* Wed Jan 04 2023 Nick Clifton  <nickc@redhat.com> - 11.01-1
- Annocheck: Add more special glibc filenames.  (#2158100)

* Wed Dec 21 2022 Nick Clifton  <nickc@redhat.com> - 10.99-1
- Annocheck: Improve handling of tool versions.

* Tue Dec 20 2022 Nick Clifton  <nickc@redhat.com> - 10.98-3
- Spec File: Fix building with plugin_rebuild enabled.

* Fri Dec 16 2022 Nick Clifton  <nickc@redhat.com> - 10.98-1
- GCC plugin: Fix building with gcc-13.

* Fri Dec 16 2022 Nick Clifton  <nickc@redhat.com> - 10.97-1
- Annocheck: Add test for binaries built by cross compilers.

* Thu Dec 15 2022 Nick Clifton  <nickc@redhat.com> - 10.96-1
- Annocheck: Improve heuristic used to detect binaries without code. (#2144533)

* Mon Dec 12 2022 Nick Clifton  <nickc@redhat.com> - 10.95-1
- Annocheck: Avoid using debug filename when parsing notes in a debuginfo file.  (#2152280)

* Wed Nov 30 2022 Nick Clifton  <nickc@redhat.com> - 10.94-1
- Annocheck: Better detection of binaries which do not contain code.  (#2144533)

* Wed Nov 23 2022 Nick Clifton  <nickc@redhat.com> - 10.93-1
- Annocheck: Provide more information when a test is skipped because the file being tested was not compiled.

* Mon Nov 07 2022 Nick Clifton  <nickc@redhat.com> - 10.92-1
- Annocheck: Try harder not to run mutually exclusive tests.

* Fri Oct 21 2022 Nick Clifton  <nickc@redhat.com> - 10.91-1
- Tests: Fix future-test so that it properly handles the situation where the compiler does not support the new options.

* Wed Oct 19 2022 Nick Clifton  <nickc@redhat.com> - 10.90-1
- Libannocheck: Actually set result fields after tests are run.

* Tue Oct 11 2022 Nick Clifton  <nickc@redhat.com> - 10.89-1
- Libannocheck: Replace libannocheck_version variable with LIBANNOCHECK_VERSION define.

* Tue Oct 11 2022 Nick Clifton  <nickc@redhat.com> - 10.88-1
- Libannocheck: Remove 'Requires binutils-devel' from libannocheck.pc.

* Wed Oct 05 2022 Nick Clifton  <nickc@redhat.com> - 10.87-2
- Libannocheck: Move into separate sub-package.

* Fri Sep 30 2022 Nick Clifton  <nickc@redhat.com> - 10.87-1
- Libannocheck: Add libannocheck.pc pkgconfig file.

* Fri Sep 30 2022 Nick Clifton  <nickc@redhat.com> - 10.86-1
- Libannocheck: Add libannocheck_reinit().

* Thu Sep 22 2022 Nick Clifton  <nickc@redhat.com> - 10.85-1
- GCC Plugin: Record -ftrivial-auto-var-init and -fzero-call-used-regs.
- Annocheck: Add future tests for  -ftrivial-auto-var-init and -fzero-call-used-regs.

* Tue Sep 20 2022 Serge Guelton  <sguelton@redhat.com> - 10.84-1
- Clang Plugin: Fix for building with Clang-15.  (#2125875)

* Fri Sep 09 2022 Nick Clifton  <nickc@redhat.com> - 10.83-1
- Annocheck: Add a test for the inconsistent use of -Ofast.  (#1248744)

* Tue Sep 06 2022 Nick Clifton  <nickc@redhat.com> - 10.81-2
- NVR Bump in order to trigger a rebuild for ELN.  (#2124562)

* Thu Aug 11 2022 Nick Clifton  <nickc@redhat.com> - 10.81-1
- Plugin: Fix top level configuration support for RiscV.

* Tue Aug 09 2022 Nick Clifton  <nickc@redhat.com> - 10.80-1
- Annocheck: Improvements to the size tool.

* Mon Jul 25 2022 Nick Clifton  <nickc@redhat.com> - 10.79-1
- Annocheck: Fixes for libannocheck.h.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 05 2022 Nick Clifton  <nickc@redhat.com> - 10.78-1
- Annocheck: Add automatic profile selection.

* Mon Jul 04 2022 Nick Clifton  <nickc@redhat.com> - 10.77-1
- Annocheck: Improve gap detection and reporting.

* Wed Jun 29 2022 Nick Clifton  <nickc@redhat.com> - 10.76-3
- Spec File: Use the %%dir directive in the %%files section to ensure that
-  plugin directories are useable.  (#2080454)

* Fri Jun 24 2022 Nick Clifton  <nickc@redhat.com> - 10.76-2
- Spec File: Remove bogus Provides from annobin-docs subpackage.

* Tue Jun 14 2022 Nick Clifton  <nickc@redhat.com> - 10.76-1
- Annocheck: Check build-id of separate debuginfo files.
- Annocheck: Add GAPS test replacing --ignore-gaps.

* Thu Jun 09 2022 Nick Clifton  <nickc@redhat.com> - 10.75-1
- Annocheck: Fix covscan detected race condition between stat() and open().

* Tue Jun 07 2022 Nick Clifton  <nickc@redhat.com> - 10.74-1
- Annocheck: Handle binaries created by Rust 1.18.  (#2094420)
- Annocheck: Add optional function name to --skip arguments.  (PR 29229)

* Tue May 17 2022 Nick Clifton  <nickc@redhat.com> - 10.73-1
- Annocheck: Fix handling of command line options that take arguments.  (#2086850)

* Mon May 16 2022 Nick Clifton  <nickc@redhat.com> - 10.72-1
- Annocheck: Do not complain about unenabled -mbranch-protection option in AArch64 binaries.  (#2078909)

* Wed May 11 2022 Nick Clifton  <nickc@redhat.com> - 10.71-1
- gcc-plugin: Fix typo in configure.ac.

* Tue May 10 2022 Nianqing Yao <imbearchild@outlook.com> - 10.70-2
- Add support for RISC-V.

* Mon May 09 2022 Nick Clifton  <nickc@redhat.com> - 10.70-1
- Annocheck: Add another special case for glibc rpms.  (#2083070)

* Fri May 06 2022 Nick Clifton  <nickc@redhat.com> - 10.69-1
- Annocheck: Do not complain about unenabled -mbranch-protection option in AArch64 binaries if compiled using LTO.  (#2082146)

* Tue May 03 2022 Nick Clifton  <nickc@redhat.com> - 10.68-1
- Annocheck: Add more glibc exceptions + check PT_TLS segments.  (#2081131)

* Fri Apr 22 2022 Nick Clifton  <nickc@redhat.com> - 10.67-1
- Annocheck: Do not complain about missing -mbranch-protection option in AArch64 binaries if compiled by golang.

* Wed Apr 13 2022 Nick Clifton  <nickc@redhat.com> - 10.66-1
- Annocheck: Do not complain about missing -mbranch-protection option in AArch64 binaries if compiled in LTO mode.

* Tue Apr 12 2022 Nick Clifton  <nickc@redhat.com> - 10.65-1
- gcc-plugin: Add support for CLVC_INTEGER options.

* Wed Apr 06 2022 Nick Clifton  <nickc@redhat.com> - 10.64-1
- Annocheck: Even more special cases for AArch64 glibc on RHEL-8.  (#2072082)

* Wed Apr 06 2022 Nick Clifton  <nickc@redhat.com> - 10.63-1
- Annocheck: Add more special cases for AArch64 glibc on RHEL-8.  (#2072082)

* Tue Apr 05 2022 Nick Clifton  <nickc@redhat.com> - 10.62-1
- llvm-plugin: Fix a thinko in the sources.

* Sat Apr 02 2022 Nick Clifton  <nickc@redhat.com> - 10.61-1
- gcc-plugin: Add remap of OPT_Wall.
- configure: Fix typo in top level configure.ac.

* Thu Mar 31 2022 Timm Bäder <mail@baedert.org>redhat.com> - 10.60-1
- Add support for building using meson+ninja.

* Wed Mar 30 2022 Serge Guelton  <sguelton@redhat.com> - 10.59-2  
- Rebuilt against new LLVM release, with patch.

* Wed Mar 30 2022 Nick Clifton  <nickc@redhat.com> - 10.59-1
- Annocheck: Fix test for AArch64 property notes.  (#2068657)

* Mon Mar 14 2022 Nick Clifton  <nickc@redhat.com> - 10.58-1
- gcc-plugin: Do not issue warning messages for autoconf generated source files.  (#2009958)

* Wed Mar 09 2022 Jakub Jelinek  <jakub@redhat.com> - 10.57-3
- NVR bump to allow rebuild for new GCC.

* Wed Mar 09 2022 Jakub Jelinek  <jakub@redhat.com> - 10.57-2
- NVR bump to allow rebuild for new GCC.

* Mon Mar 07 2022 Nick Clifton  <nickc@redhat.com> - 10.57-1
- Annocheck: Update documentation and fix typo in annocheck.  (#2061291)

* Fri Mar 04 2022 Nick Clifton  <nickc@redhat.com> - 10.56-1
- Annocheck: Add option to enable/disable following symbolic links.

* Mon Feb 28 2022 Nick Clifton  <nickc@redhat.com> - 10.55-1
- Always identify Rust binaries, even if built on a host that does not know about Rust.  (#2057737)

* Thu Feb 24 2022 Jakub Jelinek  <jakub@redhat.com> - 10.54-4
- NVR bump to allow rebuild for new GCC.

* Wed Feb 16 2022 Nick Clifton  <nickc@redhat.com> - 10.54-3
- Spec File: Use a different method to disable the annobin plugin  (#2054571)

* Mon Feb 14 2022 Jakub Jelinek  <jakub@redhat.com> - 10.54-2
- NVR bump to allow rebuild for new GCC.

* Fri Feb 11 2022 Nick Clifton  <nickc@redhat.com> - 10.54-1
- Annocheck: Skip PIE anf PIC tests for GO binaries.

* Sun Feb 06 2022 Jakub Jelinek  <jakub@redhat.com> - 10.53-2
- NVR bump to allow rebuild in yet another side tag.

* Thu Jan 27 2022 Nick Clifton  <nickc@redhat.com> - 10.53-1
- gcc-plugin: Fix libtool so that extraneous runpaths are not added to the plugin.  (#2030667)

* Thu Jan 27 2022 Nick Clifton  <nickc@redhat.com> - 10.52-1
- gcc-plugin: Use canonical_option field of save_decoded_options array. (#2047148)

* Thu Jan 27 2022 Florian Weimer <fweimer@redhat.com> - 10.51-2
- Rebuild for new gcc version

* Tue Jan 25 2022 Nick Clifton  <nickc@redhat.com> - 10.51-1
- Annocheck: Add an option to disable the use of debuginfod (if available).
- Annocheck: Add more glibc special file names.
- Annocheck: Skip some tests for BPF binaries.

* Thu Jan 20 2022 Nick Clifton  <nickc@redhat.com> - 10.50-1
- Annocheck: Add another glibc static library symbol.  (#2043047)

* Thu Jan 20 2022 Nick Clifton  <nickc@redhat.com> - 10.49-1
- Annocheck: Skip property note test for GO binaries.  (#204300)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.48-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Nick Clifton  <nickc@redhat.com> - 10.48-5
- NVR bump to allow rebuild in another side tag.

* Wed Jan 19 2022 Jakub Jelinek  <jakub@redhat.com> - 10.48-4
- NVR bump to allow rebuild in yet another side tag.

* Wed Jan 19 2022 Nick Clifton  <nickc@redhat.com> - 10.48-3
- NVR bump to allow rebuild in another side tag.

* Wed Jan 19 2022 Nick Clifton  <nickc@redhat.com> - 10.48-2
- NVR bump to allow rebuild in a side tag.

* Mon Jan 17 2022 Nick Clifton  <nickc@redhat.com> - 10.48-1
- GCC Plugin: Do not fail if a section cannot be attached to a group.

* Fri Jan 14 2022 Nick Clifton  <nickc@redhat.com> - 10.47-2
- NVR bump to allow rebuild in a side tag.

* Fri Jan 14 2022 Nick Clifton  <nickc@redhat.com> - 10.47-1
- Annocheck: Improve detection of kernel modules.
- GCC Plugin: Only default to link-once when using gcc-12 or later.  (#2039297)

* Tue Jan 11 2022 Nick Clifton  <nickc@redhat.com> - 10.46-1
- Annocheck: Add option to disable instrumentation test.

* Mon Jan 10 2022 Nick Clifton  <nickc@redhat.com> - 10.45-1
- GCC Plugin: Replace CLVC_BOOLEAN with CLVC_BIT_SET/CLVC_BIT_CLEAR.

* Sun Jan 09 2022 Jakub Jelinek  <jakub@redhat.com> - 10.44-4
- Rebuild against new GCC.

* Sun Jan 09 2022 Jakub Jelinek  <jakub@redhat.com> - 10.44-3
- Rebuild against new GCC.

* Sun Jan 09 2022 Jakub Jelinek  <jakub@redhat.com> - 10.44-2
- Rebuild against new GCC.

* Fri Jan 07 2022 Nick Clifton  <nickc@redhat.com> - 10.44-1
- Annocheck: Add even more glibc function names. (#2037333)

* Fri Jan 07 2022 Nick Clifton  <nickc@redhat.com> - 10.43-1
- Annocheck: ARM: Do not fail tests that rely upon annobin notes.

* Wed Jan 05 2022 Nick Clifton  <nickc@redhat.com> - 10.42-1
- Annocheck: Extend list of known glibc functions.  (#2037333)

* Wed Jan 05 2022 Nick Clifton  <nickc@redhat.com> - 10.41-1
- Annocheck: Ignore gaps that contain the _start symbol (for AArch64).  (#1995224)
- Annocheck: Ignore more glibc special binaries.  (#2037220)

* Tue Jan 04 2022 Nick Clifton  <nickc@redhat.com> - 10.40-1
- Annocheck: Do not complaining about missing stack clash notes if the compilation used LTO.  (#2034946)

* Fri Dec 17 2021 Nick Clifton  <nickc@redhat.com> - 10.39-1
- Annocheck: Add /usr/lib/ld-linux-aarch64.so.1 to the list of known glibc binaries.  (#2033255)
- Doc: Note that ENDBR is only needed as the landing pad for indirect branches/calls.  (#28705)
- Spec File: Store full gcc version release string in plugin info file.  (#2030671)

* Tue Dec 14 2021 Nick Clifton  <nickc@redhat.com> - 10.38-1
- Annocheck: Add special case for x86_64 RHEL-7 gaps.  (#2031133)

* Tue Dec 14 2021 Nick Clifton  <nickc@redhat.com> - 10.37-1
- Annocheck: Do not complaining about missing -mstackrealign notes in LTO mode.  (#2030298)

* Mon Dec 13 2021 Nick Clifton  <nickc@redhat.com> - 10.36-1
- GCC Plugin: Do not record missing -mstackrealign in LTO mode.  (#2030298)

* Mon Dec 13 2021 Nick Clifton  <nickc@redhat.com> - 10.35-1
- Tests: Fix fortify and debuginfod tests to use newly built annobin plugin.

* Mon Dec 06 2021 Nick Clifton  <nickc@redhat.com> - 10.34-1
- Tests: Fix gaps and stat tests to use newly built annobin plugin.  (#2028063)

* Mon Dec 06 2021 Nick Clifton  <nickc@redhat.com> - 10.32-1
- Annocheck: Ignore gaps in binaries at least partial built by golang.  (#2028583)

* Thu Dec 02 2021 Nick Clifton  <nickc@redhat.com> - 10.31-1
- Annocheck: Allow spaces in golang symbols.

* Wed Dec 01 2021 Nick Clifton  <nickc@redhat.com> - 10.30-1
- Annocheck: Initial deployment of libannocheck.

* Wed Nov 24 2021 Nick Clifton  <nickc@redhat.com> - 10.29-1
- gcc-plugin: Fix bug creating empty attachments.
- Annocheck: Change MAYB result to SKIP for DT_RPATH.  (#2026300)

* Fri Nov 19 2021 Nick Clifton  <nickc@redhat.com> - 10.27-1
- Annocheck: Skip missing fortify/warning notes for ARM32.

* Thu Nov 18 2021 Nick Clifton  <nickc@redhat.com> - 10.26-1
- gcc-plugin: Try another fix for ppc64le section grouping.  (#2023437)

* Tue Nov 16 2021 Nick Clifton  <nickc@redhat.com> - 10.25-1
- gcc-plugin: Revert 10.22 change.  (#2023437)

* Mon Nov 15 2021 Nick Clifton  <nickc@redhat.com> - 10.24-1
- Annocheck: Add exception for /usr/sbin/ldconfig.  (#2022973)

* Mon Nov 08 2021 Nick Clifton  <nickc@redhat.com> - 10.23-1
- Annocheck: Add a test for unicode characters in identifiers.

* Wed Oct 27 2021 Nick Clifton  <nickc@redhat.com> - 10.22-1
- gcc-plugin: Default to link-order grouping for PPC64LE.  (#2016458)

* Tue Oct 26 2021 Nick Clifton  <nickc@redhat.com> - 10.21-1
- Annocheck: Do not fail if a --skip-<name> option does not match a known test.
- ldconfig-test: Skip the LTO check.

* Tue Oct 26 2021 Nick Clifton  <nickc@redhat.com> - 10.20-1
- Annocheck: Add more glibc function names.

* Thu Oct 21 2021 Nick Clifton  <nickc@redhat.com> - 10.19-1
- gcc-plugin: Fix attaching the .text section to the .text.group section.

* Wed Oct 20 2021 Nick Clifton  <nickc@redhat.com> - 10.18-1
- Complain about DT_RPATH for Fedora binaries.

* Mon Oct 18 2021 Nick Clifton  <nickc@redhat.com> - 10.17-1
- Better reporting of problems in object files.  (#2013708)

* Mon Oct 18 2021 Nick Clifton  <nickc@redhat.com> - 10.16-2
- Add a requirement on llvm-libs for clang and llvm plugins.  (#2014573)

* Thu Oct 14 2021 Nick Clifton  <nickc@redhat.com> - 10.16-1
- Fix configuring annocheck without gcc-plugin.
- Annocheck: Better reporting of debuginfod problems.
- Tests: Fix bugs in debuginfod test.

* Wed Oct 13 2021 Nick Clifton  <nickc@redhat.com> - 10.15-1
- Annocheck: Add tests based upon recent bug fixes.

* Tue Oct 12 2021 Nick Clifton  <nickc@redhat.com> - 10.14-1
- Annocheck: Another tweak to glibc detection code.

* Tue Oct 12 2021 Tom Stellard <tstellar@redhat.com> - 10.13-2
- Rebuild for llvm-13.0.0

* Fri Oct 08 2021 Nick Clifton  <nickc@redhat.com> - 10.13-1
- Annocheck: Fix memory corruptions when using --debug-path and when a corrupt note is found.  (#20011438)

* Fri Oct 08 2021 Nick Clifton  <nickc@redhat.com> - 10.12-1
- Annocheck: Fix MAYB results for mixed GO/C files.
- Annocheck: Move some messages from VERBOSE to VERBOSE2.
- Annocheck: Scan zero-length tool notes.

* Tue Oct 05 2021 Nick Clifton  <nickc@redhat.com> - 10.11-1
- Annocheck: Fix covscan detected flaws.
- plugins: Add more required build options.

* Tue Oct 05 2021 Nick Clifton  <nickc@redhat.com> - 10.10-1
- Annocheck: Fix cf-prot test to fail if the CET notes are missing.
- Annocheck: Skip gaps in the .plt section.
- Plugins: Add -g option when building LLVM and Clang.

* Mon Oct 04 2021 Nick Clifton  <nickc@redhat.com> - 10.09-1
- Annocheck: Add more cases of glibc startup functions.

* Fri Oct 01 2021 Nick Clifton  <nickc@redhat.com> - 10.08-1
- Annocheck: Fix covscan detected problems.
- Annocheck: Add --profile=el8.
- gcc-plugin: Conditionalize generation of branch protection note.

* Wed Sep 29 2021 Nick Clifton  <nickc@redhat.com> - 10.07-1
- Annocheck: Ignore gaps containing NOP instructions.

* Thu Sep 16 2021 Nick Clifton  <nickc@redhat.com> - 10.06-1
- GCC Plugin: Fix detection of running inside the LTO compiler.  (#2004917)

* Wed Sep 15 2021 Nick Clifton  <nickc@redhat.com> - 10.05-1
- Annocheck: Do not insist on the DT_AARCH64_PAC_PLT flag being present in AArch64 binaries.

* Wed Sep 15 2021 Nick Clifton  <nickc@redhat.com> - 10.04-1
- Annocheck: With gaps at the start/end of the .text section, check for special symbols before displaying a MAYB result.

* Wed Sep 15 2021 Nick Clifton  <nickc@redhat.com> - 10.03-1
- Annocheck: Do not set CFLAGS/LDFLAGS when building.  Take from environment instead.

* Fri Sep 10 2021 Nick Clifton  <nickc@redhat.com> - 10.02-1
- Annocheck: Fix exit code when tests PASS.

* Thu Sep 09 2021 Nick Clifton  <nickc@redhat.com> - 10.01-1
- Documentation: Add node for each hardening test.
- Documentation: Install online.
- Annocheck: Annote FAIL and MAYB results with URL to documentation
- Annocheck: Add --no-urls and --provide-urls options
- Annocheck: Add --help-<tool> option.

* Fri Sep 03 2021 Nick Clifton  <nickc@redhat.com> - 9.95-1
- Annocheck: Fix fuzzing detected failures.
- Annocheck: Add --profile option.
- Docs: Document --profile option and rpminspect.yaml.

* Tue Aug 31 2021 Nick Clifton  <nickc@redhat.com> - 9.94-1
- Annocheck: Skip GO/CET checks.  Fix fuzzing detected failures.

* Wed Aug 25 2021 Nick Clifton  <nickc@redhat.com> - 9.93-1
- LLVM Plugin: Automatically choose the correct tests to run, based upon the version of Clang installed. (#1997444)
- spec file: Add the installation of the annobon sources into /usr/src/annobin.

* Tue Aug 24 2021 Nick Clifton  <nickc@redhat.com> - 9.92-1
- Annocheck: Fix memory corruption.  (#1996963)
- spec file: Add the creation of a gcc-plugin version info file in /usr/lib/rpm/redhat.

* Wed Aug 18 2021 Nick Clifton  <nickc@redhat.com> - 9.91-1
- Annocheck: Fix conditionalization of AArch64's PAC+BTI detection.

* Wed Aug 18 2021 Nick Clifton  <nickc@redhat.com> - 9.90-1
- Annocheck: Add linker generated function for ppc64le exceptions.  (#1981410)
- LLVM Plugin: Allow checks to be selected from the command line.
- Annocheck: Examine DW_AT_producer for -flto.    

* Tue Aug 17 2021 Nick Clifton  <nickc@redhat.com> - 9.89-1
- Annocheck: Conditionalize detection of AArch64's PAC+BTI protection.
- Annocheck: Add linker generated function for s390x exceptions.  (#1981410)

* Tue Aug 17 2021 Nick Clifton  <nickc@redhat.com> - 9.88-1
- Annocheck: Generate MAYB results for gaps in notes covering the .text section.  (#1991943)
- Annocheck: Close DWARF file descriptors once the debug info is no longer needed.  (#1981410)
- LLVM Plugin: Update to build with Clang v13.  (Thanks to: Tom Stellard <tstellar@redhat.com>)
    
* Mon Aug 16 2021 Tom Stellard <tstellar@redhat.com> - 9.87-2
- Rebuild for LLVM 13.0.0-rc1

* Mon Aug 16 2021 Nick Clifton  <nickc@redhat.com> - 9.87-1
- Annocheck: Fix memory corruption.  (#1988715)

* Wed Aug 11 2021 Nick Clifton  <nickc@redhat.com> - 9.86-1
- Annocheck: Skip certain tests for kernel modules.

* Tue Aug 10 2021 Nick Clifton  <nickc@redhat.com> - 9.85-1
- Annocheck: Detect a missing CET note.  (#1991931)
- Annocheck: Do not report future fails for AArch64 notes.
- Annocheck: Warn about multiple --debug-file, --debug-rpm and --debug-dir options.

* Mon Aug 09 2021 Nick Clifton  <nickc@redhat.com> - 9.84-1
- Annocheck: Process files in command line order.  (#1988714)

* Fri Jul 23 2021 Nick Clifton  <nickc@redhat.com> - 9.83-1
- Annocheck: Reverse AArch64 PAC+BTI check, ie fail if they are enabled.  (#1984995)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jul 13 2021 Nick Clifton  <nickc@redhat.com> - 9.82-1
- Annocheck: Add another test exceptions.

* Tue Jul 13 2021 Nick Clifton  <nickc@redhat.com> - 9.81-1
- Annocheck: Add some more test exceptions.

* Mon Jul 05 2021 Nick Clifton  <nickc@redhat.com> - 9.80-1
- Tests: Skip glibc-notes test if the assembler does not support --generate-missing-build-notes.  (#1978573)
- Tests: Skip objcopy test if objcopy does not support --merge-notes.

* Tue Jun 29 2021 Nick Clifton  <nickc@redhat.com> - 9.79-1
- Annocheck: Fix spelling mistake in -mstack-realign failure message.  (#1977349)

* Mon Jun 21 2021 Nick Clifton  <nickc@redhat.com> - 9.78-1
- gcc-plugin: Do not record global versions of stack protection settings in LTO mode, if not set.  (#1958954)

* Mon Jun 21 2021 Nick Clifton  <nickc@redhat.com> - 9.77-1
- Annocheck: Remove limit on number of input files.

* Tue Jun 15 2021 Nick Clifton  <nickc@redhat.com> - 9.76-1
- clang/llvm plugins: Build with correct security options.

* Tue Jun 15 2021 Nick Clifton  <nickc@redhat.com> - 9.75-1
- Annocheck: Better detection of GO compiler version.

* Wed Jun 09 2021 Nick Clifton  <nickc@redhat.com> - 9.74-1
- Annocheck: Better support for symbolic links.
- Annocheck: In verbose mode, report the reason for skipping specific tests.  (#1969584)

* Fri Jun 04 2021 Tom Stellard <tstellar@redhat.com> - 9.73-3
- Rebuild for LLVM 12.0.1

* Thu Jun 03 2021 Nick Clifton  <nickc@redhat.com> - 9.73-2
- Obsolete all previous versions of annobin.  (#1967339)

* Tue May 25 2021 Nick Clifton  <nickc@redhat.com> - 9.73-1
- Annocheck: Improve detection of shared libraries.  (#1958954)

* Wed May 19 2021 Nick Clifton  <nickc@redhat.com> - 9.72-2
- Tidy up spec file.

* Thu May 13 2021 Nick Clifton  <nickc@redhat.com> - 9.72-1
- Annocheck: Accept 0 as a valid number for gcc minor versions and release numbers.
- gcc-plugin: Add support for ARM and RISCV targets.

* Tue May 04 2021 Nick Clifton  <nickc@redhat.com> - 9.71-1
- timing: do not initialise the clock if the timing tool is disabled.

* Fri Apr 30 2021 Nick Clifton  <nickc@redhat.com> - 9.70-1
- gcc-plugin: Replace ICE messsages with verbose messages.

* Thu Apr 22 2021 Nick Clifton  <nickc@redhat.com> - 9.69-1
- Fix the testsuite so that it can be run in parallel.

* Wed Apr 21 2021 Nick Clifton  <nickc@redhat.com> - 9.68-1
- Annocheck: WARN if the annobin plugin was built for a newer version of the compiler than the one on which it was run.  (#1950657)

* Tue Apr 20 2021 Petr Pisar <ppisar@redhat.com> - 9.67-2
- Obsolete annobin < 9.66-1 (bug #1949570)

* Tue Apr 20 2021 Nick Clifton <nickc@redhat.com> - 9.67-1
- Annocheck: Improve detection of missing GNU-stack support.

* Mon Apr 19 2021 Petr Pisar <ppisar@redhat.com> - 9.66-4
- Bump a release

* Fri Apr 16 2021 Petr Pisar <ppisar@redhat.com> - 9.66-3
- Correct a package rename (bug #1949570)
- Require docs subpackage by the other ones because of a license
- Build-requiring perl-interpreter is enough

* Thu Apr 15 2021 Martin Cermak <mcermak@redhat.com> - 9.66-2
- Fix bz1949570

* Fri Apr 09 2021 Nick Clifton <nickc@redhat.com> - 9.66-1
- Fix anomolies reported by covscan.
- Move documentation into a sub-package.

* Sat Mar 20 2021 Jakub Jelinek <jakub@redhat.com> - 9.65-2
- NVR bump to rebuild against GCC 11.0.1

* Tue Mar 09 2021 Nick Clifton <nickc@redhat.com> - 9.65-1
- gcc-plugin: Use a fixed filename when running in LTO mode.

* Wed Mar 03 2021 Nick Clifton <nickc@redhat.com> - 9.64-1
- Annocheck: Fix detection of special function names.  (#1934189)

* Fri Feb 26 2021 Nick Clifton <nickc@redhat.com> - 9.63-1
- Annocheck: FAIL the deliberate use of -fno-stack-protector, but add some exceptions for glibc.  (#1923439)

* Thu Feb 25 2021 Nick Clifton <nickc@redhat.com> - 9.62-1
- Annocheck: Add colour to some messages.  Skip the deliberate use of -fno-stack-protector.  (#1923439)

* Mon Feb 22 2021 Nick Clifton <nickc@redhat.com> - 9.61-1
- Annocheck: Fix some problems with tests for missing notes.

* Wed Feb 10 2021 Tom Stellard <tstellar@redhat.com> = 9.60-2
- Split plugins into separate sub-packages

* Fri Feb 05 2021 Nick Clifton <nickc@redhat.com> - 9.60-1
- Add some GO tests to annocheck.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Nick Clifton <nickc@redhat.com> - 9.59-1
- Add a future fail for the presence of RPATH in the dynamic tags.

* Mon Jan 18 2021 Nick Clifton <nickc@redhat.com> - 9.58-1
- Add the ability to disable the warning message about -D_FORTIFY_SOURCE being missing.

* Wed Jan 13 2021 Nick Clifton <nickc@redhat.com> - 9.57-1
- Workaround for elflint problems with PPC compiled files.  (#1880634)

* Wed Jan 13 2021 Nick Clifton <nickc@redhat.com> - 9.56-1
- Fix bogus AArch64 test failures.

* Tue Jan 12 2021 Nick Clifton <nickc@redhat.com> - 9.55-1
- Improved testing by annocheck.  Add fixed format message mode.

* Mon Jan 04 2021 Nick Clifton <nickc@redhat.com> - 9.54-1
- Fix inconsistency reporting -fcf-protection and -fstack-clash-protection results.

* Mon Jan 04 2021 Nick Clifton <nickc@redhat.com> - 9.53-1
- Add support for -D_FORTIFY_SOURCE=3.

* Fri Dec 11 2020 Nick Clifton <nickc@redhat.com> - 9.52-2
- NVR bump in order to allow the new gating tests to be run.

* Fri Dec 11 2020 Nick Clifton <nickc@redhat.com> - 9.52-1
- annocheck: When a binary is produced both by GAS and GCC, select GAS as the real producer.  (#1906171)

* Thu Dec 10 2020 Nick Clifton <nickc@redhat.com> - 9.51-1
- annocheck: Improve test for LTO compiled binaries that do not have -Wall annotations.  (#1906171)

* Wed Dec 09 2020 Nick Clifton <nickc@redhat.com> - 9.50-1
- annocheck: Mark a missining -D_FORTIFY_SOURCE as a FAIL.

* Tue Dec 08 2020 Nick Clifton <nickc@redhat.com> - 9.49-1
- annocheck: Fix notes analyzer to accept empty PPC64 notes.

* Mon Dec 07 2020 Jakub Jelinek <jakub@redhat.com> - 9.48-5
- NVR bump for another ELN sidetag rebuild.

* Sun Dec 06 2020 Jakub Jelinek <jakub@redhat.com> - 9.48-4
- Revert back to previous settings.

* Sun Dec 06 2020 Jakub Jelinek <jakub@redhat.com> - 9.48-3
- Another NVR bump for GCC 11 rebuild.

* Sun Dec 06 2020 Jakub Jelinek <jakub@redhat.com> - 9.48-2
- NVR bump for GCC 11 rebuild.

* Wed Dec 02 2020 Nick Clifton <nickc@redhat.com> - 9.48-1
- gcc plugin: Tweak generation of end symbols for PPC64 when LTO is active.  (#1898075)

* Tue Dec 01 2020 Nick Clifton <nickc@redhat.com> - 9.47-1
- gcc plugin: Add support for GCC 11's cl_vars array.

* Fri Nov 27 2020 Jakub Jelinek <jakub@redhat.com> - 9.46-2
- NVR bump for another ELN sidetag rebuild.

* Tue Nov 24 2020 Nick Clifton <nickc@redhat.com> - 9.46-1
- Annocheck: Support enabling/disabling future fails.

* Wed Nov 18 2020 Nick Clifton <nickc@redhat.com> - 9.45-1
- GCC plugin: Always record global notes for the .text.startup,
  .text.exit, .text.hot and .text.cold sections.

* Tue Nov 17 2020 Nick Clifton <nickc@redhat.com> - 9.44-1
- Clang plugin: Add -lLLVM to the build command line.

* Mon Nov 16 2020 Nick Clifton <nickc@redhat.com> - 9.43-1
- Annocheck: Improve reporting of missing -D_FORTIFY_SOURCE option.  (#1898075)

* Mon Nov 16 2020 Nick Clifton <nickc@redhat.com> - 9.42-1
- Annocheck: Improve reporting of missing LTO option.

* Tue Nov 10 2020 Nick Clifton <nickc@redhat.com> - 9.41-1
- Add detecting of gimple compiled binaries.

* Mon Nov 09 2020 Nick Clifton <nickc@redhat.com> - 9.40-1
- Add --without-gcc-plugin option.

* Fri Nov 06 2020 Nick Clifton <nickc@redhat.com> - 9.38-1
- Annocheck: Fix bug parsing DW_AT_producer.

* Wed Nov 04 2020 Nick Clifton <nickc@redhat.com> - 9.37-1
- Add test of .note.gnu.property section for PowerPC.
- Add test of objcopy's ability to merge notes.

* Fri Oct 30 2020 Jakub Jelinek <jakub@redhat.com> - 9.36-2
- NVR bump for another ELN sidetag rebuild.

* Wed Oct 21 2020 Nick Clifton <nickc@redhat.com> - 9.36-1
- Record the -flto setting and produce a soft warning if it is absent.
- Suppress warnings about _D_GLIBCXX_ASSERTIONS if the source code is known to be something other than C++.

* Wed Oct 21 2020 Nick Clifton <nickc@redhat.com> - 9.35-3
- NVR bump to allow building on ELN sidetag.

* Mon Oct 05 2020 Nick Clifton <nickc@redhat.com> - 9.35-2
- Correct the directory chosen for 32-bit LLVM and Clang plugins.  (#1884951)

* Thu Oct 01 2020 Nick Clifton <nickc@redhat.com> - 9.35-1
- Allow the use of the SHF_LINK_ORDER section flag to discard unused notes.  (Experimental).

* Mon Sep 28 2020 Nick Clifton <nickc@redhat.com> - 9.34-1
- Enable the build and installation of the LLVM and Clang plugins.  (Experimental).

* Mon Sep 21 2020 Nick Clifton <nickc@redhat.com> - 9.33-1
- gcc-plugin: Fix test for empty PowerPC sections.  (#1880634)

* Thu Sep 17 2020 Nick Clifton <nickc@redhat.com> - 9.32-2
- NVR bump to allow rebuild against f34-build-side-30319.

* Tue Sep 15 2020 Nick Clifton <nickc@redhat.com> - 9.32-1
- annocheck: Add tests for the AArch64 BTI and PAC security features.  (#1862478)

* Thu Sep 10 2020 Nick Clifton <nickc@redhat.com> - 9.31-1
- gcc plugin: Use a 4 byte offset for PowerPC start symbols, so that they do not break disassemblies.

* Thu Sep 10 2020 Nick Clifton <nickc@redhat.com> - 9.30-1
- gcc plugin: Correct the detection of 32-bit x86 builds.  (#1876197)

* Mon Aug 17 2020 Nick Clifton <nickc@redhat.com> - 9.29-1
- gcc plugin: Detect any attempt to access the global_options array.

* Tue Aug 11 2020 Nick Clifton <nickc@redhat.com> - 9.28-1
- gcc plugin: Do not complain about missing pre-processor options when examining a preprocessed input file.  (#1862718)

* Thu Jul 30 2020 Nick Clifton <nickc@redhat.com> - 9.27-1
- Use more robust checks for AArch64 options.

* Thu Jul 30 2020 Nick Clifton <nickc@redhat.com> - 9.26-1
- Detect CLANG compiled assembler that is missing IBT support.

* Wed Jul 29 2020 Nick Clifton <nickc@redhat.com> - 9.25-1
- Improved target pointer size discovery.

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jul 26 2020 Nick Clifton <nickc@redhat.com> - 9.24-2
- Rebuild with plugin enabled to check that suppression works.

* Sun Jul 26 2020 Nick Clifton <nickc@redhat.com> - 9.24-1
- Add support for installing clang and llvm plugins.
- Temporary suppression of aarch64 pointer size check.  (#1860549)

* Sat Jul 25 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 9.23-2
- Rebuild for gcc 10.2

* Wed Jul 01 2020 Nick Clifton <nickc@redhat.com> - 9.23-1
- Annocheck: Do not skip tests of the short-enums notes.  (#1743635)

* Mon Jun 15 2020 Nick Clifton <nickc@redhat.com> - 9.22-1
- Add (optional) llvm plugin.

* Wed Apr 22 2020 Nick Clifton <nickc@redhat.com> - 9.21-1
- Annobin: Fall back on using the flags if the option cannot be found in cl_options.  (#1817659)

* Thu Apr 16 2020 Nick Clifton <nickc@redhat.com> - 9.20-1
- Annocheck: Detect Fortran compiled programs.  (#1824393)

* Wed Apr 01 2020 Nick Clifton <nickc@redhat.com> - 9.19-1
- Annobin: If option name mismatch occurs, seach for the real option.  (#1817452)

* Mon Mar 30 2020 Nick Clifton <nickc@redhat.com> - 9.18-1
- Annocheck: Fix a division by zero error when parsing GO binaries.  (#1818863)

* Fri Mar 27 2020 Nick Clifton <nickc@redhat.com> - 9.16-1
- Annobin: Fix access to the -flto and -fsanitize flags.

* Thu Mar 26 2020 Nick Clifton <nickc@redhat.com> - 9.14-1
- Annobin: Use offsets stored in gcc's cl_option structure to access the global_options array, thus removing the need to check for changes in the size of this structure.

* Thu Mar 26 2020 Nick Clifton <nickc@redhat.com> - 9.13-2
- NVR bump to allow rebuilding against new gcc.

* Thu Mar 12 2020 Nick Clifton <nickc@redhat.com> - 9.13-1
- Rename gcc plugin directory to gcc-plugin.
- Stop annocheck from complaining about missing options when the binary has been built in a mixed environment.

* Thu Mar 12 2020 Nick Clifton <nickc@redhat.com> - 9.12-3
- And again, this time with annotation enabled.  (#1810941)

* Thu Mar 12 2020 Nick Clifton <nickc@redhat.com> - 9.12-2
- NVR bump to enable rebuild against updated gcc.  (#1810941)

* Wed Mar 04 2020 Nick Clifton <nickc@redhat.com> - 9.12-1
- Improve builtby tool.
- Stop annocheck complaining about missing notes when the binary is not compiled by either gcc or clang.
- Skip the check of the ENTRY instruction for binaries not compiled by gcc or clang.  (#1809656)

* Fri Feb 28 2020 Nick Clifton <nickc@redhat.com> - 9.11-1
- Fix infinite loop hangup in annocheck.
- Disable debuginfod support by default.
- Improve parsing of .comment section.

* Thu Feb 27 2020 Nick Clifton <nickc@redhat.com> - 9.10-1
- Fix clang plugin to use hidden symbols.

* Tue Feb 25 2020 Nick Clifton <nickc@redhat.com> - 9.09-1
- Add ability to build clang plugin (disabled by default).

* Mon Feb 17 2020 Nick Clifton <nickc@redhat.com> - 9.08-1
- Annocheck: Fix error printing out the version number.

* Fri Feb 14 2020 Nick Clifton <nickc@redhat.com> - 9.07-1
- Annobin: Add checks of the exact location of the examined switches.

* Tue Feb 11 2020 Nick Clifton <nickc@redhat.com> - 9.06-1
- Annobin: Note when stack clash notes are generated.
- Annocheck: Handle multiple builder IDs in the .comment section.

* Fri Jan 31 2020 Nick Clifton <nickc@redhat.com> - 9.05-1
- Add configure option to suppress building annocheck.

* Fri Jan 31 2020 Nick Clifton <nickc@redhat.com> - 9.04-1
- Fix debuginfod test.

* Thu Jan 30 2020 Nick Clifton <nickc@redhat.com> - 9.03-2
- Correct the build requirement for building with debuginfod support.

* Thu Jan 30 2020 Nick Clifton <nickc@redhat.com> - 9.03-1
- Add debuginfod support.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 9.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Nick Clifton <nickc@redhat.com> - 9.01-2
- Rebuild againt latest gcc-10.

* Mon Jan 20 2020 Nick Clifton <nickc@redhat.com> - 9.01-1
- Add clang plugin (experimental).

* Fri Dec 06 2019 Nick Clifton <nickc@redhat.com> - 8.92-1
- Have annocheck ignore notes with an end address of 0.

* Mon Nov 18 2019 Nick Clifton <nickc@redhat.com> - 8.91-1
- Improve checking of gcc versions.

* Fri Nov 15 2019 Nick Clifton <nickc@redhat.com> - 8.90-1
- Do not skip positive results.

* Fri Nov 01 2019 Nick Clifton <nickc@redhat.com> - 8.88-1
- Generate a WARN result for code compiled with instrumentation enabled.  (#1753918)

* Tue Oct 22 2019 Nick Clifton <nickc@redhat.com> - 8.87-1
- Replace address checks with dladdr1.

* Mon Oct 21 2019 Nick Clifton <nickc@redhat.com> - 8.86-1
- Use libabigail like checking to ensure variable address consistency.

* Wed Oct 16 2019 Nick Clifton <nickc@redhat.com> - 8.85-1
- Skip generation of global notes for hot/cold sections.

* Thu Oct 10 2019 Nick Clifton <nickc@redhat.com> - 8.84-1
- Generate FAIL results if -Wall or -Wformat-security are missing.

* Thu Oct 03 2019 Nick Clifton <nickc@redhat.com> - 8.83-1
- If notes cannot be found in the executable look for them in the debuginfo file, if available.
- Generate a FAIL if notes are missing from the executable/debuginfo file.
- Record and report the setting of the AArcht64 specific -mbranch-protection option.

* Mon Sep 23 2019 Nick Clifton <nickc@redhat.com> - 8.81-1
- Improve detection of GO binaries.
- Add gcc version information to annobin notes.
- Do not complain about missing FORTIFY_SOURCE and GLIBCXX_ASSERTIONS in LTO compilations.

* Wed Sep 04 2019 Nick Clifton <nickc@redhat.com> - 8.79-2
- NVR bump to allow rebuild against latest gcc.  (#1748529)

* Tue Aug 06 2019 Nick Clifton <nickc@redhat.com> - 8.79-1
- Allow compiler used to run tests to be specified on the command line.  (#1723401)

* Tue Aug 06 2019 Nick Clifton <nickc@redhat.com> - 8.78-1
- Fix a memory allocation error in the annobin plugin.  (#1737306)

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Nick Clifton <nickc@redhat.com> - 8.77-1
- Another attempt at fixing the detection and reporting of missing -D_FORTIFY_SOURCE options.  (#1703500)

* Mon Jun 10 22:13:17 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.76-4
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:00 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 8.76-3
- Rebuild for RPM 4.15

* Thu Jun 06 2019 Panu Matilainen <pmatilai@redhat.com> - 8.76-2
- Really enable annocheck sub-package

* Tue Apr 30 2019 Nick Clifton <nickc@redhat.com> - 8.76-1
- Report a missing -D_FORTIFY_SOUCRE option if -D_GLIBCXX_ASSERTIONS was detected.  (#1703499)
- Do not report problems with -fstack-protection if the binary was not built by gcc or clang.  (#1703788)    

* Fri Apr 26 2019 Nick Clifton <nickc@redhat.com> - 8.74-1
- Add tests of clang command line options recorded in the DW_AT_producer attribute.

* Wed Apr 24 2019 Nick Clifton <nickc@redhat.com> - 8.73-1
- Fix test for an executable stack segment.  (#1700924)

* Thu Apr 18 2019 Nick Clifton <nickc@redhat.com> - 8.72-1
- Rebuild annobin with the latest rawhide gcc sources.  (#1700923)

* Thu Feb 28 2019 Nick Clifton <nickc@redhat.com> - 8.71-1
- Annobin: Suppress more calls to free() which are triggering memory checker errors.  (#1684148)

* Fri Feb 01 2019 Nick Clifton <nickc@redhat.com> - 8.70-1
- Add section flag matching ability to section size tool.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.69-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Björn Esser <besser82@fedoraproject.org> - 8.69-6
- Use 'with' for rich dependency on gcc

* Tue Jan 29 2019 Björn Esser <besser82@fedoraproject.org> - 8.69-5
- Really fix rhbz#1607430.

* Mon Jan 28 2019 Björn Esser <besser82@fedoraproject.org> - 8.69-4
- Rebuilt with annotations enabled

* Mon Jan 28 2019 Björn Esser <besser82@fedoraproject.org> - 8.69-3
- Fix rpm query for gcc version.

* Mon Jan 28 2019 Nick Clifton <nickc@redhat.com> - 8.69-2
- Add an exact requirement on the major version of gcc. (#1607430)

* Thu Jan 24 2019 Nick Clifton <nickc@redhat.com> - 8.69-1
- Annobin: Add support for .text.startup and .text.exit sections generated by gcc 9.
- Annocheck: Add a note displaying tool.

* Wed Jan 23 2019 Nick Clifton <nickc@redhat.com> - 8.68-1
- Annocheck: Skip checks for -D_FORTIFY_SOURCE and -D_GLIBCXX_ASSERTIONS if there is no compiler generated code in the binary.

* Mon Jan 21 2019 Björn Esser <besser82@fedoraproject.org> - 8.67-3
- Rebuilt with annotations enabled

* Mon Jan 21 2019 Björn Esser <besser82@fedoraproject.org> - 8.67-2
- Rebuilt for GCC 9

* Thu Jan 17 2019 Nick Clifton <nickc@redhat.com> - 8.67-1
- Annocheck: Only skip specific checks for specific symbols.  (#1666823)
- Annobin: Record the setting of the -fomit-frame-pointer option.

* Wed Jan 02 2019 Nick Clifton <nickc@redhat.com> - 8.66-1
- Annocheck: Do not ignore -Og when checking to see if an optimization level has been set.  (#1624162)

* Tue Dec 11 2018 Nick Clifton <nickc@redhat.com> - 8.65-1
- Annobin: Fix handling of multiple .text.unlikely sections.

* Fri Nov 30 2018 Nick Clifton <nickc@redhat.com> - 8.64-1
- Annocheck: Skip gaps in PPC64 executables covered by start_bcax_ symbols.  (#1630564)

* Mon Nov 26 2018 Nick Clifton <nickc@redhat.com> - 8.63-1
- Annocheck: Disable ENDBR test for shared libraries.  (#1652925)

* Mon Nov 26 2018 Nick Clifton <nickc@redhat.com> - 8.62-1
- Annocheck: Add test for ENDBR instruction at entry address of x86/x86_64 executables.  (#1652925)

* Tue Nov 20 2018 David Cantrell <dcantrell@redhat.com> - 8.61-2
- Adjust how the gcc_vr macro is set.

* Mon Nov 19 2018 Nick Clifton <nickc@redhat.com> - 8.61-1
- Fix building with gcc version 4.

* Tue Nov 13 2018 Nick Clifton <nickc@redhat.com> - 8.60-1
- Skip -Wl,-z,now and -Wl,-z,relro checks for non-gcc produced binaries.  (#1624421)

* Mon Nov 05 2018 Nick Clifton <nickc@redhat.com> - 8.59-1
- Ensure GNU Property notes are 8-byte aligned in x86_64 binaries.  (#1645817)

* Thu Oct 18 2018 Nick Clifton <nickc@redhat.com> - 8.58-1
- Skip PPC64 linker stubs created in the middle of text sections (again). (#1630640)

* Thu Oct 18 2018 Nick Clifton <nickc@redhat.com> - 8.57-1
- Suppress free of invalid pointer. (#1638371)

* Thu Oct 18 2018 Nick Clifton <nickc@redhat.com> - 8.56-1
- Skip PPC64 linker stubs created in the middle of text sections. (#1630640)

* Tue Oct 16 2018 Nick Clifton <nickc@redhat.com> - 8.55-1
- Reset the (PPC64) section start symbol to 0 if its section is empty.  (#1638251)

* Thu Oct 11 2018 Nick Clifton <nickc@redhat.com> - 8.53-1
- Also skip virtual thinks created by G++.  (#1630619)

* Wed Oct 10 2018 Nick Clifton <nickc@redhat.com> - 8.52-1
- Use uppercase for all fail/mayb/pass results.  (#1637706)

* Wed Oct 10 2018 Nick Clifton <nickc@redhat.com> - 8.51-1
- Generate notes for unlikely sections.  (#1630620)

* Mon Oct 08 2018 Nick Clifton <nickc@redhat.com> - 8.50-1
- Fix edge case computing section names for end symbols.  (#1637039)

* Mon Oct 08 2018 Nick Clifton <nickc@redhat.com> - 8.49-1
- Skip dynamic checks for binaries without a dynamic segment.  (#1636606)

* Fri Oct 05 2018 Nick Clifton <nickc@redhat.com> - 8.48-1
- Delay generating attach_to_group directives until the end of the compilation.  (#1636265)

* Mon Oct 01 2018 Nick Clifton <nickc@redhat.com> - 8.47-1
- Fix bug introduced in previous delta which would trigger a seg-fault when scanning for gaps.

* Mon Oct 01 2018 Nick Clifton <nickc@redhat.com> - 8.46-1
- Annobin:   Fix section name selection for startup sections.
- Annocheck: Improve gap skipping heuristics.   (#1630574)

* Mon Oct 01 2018 Nick Clifton <nickc@redhat.com> - 8.45-1
- Fix function section support (again).   (#1630574)

* Fri Sep 28 2018 Nick Clifton <nickc@redhat.com> - 8.44-1
- Skip compiler option checks for non-GNU producers.  (#1633749)

* Wed Sep 26 2018 Nick Clifton <nickc@redhat.com> - 8.43-1
- Fix function section support (again).   (#1630574)

* Tue Sep 25 2018 Nick Clifton <nickc@redhat.com> - 8.42-1
- Ignore ppc64le notes where start = end + 2.  (#1632259)

* Tue Sep 25 2018 Nick Clifton <nickc@redhat.com> - 8.41-1
- Make annocheck ignore symbols suffixed with ".end".  (#1639618)

* Mon Sep 24 2018 Nick Clifton <nickc@redhat.com> - 8.40-1
- Reinstate building annobin with annobin enabled.  (#1630550)

* Fri Sep 21 2018 Nick Clifton <nickc@redhat.com> - 8.39-1
- Tweak tests.

* Fri Sep 21 2018 Nick Clifton <nickc@redhat.com> - 8.38-1
- Generate notes and groups for .text.hot and .text.unlikely sections.
- When -ffunction-sections is active, put notes for startup sections into .text.startup.foo rather than .text.foo.
- Similarly put exit section notes into .text.exit.foo.  (#1630574)
- Change annocheck's maybe result for GNU Property note being missing into a PASS if it is not needed and a FAIL if it is needed.

* Wed Sep 19 2018 Nick Clifton <nickc@redhat.com> - 8.37-1
- Make the --skip-* options skip all messages about the specified test.

* Tue Sep 18 2018 Nick Clifton <nickc@redhat.com> - 8.36-1
- Improve error message when an ET_EXEC binary is detected.

* Mon Sep 17 2018 Nick Clifton <nickc@redhat.com> - 8.35-1
- Skip failures for PIC vs PIE.  (#1629698)

* Mon Sep 17 2018 Nick Clifton <nickc@redhat.com> - 8.34-1
- Ensure 4 byte alignment of note sub-sections.  (#1629671)

* Wed Sep 12 2018 Nick Clifton <nickc@redhat.com> - 8.33-1
- Add timing tool to report on speed of the checks.
- Add check for conflicting use of the -fshort-enum option.
- Add check of the GNU Property notes.
- Skip check for -O2 if compiled with -Og.  (#1624162)

* Mon Sep 03 2018 Nick Clifton <nickc@redhat.com> - 8.32-1
- Add test for ET_EXEC binaries.  (#1625627)
- Document --report-unknown option.

* Thu Aug 30 2018 Nick Clifton <nickc@redhat.com> - 8.31-1
- Fix bug in hardened tool which would skip gcc compiled files if the notes were too small.
- Fix bugs in section-size tool.
- Fix bug in built-by tool.

* Wed Aug 29 2018 Nick Clifton <nickc@redhat.com> - 8.30-1
- Generate notes for comdat sections. (#1619267)

* Thu Aug 23 2018 Nick Clifton <nickc@redhat.com> - 8.29-1
- Add more names to the gap skip list. (#1619267)

* Thu Aug 23 2018 Nick Clifton <nickc@redhat.com> - 8.28-1
- Skip gaps covered by _x86.get_pc_thunk and _savegpr symbols. (#1619267)
- Merge ranges where one is wholly covered by another.

* Wed Aug 22 2018 Nick Clifton <nickc@redhat.com> - 8.27-1
- Skip gaps at the end of functions. (#1619267)

* Tue Aug 21 2018 Nick Clifton <nickc@redhat.com> - 8.26-1
- Fix thinko in ppc64 gap detection code. (#1619267)

* Mon Aug 20 2018 Nick Clifton <nickc@redhat.com> - 8.25-1
- Skip gaps at the end of the .text section in ppc64 binaries. (#1619267)

* Wed Aug 15 2018 Nick Clifton <nickc@redhat.com> - 8.24-1
- Skip checks in stack_chk_local_fail.c
- Treat gaps as FAIL results rather than MAYBE.

* Wed Aug 08 2018 Nick Clifton <nickc@redhat.com> - 8.23-1
- Skip checks in __stack_chk_local_fail.

* Wed Aug 08 2018 Nick Clifton <nickc@redhat.com> - 8.22-1
- Reduce version check to gcc major version number only.  Skip compiler option checks if binary not built with gcc.  (#1603089)

* Tue Aug 07 2018 Nick Clifton <nickc@redhat.com> - 8.21-1
- Fix bug in annobin plugin.  Add --section-size=NAME option to annocheck.

* Thu Aug  2 2018 Peter Robinson <pbrobinson@fedoraproject.org> 8.20-2
- rebuild for new gcc

* Thu Aug 02 2018 Nick Clifton <nickc@redhat.com> - 8.20-1
- Correct name of man page for run-on-binaries-in script.  (#1611155)

* Wed Jul 25 2018 Nick Clifton <nickc@redhat.com> - 8.19-1
- Allow $ORIGIN to be at the start of entries in DT_RPATH and DT_RUNPATH.

* Mon Jul 23 2018 Nick Clifton <nickc@redhat.com> - 8.18-1
- Add support for big endian targets.

* Mon Jul 23 2018 Nick Clifton <nickc@redhat.com> - 8.17-1
- Count passes and failures on a per-component basis and report gaps.

* Fri Jul 20 2018 Nick Clifton <nickc@redhat.com> - 8.16-1
- Use our own copy of the targetm.asm_out.function_section() function.  (#159861 comment#17)

* Fri Jul 20 2018 Nick Clifton <nickc@redhat.com> - 8.15-1
- Generate grouped note section name all the time.  (#159861 comment#16)

* Thu Jul 19 2018 Nick Clifton <nickc@redhat.com> - 8.14-1
- Fix section conflict problem.  (#1603071)

* Wed Jul 18 2018 Nick Clifton <nickc@redhat.com> - 8.13-1
- Fix for building with gcc version 4.
- Fix symbol placement in functions with local assembler.

* Tue Jul 17 2018 Nick Clifton <nickc@redhat.com> - 8.12-1
- Fix assertions in range checking code.  Add detection of -U options.

* Tue Jul 17 2018 Nick Clifton <nickc@redhat.com> - 8.11-1
- Handle function sections properly.  Handle .text.startup and .text.unlikely sections.  Improve gap detection and reporting.  (#1601055)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Nick Clifton <nickc@redhat.com> - 8.10-1
- Fix construction of absolute versions of --dwarf-dir and --debug-rpm options.

* Tue Jul 10 2018 Nick Clifton <nickc@redhat.com> - 8.9-1
- Fix buffer overrun when very long symbol names are encountered.

* Tue Jul 10 2018 Nick Clifton <nickc@redhat.com> - 8.8-1
- Do not force the generation of function notes when -ffunction-sections is active.  (#1598961)

* Mon Jul 09 2018 Nick Clifton <nickc@redhat.com> - 8.7-1
- Skip the .annobin_ prfix when reporting symbols.  (#1599315)

* Mon Jul 09 2018 Nick Clifton <nickc@redhat.com> - 8.6-1
- Use the assembler (c++ mangled) version of function names when switching sections.  (#1598579)

* Mon Jul 09 2018 Nick Clifton <nickc@redhat.com> - 8.5-1
- Do not call function_section.  (#1598961)

* Fri Jul 06 2018 Nick Clifton <nickc@redhat.com> - 8.4-1
- Ignore cross-section gaps.  (#1598551)

* Thu Jul 05 2018 Nick Clifton <nickc@redhat.com> - 8.3-1
- Do not skip empty range notes in object files.  (#1598361)

* Mon Jul 02 2018 Nick Clifton <nickc@redhat.com> - 8.2-1
- Create the start symbol at the start of the function and the end symbol at the end.  (#1596823)

* Mon Jul 02 2018 Nick Clifton <nickc@redhat.com> - 8.1-1
- Fix --debug-rpm when used inside a directory.

* Thu Jun 28 2018 Nick Clifton <nickc@redhat.com> - 8.0-1
- Use a prefix for all annobin generated symbols, and make them hidden.
- Only generate weak symbol definitions for linkonce sections.

* Wed Jun 27 2018 Nick Clifton <nickc@redhat.com> - 7.1-1
- Skip some checks for relocatable object files, and dynamic objects.
- Stop bogus complaints about stackrealignment not being enabled.

* Mon Jun 25 2018 Nick Clifton <nickc@redhat.com> - 7.0-1
- Add -debug-rpm= option to annocheck.
- Only use a 2 byte offset for the initial symbol on PowerPC.

* Fri Jun 22 2018 Nick Clifton <nickc@redhat.com> - 6.6-1
- Use --dwarf-path when looking for build-id based debuginfo files.

* Fri Jun 22 2018 Nick Clifton <nickc@redhat.com> - 6.5-1
- Fix premature closing of dwarf handle.

* Fri Jun 22 2018 Nick Clifton <nickc@redhat.com> - 6.4-1
- Fix scoping bug computing the name of a separate debuginfo file.

* Tue Jun 19 2018 Nick Clifton <nickc@redhat.com> - 6.3-1
- Fix file descriptor leak.

* Tue Jun 19 2018 Nick Clifton <nickc@redhat.com> - 6.2-1
- Add command line options to annocheck to disable individual tests.

* Fri Jun 08 2018 Nick Clifton <nickc@redhat.com> - 6.1-1
- Remove C99-ism from annocheck sources.

* Wed Jun 06 2018 Nick Clifton <nickc@redhat.com> - 6.0-1
- Add the annocheck program.

* Fri Jun 01 2018 Nick Clifton <nickc@redhat.com> - 5.11-1
- Do not use the SHF_GNU_BUILD_NOTE section flag.

* Thu May 31 2018 Nick Clifton <nickc@redhat.com> - 5.10-1
- Remove .sh extension from shell scripts.

* Wed May 30 2018 Nick Clifton <nickc@redhat.com> - 5.9-1
- Record the setting of the -mstackrealign option for i686 binaries.

* Mon May 14 2018 Nick Clifton <nickc@redhat.com> - 5.8-1
- Hide the annobin start of file symbol.

* Tue May 08 2018 Nick Clifton <nickc@redhat.com> - 5.7-1
- Fix script bug in hardended.sh.  (Thanks to: Stefan Sørensen <stefan.sorensen@spectralink.com>)

* Thu May 03 2018 Nick Clifton <nickc@redhat.com> - 5.6-3
- Version number bump so that the plugin can be rebuilt with the latest version of GCC.

* Mon Apr 30 2018 Nick Clifton <nickc@redhat.com> - 5.6-2
- Rebuild the plugin with the newly created plugin enabled.  (#1573082)

* Mon Apr 30 2018 Nick Clifton <nickc@redhat.com> - 5.6-1
- Skip the isa_flags check in the ABI test because the crt[in].o files are compiled with different flags from the test files.

* Fri Apr 20 2018 Nick Clifton <nickc@redhat.com> - 5.3-1
- Add manual pages for annobin and the scripts.

* Tue Apr 03 2018 Nick Clifton <nickc@redhat.com> - 5.2-1
- Do not record a stack protection setting of -1.  (#1563141)

* Tue Mar 20 2018 Nick Clifton <nickc@redhat.com> - 5.1-1
- Do not complain about a dwarf_version value of -1.  (#1557511)

* Thu Mar 15 2018 Nick Clifton <nickc@redhat.com> - 5.0-1
- Bias file start symbols by 2 in order to avoid them confused with function symbols.  (#1554332)
- Version jump is to sync the version number with the annobin plugins internal version number.

* Mon Mar 12 2018 Nick Clifton <nickc@redhat.com> - 3.6-1
- Add --ignore-gaps option to check-abi.sh script.
- Use this option in the abi-test check.
- Tweak hardening test to skip pic and stack protection checks.

* Tue Mar 06 2018 Nick Clifton <nickc@redhat.com> - 3.5-1
- Handle functions with specific assembler names.  (#1552018)

* Fri Feb 23 2018 Nick Clifton <nickc@redhat.com> - 3.4-2
- Add an explicit requirement on the version of gcc used to built the plugin.  (#1547260)

* Fri Feb 09 2018 Nick Clifton <nickc@redhat.com> - 3.4-1
- Change type and size of symbols to STT_NOTYPE/0 so that they do not confuse GDB.  (#1539664)
- Add run-on-binaries-in.sh script to allow the other scripts to be run over a repository.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Nick Clifton <nickc@redhat.com> - 3.3-1
- Rebase on 3.3 release, which adds support for recording -mcet and -fcf-protection.

* Mon Jan 29 2018 Florian Weimer <fweimer@redhat.com> - 3.2-3
- Rebuild for GCC 8

* Fri Jan 26 2018 Nick Clifton <nickc@redhat.com> - 3.2-2
- Fix the installation of the annobin.info file.

* Fri Jan 26 2018 Nick Clifton <nickc@redhat.com> - 3.2-1
- Rebase on 3.2 release, which now contains documentation!

* Fri Jan 26 2018 Richard W.M. Jones <rjones@redhat.com> - 3.1-3
- Rebuild against GCC 7.3.1.

* Tue Jan 16 2018 Nick Clifton <nickc@redhat.com> - 3.1-2
- Add --with-gcc-plugin-dir option to the configure command line.

* Thu Jan 04 2018 Nick Clifton <nickc@redhat.com> - 3.1-1
- Rebase on version 3.1 sources.

* Mon Dec 11 2017 Nick Clifton <nickc@redhat.com> - 2.5.1-5
- Do not generate notes when there is no output file.  (#1523875)

* Fri Dec 08 2017 Nick Clifton <nickc@redhat.com> - 2.5.1-4
- Invent an input filename when reading from a pipe.  (#1523401)

* Thu Nov 30 2017 Florian Weimer <fweimer@redhat.com> - 2.5.1-3
- Use DECL_ASSEMBLER_NAME for symbol references (#1519165)

* Tue Oct 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.5.1-2
- Cleanups in spec

* Tue Sep 26 2017 Nick Clifton <nickc@redhat.com> - 2.5.1-1
- Touch the auto-generated files in order to stop them from being regenerated.

* Tue Sep 26 2017 Nick Clifton <nickc@redhat.com> - 2.5-2
- Stop the plugin complaining about compiler datestamp mismatches.

* Thu Sep 21 2017 Nick Clifton <nickc@redhat.com> - 2.4-1
- Tweak tests so that they will run on older machines.

* Thu Sep 21 2017 Nick Clifton <nickc@redhat.com> - 2.3-1
- Add annobin-tests subpackage containing some preliminary tests.
- Remove link-time test for unsupported targets.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Florian Weimer <fweimer@redhat.com> - 2.0-2
- Rebuild with binutils fix for ppc64le (#1475636)

* Wed Jun 28 2017 Nick Clifton <nickc@redhat.com> - 2.0-1
- Fixes for problems reported by the package submission review:
   * Add %%license entry to %%file section.
   * Update License and BuildRequires tags.
   * Add Requires tag.
   * Remove %%clean.
   * Add %%check.
   * Clean up the %%changelog.
- Update to use version 2 of the specification and sources.

* Thu May 11 2017 Nick Clifton <nickc@redhat.com> - 1.0-1
- Initial submission.
