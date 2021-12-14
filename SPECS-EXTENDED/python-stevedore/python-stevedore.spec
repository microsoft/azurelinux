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

%global common_desc Manage dynamic plugins for Python applications

Name:           python-stevedore
Version:        1.31.0
Release:        4%{?dist}
Summary:        Manage dynamic plugins for Python applications

Group:          Development/Languages
License:        ASL 2.0
URL:            https://github.com/openstack/stevedore
Source0:        https://tarballs.openstack.org/stevedore/stevedore-%{upstream_version}.tar.gz#/python-stevedore-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-six
BuildRequires:  python%{pyver}-testrepository
#BuildRequires:  python%{pyver}-discover
#BuildRequires:  python%{pyver}-oslotest

%description
%{common_desc}

%package -n python%{pyver}-stevedore
Summary:        Manage dynamic plugins for Python applications
Group:          Development/Libraries
%{?python_provide:%python_provide python%{pyver}-stevedore}

Requires:       python%{pyver}-six
Requires:       python%{pyver}-pbr

%description -n python%{pyver}-stevedore
%{common_desc}

%prep
%setup -q -n stevedore-%{upstream_version}

# let RPM handle deps
rm -f requirements.txt

%build
%{pyver_build}

%install
%{pyver_install}

%check
#TODO: reenable when commented test requirements above are available
#
#PYTHONPATH=. nosetests
#
#%if 0%{?with_python3}
#pushd %{py3dir}
#PYTHONPATH=. nosetests-%{python3_version}
#popd
#%endif

%files -n python%{pyver}-stevedore
%license LICENSE
%doc README.rst
%{pyver_sitelib}/stevedore
%{pyver_sitelib}/stevedore-*.egg-info

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.31.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 1.31.0-2
- Update to upstream version 1.31.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.30.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.30.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.30.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 1.30.1-1
- Update to 1.30.1

