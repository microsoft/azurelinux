%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%define _python_bytecompile_errors_terminate_build 0
Name:           python-jinja2
Version:        2.10.1
Release:        2%{?dist}
Url:            https://jinja.pocoo.org/
Summary:        A fast and easy to use template engine written in pure Python
License:        BSD
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Source0:        https://files.pythonhosted.org/packages/93/ea/d884a06f8c7f9b7afbc8138b762e80479fb17aedbbe2b06515a12de9378d/Jinja2-%{version}.tar.gz
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python-markupsafe
Requires:       python2
Requires:       python2-libs
Requires:       python-markupsafe
BuildArch:      noarch

%description
Jinja2 is a template engine written in pure Python.  It provides a Django
inspired non-XML syntax but supports inline expressions and an optional
sandboxed environment.

%package -n     python3-jinja2
Summary:        A fast and easy to use template engine written in pure Python
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-markupsafe
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       python3
Requires:       python3-libs
Requires:       python3-markupsafe

%description -n python3-jinja2

Python 3 version.

%prep
%setup -q -n Jinja2-%{version}
rm -rf ../p3dir
cp -a . ../p3dir

%build
python2 setup.py build
sed -i 's/\r$//' LICENSE # Fix wrong EOL encoding
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
sed -i 's/\r$//' LICENSE # Fix wrong EOL encoding
popd

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
make -k check |& tee %{_specdir}/%{name}-check-log || %{nocheck}

%files
%defattr(-,root,root)
%doc AUTHORS
%license LICENSE
%{python2_sitelib}/jinja2
%{python2_sitelib}/Jinja2-%{version}-py%{python_version}.egg-info

%files -n python3-jinja2
%defattr(-,root,root)
%doc AUTHORS
%license LICENSE
%{python3_sitelib}/jinja2
%{python3_sitelib}/Jinja2-%{version}-py%{python3_version}.egg-info

%changelog
* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 2.10.1-2
- Make python byte compilation errors non-fatal due to python2 errors.

*   Wed Mar 18 2020 Henry Beberman <henry.beberman@microsoft.com> 2.10.1-1
-   Update to 2.10.1. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.10-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 2.10-1
-   Update to version 2.10
*   Tue Jun 20 2017 Xiaolin Li <xiaolinl@vmware.com> 2.9.5-6
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 15 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.9.5-5
-   Change python to python2
*   Mon Jun 12 2017 Kumar Kaushik <kaushikk@vmware.com> 2.9.5-4
-   Fixing import error in python3.
*   Wed Apr 26 2017 Dheeraj Shetty <dheerajs@vmware.com> 2.9.5-3
-   BuildRequires python-markupsafe , creating subpackage python3-jinja2
*   Tue Apr 25 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.9.5-2
-   Fix arch
*   Mon Mar 27 2017 Sarah Choi <sarahc@vmware.com> 2.9.5-1
-   Upgrade version to 2.9.5
*   Tue Dec 13 2016 Dheeraj Shetty <dheerajs@vmware.com> 2.8-1
-   Initial packaging for Photon
