# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname jinja2

Name:           python-jinja2
Version:        3.1.6
Release: 7%{?dist}
Summary:        General purpose template engine
License:        BSD-3-Clause
URL:            https://palletsprojects.com/p/jinja/
Source0:        %{pypi_source %srcname}

# Enable building without docs to avoid a circular dependency between this
# and python-sphinx:
%if 0%{?rhel} || 0%{?flatpak}
%bcond_with docs
%else
%bcond_without docs
%endif
# The dependency on trio is undesired on RHEL
%bcond asyncio_tests %{undefined rhel}

BuildArch:      noarch

%global _description %{expand:
Jinja2 is a template engine written in pure Python. It provides a
Django inspired non-XML syntax but supports inline expressions and an
optional sandboxed environment.

If you have any exposure to other text-based template languages, such
as Smarty or Django, you should feel right at home with Jinja2. It's
both designer and developer friendly by sticking to Python's
principles and adding functionality useful for templating
environments.}

%description %_description

%package -n python3-jinja2
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-pytest
%if %{with asyncio_tests}
BuildRequires:  python3-trio
%endif
%if %{with docs}
BuildRequires:  %{_bindir}/sphinx-build-3
BuildRequires:  make
BuildRequires:  python3-Pallets-Sphinx-Themes >= 2
BuildRequires:  python3-sphinxcontrib-log-cabinet
BuildRequires:  python3-sphinx-issues
%endif

%description -n python3-jinja2 %_description

%pyproject_extras_subpkg -n python3-jinja2 i18n


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires -x i18n


%build
%pyproject_wheel
%if %{with docs}
make -C docs html PYTHONPATH=$(pwd)/src SPHINXBUILD=sphinx-build-3
# remove hidden file
rm -rvf docs/_build/html/.buildinfo
%endif


%install
%pyproject_install
%pyproject_save_files jinja2


%check
# test_elif_deep is flaky for an unknown reason
# https://github.com/pallets/jinja/issues/2079
%pytest tests -k "not test_elif_deep" %{!?with_asyncio_tests:--ignore tests/test_async.py --ignore tests/test_async_filters.py}


%files -n python3-jinja2 -f %{pyproject_files}
%doc README.md
%doc docs/examples
%license LICENSE.txt
%if %{with docs}
%doc docs/_build/html
%endif


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.1.6-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.1.6-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 3.1.6-3
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.1.6-2
- Bootstrap for Python 3.14

* Sun Mar  9 2025 Thomas Moschny <thomas.moschny@gmx.de> - 3.1.6-1
- Update to 3.1.6.

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 08 2025 Miro Hrončok <mhroncok@redhat.com> - 3.1.5-1
- Update to 3.1.5
- Security fix for CVE-2024-56201
- Fixes: rhzb#2333688
- Fixes: rhzb#2336377

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 3.1.4-4
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.1.4-3
- Bootstrap for Python 3.13

* Thu May 23 2024 Miro Hrončok <mhroncok@redhat.com> - 3.1.4-2
- Python 3.13 fixes
- Fixes: rhzb#2245265

* Tue May 07 2024 Lumír Balhar <lbalhar@redhat.com> - 3.1.4-1
- Update to 3.1.4 (rhbz#2279211,rhbz#2279491)

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Michel Lind <salimma@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3 to fix CVE-2024-22195

* Tue Aug 08 2023 Karolina Surma <ksurma@redhat.com> - 3.1.2-6
- Declare the license as an SPDX expression

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 3.1.2-4
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.1.2-3
- Bootstrap for Python 3.12

* Fri May 19 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 3.1.2-2
- Disable docs by default in RHEL builds

* Mon May 01 2023 Sandro Mani <manisandro@gmail.com> - 3.1.2-1
- Update to 3.1.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 14 2022 Lumír Balhar <lbalhar@redhat.com> - 3.0.3-6
- Fix compatibility with pytest 7.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.3-4
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.3-3
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.3-1
- Update to 3.0.3.

* Mon Nov 15 2021 Thomas Moschny <thomas.moschny@gmx.de> - 3.0.1-4
- Use new Python packaging guidelines.
- Jinja2 version 3 does not support Python 2 anymore.

* Wed Nov 10 2021 Karolina Surma <ksurma@redhat.com> - 3.0.1-3
- Don't explicitly declare runtime dependencies when building for Python 3
- Declare jinja2+i18n extra to map the upstream package structure

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Lumír Balhar <lbalhar@redhat.com> - 3.0.1-1
- Update to 3.0.1
- Resolves: rhbz#1961862

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.11.3-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 2.11.3-2
- Bootstrap for Python 3.10

* Sat Feb  6 2021 Thomas Moschny <thomas.moschny@gmx.de> - 2.11.3-1
- Update to 2.11.3.
- Add patches to build with Python 3.10 (#1907442).

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 21 2020 Miro Hrončok <mhroncok@redhat.com> - 2.11.2-7
- Drop python2-jinja2 on Fedora 34+

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 2.11.2-5
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 2.11.2-4
- Bootstrap for Python 3.9

* Fri May 22 2020 Thomas Moschny <thomas.moschny@gmx.de> - 2.11.2-3
- Re-add python2 subpackage (#1832057).

* Wed May  6 2020 Thomas Moschny <thomas.moschny@gmx.de> - 2.11.2-2
- Drop python2 subpackage from F33 on (#1832057).

* Wed Apr 15 2020 Thomas Moschny <thomas.moschny@gmx.de> - 2.11.2-1
- Re-add dependency on python-setuptools.

* Wed Apr 15 2020 Dan Horák <dan[at]danny.cz> - 2.11.2-1
- Update to 2.11.2

* Mon Apr 06 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.11.1-2
- Drop unneeded R: pythonX-setuptools

* Sat Feb  8 2020 Thomas Moschny <thomas.moschny@gmx.de> - 2.11.1-1
- Update to 2.11.1.

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 20 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.10.3-2
- Add missing BR on make.

* Mon Nov 11 2019 Lumír Balhar <lbalhar@redhat.com> - 2.10.3-1
- New upstream version (2.10.3)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.1-4
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 2.10.1-3
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 10 2019 Thomas Moschny <thomas.moschny@gmx.de> - 2.10.1-1
- Update to 2.10.1.
- Update specfile.

* Wed Feb 27 2019 Phil Wyett <philwyett@kathenas.org> - 2.10-8
- Fix FTBS due to bad conditional
- Add version requirement for markupsafe

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 2.10-5
- Rebuilt for Python 3.7

* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 2.10-4
- Bootstrap for Python 3.7

* Mon Apr 16 2018 Charalampos Stratakis <cstratak@redhat.com> - 2.10-3
- Don't build the Python 2 subpackage on EL > 7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.10-1
- Update to 2.10.
- Use %%bcond.
- Move BRs to their respective subpackages.

* Fri Oct 20 2017 Troy Dawson <tdawson@redhat.com> - 2.9.6-4
- Really cleanup spec file conditionals

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 2.9.6-3
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Apr  5 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.6-1
- Update to 2.9.6.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun Jan 29 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.5-1
- Update to 2.9.5.

* Fri Jan 13 2017 Thomas Moschny <thomas.moschny@gmx.de> - 2.9.4-1
- Update to 2.9.4.

* Sat Dec 31 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8.1-1
- Update to 2.8.1.

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.8-8
- Rebuild for Python 3.6

* Thu Sep 22 2016 Orion Poplawski <orion@cora.nwra.com> - 2.8-7
- Ship python2-jinja2 (bug #1378519)
- Modernize spec

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb  5 2016 Thomas Moschny <thomas.moschny@gmx.de> - 2.8-5
- Do not call py.test, there are currently no tests in the tarball.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Oct 12 2015 Robert Kuska <rkuska@redhat.com> - 2.8-3
- Rebuilt for Python3.5 rebuild

* Mon Jul 27 2015 Thomas Moschny <thomas.moschny@gmx.de> - 2.8-2
- Apply updates Python packaging guidelines.
- Mark LICENSE with %%license.

* Sun Jul 26 2015 Haïkel Guémar <hguemar@fedoraproject.org> - 2.8-1
- Upstream 2.8

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 2 2014 Orion Poplawski <orion@cora.nwra.com> - 2.7.3-2
- Add Requires python(3)-setuptools (bug #1168774)

* Sat Jun  7 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.3-1
- Update to 2.7.3.
- Reenable docs.

* Sat May 10 2014 Orion Poplawski <orion@cora.nwra.com> - 2.7.2-2
- Bootstrap (without docs) build for Python 3.4

* Fri Jan 10 2014 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.2-1
- Update to 2.7.2.
- Update python3 conditional.

* Fri Aug 16 2013 Thomas Moschny <thomas.moschny@gmx.de> - 2.7.1-1
- Update to 2.7.1.

* Thu Jul 25 2013 Orion Poplawski <orion@cora.nwra.com> - 2.7-1
- Update to 2.7
- spec cleanup

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 2.6-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 2.6-4
- remove rhel logic from with_python3 conditional

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Jul 25 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.6-1
- Update to 2.6.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 18 2011 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.5-3
- Re-enable html doc generation.
- Remove conditional for F-12 and below.
- Do not silently fail the testsuite for with py3k.

* Mon Nov  1 2010 Michel Salim <salimma@fedoraproject.org> - 2.5.5-2
- Move python3 runtime requirements to python3 subpackage

* Wed Oct 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.5-1
- Update to 2.5.5.

* Wed Aug 25 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-4
- Revert to previous behavior: fail the build on failed test.
- Rebuild for Python 3.2.

* Wed Aug 25 2010 Dan Horák <dan[at]danny.cz> - 2.5.2-3
- %%ifnarch doesn't work on noarch package so don't fail the build on failed tests

* Wed Aug 25 2010 Dan Horák <dan[at]danny.cz> - 2.5.2-2
- disable the testsuite on s390(x)

* Thu Aug 19 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5.2-1
- Update to upstream version 2.5.2.
- Package depends on python-markupsafe and is noarch now.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.5-4
- add explicit build-requirement on python-setuptools
- fix doc disablement for python3 subpackage

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.5-3
- support disabling documentation in the build to break a circular build-time
dependency with python-sphinx; disable docs for now

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jul 13 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.5-1
- Update to upstream version 2.5.
- Create python3 subpackage.
- Minor specfile fixes.
- Add examples directory.
- Thanks to Gareth Armstrong for additional hints.

* Wed Apr 21 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.4.1-1
- Update to 2.4.1.

* Tue Apr 13 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.4-1
- Update to 2.4.

* Tue Feb 23 2010 Thomas Moschny <thomas.moschny@gmx.de> - 2.3.1-1
- Update to 2.3.1.
- Docs are built using Sphinx now.
- Run the testsuite.

* Sat Sep 19 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.2.1-1
- Update to 2.2.1, mainly a bugfix release.
- Remove patch no longer needed.
- Remove conditional for FC-8.
- Compilation of speedup module has to be explicitly requested now.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 10 2009 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1 (bugfix release).

* Thu Dec 18 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.1-1
- Update to 2.1, which fixes a number of bugs.
  See http://jinja.pocoo.org/2/documentation/changelog#version-2-1.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.0-3
- Rebuild for Python 2.6

* Tue Jul 22 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-2
- Use rpm buildroot macro instead of RPM_BUILD_ROOT.

* Sun Jul 20 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-1
- Upstream released 2.0.

* Sun Jun 29 2008 Thomas Moschny <thomas.moschny@gmx.de> - 2.0-0.1.rc1
- Modified specfile from the existing python-jinja package.
