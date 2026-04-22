# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond nis %[!(0%{?rhel} >= 9)]

%global so_ver 0
%global pam_redhat_version 1.3.0

# docs require fop, which is Java-based and not included in RHEL
# PDF docs are not identical between builds, -doc needs to be archful if enabled
%ifarch %{java_arches}
%global build_pdf %[0 && %{undefined rhel}]
%else
%global build_pdf 0
%endif

Summary: An extensible library which provides authentication for applications
Name: pam
Version: 1.7.1
Release: 5%{?dist}
# The library is BSD licensed with option to relicense as GPLv2+
# - this option is redundant as the BSD license allows that anyway.
# pam_timestamp and pam_loginuid modules are GPLv2+.
License: BSD-3-Clause AND GPL-2.0-or-later
URL: http://www.linux-pam.org/
Source0: https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz
Source1: https://github.com/linux-pam/linux-pam/releases/download/v%{version}/Linux-PAM-%{version}.tar.xz.asc
Source2: https://releases.pagure.org/pam-redhat/pam-redhat-%{pam_redhat_version}.tar.xz
Source3: macros.%{name}
Source5: other.pamd
Source10: config-util.pamd
Source11: dlopen.sh
Source12: system-auth.5
Source13: config-util.5
Source15: pamtmp.conf
Source17: postlogin.5
Source18: https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt
Patch1:  pam-1.7.0-redhat-modules.patch
Patch2:  pam-1.5.3-unix-nomsg.patch
Patch3:  pam-1.7.1-pam-unix-remove-obsolete-defines.patch

%{load:%{SOURCE3}}

### Dependencies ###
Requires(meta): authselect >= 1.3
Requires: gdbm
Requires: libpwquality%{?_isa}
Requires: pam-libs%{?_isa} = %{version}-%{release}
Requires: setup

Suggests: libdb-convert-util

### Build Dependencies ###
BuildRequires: audit-libs-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: bison
BuildRequires: flex
BuildRequires: gcc
BuildRequires: gdbm-devel
BuildRequires: gettext-devel
BuildRequires: libeconf-devel
%if %{with nis}
BuildRequires: libnsl2-devel
%endif
BuildRequires: libselinux-devel
BuildRequires: libtirpc-devel
BuildRequires: libtool
BuildRequires: libxcrypt-devel
BuildRequires: make
BuildRequires: meson
BuildRequires: openssl-devel
BuildRequires: perl-interpreter
BuildRequires: pkgconfig
BuildRequires: sed
BuildRequires: systemd

%description
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication.

%package devel
Summary: Files needed for developing PAM-aware applications and modules for PAM
Requires: pam-libs%{?_isa} = %{version}-%{release}

%description devel
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. This package
contains header files used for building both PAM-aware applications
and modules for use with the PAM system.

%package doc
Summary: Extra documentation for PAM.
Requires: pam = %{version}-%{release}
Obsoletes: pam-docs < 1.5.2-6
Provides: pam-docs = %{version}-%{release}
BuildArch: noarch
BuildRequires: docbook5-schemas
BuildRequires: docbook5-style-xsl
BuildRequires: elinks
%if %{build_pdf}
BuildRequires: fop
%endif
BuildRequires: libxslt
BuildRequires: linuxdoc-tools

%description doc
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. The pam-doc
contains extra documentation for PAM. Currently, this includes additional
documentation in txt and html format.

%package libs
Summary: Shared libraries of the PAM package
# Make sure that if we don't try to upgrade -libs but not the
# main pam package and get file conflicts:
Conflicts: pam < 1.5.2-11

%description libs
PAM (Pluggable Authentication Modules) is a system security tool that
allows system administrators to set authentication policy without
having to recompile programs that handle authentication. The pam-libs
contains the shared libraries for PAM.

%prep
%setup -q -n Linux-PAM-%{version} -a 2

# Add custom modules.
mv pam-redhat-%{pam_redhat_version}/* modules

cp %{SOURCE18} .

%patch -P 1 -p1 -b .redhat-modules
%patch -P 2 -p1 -b .nomsg
%patch -P 3 -p1 -b .pam-unix-remove-obsolete-defines

%build
%meson \
  -Daudit=enabled \
  -Delogind=disabled \
%if %{without nis}
  -Dnis=disabled \
%endif
  -Dlogind=disabled \
  -Dopenssl=enabled \
  -Dpam_userdb=enabled \
  -Ddb=gdbm \
  -Dselinux=enabled
%meson_build

%install
# Install the macros file
install -D -m 644 %{SOURCE3} %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name}

# Install the binaries, libraries, and modules.
%meson_install

# Temporary compat link
ln -sf pam_sepermit.so %{buildroot}%{_pam_moduledir}/pam_selinux_permit.so

# RPM uses docs from source tree
rm -rf %{buildroot}%{_datadir}/doc/Linux-PAM
# Included in setup package
rm -f %{buildroot}%{_sysconfdir}/environment

# Install default configuration files.
install -d -m 755 %{buildroot}%{_pam_confdir}
install -d -m 755 %{buildroot}%{_pam_vendordir}
install -m 644 %{SOURCE5} %{buildroot}%{_pam_confdir}/other
install -m 644 %{SOURCE10} %{buildroot}%{_pam_confdir}/config-util
install -m 600 /dev/null %{buildroot}%{_pam_secconfdir}/opasswd
install -d -m 755 %{buildroot}/var/log
install -d -m 755 %{buildroot}/var/run/faillock

# Install man pages.
install -m 644 %{SOURCE12} %{SOURCE13} %{SOURCE17} %{buildroot}%{_mandir}/man5/
ln -sf system-auth.5 %{buildroot}%{_mandir}/man5/password-auth.5
ln -sf system-auth.5 %{buildroot}%{_mandir}/man5/fingerprint-auth.5
ln -sf system-auth.5 %{buildroot}%{_mandir}/man5/smartcard-auth.5


for phase in auth acct passwd session ; do
  ln -sf pam_unix.so %{buildroot}%{_pam_moduledir}/pam_unix_${phase}.so
done

# Remove .la files and make new .so links -- this depends on the value
# of _libdir not changing, and *not* being /usr/lib.
for lib in libpam libpamc libpam_misc ; do
  rm -f %{buildroot}%{_pam_libdir}/${lib}.la
done
rm -f %{buildroot}%{_pam_moduledir}/*.la

%if "%{_pam_libdir}" != "%{_libdir}"
install -d -m 755 %{buildroot}%{_libdir}
for lib in libpam libpamc libpam_misc ; do
  pushd %{buildroot}%{_libdir}
  ln -sf %{_pam_libdir}/${lib}.so.*.* ${lib}.so
  popd
  rm -f %{buildroot}%{_pam_libdir}/${lib}.so
done
%endif

# Duplicate doc file sets.
rm -fr %{buildroot}/usr/share/doc/pam

# Install the file for autocreation of /var/run subdirectories on boot
install -m644 -D %{SOURCE15} %{buildroot}%{_prefix}/lib/tmpfiles.d/pam.conf

# Install systemd unit file.
install -m644 -D %{_vpath_builddir}/modules/pam_namespace/pam_namespace.service \
  %{buildroot}%{_unitdir}/pam_namespace.service

# Install doc files to unified location.
install -d -m 755 %{buildroot}%{_pkgdocdir}/{adg/html,mwg/html,sag/html}
install -p -m 644 doc/specs/rfc86.0.txt %{buildroot}%{_pkgdocdir}
for i in adg mwg sag; do
  install -p -m 644 %{_vpath_builddir}/doc/$i/*.txt %{buildroot}%{_pkgdocdir}/$i
%if %{build_pdf}
  install -p -m 644 %{_vpath_builddir}/doc/$i/*.pdf %{buildroot}%{_pkgdocdir}/$i
%endif
  cp -pr %{_vpath_builddir}/doc/$i/html/* %{buildroot}%{_pkgdocdir}/$i/html
done
find %{buildroot}%{_pkgdocdir} -type d | xargs chmod 755
find %{buildroot}%{_pkgdocdir} -type f | xargs chmod 644

%find_lang Linux-PAM

%check
# Make sure every module subdirectory gave us a module.  Yes, this is hackish.
for dir in modules/pam_* ; do
if [ -d ${dir} ] ; then
  [ ${dir} = "modules/pam_lastlog" ] && continue
  [ ${dir} = "modules/pam_selinux" ] && continue
  [ ${dir} = "modules/pam_sepermit" ] && continue
  [ ${dir} = "modules/pam_tty_audit" ] && continue
  if ! ls -1 %{buildroot}%{_pam_moduledir}/`basename ${dir}`*.so ; then
    echo ERROR `basename ${dir}` did not build a module.
    exit 1
  fi
fi
done

# Check for module problems.  Specifically, check that every module we just
# installed can actually be loaded by a minimal PAM-aware application.
/sbin/ldconfig -n %{buildroot}%{_pam_libdir}
for module in %{buildroot}%{_pam_moduledir}/pam*.so ; do
  if ! env LD_LIBRARY_PATH=%{buildroot}%{_pam_libdir} \
       %{SOURCE11} -ldl -lpam -L%{buildroot}%{_libdir} ${module} ; then
    echo ERROR module: ${module} cannot be loaded.
    exit 1
  fi
done

%files -f Linux-PAM.lang
%license Copyright
%license gpl-2.0.txt
%dir %{_pam_confdir}
%dir %{_pam_vendordir}
%config(noreplace) %{_pam_confdir}/other
%config(noreplace) %{_pam_confdir}/config-util
%{_rpmconfigdir}/macros.d/macros.%{name}
%{_sbindir}/pam_namespace_helper
%{_sbindir}/faillock
%attr(4755,root,root) %{_sbindir}/pam_timestamp_check
%attr(4755,root,root) %{_sbindir}/unix_chkpwd
%attr(0700,root,root) %{_sbindir}/unix_update
%attr(0755,root,root) %{_sbindir}/mkhomedir_helper
%attr(0755,root,root) %{_sbindir}/pwhistory_helper
%dir %{_pam_moduledir}
%{_pam_moduledir}/pam_access.so
%{_pam_moduledir}/pam_canonicalize_user.so
%{_pam_moduledir}/pam_chroot.so
%{_pam_moduledir}/pam_debug.so
%{_pam_moduledir}/pam_deny.so
%{_pam_moduledir}/pam_echo.so
%{_pam_moduledir}/pam_env.so
%{_pam_moduledir}/pam_exec.so
%{_pam_moduledir}/pam_faildelay.so
%{_pam_moduledir}/pam_faillock.so
%{_pam_moduledir}/pam_filter.so
%{_pam_moduledir}/pam_ftp.so
%{_pam_moduledir}/pam_group.so
%{_pam_moduledir}/pam_issue.so
%{_pam_moduledir}/pam_keyinit.so
%{_pam_moduledir}/pam_limits.so
%{_pam_moduledir}/pam_listfile.so
%{_pam_moduledir}/pam_localuser.so
%{_pam_moduledir}/pam_loginuid.so
%{_pam_moduledir}/pam_mail.so
%{_pam_moduledir}/pam_mkhomedir.so
%{_pam_moduledir}/pam_motd.so
%{_pam_moduledir}/pam_namespace.so
%{_pam_moduledir}/pam_nologin.so
%{_pam_moduledir}/pam_permit.so
%{_pam_moduledir}/pam_postgresok.so
%{_pam_moduledir}/pam_pwhistory.so
%{_pam_moduledir}/pam_rhosts.so
%{_pam_moduledir}/pam_rootok.so
%{_pam_moduledir}/pam_selinux.so
%{_pam_moduledir}/pam_selinux_permit.so
%{_pam_moduledir}/pam_sepermit.so
%{_pam_moduledir}/pam_securetty.so
%{_pam_moduledir}/pam_setquota.so
%{_pam_moduledir}/pam_shells.so
%{_pam_moduledir}/pam_stress.so
%{_pam_moduledir}/pam_succeed_if.so
%{_pam_moduledir}/pam_time.so
%{_pam_moduledir}/pam_timestamp.so
%{_pam_moduledir}/pam_tty_audit.so
%{_pam_moduledir}/pam_umask.so
%{_pam_moduledir}/pam_unix.so
%{_pam_moduledir}/pam_unix_acct.so
%{_pam_moduledir}/pam_unix_auth.so
%{_pam_moduledir}/pam_unix_passwd.so
%{_pam_moduledir}/pam_unix_session.so
%{_pam_moduledir}/pam_userdb.so
%{_pam_moduledir}/pam_usertype.so
%{_pam_moduledir}/pam_warn.so
%{_pam_moduledir}/pam_wheel.so
%{_pam_moduledir}/pam_xauth.so
%{_pam_moduledir}/pam_filter
%{_unitdir}/pam_namespace.service
%dir %{_pam_secconfdir}
%config(noreplace) %{_pam_secconfdir}/access.conf
%config(noreplace) %{_pam_secconfdir}/chroot.conf
%config(noreplace) %{_pam_secconfdir}/faillock.conf
%config(noreplace) %{_pam_secconfdir}/group.conf
%config(noreplace) %{_pam_secconfdir}/limits.conf
%dir %{_pam_secconfdir}/limits.d
%config(noreplace) %{_pam_secconfdir}/namespace.conf
%dir %{_pam_secconfdir}/namespace.d
%attr(755,root,root) %config(noreplace) %{_pam_secconfdir}/namespace.init
%config(noreplace) %{_pam_secconfdir}/pam_env.conf
%config(noreplace) %{_pam_secconfdir}/pwhistory.conf
%config(noreplace) %{_pam_secconfdir}/time.conf
%config(noreplace) %{_pam_secconfdir}/opasswd
%config(noreplace) %{_pam_secconfdir}/sepermit.conf
%dir /var/run/sepermit
%dir /var/run/faillock
%{_prefix}/lib/tmpfiles.d/pam.conf
%{_mandir}/man5/*
%{_mandir}/man8/*

%files devel
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/rfc86.0.txt
%{_includedir}/security
%{_mandir}/man3/*
%{_libdir}/libpam.so
%{_libdir}/libpamc.so
%{_libdir}/libpam_misc.so
%{_libdir}/pkgconfig/pam.pc
%{_libdir}/pkgconfig/pam_misc.pc
%{_libdir}/pkgconfig/pamc.pc

%files doc
%doc %{_pkgdocdir}

%files libs
%license Copyright
%license gpl-2.0.txt
%{_pam_libdir}/libpam.so.%{so_ver}*
%{_pam_libdir}/libpamc.so.%{so_ver}*
%{_pam_libdir}/libpam_misc.so.%{so_ver}*

%changelog
* Fri Jan  9 2026 Iker Pedrosa <ipedrosa@redhat.com> - 1.7.1-4
- pam_unix: remove obsolete HAVE_YP_* to fix NIS
  Resolves: #2363005

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 15 2025 Iker Pedrosa <ipedrosa@redhat.com> - 1.7.1-2
- FSWC: Migrate to lastlog2
  Link: <https://fedoraproject.org/wiki/Changes/Migrate_to_lastlog2>
  Resolves: #2361594

* Wed Jun 18 2025 Iker Pedrosa <ipedrosa@redhat.com> - 1.7.1-1
- Rebase to release 1.7.1
- pam_access: fix group name match regression (#2367080)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 22 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.7.0-3
- pam_access: rework resolving of tokens as hostname.
  Resolves: CVE-2024-10963

* Thu Oct 31 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.7.0-2
- Fix documentation

* Tue Oct 29 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.7.0-1
- Rebase to release 1.7.0 (#2321512)
- Rebase to pam-redhat-1.2.0
- build: update to meson build system
- doc: disable build for i686

* Wed Oct 23 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.1-8
- pam_access: always match local address and clarify LOCAL keyword behaviour

* Wed Oct 16 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.1-7
- Rebuilt for libeconf soname bump

* Thu Aug 15 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 1.6.1-6
- Disable NIS on RHEL

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul  1 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.1-4
- spec: Use Requires(meta): authselect (#2291235)

* Tue May 28 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.1-3
- pam_env: fixes for NULL environment variables (#2280896)

* Mon May 27 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.1-2
- Several fixes for issues detected by static analyzer tools

* Wed Apr 10 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.1-1
- Rebase to release 1.6.1

* Thu Feb 15 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.0-2
- pam_unix: do not warn if password aging is disabled (#2263689)

* Tue Jan 23 2024 Iker Pedrosa <ipedrosa@redhat.com> - 1.6.0-1
- Rebase to release 1.6.0
  Resolves: #2258964

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 18 2023 Ding-Yi Chen <dchen@redhat.com> - 1.5.3-9
- pam.conf: Remove tallylog (#2253817)

* Tue Nov 21 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.3-8
- Suggest libdb-convert-util (#2245149 and #1788543)

* Tue Nov  7 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.3-7
- Include openssl-devel build dependency

* Fri Nov  3 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.3-6
- Drop explicit dependencies (#2247250)

* Mon Oct 30 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.3-5
- Explicitly state package dependencies and reorganize them

* Mon Oct 23 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.2-4
- Switch pam_userdb from BerkeleyDB to GDBM (#2245149 and #1788543)

* Thu Oct 19 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.3-3
- pam_pwhistory: fix passing NULL filename argument to pwhistory helper

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri May 19 2023 Björn Esser <besser82@fedoraproject.org> - 1.5.3-1
- Rebase to release 1.5.3
  Resolves: #2196709
- Drop pam-1.5.2-pwhistory-config.patch and pam-1.5.2-configure-c99.patch,
  as those patches are implemented upstream
- Realign left-over patches
- Update build requirements for documentation (docbook5)
- Remove --enable-vendordir from configuration
- Enable (deprecated) pam_lastlog module

* Tue Apr 25 2023 Björn Esser <besser82@fedoraproject.org> - 1.5.2-19
- Replace deprecated '%%patchN' with '%%patch -P N'

* Tue Apr 25 2023 Arjun Shankar <arjun@redhat.com> - 1.5.2-18
- Port configure script to C99

* Thu Feb  9 2023 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.2-17
- Remove pam_console (#2166692)
- Rebase to pam-redhat-1.2.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.2-15
- SPDX license migration

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 18 2022 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.2-13
- pam_pwhistory: load config from file

* Sun Feb 27 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.2-12
- Add Conflicts for pam version before the split

* Thu Feb 17 2022 Björn Esser <besser82@fedoraproject.org> - 1.5.2-11
- Split shared libraries into pam-libs package (#2055572)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 10 2022 Ondrej Mosnacek <omosnace@redhat.com> - 1.5.2-9
- Remove conflicting ownership of motd.d directories

* Tue Nov 16 2021 Pavel Březina <pbrezina@redhat.com> - 1.5.2-8
- systemd-auth, smartcard-auth, fingerprint-auth, password-auth and postlogin are now owned by authselect (#2023738)

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.2-7
- Rebuild(libnsl2)

* Wed Oct 06 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.2-6
- Remove old cruft from spec file
- Rename docs sub-package to doc
- Replace $RPM_BUILD_ROOT with %%{buildroot}
- Move documentation to %%{_pkgdocdir}
- Constantly use spaces for indentation

* Thu Sep 23 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.2-5
- Rebase to pam-redhat-1.1.5
- Drop explicit dependency on openssl, as auto-deps will pull it in
- Conditionalize BR: openssl >= 3.0.0 to supported distributions

* Thu Sep 23 2021 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.2-4
- Remove the /etc/motd.d directory to exclude its ownership from pam (#1968131)
- pam_timestamp: enable openssl hmac authentication on supported
  distributions (Fedora >= 36 and RHEL >= 9) (#1947294)
- Clean spec file: organize dependencies and move URL location

* Thu Sep 23 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.2-3
- Update patch for parallel build

* Wed Sep 22 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.2-2
- Add a patch to fix parallel builds with autgenerated sources

* Sat Sep 04 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.2-1
- Rebase to release 1.5.2
  Resolves: #2001208
- Add so_ver macro to avoid accidental soname bumps
- Add a patch to fix a missing header include in pam_console

* Thu Jul 22 2021 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.1-9
- Add macros file to allow other packages to stop hardcoding directory names

* Fri Jul  9 2021 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.1-8
- Fix issues detected by covscan tool

* Thu Jun 10 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.1-7
- Change the default password hash method to yescrypt

* Thu Jun 10 2021 Björn Esser <besser82@fedoraproject.org> - 1.5.1-6
- Add a patch to not use crypt_checksalt for password expiration
  Resolves: #1965345, #1967150

* Fri Apr 16 2021 Benjamin Berg <bberg@redhat.com> - 1.5.1-5
- Add script to avoid fingerprint-auth issues for long term Fedora users
  Resolves: #1942443

* Mon Apr 12 2021 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.1-4
- Change fingerprint-auth.pamd to return PAM_AUTHINFO_UNAVAIL from pam_fprintd.so
- Clean auto-generated message from pam stack files

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 30 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.1-2
- Add BuildRequires: make (#1902520)

* Thu Nov 26 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.1-1
- Rebase to release 1.5.1
- fix CVE-2020-27780: authentication bypass when the user doesn't exist
  and root password is blank (#1901173)

* Wed Nov 11 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.5.0-1
- Rebase to release 1.5.0
- Rebase to pam-redhat-1.1.4
- Remove pam_cracklib, pam_tally and pam_tally2
- spec file cleanup

* Fri Nov  6 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.4.0-7
- libpam: fix memory leak in pam_start (#1894630)

* Mon Oct 19 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.4.0-6
- pam_unix: fix missing initialization of daysleft  (#1887077)
- pam_motd: change privilege message prompt to default (#1861640)

* Wed Oct 14 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.4.0-5
- pam_motd: read motd files with target user credentials skipping unreadable ones (#1861640)
- Clarify upstreamed patches

* Tue Aug 04 2020 Tom Stellard <tstellar@redhat.com> - 1.4.0-4
- Add BuildRequires: gcc
- https://docs.fedoraproject.org/en-US/packaging-guidelines/C_and_C++/#_packaging

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul  2 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.4.0-2
- Enable layered configuration with distribution configs in /usr/share/pam.d
- Added new pam-redhat tarball to lookaside cache

* Wed Jun 24 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.4.0-1
- Rebased to release 1.4.0
- Rebased to pam-redhat-1.1.3
- Removed pam_cracklib as it has been deprecated

* Mon Jun 22 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.3.1-28
- pam_faillock: change /run/faillock/$USER permissions to 0660 (#1661822)

* Wed Jun 17 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.3.1-27
- pam_unix and pam_usertype: avoid determining if user exists (#1629598)

* Thu May 14 2020 Iker Pedrosa <ipedrosa@redhat.com> 1.3.1-26
- pam_tty_audit: if kernel audit is disabled return PAM_IGNORE (#1775357)
- pam_modutil_sanitize_helper_fds: fix SIGPIPE effect of PAM_MODUTIL_PIPE_FD (#1791970)

* Thu Apr 23 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.3.1-25
- docs: splitted documentation in subpackage -docs

* Mon Mar 9 2020 Iker Pedrosa <ipedrosa@redhat.com> - 1.3.1-24
- pam_selinux: check unknown object classes or permissions in current policy

* Tue Feb 4 2020 Pavel Březina <pbrezina@redhat.com> - 1.3.1-23
- Add pam_usertype.so

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Dec 18 2019 Tomáš Mráz <tmraz@redhat.com> 1.3.1-21
- pam_faillock: Fix regression in admin_group support

* Wed Oct 16 2019 Tomáš Mráz <tmraz@redhat.com> 1.3.1-20
- pam_namespace: Support noexec, nosuid and nodev flags for tmpfs mounts
- Drop tallylog and pam_tally documentation
- pam_faillock: Support local_users_only option
- pam_lastlog: Do not display failed attempts with PAM_SILENT flag
- pam_lastlog: Support unlimited option to override fsize limit
- pam_unix: Log if user authenticated without password
- pam_tty_audit: Improve manual page
- Optimize closing fds when spawning helpers
- Fix duplicate password verification in pam_authtok_verify()

* Mon Sep  9 2019 Tomáš Mráz <tmraz@redhat.com> 1.3.1-19
- pam_faillock: Support configuration file /etc/security/faillock.conf

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.3.1-16
- Rebuilt for libcrypt.so.2 (#1666033)

* Thu Dec 20 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.1-15
- Add the motd.d directories (empty) to silence warnings and to
  provide proper ownership for them (#1660935)

* Tue Dec  4 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.1-14
- Update Red Hat PAM modules to version 1.0.0 which includes pam_faillock
- Drop also pam_tally2 which was obsoleted and deprecated long time ago

* Sun Dec 02 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.1-13
- Backport upstream commit reporting disabled or invalid hashes to syslog
- Backport upstream commit fixing syslog for disabled or invalid hashes

* Wed Nov 28 2018 Robert Fairley <rfairley@redhat.com> 1.3.1-12
- Backport upstream commit pam_motd: Support multiple motd paths specified, with filename overrides (#69)
- Backport upstream commit pam_motd: Fix segmentation fault when no motd_dir specified (#76)

* Mon Nov 26 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.1-11
- Completely drop the check of invalid or disabled salt via crypt_checksalt

* Sun Nov 25 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.1-10
- Fix passphraseless sudo with crypt_checksalt (#1653023)

* Fri Nov 23 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.1-9
- Backport upstream commit removing an obsolete prototype
- Backport upstream commit preferring bcrypt_b ($2b$) for blowfish
- Backport upstream commit preferring gensalt with autoentropy
- Backport upstream commit using crypt_checksalt for password aging
- Backport upstream commit adding support for (gost-)yescrypt
- Update the no-MD5-fallback patch for alignment

* Fri Nov 16 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.1-8
- Use %%ldconfig_scriptlets
- Drop Requires(post), not needed anymore
- Prefer %%global over %%define

* Tue Nov 13 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.1-7
- when building against libxcrypt >= 4.3.3-2, we can avoid the explicit
  dependency on libxcrypt >= 4.3.3-1

* Mon Nov 12 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.1-6
- add explicit (Build)Requires for libxcrypt >= 4.3.3-1

* Mon Nov 12 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.1-5
- rebuilt against libxcrypt-4.3.3 to enable the use of crypt_gensalt_r

* Mon Sep 10 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.1-4
- add pam_umask to postlogin PAM configuration file
- fix some issues found by Coverity scan

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun  8 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.1-1
- use /run instead of /var/run in pamtmp.conf (#1588612)

* Fri May 18 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.1-1
- new upstream release 1.3.1 with multiple improvements

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 30 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.0-9
- and the NIS support now also requires libnsl2

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.3.0-8
- Rebuilt for switch to libxcrypt

* Thu Jan 11 2018 Tomáš Mráz <tmraz@redhat.com> 1.3.0-7
- the NIS support now requires libtirpc

* Mon Aug 21 2017 Tomáš Mráz <tmraz@redhat.com> 1.3.0-6
- add admin_group option to pam_faillock (#1285550)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 20 2017 Tomáš Mráz <tmraz@redhat.com> 1.3.0-3
- drop superfluous 'Changing password' message from pam_unix (#658289)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri May  6 2016 Tomáš Mráz <tmraz@redhat.com> 1.3.0-1
- new upstream release with multiple improvements

* Mon Apr 11 2016 Tomáš Mráz <tmraz@redhat.com> 1.2.1-8
- make cracklib-dicts dependency weak (#1323172)

* Wed Apr  6 2016 Tomáš Mráz <tmraz@redhat.com> 1.2.1-7
- do not drop PAM_OLDAUTHTOK if mismatched - can be used by further modules

* Mon Apr  4 2016 Tomáš Mráz <tmraz@redhat.com> 1.2.1-6
- pam_unix: use pam_get_authtok() and improve prompting

* Fri Feb  5 2016 Tomáš Mráz <tmraz@redhat.com> 1.2.1-5
- fix console device name in console.handlers (#1270224)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 16 2015 Tomáš Mráz <tmraz@redhat.com> 1.2.1-3
- pam_faillock: add possibility to set unlock_time to never

* Wed Aug 12 2015 Tomáš Mráz <tmraz@redhat.com> 1.2.1-2
- drop the nproc limit setting, it is causing more harm than it solves

* Fri Jun 26 2015 Tomáš Mráz <tmraz@redhat.com> 1.2.1-1
- new upstream release fixing security issue with unlimited password length

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 15 2015 Tomáš Mráz <tmraz@redhat.com> 1.2.0-1
- new upstream release with multiple minor improvements

* Fri Oct 17 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-18
- use USER_MGMT type for auditing in the pam_tally2 and faillock
  apps (#1151576)

* Thu Sep 11 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-17
- update the audit-grantor patch with the upstream changes
- pam_userdb: correct the example in man page (#1078784)
- pam_limits: check whether the utmp login entry is valid (#1080023)
- pam_console_apply: do not print error if console.perms.d is empty
- pam_limits: nofile refers to open file descriptors (#1111220)
- apply PIE and full RELRO to all binaries built

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-15
- audit the module names that granted access
- pam_faillock: update to latest version

* Wed Jul 30 2014 Tom Callaway <spot@fedoraproject.org> - 1.1.8-14
- fix license handling

* Wed Jul 16 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-13
- be tolerant to corrupted opasswd file

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 22 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-11
- pam_loginuid: make it return PAM_IGNORE in containers

* Mon Mar 31 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-10
- fix CVE-2014-2583: potential path traversal issue in pam_timestamp

* Wed Mar 26 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-9
- pam_pwhistory: call the helper if SELinux enabled

* Tue Mar 11 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-8
- fix CVE-2013-7041: use case sensitive comparison in pam_userdb

* Mon Mar 10 2014 Tomáš Mráz <tmraz@redhat.com> 1.1.8-7
- rename the 90-nproc.conf to 20-nproc.conf (#1071618)
- canonicalize user name in pam_selinux (#1071010)
- refresh the pam-redhat tarball

* Mon Dec 16 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.8-4
- raise the default soft nproc limit to 4096

* Mon Dec  2 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.8-3
- updated translations

* Mon Oct 21 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.8-2
- update lastlog with pam_lastlog also for su (#1021108)

* Mon Oct 14 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.8-1
- new upstream release
- pam_tty_audit: allow the module to work with old kernels

* Fri Oct  4 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.7-3
- pam_tty_audit: proper initialization of the tty_audit_status struct

* Mon Sep 30 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.7-2
- add "local_users_only" to pam_pwquality in default configuration

* Fri Sep 13 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.7-1
- new upstream release

* Wed Aug  7 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.6-14
- use links instead of w3m to create txt documentation
- recognize login session in pam_sepermit to prevent gdm from locking (#969174)
- add support for disabling password logging in pam_tty_audit

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jul 11 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.6-12
- add auditing of SELinux policy violation in pam_rootok (#965723)
- add SELinux helper to pam_pwhistory

* Tue May  7 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.6-11
- the default isadir is more correct

* Wed Apr 24 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.6-10
- pam_unix: do not fail with bad ld.so.preload

* Fri Mar 22 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.6-9
- do not fail if btmp file is corrupted (#906852)
- fix strict aliasing warnings in build
- UsrMove
- use authtok_type with pam_pwquality in system-auth
- remove manual_context handling from pam_selinux (#876976)
- other minor specfile cleanups

* Tue Mar 19 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.6-8
- check NULL return from crypt() calls (#915316)

* Thu Mar 14 2013 Tomáš Mráz <tmraz@redhat.com> 1.1.6-7
- add workaround for low nproc limit for confined root user (#432903)

* Thu Feb 21 2013 Karsten Hopp <karsten@redhat.com> 1.1.6-6
- add support for ppc64p7 arch (Power7 optimized)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Tomas Mraz <tmraz@redhat.com> 1.1.6-4
- fix build with current autotools

* Mon Oct 15 2012 Tomas Mraz <tmraz@redhat.com> 1.1.6-3
- add support for tmpfs mount options in pam_namespace

* Mon Sep  3 2012 Tomas Mraz <tmraz@redhat.com> 1.1.6-2
- link setuid binaries with full relro (#853158)
- add rhost and tty to auditing data in modules (#677664)

* Fri Aug 17 2012 Tomas Mraz <tmraz@redhat.com> - 1.1.6-1
- new upstream release

* Thu Aug  9 2012 Tomas Mraz <tmraz@redhat.com> - 1.1.5-9
- make the pam_lastlog module in postlogin 'optional' (#846843)

* Mon Aug  6 2012 Tomas Mraz <tmraz@redhat.com> - 1.1.5-8
- fix build failure in pam_unix
- add display of previous bad login attempts to postlogin.pamd
- put the tmpfiles.d config to /usr/lib and rename it to pam.conf
- build against libdb-5

* Wed May  9 2012 Tomas Mraz <tmraz@redhat.com> 1.1.5-7
- add inactive account lock out functionality to pam_lastlog
- fix pam_unix remember user name matching
- add gecoscheck and maxclassrepeat functionality to pam_cracklib
- correctly check for crypt() returning NULL in pam_unix
- pam_unix - do not fallback to MD5 on password change
  if requested algorithm not supported by crypt() (#818741)
- install empty directories

* Wed May  9 2012 Tomas Mraz <tmraz@redhat.com> 1.1.5-6
- add pam_systemd to session modules

* Tue Jan 31 2012 Tomas Mraz <tmraz@redhat.com> 1.1.5-5
- fix pam_namespace leaking the protect mounts to parent namespace (#755216)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Tomas Mraz <tmraz@redhat.com> 1.1.5-3
- add a note to limits.conf (#754285)

* Thu Nov 24 2011 Tomas Mraz <tmraz@redhat.com> 1.1.5-2
- use pam_pwquality instead of pam_cracklib

* Thu Nov 24 2011 Tomas Mraz <tmraz@redhat.com> 1.1.5-1
- upgrade to new upstream release

* Thu Aug 25 2011 Tomas Mraz <tmraz@redhat.com> 1.1.4-4
- fix dereference in pam_env
- fix wrong parse of user@host pattern in pam_access (#732081)

* Sat Jul 23 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.1.4-3
- Rebuild to fix trailing slashes in provided dirs added by rpm 4.9.1.

* Fri Jul 15 2011 Tomas Mraz <tmraz@redhat.com> 1.1.4-2
- clear supplementary groups in pam_console handler execution

* Mon Jun 27 2011 Tomas Mraz <tmraz@redhat.com> 1.1.4-1
- upgrade to new upstream release

* Tue Jun  7 2011 Tomas Mraz <tmraz@redhat.com> 1.1.3-10
- detect the shared / and make the polydir mounts private based on that
- fix memory leak and other small errors in pam_namespace

* Thu Jun  2 2011 Tomas Mraz <tmraz@redhat.com> 1.1.3-9
- add support for explicit marking of the polydir mount private (#623522)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 22 2010 Tomas Mraz <tmraz@redhat.com> 1.1.3-7
- add postlogin common PAM configuration file (#665059)

* Tue Dec 14 2010 Tomas Mraz <tmraz@redhat.com> 1.1.3-6
- include patches recently submitted and applied to upstream CVS

* Thu Nov 25 2010 Tomas Mraz <tmraz@redhat.com> 1.1.3-5
- add config for autocreation of subdirectories in /var/run (#656655)
- automatically enable kernel console in pam_securetty

* Wed Nov 10 2010 Tomas Mraz <tmraz@redhat.com> 1.1.3-4
- fix memory leak in pam_faillock

* Wed Nov 10 2010 Tomas Mraz <tmraz@redhat.com> 1.1.3-3
- fix segfault in faillock utility
- remove some cases where the information of existence of
  an user account could be leaked by the pam_faillock,
  document the remaining case

* Fri Nov  5 2010 Tomas Mraz <tmraz@redhat.com> 1.1.3-2
- fix a mistake in the abstract X-socket connect
- make pam_faillock work with screensaver

* Mon Nov  1 2010 Tomas Mraz <tmraz@redhat.com> 1.1.3-1
- upgrade to new upstream release fixing CVE-2010-3316 CVE-2010-3435
  CVE-2010-3853
- try to connect to an abstract X-socket first to verify we are
  at real console (#647191)

* Wed Sep 29 2010 jkeating - 1.1.2-2
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Tomas Mraz <tmraz@redhat.com> 1.1.2-1
- add pam_faillock module implementing temporary account lock out based
  on authentication failures during a specified interval
- do not build some auxiliary tools that are not installed that require
  flex-static to build
- upgrade to new upstream release

* Thu Jul 15 2010 Tomas Mraz <tmraz@redhat.com> 1.1.1-5
- do not overwrite tallylog with empty file on upgrade

* Mon Feb 15 2010 Tomas Mraz <tmraz@redhat.com> 1.1.1-4
- change the default password hash to sha512

* Fri Jan 22 2010 Tomas Mraz <tmraz@redhat.com> 1.1.1-3
- fix wrong prompt when pam_get_authtok is used for new password

* Mon Jan 18 2010 Tomas Mraz <tmraz@redhat.com> 1.1.1-2
- fix build with disabled audit and SELinux (#556211, #556212)

* Thu Dec 17 2009 Tomas Mraz <tmraz@redhat.com> 1.1.1-1
- new upstream version with minor changes

* Mon Nov  2 2009 Tomas Mraz <tmraz@redhat.com> 1.1.0-7
- pam_console: fix memory corruption when executing handlers (patch by
  Stas Sergeev) and a few more fixes in the handler execution code (#532302)

* Thu Oct 29 2009 Tomas Mraz <tmraz@redhat.com> 1.1.0-6
- pam_xauth: set the approprate context when creating .xauth files (#531530)

* Tue Sep  1 2009 Tomas Mraz <tmraz@redhat.com> 1.1.0-5
- do not change permissions with pam_console_apply
- drop obsolete pam_tally module and the faillog file (#461258)

* Wed Aug 19 2009 Tomas Mraz <tmraz@redhat.com> 1.1.0-4
- rebuild with new libaudit

* Mon Jul 27 2009 Tomas Mraz <tmraz@redhat.com> 1.1.0-3
- fix for pam_cracklib from upstream

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 23 2009 Tomas Mraz <tmraz@redhat.com> 1.1.0-1
- update to new upstream version

* Wed May 13 2009 Tomas Mraz <tmraz@redhat.com> 1.0.92-1
- update to new upstream version

* Fri Apr 10 2009 Tomas Mraz <tmraz@redhat.com> 1.0.91-6
- add password-auth, fingerprint-auth, and smartcard-auth
  for applications which can use them namely gdm (#494874)
  patch by Ray Strode

* Thu Mar 26 2009 Tomas Mraz <tmraz@redhat.com> 1.0.91-5
- replace also other std descriptors (#491471)

* Tue Mar 17 2009 Tomas Mraz <tmraz@redhat.com> 1.0.91-3
- we must replace the stdin when execing the helper (#490644)

* Mon Mar 16 2009 Tomas Mraz <tmraz@redhat.com> 1.0.91-2
- do not close stdout/err when execing the helpers (#488147)

* Mon Mar  9 2009 Tomas Mraz <tmraz@redhat.com> 1.0.91-1
- upgrade to new upstream release

* Fri Feb 27 2009 Tomas Mraz <tmraz@redhat.com> 1.0.90-4
- fix parsing of config files containing non-ASCII characters
- fix CVE-2009-0579 (mininimum days for password change ignored) (#487216)
- pam_access: improve handling of hostname resolution

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.90-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan 19 2009 Tomas Mraz <tmraz@redhat.com> 1.0.90-2
- add helper to pam_mkhomedir for proper SELinux confinement (#476784)

* Tue Dec 16 2008 Tomas Mraz <tmraz@redhat.com> 1.0.90-1
- upgrade to new upstream release
- add --disable-prelude (#466242)

* Tue Sep 23 2008 Tomas Mraz <tmraz@redhat.com> 1.0.2-2
- new password quality checks in pam_cracklib
- report failed logins from btmp in pam_lastlog
- allow larger groups in modutil functions
- fix leaked file descriptor in pam_tally

* Mon Sep  8 2008 Tomas Mraz <tmraz@redhat.com> 1.0.2-1
- pam_loginuid: uids are unsigned (#460241)
- new minor upstream release
- use external db4
- drop tests for not pulling in libpthread (as NPTL should
  be safe)

* Wed Jul  9 2008 Tomas Mraz <tmraz@redhat.com> 1.0.1-5
- update internal db4

* Wed May 21 2008 Tomas Mraz <tmraz@redhat.com> 1.0.1-4
- pam_namespace: allow safe creation of directories owned by user (#437116)
- pam_unix: fix multiple error prompts on password change (#443872)

* Tue May 20 2008 Tomas Mraz <tmraz@redhat.com> 1.0.1-3
- pam_selinux: add env_params option which will be used by OpenSSH
- fix build with new autoconf

* Tue Apr 22 2008 Tomas Mraz <tmraz@redhat.com> 1.0.1-2
- pam_selinux: restore execcon properly (#443667)

* Fri Apr 18 2008 Tomas Mraz <tmraz@redhat.com> 1.0.1-1
- upgrade to new upstream release (one bugfix only)
- fix pam_sepermit use in screensavers

* Mon Apr  7 2008 Tomas Mraz <tmraz@redhat.com> 1.0.0-2
- fix regression in pam_set_item

* Fri Apr  4 2008 Tomas Mraz <tmraz@redhat.com> 1.0.0-1
- upgrade to new upstream release (bugfix only)

* Thu Mar 20 2008 Tomas Mraz <tmraz@redhat.com> 0.99.10.0-4
- pam_namespace: fix problem with level polyinst (#438264)
- pam_namespace: improve override checking for umount
- pam_selinux: fix syslogging a context after free() (#438338)

* Thu Feb 28 2008 Tomas Mraz <tmraz@redhat.com> 0.99.10.0-3
- update pam-redhat module tarball
- update internal db4

* Fri Feb 22 2008 Tomas Mraz <tmraz@redhat.com> 0.99.10.0-2
- if shadow is readable for an user do not prevent him from
  authenticating any user with unix_chkpwd (#433459)
- call audit from unix_chkpwd when appropriate

* Fri Feb 15 2008 Tomas Mraz <tmraz@redhat.com> 0.99.10.0-1
- new upstream release
- add default soft limit for nproc of 1024 to prevent
  accidental fork bombs (#432903)

* Mon Feb  4 2008 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-18
- allow the package to build without SELinux and audit support (#431415)
- macro usage cleanup

* Mon Jan 28 2008 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-17
- test for setkeycreatecon correctly
- add exclusive login mode of operation to pam_selinux_permit (original
  patch by Dan Walsh)

* Tue Jan 22 2008 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-16
- add auditing to pam_access, pam_limits, and pam_time
- moved sanity testing code to check script

* Mon Jan 14 2008 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-15
- merge review fixes (#226228)

* Tue Jan  8 2008 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-14
- support for sha256 and sha512 password hashes
- account expiry checks moved to unix_chkpwd helper

* Wed Jan  2 2008 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-13
- wildcard match support in pam_tty_audit (by Miloslav Trmač)

* Thu Nov 29 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-12
- add pam_tty_audit module (#244352) - written by Miloslav Trmač

* Wed Nov  7 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-11
- add substack support

* Tue Sep 25 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-10
- update db4 to 4.6.19 (#274661)

* Fri Sep 21 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-9
- do not preserve contexts when copying skel and other namespace.init
  fixes (#298941)
- do not free memory sent to putenv (#231698)

* Wed Sep 19 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-8
- add pam_selinux_permit module
- pam_succeed_if: fix in operator (#295151)

* Tue Sep 18 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-7
- when SELinux enabled always run the helper binary instead of
  direct shadow access (#293181)

* Fri Aug 24 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-6
- do not ask for blank password when SELinux confined (#254044)
- initialize homedirs in namespace init script (original patch by dwalsh)

* Wed Aug 22 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-5
- most devices are now handled by HAL and not pam_console (patch by davidz)
- license tag fix
- multifunction scanner device support (#251468)

* Mon Aug 13 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-4
- fix auth regression when uid != 0 from previous build (#251804)

* Mon Aug  6 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-3
- updated db4 to 4.6.18 (#249740)
- added user and new instance parameters to namespace init
- document the new features of pam_namespace
- do not log an audit error when uid != 0 (#249870)

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 0.99.8.1-2
- rebuild for toolchain bug

* Mon Jul 23 2007 Tomas Mraz <tmraz@redhat.com> 0.99.8.1-1
- upgrade to latest upstream version
- add some firewire devices to default console perms (#240770)

* Thu Apr 26 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.1-6
- pam_namespace: better document behavior on failure (#237249)
- pam_unix: split out passwd change to a new helper binary (#236316)
- pam_namespace: add support for temporary logons (#241226)

* Fri Apr 13 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.1-5
- pam_selinux: improve context change auditing (#234781)
- pam_namespace: fix parsing config file with unknown users (#234513)

* Fri Mar 23 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.1-4
- pam_console: always decrement use count (#230823)
- pam_namespace: use raw context for poly dir name (#227345)
- pam_namespace: truncate long poly dir name (append hash) (#230120)
- we don't patch any po files anymore

* Wed Feb 21 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.1-3
- correctly relabel tty in the default case (#229542)
- pam_unix: cleanup of bigcrypt support
- pam_unix: allow modification of '*' passwords to root

* Tue Feb  6 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.1-2
- more X displays as consoles (#227462)

* Wed Jan 24 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.1-1
- upgrade to new upstream version resolving CVE-2007-0003
- pam_namespace: unmount poly dir for override users

* Mon Jan 22 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.0-2
- add back min salt length requirement which was erroneously removed
  upstream (CVE-2007-0003)

* Fri Jan 19 2007 Tomas Mraz <tmraz@redhat.com> 0.99.7.0-1
- upgrade to new upstream version
- drop pam_stack module as it is obsolete
- some changes to silence rpmlint

* Tue Jan 16 2007 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-8
- properly include /var/log/faillog and tallylog as ghosts
  and create them in post script (#209646)
- update gmo files as we patch some po files (#218271)
- add use_current_range option to pam_selinux (#220487)
- improve the role selection in pam_selinux
- remove shortcut on Password: in ja locale (#218271)
- revert to old euid and not ruid when setting euid in pam_keyinit (#219486)
- rename selinux-namespace patch to namespace-level

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 0.99.6.2-7
- fix selection of role

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 0.99.6.2-6
- add possibility to pam_namespace to only change MLS component
- Resolves: Bug #216184

* Thu Nov 30 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-5
- add select-context option to pam_selinux (#213812)
- autoreconf won't work with autoconf-2.61 as configure.in is not yet adjusted
  for it

* Mon Nov 13 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-4
- update internal db4 to 4.5.20 version
- move setgid before setuid in pam_keyinit (#212329)
- make username check in pam_unix consistent with useradd (#212153)

* Tue Oct 24 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-3.3
- don't overflow a buffer in pam_namespace (#211989)

* Mon Oct 16 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-3.2
- /var/log/faillog and tallylog must be config(noreplace)

* Fri Oct 13 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-3.1
- preserve effective uid in namespace.init script (LSPP for newrole)
- include /var/log/faillog and tallylog to filelist (#209646)
- add ids to .xml docs so the generated html is always the same (#210569)

* Thu Sep 28 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-3
- add pam_namespace option no_unmount_on_close, required for newrole

* Mon Sep  4 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-2
- silence pam_succeed_if in default system-auth (#205067)
- round the pam_timestamp_check sleep up to wake up at the start of the
  wallclock second (#205068)

* Thu Aug 31 2006 Tomas Mraz <tmraz@redhat.com> 0.99.6.2-1
- upgrade to new upstream version, as there are mostly bugfixes except
  improved documentation
- add support for session and password service for pam_access and
  pam_succeed_if
- system-auth: skip session pam_unix for crond service

* Thu Aug 10 2006 Dan Walsh <dwalsh@redhat.com> 0.99.5.0-8
- Add new setkeycreatecon call to pam_selinux to make sure keyring has correct context

* Thu Aug 10 2006 Tomas Mraz <tmraz@redhat.com> 0.99.5.0-7
- revoke keyrings properly when pam_keyinit called as root (#201048)
- pam_succeed_if should return PAM_USER_UNKNOWN when getpwnam fails (#197748)

* Wed Aug  2 2006 Tomas Mraz <tmraz@redhat.com> 0.99.5.0-6
- revoke keyrings properly when pam_keyinit called more than once (#201048)
  patch by David Howells

* Fri Jul 21 2006 Tomas Mraz <tmraz@redhat.com> 0.99.5.0-5
- don't log pam_keyinit debug messages by default (#199783)

* Fri Jul 21 2006 Tomas Mraz <tmraz@redhat.com> 0.99.5.0-4
- drop ainit from console.handlers (#199561)

* Mon Jul 17 2006 Tomas Mraz <tmraz@redhat.com> 0.99.5.0-3
- don't report error in pam_selinux for nonexistent tty (#188722)
- add pam_keyinit to the default system-auth file (#198623)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.99.5.0-2.1
- rebuild

* Mon Jul  3 2006 Tomas Mraz <tmraz@redhat.com> 0.99.5.0-2
- fixed network match in pam_access (patch by Dan Yefimov)

* Fri Jun 30 2006 Tomas Mraz <tmraz@redhat.com> 0.99.5.0-1
- updated to a new upstream release
- added service as value to be matched and list matching to
  pam_succeed_if
- namespace.init was missing from EXTRA_DIST

* Thu Jun  8 2006 Tomas Mraz <tmraz@redhat.com> 0.99.4.0-5
- updated pam_namespace with latest patch by Janak Desai
- merged pam_namespace patches
- added buildrequires libtool
- fixed a few rpmlint warnings

* Wed May 24 2006 Tomas Mraz <tmraz@redhat.com> 0.99.4.0-4
- actually don't link to libssl as it is not used (#191915)

* Wed May 17 2006 Tomas Mraz <tmraz@redhat.com> 0.99.4.0-3
- use md5 implementation from pam_unix in pam_namespace
- pam_namespace should call setexeccon only when selinux is enabled

* Tue May 16 2006 Tomas Mraz <tmraz@redhat.com> 0.99.4.0-2
- pam_console_apply shouldn't access /var when called with -r (#191401)
- actually apply the large-uid patch
- don't build hmactest in pam_timestamp so openssl-devel is not required
- add missing buildrequires (#191915)

* Wed May 10 2006 Tomas Mraz <tmraz@redhat.com> 0.99.4.0-1
- upgrade to new upstream version
- make pam_console_apply not dependent on glib
- support large uids in pam_tally, pam_tally2

* Thu May  4 2006 Tomas Mraz <tmraz@redhat.com> 0.99.3.0-5
- the namespace instance init script is now in /etc/security (#190148)
- pam_namespace: added missing braces (#190026)
- pam_tally(2): never call fclose twice on the same FILE (from upstream)

* Wed Apr 26 2006 Tomas Mraz <tmraz@redhat.com> 0.99.3.0-4
- fixed console device class for irda (#189966)
- make pam_console_apply fail gracefully when a class is missing

* Tue Apr 25 2006 Tomas Mraz <tmraz@redhat.com> 0.99.3.0-3
- added pam_namespace module written by Janak Desai (per-user /tmp
support)
- new pam-redhat modules version

* Fri Feb 24 2006 Tomas Mraz <tmraz@redhat.com> 0.99.3.0-2
- added try_first_pass option to pam_cracklib
- use try_first_pass for pam_unix and pam_cracklib in
  system-auth (#182350)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.99.3.0-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.99.3.0-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb  3 2006 Tomas Mraz <tmraz@redhat.com> 0.99.3.0-1
- new upstream version
- updated db4 to 4.3.29
- added module pam_tally2 with auditing support
- added manual pages for system-auth and config-util (#179584)

* Tue Jan  3 2006 Tomas Mraz <tmraz@redhat.com> 0.99.2.1-3
- remove 'initscripts' dependency (#176508)
- update pam-redhat modules, merged patches

* Fri Dec 16 2005 Tomas Mraz <tmraz@redhat.com> 0.99.2.1-2
- fix dangling symlinks in -devel (#175929)
- link libaudit only where necessary
- actually compile in audit support

* Thu Dec 15 2005 Tomas Mraz <tmraz@redhat.com> 0.99.2.1-1
- support netgroup matching in pam_succeed_if
- upgrade to new release
- drop pam_pwdb as it was obsolete long ago
- we don't build static libraries anymore

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 15 2005 Tomas Mraz <tmraz@redhat.com> 0.80-14
- pam_stack is deprecated - log its usage

* Wed Oct 26 2005 Tomas Mraz <tmraz@redhat.com> 0.80-13
- fixed CAN-2005-2977 unix_chkpwd should skip user verification only if
  run as root (#168181)
- link pam_loginuid to libaudit
- support no tty in pam_access (#170467)
- updated audit patch (by Steve Grubb)
- the previous pam_selinux change was not applied properly
- pam_xauth: look for the xauth binary in multiple directories (#171164)

* Wed Oct 26 2005 Dan Walsh <dwalsh@redhat.com> 0.80-12
- Eliminate multiple in pam_selinux

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 0.80-11
- Eliminate fail over for getseuserbyname call

* Thu Oct 13 2005 Dan Walsh <dwalsh@redhat.com> 0.80-10
- Add getseuserbyname call for SELinux MCS/MLS policy

* Tue Oct  4 2005 Tomas Mraz <tmraz@redhat.com>
- pam_console manpage fixes (#169373)

* Fri Sep 30 2005 Tomas Mraz <tmraz@redhat.com> 0.80-9
- don't include ps and pdf docs (#168823)
- new common config file for configuration utilities
- remove glib2 dependency (#166979)

* Tue Sep 20 2005 Tomas Mraz <tmraz@redhat.com> 0.80-8
- process limit values other than RLIMIT_NICE correctly (#168790)
- pam_unix: always honor nis flag on password change (by Aaron Hope)

* Wed Aug 24 2005 Tomas Mraz <tmraz@redhat.com> 0.80-7
- don't fail in audit code when audit is not compiled in
  on the newest kernels (#166422)

* Mon Aug 01 2005 Tomas Mraz <tmraz@redhat.com> 0.80-6
- add option to pam_loginuid to require auditd

* Fri Jul 29 2005 Tomas Mraz <tmraz@redhat.com> 0.80-5
- fix NULL dereference in pam_userdb (#164418)

* Tue Jul 26 2005 Tomas Mraz <tmraz@redhat.com> 0.80-4
- fix 64bit bug in pam_pwdb
- don't crash in pam_unix if pam_get_data fail

* Fri Jul 22 2005 Tomas Mraz <tmraz@redhat.com> 0.80-3
- more pam_selinux permissive fixes (Dan Walsh)
- make binaries PIE (#158938)

* Mon Jul 18 2005 Tomas Mraz <tmraz@redhat.com> 0.80-2
- fixed module tests so the pam doesn't require itself to build (#163502)
- added buildprereq for building the documentation (#163503)
- relaxed permissions of binaries (u+w)

* Thu Jul 14 2005 Tomas Mraz <tmraz@redhat.com> 0.80-1
- upgrade to new upstream sources
- removed obsolete patches
- pam_selinux module shouldn't fail on broken configs unless
  policy is set to enforcing (Dan Walsh)

* Tue Jun 21 2005 Tomas Mraz <tmraz@redhat.com> 0.79-11
- update pam audit patch
- add support for new limits in kernel-2.6.12 (#157050)

* Thu Jun  9 2005 Tomas Mraz <tmraz@redhat.com> 0.79-10
- add the Requires dependency on audit-libs (#159885)
- pam_loginuid shouldn't report error when /proc/self/loginuid
  is missing (#159974)

* Fri May 20 2005 Tomas Mraz <tmraz@redhat.com> 0.79-9
- update the pam audit patch to support newest audit library,
  audit also pam_setcred calls (Steve Grubb)
- don't use the audit_fd as global static variable
- don't unset the XAUTHORITY when target user is root

* Mon May  2 2005 Tomas Mraz <tmraz@redhat.com> 0.79-8
- pam_console: support loading .perms files in the console.perms.d (#156069)

* Tue Apr 26 2005 Tomas Mraz <tmraz@redhat.com> 0.79-7
- pam_xauth: unset the XAUTHORITY variable on error, fix
  potential memory leaks
- modify path to IDE floppy devices in console.perms (#155560)

* Sat Apr 16 2005 Steve Grubb <sgrubb@redhat.com> 0.79-6
- Adjusted pam audit patch to make exception for ECONNREFUSED

* Tue Apr 12 2005 Tomas Mraz <tmraz@redhat.com> 0.79-5
- added auditing patch by Steve Grubb
- added cleanup patches for bugs found by Steve Grubb
- don't clear the shadow option of pam_unix if nis option used

* Fri Apr  8 2005 Tomas Mraz <tmraz@redhat.com> 0.79-4
- #150537 - flush input first then write the prompt

* Thu Apr  7 2005 Tomas Mraz <tmraz@redhat.com> 0.79-3
- make pam_unix LSB 2.0 compliant even when SELinux enabled
- #88127 - change both local and NIS passwords to keep them in sync,
  also fix a regression in passwd functionality on NIS master server

* Tue Apr  5 2005 Tomas Mraz <tmraz@redhat.com>
- #153711 fix wrong logging in pam_selinux when restoring tty label

* Sun Apr  3 2005 Tomas Mraz <tmraz@redhat.com> 0.79-2
- fix NULL deref in pam_tally when it's used in account phase

* Thu Mar 31 2005 Tomas Mraz <tmraz@redhat.com> 0.79-1
- upgrade to the new upstream release
- moved pam_loginuid to pam-redhat repository

* Wed Mar 23 2005 Tomas Mraz <tmraz@redhat.com> 0.78-9
- fix wrong logging in pam_console handlers
- add executing ainit handler for alsa sound dmix
- #147879, #112777 - change permissions for dri devices

* Fri Mar 18 2005 Tomas Mraz <tmraz@redhat.com> 0.78-8
- remove ownership and permissions handling from pam_console call
  pam_console_apply as a handler instead

* Mon Mar 14 2005 Tomas Mraz <tmraz@redhat.com> 0.78-7
- add pam_loginuid module for setting the the login uid for auditing purposes
  (by Steve Grubb)

* Thu Mar 10 2005 Tomas Mraz <tmraz@redhat.com> 0.78-6
- add functionality for running handler executables from pam_console
  when console lock was obtained/lost
- removed patches merged to pam-redhat

* Tue Mar  1 2005 Tomas Mraz <tmraz@redhat.com> 0.78-5
- echo why tests failed when rebuilding
- fixed some warnings and errors in pam_console for gcc4 build
- improved parsing pam_console config file

* Mon Feb 21 2005 Tomas Mraz <tmraz@redhat.com>
- don't log garbage in pam_console_apply (#147879)

* Tue Jan 18 2005 Tomas Mraz <tmraz@redhat.com>
- don't require exact db4 version only conflict with incompatible one

* Wed Jan 12 2005 Tomas Mraz <tmraz@redhat.com> 0.78-4
- updated pam-redhat from elvis CVS
- removed obsolete patches

* Mon Jan  3 2005 Jeff Johnson <jbj@redhat.com> 0.78-3
- depend on db-4.3.27, not db-4.3.21.

* Thu Nov 25 2004 Tomas Mraz <tmraz@redhat.com> 0.78-2
- add argument to pam_console_apply to restrict its work to specified files

* Tue Nov 23 2004 Tomas Mraz <tmraz@redhat.com> 0.78-1
- update to Linux-PAM-0.78
- #140451 parse passwd entries correctly and test for failure
- #137802 allow using pam_console for authentication

* Fri Nov 12 2004 Jeff Johnson <jbj@jbj.org> 0.77-67
- rebuild against db-4.3.21.

* Thu Nov 11 2004 Tomas Mraz <tmraz@redhat.com> 0.77-66
- #77646 log failures when renaming the files when changing password
- Log failure on missing /etc/security/opasswd when remember option is present

* Wed Nov 10 2004 Tomas Mraz <tmraz@redhat.com>
- #87628 pam_timestamp remembers authorization after logout
- #116956 fixed memory leaks in pam_stack

* Wed Oct 20 2004 Tomas Mraz <tmraz@redhat.com> 0.77-65
- #74062 modify the pwd-lock patch to remove NIS passwd changing deadlock

* Wed Oct 20 2004 Tomas Mraz <tmraz@redhat.com> 0.77-64
- #134941 pam_console should check X11 socket only on login

* Tue Oct 19 2004 Tomas Mraz <tmraz@redhat.com> 0.77-63
- Fix checking of group %%group syntax in pam_limits
- Drop fencepost patch as it was already fixed
  by upstream change from 0.75 to 0.77
- Fix brokenshadow patch

* Mon Oct 11 2004 Tomas Mraz <tmraz@redhat.com> 0.77-62
- Added bluetooth, raw1394 and flash to console.perms
- pam_console manpage fix

* Mon Oct 11 2004 Tomas Mraz <tmraz@redhat.com> 0.77-61
- #129328 pam_env shouldn't abort on missing /etc/environment
- #126985 pam_stack should always copy the conversation function
- #127524 add /etc/security/opasswd to files

* Tue Sep 28 2004 Phil Knirsch <pknirsch@redhat.com> 0.77-60
- Drop last patch again, fixed now correctly elsewhere

* Thu Sep 23 2004 Phil Knirsch <pknirsch@redhat.com> 0.77-59
- Fixed bug in pam_env where wrong initializer was used

* Fri Sep 17 2004 Dan Walsh <dwalsh@redhat.com> 0.77-58
- rebuild selinux patch using checkPasswdAccess

* Mon Sep 13 2004 Jindrich Novy <jnovy@redhat.com>
- rebuilt

* Mon Sep 13 2004 Tomas Mraz <tmraz@redhat.com> 0.77-56
- #75454 fixed locking when changing password
- #127054
- #125653 removed unnecessary getgrouplist call
- #124979 added quiet option to pam_succeed_if

* Mon Aug 30 2004 Warren Togami <wtogami@redhat.com> 0.77-55
- #126024 /dev/pmu console perms

* Wed Aug 4 2004 Dan Walsh <dwalsh@redhat.com> 0.77-54
- Move pam_console.lock to /var/run/console/

* Thu Jul 29 2004 Dan Walsh <dwalsh@redhat.com> 0.77-53
- Close fd[1] before pam_modutilread so that unix_verify will complete

* Tue Jul 27 2004 Alan Cox <alan@redhat.com> 0.77-52
- First chunk of Steve Grubb's resource leak and other fixes

* Tue Jul 27 2004 Alan Cox <alan@redhat.com> 0.77-51
- Fixed build testing of modules
- Fixed dependancies

* Tue Jul 20 2004 Dan Walsh <dwalsh@redhat.com> 0.77-50
- Change unix_chkpwd to return pam error codes

* Sat Jul 10 2004 Alan Cox <alan@redhat.com>
- Fixed the pam glib2 dependancy issue

* Mon Jun 21 2004 Alan Cox <alan@redhat.com>
- Fixed the pam_limits fencepost error (#79989) since nobody seems to
  be doing it

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 9 2004 Dan Walsh <dwalsh@redhat.com> 0.77-45
- Add requires libselinux > 1.8

* Thu Jun 3 2004 Dan Walsh <dwalsh@redhat.com> 0.77-44
- Add MLS Support to selinux patch

* Wed Jun 2 2004 Dan Walsh <dwalsh@redhat.com> 0.77-43
- Modify pam_selinux to use open and close param

* Fri May 28 2004 Dan Walsh <dwalsh@redhat.com> 0.77-42
- Split pam module into two parts open and close

* Tue May 18 2004 Phil Knirsch <pknirsch@redhat.com> 0.77-41
- Fixed 64bit segfault in pam_succeed_if module.

* Wed Apr 14 2004 Dan Walsh <dwalsh@redhat.com> 0.77-40
- Apply changes from audit.

* Mon Apr 12 2004 Dan Walsh <dwalsh@redhat.com> 0.77-39
- Change to only report failure on relabel if debug

* Wed Mar 3 2004 Dan Walsh <dwalsh@redhat.com> 0.77-38
- Fix error handling of pam_unix

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 0.77-36
- fix tty handling

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 0.77-35
- remove tty closing and opening from pam_selinux, it does not work.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 12 2004 Nalin Dahyabhai <nalin@redhat.com>
- pam_unix: also log successful password changes when using shadowed passwords

* Tue Feb 10 2004 Dan Walsh <dwalsh@redhat.com> 0.77-33
- close and reopen terminal after changing context.

* Thu Feb 5 2004 Dan Walsh <dwalsh@redhat.com> 0.77-32
- Check for valid tty

* Tue Feb 3 2004 Dan Walsh <dwalsh@redhat.com> 0.77-31
- Check for multiple > 1

* Mon Feb 2 2004 Dan Walsh <dwalsh@redhat.com> 0.77-30
- fix is_selinux_enabled call for pam_rootok

* Wed Jan 28 2004 Dan Walsh <dwalsh@redhat.com> 0.77-29
- More fixes to pam_selinux,pam_rootok

* Wed Jan 28 2004 Dan Walsh <dwalsh@redhat.com> 0.77-28
- turn on selinux

* Wed Jan 28 2004 Dan Walsh <dwalsh@redhat.com> 0.77-27
- Fix rootok check.

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 0.77-26
- fix is_selinux_enabled call

* Sun Jan 25 2004 Dan Walsh <dwalsh@redhat.com> 0.77-25
- Check if ROOTOK for SELinux

* Thu Jan 15 2004 Dan Walsh <dwalsh@redhat.com> 0.77-24
- Fix tty handling for pts in pam_selinux

* Thu Jan 15 2004 Dan Walsh <dwalsh@redhat.com> 0.77-23
- Need to add qualifier context for sudo situation

* Thu Jan 15 2004 Dan Walsh <dwalsh@redhat.com> 0.77-22
- Fix pam_selinux to use prevcon instead of pam_user so it will work for su.

* Fri Dec 12 2003 Bill Nottingham <notting@redhat.com> 0.77-21.sel
- add alsa devs to console.perms

* Thu Dec 11 2003 Jeff Johnson <jbj@jbj.org> 0.77-20.sel
- rebuild with db-4.2.52.
- build db4 in build_unix, not dist.

* Wed Nov 26 2003 Dan Walsh <dwalsh@redhat.com> 0.77-19.sel
- Change unix_chkpwd to handle unix_passwd and unix_acct
- This eliminates the need for pam modules to have read/write access to /etc/shadow.

* Thu Nov 20 2003 Dan Walsh <dwalsh@redhat.com> 0.77-18.sel
- Cleanup unix_chkpwd

* Mon Nov 03 2003 Dan Walsh <dwalsh@redhat.com> 0.77-17.sel
- Fix tty handling
- Add back multiple handling

* Mon Oct 27 2003 Dan Walsh <dwalsh@redhat.com> 0.77-16.sel
- Remove Multiple from man page of pam_selinux

* Thu Oct 23 2003 Nalin Dahyabhai <nalin@redhat.com> 0.77-15
- don't install _pam_aconf.h -- apps don't use it, other PAM headers which
  are installed don't use it, and its contents may be different for arches
  on a multilib system
- check for linkage problems in modules at %%install-time (kill #107093 dead)
- add buildprereq on flex (#101563)

* Wed Oct 22 2003 Nalin Dahyabhai <nalin@redhat.com>
- make pam_pwdb.so link with libnsl again so that it loads (#107093)
- remove now-bogus buildprereq on db4-devel (we use a bundled copy for
  pam_userdb to avoid symbol collisions with other db libraries in apps)

* Mon Oct 20 2003 Dan Walsh <dwalsh@redhat.com> 0.77-14.sel
- Add Russell Coker patch to handle /dev/pty

* Fri Oct 17 2003 Dan Walsh <dwalsh@redhat.com> 0.77-13.sel
- Turn on Selinux

* Fri Oct 17 2003 Dan Walsh <dwalsh@redhat.com> 0.77-12
- Fix pam_timestamp to work when 0 seconds have elapsed

* Mon Oct 6 2003 Dan Walsh <dwalsh@redhat.com> 0.77-11
- Turn off selinux

* Thu Sep 25 2003 Dan Walsh <dwalsh@redhat.com> 0.77-10.sel
- Turn on Selinux and remove multiple choice of context.

* Wed Sep 24 2003 Dan Walsh <dwalsh@redhat.com> 0.77-10
- Turn off selinux

* Wed Sep 24 2003 Dan Walsh <dwalsh@redhat.com> 0.77-9.sel
- Add Russell's patch to check password

* Wed Sep 17 2003 Dan Walsh <dwalsh@redhat.com> 0.77-8.sel
- handle ttys correctly in pam_selinux

* Fri Sep 05 2003 Dan Walsh <dwalsh@redhat.com> 0.77-7.sel
- Clean up memory problems and fix tty handling.

* Mon Jul 28 2003 Dan Walsh <dwalsh@redhat.com> 0.77-6
- Add manual context selection to pam_selinux

* Mon Jul 28 2003 Dan Walsh <dwalsh@redhat.com> 0.77-5
- Add pam_selinux

* Mon Jul 28 2003 Dan Walsh <dwalsh@redhat.com> 0.77-4
- Add SELinux support

* Thu Jul 24 2003 Nalin Dahyabhai <nalin@redhat.com> 0.77-3
- pam_postgresok: add
- pam_xauth: add "targetuser" argument

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com>
- pam_succeed_if: fix thinko in argument parsing which would walk past the
  end of the argument list

* Wed Jul  9 2003 Nalin Dahyabhai <nalin@redhat.com> 0.77-2
- reapply:
  - set handler for SIGCHLD to SIG_DFL around *_chkpwd, not SIG_IGN

* Mon Jul  7 2003 Nalin Dahyabhai <nalin@redhat.com> 0.77-1
- pam_timestamp: fail if the key file doesn't contain enough data

* Thu Jul  3 2003 Nalin Dahyabhai <nalin@redhat.com> 0.77-0
- update to 0.77 upstream release
  - pam_limits: limits now affect root as well
  - pam_nologin: returns PAM_IGNORE instead of PAM_SUCCESS unless "successok"
    is given as an argument
  - pam_userdb: correctly return PAM_AUTH_ERR instead of PAM_USER_UNKNOWN when
    invoked with the "key_only" argument and the database has an entry of the
    form "user-<wrongpassword>"
- use a bundled libdb for pam_userdb.so because the system copy uses threads,
  and demand-loading a shared library which uses threads into an application
  which doesn't is a Very Bad Idea

* Thu Jul  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- pam_timestamp: use a message authentication code to validate timestamp files

* Mon Jun 30 2003 Nalin Dahyabhai <nalin@redhat.com> 0.75-48.1
- rebuild

* Mon Jun  9 2003 Nalin Dahyabhai <nalin@redhat.com> 0.75-49
- modify calls to getlogin() to check the directory of the current TTY before
  searching for an entry in the utmp/utmpx file (#98020, #98826, CAN-2003-0388)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com> 0.75-48
- set handler for SIGCHLD to SIG_DFL around *_chkpwd, not SIG_IGN

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.75-47
- rebuilt

* Tue Dec 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-46
- pam_xauth: reintroduce ACL support, per the original white paper
- pam_xauth: default root's export ACL to none instead of everyone

* Mon Dec  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-45
- create /lib/security, even if it isn't /%%{_lib}/security, because we
  can't locate /lib/security/$ISA without it (noted by Arnd Bergmann)
- clear out the duplicate docs directory created during %%install

* Thu Nov 21 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-44
- fix syntax errors in pam_console's yacc parser which newer bison chokes on
- forcibly set FAKEROOT at make install time

* Tue Oct 22 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-43
- patch to interpret $ISA in case the fist module load attempt fails
- use $ISA in default configs

* Fri Oct 04 2002 Elliot Lee <sopwith@redhat.com> 0.75-42
- Since cracklib-dicts location will not be correctly detected without
  that package being installed, add buildreq for cracklib-dicts.
- Add patch57: makes configure use $LIBNAME when searching for cracklib
  dicts, and error out if not found.

* Thu Sep 12 2002 Than Ngo <than@redhat.com> 0.75-41.1
- Fixed pam config files

* Wed Sep 11 2002 Than Ngo <than@redhat.com> 0.75-41
- Added fix to install libs in correct directory on 64bit machine

* Fri Aug  2 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-40
- pam_timestamp_check: check that stdio descriptors are open before we're
  invoked
- add missing chroot.conf

* Mon Jul 29 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-39
- pam_timestamp: sundry fixes, use "unknown" as the tty when none is found

* Thu Jun 27 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-38
- pam_timestamp_check: be as smart about figuring out the tty as the module is

* Wed Jun 19 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-37
- pam_timestamp_check: remove extra unlink() call spotted by Havoc

* Mon Jun 17 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-36
- pam_timestamp: chown intermediate directories when creating them
- pam_timestamp_check: add -d flag to poll

* Thu May 23 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-35
- pam_timestamp: add some sanity checks
- pam_timestamp_check: add

* Wed May 22 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-34
- pam_timestamp: add a 'verbose' option

* Thu May 16 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-33
- rebuild with db4
- just bundle install-sh into the source package

* Tue Apr  9 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-32
- pam_unix: be more compatible with AIX-style shadowing (#19236)

* Thu Mar 28 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-31
- libpam_misc: fix possible infinite loop in misc_conv (#62195)
- pam_xauth: fix cases where DISPLAY is "localhost:screen" and the xauth
  key is actually stored using the system's hostname (#61524)

* Mon Mar 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-30
- rebuild

* Mon Mar 25 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-29
- rebuild

* Mon Mar 11 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-28
- include the pwdb config file

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-27
- adjust the pwdb-static patch to build pam_radius correctly (#59408)

* Fri Mar  1 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-26
- change the db4-devel build dependency to db3-devel

* Thu Feb 21 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-25
- rebuild

* Fri Feb  8 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-24
- pam_unix: log successful password changes
- remove pam_timestamp

* Thu Feb  7 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-23
- fix pwdb embedding
- add pam_timestamp

* Thu Jan 31 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-22
- swallow up pwdb 0.61.1 for building pam_pwdb

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 0.75-21
- pam_userdb: build with db4 instead of db3

* Thu Nov 22 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-20
- pam_stack: fix some memory leaks (reported by Fernando Trias)
- pam_chroot: integrate Owl patch to report the more common causes of failures

* Fri Nov  9 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-19
- fix a bug in the getpwnam_r wrapper which sometimes resulted in false
  positives for non-existent users

* Wed Nov  7 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-18
- include libpamc in the pam package (#55651)

* Fri Nov  2 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-17
- pam_xauth: don't free a string after passing it to putenv()

* Wed Oct 24 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-16
- pam_xauth: always return PAM_SUCCESS or PAM_SESSION_ERR instead of PAM_IGNORE,
  matching the previous behavior (libpam treats PAM_IGNORE from a single module
  in a stack as a session error, leading to false error messages if we just
  return PAM_IGNORE for all cases)

* Mon Oct 22 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-15
- reorder patches so that the reentrancy patch is applied last -- we never
  came to a consensus on how to guard against the bugs in calling applications
  which this sort of change addresses, and having them last allows for dropping
  in a better strategy for addressing this later on

* Mon Oct 15 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_rhosts: allow "+hostname" as a synonym for "hostname" to jive better
  with the hosts.equiv(5) man page
- use the automake install-sh instead of the autoconf install-sh, which
  disappeared somewhere between 2.50 and now

* Mon Oct  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- add pwdb as a buildprereq

* Fri Oct  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_tally: don't try to read past the end of faillog -- it probably contains
  garbage, which if written into the file later on will confuse /usr/bin/faillog

* Thu Oct  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_limits: don't just return if the user is root -- we'll want to set the
  priority (it could be negative to elevate root's sessions)
- pam_issue: fix off-by-one error allocating space for the prompt string

* Wed Oct  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_mkhomedir: recurse into subdirectories properly
- pam_mkhomedir: handle symlinks
- pam_mkhomedir: skip over special items in the skeleton directory

* Tue Oct  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- add cracklib as a buildprereq
- pam_wheel: don't ignore out if the user is attempting to switch to a
  unprivileged user (this lets pam_wheel do its thing when users attempt
  to get to system accounts or accounts of other unprivileged users)

* Fri Sep 28 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_xauth: close a possible DoS due to use of dotlock-style locking in
  world-writable directories by relocating the temporary file to the target
  user's home directory
- general: include headers local to this tree using relative paths so that
  system headers for PAM won't be pulled in, in case include paths don't
  take care of it

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_xauth: rewrite to skip refcounting and just use a temporary file
  created using mkstemp() in /tmp

* Tue Sep 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_userdb: fix the key_only flag so that the null-terminator of the
  user-password string isn't expected to be part of the key in the db file,
  matching the behavior of db_load 3.2.9

* Mon Sep 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_unix: use crypt() instead of bigcrypt() when salted field is less than
  the critical size which lets us know it was generated with bigcrypt()
- use a wrapper to handle ERANGE errors when calling get....._r functions:
  defining PAM_GETPWNAM_R and such (for getpwnam, getpwuid, getgrnam,
  getgrgid, and getspnam) before including _pam_macros.h will cause them
  to be implemented as static functions, similar to how defining PAM_SM_xxx
  is used to control whether or not PAM declares prototypes for certain
  functions

* Mon Sep 24 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-14
- pam_unix: argh, compare entire pruned salt string with crypted result, always

* Sat Sep  8 2001 Bill Nottingham <notting@redhat.com> 0.75-13
- ship /lib/lib{pam,pam_misc}.so for legacy package builds

* Thu Sep  6 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-12
- noreplace configuration files in /etc/security
- pam_console: update pam_console_apply and man pages to reflect
  /var/lock -> /var/run move

* Wed Sep  5 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-11
- pam_unix: fix the fix for #42394

* Tue Sep  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- modules: use getpwnam_r and friends instead of non-reentrant versions
- pam_console: clear generated .c and .h files in "clean" makefile target

* Thu Aug 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_stack: perform deep copy of conversation structures
- include the static libpam in the -devel subpackage (#52321)
- move development .so and .a files to %%{_libdir}
- pam_unix: don't barf on empty passwords (#51846)
- pam_unix: redo compatibility with "hash,age" data wrt bigcrypt (#42394)
- console.perms: add usb camera, scanner, and rio devices (#15528)
- pam_cracklib: initialize all options properly (#49613)

* Wed Aug 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_limits: don't rule out negative priorities

* Mon Aug 13 2001 Nalin Dahyabhai <nalin@redhat.com> 0.75-10
- pam_xauth: fix errors due to uninitialized data structure (fix from Tse Huong
  Choo)
- pam_xauth: random cleanups
- pam_console: use /var/run/console instead of /var/lock/console at install-time
- pam_unix: fix preserving of permissions on files which are manipulated

* Fri Aug 10 2001 Bill Nottingham <notting@redhat.com>
- fix segfault in pam_securetty

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_console: use /var/run/console instead of /var/lock/console for lock files
- pam_issue: read the right number of bytes from the file

* Mon Jul  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_wheel: don't error out if the group has no members, but is the user's
  primary GID (reported by David Vos)
- pam_unix: preserve permissions on files which are manipulated (#43706)
- pam_securetty: check if the user is the superuser before checking the tty,
  thereby allowing regular users access to services which don't set the
  PAM_TTY item (#39247)
- pam_access: define NIS and link with libnsl (#36864)

* Thu Jul  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- link libpam_misc against libpam

* Tue Jul  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_chroot: chdir() before chroot()

* Fri Jun 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_console: fix logic bug when changing permissions on single
  file and/or lists of files
- pam_console: return the proper error code (reported and patches
  for both from Frederic Crozat)
- change deprecated Copyright: tag in .spec file to License:

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- console.perms: change js* to js[0-9]*
- include pam_aconf.h in more modules (patches from Harald Welte)

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- console.perms: add apm_bios to the list of devices the console owner can use
- console.perms: add beep to the list of sound devices

* Mon May  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- link pam_console_apply statically with libglib (#38891)

* Mon Apr 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_access: compare IP addresses with the terminating ".", as documented
  (patch from Carlo Marcelo Arenas Belon, I think) (#16505)

* Mon Apr 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge up to 0.75
- pam_unix: temporarily ignore SIGCHLD while running the helper
- pam_pwdb: temporarily ignore SIGCHLD while running the helper
- pam_dispatch: default to uncached behavior if the cached chain is empty

* Fri Apr  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- correct speling errors in various debug messages and doc files (#33494)

* Thu Apr  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- prereq sed, fileutils (used in %%post)

* Wed Apr  4 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove /dev/dri from console.perms -- XFree86 munges it, so it's outside of
  our control (reminder from Daryll Strauss)
- add /dev/3dfx to console.perms

* Fri Mar 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_wheel: make 'trust' and 'deny' work together correctly
- pam_wheel: also check the user's primary gid
- pam_group: also initialize groups when called with PAM_REINITIALIZE_CRED

* Tue Mar 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- mention pam_console_apply in the see also section of the pam_console man pages

* Fri Mar 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- console.perms: /dev/vc/* should be a regexp, not a glob (thanks to
  Charles Lopes)

* Mon Mar 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- console.perms: /dev/cdroms/* should belong to the user, from Douglas
  Gilbert via Tim Waugh

* Thu Mar  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_console_apply: muck with devices even if the mount point doesn't exist

* Wed Mar  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_console: error out on undefined classes in pam_console config file
- console.perms: actually change the permissions on the new device classes
- pam_console: add an fstab= argument, and -f and -c flags to pam_console_apply
- pam_console: use g_log instead of g_critical when bailing out
- console.perms: logins on /dev/vc/* are also console logins, from Douglas
  Gilbert via Tim Waugh

* Tue Mar  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- add pam_console_apply
- /dev/pilot's usually a serial port (or a USB serial port), so revert its
  group to 'uucp' instead of 'tty' in console.perms
- change pam_console's behavior wrt directories -- directories which are
  mount points according to /etc/fstab are taken to be synonymous with
  their device special nodes, and directories which are not mount points
  are ignored

* Tue Feb 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- handle errors fork()ing in pam_xauth
- make the "other" config noreplace

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- user should own the /dev/video directory, not the non-existent /dev/v4l
- tweak pam_limits doc

* Wed Feb 21 2001 Nalin Dahyabhai <nalin@redhat.com>
- own /etc/security
- be more descriptive when logging messages from pam_limits
- pam_listfile: remove some debugging code (#28346)

* Mon Feb 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_lastlog: don't pass NULL to logwtmp()

* Fri Feb 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_listfile: fix argument parser (#27773)
- pam_lastlog: link to libutil

* Tue Feb 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- pam_limits: change the documented default config file to reflect the defaults
- pam_limits: you should be able to log in a total of maxlogins times, not
  (maxlogins - 1)
- handle group limits on maxlogins correctly (#25690)

* Mon Feb 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- change the pam_xauth default maximum "system user" ID from 499 to 99 (#26343)

* Wed Feb  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- refresh the default system-auth file, pam_access is out

* Mon Feb  5 2001 Nalin Dahyabhai <nalin@redhat.com>
- actually time out when attempting to lckpwdf() (#25889)
- include time.h in pam_issue (#25923)
- update the default system-auth to the one generated by authconfig 4.1.1
- handle getpw??? and getgr??? failures more gracefully (#26115)
- get rid of some extraneous {set,end}{pw,gr}ent() calls

* Tue Jan 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- overhaul pam_stack to account for abstraction libpam now provides

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove pam_radius at request of author

* Mon Jan 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge to 0.74
- make console.perms match perms set by MAKEDEV, and add some devfs device names
- add 'sed' to the buildprereq list (#24666)

* Sun Jan 21 2001 Matt Wilson <msw@redhat.com>
- added "exit 0" to the end of the pre script

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- self-hosting fix from Guy Streeter

* Wed Jan 17 2001 Nalin Dahyabhai <nalin@redhat.com>
- use gcc for LD_L to pull in intrinsic stuff on ia64

* Fri Jan 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- take another whack at compatibility with "hash,age" data in pam_unix (#21603)

* Wed Jan 10 2001 Nalin Dahyabhai <nalin@redhat.com>
- make the -devel subpackage unconditional

* Tue Jan  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- merge/update to 0.73

* Mon Dec 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- refresh from CVS -- some weird stuff crept into pam_unix

* Tue Dec 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix handling of "nis" when changing passwords by adding the checks for the
  data source to the password-updating module in pam_unix
- add the original copyright for pam_access (fix from Michael Gerdts)

* Thu Nov 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- redo similar() using a distance algorithm and drop the default dif_ok to 5
- readd -devel

* Wed Nov 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix similar() function in pam_cracklib (#14740)
- fix example in access.conf (#21467)
- add conditional compilation for building for 6.2 (for pam_userdb)
- tweak post to not use USESHADOW any more

* Tue Nov 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- make EINVAL setting lock limits in pam_limits non-fatal, because it's a 2.4ism

* Tue Nov 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- revert to DB 3.1, which is what we were supposed to be using from the get-go

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- add RLIMIT_LOCKS to pam_limits (patch from Jes Sorensen) (#20542)
- link pam_userdb to Berkeley DB 2.x to match 6.2's setup correctly

* Mon Nov  6 2000 Matt Wilson <msw@redhat.com>
- remove prereq on sh-utils, test ([) is built in to bash

* Thu Oct 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix the pam_userdb module breaking

* Wed Oct 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix pam_unix likeauth argument for authenticate(),setcred(),setcred()

* Tue Oct 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak pre script to be called in all upgrade cases
- get pam_unix to only care about the significant pieces of passwords it checks
- add /usr/include/db1/db.h as a build prereq to pull in the right include
  files, no matter whether they're in glibc-devel or db1-devel
- pam_userdb.c: include db1/db.h instead of db.h

* Wed Oct 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- add BuildPrereq for bison (suggested by Bryan Stillwell)

* Fri Oct  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- patch from Dmitry V. Levin to have pam_stack propagate the PAM fail_delay
- roll back the README for pam_xauth to actually be the right one
- tweak pam_stack to use the parent's service name when calling the substack

* Wed Oct  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- create /etc/sysconfig/authconfig at install-time if upgrading

* Mon Oct  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify the files list to make sure #16456 stays fixed
- make pam_stack track PAM_AUTHTOK and PAM_OLDAUTHTOK items
- add pam_chroot module
- self-hosting fixes from the -devel split
- update generated docs in the tree

* Tue Sep 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- split off a -devel subpackage
- install the developer man pages

* Sun Sep 10 2000 Bill Nottingham <notting@redhat.com>
- build libraries before modules

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix problems when looking for headers in /usr/include (#17236)
- clean up a couple of compile warnings

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- give users /dev/cdrom* instead of /dev/cdrom in console.perms (#16768)
- add nvidia control files to console.perms

* Tue Aug 22 2000 Bill Nottingham <notting@redhat.com>
- add DRI devices to console.perms (#16731)

* Thu Aug 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- move pam_filter modules to /lib/security/pam_filter (#16111)
- add pam_tally's application to allow counts to be reset (#16456)
- move README files to the txts subdirectory

* Mon Aug 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a postun that runs ldconfig
- clean up logging in pam_xauth

* Fri Aug  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- make the tarball include the release number in its name

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- add a broken_shadow option to pam_unix
- add all module README files to the documentation list (#16456)

* Tue Jul 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix pam_stack debug and losing-track-of-the-result bug

* Mon Jul 24 2000 Nalin Dahyabhai <nalin@redhat.com>
- rework pam_console's usage of syslog to actually be sane (#14646)

* Sat Jul 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- take the LOG_ERR flag off of some of pam_console's new messages

* Fri Jul 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- add pam_localuser

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- need to make pam_console's checking a little stronger
- only pass data up from pam_stack if the parent didn't already define it

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Nalin Dahyabhai <nalin@redhat.com>
- make pam_console's extra checks disableable
- simplify extra check to just check if the device owner is root
- add a debug log when pam_stack comes across a NULL item
- have pam_stack hand items up to the parent from the child

* Mon Jul  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix installation of pam_xauth man pages (#12417)
- forcibly strip helpers (#12430)
- try to make pam_console a little more discriminating

* Mon Jun 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- symlink libpam.so to libpam.so.%%{version}, and likewise for libpam_misc
- reverse order of checks in _unix_getpwnam for pam_unix

* Wed Jun 14 2000 Preston Brown <pbrown@redhat.com>
- include gpmctl in pam_console

* Mon Jun 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- add MANDIR definition and use it when installing man pages

* Mon Jun 05 2000 Preston Brown <pbrown@redhat.com>
- handle scanner and cdwriter devices in pam_console

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- add account management wrappers for pam_listfile, pam_nologin, pam_securetty,
  pam_shells, and pam_wheel

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- add system-auth control file
- let gethostname() call in pam_access.c be implicitly declared to avoid
  conflicting types if unistd.c declares it

* Mon May 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix problems compiling on Red Hat Linux 5.x (bug #11005)

* Wed Apr 26 2000 Bill Nottingham <notting@redhat.com>
- fix size assumptions in pam_(pwdb|unix) md5 code

* Mon Mar 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add new pam_stack module.
- Install pwdb_chkpwd and unix_chkpwd as the current user for non-root builds

* Sat Feb 05 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix pam_xauth bug #6191.

* Thu Feb 03 2000 Elliot Lee <sopwith@redhat.com>
- Add a patch to accept 'pts/N' in /etc/securetty as a match for tty '5'
  (which is what other pieces of the system think it is). Fixes bug #7641.

* Mon Jan 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- argh, turn off gratuitous debugging

* Wed Jan 19 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 0.72
- fix pam_unix password-changing bug
- fix pam_unix's cracklib support
- change package URL

* Mon Jan 03 2000 Cristian Gafton <gafton@redhat.com>
- don't allow '/' on service_name

* Thu Oct 21 1999 Cristian Gafton <gafton@redhat.com>
- enhance the pam_userdb module some more

* Fri Sep 24 1999 Cristian Gafton <gafton@redhat.com>
- add documenatation

* Tue Sep 21 1999 Michael K. Johnson <johnsonm@redhat.com>
- a tiny change to pam_console to make it not loose track of console users

* Mon Sep 20 1999 Michael K. Johnson <johnsonm@redhat.com>
- a few fixes to pam_xauth to make it more robust

* Wed Jul 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_console: added <xconsole> to manage /dev/console

* Thu Jul 01 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_xauth: New refcounting implementation based on idea from Stephen Tweedie

* Sat Apr 17 1999 Michael K. Johnson <johnsonm@redhat.com>
- added video4linux devices to /etc/security/console.perms

* Fri Apr 16 1999 Michael K. Johnson <johnsonm@redhat.com>
- added joystick lines to /etc/security/console.perms

* Thu Apr 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed a couple segfaults in pam_xauth uncovered by yesterday's fix...

* Wed Apr 14 1999 Cristian Gafton <gafton@redhat.com>
- use gcc -shared to link the shared libs

* Wed Apr 14 1999 Michael K. Johnson <johnsonm@redhat.com>
- many bug fixes in pam_xauth
- pam_console can now handle broken applications that do not set
  the PAM_TTY item.

* Tue Apr 13 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed glob/regexp confusion in pam_console, added kbd and fixed fb devices
- added pam_xauth module

* Sat Apr 10 1999 Cristian Gafton <gafton@redhat.com>
- pam_lastlog does wtmp handling now

* Thu Apr 08 1999 Michael K. Johnson <johnsonm@redhat.com>
- added option parsing to pam_console
- added framebuffer devices to default console.perms settings

* Wed Apr 07 1999 Cristian Gafton <gafton@redhat.com>
- fixed empty passwd handling in pam_pwdb

* Mon Mar 29 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed /dev/cdrom default user permissions back to 0600 in console.perms
  because some cdrom players open O_RDWR.

* Fri Mar 26 1999 Michael K. Johnson <johnsonm@redhat.com>
- added /dev/jaz and /dev/zip to console.perms

* Thu Mar 25 1999 Michael K. Johnson <johnsonm@redhat.com>
- changed the default user permissions for /dev/cdrom to 0400 in console.perms

* Fri Mar 19 1999 Michael K. Johnson <johnsonm@redhat.com>
- fixed a few bugs in pam_console

* Thu Mar 18 1999 Michael K. Johnson <johnsonm@redhat.com>
- pam_console authentication working
- added /etc/security/console.apps directory

* Mon Mar 15 1999 Michael K. Johnson <johnsonm@redhat.com>
- added pam_console files to filelist

* Fri Feb 12 1999 Cristian Gafton <gafton@redhat.com>
- upgraded to 0.66, some source cleanups

* Mon Dec 28 1998 Cristian Gafton <gafton@redhat.com>
- add patch from Savochkin Andrey Vladimirovich <saw@msu.ru> for umask
  security risk

* Fri Dec 18 1998 Cristian Gafton <gafton@redhat.com>
- upgrade to ver 0.65
- build the package out of internal CVS server
