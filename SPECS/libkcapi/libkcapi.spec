## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 7;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Shared object version of libkcapi.
%global vmajor            1
%global vminor            5
%global vpatch            0

# Do we build the replacements packages?
%bcond_with replace_coreutils
# Replace fipscheck by default in Fedora 33+:
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%bcond_without replace_fipscheck
%else
%bcond_with replace_fipscheck
%endif
# Replace hmaccalc by default in Fedora 28+:
%if 0%{?fedora} >= 28 || 0%{?rhel} >= 8
%bcond_without replace_hmaccalc
%else
%bcond_with replace_hmaccalc
%endif
%if 0%{?fedora} >= 29 || 0%{?rhel} >= 8
%bcond_without test_package
%else
%bcond_with test_package
%endif
# disable cppcheck analysis in ELN/RHEL to avoid the dependency bz#1931518
%if 0%{?rhel}
%bcond_with cppcheck
%else
%bcond_without cppcheck
%endif

# Use `--without test` to build without running the tests
%bcond_without test
# Use `--without fuzz_test` to skip the fuzz test during build
%bcond_without fuzz_test
# Use `--without doc` to build without the -doc subpackage
%bcond_without doc
# Use `--without clang_sa` to skip clang static analysis during build
%bcond_without clang_sa

# This package needs at least Linux Kernel v4.10.0.
%global min_kernel_ver    4.10.0

# Do we need to tweak sysctl.d? In newer versions of the Linux
# Kernel the default ancillary buffer size is set high enough.
# TODO: Adapt this when the patch for net/core/sock.c is merged.
%if %{lua:print(rpm.vercmp('99.0.0', posix.uname('%r')));} >= 0
%global with_sysctl_tweak 1
%else
%global with_sysctl_tweak 0
%endif

%if %{with_sysctl_tweak}
# Priority for the sysctl.d preset.
%global sysctl_prio       50

# Value used for the sysctl.d preset.
%global sysctl_optmem_max 81920

# Extension for the README.distro file.
%global distroname_ext    %{?fedora:fedora}%{?rhel:redhat}
%endif

# Lowest limit to run the testsuite.  If we cannot obtain this
# value, we asume the testsuite cannot be run.
%global test_optmem_max   %(%{__cat} /proc/sys/net/core/optmem_max || echo 0)

# For picking patches from upstream commits or pull requests.
%global giturl            https://github.com/smuellerDD/%{name}

# Do we replace some coreutils?
%if %{with replace_coreutils}
# TODO: Adapt this when replacing some coreutils initially.
%global coreutils_evr     8.29-1%{?dist}
%endif

# Do we replace fipscheck?
%if %{with replace_fipscheck}
%global fipscheck_evr     1.5.0-9
%endif

# Do we replace hmaccalc?
%if %{with replace_hmaccalc}
%global hmaccalc_evr      0.9.14-10%{?dist}
%endif

%global apps_coreutils sha1sum sha224sum sha256sum sha384sum sha512sum md5sum sm3sum
%global apps_hmaccalc sha1hmac sha224hmac sha256hmac sha384hmac sha512hmac sm3hmac
%global apps_fipscheck fipscheck fipshmac

# On old kernels use mock hashers implemented via openssl
%if %{lua:print(rpm.vercmp(posix.uname('%r'), '3.19'));} >= 0
%global sha512hmac bin/kcapi-hasher -n sha512hmac
%global fipshmac   bin/kcapi-hasher -n fipshmac
%else
%global sha512hmac bash %{SOURCE2}
%global fipshmac   bash %{SOURCE3}
%endif

# Add generation of HMAC checksum of the final stripped
# binary.  %%define with lazy globbing is used here
# intentionally, because using %%global does not work.
%define __spec_install_post                                      \
%{?__debug_package:%{__debug_install_post}}                      \
%{__arch_install_post}                                           \
%{__os_install_post}                                             \
bin_path=%{buildroot}%{_bindir}                                  \
lib_path=%{buildroot}%{_libdir}                                  \
{ %sha512hmac "$bin_path"/kcapi-hasher || exit 1; } |            \\\
  cut -f 1 -d ' ' >"$lib_path"/hmaccalc/kcapi-hasher.hmac        \
{ %sha512hmac "$lib_path"/libkcapi.so.%{version} || exit 1; } |  \\\
  cut -f 1 -d ' ' >"$lib_path"/hmaccalc/libkcapi.so.%{version}.hmac \
%{__ln_s} libkcapi.so.%{version}.hmac                            \\\
  "$lib_path"/hmaccalc/libkcapi.so.%{vmajor}.hmac                \
%{nil}

Name:           libkcapi
Version:        %{vmajor}.%{vminor}.%{vpatch}
Release:        %autorelease
Summary:        User space interface to the Linux Kernel Crypto API

License:        BSD-3-Clause OR GPL-2.0-only
URL:            https://www.chronox.de/%{name}/
Source0:        https://www.chronox.de/%{name}/releases/%{version}/%{name}-%{version}.tar.xz
Source1:        https://www.chronox.de/%{name}/releases/%{version}/%{name}-%{version}.tar.xz.asc
Source2:        sha512hmac-openssl.sh
Source3:        fipshmac-openssl.sh

BuildRequires:  bash
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  git-core
BuildRequires:  hardlink
BuildRequires:  kernel-headers >= %{min_kernel_ver}
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  perl-interpreter
BuildRequires:  systemd
BuildRequires:  xmlto
%if %{with doc}
BuildRequires:  docbook-utils-pdf
%endif
%if %{with clang_sa}
BuildRequires:  clang
%endif
%if %{with cppcheck}
BuildRequires:  cppcheck >= 2.4
%endif

# For ownership of %%{_sysctldir}.
Requires:       systemd

Obsoletes:      %{name}-replacements <= %{version}-%{release}

%description
libkcapi allows user-space to access the Linux kernel crypto API.

This library uses the netlink interface and exports easy to use APIs
so that a developer does not need to consider the low-level netlink
interface handling.

The library does not implement any cipher algorithms.  All consumer
requests are sent to the kernel for processing.  Results from the
kernel crypto API are returned to the consumer via the library API.

The kernel interface and therefore this library can be used by
unprivileged processes.


%package        devel
Summary:        Development files for the %{name} package
Requires:       %{name}%{?_isa} == %{version}-%{release}

%description    devel
Header files for applications that use %{name}.


%if %{with doc}
%package        doc
Summary:        User documentation for the %{name} package
BuildArch:      noarch
# Depend on one of the base packages because they have the license files
# We cannot just bundle them into doc because they might conflict with an
# older or newer version of the base package.
Requires:       %{name} == %{version}-%{release}

%description    doc
User documentation for %{name}.
%endif


%package        hasher
Summary:        Common %{name} hashing application
Requires:       %{name}%{?_isa}    == %{version}-%{release}

%description    hasher
Provides The kcapi-hasher binary used by other %{name} subpackages.


%if %{with replace_coreutils}
%package        checksum
Summary:        Drop-in replacement for *sum utils provided by the %{name} package
Requires:       %{name}-hasher%{?_isa} == %{version}-%{release}

Requires:       coreutils%{?_isa}  >= %{coreutils_evr}

Conflicts:      coreutils          < %{coreutils_evr}
Conflicts:      coreutils-single

%description    checksum
Provides drop-in replacements for sha*sum tools (from package
coreutils) using %{name}.
%endif


%if %{with replace_fipscheck}
%package        fipscheck
Summary:        Drop-in replacements for fipscheck/fipshmac provided by the %{name} package
Requires:       %{name}-hasher%{?_isa} == %{version}-%{release}

Obsoletes:      fipscheck         <= %{fipscheck_evr}

Provides:       fipscheck         == %{fipscheck_evr}.1
Provides:       fipscheck%{?_isa} == %{fipscheck_evr}.1

%description    fipscheck
Provides drop-in replacements for fipscheck and fipshmac tools (from
package fipscheck) using %{name}.
%endif


%if %{with replace_hmaccalc}
%package        hmaccalc
Summary:        Drop-in replacements for hmaccalc provided by the %{name} package
Requires:       %{name}-hasher%{?_isa} == %{version}-%{release}

Obsoletes:      hmaccalc          <= %{hmaccalc_evr}

Provides:       hmaccalc          == %{hmaccalc_evr}.1
Provides:       hmaccalc%{?_isa}  == %{hmaccalc_evr}.1

%description    hmaccalc
Provides drop-in replacements for sha*hmac tools (from package
hmaccalc) using %{name}.
%endif


%package        static
Summary:        Static library for -static linking with %{name}
Requires:       %{name}-devel%{?_isa} == %{version}-%{release}

%description    static
This package contains the %{name} static libraries for -static
linking.  You don't need this, unless you link statically, which
is highly discouraged.


%package        tools
Summary:        Utility applications for the %{name} package
Requires:       %{name}%{?_isa}        == %{version}-%{release}
Requires:       %{name}-hasher%{?_isa} == %{version}-%{release}

%description    tools
Utility applications that are provided with %{name}.  This includes
tools to use message digests, symmetric ciphers and random number
generators implemented in the Linux kernel from command line.


%if %{with test_package}
%package        tests
Summary:        Testing scripts for the %{name} package
Requires:       %{name}%{?_isa}       == %{version}-%{release}
Requires:       %{name}-tools%{?_isa} == %{version}-%{release}
%if %{with replace_hmaccalc}
Requires:       %{name}-hmaccalc%{?_isa} == %{version}-%{release}
%endif
%if %{with replace_coreutils}
Requires:       %{name}-checksum%{?_isa} == %{version}-%{release}
%endif
Requires:       coreutils
Requires:       openssl
Requires:       perl-interpreter

%description    tests
Auxiliary scripts for testing %{name}.
%endif


%prep
%autosetup -p 1 -S git

# Work around https://bugzilla.redhat.com/show_bug.cgi?id=2258240
sed -i -e 's|XML V45|XML V4.1.2|' -e 's|/xml/4\.5/|/xml/4.1.2/|' \
    lib/doc/libkcapi.tmpl

%if %{with_sysctl_tweak}
%{__cat} << EOF > README.%{distroname_ext}
This package increases the default limit of the ancillary buffer size
per kernel socket defined in \`net.core.optmem_max\` to %{sysctl_optmem_max} bytes.

For this preset to become active it requires a reboot after the
installation of this package.  You can also manually increase this
limit by invocing \`sysctl net.core.optmem_max=%{sysctl_optmem_max}\` as the
super-user, e.g. using \`su\` or \`sudo\` on the terminal.

This is done to provide consumers of the new Linux Kernel Crypto API
User Space Interface a well sufficient and reasonable maximum limit
by default, especially when using AIO with a larger amount of IOVECs.

For further information about the AF_ALG kernel socket and AIO, see
the discussion at the kernel-crypto mailing-list:
https://www.mail-archive.com/linux-crypto@vger.kernel.org/msg30417.html

See the instructions given in '%{_sysctldir}/50-default.conf',
if you need or want to override the preset made by this package.
EOF

%{__cat} << EOF > %{sysctl_prio}-%{name}-optmem_max.conf
# See the 'README.%{distroname_ext}' file shipped in %%doc
# with the %{name} package.
#
# See '%{_sysctldir}/50-default.conf',
# if you need or want to override this preset.

# Increase the ancillary buffer size per socket.
net.core.optmem_max = %{sysctl_optmem_max}
EOF
%endif

%{_bindir}/autoreconf -fiv


%build
%configure               \
  --libdir=%{_libdir}    \
  --disable-silent-rules \
  --enable-kcapi-encapp  \
  --enable-kcapi-dgstapp \
  --enable-kcapi-hasher  \
  --enable-kcapi-rngapp  \
  --enable-kcapi-speed   \
  --enable-kcapi-test    \
  --enable-shared        \
  --enable-static        \
  --enable-sum-prefix=   \
  --enable-sum-dir=%{_libdir} \
  --with-pkgconfigdir=%{_libdir}/pkgconfig
%if %{with doc}
%make_build all doc
%else
%make_build all man
%endif


%install
%make_install

# Install sysctl.d preset.
%{__mkdir_p} %{buildroot}%{_sysctldir}
%{__install} -Dpm 0644 -t %{buildroot}%{_sysctldir} \
  %{sysctl_prio}-%{name}-optmem_max.conf

# Install into proper location for inclusion by %%doc.
%{__mkdir_p} %{buildroot}%{_pkgdocdir}
%{__install} -Dpm 0644 -t %{buildroot}%{_pkgdocdir} \
%if %{with_sysctl_tweak}
  README.%{distroname_ext}                          \
%endif
%if %{with doc}
  doc/%{name}.p{df,s}                               \
%endif
  README.md CHANGES.md TODO

%if %{with doc}
%{__cp} -pr lib/doc/html %{buildroot}%{_pkgdocdir}
%endif

# Install replacement tools, if enabled.
%if %{with replace_coreutils}
for app in %apps_coreutils; do
  %{__ln_s} ../libexec/libkcapi/$app %{buildroot}%{_bindir}/$app
done
%endif

%if %{with replace_fipscheck}
for app in %apps_fipscheck; do
  %{__ln_s} ../libexec/libkcapi/$app %{buildroot}%{_bindir}/$app
done
%endif

%if %{with replace_hmaccalc}
for app in %apps_hmaccalc; do
  %{__ln_s} ../libexec/libkcapi/$app %{buildroot}%{_bindir}/$app
done
%endif

# We don't ship autocrap dumplings.
%{_bindir}/find %{buildroot} -type f -name '*.la' -print -delete

# HMAC checksums are generated during __spec_install_post.
%{_bindir}/find %{buildroot} -type f -name '*.hmac' -print -delete

# Remove 0-size files.
%{_bindir}/find %{buildroot} -type f -size 0 -print -delete

%if %{with doc}
# Make sure all docs have non-exec permissions, except for the dirs.
%{_bindir}/find %{buildroot}%{_pkgdocdir} -type f -print | \
  %{_bindir}/xargs %{__chmod} -c 0644
%{_bindir}/find %{buildroot}%{_pkgdocdir} -type d -print | \
  %{_bindir}/xargs %{__chmod} -c 0755
%endif

# Possibly save some space by hardlinking.
for d in %{_mandir} %{_pkgdocdir}; do
  %{_bindir}/hardlink -cfv %{buildroot}$d
done


%check
# Some basic sanity checks.
%if %{with clang_sa}
%make_build scan
%endif
%if %{with cppcheck}
# -UCHECK_DIR: string literal concatenation raises syntaxError
# with cppcheck-2.11 (https://trac.cppcheck.net/ticket/11830)
# --check-level=exhaustive: otherwise it emits warnings that get
# treated like errors
%make_build cppcheck CPPCHECK="cppcheck --check-level=exhaustive -UCHECK_DIR"
%endif

%if %{with test}
# On some arches `/proc/sys/net/core/optmem_max` is lower than 20480,
# which is the lowest limit needed to run the testsuite.  If that limit
# is not met, we do not run it.
%if %{test_optmem_max} >= 20480
# Skip the testsuite on old kernels.
%if %{lua:print(rpm.vercmp(posix.uname('%r'), '5.1'));} >= 0
# Real testsuite.
pushd test
%if %{with fuzz_test}
ENABLE_FUZZ_TEST=1 \
%endif
NO_32BIT_TEST=1    \
  ./test-invocation.sh
popd
%endif
%endif
%endif


%ldconfig_scriptlets


%files
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%license COPYING*
%{_libdir}/%{name}.so.%{vmajor}
%{_libdir}/%{name}.so.%{version}
%{_libdir}/hmaccalc/%{name}.so.%{vmajor}.hmac
%{_libdir}/hmaccalc/%{name}.so.%{version}.hmac
%if %{with_sysctl_tweak}
%doc %{_pkgdocdir}/README.%{distroname_ext}
%{_sysctldir}/%{sysctl_prio}-%{name}-optmem_max.conf
%endif


%files          devel
%doc %{_pkgdocdir}/CHANGES.md
%doc %{_pkgdocdir}/TODO
%{_includedir}/kcapi.h
%{_mandir}/man3/kcapi_*.3.*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc


%if %{with doc}
%files          doc
%doc %{_pkgdocdir}/html
%doc %{_pkgdocdir}/%{name}.pdf
%doc %{_pkgdocdir}/%{name}.ps
%endif


%files          hasher
%{_bindir}/kcapi-hasher
%{_libexecdir}/%{name}/md5sum
%{_libexecdir}/%{name}/sha*sum
%{_libexecdir}/%{name}/sm*sum
%{_libexecdir}/%{name}/fips*
%{_libexecdir}/%{name}/sha*hmac
%{_libexecdir}/%{name}/sm*hmac
%{_libdir}/hmaccalc/kcapi-hasher.hmac
%{_mandir}/man1/kcapi-hasher.1.*


%if %{with replace_coreutils}
%files          checksum
%{_bindir}/md5sum
%{_bindir}/sha*sum
%{_bindir}/sm*sum
%endif

%if %{with replace_fipscheck}
%files          fipscheck
%{_bindir}/fips*
%endif

%if %{with replace_hmaccalc}
%files          hmaccalc
%{_bindir}/sha*hmac
%{_bindir}/sm*hmac
%endif


%files          static
%{_libdir}/%{name}.a


%files          tools
%{_bindir}/kcapi
%{_bindir}/kcapi-convenience
%{_bindir}/kcapi-dgst
%{_bindir}/kcapi-enc
%{_bindir}/kcapi-enc-test-large
%{_bindir}/kcapi-rng
%{_bindir}/kcapi-speed
%{_mandir}/man1/kcapi-dgst.1.*
%{_mandir}/man1/kcapi-enc.1.*
%{_mandir}/man1/kcapi-rng.1.*


%if %{with test_package}
%files          tests
%{_libexecdir}/%{name}/kcapi
%{_libexecdir}/%{name}/kcapi-convenience
%{_libexecdir}/%{name}/kcapi-enc-test-large
%{_libexecdir}/%{name}/*.sh
%endif


%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 1.5.0-7
- Latest state for libkcapi

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 19 2024 Ondrej Mosnáček <omosnacek@gmail.com> - 1.5.0-4
- Do not ship duplicate kcapi-hasher in libkcapi-tools
- Ship kcapi-hasher manpage in libkcapi-hasher

* Tue Aug 06 2024 Simo Sorce <simo@redhat.com> - 1.5.0-3
- Use _libdir as recommended by guidelines

* Thu Aug 01 2024 Ondrej Mosnáček <omosnacek@gmail.com> - 1.5.0-1
- Update to version 1.5.0 (fedora#2257976)

* Wed Jul 31 2024 Ondrej Mosnáček <omosnacek@gmail.com> - 1.4.0-13
- Fix cppcheck failure (fedora#2300902)

* Wed Jul 31 2024 Ondrej Mosnáček <omosnacek@gmail.com> - 1.4.0-12
- Fix upstream URLs (fedora#2291348)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 30 2023 Zoltan Fridrich <zfridric@redhat.com> - 1.4.0-8
- Migrate to SPDX license

* Fri Jul 28 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4.0-7
- Fix build with cppcheck-2.11

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Aug 25 2022 Ondrej Mosnacek <omosnace@redhat.com> - 1.4.0-4
- Convert tests to TMT

* Thu Aug 25 2022 Ondrej Mosnacek <omosnace@redhat.com> - 1.4.0-3
- Add a patch to fix tests with kernels 6.0+

* Sat Aug 13 2022 Ondrej Mosnáček <omosnace@redhat.com> - 1.4.0-2
- Switch to rpmautospec

* Sat Aug 13 2022 Ondrej Mosnáček <omosnace@redhat.com> - 1.4.0-1
- Update to upstream version 1.4.0
- Re-enable cppcheck scanning on Fedora
- Resolves: rhbz#2056732

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Simo Sorce <simo@redhat.com> - 1.3.1-2
- Remove LTO build suppression by using better symver machinery

* Wed Jul 14 2021 Simo Sorce <simo@redhat.com> - 1.3.1-1
- Update to upstream version 1.3.1 which fixes ABI issues

* Mon Jul 12 2021 Simo Sorce <simo@redhat.com> - 1.3.0-1
- Update to upstream version 1.3.0

* Mon Mar 15 2021 Sahana Prasad <sahana@redhat.com> - 1.2.1-1
- Update to upstream version 1.2.1
- Remove patch fix MSG_MORE uasge as it is added upstream
- Remove cppcheck dependency for rhel bz#1931518
- Add a patch to fix fuzz tests

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 14 2020 Ondrej Mosnáček <omosnace@redhat.com> - 1.2.0-3
- Require perl-interpreter instead of full perl
- Backport fix for 5.9 kernels

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Sahana Prasad <omosnace@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0 tracked by BZ 1839592.
- Enable kcapi-enc tests as libkcapi BZ 1826022 is fixed.
- Remove 110-fipshmac-compat.patch as the changes are merged upstream.
- Remove 100-workaround-cppcheck-bug.patch as the changes are merged upstream.

* Tue May 05 2020 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.5-5
- Fix the CI test failures
- Enable building on old kernels
- Avoid conflicts between different versions of packages

* Thu Apr 23 2020 Tomáš Mráz <tmraz@redhat.com> - 1.1.5-4
- Add . prefix to files created by fipshmac if -d option is not specified

* Wed Apr 22 2020 Sahana Prasad <sahana@redhat.com> - 1.1.5-3
- Disables kcapi-enc tests until the kernel bug bz 1826022 is fixed.
- Produce also the fipscheck replacement package

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.5-1
- Update to upstream version 1.1.5

* Sat Jul 27 2019 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.4-6
- Backport patch to fix test failure on aarch64
- Remove no longer needed ppc64 workaround

* Sat Jul 27 2019 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.4-5
- Backport patch to fix tests

* Thu Jul 25 2019 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.4-4
- Work around cppcheck issue
- Enable gating

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon May 27 2019 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.4-2
- Fix FTBFS: hardlink is now in bindir

* Sat Feb 02 2019 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.4-1
- Update to upstream version 1.1.4

* Fri Feb 01 2019 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.3-3
- Fix build with new GCC

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 23 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.3-1
- Update to upstream version 1.1.3

* Thu Aug 09 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-16
- Add missing dependencies to the tests package
- Update patch from upstream

* Thu Aug 09 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-15
- Build and tests require perl

* Thu Aug 09 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-14
- Add missing script to the 'tests' package

* Wed Aug 08 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-13
- Add missing requires to the 'tests' subpackage

* Tue Aug 07 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-12
- Produce a subpackage with test scripts
- Build the 'tests' subpackage conditionally

* Wed Aug 01 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-11
- Add patch to fix unwanted closing of FD 0

* Tue Jul 31 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-10
- Remove the kernel headers workaround

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.1-9
- Rebuild for new binutils

* Fri Jul 27 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-8
- Add more Coverity fixes from upstream
- Add patch to fix AEAD fuzz test for BE arches
- Fixup specfile

* Mon Jul 23 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-7
- Add various fixes from upstream
- Drop the Requires on kernel package

* Mon Jul 16 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-6
- Put .hmac files into a separate directory

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-4
- Add patch to work around FTBFS on rawhide

* Wed Jul 11 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-3
- Fix off-by-one error in checkfile parsing

* Wed Jul 11 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-2
- Fix command-line parsing in libkcapi-hmaccalc

* Mon Jun 18 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.1-1
- Update to upstream version 1.1.1

* Wed May 09 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.0-5
- Skip CLang static analysis in RHEL
- Revert "Skip CLang static analysis in RHEL"
- Use own sha512hmac and fipscheck

* Wed May 02 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.0-4
- Fix description lines being too long

* Fri Apr 27 2018 Björn Esser <besser82@fedoraproject.org> - 1.1.0-3
- Fix conditional for hmaccalc replacement

* Mon Apr 16 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.0-2
- Enable hmaccalc replacements in Fedora 28+

* Thu Apr 12 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.1.0-1
- Update to upstream version 1.1.0

* Sat Mar 31 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-10
- Replace single patches with a monolitic one from upstream
- Obsolete replacements subpackage
- Ignore failing tests on %%{power64} temporarily

* Thu Mar 08 2018 Ondrej Mosnáček <omosnace@redhat.com> - 1.0.3-9
- Split up the replacements subpackage

* Mon Feb 26 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-8
- Increase optmem_max preset to 81920

* Mon Feb 26 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-7
- Obsoletes work by package name, not by provides (rhbz#1537225)

* Sun Feb 25 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-6
- Add patch to fix a copy-paste typo

* Sat Feb 17 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-5
- Add patch to fix build with -Werror

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Feb 04 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-3
- Switch to %%ldconfig_scriptlets

* Wed Jan 17 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-2
- Decrease optmem_max preset to 40960
- Let the build fail, if the minimum kernel version cannot be met
- Conditionalize the sysctl.d tweak on version of the kernel
- Conditionalize the name of README.distro on the distro

* Tue Jan 16 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-1
- Initial import (rhbz#1533929)

* Tue Jan 16 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.13
- Increase optmem_max preset to 81920

* Tue Jan 16 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.12
- Add sysctl.d preset and README.fedora

* Mon Jan 15 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.11
- Make the contents of the -replacements package configurable

* Mon Jan 15 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.10
- Fix Obsoletes of the -replacements package

* Sun Jan 14 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.9
- Disable the -replacements package until we have a plan for it

* Sun Jan 14 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.8
- Move the kcapi-hasher binary to -replacements package, since it is
  not of much use without the linked invocation names and saves the
  extra Requires on the -tools package

* Sun Jan 14 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.7
- Fix internal Requires of sub-packages
- Hardlink files in %%{_bindir}

* Sun Jan 14 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.6
- Add patches from upstream

* Sat Jan 13 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.5
- Add patches from upstream

* Sat Jan 13 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.4
- Asume the testsuite cannot be run, if the value of optmem_max cannot
  be obtained

* Sat Jan 13 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.3
- Move libraries to /%%{_lib} instead of %%{_libdir}, which is useful
  during boot when the library might be needed before a potentially
  seperate /usr partition is mounted

* Sat Jan 13 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.2
- Asume optmem_max is at least 20480, if the real value cannot be obtained

* Fri Jan 12 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.3-0.1
- New upstream release

* Wed Jan 10 2018 Björn Esser <besser82@fedoraproject.org> - 1.0.2-0.1
- Initial rpm release (rhbz#1533929)

## END: Generated by rpmautospec
