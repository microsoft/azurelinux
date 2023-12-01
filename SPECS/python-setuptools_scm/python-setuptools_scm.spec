%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The blessed package to manage your versions by scm tags.
Name:           python-setuptools_scm
Version:        6.4.2
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Mariner
Url:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://files.pythonhosted.org/packages/source/s/setuptools_scm/setuptools_scm-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml

%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif

%description
setuptools_scm handles managing your python package versions in scm metadata instead of declaring them as the version argument or in a scm managed file.

It also handles file finders for the supported scm’s.

%package -n     python3-setuptools_scm
Summary:        python-setuptools_scm

Requires:       python3
Requires:       python3-libs
Requires:       python3-packaging
Requires:       python3-pip
Requires:       python3-tomli

Provides:       %{name} = %{version}-%{release}

%description -n python3-setuptools_scm
setuptools_scm handles managing your python package versions in scm metadata instead of declaring them as the version argument or in a scm managed file.

It also handles file finders for the supported scm’s.

%prep
%setup -q -n setuptools_scm-%{version}

%build
python3 setup.py build

%install
python3 setup.py install --prefix=%{_prefix} --root=%{buildroot}

%check
python3 setup.py test

%files -n python3-setuptools_scm
%defattr(-,root,root)
%{python3_sitelib}/*

%changelog
* Sun Mar 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.4.2-1
- Updating to version 6.4.2.
- Adding a dependency on 'python3-tomli'.
- Removing Python 2 version.

* Tue Feb 08 2022 Olivia Crain <oliviacrain@microsoft.com> - 3.1.0-4
- Remove unused `%%define sha1` lines
- License verified

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.1.0-3
- Added %%license line automatically

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.1.0-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Sun Sep 09 2018 Tapas Kundu <tkundu@vmware.com> - 3.1.0-1
- Update to version 3.1.0

* Wed Jun 07 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.15.0-2
- Add python3-setuptools and python3-xml to python3 sub package Buildrequires.

* Mon Mar 20 2017 Xiaolin Li <xiaolinl@vmware.com> - 1.15.0-1
- Initial packaging for Photon
