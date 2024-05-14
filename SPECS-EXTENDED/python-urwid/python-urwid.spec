Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%bcond_without tests

%global srcname urwid

Name:          python-%{srcname}
Version:       2.1.2
Release:       2%{?dist}
Summary:       Console user interface library

License:       LGPLv2+
URL:           https://excess.org/urwid/
Source0:       %{pypi_source urwid}

%global _description\
Urwid is a Python library for making text console applications.  It has\
many features including fluid interface resizing, support for UTF-8 and\
CJK encodings, standard and custom text layout modes, simple markup for\
setting text attributes, and a powerful, dynamic list box that handles a\
mix of widget types.  It is flexible, modular, and leaves the developer in\
control.

%description %_description

%package -n python3-%{srcname}
Summary: %summary
%{?python_provide:%python_provide python3-urwid}
BuildRequires: gcc
BuildRequires: python3-devel
BuildRequires: python3-setuptools
# needed by selftest suite for test.support
BuildRequires: python3-test

%description -n python3-%{srcname} %_description

%prep
%setup -q -n %{srcname}-%{version}
find urwid -type f -name "*.py" -exec sed -i -e '/^#!\//, 1d' {} \;
find urwid -type f -name "*.py" -exec chmod 644 {} \;

%build
%py3_build

find examples -type f -exec chmod 0644 \{\} \;

%check
%if %{with tests}
# tests are failing: https://github.com/urwid/urwid/issues/344
PYTHON=%{__python3} %{__python3} setup.py test || :
%endif

%install
%py3_install

%files -n python3-%{srcname}
%license COPYING
%doc README.rst examples docs
%{python3_sitearch}/urwid/
%{python3_sitearch}/urwid-%{version}*.egg-info/

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.1.2-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Mon Nov 02 2020 Tomas Tomecek <ttomecek@redhat.com> - 2.1.2-1
- New upstream release 2.1.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-2
- Rebuilt for Python 3.9

* Wed Apr 01 2020 Tomas Tomecek <ttomecek@redhat.com> - 2.1.0-1
- New upstream release 2.1.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 22 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-6
- Resurrect removed python3-urwid package

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 27 2018 David Cantrell <dcantrell@redhat.com> - 2.0.1-4
- Fix FTBFS issue in rawhide (#1605975)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-2
- Rebuilt for Python 3.7

* Fri Jun 29 2018 David Cantrell <dcantrell@redhat.com> - 2.0.1-1
- Upgrade to urwid-2.0.1

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.3.1-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 15 2017 David Cantrell <dcantrell@redhat.com> - 1.3.1-2
- Apply upstream fix for EINTR handling in test_vterm test case
- Apply upstream fix for test_remove_watch_file flakiness
- Apply upstream fix for test_vterm handling of NUL characters

* Sat Aug 19 2017 Petr Viktorin <pviktori@redhat.com> - 1.3.1-1
- Update to upstream bugfix release 1.3.1
  See https://urwid.org/changelog.html#urwid-1-3-1

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.0-11
- Python 2 binary package renamed to python2-urwid
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Nov  3 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.0-3
- Remove executable bit on docs so that they do not bring in extra rpm
  dependencies.  This complies with packaging guidelines and fixes the
  problem of python3-urwid requiring the python2 package.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Nov 25 2014 David Cantrell <dcantrell@redhat.com> - 1.3.0-1
- Upgrade to urwid-1.3.0 (#1150540)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jun 12 2014 David Cantrell <dcantrell@redhat.com> - 1.2.1-1
- Upgrade to urwid-1.2.1 (#1047698)

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Dec 06 2013 Pierre-Yves Chibon <pingou@pingoured>fr - 1.1.1-3
- Change BR from python-setuptools-devel to python-setuptools
  See https://fedoraproject.org/wiki/Changes/Remove_Python-setuptools-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Nov 21 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 1.1.1 -1
- Bugfix update

* Tue Oct 23 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 1.1.0-2
- Add new docs and examples dir

* Tue Oct 23 2012 Fabian Deutsch <fabiand@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Wed Sep 26 2012 Fabian Deutsch <fabian.deutsch@gmx.de> - 1.0.2-1
- Update to upstream 1.0.2

* Mon Aug 27 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.0-7
- add missing BRs on python-test and python3-test (for test.support)

* Fri Aug 24 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.0-6
- remove rhel logic from with_python3 conditional
- remove stray references to mako

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.0.0-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 24 2011 Luke Macken <lmacken@redhat.com> - 1.0.0-2
- Add a python3-urwid subpackage (#746627)

* Wed Oct 19 2011 Luke Macken <lmacken@redhat.com> - 1.0.0
- Update to version 1.0.0
- Add python-setuptools-devel to the BuildRequires
- Run the test suite using the setup.py

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 0.9.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed May 19 2010 David Cantrell <dcantrell@redhat.com> - 0.9.9.1-1
- Initial package
