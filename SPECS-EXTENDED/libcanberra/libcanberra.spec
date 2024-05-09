Summary:        Portable Sound Event Library
Name:           libcanberra
Version:        0.30
Release:        24%{?dist}
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://0pointer.de/lennart/projects/libcanberra/
Source0:        https://0pointer.de/lennart/projects/%{name}/%{name}-%{version}.tar.xz
Patch0:         0001-gtk-Don-t-assume-all-GdkDisplays-are-GdkX11Displays-.patch
BuildRequires:  gcc
BuildRequires:  gtk2-devel
BuildRequires:  gtk3-devel
BuildRequires:  alsa-lib-devel
BuildRequires:  libvorbis-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  gtk-doc
BuildRequires:  pulseaudio-libs-devel >= 0.9.15
BuildRequires:  gstreamer1-devel
BuildRequires:  libtdb-devel
BuildRequires:  gettext-devel
BuildRequires:  systemd-devel
Requires:       sound-theme-freedesktop
Requires:       pulseaudio-libs >= 0.9.15
Requires(post): systemd
Requires(preun):systemd
Requires(postun): systemd

%description
A small and lightweight implementation of the XDG Sound Theme Specification
(https://0pointer.de/public/sound-theme-spec.html).

%package gtk2
Summary:        Gtk+ 2.x Bindings for libcanberra
Requires:       %{name}%{?_isa} = %{version}-%{release}
# Some other stuff is included in the gtk3 package, so always pull that in.
Requires:       %{name}-gtk3%{?_isa} = %{version}-%{release}

%description gtk2
Gtk+ 2.x bindings for libcanberra

%package gtk3
Summary:        Gtk+ 3.x Bindings for libcanberra
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description gtk3
Gtk+ 3.x bindings for libcanberra

%package devel
Summary:        Development Files for libcanberra Client Development
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk2%{?_isa} = %{version}-%{release}
Requires:       %{name}-gtk3%{?_isa} = %{version}-%{release}
Requires:       gtk2-devel

%description devel
Development Files for libcanberra Client Development

%post
%{?ldconfig}
%systemd_post canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service

%preun
%systemd_preun canberra-system-bootup.service canberra-system-shutdown.service canberra-system-shutdown-reboot.service

%ldconfig_postun

%ldconfig_scriptlets gtk2

%ldconfig_scriptlets gtk3

%prep
%autosetup -p1

%build
%configure --disable-static --enable-pulse --enable-alsa --enable-null --disable-oss --with-builtin=dso --with-systemdsystemunitdir=%{_libdir}/systemd/system
%make_build %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
find %{buildroot} \( -name *.a -o -name *.la \) -exec rm {} \;
rm %{buildroot}%{_docdir}/libcanberra/README

%files
%license LGPL
%doc README LGPL
%{_libdir}/libcanberra.so.*
%dir %{_libdir}/libcanberra-%{version}
%{_libdir}/libcanberra-%{version}/libcanberra-alsa.so
%{_libdir}/libcanberra-%{version}/libcanberra-pulse.so
%{_libdir}/libcanberra-%{version}/libcanberra-null.so
%{_libdir}/libcanberra-%{version}/libcanberra-multi.so
%{_libdir}/libcanberra-%{version}/libcanberra-gstreamer.so
%{_libdir}/systemd/system/canberra-system-bootup.service
%{_libdir}/systemd/system/canberra-system-shutdown-reboot.service
%{_libdir}/systemd/system/canberra-system-shutdown.service
%{_bindir}/canberra-boot

%files gtk2
%{_libdir}/libcanberra-gtk.so.*
%{_libdir}/gtk-2.0/modules/libcanberra-gtk-module.so

%files gtk3
%{_libdir}/libcanberra-gtk3.so.*
%{_libdir}/gtk-3.0/modules/libcanberra-gtk3-module.so
%{_libdir}/gtk-3.0/modules/libcanberra-gtk-module.so
%{_bindir}/canberra-gtk-play
%{_datadir}/gnome/autostart/libcanberra-login-sound.desktop
%{_datadir}/gnome/shutdown/libcanberra-logout-sound.sh
# co-own these directories to avoid requiring GDM (#522998)
%dir %{_datadir}/gdm/
%dir %{_datadir}/gdm/autostart/
%dir %{_datadir}/gdm/autostart/LoginWindow/
%{_datadir}/gdm/autostart/LoginWindow/libcanberra-ready-sound.desktop
# co-own these directories to avoid requiring g-s-d
%dir %{_libdir}/gnome-settings-daemon-3.0/
%dir %{_libdir}/gnome-settings-daemon-3.0/gtk-modules/
%{_libdir}/gnome-settings-daemon-3.0/gtk-modules/canberra-gtk-module.desktop

%files devel
%doc %{_datadir}/gtk-doc
%{_includedir}/canberra-gtk.h
%{_includedir}/canberra.h
%{_libdir}/libcanberra-gtk.so
%{_libdir}/libcanberra-gtk3.so
%{_libdir}/libcanberra.so
%{_libdir}/pkgconfig/libcanberra-gtk.pc
%{_libdir}/pkgconfig/libcanberra-gtk3.pc
%{_libdir}/pkgconfig/libcanberra.pc
# co-own these directories to avoid requiring vala
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libcanberra-gtk.vapi
%{_datadir}/vala/vapi/libcanberra.vapi

%changelog
* Thu Nov 24 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.30-24
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.30-23
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov  8 2019 Tom Callaway <spot@fedoraproject.org> - 0.30-21
- remove %%systemd_postun macro to fix FTBFS

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 12 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.30-19
- Fix typo in postun

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Orion Poplawski <orion@cora.nwra.com> - 0.30-12
- Rebuild for libtdb 1.3.12
- Drop %%defattr
- Use %%license

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.30-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 28 2015 Kevin Fenzi <kevin@scrye.com> 0.30-9
- Try and fix devel package not pulling in the right things in rawhide

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 0.30-8
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Matthias Clasen <mclasen@redhat.com> - 0.30-5
- Add an upstream patch to drop hardcoded X11 assumptions

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Oct 29 2012 Matthias Clasen <mclasen@redhat.com> - 0.30-2
- Update to 0.30
- Add %%{_isa} as required to fix multilib issues

* Tue Sep 25 2012 Lennart Poettering <lpoetter@redhat.com> - 0.30-1
- New upstream release

* Mon Sep 24 2012 Bastien Nocera <bnocera@redhat.com> 0.29-6
- Disable the GStreamer backend, it's not used in Fedora

* Fri Sep 14 2012 Lennart Poettering <lpoetter@redhat.com> - 0.29-5
- Use systemd macros

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Kay Sievers <kay@redhat.com> - 0.29-3
- rebuild for libudev1

* Tue May 15 2012 Lennart Poettering <lpoetter@redhat.com> - 0.29-2
- Various minor .spec file fixes

* Tue May 15 2012 Lennart Poettering <lpoetter@redhat.com> - 0.29-1
- New upstream
- Closes #744888, #696194

* Thu Feb 23 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.28-6
- Update systemd service file locations

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 08 2011 Adam Jackson <ajax@redhat.com> - 0.28-4
- Rebuild to break bogus libpng dep

* Thu Mar 24 2011 Christopher Aillon <caillon@redhat.com> - 0.28-3
- Workaround a hang (fdo#35024)

* Tue Mar  1 2011 Bill Nottingham <notting@redhat.com> - 0.28-2
- own gnome-settings-daemon desktop dir, don't require g-s-d

* Fri Feb 25 2011 Lennart Poettering <lpoetter@redhat.com> - 0.28-1
- New upstream release

* Fri Feb 18 2011 Lennart Poettering <lpoetter@redhat.com> - 0.27-1
- New upstream Release

* Thu Feb 10 2011 Matthias Clasen <mclasen@redhat.com> 0.26-8
- Rebuild against newer gtk

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb  2 2011 Matthias Clasen <mclasen@redhat.com> 0.26-6
- Rebuild

* Fri Jan  7 2011 Matthias Clasen <mclasen@redhat.com> 0.26-5
- Rebuild against newer gtk

* Fri Dec 3 2010 Matthias Clasen <mclasen@redhat.com> 0.26-4
- Rebuild against new gtk

* Mon Nov 1 2010 Matthias Clasen <mclasen@redhat.com> 0.26-3
- Rebuild against newer gtk3

* Mon Oct 4 2010 Lennart Poettering <lpoetter@redhat.com> 0.26-2
- Use final 0.26 tarball

* Mon Oct 4 2010 Lennart Poettering <lpoetter@redhat.com> 0.26-1
- New version 0.26

* Mon Aug 23 2010 Matthias Clasen <mclasen@redhat.com> 0.25-3
- Co-own /usr/share/gtk-doc (#604379)

* Mon Jun 28 2010 Matthias Clasen <mclasen@redhat.com> 0.25-2
- Rebuild

* Sun Jun 13 2010 Lennart Poettering <lpoetter@redhat.com> 0.25-1
- New version 0.25

* Sat Feb 20 2010 Lennart Poettering <lpoetter@redhat.com> 0.23-1
- New version 0.23

* Tue Oct 20 2009 Lennart Poettering <lpoetter@redhat.com> 0.22-1
- New version 0.22

* Fri Oct 16 2009 Lennart Poettering <lpoetter@redhat.com> 0.21-1
- New version 0.21

* Thu Oct 15 2009 Lennart Poettering <lpoetter@redhat.com> 0.20-1
- New version 0.20

* Wed Oct 14 2009 Lennart Poettering <lpoetter@redhat.com> 0.19-1
- New version 0.19

* Fri Sep 25 2009 Matthias Clasen <mclasen@redhat.com> - 0.18-2
- Don't require vala in -devel (#523473)

* Sat Sep 19 2009 Lennart Poettering <lpoetter@redhat.com> 0.18-1
- New version 0.18

* Wed Sep 16 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 0.17-2
- Don't require gdm in -gtk2 (#522998)

* Fri Sep 11 2009 Lennart Poettering <lpoetter@redhat.com> 0.17-1
- New version 0.17

* Thu Aug 27 2009 Lennart Poettering <lpoetter@redhat.com> 0.16-1
- New version 0.16

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.15-2
- Fix mistag

* Wed Aug 5 2009 Lennart Poettering <lpoetter@redhat.com> 0.15-1
- New version 0.15

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.14-2
- Upload the right tarball

* Thu Jul 2 2009 Lennart Poettering <lpoetter@redhat.com> 0.14-1
- New version 0.14

* Tue Jun 23 2009 Lennart Poettering <lpoetter@redhat.com> 0.13-1
- New version 0.13

* Tue Jun 16 2009 Brian Pepple <bpepple@fedoraproject.org> - 0.12-2
- Rebuild for new libtdb.

* Mon Apr 13 2009 Lennart Poettering <lpoetter@redhat.com> 0.12-1
- New version 0.12

* Wed Apr 1 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-9
- Another preview for 0.12

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-8
- Add missing dependency on gettext-devel

* Wed Feb 25 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-7
- Preview for 0.12

* Thu Feb  5 2009 Matthias Clasen  <mclasen@redhat.com> 0.11-6
- Fix up Requires (#484225)

* Wed Jan 21 2009 Lennart Poettering <lpoetter@redhat.com> 0.11-5
- New version

* Sun Dec 14 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-4
- Moved login sound to "Application" startup phase.

* Thu Nov 13 2008 Matthias Clasen <mclasen@redhat.com> 0.10-3
- Rebuild

* Fri Oct 10 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-2
- Drop libcanberra-gtk-module.sh since the gconf stuff is supported just fine in current gnome-session already.

* Mon Oct 6 2008 Lennart Poettering <lpoetter@redhat.com> 0.10-1
- New version

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.9-1
- New version

* Thu Aug 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.8-2
- Fix build-time dep on Gstreamer

* Thu Aug 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.8-1
- New version

* Thu Aug 14 2008 Lennart Poettering <lpoetter@redhat.com> 0.7-1
- New version

* Mon Aug 4 2008 Lennart Poettering <lpoetter@redhat.com> 0.6-1
- New version

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-4
- Really add versioned dependency on libpulse

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-3
- Ship libcanberra-gtk-module.sh directly in CVS

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-2
- Fix build

* Wed Jul 30 2008 Lennart Poettering <lpoetter@redhat.com> 0.5-1
- New version

* Mon Jul 28 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-3
- Add versioned dependency on libpulse

* Sun Jul 27 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-2
- Fix module name in libcanberra-gtk-module.sh

* Fri Jul 25 2008 Lennart Poettering <lpoetter@redhat.com> 0.4-1
- New version
- Install libcanberra-gtk-module.sh

* Mon Jun 16 2008 Lennart Poettering <lpoetter@redhat.com> 0.3-2
- Add dependency on sound-theme-freedesktop

* Fri Jun 13 2008 Lennart Poettering <lpoetter@redhat.com> 0.3-1
- Initial package, based on Colin Guthrie's Mandriva package
