# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name pytest-django

Name:           python-%{pypi_name}
Version:        4.9.0
Release: 6%{?dist}
Summary:        A Django plugin for pytest

License:        LicenseRef-Callaway-BSD
URL:            https://pytest-django.readthedocs.io/
Source:         %{pypi_source pytest_django}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
pytest-django allows you to test your Django project/applications with the
pytest testing tool.}

%description %_description


%package -n     python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel

%description -n python3-%{pypi_name}
pytest-django allows you to test your Django project/applications with the
pytest testing tool.

%package -n python-%{pypi_name}-doc
Summary:        Documentation for %{name}

BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme

%description -n python-%{pypi_name}-doc
Documentation for %{name}.

%prep
%autosetup -n pytest_django-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel
PYTHONPATH=${PWD} sphinx-build-3 docs html
rm -rf html/.{doctrees,buildinfo}

%install
%pyproject_install
%pyproject_save_files -l pytest_django

%check
%tox

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc README.rst

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.9.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.9.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Sep 28 2024 Fabian Affolter <mail@fabian-affolter.ch> - 4.9.0-1
- Update to latest upstream release (closes rhbz#2309214)

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 4.8.0-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 4.8.0-2
- Rebuilt for Python 3.13

* Thu Feb 29 2024 Michel Lind <salimma@fedoraproject.org> - 4.8.0-1
- Update to 4.8.0 (rhbz#2261956)
- Modernize spec file

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 4.1.0-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 4.1.0-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.1.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 13 2020 Joel Capitao <jcapitao@redhat.com> - 4.1.0-1
- Update to 4.1.0

* Thu Aug 13 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.8.0-6
- Remove pathlib2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.0-4
- Rebuilt for Python 3.9

* Sat Mar 21 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.8.0-3
- Disable tests

* Sat Feb 01 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.8.0-2
- Bump release

* Fri Jan 31 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 3.8.0-1
- Enable tests
- Update to 3.8.0

* Tue Jan 07 2020 Fabian Affolter <mail@fabian-affolter.ch> - 3.7.0-2
- Use var for source URL
- Better use of wildcards (rhbz#1786920)

* Sat Dec 28 2019 Fabian Affolter <mail@fabian-affolter.ch> - 3.7.0-1
- Initial package for Fedora
