%global srcname requests-file

Name:           python-%{srcname}
Version:        2.0.0
Release:        4%{?dist}
Summary:        Transport adapter for using file:// URLs with python-requests

License:        Apache-2.0
URL:            https://github.com/dashea/requests-file
Source0:        %pypi_source

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)

%global _description %{expand:
Requests-File is a transport adapter for use with the Requests Python
library to allow local file system access via file:// URLs.}

%description %_description

%package -n python3-requests-file
Summary:        %{summary}

%description -n python3-requests-file %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files requests_file

%check
%{pytest}

%files -n python3-requests-file -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.0-3
- Rebuilt for Python 3.13

* Fri Feb 02 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 2.0.0-2
- Avoid tox dependency

* Mon Jan 29 2024 David Shea <reallylongword@gmail.com> - 2.0.0-1
- Update to version 2.0.0
- Apply current python packaging recommendations to the spec file

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.5.1-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.5.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 1.5.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Dec 14 2020 David Shea <reallylongword@gmail.com> - 1.5.1-1
- Make Content-Length optional
- Fix python2 compatibility

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 1.4.3-15
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.3-13
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4.3-12
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Dec 17 2018 David Shea <dshea@redhat.com> - 1.4.3-9
- Remove the python2 subpackage
- Remove all the dumb %%if statements

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 15 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4.3-7
- Rebuilt for Python 3.7

* Fri Mar 16 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.4.3-6
- Don't build Python 2 subpackage on EL > 7

* Mon Feb 26 2018 Nick Bebout <nb@usi.edu> - 1.4.3-5
- Add python2- prefix where possible

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Feb  7 2018 Eli Young <elyscape@gmail.com> - 1.4.3-3
- Package for EPEL7

* Sat Jan 27 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.4.3-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Jan  3 2018 David Shea <dshea@redhat.com> - 1.4.3-1
- Update to requests-file-1.4.3, which sets the response URL to the request URL

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Dec 13 2016 Charalampos Stratakis cstratak@redhat.com> - 1.4-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 03 2015 Robert Kuska <rkuska@redhat.com> - 1.4-2
- Rebuilt for Python3.5 rebuild

* Mon Sep 14 2015 David Shea <dshea@redhat.com> - 1.4-1
- Use getprerredencoding instead of nl_langinfo
- Handle files with a drive component
- Switch to the new Fedora packaging guidelines, which renames python-requests-file to python2-requests-file

* Mon May 18 2015 David Shea <dshea@redhat.com> - 1.3.1-1
- Add python version classifiers to the package info

* Mon May 18 2015 David Shea <dshea@redhat.com> - 1.3-1
- Fix a crash when closing a file response.
- Use named aliases instead of integers for status codes.

* Fri May  8 2015 David Shea <dshea@redhat.com> - 1.2-1
- Added support for HEAD requests

* Thu Mar 12 2015 David Shea <dshea@redhat.com> - 1.1-1
- Added handing for %% escapes in URLs
- Proofread the README

* Tue Mar 10 2015 David Shea <dshea@redhat.com> - 1.0-1
- Initial package
