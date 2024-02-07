%{!?python2_sitelib: %define python2_sitelib %(python2 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}

Summary:        The blessed package to manage your versions by scm tags.
Name:           python-setuptools_scm
Version:        8.0.4
Release:        1%{?dist}
License:        MIT
Group:          Development/Languages/Python
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Url:            https://pypi.python.org/pypi/setuptools_scm
Source0:        https://github.com/pypa/setuptools_scm/archive/refs/tags/v%{version}.tar.gz#/setuptools_scm-%{version}.tar.gz

BuildArch:      noarch
 
BuildRequires:  python3-devel
BuildRequires:  python3-libs
BuildRequires:  python3-setuptools
BuildRequires:  python3-xml
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pyproject-rpm-macros
%if %{with tests}
BuildRequires:  git-core
# Don't pull mercurial into RHEL just to test this work with it
%if %{undefined rhel}
BuildRequires:  mercurial
%endif
# Manually listed test dependencies from tox.ini, to avoid pulling tox into RHEL
# Omit virtualenv, used only for test_distlib_setuptools_works skipped below (requires internet)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(setuptools) >= 45
%endif
 
%description
Setuptools_scm handles managing your Python package versions in SCM metadata.
It also handles file finders for the supported SCMs.
 
 
%package -n python%{python3_pkgversion}-setuptools_scm
Summary:        %{summary}
 
%description -n python%{python3_pkgversion}-setuptools_scm
Setuptools_scm handles managing your Python package versions in SCM metadata.
It also handles file finders for the supported SCMs.
 
 
%pyproject_extras_subpkg -n python%{python3_pkgversion}-setuptools_scm toml
 
 
%prep
%autosetup -p1 -n setuptools_scm-%{version}
# In case of a bootstrap loop between toml and setuptools_scm, do:
#   rm pyproject.toml
# That way, toml is not fetched to parse the file.
# That only works assuming the backend in the file remains the default backend.
 
 
%generate_buildrequires
%pyproject_buildrequires
 
%build
%pyproject_wheel
 
%install
%pyproject_install
%pyproject_save_files setuptools_scm
 
 
%if %{with tests}
%check
# Both of the skipped tests try to download from the internet
%pytest -v -k 'not test_pip_download and not test_distlib_setuptools_works'
%endif
 
 
%files -n python%{python3_pkgversion}-setuptools_scm -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Wed Feb 07 2024 Brian Fjeldstad <bfjelds@microsoft.com> - 8.0.4-1
- Updating to version 8.0.4.

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
