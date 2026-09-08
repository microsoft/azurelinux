# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%define RELEASE 1
%define rel 4
 %define _ver 0.12.1 

Summary: InfiniBand fabric simulator for management
%global upstream_name ibsim

Name: ibsim-ofed
Version: 0.12.1
Release: 4%{?dist}
Conflicts: ibsim
License: GPLv2 or BSD
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source6000: MLNX_OFED_SRC-26.04-0.8.5.0.tgz
Url: https://github.com/linux-rdma/ibsim
BuildRequires: rdma-core-ofed-devel, gcc

%description
ibsim provides simulation of infiniband fabric for using with
OFA OpenSM, diagnostic and management tools.

%prep
tar -xf %{SOURCE6000}
_ibsim_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/ibsim-%{version}-*.src.rpm' -print -quit)
if [ -z "$_ibsim_srpm" ]; then
	echo "ERROR: ibsim source RPM not found inside %{SOURCE6000}" >&2
	exit 1
fi
rpm2cpio "$_ibsim_srpm" | cpio -idm './ibsim-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf ibsim-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}

%build
export CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}"
export LDFLAGS="${LDFLAGS:-${RPM_OPT_FLAGS}}"
make prefix=%_prefix libpath=%_libdir binpath=%_bindir %{?_smp_mflags}

%install
export CFLAGS="${CFLAGS:-${RPM_OPT_FLAGS}}"
export LDFLAGS="${LDFLAGS:-${RPM_OPT_FLAGS}}"
make DESTDIR=${RPM_BUILD_ROOT} prefix=%_prefix libpath=%_libdir binpath=%_bindir install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/umad2sim/libumad2sim*.so*
%{_bindir}/ibsim
%{_bindir}/ibsim-run
%doc README COPYING TODO net-examples scripts

%changelog
* Mon May 04 2026 root - 0.12.1-4
Automated build 4
