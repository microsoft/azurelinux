# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           usbredir
Version:        0.15.0
Release:        2%{?dist}
Summary:        USB network redirection protocol libraries
License:        LGPL-2.1-or-later
URL:            https://www.spice-space.org/usbredir.html
Source0:        http://spice-space.org/download/%{name}/%{name}-%{version}.tar.xz
Source1:        http://spice-space.org/download/%{name}/%{name}-%{version}.tar.xz.sig
Source2:        victortoso-E37A484F.keyring
BuildRequires:  gnupg2
BuildRequires:  gcc g++
BuildRequires:  glib2-devel
BuildRequires:  libusb1-devel >= 1.0.9
BuildRequires:  git-core
BuildRequires:  meson

%description
The usbredir libraries allow USB devices to be used on remote and/or virtual
hosts over TCP.  The following libraries are provided:

usbredirparser:
A library containing the parser for the usbredir protocol

usbredirhost:
A library implementing the USB host side of a usbredir connection.
All that an application wishing to implement a USB host needs to do is:
* Provide a libusb device handle for the device
* Provide write and read callbacks for the actual transport of usbredir data
* Monitor for usbredir and libusb read/write events and call their handlers


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        tools
Summary:        usbredir utility tools
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    tools
Includes usbredirect that uses libusbredirhost to export an USB device for use
in another (virtual) machine

%prep
gpgv2 --quiet --keyring %{SOURCE2} %{SOURCE1} %{SOURCE0}
%autosetup -S git_am


%build
%meson \
    -Dgit_werror=disabled \
    -Dtools=enabled \
    -Dfuzzing=disabled

%meson_build


%install
%meson_install


%ldconfig_scriptlets


%files
%{!?_licensedir:%global license %%doc}
%license COPYING.LIB
%{_libdir}/libusbredir*.so.*

%files devel
%doc docs/usb-redirection-protocol.md docs/multi-thread.md ChangeLog.md TODO
%{_includedir}/usbredir*.h
%{_libdir}/libusbredir*.so
%{_libdir}/pkgconfig/libusbredir*.pc

%files tools
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/usbredirect
%{_mandir}/man1/usbredirect.1*


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 27 2025 Victor Toso <victortoso@redhat.com> - 0.15.0-1
- Update to 0.15.0

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 0.13.0-6
- convert license to SPDX

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 03 2022 Victor Toso <victortoso@redhat.com> - 0.13.0-1
- Update to 0.13.0
  Release 0.13.0 drops usbredirserver binary so we now have renamed
  usbredir-server pacakge to usbredir-tools which is more befitting what it
  contains

* Wed Jul 27 2022 Victor Toso <victortoso@redhat.com> - 0.12.0-4
- Fixes unserialization (migration bug)
  Resolves: rhbz#2096008

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Victor Toso <victortoso@redhat.com> - 0.12.0-1
- Update to 0.12.0

* Tue Aug 10 2021 Victor Toso <victortoso@redhat.com> - 0.11.0-1
- Update to 0.11.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu May 27 2021 Victor Toso <victortoso@redhat.com> - 0.10.0-1
- Update to 0.10.0
- Now uses meson to build

* Fri Apr 02 2021 Victor Toso <victortoso@redhat.com> - 0.9.0-1
- Update to 0.9.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 07 2018 Victor Toso <victortoso@redhat.com> - 0.8.0-1
- Update to 0.8.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.1-6
- Switch to %%ldconfig_scriptlets

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 02 2015 Fabiano Fidêncio <fidencio@redhat.com> 0.7.1-1
- Update to upstream 0.7.1 release

* Tue Jun 16 2015 Peter Robinson <pbrobinson@fedoraproject.org> 0.7-4
- Use %%license

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Hans de Goede <hdegoede@redhat.com> - 0.7-1
- Update to upstream 0.7 release

* Tue Sep 10 2013 Hans de Goede <hdegoede@redhat.com> - 0.6-5
- Use the new libusb autodetach kernel driver functionality
- Fix a usbredirparser bug which causes tcp/ip redir to not work (rhbz#1005015)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Hans de Goede <hdegoede@redhat.com> - 0.6-3
- Fix usbredirserver not listening for ipv6 connections (rhbz#957470)
- Fix a few (harmless) coverity warnings

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Dec 13 2012 Hans de Goede <hdegoede@redhat.com> - 0.6-1
- Update to upstream 0.6 release

* Tue Sep 25 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.2-1
- Update to upstream 0.5.2 release

* Wed Sep 19 2012 Hans de Goede <hdegoede@redhat.com> - 0.5.1-1
- Update to upstream 0.5.1 release

* Fri Sep  7 2012 Hans de Goede <hdegoede@redhat.com> - 0.5-1
- Update to upstream 0.5 release

* Mon Jul 30 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.3-3
- Add 2 fixes from upstream fixing issues with some bulk devices (rhbz#842358)

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr  2 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.3-1
- Update to upstream 0.4.3 release

* Tue Mar  6 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.2-1
- Update to upstream 0.4.2 release

* Sat Feb 25 2012 Hans de Goede <hdegoede@redhat.com> - 0.4.1-1
- Update to upstream 0.4.1 release

* Thu Feb 23 2012 Hans de Goede <hdegoede@redhat.com> - 0.4-1
- Update to upstream 0.4 release

* Thu Jan 12 2012 Hans de Goede <hdegoede@redhat.com> - 0.3.3-1
- Update to upstream 0.3.3 release

* Tue Jan  3 2012 Hans de Goede <hdegoede@redhat.com> 0.3.2-1
- Update to upstream 0.3.2 release

* Wed Aug 24 2011 Hans de Goede <hdegoede@redhat.com> 0.3.1-1
- Update to upstream 0.3.1 release

* Thu Jul 14 2011 Hans de Goede <hdegoede@redhat.com> 0.3-1
- Initial Fedora package
