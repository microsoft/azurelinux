# Got the intial spec and patches from Fedora and modified the spec.
%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        Python bindings for PAM (Pluggable Authentication Modules).
Name:           PyPAM
Version:        0.5.0
Release:        8%{?dist}
License:        LGPLv2
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
# Note that the upstream URL is dead. Project seems to have been abandoned by authors.
Url:            http://www.pangalactic.org/PyPAM
Source0:        https://src.fedoraproject.org/repo/pkgs/%{name}/%{name}-%{version}.tar.gz/f1e7c2c56421dda28a75ace59a3c8871/%{name}-%{version}.tar.gz
Patch0:         PyPAM-dlopen.patch
Patch1:         PyPAM-0.5.0-dealloc.patch
Patch2:         PyPAM-0.5.0-nofree.patch
Patch3:         PyPAM-0.5.0-memory-errors.patch
Patch4:         PyPAM-0.5.0-return-value.patch
Patch5:         PyPAM-python3-support.patch

BuildRequires:  python2-devel
BuildRequires:  python2-libs
BuildRequires:  python-setuptools
BuildRequires:  pam-devel
BuildRequires:  python3
BuildRequires:  python3-devel
BuildRequires:  python3-libs

Requires:       python2
Requires:       python2-libs

%description
Python bindings for PAM (Pluggable Authentication Modules).

%package -n     python3-PyPAM
Summary:        python-PyPAM
Requires:       python3
Requires:       python3-libs

%description -n python3-PyPAM
Python 3 version.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
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
PATH=%{buildroot}%{_bindir}:${PATH} \
 PYTHONPATH=%{buildroot}%{python2_sitelib} \
python2 tests/PamTest.py
pushd ../p3dir
PATH=%{buildroot}%{_bindir}:${PATH} \
  PYTHONPATH=%{buildroot}%{python3_sitelib} \
python3 tests/PamTest.py
popd

%files
%defattr(-,root,root,-)
%license COPYING
%{python2_sitelib}/*

%files -n python3-PyPAM
%defattr(-,root,root,-)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:20:39 PST 2020 Nick Samson <nisamson@microsoft.com> - 0.5.0-8
- Added %%license line automatically

*   Tue Apr 28 2020 Emre Girgin <mrgirgin@microsoft.com> 0.5.0-7
-   Renaming Linux-PAM to pam
*   Mon Apr 27 2020 Nick Samson <nisamson@microsoft.com> 0.5.0-6
-   Updated Source0, License verified, %%define sha removed
*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 0.5.0-5
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Thu Jan 10 2019 Alexey Makhalov <amakhalov@vmware.com> 0.5.0-4
-   Added BuildRequires python2-devel.
-   Moved all buildRequires to the main package.
*   Thu Jun 22 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.5.0-3
-   Fix the check section
*   Wed May 31 2017 Dheeraj Shetty <dheerajs@vmware.com> 0.5.0-2
-   Changing python_sitelib to python2
*   Tue Apr 11 2017 Xiaolin Li <xiaolinl@vmware.com> 0.5.0-1
-   Initial packaging for Photon.
