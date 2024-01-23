Summary:        RDMA core userspace libraries and daemons
Name:           rdma-core
Version:        49.0
Release:        1%{?dist}
URL:            https://github.com/linux-rdma/rdma-core
Vendor:         Microsoft Corporation
Distribution:   Mariner

# Almost everything is licensed under the OFA dual GPLv2, 2 Clause BSD license
#  providers/ipathverbs/ Dual licensed using a BSD license with an extra patent clause
#  providers/rxe/ Incorporates code from ipathverbs and contains the patent clause
#  providers/hfi1verbs Uses the 3 Clause BSD license
License: GPLv2 or BSD
Source0: https://github.com/linux-rdma/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch1: 0001-kernel-boot-Do-not-perform-device-rename-on-OPA-devi.patch

# Do not build static libs by default.
%define with_static %{?_with_static: 1} %{?!_with_static: 0}

# 32-bit arm is missing required arch-specific memory barriers,
ExcludeArch: %{arm}

%global azl3 1
BuildRequires: binutils
BuildRequires: cmake >= 2.8.11
BuildRequires: gcc
BuildRequires: pkg-config
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
# Disable pyverbs for azl3, as pyverbs cannot build with cython > 3
# pyverbs/device.c: error: redefinition of '__Pyx_Enum_ibv_event_type_to_py'
# and non-matching exception definitions
%if 0%{azl3}
%define with_pyverbs 0
%endif
%if %{with_pyverbs}
BuildRequires: python3-Cython
%endif
BuildRequires: python3
BuildRequires: python3-docutils
BuildRequires: python3-devel
BuildRequires: python3-xml
BuildRequires: systemd
BuildRequires: systemd-devel
BuildRequires: valgrind
Requires: pciutils

Provides: rdma = %{version}-%{release}

BuildRequires: ninja-build
%define CMAKE_FLAGS -GNinja
%define make_jobs ninja-build -C . -v %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} ninja-build -C . install

%description
RDMA core userspace infrastructure and documentation, including initialization
scripts, kernel driver-specific modprobe override configs, IPoIB network
scripts, dracut rules, and the rdma-ndd utility.

%package devel
Summary: RDMA core development libraries and headers
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}
Provides: libibverbs-devel = %{version}-%{release}
Obsoletes: libibverbs-devel < %{version}-%{release}
Requires: libibumad%{?_isa} = %{version}-%{release}
Provides: libibumad-devel = %{version}-%{release}
Obsoletes: libibumad-devel < %{version}-%{release}
Requires: librdmacm%{?_isa} = %{version}-%{release}
Provides: librdmacm-devel = %{version}-%{release}
Obsoletes: librdmacm-devel < %{version}-%{release}
Requires: ibacm%{?_isa} = %{version}-%{release}
Provides: ibacm-devel = %{version}-%{release}
Obsoletes: ibacm-devel < %{version}-%{release}
Requires: infiniband-diags%{?_isa} = %{version}-%{release}
Provides: infiniband-diags-devel = %{version}-%{release}
Obsoletes: infiniband-diags-devel < %{version}-%{release}
Provides: libibmad-devel = %{version}-%{release}
Obsoletes: libibmad-devel < %{version}-%{release}
%if %{with_static}
# Since our pkg-config files include private references to these packages they
# need to have their .pc files installed too, even for dynamic linking, or
# pkg-config breaks.
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
%endif

%description devel
RDMA core development libraries and headers.

%package -n infiniband-diags
Summary: InfiniBand Diagnostic Tools
Requires: libibumad%{?_isa} = %{version}-%{release}
Provides: perl(IBswcountlimits)
Provides: libibmad = %{version}-%{release}
Obsoletes: libibmad < %{version}-%{release}

%description -n infiniband-diags
This package provides IB diagnostic programs and scripts needed to diagnose an
IB subnet.  infiniband-diags now also provides libibmad.  libibmad provides
low layer IB functions for use by the IB diagnostic and management
programs. These include MAD, SA, SMP, and other basic IB functions.

%package -n infiniband-diags-compat
Summary: OpenFabrics Alliance InfiniBand Diagnostic Tools

%description -n infiniband-diags-compat
Deprecated scripts and utilities which provide duplicated functionality, most
often at a reduced performance. These are maintained for the time being for
compatibility reasons.

%package -n libibverbs
Summary: A library and drivers for direct userspace use of RDMA (InfiniBand/iWARP/RoCE) hardware
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: libcxgb4 = %{version}-%{release}
Obsoletes: libcxgb4 < %{version}-%{release}
Provides: libefa = %{version}-%{release}
Obsoletes: libefa < %{version}-%{release}
Provides: libhfi1 = %{version}-%{release}
Obsoletes: libhfi1 < %{version}-%{release}
Provides: libi40iw = %{version}-%{release}
Obsoletes: libi40iw < %{version}-%{release}
Provides: libipathverbs = %{version}-%{release}
Obsoletes: libipathverbs < %{version}-%{release}
Provides: libmlx4 = %{version}-%{release}
Obsoletes: libmlx4 < %{version}-%{release}
Provides: libmlx5 = %{version}-%{release}
Obsoletes: libmlx5 < %{version}-%{release}
Provides: libmthca = %{version}-%{release}
Obsoletes: libmthca < %{version}-%{release}
Provides: libocrdma = %{version}-%{release}
Obsoletes: libocrdma < %{version}-%{release}
Provides: librxe = %{version}-%{release}
Obsoletes: librxe < %{version}-%{release}

%description -n libibverbs
libibverbs is a library that allows userspace processes to use RDMA
"verbs" as described in the InfiniBand Architecture Specification and
the RDMA Protocol Verbs Specification.  This includes direct hardware
access from userspace to InfiniBand/iWARP adapters (kernel bypass) for
fast path operations.

Device-specific plug-in ibverbs userspace drivers are included:

- libcxgb4: Chelsio T4 iWARP HCA
- libefa: Amazon Elastic Fabric Adapter
- libhfi1: Intel Omni-Path HFI
- libhns: HiSilicon Hip06 SoC
- libi40iw: Intel Ethernet Connection X722 RDMA
- libipathverbs: QLogic InfiniPath HCA
- libmlx4: Mellanox ConnectX-3 InfiniBand HCA
- libmlx5: Mellanox Connect-IB/X-4+ InfiniBand HCA
- libmthca: Mellanox InfiniBand HCA
- libocrdma: Emulex OneConnect RDMA/RoCE Device
- libqedr: QLogic QL4xxx RoCE HCA
- librxe: A software implementation of the RoCE protocol
- libsiw: A software implementation of the iWarp protocol
- libvmw_pvrdma: VMware paravirtual RDMA device

%package -n libibverbs-utils
Summary: Examples for the libibverbs library
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n libibverbs-utils
Useful libibverbs example programs such as ibv_devinfo, which
displays information about RDMA devices.

%package -n ibacm
Summary: InfiniBand Communication Manager Assistant
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n ibacm
The ibacm daemon helps reduce the load of managing path record lookups on
large InfiniBand fabrics by providing a user space implementation of what
is functionally similar to an ARP cache.  The use of ibacm, when properly
configured, can reduce the SA packet load of a large IB cluster from O(n^2)
to O(n).  The ibacm daemon is started and normally runs in the background,
user applications need not know about this daemon as long as their app
uses librdmacm to handle connection bring up/tear down.  The librdmacm
library knows how to talk directly to the ibacm daemon to retrieve data.

%package -n iwpmd
Summary: iWarp Port Mapper userspace daemon
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n iwpmd
iwpmd provides a userspace service for iWarp drivers to claim
tcp ports through the standard socket interface.

%package -n libibumad
Summary: OpenFabrics Alliance InfiniBand umad (userspace management datagram) library
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n libibumad
libibumad provides the userspace management datagram (umad) library
functions, which sit on top of the umad modules in the kernel. These
are used by the IB diagnostic and management tools, including OpenSM.

%package -n librdmacm
Summary: Userspace RDMA Connection Manager
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n librdmacm
librdmacm provides a userspace RDMA Communication Management API.

%package -n librdmacm-utils
Summary: Examples for the librdmacm library
Requires: librdmacm%{?_isa} = %{version}-%{release}

%description -n librdmacm-utils
Example test programs for the librdmacm library.

%package -n srp_daemon
Summary: Tools for using the InfiniBand SRP protocol devices
Obsoletes: srptools <= 1.0.3
Provides: srptools = %{version}-%{release}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n srp_daemon
In conjunction with the kernel ib_srp driver, srp_daemon allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%if %{with_pyverbs}
%package -n python3-pyverbs
Summary: Python3 API over IB verbs
%{?python_provide:%python_provide python3-pyverbs}

%description -n python3-pyverbs
Pyverbs is a Cython-based Python API over libibverbs, providing an
easy, object-oriented access to IB verbs.
%endif

%prep
%autosetup -v -p1

%build
# This package uses top level ASM constructs which are incompatible with LTO.
# Top level ASMs are often used to implement symbol versioning.  gcc-10
# introduces a new mechanism for symbol versioning which works with LTO.
# Converting packages to use that mechanism instead of toplevel ASMs is
# recommended.
# Disable LTO
%define _lto_cflags %{nil}

# New RPM defines _rundir, usually as /run
%if 0%{?_rundir:1}
%else
%define _rundir /var/run
%endif

%{!?EXTRA_CMAKE_FLAGS: %define EXTRA_CMAKE_FLAGS %{nil}}

# Pass all of the rpm paths directly to GNUInstallDirs and our other defines.
%cmake %{CMAKE_FLAGS} \
         -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
         -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
         -DCMAKE_INSTALL_LIBDIR:PATH=%{_libdir} \
         -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
         -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
         -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
         -DCMAKE_INSTALL_INCLUDEDIR:PATH=%{_includedir} \
         -DCMAKE_INSTALL_INFODIR:PATH=%{_infodir} \
         -DCMAKE_INSTALL_MANDIR:PATH=%{_mandir} \
         -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
         -DCMAKE_INSTALL_SYSTEMD_SERVICEDIR:PATH=%{_unitdir} \
         -DCMAKE_INSTALL_INITDDIR:PATH=%{_initrddir} \
         -DCMAKE_INSTALL_RUNDIR:PATH=%{_rundir} \
         -DCMAKE_INSTALL_DOCDIR:PATH=%{_docdir}/%{name} \
         -DCMAKE_INSTALL_UDEV_RULESDIR:PATH=%{_udevrulesdir} \
         -DCMAKE_INSTALL_PERLDIR:PATH=%{perl_vendorlib} \
         -DENABLE_IBDIAGS_COMPAT:BOOL=True \
%if %{with_static}
         -DENABLE_STATIC=1 \
%endif
         %{EXTRA_CMAKE_FLAGS} \
         -DPYTHON_EXECUTABLE:PATH=%{__python3} \
         -DCMAKE_INSTALL_PYTHON_ARCH_LIB:PATH=%{python3_sitearch} \
%if %{with_pyverbs}
         -DNO_PYVERBS=0
%else
	-DNO_PYVERBS=1
%endif
%make_jobs

%install
%cmake_install

mkdir -p %{buildroot}/%{_sysconfdir}/rdma

# Red Hat specific glue
%global dracutlibdir %{_prefix}/lib/dracut
%global sysmodprobedir %{_prefix}/lib/modprobe.d
mkdir -p %{buildroot}%{_sysconfdir}/udev/rules.d
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/05rdma
mkdir -p %{buildroot}%{sysmodprobedir}
install -D -m0644 redhat/rdma.conf %{buildroot}/%{_sysconfdir}/rdma/rdma.conf
install -D -m0644 redhat/rdma.mlx4.conf %{buildroot}/%{_sysconfdir}/rdma/mlx4.conf
install -D -m0755 redhat/rdma.modules-setup.sh %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh
install -D -m0644 redhat/rdma.mlx4.sys.modprobe %{buildroot}%{sysmodprobedir}/libmlx4.conf
install -D -m0755 redhat/rdma.mlx4-setup.sh %{buildroot}%{_libexecdir}/mlx4-setup.sh

# ibacm
bin/ib_acme -D . -O
install -D -m0644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/

# Delete the package's init.d scripts
rm -rf %{buildroot}/%{_initrddir}/
rm -f %{buildroot}/%{_sbindir}/srp_daemon.sh

%post -n libibverbs -p /sbin/ldconfig
%postun -n libibverbs -p /sbin/ldconfig

%post -n libibumad -p /sbin/ldconfig
%postun -n libibumad -p /sbin/ldconfig

%post -n librdmacm -p /sbin/ldconfig
%postun -n librdmacm -p /sbin/ldconfig

%post -n rdma-core
if [ -x /sbin/udevadm ]; then
/sbin/udevadm trigger --subsystem-match=infiniband --action=change || true
/sbin/udevadm trigger --subsystem-match=net --action=change || true
/sbin/udevadm trigger --subsystem-match=infiniband_mad --action=change || true
fi

%post -n ibacm
%systemd_post ibacm.service
%preun -n ibacm
%systemd_preun ibacm.service
%postun -n ibacm
%systemd_postun_with_restart ibacm.service

%post -n srp_daemon
%systemd_post srp_daemon.service
%preun -n srp_daemon
%systemd_preun srp_daemon.service
%postun -n srp_daemon
%systemd_postun_with_restart srp_daemon.service

%post -n iwpmd
%systemd_post iwpmd.service
%preun -n iwpmd
%systemd_preun iwpmd.service
%postun -n iwpmd
%systemd_postun_with_restart iwpmd.service

%files
%license COPYING.BSD_FB COPYING.BSD_MIT COPYING.GPL2 COPYING.md 
%dir %{_sysconfdir}/rdma
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/rxe.md
%doc %{_docdir}/%{name}/udev.md
%doc %{_docdir}/%{name}/tag_matching.md
%doc %{_docdir}/%{name}/70-persistent-ipoib.rules
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/infiniband.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/iwarp.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/opa.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/rdma.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/roce.conf
%config(noreplace) %{_sysconfdir}/rdma/rdma.conf
%dir %{_sysconfdir}/modprobe.d
%config(noreplace) %{_sysconfdir}/modprobe.d/mlx4.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/truescale.conf
%{_unitdir}/rdma-hw.target
%{_unitdir}/rdma-load-modules@.service
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%dir %{dracutlibdir}/modules.d/05rdma
%{dracutlibdir}/modules.d/05rdma/module-setup.sh
%dir %{_udevrulesdir}
%{_udevrulesdir}/../rdma_rename
%{_udevrulesdir}/60-rdma-ndd.rules
%{_udevrulesdir}/60-rdma-persistent-naming.rules
%{_udevrulesdir}/75-rdma-description.rules
%{_udevrulesdir}/90-rdma-hw-modules.rules
%{_udevrulesdir}/90-rdma-ulp-modules.rules
%{_udevrulesdir}/90-rdma-umad.rules
%dir %{sysmodprobedir}
%{sysmodprobedir}/libmlx4.conf
%{_libexecdir}/mlx4-setup.sh
%{_libexecdir}/truescale-serdes.cmds
%{_sbindir}/rdma-ndd
%{_unitdir}/rdma-ndd.service
%{_mandir}/man7/rxe*
%{_mandir}/man8/rdma-ndd.*

%files devel
%doc %{_docdir}/%{name}/MAINTAINERS
%dir %{_includedir}/infiniband
%dir %{_includedir}/rdma
%{_includedir}/infiniband/*
%{_includedir}/rdma/*
%if %{with_static}
%{_libdir}/lib*.a
%endif
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/efadv*
%{_mandir}/man3/ibv_*
%{_mandir}/man3/rdma*
%{_mandir}/man3/umad*
%{_mandir}/man3/*_to_ibv_rate.*
%{_mandir}/man7/rdma_cm.*
%{_mandir}/man3/mlx5dv*
%{_mandir}/man3/mlx4dv*
%{_mandir}/man7/efadv*
%{_mandir}/man7/mlx5dv*
%{_mandir}/man7/mlx4dv*
%{_mandir}/man3/ibnd_*
# New in v49.0
%{_mandir}/man3/manadv*
%{_mandir}/man7/manadv*

%files -n infiniband-diags-compat
%{_sbindir}/ibcheckerrs
%{_mandir}/man8/ibcheckerrs*
%{_sbindir}/ibchecknet
%{_mandir}/man8/ibchecknet*
%{_sbindir}/ibchecknode
%{_mandir}/man8/ibchecknode*
%{_sbindir}/ibcheckport
%{_mandir}/man8/ibcheckport.*
%{_sbindir}/ibcheckportwidth
%{_mandir}/man8/ibcheckportwidth*
%{_sbindir}/ibcheckportstate
%{_mandir}/man8/ibcheckportstate*
%{_sbindir}/ibcheckwidth
%{_mandir}/man8/ibcheckwidth*
%{_sbindir}/ibcheckstate
%{_mandir}/man8/ibcheckstate*
%{_sbindir}/ibcheckerrors
%{_mandir}/man8/ibcheckerrors*
%{_sbindir}/ibdatacounts
%{_mandir}/man8/ibdatacounts*
%{_sbindir}/ibdatacounters
%{_mandir}/man8/ibdatacounters*
%{_sbindir}/ibdiscover.pl
%{_mandir}/man8/ibdiscover*
%{_sbindir}/ibswportwatch.pl
%{_mandir}/man8/ibswportwatch*
%{_sbindir}/ibqueryerrors.pl
%{_sbindir}/iblinkinfo.pl
%{_sbindir}/ibprintca.pl
%{_mandir}/man8/ibprintca*
%{_sbindir}/ibprintswitch.pl
%{_mandir}/man8/ibprintswitch*
%{_sbindir}/ibprintrt.pl
%{_mandir}/man8/ibprintrt*
%{_sbindir}/set_nodedesc.sh

%files -n infiniband-diags
%{_sbindir}/ibaddr
%{_mandir}/man8/ibaddr*
%{_sbindir}/ibnetdiscover
%{_mandir}/man8/ibnetdiscover*
%{_sbindir}/ibping
%{_mandir}/man8/ibping*
%{_sbindir}/ibportstate
%{_mandir}/man8/ibportstate*
%{_sbindir}/ibroute
%{_mandir}/man8/ibroute.*
%{_sbindir}/ibstat
%{_mandir}/man8/ibstat.*
%{_sbindir}/ibsysstat
%{_mandir}/man8/ibsysstat*
%{_sbindir}/ibtracert
%{_mandir}/man8/ibtracert*
%{_sbindir}/perfquery
%{_mandir}/man8/perfquery*
%{_sbindir}/sminfo
%{_mandir}/man8/sminfo*
%{_sbindir}/smpdump
%{_mandir}/man8/smpdump*
%{_sbindir}/smpquery
%{_mandir}/man8/smpquery*
%{_sbindir}/saquery
%{_mandir}/man8/saquery*
%{_sbindir}/vendstat
%{_mandir}/man8/vendstat*
%{_sbindir}/iblinkinfo
%{_mandir}/man8/iblinkinfo*
%{_sbindir}/ibqueryerrors
%{_mandir}/man8/ibqueryerrors*
%{_sbindir}/ibcacheedit
%{_mandir}/man8/ibcacheedit*
%{_sbindir}/ibccquery
%{_mandir}/man8/ibccquery*
%{_sbindir}/ibccconfig
%{_mandir}/man8/ibccconfig*
%{_sbindir}/dump_fts
%{_mandir}/man8/dump_fts*
%{_sbindir}/ibhosts
%{_mandir}/man8/ibhosts*
%{_sbindir}/ibswitches
%{_mandir}/man8/ibswitches*
%{_sbindir}/ibnodes
%{_mandir}/man8/ibnodes*
%{_sbindir}/ibrouters
%{_mandir}/man8/ibrouters*
%{_sbindir}/ibfindnodesusing.pl
%{_mandir}/man8/ibfindnodesusing*
%{_sbindir}/ibidsverify.pl
%{_mandir}/man8/ibidsverify*
%{_sbindir}/check_lft_balance.pl
%{_mandir}/man8/check_lft_balance*
%{_sbindir}/dump_lfts.sh
%{_mandir}/man8/dump_lfts*
%{_sbindir}/dump_mfts.sh
%{_mandir}/man8/dump_mfts*
%{_sbindir}/ibclearerrors
%{_mandir}/man8/ibclearerrors*
%{_sbindir}/ibclearcounters
%{_mandir}/man8/ibclearcounters*
%{_sbindir}/ibstatus
%{_mandir}/man8/ibstatus*
%{_mandir}/man8/infiniband-diags*
%{_libdir}/libibmad*.so.*
%{_libdir}/libibnetdisc*.so.*
%{perl_vendorlib}/IBswcountlimits.pm
%config(noreplace) %{_sysconfdir}/infiniband-diags/error_thresholds
%config(noreplace) %{_sysconfdir}/infiniband-diags/ibdiag.conf

%files -n libibverbs
%dir %{_sysconfdir}/libibverbs.d
%dir %{_libdir}/libibverbs
%{_libdir}/libefa.so.*
%{_libdir}/libibverbs*.so.*
%{_libdir}/libibverbs/*.so
%{_libdir}/libmlx5.so.*
%{_libdir}/libmlx4.so.*
%{_libdir}/libmana.so.*
%config(noreplace) %{_sysconfdir}/libibverbs.d/*.driver
%doc %{_docdir}/%{name}/libibverbs.md

%files -n libibverbs-utils
%{_bindir}/ibv_*
%{_mandir}/man1/ibv_*

%files -n ibacm
%config(noreplace) %{_sysconfdir}/rdma/ibacm_opts.cfg
%{_bindir}/ib_acme
%{_sbindir}/ibacm
%{_mandir}/man1/ib_acme.*
%{_mandir}/man7/ibacm.*
%{_mandir}/man7/ibacm_prov.*
%{_mandir}/man8/ibacm.*
%{_unitdir}/ibacm.service
%{_unitdir}/ibacm.socket
%dir %{_libdir}/ibacm
%{_libdir}/ibacm/*
%doc %{_docdir}/%{name}/ibacm.md

%files -n iwpmd
%{_sbindir}/iwpmd
%{_unitdir}/iwpmd.service
%config(noreplace) %{_sysconfdir}/rdma/modules/iwpmd.conf
%config(noreplace) %{_sysconfdir}/iwpmd.conf
%{_udevrulesdir}/90-iwpmd.rules
%{_mandir}/man8/iwpmd.*
%{_mandir}/man5/iwpmd.*

%files -n libibumad
%{_libdir}/libibumad*.so.*

%files -n librdmacm
%{_libdir}/librdmacm*.so.*
%dir %{_libdir}/rsocket
%{_libdir}/rsocket/*.so*
%doc %{_docdir}/%{name}/librdmacm.md
%{_mandir}/man7/rsocket.*

%files -n librdmacm-utils
%{_bindir}/cmtime
%{_bindir}/mckey
%{_bindir}/rcopy
%{_bindir}/rdma_client
%{_bindir}/rdma_server
%{_bindir}/rdma_xclient
%{_bindir}/rdma_xserver
%{_bindir}/riostream
%{_bindir}/rping
%{_bindir}/rstream
%{_bindir}/ucmatose
%{_bindir}/udaddy
%{_bindir}/udpong
%{_mandir}/man1/cmtime.*
%{_mandir}/man1/mckey.*
%{_mandir}/man1/rcopy.*
%{_mandir}/man1/rdma_client.*
%{_mandir}/man1/rdma_server.*
%{_mandir}/man1/rdma_xclient.*
%{_mandir}/man1/rdma_xserver.*
%{_mandir}/man1/riostream.*
%{_mandir}/man1/rping.*
%{_mandir}/man1/rstream.*
%{_mandir}/man1/ucmatose.*
%{_mandir}/man1/udaddy.*
%{_mandir}/man1/udpong.*

%files -n srp_daemon
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/srp_daemon.conf
%{_libexecdir}/srp_daemon/start_on_all_ports
%{_unitdir}/srp_daemon.service
%{_unitdir}/srp_daemon_port@.service
%{_sbindir}/ibsrpdm
%{_sbindir}/srp_daemon
%{_sbindir}/run_srp_daemon
%{_udevrulesdir}/60-srp_daemon.rules
%{_mandir}/man5/srp_daemon.service.5*
%{_mandir}/man5/srp_daemon_port@.service.5*
%{_mandir}/man8/ibsrpdm.8*
%{_mandir}/man8/srp_daemon.8*
%doc %{_docdir}/%{name}/ibsrpdm.md

%if %{with_pyverbs}
%files -n python3-pyverbs
%{python3_sitearch}/pyverbs
%{_docdir}/%{name}/tests/*.py
%endif

%changelog
* Mon Jan 22 2024 Kanika Nema <kanikanema@microsoft.com> - 49.0-1
- Upgrade to 49.0 for AzL 3.0 release

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 39.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Feb 14 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 39.0-1
- Update to version 39.0.
- Modified patch to apply to new version.

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 31.0-3
- Use python3-docutils dependency instead of python-docutils

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 31.0-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT). License verified.

* Wed Aug 19 2020 Honggang Li <honli@redhat.com> - 31.0-1
- Rebase to upstream release v31.0

* Thu Jul 30 2020 Honggang Li <honli@redhat.com> - 30.0-6
- Update cmake options

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 30.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 02 2020 Stephen Gallagher <sgallagh@redhat.com> - 30.0-4
- Don't throw script errors if udev is not installed

* Wed Jul  1 2020 Jeff Law <law@redhat.com> - 30.0-3
- Disable LTO

* Thu Jun 25 2020 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 30.0-2
- Drop dependencies on systemd (#1837812)

* Mon Jun 15 2020 Honggang Li <honli@redhat.com> - 30.0-1
- Rebase to upstream release v30.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 29.0-2
- Rebuilt for Python 3.9

* Mon Apr 13 2020 Honggang Li <honli@redhat.com> - 29.0-1
- Rebase to upstream release v29.0

* Wed Feb 12 2020 Honggang Li <honli@redhat.com> - 28.0-1
- Rebase to upstream release v28.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 27.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Orion Poplawski <orion@nwra.com> - 27.0-3
- Fix typo in requires

* Sun Jan 19 2020 Honggang Li <honli@redhat.com> - 27.0-2
- Backport some spec improvement from upstream

* Thu Dec 12 2019 Honggang Li <honli@redhat.com> - 27.0-1
- Rebase to upstream release v27.0

* Thu Nov 28 2019 Honggang Li <honli@redhat.com> - 26.1-1
- Rebase to upstream release v26.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Björn Esser <besser82@fedoraproject.org> - 20.1-2
- Append curdir to CMake invokation. (#1668512)

* Fri Oct 19 2018 Jarod Wilson <jarod@redhat.com> - 20.1-1
- Long overdue update to upstream v20.1 stable release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 18 2018 Iryna Shcherbina <ishcherb@redhat.com> - 16.2-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 06 2018 Orion Poplawski <orion@nwra.com> - 16.2-3
- Build for s390/x

* Tue Feb 06 2018 Patrick Uiterwijk <patrick@puiterwijk.org> - 16.2-2
- Fix escaped macro

* Sun Feb 04 2018 Doug Ledford <dledford@redhat.com> - 16.2-1
- Update to rdma-core-16.2
- Drop the old sysv initscript files

* Wed Aug 09 2017 Jarod Wilson <jarod@redhat.com> - 14-4
- Make use of systemd_requires, own srp_daemon dir

* Tue Aug 01 2017 Jarod Wilson <jarod@redhat.com> - 14-3
- Revert work-around for ppc64le library issues
- Add Obsoletes/Provides for libusnic_verbs

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jul 25 2017 Jarod Wilson <jarod@redhat.com> - 14-1
- Update to upstream v14 release
- Sync packaging updates from RHEL and upstream

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Jarod Wilson <jarod@redhat.com> - 12-1
- Update to upstream final v12 release

* Wed Jan 25 2017 Jarod Wilson <jarod@redhat.com> - 12-0.1.rc3.1
- Initial import to Fedora package database via post-v12-rc3 git snapshot
