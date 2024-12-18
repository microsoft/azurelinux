
%define RELEASE 2
%define rel %{?CUSTOM_RELEASE}%{!?CUSTOM_RELEASE:%RELEASE}

Summary:	 InfiniBand fabric simulator for management
Name:		 ibsim
Version:	 0.12
Release:	 %rel.2410068%{?dist}
License:	 GPLv2 or BSD
Group:		 System Environment/Libraries
BuildRoot:	 %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Source0:         https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/ibsim-0.12.tar.gz#/ibsim-%{version}.tar.gz
Url:		 https://github.com/linux-rdma/ibsim

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
%doc README COPYING TODO net-examples scripts

%changelog
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Moving to core from azlinux-ai-ml repo
* Thu Nov 07 2024 Suresh Babu Chalamalasetty <schalam@microsoft.com>
- Initial version Azure Linux
