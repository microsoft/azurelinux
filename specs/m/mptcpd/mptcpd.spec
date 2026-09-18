# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Multipath TCP daemon
Name: mptcpd
Version: 0.13
Release: 3%{?dist}
License: GPL-2.0-or-later AND BSD-3-Clause
URL: https://multipath-tcp.org
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
BuildRequires: make
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: automake
BuildRequires: autoconf
BuildRequires: autoconf-archive
BuildRequires: libell-devel
BuildRequires: systemd-units
BuildRequires: systemd-rpm-macros

Source0: https://github.com/multipath-tcp/mptcpd/archive/v%{version}/%{name}-%{version}.tar.gz

%description
The Multipath TCP Daemon is a daemon for Linux based operating systems that
performs multipath TCP path management related operations in user space. It
interacts with the Linux kernel through a generic netlink connection to track
per-connection information (e.g. available remote addresses), available network
interfaces, request new MPTCP subflows, handle requests for subflows, etc.

%package devel
Summary: MPTCP path manager header files
Group: Development/Libraries
Requires: pkgconfig
Requires: %{name}%{?_isa} = %{version}-%{release}
License: BSD-3-Clause

%description devel
Header files for adding MPTCP path manager support to applications

%prep
%autosetup -p1

%build
autoreconf --install --symlink --force
%configure --enable-debug=info
%make_build V=1

%install
install -d %{buildroot}/%{_libexecdir}
install -d %{buildroot}/%{_mandir}/man8
install -d %{buildroot}/%{_sysconfdir}/%{name}
install -d %{buildroot}/%{_unitdir}
install -d %{buildroot}/%{_libdir}/%{name}
install -d %{buildroot}/%{_includedir}/%{name}
%make_install
sed -i '/^# addr-flags=subflow/s/^# //g' %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
sed -i '/^# notify-flags=existing,skip_link_local,skip_loopback/s/^# //g' %{buildroot}/%{_sysconfdir}/%{name}/%{name}.conf
find %{buildroot} -name '*.la' -exec rm -f {} ';'

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig
%systemd_postun mptcp.service

%files
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.conf
%dir %{_sysconfdir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/mptcpize
%{_libdir}/libmptcpd.so.*
%{_libdir}/%{name}/*.so
%{_libdir}/mptcpize/libmptcpwrap.so*
%{_libexecdir}/%{name}
%{_libexecdir}/mptcp-get-debug
%{_bindir}/mptcpize
%{_unitdir}/mptcp.service
%{_mandir}/man8/%{name}.8.gz
%{_mandir}/man8/mptcpize.8.gz
# todo add %doc
%license COPYING

%files devel
%doc COPYING
%dir %{_includedir}/%{name}
%{_libdir}/*.so
%{_includedir}/mptcpd/*.h
%{_libdir}/pkgconfig/mptcpd.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Nov 18 2024 Davide Caratti <dcaratti@redhat.com> - 0.13-1
- Update to version 0.13

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Feb 22 2023 Davide Caratti <dcaratti@redhat.com> - 0.12-1
- SPDX migration
- update to version 0.12

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Davide Caratti <dcaratti@redhat.com> - 0.10-1
- update to version 0.10
- fix build caused by UAPI headers

* Mon Feb 21 2022 Davide Caratti <dcaratti@redhat.com> - 0.9-1
- update to version 0.9
- fix reported FTBFS bug in rawhide

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 30 2021 Davide Caratti <dcaratti@redhat.com> - 0.8-2
- fix addr_adv plugin defaults

* Mon Sep 27 2021 Davide Caratti <dcaratti@redhat.com> - 0.8-1
- update to version 0.8

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Apr 19 2021 Davide Caratti <dcaratti@redhat.com> - 0.7-1
- update to version 0.7

* Tue Feb 23 2021 Davide Caratti <dcaratti@redhat.com> - 0.6-1
- update to version 0.6

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 20 2021 Davide Caratti <dcaratti@redhat.com> - 0.5.1-1
- initial build
