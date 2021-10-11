Summary:        A tool to check your Python code
Name:           python-pycodestyle
Version:        2.5.0
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.org/project/pycodestyle/
#Source0:       https://files.pythonhosted.org/packages/1c/d1/41294da5915f4cae7f4b388cea6c2cd0d6cd53039788635f6875dfe8c72f/pycodestyle-2.5.0.tar.gz
Source0:        %{name}-%{version}.tar.gz
BuildArch:      noarch

%description
pycodestyle is a tool to check your Python code against some of the style conventions in PEP 8.

%package -n     python3-pycodestyle
Summary:        python-pycodestyle
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-pycodestyle

Python 3 version.

%prep
%autosetup -n pycodestyle-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-pycodestyle
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*
%{_bindir}/pycodestyle

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 2.5.0-5
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.5.0-4
- Added %%license line automatically

* Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> - 2.5.0-3
- Add #Source0. License verified.

* Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> - 2.5.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Tue Jun 04 2019 Ankit Jain <ankitja@vmware.com> - 2.5.0-1
- Initial packaging for Photon
