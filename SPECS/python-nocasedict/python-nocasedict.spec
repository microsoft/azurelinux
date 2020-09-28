%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%bcond_without  python2
%define pkgname nocasedict

Summary:        Case-insensitive ordered dictionary library for Python
Name:           python-%{pkgname}
Version:        0.5.0
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/pywbem/nocasedict
Vendor:         Microsoft
Distribution:   Mariner
#Source0:       https://github.com/pywbem/%{pkgname}/archive/%{version}.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description 
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.


%if %{with python2}
%package -n python2-%{pkgname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-xml
BuildRequires:  python-six
Requires:       python2
Requires:       python-six
%if %{with tests}
BuildRequires:  python2-pytest >= 3.0.7
%endif

%description -n python2-%{pkgname}
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.
%endif


%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-six
Requires:       python3
Requires:       python3-six
%if %{with tests}
BuildRequires:  python3-pytest >= 3.0.7
%endif


%description -n python3-%{pkgname}
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.


%prep
%autosetup -n %{pkgname}-%{version} -p 1
rm -rf *.egg-info


%build
%if %{with python2}
python2 setup.py build
%endif
python3 setup.py build


%install
%if %{with python2}
python2 setup.py install --skip-build --root=%{buildroot}
%endif
python3 setup.py install --skip-build --root=%{buildroot}


%if %{with tests}
%check
%if %{with python2}
python2 setup.py test
%endif
python3 setup.py test
%endif


%if %{with python2}
%files -n python2-%{pkgname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pkgname}
%{python2_sitelib}/*.egg-info
%endif


%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*.egg-info


%changelog
* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.0-1
- Original CBL-Mariner version.