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

# comment out if no extra version
%global extraver p2

Summary: Allows restricted root access for specified users
Name: sudo
Version: 1.9.17
# remove -b 3 after rebase !!!
# use "-p -e % {?extraver}" when beta
# use "-e % {?extraver}"" when patch version
# use nothing special when normal version
Release: %autorelease -e %{?extraver}
License: ISC
URL: https://www.sudo.ws
Source0: %{url}/dist/%{name}-%{version}%{?extraver}.tar.gz
Source1: sudoers
Requires: pam
Recommends: system-default-editor
Recommends: %{name}-python-plugin%{?_isa} = %{version}-%{release}

BuildRequires: make
BuildRequires: pam-devel
BuildRequires: groff
BuildRequires: openldap-devel
BuildRequires: flex
BuildRequires: bison
BuildRequires: libtool
BuildRequires: audit-libs-devel libcap-devel
BuildRequires: libselinux-devel
BuildRequires: systemd-rpm-macros
BuildRequires: gettext
BuildRequires: zlib-devel

%description
Sudo (superuser do) allows a system administrator to give certain
users (or groups of users) the ability to run some (or all) commands
as root while logging all commands and arguments. Sudo operates on a
per-command basis.  It is not a replacement for the shell.  Features
include: the ability to restrict what commands a user may run on a
per-host basis, copious logging of each command (providing a clear
audit trail of who did what), a configurable timeout of the sudo
command, and the ability to use the same configuration file (sudoers)
on many different machines.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains header files developing sudo
plugins that use %{name}.


%package        logsrvd
Summary:        High-performance log server for %{name}
Requires:       %{name} = %{version}-%{release}
BuildRequires:  openssl-devel


%description    logsrvd
%{name}-logsrvd is a high-performance log server that accepts event and I/O logs from sudo.
It can be used to implement centralized logging of sudo logs.

%package        python-plugin
Summary:        Python plugin for %{name}
Requires:       %{name} = %{version}-%{release}
BuildRequires:  python3-devel


%description    python-plugin
%{name}-python-plugin allows using sudo plugins written in Python.

%prep
%autosetup -p1 -n %{name}-%{version}%{?extraver}

%build
# Remove bundled copy of zlib
rm -rf zlib/

%configure \
        --prefix=%{_prefix} \
        --sbindir=%{_sbindir} \
        --libdir=%{_libdir} \
        --docdir=%{_pkgdocdir} \
        --enable-tmpfiles.d=%{_tmpfilesdir} \
        --enable-openssl \
        --disable-root-mailer \
        --disable-intercept \
        --with-logging=syslog \
        --with-logfac=authpriv \
        --with-pam \
        --with-pam-login \
        --with-editor=%{_bindir}/nano:%{_bindir}/vim:%{_bindir}/vi \
        --with-env-editor \
        --with-ignore-dot \
        --with-tty-tickets \
        --with-ldap \
        --with-selinux \
        --with-sendmail=/usr/sbin/sendmail \
        --with-passprompt="[sudo] password for %p: " \
        --enable-python \
        --enable-zlib=system \
        --with-linux-audit \
        --with-sssd
#       --without-kerb5 \
#       --without-kerb4
%make_build

%check
%make_build check

%install
%make_install install_uid=`id -u` install_gid=`id -g` sudoers_uid=`id -u` sudoers_gid=`id -g`

chmod 755 $RPM_BUILD_ROOT%{_bindir}/* $RPM_BUILD_ROOT%{_sbindir}/*
install -p -d -m 700 $RPM_BUILD_ROOT/var/db/sudo
install -p -d -m 700 $RPM_BUILD_ROOT/var/db/sudo/lectured
install -p -d -m 750 $RPM_BUILD_ROOT/etc/sudoers.d
install -p -c -m 0440 %{SOURCE1} $RPM_BUILD_ROOT/etc/sudoers
# Add sudo to protected packages. Old location for yum/dnf.
mkdir -p $RPM_BUILD_ROOT/etc/dnf/protected.d/
echo "sudo" >$RPM_BUILD_ROOT/etc/dnf/protected.d/sudo.conf
# Add sudo to protected packages. New location for dnf5.
mkdir -p $RPM_BUILD_ROOT/usr/share/dnf5/libdnf.conf.d/
cat >$RPM_BUILD_ROOT/usr/share/dnf5/libdnf.conf.d/protect-sudo.conf <<EOF
[main]
protected_packages = sudo
EOF

chmod +x $RPM_BUILD_ROOT%{_libexecdir}/sudo/*.so # for stripping, reset in %%files

# Don't package LICENSE as a doc
rm -rf $RPM_BUILD_ROOT%{_pkgdocdir}/LICENSE

# Remove examples; Examples can be found in man pages too.
rm -rf $RPM_BUILD_ROOT%{_datadir}/examples/sudo

#Remove all .la files
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# Remove sudoers.dist
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/sudoers.dist

%find_lang sudo
%find_lang sudoers

cat sudo.lang sudoers.lang > sudo_all.lang
rm sudo.lang sudoers.lang

mkdir -p $RPM_BUILD_ROOT/etc/pam.d
cat > $RPM_BUILD_ROOT/etc/pam.d/sudo << EOF
#%%PAM-1.0
auth       include      system-auth
account    include      system-auth
password   include      system-auth
session    optional     pam_keyinit.so revoke
session    required     pam_limits.so
session    include      system-auth
EOF

cat > $RPM_BUILD_ROOT/etc/pam.d/sudo-i << EOF
#%%PAM-1.0
auth       include      sudo
account    include      sudo
password   include      sudo
session    optional     pam_keyinit.so force revoke
session    include      sudo
EOF


%files -f sudo_all.lang
%attr(0440,root,root) %config(noreplace) /etc/sudoers
%attr(0750,root,root) %dir /etc/sudoers.d/
%config(noreplace) /etc/pam.d/sudo
%config(noreplace) /etc/pam.d/sudo-i
%attr(0644,root,root) %{_tmpfilesdir}/sudo.conf
%attr(0644,root,root) %config(noreplace) /etc/dnf/protected.d/sudo.conf
%attr(0640,root,root) %config(noreplace) /etc/sudo.conf
%dir /usr/share/dnf5
%dir /usr/share/dnf5/libdnf.conf.d
/usr/share/dnf5/libdnf.conf.d/protect-sudo.conf
%dir /var/db/sudo
%dir /var/db/sudo/lectured
%attr(4111,root,root) %{_bindir}/sudo
%{_bindir}/sudoedit
%attr(0111,root,root) %{_bindir}/sudoreplay
%attr(0755,root,root) %{_sbindir}/visudo
%{_bindir}/cvtsudoers
%dir %{_libexecdir}/sudo
%attr(0755,root,root) %{_libexecdir}/sudo/sesh
%attr(0644,root,root) %{_libexecdir}/sudo/sudo_noexec.so
%attr(0644,root,root) %{_libexecdir}/sudo/sudoers.so
%attr(0644,root,root) %{_libexecdir}/sudo/audit_json.so
%attr(0644,root,root) %{_libexecdir}/sudo/group_file.so
%attr(0644,root,root) %{_libexecdir}/sudo/system_group.so
%attr(0644,root,root) %{_libexecdir}/sudo/libsudo_util.so.?.?.?
%{_libexecdir}/sudo/libsudo_util.so.?
%{_libexecdir}/sudo/libsudo_util.so
%{_mandir}/man5/sudoers.5*
%{_mandir}/man5/sudoers.ldap.5*
%{_mandir}/man5/sudo.conf.5*
%{_mandir}/man8/sudo.8*
%{_mandir}/man8/sudoedit.8*
%{_mandir}/man8/sudoreplay.8*
%{_mandir}/man8/visudo.8*
%{_mandir}/man1/cvtsudoers.1.gz
%{_mandir}/man5/sudoers_timestamp.5.gz
%dir %{_pkgdocdir}/
%{_pkgdocdir}/*
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%exclude %{_pkgdocdir}/ChangeLog

%files devel
%doc plugins/sample/sample_plugin.c
%{_includedir}/sudo_plugin.h
%{_mandir}/man5/sudo_plugin.5*

%files logsrvd
%attr(0640,root,root) %config(noreplace) /etc/sudo_logsrvd.conf
%attr(0755,root,root) %{_sbindir}/sudo_logsrvd
%attr(0755,root,root) %{_sbindir}/sudo_sendlog
%{_mandir}/man5/sudo_logsrv.proto.5.gz
%{_mandir}/man5/sudo_logsrvd.conf.5.gz
%{_mandir}/man8/sudo_logsrvd.8.gz
%{_mandir}/man8/sudo_sendlog.8.gz

%files python-plugin
%{_mandir}/man5/sudo_plugin_python.5.gz
%attr(0644,root,root) %{_libexecdir}/sudo/python_plugin.so

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 1.9.17-7.p2
- Latest state for sudo

* Tue Nov 04 2025 Alejandro López <allopez@redhat.com> - 1.9.17-6.p2
- Rebase to 1.9.17p2
- sudo-1.9.17p2 is available Resolves: rhbz#2383665

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.17-5.p1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 17 2025 Radovan Sroka <rsroka@fedoraproject.org> - 1.9.17-4.p1
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
