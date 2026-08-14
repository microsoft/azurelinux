Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Name:           openvmm
Version:        0.1.0
Release:        1%{?dist}
Summary:        Modular, cross-platform virtual machine monitor
Group:          Applications/System
License:        MIT
URL:            https://github.com/microsoft/openvmm
# Upstream tags releases as "openvmm-v<version>". The generated archive unpacks
# into "openvmm-openvmm-v<version>".
Source0:        https://github.com/microsoft/openvmm/archive/refs/tags/openvmm-v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Note: the %%{name}-%%{version}-vendor.tar.gz file is published by upstream and
# contains the vendored sources in vendor/ plus the source replacement config
# 'cargo_config' written by cargo vendor.
Source1:        https://github.com/microsoft/openvmm/releases/download/openvmm-v%{version}/%{name}-%{version}-vendor.tar.gz

# Upstream validates the distribution build for x86_64 only.
ExclusiveArch:  x86_64

# Cargo enforces the workspace's rust-version.
BuildRequires:  rust >= 1.95.0
BuildRequires:  cargo >= 1.95.0
BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  kernel-headers
BuildRequires:  openssl-devel
BuildRequires:  pkgconf-pkg-config
BuildRequires:  protobuf
# protoc resolves the well-known .proto imports from /usr/include.
BuildRequires:  protobuf-devel

%description
OpenVMM is a modular, cross-platform, general-purpose virtual machine monitor
written in Rust. This package provides the OpenVMM host binary, which runs
virtual machines on Linux via KVM or Microsoft Hypervisor.

%global rust_target x86_64-unknown-linux-gnu

# The release profile does not emit debug info.
%global debug_package %{nil}

%prep
%autosetup -n %{name}-openvmm-v%{version} -N
tar -xf %{SOURCE1}
%autopatch -p1
# Append the source replacement, keeping the rustflags upstream ships.
printf '\n' >> .cargo/config.toml
cat cargo_config >> .cargo/config.toml

%build
# Override the PROTOC path set for repository development builds.
export PROTOC="$(command -v protoc)"
# Link against the distribution OpenSSL.
export OPENSSL_NO_VENDOR=1

cargo build --release --locked --offline -p openvmm --target %{rust_target}

%install
install -D -p -m 0755 target/%{rust_target}/release/openvmm %{buildroot}%{_bindir}/openvmm

%check
# The upstream test suite expects virtualization unavailable to the build.
./target/%{rust_target}/release/openvmm --version

%files
%license LICENSE
%doc README.md
%{_bindir}/openvmm

%changelog
* Thu Aug 13 2026 Ben Hillis <benhill@microsoft.com> - 0.1.0-1
- Original version for Azure Linux
- License verified
