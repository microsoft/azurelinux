# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           python-manuel
Version:        1.12.4
Release:        14%{?dist}
Summary:        Build tested documentation

# The content is Apache-2.0.  Other licenses are due to files copied in by
# Sphinx.
# _static/_sphinx_javascript_frameworks_compat.js: BSD-2-Clause
# _static/alabaster.css: BSD-3-Clause
# _static/basic.css: BSD-2-Clause
# _static/check-solid.svg: MIT
# _static/clipboard.min.js: MIT
# _static/copy-button.svg: MIT
# _static/copybutton.css: MIT
# _static/copybutton.js: MIT
# _static/copybutton_funcs.js: MIT
# _static/custom.css: BSD-3-Clause
# _static/doctools.js: BSD-2-Clause
# _static/documentation_options.js: BSD-2-Clause
# _static/file.png: BSD-2-Clause
# _static/jquery*.js: MIT
# _static/language_data.js: BSD-2-Clause
# _static/minus.png: BSD-2-Clause
# _static/plus.png: BSD-2-Clause
# _static/searchtools.js: BSD-2-Clause
# _static/underscore*.js: MIT
# genindex.html: BSD-2-Clause
# search.html: BSD-2-Clause
# searchindex.js: BSD-2-Clause
License:        Apache-2.0 AND BSD-3-Clause AND BSD-2-Clause AND MIT
URL:            https://pypi.python.org/pypi/manuel
Source0:        https://github.com/benji-york/manuel/archive/%{version}/manuel-%{version}.tar.gz
# Work around a test failure due to more explicit names in python 3.11
Patch0:         %{name}-test.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist myst-parser}
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-copybutton}

%description
Manuel lets you mix and match traditional doctests with custom test
syntax.  Several plug-ins are included that provide new test syntax.
You can also create your own plug-ins.

%package -n python3-manuel
Summary:        Build tested documentation
Provides:       bundled(js-jquery)

%description -n python3-manuel
Manuel lets you mix and match traditional doctests with custom test
syntax.  Several plug-ins are included that provide new test syntax.
You can also create your own plug-ins.

%prep
%autosetup -n manuel-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -x tests

%build
%pyproject_wheel
sphinx-build -c sphinx src/manuel docs
rm -fr docs/.buildinfo docs/.doctrees

rst2html --no-datestamp CHANGES.rst CHANGES.html

%install
%pyproject_install
%pyproject_save_files manuel

%check
export PYTHONPATH=$PWD/build/lib
cp -p src/manuel/myst-markdown.md build/lib/manuel
%{python3} -m unittest manuel.tests.test_suite

%files -n python3-manuel -f %{pyproject_files}
%doc CHANGES.html docs/*
%license COPYRIGHT.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.12.4-14
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.12.4-13
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.12.4-11
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 1.12.4-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 1.12.4-4
- Rebuilt for Python 3.12

* Thu Feb 23 2023 Jerry James <loganjerry@gmail.com> - 1.12.4-3
- Dynamically generate BuildRequires

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Jerry James <loganjerry@gmail.com> - 1.12.4-2
- Convert License tag to SPDX

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 24 2022 Jerry James <loganjerry@gmail.com> - 1.12.4-1
- Version 1.12.4

* Mon Jun 20 2022 Jerry James <loganjerry@gmail.com> - 1.11.2-2
- Add -test patch to work around test failure with python 3.11

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.11.2-2
- Rebuilt for Python 3.11

* Mon May 16 2022 Jerry James <loganjerry@gmail.com> - 1.11.2-1
- Version 1.11.2
- Drop upstreamed python 3.11 patch

* Wed Feb 23 2022 Jerry James <loganjerry@gmail.com> - 1.10.1-15
- Add patch for python 3.11 compatibility

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.10.1-12
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.10.1-9
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 16 2019 Jerry James <loganjerry@gmail.com> - 1.10.1-7
- Use zope.testing instead of zope.testrunner

* Mon Sep 16 2019 Jerry James <loganjerry@gmail.com> - 1.10.1-6
- Drop the python2 subpackage (bz 1752149)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.10.1-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 17 2018 Jerry James <loganjerry@gmail.com> - 1.10.1-2
- Restore accidentally dropped python3 subpackage

* Sat Nov 17 2018 Jerry James <loganjerry@gmail.com> - 1.10.1-1
- New upstream release

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-4
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.9.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Jerry James <loganjerry@gmail.com> - 1.9.0-1
- New upstream release

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.8.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Feb  1 2016 Jerry James <loganjerry@gmail.com> - 1.8.0-4
- Comply with latest python packaging guidelines

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Jerry James <loganjerry@gmail.com> - 1.8.0-2
- Note bundled jquery

* Wed Jul 23 2014 Jerry James <loganjerry@gmail.com> - 1.8.0-1
- New upstream release
- Drop upstreamed patch
- Drop conf.py, now included in upstream source
- Avoid use of py3dir, which is not cleaned

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Jan 24 2014 Ralph Bean <rbean@redhat.com> - 1.7.2-4
- Conditionalized python3 for epel builds.
- Defined python2 macros for el6.
- Added python3 tests to the check section.

* Thu Oct  3 2013 Jerry James <loganjerry@gmail.com> - 1.7.2-3
- Update project and source URLs

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 18 2013 Jerry James <loganjerry@gmail.com> - 1.7.2-1
- New upstream release

* Wed Feb 27 2013 Jerry James <loganjerry@gmail.com> - 1.7.1-2
- Add python-six Requires (bz 915431)

* Tue Feb 19 2013 Jerry James <loganjerry@gmail.com> - 1.7.1-1
- New upstream release

* Mon Jan 28 2013 Jerry James <loganjerry@gmail.com> - 1.6.1-1
- New upstream release

* Fri Aug 10 2012 Jerry James <loganjerry@gmail.com> - 1.6.0-3
- Rebuild for python 3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 23 2012 Jerry James <loganjerry@gmail.com> - 1.6.0-1
- New upstream release
- Python3 subpackage now possible

* Tue Jan 10 2012 Jerry James <loganjerry@gmail.com> - 1.5.0-4
- Rebuild for bz 772699

* Sun Jan  8 2012 Jerry James <loganjerry@gmail.com> - 1.5.0-3
- Mass rebuild for Fedora 17

* Wed Apr 27 2011 Jerry James <loganjerry@gmail.com> - 1.5.0-2
- Do not Require python-zope-testing
- Change Group to Development/Libraries
- Remove text files from python_sitelib; they are already in docs

* Tue Apr 26 2011 Jerry James <loganjerry@gmail.com> - 1.5.0-1
- Initial RPM
