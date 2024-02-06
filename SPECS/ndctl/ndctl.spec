%{!?_udevdir: %define _udevdir /lib/udev/}
Summary:        Manage "libnvdimm" subsystem devices (Non-volatile Memory)
Name:           ndctl
Version:        78
Release:        1%{?dist}
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
BuildRequires:	meson
BuildRequires:	iniparser-devel

%define asciidoctor -Dasciidoctor=disabled
%define libtracefs -Dlibtracefs=disabled

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

%package libs
Summary:	Management library for "libnvdimm" subsystem devices (Non-volatile Memory)
License:	LGPLv2
Requires:	daxctl-libs%{?_isa} = %{version}-%{release}
 
%description libs
Libraries for %{name}.

%package -n daxctl-libs
Summary:	Management library for "Device DAX" devices
License:	LGPLv2
Conflicts:  daxctl <= 65
 
%description -n daxctl-libs
Device DAX is a facility for establishing DAX mappings of performance /
feature-differentiated memory. daxctl-libs provides an enumeration /
control API for these devices.

%package -n daxctl
Summary:    Manage Device-DAX instances
License:    GPLv2
Group:      System Environment/Base

%description -n daxctl
The daxctl utility provides enumeration and provisioning commands for
the Linux kernel Device-DAX facility. This facility enables DAX mappings
of performance / feature differentiated memory without need of a
filesystem.

%package -n cxl-cli
Summary:	Manage CXL devices
License:	GPLv2
Requires:	cxl-libs%{?_isa} = %{version}-%{release}
 
%description -n cxl-cli
The cxl utility provides enumeration and provisioning commands for
the Linux kernel CXL devices.

%package -n cxl-devel
Summary:	Development files for libcxl
License:	LGPLv2
Requires:	cxl-libs%{?_isa} = %{version}-%{release}
 
%description -n cxl-devel
This package contains libraries and header files for developing applications
that use libcxl, a library for enumerating and communicating with CXL devices.

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

%package -n cxl-libs
Summary:	Management library for CXL devices
License:	LGPLv2
 
%description -n cxl-libs
libcxl is a library for enumerating and communicating with CXL devices.

%prep
%setup -q ndctl-%{version}

%build
%meson %{?asciidoctor} %{?libtracefs} -Dversion-tag=%{version}
%meson_build

%install
%meson_install

%check
%meson_test

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion)

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license LICENSES/preferred/GPL-2.0 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_bindir}/ndctl
%{_mandir}/man1/ndctl*
%{bashcompdir}/ndctl
%{_unitdir}/ndctl-monitor.service
 
%dir %{_sysconfdir}/ndctl
%dir %{_sysconfdir}/ndctl/keys
%{_sysconfdir}/ndctl/keys/keys.readme
 
%{_sysconfdir}/modprobe.d/nvdimm-security.conf
 
%dir %{_sysconfdir}/ndctl.conf.d
%config(noreplace) %{_sysconfdir}/ndctl.conf.d/monitor.conf
%config(noreplace) %{_sysconfdir}/ndctl.conf.d/ndctl.conf

%files -n daxctl-libs
%doc README.md
%license LICENSES/preferred/LGPL-2.1 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_libdir}/libdaxctl.so.*
	
%files -n cxl-libs
%doc README.md
%license LICENSES/preferred/LGPL-2.1 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_libdir}/libcxl.so.*

	
%files libs
%doc README.md
%license LICENSES/preferred/LGPL-2.1 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_libdir}/libndctl.so.*

%files devel
%defattr(-,root,root)
%license LICENSES/preferred/LGPL-2.1
%{_includedir}/ndctl/
%{_libdir}/libndctl.so
%{_libdir}/pkgconfig/libndctl.pc

%files -n daxctl
%defattr(-,root,root)
%license LICENSES/preferred/GPL-2.0 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_bindir}/daxctl
%{_mandir}/man1/daxctl*
	
%{_datadir}/daxctl
%{bashcompdir}/daxctl
%{_unitdir}/daxdev-reconfigure@.service
%config %{_udevrulesdir}/90-daxctl-device.rules
%config(noreplace) %{_sysconfdir}/daxctl.conf.d/daxctl.example.conf

%files -n cxl-cli
%license LICENSES/preferred/GPL-2.0 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_bindir}/cxl
%{_mandir}/man1/cxl*
%{bashcompdir}/cxl
%{_unitdir}/cxl-monitor.service

%files -n daxctl-devel
%defattr(-,root,root)
%license LICENSES/preferred/LGPL-2.1
%{_includedir}/daxctl/
%{_libdir}/libdaxctl.so
%{_libdir}/pkgconfig/libdaxctl.pc

%files -n cxl-devel
%license LICENSES/preferred/LGPL-2.1
%{_includedir}/cxl/
%{_libdir}/libcxl.so
%{_libdir}/pkgconfig/libcxl.pc
%{_mandir}/man3/cxl*
%{_mandir}/man3/libcxl.3*

%changelog
*   Wed Jan 31 2024 Saul Paredes <saulparedes@microsoft.com> - 78-1
-   Update to 78
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
