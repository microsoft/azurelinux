Summary:    nghttp2 is an implementation of HTTP/2 and its header compression algorithm, HPACK.
Name:       nghttp2
Version:    1.33.0
Release:        3%{?dist}
License:    MIT
URL:        https://nghttp2.org
Group:      Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:	https://github.com/nghttp2/nghttp2/releases/download/v%{version}/%{name}-%{version}.tar.xz
%define sha1 nghttp2=0a11f7de6ea8e66fbecc9fe4ddc61b6ab40af469

BuildRequires: c-ares-devel
BuildRequires: openssl-devel
BuildRequires: systemd
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: libevent-devel
BuildRequires: jansson-devel

%description
Implementation of the Hypertext Transfer Protocol version 2 in C.

%package devel
Summary: Header files for nghttp2
#Requires: %{name}
Requires: %{name} = %{version}-%{release}

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
* Sat May 09 00:20:46 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.33.0-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.33.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Sep 7 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 1.33.0-1
-   Upgrade to version 1.33.0
*   Tue Jun 13 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.23.1-1
-   First version
