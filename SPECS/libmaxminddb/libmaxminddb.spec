Summary:        C library for reading MaxMind DB files
Name:           libmaxminddb
Version:        1.7.1
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Libraries
URL:            https://github.com/maxmind/libmaxminddb
Source0:        https://github.com/maxmind/libmaxminddb/releases/download/%{version}/%{name}-%{version}.tar.gz
BuildRequires:  gcc
BuildRequires:  make

%description
The libmaxminddb library provides a C library for reading MaxMind DB files,
including the GeoIP2 databases from MaxMind. This is a custom binary format
designed to facilitate fast lookups of IP addresses while allowing for great
flexibility in the type of data associated with an address.

%package devel
Summary:        Development headers for libmaxminddb.
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
%{summary}

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSE
%{_bindir}/mmdblookup
%{_libdir}/*.so*

%files devel
%license LICENSE
%doc README.md
%exclude %{_libdir}/libmaxminddb.a
%{_mandir}
%{_includedir}/
%{_libdir}/*.so
%{_libdir}/pkgconfig/libmaxminddb.pc

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.1-1
- Auto-upgrade to 1.7.1 - Azure Linux 3.0 - package upgrades

* Mon Jan 10 2022 Henry Li <lihl@microsoft.com> 1.6.0-1
- Upgrade to version 1.6.0

* Fri Feb 05 2021 Henry Beberman <henry.beberman@microsoft.com> 1.5.0-1
- Add libmaxminddb spec
- License verified
- Original version for CBL-Mariner