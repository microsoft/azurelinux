# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond tests 1

%global desc WebOb provides wrappers around the WSGI request environment, and an object to \
help create WSGI responses. The objects map much of the specified behavior of \
HTTP, including header parsing and accessors for other standard parts of the \
environment.


Name:           python-webob
Summary:        WSGI request and response object
Version:        1.8.9
Release: 7%{?dist}
License:        MIT
URL:            https://webob.org
Source:         %{pypi_source webob}

BuildArch:      noarch


BuildRequires:  python3-devel
%if %{with tests}
BuildRequires:  python3-pytest
%endif


%description
%{desc}


%package -n python3-webob
Summary:        %{summary}


%description -n python3-webob
%{desc}


%prep
%setup -q -n webob-%{version}
# Disable performance_test, which requires repoze.profile, which isn't
# in Fedora.
rm -f tests/performance_test.py

# Remove an empty unneeded file that is there for scm purposes.
rm docs/_static/.empty


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -L webob


%check
# Check section disabled: Disabling checks for initial set of failures.
exit 0

%if %{with tests}
# test_interrupted_request: https://github.com/Pylons/webob/issues/479
%pytest -k "not test_interrupted_request"
%else
%pyproject_check_import
%endif


%files -n python3-webob -f %{pyproject_files}
%license docs/license.txt
%doc docs/*


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.8.9-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.8.9-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.8.9-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Nov 12 2024 Carl George <carlwgeorge@fedoraproject.org> - 1.8.9-1
- Update to version 1.8.9 rhbz#2325373
- Port to pyproject macros
- Remove old provides/obsoletes for python3-webob1.2

* Sat Aug 17 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.8.8-2
- Disable legacy-cgi requires for Fedora 40 and older systems

* Thu Aug 15 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 1.8.8-1
- Update to upstream. Fix open redirect issue in 1.8-branch rhbz#2305065
- pypi_source constructed manually according to project/name case inconsistency
- only require legacy-cgi on on systems where it's present
- remove python3.9 patch (applied upstream)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 15 2024 Mattia Verga <mattia.verga@proton.me> - 1.8.7-14
- Explicitly require python3-cgi at runtime (Fedora#2245641)

* Fri Jun 14 2024 Mattia Verga <mattia.verga@proton.me> - 1.8.7-13
- Require legacy-cgi as build dependency
- Fix FTB with Python 3.13 (Fedora#2245641)

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.8.7-12
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.8.7-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.8.7-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.7-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.8.7-2
- Rebuilt for Python 3.10

* Mon Feb 22 2021 Kevin Fenzi <kevin@scrye.com> - 1.8.7-1
- Update to 1.8.7. Fixes rhbz#1930010

* Fri Jan 22 2021 Charalampos Stratakis <cstratak@redhat.com> - 1.8.6-4
- Switch the test run from nose to pytest

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 1.8.6-2
- Rebuilt for Python 3.9

* Sun Mar 22 2020 Carl George <carl@george.computer> - 1.8.6-1
- Latest upstream rhbz#1793857

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 14 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.8.5-5
- Fix Python 3.9 compatibility

* Mon Sep 09 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.5-4
- Subpackage python2-webob has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.8.5-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 08 2019 Javier Peña <jpena@redhat.com> - 1.8.5-1
- Update to 1.8.5

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jul 06 2018 Matthias Runge <mrunge@redhat.com> - 1.8.2-1
- update to 1.8.2 (rhbz#1564125)

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.8.1-2
- Rebuilt for Python 3.7

* Tue May 29 2018 Alfredo Moralejo <amoralej@redhat.com> - 1.8.1-1
- Update to upstream version 1.8.1.

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.7.4-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 18 2017 Kevin Fenzi <kevin@scrye.com> - 1.7.4-1
- Update to 1.7.4. Fixes bug #1515821

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 1.7.3-4
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.7.3-2
- Depend on python2- versions of nose and setuptools.

* Wed Jul 12 2017 Randy Barlow <bowlofeggs@fedoraproject.org> - 1.7.3-1
- Update to 1.7.3 (#1466976).
- Provide python2-webob.
- Use the license macro to mark the license file.
- Remove commented code.
- Remove an empty docs file.

* Sat Mar 25 2017 Kevin Fenzi <kevin@scrye.com> - 1.7.2-1
- Update to 1.7.2. Fixes bug #1432922

* Sat Feb 25 2017 Kevin Fenzi <kevin@scrye.com> - 1.7.1-1
- Update to 1.7.1. Fixes bug #1413950

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Kevin Fenzi <kevin@scrye.com> - 1.7.0-1
- Update to 1.7.0. Fixes bug #1408197

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.6.2-2
- Rebuild for Python 3.6

* Wed Nov 09 2016 Kevin Fenzi <kevin@scrye.com> - 1.6.2-1
- Update to 1.6.2. Fixes bug #1385661

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 31 2016 Nils Philippsen <nils@redhat.com>
- fix source URL

* Sun May 22 2016 Luke Macken <lmacken@redhat.com> - 1.6.1-1
- Update to 1.6.1. Fixes bug #1338436

* Sun Apr 10 2016 Kevin Fenzi <kevin@scrye.com> - 1.6.0-1
- Update to 1.6.0. Fixes bug #1300180

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 25 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 1.4.2-1
- Upstream 1.4.2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Apr 15 2015 Ralph Bean <rbean@redhat.com> - 1.4.1-1
- new version

* Wed Aug 27 2014 Luke Macken <lmacken@redhat.com> - 1.4-1
- Update to 1.4

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.3-10
- Enable tests again.

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.3-9
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Set up macro for test bootstrap

* Mon Jan  6 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.3-8
- And correct the obs_ver again as a later version was built
- Add obsoletes for the python3-webob1.2 package as well

* Mon Sep 16 2013 Michael Schwendt <mschwendt@fedoraproject.org> - 1.2.3-7
- correct python-webob1.2 obs_ver

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May  7 2013 Luke Macken <lmacken@redhat.com> - 1.2.3-5
- Remove the python-wsgiproxy build requirement (#960463)

* Tue Apr  2 2013 Luke Macken <lmacken@redhat.com> - 1.2.3-4
- Rebase with and obsolete the python-webob1.2 forward-compat package

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jan 10 2013 Pádraig Brady <P@draigBrady.com> - 1.2.3-2
- Update to WebOb-1.2.3

* Wed Jan 09 2013 Matthias Runge <mrunge@redhat.com> - 1.1.1-4
- fix deprecation warning (rhbz#801312)
- minor spec cleanup

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-9
- Trying pyver again with py2ver and py3ver.  Getting ugly.

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-8
- Hardcode python3 version

* Thu Nov 29 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-7
- Forced rebuild.

* Tue Oct 16 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-6
- Use pyver macro to use the correct easy-install.

* Tue Oct 16 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-5
- Forced rebuild.

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-4
- Modernized the with_python3 conditional.
- Updated README.Fedora from 1.0.x to 1.2.1.

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-3
- Removed unreferenced %%global pypiname.
- Changed %%check invocation from "nosetests" to "python setup.py test"
- Added python3 support.

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-2
- Typofix BR: python-setuptools-devel -> python-setuptools

* Mon Aug 06 2012 Ralph Bean <rbean@redhat.com> - 1.2.1-1
- Fork from python-webob1.0 for forward-compat python-webob1.2.
- Some modernization of the spec file.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Luke Macken <lmacken@redhat.com> - 1.1.1-1
- Update to the latest stable release
- Remove wsgiproxy, tempita, and dtopt from our build requirements

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 1.0.8-3
- Rename package from python-webob10 to python-webob1.0

* Thu Nov 17 2011 Steve Traylen <steve.traylen@cern.ch> - 1.0.8-2
- Fedora package adapted to parallel installable on el6.

* Wed Aug 17 2011 Nils Philippsen <nils@redhat.com> - 1.0.8-1
- Update to 1.0.8 for TurboGears 2.1.1 which needs 1.0.7 (#663117)

* Mon Mar 21 2011 Luke Macken <lmacken@redhat.com> - 1.0.5-1
- Update to 1.0.5, which restores Python 2.4 support

* Thu Feb 24 2011 Luke Macken <lmacken@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 14 2010 Ricky Zhou <ricky@fedoraproject.org> - 1.0-1
- Upstream released new version.

* Sun Jul 25 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.9.8-4
- Reenable tests since python-webtest is now available

* Sun Jul 25 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 0.9.8-3
- Disable tests. We need to bootstrap against python-webtest

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.8-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 05 2010 Luke Macken <lmacken@redhat.com> - 0.9.8-1
- Latest upstream release
- Get the test suite running

* Tue Jan 19 2010 Ricky Zhou <ricky@fedoraproject.org> - 0.9.7.1-1
- Upstream released new version.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.9.6.1-2
- Change define to global.
- Remove unnecessary BuildRequires on python-devel.

* Tue Mar 10 2009 Ricky Zhou <ricky@fedoraproject.org> - 0.9.6.1-1
- Upstream released new version.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 06 2009 Luke Macken <lmacken@redhat.com> 0.9.5-1
- Update to 0.9.5

* Sat Dec 06 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.4-1
- Upstream released new version.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.9.3-3
- Rebuild for Python 2.6

* Tue Sep 30 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.3-2
- Add BuildRequires on python-tempita.

* Tue Sep 30 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.3-1
- Upstream released new version.

* Thu Jul 17 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.2-2
- Remove conftest from the tests.

* Fri Jun 27 2008 Ricky Zhou <ricky@fedoraproject.org> 0.9.2-1
- Upstream released new version.
- Rename to python-webob, as mentioned in the Python package naming
  guidelines.
- Clean up spec.
- Add %%check section.

* Sat Mar 15 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.9-1
- Initial package for Fedora
