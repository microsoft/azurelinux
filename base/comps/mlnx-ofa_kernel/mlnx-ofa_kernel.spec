%global _name        mlnx-ofa_kernel
%global bundle_release   0.8.5.0
%global mlnx_ofa_release OFED.26.04.0.8.5.1
%global configure_options --with-core-mod --with-user_mad-mod --with-user_access-mod --with-addr_trans-mod --with-mlx5-mod --with-mlxfw-mod --with-ipoib-mod

Name:           mlnx-ofa_kernel
Version:        26.04
Release:        1%{?dist}
Summary:        NVIDIA / Mellanox OFED userspace utilities
License:        GPL-2.0-only
URL:            https://network.nvidia.com/products/infiniband-drivers/linux/mlnx_ofed/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        MLNX_OFED_SRC-%{version}-%{bundle_release}.tgz

BuildArch:      noarch
BuildRequires:  systemd-rpm-macros
BuildRequires:  cpio
BuildRequires:  rpm-build
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd

Requires:       kmod-mlnx-ofa_kernel-%{version}
Requires:       kmod
Requires:       coreutils
Requires:       pciutils
Requires:       grep
Requires:       procps-ng
Requires:       lsof
Requires:       iproute
Requires:       ethtool

%description
Userspace utilities for the NVIDIA / Mellanox InfiniBand and Ethernet drivers
(mlnx-ofa_kernel %{version}): openibd service, interface manager scripts,
ibdev2netdev, modprobe configs, and udev rules. The kernel modules themselves
ship in the matching kmod-mlnx-ofa_kernel-%{version} package.

%package source
Summary:        Source of the mlnx-ofa_kernel driver
BuildArch:      noarch

%description source
Pristine source of the mlnx-ofa_kernel %{version} driver under
/usr/src/ofa_kernel-%{version}/source/.

%prep
%setup -T -c -n %{_name}-%{version}
tar -xf %{SOURCE0} --wildcards --strip-components=2 \
    'MLNX_OFED_SRC-*/SRPMS/mlnx-ofa_kernel-*.src.rpm'
rpm2cpio mlnx-ofa_kernel-%{version}-%{mlnx_ofa_release}.src.rpm \
    | cpio -idm '*mlnx-ofa_kernel-%{version}.tgz'
tar -xf mlnx-ofa_kernel-%{version}.tgz --strip-components=1
rm -f mlnx-ofa_kernel-%{version}-%{mlnx_ofa_release}.src.rpm \
      mlnx-ofa_kernel-%{version}.tgz

%build
# Intentionally empty: userspace ships as plain scripts/configs/units.

%install
SRC=ofed_scripts

# Init script + systemd units
install -D -m 0755 $SRC/openibd                       %{buildroot}%{_sysconfdir}/init.d/openibd
install -D -m 0644 $SRC/openibd.service               %{buildroot}%{_unitdir}/openibd.service
install -D -m 0644 $SRC/mlnx_interface_mgr@.service   %{buildroot}%{_unitdir}/mlnx_interface_mgr@.service

# Configs
install -D -m 0644 $SRC/openib.conf                   %{buildroot}%{_sysconfdir}/infiniband/openib.conf
install -D -m 0644 $SRC/mlx5.conf                     %{buildroot}%{_sysconfdir}/infiniband/mlx5.conf
install -D -m 0644 $SRC/mlnx.conf                     %{buildroot}%{_sysconfdir}/modprobe.d/mlnx.conf
install -D -m 0644 $SRC/mlnx-bf.conf                  %{buildroot}%{_sysconfdir}/modprobe.d/mlnx-bf.conf
install -D -m 0644 $SRC/ib_ipoib.conf                 %{buildroot}%{_sysconfdir}/modprobe.d/ib_ipoib.conf

# Udev rules + helpers
install -D -m 0644 $SRC/83-mlnx-sf-name.rules         %{buildroot}/lib/udev/rules.d/83-mlnx-sf-name.rules
install -D -m 0644 $SRC/90-ib.rules                   %{buildroot}/lib/udev/rules.d/90-ib.rules
install -D -m 0755 $SRC/sf-rep-netdev-rename          %{buildroot}/lib/udev/sf-rep-netdev-rename
install -D -m 0755 $SRC/auxdev-sf-netdev-rename       %{buildroot}/lib/udev/auxdev-sf-netdev-rename

# Interface manager + conf manager — openibd calls these by absolute /bin path.
install -D -m 0755 $SRC/mlnx_conf_mgr.sh              %{buildroot}/bin/mlnx_conf_mgr.sh
install -D -m 0755 $SRC/mlnx_interface_mgr.sh         %{buildroot}/bin/mlnx_interface_mgr.sh

# sbin tools
install -D -m 0755 $SRC/ibdev2netdev                  %{buildroot}%{_sbindir}/ibdev2netdev
install -D -m 0755 $SRC/setup_mr_cache.sh             %{buildroot}%{_sbindir}/setup_mr_cache.sh
install -D -m 0755 $SRC/mlnx_drv_ctl                  %{buildroot}%{_sbindir}/mlnx_drv_ctl

# /usr/share/mlnx_ofed/ helpers
install -d %{buildroot}%{_datadir}/mlnx_ofed
install -m 0755 $SRC/mlnx_bf_assign_ct_cores.sh       %{buildroot}%{_datadir}/mlnx_ofed/mlnx_bf_assign_ct_cores.sh
install -m 0755 $SRC/mod_load_funcs                   %{buildroot}%{_datadir}/mlnx_ofed/mod_load_funcs

cat > %{buildroot}%{_sysconfdir}/infiniband/info << EOFINFO
#!/bin/bash
echo prefix=%{_prefix}
echo
echo "Configure options: %{configure_options}"
echo
EOFINFO
chmod 0755 %{buildroot}%{_sysconfdir}/infiniband/info

mkdir -p %{buildroot}%{_prefix}/src/ofa_kernel-%{version}/source
cp -a %{_builddir}/%{name}-%{version}/. \
      %{buildroot}%{_prefix}/src/ofa_kernel-%{version}/source/
ln -s ofa_kernel-%{version}/source \
      %{buildroot}%{_prefix}/src/mlnx-ofa_kernel-%{version}

%post
%systemd_post openibd.service

%preun
%systemd_preun openibd.service

%postun
%systemd_postun_with_restart openibd.service

%files
%license COPYING
%doc ofed_scripts/82-net-setup-link.rules
%doc ofed_scripts/vf-net-link-name.sh
%dir %{_sysconfdir}/infiniband
%config(noreplace) %{_sysconfdir}/infiniband/openib.conf
%config(noreplace) %{_sysconfdir}/infiniband/mlx5.conf
%{_sysconfdir}/infiniband/info
%{_sysconfdir}/init.d/openibd
%{_unitdir}/openibd.service
%{_unitdir}/mlnx_interface_mgr@.service
%config(noreplace) %{_sysconfdir}/modprobe.d/mlnx.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/mlnx-bf.conf
%config(noreplace) %{_sysconfdir}/modprobe.d/ib_ipoib.conf
/lib/udev/sf-rep-netdev-rename
/lib/udev/auxdev-sf-netdev-rename
/lib/udev/rules.d/83-mlnx-sf-name.rules
/lib/udev/rules.d/90-ib.rules
%{_datadir}/mlnx_ofed/
%{_sbindir}/ibdev2netdev
%{_sbindir}/setup_mr_cache.sh
%{_sbindir}/mlnx_drv_ctl
/bin/mlnx_interface_mgr.sh
/bin/mlnx_conf_mgr.sh

%files source
%license COPYING
%{_prefix}/src/ofa_kernel-%{version}/source
%{_prefix}/src/mlnx-ofa_kernel-%{version}

%changelog
* Thu Jun 11 2026 Elaheh Dehghani <edehghani@microsoft.com> - 26.04-1
- Initial AZL4 import: userspace + source companion to kmod-mlnx-ofa.
