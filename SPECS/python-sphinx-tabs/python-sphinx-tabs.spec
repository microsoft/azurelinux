# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name sphinx-tabs
%global python_module_name sphinx_tabs

Name:           python-sphinx-tabs
Version:        3.4.7
Release:        6%{?dist}
Summary:        Tabbed views for Sphinx
# SPDX
License:        MIT
URL:            https://github.com/executablebooks/sphinx-tabs
Source0:        https://github.com/executablebooks/%{pypi_name}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz

# Open PR for Python Sphinx 8.1 issues with tests
# https://bugzilla.redhat.com/show_bug.cgi?id=2330154
Patch0:         https://patch-diff.githubusercontent.com/raw/executablebooks/sphinx-tabs/pull/200.patch
BuildArch:      noarch


%global _description %{expand:
Create tabbed content in Sphinx documentation when building HTML.}

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
# Needed for testing
BuildRequires:  python3dist(beautifulsoup4)
BuildRequires:  python3dist(pygments)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-regressions)
BuildRequires:  python3dist(sphinx)

%generate_buildrequires
%pyproject_buildrequires


%description %{_description}


%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name} %{_description}


%package -n python3-%{pypi_name}-doc
Summary:        HTML documentation for %{pypi_name}
Requires:       python3-%{pypi_name}

%description -n python3-%{pypi_name}-doc
%{summary}.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# The official package doesn't support docutils 0.19 yet
# It's OK to relax the requirement, the docs are rendered without visual issues
# https://github.com/executablebooks/sphinx-tabs/issues/171
sed -i "s/docutils~=0.18.0/docutils<0.21.0/" setup.py

%build
%pyproject_wheel

PYTHONPATH=$(pwd) sphinx-build -b html docs html_docs


%install
%pyproject_install
%pyproject_save_files %{python_module_name}


%check
# rinohtype extension to Sphinx is not yet packaged
%pytest -k 'not test_rinohtype_pdf'

%files -n  python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc CHANGELOG.md README.md

%files -n python3-%{pypi_name}-doc
%doc html_docs/*


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.4.7-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.4.7-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.4.7-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 15 2024 Richard Shaw <hobbes1069@gmail.com> - 3.4.7-1
- Update to 3.4.7.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 3.4.4-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 30 2023 Richard Shaw <hobbes1069@gmail.com> - 3.4.4-1
- Update to 3.4.4.

* Wed Aug 16 2023 Karolina Surma <ksurma@redhat.com> - 3.4.1-8
- Make tests pass with Sphinx 7.1+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Karolina Surma <ksurma@redhat.com> - 3.4.1-6
- Allow to install with python-docutils 0.20+

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 3.4.1-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 10 2022 Karolina Surma <ksurma@redhat.com> - 3.4.1-3
- Allow to install with python-docutils 0.18+

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jul 11 2022 Karolina Surma <ksurma@redhat.com> - 3.4.1-1
- Update to latest usptream version

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 3.1.0-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 02 2021 Richard Shaw <hobbes1069@gmail.com> - 3.1.0-5
- Add patch for docutils >= 0.17.

* Fri Aug 20 2021 Miro Hrončok <mhroncok@redhat.com> - 3.1.0-4
- Fix tests for Pygments 2.10

* Thu Aug 05 2021 Karolina Surma <ksurma@redhat.com> - 3.1.0-3
- Enable tests in %%check
- Fix the test using Sphinx 4+ features

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Karolina Surma <ksurma@redhat.com> - 3.1.0-1
- Update to 3.1.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.0-3
- Rebuilt for Python 3.10

* Sun Feb 07 2021 Richard Shaw <hobbes1069@gmail.com> - 2.0.0-2
- Make sure doc subpackage requires main package.
- Add __pycache__ dir to %%files temporarily, see:
  https://bugzilla.redhat.com/show_bug.cgi?id=1925963

* Fri Feb 05 2021 Richard Shaw <hobbes1069@gmail.com> - 2.0.0-1
- Update to latest release and correct spec per reviewer comments.

* Wed Dec  9 2020 Richard Shaw <hobbes1069@gmail.com> 1.3.0-1
- Initial Packaging
