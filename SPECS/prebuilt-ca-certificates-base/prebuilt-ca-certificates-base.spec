Summary:        Prebuilt version of ca-certificates-base package.
Name:           prebuilt-ca-certificates-base
# When updating, "Epoch, "Version", AND "Release" tags must be updated in the "ca-certificates" package as well.
Epoch:          1
Version:        2.0.0
Release:        14%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://docs.microsoft.com/en-us/security/trusted-root/program-requirements
BuildArch:      noarch

BuildRequires:  ca-certificates-base = %{epoch}:%{version}-%{release}

Conflicts:      ca-certificates-shared
Conflicts:      prebuilt-ca-certificates

%description
Prebuilt version of the ca-certificates-base package with no runtime dependencies.

%prep -q

# Remove 'ca-certificates', if present. We don't want them
# to get mixed into the bundle provided by 'ca-certificates-base'.
if rpm -q ca-certificates &>/dev/null; then rpm -e --nodeps ca-certificates; fi

%build

%install

mkdir -p %{buildroot}%{_sysconfdir}/pki/{tls/certs,ca-trust/extracted,java}

cp %{_sysconfdir}/pki/tls/cert.pem %{buildroot}%{_sysconfdir}/pki/tls/
cp -r %{_sysconfdir}/pki/tls/certs/* %{buildroot}%{_sysconfdir}/pki/tls/certs/
cp -r %{_sysconfdir}/pki/ca-trust/extracted/* %{buildroot}%{_sysconfdir}/pki/ca-trust/extracted/
cp %{_sysconfdir}/pki/java/cacerts %{buildroot}%{_sysconfdir}/pki/java/

find %{buildroot} -name README -delete

%files
# Base certs bundle file with trust
%{_sysconfdir}/pki/tls/cert.pem
%{_sysconfdir}/pki/tls/certs/*
%{_sysconfdir}/pki/ca-trust/extracted/*
%{_sysconfdir}/pki/java/cacerts

%changelog
* Tue Dec 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1:2.0.0-14
- Making 'Release' match with 'ca-certificates'.

* Mon May 08 2023 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-13
- Making 'Release' match with 'ca-certificates'.

* Thu Mar 30 2023 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-12
- Making 'Release' match with 'ca-certificates'.

* Fri Mar 17 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.0.0-11
- Making 'Release' match with 'ca-certificates'.

* Thu Feb 23 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.0.0-10
- Making 'Release' match with 'ca-certificates'.

* Tue Dec 06 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-9
- Making 'Release' match with 'ca-certificates'.

* Fri Oct 07 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-8
- Making 'Release' match with 'ca-certificates'.

* Wed Aug 03 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-7
- Making 'Release' match with 'ca-certificates'.

* Wed Jun 29 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-6
- Adding conflict information with "ca-certificates-shared".

* Wed Jun 29 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-5
- Making 'Release' match with 'ca-certificates'.

* Thu Jun 02 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.0.0-4
- Making 'Release' match with 'ca-certificates'.

* Fri May 20 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-3
- Making 'Release' match with 'ca-certificates'.

* Fri May 06 2022 CBL-Mariner Service Account <cblmargh@microsoft.com> - 2.0.0-2
- Making 'Release' match with 'ca-certificates'.

* Wed Dec 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.0.0-1
- Updating 'URL' and 'Version' tags for CBL-Mariner 2.0.

* Tue Oct 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-20
- Removing conflicts with 'ca-certificates-shared'.
- License verified.

* Thu Sep 23 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-19
- Making 'Release' match with 'ca-certificates'.
- Removing legacy components.
- Adding a conflict with a new prebuilt set of certs.

* Mon Sep 13 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-18
- Making 'Release' match with 'ca-certificates'.

* Fri Aug 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-17
- Making 'Release' match with 'ca-certificates'.

* Fri Aug 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-16
- Making 'Release' match with 'ca-certificates'.
- No longer have to remove 'ca-bundle.legacy.crt' and 'ca-legacy.conf' - gone from 'ca-certificates'.

* Wed Jul 07 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-15
- Making 'Release' match with 'ca-certificates'.

* Thu Jun 03 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 20200720-14
- Making 'Release' match with 'ca-certificates'.

* Fri Mar 12 2021 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 20200720-13
- Making 'Release' match with 'ca-certificates'.

* Sat Mar 06 2021 CBL-Mariner Servicing Account <clbmargh@microsoft.com> - 20200720-12
- Making 'Release' match with 'ca-certificates'.

* Mon Feb 08 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-11
- Making 'Release' match with 'ca-certificates'.

* Tue Jan 12 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 20200720-10
- Making 'Release' match with 'ca-certificates'.

* Wed Dec 2 2020 Mateusz Malisz <mamalisz@microsoft.com> - 20200720-1
- Original version for CBL-Mariner
