%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Incremental is a small library that versions your Python projects.
Name:           python-incremental
Version:        17.5.0
Release:        4%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/incremental
Source0:        https://files.pythonhosted.org/packages/source/i/incremental/incremental-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
Incremental is a small library that versions your Python projects.

%package -n     python3-incremental
Summary:        python-incremental
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs
%description -n python3-incremental
Python 3 version.

%prep
%setup -q -n incremental-%{version}

%build
python2 setup.py build
python3 setup.py build


%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
python3 setup.py test

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-incremental
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 17.5.0-4
- Added %%license line automatically

*   Fri Apr 24 2020 Andrew Phelps <anphel@microsoft.com> 17.5.0-3
-   Updated Source0. Remove sha1 definition. Verified license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 17.5.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.5.0-1
-   Update to version 17.5.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.10.1-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 06 2017 Xiaolin Li <xiaolinl@vmware.com> 16.10.1-1
-   Initial packaging for Photon.
