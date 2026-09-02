# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?cmake: %global cmake cmake}
%{!?make_jobs: %global make_jobs make VERBOSE=1 %{?_smp_mflags}}
%{!?cmake_install: %global cmake_install DESTDIR=%{buildroot} make install}
%{!?_udevrulesdir: %global _udevrulesdir /etc/udev/rules.d}

# if systemd not supported, do not install the systemd service files
%{!?_unitdir: %global _unitdir NA}
%global WITH_SYSTEMD %(if ( test -d "%{_unitdir}" > /dev/null);then echo -n '1'; else echo -n '0'; fi)

# build_docs: disabled by default
%bcond_with build_docs


# valgrind support: disabled by default; use "--with valgrind" to enable
%bcond_with valgrind

%if %{?rhel:%{rhel} < 8}%{?!rhel:0}
%global with_srp_compat 1
%endif
%if %{?suse_version:%{suse_version} < 1500}%{?!suse_version:0}
%global with_srp_compat 1
%endif

%define rst2man_exist %(test -f /usr/bin/rst2man; echo $?)
%define __cmake_in_source_build 0

%define python38_exist %(test -f /usr/bin/python3.8; echo $?)
%if 0%{?alinux} == 3 && %{python38_exist} == 0
%define __python3 /usr/bin/python3.8
%endif

Name: rdma-core-ofed
Version: 2604.0.7
Release: 1%{?dist}
Summary: RDMA core userspace libraries and daemons
Group: System Environment/Libraries

%global community_rdma_conflicts() %{expand:
Conflicts: rdma-core < %{version}
Conflicts: rdma-core-devel < %{version}
Conflicts: libibverbs < %{version}
Conflicts: libibverbs-devel < %{version}
Conflicts: libibverbs-utils < %{version}
Conflicts: libibumad < %{version}
Conflicts: librdmacm < %{version}
Conflicts: librdmacm-utils < %{version}
Conflicts: infiniband-diags < %{version}
Conflicts: infiniband-diags-compat < %{version}
Conflicts: ibacm < %{version}
Conflicts: iwpmd < %{version}
Conflicts: srp_daemon < %{version}
Conflicts: python3-pyverbs < %{version}
}
%{community_rdma_conflicts}

# Almost everything is licensed under the OFA dual GPLv2, 2 Clause BSD license
#  providers/ipathverbs/ Dual licensed using a BSD license with an extra patent clause
#  providers/rxe/ Incorporates code from ipathverbs and contains the patent clause
#  providers/hfi1verbs Uses the 3 Clause BSD license
License: GPLv2 or BSD
Url: https://github.com/linux-rdma/rdma-core
Source: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
# OFED: Build static libs by default.
%define with_static %{?_without_static: 0} %{?!_without_static: 1}
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

# 32-bit arm is missing required arch-specific memory barriers,
ExcludeArch: %{arm}

BuildRequires: binutils
BuildRequires: gcc
BuildRequires: libudev-devel
BuildRequires: cmake
BuildRequires: pkgconfig
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
%if %{with valgrind}
BuildRequires: valgrind-devel
%endif
%if 0%{?fedora} < 37
BuildRequires: systemd
%endif
BuildRequires: systemd-devel
%if 0%{?euleros:1} || 0%{?rhel} == 7 || 0%{?uos} == 20 || 0%{?UnionTech} == 2
%define with_pyverbs 0
%else
%define with_pyverbs 1
%endif
%if %{with_pyverbs}
%if 0%{?rhel} == 7
BuildRequires: python36-devel
BuildRequires: python36-Cython
BuildRequires: cmake3
%global cmake %cmake3
%else
BuildRequires: cmake >= 2.8.11
%if 0%{?alinux} == 3 && %{python38_exist} == 0
BuildRequires: python38-devel
BuildRequires: python38-Cython
%else
BuildRequires: python3-devel
BuildRequires: python3-Cython
%endif
%endif
%else
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30 || "%{bclinux}" == "22.10U2" ||  0%{?openEuler} >= 2 || 0%{?UnionTech} == 2
BuildRequires: python3
%else
BuildRequires: python
%endif
%endif

# Mariner specific fix to include missing asm/socket.h
%if "%{_vendor}" == "mariner"
BuildRequires: kernel-headers
%endif

# EulerOS fix to include make and /usr/bin/ld
%if 0%{?euleros}
BuildRequires: binutils-extra
%endif

%if 0%{?euleros} || 0%{?openEuler}
BuildRequires: make
%endif

%if %{with build_docs}
%if 0%{?rhel} >= 8 || 0%{?fedora} >= 30 || %{with_pyverbs}
BuildRequires: python3-docutils
%else
BuildRequires: python-docutils
%endif
%endif

%if 0%{?fedora} >= 21 || 0%{?rhel} >= 8
BuildRequires: perl-generators
%endif

Requires: pciutils
# Red Hat/Fedora previously shipped redhat/ as a stand-alone
# package called 'rdma', which we're supplanting here.
Provides: rdma = %{version}-%{release}
Obsoletes: rdma < %{version}-%{release}
Provides: rdma-ndd = %{version}-%{release}
Obsoletes: rdma-ndd < %{version}-%{release}
Provides: rdma-core-help = %{version}-%{release}
Obsoletes: rdma-core-help < %{version}-%{release}
# the ndd utility moved from infiniband-diags to rdma-core
Requires: pciutils
# 32-bit arm is missing required arch-specific memory barriers,
ExcludeArch: %{arm}

%define CMAKE_FLAGS %{nil}
%if 0%{?suse_version}
# Tumbleweed's cmake RPM macro adds -Wl,--no-undefined to the module flags
# which is totally inappropriate and breaks building 'ENABLE_EXPORTS' style
# module libraries (eg ibacmp).
%define CMAKE_FLAGS -DCMAKE_MODULE_LINKER_FLAGS=""
%endif

%if 0%{?fedora} >= 25 || 0%{?rhel} == 8
# pandoc was introduced in FC25, Centos8
%if %{with build_docs}
BuildRequires: pandoc
%endif
%endif

%description
RDMA core userspace infrastructure and documentation, including initialization
scripts, kernel driver-specific modprobe override configs, IPoIB network
scripts, dracut rules, and the rdma-ndd utility.

%package devel
%{community_rdma_conflicts}
Summary: RDMA core development libraries and headers
Group: System Environment/Libraries
Requires: libibverbs-ofed%{?_isa} = %{version}-%{release}
Provides: libibverbs-devel = %{version}-%{release}
Obsoletes: libibverbs-devel < %{version}-%{release}
Provides: libibverbs-devel-static = %{version}-%{release}
Obsoletes: libibverbs-devel-static < %{version}-%{release}
Requires: libibumad-ofed%{?_isa} = %{version}-%{release}
Provides: libibumad-devel = %{version}-%{release}
Obsoletes: libibumad-devel < %{version}-%{release}
Provides: libibumad-static = %{version}-%{release}
Obsoletes: libibumad-static < %{version}-%{release}
Requires: librdmacm-ofed%{?_isa} = %{version}-%{release}
Provides: librdmacm-devel = %{version}-%{release}
Obsoletes: librdmacm-devel < %{version}-%{release}
Provides: librdmacm-static = %{version}-%{release}
Obsoletes: librdmacm-static < %{version}-%{release}
Provides: ibacm-devel = %{version}-%{release}
Obsoletes: ibacm-devel < %{version}-%{release}
Requires: infiniband-diags-ofed%{?_isa} = %{version}-%{release}
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
Provides: libcxgb3-static = %{version}-%{release}
Obsoletes: libcxgb3-static < %{version}-%{release}
Provides: libcxgb4-static = %{version}-%{release}
Obsoletes: libcxgb4-static < %{version}-%{release}
Provides: libhfi1-static = %{version}-%{release}
Obsoletes: libhfi1-static < %{version}-%{release}
Provides: libipathverbs-static = %{version}-%{release}
Obsoletes: libipathverbs-static < %{version}-%{release}
Provides: libmlx4-devel = %{version}-%{release}
Obsoletes: libmlx4-devel < %{version}-%{release}
Provides: libmlx4-static = %{version}-%{release}
Obsoletes: libmlx4-static < %{version}-%{release}
Provides: libmlx5-devel = %{version}-%{release}
Obsoletes: libmlx5-devel < %{version}-%{release}
Provides: libmlx5-static = %{version}-%{release}
Obsoletes: libmlx5-static < %{version}-%{release}
Provides: libnes-static = %{version}-%{release}
Obsoletes: libnes-static < %{version}-%{release}
Provides: libocrdma-static = %{version}-%{release}
Obsoletes: libocrdma-static < %{version}-%{release}
Provides: libi40iw-devel-static = %{version}-%{release}
Obsoletes: libi40iw-devel-static < %{version}-%{release}
Provides: libmthca-static = %{version}-%{release}
Obsoletes: libmthca-static < %{version}-%{release}

%description devel
RDMA core development libraries and headers.

%changelog
* Fri May 1 2026 root - 2604.0.7-1
Automated build 1

* Tue May 9 2023 Leon Romanovsky <leonro@nvidia.com> - 44
- Fix epoch warning

%package -n infiniband-diags-ofed
%{community_rdma_conflicts}
Provides: perl(IBswcountlimits)
Provides: libibmad = %{version}-%{release}
Obsoletes: libibmad < %{version}-%{release}
Provides: libibmad5 = %{version}-%{release}
Obsoletes: libibmad5 < %{version}-%{release}
Provides: libibnetdisc5 = %{version}-%{release}
Obsoletes: libibnetdisc5 < %{version}-%{release}
Obsoletes: openib-diags < 1.3
Summary: InfiniBand Diagnostic Tools

%description -n infiniband-diags-ofed
This package provides IB diagnostic programs and scripts needed to diagnose an
IB subnet.  infiniband-diags now also provides libibmad.  libibmad provides
low layer IB functions for use by the IB diagnostic and management
programs. These include MAD, SA, SMP, and other basic IB functions.

%package -n infiniband-diags-compat-ofed
%{community_rdma_conflicts}
Summary: OpenFabrics Alliance InfiniBand Diagnostic Tools

%description -n infiniband-diags-compat-ofed
Deprecated scripts and utilities which provide duplicated functionality, most
often at a reduced performance. These are maintained for the time being for
compatibility reasons.

%package -n libibverbs-ofed
%{community_rdma_conflicts}
Provides: libcxgb4 = %{version}-%{release}
Obsoletes: libcxgb4 < %{version}-%{release}
Provides: libefa = %{version}-%{release}
Obsoletes: libefa < %{version}-%{release}
Provides: libefa1 = %{version}-%{release}
Obsoletes: libefa1 < %{version}-%{release}
Provides: liberdma = %{version}-%{release}
Obsoletes: liberdma < %{version}-%{release}
Provides: libhfi1 = %{version}-%{release}
Obsoletes: libhfi1 < %{version}-%{release}
Provides: libhns = %{version}-%{release}
Obsoletes: libhns < %{version}-%{release}
Provides: libhns1 = %{version}-%{release}
Obsoletes: libhns1 < %{version}-%{release}
Provides: libionic = %{version}-%{release}
Obsoletes: libionic < %{version}-%{release}
Provides: libipathverbs = %{version}-%{release}
Obsoletes: libipathverbs < %{version}-%{release}
Provides: libirdma = %{version}-%{release}
Obsoletes: libirdma < %{version}-%{release}
Provides: libmana = %{version}-%{release}
Obsoletes: libmana < %{version}-%{release}
Provides: libmana1 = %{version}-%{release}
Obsoletes: libmana1 < %{version}-%{release}
Provides: libmlx4 = %{version}-%{release}
Obsoletes: libmlx4 < %{version}-%{release}
Provides: libmlx4-1 = %{version}-%{release}
Obsoletes: libmlx4-1 < %{version}-%{release}
Provides: libmlx5-1 = %{version}-%{release}
Obsoletes: libmlx5-1 < %{version}-%{release}
Provides: libmlx5 = %{version}-%{release}
Obsoletes: libmlx5 < %{version}-%{release}
Provides: libmthca = %{version}-%{release}
Obsoletes: libmthca < %{version}-%{release}
Provides: libocrdma = %{version}-%{release}
Obsoletes: libocrdma < %{version}-%{release}
Provides: librxe = %{version}-%{release}
Obsoletes: librxe < %{version}-%{release}
Provides: libibverbs1 = %{version}-%{release}
Obsoletes: libibverbs1 < %{version}-%{release}
Summary: A library and drivers for direct userspace use of RDMA (InfiniBand/iWARP/RoCE) hardware
Group: System Environment/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
%ifnarch s390x s390
%endif

%description -n libibverbs-ofed
libibverbs is a library that allows userspace processes to use RDMA
"verbs" as described in the InfiniBand Architecture Specification and
the RDMA Protocol Verbs Specification.  This includes direct hardware
access from userspace to InfiniBand/iWARP adapters (kernel bypass) for
fast path operations.

Device-specific plug-in ibverbs userspace drivers are included:

- liberdma: Alibaba Elastic RDMA (iWarp) Adapter
- libirdma: Intel Ethernet Connection RDMA
- libmana: Microsoft Azure Network Adapter
- libmlx5: Mellanox ConnectX-4+ InfiniBand HCA

%package -n libibverbs-utils-ofed
%{community_rdma_conflicts}
Summary: Examples for the libibverbs library
Requires: libibverbs-ofed%{?_isa} = %{version}-%{release}

%description -n libibverbs-utils-ofed
Useful libibverbs example programs such as ibv_devinfo, which
displays information about RDMA devices.

%package -n ibacm-ofed
%{community_rdma_conflicts}
Summary: InfiniBand Communication Manager Assistant
Group: System Environment/Libraries
%if "%{WITH_SYSTEMD}" == "1"
%{systemd_requires}
%endif
Requires: libibumad-ofed%{?_isa} = %{version}-%{release}
Requires: libibverbs-ofed%{?_isa} = %{version}-%{release}

%description -n ibacm-ofed
The ibacm daemon helps reduce the load of managing path record lookups on
large InfiniBand fabrics by providing a user space implementation of what
is functionally similar to an ARP cache.  The use of ibacm, when properly
configured, can reduce the SA packet load of a large IB cluster from O(n^2)
to O(n).  The ibacm daemon is started and normally runs in the background,
user applications need not know about this daemon as long as their app
uses librdmacm to handle connection bring up/tear down.  The librdmacm
library knows how to talk directly to the ibacm daemon to retrieve data.

%package -n libibumad-ofed
%{community_rdma_conflicts}
Provides: libibumad3 = %{version}-%{release}
Obsoletes: libibumad3 < %{version}-%{release}
Summary: OpenFabrics Alliance InfiniBand umad (userspace management datagram) library

%description -n libibumad-ofed
libibumad provides the userspace management datagram (umad) library
functions, which sit on top of the umad modules in the kernel. These
are used by the IB diagnostic and management tools, including OpenSM.

%package -n librdmacm-ofed
%{community_rdma_conflicts}
Provides: librdmacm1 = %{version}-%{release}
Obsoletes: librdmacm1 < %{version}-%{release}
Provides: rsocket = %{version}-%{release}
Obsoletes: rsocket < %{version}-%{release}
Summary: Userspace RDMA Connection Manager
Group: System Environment/Libraries
Requires: libibverbs-ofed%{?_isa} = %{version}-%{release}

%description -n librdmacm-ofed
librdmacm provides a userspace RDMA Communication Management API.

%package -n librdmacm-utils-ofed
%{community_rdma_conflicts}
Summary: Examples for the librdmacm library
Group: System Environment/Libraries
Requires: librdmacm-ofed%{?_isa} = %{version}-%{release}
Requires: libibverbs-ofed%{?_isa} = %{version}-%{release}

%description -n librdmacm-utils-ofed
Example test programs for the librdmacm library.

%package -n srp_daemon-ofed
%{community_rdma_conflicts}
Obsoletes: srptools < %{version}-%{release}
Provides: srptools = %{version}-%{release}
Obsoletes: openib-srptools <= 0.0.6
Summary: Tools for using the InfiniBand SRP protocol devices
Group: System Environment/Libraries
%if "%{WITH_SYSTEMD}" == "1"
%{systemd_requires}
%endif
Requires: libibumad-ofed%{?_isa} = %{version}-%{release}
Requires: libibverbs-ofed%{?_isa} = %{version}-%{release}

%description -n srp_daemon-ofed
In conjunction with the kernel ib_srp driver, srp_daemon allows you to
discover and use SCSI devices via the SCSI RDMA Protocol over InfiniBand.

%if %{with_pyverbs}
%package -n python3-pyverbs-ofed
%{community_rdma_conflicts}
Summary: Python3 API over IB verbs
%{?python_provide:%python_provide python%{python3_pkgversion}-pyverbs}

%description -n python3-pyverbs-ofed
Pyverbs is a Cython-based Python API over libibverbs, providing an
easy, object-oriented access to IB verbs.
%endif

%prep
tar -xf %{SOURCE0}
_rdmacore_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/rdma-core-*.src.rpm' -print -quit)
if [ -z "$_rdmacore_srpm" ]; then
    echo "ERROR: rdma-core source RPM not found inside %{SOURCE0}" >&2
    exit 1
fi
rpm2cpio "$_rdmacore_srpm" | cpio -idm './rdma-core-%{version}.tar.gz'
tar -xf rdma-core-%{version}.tar.gz
rm -rf MLNX_OFED_SRC-* rdma-core-%{version}.tar.gz
cd rdma-core-%{version}

%build
pushd rdma-core-%{version}

# New RPM defines _rundir, usually as /run
%if 0%{?_rundir:1}
%else
%define _rundir /var/run
%endif

%{!?EXTRA_CMAKE_FLAGS: %global EXTRA_CMAKE_FLAGS %{nil}}

# Pass all of the rpm paths directly to GNUInstallDirs and our other defines.
%cmake %{CMAKE_FLAGS} \
         -DCMAKE_BUILD_TYPE=Release \
         -DCMAKE_INSTALL_BINDIR:PATH=%{_bindir} \
         -DCMAKE_INSTALL_SBINDIR:PATH=%{_sbindir} \
         -DCMAKE_INSTALL_LIBDIR:PATH=%{_lib} \
         -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
         -DCMAKE_INSTALL_LOCALSTATEDIR:PATH=%{_localstatedir} \
         -DCMAKE_INSTALL_SHAREDSTATEDIR:PATH=%{_sharedstatedir} \
         -DCMAKE_INSTALL_INCLUDEDIR:PATH=include \
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
%if "%{WITH_SYSTEMD}" == "0"
         -DWITHOUT_SYSTEMD=1 \
%endif
%if %{with_static}
         -DENABLE_STATIC=1 \
%endif
         %{EXTRA_CMAKE_FLAGS} \
%if %{defined __python3}
         -DPYTHON_EXECUTABLE:PATH=%{__python3} \
         -DCMAKE_INSTALL_PYTHON_ARCH_LIB:PATH=%{python3_sitearch} \
%endif
%if %{with srp_compat}
         -DENABLE_SRP_COMPAT=1 \
%endif
%if %{with_pyverbs}
         -DNO_PYVERBS=0
%else
	 -DNO_PYVERBS=1
%endif
%make_jobs
popd

%install
pushd rdma-core-%{version}
%cmake_install
mkdir installed_docs
mv %{buildroot}%{_docdir}/%{name}/* installed_docs/
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}

mkdir -p %{buildroot}/%{_sysconfdir}/rdma

# Red Hat specific glue
%global dracutlibdir %{_prefix}/lib/dracut
%global sysmodprobedir %{_prefix}/lib/modprobe.d
 %define _ver 2604.0.7 
 %define _rel 1 
mkdir -p %{buildroot}%{_libexecdir}
mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{dracutlibdir}/modules.d/50rdma
mkdir -p %{buildroot}%{sysmodprobedir}
install -D -m0644 redhat/rdma.mlx4.conf %{buildroot}/%{_sysconfdir}/rdma/mlx4.conf
install -D -m0644 redhat/rdma.mlx4.sys.modprobe %{buildroot}%{sysmodprobedir}/libmlx4.conf
install -D -m0755 redhat/rdma.mlx4-setup.sh %{buildroot}%{_libexecdir}/mlx4-setup.sh
rm -f %{buildroot}%{_sysconfdir}/rdma/modules/rdma.conf
install -D -m0644 kernel-boot/modules/rdma.conf %{buildroot}%{_sysconfdir}/rdma/modules/rdma.conf

# ibacm
(if [ -d %{__cmake_builddir} ]; then cd %{__cmake_builddir}; fi
IB_ACME=bin/ib_acme
[ -e build/bin/ib_acme ] && IB_ACME=build/bin/ib_acme
LD_LIBRARY_PATH=%{buildroot}%{_libdir} ${IB_ACME} -D . -O
# multi-lib conflict resolution hacks (bug 1429362)
sed -i -e 's|%{_libdir}|/usr/lib|' %{buildroot}%{_mandir}/man7/ibacm_prov.7
sed -i -e 's|%{_libdir}|/usr/lib|' ibacm_opts.cfg
 install -D -m0644 ibacm_opts.cfg %{buildroot}%{_sysconfdir}/rdma/)

if [ "%{_libexecdir}" != "/usr/libexec" ]; then
	sed -i -e 's|/usr/libexec|%{_libexecdir}|g' \
		%{buildroot}%{sysmodprobedir}/libmlx4.conf \
		#
fi

[ -d "%{buildroot}%{_prefix}/NA" ] && %{__rm} -rf %{buildroot}%{_prefix}/NA
popd

%if %{WITH_SYSTEMD} == 1
# Delete the package's init.d scripts
rm -rf %{buildroot}/%{_initrddir}/
rm -f %{buildroot}/%{_sbindir}/srp_daemon.sh
%endif

rm -f %{buildroot}%{_sysconfdir}/libibverbs.d/efa.driver
rm -f %{buildroot}%{_sysconfdir}/libibverbs.d/mlx4.driver
rm -f %{buildroot}%{_libdir}/libibverbs/libefa-rdmav*.so
rm -f %{buildroot}%{_libdir}/libibverbs/libmlx4-rdmav*.so

%post -n rdma-core-ofed
if [ -x /sbin/udevadm ]; then
/sbin/udevadm trigger --subsystem-match=infiniband --action=change || true
/sbin/udevadm trigger --subsystem-match=net --action=change || true
/sbin/udevadm trigger --subsystem-match=infiniband_mad --action=change || true
fi

%post -n infiniband-diags-ofed -p /sbin/ldconfig
%postun -n infiniband-diags-ofed -p /sbin/ldconfig

%post -n libibverbs-ofed -p /sbin/ldconfig
%postun -n libibverbs-ofed -p /sbin/ldconfig

%post -n libibumad-ofed -p /sbin/ldconfig
%postun -n libibumad-ofed -p /sbin/ldconfig

%post -n librdmacm-ofed -p /sbin/ldconfig
%postun -n librdmacm-ofed -p /sbin/ldconfig

%post -n ibacm-ofed
%systemd_post ibacm.service
%preun -n ibacm-ofed
%systemd_preun ibacm.service
%postun -n ibacm-ofed
%systemd_postun_with_restart ibacm.service

%if "%{WITH_SYSTEMD}" == "1"
%post -n srp_daemon-ofed
%systemd_post srp_daemon.service
%preun -n srp_daemon-ofed
%systemd_preun srp_daemon.service
%postun -n srp_daemon-ofed
%systemd_postun_with_restart srp_daemon.service
%endif

%files
%dir %{_sysconfdir}/rdma
%doc rdma-core-%{version}/installed_docs/README.md
%doc rdma-core-%{version}/installed_docs/udev.md
%doc rdma-core-%{version}/installed_docs/tag_matching.md
%doc rdma-core-%{version}/installed_docs/70-persistent-ipoib.rules
%config(noreplace) %{_sysconfdir}/rdma/mlx4.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/rdma.conf
%if 0
%dir %{_sysconfdir}/modprobe.d
%config(noreplace) %{_sysconfdir}/modprobe.d/mlx4.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/truescale.conf
%endif
%dir %{dracutlibdir}
%dir %{dracutlibdir}/modules.d
%dir %{dracutlibdir}/modules.d/50rdma
%dir %{_udevrulesdir}
%{_udevrulesdir}/../rdma_rename
%{_udevrulesdir}/60-rdma-ndd.rules
%{_udevrulesdir}/60-rdma-persistent-naming.rules
%{_udevrulesdir}/75-rdma-description.rules
%{_udevrulesdir}/90-rdma-umad.rules
%dir %{sysmodprobedir}
%{sysmodprobedir}/libmlx4.conf
%{_libexecdir}/mlx4-setup.sh
%if 0
%{_libexecdir}/truescale-serdes.cmds
%endif
%{_sbindir}/rdma-ndd
%if "%{WITH_SYSTEMD}" == "1"
%{_unitdir}/rdma-ndd.service
%endif
%{_sbindir}/rdma_topo
%{_mandir}/man8/rdma-ndd.*
%license rdma-core-%{version}/COPYING.*

%files devel
%doc rdma-core-%{version}/installed_docs/MAINTAINERS
%dir %{_includedir}/infiniband
%dir %{_includedir}/rdma
%{_includedir}/infiniband/*
%{_includedir}/rdma/*
%if %{with_static}
%{_libdir}/lib*.a
%endif
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/ibv_*
%{_mandir}/man3/rdma*
%{_mandir}/man3/umad*
%{_mandir}/man3/*_to_ibv_rate.*
%{_mandir}/man7/rdma_cm.*
%ifnarch s390x s390
%{_mandir}/man3/mlx5dv*
%endif
%ifnarch s390x s390
%{_mandir}/man7/mlx5dv*
%endif
%{_mandir}/man3/ibnd_*

%files -n infiniband-diags-compat-ofed
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
%{_sbindir}/ibclearerrors
%{_mandir}/man8/ibclearerrors*
%{_sbindir}/ibclearcounters
%{_mandir}/man8/ibclearcounters*

%files -n infiniband-diags-ofed
%{_sbindir}/ibaddr
%{_sbindir}/ibnetdiscover
%{_sbindir}/ibping
%{_sbindir}/ibportstate
%{_sbindir}/ibroute
%{_sbindir}/ibstat
%{_sbindir}/ibsysstat
%{_sbindir}/ibtracert
%{_sbindir}/perfquery
%{_sbindir}/sminfo
%{_sbindir}/smpdump
%{_sbindir}/smpquery
%{_sbindir}/saquery
%{_sbindir}/vendstat
%{_sbindir}/iblinkinfo
%{_sbindir}/ibqueryerrors
%{_sbindir}/ibcacheedit
%{_sbindir}/ibccquery
%{_sbindir}/ibccconfig
%{_sbindir}/dump_fts
%{_sbindir}/ibhosts
%{_sbindir}/ibswitches
%{_sbindir}/ibnodes
%{_sbindir}/ibrouters
%{_sbindir}/ibfindnodesusing.pl
%{_sbindir}/ibidsverify.pl
%{_sbindir}/check_lft_balance.pl
%{_sbindir}/dump_lfts.sh
%{_mandir}/man8/dump_lfts*
%{_sbindir}/dump_mfts.sh
%{_mandir}/man8/dump_mfts*
%{_sbindir}/ibstatus
%{_libdir}/libibmad*.so.*
%{_libdir}/libibnetdisc*.so.*
%if %{rst2man_exist} == 0
%{_mandir}/man8/infiniband-diags*
%{_mandir}/man8/ibstatus*
%{_mandir}/man8/check_lft_balance*
%{_mandir}/man8/ibidsverify*
%{_mandir}/man8/ibfindnodesusing*
%{_mandir}/man8/ibrouters*
%{_mandir}/man8/ibnodes*
%{_mandir}/man8/ibnodes*
%{_mandir}/man8/ibswitches*
%{_mandir}/man8/ibhosts*
%{_mandir}/man8/dump_fts*
%{_mandir}/man8/ibping*
%{_mandir}/man8/ibportstate*
%{_mandir}/man8/ibroute.*
%{_mandir}/man8/ibstat.*
%{_mandir}/man8/ibsysstat*
%{_mandir}/man8/ibtracert*
%{_mandir}/man8/perfquery*
%{_mandir}/man8/sminfo*
%{_mandir}/man8/smpdump*
%{_mandir}/man8/smpquery*
%{_mandir}/man8/saquery*
%{_mandir}/man8/vendstat*
%{_mandir}/man8/iblinkinfo*
%{_mandir}/man8/ibqueryerrors*
%{_mandir}/man8/ibcacheedit*
%{_mandir}/man8/ibccquery*
%{_mandir}/man8/ibccconfig*
%{_mandir}/man8/ibaddr*
%{_mandir}/man8/ibnetdiscover*
%endif
%{perl_vendorlib}/IBswcountlimits.pm
%config(noreplace) %{_sysconfdir}/infiniband-diags/error_thresholds
%config(noreplace) %{_sysconfdir}/infiniband-diags/ibdiag.conf

%files -n libibverbs-ofed
%dir %{_sysconfdir}/libibverbs.d
%dir %{_libdir}/libibverbs
%{_libdir}/libibverbs*.so.*
%{_libdir}/libibverbs/*.so
%ifnarch s390x s390
%{_libdir}/libefa.so.*
%{_libdir}/libmlx4.so.*
%{_libdir}/libmlx5.so.*
%endif
%config(noreplace) %{_sysconfdir}/libibverbs.d/mlx5.driver
%doc rdma-core-%{version}/installed_docs/libibverbs.md

%files -n libibverbs-utils-ofed
%{_bindir}/ibv_*
%{_mandir}/man1/ibv_*

%files -n ibacm-ofed
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
%doc rdma-core-%{version}/installed_docs/ibacm.md

%if 0
%files -n iwpmd-ofed
%{_sbindir}/iwpmd
%{_unitdir}/iwpmd.service
%config(noreplace) %{_sysconfdir}/rdma/modules/iwpmd.conf
%config(noreplace) %{_sysconfdir}/iwpmd.conf
%{_udevrulesdir}/90-iwpmd.rules
%{_mandir}/man8/iwpmd.*
%{_mandir}/man5/iwpmd.*
%endif

%files -n libibumad-ofed
%{_libdir}/libibumad*.so.*

%files -n librdmacm-ofed
%{_libdir}/librdmacm*.so.*
%dir %{_libdir}/rsocket
%{_libdir}/rsocket/*.so*
%doc rdma-core-%{version}/installed_docs/librdmacm.md
%{_mandir}/man7/rsocket.*

%files -n librdmacm-utils-ofed
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

%files -n srp_daemon-ofed
%config(noreplace) %{_sysconfdir}/srp_daemon.conf
%config(noreplace) %{_sysconfdir}/rdma/modules/srp_daemon.conf
%{_libexecdir}/srp_daemon/start_on_all_ports
%if "%{WITH_SYSTEMD}" == "1"
%{_unitdir}/srp_daemon.service
%{_unitdir}/srp_daemon_port@.service
%else
%{_initddir}/srpd
%{_sbindir}/srp_daemon.sh
%endif
%{_sbindir}/ibsrpdm
%{_sbindir}/srp_daemon
%{_sbindir}/run_srp_daemon
%{_udevrulesdir}/60-srp_daemon.rules
%{_mandir}/man5/srp_daemon.service.5*
%{_mandir}/man5/srp_daemon_port@.service.5*
%{_mandir}/man8/ibsrpdm.8*
%{_mandir}/man8/srp_daemon.8*
%doc rdma-core-%{version}/installed_docs/ibsrpdm.md

%if %{with_pyverbs}
%files -n python3-pyverbs-ofed
%{python3_sitearch}/pyverbs
%doc rdma-core-%{version}/installed_docs/tests
%endif
