%define pypi_name zope.event
Summary:        Very basic event publishing system
Name:           python-zope-event
Version:        4.5.0
Release:        1%{?dist}
License:        ZPLv2.1
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          Development/Languages/Python
URL:            https://github.com/zopefoundation/zope.event
Source0:        https://pypi.python.org/packages/source/z/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

%description
Very basic event publishing system for Python

%package -n     python3-zope-event
Summary:        python3-zope-event
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description -n python3-zope-event
This package provides a simple event system on which application-specific event systems can be built. For example, a type-based event dispatching system that builds on zope.interface can be found in zope.component. A simpler system is distributed with this package and is described in Class-based event handlers.
This package is intended to be independently reusable in any Python project. It is maintained by the Zope Toolkit project.
For detailed documentation, please see http://docs.zope.org/zope.event

%global debug_package %{nil}

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
pip3 install 'tox>=3.18,<4.0.0' zope.testrunner tox-current-env
%tox

%files -n python3-zope-event
%defattr(-,root,root,-)
%license LICENSE.txt
%{python3_sitelib}/*

%changelog
* Tue Jun 02 2024 Nick Samson <nisamson@microsoft.com> - 4.5.0-1
- zope.event package added for Azure Linux 3.0
