%define using_rustup 0
%define using_musl_libc 0
%define using_vendored_crates 1

Name:           cloud-hypervisor
Summary:        Cloud Hypervisor is an open source Virtual Machine Monitor (VMM) that runs on top of the KVM hypervisor and the Microsoft Hypervisor (MSHV).
Version:        48.0.246
Release:        3%{?dist}
License:        ASL 2.0 OR BSD-3-clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/microsoft/cloud-hypervisor
Source0:        https://github.com/microsoft/cloud-hypervisor/archive/refs/tags/msft/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%if 0%{?using_vendored_crates}
# Note: the %%{name}-%%{version}-vendor.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache and config.toml run:
#   tar -xf %%{name}-%%{version}.tar.gz
#   cd %%{name}-%%{version}
#   cargo vendor > config.toml
#   tar -czf %%{name}-%%{version}-vendor.tar.gz vendor/
Source1:        %{name}-%{version}-vendor.tar.gz
%endif

BuildRequires:  binutils
BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  glibc-devel
BuildRequires:  openssl-devel

%if ! 0%{?using_rustup}
BuildRequires:  rust >= 1.85.0
BuildRequires:  cargo >= 1.85.0
%endif

Requires: bash
Requires: glibc
Requires: libgcc
Requires: libcap

%ifarch x86_64
%define rust_def_target x86_64-unknown-linux-gnu
%define cargo_pkg_feature_opts --features "mshv"
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

# This package replaces cloud-hypervisor-cvm. As of 9/10/2025, cloud-hypervisor-cvm is a deprecated name.
# This is a temporary measure for compatibility.
# todo: remove this provides/obsoletes pair in the future.
Provides: cloud-hypervisor-cvm = %{version}-%{release}
Obsoletes: cloud-hypervisor-cvm < %{version}-%{release}

%description
Cloud Hypervisor is an open source Virtual Machine Monitor (VMM) that runs on top of KVM. The project focuses on exclusively running modern, cloud workloads, on top of a limited set of hardware architectures and platforms. Cloud workloads refers to those that are usually run by customers inside a cloud provider. For our purposes this means modern Linux* distributions with most I/O handled by paravirtualised devices (i.e. virtio), no requirement for legacy devices and recent CPUs and KVM.

%prep

%setup -q -n cloud-hypervisor-%{version}
%if 0%{?using_vendored_crates}
tar xf %{SOURCE1}
%endif

%install
install -d %{buildroot}%{_bindir}
install -D -m755  ./target/%{rust_def_target}/release/cloud-hypervisor %{buildroot}%{_bindir}

%if 0%{?using_musl_libc}
install -d %{buildroot}%{_libdir}/cloud-hypervisor/static
install -D -m755 target/%{rust_musl_target}/release/cloud-hypervisor %{buildroot}%{_libdir}/cloud-hypervisor/static
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
%if 0%{?using_musl_libc}
cargo build --release --target=%{rust_musl_target} %{cargo_pkg_feature_opts} %{cargo_offline}
%endif

%files
%defattr(-,root,root,-)
%caps(cap_net_admin=ep) %{_bindir}/cloud-hypervisor
%if 0%{?using_musl_libc}
%{_libdir}/cloud-hypervisor/static/ch-remote
%caps(cap_net_admim=ep) %{_libdir}/cloud-hypervisor/static/cloud-hypervisor
%endif
%license LICENSES/Apache-2.0.txt
%license LICENSES/BSD-3-Clause.txt
%license LICENSES/CC-BY-4.0.txt

%changelog
* Wed Feb 11 2026 BinduSri Adabala <v-badabala@microsoft.com> - 48.0.246-3
- Bump release to rebuild with rust

* Mon Feb 02 2026 Archana Shettigar <v-shettigara@microsoft.com> - 48.0.246-2
- Bump release to rebuild with rust

* Fri Jan 23 2026 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 48.0.246-1
- Auto-upgrade to 48.0.246

* Wed Oct 15 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 41.0.139-3
- Bump release to rebuild with rust

* Thu Oct 09 2025 Saul Paredes <saulparedes@microsoft.com> -  41.0.139-2
- Enable build on aarch64

* Tue Sep 09 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 41.0.139-1
- Auto-upgrade to 41.0.139
- Rename package to cloud-hypervisor

* Fri Aug 08 2025 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 41.0.79-4
- Bump release to rebuild with rust

* Mon Jul 21 2025 Jyoti Kanase <v-jykanase@microsoft.com> - 41.0.79-3
- Bump release to rebuild with rust

* Fri Jun 13 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 41.0.79-2
- Bump release to rebuild with rust

* Mon Apr 28 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 41.0.79-1
- Auto-upgrade to 41.0.79

* Mon Apr 21 2025 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 38.0.72.2-4
- Pin rust version

* Sun Feb 16 2025 Kanishk Bansal <kanbansal@microsoft.com> - 38.0.72.2-3
- Patch CVE-2024-12797

* Tue Sep 17 2024 Jiri Appl <jiria@microsoft.com> - 38.0.72.2-2
- Patch openssl in the vendored archive to 3.3.2 to address CVE-2024-6119

* Fri Jul 12 2024 Archana Choudhary <archana1@microsoft.com> - 38.0.72.2-1
- Upgrade to v38.0.72.2
- Fixes CVE-2023-45853, CVE-2018-25032, CVE-2023-5363, CVE-2023-5678, CVE-2023-6129, CVE-2023-6237, CVE-2024-0727, CVE-2024-4603

* Tue Jun 25 2024 Chris Co <chrco@microsoft.com> - 38.0.72-2
- Remove conflicts with cloud-hypervisor

* Wed May 15 2024 Saul Paredes <saulparedes@microsoft.com> - 38.0.72-1
- Initial CBL-Mariner import from Azure
- Upgrade to v38.0.72
- Update install to match cloud-hypervisor install locations
- Add conflicts with cloud-hypervisor
- License verified.

* Mon Nov 6 2023 Dallas Delaney <dadelan@microsoft.com> - 32.0.314-2000
- Upgrade to v32.0.314

* Thu Sep 21 2023 Saul Paredes <saulparedes@microsoft.com> - 32.0.209-2000
- Upgrade to v32.0.209

* Fri Sep 15 2023 Saul Paredes <saulparedes@microsoft.com> - 32.0.192-2000
- Upgrade to v32.0.192

* Tue Aug 1 2023 Saul Paredes <saulparedes@microsoft.com> - 32.0.0-2000
- Accomodate cloud-hypervisor

* Fri May 19 2023 Anatol Belski <anbelski@linux.microsoft.com> - 32.0.0-1000
- Upgrade to v32.0

* Wed Apr 19 2023 Anatol Belski <anbelski@linux.microsoft.com> - 31.1.0-1000
- Upgrade to v31.1

* Thu Apr 06 2023 Anatol Belski <anbelski@linux.microsoft.com> - 31.0.0-1000
- Upgrade to v31.0

* Fri Feb 24 2023 Anatol Belski <anbelski@linux.microsoft.com> - 30.0.0-1000
- Upgrade to v30.0

* Sun Jan 15 2023 Anatol Belski <anbelski@linux.microsoft.com> - 29.0.0-1000
- Upgrade to v29.0

* Thu Dec 15 2022 Anatol Belski <anbelski@linux.microsoft.com> - 28.1.0-1000
- Upgrade to v28.1

* Thu Nov 17 2022 Anatol Belski <anbelski@linux.microsoft.com> - 28.0.0-1000
- Upgrade to v28.0

* Wed Oct 12 2022 Anatol Belski <anbelski@linux.microsoft.com> - 27.0.0-1001
- Spec refactoring towards pulling an arbitrary revision

* Wed Oct 05 2022 Anatol Belski <anbelski@linux.microsoft.com> - 27.0-1
- Upgrade to 27.0

* Thu Sep 15 2022 Anatol Belski <anbelski@linux.microsoft.com> - 26.0-2
- Unbundle tarballs from git

* Wed Aug 17 2022 Anatol Belski <anbelski@linux.microsoft.com> - 26.0-1
- Pull release 26.0 for Mariner from upstream

* Tue May 16 2022 Anatol Belski <anbelski@linux.microsoft.com> - 23.1-0
- Initial import 23.1 for Mariner from upstream

*   Thu Apr 13 2022 Rob Bradford <robert.bradford@intel.com> 23.0-0
-   Update to 23.0

*   Thu Mar 03 2022 Rob Bradford <robert.bradford@intel.com> 22.0-0
-   Update to 22.0

*   Thu Jan 20 2022 Rob Bradford <robert.bradford@intel.com> 21.0-0
-   Update to 21.0

*   Thu Dec 02 2021 Sebastien Boeuf <sebastien.boeuf@intel.com> 20.0-0
-   Update to 20.0

*   Mon Nov 08 2021 Fabiano Fidêncio <fabiano.fidencio@intel.com> 19.0-0
-   Update to 19.0

*   Fri May 28 2021 Muminul Islam <muislam@microsoft.com> 15.0-0
-   Update version to 15.0

*   Wed Jul 22 2020 Muminul Islam <muislam@microsoft.com> 0.8.0-0
-   Initial version
