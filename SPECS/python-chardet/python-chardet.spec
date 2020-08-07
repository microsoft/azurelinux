%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        A Universal Character Encoding Detector in Python
Name:           python-chardet
Version:        3.0.4
Release:        5%{?dist}
Url:            https://github.com/chardet/chardet
License:        LGPLv2+
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/chardet/chardet/archive/%{version}.tar.gz
Source0:        chardet-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if %{with_check}
BuildRequires:	pytest
%endif

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
chardet is a universal character encoding detector in Python.

%package -n     python3-chardet
Summary:        python3-chardet

BuildRequires:  python3
BuildRequires:  python3-libs
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:	python3-pytest
%endif

Requires:       python3
Requires:       python3-libs

%description -n python3-chardet
Python 3 version of chardet.

%prep
%setup -q -n chardet-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
# TODO

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-chardet
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/chardetect

%changelog
* Sat May 09 00:21:23 PST 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> 3.0.4-4
-   Renaming python-pytest to pytest
*   Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 3.0.4-3
-   Update URL.
-   Update License.
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.0.4-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 3.0.4-1
-   Initial packaging.
