%global crate update-ssh-keys

# Below is a manually created tarball containing vendored Rust dependencies.
# The vendored crates are needed because network access is disabled during build time.
#
# How to recreate this vendor tarball:
#   1. Download the update-ssh-keys source tarball
#   2. Extract it: tar xzf update-ssh-keys-X.Y.Z.tar.gz && cd update-ssh-keys-X.Y.Z
#   3. Generate vendor directory: cargo vendor > /dev/null
#   4. Create the vendor tarball: tar czf ../update-ssh-keys-X.Y.Z-vendor.tar.gz vendor/
#
# Note: The vendor tarball should be uploaded to the GitHub releases page or stored
# in the package's source location (using the format update-ssh-keys-VERSION-vendor.tar.gz)

Name:           update-ssh-keys
Version:        0.7.0
Release:        1%{?dist}
Summary:        Utility for managing OpenSSH authorized public keys

License:        Apache-2.0
URL:            https://github.com/flatcar/update-ssh-keys
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
Source0:        https://github.com/flatcar/update-ssh-keys/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  cargo
BuildRequires:  rust >= 1.60

Requires: coreos-init

%ifarch x86_64
%define rust_def_target x86_64-unknown-linux-gnu
%endif
%ifarch aarch64
%define rust_def_target aarch64-unknown-linux-gnu
%endif

%description
update-ssh-keys is a command line tool and library for managing OpenSSH
authorized public keys. It keeps track of sets of keys with names, allows
for adding additional keys, as well as deleting and disabling them.

The tool is commonly used on Container Linux and Flatcar to manage SSH
access in cloud environments. It can integrate with cloud-config and other
provisioning systems to maintain authorized_keys files.

%prep
%autosetup -n %{crate}-%{version} -p1

# Extract vendored crates
tar xf %{SOURCE1}
mkdir -p .cargo

cat >.cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --release --target=%{rust_def_target} --offline

%install
mkdir -p %{buildroot}%{_bindir}
install -m 755 ./target/%{rust_def_target}/release/%{crate} %{buildroot}%{_bindir}/%{crate}

%check
cargo test --offline

%files
%license LICENSE
%doc README.md
%{_bindir}/%{crate}

%changelog
* Wed Feb 19 2026 Akarsh Chaudhary <v-akarshc@microsoft.com> - 1.35.3-10
- Initial Azure Linux import from the source project (license: same as "License" tag).
- License verified
