# Shared object version of libkcapi.
%global vmajor            1
%global vminor            3
%global vpatch            1
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
# Lowest limit to run the testsuite.  If we cannot obtain this
# value, we asume the testsuite cannot be run.
%global test_optmem_max   %(cat /proc/sys/net/core/optmem_max || echo 0)
# For picking patches from upstream commits or pull requests.
%global giturl            https://github.com/smuellerDD/%{name}
%global apps_hmaccalc sha1hmac sha224hmac sha256hmac sha384hmac sha512hmac
%global apps_fipscheck sha1sum sha224sum sha256sum sha384sum sha512sum md5sum fipscheck fipshmac
# Use OpenSSL to perform hmac calculations
%global sha512hmac bash %{_sourcedir}/sha512hmac-openssl.sh
%global fipshmac   bash %{_sourcedir}/fipshmac-openssl.sh
# Add generation of HMAC checksums of the final stripped
# binaries.  %%define with lazy globbing is used here
# intentionally, because using %%global does not work.
%define __spec_install_post                                      \
%{?__debug_package:%{__debug_install_post}}                      \
%{__arch_install_post}                                           \
%__os_install_post                                             \
bin_path=%{buildroot}%{_bindir}                                  \
lib_path=%{buildroot}/%{_lib}                                    \
for app in %{apps_hmaccalc}; do                                  \
  test -e "$bin_path"/$app || continue                           \
  { %{sha512hmac} "$bin_path"/$app || exit 1; }                    \\\
    | cut -f 1 -d ' ' >"$lib_path"/hmaccalc/$app.hmac            \
done                                                             \
for app in %{apps_fipscheck}; do                                 \
  test -e "$bin_path"/$app || continue                           \
  %{fipshmac} -d "$lib_path"/fipscheck "$bin_path"/$app || exit 1  \
done                                                             \
%{fipshmac} -d "$lib_path"/fipscheck                               \\\
  "$lib_path"/libkcapi.so.%{version} || exit 1                   \
ln -s libkcapi.so.%{version}.hmac                            \\\
  "$lib_path"/fipscheck/libkcapi.so.%{vmajor}.hmac               \
%{nil}
%global fipscheck_next_evr     1.5.0-10%{?dist}
%global hmaccalc_next_evr      0.9.14-11%{?dist}
%if %{with_sysctl_tweak}
# Priority for the sysctl.d preset.
%global sysctl_prio       50
# Value used for the sysctl.d preset.
%global sysctl_optmem_max 81920
# Extension for the README.distro file.
%global distroname_ext    %{?fedora:fedora}%{?rhel:redhat}
%endif
Summary:        User space interface to the Linux Kernel Crypto API
Name:           libkcapi
Version:        %{vmajor}.%{vminor}.%{vpatch}
Release:        3%{?dist}
License:        BSD OR GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.chronox.de/%{name}.html
Source0:        https://www.chronox.de/%{name}/%{name}-%{version}.tar.xz
Source1:        sha512hmac-openssl.sh
Source2:        fipshmac-openssl.sh
BuildRequires:  bash
BuildRequires:  clang
BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  kernel-headers
BuildRequires:  libtool
BuildRequires:  openssl
BuildRequires:  perl
BuildRequires:  systemd
BuildRequires:  xmlto
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
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
Header files for applications that use %{name}.

%package        fipscheck
Summary:        Drop-in replacements for fipscheck/fipshmac provided by the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      fipscheck < %{fipscheck_next_evr}
Provides:       fipscheck = %{fipscheck_next_evr}
Provides:       fipscheck%{?_isa} = %{fipscheck_next_evr}

%description    fipscheck
Provides drop-in replacements for fipscheck and fipshmac tools (from
package fipscheck) using %{name}.

%package        hmaccalc
Summary:        Drop-in replacements for hmaccalc provided by the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      hmaccalc < %{hmaccalc_next_evr}
Provides:       hmaccalc = %{hmaccalc_next_evr}
Provides:       hmaccalc%{?_isa} = %{hmaccalc_next_evr}

%description    hmaccalc
Provides drop-in replacements for sha*hmac tools (from package
hmaccalc) using %{name}.

%package        static
Summary:        Static library for -static linking with %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}

%description    static
This package contains the %{name} static libraries for -static
linking.  You don't need this, unless you link statically, which
is highly discouraged.

%package        tools
Summary:        Utility applications for the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Utility applications that are provided with %{name}.  This includes
tools to use message digests, symmetric ciphers and random number
generators implemented in the Linux kernel from command line.

%package        tests
Summary:        Testing scripts for the %{name} package
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-hmaccalc%{?_isa} = %{version}-%{release}
Requires:       %{name}-tools%{?_isa} = %{version}-%{release}
Requires:       coreutils
Requires:       openssl
Requires:       perl

%description    tests
Auxiliary scripts for testing %{name}.

%prep
%autosetup -p 1 -S git

%if %{with_sysctl_tweak}

cat << EOF > %{sysctl_prio}-%{name}-optmem_max.conf
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
  --libdir=/%{_lib}      \
  --disable-silent-rules \
  --disable-kcapi-encapp \
  --enable-kcapi-dgstapp \
  --enable-kcapi-hasher  \
  --enable-kcapi-rngapp  \
  --enable-kcapi-speed   \
  --enable-kcapi-test    \
  --enable-shared        \
  --enable-static        \
  --enable-sum-prefix=   \
  --enable-sum-dir=/%{_lib} \
  --with-pkgconfigdir=%{_libdir}/pkgconfig


%install
%make_install

# Install sysctl.d preset.
mkdir -p %{buildroot}%{_sysctldir}
install -Dpm 0644 -t %{buildroot}%{_sysctldir} \
  %{sysctl_prio}-%{name}-optmem_max.conf


rm -f                            \
  %{buildroot}%{_bindir}/md5sum       \
  %{buildroot}%{_bindir}/sha*sum

# We don't ship autocrap dumplings.
find %{buildroot} -type f -name "*.la" -delete -print

# HMAC checksums are generated during __spec_install_post.
%{_bindir}/find %{buildroot} -type f -name '*.hmac' -print -delete

# Remove 0-size files.
%{_bindir}/find %{buildroot} -type f -size 0 -print -delete


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING*
/%{_lib}/%{name}.so.%{vmajor}
/%{_lib}/%{name}.so.%{version}
/%{_lib}/fipscheck/%{name}.so.%{vmajor}.hmac
/%{_lib}/fipscheck/%{name}.so.%{version}.hmac
%if %{with_sysctl_tweak}
%{_sysctldir}/%{sysctl_prio}-%{name}-optmem_max.conf
%endif

%files devel
%{_includedir}/kcapi.h
%{_mandir}/man3/kcapi_*.3.*
/%{_lib}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

%files hmaccalc
%{_bindir}/sha*hmac
/%{_lib}/hmaccalc/sha*hmac.hmac

%files fipscheck
%{_bindir}/fips*
/%{_lib}/fipscheck/fips*.hmac

%files hmaccalc
%{_bindir}/sha*hmac
/%{_lib}/hmaccalc/sha*hmac.hmac

%files static
/%{_lib}/%{name}.a

%files tools
%{_bindir}/kcapi*
%{_mandir}/man1/kcapi*.1.*

%files tests
%{_libexecdir}/%{name}/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.3.1-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jan 19 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.3.1-2
- Fixing 'Obsoletes' and 'Provides' for 'fipscheck' and 'hmaccalc' subpackages.

* Mon Jan 10 2022 Henry Li <lihl@microsoft.com> - 1.3.1-1
- Upgrade to version 1.3.1

* Fri Feb 05 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.2.0-5
- Use OpenSSL to perform hmac calculations

* Tue Jan 19 2021 Nicolas Ontiveros <niontive@microsoft.com> - 1.2.0-4
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Disable %%check section for now.

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
