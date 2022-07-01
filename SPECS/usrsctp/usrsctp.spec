Summary:        A portable SCTP userland stack
Name:           usrsctp
Version:        0.9.5.0
Release:        1%{?dist}
License:        LGPLv2+ AND CC0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/sctplab/usrsctp
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make

%description
SCTP is a message oriented, reliable transport protocol with direct support for
multihoming that runs on top of IP or UDP, and supports both v4 and v6 versions.

Like TCP, SCTP provides reliable, connection oriented data delivery with
congestion control. Unlike TCP, SCTP also provides message boundary
preservation, ordered and unordered message delivery, multi-streaming
and multi-homing. Detection of data corruption, loss of data and duplication of
data is achieved by using checksums and sequence numbers. A selective
retransmission mechanism is applied to correct loss or corruption of data.

%package devel
Summary:        A portable SCTP userland stack
Group:          Development/Libraries
Requires:       %{name} = %{version}

%description devel
usrsctp header files and libraries for developments

%prep
%autosetup
mkdir build

%build
cd build
%cmake -DCMAKE_BUILD_TYPE=Release ..
%make_build

%install
cd build
%make_install

%files
%defattr(-,root,root)
%license LICENSE.md
%{_libdir}/*.so.*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Fri May 20 2022 Rahul Sharma <sharmarahu@microsoft.com> - 0.9.5.0-1
- Initial SPEC
- Initial CBL-Mariner import from Azure (license: MIT).
- License verified.
