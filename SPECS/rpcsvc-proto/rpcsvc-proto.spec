Summary:        rcpsvc protocol.x files and headers
Name:           rpcsvc-proto
Version:        1.4.4
Release:        1%{?dist}
License:        BSD-3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/thkukuk/rpcsvc-proto
Source0:        https://github.com/thkukuk/rpcsvc-proto/releases/download/v%{version}/%{name}-%{version}.tar.xz
Provides:       rpcgen = %{version}-%{release}

%description
The rpcsvc-proto package contains the rcpsvc protocol.x files and headers,
formerly included with glibc, that are not included in replacement
libtirpc-1.1.4, along with the rpcgen program.

%package    devel
Summary:        Development files for the rpcsvc library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description    devel
This package includes header files and libraries necessary for developing programs which use the rpcsvc library.

%prep
%setup -q

%build
autoreconf -fi
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%license COPYING
%{_bindir}/rpcgen
%{_mandir}/man1/*

%files devel
%{_includedir}/rpcsvc/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.4.4-1
- Auto-upgrade to 1.4.4 - Azure Linux 3.0 - package upgrades

* Fri Feb 04 2022 Chris Co <chrco@microsoft.com> - 1.4.3-1
- Update to 1.4.3
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.4-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Alexey Makhalov <amakhalov@vmware.com> 1.4-1
- Initial version
