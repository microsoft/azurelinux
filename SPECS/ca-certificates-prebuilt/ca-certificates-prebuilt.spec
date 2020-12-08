Summary:        Prebuilt version of ca-certificates package
Name:           ca-certificates-prebuilt

Version:        20200720
Release:        1%{?dist}
License:        MIT

URL:            https://hg.mozilla.org
Group:          System Environment/Security
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildArch:      noarch

BuildRequires:  ca-certificates-base
Conflicts:      ca-certificates-base
Conflicts:      ca-certificates

%description
Prebuilt version of the ca-certificates-base package with no runtime dependencies.

%prep -q

%build

%install

mkdir -p $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy/
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pki/

install -p -m 644 %{_datadir}/pki/ca-trust-legacy/* $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy/
install -p -m 644 %{_datadir}/pki/ca-trust-source/* $RPM_BUILD_ROOT%{_datadir}/pki/ca-trust-legacy/
cp -r %{_sysconfdir}/pki/* $RPM_BUILD_ROOT%{_sysconfdir}/pki/

%files
# Base certs bundle file with trust
%{_datadir}/pki/*
%{_sysconfdir}/pki/*

%changelog
* Wed Dec 2 2020 Mateusz Malisz <mamalisz@microsoft.com> - 20200720-1
- Initial version.
