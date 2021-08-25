%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

%define pkgname nocasedict

Summary:        Case-insensitive ordered dictionary library for Python
Name:           python-%{pkgname}
Version:        0.5.0
Release:        1%{?dist}
License:        LGPLv2+
URL:            https://github.com/pywbem/nocasedict
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/pywbem/%{pkgname}/archive/%{version}.tar.gz
Source0:        %{pkgname}-%{version}.tar.gz
BuildArch:      noarch

%description 
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.


%package -n python3-%{pkgname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-six
BuildRequires:  python3-pytest >= 3.0.7
Requires:       python3
Requires:       python3-six


%description -n python3-%{pkgname}
The NocaseDict class supports the functionality of the built-in dict class of Python 3.8.

%prep
%autosetup -n %{pkgname}-%{version} -p 1
rm -rf *.egg-info


%build
python3 setup.py build


%install
python3 setup.py install --skip-build --root=%{buildroot}


%if %{with tests}
%check
python3 setup.py test
%endif


%files -n python3-%{pkgname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{pkgname}
%{python3_sitelib}/*.egg-info

%changelog
* Tue Jan 05 2021 Ruying Chen <v-ruyche@microsoft.com> - 0.5.0-2
- Disable auto dependency generator.
- Add explicit dist provides.

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 0.5.0-1
- Original CBL-Mariner version.
- License verified.
