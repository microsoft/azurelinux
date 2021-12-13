Vendor:         Microsoft Corporation
Distribution:   Mariner
# Macros for py2/py3 compatibility
%global pyver %{python3_pkgversion}
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
%global pypi_name oslotest
# Remove after train bootstrapping is completed
%global repo_bootstrap 1
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%if 0%{?repo_bootstrap} == 0
%global with_doc 1
%else
%global with_doc 0
%endif

%global common_desc OpenStack test framework and test fixtures.

Name:           python-%{pypi_name}
Version:        3.8.1
Release:        4%{?dist}
Summary:        OpenStack test framework

License:        ASL 2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  git

%description
%{common_desc}

%package -n python%{pyver}-%{pypi_name}
Summary:        OpenStack test framework
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools


# test requires
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-mox3
BuildRequires:  python%{pyver}-debtcollector
BuildRequires:  python%{pyver}-stestr
%if 0%{?repo_bootstrap} == 0
BuildRequires:  python%{pyver}-os-client-config
BuildRequires:  python%{pyver}-oslo-config
%endif

Requires: python%{pyver}-debtcollector >= 1.2.0
Requires: python%{pyver}-fixtures
# os-client-config is a dependency but it's circular dependency making it
# imposible to bootstrap the repo.
%if 0%{?repo_bootstrap} == 0
Requires: python%{pyver}-os-client-config
%endif
Requires: python%{pyver}-six
Requires: python%{pyver}-subunit
Requires: python%{pyver}-testtools
Requires: python%{pyver}-mock
Requires: python%{pyver}-mox3 >= 0.20.0
Requires: python%{pyver}-stestr


%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for the OpenStack test framework

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

%description -n python-%{pypi_name}-doc
%{common_desc} Documentation
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# let RPM handle deps
rm -rf {test-,}requirements.txt

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
%{_bindir}/oslo_run_cross_tests
%{_bindir}/oslo_run_pre_release_tests
%{_bindir}/oslo_debug_helper
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%doc README.rst
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.8.1-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 3.8.1-2
- Update to upstream version 3.8.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 3.7.1-1
- Update to 3.7.1

