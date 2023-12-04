%global pypi_name tox-current-env
%global pypi_under tox_current_env

Summary:        Tox plugin to run tests in current Python environment
Name:           python-%{pypi_name}
Version:        0.0.11
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/fedora-python/tox-current-env
Source0:        https://github.com/fedora-python/tox-current-env/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildArch:      noarch


BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(wheel)
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-pip

%description
The tox-current-env plugin allows to run tests in current Python environment.

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

%description -n python%{python3_pkgversion}-%{pypi_name}
The tox-current-env plugin allows to run tests in current Python environment.

%prep
%autosetup -n %{pypi_name}-%{version}


%generate_buildrequires
# Don't use %%pyproject_buildrequires -t/-e to avoid a build dependency loop
%pyproject_buildrequires -r


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{pypi_under}


%check
pip3 install tox
tox -e py%{python3_version_nodots}


%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Fri Oct 27 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.0.11-1
- Auto-upgrade to 0.0.11 - Azure Linux 3.0 - package upgrades

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 0.0.7-4
- Use `py%{python3_version_nodots}` instead of harcoding `py39`

* Fri Mar 04 2022 Bala <balakumaran.kannan@microsoft.com> - 0.0.7-3
- Use tox to run Ptest

* Mon Feb 14 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.0.7-2
- Initial CBL-Mariner import from Fedora 36 (license: MIT).
- License verified.

* Mon Feb 07 2022 Miro Hrončok <mhroncok@redhat.com> - 0.0.7-1
- Update to 0.0.7 to pin tox < 4

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Aug 05 2021 Miro Hrončok <mhroncok@redhat.com> - 0.0.6-4
- In %%check, test if the module at least imports

* Tue Jul 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.6-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 02 2021 Python Maint <python-maint@redhat.com> - 0.0.6-2
- Rebuilt for Python 3.10

* Mon Mar 29 2021 Miro Hrončok <mhroncok@redhat.com> - 0.0.6-1
- Update to 0.0.6

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Nov 25 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.5-1
- Update to 0.0.5

* Wed Nov 04 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.4-1
- Update to 0.0.4

* Wed Sep 30 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.3-1
- Update to 0.0.3

* Wed Aug 12 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-7
- Fix FTBFS with pyproject-rpm-macros >= 0-23

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-2
- Rebuilt for Python 3.8

* Mon Aug 12 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.2-1
- Update to 0.0.2

* Wed Jul 24 2019 Miro Hrončok <mhroncok@redhat.com> - 0.0.1-1
- Initial package
