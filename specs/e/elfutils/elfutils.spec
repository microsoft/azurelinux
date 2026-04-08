# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Rebuild --with static to enable static subpackages
# This is *not* supported by elfutils maintainers
%bcond_with static

Name: elfutils
Version: 0.194
%global baserelease 1
Release: %{baserelease}%{?dist}
URL: http://elfutils.org/
%global source_url ftp://sourceware.org/pub/elfutils/%{version}/
License: GPL-3.0-or-later AND (GPL-2.0-or-later OR LGPL-3.0-or-later) AND GFDL-1.3-no-invariants-or-later
Source: %{?source_url}%{name}-%{version}.tar.bz2
Source1: elfutils-debuginfod.sysusers
Summary: A collection of utilities and DSOs to handle ELF files and DWARF data

# Needed for isa specific Provides and Requires.
%global depsuffix %{?_isa}%{!?_isa:-%{_arch}}

# eu-stacktrace currently only supports x86_64
%ifarch x86_64
%global enable_stacktrace 1
%else
%global enable_stacktrace 0
%endif

Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}
Requires: elfutils-debuginfod-client%{depsuffix} = %{version}-%{release}

BuildRequires: gcc
# For libstdc++ demangle support
BuildRequires: gcc-c++

BuildRequires: gettext
BuildRequires: bison
BuildRequires: flex

# Compression support
BuildRequires: zlib-devel
BuildRequires: bzip2-devel
BuildRequires: xz-devel
BuildRequires: libzstd-devel

# For debuginfod
BuildRequires: pkgconfig(libmicrohttpd) >= 0.9.33
BuildRequires: pkgconfig(libcurl) >= 7.29.0
BuildRequires: pkgconfig(sqlite3) >= 3.7.17
BuildRequires: pkgconfig(libarchive) >= 3.1.2
# For debugindod metadata query
BuildRequires: pkgconfig(json-c) >= 0.11

# For tests need to bunzip2 test files.
BuildRequires: bzip2
BuildRequires: zstd
# For the run-debuginfod-find.sh test case in %%check for /usr/sbin/ss etc.
BuildRequires: iproute
BuildRequires: procps
BuildRequires: bsdtar
BuildRequires: curl
# For run-debuginfod-response-headers.sh test case
BuildRequires: socat
# For run-debuginfod-find-metadata.sh
BuildRequires: jq

# For debuginfod rpm IMA verification
BuildRequires: rpm-devel
BuildRequires: ima-evm-utils-devel
BuildRequires: openssl-devel
BuildRequires: rpm-sign

# For eu-stacktrace
%if %{enable_stacktrace}
BuildRequires: sysprof-capture-devel
%endif

BuildRequires: automake
BuildRequires: autoconf
BuildRequires: gettext-devel

%global _gnu %{nil}
%global _program_prefix eu-

%global provide_yama_scope      0

%if 0%{?fedora} >= 22 || 0%{?rhel} >= 7
%global provide_yama_scope      1
%endif

%global with_sysusers           0

%if 0%{?fedora} >= 32 || 0%{?rhel} >= 9
%global with_sysusers           1
%endif

# Patches

# For s390x... FDO package notes are bogus.
Patch1: elfutils-0.186-fdo-swap.patch

# Prevent assert failure in readelf for some -ggdb3 binaries.
Patch2: elfutils-0.194-alloc-jobs.patch

%description
Elfutils is a collection of utilities, including stack (to show
backtraces), nm (for listing symbols from object files), size
(for listing the section sizes of an object or archive file),
strip (for discarding symbols), readelf (to see the raw ELF file
structures), elflint (to check for well-formed ELF files) and
elfcompress (to compress or decompress ELF sections).

%package libs
Summary: Libraries to handle compiled objects
License: GPL-2.0-or-later OR LGPL-3.0-or-later
%if 0%{!?_isa:1}
Provides: elfutils-libs%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
%if %{provide_yama_scope}
Requires: default-yama-scope
%endif
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 20
Recommends: elfutils-debuginfod-client%{depsuffix} = %{version}-%{release}
%else
Requires: elfutils-debuginfod-client%{depsuffix} = %{version}-%{release}
%endif

%description libs
The elfutils-libs package contains libraries which implement DWARF, ELF,
and machine-specific ELF handling and process introspection.  These
libraries are used by the programs in the elfutils package.  The
elfutils-devel package enables building other programs using these
libraries.

%package devel
Summary: Development libraries to handle compiled objects
License: GPL-2.0-or-later OR LGPL-3.0-or-later
%if 0%{!?_isa:1}
Provides: elfutils-devel%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 20
Recommends: elfutils-debuginfod-client-devel%{depsuffix} = %{version}-%{release}
%else
Requires: elfutils-debuginfod-client-devel%{depsuffix} = %{version}-%{release}
%endif

%description devel
The elfutils-devel package contains the libraries to create
applications for handling compiled objects.  libdw provides access
to the DWARF debugging information.  libasm provides a programmable
assembler interface.

%if %{with static}
%package devel-static
Summary: Static archives to handle compiled objects
License: GPL-2.0-or-later OR LGPL-3.0-or-later
%if 0%{!?_isa:1}
Provides: elfutils-devel-static%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-devel%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf-devel-static%{depsuffix} = %{version}-%{release}

%description devel-static
The elfutils-devel-static package contains the static archives
with the code to handle compiled objects.
%endif

%package libelf
Summary: Library to read and write ELF files
License: GPL-2.0-or-later OR LGPL-3.0-or-later
%if 0%{!?_isa:1}
Provides: elfutils-libelf%{depsuffix} = %{version}-%{release}
%endif
Obsoletes: libelf <= 0.8.2-2

%description libelf
The elfutils-libelf package provides a DSO which allows reading and
writing ELF files on a high level.  Third party programs depend on
this package to read internals of ELF files.  The programs of the
elfutils package use it also to generate new ELF files.

%package libelf-devel
Summary: Development support for libelf
License: GPL-2.0-or-later OR LGPL-3.0-or-later
%if 0%{!?_isa:1}
Provides: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
Obsoletes: libelf-devel <= 0.8.2-2

%description libelf-devel
The elfutils-libelf-devel package contains the libraries to create
applications for handling compiled objects.  libelf allows you to
access the internals of the ELF object file format, so you can see the
different sections of an ELF file.

%if %{with static}
%package libelf-devel-static
Summary: Static archive of libelf
License: GPL-2.0-or-later OR LGPL-3.0-or-later
%if 0%{!?_isa:1}
Provides: elfutils-libelf-devel-static%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-libelf-devel%{depsuffix} = %{version}-%{release}
Requires: libzstd-static%{depsuffix}

%description libelf-devel-static
The elfutils-libelf-static package contains the static archive
for libelf.
%endif

%if %{provide_yama_scope}
%package default-yama-scope
Summary: Default yama attach scope sysctl setting
License: GPL-2.0-or-later OR LGPL-3.0-or-later
Provides: default-yama-scope
BuildArch: noarch
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
BuildRequires: systemd >= 215
%if 0%{?fedora} > 24 || 0%{?rhel} > 7
Recommends: systemd
%else
Requires(post): systemd
%endif

%description default-yama-scope
Yama sysctl setting to enable default attach scope settings
enabling programs to use ptrace attach, access to
/proc/PID/{mem,personality,stack,syscall}, and the syscalls
process_vm_readv and process_vm_writev which are used for
interprocess services, communication and introspection
(like synchronisation, signaling, debugging, tracing and
profiling) of processes.
%endif

%package debuginfod-client
Summary: Library and command line client for build-id HTTP ELF/DWARF server
License: GPL-3.0-or-later AND (GPL-2.0-or-later OR LGPL-3.0-or-later)
%if 0%{!?_isa:1}
Provides: elfutils-debuginfod-client%{depsuffix} = %{version}-%{release}
%endif
# For debuginfod-find binary
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}

%package debuginfod-client-devel
Summary: Libraries and headers to build debuginfod client applications
License: GPL-2.0-or-later OR LGPL-3.0-or-later
%if 0%{!?_isa:1}
Provides: elfutils-debuginfod-client-devel%{depsuffix} = %{version}-%{release}
%endif
Requires: elfutils-debuginfod-client%{depsuffix} = %{version}-%{release}

%package debuginfod
Summary: HTTP ELF/DWARF file server addressed by build-id
License: GPL-3.0-or-later
Requires: elfutils-libs%{depsuffix} = %{version}-%{release}
Requires: elfutils-libelf%{depsuffix} = %{version}-%{release}
Requires: elfutils-debuginfod-client%{depsuffix} = %{version}-%{release}
BuildRequires: systemd
%if %{with_sysusers}
BuildRequires: systemd-rpm-macros
%endif
BuildRequires: make
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
%if %{with_sysusers}
%{?sysusers_requires_compat}
%else
Requires(pre): shadow-utils
%endif
# To extract .deb files with a bsdtar (= libarchive) subshell
Requires: bsdtar

%description debuginfod-client
The elfutils-debuginfod-client package contains shared libraries
dynamically loaded from -ldw, which use a debuginfod service
to look up debuginfo and associated data. Also includes a
command-line frontend.

%description debuginfod-client-devel
The elfutils-debuginfod-client-devel package contains the libraries
to create applications to use the debuginfod service.

%description debuginfod
The elfutils-debuginfod package contains the debuginfod binary
and control files for a service that can provide ELF/DWARF
files to remote clients, based on build-id identification.
The ELF/DWARF file searching functions in libdwfl can query
such servers to download those files on demand.

%prep
%autosetup -p1

autoreconf -f -v -i

# In case the above patches added any new test scripts, make sure they
# are executable.
find . -name \*.sh ! -perm -0100 -print | xargs chmod +x

%build
# Remove -Wall from default flags.  The makefiles enable enough warnings
# themselves, and they use -Werror.  Appending -Wall defeats the cases where
# the makefiles disable some specific warnings for specific code.
# But add -Wformat explicitly for use with -Werror=format-security which
# doesn't work without -Wformat (enabled by -Wall).
RPM_OPT_FLAGS="${RPM_OPT_FLAGS/-Wall/}"
RPM_OPT_FLAGS="${RPM_OPT_FLAGS} -Wformat"


trap 'cat config.log' EXIT
# dist_debuginfod_url is defined in macros.dist. Fedora and CentOS have
# URLs pointing to their respective servers.  RHEL and Amazon Linux do
# not configure a default server.
%configure CFLAGS="$RPM_OPT_FLAGS" \
%if "%{?dist_debuginfod_url}"
	--enable-debuginfod \
	--enable-debuginfod-urls="%{dist_debuginfod_url}" \
%endif
%if %{enable_stacktrace}
	--enable-stacktrace \
%endif
	--enable-debuginfod-ima-verification \
	--enable-debuginfod-ima-cert-path=%{_sysconfdir}/keys/ima
trap '' EXIT
%make_build

%install
%make_install

chmod +x ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib*.so*
%if %{without static}
# We don't want the static libraries
rm ${RPM_BUILD_ROOT}%{_prefix}/%{_lib}/lib{elf,dw,asm}.a
%endif

%find_lang %{name}

%if %{provide_yama_scope}
install -Dm0644 config/10-default-yama-scope.conf ${RPM_BUILD_ROOT}%{_sysctldir}/10-default-yama-scope.conf
%endif

install -Dm0644 config/debuginfod.service ${RPM_BUILD_ROOT}%{_unitdir}/debuginfod.service
install -Dm0644 config/debuginfod.sysconfig ${RPM_BUILD_ROOT}%{_sysconfdir}/sysconfig/debuginfod
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/cache/debuginfod
touch ${RPM_BUILD_ROOT}%{_localstatedir}/cache/debuginfod/debuginfod.sqlite

%if %{with_sysusers}
install -Dm0644 %{SOURCE1} %{buildroot}%{_sysusersdir}/elfutils-debuginfod.conf
%endif

%check
# Record some build root versions in build.log
uname -r; rpm -q binutils gcc glibc || true

%make_build check || (cat tests/test-suite.log; false)

# Only the latest Fedora and EPEL have these scriptlets,
# older Fedora and plain RHEL don't.
%if 0%{?ldconfig_scriptlets:1}
%ldconfig_scriptlets libs
%ldconfig_scriptlets libelf
%ldconfig_scriptlets debuginfod-client
%else
%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig
%post libelf -p /sbin/ldconfig
%postun libelf -p /sbin/ldconfig
%post debuginfod-client -p /sbin/ldconfig
%postun debuginfod-client -p /sbin/ldconfig
%endif

%if %{provide_yama_scope}
%post default-yama-scope
# Due to circular dependencies might not be installed yet, so double check.
# (systemd -> elfutils-libs -> default-yama-scope -> systemd)
if [ -x /usr/lib/systemd/systemd-sysctl ] ; then
%sysctl_apply 10-default-yama-scope.conf
fi
%endif

%files
%license COPYING COPYING-GPLV2 COPYING-LGPLV3 doc/COPYING-GFDL
%doc README TODO CONTRIBUTING
%{_bindir}/eu-addr2line
%{_bindir}/eu-ar
%{_bindir}/eu-elfclassify
%{_bindir}/eu-elfcmp
%{_bindir}/eu-elfcompress
%{_bindir}/eu-elflint
%{_bindir}/eu-findtextrel
%{_bindir}/eu-make-debug-archive
%{_bindir}/eu-nm
%{_bindir}/eu-objdump
%{_bindir}/eu-ranlib
%{_bindir}/eu-readelf
%{_bindir}/eu-size
%{_bindir}/eu-srcfiles
%{_bindir}/eu-stack
%if %{enable_stacktrace}
%{_bindir}/eu-stacktrace
%endif
%{_bindir}/eu-strings
%{_bindir}/eu-strip
%{_bindir}/eu-unstrip
%{_mandir}/man1/eu-*.1*

%files libs
%license COPYING-GPLV2 COPYING-LGPLV3
%{_libdir}/libasm-%{version}.so
%{_libdir}/libdw-%{version}.so
%{_libdir}/libasm.so.*
%{_libdir}/libdw.so.*

%files devel
%{_includedir}/dwarf.h
%dir %{_includedir}/elfutils
%{_includedir}/elfutils/elf-knowledge.h
%{_includedir}/elfutils/known-dwarf.h
%{_includedir}/elfutils/libasm.h
%{_includedir}/elfutils/libdw.h
%{_includedir}/elfutils/libdwfl.h
%{_includedir}/elfutils/libdwelf.h
%{_includedir}/elfutils/version.h
%{_includedir}/elfutils/libdwfl_stacktrace.h
%{_libdir}/libasm.so
%{_libdir}/libdw.so
%{_libdir}/pkgconfig/libdw.pc

%if %{with static}
%files devel-static
%{_libdir}/libdw.a
%{_libdir}/libasm.a
%endif

%files -f %{name}.lang libelf
%license COPYING-GPLV2 COPYING-LGPLV3
%{_libdir}/libelf-%{version}.so
%{_libdir}/libelf.so.*

%files libelf-devel
%{_includedir}/libelf.h
%{_includedir}/gelf.h
%{_includedir}/nlist.h
%{_libdir}/libelf.so
%{_libdir}/pkgconfig/libelf.pc
%{_mandir}/man3/elf_*.3*
%{_mandir}/man3/elf32_*.3*
%{_mandir}/man3/elf64_*.3*
%{_mandir}/man3/gelf_*.3*
%{_mandir}/man3/libelf.3*

%if %{with static}
%files libelf-devel-static
%{_libdir}/libelf.a
%endif

%if %{provide_yama_scope}
%files default-yama-scope
%{_sysctldir}/10-default-yama-scope.conf
%endif

%files debuginfod-client
%{_libdir}/libdebuginfod-%{version}.so
%{_libdir}/libdebuginfod.so.*
%{_bindir}/debuginfod-find
%{_mandir}/man1/debuginfod-find.1*
%{_mandir}/man7/debuginfod*.7*
%config(noreplace) %{_sysconfdir}/profile.d/*
%if "%{?dist_debuginfod_url}"
%config(noreplace) %{_sysconfdir}/debuginfod/*
%config(noreplace) %{_datadir}/fish/vendor_conf.d/*
%endif

%files debuginfod-client-devel
%{_libdir}/pkgconfig/libdebuginfod.pc
%{_mandir}/man3/debuginfod_*.3*
%{_includedir}/elfutils/debuginfod.h
%{_libdir}/libdebuginfod.so

%files debuginfod
%{_bindir}/debuginfod
%config(noreplace) %{_sysconfdir}/sysconfig/debuginfod
%{_unitdir}/debuginfod.service
%if %{with_sysusers}
%{_sysusersdir}/elfutils-debuginfod.conf
%endif
%{_mandir}/man8/debuginfod*.8*


%dir %attr(0700,debuginfod,debuginfod) %{_localstatedir}/cache/debuginfod
%ghost %attr(0600,debuginfod,debuginfod) %{_localstatedir}/cache/debuginfod/debuginfod.sqlite

%pre debuginfod
%if %{with_sysusers}
%sysusers_create_compat %{SOURCE1}
%else
getent group debuginfod >/dev/null || groupadd -r debuginfod
getent passwd debuginfod >/dev/null || \
    useradd -r -g debuginfod -d /var/cache/debuginfod -s /sbin/nologin \
            -c "elfutils debuginfo server" debuginfod
exit 0
%endif

%post debuginfod
%systemd_post debuginfod.service

%postun debuginfod
%systemd_postun_with_restart debuginfod.service

%changelog
* Tue Oct 28 2025 Aaron Merey <amerey@redhat.com> - 0.194-1
- Upgrade to upstream elfutils 0.194
- Add elfutils-0.194-alloc-jobs.patch

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.193-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Apr 28 2025 Aaron Merey <amerey@redhat.com> - 0.193-1
- Upgrade to upstream elfutils 0.193
- Drop upstreamed patches
  elfutils-0.192-ATOMIC_VAR_INIT.patch
  elfutils-0.192-libelf-static.patch
  elfutils-0.192-fix-configure-conditional.patch
  elfutils-0.192-more-dwarf5-lang.patch
  elfutils-0.192-fix-zsh-profile.patch
  elfutils-0.192-stacktrace-lto.patch
  elfutils-0.192-imasig-fail-free.patch
  elfutils-0.192-strip-ignore-non-ET_REL.patch

* Sun Feb 23 2025 Mark Wielaard <mjw@fedoraproject.org> - 0.192-9
- Add elfutils-0.192-imasig-fail-free.patch

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.192-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 2 2024 Mark Wielaard <mjw@fedoraproject.org> - 0.192-7
- Add elfutils-0.192-ATOMIC_VAR_INIT.patch
- Add elfutils-0.192-more-dwarf5-lang.patch

* Tue Nov 12 2024 Aaron Merey <amerey@fedoraproject.org> - 0.192-6
- Add elfutils-0.192-strip-ignore-non-ET_REL.patch
- Set debuginfod IMA cert path

* Tue Oct 29 2024 Aaron Merey <amerey@fedoraproject.org> - 0.192-5
- Enable debuginfod IMA verification
- Add elfutils-0.192-fix-configure-conditional.patch
- Add elfutils-0.192-fix-zsh-profile.patch

* Thu Oct 24 2024 Mark Wielaard <mjw@fedoraproject.org> - 0.192-4
- Add elfutils-0.192-stacktrace-lto.patch
- Enable eu-stacktrace on x86_64

* Tue Oct 22 2024 Aaron Merey <amerey@fedoraproject.org> - 0.192-3
- Add elfutils-0.192-libelf-static.patch

* Mon Oct 21 2024 Aaron Merey <amerey@fedoraproject.org> - 0.192-2
- Add BuildRequires for json-c

* Mon Oct 21 2024 Aaron Merey <amerey@fedoraproject.org> - 0.192-1
- Upgrade to upstream elfutils 0.192
- Drop upstreamed patches
  Add elfutils-0.190-profile-empty-urls.patch
  Add elfutils-0.190-riscv-flatten.patch

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.191-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 22 2024 Aaron Merey <amerey@fedoraproject.org> - 0.191-7
- Capitalize SPDX booleans.

* Fri Apr 19 2024 Mark Wielaard <mjw@fedoraproject.org> - 0.191-6
- eu-srcfiles directly links to libdebuginfod.so so explicitly
  Require elfutils-debuginfod-client not just Recommends.

* Wed Mar 27 2024 Mark Wielaard <mjw@fedoraproject.org> - 0.191-5
- Add elfutils-0.190-profile-empty-urls.patch

* Wed Mar 20 2024 Mark Wielaard <mjw@fedoraproject.org> - 0.191-4
- Add elfutils-0.190-riscv-flatten.patch

* Fri Mar 15 2024 Michel Lind <salimma@fedoraproject.org> - 0.191-3
- Add feature flag for reenabling elfutils-libelf-devel-static and elfutils-devel-static
- Add dependency on libzstd-static for elfutils-libelf-devel-static

* Mon Mar  4 2024 Aaron Merey <amerey@fedoraproject.org> - 0.191-2
- Update SPDX license.

* Mon Mar  4 2024 Aaron Merey <amerey@fedoraproject.org> - 0.191-1
- Upgrade to upstream elfutils 0.191
- Drop upstreamed patches
  elfutils-0.190-fix-core-noncontig.patch
  elfutils-0.190-gcc-14.patch
  elfutils-0.190-remove-ET_REL-unstrip-test.patch
- Drop testcore-noncontig.bz2

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.190-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.190-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Aaron Merey <amerey@fedoraproject.org> - 0.190-4
- Add elfutils-0.190-remove-ET_REL-unstrip-test.patch

* Fri Nov 24 2023 Aaron Merey <amerey@fedoraproject.org> - 0.190-3
- Add elfutils-0.190-fix-core-noncontig.patch

* Fri Nov  3 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.190-2
- Update Fedora license tags to spdx license tags

* Fri Nov  3 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.190-1
- Upgrade to upstream elfutils 0.190
- Add eu-srcfiles
- Drop upstreamed patches
  elfutils-0.189-relr.patch
  elfutils-0.189-debuginfod_config_cache-double-close.patch
  elfutils-0.189-elf_getdata_rawchunk.patch
  elfutils-0.189-elfcompress.patch
  elfutils-0.189-c99-compat.patch
- Only package debuginfod-client-config.7 manpage for debuginfod-client

* Thu Aug 24 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.189-6
- Update elfutils-0.189-relr.patch

* Wed Aug 23 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.189-5
- Add elfutils-0.189-relr.patch

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.189-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.189-3
- Add elfutils-0.189-elf_getdata_rawchunk.patch
- Add elfutils-0.189-debuginfod_config_cache-double-close.patch

* Sat Apr 22 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.189-2
- Add elfutils-0.189-c99-compat.patch
- Add elfutils-0.189-elfcompress.patch

* Fri Mar 3 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.189-1
- Upgrade to upsteam elfutils 0.189.

* Fri Jan 27 2023 Mark Wielaard <mjw@fedoraproject.org> - 0.188-5
- Add elfutils-0.188-deprecated-CURLINFO.patch,
  elfutils-0.188-CURL_AT_LEAST_VERSION.patch and
  elfutils-0.188-CURLOPT_PROTOCOLS_STR.patch

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.188-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 7 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.188-3
- Add elfutils-0.188-compile-warnings.patch
- Add elfutils-0.188-debuginfod-client-lifetime.patch

* Wed Nov 2 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.188-2
- Add elfutils-0.188-static-extract_section.patch.

* Wed Nov 2 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.188-1
- Upgrade to upsteam elfutils 0.188.

* Wed Oct 5 2022 Amit Shah <amitshah@fedoraproject.org> - 0.187-9
- Auto-configure debuginfod_url based on macros.dist

* Wed Aug 24 2022 Debarshi Ray <rishi@fedoraproject.org> - 0.187-8
- Use %%sysusers_requires_compat to match %%sysusers_create_compat

* Wed Jul 27 2022 Amit Shah <amitshah@fedoraproject.org> - 0.187-7
- Allow building without default debuginfod URL

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.187-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.187-5
- Add sysuser support for creating the debuginfod user

* Fri May  6 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.187-4
- Add elfutils-0.187-mhd_no_dual_stack.patch
- Add elfutils-0.187-mhd_epoll.patch

* Thu May  5 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.187-3
- Add elfutils-0.187-debuginfod-client-fd-leak.patch

* Tue May  3 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.187-2
- Add elfutils-0.187-csh-profile.patch

* Tue Apr 26 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.187-1
- Upgrade to elfutils 0.187
  - debuginfod: Support -C option for connection thread pooling.
  - debuginfod-client: Negative cache file are now zero sized instead
    of no-permission files.
  - addr2line: The -A, --absolute option, which shows file names
    includingthe full compilation directory is now the
    default.  To get theold behavior use the new option --relative.
  - readelf, elflint: Recognize FDO Packaging Metadata ELF notes
  - libdw, debuginfo-client: Load libcurl lazily only when files need
    to be fetched remotely. libcurl is now never loaded when
    DEBUGINFOD_URLS is unset. And whenDEBUGINFOD_URLS is set,
    libcurl is only loaded when the debuginfod_begin function is
    called.

* Tue Apr 12 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.186-5
- Add an explicit versioned requires from elfutils-debuginfod-client
  on elfutils-libelf.

* Thu Apr  7 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.186-4
- Add an explicit versioned requires from elfutils-debuginfod-client
  on elfutils-libs.

* Fri Mar 25 2022 Mark Wielaard <mjw@fedoraproject.org> - 0.186-3
- Add elfutils-0.186-elf-glibc.patch
- Add elfutils-0.186-fdo-ebl.patch
- Add elfutils-0.186-fdo-efllint.patch
- Add elfutils-0.186-fdo-swap.patch
- Add elfutils-0.186-ppc64le-error-return-workaround.patch

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.186-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 10 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.186-1
- Upgrade to upstream 0.186
  - debuginfod-client: Default $DEBUGINFOD_URLS is computed from
    drop-in files /etc/debuginfod/*.urls rather than
    hardcoded into the /etc/profile.d/debuginfod*
    scripts.
    Add $DEBUGINFOD_MAXSIZE and $DEBUGINFOD_MAXTIME settings
    for skipping large/slow transfers.
    Add $DEBUGINFOD_RETRY for retrying aborted lookups.
  - debuginfod: Supply extra HTTP response headers, describing
    archive/file names that satisfy the requested buildid content.
    Support -d :memory: option for in-memory databases.
    Protect against loops in federated server configurations.
    Add -r option to use -I/-X regexes for grooming stale files.
    Protect against wasted CPU from duplicate concurrent requests.
    Limit the duration of groom ops roughly to rescan (-t) times.
    Add --passive mode for serving from read-only database.
    Several other performance improvements & prometheus metrics.
  - libdw: Support for the NVIDIA Cuda line map extensions.
    DW_LNE_NVIDIA_inlined_call and DW_LNE_NVIDIA_set_function_name
    are defined in dwarf.h. New functions dwarf_linecontext and
    dwarf_linefunctionname.
  - translations: Update Japanese translation.

* Thu Aug  5 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.185-5
- Use autosetup
- Add elfutils-0.185-raise-pthread_kill-backtrace.patch

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.185-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 15 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.185-3
- Update version to 0.185-3 for rawhide/f35 upgrade from f34
  This build enables debuginfod client by default
- Workaround bad test in make check

* Wed May 26 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.185-1
- Upgrade to upstream 0.185
  - debuginfod-client: Simplify curl handle reuse so downloads which
                       return an error are retried.
  - elfcompress: Always exit with code 0 when the operation succeeds
                 (even when nothing was done). On error the exit code
                 is now always 1.

* Sun May 16 2021 Frank Ch. Eigler <fche@redhat.com> - 0.184-5
- Fix 404-latch problem on reused debuginfod_client. (PR27859)

* Wed May 12 2021 Frank Ch. Eigler <fche@redhat.com> - 0.184-4
- Ship new profile.d files. (1956952)

* Wed May 12 2021 Frank Ch. Eigler <fche@redhat.com> - 0.184-3
- Don't nuke the new profile.d files. (1956952)

* Tue May 11 2021 Frank Ch. Eigler <fche@redhat.com> - 0.184-2
- Activate debuginfod client by default (1956952) to the fedora server.

* Mon May 10 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.184-1
- Upgrade to upstream 0.184
  - debuginfod: Use libarchive's bsdtar as the .deb-family file unpacker.
  - debuginfod-client: Client caches negative results. If a query for a
                       file failed with 404, an empty 000 permission
                       file is created in the cache. This will prevent
                       requesting the same file for the next 10 minutes.
                       Client objects now carry long-lived curl handles
                       for outgoing connections.  This makes it more
                       efficient for multiple sequential queries, because
                       the TCP connections and/or TLS state info are kept
                       around awhile, avoiding O(100ms) setup latencies.
  - libdw: handle DW_FORM_indirect when reading attributes
  - translations: Update Polish translation.

* Mon Apr 19 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.183-3
- Introduce CI gating setup

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.183-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb  8 2021 Mark Wielaard <mjw@fedoraproject.org> - 0.183-1
- Upgrade to upstream 0.183
  - debuginfod: New thread-busy metric and more detailed error metrics.
    New --fdcache-mintmp and tracking of filesystem freespace.
  - debuginfod-client: DEBUGINFOD_SONAME macro added to debuginfod.h can
    be used to dlopen the libdebuginfod.so library.
    New function debuginfod_set_verbose_fd and DEBUGINFOD_VERBOSE
    environment variable.
  - config: profile.sh and profile.csh won't export DEBUGINFOD_URLS
    unless configured --enable-debuginfod-urls[=URLS]
  - elflint, readelf: Recognize SHF_GNU_RETAIN.
    Handle SHT_X86_64_UNWIND as valid relocation target type.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.182-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.182-2
- Add elfutils-0.182-s390-pid_memory_read.patch

* Sat Oct 31 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.182-1
- Upgrade to upstream 0.182
  - backends: Support for tilegx has been removed.
  - config: New /etc/profile.d files to provide default $DEBUGINFOD_URLS.
  - debuginfod: More efficient package traversal, tolerate various
    errors during scanning, grooming progress is more visible and
    interruptible, more prometheus metrics.
  - debuginfod-client: Now supports compressed (kernel) ELF images.
  - libdwfl: Add ZSTD compression support.

* Mon Oct 19 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.181-3
- Add elfutils-0.181-array-param.patch.

* Fri Sep 18 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.181-2
- Add ZSTD support elfutils-0.181-zstd.patch.

* Tue Sep  8 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.181-1
- Upgrade to upstream 0.181
  - libelf: elf_update now compensates (fixes up) a bad sh_addralign
    for SHF_COMPRESSED sections.
  - libdebuginfod: configure now takes --enable-libdebuginfod=dummy or
    --disable-libdebuginfod for bootstrapping.
    DEBUGINFOD_URLS now accepts "scheme-free" urls
    (guessing at what the user meant, either http:// or file://)
  - readelf, elflint: Handle aarch64 bti, pac bits in dynamic table and
    gnu property notes.
  - libdw, readelf: Recognize DW_CFA_AARCH64_negate_ra_state. Allows
    unwinding on arm64 for code that is compiled for PAC
    (Pointer Authentication Code) as long as it isn't enabled.

* Tue Aug 25 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.180-7
- Add elfutils-0.180-shf-compressed.patch

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.180-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.180-5
- Remove elfutils-libelf-devel-static and elfutils-devel-static subpackages.
- Remove duplicate listing of sysconfig/debuginfod (config) file.

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 0.180-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jul  3 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.180-3
- Add elfutils-0.180-mhd-result.patch

* Wed Jul  1 2020 Jeff Law <law@redhat.com> - 0.180-2
- Disable LTO

* Thu Jun 11 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.180-1
- New upstream release.
  elflint: Allow SHF_EXCLUDE as generic section flag when --gnu is given.
  libdw, readelf: Handle GCC LTO .gnu.debuglto_ prefix.
  libdw: Use correct CU to resolve file names in dwarf_decl_file.
  libdwfl: Handle debugaltlink in dwfl_standard_find_debuginfo.
  size: Also obey radix printing for bsd format.
  nm: Explicitly print weak 'V' or 'T' and common 'C' symbols.

* Thu Apr 30 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.179-2
- Add elfutils-0.179-debug-client-alt-link.patch

* Mon Mar 30 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.179-1
- New upstream release.
  debuginfod-client:
  - When DEBUGINFOD_PROGRESS is set and the program doesn't
    install its own debuginfod_progressfn_t show download
    progress on stderr.
  - DEBUGINFOD_TIMEOUT is now defined as seconds to get at
    least 100K, defaults to 90 seconds.
  - Default to $XDG_CACHE_HOME/debuginfod_client.
  - New functions debuginfod_set_user_data,
    debuginfod_get_user_data, debuginfod_get_url and
    debuginfod_add_http_header.
  - Support for file:// URLs.

  debuginfod:
  - Performance improvements through highly parallelized scanning
    and archive content caching.
  - Uses libarchive directly for reading rpm archives.
  - Support for indexing .deb/.ddeb archives through dpkg-deb
    or bsdtar.
  - Generic archive support through -Z EXT[=CMD]. Which can be
    used for example for arch-linux pacman files by using
    -Z '.tar.zst=zstdcat'.
  - Better logging using User-Agent and X-Forwarded-For headers.
  - More prometheus metrics.
  - Support for eliding dots or extraneous slashes in path names.

  debuginfod-find:
  - Accept /path/names in place of buildid hex.

  libelf:
  - Handle PN_XNUM in elf_getphdrnum before shdr 0 is cached
  - Ensure zlib resource cleanup on failure.

  libdwfl:
  - dwfl_linux_kernel_find_elf and dwfl_linux_kernel_report_offline
    now find and handle a compressed vmlinuz image.

  readelf, elflint:
  - Handle PT_GNU_PROPERTY.

  translations:
  - Updated Ukrainian translation.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.178-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 24 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.178-8
- Add elfutils-0.178-gcc10-null-dereference.patch

* Fri Jan 10 2020 Mark Wielaard <mjw@fedoraproject.org> - 0.178-7
- Add elfutils-0.178-debuginfod-timeoutprogress.patch
- Add elfutils-0.178-libasm-ebl.patch

* Wed Dec 11 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.178-6
- Add elfutils-0.178-curl-code-gcc-10.patch
- Add elfutils-0.178-compressed-vmlinuz.patch

* Mon Dec  9 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.178-5
- Add elfutils-0.178-debuginfod-no-cache.patch.

* Thu Nov 28 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.178-4
- Define %%{depsuffix} before use.

* Thu Nov 28 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.178-3
- Add elfutils-debuginfod-client Provides and Requires with depsuffix
  to get multilib dependencies correct. Add %%{version}-%%{release} to
  keep subpackages in sync.

* Wed Nov 27 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.178-2
- Fix libdebuginfod file list for debuginfo-client[-devel].

* Tue Nov 26 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.178-1
- New upstream release.
  - debuginfod: New server, client tool and library to index and fetch
                ELF/DWARF files addressed by build-id through HTTP.
  - doc: There are now some manual pages for functions and tools.
  - backends: The libebl libraries are no longer dynamically loaded
              through dlopen, but are now compiled into libdw.so directly.
  - readelf: -n, --notes now takes an optional "SECTION" argument.
             -p and -x now also handle section numbers.
             New option --dyn-sym to show just the dynamic symbol table.
  - libcpu: Add RISC-V disassembler.
  - libdw: Abbrevs and DIEs can now be read concurrently by multiple
           threads through the same Dwarf handle.
  - libdwfl: Will try to use debuginfod when installed as fallback to
             retrieve ELF and DWARF debug data files by build-id.

* Wed Aug 14 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.177-1
- New upstream release.
  - elfclassify: New tool to analyze ELF objects.
  - readelf: Print DW_AT_data_member_location as decimal offset.
             Decode DW_AT_discr_list block attributes.
  - libdw: Add DW_AT_GNU_numerator, DW_AT_GNU_denominator and DW_AT_GNU_bias.
  - libdwelf: Add dwelf_elf_e_machine_string.
              dwelf_elf_begin now only returns NULL when there is an error
              reading or decompressing a file. If the file is not an ELF file
              an ELF handle of type ELF_K_NONE is returned.
  - backends: Add support for C-SKY.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.176-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul  5 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.176-4
- Add elfutils-0.176-strip-symbols-illformed.patch

* Mon Jun  3 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.176-3
- Add elfutils-0.176-elf-update.patch

* Tue Apr 30 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.176-2
- Update elfutils-0.176-gcc-pr88835.patch.
- Add elfutils-0.176-pt-gnu-prop.patch
- Add elfutils-0.176-xlate-note.patch

* Fri Feb 15 2019 Mark Wielaard <mjw@fedoraproject.org> - 0.176-1
- New upstream release.
  - backends: riscv improved core file and return value location support.
  - Fixes CVE-2019-7146, CVE-2019-7148, CVE-2019-7149, CVE-2019-7150,
          CVE-2019-7664, CVE-2019-7665.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.175-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec  3 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.175-2
- Add elfutils-0.175-gnu-props-32.patch.

* Fri Nov 16 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.175-1
- New upstream release.
  - readelf: Handle multiple .debug_macro sections.
  - strip: Add strip --reloc-debug-sections-only option.
    Handle relocations against GNU compressed sections.
  - libdwelf: New function dwelf_elf_begin.
  - libcpu: Recognize bpf jump variants BPF_JLT, BPF_JLE, BPF_JSLT
    and BPF_JSLE.
  - backends: RISCV handles ADD/SUB relocations.
- Remove all patches.

* Wed Nov 14 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.174-5
- Add elfutils-0.174-x86_64_unwind.patch.
- Add elfutils-0.174-gnu-property-note.patch.
- Add elfutils-0.174-version-note.patch.
- Add elfutils-0.174-gnu-attribute-note.patch

* Tue Nov  6 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.174-4
- Add elfutils-0.174-size-rec-ar.patch
  CVE-2018-18520 (#1646478)
- Add elfutils-0.174-ar-sh_entsize-zero.patch
  CVE-2018-18521 (#1646483)

* Fri Nov  2 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.174-3
- Add elfutils-0.174-libdwfl-sanity-check-core-reads.patch
  CVE-2018-18310 (#1642605)

* Wed Oct 17 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.174-2
- Add elfutils-0.174-strip-unstrip-group.patch.

* Fri Sep 14 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.174-1
- New upstream release
  - libelf, libdw and all tools now handle extended shnum and shstrndx
    correctly (#1608390).
  - elfcompress: Don't rewrite input file if no section data needs
    updating.  Try harder to keep same file mode bits (suid) on rewrite.
  - strip: Handle mixed (out of order) allocated/non-allocated sections.
  - unstrip: Handle SHT_GROUP sections.
  - backends: RISCV and M68K now have backend implementations to
    generate CFI based backtraces.
  - Fixes CVE-2018-16062, CVE-2018-16402 and CVE-2018-16403
    (#1623753, #1625051, #1625056).

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.173-8
- Rebuild with fixed binutils

* Sun Jul 29 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.173-7
- Add elfutils-0.173-strip-alloc-nonalloc.patch (#1609577)

* Tue Jul 24 2018 Mark Wielaard <mjw@fedoraproject.org>
- Drop libstdc++-devel BuildRequires. gcc-c++ will pull it in.

* Tue Jul 24 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.173-6
- Update elfutils-0.173-annobingroup.patch.

* Sat Jul 21 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.173-5
- Add BuildRequires gcc-c++ for demangle support.
- Add elfutils-0.173-annobingroup.patch.

* Sat Jul 21 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.173-4
- Add elfutils-0.173-elfcompress.patch (#1607044)

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.173-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul  9 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.173-2
- Update elfutils-0.173-new-notes-hack.patch for new annobin note.
- Unbreak cyclic systemd dependency for buildroot container (#1599083)

* Fri Jun 29 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.173-1
- New upstream release
  - More fixes for crashes and hangs found by afl-fuzz. In particular
    various functions now detect and break infinite loops caused by bad
    DIE tree cycles.
  - readelf: Will now lookup the size and signedness of constant value
    types to display them correctly (and not just how they were encoded).
  - libdw: New function dwarf_next_lines to read CU-less .debug_line data.
    dwarf_begin_elf now accepts ELF files containing just .debug_line
    or .debug_frame sections (which can be read without needing a DIE
    tree from the .debug_info section).
    Removed dwarf_getscn_info, which was never implemented.
  - backends: Handle BPF simple relocations.
    The RISCV backends now handles ABI specific CFI and knows about
    RISCV register types and names.

* Wed Jun 20 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.172-2
- Add elfutils-0.172-robustify.patch.

* Mon Jun 11 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.172-1
- New upstream release.
  - No functional changes compared to 0.171.
  - Various bug fixes in libdw and eu-readelf dealing with bad DWARF5
    data. Thanks to running the afl fuzzer on eu-readelf and various
    testcases.
  - eu-readelf -N is ~15% faster.

* Fri Jun 01 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.171-1
- New upstream release.
  - DWARF5 and split dwarf, including GNU DebugFission, support.
  - readelf: Handle all new DWARF5 sections.
    --debug-dump=info+ will show split unit DIEs when found.
    --dwarf-skeleton can be used when inspecting a .dwo file.
    Recognizes GNU locviews with --debug-dump=loc.
  - libdw: New functions dwarf_die_addr_die, dwarf_get_units,
    dwarf_getabbrevattr_data and dwarf_cu_info.
    libdw will now try to resolve the alt file on first use
    when not set yet with dwarf_set_alt.
    dwarf_aggregate_size() now works with multi-dimensional arrays.
  - libdwfl: Use process_vm_readv when available instead of ptrace.
  - backends: Add a RISC-V backend.

* Wed Apr 11 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.170-11
- Add explict libstdc++-devel BuildRequires for demangle support.
- Add elfutils-0.170-unwind.patch. (#1555726)

* Thu Mar 01 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.170-10
- Add elfutils-0.170-GNU_variable_value.patch
- Add elfutils-0.170-locviews.patch

* Fri Feb 16 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.170-9
- Add elfutils-0.170-core-pid.patch
- Add elfutils-0.170-elf_sync.patch
- Add elfutils-0.170-new-notes-hack.patch

* Thu Feb 15 2018 Mark Wielaard <mjw@fedoraproject.org> - 0.170-8
- Add elfutils-0.170-sys-ptrace.patch
- Make sure spec can be build even when ldconfig_scriplets aren't defined.
- Add elfutils-0.170-m68k-packed-not-aligned.patch

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.170-7
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.170-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.170-5
- Switch to %%ldconfig_scriptlets

* Wed Dec 20 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.170-4
- Add elfutils-0.170-dwarf_aggregate_size.patch.

* Wed Nov  8 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.170-3
- Rely on (and check) systemd_requires for sysctl_apply default-yama-scope.

* Thu Nov  2 2017 Mark Wielaard <mjw@redhat.com> - 0.170-2
- Config files under /usr/lib/sysctl.d (_sysctldir) aren't %%config (#1506660)
  Admin can place the real config file under /etc/sysctl.d as override.

* Thu Aug  3 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.170-1
- New upstream release. Remove upstreamed patches.
- provide_yama_scope for either fedora >= 22 and rhel >= 7.

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.169-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.169-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.169-6
- Add elfutils-0.169-strip-data-marker-symbols.patch.

* Mon Jul 17 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.169-5
- Fix build on s390 (ptrace.h). Add elfutils-0.169-s390x-ptrace.patch.

* Mon Jul 17 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.169-4
- Add elfutils-0.169-strip-keep-remove-section.patch (#1465997)

* Wed Jun  7 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.169-3
- Add elfutils-0.169-dup-shstrtab.patch
- Add elfutils-0.169-strip-empty.patch

* Tue May 30 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.169-2
- Add ppc64 fallback unwinder.

* Fri May  5 2017 Mark Wielaard <mjw@fedoraproject.org> - 0.169-1
- New upstream release. Removed upstreamed patches.

* Wed Feb 15 2017 Mark Wielaard <mark@klomp.org> - 0.168-5
- Add patches for new gcc warnings and new binutils ppc64 attributes.
  - elfutils-0.168-libasm-truncation.patch
  - elfutils-0.168-ppc64-attrs.patch

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.168-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Mark Wielaard <mark@klomp.org> - 0.168-3
- Never use old, deprecated, filter_provides_in, it really is too broken.

* Fri Jan 13 2017 Mark Wielaard <mark@klomp.org> - 0.168-2
- Filter out private libebl backends from provides.

* Wed Dec 28 2016 Mark Wielaard <mark@klomp.org> - 0.168-1
- New upstream release from new home https://sourceware.org/elfutils/
- Resolves:
  - #1396092 Please implement eu-readelf --symbols[=SECTION]
  - #1388057 memory allocation failure in allocate_elf
  - #1387584 memory allocation failure in __libelf_set_rawdata_wrlock

* Fri Oct  7 2016 Mark Wielaard <mjw@redhat.com> - 0.167-2
- Add elfutils-0.167-strip-alloc-symbol.patch (#1380961)

* Fri Aug 26 2016 Mark Wielaard <mjw@redhat.com> - 0.167-1
- Upgrade to elfutils-0.167
  Drop upstream elfutils-0.166-elfcmp-comp-gcc6.patch
  Fixes: #1365812, #1352232.

* Thu Apr 14 2016 Mark Wielaard <mjw@redhat.com> - 0.166-2
- Add elfutils-0.166-elfcmp-comp-gcc6.patch

* Thu Mar 31 2016 Mark Wielaard <mjw@redhat.com> - 0.166-1
- Upgrade to elfutils-0.166
  Drop upstreamed patches:
    - elfutils-0.165-nobitsalign-strip.patch.
    - elfutils-0.165-reloc.patch.
    - elfutils-0.165-elf-libelf.patch.

* Thu Feb 04 2016 Mark Wielaard <mjw@redhat.com> - 0.165-5
- Add elfutils-0.165-nobitsalign-strip.patch.

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.165-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Mark Wielaard <mjw@redhat.com> - 0.165-3
- Add elfutils-0.165-reloc.patch.

* Thu Jan 14 2016 Mark Wielaard <mjw@redhat.com> - 0.165-2
- Add elfutils-0.165-elf-libelf.patch.

* Mon Jan 11 2016 Mark Wielaard <mjw@redhat.com> - 0.165-1
- Update to elfutils-0.165 (#1294079, #1236699, #807053)
  - Add eu-elfcompress
  - Add pkg-config files for libelf and libdw.

* Fri Oct 16 2015 Mark Wielaard <mjw@redhat.com> - 0.164-1
- Update to elfutils-0.164
- Drop old compat stuff

* Mon Sep 07 2015 Mark Wielaard <mjw@redhat.com> - 0.163-4
- Add elfutils-0.163-readelf-n-undefined-shift.patch (#1259259)

* Tue Aug 04 2015 Mark Wielaard <mjw@redhat.com> - 0.163-3
- Add elfutils-0.163-default-yama-conf.patch (#1250079)
  Provides: default-yama-scope

* Mon Aug 03 2015 Mark Wielaard <mjw@redhat.com> - 0.163-2
- Add elfutils-0.163-unstrip-shf_info_link.patch

* Fri Jun 19 2015 Mark Wielaard <mjw@redhat.com> - 0.163-1
- Update to 0.163
  - Drop elfutils-0.162-ftruncate-allocate.patch

* Tue Jun 16 2015 Mark Wielaard <mjw@redhat.com> - 0.162-2
- Add elfutils-0.162-ftruncate-allocate.patch (#1232206)

* Thu Jun 11 2015 Mark Wielaard <mjw@redhat.com> - 0.162-1
- Update to 0.162 (#1170810, #1139815, #1129756, #1020842)
- Include elfutils/known-dwarf.h
- Drop BuildRequires glibc-headers (#1230468)
- Removed integrated upstream patches:
  - elfutils-0.161-aarch64relro.patch
  - elfutils-0.161-copyreloc.patch
  - elfutils-0.161-addralign.patch
  - elfutils-0.161-ar-long-name.patch
  - elfutils-0.161-formref-type.patch

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.161-8
- Rebuilt for GCC 5 C++11 ABI change

* Mon Mar 23 2015 Mark Wielaard <mjw@redhat.com> - 0.161-7
- Add elfutils-0.161-aarch64relro.patch (#1201778)

* Mon Mar 09 2015 Mark Wielaard <mjw@redhat.com> - 0.161-6
- Add elfutils-0.161-copyreloc.patch.

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.161-5
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Feb 07 2015 Mark Wielaard <mjw@redhat.com> - 0.161-4
- Add elfutils-0.161-addralign.patch (#1189928)

* Thu Feb 05 2015 Mark Wielaard <mjw@redhat.com> - 0.161-3
- Add elfutils-0.161-formref-type.patch

* Tue Jan 13 2015 Mark Wielaard <mjw@redhat.com> - 0.161-2
- Add elfutils-0.161-ar-long-name.patch (#1181525 CVE-2014-9447)

* Fri Dec 19 2014 Mark Wielaard <mjw@redhat.com> - 0.161-1
- Update to 0.161.

* Wed Aug 27 2014 Mark Wielaard <mjw@redhat.com> - 0.160-1
- Update to 0.160.
  - Remove integrated upstream patches:
    elfutils-aarch64-user_regs_struct.patch
    elfutils-0.159-argp-attach.patch
    elfutils-0.159-aarch64-bool-ret.patch
    elfutils-0.159-elf-h.patch
    elfutils-0.159-ppc64le-elfv2-abi.patch
    elfutils-0.159-report_r_debug.patch
    elfutils-0.159-ko_xz.patch

* Sat Aug 16 2014 Mark Wielaard <mjw@redhat.com> - 0.159-10
- Add elfutils-0.159-ko_xz.patch

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.159-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 28 2014 Mark Wielaard <mjw@redhat.com> - 0.159-8
- Add elfutils-0.159-report_r_debug.patch (#1112610)

* Fri Jul 18 2014 Mark Wielaard <mjw@redhat.com> - 0.159-7
- Add configure check to elfutils-aarch64-user_regs_struct.patch.

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 0.159-6
- fix license handling

* Fri Jul  4 2014 Mark Wielaard <mjw@redhat.com> - 0.159-5
- Add elfutils-0.159-aarch64-bool-ret.patch
- Add elfutils-0.159-elf-h.patch
- Add elfutils-0.159-ppc64le-elfv2-abi.patch (#1110249)

* Tue Jun 10 2014 Mark Wielaard <mjw@redhat.com> - 0.159-4
- Add elfutils-0.159-argp-attach.patch (#1107654)

* Mon Jun 09 2014 Kyle McMartin <kyle@fedoraproject.org> - 0.159-3
- AArch64: handle new glibc-headers which provides proper GETREGSET structs.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.159-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Mark Wielaard <mjw@redhat.com> - 0.159-1
- Update to 0.159.
  - Remove integrated upstream patches:
    robustify.patch, mod-e_type.patch and CVE-2014-0172.patch.
  - Remove special handling of now default compile and configure flags:
    Don't remove -Werror=format-security, don't configure --enable-dwz.

* Thu Apr 10 2014 Mark Wielaard <mjw@redhat.com> - 0.158-3
- Add elfutils-0.158-CVE-2014-0172.patch (#1085729)

* Tue Mar 11 2014 Mark Wielaard <mjw@redhat.com> - 0.158-2
- Add elfutils-0.158-mod-e_type.patch.

* Mon Jan  6 2014 Mark Wielaard <mjw@redhat.com> - 0.158-1
- Update to 0.158. Remove all patches now upstream. Add eu-stack.

* Thu Dec 19 2013 Mark Wielaard <mjw@redhat.com> - 0.157-4
- Add elfutils-0.157-aarch64-got-special-symbol.patch.
- Remove -Werror=format-security from RPM_OPT_FLAGS.

* Fri Dec 13 2013 Petr Machata <pmachata@redhat.com> - 0.157-3
- Add upstream support for aarch64

* Wed Oct  9 2013 Mark Wielaard <mjw@redhat.com> 0.157-2
- Show tests/test-suite.log in build.log when make check fails.

* Mon Sep 30 2013 Mark Wielaard <mjw@redhat.com> 0.157-1
- Update to 0.157.
- Remove elfutils-0.156-abi_cfi-ppc-s390-arm.patch.
- Remove elfutils-0.156-et_dyn-kernels.patch.

* Fri Sep 06 2013 Mark Wielaard <mjw@redhat.com> 0.156-5
- Add elfutils-0.156-abi_cfi-ppc-s390-arm.patch.
  Sets up initial CFI return register, CFA location expression and
  register rules for PPC, S390 and ARM (dwarf_cfi_addrframe support).

* Mon Aug 26 2013 Mark Wielaard <mjw@redhat.com> 0.156-4
- Add elfutils-0.156-et_dyn-kernels.patch.
  Fixes an issue on ppc64 with systemtap kernel address placement.

* Thu Aug  8 2013 Mark Wielaard <mjw@redhat.com> 0.156-3
- Make check can now also be ran in parallel.

* Thu Jul 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> 0.156-2
- Update the %%configure command for compatibility with fc20 Koji.

* Thu Jul 25 2013 Jan Kratochvil <jan.kratochvil@redhat.com> 0.156-1
- Update to 0.156.
  - #890447 - Add __bss_start and __TMC_END__ to elflint.
  - #909481 - Only try opening files with installed compression libraries.
  - #914908 - Add __bss_start__ to elflint.
  - #853757 - Updated Polish translation.
  - #985438 - Incorrect prototype of __libdwfl_find_elf_build_id.
  - Drop upstreamed elfutils-0.155-binutils-pr-ld-13621.patch.
  - Drop upstreamed elfutils-0.155-mem-align.patch.
  - Drop upstreamed elfutils-0.155-sizeof-pointer-memaccess.patch.

* Tue Jul 02 2013 Karsten Hopp <karsten@redhat.com> 0.155-6
- bump release and rebuild to fix dependencies on PPC

* Sun Feb 24 2013 Mark Wielaard <mjw@redhat.com> - 0.155-5
- Add ARM variant to elfutils-0.155-binutils-pr-ld-13621.patch rhbz#914908.
- rhel >= 5 has xz-devel

* Fri Feb 22 2013 Mark Wielaard <mjw@redhat.com> - 0.155-4
- Replace elfutils-0.155-binutils-pr-ld-13621.patch with upstream fix.

* Thu Jan 24 2013 Mark Wielaard <mjw@redhat.com> - 0.155-3
- Backport sizeof-pointer-memaccess upstream fixes.

* Thu Jan 10 2013 Mark Wielaard <mjw@redhat.com> - 0.155-2
- #891553 - unaligned memory access issues.

* Mon Aug 27 2012 Mark Wielaard <mjw@redhat.com> - 0.155-1
- Update to 0.155.
  - #844270 - eu-nm invalid %%N$ use detected.
  - #847454 - Ukrainian translation update.
  - Removed local ar 64-bit symbol patch, dwz support patch and xlatetom fix.

* Tue Aug 14 2012 Petr Machata <pmachata@redhat.com> - 0.154-4
- Add support for archives with 64-bit symbol tables (#843019)

* Wed Aug 01 2012 Mark Wielaard <mjw@redhat.com> 0.154-3
- Add dwz support

* Wed Jul 18 2012 Mark Wielaard <mjw@redhat.com> 0.154-2
- Add upstream xlatetom fix (#835877)

* Mon Jul 02 2012 Karsten Hopp <karsten@redhat.com> 0.154-1.1
- disable unstrip-n check for now (835877)

* Fri Jun 22 2012 Mark Wielaard <mjw@redhat.com> - 0.154-1
- Update to 0.154
  - elflint doesn't recognize SHF_INFO_LINK on relocation sections (#807823)
  - Update license to GPLv3+ and (GPLv2+ or LGPLv3+)
  - Remove elfutils-0.153-dwfl_segment_report_module.patch
- Add elfutils-0.154-binutils-pr-ld-13621.patch

* Mon Apr 02 2012 Mark Wielaard <mark@klomp.org> - 0.153-2
- Fix for eu-unstrip emits garbage for librt.so.1 (#805447)

* Thu Feb 23 2012 Mark Wielaard <mjw@redhat.com> - 0.153-1
- Update to 0.153
  - New --disable-werror for portability.
  - Support for .zdebug sections (#679777)
  - type_units and DW_AT_GNU_odr_signature support (#679815)
  - low level support DW_OP_GNU_entry_value and DW_TAG_GNU_call_site (#688090)
  - FTBFS on rawhide with gcc 4.7 (#783506)
    - Remove gcc-4.7 patch

* Fri Jan 20 2012 Mark Wielaard <mjw@redhat.com> - 0.152-3
- Fixes for gcc-4.7 based on upstream commit 32899a (#783506).

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.152-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 15 2011 Roland McGrath <roland@redhat.com> - 0.152-1
- Update to 0.152
  - Various build and warning nits fixed for newest GCC and Autoconf.
  - libdwfl: Yet another prelink-related fix for another regression. (#674465)
  - eu-elfcmp: New flag --ignore-build-id to ignore differing build ID bits.
  - eu-elfcmp: New flag -l/--verbose to print all differences.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.151-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Roland McGrath <roland@redhat.com> - 0.151-1
- Update to 0.151
  - libdwfl: Fix for more prelink cases with separate debug file.
  - eu-strip: New flag --strip-sections to remove section headers entirely.

* Thu Dec  2 2010 Roland McGrath <roland@redhat.com> - 0.150-2
- libdwfl: Remove bogus assert. (#658268)

* Tue Nov 23 2010 Roland McGrath <roland@redhat.com> - 0.150-1
- Update to 0.150
  - libdw: Fix for handling huge .debug_aranges section. (#638432)
  - libdwfl: Fix for handling prelinked DSO with separate debug file. (#652857)
  - findtextrel: Fix diagnostics to work with usual section ordering.

* Wed Sep 29 2010 jkeating - 0.149-2
- Rebuilt for gcc bug 634757

* Mon Sep 13 2010 Roland McGrath <roland@redhat.com> - 0.149-1
- Update to 0.149
  - libdw: Decode new DW_OP_GNU_implicit_pointer operation;
           new function dwarf_getlocation_implicit_pointer.
  - libdwfl: New function dwfl_dwarf_line.
  - eu-addr2line: New flag -F/--flags to print more DWARF line info details.
  - eu-readelf: better .debug_loc processing (#627729)
  - eu-strings: Fix non-mmap file reading. (#609468)
  - eu-strip: -g recognizes .gdb_index as a debugging section. (#631997)

* Mon Jun 28 2010 Roland McGrath <roland@redhat.com> - 0.148-1
- Update to 0.148
  - libdw: Accept DWARF 4 format: new functions dwarf_next_unit,
           dwarf_offdie_types.
           New functions dwarf_lineisa, dwarf_linediscriminator,
           dwarf_lineop_index.
  - libdwfl: Fixes in core-file handling, support cores from PIEs. (#588818)
             When working from build IDs, don't open a named file
             that mismatches.
  - readelf: Handle DWARF 4 formats.

* Mon May  3 2010 Roland McGrath <roland@redhat.com> - 0.147-1
- Update to 0.147

* Wed Apr 21 2010 Roland McGrath <roland@redhat.com> - 0.146-1
- Update to 0.146
  - libdwfl: New function dwfl_core_file_report.
  - libelf: Fix handling of phdrs in truncated file. (#577310)
  - libdwfl: Fix infinite loop handling clobbered link_map. (#576379)
- Package translations.

* Tue Feb 23 2010 Roland McGrath <roland@redhat.com> - 0.145-1
- Update to 0.145
  - Fix build with --disable-dependency-tracking. (#564646)
  - Fix build with most recent glibc headers.
  - libdw: Fix CFI decoding. (#563528)
  - libdwfl: Fix address bias returned by CFI accessors. (#563528)
             Fix core file module layout identification. (#559836)
  - readelf: Fix CFI decoding.

* Fri Jan 15 2010 Roland McGrath <roland@redhat.com> - 0.144-2
- Fix sloppy #include's breaking build with F-13 glibc.

* Thu Jan 14 2010 Roland McGrath <roland@redhat.com> - 0.144-1
- Update to 0.144
  - libdw: New function dwarf_aggregate_size for computing (constant) type
           sizes, including array_type cases with nontrivial calculation.
  - readelf: Don't give errors for missing info under -a.
             Handle Linux "VMCOREINFO" notes under -n.
- Resolves: RHBZ #527004, RHBZ #530704, RHBZ #550858

* Mon Sep 21 2009 Roland McGrath <roland@redhat.com> - 0.143-1
- Update to 0.143
  - libdw: Various convenience functions for individual attributes now use
           dwarf_attr_integrate to look up indirect inherited attributes.
           Location expression handling now supports DW_OP_implicit_value.
  - libdwfl: Support automatic decompression of files in XZ format,
             and of Linux kernel images made with bzip2 or LZMA
             (as well as gzip).

* Tue Jul 28 2009 Roland McGrath <roland@redhat.com> - 0.142-1
- Update to 0.142
  - libelf: Bug fix in filling gaps between sections. (#512840)
  - libelf: Add elf_getshdrnum alias for elf_getshnum and elf_getshdrstrndx
            alias for elf_getshstrndx and deprecate original names.
  - libebl, elflint: Add support for STB_GNU_UNIQUE. (#511436)
  - readelf: Add -N option, speeds up DWARF printing
             without address->name lookups. (#505347)
  - libdw: Add support for decoding DWARF CFI into location description form.
           Handle some new DWARF 3 expression operations previously omitted.
           Basic handling of some new encodings slated for DWARF 4.

* Thu Apr 23 2009 Roland McGrath <roland@redhat.com> - 0.141-1
- Update to 0.141
  - libebl: sparc backend fixes (#490585)
            some more arm backend support
  - libdwfl: fix dwfl_module_build_id for prelinked DSO case (#489439)
             fixes in core file support (#494858)
             dwfl_module_getsym interface improved for non-address symbols
  - eu-strip: fix infinite loop on strange inputs with -f
  - eu-addr2line: take -j/--section=NAME option for binutils compatibility
                  (same effect as '(NAME)0x123' syntax already supported)
- Resolves: RHBZ #495213, RHBZ #465872, RHBZ #470055, RHBZ #484623

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.140-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb 15 2009 Roland McGrath <roland@redhat.com> - 0.140-1
- Update to 0.140
  - libelf: Fix regression in creation of section header. (#484946)

* Fri Jan 23 2009 Roland McGrath <roland@redhat.com> - 0.139-1
- Update to 0.139
  - libcpu: Add Intel SSE4 disassembler support
  - readelf: Implement call frame information and exception handling dumping.
             Add -e option.  Enable it implicitly for -a.
  - elflint: Check PT_GNU_EH_FRAME program header entry.
  - libdwfl: Support automatic gzip/bzip2 decompression of ELF files. (#472136)

* Thu Jan  1 2009 Roland McGrath <roland@redhat.com> - 0.138-2
- Fix libelf regression.

* Wed Dec 31 2008 Roland McGrath <roland@redhat.com> - 0.138-1
- Update to 0.138
  - Install <elfutils/version.h> header file for applications to use in
    source version compatibility checks.
  - libebl: backend fixes for i386 TLS relocs; backend support for NT_386_IOPERM
  - libcpu: disassembler fixes (#469739)
  - libdwfl: bug fixes (#465878)
  - libelf: bug fixes
  - eu-nm: bug fixes for handling corrupt input files (#476136)

* Wed Oct  1 2008 Roland McGrath <roland@redhat.com> - 0.137-3
- fix libdwfl regression (#462689)

* Thu Aug 28 2008 Roland McGrath <roland@redhat.com> - 0.137-2
- Update to 0.137
  - libdwfl: bug fixes; new segment interfaces;
             all the libdwfl-based tools now support --core=COREFILE option
- Resolves: RHBZ #325021, RHBZ #447416

* Mon Jul  7 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.135-2
- fix conditional comparison

* Mon May 12 2008 Roland McGrath <roland@redhat.com> - 0.135-1
- Update to 0.135
  - libdwfl: bug fixes
  - eu-strip: changed handling of ET_REL files wrt symbol tables and relocs

* Wed Apr  9 2008 Roland McGrath <roland@redhat.com> - 0.134-1
- Update to 0.134
  - elflint: backend improvements for sparc, alpha (#204170)
  - libdwfl, libelf: bug fixes (#439344, #438867, #438263, #438190)
- Remove Conflicts: libelf-devel from elfutils-libelf-devel. (#435742)

* Sun Mar  2 2008 Roland McGrath <roland@redhat.com> - 0.133-2
- Update to 0.133
  - readelf, elflint, libebl: SHT_GNU_ATTRIBUTE section handling (readelf -A)
  - readelf: core note handling for NT_386_TLS, NT_PPC_SPE, Alpha NT_AUXV
  - libdwfl: bug fixes and optimization in relocation handling
  - elfcmp: bug fix for non-allocated section handling
  - ld: implement newer features of binutils linker.
- Install eu-objdump and libasm, now has limited disassembler support.

* Mon Jan 21 2008 Roland McGrath <roland@redhat.com> - 0.132-3
- Update to 0.132
  - libelf: Use loff_t instead of off64_t in libelf.h header. (#377241)
  - eu-readelf: Fix handling of ET_REL files in archives.
  - libcpu: Implement x86 and x86-64 disassembler.
  - libasm: Add interface for disassembler.
  - all programs: add debugging of branch prediction.
  - libelf: new function elf_scnshndx.

* Sun Nov 11 2007 Roland McGrath <roland@redhat.com> - 0.131-1
- Update to 0.131
  - libdw: DW_FORM_ref_addr support; dwarf_formref entry point now deprecated;
           bug fixes for oddly-formatted DWARF
  - libdwfl: bug fixes in offline archive support, symbol table handling;
             apply partial relocations for dwfl_module_address_section on ET_REL
  - libebl: powerpc backend support for Altivec registers

* Wed Oct 17 2007 Roland McGrath <roland@redhat.com> - 0.130-3
- Fix ET_REL support.
- Fix odd indentation in eu-readelf -x output.

* Tue Oct 16 2007 Roland McGrath <roland@redhat.com> - 0.130-1
- Update to 0.130
  - eu-readelf -p option can take an argument like -x for one section
  - eu-readelf --archive-index (or -c)
  - eu-readelf -n improved output for core dumps
  - eu-readelf: handle SHT_NOTE sections without requiring phdrs (#249467)
  - eu-elflint: ditto
  - eu-elflint: stricter checks on debug sections
  - eu-unstrip: new options, --list (or -n), --relocate (or -R)
  - libelf: new function elf_getdata_rawchunk, replaces gelf_rawchunk;
            new functions gelf_getnote, gelf_getauxv, gelf_update_auxv
  - libebl: backend improvements (#324031)
  - libdwfl: build_id support, new functions for it
  - libdwfl: dwfl_module_addrsym fixes (#268761, #268981)
  - libdwfl offline archive support, new script eu-make-debug-archive

* Mon Aug 20 2007 Roland McGrath <roland@redhat.com> - 0.129-2
- Fix false-positive eu-elflint failure on ppc -mbss-plt binaries.

* Tue Aug 14 2007 Roland McGrath <roland@redhat.com> - 0.129-1
- Update to 0.129
  - readelf: new options --hex-dump (or -x), --strings (or -p) (#250973)
  - addr2line: new option --symbols (or -S)
  - libdw: dwarf_getscopes fixes (#230235)
  - libdwfl: dwfl_module_addrsym fixes (#249490)

* Fri Jun  8 2007 Roland McGrath <roland@redhat.com> - 0.128-2
- Update to 0.128
  - new program: unstrip
  - elfcmp: new option --hash-inexact
- Replace Conflicts: with Provides/Requires using -arch

* Wed Apr 18 2007 Roland McGrath <roland@redhat.com> - 0.127-1
- Update to 0.127
  - libdw: new function dwarf_getsrcdirs
  - libdwfl: new functions dwfl_module_addrsym, dwfl_report_begin_add,
             dwfl_module_address_section

* Mon Feb  5 2007 Roland McGrath <roland@redhat.com> - 0.126-1
- Update to 0.126
  - New program eu-ar.
  - libdw: fix missing dwarf_getelf (#227206)
  - libdwfl: dwfl_module_addrname for st_size=0 symbols (#227167, #227231)

* Wed Jan 10 2007 Roland McGrath <roland@redhat.com> - 0.125-3
- Fix overeager warn_unused_result build failures.

* Wed Jan 10 2007 Roland McGrath <roland@redhat.com> - 0.125-1
- Update to 0.125
  - elflint: Compare DT_GNU_HASH tests.
  - move archives into -static RPMs
  - libelf, elflint: better support for core file handling
  - Really fix libdwfl sorting of modules with 64-bit addresses (#220817).
- Resolves: RHBZ #220817, RHBZ #213792

* Tue Oct 10 2006 Roland McGrath <roland@redhat.com> - 0.124-1
- eu-strip -f: copy symtab into debuginfo file when relocs use it (#203000)
- Update to 0.124
  - libebl: fix ia64 reloc support (#206981)
  - libebl: sparc backend support for return value location
  - libebl, libdwfl: backend register name support extended with more info
  - libelf, libdw: bug fixes for unaligned accesses on machines that care
  - readelf, elflint: trivial bugs fixed

* Mon Aug 14 2006 Roland McGrath <roland@redhat.com> 0.123-1
- Update to 0.123
  - libebl: Backend build fixes, thanks to Stepan Kasal.
  - libebl: ia64 backend support for register names, return value location
  - libdwfl: Handle truncated linux kernel module section names.
  - libdwfl: Look for linux kernel vmlinux files with .debug suffix.
  - elflint: Fix checks to permit --hash-style=gnu format.

* Mon Jul 17 2006 Roland McGrath <roland@redhat.com> - 0.122-4
- Fix warnings in elflint compilation.

* Wed Jul 12 2006 Roland McGrath <roland@redhat.com> - 0.122-3
- Update to 0.122
  - Fix libdwfl sorting of modules with 64-bit addresses (#198225).
  - libebl: add function to test for relative relocation
  - elflint: fix and extend DT_RELCOUNT/DT_RELACOUNT checks
  - elflint, readelf: add support for DT_GNU_HASH
  - libelf: add elf_gnu_hash
  - elflint, readelf: add support for 64-bit SysV-style hash tables
  - libdwfl: new functions dwfl_module_getsymtab, dwfl_module_getsym.

* Thu Jun 15 2006 Roland McGrath <roland@redhat.com> - 0.121-1
- Update to 0.121
  - libelf: bug fixes for rewriting existing files when using mmap (#187618).
  - make all installed headers usable in C++ code (#193153).
  - eu-readelf: better output format.
  - eu-elflint: fix tests of dynamic section content.
  - libdw, libdwfl: handle files without aranges info.

* Thu May 25 2006 Jeremy Katz <katzj@redhat.com> - 0.120-3
- rebuild to pick up -devel deps

* Tue Apr  4 2006 Roland McGrath <roland@redhat.com> - 0.120-2
- Update to 0.120
  - License changed to GPL, with some exceptions for using
    the libelf, libebl, libdw, and libdwfl library interfaces.
    Red Hat elfutils is an included package of the Open Invention Network.
  - dwarf.h updated for DWARF 3.0 final specification.
  - libelf: Fix corruption in ELF_C_RDWR uses (#187618).
  - libdwfl: New function dwfl_version; fixes for offline.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.119-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.119-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Jan 13 2006 Roland McGrath <roland@redhat.com> - 0.119-1
- update to 0.119

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 27 2005 Roland McGrath <roland@redhat.com> - 0.118-1
- update to 0.118
  - elflint: more tests.
  - libdwfl: New function dwfl_module_register_names.
  - libebl: New backend hook for register names.
- Make sure -fexceptions is always in CFLAGS.

* Tue Nov 22 2005 Roland McGrath <roland@redhat.com> - 0.117-2
- update to 0.117
  - libdwfl: New function dwfl_module_return_value_location (#166118)
  - libebl: Backend improvements for several CPUs

* Mon Oct 31 2005 Roland McGrath <roland@redhat.com> - 0.116-1
- update to 0.116
  - libdw fixes, API changes and additions
  - libdwfl fixes (#169672)
  - eu-strip/libelf fix to preserve setuid/setgid permission bits (#167745)

* Fri Sep  9 2005 Roland McGrath <roland@redhat.com> - 0.115-3
- Update requires/conflicts for better biarch update behavior.

* Mon Sep  5 2005 Roland McGrath <roland@redhat.com> - 0.115-2
- update to 0.115
  - New program eu-strings.
  - libdw: New function dwarf_getscopes_die.
  - libelf: speed-ups of non-mmap reading.
  - Implement --enable-gcov option for configure.

* Wed Aug 24 2005 Roland McGrath <roland@redhat.com> - 0.114-1
- update to 0.114
  - new program eu-ranlib
  - libdw: new calls for inlines
  - libdwfl: new calls for offline modules

* Sat Aug 13 2005 Roland McGrath <roland@redhat.com> - 0.113-2
- update to 0.113
  - elflint: relax a bit.  Allow version definitions for defined symbols
    against DSO versions also for symbols in nobits sections.
    Allow .rodata section to have STRINGS and MERGE flag set.
  - strip: add some more compatibility with binutils.
  - libdwfl: bug fixes.
- Separate libdw et al into elfutils-libs subpackage.

* Sat Aug  6 2005 Roland McGrath <roland@redhat.com> - 0.112-1
- update to 0.112
  - elfcmp: some more relaxation.
  - elflint: many more tests, especially regarding to symbol versioning.
  - libelf: Add elfXX_offscn and gelf_offscn.
  - libasm: asm_begin interface changes.
  - libebl: Add three new interfaces to directly access machine, class,
    and data encoding information.

* Fri Jul 29 2005 Roland McGrath <roland@redhat.com> - 0.111-2
- update portability patch

* Thu Jul 28 2005 Roland McGrath <roland@redhat.com> - 0.111-1
- update to 0.111
  - libdwfl library now merged into libdw

* Sun Jul 24 2005 Roland McGrath <roland@redhat.com> - 0.110-1
- update to 0.110

* Fri Jul 22 2005 Roland McGrath <roland@redhat.com> - 0.109-2
- update to 0.109
  - verify that libebl modules are from the same build
  - new eu-elflint checks on copy relocations
  - new program eu-elfcmp
  - new experimental libdwfl library

* Thu Jun  9 2005 Roland McGrath <roland@redhat.com> - 0.108-5
- robustification of eu-strip and eu-readelf

* Wed May 25 2005 Roland McGrath <roland@redhat.com> - 0.108-3
- more robustification

* Mon May 16 2005 Roland McGrath <roland@redhat.com> - 0.108-2
- robustification

* Mon May  9 2005 Roland McGrath <roland@redhat.com> - 0.108-1
- update to 0.108
  - merge strip fixes
  - sort records in dwarf_getsrclines, fix dwarf_getsrc_die searching
  - update elf.h from glibc

* Sun May  8 2005 Roland McGrath <roland@redhat.com> - 0.107-2
- fix strip -f byte-swapping bug

* Sun May  8 2005 Roland McGrath <roland@redhat.com> - 0.107-1
- update to 0.107
  - readelf: improve DWARF output format
  - elflint: -d option to support checking separate debuginfo files
  - strip: fix ET_REL debuginfo files (#156341)

* Mon Apr  4 2005 Roland McGrath <roland@redhat.com> - 0.106-3
- fix some bugs in new code, reenable make check

* Mon Apr  4 2005 Roland McGrath <roland@redhat.com> - 0.106-2
- disable make check for most arches, for now

* Mon Apr  4 2005 Roland McGrath <roland@redhat.com> - 0.106-1
- update to 0.106

* Mon Mar 28 2005 Roland McGrath <roland@redhat.com> - 0.104-2
- update to 0.104

* Wed Mar 23 2005 Jakub Jelinek <jakub@redhat.com> 0.103-2
- update to 0.103

* Wed Feb 16 2005 Jakub Jelinek <jakub@redhat.com> 0.101-2
- update to 0.101.
- use %%configure macro to get CFLAGS etc. right

* Sat Feb  5 2005 Jeff Johnson <jbj@redhat.com> 0.99-2
- upgrade to 0.99.

* Sun Sep 26 2004 Jeff Johnson <jbj@redhat.com> 0.97-3
- upgrade to 0.97.

* Tue Aug 17 2004 Jakub Jelinek <jakub@redhat.com> 0.95-5
- upgrade to 0.96.

* Mon Jul  5 2004 Jakub Jelinek <jakub@redhat.com> 0.95-4
- rebuilt with GCC 3.4.x, workaround VLA + alloca mixing
  warning

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr  2 2004 Jeff Johnson <jbj@redhat.com> 0.95-2
- upgrade to 0.95.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 0.94-1
- upgrade to 0.94

* Fri Jan 16 2004 Jakub Jelinek <jakub@redhat.com> 0.93-1
- upgrade to 0.93

* Thu Jan  8 2004 Jakub Jelinek <jakub@redhat.com> 0.92-1
- full version
- macroized spec file for GPL or OSL builds
- include only libelf under GPL plus wrapper scripts

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 0.91-2
- macroized spec file for GPL or OSL builds

* Wed Jan  7 2004 Ulrich Drepper <drepper@redhat.com>
- split elfutils-devel into two packages.

* Wed Jan  7 2004 Jakub Jelinek <jakub@redhat.com> 0.91-1
- include only libelf under GPL plus wrapper scripts

* Tue Dec 23 2003 Jeff Johnson <jbj@redhat.com> 0.89-3
- readelf, not readline, in %%description (#111214).

* Fri Sep 26 2003 Bill Nottingham <notting@redhat.com> 0.89-1
- update to 0.89 (fix eu-strip)

* Tue Sep 23 2003 Jakub Jelinek <jakub@redhat.com> 0.86-3
- update to 0.86 (fix eu-strip on s390x/alpha)
- libebl is an archive now; remove references to DSO

* Mon Jul 14 2003 Jeff Johnson <jbj@redhat.com> 0.84-3
- upgrade to 0.84 (readelf/elflint improvements, rawhide bugs fixed).

* Fri Jul 11 2003 Jeff Johnson <jbj@redhat.com> 0.83-3
- upgrade to 0.83 (fix invalid ELf handle on *.so strip, more).

* Wed Jul  9 2003 Jeff Johnson <jbj@redhat.com> 0.82-3
- upgrade to 0.82 (strip tests fixed on big-endian).

* Tue Jul  8 2003 Jeff Johnson <jbj@redhat.com> 0.81-3
- upgrade to 0.81 (strip excludes unused symtable entries, test borked).

* Thu Jun 26 2003 Jeff Johnson <jbj@redhat.com> 0.80-3
- upgrade to 0.80 (debugedit changes for kernel in progress).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 21 2003 Jeff Johnson <jbj@redhat.com> 0.79-2
- upgrade to 0.79 (correct formats for size_t, more of libdw "works").

* Mon May 19 2003 Jeff Johnson <jbj@redhat.com> 0.78-2
- upgrade to 0.78 (libdwarf bugfix, libdw additions).

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- debuginfo rebuild

* Thu Feb 20 2003 Jeff Johnson <jbj@redhat.com> 0.76-2
- use the correct way of identifying the section via the sh_info link.

* Sat Feb 15 2003 Jakub Jelinek <jakub@redhat.com> 0.75-2
- update to 0.75 (eu-strip -g fix)

* Tue Feb 11 2003 Jakub Jelinek <jakub@redhat.com> 0.74-2
- update to 0.74 (fix for writing with some non-dirty sections)

* Thu Feb  6 2003 Jeff Johnson <jbj@redhat.com> 0.73-3
- another -0.73 update (with sparc fixes).
- do "make check" in %%check, not %%install, section.

* Mon Jan 27 2003 Jeff Johnson <jbj@redhat.com> 0.73-2
- update to 0.73 (with s390 fixes).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Jakub Jelinek <jakub@redhat.com> 0.72-4
- fix arguments to gelf_getsymshndx and elf_getshstrndx
- fix other warnings
- reenable checks on s390x

* Sat Jan 11 2003 Karsten Hopp <karsten@redhat.de> 0.72-3
- temporarily disable checks on s390x, until someone has
  time to look at it

* Thu Dec 12 2002 Jakub Jelinek <jakub@redhat.com> 0.72-2
- update to 0.72

* Wed Dec 11 2002 Jakub Jelinek <jakub@redhat.com> 0.71-2
- update to 0.71

* Wed Dec 11 2002 Jeff Johnson <jbj@redhat.com> 0.69-4
- update to 0.69.
- add "make check" and segfault avoidance patch.
- elfutils-libelf needs to run ldconfig.

* Tue Dec 10 2002 Jeff Johnson <jbj@redhat.com> 0.68-2
- update to 0.68.

* Fri Dec  6 2002 Jeff Johnson <jbj@redhat.com> 0.67-2
- update to 0.67.

* Tue Dec  3 2002 Jeff Johnson <jbj@redhat.com> 0.65-2
- update to 0.65.

* Mon Dec  2 2002 Jeff Johnson <jbj@redhat.com> 0.64-2
- update to 0.64.

* Sun Dec 1 2002 Ulrich Drepper <drepper@redhat.com> 0.64
- split packages further into elfutils-libelf

* Sat Nov 30 2002 Jeff Johnson <jbj@redhat.com> 0.63-2
- update to 0.63.

* Fri Nov 29 2002 Ulrich Drepper <drepper@redhat.com> 0.62
- Adjust for dropping libtool

* Sun Nov 24 2002 Jeff Johnson <jbj@redhat.com> 0.59-2
- update to 0.59

* Thu Nov 14 2002 Jeff Johnson <jbj@redhat.com> 0.56-2
- update to 0.56

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 0.54-2
- update to 0.54

* Sun Oct 27 2002 Jeff Johnson <jbj@redhat.com> 0.53-2
- update to 0.53
- drop x86_64 hack, ICE fixed in gcc-3.2-11.

* Sat Oct 26 2002 Jeff Johnson <jbj@redhat.com> 0.52-3
- get beehive to punch a rhpkg generated package.

* Wed Oct 23 2002 Jeff Johnson <jbj@redhat.com> 0.52-2
- build in 8.0.1.
- x86_64: avoid gcc-3.2 ICE on x86_64 for now.

* Tue Oct 22 2002 Ulrich Drepper <drepper@redhat.com> 0.52
- Add libelf-devel to conflicts for elfutils-devel

* Mon Oct 21 2002 Ulrich Drepper <drepper@redhat.com> 0.50
- Split into runtime and devel package

* Fri Oct 18 2002 Ulrich Drepper <drepper@redhat.com> 0.49
- integrate into official sources

* Wed Oct 16 2002 Jeff Johnson <jbj@redhat.com> 0.46-1
- Swaddle.
