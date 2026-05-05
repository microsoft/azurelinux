%{!?configure_options: %global configure_options --disable-lto}
%{!?use_rel: %global use_rel 1}

%{!?make_build: %global make_build %{__make} %{?_smp_mflags} %{?mflags} V=1}
%{!?run_ldconfig: %global run_ldconfig %{?ldconfig}}
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
%global use_systemd %(if command -v systemctl >/dev/null 2>&1; then echo -n '1'; else echo -n '0'; fi)

Name: libxlio
Version: 3.60.4
Release:        1%{?dist}
Summary: A library for boosting TCP and UDP traffic (over RDMA hardware)
%if 0%{?rhl}%{?fedora} == 0
Group: System Environment/Libraries
%endif

License: GPLv2 or BSD
Vendor:          Microsoft Corporation
Distribution:    Azure Linux
Url: https://github.com/Mellanox/%{name}
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.2.2/SOURCES/mlnx_ofed/OFED-internal-25.10-2.4.1.tgz
Source0:         %{_distro_sources_url}/libxlio-3.60.4.tar.gz
Patch0:          fix-recvmmsg-const-timespec.patch

# library currently supports only the following architectures
ExclusiveArch: x86_64 ppc64le ppc64 aarch64

BuildRequires: pkgconfig
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: libtool
BuildRequires: gcc-c++
BuildRequires: rdma-core-devel
BuildRequires: dpcp
%if "%{use_systemd}" == "1"
%if 0%{?rhel} >= 9 || 0%{?fedora} >= 30 || 0%{?suse_version} >= 1210
BuildRequires: systemd-rpm-macros
%{?systemd_requires}
%else
BuildRequires: systemd
%endif
%endif
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 24 || 0%{?suse_version} >= 1500 || 0%{?azl}
BuildRequires: pkgconfig(libnl-3.0)
BuildRequires: pkgconfig(libnl-route-3.0)
%endif
BuildRequires: make

%description
libxlio is a LD_PRELOAD-able library that boosts performance of TCP and
UDP traffic. It allows application written over standard socket API to
handle fast path data traffic from user space over Ethernet and/or
Infiniband with full network stack bypass and get better throughput,
latency and packets/sec rate.

No application binary change is required for that.
library is supported by RDMA capable devices that support "verbs"
IBV_QPT_RAW_PACKET QP for Ethernet and/or IBV_QPT_UD QP for IPoIB.

%package devel
Summary: Header files required to develop with libxlio
%if 0%{?rhl}%{?fedora} == 0
Group: System Environment/Libraries
%endif
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package includes headers for building programs with libxlio's
interfaces.

%package utils
Summary: Utilities used with libxlio
%if 0%{?rhl}%{?fedora} == 0
Group: System Environment/Libraries
%endif
Requires: %{name}%{?_isa} = %{version}-%{release}

%description utils
This package contains the tool for collecting and analyzing libxlio statistic.

%prep
%setup -q
%patch0 -p0

%build
if [ ! -e configure ] && [ -e autogen.sh ]; then
    PRJ_RELEASE=%{use_rel} ./autogen.sh
fi

%if %{use_rel} > 0
%configure --enable-opt-log=none --enable-debug \
           %{?configure_options}
%{make_build}
cp -f src/core/.libs/%{name}.so %{name}-debug.so
%{make_build} clean
%endif

%configure --enable-opt-log=high --docdir=%{_pkgdocdir} \
           %{?configure_options}
%{make_build}

%install
%{make_build} DESTDIR=${RPM_BUILD_ROOT} install

find $RPM_BUILD_ROOT%{_libdir} -name '*.la' -delete
%if "%{use_systemd}" == "1"
install -D -m 644 contrib/scripts/xlio.service $RPM_BUILD_ROOT/%{_prefix}/lib/systemd/system/xlio.service
%endif

%if %{use_rel} > 0
install -m 755 ./%{name}-debug.so $RPM_BUILD_ROOT/%{_libdir}/%{name}-debug.so
%endif

%post
%if 0%{?fedora} || 0%{?rhel} > 7
# https://fedoraproject.org/wiki/Changes/Removing_ldconfig_scriptlets
%else
%{run_ldconfig}
%endif
if [ $1 = 1 ]; then
    if command -v systemctl >/dev/null 2>&1; then
        %if 0%{?systemd_post:1} || 0%{?service_add_post:1}
            %if 0%{?service_add_post:1}
            %service_add_post xlio.service
            %else
            %systemd_post xlio.service
            %endif
        %else
            systemctl --no-reload enable xlio.service >/dev/null 2>&1 || true
        %endif
    fi
fi

%preun
if [ $1 = 0 ]; then
    if command -v systemctl >/dev/null 2>&1; then
        %if 0%{?systemd_preun:1} || 0%{?service_del_preun:1}
            %if 0%{?service_del_preun:1}
            %service_del_preun xlio.service
            %else
            %systemd_preun xlio.service
            %endif
        %else
            systemctl --no-reload disable xlio.service >/dev/null 2>&1 || true
            systemctl stop xlio.service || true
        %endif
    fi
fi

%postun
%if 0%{?fedora} || 0%{?rhel} > 7
# https://fedoraproject.org/wiki/Changes/Removing_ldconfig_scriptlets
%else
%{run_ldconfig}
%endif
if command -v systemctl >/dev/null 2>&1; then
        %if 0%{?systemd_postun_with_restart:1} || 0%{?service_del_postun:1}
            %if 0%{?service_del_postun:1}
            %service_del_postun xlio.service
            %else
            %systemd_postun_with_restart xlio.service
            %endif
        %else
            systemctl --system daemon-reload >/dev/null 2>&1 || true
        %endif
fi

%files
%{_libdir}/%{name}.so*
%dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README
%doc %{_pkgdocdir}/CHANGES
%config(noreplace) %{_sysconfdir}/xlio_config_schema.json
%config(noreplace) %{_sysconfdir}/libxlio_config.json
%{_sbindir}/xliod
%if "%{use_systemd}" == "1"
%{_prefix}/lib/systemd/system/xlio.service
%endif
%{_mandir}/man7/xlio.*
%{_mandir}/man8/xliod.*
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 24 || 0%{?suse_version} >= 1500
%license LICENSE
%endif

%files devel
%dir %{_includedir}/mellanox
%{_includedir}/mellanox/xlio_extra.h
%{_includedir}/mellanox/xlio_types.h
%{_includedir}/mellanox/xlio.h
%if %{use_rel} > 0
%{_libdir}/%{name}-debug.so
%endif

%files utils
%{_bindir}/xlio_stats
%{_mandir}/man8/xlio_stats.*

%changelog
* Thu Apr 17 2026 Azure Linux Team - 3.60.4-1
- Initial Azure Linux import from NVIDIA (license: GPLv2 or BSD)
- License verified
