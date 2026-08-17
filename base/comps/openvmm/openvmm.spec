Name:           openvmm
Version:        0.1.0
Release:        %autorelease
Summary:        Modular, cross-platform virtual machine monitor

License:        MIT
URL:            https://github.com/microsoft/openvmm
Source0:        %{url}/archive/openvmm-v%{version}/%{name}-%{version}.tar.gz
# Published with the release; contains the vendor tree and the cargo_config that
# maps the workspace's git dependencies into it.
Source1:        %{url}/releases/download/openvmm-v%{version}/%{name}-%{version}-vendor.tar.gz

# Upstream validates this configuration for x86_64-unknown-linux-gnu only.
ExclusiveArch:  x86_64

BuildRequires:  cargo-rpm-macros >= 25
BuildRequires:  rust >= 1.95.0
BuildRequires:  cargo >= 1.95.0
BuildRequires:  openssl-devel
BuildRequires:  protobuf-compiler
# protoc resolves the well-known .proto imports from /usr/include.
BuildRequires:  protobuf-devel

%description
OpenVMM is a modular, cross-platform virtual machine monitor written in Rust.
This package provides the host binary, which runs virtual machines on Linux
via KVM or the Microsoft Hypervisor.

%prep
%autosetup -n %{name}-openvmm-v%{version} -N
tar -xf %{SOURCE1}
# -N writes the build configuration without setting up a registry: the source
# replacements come from the cargo_config generated alongside the vendor tree,
# which also maps the git dependencies.
%cargo_prep -N
cat cargo_config >> .cargo/config.toml

%build
# Link against the system OpenSSL rather than building a bundled copy.
export OPENSSL_NO_VENDOR=1
%cargo_build -- --locked -p %{name}
%cargo_license_summary
%{cargo_license} > LICENSE.dependencies
# Equivalent to %%cargo_vendor_manifest, minus "--no-dedupe". That flag expands
# every shared dependency at each point it is reached, which on a workspace this
# size grows without bound (over 10^8 lines and still growing after ten minutes).
# cargo2rpm collapses the output into a set, so suppressing the duplicates cannot
# change the result. The remaining transformations match write-vendor-manifest:
# drop the "(proc-macro)" annotation and the workspace's own crates, then sort.
# The subshell keeps %%cargo_vendor_manifest's "set -euo pipefail", so a failing
# "cargo tree" is not masked by the exit status of the trailing "sort".
(
set -euo pipefail
%{__cargo} tree --workspace --offline --edges=normal,build,dev --target=all \
    --all-features --prefix=none --format '{p}' \
  | sed -e 's/ (proc-macro)//' -e 's/ (\*)$//' -e '/^$/d' \
  | grep -vF "$PWD" | sort -u > cargo-vendor.txt
)

%install
install -D -p -m 0755 target/rpm/%{name} %{buildroot}%{_bindir}/%{name}

%check
target/rpm/%{name} --version

%files
%license LICENSE
%license LICENSE.dependencies
%license cargo-vendor.txt
%doc README.md
%{_bindir}/%{name}

%changelog
%autochangelog
