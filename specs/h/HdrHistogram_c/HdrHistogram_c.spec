# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: HdrHistogram_c
Version: 0.11.8
Release: 8%{?dist}
Summary: C port of the HdrHistogram 
License: BSD-2-Clause
URL: https://github.com/HdrHistogram/%{name}
Source0: https://github.com/HdrHistogram/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc g++ cmake zlib-devel

%description
C port of High Dynamic Range (HDR) Histogram.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -n %{name}-%{version}


%build
%cmake -DHDR_HISTOGRAM_INSTALL_STATIC=OFF .
%cmake_build


%check
%ctest


%install
rm -rf $RPM_BUILD_ROOT
%cmake_install
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT

%ldconfig_post

%ldconfig_postun


%files
%license LICENSE.txt
%doc README.md
%exclude %{_bindir}/*
%{_libdir}/libhdr_histogram.so.6.1.3
%{_libdir}/libhdr_histogram.so.6

%files devel
%dir %{_includedir}/hdr
%{_includedir}/hdr/hdr_thread.h
%{_includedir}/hdr/hdr_interval_recorder.h
%{_includedir}/hdr/hdr_writer_reader_phaser.h
%{_includedir}/hdr/hdr_time.h
%{_includedir}/hdr/hdr_histogram_version.h
%{_includedir}/hdr/hdr_histogram_log.h
%{_includedir}/hdr/hdr_histogram.h
%{_libdir}/libhdr_histogram.so
%{_libdir}/cmake/hdr_histogram/*.cmake
%{_libdir}/pkgconfig/hdr_histogram.pc


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 12 2023 Nathan Scott <nathans@redhat.com> - 0.11.8-1
- Update to latest upstream version.
- Update spec file and resolve a build issue (BZ 2113091).
- Switch to SPDX licensing.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jan 25 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Lukas Zapletal <lzap+rpm@redhat.com> - 0.11.0-1
- New upstream version

* Wed Apr 29 2020 Nathan Scott <nathans@redhat.com> - 0.9.13-1
- New upstream version

* Wed Feb 12 2020 Lukas Zapletal <lzap+rpm@redhat.com> - 0.9.12-1
- New upstream version

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 14 2019 Lukáš Zapletal 0.9.11-1
- Initial package version
