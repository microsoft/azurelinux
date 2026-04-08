## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 5;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: rdma-core
Version: 58.0
Release: %autorelease
Summary: RDMA core userspace libraries and daemons

# Almost everything is licensed under the OFA dual GPLv2, 2 Clause BSD license
#  providers/ipathverbs/ Dual licensed using a BSD license with an extra patent clause
#  providers/rxe/ Incorporates code from ipathverbs and contains the patent clause
#  providers/hfi1verbs Uses the 3 Clause BSD license
License: GPL-2.0-only OR BSD-2-Clause AND BSD-3-Clause
Url: https://github.com/linux-rdma/rdma-core
Source: https://github.com/linux-rdma/rdma-core/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch9998: 9998-kernel-boot-Do-not-perform-device-rename-on-OPA-devi.patch
Patch9999: 9999-udev-keep-NAME_KERNEL-as-default-interface-naming-co.patch
# Do not build static libs by default.
%define with_static %{?_with_static: 1} %{?!_with_static: 0}

# 32-bit arm is missing required arch-specific memory barriers,
ExcludeArch: %{arm}

BuildRequires: binutils
BuildRequires: cmake >= 2.8.11
BuildRequires: gcc
BuildRequires: libudev-devel
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
BuildRequires: /usr/bin/rst2man
%ifarch %{valgrind_arches}
BuildRequires: valgrind-devel
%endif
BuildRequires: systemd
BuildRequires: systemd-devel
%if 0%{?fedora} >= 32 || 0%{?rhel} >= 8
%define with_pyverbs %{?_with_pyverbs: 1} %{?!_with_pyverbs: %{?!_without_pyverbs: 1} %{?_without_pyverbs: 0}}
%else
%define with_pyverbs %{?_with_pyverbs: 1} %{?!_with_pyverbs: 0}
%endif
%if %{with_pyverbs}
BuildRequires: python3-devel
BuildRequires: python3-Cython
%else
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30
BuildRequires: python3
%else
BuildRequires: python
%endif
%endif

%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30 || %{with_pyverbs}
BuildRequires: python3-docutils
%else
BuildRequires: python-docutils
%endif

%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
BuildRequires: perl-generators
%endif

Requires: pciutils
# Red Hat/Fedora previously shipped redhat/ as a stand-alone
# package called 'rdma', which we're supplanting here.
Provides: rdma = %{version}-%{release}
Obsoletes: rdma < %{version}-%{release}
Conflicts: infiniband-diags <= 1.6.7

# Since we recommend developers use Ninja, so should packagers, for consistency.
%define CMAKE_FLAGS %{nil}
%if 0%{?fedora} >= 23 || 0%{?rhel} >= 8
# Ninja was introduced in FC23
BuildRequires: ninja-build
%define CMAKE_FLAGS -GNinja
%if 0%{?fedora} >= 33 || 0%{?rhel} >= 9
%define make_jobs ninja-build -C %{_vpath_builddir} -v %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} ninja-build -C %{_vpath_builddir} install
%else
%define make_jobs ninja-build -v %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} ninja-build install
%endif
%else
# Fallback to make otherwise
BuildRequires: make
%define make_jobs make VERBOSE=1 %{?_smp_mflags}
%define cmake_install DESTDIR=%{buildroot} make install
%endif

%if 0%{?fedora} >= 25 || 0%{?rhel} == 8
# pandoc was introduced in FC25, Centos8
BuildRequires: pandoc
%endif

%if 0%{?fedora} >= 34
# self obsoletes to remove i686 multilib package when updating to F34
Obsoletes: rdma-core < %{version}-%{release}
%endif

%description
RDMA core userspace infrastructure and documentation, including initialization
scripts, kernel driver-specific modprobe override configs, IPoIB network
scripts, dracut rules, and the rdma-ndd utility.

%package devel
Summary: RDMA core development libraries and headers
Requires: libibverbs%{?_isa} = %{version}-%{release}
Provides: libibverbs-devel = %{version}-%{release}
Obsoletes: libibverbs-devel < %{version}-%{release}
Requires: libibumad%{?_isa} = %{version}-%{release}
Provides: libibumad-devel = %{version}-%{release}
Obsoletes: libibumad-devel < %{version}-%{release}
Requires: librdmacm%{?_isa} = %{version}-%{release}
Provides: librdmacm-devel = %{version}-%{release}
Obsoletes: librdmacm-devel < %{version}-%{release}
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
Obsoletes: openib-diags < 1.3

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
Provides: libcxgb4 = %{version}-%{release}
Obsoletes: libcxgb4 < %{version}-%{release}
Provides: libefa = %{version}-%{release}
Obsoletes: libefa < %{version}-%{release}
Provides: libhfi1 = %{version}-%{release}
Obsoletes: libhfi1 < %{version}-%{release}
Provides: libipathverbs = %{version}-%{release}
Obsoletes: libipathverbs < %{version}-%{release}
Provides: libirdma = %{version}-%{release}
Obsoletes: libirdma < %{version}-%{release}
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
%if 0%{?fedora} >= 34
Obsoletes: libibverbs-core < %{version}-%{release}
%endif

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
- libipathverbs: QLogic InfiniPath HCA
- libirdma: Intel Ethernet Connection RDMA
- libmana: Microsoft Azure Network Adapter
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
%{?systemd_requires}
Requires: libibumad%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

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
%{?systemd_requires}

%description -n iwpmd
iwpmd provides a userspace service for iWarp drivers to claim
tcp ports through the standard socket interface.

%package -n libibumad
Summary: OpenFabrics Alliance InfiniBand umad (userspace management datagram) library

%description -n libibumad
libibumad provides the userspace management datagram (umad) library
functions, which sit on top of the umad modules in the kernel. These
are used by the IB diagnostic and management tools, including OpenSM.

%package -n librdmacm
Summary: Userspace RDMA Connection Manager
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n librdmacm
librdmacm provides a userspace RDMA Communication Management API.

%package -n librdmacm-utils
Summary: Examples for the librdmacm library
Requires: librdmacm%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n librdmacm-utils
Example test programs for the librdmacm library.

%package -n srp_daemon
Summary: Tools for using the InfiniBand SRP protocol devices
Obsoletes: srptools <= 1.0.3
Provides: srptools = %{version}-%{release}
Obsoletes: openib-srptools <= 0.0.6
%{?systemd_requires}
Requires: libibumad%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n srp_daemon
In conjunction with the kernel ib_srp driver, srp_daemon allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%if %{with_pyverbs}
%package -n python3-pyverbs
Summary: Python3 API over IB verbs
%{?python_provide:%python_provide python3-pyverbs}
Requires: librdmacm%{?_isa} = %{version}-%{release}
Requires: libibverbs%{?_isa} = %{version}-%{release}

%description -n python3-pyverbs
Pyverbs is a Cython-based Python API over libibverbs, providing an
easy, object-oriented access to IB verbs.
%endif

%prep
%setup -q
%if 0%{?fedora}
%patch 9998 -p1
%endif
%if 0%{?rhel}
%patch 9999 -p1
%endif

%build

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
%if %{defined __python3}
         -DPYTHON_EXECUTABLE:PATH=%{__python3} \
         -DCMAKE_INSTALL_PYTHON_ARCH_LIB:PATH=%{python3_sitearch} \
%endif
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
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/05rdma
mkdir -p %{buildroot}%{sysmodprobedir}
install -D -m0644 redhat/rdma.mlx4.conf %{buildroot}/%{_sysconfdir}/rdma/mlx4.conf
install -D -m0755 redhat/rdma.modules-setup.sh %{buildroot}%{dracutlibdir}/modules.d/05rdma/module-setup.sh
install -D -m0644 redhat/rdma.mlx4.sys.modprobe %{buildroot}%{sysmodprobedir}/libmlx4.conf
install -D -m0755 redhat/rdma.mlx4-setup.sh %{buildroot}%{_libexecdir}/mlx4-setup.sh
rm -f %{buildroot}%{_sysconfdir}/rdma/modules/rdma.conf
install -D -m0644 redhat/rdma.conf %{buildroot}%{_sysconfdir}/rdma/modules/rdma.conf

# ibacm
(if [ -d %{__cmake_builddir} ]; then cd %{__cmake_builddir}; fi
 ./bin/ib_acme -D . -O &&
 install -D -m0644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/)

# Delete the package's init.d scripts
rm -rf %{buildroot}/%{_initrddir}/
rm -f %{buildroot}/%{_sbindir}/srp_daemon.sh

%ldconfig_scriptlets -n libibverbs

%ldconfig_scriptlets -n libibumad

%ldconfig_scriptlets -n librdmacm

%post -n rdma-core
if [ -x /sbin/udevadm ]; then
/sbin/udevadm trigger --subsystem-match=infiniband --action=change || true
/sbin/udevadm trigger --subsystem-match=net --action=change || true
/sbin/udevadm trigger --subsystem-match=infiniband_mad --action=change || true
fi
%systemd_post rdma-load-modules@rdma.service
%systemd_post rdma-load-modules@infiniband.service
%systemd_post rdma-load-modules@roce.service

%preun -n rdma-core
%systemd_preun rdma-load-modules@rdma.service
%systemd_preun rdma-load-modules@infiniband.service
%systemd_preun rdma-load-modules@roce.service
%postun -n rdma-core
%systemd_postun_with_restart rdma-load-modules@rdma.service
%systemd_postun_with_restart rdma-load-modules@infiniband.service
%systemd_postun_with_restart rdma-load-modules@roce.service

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
%dir %{_sysconfdir}/rdma
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/70-persistent-ipoib.rules
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/rxe.md
%doc %{_docdir}/%{name}/udev.md
%doc %{_docdir}/%{name}/tag_matching.md
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/infiniband.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/iwarp.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/opa.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/rdma.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/roce.conf
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
%license COPYING.*

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
%{_mandir}/man3/hnsdv*
%{_mandir}/man3/ibv_*
%{_mandir}/man3/rdma*
%{_mandir}/man3/umad*
%{_mandir}/man3/*_to_ibv_rate.*
%{_mandir}/man7/rdma_cm.*
%{_mandir}/man3/manadv*
%{_mandir}/man3/mlx5dv*
%{_mandir}/man3/mlx4dv*
%{_mandir}/man7/efadv*
%{_mandir}/man7/hnsdv*
%{_mandir}/man7/manadv*
%{_mandir}/man7/mlx5dv*
%{_mandir}/man7/mlx4dv*
%{_mandir}/man3/ibnd_*

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
%{_libdir}/libhns.so.*
%{_libdir}/libibverbs*.so.*
%{_libdir}/libibverbs/*.so
%{_libdir}/libmana.so.*
%{_libdir}/libmlx5.so.*
%{_libdir}/libmlx4.so.*
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
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 58.0-5
- Latest state for rdma-core

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 58.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 58.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Kamal Heib <kheib@redhat.com> - 58.0-2
- Add support for packit

* Mon Jun 16 2025 Kamal Heib <kheib@redhat.com> - 58.0-1
- Update to upstream release v58.0

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 57.0-3
- Rebuilt for Python 3.14

* Thu Apr 24 2025 TD Mackey <tdmackey@booleanhaiku.com> - 57.0-2
- Fix rdma-core post scripts

* Wed Apr 23 2025 Kamal Heib <kheib@redhat.com> - 57.0-1
- Update to upstream release v57.0

* Wed Feb 12 2025 Kamal Heib <kheib@redhat.com> - 56.0-2
- Add missing rdma-load-modules systemd scriptlets

* Thu Feb 06 2025 Kamal Heib <kheib@redhat.com> - 56.0-1
- Update to upstream release v56.0

* Wed Jan 29 2025 Kamal Heib <kheib@redhat.com> - 55.0-1
- Update to upstream release v55.0

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 54.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 19 2024 Richard W.M. Jones <rjones@redhat.com> - 54.0-3
- Rebuild for riscv64

* Tue Nov 19 2024 Richard W.M. Jones <rjones@fedoraproject.org> - 54.0-2
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
