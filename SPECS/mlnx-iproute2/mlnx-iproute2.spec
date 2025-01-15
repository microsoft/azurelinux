# This is a version of iproute2.spec sent to upstream with mlnx customization.

# On e.g. Mariner, __make is set to {_bindir}/make which gets broken when
# you modify _prefix that modifies _bindir. Use 'global' to save this with
# the original value. This works with a simple macro such as __make but
# should probably not ne used with more complex ones:
%global __make %{__make}

%global _prefix /opt/mellanox/iproute2
%global _exec_prefix %{_prefix}
%global package_name mlnx-iproute2
%global package_version 6.10.0
%global configs_under_prefix 1
%global netns_package_name netns-mlnx

# Specify mandatory rpmbuild parameter package_version, like:
#   rpmbuild -d'package_version 5.1.0'
#
# Other optional parameters are: package_name, netns_package_name
# and configs_under_prefix.

%global debug_package %{nil}

%{!?package_name: %global package_name iproute2}
%{!?netns_package_name: %global netns_package_name netns}

%if 0%{?configs_under_prefix:1}
	%global config_dir %{_prefix}%{_sysconfdir}
	%global netns_config_dir %{config_dir}/netns
%else
	%global config_dir %{_sysconfdir}/mlnx-iproute2
	%global netns_config_dir %{_sysconfdir}/%{netns_package_name}
%endif

Summary:	Advanced IP routing and network device configuration tools
Name:		mlnx-iproute2
Version:	6.10.0
Release:        2%{?dist}
License:	GPLv2
Group:		Networking/Admin
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://linux.mellanox.com/public/repo/mlnx_ofed/24.10-0.7.0.0/SRPMS/mlnx-iproute2-6.10.0.tar.gz#/%{name}-%{version}.tar.gz
URL:		http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2
ExclusiveArch:   x86_64

BuildRequires:	bison
BuildRequires:	flex
BuildRoot:	/var/tmp/%{name}-%{version}-build

%description
The iproute package contains networking utilities (like ip and tc)
designed to use the advanced networking capabilities of the Linux kernel.

%package -n libnetlink-devel
Summary:	Library for the netlink interface
Group:		Development/Libraries

%description -n libnetlink-devel
This library provides an interface for kernel-user netlink interface.

# The dependency on libdb-5.3 comes from arpd. This tool is not really
# used in our package. In some platforms libdb-5.3 is not available by
# default even though we include the devel package on the build system.
# But users don't really need arpd from this package.
%global __requires_exclude_from sbin/arpd

%prep
%setup -q

%build
./configure
%{__make} \
	CC="%{__cc}" \
	PREFIX="%{_prefix}" \
	LIBDIR="%{_libdir}" \
	SBINDIR="%{_sbindir}" \
	CONF_ETC_DIR="%{config_dir}/etc" \
	CONF_USR_DIR="%{config_dir}/usr" \
	NETNS_RUN_DIR="%{_var}/run/%{netns_package_name}" \
	NETNS_ETC_DIR="%{netns_config_dir}" \

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT	\
	PREFIX="%{_prefix}" \
	LIBDIR="%{_libdir}" \
	SBINDIR="%{_sbindir}" \
	CONF_ETC_DIR="%{config_dir}/etc" \
	CONF_USR_DIR="%{config_dir}/usr" \
	NETNS_RUN_DIR="%{_var}/run/%{netns_package_name}" \
	NETNS_ETC_DIR="%{netns_config_subdir}" \

install -m 644 lib/libnetlink.a $RPM_BUILD_ROOT%{_libdir}
install -m 644 include/libnetlink.h $RPM_BUILD_ROOT%{_includedir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%doc README README.devel
%config(noreplace) %verify(not md5 mtime size) %{config_dir}/*
%{_prefix}/include/*
%{_prefix}/share/*
%{_libdir}/*
%{_sbindir}/*

%changelog
* Tue Dec  17 2024 Binu Jose Philip <bphilip@microsoft.com>
- Initial Azure Linux import from NVIDIA (license: GPLv2)
- License verified
