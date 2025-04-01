## START: Set by rpmautospec
## (rpmautospec version 0.6.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 13;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# Run tests by default.
%bcond_without  tests

%global srcname isodate

Name:           python-%{srcname}
Version:        0.6.1
Release:        1%{?dist}
Summary:        An ISO 8601 date/time/duration parser and formatter
License:        BSD-3-Clause
URL:            https://pypi.org/project/isodate/
Source0:        %pypi_source
BuildArch:      noarch

BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3dist(pytest)
%endif


%global _description This module implements ISO 8601 date, time and duration \
parsing. The implementation follows ISO8601:2004 standard, and implements only \
date/time\ representations mentioned in the standard. If something is not \
mentioned there, then it is treated as non existent, and not as an allowed \
option.\
\
For instance, ISO8601:2004 never mentions 2 digit years. So, it is not intended\
by this module to support 2 digit years. (while it may still be valid as ISO\
date, because it is not explicitly forbidden.) Another example is, when no time\
zone information is given for a time, then it should be interpreted as local\
time, and not UTC.\
\
As this module maps ISO 8601 dates/times to standard Python data types, like\
date, time, datetime and timedelta, it is not possible to convert all possible\
ISO 8601 dates/times. For instance, dates before 0001-01-01 are not allowed by\
the Python date and datetime classes. Additionally fractional seconds are\
limited to microseconds. That means if the parser finds for instance\
nanoseconds it will round it to microseconds.

%description
%{_description}

%package -n python3-%{srcname}
Summary: %summary
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{_description}


%prep
%autosetup -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%if %{with tests}
%check
%pytest
%endif


%files -n python3-%{srcname} -f %{pyproject_files}
%doc CHANGES.txt README.rst TODO.txt


%changelog
* Mon Feb 17 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.6.1-1
- Auto-upgrade to 0.6.1 - Extended package upgrade to IDC
- License verified

* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 0.6.0-7
- License verified

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 0.6.0-10
- Rebuilt for Python 3.10

* Mon Mar 15 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0.6.0-9
- Fix builtin and extension functions that takes integer arguments

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <miro@hroncok.cz> - 0.6.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 23 2019 Miro Hrončok <miro@hroncok.cz> - 0.6.0-4
- Subpackage python2-isodate has been removed

* Fri Aug 16 2019 Miro Hrončok <miro@hroncok.cz> - 0.6.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Jeremy Cline <jcline@redhat.com> - 0.6.0-1
- Modernize specfile, bump to 0.6.0

* Mon Mar 18 2019 Marc Dequènes (Duck) <duck@redhat.com> - 0.5.4-16
- update URLs to use HTTPS

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.4-14
- Remove obsolete Group tag

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Jason Tibbitts <tibbs@math.uh.edu> - 0.5.4-12
- Remove needless use of %%defattr

* Sat Jun 16 2018 Miro Hrončok <miro@hroncok.cz> - 0.5.4-11
- Rebuilt for Python 3.7

* Wed Feb 14 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.4-10
- Remove %%clean section

* Mon Feb 12 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 0.5.4-9
- Update Python 2 dependency declarations to new packaging standards

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.4-7
- Python 2 binary package renamed to python2-isodate

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.4-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_
  Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 19 2015 John Matthews <jwmatthews@gmail.com> - 0.5.4-1
- Update to 0.5.4

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 0.5.0-8
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Dennis Gilmore <dennis@ausil.us> - 0.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Dennis Gilmore <dennis@ausil.us> - 0.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Kalev Lember <kalevlember@gmail.com> - 0.5.0-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Apr 30 2014 Dan Scott <dan@coffeecode.net> - 0.5.0-4
- Use versioned Python macros for Python2 and Python3

* Wed Apr 30 2014 Dan Scott <dan@coffeecode.net> - 0.5.0-3
- Remove python-setuptools-devel BR

* Wed Apr 30 2014 Dan Scott <dan@coffeecode.net> - 0.5.0-2
- Run python-isodate unit tests

* Wed Apr 30 2014 Dan Scott <dan@coffeecode.net> - 0.5.0-1
- Update to 0.5.0
- Add a Python3 build

* Wed Apr 30 2014 Dan Scott <dan@coffeecode.net> - 0.4.7-5
- Add 0.5.0 sources / .gitignore for python-isodate

* Sun Aug 04 2013 Dennis Gilmore <dennis@ausil.us> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Dennis Gilmore <dennis@ausil.us> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Dennis Gilmore <dennis@ausil.us> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 James Laska <jlaska@redhat.com> - 0.4.7-1
- Update to 0.4.7

* Thu Jan 26 2012 James Laska <jlaska@redhat.com> - 0.4.6-2
- Update to 0.4.7

* Mon Jan 23 2012 James Laska <jlaska@redhat.com> - 0.4.6-1
- Update to 0.4.6

* Sat Jan 14 2012 Dennis Gilmore <dennis@ausil.us> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 30 2011 James Laska <jlaska@redhat.com> - 0.4.4-1
- Initial import (#741945)
## END: Generated by rpmautospec
