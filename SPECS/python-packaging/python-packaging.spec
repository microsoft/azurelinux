%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Core utilities for Python packages
Name:           python-packaging
Version:        17.1
Release:        6%{?dist}
Url:            https://pypi.python.org/pypi/packaging
License:        BSD or ASL 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
# This link seems very sensitive to the precise package version.
# Source0:      https://files.pythonhosted.org/packages/77/32/439f47be99809c12ef2da8b60a2c47987786d2c6c9205549dd6ef95df8bd/packaging-%{version}.tar.gz
Source0:        packaging-%{version}.tar.gz
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires:  python-setuptools
BuildRequires:  python3-setuptools
BuildRequires:  pyparsing
BuildRequires:  python-six
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-xml
BuildRequires:  python3-pyparsing
BuildRequires:  python3-six
%endif

Requires:       python2
Requires:       python2-libs
Requires:       pyparsing
Requires:       python-six

BuildArch:      noarch

%description
Cryptography is a Python library which exposes cryptographic recipes and primitives.

%package -n     python3-packaging
Summary:        python-packaging

Requires:       python3
Requires:       python3-libs
Requires:       python3-pyparsing
Requires:       python3-six

%description -n python3-packaging

Python 3 version.

%prep
%setup -q -n packaging-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
pushd ../p3dir
python3 setup.py build
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pretend pytest
PYTHONPATH=./ pytest

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pretend pytest
PYTHONPATH=./ pytest

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-packaging
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Fri Apr 17 2020 Nicolas Ontiveros <niontive@microsoft.com> 17.1-5
-   Use pyparsing in Requres and BR.
*   Mon Apr 13 2020 Nick Samson <nisamson@microsoft.com> 17.1-4
-   Updated Source0, removed %%define sha1, confirmed license.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 17.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Dec 07 2018 Tapas Kundu <tkundu@vmware.com> 17.1-2
-   Fix makecheck
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 17.1-1
-   Update to version 17.1
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 16.8-4
-   Fixed rpm check errors
-   Fixed runtime dependencies
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 16.8-3
-   Fix arch
*   Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 16.8-2
-   Remove python-setuptools from BuildRequires
*   Tue Apr 04 2017 Xiaolin Li <xiaolinl@vmware.com> 16.8-1
-   Initial packaging for Photon
