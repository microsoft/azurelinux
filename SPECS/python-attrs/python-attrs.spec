%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Attributes without boilerplate.
Name:           python-attrs
Version:        18.2.0
Release:        7%{?dist}
Url:            https://pypi.python.org/pypi/attrs
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/0f/9e/26b1d194aab960063b266170e53c39f73ea0d0d3f5ce23313e0ec8ee9bdf/attrs-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-zope-interface
BuildRequires:  python3-pip
%endif
Requires:       python2
Requires:       python2-libs

%description
Attributes without boilerplate.

%package -n     python3-attrs
Summary:        python-attrs

Requires:       python3
Requires:       python3-libs

%description -n python3-attrs

Python 3 version.

%prep
%setup -q -n attrs-%{version}
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
# Tests are only supported with Python3
pip3 install pytest hypothesis==4.38.0 tox
LANG=en_US.UTF-8 tox -e py37

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-attrs
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Tue Jan 05 2021 Andrew Phelps <anphel@microsoft.com> 18.2.0-7
-   Use tox to run tests.
*   Wed Jul 08 2020 Henry Beberman <henry.beberman@microsoft.com> 18.2.0-6
-   Fix typo in BuildRequires for python3-zope-interface
*   Sat May 09 00:20:45 PST 2020 Nick Samson <nisamson@microsoft.com> 18.2.0-5
-   Added %%license line automatically
*   Fri Apr 24 2020 Nick Samson <nisamson@microsoft.com> 18.2.0-4
-   Updated Source0, license verified. Removed %%define sha1
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 18.2.0-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Tue Nov 13 2018 Tapas Kundu <tkundu@vmware.com> 18.2.0-2
-   Fixed the makecheck errors
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 18.2.0-1
-   Update to version 18.2.0
*   Thu Jul 06 2017 Chang Lee <changlee@vmware.com> 16.3.0-3
-   Updated %check
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 13 2017 Xiaolin Li <xiaolinl@vmware.com> 16.3.0-1
-   Initial packaging for Photon
