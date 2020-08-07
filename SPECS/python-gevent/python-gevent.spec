%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Coroutine-based network library
Name:           python-gevent
Version:        1.3.6
Release:        5%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            http://www.gevent.org
#Source0:       https://github.com/gevent/gevent/archive/%{version}.tar.gz
Source0:        gevent-%{version}.tar.gz
Patch0:         python-gevent-makecheck.patch

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires: lsof
BuildRequires: python2-test
BuildRequires: curl-devel
BuildRequires: openssl-devel
BuildRequires: python3-test
%endif

Requires:       python2
Requires:       python2-libs
Requires:       python-greenlet

%description
gevent is a coroutine-based Python networking library.
Features include:
    Fast event loop based on libev.
    Lightweight execution units based on greenlet.
    Familiar API that re-uses concepts from the Python standard library.
    Cooperative sockets with SSL support.
    DNS queries performed through c-ares or a threadpool.
    Ability to use standard library and 3rd party modules written for standard blocking sockets

%package -n     python3-gevent
Summary:        python-gevent

Requires:       python3
Requires:       python3-libs
Requires:       python3-greenlet

%description -n python3-gevent
Python 3 version.

%prep
%setup -q -n gevent-%{version}
%patch0 -p1
cp -a . ../p3dir

%build
python2 setup.py build
cd ../p3dir
python3 setup.py build

%install
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}
pushd ../p3dir
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
popd

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 nose
python2 setup.py develop
nosetests
pushd ../p3dir
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose
python3 setup.py develop
nosetests
popd


%files
%defattr(-,root,root,-)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-gevent
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:06 PST 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Thu Apr 09 2020 Joe Schmitt <joschmit@microsoft.com> 1.3.6-4
-   Update Source0 with valid URL.
-   Remove sha1 macro.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.3.6-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Jan 14 2019 Tapas Kundu <tkundu@vmware.com>1.3.6-2
-   Fix make check
*   Wed Sep 12 2018 Tapas Kundu <tkundu@vmware.com> 1.3.6-1
-   Updated to version 1.3.6
*   Wed Sep 20 2017 Bo Gan <ganb@vmware.com> 1.2.1-6
-   Fix build and make check issues
*   Wed Sep 13 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.1-5
-   Update make check for bug 1900401
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-4
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu Jun 01 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.2.1-3
-   Removed erroneous line
*   Tue May 16 2017 Rongrong Qiu <rqiu@vmware.com> 1.2.1-2
-   Add requires python-greenlet and python3-greenlet
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.2.1-1
-   Initial packaging for Photon
