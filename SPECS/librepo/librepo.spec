%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%define _python3_sitearch %(python3 -c "from distutils.sysconfig import get_python_lib; import sys; sys.stdout.write(get_python_lib(1))")

Summary:        Repodata downloading library
Name:           librepo
Version:        1.11.0
Release:        2%{?dist}
License:        LGPLv2+
URL:            https://github.com/rpm-software-management/librepo
Group:          Applications/System
Vendor:         Microsoft Corporation
Distribution:   Mariner
#Source0:       https://github.com/rpm-software-management/librepo/archive/%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc
BuildRequires:  check
BuildRequires:  glib-devel
BuildRequires:  gpgme-devel
BuildRequires:  attr-devel
BuildRequires:  curl-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:  zchunk-devel
BuildRequires:  python-sphinx
BuildRequires:  python2-devel
BuildRequires:  python3-devel
BuildRequires:  python3-sphinx
Requires:       curl-libs
Requires:       gpgme
Requires:       zchunk

%description
A library providing C and Python (libcURL like) API to downloading repository
metadata.

%package devel
Summary:        Repodata downloading library
Requires:       curl-libs
Requires:       curl-devel
Requires:       %{name} = %{version}-%{release}

%description devel
Development files for librepo.

%package -n python2-%{name}
Summary:        Python bindings for the librepo library
%{?python_provide:%python_provide python2-%{name}}
Requires:       %{name} = %{version}-%{release}

%description -n python2-%{name}
Python 2 bindings for the librepo library.

%package -n python3-%{name}
Summary:        Python 3 bindings for the librepo library
%{?python_provide:%python_provide python3-%{name}}
Requires:       %{name} = %{version}-%{release}

%description -n python3-%{name}
Python 3 bindings for the librepo library.

%prep
%setup -q
mkdir build-py2
mkdir build-py3

%build
pushd build-py2
  %cmake -DPYTHON_DESIRED:FILEPATH=/usr/bin/python -DENABLE_PYTHON_TESTS=%{!?with_pythontests:OFF} ..
  make %{?_smp_mflags}
popd

pushd build-py3
  %cmake -DPYTHON_DESIRED:FILEPATH=/usr/bin/python3 -DENABLE_PYTHON_TESTS=%{!?with_pythontests:OFF} ..
  make %{?_smp_mflags}
popd

%check
make check

%install
pushd build-py2
  make DESTDIR=%{buildroot} install
popd

pushd build-py3
  make DESTDIR=%{buildroot} install
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYING
%doc COPYING
%doc README.md
%{_libdir}/%{name}.so.*

%files devel
%{_libdir}/%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}/

%files -n python2-%{name}
%{python_sitearch}/%{name}/

%files -n python3-%{name}
%{_python3_sitearch}/%{name}/

%changelog
* Sat May 09 00:21:34 PST 2020 Nick Samson <nisamson@microsoft.com> - 1.11.0-2
- Added %%license line automatically

*   Tue May 05 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.11.0-1
-   Update version to 1.11.0.
*   Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> 1.10.3-1
-   Update to version 1.10.3. License verified.
*   Wed Sep 25 2019 Saravanan Somasundaram <sarsoma@microsoft.com> 1.10.2-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Wed May 15 2019 Ankit Jain <ankitja@vmware.com> 1.10.2-1
-   Initial build. First version
