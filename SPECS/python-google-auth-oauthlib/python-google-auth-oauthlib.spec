%global pypi_name google-auth-oauthlib

Summary:        Google oAuth Authentication Library
Name:           python-%{pypi_name}
Version:        1.0.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/googleapis/google-auth-library-python-oauthlib
Source0:        https://files.pythonhosted.org/packages/e3/b4/ef2170c5f6aa5bc2461bab959a84e56d2819ce26662b50038d2d0602223e/%{pypi_name}-%{version}.tar.gz
BuildRequires:  python3-click
BuildRequires:  python3-devel
BuildRequires:  python3-google-auth
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-requests-oauthlib
BuildRequires:  python3-setuptools
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
This library provides oauthlib integration with google-auth.

%package -n     python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}

%description -n python3-%{pypi_name}
This library provides oauthlib integration with google-auth.

%prep
%autosetup -n %{pypi_name}-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
pip3 install pytest
PYTHONPATH=%{buildroot}%{python3_sitelib} pytest -v tests

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/google-oauthlib-tool
%{python3_sitelib}/google_auth_oauthlib/
%{python3_sitelib}/google_auth_oauthlib-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.0.0-1
- Auto-upgrade to 1.0.0 - Azure Linux 3.0 - package upgrades

* Mon Oct 17 2022 Riken Maharjan <rmaharjan@microsoft.com> - 0.5.3-2
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

* Thu Sep 15 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.3-1
- Update to latest upstream release 0.5.3 (closes rhbz#2095595)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 0.5.1-2
- Rebuilt for Python 3.11

* Fri Mar 18 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.1-1
- Update to latest upstream release 0.5.1 (closes rhbz#2064495)

* Thu Mar 03 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.5.0-1
- Update to latest upstream release 0.5.0 (closes rhbz#2018793)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.1-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 17 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.4.1-1
- Initial package for Fedora
