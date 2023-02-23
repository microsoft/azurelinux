Vendor:         Microsoft Corporation
Distribution:   Mariner
## START: Set by rpmautospec
## (rpmautospec version 0.2.6)
%define autorelease(e:s:pb:) %{?-p:0.}%{lua:
    release_number = 1;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{?dist}
## END: Set by rpmautospec

%bcond_without tests

# The python-diskcache package, used in some of the tests, has been retired.
%bcond_with diskcache

Name:           python-fasteners
Version:        0.18
Release:        %autorelease
Summary:        A python package that provides useful locks

License:        Apache-2.0
URL:            https://github.com/harlowja/fasteners
# We need to use the GitHub archive instead of the PyPI sdist to get tests.
Source0:        %{url}/archive/%{version}/fasteners-%{version}.tar.gz

# Backport 80a3eaed75276faf21034e7e6c626fd19485ea39 “Move eventlet tests to
# main folder and to child process”. Fixes “Tests hang with eventlet support”
# https://github.com/harlowja/fasteners/issues/101. (As an alternative, we
# could run pytest on tests/ and tests_eventlet/ in separate invocations.) See
# https://github.com/harlowja/fasteners/issues/101#issuecomment-1249462951.
Patch:          %{url}/commit/80a3eaed75276faf21034e7e6c626fd19485ea39.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-packaging
BuildRequires:  python3-requests
BuildRequires:  python3-wheel

%global common_description %{expand:
Cross platform locks for threads and processes}

%description %{common_description}


%package -n python3-fasteners
Summary:        A python package that provides useful locks

# The mkdocs-generated HTML documentation is not suitable for packaging; see
# https://bugzilla.redhat.com/show_bug.cgi?id=2006555 for discussion.
#
# The Provides/Obsoletes can be removed after F38 reaches end-of-life.
Provides:       python-fasteners-doc = %{version}-%{release}
Obsoletes:      python-fasteners-doc < 0.18-1

%description -n python3-fasteners %{common_description}


%prep
%autosetup -p1 -n fasteners-%{version}
%if %{without diskcache}
sed -r -i '/\b(diskcache)\b/d' requirements-test.txt
%endif


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:requirements-test.txt}


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files fasteners


%check
%if %{with tests}
%pytest %{?!with_diskcache:--ignore=tests/test_reader_writer_lock.py} -v
%else
%pyproject_check_import -e 'fasteners.pywin32*'
%endif


%files -n python3-fasteners -f %{pyproject_files}
# pyproject_files handles LICENSE; verify with “rpm -qL -p …”
%doc CHANGELOG.md
%doc README.md


%changelog
* Fri Sep 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.18-1
- Update to 0.18 (close RHBZ#2126965)
- The separate -doc subpackage is dropped since upstream switched from
  sphinx to mkdocs

* Fri Sep 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.17.3-5
- Update License to SPDX

* Fri Sep 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.17.3-4
- Parallelize sphinx-build

* Fri Sep 16 2022 Benjamin A. Beasley <code@musicinmybrain.net> 0.17.3-3
- Fix extra newline in description

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

