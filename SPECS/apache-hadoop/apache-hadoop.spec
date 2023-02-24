Summary:        Software platform for processing vast amounts of data
Name:           apache-hadoop
Version:        3.3.4
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Productivity/Databases/Servers
URL:            http://hadoop.apache.org/
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# Use generate_source_tarbbal.sh to get this generated from a source code file.
# How to re-build this file:
#   1. wget https://github.com/influxdata/influxdb/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
Source1:        %{name}-%{version}-vendor.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  fuse-devel
BuildRequires:  make
BuildRequires:  g++
BuildRequires:  gcc
BuildRequires:  clang
BuildRequires:  git
BuildRequires:  maven
BuildRequires:  file
BuildRequires:  pkgconfig(snappy-devel)
BuildRequires:  zlib-devel
BuildRequires:  cyrus-sasl-devel
BuildRequires:  openssl-devel
BuildRequires:  build-essential
BuildRequires:  doxygen
BuildRequires:  yasm
BuildRequires:  libtool
BuildRequires:  libtirpc-devel
BuildRequires:  python3
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel
BuildRequires:  protobuf-devel
BuildRequires:  temurin-8-jdk
Requires:       temurin-8-jdk

%description
Hadoop is a software platform that lets one easily write and
run applications that process vast amounts of data.