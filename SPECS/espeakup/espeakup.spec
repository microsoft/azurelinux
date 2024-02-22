Summary:        Connector for espeak and speakup
Name:           espeakup
Version:        0.90
Release:        1%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/linux-speakup/espeakup
Source0:        https://github.com/linux-speakup/%{name}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}.conf
Source2:        %{name}.service
BuildRequires:  alsa-lib-devel
BuildRequires:  espeak-ng-devel
BuildRequires:  gcc
BuildRequires:  meson
BuildRequires:  systemd
Requires:       espeak-ng
Requires:       glibc
Requires:       kernel-drivers-accessibility
Requires:       systemd

%description
espeakup is a light weight connector for espeak and speakup.

%prep
%autosetup -p1

%build
%meson -Dsystemd=enabled -Dman=disabled
%meson_build

%install
export MESON_INSTALL_DESTDIR_PREFIX=%{buildroot}%{_prefix} %meson_install
mkdir -p %{buildroot}%{_libdir}/modules-load.d
install -m755 %{SOURCE1} %{buildroot}%{_libdir}/modules-load.d/%{name}.conf
mkdir -p %{buildroot}%{_libdir}/systemd/system
install -m755 %{SOURCE2} %{buildroot}%{_libdir}/systemd/system/%{name}.service

# %check
# This package has no check section as of version 0.90

%files
%defattr(-,root,root)
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_libdir}/systemd/system/%{name}.service
%{_libdir}/modules-load.d/%{name}.conf

%changelog
* Wed Jan 31 2024 Sumedh Sharma <sumsharma@microsoft.com> - 0.90-1
- Bump version to 0.90.
- Remove unneeded patch files.

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 0.80-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Jan 07 2021 Thomas Crain <thcrain@microsoft.com> - 0.80-1
- Original version for CBL-Mariner (license: MIT)
- License verified
