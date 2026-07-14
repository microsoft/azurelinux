%global upstream_name SymCrypt-OpenSSL

Summary:        The standalone KeysInUse library for tracking asymmetric key and certificate usage
Name:           libkeysinuse
Version:        1.11.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt-OpenSSL
Source0:        https://github.com/microsoft/SymCrypt-OpenSSL/archive/v%{version}.tar.gz#/%{upstream_name}-%{version}.tar.gz
BuildRequires:  SymCrypt >= 103.8.0
BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel

Requires:       openssl

%description
KeysInUse logging allows application owners to keep an inventory of which
certificates and keys are actively being used on their machine. libkeysinuse.so
is the standalone build of the KeysInUse functionality from SymCrypt-OpenSSL,
exported as an API for other OpenSSL providers, engines, and applications to use
independently of the SymCrypt provider.

%package devel
Summary:        Development files for libkeysinuse
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -q -n %{upstream_name}-%{version}

%build
mkdir bin; cd bin

cmake   .. \
        -DKEYSINUSE_STANDALONE=1 \
        -DOPENSSL_ROOT_DIR="%{_prefix}/local/ssl" \
        -DCMAKE_INSTALL_PREFIX=%{_prefix} \
        -DCMAKE_INSTALL_LIBDIR=%{_lib} \
        -DCMAKE_INSTALL_INCLUDEDIR=include \
        -DCMAKE_BUILD_TYPE=RelWithDebInfo

cmake --build .

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

install KeysInUse/keysinuse.h %{buildroot}%{_includedir}
cp -P bin/KeysInUse/libkeysinuse.so* %{buildroot}%{_libdir}

mkdir -p %{buildroot}%{_localstatedir}/log/keysinuse/

%files
%license LICENSE
%{_libdir}/libkeysinuse.so.*

%dir %attr(1733, root, root) %{_localstatedir}/log/keysinuse/

%files devel
%{_includedir}/keysinuse.h
%{_libdir}/libkeysinuse.so

%changelog
* Mon Jul 13 2026 Maxwell Moyer-McKee <mamckee@microsoft.com> - 1.11.0-1
- Initial release of standalone KeysInUse library
