%global security_hardening nonow
%define glibc_target_cpu %{_build}

# Don't depend on bash by default
%define __requires_exclude ^/(bin|usr/bin).*$

Summary:        Main C library
Name:           glibc
Version:        2.35
Release:        7%{?dist}
License:        BSD AND GPLv2+ AND Inner-Net AND ISC AND LGPLv2+ AND MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.gnu.org/software/libc
Source0:        https://ftp.gnu.org/gnu/glibc/%{name}-%{version}.tar.xz
Source1:        locale-gen.sh
Source2:        locale-gen.conf
Patch0:         https://www.linuxfromscratch.org/patches/downloads/glibc/glibc-2.35-fhs-1.patch
# Only applicable on ARMv7 targets.
Patch1:         CVE-2020-6096.nopatch
# Only applicable on x32 targets.
Patch2:         CVE-2019-6488.nopatch
# Only applicable on PowerPC targets.
Patch3:         CVE-2020-1751.nopatch
# Marked by upstream/Ubuntu/Red Hat as not a security bug, no fix available
# Rationale: Exploit requires crafted pattern in regex compiler meant only for trusted content
Patch4:         CVE-2018-20796.nopatch
Patch5:         glibc-2.34_pthread_cond_wait.patch
Patch6:         CVE-2023-4911.patch
Patch7:         CVE-2023-4806.patch
Patch8:         CVE-2023-5156.patch
BuildRequires:  bison
BuildRequires:  gawk
BuildRequires:  gettext
BuildRequires:  kernel-headers
BuildRequires:  texinfo
Requires:       filesystem
Provides:       %{name}-common = %{version}-%{release}
Provides:       /sbin/ldconfig
Provides:       nss_db = %{version}-%{release}
Provides:       rtld(GNU_HASH)
ExcludeArch:    armv7 ppc i386 i686

%description
This library provides the basic routines for allocating memory,
searching directories, opening and closing files, reading and
writing files, string handling, pattern matching, arithmetic,
and so on.

%package devel
Summary:        Header files for glibc
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-headers = %{version}-%{release}

%description devel
These are the header files of glibc.

%package static
Summary:        Static glibc library and runtimes
Group:          Applications/System
Requires:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-static%{?_isa} = %{version}-%{release}

%description static
These are the static artefacts for glibc.

%package lang
Summary:        Additional language files for glibc
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description lang
These are the additional language files of glibc.

%package i18n
Summary:        Additional internationalization files for glibc
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Provides:       %{name}-locale-source = %{version}-%{release}

%description i18n
These are the additional internationalization files of glibc.

%package iconv
Summary:        gconv modules for glibc
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description iconv
These are gconv modules for iconv().

%package tools
Summary:        tools for glibc
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description tools
Extra tools for glibc.

%package nscd
Summary:        Name Service Cache Daemon
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description nscd
Name Service Cache Daemon

%prep
%autosetup -p1
sed -i 's/\\$$(pwd)/`pwd`/' timezone/Makefile
install -vdm 755 %{_builddir}/%{name}-build
# do not try to explicitly provide GLIBC_PRIVATE versioned libraries
%define __find_provides %{_builddir}/%{name}-%{version}/find_provides.sh
%define __find_requires %{_builddir}/%{name}-%{version}/find_requires.sh

# create find-provides and find-requires script in order to ignore GLIBC_PRIVATE errors
cat > find_provides.sh << _EOF
#! /bin/sh
if [ -d /tools ]; then
/tools/lib/rpm/find-provides | grep -v GLIBC_PRIVATE
else
%{_libdir}/rpm/find-provides | grep -v GLIBC_PRIVATE
fi
exit 0
_EOF
chmod +x find_provides.sh

cat > find_requires.sh << _EOF
#! /bin/sh
if [ -d /tools ]; then
/tools/lib/rpm/find-requires %{buildroot} %{glibc_target_cpu} | grep -v GLIBC_PRIVATE
else
%{_libdir}/rpm/find-requires %{buildroot} %{glibc_target_cpu} | grep -v GLIBC_PRIVATE
fi
_EOF
chmod +x find_requires.sh
#___EOF

%build
CFLAGS="`echo " %{build_cflags} " | sed 's/-Wp,-D_FORTIFY_SOURCE=2//'`"
CXXFLAGS="`echo " %{build_cxxflags} " | sed 's/-Wp,-D_FORTIFY_SOURCE=2//'`"
export CFLAGS
export CXXFLAGS

cd %{_builddir}/%{name}-build
../%{name}-%{version}/configure \
        --prefix=%{_prefix} \
        --disable-profile \
        --disable-werror \
        --enable-kernel=3.2 \
        --enable-bind-now \
        --enable-static-pie \
        --disable-experimental-malloc \
%ifarch x86_64
        --enable-cet \
%endif
        --disable-silent-rules

make %{?_smp_mflags}

%install
#       Do not remove static libs
pushd %{_builddir}/glibc-build
#       Create directories
make install_root=%{buildroot} install
install -vdm 755 %{buildroot}%{_sysconfdir}/ld.so.conf.d
install -vdm 755 %{buildroot}%{_var}/cache/nscd
install -vdm 755 %{buildroot}%{_libdir}/locale
cp -v ../%{name}-%{version}/nscd/nscd.conf %{buildroot}%{_sysconfdir}/nscd.conf
#       Install locale generation script and config file
cp -v %{SOURCE2} %{buildroot}%{_sysconfdir}
cp -v %{SOURCE1} %{buildroot}/sbin
#       Remove unwanted cruft
rm -rf %{buildroot}%{_infodir}
#       Install configuration files

# Spaces should not be used in nsswitch.conf in the begining of new line
# Only tab should be used as it expects the same in source code.
# Otherwise "altfiles" will not be added. which may cause dbus.service failure
cat > %{buildroot}%{_sysconfdir}/nsswitch.conf <<- "EOF"
#       Begin /etc/nsswitch.conf

	passwd: files
	group: files
	shadow: files

	hosts: files dns
	networks: files

	protocols: files
	services: files
	ethers: files
	rpc: files
#       End /etc/nsswitch.conf
EOF
cat > %{buildroot}%{_sysconfdir}/ld.so.conf <<- "EOF"
#       Begin /etc/ld.so.conf
	%{_prefix}/local/lib
	/opt/lib
	include %{_sysconfdir}/ld.so.conf.d/*.conf
EOF
popd
%find_lang %{name} --all-name
pushd localedata
# Generate out of locale-archive an (en_US.) UTF-8 locale
mkdir -p %{buildroot}%{_libdir}/locale
I18NPATH=. GCONV_PATH=../../glibc-build/iconvdata LC_ALL=C ../../glibc-build/locale/localedef --no-archive --prefix=%{buildroot} -A ../intl/locale.alias -i locales/en_US -c -f charmaps/UTF-8 en_US.UTF-8
mv %{buildroot}%{_libdir}/locale/en_US.utf8 %{buildroot}%{_libdir}/locale/en_US.UTF-8
popd
# to do not depend on /bin/bash
sed -i 's@#! /bin/bash@#! /bin/sh@' %{buildroot}%{_bindir}/ldd
sed -i 's@#!/bin/bash@#!/bin/sh@' %{buildroot}%{_bindir}/tzselect

# Determine which static libs are needed in `glibc-devel` - the rest will be put
# into `glibc-static`.  We need to keep the static shims for function that's now
# in `libc.so` (since 2.34 - see https://developers.redhat.com/articles/2021/12/17/why-glibc-234-removed-libpthread)
# and the "statically linked bit" of `libc.so` (called `libc_nonshared.a`)
static_libs_in_devel_pattern="lib\(c_nonshared\|pthread\|dl\|rt\|g\|util\|mcheck\).a"
ls -1 %{buildroot}%{_lib64dir}/*.a | grep -e "$static_libs_in_devel_pattern" | sed "s:^%{buildroot}::g" > devel.filelist
ls -1 %{buildroot}%{_lib64dir}/*.a | grep -v -e "$static_libs_in_devel_pattern" | sed "s:^%{buildroot}::g" > static.filelist

%check
cd %{_builddir}/glibc-build
make %{?_smp_mflags} check ||:
# These 2 persistant false positives are OK
# XPASS for: elf/tst-protected1a and elf/tst-protected1b
[ `grep ^XPASS tests.sum | wc -l` -ne 2 -a `grep "^XPASS: elf/tst-protected1[ab]" tests.sum | wc -l` -ne 2 ] && exit 1 ||:

# FAIL (intermittent) in chroot but PASS in container:
# posix/tst-spawn3 and stdio-common/test-vfprintf
n=0
grep "^FAIL: posix/tst-spawn3" tests.sum >/dev/null && n=$((n+1)) ||:
grep "^FAIL: stdio-common/test-vfprintf" tests.sum >/dev/null && n=$((n+1)) ||:
# FAIL always on overlayfs/aufs (in container)
grep "^FAIL: posix/tst-dir" tests.sum >/dev/null && n=$((n+1)) ||:

#https://sourceware.org/glibc/wiki/Testing/Testsuite
grep "^FAIL: nptl/tst-eintr1" tests.sum >/dev/null && n=$((n+1)) ||:
#This happens because the kernel fails to reap exiting threads fast enough,
#eventually resulting an EAGAIN when pthread_create is called within the test.

# check for exact 'n' failures
[ `grep ^FAIL tests.sum | wc -l` -ne $n ] && exit 1 ||:

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING COPYING.LIB LICENSES
%{_libdir}/locale/*
%dir %{_sysconfdir}/ld.so.conf.d
%config(noreplace) %{_sysconfdir}/nsswitch.conf
%config(noreplace) %{_sysconfdir}/ld.so.conf
%config(noreplace) %{_sysconfdir}/rpc
%config(missingok,noreplace) %{_sysconfdir}/ld.so.cache
%config %{_sysconfdir}/locale-gen.conf
/lib64/*
%ifarch aarch64
/lib/ld-linux-aarch64.so.1
%endif
%exclude /lib64/libpcprofile.so
%{_lib64dir}/*.so
/sbin/ldconfig
/sbin/locale-gen.sh
#%%{_sbindir}/zdump
%{_sbindir}/zic
%{_sbindir}/iconvconfig
%{_bindir}/*
%{_libexecdir}/*
%{_datadir}/i18n/charmaps/UTF-8.gz
%{_datadir}/i18n/charmaps/ISO-8859-1.gz
%{_datadir}/i18n/locales/en_US
%{_datarootdir}/locale/locale.alias
%exclude %{_localstatedir}/lib/nss_db/Makefile
%exclude %{_bindir}/mtrace
%exclude %{_bindir}/pcprofiledump
%exclude %{_bindir}/xtrace

%files iconv
%defattr(-,root,root)
%{_lib64dir}/gconv/*

%files tools
%defattr(-,root,root)
%{_bindir}/mtrace
%{_bindir}/pcprofiledump
%{_bindir}/xtrace
/sbin/sln
%{_lib64dir}/audit/*
/lib64/libpcprofile.so

%files nscd
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/nscd.conf
%{_sbindir}/nscd
%dir %{_localstatedir}/cache/nscd

%files i18n
%defattr(-,root,root)
%{_datadir}/i18n/charmaps/*.gz
%{_datadir}/i18n/locales/*

%files devel -f devel.filelist
%defattr(-,root,root)
# TODO: Excluding for now to remove dependency on PERL
# /usr/bin/mtrace
# C Runtime files for `-pie`, `-no-pie` and profiled executables as well as for shared libs
%{_lib64dir}/{,g,M,S}crt1.o
# C Runtime files needed for all targets
%{_lib64dir}/crt{i,n}.o
%{_includedir}/*

%files static -f static.filelist
%defattr(-,root,root)
# C Runtime files for `-static-pie` and profiled `-static-pie`
%{_lib64dir}/{r,gr}crt1.o

%files -f %{name}.lang lang
%defattr(-,root,root)

%changelog
* Mon May 06 2024 Rachel Menge <rachelmenge@microsoft.com> - 2.35-7
- Fixup CVE-2023-4806 patch

* Wed Oct 04 2023 Minghe Ren <mingheren@microsoft.com> - 2.35-6
- Add patches for CVE-2023-4806 and CVE-2023-5156

* Tue Oct 03 2023 Mandeep Plaha <mandeepplaha@microsoft.com> - 2.35-5
- Patch CVE-2023-4911

* Fri Jun 30 2023 Andrew Phelps <anphel@microsoft.com> - 2.35-4
- Restore glibc-debuginfo package

* Fri Sep 30 2022 Andy Caldwell <andycaldwell@microsoft> - 2.35-3
- Split `glibc-static` into an actual package containing static libraries and runtime

* Mon May 02 2022 Sriram Nambakam <snambakam@microsoft.com> - 2.35-2
- To remove leading spaces in /etc/nsswitch.conf, use tabs instead of spaces

* Tue Apr 12 2022 Andrew Phelps <anphel@microsoft.com> - 2.35-1
- Upgrade to version 2.35
- Cleanup old patch files

* Wed Mar 02 2022 Andy Caldwell <andycaldwell@microsoft.com> - 2.34-3
- Add support for building `-static-pie` binaries against `glibc`
- Add additional BuildRequires

* Thu Nov 04 2021 Pawel Winogrodzki <pawel.winogrodzki@microsoft.com> - 2.34-2
- Adding missing BR on "perl(File::Find)".
- Fixing licensing information.
- Removing redundant 'Provides'.

* Thu Oct 14 2021 Andrew Phelps <anphel@microsoft.com> - 2.34-1
- Upgrade to version 2.34
- License verified

* Fri Sep 24 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.28-19
- Adding 'Provides' for 'nss_db'.

* Thu Jul 29 2021 Jon Slobodzian <joslobo@microsoft.com> 2.28-18
- Dash Rolled for Merge from 1.0 branch

* Fri Apr 02 2021 Thomas Crain <thcrain@microsoft.com> - 2.28-17
- Merge the following releases from 1.0 to dev branch
- lihl@microsoft.com, 2.28-13: Added patch to resolve CVE-2019-7309, Used autosteup
- thcrain@microsoft.com, 2.28-14: Patch CVE-2019-19126
- mamalisz@microsoft.com, 2.28-15: Exclude binaries(such as bash) from requires list.
- nicolasg@microsoft.com, 2.28-16: Patch CVE-2019-25013
- thcrain@microsoft.com, 2.28-17: Patch CVE-2021-3326
- nisamson@microsoft.com, 2.28-18: Patch CVE-2021-27618

* Thu Mar 25 2021 Henry Li <lihl@microsoft.com> - 2.28-16
- Provides glibc-locale-source from glibc-i18n
- Add back exluded files to glibc-i18n

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.28-15
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Thu Dec 10 2020 Joe Schmitt <joschmit@microsoft.com> - 2.28-14
- Provide isa version of glibc-static.

* Mon Sep 28 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.28-13
- Move some tools from glibc-tools and glibc-iconv to glibc and provide glibc-common
- Provide glibc-static and glibc-headers under glibc-devel

* Wed Jul 29 2020 Thomas Crain <thcrain@microsoft.com> - 2.28-12
- Ignore CVE-2018-20796, as it is not a security issue

* Wed Jul 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.28-11
- Disable the debuginfo package for glibc, and use unstripped binaries instead.

* Fri Jun 26 2020 Ruying Chen <v-ruyche@microsoft.com> - 2.28-10
- Added provides for binary capability.

* Thu Jun 11 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.28-9
- Disable -Wp,-D_FORTIFY_SOURCE=2 to build with hardened cflags.

* Tue May 19 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.28-8
- Ignore CVE-2019-6488, CVE-2020-1751, CVE-2020-6096 as they don't apply to aarch64 or x86_64.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.28-7
- Added %%license line automatically

* Fri Mar 20 2020 Andrew Phelps <anphel@microsoft.com> - 2.28-6
- Configure with --disable-werror.

* Mon Dec 02 2019 Saravanan Somasundaram <sarsoma@microsoft.com> - 2.28-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Jul 12 2019 Ankit Jain <ankitja@vmware.com> - 2.28-4
- Replaced spaces with tab in nsswitch.conf file

* Fri Mar 08 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.28-3
- Fix CVE-2019-9169

* Tue Jan 22 2019 Anish Swaminathan <anishs@vmware.com> - 2.28-2
- Fix CVE-2018-19591

* Tue Aug 28 2018 Alexey Makhalov <amakhalov@vmware.com> - 2.28-1
- Version update. Disable obsolete rpc (use libtirpc) and nsl.

* Tue Jan 23 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.26-10
- Fix CVE-2018-1000001 and CVE-2018-6485

* Mon Jan 08 2018 Xiaolin Li <xiaolinl@vmware.com> - 2.26-9
- Fix CVE-2017-16997

* Thu Dec 21 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.26-8
- Fix CVE-2017-17426

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.26-7
- Aarch64 support

* Wed Oct 25 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.26-6
- Fix CVE-2017-15670 and CVE-2017-15804

* Tue Oct 10 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.26-5
- Compile out tcache.

* Fri Sep 15 2017 Bo Gan <ganb@vmware.com> - 2.26-4
- exclude tst-eintr1 per official wiki recommendation.

* Tue Sep 12 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.26-3
- Fix makecheck for run in docker.

* Tue Aug 29 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.26-2
- Fix tunables setter.
- Add malloc arena fix.
- Fix makecheck.

* Tue Aug 15 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.26-1
- Version update

* Tue Aug 08 2017 Anish Swaminathan <anishs@vmware.com> - 2.25-4
- Apply fix for CVE-2017-1000366

* Thu May 4  2017 Bo Gan <ganb@vmware.com> - 2.25-3
- Remove bash dependency in post/postun script

* Fri Apr 21 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.25-2
- Added -iconv -tools and -nscd subpackages

* Wed Mar 22 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.25-1
- Version update

* Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.24-1
- Version update

* Wed Nov 23 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.22-13
- Install en_US.UTF-8 locale by default

* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.22-12
- Added i18n subpackage

* Tue Oct 25 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.22-11
- Workaround for build failure with "out of memory" message

* Wed Sep 28 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.22-10
- Added pthread_create-fix-use-after-free.patch

* Tue Jun 14 2016 Divya Thaluru <dthaluru@vmware.com> - 2.22-9
- Enabling rpm debug package and stripping the libraries

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.22-8
- GA - Bump release of all rpms

* Mon May 23 2016 Divya Thaluru <dthaluru@vmware.com> - 2.22-7
- Added patch for CVE-2014-9761

* Mon Mar 21 2016 Alexey Makhalov <amakhalov@vmware.com> - 2.22-6
- Security hardening: nonow

* Fri Mar 18 2016 Anish Swaminathan <anishs@vmware.com> - 2.22-5
- Change conf file qualifiers

* Fri Mar 11 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.22-4
- Added patch for res_qeury assertion with bad dns config
- Details: https://sourceware.org/bugzilla/show_bug.cgi?id=19791

* Tue Feb 16 2016 Anish Swaminathan <anishs@vmware.com> - 2.22-3
- Added patch for CVE-2015-7547

* Mon Feb 08 2016 Anish Swaminathan <anishs@vmware.com> - 2.22-2
- Added patch for bindresvport blacklist

* Tue Jan 12 2016 Xiaolin Li <xiaolinl@vmware.com> - 2.22-1
- Updated to version 2.22

* Tue Dec 1 2015 Divya Thaluru <dthaluru@vmware.com> - 2.19-8
- Disabling rpm debug package and stripping the libraries

* Wed Nov 18 2015 Divya Thaluru <dthaluru@vmware.com> - 2.19-7
- Adding patch to close nss files database

* Tue Nov 10 2015 Xiaolin Li <xiaolinl@vmware.com> - 2.19-6
- Handled locale files with macro find_lang

* Wed Aug 05 2015 Kumar Kaushik <kaushikk@vmware.com> - 2.19-5
- Adding postun section for ldconfig.

* Tue Jul 28 2015 Alexey Makhalov <amakhalov@vmware.com> - 2.19-4
- Support glibc building against current rpm version.

* Thu Jul 23 2015 Divya Thaluru <dthaluru@vmware.com> - 2.19-3
- Packing locale-gen scripts

* Mon May 18 2015 Touseef Liaqat <tliaqat@vmware.com> - 2.19-2
- Update according to UsrMove.

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 2.19-1
- Initial build. First version
