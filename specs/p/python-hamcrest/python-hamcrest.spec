# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global modname hamcrest
%global origname PyHamcrest

Name:           python-%{modname}
Version:        2.1.0
Release:        5%{?dist}
Summary:        Hamcrest matchers for Python

License:        BSD-3-Clause
URL:            https://github.com/hamcrest/PyHamcrest
Source0:        %{url}/archive/V%{version}/%{name}-%{version}.tar.gz

# Numpy 2.x patch replacing shorthands (float_, complex_, etc.)
Patch:          https://github.com/hamcrest/PyHamcrest/pull/248.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-numpy
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-xdist

%global _description \
PyHamcrest is a framework for writing matcher objects, allowing you to\
declaratively define "match" rules. There are a number of situations where\
matchers are invaluable, such as UI validation, or data filtering, but it is\
in the area of writing flexible tests that matchers are most commonly used.

%description %{_description}

%package -n python3-%{modname}
Summary:        %{summary}

%description -n python3-%{modname} %{_description}

Python 3 version.

%prep
%autosetup -n %{origname}-%{version} -p1

%generate_buildrequires
# Let hatch-vcs/setuptools_scm determine version outside of SCM
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_buildrequires

%build
# Let hatch-vcs/setuptools_scm determine version outside of SCM
export SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{modname}

%check
# future_test.py implicitly creates event loops - this has been removed from Python 3.14
# Reported upstream and deselected for now:
# https://github.com/hamcrest/PyHamcrest/issues/265
%pytest -v --deselect tests/hamcrest_unit_test/core/future_test.py

%files -n python3-%{modname} -f %{pyproject_files}

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.1.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.1.0-2
- Rebuilt for Python 3.14

* wed Jan 22 2025 Sandro <devel@penguinpee.nl> - 2.1.0-1
- Update to 2.1.0 (RHBZ#2245624)
- Support NumPy 2.x
- Close RHBZ#2341160

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 2.0.3-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.0.3-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 05 2022 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3 (RHBZ #1788673)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.9.0-20
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.9.0-17
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-14
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 20 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-12
- Subpackage python2-hamcrest has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-11
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-10
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-2
- Rebuild for Python 3.6

* Mon Oct 03 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 1.9.0-1
- Update to 1.9.0

* Sun Aug 21 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.8.5-2
- Backport couple of upstream patches

* Fri Aug 19 2016 Igor Gnatenko <ignatenko@redhat.com> - 1.8.5-1
- Initial package
