# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname requests-toolbelt
%global altname requests_toolbelt

Name:           python-%{srcname}
Version:        1.0.0
Release: 15%{?dist}
Summary:        Utility belt for advanced users of python-requests

License:        Apache-2.0
URL:            https://toolbelt.readthedocs.io
Source0:        https://github.com/sigmavirus24/%{srcname}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
This is just a collection of utilities for python-requests, but don’t really\
belong in requests proper.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%py_provides    python3-%{altname}
BuildRequires:  python3-devel
BuildRequires:  python3-betamax
BuildRequires:  python3-pyOpenSSL
BuildRequires:  python3-pytest
BuildRequires:  python3-requests
Requires:       python3-requests

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -p1 -n toolbelt-%{version}

# https://fedoraproject.org/wiki/Changes/DeprecatePythonMock
sed -i -E -e 's/^(\s*)import mock/\1from unittest import mock/' \
          -e 's/^(\s*)from mock import /\1from unittest.mock import /' \
    tests/*.py tests/*/*.py


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files -l %{altname}

%check
%pyproject_check_import

# Disable tests that need network access and those which are currently failing
py.test-%{python3_version} -v --ignore=tests/test_x509_adapter.py \
       -k "not test_downloadutils and not test_dump and not test_sessions"


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst HISTORY.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.0-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.0-13
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jul 10 2025 Parag Nemade <pnemade AT redhat DOT com> - 1.0.0-11
- Convert a spec to use pyproject macros (rh#2378170)

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.0-10
- Rebuilt for Python 3.14

* Tue Jan 28 2025 Parag Nemade <pnemade AT redhat DOT com> - 1.0.0-9
- Disable tests that need network access (#2341206)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.0-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.0.0-2
- Rebuilt for Python 3.12

* Mon May 08 2023 Parag Nemade <pnemade AT redhat DOT com> - 1.0.0-1
- Update to 1.0.0 version (#2192400)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.10.1-2
- Update license tag to SPDX format

* Wed Oct 26 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.10.1-1
- Update to 0.10.1 version (#2137927)

* Tue Oct 11 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.10.0-1
- Update to 0.10.0 version (#2133011)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.9.1-18
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 06 2022 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-16
- Drop build dependency on deprecated python3-mock

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.1-14
- Rebuilt for Python 3.10

* Sat May 15 2021 Parag Nemade <pnemade AT redhat DOT com> - 0.9.1-13
- Disable some tests for Python 3.10 bootstrap process

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Oct 18 2020 Parag Nemade <pnemade AT redhat DOT com> - 0.9.1-11
- Ignore failing tests (rh#1863713)

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-10
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-8
- Rebuilt for Python 3.9

* Sat Apr 11 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 0.9.1-7
- run test suite in %%check

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 04 2019 Parag Nemade <pnemade AT redhat DOT com> - 0.9.1-2
- Remove python2 subpackage (#1696338)

* Thu Jan 31 2019 Parag Nemade <pnemade AT redhat DOT com> - 0.9.1-1
- Update to 0.9.1 version (#1670521)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun May 21 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.8.0-1
- Update to 0.8.0 version

* Mon Mar 20 2017 Parag Nemade <pnemade AT redhat DOT com> - 0.7.1-1
- Update to 0.7.1 version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.7.0-2
- Rebuild for Python 3.6

* Sun Jul 24 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.7.0-1
- Update to 0.7.0 (RHBZ #1359456)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 29 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.6.2-1
- Update to 0.6.2
- Add proper python2 subpackage
- Run tests properly
- Other fixes

* Mon May 09 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.6.1-1
- update to 0.6.1 release

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 28 2016 Parag Nemade <pnemade AT redhat DOT com> - 0.6.0-1
- update to 0.6.0 release

* Mon Dec 21 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.5.1-1
- update to 0.5.1 release

* Thu Nov 26 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.5.0-1
- update to 0.5.0 release

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 06 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.4.0-1
- update to 0.4.0 release

* Fri Feb 13 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.3.1-2
- Add missing LICENSE file

* Mon Feb 02 2015 Parag Nemade <pnemade AT redhat DOT com> - 0.3.1-1
- Initial packaging

