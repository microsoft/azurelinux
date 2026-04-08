# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global modname zope.exceptions
%global giturl  https://github.com/zopefoundation/zope.exceptions

# There is a test dependency loop, so we need a way to build this without tests
# zope.exceptions -> zope.testrunner-> zope.exceptions
%bcond tests 1

Summary:    Zope Exceptions
Name:       python-zope-exceptions
Version:    6.0
Release:    2%{?dist}
VCS:        git:%{giturl}.git
Source0:    %{giturl}/archive/%{version}/%{modname}-%{version}.tar.gz
License:    ZPL-2.1
BuildArch:  noarch
URL:        https://zopeexceptions.readthedocs.io/

%description
This package contains exception interfaces and implementations which are so
general purpose that they don't belong in Zope application-specific packages.

%package -n python3-zope-exceptions
Summary:    Zope Exceptions
BuildRequires:  python3-devel

%description -n python3-zope-exceptions
This package contains exception interfaces and implementations which are so
general purpose that they don't belong in Zope application-specific packages.

%prep
%autosetup -n %{modname}-%{version} -p1
# we don't have specific versions of setuptools available
sed -i -r 's/    setuptools [<>=]+ [0-9\.]+/    setuptools/g' tox.ini


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:-t}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files zope

%check
%pyproject_check_import
%if %{with tests}
%tox
%endif

%files -n python3-zope-exceptions -f %{pyproject_files}
%doc CHANGES.rst README.rst
%license COPYRIGHT.txt LICENSE.txt

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 6.0-2
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Sep 12 2025 David Auer <dreua@posteo.de> - 6.0-1
- Version 6.0 (rhbz#2394776)

* Sat Aug 30 2025 David Auer <dreua@posteo.de> - 5.2-1
- Version 5.2 (rhbz#2322672, rhbz#2329901)
- Remove patch
- Remove setuptools version requirement in tox.ini

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.1-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 5.1-4
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 5.1-3
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 23 2024 Jerry James <loganjerry@gmail.com> - 5.1-1
- Version 5.1 (rhbz#2290844)
- Add patch for python 3.13 compatibility (rhbz#2280553)
- Minor spec file cleanups

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 5.0.1-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.0.1-2
- Bootstrap for Python 3.13

* Mon Jan 29 2024 Jerry James <loganjerry@gmail.com> - 5.0.1-1
- Version 5.0.1
- Convert License tag to SPDX
- Modernize the spec file

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.0.8-26
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.0.8-23
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.8-20
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.8-17
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Sep 20 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.8-15
- Subpackage python2-zope-exceptions has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.8-14
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 4.0.8-10
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.0.8-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jul 18 2016 Ralph Bean <rbean@redhat.com> - 4.0.8-4
- Explicit python2 subpackage.
- Modernized python macros.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Sep 19 2015 Ralph Bean <rbean@redhat.com> - 4.0.8-1
- new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 20 2014 Ralph Bean <rbean@redhat.com> - 4.0.7-1
- Latest uptream.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 4.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Apr 10 2013 Ralph Bean <rbean@redhat.com> - 4.0.6-1
- Update to the latest upstream.
- Modernized python3 conditional.
- Renamed CHANGES and README from .txt to .rst.
- Disabled tests which now require python-zope-testrunner.

* Mon Feb 25 2013 Ralph Bean <rbean@redhat.com> - 4.0.5-1
- Latest upstream.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 01 2013 Ralph Bean <rbean@redhat.com> - 4.0.3-2
- Require python-zope-interface4 compat package on el6.

* Tue Dec 11 2012 Ralph Bean <rbean@redhat.com> - 4.0.3-1
- Latest upstream.
- Packaged a python3 subpackage.
- Made indentation consistent.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Sep 19 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-6
- Exclude the tests from installation

* Wed Sep 15 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-5
- BR: python-zope-interface added
- Add %%check section and run the tests

* Tue Aug 31 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-4
- Own %%{python_sitelib}/zope/

* Mon Aug 30 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-3
- Remove python-zope-filesystem from requirements
- Import to Fedora repositories

* Mon Aug 30 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-2
- Remove %%clean section
- Remove python-setuptools from requirements
- Remove definitions of Python-related macros 

* Mon Aug 30 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.1-1
- Update to 3.6.1
- Summit review request

* Wed Jun 16 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.6.0-1
- Initial packaging
