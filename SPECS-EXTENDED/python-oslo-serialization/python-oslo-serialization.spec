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
%global pypi_name oslo.serialization
%global pkg_name oslo-serialization
%global with_doc 1

%global common_desc \
An OpenStack library for representing objects in transmittable and \
storable formats.

Name:           python-%{pkg_name}
Version:        2.29.2
Release:        5%{?dist}
Summary:        OpenStack oslo.serialization library

License:        ASL 2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz#/python-%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n python%{pyver}-%{pkg_name}
Summary:        OpenStack oslo.serialization library
%{?python_provide:%python_provide python%{pyver}-%{pkg_name}}

BuildRequires:  git
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-pbr
# test requirements
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-oslo-i18n
BuildRequires:  python%{pyver}-stestr
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-msgpack >= 0.5.2
BuildRequires:  python%{pyver}-netaddr
BuildRequires:  python%{pyver}-simplejson
# Handle python2 exception
%if "%{pyver}" == "2"
BuildRequires:  python-ipaddress
%endif

Requires:       python%{pyver}-babel
Requires:       python%{pyver}-iso8601
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-six
Requires:       python%{pyver}-msgpack >= 0.5.2
Requires:       python%{pyver}-pytz
# Handle python2 exception
%if "%{pyver}" == "2"
Requires:       python-ipaddress
%endif

%description -n python%{pyver}-%{pkg_name}
%{common_desc}


%package -n python%{pyver}-%{pkg_name}-tests
Summary:   Tests for OpenStack Oslo serialization library
%{?python_provide:%python_provide python2-%{pkg_name}}

Requires:  python%{pyver}-%{pkg_name} = %{version}-%{release}
Requires:  python%{pyver}-hacking
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-oslo-i18n
Requires:  python%{pyver}-stestr
Requires:  python%{pyver}-netaddr
Requires:  python%{pyver}-simplejson

%description -n python%{pyver}-%{pkg_name}-tests
Tests for OpenStack Oslo serialization library

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo serialization library

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme

Requires:  python%{pyver}-%{pkg_name} = %{version}-%{release}

%description -n python-%{pkg_name}-doc
Documentation for the Oslo serialization library.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Let RPM handle the dependencies
rm -f requirements.txt

%build
%{pyver_build}

%if 0%{?with_doc}
# doc
sphinx-build-%{pyver} -W -b html doc/source doc/build/html
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
export OS_TEST_PATH="./oslo_serialization/tests"
PYTHON=python%{pyver} stestr-%{pyver} --test-path $OS_TEST_PATH run

%files -n python%{pyver}-%{pkg_name}
%doc README.rst
%license LICENSE
%{pyver_sitelib}/oslo_serialization
%{pyver_sitelib}/*.egg-info
%exclude %{pyver_sitelib}/oslo_serialization/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python%{pyver}-%{pkg_name}-tests
%{pyver_sitelib}/oslo_serialization/tests

%changelog
* Fri Dec 17 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.29.2-5
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.29.2-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.29.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 2.29.2-2
- Update to upstream version 2.29.2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.28.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.28.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 2.28.2-1
- Update to 2.28.2

