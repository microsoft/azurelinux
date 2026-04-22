# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#
# Copyright (C) 2014-2020 Red Hat, Inc.
# SPDX-License-Identifier: LGPL-2.1-or-later
#

# This file is maintained at the following location:
# https://github.com/cockpit-project/cockpit/blob/main/tools/cockpit.spec
#
# If you are editing this file in another location, changes will likely
# be clobbered the next time an automated release is done.
#
# Check first cockpit-devel@lists.fedorahosted.org
#

# earliest base that the subpackages work on; this is still required as long as
# we maintain the basic/optional split, then it can be replaced with just %{version}.
%define required_base 266

# we generally want CentOS packages to be like RHEL; special cases need to check %{centos} explicitly
%if 0%{?centos}
%define rhel %{centos}
%endif

%define _hardened_build 1

%define __lib lib

%if 0%{?suse_version} > 1500
%define pamconfdir %{_pam_vendordir}
%define pamconfig tools/cockpit.suse.pam
%else
%define pamconfdir %{_sysconfdir}/pam.d
%define pamconfig tools/cockpit.pam
%endif

%if %{defined _pamdir}
%define pamdir %{_pamdir}
%else
%define pamdir %{_libdir}/security
%endif

# distributions which ship nodejs-esbuild can rebuild the bundle during package build
# allow override from command line (e.g. for development builds)
%if 0%{?fedora} >= 42
%{!?rebuild_bundle: %define rebuild_bundle 1}
%endif

# to avoid using asciidoc-py in RHEL and CentOS we use the prebuilt docs
%if 0%{?rhel}
%define bundle_docs 1
%endif

Name:           cockpit
Summary:        Web Console for Linux servers
License:        LGPL-2.1-or-later AND GPL-3.0-and-later AND MIT AND CC-BY-SA-3.0 AND BSD-3-Clause
URL:            https://cockpit-project.org/

Version:        356
Release: 2%{?dist}
Source0:        https://github.com/cockpit-project/cockpit/releases/download/%{version}/cockpit-%{version}.tar.xz
Source1:        https://github.com/cockpit-project/cockpit/releases/download/%{version}/cockpit-node-%{version}.tar.xz

%if 0%{?fedora} >= 41 || 0%{?rhel}
ExcludeArch: %{ix86}
%endif

%define enable_multihost 1
%if 0%{?fedora} >= 41 || 0%{?rhel} >= 10
%define enable_multihost 0
%endif

# Ship custom SELinux policy
%define selinuxtype targeted
%define selinux_configure_arg --enable-selinux-policy=%{selinuxtype}

BuildRequires: gcc
BuildRequires: pkgconfig(gio-unix-2.0)
BuildRequires: pkgconfig(json-glib-1.0)
BuildRequires: pkgconfig(polkit-agent-1) >= 0.105
BuildRequires: pam-devel

BuildRequires: autoconf automake
BuildRequires: make
BuildRequires: python3-devel
BuildRequires: gettext >= 0.21
BuildRequires: openssl-devel
BuildRequires: gnutls-devel >= 3.4.3
BuildRequires: zlib-devel
BuildRequires: krb5-devel >= 1.11
BuildRequires: glib-networking
BuildRequires: sed

BuildRequires: glib2-devel >= 2.68.0
# this is for runtimedir in the tls proxy ace21c8879
BuildRequires: systemd-devel >= 235
%if 0%{?suse_version}
BuildRequires: distribution-release
BuildRequires: openssh
BuildRequires: distribution-logos
BuildRequires: wallpaper-branding
%else
BuildRequires: openssh-clients
%endif
BuildRequires: krb5-server
BuildRequires: gdb

%if 0%{?rebuild_bundle}
BuildRequires: nodejs
BuildRequires: %{_bindir}/node
BuildRequires: nodejs-esbuild
%endif

%if !%{defined bundle_docs}
%if 0%{?suse_version}
BuildRequires: rubygem(asciidoctor)
%else
BuildRequires: asciidoctor
%endif
%endif

BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel

# This is the "cockpit" metapackage. It should only
# Require, Suggest or Recommend other cockpit-xxx subpackages

Requires: cockpit-bridge
Requires: cockpit-ws
Requires: cockpit-system

# Optional components
Recommends: (cockpit-storaged if udisks2)
Recommends: (cockpit-packagekit if dnf)
%if 0%{?suse_version} == 0
Recommends: (dnf5daemon-server if dnf5)
%endif
Suggests: python3-pcp

%if 0%{?rhel} == 0
Recommends: (cockpit-networkmanager if NetworkManager)
# c-ostree is not in RHEL 8/9
Recommends: (cockpit-ostree if rpm-ostree)
Suggests: cockpit-selinux
%endif
%if 0%{?rhel} && 0%{?centos} == 0
Recommends: subscription-manager-cockpit
%endif

BuildRequires:  python3-devel
BuildRequires:  python3-pip
%if 0%{?rhel} == 0 && !0%{?suse_version}
# All of these are only required for running pytest (which we only do on Fedora)
BuildRequires:  procps-ng
BuildRequires:  python3-pytest-asyncio
BuildRequires:  python3-pytest-timeout
%endif

%prep
%setup -q -n cockpit-%{version}
%if 0%{?rebuild_bundle}
%setup -q -D -T -a 1 -n cockpit-%{version}
%endif

%build
%if 0%{?rebuild_bundle}
rm -rf dist
# HACK: node module packaging is currently broken in Fedora ≤ 43, should be in
# common location, not major version specific one
NODE_ENV=production NODE_PATH=/usr/lib/node_modules:$(echo /usr/lib/node_modules_*) ./build.js
%else
# Use pre-built bundle on distributions without nodejs-esbuild
%endif

%configure \
    %{?selinux_configure_arg} \
%if 0%{?suse_version}
    --docdir=%_defaultdocdir/%{name} \
%endif
    --with-pamdir='%{pamdir}' \
%if %{enable_multihost}
    --enable-multihost \
%endif
%if %{defined bundle_docs}
    --disable-doc \
%endif

%make_build

%check
make -j$(nproc) check

%if 0%{?rhel} == 0 && 0%{?suse_version} == 0
export NO_QUNIT=1
%pytest
%endif

%install
%if 0%{?suse_version}
export NO_BRP_STALE_LINK_ERROR="yes"
%endif
%make_install

mkdir -p $RPM_BUILD_ROOT%{pamconfdir}
install -p -m 644 %{pamconfig} $RPM_BUILD_ROOT%{pamconfdir}/cockpit

rm -f %{buildroot}/%{_libdir}/cockpit/*.so
install -D -p -m 644 AUTHORS README.md %{buildroot}%{_docdir}/cockpit/

# We install the upstream pre-built docs as we can't build them
%if %{defined bundle_docs}
%define docbundledir %{_builddir}/%{name}-%{version}/doc/output/html
install -d %{buildroot}%{_docdir}/cockpit/guide
cp -rp %{docbundledir}/* %{buildroot}%{_docdir}/cockpit/guide/
# Install pre-built man pages
%define manbundledir %{_builddir}/%{name}-%{version}/doc/output/man
for section in 1 5 8; do
  for manpage in %{manbundledir}/*.${section}; do
    install -D -p -m 644 "$manpage" %{buildroot}%{_mandir}/man${section}/$(basename "$manpage")
  done
done
%endif

# Build the package lists for resource packages
# cockpit-bridge is the basic dependency for all cockpit-* packages, so centrally own the page directory
echo '%dir %{_datadir}/cockpit' > base.list
echo '%dir %{_datadir}/cockpit/base1' >> base.list
find %{buildroot}%{_datadir}/cockpit/base1 -type f -o -type l >> base.list
echo '%{_sysconfdir}/cockpit/machines.d' >> base.list
echo %{buildroot}%{_datadir}/polkit-1/actions/org.cockpit-project.cockpit-bridge.policy >> base.list

echo '%dir %{_datadir}/cockpit/shell' >> system.list
find %{buildroot}%{_datadir}/cockpit/shell -type f >> system.list

echo '%dir %{_datadir}/cockpit/systemd' >> system.list
find %{buildroot}%{_datadir}/cockpit/systemd -type f >> system.list

echo '%dir %{_datadir}/cockpit/users' >> system.list
find %{buildroot}%{_datadir}/cockpit/users -type f >> system.list

echo '%dir %{_datadir}/cockpit/metrics' >> system.list
find %{buildroot}%{_datadir}/cockpit/metrics -type f >> system.list

echo '%dir %{_datadir}/cockpit/kdump' > kdump.list
find %{buildroot}%{_datadir}/cockpit/kdump -type f >> kdump.list

echo '%dir %{_datadir}/cockpit/sosreport' > sosreport.list
find %{buildroot}%{_datadir}/cockpit/sosreport -type f >> sosreport.list

echo '%dir %{_datadir}/cockpit/storaged' > storaged.list
find %{buildroot}%{_datadir}/cockpit/storaged -type f >> storaged.list

echo '%dir %{_datadir}/cockpit/networkmanager' > networkmanager.list
find %{buildroot}%{_datadir}/cockpit/networkmanager -type f >> networkmanager.list

echo '%dir %{_datadir}/cockpit/packagekit' > packagekit.list
find %{buildroot}%{_datadir}/cockpit/packagekit -type f >> packagekit.list

echo '%dir %{_datadir}/cockpit/apps' >> packagekit.list
find %{buildroot}%{_datadir}/cockpit/apps -type f >> packagekit.list

echo '%dir %{_datadir}/cockpit/selinux' > selinux.list
find %{buildroot}%{_datadir}/cockpit/selinux -type f >> selinux.list

echo '%dir %{_datadir}/cockpit/static' > static.list
echo '%dir %{_datadir}/cockpit/static/fonts' >> static.list
find %{buildroot}%{_datadir}/cockpit/static -type f >> static.list

sed -i "s|%{buildroot}||" *.list

%if 0%{?suse_version}
# remove files of not installable packages
rm -r %{buildroot}%{_datadir}/cockpit/sosreport
rm -f %{buildroot}/%{_prefix}/share/metainfo/org.cockpit_project.cockpit_sosreport.metainfo.xml
rm -f %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/cockpit-sosreport.png
%else
%global _debugsource_packages 1
%global _debuginfo_subpackages 0

%define find_debug_info %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_include_minidebuginfo:-m} %{?_find_debuginfo_dwz_opts} %{?_find_debuginfo_opts} %{?_debugsource_packages:-S debugsourcefiles.list} "%{_builddir}/%{?buildsubdir}"

%endif
# /suse_version
rm -rf %{buildroot}/usr/src/debug

# On RHEL kdump, networkmanager, selinux, and sosreport are part of the system package
%if 0%{?rhel}
cat kdump.list sosreport.list networkmanager.list selinux.list >> system.list
rm -f %{buildroot}%{_datadir}/metainfo/org.cockpit_project.cockpit_sosreport.metainfo.xml
rm -f %{buildroot}%{_datadir}/metainfo/org.cockpit_project.cockpit_kdump.metainfo.xml
rm -f %{buildroot}%{_datadir}/metainfo/org.cockpit_project.cockpit_selinux.metainfo.xml
rm -f %{buildroot}%{_datadir}/metainfo/org.cockpit_project.cockpit_networkmanager.metainfo.xml
rm -f %{buildroot}%{_datadir}/icons/hicolor/64x64/apps/cockpit-sosreport.png
%endif

# -------------------------------------------------------------------------------
# Sub-packages

%description
The Cockpit Web Console enables users to administer GNU/Linux servers using a
web browser.

It offers network configuration, log inspection, diagnostic reports, SELinux
troubleshooting, interactive command-line sessions, and more.

%files
%license LICENSES/LGPL-2.1.txt
%{_docdir}/cockpit/AUTHORS
%{_docdir}/cockpit/README.md
%{_datadir}/metainfo/org.cockpit_project.cockpit.appdata.xml
%{_datadir}/icons/hicolor/128x128/apps/cockpit.png
%doc %{_mandir}/man1/cockpit.1.gz


%package bridge
Summary: Cockpit bridge server-side component
BuildArch: noarch

%description bridge
The Cockpit bridge component installed server side and runs commands on the
system on behalf of the web based user interface.

%files bridge -f base.list
%license LICENSES/GPL-3.0.txt
%doc %{_mandir}/man1/cockpit-bridge.1.gz
%{_bindir}/cockpit-bridge
%{_libexecdir}/cockpit-askpass
%{python3_sitelib}/%{name}*

%package doc
Summary: Cockpit deployment and developer guide
BuildArch: noarch

%description doc
The Cockpit Deployment and Developer Guide shows sysadmins how to
deploy Cockpit on their machines as well as helps developers who want to
embed or extend Cockpit.

%files doc
%license LICENSES/LGPL-2.1.txt
%exclude %{_docdir}/cockpit/AUTHORS
%exclude %{_docdir}/cockpit/README.md
%{_docdir}/cockpit

%package system
Summary: Cockpit admin interface package for configuring and troubleshooting a system
BuildArch: noarch
Requires: cockpit-bridge >= %{version}-%{release}
%if !0%{?suse_version}
Requires: shadow-utils
%endif
Requires: grep
Requires: /usr/bin/pwscore
Requires: /usr/bin/date
Provides: cockpit-shell = %{version}-%{release}
Provides: cockpit-systemd = %{version}-%{release}
Provides: cockpit-tuned = %{version}-%{release}
Provides: cockpit-users = %{version}-%{release}
%if 0%{?rhel}
Requires: NetworkManager >= 1.6
Requires: sos
Requires: sudo
Recommends: setroubleshoot-server >= 3.3.3
Recommends: /usr/bin/kdumpctl
Suggests: NetworkManager-team
Suggests: python3-pcp
Provides: cockpit-kdump = %{version}-%{release}
Provides: cockpit-networkmanager = %{version}-%{release}
Provides: cockpit-selinux = %{version}-%{release}
Provides: cockpit-sosreport = %{version}-%{release}
%endif

Provides: bundled(npm(@patternfly/patternfly)) = 6.4.0
Provides: bundled(npm(@patternfly/react-core)) = 6.4.1
Provides: bundled(npm(@patternfly/react-icons)) = 6.4.0
Provides: bundled(npm(@patternfly/react-styles)) = 6.4.0
Provides: bundled(npm(@patternfly/react-table)) = 6.4.1
Provides: bundled(npm(@patternfly/react-tokens)) = 6.4.0
Provides: bundled(npm(@xterm/addon-webgl)) = 0.19.0
Provides: bundled(npm(@xterm/xterm)) = 6.0.0
Provides: bundled(npm(dequal)) = 2.0.3
Provides: bundled(npm(focus-trap)) = 7.6.4
Provides: bundled(npm(ipaddr.js)) = 2.3.0
Provides: bundled(npm(json-stable-stringify-without-jsonify)) = 1.0.1
Provides: bundled(npm(lodash)) = 4.17.23
Provides: bundled(npm(prop-types)) = 15.8.1
Provides: bundled(npm(react)) = 18.3.1
Provides: bundled(npm(react-dom)) = 18.3.1
Provides: bundled(npm(remarkable)) = 2.0.1
Provides: bundled(npm(scheduler)) = 0.23.2
Provides: bundled(npm(tabbable)) = 6.4.0
Provides: bundled(npm(throttle-debounce)) = 5.0.2
Provides: bundled(npm(tslib)) = 2.8.1
Provides: bundled(npm(uuid)) = 13.0.0

%description system
This package contains the Cockpit shell and system configuration interfaces.

%files system -f system.list
%license LICENSES/LGPL-2.1.txt
%dir %{_datadir}/cockpit/shell/images

%package ws
Summary: Cockpit Web Service
Requires: openssl
Requires: glib2 >= 2.68.0
Requires: (%{name}-ws-selinux = %{version}-%{release} if selinux-policy-base)
Recommends: sscg >= 2.3
Recommends: system-logos
Suggests: sssd-dbus >= 2.6.2
# for cockpit-desktop
Suggests: python3
Obsoletes: cockpit-tests < 331

# prevent hard python3 dependency for cockpit-desktop, it falls back to other browsers
%global __requires_exclude_from ^%{_libexecdir}/cockpit-client$

%description ws
The Cockpit Web Service listens on the network, and authenticates users.

If sssd-dbus is installed, you can enable client certificate/smart card
authentication via sssd/FreeIPA.

%files ws -f static.list
%license LICENSES/LGPL-2.1.txt
%doc %{_mandir}/man1/cockpit-desktop.1.gz
%doc %{_mandir}/man5/cockpit.conf.5.gz
%doc %{_mandir}/man8/cockpit-ws.8.gz
%doc %{_mandir}/man8/cockpit-tls.8.gz
%doc %{_mandir}/man8/pam_ssh_add.8.gz
%dir %{_sysconfdir}/cockpit
%config(noreplace) %{_sysconfdir}/cockpit/ws-certs.d
%config(noreplace) %{pamconfdir}/cockpit

# created in %post, so that users can rm the files
%ghost %{_sysconfdir}/issue.d/cockpit.issue
%ghost %{_sysconfdir}/motd.d/cockpit
%ghost %attr(0644, root, root) %{_sysconfdir}/cockpit/disallowed-users
%dir %{_datadir}/cockpit/issue
%{_datadir}/cockpit/issue/update-issue
%{_datadir}/cockpit/issue/inactive.issue
%{_unitdir}/cockpit.service
%{_unitdir}/cockpit-issue.service
%{_unitdir}/cockpit.socket
%{_unitdir}/cockpit-session-socket-user.service
%{_unitdir}/cockpit-session.socket
%{_unitdir}/cockpit-session@.service
%{_unitdir}/cockpit-wsinstance-http.socket
%{_unitdir}/cockpit-wsinstance-http.service
%{_unitdir}/cockpit-wsinstance-https-factory.socket
%{_unitdir}/cockpit-wsinstance-https-factory@.service
%{_unitdir}/cockpit-wsinstance-https@.socket
%{_unitdir}/cockpit-wsinstance-https@.service
%{_unitdir}/cockpit-wsinstance-socket-user.service
%{_unitdir}/system-cockpithttps.slice
%{_prefix}/%{__lib}/tmpfiles.d/cockpit-ws.conf
%{pamdir}/pam_ssh_add.so
%{_libexecdir}/cockpit-ws
%{_libexecdir}/cockpit-wsinstance-factory
%{_libexecdir}/cockpit-tls
%{_libexecdir}/cockpit-client
%{_libexecdir}/cockpit-client.ui
%{_libexecdir}/cockpit-desktop
%{_libexecdir}/cockpit-certificate-ensure
%{_libexecdir}/cockpit-certificate-helper
%{_libexecdir}/cockpit-session
%{_datadir}/cockpit/branding

%post ws
# set up dynamic motd/issue symlinks on first-time install; don't bring them back on upgrades if admin removed them
# disable root login on first-time install; so existing installations aren't changed
if [ "$1" = 1 ]; then
    mkdir -p /etc/motd.d /etc/issue.d
    ln -s ../../run/cockpit/issue /etc/motd.d/cockpit
    ln -s ../../run/cockpit/issue /etc/issue.d/cockpit.issue
    printf "# List of users which are not allowed to login to Cockpit\n" > /etc/cockpit/disallowed-users
    printf "root\n" >> /etc/cockpit/disallowed-users
    chmod 644 /etc/cockpit/disallowed-users
fi

# on upgrades, adjust motd/issue links to changed target if they still exist (changed in 331)
if [ "$1" = 2 ]; then
    if [ "$(readlink /etc/motd.d/cockpit 2>/dev/null)" = "../../run/cockpit/motd" ]; then
        ln -sfn ../../run/cockpit/issue /etc/motd.d/cockpit
    fi
    if [ "$(readlink /etc/issue.d/cockpit.issue 2>/dev/null)" = "../../run/cockpit/motd" ]; then
        ln -sfn ../../run/cockpit/issue /etc/issue.d/cockpit.issue
    fi
fi

%tmpfiles_create cockpit-ws.conf
%systemd_post cockpit.socket cockpit.service
# firewalld only partially picks up changes to its services files without this
test -f %{_bindir}/firewall-cmd && firewall-cmd --reload --quiet || true

# remove obsolete system user on upgrade (replaced with DynamicUser in version 330)
if getent passwd cockpit-wsinstance >/dev/null; then
    userdel cockpit-wsinstance
fi

%preun ws
%systemd_preun cockpit.socket cockpit.service

%postun ws
%systemd_postun_with_restart cockpit.socket cockpit.service

%package ws-selinux
Summary: SELinux security policy for cockpit-ws
# older -ws contained the SELinux policy, now split out
Conflicts: %{name}-ws < 337-1.2025
Requires(post): selinux-policy-%{selinuxtype} >= %{_selinux_policy_version}
Requires(post): libselinux-utils
Requires(post): policycoreutils

%description ws-selinux
SELinux policy module for the cockpit-ws package.

%files ws-selinux
%license LICENSES/LGPL-2.1.txt
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%{_mandir}/man8/%{name}_session_selinux.8cockpit.*
%{_mandir}/man8/%{name}_ws_selinux.8cockpit.*
%ghost %{_selinux_store_path}/%{selinuxtype}/active/modules/200/%{name}

%pre ws-selinux
%selinux_relabel_pre -s %{selinuxtype}

%post ws-selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%selinux_relabel_post -s %{selinuxtype}

%postun ws-selinux
%selinux_modules_uninstall -s %{selinuxtype} %{name}
%selinux_relabel_post -s %{selinuxtype}

# -------------------------------------------------------------------------------
# Sub-packages that are part of cockpit-system in RHEL/CentOS, but separate in Fedora

%if 0%{?rhel} == 0

%package kdump
Summary: Cockpit user interface for kernel crash dumping
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
%if 0%{?suse_version}
Requires: kexec-tools
%else
Requires: /usr/bin/kdumpctl
%endif
BuildArch: noarch

%description kdump
The Cockpit component for configuring kernel crash dumping.

%files kdump -f kdump.list
%license LICENSES/LGPL-2.1.txt
%{_datadir}/metainfo/org.cockpit_project.cockpit_kdump.metainfo.xml

# sosreport is not supported on opensuse yet
%if !0%{?suse_version}
%package sosreport
Summary: Cockpit user interface for diagnostic reports
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
Requires: sos
BuildArch: noarch

%description sosreport
The Cockpit component for creating diagnostic reports with the
sosreport tool.

%files sosreport -f sosreport.list
%license LICENSES/LGPL-2.1.txt
%{_datadir}/metainfo/org.cockpit_project.cockpit_sosreport.metainfo.xml
%{_datadir}/icons/hicolor/64x64/apps/cockpit-sosreport.png
%endif

%package networkmanager
Summary: Cockpit user interface for networking, using NetworkManager
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
Requires: NetworkManager >= 1.6
# Optional components
Recommends: NetworkManager-team
BuildArch: noarch

%description networkmanager
The Cockpit component for managing networking.  This package uses NetworkManager.

%files networkmanager -f networkmanager.list
%license LICENSES/LGPL-2.1.txt
%{_datadir}/metainfo/org.cockpit_project.cockpit_networkmanager.metainfo.xml

%endif

%if 0%{?rhel} == 0

%package selinux
Summary: Cockpit SELinux package
Requires: cockpit-bridge >= %{required_base}
Requires: cockpit-shell >= %{required_base}
# setroubleshoot is available on SLE Micro starting with 5.5
%if !0%{?is_smo} || ( 0%{?is_smo} && 0%{?sle_version} >= 150500 )
Requires:       setroubleshoot-server >= 3.3.3
%endif
BuildArch: noarch

%description selinux
This package contains the Cockpit user interface integration with the
utility setroubleshoot to diagnose and resolve SELinux issues.

%files selinux -f selinux.list
%license LICENSES/LGPL-2.1.txt
%{_datadir}/metainfo/org.cockpit_project.cockpit_selinux.metainfo.xml

%endif

%package -n cockpit-storaged
Summary: Cockpit user interface for storage, using udisks
Requires: cockpit-shell >= %{required_base}
Requires: udisks2 >= 2.9
Recommends: udisks2-lvm2 >= 2.9
Recommends: udisks2-iscsi >= 2.9
%if ! 0%{?rhel}
Recommends: (udisks2-btrfs >= 2.9 if btrfs-progs)
%endif
Recommends: device-mapper-multipath
Recommends: clevis-luks
Requires: %{__python3}
%if 0%{?suse_version}
Requires: python3-dbus-python
%else
Requires: python3-dbus
%endif
BuildArch: noarch

%description -n cockpit-storaged
The Cockpit component for managing storage.  This package uses udisks.

%files -n cockpit-storaged -f storaged.list
%license LICENSES/LGPL-2.1.txt
%{_datadir}/metainfo/org.cockpit_project.cockpit_storaged.metainfo.xml

%post storaged

# version 332 moved the btrfs temp mounts db to /run
if [ "$1" = 2 ] && [ -d /var/lib/cockpit/btrfs ]; then
    rm -rf --one-file-system  /var/lib/cockpit/btrfs || true
fi

%package -n cockpit-packagekit
Summary: Cockpit user interface for packages
BuildArch: noarch
Requires: cockpit-bridge >= %{required_base}
Requires: PackageKit
Recommends: python3-tracer
# HACK: https://bugzilla.redhat.com/show_bug.cgi?id=1800468
Requires: polkit

%description -n cockpit-packagekit
The Cockpit components for installing OS updates and Cockpit add-ons,
via PackageKit.

%files -n cockpit-packagekit -f packagekit.list
%license LICENSES/LGPL-2.1.txt

# The changelog is automatically generated and merged
%changelog
* Wed Feb 11 2026 Packit <hello@packit.dev> - 356-1
- systemd: Allow editing timers created by Cockpit
- Convert license headers to SPDX format


* Thu Jan 29 2026 Packit <hello@packit.dev> - 355-1
- ws: Remove obsolete pam_cockpit_cert module
- shell: add StartTransientUnit as a sudo alternative


* Wed Jan 07 2026 Martin Pitt <mpitt@redhat.com> - 354-1
- Convert documentation to AsciiDoc
- Work around Firefox 146/147 bug (rhbz#2422331)
- Bug fixes


* Mon Dec 15 2025 Jelle van der Waa <jelle@vdwaa.nl> - 353.1-1
- Release workflow fixes


* Wed Nov 12 2025 Packit <hello@packit.dev> - 351-1
- Firewall ports can be deleted individually

* Wed Oct 29 2025 Packit <hello@packit.dev> - 350-1
- networking: fix renaming of bridges and other groups (RHEL-117883)
- bridge: fix OpenSSH_10.2p1 host key detection

* Wed Oct 15 2025 Packit <hello@packit.dev> - 349-1
- Package manifests: Add `any` test
- Bug fixes and translation updates

* Thu Oct 02 2025 Packit <hello@packit.dev> - 348-1
- Bug fixes and translation updates

* Wed Sep 17 2025 Packit <hello@packit.dev> - 347-1
- Site-specific branding support

* Thu Sep 11 2025 Packit <hello@packit.dev> - 345.2-1
- storage: Apply missing patch to make rhbz#2388785 fix take effect

* Wed Sep 10 2025 Martin Pitt <mpitt@redhat.com> - 345.1-1
 - storage: Fix dropdown menus hidden behind non-scrollable content (rhbz#2388785)

* Wed Aug 20 2025 Packit <hello@packit.dev> - 345-1
- Translation and dependency updates
- Shorter IPv6 addresses
- IPv6 addresses for WireGuard

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 344-2
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 06 2025 Packit <hello@packit.dev> - 344-1
Bug fixes and translation updates

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 343-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Packit <hello@packit.dev> - 343-1
- Bug fixes and translation updates

* Wed Jul 09 2025 Packit <hello@packit.dev> - 342-1
- Bug fixes and translation updates

* Fri Jun 27 2025 Packit <hello@packit.dev> - 341.1-1
- Stratis gating fixes

* Wed Jun 25 2025 Packit <hello@packit.dev> - 341-1
- services: show link to podman page for quadlets

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 340-2
- Rebuilt for Python 3.14

* Wed Jun 04 2025 Packit <hello@packit.dev> - 340-1
- Storage: Prevent modifying partitions in unsupported places
- Bug fixes and translation updates

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 339-2
- Rebuilt for Python 3.14

* Wed May 21 2025 Packit <hello@packit.dev> - 339-1
- Add cockpit/ws arm64 container
- Storage: Disk Self-Test error warnings on the overview page
- Bug fixes and translation updates

* Wed May 07 2025 Packit <hello@packit.dev> - 338-1
- Translation updates
- Bug fixes

* Wed Apr 23 2025 Packit <hello@packit.dev> - 337-1
- Upgraded to Patternfly 6
- Support dnf needs-restarting

* Fri Mar 28 2025 Packit <hello@packit.dev> - 336.2-1
- storage: Revert "Use mdraid metadata version 1.0 when in Anaconda mode" (rhbz#2352953)
- Translation updates (rhbz#2354986)

* Wed Mar 26 2025 Packit <hello@packit.dev> - 336.1-1
- storage: Fix passphrase remembering with "Reuse encryption" (rhbz#2354497)
- Translation updates (rhbz#2354986)

* Mon Mar 24 2025 Packit <hello@packit.dev> - 336-1
- storage: Implement deletion of multi-device btrfs (rhbz#2352385)
- storage: Use mdraid metadata version 1.0 when in Anaconda mode (rhbz#2352953)
- Add a channel capabilities system

* Wed Mar 12 2025 Packit <hello@packit.dev> - 335-1
- storage: SMART support

* Thu Feb 27 2025 Packit <hello@packit.dev> - 334-1
- https://issues.redhat.com/browse/RHEL-32834

* Thu Feb 13 2025 Packit <hello@packit.dev> - 333-1
- various bug fixes and improvements

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 332-2
- Add explicit BR: libxcrypt-devel

* Wed Jan 29 2025 Packit <hello@packit.dev> - 332-1
- containers/ws: Include cockpit-files
- login: Beibooting to all supported OSes
- metrics: Show system boots in metrics

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 331-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 18 2024 Packit <hello@packit.dev> - 331-1
- ws: Prevent search engine indexing with robots.txt
- container/ws: Support using an external SSH agent

* Wed Dec 04 2024 Packit <hello@packit.dev> - 330-1
- Web server: Increased sandboxing, setuid removal, bootc support
- Development: New install mode using systemd-sysext
- ws container: Move to Fedora 41

* Mon Nov 25 2024 Packit <hello@packit.dev> - 329.1-1
- cockpit.js: Put back cockpit.{resolve,reject}() to fix subscription-manager-cockpit

* Wed Nov 20 2024 Packit <hello@packit.dev> - 329-1
- Shell: Extra warnings when connecting to remote hosts

* Wed Nov 06 2024 Packit <hello@packit.dev> - 328-1
- Bug fixes and performance improvements

* Wed Oct 23 2024 Packit <hello@packit.dev> - 327-1
- Connect to similar servers without Cockpit installed

* Wed Oct 09 2024 Packit <hello@packit.dev> - 326-1
- cockpit-pcp package is now obsolete
- cockpit/ws container: Connect to servers without installed Cockpit
- cockpit/ws container: Support host specific SSH keys
- Storage: Support for Stratis filesystem sizes and limits

* Wed Sep 25 2024 Packit <hello@packit.dev> - 325-1
- storage: Expose Stratis virtual filesystem sizes
- client: Properly handle unknown SSH host keys

* Wed Sep 04 2024 Packit <hello@packit.dev> - 324-1
- Bug fixes and performance improvements

* Tue Aug 20 2024 Packit <hello@packit.dev> - 323-1
- metrics: Install valkey instead of redis on RHEL/CentOS 10
- login: Prevent multiple logins in a single browser session
- Update documentation links

* Thu Aug 08 2024 Packit <hello@packit.dev> - 322-1
- shell: Deprecate host switcher

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 321-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Packit <hello@packit.dev> - 321-1
- Bug fixes and performance improvements

* Wed Jul 03 2024 Packit <hello@packit.dev> - 320-1
- pam-ssh-add: Fix insecure killing of session ssh-agent [CVE-2024-6126]
- sosreport: Read report directory from sos config (fix page on Debian/Ubuntu)

* Wed Jun 26 2024 Packit <hello@packit.dev> - 319-1
- List btrfs snapshots in subvolume detail view

* Mon Jun 17 2024 Martin Pitt <mpitt@redhat.com> - 318-2
- Rebuilt for Python 3.13

* Wed Jun 12 2024 Packit <hello@packit.dev> - 318-1
- Storage: Extra confirmation before deleting non-empty partitions in Anaconda's Web UI
- Discontinue Intel 32-bit support in Fedora, CentOS, and RHEL
- cockpit.js: Get user primary group ID

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 317-2
- Rebuilt for Python 3.13

* Wed May 29 2024 Packit <hello@packit.dev> - 317-1
- webserver: System user changes
- metrics: Prefer valkey over redis on Fedora

* Thu Apr 25 2024 Packit <hello@packit.dev> - 316-1
- cockpit.js API: Fix format_bytes() units

* Wed Apr 10 2024 Packit <hello@packit.dev> - 315-1
- systemd: Check proper ssh service unit on Debian/Ubuntu
- Translation updates

* Thu Mar 28 2024 Packit <hello@packit.dev> - 314-1
- Diagnostic reports: Fix command injection vulnerability with crafted report names
- Storage: Improvements to read-only encrypted filesystems

* Wed Mar 13 2024 Packit <hello@packit.dev> - 313-1
- assorted bug fixes and improvements

* Wed Feb 28 2024 Packit <hello@packit.dev> - 312-1
- Accounts: support lastlog2 and make the page faster
- Storage: Various Anaconda mode fixes
- Fix package build if cockpit-bridge package is installed

* Tue Feb 20 2024 Packit <hello@packit.dev> - 311.1-1
- Update documentation links to RHEL 9 (RHEL-3954)
- Storage: Various bug fixes

* Wed Feb 14 2024 Packit <hello@packit.dev> - 311-1
- Bug fixes and stability improvements

* Wed Feb 07 2024 Packit <hello@packit.dev> - 310.2-1
- selinux: Cover migration to /run
- ws: Handle HEAD requests correctly, for curl 8.6.0

* Fri Feb 02 2024 Packit <hello@packit.dev> - 310.1-1
- bridge: Fix race condition/crash in file watching channels

* Wed Jan 31 2024 Packit <hello@packit.dev> - 310-1
- Storage: support for btrfs
- Storage: improved support for swap

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 309-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 309-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Packit <hello@packit.dev> - 309-1
- Storage: Introduce btrfs support

* Wed Jan 03 2024 Packit <hello@packit.dev> - 308-1
- Fix connecting to remote hosts with OpenSSH 0.9.6

* Fri Dec 15 2023 Martin Pitt <mpitt@redhat.com> - 307-1
- Storage redesign

* Wed Nov 29 2023 Packit <hello@packit.dev> - 306-1
- Kdump: Add Ansible/shell automation

* Wed Nov 15 2023 Packit <hello@packit.dev> - 305-1
- Performance and stability improvements

* Wed Nov 01 2023 Packit <hello@packit.dev> - 304-1
Storage: Support for RAID layouts with LVM2

* Thu Oct 19 2023 Adam Williamson <awilliam@redhat.com> - 303-2
- Rebuild for untagged selinux-policy (cockpit-ws dep)

* Wed Oct 18 2023 Packit <hello@packit.dev> - 303-1
- Apps: Warn if appstream data package is missing
- Shell: Redesign untrusted "add host" dialog

* Thu Oct 05 2023 Packit <hello@packit.dev> - 302-1
- Storage: Partitions can be resized
- many bug fixes

* Wed Sep 20 2023 Packit <hello@packit.dev> - 301-1
- WireGuard support
- Metrics: link to network interface details

* Wed Sep 06 2023 Packit <hello@packit.dev> - 300-1
- Celebrating the Nürnberg life release!
- Storage: Support for growing block devices of a Stratis pool

* Wed Aug 23 2023 Packit <hello@packit.dev> - 299-1
- Kdump: Show location of kdump to verify the successful configuration test
- Storage: Support for no-overprovisioning with Stratis
- Storage: Cockpit can now add caches to encrypted Stratis pools

* Wed Jul 26 2023 Packit <hello@packit.dev> - 297-1
- users: allow administrators to change the user shell
- tools: Enable Python bridge on Fedora 38

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 296-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Packit <hello@packit.dev> - 296-1
- Performance and stability improvements

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 295-2
- Rebuilt for Python 3.12

* Wed Jun 28 2023 Packit <hello@packit.dev> - 295-1
- Cockpit Client can now connect to servers without Cockpit installed

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 294.1-2
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Packit <hello@packit.dev> - 294.1-1
- Multiple major fixes for the "remote python bridge" use case

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 294-2
- Rebuilt for Python 3.12

* Wed Jun 14 2023 Packit <hello@packit.dev> - 294-1
- Introduce Python bridge on Fedora Rawhide and Debian unstable

* Thu Jun 01 2023 Packit <hello@packit.dev> - 293-1
- Tests and code quality improvements

* Tue May 16 2023 Packit <hello@packit.dev> - 292-1
- Metrics: Add disk IO per service
- Several right-to-left language fixes

* Wed May 03 2023 Packit <hello@packit.dev> - 291-1
- Update to PatternFly 5 Alpha

* Wed Apr 19 2023 Packit <hello@packit.dev> - 290-1
- Login page: Add autocomplete tags
- webserver: Disallow direct URL logins with LoginTo=false

* Wed Apr 05 2023 Packit <hello@packit.dev> - 289-1
- Metrics: Indicate high usage and use colorblind-friendly colors
- Accounts: Improve password validation

* Fri Mar 24 2023 Packit <hello@packit.dev> - 288.1-1
- Fix broken "SELinux" menu entry

* Thu Mar 23 2023 Packit <hello@packit.dev> - 288-1
- Accounts: Show shell and home directory on detail page
- Accounts: Custom user ID during account creation
- Overview: Support additional timeservers with chronyd
- Metrics: Show longer time span by default
- Storage: Mounting filesystems at boot time
- Services: Units need to be re-pinned
- API removal: Remove cockpit.dbus.publish() and .meta()
- Development: Cockpit now supports the esbuild bundler

* Thu Mar 09 2023 Packit <hello@packit.dev> - 287-1
- Metrics: Column visiblity
- Services: Pinned units need to be re-done

* Wed Feb 22 2023 Packit <hello@packit.dev> - 286-1
- Metrics page: control visibility of the resource usage graphs

* Wed Feb 08 2023 Packit <hello@packit.dev> - 285-1
- Cryptographic subpolicies support
- users: Group creation and filtering support

* Wed Jan 25 2023 Packit <hello@packit.dev> - 284-1
- Services: Show logs for user units
- Storage: Set up a system to use NBDE

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 283-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Packit <hello@packit.dev> - 283-1
- Services: Create timer to run every minute

* Wed Dec 14 2022 Packit <hello@packit.dev> - 282-1
- Add right-to-left language support
- Accounts: Redesign and include groups


* Thu Dec 01 2022 Packit <hello@packit.dev> - 281-1
- Dark theme switcher


* Thu Nov 24 2022 Packit <hello@packit.dev> - 280.1-1
- Exclude kpatch test on RHEL gating


* Wed Nov 16 2022 Packit <hello@packit.dev> - 280-1
- tools: Disallow root login by default


* Mon Nov 07 2022 Packit <hello@packit.dev> - 279-1
- Dark theme support


* Wed Oct 19 2022 Packit <hello@packit.dev> - 278-1
- Metrics: Display individual disk read/write usage


* Wed Sep 21 2022 Packit <hello@packit.dev> - 277-1
- Performance and stability improvements


* Mon Sep 12 2022 Packit <hello@packit.dev> - 276.1-1
 - login: Use valid selectors when testing for :is() / :where() support.


* Wed Sep 07 2022 Packit <hello@packit.dev> - 276-1
 - Stability and performance improvements


* Wed Aug 24 2022 Packit <hello@packit.dev> - 275-1
- shell: Support for alternatives to sudo


* Mon Aug 08 2022 Packit <hello@packit.dev> - 274.1-1
- cockpit-client: Support WebKit 4.1 API


* Wed Aug 03 2022 Packit <hello@packit.dev> - 274-1
- ws: Fix segfault with channel closing (#17492)
- Services: Fix time picker behaviour in Timer creation dialog
- Metrics: Improve CPU temperature sensors detection


* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 273-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 20 2022 Packit <hello@packit.dev> - 273-1
- Metrics: Display CPU temperature
- Networking: Suggest netmask and gateway addresses
- Software Updates: Optionally reboot after updating
- cockpit/ws container: Support modern SSH keys


* Thu Jun 23 2022 Packit <hello@packit.dev> - 272-1
- Firewall: Edit custom services
- Services: Pin services as favorites
- Login: Dark mode
- Unprivileged cockpit/ws container mode


* Wed Jun 08 2022 Packit <hello@packit.dev> - 271-1
- Tests improvements and stabilization


* Tue May 24 2022 Packit <hello@packit.dev> - 270-1
- Services: User-created timer deletion
- System Diagnostics: Working with diagnostic reports has been improved


* Thu May 12 2022 Cockpit Project <cockpituous@gmail.com> - 269-1
- Update to upstream 269 release

* Thu Apr 28 2022 Cockpit Project <cockpituous@gmail.com> - 268.1-1
- Update to upstream 268.1 release

* Thu Apr 28 2022 Cockpit Project <cockpituous@gmail.com> - 268-1
- Update to upstream 268 release

* Wed Apr 13 2022 Cockpit Project <cockpituous@gmail.com> - 267-1
- Update to upstream 267 release

* Wed Mar 30 2022 Cockpit Project <cockpituous@gmail.com> - 266-1
- Update to upstream 266 release

* Wed Mar 16 2022 Cockpit Project <cockpituous@gmail.com> - 265-1
- Update to upstream 265 release

* Fri Feb 25 2022 Cockpit Project <cockpituous@gmail.com> - 264-1
- Update to upstream 264 release

* Wed Feb 16 2022 Cockpit Project <cockpituous@gmail.com> - 263-1
- Update to upstream 263 release

* Wed Feb 02 2022 Cockpit Project <cockpituous@gmail.com> - 262-1
- Update to upstream 262 release

* Mon Jan 24 2022 Cockpit Project <cockpituous@gmail.com> - 261-1
- Update to upstream 261 release

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 260-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Martin Pitt <mpitt@redhat.com> - 260-1
- Certificate login validation: Action required on updates
- Client: Show previously used hosts
- Client: Support port specification
- bridge: Warning on missing cockpit-system package

* Wed Dec 08 2021 Marius Vollmer <mvollmer@redhat.com> - 259-1
- storage: More information in table rows

* Wed Nov 24 2021 Allison Karlitskaya <allison.karlitskaya@redhat.com> - 258-1
- Tweak login screen UI
- Use official VDO LVM API
- Add cockpit-client, to be bundled as a flatpak

* Wed Nov 10 2021 Katerina Koukiou <kkoukiou@redhat.com> - 257-1
- Support for reading TLS certificates with any permissions
- cockpit-ws no longer supports merged certificates
- Services: Show user-owned systemd units

* Wed Oct 27 2021 Jelle van der Waa <jvanderwaa@redhat.com> - 256-1
- Clean up old self-signed certificates
- Storage: Add support for Stratis

* Fri Oct 15 2021 Martin Pitt <mpitt@redhat.com> - 255.1-1
- Fix realmd join dialog crash if given address is not the domain name

* Wed Oct 13 2021 Martin Pitt <mpitt@redhat.com> - 255-1
- FreeIPA-issued webserver certificates get auto-renewed

* Wed Sep 29 2021 Matej Marusak <mmarusak@redhat.com> - 254-1
- Overview: Move last login to Health Card
- Webserver: Restrict frame embedding to same origin
- Login: Add Arch Linux branding
- Users: Add login history

* Wed Sep 15 2021 Katerina Koukiou <kkoukiou@redhat.com> - 253-1
- SELinux: Dismiss multiple alerts

* Wed Sep 01 2021 Simon Kobyda <skobyda@redhat.com> - 252-1
- Webserver: Drop remotectl utility
- Shell: Show package version in ‘About web console’ modal
- Storage: Encryption is presented as a property of a Filesystem

* Wed Aug 18 2021 Marius Vollmer <mvollmer@redhat.com> - 251-1
- Update to upstream 251 release

* Wed Aug 04 2021 Martin Pitt <mpitt@redhat.com> - 250-1
- Shell: Improve admin switcher and session menu
- Software Updates: Introduce basic kpatch support

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 249-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Matej Marusak <mmarusak@redhat.com> - 249-1
- storage: Content table improvements
- common: Add Content-Type for wasm
- all: Port away from Moment.js

* Wed Jul 07 2021 Allison Karlitskaya <allison.karlitskaya@redhat.com> - 248-1
- Metrics: Install missing packages
- PAM: Deprecate `pam_cockpit_cert` module
- Build system cleanups

* Wed Jun 23 2021 Katerina Koukiou <kkoukiou@redhat.com> - 247-1
- Metrics: Enable Grafana client setup
- Machines: Share host files with the guest using virtio-fs
- Machines: Show list of pass-through devices


* Wed Jun 09 2021 Marius Vollmer <mvollmer@redhat.com> - 246-1
- Improvements to the build system
- Polish of the Services and Storage pages
- Updated translations


* Wed May 26 2021 Martin Pitt <mpitt@redhat.com> - 245-1
- Metrics: New PCP configuration dialog
- Storage: Show both SHA256 and SHA1 Tang fingerprints
- Release: No more cockpit-cache tarball


* Sun May 16 2021 Martin Pitt <mpitt@redhat.com> - 244.1-1
- storage: use SHA256 for Tang fingerprints
- testlib: Eliminate dataclass for RHEL/CentOS 8 compatibility


* Wed May 12 2021 Katerina Koukiou <kkoukiou@redhat.com> - 244-1
- Shell: sudo is invoked only when explicitly requested


* Wed Apr 28 2021 Martin Pitt <mpitt@redhat.com> - 243-1
- Services: Show sockets and memory usage
- Developer API: Watch for file changes without reading


* Wed Apr 14 2021 Matej Marusak <mmarusak@redhat.com> - 242-1
- Support for pages built with snowpack
- Machines: Split out to separate project


* Wed Mar 31 2021 Simon Kobyda <skobyda@redhat.com> - 241-1
- kdump: redesign the page


* Wed Mar 17 2021 Marius Vollmer <mvollmer@redhat.com> - 240-1
- New localization: Norwegian Bokmål
- Performance metrics: Journal integration
- Machines: support authentication against cloud images

* Wed Mar 03 2021 Martin Pitt <mpitt@redhat.com> - 239-1
- Terminal: Support for changing the font size
- Machines: Allow editing disk cache mode
- Logs: Link to related services page
- SELinux: Restyle to resemble other pages
- Packaging: Removed ./configure options for distribution specific packages


* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 238.1-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 22 2021 Martin Pitt <mpitt@redhat.com> - 238.1-1
- Several UI alignment fixes
- Updates: Show PackageKit errors properly
- Re-drop unit tests from built packages
- Metrics: Don't show swap column when no swap is present
- Metrics: Don't show duplicate events


* Wed Feb 17 2021 Katerina Koukiou <kkoukiou@redhat.com> - 238-1
- Updates: List outdated software that needs a restart
- Web server: Preserve permissions of administrator-provided certificates
- System: Performance page shows busiest CPU cores
- Machines: VM disk creation supports a custom path


* Thu Feb 04 2021 Matej Marusak <mmarusak@redhat.com> - 237-1
- Restyling updates page in preparation for upcoming features
- SSH connections to remote machines are only opened when necessary


* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 236-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 21 2021 Martin Pitt <mpitt@redhat.com> - 236-1
- fslist channels: Include properties of changed files
- Internal stabilization work


* Thu Jan 07 2021 Martin Pitt <mpitt@redhat.com> - 235-1
- Login: Improved handling of SSH host keys
- Overview: Editable motd


* Wed Dec 09 2020 Marius Vollmer <mvollmer@redhat.com> - 234-1
- machines: Allow editing VM's CPU mode and model
- machines: Add support for cloning VMs
- dashboard: So long

* Thu Nov 26 2020 Katerina Koukiou <kkoukiou@redhat.com> - 233.1-1
- Machines: Fix CSS regression on the VMs details page
- One test fix for the metrics page


* Thu Nov 26 2020 Cockpit Project <cockpituous@gmail.com> - 233-1
- Update to upstream 233 release

* Wed Nov 11 2020 Katerina Koukiou <kkoukiou@redhat.com> - 232-1
- Improved host editing
- Machines: Inline error messages


* Thu Oct 29 2020 Matej Marusak <mmarusak@redhat.com> - 231-1
- Replace system's graph page with a completely new USE method page
- Machines: Reimplement the design of the main VMs list
- Logging of remote IP addresses


* Wed Oct 14 2020 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 230-1
- storage: List entries from /etc/crypttab that are still locked


* Wed Sep 30 2020 Marius Vollmer <mvollmer@redhat.com> - 229-1
-  shell: Any page can be the shell


* Wed Sep 16 2020 Katerina Koukiou <kkoukiou@redhat.com> - 228-1
- Accounts: Allow setting weak passwords
- Changes to remote host logins
- Machines: Add support for reverting and deleting VM snapshots
- Drop cockpit-docker code


* Wed Sep 02 2020 Martin Pitt <mpitt@redhat.com> - 227-1
- Machines: Virtual machine list filtering
- Continued PatternFly 4 migration


* Wed Aug 19 2020 Marius Vollmer <mvollmer@redhat.com> - 226-1
- Storage: Better support for "noauto" LUKS devices


* Wed Aug 05 2020 Matej Marusak <mmarusak@redhat.com> - 225-1
- machines: Add support for VM snapshots
- developer API: Launch and reattach to a long-running process


* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 224-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 224-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Katerina Koukiou <kkoukiou@redhat.com> - 224-1
- machines/services: Multiple bug fixes


* Wed Jul 08 2020 Katerina Koukiou <kkoukiou@redhat.com> - 223-1
- Webserver: Standard-conformant lifetime of web server Certificate
- Certificate authentication against Active Directory


* Fri Jun 26 2020 Martin Pitt <mpitt@redhat.com> - 222.1-1
- Machines: Fix crash on unset 'ui' property
- Some integration test fixes for dist-git gating


* Wed Jun 24 2020 Martin Pitt <mpitt@redhat.com> - 222-1
- Logs: More flexible text filters
- Services, Dashboard: Hide some buttons when access is limited
- Webserver: Lock down cockpit.service privileges


* Mon Jun 15 2020 Martin Pitt <mpitt@redhat.com> - 221.1-1
- Put back missing base1/patternfly.css
- Services: Don't offer 'Start Service' in Limited Access mode


* Wed Jun 10 2020 Marius Vollmer <mvollmer@redhat.com> - 221-1
- Support for Cross-Origin-Resource-Policy
- Accounts: Some buttons are hidden when access is limited
- Developers: Importing "base1/patternfly.css" is deprecated


* Wed May 27 2020 Matej Marusak <mmarusak@redhat.com> - 220-1
- New navigation with integrated switching of hosts
- Logs: Inline help for filtering
- Storage: Improve side panel on details page


* Wed May 13 2020 Katerina Koukiou <kkoukiou@redhat.com> - 219-1
- Logs: Improved filtering
- Gain or drop administrative access in a running Cockpit session


* Wed Apr 29 2020 Martin Pitt <mpitt@redhat.com> - 218-1
- Services: Improved accessibility and mobile support
- Overview: Add uptime information
- Disable idle timeout by default
- Support building without polkit


* Wed Apr 15 2020 Marius Vollmer <mvollmer@redhat.com> - 217-1
- verview: more Insights details
- ialogs: new button order
- achines: sendings keys to VM consoles


* Wed Apr 01 2020 sanne raymaekers <sanne.raymaekers@gmail.com> - 216-1
- SELinux: Automatic application of solutions that set booleans
- Machines: Drop virsh backend support
- Overview: New “last login” banner


* Wed Mar 18 2020 Katerina Koukiou <kkoukiou@redhat.com> - 215-1
- Networking: Show additional ports for each firewall zone


* Thu Mar 12 2020 Martin Pitt <mpitt@redhat.com> - 214.1-1
- Updates: Fix unstyled button regression
- Machines: Fix slow requests when enabling polkit access driver
- Deprecate cockpit-docker for Fedora, Debian, and Ubuntu development series


* Wed Mar 04 2020 Martin Pitt <mpitt@redhat.com> - 214-1
- Networking: List Firewall active zones when unprivileged
- Start Selenium tests deprecation


* Wed Feb 19 2020 Marius Vollmer <mvollmer@redhat.com> - 213-1
- Inline documentation
- Support for transient virtual machines
- UEFI for virtual machines
- Unattended virtual machines installation


* Wed Feb 05 2020 sanne raymaekers <sanne.raymaekers@gmail.com> - 212-1
- Per page documentation
- Localize times


* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 211.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 25 2020 Martin Pitt <mpitt@redhat.com> - 211.1-1
- system: Fix graph layout across all browsers (rhbz#1792623)
- websocket: Fix unaligned access in send_prefixed_message_rfc6455()


* Wed Jan 22 2020 Martin Pitt <mpitt@redhat.com> - 211-1
- Better support for various TLS certificate formats
- Switch from Zanata to Weblate
- Overview layout optimizations


* Wed Jan 08 2020 Katerina Koukiou <kkoukiou@redhat.com> - 210-1
- Overview: Add CPU utilization to usage card
- Dashboard: Support SSH identity unlocking when adding new machines
- SElinux: Introduce an Ansible automation script
- Machines: Support “bridge” type network interfaces
- Machines: Support “bus” type disk configuration


* Fri Dec 13 2019 Marius Vollmer <mvollmer@redhat.com> - 209-1
- New overview design
- Session timeouts
- Banners on login screen
- Client certificate authentication
- Support for Fedora CoreOS
- Dropped support for pam_rhost


* Wed Nov 27 2019 Martin Pitt <mpitt@redhat.com> - 208-1
- Storage: Drop “default mount point” concept
- Machines: Support transient virtual networks and storage pools
- Machines: Sliders for disk size and memory in VM creation
- Logs: Improve crash reporting


* Wed Nov 13 2019 Katerina Koukiou <kkoukiou@redhat.com> - 207-1
- Web server: Accept EC certificates
- Storage: List all software devices in a single panel
- Redesigned notifications


* Wed Oct 30 2019 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 206-1
- Machines: Network interface deletion
- login: Enable administration mode by default
- Firewall: Prevent accidental deletion


* Thu Oct 17 2019 Martin Pitt <mpitt@redhat.com> - 205.1-1
- Fix web server slowness/crash bugs with TLS connections


* Wed Oct 16 2019 Simon Kobyda <skobyda@redhat.com> - 205-1
- Firewall: UI restructuring
- Machines: Refactor Create VM dialog and introduce a download option
- Adjust menu to PatternFly's current navigation design
- Searching with keywords
- Software Updates: Use notifications for available updates info
- Web server security hardening


* Wed Oct 02 2019 Martin Pitt <mpitt@redhat.com> - 204-1
- System: Highlight failed services
- Machines: Configure read-only and shareable disks
- Playground: Add index page


* Wed Sep 18 2019 Marius Vollmer <mvollmer@redhat.com> - 203-1
- shell: Display message when websocket fails early
- machines: Implement adding virtual network interfaces


* Mon Sep 09 2019 Martin Pitt <mpitt@redhat.com> - 202.1-1
- Fix major CSS regression on Logs and some other pages
- Fix building on RHEL/CentOS 7


* Wed Sep 04 2019 Katerina Koukiou <kkoukiou@redhat.com> - 202-1
- Machines: Creation of Storage Volumes
- Improved component for selecting paths on the filesystem


* Wed Aug 21 2019 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 201-1
- Machines: VM creation and import dialog changes
- Machines: Enable interface type "direct" in NIC configuration
- systemd: Add more actions to services


* Wed Aug 07 2019 Martin Pitt <mpitt@redhat.com> - 200-1
- Machines: Type-ahead OS selection
- Machines: LVM storage pools
- Networking: Show included firewalld services
- Web server: Split out TLS handling


* Thu Jul 25 2019 Martin Pitt <mpitt@redhat.com> - 199-1
- Redesigned logs all over cockpit
- Services: Design and accesibility improvements
- System: Show DIMM information on Hardware Info page
- Machines: VM creation dialog now shows the recommended memory for the selected OS
- cockpit-docker: Avoid file dependency (rhbz#1731686)


* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 198-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Martin Pitt <mpitt@redhat.com> - 198-1
- PatternFly4 user interface design
- SELinux: Show changes
- Machines: Deletion of Virtual Networks
- Machines: Support more disk types
- Docker: Change menu label
- Web server: More flexible https redirection for proxies


* Wed May 15 2019 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 194-1
- Firewall: Add services to a specific zone
- Redesigned on/off switch


* Thu May 02 2019 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 193-1
- Machines: iSCSI direct storage pools
- Storage: The "Format" button is no longer hidden
- Storage: Improve performance with many block devices


* Wed Apr 17 2019 Martin Pitt <mpitt@redhat.com> - 192-1
- Machines: Auto-detect guest operating system
- Translation cleanup
- Allow accounts with non-standard shells


* Wed Apr 03 2019 Marius Vollmer <mvollmer@redhat.com> - 191-1
- Machines: iSCSI Storage pools
- Machines: better notifications
- System: CPU security mitigation
- Network: Ports in the Firewall


* Fri Mar 22 2019 Katerina Koukiou <kkoukiou@redhat.com> - 190-1
- Logs: Filter log entries by service
- Machines: Support for Pausing/Resuming VMs
- Machines: Make Autostart property of a Virtual Network configurable
- Machines: Support for creating VM with option to boot from PXE
- Accessibility improvements


* Wed Mar 06 2019 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 189-1
- Machines: Import existing image when creating VM
- Machines: Introduce virtual networks
- Services: Filtering of services by name, description, and state


* Wed Feb 20 2019 Martin Pitt <mpitt@redhat.com> - 188-1
- Machines: Show Storage Volume user
- Machines: Autostart configuration
- Terminal: Themes and context menu
- Storage: Responsive dialogs
- Software Updates: Show three most recent updates


* Wed Feb 06 2019 Marius Vollmer <mvollmer@redhat.com> - 187-1
- Machines: More operations for Storage Pools
- Domains: More information about the joined domain
- Storage: The options for VDO volumes are explained
- Machines: Support for oVirt will be dropped in the future


* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 185-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 16 2019 Björn Esser <besser82@fedoraproject.org> - 185-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Jan 09 2019 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 185-1
- Responsive dialogs on network, kdump and users page
- Kubernetes containers included in docker graphs


* Thu Dec 13 2018 Martin Pitt <martin@piware.de> - 184-1
- Machines: Dialog and tab layout is now responsive
- Storage: Filesystem labels are validated upfront
- Storage: Some mount options are prefilled when needed
- Integration of Cockpit pages on the desktop


* Wed Nov 28 2018 Martin Pitt <martin@piware.de> - 183-1
- Machines: Manage storage pools
- Kernel Dump: Support non-local targets
- Respect SSH configuration
- Never send Content-Length with chunked encoding


* Wed Nov 14 2018 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 182-1
- libvirt connection choice during VM creation
- PackageKit page update severity tooltip
- PackageKit page display registration status clearly


* Wed Oct 31 2018 Marius Vollmer <mvollmer@redhat.com> - 181-1
- Followup fixes related to the switch away from react-lite
- Graph layout and color improvements
- Machines: edit network interfaces
- Update look of lists to match Patternfly


* Fri Oct 12 2018 Martin Pitt <martin@piware.de> - 180-1
- Move to ssh SHA256 fingerprints
- Machines: Show error messages in the correct place


* Thu Oct 04 2018 Sanne Raymaekers <sanne.raymaekers@gmail.com> - 179-1
- Machines: Detach disk from VM with LibvirtDBus provider
- Machines: Offer cockpit-machines as Application

* Wed Sep 19 2018 Marius Vollmer <mvollmer@redhat.com> - 178-1
- Dropped support for KubeVirt


* Wed Sep 05 2018 Martin Pitt <martin@piware.de> - 177-1
- Storage: Support LUKS v2
- Support centrally-managed SSH known hosts
- Drop support for Internet Explorer


* Wed Aug 08 2018 Marius Vollmer <mvollmer@redhat.com> - 175-1
- Network bound disk encryption


* Wed Aug 01 2018 Marius Vollmer <mvollmer@redhat.com> - 174-1
- Kubernetes: VM detail page
- Realmd: Install on demand


* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 173-3
- Rebuild with fixed binutils

* Sat Jul 28 2018 Martin Pitt <martin@piware.de> - 173-2
- Drop firewalld service (moved to firewalld), add corresponding conflict
  rhbz#1609393
- Fix CI pipeline tests

* Wed Jul 25 2018 Martin Pitt <martin@piware.de> - 173-1
- Storage: Offer installation of VDO
- Machines: Add disks to a virtual machine


* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 171-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Martin Pitt <martin@piware.de> - 171-1
- Machines: Add virtual CPU configuration
- Kubernetes: Add KubeVirt pod metrics
- Docker: Show container volumes
- Fix broken actions for non-administrators
- Networking: Handle non-running NetworkManager
- Accounts: User role improvements
- Localize times


* Wed Jun 13 2018 Martin Pitt <martin@piware.de> - 170-1
- Software Updates: Layout rework
- oVirt: Use authenticated libvirt connection by default


* Wed May 16 2018 Martin Pitt <martin@piware.de> - 168-1
- Improve checks for root privilege availability


* Wed May 02 2018 Martin Pitt <martin@piware.de> - 167-1
- Networking: Add Firewall Configuration
- Kubernetes: Show Kubevirt Registry Disks


* Wed Apr 18 2018 Martin Pitt <martin@piware.de> - 166-1
- Kubernetes: Add creation of Virtual Machines
- Realms: Automatically set up Kerberos keytab for Cockpit web server
- Numbers now get formatted correctly for the selected language


* Wed Apr 04 2018 Martin Pitt <martin@piware.de> - 165-1
- Storage: Show more details of sessions and services that keep NFS busy
- Machines: Detect if libvirtd is not running
- Machines: Show virtual machines that are being created


* Wed Mar 21 2018 Martin Pitt <martin@piware.de> - 164-1
- Storage: Move NFS management into new details page
- System: Show available package updates and missing registration
- System: Fix inconsistent tooltips
- Logs: Change severities to officially defined syslog levels
- Machines: Add error notifications
- Accessibility improvements
- Reloading the page in the browser now reloads Cockpit package manifests


* Wed Mar 07 2018 Martin Pitt <martin@piware.de> - 163-1
- Drop "Transfer data asynchronously" VDO option on Storage page
- Hide Docker storage pool reset button when it cannot work properly
- Update jQuery to version 3.3.1 (deprecated cockpit API!)


* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 161-2
- Escape macros in %%changelog

* Wed Feb 07 2018 Martin Pitt <martin@piware.de> - 161-1
- New VMs can be created on Machines page
- VMs running in Kubernetes can now be deleted
- Improve LVM volume resizing
- Add new Hardware Information page
- Load Application metadata (Appstream) packages on demand on Debian/Ubuntu
- Rename cockpit-ovirt package to cockpit-machines-ovirt
- Stop advertising and supporting cockpit-bundled jQuery library


* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 160-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 24 2018 Martin Pitt <martin@piware.de> - 160-1
- Add kubevirt Virtual Machines overview
- Redesign package list on Software Updates page and show RHEL Errata
- Install AppStream collection metadata packages on demand on Apps page
- Add AppStream metadata to cockpit-sosreport for showing up on Apps page
- Change CPU graphs to use "100%%" for a fully loaded multi-processor system
- Show storage, network, and other numbers with 3 digits of precision
- Add an example bastion container


* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 159-2
- Rebuilt for switch to libxcrypt

* Wed Jan 10 2018 Martin Pitt <martin@piware.de> - 159-1
- Configure data deduplication with VDO devices on Storage page
- Add serial console to virtual Machines page and redesign the Consoles tab
- Show more error message details for failures on virtual Machines page


* Wed Dec 13 2017 Martin Pitt <martin@piware.de> - 158-1
- Add check boxes for common NFS mount options
- Clarify Software Update status if only security updates are available
- Create self-signed certificates with SubjectAltName


* Thu Nov 30 2017 Martin Pitt <martin@piware.de> - 157-1
- Add Networks tab to overview on Machines page
- The Apps page now displays SVG app icons


* Thu Nov 16 2017 Martin Pitt <martin@piware.de> - 156-1
- Redesign navigation and support mobile browsing
- Use /etc/cockpit/krb5.keytab if present to support alternate keytabs
- Add project homepage link to Apps page
- Maintain issue(5) file with current Cockpit status
- Use event-driven refresh of oVirt data instead of polling


* Tue Nov 07 2017 Martin Pitt <martin@piware.de> - 155-1
- Add NFS client support to the Storage page
- Add "Maintenance" switch for oVirt hosts
- Fix Terminal rendering issues in Chrome
- Prevent closing Terminal with Ctrl+W when focused
- Support the upcoming OpenShift 3.7 release


* Wed Oct 18 2017 Martin Pitt <martin@piware.de> - 154-1
- Center the "Disconnected" message in the content area
- Fix two layout regressions on the Cluster page
- Remove long-obsolete "./configure --branding" option


* Tue Oct 17 2017 Martin Pitt <martin@piware.de> - 153-1
- Add cockpit-ovirt package to control oVirt virtual machine clusters
- Clean up rpmlint/lintian errors in the packages


* Fri Oct 06 2017 Martin Pitt <martin@piware.de> - 152-1
- Add Applications page
- Add automatic update configuration for dnf to Software Updates
- Fix cockpit-bridge crash if /etc/os-release does not exist


* Mon Sep 25 2017 Stef Walter <stefw@redhat.com> - 151-2
- Add simulated test failure

* Thu Sep 21 2017 Martin Pitt <martin@piware.de> - 151-1
- Support loading SSH keys from arbitrary paths
- Support X-Forwarded-Proto HTTP header for Kubernetes
- Fix Kubernetes connection hangs (regression in version 150)


* Fri Sep 08 2017 Martin Pitt <martin@piware.de> - 150-1
- Automatically enable and start newly created timers on the Services page
- Support cockpit-dashboard installation into OSTree overlay on Atomic
- Support Kubernetes basic auth with Google Compute Engine 1.7.x


* Mon Aug 21 2017 petervo <petervo@redhat.com> - 149-1
- Support sending non-maskable interrupt to VMs
- Fix building on fedora 27
- Add information about non-met conditions for systemd services
- Clear cockpit cookie on logout

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 146-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 146-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Martin Pitt <martin@piware.de> - 146-1
- Show recent updates and live update log on Software Updates page
- Improve available Software Updates table layout for small/mobile screens
- Support OAuth Kubernetes logins to work with Google Compute Engine
- Fix reporting ABRT crashes that are already known to the server
- Scroll the virtual machine VNC console into view automatically


* Fri Jul 07 2017 Martin Pitt <martin@piware.de> - 145-1
- Resize the terminal dynamically to use all available space
- Let the Machines page update immediately after changes
- Add delete VM functionality to the Machines page
- Retire support for external Machines provider API
- Always recommend rebooting after applying Software Updates
- Group D-Bus channels to avoid hitting connection limits
- Fix building on Fedora Rawhide/glibc 2.25.90


* Mon Jun 19 2017 Martin Pitt <<martin@piware.de>> - 143-1
- Add "Software Updates" page for package (rpm/deb) based operating systems
- Fix cockpit-machines package to make inline VNC console actually work
- Fix Kubernetes authentication when Kubernetes configured for RBAC
- Build Docker page for s390x architecture


* Fri Jun 09 2017 Martin Pitt <<martin@piware.de>> - 142-1
- Virtual machines display an interactive console, either in browser, or a popup viewer
- Fix Virtual Machines operations on non-English locales
- Add documentation explaining how to grant/restrict access via polkit rules


* Fri Apr 21 2017 Martin Pitt <<mpitt@redhat.com>> - 139-1
- Show more information about virtual machines, such as boot order
- Fix enablement of timer systemd units created on Services page
- Fix Storage crash on multiple iSCSI sessions
- cockpit-docker is now installable with docker-ce or other alternatives
- Hide docker push commands on Registry image pages for  "pull" roles


* Mon Apr 10 2017 Stef Walter <<stefw@redhat.com>> - 138-1
- Only allow mdraid disk removal when it won't destroy data
- Allow DN style usernames in the Kubernetes dashboard
- Simplify protocol that cockpit talks to session authentication processes

* Thu Mar 30 2017 Martin Pitt <<mpitt@redhat.com>> - 137-1
- Read ~/.ssh/known_hosts for connecting to remote machines with ssh
- The Storage LVM setup can add unpartitioned free space as a physical volume
- NetworkManager's Team plugin can be used on architectures other than x86_64
- Cockpit's web server understands and properly responds to HTTP HEAD requests
- Allow parameter substitution in manifest when spawning peer bridges


* Thu Mar 09 2017 Martin Pitt <<mpitt@redhat.com>> - 134-1
- Show /etc/motd in the "System" task page
- Drop "System" service actions which are intended for scripts
- Make login page translatable
- NetworkManager now activates slave interfaces by itself
- Add call timeout option to the cockpit.dbus() API
- The Debian packaging is now able to apply binary patches


* Thu Mar 02 2017 Martin Pitt <<mpitt@redhat.com>> - 133-1
- Remotely managed machines are now configured in /etc/cockpit/machines.d/*.json
- Fix NetworkManager's "MTU" dialog layout
- Build the cockpit-tests package for releases too
- Split translations into individual packages
- Packages now configure alternate cockpit-bridge's to interact with the system


* Thu Feb 23 2017 Martin Pitt <<mpitt@redhat.com>> - 132-1
- Make basic SELinux functionality available without setroubleshootd
- Allow changing the MAC address for ethernet adapters and see them for bonds
- Hide "autoconnect" checkbox for network devices without settings
- Support for external providers other than libvirt on Machines page
- Some tooltip fixes
- Add option to restrict max read size to the Cockpit file API
- Relax dependencies on cockpit-bridge package on Debian/Ubuntu
- Rename cockpit-test-assets package to cockpit-tests
- When touching patched files handle case of only one file
- Always build the cockpit-tests subpackage


* Mon Feb 06 2017 Stef Walter <<stefw@redhat.com>> - 131-1
- Show session virtual machines on Machines page
- Fix use of the TAB key on login page
- Robust naming and detection of network bond master
- Debian packaging fixes

* Wed Jan 25 2017 Stef Walter <<stefw@redhat.com>> - 130-1
- cockpit.file() can read non-memory-mappable file
- Add kdump configuration user interface
- Allow container Registry Console user names with '@' sign

* Wed Jan 18 2017 Stef Walter <<stefw@redhat.com>> - 129-1
- Diagnostic sosreport feature now works on RHEL Atomic again
- The configure script has a --disable-ssh option to toggle libssh dep
- The configure --disable-ws option has been replaced with above.
- Unit tests have been fixed on recent GLib versions
- Several Fedora and Debian packaging fixes

* Wed Dec 14 2016 Stef Walter <<stefw@redhat.com>> - 126-1
- Show security scan information about containers
- Choose whether password is cached and reused on login screen
- Allow renaming of active devices in networking interface
- More clearly indicate when checking network connectivity
- The remotectl command can now combine certificate and key files
- Support Openshift's certificate autogeneration when used as a pod
- The remotectl tool now checks for keys in certificate files
- Domain join operations can now be properly cancelled
- Make Kerberos authentication work even if gss-proxy is in use
- Javascript code can now export DBus interfaces
- When proxied, support X-Forwarded-Proto
- Ignore block devices with a zero size in the storage interface

* Thu Nov 24 2016 Stef Walter <<stefw@redhat.com>> - 125-1
- Cockpit is now properly translatable
- Display OSTree signatures
- New expandable views for storage devices
- No longer offer to format read-only block devices
- Use stored passphrases for LUKS devices properly
- Start testing on RHEL 7.3
- More strict about transport channels a bridge accepts
- System shutdown can be scheduled by date

* Wed Nov 16 2016 Stef Walter <<stefw@redhat.com>> - 124-1
- Build and test on Debian Jessie
- Deprecate older javascript files
- Properly terminate user sessions on the Accounts page
- Fix regression on login screen in older Internet Explorer browsers
- Fix regression where Date Picker was not shown in System Time dialog

* Thu Nov 10 2016 Stef Walter <<stefw@redhat.com>> - 123-1
- Release a second tarball with cached javascript dependencies
- Start verifying that Cockpit works on Ubuntu 16.04
- Enable and verify the network functionality on Debian
- Integration tests now log core dumps for diagnosis

* Tue Nov 01 2016 Stef Walter <stefw@redhat.com> - 122-1
- Works with UDisks in addition to storaged
- Allow logging into other systems from login page
- Explicitly specify javascript dependency versions

* Fri Oct 28 2016 Stef Walter <stefw@redhat.com> - 121-1
- Network Manager Checkpoints
- Add Debian Branding
- Fix GSSAPI login on Debian and Ubuntu
- Generate map files for debugging Javascript and CSS

* Sat Oct 22 2016 Stef Walter <stefw@redhat.com> - 120-1
- New containers page layout
- Quick filtering of containers and images on the container page
- Added sidebar for phisical volumes in a volume group
- Run a separate cockpit-ssh process when making SSH connections
- Allow connecting to remote machines from the login page
- Only connect to remote machines already known to Cockpit
- Fix bugs preventing journal page from working on Firefox 49
- Add tooltip describing group name in Roles list

* Sat Oct 01 2016 Dennis Gilmore <dennis@ausil.us> - 119-2
- enabled cockpit-docker on aarch64, ppc64, ppc64le

* Thu Sep 29 2016 petervo <petervo@redhat.com> - 119-1
- Adds basic VM Management and Monitoring
- MDRaid job improvements
- Show unmanaged network devices
- Better errors when formating storage devices
- Updated VNC example
- Port subscriptions package to react
- Allow branding.css to overide shell css

* Wed Sep 07 2016 Stef Walter <stefw@redhat.com> - 118-1
- Support PAM conversations on the Login screen
- Users can create systemd timer jobs
- Provide default names for volume groups and logical volumes
- Make Docker graphs work on Debian
- Only offer to format disks with supported file systems
- Show all managed NetworkManager devices
- Use webpack for building Cockpit javascript
- Cockpit URLs can be proxied with a configured HTTP path prefix
- Allow Cockpit packages to require a minimum version of Cockpit
- Translations fixes

* Thu Aug 11 2016 Stef Walter <stefw@redhat.com> - 0.117-1
- * Add support for network teams
- * Select translations for complex language names
- * Don't allow formating extended partitions
- * Can configure Openshift Registry so anonymous users can pull images

* Fri Jul 29 2016 Stef Walter <stefw@redhat.com> - 0.116-1
- * Support for volumes when starting a docker container
- * Support for setting environment variables in a docker container
- * Fix regressions that broke display of localized text

* Thu Jul 21 2016 Stef Walter <stefw@redhat.com> - 0.115-1
- * Setup Docker container and image storage through the UI
- * Use Webpack to build Cockpit UI packages
- * Update the Cockpit Vagrant development box to use Fedora 24

* Tue Jul 12 2016 Stef Walter <stefw@redhat.com> - 0.114-1
- .104
- * Network configuration of the Ethernet MTU
- * Red Hat Subscriptions can now specify activation keys and orgs
- * Start integration testing on CentOS
- * SSH Host keys are show on system page
- * Machine ID is shown on system page
- * Show intelligent password score error messages

* Thu Jul 07 2016 Stef Walter <stefw@redhat.com> - 0.113-1
- * Show timer information for systemd timer jobs
- * Use 'active-backup' as the default for new network bonds
- * When changing system time check formats properly
- * Hide the machine asset tag when no asset exists
- * Disable the network on/off switch for unknown or unmanaged interfaces
- * Show full string for system hardware info and operating system name

* Wed Jun 29 2016 Stef Walter <stefw@redhat.com> - 0.112-1
- * Don't show network interfaces where NM_CONTROLLED=no is set
- * Add textual fields to container memory and CPU sliders
- * Display contianer memory and CPU resources on Debian
- * Disable tuned correctly when clearing a performance profile
- * Fix SELinux enforcing toggle switch and status

* Tue Jun 21 2016 Stef Walter <stefw@redhat.com> - 0.111-1
- * Tarball build issue in 0.110 is now fixed
- * The Containers page layouts have been tweaked
- * Make the Containers resource limits work again
- * Registry image now have layers displayed correctly

* Thu Jun 02 2016 Dominik Perpeet <dperpeet@redhat.com> - 0.109-1
- * API stabilization, structural cleanup
- * SELinux Troubleshooting: documentation, support latest API
- * Update Patternfly
- * Use CockpitLang cookie and Accept-Language for localization
- * Can now click through to perform administration tasks on Nodes on the Cluster dashboard
- * Cockpit terminal now supports shells like fish

* Fri May 27 2016 Stef Walter <stefw@redhat.com> - 0.108-1
- * SELinux troubleshooting alerts can now be dismissed
- * Show SELinux icon for critical alerts
- * SELinux enforcing mode can be turned off and on with a switch
- * Kubernetes Nodes are now include charts about usage data
- * Fix Debian dependency on Docker
- * Update the look and feel of the toggle switch
- * Update ListenStream documentation to include address info

* Fri May 20 2016 Stef Walter <stefw@redhat.com> - 0.107-1
- * Display image stream import errors
- * Add GlusterFS persistent volumes in Cluster dashboard
- * Show a list of pending persistent volume claims
- * jQuery Flot library is no longer part of the base1 package
- * Fix Content-Security-Policy issues with jQuery Flot

* Thu May 12 2016 Stef Walter <stefw@redhat.com> - 0.106-1
- * Add namespaces to cockpit CSS classes
- * Display container image layers in a simpler graph
- * Hide actions in Cluster projects listing that are not accessible

* Wed May 04 2016 Stef Walter <stefw@redhat.com> - 0.105-1
- * Strict Content-Security-Policy in all shipped components of Cockpit
- * Can now add and remove Openshift users to and from groups
- * Add timeout setting for Cockpit authentication
- * Registry interface now has checkbox for mirroring from insecure registries
- * Kubernetes dashboard now allows deletion of Nodes

* Thu Apr 28 2016 Stef Walter <stefw@redhat.com> - 0.104-1
- * Show errors correctly when deleting or modifying user accounts
- * Add support for iSCSI cluster volumes
- * Strict Content-Security-Policy in the dashboard, sosreport and realmd code
- * Better list expansion and navigation behavior across Cockpit
- * Don't show 'Computer OU' field when leaving a domain
- * Remove usage of bootstrap-select
- * Show errors properly in performance profile dialog
- * Fix Cluster sidebar to react to window size
- * Allow specifying specific tags in registry image streams
- * Make registry project access policy more visible

* Tue Apr 19 2016 Stef Walter <stefw@redhat.com> - 0.103-1
- * Strict Content-Security-Policy for subscriptions component
- * New dialog for Kubernetes connection configuration
- * Release to a cockpit-project Ubuntu PPA
- * Remove jQuery usage from cockpit.js
- * New styling for cluster dashboard
- * Fix build issue on MIPS

* Thu Apr 14 2016 Stef Walter <stefw@redhat.com> - 0.102-1
- * Can configure Docker restart policy for new containers
- * Use a single dialog for creating logical volumes
- * Package and test the storage UI on Debian
- * Don't offer 'Computer OU' when joining IPA domains
- * Don't distribute jshint build dependency due to its non-free license

* Fri Feb 12 2016 Stef Walter <stefw@redhat.com> - 0.95-1
- * iSCSI initiator support on the storage page
- * Page browser title now uses on operating system name
- * Better look when Cockpit disconnects from the server
- * Avoid use of NFS in the Vagrantfile
- * Expand 'Tools' menu when navigating to one of its items
- * Set a default $PATH in cockpit-bridge

* Tue Feb 02 2016 Stef Walter <stefw@redhat.com> - 0.94-1
- * Handle interruptions during cockpit-ws start while reading from /dev/urandom
- * Remove BIOS display from Server Summary page
- * Support tuned descriptions
- * Fix Content-Security-Policy in example manifest.json files

* Mon Jan 25 2016 Stef Walter <stefw@redhat.com> - 0.93-1
- * Set system performance profile via tuned
- * Support for WebSocket client in cockpit-bridge
- * Support using Nulecule with Openshift
- * Actually exit cockpit-ws when it's idle

* Wed Jan 20 2016 Stef Walter <stefw@redhat.com> - 0.92-1
- * OAuth login support
- * Update Patternfly
- * Log to stderr when no journal
- * Make sosreport work on RHEL and Atomic

* Thu Jan 14 2016 Stef Walter <stefw@redhat.com> - 0.91-1
- * Fix computing of graph samples on 32-bit OS
- * Distribute licenses of included components
- * Distribute development dependencies
- * Support 'make clean' properly in the tarball

* Tue Jan 05 2016 Stef Walter <stefw@redhat.com> - 0.90-1
- * Fix Content-Security-Policy which broke loading in certain situations
- * Deal correctly with failures trying to join unsupported domains
- * Add documentation about Cockpit startup
- * Better data in storage usage graphs
- * Start creating debian source packages

* Tue Dec 22 2015 Stef Walter <stefw@redhat.com> - 0.89-1
- * Start routine testing of Cockpit on Debian Unstable
- * Make the config file case insensitive
- * Reorder graphs on server summary page
- * Don't suggest syncing users when adding a machine to dashboard
- * Enable weak dependencies for F24+
- * Show correct data in per interface network graphs
- * Fix the Vagrantfile to pull in latest Cockpit
- * Add Content-Security-Policy header support

* Fri Dec 18 2015 Stef Walter <stefw@redhat.com> - 0.88-1
- * User interface for OSTree upgrades and rollbacks
- * General reusable purpose angular kubernetes client code
- * Allow custom login scripts for handling authentication
- * A specific dashboards can now be the default destination after login
- * Kill ssh-agent correctly when launched by cockpit-bridge
- * Add a new cockpit-stub bridge for non-local access

* Thu Dec 10 2015 Stef Walter <stefw@redhat.com> - 0.87-1
- * Fix login on Windows, don't prompt for additional auth
- * Use the machine host name in the default self-signed certificate
- * Cockpit release tarballs are now distributed in tar-ustar format
- * Allow overriding package manifests
- * Testing and build fixes

* Fri Dec 04 2015 Stef Walter <stefw@redhat.com> - 0.86-1
- * SOS report UI page
- * Simpler way for contributors to build cockpit RPMs
- * Infrastructure for implementing downloads

* Wed Nov 18 2015 Stef Walter <stefw@redhat.com> - 0.84-1
- * Add a cockpit manual page
- * Set correct SELinux context for certificates
- * Remove custom SELinux policy
- * Testing and bug fixes

* Tue Nov 03 2015 Stef Walter <stefw@redhat.com> - 0.83-1
- * Fix NTP server configuration bugs
- * Kubernetes dashboard topology icons don't leave the view
- * Kubernetes dashboard uses shared container-terminal component
- * Fix race when adding machine to Cockpit dashboard
- * Updated documentation for running new distributed tests
- * Lots of other bug and testing fixes

* Wed Oct 28 2015 Stef Walter <stefw@redhat.com> - 0.82-1
- * Support certificate chains properly in cockpit-ws
- * Rename the default self-signed certificate
- * Implement distributed integration testing

* Wed Oct 21 2015 Stef Walter <stefw@redhat.com> - 0.81-1
- * Allow configuring NTP servers when used with timesyncd
- * Fix regression in network configuration switches
- * Make the various graphs look better
- * Openshift Routes and Deployment Configs can be removed
- * Run integration tests using TAP "test anything protocol"
- * Lots of other bug fixes and cleanup

* Wed Oct 14 2015 Stef Walter <stefw@redhat.com> - 0.80-1
- * UI for loading, viewing, changing Private SSH Keys
- * Always start an ssh-agent in the cockpit login session
- * New listing panel designs
- * Lots of testing and bug fixes

* Wed Oct 07 2015 Stef Walter <stefw@redhat.com> - 0.79-1
- * Vagrant file for Cockpit development
- * Use libvirt for testing
- * Display only last lines of Kubernetes container logs

* Wed Sep 30 2015 Stef Walter <stefw@redhat.com> - 0.78-1
- * Fix extreme CPU usage issue in 0.77 release
- * Fix compatibility with older releases
- * Offer to activate multipathd for multipath disks
- * Guide now contains insight into feature internals
- * Lots of other minor bug fixes

* Wed Sep 23 2015 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 0.77-1.1
- disable FMA support to get it pass all tests on secondary architectures
- removed duplicated "global rel 1"

* Tue Sep 22 2015 Stef Walter <stefw@redhat.com> - 0.77-1
- * Work better with multipath storage
- * Deletion of kubernetes objects
- * Cleaner URLs in the bookmark bar
- * Show a warning when adding too many machines
- * Make authentication work when embedding Cockpit
- * Complete componentizing Cockpit

* Wed Sep 16 2015 Stef Walter <stefw@redhat.com> - 0.76-1
- * Fix displaying of network bonds
- * Better Kubernetes filter bar, shell access
- * Show some Openshift related objects
- * Use patternfly v2.2

* Thu Sep 10 2015 petervo <petervo@redhat.com> - 0.75-1
- New design for kubernetes listing pages
- Namespace filter for kubernetes
- Pretty http error pages
- Lots of bugs, build and testing fixes

* Thu Sep 03 2015 Stef Walter <stefw@redhat.com> - 0.74-1
- * Display an intelligent message when password auth is not possible
- * Correctly start terminal in home directory
- * NetworkManager code is in a separate package
- * PCP is an optional build dependency
- * Lots of bugs, build and testing fixes

* Wed Aug 26 2015 Stef Walter <stefw@redhat.com> - 0.73-1
- * Kubernetes UI can connect to non-local API server
- * Automate Web Service container build on Docker Hub
- * Add validation options to TLS client connections
- * PAM pam_ssh_add.so module for loading SSH keys based on login password
- * Build, testing and other fixes

* Mon Aug 17 2015 Peter <petervo@redhat.com> - 0.71-1
- Update to 0.71 release.

* Wed Aug 12 2015 Stef Walter <stefw@redhat.com> - 0.70-1
- Depend on kubernetes-client instead of kubernetes
- Update to 0.70 release.

* Thu Aug 06 2015 Stef Walter <stefw@redhat.com> - 0.69-1
- Update to 0.69 release.

* Wed Jul 29 2015 Peter <petervo@redhat.com> - 0.68-1
- Update to 0.68 release.

* Thu Jul 23 2015 Peter <petervo@redhat.com> - 0.66-1
- Update to 0.66 release

* Fri Jul 17 2015 Peter <petervo@redhat.com> - 0.65-2
- Require libssh 0.7.1 on fedora >= 22 systems

* Wed Jul 15 2015 Peter <petervo@redhat.com> - 0.65-1
- Update to 0.65 release

* Wed Jul 08 2015 Peter <petervo@redhat.com> - 0.64-1
- Update to 0.64 release

* Wed Jul 01 2015 Peter <petervo@redhat.com> - 0.63-1
- Update to 0.63 release
- Remove cockpit-docker for armv7hl while docker
  packages are being fixed

* Thu Jun 25 2015 Peter <petervo@redhat.com> - 0.62-1
- Update to 0.62 release

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.61-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 10 2015 Peter <petervo@redhat.com> - 0.61-1
- Update to 0.61 release

* Mon Jun 01 2015 Stef Walter <stefw@redhat.com> - 0.60-1
- Update to 0.60 release

* Wed May 27 2015 Peter <petervo@redhat.com> - 0.59-1
- Update to 0.59 release

* Fri May 22 2015 Peter <petervo@redhat.com> - 0.58-1
- Update to 0.58 release

* Wed May 20 2015 Peter <petervo@redhat.com> - 0.57-1
- Update to 0.57 release

* Wed May 13 2015 Peter <petervo@redhat.com> - 0.56-1
- Update to 0.56 release

* Wed May 06 2015 Stef Walter <stefw@redhat.com> - 0.55-1
- Update to 0.55 release

* Fri Apr 24 2015 Peter <petervo@redhat.com> - 0.54-1
- Update to 0.54 release

* Tue Apr 21 2015 Peter <petervo@redhat.com> - 0.53-1
- Update to 0.53 release

* Thu Apr 16 2015 Stef Walter <stefw@redhat.com> - 0.52-1
- Update to 0.52 release

* Tue Apr 14 2015 Peter <petervo@redhat.com> - 0.51-1
- Update to 0.51 release

* Tue Apr 07 2015 Stef Walter <stefw@redhat.com> - 0.50-1
- Update to 0.50 release

* Wed Apr 01 2015 Stephen Gallagher <sgallagh@redhat.com> 0.49-2
- Fix incorrect Obsoletes: of cockpit-daemon

* Wed Apr 01 2015 Peter <petervo@redhat.com> - 0.49-1
- Update to 0.49 release.
- cockpitd was renamed to cockpit-wrapper the cockpit-daemon
  package was removed and is now installed with the
  cockpit-bridge package.

* Mon Mar 30 2015 Peter <petervo@redhat.com> - 0.48-1
- Update to 0.48 release

* Mon Mar 30 2015 Stephen Gallagher <sgallagh@redhat.com> 0.47-2
- Don't attempt to build cockpit-kubernetes on armv7hl

* Fri Mar 27 2015 Peter <petervo@redhat.com> - 0.47-1
- Update to 0.47 release, build docker on armvrhl

* Thu Mar 26 2015 Stef Walter <stefw@redhat.com> - 0.46-1
- Update to 0.46 release

* Mon Mar 23 2015 Stef Walter <stefw@redhat.com> - 0.45-1
- Update to 0.45 release

* Sat Mar 21 2015 Stef Walter <stefw@redhat.com> - 0.44-3
- Add back debuginfo files to the right place

* Fri Mar 20 2015 Stef Walter <stefw@redhat.com> - 0.44-2
- Disable separate debuginfo for now: build failure

* Fri Mar 20 2015 Stef Walter <stefw@redhat.com> - 0.44-1
- Update to 0.44 release

* Thu Mar 19 2015 Stef Walter <stefw@redhat.com> - 0.43-2
- Don't break EPEL or CentOS builds due to missing branding

* Wed Mar 18 2015 Stef Walter <stefw@redhat.com> - 0.43-1
- Update to 0.43 release

* Tue Mar 17 2015 Stef Walter <stefw@redhat.com> - 0.42-2
- Fix obseleting cockpit-assets

* Sat Mar 14 2015 Stef Walter <stefw@redhat.com> - 0.42-1
- Update to 0.42 release

* Wed Mar 04 2015 Stef Walter <stefw@redhat.com> - 0.41-1
- Update to 0.41 release

* Thu Feb 26 2015 Stef Walter <stefw@redhat.com> - 0.40-1
- Update to 0.40 release

* Thu Feb 19 2015 Stef Walter <stefw@redhat.com> - 0.39-1
- Update to 0.39 release

* Wed Jan 28 2015 Stef Walter <stefw@redhat.com> - 0.38-1
- Update to 0.38 release

* Thu Jan 22 2015 Stef Walter <stefw@redhat.com> - 0.37-1
- Update to 0.37 release

* Mon Jan 12 2015 Stef Walter <stefw@redhat.com> - 0.36-1
- Update to 0.36 release

* Mon Dec 15 2014 Stef Walter <stefw@redhat.com> - 0.35-1
- Update to 0.35 release

* Thu Dec 11 2014 Stef Walter <stefw@redhat.com> - 0.34-1
- Update to 0.34 release

* Fri Dec 05 2014 Stef Walter <stefw@redhat.com> - 0.33-3
- Only depend on docker stuff on x86_64

* Fri Dec 05 2014 Stef Walter <stefw@redhat.com> - 0.33-2
- Only build docker stuff on x86_64

* Wed Dec 03 2014 Stef Walter <stefw@redhat.com> - 0.33-1
- Update to 0.33 release

* Mon Nov 24 2014 Stef Walter <stefw@redhat.com> - 0.32-1
- Update to 0.32 release

* Fri Nov 14 2014 Stef Walter <stefw@redhat.com> - 0.31-1
- Update to 0.31 release

* Wed Nov 12 2014 Stef Walter <stefw@redhat.com> - 0.30-1
- Update to 0.30 release
- Split Cockpit into various sub packages

* Wed Nov 05 2014 Stef Walter <stefw@redhat.com> - 0.29-3
- Don't require test-assets from selinux-policy
- Other minor tweaks and fixes

* Wed Nov 05 2014 Stef Walter <stefw@redhat.com> - 0.29-2
- Include selinux policy as a dep where required

* Wed Nov 05 2014 Stef Walter <stefw@redhat.com> - 0.29-1
- Update to 0.29 release

* Thu Oct 16 2014 Stef Walter <stefw@redhat.com> - 0.28-1
- Update to 0.28 release
- cockpit-agent was renamed to cockpit-bridge

* Fri Oct 10 2014 Stef Walter <stefw@redhat.com> - 0.27-1
- Update to 0.27 release
- Don't create cockpit-*-admin groups rhbz#1145135
- Fix user management for non-root users rhbz#1140562
- Fix 'out of memory' error during ssh auth rhbz#1142282

* Wed Oct 08 2014 Stef Walter <stefw@redhat.com> - 0.26-1
- Update to 0.26 release
- Can see disk usage on storage page rhbz#1142459
- Better order for lists of block devices rhbz#1142443
- Setting container memory limit fixed rhbz#1142362
- Can create storage volume of maximum capacity rhbz#1142259
- Fix RAID device Bitmap enable/disable error rhbz#1142248
- Docker page connects to right machine rhbz#1142229
- Clear the format dialog label correctly rhbz#1142228
- No 'Drop Privileges' item in menu for root rhbz#1142197
- Don't flash 'Server has closed Connection on logout rhbz#1142175
- Non-root users can manipulate user accounts rhbz#1142154
- Fix strange error message when editing user accounts rhbz#1142154

* Wed Sep 24 2014 Stef Walter <stefw@redhat.com> - 0.25-1
- Update to 0.25 release

* Wed Sep 17 2014 Stef Walter <stefw@redhat.com> - 0.24-1
- Update to 0.24 release

* Wed Sep 10 2014 Stef Walter <stefw@redhat.com> - 0.23-1
- Update to 0.23 release

* Wed Sep 03 2014 Stef Walter <stefw@redhat.com> - 0.22-1
- Update to 0.22 release

* Tue Aug 26 2014 Patrick Uiterwijk <puiterwijk@redhat.com> - 0.21-1
- Update to 0.21 release

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Stef Walter <stefw@redhat.com> 0.20-1
- Update to 0.20 release

* Thu Aug 07 2014 Stef Walter <stefw@redhat.com> 0.19-1
- Update to 0.19 release

* Wed Jul 30 2014 Stef Walter <stefw@redhat.com> 0.18-1
- Update to 0.18 release
- Add glib-networking build requirement
- Let selinux-policy-targetted distribute selinux policy

* Mon Jul 28 2014 Colin Walters <walters@verbum.org> 0.17-2
- Drop Requires and references to dead test-assets subpackage

* Thu Jul 24 2014 Stef Walter <stefw@redhat.com> 0.17-1
- Update to 0.17 release

* Wed Jul 23 2014 Stef Walter <stefw@redhat.com> 0.16-3
- Distribute our own selinux policy rhbz#1110758

* Tue Jul 22 2014 Stef Walter <stefw@redhat.com> 0.16-2
- Refer to cockpit.socket in scriptlets rhbz#1110764

* Thu Jul 17 2014 Stef Walter <stefw@redhat.com> 0.16-1
- Update to 0.16 release

* Thu Jul 10 2014 Stef Walter <stefw@redhat.com> 0.15-1
- Update to 0.15 release
- Put pam_reauthorize.so in the cockpit PAM stack

* Thu Jul 03 2014 Stef Walter <stefw@redhat.com> 0.14-1
- Update to 0.14 release

* Mon Jun 30 2014 Stef Walter <stefw@redhat.com> 0.13-1
- Update to 0.13 release

* Tue Jun 24 2014 Stef Walter <stefw@redhat.com> 0.12-1
- Update to upstream 0.12 release

* Fri Jun 20 2014 Stef Walter <stefw@redhat.com> 0.11-1
- Update to upstream 0.11 release

* Thu Jun 12 2014 Stef Walter <stefw@redhat.com> 0.10-1
- Update to upstream 0.10 release

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Stef Walter <stefw@redhat.com> 0.9-1
- Update to upstream 0.9 release
- Fix file attribute for cockpit-polkit

* Wed May 21 2014 Stef Walter <stefw@redhat.com> 0.8-1
- Update to upstream 0.8 release
- cockpitd now runs as a user session DBus service

* Mon May 19 2014 Stef Walter <stefw@redhat.com> 0.7-1
- Update to upstream 0.7 release

* Wed May 14 2014 Stef Walter <stefw@redhat.com> 0.6-1
- Update to upstream 0.6 release

* Tue Apr 15 2014 Stef Walter <stefw@redhat.com> 0.5-1
- Update to upstream 0.5 release

* Thu Apr 03 2014 Stef Walter <stefw@redhat.com> 0.4-1
- Update to upstream 0.4 release
- Lots of packaging cleanup and polish

* Fri Mar 28 2014 Stef Walter <stefw@redhat.com> 0.3-1
- Update to upstream 0.3 release

* Wed Feb 05 2014 Patrick Uiterwijk (LOCAL) <puiterwijk@redhat.com> - 0.2-0.4.20140204git5e1faad
- Redid the release tag

* Tue Feb 04 2014 Patrick Uiterwijk (LOCAL) <puiterwijk@redhat.com> - 0.2-0.3.5e1faadgit
- Fixed license tag
- Updated to new FSF address upstream
- Removing libgsystem before build
- Now claiming specific manpages
- Made the config files noreplace
- Removed the test assets
- Put the web assets in a subpackage

* Tue Feb 04 2014 Patrick Uiterwijk (LOCAL) <puiterwijk@redhat.com> - 0.2-0.2.5e1faadgit
- Patch libgsystem out
