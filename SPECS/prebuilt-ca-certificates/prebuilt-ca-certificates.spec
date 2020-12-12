Summary:        Prebuilt version of ca-certificates package.
Name:           prebuilt-ca-certificates
Version:        20200720
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://hg.mozilla.org
BuildArch:      noarch

%description
Prebuilt versions of the ca-certificates package with no runtime dependencies.

%package base
Summary:        Prebuilt version of ca-certificates-base package.
BuildRequires:  ca-certificates-base
Conflicts:      ca-certificates
Conflicts:      ca-certificates-base
Conflicts:      ca-certificates-microsoft

%description base
%{summary}

%prep -q

%build

%install

mkdir -p %{buildroot}%{_datadir}/pki/ca-trust-legacy/
mkdir -p %{buildroot}%{_sysconfdir}/pki/

install -p -m 644 %{_datadir}/pki/ca-trust-legacy/* %{buildroot}%{_datadir}/pki/ca-trust-legacy/
install -p -m 644 %{_datadir}/pki/ca-trust-source/* %{buildroot}%{_datadir}/pki/ca-trust-legacy/
cp -r %{_sysconfdir}/pki/* %{buildroot}%{_sysconfdir}/pki/

%files
# Base certs bundle file with trust
%{_datadir}/pki/*
%{_sysconfdir}/pki/*

%changelog
* Wed Dec 2 2020 Mateusz Malisz <mamalisz@microsoft.com> - 20200720-1
- Original version for CBL-Mariner
