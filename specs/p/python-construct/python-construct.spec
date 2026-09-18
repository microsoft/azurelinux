# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary:        A powerful declarative parser/builder for binary data
Name:           python-construct
Version:        2.10.70
Release:        11%{?dist}
License:        MIT
URL:            http://construct.readthedocs.org
Source0:        https://pypi.python.org/packages/source/c/construct/construct-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
Construct is a powerful declarative parser (and builder) for binary
data.

Instead of writing imperative code to parse a piece of data, you
declaratively define a data structure that describes your data. As
this data structure is not code, you can use it in one direction to
parse data into Pythonic objects, and in the other direction, convert
(build) objects into binary data.}

%description %_description
%package     -n python3-construct
Summary:        %summary
Requires:       python3-six
%description -n python3-construct %_description

%prep
%autosetup -n construct-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%{pyproject_wheel}

%install
%{pyproject_install}
%pyproject_save_files -l construct

%check
%pyproject_check_import

%files -n python3-construct -f %{pyproject_files}
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.10.70-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.10.70-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Thu Aug 07 2025 Terje Røsten <terjeros@gmail.com> - 2.10.70-9
- New macros

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.70-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 2.10.70-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.70-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.70-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.10.70-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.70-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.70-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Dec 02 2023 Terje Rosten <terje.rosten@ntnu.no> - 2.10.70-1
- 2.10.70

* Sun Oct 22 2023 Terje Rosten <terje.rosten@ntnu.no> - 2.10.69-1
- 2.10.69

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.68-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.10.68-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.68-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.68-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.10.68-2
- Rebuilt for Python 3.11

* Sat Feb 26 2022 Terje Rosten <terje.rosten@ntnu.no> - 2.10.68-1
- 2.10.68

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.67-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.67-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.10.67-2
- Rebuilt for Python 3.10

* Fri Apr 23 2021 Terje Rosten <terje.rosten@ntnu.no> - 2.10.67-1
- 2.10.67

* Mon Apr 05 2021 Terje Rosten <terje.rosten@ntnu.no> - 2.10.66-1
- 2.10.66

* Thu Mar 25 2021 Terje Rosten <terje.rosten@ntnu.no> - 2.10.63-1
- 2.10.63

* Sun Mar 14 2021 Terje Rosten <terje.rosten@ntnu.no> - 2.10.61-1
- 2.10.61

* Sat Feb 20 2021 Terje Rosten <terje.rosten@ntnu.no> - 2.10.60-1
- 2.10.60

* Sun Feb 07 2021 Terje Rosten <terje.rosten@ntnu.no> - 2.10.59-1
- 2.10.59

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.56-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.56-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.10.56-2
- Rebuilt for Python 3.9

* Tue Feb 11 2020 Terje Rosten <terje.rosten@ntnu.no> - 2.10.56-1
- 2.10.56

* Tue Jan 28 2020 Terje Rosten <terje.rosten@ntnu.no> - 2.10.55-1
- 2.10.55
- Python < 3.6 is not supported any longer

* Thu Jan 23 2020 Terje Rosten <terje.rosten@ntnu.no> - 2.10.53-1
- 2.10.53

* Sun Jan 19 2020 Terje Rosten <terje.rosten@ntnu.no> - 2.9.51-1
- 2.9.51

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.9.45-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.9.45-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.45-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 18 2019 Peter Robinson <pbrobinson@fedoraproject.org> 2.9.45-2
- Add python2 build deps to conditional
- Re-enable python2 builds on rawhide as it's still a build requirement

* Mon May 13 2019 Terje Rosten <terje.rosten@ntnu.no> - 2.9.45-1
- 2.9.45
- Remove Python 2 subpackage

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-17
- Rebuilt for Python 3.7

* Mon May 21 2018 Terje Rosten <terje.rosten@ntnu.no> - 2.5.1-16
- Add patch to fix Python 3 import issue (rhbz#1560199)

* Mon Feb 12 2018 Terje Rosten <terje.rosten@ntnu.no> - 2.5.1-15
- Clean up

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.5.1-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.1-12
- Python 2 binary package renamed to python2-construct
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.5.1-9
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-8
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jun 08 2013 Terje Rosten <terje.rosten@ntnu.no> - 2.5.1-1
- initial package
