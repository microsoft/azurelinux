# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname py

Name:           python-%{srcname}
Version:        1.11.0
Release: 20%{?dist}
Summary:        Library with cross-python path, ini-parsing, io, code, log facilities
# Automatically converted from old format: MIT and Public Domain - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND LicenseRef-Callaway-Public-Domain
#               main package: MIT, except: doc/style.css: Public Domain
URL:            http://py.readthedocs.io/
Source:         %{pypi_source}
BuildArch:      noarch
BuildRequires:  python3-devel

%description
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects


%package -n python3-%{srcname}
Summary:        Library with cross-python path, ini-parsing, io, code, log facilities
Requires:       python3-setuptools
Provides:       bundled(python3-apipkg) = 2.0
Provides:       bundled(python3-iniconfig) = 1.1.1
Obsoletes:      platform-python-%{srcname} < %{version}-%{release}

%description -n python3-%{srcname}
The py lib is a Python development support library featuring the
following tools and modules:

  * py.path: uniform local and svn path objects
  * py.apipkg: explicit API control and lazy-importing
  * py.iniconfig: easy parsing of .ini files
  * py.code: dynamic code generation and introspection
  * py.path: uniform local and svn path objects


%prep
%autosetup -n %{srcname}-%{version}

# remove shebangs and fix permissions
find . \
   -type f -a \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l %{srcname}

# Remove bundled dist/egg-info directories, they shouldn't be shipped for
# bundled modules and in some cases they could confuse automatic generators
# that read the dist/egg-info data.
rm -rf %{buildroot}%{python3_sitelib}/py/_vendored_packages/*.{dist,egg}-info
sed -i -r -e '/\/py\/_vendored_packages\/.*(dist|egg)-info/d' %{pyproject_files}


%check
%pyproject_check_import

%py3_check_import %{srcname}

%files -n python3-%{srcname} -f %{pyproject_files}
%doc CHANGELOG.rst
%doc README.rst


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.11.0-19
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.11.0-18
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.0-16
- Update for current Python packaging guidelines.

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.11.0-15
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 1.11.0-13
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.11.0-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.11.0-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.11.0-4
- Rebuilt for Python 3.11

* Tue Feb 15 2022 Karolina Surma <ksurma@redhat.com> - 1.11.0-3
- Remove documentation from the package
- Remove testing that requires very old pytest, use %%py3_check_import instead

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sun Dec  5 2021 Thomas Moschny <thomas.moschny@gmx.de> - 1.11.0-1
- Update to 1.11.0.

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.10.0-4
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.10.0-3
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 26 2020 Thomas Moschny <thomas.moschny@gmx.de> - 1.10.0-1
- Update to 1.10.0.

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 28 2020 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.0-1
- Update to 1.9.0.

* Sat Jun 20 2020 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.2-1
- Update to 1.8.2.

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.8.0-10
- Rebuilt for Python 3.9

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 1.8.0-9
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Nov 23 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.0-7
- Subpackage python2-py has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.0-5
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.0-4
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 15 2019 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.0-1
- Update to 1.8.0.
- Update spec file.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.7.0-2
- Drop explicit locale setting for python3, use C.UTF-8 for python2
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sun Nov 11 2018 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-1
- Update to 1.7.0.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.4-2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.4-1
- Update to 1.5.4.
- Add BR on setuptools_scm.

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.3-3
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.3-2
- Bootstrap for Python 3.7

* Thu Mar 22 2018 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.3-1
- Update to 1.5.3.

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.5.2-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Nov 16 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.2-1
- Update to 1.5.2.

* Wed Nov 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.1-1
- Update to 1.5.1.
- Update list of vendored packages.
- Fix HTML doc path.

* Wed Nov 15 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.34-8
- Restore earlier structure of the spec file, also fixing previously
  introduced problems.

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.34-7
- Use better Obsoletes for platform-python

* Fri Nov 03 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.4.34-6
- Remove platform-python subpackage

* Tue Sep 05 2017 Troy Dawson <tdawson@redhat.com> - 1.4.34-5
- Cleanup spec file conditionals

* Fri Aug 11 2017 Tomas Orsava <torsava@redhat.com> - 1.4.34-4
- Switch with_docs and run_test macros to bcond_without docs, tests

* Thu Aug 10 2017 Tomas Orsava <torsava@redhat.com> - 1.4.34-3
- Added the platform-python subpackage

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun  5 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.34-1
- Update to 1.4.34.

* Sun Mar 19 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.33-1
- Update to 1.4.33.

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.32-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.32-2
- Enable tests for Fedora<26.

* Thu Dec 29 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.32-1
- Update to 1.4.32.

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.4.31-5
- Rebuild for Python 3.6
- Disable tests

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.31-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.31-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.31-2
- Re-enable checks and docs.

* Sat Jan 23 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.31-1
- Update to 1.4.31.
- Follow updated Python packaging guidelines.
- Add Provides tag for bundled apipkg.

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 1.4.30-3
- Rebuilt for Python3.5 rebuild
- With check and docs

* Wed Sep 23 2015 Robert Kuska <rkuska@redhat.com> - 1.4.30-2
- Rebuilt for Python3.5 rebuild without check and docs

* Mon Jul 27 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.30-1
- Update to 1.4.30.

* Thu Jun 25 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.29-1
- Update to 1.4.29.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri May 29 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.28-1
- Update to 1.4.28.
- Modernize spec file.
- Apply updates Python packaging guidelines.
- Mark LICENSE with %%license.

* Sat Dec  6 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.26-2
- Re-enable doc building and testsuite.

* Tue Dec  2 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.26-1
- Update to 1.4.26.

* Sat Oct 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.25-2
- Re-enable doc building and testsuite.

* Sat Oct 11 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.25-1
- Update to 1.4.25.

* Wed Aug  6 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.23-1
- Update to 1.4.23.

* Fri Aug  1 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.22-2
- Re-enable doc building and testsuite.

* Fri Aug  1 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.22-1
- Update to 1.4.22.

* Fri Jul 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.21-1
- Update to 1.4.21.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.20-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 1.4.20-2.1
- rebuild for python 3.4 disable tests for circular deps

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.20-2
- Re-enable doc building and testsuite.

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.20-1
- Update to 1.4.20.

* Sun Nov 10 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.18-1
- Update to 1.4.18.

* Mon Oct  7 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.17-2
- Only run tests from the 'testing' subdir in %%check.

* Fri Oct  4 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.17-1
- Update to 1.4.17.

* Thu Oct  3 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.16-1
- Update to 1.4.16.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 30 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.15-1
- Update to 1.4.15.
- Disable failing Subversion checks for now.

* Wed Jun 12 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.14-2
- Use python-sphinx for rhel > 6 (rhbz#973321).
- Update URL.
- Fix changelog entry with an incorrect date (rhbz#973325).

* Sat May 11 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.14-1
- Update to 1.4.14.

* Sat Mar  2 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.13-1
- Update to 1.4.13.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 23 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.12-1
- Update to 1.4.12.

* Sat Oct 27 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.11-1
- Update to 1.4.11.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.10-2
- Re-enable doc building and testsuite.
- Minor testsuite fixes.

* Sun Oct 21 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.10-1
- Update to 1.4.10.

* Fri Oct 12 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-8
- Re-enable doc building and testsuite.

* Thu Oct 11 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-7
- Add conditional for sphinx on rhel.
- Remove rhel logic from with_python3 conditional.

* Wed Oct 10 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-6
- Re-enable doc building and testsuite.

* Sat Aug  4 2012 David Malcolm <dmalcolm@redhat.com> - 1.4.9-5
- Temporarily disable docs and testsuite.

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.4.9-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 15 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-2
- Re-enable doc building and testsuite.

* Thu Jun 14 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.9-1
- Update to 1.4.9.

* Sat Jun  9 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.8-2
- Re-enable doc building and testsuite.

* Wed Jun  6 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.8-1
- Update to 1.4.8.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.7-2
- Re-enable doc building and testsuite.

* Wed Feb  8 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.7-1
- Update to 1.4.7.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.6-2
- Re-enable doc building and testsuite.

* Sat Dec 17 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.6-1
- Update to 1.4.6.
- Remove %%prerelease macro.
- Temporarily disable docs and testsuite.

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.5-4
- Rebuilt for glibc bug#747377

* Sat Sep  3 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.5-3
- Fix: python3 dependencies.

* Tue Aug 30 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.5-2
- Re-enable doc building and testsuite.

* Sat Aug 27 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.5-1
- Update to 1.4.5.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.4-2
- Re-enable doc building and testsuite.

* Thu Aug 11 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.4-1
- Update to 1.4.4.
- Upstream provides a .zip archive only.
- pytest and pycmd are separate packages now.
- Disable building html docs und the testsuite to break the circular
  build dependency with pytest.
- Update summary and description.
- Remove BRs no longer needed.
- Create a Python 3 subpackage.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Sep 18 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.4-1
- Update to 1.3.4

* Fri Aug 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.3-2
- Add dependency on python-setuptools (see bz 626808).

* Sat Jul 31 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.3-1
- Update to 1.3.3.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 10 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.2-1
- Update to 1.3.2.
- Do cleanups already in %%prep to avoid inconsistent mtimes between
  source files and bytecode.

* Sat May 29 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.1-1
- Update to 1.3.1.

* Sat May  8 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.0-1
- Update to 1.3.0.
- Remove some backup (.orig) files.

* Sun Feb 14 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.1-1
- Update to 1.2.1.

* Wed Jan 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.0-1
- Update to 1.2.0.
- Adjust summary and %%description.
- Use %%global instead of %%define.

* Sat Nov 28 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.1-1
- Update to 1.1.1.

* Sat Nov 21 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.1.0-1
- Update to 1.1.0. Upstream reorganized the package's structure and
  cleaned up the install process, so the specfile could be greatly
  simplified.
- Dropped licenses for files no longer present from the License tag.

* Thu Aug 27 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.2-1
- Update to 1.0.2.
- One failing test is no longer part of the testsuite, thus needs not
  to be skipped anymore.
- Some developer docs are missing this time in upstream's tarfile, so
  cannot be moved to %%{_docdir}

* Thu Aug 13 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-1
- Update to 1.0.0.
- Re-enable SVN tests in %%check.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-1.b8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-0.b8
- Update to 1.0.0b8.
- Remove patches applied upstream.
- Greenlets have been removed upstream. So, package is noarch and
  - installs to %%{python_sitelib} again
  - %%ifarch sections have been removed.
- Don't remove files used by the testsuite for now.
- Add dependency on python-pygments, pylint and pexpect (for the
  testsuite).

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 14 2009 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-6
- Use system doctest module again, as this wasn't the real cause of
  the test failure. Instead, remove the failing test for now.

* Fri Dec 12 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-5
- Add patch from trunk fixing a subversion 1.5 problem (pylib
  issue66).
- Don't replace doctest compat module (pylib issue67).

* Fri Nov 21 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-4
- Use dummy_greenlet on ppc and ppc64.

* Tue Oct  7 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-3
- Replace compat modules by stubs using the system modules instead.
- Add patch from trunk fixing a timing issue in the tests.

* Tue Sep 30 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-2
- Update license information.
- Fix the tests.

* Sun Sep  7 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.2-1
- Update to 0.9.2.
- Upstream now uses setuptools and installs to %%{python_sitearch}.
- Remove %%{srcname} macro.
- More detailed information about licenses.

* Thu Aug 21 2008 Thomas Moschny <thomas.moschny@gmx.de> - 0.9.1-1
- New package.
