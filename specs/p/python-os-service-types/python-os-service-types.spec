# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
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
Release: 25%{?dist}
Summary:        Python library for consuming OpenStack sevice-types-authority data

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
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
sphinx-build -b html doc/source doc/build/html
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
%{pyver_sitelib}/%{module_name}-%{upstream_version}-py%{python3_version}.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7.0-24
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7.0-23
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.7.0-21
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.7.0-19
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.7.0-17
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.7.0-13
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1.7.0-10
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7.0-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.0-4
- Rebuilt for Python 3.9

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

