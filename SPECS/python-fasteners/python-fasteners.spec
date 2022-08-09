# Sphinx-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# We can generate PDF documentation as a substitute.
# MARINER - Not creating doc rpm package.

# The python-diskcache package, used in some of the tests, has been retired.
%bcond_with diskcache

%global common_description %{expand: \
Cross platform locks for threads and processes}

Name:           python-fasteners
Version:        0.17.3
Release:        3%{?dist}
Summary:        A python package that provides useful locks
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/harlowja/fasteners
# We need to use the GitHub archive instead of the PyPI sdist to get tests.
Source0:        %{url}/archive/refs/tags/%{version}.tar.gz#/fasteners-%{version}.tar.gz

# “Remove futures from the requirements-test.txt”
# Backport upstream commit 49d8f5b to remove a test dependency that is no
# longer used and only supports Python 2.
Patch0:         %{url}/commit/49d8f5bb56157a82ff3e6128b506638a214e6d43.patch
BuildArch:      noarch

%description
%{common_description}

%package -n python3-fasteners
Summary:        A python package that provides useful locks

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%if %{with_check}
BuildRequires:  python3-pytest
%endif
Requires:       python3

%description -n python3-fasteners
%{common_description}

%prep
%autosetup -p1 -n fasteners-%{version}
%if %{without diskcache}
sed -r -i '/\b(diskcache)\b/d' requirements-test.txt
%endif

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files fasteners

%check
%{python3} -m pip install atomicwrites attrs pluggy pygments six more-itertools
%pytest %{?!with_diskcache:--ignore=tests/test_reader_writer_lock.py}
%pyproject_check_import -e 'fasteners.pywin32*'

%files -n python3-fasteners -f %{pyproject_files}
# pyproject_files handles LICENSE; verify with “rpm -qL -p …”

%changelog
* Thu Jun 23 2022 Sumedh Sharma <sumsharma@microsoft.com> - 0.17.3-3
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Adding as run dependency for package cassandra medusa
- Removing subpackage 'doc'.
- License verified

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.17.3-2
- Build Sphinx docs as PDF in a new -doc subpackage

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.17.3-1
- Update to 0.17.3 (close RHBZ#1712140)

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.17-4
- Use pyproject-rpm-macros

* Mon May 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.17-3
- Drop EPEL8 conditionals

* Tue May 03 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.17-1
- Update to 0.17

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-26
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.14.1-25
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-22
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 15 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.14.1-21
- Fix conditionals.

* Mon Jan 13 2020 Gwyn Ciesla <gwync@protonmail.com> - 0.14.1-19
- Disable tests on EL-8

* Mon Sep 02 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-18
- Subpackage python2-fasteners has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-17
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-13
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.14.1-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 17 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.14.1-10
- Fix monotonic req on py3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.14.1-7
- Rebuild for Python 3.6

* Mon Aug 29 2016 Matthias Runge <mrunge@redhat.com> - 0.14.1-6
- Use time.monotonic if available (Python3 > 3.2)
  patch thanks to Ville Skyttä (rhbz#1294335)
- modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.14.1-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar 16 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.14.1-4
- Spec cleanups

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 18 2015 Matthias Runge <mrunge@redhat.com> - 0.14.1-2
- update to 0.14.1 (rhbz#1281772)
- fix python_provide

* Mon Nov 16 2015 Matthias Runge <mrunge@redhat.com> - 0.13.0-3
- Fix build

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Aug 28 2015 Matthias Runge <mrunge@redhat.com> - 0.13.0-1
- update to 0.13.0 (rhbz#1256153)

* Mon Jun 22 2015 Matthias Runge <mrunge@redhat.com> - 0.12.0-1
- update to 0.12.0 (rhbz#1234253)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 12 2015 Matthias Runge <mrunge@redhat.com> - 0.9.0-2
- switch to github sourcecode, license included
- add tests, fix conditionals for python3

* Thu Jun 11 2015 Matthias Runge <mrunge@redhat.com> - 0.9.0-1
- Initial package. (rhbz#1230548)

