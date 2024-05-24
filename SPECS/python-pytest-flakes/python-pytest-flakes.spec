%{?python_enable_dependency_generator}
%global srcname pytest-flakes

Name:           python-%{srcname}
Version:        4.0.5
Release:        9%{?dist}
Summary:        Pytest plugin to check source code with pyflakes

License:        MIT
URL:            https://pypi.python.org/pypi/pytest-flakes
Source0:        %{pypi_source}

BuildArch:      noarch

%description
Py.test plugin for efficiently checking python source with pyflakes.

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3dist(pytest) >= 2.8
BuildRequires:  python3dist(pyflakes)
%if 0%{?with_check}
BuildRequires:  python3-pip
%endif

%description -n python3-%{srcname}
Py.test plugin for efficiently checking python source with pyflakes.

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}
rm -rf *.egg-info

%build
%py3_build

%install
%py3_install

%check
%{__python3} setup.py test

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/pytest_flakes-*.egg-info/
%{python3_sitelib}/pytest_flakes.py
%{python3_sitelib}/__pycache__/pytest_flakes.*

%changelog
* Mon May 20 2024 Sam Meluch <sammeluch@microsoft.com> - 4.0.5-9
- Add pip test dependency to fix package tests

* Tue Feb 27 2024 Dan Streetman <ddstreet@microsoft.com> - 4.0.5-8
- Initial CBL-Mariner import from Fedora 39 (license: MIT).
- license verified

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 20 2023 Python Maint <python-maint@redhat.com> - 4.0.5-6
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 4.0.5-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Dec 06 2020 Chedi Toueiti <chedi.toueiti@gmail.com> - 4.0.5-1
- Update to 4.0.5 (#2017557)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.3-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 08 2020 Chedi Toueiti <chedi.toueiti@gmail.com> - 4.0.3-1
- Update to 4.0.3 (#1902352)

* Thu Oct 22 2020 Chedi Toueiti <chedi.toueiti@gmail.com> - 4.0.2-1
- Update to 4.0.2 (#1880588)

* Tue Jul 28 2020 Chedi Toueiti <chedi.toueiti@gmail.com> - 4.0.1-1
- Update to 4.0.1 (#1861534)

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-6
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Thu Aug 22 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-5
- Subpackage python2-pytest-flakes has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Sep 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-4
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.0.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Nov 17 2017 Orin Poplawski <orion@nwra.com> - 2.0.0-1
- Update to 2.0.0

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.0.1-5
- Rebuild for Python 3.6

* Wed Nov 16 2016 Orion Poplawski <orion@cora.nwra.com> - 1.0.1-4
- Do not own __pycache__ dir

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 22 2016 Adam Williamson <awilliam@redhat.com> - 1.0.1-1
- new release 1.0.1 (compatible with pytest 2.8)
- rename py2 package to python2-pytest-flakes
- only require pytest-cache on <F24 (and EPEL), pytest 2.8 includes it
- use pyX_build and pyX_install
- use license macro
- provide python2-pytest-flakes
- drop EPEL 6 workarounds from spec as we can't build on EPEL 6 anyway

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 19 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Sat Mar 22 2014 Orion Poplawski <orion@cora.nwra.com> - 0.2-2
- Capitalize summary/description
- Add upstream license file

* Tue Feb 25 2014 Orion Poplawski <orion@cora.nwra.com> - 0.2-1
- Initial package
