%global srcname fields
Summary:        Container class boilerplate killer
Name:           python-%{srcname}
Version:        5.0.0
Release:        10%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/ionelmc/python-fields
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
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinx-theme-py3doc-enhanced
BuildRequires:  python%{python3_pkgversion}-sphinxcontrib-websupport

%description doc
HTML API documentation for the '%{srcname}' Python module.

%package -n     python%{python3_pkgversion}-%{srcname}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-sphinxcontrib-websupport
BuildRequires:  python%{python3_pkgversion}-xml
%if %{with_check}
BuildRequires:  python3-pip
%endif

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
PYTHONPATH=$PWD/src sphinx-build%{python3_pkgversion} -b html docs docs/_build/html
rm -rf docs/_build/html/.buildinfo docs/_build/html/.doctrees

%install
%py3_install

%check
# Perf tests require unmaintained 'characteristic' module
pip3 install atomicwrites>=1.3.0 \
    attrs>=19.1.0 \
    more-itertools>=7.0.0 \
    pluggy>=0.11.0 \
    pytest>=5.4.0 \
    pytest-cov>=2.7.1 \
    pytest-benchmark
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    python%{python3_version} -m pytest -v --ignore=tests/test_perf.py tests

%files doc
%license LICENSE
%doc docs/_build/html

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc AUTHORS.rst
%doc CHANGELOG.rst
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/

%changelog
* Sun Feb 13 2022 Jon Slobodzian <joslobo@microsoft,.com> - 5.0.0-10
- Add missing build requires on python-devel

* Wed Jun 23 2021 Rachel Menge <rachelmenge@microsoft.com> - 5.0.0-9
- Update check section to use pytest module
- License verified

* Sun Oct 18 2020 Steve Laughman <steve.laughman@microsoft.com> - 5.0.0-8
- Initial CBL-Mariner import from Fedora 33 (license: MIT)

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
