%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
	
%global srcname setuptools_scm

Summary:        The blessed package to manage your versions by scm tags.
Name:           python-%{srcname}
Version:        8.0.3
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Url:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://files.pythonhosted.org/packages/af/54/0a75c590c1aa1908c1036de783c0b7136d8fe4beb8ce4c52e4d92b9e9ca7/setuptools-scm-8.0.3.tar.gz

BuildArch:      noarch

BuildRequires:  python3-wheel
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  cmake
%if %{with_check}
BuildRequires:  git
%endif

%description
setuptools_scm handles managing your python package versions in scm metadata instead of declaring them as the version argument or in a scm managed file.

It also handles file finders for the supported scm’s.

%package -n     python3-%{srcname}
Summary:        python-setuptools_scm

BuildRequires:  python3-tomli

Requires:       python3
Requires:       python3-libs
Requires:       python3-packaging
Requires:       python3-pip
Requires:       python3-tomli

Provides:       %{name} = %{version}-%{release}

%description -n python3-%{srcname}
setuptools_scm handles managing your python package versions in scm metadata instead of declaring them as the version argument or in a scm managed file.

It also handles file finders for the supported scm’s.

%prep
%autosetup -n setuptools-scm-%{version}

%generate_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%if %{with_check}
%check
pip3 install tox tox-current-env
tox -e py%{python3_version_nodots}
%endif

%files -n python3-%{srcname}
%license LICENSE
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}.dist-info/INSTALLER
%{python3_sitelib}/%{srcname}-%{version}.dist-info/METADATA
%{python3_sitelib}/%{srcname}-%{version}.dist-info/LICENSE
%{python3_sitelib}/%{srcname}-%{version}.dist-info/WHEEL
%{python3_sitelib}/%{srcname}-%{version}.dist-info/entry_points.txt
%{python3_sitelib}/%{srcname}-%{version}.dist-info/top_level.txt
 

%changelog
* Wed Feb 21 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 8.0.3-1
- Auto-upgrade to 8.0.3 - 3.0 package upgrade

* Fri Feb 16 2024 Andrew Phelps <anphel@microsoft.com> - 6.4.2-2
- Add build requirement on python3-tomli to fix python 3.12 break

* Sun Mar 27 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 6.4.2-1
- Updating to version 6.4.2.
- Adding a dependency on 'python3-tomli'.
- Removing Python 2 version.

* Tue Feb 08 2022 Thomas Crain <thcrain@microsoft.com> - 3.1.0-4
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
