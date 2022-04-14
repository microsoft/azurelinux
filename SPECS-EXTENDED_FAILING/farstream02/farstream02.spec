Vendor:         Microsoft Corporation
Distribution:   Mariner
%global glib2_ver 2.40
%global gst_ver 1.0.0
%global gst_plugins_base_ver 1.0.0
%global far farstream

Name:           %{far}02
Version:        0.2.9
Release:        2%{?dist}
Summary:        Libraries for videoconferencing

# Package is LGPLv2 except for a few files in /common/coverage/
License:        LGPLv2+ and GPLv2+
URL:            https://www.freedesktop.org/wiki/Software/Farstream
Source0:        https://freedesktop.org/software/%{far}/releases/%{far}/%{far}-%{version}.tar.gz
# patch for upstream issue https://gitlab.freedesktop.org/farstream/farstream/issues/16
Patch0:         farstream-0.2.8-configure-add-check-for-glib-mkenums.patch
Patch1:         farstream-0.2.9-build-Adapt-to-backwards-incompatible-change-in-GNU-.patch

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libnice-devel >= 0.1.8
BuildRequires:  glib2-devel >= %{glib2_ver}
BuildRequires:  gstreamer1-devel >= %{gst_ver}
BuildRequires:  gstreamer1-plugins-base-devel >= %{gst_plugins_base_ver}
BuildRequires:  gupnp-igd-devel
BuildRequires:  gobject-introspection-devel

Requires:       glib2%{?isa} >= %{glib2_ver}
Requires:       gstreamer1-plugins-good >= 1.0.0
Requires:       gstreamer1-plugins-bad-free >= 1.0.0
Requires:       libnice-gstreamer1


%description
%{name} is a collection of GStreamer modules and libraries for
videoconferencing.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       gstreamer1-devel  >= %{gst_ver}
Requires:       gstreamer1-plugins-base-devel >= %{gst_plugins_base_ver}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n %{far}-%{version}
%patch0 -p1
%patch1 -p1


%check
#make check


%build
autoreconf --force --install
%configure                                                  \
  --with-package-name='Fedora Farstream-0.2 package'        \
  --with-package-origin='http://download.fedoraproject.org' \
  --disable-silent-rules                                    \
  --disable-static

# It appears there are dependencies missing in the generated
# Makefiles which can result in libfarstream being referenced
# before or while it is still being built.
#
# This is particularly easy to reproduce with LTO because it
# changes the relative speeds of TU compilation vs linking
# Just disable parallel builds for now
make


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%ldconfig_scriptlets


%files
%doc COPYING NEWS AUTHORS
%{_libdir}/*.so.*
%dir %{_libdir}/%{far}-0.2
%{_libdir}/%{far}-0.2/libmulticast-transmitter.so
%{_libdir}/%{far}-0.2/libnice-transmitter.so
%{_libdir}/%{far}-0.2/librawudp-transmitter.so
%{_libdir}/%{far}-0.2/libshm-transmitter.so
%{_libdir}/gstreamer-1.0/libfsrawconference.so
%{_libdir}/gstreamer-1.0/libfsrtpxdata.so
%{_libdir}/gstreamer-1.0/libfsrtpconference.so
%{_libdir}/gstreamer-1.0/libfsvideoanyrate.so
%{_libdir}/girepository-1.0/Farstream-0.2.typelib
%dir %{_datadir}/%{far}
%dir %{_datadir}/%{far}/0.2
%dir %{_datadir}/%{far}/0.2/fsrtpconference
%dir %{_datadir}/%{far}/0.2/fsrawconference
%{_datadir}/%{far}/0.2/fsrawconference/default-element-properties
%{_datadir}/%{far}/0.2/fsrtpconference/default-codec-preferences
%{_datadir}/%{far}/0.2/fsrtpconference/default-element-properties

%files devel
%{_libdir}/libfarstream-0.2.so
%{_libdir}/pkgconfig/%{far}-0.2.pc
%{_includedir}/%{far}-0.2/%{far}/
%{_datadir}/gir-1.0/Farstream-0.2.gir
%{_datadir}/gtk-doc/html/%{far}-libs-0.2/
%{_datadir}/gtk-doc/html/%{far}-plugins-0.2/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.2.9-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Mar 12 2020 Debarshi Ray <rishi@fedoraproject.org> - 0.2.9-1
- Update to 0.2.9.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 17 2020 Jeff Law <law@redhat.com> - 0.2.8-6
- Disable parallel builds for now

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 16 2019 Stefan Becker <chemobejk@gmail.com> - 0.2.8-4
- update to 0.2.8-30-g092d884d (#1647672)
- add patch for upstream issue #16
- raise BR libnice >= 0.1.8 (#1556950)
- add BR glib2-devel
- drop unnecessary BR python-devel
- remove MSN plugin - it was dropped upstream
- update URLs

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Apr 30 2018 David Woodhouse <dwmw2@infradead.org> - 0.2.8-1
- Update to 0.2.8.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 David Woodhouse <dwmw2@infradead.org> - 0.2.7-1
- Update to 0.2.7.

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.4-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.4-1
- Update to 0.2.4.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun May 12 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.2.3-2
- Add requires on libnice-gstreamer1 for recent libnice subpackage change.

* Tue Apr 16 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.2.3-1
- Update to 0.2.3.
- Drop leak patches. Fixed upstream.

* Wed Mar 27 2013 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-3
- Pull some patches from upstream that fix serveral leaks.

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.2-1
- Update to 0.2.2
- Drop properties patch. Fixed upstream.

* Wed Oct 24 2012 Debarshi Ray <rishi@fedoraproject.org> - 0.2.1-2
- Update and fix the default properties for vp8enc

* Thu Oct  4 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.1-1
- Update to 0.2.1

* Wed Oct  3 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.0-2
- Drop unnecessary removal of buildroot in the install section.
- Update License info.

* Wed Sep 26 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.2.0-1
- Update to 0.2.0

* Tue Sep 25 2012 Brian Pepple <bpepple@fedoraproject.org> - 0.1.91-1
- Initial Fedora spec.
