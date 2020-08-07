%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        the blessed package to manage your versions by scm tags.
Name:           python-setuptools_scm
Version:        3.1.0
Release:        3%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://files.pythonhosted.org/packages/source/s/setuptools_scm/setuptools_scm-%{version}.tar.gz
%define sha1    setuptools_scm=cffffd63429761edece3957321a50fbdb364f043

BuildRequires:  python2
BuildRequires:  python2-libs
BuildRequires:  python2-devel
BuildRequires:  python-setuptools

Requires:       python2
Requires:       python2-libs

BuildArch:      noarch

%description
setuptools_scm handles managing your python package versions in scm metadata instead of declaring them as the version argument or in a scm managed file.

It also handles file finders for the supported scm’s.

%package -n     python3-setuptools_scm
Summary:        python-setuptools_scm
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

Requires:       python3
Requires:       python3-libs

%description -n python3-setuptools_scm
Python 3 version.

%prep
%setup -q -n setuptools_scm-%{version}
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
python2 setup.py test
pushd ../p3dir
python3 setup.py test
popd

%files
%defattr(-,root,root)
%license LICENSE
%{python2_sitelib}/*

%files -n python3-setuptools_scm
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sat May 09 00:21:33 PST 2020 Nick Samson <nisamson@microsoft.com> - 3.1.0-3
- Added %%license line automatically

*   Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 3.1.0-2
-   Initial CBL-Mariner import from Photon (license: Apache2).
*   Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> 3.1.0-1
-   Update to version 3.1.0
*   Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-2
-   Add python3-setuptools and python3-xml to python3 sub package Buildrequires.
*   Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> 1.15.0-1
-   Initial packaging for Photon
