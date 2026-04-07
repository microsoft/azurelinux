# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name cbor2

Name:           python-%{pypi_name}
Version:        5.6.5
Release:        6%{?dist}
Summary:        Python CBOR (de)serializer with extensive tag support

License:        MIT
URL:            https://github.com/agronholm/cbor2
Source0:        %{pypi_source}

BuildRequires:  gcc
BuildRequires:  python3-devel

%description
This library provides encoding and decoding for the Concise Binary Object
Representation (CBOR) (RFC 7049) serialization format.

%package -n     python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
This library provides encoding and decoding for the Concise Binary Object
Representation (CBOR) (RFC 7049) serialization format.

%package -n python-%{pypi_name}-doc
Summary:        cbor2 documentation
BuildArch:      noarch
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildRequires:  python3dist(sphinx-autodoc-typehints)

%description -n python-%{pypi_name}-doc
Documentation for cbor2.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -x test

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}
PYTHONPATH=${PWD} sphinx-build-3 docs html
rm -rf html/.{doctrees,buildinfo}

%check
%pytest -v tests

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst
%{python3_sitearch}/_%{pypi_name}%{python3_ext_suffix}
%{_bindir}/%{pypi_name}

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE.txt

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.6.5-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.6.5-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.6.5-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 10 2024 Fabian Affolter <mail@fabian-affolter.ch> - 5.6.5-1
- Update to latest upstream release (closes rhbz#2274416)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 5.6.2-2
- Rebuilt for Python 3.13

* Mon Apr 08 2024 Fabian Affolter <mail@fabian-affolter.ch> - 5.6.2-1
- Update to latest upstream release (closes rhbz#2261550, closes rhbz#2245361)
- Fixes CVE-2024-26134 (closes rhbz#2265036, closes rhbz#bug 2265035)

* Sat Feb 03 2024 Fabian Affolter <mail@fabian-affolter.ch> - 5.6.1-1
- Update to latest upstream release 5.6.1 (closes rhbz#2245361)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Aug 30 2023 Carl George <carlwgeorge@fedoraproject.org> - 5.1.2-12
- Convert to pyproject macros
- Validated license as SPDX identifier

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 5.1.2-10
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.1.2-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 5.1.2-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Fabian Affolter <mail@fabian-affolter.ch> - 5.1.2-2
- Make doc subpackage noarch (rhbz#1877691)

* Thu Sep 10 2020 Fabian Affolter <mail@fabian-affolter.ch> - 5.1.2-1
- Initial package
