%define using_rustup 0
%define using_vendored_crates 1

Name:           openvmm
Summary:        OpenVMM is an open source Virtual Machine Monitor (VMM) that enables running Hyper-V compatible Virtual Machines on top of the MSHV hypervisor.
Version:        0.0.2
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/microsoft/openvmm
# [jocelynb] TODO: get a proper openvmm release and update the following line. For now, we are taking the latest commit from the main branch as of 4/23/2025.
# This is the last change that was made to the main branch before the switch to rust 1.86 (Which is not supported in azure linux yet).
# Full commit hash of the package used below: d2ea7d59b73646ddb60c4f7876f15f0465851d6a
Source0:        https://github.com/microsoft/openvmm/archive/d2ea7d5.tar.gz
%if 0%{?using_vendored_crates}
# Note: the %%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache and config.toml run:
#   tar -xf %%{name}-%%{version}.tar.gz
#   cd %%{name}-%%{version}
#   cargo vendor > config.toml
#   tar -czf %%{name}-%%{version}-vendor.tar.gz vendor/
# then, upload the tarball to the azure linux tarball server
Source1:        %{name}-%{version}-vendor.tar.gz
%endif

BuildRequires:  binutils
BuildRequires:  build-essential
BuildRequires:  gcc
BuildRequires:  gcc-aarch64-linux-gnu
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  openssl
BuildRequires:  perl-FindBin
BuildRequires:  perl-IPC-Cmd
BuildRequires:  qemu-img
BuildRequires:  protobuf
BuildRequires:  protobuf-devel
# Make sure we pick a version of rust and cargo that can handle cargo.lock version 4
BuildRequires:  rust

Requires: bash
Requires: glibc
Requires: libgcc
Requires: libcap

%ifarch x86_64
%define rust_def_target x86_64-unknown-linux-gnu
%define cargo_pkg_feature_opts --all
%endif
%ifarch aarch64
%define rust_def_target aarch64-unknown-linux-gnu
%define cargo_pkg_feature_opts --all
%endif

%description
OpenVMM is an open source Virtual Machine Monitor (VMM) that enables running Hyper-V compatible Virtual Machines on top of the MSHV hypervisor.
It is designed to be lightweight and efficient, providing a minimalistic interface for managing virtual machines. OpenVMM is built on top of the Microsoft Hypervisor Platform (MHP) and leverages its capabilities to provide a seamless virtualization experience.

%prep
%setup -q -n openvmm-d2ea7d59b73646ddb60c4f7876f15f0465851d6a
# Do vendor expansion here manually by
# calling `tar -xf` and setting up
# .cargo/config.toml to use it.
tar -xf %{SOURCE1}

%if 0%{?using_vendored_crates}
mkdir -p .cargo

# To update the cache and config.toml run:
#   tar -xf %%{SOURCE0}
#   cd %%{SOURCE0}
#   cargo vendor
# and copy the vendored result to the below
cat >.cargo/config.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/jstarks/pbjson?branch=aliases"]
git = "https://github.com/jstarks/pbjson"
branch = "aliases"
replace-with = "vendored-sources"

[source."git+https://github.com/microsoft/igvm?rev=365065d7e31da0a0116e7934de3ecd85f00bab70"]
git = "https://github.com/microsoft/igvm"
rev = "365065d7e31da0a0116e7934de3ecd85f00bab70"
replace-with = "vendored-sources"

[source."git+https://github.com/microsoft/ms-tpm-20-ref-rs.git?branch=main"]
git = "https://github.com/microsoft/ms-tpm-20-ref-rs.git"
branch = "main"
replace-with = "vendored-sources"

[source."git+https://github.com/smalis-msft/bitvec?branch=set-aliased-previous-val"]
git = "https://github.com/smalis-msft/bitvec"
branch = "set-aliased-previous-val"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%endif


%install
install -d %{buildroot}%{_bindir}
install -D -m755  ./target/%{rust_def_target}/release/openvmm %{buildroot}%{_bindir}

%build
cargo_version=$(cargo --version)
if [[ $? -ne 0 ]]; then
	echo "Cargo not found, please install cargo. exiting"
	exit 0
fi

%if 0%{?using_rustup}
which rustup
if [[ $? -ne 0 ]]; then
	echo "Rustup not found please install rustup #curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh"
fi
%endif

echo ${cargo_version}

%if 0%{?using_rustup}
rustup target list --installed | grep x86_64-unknown-linux-gnu
if [[ $? -ne 0 ]]; then
         echo "Target  x86_64-unknown-linux-gnu not found, please install(#rustup target add x86_64-unknown-linux-gnu). exiting"
fi
%endif

%if 0%{?using_vendored_crates}
# For vendored build, prepend this so openssl-sys doesn't trigger full OpenSSL build
export OPENSSL_NO_VENDOR=1
%endif

echo "Building for target: %{rust_def_target} %{cargo_pkg_feature_opts} --offline"
cargo build --release --target=%{rust_def_target} %{cargo_pkg_feature_opts} --offline

%files
%defattr(-,root,root,-)
%caps(cap_net_admin=ep) %{_bindir}/openvmm

%license LICENSE

%changelog
* Fri May 9 2025 Jocelyn Berrendonner <jocelynb@microsoft.com> - 0.0.1-1
- Initial package version


