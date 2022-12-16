Summary:        Lightweight Kubernetes
Name:           k3s
Version:        1.23.8
Release:        4%{?dist}
License:        ASL 2.0
Group:          System Environment/Base
URL:            http://k3s.io
Source0:        https://github.com/k3s-io/%{name}/archive/refs/tags/v%{version}+k3s2.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# We are also pre-cloning 3 git repositories
# How to re-build this file:
# 1. wget https://github.com/k3s-io/%%{name}/archive/refs/tags/v%%{version}+k3s2.tar.gz -O %%{name}-%%{version}.tar.gz
# 2. tar -xf %%{name}-%%{version}.tar.gz
# 3. cd %%{name}-%%{version}-k3s2
# 4. go mod vendor
# 5. pushd vendor
# 6. git clone --single-branch --branch="v1.5.13-k3s1" --depth=1 https://github.com/k3s-io/containerd
# 7. git clone -b "v1.1.1-k3s1" https://github.com/rancher/plugins.git
# 8. git clone --single-branch --branch="v1.1.2" --depth=1 https://github.com/opencontainers/runc
# 9. popd
# 10. tar -cf %%{name}-%%{version}-vendor.tar.gz vendor
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         vendor_build-1.23.8.patch
%global debug_package %{nil}
%define install_path  /usr/local/bin
%define util_path     %{_datadir}/k3s
%define install_sh    %{util_path}/setup/install.sh
%define uninstall_sh  %{util_path}/setup/uninstall.sh
%define k3s_binary    k3s
BuildRequires:  golang
BuildRequires:  libseccomp-devel
BuildRequires:  btrfs-progs-devel
Requires:       apparmor-parser
# K3s on Mariner is supported on x86_64 only:
ExclusiveArch:  x86_64
# Note: k3s is not exclusive with coredns, etcd, containerd, runc and other CBL-Mariner packages which it embeds.
# This means there may be multiple versions of these packages. At this time exclusivity is not being enforced to
# allow k3s to use its required version even when other versions are installed.

%description
The certified Kubernetes distribution built for IoT & Edge computing.

%prep
%autosetup -p1 -n %{name}-%{version}-k3s2
tar -xvf %{SOURCE1}

%build
mkdir -p build/static
mkdir etc
./scripts/build
./scripts/package-cli

%install
install -d %{buildroot}%{install_path}
install dist/artifacts/%{k3s_binary} %{buildroot}%{install_path}/%{k3s_binary}
install -d %{buildroot}%{util_path}/setup
install package/rpm/install.sh %{buildroot}%{install_sh}

%post
export INSTALL_K3S_SKIP_DOWNLOAD=true
export INSTALL_K3S_SKIP_ENABLE=true
export INSTALL_K3S_SKIP_START=true
export UNINSTALL_K3S_SH=%{uninstall_sh}

%{install_sh}
exit 0

%postun
# do not run uninstall script on upgrade
if [ $1 = 0 ]; then
    %{uninstall_sh}
    rm -rf %{util_path}
fi
exit 0

%files
%{install_path}/k3s
%{install_sh}

%changelog
* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.23.8-4
- Bump release to rebuild with go 1.18.9

* Thu Dec 08 2022 Vinayak Gupta <guptavinayak@microsoft.com> - 1.23.8-3
- Update the vendor tarball with the corrected versions of the dependencies

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.8-2
- Bump release to rebuild with go 1.18.8

* Fri Jul 29 2022 Lior Lustgarten <lilustga@microsoft.com> - 1.23.8-1
- Update to 1.23.8

* Thu Jul 21 2022 Lior Lustgarten <lilustga@microsoft.com> 1.23.6-3
- Fixes the install section. Allows integration of k3s at runtime in the Mariner build environment.

* Wed Jun 29 2022 Lior Lustgarten <lilustga@microsoft.com> 1.23.6-2
- Fixed uninstall path
- Added exclusivity for x86_64

* Thu Jun 23 2022 Lior Lustgarten <lilustga@microsoft.com> 1.23.6-1
- Switched to building using the upstream k3s tarball and a separate vendor tarball

* Tue May 24 2022 Manuel Huber <mahuber@microsoft.com> 1.23.6-1
- Changes to install phase on Mariner

* Fri May 20 2022 Lior Lustgarten <lilustga@microsoft.com> 1.23.6-1
- License verified
- Initial changes to build for Mariner
- Initial CBL-Mariner import from Rancher (license: ASL 2.0).

* Mon Mar 2 2020 Erik Wilson <erik@rancher.com> 0.1-1
- Initial version