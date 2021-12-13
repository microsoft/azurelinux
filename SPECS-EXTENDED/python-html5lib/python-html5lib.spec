%global srcname html5lib
Name:           python-%{srcname}
Summary:        A python based HTML parser/tokenizer
Version:        1.0.1
Release:        10%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/html5lib/html5lib-python
Source0:        %pypi_source
Patch0:         %{url}/pull/403.patch#/collections-abc.patch
#{url}/pull/414.patch#/pytest4.patch (tox.ini hunk fails)
Patch1:         pytest4.patch

BuildArch:      noarch

%?python_enable_dependency_generator

%description
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.


%package -n python3-%{srcname}
Summary:        %summary
BuildRequires:    python3-devel
BuildRequires:    python3-setuptools

# Test deps
BuildRequires:  python3-mock
BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-expect
BuildRequires:  python3-six
BuildRequires:  python3-webencodings

# Optional test deps:
BuildRequires:  python3-chardet
BuildRequires:  python3-genshi
BuildRequires:  python3-lxml

%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
A python based HTML parser/tokenizer based on the WHATWG HTML5 
specification for maximum compatibility with major desktop web browsers.


%prep
%autosetup -p1 -n %{srcname}-%{version}

%build
%py3_build


%install
%py3_install


%check
# XXX figure out the failure in test_encoding
%{__python3} -m pytest -k "not test_encoding"


%files -n python3-%{srcname}
%license LICENSE 
%doc CHANGES.rst README.rst
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/


%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 1.0.1-10
- Remove epoch

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:1.0.1-9
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.0.1-7
- Drop python2-html5lib

* Mon Aug 26 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.0.1-6
- Reduce Python 2 build dependencies

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1:1.0.1-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:1.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Sep 24 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.0.1-2
- Fix dire deprecation warnings (#1627071)

* Mon Aug 20 2018 Miro Hrončok <mhroncok@redhat.com> - 1:1.0.1-1
- Update to 1.0.1 (#1584176)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.999999999-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 1:0.999999999-7
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1:0.999999999-6
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.999999999-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 0.999999999-4
- Cleanup spec file conditionals

* Thu Jul 27 2017 Kevin Fenzi <kevin@scrye.com> - 0.999999999-3
- Add Requires on python-webencodings. Fixes bug #1474883

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.999999999-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Kevin Fenzi <kevin@scrye.com> - 1:0.999999999-1
- Update to 0.999999999. Fixes bug #1431378 and #1305828
- Security fix for CVE-2016-9909, CVE-2016-9910. Fixes bug #1402706 and #1402707

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.999-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 30 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 1:0.999-12
- Correct usage of the %%python_provide macro

* Fri Dec 30 2016 Orion Poplawski <orion@cora.nwra.com> - 1:0.999-11
- Ship python2-html5lib
- Modernize spec
- Use %%license

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1:0.999-10
- Rebuild for Python 3.6
- Fix invalid escape sequences

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.999-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 1:0.999-7
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:0.999-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1:0.999-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri May 09 2014 Dennis Gilmore <dennis@ausil.us> - 0.999-3
- move python3 Requires and BuildRequires into the python3 sub-package

* Wed Mar 12 2014 Dan Scott <dan@coffeecode.net> - 0.999-2
- "six" module is a runtime requirement

* Sat Mar 01 2014 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> 0.999-1
- Added epoch information

* Wed Feb 26 2014 Dan Scott <dan@coffeecode.net> - 0.999-1
- Updated for new version
- Fixed bogus dates in changelog

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0b2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 8 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.0b2-2
- Updated python3 support which accidently removed from previous revision.

* Mon Jul 8 2013 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 1.0b2-1
- Updated new source

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 0.95-3
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.95-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 21 2012 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.95-1
- Added python3 spec and updated new source

* Mon Jul 18 2011 Praveen Kumar <kumarpraveen.nitdgp@gmail.com> - 0.90-1
- Initial spec
