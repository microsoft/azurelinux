# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname fields

Name:           python-%{srcname}
Version:        5.0.0
Release:        27%{?dist}
Summary:        Container class boilerplate killer

License:        BSD-2-Clause
URL:            https://github.com/ionelmc/%{name}
Source0:        https://github.com/ionelmc/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz

# Compatibility with python-sphinx >= 1.3, already applied upstream
Patch0:         %{name}-5.0.0-sphinx-1.3.patch

BuildArch:      noarch

%description
Container class boilerplate killer.

Features:
- Human-readable __repr__
- Complete set of comparison methods
- Keyword and positional argument support. Works like a normal class - you can
  override just about anything in the subclass (eg: a custom __init__). In
  contrast, hynek/characteristic forces different call schematics and calls
  your __init__ with different arguments.

%package doc
Summary:        Documentation for '%{name}'
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx-theme-py3doc-enhanced

%description doc
HTML API documentation for the '%{srcname}' Python module.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pytest-benchmark
Recommends:     %{name}-doc = %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}
Container class boilerplate killer.

Features:
- Human-readable __repr__
- Complete set of comparison methods
- Keyword and positional argument support. Works like a normal class - you can
  override just about anything in the subclass (eg: a custom __init__). In
  contrast, hynek/characteristic forces different call schematics and calls
  your __init__ with different arguments.

%prep
%autosetup -p1
sed -i 's/\[pytest\]/\[tool:pytest\]/' setup.cfg

%build
%py3_build
PYTHONPATH=$PWD/src sphinx-build -b html docs docs/_build/html
rm -rf docs/_build/html/.buildinfo docs/_build/html/.doctrees

%install
%py3_install

%check
# Perf tests require unmaintained 'characteristic' module
PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} \
  --ignore=tests/test_perf.py \
  tests

%files doc
%license LICENSE
%doc docs/_build/html

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc AUTHORS.rst CHANGELOG.rst README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.0.0-27
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.0.0-26
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.0.0-24
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 13 2024 Scott K Logan <logans@cottsay.net> - 5.0.0-22
- Update SPDX license identifier
- Drop spec file support for EPEL 7
- Drop unused rpmlintrc filter

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 5.0.0-21
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.0.0-19
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 5.0.0-15
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 5.0.0-12
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 5.0.0-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 5.0.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 14 2019 Scott K Logan <logans@cottsay.net> - 5.0.0-1
- Initial package
