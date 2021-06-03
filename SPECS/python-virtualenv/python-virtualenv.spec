%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-virtualenv
Version:        16.0.0
Release:        5%{?dist}
Summary:        Virtual Python Environment builder
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/virtualenv
Source0:        https://files.pythonhosted.org/packages/33/bc/fa0b5347139cd9564f0d44ebd2b147ac97c36b2403943dbee8a25fd74012/virtualenv-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Mariner

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  pytest
Requires:       python2
Requires:       python2-libs
BuildRequires:  python-setuptools

BuildArch:      noarch

%description
virtualenv is a tool to create isolated Python environment.

%package -n     python3-virtualenv
Summary:        Virtual Python Environment builder
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pytest
Requires:       python3
Requires:       python3-libs
BuildRequires:  python3-setuptools

%description -n python3-virtualenv
Python 3 version.

%prep
%setup -n virtualenv-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{_bindir}/virtualenv
%{python_sitelib}/*

%files -n python3-virtualenv
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 16.0.0-5
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 16.0.0-4
-   Renaming python-pytest to pytest
*   Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 16.0.0-3
-   License verified.
-   Fixed 'Source0' tag.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 16.0.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 16.0.0-1
-   Update to version 16.0.0
*   Fri Aug 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 15.1.0-1
-   Initial version of python-virtualenv package for Photon.
