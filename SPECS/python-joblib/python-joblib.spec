%bcond_without check

%global srcname joblib

Summary:        Lightweight pipelining: using Python functions as pipeline jobs
Name:           python-%{srcname}
Version:        1.5.3
Release:        1%{?dist}
License:        BSD-3-Clause
URL:            https://joblib.readthedocs.io
Source0:        https://github.com/joblib/joblib/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

Patch:          joblib-unbundle-cloudpickle.patch

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
Joblib is a set of tools to provide lightweight pipelining in Python.
In particular, joblib offers:
 * transparent disk-caching of the output values and lazy
   re-evaluation (memorize pattern)
 * easy simple parallel computing
 * logging and tracing of the execution}

%description %_description

%package -n python3-%{srcname}
Summary: %{summary}

# Testing
%if %{with check}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist numpy}
BuildRequires:  %{py3_dist lz4}
BuildRequires:  %{py3_dist psutil} 
BuildRequires:  %{py3_dist threadpoolctl}
%endif

Recommends: %{py3_dist numpy}
Recommends: %{py3_dist lz4}
Recommends: %{py3_dist psutil} 
Provides: bundled(python3dist(loky)) = 3.5.5

%description -n python3-%{srcname} %_description

%prep
%autosetup -p1 -n %{srcname}-%{version}
rm -rf joblib/externals/cloudpickle/ 

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files joblib

%if %{with check}
%check
%pytest \
 --deselect "joblib/test/test_memory.py::test_parallel_call_cached_function_defined_in_jupyter" \
  joblib
%endif

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst

%changelog
* Thu Nov 13 2025 Henry Li <lihl@microsoft.com> - 1.5.3-1
- Initial Azure Linux import from Fedora 43 (license: MIT)
- License Verified

* Fri Sep 26 2025 Sergio Pascual <sergiopr@fedoraproject.org> - 1.5.2-1
- New upstream version 1.5.2

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.5.1-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.5.1-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.5.1-3
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Karolina Surma <ksurma@redhat.com> - 1.5.1-2
- Ensure compatibility with Python 3.14

* Thu May 29 2025 Karolina Surma <ksurma@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Tue Mar 11 2025 Miro Hrončok <miro@hroncok.cz> - 1.4.2-6
- Python 3.14 support
- Fixes: rhbz#2339519

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 26 2024 Sandro <devel@penguinpee.nl> - 1.4.2-4
- Apply patch for NumPy 2.x

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.4.2-2
- Rebuilt for Python 3.13

* Wed May 15 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 1.4.2-1
- New upstream 1.4.2

* Tue Apr 09 2024 Igor Raits <igor.raits@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Aug 28 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 1.3.2-1
- New upstream source 1.3.2
- Convert to SPDX

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 08 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 1.3.0-1
- New upstream source 1.3.0

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 1.2.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Sep 29 2022 Sergio Pascual <sergiopr@fedoraproject.org> - 1.2.0-1
- New upstream source 1.2.0. Fixes bz#2129824 CVE-2022-21797

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 20 2022 Python Maint <python-maint@redhat.com> - 1.1.0-5
- Rebuilt for Python 3.11

* Thu Jun 09 2022 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-4
- Unbundle cloudpickle to fix crashing tests with Python 3.11

* Sun Apr 24 2022 Sergio Pascual <sergiopr@fedoraproject.org> - 1.1.0-3
- Rewrite with new guidelines
- Avoid problematic test

* Sun Apr 24 2022 Sergio Pascual <sergiopr@fedoraproject.org> - 1.1.0-1
- New upstream source (1.1.0)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 11 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 1.0.1-5
- Add patch for broken test in 3.10
- Re-enable tests

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.1-4
- Rebuilt for Python 3.10

* Thu Feb 18 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 1.0.1-3
- Disable all tests for the moment

* Wed Feb 17 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 1.0.1-2
- Avoid failling test

* Tue Feb 09 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 1.0.1-1
- New upstream source (1.0.1)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 1.0.0-1
- New upstream source (1.0.0)

* Thu Nov 26 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.17.0-3
- New upstream source (0.17.0)
- Deselect test "test_parallel_call_cached_function_defined_in_jupyter"
- Deselect test "test_joblib_pickle_across_python_versions"
- Add sources

* Mon Sep 07 2020 Charalampos Stratakis <cstratak@redhat.com> - 0.16.0-3
- Add Python 3.9 compatibility
Resolves: rhbz#1871994

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jul 02 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.16.0-1
- New upstream source (0.16.0)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.15.1-3
- Rebuilt for Python 3.9

* Sun May 24 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.1-2
- Add python3-threadpoolctl as a build dependency

* Sat May 16 2020 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.15.1-1
- Update to 0.15.1 (#1836508)

* Fri May 15 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.0-1
- New upstream source (0.15.0)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Sep 10 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.13.2-5
- Backport all patches from upstream to fix python3.8 compat

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.2-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 11 2019 Sergio Pascual <sergiopr@fedoraproject.org> - 0.13.2-2
- New upstream source (0.13.2)
- Skip broken test "test_joblib_pickle_across_python_versions"
- Do no create pyc files during testing
- Unbundle cloudpickle

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 16 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.13.0-1
- Update to 0.13.0
- Drop python2 subpackage

* Fri Oct 05 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.12.5-1
- New upstream source (0.12.5)

* Sun Sep 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.12.3-1
- Update to 0.12.3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11-5
- Rebuilt for Python 3.7

* Tue Jun 05 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11-4
- Disable broken test (https://github.com/joblib/joblib/issues/691)
- Disable cache in pytest

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 11 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.11-1
- Update to 0.11

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.3-3
- Rebuild for Python 3.6

* Thu Oct 27 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.3-2
- New upstream source (0.10.3)
- Add patch to fix a test in python 3.5
- Run all tests

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.0-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 13 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.0-1
- New upstream source (0.10.0)
- Updated pypi url

* Tue Mar 29 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.9.4-1
- New upstream source (0.9.4)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 26 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.9.3-3
- Add patch to fix the testing errors

* Tue Nov 24 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.9.3-2
- New upstream release (0.9.3)
- Using new python macros
- Disable failling tests (https://github.com/joblib/joblib/issues/278)

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.4-1
- New upstream release (0.8.4)

* Wed Sep 03 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.3-1
- New upstream release (0.8.3)

* Wed Jul 02 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.2-1
- New upstream release (0.8.2)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.0-2
- Reverted stylistic changes
- Run checks on installed files
- Use tarball from PyPI

* Mon Jun 02 2014 Björn Esser <bjoern.esser@gmail.com> - 0.8.0-1
- new stable upstream
- restructured spec-file
- include README from src-tarball in %%doc
- updated python2-macros
- make testsuite a bit more verbose
- preserve timestamps of modified files
- use tarball from github-tags

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-0.2.a2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Jan 09 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.0-0.1.a2
- New upstream prerelease (0.8.0a2)

* Sun Aug 25 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.7.1-2
- Removing upstream egg
- Adding BR python(3)-setuptools

* Sat Aug 24 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.7.1-1
- New upstream version (0.7.1)

* Thu Jul 4 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.7.0d-1
- Adding index.rst before importing
