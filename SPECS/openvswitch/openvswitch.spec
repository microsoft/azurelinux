# https://linux.mellanox.com/public/repo/doca/3.3.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-26.01-1.0.0.0.tgz
#
# Spec file for Open vSwitch.
#
# Copyright (C) 2009, 2010, 2013, 2014, 2015, 2016 Nicira Networks, Inc.
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without warranty of any kind.

# If libcap-ng isn't available and there is no need for running OVS
# as regular user, specify the '--without libcapng'
%bcond_without libcapng
# To enable DPDK support, specify '--with dpdk' when building
%bcond_with dpdk
# To enable AF_XDP support, specify '--without afxdp' to disable
%bcond_without afxdp
%if %{with dpdk}
%{!?dpdk_datadir:%define dpdk_datadir /opt/mellanox/dpdk}
%endif

# Enable PIE, bz#955181
%global _hardened_build 1

# Bytecompiling with python3
%global __python %{__python3}

Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        3.3.0040
Release:        1%{?dist}
License:        Proprietary
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Daemons
URL:            http://www.openvswitch.org/
Source0:        %{_distro_sources_url}/%{name}-%{version}.tar.gz
Source1:        openvswitch.sysusers

BuildRequires: gcc gcc-c++
BuildRequires: autoconf automake libtool
BuildRequires: systemd-rpm-macros openssl openssl-devel
BuildRequires: python3-devel
BuildRequires: desktop-file-utils
BuildRequires: groff graphviz
BuildRequires: python3-sphinx
# make check dependencies
BuildRequires: procps-ng
%if %{with libcapng}
BuildRequires: libcap-ng libcap-ng-devel
%endif
%if %{with dpdk}
BuildRequires: libpcap-devel numactl-devel
BuildRequires: dpdk-devel >= 25.11
Provides: %{name}-dpdk = %{version}-%{release}
%endif
%if %{with afxdp}
BuildRequires: libxdp-devel libbpf-devel numactl-devel
%endif
BuildRequires: unbound unbound-devel

Requires: openssl hostname iproute module-init-tools unbound

%{?systemd_requires}
%{?sysusers_requires_compat}

Requires(post): /bin/sed
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Obsoletes: openvswitch-controller <= 0:2.1.0-1

# to skip running checks, pass --without check
%bcond_without check
%bcond_with check_datapath_kernel

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package -n python3-openvswitch
Summary: Open vSwitch python3 bindings
License: Proprietary
BuildArch: noarch
Requires: python3
Suggests: python3-netaddr python3-pyparsing python3-unbound
%{?python_provide:%python_provide python3-openvswitch = %{version}-%{release}}

%description -n python3-openvswitch
Python bindings for the Open vSwitch database

%package test
Summary: Open vSwitch testing utilities
License: Proprietary
BuildArch: noarch

%description test
Utilities that are useful to diagnose performance and connectivity
issues in Open vSwitch setup.

%package devel
Summary: Open vSwitch OpenFlow development package (library, headers)
License: Proprietary

%description devel
This provides shared library, libopenswitch.so and the openvswitch header
files needed to build an external application.

%package ipsec
Summary: Open vSwitch IPsec tunneling support
License: Proprietary
Requires: openvswitch python3-openvswitch libreswan

%description ipsec
This package provides IPsec tunneling support for OVS tunnels.

%prep
%setup -q

%build
%configure \
%if %{with libcapng}
        --enable-libcapng \
%else
        --disable-libcapng \
%endif
%if %{with dpdk}
        --with-dpdk=$(dirname %{dpdk_datadir}) \
%endif
%if %{with afxdp}
        --enable-afxdp \
%else
        --disable-afxdp \
%endif
        --enable-ssl \
        --enable-shared \
        --disable-static \
        --with-pkidir=%{_sharedstatedir}/openvswitch/pki \
        PYTHON3=%{__python3}

build-aux/dpdkstrip.py \
%if %{with dpdk}
        --dpdk \
%else
        --nodpdk \
%endif
        < rhel/usr_lib_systemd_system_ovs-vswitchd.service.in \
        > rhel/usr_lib_systemd_system_ovs-vswitchd.service

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT%{_rundir}/openvswitch
install -d -m 0750 $RPM_BUILD_ROOT%{_localstatedir}/log/openvswitch
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch

install -p -D -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysusersdir}/openvswitch.conf

%if %{with dpdk}
install -p -D -m 0644 rhel/usr_lib_udev_rules.d_91-vfio.rules \
        $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/91-vfio.rules
%endif

install -p -D -m 0644 \
        rhel/usr_share_openvswitch_scripts_systemd_sysconfig.template \
        $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/openvswitch
for service in openvswitch ovsdb-server ovs-vswitchd ovs-delete-transient-ports \
                openvswitch-ipsec ovs-exporter; do
        install -p -D -m 0644 \
                        rhel/usr_lib_systemd_system_${service}.service \
                        $RPM_BUILD_ROOT%{_unitdir}/${service}.service
done
install -m 0755 rhel/etc_init.d_openvswitch \
        $RPM_BUILD_ROOT%{_datadir}/openvswitch/scripts/openvswitch.init

install -p -D -m 0644 rhel/etc_openvswitch_default.conf \
        $RPM_BUILD_ROOT/%{_sysconfdir}/openvswitch/default.conf

install -p -D -m 0644 rhel/etc_openvswitch_ovs-exporter.conf \
        $RPM_BUILD_ROOT/%{_sysconfdir}/openvswitch/ovs-exporter.conf

install -p -D -m 0644 rhel/etc_logrotate.d_openvswitch \
        $RPM_BUILD_ROOT/%{_sysconfdir}/logrotate.d/openvswitch

install -m 0644 vswitchd/vswitch.ovsschema \
        $RPM_BUILD_ROOT/%{_datadir}/openvswitch/vswitch.ovsschema

install -d -m 0755 $RPM_BUILD_ROOT%{python3_sitelib}
cp -a $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/* \
   $RPM_BUILD_ROOT%{python3_sitelib}

rm -rf $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/

install -d -m 0755 $RPM_BUILD_ROOT/%{_sharedstatedir}/openvswitch

touch $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch/system-id.conf

install -d $RPM_BUILD_ROOT%{_prefix}/lib/firewalld/services/

install -p -D -m 0755 \
        rhel/usr_share_openvswitch_scripts_ovs-systemd-reload \
        $RPM_BUILD_ROOT%{_datadir}/openvswitch/scripts/ovs-systemd-reload

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/ovs-parse-backtrace

%check
%if %{with check}
    touch resolv.conf
    export OVS_RESOLV_CONF=$(pwd)/resolv.conf
    if make check TESTSUITEFLAGS='%{_smp_mflags}' RECHECK=yes; then :;
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

%clean
rm -rf $RPM_BUILD_ROOT

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
%sysusers_create_compat %{SOURCE1}
exit 0

%post
%if %{with libcapng}
if [ $1 -eq 1 ]; then
%if %{with dpdk}
    %define gname hugetlbfs
%else
    %define gname openvswitch
%endif
    sed -i \
        's@^#OVS_USER_ID="openvswitch:openvswitch"@OVS_USER_ID="openvswitch:%{gname}"@'\
        %{_sysconfdir}/sysconfig/openvswitch
    sed -i 's:\(.*su\).*:\1 openvswitch %{gname}:' %{_sysconfdir}/logrotate.d/openvswitch

    # In the case of upgrade, this is not needed
    chown -R openvswitch:openvswitch %{_sysconfdir}/openvswitch
    chown -R openvswitch:%{gname} %{_localstatedir}/log/openvswitch
fi
%endif

# Ensure that /etc/openvswitch/conf.db links to /var/lib/openvswitch,
# moving an existing file if there is one.
#
# Ditto for .conf.db.~lock~.
for base in conf.db .conf.db.~lock~; do
    new=/var/lib/openvswitch/$base
    old=/etc/openvswitch/$base
    if test -f $old && test ! -e $new; then
        mv $old $new
    fi
    if test ! -e $old && test ! -h $old; then
        ln -s $new $old
    fi
done

%if 0%{?systemd_post:1}
    # This may not enable openvswitch service or do daemon-reload.
    %systemd_post %{name}.service
%else
    # Package install, not upgrade
    if [ $1 -eq 1 ]; then
        /bin/systemctl daemon-reload >/dev/null || :
    fi
%endif

%postun
%if 0%{?systemd_postun:1}
    %systemd_postun %{name}.service
%else
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
%endif

%files -n python3-openvswitch
%{python3_sitelib}/ovs

%files test
%{_bindir}/ovs-test
%{_bindir}/ovs-vlan-test
%{_bindir}/ovs-l3ping
%{_bindir}/ovs-pcap
%{_bindir}/ovs-tcpdump
%{_bindir}/ovs-tcpundump
%{_datadir}/openvswitch/scripts/usdt/*
%{_mandir}/man8/ovs-test.8*
%{_mandir}/man8/ovs-vlan-test.8*
%{_mandir}/man8/ovs-l3ping.8*
%{_mandir}/man1/ovs-pcap.1*
%{_mandir}/man8/ovs-tcpdump.8*
%{_mandir}/man1/ovs-tcpundump.1*
%{python3_sitelib}/ovstest

%files devel
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/openvswitch/*
%{_includedir}/openflow/*
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.a

%files ipsec
%{_datadir}/openvswitch/scripts/ovs-monitor-ipsec
%{_unitdir}/openvswitch-ipsec.service

%files
%if %{with libcapng}
%defattr(-,openvswitch,openvswitch)
%else
%defattr(-,root,root)
%endif
%dir %{_sysconfdir}/openvswitch
%{_sysconfdir}/openvswitch/default.conf
%{_sysconfdir}/openvswitch/ovs-exporter.conf
%config %ghost %{_sharedstatedir}/openvswitch/conf.db
%ghost %{_sharedstatedir}/openvswitch/.conf.db.~lock~
%config %ghost %{_sysconfdir}/openvswitch/system-id.conf
%config(noreplace) %{_sysconfdir}/sysconfig/openvswitch
%defattr(-,root,root)
%{_sysconfdir}/bash_completion.d/ovs-appctl-bashcomp.bash
%{_sysconfdir}/bash_completion.d/ovs-vsctl-bashcomp.bash
%config(noreplace) %{_sysconfdir}/logrotate.d/openvswitch
%{_unitdir}/openvswitch.service
%{_unitdir}/ovsdb-server.service
%{_unitdir}/ovs-vswitchd.service
%{_unitdir}/ovs-exporter.service
%{_unitdir}/ovs-delete-transient-ports.service
%{_datadir}/openvswitch/scripts/openvswitch.init
%{_datadir}/openvswitch/bugtool-plugins/
%{_datadir}/openvswitch/scripts/ovs-bugtool-*
%{_datadir}/openvswitch/scripts/ovs-check-dead-ifs
%{_datadir}/openvswitch/scripts/ovs-lib
%{_datadir}/openvswitch/scripts/ovs-save
%{_datadir}/openvswitch/scripts/ovs-vtep
%{_datadir}/openvswitch/scripts/ovs-ctl
%{_datadir}/openvswitch/scripts/ovs-kmod-ctl
%{_datadir}/openvswitch/scripts/ovs-systemd-reload
%config %{_datadir}/openvswitch/local-config.ovsschema
%config %{_datadir}/openvswitch/vswitch.ovsschema
%config %{_datadir}/openvswitch/vtep.ovsschema
%{_bindir}/ovs-appctl
%{_bindir}/ovs-docker
%{_bindir}/ovs-dpctl
%{_bindir}/ovs-dpctl-top
%{_bindir}/ovs-metrics
%{_bindir}/ovs-exporter
%{_bindir}/ovs-ofctl
%{_bindir}/ovs-vsctl
%{_bindir}/ovsdb-client
%{_bindir}/ovsdb-tool
%{_bindir}/ovs-testcontroller
%{_bindir}/ovs-pki
%{_bindir}/vtep-ctl
%{_libdir}/lib*.so.*
%{_sbindir}/ovs-bugtool
%{_sbindir}/ovs-vswitchd
%{_sbindir}/ovsdb-server
%{_mandir}/man1/ovsdb-client.1*
%{_mandir}/man1/ovsdb-server.1*
%{_mandir}/man1/ovsdb-tool.1*
%{_mandir}/man5/ovsdb-server.5*
%{_mandir}/man5/ovsdb.local-config.5*
%{_mandir}/man5/ovs-vswitchd.conf.db.5*
%{_mandir}/man5/ovsdb.5*
%{_mandir}/man5/vtep.5*
%{_mandir}/man7/ovs-actions.7*
%{_mandir}/man7/ovs-fields.7*
%{_mandir}/man7/ovsdb.7*
%{_mandir}/man7/ovsdb-server.7*
%{_mandir}/man8/vtep-ctl.8*
%{_mandir}/man8/ovs-appctl.8*
%{_mandir}/man8/ovs-bugtool.8*
%{_mandir}/man8/ovs-ctl.8*
%{_mandir}/man8/ovs-dpctl.8*
%{_mandir}/man8/ovs-dpctl-top.8*
%{_mandir}/man8/ovs-kmod-ctl.8*
%{_mandir}/man8/ovs-metrics.8*
%{_mandir}/man8/ovs-exporter.8*
%{_mandir}/man8/ovs-ofctl.8*
%{_mandir}/man8/ovs-pki.8*
%{_mandir}/man8/ovs-vsctl.8*
%{_mandir}/man8/ovs-vswitchd.8*
%{_mandir}/man8/ovs-parse-backtrace.8*
%{_mandir}/man8/ovs-testcontroller.8*
%if %{with dpdk}
%{_prefix}/lib/udev/rules.d/91-vfio.rules
%endif
%doc NOTICE README.rst NEWS rhel/README.RHEL.rst
%if %{with dpdk}
%attr(750,openvswitch,hugetlbfs) /var/lib/openvswitch
%else
%attr(750,openvswitch,openvswitch) /var/lib/openvswitch
%endif
%attr(750,root,root) /var/log/openvswitch
%ghost %attr(755,root,root) %{_rundir}/openvswitch
%ghost %attr(644,root,root) %{_rundir}/openvswitch.useropts
%{_sysusersdir}/openvswitch.conf

%changelog
* Mon May 11 2026 Azure Linux Team - 3.3.0040-1
- Upgrade to DOCA 3.3.0 (OFED 26.01-1.0.0.0)

* Fri May 15 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 3.3.0-3
- Patch for CVE-2026-34956

* Thu Jan 08 2026 Tobias Brick <tobiasb@microsoft.com> - 3.3.0-2
- Add patches from fedora f40 to fix tests with new versions of openssl and python.
- Update to use correct locations for license files.

* Wed Feb 21 2024 Thien Trung Vuong <tvuong@microsoft.com> - 3.3.0-1
- Update to version 3.3.0

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 2.17.5-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Tue May 02 2023 Rakshaa Viswanathan <rviswanathan@microsoft.com> - 2.17.5-2
- Add patch to fix CVE-2023-1668

* Tue Jan 17 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.17.5-1
- Auto-upgrade to 2.17.5 - to fix CVE-2022-4337, CVE-2022-4338

* Wed Mar 23 2022 Jon Slobodzian <joslobo@microsoft.com> - 2.17.0-1
- Upgrade to latest version of openvswitch.  Remove python2 support
- Portions of this SPEC file were imported from OpenVswitch.org's autogenerated openvswitch-fedora spec.

* Mon Apr 19 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.12.3-2
- Don't include static libraries in openvswitch package

* Thu Apr 01 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.12.3-1
- Upgrade to version 2.12.3, which fixes CVE-2020-27827

* Mon Feb 22 2021 Emre Girgin <mrgirgin@microsoft.com> - 2.12.0-3
- Fix CVE-2020-35498.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.12.0-2
- Added %%license line automatically

* Tue Mar 31 2020 Henry Beberman <henry.beberman@microsoft.com> 2.12.0-1
- Update to 2.12.0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.8.2-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 13 2018 Anish Swaminathan <anishs@vmware.com> 2.8.2-3
- Replace with configure macro

* Wed Feb 28 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-2
- Setup the default conf file for local ovsdb server.

* Tue Feb 27 2018 Vinay Kulkarni <kulkarniv@vmware.com> 2.8.2-1
- Update to OVS 2.8.2

* Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-9
- Fix CVE-2017-14970

* Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.7.0-8
- Fix CVE-2017-9263

* Tue Sep 19 2017 Anish Swaminathan <anishs@vmware.com> 2.7.0-7
- Add gawk to Requires

* Tue Aug 29 2017 Sarah Choi <sarahc@vmware.com> 2.7.0-6
- Add python2/python-six/python-xml to Requires

* Thu Jul 13 2017 Nishant Nelogal <nnelogal@vmware.com> 2.7.0-5
- Created OVN packages and systemd service scripts

* Fri Jun 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-4
- Fix CVE-2017-9214, CVE-2017-9265

* Mon Jun 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.7.0-3
- Fix CVE-2017-9264

* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> 2.7.0-2
- Added python and python3 subpackage.

* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.7.0-1
- Update to 2.7.0

* Fri Feb 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-2
- Build ovs shared library

* Wed Nov 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.6.1-1
- Update to openvswitch 2.6.1

* Sat Sep 24 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.5.0-1
- Update to openvswitch 2.5.0

* Fri Sep 09 2016 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.1-1
- Update to openvswitch 2.4.1

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.0-3
- GA - Bump release of all rpms

* Sat Oct 31 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-2
- OVS requires libatomic.so.1 provided by gcc.

* Mon Oct 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.0-1
- Update to OVS v2.4.0

* Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> 2.3.1-1
- Initial build. First version
