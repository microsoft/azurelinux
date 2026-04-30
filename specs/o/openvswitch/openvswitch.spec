## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Uncomment these for snapshot releases:
# commit0 is the git sha of the last commit
# date is the date YYYYMMDD of the snapshot
#%%global commit0 bd916d13dbb845746983a6780da772154df647ba
#%%global date 20180219
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# If wants to run tests while building, specify the '--with check'
# option. For example:
# rpmbuild -bb --with check openvswitch.spec

# Enable PIE, bz#955181
%global _hardened_build 1

# RHEL-7 doesn't define _rundir macro yet
# Fedora 15 onwards uses /run as _rundir
%if 0%{!?_rundir:1}
%define _rundir /run
%endif

# To disable DPDK support, specify '--without dpdk' when building
%bcond_without dpdk

# To disable AF_XDP support, specify '--without afxdp' when building
%bcond_without afxdp

# test-suite is broken for big endians
# https://bugzilla.redhat.com/show_bug.cgi?id=1105458#c10
# "ofproto-dpif - select group with dp_hash selection method" test is broken on armv7lh
# FIXME often tests fails on non-x86_64 architectures due to timing problems
%ifarch x86_64
%bcond_without check
%else
%bcond_with check
%endif
# option to run kernel datapath tests, requires building as root!
%bcond_with check_datapath_kernel
# option to build with libcap-ng, needed for running OVS as regular user
%bcond_without libcapng


%if 0%{?centos} == 7
# Carried over from 2.6.1 CBS builds, introduced to win over 2.6.90
Epoch:   1
%endif

Name: openvswitch
Summary: Open vSwitch daemon/database/utilities
URL: https://www.openvswitch.org/
Version: 3.6.2
Release: %autorelease

# Nearly all of openvswitch is Apache-2.0.  The bugtool is LGPLv2+, and the
# lib/sflow*.[ch] files are SISSL
# datapath/ is GPLv2 (although not built into any of the binary packages)
License: Apache-2.0 AND LGPL-2.0-or-later AND SISSL

# NOTE: DPDK does not currently build for s390x
%define dpdkarches aarch64 i686 ppc64le x86_64

%if 0%{?commit0:1}
Source0: https://github.com/openvswitch/ovs/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
%else
Source0: https://www.openvswitch.org/releases/%{name}-%{version}.tar.gz
%endif
Source1: openvswitch.sysusers

# ovs-patches

# OVS (including OVN) backports (0 - 300)

BuildRequires: gcc gcc-c++ make
BuildRequires: autoconf automake libtool
BuildRequires: systemd-rpm-macros
BuildRequires: openssl openssl-devel
BuildRequires: python3-devel python3-six python3-setuptools python3-sortedcontainers
BuildRequires: python3-sphinx
BuildRequires: desktop-file-utils
BuildRequires: groff-base graphviz
BuildRequires: unbound-devel
BuildRequires: systemtap-sdt-devel
%if %{with afxdp}
BuildRequires: libxdp-devel libbpf-devel numactl-devel
%endif
# make check dependencies
BuildRequires: procps-ng
%if 0%{?rhel} > 7 || 0%{?fedora}
BuildRequires: groff
BuildRequires: python3-pyOpenSSL
%endif

%if %{with check_datapath_kernel}
BuildRequires: nmap-ncat
# would be useful but not available in RHEL or EPEL
#BuildRequires: pyftpdlib
%endif

%if %{with libcapng}
BuildRequires: libcap-ng libcap-ng-devel
%endif

%if %{with dpdk}
%ifarch %{dpdkarches}
BuildRequires: dpdk-devel libpcap-devel numactl-devel
# Currently DPDK on Extras/AppStream includes the mlx{4,5} glue libraries, so
# libibverbs is needed to run the tests (make check).
%if 0%{?rhel}
BuildRequires: libibverbs >= 15
%endif
%endif
%endif

Requires: openssl iproute module-init-tools
#Upstream kernel commit 4f647e0a3c37b8d5086214128614a136064110c3
#Requires: kernel >= 3.15.0-0

%{?systemd_requires}

Requires(post): /bin/sed
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives
Obsoletes: openvswitch-controller <= 0:2.1.0-1

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package -n python3-openvswitch
Summary: Open vSwitch python3 bindings
License: Apache-2.0
Requires: python3 python3-six
Obsoletes: python-openvswitch < 2.10.0-6
Provides: python-openvswitch = %{?epoch:%{epoch}:}%{version}-%{release}

%description -n python3-openvswitch
Python bindings for the Open vSwitch database

%package test
Summary: Open vSwitch testing utilities
License: Apache-2.0
BuildArch: noarch
Requires: python3-openvswitch = %{?epoch:%{epoch}:}%{version}-%{release}

%description test
Utilities that are useful to diagnose performance and connectivity
issues in Open vSwitch setup.

%package testcontroller
Summary: Simple controller for testing OpenFlow setups
License: Apache-2.0
Requires: openvswitch = %{?epoch:%{epoch}:}%{version}-%{release}

%description testcontroller
This controller enables OpenFlow switches that connect to it to act as
MAC-learning Ethernet switches.
It can be used for initial testing of OpenFlow networks.
It is not a necessary or desirable part of a production OpenFlow deployment.

%package devel
Summary: Open vSwitch OpenFlow development package (library, headers)
License: Apache-2.0

%description devel
This provides shared library, libopenswitch.so and the openvswitch header
files needed to build an external application.

%if 0%{?rhel} == 8 || ( 0%{?fedora} > 28 && 0%{?fedora} < 40)
%package -n network-scripts-%{name}
Summary: Open vSwitch legacy network service support
License: Apache-2.0
Requires: network-scripts
Supplements: (%{name} and network-scripts)

%description -n network-scripts-%{name}
This provides the ifup and ifdown scripts for use with the legacy network
service.
%endif

%package ipsec
Summary: Open vSwitch IPsec tunneling support
License: Apache-2.0
Requires: openvswitch libreswan
Requires: python3-openvswitch = %{?epoch:%{epoch}:}%{version}-%{release}

%description ipsec
This package provides IPsec tunneling support for OVS tunnels.

%if %{with dpdk}
%ifarch %{dpdkarches}
%package dpdk
Summary: Open vSwitch OpenFlow development package (switch, linked with DPDK)
License: Apache-2.0
Supplements: %{name}

%description dpdk
This provides ovs-vswitchd linked with DPDK library.
%endif
%endif

%prep
%if 0%{?commit0:1}
%autosetup -n ovs-%{commit0} -p 1
%else
%autosetup -p 1
%endif

%build
%if 0%{?commit0:1}
# fix the snapshot unreleased version to be the released one.
sed -i.old -e "s/^AC_INIT(openvswitch,.*,/AC_INIT(openvswitch, %{version},/" configure.ac
%endif

# BZ#2055576
rm -f python/ovs/dirs.py

# version.h and version.py should not be included in release tarball
rm -f include/openvswitch/version.h python/ovs/version.py

./boot.sh
mkdir build build-dpdk
pushd build
ln -s ../configure
%configure \
%if %{with libcapng}
        --enable-libcapng \
%else
        --disable-libcapng \
%endif
        --disable-static \
        --enable-shared \
        --enable-ssl \
        --with-pkidir=%{_sharedstatedir}/openvswitch/pki \
        --enable-usdt-probes \
        --with-version-suffix=-%{release} \
%if %{with afxdp}
        --enable-afxdp
%else
        --disable-afxdp
%endif
make %{?_smp_mflags}
popd
%if %{with dpdk}
%ifarch %{dpdkarches}
pushd build-dpdk
ln -s ../configure
%configure \
%if %{with libcapng}
        --enable-libcapng \
%else
        --disable-libcapng \
%endif
        --disable-static \
        --enable-shared \
        --enable-ssl \
        --enable-usdt-probes \
        --with-dpdk=shared \
        --with-pkidir=%{_sharedstatedir}/openvswitch/pki \
        --libdir=%{_libdir}/openvswitch-dpdk \
        --program-suffix=.dpdk \
        --with-version-suffix=-%{release} \
%if %{with afxdp}
        --enable-afxdp
%else
        --disable-afxdp
%endif
make %{?_smp_mflags}
popd
%endif
%endif

/usr/bin/python3 build-aux/dpdkstrip.py \
        --dpdk \
        < rhel/usr_lib_systemd_system_ovs-vswitchd.service.in \
        > rhel/usr_lib_systemd_system_ovs-vswitchd.service

%install
rm -rf $RPM_BUILD_ROOT

%if %{with dpdk}
%ifarch %{dpdkarches}
make -C build-dpdk install-exec DESTDIR=$RPM_BUILD_ROOT

# We only need ovs-vswitchd-dpdk and some libraries for dpdk subpackage
%if 0%{?fedora} < 42
rm -rf $RPM_BUILD_ROOT%{_bindir}
%endif
find $RPM_BUILD_ROOT%{_sbindir} -mindepth 1 -maxdepth 1 -not -name ovs-vswitchd.dpdk -delete
find $RPM_BUILD_ROOT%{_libdir}/openvswitch-dpdk -mindepth 1 -maxdepth 1 -not -name "libofproto*.so.*" -not -name "libopenvswitch*.so.*" -delete
%endif
%endif

make -C build install DESTDIR=$RPM_BUILD_ROOT
mv $RPM_BUILD_ROOT%{_sbindir}/ovs-vswitchd $RPM_BUILD_ROOT%{_sbindir}/ovs-vswitchd.nodpdk
touch $RPM_BUILD_ROOT%{_sbindir}/ovs-vswitchd

install -d -m 0755 $RPM_BUILD_ROOT%{_rundir}/openvswitch
install -d -m 0750 $RPM_BUILD_ROOT%{_localstatedir}/log/openvswitch
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch

install -p -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysusersdir}/openvswitch.conf

install -p -D -m 0644 rhel/usr_lib_udev_rules.d_91-vfio.rules \
        $RPM_BUILD_ROOT%{_udevrulesdir}/91-vfio.rules

install -p -D -m 0644 \
        rhel/usr_share_openvswitch_scripts_systemd_sysconfig.template \
        $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/openvswitch

for service in openvswitch ovsdb-server ovs-vswitchd ovs-delete-transient-ports \
               openvswitch-ipsec; do
        install -p -D -m 0644 \
                        rhel/usr_lib_systemd_system_${service}.service \
                        $RPM_BUILD_ROOT%{_unitdir}/${service}.service
done

install -m 0755 rhel/etc_init.d_openvswitch \
        $RPM_BUILD_ROOT%{_datadir}/openvswitch/scripts/openvswitch.init

install -p -D -m 0644 rhel/etc_openvswitch_default.conf \
        $RPM_BUILD_ROOT/%{_sysconfdir}/openvswitch/default.conf

install -p -D -m 0644 rhel/etc_logrotate.d_openvswitch \
        $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/openvswitch

install -m 0644 vswitchd/vswitch.ovsschema \
        $RPM_BUILD_ROOT/%{_datadir}/openvswitch/vswitch.ovsschema

%if ( 0%{?rhel} && 0%{?rhel} < 9 ) || ( 0%{?fedora} && 0%{?fedora} < 40)
install -d -m 0755 $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/network-scripts/
install -p -m 0755 rhel/etc_sysconfig_network-scripts_ifdown-ovs \
        $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/network-scripts/ifdown-ovs
install -p -m 0755 rhel/etc_sysconfig_network-scripts_ifup-ovs \
        $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/network-scripts/ifup-ovs
%endif

install -d -m 0755 $RPM_BUILD_ROOT%{python3_sitelib}
cp -a $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/ovstest \
        $RPM_BUILD_ROOT%{python3_sitelib}

# Build the JSON C extension for the Python lib (#1417738)
pushd python
(
export CPPFLAGS="-I ../build/include -I ../include"
export LDFLAGS="%{__global_ldflags} -L $RPM_BUILD_ROOT%{_libdir}"
%py3_build
%py3_install
[ -f "$RPM_BUILD_ROOT/%{python3_sitearch}/ovs/_json$(python3-config --extension-suffix)" ]
)
popd

rm -rf $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/

install -d -m 0755 $RPM_BUILD_ROOT/%{_sharedstatedir}/openvswitch

install -d -m 0755 $RPM_BUILD_ROOT%{_prefix}/lib/firewalld/services/

install -p -D -m 0755 \
        rhel/usr_share_openvswitch_scripts_ovs-systemd-reload \
        $RPM_BUILD_ROOT%{_datadir}/openvswitch/scripts/ovs-systemd-reload

touch $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch/conf.db
# The db needs special permission as IPsec Pre-shared keys are stored in it.
chmod 0640 $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch/conf.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch/system-id.conf

# remove unpackaged files
rm -f $RPM_BUILD_ROOT/%{_bindir}/ovs-benchmark \
        $RPM_BUILD_ROOT/%{_bindir}/ovs-docker \
        $RPM_BUILD_ROOT/%{_bindir}/ovs-parse-backtrace \
        $RPM_BUILD_ROOT/%{_sbindir}/ovs-vlan-bug-workaround \
        $RPM_BUILD_ROOT/%{_mandir}/man1/ovs-benchmark.1* \
        $RPM_BUILD_ROOT/%{_mandir}/man8/ovs-vlan-bug-workaround.8*

# remove ovn unpackages files
rm -f $RPM_BUILD_ROOT%{_bindir}/ovn*
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/ovn*
rm -f $RPM_BUILD_ROOT%{_mandir}/man5/ovn*
rm -f $RPM_BUILD_ROOT%{_mandir}/man7/ovn*
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/ovn*
rm -f $RPM_BUILD_ROOT%{_datadir}/openvswitch/ovn*
rm -f $RPM_BUILD_ROOT%{_datadir}/openvswitch/scripts/ovn*
rm -f $RPM_BUILD_ROOT%{_includedir}/ovn/*

%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

for dir in build \
%if %{with dpdk}
%ifarch %{dpdkarches}
build-dpdk \
%endif
%endif
; do
pushd $dir
%if %{with check}
    touch resolv.conf
    export OVS_RESOLV_CONF=$(pwd)/resolv.conf
    if make check TESTSUITEFLAGS='%{_smp_mflags}' ||
       make check TESTSUITEFLAGS='--recheck' ||
       make check TESTSUITEFLAGS='--recheck'; then :;
    else
        cat tests/testsuite.log
        exit 1
    fi
%endif
%if %{with check_datapath_kernel}
    if make check-kernel RECHECK=yes; then :;
    else
        cat tests/system-kmod-testsuite.log
        exit 1
    fi
%endif
popd
done

%preun
%if 0%{?systemd_preun:1}
    %systemd_preun %{name}.service
%else
    if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
        /bin/systemctl --no-reload disable %{name}.service >/dev/null 2>&1 || :
        /bin/systemctl stop %{name}.service >/dev/null 2>&1 || :
    fi
%endif

%pre
[ -L %{_sbindir}/ovs-vswitchd ] || rm -f %{_sbindir}/ovs-vswitchd

%post
%{_sbindir}/update-alternatives --install %{_sbindir}/ovs-vswitchd \
  ovs-vswitchd %{_sbindir}/ovs-vswitchd.nodpdk 10
if [ $1 -eq 1 ]; then
    sed -i 's:^#OVS_USER_ID=:OVS_USER_ID=:' /etc/sysconfig/openvswitch

    sed -i \
        's@OVS_USER_ID="openvswitch:openvswitch"@OVS_USER_ID="openvswitch:hugetlbfs"@'\
        /etc/sysconfig/openvswitch
fi
chown -R openvswitch:openvswitch /etc/openvswitch

%if 0%{?systemd_post:1}
    %systemd_post %{name}.service
%else
    # Package install, not upgrade
    if [ $1 -eq 1 ]; then
        /bin/systemctl daemon-reload >dev/null || :
    fi
%endif

%postun
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove ovs-vswitchd %{_sbindir}/ovs-vswitchd.nodpdk
fi
%if 0%{?systemd_postun:1}
    %systemd_postun %{name}.service
%else
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

%if %{with dpdk}
%ifarch %{dpdkarches}
%post dpdk
if grep -Fqw sse4_1 /proc/cpuinfo; then
    priority=20
else
    echo "Warning: the CPU doesn't support SSE 4.1, dpdk support is not enabled." >&2
    priority=5
fi
%{_sbindir}/update-alternatives --install %{_sbindir}/ovs-vswitchd \
  ovs-vswitchd %{_sbindir}/ovs-vswitchd.dpdk $priority

%postun dpdk
if [ $1 -eq 0 ] ; then
  %{_sbindir}/update-alternatives --remove ovs-vswitchd %{_sbindir}/ovs-vswitchd.dpdk
fi
%endif
%endif

%files -n python3-openvswitch
%{python3_sitearch}/ovs
%{python3_sitearch}/ovs-*.egg-info
%{_datadir}/openvswitch/bugtool-plugins/
%{_datadir}/openvswitch/scripts/ovs-bugtool-*
%{_datadir}/openvswitch/scripts/ovs-check-dead-ifs
%{_datadir}/openvswitch/scripts/ovs-vtep
%{_bindir}/ovs-dpctl-top
%{_sbindir}/ovs-bugtool
%{_mandir}/man8/ovs-dpctl-top.8*
%{_mandir}/man8/ovs-bugtool.8*
%doc LICENSE

%files test
%{_bindir}/ovs-pcap
%{_bindir}/ovs-tcpdump
%{_bindir}/ovs-tcpundump
%{_datadir}/openvswitch/scripts/usdt/*
%{_mandir}/man1/ovs-pcap.1*
%{_mandir}/man8/ovs-tcpdump.8*
%{_mandir}/man1/ovs-tcpundump.1*
%{_bindir}/ovs-test
%{_bindir}/ovs-vlan-test
%{_bindir}/ovs-l3ping
%{_mandir}/man8/ovs-test.8*
%{_mandir}/man8/ovs-vlan-test.8*
%{_mandir}/man8/ovs-l3ping.8*
%{python3_sitelib}/ovstest

%files testcontroller
%{_bindir}/ovs-testcontroller
%{_mandir}/man8/ovs-testcontroller.8*

%files devel
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/openvswitch/*
%{_includedir}/openflow/*
%exclude %{_libdir}/*.a

%if 0%{?rhel} == 8 || ( 0%{?fedora} > 28 && 0%{?fedora} < 40 )
%files -n network-scripts-%{name}
%{_sysconfdir}/sysconfig/network-scripts/ifup-ovs
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ovs
%endif

%files ipsec
%{_datadir}/openvswitch/scripts/ovs-monitor-ipsec
%{_unitdir}/openvswitch-ipsec.service

%if %{with dpdk}
%ifarch %{dpdkarches}
%files dpdk
%{_libdir}/openvswitch-dpdk/
%ghost %{_sbindir}/ovs-vswitchd
%{_sbindir}/ovs-vswitchd.dpdk
%endif
%endif

%files
%defattr(-,openvswitch,openvswitch)
%dir %{_sysconfdir}/openvswitch
%{_sysconfdir}/openvswitch/default.conf
%config %ghost %verify(not owner group md5 size mtime) %{_sysconfdir}/openvswitch/conf.db
%ghost %attr(0600,-,-) %verify(not owner group md5 size mtime) %{_sysconfdir}/openvswitch/.conf.db.~lock~
%config %ghost %{_sysconfdir}/openvswitch/system-id.conf
%defattr(-,root,root)
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sysconfig/openvswitch
%{_sysconfdir}/bash_completion.d/ovs-appctl-bashcomp.bash
%{_sysconfdir}/bash_completion.d/ovs-vsctl-bashcomp.bash
%config(noreplace) %{_sysconfdir}/logrotate.d/openvswitch
%{_unitdir}/openvswitch.service
%{_unitdir}/ovsdb-server.service
%{_unitdir}/ovs-vswitchd.service
%{_unitdir}/ovs-delete-transient-ports.service
%{_datadir}/openvswitch/scripts/openvswitch.init
%{_datadir}/openvswitch/scripts/ovs-lib
%{_datadir}/openvswitch/scripts/ovs-save
%{_datadir}/openvswitch/scripts/ovs-ctl
%{_datadir}/openvswitch/scripts/ovs-kmod-ctl
%{_datadir}/openvswitch/scripts/ovs-systemd-reload
%config %{_datadir}/openvswitch/local-config.ovsschema
%config %{_datadir}/openvswitch/vswitch.ovsschema
%config %{_datadir}/openvswitch/vtep.ovsschema
%{_bindir}/ovs-appctl
%{_bindir}/ovs-dpctl
%{_bindir}/ovs-flowviz
%{_bindir}/ovs-ofctl
%{_bindir}/ovs-vsctl
%{_bindir}/ovsdb-client
%{_bindir}/ovsdb-tool
%{_bindir}/ovs-pki
%{_bindir}/vtep-ctl
%{_libdir}/*.so.*
%ghost %{_sbindir}/ovs-vswitchd
%{_sbindir}/ovs-vswitchd.nodpdk
%{_sbindir}/ovsdb-server
%{_mandir}/man1/ovsdb-client.1*
%{_mandir}/man1/ovsdb-server.1*
%{_mandir}/man1/ovsdb-tool.1*
%{_mandir}/man5/ovsdb.5*
%{_mandir}/man5/ovsdb.local-config.5*
%{_mandir}/man5/ovsdb-server.5.*
%{_mandir}/man5/ovs-vswitchd.conf.db.5*
%{_mandir}/man5/vtep.5*
%{_mandir}/man7/ovsdb-server.7*
%{_mandir}/man7/ovsdb.7*
%{_mandir}/man7/ovs-actions.7*
%{_mandir}/man7/ovs-fields.7*
%{_mandir}/man8/vtep-ctl.8*
%{_mandir}/man8/ovs-appctl.8*
%{_mandir}/man8/ovs-ctl.8*
%{_mandir}/man8/ovs-dpctl.8*
%{_mandir}/man8/ovs-flowviz.8*
%{_mandir}/man8/ovs-kmod-ctl.8.*
%{_mandir}/man8/ovs-ofctl.8*
%{_mandir}/man8/ovs-pki.8*
%{_mandir}/man8/ovs-vsctl.8*
%{_mandir}/man8/ovs-vswitchd.8*
%{_mandir}/man8/ovs-parse-backtrace.8*
%{_udevrulesdir}/91-vfio.rules
%doc LICENSE NOTICE README.rst NEWS rhel/README.RHEL.rst
/var/lib/openvswitch
%attr(750,openvswitch,openvswitch) %verify(not owner group) /var/log/openvswitch
%ghost %attr(755,root,root) %verify(not owner group) %{_rundir}/openvswitch
%if (0%{?rhel} && 0%{?rhel} <= 7) || (0%{?fedora} && 0%{?fedora} < 29)
%{_sysconfdir}/sysconfig/network-scripts/ifup-ovs
%{_sysconfdir}/sysconfig/network-scripts/ifdown-ovs
%endif
%{_sysusersdir}/openvswitch.conf

%changelog
## START: Generated by rpmautospec
* Thu Apr 30 2026 Daniel McIlvaney <damcilva@microsoft.com> - 3.6.2-2
- test: add initial lock files

* Fri Feb 13 2026 Timothy Redaelli <timothy.redaelli@gmail.com> - 3.6.2-1
- Update to 3.6.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.6.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Aug 25 2025 Timothy Redaelli <tredaelli@redhat.com> - 3.6.0-1
- Update to 3.6.0

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.5.1-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 20 2025 Adrian Moreno <amorenoz@redhat.com> - 3.5.1-2
- sysusers: add hugetlbfs

* Tue Jun 17 2025 Timothy Redaelli <tredaelli@redhat.com> - 3.5.1-1
- Update to 3.5.1

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.4.1-5
- Rebuilt for Python 3.14

* Fri May 30 2025 Timothy Redaelli <tredaell@fedoraproject.org> - 3.4.1-4
- Merge #19 `Drop call to %%sysusers_create_compat`

* Tue Feb 11 2025 Timothy Redaelli <tredaelli@redhat.com> - 3.4.1-3
- Fix building on rawhide

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Timothy Redaelli <tredaelli@redhat.com> - 3.4.1-1
- Update to 3.4.1 (with DPDK 24.11.1)

* Tue Aug 27 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.4.0-3
- version.h and version.py should not be included in release version

* Tue Aug 27 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.4.0-2
- Add -release to version

* Tue Aug 27 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.3.0-4
- Backport "tests: Fix compatibility issue with Python 3.13 in vlog.at."

* Tue Jul 09 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.3.0-3
- Rebuilt with dpdk 23.11

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.3.0-2
- Rebuilt for Python 3.13

* Thu Mar 07 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Oct 04 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.1.1-4
- Rebuilt for Python 3.12

* Thu Jun 08 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.1-3
- Backport "cpu: Fix cpuid check for some AMD processors."

* Mon May 22 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.1-2
- Replace fgrep with grep -F Delete ovs-vswitchd, if it's not a link

* Fri Apr 14 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.1-1
- Update for 3.1.1, includes fixes for CVE-2023-1668

* Wed Mar 15 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.0-3
- Sync spec file with upstream and RHEL

* Fri Mar 03 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.0-2
- Added missing openvswitch-3.1.0.tar.gz source file

* Fri Mar 03 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Wed Feb 01 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.0.3-1
- Rebase to 3.0.3, includes fixes for CVE-2022-4337

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Timothy Redaelli <tredaelli@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.17.0-6
- Rebuilt for Python 3.11

* Tue May 24 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-5
- Fix %%post dpdk

* Tue May 24 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-4
- Create openvswitch-dpdk subpackage, install it by default (weak
  dependency), but enable it only if the CPU is new enough

* Mon Mar 28 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-3
- Be sure dirs.py is updated

* Tue Mar 15 2022 Christian Glombek <lorbus@fedoraproject.org> - 2.17.0-2
- Provide a sysusers.d file to get user() and group() provides

* Fri Mar 11 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 22 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.16.0-2
- Commit sources

* Wed Sep 22 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.16.0-1
- Update to 2.16.0 (#1978767)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.15.0-8
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.15.0-6
- Rebuilt for Python 3.10

* Wed Feb 24 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-5
- Move scripts that requires python in python3-openvswitch

* Tue Feb 23 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-4
- Add openvswitch-testcontroller subpackage since it's required by mininet

* Mon Feb 22 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-3
- Add python3-sortedcontainers as dependency

* Sun Feb 21 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.15.0-2
- Properly build with dpdk specifying shared option

* Wed Feb 17 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-1
- Updated to 2.15.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 19 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.14.0-6
- Fix building OVS on ppc64le and armv7hl

* Thu Nov 19 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.14.0-5
- Move patches

* Thu Nov 19 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.14.0-4
- Backport patches for CVE-2015-8011

* Mon Sep 14 2020 Aaron Conole <aconole@redhat.com> - 2.14.0-3
- Add missing changelog entry

* Mon Sep 14 2020 Aaron Conole <aconole@fedoraproject.org> - 2.14.0-2
- Merge #11 `hugetlbfs group should be added as a system group`

* Tue Sep 01 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.14.0-1
- Updated to 2.14.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <miro@hroncok.cz> - 2.13.0-3
- Rebuilt for Python 3.9

* Thu Apr 09 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.13.0-2
- Add BuildRequires: groff and fix ovstest path

* Tue Apr 07 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.13.0-1
- Updated to 2.13.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Vladimír Beneš <vbenes@redhat.com> - 2.12.0-2
- tests: add tests definition file

* Sat Sep 14 2019 Flavio Leitner <fbl@redhat.com> - 2.12.0-1
- Updated to 2.12.0

* Mon Aug 19 2019 Miro Hrončok <miro@hroncok.cz> - 2.11.1-5
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 03 2019 Charalampos Stratakis <cstratak@redhat.com> - 2.11.1-3
- Don't hard-code python's abi flags

* Fri May 10 2019 Timothy Redaelli <tredaelli@redhat.com> - 2.11.1-2
- Remove unwanted openvswitch.spec from .gitignore

* Wed May 08 2019 Timothy Redaelli <tredaelli@redhat.com> - 2.11.1-1
- Rebase to 2.11.1 Ignore sortedcontainer python2.7 dependency

* Thu Apr 11 2019 Numan Siddique <numan.siddique@gmail.com> - 2.11.0-5
- Remove openvswitch-ovn* packages

* Fri Mar 08 2019 Timothy Redaelli <tredaelli@redhat.com> - 2.11.0-4
- Release bump

* Fri Mar 08 2019 Timothy Redaelli <tredaelli@redhat.com> - 2.11.0-3
- Add libmnl as build requirement in RHEL/CentOS

* Thu Feb 28 2019 Timothy Redaelli <tredaelli@redhat.com> - 2.11.0-2
- Fix tests on koji/mock

* Thu Feb 28 2019 Timothy Redaelli <tredaelli@redhat.com> - 2.11.0-1
- Rebase to 2.11.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.10.1-3
- Remove unneeded %%clean section

* Thu Nov 29 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.1-2
- Update sources file

* Thu Nov 29 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.1-1
- Rebase to 2.10.1

* Wed Nov 21 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-9
- Fix C JSON library creation on Fedora Rawhide and exit if shared library
  cannot be created

* Wed Nov 21 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-8
- Clean up spec file in order to build with RHEL7, RHEL8 and Fedora

* Fri Nov 02 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-7
- Build for any architectures

* Thu Oct 11 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-6
- Enable tests only for x86_64

* Thu Oct 11 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-5
- Rebuilt for new unbound

* Fri Oct 05 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-4
- Backport ovn.at: Skip ACL rate-limiting test on slow/overloaded

* Fri Oct 05 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-3
- python2-sphinx is removed, use python3-sphinx instead

* Fri Oct 05 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-2
- Fix build

* Fri Oct 05 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.10.0-1
- Align with "Fast Datapath" 2.10.0-10

* Fri Sep 14 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.2-9
- Backport "Add ovs.compat module to python package" (#1619712) Backport a
  variant of "dhparams: Fix .c file generation with OpenSSL >= 1.1.1-pre9"

* Mon Aug 13 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.2-8
- Backport "Don't enable new TLS versions by default"

* Mon Aug 06 2018 Lubomir Rintel <lkundrak@v3.sk> - 2.9.2-7
- Split out the network-scripts

* Wed Aug 01 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.2-6
- Build OVS as shared library Build the C json native extension for Python
  (60x faster) Fix TPS VerifyTest (rpm -V) by do not verify md5, size and
  mtime of /etc/sysconfig/openvswitch Backport spec file modfications from
  "rhel: Use openvswitch user/group for the log directory"

* Thu Jul 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.9.2-5
- add BuildRequires: gcc-c++

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 04 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.2-3
- Backport a patch to make some tests pass on Fedora Rawhide

* Fri Jun 22 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.2-2
- Do not run "make check" simultaneously.

* Tue Jun 19 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.2-1
- Update to OVS 2.9.2

* Tue Jun 19 2018 Miro Hrončok <miro@hroncok.cz> - 2.9.1-2
- Rebuilt for Python 3.7

* Tue May 22 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.1-1
- Update to 2.9.1

* Tue Apr 10 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.0-7
- Align with with RHEL "Fast Datapath" 2.9.0-15 Backport "rhel: don't drop
  capabilities when running as root" Change owner of /etc/openvswitch
  during upgrade Use DPDK as shared library

* Thu Feb 22 2018 Alan Pevec <alan.pevec@redhat.com> - 2.9.0-6
- Group: tag should not be used

* Tue Feb 20 2018 Timothy Redaelli <tredaell@fedoraproject.org> - 2.9.0-5
- Merge #2 `Update Python 2 dependency declarations to new packaging
  standards`

* Tue Feb 20 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.0-4
- Align to RHEL "Fast Datapath" channel 2.9.0-3

* Tue Feb 20 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.0-3
- Release bump

* Tue Feb 20 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.0-2
- Align totally with RHEL Fast Datapath

* Tue Feb 20 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.9.0-1
- Update to Open vSwitch 2.9.0 and DPDK 17.11 Align with RHEL "Fast
  Datapath" channel 2.9.0-1

* Mon Feb 19 2018 Timothy Redaelli <tredaelli@redhat.com> - 2.8.1-5
- Add BuildRequires: gcc

* Wed Feb 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.8.1-4
- Remove %%clean section

* Fri Feb 09 2018 Aaron Conole <aconole@bytheb.org> - 2.8.1-3
- ovs: fix permissions issues on install

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 02 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.8.1-1
- Update to Open vSwitch 2.8.1

* Tue Sep 19 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.8.0-2
- Update DPDK to 17.05.2 (bugfixes)

* Mon Sep 04 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.8.0-1
- Update to Open vSwitch 2.8.0 and DPDK 17.05.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-3
- Rebuilt for
  https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 19 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.2-1
- Update to Open vSwitch 2.7.2 Add a symlink of the OCF script in the OCF
  resources folder

* Fri Jul 14 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.1-4
- Fix typo in changelog

* Fri Jul 14 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.1-3
- Backport fix for CVE-2017-9263 and CVE-2017-9265

* Thu Jul 06 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.1-2
- Update .gitignore and sources

* Thu Jul 06 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.1-1
- Updated to Open vSwitch 2.7.1 + DPDK 16.11.2

* Tue Jun 13 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-12
- Backport fix for CVE-2017-9264

* Thu Jun 08 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-11
- Remove PYTHONCOERCECLOCALE=0 workaround and backport upstream patch

* Wed May 31 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-10
- Backport fix for CVE-2017-9214

* Mon May 29 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-9
- Install OVN firewalld files

* Wed May 24 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-8
- Add bz for PYTHONCOERCECLOCALE=0 workaround

* Wed May 24 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-7
- Disable tests on armv7hl

* Mon May 22 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-6
- Fixed python3 tests by setting PYTHONCOERCECLOCALE=0

* Sun May 21 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-5
- FIXME Disable python3 tests (fails on f26 and rawhide with python 3.6)

* Fri May 19 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-4
- Build OVS without DPDK support on all architectures not supported by DPDK

* Fri May 19 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-3
- Link statically with DPDK 16.11.1 and add python3-six as BuildRequires
- Link statically is needed since DPDK package in Fedora is moving faster
  than what is supported by Open vSwitch.

* Fri Mar 03 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-2
- Fix check dependencies

* Fri Feb 24 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.7.0-1
- Updated to Open vSwitch 2.7.0

* Thu Feb 16 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.6.1-6
- Added python3-openvswitch and renamed python-openvswitch to
  python2-openvswitch

* Thu Feb 16 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.6.1-5
- Remove python/compat license comment

* Thu Feb 16 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.6.1-4
- Remove PyQt4 dependency

* Tue Feb 14 2017 Timothy Redaelli <tredaelli@redhat.com> - 2.6.1-3
- Fix some mixed-use-of-spaces-and-tabs rpmlint warnings

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Flavio Leitner <fbl@redhat.com> - 2.6.1-1
- Updated to 2.6.1

* Tue Nov 01 2016 Aaron Conole <aconole@redhat.com> - 2.6.0-1
- Update to 2.6.0

* Wed Aug 24 2016 Dan Horák <dan@danny.cz> - 2.5.0-5
- don't run the test-suite for big endian arches

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Tue Mar 15 2016 Panu Matilainen <pmatilai@redhat.com> - 2.5.0-3
- Gaah, remember to bump release

* Tue Mar 15 2016 Panu Matilainen <pmatilai@redhat.com> - 2.5.0-2
- Remove unpackaged files instead of excluding (#1281913)

* Wed Mar 02 2016 Panu Matilainen <pmatilai@redhat.com> - 2.5.0-1
- Update to 2.5.0

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 25 2015 Flavio Leitner <fbl@redhat.com> - 2.4.0-1
- Updated to 2.4.0

* Fri Jun 19 2015 Flavio Leitner <fbl@redhat.com> - 2.3.2-1
- Updated to 2.3.2

* Thu Jun 18 2015 Dennis Gilmore <dennis@ausil.us> - 2.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 27 2015 Flavio Leitner <fbl@redhat.com> - 2.3.1-3
- Updated to 2.3.1-git4750c96

* Wed Jan 14 2015 Flavio Leitner <fbl@redhat.com> - 2.3.1-2
- Updated to 2.3.1-git3282e51

* Fri Dec 12 2014 Flavio Leitner <fbl@redhat.com> - 2.3.1-1
- Updated to 2.3.1

* Fri Nov 07 2014 Flavio Leitner <fbl@redhat.com> - 2.3.0-3
- Updated to 2.3.0-git39ebb203

* Thu Oct 23 2014 Flavio Leitner <fbl@redhat.com> - 2.3.0-2
- Fixed to own conf.db and system-id.conf in /etc/openvswitch.

* Thu Aug 21 2014 Flavio Leitner <fbl@redhat.com> - 2.3.0-1
- Updated to 2.3.0

* Sun Aug 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> - 2.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 Flavio Leitner <fbl@redhat.com> - 2.1.2-4
- Moved README.RHEL to be in the standard doc dir. Added FAQ and NEWS files
  to the doc list. Excluded PPC arch

* Thu Jun 12 2014 Flavio Leitner <fbl@redhat.com> - 2.1.2-3
- Removed ovsdbmonitor packaging

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 13 2014 Flavio Leitner <fbl@redhat.com> - 2.1.2-1
- Updated to 2.1.2

* Fri Apr 04 2014 Flavio Leitner <fbl@redhat.com> - 2.1.0-1
- updated to 2.1.0

* Fri Mar 07 2014 Flavio Leitner <fbl@redhat.com> - 2.0.1-1
- updated to 2.0.1

* Mon Jan 27 2014 Chris Wright <chrisw@redhat.com> - 2.0.0-6
- openvswitch -devel package

* Wed Jan 15 2014 Flavio Leitner <fbl@redhat.com> - 2.0.0-5
- enable DHCP support for internal ports

* Wed Jan 15 2014 Flavio Leitner <fbl@redhat.com> - 2.0.0-4
- disabled ovsdbmonitor packaging

* Wed Jan 15 2014 Flavio Leitner <fbl@redhat.com> - 2.0.0-3
- fedora package: fix systemd ordering and deps.

* Wed Jan 15 2014 Flavio Leitner <fbl@redhat.com> - 2.0.0-2
- util: use gcc builtins to better check array sizes

* Mon Oct 28 2013 Flavio Leitner <fbl@redhat.com> - 2.0.0-1
- updated to 2.0.0 (#1023184)

* Mon Oct 28 2013 Flavio Leitner <fbl@redhat.com> - 1.11.0-8
- rhel: Option to create tunnel through ifcfg scripts.

* Mon Oct 28 2013 Flavio Leitner <fbl@redhat.com> - 1.11.0-7
- rhel: Set STP of a bridge during bridge creation.

* Mon Oct 28 2013 Flavio Leitner <fbl@redhat.com> - 1.11.0-6
- rhel: Prevent duplicate ifup calls.

* Mon Oct 28 2013 Flavio Leitner <fbl@redhat.com> - 1.11.0-5
- rhel: Return an exit value of 0 for ifup-ovs.

* Mon Oct 28 2013 Flavio Leitner <fbl@redhat.com> - 1.11.0-4
- Added RHEL ovs-ifup STP option handling

* Tue Oct 01 2013 Flavio Leitner <fbl@redhat.com> - 1.11.0-3
- don't use /var/lock/subsys with systemd (#1006412)

* Fri Sep 20 2013 Flavio Leitner <fbl@redhat.com> - 1.11.0-2
- ovsdbmonitor package is now optional

* Thu Aug 29 2013 Thomas Graf <tgraf@redhat.com> - 1.11.0-1
- Update to 1.11.0

* Wed Aug 14 2013 Flavio Leitner <fbl@redhat.com> - 1.10.0-8
- Fixed openvswitch-nonetwork to start openvswitch.service (#996804)

* Sat Aug 03 2013 Petr Písař <ppisar@redhat.com> - 1.10.0-7
- Perl 5.18 rebuild

* Tue Jul 23 2013 Thomas Graf <tgraf@redhat.com> - 1.10.0-6
- Fix typo

* Tue Jul 23 2013 Thomas Graf <tgraf@redhat.com> - 1.10.0-5
- spec file fixes and keep local copy of sysconfig.template

* Thu Jul 18 2013 Petr Písař <ppisar@redhat.com> - 1.10.0-4
- Perl 5.18 rebuild

* Mon Jul 01 2013 Thomas Graf <tgraf@redhat.com> - 1.10.0-3
- Provide native systemd unit files (#818754)

* Mon Jul 01 2013 Thomas Graf <tgraf@redhat.com> - 1.10.0-2
- Enable PIE (#955181)

* Thu May 02 2013 Thomas Graf <tgraf@redhat.com> - 1.10.0-1
- Update to 1.10.0 (#958814)

* Thu Feb 28 2013 Thomas Graf <tgraf@redhat.com> - 1.9.0-1
- Update to 1.9.0 (#916537)

* Tue Feb 12 2013 Thomas Graf <tgraf@redhat.com> - 1.7.3-3
- Fix systemd service dependency loop (#818754)

* Fri Jan 25 2013 Thomas Graf <tgraf@redhat.com> - 1.7.3-2
- Auto-start openvswitch service on ifup/ifdown (#818754)

* Thu Jan 24 2013 Thomas Graf <tgraf@redhat.com> - 1.7.3-1
- Update to openvswitch 1.7.3 (#903599)

* Tue Nov 20 2012 Thomas Graf <tgraf@suug.ch> - 1.7.1-7
- Increase max fd limit to support 256 bridges (#873072)

* Thu Nov 01 2012 Thomas Graf <tgraf@suug.ch> - 1.7.1-6
- Don't create world writable pki/*/incomming directory (#845351)

* Thu Oct 25 2012 Thomas Graf <tgraf@suug.ch> - 1.7.1-5
- Don't add iptables accept rule for -p GRE as GRE tunneling is unsupported

* Tue Oct 16 2012 Thomas Graf <tgraf@suug.ch> - 1.7.1-4
- bump spec file for systemd require fix (#850258)

* Tue Oct 16 2012 Thomas Graf <tgraf@suug.ch> - 1.7.1-3
- Require systemd instead of systemd-units to use F18+ helper macros
  (#850258)

* Tue Oct 09 2012 Thomas Graf <tgraf@suug.ch> - 1.7.1-2
- make ovs-vsctl timeout if daemon is not running (#858722)

* Mon Sep 10 2012 Thomas Graf <tgraf@suug.ch> - 1.7.1-1
- Update to Open vSwitch 1.7.1 (#855601)

* Fri Sep 07 2012 Thomas Graf <tgraf@suug.ch> - 1.7.0-3
- package ovs-controller as separate openvswitch-controller (#815628)

* Thu Aug 23 2012 Tomas Hozza <thozza@redhat.com> - 1.7.0-2
- fixed SPEC file so it comply with new systemd-rpm macros guidelines
  (#850258)

* Fri Aug 17 2012 Tomas Hozza <thozza@redhat.com> - 1.7.0-1
- Update to 1.7.0
- Fixed openvswitch-configure-ovskmod-var-autoconfd.patch because
  openvswitch kernel module name changed in 1.7.0
- Removed Source8: ovsdbmonitor-move-to-its-own-data-directory.patch
- Patches merged:
- ovsdbmonitor-move-to-its-own-data-directory-automaked.patch
- openvswitch-rhel-initscripts-resync.patch

* Fri Jul 20 2012 Dennis Gilmore <dennis@ausil.us> - 1.4.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Mar 15 2012 Chris Wright <chrisw@sous-sol.org> - 1.4.0-6
- missed patch in commit 87a74a57, add it to really fix (#803843)

* Thu Mar 15 2012 Chris Wright <chrisw@sous-sol.org> - 1.4.0-5
- fix ovs network initscripts DHCP address acquisition (#803843)

* Tue Mar 06 2012 Chris Wright <chrisw@sous-sol.org> - 1.4.0-4
- make BuildRequires openssl explicit (needed on f18/rawhide now)

* Tue Mar 06 2012 Chris Wright <chrisw@sous-sol.org> - 1.4.0-3
- Update specfile to use glob to catch compressed manpages

* Tue Mar 06 2012 Chris Wright <chrisw@sous-sol.org> - 1.4.0-2
- Initial import (#799171).

* Tue Feb 20 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 2.9.0-1
- Update Python 2 dependency declarations to new packaging standards

* Mon Dec 16 2019 Edgar Hoch <edgar.hoch@ims.uni-stuttgart.de> - 2.12.0-1
- hugetlbfs group should be added as a system group

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.4.1-3
- Drop call to %%sysusers_create_compat

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Timothy Redaelli <tredaelli@redhat.com> - 3.4.1-1
- Update to 3.4.1 (with DPDK 24.11.1)

* Tue Aug 27 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.4.0-3
- version.h and version.py should not be included in release version

* Tue Aug 27 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.4.0-2
- Add -release to version

* Tue Aug 27 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.4.0-1
- Update to 3.4.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.3.0-4
- Backport "tests: Fix compatibility issue with Python 3.13 in vlog.at."

* Tue Jul 09 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.3.0-3
- Rebuilt with dpdk 23.11

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.3.0-2
- Rebuilt for Python 3.13

* Thu Mar 07 2024 Timothy Redaelli <tredaelli@redhat.com> - 3.3.0-1
- Update to 3.3.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.2.1-1
- Update to 3.2.1

* Wed Oct 04 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.2.0-1
- Update to 3.2.0

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.1.1-4
- Rebuilt for Python 3.12

* Thu Jun 08 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.1-3
- Backport "cpu: Fix cpuid check for some AMD processors."

* Mon May 22 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.1-2
- Replace fgrep with grep -F Delete ovs-vswitchd, if it's not a link

* Fri Apr 14 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.1-1
- Update for 3.1.1, includes fixes for CVE-2023-1668

* Wed Mar 15 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.0-3
- Sync spec file with upstream and RHEL

* Fri Mar 03 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.0-2
- Added missing openvswitch-3.1.0.tar.gz source file

* Fri Mar 03 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Wed Feb 01 2023 Timothy Redaelli <tredaelli@redhat.com> - 3.0.3-1
- Rebase to 3.0.3, includes fixes for CVE-2022-4337

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 29 2022 Timothy Redaelli <tredaelli@redhat.com> - 3.0.1-1
- Update to 3.0.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 2.17.0-6
- Rebuilt for Python 3.11

* Tue May 24 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-5
- Fix %%post dpdk

* Tue May 24 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-4
- Create openvswitch-dpdk subpackage, install it by default (weak
  dependency), but enable it only if the CPU is new enough

* Mon Mar 28 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-3
- Be sure dirs.py is updated

* Tue Mar 15 2022 Christian Glombek <lorbus@fedoraproject.org> - 2.17.0-2
- Provide a sysusers.d file to get user() and group() provides

* Fri Mar 11 2022 Timothy Redaelli <tredaelli@redhat.com> - 2.17.0-1
- Update to 2.17.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 22 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.16.0-2
- Commit sources

* Wed Sep 22 2021 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 2.16.0-1
- Update to 2.16.0 (#1978767)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.15.0-8
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.15.0-6
- Rebuilt for Python 3.10

* Wed Feb 24 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-5
- Move scripts that requires python in python3-openvswitch

* Tue Feb 23 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-4
- Add openvswitch-testcontroller subpackage since it's required by mininet

* Mon Feb 22 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-3
- Add python3-sortedcontainers as dependency

* Sun Feb 21 2021 Mamoru TASAKA <mtasaka@fedoraproject.org> - 2.15.0-2
- Properly build with dpdk specifying shared option

* Wed Feb 17 2021 Timothy Redaelli <tredaelli@redhat.com> - 2.15.0-1
- Updated to 2.15.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 19 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.14.0-6
- Fix building OVS on ppc64le and armv7hl

* Thu Nov 19 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.14.0-5
- Move patches

* Thu Nov 19 2020 Timothy Redaelli <tredaelli@redhat.com> - 2.14.0-4
- Backport patches for CVE-2015-8011

* Mon Sep 14 2020 Aaron Conole <aconole@redhat.com> - 2.14.0-3
- Add missing changelog entry

* Mon Sep 14 2020 Aaron Conole <aconole@fedoraproject.org> - 2.14.0-2
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
