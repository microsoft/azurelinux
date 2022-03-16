Summary:        DBus for systemd
Name:           dbus-x11
Version:        1.14.0
Release:        1%{?dist}
License:        GPLv2+ OR AFL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/File
URL:            https://www.freedesktop.org/wiki/Software/dbus
Requires:       dbus = %{version}

%description
This is a metapackage that requires dbus. The Fedora dbus-x11 package
is a subpackage of dbus, containing the dbus-launch binary built in presence of
x11 libraries. The Mariner dbus package is not built with x11 libraries, but
does still ship the dbus-launch binary. Since packages needing dbus-x11 either
require it for package tests or for desktop applications, we don't really
need to concern ourselves with shipping the "proper" binary built with x11.

To avoid conflicting with the Mariner dbus package, this metapackage will exist
until the Mariner dbus package is built with x11 libraries.

%prep

%build

%install

%files

%changelog
* Tue Mar 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14.0-1
- Updating version to be in-sync with "dbus".

* Tue Jun 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.13.6-1
- Original version for CBL-Mariner
- License verified
