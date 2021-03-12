%define         debug_package %{nil}
%define         OUR_GOPATH %{_topdir}/.gopath
Summary:        High-level tool for Linux filesystem encryption management
Name:           fscrypt
Version:        0.2.9
Release:        1%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://github.com/google/fscrypt
#Source0:       https://github.com/google/fscrypt/archive/v%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
#Source1:       https://github.com/client9/misspell/archive/v0.3.4.tar.gz
Source1:        misspell-0.3.4.tar.gz
#Source2:       https://github.com/golang/protobuf/archive/v1.2.0.tar.gz
Source2:        protobuf-1.2.0.tar.gz
#Source3:       https://github.com/pkg/errors/archive/v0.8.0.tar.gz
Source3:        errors-0.8.0.tar.gz
#Source4:       https://github.com/urfave/cli/archive/v1.20.0.tar.gz
Source4:        cli-1.20.0.tar.gz
#Source5:       https://github.com/wadey/gocovmerge
Source5:        gocovmerge.tar.gz
#Source6:       https://github.com/dominikh/go-tools/archive/2019.2.3.tar.gz
Source6:        go-tools-2019.2.3.tar.gz
# golang crypto, lint, sys and tools sources are git cloned.
# Please look at ./getgosources.sh for more details.
Source7:        golang-crypto-cbcb750295291b33242907a04be40e80801d0cfc.tar.gz
Source8:        golang-lint-16217165b5de779cb6a5e4fc81fa9c1166fda457.tar.gz
Source9:        golang-sys-63cb32ae39b28d6bb8e7e215c1fc39dd80dcdb02.tar.gz
Source10:       golang-tools-2077df36852e9a22c3b78f535833d3e54e9fcc8a.tar.gz
Patch0:         gomodule_off.patch

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  golang
BuildRequires:  make
BuildRequires:  pam-devel

Requires:       pam

%description
fscrypt is a high-level tool for the management of Linux filesystem encryption.
fscrypt manages metadata, key generation, key wrapping, PAM integration, and provides
a uniform interface for creating and modifying encrypted directories

%prep
%setup -q
%patch0
mkdir -p %{OUR_GOPATH}/src/github.com/google
ln -s %{_topdir}/BUILD/%{name}-%{version} %{OUR_GOPATH}/src/github.com/google/fscrypt

pushd ..

tar -xvf %{SOURCE1}
tar -xvf %{SOURCE2}
tar -xvf %{SOURCE3}
tar -xvf %{SOURCE4}
tar -xvf %{SOURCE5}
tar -xvf %{SOURCE6}
tar -xzvf %{SOURCE7}
tar -xzvf %{SOURCE8}
tar -xzvf %{SOURCE9}
tar -xzvf %{SOURCE10}

mkdir -p %{OUR_GOPATH}/src/github.com/client9/
mkdir -p %{OUR_GOPATH}/src/github.com/golang/
mkdir -p %{OUR_GOPATH}/src/github.com/pkg/
mkdir -p %{OUR_GOPATH}/src/github.com/urfave/
mkdir -p %{OUR_GOPATH}/src/github.com/wadey/
mkdir -p %{OUR_GOPATH}/src/honnef.co/go/
mkdir -p %{OUR_GOPATH}/src/golang.org/x/

ln -sfT %{_topdir}/BUILD/misspell-0.3.4 %{OUR_GOPATH}/src/github.com/client9/misspell
ln -sfT %{_topdir}/BUILD/protobuf-1.2.0 %{OUR_GOPATH}/src/github.com/golang/protobuf
ln -sfT %{_topdir}/BUILD/errors-0.8.0 %{OUR_GOPATH}/src/github.com/pkg/errors
ln -sfT %{_topdir}/BUILD/cli-1.20.0 %{OUR_GOPATH}/src/github.com/urfave/cli
ln -sfT %{_topdir}/BUILD/gocovmerge %{OUR_GOPATH}/src/github.com/wadey/gocovmerge
ln -sfT %{_topdir}/BUILD/go-tools-2019.2.3 %{OUR_GOPATH}/src/honnef.co/go/tools
ln -sfT %{_topdir}/BUILD/crypto-master %{OUR_GOPATH}/src/golang.org/x/crypto
ln -sfT %{_topdir}/BUILD/lint-master %{OUR_GOPATH}/src/golang.org/x/lint
ln -sfT %{_topdir}/BUILD/sys-master %{OUR_GOPATH}/src/golang.org/x/sys
ln -sfT %{_topdir}/BUILD/tools-master %{OUR_GOPATH}/src/golang.org/x/tools

popd

%build
export GOPATH=%{OUR_GOPATH}
export GOCACHE=%{OUR_GOPATH}/.cache

cd %{OUR_GOPATH}/src/github.com/google/fscrypt
make %{?_smp_mflags}

%install
cd %{OUR_GOPATH}/src/github.com/google/fscrypt
make install DESTDIR=%{buildroot} PREFIX=%{_prefix}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/fscrypt
%{_libdir}/security/pam_fscrypt.so
%{_datadir}/pam-configs/fscrypt

%changelog
*   Wed Mar 03 2021 Nicolas Ontiveros <niontive@microsoft.com> - 0.2.9-1
-   Original version for CBL-Mariner
-   License verified