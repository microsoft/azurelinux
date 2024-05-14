# To disable DPDK support, specify '--without dpdk' when building
%bcond_without dpdk

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

Summary:           Open vSwitch daemon/database/utilities
Name:              openvswitch
Version:           3.3.0
Release:           1%{?dist}
License:           ASL 2.0 AND LGPLv2+ AND SISSL
Vendor:            Microsoft Corporation
Distribution:      Azure Linux
Group:             System Environment/Daemons
URL:               https://www.openvswitch.org/
Source0:           https://openvswitch.org/releases/%{name}-%{version}.tar.gz
Source1:           openvswitch.sysusers

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
BuildRequires: groff
BuildRequires: python3-pyOpenSSL

%if %{with check_datapath_kernel}
BuildRequires: nmap-ncat
%endif

%if %{with libcapng}
BuildRequires: libcap-ng libcap-ng-devel
%endif

%if %{with dpdk}
BuildRequires: dpdk-devel libpcap-devel numactl-devel
%endif

Requires: openssl
Requires: iproute
Requires: module-init-tools

%{?systemd_requires}
%{?sysusers_requires_compat}

Requires(post): /bin/sed
Requires(post): %{_sbindir}/update-alternatives
Requires(postun): %{_sbindir}/update-alternatives

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for the remote per-flow control of
traffic.

%package -n python3-openvswitch
Summary: Open vSwitch python3 bindings
License: ASL 2.0
Requires: python3 python3-six
Provides: python-openvswitch = %{version}-%{release}

%description -n python3-openvswitch
Python bindings for the OpenvSwitch database

%package test
Summary: Open vSwitch testing utilities
License: ASL 2.0
BuildArch: noarch
Requires: python3-openvswitch = %{version}-%{release}

%description test
Utilities that are useful to diagnose performance and connectivity
issues in Open vSwitch setup.

%package testcontroller
Summary: Simple controller for testing OpenFlow setups
License: ASL 2.0
Requires: openvswitch = %{version}-%{release}

%description testcontroller
This controller enables OpenFlow switches that connect to it to act as
MAC-learning Ethernet switches.
It can be used for initial testing of OpenFlow networks.
It is not a necessary or desirable part of a production OpenFlow deployment.

%package devel
Summary: Open vSwitch OpenFlow development package (library, headers)
License: ASL 2.0

%description devel
This provides shared library, libopenswitch.so and the openvswitch header
files needed to build an external application.

%package ipsec
Summary: Open vSwitch IPsec tunneling support
License: ASL 2.0
Requires: openvswitch libreswan
Requires: python3-openvswitch = %{version}-%{release}

%description ipsec
This package provides IPsec tunneling support for OVS tunnels.

%if %{with dpdk}
%package dpdk
Summary: Open vSwitch OpenFlow development package (switch, linked with DPDK)
License: ASL 2.0
Supplements: %{name}

%description dpdk
This provides ovs-vswitchd linked with DPDK library.
%endif

%prep
%autosetup -p1

%build
# BZ#2055576
rm -f python/ovs/dirs.py

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
%if %{with afxdp}
        --enable-afxdp
%else
        --disable-afxdp
%endif
make %{?_smp_mflags}
popd
%if %{with dpdk}
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
%if %{with afxdp}
        --enable-afxdp
%else
        --disable-afxdp
%endif
make %{?_smp_mflags}
popd
%endif

/usr/bin/python3 build-aux/dpdkstrip.py \
        --dpdk \
        < rhel/usr_lib_systemd_system_ovs-vswitchd.service.in \
        > rhel/usr_lib_systemd_system_ovs-vswitchd.service

%install
rm -rf $RPM_BUILD_ROOT

%if %{with dpdk}
make -C build-dpdk install-exec DESTDIR=$RPM_BUILD_ROOT

# We only need ovs-vswitchd-dpdk and some libraries for dpdk subpackage
rm -rf $RPM_BUILD_ROOT%{_bindir}
find $RPM_BUILD_ROOT%{_sbindir} -mindepth 1 -maxdepth 1 -not -name ovs-vswitchd.dpdk -delete
find $RPM_BUILD_ROOT%{_libdir}/openvswitch-dpdk -mindepth 1 -maxdepth 1 -not -name "libofproto*.so.*" -not -name "libopenvswitch*.so.*" -delete
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

install -d -m 0755 $RPM_BUILD_ROOT%{python3_sitelib}
cp -a $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/ovstest \
        $RPM_BUILD_ROOT%{python3_sitelib}

# Build the JSON C extension for the Python lib (#1417738)
pushd python
(
export CPPFLAGS="-I ../include"
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
for dir in build \
%if %{with dpdk}
build-dpdk \
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
%sysusers_create_compat %{SOURCE1}
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
%{_libdir}/*.la
%{_includedir}/openvswitch/*
%{_includedir}/openflow/*
%exclude %{_libdir}/*.a

%files ipsec
%{_datadir}/openvswitch/scripts/ovs-monitor-ipsec
%{_unitdir}/openvswitch-ipsec.service

%if %{with dpdk}
%files dpdk
%{_libdir}/openvswitch-dpdk/
%ghost %{_sbindir}/ovs-vswitchd
%{_sbindir}/ovs-vswitchd.dpdk
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
%{_sysusersdir}/openvswitch.conf

%changelog
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
