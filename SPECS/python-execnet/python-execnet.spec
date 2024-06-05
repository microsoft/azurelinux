%define pkgname execnet
Summary:        Python execution distributor
Name:           python-%{pkgname}
Version:        2.1.1
Release:        1%{?dist}
License:        MIT
URL:            https://codespeak.net/execnet/
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Source0:        https://pypi.io/packages/source/e/%{pkgname}/%{pkgname}-%{version}.tar.gz
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-hatchling
BuildRequires:  python%{python3_pkgversion}-hatch-vcs
BuildRequires:  python%{python3_pkgversion}-pathspec
BuildRequires:  python%{python3_pkgversion}-pluggy
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools_scm
BuildRequires:  python%{python3_pkgversion}-sphinx
BuildRequires:  python%{python3_pkgversion}-trove-classifiers
BuildRequires:  python%{python3_pkgversion}-wheel
%if %{with check}
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-pytest
%endif
BuildArch:      noarch

%description
Python execution distributor

%package -n python%{python3_pkgversion}-%{pkgname}
Summary:        Python execution distributor
Requires:       python%{python3_pkgversion}

%description -n python%{python3_pkgversion}-%{pkgname}
execnet provides carefully tested means to ad-hoc interact with Python
interpreters across version, platform and network barriers. It provides
a minimal and fast API targetting the following uses:

-distribute tasks to local or remote processes
-write and deploy hybrid multi-process applications
-write scripts to administer multiple hosts}

%prep
%autosetup -n %{pkgname}-%{version}

find . -type f -a \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;

%pyproject_buildrequires -t

%build
%pyproject_wheel
make -C doc html PYTHONPATH=$(pwd)/src
# remove hidden file
rm doc/_build/html/.buildinfo
 
%install
%pyproject_install
%pyproject_save_files %{pkgname}

%check
pip3 install tox iniconfig
# sed -i "s/pytest$/pytest==7.1.3/" tox.ini
LANG=en_US.UTF-8 tox -e py%{python3_version_nodots}

%files -n python%{python3_pkgversion}-%{pkgname} -f %{pyproject_files}
%doc README.rst
%doc doc/_build/html
%license %{python3_sitelib}/%{pkgname}-%{version}.dist-info/licenses/LICENSE

%changelog
* Wed Apr 24 2024 Osama Esmail <osamaesmail@microsoft.com> - 2.1.1-1
- Auto-upgrade to 2.1.1
- Replacing most of the %%py3... with %%pyproject...
- Redoing %%check section as well

* Wed Oct 26 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.0-2
- Freezing 'pytest' test dependency to version 7.1.3.

* Wed Mar 30 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.9.0-1
- Upgrade to latest upstream version
- Lint spec

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.7.1-4
- Use `py%%{python3_version_nodots}` instead of harcoding `py39`

* Wed Feb 09 2022 Muhammad Falak <mwani@microsoft.com> - 1.7.1-3
- Use `py39` instead of `py37` as tox environment to enable ptest

* Tue Jun 08 2021 Andrew Phelps <anphel@microsoft.com> - 1.7.1-2
- Fix check tests

* Fri Aug 21 2020 Thomas Crain <thcrain@microsoft.com> - 1.7.1-1
- Original version for CBL-Mariner
- License verified
