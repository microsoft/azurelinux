%global debug_package %{nil}

Summary:        Fast and flexible DNS server
Name:           coredns
Version:        1.7.0
Release:        1%{?dist}
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/coredns/coredns
#Source0:       https://github.com/coredns/coredns/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/coredns/coredns/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar -cf %%{name}-%%{version}-vendor.tar.gz vendor
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         makefile-buildoption-commitnb.patch

BuildRequires:  golang >= 1.12

%description
CoreDNS is a fast and flexible DNS server.

%prep
%autosetup -p1

%build
# create vendor folder from the vendor tarball and set vendor mode
tar -xf %{SOURCE1} --no-same-owner
export BUILDOPTS="-mod=vendor -v"
# set commit number that correspond to the github tag for that version
export GITCOMMIT="f59c03d"
make

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} %{name}

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.7.0-1
- Original version for CBL-Mariner.
