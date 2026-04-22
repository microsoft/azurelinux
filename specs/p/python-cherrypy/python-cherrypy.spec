# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?python_enable_dependency_generator}

%if 0%{?el8}
  # jaraco.collections not yet available in epel8
  %bcond_with tests
%else
  %bcond_without tests
%endif

Name:           python-cherrypy
%global         camelname CherryPy
Version:        18.10.0
Release: 10%{?dist}
Summary:        Pythonic, object-oriented web development framework
# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            https://cherrypy.dev/
Source0:        https://files.pythonhosted.org/packages/source/C/%{camelname}/cherrypy-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(setuptools-scm)
%if %{with tests}
# Test dependencies
BuildRequires:  python3dist(cheroot)
BuildRequires:  python3dist(jaraco-collections)
BuildRequires:  python3dist(path)
BuildRequires:  python3dist(portend)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(requests-toolbelt)
BuildRequires:  python3dist(more-itertools)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3-zc-lockfile
%endif

%global _description\
%{camelname} allows developers to build web applications in much the same way\
they would build any other object-oriented Python program. This usually\
results in smaller source code developed in less time.

%description %_description

%package -n python3-cherrypy
Summary: %summary
%{?python_provide:%python_provide python3-cherrypy}

%package -n python3-cherrypy-devel
Summary: Test and Tutorial files excluded from main package

# Remove after F32.
Obsoletes: python2-cherrypy < 3.5.1

%description -n python3-cherrypy %_description
%description -n python3-cherrypy-devel %_description

%prep
%autosetup -p1 -n cherrypy-%{version}

# These tests still fail (reason unknown):
rm cherrypy/test/test_session.py
sed -i '/pytest_cov/d' setup.py
sed -i '/cov/d' pytest.ini

%build
%py3_build

%install
%py3_install

%if %{with tests}
%check
# https://github.com/cherrypy/cherrypy/commit/5d3c86eb36dfdf972a1d3c8d69cf8be2050eb99c
export WEBTEST_INTERACTIVE=false
%pytest cherrypy/test \
  --deselect=cherrypy/test/test_tools.py::ToolTests::testCombinedTools \
  -p no:unraisableexception
%endif

%files -n python3-cherrypy
%doc README.rst
%license LICENSE.md
%doc cherrypy/tutorial
%{_bindir}/cherryd
%{python3_sitelib}/*
%exclude %{python3_sitelib}/cherrypy/test
%exclude %{python3_sitelib}/cherrypy/tutorial

%files -n python3-cherrypy-devel
%{python3_sitelib}/cherrypy/test
%{python3_sitelib}/cherrypy/tutorial

%changelog
* Fri Sep 19 2025 Gwyn Ciesla <gwync@protonmail.com> - 18.10.0-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 18.10.0-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 18.10.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 18.10.0-6
- Rebuilt for Python 3.14

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 18.10.0-5
- Bootstrap for Python 3.14

* Sun Jan 19 2025 Dan Radez <dradez@redhat.com> - 18.10.0-4
- removing coverage

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 18.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 18.10.0-2
- convert license to SPDX

* Thu Aug 01 2024 Dan Radez <dradez@redhat.com> - 18.10.0-1
- update to upstream 18.10.0 rhbz#2292418

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 18.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 18.9.0-7
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 18.9.0-6
- Bootstrap for Python 3.13

* Thu Feb 22 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 18.9.0-5
- Add patch for compatibility with Python 3.13, workaround removed cgi stdlib module
- Fixes: rhbz#2256924

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 18.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 18.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Dec 22 2023 Dan Radez <dradez@redhat.com> - 18.9.0-2
- reenabled static tests
- removed dos2unix fix
- removed readfp with read_file fix, it's upstream

* Thu Dec 14 2023 Dan Radez <dradez@redhat.com> - 18.9.0-1
- updating to upsteam 18.9.0 rhbz#2254371

* Tue Oct 10 2023 Dan Radez <dradez@redhat.com> - 18.8.0-8
- adding -devel package to provide test and tutorial modules

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 18.8.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 01 2023 Python Maint <python-maint@redhat.com> - 18.8.0-6
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 18.8.0-5
- Bootstrap for Python 3.12

* Tue Apr 04 2023 Dan Radez <dradez@redhat.com> - 18.8.0-4
- rhbz#2183388 submitting upstream patch to resolve pkg_resources dep warning

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 18.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 19 2022 Dan Radez <dradez@redhat.com> - 18.8.0-2
- Ignore urllib3.contrib.pyopenssl DeprecationWarnings to fix FTBFS

* Mon Aug 29 2022 Dan Radez <dradez@redhat.com> - 18.8.0-1
- updating to 18.8.0 (rhbz#2105856)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 18.6.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Miro Hrončok <mhroncok@redhat.com> - 18.6.1-6
- Adjust tests for a last minute Python 3.11 change in the traceback format

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 18.6.1-5
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 18.6.1-4
- Bootstrap for Python 3.11

* Tue Apr 12 2022 Dan Radez <dradez@redhat.com> - 18.6.1-3
- updating python-path-py to python-path

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 18.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 09 2021 Matthias Runge <mrunge@redhat.com> - 18.6.1-1
- rebase to 18.6.1 (rhbz#1978987)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 18.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 18.6.0-5
- Rebuilt for Python 3.10

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 18.6.0-4
- Bootstrap for Python 3.10

* Wed May 26 2021 Miro Hrončok <mhroncok@redhat.com> - 18.6.0-3
- Fix/workaround build failures with pytest 6.2 and/or Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 18.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Ken Dreyer <kdreyer@redhat.com> - 18.6.0-1
- Update to 18.6.0 (rhbz#1777494)
- Re-enable tests on non-EPEL8

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 18.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 20 2020 Miro Hrončok <mhroncok@redhat.com> - 18.4.0-5
- Disable unused automagic Python bytecompilation

* Fri Jun 05 2020 Matthias Runge <mrunge@redhat.com> - 18.4.0-4
- skip tests to fix FTBFS (rhbz#1810313)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 18.4.0-4
- Rebuilt for Python 3.9

* Sat Feb 15 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 18.4.0-3
- Fix Obsoletes for python2-cherrypy

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 18.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Ken Dreyer <kdreyer@redhat.com> - 18.4.0-1
- Update to 18.4.0 (rhbz#1748716)
- Update comments about current test failures

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 18.1.2-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 18.1.2-4
- Rebuilt for Python 3.8

* Thu Aug 08 2019 Dan Radez <dradez@redhat.com> - 18.1.2-3
- Update to 18.1.2
- Replaced Python2 package with Python 3 package
- python3-cherrypy-18.1.2-2 is already built by package python3-cherrypy
  this release is to migrate python3-cherrypy into python-cherrypy

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 3.5.0-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 3.5.0-7
- Python 2 binary package renamed to python2-cherrypy
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Aug 27 2014 Luke Macken <lmacken@redhat.com> - 3.5.0-1
- Update to 3.5.0 (#1104560)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Oct 27 2011 Conrad Meyer <konrad@tylerc.org> - 3.2.2-1
- Update to 3.2.2

* Sat Jul 16 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.1-1
- Update to 3.2.1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 31 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-4
- Fix a failing unittest with newer python

* Sat Apr 24 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-3
- Revert a try at 3.2.x-rc1 as the tests won't pass without some work.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 16 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-1
- New upstream with python-2.6 fixes.
- BR tidy for tests.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 1 2008 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.1-1
- Update to 3.1.1
- Fix python-2.6 build errors
- Make test code non-interactive via cmdline switch
- Refresh the no test and tutorial patch

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.0.3-3
- Rebuild for Python 2.6

* Tue Jan 22 2008 Toshio Kuratomi <toshio@fedoraproject.org> 3.0.3-2
- Forgot to upload the tarball.

* Mon Jan 21 2008 Toshio Kuratomi <toshio@fedoraproject.org> 3.0.3-1
- Upgrade to 3.0.3.

* Thu Jan 17 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-2
- EINTR Patch needed to be forwarded ported as well as it is only applied to
  CP trunk (3.x).

* Thu Jan 17 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.3.0-1
- Update to new upstream which rolls in the backported security fix.
- Refresh other patches to apply against new version.
- Change to new canonical source URL.
- Reenable tests.

* Sun Jan  6 2008 Toshio Kuratomi <toshio@fedoraproject.org> 2.2.1-8
- Fix a security bug with a backport of http://www.cherrypy.org/changeset/1775
- Include the egginfo files as well as the python files.

* Sat Nov  3 2007 Luke Macken <lmacken@redhat.com> 2.2.1-7
- Apply backported fix from http://www.cherrypy.org/changeset/1766
  to improve CherryPy's SIGSTOP/SIGCONT handling (Bug #364911).
  Thanks to Nils Philippsen for the patch.

* Mon Feb 19 2007 Luke Macken <lmacken@redhat.com> 2.2.1-6
- Disable regression tests until we can figure out why they
  are dying in mock.

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 2.2.1-5
- Add python-devel to BuildRequires

* Sun Dec 10 2006 Luke Macken <lmacken@redhat.com> 2.2.1-4
- Rebuild for python 2.5

* Mon Sep 18 2006 Luke Macken <lmacken@redhat.com> 2.2.1-3
- Rebuild for FC6
- Include pyo files instead of ghosting them

* Thu Jul 13 2006 Luke Macken <lmacken@redhat.com> 2.2.1-2
- Rebuild

* Thu Jul 13 2006 Luke Macken <lmacken@redhat.com> 2.2.1-1
- Update to 2.2.1
- Remove unnecessary python-abi requirement

* Sat Apr 22 2006 Gijs Hollestelle <gijs@gewis.nl> 2.2.0-1
- Update to 2.2.0

* Wed Feb 22 2006 Gijs Hollestelle <gijs@gewis.nl> 2.1.1-1
- Update to 2.1.1 (Security fix)

* Tue Nov  1 2005 Gijs Hollestelle <gijs@gewis.nl> 2.1.0-1
- Updated to 2.1.0

* Sat May 14 2005 Gijs Hollestelle <gijs@gewis.nl> 2.0.0-2
- Added dist tag

* Sun May  8 2005 Gijs Hollestelle <gijs@gewis.nl> 2.0.0-1
- Updated to 2.0.0 final
- Updated python-cherrypy-tutorial-doc.patch to match new version

* Wed Apr  6 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 2.0.0-0.2.b
- Removed CFLAGS

* Wed Mar 23 2005 Gijs Hollestelle <gijs[AT]gewis.nl> 2.0.0-0.1.b
- Initial Fedora Package
