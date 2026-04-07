## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           kea
Version:        3.0.2
Release:        %autorelease
Summary:        DHCPv4, DHCPv6 and DDNS server from ISC
License:        MPL-2.0 AND BSL-1.0
URL:            http://kea.isc.org

# Support for netconf is not enabled
%bcond_with sysrepo
%bcond_with tests

%global keama_version 4.5.0
# Bundled version of Bind libraries linked into Keama
%global bind_version 9.11.36

# Conflict with kea-next
%global upstream_name kea
%define upstream_name_compat() \
%if "%{name}" != "%{upstream_name}" \
Provides: %1 = %{version}-%{release} \
Conflicts: %1 \
%endif

Source0:        https://downloads.isc.org/isc/kea/%{version}/kea-%{version}.tar.xz
Source1:        https://downloads.isc.org/isc/kea/%{version}/kea-%{version}.tar.xz.asc
Source2:        https://downloads.isc.org/isc/keama/%{keama_version}/keama-%{keama_version}.tar.gz
Source3:        https://downloads.isc.org/isc/keama/%{keama_version}/keama-%{keama_version}.tar.gz.asc
Source10:       https://www.isc.org/docs/isc-keyblock.asc
Source11:       kea-dhcp4.service
Source12:       kea-dhcp6.service
Source13:       kea-dhcp-ddns.service
Source14:       kea-ctrl-agent.service
Source15:       systemd-tmpfiles.conf
Source16:       systemd-sysusers.conf

Patch1:         kea-sd-daemon.patch

BuildRequires: boost-devel
# %%meson -D crypto=openssl
BuildRequires: openssl-devel
%if 0%{?fedora}
# https://bugzilla.redhat.com/show_bug.cgi?id=2300868#c4
BuildRequires: openssl-devel-engine
%endif
# %%meson -D krb5=enabled
BuildRequires: krb5-devel
# %%meson -D mysql=enabled
BuildRequires: mariadb-connector-c-devel
# %%meson -D postgresql=enabled
%if 0%{?fedora} || 0%{?rhel} > 9
BuildRequires: libpq-devel
%else
BuildRequires: postgresql-server-devel
%endif
# %%meson -D systemd=enabled
BuildRequires: systemd-devel
%if %{with sysrepo}
# %%meson -D netconf=enabled
BuildRequires: sysrepo-devel
%endif
%if %{with tests}
# %%meson -D tests=enabled
%ifarch %{valgrind_arches}
BuildRequires: valgrind-devel
%endif
BuildRequires: gtest-devel
BuildRequires: procps-ng
%endif
BuildRequires: log4cplus-devel
BuildRequires: python3-devel

BuildRequires: gcc-c++
BuildRequires: autoconf automake libtool
BuildRequires: make
BuildRequires: meson
BuildRequires: bison
BuildRequires: flex
BuildRequires: systemd
BuildRequires: systemd-rpm-macros
BuildRequires: python3-sphinx
BuildRequires: python3-sphinx_rtd_theme
BuildRequires: gnupg2

Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%upstream_name_compat %{upstream_name}
Requires: coreutils util-linux
%{?systemd_requires}

%description
DHCP implementation from Internet Systems Consortium, Inc. that features fully
functional DHCPv4, DHCPv6 and Dynamic DNS servers.
Both DHCP servers fully support server discovery, address assignment, renewal,
rebinding and release. The DHCPv6 server supports prefix delegation. Both
servers support DNS Update mechanism, using stand-alone DDNS daemon.

%package doc
Summary: Documentation for Kea DHCP server
BuildArch: noarch

%description doc
Documentation and example configuration for Kea DHCP server.

%package devel
Summary: Development headers and libraries for Kea DHCP server
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
# to build hooks (#1335900)
Requires: boost-devel
Requires: openssl-devel
Requires: pkgconfig

%description devel
Header files and API documentation.

%package hooks
Summary: Hooks libraries for kea
Requires: %{name}-libs%{?_isa} = %{version}-%{release}

%description hooks
Hooking mechanism allow Kea to load one or more dynamically-linked libraries
(known as "hooks libraries") and, at various points in its processing
("hook points"), call functions in them.  Those functions perform whatever
custom processing is required.

%package libs
Summary: Shared libraries used by Kea DHCP server
%upstream_name_compat %{upstream_name}-libs

%description libs
This package contains shared libraries used by Kea DHCP server.

%package keama
Summary: Experimental migration assistant for Kea
Provides: bundled(bind-libs) = %{bind_version}

%description keama
The KEA Migration Assistant is an experimental tool which helps to translate
ISC DHCP configurations to Kea.

%prep
%if 0%{?fedora} || 0%{?rhel} > 8
%{gpgverify} --keyring='%{S:10}' --signature='%{S:1}' --data='%{S:0}'
%{gpgverify} --keyring='%{S:10}' --signature='%{S:3}' --data='%{S:2}'
%endif

%autosetup -T -b2 -N -n keama-%{keama_version}
%autosetup -p1 -n kea-%{version}

%build
# This removes RPATH from binaries
export KEA_PKG_TYPE_IN_CONFIGURE="rpm"

%meson \
    --install-umask 0022 \
%if %{with sysrepo}
    -D netconf=enabled \
%else
    -D netconf=disabled \
%endif
%if %{with tests}
    -D tests=enabled \
%else
    -D tests=disabled \
%endif
    -D crypto=openssl \
    -D krb5=enabled \
    -D mysql=enabled \
    -D postgresql=enabled \
    -D systemd=enabled

%meson_build
%meson_build doc

# Configure & build Keama
pushd ../keama-%{keama_version}

# We need to unpack the embedded copy of bind and call autoreconf to
# ensure that config.{sub,guess} is up to date, since the copies
# included in the archive are extremely old (2013) and unaware of
# more recent architectures such as riscv64. The Keama build system
# would normally take care of unpacking the archive, but it also
# handles gracefully us doing it ourselves
tar -C bind/ -zxvf bind/bind.tar.gz

pushd bind/bind-%{bind_version}/

autoreconf --verbose --force --install

# Back to Keama. Its build system will take care of configuring and
# building the embedded copy of bind
popd

autoreconf --verbose --force --install

%configure \
    --disable-dependency-tracking \
    --disable-silent-rules

%make_build
popd

%if %{with tests}
%check
%meson_test
%endif

%install
%meson_install

# Install Keama
pushd ../keama-%{keama_version}
%make_install
popd

# Remove Keama's static library, dhcp headers and man pages
rm %{buildroot}/%{_libdir}/libdhcp.a
rm -rf %{buildroot}/%{_includedir}/omapip/
rm -rf %{buildroot}%{_mandir}/man5/

# Remove keactrl
rm %{buildroot}%{_sysconfdir}/kea/keactrl.conf
rm %{buildroot}%{_sbindir}/keactrl 
rm %{buildroot}%{_mandir}/man8/keactrl.8*

%if %{without sysrepo}
# Remove netconf files
rm %{buildroot}%{_mandir}/man8/kea-netconf.8
%endif

rm %{buildroot}%{_pkgdocdir}/COPYING

rm -rf %{buildroot}/usr/share/kea/meson-info/

# Create empty password file for the Kea Control Agent
install -m 0640 /dev/null %{buildroot}%{_sysconfdir}/kea/kea-api-password

# Install systemd units
install -Dpm 0644 %{S:11} %{buildroot}%{_unitdir}/kea-dhcp4.service
install -Dpm 0644 %{S:12} %{buildroot}%{_unitdir}/kea-dhcp6.service
install -Dpm 0644 %{S:13} %{buildroot}%{_unitdir}/kea-dhcp-ddns.service
install -Dpm 0644 %{S:14} %{buildroot}%{_unitdir}/kea-ctrl-agent.service

# Start empty lease databases
mkdir -p %{buildroot}%{_sharedstatedir}/kea/
touch %{buildroot}%{_sharedstatedir}/kea/kea-leases4.csv
touch %{buildroot}%{_sharedstatedir}/kea/kea-leases6.csv

# Install systemd sysusers and tmpfiles configs
install -Dpm 0644 %{S:16} %{buildroot}%{_sysusersdir}/kea.conf
install -Dpm 0644 %{S:15} %{buildroot}%{_tmpfilesdir}/kea.conf

mkdir -p %{buildroot}%{_rundir}
install -dm 0750 %{buildroot}%{_rundir}/kea/

mkdir -p %{buildroot}%{_localstatedir}/log
install -dm 0750 %{buildroot}%{_localstatedir}/log/kea/

%post
# Kea runs under kea user instead of root now, but if its files got altered, their new
# ownership&permissions won't get changed so fix them to prevent startup failures
[ "`stat --format '%U:%G' %{_rundir}/kea/logger_lockfile 2>&1 | grep root:root`" = "root:root" ] \
    && chown kea:kea %{_rundir}/kea/logger_lockfile
[ "`stat --format '%U:%G' %{_sharedstatedir}/kea/kea-leases4.csv* 2>&1 | grep root:root | head -1`" = "root:root" ] \
    && chown kea:kea %{_sharedstatedir}/kea/kea-leases4.csv* && chmod 0640 %{_sharedstatedir}/kea/kea-leases4.csv*
[ "`stat --format '%U:%G' %{_sharedstatedir}/kea/kea-leases6.csv* 2>&1 | grep root:root | head -1`" = "root:root" ] \
    && chown kea:kea %{_sharedstatedir}/kea/kea-leases6.csv* && chmod 0640 %{_sharedstatedir}/kea/kea-leases6.csv*
[ "`stat --format '%U:%G' %{_sharedstatedir}/kea/kea-dhcp6-serverid 2>&1 | grep root:root`" = "root:root" ] \
    && chown kea:kea %{_sharedstatedir}/kea/kea-dhcp6-serverid
[ "`stat --format '%U:%G' %{_sysconfdir}/kea/kea*.conf 2>&1 | grep root:root | head -1`" = "root:root" ] \
    && chown root:kea %{_sysconfdir}/kea/kea*.conf && chmod 0640 %{_sysconfdir}/kea/kea*.conf

# Remove /tmp/ from socket-name for existing configurations to fix CVE-2025-32802
for i in kea-ctrl-agent.conf kea-dhcp4.conf kea-dhcp6.conf kea-dhcp-ddns.conf; do
    if [ -n "`grep '\"socket-name\": \"/tmp/' %{_sysconfdir}/kea/$i`" ]; then
        sed -i.CVE-2025-32802.bak 's#\("socket-name": "/tmp/\)\(.*\)#"socket-name": "\2#g' %{_sysconfdir}/kea/$i
    fi
done
# Set a pseudo-random password for default config to secure fresh install and allow CA startup without user intervention
if [[ ! -s %{_sysconfdir}/kea/kea-api-password && -n `grep '"password-file": "kea-api-password"' %{_sysconfdir}/kea/kea-ctrl-agent.conf` ]]; then
    (umask 0027; head -c 32 /dev/urandom | base64 > %{_sysconfdir}/kea/kea-api-password)
    chown root:kea %{_sysconfdir}/kea/kea-api-password
fi
%systemd_post kea-dhcp4.service kea-dhcp6.service kea-dhcp-ddns.service kea-ctrl-agent.service

%preun
%systemd_preun kea-dhcp4.service kea-dhcp6.service kea-dhcp-ddns.service kea-ctrl-agent.service

%postun
%systemd_postun_with_restart kea-dhcp4.service kea-dhcp6.service kea-dhcp-ddns.service kea-ctrl-agent.service
%ldconfig_scriptlets libs

%files
%license COPYING
%{_sbindir}/kea-admin
%{_sbindir}/kea-ctrl-agent
%{_sbindir}/kea-dhcp-ddns
%{_sbindir}/kea-dhcp4
%{_sbindir}/kea-dhcp6
%{_sbindir}/kea-lfc
%{_sbindir}/kea-shell
%{_sbindir}/perfdhcp
%{_unitdir}/kea*.service
%{_datarootdir}/kea
%dir %attr(0750,root,kea) %{_sysconfdir}/kea/
%config(noreplace) %attr(0640,root,kea) %{_sysconfdir}/kea/kea*.conf
%ghost %config(noreplace,missingok) %attr(0640,root,kea) %verify(not md5 size mtime) %{_sysconfdir}/kea/kea-api-password
%dir %attr(0750,kea,kea) %{_sharedstatedir}/kea
%config(noreplace) %attr(0640,kea,kea) %{_sharedstatedir}/kea/kea-leases*.csv
%dir %attr(0750,kea,kea) %{_rundir}/kea/
%dir %attr(0750,kea,kea) %{_localstatedir}/log/kea
%{python3_sitelib}/kea
%{_mandir}/man8/kea-admin.8*
%{_mandir}/man8/kea-ctrl-agent.8*
%{_mandir}/man8/kea-dhcp-ddns.8*
%{_mandir}/man8/kea-dhcp4.8*
%{_mandir}/man8/kea-dhcp6.8*
%{_mandir}/man8/kea-lfc.8*
%if %{with sysrepo}
%{_mandir}/man8/kea-netconf.8*
%endif
%{_mandir}/man8/kea-shell.8*
%{_mandir}/man8/perfdhcp.8*
%{_tmpfilesdir}/kea.conf
%{_sysusersdir}/kea.conf

%files doc
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/AUTHORS
%doc %{_pkgdocdir}/ChangeLog
%doc %{_pkgdocdir}/code_of_conduct.md
%doc %{_pkgdocdir}/CONTRIBUTING.md
%doc %{_pkgdocdir}/examples
%doc %{_pkgdocdir}/html
%doc %{_pkgdocdir}/platforms.rst
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/SECURITY.md

%files devel
%{_bindir}/kea-msg-compiler
%{_includedir}/kea
%{_libdir}/libkea-asiodns.so
%{_libdir}/libkea-asiolink.so
%{_libdir}/libkea-cc.so
%{_libdir}/libkea-cfgrpt.so
%{_libdir}/libkea-config.so
%{_libdir}/libkea-cryptolink.so
%{_libdir}/libkea-d2srv.so
%{_libdir}/libkea-database.so
%{_libdir}/libkea-dhcp_ddns.so
%{_libdir}/libkea-dhcp.so
%{_libdir}/libkea-dhcpsrv.so
%{_libdir}/libkea-dns.so
%{_libdir}/libkea-eval.so
%{_libdir}/libkea-exceptions.so
%{_libdir}/libkea-hooks.so
%{_libdir}/libkea-http.so
%{_libdir}/libkea-log-interprocess.so
%{_libdir}/libkea-log.so
%{_libdir}/libkea-mysql.so
%{_libdir}/libkea-pgsql.so
%{_libdir}/libkea-process.so
%{_libdir}/libkea-stats.so
%{_libdir}/libkea-tcp.so
%{_libdir}/libkea-util-io.so
%{_libdir}/libkea-util.so
%{_libdir}/pkgconfig/kea.pc

%files hooks
%dir %{_sysconfdir}/kea/radius
%{_sysconfdir}/kea/radius/dictionary
%dir %{_libdir}/kea
%dir %{_libdir}/kea/hooks
%{_libdir}/kea/hooks/libddns_gss_tsig.so
%{_libdir}/kea/hooks/libdhcp_bootp.so
%{_libdir}/kea/hooks/libdhcp_class_cmds.so
%{_libdir}/kea/hooks/libdhcp_ddns_tuning.so
%{_libdir}/kea/hooks/libdhcp_flex_id.so
%{_libdir}/kea/hooks/libdhcp_flex_option.so
%{_libdir}/kea/hooks/libdhcp_ha.so
%{_libdir}/kea/hooks/libdhcp_host_cache.so
%{_libdir}/kea/hooks/libdhcp_host_cmds.so
%{_libdir}/kea/hooks/libdhcp_lease_cmds.so
%{_libdir}/kea/hooks/libdhcp_lease_query.so
%{_libdir}/kea/hooks/libdhcp_legal_log.so
%{_libdir}/kea/hooks/libdhcp_limits.so
%{_libdir}/kea/hooks/libdhcp_mysql.so
%{_libdir}/kea/hooks/libdhcp_perfmon.so
%{_libdir}/kea/hooks/libdhcp_pgsql.so
%{_libdir}/kea/hooks/libdhcp_ping_check.so
%{_libdir}/kea/hooks/libdhcp_radius.so
%{_libdir}/kea/hooks/libdhcp_run_script.so
%{_libdir}/kea/hooks/libdhcp_stat_cmds.so
%{_libdir}/kea/hooks/libdhcp_subnet_cmds.so

%files libs
%license COPYING
# older: find `rpm --eval %%{_topdir}`/BUILDROOT/kea-*/usr/lib64/ -type f | grep /usr/lib64/libkea | sed -e 's#.*/usr/lib64\(.*\.so\.[0-9]\+\)\.[0-9]\+\.[0-9]\+#%%{_libdir}\1*#' | sort
# >=f41: find `rpm --eval %%{_topdir}`/BUILD/kea-*/BUILDROOT/usr/lib64/ -type f | grep /usr/lib64/libkea | sed -e 's#.*/usr/lib64\(.*\.so\.[0-9]\+\)\.[0-9]\+\.[0-9]\+#%%{_libdir}\1*#' | sort
%{_libdir}/libkea-asiodns.so.62*
%{_libdir}/libkea-asiolink.so.88*
%{_libdir}/libkea-cc.so.82*
%{_libdir}/libkea-cfgrpt.so.3*
%{_libdir}/libkea-config.so.83*
%{_libdir}/libkea-cryptolink.so.64*
%{_libdir}/libkea-d2srv.so.63*
%{_libdir}/libkea-database.so.76*
%{_libdir}/libkea-dhcp_ddns.so.68*
%{_libdir}/libkea-dhcp.so.109*
%{_libdir}/libkea-dhcpsrv.so.131*
%{_libdir}/libkea-dns.so.71*
%{_libdir}/libkea-eval.so.84*
%{_libdir}/libkea-exceptions.so.45*
%{_libdir}/libkea-hooks.so.120*
%{_libdir}/libkea-http.so.87*
%{_libdir}/libkea-log-interprocess.so.3*
%{_libdir}/libkea-log.so.75*
%{_libdir}/libkea-mysql.so.88*
%{_libdir}/libkea-pgsql.so.88*
%{_libdir}/libkea-process.so.90*
%{_libdir}/libkea-stats.so.53*
%{_libdir}/libkea-tcp.so.33*
%{_libdir}/libkea-util-io.so.12*
%{_libdir}/libkea-util.so.101*

%files keama
%license COPYING
%{_bindir}/keama
%{_mandir}/man8/keama.8*

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 3.0.2-2
- Latest state for kea

* Wed Oct 29 2025 Martin Osvald <mosvald@redhat.com> - 3.0.2-1
- New version 3.0.2 (rhbz#2407048)
- Fixes CVE-2025-11232

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0.1-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 29 2025 Martin Osvald <mosvald@redhat.com> - 3.0.1-1
- New version 3.0.1 (rhbz#2391289)
- Fixes CVE-2025-40779 (rhbz#2391373)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 31 2025 Martin Osvald <mosvald@redhat.com> - 3.0.0-4
- Move radius config into hooks sub-package

* Wed Jul 30 2025 Martin Osvald <mosvald@redhat.com> - 3.0.0-3
- Support for sending startup notifications to systemd (rhbz#2384776)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Martin Osvald <mosvald@redhat.com> - 3.0.0-1
- New version 3.0.0 (rhbz#2374737)
- Remove broken keactrl in favor of systemd unit files
- kea.spec: General cleanup and removal of lines that have no effect
- kea-msg-compiler was moved from kea to kea-devel

* Mon Jun 09 2025 Python Maint <python-maint@redhat.com> - 2.6.3-2
- Rebuilt for Python 3.14

* Sun Jun 08 2025 Martin Osvald <mosvald@redhat.com> - 2.6.3-1
- New version 2.6.3 (rhbz#2368989)
- Fix for: CVE-2025-32801, CVE-2025-32802, CVE-2025-32803
- kea.conf: Remove /tmp/ from socket-name for existing configurations
- kea.conf: Set pseudo-random password for default config to secure fresh
  install and allow CA startup without user intervention
- kea.conf: Restrict directory permissions
- Sync service files with upstream
- Fix leases ownership when switching from root to kea user (rhbz#2324168)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.6.2-6
- Rebuilt for Python 3.14

* Mon Jun 02 2025 František Hrdina <fhrdina@redhat.com> - 2.6.2-5
- Update of fmf plans and gating to be rhel-11 ready

* Thu May 29 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 2.6.2-4
- Reconditionalize openssl-devel-engine

* Wed May 21 2025 Martin Osvald <mosvald@redhat.com> - 2.6.2-3
- kea.spec: remove rhel7 and f40 conditions

* Wed Apr 16 2025 Pavol Sloboda <pavol.sloboda02@gmail.com> - 2.6.2-2
- fix: fixed the BuildRequires of mariadb-devel package the mariadb-
  connector-c-devel package is available for all RHEL versions from version
  8 and above, as version 7 is quite old this condition is not necessary
  and all packages should use the BuildRequires of mariadb-connector-c-
  devel instead of mariadb-devel if possible

* Wed Mar 26 2025 Martin Osvald <mosvald@redhat.com> - 2.6.2-1
- New version 2.6.2 (rhbz#2355027)

* Fri Feb 28 2025 František Hrdina <fhrdina@redhat.com> - 2.6.1-9
- fmf plans & gating rhel-11 ready

* Wed Feb 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.6.1-8
- Drop call to %%sysusers_create_compat

* Wed Feb 12 2025 pdancak <pdancak@redhat.com> - 2.6.1-7
- User kea can't create log files (#2329450)

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Nov 21 2024 Andrea Bolognani <abologna@redhat.com> - 2.6.1-5
- Use autoreconf more (fixes riscv64 build)

* Wed Aug 21 2024 Martin Osvald <mosvald@redhat.com> - 2.6.1-4
- Fix startup failures during upgrade due to wrong permissions and
  ownership

* Wed Aug 07 2024 Martin Osvald <mosvald@redhat.com> - 2.6.1-3
- Fix /run/kea ownership

* Mon Aug 05 2024 Martin Osvald <mosvald@redhat.com> - 2.6.1-2
- Do not run as root and restrict file access (rhbz#2302204)

* Thu Aug 01 2024 Martin Osvald <mosvald@redhat.com> - 2.6.1-1
- New version 2.6.1 (rhbz#2301927)

* Tue Jul 30 2024 Martin Osvald <mosvald@redhat.com> - 2.6.0-7
- Fix FTBFS on f41 caused by openssl engine headers moving from -devel to
  -devel-engine (rhbz#2300868)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 25 2024 Martin Osvald <mosvald@redhat.com> - 2.6.0-5
- Keactrl is using rev without dependency on util-linux

* Wed Jun 19 2024 Martin Osvald <mosvald@redhat.com> - 2.6.0-4
- kea.spec: minor fixes

* Tue Jun 18 2024 Martin Osvald <mosvald@redhat.com> - 2.6.0-3
- Require libpq-devel instead of postgresql-server-devel (rhbz#2120322)

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2.6.0-2
- Rebuilt for Python 3.13

* Thu May 30 2024 Martin Osvald <mosvald@redhat.com> - 2.6.0-1
- New version 2.6.0 (rhbz#2283671)

* Tue Mar 26 2024 Martin Osvald <mosvald@redhat.com> - 2.4.1-9
- Allow building with unit tests for future upstream contributions

* Sun Mar 24 2024 psklenar@redhat.com <psklenar@redhat.com> - 2.4.1-8
- setup fedora CI

* Sat Feb 24 2024 David Abdurachmanov <davidlt@rivosinc.com> - 2.4.1-7
- Properly check valgrind arches

* Tue Feb 20 2024 Martin Osvald <mosvald@redhat.com> - 2.4.1-6
- Add keama migration utility (rhbz#2250608)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Jonathan Wakely <jwakely@redhat.com> - 2.4.1-3
- Rebuilt for Boost 1.83

* Thu Dec 07 2023 Martin Osvald <mosvald@redhat.com> - 2.4.1-2
- kea.spec: Fix missing _pkgdocdir ownership and other small fixes

* Thu Nov 30 2023 Martin Osvald <mosvald@redhat.com> - 2.4.1-1
- New version 2.4.1 (rhbz#2251930)

* Thu Nov 30 2023 Lukas Javorsky <ljavorsk@redhat.com> - 2.4.0-7
- Rebuild for PostgreSQL 16 (BZ#2251109)

* Tue Aug 22 2023 Martin Osvald <mosvald@redhat.com> - 2.4.0-6
- Various spec file improvements
- Remove _hardened_build variable as it is no longer needed
- Clean up numbering of sources
- Further %%{name} changes to allow different package name
- Move documentation into sub-package
- Move tpmfiles.d configuration into separate file
- Start using %%autorelease and %%autochangelog
- Remove %%license COPYING for devel due to lib dependency

* Thu Aug 10 2023 Martin Osvald <mosvald@redhat.com> - 2.4.0-4
- Rebuilt for log4cplus 2.1.0
- kea.spec: do not use %%{name} to allow different package name
- kea.spec: do not use glob on %%{_libdir}, %%{_mandir} and %%{_sbindir}
  to conform with packaging guidelines

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Martin Osvald <mosvald@redhat.com> - 2.4.0-1
- New version 2.4.0
- Migrated to SPDX license
- Do not export CXXFLAGS with -std=gnu++11 to stop boost warning messages

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 2.2.0-5
- Rebuilt for Python 3.12

* Mon Feb 20 2023 Jonathan Wakely <jwakely@redhat.com> - 2.2.0-4
- Rebuilt for Boost 1.81

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 16 2022 Ondřej Sloup <osloup@redhat.com> - 2.2.0-2
- Rebuild for new PostgreSQL 15

* Wed Jul 27 2022 Martin Osvald <mosvald@redhat.com> - 2.2.0-1
- New version 2.2.0
- Add source code signature verification

* Thu Jul 21 2022 Martin Osvald <mosvald@redhat.com> - 2.0.2-4
- kea fails to build docs with Sphinx 5+ (#2105931)

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.2-3
- Rebuilt for Python 3.11

* Wed May 04 2022 Thomas Rodgers <trodgers@redhat.com> - 2.0.2-2
- Rebuilt for Boost 1.78

* Thu Mar 03 2022 Martin Osvald <mosvald@redhat.com> - 2.0.2-1
- New version 2.0.2

* Mon Feb 07 2022 Martin Osvald <mosvald@redhat.com> - 2.0.1-1
- New version 2.0.1

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Filip Januš <fjanus@redhat.com> - 1.9.8-6
- Rebuild for Postgresql 14

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1.9.8-5
- Rebuilt with OpenSSL 3.0.0

* Fri Aug 06 2021 Jonathan Wakely <jwakely@redhat.com> - 1.9.8-4
- Rebuilt for Boost 1.76

* Tue Jul 27 2021 Filip Januš <fjanus@redhat.com> - 1.9.8-3
- Remove libpq-devel requirement, it conflicts with postgresql-server-devel
  dependencies

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 23 2021 Pavel Zhukov <pzhukov@redhat.com> - 1.9.8-1
- New version 1.9.8

* Wed Jun 23 2021 Pavel Zhukov <pzhukov@redhat.com> - 1.9.6-2
- Make compatible with spinx 4.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.9.6-2
- Rebuilt for Python 3.10

* Sun Apr 04 2021 Pavel Zhukov <pzhukov@redhat.com> - 1.9.6-1
- New version v1.9.6

* Thu Mar 11 2021 Pavel Zhukov <pzhukov@redhat.com> - 1.9.5-1
- New version v1.9.5

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.9.4-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Feb 09 2021 Pavel Raiskup <praiskup@redhat.com> - 1.9.4-2
- rebuild all postgresql deps once more, for libpq ABI fix rhbz#1908268

* Mon Feb 08 2021 Pavel Zhukov pzhukov@redhat.com> - 1.9.4-1
- Update to 1.9.4

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 1.9.3-5
- rebuild for libpq ABI fix rhbz#1908268

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Pavel Zhukov pzhukov@redhat.com> - 1.9.3-3
- Update to 1.9.3
- Fix Werror bug

* Fri Jan 22 2021 Jonathan Wakely <jwakely@redhat.com> - 1.9.2-3
- Rebuilt for Boost 1.75

* Sat Dec 05 2020 Jeff Law <law@redhat.com> - 1.9.2-2
- Fix more missing includes for gcc-11

* Thu Nov 26 2020 Pavel Zhukov <pzhukov@redhat.com> - 1.9.2-1
- new version v1.9.2

* Fri Nov 20 2020 Pavel Zhukov <pzhukov@redhat.com> - 1.9.1-3
- Rebuild with new log4cplus

* Thu Oct 15 2020 Jeff Law <law@redhat.com> - 1.8.0-2
- Fix missing #includes for gcc-11

* Wed Sep 16 2020 Pavel Zhukov <pzhukov@redhat.com> - 1.8.0-1
- New version v1.8.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 29 2020 Jonathan Wakely <jwakely@redhat.com> - 1.6.0-4
- Rebuilt for Boost 1.73

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-3
- Rebuilt for Python 3.9

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep 11 2019 Kenneth Topp <toppk@bllue.org> - 1.6.0-1
- update to 1.6.0
- includes fixes for CVE-2019-6472, CVE-2019-6473 and CVE-2019-6474

* Tue Jul 30 2019 Pavel Zhukov <pzhukov@redhat.com> - 1.5.0-8
- Do not specify openssl version

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Felix Kaechele <heffer@fedoraproject.org> - 1.5.0-4
- Update to 1.3.0 release version
- fix PID file path in service files
- clean up spec file
- switched to openssl-devel, now builds with openssl 1.1
- install systemd units manually instead of patching the souce to do it
- enable kea-shell
- add boost patch
- add kea-ctrl-agent unit
- change postgresql-devel to postgresql-server-devel
- update to 1.4.0

* Sun Dec 16 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.5.0-3
- Update to released version

* Tue Dec 11 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.5.0-beta2.2%{?dist}
- Do not require -connectors on RHEL

* Tue Dec  4 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.5.0-beta2.1%{?dist}
- update to beta2

* Tue Nov 20 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.5.0-2
- Update to 1.5.0 beta

* Mon Aug 27 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.3.0-12
- Disable tests again.

* Mon Aug 27 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.3.0-11
- Do not use compat verion of openssl

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 17 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.3.0-9
- Fix config files names (#1579298)

* Mon Feb 19 2018 Pavel Zhukov <pzhukov@redhat.com> - 1.3.0-8
- Add gcc-c++ BR

* Wed Feb 14 2018 Pavel Zhukov <landgraf@fedoraproject.org> - 1.3.0-7
- Package released version (#1545096)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Pavel Zhukov <landgraf@fedoraproject.org> - 1.3.0-4
- Fix build with boost 1.66 (#1540331)

* Thu Nov  2 2017 Pavel Zhukov <pzhukov@redhat.com> - 1.3.0-3
- Add openssl-devel requires
- Do not force pkgconfig(openssl) version

* Mon Oct 23 2017 Pavel Zhukov <pzhukov@redhat.com> - 1.2.0-8
- Require openssl102

* Sun Oct 22 2017 Pavel Zhukov <pzhukov@redhat.com> - 1.2.0-7
- Rebuild with new openssl

* Thu Oct 12 2017 Pavel Zhukov <pzhukov@redhat.com> - 1.2.0-6
- Use mariadb-connector-c-devel instead of mysql-devel (#1493628)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 03 2017 Jonathan Wakely <jwakely@redhat.com> - 1.2.0-3
- Rebuilt for Boost 1.64

* Fri May 26 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.2.0-2
- New release 1.2.0 (#1440348)

* Tue Apr 04 2017 Pavel Zhukov <landgraf@fedoraproject.org> - 1.1.0-3
- Add patch for OpenSSL 1.1. Fix FTBFS (#1423812)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Oct 04 2016 Jiri Popelka <jpopelka@redhat.com> - 1.1.0-1
- 1.1.0

* Thu Sep 01 2016 Jiri Popelka <jpopelka@redhat.com> - 1.1.0-0.1
- 1.1.0-beta

* Fri Aug 12 2016 Michal Toman <mtoman@fedoraproject.org> - 1.0.0-11
- No valgrind on MIPS

* Wed Aug 03 2016 Jiri Popelka <jpopelka@redhat.com> - 1.0.0-10
- %%{_defaultdocdir}/kea/ -> %%{_pkgdocdir}

* Fri May 13 2016 Jiri Popelka <jpopelka@redhat.com> - 1.0.0-9
- devel subpackage Requires: boost-devel

* Wed Mar 23 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.0.0-8
- Rebuild for log4cplus-1.2.0-2

* Wed Mar 23 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.0.0-7
- Rebuilding kea for log4cplus-1.2.0

* Wed Mar 16 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.0.0-6
- Editing pgsql_lease_mgr.cc according to upstream

* Fri Mar 11 2016 Zdenek Dohnal <zdohnal@redhat.com> - 1.0.0-4
- Fixing bugs created from new C++ standard

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 1.0.0-2
- Rebuilt for Boost 1.60

* Tue Dec 29 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.0-1
- 1.0.0

* Wed Dec 23 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.0-0.3.beta2
- fix compile error

* Wed Dec 23 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.0-0.2.beta2
- 1.0.0-beta2

* Wed Dec 09 2015 Jiri Popelka <jpopelka@redhat.com> - 1.0.0-0.1.beta
- 1.0.0-beta

* Mon Aug 24 2015 Jiri Popelka <jpopelka@redhat.com> - 0.9.2-3
- fix valgrind-devel availability

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Tue Jul 28 2015 Jiri Popelka <jpopelka@redhat.com> - 0.9.2-1
- 0.9.2

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 0.9.2-0.2.beta
- rebuild for Boost 1.58

* Thu Jul 02 2015 Jiri Popelka <jpopelka@redhat.com> - 0.9.2-0.1.beta
- 0.9.2-beta

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 0.9.1-2
- Rebuilt for GCC 5 C++11 ABI change

* Wed Apr 01 2015 Jiri Popelka <jpopelka@redhat.com> - 0.9.1-1
- 0.9.1

* Fri Feb 20 2015 Jiri Popelka <jpopelka@redhat.com> - 0.9.1-0.2.beta
- /run/kea/ (for logger_lockfile)

* Thu Feb 19 2015 Jiri Popelka <jpopelka@redhat.com> - 0.9.1-0.1.beta
- 0.9.1-beta

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 0.9-4
- Rebuild for boost 1.57.0

* Tue Nov 04 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9-3
- do not override @localstatedir@ globally
- include latest upstream kea.conf

* Wed Sep 24 2014 Dan Horák <dan[at]danny.cz> - 0.9-2
- valgrind available only on selected arches

* Mon Sep 01 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9-1
- 0.9

* Thu Aug 21 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9-0.5.beta1
- fix building with PostgreSQL on i686
- redefine localstatedir to sharedstatedir (kea#3523)

* Wed Aug 20 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9-0.4.beta1
- install systemd service units with a proper patch that we can send upstream
- build with MySQL & PostgreSQL & Google Test
- no need to copy sample configuration, /etc/kea/kea.conf already contains one

* Tue Aug 19 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9-0.3.beta1
- comment patches
- use --preserve-timestamps with install

* Mon Aug 18 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9-0.2.beta1
- make it build on armv7
- BuildRequires procps-ng for %%check
- use install instead of cp
- configure.ac: AC_PROG_LIBTOOL -> LT_INIT
- move license files to -libs

* Thu Aug 14 2014 Jiri Popelka <jpopelka@redhat.com> - 0.9-0.1.beta1
- initial spec

## END: Generated by rpmautospec
