%global rustflags '-Clink-arg=-Wl,-z,relro,-z,now'

Summary:        A rust-based reference implementation for provisioning Linux VMs on Azure.
Name:           azure-init
Version:        0.1.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/Azure/azure-init
Source0:        https://github.com/Azure/azure-init/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
Source2:        cargo-config
Patch0:         0001-add-Azure-Linux-support.patch
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
install -m 0644 config/azure-provisioning-agent.service %{buildroot}%{_unitdir}/azure-provisioning-agent.service
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
%systemd_post azure-provisioning-agent.service
systemctl enable azure-provisioning-agent

%preun
%systemd_preun azure-provisioning-agent.service

%postun
%systemd_postun azure-provisioning-agent.service

%files
%{_sharedstatedir}/azure-init/azure-init
%{_unitdir}/azure-provisioning-agent.service
%{_sysconfdir}/netplan/eth0.yaml

%changelog
* Wed May 08 2024 Sean Dougherty <sdougherty@microsoft.com> - 0.1.1-1
- Initial introduction to Azure Linux (license: MIT)
- License verified