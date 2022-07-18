Summary:        The KeysInUse Engine for OpenSSL allows the logging of private key usage through OpenSSL
Name:           KeysInUse-OpenSSL
Version:        0.3.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System/Libraries
URL:            https://github.com/microsoft/KeysInUse-OpenSSL
#Source0:       https://github.com/microsoft/KeysInUse-OpenSSL/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  golang >= 1.16.6
BuildRequires:  make
BuildRequires:  openssl-devel
Requires:       openssl < 1.1.2
Requires:       openssl >= 1.1.1

%description
 The KeysInUse Engine for OpenSSL allows the logging of private key usage through OpenSSL

%prep
%setup -q

%build
export GO111MODULE=off

cmake -DCMAKE_TOOLCHAIN_FILE=./cmake-toolchains/linux-amd64-glibc.cmake -H./ -B./build
cmake --build ./build --target keysinuse

cd ./packaging/util
make $(realpath ../../bin/keysinuseutil)

%define keysinuse_dir %{buildroot}/%{_libdir}/keysinuse/

%install
mkdir -p %{keysinuse_dir}
mkdir -p %{buildroot}%{_bindir}/

install -m 0644 ./bin/keysinuse.so %{keysinuse_dir}
install -m 0744 ./bin/keysinuseutil %{buildroot}%{_bindir}/

%files
%license LICENSE
%{_libdir}/keysinuse/keysinuse.so
%{_bindir}/keysinuseutil

%pre
if [ -x %{_bindir}/keysinuseutil ]; then
  echo "Disabling version $2 of keysinuse engine for OpenSSL"
  %{_bindir}/keysinuseutil uninstall || echo "Failed to deconfigure old version"
fi

%post
if [ ! -e %{_var}/log/keysinuse ]; then
  mkdir %{_var}/log/keysinuse
fi
chown root:root %{_var}/log/keysinuse
chmod 1733 %{_var}/log/keysinuse

ln -s %{_lib}/keysinuse/keysinuse.so $(%{_bindir}/openssl version -e | awk '{gsub(/"/, "", $2); print $2}')/keysinuse.so

if [ -x %{_bindir}/keysinuseutil ]; then
  echo "Enabling keysinuse engine for OpenSSL"
  %{_bindir}/keysinuseutil install || echo "Configuring engine failed"
fi

%preun
if [ -x %{_bindir}/keysinuseutil ]; then
  echo "Disabling keysinuse engine for OpenSSL"
  %{_bindir}/keysinuseutil uninstall || echo "Deconfiguring keysinuse engine failed"
fi
with
engine_link=$(%{_bindir}/openssl version -e | awk '{gsub(/"/, "", $2); print $2}')/keysinuse.so
if [ -e $engine_link ]; then
  rm $engine_link
fi

%changelog
* Fri Jun 17 2022 Maxwell Moyer-McKee <mamckee@microsoft.com> - 0.3.1-1
- Original version for CBL-Mariner
- Verified license