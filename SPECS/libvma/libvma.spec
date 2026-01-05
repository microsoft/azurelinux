%{!?configure_options: %global configure_options %{nil}}
%{!?use_rel: %global use_rel 1}

%{!?make_build: %global make_build %{__make} %{?_smp_mflags} %{?mflags} V=1}
%{!?run_ldconfig: %global run_ldconfig %{?ldconfig}}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
# Azure Linux build with use_systemd
%global use_systemd 1

Name:           libvma
Version:        9.8.72
Release:        1%{?dist}
Summary:        A library for boosting TCP and UDP traffic (over RDMA hardware)
Group:          System Environment/Libraries
License:        GPLv2 or BSD
Url:            https://github.com/Mellanox/%{name}
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

# libvma currently supports only the following architectures
ExclusiveArch: x86_64 ppc64le ppc64 aarch64

BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gcc-c++
BuildRequires: rdma-core-devel
BuildRequires: libnl3-devel
%if "%{use_systemd}" == "1"
BuildRequires: systemd
%endif
BuildRequires: make

%description
libvma is a LD_PRELOAD-able library that boosts performance of TCP and
UDP traffic. It allows application written over standard socket API to
handle fast path data traffic from user space over Ethernet and/or
Infiniband with full network stack bypass and get better throughput,
latency and packets/sec rate.

No application binary change is required for that.
libvma is supported by RDMA capable devices that support "verbs"
IBV_QPT_RAW_PACKET QP for Ethernet and/or IBV_QPT_UD QP for IPoIB.

%package devel
Summary: Header files required to develop with libvma
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This package includes headers for building programs with libvma's
interfaces.

%package utils
Summary: Utilities used with libvma
Group: System Environment/Libraries
Requires: %{name} = %{version}-%{release}

%description utils
This package contains the tool for collecting and analyzing libvma statistic.

%prep
%setup -q

%build

export CFLAGS="$CFLAGS -Werror=discarded-qualifiers"

if [ ! -e configure ] && [ -e autogen.sh ]; then
    PRJ_RELEASE=%{use_rel} ./autogen.sh
fi

%if %{use_rel} > 0
%configure --enable-opt-log=none --enable-debug \
           %{?configure_options}
%{make_build}
cp -f src/vma/.libs/%{name}.so %{name}-debug.so
%{make_build} clean
%endif

%configure --docdir=%{_pkgdocdir} \
           %{?configure_options}
%{make_build}

%install
%{make_build} DESTDIR=${RPM_BUILD_ROOT} install

find $RPM_BUILD_ROOT%{_libdir} -name '*.la' -delete
%if "%{use_systemd}" == "1"
install -D -m 644 contrib/scripts/vma.service $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/system/vma.service
%endif

%if %{use_rel} > 0
install -m 755 ./%{name}-debug.so $RPM_BUILD_ROOT/%{_libdir}/%{name}-debug.so
%endif

%post
%systemd_post vma.service

%preun
%systemd_preun vma.service

%postun
%systemd_postun_with_restart vma.service

%files
%license LICENSE
%{_libdir}/%{name}.so*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/CHANGES
%config(noreplace) %{_sysconfdir}/libvma.conf
%{_sbindir}/vmad
%if "%{use_systemd}" == "1"
%{_prefix}/lib/systemd/system/vma.service
%endif
%{_mandir}/man7/vma.*
%{_mandir}/man8/vmad.*

%files devel
%dir %{_includedir}/mellanox
%{_includedir}/mellanox/vma_extra.h
%if %{use_rel} > 0
%{_libdir}/%{name}-debug.so
%endif

%files utils
%{_bindir}/vma_stats
%{_mandir}/man8/vma_stats.*

%changelog
* Tue Nov 04 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 9.8.72-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
- Update build with use_systemd=1

* Wed Feb 28 2024 NVIDIA CORPORATION <networking-support@nvidia.com> 9.8.60-1
- Bump version to 9.8.60
- Please refer to CHANGES for full changelog.

