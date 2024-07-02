Summary:        Little helper to run CNCF's k3s in Docker
Name:           k3d
Version:        5.6.3
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/Tools
URL:            https://github.com/k3d-io/k3d
Source0:        https://github.com/k3d-io/k3d/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
BuildRequires:  golang >= 1.18
Requires:       moby-engine

%description
Little helper to run CNCF's k3s in Docker, useful for local development and CI testing.

%prep
%setup -q

%build
tar --no-same-owner -xf %{SOURCE0}
export GOPATH=%{our_gopath}
go build -buildmode=pie -mod=vendor

%install
install -D -m 0755 ./k3d %{buildroot}%{_bindir}/k3d

%check
go test -mod=vendor ./...
./k3d --version

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/%{name}

%changelog
* Thu Jun 13 2024 Tom Fay <tomfay@microsoft.com> - 5.6.3-1
- Original version for CBL-Mariner.
- License verified.
