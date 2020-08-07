%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Array processing for numbers, strings, records, and objects
Name:           numpy
Version:        1.16.6
Release:        1%{?dist}
# The custom license is inside numpy/core/src/multiarray/dragon4.c.
License:        BSD and ZLIB custom
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://numpy.org/
Source0:        https://github.com/numpy/numpy/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  python2-devel
BuildRequires:  lapack-devel
BuildRequires:  unzip

BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
%endif
Requires:       python2
Requires:       python2-libs
%description
NumPy is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays. NumPy is built on the Numeric code base and adds features introduced by numarray as well as an extended C-API and the ability to create arrays of arbitrary type which also makes NumPy suitable for interfacing with general-purpose data-base applications.

%package -n python2-numpy-f2py
Summary:        f2py for numpy
Requires:       %{name} = %{version}-%{release}
Requires:       python2-devel
Provides:       f2py = %{version}-%{release}
Provides:       numpy-f2py = %{version}-%{release}
%description -n python2-numpy-f2py
This package includes a version of f2py that works properly with NumPy.

%package -n     python3-numpy
Summary:        python-numpy
Requires:       python3
Requires:       python3-libs
%description -n python3-numpy
Python 3 version.

%package -n python3-numpy-f2py
Summary:        f2py for numpy
Requires:       python3-numpy = %{version}-%{release}
Requires:       python3-devel
Provides:       python3-f2py = %{version}-%{release}
%description -n python3-numpy-f2py
This package includes a version of f2py that works properly with NumPy.


%prep
%setup -q

%build
# xlocale.h has been removed from glibc 2.26
# The above include of locale.h is sufficient
# Further details: https://sourceware.org/git/?p=glibc.git;a=commit;h=f0be25b6336db7492e47d2e8e72eb8af53b5506d */
sed -i "/xlocale.h/d" numpy/core/src/common/numpyos.c
python2 setup.py build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}
python2 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
easy_install_2=$(ls /usr/bin |grep easy_install |grep 2)
$easy_install_2 nose pytest
mkdir test
pushd test
PYTHONPATH=%{buildroot}%{python2_sitelib} PATH=$PATH:%{buildroot}%{_bindir} python2 -c "import numpy; numpy.test()"
popd

easy_install_3=$(ls /usr/bin |grep easy_install |grep 3)
$easy_install_3 nose pytest
pushd test
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} python3 -c "import numpy; numpy.test()"
popd

rm -rf test

%files
%defattr(-,root,root,-)
%license LICENSE.txt
%{python2_sitelib}/*
%{_bindir}/f2py2

%files -n python3-numpy
%defattr(-,root,root,-)
%{python3_sitelib}/*
%{_bindir}/f2py3

%files -n python3-numpy-f2py
%{_bindir}/f2py3
%{_bindir}/f2py3.7

%files -n python2-numpy-f2py
%{_bindir}/f2py
%{_bindir}/f2py2
%{_bindir}/f2py2.7
#{_bindir}/f2py.numpy
#{python2_sitearch}/{name}/f2py

%changelog
*   Mon Jun 08 2020 Paul Monson <paulmon@microsoft.com> 1.16.6-1
-   Update to 1.16.6 to fix CVE-2019-6446
*   Sat May 09 2020 Nick Samson <nisamson@microsoft.com> 1.15.1-6
-   Added %%license line automatically
*   Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> 1.15.1-5
-   Renaming python-numpy to numpy
*   Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.15.1-4
-   Fixed 'Source0' and 'URL' tags.
-   License verified.
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.15.1-3
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> 1.15.1-2
-   Fixed make check
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 1.15.1-1
-   Update to version 1.15.1
*   Fri Aug 25 2017 Alexey Makhalov <amakhalov@vmware.com> 1.12.1-5
-   Fix compilation issue for glibc-2.26
*   Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> 1.12.1-4
-   Fixed rpm check errors
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.12.1-3
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Thu May 04 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-2
-   Fix typo in Source0
*   Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> 1.12.1-1
-   Upgrade version to 1.12.1
*   Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> 1.8.2-1
-   Initial packaging for Photon
