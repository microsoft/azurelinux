%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Lightweight in-process concurrent programming
Name:           python-greenlet
Version:        0.4.15
Release:        5%{?dist}
License:        MIT or Python
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/greenlet
# Source0:      https://files.pythonhosted.org/packages/f8/e8/b30ae23b45f69aa3f024b46064c0ac8e5fcb4f22ace0dca8d6f9c8bbe5e7/greenlet-%{version}.tar.gz
Source0:        greenlet-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
Requires:       python2
Requires:       python2-libs

%description
The greenlet package is a spin-off of Stackless, a version of CPython that supports micro-threads called “tasklets”. Tasklets run pseudo-concurrently (typically in a single or a few OS-level threads) and are synchronized with data exchanges on “channels”.

A “greenlet”, on the other hand, is a still more primitive notion of micro-thread with no implicit scheduling; coroutines, in other words. This is useful when you want to control exactly when your code runs. You can build custom scheduled micro-threads on top of greenlet; however, it seems that greenlets are useful on their own as a way to make advanced control flow structures. For example, we can recreate generators; the difference with Python’s own generators is that our generators can call nested functions and the nested functions can yield values too. Additionally, you don’t need a “yield” keyword. See the example in tests/test_generator.py.

%package -n     python3-greenlet
Summary:        python-greenlet
Requires:       python3
Requires:       python3-libs

%description -n python3-greenlet
Python 3 version.

%prep
%setup -q -n greenlet-%{version}

%build
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python2 setup.py test
#make check test code only support python2
#python3 setup.py test

%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*
/usr/include/python2.7/greenlet/greenlet.h

%files -n python3-greenlet
%defattr(-,root,root,-)
%{python3_sitelib}/*
/usr/include/python3.7m/greenlet/greenlet.h

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 0.4.15-5
- Added %%license line automatically

*   Tue Apr 14 2020 Nick Samson <nisamson@microsoft.com> 0.4.15-4
-   Updated Source0, license, removed sha1 line. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.4.15-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Fri Oct 05 2018 Tapas Kundu <tkundu@vmware.com> 0.4.15-2
-   Updated using python 3.7
-   removed buildrequires from subpackages
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 0.4.15-1
-   Update to version 0.4.15
*   Fri Aug 11 2017 Rongrong Qiu <rqiu@vmware.com> 0.4.12-3
-   make check only support python3 for bug 1937030
*   Thu Apr 27 2017 Siju Maliakkal <smaliakkal@vmware.com> 0.4.12-2
-   updated python version
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 0.4.12-1
-   Initial packaging for Photon
