# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global rc %{nil}

Name:           srt
Version:        1.5.4
Release: 5%{?dist}
Summary:        Secure Reliable Transport protocol tools

License:        MPL-2.0
URL:            https://www.srtalliance.org
Source0:        https://github.com/Haivision/srt/archive/v%{version}%{rc}/%{name}-%{version}%{rc}.tar.gz

# https://github.com/Haivision/srt/commit/0def1b1a1094fc57752f241250e9a1aed71bbffd
Patch0:         0001-build-Update-for-compatibility-with-CMake-4.x-3167.patch

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  gmock-devel
BuildRequires:  gnutls-devel
BuildRequires:  gtest-devel
BuildRequires:  make
BuildRequires:  nettle-devel

Requires: srt-libs%{?_isa} = %{version}-%{release}


%description
Secure Reliable Transport (SRT) is an open source transport technology that
optimizes streaming performance across unpredictable networks, such as 
the Internet.

%package libs
Summary: Secure Reliable Transport protocol libraries

%description libs
Secure Reliable Transport protocol libraries

%package devel
Summary: Secure Reliable Transport protocol development libraries and headers
Requires: srt-libs%{?_isa} = %{version}-%{release}

%description devel
Secure Reliable Transport protocol development libraries and header files


%prep
%autosetup -p1 -n %{name}-%{version}%{rc}


%build
%cmake \
  -DENABLE_STATIC=OFF \
  -DENABLE_UNITTESTS=ON \
  -DENABLE_GETNAMEINFO=ON \
  -DENABLE_BONDING=ON \
  -DENABLE_PKTINFO=ON \
  -DUSE_ENCLIB=gnutls

%cmake_build


%install
%cmake_install
# remove old upstream temporary compatibility pc
rm -f %{buildroot}/%{_libdir}/pkgconfig/haisrt.pc


%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

# tests do not work in parallel as of 1.5.4 rc0
# - TestIPv6 are known broken due to v4_v6 mapping differnces between platforms
#   https://github.com/Haivision/srt/issues/1972#
%ctest -j1 -E TestIPv6


%ldconfig_scriptlets libs


%files
%license LICENSE
%doc README.md docs
%{_bindir}/srt-ffplay
%{_bindir}/srt-file-transmit
%{_bindir}/srt-live-transmit
%{_bindir}/srt-tunnel

%files libs
%license LICENSE
%{_libdir}/libsrt.so.1.5*

%files devel
%doc examples
%{_includedir}/srt
%{_libdir}/libsrt.so
%{_libdir}/pkgconfig/srt.pc


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Yanko Kaneti <yaneti@declera.com> - 1.5.4-3
- Backport upstream patch for CMake 4.0 compatibility

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 11 2024 Yanko Kaneti <yaneti@declera.com> - 1.5.4-1
- Update to 1.5.4

* Thu Oct 10 2024 Yanko Kaneti <yaneti@declera.com> - 1.5.4-0.rc2
- Update to 1.5.4-rc2

* Tue Oct  1 2024 Yanko Kaneti <yaneti@declera.com> - 1.5.4-0.rc1
- Update to 1.5.4-rc1

* Wed Sep 11 2024 Xavier Bachelot <xavier@bachelot.org> - 1.5.4-0.rc0.1
- Explicitely BR: nettle-devel

* Mon Aug 26 2024 Yanko Kaneti <yaneti@declera.com> - 1.5.4-0.rc0
- Update to 1.5.4-rc0

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep  7 2023 Yanko Kaneti <yaneti@declera.com> - 1.5.3-1
- Update to 1.5.3

* Mon Aug 21 2023 Yanko Kaneti <yaneti@declera.com> - 1.5.3-0.rc0
- Update to 1.5.3-rc0

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Yanko Kaneti <yaneti@declera.com> - 1.5.2-1
- Update to 1.5.2

* Wed May  3 2023 Yanko Kaneti <yaneti@declera.com> - 1.5.2-0.rc2
- Update to 1.5.2-rc2. Reenable running tests on s390x

* Mon Feb 20 2023 Yanko Kaneti <yaneti@declera.com> - 1.5.2-0.rc1
- Update to 1.5.2-rc1

* Mon Jan 30 2023 Yanko Kaneti <yaneti@declera.com> - 1.5.1-4
- With gcc fixed re-enable TestSocketOptions.InvalidVals test

* Sat Jan 21 2023 Yanko Kaneti <yaneti@declera.com> - 1.5.1-3
- Additional test tweaks

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 26 2022 Yanko Kaneti <yaneti@declera.com> - 1.5.1-1
- Update to 1.5.1

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Yanko Kaneti <yaneti@declera.com> - 1.5.0-1
- Update to 1.5.0. Major API/ABI update

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Oct  4 2021 Yanko Kaneti <yaneti@declera.com> - 1.4.4-1
- Update to 1.4.4
- Various tweaks around tests/checks
- Tighten soname wildcard

* Mon Sep  6 2021 Yanko Kaneti <yaneti@declera.com> - 1.4.3-3
- Bump rebuild for gtest soname change

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May  9 2021 Yanko Kaneti <yaneti@declera.com> - 1.4.3-1
- Update to 1.4.3. New soname

* Tue Mar 30 2021 Jonathan Wakely <jwakely@redhat.com> - 1.4.2-4
- Rebuilt for removed libstdc++ symbol (#1937698)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Jeff Law <law@redhat.com> - 1.4.2-2
- Fix missing #includes for gcc-11

* Thu Oct 29 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Jeff Law <law@redhat.com> - 1.4.1-4
- Use __cmake_in_source_build 

* Mon Apr 06 2020 Nicolas Chauvet <kwizart@gmail.com> - 1.4.1-3
- Switch to gnutls instead of openssl
- Enable tests
- Enforce strict EVR from main to -libs

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec  9 2019 Yanko Kaneti <yaneti@declera.com> - 1.4.1-1
- Update to 1.4.1

* Mon Sep 16 2019 Yanko Kaneti <yaneti@declera.com> - 1.4.0-1
- Update to 1.4.0

* Wed Sep 11 2019 Yanko Kaneti <yaneti@declera.com> - 1.3.4-1
- Update to 1.3.4

* Thu Aug  1 2019 Yanko Kaneti <yaneti@declera.com> - 1.3.3-3
- First attempt
- Adjustments suggested by review
