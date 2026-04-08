# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Enable tests by default.
%bcond_without  tests

%global modname vcrpy

Name:               python-%{modname}
Version:            7.0.0
Release:            6%{?dist}
Summary:            Automatically mock your HTTP interactions to simplify and speed up testing

License:            MIT
URL:                https://pypi.io/project/%{modname}
Source0:            %pypi_source %{modname}

BuildArch:          noarch

BuildRequires:      python3-devel

%if %{with tests}
BuildRequires:      python3dist(pytest)

# For checking imports.
# https://vcrpy.readthedocs.io/en/latest/installation.html
BuildRequires:      python3dist(aiohttp)
BuildRequires:      python3dist(boto3)
BuildRequires:      python3dist(httplib2)
BuildRequires:      python3dist(httpx)
BuildRequires:      python3dist(requests)
BuildRequires:      python3dist(tornado)
%endif

%global _description %{expand:
Simplify and speed up testing HTTP by recording all HTTP interactions and
saving them to "cassette" files, which are yaml files containing the contents
of your requests and responses.  Then when you run your tests again, they all
just hit the text files instead of the internet.  This speeds up your tests and
lets you work offline.

If the server you are testing against ever changes its API, all you need to do
is delete your existing cassette files, and run your tests again.  All of the
mocked responses will be updated with the new API.}

%description %{_description}

%package -n python3-%{modname}
Summary:            %{summary}

%description -n python3-%{modname} %{_description}


%prep
%autosetup -n %{modname}-%{version} -p1

# asyncio.iscoroutinefunction() is deprecated in Python 3.14 and will be removed
# in Python 3.16. Use inspect.iscoroutinefunction() instead
# Also sent upstream: https://github.com/kevin1024/vcrpy/pull/910
sed -i "s/from asyncio/from inspect/" vcr/cassette.py

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files vcr


%check
%pyproject_check_import

%if %{with tests}
# These tests make lots of outgoing connections, so we can't run them in
# the fedora buildsystem.
rm -rf tests/integration
# This test tries to contact google.com and fails in the fedora build system
rm -rf tests/unit/test_stubs.py
# Skip two tests that require DNS resolution
%pytest -k 'not test_get_vcr_with_matcher and not test_testcase_playback'
%endif


%files -n python3-%{modname} -f %{pyproject_files}
%doc README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.0.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.0.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 06 2025 Python Maint <python-maint@redhat.com> - 7.0.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 04 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 7.0.0-1
- update to 7.0.0. Fixes rhbz#2227609

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 5.0.0-5
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jul 06 2023 Major Hayden <major@redhat.com> - 5.0.0-1
- Update to 5.0.0

* Wed Jul 05 2023 Python Maint <python-maint@redhat.com> - 4.2.1-5
- Rebuilt for Python 3.12

* Tue Jul 04 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 4.2.1-4
- backport patch to fix test failures with Python 3.12: AttributeError: type
  object 'VCRHTTPConnection[…]' has no attribute 'debuglevel'

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 4.2.1-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 01 2022 Major Hayden <major@redhat.com> - 4.2.1-1
- new version

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Major Hayden <major@redhat.com> - 4.2.0-1
- Update to 4.2.0 rhbz#2102429
- Add pyproject_check_import

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.1.1-7
- Rebuilt for Python 3.11

* Fri Apr 22 2022 Major Hayden <major@mhtx.net> - 4.1.1-6
- Update spec to use pyproject-rpm-macros.

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.1.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 31 2020 Kevin Fenzi <kevin@scrye.com> - 4.1.1-1
- Update to 4.1.1. Fixes bug #1862531
- Enable at least the unit tests (integration tests do lots of network calls)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.2-2
- Rebuilt for Python 3.9

* Mon Mar 16 2020 Clément Verna <cverna@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2 Fixes bug 1768194

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 06 2019 Kevin Fenzi <kevin@scrye.com> - 2.1.0-1
- Update to 2.1.0. Fixes bug 1742605
- Enabled all tests in check.

* Wed Sep 04 2019 Miro Hrončok <mhroncok@redhat.com> - 1.13.0-5
- Subpackage python2-vcrpy has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.13.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jul 25 2018 Pierre-Yves Chibon <pingou@pingoured.fr> - 1.13.0
- Update to 1.13.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.11.1-4
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.11.1-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 15 2017 Kevin Fenzi <kevin@scrye.com> - 1.11.1-1
- Update to 1.11.1. Fixes bug #1447325

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.10.5-4
- Python 2 binary package renamed to python2-vcrpy
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 13 2017 Kevin Fenzi <kevin@scrye.com> - 1.10.5-1
- Update to 1.10.5. Fixes bug #1412604

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.10.4-2
- Rebuild for Python 3.6

* Fri Dec 16 2016 Ralph Bean <rbean@redhat.com> - 1.10.4-1
- new version

* Sun Oct 02 2016 Kevin Fenzi <kevin@scrye.com> - 1.10.3-1
- Update to 1.10.3. Fixes bug #1381102

* Sat Sep 17 2016 Kevin Fenzi <kevin@scrye.com> - 1.10.2-1
- Update to 1.10.2. Fixes bug #1376311

* Mon Sep 12 2016 Kevin Fenzi <kevin@scrye.com> - 1.10.1-1
- Update to 1.10.1.

* Fri Sep 09 2016 Kevin Fenzi <kevin@scrye.com> - 1.10.0-1
- Update to 1.10.0. Fixes bug #1370830

* Wed Jul 27 2016 Ralph Bean <rbean@redhat.com> - 1.9.0-1
- new version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 15 2016 Ralph Bean <rbean@redhat.com> - 1.8.0-1
- new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Oct 19 2015 Ralph Bean <rbean@redhat.com> - 1.7.4-1
- new version

* Wed Sep 16 2015 Ralph Bean <rbean@redhat.com> - 1.7.3-1
- new version

* Mon Jul 06 2015 Ralph Bean <rbean@redhat.com> - 1.6.0-1
- new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Ralph Bean <rbean@redhat.com> - 1.5.2-2
- Move python3 deps into the python3 subpackage.

* Sat May 16 2015 Ralph Bean <rbean@redhat.com> - 1.5.2-1
- new version

* Fri May 15 2015 Ralph Bean <rbean@redhat.com> - 1.5.1-1
- new version

* Wed May 06 2015 Ralph Bean <rbean@redhat.com> - 1.4.2-1
- Adjusted spec with feedback from package review.
- Fix original changelog entry.
- Fix directory ownership in the files section.
- Latest upstream.

* Sat Apr 11 2015 Ralph Bean <rbean@redhat.com> 1.4.0-1
- initial package for Fedora
