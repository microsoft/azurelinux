Summary:        GStreamer integration library for Clutter
Name:           clutter-gst3
Version:        3.0.27
Release:        15%{?dist}
License:        LGPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://developer.gnome.org/clutter-gst/stable/
Source0:        https://download.gnome.org/sources/clutter-gst/3.0/clutter-gst-%{version}.tar.xz
Patch0:         remove-rgbx-bgrx-support.patch
BuildRequires:  %{_bindir}/chrpath
BuildRequires:  make
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(clutter-1.0)
BuildRequires:  pkgconfig(cogl-2.0-experimental)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gstreamer-1.0)
BuildRequires:  pkgconfig(gstreamer-audio-1.0)
BuildRequires:  pkgconfig(gstreamer-base-1.0)
BuildRequires:  pkgconfig(gstreamer-pbutils-1.0)
BuildRequires:  pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:  pkgconfig(gstreamer-tag-1.0)
BuildRequires:  pkgconfig(gstreamer-video-1.0)
BuildRequires:  pkgconfig(gudev-1.0)

%description
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Clutter is an open source software library for creating fast, visually
rich and animated graphical user interfaces.

Clutter GStreamer enables the use of GStreamer with Clutter.

The %{name}-devel package contains libraries and header files for
developing applications that use clutter-gst API version 3.0.

%prep
%autosetup -p1 -n clutter-gst-%{version}

%build
%configure
%make_build

%install
%make_install

find %{buildroot} -type f -name "*.la" -delete -print

rm -rf %{buildroot}%{_libdir}/gstreamer-1.0/

%files
%doc AUTHORS NEWS README
%license COPYING
%{_libdir}/girepository-1.0/ClutterGst-3.0.typelib
%{_libdir}/libclutter-gst-3.0.so.*

%files devel
%{_includedir}/clutter-gst-3.0/
%{_libdir}/libclutter-gst-3.0.so
%{_libdir}/pkgconfig/clutter-gst-3.0.pc
%{_datadir}/gir-1.0/ClutterGst-3.0.gir
%doc %{_datadir}/gtk-doc/

%changelog
* Thu Jan 05 2023 Sumedh Sharma <sumsharma@microsoft.com> - 3.0.27-15
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- License verified

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> 3.0.27-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 18 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 3.0.27-9
- Really add patch to fix cheese#51

* Fri May 13 2022 Michael Catanzaro <mcatanzaro@redhat.com> - 3.0.27-8
- Add patch to fix cheese#51

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.27-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.27-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.27-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 07 2019 Kalev Lember <klember@redhat.com> - 3.0.27-1
- Update to 3.0.27

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Mar 11 2018 Kalev Lember <klember@redhat.com> - 3.0.26-1
- Update to 3.0.26
- Remove ldconfig scriptlets

* Thu Feb 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0.24-5
- Switch to %%ldconfig_scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 03 2017 Kalev Lember <klember@redhat.com> - 3.0.24-1
- Update to 3.0.24

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 06 2016 Kalev Lember <klember@redhat.com> - 3.0.22-1
- Update to 3.0.22

* Thu Sep 08 2016 Kalev Lember <klember@redhat.com> - 3.0.20-1
- Update to 3.0.20
- Don't set group tags

* Sun Mar 20 2016 Kalev Lember <klember@redhat.com> - 3.0.18-1
- Update to 3.0.18
- Use make_install macro

* Sun Feb 14 2016 David King <amigadave@amigadave.com> - 3.0.16-1
- Update to 3.0.16

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Oct 15 2015 Kalev Lember <klember@redhat.com> - 3.0.14-2
- Rebuilt

* Sun Oct 11 2015 David King <amigadave@amigadave.com> - 3.0.14-1
- Update to 3.0.14

* Wed Sep 30 2015 David King <amigadave@amigadave.com> - 3.0.12-1
- Update to 3.0.12

* Fri Sep 04 2015 David King <amigadave@amigadave.com> - 3.0.10-1
- Update to 3.0.10

* Sun Jul 19 2015 David King <amigadave@amigadave.com> - 3.0.8-1
- Update to 3.0.8

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon May 25 2015 David King <amigadave@amigadave.com> - 3.0.6-1
- Update to 3.0.6

* Fri Mar 27 2015 Bastien Nocera <bnocera@redhat.com> - 3.0.4-2
- Remove the GStreamer plugin, as it can cause the one in the
  clutter-gst2 package to become unavailable, breaking Cheese
  https://bugzilla.gnome.org/show_bug.cgi?id=746883

* Sun Feb 22 2015 David King <amigadave@amigadave.com> - 3.0.4-1
- Initial packaging (#1190361)
