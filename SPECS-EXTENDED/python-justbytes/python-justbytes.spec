%global srcname justbytes

Name:           python-%{srcname}
Version:        0.15.2
Release:        8%{?dist}
Summary:        Library for handling computation with address ranges in bytes

License:        LGPL-2.1-or-later
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            http://pypi.python.org/pypi/justbytes
Source0:        https://pypi.io/packages/source/j/%{srcname}/%{srcname}-%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%global _description \
A library for handling computations with address ranges. The library also offers\
a configurable way to extract the representation of a value.

%description %{_description}

%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

%description -n python3-%{srcname} %{_description}

Python 3 version.

%prep
%autosetup -n %{srcname}-%{version}
rm -rf justbytes.egg-info

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/justbytes/
%{python3_sitelib}/justbytes-%{version}-*.egg-info/

%changelog
* Fri Dec 20 2024 Akhila Guruju <v-guakhila@microsoft.com> - 0.15.2-8
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.15.2-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.15.2-2
- Rebuilt for Python 3.12

* Mon May 15 2023 mulhern <amulhern@redhat.com> - 0.15.2-1
- Update to 0.15.2

* Mon May 15 2023 mulhern <amulhern@redhat.com> - 0.15.1-2
- Add .fmf/version file

* Mon May 15 2023 mulhern <amulhern@redhat.com> - 0.15.1-1
- Update to 0.15.1; use SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.15-9
- Rebuilt for Python 3.11

* Sun Feb 27 2022 mulhern <amulhern@redhat.com> - 0.15-8
- Add gating tests

* Tue Feb 15 2022 mulhern <amulhern@redhat.com> - 0.15-7
- Drop redundant requires

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.15-4
- Rebuilt for Python 3.10

* Mon Mar 22 2021 mulhern <amulhern@redhat.com> - 0.15-3
- Use the correct tarball

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 17 2020 mulhern <amulhern@redhat.com> - 0.15-1
- Update to 0.15

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.14-2
- Rebuilt for Python 3.9

* Thu Apr 23 2020 mulhern <amulhern@redhat.com> - 0.14-1
- Update to new release

* Thu Apr 23 2020 mulhern <amulhern@redhat.com> - 0.12-1
- Change license to LGPLv2+

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.11-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.11-5
- Subpackage python2-justbytes has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.11-3
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.11-1
- Update to 0.11

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10-2
- Rebuild for Python 3.6

* Wed Aug 10 2016 mulhern <amulhern@redhat.com> - 0.10
- New release

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Mar 23 2016 mulhern <amulhern@redhat.com> - 0.6
- Initial release
