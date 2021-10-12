# When updating, "Version" AND "Release" tags must be updated in the "ca-certificates" package as well.
Summary:        Prebuilt version of ca-certificates package.
Name:           prebuilt-ca-certificates
Version:        20200720
Release:        20%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://hg.mozilla.org
BuildArch:      noarch

BuildRequires:  ca-certificates = %{version}-%{release}

Conflicts:      prebuilt-ca-certificates-base

%description
Prebuilt version of the ca-certificates package with no runtime dependencies.

%prep -q

# We don't want the pre-installed base set of certificates
# to get mixed into the bundle provided by 'ca-certificates'.
rpm -e ca-certificates-base

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/pki/

cp -r %{_sysconfdir}/pki/* %{buildroot}%{_sysconfdir}/pki/

find %{buildroot} -name README -delete

rm %{buildroot}%{_sysconfdir}/pki/tls/*.cnf
rm %{buildroot}%{_sysconfdir}/pki/rpm-gpg/*

%files
# Certs bundle file with trust
%{_sysconfdir}/pki/tls/cert.pem
%{_sysconfdir}/pki/tls/certs/*
%{_sysconfdir}/pki/ca-trust/extracted/*
%{_sysconfdir}/pki/java/cacerts

%changelog
* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-20
- Removing conflicts with 'ca-certificates-shared'.

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-19
- Original version for CBL-Mariner.
