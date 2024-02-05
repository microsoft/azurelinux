#
# spec file for package flux
#
# Copyright (c) 2022 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%global rustflags '-Clink-arg=-Wl,-z,relro,-z,now'

%define libflux_suffix %{version}-%{release}

Summary:        Influx data language
Name:           flux
Version:        0.194.5
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Productivity/Databases/Servers
URL:            https://github.com/influxdata/flux
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# Note: the %%{name}-%%{version}-cargo.tar.gz file contains a cache created by capturing the contents downloaded into $CARGO_HOME.
# To update the cache and config.toml run:
#   tar -xf %{name}-%{version}.tar.gz
#   cd %{name}-%{version}/libflux
#   cargo vendor > config.toml
#   tar -czf %{name}-%{version}-cargo.tar.gz vendor/
#
Source1:        %{name}-%{version}-cargo.tar.gz
Source2:        cargo_config
Patch1:         disable-static-library.patch
Patch2:         0001-libflux-unblock-build-by-allowing-warnings.patch
BuildRequires:  cargo >= 1.45
BuildRequires:  kernel-headers
BuildRequires:  rust >= 1.45

%description
Flux is a lightweight scripting language for querying databases (like InfluxDB)
and working with data. It is part of InfluxDB 1.7 and 2.0, but can be run
independently of those. This repository contains the language definition and an
implementation of the language core.

%package -n libflux
Summary:        Influx data language
Provides:       libflux = %{libflux_suffix}

%description -n libflux
Flux is a lightweight scripting language for querying databases (like InfluxDB)
and working with data. It is part of InfluxDB 1.7 and 2.0, but can be run
independently of those. This repository contains the language definition and an
implementation of the language core.

%package -n libflux-devel
Summary:        Development libraries and header files for Influx data language
Requires:       libflux = %{libflux_suffix}

%description -n libflux-devel
This package contains the header files and libraries for building
programs using Influx data language.

%prep
%setup -q
%patch2 -p1
pushd libflux
tar -xf %{SOURCE1}
install -D %{SOURCE2} .cargo/config

patch -p2 < %{PATCH1}
patch -p2 <<EOF
--- a/libflux/flux/build.rs
+++ b/libflux/flux/build.rs
@@ -82,5 +82,7 @@ fn main() -> Result<()> {
     let path = dir.join("stdlib.data");
     serialize(Environment::from(imports), fb::build_env, &path)?;

+    println!("cargo:rustc-cdylib-link-arg=-Wl,-soname,libflux.so.%{version}");
+
     Ok(())
 }
popd

%build
pushd libflux
RUSTFLAGS=%{rustflags} cargo build --release
RUSTFLAGS=%{rustflags} cargo build --features=doc --release --bin fluxdoc
popd

%install
install -D -m 644 libflux/include/influxdata/flux.h %{buildroot}%{_includedir}/influxdata/flux.h
install -D -m 755 libflux/target/release/libflux.so %{buildroot}%{_libdir}/libflux.so.%{version}
ln -sf ./libflux.so.%{version} %{buildroot}%{_libdir}/libflux.so

cat > flux.pc <<EOF
prefix=%{_prefix}
exec_prefix=%{_prefix}
libdir=%{_libdir}
includedir=%{_includedir}

Name:           Flux
Version:        %{version}
Description: Library for the InfluxData Flux engine
Libs: -L%{_libdir} -lflux
Libs.private: -ldl -lpthread
Cflags: -I%{_includedir}
EOF

install -D -m 644 flux.pc %{buildroot}%{_libdir}/pkgconfig/flux.pc
install -D -m 755 libflux/target/release/fluxdoc %{buildroot}%{_bindir}/fluxdoc

%check
cd libflux
RUSTFLAGS=%{rustflags} cargo test --release

%post -n libflux -p /sbin/ldconfig
%postun -n libflux -p /sbin/ldconfig

%files -n libflux
%{_libdir}/libflux.so.%{version}

%files -n libflux-devel
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/fluxdoc
%{_libdir}/libflux.so
%{_libdir}/pkgconfig/flux.pc
%dir %{_includedir}/influxdata
%{_includedir}/influxdata/flux.h

%changelog
* Thu Feb 01 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.194.5-1
- Upgrade to version 0.194.5

* Thu Sep 14 2023 Muhammad Falak <mwani@microsoft.com> - 0.191.0-3
- Introduce patch to drop warnings as build blocker

* Thu Sep 07 2023 Daniel McIlvaney <damcilva@microsoft.com> - 0.191.0-2
- Bump package to rebuild with rust 1.72.0

* Mon Jan 30 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.191.0-1
- Upgrade to version 0.191.0
- Added patches to fix libflux.so file linking issues

* Fri Jan 13 2023 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 0.179.0-1
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified
- Upgrade to version 0.179.0

* Wed Oct 19 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Add 0001-fix-compile-error-with-Rust-1.64-5273.patch:
    Fix build for rust1.64

* Tue Oct  4 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.171.0, see:
  https://github.com/influxdata/flux/releases/

* Thu Jun 30 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Add disable-static-library.patch: do not build static library
  (follow Factory guidelines).

* Thu Jun  9 2022 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.161.0, see:
  https://github.com/influxdata/flux/releases/

* Wed Dec  1 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Fix libflux.so for Leap 15.2 and 15.3 (boo#1193120)

* Tue Nov 16 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.139.0, see:
  https://github.com/influxdata/flux/releases/
- Build fluxc and fluxdoc binaries

* Tue Oct 26 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.136.0, see:
  https://github.com/influxdata/flux/releases/

* Fri Sep 24 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.131.0, see:
  https://github.com/influxdata/flux/releases/

* Thu Jun 10 2021 Michal Hrusecky <michal.hrusecky@opensuse.org>
- Update to version 0.117.3, see:
  https://github.com/influxdata/flux/releases/

* Wed May 19 2021 Michal Hrusecky <michal.hrusecky@opensuse.org>
- Update to version 0.116.0, see:
  https://github.com/influxdata/flux/releases/

* Fri Mar  5 2021 Matwey Kornilov <matwey.kornilov@gmail.com>
- Initial version
