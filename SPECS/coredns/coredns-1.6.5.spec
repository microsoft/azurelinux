%global debug_package %{nil}

Summary:        Fast and flexible DNS server
Name:           coredns
Version:        1.6.5
Release:        1%{?dist}
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/coredns/coredns
#Source0:       https://github.com/coredns/coredns/archive/v1.6.5.tar.gz
Source0:        %{name}-%{version}.tar.gz
# use go modules from tarball because they cannot be downloaded at build time
# (build system prevents that)
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         makefile-buildoption-commitnb-%{version}.patch

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
export GITCOMMIT="c2fd1b2"
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
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.6.5-1
- Initial version
