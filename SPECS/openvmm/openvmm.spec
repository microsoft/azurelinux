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

ExclusiveArch:  x86_64 aarch64

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

%ifarch x86_64
%global rust_target x86_64-unknown-linux-gnu
%endif
%ifarch aarch64
%global rust_target aarch64-unknown-linux-gnu
%endif

# A representative subset of the openvmm binary's dependency closure whose unit
# tests need no live VM. Not exhaustive; more crates can be added over time.
%global test_crates -p acpi -p consomme -p crypto -p loader -p mesh_protobuf -p openvmm_core -p openvmm_entry -p pal -p pci_core -p vhdx -p vm_topology -p vmcore -p vmm_core

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
cargo test --release --locked --offline --lib --target %{rust_target} %{test_crates}
./target/%{rust_target}/release/openvmm --version

%files
%license LICENSE
%doc README.md
%{_bindir}/openvmm

%changelog
* Thu Aug 13 2026 Ben Hillis <benhill@microsoft.com> - 0.1.0-1
- Original version for Azure Linux
- License verified
