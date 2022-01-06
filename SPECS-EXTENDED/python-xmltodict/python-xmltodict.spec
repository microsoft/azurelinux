%global pypi_name xmltodict

Name:               python-xmltodict
Version:            0.12.0
Release:            14%{?dist}
Summary:            Python to transform XML to JSON
Vendor:		    Microsoft Corporation
Distribution:	    Mariner
License:            MIT
URL:                https://github.com/martinblech/xmltodict
Source0:            %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildArch:          noarch

%description
xmltodict is a Python module that makes working with XML feel like you are
working with JSON.  It's very fast (Expat-based) and has a streaming mode
with a small memory footprint, suitable for big XML dumps like Discogs or
Wikipedia.

%package -n python3-%{pypi_name}
Summary:            %{summary}

BuildRequires:      python3-devel
BuildRequires:      python3-setuptools
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
xmltodict is a Python module that makes working with XML feel like you are
working with JSON.  It's very fast (Expat-based) and has a streaming mode
with a small memory footprint, suitable for big XML dumps like Discogs or
Wikipedia.

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{__python3} -m nose

%files -n python3-%{pypi_name}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-*
%{python3_sitelib}/__pycache__/%{pypi_name}*

%changelog
* Mon Dec 27 2021 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 0.12.0-14
- Initial CBL-Mariner import from Fedora 35 (license: MIT)
- License verified

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.12.0-12
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jun 26 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.12.0-9
- Add python3-setuptools as BR

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 11 2020 Fabian Affolter <mail@fabian-affolter.ch> - 0.12.0-6
- Remove support for Python 2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.12.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Jun 30 2019 Kevin Fenzi <kevin@scrye.com> - 0.12.0-2
- Conditionalize dropping python2 support so it only happens in f31+
- Fixes bug 1724842

* Sat Jun 08 2019 Fabian Affolter <mail@fabian-affolter.ch> - 0.12.0-1
- Update to latest upstream release 0.12.0

* Wed Mar 27 2019 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-9
- Subpackage python2-xmltodict has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-2
- Rebuild for Python 3.6

* Tue Nov 15 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.10.2-1
- Update to latest upstream release 0.10.2

* Sun May 01 2016 Fabian Affolter <mail@fabian-affolter.ch> - 0.10.1-1
- Update to latest upstream release 0.10.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Nov 14 2015 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.2-1
- Cleanup
- Update to latest upstream release 0.9.2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Oct 02 2014 Fabian Affolter <mail@fabian-affolter.ch> - 0.9.0-1
- Update spec file according guidelines 
- Update to upstream release 0.9.0

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Ralph Bean <rbean@redhat.com> - 0.4.2-1
- Latest upstream
- Included README and LICENSE
- Running tests now
- https://github.com/martinblech/xmltodict/pull/11
- Added Requires python3 to the python3 subpackage.

* Fri Jan 04 2013 Ralph Bean <rbean@redhat.com> - 0.4.1-1
- Initial packaging for Fedora
