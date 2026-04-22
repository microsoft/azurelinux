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
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 3.6.2-2
- Latest state for openvswitch

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
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
