# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name lesscpy

%if 0%{?rhel} > 7
# Disable python2 build by default
%endif

Name:           python-%{pypi_name}
Version:        0.14.0
Release: 23%{?dist}
Summary:        Lesscss compiler

License:        MIT
URL:            https://github.com/robotis/lesscpy
Source0:        https://pypi.python.org/packages/source/l/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch
 
%global _description\
A compiler written in python 3 for the lesscss language.  For those of us not\
willing/able to have node.js installed in our environment.  Not all features\
of lesscss are supported (yet).  Some features wil probably never be\
supported (JavaScript evaluation).

%description %_description


%package -n python3-lesscpy
Summary:    %summary
Requires:   python3-ply
Requires:   python3-six
BuildRequires: python3-devel
BuildRequires: python3-setuptools
BuildRequires: python3-ply
BuildRequires: python3-pytest
BuildRequires: python3-six
%{?python_provide:%python_provide python3-lesscpy}

%description -n python3-lesscpy
A compiler written in python 3 for the lesscss language.  For those of us not
willing/able to have node.js installed in our environment.  Not all features
of lesscss are supported (yet).  Some features wil probably never be
supported (JavaScript evaluation).

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

%build

%py3_build


%install

%py3_install
# link for backwards compatibility. consider removal in Fedora 30+
ln -s ./lesscpy %{buildroot}/%{_bindir}/py3-lesscpy


%check
%pytest


%files -n python3-lesscpy
%doc LICENSE
%{_bindir}/lesscpy
%{_bindir}/py3-lesscpy
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.egg-info


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.14.0-22
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.14.0-21
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.14.0-19
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.14.0-16
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.14.0-12
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.14.0-9
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.14.0-6
- Rebuilt for Python 3.10

* Wed Feb 03 2021 Christian Heimes <cheimes@redhat.com> - 0.14.0-5
- Check with pytest instead of nose
- Remove build dependency on coverage

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14.0-2
- Rebuilt for Python 3.9

* Mon Feb 24 2020 Thomas Andrejak <thomas.andrejak@gmail.com> - 0.14.0-1
- Bump version 0.14.0 (Fix #1792982)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-12
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-11
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.13.0-8
- Subpackage python2-lesscpy has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Jul 16 2018 Marcel Plch <mplch@redhat.com> - 0.13.0-7
- Remove the unused flake8 build dependency

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-5
- Rebuilt for Python 3.7

* Wed Jun 13 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-4
- Add explicit conflicts

* Tue Jun 12 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-3
- General spec cleanup
- Add missing dependency on six
- Run the tests

* Tue Jun 12 2018 Miro Hrončok <mhroncok@redhat.com> - 0.13.0-2
- /usr/bin/lesscpy is Python 3

* Mon Jun 11 2018 Christian Heimes <cheimes@redhat.com> - 0.13.0-1
- New upstream release 0.13.0, resolves rhbz#1584773

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.10.1-12
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.10.1-11
- Python 2 binary package renamed to python2-lesscpy
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.1-8
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-7
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-5
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 14 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/Python_3.4

* Tue Feb 11 2014 Matthias Runge <mrunge@redhat.com> - 0.10.1-1
- update to 0.10.1

* Thu Aug 29 2013 Matthias Runge <mrunge@redhat.com> - 0.9j-3
- use python instead of python3 in python2 package

* Wed Aug 21 2013 Matthias Runge <mrunge@redhat.com> - 0.9j-2
- add br python-ply

* Mon Jul 29 2013 Matthias Runge <mrunge@redhat.com> - 0.9j-1
- Initial package.
