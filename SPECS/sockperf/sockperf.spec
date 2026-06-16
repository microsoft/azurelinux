# https://linux.mellanox.com/public/repo/doca/3.3.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-26.01-1.0.0.0.tgz
Summary:        Network Benchmarking Utility for high-performance systems
Name:           sockperf
Version:        3.1
Release:        1%{?dist}
License:        BSD-3-Clause
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/Mellanox/sockperf
Source0:        %{_distro_sources_url}/%{name}-%{version}_doca-3.3.0.tar.gz
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool
BuildRequires:  m4
BuildRequires:  perl
ExclusiveArch:  x86_64

%description
sockperf is a network benchmarking utility over socket API that was designed
for testing performance (latency and throughput) of high-performance systems.
It covers most of the socket API calls and options and can measure latency
of each discrete packet at sub-nanosecond resolution.

%prep
%setup -n %{name}-%{version}

%build
# Run autogen.sh if configure doesn't exist
if [ ! -f configure ]; then
    ./autogen.sh
fi
%configure
%make_build

%install
%make_install

%files
%defattr(-,root,root)
%license copying
%{_bindir}/sockperf
%doc /usr/share/doc/sockperf/README.md
%doc /usr/share/doc/sockperf/authors
%doc /usr/share/doc/sockperf/news
%doc /usr/share/doc/sockperf/version
%doc /usr/share/doc/sockperf/copying

%changelog
* Mon May 11 2026 Azure Linux Team - 3.1-1
- Upgrade to DOCA 3.3.0 (OFED 26.01-1.0.0.0)

* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Initial Azure Linux import from NVIDIA (license: BSD).
- License verified
