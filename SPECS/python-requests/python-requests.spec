%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
Summary:        Awesome Python HTTP Library That's Actually Usable
Name:           python-requests
Version:        2.22.0
Release:        1%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            http://python-requests.org
#Source0:       https://github.com/requests/requests/archive/v%{version}/requests-v%{version}.tar.gz
Source0:        requests-%{version}.tar.gz
BuildRequires:  python-setuptools
BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
Requires:       pyOpenSSL
Requires:       python-certifi
Requires:       python-chardet
Requires:       python-idna
Requires:       python-urllib3
Requires:       python2
Requires:       python2-libs
BuildArch:      noarch
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  pytest
BuildRequires:  python-atomicwrites
BuildRequires:  python-attrs
BuildRequires:  python-certifi
BuildRequires:  python-chardet
BuildRequires:  python-idna
BuildRequires:  python-urllib3
%endif
%if %{with_check}
BuildRequires:  python3-atomicwrites
BuildRequires:  python3-attrs
BuildRequires:  python3-certifi
BuildRequires:  python3-chardet
BuildRequires:  python3-idna
BuildRequires:  python3-pytest
BuildRequires:  python3-urllib3
%endif

%description
Requests is an Apache2 Licensed HTTP library, written in Python, for human
beings.

Most existing Python modules for sending HTTP requests are extremely
verbose and cumbersome. Python's builtin urllib2 module provides most of
the HTTP capabilities you should need, but the api is thoroughly broken.
It requires an enormous amount of work (even method overrides) to
perform the simplest of tasks.

Features:

- Extremely simple GET, HEAD, POST, PUT, DELETE Requests
    + Simple HTTP Header Request Attachment
    + Simple Data/Params Request Attachment
    + Simple Multipart File Uploads
    + CookieJar Support
    + Redirection History
    + Redirection Recursion Urllib Fix
    + Auto Decompression of GZipped Content
    + Unicode URL Support
- Simple Authentication
    + Simple URL + HTTP Auth Registry

%package -n     python3-requests
Summary:        python-requests
Requires:       python3
Requires:       python3-certifi
Requires:       python3-chardet
Requires:       python3-idna
Requires:       python3-libs
Requires:       python3-pyOpenSSL
Requires:       python3-urllib3

%description -n python3-requests
Python 3 version.

%prep
%setup -q -n requests-%{version}
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
easy_install_2=$(ls %{_bindir} |grep easy_install |grep 2)
$easy_install_2 pathlib2 funcsigs pluggy more_itertools pysocks
$easy_install_2 pytest-mock pytest-httpbin
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python2_sitelib} \
py.test2

easy_install_3=$(ls %{_bindir} |grep easy_install |grep 3)
$easy_install_3 pathlib2 funcsigs pluggy more_itertools pysocks
$easy_install_3 pytest-mock pytest-httpbin
LANG=en_US.UTF-8  PYTHONPATH=%{buildroot}%{python3_sitelib} \
py.test3

%files
%defattr(-,root,root)
%license LICENSE
%license LICENSE
%doc README.md HISTORY.md
%{python2_sitelib}/*

%files -n python3-requests
%defattr(-,root,root)
%license LICENSE
%doc README.md HISTORY.md
%{python3_sitelib}/*

%changelog
* Thu Dec 31 2020 Thomas Crain <thcrain@microsoft.com> - 2.22.0-1
- Upgrade to version 2.22.0
- Fix Source0 URL

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 2.20.0-4
- Added %%license line automatically

* Thu Apr 30 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.20.0-3
- Renaming python-pytest to pytest

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.20.0-2
- Renaming python-pyOpenSSL to pyOpenSSL

* Thu Mar 19 2020 Paul Monson <paulmon@microsoft.com> - 2.20.0-1
- Update to 2.20.0. Fix source0 URL. Fix license.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.19.1-5
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Mar 28 2019 Tapas Kundu <tkundu@vmware.com> - 2.19.1-4
- Fix for CVE-2018-18074

* Thu Dec 06 2018 Ashwin H <ashwinh@vmware.com> - 2.19.1-3
- Add %check

* Thu Sep 27 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> - 2.19.1-2
- Add a few missing runtime dependencies (urllib3, chardet,
- pyOpenSSL, certifi, idna).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 2.19.1-1
- Update to version 2.19.1

* Mon Aug 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.13.0-3
- Disabled check section as tests are not available

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.13.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu Mar 23 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.13.0-1
- Updated to version 2.13.0.

* Wed Mar 01 2017 Xiaolin Li <xiaolinl@vmware.com> - 2.9.1-4
- Added python3 package.

* Mon Oct 04 2016 ChangLee <changlee@vmware.com> - 2.9.1-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.9.1-2
- GA - Bump release of all rpms

* Tue Feb 23 2016 Harish Udaiya Kumar <hudaiyakumar@vmware.com> - 2.9.1-1
- Updated to version 2.9.1

* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
