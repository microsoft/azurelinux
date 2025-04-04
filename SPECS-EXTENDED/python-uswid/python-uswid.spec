%global srcname uswid
%global _description %{expand:
Software Identification (SWID) tags provide an extensible XML-based structure to
identify and describe individual software components, patches, and installation
bundles. XML SWID tag representations can be too large for devices with network
and storage constraints.}
Summary:        Python module for working with Firmware SBoMs
Name:           python-%{srcname}
Version:        0.5.0
Release:        4%{?dist}
License:        LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/hughsie/python-uswid
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-cbor2
BuildRequires:  python3-devel
BuildRequires:  python3-lxml
BuildRequires:  python3-pefile
BuildRequires:  python3-pytest
BuildRequires:  python3-setuptools
BuildRequires:  python3-wheel

%description -n python3-%{srcname} %{_description}

%prep
%autosetup -n python-%{srcname}-%{version}
sed -i -e '/^#!\//, 1d' %{srcname}/*.py

%build
%py3_build

%install
%py3_install

%check
#%{python3} setup.py test
%pytest

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/
%{_bindir}/%{srcname}

%changelog
* Mon Oct 28 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 0.5.0-4
- Integrating the spec into Azure Linux
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 0.5.0-2
- Rebuilt for Python 3.13

* Thu May 09 2024 Richard Hughes <richard@hughsie.com> - 0.5.0-1
- New upstream release

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Dec 03 2023 Richard Hughes <richard@hughsie.com> - 0.4.7-1
- New upstream release

* Mon Oct 09 2023 Richard Hughes <richard@hughsie.com> - 0.4.5-1
- New upstream release

* Tue Oct 03 2023 Richard Hughes <richard@hughsie.com> - 0.4.3-2
- Fix BRs

* Mon Oct 02 2023 Richard Hughes <richard@hughsie.com> - 0.4.3-1
- New upstream release

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 0.4.1-2
- Rebuilt for Python 3.12

* Sat Feb 04 2023 Richard Hughes <richard@hughsie.com> - 0.4.1-1
- Initial import (fedora#2167067).
