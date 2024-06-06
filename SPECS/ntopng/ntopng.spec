%global nDPIver 4.2
Summary:        Web-based Network Traffic Monitoring Application
Name:           ntopng
Version:        6.0
Release:        1%{?dist}
License:        GPLv3
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://www.ntop.org/
#Source0:       https://github.com/ntop/ntopng/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
#Source1:       https://github.com/ntop/nDPI/archive/%{nDPIver}.tar.gz
Source1:        nDPI-%{nDPIver}.tar.gz
Patch1:         CVE-2021-45985.patch
Patch2:         CVE-2022-28805.patch
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
* Wed Jun 05 2024 Nicolas Guibourge <nicolasg@microsoft.com> - 6.0-1
- Upgrade to 6.0 and patch CVE-2022-28805 on integrated lua source

* Tue Apr 18 2023 Bala <balakumaran.kannan@microsoft.com> - 5.2.1-2
- Patch CVE-2021-45985 on integrated lua source

* Thu Feb 24 2022 Max Brodeur-Urbas <maxbr@microsoft.com> - 5.2.1-1
- Upgrading to v5.2.1
- Upgrading nDPI to v4.2

* Fri Feb 26 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 4.2-2
- Updating source URLs.

* Fri Feb 05 2021 Henry Beberman <henry.beberman@microsoft.com> - 4.2-1
- Add ntopng spec
- License verified
- Original version for CBL-Mariner
