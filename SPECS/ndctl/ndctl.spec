%{!?_udevdir: %define _udevdir /lib/udev/}
Summary:        Manage "libnvdimm" subsystem devices (Non-volatile Memory)
Name:           ndctl
Version:        65
Release:        3%{?dist}
License:        LGPLv2
Group:          System Environment/Base
Url:            https://github.com/pmem/ndctl
Source0:        https://github.com/pmem/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  asciidoc
BuildRequires:  which
BuildRequires:  xmlto
BuildRequires:  libtool
BuildRequires:  pkg-config
BuildRequires:  kmod-devel
BuildRequires:  systemd-devel
BuildRequires:  json-c-devel
BuildRequires:  bash-completion-devel
BuildRequires:  keyutils-devel

%description
Utility library for managing the "libnvdimm" subsystem.  The "libnvdimm"
subsystem defines a kernel device model and control message interface for
platform NVDIMM resources.

%package    devel
Summary:    Development files for ndctl
License:    LGPLv2
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n daxctl
Summary:    Manage Device-DAX instances
License:    GPLv2
Group:      System Environment/Base

%description -n daxctl
The daxctl utility provides enumeration and provisioning commands for
the Linux kernel Device-DAX facility. This facility enables DAX mappings
of performance / feature differentiated memory without need of a
filesystem.

%package -n daxctl-devel
Summary:    Development files for daxctl
License:    LGPLv2
Group:      Development/Libraries
Requires:   daxctl = %{version}-%{release}

%description -n daxctl-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}, a library for enumerating
"Device DAX" devices.  Device DAX is a facility for establishing DAX
mappings of performance / feature-differentiated memory.

%prep
%setup -q ndctl-%{version}

%build
./autogen.sh
%configure \
    --disable-static  \
    --enable-local    \
    --disable-docs
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
find %{buildroot} -name '*.la' -delete

%check
make check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license util/COPYING licenses/BSD-MIT licenses/CC0
%{_bindir}/ndctl
%{_libdir}/libndctl.so.*
%{_datadir}/bash-completion/
%{_sysconfdir}/ndctl/*
%{_sysconfdir}/modprobe.d/nvdimm-security.conf
%{_unitdir}/ndctl-monitor.service

%files devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/ndctl/
%{_libdir}/libndctl.so
%{_libdir}/pkgconfig/libndctl.pc

%files -n daxctl
%defattr(-,root,root)
%license util/COPYING licenses/BSD-MIT licenses/CC0
%{_bindir}/daxctl
%{_libdir}/libdaxctl.so.*
%{_datadir}/daxctl/daxctl.conf

%files -n daxctl-devel
%defattr(-,root,root)
%license COPYING
%{_includedir}/daxctl/
%{_libdir}/libdaxctl.so
%{_libdir}/pkgconfig/libdaxctl.pc

%changelog
*   Mon Apr 11 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 65-3
-   Fixing invalid source URL.
*   Wed Mar 16 2022 Andrew Phelps <anphel@microsoft.com> 65-2
-   License verified.
*   Tue Mar 17 2020 Henry Beberman <henry.beberman@microsoft.com> 65-1
-   Update to 65. Remove udev rules reverted in release 63. License fixed.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 62-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Sep 12 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 62-1
-   Upgrade to v62
*   Fri Jun 23 2017 Xiaolin Li <xiaolinl@vmware.com> 56-3
-   Add kmod-devel to BuildRequires
*   Mon Apr 24 2017 Dheeraj Shetty <dheerajs@vmware.com> 56-2
-   Removing the Requires section
*   Thu Apr 06 2017 Dheeraj Shetty <dheerajs@vmware.com> 56-1
-   Initial build.  First version