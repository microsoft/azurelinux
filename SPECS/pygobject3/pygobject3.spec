%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Name:           pygobject3
Version:        3.30.1
Release:        6%{?dist}
Summary:        Python Bindings for GObject
Group:          Development/Languages
License:        LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.org/project/PyGObject
Source0:        https://files.pythonhosted.org/packages/00/17/198a9d0eb0e89b5c7d2a9b4437eb40d62702ab771030cd79fc7141cb0d30/PyGObject-3.30.1.tar.gz
Patch0:         pygobject-makecheck-fixes.patch
Patch1:         build_without_cairo.patch
Requires:       gobject-introspection
Requires:       glib
BuildRequires:  glib-devel
BuildRequires:  gobject-introspection-devel
BuildRequires:  which
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs
%if %{with_check}
BuildRequires:  python-setuptools
BuildRequires:  python3-setuptools
BuildRequires:  gobject-introspection-python
BuildRequires:  python3-test
BuildRequires:  glib-schemas
BuildRequires:  dbus
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-xml
%endif

%description
Python bindings for GLib and GObject.

%package -n     python3-pygobject
Summary:        python3-pygobject
Requires:       python3
Requires:       python3-libs
Requires:       gobject-introspection
Requires:       glib

%description -n python3-pygobject
Python 3 version.

%package        devel
Summary:        Development files for embedding PyGObject introspection support
Requires:       python3-pygobject = %{version}-%{release}

%description    devel
Development files for pygobject.

%prep
%setup -q -n PyGObject-%{version}
%patch0 -p1
%patch1 -p1

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 pytest
python3 setup.py test

%clean
rm -rf %{buildroot}

%files -n python3-pygobject
%defattr(-,root,root,-)
%license COPYING
%{python3_sitelib}/*

%files  devel
%{_libdir}/pkgconfig/*.pc
%{_includedir}/*

%changelog
* Sat May 09 2020 Nick Samson <nisamson@microsoft.com>
- Added %%license line automatically

*   Wed Apr 29 2020 Nicolas Ontiveros <niontive@microsoft.com> 3.30.1-5
-   Rename to pygobject3.
-   Remove python2 build. 
*   Tue Mar 31 2020 Paul Monson <paulmon@microsoft.com> 3.30.1-4
-   Fix Source0 URL. License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.30.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Dec 06 2018 Tapas Kundu <tkundu@vmware.com> 3.30.1-2
-   Fix makecheck
*   Thu Sep 27 2018 Tapas Kundu <tkundu@vmware.com> 3.30.1-1
-   Updated to release 3.30.1
*   Tue Sep 19 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.24.1-3
-   Skip some ui make check paths that failed.
*   Thu Aug 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.24.1-2
-   Fix make check
*   Fri Apr 14 2017 Xiaolin Li <xiaolinl@vmware.com> 3.24.1-1
-   Updated to version 3.24.1 and added python3 package.
*   Mon Oct 03 2016 ChangLee <changLee@vmware.com> 3.10.2-3
-   Modified %check
*   Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 3.10.2-2
-   GA - Bump release of all rpms
*   Sat Jan 24 2015 Touseef Liaqat <tliaqat@vmware.com> 7.19.5.1
-   Initial build.  First version
