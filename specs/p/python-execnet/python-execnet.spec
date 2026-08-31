# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname execnet

# Some of the BuildRequires are used in tests only when installed.
# To speedup bootstrap of the next Python version in Fedora
# we allow disabling them.
%bcond optional_test_deps %{undefined rhel}

Name:           python-%{srcname}
Version:        2.1.2
Release:        1%{?dist}
Summary:        Distributed Python deployment and communication
License:        MIT
URL:            https://github.com/pytest-dev/execnet
Source0:        %pypi_source

BuildArch:      noarch
BuildRequires:  make
BuildRequires:  /usr/bin/ps

%global _description %{expand:
execnet provides a share-nothing model with channel-send/receive
communication for distributing execution across many Python
interpreters across version, platform and network barriers. It has a
minimal and fast API targetting the following uses:

 * distribute tasks to (many) local or remote CPUs
 * write and deploy hybrid multi-process applications
 * write scripts to administer multiple environments
}

%description %_description

%package -n python3-%{srcname}
Summary:        Elastic Python Deployment
BuildRequires:  python3-devel
%if %{with optional_test_deps}
#BuildRequires: python3-eventlet -- retired in Fedora 41+
BuildRequires:  python3-gevent
%endif
BuildRequires:  %{_bindir}/sphinx-build-3
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}
# remove shebangs and fix permissions
find . -type f -a \( -name '*.py' -o -name 'py.*' \) \
   -exec sed -i '1{/^#!/d}' {} \; \
   -exec chmod u=rw,go=r {} \;


%generate_buildrequires
%pyproject_buildrequires -t


%build
SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_wheel
make -C doc html PYTHONPATH=$(pwd)/src
# remove hidden file
rm doc/_build/html/.buildinfo


%install
SETUPTOOLS_SCM_PRETEND_VERSION=%{version}
%pyproject_install
%pyproject_save_files -l execnet


%check
PYTEST_SELECT='not test_popen_io[gevent-sys.executable]'
PYTEST_SELECT+=' and not [gevent-socket]'
PYTEST_SELECT+=' and not [eventlet-socket]'
PYTEST_SELECT+=' and not [python2.7]'
PYTHONPATH=$(pwd)/src \
py.test-%{python3_version} -r s \
  -k "$PYTEST_SELECT" \
  testing \
  --timeout=30


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%doc doc/_build/html
%license LICENSE


%changelog
* Sat Nov 15 2025 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.2-1
- Update to 2.1.2.

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.1.1-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.1.1-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 2.1.1-7
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.1.1-6
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Aug 12 2024 Miro Hrončok <mhroncok@redhat.com> - 2.1.1-4
- Generate BuildRequires instead of manually listing them
- Drop some unused BuildRequires

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.1.1-2
- Bootstrap for Python 3.13

* Sun Apr 14 2024 Thomas Moschny <thomas.moschny@gmx.de> - 2.1.1-1
- Update to 2.1.1.
- Modernize spec file.

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Miro Hrončok <mhroncok@redhat.com> - 1.9.0-11
- Run gevent tests during build

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.9.0-10
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Nov 30 2022 Lumír Balhar <lbalhar@redhat.com> - 1.9.0-8
- Fix compatibility with pytest 7.2 (#2142053)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jun 18 2022 Python Maint <python-maint@redhat.com> - 1.9.0-6
- Rebuilt for Python 3.11

* Wed Jun 15 2022 Ali Erdinc Koroglu <aekoroglu@fedoraproject.org> - 1.9.0-5
- apipkg dependency removed from 1.9.0

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 1.9.0-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.0-2
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jul  9 2021 Thomas Moschny <thomas.moschny@gmx.de> - 1.9.0-1
- Update to 1.9.0.

* Fri Jul  9 2021 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.1-1
- Update to 1.8.1.

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8.0-3
- Rebuilt for Python 3.10

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.8.0-2
- Bootstrap for Python 3.10

* Sat May  8 2021 Thomas Moschny <thomas.moschny@gmx.de> - 1.8.0-1
- Update to 1.8.0.

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.7.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep  2 2019 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.1-1
- Update to 1.7.1.

* Tue Aug 27 2019 Thomas Moschny <thomas.moschny@gmx.de> - 1.7.0-1
- Update to 1.7.0.

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-4
- Rebuilt for Python 3.8

* Mon Aug 12 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-3
- Subpackage python2-execnet has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Apr 01 2019 Miro Hrončok <mhroncok@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Mon Mar 18 2019 Ken Dreyer <kdreyer@redhat.com> - 1.5.0-7
- Update Summary to match upstream
- Use HTTPS in upstream URL
- License is now MIT-only
- Use standard pypi_source macro
- Remove explicit Requires
- Remove Sphinx docs generation on py2 (rhbz#1690057)
- Drop double listing of python3/LICENSE file
- Patch tests for latest apipkg (rhbz#1690057)
- Patch docs config for Sphinx 2 (rhbz#1690057)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.5.0-5
- Drop explicit locale setting for python3, use C.UTF-8 for python2
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.0-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Nov 18 2017 Thomas Moschny <thomas.moschny@gmx.de> - 1.5.0-1
- Update to 1.5.0.
- Move BRs to their respective subpackages.
- Update Source URL.

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Ken Dreyer <ktdreyer@ktdreyer.com> - 1.4.1-6
- drop hgdistver dependency by overriding setuptools-scm version (rhbz#1470305)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.4.1-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 23 2016 Thomas Moschny <thomas.moschny@gmx.de> - 1.4.1-1
- Update to 1.4.1.
- Apipkg has been debundled.
- Add BR on python-setuptools_scm.
- Follow updated Python packaging guidelines.
- Spec file cleanups.

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Apr 20 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.0-2
- Re-add dependency on python-hgdistver, see bz#1208984.
- Apply updated Python packaging guidelines.
- Mark LICENSE with %%license.

* Sun Mar  8 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.3.0-1
- Update to 1.3.0.
- Drop obsolete patches.

* Mon Jan 19 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.0-5
- Bump and rebuild in rawhide.

* Sun Jan 18 2015 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.0-4.1
- Conditionalize dependency on python-gevent, in order to update
  python-execnet for F20 and add it to EPEL6 (bugs 1178233 and
  1178235). Suggested by Ken Dreyer <ktdreyer@ktdreyer.com>.
- Disable test failing on Rawhide and F21.

* Wed Jun 18 2014 Orion Poplawski <orion@cora.nwra.com> - 1.2.0-4
- Add patch to fix failing test with old pytest on EL7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Apr 18 2014 Thomas Moschny <thomas.moschny@gmx.de> - 1.2.0-1
- Update to 1.2.0.
- Update license.
- Modernize spec file.
- Remove patch not needed anymore.
- Update build requirements.
- Only run tests in 'testing'.

* Sun Aug 18 2013 Thomas Moschny <thomas.moschny@gmx.de> - 1.1-6
- Fixing FTBFS (rhbz#992888, rhbz#914405): Add patch for failing
  tests, disable other failing tests for now.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.1-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.1-1
- Update to 1.1.
- Update description.
- Remove patch applied upstream.

* Tue Jan 17 2012 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.9-3
- Add upstream patch for failing test.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Sep  4 2011 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.9-1
- Update to 1.0.9.
- Use BR on python-setuptools instead of python-setuptools-devel.
- Create Python3 subpackage.
- Fix dependencies.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 31 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.8-1
- Update to 1.0.8.

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.0.7-1.1
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul 10 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.7-1
- Update to 1.0.7.
- Do cleanups already in %%prep to avoid inconsistent mtimes between
  source files and bytecode.

* Sat May  8 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.6-1
- Update to 1.0.6.

* Sun Feb 14 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.5-1
- Update to 1.0.5.

* Wed Jan 27 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.4-1
- Update to 1.0.4.
- No need to skip tests.

* Fri Jan  8 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.2-3
- Remove .buildinfo file from the doc dir.

* Thu Jan  7 2010 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.2-2
- Skip tests that need network access.

* Tue Dec 29 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.2-1
- Update to 1.0.2.

* Sat Dec  5 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.1-1
- Update to 1.0.1.
- Build and include HTML documentation.
- Be a bit more explicit in the %%files section.

* Sat Nov 28 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-1
- Update to 1.0.0.

* Sun Nov 22 2009 Thomas Moschny <thomas.moschny@gmx.de> - 1.0.0-0.1.b3
- New package.
