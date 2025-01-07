%global srcname dbus-python-client-gen

Name:           python-%{srcname}
Version:        0.8.3
Release:        8%{?dist}
Summary:        Python Library for Generating dbus-python Client Code
License:        MPL-2.0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/stratis-storage/dbus-python-client-gen
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/python-%{srcname}-%{version}.tar.gz
BuildArch:      noarch

%global _description \
%{summary}.

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

%build
%py3_build

%install
%py3_install

%files -n python3-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/dbus_python_client_gen/
%{python3_sitelib}/dbus_python_client_gen-*.egg-info/

%changelog
* Mon Dec 23 2024 Akhila Guruju <v-guakhila@microsoft.com> - 0.8.3-8
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.8.3-6
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.8.3-2
- Rebuilt for Python 3.12

* Thu Apr 27 2023 mulhern <amulhern@redhat.com> - 0.8.3-1
- Update to 0.8.3

* Tue Apr 25 2023 mulhern <amulhern@redhat.com> - 0.8.2-6
- Revise gating.yaml so that the phantom tier0 test becomes real

* Tue Apr 25 2023 mulhern <amulhern@redhat.com> - 0.8.2-5
- Rebuild again to see if tier0 test continues to appear

* Tue Apr 25 2023 mulhern <amulhern@redhat.com> - 0.8.2-4
- Rebuild to get rid of phantom tier0 test

* Tue Apr 25 2023 mulhern <amulhern@redhat.com> - 0.8.2-3
- Amend tmt specification

* Tue Apr 25 2023 mulhern <amulhern@redhat.com> - 0.8.2-2
- Use tmt format testing specification

* Thu Feb 23 2023 Bryan Gurney <bgurney@redhat.com> - 0.8.2-1
- Update to 0.8.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.8-9
- Rebuilt for Python 3.11

* Sat Feb 26 2022 mulhern <amulhern@redhat.com> - 0.8-8
- Fix gating tests

* Sat Feb 26 2022 mulhern <amulhern@redhat.com> - 0.8-7
- Add gating tests

* Tue Feb 15 2022 mulhern <amulhern@redhat.com> - 0.8-6
- Remove redundant Requires

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.8-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Dec 8 2020 mulhern <amulhern@redhat.com> - 0.8-1
- Update to 0.8

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7-8
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.7-6
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7-2
- Rebuilt for Python 3.7

* Tue May 1 2018 Andy Grover <agrover@redhat.com> - 0.7-1
- Update to 0.7

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.6-1
- Update to 0.6

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5-1
- Initial import
