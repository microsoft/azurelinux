# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%{!?_licensedir:%global license %%doc}
%global pypi_name os-client-config
%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
The os-client-config is a library for collecting client configuration for \
using an OpenStack cloud in a consistent and comprehensive manner. It \
will find cloud config for as few as 1 cloud and as many as you want to \
put in a config file. It will read environment variables and config files, \
and it also contains some vendor specific default values so that you don't \
have to know extra info to use OpenStack \
 \
* If you have a config file, you will get the clouds listed in it \
* If you have environment variables, you will get a cloud named `envvars` \
* If you have neither, you will get a cloud named `defaults` with base defaults

Name:           python-%{pypi_name}
Version:        2.1.0
Release:        19%{?dist}
Summary:        OpenStack Client Configuration Library
# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:        Apache-2.0
URL:            https://github.com/openstack/%{pypi_name}
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  git

%description
%{common_desc}


%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
# Testing requirements
BuildRequires:  python3-fixtures
BuildRequires:  python3-stestr
BuildRequires:  python3-glanceclient >= 0.18.0
BuildRequires:  python3-openstacksdk
BuildRequires:  python3-oslotest >= 1.10.0
BuildRequires:  python3-jsonschema >= 2.6.0

Requires:       python3-openstacksdk >= 0.13.0


%description -n python3-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package  -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack os-client-config library

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-reno

%description -n python-%{pypi_name}-doc
Documentation for the os-client-config library.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Let RPM handle the dependencies
rm -f test-requirements.txt requirements.txt

%build
%{py3_build}

%if 0%{?with_doc}
# generate html doc
sphinx-build-3 -b html doc/source/ doc/build/html
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv
%endif

%install
%{py3_install}

%check
# NOTE(jpena): we are disabling Python2 unit tests when building the Python 3 package.
# The reason is that unit tests require glanceclient, and glanceclient is python3-only
# when building with Python 3. We could revert that, but it is a rabbit hole we do not
# want to enter
export OS_TEST_PATH='./os_client_config/tests'
export PATH=$PATH:$RPM_BUILD_ROOT/usr/bin
export PYTHONPATH=$PWD

#rm -rf .stestr
#PYTHON=python3 stestr-3 --test-path $OS_TEST_PATH run

%files -n python3-%{pypi_name}
%doc ChangeLog CONTRIBUTING.rst PKG-INFO README.rst
%license LICENSE
%{python3_sitelib}/os_client_config
%{python3_sitelib}/*.egg-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1.0-19
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.1.0-18
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Alfredo Moralejo <amoralej@redhat.com> - 2.1.0-16
- Rebuilt for Fedora 43

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 2.1.0-14
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Python Maint <python-maint@redhat.com> - 2.1.0-12
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.1.0-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 2.1.0-1
- Update to upstream version 2.1.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.33.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.33.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Joel Capitao <jcapitao@redhat.com> 1.33.0-2
- Removed python2 subpackages in no el7 distros

* Tue Nov 05 2019 RDO <dev@lists.rdoproject.org> 1.33.0-1
- Update to 1.33.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.32.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.32.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.32.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 10 2019 Alfredo Moralejo <amoralej@redhat.com> 1.32.0-2
- Added stestr as BR

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 1.32.0-1
- Update to 1.32.0

