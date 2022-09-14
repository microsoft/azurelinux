%global pypi_name outcome

%global _description \
Outcome provides a function for capturing the outcome of a Python function\
call, so that it can be passed around.

Summary:        Capture the outcome of Python function calls
Name:           python-%{pypi_name}
Version:        1.1.0
Release:        5%{?dist}
License:        MIT or ASL 2.0
URL:            https://github.com/python-trio/outcome
Source0:        %{url}/archive/refs/tags/v%{version}.tar.gz#/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

%description %{_description}

%package -n python3-%{pypi_name}
Summary:        %{summary}

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
Requires:       python3-attrs

%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name} %{_description}

%prep
%autosetup -n %{pypi_name}-%{version}

%build
%py3_build

%install
%py3_install

%check
%{python3} -m pip install -r test-requirements.txt
%pytest -v tests

%files -n python3-%{pypi_name}
%license LICENSE LICENSE.MIT LICENSE.APACHE2
%doc README.rst
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Wed Sep 14 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.1.0-6
- Initial CBL-Mariner import from Fedora 36 (license: MIT)
- Adding as dependency for package python-trio
- License verified

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 19 2022 Michel Alexandre Salim <salimma@fedoraproject.org> - 1.1.0-4
- Use old attrs API on EPEL 8

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.10

* Mon Feb 22 2021 Lumír Balhar <lbalhar@redhat.com> - 1.1.0-1
- Update to 1.1.0
Resolves: rhbz#1898627

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jul 31 2020 Charalampos Stratakis <cstratak@redhat.com> - 1.0.1-1
- Update to 1.0.1 (#1762713)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Sep 12 2018 Carl George <carl@george.computer> - 1.0.0-1
- Initial package
