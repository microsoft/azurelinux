%global rustflags '-Clink-arg=-Wl,-z,relro,-z,now'

%define libflux_suffix %(echo %{version} | tr . _)

Name:           flux
Version:        0.179.0
Release:        0%{?dist}
Summary:        Influx data language
License:        MIT
Group:          Productivity/Databases/Servers
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/influxdata/flux
Source0:        %{url}%archive/refs/tags/v%{version}#/%{name}-%{version}.tar.gz
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
BuildRequires:  rust >= 1.45
BuildRequires:  kernel-headers
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Flux is a lightweight scripting language for querying databases (like InfluxDB)
and working with data. It is part of InfluxDB 1.7 and 2.0, but can be run
independently of those. This repository contains the language definition and an
implementation of the language core.

%package -n libflux%{libflux_suffix}
Summary:        Influx data language
Provides:       libflux = %{version}-%{release}

%description -n libflux%{libflux_suffix}
Flux is a lightweight scripting language for querying databases (like InfluxDB)
and working with data. It is part of InfluxDB 1.7 and 2.0, but can be run
independently of those. This repository contains the language definition and an
implementation of the language core.

%package -n libflux-devel
Summary:        Development libraries and header files for Influx data language
Requires:       libflux%{libflux_suffix} = %{version}-%{release}

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

%post -n libflux%{libflux_suffix} -p /sbin/ldconfig
%postun -n libflux%{libflux_suffix} -p /sbin/ldconfig

%files -n libflux%{libflux_suffix}
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