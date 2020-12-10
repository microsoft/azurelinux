Summary:        Prebuilt version of ca-certificates package
Name:           ca-certificates-prebuilt
Version:        20200720
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://hg.mozilla.org
BuildRequires:  ca-certificates-base
Conflicts:      ca-certificates
Conflicts:      ca-certificates-base
BuildArch:      noarch

%description
Prebuilt version of the ca-certificates-base package with no runtime dependencies.

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
