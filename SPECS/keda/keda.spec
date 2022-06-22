Summary:        Kubernetes-based Event Driven Autoscaling
Name:           keda
Version:        2.4.0
Release:        2%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/kedacore/keda
#Source0:       https://github.com/kedacore/%%{name}/archive/refs/tags/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/kedacore/%%{name}/archive/refs/tags/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
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
BuildRequires:  golang >= 1.15

%description
KEDA is a Kubernetes-based Event Driven Autoscaling component. 
It provides event driven scale for any container running in Kubernetes 

%prep
%setup -q

%build
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner
export LDFLAGS="-X=github.com/kedacore/keda/v2/version.GitCommit= -X=github.com/kedacore/keda/v2/version.Version=main"

go build -ldflags "$LDFLAGS" -mod=vendor -v -o bin/keda main.go

gofmt -l -w -s .
go vet ./...

go build -ldflags "$LDFLAGS" -mod=vendor -v -o bin/keda-adapter adapter/main.go

%install
mkdir -p %{buildroot}%{_bindir}
cp ./bin/keda %{buildroot}%{_bindir}
cp ./bin/keda-adapter %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}
%{_bindir}/%{name}-adapter

%changelog
* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 2.4.0-2
- Bump release to rebuild with golang 1.18.3
- License verified

* Wed Aug 25 2021 Henry Li <lihl@microsoft.com> - 2.4.0-1
- Original version for CBL-Mariner
