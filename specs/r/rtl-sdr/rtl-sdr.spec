# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global __cmake_in_source_build 1
#%%global git_commit 1261fbb285297da08f4620b18871b6d6d9ec2a7b
#%%global git_date 20230921

#%%global git_short_commit %%(echo %%{git_commit} | cut -c -8)
#%%global git_suffix %%{git_date}git%%{git_short_commit}

# git clone git://git.osmocom.org/gr-osmosdr
# cd %%{name}
# git archive --format=tar --prefix=%%{name}-%%{version}/ %%{git_commit} | \
# bzip2 > ../%%{name}-%%{version}-%%{git_suffix}.tar.bz2

Name:             rtl-sdr
URL:              http://sdr.osmocom.org/trac/wiki/rtl-sdr
#Version:          0.6.0^%%{git_suffix}
Version:          2.0.1
Release:          6%{?dist}
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:          GPL-2.0-or-later
BuildRequires:    gcc
BuildRequires:    cmake
BuildRequires:    libusbx-devel
#BuildRequires:    libusb1-devel
Requires(pre):    glibc-common
Summary:          SDR utilities for Realtek RTL2832 based DVB-T dongles
#Source0:          https://github.com/steve-m/librtlsdr/archive/%%{git_commit}/librtlsdr-%%{git_commit}.tar.gz
Source0:          https://github.com/steve-m/librtlsdr/archive/refs/tags/v%{version}/librtlsdr-%{version}.tar.gz
#Source0:          https://github.com/steve-m/librtlsdr/archive/%%{version}/librtlsdr-%%{version}.tar.gz
# https://osmocom.org/projects/rtl-sdr/repository/revisions/222517b506278178ab93182d79ccf7eb04d107ce

%description
This package can turn your RTL2832 based DVB-T dongle into a SDR receiver.

%package devel
Summary:          Development files for rtl-sdr
Requires:         %{name}%{?_isa} = %{version}-%{release}
Requires:         cmake-filesystem

%description devel
Development files for rtl-sdr.

%prep
#%%autosetup -p1 -n librtlsdr-%%{git_commit}
%autosetup -p1 -n librtlsdr-%{version}
rm -f src/getopt/*
rmdir src/getopt

# Create a sysusers.d config file
cat >rtl-sdr.sysusers.conf <<EOF
g rtlsdr -
EOF

%build
%cmake -DDETACH_KERNEL_DRIVER=ON
%cmake_build

%install
%cmake_install

# remove static libs
rm -f %{buildroot}%{_libdir}/*.a

# Fix udev rules and allow access only to users in rtlsdr group
sed -i 's/GROUP="plugdev"/GROUP="rtlsdr"/' ./rtl-sdr.rules
install -Dpm 644 ./rtl-sdr.rules %{buildroot}%{_prefix}/lib/udev/rules.d/10-rtl-sdr.rules

install -m0644 -D rtl-sdr.sysusers.conf %{buildroot}%{_sysusersdir}/rtl-sdr.conf


%ldconfig_scriptlets

%files
%license COPYING
%doc AUTHORS
%{_bindir}/*
%{_libdir}/*.so.*
%{_prefix}/lib/udev/rules.d/10-rtl-sdr.rules
%{_sysusersdir}/rtl-sdr.conf

%files devel
%{_includedir}/*
%{_libdir}/cmake/rtlsdr
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.1-5
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul  26 2024 Miroslav Suchý <msuchy@redhat.com> - 2.0.1-3
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Apr  4 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 2.0.1-1
- New version
  Resolves: rhbz#2272629

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0^20230921git1261fbb2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0^20230921git1261fbb2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 21 2023 Daniel Rusek <mail@asciiwolf.com> - 0.6.0^20230921git1261fbb2-1
- Updated to latest commit adding rtl-sdr blog v4 support

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0^20230403git142325a9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Apr 13 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.0^20230403git142325a9-2
- Fixed device group to be rtlsdr
  Resolves: rhbz#2186090

* Mon Apr  3 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 0.6.0^20230403git142325a9-1
- New snapshot

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

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
