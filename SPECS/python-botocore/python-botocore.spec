%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        Amazon Web Services Library.
Name:           python-botocore
Version:        1.13.21
Release:        2%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://github.com/boto/botocore
Source0:        https://github.com/boto/botocore/archive/botocore-%{version}.tar.gz
#Source0:        https://github.com/boto/botocore/archive/%{version}.tar.gz
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-xml
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  python-pip
BuildRequires:  python3-pip
BuildRequires:  python-dateutil
BuildRequires:  python-urllib3
BuildRequires:  python3-dateutil
BuildRequires:  python3-urllib3
%endif
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch

%description
A low-level interface to a growing number of Amazon Web Services. The botocore package is the foundation for the AWS CLI as well as boto3.

%package -n     python3-botocore
Summary:        python3-botocore
Requires:       python3
Requires:       python3-libs

%description -n python3-botocore
Python 3 version.

%prep
%setup -q -n botocore-%{version}
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
pip install nose
pip install mock
pip install jmespath
nosetests tests/unit
pushd ../p3dir
pip3 install nose
pip3 install mock
pip3 install jmespath
nosetests tests/unit
popd

%files
%defattr(-,root,root)
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python3-botocore
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 1.13.21-1
-   Update to 1.13.21. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.12.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com> 1.12.0-2
-   Fix make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.12.0-1
-   Update to version 1.12.0
*   Sun Jan 07 2018 Kumar Kaushik <kaushikk@vmware.com> 1.8.15-1
-   Initial packaging for photon.
