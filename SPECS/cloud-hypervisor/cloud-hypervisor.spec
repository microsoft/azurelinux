%define using_rustup 0
%define using_musl_libc 0
%define using_vendored_crates 1

Summary:        Cloud Hypervisor is an open source Virtual Machine Monitor (VMM) that runs on top of KVM.
Name:           cloud-hypervisor
Version:        32.0
Release:        3%{?dist}
License:        ASL 2.0 OR BSD-3-clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://github.com/cloud-hypervisor/cloud-hypervisor
Source0:        https://github.com/cloud-hypervisor/cloud-hypervisor/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%if 0%{?using_vendored_crates}
# Note: the %%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache and config.toml run:
#   tar -xf %{name}-%{version}.tar.gz
#   cd %{name}-%{version}
#   cargo vendor > config.toml
#   tar -czf %{name}-%{version}-cargo.tar.gz vendor/
# rename the tarball to %{name}-%{version}-cargo.tar.gz when updating version
Source1:        %{name}-%{version}-cargo-v1.tar.gz
Source2:        config.toml
Patch0:         CVE-2023-45853.patch
Patch1:         CVE-2023-50711.patch
%endif

BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  openssl-devel

%if ! 0%{?using_rustup}
BuildRequires:  rust >= 1.60.0
BuildRequires:  cargo >= 1.60.0
%endif

Requires: bash
Requires: glibc
Requires: libgcc
Requires: libcap

ExclusiveArch:  x86_64

%ifarch x86_64
%define rust_def_target x86_64-unknown-linux-gnu
%define cargo_pkg_feature_opts --no-default-features --features "mshv,kvm"
%endif
%ifarch aarch64
%define rust_def_target aarch64-unknown-linux-gnu
%define cargo_pkg_feature_opts --all
%endif

%if 0%{?using_musl_libc}
%ifarch x86_64
%define rust_musl_target x86_64-unknown-linux-musl
%endif
%ifarch aarch64
%define rust_musl_target aarch64-unknown-linux-musl
%endif
%endif

%if 0%{?using_vendored_crates}
%define cargo_offline --offline
%endif

%description
Cloud Hypervisor is an open source Virtual Machine Monitor (VMM) that runs on top of KVM. The project focuses on exclusively running modern, cloud workloads, on top of a limited set of hardware architectures and platforms. Cloud workloads refers to those that are usually run by customers inside a cloud provider. For our purposes this means modern Linux* distributions with most I/O handled by paravirtualised devices (i.e. virtio), no requirement for legacy devices and recent CPUs and KVM.

%prep

%setup -q -n %{name}-%{version}
%if 0%{?using_vendored_crates}
tar xf %{SOURCE1}
pushd vendor/libz-sys/src/zlib
%patch0 -p1
%patch1 -p1
popd
mkdir -p .cargo
cp %{SOURCE2} .cargo/
%endif

%install
install -d %{buildroot}%{_bindir}
install -D -m755  ./target/%{rust_def_target}/release/cloud-hypervisor %{buildroot}%{_bindir}
install -D -m755  ./target/%{rust_def_target}/release/ch-remote %{buildroot}%{_bindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/cloud-hypervisor
install -D -m755 target/%{rust_def_target}/release/vhost_user_block %{buildroot}%{_libdir}/cloud-hypervisor
install -D -m755 target/%{rust_def_target}/release/vhost_user_net %{buildroot}%{_libdir}/cloud-hypervisor

%if 0%{?using_musl_libc}
install -d %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/cloud-hypervisor %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/vhost_user_block %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/vhost_user_net %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/ch-remote %{buildroot}%{_libdir}/cloud-hypervisor/static
%endif


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
	%if 0%{?using_musl_libc}
rustup target list --installed | grep x86_64-unknown-linux-musl
if [[ $? -ne 0 ]]; then
         echo "Target  x86_64-unknown-linux-musl not found, please install(#rustup target add x86_64-unknown-linux-musl). exiting"
fi
	%endif
%endif

%if 0%{?using_vendored_crates}
# For vendored build, prepend this so openssl-sys doesn't trigger full OpenSSL build
export OPENSSL_NO_VENDOR=1
%endif
cargo build --release --target=%{rust_def_target} %{cargo_pkg_feature_opts} %{cargo_offline}
cargo build --release --target=%{rust_def_target} --package vhost_user_net %{cargo_offline}
cargo build --release --target=%{rust_def_target} --package vhost_user_block %{cargo_offline}
%if 0%{?using_musl_libc}
cargo build --release --target=%{rust_musl_target} %{cargo_pkg_feature_opts} %{cargo_offline}
cargo build --release --target=%{rust_musl_target} --package vhost_user_net %{cargo_offline}
cargo build --release --target=%{rust_musl_target} --package vhost_user_block %{cargo_offline}
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/ch-remote
%caps(cap_net_admin=ep) %{_bindir}/cloud-hypervisor
%{_libdir}/cloud-hypervisor/vhost_user_block
%caps(cap_net_admin=ep) %{_libdir}/cloud-hypervisor/vhost_user_net
%if 0%{?using_musl_libc}
%{_libdir}/cloud-hypervisor/static/ch-remote
%caps(cap_net_admim=ep) %{_libdir}/cloud-hypervisor/static/cloud-hypervisor
%{_libdir}/cloud-hypervisor/static/vhost_user_block
%caps(cap_net_admin=ep) %{_libdir}/cloud-hypervisor/static/vhost_user_net
%endif
%license LICENSE-APACHE
%license LICENSE-BSD-3-Clause

%changelog
* Mon Jan 15 2024 Sindhu Karri <lakarri@microsoft.com> - 32.0-3
- Bump version of vmm-sys-util in vendor to 0.12.1 to fix CVE-2023-50711. Update and rename vendor cargo tarball
- Patch CVE-2023-50711 to use updated vmm-sys-util

* Mon Oct 23 2023 Rohit Rawat <rohitrawat@microsoft.com> - 32.0-2
- Patch CVE-2023-45853 in vendor/libz-sys/src/zlib

* Wed Sep 27 2023 Saul Paredes <saulparedes@microsoft.com> - 32.0-1
- Update to v32.0

* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 31.1-2
- Bump package to rebuild with rust 1.72.0

* Fri May 12 2023 Saul Paredes <saulparedes@microsoft.com> - 31.1-1
- Update to v31.1

* Mon Apr 03 2023 Henry Beberman <henry.beberman@microsoft.com> 30.0-2
- Patch CVE-2023-28448 in vendor/versionize

* Fri Mar 24 2023 Mitch Zhu <mitchzhu@microsoft.com> 30.0-1
- Update to v30.0

* Tue Jan 24 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 29.0-1
- Update to v29.0

* Mon Dec 12 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 28.0-1
- Update to v28.0

* Thu Oct 27 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 27.0.60-1
- Update to v27.0.60

* Wed Aug 31 2022 Olivia Crain <oliviacrain@microsoft.com> - 26.0-2
- Bump package to rebuild with stable Rust compiler

* Thu Aug 18 2022 Chris Co <chrco@microsoft.com> - 26.0-1
- anbelski@linux.microsoft.com, 26.0-1 - Pull release 26.0 for Mariner from upstream
- anbelski@linux.microsoft.com, 23.1-0 - Initial import 23.1 for Mariner from upstream
- robert.bradford@intel.com, 23.0-0 - Update to 23.0
- robert.bradford@intel.com, 22.0-0 - Update to 22.0
- robert.bradford@intel.com, 21.0-0 - Update to 21.0
- sebastien.boeuf@intel.com, 20.0-0 - Update to 20.0
- fabiano.fidencio@intel.com, 19.0-0 - Update to 19.0
- muislam@microsoft.com, 15.0-0 - Update version to 15.0
- muislam@microsoft.com, 0.8.0-0 - Initial version

* Wed Mar 09 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 22.0-1
- Updating to version 22.0 to build with 'rust' 1.59.0.

* Tue Feb 08 2022 Henry Li <lihl@microsoft.com> - 21.0-1
- Update to version 21.0

* Wed Dec 01 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 19.0-1
- Updating to version 19.0 to use existing dependencies and build with the 1.56.1 version of 'rust'.

* Mon Apr 26 2021 Thomas Crain <thcrain@microsoft.com> - 0.6.0-7
- Bump release to rebuild with rust 1.47.0-3 (security update)

* Tue Apr 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.6.0-6
- Bump release to rebuild with rust 1.47.0-2 (security update)

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.6.0-5
- Added %%license line automatically

* Thu May 07 2020 Nicolas Guibourge <mrgirgin@microsoft.com> - 0.6.0-4
- Fix docker based build issue

* Mon May 04 2020 Emre Girgin <mrgirgin@microsoft.com> - 0.6.0-3
- Replace BuildArch with ExclusiveArch

* Fri Apr 24 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-3
- License verified.
- Fixed Source0 tag.

* Tue Apr 21 2020 Andrew Phelps <anphel@microsoft.com> - 0.6.0-2
- Support building offline with prepopulated .cargo directory.

* Thu Feb 13 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.6.0-1
- Original version for CBL-Mariner.
