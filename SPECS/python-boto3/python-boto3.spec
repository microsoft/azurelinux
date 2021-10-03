Summary:        The AWS SDK for Python
Name:           python-boto3
Version:        1.10.21
Release:        3%{?dist}
License:        Apache 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://github.com/boto/boto3
#Source0:       https://github.com/boto/boto3/archive/%{version}.tar.gz
Source0:        https://github.com/boto/boto3/archive/boto3-%{version}.tar.gz

%description
The AWS SDK for Python

%package -n     python3-boto3
Summary:        python3-boto3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-botocore
Requires:       python3-dateutil
Requires:       python3-jmespath

%description -n python3-boto3
Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python,
which allows Python developers to write software that makes use of services like
Amazon S3 and Amazon EC2

%prep
%autosetup -n boto3-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} setup.py test

%files -n python3-boto3
%defattr(-,root,root)
%license LICENSE
%{python3_sitelib}/*

%changelog
* Fri Oct 01 2021 Thomas Crain <thcrain@microsoft.com> - 1.10.21-3
- Add license to python3 package
- Remove python2 package
- Lint spec

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.10.21-2
- Added %%license line automatically

* Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 1.10.21-1
- Update to 1.10.21. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.9.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.9.0-1
- Update to version 1.9.0

* Wed Jan 24 2018 Kumar Kaushik <kaushikk@vmware.com> 1.5.9-1
- Initial packaging for photon.
