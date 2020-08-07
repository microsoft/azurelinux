%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-websocket-client
Version:        0.56.0
Release:        2%{?dist}
Summary:        WebSocket client for python
License:        BSD
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/websocket-client
Source0:        https://files.pythonhosted.org/packages/c5/01/8c9c7de6c46f88e70b5a3276c791a2be82ae83d8e0d0cc030525ee2866fd/websocket_client-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
%endif

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
WebSocket client for python

%package -n     python3-websocket-client
Summary:        WebSocket client for python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%description -n python3-websocket-client
WebSocket client for python3

%prep
%setup -n websocket_client-%{version}
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
%license LICENSE
%{python2_sitelib}/*
/usr/bin/wsdump.py

%files -n python3-websocket-client
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 0.56.0-2
-   Added %%license line automatically
*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 0.56.0-1
-   Initial CBL-Mariner import from Photon (license: Apache2).
-   Update to 0.56.0. Update Vendor and Distribution. Source0 URL Fixed. License fixed.
*   Fri Dec 07 2018 Ashwin H <ashwinh@vmware.com> 0.53.0-2
-   Add %check
*   Fri Sep 14 2018 Tapas Kundu <tkundu@vmware.com> 0.53.0-1
-   Updated to release 0.53.0
*   Thu Nov 30 2017 Xiaolin Li <xiaolinl@vmware.com> 0.44.0-1
-   Update websocket_client to version 0.44.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 0.7.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Sun Jun 04 2017 Vinay Kulkarni <kulkarniv@vmware.com> 0.7.0-1
-   Initial version of python WebSocket for PhotonOS.
