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

%global sname novaclient
%global with_doc 1

%global common_desc \
This is a client for the OpenStack Nova API. There's a Python API (the \
novaclient module), and a command-line script (nova). Each implements 100% of \
the OpenStack Nova API.

Name:             python-novaclient
Version:          15.1.0
Release:          5%{?dist}
Summary:          Python API and CLI for OpenStack Nova
License:          ASL 2.0
URL:              https://launchpad.net/%{name}
Source0:          https://pypi.io/packages/source/p/%{name}/%{name}-%{version}.tar.gz
BuildArch:        noarch

BuildRequires:  git

%description
%{common_desc}

%package -n python%{pyver}-%{sname}
Summary:          Python API and CLI for OpenStack Nova
%{?python_provide:%python_provide python%{pyver}-novaclient}
%if "%{pyver}" == "3"
Obsoletes: python2-%{sname} < %{version}-%{release}
%endif

BuildRequires:    python%{pyver}-devel
BuildRequires:    python%{pyver}-pbr
BuildRequires:    python%{pyver}-setuptools

Requires:         python%{pyver}-babel >= 2.3.4
Requires:         python%{pyver}-iso8601 >= 0.1.11
Requires:         python%{pyver}-keystoneauth1 >= 3.5.0
Requires:         python%{pyver}-oslo-i18n >= 3.15.3
Requires:         python%{pyver}-oslo-serialization >= 2.18.0
Requires:         python%{pyver}-oslo-utils >= 3.33.0
Requires:         python%{pyver}-pbr >= 2.0.0
Requires:         python%{pyver}-prettytable >= 0.7.2
Requires:         python%{pyver}-six >= 1.10.0
# Handle python2 exception
%if "%{pyver}" == "2"
Requires:         python-simplejson >= 3.5.1
%else
Requires:         python%{pyver}-simplejson >= 3.5.1
%endif

%description -n python%{pyver}-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Nova API Client

BuildRequires:    python%{pyver}-sphinx
BuildRequires:    python%{pyver}-sphinxcontrib-apidoc
BuildRequires:    python%{pyver}-openstackdocstheme
BuildRequires:    python%{pyver}-oslo-utils
BuildRequires:    python%{pyver}-keystoneauth1
BuildRequires:    python%{pyver}-oslo-serialization
BuildRequires:    python%{pyver}-prettytable

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%prep
%autosetup -n %{name}-%{upstream_version} -S git

# Let RPM handle the requirements
rm -rf *requirements.txt

%build
%{pyver_build}

%install
%{pyver_install}
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s nova %{buildroot}%{_bindir}/nova-%{pyver}

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/nova.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/nova

# Delete tests
rm -fr %{buildroot}%{pyver_sitelib}/novaclient/tests

%if 0%{?with_doc}
sphinx-build-%{pyver} -b html doc/source doc/build/html
sphinx-build-%{pyver} -b man doc/source doc/build/man

install -p -D -m 644 doc/build/man/nova.1 %{buildroot}%{_mandir}/man1/nova.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo doc/build/html/.htaccess
%endif

%files -n python%{pyver}-%{sname}
%license LICENSE
%doc README.rst
%{pyver_sitelib}/%{sname}
%{pyver_sitelib}/*.egg-info
%{_sysconfdir}/bash_completion.d
%if 0%{?with_doc}
%{_mandir}/man1/nova.1.gz
%endif
%{_bindir}/nova
%{_bindir}/nova-%{pyver}

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Dec 17 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 15.1.0-5
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 15.1.0-4
- Remove epoch

* Mon Feb 01 2021 Joe Schmitt <joschmit@microsoft.com> - 1:15.1.0-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove Fedora version check for python version

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:15.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Alfredo Moralejo <amoralej@redhat.com> 1:15.1.0-1
- Update to upstream version 15.1.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:13.0.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:13.0.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:13.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 RDO <dev@lists.rdoproject.org> 1:13.0.0-1
- Update to 13.0.0

