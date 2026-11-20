## START: Set by rpmautospec
## (rpmautospec version 0.8.3)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This is a version of iproute2.spec sent to upstream with mlnx customization.

# On e.g. Mariner, __make is set to {_bindir}/make which gets broken when
# you modify _prefix that modifies _bindir. Use 'global' to save this with
# the original value. This works with a simple macro such as __make but
# should probably not ne used with more complex ones:
%global __make %{__make}

%global _prefix /opt/mellanox/iproute2
%global _exec_prefix %{_prefix}
# AZL: keep the vendor sbin/ layout under the private prefix (vendor tools such
# as sysinfo-snapshot.py call /opt/mellanox/iproute2/sbin/*); the distro
# default maps sbindir to bin.
%global _sbindir %{_exec_prefix}/sbin
%global package_name mlnx-iproute2
%global package_version 6.18.0
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
%global upstream_name mlnx-iproute2

Name:		mlnx-iproute2
Version:	2604.0.0
Release:	%autorelease
# Mix of GPL-2.0-only and GPL-2.0-or-later sources; the netem
# distribution tables are NIST-PD.
License:	GPL-2.0-only AND GPL-2.0-or-later AND NIST-PD
Group:		Networking/Admin
Source6000:	MLNX_OFED_SRC-26.04-0.8.5.0.tgz
URL:		http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2
BuildRequires:	bison
BuildRequires:	flex
BuildRequires: libmnl-devel
# AZL: missing from upstream spec; required by ./configure and make.
BuildRequires: gcc
BuildRequires: make
BuildRequires: pkgconfig
BuildRequires: cpio
# AZL: optional features that ./configure silently disables when missing;
# this matches the build dependencies NVIDIA's installer (install.pl) uses
# for mlnx-iproute2 (tc xt actions, eBPF object loading, SELinux in ss, arpd).
BuildRequires: iptables-devel
BuildRequires: elfutils-libelf-devel
BuildRequires: libdb-devel
BuildRequires: libselinux-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The iproute package contains networking utilities (like ip and tc)
designed to use the advanced networking capabilities of the Linux kernel.

# AZL: the vendor declares libnetlink-devel without a %%files section, so it is
# never built; libnetlink.a and its headers ship in the main package as in the
# vendor build.
%package -n libnetlink-devel
Summary:	Library for the netlink interface
Group:		Development/Libraries

%description -n libnetlink-devel
This library provides an interface for kernel-user netlink interface.
# AZL: the vendor excludes arpd's automatic libdb dependency because libdb
# is missing on some of its platforms; libdb is available here, so keep the
# dependency to avoid shipping a broken arpd.

%prep
tar -xf %{SOURCE6000}
_mlnx_iproute2_srpm=$(find MLNX_OFED_SRC-* -path '*/SRPMS/mlnx-iproute2-%{version}-*.src.rpm' -print -quit)
if [ -z "$_mlnx_iproute2_srpm" ]; then
	echo "ERROR: mlnx-iproute2 source RPM not found inside %{SOURCE6000}" >&2
	exit 1
fi
rpm2cpio "$_mlnx_iproute2_srpm" | cpio -idm './mlnx-iproute2-%{version}.tar.gz'
rm -rf MLNX_OFED_SRC-*
tar -xf mlnx-iproute2-%{version}.tar.gz
%setup -q -T -D -n %{upstream_name}-%{version}

%build
./configure
%{__make} %{?_smp_mflags} \
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
	NETNS_ETC_DIR="%{netns_config_dir}" \

install -m 644 lib/libnetlink.a $RPM_BUILD_ROOT%{_libdir}
install -m 644 include/libnetlink.h $RPM_BUILD_ROOT%{_includedir}
# AZL: pre-create the private doc/license parents so they can be owned below.
install -d $RPM_BUILD_ROOT%{_prefix}/share/doc $RPM_BUILD_ROOT%{_prefix}/share/licenses

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%license COPYING
%doc README README.devel
# AZL: own the private prefix hierarchy; /opt/mellanox is shared with other
# MLNX OFED packages.
%dir /opt/mellanox
%dir %{_prefix}
%dir %{config_dir}
# AZL: CONF_USR_DIR holds read-only vendor defaults (rt_tables, rt_protos,
# ...), like /usr/share/iproute2 in the distro iproute, so they are not
# %%config; local overrides go in CONF_ETC_DIR, which is not populated.
%{config_dir}/usr
%{_prefix}/include
%dir %{_prefix}/share
%dir %{_prefix}/share/doc
%dir %{_prefix}/share/licenses
%{_prefix}/share/bash-completion
%{_prefix}/share/man
%{_libdir}
%{_sbindir}

%changelog
## START: Generated by rpmautospec
* Fri Nov 20 2026 Elaheh Dehghani <edehghani@microsoft.com> - 2604.0.0-2
- feat(mlnx-iproute2): add mlnx-iproute2 component

* Thu Jan 01 1970 azldev <> - 2604.0.0-1
- Initial sources
## END: Generated by rpmautospec
