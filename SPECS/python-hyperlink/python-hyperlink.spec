%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        provides a pure-Python implementation of immutable URLs
Name:           python-hyperlink
Version:        19.0.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://github.com/python-hyper/hyperlink
Source0:        https://github.com/python-hyper/hyperlink/archive/%{name}-%{version}.tar.gz
#Source0:        https://github.com/python-hyper/hyperlink/archive/v%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python2
Requires:       python2-libs
%if %{with_check}
BuildRequires:  python-idna
BuildRequires:  python3-idna
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
BuildArch:      noarch

%description
Hyperlink provides a pure-Python implementation of immutable URLs. Based on RFC 3986 and 3987, the Hyperlink URL makes working with both URIs and IRIs easy.

%package -n     python3-hyperlink
Summary:        provides a pure-Python implementation of immutable URLs

Requires:       python3
Requires:       python3-libs

%description -n python3-hyperlink
Python 3 version.

%prep
%setup -q -n hyperlink-%{version}
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
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 pytest
pytest
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
pytest
popd


%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-hyperlink
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 19.0.0-1
-   Update to 19.0.0. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 18.0.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Dec 06 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-2
-   Fix make check.
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.0.0-1
-   Update to version 18.0.0
*   Wed Sep 20 2017 Bo Gan <ganb@vmware.com> 17.3.1-2
-   Fix make check issues
*   Mon Sep 11 2017 Dheeraj Shetty <dheerajs@vmware.com> 17.3.1-1
-   Initial packaging for Photon
