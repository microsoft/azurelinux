%global upstream_name mlnx-ethtool

%if 0%{?_ver:1}
%define ver 2604.0.0
%else
%define ver 6.4
%endif

%if 0%{?_rel:1}
%define rel 1
%else
%define rel 1
%endif

%global _prefix /opt/mellanox/ethtool

Name: mlnx-ethtool
Version: 2604.0.0
Release: 1%{?dist}
Group		: Utilities

Summary		: Settings tool for Ethernet and other network devices

License		: GPL
URL		: https://ftp.kernel.org/pub/software/network/ethtool/

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc-c++
BuildRequires: libmnl-devel
Buildroot	: %{_tmppath}/%{name}-%{version}
Source0		: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
Source6000: MLNX_OFED_SRC-26.04-0.8.5.0.tgz


%description
This utility allows querying and changing settings such as speed,
port, auto-negotiation, PCI locations and checksum offload on many
network devices, especially Ethernet devices.

%prep
tar -xf %{SOURCE6000}
_mlnx_ethtool_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/mlnx-ethtool-%{version}-*.src.rpm' -print -quit)
if [ -z "$_mlnx_ethtool_srpm" ]; then
	echo "ERROR: mlnx-ethtool source RPM not found inside %{SOURCE6000}" >&2
	exit 1
fi
rpm2cpio "$_mlnx_ethtool_srpm" | cpio -idm './mlnx-ethtool-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf mlnx-ethtool-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}


%build
./autogen.sh
CFLAGS="${RPM_OPT_FLAGS}" ./configure --prefix=%{_prefix} --mandir=%{_mandir}
make


%install
make install DESTDIR=${RPM_BUILD_ROOT}


%files
%defattr(-,root,root)
# AZL: upstream's autotools build always installs to a literal sbin/
# subdirectory; %{_sbindir} on this distro maps to .../bin instead.
%{_prefix}/sbin/ethtool
%{_mandir}/man8/ethtool.8*
%{_datadir}/bash-completion/completions/ethtool
%{_datadir}/metainfo/org.kernel.software.network.ethtool.metainfo.xml
%doc AUTHORS COPYING NEWS README


%changelog
* Sun Apr 19 2026 root - 2604.0.0-1
Automated build 1
