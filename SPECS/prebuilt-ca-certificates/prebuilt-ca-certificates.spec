# When updating, "Version" AND "Release" tags must be updated in the "ca-certificates" package as well.
Summary:        Prebuilt version of ca-certificates package.
Name:           prebuilt-ca-certificates
Version:        2.0.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://docs.microsoft.com/en-us/security/trusted-root/program-requirements
BuildArch:      noarch

BuildRequires:  ca-certificates = %{version}-%{release}

Conflicts:      prebuilt-ca-certificates-base

%description
Prebuilt version of the ca-certificates package with no runtime dependencies.

%prep -q

# Remove 'ca-certificate-base', if present. We don't want them
# to get mixed into the bundle provided by 'ca-certificates'.
if rpm -q ca-certificates-base &>/dev/null ; then rpm -e ca-certificates-base; fi

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
* Wed Dec 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-1
- Making removal of 'ca-certificates-base' account for the package not being installed.
- Updating 'URL' and 'Version' tags for CBL-Mariner 2.0.
- License verified.

* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-20
- Removing conflicts with 'ca-certificates-shared'.

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-19
- Original version for CBL-Mariner.
