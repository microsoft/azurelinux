Name:    k3s
Version: 1.23.6
Release: %{version}%{?dist}
Summary: Lightweight Kubernetes

Group:   System Environment/Base		
License: ASL 2.0
URL:     http://k3s.io
Source0: %{name}-%{version}-k3s1.tar.gz

BuildRequires: systemd
BuildRequires: golang

%description
The certified Kubernetes distribution built for IoT & Edge computing.

#%prep
#%autosetup -p1

%build
%define OUR_GOPATH %{_topdir}/.gopath
export GOPATH=%{OUR_GOPATH}
# make bin/service/k3s GOMODVENDOR=1
mkdir build/static
mkdir etc
./scripts/build
./scripts/package-cli
echo ls


%install
install -d %{buildroot}%{install_path}
#install dist/artifacts/%{k3s_binary} %{buildroot}%{install_path}/k3s
#install -d %{buildroot}%{util_path}/setup
#install package/rpm/install.sh %{buildroot}%{install_sh}