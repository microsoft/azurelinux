Summary:        A dispatcher daemon for systemd-networkd events
Name:           networkd-dispatcher
Version:        2.2.4
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.com/craftyguy/networkd-dispatcher
Source0:        https://gitlab.com/craftyguy/%{name}/-/archive/%{version}/%{name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
%global debug_package %{nil}
BuildRequires:  asciidoc
Requires:       dbus-glib
Requires:       python3
Requires:       python3-dbus
Requires:       python3-gobject

%description
networkd-dispatcher is a dispatcher daemon for systemd-networkd connection status changes. This daemon
is similar to NetworkManager-dispatcher, but is much more limited in the types of events it supports due
to the limited nature of systemd-networkd. The daemon listens for signals from systemd-networkd over dbus,
so it should be very light on resources (e.g. no polling). It is meant to be run as a system-wide daemon (as root).
This allows it to be used for tasks such as starting a VPN after a connection is established.

%prep
%autosetup -p1

%build
make

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}/conf.d
install -m755 %{name} %{buildroot}%{_bindir}/%{name}
install -m644 -D %{name}.service %{buildroot}%{_libdir}/systemd/system/%{name}.service
install -m644 -D %{name}.conf %{buildroot}%{_sysconfdir}/conf.d/%{name}.conf
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/{off.d,routable.d,dormant.d,no-carrier.d,carrier.d,degraded.d,configured.d,configuring.d}
install -Dm644 LICENSE %{buildroot}%{_datadir}/licenses/%{name}/LICENSE
install -Dm644 README.md %{buildroot}%{_docdir}/%{name}/README.md
install -Dm644 %{name}.8 %{buildroot}%{_mandir}/man8/%{name}.8

%files
%license LICENSE
%doc README.md
%dir %{_sysconfdir}/conf.d
%{_bindir}/%{name}
%{_libdir}/systemd/system/%{name}.service
%{_sysconfdir}/conf.d/%{name}.conf
%{_mandir}/man8/networkd-dispatcher.8*
%dir %{_sysconfdir}/%{name}/off.d
%dir %{_sysconfdir}/%{name}/routable.d
%dir %{_sysconfdir}/%{name}/dormant.d
%dir %{_sysconfdir}/%{name}/no-carrier.d
%dir %{_sysconfdir}/%{name}/carrier.d
%dir %{_sysconfdir}/%{name}/degraded.d
%dir %{_sysconfdir}/%{name}/configured.d
%dir %{_sysconfdir}/%{name}/configuring.d

%changelog
* Fri Jun 2 2023 Aditya Dubey <adityadubey@microsoft.com> - 2.2.4-1
- Original version for CBL-Mariner
- License Verified
