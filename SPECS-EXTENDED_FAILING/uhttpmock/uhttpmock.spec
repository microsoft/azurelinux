Vendor:         Microsoft Corporation
Distribution:   Mariner
%global glib2_version 2.31.0
%global libsoup_version 2.37.91

# Packagers: This is the API version of libuhttpmock, as it allows
# for parallel installation of different major API versions (e.g. like
# GTK+ 2 and 3).
%global uhm_api_version 0.0

Name:           uhttpmock
Version:        0.5.0
Release:        12%{?dist}
Summary:        HTTP web service mocking library
License:        LGPLv2
URL:            https://gitlab.com/groups/uhttpmock
Source0:        https://tecnocode.co.uk/downloads/uhttpmock/uhttpmock-%{version}.tar.xz

BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}
BuildRequires:  intltool
BuildRequires:  gobject-introspection-devel
BuildRequires:  gtk-doc
BuildRequires:  vala

Requires:       glib2%{?_isa} >= %{glib2_version}
Requires:       libsoup%{?_isa} >= %{libsoup_version}

%description
uhttpmock is a project for mocking web service APIs which use HTTP or HTTPS.
It provides a library, libuhttpmock, which implements recording and
playback of HTTP request–response traces.

%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains libraries, header files and documentation for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure \
    --enable-gtk-doc \
    --enable-introspection \
    --enable-vala=yes \
    --disable-static
make %{?_smp_mflags}

%check
make check

%install
make DESTDIR=$RPM_BUILD_ROOT install

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%ldconfig_scriptlets

%files
%license COPYING
%doc README NEWS AUTHORS
%{_libdir}/libuhttpmock-%{uhm_api_version}.so.0*
%{_libdir}/girepository-1.0/Uhm-%{uhm_api_version}.typelib

%files devel
%{_libdir}/libuhttpmock-%{uhm_api_version}.so
%{_includedir}/libuhttpmock-%{uhm_api_version}/
%{_libdir}/pkgconfig/libuhttpmock-%{uhm_api_version}.pc
%{_datadir}/gir-1.0/Uhm-%{uhm_api_version}.gir
%{_datadir}/vala/vapi/libuhttpmock-%{uhm_api_version}.deps
%{_datadir}/vala/vapi/libuhttpmock-%{uhm_api_version}.vapi
%doc %{_datadir}/gtk-doc/html/libuhttpmock-%{uhm_api_version}/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.5.0-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
