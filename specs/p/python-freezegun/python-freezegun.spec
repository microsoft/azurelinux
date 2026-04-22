# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global modname freezegun
%global sum Let your Python tests travel through time

Name:               python-freezegun
Version:            1.5.1
Release: 8%{?dist}
Summary:            %{sum}

License:            Apache-2.0
URL:                https://pypi.io/project/freezegun
Source0:            https://pypi.io/packages/source/f/%{modname}/%{modname}-%{version}.tar.gz

Patch:              freezegun-1.5.1-no-coverage.patch

BuildArch:          noarch

%description
freezegun is a library that allows your python tests to travel through time by
mocking the datetime module.


%package -n python3-freezegun
Summary:            %{sum}

BuildRequires:      python3-devel

%{?python_provide:%python_provide python3-freezegun}

#Requires:           python3-six
#Requires:           python3-dateutil >= 2.7

%description -n python3-freezegun
freezegun is a library that allows your python tests to travel through time by
mocking the datetime module. This is the Python 3 library.

%prep
%autosetup -p1 -n %{modname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files -l freezegun

%check
# Ignore two tests that are broken when run on systems in certain timezones.
# Reported upstream: https://github.com/spulec/freezegun/issues/348
pytest-3 --deselect tests/test_datetimes.py::TestUnitTestMethodDecorator::test_method_decorator_works_on_unittest_kwarg_frozen_time \
         --deselect tests/test_datetimes.py::TestUnitTestMethodDecorator::test_method_decorator_works_on_unittest_kwarg_hello

%files -n python3-freezegun -f %{pyproject_files}
%doc README.rst LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.5.1-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.5.1-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.5.1-4
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Nov 02 2024 Kevin Fenzi <kevin@scrye.com> - 1.5.1-2
- Add patch to not run coverage tests to allow epel10. rhbz#2321257

* Sat Nov 02 2024 Kevin Fenzi <kevin@scrye.com> - 1.5.1-1
- Upgrade to 1.5.1.
- Modernize spec.

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 1.2.2-9
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.2.2-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 1.2.2-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Oct 26 2022 Roman Inflianskas <rominf@aiven.io> - 1.2.2-1
- Update to 1.2.2

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.0-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Sep 15 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.1.0-1
- Update to 1.1.0

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-7
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-6
- Remove unused build dependency on python-sure

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 1.0.0-5
- Rebuilt for Python 3.10

* Fri Feb 19 2021 Stephen Gallagher <sgallagh@redhat.com> - 1.0.0-4
- Skip tests that are buggy on certain architectures
- Restore the UUID tests, as the bug was fixed some time ago

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 24 2020 Kevin Fenzi <kevin@scrye.com> - 1.0.0-2
- Drop build deps on python-mock and python-coverage.

* Thu Nov 19 2020 Joel Capitao <jcapitao@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Tue Sep 08 2020 Yatin Karel <ykarel@redhat.com> - 0.3.15-1
- Update to 0.3.15

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri May 22 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.12-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Sep 21 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.12-4
- Subpackage python2-freezegun has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 15 2019 Richard Shaw <hobbes1069@gmail.com> - 0.3.12-3
- Rebuild with Python 3.8.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Charalampos Stratakis <cstratak@redhat.com> - 0.3.12-1
- Update to 0.3.12

* Mon Feb 11 2019 Adam Williamson <awilliam@redhat.com> - 0.3.11-4
- Backport fix for #269 that should fix cached-property tests

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Dec 14 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.11-2
- Enable py2 on all Fedoras, it is unfortunately still needed

* Sun Nov 11 2018 Ankur Sinha <ankursinha AT fedoraproject DOT org> - 0.3.11-1
- Update to latest upstream release
- Disable py2 on F30+
- Fix py2 build

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Jun 16 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.8-10
- Rebuilt for Python 3.7

* Thu Apr 05 2018 Charalampos Stratakis <cstratak@redhat.com> - 0.3.8-9
- Conditionalize the Python 2 subpackage and don't build it on EL > 7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.3.8-8
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 28 2016 Adam Williamson <awilliam@redhat.com> - 0.3.8-4
- REALLY rename Python 2 package to python2-freezegun

* Wed Dec 21 2016 Adam Williamson <awilliam@redhat.com> - 0.3.8-3
- Rebuild with Python 3.6 again (now python-sure is built)
- rename Python 2 package to python2-freezegun

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.8-2
- Rebuild for Python 3.6

* Tue Nov 08 2016 Ralph Bean <rbean@redhat.com> - 0.3.8-1
- new version

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Apr 20 2016 Kevin Fenzi <kevin@scrye.com> - 0.3.6-1
- Update to 0.3.6. Fixes bug #1328934

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 0.3.2-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 16 2015 Adam Williamson <awilliam@redhat.com> - 0.3.2-1
- latest upstream release

* Thu Jan 22 2015 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.1.12-4
- Adjust tests to actually do something

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.12-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Feb 12 2014 Ralph Bean <rbean@redhat.com> - 0.1.12-1
- initial package for Fedora
