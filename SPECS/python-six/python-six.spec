Summary:        Python 2 and 3 compatibility utilities
Name:           python-six
Version:        1.16.0
Release:        2%{?dist}
License:        MIT
Group:          Development/Languages/Python
URL:            https://pypi.org/project/six/
Source0:        https://pypi.python.org/packages/source/s/six/six-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  openssl-devel
BuildRequires:  curl-devel
BuildRequires:  python3-pip
%endif
BuildArch:      noarch

%description
Six is a Python 2 and 3 compatibility library. It provides utility functions for smoothing over the differences between the Python versions with the goal of writing Python code that is compatible on both Python versions. 

%package -n     python3-six
Summary:        Python 2 and 3 compatibility utilities
Requires:       python3

%description -n python3-six

Python 3 version.

%prep
%setup -n six-%{version}

%build
%py3_build

%install
%py3_install

%check
export LANG=C.UTF-8
pip3 install pytest
%pytest test_six.py

%files -n python3-six
%license LICENSE
%{python3_sitelib}/*

%changelog
* Tue Mar 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.16.0-2
- Remove python2 package
- Add license file to the python3 subpackage

* Thu Feb 10 2022 Muhammad Falak <mwani@microsft.com>- 1.16.0-1
- Bump verstion to 1.16.0
- Add an explicit BR on `pip`
- Use `%pytest` to enable ptest

* Fri Dec 03 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.11.0-6
- Replace easy_install usage with pip in %%check sections

* Tue Jul 06 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.11.0-5
- Adding an additional "Provides" for "python2-six" as it's the name expected by some packages.
- Removed the "sha1" macro.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.11.0-4
- Added %%license line automatically

* Tue Apr 07 2020 Paul Monson <paulmon@microsoft.com> 1.11.0-3
- Initial CBL-Mariner import from Photon (license: Apache2).
- Fix Source0. Fix URL. License verified.

* Mon Nov 26 2018 Tapas Kundu <tkundu@vmware.com> 1.11.0-2
- Fix makecheck

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.11.0-1
- Update to version 1.11.0

* Tue Jun 23 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.10.0-8
- Add python-setuptools to BuildRequires to avoid Update issues

* Wed Jun 21 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-7
- Fix make check.

* Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.10.0-6
- Use python2 explicitly

* Wed Apr 05 2017 Sarah Choi <sarahc@vmware.com> 1.10.0-5
- Remove python-setuptools from BuildRequires

* Mon Jan 09 2017 Xiaolin Li <xiaolinl@vmware.com> 1.10.0-4
- Added python3 site-packages.

* Mon Oct 10 2016 ChangLee <changlee@vmware.com> 1.10.0-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.10.0-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Anish Swaminathan <anishs@vmware.com> 1.10.0-1
- Upgrade version

* Wed Mar 04 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial packaging for Photon
