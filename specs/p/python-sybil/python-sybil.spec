# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name sybil

Name:           python-%{pypi_name}
Version:        9.1.0
Release:        5%{?dist}
Summary:        Automated testing for the examples in your documentation

License:        MIT
URL:            https://sybil.readthedocs.io/
Source0:        https://github.com/simplistix/sybil/archive/refs/tags/%{version}.tar.gz
# seedir is not available in Fedora yet
Patch:          drop-dependency-on-seedir.patch
BuildArch:      noarch

%description
This library provides a way to test examples in your documentation by parsing
them from the documentation source and evaluating the parsed examples as part
of your normal test run. Integration is provided for the three main Python
test runners.

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pytest
BuildRequires:  python3-testfixtures
BuildRequires:  python3-pyyaml

%description -n python3-%{pypi_name}
This library provides a way to test examples in your documentation by parsing
them from the documentation source and evaluating the parsed examples as part
of your normal test run. Integration is provided for the three main Python
test runners.

%prep
%autosetup -n %{pypi_name}-%{version} -p1
sed -i "/seeddir/d" setup.py

%build
%py3_build

%install
%py3_install

%check
%{pytest} tests

%files -n python3-%{pypi_name}
%doc README.rst
%license docs/license.rst
%{python3_sitelib}/*.egg-info
%{python3_sitelib}/%{pypi_name}/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 9.1.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 9.1.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 9.1.0-2
- Rebuilt for Python 3.14

* Tue Apr 01 2025 Fabian Affolter <mail@fabian-affolter.ch> - 9.1.0-1
- Update to latest upstream release (closes rhbz#2322732)

* Sun Feb  2 2025 Orion Poplawski <orion@nwra.com> - 8.0.0-3
- Drop unneeded BR on python3-pytest-cov

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 24 2024 Fabian Affolter <mail@fabian-affolter.ch> - 8.0.0-1
- Update to latest upstream version (closes rhbz#2313721)

* Wed Sep 18 2024 Fabian Affolter <mail@fabian-affolter.ch> - 7.1.1-1
- Update to latest upstream version (closes rhbz#2250917)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 6.0.3-2
- Rebuilt for Python 3.13

* Sun Apr 07 2024 Fabian Affolter <mail@fabian-affolter.ch> - 6.0.3-1
- Update to latest upstream version 6.0.3

* Thu Apr 04 2024 Karolina Surma <ksurma@redhat.com> - 5.0.3-5
- Remove the compatibility patch - since Python 3.13.0a4 it's not needed

* Tue Feb 06 2024 Miro Hrončok <mhroncok@redhat.com> - 5.0.3-4
- Add patch for Python 3.13.0a3+ compatibility

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 09 2023 Lumír Balhar <lbalhar@redhat.com> - 5.0.3-1
- Update to 5.0.3 (rhbz#2156205)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.0.1-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.1-2
- Rebuilt for Python 3.11

* Fri Feb 25 2022 Fabian Affolter <mail@fabian-affolter.ch> - 3.0.1-1
- Update to latest upstream release 3.0.1 (closes rhbz#2017563)
- Remove doc subpackage (missing dependency)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun  9 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.1-3
- Add patches for failing tests (#1908278)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 02 2020 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.1-1
- Update to latest upstream release 2.0.1 (#1898712)

* Tue Nov 17 2020 Fabian Affolter <mail@fabian-affolter.ch> - 2.0.0-1
- Update to latest upstream release 2.0.0 (#1898712)

* Thu Aug 06 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.4.0-1
- Update to latest upstream release 1.4.0 (#1861675)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Fabian Affolter <mail@fabian-affolter.ch> -  1.3.0-3
- Add python3-setuptools as BR

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-2
- Rebuilt for Python 3.9

* Sat Mar 28 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.3.0-1
- Update to latest upstream release 1.3.0 (#1818465)

* Wed Mar 18 2020 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.2-1
- Update to latest upstream release 1.2.2

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.0-2
- Enable tests
- Add documentation

* Sat Jun 08 2019 Fabian Affolter <mail@fabian-affolter.ch> - 1.2.0-1
- Initial package for Fedora
