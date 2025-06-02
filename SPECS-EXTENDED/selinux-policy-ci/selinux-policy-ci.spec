%global modulename hotfix

Summary:        Azure Linux CI SELinux policy
Name:           selinux-policy-ci
Version:        1.0
Release:        1%{?dist}
License:        Proprietary
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/microsoft/azurelinux
Source0:        hotfix.te
Source1:        azureci.te
Source2:        ci_unconfined_u

BuildArch:      noarch
Requires:       selinux-policy
Requires(post): selinux-policy
BuildRequires:  selinux-policy
BuildRequires:  selinux-policy-devel
%{?selinux_requires}

%description
SELinux policy for Azure Linux CI.

%prep
cp %{SOURCE0} %{SOURCE1} .

%build
make -f %{_datadir}/selinux/devel/Makefile hotfix.pp azureci.pp
# remove cloudinit_manage_non_security rules as it breaks CI.  azureci.te has
# replacement rules.
semodule -c -X 100 -E cloudinit
sed -i '/(booleanif (cloudinit_manage_non_security)/,/^)/d' cloudinit.cil

# remove CI-breaking rules for cron.
semodule -c -X 100 -E cron
sed -r -i -e '/(cifs_t|nfs_t|fusefs_t|user_home_t)/s/execute(_no_trans)?//g' cron.cil
sed -r -i -e '/system_cronjob_t usr_t \(file/s/execute(_no_trans)?//g' cron.cil

# remove init_create_mountpoints as it breaks CI.  azureci.te has replacement rules.
semodule -c -X 100 -E init
sed -i '/(booleanif (and (init_create_mountpoints) (init_mounton_non_security))/,/^)/d' init.cil
sed -i '/(booleanif (init_create_mountpoints)/,/^)/d' init.cil
sed -i '/(booleanif (init_mounton_non_security)/,/^)/d' init.cil
sed -r -i -e '/init_t init_mountpoint_type \(file/s/mounton//g' init.cil
sed -r -i -e '/init_t var_run_t/s/execute(_no_trans)?//g' init.cil
sed -r -i -e '/initrc_t initrc_tmp_t/s/execute(_no_trans)?//g' init.cil

# replace sysadm with ci_unconfined in locallogin
semodule -c -X 100 -E locallogin
sed -i -e 's/sysadm/ci_unconfined/' locallogin.cil

# remove CI-breaking rules for mount
semodule -c -X 100 -E mount
sed -r -i -e '/mount_t mountpoint \(file/s/mounton//g' mount.cil
sed -r -i -e '/mount_t non_security_file_type \(file/s/mounton//g' mount.cil

# remove semanage temp file exec as it breaks CI.  May lead to breakage if python3-networkx
# is installed (unlikely). See https://github.com/SELinuxProject/refpolicy/commit/a114d07fd3c8675533f7f0670055ec895e09c19b
semodule -c -X 100 -E selinuxutil
sed -r -i -e '/semanage_t semanage_tmp_t/s/execute(_no_trans)?//g' selinuxutil.cil

# remove CI-breaking rules for dhcp client.
semodule -c -X 100 -E sysnetwork
sed -r -i -e '/dhcpc_t dhcp_etc_t/s/execute(_no_trans)?//g' sysnetwork.cil

# remove systemd_tmpfiles_manage_all as it breaks CI.  azureci.te has
# replacement rules.
semodule -c -X 100 -E systemd
sed -i '/(booleanif (systemd_tmpfiles_manage_all)/,/^)/d' systemd.cil

# remove CI-breaking rules for virt.
semodule -c -X 100 -E virt
sed -r -i -e '/virtd_t virt_tmp_t/s/execute(_no_trans)?//g' virt.cil

%install
mkdir -p %{buildroot}%{_datadir}/selinux/packages/targeted/
install -D -m 0644 *.pp *.cil %{buildroot}%{_datadir}/selinux/packages/targeted/
install -D -m 0644 %{SOURCE2} %{buildroot}/etc/selinux/targeted/contexts/users/ci_unconfined_u

%pre
%selinux_relabel_pre

%post
cd %{_datadir}/selinux/packages/targeted/
%selinux_modules_install -p 200 {cloudinit,cron,locallogin,init,mount,selinuxutil,sysnetwork,systemd,virt}.cil {hotfix,azureci}.pp

%postun
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -p 200 hotfix azureci cron locallogin cloudinit init mount selinuxutil sysnetwork systemd virt
fi

%posttrans
%selinux_relabel_post

%files
/etc/selinux/targeted/contexts/users/ci_unconfined_u
%{_datadir}/selinux/packages/targeted/*

%changelog
* Mon Jun 02 2025 Dallas Delaney <dadelan@microsoft.com> - 1.0-1
- Add package to specs-extended
- License verified
- Original version for Azure Linux
