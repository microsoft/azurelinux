Summary:        The fastest markdown parser in pure Python.
Name:           python-mistune
Version:        0.8.3
Release:        5%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://pypi.python.org/pypi/mistune/
Source0:        https://files.pythonhosted.org/packages/source/m/mistune/mistune-%{version}.tar.gz
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
%endif

%description
The fastest markdown parser in pure Python with renderer features, inspired by marked.

%package -n     python3-mistune
Summary:        The fastest markdown parser in pure Python.
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3

%description -n python3-mistune
The fastest markdown parser in pure Python with renderer features, inspired by marked.

%prep
%autosetup -n mistune-%{version}


%build
%py3_build

%install
%py3_install

%check
%python3 setup.py test

%files -n python3-mistune
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Wed Feb 09 2022 Muhammad Falak <mwani@microsoft.com> - 0.8.3-5
- Add an explict BR on 'pip' to enable ptest

* Wed Oct 20 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.8.3-4
- Add license to python3 package
- Remove python2 package
- Lint spec
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.8.3-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 0.8.3-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 0.8.3-1
- Update to version 0.8.3

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.4-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 0.7.4-1
- Initial packaging for Photon
