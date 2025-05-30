## START: Set by rpmautospec
## (rpmautospec version 0.6.5)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 3;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

%global srcname prometheus_client

Name:           python-%{srcname}
Version:        0.20.0
Release:        4%{?dist}
Summary:        Python client for Prometheus
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        Apache-2.0
URL:            https://github.com/prometheus/client_python
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
Patch0001:      0001-Remove-the-bundled-decorator-package.patch

BuildArch:      noarch

%description
%{summary}.

%package -n python3-%{srcname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3dist(decorator)
BuildRequires:  python3dist(pytest)
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{summary}.

%package -n python3-%{srcname}+twisted
Summary:        %{summary}
Requires:       python3-%{srcname} = %{version}-%{release}
Requires:       python3-twisted
BuildRequires:  python3dist(twisted)
%{?python_provide:%python_provide python3-%{srcname}+twisted}

%description -n python3-%{srcname}+twisted
%{summary}.

"twisted" extras.

%prep
%autosetup -p1 -n client_python-%{version}
sed -i -e '1{/^#!/d}' prometheus_client/__init__.py

%build
%py3_build

%install
%py3_install

%check
%{__python3} -m pytest -v

%files -n python3-%{srcname}
%license LICENSE
%doc README.md MAINTAINERS.md
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/

%files -n python3-%{srcname}+twisted
%{?python_extras_subpkg:%ghost %{python3_sitelib}/%{srcname}-*.egg-info/}

%changelog
* Thu Jan 09 2025 Alberto David Perez Guevara <aperezguevar@microsoft.com> 0.20.0-4
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.20.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 0.20.0-2
- Rebuilt for Python 3.13

* Fri Feb 16 2024 Kai A. Hiller <V02460@gmail.com> - 0.20.0-1
- Update to v0.20.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Nov 23 2023 Kai A. Hiller <V02460@gmail.com> - 0.19.0-1
- Update to v0.19.0

* Wed Nov 15 2023 Kai A. Hiller <V02460@gmail.com> - 0.18.0-1
- Update to v0.18.0

* Sat Aug 19 2023 Kai A. Hiller <V02460@gmail.com> - 0.17.1-1
- Update to v1.17.1

* Sat Aug 19 2023 Kai A. Hiller <V02460@gmail.com> - 0.16.0-4
- SPDX migration

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.16.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 0.16.0-2
- Rebuilt for Python 3.12

* Wed Mar 29 2023 Kai A. Hiller <V02460@gmail.com> - 0.16.0-1
- Update to v0.16.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.13.1-2
- Rebuilt for Python 3.11

* Tue Feb 01 2022 Matt Prahl <mprahl@redhat.com> - 0.13.1-1
- Update to 0.13.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.9.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 12 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 10 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-4
- Add metadata for Python extras subpackages

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 23 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.1-1
- Update to 0.7.1
- Split twisted extras into a separate subpackage

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 18 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Feb 21 2019 mprahl <mprahl@redhat.com> - 0.6.0-1
- Update to 0.6.0

* Wed Feb 20 2019 mprahl <mprahl@redhat.com> - 0.5.0-2
- Remove #!/usr/bin/python line from prometheus_client/openmetrics/*.py

* Thu Feb 07 2019 mprahl <mprahl@redhat.com> - 0.5.0-1
- Update to 0.5.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-4
- Subpackage python2-prometheus_client has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.2.0-2
- Rebuilt for Python 3.7

* Sat Jun 09 2018 Jeremy Cline <jeremy@jcline.org> - 0.2.0-1
- Initial package

## END: Generated by rpmautospec
