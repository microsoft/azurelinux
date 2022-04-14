%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global pypi_name vine

# Enable tests by default
%bcond_without tests

# docs depend on package sphinx_celery
# https://github.com/celery/sphinx_celery
%bcond_with docs

Summary:        Promises, promises, promises
Name:           python-%{pypi_name}
Version:        5.0.0
Release:        3%{?dist}
License:        BSD
URL:            http://github.com/celery/vine
#Source0:       https://files.pythonhosted.org/packages/source/v/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/source/v/%{pypi_name}/%{name}-%{version}.tar.gz
BuildArch:      noarch

%if %{with docs}
BuildRequires:  python3-sphinx
%endif

%description
%{summary}

%package -n     python3-%{pypi_name}
Summary:        Promises, promises, promises
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-cov
BuildRequires:  python3-case
BuildRequires:  python3-mock
%endif

%description -n python3-%{pypi_name}
%{summary}

%if %{with docs}
%package -n python-%{pypi_name}-doc
Summary:        vine documentation
%description -n python-%{pypi_name}-doc
Documentation for vine
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py3_build

# docs depend on sphinx-celery
%if %{with docs}
# generate html docs

sphinx-build docs html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py3_install

%if %{with tests}
%check
py.test-3 -xv --cov=vine --cov-report=xml --no-cov-on-fail
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%doc docs/templates/readme.txt README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%if %{with docs}
%files -n python-%{pypi_name}-doc
%doc html
%endif

%changelog
* Mon Dec 07 2020 Steve Laughman <steve.laughman@microsoft.com> - 5.0.0-3
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Sep 30 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.0.0-2
- Enable tests
* Tue Sep 29 2020 Frantisek Zatloukal <fzatlouk@redhat.com> - 5.0.0-1
- python-vine 5.0.0
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-6
- Rebuilt for Python 3.9
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)
* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-3
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Tue Jul 02 2019 Nils Philippsen <nils@redhat.com> - 1.3.0-1
- Update to 1.3.0
* Fri Jun 28 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-3
- Subpackage python2-vine has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Sat Jan 26 2019 Neal Gompa <ngompa13@gmail.com> - 1.2.0-1
- Update to 1.2.0
- Switch to using bconds for controlling build behaviors
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Mon Jul 09 2018 Matthias Runge <mrunge@redhat.com> - 1.1.4-1
- update to 1.1.4 (rhbz#1471577)
* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.3-6
- Rebuilt for Python 3.7
* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.3-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
* Tue Dec 27 2016 Matthias Runge <mrunge@redhat.com> - 1.1.3-1
- Initial package. (rhbz#1408869)