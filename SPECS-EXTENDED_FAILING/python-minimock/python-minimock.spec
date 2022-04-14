Vendor:         Microsoft Corporation
Distribution:   Mariner
Name:           python-minimock
Version:        1.2.8
Release:        24%{?dist}
Summary:        The simplest possible mock library

License:        MIT
URL:            http://pypi.python.org/pypi/MiniMock
Source0:        http://pypi.python.org/packages/source/M/MiniMock/MiniMock-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  %{_bindir}/2to3

%description
minimock is a simple library for doing Mock objects with doctest.

%package -n python3-minimock
Summary:        The simplest possible mock library
%{?python_provide:%python_provide python3-minimock}
%description -n python3-minimock
minimock is a simple library for doing Mock objects with doctest.


%prep
%setup -q -n MiniMock-%{version}


%build
%py3_build


%install
%py3_install


%check
%{__python3} minimock.py -v


%files -n python3-minimock
%license docs/license.txt
%doc docs/changelog.rst docs/index.rst
%{python3_sitelib}/MiniMock-%{version}-py?.?.egg-info
%{python3_sitelib}/minimock*
%{python3_sitelib}/__pycache__/minimock*


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.8-24
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-22
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-21
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 20 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-18
- Remove python2 subpackage (#1641282)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-16
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.2.8-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.8-11
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-10
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Jul 03 2015 Thomas Spura <tomspur@fedoraproject.org> - 1.2.8-7
- Use new python macros and clean up

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 1.2.8-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Jan 15 2014 Thomas Spura <tomspur@fedoraproject.org> - 1.2.8-3
- There is no python3 on epel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Mar 21 2013 Thomas Spura <tomspur@fedoraproject.org> - 1.2.8-1
- update to 1.2.8
- python3 supported natively
- run tests in check section

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 1.2.7-4
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 20 2011 Thomas Spura <tomspur@fedoraproject.org> - 1.2.7-1
- update to new version

* Sun Feb 20 2011 Thomas Spura <tomspur@fedoraproject.org> - 1.2.6-1
- update to new version (#678851)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Aug 22 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.5-5
- rebuild with python3.2
  http://lists.fedoraproject.org/pipermail/devel/2010-August/141368.html

* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Feb  5 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.5-3
- update python3 subpackage to reflect actuall guidelines

* Thu Jan 14 2010 Thomas Spura <tomspur@fedoraproject.org> - 1.2.5-2
- also ship python3-minimock
- be more explicit in %%files

* Tue Dec 22 2009 Thomas Spura <tomspur@fedoraproject.org> - 1.2.5-1
- correct URL
- update to new version

* Sat Dec 5 2009 Thomas Spura <tomspur@fedoraproject.org> - 1.0-1
- Initial creation for review
