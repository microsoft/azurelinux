
%global pypi_name colorama

Name:           python-%{pypi_name}
Version:        0.4.6
Release:        10%{?dist}
Summary:        Cross-platform colored terminal text

License:        BSD-3-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/tartley/colorama
Source0:        https://files.pythonhosted.org/packages/d8/53/6f443c9a4a8358a93a6792e2acffb9d9d5cb0a5cfd8802644b7b1c9a02e4/colorama-0.4.6.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires: 	python3-pip
BuildRequires: 	python3-wheel
BuildRequires: 	python3-trove-classifiers
BuildRequires: 	python3-hatchling
BuildRequires: 	python3-pathspec

# for check
BuildRequires:  python3dist(pytest)

%description
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.

%package -n python3-%{pypi_name}
Summary:        Cross-platform colored terminal text

%description -n python3-%{pypi_name}
Makes ANSI escape character sequences, for producing colored
terminal text and cursor positioning, work under MS Windows.

ANSI escape character sequences have long been used to produce colored terminal
text and cursor positioning on Unix and Macs. Colorama makes this work on
Windows, too.
It also provides some shortcuts to help generate ANSI sequences, and works fine
in conjunction with any other ANSI sequence generation library, such as
Termcolor.

%prep
%autosetup -n %{pypi_name}-%{version}

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files colorama

%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc CHANGELOG.rst README.rst
%license %{python3_sitelib}/%{pypi_name}-*.dist-info/licenses/LICENSE.txt

%changelog
* Wed Feb 26 2025 Akhila Guruju <v-guakhila@microsoft.com> - 0.4.6-10
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
- Added `BuildRequires: python3-trove-classifiers python3-hatchling python3-pathspec` to fix build.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.4.6-8
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Oct 22 2023 Miroslav Suchý <msuchy@redhat.com> - 0.4.6-5
- Migrate to SPDX license

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.4.6-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 01 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.4.6-1
- Update to 0.4.6 - Closes rhz#2136298

* Tue Aug 09 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.4.5-1
- Update to 0.4.5 - Closes rhbz#2097423

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.4.4-14
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 14 2022 Mikel Olasagasti Uranga <mikel@olasagasti.info> - 0.4.4-12
- Clean up spec
- Remove all python2 bits
- Adopt pyproject-rpm-macros
- Switch to GitHub tarball for tests and enable check

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.4.4-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Nov 19 2020 Joel Capitao <jcapitao@redhat.com> - 0.4.4-1
- Update to 0.4.4 (rhbz#1887630)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.3-2
- Rebuilt for Python 3.9

* Sun May 03 2020 Fabio Alessandro Locati <me@fale.io> - 0.4.3-1
* Update to 0.4.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Feb 05 2019 Alfredo Moralejo <amoralej@redhat.com> - 0.4.1-1
- Update to 0.4.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Oct 30 2018 Matthias Runge <mrunge@redhat.com> - 0.4.0-3
- fix python2 and python3 package for all releases

* Fri Oct 19 2018 Javier Peña <jpena@redhat.com> - 0.4.0-2
- Fix python2 package for non-Fedora

* Fri Oct 19 2018 Matthias Runge <mrunge@redhat.com> - 0.4.0-1
- update to 0.4.0

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.3.9-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 20 2017 Matthias Runge <mrunge@redhat.com> - 0.3.9-1
- update to 0.3.9 (rhbz#1444626)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.3.7-4
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Sun Apr 10 2016 Igor Gnatenko <ignatenko@redhat.com> - 0.3.7-2
- Follow new packaging guidelines

* Tue Mar 08 2016 Matthias Runge <mrunge@redhat.com> - 0.3.7-1
- update to 0.3.7 (rhbz#1179250)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Sep 05 2014 Matthias Runge <mrunge@redhat.com> - 0.3.2-1
- update to 0.3.2 (rhbz#1090014)

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.2.7-5
- Skip the python3 %%files section if we don't build the python3 package

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 28 2014 Kalev Lember <kalevlember@gmail.com> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Wed Mar 12 2014 Matthias Runge <mrunge@redhat.com> - 0.2.7-2
- introduce python3 package (rhbz#1075410)

* Mon Sep 30 2013 Matthias Rugne <mrunge@redhat.com> - 0.2.7-1
- uddate to 0.2.7 (rhbz#1010924)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Mar 22 2013 Matthias Runge <mrunge@redhat.com> - 0.2.5-1
- update to 0.2.5 (rhbz#913431)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 11 2012 Matthias Runge <mrunge@redhat.com> - 0.2.4-1
- Initial package.

