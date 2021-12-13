%{!?python3_pkgversion: %global python3_pkgversion 3}
%{!?python3_version: %define python3_version %(python3 -c "import sys; sys.stdout.write(sys.version[:3])")}
%{!?python3_sitelib: %define python3_sitelib %(python3 -c "from distutils.sysconfig import get_python_lib;print(get_python_lib())")}
%{!?__python3: %global __python3 /usr/bin/python3}
%{!?py3_build: %define py3_build CFLAGS="%{optflags}" %{__python3} setup.py build}
%{!?py3_install: %define py3_install %{__python3} setup.py install --skip-build --root %{buildroot}}

%global pypi_name decorator

Summary:        Module to simplify usage of decorators
Name:           python-%{pypi_name}
Version:        4.4.2
Release:        4%{?dist}
License:        BSD
URL:            https://github.com/micheles/decorator
#Source0:       https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source0:        https://files.pythonhosted.org/packages/source/d/%{pypi_name}/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel

%description
The aim of the decorator module is to simplify the usage of decorators for
the average programmer, and to popularize decorators usage giving examples
of useful decorators, such as memoize, tracing, redirecting_stdout, locked,
etc.  The core of this module is a decorator factory called decorator.

%package -n python3-decorator
Summary:        Module to simplify usage of decorators in python3
%{?python_provide:%python_provide python3-decorator}

%description -n python3-decorator
The aim of the decorator module is to simplify the usage of decorators for
the average programmer, and to popularize decorators usage giving examples
of useful decorators, such as memoize, tracing, redirecting_stdout, locked,
etc.  The core of this module is a decorator factory called decorator.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

# Remove this when https://github.com/micheles/decorator/issues/32 is fixed.
find %{buildroot} -name SOURCES.txt~ -exec rm -f {} \;

%check
%{__python3} setup.py test

%files -n python3-%{pypi_name}
%doc README.rst CHANGES.md
%license LICENSE.txt
%{python3_sitelib}/decorator.py
%{python3_sitelib}/decorator-*.egg-info/
%{python3_sitelib}/__pycache__/*

%changelog
* Wed Dec 09 2020 Steve Laughman <steve.laughman@microsoft.com> - 4.4.2-4
- Initial CBL-Mariner import from Fedora 33 (license: MIT)
* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild
* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 4.4.2-2
- Rebuilt for Python 3.9
* Fri Apr 03 2020 Michal Konečný <mkonecny@redhat.com> - 4.4.2-1
- new version
  Remove python39.patch no longer needed
* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild
* Thu Jan 16 2020 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-5
- Subpackage python2-decorator has been removed
  See https://fedoraproject.org/wiki/Changes/RetirePython2
* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)
* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 4.4.0-3
- Rebuilt for Python 3.8
* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild
* Sat Jun 22 2019 Kevin Fenzi <kevin@scrye.com> - 4.4.0-1
- Update to 4.4.0. Fixes bug #1669189
* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild
* Wed Jul 25 2018 Pierre-Yves Chibon <pingou@pingoured.fr> - 4.3.0-1
- Update to 4.3.0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild
* Thu Jun 14 2018 Miro Hrončok <mhroncok@redhat.com> - 4.2.1-2
- Rebuilt for Python 3.7
* Wed Feb  7 2018 Haïkel Guémar <hguemar@fedoraproject.org> - 4.2.1-1
- Upstream 4.2.1
* Tue Jan 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.1.2-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)
* Sat Sep 16 2017 Kevin Fenzi <kevin@scrye.com> - 4.1.2-1
- Update to 4.1.2. Fixes bug #1471373
* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild
* Mon Jan 23 2017 Fabio Alessandro Locati <fale@fedoraproject.org> - 4.0.11-1
- Update to 4.0.11
* Thu Dec 29 2016 Kevin Fenzi <kevin@scrye.com> - 4.0.10-5
- Remove SOURCES.txt~ file. Fixes bug #1404634
* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 4.0.10-4
- Rebuild for Python 3.6
* Mon Aug 29 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 4.0.10-3
- SPEC Cleanup
- Remove unused build requires
* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.10-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages
* Tue Jun 07 2016 Kevin Fenzi <kevin@scrye.com> - 4.0.10-1
- Update to 4.0.10. Fixes bug #1343523
* Mon Apr 04 2016 Ralph Bean <rbean@redhat.com> - 4.0.9-1
- new version
* Tue Feb 2 2016 Orion Poplawski <orion@cora.nwra.com> - 4.0.6-2
- Modernize spec
- Fix python3 package file ownership
- Run python3 tests
* Fri Dec 11 2015 Ralph Bean <rbean@redhat.com> - 4.0.6-1
- new version
* Wed Nov 04 2015 Robert Kuska <rkuska@redhat.com> - 4.0.4-2
- Rebuilt for Python3.5 rebuild
* Fri Sep 25 2015 Ralph Bean <rbean@redhat.com> - 4.0.4-1
- new version
* Wed Sep 16 2015 Ralph Bean <rbean@redhat.com> - 4.0.2-1
- new version
* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild
* Mon Mar 23 2015 Ralph Bean <rbean@redhat.com> - 3.4.2-1
- new version
- The documentation.py files are now gone from upstream.
* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild
* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 3.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild
* Thu Oct 18 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 3.4.0-1
- New upstream release
* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.3-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3
* Fri Aug  3 2012 David Malcolm <dmalcolm@redhat.com> - 3.3.3-3
- remove rhel logic from with_python3 conditional
* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Tue Apr 24 2012 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.3-1
- New upstream release
* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Fri Sep 2 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.2-1
- New upstream release
* Thu Apr 28 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.1-1
- Upstream update 3.3.1 that deprecates the .decorated attribute name in
  favor of .__wrapped__
* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild
* Sat Jan 1 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 3.3.0-1
- Upstream update 3.3.0 that adds function annotation support for python3 code
* Wed Dec 1 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.1-1
- Upstream bugfix 3.2.1
- Enable unittests for python3
* Mon Aug 23 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-4
- Rebuild for python-3.2.
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild
* Wed Jul 7 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-2
- Add documentation.py files to both subpackages (this contains a brief license
  assertion among other things).
* Wed Jun 30 2010 Toshio Kuratomi <toshio@fedoraproject.org> - 3.2.0-1
- Minor cleanups
- Upgrade to 3.2.0
- Add python3 subpackage
* Tue Oct 6 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-2
- Really include the new source tarball
* Tue Oct 6 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.1.2-1
- Update to upstream release 3.1.2
* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
* Sun May 31 2009 Luke Macken <lmacken@redhat.com> - 3.0.1-2
- Only run the test suite on Fedora 11, which has Py2.6 and the multiprocessing
  module.  We can disable this once the compat module is packaged for F10 and
  below.
* Thu May 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 3.0.1-1
- Update to upstream release 3.0.1.
* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild
* Wed Jan 21 2009 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2
- Enable tests via nose
* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.2.0-2
- Rebuild for Python 2.6