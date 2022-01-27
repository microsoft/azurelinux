Summary:        Array processing for numbers, strings, records, and objects
Name:           numpy
Version:        1.22.0
Release:        1%{?dist}
# The custom license is inside numpy/core/src/multiarray/dragon4.c.
License:        BSD AND ZLIB custom
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Languages/Python
URL:            https://numpy.org/
Source0:        https://github.com/numpy/numpy/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  lapack-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-libs
BuildRequires:  unzip
BuildRequires:  python3-Cython >= 0.29.24
%if %{with_check}
BuildRequires:  curl-devel
BuildRequires:  openssl-devel
BuildRequires:  python3-pip
%endif

%description
NumPy is a general-purpose array-processing package designed to efficiently manipulate large multi-dimensional arrays of arbitrary records without sacrificing too much speed for small multi-dimensional arrays. NumPy is built on the Numeric code base and adds features introduced by numarray as well as an extended C-API and the ability to create arrays of arbitrary type which also makes NumPy suitable for interfacing with general-purpose data-base applications.

%package -n     python3-numpy
Summary:        python-numpy
Requires:       python3
Requires:       python3-libs

%description -n python3-numpy
Python 3 version.

%package -n python3-numpy-f2py
Summary:        f2py for numpy
Requires:       python3-devel
Requires:       python3-numpy = %{version}-%{release}
Provides:       python3-f2py = %{version}-%{release}

%description -n python3-numpy-f2py
This package includes a version of f2py that works properly with NumPy.

%prep
%autosetup -p1

%build
%py3_build

%install
%py3_install

%check
pip3 install nose pytest
pushd test
PYTHONPATH=%{buildroot}%{python3_sitelib} PATH=$PATH:%{buildroot}%{_bindir} python3 -c "import numpy; numpy.test()"
popd
rm -rf test

%files -n python3-numpy
%license LICENSE.txt
%{python3_sitelib}/*
%{_bindir}/f2py3

%files -n python3-numpy-f2py
%{_bindir}/f2py
%{_bindir}/f2py3
%{_bindir}/f2py%{python3_version}

%changelog
* Thu Jan 06 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.22.0-1
- Update version to 1.22.0 fix CVE-2021-34141.

* Tue Dec 28 2021 Henry Beberman <henry.beberman@microsoft.com> - 1.16.6-4
- Backported upstream patch for CVE-2021-41496

* Tue Dec 14 2021 Chris Co <chrco@microsoft.com> - 1.16.6-3
- Backport patch to fix python3 setup.py install error
- Add f2py to packaging

* Fri Dec 03 2021 Thomas Crain <thcrain@microsoft.com> - 1.16.6-2
- Remove python2 subpackage
- Replace easy_insall usage with pip in %%check section

* Mon Jun 08 2020 Paul Monson <paulmon@microsoft.com> - 1.16.6-1
- Update to 1.16.6 to fix CVE-2019-6446

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 1.15.1-6
- Added %%license line automatically

* Wed Apr 29 2020 Emre Girgin <mrgirgin@microsoft.com> - 1.15.1-5
- Renaming python-numpy to numpy

* Mon Apr 27 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.15.1-4
- Fixed 'Source0' and 'URL' tags.
- License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 1.15.1-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Dec 03 2018 Tapas Kundu <tkundu@vmware.com> - 1.15.1-2
- Fixed make check

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 1.15.1-1
- Update to version 1.15.1

* Fri Aug 25 2017 Alexey Makhalov <amakhalov@vmware.com> - 1.12.1-5
- Fix compilation issue for glibc-2.26

* Wed Jul 26 2017 Divya Thaluru <dthaluru@vmware.com> - 1.12.1-4
- Fixed rpm check errors

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.12.1-3
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Thu May 04 2017 Sarah Choi <sarahc@vmware.com> - 1.12.1-2
- Fix typo in Source0

* Thu Mar 30 2017 Sarah Choi <sarahc@vmware.com> - 1.12.1-1
- Upgrade version to 1.12.1

* Thu Mar 02 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.8.2-1
- Initial packaging for Photon
