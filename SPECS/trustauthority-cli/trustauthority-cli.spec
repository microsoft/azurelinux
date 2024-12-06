# Define global variables
%global debug_package %{nil}
%global gh_owner    intel
%global gh_project  trustauthority-client-for-go
%global gh_version  1.7.0

Name:           trustauthority-cli
Summary:        Intel Trust Authority TDX CLI Tool
Version:        %{gh_version}
Release:        1%{?dist}
License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        v%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  golang >= 1.22
BuildRequires:  build-essential

%description
Intel Trust Authority TDX CLI tool enables quote generation and 
token retrieval for TDX-enabled virtual machines. It provides command-line 
interfaces for generating quotes and retrieving tokens from Intel Trust 
Authority service.

%prep
%autosetup -n %{gh_project}-%{gh_version}
# Extract vendor files
tar xf %{SOURCE1}

%build
cd tdx-cli
# Build the CLI tool
go build -mod=vendor -o trustauthority-cli

%install
install -d %{buildroot}%{_bindir}
install -p -m 755 tdx-cli/trustauthority-cli %{buildroot}%{_bindir}/trustauthority-cli

%check
# Run all tests with verbose output
go test -v ./... --tags=test

%files
%license LICENSE
%doc tdx-cli/README.md
%{_bindir}/trustauthority-cli

%changelog
* Sat Nov 23 2024 Archana Choudhary <archana1@microsoft.com> - 1.7.0-1
- Initial RPM package for Intel Trust Authority TDX CLI tool
