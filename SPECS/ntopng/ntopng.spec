%global nDPIver 3.4
Summary:        Web-based Network Traffic Monitoring Application
Name:           ntopng
Version:        4.2
Release:        1%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.ntop.org/
Source0:        https://github.com/ntop/ntopng/archive/%{name}-%{version}.tar.gz
Source1:        https://github.com/ntop/nDPI/archive/nDPI-%{nDPIver}.tar.gz
BuildRequires:  curl-devel
BuildRequires:  gcc
BuildRequires:  glib-devel
BuildRequires:  groff
BuildRequires:  json-c-devel
BuildRequires:  libmaxminddb-devel
BuildRequires:  libpcap-devel
BuildRequires:  libxml2-devel
BuildRequires:  make
BuildRequires:  mysql-devel
BuildRequires:  readline-devel
BuildRequires:  sqlite-devel
BuildRequires:  zeromq-devel
Requires:       curl
Requires:       glib
Requires:       json-c
Requires:       libmaxminddb
Requires:       libpcap
Requires:       libxml2
Requires:       mysql
Requires:       sqlite
Requires:       zeromq

%description
ntopng® is a web-based network traffic monitoring application released
under GPLv3. It is the new incarnation of the original ntop written in
1998, and now revamped in terms of performance, usability, and features.

%prep
tar -xf %{SOURCE1}
mv nDPI-%{nDPIver} nDPI
%autosetup -p1 -b 0

%build
./autogen.sh
%configure
%make_build

%install
%make_install

%files
%license LICENSE COPYING
%doc README.md
%{_bindir}/ntopng
%{_prefix}/man/man8/*
%{_datadir}/ntopng/*

%changelog
* Fri Feb 05 2021 Henry Beberman <henry.beberman@microsoft.com> 4.2-1
- Add ntopng spec
- License verified
- Original version for CBL-Mariner
