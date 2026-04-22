# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global glib2_version 2.38.0
%global libsoup_version 3.1.2

# Packagers: This is the API version of libuhttpmock, as it allows
# for parallel installation of different major API versions (e.g. like
# GTK+ 2 and 3).
%global somajor 1
%global apiver %{somajor}.0

Name:           uhttpmock
Version:        0.11.0
Release: 5%{?dist}
Summary:        HTTP web service mocking library

License:        LGPL-2.1-or-later
URL:            https://gitlab.freedesktop.org/pwithnall/uhttpmock
Source:         %{url}/-/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  meson
BuildRequires:  gcc
BuildRequires:  pkgconfig(glib-2.0) >= %{glib2_version}
BuildRequires:  pkgconfig(gio-2.0) >= %{glib2_version}
BuildRequires:  glib-networking
BuildRequires:  pkgconfig(libsoup-3.0) >= %{libsoup_version}
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  /usr/bin/vapigen

%description
uhttpmock is a project for mocking web service APIs which use HTTP or HTTPS.
It provides a library, libuhttpmock, which implements recording and
playback of HTTP request–response traces.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package        doc
Summary:        Documentation files for %{name}
Enhances:       %{name}-devel = %{version}-%{release}
BuildArch:      noarch

%description    doc
The %{name}-doc package contains documentation for
developing applications that use %{name}.


%prep
%autosetup


%build
%meson -Dgtk_doc=true -Dintrospection=true -Dvapi=enabled
%meson_build


%install
%meson_install


%check
%meson_test


%files
%license COPYING
%doc README NEWS AUTHORS
%{_libdir}/lib%{name}-%{apiver}.so.%{somajor}{,.*}
%{_libdir}/girepository-1.0/Uhm-%{apiver}.typelib

%files devel
%{_includedir}/lib%{name}-%{apiver}/
%{_libdir}/lib%{name}-%{apiver}.so
%{_libdir}/pkgconfig/lib%{name}-%{apiver}.pc
%{_datadir}/gir-1.0/Uhm-%{apiver}.gir
%{_datadir}/vala/vapi/lib%{name}-%{apiver}.*

%files doc
%license COPYING
%{_datadir}/gtk-doc/html/lib%{name}-%{apiver}/


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Jonathan Wright <jonathan@almalinux.org> - 0.11.0-1
- update to 0.11.0 rhbz#2292898

* Tue Mar 05 2024 Jeremy Cline <jeremycline@microsoft.com> - 0.10.0-1
- Rebase to 0.10.0 (rhbz#2267675)

* Fri Mar 01 2024 Neal Gompa <ngompa@fedoraproject.org> - 0.9.0-1
- Rebase to 0.9.0 (rhbz#2264130, rhbz#1217971)
- Modernize spec

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Bastien Nocera <bnocera@redhat.com> - 0.5.5-1
+ uhttpmock-0.5.5-1
- Update to 0.5.5

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Kalev Lember <klember@redhat.com> - 0.5.0-9
- Update BRs for vala packaging changes

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 10 2015 Kalev Lember <klember@redhat.com> - 0.5.0-1
- Update to 0.5.0
- Tighten deps with the _isa macro
- Use license macro for COPYING

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Nov 3 2014 Philip Withnall <philip@tecnocode.co.uk> - 0.3.3-1
- Update to 0.3.3

* Fri Aug 22 2014 Philip Withnall <philip@tecnocode.co.uk> - 0.3.1-1
- Update to 0.3.1

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Kalev Lember <kalevlember@gmail.com> - 0.3.0-2
- Rebuilt for gobject-introspection 1.41.4

* Sun Jun 22 2014 Philip Withnall <philip@tecnocode.co.uk> - 0.3.0-1
- Update to 0.3.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Nov 05 2013 Philip Withnall <philip.withnall@collabora.co.uk> - 0.2.0-1
- Initial spec file for version 0.2.0.
