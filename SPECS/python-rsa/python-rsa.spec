%{!?python3_sitelib: %global python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%global pkgname rsa

Summary:        Purely Python RSA implementation
Name:           python-%{pkgname}
Version:        4.9
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://stuvel.eu/software/rsa/
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/aa/65/7d973b89c4d2351d7fb232c2e452547ddfa243e93131e7cfa766da627b52/%{pkgname}-%{version}.tar.gz
BuildArch:  noarch

%description
Python-RSA is a pure-Python RSA implementation. It supports encryption and decryption, signing and verifying signatures, and key generation according to PKCS#1 version 1.5.

%package -n python3-%{pkgname}
Summary:    Various memoizing collections and decorators

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-pyasn1

%description -n python3-%{pkgname}
Python-RSA is a pure-Python RSA implementation. It supports encryption and decryption, signing and verifying signatures, and key generation according to PKCS#1 version 1.5.

%prep
%autosetup -n %{pkgname}-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --skip-build --root=%{buildroot}

%files -n python3-%{pkgname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*.egg-info
%{_bindir}/*

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 4.9-1
- Auto-upgrade to 4.9 - Azure Linux 3.0 - package upgrades

* Fri May 21 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 4.7.2-1
- Update package version to fix CVE-2020-25658

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 4.6-1
- Original version for CBL-Mariner
- License verified
