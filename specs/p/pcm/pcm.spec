# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           pcm
Version:        202509
Release: 2%{?dist}
Summary:        Intel(r) Performance Counter Monitor
License:        BSD-3-Clause
Url:            https://github.com/intel/pcm
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  cmake
BuildRequires:  systemd
BuildRequires:  openssl-devel
ExclusiveArch:  %{ix86} x86_64

%description

Intel(r) Performance Counter Monitor (Intel(r) PCM) is an application
programming interface (API) and a set of tools based on the API to
monitor performance and energy metrics of Intel(r) Core(tm), Xeon(r),
Atom(tm) and Xeon Phi(tm) processors. PCM works on Linux, Windows,
Mac OS X, FreeBSD and DragonFlyBSD operating systems.

%prep
%autosetup

%build
%set_build_flags
cat src/CMakeLists.txt | sed 's/CMAKE_INSTALL_SBINDIR/CMAKE_INSTALL_BINDIR/g' > src/CMakeLists.txt.no-sbin
mv src/CMakeLists.txt.no-sbin src/CMakeLists.txt
cat src/pcm-sensor-server.service.in | sed 's/CMAKE_INSTALL_SBINDIR/CMAKE_INSTALL_BINDIR/g' > src/pcm-sensor-server.service.in.no-sbin
mv src/pcm-sensor-server.service.in.no-sbin src/pcm-sensor-server.service.in
%cmake -DCMAKE_BUILD_TYPE=CUSTOM -DLINUX_SYSTEMD=TRUE -DLINUX_SYSTEMD_UNITDIR=%{_unitdir}/
%cmake_build

%install
%cmake_install
rm -rf %{buildroot}/usr/share/doc/PCM/*.md
rm -rf %{buildroot}/usr/share/doc/PCM/*.txt

%files
%license LICENSE
%doc doc/LINUX_HOWTO.txt README.md doc/FAQ.md doc/CUSTOM-COMPILE-OPTIONS.md doc/ENVVAR_README.md doc/PCM-EXPORTER.md doc/PCM-SENSOR-SERVER-README.md doc/PCM_RAW_README.md doc/DOCKER_README.md doc/license.txt doc/LATENCY-OPTIMIZED-MODE.md doc/PCM_IIO_README.md
%{_sbindir}/%{name}-core
%{_sbindir}/%{name}-iio
%{_sbindir}/%{name}-latency
%{_sbindir}/%{name}-memory
%{_sbindir}/%{name}-msr
%{_sbindir}/%{name}-mmio
%{_sbindir}/%{name}-tpmi
%{_sbindir}/%{name}-numa
%{_sbindir}/%{name}-accel
%{_sbindir}/%{name}-pcicfg
%{_sbindir}/%{name}-pcie
%{_sbindir}/%{name}-power
%{_sbindir}/%{name}-sensor
%{_sbindir}/%{name}-sensor-server
%{_sbindir}/%{name}-tsx
%{_sbindir}/%{name}-raw
%{_sbindir}/%{name}
%{_bindir}/%{name}-client
%{_sbindir}/%{name}-daemon
%{_sbindir}/%{name}-bw-histogram
%{_datadir}/%{name}/
%{_unitdir}/%{name}-sensor-server.service

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 202509-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 202502-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 202409-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 202405-2
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 202405-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 202311-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 202311-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 202307-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Mar 05 2023 Felix Wang <topazus@outlook.com> - 202302-1
- Update to version 202302

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 202212-1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 23 2022 Roman Dementiev <roman.dementiev@intel.com> 0.1-11
- Update to version 202212

* Thu Nov 24 2022 Roman Dementiev <roman.dementiev@intel.com> 0.1-10
- Update to new upstream repository location and the name
- Update to version 202211

* Tue Jul 26 2022 Roman Dementiev <roman.dementiev@intel.com> 0.1-9
- Update to version 202207

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 202205-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 202112-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jul 26 2021 Roman Dementiev <roman.dementiev@intel.com> 0.1-8
- Update to version 202107
- Add pcm-mmio utility to rpm spec

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 202105-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Apr 13 2021 Roman Dementiev <roman.dementiev@intel.com> 0.1-7
- Implement suggestions from Fedora review.

* Fri Mar 26 2021 William Cohen <wcohen@redhat.com> 0.1-6
- Clean up pcm.spec.

* Tue Aug 25 2020 Roman Dementiev <roman.dementiev@intel.com> 0.1-5
- Add pcm-raw under %files

* Wed Apr 01 2020 Otto Bruggeman <otto.g.bruggeman@intel.com> 0.1-4
- Add pcm-sensor-server under %files

* Mon Nov 25 2019 Roman Dementiev <roman.dementiev@intel.com> 0.1-3
- call make install and use %{_sbindir} or %{_bindir}

* Mon Oct 21 2019 Roman Dementiev <roman.dementiev@intel.com> 0.1-2
- add opCode file to /usr/share/pcm
- use "install" to copy pcm-bw-histogram.sh

* Fri Oct 18 2019 Roman Dementiev <roman.dementiev@intel.com> 0.1-1
- created spec file

