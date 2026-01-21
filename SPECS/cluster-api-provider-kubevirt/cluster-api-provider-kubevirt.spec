Summary:        Package to create the cluster-api-provider-kubevirt binary.
Name:           cluster-api-provider-kubevirt
Version:        0.11.0
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes-sigs/cluster-api-provider-kubevirt
Group:          System/Management
# The Group has been set to System/Management to mimic SPEC file of Kubevirt
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/kubernetes-sigs/cluster-api-provider-kubevirt/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0:         makefile-upgrade.patch
Patch1:         remove-caBundle-placeholder.patch
Patch2:         patch-datavolume-based-on-kubernetes-version.patch
Patch3:         replace-cloudinit-configdrive-with-nocloud.patch
Patch4:         refactor-bootstrap-handling-for-faster-reconciliation.patch
Patch5:         nodeport-service-support-in-KubevirtCluster.patch
Patch6:         cleanup-vms-which-have-never-been-ready.patch
%global debug_package %{nil}
BuildRequires:  gcc
BuildRequires:  build-essential
BuildRequires:  golang >= 1.24

%define our_gopath %{_topdir}/.gopath

%description
The Cluster API brings declarative Kubernetes-style APIs 
to cluster creation, configuration and management. 
The API itself is shared across multiple cloud providers
allowing for true Kubevirt hybrid deployments of Kubernetes.

%prep
%autosetup -N
rm -rf vendor
tar -xf %{SOURCE1} --no-same-owner
%autopatch -p1

%build
export GOPATH=%{our_gopath}
export GOFLAGS="-mod=vendor"
make manager

%install
mkdir -p %{buildroot}%{_bindir}

install -p -m 0755 bin/manager %{buildroot}%{_bindir}/cluster-api-provider-kubevirt-manager

%check
make test

%files
%defattr(-,root,root)
%{_bindir}/cluster-api-provider-kubevirt-manager

%changelog
* Tue Feb 04 2025 Sharath Srikanth Chellappa <sharathsr@microsoft.com> 0.5.1-1
- Original version for Azure Linux.
- License verified.
