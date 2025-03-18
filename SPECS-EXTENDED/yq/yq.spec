Summary:        Yq is a portable command-line YAML, JSON, XML, CSV, TOML  and properties processor
Name:           yq
Version:        4.45.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/mikefarah/yq
Source:         https://github.com/mikefarah/yq/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
BuildRequires:  golang
BuildRequires:  git
Requires:       git
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath
 
%description
yq is a lightweight and portable command-line YAML, JSON and XML processor. yq uses jq like syntax but works with yaml files as well as json, xml, properties, csv and tsv. It doesn't yet support everything jq does - but it does support the most common operations and functions, and more is being added continuously.

%prep
%autosetup -p1 -n %{name}-%{version} -a1

%build
export GOPATH=%{our_gopath}
# No mod download use vendor cache locally
export GOFLAGS="-buildmode=pie -trimpath -mod=vendor -modcacherw"
go build -o bin/ --ldflags "-X main.GitCommit= -X main.GitDescribe= -w -s"

%install
install -m 0755 -vd %{buildroot}%{_bindir}
install -m 0755 -vp bin/* %{buildroot}%{_bindir}/

%check
cp bin/yq .
bash ./scripts/acceptance.sh

%files
%license LICENSE
%doc examples CODE_OF_CONDUCT.md how-it-works.md project-words.txt
%doc release_instructions.txt CONTRIBUTING.md README.md release_notes.txt
%{_bindir}/yq

%changelog
* Mon Mar 17 2025 Sandeep Karambelkar <skarambelkar@microsoft.com> - 4.45.1-1
- Initial Azure Linux import from Fedora 42 (license: MIT).
- License verified
