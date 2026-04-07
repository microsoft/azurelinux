# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname d2to1

Name: python-%{srcname}
Version: 0.2.12
Release: 40.post1%{?dist}
Summary: Allows using distutils2-like setup.cfg files with setup.py
License: BSD-3-Clause

URL: http://pypi.python.org/pypi/d2to1
#Source0: http://pypi.python.org/packages/source/d/d2to1/%{srcname}-%{version}.tar.gz
Source0: https://pypi.python.org/packages/source/d/d2to1/d2to1-0.2.12.post1.tar.gz

# Compatibility with the newer setuptools
Patch:   setuptools-compatibility.patch

BuildArch: noarch

%global _description\
d2to1 allows using distutils2-like setup.cfg files for a package's metadata\
with a distribute/setuptools setup.py script. It works by providing a\
distutils2-formatted setup.cfg file containing all of a package's metadata,\
and a very minimal setup.py which will slurp its arguments from the setup.cfg.

%description %_description

%package -n python3-d2to1
Summary: Allows using distutils2-like setup.cfg files with setup.py
%{?python_provide:%python_provide python3-d2to1}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
Requires:  python3-setuptools

%description -n python3-d2to1 %_description

%prep
%dnl %setup -q -n %{srcname}-%{version}
%autosetup -n %{srcname}-%{version}.post1 -p1

find . -name '*.py' | xargs sed -i '1s|^#!python|#!%{__python3}|'

%build
%py3_build

%install
%py3_install

%files -n python3-d2to1
%doc CHANGES.rst README.rst
%license LICENSE
%{python3_sitelib}/*


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.12-40.post1
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.12-39.post1
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-38.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.2.12-37.post1
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-36.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 09 2024 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.12-35.post1
- Add reviewed license identifier

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.2.12-34.post1
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-33.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 11 2024 Python Maint <python-maint@redhat.com> - 0.2.12-32.post1
- Rebuilt for Python 3.13

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.2.12-31.post1
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-30.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-29.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Sep 22 2023 Lumír Balhar <lbalhar@redhat.com> - 0.2.12-28.post1
- Fix compatibility with newer setuptools
Resolves: rhbz#2239998

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-27.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.2.12-26.post1
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-25.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-24.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.2.12-23.post1
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-22.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-21.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.2.12-20.post1
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-19.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-18.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-17.post1
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-16.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-15.post1
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-14.post1
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-13.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun May 05 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-12.post1
- Subpackage python2-d2to1 has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-11.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-10.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-9.post1
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.2.12-8.post1
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-7.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.2.12-6.post1
- Python 2 binary package renamed to python2-d2to1
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-5.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.12-4.post1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.2.12-3.post1
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.12-2.post1
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Mar 29 2016 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.12-1.post1
- New upstream source (0.2.12)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.11-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Mon Feb 24 2014 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.11-1
- New upstream source (0.2.11)
- Use python2 macro

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Apr 25 2013 Sergio Pascual <sergiopr@fedoraproject.org> - 0.2.10-1
- New upstream source

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 04 2013 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.7-2
- Requires for python3 inside python3 package (bz #891381)

* Wed Sep 26 2012 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.7-1
- New upstream source
- Removing upstream egg-info and defattr

* Thu Sep 22 2011 Sergio Pascual <sergiopr at fedoraproject.org> - 0.2.5-1
- Initial spec file

