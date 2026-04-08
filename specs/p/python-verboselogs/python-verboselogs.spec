# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname verboselogs

Name:           python-%{srcname}
Version:        1.7
Release:        31%{?dist}
Summary:        Verbose logging level for Python's logging module

License:        MIT
URL:            https://%{srcname}.readthedocs.io
Source0:        https://github.com/xolox/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

# Use unittest.mock instead of mock backport package
Patch0:         %{name}-1.7-mock.patch
# Use a more available sphinx theme - not submitted upstream
Patch1:         %{name}-1.7-sphinx-theme.patch

BuildArch:      noarch

%description
The verboselogs package extends Python's logging module to add the log levels
NOTICE, SPAM, SUCCESS and VERBOSE:

- The NOTICE level sits between the predefined WARNING and INFO levels.
- The SPAM level sits between the predefined DEBUG and NOTSET levels.
- The SUCCESS level sits between the predefined WARNING and ERROR levels.
- The VERBOSE level sits between the predefined INFO and DEBUG levels.

The code to do this is simple and short, but I still don't want to copy/paste it
to every project I'm working on, hence this package.


%package doc
Summary:        Documentation for the '%{srcname}' Python module
BuildRequires:  python%{python3_pkgversion}-sphinx

%description doc
HTML documentation for the '%{srcname}' Python module.


%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-setuptools
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%if 0%{?fedora} || 0%{?rhel} >= 8
Suggests:       %{name}-doc = %{version}-%{release}
%endif

%description -n python%{python3_pkgversion}-%{srcname}
The verboselogs package extends Python's logging module to add the log levels
NOTICE, SPAM, SUCCESS and VERBOSE:

- The NOTICE level sits between the predefined WARNING and INFO levels.
- The SPAM level sits between the predefined DEBUG and NOTSET levels.
- The SUCCESS level sits between the predefined WARNING and ERROR levels.
- The VERBOSE level sits between the predefined INFO and DEBUG levels.

The code to do this is simple and short, but I still don't want to copy/paste it
to every project I'm working on, hence this package.


%prep
%autosetup -p1


%build
%py3_build

# Don't install pylint.py or tests.py
rm build/lib/%{srcname}/{pylint,tests}.py

sphinx-build-%{python3_version} -nb html -d docs/build/doctrees docs docs/build/html
rm docs/build/html/.buildinfo


%install
%py3_install


%check
PYTHONUNBUFFERED=1 py.test-%{python3_version} %{srcname}/tests.py \
  -k 'not test_pylint_plugin'


%files doc
%license LICENSE.txt
%doc docs/build/html

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE.txt
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.7-31
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.7-30
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.7-28
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.7-25
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.7-21
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.7-18
- Rebuilt for Python 3.11

* Wed Apr 27 2022 Scott K Logan <logans@cottsay.net> - 1.7-17
- Drop pylint tests
- Use unittest.mock

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-15
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.7-14
- Rebuilt for Python 3.10

* Mon May 10 2021 Scott K Logan <logans@cottsay.net> - 1.7-13
- Improve astroid compatibility patch (rhbz#1958921)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7-10
- Rebuilt for Python 3.9

* Fri Feb 21 2020 Scott K Logan <logans@cottsay.net> - 1.7.8-9
- Drop unsupported comments from spec file
- Add weak dependency for EPEL 8

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7-7
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.7-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Mar 13 2019 Scott K Logan <logans@cottsay.net> - 1.7-4
- Drop python2 and python3_other
- Add patches for astroid and sphinx compatibility

* Fri Oct 26 2018 Scott K Logan <logans@cottsay.net> - 1.7-3
- Pattern conformance

* Fri Sep 28 2018 Scott K Logan <logans@cottsay.net> - 1.7-2
- Add setuptools dependency for EPEL

* Fri Sep 28 2018 Scott K Logan <logans@cottsay.net> - 1.7-1
- Initial package
