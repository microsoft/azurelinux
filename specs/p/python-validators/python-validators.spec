# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name validators

Name:           python-%{pypi_name}
Version:        0.35.0
Release: 5%{?dist}
Summary:        Data validation in Python for humans

License:        LicenseRef-Callaway-BSD
URL:            https://github.com/kvesteri/validators
Source0:        %pypi_source
BuildArch:      noarch

%description
Python has all kinds of data validation tools, but every one of them seems to
require defining a schema or form. I wanted to create a simple validation
library where validating a simple value does not require defining a form or
a schema.

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%description -n python3-%{pypi_name}
Python has all kinds of data validation tools, but every one of them seems to
require defining a schema or form. I wanted to create a simple validation
library where validating a simple value does not require defining a form or
a schema.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files validators

%check
pytest-%{python3_version} --ignore "tests/crypto_addresses/test_eth_address.py"

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc CHANGES.md README.md
%license LICENSE.txt

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.35.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.35.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.35.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Fabian Affolter <mail@fabian-affolter.ch> - 0.35.0-1
- Update to latest upstream release (closes rhbz#2355176)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.34.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 17 2024 Fabian Affolter <mail@fabian-affolter.ch> - 0.34.0-1
- Update to new upstream version (closes rhbz#2295587)

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.28.3-3
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 16 2024 Fabian Affolter <mail@fabian-affolter.ch> - 0.28.3-1
- Update to latest upstream release (closes rhbz#2276061)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.28.0-2
- Rebuilt for Python 3.13

* Sat Apr 13 2024 Fabian Affolter <mail@fabian-affolter.ch> - 0.28.0-1
- Update to latest upstream release (closes rhbz#2231344)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.20.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Aug 19 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.20.0-1
- Update to latest upstream release 0.18.1 (closes rhbz#2081763)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.18.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.18.1-2
- Rebuilt for Python 3.11

* Thu Mar 24 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.18.1-1
- Update to latest upstream release 0.18.1 (closes rhbz#1697459)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.14.2-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.14.2-4
- Add python3-setuptools as BR

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.2-3
- Rebuilt for Python 3.9

* Tue Jan 28 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.14.2-2
- Fix wildcard

* Sun Jan 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.14.2-1
- Update to latest upstream release 0.14.2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.13.0-1
- Update to latest upstream release 0.13.0
- Update source
- Update variable name

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.12.0-6
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 William Moreno Reyes <williamjmorenor@gmail.com> - 0.12.0-2
- Initial import

* Mon Dec 25 2017 William Moreno Reyes <williamjmorenor@gmail.com> - 0.12.0-1
- Initial packaging
  Skip docs build with sphinx because a lot of extensions
