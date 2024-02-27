%global pypi_name termcolor
%global sum ANSI Color formatting for output in terminal
Summary:        %{sum}
Name:           python-%{pypi_name}
Version:        2.4.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pypi.python.org/pypi/termcolor/
Source0:        https://files.pythonhosted.org/packages/10/56/d7d66a84f96d804155f6ff2873d065368b25a07222a6fd51c4f24ef6d764/termcolor-2.4.0.tar.gz
Patch0:         0001-PATCH-change-build-backend-to-flit.patch

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-flit
BuildRequires:  python3-flit-core
BuildRequires:  python3-wheel

%description
ANSI Color formatting for output in terminal.

%package -n python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{sum}

%description -n python3-%{pypi_name}
A Python 3 version of ANSI Color formatting for output in terminal.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files %{pypi_name}
 
%check
%pytest

%files -n python3-%{pypi_name} -f %{pyproject_files}
%doc CHANGES.md README.md
%license COPYING.txt

%changelog
* Tue Feb 27 2024 Yash Panchal <yashpanchal@microsoft.com> - 2.4.0-1
- Update to 2.4.0

* Fri Oct 21 2022 Riken Maharjan <rmaharjan@microsoft.com> - 1.1.0-30
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.1.0-28
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.0-25
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-22
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-20
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sat Aug 17 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-19
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.0-16
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-14
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-10
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-9
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Fri Jun 24 2016 Matthias Runge <mrunge@redhat.com> - 1.1.0-8
- fix typo in summary (rhbz#1263051)
- source location updated

* Fri May 06 2016 Dominika Krejci <dkrejci@redhat.com> - 1.1.0-7
- added support for Python 3

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 11 2012 Matthias Runge <mrunge@matthias-runge.de> - 1.1.0-1
- Initial package.
