%global rustflags '-Clink-arg=-Wl,-z,relro,-z,now'

Summary:        A rust-based reference implementation for provisioning Linux VMs on Azure.
Name:           azure-init
Version:        7142bced859169553e8948497aa13df742aac1ff
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/Azure/azure-init
Source0:        https://github.com/Azure/azure-init/archive/refs/tags/v%{version}.tar.gz#/%{name}-local.tar.gz
Source1:        %{name}-local-vendor.tar.gz
Source2:        cargo-config
# Patch0:         0001-add-Azure-Linux-support.patch
BuildRequires:  cargo
BuildRequires:  rust
BuildRequires:  libudev-devel
BuildRequires:  systemd-rpm-macros
Requires:       systemd

%description
An open-source lightweight rust-based replacement for cloud-init, maintained by Microsoft's Cloud Provisioning team 

%prep
%autosetup -p1
tar -xf %{SOURCE1}
mkdir -p .cargo
cp %{SOURCE2} .cargo/config

%build
cargo build --all

%install
mkdir -p %{buildroot}%{_sharedstatedir}/azure-init
mkdir -p %{buildroot}%{_unitdir}
install -m 0755 target/debug/azure-init %{buildroot}%{_sharedstatedir}/azure-init/azure-init
install -m 0644 config/azure-init.service %{buildroot}%{_unitdir}/azure-init.service
mkdir -p %{buildroot}%{_sysconfdir}/netplan
cat > %{buildroot}%{_sysconfdir}/netplan/eth0.yaml <<EOF
network:
    ethernets:
        eth0:
            dhcp4: true
            dhcp4-overrides:
                route-metric: 100
            dhcp6: false
            match:
                driver: hv_netvsc
                name: eth0
EOF
chmod 0644 %{buildroot}%{_sysconfdir}/netplan/eth0.yaml


%post
%systemd_post azure-init.service
systemctl enable azure-init

%preun
%systemd_preun azure-init.service

%postun
%systemd_postun azure-init.service

%files
%{_sharedstatedir}/azure-init/azure-init
%{_unitdir}/azure-init.service
%{_sysconfdir}/netplan/eth0.yaml

%changelog
* Thu Jun 20 2024 Sean Dougherty <sdougherty@microsoft.com> - 0.1.1-2
- Test Dongsu Park's PR86 in azure-init

* Wed May 08 2024 Sean Dougherty <sdougherty@microsoft.com> - 0.1.1-1
- Initial introduction to Azure Linux (license: MIT)
- License verified