Summary:        Python package for providing Mozilla's CA Bundle
Name:           python-certifi
Version:        2023.05.07
Release:        1%{?dist}
License:        MPL-2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://certifi.io/
Source:         https://github.com/certifi/%{name}/archive/%{version}/%{name}-%{version}.tar.gz
Patch0:         certifi-2022.12.07-use-system-cert.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

%if %{with_check}
BuildRequires:  ca-certificates-base
BuildRequires:  python3-pytest
%endif

%description
This Azure Linux package does not include its own certificate
collection. It reads the system shared certificate trust collection
instead. For more details on this system, see the 'ca-certificates' package.

%package -n python3-certifi
Summary:        %{summary}

Requires:       %{_sysconfdir}/pki/tls/certs/ca-bundle.crt

%description -n python3-certifi
This Azure Linux package does not include its own certificate
collection. It reads the system shared certificate trust collection
instead. For more details on this system, see the 'ca-certificates' package.

This package provides the Python 3 certifi library.

%prep
%autosetup -p1

# Remove bundled root certificates collection
rm -rf certifi/*.pem

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files certifi

%check
%pytest -v

%files -n python3-certifi -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Aug 04 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 2023.05.07-1
- Removing bundled certificates.
- Switching to Fedora 39 implementation of the spec (license: MIT).

* Tue Jan 24 2023 Muhammad Falak <mwani@microsoft.com> - 2022.12.07-1
- Bump version to 2022.12.07 to address CVE-2022-23491

* Sat Feb 12 2022 Muhammad Falak <mwani@microsoft.com> - 2021.10.08-2
- Add an explict BR on pip
- Drop un-needed dependencies
- Use `%pytest` to enable ptest

* Wed Feb 09 2022 Nick Samson <nisamson@microsoft.com> - 2021.10.08-1
- Updated URL, updated to 2021.10.08

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 2018.10.15-6
- Add license to python3 package
- Remove python2 package
- Lint spec

* Tue Oct 20 2020 Andrew Phelps <anphel@microsoft.com> - 2018.10.15-5
- Fix check test

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2018.10.15-4
- Added %%license line automatically

* Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2018.10.15-3
- Removing *Requires for "ca-certificates".

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2018.10.15-2
- Renaming python-pytest to pytest

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> - 2018.10.15-1
- Update to 2018.10.15. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2018.08.24-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> - 2018.08.24-1
- Initial packaging
