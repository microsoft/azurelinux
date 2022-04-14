Vendor:         Microsoft Corporation
Distribution:   Mariner
# Macros for py2/py3 compatibility
%global pyver %{python3_pkgversion}
%global pyver_bin python%{pyver}
%global pyver_sitelib %{expand:%{python%{pyver}_sitelib}}
%global pyver_install %{expand:%{py%{pyver}_install}}
%global pyver_build %{expand:%{py%{pyver}_build}}
# End of macros for py2/py3 compatibility
# Created by pyp2rpm-1.1.1
%global pypi_name mox3

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
Mox3 is a mock object framework for Python 3 and 2.7. \
Mox3 is an unofficial port of the Google mox framework to Python 3. It was \
meant to be as compatible with mox as possible, but small enhancements have \
been made.

Name:           python-%{pypi_name}
Version:        0.28.0
Release:        4%{?dist}
Summary:        Mock object framework for Python

License:        ASL 2.0
URL:            http://git.openstack.org/cgit/openstack/mox3
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz#/python-%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch


%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        Mock object framework for Python
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

Requires:  python%{pyver}-pbr
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-six >= 1.9.0
Requires:  python%{pyver}-testtools

BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr

# test requires
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-testtools
BuildRequires:  python%{pyver}-six >= 1.9.0

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

%prep
%autosetup -p1 -n %{pypi_name}-%{upstream_version}

# let RPM handle deps
rm -rf *requirements.txt

%build
%{pyver_bin} setup.py build

%install
%{pyver_bin} setup.py install --skip-build --root %{buildroot}

%check
PYTHON=python%{pyver} stestr-%{pyver} run

%files -n python%{pyver}-%{pypi_name}
%doc README.rst
%license COPYING.txt
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}*.egg-info

%changelog
* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 0.28.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora version check for python version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.28.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 0.28.0-2
- Update to upstream version 0.28.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.27.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.27.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 0.27.0-1
- Update to 0.27.0

