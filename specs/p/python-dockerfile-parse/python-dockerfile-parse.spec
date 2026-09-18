# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_without tests

%global srcname dockerfile-parse
%global modname %(n=%{srcname}; echo ${n//-/_})

Name:           python-%{srcname}
Version:        2.0.1
Release:        11%{?dist}

Summary:        Python library for Dockerfile manipulation
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://github.com/containerbuildsystem/dockerfile-parse
Source0:        https://github.com/containerbuildsystem/dockerfile-parse/archive/%{version}.tar.gz

BuildArch:      noarch

%description
%{summary}.

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with tests}
BuildRequires:  python3-pytest
%endif

%description -n python3-%{srcname}
%{summary}.

Python 3 version.

%prep
%setup -q -n %{srcname}-%{version}


%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
export LANG=C.UTF-8
py.test-%{python3_version} -v tests
%endif

%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}/


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.0.1-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.0.1-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.0.1-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 2.0.1-6
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.1-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 Lukas Slebodnik <lslebodn@fedoraproject.org> - 2.0.1-1
- Automatic commit of package [python-dockerfile-parse] release [2.0.1-1]. (mkosiarc)
- fix(pylint): address broad-exception-raised (Martin Basti)
- fix(spec): remove six module (Martin Basti)
- Automatic commit of package [python-dockerfile-parse] release [2.0.0-1]. (mkosiarc)
- Extend support for py3.11 (Martin Basti)
- Extend testing to all supported python versions (Martin Basti)
- Remove test.sh (Martin Basti)
- GH workflows: Use tox in CI (Martin Basti)
- pylint: fix redundant-u-string-prefix (Martin Basti)
- Pylint: disable unspecified-encoding check (Martin Basti)
- pylint: disable consider-using-f-string check (Martin Basti)
- Add tox (Martin Basti)
- Remove six from tests (Martin Basti)
- Pylint: silence no-absolute-import (Martin Basti)
- Remove six module (Martin Basti)
- support only py3.6 and newer (Martin Basti)
- Drop Python2 support (Martin Basti)
- Bump actions/upload-artifact from 2 to 3 (dependabot[bot])
- flake8: Fix whitespace issue (Martin Basti)
- Automatic updates of GH actions with dependabot (Martin Basti)
- support --platform parameter in image_from (Tim van Katwijk)
- Add CodeQL workflow for GitHub code scanning (LGTM Migrator)
- Fix compatibility with pytest 7.2.0 (Lumír 'Frenzy' Balhar)
- pylint: fix unsupported-assignment-operation (Martin Basti)
- workflow: use checkout action version 3 (Martin Basti)
- Fix E741 ambiguous variable name 'l' (Adam Cmiel)
- Add necessary noqa directive to version_init.template (Ben Alkov)
- Automatic commit of package [python-dockerfile-parse] release [1.2.0-1]. (Robert Cerven)
- Avoid adding repos to from scratch with alias (Ladislav Kolacek)
- Update docstring (fixes #113) (Tim Waugh)
- Pin pip<21.0 for running tests with Python 2 (Chenxiong Qi)
- Replace f32 with f33 to run bandit and pylint (Chenxiong Qi)
- Fix coveralls 422 Client Error (Chenxiong Qi)
- Make the bandit action runnable with Python 2 (Chenxiong Qi)
- Replace f31 with f33 in CI workflow (Chenxiong Qi)
- Fix coverage collection in `test.sh` (Ben Alkov)
- addopts for pytest-html have to go in test.sh because of packit... ...(rpm specfile runs unit tests) (Ben Alkov)
- Add pytest.ini for pytest improvements (Ben Alkov)
- Silence remaining flake8 hits; mostly WS and wraps (Ben Alkov)
- Add GH workflows (Ben Alkov)
- Add new reqs for unit tests (Ben Alkov)
- Refactor test.sh (Ben Alkov)
- Update README badges (Ben Alkov)
- Remove unneeded config files (Ben Alkov)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.1.0-15
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.0-12
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.0-9
- Rebuilt for Python 3.10

* Mon Mar 08 2021 David Kirwan <dkirwan@redhat.com> - 1.1.0
- Updated python-dockerfile-parse to 1.1.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.13-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.13-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.13-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 12 2019 Athos Ribeiro <athoscr@fedoraproject.org> - 0.0.13-1
- New upstream release 0.0.13
- Require six for RHEL builds
- Do not build python2 packages for Fedora >= 30

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Tim Waugh <twaugh@redhat.com> - 0.0.11-3
- Require six

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Tim Waugh <twaugh@redhat.com> - 0.0.11-1
- New upstream release 0.0.11

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.0.10-2
- Rebuilt for Python 3.7

* Thu Apr 19 2018 Tomas Tomecek <ttomecek@redhat.com> - 0.0.10-1
- New upstream release 0.0.10

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Oct 05 2017 Tomas Tomecek <ttomecek@redhat.com> - 0.0.7-1
- new upstream release: 0.0.7

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.0.5-8
- Rebuild for Python 3.6

* Tue Dec 06 2016 Adam Miller <maxamillion@fedoraproject.org> - 0.0.5-7
- Patch to handle inheriting parent Dockerfile ENVs

* Wed Sep 07 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 0.0.5-6
- Modernize spec
- Trivial fixes

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov 06 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.5-2
- %%check section

* Mon Sep 21 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.5-1
- 0.0.5

* Thu Aug 27 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.4-1
- 0.0.4

* Tue Jun 30 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.3-2
- define macros for RHEL-6

* Fri Jun 26 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.3-1
- 0.0.3

* Fri Jun 26 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.2-1
- 0.0.2

* Thu Jun 18 2015 Jiri Popelka <jpopelka@redhat.com> - 0.0.1-1
- initial release
