%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        An implementation of the OAuth request-signing logic
Name:           python-oauthlib
Version:        2.1.0
Release:        4%{?dist}
License:        BSD
Url:            https://github.com/oauthlib/oauthlib
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/df/5f/3f4aae7b28db87ddef18afed3b71921e531ca288dc604eb981e9ec9f8853/oauthlib-%{version}.tar.gz

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  libffi-devel
Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
OAuthLib is a generic utility which implements the logic of OAuth without assuming a specific HTTP request object or web framework

%package -n python3-oauthlib
Summary:        Python3 package for oauthlib
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs

%description -n python3-oauthlib
Python 3 version of oauthlib

%prep
%setup -q -n oauthlib-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build

pushd ../p3dir
python3 setup.py build
popd


%install
rm -rf %{buildroot}
python2 setup.py install --root=%{buildroot}

pushd ../p3dir
python3 setup.py install --root=%{buildroot}
popd

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 mock
python2 setup.py test

pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 mock
python3 setup.py test
popd

%files
%defattr(-, root, root, -)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-oauthlib
%{python3_sitelib}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.1.0-4
- Added %%license line automatically

*   Mon Apr 13 2020 Jon Slobodzian <joslobo@microsoft.com> 2.1.0-3
-   Verified license. Removed sha1. Fixed Source0 URL. Fixed URL.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.1.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.1.0-1
-   Update to version 2.1.0
*   Fri Jul 07 2017 Chang Lee <changlee@vmware.com> 2.0.2-3
-   Add  libffi-devel in BuildRequires and install mock python module in %check
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 2.0.2-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Apr 13 2017 Anish Swaminathan <anishs@vmware.com> 2.0.2-1
-   Initial packaging for Photon
