Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname isodate

Name:           python-%{srcname}
Version:        0.6.0
Release:        6%{?dist}
Summary:        An ISO 8601 date/time/duration parser and formatter
License:        BSD
URL:            https://pypi.org/project/isodate/
Source0:        %pypi_source
Source1:        %{name}-LICENSE.txt
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six


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
mv %{SOURCE1} ./LICENSE.txt


%build
%py3_build

%install
%py3_install


%check
%{__python3} setup.py test


%files -n python3-%{srcname}
%license LICENSE.txt
%doc CHANGES.txt README.rst TODO.txt
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/


%changelog
* Fri Dec 10 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.6.0-7
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.0-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 23 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-4
- Subpackage python2-isodate has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Apr 24 2019 Jeremy Cline <jcline@redhat.com> - 0.6.0-1
- Modernize specfile
- Update to 0.6.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 0.5.4-10
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.5.4-9
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.5.4-7
- Python 2 binary package renamed to python2-isodate
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 0.5.4-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 19 2015 John Matthews <jwmatthews@gmail.com> - 0.5.4-1
- Update to 0.5.4

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 0.5.0-5
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Fri Apr 18 2014 Dan Scott <dan@coffeecode.net> - 0.5.0-1
- Update to 0.5.0
- Add a Python3 build
- Run unit tests
- Remove python-setuptools-devel BR per https://fedoraproject.org/wiki/Changes/Remove_Python-setuptools-devel

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 26 2012 James Laska <jlaska@redhat.com> - 0.4.7-1
- Update to 0.4.7

* Mon Jan 23 2012 James Laska <jlaska@redhat.com> - 0.4.6-1
- Update to 0.4.6

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Sep 28 2011 James Laska <jlaska@redhat.com> - 0.4.4-1
- Initial package build
