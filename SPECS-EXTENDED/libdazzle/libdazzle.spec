Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global glib2_version 2.57.2
%global gtk3_version 3.24.0

Name:           libdazzle
Version:        3.44.0
Release:        1%{?dist}
Summary:        Experimental new features for GTK+ and GLib

License:        GPLv3+
URL:            https://git.gnome.org/browse/libdazzle/
Source0:        https://download.gnome.org/sources/%{name}/3.44/%{name}-%{version}.tar.xz

BuildRequires:  meson
BuildRequires:  vala

BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gmodule-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0) >= %{gtk3_version}

# for tests
BuildRequires:  words
BuildRequires:  xorg-x11-server-Xvfb

Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       gtk3%{?_isa} >= %{gtk3_version}

%description
libdazzle is a collection of fancy features for GLib and Gtk+ that aren't quite
ready or generic enough for use inside those libraries. This is often a proving
ground for new widget prototypes. Applications such as Builder tend to drive
development of this project.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%autosetup -p1


%build
%meson -D enable_gtk_doc=false
%meson_build


%install
%meson_install

%find_lang libdazzle-1.0

%check
xvfb-run -w 10 ninja test %{__ninja_common_opts} -C %{_vpath_builddir}



%files -f libdazzle-1.0.lang
%license COPYING
%doc AUTHORS NEWS README.md
%{_bindir}/dazzle-list-counters
%{_libdir}/libdazzle-1.0.so.*
%dir %{_libdir}/girepository-1.0
%{_libdir}/girepository-1.0/Dazzle-1.0.typelib

%files devel
%doc CONTRIBUTING.md examples
%dir %{_datadir}/gir-1.0
%{_datadir}/gir-1.0/Dazzle-1.0.gir
%dir %{_datadir}/vala
%dir %{_datadir}/vala/vapi
%{_datadir}/vala/vapi/libdazzle-1.0.*
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/libdazzle-1.0.pc


%changelog
* Wed Nov 13 2024 Jyoti Kanase <v-jykanase@microsoft.com> - 3.44.0-1
- Update to 3.44.0
- License verified

* Mon Mar 21 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.36.0-3
- Adding BR on '%%{_bindir}/xsltproc'.
- Disabled gtk doc generation to remove network dependency during build-time.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.36.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Mar 06 2020 Kalev Lember <klember@redhat.com> - 3.36.0-1
- Update to 3.36.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.35.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 12 2020 Kalev Lember <klember@redhat.com> - 3.35.3-1
- Update to 3.35.3

* Tue Dec 17 2019 Kalev Lember <klember@redhat.com> - 3.35.2-1
- Update to 3.35.2

* Mon Oct 07 2019 Kalev Lember <klember@redhat.com> - 3.34.1-1
- Update to 3.34.1

* Tue Sep 10 2019 Kalev Lember <klember@redhat.com> - 3.34.0-1
- Update to 3.34.0

* Mon Aug 12 2019 Kalev Lember <klember@redhat.com> - 3.33.90-1
- Update to 3.33.90

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.33.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 25 2019 Kalev Lember <klember@redhat.com> - 3.33.3-1
- Update to 3.33.3

* Thu May 09 2019 Kalev Lember <klember@redhat.com> - 3.33.1-1
- Update to 3.33.1

* Tue May 07 2019 Kalev Lember <klember@redhat.com> - 3.32.2-1
- Update to 3.32.2

* Tue Apr 16 2019 Adam Williamson <awilliam@redhat.com> - 3.32.1-2
- Rebuild with Meson fix for #1699099

* Thu Apr 11 2019 Kalev Lember <klember@redhat.com> - 3.32.1-1
- Update to 3.32.1

* Wed Mar 13 2019 Kalev Lember <klember@redhat.com> - 3.32.0-1
- Update to 3.32.0

* Tue Mar 05 2019 Kalev Lember <klember@redhat.com> - 3.31.92-1
- Update to 3.31.92

* Tue Feb 05 2019 Kalev Lember <klember@redhat.com> - 3.31.90-1
- Update to 3.31.90

* Mon Feb  4 2019 Yanko Kaneti <yaneti@declera.com> - 3.31.4-3
- Drop dbus-run-session from the tests run

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.31.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 10 2019 Kalev Lember <klember@redhat.com> - 3.31.4-1
- Update to 3.31.4

* Tue Oct 09 2018 Kalev Lember <klember@redhat.com> - 3.31.1-1
- Update to 3.31.1

* Sat Sep 29 2018 Kalev Lember <klember@redhat.com> - 3.30.1-1
- Update to 3.30.1

* Fri Sep 07 2018 Kalev Lember <klember@redhat.com> - 3.30.0-2
- Rebuilt against fixed atk (#1626575)

* Thu Sep 06 2018 Kalev Lember <klember@redhat.com> - 3.30.0-1
- Update to 3.30.0

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 3.28.5-2
- Rebuild with fixed binutils

* Sat Jul 28 2018 Kalev Lember <klember@redhat.com> - 3.28.5-1
- Update to 3.28.5

* Fri Jul 27 2018 Kalev Lember <klember@redhat.com> - 3.28.4-1
- Update to 3.28.4

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.28.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Kalev Lember <klember@redhat.com> - 3.28.3-1
- Update to 3.28.3

* Thu May 24 2018 Kalev Lember <klember@redhat.com> - 3.28.2-1
- Update to 3.28.2

* Tue Apr 10 2018 Kalev Lember <klember@redhat.com> - 3.28.1-1
- Update to 3.28.1

* Wed Mar 14 2018 Kalev Lember <klember@redhat.com> - 3.28.0-1
- Update to 3.28.0

* Mon Mar 05 2018 Kalev Lember <klember@redhat.com> - 3.27.92-1
- Update to 3.27.92

* Sat Mar 03 2018 Kalev Lember <klember@redhat.com> - 3.27.91-1
- Update to 3.27.91

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.27.90-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Kalev Lember <klember@redhat.com> - 3.27.90-1
- Update to 3.27.90
- Drop ldconfig scriptlets

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.27.5-2
- Switch to %%ldconfig_scriptlets

* Sun Jan 28 2018 Kalev Lember <klember@redhat.com> - 3.27.5-1
- Update to 3.27.5

* Tue Dec 19 2017 Kalev Lember <klember@redhat.com> - 3.27.3-1
- Update to 3.27.3
- Set minimum required glib version

* Tue Oct  3 2017 Yanko Kaneti <yaneti@declera.com> - 3.26.1-1
- Update to 3.26.1

* Tue Sep 12 2017 Yanko Kaneti <yaneti@declera.com> - 3.26.0-1
- Update to 3.26.0

* Tue Sep  5 2017 Yanko Kaneti <yaneti@declera.com> - 3.25.92-1
- Update to 3.25.92
- Reenable test-fuzzy-index, should be fixed upstream

* Sun Aug 27 2017 Kalev Lember <klember@redhat.com> - 3.25.91-1
- Update to 3.25.91

* Tue Aug  8 2017 Yanko Kaneti <yaneti@declera.com> - 3.25.90-1
- Update to 3.25.90

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.25.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Yanko Kaneti <yaneti@declera.com> - 3.25.5-1
- Update to 3.25.5

* Wed Jul 19 2017 Yanko Kaneti <yaneti@declera.com> - 3.25.4-1
- Update to 3.25.4. Add tests, BR: xorg-x11-server-Xvfb, words, dbus

* Tue Jul 18 2017 Kalev Lember <klember@redhat.com> - 3.25.3-3
- Drop the workaround as meson is now fixed

* Thu Jun 22 2017 Yanko Kaneti <yaneti@declera.com> - 3.25.3-2
- Add temporary workaround for meson 0.41.1 breakage

* Mon Jun 19 2017 Yanko Kaneti <yaneti@declera.com> - 3.25.3-1
- Initial spec
