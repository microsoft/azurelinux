Summary:        Switch user and group before executing a container command
Name:           gosu
Version:        1.19
Release:        1%{?dist}
License:        Apache-2.0 AND BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/tianon/gosu
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Generate with toolkit/scripts/build_go_vendor_cache.sh using Source0,
# --pkgVersion 1.19 --vendorVersion 1, then rename the output to Source1.
Source1:        %{name}-%{version}-vendor.tar.gz
BuildRequires:  golang >= 1.20

%global debug_package %{nil}

%description
gosu switches to the requested user and group, sets HOME, and directly executes
the supplied command. It is intended for container entrypoints that start as root
and then run an application as an unprivileged user.

%prep
%setup -q
tar -xf %{SOURCE1}
cp vendor/github.com/moby/sys/user/LICENSE LICENSE.moby-user
cp vendor/golang.org/x/sys/LICENSE LICENSE.x-sys

%build
export CGO_ENABLED=0
export GOPROXY=off
export GOTOOLCHAIN=local
export GOCACHE=%{_builddir}/.gosu-cache
go build -mod=vendor -trimpath -buildvcs=false -buildmode=pie -o gosu .

%install
install -D -m 0755 gosu %{buildroot}%{_bindir}/gosu

%check
test "$(./gosu --version | cut -d ' ' -f1)" = "%{version}"
./gosu --help

%files
%license LICENSE LICENSE.moby-user LICENSE.x-sys
%doc README.md
%{_bindir}/gosu

%changelog
* Wed Oct 28 2026 Mitch Zhu <mitchzhu@microsoft.com> - 1.19-1
- Original version for Azure Linux.
- License verified.
- Build gosu from source with vendored dependencies.
