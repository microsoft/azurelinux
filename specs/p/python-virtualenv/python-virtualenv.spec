## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 4;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond bootstrap 0
%bcond tests %{without bootstrap}

Name:           python-virtualenv
Version:        20.35.4
Release:        %autorelease
Summary:        Tool to create isolated Python environments

License:        MIT
URL:            http://pypi.python.org/pypi/virtualenv
Source:         %{pypi_source virtualenv}

# Add /usr/share/python-wheels to extra_search_dir
Patch:          rpm-wheels.patch

# Restore support for Python 3.6 virtual environments
Patch:          python3.6.patch

BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  fish
BuildRequires:  tcsh
BuildRequires:  gcc
# from the [test] extra, but manually filtered, version bounds removed
BuildRequires:  python3-flaky
BuildRequires:  python3-packaging
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-env
#BuildRequires: python3-pytest-freezer -- not available, tests skipped
BuildRequires:  python3-pytest-mock
BuildRequires:  python3-pytest-randomly
BuildRequires:  python3-pytest-timeout
BuildRequires:  python3-setuptools
BuildRequires:  python3-time-machine
%endif

# RPM installed wheels
BuildRequires:  %{python_wheel_pkg_prefix}-pip-wheel >= 25.1
BuildRequires:  %{python_wheel_pkg_prefix}-setuptools-wheel >= 70.1
# python-wheel-wheel is only used on Python 3.8 which is retired from Fedora 42+

%global _description %{expand:
virtualenv is a tool to create isolated Python environments.
A subset of it has been integrated into the Python standard library under
the venv module. The venv module does not offer all features of this library,
to name just a few more prominent:

- is slower (by not having the app-data seed method),
- is not as extendable,
- cannot create virtual environments for arbitrarily installed Python versions
  (and automatically discover these),
- does not have as rich programmatic API (describe virtual environments
  without creating them).}

%description %_description


%package -n     python3-virtualenv
Summary:        Tool to create isolated Python environments

# Provide "virtualenv" for convenience
Provides:       virtualenv = %{version}-%{release}

# RPM installed wheels
Requires:       %{python_wheel_pkg_prefix}-pip-wheel >= 25.1
# Python 3.12 virtualenvs are created without setuptools,
# but the users can still do --setuptools=bundle to force them:
Requires:       %{python_wheel_pkg_prefix}-setuptools-wheel >= 70.1
# This is only needed for Python 3.6 virtual environments
Requires:       (%{python_wheel_pkg_prefix}-wheel0.37-wheel if python3.6)

%description -n python3-virtualenv %_description


%prep
%autosetup -p1 -n virtualenv-%{version}

# Remove the wheels provided by RPM packages
rm src/virtualenv/seed/wheels/embed/pip-*
rm src/virtualenv/seed/wheels/embed/setuptools-*
rm src/virtualenv/seed/wheels/embed/wheel-*

test ! -f src/virtualenv/seed/embed/wheels/*.whl

# Replace hardcoded path from rpm-wheels.patch by %%{python_wheel_dir}
# On Fedora, this should change nothing, but when building for RHEL9+, it will
sed -i "s|/usr/share/python-wheels|%{python_wheel_dir}|" src/virtualenv/util/path/_system_wheels.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l virtualenv

%check
%pyproject_check_import -e '*activate_this' -e '*windows*'
%if %{with tests}
# Skip tests which requires internet or some extra dependencies
# Requires internet:
# - test_download_*
# - test_can_build_c_extensions
# - test_create_distutils_cfg
# Uses disabled functionalities around bundled wheels:
# - test_wheel_*
# - test_seed_link_via_app_data
# - test_base_bootstrap_via_pip_invoke
# - test_acquire.py (whole file)
# - test_bundle.py (whole file)
# Uses disabled functionalities around automatic updates:
# - test_periodic_update.py (whole file)
# We don't run the tests in an active virtual environment
# https://github.com/pypa/virtualenv/issues/2939#issuecomment-3384554583
# - test_py_info_cache_clear
PIP_CERT=/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
%pytest -vv -k "not test_bundle and \
                not test_acquire and \
                not test_periodic_update and \
                not test_wheel_ and \
                not test_download_ and \
                not test_can_build_c_extensions and \
                not test_base_bootstrap_via_pip_invoke and \
                not test_seed_link_via_app_data and \
                not test_py_info_cache_clear and \
                not test_create_distutils_cfg"
%endif

%files -n python3-virtualenv -f %{pyproject_files}
%doc README.md
%{_bindir}/virtualenv

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 20.35.4-4
- Latest state for python-virtualenv

* Fri Jan 09 2026 Miro Hrončok <miro@hroncok.cz> - 20.35.4-3
- Restore support for Python 3.6 virtual environments
- Fixes: rhbz#2427756

* Thu Oct 30 2025 Lumir Balhar <lbalhar@redhat.com> - 20.35.4-2
- Switch python3.9 → python3.9-devel in CI

* Wed Oct 29 2025 Lumir Balhar <lbalhar@redhat.com> - 20.35.4-1
- Update to 20.35.4 (rhbz#2406997)

* Sat Oct 11 2025 Lumir Balhar <lbalhar@redhat.com> - 20.35.3-1
- Update to 20.35.3 (rhbz#2403131)

* Fri Oct 10 2025 Lumir Balhar <lbalhar@redhat.com> - 20.35.2-1
- Update to 20.35.2 (rhbz#2403131)

* Fri Oct 10 2025 Lumir Balhar <lbalhar@redhat.com> - 20.35.1-1
- Update to 20.35.1 (rhbz#2402968)

* Thu Oct 09 2025 Lumir Balhar <lbalhar@redhat.com> - 20.35.0-1
- Update to 20.35.0 (rhbz#2402601)

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 20.34.0-3
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Aug 18 2025 Lumir Balhar <lbalhar@redhat.com> - 20.34.0-2
- Re-enable fixed tests

* Sun Aug 17 2025 Lumir Balhar <lbalhar@redhat.com> - 20.34.0-1
- Update to 20.34.0 (rhbz#2388237)

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 20.33.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Aug 06 2025 Lumir Balhar <lbalhar@redhat.com> - 20.33.1-1
- Update to 20.33.1 (rhbz#2382211)

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20.31.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jul 08 2025 Miro Hrončok <miro@hroncok.cz> - 20.31.2-4
- Use /etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem for tests
- https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 20.31.2-3
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 20.31.2-2
- Bootstrap for Python 3.14

* Mon May 12 2025 Miro Hrončok <miro@hroncok.cz> - 20.31.2-1
- Update to 20.31.2
- Fixes: rhbz#2365142

* Tue May 06 2025 Miro Hrončok <miro@hroncok.cz> - 20.31.1-1
- Update to 20.31.1
- Fixes: rhbz#2364255

* Mon May 05 2025 Miro Hrončok <miro@hroncok.cz> - 20.31.0-1
- Update to 20.31.0
- Removes the requirement for python-wheel-wheel
- Fixes: rhbz#2364149

* Wed Mar 12 2025 Lumir Balhar <lbalhar@redhat.com> - 20.29.3-2
- Drop Python 3.8 (retired from F42) from CI

* Wed Mar 12 2025 Lumir Balhar <lbalhar@redhat.com> - 20.29.3-1
- Update to 20.29.3 (rhbz#2350474)

* Sun Jan 19 2025 Lumir Balhar <lbalhar@redhat.com> - 20.29.1-1
- Update to 20.29.1 (rhbz#2338371)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 20.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Miro Hrončok <miro@hroncok.cz> - 20.28.1-1
- Update to 20.28.1
- Fixes: rhbz#2319571
- Fixes: rhbz#2331351

* Tue Nov 26 2024 Miro Hrončok <miro@hroncok.cz> - 20.26.6-2
- Amend a fix for --download with old Pythons not to break --seeder pip
  with new Pythons

* Mon Oct 14 2024 Miro Hrončok <miro@hroncok.cz> - 20.26.6-1
- Update to 20.26.6
- Fixes: rhbz#2188155
- Removes support for Python 2.7 virtual environments
- Removes support for Python 3.6 virtual environments

* Tue Oct 08 2024 Lumir Balhar <lbalhar@redhat.com> - 20.21.1-25
- Make tests with Python 2.7 optional

* Tue Oct 08 2024 Lumir Balhar <lbalhar@redhat.com> - 20.21.1-24
- Prevent command injection by quoting template strings in activation
  scripts

* Thu Aug 08 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 20.21.1-22
- Backport a builtin interpreter discovery fix

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20.21.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 20.21.1-20
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 20.21.1-19
- Bootstrap for Python 3.13

* Tue Apr 16 2024 Karolina Surma <ksurma@redhat.com> - 20.21.1-18
- Update Python 3.13 compat patch: 3.13.0a6 renamed pathmod to parser

* Thu Apr 11 2024 Lumir Balhar <lbalhar@redhat.com> - 20.21.1-17
- Fix compatibility with pytest 8

* Thu Apr 04 2024 Miro Hrončok <miro@hroncok.cz> - 20.21.1-13
- When getting wheels for /usr/bin/python3 interpreter, look for them in
  proper directories
- Fixes: rhbz#2272958

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20.21.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 20.21.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Dec 04 2023 Lumír Balhar <lbalhar@redhat.com> - 20.21.1-7
- Fix compatibility with Python 3.13
Resolves: rhbz#2251781

* Thu Nov 23 2023 Lumír Balhar <lbalhar@redhat.com> - 20.21.1-6
- Allow platformdirs version 4

* Wed Aug 30 2023 Miro Hrončok <mhroncok@redhat.com> - 20.21.1-5
- Fix tests with pluggy 1.2.0+

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20.21.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 20.21.1-3
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 20.21.1-2
- Bootstrap for Python 3.12

* Fri Apr 28 2023 Miro Hrončok <mhroncok@redhat.com> - 20.21.1-1
- Update to 20.21.1
- Backport from 20.23.0: Don't install setuptools and wheel to Python 3.12+ environments

* Mon Mar 13 2023 Lumír Balhar <lbalhar@redhat.com> - 20.21.0-1
- Update to 20.21.0 (rhbz#2177543)

* Mon Mar 06 2023 Miro Hrončok <mhroncok@redhat.com> - 20.20.0-2
- Fix build with pyproject-rpm-macros >= 1.6.3
- Local workaround collided with the fix there

* Wed Mar 01 2023 Lumír Balhar <lbalhar@redhat.com> - 20.20.0-1
- Update to 20.20.0 (rhbz#2174221)

* Thu Feb 09 2023 Lumír Balhar <lbalhar@redhat.com> - 20.19.0-1
- Update to 20.19.0 (rhbz#2167499)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 20.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 12 2022 Miro Hrončok <mhroncok@redhat.com> - 20.17.1-2
- Require python-wheel0.37-wheel for older Pythons

* Wed Dec 07 2022 Lumír Balhar <lbalhar@redhat.com> - 20.17.1-1
- Update to 20.17.1 (rhbz#2151044)

* Thu Dec 01 2022 Lumír Balhar <lbalhar@redhat.com> - 20.17.0-1
- Update to 20.17.0 (rhbz#2148907)

* Mon Nov 14 2022 Lumír Balhar <lbalhar@redhat.com> - 20.16.7-1
- Update to 20.16.7 (#2142311)

* Thu Oct 27 2022 Lumír Balhar <lbalhar@redhat.com> - 20.16.6-1
- Update to 20.16.6
Resolves: rhbz#2137713

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 29 2022 Lumír Balhar <lbalhar@redhat.com> - 20.15.1-1
- Update to 20.15.1
Resolves: rhbz#2101975

* Sun Jun 26 2022 Lumír Balhar <lbalhar@redhat.com> - 20.15.0-1
- Update to 20.15.0
Resolves: rhbz#2101126

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 20.13.4-4
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 20.13.4-3
- Bootstrap for Python 3.11

* Mon Jun 06 2022 Lumír Balhar <lbalhar@redhat.com> - 20.13.4-2
- Improve compatibility with Python 3.11
Resolves: rhbz#2093193

* Mon Mar 21 2022 Lumír Balhar <lbalhar@redhat.com> - 20.13.4-1
- Update to 20.13.4
Resolves: rhbz#2065839

* Mon Mar 14 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 20.13.3-3
- BR tcsh so we can test csh activation scripts

* Mon Mar 14 2022 Lumír Balhar <lbalhar@redhat.com> - 20.13.3-2
- Add explicit error when embed version of wheels is requested
Resolves: rhbz#2053948

* Tue Mar 08 2022 Lumír Balhar <lbalhar@redhat.com> - 20.13.3-1
- Update to 20.13.3
Resolves: rhbz#2061449

* Fri Feb 25 2022 Lumír Balhar <lbalhar@redhat.com> - 20.13.2-1
- Update to 20.13.2
Resolves: rhbz#2058146

* Sun Feb 06 2022 Lumír Balhar <lbalhar@redhat.com> - 20.13.1-1
- Update to 20.13.1
Resolves: rhbz#2051025

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 20.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Jan 03 2022 Lumír Balhar <lbalhar@redhat.com> - 20.13.0-1
- Update to 20.13.0
Resolves: rhbz#2035895

* Mon Nov 08 2021 Lumír Balhar <lbalhar@redhat.com> - 20.10.0-2
- Remove hack for local/ prefixes

* Tue Nov 02 2021 Lumír Balhar <lbalhar@redhat.com> - 20.10.0-1
- Update to 20.10.0
Resolves: rhbz#2019116

* Mon Oct 25 2021 Lumír Balhar <lbalhar@redhat.com> - 20.9.0-1
- Update to 20.9.0
Resolves: rhbz#2016758

* Wed Oct 06 2021 Lumír Balhar <lbalhar@redhat.com> - 20.8.1-1
- Update to 20.8.1
Resoves: rhbz#2007595

* Wed Oct 06 2021 Miro Hrončok <mhroncok@redhat.com> - 20.7.2-2
- Remove /local/ part from virtualenv paths
Resolves: rhbz#2011455

* Mon Aug 16 2021 Lumír Balhar <lbalhar@redhat.com> - 20.7.2-1
- Update to 20.7.2
Resolves: rhbz#1991618

* Sun Aug 01 2021 Lumír Balhar <lbalhar@redhat.com> - 20.7.0-1
- Update to 20.7.0
Resolves: rhbz#1988721

* Wed Jul 21 2021 Lumír Balhar <lbalhar@redhat.com> - 20.6.0-1
- Update to 20.6.0
Resolves: rhbz#1981792

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 20.4.7-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 20.4.7-2
- Bootstrap for Python 3.10

* Tue May 25 2021 Lumír Balhar <lbalhar@redhat.com> - 20.4.7-1
- Update to 20.4.7
Resolves: rhbz#1964115

* Wed Apr 21 2021 Lumír Balhar <lbalhar@redhat.com> - 20.4.4-1
- Update to 20.4.4
  Resolves: rhbz#1951515

* Wed Mar 17 2021 Lumír Balhar <lbalhar@redhat.com> - 20.4.3-1
- Update to 20.4.3
Resolves: rhbz#1939428

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 20.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Lumír Balhar <lbalhar@redhat.com> - 20.4.0-1
- Update to 20.4.0 (#1915682)

* Tue Jan 12 2021 Lumír Balhar <lbalhar@redhat.com> - 20.3.0-1
- Update to 20.3.0 (#1914641)

* Mon Nov 23 2020 Lumír Balhar <lbalhar@redhat.com> - 20.2.1-1
- Update to 20.2.1 (#1900253)

* Wed Nov 18 2020 Lumír Balhar <lbalhar@redhat.com> - 20.1.0-1
- Update to 20.1.0 (#1891297)

* Fri Oct 02 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0.32-1
- Update to 20.0.32 (#1884449)

* Thu Sep 03 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0.31-1
- Update to 20.0.31 (#1869352)

* Thu Aug 06 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0.30-1
- Update to 20.0.30 (#1862562)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 20.0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Miro Hrončok <mhroncok@redhat.com> - 20.0.28-1
- Update to 20.0.28
- Fixes rhbz#1860272

* Thu Jul 23 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0.27-1
- Update to 20.0.27 (#1854551)

* Tue Jun 23 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0.25-1
- Update to 20.0.25

* Mon Jun 15 2020 Lumír Balhar <lbalhar@redhat.com> - 20.0.23-1
- Update to 20.0.23 (#1742034)

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 16.7.10-2
- Rebuilt for Python 3.9

* Tue Feb 25 2020 Miro Hrončok <mhroncok@redhat.com> - 16.7.10-1
- Update to 16.7.10
- Explicitly require setuptools < 44 with Python 3.4

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 16.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 03 2019 Miro Hrončok <mhroncok@redhat.com> - 16.7.3-2
- Prefer wheels bundled in Python's ensurepip module over the RPM built ones
- This allows continuing support for Python 3.4 in Fedora 32+

* Wed Aug 21 2019 Charalampos Stratakis <cstratak@redhat.com> - 16.7.3-1
- Update to 16.7.3 (#1742034)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 16.6.1-3
- Rebuilt for Python 3.8

* Mon Jul 29 2019 Miro Hrončok <mhroncok@redhat.com> - 16.6.1-2
- Drop python2-virtualenv

* Thu Jul 11 2019 Miro Hrončok <mhroncok@redhat.com> - 16.6.1-1
- Update to 16.6.1 (#1699031)
- No more Python 2.6 or Jython support
- Drop runtime dependency on pythonX-devel

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Dec 13 2018 Miro Hrončok <mhroncok@redhat.com> - 16.0.0-6
- Don't fail on missing certifi's cert bundle (#1655253)

* Wed Aug 15 2018 Miro Hrončok <mhroncok@redhat.com> - 16.0.0-5
- Use wheels from RPM packages
- Put wheels needed for Python 2.6 into a subpackage
- Only have one /usr/bin/virtualenv (#1599422)
- Provide "virtualenv" (#1502670)

* Wed Jul 18 2018 Miro Hrončok <mhroncok@redhat.com> - 16.0.0-4
- Reintroduce support for Python 2.6 (#1602347)
- Add missing bundled provides

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 16.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 16.0.0-2
- Rebuilt for Python 3.7

* Thu May 17 2018 Steve Milner <smilner@redhat.com> - 16.0.0-1
- Updated for upstream release.

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 15.1.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 15.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 15.1.0-3
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 12 2017 Steve Milner <smilner@redhat.com> - 15.1.0-1
- Update to 15.1.0 per https://bugzilla.redhat.com/show_bug.cgi?id=1454962

* Fri Feb 17 2017 Michal Cyprian <mcyprian@redhat.com> - 15.0.3-6
- Check if exec_dir exists before listing it's content during venv create process

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 15.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan  4 2017 Steve Milner <smilner@redhat.com> - 15.0.3-4
- Updated version binaries per discussion at bz#1385240.

* Tue Dec 13 2016 Stratakis Charalampos <cstratak@redhat.com> - 15.0.3-3
- Rebuild for Python 3.6

* Mon Oct 17 2016 Steve Milner <smilner@redhat.com> - 15.0.3-2
- Added MAJOR symlinks per bz#1385240.

* Mon Aug  8 2016 Steve Milner <smilner@redhat.com> - 15.0.3-1
- Update for upstream release.

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 14.0.6-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Feb 21 2016 Orion Poplawski <orion@cora.nwra.com> - 14.0.6-1
- Update to 14.0.6

* Tue Feb 2 2016 Orion Poplawski <orion@cora.nwra.com> - 13.1.2-4
- Modernize spec
- Fix python3 package file ownership

* Wed Dec 2 2015 Orion Poplawski <orion@cora.nwra.com> - 13.1.2-3
- Move documentation to separate package (bug #1219139)

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 13.1.2-2
- Rebuilt for Python3.5 rebuild

* Mon Aug 24 2015 Steve Milner <smilner@redhat.com> - 13.1.2-1
- Update for upstream release.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 16 2015 Matej Stuchlik <mstuchli@redhat.com> - 12.0.7-1
- Update to 12.0.7

* Thu Jan 15 2015 Matthias Runge <mrunge@redhat.com> - 1.11.6-2
- add a python3-package, thanks to Matej Stuchlik (rhbz#1179150)

* Wed Jul 09 2014 Matthias Runge <mrunge@redhat.com> - 1.11.6-1
- update to 1.11.6:
  Upstream updated setuptools to 3.6, updated pip to 1.5.6

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Aug 15 2013 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.10.1-1
- Upstream upgraded pip to v1.4.1
- Upstream upgraded setuptools to v0.9.8 (fixes CVE-2013-1633)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.1-1
- Update to upstream 1.9.1 because of security issues with the bundled
  python-pip in older releases.  This is just a quick fix until a
  python-virtualenv maintainer can unbundle the python-pip package
  see: https://bugzilla.redhat.com/show_bug.cgi?id=749378

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Aug 14 2012 Steve Milner <me@stevemilner.org> - 1.7.2-1
- Update for upstream bug fixes.
- Added path for versioned binary.
- Patch no longer required.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.7.1.2-1
- Update for upstream bug fixes.
- Added patch for sphinx building

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 20 2011 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.7-1
- Update for https://bugzilla.redhat.com/show_bug.cgi?id=769067

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Oct 16 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.5.1-1
- Added _weakrefset requirement for Python 2.7.1.
- Add support for PyPy.
- Uses a proper temporary dir when installing environment requirements.
- Add --prompt option to be able to override the default prompt prefix.
- Add fish and csh activate scripts.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul  7 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.8-3
- Fixed EPEL installation issue from BZ#611536

* Wed Jun  9 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.8-2
- Only replace the python shebang on the first line (Robert Buchholz)

* Wed Apr 28 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.8-1
- update pip to 0.7
- move regen-docs into bin/
- Fix #31, make activate_this.py work on Windows (use Lib/site-packages)
unset PYTHONHOME envioronment variable -- first step towards fixing the PYTHONHOME issue; see e.g. https://bugs.launchpad.net/virtualenv/+bug/290844
- unset PYTHONHOME in the (Unix) activate script (and reset it in deactivate())
- use the activate.sh in virtualenv.py via running bin/rebuild-script.py
- add warning message if PYTHONHOME is set

* Fri Apr 2 2010 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.6-1
- allow script creation without setuptools
- fix problem with --relocate when bin/ has subdirs (fixes #12)
- Allow more flexible .pth file fixup
- make nt a required module, along with posix. it may not be a builtin module on jython
- don't mess with PEP 302-supplied __file__, from CPython, and merge in a small startup optimization for Jython, from Jython

* Tue Dec 22 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.3-1
- Updated for upstream release.

* Thu Nov 12 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.4.2-1
- Updated for upstream release.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 28 2009 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.3-1
- Updated for upstream release.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 25 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.2-1
- Updated for upstream release.

* Thu Dec 04 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.1-4
- Rebuild for Python 2.6

* Mon Dec  1 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-3
- Added missing dependencies.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.3.1-2
- Rebuild for Python 2.6

* Fri Nov 28 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3.1-1
- Updated for upstream release

* Sun Sep 28 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.3-1
- Updated for upstream release

* Sat Aug 30 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.2-1
- Updated for upstream release

* Fri Aug 29 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1-3
- Updated from review notes

* Thu Aug 28 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1-2
- Updated from review notes

* Tue Aug 26 2008 Steve 'Ashcrow' Milner <me@stevemilner.org> - 1.1-1
- Initial Version

## END: Generated by rpmautospec
