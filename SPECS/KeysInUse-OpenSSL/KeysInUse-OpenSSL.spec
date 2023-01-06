Summary:        The KeysInUse Engine for OpenSSL allows the logging of private key usage through OpenSSL
Name:           KeysInUse-OpenSSL
Version:        0.3.1
Release:        6%{?dist}
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

%install
mkdir -p %{buildroot}/%{_libdir}/engines-1.1/
mkdir -p %{buildroot}%{_bindir}/
install -m 0755 ./bin/keysinuse.so %{buildroot}/%{_libdir}/engines-1.1/keysinuse.so
install -m 0744 ./bin/keysinuseutil %{buildroot}%{_bindir}/

%files
%license LICENSE
%{_libdir}/engines-1.1/keysinuse.so
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

if [ -x %{_bindir}/keysinuseutil ]; then
  echo "Enabling keysinuse engine for OpenSSL"
  %{_bindir}/keysinuseutil install || echo "Configuring engine failed"
fi

%preun
if [ -x %{_bindir}/keysinuseutil ]; then
  %{_bindir}/keysinuseutil uninstall || echo "Deconfiguring keysinuse engine failed"
fi

%changelog
* Fri Jan 06 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.3.1-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 0.3.1-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.3.1-4
- Bump release to rebuild with go 1.18.8

* Thu Sep 01 2022 Maxwell Moyer-McKee <mamckee@microsoft.com> - 0.3.1-3
- Fix bad permissions on engine library during package install
- Simplify package installation strategy

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 0.3.1-2
- Bump release to rebuild against Go 1.18.5

* Fri Jun 17 2022 Maxwell Moyer-McKee <mamckee@microsoft.com> - 0.3.1-1
- Original version for CBL-Mariner
- Verified license
