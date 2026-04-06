# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:       xhost
Version:    1.0.9
Release:    10%{?dist}
Summary:    Manage hosts or users allowed to connect to the X server

License:    MIT AND ICU
URL:        https://www.x.org
Source0:    https://www.x.org/pub/individual/app/%{name}-%{version}.tar.xz

Patch01:    0001-Replace-inet_addr-inet_aton-with-a-call-to-inet_pton.patch

BuildRequires:  automake libtool
BuildRequires:  gcc make gettext
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xmu)
BuildRequires:  pkgconfig(xau)
BuildRequires:  pkgconfig(xtrans)
BuildRequires:  pkgconfig(xorg-macros) >= 1.8

Obsoletes:  xorg-x11-server-utils < 7.7-40

%description
xhost is used to manage the list of host names or user names
allowed to make connections to the X server.

%prep
%autosetup

%build
autoreconf -v --install
%configure --disable-silent-rules
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 28 2024 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.9-7
- Replace inet_aton() with inet_pton() to silence rpminspect

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 08 2023 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.9-5
- SPDX migration

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.9-2
- add xgettext to build requires

* Tue Dec 13 2022 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.9-1
- xhost 1.0.9

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 06 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.0.8-1
- xhost 1.0.8

* Thu Apr 08 2021 Peter Hutterer <peter.hutterer@redhat.com> - 1.0.7-2
- Fix Obsoletes line to actually obsolete the -39 server-utils (#1932754)

* Wed Mar 03 2021 Peter Hutterer <peter.hutterer@redhat.com> 1.0.7-1
- Split xhost out from xorg-x11-server-utils into a separate package
  (#1934386)

