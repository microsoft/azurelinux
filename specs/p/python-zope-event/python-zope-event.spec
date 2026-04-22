# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Running the tests requires python3-zope-testrunner, which requires
# python3-zope-interface, which requires this package.  Build in bootstrap
# mode to avoid the circular dependency.
%bcond_with bootstrap
%bcond_without docs

# Install doc subpackage files into the main package doc directory
%global _docdir_fmt %{name}

Name:           python-zope-event
Version:        5.1
Release: 5%{?dist}
Summary:        Zope Event Publication
License:        ZPL-2.1
URL:            https://pypi.python.org/pypi/zope.event/
Source0:        %pypi_source zope_event
BuildArch:      noarch

%description
The zope.event package provides a simple event system. It provides
an event publishing system and a very simple event-dispatching system
on which more sophisticated event dispatching systems can be built.
(For example, a type-based event dispatching system that builds on
zope.event can be found in zope.component.)

%package -n python3-zope-event
Summary:        Zope Event Publication (Python 3)

BuildRequires:  make
BuildRequires:  python3-devel
%if %{with docs}
BuildRequires:  python3-docs
BuildRequires:  %{py3_dist sphinx}
%endif

%description -n python3-zope-event
The zope.event package provides a simple event system. It provides
an event publishing system and a very simple event-dispatching system
on which more sophisticated event dispatching systems can be built.
(For example, a type-based event dispatching system that builds on
zope.event can be found in zope.component.)

This package contains the version for Python 3.

%package doc
Summary:        Documentation for zope.event

%description doc
Documentation for %{name}.

%prep
%autosetup -n zope_event-%{version} -p1

# Update the sphinx theme name
sed -i "s/'default'/'classic'/" docs/conf.py

# Use local objects.inv for intersphinx
sed -i "s|\('https://docs\.python\.org/': \)None|\1'%{_docdir}/python3-docs/html/objects.inv'|" docs/conf.py

%generate_buildrequires
%if %{with bootstrap}
%pyproject_buildrequires
%else
%pyproject_buildrequires -t
%endif

%build
%pyproject_wheel

%if %{with docs}
# build the sphinx documents
PYTHONPATH=$PWD/src make -C docs html
rm -f docs/_build/html/.buildinfo
%endif

%install
%pyproject_install
%pyproject_save_files zope

%if %{without bootstrap}
%check
%tox
%endif

%files -n python3-zope-event -f %{pyproject_files}
%doc CHANGES.rst COPYRIGHT.txt README.rst
%license LICENSE.txt
%exclude %{python3_sitelib}/zope/event/tests.py*
%exclude %{python3_sitelib}/zope/event/__pycache__/tests*
%{python3_sitelib}/zope.event-*-nspkg.pth

%files doc
%if %{with docs}
%doc docs/_build/html/
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.1-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.1-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 30 2025 Orion Poplawski <orion@nwra.com> - 5.1-1
- Update to 5.1

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 5.0-8
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 5.0-7
- Bootstrap for Python 3.14

* Mon Jan 20 2025 Orion Poplawski <orion@nwra.com> - 5.0-6
- Rebuild without bootstrop (rhbz#2314522)
- Add upstream fix for doc build with sphinx 8.x (rhbz#2329899)

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 5.0-3
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 5.0-2
- Bootstrap for Python 3.13

* Mon Jan 29 2024 Jerry James <loganjerry@gmail.com> - 5.0-1
- Version 5.0
- Convert the License field to SPDX
- Drop upstreamed patches
- Simplify with pyproject_save_files

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 4.5.0-7
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 4.5.0-6
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Sep 20 2022 Miro Hrončok <mhroncok@redhat.com> - 4.5.0-4
- Disable bootstrap
- Enable docs

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.5.0-2.1
- Rebuilt for Python 3.11

* Thu Apr 21 2022 Orion Poplawski <orion@nwra.com> - 4.5.0-1.1
- Drop docs for EPEL9

* Fri Mar  4 2022 Jerry James <loganjerry@gmail.com> - 4.5.0-1
- Version 4.5.0 (bz 1475058)
- Add bootstrap conditional to break circular dependency when testing
- Add doc subpackage to hold Sphinx-built documentation
- Add tox and python3 patches to fix build and test failures
- Modernize the spec file

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 4.2.0-21
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-18
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 31 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-16
- Subpackage python2-zope-event has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-15
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-14
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-10
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 4.2.0-9
- Build the docs with Python 3

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 4.2.0-7
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.2.0-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 28 2016 Ralph Bean <rbean@redhat.com> - 4.2.0-2
- Modernized python macros.
- Added an explicit python2 subpackage.

* Fri Feb 19 2016 Ralph Bean <rbean@redhat.com> - 4.2.0-1
- new version

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Nov 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 4.1.0-2
- Rebuilt for Python 3.5

* Mon Oct 19 2015 Ralph Bean <rbean@redhat.com> - 4.1.0-1
- new version

* Mon Oct 19 2015 Ralph Bean <rbean@redhat.com> - 4.0.3-4
- No longer own zope/__init__.py.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Oct 15 2014 Ralph Bean <rbean@redhat.com> - 4.0.3-2
- Fix a python3 conditional block.

* Mon Jul 21 2014 Ralph Bean <rbean@redhat.com> - 4.0.3-1
- Latest upstream.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 4.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Ralph Bean <rbean@redhat.com> - 4.0.2-1
- Latest upstream.
- Conditionalized python3 subpackage for el6.

* Thu Oct 18 2012 Robin Lee <cheeselee@fedoraproject.org> - 3.5.2-1
- Update to 3.5.2 (ZTK 1.1.5)

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.5.1-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep  1 2011 Robin Lee <cheeselee@fedoraproject.org> - 3.5.1-1
- Update to 3.5.1 (#728489)
- Build subpackage for Python 3.
- Include the sphinx documents
- Exclude the module for tests.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Aug 31 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.5.0.1-4
- Add a missed percent character

* Tue Aug 31 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.5.0.1-3
- Remove python-zope-filesystem from requirements
- Own %%{python_sitelib}/zope/
- Spec cleaned up

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Robin Lee <robinlee.sysu@gmail.com> - 3.5.0.1-1
- Update to 3.5.0-1
- Include more documents

* Sun Jul 5 2009 Conrad Meyer <konrad@tylerc.org> - 3.4.1-1
- Add missing BR on python-setuptools.
- Enable testing stuff as zope-testing is in devel.

* Sun Dec 14 2008 Conrad Meyer <konrad@tylerc.org> - 3.4.0-1
- Initial package.
