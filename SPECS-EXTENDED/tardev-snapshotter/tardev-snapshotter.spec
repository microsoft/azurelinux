%global debug_package %{nil}

Summary: Tardev Snapshotter for containerd
Name: tardev-snapshotter
Version: 0.0.13
Release: 1%{?dist}
License: ASL 2.0
Group: Tools/Container
# URL: https://www.containerd.io
Vendor: Microsoft Corporation
Distribution: Azure Linux

# Source0: https://github.com/microsoft/kata-containers/tree/jiria/solar
Source0: %{name}-%{version}.tar.gz
# Note: the %%{name}-%%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache run:
#   [repo_root]/toolkit/scripts/build_cargo_cache.sh %%{name}-%%{version}.tar.gz %%{name}-%%{name}-%%{version}
Source1: %{name}-%{version}-cargo.tar.gz

%{?systemd_requires}

BuildRequires: clang-devel
BuildRequires: cmake
BuildRequires: device-mapper-devel
BuildRequires: git
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: pkgconfig(libudev)
BuildRequires: protobuf-compiler
BuildRequires: rust

%description
tardev-snapshotter is a snapshotter for containerd that uses tar archives to store snapshots.

%prep
# Setup .cargo directory
mkdir -p $HOME
pushd $HOME
tar xf %{SOURCE1} --no-same-owner
popd

%autosetup -p1

%build
export CARGO_NET_OFFLINE=true
make

# %check

%install

mkdir -p %{buildroot}/%{_unitdir}
install -D -p -m 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -D -m 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}

%post
%systemd_post %{name}.service

if [ $1 -eq 1 ]; then # Package install
	systemctl enable %{name}.service > /dev/null 2>&1 || :
	systemctl start %{name}.service > /dev/null 2>&1 || :
fi

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
# %license LICENSE NOTICE
%{_bindir}/*
%config(noreplace) %{_unitdir}/%{name}.service

%changelog
* Tue Dec 31 2024 Jiri Appl <jiria@microsoft.com> - 0.0.1-1
- Initial version
