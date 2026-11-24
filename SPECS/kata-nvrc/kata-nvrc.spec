%global debug_package %{nil}
%global commit 77ce29cac2a7d1b943b9349a630e4d27640c3e6a
%global shortcommit %(c=%{commit}; echo ${c:0:7})
%global snapdate 20261109
%global upstream_version 0.1.7
%ifarch x86_64
%global rust_target x86_64-unknown-linux-gnu
%endif
%ifarch aarch64
%global rust_target aarch64-unknown-linux-gnu
%endif
Summary:        NVIDIA runtime init for the GPU utility VMs of Kata Containers
Name:           kata-nvrc
Version:        %{upstream_version}^%{snapdate}git%{shortcommit}
Release:        1%{?dist}
License:        Apache-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System Environment/Base
URL:            https://github.com/NVIDIA/nvrc
Source0:        https://github.com/NVIDIA/nvrc/archive/%{commit}.tar.gz#/%{name}-%{upstream_version}-%{shortcommit}.tar.gz
# Below is a manually created tarball, no download link.
# It contains the vendored Rust crates of Source0. Create it with:
#   ./generate_source_tarball.sh --srcTarball %%{name}-%%{upstream_version}-%%{shortcommit}.tar.gz \
#       --pkgVersion %%{upstream_version}-%%{shortcommit}
Source1:        %{name}-%{upstream_version}-%{shortcommit}-vendor.tar.gz
# Support the HGX A100 8-GPU baseboard with six NVSwitches (NVL3), report the
# exit status of a daemon that dies before it is ready, and start nvidia-imex on
# GB200. The three commits of
# https://github.com/JocelynBerrendonner/nvrc/tree/test/a100-nvl3 on top of
# upstream main.
Patch0:         0001-Support-HGX-A100-NVL3-report-daemon-exits-and-start-IMEX-on-GB200.patch
ExclusiveArch:  x86_64 aarch64
# rust-toolchain.toml pins 1.94.0; Azure Linux builds with its own toolchain.
BuildRequires:  cargo >= 1.94.0
BuildRequires:  rust >= 1.94.0
BuildRequires:  gcc
BuildRequires:  glibc-devel

%description
NVRC is the init process (PID 1) of the NVIDIA GPU utility VMs (UVMs) of Kata
Containers. It loads the NVIDIA kernel modules, configures the GPUs, starts the
NVIDIA management daemons (persistenced, fabric manager, IMEX, DCGM, ...),
generates the CDI specification of the GPUs, and then hands off to the Kata
agent.

%prep
%autosetup -n nvrc-%{commit} -N
tar -xf %{SOURCE1}
%autopatch -p1
cat >> .cargo/config.toml << 'EOF'

[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build
cargo build --release --locked --offline --target %{rust_target}

%install
install -D -p -m 0755 target/%{rust_target}/release/NVRC %{buildroot}%{_bindir}/NVRC

%check
# Skip the tests that need a privileged root (mounts, sysctl writes, network
# configuration, module loading), which the build environment does not provide.
cargo test --release --locked --offline --target %{rust_target} -- \
    --skip gpu_extension::tests::test_bind_ \
    --skip kata_agent::tests::test_agent_setup \
    --skip kernel_params::tests::test_nvrc_log_debug \
    --skip kernel_params::tests::test_process_kernel_params_nvrc_log_ \
    --skip kmsg::tests::test_kernlog_setup \
    --skip modprobe::tests::test_load_loop \
    --skip mount::tests::test_mount_optional_success \
    --skip mount::tests::test_setup_at_with_temp_root \
    --skip net::tests::test_loopback_up

%files
%license LICENSE
%doc README.md
%{_bindir}/NVRC

%changelog
* Mon Nov 23 2026 Jocelyn Berrendonner <jocelynb@microsoft.com> - 0.1.7^20261109git77ce29c-1
- Original version for Azure Linux
- License verified
