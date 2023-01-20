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
Version:        0.179.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
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
BuildRequires:  cargo >= 1.45
BuildRequires:  kernel-headers
BuildRequires:  rust >= 1.45

%description
Flux is a lightweight scripting language for querying databases (like InfluxDB)
and working with data. It is part of InfluxDB 1.7 and 2.0, but can be run
independently of those. This repository contains the language definition and an
implementation of the language core.

%package -n libflux-%{libflux_suffix}
Summary:        Influx data language
Provides:       libflux = %{version}-%{release}

%description -n libflux-%{libflux_suffix}
Flux is a lightweight scripting language for querying databases (like InfluxDB)
and working with data. It is part of InfluxDB 1.7 and 2.0, but can be run
independently of those. This repository contains the language definition and an
implementation of the language core.

%package -n libflux-devel
Summary:        Development libraries and header files for Influx data language
Requires:       libflux-%{libflux_suffix} = %{version}-%{release}

%description -n libflux-devel
This package contains the header files and libraries for building
programs using Influx data language.

%prep
%autosetup
pushd libflux
tar -xf %{SOURCE1}
install -D %{SOURCE2} .cargo/config

popd

%build
pushd libflux
RUSTFLAGS=%{rustflags} cargo build --release
RUSTFLAGS=%{rustflags} cargo build --release --bin fluxc
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

install -D -m 755 libflux/target/release/fluxc %{buildroot}%{_bindir}/fluxc
install -D -m 755 libflux/target/release/fluxdoc %{buildroot}%{_bindir}/fluxdoc

%check
pushd libflux
RUSTFLAGS=%{rustflags} cargo test --release
popd

%post -n libflux-%{libflux_suffix} -p /sbin/ldconfig
%postun -n libflux%{libflux_suffix} -p /sbin/ldconfig

%files -n libflux-%{libflux_suffix}
%{_libdir}/libflux.so.%{version}

%files -n libflux-devel
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/fluxc
%{_bindir}/fluxdoc
%{_libdir}/libflux.so
%{_libdir}/pkgconfig/flux.pc
%dir %{_includedir}/influxdata
%{_includedir}/influxdata/flux.h

%changelog
* Fri Jan 13 10:49:53 UTC 2023 - Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com>
- Initial CBL-Mariner import from openSUSE Tumbleweed (license: same as "License" tag).
- License verified
- Upgrade to version 0.179.0

* Wed Oct 19 13:39:14 UTC 2022 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Add 0001-fix-compile-error-with-Rust-1.64-5273.patch:
    Fix build for rust1.64

* Tue Oct  4 15:21:40 UTC 2022 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.171.0, see:
  https://github.com/influxdata/flux/releases/

* Thu Jun 30 19:42:09 UTC 2022 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Add disable-static-library.patch: do not build static library
  (follow Factory guidelines).

* Thu Jun  9 15:55:20 UTC 2022 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.161.0, see:
  https://github.com/influxdata/flux/releases/

* Wed Dec  1 14:40:04 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Fix libflux.so for Leap 15.2 and 15.3 (boo#1193120)

* Tue Nov 16 16:55:49 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.139.0, see:
  https://github.com/influxdata/flux/releases/
- Build fluxc and fluxdoc binaries

* Tue Oct 26 16:46:43 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.136.0, see:
  https://github.com/influxdata/flux/releases/

* Fri Sep 24 17:21:31 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Update to version 0.131.0, see:
  https://github.com/influxdata/flux/releases/

* Thu Jun 10 08:17:57 UTC 2021 - Michal Hrusecky <michal.hrusecky@opensuse.org>
- Update to version 0.117.3, see:
  https://github.com/influxdata/flux/releases/

* Wed May 19 22:00:36 UTC 2021 - Michal Hrusecky <michal.hrusecky@opensuse.org>
- Update to version 0.116.0, see:
  https://github.com/influxdata/flux/releases/

* Fri Mar  5 14:08:31 UTC 2021 - Matwey Kornilov <matwey.kornilov@gmail.com>
- Initial version
