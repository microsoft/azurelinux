%bcond_with    tests

%global         srcname     msrestazure
%global         forgeurl    https://github.com/Azure/msrestazure-for-python/

Summary:        The runtime library "msrestazure" for AutoRest generated Python clients
Vendor:         Microsoft Corporation
Distribution:   Mariner
Version:        0.6.4
Name:           python-%{srcname}
Release:        11%{?dist}

License:        MIT
%global         tag         v%{version}
URL:            %forgeurl
Source0:        https://github.com/Azure/msrestazure-for-python/archive/v%{version}/msrestazure-for-python-%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-packaging
BuildRequires:  python3-requests
BuildRequires:  python3-wheel


%if %{with_check}
BuildRequires:  python3dist(pytest)

# Missing test dependencies:
# BuildRequires:  python3dist(httpretty)
%endif

%global _description %{expand:
The runtime library "msrest" for AutoRest generated Python clients}

%description %{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -p1 -n msrestazure-for-python-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}


%check
%pytest


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE.md


%changelog
* Thu Aug 31 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.4-11
- Disabling missing test dependency.

* Wed Mar 15 2023 Muhammad Falak <mwani@microsoft.com> - 0.6.4-10
- Rename Source0 to `%{name}-%{version}.extension

* Fri Mar 03 2023 Muhammad Falak <mwani@microsoft.com> - 0.6.4-9
- Convert 'Release' tag to '[number].[distribution]' format
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified

* Mon Apr 25 2022 Major Hayden <major@mhtx.net> 0.6.4-8
- Disable tests in EPEL 9

* Mon Apr 25 2022 Major Hayden <major@mhtx.net> 0.6.4-7
- Update to use pyproject-rpm-macros

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> 0.6.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> 0.6.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> 0.6.4-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> 0.6.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> 0.6.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 01 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.6.4-1
- Update to 0.6.4

* Tue May 26 2020 Miro Hrončok <miro@hroncok.cz> 0.6.3-2
- Rebuilt for Python 3.9

* Tue Apr 07 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.6.3-1
- Update to 0.6.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.6.2-1
- Update to 0.6.2

* Mon Aug 19 2019 Miro Hrončok <miro@hroncok.cz> 0.6.1-3
- Rebuilt for Python 3.8

* Fri Aug 09 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.6.1-1
- Update to 0.6.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.6.0-2
- Fix Python 3-only file deployment

* Mon Feb 04 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.6.0-1
- Update to 0.6.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.5.1-2
- Rebuild for python-msrest dependency fix update

* Tue Nov 13 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.5.1-1
- Update to 0.5.1

* Sun Aug 05 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.5.0-1
- Fix version

* Sun Aug 05 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> 0.6.0-2
- RPMAUTOSPEC: unresolvable merge
