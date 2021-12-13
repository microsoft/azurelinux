%global pypi_name sure

Name:           python-%{pypi_name}
Version:        1.4.11
Release:        10%{?dist}
Summary:        Utility belt for automated testing in Python

License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/gabrielfalcao/sure
Source0:        %{pypi_source}

# Python 3.9 compatibility
# https://github.com/gabrielfalcao/sure/commit/9f0e834b2e5eea5dfe21d5be4ea6a3df47baf0b9
Patch1:         9f0e834b2e5eea5dfe21d5be4ea6a3df47baf0b9.patch

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-mock
BuildRequires:  python3-nose
BuildRequires:  python3-setuptools
BuildRequires:  python3-six

%description
A testing library for Python with powerful and flexible assertions. Sure is
heavily inspired by should.js.


%package -n python3-%{pypi_name}
Summary:        %{summary} 3
%{?python_provide:%python_provide python3-%{pypi_name}}
Requires:       python3-six

%description -n python3-%{pypi_name}
A testing library for Python with powerful and flexible assertions. Sure is
heavily inspired by should.js.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}


%build
%py3_build


%install
%py3_install


%check
%{__python3} -m nose --verbosity 2


%files -n python3-%{pypi_name}
%doc COPYING
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.11-10
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 21 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.11-8
- Subpackage python2-sure has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Richard Shaw <hobbes1069@gmail.com> - 1.4.11-7
- Rebuild for Python 3.8.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 03 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.11-4
- Fix ambiguous Python requires

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.11-2
- Rebuilt for Python 3.7

* Thu May 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.11-1
- Updated to 1.4.11 (#1421319)

* Thu May 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.10-1
- Updated to 1.4.10 that supports Python 3.7 (#1578530)
- Stop py3dir pushd/popd, it is not needed
- Removed an unneeded shebeng sed
- Drop %%sum macro, use %%summary
- Drop forbidden SCL macros
- Drop unneeded python3 conditional

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Sep 29 2017 Troy Dawson <tdawson@redhat.com> - 1.4.0-4
- Cleanup spec file conditionals

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 21 2016 Adam Williamson <awilliam@redhat.com> - 1.4.0-1
- New release 1.4.0 (builds against Python 3.6)
- Drop sources merged upstream
- Modernize spec a bit (use modern macros)
- Rename python2 package to python2-sure

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.7-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 1.2.7-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.2.7-1
- Updated to 1.2.7

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 31 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.5-2
- Remove unneeded dependencies from setup.py.
Resolves: rhbz#1082400

* Fri Mar 07 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 1.2.5-1
- Updated to 1.2.5
- Fix with_python3 macro definition to work correctly on EPEL, too.

* Fri Nov 29 2013 Miro Hrončok <mhroncok@redhat.com> - 1.2.3-1
- Updated
- Introduced Python 3 subpackage

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu May 30 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.7-2
- Introduce SCL macros in the specfile.

* Mon Feb 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 1.1.7-1
- Update to 1.1.7.
- License change from MIT to GPLv3.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.0.6-1
- Update to 1.0.6.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.3-2
- python-devel should be python2-devel
- URL now points to the real homepage of the project

* Fri Jun 22 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.3-1
- Initial package.
