%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python package for providing Mozilla's CA Bundle
Name:           python-certifi
Version:        2018.10.15
Release:        4%{?dist}
URL:            https://github.com/certifi
License:        MPL-2.0
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://github.com/certifi/python-certifi/archive/certifi-%{version}.tar.gz
#Source0:        https://github.com/certifi/python-certifi/archive/%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  pytest
%endif

BuildArch:      noarch

%description
Certifi is a carefully curated collection of
Root Certificates for validating the trustworthiness of
SSL certificates while verifying the identity of TLS hosts

%package -n     python3-certifi
Summary:        Python 3 certifi library

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pytest
%endif

%description -n python3-certifi
Python 3 version of certifi.

%prep
%setup -q -n python-certifi-%{version}

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
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-certifi
%defattr(-,root,root,-)
%license LICENSE
%{python3_sitelib}/*

%changelog
*   Sat May 09 00:20:57 PST 2020 Nick Samson <nisamson@microsoft.com> 2018.10.15-4
-   Added %%license line automatically
*   Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2018.10.15-3
-   Removing *Requires for "ca-certificates".
*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 2018.10.15-2
-   Renaming python-pytest to pytest
*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 2018.10.15-1
-   Update to 2018.10.15. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2018.08.24-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed Sep 19 2018 Ajay Kaher <akaher@vmware.com> 2018.08.24-1
-   Initial packaging
