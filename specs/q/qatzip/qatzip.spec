# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT

%global githubname QATzip
%global libqatzip_soversion 3

Name:           qatzip
Version:        1.3.1
Release: 3%{?dist}
Summary:        Intel QuickAssist Technology (QAT) QATzip Library
License:        BSD-3-Clause
URL:            https://github.com/intel/%{githubname}
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  gcc >= 4.8.5
BuildRequires:  zlib-devel >= 1.2.7
BuildRequires:  qatlib-devel >= 23.08.0
BuildRequires:  autoconf automake libtool make lz4-devel numactl-devel
# The purpose of the package is to support hardware that only exists on x86_64 platforms
# https://bugzilla.redhat.com/show_bug.cgi?id=1987280
ExclusiveArch:  x86_64

%description
QATzip is a user space library which builds on top of the Intel
QuickAssist Technology user space library, to provide extended
accelerated compression and decompression services by offloading the
actual compression and decompression request(s) to the Intel Chipset
Series. QATzip produces data using the standard gzip* format
(RFC1952) with extended headers. The data can be decompressed with a
compliant gzip* implementation. QATzip is designed to take full
advantage of the performance provided by Intel QuickAssist
Technology.

%package        libs
Summary:        Libraries for the qatzip package

%description    libs
This package contains libraries for applications to use
the QATzip APIs.

%package        devel
Summary:        Development components for the libqatzip package
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    devel
This package contains headers and libraries required to build
applications that use the QATzip APIs.

%prep
%autosetup -n %{githubname}-%{version}

%build
%set_build_flags

autoreconf -vif
./configure \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --prefix=%{_prefix} \
    --enable-symbol

%make_build

%install
%make_install
rm %{buildroot}/%{_libdir}/libqatzip.a
rm %{buildroot}/%{_libdir}/libqatzip.la
rm -vf %{buildroot}%{_mandir}/*.pdf

# Check section is not available for these functional and performance tests require special hardware.

%files
%license LICENSE*
%{_mandir}/man1/qzip.1*
%{_bindir}/qzip
%{_bindir}/qatzip-test

%files libs
%license LICENSE*
%{_libdir}/libqatzip.so.%{libqatzip_soversion}*

%files devel
%doc docs/QATzip-man.pdf
%{_includedir}/qatzip.h
%{_libdir}/libqatzip.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Apr 25 2025 Vladis Dronov <vdronov@redhat.com> - 1.3.1-1
- Update to qatzip 1.3.1 @ 10dbadba
- Fix qatzip docker file build broken issue
- Support Latency sensitive mode for qatzip
- Add a suit of comp/decomp API to support Async offloading
- Support zlib format and end of stream flag
- Fix some bugs

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Mar 19 2024 taorong <taorong.jian@intel.com> - 1.2.0-1
- Update to qatzip v1.2.0
- Add qatzip-test tool
- SW fallback
- Fix some bugs

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 08 2023 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 1.1.2-3
- Rebuilt for qatlib 23.08

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Mar 06 2023 xinghong <xinghong.chen@intel.com> - 1.1.2-1
- Update to qatzip v1.1.2
- Update README, update driver configure files
- Fix some bugs

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Vladis Dronov <vdronov@redhat.com> - 1.1.1-1
- Update to qatzip v1.1.1
- Add support for pkgconfig

* Thu Nov 24 2022 Vladis Dronov <vdronov@redhat.com> - 1.1.0-1
- Rebuild for qatzip v1.1.0

* Mon Aug 08 2022 Vladis Dronov <vdronov@redhat.com> - 1.0.9-1
- Rebuild for qatzip v1.0.9
- Update to require qatlib-devel >= 22.07.0 due to soversion bump

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Feb 09 2022 Vladis Dronov <vdronov@redhat.com> - 1.0.7-1
- Rebuild for qatzip v1.0.7
- Fix snprintf truncation check (bz 2046925)
- Add -fstack-protector-strong build option (bz 2044889)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Sep 13 2021 zm627 <zheng.ma@intel.com> - 1.0.6-3
- Rebuild for qatzip v1.0.6

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.6-2
- Upload new qatzip source package and rebuild

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.6-1
- Update to latest qatlib and qatzip upstream release

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.5-3
- Add ExcludeArch ticket number

* Sun Sep 12 2021 zm627 <zheng.ma@intel.com> - 1.0.5-2
- Rebuilt for qatlib v21.08

* Tue Jul 13 2021 Ma Zheng <zheng.ma@intel.com> - 1.0.5-1
- Initial version of RPM Package
