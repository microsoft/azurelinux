%global _description\
WebTest wraps any WSGI application and makes it easy to send test\
requests to that application, without starting up an HTTP server.\
\
This provides convenient full-stack testing of applications written\
with any WSGI-compatible framework.
%global srcname webtest
Summary:        Helper to test WSGI applications
Name:           python-%{srcname}
Version:        3.0.0
Release:        5%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/Pylons/webtest
Source0:        https://github.com/Pylons/webtest/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildArch:      noarch
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif

%description %{_description}

%package -n python3-webtest
Summary:        Helper to test WSGI applications
Requires:       python3-beautifulsoup4
Requires:       python3-waitress
Requires:       python3-webob

%description -n python3-webtest
WebTest wraps any WSGI application and makes it easy to send test
requests to that application, without starting up an HTTP server.

This provides convenient full-stack testing of applications written
with any WSGI-compatible framework.

%prep
%autosetup -n %{srcname}-%{version}
# Remove bundled egg info if it exists.
rm -rf *.egg-info

%build
%py3_build
# remove files not needed in documentation
rm -f docs/Makefile docs/conf.py docs/changelog.rst
cp -a CHANGELOG.rst docs/

%install
%py3_install

%check
%{python3} -m pip install pytest-cov beautifulsoup4 PasteDeploy pyquery waitress webob WSGIProxy2
%pytest

%files -n python3-webtest
%license license.rst
%doc docs/* CHANGELOG.rst
%{python3_sitelib}/webtest
%{python3_sitelib}/*.egg-info

%changelog
* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 3.0.0-5
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- license verified

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 17 2022 Python Maint <python-maint@redhat.com> - 3.0.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Aug 20 2021 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.0.0-1
- Update to upstream
- Change dependencies according to upstream

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.35-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.35-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.35-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jan 25 2021 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 2.0.35-5
- Reenable check tests using pytest.

* Mon Jan 25 2021 Charalampos Stratakis <cstratak@redhat.com> - 2.0.35-4
- Switch the test run from nose to pytest

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 25 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.35-2
- Rebuilt for Python 3.9

* Mon Apr 27 2020 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 2.0.35-1
- Update to upstream (bz#1828294)

* Thu Jan 30 2020 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 2.0.34-1
- Update to upstream (bz#1795938)

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.33-4
- Fix the release number to be strictly chronological

* Mon Sep 02 2019 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 2.0.33-2
- Removed python2 support (BZ#1747970)
- Updated documentation (remove unwanted files and add CHANGELOG instead
  of it's broken symlink)

* Sat Jun 22 2019 Kevin Fenzi <kevin@scrye.com> - 2.0.33-1
- Update to 2.0.33. Fixes bug #1674207
- Drop python2 tests due to lack of sphinx theme.

* Thu Jun 20 2019 Troy Dawson <tdawson@redhat.com> - 2.0.30-3.1
- Turn off tests for initial EPEL8 build

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.30-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.30-2
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Tue Jul 24 2018 Kevin Fenzi <kevin@scrye.com> - 2.0.30-1
- Update to 2.0.30
- Fix FTBFS bug #1605988

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jun 18 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.29-6
- Rebuilt for Python 3.7

* Wed Feb 28 2018 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.0.29-5
- Use python2 explicitly during build, install, and testing.

* Wed Feb 28 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.29-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 23 2018 Merlin Mathesius <mmathesi@redhat.com> - 2.0.29-3
- Override py3dir to avoid potential troublesome characters in path
  (such as "+") that can cause test_http self-test errors

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Dec 17 2017 Kevin Fenzi <kevin@scrye.com> - 2.0.29-1
- Update to 2.0.29. Fixes bug #1477394

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 2.0.27-4
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.0.27-3
- Python 2 binary package renamed to python2-webtest
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Mar 25 2017 Kevin Fenzi <kevin@scrye.com> - 2.0.27-1
- Update to 2.0.27. Fixes bug #1429268

* Sat Feb 25 2017 Kevin Fenzi <kevin@scrye.com> - 2.0.25-1
- Update to 2.0.25. Fixes bug #1419377

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Kevin Fenzi <kevin@scrye.com> - 2.0.24-1
- Update to 2.0.24. Fixes bug #1405668

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.0.23-2
- Rebuild for Python 3.6

* Sat Jul 23 2016 Kevin Fenzi <kevin@scrye.com> - 2.0.23-1
- Update to 2.0.23. Fixes bug #1359466

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.19-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Mon Nov 02 2015 Ralph Bean <rbean@redhat.com> - 2.0.19-1
- new version

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Feb 18 2015 Ralph Bean <rbean@redhat.com> - 2.0.17-1
- new version

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 2.0.16-1
- Updated to 2.0.16.

* Fri Jun 13 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.0.15-1
- Updated to 2.0.15.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.4-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4
- Fix python3 subpackage dependencies

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr  5 2013 Luke Macken <lmacken@redhat.com> - 1.3.4-5
- Made the python3 subpackage require python-webob instead of python-webob1.2

* Tue Feb 19 2013 Ralph Bean <rbean@redhat.com> - 1.3.4-4
- Added python3 subpackage

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jun 24 2012 Ricky Zhou <ricky@fedoraproject.org> - 1.3.4-1
- Update to 1.3.4.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Luke Macken <lmacken@redhat.com> - 1.3.3-1
- Update to 1.3.3

* Fri Jul 15 2011 Toshio Kuratomi <toshio@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Luke Macken <lmacken@redhat.com> - 1.2.2-1
- Update to 1.2.2
- Add python-dtopt to the BuildRequires
- Include the docs again

* Sun Jul 25 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot[com> - 1.2.1-3
- Disable tests and docs for now. They are not included in this tarball

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jun 09 2010 Luke Macken <lmacken@redhat.com> - 1.2.1-1
- Update to 1.2.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 31 2009 Luke Macken <lmacken@redhat.com> - 1.2-1
- Update to 1.2

* Tue Apr 14 2009 Ricky Zhou <ricky@fedoraproject.org> - 1.1-3
- Change define to global.
- Remove old >= 8 conditional.
- Remove unnecessary BuildRequires on python-devel.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Dec 06 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.1-1
- Upstream released new version.

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.0-4
- Rebuild for Python 2.6

* Thu Jul 17 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.0-3
- Update Requires for python-webob rename.
- Add BuildRequires on python-webob for tests.

* Mon Jul 07 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.0-2
- Add %%check section.

* Sat Jun 14 2008 Ricky Zhou <ricky@fedoraproject.org> - 1.0-1
- Initial RPM Package.
