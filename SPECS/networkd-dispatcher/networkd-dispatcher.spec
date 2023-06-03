Summary:        A dispatcher daemon for systemd-networkd events
Name:           networkd-dispatcher
Version:        2.2.4
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.com/craftyguy/networkd-dispatcher
Source0:        https://gitlab.com/craftyguy/%{name}/-/archive/v%{version}/%{name}-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  asciidoc
Requires:       python3
Requires:       dbus-python
Requires:       pygobject3
Requires:       dbus-glib

%description
networkd-dispatcher is a dispatcher daemon for systemd-networkd connection status changes. This daemon 
is similar to NetworkManager-dispatcher, but is much more limited in the types of events it supports due 
to the limited nature of systemd-networkd. The daemon listens for signals from systemd-networkd over dbus, 
so it should be very light on resources (e.g. no polling). It is meant to be run as a system-wide daemon (as root). 
This allows it to be used for tasks such as starting a VPN after a connection is established.

%prep
%autosetup -p1

%build

%install

%files
%license LICENSE
%doc README.md

%changelog
* Fri Jun 2 2023 Aditya Dubey <adityadubey@microsoft.com> - 2.2.4-1
- Original version for CBL-Mariner
- License Verified