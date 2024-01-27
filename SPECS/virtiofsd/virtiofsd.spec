Name:           virtiofsd
Version:        1.8.0
Release:        1%{?dist}
Summary:        Virtio-fs vhost-user device daemon (Rust version)
License:        Apache-2.0 AND BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://gitlab.com/virtio-fs/virtiofsd
Source0:        https://gitlab.com/virtio-fs/virtiofsd/-/archive/v%{version}/%{name}-v%{version}.tar.gz

# To update the vendor tarball and config.toml:
#   wget %{SOURCE0}
#   tar -xf %{name}-v%{version}.tar.gz
#   cd %{name}-v%{version}
#   cargo vendor > ../config.toml
#   tar -czf ../%{name}-v%{version}-cargo.tar.gz vendor/
Source1:        %{name}-v%{version}-cargo.tar.gz
Source2:        config.toml
Source3:        %{name}-v%{version}-cargo-vendor-CVE-2023-41051.tar.gz
# Updates vm-memory to 0.12.2. Remove once virtiofsd gets updated to a version >= 1.9.0: 
# https://gitlab.com/virtio-fs/virtiofsd/-/blob/v1.9.0/Cargo.toml
Patch0: CVE-2023-41051.patch

ExclusiveArch:  x86_64

BuildRequires:  cargo
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp-devel

%description
Virtio-fs vhost-user device daemon (Rust version)

%prep
%autosetup -p1 -n %{name}-v%{version}

pushd %{_builddir}/%{name}-v%{version}
# Updated vendor package in Source3 to fix CVE-2023-41051
tar -xf %{SOURCE3}
mkdir -p .cargo
cp %{SOURCE2} .cargo/
popd

%build
pushd %{_builddir}/%{name}-v%{version}
cargo build --release --offline
popd

%install
mkdir -p %{buildroot}%{_libexecdir}
install -D -p -m 0755 target/release/virtiofsd %{buildroot}%{_libexecdir}/virtiofsd-rs

%files
%license LICENSE-APACHE LICENSE-BSD-3-Clause
%doc README.md
%{_libexecdir}/virtiofsd-rs

%changelog
* Fri Jan 26 2024 Nadiia Dubchak <ndubchak@microsoft.com> - 1.8.0-2
- Update vendor tarball to include vm-memory version 0.12.2.
- Set the new tarball as Source3 and use it in step %prep.

* Wed Jan 24 2024 Nadiia Dubchak <ndubchak@microsoft.com> - 1.8.0-2
- Patch CVE-2023-41051.

* Tue Jan 9 2024 Aurélien Bombo <abombo@microsoft.com> - 1.8.0-1
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License verified.
