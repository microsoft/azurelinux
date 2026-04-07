# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global srcname tinycss2

Name:           python-%{srcname}
Version:        1.5.1
Release:        1%{?dist}
Summary:        Low-level CSS parser for Python

License:        BSD-3-Clause
URL:            https://www.courtbouillon.org/tinycss2/
Source0:        %{pypi_source tinycss2}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

# The test extra contains linters, we cherry-pick only what we need:
BuildRequires:  python3-pytest


%description
tinycss2 is a modern, low-level CSS parser for Python. tinycss2 is a rewrite of
tinycss with a simpler API, based on the more recent CSS Syntax Level 3
specification.


%package     -n python3-%{srcname}
Summary:        Low-level CSS parser for Python 3
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
tinycss2 is a modern, low-level CSS parser for Python. tinycss2 is a rewrite of
tinycss with a simpler API, based on the more recent CSS Syntax Level 3
specification.


%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install


%check
%{pytest}
# remove files which are only required for unit tests (including test.pyc/.pyo)
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/css-parsing-tests
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/test.py
rm -rf %{buildroot}%{python3_sitelib}/%{srcname}/__pycache__/test.*.py?


%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}.dist-info/


%changelog
* Sun Nov 23 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 1.5.1-1
- update to 1.5.1

* Wed Nov 19 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 1.5.0-1
- update to 1.5.0

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.4.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.4.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.4.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Oct 26 2024 Felix Schwarz <fschwarz@fedoraproject.org> - 1.4.0-1
- update to 1.4.0

* Sat Oct 26 2024 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3.0-5
- SPDX conversion

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.3.0-4
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.3.0-2
- Rebuilt for Python 3.13

* Tue Apr 23 2024 Felix Schwarz <fschwarz@fedoraproject.org> - 1.3.0-1
- update to 1.3.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 1.2.1-4
- Rebuilt for Python 3.12

* Mon May 15 2023 Miro Hrončok <mhroncok@redhat.com> - 1.2.1-3
- Drop redundant build dependency on flit, this package uses flit-core

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Oct 18 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 1.2.1-1
- update to 1.2.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.1-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 22 2021 Felix Schwarz <fschwarz@fedoraproject.org> - 1.1.1-1
- update to 1.1.1

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Nov 07 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 1.1.0-1
- update to 1.1.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 25 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 1.0.2-7
- add python3-setuptools to BuildRequires

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 29 2019 Felix Schwarz <fschwarz@fedoraproject.org> 1.0.2-1
- update to new upstream version 1.0.2

* Thu Mar 07 2019 Felix Schwarz <fschwarz@fedoraproject.org> 1.0.1-1
- update to new upstream version

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Felix Schwarz <fschwarz@fedoraproject.org> - 0.6.1-7
- remove even more Python 2 leftovers

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.6.1-6
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Dec 16 2017 Felix Schwarz <fschwarz@fedoraproject.org> 0.6.1-2
- remove also generated bytecode for test.py in Python 3
- more specific files specification

* Tue Dec 12 2017 Felix Schwarz <fschwarz@fedoraproject.org> 0.6.1-1
- initial package

