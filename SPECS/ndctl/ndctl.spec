# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:		ndctl
Version:	83
Release:	1%{?dist}
Summary:	Manage "libnvdimm" subsystem devices (Non-volatile Memory)
License:	GPL-2.0-only AND LGPL-2.1-only AND CC0-1.0 AND MIT
Url:		https://github.com/pmem/ndctl
Source0:	https://github.com/pmem/%{name}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

Requires:	ndctl-libs%{?_isa} = %{version}-%{release}
Requires:	daxctl-libs%{?_isa} = %{version}-%{release}
Requires:	cxl-libs%{?_isa} = %{version}-%{release}
BuildRequires:	autoconf
%if 0%{?rhel} && 0%{?rhel} < 9
BuildRequires:	asciidoc
%define asciidoctor -Dasciidoctor=disabled
%define libtracefs -Dlibtracefs=disabled
%else
BuildRequires:	rubygem-asciidoctor
BuildRequires:	libtraceevent-devel
BuildRequires:	libtracefs-devel
%define asciidoctor -Dasciidoctor=enabled
%define libtracefs -Dlibtracefs=enabled
%endif
BuildRequires:	xmlto
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libkmod)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(bash-completion)
BuildRequires:	pkgconfig(systemd)
BuildRequires:	keyutils-libs-devel
BuildRequires:	systemd-rpm-macros
BuildRequires:	iniparser-devel
BuildRequires:	meson

%description
Utility library for managing the "libnvdimm" subsystem.  The "libnvdimm"
subsystem defines a kernel device model and control message interface for
platform NVDIMM resources like those defined by the ACPI 6+ NFIT (NVDIMM
Firmware Interface Table).

%if 0%{?flatpak}
%global _udevrulesdir %{_prefix}/lib/udev/rules.d
%endif

%package -n ndctl-devel
Summary:	Development files for libndctl
License:	LGPL-2.1-only
Requires:	ndctl-libs%{?_isa} = %{version}-%{release}

%description -n ndctl-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package -n daxctl
Summary:	Manage Device-DAX instances
License:	GPL-2.0-only
Requires:	daxctl-libs%{?_isa} = %{version}-%{release}

%description -n daxctl
The daxctl utility provides enumeration and provisioning commands for
the Linux kernel Device-DAX facility. This facility enables DAX mappings
of performance / feature differentiated memory without need of a
filesystem.

%package -n cxl-cli
Summary:	Manage CXL devices
License:	GPL-2.0-only
Requires:	cxl-libs%{?_isa} = %{version}-%{release}

%description -n cxl-cli
The cxl utility provides enumeration and provisioning commands for
the Linux kernel CXL devices.

%package -n cxl-devel
Summary:	Development files for libcxl
License:	LGPL-2.1-only
Requires:	cxl-libs%{?_isa} = %{version}-%{release}

%description -n cxl-devel
This package contains libraries and header files for developing applications
that use libcxl, a library for enumerating and communicating with CXL devices.

%package -n daxctl-devel
Summary:	Development files for libdaxctl
License:	LGPL-2.1-only
Requires:	daxctl-libs%{?_isa} = %{version}-%{release}

%description -n daxctl-devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}, a library for enumerating
"Device DAX" devices.  Device DAX is a facility for establishing DAX
mappings of performance / feature-differentiated memory.


%package -n ndctl-libs
Summary:	Management library for "libnvdimm" subsystem devices (Non-volatile Memory)
License:	LGPL-2.1-only AND CC0-1.0 AND MIT
Requires:	daxctl-libs%{?_isa} = %{version}-%{release}


%description -n ndctl-libs
Libraries for %{name}.

%package -n daxctl-libs
Summary:	Management library for "Device DAX" devices
License:	LGPL-2.1-only AND CC0-1.0 AND MIT

%description -n daxctl-libs
Device DAX is a facility for establishing DAX mappings of performance /
feature-differentiated memory. daxctl-libs provides an enumeration /
control API for these devices.

%package -n cxl-libs
Summary:	Management library for CXL devices
License:	LGPL-2.1-only AND CC0-1.0 AND MIT

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

%ldconfig_scriptlets -n ndctl-libs

%ldconfig_scriptlets -n daxctl-libs

%ldconfig_scriptlets -n cxl-libs

%define bashcompdir %(pkg-config --variable=completionsdir bash-completion)

%pre
if [ -f %{_sysconfdir}/ndctl/monitor.conf ] ; then
  if ! [ -f %{_sysconfdir}/ndctl.conf.d/monitor.conf ] ; then
    cp -a %{_sysconfdir}/ndctl/monitor.conf /var/run/ndctl-monitor.conf-migration
  fi
fi

%post
if [ -f /var/run/ndctl-monitor.conf-migration ] ; then
  config_found=false
  while read line ; do
    [ -n "$line" ] || continue
    case "$line" in
      \#*) continue ;;
    esac
    config_found=true
    break
  done < /var/run/ndctl-monitor.conf-migration
  if $config_found ; then
    echo "[monitor]" > %{_sysconfdir}/ndctl.conf.d/monitor.conf
    cat /var/run/ndctl-monitor.conf-migration >> %{_sysconfdir}/ndctl.conf.d/monitor.conf
  fi
  rm /var/run/ndctl-monitor.conf-migration
fi

%files
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

%files -n daxctl
%license LICENSES/preferred/GPL-2.0 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_bindir}/daxctl
%{_mandir}/man1/daxctl*
%{_datadir}/daxctl
%{bashcompdir}/daxctl
%{_unitdir}/daxdev-reconfigure@.service
%config %{_udevrulesdir}/90-daxctl-device.rules
%dir %{_sysconfdir}/daxctl.conf.d/
%config(noreplace) %{_sysconfdir}/daxctl.conf.d/daxctl.example.conf

%files -n cxl-cli
%license LICENSES/preferred/GPL-2.0 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_bindir}/cxl
%{_mandir}/man1/cxl*
%{bashcompdir}/cxl
%{_unitdir}/cxl-monitor.service

%files -n ndctl-libs
%doc README.md
%license LICENSES/preferred/LGPL-2.1 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_libdir}/libndctl.so.*

%files -n daxctl-libs
%doc README.md
%license LICENSES/preferred/LGPL-2.1 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_libdir}/libdaxctl.so.*

%files -n cxl-libs
%doc README.md
%license LICENSES/preferred/LGPL-2.1 LICENSES/other/MIT LICENSES/other/CC0-1.0
%{_libdir}/libcxl.so.*

%files -n ndctl-devel
%license LICENSES/preferred/LGPL-2.1
%{_includedir}/ndctl/
%{_libdir}/libndctl.so
%{_libdir}/pkgconfig/libndctl.pc

%files -n daxctl-devel
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
* Sat Oct 04 2025 Alison Schofield <alison.schofield@intel.com> - 83-1
- release v83

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 82-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jun 12 2025 Alison Schofield <alison.schofield@intel.com> - 82-1
- release v82

* Tue Apr 01 2025 Alison Schofield <alison.schofield@intel.com> - 81-1
- release v81

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 80-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Oct 11 2024 Alison Schofield <alison.schofield@intel.com> - 80-1
- release v80

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 79-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 David Cantrell <dcantrell@redhat.com> - 79-3
- Rebuild for iniparser-4.2.4

* Thu May 30 2024 Adam Williamson <awilliam@redhat.com> - 79-2
- Rebuild with new iniparser

* Thu May 02 2024 Vishal Verma <vishal.l.verma@intel.com> - 79-1
- release v79

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 78-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 78-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 Vishal Verma <vishal.l.verma@intel.com> - 78-1
- release v78

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 77-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 02 2023 Vishal Verma <vishal.l.verma@intel.com> - 77-1
- release v77

* Fri Feb 24 2023 Vishal Verma <vishal.l.verma@intel.com> - 76.1-1
- release v76.1

* Wed Feb 22 2023 Vishal Verma <vishal.l.verma@intel.com> - 76-1
- release v76

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 75-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 13 2023 Vishal Verma <vishal.l.verma@intel.com> - 75-1
- release v75

* Wed Aug 24 2022 Vishal Verma <vishal.l.verma@intel.com> - 74-1
- release v74

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 73-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Ralf Corsépius <corsepiu@fedoraproject.org> - 73-2
- Address misc. packaging bugs (RHBZ#2100157).
- Fix broken ChangeLog-entry.

* Tue Mar 08 2022 Vishal Verma <vishal.l.verma@intel.com> - 73-1
- release v73

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 72.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Vishal Verma <vishal.l.verma@intel.com> - 72.1-1
- release v72.1

* Sun Dec 19 2021 Vishal Verma <vishal.l.verma@intel.com> - 72-1
- release v72

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 71.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 71.1-3
- Rebuild for versioned symbols in json-c

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 71.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 22 2020 Vishal Verma <vishal.l.verma@intel.com> - 71.1-1
- release v71.1

* Sat Dec 19 2020 Vishal Verma <vishal.l.verma@intel.com> - 71-1
- release v71

* Sat Oct 10 2020 Vishal Verma <vishal.l.verma@intel.com> - 70.1-1
- release v70.1

* Tue Oct 06 2020 Vishal Verma <vishal@stellar.sh> - 70-1
- release v70

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 69-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 23 2020 Vishal Verma <vishal.l.verma@intel.com> - 69-1
- release v69

* Tue Apr 21 2020 Björn Esser <besser82@fedoraproject.org> - 68-2
- Rebuild (json-c)

* Tue Mar 24 2020 Vishal Verma <vishal@stellar.sh> - 68-1
- release v68

* Fri Jan 31 2020 Vishal Verma <vishal.l.verma@intel.com> - 67-3
- Add fix for GCC10 builds

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 28 2019 Vishal Verma <vishal.l.verma@intel.com> - 67-1
- release v67

* Wed Aug 07 2019 Vishal Verma <vishal.l.verma@intel.com> - 66-1
- release v66

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat May 11 2019 Vishal Verma <vishal.l.verma@intel.com> - 65-1
- release v65

* Wed Feb 06 2019 Vishal Verma <vishal.l.verma@intel.com> - 64.1-1
- release v64.1

* Mon Feb 04 2019 Vishal Verma <vishal.l.verma@intel.com> - 64-1
- release v64

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 63-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 05 2018 Vishal Verma <vishal.l.verma@intel.com> - 63-1
- release v63
- remove ndctl-udev and related files

* Tue Aug 14 2018 Vishal Verma <vishal@stellar.sh> - 62-1
- release v62
- Add files for udev and ndctl-monitor

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 61.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Vishal Verma <vishal.l.verma@intel.com> - 61.2-1
- release v61.2

* Tue Jun 26 2018 Vishal Verma <vishal@stellar.sh> - 61.1-1
- release v61.1

* Tue Jun 26 2018 Vishal Verma <vishal@stellar.sh> - 61-1
- new version

* Thu May 17 2018 Dan Williams <dan.j.williams@intel.com> - 60.3-1
- release v60.3

* Mon Apr 23 2018 Dan Williams <dan.j.williams@intel.com> - 60.1-1
- release v60.1

* Thu Apr 19 2018 Dan Williams <dan.j.williams@intel.com> - 60-1
- release v60

* Tue Mar 27 2018 Dan Williams <dan.j.williams@intel.com> - 59.3-1
- release v59.3

* Tue Mar 06 2018 Björn Esser <besser82@fedoraproject.org> - 59.2-2
- Rebuilt for libjson-c.so.4 (json-c v0.13.1)

* Fri Feb 09 2018 Dan Williams <dan.j.williams@intel.com> - 59.2-1
- release v59.2

* Fri Feb 09 2018 Dan Williams <dan.j.williams@intel.com> - 59.1-1
- release v59.1

* Fri Feb 09 2018 Dan Williams <dan.j.williams@intel.com> - 59-1
- release v59

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 58.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 10 2017 Björn Esser <besser82@fedoraproject.org> - 58.4-2
- Rebuilt for libjson-c.so.3

* Thu Nov 16 2017 Dan Williams <dan.j.williams@intel.com> - 58.4-1
- release v58.4

* Thu Sep 21 2017 Dan Williams <dan.j.williams@intel.com> - 58.2-1
- release v58.2

* Fri Sep 08 2017 Dan Williams <dan.j.williams@intel.com> - 58.1-2
- gate libpmem dependency on x86_64

* Fri Sep 08 2017 Dan Williams <dan.j.williams@intel.com> - 58.1-1
- add libpmem dependency
- release v58.1

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 57.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Dan Williams <dan.j.williams@intel.com> - 57.1-1
- Release v57.1

* Sat May 27 2017 Dan Williams <dan.j.williams@intel.com> - 57-1
- Release v57

* Fri Feb 10 2017 Dan Williams <dan.j.williams@intel.com> - 56-1
- Release v56

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Oct 21 2016 Dan Williams <dan.j.williams@intel.com> - 55-1
- release v55

* Fri Aug 05 2016 Dan Williams <dan.j.williams@intel.com> - 54-1
- add explicit lib version dependencies

* Sat May 28 2016 Dan Williams <dan.j.williams@intel.com> - 53.1-1
- Fix up tag format vs source url confusion

* Fri May 27 2016 Dan Williams <dan.j.williams@intel.com> - 53-1
- add daxctl-libs + daxctl-devel packages
- add bash completion

* Mon Apr 04 2016 Dan Williams <dan.j.williams@intel.com> - 52-1
- Initial rpm submission to Fedora
