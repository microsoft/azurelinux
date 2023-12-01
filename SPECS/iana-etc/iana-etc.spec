Summary:        Data for network services and protocols
Name:           iana-etc
Version:        20211115
Release:        2%{?dist}
# IANA base information is Public Domain
# Scripts used to translate original XML data into the necessary format are MIT
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/Mic92/iana-etc
Source0:        https://github.com/Mic92/iana-etc/releases/download/%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-LICENSE
BuildArch:      noarch

%description
The iana-etc package provides data for network services and protocols.

%package doc
Summary:        Original IANA XML data for %{name}
License:        Public Domain
Requires:       %{name} = %{version}-%{release}

%description doc
Original IANA XML data for %{name}

%prep
%autosetup
cp %{SOURCE1} ./LICENSE

%build
# Empty- nothing to build

%install
# Install data files into %%{_sysconfdir}
install -vdm 755 %{buildroot}%{_sysconfdir}
install -vm 644 protocols %{buildroot}%{_sysconfdir}/protocols
install -vm 644 services %{buildroot}%{_sysconfdir}/services

# %%check
# No tests available- this is just a data package

%files
%license LICENSE
%config %{_sysconfdir}/protocols
%config %{_sysconfdir}/services

%files doc
%doc protocol-numbers.xml service-names-port-numbers.xml

%changelog
* Mon Sep 12 2022 Olivia Crain <oliviacrain@microsoft.com> - 20211115-2
- Separate documents into separate package to reduce base package size

* Mon Nov 22 2021 Olivia Crain <oliviacrain@microsoft.com> - 20211115-1
- Switch to new upstream source used by LFS and upgrade to latest
- Use new release version corresponding to IANA source update dates
- Include original IANA XML sources in packaging
- License verified (now MIT, old upstream was OSL 3.0)

* Tue May 26 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.30-5
- Adding the "%%license" macro.

* Fri May 08 2020 Joe Schmitt <joschmit@microsoft.com> 2.30-4
- Remove sha1 macro.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.30-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.30-2
- GA - Bump release of all rpms

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> 2.30-1
- Initial build. First version
