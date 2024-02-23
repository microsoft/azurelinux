%global srcname ruamel-yaml
%global commit 6f41eb6001661917fceb0e88ed0693ae1a7c50f4
%global debug_package %{nil}
Summary:        YAML 1.2 loader/dumper package for Python
Name:           python-%{srcname}
Version:        0.18.6
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pypi.org/project/ruamel.yaml/
Source0:        https://sourceforge.net/code-snapshots/hg/r/ru/ruamel-yaml/code/ruamel-yaml-code-%{commit}.zip

%description
ruamel.yaml is a YAML 1.2 loader/dumper package for Python.
It is a derivative of Kirill Simonov’s PyYAML 3.11

%package -n     python3-%{srcname}
Summary:        YAML 1.2 loader/dumper package for Python

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-wheel

Requires:       python3-ruamel-yaml-clib

# For tests
%if %{with_check}
BuildRequires:  python3-ruamel-yaml-clib
BuildRequires:  python3-pytest
BuildRequires:  python3-tomli
%endif

%description -n python3-%{srcname}
ruamel.yaml is a YAML 1.2 loader/dumper package for Python.
It is a derivative of Kirill Simonov’s PyYAML 3.11

%prep
%autosetup -n ruamel-yaml-code-%{commit}

%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files ruamel

%check
pip3 install exceptiongroup iniconfig
%pytest _test/test_*.py

%files -n python3-%{srcname} -f %{pyproject_files}
%license LICENSE
%doc README.md

%changelog
* Wed Feb 21 2024 Chris Gunn <chrisgun@mircosoft.com> - 0.18.6-1
- Update to 0.18.6
- Switch to sourceforge sources
- Enable tests

* Wed Oct 20 2021 Thomas Crain <thcrain@microsoft.com> - 0.16.6-7
- Remove requirement on python3-typing (not needed for python >= 3.5)

* Mon Jun 21 2021 Rachel Menge <rachelmenge@microsoft.com> - 0.16.6-6
- Initial CBL-Mariner import from Fedora 34 (license: MIT)
- License verified

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.16.6-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Jason Montleon <jmontleo@redhat.com> - 0.16.6-1
- Update to 0.16.6

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.16.5-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Fri Aug 30 2019 Chandan Kumar <raukadah@gmail.com> - 0.16.5-2
- Added ruamel-yaml-clib as Requires

* Tue Aug 27 2019 Chedi Toueiti <chedi.toueiti@gmail.com> - 0.16.5-1
- Update to 0.16.5

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.41-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.41-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.41-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0.15.41-3
- Subpackage python2-ruamel-yaml has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Jun 29 2018 Miro Hrončok <mhroncok@redhat.com> - 0.15.41-1
- Update to 0.15.41
- Add patch not to require ruamel.std.pathlib

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.14-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.14-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 9 2017 Orion Poplawski <orion@nwra.com> - 0.13.14-1
- Update to 0.13.14

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Jan Chaloupka <jchaloup@redhat.com> - 0.13.13-3
- The ruamel.yaml needs at least typing >= 3.5.2.2
  related: #1386563

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 0.13.13-1
- Update to 0.13.13

* Tue Jan 31 2017 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-7
- Add patch to support pytest 2.7 in EPEL7

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.12.14-6
- Rebuild for Python 3.6

* Wed Oct 26 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-5
- Require python34-typing on EPEL
- Ignore python2 test failure due to old pytest on EPEL7

* Wed Oct 26 2016 Orion Poplawski <orion@cora.nwra.com> - 0.12.14-4
- Build python3 package
- Run tests

* Tue Oct 25 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-3
- Disabling python3 as python3-ruamel-ordereddict not available

* Mon Oct 24 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-2
- Fixed python2-typing runtime dependency issue

* Fri Oct 14 2016 Chandan Kumar <chkumar@redhat.com> - 0.12.14-1
- Initial package.
