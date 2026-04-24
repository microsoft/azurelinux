# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global	project_name	idxd-config

Name:		accel-config
Version:	4.1.8
Release: 12%{?dist}
Summary:	Configure accelerator subsystem devices
License:	GPL-2.0-only
URL:		https://github.com/intel/%{project_name}
Source0:	%{URL}/archive/%{name}-v%{version}.tar.gz

Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires:	gcc
BuildRequires:	autoconf
BuildRequires:	asciidoc
BuildRequires:	xmlto
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libkmod)
BuildRequires:	pkgconfig(uuid)
BuildRequires:	pkgconfig(json-c)
BuildRequires:	pkgconfig(libudev)
BuildRequires:	systemd
BuildRequires: make

# accel-config is for configuring Intel DSA (Data-Streaming
# Accelerator) subsystem in the Linux kernel. It supports x86_64 only.
ExclusiveArch:	%{ix86} x86_64

%description
Utility library for configuring the accelerator subsystem.

%package devel
Summary:	Development files for libaccfg
License:	LGPL-2.1-only
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package libs
Summary:	Configuration library for accelerator subsystem devices
License:	LGPL-2.1-only
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description libs
Libraries for %{name}.

%prep
%autosetup -n %{project_name}-%{name}-v%{version}

%build
echo %{version} > version
./autogen.sh
%configure --disable-static --disable-silent-rules
%make_build

%install
%make_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

%check
make check

%files
%license Documentation/COPYING licenses/BSD-MIT licenses/CC0
%license licenses/accel-config-licenses LICENSE_GPL_2_0
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%{_sysconfdir}/%{name}/contrib/configs/*

%files libs
%doc README.md
%license Documentation/COPYING licenses/BSD-MIT licenses/CC0
%license licenses/accel-config-licenses accfg/lib/LICENSE_LGPL_2_1
%{_libdir}/lib%{name}.so.*

%files devel
%license Documentation/COPYING
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/lib%{name}.pc

%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 09 2025 Jun Miao <jun.miao@intel.com> - 4.1.8-9
- Update to v4.1.8 release

* Sun Jul 28 2024 Jun Miao <jun.miao@intel.com> - 4.1.6-8
- Update to v4.1.7 release

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 05 2024 Jun Miao <jun.miao@intel.com> - 4.1.2-6
- Update to v4.1.6 release

* Sun Mar 03 2024 Jun Miao <jun.miao@intel.com> - 4.1.2-5
- Update to v4.1.2 release

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Oct 10 2023 Jun Miao <jun.miao@intel.com> - 4.1.1-2
- Update to v4.1.1 release

* Tue Sep 26 2023 Jun Miao <jun.miao@intel.com> - 4.1-1
- Update to v4.1 release

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Jerry Snitselaar <jsnitsel@redhat.com> - 4.0-2
- Update spec file to use SPDX identifiers

* Sun Apr 23 2023 Jun Miao <jun.miao@intel.com> - 4.0-1
- Update to v4.0 release

* Mon Feb 27 2023 Jun Miao <jun.miao@intel.com> - 3.5.3-1
- Update to v3.5.3 release

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Dec 04 2022 Jun Miao <jun.miao@intel.com> - 3.5.2-3
- Update to v3.5.2 release

* Tue Nov 29 2022 Jun Miao <jun.miao@intel.com> - 3.5.1-2
- Update to v3.5.1 release

* Tue Oct 25 2022 Jun Miao <jun.miao@intel.com> - 3.5.0-1
- Update to v3.5.0 release

* Mon Sep 26 2022 Jun Miao <jun.miao@intel.com> - 3.4.8-2
- Update to v3.4.8 release

* Wed Aug 31 2022 Jun Miao <jun.miao@intel.com> - 3.4.7-1
- Update to v3.4.7 release

* Tue Aug 23 2022 Jun Miao <jun.miao@intel.com> - 3.4.6.5-4
- Update to v3.4.6.5 release

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 06 2022 Jun Miao <jun.miao@intel.com> - 3.4.6.4-2
- Update to v3.4.6.4 release

* Wed Apr 20 2022 Jun Miao <jun.miao@intel.com> - 3.4.6.3-1
- Update to v3.4.6.3 release

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Dec 22 2021 Yunying Sun <yunying.sun@intel.com> - 3.4.4-1
- Updated to 3.4.4 release
- Added several config example files to package under contrib/configs

* Wed Sep 29 2021 Yunying Sun <yunying.sun@intel.com> - 3.4.2-1
- Updated to 3.4.2 release

* Fri Aug 13 2021 Yunying Sun <yunying.sun@intel.com> - 3.4.1-1
- Updated to 3.4.1 release

* Thu Jul 29 2021 Yunying Sun <yunying.sun@intel.com> - 3.4-1
- Updated to 3.4 release

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Björn Esser <besser82@fedoraproject.org> - 3.2-2
- Rebuild for versioned symbols in json-c

* Mon Jun 7 2021 Yunying Sun <yunying.sun@intel.com> - 3.2-1
- Updated to 3.2 release

* Mon Mar 29 2021 Yunying Sun <yunying.sun@intel.com> - 3.1-1
- Added ix86 support back as 3.1 release fixed it
- Updated to 3.1 release

* Thu Feb 18 2021 Yunying Sun <yunying.sun@intel.com> - 3.0.1-1
- Updated to 3.0.1 release
- Removed ix86 support as so far it supports x86_64 only
- Updated licenses following upstream

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 6 2020 Yunying Sun <yunying.sun@intel.com> - 2.8-1
- Initial Packaging
