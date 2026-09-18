# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# We must break a circular test dependency on python-capturer to bootstrap a
# new Python version.
%bcond bootstrap 0
%bcond tests %{without bootstrap}

%global srcname humanfriendly

Name:           python-%{srcname}
Version:        10.0
Release:        19%{?dist}
Summary:        Human friendly output for text interfaces using Python

License:        MIT
URL:            https://%{srcname}.readthedocs.io
Source0:        https://github.com/xolox/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:      noarch

# Use unittest.mock instead of mock backport package
Patch0:         %{name}-10.0-mock.patch

# Replace pipes.quote with shlex.quote on Python 3
# https://github.com/xolox/python-humanfriendly/pull/75
#
# Fixes:
#
# module pipes is removed in python version 3.13 - Please use the subprocess
# module instead
# https://github.com/xolox/python-humanfriendly/issues/73
Patch1:         https://github.com/xolox/%{name}/pull/75.patch

# Do not import setup in the tests module
# https://github.com/xolox/python-humanfriendly/pull/65
#
# Fixes:
#
# test failures with pytest7: AttributeError: module 'humanfriendly.tests' has
# no attribute 'connect'
# https://github.com/xolox/python-humanfriendly/issues/64
Patch2:         https://github.com/xolox/%{name}/pull/65.patch

%description
The functions and classes in the humanfriendly package can be used to make text
interfaces more user friendly. Some example features:

- Parsing and formatting numbers, file sizes, pathnames and timespans in
  simple, human friendly formats.
- Easy to use timers for long running operations, with human friendly
  formatting of the resulting timespans.
- Prompting the user to select a choice from a list of options by typing the
  option's number or a unique substring of the option.
- Terminal interaction including text styling (ANSI escape sequences), user
  friendly rendering of usage messages and querying the terminal for its size.


%package doc
Summary:        Documentation for the '%{srcname}' Python module
BuildRequires:  python%{python3_pkgversion}-sphinx

%description doc
HTML documentation for the '%{srcname}' Python module.


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-capturer >= 2.1
BuildRequires:  python%{python3_pkgversion}-coloredlogs >= 2.0
BuildRequires:  python%{python3_pkgversion}-pytest
%endif

%if !0%{?rhel} || 0%{?rhel} >= 8
Suggests:       %{name}-doc = %{version}-%{release}
%endif

%description -n python%{python3_pkgversion}-%{srcname}
The functions and classes in the humanfriendly package can be used to make text
interfaces more user friendly. Some example features:

- Parsing and formatting numbers, file sizes, pathnames and timespans in
  simple, human friendly formats.
- Easy to use timers for long running operations, with human friendly
  formatting of the resulting timespans.
- Prompting the user to select a choice from a list of options by typing the
  option's number or a unique substring of the option.
- Terminal interaction including text styling (ANSI escape sequences), user
  friendly rendering of usage messages and querying the terminal for its size.


%prep
%autosetup -p1


%build
%py3_build

# Don't install the tests.py
rm build/lib/%{srcname}/tests.py

sphinx-build-%{python3_version} -nb html -d docs/build/doctrees docs docs/build/html
rm docs/build/html/.buildinfo


%install
%py3_install


%check
%if 0%{?with_tests}
PYTHONUNBUFFERED=1 py.test-%{python3_version} %{srcname}/tests.py
%else
%py3_check_import %{srcname}
%endif


%files doc
%license LICENSE.txt
%doc docs/build/html

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE.txt
%doc CHANGELOG.rst README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/
%{_bindir}/%{srcname}


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 10.0-19
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 10.0-18
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Python Maint <python-maint@redhat.com> - 10.0-16
- Bootstrap for Python 3.14.0b3 bytecode

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 10.0-15
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jun 12 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 10.0-12
- Patch for pipes module removal in Python 3.13 (fix RHBZ#2245647)
- At least do an import-only check when tests are disabled
- Fix and re-enable the tests
- Add a bootstrap conditional

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 10.0-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 10.0-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 10.0-4
- Rebuilt for Python 3.11

* Wed Apr 27 2022 Scott K Logan <logans@cottsay.net> - 10.0-3
- Use unittest.mock

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Sep 21 2021 Major Hayden <major@mhtx.net> - 10.0-1
- Update to 10.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 8.2-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 30 2020 Scott K Logan <logans@cottsay.net> - 8.2-1
- Update to 8.2 (rhbz#1825604)

* Fri May 29 2020 Scott K Logan <logans@cottsay.net> - 8.1-3
- Disable tests in rawhide (rhbz#1841722)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 8.1-2
- Rebuilt for Python 3.9

* Wed Apr 15 2020 Scott K Logan <logans@cottsay.net> - 8.1-1
- Update to 8.1 (#1798963)
- Enable tests by default

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.18-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.18-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Scott K Logan <logans@cottsay.net> - 4.18-1
- Update to 4.18
- Drop python2 and python3_other

* Fri Oct 26 2018 Scott K Logan <logans@cottsay.net> - 4.17-1
- Update to 4.17

* Fri Sep 28 2018 Scott K Logan <logans@cottsay.net> - 4.16.1-6
- Fix monotonic dependency for EPEL

* Mon Sep 24 2018 Scott K Logan <logans@cottsay.net> - 4.16.1-5
- Disable python2 for Fedora 30+
- Better conditionals in spec

* Fri Sep 21 2018 Scott K Logan <logans@cottsay.net> - 4.16.1-4
- Enable both python34 and python36 for EPEL

* Fri Sep 21 2018 Scott K Logan <logans@cottsay.net> - 4.16.1-3
- Switch EPEL to python36

* Fri Sep 21 2018 Scott K Logan <logans@cottsay.net> - 4.16.1-2
- Enable python34 builds for EPEL

* Thu Sep 20 2018 Scott K Logan <logans@cottsay.net> - 4.16.1-1
- Initial package
