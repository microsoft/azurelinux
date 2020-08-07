%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Name:           python-futures
Version:        3.2.0
Release:        4%{?dist}
Summary:        Backport of the concurrent.futures package to Python 2.6 and 2.7
License:        PSF
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/futures
Source0:        https://files.pythonhosted.org/packages/1f/9e/7b2ff7e965fc654592269f2906ade1c7d705f1bf25b7d469fa153f7d19eb/futures-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner
BuildRequires:  pkg-config
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch
%description
Backport of the concurrent.futures package to Python 2.6 and 2.7

%prep
%setup -n futures-%{version}

%build
python2 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install py

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*

%changelog
* Sat May 09 00:21:20 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.2.0-4
- Added %%license line automatically

*   Mon Apr 27 2020 Nick Samson <nisamson@microsoft.com> 3.2.0-3
-   Updated Source0, License verified. Removed sha line.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.2.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.2.0-1
-   Update to version 3.2.0
*   Thu Apr 06 2017 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 3.1.1-1
-   Initial version of python-fuse package for Photon.
