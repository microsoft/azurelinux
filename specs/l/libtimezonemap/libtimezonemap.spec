# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           libtimezonemap
Version:        0.4.5.3
Release:        7%{?dist}
Summary:        Time zone map widget for Gtk+

# Automatically converted from old format: GPLv3 - review is highly recommended.
License:        GPL-3.0-only
URL:            https://launchpad.net/timezonemap
Source0:        https://github.com/dashea/timezonemap/archive/%{version}.tar.gz

BuildRequires:  autoconf automake libtool
BuildRequires:  glib2-devel >= 2.26
BuildRequires:  gtk3-devel >= 3.1.4
BuildRequires:  json-glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  libsoup-devel >= 2.42.0
BuildRequires:  librsvg2-devel
BuildRequires: make

%description
libtimezonemap is a time zone map widget for Gtk+. The widget displays a world
map with a highlighted region representing the selected time zone, and the
location can be changed by clicking on the map.

This library is a fork of the of the code from gnome-control-center's datetime
panel, which was itself a fork of Ubiquity's timezone map.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
libtimezonemap is a time zone map widget for Gtk+. This package contains header
files used for building applications that use %{name}.

%prep
%autosetup -n timezonemap-%{version}

%build
./autogen.sh
%configure --disable-static
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}%{_libdir}/*.la

%ldconfig_scriptlets

%files
%license COPYING
%doc README TODO
%{_libdir}/libtimezonemap.so.*
%{_libdir}/girepository-1.0/TimezoneMap-1.0.typelib
%{_datadir}/%{name}

%files devel
%{_libdir}/libtimezonemap.so
%{_libdir}/pkgconfig/timezonemap.pc
%{_includedir}/timezonemap
%{_datadir}/gir-1.0/TimezoneMap-1.0.gir
%{_datadir}/glade/catalogs/TimezoneMap.xml

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 19 2024 David Shea <reallylongword@gmail.com> - 0.4.5.3-4
- Rebuild

* Mon Jul 29 2024 Miroslav Suchý <msuchy@redhat.com> - 0.4.5.3-3
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Feb 20 2024 David Shea <reallylongword@gmail.com> - 0.4.5.3-1
- Clean up the autotools files and scripts
- Remove the tests since the data they were testing has been removed
- Import latest data from geonames.org
- Restore some missing islands

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Aug 17 2022 David Shea <reallylongword@gmail.com> - 0.4.5.2-1
- Release 0.4.5.2
- Remove regions from the map (jkonecny)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.4.5.1-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 20 2017 David Shea <dshea@redhat.com> - 0.4.5.1-1
- Fix SVG visibility (jkonecny) (#1502915)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 17 2017 David Shea <dshea@redaht.com> - 0.4.5-6
- Removed tests

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Aug 17 2016 David Shea <dshea@redhat.com> - 0.4.5-4
- Bring back the setting of $TZ (#1367647)

* Wed Jun 29 2016 David Shea <dshea@redhat.com> - 0.4.5-3
- Render the map directly from SVG (#1335158)
- Fix memory leaks in tz.c
- Fix an invalid memory access
- Do not modify TZ in the process environment
- Move all data files to /usr/share/libtimezonemap from .../libtimezonemap/ui
- Add extra city data so all timezone offsets are clickable
- Move Venezuela from -04:30 to -04:00
- Fix the conversion of points just west of 180 longitude
- Remove the out-of-date Olson map data
- Update the "backward" file
- Improve the location selected when setting the timezone by name (#1322648)
- Remove an extra line in the +10:00 layer
- Move Chile back an hour

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan  4 2016 David Shea <dshea@redhat.com> - 0.4.5-1
- Update the map images

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May  8 2015 David Shea <dshea@redhat.com> - 0.4.4-1
- Fixes for LP#1440157:
  Port to libsoup directly for geoname results
  Fix some memory leaks
  Do not reuse GCancellables
- Upstream merges of SVG update and constrained location cycles

* Fri May  1 2015 David Shea <dshea@redhat.com> - 0.4.2-6
- Updated the time zone map images
- Updated the city data from geonames.org
- Fix a memory leak and potential crash with the locations list
- Cycle through a smaller list of map locations on repeated clicks

* Wed Jan 28 2015 David Shea <dshea@redhat.com> - 0.4.2-5
- Use %%license for the license file

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.2-3
- Rebuilt for gobject-introspection 1.41.4

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  2 2014 David Shea <dshea@redhat.com> - 0.4.2-1
- New upstream release libtimezonemap-0.4.2

* Mon Dec  2 2013 David Shea <dshea@redhat.com> - 0.4.1-4
- Merge fixes from lp:timezonemap
- Add cc-timezone-location.h to timezonemapincludes_HEADERS so it gets installed (iain.lane)
- Set en_name correctly (iain.lane)
- Don't call g_type_init() on glib >= 2.35; it's deprecated (iain.lane)

* Wed Nov 27 2013 David Shea <dshea@redhat.com> - 0.4.1-3
- Added a glade catalog file (dshea)

* Tue Nov 26 2013 David Shea <dshea@redhat.com> - 0.4.1-2
- Make whitespace and indentation consistent (iain.lane@canonical.com)
- Switched to a git-formatted patch for the FSF address to make things easier
  for me to track (dshea)
- Create local copies of string properties. (dshea)
- Moved CcTimezoneLocation into its own file. (dshea)
- Don't close a NULL file pointer. (dshea)
- Turn on and fix g-ir-scanner warnings. (dshea)
- Added a .bzrignore file to ignore all the files generated by the build. (dshea)
- Ignore the INSTALL file (dshea)
- Added a function to clear the location set for a CcTimezoneMap (dshea)
- Allow the timezone highlight to be manually set separately from the location. (dshea)

* Thu Nov 14 2013 David Shea <dshea@redhat.com> - 0.4.1-1
- Initial version
