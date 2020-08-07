%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-enum34
Version:        1.1.6
Release:        4%{?dist}
Summary:        Robust enumerated type support in Python
License:        BSD
Group:          Development/Libraries
Url:            https://bitbucket.org/stoneleaf/enum34
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://pypi.python.org/packages/bf/3e/31d502c25302814a7c2f1d3959d2a3b3f78e509002ba91aea64993936876/enum34-%{version}.tar.gz
%define sha1    enum34=014ef5878333ff91099893d615192c8cd0b1525a

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
An enumeration is a set of symbolic names (members) bound to unique, constant values. Within an enumeration, the members can be compared by identity, and the enumeration itself can be iterated over.

%prep
%setup -n enum34-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
PATH=%{buildroot}%{_bindir}:${PATH} \
PYTHONPATH=%{buildroot}%{python_sitelib} \
 python2 enum/test.py

%files
%defattr(-,root,root,-)
%license enum/LICENSE
%{python2_sitelib}/*

%changelog
* Sat May 09 00:20:57 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.1.6-4
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.1.6-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.6-2
-   Changed python to python2
*   Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.1.6-1
-   Initial packaging for Photon
