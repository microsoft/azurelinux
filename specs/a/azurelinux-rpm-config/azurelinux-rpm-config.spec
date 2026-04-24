## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autochangelog
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#                        TO WHOM IT MAY CONCERN
#
# Don't add patches, dist-git is the upstream repository for this package.

Summary: Red Hat-family-specific rpm configuration files
Name: azurelinux-rpm-config
# The version should be 300 + Fedora release number.
# If the branches haven't diverged yet, keep the Fedora release number from
# the older branch. When the branch diverges, bump the Version to the Fedora
# release number.
Version: 1004
Release: 3%{?dist}
# config.guess, config.sub are GPL-3.0-or-later WITH Autoconf-exception-generic
License: GPL-1.0-or-later AND GPL-2.0-or-later AND GPL-3.0-or-later WITH Autoconf-exception-generic
URL: https://aka.ms/azurelinux

# Core rpm settings
Source0: macros
Source1: rpmrc

# gcc specs files for hardened builds
Source50: redhat-hardened-cc1
Source51: redhat-hardened-ld
Source52: redhat-hardened-ld-errors
# clang config spec files
Source53: redhat-hardened-clang.cfg
Source54: redhat-hardened-clang-ld.cfg

# gcc specs files for annobin builds
Source60: redhat-annobin-cc1
Source61: redhat-annobin-select-gcc-built-plugin
Source62: redhat-annobin-select-annobin-built-plugin
Source63: redhat-annobin-plugin-select.sh

# The macros defined by these files are for things that need to be defined
# at srpm creation time when it is not feasible to require the base packages
# that would otherwise be providing the macros. other language/arch specific
# macros should not be defined here but instead in the base packages that can
# be pulled in at rpm build time, this is specific for srpm creation.
Source100: macros.fedora-misc-srpm
Source102: macros.mono-srpm
Source103: macros.nodejs-srpm
Source104: macros.ldc-srpm
Source105: macros.valgrind-srpm
Source108: macros.dotnet-srpm
Source109: macros.hare-srpm

# Other misc macros
Source150: macros.build-constraints
Source151: macros.dwz
Source152: macros.fedora-misc
Source155: macros.ldconfig
Source156: macros.vpath
Source157: macros.shell-completions
Source158: macros.rpmautospec

# Build policy scripts
# this comes from https://github.com/rpm-software-management/rpm/pull/344
# added a python -> python2 conversion for fedora with warning
# and an echo when the mangling happens
Source201: brp-mangle-shebangs

# Dependency generator scripts (deprecated)
Source300: find-provides
Source304: find-requires

# Misc helper scripts
Source400: dist.sh

# Snapshots from http://git.savannah.gnu.org/gitweb/?p=config.git
Source500: https://git.savannah.gnu.org/cgit/config.git/plain/config.guess
Source501: https://git.savannah.gnu.org/cgit/config.git/plain/config.sub

# Dependency generators & their rules
Source602: libsymlink.attr

# BRPs
Source700: brp-ldconfig
Source701: brp-strip-lto

# Convenience lua functions
Source800: common.lua

# Documentation
Source900: buildflags.md

BuildArch: noarch
BuildRequires: perl-generators
Requires: coreutils

Requires: efi-srpm-macros
Requires: fonts-srpm-macros
# ↓ Provides macros.forge and forge.lua originally shipped by us
Requires: forge-srpm-macros
Requires: gap-srpm-macros
Requires: go-srpm-macros
Requires: java-srpm-macros
# ↓ Provides kmod.attr originally shipped by us
Requires: kernel-srpm-macros >= 1.0-12
Requires: lua-srpm-macros
Requires: ocaml-srpm-macros
Requires: openblas-srpm-macros
Requires: perl-srpm-macros
# ↓ Has Python BRPs originaly present in redhat-rpm-config
Requires: python-srpm-macros >= 3.11-7
Requires: qt6-srpm-macros
Requires: rust-srpm-macros
Requires: package-notes-srpm-macros
Requires: pyproject-srpm-macros
# ↓ Create compat Provides/Requires when things move around in filesystem
Requires: filesystem-srpm-macros

%if ! 0%{?rhel}
Requires: ansible-srpm-macros
Requires: fpc-srpm-macros
Requires: ghc-srpm-macros
Requires: gnat-srpm-macros
Requires: tree-sitter-srpm-macros
Requires: qt5-srpm-macros
Requires: zig-srpm-macros
Requires: build-reproducibility-srpm-macros
%endif

Requires: rpm >= 4.19.91
Requires: dwz >= 0.4
Requires: zip
Requires: (annobin-plugin-gcc if gcc)
Requires: (gcc-plugin-annobin if gcc)
# ↓ to not break packages that buildrequire GnuPG but use it through GPGverify
Requires: (gpgverify if gnupg2)

# for brp-mangle-shebangs
Requires: %{_bindir}/find
Requires: %{_bindir}/file
Requires: %{_bindir}/grep
Requires: %{_bindir}/sed
Requires: %{_bindir}/xargs

# -fstack-clash-protection and -fcf-protection require GCC 8.
Conflicts: gcc < 8.0.1-0.22

# Replaced by macros.rpmautospec shipped by us
Obsoletes: rpmautospec-rpm-macros < 0.6.3-2

Provides: system-rpm-config = %{version}-%{release}

%global rrcdir /usr/lib/rpm/redhat

Provides: redhat-rpm-config = %{version}-%{release}
Obsoletes: redhat-rpm-config < 1000
Conflicts: redhat-rpm-config < 1000
%description
Red Hat specific rpm configuration files.

%prep
# Not strictly necessary but allows working on file names instead
# of source numbers in install section
%setup -c -T
cp -p %{sources} .

%install
mkdir -p %{buildroot}/usr/lib/rpm
ln -sf redhat %{buildroot}/usr/lib/rpm/azurelinux
mkdir -p %{buildroot}%{rrcdir}
install -p -m 644 -t %{buildroot}%{rrcdir} macros rpmrc
install -p -m 444 -t %{buildroot}%{rrcdir} redhat-hardened-*
install -p -m 444 -t %{buildroot}%{rrcdir} redhat-annobin-*
install -p -m 755 -t %{buildroot}%{rrcdir} config.*
install -p -m 755 -t %{buildroot}%{rrcdir} dist.sh
install -p -m 755 -t %{buildroot}%{rrcdir} brp-*

install -p -m 755 -t %{buildroot}%{rrcdir} find-*
install -p -m 755 -t %{buildroot}%{rrcdir} brp-*

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
install -p -m 644 -t %{buildroot}%{_rpmconfigdir}/macros.d macros.*

mkdir -p %{buildroot}%{_fileattrsdir}
install -p -m 644 -t %{buildroot}%{_fileattrsdir} *.attr

mkdir -p %{buildroot}%{_rpmluadir}/fedora/{rpm,srpm}
install -p -m 644 -t %{buildroot}%{_rpmluadir}/fedora common.lua

# This trigger is used to decide which version of the annobin plugin for gcc
# should be used.  See comments in the script for full details.
#
# Note - whilst "gcc-plugin-annobin" requires "gcc" and hence in theory we
# do not need to trigger on "gcc", the redhat-annobin-plugin-select.sh
# script invokes gcc to determine the version of the gcc plugin, and this
# can be significant.
#
# For example, suppose that version N of gcc is installed and that annobin
# version A (built by gcc version N) is also installed.  Then a new version
# of gcc is released.  If the rpms are updated in this order:
#   gcc-plugin-annobin
#   gcc
# then when the trigger for gcc-plugin-annobin is run, the script will see
# (the not yet updated) gcc is currently version N, which matches the current
# annobin plugin A, so no changes are necessary.  Then gcc is updated and,
# if the trigger below did not include "gcc", the script would not run again
# and so now you would have an out of date version of the annobin plugin.
#
# Alternatively imagine installing gcc and annobin for the first time.
# If the installation order is:
#    gcc
#    annobin-plugin-gcc
#    gcc-plugin-annobin
# then the installation of gcc will not cause the gcc-plugin-annobin to be
# selected, since it does not exist yet.  Then annobin-plugin-gcc is installed
# and since it is the only plugin, it will be selected.  Then
# gcc-plugin-annobin is installed, and if the trigger below was not set to
# run on gcc-plugin-annobin, it would pass unnoticed.
#
# Hence it is necessary to trigger on both gcc and gcc-plugin-annobin.

ln -sf fedora %{buildroot}%{_rpmluadir}/azurelinux
%triggerin -- annobin-plugin-gcc gcc-plugin-annobin gcc
%{rrcdir}/redhat-annobin-plugin-select.sh
%end

# We also trigger when an annobin plugin is uninstalled.  This allows us to
# switch over to the other version of the plugin.  Note - we do not bother
# triggering on the uninstallation of "gcc", since if that is removed, the
# plugins are rendered useless.

%triggerpostun -- annobin-plugin-gcc gcc-plugin-annobin
%{rrcdir}/redhat-annobin-plugin-select.sh
%end

%files
/usr/lib/rpm/azurelinux
%dir %{rrcdir}
%{rrcdir}/brp-ldconfig
%{rrcdir}/brp-mangle-shebangs
%{rrcdir}/brp-strip-lto
%{rrcdir}/config.*
%{rrcdir}/dist.sh
%{rrcdir}/find-provides
%{rrcdir}/find-requires
%{rrcdir}/macros
%{rrcdir}/redhat-hardened-*
%{rrcdir}/rpmrc
%{_fileattrsdir}/*.attr
%{_rpmconfigdir}/macros.d/macros.*-srpm
%{_rpmconfigdir}/macros.d/macros.build-constraints
%{_rpmconfigdir}/macros.d/macros.dwz
%{_rpmconfigdir}/macros.d/macros.fedora-misc
%{_rpmconfigdir}/macros.d/macros.ldconfig
%{_rpmconfigdir}/macros.d/macros.rpmautospec
%{_rpmconfigdir}/macros.d/macros.shell-completions
%{_rpmconfigdir}/macros.d/macros.vpath
%dir %{_rpmluadir}/fedora
%dir %{_rpmluadir}/fedora/srpm
%dir %{_rpmluadir}/fedora/rpm
%{_rpmluadir}/fedora/*.lua

%attr(0755,-,-) %{rrcdir}/redhat-annobin-plugin-select.sh
%verify(owner group mode) %{rrcdir}/redhat-annobin-cc1
%{rrcdir}/redhat-annobin-select-gcc-built-plugin
%{rrcdir}/redhat-annobin-select-annobin-built-plugin

%doc buildflags.md

%{_rpmluadir}/azurelinux
%changelog
## START: Generated by rpmautospec
* Thu Dec 05 2024 Michal Domonkos <mdomonko@redhat.com> - 300-1
- Fix automatic soname requires on non-versioned symlink targets

* Thu Dec 05 2024 Denys Vlasenko <dvlasenk@redhat.com> - 299-1
- find-provides: fix filtering for find-provides.ksyms

* Wed Nov 20 2024 Matthieu Bec <mbec@lbto.org> - 298-1
- Restore handling of %%__brp_mangle_shebangs_exclude
- Fixes: rhbz#2312961

* Wed Oct  2 2024 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 297-1
- Pull in filesystem-srpm-macros

* Wed Sep 25 2024 Siddhesh Poyarekar <siddhesh@redhat.com> - 296-1
- Change ppc64le tuning to Power 10 for RHEL10 and beyond.

* Fri Sep 06 2024 Dridi Boukelmoune <dridi@fedoraproject.org> - 295-1
- Define %%hare_arches with a list of Hare host architectures

* Wed Aug 14 2024 Frédéric Bérat <fberat@redhat.com> - 294-1
- Update config.{guess,sub} to gnuconfig git HEAD

* Fri Jun  7 2024 Florian Weimer <fweimer@redhat.com> - 293-1
- Enable DT_RELR for aarch64

* Fri May 31 2024 Daan De Meyer <daan.j.demeyer@gmail.com> - 292-1
- Use --config=xxx for clang configs instead of two separate arguments to work
  around a bug in meson

* Wed May 22 2024 Michal Domonkos <mdomonko@redhat.com> - 291-1
- Drop the now obsolete %%install override hack for debuginfo enablement

* Mon May 13 2024 Timm Bäder <tbaeder@redhat.com> - 290-1
- Add clang link config file

* Tue May  7 2024 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 289-1
- Add %%__os_install_post_build_reproducibility to %%__os_install_post.
  This hooks 'add-determinism' post-processing tool into the build process.
  See https://fedoraproject.org/wiki/Changes/ReproduciblePackageBuilds
  and https://docs.fedoraproject.org/en-US/reproducible-builds/ for
  more details.
- Pull in build-reproducibility-srpm-macros.

* Thu Apr 11 2024 Nikita Popov <npopov@redhat.com> - 288-1
- Use Fat LTO with Clang

* Thu Mar 14 2024 Florian Weimer <fweimer@redhat.com> - 287-1
- Enable TLS descriptors on x86-64 (GCC only)

* Tue Mar 12 2024 Omair Majid <omajid@redhat.com> - 286-1
- Define %%dotnet_arches with a list of .NET-compatible architectures

* Tue Feb 20 2024 Miro Hrončok <mhroncok@redhat.com> - 285-1
- brp-mangle-shebangs: Strip env flags when mangling shebangs
- For example, mangle "#!/usr/bin/env -S vd" to "#!/usr/bin/vd"
- Fixes: rhbz#2265038

* Wed Feb 14 2024 Florian Weimer <fweimer@redhat.com> - 284-1
- Correct advise for disabling debuginfo packages (#2264161)

* Wed Feb 14 2024 Frédéric Bérat <fberat@redhat.com> - 283-1
- Update config.{guess,sub} to gnuconfig git HEAD

* Tue Feb 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 282-1
- Loosen rust-srpm-macros requirement

* Mon Feb 05 2024 Jonathan Wright <jonathan@almalinux.org> - 281-1
- simplify microarch macros for x86_64

* Tue Jan 16 2024 Florian Weimer <fweimer@redhat.com> - 280-1
- Drop -fcf-protection for i686 because there won't be kernel support

* Tue Jan 16 2024 Nils Philippsen <nils@redhat.com> - 279-1
- Obsolete rpmautospec-rpm-macros without version

* Mon Jan 15 2024 Nick Clifton  <nickc@redhat.com> - 278-1
- Add hardening feature to convert linker warning messages into errors.
- https://fedoraproject.org/wiki/Changes/Linker_Error_On_Security_Issues

* Mon Jan 15 2024 Florian Weimer <fweimer@redhat.com> - 277-1
- Switch C type safety level to 3 (GCC 14 default), and adjust for GCC 14

* Thu Jan 11 2024 Jan Grulich <jgrulich@redhat.com> - 276-1
- Drop qt5-srpm-macros from RHEL 10

* Fri Jan 05 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 275-1
- Define RUSTFLAGS only when rust macros are installed

* Wed Jan  3 2024 Florian Weimer <fweimer@redhat.com> - 274-1
- Missing packed relative relocation support on aarch64, s390x (#2256645)

* Tue Jan  2 2024 Florian Weimer <fweimer@redhat.com> - 273-1
- Pack relative ELF relocations by default

* Tue Dec 26 2023 Jan Drögehoff <sentrycraft123@gmail.com> - 272-1
- Add zig-srpm-macros

* Fri Nov 03 2023 Stephen Gallagher <sgallagh@redhat.com> - 271-1
- ELN: Enable frame pointers for RHEL 11+ (for now)

* Thu Oct  5 2023 Florian Weimer <fweimer@redhat.com> - 270-1
- Disable -fstack-clash-protection on riscv64 (#2242327)

* Thu Oct  5 2023 Nikita Popov <npopov@redhat.com> - 269-1
- Use correct format specifier in brp-llvm-compile-lto-elf

* Fri Sep 29 2023 Nikita Popov <npopov@redhat.com> - 268-1
- Fix brp-llvm-compile-lto-elf parallelism with hardlinks (#2234024)

* Tue Sep 26 2023 Florian Weimer <fweimer@redhat.com> - 267-1
- Switch %%build_type_safety_c to 1 (#2142177)

* Thu Sep 07 2023 Maxwell G <maxwell@gtmx.me> - 266-1
- Split out forge macros to forge-srpm-macros package

* Tue Aug 29 2023 Florian Weimer <fweimer@redhat.com> - 265-1
- Add support for x86_64_v2, x86_64_v3, x86_64_v4 (#2233093)

* Tue Aug 22 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 264-1
- Add macros.rpmautospec

* Mon Aug 21 2023 Miroslav Suchy <msuchy@redhat.com> - 263-1
- Migrate to SPDX

* Wed Aug 02 2023 Charalampos Stratakis <cstratak@redhat.com> - 262-1
- Strip all extension builder flags except -fexceptions and -fcf-protection
- https://fedoraproject.org/wiki/Changes/Python_Extension_Flags_Reduction

* Fri Jul  7 2023 Florian Weimer <fweimer@redhat.com> - 261-1
- Fix warnings that appear during the build of the llvm package

* Wed Jul  5 2023 Florian Weimer <fweimer@redhat.com> - 260-1
- Implement the %%build_type_safety_c macro (#2218019)

* Wed Jul  5 2023 Florian Weimer <fweimer@redhat.com> - 259-1
- Filter out C, C++ build flags from Fortran build flags (#2177253)

* Wed Jul  5 2023 Florian Weimer <fweimer@redhat.com> - 258-1
- Enable PIC mode for assembler files (#2167430)

* Wed Jul 05 2023 Frederic Berat <fberat@redhat.com> - 257-1
- update config.{guess,sub} to gnuconfig git HEAD

* Sat Jun 17 2023 Tom Stellard <tstellar@redhat.com> - 256-1
- Remove -fno-openmp-implicit-rpath from clang ldflags

* Fri Jun 16 2023 Lumír Balhar <lbalhar@redhat.com> - 255-1
- Add qt6-srpm-macros

* Thu Mar  9 2023 Florian Weimer <fweimer@redhat.com> - 254-1
- Switch ELN to x86-64-v3

* Tue Feb 28 2023 Maxwell G <gotmax@e.email> - 253-1
- Include RUSTFLAGS in %%set_build_flags
- Fixes: rhbz#2167183

* Tue Feb 28 2023 Tom Stellard <tstellar@redhat.com> - 252-1
- Rename _pkg_extra_* macros to _distro_extra_*

* Thu Feb 23 2023 Miro Hrončok <mhroncok@redhat.com> - 251-1
- Drop the requirement of orphaned nim-srpm-macros
- No Fedora package uses the %%nim_arches macro

* Tue Feb 14 2023 Frederic Berat <fberat@redhat.com> - 250-1
- update config.{guess,sub} to gnuconfig git HEAD

* Thu Feb 09 2023 Jerry James <loganjerry@gmail.com> - 249-1
- Add macros.gap-srpm

* Tue Feb 07 2023 Tom Stellard <tstellar@redhat.com> - 248-1
- Add %%pkg_extra_* macros

* Mon Feb 06 2023 Nick Clifton  <nickc@redhat.com> - 247-1
- Fix triggers for the installation and removal of gcc-plugin-annobin.
  Fixes: rhbz#2124562

* Tue Jan 17 2023 Miro Hrončok <mhroncok@redhat.com> - 246-1
- Add pyproject-srpm-macros to the default buildroot

* Tue Jan 17 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 245-1
- Do not include frame pointers on ppc64le for now
  Fixes: rhbz#2161595

* Mon Jan 16 2023 Tom Stellard <tstellar@redhat.com> - 244-1
- Make -flto=thin the default lto flag for clang

* Mon Jan 16 2023 Siddhesh Poyarekar <siddhesh@redhat.com> - 243-1
- Consolidate the _FORTIFY_SOURCE switches.

* Fri Jan 13 2023 Miro Hrončok <mhroncok@redhat.com> - 242-1
- Don't use %%[ ] expressions with %%{undefined}
- Fixes: rhbz#2160716

* Thu Jan 12 2023 Stephen Gallagher <sgallagh@redhat.com> - 241-1
- Do not include frame pointers on RHEL

* Tue Jan 10 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 240-1
- Do not include frame pointers on i686 and s390x for now

* Wed Jan  4 2023 Davide Cavalca <dcavalca@fedoraproject.org> - 239-1
- Enable frame pointers by default
- Set arch specific flags for frame pointers support

* Tue Jan  3 2023 Miro Hrončok <mhroncok@redhat.com> - 238-1
- Set %%source_date_epoch_from_changelog to 1
- https://fedoraproject.org/wiki/Changes/ReproducibleBuildsClampMtimes

* Tue Jan  3 2023 Siddhesh Poyarekar <siddhesh@redhat.com> - 237-1
- Make _FORTIFY_SOURCE configurable and bump default to 3.

* Wed Dec 28 2022 Davide Cavalca <dcavalca@fedoraproject.org> - 236-1
- Add conditional support for always including frame pointers

* Sat Dec 10 2022 Florian Weimer <fweimer@redhat.com> - 235-1
- Add %%_configure_use_runstatedir to disable --runstatedir configure option

* Fri Nov  4 2022 Tom Stellard <tstellar@redhat.com> - 234-1
- Remove unsupported arches from rpmrc

* Fri Nov  4 2022 Florian Weimer <fweimer@redhat.com> - 233-1
- Set -g when building Vala applications

* Fri Sep 23 2022 Timm Bäder <tbaeder@redhat.com> - 232-1
- Fix brp-compile-lto-elf to not rely on a backtracking regex

* Thu Sep 08 2022 Maxwell G <gotmax@e.email> - 231-1
- forge macros: Support Sourcehut. Fixes rhbz#2035935.

* Tue Aug 30 2022 Frederic Berat <fberat@redhat.com> - 230-1
- Add support for runstatedir in %%configure

* Fri Aug 26 2022 Dan Horák <dan[at]danny.cz> - 229-1
- Move the baseline s390x arch to z13 for F-38+

* Mon Aug 8 2022 Maxwell G <gotmax@e.email> - 228-1
- Add macros.shell-completions

* Fri Aug 05 2022 Nikita Popov <npopov@redhat.com> - 227-1
- brp-llvm-compile-lto-elf: Pass -r to xargs

* Wed Jun 22 2022 Timm Bäder <tbaeder@redhat.com> - 226-1
- Move llvm_compile_lto_to_elf before __debug_install_post

* Fri Jun 17 2022 Nick Clifton  <nickc@redhat.com> - 225-1
- Add definition of _find_debuginfo_extra_opts which will
-  move annobin data into a separate debuginfo file.

* Tue Jun 14 2022 Tom Stellard <tstellar@redhat.com> - 224-1
- Fix passing of CFLAGS to brp-llvm-compile-lto-elf

* Fri May 27 2022 Tom Stellard <tstellar@redhat.com> - 223-1
- Move -fno-openmp-implicit-rpath option from CFLAGS to LDFLAGS

* Fri May 27 2022 Florian Weimer <fweimer@redhat.com> - 222-1
- Use %%baserelease to store the version number

* Fri May 27 2022 Frederic Berat <fberat@redhat.com> - 221-1
- update config.{guess,sub} to gnuconfig git HEAD

* Tue May 17 2022 Maxwell G <gotmax@e.email> - 220-1
- Add `Requires: ansible-srpm-macros`

* Tue May 17 2022 Miro Hrončok <mhroncok@redhat.com> - 219-2
- Remove a tab character from the definition of %%__global_compiler_flags
- Fixes: rhbz#2083296

* Tue May 10 2022 Mikolaj Izdebski <mizdebsk@redhat.com> - 219-1
- Add java_arches macro

* Wed Apr 20 2022 Timm Bäder <tbaeder@redhat.com> - 218-1
- Parallelize bpr-llvm-compile-lto-elf

* Tue Apr 19 2022 Tom Stellard <tstellar@redhat.com> - 217-1
- Add -fno-openmp-implicit-rpath when building with clang

* Wed Apr 13 2022 Nick Clifton  <nickc@redhat.com> - 216-1
- Add support for comparing gcc-built and annobin-built plugins.

* Mon Feb 21 2022 Timm Bäder <tbaeder@redhat.com> - 215-1
- Add %%__brp_remove_la_files to %%__os_install_post

* Thu Feb 10 2022 Florian Weimer <fweimer@redhat.com> - 214-1
- ppc64le: Switch baseline to POWER9 on ELN (ELN issue 78)

* Thu Feb 10 2022 Florian Weimer <fweimer@redhat.com> - 213-1
- s390x: Switch baseline to z14 on ELN (ELN issue 79)

* Sun Jan 23 2022 Robert-André Mauchin <zebob.m@gmail.com> - 212-1
- Add package note generation to %%check preamble
- Fix: rhbz#2043977

* Fri Jan 21 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 211-1
- Move package note generation to build preamble
- Do ELF package notes also on ELN

* Thu Jan 20 2022 Miro Hrončok <mhroncok@redhat.com> - 210-1
- Remove package ELF note from the extension LDFLAGS
- Related: rhbz#2043092
- Fix %%set_build_flags when %%_generate_package_note_file is not defined
- Fixes: rhbz#2043166

* Thu Jan 13 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 209-1
- Add package ELF note to the default LDFLAGS

* Tue Jan 04 2022 Tom Stellard <tstellar@redhat.com> - 208-1
- Call %%set_build_flags before %%build, %%check, and %%install stages

* Tue Dec 14 2021 Tom Stellard <tstellar@redhat.com> - 207-1
- Add -Wl,--build-id=sha1 to the default LDFLAGS

* Tue Dec 07 2021 Miro Hrončok <mhroncok@redhat.com> - 206-1
- brp-mangle-shebangs: also mangle shebangs of JavaScript executables
- Fixes: rhbz#1998924

* Thu Nov 18 2021 Michal Domonkos <mdomonko@redhat.com> - 205-1
- Drop kernel-rpm-macros subpackage & kmod.attr (new home: kernel-srpm-macros)

* Tue Nov 16 2021 Miro Hrončok <mhroncok@redhat.com> - 204-1
- Don't pull in Python to all buildroots
- Remove llvm-lto-elf-check script

* Tue Nov 09 2021 Michal Domonkos <mdomonko@redhat.com> - 203-1
- Drop {fpc,gnat,nim}-srpm-macros dependencies on RHEL

* Wed Nov 03 2021 David Benoit <dbenoit@redhat.com> - 202-1
- Add llvm-lto-elf-check script
- Resolves: rhbz#2017193

* Mon Nov 01 2021 Jason L Tibbitts III <j@tib.bs> - 201-1
- Better error handling for %%constrain_build.

* Mon Oct 18 2021 Jason L Tibbitts III <j@tib.bs> - 200-1
- Add %%constrain_build macro.

* Tue Sep 21 2021 Tom Stellard <tstellar@redhat.com> - 199-1
- Drop annobin-plugin-clang dependency

* Mon Aug 30 2021 Florian Weimer <fweimer@redhat.com> - 198-1
- ELN: Enable -march=x86-64-v2 for Clang as well

* Tue Aug 17 2021 Tom Stellard <tstellar@redhat.com> - 197-1
- Add build_ preifix to cc, cxx, and cpp macros

* Mon Aug 16 2021 Tom Stellard <tstellar@redhat.com> - 196-1
- Add cc, cxx, and cpp macros

* Sun Aug 15 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 195-1
- Fix macros.build-constraints' %%limit_build
  - number of CPUs will never be set to less than 1
  - this now outputs build flag overrides to be used with %%make_build etc.
  - add documentation

* Mon Aug  2 2021 Florian Weimer <fweimer@redhat.com> - 194-1
- Active GCC plugin during LTO linking

* Sat Jul 24 2021 Michel Alexandre Salim <salimma@fedoraproject.org> - 193-1
- Add macros.build-constraints
- Keep the misc macros in alphabetical order

* Sat Jul 10 2021 Neal Gompa <ngompa13@gmail.com> - 192-1
- Make vpath builddir not include arch-specific info

* Thu Jul 01 2021 Miro Hrončok <mhroncok@redhat.com> - 191-1
- Require python-srpm-macros with Python related BuildRoot Policy scripts

* Wed Jun 30 2021 Miro Hrončok <mhroncok@redhat.com> - 190-1
- Move Python related BuildRoot Policy scripts from azurelinux-rpm-config to python-srpm-macros

* Mon Jun 28 2021 Ben Burton <bab@debian.org> - 189-1
- Adapt macros and BRP scripts for %%topdir with spaces
- Fixes rhbz#1947416

* Tue Jun 22 2021 Panu Matilainen <pmatilai@redhat.com> - 188-1
- Drop reference to now extinct brp-python-hardlink script

* Tue Jun 8 2021 Stephen Coady <scoady@redhat.com> - 187-1
- Add Requires: rpmautospec-rpm-macros

* Mon May 31 2021 Charalampos Stratakis <cstratak@redhat.com> - 186-1
- Enable RPATH check after %%install
- Part of https://fedoraproject.org/wiki/Changes/Broken_RPATH_will_fail_rpmbuild
- Resolves: rhbz#1964548

* Wed May 26 2021 Arjun Shankar <arjun@redhat.com> - 185-1
- Disable annobin on armv7hl

* Mon Apr 12 2021 David Benoit <dbenoit@redhat.com> - 184-1
- Change 'Requires: annobin' to 'Requires: annobin-plugin-gcc'.

* Tue Apr  6 2021 David Benoit <dbenoit@redhat.com> - 183-1
- BRP: LLVM Compile LTO Bitcode to ELF
- Add Requires: (llvm if clang)

* Mon Mar 22 2021 Lumír Balhar <lbalhar@redhat.com> - 182-1
- Fix handling of files without newlines in brp-mangle-shebang

* Wed Mar 10 2021 Kalev Lember <klember@redhat.com> - 181-1
- BRP Python Bytecompile: Avoid hardcoding /usr/bin prefix for python

* Tue Jan 19 2021 Florian Weimer <fweimer@redhat.com> - 180-1
- Use -march=x86-64-v2 only for the gcc toolchain

* Tue Jan 19 2021 Florian Weimer <fweimer@redhat.com> - 179-1
- x86_64: Enable -march=x86-64-v2 for ELN, following GCC.

* Sun Nov 29 2020 Miro Hrončok <mhroncok@redhat.com> - 178-1
- BRP Python Bytecompile: Also detect Python files in /app/lib/pythonX.Y

* Tue Oct 27 2020 Tom Stellard <tstellar@redhat.com> - 177-1
- Add back -fcf-protection flag for x86_64

* Tue Oct 20 2020 Florian Weimer <fweimer@redhat.com> - 176-1
- s390x: Tune for z14 (as in Red Hat Enterprise Linux 8)

* Mon Oct  5 2020 Florian Weimer <fweimer@redhat.com> - 175-1
- s390x: Switch Fedora ELN to z13 baseline

* Fri Sep 11 2020 Miro Hrončok <mhroncok@redhat.com> - 172-1
- Filter out LTO flags from %%extension flags macros
- Fixes: rhbz#1877652

* Wed Sep  2 2020 Michel Alexandre Salim <salimma@fedoraproject.org> - 171-1
- Add Requires: lua-srpm-macros

* Fri Aug 21 2020 Tom Stellard <tstellar@redhat.com> - 170-1
- Enable -fstack-clash-protection for clang on x86, s390x, and ppc64le

* Thu Aug 20 2020 Tom Stellard <tstellar@redhat.com> - 169-1
- Add -flto to ldflags for clang toolchain

* Thu Aug 20 2020 Neal Gompa <ngompa13@gmail.com> - 168-1
- Fix CC/CXX exports so arguments are included in exported variable
- Allow overrides of CC/CXX like CFLAGS and CXXFLAGS from shell variables

* Mon Aug 03 2020 Troy Dawson <tdawson@redhat.com> - 167-1
- Add Requires: kernel-srpm-macros

* Thu Jul 30 2020 Jeff Law <law@redhat.com> - 166-1
- Use -flto=auto for GCC to speed up builds

* Tue Jul 28 2020 Tom Stellard <tstellar@redhat.com> - 165-1
- Only use supported lto flags for clang toolchain

* Thu Jul 23 2020 Lumír Balhar <lbalhar@redhat.com> - 164-1
- Disable Python hash seed randomization in brp-python-bytecompile

* Tue Jul 21 2020 Jeff Law <law@redhat.com> - 163-1
- Enable LTO by default

* Thu Jul 16 2020 Lumír Balhar <lbalhar@redhat.com> - 162-1
- New script brp-fix-pyc-reproducibility

* Tue Jun 16 2020 Lumír Balhar <lbalhar@redhat.com> - 161-2
- Use stdlib compileall for Python >= 3.9

* Mon Jun 15 2020 Lumír Balhar <lbalhar@redhat.com> - 161-1
- No more automagic Python bytecompilation (phase 3)
  https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_3

* Thu Jun 04 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 160-1
- Fix broken %%configure

* Wed Jun 03 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 159-1
- Fixes for new_package macro

* Wed Jun 03 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 158-1
- Add option to choose C/C++ toolchain

* Sat May 30 2020 Jeff Law <law@redhat.com> - 157-1
- When LTO is enabled, fix broken configure files.

* Sat May 30 2020 Nicolas Mailhot <nim@fedoraproject.org> - 156-1
- Add new_package macro and associated lua framework.

* Sat May 23 2020 Nicolas Mailhot <nim@fedoraproject.org> - 155-1
- forge: add gitea support

* Thu Apr 09 2020 Panu Matilainen <pmatilai@redhat.com> - 154-1
- Optimize kernel module provides by using a parametric generator

* Thu Feb 20 2020 Jason L Tibbitts III <tibbs@math.uh.edu> - 153-1
- Add dependency on fonts-srpm-macros, as those have now been approved by FPC.

* Thu Feb 20 2020 Jeff Law <law@redhat.com> - 152-1
- Use eu-elfclassify to only run strip on ELF relocatables
  and archive libraries.

* Fri Feb 14 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 151-1
- Fixup parallel algorithm for brp-strip-lto

* Fri Feb 14 2020 Jeff Law <law@redhat.com> - 150-1
- Strip LTO sections/symbols from installed .o/.a files

* Thu Jan 23 2020 Jeff Law <law@redhat.com> - 149-1
- Allow conditionally adding -fcommon to CFLAGS by defining %%_legacy_common_support

* Mon Jan 20 2020 Florian Weimer <fweimer@redhat.com> - 148-1
- Reenable annobin after GCC 10 integration (#1792892)

* Mon Jan 20 2020 Florian Weimer <fweimer@redhat.com> - 147-1
- Temporarily disable annobin for GCC 10 (#1792892)

* Thu Dec 05 2019 Denys Vlasenko <dvlasenk@redhat.com> - 146-1
- kmod.prov: fix and speed it up

* Tue Dec 03 15:48:18 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 145-1
- %%set_build_flags: define LT_SYS_LIBRARY_PATH

* Thu Nov 21 2019 Denys Vlasenko <dvlasenk@redhat.com> - 144-1
- Speed up brp-mangle-shebangs.

* Tue Nov 05 2019 Lumír Balhar <lbalhar@redhat.com> - 143-1
- Fix brp-python-bytecompile with the new features from compileall2
- Resolves: rhbz#1595265

* Fri Nov 01 2019 Miro Hrončok <mhroncok@redhat.com> - 142-1
- Fix the simple API of %%gpgverify.

* Thu Aug 22 2019 Jason L Tibbitts III <tibbs@math.uh.edu> - 141-2
- Simplify the API of %%gpgverify.

* Thu Jul 25 2019 Richard W.M. Jones <rjones@redhat.com> - 140-2
- Bump version and rebuild.

* Sat Jul 20 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 140-1
- Fixup python-srpm-macros version

* Wed Jul 17 2019 Lumír Balhar <lbalhar@redhat.com> - 139-1
- Use compileall2 Python module for byte-compilation in brp-python-bytecompile

* Tue Jul 09 2019 Miro Hrončok <mhroncok@redhat.com> - 138-1
- Move brp-python-bytecompile from rpm, so we can easily adapt it

* Mon Jul 08 2019 Nicolas Mailhot <nim@fedoraproject.org> - 137-1
- listfiles: make it robust against all kinds of “interesting” inputs
- wordwrap: make list indenting smarter, to produce something with enough
  structure that it can be converted into AppStream metadata

* Mon Jul 08 2019 Robert-André Mauchin <zebob.m@gmail.com> - 136-1
- Revert "Fix expansion in listfiles_exclude/listfiles_include"

* Mon Jul 08 2019 Nicolas Mailhot <nim@fedoraproject.org> - 135-1
- Fix expansion in listfiles_exclude/listfiles_include

* Mon Jul 01 2019 Florian Festi <ffesti@redhat.com> - 134-1
- Switch binary payload compression to Zstandard level 19

* Thu Jun 27 2019 Vít Ondruch <vondruch@redhat.com> - 133-2
- Enable RPM to set SOURCE_DATE_EPOCH environment variable.

* Tue Jun 25 08:13:50 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 133-1
- Expand listfiles_exclude/listfiles_include

* Tue Jun 11 2019 Jitka Plesnikova <jplesnik@redhat.com> - 132-1
- Remove perl macro refugees

* Mon Jun 10 2019 Panu Matilainen <pmatilai@redhat.com> - 131-1
- Provide temporary shelter for rpm 4.15 perl macro refugees

* Tue Jun 04 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 130-1
- New macro for wrapping text — %%wordwrap
- Smal fix for %%listfiles with no arguments

* Thu May 30 2019 Björn Persson <Bjorn@Rombobjörn.se> - 129-1
- Added gpgverify.

* Tue Jan 15 2019 Panu Matilainen <pmatilai@redhat.com> - 128-1
- Drop redundant _smp_mflag re-definition, use the one from rpm instead

* Thu Dec 20 2018 Florian Weimer <fweimer@redhat.com> - 127-1
- Build flags: Add support for extension builders (#1543394)

* Mon Dec 17 2018 Panu Matilainen <pmatilai@redhat.com> - 126-1
- Silence the annoying warning from ldconfig brp-script (#1540971)

* Thu Nov 15 2018 Miro Hrončok <mhroncok@redhat.com> - 125-1
- Make automagic Python bytecompilation optional
  https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_2

* Thu Nov 08 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 124-1
- forge: add more distprefix cleaning (bz1646724)

* Mon Oct 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 123-1
- Add -q option to %%forgesetup

* Sat Oct 20 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 122-1
- Allow multiple calls to forge macros

* Thu Oct 11 2018 Jan Pazdziora <jpazdziora@redhat.com> - 121-1
- Add %_swidtagdir for directory for SWID tag files describing the
  installation.

* Mon Sep 10 2018 Miro Hrončok <mhroncok@redhat.com> - 120-1
- Make ambiguous python shebangs error
  https://fedoraproject.org/wiki/Changes/Make_ambiguous_python_shebangs_error

* Mon Aug 20 2018 Kalev Lember <klember@redhat.com> - 119-1
- Add aarch64 to ldc arches

* Wed Aug 15 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 118-1
- Enable --as-needed by default

* Mon Jul 16 2018 Miro Hrončok <mhroncok@redhat.com> - 117-1
- Mangle /bin shebnags to /usr/bin ones (#1581757)

* Tue Jul 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 116-1
- Add option to add -Wl,--as-needed into LDFLAGS

* Mon Jul 09 2018 Kalev Lember <klember@redhat.com> - 115-1
- Disable non-functional ppc64 support for ldc packages

* Tue Jun 26 2018 Panu Matilainen <pmatilai@redhat.com> - 114-1
- Fix kernel ABI related strings (Peter Oros, #26)
- Automatically trim changelog to two years (Zbigniew Jędrzejewski-Szmek, #22)
- Cosmetics cleanups (Zbigniew Jędrzejewski-Szmek, #22)

* Mon Jun 18 2018 Florian Weimer <fweimer@redhat.com> - 113-1
- Build flags: Require SSE2 on i686 (#1592212)

* Mon May 28 2018 Miro Hrončok <mhroncok@redhat.com> - 112-1
- Add a possibility to opt-out form automagic Python bytecompilation
  https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation

* Wed May 02 2018 Peter Jones <pjones@redhat.com> - 111-1
- brp-mangle-shebangs: add %%{__brp_mangle_shebangs_exclude_file} and
  %%{__brp_mangle_shebangs_exclude_from_file} to allow you to specify files
  containing the shebangs to be ignore and files to be ignored regexps,
  respectively, so that they can be generated during the package build.

* Wed May  2 2018 Florian Weimer <fweimer@redhat.com> - 110-1
- Reflect -fasynchronous-unwind-tables GCC default on POWER (#1550914)

* Wed May  2 2018 Florian Weimer <fweimer@redhat.com> - 109-1
- Use plain -fcf-protection compiler flag, without -mcet (#1570823)

* Tue May 01 2018 Peter Jones <pjones@redhat.com> - 108-1
- Add Requires: efi-srpm-macros for %%{efi}

* Fri Apr 20 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 107-1
- Add %%_metainfodir macro.
- %%forgeautosetup tweak to fix patch application.

* Mon Mar 05 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 106-1
- Update forge macros.

* Wed Feb 28 2018 Florian Weimer <fweimer@redhat.com> - 105-1
- Make -fasynchronous-unwind-tables explicit on aarch64 (#1536431)

* Wed Feb 28 2018 Florian Weimer <fweimer@redhat.com> - 104-1
- Use -funwind-tables on POWER (#1536431, #1548847)

* Sun Feb 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 103-1
- Make %%ldconfig_post/%%ldconfig_postun parameterized

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 102-1
- Second step of -z now move: removal from GCC specs file (#1548397)

* Sat Feb 24 2018 Florian Weimer <fweimer@redhat.com> - 101-1
- First step of moving -z now to the gcc command line (#1548397)

* Thu Feb 22 2018 Miro Hrončok <mhroncok@redhat.com> - 100-1
- Don't mangle shebangs with whitespace only changes (#1546993)

* Thu Feb 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 99-1
- Move %%end to %%ldconfig_scriptlets

* Sat Feb 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 98-1
- Explicitly close scriptlets with %%end (ldconfig)

* Wed Feb 14 2018 Miro Hrončok <mhroncok@redhat.com> - 97-1
- Allow to opt-out from shebang mangling for specific paths/shebangs

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 96-1
- Simplify/Fix check for shebang starting with "/"

* Wed Feb 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 95-1
- Fix mangling env shebangs with absolute paths

* Sun Feb  4 2018 Florian Weimer <fweimer@redhat.com> - 94-1
- Add RPM macros for compiler/linker flags

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 93-1
- Use newly available /usr/bin/grep

* Wed Jan 31 2018 Peter Robinson <pbrobinson@fedoraproject.org> 92-1
- Use generic tuning for ARMv7

* Tue Jan 30 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 91-1
- The grep package only provides /bin/grep, not /usr/bin/grep.

* Mon Jan 29 2018 Miro Hrončok <mhroncok@redhat.com> - 90-1
- Add brp-mangle-shebangs

* Mon Jan 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 89-1
- Add macros.ldconfig

* Mon Jan 29 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 88-1
- Create DSO symlinks automatically

* Mon Jan 29 2018 Florian Weimer <fweimer@redhat.com> - 87-1
- Build flags: Disable -z defs again (#1535422)

* Mon Jan 29 2018 Florian Weimer <fweimer@redhat.com> - 86-1
- Build flags: Enable CET on i686, x86_64 (#1538725)

* Thu Jan 25 2018 Florian Weimer <fweimer@redhat.com> - 85-1
- Build flags: Switch to generic tuning on i686 (#1538693)

* Mon Jan 22 2018 Florian Weimer <fweimer@redhat.com> - 84-1
- Link with -z defs by default (#1535422)

* Mon Jan 22 2018 Florian Weimer <fweimer@redhat.com> - 83-1
- Make armhfp flags consistent with GCC defaults

* Mon Jan 22 2018 Florian Weimer <fweimer@redhat.com> - 82-1
- Make use of -fasynchronous-unwind-tables more explicit (#1536431)

* Mon Jan 22 2018 Florian Weimer <fweimer@redhat.com> - 81-1
- Remove --param=ssp-buffer-size=4

* Mon Jan 22 2018 Florian Weimer <fweimer@redhat.com> - 80-1
- Document build flags

* Fri Jan 19 2018 Panu Matilainen <pmatilai@redhat.com> - 79-1
- Document how to disable hardened and annotated build (#1211296)

* Wed Jan 17 2018 Panu Matilainen <pmatilai@redhat.com> - 78-1
- Fix the inevitable embarrassing typo in 77, doh

* Wed Jan 17 2018 Panu Matilainen <pmatilai@redhat.com> - 77-1
- Macroize build root policies for consistent disable/override ability

* Wed Jan 17 2018 Florian Weimer <fweimer@redhat.com> - 76-1
- Add -fstack-clash-protection for supported architectures (#1515865)

* Wed Jan 17 2018 Florian Weimer <fweimer@redhat.com> - 75-1
- Add _GLIBCXX_ASSERTIONS to CFLAGS/CXXFLAGS (#1515858)

* Mon Jan 15 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 74-1
- Remove Requires: cmake-rpm-macros

* Thu Jan 11 2018 Jason L Tibbitts III <tibbs@math.uh.edu> - 73-1
- Add macros.forge for simplifying packaging of forge-hosted packages.  See
  https://fedoraproject.org/wiki/Forge-hosted_projects_packaging_automation and
  https://bugzilla.redhat.com/show_bug.cgi?id=1523779

* Wed Jan 03 2018 Sergey Avseyev <sergey.avseyev@gmail.com> - 72-1
- Add Requires: nim-srpm-macros for %%nim_arches

* Tue Jan 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 71-1
- Require annobin only if gcc is installed

* Thu Dec 21 2017 Björn Esser <besser82@fedoraproject.org> - 70-2
- Add Requires: cmake-rpm-macros for CMake auto-{provides,requires} (#1498894)

* Fri Dec 08 2017 Panu Matilainen <pmatilai@redhat.com> - 70-1
- Update URL to current location at src.fedoraproject.org

* Wed Nov 22 2017 Nick Clifton <nickc@redhat.com> - 69-1
- Enable binary annotations in compiler flags

* Thu Oct 26 2017 Troy Dawson <tdawson@redhat.com> - 68-1
- Remove Requires: fedora-rpm-macros

* Mon Jul 31 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 67-1
- Define _include_gdb_index (RHBZ #1476722)
- Move _debuginfo_subpackages and _debugsource_packages from rpm (RHBZ #1476735)

* Tue Jul 18 2017 Florian Festi <ffesti@redhat.com> - 66-1
- Honor %%kmodtool_generate_buildreqs (#1472201)

* Thu Jul 13 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 65-1
- Add Requires: rust-srpm-macros for %%rust_arches

* Wed Mar 15 2017 Orion Poplawski <orion@cora.nwra.com> - 64-1
- Add Requires: openblas-srpm-macros for %%openblas_arches

* Thu Feb 02 2017 Dan Horák <dan[at]danny.cz> - 63-1
- set zEC12 as minimum architecture level for s390(x) (#1404991)

* Thu Dec 15 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 62-1
- Add macros.vpath (https://fedorahosted.org/fpc/attachment/ticket/655)

* Tue Dec 06 2016 Adam Williamson <awilliam@redhat.com> - 61-1
- revert changes from 60, they break far too much stuff (#1401231)

* Wed Nov 30 2016 Panu Matilainen <pmatilai@redhat.com> - 60-1
- Error on implicit function declaration and -return type for C (#1393492)

* Wed Nov 30 2016 Panu Matilainen <pmatilai@redhat.com> - 59-1
- Move global compiler flags to __global_compiler_flags macro
- Introduce separate __global_fooflags for C, C++ and Fortran

* Tue Nov 29 2016 Panu Matilainen <pmatilai@redhat.com> - 58-1
- Drop atom optimization on i686 (#1393492)

* Tue Nov 15 2016 Dan Horák <dan[at]danny.cz> - 57-1
- set z10 as minimum architecture level for s390(x)

* Fri Nov 11 2016 Panu Matilainen <pmatilai@redhat.com> - 56-1
- Fix directory name mismatch in kernel_source macro (#648996)

* Tue Nov 08 2016 Michal Toman <mtoman@fedoraproject.org> - 55-1
- Add default compiler flags for various MIPS architectures (#1366735)

* Tue Nov 08 2016 Panu Matilainen <pmatilai@redhat.com> - 54-1
- -pie is incompatible with static linkage (#1343892, #1287743)

* Mon Nov 07 2016 Panu Matilainen <pmatilai@redhat.com> - 53-1
- Drop brp-java-repack-jars by request (#1235770)
- Drop brp-implant-ident-static, unused for 13 years and counting

* Mon Nov 07 2016 Lubomir Rintel <lkundrak@v3.sk> - 52-1
- Add valgrind_arches macro for BuildRequires of valgrind

* Fri Nov 04 2016 Stephen Gallagher <sgallagh@redhat.com> - 51-1
- Add s390x build target for Node.js packages

* Mon Oct 31 2016 Kalev Lember <klember@redhat.com> - 50-1
- Add ldc_arches macro

* Mon Oct 17 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 49-1
- Remove hardcoded limit of 16 CPUs for makefile parallelism.
- See https://bugzilla.redhat.com/show_bug.cgi?id=1384938

* Thu Oct 13 2016 Richard W.M. Jones <rjones@redhat.com> 48-1
- Add support for riscv64.
  This also updates config.sub/config.guess to the latest upstream versions.

* Wed Oct 12 2016 Peter Robinson <pbrobinson@fedoraproject.org> 47-1
- Enable aarch64 for mono arches

* Mon Oct 03 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 46-1
- Allow %%configure to optionally pass --disable-silent-rules.  Define
  %%_configure_disable_silent_rules (defaulting to 0) to control this.

* Wed Sep 14 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 45-1
- Add dependency on qt5-srpm-macros.

* Fri Aug 12 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 44-1
- And somehow I managed to make a typo in that dependency.

* Fri Aug 12 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 43-1
- Add dependency on fedora-rpm-macros.

* Tue Apr 12 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 42-1
- Add dependency on fpc-srpm-macros.

* Mon Apr 11 2016 Jason L Tibbitts III <tibbs@math.uh.edu> - 41-1
- Add a file for miscellaneous macros, currently containing just %%rpmmacrodir.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Feb 02 2016 Dan Horák <dan[at]danny.cz> 40-1
- switch to -mcpu=power8 for ppc64le default compiler flags

* Wed Jan 13 2016 Orion Poplawski <orion@cora.nwra.com> 39-1
- Add Requires: python-srpm-macros

* Fri Jan  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 38-1
- Add missing ARMv6 optflags

* Wed Dec  2 2015 Peter Robinson <pbrobinson@fedoraproject.org> 37-1
- nodejs 4+ now supports aarch64 and power64

* Fri Jul 17 2015 Florian Festi <ffesti@redhat.com> 36-1
- Add Requires: go-srpm-macros (#1243922)

* Thu Jul 09 2015 Sandro Mani <manisandro@gmail.com> 35-1
- Use %%__libsymlink_path instead of %%__libsymlink_exclude_path in libsymlink.attr

* Wed Jul 08 2015 Adam Jackson <ajax@redhat.com> 34-1
- Fix cc1 specs mishandling of incremental linking

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Dan Horák <dan[at]danny.cz> 33-1
- Mono 4 adds support for ppc64le

* Fri May 29 2015 Florian Festi <ffesti@redhat.com> 32-1
- Support out of source builds for %%_configure_gnuconfig_hack (#1191788)
- Fix typo in %%kernel_module_package (#1159361)

* Tue May 19 2015 Florian Festi <ffesti@redhat.com> 31-1
- Add %%py_auto_byte_compile macro controlling Python bytecompilation
(#976651)

* Wed Apr 29 2015 Florian Festi <ffesti@redhat.com> 30-1
- Fix libsymlink.attr for new magic pattern for symlinks (#1207945)

* Wed Apr 08 2015 Adam Jackson <ajax@redhat.com> 29-1
- Fix ld specs mishandling of incremental linking

* Thu Feb 19 2015 Till Maas <opensource@till.name> - 28-1
- Enable harden flags by default (#1192183)

* Wed Dec 10 2014 Dan Horák <dan[at]danny.cz> - 27-1
- Explicitly set -mcpu/-mtune for ppc64p7 and ppc64le to override rpm defaults

* Mon Sep 22 2014 Panu Matilainen <pmatilai@redhat.com> - 26-1
- Gnat macros are now in a package of their own (#1133632)

* Fri Sep 19 2014 Dan Horák <dan[at]danny.cz> - 25-1
- there is still no properly packaged Mono for ppc64le

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jun  5 2014 Peter Robinson <pbrobinson@fedoraproject.org> 24-1
- ARMv7 has Ada so add it to GNAT_arches

* Sat May 24 2014 Brent Baude <baude@us.ibm.com> - 23-2
- Changed ppc64 to power64 macro for mono_archs

* Tue May 13 2014 Peter Robinson <pbrobinson@fedoraproject.org>
- aarch64 has Ada so add it to GNAT_arches

* Mon May 12 2014 Josh Boyer <jwboyer@fedoraproject.org> - 22-1
- Fix kmod.prov to deal with compressed modules (#1096349)

* Wed Apr 30 2014 Jens Petersen <petersen@redhat.com> - 21-1
- macros.ghc-srpm moved to ghc-rpm-macros package (#1089102)
- add requires ghc-srpm-macros

* Tue Apr 29 2014 Peter Robinson <pbrobinson@fedoraproject.org> 20-1
- With gcc 4.9 aarch64 now supports stack-protector

* Sun Apr 27 2014 Ville Skyttä <ville.skytta@iki.fi> - 19-1
- Drop bunch of duplicated-with-rpm macro definitions and brp-* scripts

* Tue Apr 15 2014  Panu Matilainen <pmatilai@redhat.com> - 18-1
- Temporarily bring back find-requires and -provides scripts to rrc-side

* Tue Apr 15 2014  Panu Matilainen <pmatilai@redhat.com> - 17-1
- Let OCaml handle its own arch macros (#1087794)

* Tue Apr 15 2014  Panu Matilainen <pmatilai@redhat.com> - 16-1
- Move kmod and libsymlink dependency generators here from rpm

* Thu Apr 10 2014  Panu Matilainen <pmatilai@redhat.com> - 15-1
- Drop most of the script-based dependency generation bits

* Tue Apr 08 2014  Panu Matilainen <pmatilai@redhat.com> - 14-1
- Add Mono path macros (#1070936)
- Allow opting out of config.{guess,sub} replacement hack (#991613)

* Tue Apr 08 2014  Panu Matilainen <pmatilai@redhat.com> - 13-1
- Move the remaining dependency generator stuff to the kmp macro package
- Stop overriding rpm external dependency generator settings by default

* Mon Apr 07 2014  Panu Matilainen <pmatilai@redhat.com> - 12-1
- Be more explicit about the package contents
- Split kernel module macros to a separate file
- Split kernel module scripts and macros to a separate package

* Wed Apr 02 2014  Panu Matilainen <pmatilai@redhat.com> - 11-1
- Stop pretending this package is relocatable, its not
- Require rpm >= 4.11 for /usr/lib/rpm/macros.d support etc
- Move our macros out of from /etc, they're not configuration

* Wed Apr 02 2014  Panu Matilainen <pmatilai@redhat.com> - 10-1
- Make fedora dist-git the upstream of this package and its sources
- Add maintainer comments to spec wrt versioning and changes

* Mon Mar 24 2014 Dan Horák <dan[at]danny.cz> - 9.1.0-58
- enable ppc64le otherwise default rpm cflags will be used

* Fri Feb 07 2014 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-57
- config.guess/sub don't need to be group-writable (#1061762)

* Sun Jan 12 2014 Kevin Fenzi <kevin@scrye.com> 9.1.0-56
- Update libtool hardening hack and re-enable (#978949)

* Wed Dec 18 2013 Dhiru Kholia <dhiru@openwall.com> - 9.1.0-55
- Enable "-Werror=format-security" by default (#1043495)

* Wed Sep 04 2013 Karsten Hopp <karsten@redhat.com> 9.1.0-54
- update config.sub with ppc64p7 support (from Fedora automake)

* Fri Aug 16 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-53
- updated config.guess/sub from upstream for little-endian ppc archs

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 9.1.0-52
- Perl 5.18 rebuild

* Thu Jul 25 2013 Tomas Mraz <tmraz@redhat.com> 9.1.0-51
- Disable the libtool hack as it is breaking builds

* Wed Jul 24 2013 Kevin Fenzi <kevin@scrye.com> 9.1.0-50
- Make docdirs unversioned on Fedora 20+ (#986871)
- Hack around libtool issue for hardened build for now (#978949)

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 9.1.0-49
- Perl 5.18 rebuild

* Fri Jul 05 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-48
- fix brp-java-repack-jars failing on strange permissions (#905573)

* Thu Jul 04 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-47
- switch from -fstack-protector to -fstack-protector-strong (#978763)

* Thu Jun 27 2013 Panu Matilainen <pmatilai@redhat.com> - - 9.1.0-46
- make cpu limit for building configurable through _smp_ncpus_max macro

* Tue May 21 2013 T.C. Hollingsworth <tchollingsworth@gmail.com> - 9.1.0-45
- add nodejs_arches macro for ExclusiveArch for Node.js packages

* Mon May 13 2013 Adam Jackson <ajax@redhat.com> 9.1.0-44
- redhat-config-*: Use + to append rather than %%rename, to protect against
  multiple -specs= ending up in the command line. (#892837)

* Tue Apr 23 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-43
- Add optflags stack protector override for AArch64 (#909788)
- Also set FCFLAGS from %%configure (#914831)

* Mon Apr 22 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-42
- Switch back to manual config.guess/sub copies for reproducability
- Replace config.guess/sub from %%configure again (#951442)

* Mon Apr 22 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-41
- Add -grecord-gcc-switches to global CFLAGS (#951669)

* Mon Mar 25 2013 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-40
- Add virtual system-rpm-config provide

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.0-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Nov 17 2012 Jens Petersen <petersen@redhat.com> - 9.1.0-38
- add ARM to ghc_arches_with_ghci for ghc-7.4.2 ghci support
  (NB this change should not be backported before ghc-7.4.2)

* Fri Nov  9 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 9.1.0-37
- Patch to fix spaces in java jar files
  https://bugzilla.redhat.com/show_bug.cgi?id=872737

* Fri Nov  9 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 9.1.0-36
- Patch to fix spaces in files used in filtering macros
  https://bugzilla.redhat.com/show_bug.cgi?id=783932

* Wed Oct  3 2012 Ville Skyttä <ville.skytta@iki.fi> - 9.1.0-35
- Drop (un)setting LANG and DISPLAY in build stages, require rpm >= 4.8.0.

* Wed Oct  3 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 9.1.0-34
- Add patch from https://bugzilla.redhat.com/show_bug.cgi?id=783433
  to fix spaces in files and directories that are fed to the
  brp-python-hardlink script
- Require zip since java repack jars requires it
  https://bugzilla.redhat.com/show_bug.cgi?id=857479
- Java jars need the MANIFEST.MF file to be first in the archive
  https://bugzilla.redhat.com/show_bug.cgi?id=465664
- Fix kernel_source macro to match the directory that kernel sources are installed in
  https://bugzilla.redhat.com/show_bug.cgi?id=648996
- Patch _mandir, _infodir, and _defaultocdir to use _prefix
  https://bugzilla.redhat.com/show_bug.cgi?id=853216

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.0-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 27 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-32
- enable minidebuginfo generation (#834073)

* Mon Jun 25 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-31
- revert back to plain -g, -g3 seems to cancel dwz size improvements

* Mon Jun 25 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-30
- require dwz, enable dwarf compression for debuginfo packages (#833311)

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 9.1.0-29
- Pull in dependency with macros specific for building Perl source packages

* Sat Mar  3 2012 Jens Petersen <petersen@redhat.com> - 9.1.0-28
- add s390 and s390x to ghc_arches

* Wed Feb 22 2012 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-27
- add GNAT arch definitions

* Sun Jan 15 2012 Dennis Gilmore <dennis@ausil.us> - 9.1.0-26
- per ppc team request drop -mminimal-toc on ppc64

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.1.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-24
- add ghc_arches_with_ghci

* Wed Nov 09 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-23
- remove patch that forces --disable-silent-rules to configure
- it breaks anything set to not ignore unknown configure options

* Tue Oct 18 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-22
- add armv5tel to ghc_arches

* Wed Sep 28 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-21
- build armv5tel on armv7l since they are the same abi armv7hl is
  an incompatible ABI

* Wed Sep 28 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-20
- add armv7hl to ghc_arches

* Sun Sep 25 2011 Ville Skyttä <ville.skytta@iki.fi> - 9.1.0-19
- Fix URL.

* Thu Sep 22 2011 Adam Jackson <ajax@redhat.com> 9.1.0-18
- redhat-hardened-cc1: Inject -fPIE, not -fPIC.
  cf. http://lists.fedoraproject.org/pipermail/devel/2011-September/157365.html

* Fri Sep 16 2011 Adam Jackson <ajax@redhat.com> 9.1.0-17
- Expose %%_hardening_{c,ld}flags independently to make it easier for
  packages to apply them to selected components

* Wed Aug 10 2011 Colin Walters <walters@verbum.org> - 9.1.0-16
- Globally disable silent rules

* Wed Aug 03 2011 Adam Jackson <ajax@redhat.com> 9.1.0-15
- redhat-hardened-{cc1,ld}: Move some of the rewrite magic to gcc specs so
  we don't end up with both -fPIC and -fPIE on the command line

* Mon Aug 01 2011 Adam Jackson <ajax@redhat.com> 9.1.0-14
- azurelinux-rpm-config-9.1.0-hardened.patch: Add macro magic for %%_hardened_build

* Thu Jul 07 2011 Adam Jackson <ajax@redhat.com> 9.1.0-13
- azurelinux-rpm-config-9.1.0-relro.patch: LDFLAGS, not CFLAGS.

* Sat Jul 02 2011 Jon Masters <jcm@jonmasters.org> - 9.1.0-12
- azurelinux-rpm-config-9.1.0-arm.patch: Make armv7hl default on all v7 ARM

* Mon Jun 27 2011 Adam Jackson <ajax@redhat.com> - 9.1.0-11
- azurelinux-rpm-config-9.1.0-relro.patch: Add -Wl,-z,relro to __global_cflags

* Tue Jun 21 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-10
- revert last build since releng prefers exclusivearch here

* Sat Jun 18 2011 Jens Petersen <petersen@redhat.com> - 9.1.0-9
- replace ghc_archs with ghc_excluded_archs

* Mon Jun 13 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-8
- add arm hardware float macros, fix up armv7l

* Mon May 30 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-7
- add -srpm to the arches files so that the base language macros can
  be parallel installable with these

* Fri May 27 2011 Dennis Gilmore <dennis@ausil.us> - 9.1.0-6
- add some specific macros needed at srpm creation time

* Thu May 27 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-5
- adjust to new pkg-config behavior wrt private dependencies (#596433)

* Mon Mar 01 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-4
- avoid unnecessarily running brp-strip-comment-note (#568924)

* Mon Feb 15 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-3
- unbreak find-requires again, doh (#564527)

* Wed Feb 3 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-2
- python byte-compilation errors abort the build by default

* Tue Feb 2 2010 Panu Matilainen <pmatilai@redhat.com> - 9.1.0-1
- new version, lose merged patches (fixes #521141, #455279, #496522, #458648)
- require rpm for parent dir, version >= 4.6.0 for sane keyserver behavior
- buildrequire libtool to grab copies of config.guess and config.sub
- add URL to the git repo and upstream changelog as documentation

* Mon Nov 23 2009 Orion Poplawski <orion@cora.nwra.com> - 9.0.3-19
- Change configure macro to use _configure to allow override (bug #489942)

* Mon Sep 28 2009 Bill Nottingham <notting@redhat.com>
- Drop xz compression level to 2

* Thu Sep 03 2009 Adam Jackson <ajax@redhat.com>
- Delete *.orig in %%install

* Thu Sep 03 2009 Paul Howarth <paul@city-fan.org> 9.0.3-17
- azurelinux-rpm-config-9.0.3-filtering-macros.patch: Rediff so we don't ship a .orig file
- add (empty) %%build section
- fix unescaped macros in changelog

* Tue Aug 18 2009 Chris Weyl <cweyl@alumni.drew.edu> 9.0.3-16
- add the filtering framework approved by the FPC/FESCo. (#516240)

* Thu Aug 13 2009 Adam Jackson <ajax@redhat.com> 9.0.3-15
- azurelinux-rpm-config-9.0.4-brpssa-speedup.patch: When looking for static
  archives, only run file(1) on files named *.a. (#517101)

* Wed Aug 12 2009 Adam Jackson <ajax@redhat.com> 9.0.3-14
- azurelinux-rpm-config-9.0.3-jars-with-spaces.patch: Handle repacking jars
  whose filenames contain spaces. (#461854)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Bill Nottingham <notting@redhat.com> 9.0.3-12
- use XZ payload compression for binary packages

* Tue Jul 21 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 9.0.3-10
- always delete %%buildroot as first step of %%install (as long as %%buildroot is not /)

* Fri Jul 17 2009 Bill Nottingham <notting@redhat.com> 9.0.3-10
- apply fedora 12 default buildflags

* Wed Jun 03 2009 Adam Jackson <ajax@redhat.com> 9.0.3-9
- limit-smp-16-threads.patch: Rediff so we don't ship a .orig file (#500316)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 9.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Jon Masters <jcm@redhat.com> - 9.0.3-7
- Change default hashing algorithm in file digests to SHA-256
- Resolves: #485826.

* Tue Feb 17 2009 Dennis Gilmore <dennis@ausil.us> - 9.0.3-6
- add missing armv7l arch
- set the default build arch to match fedora arm build target

* Mon Feb 16 2009 Dennis Gilmore <dennis@ausil.us> - 9.0.3-5
- apply fedora 11 default buildflags
- set 32 bit intel build arch to i586 on compatible hardware
- set 32 bit sparc build arch to sparcv9 on compatible hardware

* Mon Feb 16 2009 Dennis Gilmore <dennis@ausil.us> - 9.0.3-4
- limit _smp_flags to -j16

* Wed Sep  3 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 9.0.3-3
- fix license tag
- nuke ancient conflicts

* Mon Aug 11 2008 Panu Matilainen <pmatilai@redhat.com> - 9.0.3-2
- Unbreak find-requires (#443015)

* Tue May 06 2008 Jon Masters <jcm@redhat.com> - 9.0.3-1
- Ensure Java Jar files have readable files within.
- Remove overwritten config.guess|sub files (testing).
- Fix Fortran flags for building using _fmoddir.
- Pull in objdump fix to upstream find-requires.

* Thu Apr 03 2008 Jon Masters <jcm@redhat.com> - 9.0.2-1
- Remove smp dependencies
- Update config.guess|sub files
- Don't call find-requires.ksyms for kmod packages (kernel kABI scripts).

* Thu Jul 05 2007 Jesse Keating <jkeating@redhat.com> - 9.0.1-1
- Remove dist defines, fedora-release does that now
- Enable post-build buildroot checking by default

* Tue Jun 19 2007 Jeremy Katz <katzj@redhat.com> - 9.0.0-1
- use stock find-lang.sh (#213041)
- arm fixes (Lennert Buytenhek, #243523)
- allow jar repacking to be disabled (#219731)
- fix running dist.sh --fc (#223651)
- hardlink identical .pyc and .pyo files to save space (Ville Skyttä)
- fix TMPDIR usage (Matthew Miller, #235614)

* Tue Jun 19 2007 Jeremy Katz <katzj@redhat.com> - 8.1.0-1
- add modalias tags to kmod packages and other kmod changes (jcm)
- recompress jars to avoid multilib conflicts (bkonrath)

* Fri May 18 2007 Jesse Keating <jkeating@redhat.com> 8.0.45-16
- Update macros for F8
- hardcode dist in release string, as we provide it.  chicken/egg.

* Wed Apr 11 2007 Jon Masters <jcm@redhat.com> 8.0.45-15
- Add modalias tags to kernel module packages (kmods) for tracking.
- Further information is available at http://www.kerneldrivers.org/.

* Tue Apr 03 2007 Jon Masters <jcm@redhat.com> 8.0.45-14
- Rebased all previous patches (since java fix introduced offset).
- Added Fedora per-release macros to platforms section of macros.
  Further debate may see these move elsewhere in the ordering.

* Tue Mar 13 2007 Ben Konrath <bkonrath@redhat.com> 8.0.45-13
- Update brp-java-repack-jars to fix issue with tomcat.

* Wed Oct 18 2006 Jon Masters <jcm@redhat.com> 8.0.45-12
- Synced kernel_module_package semantics with SuSE.
- Updated kmodtool.

* Tue Oct 17 2006 Jon Masters <jcm@redhat.com> 8.0.45-10
- Updated kernel_module_package.

* Mon Oct 16 2006 Jon Masters <jcm@redhat.com> 8.0.45-9
- Added kernel_module_package macro. Working on unified packaging.

* Thu Oct 12 2006 Jon Masters <jcm@redhat.com> 8.0.45-8
- Added patch for find-requires. Waiting on write access to public CVS.

* Tue Sep 12 2006 Deepak Bhole <dbhole@redhat.com> 8.0.45-6
- Fix brp-java-repack-jars to work with builddirs that aren't %%name-%%version

* Mon Sep 11 2006 Fernando Nasser <fnasser@redhat.com> - 8.0.45-5
- Fix order of tokens in find command (thanks mikeb@redhat.com)

* Thu Sep  7 2006 Ben Konrath <bkonrath@redhat.com> - 8.0.45-4
- Fix bug in repack jars script.

* Wed Sep  6 2006 Jeremy Katz <katzj@redhat.com> - 8.0.45-3
- path fix

* Tue Sep  5 2006 Jeremy Katz <katzj@redhat.com> - 8.0.45-2
- Add script from Ben Konrath <bkonrath@redhat.com> to repack jars to
  avoid multilib conflicts

* Sun Jul 30 2006 Jon Masters <jcm@redhat.com> - 8.0.45-1
- Fix inverted kernel test.

* Sun Jul 30 2006 Jon Masters <jcm@redhat.com> - 8.0.44-1
- Add a better check for a kernel vs. kmod.

* Thu Jun 15 2006 Jon Masters <jcm@redhat.com> - 8.0.43-1
- Workaround bug in find-requires/find-provides for kmods.

* Thu Jun 15 2006 Jon Masters <jcm@redhat.com> - 8.0.42-1
- Fix a typo in KMP find-requires.

* Tue Jun 13 2006 Jon Masters <jcm@redhat.com> - 8.0.41-1
- Add support for KMP Fedora Extras packaging.

* Fri Feb  3 2006 Jeremy Katz <katzj@redhat.com> - 8.0.40-1
- use -mtune=generic for x86 and x86_64

* Tue Aug 16 2005 Elliot Lee <sopwith@redhat.com> - 8.0.39-1
- Fix #165416

* Mon Aug 01 2005 Elliot Lee <sopwith@redhat.com> - 8.0.38-1
- Add -Wall into cflags

* Mon Aug 01 2005 Elliot Lee <sopwith@redhat.com> - 8.0.37-1
- Patch from Uli: enable stack protector, fix sparc & ppc cflags

* Thu Jun 16 2005 Elliot Lee <sopwith@redhat.com> - 8.0.36-1
- Fix the fix

* Wed Apr  6 2005 Elliot Lee <sopwith@redhat.com> - 8.0.35-1
- Fix #129025 (enable python byte compilation)

* Wed Mar 23 2005 Elliot Lee <sopwith@redhat.com> 8.0.34-1
- Bug fixes
- Cflags change by drepper

* Wed Feb 9 2005 Elliot Lee <sopwith@redhat.com> 8.0.33-1
- Change -D to -Wp,-D to make java happy
- Add -D_FORTIFY_SOURCE=2 to global cflags (as per Jakub & Arjan's request)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 8.0.32-1
- allow all symbol versioning in find_requires - matches RPM internal
  behavior

* Mon Jun 28 2004 Elliot Lee <sopwith@redhat.com> 8.0.31-1
- Add ppc8[25]60 to rpmrc optflags

* Fri Jun 25 2004 Elliot Lee <sopwith@redhat.com> 8.0.29-1
- rpmrc patch from jakub to change optflags.

* Wed Sep 17 2003 Elliot Lee <sopwith@redhat.com> 8.0.28-1
- Change brp-compress to pass -n flag to gzip (per msw's request)

* Tue Jul 15 2003 Elliot Lee <sopwith@redhat.com> 8.0.27-1
- Fix broken configure macro find for config.guess/config.sub
- Put host/target/build back for now

* Mon Jul  7 2003 Jens Petersen <petersen@redhat.com> - 8.0.26-1
- preserve the vendor field when VENDOR not set
- put VENDOR in the final i386-libc line, not the tentative one

* Mon Jul  7 2003 Jens Petersen <petersen@redhat.com> - 8.0.25-1
- update config.{guess,sub} to 2003-06-17
- define VENDOR to be redhat only when /etc/redhat-release present
  [suggested by jbj]
- put VENDOR in vendor field in our config.guess file for
  ia64, ppc, ppc64, s390, s390x, x86_64 and elf32-i386 Linux
- drop the --host, --build, --target and --program-prefix configure options
  from %%configure, since this causes far too many problems

* Fri May  2 2003 Jens Petersen <petersen@redhat.com> - 8.0.24-3
- make config.{guess,sub} executable

* Thu May  1 2003 Jens Petersen <petersen@redhat.com> - 8.0.22-2
- add config.guess and config.sub (2003-02-22) with s390 patch on config.sub
- make %%configure use them

* Mon Mar 03 2003 Elliot Lee <sopwith@redhat.com>
- Unset $DISPLAY in macros

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com> 8.0.21-1
- Just turn on -g unconditionally for now

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 8.0.20-1
- Reorganize rpmrc/macros to set cflags in a nicer manner.

* Wed Jan 22 2003 Elliot Lee <sopwith@redhat.com> 8.0.19-1
- Disable brp-implant-ident-static until it works everywhere

* Thu Jan 16 2003 Nalin Dahyabhai <nalin@redhat.com> 8.0.18-1
- add brp-implant-ident-static, which requires mktemp

* Thu Jan  9 2003 Bill Nottingham <notting@redhat.com> 8.0.17-1
- add brp-strip-static-archive from rpm-4.2-0.54

* Tue Dec 17 2002 Bill Nottingham <notting@redhat.com> 8.0.16-1
- make -g in rpmrc conditional on debug_package

* Mon Dec 16 2002 Elliot Lee <sopwith@redhat.com> 8.0.15-1
- Rename -debug subpackages to -debuginfo

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 8.0.14-1
- tweak debug package stuff so that we are overloading %%install
  instead of %%post

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 8.0.13-1
- turn on internal rpm dep generation by default

* Fri Dec 13 2002 Elliot Lee <sopwith@redhat.com> 8.0.12-1
- New release with debug packages on

* Tue Dec  3 2002 Bill Nottingham <notting@redhat.com> 8.0.8-1
- turn debug packages off
- override optflags with no -g

* Fri Nov 22 2002 Elliot Lee <sopwith@redhat.com> 8.0.7-1
- turn on debug packages

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 8.0.6-1
- Pass __strip and __objdump macros

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com> 8.0.5-1
- Update macros to specify find-provides/find-requires

* Thu Oct 31 2002 Elliot Lee <sopwith@redhat.com> 8.0.4-1
- Remove tracking dependency

* Wed Oct 16 2002 Phil Knirsch <pknirsch@redhat.com> 8.0.3-2
- Added fix for outdated config.[sub|guess] files in %%configure section

* Wed Oct 16 2002 Elliot Lee <sopwith@redhat.com> 8.0.3-1
- New release that blows up on unpackaged files and missing doc files.

* Thu Oct  3 2002 Jeremy Katz <katzj@redhat.com> 8.0.2
- don't redefine everything in macros, just what we need to

* Mon Sep 16 2002 Alexander Larsson <alexl@redhat.com> 8.0.1
- Add debug package support to %%__spec_install_post

* Tue Sep  3 2002 Bill Nottingham <notting@redhat.com> 8.0-1
- bump version

* Wed Aug 28 2002 Elliot Lee <sopwith@redhat.com> 7.3.94-1
- Update macrofiles

* Wed Jul 31 2002 Elliot Lee <sopwith@redhat.com> 7.3.93-1
- Add _unpackaged_files_terminate_build and
_missing_doc_files_terminate_build to macros

* Thu Jul 11 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-6
- find-lang.sh fix from 67368
- find-requires fix from 67325

* Thu Jul 11 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-5
- Add /etc/rpm/macros back to make #67951 go away

* Wed Jun 26 2002 Jens Petersen <petersen@redhat.com> 7.3.92-4
- fix %%configure targeting for autoconf-2.5x (#58468)
- include ~/.rpmmacros in macrofiles file path again

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 7.3.92-3
- automated rebuild

* Fri Jun 21 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-2
- Don't define _arch

* Thu Jun 20 2002 Elliot Lee <sopwith@redhat.com> 7.3.92-1
- find-lang error detection from Havoc

* Wed Jun 12 2002 Elliot Lee <sopwith@redhat.com> 7.3.91-1
- Update

* Sun Jun  9 2002 Jeff Johnson <jbj@redhat.com>
- create.

## END: Generated by rpmautospec
