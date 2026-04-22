# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?python_enable_dependency_generator}

%global srcname pytest-multihost
%global modulename pytest_multihost
%global srcversion 3.0
%global versionedname %{srcname}-%{srcversion}

Name: python-%{srcname}
Version: %{srcversion}
Release: 32%{?dist}
Summary: Utility for writing multi-host tests for pytest

# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:       GPL-3.0-or-later
URL:           https://github.com/encukou/pytest-multihost
Source0:       %{url}/archive/v%{srcversion}/%{versionedname}.tar.gz

BuildArch:     noarch

%description
Allows pytest tests to run commands on several machines.
The machines to run on are described on the command line, the tests
specify how many machines they need and commands/checks to run on them.


%package -n python3-%{srcname}
Summary: Utility for writing multi-host tests for pytest
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-pytest
# These are not *strictly* required, but are part of the default workflow.
Recommends:    python%{python3_version}dist(pyyaml)
Recommends:    python%{python3_version}dist(paramiko)

%description -n python3-%{srcname}
Allows pytest tests to run commands on several machines.
The machines to run on are described on the command line, the tests
specify how many machines they need and commands/checks to run on them.

%prep
%autosetup -n %{versionedname}

%build
%py3_build

%check
# Do not run the test that needs passwordless SSH to localhost set up
%{__python3} -m pytest -m "not needs_ssh"

%install
%py3_install

%files -n python3-%{srcname}
%license COPYING
%doc README.rst
%{python3_sitelib}/%{modulename}-*.egg-info/
%{python3_sitelib}/%{modulename}/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.0-31
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.0-30
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.0-28
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 3.0-26
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.0-24
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.0-20
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0-17
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.0-14
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.0-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0-5
- Remove python2 subpackage

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 3.0-3
- Modernize spec

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0-2
- Rebuilt for Python 3.7

* Fri Mar 02 2018 Petr Viktorin <encukou@gmail.com> - 3.0-1
- Update to upstream 3.0:
  Do not add extra newlines to stdin contents
  Remove forgotten debug print

* Mon Feb 12 2018 Petr Viktorin <encukou@gmail.com> - 2.0-1
- Update to upstream 2.0:
  Add support to run commands in background
  Fix several issues around quoting, background processes, and encoding
- Add Recommends: for PyYAML and Paramiko to the py3 package

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Dec 01 2017 Iryna Shcherbina <ishcherb@redhat.com> - 1.1-9
- Fix ambiguous Python 2 dependencies declarations
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Oct 31 2017 Troy Dawson <tdawson@redhat.com> - 1.1-8
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 28 2017 Petr Viktorin <encukou@gmail.com> - 1.1-6
- Rename "python-pytest-multihost" package to "python2-pytest-multihost"

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Apr 22 2016 Petr Viktorin <encukou@gmail.com> - 1.1-1
- Much improved support for Windows hosts (thanks to Niranjan MR)

* Thu Mar 03 2016 Petr Viktorin <encukou@gmail.com> - 1.0-1
- Add error handling in config file handling (thanks to Abhijeet Kasurde)
- Add support to specify username/password per host (thanks to Niranjan MR)
- Add ability to reset the SSH connection (thanks to Scott Poore)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 26 2015 Petr Viktorin <encukou@gmail.com> - 0.9-1
- Add more file manipulation functions (thanks to Abhijeet Kasurde)
- Slightly improve Python 3 support

* Tue Nov 10 2015 Petr Viktorin <encukou@gmail.com> - 0.8-1
- Fix creating multiple Configs from one dict

* Tue Nov 10 2015 Petr Viktorin <encukou@gmail.com> - 0.7-1
- Add compatibility with Python 2.6

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 27 2015 Petr Viktorin <encukou@gmail.com> - 0.6-2
- Also install COPYING as a license on the Python 3 version

* Mon Jan 26 2015 Petr Viktorin <encukou@gmail.com> - 0.6-1
- Run tests
- Install COPYING as a license

* Wed Nov 26 2014 Petr Viktorin <encukou@gmail.com> - 0.5-1
- Packaging fixes

* Wed Nov 26 2014 Petr Viktorin <encukou@gmail.com> - 0.4-2
- Specify minimum version of pytest

* Wed Nov 26 2014 Petr Viktorin <encukou@gmail.com> - 0.4-1
- Ensure backwards compatibility with FreeIPA's root-only logins

* Wed Nov 26 2014 Petr Viktorin <encukou@gmail.com> - 0.3-1
- "Upstream" packaging fixes

* Mon Nov 10 2014 Petr Viktorin <encukou@gmail.com> - 0.2-1
- better extensibility
- bug fixes

* Mon Nov 10 2014 Petr Viktorin <encukou@gmail.com> - 0.1-1
- initial public version of package
