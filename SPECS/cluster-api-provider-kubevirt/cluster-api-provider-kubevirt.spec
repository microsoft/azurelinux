Summary:        Package to create the cluster-api-provider-kubevirt binary.
Name:           cluster-api-provider-kubevirt
Version:        0.1.10
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/kubernetes-sigs/cluster-api-provider-kubevirt
Group:          System/Management
# The Group has been set to System/Management to mimic SPEC file of Kubevirt
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://github.com/kubernetes-sigs/cluster-api-provider-kubevirt/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# We can use the generate-source-tarball.sh script in the given folder along with the package version to build the tarball automatically.
# In case we need to re-build this file manually:
#   1. wget https://github.com/kubernetes-sigs/cluster-api-provider-kubevirt/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
Patch0:         golang-version-upgrade.patch
Patch1:         remove-caBundle-placeholder.patch
Patch2:         enforce-tls-1.2-on-webhooks.patch
Patch3:         patch-datavolume-based-on-kubernetes-version.patch
Patch4:         replace-cloudinit-configdrive-with-nocloud.patch
Patch5:         refactor-bootstrap-handling-for-faster-reconciliation.patch
Patch6:         nodeport-service-support-in-KubevirtCluster.patch
Patch7:         cleanup-vms-which-have-never-been-ready.patch
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
