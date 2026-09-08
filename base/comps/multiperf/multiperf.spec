%global upstream_name multiperf

Name:           multiperf
Summary:        IB Performance tests
Version:        3.0
Release: 3.0.2604085
License:        BSD 3-Clause, GPL v2 or later
Group:          Productivity/Networking/Diagnostic
Source0:        MLNX_OFED_SRC-26.04-0.8.5.0.tgz
Source6000:     MLNX_OFED_SRC-26.04-0.8.5.0.tgz
Url:            ""
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
# AZL: missing from upstream spec; required by ./configure and make.
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libibverbs-devel

%description
gen3 uverbs microbenchmarks

%prep
tar -xf %{SOURCE6000}
_multiperf_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/multiperf-%{version}-*.src.rpm' -print -quit)
if [ -z "$_multiperf_srpm" ]; then
	echo "ERROR: multiperf source RPM not found inside %{SOURCE6000}" >&2
	exit 1
fi
rpm2cpio "$_multiperf_srpm" | cpio -idm './multiperf-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf multiperf-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}

%build
%configure
# AZL: Makefile does not honor configure-exported CFLAGS; pass -fPIC
# explicitly so linking with -pie hardening does not fail. -D_GNU_SOURCE
# is needed because this GCC now errors (not warns) on the implicit
# strdupa() declaration, which strdupa needs to see as a real prototype.
%{__make} CFLAGS="%{optflags} -fPIC -D_GNU_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=%{buildroot} install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-, root, root)
%doc README COPYING
%_bindir/*
%changelog
* Sun Feb 08 2015 - gilr@mellanox.com
- Initial Package, Version 3.0
