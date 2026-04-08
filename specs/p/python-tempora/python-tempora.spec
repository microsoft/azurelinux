# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Created by pyp2rpm-3.3.2
%global pypi_name tempora
%bcond_with docs

Name:           python-%{pypi_name}
Version:        5.7.0
Release:        6%{?dist}
Summary:        Objects and routines pertaining to date and time (tempora)

License:        MIT
URL:            https://github.com/jaraco/tempora
Source0:        https://files.pythonhosted.org/packages/source/t/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
 
%description
Objects and routines pertaining to date and time (tempora).

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  python3-devel
BuildRequires:  python3dist(build)
BuildRequires:  python3dist(freezegun)
BuildRequires:  python3dist(jaraco-functools) >= 1.20
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(pytz)
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(setuptools-scm) >= 1.15
BuildRequires:  python3dist(six)
BuildRequires:  python3dist(wheel)
# testing Reqs
BuildConflicts: python3dist(pytest) = 3.7.3
BuildRequires:  python3dist(pytest) >= 3.4
BuildRequires:  python3-more-itertools

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
Objects and routines pertaining to date and time (tempora).

%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        tempora documentation

BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(jaraco-packaging) >= 3.2
BuildRequires:  python3dist(rst-linker) >= 1.9


%description -n python-%{pypi_name}-doc
Documentation for tempora
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove tests that requires pytest-freezer.
# it is not packaged in Fedora
sed -i 214,226d tempora/__init__.py
sed -i 25,30d tempora/utc.py

%build
LANG=C.utf-8 %{__python3} -m build --no-isolation
%if %{with docs}
# generate html docs 
PYTHONPATH=${PWD} sphinx-build-3 docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py3_install_wheel %{pypi_name}-%{version}-py3-none-any.whl

%check
LANG=C.utf-8 %{__python3} -m pytest --ignore=build


%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/calc-prorate
%{python3_sitelib}/%{pypi_name}*

%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.7.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.7.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.7.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Aug 01 2024 Dan Radez <dradez@redhat.com> - 5.7.0-1
- update to 5.7.0 rhbz#2292920

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.5.1-2
- Rebuilt for Python 3.13

* Mon Feb 19 2024 Dan Radez <dradez@redhat.com> - 5.5.1-1
- update to 5.5.1 rhbz#2264858

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 27 2023 Python Maint <python-maint@redhat.com> - 5.5.0-2
- Rebuilt for Python 3.12

* Tue Jun 27 2023 Dan Radez <dradez@redhat.com> - 5.5.0-1
- update to 5.5.0 rhbz#2217851

* Mon Jun 26 2023 Python Maint <python-maint@redhat.com> - 5.3.0-2
- Rebuilt for Python 3.12

* Mon Jun 19 2023 Dan Radez <dradez@redhat.com> - 5.3.0-1
- update to 5.3.0 rhbz#2213983

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 5.2.2-2
- Rebuilt for Python 3.12

* Tue Apr 11 2023 Dan Radez <dradez@redhat.com> - 5.2.2-1
- update to 5.2.2 rhbz#2185610

* Thu Jan 19 2023 Dan Radez <dradez@redhat.com> - 5.2.1-1
- update to 5.2.1 (rhbz#2157607)

* Wed Nov 23 2022 Dan Radez <dradez@redhat.com> - 5.1.0-1
- update to 5.1.0 (rhbz#2144174)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 Dan Radez <dradez@redhat.com> - 5.0.2-1
- Upstream update to 5.0.2

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 5.0.1-2
- Rebuilt for Python 3.11

* Mon Feb 14 2022 Dan Radez <dradez@redhat.com> - 5.0.1-1
- Upstream update to 5.0.1

* Thu Feb 10 2022 Dan Radez <dradez@redhat.com> - 5.0.0-3
- adding provides

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 11 2022 Dan Radez <dradez@redhat.com> - 5.0.0
- Upstream update to 5.0.0

* Mon Dec 06 2021 Dan Radez <dradez@redhat.com> - 4.1.2-1
- Upstream update to 4.1.2

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Dan Radez <dradez@redhat.com> - 4.1.0-1
- Upstream update to 4.1.0

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.14.1-10
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.14.1-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 30 2019 Dan Radez <dradez@redhat.com> - 1.14.1-5
- Rebuilding to fix deps

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.14.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 22 2019 Dan Radez <dradez@redhat.com> - 1.14.1-2
- fix setup.py reqs so the RPM reqs get generated properly

* Tue Apr 02 2019 Dan Radez <dradez@redhat.com> - 1.14.1-1
- Initial package.
