%global libauditver     3.0
%global libsepolver     %{version}-1
%global libsemanagever  %{version}-1
%global libselinuxver   %{version}-1
%global __python3	%{_bindir}/python3
%global generatorsdir   %{_libdir}/systemd/system-generators
# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0
Summary:        SELinux policy core utilities
Name:           policycoreutils
Version:        3.6
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/SELinuxProject/selinux/wiki
Source0:        https://github.com/SELinuxProject/selinux/releases/download/%{version}/selinux-%{version}.tar.gz
Source1:        selinux-autorelabel
Source2:        selinux-autorelabel.service
Source3:        selinux-autorelabel-mark.service
Source4:        selinux-autorelabel.target
Source5:        selinux-autorelabel-generator.sh
BuildRequires:  audit-devel
BuildRequires:  audit-libs >= %{libauditver}
BuildRequires:  dbus-devel
BuildRequires:  dbus-glib-devel
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  git
BuildRequires:  libcap-devel
BuildRequires:  libselinux-devel >= %{libselinuxver}
BuildRequires:  libsemanage-devel >= %{libsemanagever}
BuildRequires:  libsepol-devel >= %{libsepolver}
BuildRequires:  pam-devel
BuildRequires:  python3-devel
BuildRequires:  pkgconf
BuildRequires:  systemd-devel
Requires:       coreutils
Requires:       diffutils
Requires:       gawk
Requires:       grep
Requires:       libselinux-utils >= %{libselinuxver}
Requires:       libsepol >= %{libsepolver}
Requires:       rpm
Requires:       sed
Requires:       util-linux
Conflicts:      initscripts < 9.66
Obsoletes:      policycoreutils < 2.0.61-2
Provides:       /sbin/fixfiles
Provides:       /sbin/restorecon

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

policycoreutils contains the policy core utilities that are required
for basic operation of a SELinux system.  These utilities include
load_policy to load policies, setfiles to label filesystems, newrole
to switch roles.

%prep
%autosetup -n selinux-%{version}

%build
%{set_build_flags}
export PYTHON=python3

%make_build -C policycoreutils LSPP_PRIV=y SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="%{_sbindir}" LIBSEPOLA="%{_libdir}/libsepol.a"
%make_build -C python SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"
%make_build -C semodule-utils SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"
%make_build -C restorecond SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a"

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
mkdir -p %{buildroot}/%{_usr}/share/doc/%{name}/

%make_install -C policycoreutils LSPP_PRIV=y   SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="%{_sbindir}" LIBSEPOLA="%{_libdir}/libsepol.a" CFLAGS="%{build_cflags} -fno-semantic-interposition"
%make_install -C python PYTHON=python3 SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" CFLAGS="%{build_cflags} -fno-semantic-interposition"
%make_install -C semodule-utils PYTHON=python3 SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" CFLAGS="%{build_cflags} -fno-semantic-interposition"
%make_install -C restorecond PYTHON=python3 SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" SYSTEMDDIR="/usr/lib/systemd" CFLAGS="%{build_cflags} -fno-semantic-interposition"

# Fix perms on newrole so that objcopy can process it
chmod 0755 %{buildroot}%{_bindir}/newrole

# Systemd
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/restorecond

rm -f %{buildroot}%{_mandir}/ru/man8/genhomedircon.8.gz
rm -f %{buildroot}%{_mandir}/ru/man8/open_init_pty.8*
rm -f %{buildroot}%{_mandir}/ru/man8/semodule_deps.8.gz
rm -f %{buildroot}%{_mandir}/man8/open_init_pty.8
rm -f %{buildroot}%{_sbindir}/open_init_pty
rm -f %{buildroot}%{_sbindir}/run_init
rm -f %{buildroot}%{_mandir}/ru/man8/run_init.8*
rm -f %{buildroot}%{_mandir}/man8/run_init.8*
rm -f %{buildroot}%{_sysconfdir}/pam.d/run_init*

mkdir   -m 755 -p %{buildroot}/%{generatorsdir}
mkdir   -m 755 -p %{buildroot}/%{_unitdir}
install -m 755 -p %{SOURCE1} %{buildroot}%{_libexecdir}/selinux/
install -m 644 -p %{SOURCE2} %{buildroot}%{_unitdir}/
install -m 644 -p %{SOURCE3} %{buildroot}%{_unitdir}/
install -m 644 -p %{SOURCE4} %{buildroot}%{_unitdir}/
install -m 755 -p %{SOURCE5} %{buildroot}%{generatorsdir}/


%package python-utils
Summary:        SELinux policy core python utilities
Requires:       policycoreutils-python3 = %{version}-%{release}
BuildArch:      noarch

%description python-utils
The policycoreutils-python-utils package contains the management tools use to manage
an SELinux environment.

%package python3
Summary:        SELinux policy core python3 interfaces
Requires:       checkpolicy
Requires:       libselinux-python3
Requires:       libsemanage-python3 >= %{libsemanagever}
Requires:       %{name} = %{version}-%{release}
Requires:       python3-audit
Requires:       setools-python3 >= 4.4.0
Provides:       python3-%{name} = %{version}-%{release}
BuildArch:      noarch

%description python3
The policycoreutils-python3 package contains the interfaces that can be used
by python 3 in an SELinux environment.

%package devel
Summary:        SELinux policy core policy devel utilities
Requires:       dnf
Requires:       make
Requires:       policycoreutils-python-utils

%description devel
The policycoreutils-devel package contains the management tools use to develop policy in an SELinux environment.

%package newrole
Summary:        The newrole application for RBAC/MLS
BuildRequires:  libcap-ng-devel
Requires:       policycoreutils = %{version}-%{release}

%description newrole
RBAC/MLS policy machines require newrole as a way of changing the role
or level of a logged in user.

%package restorecond
Summary:        SELinux restorecond utilities
BuildRequires:  systemd

%description restorecond
The policycoreutils-restorecond package contains the restorecond service.

%files python-utils
%license python/COPYING
%{_sbindir}/semanage
%{_bindir}/chcat
%{_bindir}/audit2allow
%{_bindir}/audit2why
%{_mandir}/man1/audit2allow.1*
%{_mandir}/ru/man1/audit2allow.1*
%{_mandir}/man1/audit2why.1*
%{_mandir}/ru/man1/audit2why.1*
%{_mandir}/man8/chcat.8*
%{_mandir}/ru/man8/chcat.8*
%{_mandir}/man8/semanage*.8*
%{_mandir}/ru/man8/semanage*.8*
%{_datadir}/bash-completion/completions/semanage

%files python3
%license python/COPYING
%{python3_sitelib}/__pycache__
%{python3_sitelib}/seobject.py*
%{python3_sitelib}/sepolgen
%dir %{python3_sitelib}/sepolicy
%{python3_sitelib}/sepolicy/templates
%dir %{python3_sitelib}/sepolicy/help
%{python3_sitelib}/sepolicy/help/*
%{python3_sitelib}/sepolicy/__init__.py*
%{python3_sitelib}/sepolicy/booleans.py*
%{python3_sitelib}/sepolicy/communicate.py*
%{python3_sitelib}/sepolicy/generate.py*
%{python3_sitelib}/sepolicy/gui.py*
%{python3_sitelib}/sepolicy/interface.py*
%{python3_sitelib}/sepolicy/manpage.py*
%{python3_sitelib}/sepolicy/network.py*
%{python3_sitelib}/sepolicy/sepolicy.glade
%{python3_sitelib}/sepolicy/transition.py*
%{python3_sitelib}/sepolicy/sedbus.py*
%{python3_sitelib}/sepolicy*.egg-info
%{python3_sitelib}/sepolicy/__pycache__
%{_mandir}/man8/sepolicy-gui.8.gz

%files devel
%{_bindir}/sepolgen
%{_bindir}/sepolgen-ifgen
%{_bindir}/sepolgen-ifgen-attr-helper
%dir %{_sharedstatedir}/sepolgen
%{_sharedstatedir}/sepolgen/perm_map
%{_bindir}/sepolicy
%{_mandir}/man8/sepolgen.8*
%{_mandir}/ru/man8/sepolgen.8*
%{_mandir}/man8/sepolicy-booleans.8*
%{_mandir}/man8/sepolicy-generate.8*
%{_mandir}/man8/sepolicy-interface.8*
%{_mandir}/man8/sepolicy-network.8*
%{_mandir}/man8/sepolicy.8*
%{_mandir}/man8/sepolicy-communicate.8*
%{_mandir}/man8/sepolicy-manpage.8*
%{_mandir}/man8/sepolicy-transition.8*
%{_mandir}/ru/man8/sepolicy*.8*
%{_usr}/share/bash-completion/completions/sepolicy

%files newrole
%license policycoreutils/COPYING
%attr(0755,root,root) %caps(cap_dac_read_search,cap_setpcap,cap_audit_write,cap_sys_admin,cap_fowner,cap_chown,cap_dac_override=pe) %{_bindir}/newrole
%{_mandir}/man1/newrole.1.gz
%{_mandir}/ru/man1/newrole.1.gz
%config(noreplace) %{_sysconfdir}/pam.d/newrole

%files restorecond
%license restorecond/COPYING
%{_sbindir}/restorecond
%{_unitdir}/restorecond.service
%{_libdir}/systemd/user/restorecond_user.service
%config(noreplace) %{_sysconfdir}/selinux/restorecond.conf
%config(noreplace) %{_sysconfdir}/selinux/restorecond_user.conf
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
%{_mandir}/man8/restorecond.8*
%{_mandir}/ru/man8/restorecond.8*
%{_mandir}/ru/man1/audit2why.1*
%{_mandir}/ru/man1/newrole.1*
%{_mandir}/ru/man5/selinux_config.5*
%{_mandir}/ru/man5/sestatus.conf.5*
%{_mandir}/ru/man8/genhomedircon.8*
%{_mandir}/ru/man8/restorecon_xattr.8*
%{_mandir}/ru/man8/semanage-boolean.8*
%{_mandir}/ru/man8/semanage-dontaudit.8*
%{_mandir}/ru/man8/semanage-export.8*
%{_mandir}/ru/man8/semanage-fcontext.8*
%{_mandir}/ru/man8/semanage-ibendport.8*
%{_mandir}/ru/man8/semanage-ibpkey.8*
%{_mandir}/ru/man8/semanage-import.8*
%{_mandir}/ru/man8/semanage-interface.8*
%{_mandir}/ru/man8/semanage-login.8*
%{_mandir}/ru/man8/semanage-module.8*
%{_mandir}/ru/man8/semanage-node.8*
%{_mandir}/ru/man8/semanage-permissive.8*
%{_mandir}/ru/man8/semanage-port.8*
%{_mandir}/ru/man8/semanage-user.8*
%{_mandir}/ru/man8/semodule_unpackage.8*
%{_mandir}/ru/man8/sepolgen.8*
%{_mandir}/ru/man8/sepolicy-booleans.8*
%{_mandir}/ru/man8/sepolicy-communicate.8*
%{_mandir}/ru/man8/sepolicy-generate.8*
%{_mandir}/ru/man8/sepolicy-gui.8*
%{_mandir}/ru/man8/sepolicy-interface.8*
%{_mandir}/ru/man8/sepolicy-manpage.8*
%{_mandir}/ru/man8/sepolicy-network.8*
%{_mandir}/ru/man8/sepolicy-transition.8*
%{_mandir}/ru/man8/sepolicy.8*

%files
%license policycoreutils/COPYING
%{_sbindir}/restorecon
%{_sbindir}/restorecon_xattr
%{_sbindir}/fixfiles
%{_sbindir}/setfiles
%{_sbindir}/load_policy
%{_sbindir}/genhomedircon
%{_sbindir}/setsebool
%{_sbindir}/semodule
%{_sbindir}/sestatus
%{_bindir}/secon
%{_bindir}/semodule_expand
%{_bindir}/semodule_link
%{_bindir}/semodule_package
%{_bindir}/semodule_unpackage
%{_bindir}/sestatus
%{_libexecdir}/selinux/hll
%{_libexecdir}/selinux/selinux-autorelabel
%{_unitdir}/selinux-autorelabel-mark.service
%{_unitdir}/selinux-autorelabel.service
%{_unitdir}/selinux-autorelabel.target
%{generatorsdir}/selinux-autorelabel-generator.sh
%config(noreplace) %{_sysconfdir}/sestatus.conf
%{_mandir}/man5/selinux_config.5.gz
%{_mandir}/ru/man5/selinux_config.5.gz
%{_mandir}/man5/sestatus.conf.5.gz
%{_mandir}/ru/man5/sestatus.conf.5.gz
%{_mandir}/man8/fixfiles.8*
%{_mandir}/ru/man8/fixfiles.8*
%{_mandir}/man8/load_policy.8*
%{_mandir}/ru/man8/load_policy.8*
%{_mandir}/man8/restorecon.8*
%{_mandir}/ru/man8/restorecon.8*
%{_mandir}/man8/restorecon_xattr.8*
%{_mandir}/ru/man8/restorecon_xattr.8*
%{_mandir}/man8/semodule.8*
%{_mandir}/ru/man8/semodule.8*
%{_mandir}/man8/sestatus.8*
%{_mandir}/ru/man8/sestatus.8*
%{_mandir}/man8/setfiles.8*
%{_mandir}/ru/man8/setfiles.8*
%{_mandir}/man8/setsebool.8*
%{_mandir}/ru/man8/setsebool.8*
%{_mandir}/man1/secon.1*
%{_mandir}/ru/man1/secon.1*
%{_mandir}/man8/genhomedircon.8*
%{_mandir}/ru/man8/genhomedircon.8*
%{_mandir}/man8/semodule_expand.8*
%{_mandir}/ru/man8/semodule_expand.8*
%{_mandir}/man8/semodule_link.8*
%{_mandir}/ru/man8/semodule_link.8*
%{_mandir}/man8/semodule_unpackage.8*
%{_mandir}/ru/man8/semodule_unpackage.8*
%{_mandir}/man8/semodule_package.8*
%{_mandir}/ru/man8/semodule_package.8*
%dir %{_datadir}/bash-completion
%{_datadir}/bash-completion/completions/setsebool
%doc %{_usr}/share/doc/%{name}
%{_datadir}/locale/*

%post
%systemd_post selinux-autorelabel-mark.service

%preun
%systemd_preun selinux-autorelabel-mark.service

%post restorecond
%systemd_post restorecond.service

%preun restorecond
%systemd_preun restorecond.service

%postun restorecond
%systemd_postun_with_restart restorecond.service

%changelog
* Fri Jan 12 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.6-1
- Auto-upgrade to 3.6 - Mariner 3.0 upgrade

* Fri Aug 13 2021 Thomas Crain <thcrain@microsoft.com> - 3.2-1
- Upgrade to latest upstream version
- Switch source to use upstream's combined tarball
- Add -fno-semantic-interposition to CFLAGS as recommended by upstream
- Lint spec
- License verified

* Fri Aug 21 2020 Daniel Burgener <daburgen@microsoft.com> - 2.9-6
- Initial CBL-Mariner import from Fedora 31 (license: MIT)
- License verified

* Thu Aug 29 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-5
- gui: Fix remove module in system-config-selinux (#1740936)

* Fri Aug 23 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-4
- fixfiles: Fix unbound variable problem

* Mon Aug  5 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-3
- Drop python2-policycoreutils
- Update ru man page translations
- fixfiles: Fix [-B] [-F] onboot

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 18 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-1
- SELinux userspace 2.9 release

* Mon Mar 11 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc2.1
- SELinux userspace 2.9-rc2 release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9-0.rc1.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 25 2019 Petr Lautrbach <plautrba@redhat.com> - 2.9-0.rc1.1
- SELinux userspace 2.9-rc1 release candidate

* Fri Jan 25 2019 Petr Lautrbach <plautrba@redhat.com> - 2.8-17
- python2-policycoreutils requires python2-ipaddress (#1669230)

* Tue Jan 22 2019 Petr Lautrbach <plautrba@redhat.com> - 2.8-16
- restorecond: Install DBUS service file with 644 permissions

* Mon Jan 21 2019 Petr Lautrbach <plautrba@redhat.com> - 2.8-15
- setsebool: support use of -P on SELinux-disabled hosts
- sepolicy: initialize mislabeled_files in __init__()
- audit2allow: use local sepolgen-ifgen-attr-helper for tests
- audit2allow: allow using audit2why as non-root user
- audit2allow/sepolgen-ifgen: show errors on stderr
- audit2allow/sepolgen-ifgen: add missing \n to error message
- sepolgen: close /etc/selinux/sepolgen.conf after parsing it
- sepolicy: Make policy files sorting more robust
- semanage: Load a store policy and set the store SELinux policy root

* Thu Dec 20 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-14
- chcat: fix removing categories on users with Fedora default setup
- semanage: Include MCS/MLS range when exporting local customizations
- semanage: Start exporting "ibendport" and "ibpkey" entries
- semanage: do not show "None" levels when using a non-MLS policy
- sepolicy: Add sepolicy.load_store_policy(store)
- semanage: import sepolicy only when it's needed
- semanage: move valid_types initialisations to class constructors

* Mon Dec 10 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-13
- chcat: use check_call instead of getstatusoutput
- Use matchbox-window-manager instead of openbox
- Use ipaddress python module instead of IPy
- semanage: Fix handling of -a/-e/-d/-r options
- semanage: Use standard argparse.error() method

* Mon Nov 12 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-12
- sepolicy,semanage: replace aliases with corresponding type names
- sepolicy-generate: Handle more reserved port types
- Fix RESOURCE_LEAK coverity scan defects

* Tue Oct 16 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-11
- sepolicy: Fix get_real_type_name to handle query failure properly
- sepolicy: search() for dontaudit rules as well

* Tue Oct  2 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-10
- semanage: "semanage user" does not use -s, fix documentation
- semanage: add a missing space in ibendport help
- sepolicy: Update to work with setools-4.2.0

* Fri Sep 14 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-9
- semanage: Stop rejecting aliases in semanage commands
- sepolicy: Stop rejecting aliases in sepolicy commands
- sepolicy: Fix "info" to search aliases as well
- setfiles: Improve description of -d switch

* Wed Sep 12 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-8
- Update translations

* Tue Sep  4 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-7
- Fix typo in newrole.1 manpage
- sepolgen: print all AV rules correctly
- sepolgen: fix access vector initialization
- Add xperms support to audit2allow
- semanage: Stop logging loginRecords changes
- semanage: Fix logger class definition
- semanage: Replace bare except with specific one
- semanage: fix Python syntax of catching several exceptions
- sepolgen: return NotImplemented instead of raising it
- sepolgen: fix refpolicy parsing of "permissive"

* Mon Aug  6 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-6
- Use split translation files
  https://github.com/fedora-selinux/selinux/issues/43

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8-4
- Rebuilt for Python 3.7

* Mon Jun 18 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-3
- selinux-autorelabel: Use plymouth --quit rather then --hide-splash (#1592221)
- selinux-autorelabel: Increment boot_indeterminate grub environment variable (#1592221)

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.8-2
- Rebuilt for Python 3.7

* Fri May 25 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-1
- SELinux userspace 2.8 release

* Tue May 22 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc3.2
- selinux-autorelabel: set UEFI boot order (BootNext) same as BootCurrent
- selinux-autorelabel: synchronize cached writes before reboot (#1385272)

* Tue May 15 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc3.1
- SELinux userspace 2.8-rc2 release candidate

* Fri May  4 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc2.1
- SELinux userspace 2.8-rc2 release candidate

* Mon Apr 23 2018 Petr Lautrbach <plautrba@redhat.com> - 2.8-0.rc1.1
- SELinux userspace 2.8-rc1 release candidate

* Thu Apr 19 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-20
- Drop python2 sepolicy gui files from policycoreutils-gui (#1566618)

* Wed Apr 18 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 2.7-19
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Apr  3 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-18
- Move semodule_* utilities to policycoreutils package (#1562549)

* Thu Mar 22 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-17
- semanage/seobject.py: Fix undefined store check (#1559174)

* Fri Mar 16 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-16
- Build python only subpackages as noarch
- Move semodule_package to policycoreutils-devel

* Tue Mar 13 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-15
- sepolicy: Fix translated strings with parameters
- sepolicy: Support non-MLS policy
- sepolicy: Initialize policy.ports as a dict in generate.py
- gui/polgengui.py: Use stop_emission_by_name instead of emit_stop_by_name
- Minor update for bash completion
- semodule_package: fix semodule_unpackage man page
- gui/semanagePage: Close "edit" and "add" dialogues when successfull
- gui/fcontextPage: Set default object class in addDialog\
- sepolgen: fix typo in PolicyGenerator
- build: follow standard semantics for DESTDIR and PREFIX

* Mon Feb 26 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-14
- Use Fedora RPM build flags (#1548740)

* Tue Feb 20 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-13
- Fix mangling of python shebangs

* Mon Feb 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.7-12
- Rename the python3 subpackage to have prefix, not suffix
- Use python3 prefixes in requires where possible

* Thu Feb 15 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-11
- Rewrite selinux-polgengui to use Gtk3
- Drop python2 and gnome-python2 from gui Requires

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Petr Lautrbach <plautrba@redhat.com> - 2.7-9
- Require audit-libs-python2

* Thu Jan 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.7-8
- Remove obsolete scriptlets

* Wed Dec 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-7
- semanage: bring semanageRecords.set_reload back to seobject.py (#1527745)

* Wed Dec 13 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-6
- semanage: make seobject.py backward compatible
- Own %%{pythonX_sitelib}/site-packages/sepolicy directories (#1522942)

* Wed Nov 22 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-5
- sepolicy: Fix sepolicy manpage
- semanage: Update Infiniband code to work on python3
- semanage: Fix export of ibendport entries
- semanage: Enforce noreload only if it's requested by -N option

* Fri Oct 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-4
- restorecond: check write() and daemon() results
- sepolicy: do not fail when file_contexts.local or .subs do not exist
- sepolicy: remove stray space in section "SEE ALSO"
- sepolicy: fix misspelling of _ra_content_t suffix
- gui: port to Python 3 by migrating to PyGI
- gui: remove the status bar
- gui: fix parsing of "semodule -lfull" in tab Modules
- gui: delete overridden definition of usersPage.delete()
- Enable listing file_contexts.homedirs (#1409813)
- remove semodule_deps

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.7-3
- Also add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.7-2
- Python 2 binary package renamed to python2-policycoreutils
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Mon Aug 07 2017 Petr Lautrbach <plautrba@redhat.com> - 2.7-1
- Update to upstream release 2017-08-04
- Move DBUS API from -gui to -dbus package

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 2.6-8
- Rebuild with binutils fix for ppc64le (#1475636)

* Fri Jul 28 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-7
- Make 'sepolicy manpage' and 'sepolicy transition' faster
- open_init_pty: restore stdin/stdout to blocking upon exit
- fixfiles: do not dereference link files in tmp
- fixfiles: use a consistent order for options to restorecon
- fixfiles: don't ignore `-F` when run in `-C` mode
- fixfiles: remove bad modes of "relabel" command
- fixfiles: refactor into the `set -u` dialect
- fixfiles: if restorecon aborts, we should too
- fixfiles: usage errors are fatal
- fixfiles: syntax error
- fixfiles: remove two unused variables
- fixfiles: tidy up usage(), manpage synopsis
- fixfiles: deprecate -l option
- fixfiles: move logit call outside of redirected function
- fixfiles: fix logging about R/O filesystems
- fixfiles: clarify exclude_dirs()
- fixfiles: remove (broken) redundant code

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Apr 06 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-5
- semanage: Unify argument handling (#1398987)
- setfiles: set up a logging callback for libselinux
- setfiles: Fix setfiles progress indicator
- setfiles: stdout messages don't need program prefix
- setfiles: don't scramble stdout and stderr together (#1435894)
- restorecond: Decrease loglevel of termination message (#1264505)
- fixfiles should handle path arguments more robustly
- fixfiles: handle unexpected spaces in command
- fixfiles: remove useless use of cat (#1435894)
- semanage: Add checks if a module name is passed in (#1420707)
- semanage: fix export of fcontext socket entries (#1435127)
- selinux-autorelabel: remove incorrect redirection to /dev/null (#1415674)

* Fri Mar 17 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-4
- Fix selinux-polgengui (#1432337)
- sepolicy - fix obtaining domain name in HTMLManPages

* Tue Feb 28 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-3
- Fix several issues in gui and 'sepolicy manpage' (#1416372)

* Thu Feb 23 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-2
- Use %%{__python3} instead of python3

* Mon Feb 20 2017 Petr Lautrbach <plautrba@redhat.com> - 2.6-1.1
- Fix pp crash when processing base module (#1417200)
- Update to upstream release 2016-10-14

* Wed Feb 15 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.5-22
- Rebuild for brp-python-bytecompile

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Kevin Fenzi <kevin@scrye.com> - 2.5-20
- Rebuild for python 3.6

* Thu Dec 01 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-19
- seobject: Handle python error returns correctly
- policycoreutils/sepolicy/gui: fix current selinux state radiobutton
- policycoreutils: semodule_package: do not fail with an empty fc file

* Tue Nov 22 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-18
- Update translations
- Fix fcontextPage editing features (#1344842)

* Mon Oct 03 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-17
- sandbox: Use dbus-run-session instead of dbus-launch when available
- hll/pp: Change warning for module name not matching filename to match new behavior
- Remove LDFLAGS from CFLAGS
- sandbox: create a new session for sandboxed processes
- sandbox: do not try to setup directories without -X or -M
- sandbox: do not run xmodmap in a new X session
- sandbox: Use GObject introspection binding instead of pygtk2
- sandbox: fix file labels on copied files
- sandbox: tests - close stdout of p
- sandbox: tests - use sandbox from cwd
- audit2allow: tests should use local copy not system
- audit2allow: fix audit2why import from seobject
- audit2allow: remove audit2why so that it gets symlinked
- semanage: fix man page and help message for import option
- semanage: fix error message for fcontext -m
- semanage: Fix semanage fcontext -D
- semanage: Correct fcontext auditing
- semanage: Default serange to "s0" for port modify
- semanage: Use socket.getprotobyname for protocol
- semanage: fix modify action in node and interface
- fixfiles: Pass -n to restorecon for fixfiles check
- sepolicy: Check get_rpm_nvr_list() return value
- Don't use subprocess.getstatusoutput() in Python 2 code
- semanage: Add auditing of changes in records
- Remove unused 'q' from semodule getopt string

* Mon Aug 01 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-16
- Remove unused autoconf files from po/
- Remove duplicate, empty translation files
- Rebuilt with libsepol-2.5-9, libselinux-2.5-11, libsemanage-2.5-7

* Thu Jul 21 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-15
- Fix sandbox -X issue related to python3 (#1358138)

* Wed Jul 20 2016 Richard W.M. Jones <rjones@redhat.com> - 2.5-14
- Use generator approach to fix autorelabel

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5-13
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 14 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-12
- open_init_pty: Do not error on EINTR
- Fix [-s STORE] typos in semanage
- Update sandbox types in sandbox manual
- Update translations

* Mon Jun 27 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-11
- Convert sandbox to gtk-3 using pygi-convert.sh (#1343166)

* Thu Jun 23 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-10
- Fix typos in semanage manpages
- Fix the documentation of -l,--list for semodule
- Minor fix in a French translation
- Fix the extract example in semodule.8
- Update sandbox.8 man page
- Remove typos from chcat --help
- sepolgen: Remove additional files when cleaning

* Wed May 11 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-9
- Fix multiple spelling errors
- Rebuild with libsepol-2.5-6

* Mon May 02 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-8
- Rebuilt with libsepol-2.5-5

* Fri Apr 29 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-7
- hll/pp: Warn if module name different than output filename

* Mon Apr 25 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-6
- Ship selinux-autorelabel utility and systemd unit files (#1328825)

* Fri Apr 08 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-5
- sepolgen: Add support for TYPEBOUNDS statement in INTERFACE policy files (#1319338)

* Fri Mar 18 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-4
- Add documentation for MCS separated domains
- Move svirt man page out of libvirt into its own

* Thu Mar 17 2016 Petr Lautrbach <plautrba@redhat.com> - 2.5-3
- policycoreutils: use python3 in chcat(#1318408)

* Sat Mar 05 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-2
- policycoreutils/sepolicy: selinux_server.py to use GLib instead of gobject
- policycoreutils-gui requires python-slip-dbus (#1314685)

* Tue Feb 23 2016 Petr Lautrbach <plautrba@redhat.com> 2.5-1
- Update to upstream release 2016-02-23

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 14 2015 Petr Lautrbach <plautrba@redhat.com> - 2.4-20
- Fix 'semanage permissive -l' subcommand (#1286325)
- Several 'sepolicy gui' fixes (#1281309,#1281309,#1282382)

* Tue Nov 17 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-19
- Require at least one argument for 'semanage permissive -d' (#1255676)

* Mon Nov 16 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-18
- Improve sepolicy command line interface
- Fix sandbox to propagate specified MCS/MLS Security Level. (#1279006)
- Fix 'audit2allow -R' (#1280418)

* Thu Nov 12 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-17
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 09 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-16
- policycoreutils-gui needs policycoreutils-python (#1279046)

* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 2.4-15
- Rebuilt for Python3.5 rebuild

* Thu Oct 08 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-14
- Revert the attempt to port -gui to GTK 3 (#1269328, #1266059)

* Fri Oct 02 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-13
- newrole: Set keepcaps around setresuid calls
- newrole: Open stdin as read/write

* Fri Sep 04 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-12
- Fix several semanage issue (#1247714)
- Decode output from subprocess, if error occurred (#1247039)

* Wed Sep 02 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-11
- audit2allow, audit2why - ignore setlocale errors (#1208529)

* Fri Aug 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-10
- Port sandbox to GTK 3 and fix issue with Xephyr

* Thu Aug 13 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-9
- Fix another python3 issues mainly in sepolicy (#1247039,#1247575,#1251713)

* Thu Aug 06 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-8
- Fix multiple python3 issues in sepolgen (#1249388,#1247575,#1247564)

* Mon Jul 27 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-7
- policycoreutils-python3 depends on python-IPy-python3

* Mon Jul 27 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-6
- policycoreutils-devel depends on policycoreutils-python-utils (#1246818)

* Fri Jul 24 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-5
- Move python utilities from -python to -python-utilities
- All scripts originally from policycoreutils-python use python 3 now

* Fri Jul 24 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-4
- policycoreutils: semanage: fix moduleRecords deleteall method

* Thu Jul 23 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-3
- Improve compatibility with python 3
- Add sepolgen module to python3 package

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-2
- Add Python3 support for sepolgen module (#1125208,#1125209)

* Tue Jul 21 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-1.1
- Update to 2.4 release

* Wed Jul 15 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.7
- Fix typo in semanage args for minimum policy store

* Fri Jul 03 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.6
- policycoreutils: semanage: update to new source policy infrastructure
- semanage: move permissive module creation to /tmp

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 06 2015 Petr Lautrbach <plautrba@redhat.com> 2.3-17
- setfiles/restorecon: fix -r/-R option (#1211721)

* Mon Apr 13 2015 Petr Lautrbach <plautrba@redhat.com> 2.4-0.4
- Update to upstream 2.4

* Tue Feb 24 2015 Petr Lautrbach <plautrba@redhat.com> 2.3-16
- Temporary removed Requires:audit-libs-python from policycoreutils-python3 subpackage (#1195139)
- Simplication of sepolicy-manpage web functionality (#1193552)

* Mon Feb 02 2015 Petr Lautrbach <plautrba@redhat.com> 2.3-15
- We need to cover file_context.XXX.homedir to have fixfiles with exclude_dirs working correctly
- Use dnf instead of yum (#1156547)

* Tue Nov 18 2014 Dan Walsh <dwalsh@redhat.com> - 2.3-14
- Audit2allow will check for mislabeled files, and tells user to fix the label.
- Also checks for basefiles and suggests creating a different label.
- Patch from Ryan Hallisey

* Wed Nov 5 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.3-13
- Switch back to yum. Need additional fixes to make it working correctly.

* Wed Nov 5 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.3-12
- Switch over to dnf from yum

* Tue Sep 23 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.3-11
- Improvements to audit2allow from rhallise@redhat.com
    * Check for mislabeled files.
    * Check for base file use and
    * Suggest writable files as alternatives

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 4 2014  Dan Walsh <dwalsh@redhat.com> - 2.3-9
- Remove build requires for openbox, not needed

* Thu Jul 31 2014 Tom Callaway <spot@fedoraproject.org> - 2.3-8
- fix license handling

* Wed Jul 23 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.3-7
- Examples are no longer in the main semanage man page (#1084390)
- Add support for Fedora22 man pages. We need to fix it to not using hardcoding.
- Print usage for all mutually exclusive options.
- Fix selinux man page to refer seinfo and sesearch tools.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue May 20 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.3-4
- Fix setfiles to work correctly if -r option is defined

* Fri May 16 2014 Dan Walsh <dwalsh@redhat.com> - 2.3-3
- Update Miroslav Grepl Patches
  * If there is no executable we don't want to print a part of STANDARD FILE CON
  * Add-manpages-for-typealiased-types
  * Make fixfiles_exclude_dirs working if there is a substituion for the given d

* Mon May 12 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.3-2
- If there is no executable we don't want to print a part of STANDARD FILE CONTEXT

* Tue May 6 2014 Dan Walsh <dwalsh@redhat.com> - 2.3-1
- Update to upstream 
        * Add -P semodule option to man page from Dan Walsh.
        * selinux_current_policy_path will return none on a disabled SELinux system from Dan Walsh.
        * Add new icons for sepolicy gui from Dan Walsh.
        * Only return writeable files that are enabled from Dan Walsh.
        * Add domain to short list of domains, when -t and -d from Dan Walsh.
        * Fix up desktop files to match current standards from Dan Walsh.
        * Add support to return sensitivities and categories for python from Dan Walsh.
        * Cleanup whitespace from Dan Walsh.
        * Add message to tell user to install sandbox policy from Dan Walsh.
        * Add systemd unit file for mcstrans from Laurent Bigonville.
        * Improve restorecond systemd unit file from Laurent Bigonville.
        * Minor man pages improvements from Laurent Bigonville.

* Tue May 6 2014 Miroslav Grepl <mgreplh@redhat.com> - 2.2.5-15
- Apply patch to use setcon in seunshare from luto@mit.edu

* Wed Apr 30 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-14
- Remove requirement for systemd-units 

* Fri Apr 25 2014 Miroslav Grepl <mgreplh@redhat.com> - 2.2.5-13
- Fix previous Fix-STANDARD_FILE_CONTEXT patch to exclude if non_exec does not exist

* Thu Apr 24 2014 Miroslav Grepl <mgreplh@redhat.com> - 2.2.5-12
- Add policycoreutils-rhat-revert.patch to revert the last two commits to make build working
- Add 0001-Fix-STANDARD_FILE_CONTEXT-section-in-man-pages patch

* Tue Apr 1 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-11
- Update Translations

* Thu Mar 27 2014 Miroslav Grepl <mgrepl@redhat.com> - 2.2.5-10
- Add support for Fedora21 html manpage structure
- Fix broken dependencies to require only usermode-gtk

* Wed Mar 26 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-9
- mgrepl [PATCH] Deleteall user customization fails if there is a user used
- for the default login. We do not want to fail on it and continue to delete
- customizations for users which are not used for default login.

* Mon Mar 24 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-8
- Update Translations
- Make selinux-policy build working also on another architectures related to s
- Miroslav grepl patch to fix the creation of man pages on different architectures.
- Add ability to list the actual active modules
- Fix spelling mistake on sesearch in generate man pages.

* Fri Feb 14 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-7
- Allow manpages to be built on aarch64

* Fri Feb 14 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-6
- Don't be verbose in fixfiles if there is not tty

* Thu Feb 13 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-5
- Yum should only be required for policycoreutils-devel

* Tue Jan 21 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-4
- Update translations

* Thu Jan 16 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-3
- Add Miroslav patch to
- Fix previously_modified_initialize() to show modified changes properly for all selections

* Wed Jan 8 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-2
- Do not require /usr/share/selinux/devel/Makefile to build permissive domains

* Mon Jan 6 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.5-1
- Update to upstream 
        * Ignore selevel/serange if MLS is disabled from Sven Vermeulen.

* Fri Jan 3 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.4-8
- Update Tranlations
- Patch from Yuri Chornoivan to fix typos

* Fri Jan 3 2014 Dan Walsh <dwalsh@redhat.com> - 2.2.4-7
- Fixes Customized booleans causing a crash of the sepolicy gui

* Fri Dec 20 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.4-6
- Fix sepolicy gui selection for advanced screen
- Update Translations
- Move requires checkpolicy requirement into policycoreutils-python

* Mon Dec 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.4-5
- Fix semanage man page description of import command
- Fix policy kit file to allow changing to permissive mode

* Mon Dec 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.4-4
- Fix broken dependencies.

* Fri Dec 13 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.4-3
- Break out python3 code into separate package

* Fri Dec 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.4-2
- Add mgrepl patch
-   ptrace should be a part of deny_ptrace boolean in TEMPLATETYPE_admin

* Tue Dec 3 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.4-1
- Update to upstream 
        * Revert automatic setting of serange and seuser in seobject; was breaking non-MLS systems.
- Add patches for sepolicy gui from mgrepl to
  Fix advanced_item_button_push() to allow to select an application in advanced search menu
  Fix previously_modified_initialize() to show modified changes properly for all selections

* Fri Nov 22 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.3-1
- Update to upstream 
        * Apply polkit check on all dbus interfaces and restrict to active user from Dan Walsh.
        * Fix typo in sepolicy gui dbus.relabel_on_boot call from Dan Walsh.
- Apply Miroslav Grepl patch to fix TEMPLATETYPE_domtrans description in sepolicy generate

* Wed Nov 20 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.2-2
- Fix selinux-polgengui, get_all_modules call

* Fri Nov 15 2013 Dan Walsh <dwalsh@redhat.com> - 2.2.2-1
- Speed up startup time of sepolicy gui
- Clean up ports screen to only show enabled ports.
- Update to upstream 
        * Remove import policycoreutils.default_encoding_utf8 from semanage from Dan Walsh.
        * Make yum/extract_rpms optional for sepolicy generate from Dan Walsh.
        * Add test suite for audit2allow and sepolgen-ifgen from Dan Walsh.

* Thu Oct 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.2-2
- Shift around some of the files to more appropriate packages.
        * semodule_* packages are required for devel.

* Thu Oct 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.2-1
- Update to upstream 
        * Properly build the swig exception file from Laurent Bigonville.
        * Fix man pages from Laurent Bigonville.
        * Support overriding PATH and INITDIR in Makefile from Laurent Bigonville.
        * Fix LDFLAGS usage from Laurent Bigonville.
        * Fix init_policy warning from Laurent Bigonville.
        * Fix semanage logging from Laurent Bigonville.
        * Open newrole stdin as read/write from Sven Vermeulen.
        * Fix sepolicy transition from Sven Vermeulen.
        * Support overriding CFLAGS from Simon Ruderich.
        * Create correct man directory for run_init from Russell Coker.
        * restorecon GLOB_BRACE change from Michal Trunecka.
        * Extend audit2why to report additional constraint information.
        * Catch IOError errors within audit2allow from Dan Walsh.
        * semanage export/import fixes from Dan Walsh.
        * Improve setfiles progress reporting from Dan Walsh.
        * Document setfiles -o option in usage from Dan Walsh.
        * Change setfiles to always return -1 on failure from Dan Walsh.
        * Improve setsebool error r eporting from Dan Walsh.
        * Major overhaul of gui from Dan Walsh.
        * Fix sepolicy handling of non-MLS policy from Dan Walsh.
        * Support returning type aliases from Dan Walsh.
        * Add sepolicy tests from Dan Walsh.
        * Add org.selinux.config.policy from Dan Walsh.
        * Improve range and user input checking by semanage from Dan Walsh.
        * Prevent source or target arguments that end with / for substitutions from Dan Walsh.
        * Allow use of <<none>> for semanage fcontext from Dan Walsh.
        * Report customized user levels from Dan Walsh.
        * Support deleteall for restoring disabled modules from Dan Walsh.
        * Improve semanage error reporting from Dan Walsh.
        * Only list disabled modules for module locallist from Dan Walsh.
        * Fix logging from Dan Walsh.
        * Define new constants for file type character codes from Dan Walsh.
        * Improve bash completions from Dan Walsh.
        * Convert semanage to argparse from Dan Walsh (originally by Dave Quigley).
        * Add semanage tests from Dan Walsh.
        * Split semanage man pages from Dan Walsh.
        * Move bash completion scripts from Dan Walsh.
        * Replace genhomedircon script with a link to semodule from Dan Walsh.
        * Fix fixfiles from Dan Walsh.
        * Add support for systemd service for restorecon from Dan Walsh.
        * Spelling corrections from Dan Walsh.
        * Improve sandbox support for home dir symlinks and file caps from Dan Walsh.
        * Switch sandbox to openbox window manager from Dan Walsh.
        * Coalesce audit2why and audit2allow from Dan Walsh.
        * Change audit2allow to append to output file from Dan Walsh.
        * Update translations from Dan Walsh.
        * Change audit2why to use selinux_current_policy_path from Dan Walsh.

* Fri Oct 25 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-89
- Fix handling of man pages.

* Wed Oct 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-88
- Cleanup errors found by pychecker
- Apply patch from Michal Trunecka to allow restorecon to handle {} in globs

* Fri Oct 11 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-87
- sepolicy gui
  - mgrepl fixes for users and login
- Update Translations.

* Fri Oct 11 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-86
- sepolicy gui
  - mgrepl added delete screens for users and login
  - Fix lots of bugs.
- Update Translations.

* Fri Oct 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-85
- Fixes for fixfiles
  * exclude_from_dirs should apply to all types of restorecon calls
  * fixfiles check now works
  * exit with the correct status
- semanage no longer import selinux

* Wed Oct 2 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-84
- Fixes for sepolicy gui
- Fix setsebool to return 0 on success
- Update Po

* Mon Sep 30 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-83
- Fix sizes of help screens in sepolicy gui

* Sat Sep 28 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-82
- Improvements to sepolicy gui
  - Add more help information
  - Cleanup code
  - Add deny_ptrace on lockdown screen
  - Make unconfined/permissivedomains lockdown work
  - Add more support for file equivalency

* Wed Sep 18 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-81
- Add back in the help png files
- Begin Adding support for file equivalency.

* Wed Sep 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-80
- Random fixes for sepolicy gui
  * Do not prompt for password until you make a change
  * Add user mappings and selinux users page
  * lots of code cleanup
- Verify homedir is owned by user before mounting over it with seunshare
- Fix fixfiles to handle Relabel properly
- Fix semanage fcontext -e / command to allow "/"

* Wed Sep 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-79
- Add Miroslav Grepl setsebool patch to give better error message on bad boolean names
- Additional help screens for sepolicy gui

* Tue Sep 3 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-78
- Random fixes for sepolicy gui
- Update Translations

* Fri Aug 30 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-77
- Add help screens for each page
- Fixes for system page

* Mon Aug 26 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-76
- Add Miroslav Grepl Patch to handle semanage -i and semanage -o better
- Update Translations

* Thu Aug 15 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-75
- Update sepolicy gui code, cleanups and add file transition tab
- Fix semanage fcontext -a --ftype code to work.

* Wed Aug 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-74
- If policy is not installed get_bools should not crash

* Wed Aug 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-73
- Fix doc versioning

* Tue Aug 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-72
- Update sepolicy gui code, cleanups and add file transition tab
- Fix semanage argparse problems

* Fri Aug 2 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-71
- Update sepolicy gui code, adding dbus calls
- Update Translations

* Fri Jul 26 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-70
- Fix semanage argparse bugs
- Update Translations
- Add test suite for semanage command lines

* Wed Jul 24 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-69
- Fix semanage argparse bugs

* Tue Jul 23 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-68
- Fix bugs introduced by previous patch.  semanage port
- Update Translations
- Add test suite for sepolicy command lines

* Fri Jul 19 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-67
- Fix bugs introduced by previous patch.  semanage port
- Update Translations

* Wed Jul 17 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-66
- Rewrite argparse code in semanage and fix reload problem.

* Tue Jul 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-65
- Do not generate shell script or spec file for sepolicy generate --newtype
- Update translations
- Fix sepolicy generate --admin_user man page again
- Fix setsebool to print less verbose error messages by default, add -V for ve

* Mon Jul 15 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-64
- Move audit2allow and audit2why back into -python package

* Wed Jul 10 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-63
- Update sepolicy gui.
- Error out of you call sepolicy gui without policycoreutils-gui package installed
- Fix semanage login -d command
- Update Translations

* Wed Jul 10 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-62
- Update sepolicy gui.

* Fri Jul 5 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-61
- Add Ryan Hallisey sepolicy gui.
- Update Translations

* Mon Jun 24 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-60
- Fix semanage module error handling

* Sun Jun 23 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-59
- Add back default exception handling for errors, which argparse rewrite removed.

* Fri Jun 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-58
- Fix generation of booleans in man pages

* Fri Jun 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-57
- Remove requires for systemd-sysv
- Move systemd-units require to restorecond section
- Update Tranlasions
- More sepolicy interfaces for gui
- Cleanup man pages for sepolicy generate

* Wed Jun 19 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-56
- Fix semanage export/import commands
- Fix semange module command
- Remove --version option from sandbox

* Tue Jun 18 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-55
- Add man page doc for --role and bash complestion support for sepolicy --role

* Tue Jun 18 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-54
- Make fcdict return a dictionary of dictionaries
- Fix for sepolicy manpage

* Mon Jun 17 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-53
- Add new man pages for each semanage subsection

* Mon Jun 17 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-52
- Fix handling of sepolicy network sorting.
- Additional interfaces needed for sepolicy gui

* Thu Jun 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-51
- Fix handling of semanage args

* Thu Jun 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-50
- Fix sepolicy generate --confined_admin to generate tunables
- Add new interface to generate entrypoints for use with new gui

* Wed Jun 5 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-49
- Fix handing of semanage with no args

* Tue Jun 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-48
- Fix audit2allow -o to open file for append
- Fix the name of the spec file generated in the build script

* Fri May 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-47
- Fix mgrepl patch to support all semanage command parsing

* Sun May 26 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-46
- Fix the name of the spec file generated in the build script
- Add mgrepl patch to support argparse for semanage command parsing

* Tue May 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-45
- Fix sandbox to always use sandbox_file_t, so generated policy will work.
- Update Translations

* Thu May 16 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-44
- Fix sepolicy-generate man page to clear up options/policy type
- Add Miroslav Grepl to not generate man page when doing
  sepolicy generate --customize
- Add support for executing semanage user within spec file
- Fix generation of confined admin domains, to handle booleans properly.

* Tue May 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-43
- Need to handle gziped policy.xml as well as not compressed.

* Tue May 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-42
- Add support for Xephyr -resizable, so sandbox can now resize window
- Add support for compressed policy.xml
- Miroslav Grepl patch to allow sepolicy interface on individual interface fil
- Also add capability to test interfaces for correctness.

* Mon May 13 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-41
- Apply patches from Sven Vermeulen for sepolgen to fix typos.

* Mon May 13 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-40
- Only require selinux-policy-devel for policycoreutils-devel, this will shrink the size of the livecd.

* Sun May 12 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-39
- Run sepolgen-ifgen in audit2allow and sepolicy generate, if needed, first time
- Add  Sven Vermeulen  patches to cleanup man pages

* Fri May 10 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-38
- No longer run sepolgen-ifgen at install time.
- Run sepolgen-ifgen in audit2allow and sepolicy generate, if needed.
- Update Translations

* Mon Apr 22 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-37
- Fix exceptionion hanling in audit2allow -o
- Generate Man pages for everydomain, not just ones with exec_t entrypoints
- sepolicy comunicate should return ValueError not TypeError
- Trim header line in sepolicy manpage to use less space
- Add missing options to restorecon man page

* Thu Apr 11 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-36
- Raise proper Exception on sepolicy communicate with invalid value

* Wed Apr 10 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-35
- Update translations
- Add patch by Miroslav Grepl to add compile test for sepolicy interface command.

* Tue Apr 9 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-34
- Update translations
- Add patch inspired by Miroslav Grepl to add extended information for sepolicy interface command.

* Mon Apr 8 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-33
- Update translations
- Add missing man pages and fixup existing man pages

* Wed Apr 3 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-32
- Move sepolicy to policycoreutils-devel pacage, since most of it is used for devel
- Apply Miroslav Grepl Patches for sepolicy
-- Fix generate mutually groups option handling
-- EUSER is used for existing policy
-- customize options can be used together with admin_domain option
-- Fix manpage.py to generate correct man pages for SELinux users
-- Fix policy *.te file generated by customize+writepaths options
-- Fix install script for confined_admin option

* Mon Apr 1 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-31
- Add post install scripts for gui to make sure Icon Cache is refreshed.
- Fix grammar issue in secon man page
- Update Translations

* Thu Mar 28 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-30
- Add buildrequires for OpenBox to prevent me from accidently building into RHEL7
- Add support for returning alias data to sepolicy.info python bindings

* Wed Mar 27 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-28
- Fix audit2allow output to better align analysys with the allow rules
- Apply Miroslav Grepl patch to clean up sepolicy generate usage
- Apply Miroslav Grepl patch to fixupt handing of admin_user generation
- Update Tranlslations

* Wed Mar 27 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-27
- Allow semanage fcontext -a -t "<<none>>" ...  to work

* Mon Mar 25 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-26
- Can not unshare IPC in sandbox, since it blows up Xephyr
- Remove bogus error message sandbox about reseting setfsuid

* Thu Mar 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-25
- Fix sepolicy generate --customize to generate policy with -w commands

* Thu Mar 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-24
- sepolgen-ifgen needs to handle filename transition rules containing ":"

* Tue Mar 19 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-23
- sepolicy manpage:
-   use nroff instead of man2html
-   Remove checking for name of person who created the man page
- audit2allow
-   Fix output to show the level that is different.

* Thu Mar 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-22
- Fix newrole to not drop capabilities from the bounding set.
- Stop dropping capabilities from its children.
- Add better error messages.
- Change location of bash_completion files to /usr/share/bash-completion/compl

* Mon Mar 11 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-21
- sepolicy generate should look for booleans that effect equivalence names, and add them to the man page

* Thu Mar 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-20
- Mention creation of permissive domains in sepolicy generate man page
- Change sepolicy manpage to use shortname with an "_" to stop accidently grabbing unrelated types for a domain.
- Fix audit2allow to show better information on constraint violations.

* Wed Mar 6 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-19
- Have restorecon exit -1 on errors for consistancy.

* Tue Mar 5 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-18
- Need to provide a value to semanage boolean -m

* Mon Mar 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-17
- Fix cut and paste errors for sepolicy network command

* Fri Mar 1 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-16
- Fix sepoicy interface to work properly

* Thu Feb 28 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-15
- Fix fixfiles to use exclude_dirs on fixfiles restore

* Thu Feb 28 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-14
- Allow users with symlinked homedirs to work. call realpath on homedir
- Fix sepolicy reorganization of helper functions.

* Sun Feb 24 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-13
- Update trans
- Fix sepolicy reorganization of helper functions.

* Sun Feb 24 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 2.1.14-13
- remove vendor tag from desktop file. https://fedorahosted.org/fpc/ticket/247
- clean up spec to follow current guidelines

* Fri Feb 22 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-12
- Do not load interface file by default when sepolicy is called, mov get_all_methods to the sepolicy package

* Fri Feb 22 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-11
- sepolgen-ifgen should use the current policy path if selinux is enabled

* Fri Feb 22 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-10
- Fix sepolicy to be able to work on an SELinux disabled system.
- Needed to be able to build man pages in selinux-policy package

* Thu Feb 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-9
- Add yum to requires of policycoreutils-python since sepolicy requires it.

* Thu Feb 21 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-8
- Sepolixy should not throw an exception on an SELinux disabled machine
- Switch from using console app to using pkexec, so we will work better
with policykit.
- Add missing import to fix system-config-selinux startup
- Add comment to pamd files about pam_rootok.so
- Fix sepolicy generate to not comment out the first line

* Wed Feb 20 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-7
- Add --root/-r flag to sepolicy manpage,
- This allows us to generate man pages on the fly in the selinux-policy build

* Mon Feb 18 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-6
- Fix newrole to retain cap_audit_write when compiled with namespace, also
do not drop capabilities when run as root.

* Thu Feb 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-5
- Fix man page generation and public_content description

* Thu Feb 14 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-4
- Revert some changes which are causing the wrong policy version file to be created
- Switch sandbox to start using openbox rather then matchbox
- Make sepolgen a symlink to sepolicy
- update translations

* Wed Feb 13 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-3
- Fix empty system-config-selinux.png, again

* Tue Feb 12 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-2
- Fix empty system-config-selinux.png

* Thu Feb 7 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.14-1
- Update to upstream
        * setfiles: estimate percent progress
        * load_policy: make link at the destination directory
        * Rebuild polgen.glade with glade-3
        * sepolicy: new command to unite small utilities
        * sepolicy: Update Makefiles and po files
        * sandbox: use sepolicy to look for sandbox_t
        * gui: switch to use sepolicy
        * gui: sepolgen: use sepolicy to generate
        * semanage: use sepolicy for boolean dictionary
        * add po file configuration information
        * po: stop running update-po on all
        * semanage: seobject verify policy types before allowing you to assign them.
        * gui: Start using Popen, instead of os.spawnl
        * sandbox: Copy /var/tmp to /tmp as they are the same inside
        * qualifier to shred content
        * semanage: Fix handling of boolean_sub names when using the -F flag
        * semanage: man: roles instead of role
        * gui: system-config-selinux: Catch no DISPLAY= error
        * setfiles: print error if no default label found
        * semanage: list logins file entries in semanage login -l
        * semanage: good error message is sepolgen python module missing
        * gui: system-config-selinux: do not use lokkit
        * secon: add support for setrans color information in prompt output
        * restorecond: remove /etc/mtab from default list
        * gui: If you are not able to read enforcemode set it to False
        * genhomedircon: regenerate genhomedircon more often
        * restorecond: Add /etc/udpatedb.conf to restorecond.conf
        * genhomedircon generation to allow spec file to pass in SEMODULE_PATH
        * fixfiles: relabel only after specific date
        * po: update translations
        * sandbox: seunshare: do not reassign realloc value
        * seunshare: do checking on setfsuid
        * sestatus: rewrite to shut up coverity

* Thu Jan 31 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-58
- Reorginize sepolicy so all get_all functions are in main module
- Add -B capability to fixfiles onboot and fixfiles restore, basically searches for all files created since the last boot.

* Fri Jan 25 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-57
- Update to latest patches from eparis/Upstream
- fixfiles onboot will write any flags handed to it to /.autorelabel.
-   * Patch sent to initscripts to have fedora-autorelabel pass flags back to fixfiles restore
-   * This should allow fixfiles -F onboot, to force a hard relabel.
- Add -p to show progress on full relabel.

* Tue Jan 15 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-56
-  Additional changes for bash completsion and generate man page to match the w
-  Add newtype as a new qualifier to sepolicy generate.  This new mechanism wil
-  a policy write to generate types after the initial policy has been written a
-  will autogenerate all of the interfaces.
-  I also added a -w options to allow policy writers from the command line to s
-  the writable directories of files.
-
-  Modify network.py to include interface definitions for newly created port type
-  Standardize of te_types just like all of the other templates.
-  Change permissive domains creation to raise exception if sepolgen is not ins
-  get_te_results no longer needs or uses the opts parameter.
-  The compliler was complaining so I just removed the option.
-  Start returning analysis data for audit2allow

* Tue Jan 15 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-55
- Update Translations
- Fix handling of semanage generate --cgi -n MODULE PATHTO/CGI
-   This fixes the spec file and script file getting wrong names for modules and types.

* Wed Jan 9 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-54
- Additional patch from Miroslav to handle role attributes

* Wed Jan 9 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-53
- Update with Miroslav patch to handle role attributes
- Update Translations
- import sepolicy will only throw exception on missing policy iff selinux is enabled

* Sat Jan 5 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-52
- Update to latest patches from eparis/Upstream
-    secon: add support for setrans color information in prompt output
- Update translations

* Fri Jan 4 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-51
- Update translations
- Fix sepolicy booleans to handle autogenerated booleans descriptions
- Cleanups of sepolicy manpage
- Fix crash on git_shell man page generation

* Thu Jan 3 2013 Dan Walsh <dwalsh@redhat.com> - 2.1.12-50
- Update translations
- update sepolicy manpage to generate fcontext equivalence data and to list
default file context paths.
- Add ability to generate policy for confined admins and domains like puppet.

* Thu Dec 20 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-49
- Fix semanage permissive , this time with the patch.
- Update translations

* Wed Dec 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-48
- Fix semanage permissive
- Change to use correct gtk forward button
- Update po

* Mon Dec 17 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-47
- Move audit2why to -devel package

* Mon Dec 17 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-46
- sepolicy transition was blowing up. Also cleanup output when only source is specified.
- sepolicy generate should allow policy modules names that include - or _

* Mon Dec 10 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-45
- Apply patch from Miroslav to display proper range description in man pages g
- Should print warning on missing default label when run in recusive mode iff
- Remove extra -R description, and fix recursive description

* Thu Dec 6 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-44
- Additional fixes for disabled SELinux Box
- system-config-selinux no longer relies on lokkit for /etc/selinux/config

* Thu Dec 6 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-43
- sepolicy should failover to installed policy file on a disabled SELinux box, if it exists.

* Wed Dec 5 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-42
- Update Translations
- sepolicy network -d needs to accept multiple domains

* Fri Nov 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-41
- Add --path as a parameter to sepolicy generate
- Print warning message if program does not exists when generating policy, and do not attempt to run nm command
- Fix sepolicy generate -T to not take an argument, and supress the help message
- Since this is really just a testing tool

* Fri Nov 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-40
- Fix sepolicy communicate to handle invalid input

* Thu Nov 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-39
- Fix sepolicy network -p to handle high ports

* Thu Nov 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-38
- Fix handling of manpages without entrypoints, nsswitch domains
- Update Translations

* Wed Nov 28 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-37
- Move sepogen python bindings back into policycoreutils-python out of -devel, since sepolicy is using the

* Tue Nov 27 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-36
- Fix sepolicy/__init__.py to handle _()

* Wed Nov 21 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-35
- Add Miroslav Grepl patch to create etc_rw_t sock files policy

* Fri Nov 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-34
- Fix semanage to work without policycoreutils-devel installed
- Update translations

* Tue Nov 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-33
- Fix semanage login -l to list contents of /etc/selinux/POLICY/logins directory

* Tue Nov 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-32
- Fix booleansPage not showing booleans
- Fix audit2allow -b

* Tue Nov 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-31
- Fix sepolicy booleans again
- Fix man page

* Mon Nov 12 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-30
- Move policy generation tools into policycoreutils-devel

* Mon Nov 12 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-29
- Document and fix sepolicy booleans
- Update Translations
- Fix several spelling mistakes

* Wed Nov 7 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-27
- Only report restorecon warning for missing default label, if not running
recusively
- Update translations

* Mon Nov 5 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-26
- Fix semanage booleans -l, move more boolean_dict handling into sepolicy
- Update translations
- Fixup sepolicy generate to discover /var/log, /var/run and /var/lib directories if they match the name
- Fix kill function call should indicate signal_perms not kill capability
- Error out cleanly in system-config-selinux, if it can not contact XServer

* Mon Nov 5 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-25
- Remove run_init, no longer needed with systemd.
- Fix sepolicy generate to not include subdirs in generated fcontext file.  (mgrepl patch)

* Sat Nov 3 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-24
- Fix manpage to generate proper man pages for alternate policy,
basically allow me to build RHEL6 man pages on a Fedora 18 box, as long as
I pull the policy, policy.xml and file_contexts and file_contexts.homedir

* Thu Nov 1 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-23
- Fix some build problems in sepolicy manpage and sepolicy transition

* Tue Oct 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-22
- Add alias man pages to sepolicy manpage

* Mon Oct 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-21
- Redesign sepolicy to only read the policy file once, not for every call

* Mon Oct 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-20
- Fixes to sepolicy transition, allow it to list all transitions from a domain

* Sat Oct 27 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-19
- Change sepolicy python bindings to have python pick policy file, fixes weird memory problems in sepolicy network

* Fri Oct 26 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-18
- Allow sepolicy to specify the policy to generate content from

* Thu Oct 25 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-17
- Fix semanage boolean -F to handle boolean subs

* Thu Oct 25 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-16
- Add Miroslav Grepl patch to generate html man pages
- Update Translations
- Add option to sandbox to shred files before deleting

* Mon Oct 22 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-15
- Add Requires(post) PKGNAME to sepolicy generate /usr/bin/pkg

* Fri Oct 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-14
- Add role_allow to sepolicy.search python bindings, this allows us to remove last requirement for setools-cmdline in gui tools.
- Fix man page generator.

* Wed Oct 17 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-13
- Remove dwalsh@redhat.com from man pages
- Fix spec file for sepolicy generate

* Wed Oct 17 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-12
- Add missing spec.py from templates directory needed for sepolicy generate
- Add /var/tmp as collection point for sandbox apps.

* Tue Oct 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-11
- Handle audit2allow -b in foreign locales

* Tue Oct 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-10
- Update sepolicy generate with patch to create spec file and man page.
- Patch initiated by Miroslav Grepl

* Wed Oct 10 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-9
- Fix semanage to verify that types are appropriate for commands.
  * Patch initiated by mgrepl
  * Fixes problem of specifying non file_types for fcontext, or not port_types for semanage port

* Tue Oct 9 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-8
- Fix typo in preunstall line for restorecond
- Add mgrepl patch to consolidate file context generated by sepolicy generate

* Mon Oct 8 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-7
- Fix manpage generation, missing import
- Add equiv_dict to get samba booleans into smbd_selinux
- Add proper translations for booleans and remove selinux.tbl

* Sat Oct 6 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-6
- Fix system-config-selinux to use sepolicy.generate instead of sepolgen

* Thu Oct 4 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-5
- Add sepolicy commands, and change tools to use them.

* Tue Sep 25 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-4
- Rebuild without bogus prebuild 64 bit seunshare app

* Sun Sep 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-3
- Allow fixfiles to specify -v, so they can get verbosity rather then progress.
- Fix load_file Makefile to use SBINDIR rather then real OS.
- Fix man pages in setfiles and restorecon to reflect what happens when you relabel the entire OS.

* Sun Sep 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-2
- Use systemd post install scriptlets

* Thu Sep 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.12-1
- Update to upstream
        * genhomedircon: manual page improvements
        * setfiles/restorecon minor improvements
        * run_init: If open_init_pty is not available then just use exec
        * newrole: do not drop capabilities when newrole is run as
        * restorecon: only update type by default
        * scripts: Don't syslog setfiles changes on a fixfiles restore
        * setfiles: do not syslog if no changes
        * Disable user restorecond by default
        * Make restorecon return 0 when a file has changed context
        * setfiles: Fix process_glob error handling
        * semanage: allow enable/disable under -m
        * add .tx to gitignore
        * translations: commit translations from Fedora community
        * po: silence build process
        * gui: Checking in policy to support polgengui and sepolgen.
        * gui: polgen: search for systemd subpackage when generating policy
        * gui: for exploring booleans
        * gui: system-config-selinux gui
        * Add Makefiles to support new gui code
        * gui: remove lockdown wizard
        * return equivalency records in fcontext customized
        * semanage: option to not load new policy into kernel after
        * sandbox: manpage update to describe standard types
        * setsebool: -N should not reload policy on changes
        * semodule: Add -N qualifier to no reload kernel policy
        * gui: polgen: sort selinux types of user controls
        * gui: polgen: follow symlinks and get the real path to
        * gui: Fix missing error function
        * setfiles: return errors when bad paths are given
        * fixfiles: tell restorecon to ignore missing paths
        * setsebool: error when setting multiple options
        * semanage: use boolean subs.
        * sandbox: Make sure Xephyr never listens on tcp ports
        * sepolgen: return and output constraint violation information
        * semanage: skip comments while reading external configuration files
        * restorecond: relabel all mount runtime files in the restorecond example
        * genhomedircon: dynamically create genhomedircon
        * Allow returning of bastard matches
        * sepolgen: return and output constraint violation information
        * audit2allow: one role/type pair per line

* Wed Aug 8 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-6
- Change polgen to generate dbus apps as optional so they can compile on minimal policy system, patch from Miroslav Grepl

* Fri Jul 27 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-5
- Fix sepolgen/audit2allow to handle multiple role/types in avc messages properly

* Thu Jul 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-4
- Fix restorecon to generate a better percentage of completion on restorecon -R /.
- Have audit2allow look at the constaint violation and tell the user whether it
- is because of user,role or level

* Wed Jul 11 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-3
- userapps is generating sandbox code in polgengui

* Thu Jul 5 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-2
- Remove load_policy symbolic link on usrmove systems this breaks the system

* Wed Jul 4 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-1
- Update to upstream
  - policycoreutils
        * restorecond: wrong options should exit with non-zero error code
        * restorecond: Add -h option to get usage command
        * resorecond: user: fix fd leak
        * mcstrans: add -f to run in foreground
        * semanage: fix man page range and level defaults
        * semanage: bash completion for modules should include -a,-m, -d
        * semanage: manpage update for -e
        * semanage: dontaudit off should work
        * semanage: locallist option does not take an argument
        * sepolgen: Make use of setools optional within sepolgen
   - sepolgen
        * Make use of setools optional within sepolgen
        * We need to support files that have a + in them

* Thu May 24 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-18
- Make restorecon exit with an error on a bad path

* Thu May 24 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-17
- Fix setsebool command, handling of = broken.
- Add missing error option in booleansPage

* Sun May 20 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-16
- Fix sepolgen to use realpath on executables handed to it. - Brian Bickford

* Fri May 18 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-15
- Allow stream sock_files to be stored in /tmp and etc_rw_t directories by sepolgen
- Trigger on selinux-policy needs to change to selinux-policy-devel
- Update translations
- Fix semanage dontaudit off/on exception

* Tue May 8 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-12
- Add -N qualifier to semanage, setsebool and semodule to allow you to update
- policy without reloading it into the kernel.

* Thu May 3 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-11
- add some definition to the standard types available for sandboxes

* Tue May 1 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-10
- Remove lockdown wizard

* Mon Apr 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-9
- Fix semanage fcontext -E to extract the equivalance customizations.

* Thu Apr 26 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-8
- Add mgrepl patch to have sepolgen search for -systemd rpm packages

* Tue Apr 24 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-7
- Apply Stef Walter patch for semanage man page

* Mon Apr 23 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-6
- Rebuild to get latest libsepol which fixes the file_name transition problems
- Update translations
- Fix calls to close fd for restorecond

* Fri Apr 13 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-5
- Update translations
- Fix sepolgen to discover unit files in /lib/systemd/

* Tue Apr 3 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-4
- Update translations
- Fix segfault on restorecon

* Tue Apr 3 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-3
- Allow filename transitions to use + in a file name

* Fri Mar 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-2
- Change policycoreutils-python to require selinux-policy-devel package

* Thu Mar 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.11-1
- Update to upstream
  - policycoreutils
        * sandbox: do not propogate inside mounts outside
        * sandbox: Removing sandbox init script, should no longer be necessary
        * restorecond: Stop using deprecated interfaces for g_io
        * semanage: proper auditting of user changes for LSPP
        * semanage: audit message to show what record(s) and item(s) have chaged
        * scripts: Update Makefiles to handle /usrmove
        * mcstrans: Version should have been bumped on last check in
        * seunshare: Only drop caps not the Bounding Set from seunshare
        * Add bash-completion scripts for setsebool and semanage
        * newrole: Use correct capng calls in newrole
        * Fix infinite loop with inotify on 2.6.31 kernels
        * fix ftbfs with hardening flags
        * Only run setfiles if we found read-write filesystems to run it on
        * update .po files
        * remove empty po files
        * do not fail to install if unable to make load_policy lnk file
   - sepolgen
        * Fix dead links to www.nsa.gov/selinux
        * audit.py Dont crash if empty data is passed to sepolgen
        * do not use md5 when calculating hash signatures
        * fix detection of policy loads

* Wed Mar 28 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-30
- Have sepolgen script specify the pp file with the make command.  From mgrepl.

* Wed Mar 21 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-29
- Fix sepolgen handling of unit files.

* Thu Mar 8 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-28
- Require selinux-policy-doc

* Thu Mar 8 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-27
- Fix unit file handling in sepolgen

* Wed Feb 29 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-26
- Add bash_command completion for setsebool/getsebool

* Mon Feb 27 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-25
- Disable restorecond on desktop by default
- Change seunshare to not modify the bounding set

* Mon Feb 20 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-24
- Stop using sandbox init in post install since it no longer exists.

* Thu Feb 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-23
- Change to use new selinux_current_policy_path()

* Wed Feb 15 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-22
- Change to use new selinux_binary_policy_path()
- Add systemd_passwd_agent_exec($1), and systemd_read_fifo_file_passwd_run($1) to templates for _admin interface

* Fri Feb 3 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-21
- On full relabels we will now show a estimated percent complete rather then
just *s.

* Wed Feb 1 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-20
- Add unit_file.py for sepolgen

* Tue Jan 31 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-19
- Change sepolgen to use sha256 instead of md5

* Mon Jan 30 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-18
- Stop syslogging on full restore
- Stop syslogging when restorecon is not changing values

* Fri Jan 27 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-17
- Change semanage to produce proper audit records for Common Criteria
- Cleanup packaging for usrmove

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 2.1.10-16
- fixed load_policy location

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 2.1.10-15
- fixed load_policy location

* Thu Jan 26 2012 Harald Hoyer <harald@redhat.com> 2.1.10-14
- fixed load_policy location

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.1.10-13
- add filesystem guard

* Wed Jan 25 2012 Harald Hoyer <harald@redhat.com> 2.1.10-12
- install everything in /usr
  https://fedoraproject.org/wiki/Features/UsrMove

* Tue Jan 24 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-11
- restorecond fixes:
  Stop using depracated g_io interfaces
  Exit with non zero exit code if wrong options given
  Add -h option

* Thu Jan 19 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-10
- Eliminate not needed Requires

* Wed Jan 18 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-9
- fix sepolgen to not crash on echo "" | audit2allow

* Mon Jan 16 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-8
- Remove sandbox init script, should no longer be necessary

* Sun Jan 15 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-7
- Add unit file support to sepolgen, and cleanup some of the output.

* Mon Jan 9 2012 Dan Walsh <dwalsh@redhat.com> - 2.1.10-5
- Fix English in templates for sepolgen

* Fri Dec 23 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.10-4
- Fix the handling of namespaces in seunshare/sandbox.
- Currently mounting of directories within sandbox is propogating to the
- parent namesspace.

* Thu Dec 22 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.10-3
- Add umount code to seunshare to cleanup left over mounts of /var/tmp

* Wed Dec 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.10-2
- Remove open_init_pty

* Wed Dec 21 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.10-1
-Update to upstream
- sepolgen
        * better analysis of why things broke
- policycoreutils
        * Remove excess whitespace
        * sandbox: Add back in . functions to sandbox.init script
        * Fix Makefile to match other policycoreutils Makefiles
        * semanage: drop unused translation getopt

* Thu Dec 15 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.9-3
- Bump libsepol version requires rebuild

* Wed Dec 7 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.9-2
- Add back accidently dropped patches for semanage

* Tue Dec 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.9-1
- Upgrade to upstream
        * sandbox: move sandbox.conf.5 to just sandbox.5
        * po: Makefile use -p to preserve times to allow multilib simultatious installs
        * of po files
        * sandbox: Allow user to specify the DPI value for X in a sandbox
        * sandbox: make sure the domain launching sandbox has at least 100 categories
        * sandbox: do not try forever to find available category set
        * sandbox: only complain if sandbox unable to launch
        * sandbox: init script run twice is still successful
        * semanage: print local and dristo equiv rules
        * semanage: check file equivalence rules for conflict
        * semanage: Make sure semanage fcontext -l -C prints even if local keys
        * are not defined
        * semanage: change src,dst to target,substitute for equivalency
        * sestatus: Updated sestatus and man pages.
        * Added SELinux config file man page.
        * add clean target to man Makefile

* Wed Nov 30 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-8
- Fix semange fcontext -a  to check for more conflicts on equivalency

* Tue Nov 29 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-7
- Fix dpi handling in sandbox
- Make sure semanage fcontext -l -C prints if only local equiv have changed

* Wed Nov 16 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-6
- Add listing of distribution equivalence class from semanage fcontext -l
- Add checking to semanage fcontext -a to guarantee a file specification will not be masked by an equivalence

* Wed Nov 16 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-5
- Allow ~ as a valid part of a filename in sepolgen

* Fri Nov 11 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-4
- sandbox init script should always return 0
- sandbox command needs to check range of categories and report error if not big enough

* Mon Nov 7 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-3
- Allow user to specify DPI when running sandbox

* Mon Nov 7 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-2
- Add Miroslav patch to return all attributes

* Fri Nov 4 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.8-1
- Upgrade to policycoreutils upstream
        * sandbox: Maintain the LANG environment into the sandbox
        * audit2allow: use audit2why internally
        * fixfiles: label /root but not /var/lib/BackupPC
        * semanage: update local boolean settings is dealing with localstore
        * semanage: missing modify=True
        * semanage: set modified correctly
        * restorecond: make restorecond dbuss-able
        * restorecon: Always check return code on asprintf
        * restorecond: make restorecond -u exit when terminal closes
        * sandbox: introduce package name and language stuff
        * semodule_package: remove semodule_unpackage on clean
        * fix sandbox Makefile to support DESTDIR
        * semanage: Add -o description to the semanage man page
        * make use of the new realpath_not_final function
        * setfiles: close /proc/mounts file when finished
        * semodule: Document semodule -p in man page
        * setfiles: fix use before initialized
        * restorecond: Add .local/share as a directory to watch
- Upgrade to sepolgen upstream
        * Ignore permissive qualifier if found in an interface
        * Return name field in avc data

* Mon Oct 31 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-6
- Rebuild versus newer libsepol

* Fri Oct 28 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-5
- A couple of minor coverity fixes for a potential leaked file descriptor
- An an unchecked return code.
- Add ~/.local/share/* to restorecond_user watches

* Thu Oct 13 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-4
- Have sepolgen return name field in AVC

* Thu Oct 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-3
- restorecond -u needs to watch terminal for exit if run outside of dbus.

* Tue Oct 4 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-2
- Do not drop capabilities if running newrole as root

* Fri Sep 30 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.7-1
-Update to upstream
        * semanage: fix indentation error in seobject

* Thu Sep 29 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-3
- Ignore permissive commands in interfaces

* Thu Sep 29 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-2
- Remove gnome requirement from polgengui

* Mon Sep 19 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.6-1
-Update to upstream
    policycoreutils-2.1.6
        * sepolgen-ifgen: new attr-helper does something
        * audit2allow: use alternate policy file
        * audit2allow: sepolgen-ifgen use the attr helper
        * setfiles: switch from stat to stat64
        * setfiles: Fix potential crash using dereferenced ftsent
        * setfiles: do not wrap * output at 80 characters
        * sandbox: add -Wall and -Werror to makefile
        * sandbox: add sandbox cgroup support
        * sandbox: rewrite /tmp handling
        * sandbox: do not bind mount so much
        * sandbox: add level based kill option
        * sandbox: cntrl-c should kill entire process control group
        * Create a new preserve_tunables flag in sepol_handle_t.
        * semanage: show running and disk setting for booleans
        * semanage: Dont print heading if no items selected
        * sepolgen: audit2allow is mistakakenly not allowing valid module names
        * semanage: Catch RuntimeErrors, that can be generated when SELinux is disabled
        * More files to ignore
        * tree: default make target to all not install
        * sandbox: do not load unused generic init functions
    sepolgen-1.1.2
        * src: sepolgen: add attribute storing infrastructure
        * Change perm-map and add open to try to get better results on
        * look for booleans that might solve problems
        * sepolgen: audit2allow is mistakakenly not allowing valid module names
        * tree: default make target to all not install

* Wed Sep 14 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-6
- Change separator on -L from ; to :

* Thu Sep 8 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-5
- Add back lockdown wizard for booleans using pywebkitgtk

* Wed Sep 7 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-4
- Maintain the LANG environment Variable into the sandbox
- Change restorecon/setfiles to only change type part of the context unless
  -f qualifier is given

* Tue Sep 6 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-3
- Remove lockdown wizard, since gtkhtml2 is no longer supported.

* Fri Sep 2 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-2
- Allow setfiles and restorecon to use labeledprefix to speed up processing
and limit memory.

* Tue Aug 30 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.5-1
-Update to upstream
   * policycoreutils
        * setfiles: Fix process_glob to handle error situations
        * sandbox: Allow seunshare to run as root
        * sandbox: trap sigterm to make sure sandbox
        * sandbox: pass DPI from the desktop
        * sandbox: seunshare: introduce helper spawn_command
        * sandbox: seunshare: introduce new filesystem helpers
        * sandbox: add -C option to not drop
        * sandbox: split seunshare caps dropping
        * sandbox: use dbus-launch
        * sandbox: numerous simple updates to sandbox
        * sandbox: do not require selinux context
        * sandbox: Makefile: new man pages
        * sandbox: rename dir to srcdir
        * sandbox: allow users specify sandbox window size
        * sandbox: check for paths up front
        * sandbox: use defined values for paths rather
        * sandbox: move seunshare globals to the top
        * sandbox: whitespace fix
        * semodule_package: Add semodule_unpackage executable
        * setfiles: get rid of some stupid globals
        * setfiles: move exclude_non_seclabel_mounts to a generic location
   * sepolgen
        * refparser: include open among valid permissions
        * refparser: add support for filename_trans rules

* Thu Aug 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-2
- Fix bug in glob handling for restorecon

* Thu Aug 18 2011 Dan Walsh <dwalsh@redhat.com> - 2.1.4-1
-Update to upstream
2.1.4 2011-08-17
        * run_init: clarification of the usage in the
        * semanage: fix usage header around booleans
        * semanage: remove useless empty lines
        * semanage: update man page with new examples
        * semanage: update usage text
        * semanage: introduce file context equivalencies
        * semanage: enable and disable modules
        * semanage: output all local modifications
        * semanage: introduce extraction of local configuration
        * semanage: cleanup error on invalid operation
        * semanage: handle being called with no arguments
        * semanage: return sooner to save CPU time
        * semanage: surround getopt with try/except
        * semanage: use define/raise instead of lots of
        * semanage: some options are only valid for
        * semanage: introduce better deleteall support
        * semanage: do not allow spaces in file
        * semanage: distinguish between builtin and local permissive
        * semanage: centralized ip node handling
        * setfiles: make the restore function exclude() non-static
        * setfiles: use glob to handle ~ and
        * fixfiles: do not hard code types
        * fixfiles: stop trying to be smart about
        * fixfiles: use new kernel seclabel option
        * fixfiles: pipe everything to cat before sending
        * fixfiles: introduce /etc/selinux/fixfiles_exclude_dirs
        * semodule: support for alternative root paths
2.1.3 2011-08-03
        * semanage: fix indention
        * semodule_package: fix man page typo
        * semodule_expand: update man page with -a
        * semanage: handle os errors
        * semanage: fix traceback with bad options
        * semanage: show usage on -h or --help
        * semanage: introduce more deleteall options
        * semanage: verify ports < 65536
        * transaction into semanageRecords
        * make get_handle a method of semanageRecords
        * remove a needless blank line
        * make process_one error if not initialized correctly
        * fixfiles: correct usage for r_opts.rootpath
        * put -p in help for restorecon and
        * fixfiles: do not try to only label
        * fixfiles clean up /var/run and /var/lib/debug
        * fixfiles delete tmp sockets and pipes rather
        * fixfile use find -delete instead of pipe
        * chcat man page typo
        * add man page for genhomedircon
        * setfiles fix typo
        * setsebool should inform users they need to
        * setsebool typos
        * open_init_tty man page typos
        * Don't add user site directory to sys.path
        * newrole retain CAP_SETPCAP
2.1.2 2011-08-02
        * seunshare: define _GNU_SOURCE earlier
        * make ignore_enoent do something
        * restorecond: first user logged in is not noticed
        * Repo: update .gitignore
2.1.1 2011-08-01
        * Man page updates
        * restorecon fix for bad inotify assumptions
2.1.0 2011-07-27
        * Release, minor version bump

* Tue Jul 26 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-20
- Fix sepolgen usage statement
- Stop using -k insandbox
- Fix seunshare usage statement

* Thu Jul 7 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-18
- Change seunshare to send kill signals to the childs session.
- Also add signal handler to catch sigint, so if user enters ctrl-C sandbox will shutdown.

* Wed Jul 6 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-17
- Add -k qualifier to seunshare to have it attempt to kill all processes with
the matching MCS label.

* Tue Jul 5 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-16
- Add -C option to sandbox and seunshare to maintain capabilities, otherwise
the bounding set will be dropped.
- Change --cgroups short name -c rather then -C for consistancy
- Fix memory and fd leaks in seunshare

* Wed Jun 29 2011 Jóhann B. Guðmundsson <johannbg@gmail.com> - 2.0.86-15
- Introduce systemd unit file for restorecond drop SysV support

* Mon Jun 13 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-14
- Do not drop capability bounding set in seunshare, this allows sandbox to
- run setuid apps.

* Fri Jun 10 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-13
- Add semanage-bash-completion.sh script

* Tue Jun 7 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-12
- Remove mount -o bind calls from sandbox init script
- pam_namespace now has this built in.

* Tue Jun 7 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-11
- Pass desktop dpi to sandbox Xephyr window

* Mon Jun 6 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-10
- Allow semodule to pick alternate root for selinux files
- Add ~/.config/* to restorcond_user.conf, so restorecond will watch for mislabeled files in this directory.

* Wed May 25 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-9
- Fix var_spool template read_spool_files
- Fix sepolgen to handle filename transitions

* Mon May 23 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-8
- Templates cleanedup by Dominic Grift

* Fri Apr 29 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-7
- Clean up some of the templates for sepolgen

* Fri Apr 22 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-6
- Apply patches from Christoph A.
  * fix sandbox title
  * stop xephyr from li
- Also ignore errors on sandbox include of directory missing files

* Thu Apr 21 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-5
- rebuild versus latest libsepol

* Mon Apr 18 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-4
- Change fixfiles restore to delete unlabeled sockets in /tmp

* Mon Apr 18 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-2
- rebuild versus latest libsepol

* Tue Apr 12 2011 Dan Walsh <dwalsh@redhat.com> 2.0.86-1
- Update to upstream
        * Use correct color range in mcstrand by Richard Haines.

* Mon Apr 11 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-30
- Add Elia Pinto patches to allow user to specify directories to ignore

* Tue Apr 5 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-29
- Fix policycoreutils-sandbox description

* Tue Mar 29 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-28
- rsynccmd should run outside of execcon

* Thu Mar 24 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-27
- Fix semange node handling of ipv6 addresses

* Wed Mar 23 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-26
- Fix sepolgen-ifgen call, add -p option

* Wed Mar 23 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-25
- Fix sepolgen-ifgen call

* Fri Mar 18 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-24
- Fix rsync command to work if the directory is old.
- Fix all tests

* Wed Mar 16 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-23
- Fix sepolgen to generate network polcy using generic_if and genric_node versus all_if and all_node

* Wed Mar 16 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-22
- Return to original seunshare man page

* Fri Mar 11 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-21
- change default location of HOMEDIR in sandbox to /tmp/.sandbox_home_*
- This will allow default sandboxes to work on NFS homedirs without allowing
  access to homedir data

* Fri Mar 11 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-20
- Change sepolgen-ifgen to search all available policy files
- Exit in restorecond if it can not find a UID in the passwd database

* Wed Mar 9 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-19
- Fix portspage in system-config-selinux to not crash
- More fixes for seunshare from Tomas Hoger

* Tue Mar 8 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-18
- put back in old handling of -T in sandbox command
- Put back setsid in seunshare
- Fix rsync to maintain times

* Tue Mar 8 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-17
- Use rewritten seunshare from thoger

* Mon Mar 7 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-16
- Require python-IPy for policycoreutils-python package
- Fixes for sepologen
  - Usage statement needs -n name
  - Names with _ are being prevented
  - dbus apps should get _chat interface

* Thu Mar 3 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-15
- Fix error message in seunshare, check for tmpdir existance before unlink.

* Fri Feb 25 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-13
- Rewrite seunshare to make sure /tmp is mounted stickybit owned by root
- Only allow names in polgengui that contain letters and numbers
- Fix up node handling in semanage command
- Update translations

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.85-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 3 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-11
- Fix sandbox policy creation with udp connect ports

* Thu Feb 3 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-10
- Cleaup selinux-polgengui to be a little more modern, fix comments and use selected name
- Cleanup chcat man page

* Wed Feb 2 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-9
- Report full errors on OSError on Sandbox

* Fri Jan 21 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-8
- Fix newrole hanlding of pcap

* Wed Jan 19 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-7
- Have restorecond watch more directories in homedir

* Fri Jan 14 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-6
- Add sandbox to sepolgen

* Thu Jan 6 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-4
- Fix proper handling of getopt errors
- Do not allow modules names to contain spaces

* Wed Jan 5 2011 Dan Walsh <dwalsh@redhat.com> 2.0.85-3
- Polgengui raises the wrong type of exception.  #471078
- Change semanage to not allow it to semanage module -D
- Change setsebool to suggest run as root on failure

* Wed Dec 22 2010 Dan Walsh <dwalsh@redhat.com> 2.0.85-2
- Fix restorecond watching utmp file for people logging in our out

* Tue Dec 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.85-1
- Update to upstream

* Thu Dec 16 2010 Dan Walsh <dwalsh@redhat.com> 2.0.84-5
- Change to allow sandbox to run on nfs homedirs, add start python script

* Wed Dec 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.84-4
- Move seunshare to sandbox package

* Mon Nov 29 2010 Dan Walsh <dwalsh@redhat.com> 2.0.84-3
- Fix sandbox to show correct types in usage statement

* Mon Nov 29 2010 Dan Walsh <dwalsh@redhat.com> 2.0.84-2
- Stop fixfiles from complaining about missing dirs

* Mon Nov 22 2010 Dan Walsh <dwalsh@redhat.com> 2.0.84-1
- Update to upstream
- List types available for sandbox in usage statement

* Mon Nov 22 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-37
- Don't report error on load_policy when system is disabled.

* Mon Nov 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-36
- Fix up problems pointed out by solar designer on dropping capabilities

* Mon Nov 1 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-35
- Check if you have full privs and reset otherwise dont drop caps

* Mon Nov 1 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-34
- Fix setools require line

* Fri Oct 29 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-33
- Move /etc/pam.d/newrole in to polcicycoreutils-newrole
- Additional capability checking in sepolgen

* Mon Oct 25 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-32
- Remove setuid flag and replace with file capabilities
- Fix sandbox handling of files with spaces in them

* Wed Sep 29 2010 jkeating - 2.0.83-31
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-30
- Move restorecond into its own subpackage

* Thu Sep 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-29
- Fix semanage man page

* Mon Sep 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-28
- Add seremote, to allow the execution of command inside the sandbox from outside the sandbox.

* Mon Sep 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-27
- Fix sandbox copyfile when copying a dir with a socket, print error

* Fri Sep 10 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-26
- Stop polgengui from crashing if selinux policy is not installed

* Thu Sep 9 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-25
- Fix bug preventing sandbox from using -l

* Tue Sep 7 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-24
- Eliminate quotes fro desktop files

* Mon Aug 30 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-23
- Add -w windowsize patch from Christoph A.

* Mon Aug 30 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-22
- Update po

* Wed Aug 25 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-21
- Update po

* Tue Aug 24 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-20
- Tighten down seunshare to create /tmp dir with sticky bit and MS_NODEV | MS_NOSUID | MS_NOEXEC;
- Remove setsid on seunshare so ^c on sandbox will cause apps to exit
- Add dbus-launch --exit-with-session so all processes launched within the sandbox exit with the sandbox
- Clean up error handling so error will get sent back to sandbox tool

* Mon Aug 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-19
- Fix translation handling in file context page of system-config-selinux

* Fri Aug 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-18
- Fix sandbox error handling

* Fri Aug 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-17
- Apply patch to restorecond from Chris Adams, which will cause restorecond
- to watch first user that logs in.

* Thu Aug 12 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-16
- Add COPYING file to doc dir

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-15
- Update po and translations
Resolves: #610473

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-14
- More fixes for polgen tools

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-13
- Remove requirement to run selinux-polgen as root

* Thu Aug 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-12
- Update po and translations
- Fix gui policy generation tools

* Wed Aug 4 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-11
- Update po and translations

* Sat Jul 31 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.83-10
- rebuild against python 2.7

* Wed Jul 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-9
- Update selinux-polgengui to sepolgen policy generation

* Wed Jul 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-8
- Fix invalid free in seunshare and fix man page

* Tue Jul 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-7
- Update translations

* Mon Jul 26 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-6
- Fix sandbox man page

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.0.83-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 20 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-4
- Add translations for menus
- Fixup man page from Russell Coker

* Tue Jun 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-3
- Change python scripts to use -s flag
- Update po

* Tue Jun 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.83-1
- Update to upstream
        * Add sandbox support from Dan Walsh with modifications from Steve Lawrence.

* Tue Jun 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-31
- Fix sepolgen code generation
Resolve: #603001

* Tue Jun 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-30
- Add cgroup support for sandbox

* Mon Jun 7 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-29
- Allow creation of /var/cache/DOMAIN from sepolgen

* Thu Jun 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-28
- Fix sandbox init script
- Add dbus-launch to sandbox -X
Resolve: #599599

* Thu Jun 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-27
- Move genhomedircon.8 to same package as genhomedircon
- Fix sandbox to pass unit test
Resolves: #595796

* Wed Jun 2 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-26
- Fix listing of booleans from audit2allow

* Wed Jun 2 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-25
- Fix audit2allow to output if the current policy has avc
- Update translations
- Fix icon

* Thu May 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-24
- Man page fixes
- sandbox fixes
- Move seunshare to base package

* Fri May 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-23
- Fix seunshare translations
- Fix seunshare to work on all arches
- Fix icon for system-config-selinux
Resolves: #595276

* Fri May 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-22
- Fix can_exec definition in sepolgen

* Fri May 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-21
- Add man page for seunshare and genhomedircon
Resolves: #594303
- Fix node management via semanage

* Wed May 19 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-20
- Fixes from upstream for sandbox command
Resolves: #580938

* Thu May 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-18
- Fix sandbox error handling on copyfile
- Fix desktop files

* Tue May 11 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-17
- Fix policy tool to have correct name in menus
- Fix seunshare to handle /tmp being in ~/home
- Fix saving of altered files
- Update translations

* Tue May 4 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-15
- Allow audit2allow to specify alternative policy file for analysis

* Mon May 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-14
- Update po
- Fix sepolgen --no_attrs
Resolves: #588280

* Thu Apr 29 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-13
- Make semanage boolean work on disabled machines and during livecd xguest
- Fix homedir and tmpdir handling in sandbox
Resolves: #587263

* Wed Apr 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-11
- Make semanage boolean work on disabled machines

* Tue Apr 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-10
- Make sepolgen-ifgen be quiet

* Wed Apr 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-8
- Make sepolgen report on more interfaces
- Fix system-config-selinux display of modules

* Thu Apr 15 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-7
- Fix crash when args are empty
Resolves: #582542
- Fix semange to exit on bad options
- Fix semanage dontaudit man page section
Resolves: #582533

* Wed Apr 14 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-6
- Remove debug line from semanage
- Update po

* Tue Apr 13 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-5
- Fix sandbox comment on HOMEDIRS
- Fix sandbox to throw error on bad executable

* Tue Apr 6 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-4
- Fix spacing in templates

* Wed Mar 31 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-3
- Fix semanage return codes

* Tue Mar 30 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-2
- Fix sepolgen to confirm to the "Reference Policy Style Guide"

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.82-1
- Update to upstream
        * Add avc's since boot from Dan Walsh.
        * Fix unit tests from Dan Walsh.

* Tue Mar 23 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-4
- Update to upstream - sepolgen
        * Add since-last-boot option to audit2allow from Dan Walsh.
        * Fix sepolgen output to match what Chris expects for upstream
          refpolicy from Dan Walsh.

* Mon Mar 22 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-3
- Allow restorecon on > 2 Gig files

* Tue Mar 16 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-2
- Fix semanage handling of boolean options
- Update translations

* Fri Mar 12 2010 Dan Walsh <dwalsh@redhat.com> 2.0.81-1
- Update to upstream
        * Add dontaudit flag to audit2allow from Dan Walsh.

* Thu Mar 11 2010 Dan Walsh <dwalsh@redhat.com> 2.0.80-2
- Use --rbind in sandbox init scripts

* Mon Mar 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.80-1
- Update to upstream
        * Module enable/disable support from Dan Walsh.

* Mon Mar 1 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-5
- Rewrite of sandbox script, add unit test for sandbox
- Update translations

* Mon Mar 1 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-4
- Fix patch for dontaudit rules from audit2allow for upstream acceptance

* Fri Feb 26 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-3
- Fixes for fixfiles

* Wed Feb 17 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-2
- Fix sandbox to complain if mount-shared has not been run
- Fix to use /etc/sysconfig/sandbox

* Tue Feb 16 2010 Dan Walsh <dwalsh@redhat.com> 2.0.79-1
- Update to upstream
        * Fix double-free in newrole
- Fix python language handling

* Thu Feb 11 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-21
- Fix display of command in sandbox

* Fri Feb 5 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-20
- Catch OSError in semanage

* Wed Feb 3 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-19
- Fix seobject and fixfiles

* Fri Jan 29 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-17
- Change seobject to use translations properly

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-16
- Cleanup spec file
Resolves: 555835

* Thu Jan 28 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-15
- Add use_resolve to sepolgen

* Wed Jan 27 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-14
- Add session capability to sandbox
- sandbox -SX -H ~/.homedir -t unconfined_t -l s0:c15 /etc/gdm/Xsession

* Thu Jan 21 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-13
- Fix executable template for fifo files

* Tue Jan 19 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-12
- Fix patch xod xmodmap
- Exit 0 from script

* Thu Jan 14 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-11
- Run with the same xdmodmap in sandbox as outside
- Patch from Josh Cogliati

* Fri Jan 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-10
- Fix sepolgen to not generate user sh section on non user policy

* Fri Jan 8 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-9
- Add -e to semanage man page
- Add -D qualifier to audit2allow to generate dontaudit rules

* Wed Jan 6 2010 Dan Walsh <dwalsh@redhat.com> 2.0.78-8
- Speed up audit2allow processing of audit2why comments

* Fri Dec 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-7
- Fixes to sandbox man page

* Thu Dec 17 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-6
- Add setools-libs-python to requires for gui

* Wed Dec 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-5
- If restorecond running as a user has no files to watch then it should exit.  (NFS Homedirs)

* Thu Dec 10 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-4
- Move sandbox man page to base package

* Tue Dec 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-3
- Fix audit2allow to report constraints, dontaudits, types, booleans

* Fri Dec 4 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-2
- Fix restorecon -i to ignore enoent

* Tue Dec 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.78-1
- Update to upstream
        * Remove non-working OUTFILE from fixfiles from Dan Walsh.
        * Additional exception handling in chcat from Dan Walsh.
        * fix sepolgen to read a "type 1403" msg as a policy load by Stephen
          Smalley <sds@tycho.nsa.gov>
        * Add support for Xen ocontexts from Paul Nuzzi.

* Tue Nov 24 2009 Dan Walsh <dwalsh@redhat.com> 2.0.77-1
- Update to upstream
        * Fixed bug preventing semanage node -a from working
          from Chad Sellers
        * Fixed bug preventing semanage fcontext -l from working
          from Chad Sellers
- Change semanage to use unicode

* Wed Nov 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.76-1
- Update to upstream
        * Remove setrans management from semanage, as it does not work
          from Dan Walsh.
        * Move load_policy from /usr/sbin to /sbin from Dan Walsh.

* Mon Nov 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.75-3
- Raise exception if user tries to add file context with an embedded space

* Wed Nov 11 2009 Dan Walsh <dwalsh@redhat.com> 2.0.75-2
- Fix sandbox to setsid so it can run under mozilla without crashing the session

* Mon Nov 2 2009 Dan Walsh <dwalsh@redhat.com> 2.0.75-1
- Update to upstream
        * Factor out restoring logic from setfiles.c into restore.c

* Fri Oct 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-15
- Fix typo in seobject.py

* Fri Oct 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-14
- Allow semanage -i and semanage -o to generate customization files.
- semanage -o will generate a customization file that semanage -i can read and set a machines to the same selinux configuration

* Tue Oct 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-13
- Fix restorecond man page

* Mon Oct 19 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-12
- Add generation of the users context file to polgengui

* Fri Oct 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-11
- Remove tabs from system-config-selinux glade file

* Thu Oct 15 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-10
- Remove translations screen from system-config-selinux

* Wed Oct 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-9
- Move fixfiles man pages into the correct package
- Add genhomedircon to fixfiles restore

* Tue Oct 6 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-8
- Add check to sandbox to verify save changes - Chris Pardy
- Fix memory leak in restorecond - Steve Grubb

* Thu Oct 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-7
- Fixes Templates

* Thu Oct 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-6
- Fixes for polgengui to handle tcp ports correctly
- Fix semanage node -a

* Wed Sep 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-5
- Fixes for semanage -equiv, readded modules, --enable, --disable

* Sun Sep 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-4
- Close sandbox when eclipse exits

* Fri Sep 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-3
- Security fixes for seunshare
- Fix Sandbox to handle non file input to command.

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-2
- Security fixes for seunshare

* Thu Sep 17 2009 Dan Walsh <dwalsh@redhat.com> 2.0.74-1
- Update to upstream
        * Change semodule upgrade behavior to install even if the module
          is not present from Dan Walsh.
        * Make setfiles label if selinux is disabled and a seclabel aware
          kernel is running from Caleb Case.
        * Clarify forkpty() error message in run_init from Manoj Srivastava.

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-5
- Fix sandbox to handle relative paths

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-4
- Add symbolic link to load_policy

* Mon Sep 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-3
- Fix restorecond script to use force-reload

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-2
- Fix init script to show status in usage message

* Tue Sep 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.73-1
- Update to upstream
        * Add semanage dontaudit to turn off dontaudits from Dan Walsh.
        * Fix semanage to set correct mode for setrans file from Dan Walsh.
        * Fix malformed dictionary in portRecord from Dan Walsh.
        * Restore symlink handling support to restorecon based on a patch by
        Martin Orr.  This fixes the restorecon /dev/stdin performed by Debian
        udev scripts that was broken by policycoreutils 2.0.70.

* Thu Sep 3 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-15
- Add DAC_OVERRIED to seunshare

* Wed Sep  2 2009 Bill Nottingham <notting@redhat.com> 2.0.71-15
- Fix typo

* Fri Aug 28 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-14
- Add enable/disable patch

* Thu Aug 27 2009 Tomas Mraz <tmraz@redhat.com> - 2.0.71-13
- rebuilt with new audit

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-12
- Tighten up controls on seunshare.c

* Wed Aug 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-11
- Add sandboxX

* Sat Aug 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-10
- Fix realpath usage to only happen on argv input from user

* Fri Aug 21 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.0.71-9
- Don't try to remove restorecond after last erase (done already in %%preun).
- Ensure scriptlets exit with status 0.
- Fix %%post and %%pr

* Thu Aug 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-7
- Fix glob handling of /..

* Wed Aug 19 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-6
- Redesign restorecond to use setfiles/restore functionality

* Wed Aug 19 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-5
- Fix sepolgen again

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-4
- Add --boot flag to audit2allow to get all AVC messages since last boot

* Tue Aug 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-3
- Fix semanage command

* Thu Aug 13 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-2
- exclude unconfined.if from sepolgen

* Thu Aug 13 2009 Dan Walsh <dwalsh@redhat.com> 2.0.71-1
- Fix chcat to report error on non existing file
- Update to upstream
        * Modify setfiles/restorecon checking of exclude paths.  Only check
        user-supplied exclude paths (not automatically generated ones based on
        lack of seclabel support), don't require them to be directories, and
        ignore permission denied errors on them (it is ok to exclude a path to
        which the caller lacks permission).

* Mon Aug 10 2009 Dan Walsh <dwalsh@redhat.com> 2.0.70-2
- Don't warn if the user did not specify the exclude if root can not stat file system

* Wed Aug 5 2009 Dan Walsh <dwalsh@redhat.com> 2.0.70-1
- Update to upstream
        * Modify restorecon to only call realpath() on user-supplied pathnames
        from Stephen Smalley.
        * Fix typo in fixfiles that prevented it from relabeling btrfs
          filesystems from Dan Walsh.

* Wed Jul 29 2009 Dan Walsh <dwalsh@redhat.com> 2.0.68-1
- Fix location of man pages
- Update to upstream
        * Modify setfiles to exclude mounts without seclabel option in
        /proc/mounts on kernels >= 2.6.30 from Thomas Liu.
        * Re-enable disable_dontaudit rules upon semodule -B from Christopher
        Pardy and Dan Walsh.
        * setfiles converted to fts from Thomas Liu.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.64-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Tom "spot" Callaway <tcallawa@redhat.com> 2.0.64-2
- fix multiple directory ownership of mandirs

* Fri Jun 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.64-1
- Update to upstream
        * Keep setfiles from spamming console from Dan Walsh.
        * Fix chcat's category expansion for users from Dan Walsh.
- Update po files
- Fix sepolgen

* Thu Jun 4 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-5
- Add sepolgen executable

* Mon Jun 1 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-4
- Fix Sandbox option handling
- Fix fixfiles handling of btrfs

* Tue May 26 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-3
- Fix sandbox to be able to execute files in homedir

* Fri May 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-2
- Change polgen.py to be able to generate policy

* Wed May 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.63-1
- Update to upstream
        * Fix transaction checking from Dan Walsh.
        * Make fixfiles -R (for rpm) recursive.
        * Make semanage permissive clean up after itself from Dan Walsh.
        * add /root/.ssh/* to restorecond.conf

* Wed Apr 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-14
- Fix audit2allow -a to retun /var/log/messages

* Wed Apr 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-13
- Run restorecond as a user service

* Thu Apr 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-12
- Add semanage module support

* Tue Apr 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-10
- Do not print \n, if count < 1000;

* Sat Apr 11 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-9
- Handle case where subs file does not exist

* Wed Apr 8 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-8
- Update po files
- Add --equiv command for semanage

* Tue Mar 31 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-7
- Cleanup creation of permissive domains
- Update po files

* Mon Mar 23 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-6
- Update po files

* Thu Mar 12 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-5
- Fix semanage transations

* Sat Mar 7 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-4
- Update polgengui templates to match current upstream policy

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.62-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 23 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-2
- Add /root/.ssh to restorecond.conf
- fixfiles -R package should recursively fix files

* Wed Feb 18 2009 Dan Walsh <dwalsh@redhat.com> 2.0.62-1
- Update to upstream
        * Add btrfs to fixfiles from Dan Walsh.
        * Remove restorecond error for matching globs with multiple hard links
        and fix some error messages from Dan Walsh.
        * Make removing a non-existant module a warning rather than an error
          from Dan Walsh.
        * Man page fixes from Dan Walsh.

* Mon Feb 16 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-10
- Fix script created by polgengui to not refer to selinux-policy-devel

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-9
- Change initc scripts to use proper labeling on gui

* Mon Feb 9 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-8
- Add obsoletes to cause policycoreuils to update both python and non python version

* Fri Jan 30 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-7
- Dont report errors on glob match and multiple links

* Thu Jan 22 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-6
- Move sepolgen-ifgen to post python

* Wed Jan 21 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-4
- Fix Translations

* Tue Jan 20 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-3
- Add Domains Page to system-config-selinux
- Add ability to create dbus confined applications to polgen

* Wed Jan 14 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-2
- Split python into a separate package

* Tue Jan 13 2009 Dan Walsh <dwalsh@redhat.com> 2.0.61-1
- Update to upstream
        * chcat: cut categories at arbitrary point (25) from Dan Walsh
        * semodule: use new interfaces in libsemanage for compressed files
          from Dan Walsh
        * audit2allow: string changes for usage

* Tue Jan 6 2009 Dan Walsh <dwalsh@redhat.com> 2.0.60-7
- Don't error out when removing a non existing module

* Mon Dec 15 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-6
- fix audit2allow man page

* Wed Dec 10 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-5
- Fix Japanese translations

* Sat Dec 6 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-4
- Change md5 to hashlib.md5 in sepolgen

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.60-3
- Rebuild for Python 2.6

* Tue Dec 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-2
- Fix error checking in restorecond, for inotify_add_watch

* Mon Dec 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.60-1
- Update to upstream
        * semanage: use semanage_mls_enabled() from Stephen Smalley.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0.59-2
- Rebuild for Python 2.6

* Tue Nov 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.59-1
- Update to upstream
        * fcontext add checked local records twice, fix from Dan Walsh.

* Mon Nov 10 2008 Dan Walsh <dwalsh@redhat.com> 2.0.58-1
- Update to upstream
        * Allow local file context entries to override policy entries in
        semanage from Dan Walsh.
        * Newrole error message corrections from Dan Walsh.
        * Add exception to audit2why call in audit2allow from Dan Walsh.

* Fri Nov 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-12
- add compression

* Tue Nov 04 2008 Jesse Keating <jkeating@redhat.com> - 2.0.57-11
- Move the usermode-gtk requires to the -gui subpackage.

* Thu Oct 30 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-10
- Fix traceback in audit2why

* Wed Oct 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-9
- Make GUI use translations

* Wed Oct 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-8
- Fix typo in man page

* Tue Oct 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-7
- Handle selinux disabled correctly
- Handle manipulation of fcontext file correctly

* Mon Oct 27 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-6
- Add usermode-gtk requires

* Thu Oct 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-5
- Allow addition of local modifications of fcontext policy.

* Mon Oct 20 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-4
- Fix system-config-selinux booleanspage throwing and exception
- Update po files

* Fri Oct 17 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-3
- Fix text in newrole
- Fix revertbutton on booleans page in system-config-selinux

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-2
- Change semodule calls for libsemanage

* Wed Oct 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.57-1
- Update to upstream
        * Update po files from Dan Walsh.

* Fri Sep 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.56-1
- Fix semanage help display
- Update to upstream
        * fixfiles will now remove all files in /tmp and will check for
          unlabeled_t in /tmp and /var/tmp from Dan Walsh.
        * add glob support to restorecond from Dan Walsh.
        * allow semanage to handle multi-line commands in a single transaction
          from Dan Walsh.

* Thu Sep 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-8
- Only call gen_requires once in sepolgen

* Tue Sep 9 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-7
- Change Requires line to gnome-python2-gnome
- Fix spelling mistakes
- Require libselinux-utils

* Mon Sep 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-5
- Add node support to semanage

* Mon Sep 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-4
- Fix fixfiles to correct unlabeled_t files and remove .? files

* Wed Sep 3 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-2
- Add glob support to restorecond so it can check every file in the homedir

* Thu Aug 28 2008 Dan Walsh <dwalsh@redhat.com> 2.0.55-1
- Update to upstream
        * Merged semanage node support from Christian Kuester.

* Fri Aug 15 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-7
- Add require libsemanage-python

* Mon Aug 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-6
- Add missing html_util.py file

* Thu Aug 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-5
- Fixes for multiple transactions

* Wed Aug 6 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-2
- Allow multiple transactions in one semanage command

* Tue Aug 5 2008 Dan Walsh <dwalsh@redhat.com> 2.0.54-1
- Update to upstream
        * Add support for boolean files and group support for seusers from Dan Walsh.
        * Ensure that setfiles -p output is newline terminated from Russell Coker.

* Fri Aug 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.53-3
- Allow semanage user to add group lists % groupname

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.53-2
- Fix help

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.53-1
- Update to upstream
        * Change setfiles to validate all file_contexts files when using -c from Stephen Smalley.

* Tue Jul 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-6
- Fix boolean handling
- Upgrade to latest sepolgen
- Update po patch

* Wed Jul 9 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-5
- Additial cleanup of boolean handling for semanage

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-4
- Handle ranges of ports in gui

* Tue Jul 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-3
- Fix indent problems in seobject

* Wed Jul 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-2
- Add lockdown wizard
- Allow semanage booleans to take an input file an process lots of booleans at once.

* Wed Jul 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.52-1
- Default prefix to "user"

* Tue Jul 1 2008 Dan Walsh <dwalsh@redhat.com> 2.0.50-2
- Remove semodule use within semanage
- Fix launching of polgengui from toolbar

* Mon Jun 30 2008 Dan Walsh <dwalsh@redhat.com> 2.0.50-1
- Update to upstream
        * Fix audit2allow generation of role-type rules from Karl MacMillan.

* Tue Jun 24 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-10
- Fix spelling of enforcement

* Mon Jun 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-8
- Fix sepolgen/audit2allow handling of roles

* Mon Jun 16 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-7
- Fix sepolgen-ifgen processing

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-6
- Add deleteall to semanage permissive, cleanup error handling

* Thu Jun 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-5
- Complete removal of rhpl requirement

* Wed Jun 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-4
- Add semanage permissive *

* Fri May 16 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-3
- Fix fixfiles to cleanup /tmp and /var/tmp

* Fri May 16 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-2
- Fix listing of types in gui

* Mon May 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.49-1
- Update to upstream
        * Remove security_check_context calls for prefix validation from semanage.
        * Change setfiles and restorecon to not relabel if the file already has the correct context value even if -F/force is specified.

* Mon May 12 2008 Dan Walsh <dwalsh@redhat.com> 2.0.47-3
- Remove /usr/share/locale/sr@Latn/LC_MESSAGES/policycoreutils.mo

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.47-2
- Add rm -rf /tmp/gconfd-* /tmp/pulse-* /tmp/orbit-* to fixfiles restore
- So that mislabeled files will get removed on full relabel

* Wed May 7 2008 Dan Walsh <dwalsh@redhat.com> 2.0.47-1
- Make restorecond not start by default
- Fix polgengui to allow defining of confined roles.
- Add patches from Lubomir Rintel <lkundrak@v3.sk>
  * Add necessary runtime dependencies on setools-console for -gui
  * separate stderr when run seinfo commands
- Update to upstream
  * Update semanage man page for booleans from Dan Walsh.
  * Add further error checking to seobject.py for setting booleans.

* Fri Apr 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.0.46-5
- Uninvasive (ie no string or widget changes) HIG approximations
  in selinux-polgenui

* Fri Apr 18 2008 Matthias Clasen <mclasen@redhat.com> - 2.0.46-4
- Move s-c-selinux to the right menu

* Sun Apr 6 2008 Dan Walsh <dwalsh@redhat.com> 2.0.46-3
- Fix boolean descriptions
- Fix semanage man page

* Wed Mar 19 2008 Dan Walsh <dwalsh@redhat.com> 2.0.46-2
- Don't use prefix in gui

* Tue Mar 18 2008 Dan Walsh <dwalsh@redhat.com> 2.0.46-1
- Update to upstream
        * Update audit2allow to report dontaudit cases from Dan Walsh.
        * Fix semanage port to use --proto from Caleb Case.

* Fri Feb 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.44-1
- Update to upstream
        * Fix for segfault when conf file parse error occurs.

* Wed Feb 13 2008 Dan Walsh <dwalsh@redhat.com> 2.0.43-2
- Don't show tabs on polgengui

* Wed Feb 13 2008 Dan Walsh <dwalsh@redhat.com> 2.0.43-1
- Update to upstream
        * Merged fix fixfiles option processing from Vaclav Ovsik.
- Added existing users, staff and user_t users to polgengui

* Fri Feb 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.42-3
- Add messages for audit2allow DONTAUDIT

* Tue Feb 5 2008 Dan Walsh <dwalsh@redhat.com> 2.0.42-2
- Add ability to transition to roles via polgengui

* Sat Feb 2 2008 Dan Walsh <dwalsh@redhat.com> 2.0.42-1
- Update to upstream
        * Make semodule_expand use sepol_set_expand_consume_base to reduce
          peak memory usage.

* Tue Jan 29 2008 Dan Walsh <dwalsh@redhat.com> 2.0.41-1
- Update to upstream
        * Merged audit2why fix and semanage boolean --on/--off/-1/-0 support from Dan Walsh.
        * Merged a second fixfiles -C fix from Marshall Miller.

* Thu Jan 24 2008 Dan Walsh <dwalsh@redhat.com> 2.0.39-1
- Don't initialize audit2allow for audit2why call.  Use default
- Update to upstream
        * Merged fixfiles -C fix from Marshall Miller.

* Thu Jan 24 2008 Dan Walsh <dwalsh@redhat.com> 2.0.38-1
- Update to upstream
  * Merged audit2allow cleanups and boolean descriptions from Dan Walsh.
  * Merged setfiles -0 support by Benny Amorsen via Dan Walsh.
  * Merged fixfiles fixes and support for ext4 and gfs2 from Dan Walsh.

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.37-1
- Update to upstream
  * Merged replacement for audit2why from Dan Walsh.

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.36-2
- Cleanup fixfiles -f message in man page

* Wed Jan 23 2008 Dan Walsh <dwalsh@redhat.com> 2.0.36-1
- Update to upstream
        * Merged update to chcat, fixfiles, and semanage scripts from Dan Walsh.
        * Merged sepolgen fixes from Dan Walsh.

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-5
- handle files with spaces on upgrades

* Tue Jan 22 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-4
- Add support in fixfiles for ext4 ext4dev and gfs2

* Mon Jan 21 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-3
- Allow files with spaces to be used by setfiles

* Tue Jan 15 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-2
- Add descriptions of booleans to audit2allow

* Fri Jan 11 2008 Dan Walsh <dwalsh@redhat.com> 2.0.35-1
- Update to upstream
        * Merged support for non-interactive newrole command invocation from Tim Reed.

* Thu Jan 10 2008 Dan Walsh <dwalsh@redhat.com> 2.0.34-8
- Change to use selinux bindings to audit2why

* Tue Jan 8 2008 Dan Walsh <dwalsh@redhat.com> 2.0.34-7
- Fix fixfiles to handle no args

* Mon Dec 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-5
- Fix roles output when creating a module

* Mon Dec 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-4
- Handle files with spaces in fixfiles

* Fri Dec 21 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-3
- Catch SELINUX_ERR with audit2allow and generate policy

* Thu Dec 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-2
- Make sepolgen set error exit code when partial failure
- audit2why now checks booleans for avc diagnosis

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.34-1
- Update to upstream
        * Update Makefile to not build restorecond if
          /usr/include/sys/inotify.h is not present

* Wed Dec 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-4
- Fix sepolgen to be able to parse Fedora 9 policy
      Handle ifelse statements
      Handle refpolicywarn inside of define
      Add init.if and inetd.if into parse
      Add parse_file to syntax error message

* Fri Dec 14 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-3
- Add scroll bar to fcontext gui page

* Tue Dec 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-2
- Add Russion Man pages

* Mon Dec 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.33-1
- Upgrade from NSA
        * Drop verbose output on fixfiles -C from Dan Walsh.
        * Fix argument handling in fixfiles from Dan Walsh.
        * Enhance boolean support in semanage, including using the .xml description when available, from Dan Walsh.
- Fix handling of final screen in polgengui

* Sun Dec 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.32-2
- Fix handling of disable selinux button in gui

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.32-1
- Upgrade from NSA
        * load_policy initial load option from Chad Sellers.

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-20
- Don't show error on missing policy.xml

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-19
- GUI Enhancements
  - Fix cgi generation
  - Use more patterns

* Mon Nov 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-18
- Remove codec hacking, which seems to be fixed in python

* Fri Nov 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-17
- Fix typo
- Change to upstream minimal privledge interfaces

* Fri Nov 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-16
- Fix fixfiles argument parsing

* Thu Nov 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-15
- Fix File Labeling add

* Thu Nov 8 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-14
- Fix semanage to handle state where policy.xml is not installed

* Mon Nov 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-13
- Remove -v from restorecon in fixfiles

* Mon Nov 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-12
- Fix filter and search capabilities, add wait cursor

* Fri Nov 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-11
- Translate booleans via policy.xml
- Allow booleans to be set via semanage

* Thu Nov 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-10
- Require use of selinux-policy-devel

* Wed Oct 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-9
- Validate semanage fcontext input
- Fix template names for log files in gui

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-8
- Fix template to generate correct content

* Fri Oct 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-7
- Fix consolekit link to selinux-polgengui

* Thu Oct 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-6
- Fix the generation templates

* Tue Oct 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-5
- Fix enable/disable audit messages

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-4
- Add booleans page

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-3
- Lots of updates to gui

* Mon Oct 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.31-1
- Remove no.po
- Update to upstream
        * Fix semodule option handling from Dan Walsh.
        * Add deleteall support for ports and fcontexts in semanage from Dan Walsh.

* Thu Oct 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.29-2
- Fix semodule parameter checking

* Sun Oct 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.29-1
- Update to upstream
        * Add genhomedircon script to invoke semodule -Bn from Dan Walsh.
- Add deleteall for ports and fcontext

* Fri Oct 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.28-1
- Update to upstream
        * Update semodule man page for -D from Dan Walsh.
        * Add boolean, locallist, deleteall, and store support to semanage from Dan Walsh.

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-7
- Add genhomedircon script to rebuild file_context for shadow-utils

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-6
- Update translations

* Tue Oct 2 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-5
- Additional checkboxes for application policy

* Fri Sep 28 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-4
- Allow policy writer to select user types to transition to there users

* Thu Sep 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-3
- Fix bug in building policy with polgengui
- Creating ports correctly

* Wed Sep 26 2007 Dan Walsh <dwalsh@redhat.com> 2.0.27-1
- Update to upstream
        * Improve semodule reporting of system errors from Stephen Smalley.

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.26-3
- Show local changes with semanage

* Mon Sep 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.26-2
- Fixed spelling mistakes in booleans defs
- Update po

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.26-1
- Update to upstream
  * Fix setfiles selabel option flag setting for 64-bit from Stephen Smalley.

* Tue Sep 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-15
- Fix wording in policy generation tool

* Fri Sep 14 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-14
- Fix calls to _admin interfaces

* Thu Sep 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-13
- Upgrade version of sepolgen from NSA
        * Expand the sepolgen parser to parse all current refpolicy modules from Karl MacMillan.
        * Suppress generation of rules for non-denials from Karl MacMillan (take 3).

* Tue Sep 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-12
- Remove bogus import libxml2

* Mon Sep 10 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-11
- Lots of fixes for polgengui

* Thu Sep 6 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-10
- Change Requires /bin/rpm to rpm

* Wed Sep 5 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-9
- Bump libsemanage version for disable dontaudit
- New gui features for creating admin users

* Fri Aug 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-8
- Fix generated code for admin policy

* Fri Aug 31 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-7
- Lots of fixes for role templates

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-6
- Add more role_templates

* Tue Aug 28 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-5
- Update genpolgui to add creation of user domains

* Mon Aug 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-4
- Fix location of sepolgen-ifgen

* Sat Aug 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-3
- Add selinux-polgengui to desktop

* Fri Aug 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-2
- Cleanup spec

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.25-1
- Update semodule man page
        * Fix genhomedircon searching for USER from Todd Miller
        * Install run_init with mode 0755 from Dan Walsh.
        * Fix chcat from Dan Walsh.
        * Fix fixfiles pattern expansion and error reporting from Dan Walsh.
        * Optimize genhomedircon to compile regexes once from Dan Walsh.
        * Fix semanage gettext call from Dan Walsh.

* Thu Aug 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.23-2
- Update semodule man page

* Mon Aug 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.23-1
- Update to match NSA
        * Disable dontaudits via semodule -D

* Wed Aug 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-13
- Speed up genhomedircon by an order of magnitude by compiling regex
- Allow semanage fcontext -a -t <<none>> /path to work

* Fri Jul 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-11
- Fixfiles update required to match new regex

* Fri Jul 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-10
- Update booleans translations

* Wed Jul 25 2007 Jeremy Katz <katzj@redhat.com> - 2.0.22-9
- rebuild for toolchain bug

* Tue Jul 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-8
- Add requires libselinux-python

* Mon Jul 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-7
- Fix fixfiles to report incorrect rpm
- Patch provided by Tony Nelson

* Fri Jul 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-6
- Clean up spec file

* Fri Jul 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-5
- Require newer libselinux version

* Sat Jul 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-4
- Fix checking for conflicting directory specification in genhomedircon

* Mon Jun 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-3
- Fix spelling mistakes in GUI

* Fri Jun 22 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-2
- Fix else path in chcat

* Thu Jun 21 2007 Dan Walsh <dwalsh@redhat.com> 2.0.22-1
- Update to match NSA
        * Rebase setfiles to use new labeling interface.

* Wed Jun 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.21-2
- Add filter to all system-config-selinux lists

* Wed Jun 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.21-1
- Update to match NSA
        * Fixed setsebool (falling through to error path on success).

* Mon Jun 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.20-1
- Update to match NSA
        * Merged genhomedircon fixes from Dan Walsh.
        * Merged setfiles -c usage fix from Dan Walsh.
        * Merged restorecon fix from Yuichi Nakamura.
        * Dropped -lsepol where no longer needed.

* Mon Jun 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-5
- Fix translations code,  Add more filters to gui

* Mon Jun 4 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-4
- Fix setfiles -c to make it work

* Mon Jun 4 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-3
- Fix french translation to not crash system-config-selinux

* Fri Jun 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-2
- Fix genhomedircon to work in stage2 builds of anaconda

* Sat May 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.19-1
- Update to match NSA

* Thu May 17 2007 Dan Walsh <dwalsh@redhat.com> 2.0.16-2
- Fixes for polgentool templates file

* Fri May 4 2007 Dan Walsh <dwalsh@redhat.com> 2.0.16-1
- Updated version of policycoreutils
        * Merged support for modifying the prefix via semanage from Dan Walsh.
- Fixed genhomedircon to find homedirs correctly.

* Tue May 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.15-1
- Updated version of policycoreutils
        * Merged po file updates from Dan Walsh.
- Fix semanage to be able to modify prefix in user record

* Mon Apr 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.14-2
- Fix title on system-config-selinux

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.14-1
- Updated version of policycoreutils
        * Build fix for setsebool.

* Wed Apr 25 2007 Dan Walsh <dwalsh@redhat.com> 2.0.13-1
- Updated version of policycoreutils
        * Merged setsebool patch to only use libsemanage for persistent boolean changes from Stephen Smalley.
        * Merged genhomedircon patch to use the __default__ setting from Dan Walsh.
        * Dropped -b option from load_policy in preparation for always preserving booleans across reloads in the kernel.

* Tue Apr 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.10-2
- Fixes for polgengui

* Tue Apr 24 2007 Dan Walsh <dwalsh@redhat.com> 2.0.10-1
- Updated version of policycoreutils
        * Merged chcat, fixfiles, genhomedircon, restorecond, and restorecon patches from Dan Walsh.

* Fri Apr 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-10
- Fix genhomedircon to handle non user_u for the default user

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-9
- More cleanups for gui

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-8
- Fix size and use_tmp problem on gui

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-7
- Fix restorecon crash

* Wed Apr 18 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-6
- Change polgengui to a druid

* Tue Apr 17 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-5
- Fully path script.py

* Mon Apr 16 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-4
- Add -l flag to restorecon to not traverse file systems

* Sat Apr 14 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-3
- Fixes for policygengui

* Fri Apr 13 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-2
- Add polgengui

* Thu Apr 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.9-1
- Updated version of sepolgen
        * Merged seobject setransRecords patch to return the first alias from Xavier Toth.

* Wed Apr 11 2007 Dan Walsh <dwalsh@redhat.com> 2.0.8-1
- Updated version of sepolgen
        * Merged updates to sepolgen-ifgen from Karl MacMillan.
        * Merged updates to sepolgen parser and tools from Karl MacMillan.
          This includes improved debugging support, handling of interface
          calls with list parameters, support for role transition rules,
          updated range transition rule support, and looser matching.

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-11
- Don't generate invalid context with genhomedircon

* Mon Apr 9 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-10
- Add filter to booleans page

* Tue Apr 3 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-9
- Fix polgen.py to not generate udp rules on tcp input

* Fri Mar 30 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-8
- system-config-selinux should be able to run on a disabled system,
- at least enough to get it enabled.

* Thu Mar 29 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-7
- Many fixes to polgengui

* Fri Mar 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-6
- Updated version of sepolgen
        * Merged patch to discard self from types when generating requires from Karl MacMillan.

* Fri Mar 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-5
- Change location of audit2allow and sepol-ifgen to sbin
- Updated version of sepolgen
        * Merged patch to move the sepolgen runtime data from /usr/share to /var/lib to facilitate a read-only /usr from Karl MacMillan.

* Mon Mar 19 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-4
- Add polgen gui
- Many fixes to system-config-selinux

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-3
- service restorecond status needs to set exit value correctly

* Mon Mar 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-2
- Fix gui

* Thu Mar 1 2007 Dan Walsh <dwalsh@redhat.com> 2.0.7-1
- Update to upstream
        * Merged restorecond init script LSB compliance patch from Steve Grubb.
  -sepolgen
        * Merged better matching for refpolicy style from Karl MacMillan
        * Merged support for extracting interface paramaters from interface calls from Karl MacMillan
        * Merged support for parsing USER_AVC audit messages from Karl MacMillan.

* Tue Feb 27 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-3
- Update to upstream
  -sepolgen
        * Merged support for enabling parser debugging from Karl MacMillan.
- Add sgrupp cleanup of restorcon init script

* Mon Feb 26 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-2
- Add Bill Nottinham patch to run restorcond condrestart in postun

* Fri Feb 23 2007 Dan Walsh <dwalsh@redhat.com> 2.0.6-1
- Update to upstream
  - policycoreutils
        * Merged newrole O_NONBLOCK fix from Linda Knippers.
        * Merged sepolgen and audit2allow patches to leave generated files
          in the current directory from Karl MacMillan.
        * Merged restorecond memory leak fix from Steve Grubb.
  -sepolgen
        * Merged patch to leave generated files (e.g. local.te) in current directory from Karl MacMillan.
        * Merged patch to make run-tests.py use unittest.main from Karl MacMillan.
        * Merged patch to update PLY from Karl MacMillan.
        * Merged patch to update the sepolgen parser to handle the latest reference policy from Karl MacMillan.

* Thu Feb 22 2007 Dan Walsh <dwalsh@redhat.com> 2.0.3-2
- Do not fail on sepolgen-ifgen

* Thu Feb 22 2007 Dan Walsh <dwalsh@redhat.com> 2.0.3-1
- Update to upstream
        * Merged translations update from Dan Walsh.
        * Merged chcat fixes from Dan Walsh.
        * Merged man page fixes from Dan Walsh.
        * Merged seobject prefix validity checking from Dan Walsh.
        * Merged Makefile and refparser.py patch from Dan Walsh.
          Fixes PYTHONLIBDIR definition and error handling on interface files.

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-3
- Updated newrole NONBlOCK patch

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-2
- Remove Requires: %%{name}-plugins

* Tue Feb 20 2007 Dan Walsh <dwalsh@redhat.com> 2.0.2-1
- Update to upstream
        * Merged seobject exception handler fix from Caleb Case.
        * Merged setfiles memory leak patch from Todd Miller.

* Thu Feb 15 2007 Dan Walsh <dwalsh@redhat.com> 2.0.1-2
- Cleanup man pages syntax
- Add sepolgen

* Mon Feb 12 2007 Dan Walsh <dwalsh@redhat.com> 2.0.1-1
- Update to upstream
        * Merged small fix to correct include of errcodes.h in semodule_deps from Dan Walsh.

* Wed Feb 7 2007 Dan Walsh <dwalsh@redhat.com> 2.0.0-1
- Update to upstream
        * Merged new audit2allow from Karl MacMillan.
          This audit2allow depends on the new sepolgen python module.
          Note that you must run the sepolgen-ifgen tool to generate
          the data needed by audit2allow to generate refpolicy.
        * Fixed newrole non-pam build.
- Fix Changelog and spelling error in man page

* Thu Feb 1 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-4
- Fix audit2allow on missing translations

* Wed Jan 24 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-3
- More chcat fixes

* Wed Jan 24 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-2
- Change chcat to exec semodule so file context is maintained

* Wed Jan 24 2007 Dan Walsh <dwalsh@redhat.com> 1.34.1-1
- Fix system-config-selinux ports view
- Update to upstream
        * Fixed newrole non-pam build.
        * Updated version for stable branch.

* Wed Jan 17 2007 Dan Walsh <dwalsh@redhat.com> 1.33.15-1
- Update to upstream
        * Merged unicode-to-string fix for seobject audit from Dan Walsh.
        * Merged man page updates to make "apropos selinux" work from Dan Walsh.

* Tue Jan 16 2007 Dan Walsh <dwalsh@redhat.com> 1.33.14-1
        * Merged newrole man page patch from Michael Thompson.
        * Merged patch to fix python unicode problem from Dan Walsh.

* Tue Jan 16 2007 Dan Walsh <dwalsh@redhat.com> 1.33.12-3
- Fix handling of audit messages for useradd change
Resolves: #222159

* Fri Jan 12 2007 Dan Walsh <dwalsh@redhat.com> 1.33.12-2
- Update man pages by adding SELinux to header to fix apropos database
Resolves: #217881

* Tue Jan 9 2007 Dan Walsh <dwalsh@redhat.com> 1.33.12-1
- Want to update to match api
- Update to upstream
        * Merged newrole securetty check from Dan Walsh.
        * Merged semodule patch to generalize list support from Karl MacMillan.
Resolves: #200110

* Tue Jan 9 2007 Dan Walsh <dwalsh@redhat.com> 1.33.11-1
- Update to upstream
        * Merged fixfiles and seobject fixes from Dan Walsh.
        * Merged semodule support for list of modules after -i from Karl MacMillan.

* Tue Jan 9 2007 Dan Walsh <dwalsh@redhat.com> 1.33.10-1
- Update to upstream
        * Merged patch to correctly handle a failure during semanage handle
          creation from Karl MacMillan.
        * Merged patch to fix seobject role modification from Dan Walsh.

* Fri Jan 5 2007 Dan Walsh <dwalsh@redhat.com> 1.33.8-2
- Stop newrole -l from working on non secure ttys
Resolves: #200110

* Thu Jan 4 2007 Dan Walsh <dwalsh@redhat.com> 1.33.8-1
- Update to upstream
        * Merged patches from Dan Walsh to:
          - omit the optional name from audit2allow
          - use the installed python version in the Makefiles
          - re-open the tty with O_RDWR in newrole

* Wed Jan 3 2007 Dan Walsh <dwalsh@redhat.com> 1.33.7-1
- Update to upstream
        * Patch from Dan Walsh to correctly suppress warnings in load_policy.

* Tue Jan 2 2007 Dan Walsh <dwalsh@redhat.com> 1.33.6-9
- Fix fixfiles script to use tty command correctly.  If this command fails, it
should set the LOGFILE to /dev/null
Resolves: #220879

* Wed Dec 20 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-8
- Remove hard coding of python2.4 from Makefiles

* Tue Dec 19 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-7
- add exists switch to semanage to tell it not to check for existance of Linux user
Resolves: #219421

* Mon Dec 18 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-6
- Fix audit2allow generating reference policy
- Fix semanage to manage user roles properly
Resolves: #220071

* Fri Dec 8 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-5
- Update po files
- Fix newrole to open stdout and stderr rdrw so more will work on MLS machines
Resolves: #216920

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.33.6-4
- rebuild for python 2.5

* Wed Dec 6 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-3
- Update po files
Resolves: #216920

* Fri Dec 1 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-2
- Update po files
Resolves: #216920

* Wed Nov 29 2006 Dan Walsh <dwalsh@redhat.com> 1.33.6-1
- Update to upstream
        * Patch from Dan Walsh to add an pam_acct_msg call to run_init
        * Patch from Dan Walsh to fix error code returns in newrole
        * Patch from Dan Walsh to remove verbose flag from semanage man page
        * Patch from Dan Walsh to make audit2allow use refpolicy Makefile
          in /usr/share/selinux/<SELINUXTYPE>

* Wed Nov 29 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-4
- Fixing the Makefile line again to build with LSPP support
Resolves: #208838

* Wed Nov 29 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-3
- Don't report errors on restorecond when file system does not support XATTRS
Resolves: #217694

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-2
- Fix -q qualifier on load_policy
Resolves: #214827

* Tue Nov 28 2006 Dan Walsh <dwalsh@redhat.com> 1.33.5-1
- Merge to upstream
- Fix makefile line
Resolves: #208838

* Fri Nov 24 2006 Dan Walsh <dwalsh@redhat.com> 1.33.4-2
- Additional po changes
- Added all booleans definitions

* Wed Nov 22 2006 Dan Walsh <dwalsh@redhat.com> 1.33.4-1
- Upstream accepted my patches
        * Merged setsebool patch from Karl MacMillan.
          This fixes a bug reported by Yuichi Nakamura with
          always setting booleans persistently on an unmanaged system.

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 1.33.2-2
- Fixes for the gui

* Mon Nov 20 2006 Dan Walsh <dwalsh@redhat.com> 1.33.2-1
- Upstream accepted my patches

* Fri Nov 17 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-9
- Add Amy Grifis Patch to preserve newrole exit status

* Thu Nov 16 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-8
- Fix display of gui

* Thu Nov 16 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-7
- Add patch by Jose Plans to make run_init use pam_acct_mgmt

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-6
- More fixes to gui

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-5
- Fix audit2allow to generate referene policy

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-4
- Add group sort for portsPage.py
- Add enable/disableaudit to modules page

* Wed Nov 15 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-3
- Add glade file

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-2
- Fix Module handling in system-config-selinux

* Tue Nov 14 2006 Dan Walsh <dwalsh@redhat.com> 1.33.1-1
- Update to upstream
        * Merged newrole patch set from Michael Thompson.
- Add policycoreutils-gui

* Thu Nov 9 2006 Dan Walsh <dwalsh@redhat.com> 1.32-3
- No longer requires rhpl

* Mon Nov 6 2006 Dan Walsh <dwalsh@redhat.com> 1.32-2
- Fix genhomedircon man page

* Mon Oct 9 2006 Dan Walsh <dwalsh@redhat.com> 1.32-1
- Add newrole audit patch from sgrubb
- Update to upstream
        * Merged audit2allow -l fix from Yuichi Nakamura.
        * Merged restorecon -i and -o - support from Karl MacMillan.
        * Merged semanage/seobject fix from Dan Walsh.
        * Merged fixfiles -R and verify changes from Dan Walsh.

* Fri Oct 6 2006 Dan Walsh <dwalsh@redhat.com> 1.30.30-2
- Separate out newrole into its own package

* Fri Sep 29 2006 Dan Walsh <dwalsh@redhat.com> 1.30.30-1
- Update to upstream
        * Merged newrole auditing of failures due to user actions from
          Michael Thompson.

* Thu Sep 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-6
- Pass -i qualifier to restorecon  for fixfiles -R
- Update translations

* Thu Sep 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-5
- Remove recursion from fixfiles -R calls
- Fix semanage to verify prefix

* Thu Sep 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-4
- More translations
- Compile with -pie

* Mon Sep 18 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-3
- Add translations
- Fix audit2allow -l

* Thu Sep 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-2
- Rebuild

* Thu Sep 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.29-1
- Update to upstream
- Change -o to take "-" for stdout

* Wed Sep 13 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-9
- Add -h support for genhomedircon

* Wed Sep 13 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-8
- Fix fixfiles handling of -o

* Mon Sep 11 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-7
- Make restorecon return the number of changes files if you use the -n flag

* Fri Sep 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-6
- Change setfiles and restorecon to use stderr except for -o flag
- Also -o flag will now output files

* Thu Sep 7 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-5
- Put back Erich's change

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-4
- Remove recursive switch when using rpm

* Wed Sep 6 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-3
- Fix fixfiles to handle multiple rpm and make -o work

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-2
- Apply patch

* Fri Sep 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.28-1
- Security fixes to run python in a more locked down manner
- More Translations
- Update to upstream
        * Merged fix for restorecon // handling from Erich Schubert.
        * Merged translations update and fixfiles fix from Dan Walsh.

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-5
- Change scripts to use /usr/sbin/python

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-4
- Add -i qualified to restorecon to tell it to ignore files that do not exist
- Fixfiles also modified for this change

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-3
- Ignore sigpipe

* Thu Aug 31 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-2
- Fix init script and add translations

* Thu Aug 24 2006 Dan Walsh <dwalsh@redhat.com> 1.30.27-1
- Update to upstream
        * Merged fix for restorecon symlink handling from Erich Schubert.

* Sat Aug 12 2006 Dan Walsh <dwalsh@redhat.com> 1.30.26-1
- Update to upstream
        * Merged semanage local file contexts patch from Chris PeBenito.
- Fix fixfiles log creation
- More translations

* Thu Aug 3 2006 Dan Walsh <dwalsh@redhat.com> 1.30.25-1
- Update to upstream
        * Merged patch from Dan Walsh with:
                * audit2allow: process MAC_POLICY_LOAD events
                * newrole: run shell with - prefix to start a login shell
                * po: po file updates
                * restorecond: bail if SELinux not enabled
                * fixfiles: omit -q
                * genhomedircon:  fix exit code if non-root
                * semodule_deps:  install man page
        * Merged secon Makefile fix from Joshua Brindle.
        * Merged netfilter contexts support patch from Chris PeBenito.

* Wed Aug 2 2006 Dan Walsh <dwalsh@redhat.com> 1.30.22-3
- Fix audit2allow to handle reload of policy

* Wed Aug 2 2006 Dan Walsh <dwalsh@redhat.com> 1.30.22-2
- Stop restorecond init script when selinux is not enabled

* Tue Aug 1 2006 Dan Walsh <dwalsh@redhat.com> 1.30.22-1
- Update to upstream
        * Merged restorecond size_t fix from Joshua Brindle.
        * Merged secon keycreate patch from Michael LeMay.
        * Merged restorecond fixes from Dan Walsh.
          Merged updated po files from Dan Walsh.
        * Merged python gettext patch from Stephen Bennett.
        * Merged semodule_deps from Karl MacMillan.

* Thu Jul 27 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-7
- Change newrole to exec a login shell to prevent suspend.

* Fri Jul 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-6
- Report error when selinux not enabled in restorecond

* Tue Jul 18 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-5
- Fix handling of restorecond

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-4
- Fix creation of restorecond pidfile

* Mon Jul 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-3
- Update translations
- Update to new GCC

* Mon Jul 10 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-2
- Add verbose flag to restorecond and update translations

* Tue Jul 4 2006 Dan Walsh <dwalsh@redhat.com> 1.30.17-1
- Update to upstream
        * Lindent.
        * Merged patch from Dan Walsh with:
          * -p option (progress) for setfiles and restorecon.
          * disable context translation for setfiles and restorecon.
          * on/off values for setsebool.
        * Merged setfiles and semodule_link fixes from Joshua Brindle.

* Thu Jun 22 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-5
- Add progress indicator on fixfiles/setfiles/restorecon

* Wed Jun 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-4
- Don't use translations with matchpathcon

* Tue Jun 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-3
- Prompt for selinux-policy-devel package in audit2allow

* Mon Jun 19 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-2
- Allow setsebool to use on/off
- Update translations

* Fri Jun 16 2006 Dan Walsh <dwalsh@redhat.com> 1.30.14-1
- Update to upstream
        * Merged fix for setsebool error path from Serge Hallyn.
        * Merged patch from Dan Walsh with:
        *    Updated po files.
        *    Fixes for genhomedircon and seobject.
        *    Audit message for mass relabel by setfiles.

* Tue Jun 13 2006 James Antill <jantill@redhat.com> 1.30.12-5
- Update audit mass relabel to only compile in when audit is installed.

* Mon Jun 12 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-4
- Update to required versions
- Update translation

* Wed Jun 7 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-3
- Fix shell selection

* Mon Jun 5 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-2
- Add BuildRequires for gettext

* Mon Jun 5 2006 Dan Walsh <dwalsh@redhat.com> 1.30.12-1
        * Updated fixfiles script for new setfiles location in /sbin.

* Tue May 30 2006 Dan Walsh <dwalsh@redhat.com> 1.30.11-1
- Update to upstream
        * Merged more translations from Dan Walsh.
        * Merged patch to relocate setfiles to /sbin for early relabel
          when /usr might not be mounted from Dan Walsh.
        * Merged semanage/seobject patch to preserve fcontext ordering in list.
        * Merged secon patch from James Antill.

* Fri May 26 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-4
- Fix seobject.py to not sort the file_context file.
- move setfiles to /sbin

* Wed May 24 2006 James Antill <jantill@redhat.com> 1.30.10-3
- secon man page and getopt fixes.
- Enable mass relabel audit, even though it doesn't work.

* Wed May 24 2006 James Antill <jantill@redhat.com> 1.30.10-2
- secon fixes for --self-exec etc.
- secon change from level => sensitivity, add clearance.
- Add mass relabel AUDIT patch, but disable it until kernel problem solved.

* Tue May 23 2006 Dan Walsh <dwalsh@redhat.com> 1.30.10-1
- Update to upstream
        * Merged patch with updates to audit2allow, secon, genhomedircon,
          and semanage from Dan Walsh.

* Sat May 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30.9-4
- Fix exception in genhomedircon

* Mon May 15 2006 James Antill <jantill@redhat.com> 1.30.9-3
- Add rhpl dependancy

* Mon May 15 2006 James Antill <jantill@redhat.com> 1.30.9-2
- Add secon man page and prompt options.

* Mon May 15 2006 Dan Walsh <dwalsh@redhat.com> 1.30.9-1
- Update to upstream
        * Fixed audit2allow and po Makefiles for DESTDIR= builds.
        * Merged .po file patch from Dan Walsh.
        * Merged bug fix for genhomedircon.

* Wed May 10 2006 Dan Walsh <dwalsh@redhat.com> 1.30.8-2
- Fix exception on bad file_context

* Mon May 8 2006 Dan Walsh <dwalsh@redhat.com> 1.30.8-1
- Update to upstream
        * Merged fix warnings patch from Karl MacMillan.
        * Merged patch from Dan Walsh.
          This includes audit2allow changes for analysis plugins,
          internationalization support for several additional programs
          and added po files, some fixes for semanage, and several cleanups.
          It also adds a new secon utility.

* Sun May 7 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-5
- Fix genhomedircon to catch duplicate homedir problem

* Thu May 4 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-4
- Add secon program
- Add translations

* Thu Apr 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-3
- Fix check for "msg"

* Mon Apr 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-2
- Ship avc.py

* Fri Apr 14 2006 Dan Walsh <dwalsh@redhat.com> 1.30.6-1
- Add /etc/samba/secrets.tdb to restorecond.conf
- Update from upstream
        * Merged semanage prefix support from Russell Coker.
        * Added a test to setfiles to check that the spec file is
          a regular file.

* Thu Apr 06 2006 Karsten Hopp <karsten@redhat.de> 1.30.4-4
- added some missing buildrequires
- added Requires: initscripts for /sbin/service

* Thu Apr 06 2006 Karsten Hopp <karsten@redhat.de> 1.30.4-3
- use absolute path /sbin/service

* Wed Apr 5 2006 Dan Walsh <dwalsh@redhat.com> 1.30.4-2
- Fix audit2allow to not require ausearch.
- Fix man page
- Add libflashplayer to restorecond.conf

* Wed Mar 29 2006 Dan Walsh <dwalsh@redhat.com> 1.30.4-1
- Update from upstream
        * Merged audit2allow fixes for refpolicy from Dan Walsh.
        * Merged fixfiles patch from Dan Walsh.
        * Merged restorecond daemon from Dan Walsh.
        * Merged semanage non-MLS fixes from Chris PeBenito.
        * Merged semanage and semodule man page examples from Thomas Bleher.

* Tue Mar 28 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-4
- Clean up reference policy generation in audit2allow

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-3
- Add IN_MOVED_TO to catch renames

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-2
- make restorecond only ignore non directories with lnk > 1

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30.1-1
- Make audit2allow translate dontaudit as well as allow rules
- Update from upstream
        * Merged semanage labeling prefix patch from Ivan Gyurdiev.

* Tue Mar 21 2006 Dan Walsh <dwalsh@redhat.com> 1.30-5
- Fix audit2allow to retrieve dontaudit rules

* Mon Mar 20 2006 Dan Walsh <dwalsh@redhat.com> 1.30-4
- Open file descriptor to make sure file does not change from underneath.

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30-3
- Fixes for restorecond attack via symlinks
- Fixes for fixfiles

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30-2
- Restorecon has to handle suspend/resume

* Fri Mar 17 2006 Dan Walsh <dwalsh@redhat.com> 1.30-1
- Update to upstream

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.27-1
- Add restorecond

* Fri Mar 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-6
- Remove prereq

* Mon Mar 6 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-5
- Fix audit2allow to generate all rules

* Fri Mar 3 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-4
- Minor fixes to chcat and semanage

* Fri Feb 24 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-3
- Add missing setsebool man page

* Thu Feb 23 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-2
- Change audit2allow to use devel instead of refpolicy

* Mon Feb 20 2006 Dan Walsh <dwalsh@redhat.com> 1.29.26-1
- Update from upstream
        * Merged semanage bug fix patch from Ivan Gyurdiev.
        * Merged improve bindings patch from Ivan Gyurdiev.
        * Merged semanage usage patch from Ivan Gyurdiev.
        * Merged use PyList patch from Ivan Gyurdiev.

* Mon Feb 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.23-1
- Update from upstream
        * Merged newrole -V/--version support from Glauber de Oliveira Costa.
        * Merged genhomedircon prefix patch from Dan Walsh.
        * Merged optionals in base patch from Joshua Brindle.

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.29.20-2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Dan Walsh <dwalsh@redhat.com> 1.29.20-2
- Fix auditing to semanage
- Change genhomedircon to use new prefix interface in libselinux

* Tue Feb 07 2006 Dan Walsh <dwalsh@redhat.com> 1.29.20-1
- Update from upstream
        * Merged seuser/user_extra support patch to semodule_package
          from Joshua Brindle.
        * Merged getopt type fix for semodule_link/expand and sestatus
          from Chris PeBenito.
- Fix genhomedircon output

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.29.18-2.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Feb 3 2006 Dan Walsh <dwalsh@redhat.com> 1.29.18-2
- Add auditing to semanage

* Thu Feb 2 2006 Dan Walsh <dwalsh@redhat.com> 1.29.18-1
- Update from upstream
        * Merged clone record on set_con patch from Ivan Gyurdiev.

* Mon Jan 30 2006 Dan Walsh <dwalsh@redhat.com> 1.29.17-1
- Update from upstream
        * Merged genhomedircon fix from Dan Walsh.
        * Merged seusers.system patch from Ivan Gyurdiev.
        * Merged improve port/fcontext API patch from Ivan Gyurdiev.
        * Merged genhomedircon patch from Dan Walsh.

* Fri Jan 27 2006 Dan Walsh <dwalsh@redhat.com> 1.29.15-1
- Update from upstream
        * Merged newrole audit patch from Steve Grubb.
        * Merged seuser -> seuser local rename patch from Ivan Gyurdiev.
        * Merged semanage and semodule access check patches from Joshua Brindle.

* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.12-1
- Add a default of /export/home

* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.11-3
- Cleanup of the patch

* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.11-2
- Correct handling of symbolic links in restorecon

* Wed Jan 25 2006 Dan Walsh <dwalsh@redhat.com> 1.29.11-1
- Added translation support to semanage
- Update from upstream
        * Modified newrole and run_init to use the loginuid when
          supported to obtain the Linux user identity to re-authenticate,
          and to fall back to real uid.  Dropped the use of the SELinux
          user identity, as Linux users are now mapped to SELinux users
          via seusers and the SELinux user identity space is separate.
        * Merged semanage bug fixes from Ivan Gyurdiev.
        * Merged semanage fixes from Russell Coker.
        * Merged chcat.8 and genhomedircon patches from Dan Walsh.

* Thu Jan 19 2006 Dan Walsh <dwalsh@redhat.com> 1.29.9-2
- Fix genhomedircon to work on MLS policy

* Thu Jan 19 2006 Dan Walsh <dwalsh@redhat.com> 1.29.9-1
- Update to match NSA
        * Merged chcat, semanage, and setsebool patches from Dan Walsh.

* Thu Jan 19 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-4
- Fixes for "add"-"modify" error messages
- Fixes for chcat

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-3
- Add management of translation file to semaange and seobject

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-2
- Fix chcat -l -L to work while not root

* Wed Jan 18 2006 Dan Walsh <dwalsh@redhat.com> 1.29.8-1
- Update to match NSA
        * Merged semanage fixes from Ivan Gyurdiev.
        * Merged semanage fixes from Russell Coker.
        * Merged chcat, genhomedircon, and semanage diffs from Dan Walsh.

* Tue Jan 17 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-4
- Update chcat to manage user categories also

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-3
- Add check for root for semanage, genhomedircon

* Sat Jan 14 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-2
- Add ivans patch

* Fri Jan 13 2006 Dan Walsh <dwalsh@redhat.com> 1.29.7-1
- Update to match NSA
        * Merged newrole cleanup patch from Steve Grubb.
        * Merged setfiles/restorecon performance patch from Russell Coker.
        * Merged genhomedircon and semanage patches from Dan Walsh.
        * Merged remove add_local/set_local patch from Ivan Gyurdiev.

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-3
- Fixes for mls policy

* Tue Jan 10 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-2
- Update semanage and split out seobject
- Fix labeleing of home_root

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.29.5-1
- Update to match NSA
        * Added filename to semodule error reporting.

* Thu Jan 5 2006 Dan Walsh <dwalsh@redhat.com> 1.29.4-1
- Update to match NSA
        * Merged genhomedircon and semanage patch from Dan Walsh.
        * Changed semodule error reporting to include argv[0].

* Wed Jan 4 2006 Dan Walsh <dwalsh@redhat.com> 1.29.3-1
- Update to match NSA
        * Merged semanage getpwnam bug fix from Serge Hallyn (IBM).
        * Merged patch series from Ivan Gyurdiev.
          This includes patches to:
          - cleanup setsebool
          - update setsebool to apply active booleans through libsemanage
          - update semodule to use the new semanage_set_rebuild() interface
          - fix various bugs in semanage
        * Merged patch from Dan Walsh (Red Hat).
          This includes fixes for restorecon, chcat, fixfiles, genhomedircon,
          and semanage.

* Mon Jan 2 2006 Dan Walsh <dwalsh@redhat.com> 1.29.2-10
- Fix restorecon to not say it is changing user section when -vv is specified

* Tue Dec 27 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-9
- Fixes for semanage, patch from Ivan and added a test script

* Sat Dec 24 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-8
- Fix getpwnam call

* Fri Dec 23 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-7
- Anaconda fixes

* Thu Dec 22 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-6
- Turn off try catch block to debug anaconda failure

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-5
- More fixes for chcat

* Tue Dec 20 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-4
- Add try catch for files that may not exists

* Mon Dec 19 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-3
- Remove commands from genhomedircon for installer

* Wed Dec 14 2005 Dan Walsh <dwalsh@redhat.com> 1.29.2-1
- Fix genhomedircon to work in installer
- Update to match NSA
        * Merged patch for chcat script from Dan Walsh.

* Fri Dec 9 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-2
- More fixes to chcat

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 8 2005 Dan Walsh <dwalsh@redhat.com> 1.29.1-1
- Update to match NSA
        * Merged fix for audit2allow long option list from Dan Walsh.
        * Merged -r option for restorecon (alias for -R) from Dan Walsh.
        * Merged chcat script and man page from Dan Walsh.

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.28-1
- Update to match NSA
- Add gfs support

* Wed Dec 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.37-1
- Update to match NSA
- Add chcat to policycoreutils, adding +/- syntax
`

* Tue Dec 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.36-2
- Require new version of libsemanage

* Mon Dec 5 2005 Dan Walsh <dwalsh@redhat.com> 1.27.36-1
- Update to match NSA
        * Changed genhomedircon to warn on use of ROLE in homedir_template
          if using managed policy, as libsemanage does not yet support it.

* Sun Dec 4 2005 Dan Walsh <dwalsh@redhat.com> 1.27.35-1
- Update to match NSA
        * Merged genhomedircon bug fix from Dan Walsh.
        * Revised semodule* man pages to refer to checkmodule and
          to include example sections.

* Thu Dec 1 2005 Dan Walsh <dwalsh@redhat.com> 1.27.33-1
- Update to match NSA
        * Merged audit2allow --tefile and --fcfile support from Dan Walsh.
        * Merged genhomedircon fix from Dan Walsh.
        * Merged semodule* man pages from Dan Walsh, and edited them.
        * Changed setfiles to set the MATCHPATHCON_VALIDATE flag to
          retain validation/canonicalization of contexts during init.

* Wed Nov 30 2005 Dan Walsh <dwalsh@redhat.com> 1.27.31-1
- Update to match NSA
        * Changed genhomedircon to always use user_r for the role in the
          managed case since user_get_defrole is broken.
- Add te file capabilities to audit2allow
- Add man pages for semodule

* Tue Nov 29 2005 Dan Walsh <dwalsh@redhat.com> 1.27.30-1
- Update to match NSA
        * Merged sestatus, audit2allow, and semanage patch from Dan Walsh.
        * Fixed semodule -v option.

* Mon Nov 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.29-1
- Update to match NSA
        * Merged audit2allow python script from Dan Walsh.
          (old script moved to audit2allow.perl, will be removed later).
        * Merged genhomedircon fixes from Dan Walsh.
        * Merged semodule quieting patch from Dan Walsh
          (inverts default, use -v to restore original behavior).

* Thu Nov 17 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-3
- Audit2allow
        * Add more error checking
        * Add gen policy package
        * Add gen requires

* Wed Nov 16 2005 Dan Walsh <dwalsh@redhat.com> 1.27.28-2
- Update to match NSA
        * Merged genhomedircon rewrite from Dan Walsh.
- Rewrite audit2allow to python

* Mon Nov 14 2005 Dan Walsh <dwalsh@redhat.com> 1.27.27-5
- Fix genhomedircon to work with non libsemanage systems

* Fri Nov 11 2005 Dan Walsh <dwalsh@redhat.com> 1.27.27-3
- Patch genhomedircon to use libsemanage.py stuff

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.27.27-1
- Update to match NSA
        * Merged setsebool cleanup patch from Ivan Gyurdiev.

* Wed Nov 9 2005 Dan Walsh <dwalsh@redhat.com> 1.27.26-4
- Fix genhomedircon to use seusers file, temporary fix until swigified semanage

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.26-1
        * Added -B (--build) option to semodule to force a rebuild.
        * Reverted setsebool patch to call semanage_set_reload_bools().
        * Changed setsebool to disable policy reload and to call
          security_set_boolean_list to update the runtime booleans.
        * Changed setfiles -c to use new flag to set_matchpathcon_flags()
          to disable context translation by matchpathcon_init().

* Tue Nov 8 2005 Dan Walsh <dwalsh@redhat.com> 1.27.23-1
- Update to match NSA
        * Changed setfiles for the context canonicalization support.
        * Changed setsebool to call semanage_is_managed() interface
          and fall back to security_set_boolean_list() if policy is
          not managed.
        * Merged setsebool memory leak fix from Ivan Gyurdiev.
        * Merged setsebool patch to call semanage_set_reload_bools()
          interface from Ivan Gyurdiev.

* Mon Nov 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.20-1
- Update to match NSA
        * Merged setsebool patch from Ivan Gyurdiev.
          This moves setsebool from libselinux/utils to policycoreutils,
          and rewrites it to use libsemanage for permanent boolean changes.

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.19-2
- Rebuild to use latest libselinux, libsemanage, and libsepol

* Tue Oct 25 2005 Dan Walsh <dwalsh@redhat.com> 1.27.19-1
- Update to match NSA
        * Merged semodule support for reload, noreload, and store options
          from Joshua Brindle.
        * Merged semodule_package rewrite from Joshua Brindle.

* Thu Oct 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.18-1
- Update to match NSA
        * Cleaned up usage and error messages and releasing of memory by
        semodule utilities.
        * Corrected error reporting by semodule.
        * Updated semodule_expand for change to sepol interface.
        * Merged fixes for make DESTDIR= builds from Joshua Brindle.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.27.14-1
- Update to match NSA
        * Updated semodule_package for sepol interface changes.

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 1.27.13-1
- Update to match NSA
        * Updated semodule_expand/link for sepol interface changes.

* Sat Oct 15 2005 Dan Walsh <dwalsh@redhat.com> 1.27.12-1
- Update to match NSA
        * Merged non-PAM Makefile support for newrole and run_init from Timothy Wood.

* Fri Oct 14 2005 Dan Walsh <dwalsh@redhat.com> 1.27.11-1
- Update to match NSA
        * Updated semodule_expand to use get interfaces for hidden sepol_module_package type.
        * Merged newrole and run_init pam config patches from Dan Walsh (Red Hat).
        * Merged fixfiles patch from Dan Walsh (Red Hat).
        * Updated semodule for removal of semanage_strerror.

* Thu Oct 13 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-2
- Fix run_init.pamd and spec file

* Wed Oct 12 2005 Dan Walsh <dwalsh@redhat.com> 1.27.7-1
- Update to match NSA
        * Updated semodule_link and semodule_expand to use shared libsepol.
        Fixed audit2why to call policydb_init prior to policydb_read (still
        uses the static libsepol).

* Mon Oct 10 2005 Dan Walsh <dwalsh@redhat.com> 1.27.6-1
- Update to match NSA
        * Updated for changes to libsepol.
        Changed semodule and semodule_package to use the shared libsepol.
        Disabled build of semodule_link and semodule_expand for now.
        Updated audit2why for relocated policydb internal headers,
        still needs to be converted to a shared lib interface.

* Fri Oct 7 2005 Dan Walsh <dwalsh@redhat.com> 1.27.5-3
- Update newrole pam file to remove pam-stack
- Update run_init pam file to remove pam-stack

* Thu Oct 6 2005 Dan Walsh <dwalsh@redhat.com> 1.27.5-1
- Update to match NSA
        * Fixed warnings in load_policy.
        * Rewrote load_policy to use the new selinux_mkload_policy()
        interface provided by libselinux.

* Wed Oct 5 2005 Dan Walsh <dwalsh@redhat.com> 1.27.3-2
- Rebuild with newer libararies

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.3-1
- Update to match NSA
        * Merged patch to update semodule to the new libsemanage API
        and improve the user interface from Karl MacMillan (Tresys).
        * Modified semodule for the create/connect API split.

* Wed Sep 28 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-2
- More fixes to stop find from following nfs paths

* Wed Sep 21 2005 Dan Walsh <dwalsh@redhat.com> 1.27.2-1
- Update to match NSA
        * Merged run_init open_init_pty bug fix from Manoj Srivastava
          (unblock SIGCHLD).  Bug reported by Erich Schubert.

* Tue Sep 20 2005 Dan Walsh <dwalsh@redhat.com> 1.27.1-1
- Update to match NSA
        * Merged error shadowing bug fix for restorecon from Dan Walsh.
        * Merged setfiles usage/man page update for -r option from Dan Walsh.
        * Merged fixfiles -C patch to ignore :s0 addition on update
          to a MCS/MLS policy from Dan Walsh.

* Thu Sep 15 2005 Dan Walsh <dwalsh@redhat.com> 1.26-3
- Add chcat script for use with chcon.

* Tue Sep 13 2005 Dan Walsh <dwalsh@redhat.com> 1.26-2
- Fix restorecon to exit with error code

* Mon Sep 12 2005 Dan Walsh <dwalsh@redhat.com> 1.26-1
        * Updated version for release.

* Tue Sep 6 2005 Dan Walsh <dwalsh@redhat.com> 1.25.9-2
- Add prereq for mount command

* Thu Sep 1 2005 Dan Walsh <dwalsh@redhat.com> 1.25.9-1
- Update to match NSA
        * Changed setfiles -c to translate the context to raw format
        prior to calling libsepol.

* Fri Aug 26 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-3
- Use new version of libsemange and require it for install

* Fri Aug 26 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-2
- Ignore s0 in file context

* Thu Aug 25 2005 Dan Walsh <dwalsh@redhat.com> 1.25.7-1
- Update to match NSA
        * Merged patch for fixfiles -C from Dan Walsh.

* Tue Aug 23 2005 Dan Walsh <dwalsh@redhat.com> 1.25.6-1
- Update to match NSA
        * Merged fixes for semodule_link and sestatus from Serge Hallyn (IBM).
          Bugs found by Coverity.

* Mon Aug 22 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-3
- Fix fixfiles to call sort -u followed by sort -d.

* Wed Aug 17 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-2
- Change fixfiles to ignore /home directory on updates

* Fri Aug 5 2005 Dan Walsh <dwalsh@redhat.com> 1.25.5-1
- Update to match NSA
        * Merged patch to move module read/write code from libsemanage
          to libsepol from Jason Tang (Tresys).

* Thu Jul 28 2005 Dan Walsh <dwalsh@redhat.com> 1.25.4-1
- Update to match NSA
        * Changed semodule* to link with libsemanage.

* Wed Jul 27 2005 Dan Walsh <dwalsh@redhat.com> 1.25.3-1
- Update to match NSA
        * Merged restorecon patch from Ivan Gyurdiev.

* Mon Jul 18 2005 Dan Walsh <dwalsh@redhat.com> 1.25.2-1
- Update to match NSA
        * Merged load_policy, newrole, and genhomedircon patches from Red Hat.

* Thu Jul 7 2005 Dan Walsh <dwalsh@redhat.com> 1.25.1-1
- Update to match NSA
        * Merged loadable module support from Tresys Technology.

* Wed Jun 29 2005 Dan Walsh <dwalsh@redhat.com> 1.24-1
- Update to match NSA
        * Updated version for release.

* Tue Jun 14 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-4
- Fix Ivan's patch for user role changes

* Sat May 28 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-3
- Add Ivan's patch for user role changes in genhomedircon

* Thu May 26 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-2
- Fix warning message on reload of booleans

* Fri May 20 2005 Dan Walsh <dwalsh@redhat.com> 1.23.11-1
- Update to match NSA
        * Merged fixfiles and newrole patch from Dan Walsh.
        * Merged audit2why man page from Dan Walsh.

* Thu May 19 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-2
- Add call to pam_acct_mgmt in newrole.

* Tue May 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.10-1
- Update to match NSA
        * Extended audit2why to incorporate booleans and local user
          settings when analyzing audit messages.

* Mon May 16 2005 Dan Walsh <dwalsh@redhat.com> 1.23.9-1
- Update to match NSA
        * Updated audit2why for sepol_ prefixes on Flask types to
          avoid namespace collision with libselinux, and to
          include <selinux/selinux.h> now.

* Fri May 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.8-1
- Fix fixfiles to accept -f
- Update to match NSA
        * Added audit2why utility.

* Fri Apr 29 2005 Dan Walsh <dwalsh@redhat.com> 1.23.7-1
- Change -f flag in fixfiles to remove stuff from /tmp
- Change -F flag to pass -F flag  to restorecon/fixfiles.  (IE Force relabel).

* Thu Apr 14 2005 Dan Walsh <dwalsh@redhat.com> 1.23.6-1
- Update to match NSA
        * Fixed signed/unsigned pointer bug in load_policy.
        * Reverted context validation patch for genhomedircon.

* Wed Apr 13 2005 Dan Walsh <dwalsh@redhat.com> 1.23.5-1
- Update to match NSA
        * Reverted load_policy is_selinux_enabled patch from Dan Walsh.
          Otherwise, an initial policy load cannot be performed using
          load_policy, e.g. for anaconda.

* Mon Apr 11 2005 Dan Walsh <dwalsh@redhat.com> 1.23.4-3
- remove is_selinux_enabled check from load_policy  (Bad idea)

* Mon Apr 11 2005 Dan Walsh <dwalsh@redhat.com> 1.23.4-1
- Update to version from NSA
        * Merged load_policy is_selinux_enabled patch from Dan Walsh.
        * Merged restorecon verbose output patch from Dan Walsh.
        * Merged setfiles altroot patch from Chris PeBenito.

* Thu Apr 7 2005 Dan Walsh <dwalsh@redhat.com> 1.23.3-2
- Don't run load_policy on a non SELinux kernel.

* Wed Apr 6 2005 Dan Walsh <dwalsh@redhat.com> 1.23.3-1
- Update to version from NSA
        * Merged context validation patch for genhomedircon from Eric Paris.
- Fix verbose output of restorecon

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 1.23.2-1
- Update to version from NSA
        * Changed setfiles -c to call set_matchpathcon_flags(3) to
          turn off processing of .homedirs and .local.

* Tue Mar 15 2005 Dan Walsh <dwalsh@redhat.com> 1.23.1-1
- Update to released version from NSA
        * Merged rewrite of genhomedircon by Eric Paris.
        * Changed fixfiles to relabel jfs since it now supports security xattrs
          (as of 2.6.11).  Removed reiserfs until 2.6.12 is released with
          fixed support for reiserfs and selinux.

* Thu Mar 10 2005 Dan Walsh <dwalsh@redhat.com> 1.22-2
- Update to released version from NSA
- Patch genhomedircon to handle passwd in different places.

* Wed Mar 9 2005 Dan Walsh <dwalsh@redhat.com> 1.21.22-2
- Fix genhomedircon to not put bad userad error in file_contexts.homedir

* Tue Mar 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.22-1
- Cleanup error reporting

* Tue Mar 1 2005 Dan Walsh <dwalsh@redhat.com> 1.21.21-1
        * Merged load_policy and genhomedircon patch from Dan Walsh.

* Mon Feb 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.20-3
- Fix genhomedircon to add extr "\n"

* Fri Feb 25 2005 Dan Walsh <dwalsh@redhat.com> 1.21.20-2
- Fix genhomedircon to handle blank users

* Fri Feb 25 2005 Dan Walsh <dwalsh@redhat.com> 1.21.20-1
- Update to latest from NSA
- Add call to libsepol

* Thu Feb 24 2005 Dan Walsh <dwalsh@redhat.com> 1.21.19-4
- Fix genhomedircon to handle root
- Fix fixfiles to better handle file system types

* Wed Feb 23 2005 Dan Walsh <dwalsh@redhat.com> 1.21.19-2
- Fix genhomedircon to handle spaces in SELINUXPOLICYTYPE

* Tue Feb 22 2005 Dan Walsh <dwalsh@redhat.com> 1.21.19-1
- Update to latest from NSA
        * Merged several fixes from Ulrich Drepper.

* Mon Feb 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.18-2
- Apply Uli patch
        * The Makefiles should use the -Wall option even if compiled in beehive
        * Add -W, too
        * use -Werror when used outside of beehive.  This could also be used unconditionally
        * setfiles/setfiles.c: fix resulting warning
        * restorecon/restorecon.c: Likewise
        * run_init/open_init_pty.c: argc hasn't been checked, the program would crash if
called without parameters.  ignore the return value of nice properly.
        * run_init: don't link with -ldl lutil
        * load_policy: that's the bad bug.  pointer to unsigned int is passed, size_t is
written to.  fails on 64-bit archs
        * sestatus: signed vs unsigned problem
        * newrole: don't link with -ldl

* Sat Feb 19 2005 Dan Walsh <dwalsh@redhat.com> 1.21.18-1
- Update to latest from NSA
        * Changed load_policy to fall back to the original policy upon
          an error from sepol_genusers().

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.17-2
- Only restorecon on ext[23], reiser and xfs

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.17-1
- Update to latest from NSA
        * Merged new genhomedircon script from Dan Walsh.
        * Changed load_policy to call sepol_genusers().

* Thu Feb 17 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-9
- Remove Red Hat rhpl usage
- Add back in original syntax
- Update man page to match new syntax

* Fri Feb 11 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-8
- Fix genhomedircon regular expression
- Fix exclude in restorecon

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-5
- Trap failure on write
- Rewrite genhomedircon to generate file_context.homedirs
- several passes

* Thu Feb 10 2005 Dan Walsh <dwalsh@redhat.com> 1.21.15-1
- Update from NSA
        * Changed relabel Makefile target to use restorecon.

* Wed Feb 9 2005 Dan Walsh <dwalsh@redhat.com> 1.21.14-1
- Update from NSA
        * Merged restorecon patch from Dan Walsh.

* Tue Feb 8 2005 Dan Walsh <dwalsh@redhat.com> 1.21.13-1
- Update from NSA
        * Merged further change to fixfiles -C from Dan Walsh.
        * Merged updated fixfiles script from Dan Walsh.
- Fix error handling of restorecon

* Mon Feb 7 2005 Dan Walsh <dwalsh@redhat.com> 1.21.12-2
- Fix sestatus for longer booleans

* Wed Feb 2 2005 Dan Walsh <dwalsh@redhat.com> 1.21.12-1
- More cleanup of fixfiles sed patch
        * Merged further patches for restorecon/setfiles -e and fixfiles -C.

* Wed Feb 2 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-2
- More cleanup of fixfiles sed patch

* Mon Jan 31 2005 Dan Walsh <dwalsh@redhat.com> 1.21.10-1
- More cleanup of fixfiles sed patch
- Upgrade to latest from NSA
        * Merged patch for open_init_pty from Manoj Srivastava.

* Fri Jan 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.9-1
- More cleanup of sed patch
- Upgrade to latest from NSA
        * Merged updated fixfiles script from Dan Walsh.
        * Merged updated man page for fixfiles from Dan Walsh and re-added unzipped.
        * Reverted fixfiles patch for file_contexts.local;
          obsoleted by setfiles rewrite.
        * Merged error handling patch for restorecon from Dan Walsh.
        * Merged semi raw mode for open_init_pty helper from Manoj Srivastava.
        * Rewrote setfiles to use matchpathcon and the new interfaces
          exported by libselinux (>= 1.21.5).

* Fri Jan 28 2005 Dan Walsh <dwalsh@redhat.com> 1.21.7-3
- Fix fixfiles patch
- Upgrade to latest from NSA
        * Prevent overflow of spec array in setfiles.
- Add diff comparason between file_contexts to fixfiles
- Allow restorecon to give an warning on file not found instead of exiting

* Thu Jan 27 2005 Dan Walsh <dwalsh@redhat.com> 1.21.5-1
- Upgrade to latest from NSA
        * Merged newrole -l support from Darrel Goeddel (TCS).
- Fix genhomedircon STARTING_UID

* Wed Jan 26 2005 Dan Walsh <dwalsh@redhat.com> 1.21.4-1
- Upgrade to latest from NSA
        * Merged fixfiles patch for file_contexts.local from Dan Walsh.

* Fri Jan 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.3-2
- Temp file needs to be created in /etc/selinux/POLICYTYPE/contexts/files/ directory.

* Fri Jan 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.3-1
- Upgrade to latest from NSA
        * Fixed restorecon to not treat errors from is_context_customizable()
          as a customizable context.
        * Merged setfiles/restorecon patch to not reset user field unless
          -F option is specified from Dan Walsh.
        * Merged open_init_pty helper for run_init from Manoj Srivastava.
        * Merged audit2allow and genhomedircon man pages from Manoj Srivastava.

* Fri Jan 21 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-3
- Don't change user componant if it is all that changed unless forced.
- Change fixfiles to concatinate file_context.local for setfiles

* Thu Jan 20 2005 Dan Walsh <dwalsh@redhat.com> 1.21.1-1
- Update to latest from NSA

* Mon Jan 10 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-2
- Fix restorecon segfault

* Mon Jan 3 2005 Dan Walsh <dwalsh@redhat.com> 1.20.1-1
- Update to latest from NSA
        * Merged fixfiles rewrite from Dan Walsh.
        * Merged restorecon patch from Dan Walsh.

* Mon Jan 3 2005 Dan Walsh <dwalsh@redhat.com> 1.19.3-1
- Update to latest from NSA
        * Merged fixfiles and restorecon patches from Dan Walsh.
        * Don't display change if only user part changed.

* Mon Jan 3 2005 Dan Walsh <dwalsh@redhat.com> 1.19.2-4
- Fix fixfiles handling of rpm
- Fix restorecon to not warn on symlinks unless -v -v
- Fix output of verbose to show old context as well as new context

* Wed Dec 29 2004 Dan Walsh <dwalsh@redhat.com> 1.19.2-1
- Update to latest from NSA
        * Changed restorecon to ignore ENOENT errors from matchpathcon.
        * Merged nonls patch from Chris PeBenito.

* Mon Dec 20 2004 Dan Walsh <dwalsh@redhat.com> 1.19.1-1
- Update to latest from NSA
        * Removed fixfiles.cron.
        * Merged run_init.8 patch from Dan Walsh.

* Thu Nov 18 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-3
- Fix run_init.8 to refer to correct location of initrc_context

* Wed Nov 3 2004 Dan Walsh <dwalsh@redhat.com> 1.18.1-1
- Upgrade to latest from NSA

* Wed Oct 27 2004 Steve Grubb <sgrubb@redhat.com> 1.17.7-3
- Add code to sestatus to output the current policy from config file

* Fri Oct 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.7-2
- Patch audit2allow to return self and no brackets if only one rule

* Fri Oct 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.7-1
- Update to latest from NSA
- Eliminate fixfiles.cron

* Tue Oct 12 2004 Dan Walsh <dwalsh@redhat.com> 1.17.6-2
- Only run fixfiles.cron once a week, and eliminate null message

* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.6-1
- Update with NSA
        * Added -l option to setfiles to log changes via syslog.
        * Merged -e option to setfiles to exclude directories.
        * Merged -R option to restorecon for recursive descent.

* Fri Oct 1 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-6
- Add -e (exclude directory) switch to setfiles
- Add syslog to setfiles

* Fri Sep 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-5
- Add -R (recursive) switch to restorecon.

* Thu Sep 23 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-4
- Change to only display to terminal if tty is specified

* Tue Sep 21 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-3
- Only display to stdout if logfile not specified

* Thu Sep 9 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-2
- Add Steve Grubb patch to cleanup log files.

* Mon Aug 30 2004 Dan Walsh <dwalsh@redhat.com> 1.17.5-1
- Add optargs
- Update to match NSA

* Wed Aug 25 2004 Dan Walsh <dwalsh@redhat.com> 1.17.4-1
- Add fix to get cdrom info from /proc/media in fixfiles.

* Wed Aug 25 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-4
- Add Steve Grub patches for
        * Fix fixfiles.cron MAILTO
        * Several problems in sestatus

* Wed Aug 25 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-3
- Add -q (quiet) qualifier to load_policy to not report warnings

* Tue Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-2
- Add requires for libsepol >= 1.1.1

* Tue Aug 24 2004 Dan Walsh <dwalsh@redhat.com> 1.17.3-1
- Update to latest from upstream

* Mon Aug 23 2004 Dan Walsh <dwalsh@redhat.com> 1.17.2-1
- Update to latest from upstream
- Includes Colin patch for verifying file_contexts

* Sun Aug 22 2004 Dan Walsh <dwalsh@redhat.com> 1.17.1-1
- Update to latest from upstream

* Mon Aug 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.7-1
- Update to latest from upstream

* Thu Aug 12 2004 Dan Walsh <dwalsh@redhat.com> 1.15.6-1
- Add Man page for load_policy

* Tue Aug 10 2004 Dan Walsh <dwalsh@redhat.com> 1.15.5-1
-  new version from NSA uses libsepol

* Mon Aug 2 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-2
- Fix genhomedircon join command

* Thu Jul 29 2004 Dan Walsh <dwalsh@redhat.com> 1.15.3-1
- Latest from NSA

* Mon Jul 26 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-4
- Change fixfiles to not change when running a check

* Tue Jul 20 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-3
- Fix restorecon getopt call to stop hang on IBM Arches

* Mon Jul 19 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-2
- Only mail files less than 100 lines from fixfiles.cron
- Add Russell's fix for genhomedircon

* Fri Jul 16 2004 Dan Walsh <dwalsh@redhat.com> 1.15.2-1
- Latest from NSA

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-2
- Add ro warnings

* Thu Jul 8 2004 Dan Walsh <dwalsh@redhat.com> 1.15.1-1
- Latest from NSA
- Fix fixfiles.cron to delete outfile

* Tue Jul 6 2004 Dan Walsh <dwalsh@redhat.com> 1.14.1-2
- Fix fixfiles.cron to not run on non SELinux boxes
- Fix several problems in fixfiles and fixfiles.cron

* Wed Jun 30 2004 Dan Walsh <dwalsh@redhat.com> 1.14.1-1
- Update from NSA
- Add cron capability to fixfiles

* Fri Jun 25 2004 Dan Walsh <dwalsh@redhat.com> 1.13.4-1
- Update from NSA

* Thu Jun 24 2004 Dan Walsh <dwalsh@redhat.com> 1.13.3-2
- Fix fixfiles to handle no rpm file on relabel

* Wed Jun 23 2004 Dan Walsh <dwalsh@redhat.com> 1.13.3-1
- Update latest from NSA
- Add -o option to setfiles to save output of any files with incorrect context.

* Tue Jun 22 2004 Dan Walsh <dwalsh@redhat.com> 1.13.2-2
- Add rpm support to fixfiles
- Update restorecon to add file input support

* Fri Jun 18 2004 Dan Walsh <dwalsh@redhat.com> 1.13.2-1
- Update with NSA Latest

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jun 12 2004 Dan Walsh <dwalsh@redhat.com> 1.13.1-2
- Fix run_init to use policy formats

* Wed Jun 2 2004 Dan Walsh <dwalsh@redhat.com> 1.13.1-1
- Update from NSA

* Tue May 25 2004 Dan Walsh <dwalsh@redhat.com> 1.13-3
- Change location of file_context file

* Tue May 25 2004 Dan Walsh <dwalsh@redhat.com> 1.13-2
- Change to use /etc/sysconfig/selinux to determine location of policy files

* Fri May 21 2004 Dan Walsh <dwalsh@redhat.com> 1.13-1
- Update to latest from NSA
- Change fixfiles to prompt before deleteing /tmp files

* Tue May 18 2004 Dan Walsh <dwalsh@redhat.com> 1.12-2
- have restorecon ingnore <<none>>
- Hand matchpathcon the file status

* Thu May 13 2004 Dan Walsh <dwalsh@redhat.com> 1.12-1
- Update to match NSA

* Mon May 10 2004 Dan Walsh <dwalsh@redhat.com> 1.11-4
- Move location of log file to /var/tmp

* Mon May 10 2004 Dan Walsh <dwalsh@redhat.com> 1.11-3
- Better grep command for bind

* Fri May 7 2004 Dan Walsh <dwalsh@redhat.com> 1.11-2
- Eliminate bind and context mounts

* Wed May 5 2004 Dan Walsh <dwalsh@redhat.com> 1.11-1
- update to match NSA

* Wed Apr 28 2004 Dan Walsh <dwalsh@redhat.com> 1.10-4
- Log fixfiles to the /tmp directory

* Wed Apr 21 2004 Colin Walters <walters@redhat.com> 1.10-3
- Add patch to fall back to authenticating via uid if
  the current user's SELinux user identity is the default
  identity
- Add BuildRequires pam-devel

* Mon Apr 12 2004 Dan Walsh <dwalsh@redhat.com> 1.10-2
- Add man page, thanks to Richard Halley

* Thu Apr 8 2004 Dan Walsh <dwalsh@redhat.com> 1.10-1
- Upgrade to latest from NSA

* Fri Apr 2 2004 Dan Walsh <dwalsh@redhat.com> 1.9.2-1
- Update with latest from gentoo and NSA

* Thu Apr 1 2004 Dan Walsh <dwalsh@redhat.com> 1.9.1-1
- Check return codes in sestatus.c

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-19
- Fix sestatus to not double free
- Fix sestatus.conf to be unix format

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-18
- Warn on setfiles failure to relabel.

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-17
- Updated version of sestatus

* Mon Mar 29 2004 Dan Walsh <dwalsh@redhat.com> 1.9-16
- Fix fixfiles to checklabel properly

* Fri Mar 26 2004 Dan Walsh <dwalsh@redhat.com> 1.9-15
- add sestatus

* Thu Mar 25 2004 Dan Walsh <dwalsh@redhat.com> 1.9-14
- Change free call to freecon
- Cleanup

* Tue Mar 23 2004 Dan Walsh <dwalsh@redhat.com> 1.9-12
- Remove setfiles-assoc patch
- Fix restorecon to not crash on missing dir

* Thu Mar 18 2004 Dan Walsh <dwalsh@redhat.com> 1.9-11
- Eliminate trailing / in restorecon

* Thu Mar 18 2004 Dan Walsh <dwalsh@redhat.com> 1.9-10
- Add Verbosity check

* Thu Mar 18 2004 Dan Walsh <dwalsh@redhat.com> 1.9-9
- Change restorecon to not follow symlinks.  It is too difficult and confusing
- to figure out the file context for the file pointed to by a symlink.

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-8
- Fix restorecon

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-7
- Read restorecon patch

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-6
- Change genhomedircon to take POLICYSOURCEDIR from command line

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-5
- Add checkselinux
- move fixfiles and restorecon to /sbin

* Wed Mar 17 2004 Dan Walsh <dwalsh@redhat.com> 1.9-4
- Restore patch of genhomedircon

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.9-3
- Add setfiles-assoc patch to try to freeup memory use

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.9-2
- Add fixlabels

* Mon Mar 15 2004 Dan Walsh <dwalsh@redhat.com> 1.9-1
- Update to latest from NSA

* Wed Mar 10 2004 Dan Walsh <dwalsh@redhat.com> 1.6-8
- Increase the size of buffer accepted by setfiles to BUFSIZ.

* Tue Mar 9 2004 Dan Walsh <dwalsh@redhat.com> 1.6-7
- genhomedircon should complete even if it can't read /etc/default/useradd

* Tue Mar 9 2004 Dan Walsh <dwalsh@redhat.com> 1.6-6
- fix restorecon to relabel unlabled files.

* Fri Mar 5 2004 Dan Walsh <dwalsh@redhat.com> 1.6-5
- Add genhomedircon from tresys
- Fixed patch for restorecon

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 1.6-4
- exit out when selinux is not enabled

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 1.6-3
- Fix minor bugs in restorecon

* Thu Feb 26 2004 Dan Walsh <dwalsh@redhat.com> 1.6-2
- Add restorecon c program

* Tue Feb 24 2004 Dan Walsh <dwalsh@redhat.com> 1.6-1
- Update to latest tarball from NSA

* Thu Feb 19 2004 Dan Walsh <dwalsh@redhat.com> 1.4-9
- Add sort patch

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 29 2004 Dan Walsh <dwalsh@redhat.com> 1.4-7
- remove mods to run_init since init scripts don't require it anymore

* Wed Jan 28 2004 Dan Walsh <dwalsh@redhat.com> 1.4-6
- fix genhomedircon not to return and error

* Wed Jan 28 2004 Dan Walsh <dwalsh@redhat.com> 1.4-5
- add setfiles quiet patch

* Tue Jan 27 2004 Dan Walsh <dwalsh@redhat.com> 1.4-4
- add checkcon to verify context match file_context

* Wed Jan 7 2004 Dan Walsh <dwalsh@redhat.com> 1.4-3
- fix command parsing restorecon

* Tue Jan 6 2004 Dan Walsh <dwalsh@redhat.com> 1.4-2
- Add restorecon

* Sat Dec 6 2003 Dan Walsh <dwalsh@redhat.com> 1.4-1
- Update to latest NSA 1.4

* Tue Nov 25 2003 Dan Walsh <dwalsh@redhat.com> 1.2-9
- Change run_init.console to run as run_init_t

* Tue Oct 14 2003 Dan Walsh <dwalsh@redhat.com> 1.2-8
- Remove dietcc since load_policy is not in mkinitrd
- Change to use CONSOLEHELPER flag

* Tue Oct 14 2003 Dan Walsh <dwalsh@redhat.com> 1.2-7
- Don't authenticate run_init when used with consolehelper

* Wed Oct 01 2003 Dan Walsh <dwalsh@redhat.com> 1.2-6
- Add run_init consolehelper link

* Wed Sep 24 2003 Dan Walsh <dwalsh@redhat.com> 1.2-5
- Add russell spead up patch to deal with file path stems

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 1.2-4
- Build load_policy with diet gcc in order to save space on initrd

* Fri Sep 12 2003 Dan Walsh <dwalsh@redhat.com> 1.2-3
- Update with NSA latest

* Thu Aug 7 2003 Dan Walsh <dwalsh@redhat.com> 1.2-1
- remove i18n
- Temp remove gtk support

* Thu Aug 7 2003 Dan Walsh <dwalsh@redhat.com> 1.1-4
- Remove wnck requirement

* Thu Aug 7 2003 Dan Walsh <dwalsh@redhat.com> 1.1-3
- Add gtk support to run_init

* Tue Aug 5 2003 Dan Walsh <dwalsh@redhat.com> 1.1-2
- Add internationalization

* Mon Jun 2 2003 Dan Walsh <dwalsh@redhat.com> 1.0-1
- Initial version
