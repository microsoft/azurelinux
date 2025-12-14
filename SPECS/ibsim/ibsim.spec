
%define RELEASE 1
%define rel %{?CUSTOM_RELEASE}%{!?CUSTOM_RELEASE:%RELEASE}

Summary:	 InfiniBand fabric simulator for management
Name:		 ibsim
Version:	 0.12.1
Release:	 1%{?dist}
License:	 GPLv2 or BSD
Group:		 System Environment/Libraries
BuildRoot:	 %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# DOCA OFED feature sources come from the following MLNX_OFED_SRC tgz.
# This archive contains the SRPMs for each feature and each SRPM includes the source tarball and the SPEC file.
# https://linux.mellanox.com/public/repo/doca/3.1.0/SOURCES/mlnx_ofed/MLNX_OFED_SRC-25.07-0.9.7.0.tgz
Source0:         %{_distro_sources_url}/ibsim-%{version}.tar.gz
Url:		 https://github.com/linux-rdma/ibsim
Vendor:          Microsoft Corporation
Distribution:    Azure Linux

BuildRequires: libibmad-devel
BuildRequires: libibumad-devel
BuildRequires: gcc

%description
ibsim provides simulation of infiniband fabric for using with
OFA OpenSM, diagnostic and management tools.

%prep
%setup -q

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
%doc README TODO net-examples scripts
%license COPYING

%changelog
* Tue Nov 04 2025 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.12.1-1
- Upgrade version to 0.12.1.
- Update source path
* Mon Sep 15 2025 Elaheh Dehghani <edehghani@microsoft.com> - 0.12-2
- Enable ARM64 build by removing ExclusiveArch
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com> - 0.12-1
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
