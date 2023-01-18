%{!?python2_sitelib: %global python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%define maj_min_version %(echo %{version} | cut -d. -f1-2)

Summary:        Open vSwitch daemon/database/utilities
Name:           openvswitch
Version:        2.15.7
Release:        1%{?dist}
License:        ASL 2.0 AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Daemons
URL:            https://www.openvswitch.org/
Source0:        https://www.openvswitch.org/releases/%{name}-%{version}.tar.gz
BuildRequires:  gcc >= 4.0.0
BuildRequires:  libcap-ng
BuildRequires:  libcap-ng-devel
BuildRequires:  make
BuildRequires:  openssl
BuildRequires:  openssl-devel
BuildRequires:  python-pip
BuildRequires:  python-setuptools
BuildRequires:  python-six
BuildRequires:  python-xml
BuildRequires:  python2 >= 2.7.0
BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python3 >= 3.4.0
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-six
BuildRequires:  python3-xml
BuildRequires:  systemd
Requires:       gawk
Requires:       libcap-ng
Requires:       libgcc-atomic
Requires:       openssl
Requires:       python-six
Requires:       python-xml
Requires:       python2
Requires:       python2-libs
Requires:       python3-xml

%description
Open vSwitch provides standard network bridging functions and
support for the OpenFlow protocol for remote per-flow control of
traffic.

%package -n     python-openvswitch
Summary:        python-openvswitch
Requires:       python2
Requires:       python2-libs

%description -n python-openvswitch
Python 2 openvswith bindings.

%package -n     python3-openvswitch
Summary:        python3-openvswitch
Requires:       python3
Requires:       python3-libs

%description -n python3-openvswitch
Python 3 version.

%package        devel
Summary:        Header and development files for openvswitch
Requires:       %{name} = %{version}

%description    devel
openvswitch-devel package contains header files and libs.

%package        devel-static
Summary:        Static libs for openvswitch
Requires:       %{name} = %{version}

%description    devel-static
openvswitch-devel-static package contains static libs.

%package        doc
Summary:        Documentation for openvswitch
Requires:       %{name} = %{version}-%{release}

%description    doc
It contains the documentation and manpages for openvswitch.

%prep
%autosetup -p1

%build
%configure --enable-ssl --enable-shared

%make_build

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete -print
mkdir -p %{buildroot}/%{python2_sitelib}
mkdir -p %{buildroot}/%{python3_sitelib}
cp -a %{buildroot}/%{_datadir}/openvswitch/python/ovs/* %{buildroot}/%{python2_sitelib}

cp -a %{buildroot}/%{_datadir}/openvswitch/python/ovs/* %{buildroot}/%{python3_sitelib}

mkdir -p %{buildroot}/%{_libdir}/systemd/system
install -p -D -m 0644 rhel/usr_share_openvswitch_scripts_systemd_sysconfig.template %{buildroot}/%{_sysconfdir}/sysconfig/openvswitch

%{_bindir}/python build-aux/dpdkstrip.py --nodpdk < rhel/usr_lib_systemd_system_ovs-vswitchd.service.in > rhel/usr_lib_systemd_system_ovs-vswitchd.service
for service in openvswitch ovsdb-server ovs-vswitchd; do
	install -p -D -m 0644 rhel/usr_lib_systemd_system_${service}.service %{buildroot}/%{_unitdir}/${service}.service
done

mkdir -p %{buildroot}/%{_sysconfdir}/openvswitch
install -p -D -m 0644 rhel/etc_openvswitch_default.conf %{buildroot}/%{_sysconfdir}/openvswitch/default.conf
sed -i '/OVS_USER_ID=.*/c\OVS_USER_ID=' %{buildroot}/%{_sysconfdir}/openvswitch/default.conf

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%preun
%systemd_preun %{name}.service

%post
%systemd_post %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/ovs-*
%{_bindir}/ovsdb-*
%{_bindir}/vtep-ctl
%{_sbindir}/ovs-*
%{_sbindir}/ovsdb-server
%{_unitdir}/openvswitch.service
%{_unitdir}/ovs-vswitchd.service
%{_unitdir}/ovsdb-server.service
%{_libdir}/libopenvswitch.so
%{_libdir}/libopenvswitch-%{maj_min_version}.so.0*
%{_libdir}/libofproto.so
%{_libdir}/libofproto-%{maj_min_version}.so.0*
%{_libdir}/libvtep.so
%{_libdir}/libvtep-%{maj_min_version}.so.0*
%{_libdir}/libovsdb.so
%{_libdir}/libovsdb-%{maj_min_version}.so.0*
%{_libdir}/libsflow.so
%{_libdir}/libsflow-%{maj_min_version}.so.0*
%{_sysconfdir}/openvswitch/default.conf
%{_sysconfdir}/bash_completion.d/ovs-*-bashcomp.bash
%{_datadir}/openvswitch/*.ovsschema
%{_datadir}/openvswitch/bugtool-plugins/*
%{_datadir}/openvswitch/python/*
%{_datadir}/openvswitch/scripts/ovs-*
%config(noreplace) %{_sysconfdir}/sysconfig/openvswitch

%files -n python-openvswitch
%{python2_sitelib}/*

%files -n python3-openvswitch
%{python3_sitelib}/*

%files devel
%{_includedir}/openflow/*.h
%{_includedir}/openvswitch/*.h
%{_libdir}/pkgconfig/*.pc

%files devel-static
%{_libdir}/*.a

%files doc
%{_mandir}/man1/ovs-*.1.gz
%{_mandir}/man1/ovsdb-*.1.gz
%{_mandir}/man5/ovs-vswitchd.conf.db.5.gz
%{_mandir}/man5/ovsdb-server.5.gz
%{_mandir}/man5/vtep.5.gz
%{_mandir}/man7/ovs-actions.7.gz
%{_mandir}/man7/ovs-fields.7.gz
%{_mandir}/man8/ovs-*.8.gz
%{_mandir}/man8/vtep-ctl.8.gz

%changelog
* Tue Jan 17 2023 Andrew Phelps <anphel@microsoft.com> - 2.15.7-1
- Upgrade to 2.15.7 to fix CVE-2022-4338, CVE-2022-4337
- Remove unneeded patch CVE-2021-3905.patch

* Thu Sep 01 2022 Minghe Ren <mingheren@microsoft.com> - 2.15.1-2
- Add patch to fix CVE-2021-3905

* Wed Aug 11 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.15.1-1
- Updating to version 2.15.1 to fix CVE-2021-36980.
- Removing no longer present OVN components and subpackages:
	- ovn-central;
	- ovn-common;
	- ovn-controller-vtep;
	- ovn-doc;
	- ovn-docker;
	- ovn-host;
	- ovn-northd.
- Updating source URL to use HTTPS.

* Mon Apr 19 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.12.3-2
- Don't include static libraries in openvswitch package

* Thu Apr 01 2021 Nicolas Ontiveros <niontive@microsoft.com> - 2.12.3-1
- Upgrade to version 2.12.3, which fixes CVE-2020-27827

* Mon Feb 22 2021 Emre Girgin <mrgirgin@microsoft.com> - 2.12.0-3
- Fix CVE-2020-35498.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.12.0-2
- Added %%license line automatically

* Tue Mar 31 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.12.0-1
- Update to 2.12.0. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.8.2-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Nov 13 2018 Anish Swaminathan <anishs@vmware.com> - 2.8.2-3
- Replace with configure macro

* Wed Feb 28 2018 Vinay Kulkarni <kulkarniv@vmware.com> - 2.8.2-2
- Setup the default conf file for local ovsdb server.

* Tue Feb 27 2018 Vinay Kulkarni <kulkarniv@vmware.com> - 2.8.2-1
- Update to OVS 2.8.2

* Tue Oct 10 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.7.0-9
- Fix CVE-2017-14970

* Wed Oct 04 2017 Dheeraj Shetty <dheerajs@vmware.com> - 2.7.0-8
- Fix CVE-2017-9263

* Tue Sep 19 2017 Anish Swaminathan <anishs@vmware.com> - 2.7.0-7
- Add gawk to Requires

* Tue Aug 29 2017 Sarah Choi <sarahc@vmware.com> - 2.7.0-6
- Add python2/python-six/python-xml to Requires

* Thu Jul 13 2017 Nishant Nelogal <nnelogal@vmware.com> - 2.7.0-5
- Created OVN packages and systemd service scripts

* Fri Jun 16 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 2.7.0-4
- Fix CVE-2017-9214, CVE-2017-9265

* Mon Jun 12 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 2.7.0-3
- Fix CVE-2017-9264

* Tue May 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.7.0-2
- Added python and python3 subpackage.

* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.7.0-1
- Update to 2.7.0

* Fri Feb 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> - 2.6.1-2
- Build ovs shared library

* Wed Nov 16 2016 Vinay Kulkarni <kulkarniv@vmware.com> - 2.6.1-1
- Update to openvswitch 2.6.1

* Sat Sep 24 2016 Vinay Kulkarni <kulkarniv@vmware.com> - 2.5.0-1
- Update to openvswitch 2.5.0

* Fri Sep 09 2016 Vinay Kulkarni <kulkarniv@vmware.com> - 2.4.1-1
- Update to openvswitch 2.4.1

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.4.0-3
- GA - Bump release of all rpms

* Sat Oct 31 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 2.4.0-2
- OVS requires libatomic.so.1 provided by gcc.

* Mon Oct 12 2015 Vinay Kulkarni <kulkarniv@vmware.com> - 2.4.0-1
- Update to OVS v2.4.0

* Fri May 29 2015 Kumar Kaushik <kaushikk@vmware.com> - 2.3.1-1
- Initial build. First version
