# Remove -s from Python shebang - ensure that extensions installed with pip
# to user locations are seen and properly loaded
%undefine _py3_shebang_s

%global forgeurl https://github.com/PyCQA/pylint
%global basever 4.0.2
#%%global prever b0
Version:        4.0.2

Name:           pylint
Release:        2%{?dist}
Summary:        Analyzes Python code looking for bugs and signs of poor quality
License:        GPL-2.0-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/pylint-dev/pylint
Source0:        %{forgeurl}/archive/v%{basever}/pylint-%{basever}.tar.gz
#Patch0:         7829.patch apply when rebased then re-enable tests
Patch1:         pep639.patch
BuildArch:      noarch

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  python3-setuptools
# For tests
BuildRequires:  python3-pytest-benchmark
BuildRequires:  python3-pytest-xdist
BuildRequires:  python3-typing-extensions
BuildRequires:  graphviz
BuildRequires:  python3-execnet
BuildRequires:  python3-astroid
BuildRequires:  python3-platformdirs
BuildRequires:  python3-isort
BuildRequires:  git
BuildRequires:  python3-mccabe

# For the main pylint package
Requires:       python3-%{name} = %{version}-%{release}

%global _description %{expand:
Pylint is a Python source code analyzer which looks for programming errors,
helps enforcing a coding standard and sniffs for some code smells (as defined in
Martin Fowler's Refactoring book). Pylint can be seen as another PyChecker since
nearly all tests you can do with PyChecker can also be done with Pylint.
However, Pylint offers some more features, like checking length of lines of
code, checking if variable names are well-formed according to your coding
standard, or checking if declared interfaces are truly implemented, and much
more.

Additionally, it is possible to write plugins to add your own checks.}

%description %_description

%package -n python3-%{name}
Summary:        %{summary}

%description -n python3-%{name} %_description

%prep
%autosetup -p1 -n %{name}-%{basever}
# Relax version requirements
sed -i -e 's/"setuptools>=[^"]*"/"setuptools"/' pyproject.toml


%build
%pyproject_wheel

%install
%pyproject_install
rm -rf %{buildroot}%{python3_sitelib}/pylint/test

# Add -%%{python3_version} to the binaries and manpages for backwards compatibility
for NAME in pylint pyreverse symilar; do
    mv %{buildroot}%{_bindir}/{$NAME,${NAME}-%{python3_version}}
    ln -s ${NAME}-%{python3_version} %{buildroot}%{_bindir}/${NAME}-3
    ln -s ${NAME}-%{python3_version} %{buildroot}%{_bindir}/${NAME}
done

%check
pip3 install tomlkit==0.12.5 \
             dill \
             GitPython
# Skip benchmarks
# Deselect all tests failing with Python 3.14
%pytest -v --ignore=benchmark \
  -n auto \
  --deselect=tests/test_functional.py::test_functional[missing_timeout] \
  --deselect=tests/config/pylint_config/test_pylint_config_help.py::test_pylint_config_main_messages \
  --deselect=tests/pyreverse/test_writer.py::test_dot_files[packages_No_Name.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_dot_files[classes_No_Name.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_colorized_dot_files[packages_colorized.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_colorized_dot_files[classes_colorized.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_no_standalone_dot_files[classes_no_standalone.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_no_standalone_dot_files[packages_no_standalone.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_type_check_imports_dot_files[packages_type_check_imports.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_type_check_imports_dot_files[classes_type_check_imports.dot] \
  --deselect=tests/pyreverse/test_writer.py::test_puml_files[packages_No_Name.puml] \
  --deselect=tests/pyreverse/test_writer.py::test_puml_files[classes_No_Name.puml] \
  --deselect=tests/pyreverse/test_writer.py::test_mmd_files[packages_No_Name.mmd] \
  --deselect=tests/pyreverse/test_writer.py::test_mmd_files[classes_No_Name.mmd] \
  --deselect=tests/pyreverse/test_writer.py::test_html_files[packages_No_Name.html] \
  --deselect=tests/pyreverse/test_writer.py::test_html_files[classes_No_Name.html] \
  --deselect=tests/pyreverse/test_writer.py::test_colorized_puml_files[packages_colorized.puml] \
  --deselect=tests/pyreverse/test_writer.py::test_colorized_puml_files[classes_colorized.puml] \
  --deselect=tests/test_functional.py::test_functional[continue_in_finally] \
  --deselect=tests/test_functional.py::test_functional[consider_using_with] \
  --deselect=tests/test_functional.py::test_functional[typing_broken_callable] \
  --deselect=tests/test_functional.py::test_functional[typing_broken_callable_future_import] \
  --deselect=tests/test_functional.py::test_functional[typing_consider_using_union] \
  --deselect=tests/test_functional.py::test_functional[typing_consider_using_union_py310] \
  --deselect=tests/test_functional.py::test_functional[typing_consider_using_union_without_future] \
  --deselect=tests/test_functional.py::test_functional[function_redefined_2540] \
  --deselect=tests/test_functional.py::test_functional[generic_alias_collections] \
  --deselect=tests/test_functional.py::test_functional[generic_alias_mixed_py39] \
  --deselect=tests/test_functional.py::test_functional[generic_alias_typing] \
  --deselect=tests/test_functional.py::test_functional[lost_exception] \
  --deselect=tests/test_functional.py::test_functional[return_in_finally] \
  --deselect=tests/test_functional.py::test_functional[wrong_import_order] \
  --deselect=tests/test_import_graph.py::test_dependencies_graph[foo.dot] \
  --deselect=tests/test_import_graph.py::test_dependencies_graph[foo.gv] \
  --deselect=tests/test_import_graph.py::test_dependencies_graph[tests/regrtest_data/foo.dot] \
  --deselect=tests/test_import_graph.py::test_checker_dep_graphs \
  --deselect=tests/test_self.py::TestRunTC::test_do_not_import_files_from_local_directory[args0] \
  --deselect=tests/test_self.py::TestRunTC::test_do_not_import_files_from_local_directory[args1] \
  --deselect=tests/test_self.py::TestRunTC::test_progress_reporting \
  --deselect=tests/pyreverse/test_diadefs.py::TestDefaultDiadefGenerator::test_functional_relation_extraction

%files
%doc CONTRIBUTORS.txt
%license LICENSE
%{_bindir}/pylint
%{_bindir}/pylint-config
%{_bindir}/pyreverse
%{_bindir}/symilar

%files -n python3-%{name}
%license LICENSE
%{python3_sitelib}/pylint*
# backwards compatible versioned executables and manpages:
%{_bindir}/*-3
%{_bindir}/*-%{python3_version}

%changelog
* Tue Nov 11 2025 Akhila Guruju <guakhila@microsoft.com> 4.0.2-2
- Upgrade to 4.0.2 by taking reference from Fedora 43 (license: MIT).
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.4-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Gwyn Ciesla <gwync@protonmail.com> - 2.4.4-2
- Disable deprecated tests on Python 3.9

* Thu Nov 14 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.4-1
- 2.4.4

* Fri Oct 18 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.3-1
- 2.4.3

* Mon Sep 30 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.2-1
- 2.4.2

* Wed Sep 25 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.1-1
- 2.4.1

* Tue Sep 24 2019 Gwyn Ciesla <gwync@protonmail.com> - 2.4.0-1
- 2.4.0

* Tue Aug 27 2019 Vojtech Trefny <vtrefny@redhat.com> - 2.3.1-4
- Added upstream fix to build with Python 3.8

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Mar 30 2019 Christian Dersch <lupinix@fedoraproject.org> - 2.3.1-1
- new version
- removed Patch0, applied upstream

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Nov 09 2018 Christian Dersch <lupinix@mailbox.org> - 2.1.1-2
- Apply upstream fix for #1648299

* Tue Oct 02 2018 Christian Dersch <lupinix@fedoraproject.org> - 2.1.1-1
- new version

* Wed Aug 01 2018 Christian Dersch <lupinix@mailbox.org> - 2.1.0-1
- new version

* Wed Jul 25 2018 Christian Dersch <lupinix.fedora@gmail.com> - 2.0.1-1
- new version

* Sun Jul 15 2018 Christian Dersch <lupinix@fedoraproject.org> - 2.0.0-1
- Final 2.0.0 release

* Sun Jul 15 2018 Christian Dersch <lupinix@fedoraproject.org> - 2.0.0-0.5dev1
- Import upstream fix for https://github.com/PyCQA/pylint/issues/2238

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.4dev1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-0.3dev1
- Rebuilt for Python 3.7

* Tue Jun 05 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-0.2dev1
- Update to 2.0.0dev1

* Mon May 21 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-0.1dev0
- Update to 2.0.0dev0
- Drop python2-pylint (to it's own source RPM)

* Sun Apr 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.7.5-3
- Conditionalize python2 subpackage, don't build it on RHEL > 7

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.7.5-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Tue Feb 27 2018 Gwyn Ciesla <limburgher@gmail.com> - 1.7.5-1
- 1.7.5.

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.7.4-4
- Escape macros in %%changelog

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 18 2018 Karsten Hopp <karsten@redhat.com> - 1.7.4-2
- update requirements

* Tue Oct 10 2017 Christian Dersch <lupinix@mailbox.org> - 1.7.4-1
- new version
- added BR: python2-configparser, python(2,3)-mccabe for proper test execution

* Thu Aug 31 2017 Brian C. Lane <bcl@redhat.com> - 1.7.2-2
- Remove module that wasn't actually moved. (#1483869)

* Wed Aug 02 2017 Gwyn Ciesla <limburgher@gmail.com> - 1.7.2-1
- 1.7.2.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun May 14 2017 Christian Dersch <lupinix@mailbox.org> - 1.7.1-1
- new version
- we need pytest-runner now
- pylint-gui has been removed upstream

* Wed Apr 5 2017 Orion Poplawski <orion@cora.nwra.com> - 1.6.5-4
- Provide python major version links (bug #1439070)

* Tue Mar 28 2017 Orion Poplawski <orion@cora.nwra.com> - 1.6.5-3
- Split python2 modules into sub-packages
- Make python3 the default for scripts on Fedora 26+

* Mon Mar 13 2017 Orion Poplawski <orion@cora.nwra.com> - 1.6.5-2
- Enable python3 build for EPEL
- Include python3-pylint-gui __pycache__ files in gui package (bug #1422609)
- Cleanup spec
- Run tests, but they currently fail

* Wed Feb 22 2017 Christian Dersch <lupinix@mailbox.org> - 1.6.5-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.6.4-2
- Rebuild for Python 3.6

* Mon Oct 03 2016 Jon Ciesla <limburgher@gmail.com> - 1.6.4-1
- Upstream v1.6.4

* Fri Jul 29 2016 Jon Ciesla <limburgher@gmail.com> - 1.5.6-1
- Upstream v1.5.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.5-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 07 2016 Brian C. Lane <bcl@redhat.com> 1.5.5-1
- Upstream v1.5.5

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 18 2016 Brian C. Lane <bcl@redhat.com> 1.5.4-1
- Upstream v1.5.4

* Mon Jan 04 2016 Brian C. Lane <bcl@redhat.com> 1.5.2-1
- Upstream v1.5.2

* Thu Dec 10 2015 Brian C. Lane <bcl@redhat.com> 1.5.1-1
- Upstream v1.5.1
- Remove %%check section, it does not work due to unpackaged requirements.
- Update description from the package's __pkginfo__.py file.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Mathieu Bridon <bochecha@daitauha.fr> - 1.4.3-2
- Drop python3 requirements from the python2 package.
- Add missing requirement on six.

* Tue Apr 28 2015 Brian C. Lane <bcl@redhat.com> 1.4.3-1
- Upstream v1.4.3

* Fri Jan 30 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-3
- Exclude the python3-* files from the python2 package

* Thu Jan 29 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-2
- Add python-six requirement

* Wed Jan 28 2015 Brian C. Lane <bcl@redhat.com> 1.4.1-1
- Upstream v1.4.1

* Mon Oct 27 2014 Brian C. Lane <bcl@redhat.com> 1.3.1-2
- python3-pylint-gui needs python3-tkinter

* Fri Oct 03 2014 Brian C. Lane <bcl@redhat.com> 1.3.1-1
- Upstream v1.3.1
  Dropped patches included in upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun 02 2014 Brian C. Lane <bcl@redhat.com> 1.2-6
- Add python3-astroid and python3-setuptools as Requires (#1103479)

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 09 2014 Brian C. Lane <bcl@redhat.com> 1.2-4
- Fix a potential AttributeError when checking for `reversed` arguments.
  https://bitbucket.org/logilab/pylint/commits/93babaf6bffc59a49c75319d9850086b4935edbc

* Thu May 08 2014 Brian C. Lane <bcl@redhat.com> 1.2-3
- fix explicit check of python script
  https://bitbucket.org/logilab/pylint/issue/219/

* Thu Apr 24 2014 Brian C. Lane <bcl@redhat.com> 1.2-2
- Patch to Fix --init-hook typo (dshea)
  https://bitbucket.org/logilab/pylint/issue/211/init-hook-no-longer-works

* Tue Apr 22 2014 Brian C. Lane <bcl@redhat.com> 1.2-1
- Upstream v1.2

* Thu Feb 27 2014 Brian C. Lane <bcl@redhat.com> 1.1.0-1
- Upstream v1.1.0
  Drop patch included in upstream

* Thu Oct 24 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-3
- Switching on python3 support

* Tue Sep 03 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-2
- Add upstream patch for epylint input validation (#981859)

* Tue Aug 13 2013 Brian C. Lane <bcl@redhat.com> 1.0.0-1
- Upstream 1.0.0

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.26.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Brian C. Lane <bcl@redhat.com> 0.26.0-1
- Upstream 0.26.0
- Add python3-pylint and python3-pylint-gui subpackages. Not ready to turn it
  on yet due to this upstream bug: http://www.logilab.org/ticket/110213

* Fri Aug 03 2012 Brian C. Lane <bcl@redhat.com> 0.25.2-1
- Upstream 0.25.2

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Mar 14 2012 Brian C. Lane <bcl@redhat.com> 0.25.1-1
- Upstream 0.25.1

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Nov 18 2011 Brian C. Lane <bcl@redhat.com> - 0.25.0-1
- Upstream 0.25.0

* Fri Jul 29 2011 Brian C. Lane <bcl@redhat.com> - 0.24.0-1
- Upstream 0.24.0

* Mon Mar 28 2011 Brian C. Lane <bcl@redhat.com> - 0.23-0.1
- Upstream 0.23.0
- Add unit tests to spec

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 06 2010 Brian C. Lane <bcl@redhat.com> - 0.22.0-2
- Add version to requirement for python-logilab-astng so that updates will
  work correctly.

* Mon Nov 29 2010 Brian C. Lane <bcl@redhat.com> - 0.22.0-1
- Upstream 0.22.0

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.21.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jul 08 2010 Brian C. Lane <bcl@redhat.com> - 0.21.1-1
- Upstream 0.21.1
- Removed patch for 500272, fixed upstream - http://www.logilab.org/ticket/22962

* Mon Apr 05 2010 Brian C. Lane <bcl@redhat.com> - 0.20.0-2
- Added patch for bug 500272 (exception with --disable-msg-cat)

* Fri Mar 26 2010 Brian C.Lane <bcl@redhat.com> - 0.20.0-1
- Upstream 0.20.0
- Added python-setuptools to BuildRequires

* Sun Aug 30 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.18.1-1
- Upstream 0.18.1 (bugfixes and small enhancements)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.18.0-1
- Upstream 0.18.0 (bugfixes and minor feature updates)

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jan 28 2009 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.16.0-1
- Upstream 0.16.0

* Tue Dec 30 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.15.2-1
- Upstream 0.15.2

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.14.0-2
- Rebuild for Python 2.6

* Thu Jan 17 2008 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.14.0-1
- Upstream 0.14.0
- Package the .egg-info files.

* Mon Dec 24 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.2-1
- Upstream 0.13.2
- Adjust license to a more precise version
- Fix docs to be valid utf-8

* Sun Apr 01 2007 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.13.1-1
- Upstream 0.13.1

* Sun Dec 17 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.2-1
- Upstream 0.12.2
- Add COPYING to -gui

* Tue Sep 26 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.12.1-1
- Upstream 0.12.1
- Require the renamed python-logilab-astng

* Mon May 01 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.11.0-0
- Version 0.11.0

* Sun Mar 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.10.0-1
- Version 0.10.0

* Thu Jan 12 2006 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.9.0-1
- Version 0.9.0
- Add COPYING to docs

* Sun Nov 13 2005 Konstantin Ryabitsev <icon@fedoraproject.org> - 0.8.1-1
- Version 0.8.1
- Add dependency on python-astng
- Drop artificial version requirement on python-logilab-common

* Mon Jun 13 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.7.0-1
- Version 0.7.0
- No longer in the logilab subdir
- Disttagging

* Mon May 09 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-4
- Install the pylint.1 manfile.
- Add examples and elisp dirs to docs.

* Thu May 05 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-3
- Only doc the .txt files.
- Don't buildrequire python-logilab-common
- Fix paths.

* Tue Apr 26 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-2
- Ghost .pyo files.
- Remove the test dir, as it doesn't do anything.
- Separate the gui package, which depends on tkinter.
- Don't own site-packages/logilab, which is owned by
  python-logilab-common.

* Fri Apr 22 2005 Konstantin Ryabitsev <icon@linux.duke.edu> - 0.6.4-1
- Initial packaging.
