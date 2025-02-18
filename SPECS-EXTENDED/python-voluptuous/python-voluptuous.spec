%global srcname voluptuous

Name:      python-%{srcname}
Version:   0.15.2
Release:   1%{?dist}
Summary:   Python data validation library

License:   BSD-3-Clause
URL:       http://github.com/alecthomas/voluptuous
Source0:   %{pypi_source}
BuildArch: noarch

%global _description %{expand:
Voluptuous, despite the name, is a Python data validation library. It is 
primarily intended for validating data coming into Python as JSON, YAML, etc.}

%description %_description

%package -n python3-%{srcname}
Summary: %{summary}
BuildRequires: python3-devel
BuildRequires: %{py3_dist setuptools}
BuildRequires: %{py3_dist pytest}

%description -n python3-%{srcname} %_description

%prep
%autosetup -n %{srcname}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%install
%pyproject_install

%pyproject_save_files voluptuous

%check
%pytest

%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.md
%license COPYING

%changelog
* Wed Aug 21 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.2-1
- New upstream source 0.15.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jun 27 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 0.15.0-1
- New upstream source 0.15.0

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.14.2-2
- Rebuilt for Python 3.13

* Mon Feb 05 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.2-1
- New upstream source 0.14.2

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Nov 26 2023 Sergio Pascual <sergiopr@fedoraproject.org> - 0.14.1-1
- New upstream source 0.14.1
- Updated license to SPDX

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.13.1-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.13.1-2
- Rebuilt for Python 3.11

* Thu Apr 07 2022 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.13.1-1
- Update to 0.13.1 (#2073109)

* Fri Apr 01 2022 Fabian Affolter <mail@fabian-affolter.ch> - 0.13.0-1
- Update to latest upstream release 0.13.0 (closes rhbz#2070062)

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Oct 06 2021 Sergio Pascual <sergiopr@fedoraproject.org> - 0.12.2-1
- New upstream source (0.12.2)

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.12.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.12.1-1
- New upstream source (0.12.1)

* Wed Nov 04 2020 Sergio Pascual <sergiopr@fedoraproject.org> - 0.12.0-1
- New upstream source (0.12.0)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.11.7-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11.7-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Fedora Release Monitoring <release-monitoring@fedoraproject.org> - 0.11.7-1
- Update to 0.11.7 (#1742700)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11.5-7
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 21 2019 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-5
- Drop python2 subpackage (bz #1712339)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Oct 06 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-3
- Readd python2 subpackage, not yet

* Fri Oct 05 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-2
- Drop python2 subpackage

* Tue Aug 21 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.5-1
- New upstream source (0.11.5)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11.1-2
- Rebuilt for Python 3.7

* Thu Mar 08 2018 Sergio Pascual <sergiopr@fedoraproject.org> - 0.11.1-1
- New upstream source (0.11.1)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.10.5-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon May 15 2017 Sergio Pascual <sergiopr@fedoraproject.org> - 0.10.5-1
- New upstream source (0.10.5.1)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.3-3
- Rebuild for Python 3.6

* Sun Oct 02 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.9.3-2
- New upstream source (0.9.3)

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.11-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jul 13 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.11-1
- New upstream source (0.8.11)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 21 2015 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.8-1
- New upstream source
- Use new python macros
- Enable python3, fixes bz #1292616

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jul 22 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.5-2
- Use tarball from github
- Add COPYING to doc

* Mon Mar 17 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.8.5-1
- Initial spec file

