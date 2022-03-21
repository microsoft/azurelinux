Summary:        nghttp2 is an implementation of HTTP/2 and its header compression algorithm, HPACK.
Name:           nghttp2
Version:        1.46.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://nghttp2.org
Source0:        https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz

BuildRequires:  c-ares-devel
BuildRequires:  jansson-devel
BuildRequires:  libevent-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd
BuildRequires:  zlib-devel

Provides:       libnghttp2 = %{version}-%{release}

%description
Implementation of the Hypertext Transfer Protocol version 2 in C.

%package devel
Summary:        Header files for nghttp2

Provides:       libnghttp2-devel = %{version}-%{release}

Requires:       %{name} = %{version}-%{release}

%description devel
These are the header files of nghttp2.

%prep
%setup -q

%build
./configure --prefix=%{_prefix}        \
            --disable-static           \
            --enable-lib-only          \
            --disable-python-bindings

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
rm %{buildroot}/%{_libdir}/*.la

%files
%defattr(-,root,root)
%license COPYING
%{_libdir}/*.so.*
%{_datadir}/nghttp2
%{_docdir}/%{name}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Jan 31 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 1.46.0-1
- Upgrading to v1.46.0

* Wed Jun 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.41.0-2
- Adding 'Provides' for 'libhttpng2*' subpackages to align with other naming for the package.

* Tue Nov 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.41.0-1
- Upgrading to 1.41.0 to fix CVE-2020-11080.
- License verified.
- Removed %%sha1 macro.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.33.0-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.33.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> - 1.33.0-1
- Upgrade to version 1.33.0

* Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> - 1.23.1-1
- First version
