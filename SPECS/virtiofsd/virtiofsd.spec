Name:           virtiofsd
Version:        1.8.0
Release:        3%{?dist}
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

Patch0:         CVE-2024-43806.patch

BuildRequires:  cargo
BuildRequires:  libcap-ng-devel
BuildRequires:  libseccomp-devel

%description
Virtio-fs vhost-user device daemon (Rust version)

%prep
%autosetup -N -n %{name}-v%{version}

pushd %{_builddir}/%{name}-v%{version}
tar -xf %{SOURCE1}
%autopatch -p1
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
* Fri Jan 17 2025 Archana Choudhary <archana1@microsoft.com> - 1.8.0-3
- Patch CVE-2024-43806

* Fri Feb 16 2024 Muhammad Falak <mwani@microsoft.com> - 1.8.0-2
- Drop ExclusiveArch: x86_64 to build on all supported platforms

* Tue Jan 9 2024 Aurélien Bombo <abombo@microsoft.com> - 1.8.0-1
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- License verified.
