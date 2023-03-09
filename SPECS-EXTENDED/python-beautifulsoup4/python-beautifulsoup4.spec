%global srcname beautifulsoup4
%global _description %{expand:
Beautiful Soup is a Python HTML/XML parser designed for quick
turnaround projects like screen-scraping. Three features make it
powerful:
Beautiful Soup won't choke if you give it bad markup.
Beautiful Soup provides a few simple methods and Pythonic idioms for
Beautiful Soup automatically converts incoming documents to Unicode
and outgoing documents to UTF-8.
Beautiful Soup parses anything you give it.
Valuable data that was once locked up in poorly-designed websites is
now within your reach. Projects that would have taken hours take only
minutes with Beautiful Soup.}

# Ciruclar dependency with soupsieve which must be disabled at times
%bcond_without  soupsieve
Summary:        HTML/XML parser for quick-turnaround applications like screen-scraping
Name:           python-%{srcname}
Version:        4.11.2
Release:        2%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.crummy.com/software/BeautifulSoup/
Source0:        https://files.pythonhosted.org/packages/source/b/%{srcname}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with soupsieve}
BuildRequires:  python3-pytest
BuildRequires:  python3-soupsieve
%endif
BuildRequires:  python3-lxml
# html5lib BR just for test coverage
%if %{with_check}
BuildRequires:  python3-html5lib
%endif

%description %_description

%package     -n python3-beautifulsoup4
Summary:        %summary
Requires:       python3-lxml
%if %{with soupsieve}
Requires:       python3-soupsieve
%endif
Obsoletes:      python3-BeautifulSoup < 1:3.2.1-2
%{?python_provide:%python_provide python3-beautifulsoup4}

%description -n python3-beautifulsoup4 %_description

%prep
%autosetup -n %{srcname}-%{version}
rm -rf %{py3dir} && cp -a . %{py3dir}

%build
pushd %{py3dir}
%py3_build

%install
pushd %{py3dir}
%py3_install

%check
%py3_check_import bs4
pushd %{py3dir}
python3 -m unittest discover -s bs4 || :

%files -n python3-beautifulsoup4
%license LICENSE
%doc NEWS.txt
%{python3_sitelib}/beautifulsoup4-%{version}*.egg-info
%{python3_sitelib}/bs4

%changelog
* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 4.11.2-2
- Initial CBL-Mariner import from Fedora 38 (license: MIT)
- license verified

* Thu Feb 02 2023 Terje Rosten <terje.rosten@ntnu.no> - 4.11.2-1
- 4.11.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jan 05 2023 Major Hayden <major@redhat.com> - 4.11.1-1
- Update to 4.11.1

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.11.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.11.0-2
- Rebuilt for Python 3.11

* Sat Apr 09 2022 Terje Rosten <terje.rosten@ntnu.no> - 4.11.0-1
- 4.11.0

* Sun Feb 13 2022 Terje Rosten <terje.rosten@ntnu.no> - 4.10.0-4
- Rebuild to get fc36/rawhide split

* Tue Feb 08 2022 Steve Traylen <steve.traylen@cern.ch> - 4.10.0-3
- New bcond flag to disable/enable soupsieve dependency
- New bcond flag to disable/enable testing
- Test module loading in check section

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Sep 09 2021 Terje Rosten <terje.rosten@ntnu.no> - 4.10.0-1
- 4.10.0

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 4.9.3-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Oct 11 2020 Terje Rosten <terje.rosten@ntnu.no> - 4.9.3-1
- 4.9.3

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Terje Rosten <terje.rosten@ntnu.no> - 4.9.1-1
- 4.9.1

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 4.9.0-2
- Rebuilt for Python 3.9

* Mon Apr 13 2020 Terje Rosten <terje.rosten@ntnu.no> - 4.9.0-1
- 4.9.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 19 2020 Terje Rosten <terje.rosten@ntnu.no> - 4.8.2-1
- 4.8.2

* Mon Dec 02 2019 Terje Rosten <terje.rosten@ntnu.no> - 4.8.1-1
- 4.8.1

* Tue Sep 03 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.8.0-3
- Subpackage python2-beautifulsoup4 has been removed (#1748299)

* Mon Aug 19 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.8.0-2
- Rebuilt for Python 3.8 (again)

* Sun Aug 18 2019 Terje Rosten <terje.rosten@ntnu.no> - 4.8.0-1
- 4.8.0

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 4.6.3-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 27 2018 Terje Rosten <terje.rosten@ntnu.no> - 4.6.3-1
- 4.6.3

* Mon Jul 30 2018 Terje Rosten <terje.rosten@ntnu.no> - 4.6.1-1
- 4.6.1

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 4.6.0-7
- Rebuilt for Python 3.7

* Wed Feb 07 2018 Terje Rosten <terje.rosten@ntnu.no> - 4.6.0-6
- Clean up

* Wed Feb 07 2018 Iryna Shcherbina <ishcherb@redhat.com> - 4.6.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 4.6.0-4
- Cleanup spec file conditionals

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.6.0-3
- Python 2 binary package renamed to python2-beautifulsoup4
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 08 2017 Terje Rosten <terje.rosten@ntnu.no> - 4.6.0-1
- 4.6.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 04 2017 Terje Rosten <terje.rosten@ntnu.no> - 4.5.3-1
- 4.5.3

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.5.1-3
- Un-bootstrap for Python 3.6

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 4.5.1-2
- Rebuild for Python 3.6

* Tue Aug 09 2016 Terje Rosten <terje.rosten@ntnu.no> - 4.5.1-1
- 4.5.1

* Tue Jul 26 2016 Ville Skyttä <ville.skytta@iki.fi> - 4.5.0-1
- Update to 4.5.0
- Mark COPYING.txt as %%license
- Don't require html5lib
- Require lxml on EL too

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Sat Oct 03 2015 Terje Rosten <terje.rosten@ntnu.no> - 4.4.1-1
- 4.4.1

* Sat Jul 04 2015 Terje Rosten <terje.rosten@ntnu.no> - 4.4.0-1
- 4.4.0

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 4.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Thu Oct 17 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.3.2-1
- 4.3.2

* Mon Aug 19 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.3.1-1
- 4.3.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 29 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.2.1-1
- 4.2.1

* Mon May 27 2013 Terje Rosten <terje.rosten@ntnu.no> - 4.2.0-1
- 4.2.0

* Tue Mar 19 2013 Ralph Bean <rbean@redhat.com> - 4.1.3-3
- Don't include python-lxml for el6.
- Conditionalize python3 support.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 03 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.3-1
- 4.1.3

* Sat Aug 04 2012 David Malcolm <dmalcolm@redhat.com> - 4.1.1-5
- rebuild for https://fedoraproject.org/wiki/Features/Python_3.3

* Sun Jul 22 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.1-4
- Move python3 req to sub package

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 10 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.1-2
- License is MIT
- Remove old cruft
- Fix obsolete

* Mon Jul 09 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.1.1-1
- 4.1.1
- Obsolete the old py3-bs4 from bs3 package

* Mon May 28 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.0.5-1
- 4.0.5

* Sat Mar 24 2012 Terje Rosten <terje.rosten@ntnu.no> - 4.0.1-1
- initial package based on python-BeautifulSoup.
