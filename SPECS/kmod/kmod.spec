# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Fedora does not support CONFIG_MODVERSIONS. Without kabi support
# weak-modules is useless at best, and can be actively harmful.
# Since RHEL *does* support this and offers kabi support,
# turn it on there by default.
%if 0%{?rhel}
%bcond_without weak_modules
%bcond_without dist_conf
%else
%bcond_with weak_modules
%bcond_with dist_conf
%endif

%bcond_without zlib
%bcond_without xz
%bcond_without zstd

Name:		kmod
Version:	34.2
Release:	2%{?dist}
Summary:	Linux kernel module management utilities

# https://docs.fedoraproject.org/en-US/legal/license-field/#_no_effective_license_analysis
# GPL-2.0-or-later:
#   build-aux/compile
#   build-aux/depcomp
#   build-aux/ltmain.sh
#   build-aux/ltmain.sh
#   build-aux/missing
#   build-aux/py-compile
#   build-aux/test-driver
#   m4/attributes.m4
#   m4/features.m4
#   tools
# GPL-3.0-or-later:
#   build-aux/config.guess
#   build-aux/config.sub
#   build-aux/git-version-gen
#   libkmod/docs/gtk-doc.make
#   m4/gtk-doc.m4
# FSFUL:
#   configure
# FSFULLRWD:
#   aclocal.m4
#   libkmod/docs/Makefile.in
#   m4/libtool.m4
#   m4/lt~obsolete.m4
#   m4/ltoptions.m4
#   m4/ltsugar.m4
#   m4/ltversion.m4
#   Makefile.in
# LGPL-2.1-only:
#   libkmod/python/kmod/error.py
#   libkmod/python/kmod/__init__.py
#   libkmod/python/kmod/version.py
#   libkmod/python/kmod/version.py.in
# LGPL-2.1-or-later:
#   config.h.in (no explicit license, the one in COPYING is assumed)
#   libkmod
#   man (no explicit license, the one in COPYING is assumed)
#   shared
#   shell-completion/bash/kmod
#   testsuite
# X11:
#   build-aux/install-sh
License:	GPL-2.0-or-later AND GPL-3.0-or-later AND FSFUL AND FSFULLRWD AND LGPL-2.1-only AND LGPL-2.1-or-later AND X11
URL:		https://git.kernel.org/pub/scm/utils/kernel/kmod/kmod.git
Source0:	https://www.kernel.org/pub/linux/utils/kernel/kmod/%{name}-%{version}.tar.xz
Source1:	weak-modules
Source2:	depmod.conf.dist
Exclusiveos:	Linux

BuildRequires:  gcc
BuildRequires:	chrpath
%if %{with zlib}
BuildRequires:	zlib-devel
%endif
%if %{with xz}
BuildRequires:	xz-devel
%endif
BuildRequires:  scdoc gtk-doc
BuildRequires:  openssl-devel
BuildRequires:  make automake libtool
%if %{with zstd}
BuildRequires:  libzstd-devel
%endif

Provides:	module-init-tools = 4.0-1
Obsoletes:	module-init-tools < 4.0-1
Provides:	/sbin/modprobe

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/modprobe
Provides:       /usr/sbin/modinfo
Provides:       /usr/sbin/insmod
Provides:       /usr/sbin/rmmod
Provides:       /usr/sbin/lsmod
Provides:       /usr/sbin/depmod
%endif

%description
The kmod package provides various programs needed for automatic
loading and unloading of modules under 2.6, 3.x, and later kernels, as well
as other module management programs. Device drivers and filesystems are two
examples of loaded and unloaded modules.

%package libs
Summary:	Libraries to handle kernel module loading and unloading

%description libs
The kmod-libs package provides runtime libraries for any application that
wishes to load or unload Linux kernel modules from the running system.

%package devel
Summary:	Header files for kmod development
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The kmod-devel package provides header files used for development of
applications that wish to load or unload Linux kernel modules.

%prep
%autosetup -p1

%build
autoreconf --install
%configure \
  --with-openssl \
%if %{with zlib}
  --with-zlib \
%endif
%if %{with xz}
  --with-xz \
%endif
%if %{with zstd}
  --with-zstd \
%endif
  --enable-debug

%{make_build} V=1

%install
%{make_install}

pushd $RPM_BUILD_ROOT%{_mandir}/man5
ln -s modprobe.d.5.gz modprobe.conf.5.gz
popd

find %{buildroot} -type f -name "*.la" -delete

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/modprobe.d

%if %{with weak_modules}
install -pm 755 %{SOURCE1} $RPM_BUILD_ROOT%{_sbindir}/weak-modules
%endif

%if %{with dist_conf}
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/depmod.d/dist.conf
%endif

%files
%dir %{_sysconfdir}/depmod.d
%dir %{_sysconfdir}/modprobe.d
%dir %{_prefix}/lib/modprobe.d
%{_bindir}/kmod
%{_sbindir}/modprobe
%{_sbindir}/modinfo
%{_sbindir}/insmod
%{_sbindir}/rmmod
%{_sbindir}/lsmod
%{_sbindir}/depmod
%if %{with weak_modules}
%{_sbindir}/weak-modules
%endif
%{_datadir}/bash-completion/
%{_datadir}/fish/vendor_functions.d/*
%{_datadir}/zsh/site-functions/*
%if %{with dist_conf}
%{_sysconfdir}/depmod.d/dist.conf
%endif
%{_datadir}/pkgconfig/kmod.pc
%attr(0644,root,root) %{_mandir}/man5/mod*.d*.5*
%attr(0644,root,root) %{_mandir}/man5/depmod.d.5*
%{_mandir}/man5/modprobe.conf.5*
%attr(0644,root,root) %{_mandir}/man8/*.8*
%doc NEWS README.md

%files libs
%license COPYING
%{_libdir}/libkmod.so.*

%files devel
%{_includedir}/libkmod.h
%{_libdir}/pkgconfig/libkmod.pc
%{_libdir}/libkmod.so

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 34.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Mar 31 2025 Josh Boyer <jwboyer@fedoraproject.org> - 34.2-1
- New upstream v34.2
- Resolves: rhbz#2355680

* Sat Mar 08 2025 Josh Boyer <jwboyer@fedoraproject.org> - 34.1-1
- New upstream v34.1
- Resolves: rhbz#2350269

* Mon Feb 24 2025 Josh Boyer <jwboyer@fedoraproject.org>
- New upstream v34
- Resolves: rhbz#2347049

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 33-2
- Rebuilt for the bin-sbin merge (2nd attempt)

* Thu Aug 15 2024 Eugene Syromiatnikov <esyr@redhat.com> - 33-1
- New upstream v33
- Resolves: rhbz#2268030

* Mon Aug 12 2024 Eugene Syromiatnikov <esyr@redhat.com> - 31-8
- weak-modules: use either zcat or xzcat based on symvers file extension

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr 11 2024 Zbigniew Jedrzejewski-Szmek <zbyszek@in.waw.pl> - 31-6
- Prepare for %%_bindir==%%_sbindir

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 31-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 01 2023 Eugene Syromiatnikov <esyr@redhat.com> - 31-3
- migrated to SPDX license

* Thu Nov 09 2023 Josh Boyer <jwboyer@fedoraproject.org> - 31-2
- Add upstream patches to enable SHA3 support
- New upstream v31
- Resolves: rhbz#2241394

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 09 2023 Eugene Syromiatnikov <esyr@redhat.com> - 30-5
- Add symvers.xz support to weak-modules

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 17 2022 Florian Weimer <fweimer@redhat.com> - 30-3
- Port configure script to C99

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 30-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul  4 2022 Yauheni Kaliuta <ykaliuta@redhat.com> - 30-1
- New upstream v30
- Resolves: rhbz#2102796

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 29-6
- Rebuilt with OpenSSL 3.0.0

* Tue Aug 10 2021 Yauheni Kaliuta <ykaliuta@redhat.com> - 29-5
- kmod.spec: enable debug
- weak-modules: compare_initramfs_modules: exit on pushd/popd failures
- weak-modules: split modules into array with read -a
- Add default config file, /etc/depmod.d/dist.conf

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Neal Gompa <ngompa13@gmail.com> - 29-3
- Fix conditional to only install weak-modules for RHEL

* Tue May 25 2021 Justin M. Forbes <jforbes@fedoraproject.org> - 29-2
- Rebuild for weak-modules drop in Fedora

* Mon May 24 2021 Justin M. Forbes <jforbes@fedoraproject.org>
- Remove weak-modules for Fedora as it causes problems.

* Fri May 14 2021 Josh Boyer <jwboyer@fedoraproject.org> - 29-1
- New upstream v29
- Resolves: rhbz#1962980

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 07 2021 Josh Boyer <jwboyer@fedoraproject.org> - 28-1
- New upstream v28
- Enable zstd support
- Resolves: rhbz#1913949

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Mar 25 2020 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 27-2
- add 0001-depmod-do-not-output-.bin-to-stdout.patch
  Resolves: rhbz#1808430

* Thu Feb 20 2020 Peter Robinson <pbrobinson@fedoraproject.org> - 27-1
- New upstream v27

* Mon Jan 20 2020 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 26-5
- weak-modules: sync with RHEL

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 26-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 25 2019 Yauheni Kaliuta <yauheni.kaliuta@redhat.com> - 26-3
- weak-modules: sync with RHEL

* Sun Feb 24 2019 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 26-2
- add PKCS7/openssl support (rhbz 1320921)

* Sun Feb 24 2019 Yauheni Kaliuta <ykaliuta@fedoraproject.org> - 26-1
- Update to version 26 (rhbz 1673749)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 25-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 29 2018 James Antill <james.antill@redhat.com> - 25-4
- Remove ldconfig scriptlet, now done via. transfiletrigger in glibc (rhbz 1644063)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Josh Boyer <jwboyer@fedoraproject.org> - 25-1
- Update to version 25 (rhbz 1532597)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 24 2017 Josh Boyer <jwboyer@fedoraproject.org> - 24-1
- Update to version 24 (rhbz 1426589)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jul 22 2016 Josh Boyer <jwboyer@fedoraproject.org> - 23-1
- Update to version 23

* Thu Feb 25 2016 Peter Robinson <pbrobinson@fedoraproject.org> 22-4
- Add powerpc patch to fix ToC on 4.5 ppc64le kernel

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 07 2016 Josh Boyer <jwboyer@fedoraproject.org> - 22-2
- Fix path to dracut in weak-modules (rhbz 1295038)

* Wed Nov 18 2015 Josh Boyer <jwboyer@fedoraproject.org> - 22-1
- Update to version 22

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 21-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 15 2015 Ville Skyttä <ville.skytta@iki.fi> - 21-2
- Own bash completion dirs not owned by anything in dep chain

* Tue Jun 09 2015 Josh Boyer <jwboyer@fedoraproject.org> - 21-1
- Update to verion 21

* Mon Mar 02 2015 Josh Boyer <jwboyer@fedoraproject.org> - 20.1
- Update to version 20

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 19-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Nov 16 2014 Josh Boyer <jwboyer@fedoraproject.org> - 19-1
- Update to version 19

* Wed Oct 29 2014 Josh Boyer <jwboyer@fedoraproject.org> - 18-4
- Backport patch to fix device node permissions (rhbz 1147248)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jul 12 2014 Tom Callaway <spot@fedoraproject.org> - 18-2
- fix license handling

* Tue Jun 24 2014 Josh Boyer <jwboyer@fedoraproject.org> - 18-1
- Update to version 18

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 09 2014 Josh Boyer <jwboyer@fedoraproject.org> - 17-1
- Update to version 17

* Thu Jan 02 2014 Václav Pavlín <vpavlin@redhat.com> - 16-1
- Update to version 16

* Thu Aug 22 2013 Josh Boyer <jwboyer@fedoraproject.org> - 15-1
- Update to version 15

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 05 2013 Josh Boyer <jwboyer@redhat.com> - 14-1
- Update to version 14

* Fri Apr 19 2013 Václav Pavlín <vpavlin@redhat.com> - 13-2
- Main package should require -libs

* Wed Apr 10 2013 Josh Boyer <jwboyer@redhat.com> - 13-1
- Update to version 13

* Wed Mar 20 2013 Weiping Pan <wpan@redhat.com> - 12-3
- Pull in weak-modules for kABI from Jon Masters <jcm@redhat.com> 

* Mon Mar 18 2013 Josh Boyer <jwboyer@redhat.com>
- Add patch to make rmmod understand built-in modules (rhbz 922187)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 06 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 12

* Thu Nov 08 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 11

* Fri Sep 07 2012 Josh Boyer <jwboyer@redaht.com>
- Update to version 10

* Mon Aug 27 2012 Josh Boyer <jwboyer@redhat.com>
- Update to version 9

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Josh Boyer <jwboyer@redhat.com> - 8-2
- Provide modprobe.conf(5) (rhbz 824552)

* Tue May 08 2012 Josh Boyer <jwboyer@redhat.com> - 8-1
- Update to version 8

* Mon Mar 19 2012 Kay Sievers <kay@redhat.com> - 7-1
- update to version 7
  - fix issue with --show-depends, where built-in
    modules of the running kernel fail to include
    loadable modules of the kernel specified

* Sun Mar 04 2012 Kay Sievers <kay@redhat.com> - 6-1
- update to version 6
- remove all patches, they are included in the release

* Fri Feb 24 2012 Kay Sievers <kay@redhat.com> - 5-8
- try to address brc#771285

* Sun Feb 12 2012 Kay Sievers <kay@redhat.com> - 5-7
- fix infinite loop with softdeps

* Thu Feb 09 2012 Harald Hoyer <harald@redhat.com> 5-6
- add upstream patch to fix "modprobe --ignore-install --show-depends"
  otherwise dracut misses a lot of modules, which are already loaded

* Wed Feb 08 2012 Harald Hoyer <harald@redhat.com> 5-5
- add "lsmod"

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-4
- remove temporarily added fake-provides

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-3
- temporarily add fake-provides to be able to bootstrap
  the new udev which pulls the old udev into the buildroot

* Tue Feb  7 2012 Kay Sievers <kay@redhat.com> - 5-1
- Update to version 5
- replace the module-init-tools package and provide all tools
  as compatibility symlinks

* Mon Jan 16 2012 Kay Sievers <kay@redhat.com> - 4-1
- Update to version 4
- set --with-rootprefix=
- enable zlib and xz support

* Thu Jan 05 2012 Jon Masters <jcm@jonmasters.org> - 3-1
- Update to latest upstream (adds new depmod replacement utility)
- For the moment, use the "kmod" utility to test the various functions

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-6
- Update kmod-2-with-rootlibdir patch with rebuild automake files

* Fri Dec 23 2011 Jon Masters <jcm@jonmasters.org> - 2-5
- Initial build for Fedora following package import

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-4
- There is no generic macro for non-multilib "/lib", hardcode like others

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-3
- Update package incorporating fixes from initial review feedback
- Cleaups to SPEC, rpath, documentation, library and binary locations

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-2
- Update package for posting to wider test audience (initial review submitted)

* Thu Dec 22 2011 Jon Masters <jcm@jonmasters.org> - 2-1
- Initial Fedora package for module-init-tools replacement (kmod) library
