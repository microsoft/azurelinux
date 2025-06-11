Summary:        A CLI tool to sign and verify artifacts
Name:           notation
Version:        1.3.2
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Notary Project
Distribution:   Azure Linux
URL:            https://github.com/notaryproject/notation
Source0:        https://github.com/notaryproject/notation/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
#Source0:        %{name}-%{version}.tar.gz
BuildRequires:  golang
BuildRequires:  make

%description
Notation is a CLI project to add signatures as standard items in the OCI registry ecosystem,
and to build a set of simple tooling for signing and verifying these signatures.

%prep
%setup -q

%build
make build

%install
mkdir -p %{buildroot}%{_bindir}
cp ./bin/notation %{buildroot}%{_bindir}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Tue Jun 10 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.3.2-1
- Original version for CBL-Mariner
