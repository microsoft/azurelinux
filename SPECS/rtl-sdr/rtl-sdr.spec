%global __cmake_in_source_build 1
Summary:        SDR utilities for Realtek RTL2832 based DVB-T dongles
Name:           rtl-sdr
Version:        0.6.0
Release:        12%{?dist}
License:        GPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr
Source0:        https://github.com/steve-m/librtlsdr/archive/%{version}/librtlsdr-%{version}.tar.gz
Patch0:         librtlsdr-0.6.0-pkgconfig.patch
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  libusbx-devel
Requires(pre):  glibc-common
Requires(pre):  shadow-utils

%description
This package can turn your RTL2832 based DVB-T dongle into a SDR receiver.

%package devel
Summary:        Development files for rtl-sdr
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for rtl-sdr.

%prep
%setup -q -n librtlsdr-%{version}
%patch0 -p1
rm -f src/getopt/*
rmdir src/getopt

%build
%cmake -DDETACH_KERNEL_DRIVER=ON
%cmake_build

%install
%cmake_install

# remove static libs
rm -f %{buildroot}%{_libdir}/*.a

# Fix udev rules and allow access only to users in rtlsdr group
sed -i 's/MODE:="0666"/GROUP:="rtlsdr", MODE:="0660", ENV{ID_SOFTWARE_RADIO}="1"/' ./rtl-sdr.rules
install -Dpm 644 ./rtl-sdr.rules %{buildroot}%{_libdir}/udev/rules.d/10-rtl-sdr.rules

%pre
getent group rtlsdr >/dev/null || \
  %{_sbindir}/groupadd -r rtlsdr >/dev/null 2>&1
exit 0

%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS
%{_bindir}/*
%{_libdir}/*.so.*
%{_libdir}/udev/rules.d/10-rtl-sdr.rules

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Feb 08 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 0.6.0-12
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- License verified

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug  5 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.0-8
- Fixed FTBFS
  Resolves: rhbz#1865404

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 0.6.0-4
- Use __cmake_in_source_build

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 0.6.0-4
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon Mar 09 2020 Dan Horák <dan[at]danny.cz> - 0.6.0-3
- Fix pkgconfig

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 22 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.0-1
- New version

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr  1 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.4-5
- Simplified URL

* Mon Apr  1 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.4-4
- Fixed indentation
- Added requirement for glibc-common (for getent)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May  7 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.4-1
- New version

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb  1 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.3-7
- Add rtlsdr group as system group
  Resolves: rhbz#1418027

* Tue Mar 29 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.3-6
- Re-introduced rtlsdr group, it's useful for servers
  Resolves: rhbz#1321424

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 29 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.3-3
- Migrated udev rule to dynamic ACL management
- Fixed udev rule location
- Group rtlsdr is no more used / created

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul  1 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 0.5.3-1
- New version
  Resolves: rhbz#1114342
- Dropped rtl-sdr-0-lib64-fix patch (upstreamed)
- Enabled detaching of kernel driver

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.4.20130403git4a068f56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.3.20130403git4a068f56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Apr  7 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0-0.2.20130403git4a068f56
- Preserve timestamp of 10-rtl-sdr.rules during install
- Added isa to devel subpackage requirement
- Removed bundled getopt

* Wed Apr  3 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 0-0.1.20130403git4a068f56
- Initial version
