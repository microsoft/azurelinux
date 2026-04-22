# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name jsonschema

%global common_description %{expand:
jsonschema is an implementation of JSON Schema for Python (supporting
2.7+, including Python 3).

 - Full support for Draft 7, Draft 6, Draft 4 and Draft 3
 - Lazy validation that can iteratively report all validation errors.
 - Small and extensible
 - Programmatic querying of which properties or items failed validation.}

Name:           python-%{pypi_name}
Summary:        Implementation of JSON Schema validation for Python
Version:        4.23.0
Release: 7%{?dist}
License:        MIT
URL:            https://github.com/Julian/jsonschema
Source0:        %{pypi_source}

BuildArch:      noarch
BuildRequires:  python3-devel

# test requirements
%if %{defined rhel}
%bcond_with tests
%else
%bcond_without tests
%endif

%if %{with tests}
# For “trial-3”
BuildRequires:  python3dist(twisted)
%endif

%description %{common_description}


%package -n     python3-%{pypi_name}
Summary:        %{summary}
%description -n python3-%{pypi_name} %{common_description}

%pyproject_extras_subpkg -n python3-%{pypi_name} format format-nongpl


%prep
%autosetup -n %{pypi_name}-%{version}

# Requires a checkout of the JSON-Schema-Test-Suite
# https://github.com/json-schema-org/JSON-Schema-Test-Suite
rm jsonschema/tests/test_jsonschema_test_suite.py

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}


%if %{with tests}
%check
PYTHONPATH=%{buildroot}%{python3_sitelib} trial-3 %{pypi_name}
%endif

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license COPYING json/LICENSE
%doc README.rst
%{_bindir}/jsonschema

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.23.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.23.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.23.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 4.23.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.23.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jan 14 2025 Joel Capitao <jcapitao@redhat.com> - 4.23.0-1
- Update to 4.23.0 release (#2247079)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 4.19.1-5
- Rebuilt for Python 3.13

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 4.19.1-4
- Bootstrap for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.19.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Sep 20 2023 Joel Capitao <jcapitao@redhat.com> - 4.19.1-1
- Update to 4.19.1 release (#2239879)

* Mon Aug 07 2023 Joel Capitao <jcapitao@redhat.com> - 4.19.0-1
- Update to 4.19.0 release (#2139238)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 4.17.3-4
- Rebuilt for Python 3.12

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 4.17.3-3
- Bootstrap for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.17.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.17.3-1
- Update to 4.17.3 release

* Mon Nov 07 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.17.0-1
- Update to 4.17.0 release

* Wed Sep 21 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.16.0-1
- Update to 4.16.0 release

* Wed Aug 17 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.10.0-1
- Update to 4.10.0 release

* Mon Aug 01 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.9.0-1
- Update to 4.9.0 release

* Sun Jul 24 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.7.2-1
- Update to 4.7.2 release

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 4.6.0-3
- Drop some BuildRequires that are generated or no longer needed

* Tue Jun 28 2022 Miro Hrončok <mhroncok@redhat.com> - 4.6.0-2
- Include the metadata directory in python3-jsonschema
- Fixes: rhbz#2101786

* Mon Jun 27 2022 Parag Nemade <pnemade AT redhat DOT com> - 4.6.0-1
- Update to 4.6.0

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.2.0-17
- Rebuilt for Python 3.11

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.2.0-16
- Bootstrap for Python 3.11

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 3.2.0-15
- Rebuilt for Python 3.11

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.2.0-14
- Bootstrap for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 3.2.0-11
- Rebuilt for Python 3.10

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 3.2.0-10
- Bootstrap for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Nov 10 2020 Nils Philippsen <nils@redhat.com> - 3.2.0-8
- Provide python3dist(jsonschema[format]) again (#1878976)

* Tue Sep 29 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-7
- Remove metapackage for python3dist(jsonschema[format]) (missing deps, #1880820)

* Sat Sep 19 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-6
- Add metapackage for python3dist(jsonschema[format]) needed by python3-bravado-core (#1878976)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-4
- Rebuilt for Python 3.9

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-3
- Bootstrap for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 07 2019 Fabio Valentini <decathorpe@gmail.com> - 3.2.0-1
- Update to version 3.2.0.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-3
- Rebuilt for Python 3.8

* Thu Aug 15 2019 Miro Hrončok <mhroncok@redhat.com> - 3.0.2-2
- Bootstrap for Python 3.8

* Fri Aug 02 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.2-1
- Update to version 3.0.2.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 01 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.1-1
- Update to version 3.0.1.

* Sun Feb 24 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.0-1
- Update to version 3.0.0.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0~b3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.0~b3-1
- Update to version 3.0.0b3.

* Tue Jan 22 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.0~b1-1
- Update to version 3.0.0b1.

* Sat Jan 19 2019 Fabio Valentini <decathorpe@gmail.com> - 3.0.0~a5-1
- Update to version 3.0.0a5.
- Moved python2 sub-package to separate source package.

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-5
- Rebuilt for Python 3.7

* Wed Feb 21 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.6.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Jan Beran <jberan@redhat.com> 2.6.0-1
- Update to 2.6.0
- Fix of missing Python 3 version executables

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Dec 14 2016 Charalampos Stratakis <cstratak@redhat.com> - 2.5.1-4
- Rebuild for Python 3.6

* Mon Nov 21 2016 Orion Poplawski <orion@cora.nwra.com> - 2.5.1-3
- Enable python3 builds for EPEL (bug #1395653)
- Ship python2-jsonschema
- Modernize spec
- Use %%license

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Feb 26 2016 Lon Hohberger <lhh@redhat.com> 2.5.1-1
- Update to 2.5.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 2.4.0-3
- Rebuilt for Python3.5 rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Sep 06 2014 Alan Pevec <apevec@redhat.com> - 2.4.0-1
- Latest upstream

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 2.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Mar 10 2014 Pádraig Brady <pbrady@redhat.com> - 2.3.0-1
- Latest upstream

* Tue Feb 04 2014 Matthias Runge <mrunge@redhat.com> - 2.0.0-3
- fix %%{? issues in spec

* Thu Oct 17 2013 Thomas Spura <tomspur@fedoraproject.org> - 2.0.0-2
- add python3 subpackage (#1016207)
- add %%check

* Fri Aug 16 2013 Alan Pevec <apevec@redhat.com> 2.0.0-1
- Update to 2.0.0 release

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Pádraig Brady <P@draigBrady.com> - 1.3.0-1
- Update to 1.3.0 release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Pádraig Brady <P@draigBrady.com> - 0.2-1
- Initial package.

