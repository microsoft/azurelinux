Summary:        Dasel (short for data-selector) allows you to query and modify data structures using selector strings. Comparable to jq, yq, and xmlstarlet, but for any data format.
Name:           dasel
Version:        2.8.1
Release:        3%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Applications/System
URL:            https://github.com/TomWright/dasel
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-govendor-v1.tar.gz
Patch1:         CVE-2024-45338.patch
Patch2:         CVE-2025-22872.patch
Patch3:         CVE-2025-47911.patch
Patch4:         CVE-2025-58190.patch
BuildRequires:  golang >= 1.22

%description
Say good bye to learning new tools just to work with a different data format.
Dasel uses a standard selector syntax no matter the data format. This means that once you learn how to use dasel you immediately have the ability to query/modify any of the supported data types without any additional tools or effort.

%prep
%autosetup -p1 -a 1

%build
export GOPATH=$HOME/go
export GOBIN=$GOPATH/bin
export PATH=$PATH:$GOPATH:$GOBIN
export GO111MODULE=on

# Build dasel
go build -mod vendor -o bin/dasel ./cmd/dasel

%install
mkdir -p %{buildroot}%{_bindir}
install -D -m 0755 bin/dasel %{buildroot}%{_bindir}/

%check
export GOTRACEBACK=all
export GO111MODULE=on
go test ./...

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{_bindir}/dasel

%changelog
* Thu Feb 12 2026 Azure Linux Security Servicing Account <azurelinux-security@microsoft.com> - 2.8.1-3
- Patch for CVE-2025-58190, CVE-2025-47911

* Tue Jun 24 2025 Archana Shettigar <v-shettigara@microsoft.com> - 2.8.1-2
- Patch CVE-2024-45338 & CVE-2025-22872

* Tue Jun 17 2025 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 2.8.1-1
- Original version for Azure Linux (license: MIT)
- License verified
