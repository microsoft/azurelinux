Summary:        Package to create the cloud-provider-kubevirt binary.
Name:           cloud-provider-kubevirt
Version:        0.5.1
Release:        1%{?dist}
License:        MIT
URL:            https://github.com/kubevirt/cloud-provider-kubevirt/
Group:          System/Management
# The Group has been set to System/Management to mimic SPEC file of Kubevirt
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/kubevirt/cloud-provider-kubevirt/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         KCCM-Changes.patch
Patch1:         Golang-Version-Upgrade.patch
Patch2:         Modifying-Makefile-Target.patch
%global debug_package %{nil}
BuildRequires:  golang >= 1.22.11
BuildRequires:  golang-packaging

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
%autosetup -p1

%build
export GOPATH=%{our_gopath}
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
* Tue Feb 04 2025 Sharath Srikanth Chellappa <sharathsr@microsoft.com> 0.5.1-1
- Initial Versioning of cloud-provider-kubevirt package.