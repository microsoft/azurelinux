%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           python-appdirs
Version:        1.4.3
Release:        4%{?dist}
Summary:        Python 2 and 3 compatibility utilities
License:        MIT
Group:          Development/Languages/Python
Url:            https://pypi.python.org/pypi/appdirs
Source0:        https://pypi.python.org/packages/48/69/d87c60746b393309ca30761f8e2b49473d43450b150cb08f3c6df5c11be5/appdirs-%{version}.tar.gz
%define sha1    appdirs=9ad09395ed489ad66e9688e49087ce1814c64276

BuildRequires:  python2
BuildRequires:  python2-libs

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
A small Python module for determining appropriate platform-specific dirs, e.g. a "user data dir".

%package -n     python3-appdirs
Summary:        python-appdirs
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python3
Requires:       python3-libs

%description -n python3-appdirs

Python 3 version.

%prep
%setup -n appdirs-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
cd test

PATH=%{buildroot}%{_bindir}:${PATH} \
 PYTHONPATH=%{buildroot}%{python2_sitelib} \
python2 test_api.py

PATH=%{buildroot}%{_bindir}:${PATH} \
 PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 test_api.py

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{python2_sitelib}/*

%files -n python3-appdirs
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.4.3-4
-   Added %%license line automatically
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.3-3
-   Changes to check section
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.4.3-2
-   Change python to python2
*   Mon Apr 03 2017 Sarah Choi <sarahc@vmware.com> 1.4.3-1
-   Create appdirs 1.4.3
