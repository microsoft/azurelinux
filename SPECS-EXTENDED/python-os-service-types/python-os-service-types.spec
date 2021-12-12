Vendor:         Microsoft Corporation
Distribution:   Mariner
# Macros for py2/py3 compatibility
%global pyver %{python3_pkgversion}
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name os-service-types
%global module_name os_service_types

# Needed for train bootstrap
%global repo_bootstrap 1

%global common_desc \
OsServiceTypes is a Python library for consuming OpenStack sevice-types-authority data \
The OpenStack Service Types Authority contains information about official \
OpenStack services and their historical service-type aliases. \
The data is in JSON and the latest data should always be used. This simple \
library exists to allow for easy consumption of the data, along with a built-in \
version of the data to use in case network access is for some reason not possible \
and local caching of the fetched data.

%global with_doc 1

Name:           python-%{pypi_name}
Version:        1.7.0
Release:        4%{?dist}
Summary:        Python library for consuming OpenStack sevice-types-authority data

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz#/python-%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-testscenarios
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-requests-mock

%if 0%{?repo_bootstrap} == 0
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-oslotest
%endif

Requires:       python%{pyver}-pbr >= 2.0.0
%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        %{pypi_name} documentation

BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-sphinx

%description -n python-%{pypi_name}-doc
%{common_desc}


Documentation for %{pypi_name}
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -rf {test-,}requirements.txt
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
%{pyver_bin} setup.py build_sphinx -b html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
%if 0%{?repo_bootstrap} == 0
%{pyver_bin} setup.py test
%endif

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%doc README.rst doc/source/readme.rst
%{pyver_sitelib}/%{module_name}
%{pyver_sitelib}/%{module_name}-%{upstream_version}-py?.?.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 1.7.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora version check for python version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 1.7.0-2
- Update to upstream version 1.7.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 Alfredo Morlejo <amoralej@redhat.com> 1.6.0-2
- Disable bootstrap mode.

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 1.6.0-1
- Update to 1.6.0

