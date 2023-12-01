Summary:        GLib wrapper around libusb1
Name:           libgusb
Version:        0.3.5
Release:        3%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/hughsie/libgusb
Source0:        https://people.freedesktop.org/~hughsient/releases/%{name}-%{version}.tar.xz
BuildRequires:  glib2-devel >= 2.38.0
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  libusb1-devel >= 1.0.19
BuildRequires:  meson
BuildRequires:  vala

%description
GUsb is a GObject wrapper for libusb1 that makes it easy to do
asynchronous control, bulk and interrupt transfers with proper
cancellation and integration into a mainloop.

%package        devel
Summary:        Libraries and headers for gusb
Requires:       %{name} = %{version}-%{release}

%description devel
GLib headers and libraries for gusb.

%prep
%autosetup

%build
%meson -Dvapi=true -Dtests=true

%meson_build

%install
%meson_install

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md AUTHORS NEWS
%{_libdir}/libgusb.so.?
%{_libdir}/libgusb.so.?.0.*
%{_libdir}/girepository-1.0/GUsb-1.0.typelib

%files devel
%{_includedir}/gusb-1
%{_bindir}/gusbcmd
%{_libdir}/libgusb.so
%{_libdir}/pkgconfig/gusb.pc
%{_datadir}/gtk-doc/html/gusb
%{_datadir}/gir-1.0/GUsb-1.0.gir
%{_datadir}/vala/vapi/gusb.deps
%{_datadir}/vala/vapi/gusb.vapi

%changelog
* Wed Dec 08 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.3.5-3
- License verified
- Lint spec

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.3.5-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Thu Jul 30 2020 Richard Hughes <richard@hughsie.com> 0.3.5-1
- New upstream version
- Add a way to get iConfiguration
- Allow building GtkDoc when building as a subproject

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Feb 20 2020 Richard Hughes <richard@hughsie.com> 0.3.4-1
- New upstream version
- Include the USB bus in the generated platform_id
- Validate the exported symbol list during check

* Thu Jan 30 2020 Richard Hughes <richard@hughsie.com> 0.3.3-1
- New upstream version
- Add a thin glib wrapper around libusb_endpoint_descriptor
- Fix high number of wakeups when checking the GUsbContext

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 06 2020 Richard Hughes <richard@hughsie.com> 0.3.2-1
- New upstream version
- Do not use deprecated libusb API
- Use a 1ms timeout in the Windows event thread

* Sat Nov 16 2019 Richard Hughes <richard@hughsie.com> 0.3.1-1
- New upstream version
- Add some new API for fwupd
- Fix GI length introspection annotations

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.3.0-4
- Update BRs for vala packaging changes

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 15 2018 Richard Hughes <richard@hughsie.com> 0.3.0-1
- New upstream version
- Port to the Meson build system

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.2.11-4
- Switch to %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 24 2017 Richard Hughes <richard@hughsie.com> 0.2.11-1
- New upstream version
- Add new API allowing devices to be auto-opened

* Mon Apr 10 2017 Richard Hughes <richard@hughsie.com> 0.2.10-1
- New upstream version
- Correctly detect removed devices when rescanning
- Fix a memory leak when using control tranfers
- Fix symbol version table up to version 0.2.9

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Mar 22 2016 Richard Hughes <richard@hughsie.com> 0.2.9-1
- New upstream version
- Add g_usb_context_wait_for_replug()
- Install gusbcmd as a debugging aid

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 01 2015 Richard Hughes <richard@hughsie.com> 0.2.8-1
- New upstream version
- Add a PERMISSION_DENIED error enum
- Add a thin glib wrapper around a libusb_interface_descriptor
- Ignore the not-found error when resetting a device

* Tue Sep 15 2015 Richard Hughes <richard@hughsie.com> 0.2.7-1
- New upstream version
- Add missing element-type annotations
- Support g_autoptr() for all gusb object types

* Mon Jul 06 2015 Richard Hughes <richard@hughsie.com> 0.2.6-1
- New upstream version
  Do not unref the GMainContext after each request

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Richard Hughes <richard@hughsie.com> 0.2.5-1
- New upstream version
- Add g_usb_device_get_custom_index()
- Allow setting the GMainContext when used for sync methods
- Use symbol versioning

* Mon Jan 09 2015 Richard Hughes <richard@hughsie.com> 0.2.4-1
- New upstream version
- Add new API for various client programs
- Don't filter out hub devices when getting the device list
- Make the platform ID persistent across re-plug

* Mon Dec 01 2014 Richard Hughes <richard@hughsie.com> 0.2.3-1
- New upstream version
- Correctly terminate the libusb event thread

* Wed Nov 26 2014 Richard Hughes <richard@hughsie.com> 0.2.2-1
- New upstream version
- Use a thread to process libusb1 events

* Mon Nov 24 2014 Richard Hughes <richard@hughsie.com> 0.2.1-1
- New upstream version
- Always set a device platform ID
- Ignore 'unsupported' as a return value for kernel drivers

* Thu Nov 20 2014 Richard Hughes <richard@hughsie.com> 0.2.0-1
- New upstream version
- Use the native hotplug support in libusb 1.0.19
- Fix a crash where libusb_get_pollfds() is unavailable

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.1.6-4
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Feb 06 2013 Richard Hughes <richard@hughsie.com> 0.1.6-1
- New upstream version
- Do not use deprecated GLib functionality
- Unref the GMainloop after it has been run, not when just quit

* Tue Feb 05 2013 Richard Hughes <richard@hughsie.com> 0.1.5-1
- New upstream version

* Tue Nov 06 2012 Richard Hughes <richard@hughsie.com> 0.1.4-1
- New upstream version
- Add GObject Introspection support
- Add Vala bindings

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Dec 05 2011 Richard Hughes <richard@hughsie.com> 0.1.3-1
- New upstream version
- Add a missing error enum value

* Fri Nov 11 2011 Richard Hughes <richard@hughsie.com> 0.1.2-1
- New upstream version
- Ignore EBUSY when trying to detach a detached kernel driver

* Tue Nov 01 2011 Richard Hughes <richard@hughsie.com> 0.1.1-1
- New upstream version

* Thu Sep 15 2011 Richard Hughes <richard@hughsie.com> 0.1.0-1
- Initial version for Fedora package review
