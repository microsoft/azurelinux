# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

#global candidate rc2

Name:          libi2cd
Version:       1.0.3
Release:       9%{?candidate:.%{candidate}}%{?dist}
Summary:       C library for interacting with linux I2C devices

License:       LGPL-2.1-or-later
URL:           https://github.com/sstallion/libi2cd/
Source0:       https://github.com/sstallion/libi2cd/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires: automake autoconf libtool
BuildRequires: gcc
BuildRequires: libcmocka-devel
BuildRequires: make

%description
libi2cd provides a simple and straightforward API for accessing I2C devices from
userspace. It relies on the i2c-dev Linux kernel module and is intended to
complement existing tools and libraries, such as those provided by i2c-tools.
It provides both high- and low-level access to the underlying ioctl requests.

%package devel
Summary: Development package for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%setup -q -n %{name}-%{version}%{?candidate:-%{candidate}}

%build
autoreconf -vif
%configure --disable-static

%make_build

%install
%make_install

#Remove libtool archives.
find %{buildroot} -name '*.la' -delete

%ldconfig_scriptlets

%files
%license COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_includedir}/i2cd.h
%{_libdir}/%{name}*.so
%{_libdir}/pkgconfig/libi2cd.pc

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Tue Sep 21 2021 Peter Robinson <pbrobinson@fedoraproject.org> - 1.0-1
- Iniital build
