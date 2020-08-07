%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}

Summary:        The AWS SDK for Python
Name:           python-boto3
Version:        1.10.21
Release:        2%{?dist}
License:        Apache 2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://github.com/boto/boto3
Source0:        https://github.com/boto/boto3/archive/boto3-%{version}.tar.gz
#Source0:        https://github.com/boto/boto3/archive/%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-xml
Requires:       python2
Requires:       python2-libs
Requires:       python-botocore
Requires:       python-jmespath
Requires:       python-dateutil
BuildArch:      noarch

%description
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python,
which allows Python developers to write software that makes use of services like
Amazon S3 and Amazon EC2

%package -n     python3-boto3
Summary:        python3-boto3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-botocore
Requires:       python3-jmespath
Requires:       python3-dateutil

%description -n python3-boto3
Python 3 version.

%prep
%setup -q -n boto3-%{version}
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
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-boto3
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:11 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.10.21-2
- Added %%license line automatically

*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 1.10.21-1
-   Update to 1.10.21. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.9.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
-   Update to version 1.9.0
*   Wed Jan 24 2018 Kumar Kaushik <kaushikk@vmware.com> 1.5.9-1
-   Initial packaging for photon.
