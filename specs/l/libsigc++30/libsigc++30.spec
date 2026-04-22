# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# first two digits of version
%define release_version %(echo %{version} | awk -F. '{print $1"."$2}')

Name:           libsigc++30
Version:        3.6.0
Release: 7%{?dist}
Summary:        Typesafe signal framework for C++

License:        LGPL-2.1-or-later
URL:            https://github.com/libsigcplusplus/libsigcplusplus
Source0:        https://download.gnome.org/sources/libsigc++/%{release_version}/libsigc++-%{version}.tar.xz

BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen
BuildRequires:  gcc-c++
BuildRequires:  libxslt
BuildRequires:  m4
BuildRequires:  meson
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl-interpreter

%description
libsigc++ implements a typesafe callback system for standard C++. It
allows you to define signals and to connect those signals to any
callback function, either global or a member function, regardless of
whether it is static or virtual.

libsigc++ is used by gtkmm to wrap the GTK+ signal system. It does not
depend on GTK+ or gtkmm.


%package        devel
Summary:        Development tools for the typesafe signal framework for C++
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains the static libraries and header files
needed for development with %{name}.


%package        doc
Summary:        Documentation for %{name}, includes full API docs
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description    doc
This package contains the full API documentation for %{name}.


%prep
%autosetup -n libsigc++-%{version}

chmod -x NEWS


%build
%meson -Dbuild-documentation=true
%meson_build


%install
%meson_install


%files
%license COPYING
%doc NEWS README.md
%{_libdir}/libsigc-3.0.so.0*

%files devel
%{_includedir}/sigc++-3.0/
%{_libdir}/sigc++-3.0/
%{_libdir}/pkgconfig/sigc++-3.0.pc
%{_libdir}/libsigc-3.0.so

%files doc
%doc %{_datadir}/doc/libsigc++-3.0/
%doc %{_datadir}/devhelp/


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 01 2023 Kalev Lember <klember@redhat.com> - 3.6.0-1
- Update to 3.6.0
- Fix NEWS file to not be executable

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 02 2023 David King <amigadave@amigadave.com> - 3.4.0-1
- Update to 3.4.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 David King <amigadave@amigadave.com> - 3.2.0-1
- Update to 3.2.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed May 26 2021 Kalev Lember <klember@redhat.com> - 3.0.7-1
- Update to 3.0.7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Kalev Lember <klember@redhat.com> - 3.0.6-1
- Update to 3.0.6

* Mon Sep 28 2020 Kalev Lember <klember@redhat.com> - 3.0.4-1
- Update to 3.0.4
- Switch to meson build system
- Update upstream URL
- Tighten soname globs

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar 27 2020 Kalev Lember <klember@redhat.com> - 3.0.3-1
- Update to 3.0.3

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 07 2020 Kalev Lember <klember@redhat.com> - 3.0.2-1
- Update to 3.0.2

* Thu Sep 05 2019 Kalev Lember <klember@redhat.com> - 3.0.0-1
- Initial Fedora packaging, based on libsigc++20
