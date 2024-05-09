# Created by pyp2rpm-1.1.1
%global pypi_name unittest2
%global bootstrap_traceback2 1

Name:           python-%{pypi_name}
Version:        1.1.0
Release:        25%{?dist}
Summary:        The new features in unittest backported to Python 2.4+

License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pypi.python.org/pypi/unittest2
Source0:        https://pypi.python.org/packages/source/u/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
# we don't need this in Fedora, since we have Python 2.7, which has argparse
Patch0:         unittest2-1.1.0-remove-argparse-from-requires.patch
# we only apply this if bootstrap_traceback2 == 1
Patch1:         unittest2-1.1.0-remove-traceback2-from-requires.patch
# this patch backports tests from Python 3.5, that weren't yet merged, thus the tests are failing
#  (the test is modified to also pass on Python < 3.5)
#  TODO: submit upstream
Patch2:         unittest2-1.1.0-backport-tests-from-py3.5.patch
Patch3:         unittest2-1.1.0-fix-MutableMapping.patch
BuildArch:      noarch


%description
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.


%package -n     python3-%{pypi_name}
Summary:        The new features in unittest backported to Python 2.4+
%{?python_provide:%python_provide python3-%{pypi_name}}
Conflicts:      python-%{pypi_name} < %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
%if ! 0%{?bootstrap_traceback2}
BuildRequires:  python3-traceback2
%endif # bootstrap_traceback2
Requires:       python3-setuptools
Requires:       python3-six
%if ! 0%{?bootstrap_traceback2}
Requires:       python3-traceback2
%endif


%description -n python3-%{pypi_name}
unittest2 is a backport of the new features added to the unittest testing
framework in Python 2.7 and onwards. It is tested to run on Python 2.6, 2.7,
3.2, 3.3, 3.4 and pypy.


%prep
%setup -q -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%patch 0 -p0
%patch 2 -p0
%if 0%{?bootstrap_traceback2}
%patch 1 -p0
%endif
%patch 3 -p0


%build
%py3_build


%install
%py3_install
pushd %{buildroot}%{_bindir}
mv unit2 unit2-%{python3_version}
ln -s unit2-%{python3_version} unit2-3
ln -s unit2-3 unit2
popd


%check
%if ! 0%{?bootstrap_traceback2}
%{__python3} -m unittest2
%endif # bootstrap_traceback2


%files -n python3-%{pypi_name}
%doc README.txt
%{_bindir}/unit2
%{_bindir}/unit2-3
%{_bindir}/unit2-%{python3_version}
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info


%changelog
* Tue Mar 09 2021 Henry Li <lihl@microsoft.com> - 1.1.0-25
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Turn on bootstrap_track2 to circumvent cyclic dependency

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 09 2020 Alfredo Moralejo <amoralej@redhat.com> - 1.1.0-23
- Fix compatibility with python 3.9

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-22
- Subpackage python2-unittest2 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-21
- Rebuilt for Python 3.8

* Wed Aug 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-19
- Bootstrap for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul 22 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-17
- Make /usr/bin/unit2 Python 3

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-14
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-13
- Bootstrap for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.0-11
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-8
- Disable bootstrap method

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 1.1.0-7
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-6
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu May 19 2016 Carl George <carl.george@rackspace.com> - 1.1.0-5
- Implement new Python packaging guidelines (python2 subpackage)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Nov 15 2015 Slavek Kabrda <bkabrda@redhat.com> - 1.1.0-3
- Fix tests on Python 3.5

* Sat Nov 14 2015 Toshio Kuratomi <toshio@fedoraproject.org> - - 1.1.0-2
- traceback2 has been bootstrapped.  Remove the bootstrapping conditional

* Thu Nov 12 2015 bkabrda <bkabrda@redhat.com> - 1.1.0-1
- Update to 1.1.0
- Bootstrap dependency on traceback2

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov 14 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-2
- Bump to avoid collision with previously blocked 0.8.0-1

* Mon Nov 10 2014 Slavek Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Unretire the package, create a fresh specfile
