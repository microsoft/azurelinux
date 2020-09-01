%global libauditver     3.0
%global libsepolver     2.9-1
%global libsemanagever  2.9-1
%global libselinuxver   2.9-1
%global sepolgenver     2.9
%global __python3	/usr/bin/python3
%global generatorsdir %{_prefix}/lib/systemd/system-generators

# Disable automatic compilation of Python files in extra directories
%global _python_bytecompile_extra 0

%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary: SELinux policy core utilities
Name:    policycoreutils
Version: 2.9
Release: 1%{?dist}
License: GPLv2
# https://github.com/SELinuxProject/selinux/wiki/Releases
Source0: https://github.com/SELinuxProject/selinux/releases/download/20190315/policycoreutils-2.9.tar.gz
Source1: https://github.com/SELinuxProject/selinux/releases/download/20190315/selinux-python-2.9.tar.gz
Source2: https://github.com/SELinuxProject/selinux/releases/download/20190315/semodule-utils-2.9.tar.gz
Source3: https://github.com/SELinuxProject/selinux/releases/download/20190315/restorecond-2.9.tar.gz
URL:     https://github.com/SELinuxProject/selinux
Source5: selinux-autorelabel
Source6: selinux-autorelabel.service
Source7: selinux-autorelabel-mark.service
Source8: selinux-autorelabel.target
Source9: selinux-autorelabel-generator.sh

Obsoletes: policycoreutils < 2.0.61-2
Conflicts: initscripts < 9.66
Provides: /sbin/fixfiles
Provides: /sbin/restorecon

BuildRequires: gcc
BuildRequires: pam-devel libsepol-devel >= %{libsepolver} libsemanage-devel >= %{libsemanagever} libselinux-devel >= %{libselinuxver}  libcap-devel audit-libs >=  %{libauditver} gettext
BuildRequires: audit-devel
BuildRequires: dbus-devel dbus-glib-devel
BuildRequires: python3-devel
BuildRequires: systemd
BuildRequires: git
Requires: util-linux grep gawk diffutils rpm sed
Requires: libsepol >= %{libsepolver} coreutils libselinux-utils >=  %{libselinuxver}

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

%prep -p /usr/bin/bash
# create selinux/ directory and extract sources
%autosetup -S git -N -c -n selinux
%autosetup -S git -N -T -D -a 1 -n selinux
%autosetup -S git -N -T -D -a 2 -n selinux
%autosetup -S git -N -T -D -a 3 -n selinux
#autosetup -S git -N -T -D -a 4 -n selinux
#autosetup -S git -N -T -D -a 5 -n selinux
#autosetup -S git -N -T -D -a 6 -n selinux

for i in *; do
    git mv $i ${i/-%{version}/}
    git commit -q --allow-empty -a --author 'rpm-build <rpm-build>' -m "$i -> ${i/-%{version}/}"
done

for i in selinux-*; do
    git mv $i ${i#selinux-}
    git commit -q --allow-empty -a --author 'rpm-build <rpm-build>' -m "$i -> ${i#selinux-}"
done

echo "G"

%build
%set_build_flags
export PYTHON=%{__python3}

make -C policycoreutils LSPP_PRIV=y SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C python SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C semodule-utils SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all
make -C restorecond SBINDIR="%{_sbindir}" LSPP_PRIV=y LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" all

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_mandir}/man5
mkdir -p %{buildroot}%{_mandir}/man8
%{__mkdir} -p %{buildroot}/%{_usr}/share/doc/%{name}/

make -C policycoreutils LSPP_PRIV=y  DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" SEMODULE_PATH="/usr/sbin" LIBSEPOLA="%{_libdir}/libsepol.a" install

make -C python PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install

make -C semodule-utils PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" install

make -C restorecond PYTHON=%{__python3} DESTDIR="%{buildroot}" SBINDIR="%{_sbindir}" LIBDIR="%{_libdir}" LIBSEPOLA="%{_libdir}/libsepol.a" SYSTEMDDIR="/lib/systemd" install

# Fix perms on newrole so that objcopy can process it
chmod 0755 %{buildroot}%{_bindir}/newrole

# Systemd
rm -rf %{buildroot}/%{_sysconfdir}/rc.d/init.d/restorecond

rm -f %{buildroot}/usr/share/man/ru/man8/genhomedircon.8.gz
rm -f %{buildroot}/usr/share/man/ru/man8/open_init_pty.8*
rm -f %{buildroot}/usr/share/man/ru/man8/semodule_deps.8.gz
rm -f %{buildroot}/usr/share/man/man8/open_init_pty.8
rm -f %{buildroot}/usr/sbin/open_init_pty
rm -f %{buildroot}/usr/sbin/run_init
rm -f %{buildroot}/usr/share/man/ru/man8/run_init.8*
rm -f %{buildroot}/usr/share/man/man8/run_init.8*
rm -f %{buildroot}/etc/pam.d/run_init*

mkdir   -m 755 -p %{buildroot}/%{generatorsdir}
mkdir   -m 755 -p %{buildroot}/%{_unitdir}
install -m 644 -p %{SOURCE6} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE7} %{buildroot}/%{_unitdir}/
install -m 644 -p %{SOURCE8} %{buildroot}/%{_unitdir}/
install -m 755 -p %{SOURCE9} %{buildroot}/%{generatorsdir}/
install -m 755 -p %{SOURCE5} %{buildroot}/%{_libexecdir}/selinux/

%package python-utils
Summary:    SELinux policy core python utilities
Requires:   policycoreutils-python3 = %{version}-%{release}
BuildArch:  noarch

%description python-utils
The policycoreutils-python-utils package contains the management tools use to manage
an SELinux environment.

%files python-utils
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

%package python3
Summary: SELinux policy core python3 interfaces
Requires:policycoreutils = %{version}-%{release}
Requires:libsemanage-python3 >= %{libsemanagever} libselinux-python3
Requires: python3-audit
Requires: checkpolicy
Requires: setools-python3 >= 4.1.1
BuildArch: noarch

%description python3
The policycoreutils-python3 package contains the interfaces that can be used
by python 3 in an SELinux environment.

%files python3
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
/usr/share/man/man8/sepolicy-gui.8.gz

%package devel
Summary: SELinux policy core policy devel utilities
Requires: policycoreutils-python-utils
Requires: make dnf

%description devel
The policycoreutils-devel package contains the management tools use to develop policy in an SELinux environment.

%files devel
%{_bindir}/sepolgen
%{_bindir}/sepolgen-ifgen
%{_bindir}/sepolgen-ifgen-attr-helper
%dir  /var/lib/sepolgen
/var/lib/sepolgen/perm_map
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

%package newrole
Summary: The newrole application for RBAC/MLS
BuildRequires: libcap-ng-devel
Requires: policycoreutils = %{version}-%{release}

%description newrole
RBAC/MLS policy machines require newrole as a way of changing the role
or level of a logged in user.

%files newrole
%attr(0755,root,root) %caps(cap_dac_read_search,cap_setpcap,cap_audit_write,cap_sys_admin,cap_fowner,cap_chown,cap_dac_override=pe) %{_bindir}/newrole
%{_mandir}/man1/newrole.1.gz
%{_mandir}/ru/man1/newrole.1.gz
%config(noreplace) %{_sysconfdir}/pam.d/newrole

%files
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
%{!?_licensedir:%global license %%doc}
%license policycoreutils/COPYING
%doc %{_usr}/share/doc/%{name}
/usr/share/locale/*

%package restorecond
Summary: SELinux restorecond utilities
BuildRequires: systemd

%description restorecond
The policycoreutils-restorecond package contains the restorecond service.

%files restorecond
%{_sbindir}/restorecond
%{_unitdir}/restorecond.service
%config(noreplace) %{_sysconfdir}/selinux/restorecond.conf
%config(noreplace) %{_sysconfdir}/selinux/restorecond_user.conf
%{_sysconfdir}/xdg/autostart/restorecond.desktop
%{_datadir}/dbus-1/services/org.selinux.Restorecond.service
%{_mandir}/man8/restorecond.8*
%{_mandir}/ru/man8/restorecond.8*
/usr/share/man/ru/man1/audit2why.1.gz
/usr/share/man/ru/man1/newrole.1.gz
/usr/share/man/ru/man5/selinux_config.5.gz
/usr/share/man/ru/man5/sestatus.conf.5.gz
/usr/share/man/ru/man8/genhomedircon.8.gz
/usr/share/man/ru/man8/restorecon_xattr.8.gz
/usr/share/man/ru/man8/semanage-boolean.8.gz
/usr/share/man/ru/man8/semanage-dontaudit.8.gz
/usr/share/man/ru/man8/semanage-export.8.gz
/usr/share/man/ru/man8/semanage-fcontext.8.gz
/usr/share/man/ru/man8/semanage-ibendport.8.gz
/usr/share/man/ru/man8/semanage-ibpkey.8.gz
/usr/share/man/ru/man8/semanage-import.8.gz
/usr/share/man/ru/man8/semanage-interface.8.gz
/usr/share/man/ru/man8/semanage-login.8.gz
/usr/share/man/ru/man8/semanage-module.8.gz
/usr/share/man/ru/man8/semanage-node.8.gz
/usr/share/man/ru/man8/semanage-permissive.8.gz
/usr/share/man/ru/man8/semanage-port.8.gz
/usr/share/man/ru/man8/semanage-user.8.gz
/usr/share/man/ru/man8/semodule_unpackage.8.gz
/usr/share/man/ru/man8/sepolgen.8.gz
/usr/share/man/ru/man8/sepolicy-booleans.8.gz
/usr/share/man/ru/man8/sepolicy-communicate.8.gz
/usr/share/man/ru/man8/sepolicy-generate.8.gz
/usr/share/man/ru/man8/sepolicy-gui.8.gz
/usr/share/man/ru/man8/sepolicy-interface.8.gz
/usr/share/man/ru/man8/sepolicy-manpage.8.gz
/usr/share/man/ru/man8/sepolicy-network.8.gz
/usr/share/man/ru/man8/sepolicy-transition.8.gz
/usr/share/man/ru/man8/sepolicy.8.gz

%{!?_licensedir:%global license %%doc}
%license policycoreutils/COPYING

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
* Fri Aug 21 2020 Daniel Burgener <daburgen@microsoft.com> 2.9-1
- Initial import from Fedora 31
