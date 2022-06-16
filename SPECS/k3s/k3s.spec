%global debug_package %{nil}
%define install_path  /usr/local/bin
%define util_path     %{_datadir}/k3s
%define install_sh    %{util_path}/setup/install.sh
%define uninstall_sh  %{util_path}/setup/uninstall.sh
%define k3s_binary    k3s

Name:    k3s
Version: 1.23.6
Release: %{version}%{?dist}
Summary: Lightweight Kubernetes

Group:   System Environment/Base
License: ASL 2.0
URL:     http://k3s.io
Source0: %{name}-%{version}-k3s1.tar.gz

BuildRequires: golang
BuildRequires: libseccomp-devel
BuildRequires: btrfs-progs-devel
Requires:      apparmor-parser

%description
The certified Kubernetes distribution built for IoT & Edge computing.

%prep
%setup -q -n %{name}-%{version}-k3s1

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
* Tue May 24 2022 Manuel Huber <mahuber@microsoft.com>
- Changes to install phase on Mariner
* Fri May 20 2022 Lior Lustgarten <lilustga@microsoft.com>
- Initial changes to build for Mariner
* Mon Mar 2 2020 Erik Wilson <erik@rancher.com> 0.1-1
- Initial version