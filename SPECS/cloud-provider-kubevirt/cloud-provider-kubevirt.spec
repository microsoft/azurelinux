Summary:        Package to create the cloud-provider-kubevirt binary.
Name:           cloud-provider-kubevirt
Version:        0.5.1
Release:        3%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubevirt/cloud-provider-kubevirt/
Group:          System/Management
# The Group has been set to System/Management to mimic SPEC file of Kubevirt
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/kubevirt/cloud-provider-kubevirt/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# We can use the generate-source-tarball.sh script in the given folder along with the package version to build the tarball automatically.
# In case we need to re-build this file manually:
#   1. wget https://github.com/kubevirt/cloud-provider-kubevirt/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. Apply golang-version-upgrade.patch
#   5. go mod vendor
#   6. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         initialization-and-configuration-handling.patch
Patch1:         single-ip-address-for-node.patch
Patch2:         golang-version-upgrade.patch
Patch3:         instanceexists-watches-vms-instead-of-vmis.patch
Patch4:         CVE-2025-11065.patch
%global debug_package %{nil}
BuildRequires:  golang < 1.25

%define our_gopath %{_topdir}/.gopath

%description
The KubeVirt cloud-provider allows a Kubernetes cluster running 
in KubeVirt VMs (tenant cluster) to interact with KubeVirt and 
Kubernetes (infrastructure cluster) to provision, manage and 
clean up resources. For example, the cloud-provider ensures that 
zone and region labels of nodes in the tenant cluster are set 
based on the zone and region of the KubeVirt VMs in the 
infrastructure cluster. The cloud-provider also ensures 
tenant cluster services of type LoadBalancer are properly 
exposed through services in the UnderKube.

%prep
%autosetup -N
rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner
%autopatch -p1

%build
export GOPATH=%{our_gopath}
export GOFLAGS="-mod=vendor"
make build

%install
mkdir -p %{buildroot}%{_bindir}

install -p -m 0755 bin/kubevirt-cloud-controller-manager %{buildroot}%{_bindir}/

%check
make test

%files
%defattr(-,root,root)
%{_bindir}/kubevirt-cloud-controller-manager

%changelog
* Fri Jan 30 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 0.5.1-3
- Patch for CVE-2025-11065

* Sun Aug 31 2025 Andrew Phelps <anphel@microsoft.com> - 0.5.1-2
- Set BR for golang to < 1.25

* Tue Feb 04 2025 Sharath Srikanth Chellappa <sharathsr@microsoft.com> 0.5.1-1
- Original version for Azure Linux.
- License verified.
