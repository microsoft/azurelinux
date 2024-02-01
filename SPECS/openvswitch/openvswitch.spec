# Copyright (C) 2009, 2010, 2013, 2014, 2015, 2016 Nicira Networks, Inc.
#
# Copying and distribution of this file, with or without modification,
# are permitted in any medium without royalty provided the copyright
# notice and this notice are preserved.  This file is offered as-is,
# without warranty of any kind.

Summary:           Open vSwitch daemon/database/utilities
Name:              openvswitch
Version:           3.2.1
Release:           1%{?dist}
License:           ASL 2.0 AND LGPLv2+ AND SISSL
Vendor:            Microsoft Corporation
Distribution:      Mariner
Group:             System Environment/Daemons
URL:               https://www.openvswitch.org/
Source0:           http://openvswitch.org/releases/%{name}-%{version}.tar.gz
BuildRequires:     autoconf
BuildRequires:     automake
BuildRequires:     checkpolicy
BuildRequires:     dpdk-devel
BuildRequires:     gcc >= 4.0.0
BuildRequires:     graphviz
BuildRequires:     groff
BuildRequires:     libcap-ng
BuildRequires:     libcap-ng-devel
BuildRequires:     libpcap-devel
BuildRequires:     libtool
BuildRequires:     make
BuildRequires:     numactl-devel
BuildRequires:     openssl
BuildRequires:     openssl-devel
BuildRequires:     procps-ng
BuildRequires:     python3
BuildRequires:     python3-devel
BuildRequires:     python3-libs
BuildRequires:     python3-six
BuildRequires:     python3-sphinx
BuildRequires:     selinux-policy-devel
BuildRequires:     systemd
BuildRequires:     unbound
BuildRequires:     unbound-devel
Requires:          hostname
Requires:          iproute
Requires:          module-init-tools
Requires:          openssl
Requires:          unbound
Requires(pre):     shadow-utils
Requires(post):    /bin/sed
Requires(post):    systemd-units
Requires(preun):   systemd-units
Requires(postun):  systemd-units


%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package        selinux-policy
Summary:        Open vSwitch SELinux policy
License:        ASL 2.0
Requires:       selinux-policy
BuildArch:      noarch

%description    selinux-policy
Open vSwitch SELinux policy

%package -n     python3-openvswitch
Summary:        Python3 bindings for Open vSwitch
License:        ASL 2.0
Requires:       python3
Requires:       python3-libs
BuildArch:      noarch

%description -n python3-openvswitch
Python binding for Open vSwitch database 

%package        devel
Summary:        Header and development files for openvswitch
License:        ASL 2.0
Requires:       %{name} = %{version}

%description    devel
openvswitch-devel package contains header files and libs.

%package        test
Summary: Open vSwitch testing utilities
License:        ASL 2.0
BuildArch: noarch

%description    test
Utilities that are useful to diagnose performance and connectivity
issues in Open vSwitch setup.

%package        doc
Summary:        Documentation for openvswitch
License:        ASL 2.0
Requires:       %{name} = %{version}-%{release}

%description    doc
It contains the documentation and manpages for openvswitch.

%package        ipsec
Summary:        Open vSwitch IPsec tunneling support
License:        ASL 2.0
Requires:       openvswitch 
Requires:       python3-openvswitch 
Requires:       strongswan

%description    ipsec
This package provides IPsec tunneling support for OVS tunnels.

%prep
%autosetup -p1

%build
%configure \
           --enable-ssl         \
           --enable-shared      \
           --disable-static     \
           --with-dpdk=shared   \
           --enable-libcapng    \
           --with-pkidir=%{_sharedstatedir}/openvswitch/pki \
           PYTHON3=%{__python3}

build-aux/dpdkstrip.py \
           --dpdk      \
           < rhel/usr_lib_systemd_system_ovs-vswitchd.service.in \
           > rhel/usr_lib_systemd_system_ovs-vswitchd.service

make %{_smp_mflags}
make selinux-policy

%install
make install DESTDIR=$RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT%{_rundir}/openvswitch
install -d -m 0750 $RPM_BUILD_ROOT%{_localstatedir}/log/openvswitch
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch
copy_headers() {
    src=$1
    dst=$RPM_BUILD_ROOT/$2
    install -d -m 0755 $dst
    install -m 0644 $src/*.h $dst
}
copy_headers include %{_includedir}/openvswitch
copy_headers include/openflow %{_includedir}/openvswitch/openflow
copy_headers include/openvswitch %{_includedir}/openvswitch/openvswitch
copy_headers include/sparse %{_includedir}/openvswitch/sparse
copy_headers include/sparse/arpa %{_includedir}/openvswitch/sparse/arpa
copy_headers include/sparse/netinet %{_includedir}/openvswitch/sparse/netinet
copy_headers include/sparse/sys %{_includedir}/openvswitch/sparse/sys
copy_headers lib %{_includedir}/openvswitch/lib


install -p -D -m 0644 rhel/usr_lib_udev_rules.d_91-vfio.rules \
        $RPM_BUILD_ROOT%{_prefix}/lib/udev/rules.d/91-vfio.rules

install -p -D -m 0644 \
        rhel/usr_share_openvswitch_scripts_systemd_sysconfig.template \
        $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/openvswitch


for service in openvswitch ovsdb-server ovs-vswitchd ovs-delete-transient-ports openvswitch-ipsec; do
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
cp -a $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/* \
   $RPM_BUILD_ROOT%{python3_sitelib}

rm -rf $RPM_BUILD_ROOT/%{_datadir}/openvswitch/python/

install -d -m 0755 $RPM_BUILD_ROOT/%{_sharedstatedir}/openvswitch

touch $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch/conf.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch/.conf.db.~lock~
touch $RPM_BUILD_ROOT%{_sysconfdir}/openvswitch/system-id.conf

install -p -m 644 -D selinux/openvswitch-custom.pp \
        $RPM_BUILD_ROOT%{_datadir}/selinux/packages/%{name}/openvswitch-custom.pp

install -d $RPM_BUILD_ROOT%{_prefix}/lib/firewalld/services/

install -p -D -m 0755 \
        rhel/usr_share_openvswitch_scripts_ovs-systemd-reload \
        $RPM_BUILD_ROOT%{_datadir}/openvswitch/scripts/ovs-systemd-reload

# remove unpackaged files
rm -f $RPM_BUILD_ROOT%{_bindir}/ovs-parse-backtrace

%check
touch resolv.conf
export OVS_RESOLV_CONF=$(pwd)/resolv.conf
make -k check TESTSUITEFLAGS='%{_smp_mflags}' RECHECK=yes |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%pre selinux-policy
%selinux_relabel_pre -s targeted

%preun
%systemd_preun %{name}.service

%pre
getent group openvswitch >/dev/null || groupadd -r openvswitch
getent passwd openvswitch >/dev/null || \
    useradd -r -g openvswitch -d / -s /sbin/nologin \
    -c "Open vSwitch Daemons" openvswitch

getent group hugetlbfs >/dev/null || groupadd -r hugetlbfs
usermod -a -G hugetlbfs openvswitch

exit 0

%post
if [ $1 -eq 1 ]; then
    %define gname hugetlbfs
    sed -i \
        's@^#OVS_USER_ID="openvswitch:openvswitch"@OVS_USER_ID="openvswitch:%{gname}"@'\
        %{_sysconfdir}/sysconfig/openvswitch
    sed -i 's:\(.*su\).*:\1 openvswitch %{gname}:' %{_sysconfdir}/logrotate.d/openvswitch

    # In the case of upgrade, this is not needed
    chown -R openvswitch:openvswitch %{_sysconfdir}/openvswitch
    chown -R openvswitch:%{gname} %{_localstatedir}/log/openvswitch
fi

# This may not enable openvswitch service or do daemon-reload.
%systemd_post %{name}.service

%post selinux-policy
%selinux_modules_install -s targeted %{_datadir}/selinux/packages/%{name}/openvswitch-custom.pp

%postun
%systemd_postun %{name}.service

%postun selinux-policy
if [ $1 -eq 0 ] ; then
  %selinux_modules_uninstall -s targeted openvswitch-custom
fi

%posttrans selinux-policy
%selinux_relabel_post -s targeted

%files selinux-policy
%defattr(-,root,root)
%{_datadir}/selinux/packages/%{name}/openvswitch-custom.pp

%files -n python3-openvswitch
%{python3_sitelib}/ovs

%files test
%{_bindir}/ovs-test
%{_bindir}/ovs-vlan-test
%{_bindir}/ovs-l3ping
%{_bindir}/ovs-pcap
%{_bindir}/ovs-tcpdump
%{_bindir}/ovs-tcpundump
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

%files doc
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
%{_mandir}/man8/ovs-ofctl.8*
%{_mandir}/man8/ovs-pki.8*
%{_mandir}/man8/ovs-vsctl.8*
%{_mandir}/man8/ovs-vswitchd.8*
%{_mandir}/man8/ovs-parse-backtrace.8*
%{_mandir}/man8/ovs-testcontroller.8*


%files
%defattr(-,openvswitch,openvswitch)
%dir %{_sysconfdir}/openvswitch
%{_sysconfdir}/openvswitch/default.conf
%config %ghost %{_sysconfdir}/openvswitch/conf.db
%ghost %{_sysconfdir}/openvswitch/.conf.db.~lock~
%config %ghost %{_sysconfdir}/openvswitch/system-id.conf
%config(noreplace) %{_sysconfdir}/sysconfig/openvswitch
%defattr(-,root,root)
%license LICENSE
%{_sysconfdir}/bash_completion.d/ovs-appctl-bashcomp.bash
%{_sysconfdir}/bash_completion.d/ovs-vsctl-bashcomp.bash
%config(noreplace) %{_sysconfdir}/logrotate.d/openvswitch
%{_unitdir}/openvswitch.service
%{_unitdir}/ovsdb-server.service
%{_unitdir}/ovs-vswitchd.service
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
%{_prefix}/lib/udev/rules.d/91-vfio.rules
%doc NOTICE README.rst NEWS rhel/README.RHEL.rst
/var/lib/openvswitch
%attr(750,root,root) /var/log/openvswitch
%ghost %attr(755,root,root) %{_rundir}/openvswitch
%ghost %attr(644,root,root) %{_rundir}/openvswitch.useropts




%files ipsec
%{_datadir}/openvswitch/scripts/ovs-monitor-ipsec
%{_unitdir}/openvswitch-ipsec.service

%changelog
* Thu Feb 01 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 3.2.1-1
- Auto-upgrade to 3.2.1 - Package upgrade for Azure Linux 3.0

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
