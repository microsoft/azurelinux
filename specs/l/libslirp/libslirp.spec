# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libslirp
Version:        4.9.7
Release: 5%{?dist}
Summary:        A general purpose TCP-IP emulator

# check the SPDX tags in source files for details
License:        BSD-3-Clause AND MIT
URL:            https://gitlab.freedesktop.org/slirp/%{name}
Source0:        %{url}/-/archive/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  git-core
BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  glib2-devel

%description
A general purpose TCP-IP emulator used by virtual machine hypervisors
to provide virtual networking services.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -S git_am

%build
%meson
%meson_build


%install
%meson_install


%files
%license COPYRIGHT LICENSE
%doc README.md CHANGELOG.md
%{_libdir}/%{name}.so.0*

%files devel
%dir %{_includedir}/slirp/
%{_includedir}/slirp/*
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/slirp.pc


%changelog
* Fri Oct 30 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.7-1
- new version, rhbz#2563742
- Fix memory leak on IPv6 ping
- Fix out-of-bounds heap read and information disclosure in ICMP error forwarding
- Fix queue pointer corruption and crash in if_output
- Avoid adding ARP/NDP records for multicast and own addresses
- Fix build with llvm
- Fix endianness of addition in bootp

* Sun Oct 25 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.6-1
- new version, rhbz#2560335
- Fix buffer underflow in TFTP RRQ handling with an empty filename
- Fix ICMP/ICMPv6 echo reply length desynchronization and protocol type mismatch
- Fix several memory and socket descriptor leaks

* Tue Sep 22 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.5-1
- new version, rhbz#2524215
- Fix CVE-2026-95508: heap buffer overflow in DHCPv6/TFTP response builders on small interface MTU
- Fix CVE-2026-95507: out-of-bounds read in NC-SI OEM response handler discloses host memory to guest

* Thu Jul 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_45_Mass_Rebuild

* Tue May 26 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.3-1
- new version

* Sun May 24 2026 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.2-1
- new version, rhbz#2480978

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May 28 2025 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.1-1
- new version

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri May 10 2024 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.8.0-1
- new version

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Apr 27 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.7.0-1
- new version

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 18 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.6.1-1
- new version

* Mon Jun 14 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.6.0-1
- new version

* Wed May 19 2021 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.5.0-1
- new version

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec  2 18:19:30 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.4.0-1
- new version

* Fri Nov 27 20:10:28 +04 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.1-3
- Fix CVE-2020-29129 CVE-2020-29130 out-of-bounds access while processing ARP/NCSI packets
  rhbz#1902232

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 08 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.1-1
- New v4.3.1 release

* Thu Apr 23 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.3.0-1
- New v4.3.0 release

* Mon Apr 20 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.2.0-2
- CVE-2020-1983 fix

* Tue Mar 17 2020 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.2.0-1
- New v4.2.0 release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 03 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.1.0-1
- New v4.1.0 release

* Fri Aug  2 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-3
- Fix CVE-2019-14378, rhbz#1735654

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.0.0-1
- Initial package, rhbz#1712980
