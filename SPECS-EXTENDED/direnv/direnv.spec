Summary:        A shell extension that manages your environment
Name:           direnv
Version:        2.37.1
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/direnv/direnv
Source0:        https://github.com/direnv/direnv/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
BuildRequires:  golang
BuildRequires:  make
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
direnv is an extension for your shell. It augments existing shells with a new
feature that can load and unload environment variables depending on the current
directory. Before each prompt, direnv checks for the existence of a .envrc file
in the current and parent directories. If the file exists, it is loaded into a
bash sub-shell and all exported variables are then captured by direnv and made
available to the current shell.

%prep
%autosetup -p1 -n %{name}-%{version} -a1

%build
export GOPATH=%{our_gopath}
export GO111MODULE=on
# Use the local vendor cache, do not download modules.
export GOFLAGS="-buildmode=pie -trimpath -mod=vendor -modcacherw"
make build BASH_PATH=%{_bindir}/bash

%install
install -d %{buildroot}%{_bindir}
install -m 0755 -p direnv %{buildroot}%{_bindir}/direnv
install -d %{buildroot}%{_mandir}/man1
cp -p man/*.1 %{buildroot}%{_mandir}/man1
install -d %{buildroot}%{_datadir}/fish/vendor_conf.d
echo "%{_bindir}/direnv hook fish | source" > %{buildroot}%{_datadir}/fish/vendor_conf.d/direnv.fish

%check
./direnv version

%files
%license LICENSE
%doc README.md CHANGELOG.md CONTRIBUTING.md
%{_bindir}/direnv
%{_mandir}/man1/direnv.1*
%{_mandir}/man1/direnv-fetchurl.1*
%{_mandir}/man1/direnv-stdlib.1*
%{_mandir}/man1/direnv.toml.1*
%{_datadir}/fish/vendor_conf.d/direnv.fish

%changelog
* Wed Jul 15 2026 Siva Kannan <sikannan@microsoft.com> - 2.37.1-1
- Original version for Azure Linux (license: MIT).
- License verified
