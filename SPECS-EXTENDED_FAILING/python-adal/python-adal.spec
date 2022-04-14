Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname adal
%global _description %{expand:The ADAL for Python library makes it easy for python applications to
authenticate to AAD in order to access AAD protected web resources.}

Name:           python-%{srcname}
Version:        1.2.4
Release:        2%{?dist}
Summary:        ADAL for Python

License:        MIT
URL:            https://github.com/AzureAD/azure-activedirectory-library-for-python
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz
# Fix tests with httpretty >= 0.9.0
Patch0:         %{name}-1.2.0-tests.patch

BuildRequires:  python3-devel
BuildRequires:  %{py3_dist setuptools}
# Required for tests
BuildRequires:  %{py3_dist cryptography}
BuildRequires:  %{py3_dist httpretty}
BuildRequires:  %{py3_dist pyjwt}
BuildRequires:  %{py3_dist pytest}
BuildRequires:  %{py3_dist python-dateutil}
BuildRequires:  %{py3_dist requests}
# Required for documentation
BuildRequires:  %{py3_dist sphinx}
BuildRequires:  %{py3_dist sphinx-rtd-theme}
BuildArch:      noarch

%description
%{_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{_description}


%package doc
Summary:        Documentation for %{name}

%description doc
This package provides documentation for %{name}.


%prep
%autosetup -p0 -n azure-activedirectory-library-for-python-%{version}

# Remove bundled egg-info
rm -rf *.egg-info


%build
%py3_build

PYTHONPATH=$PWD/build/lib/ %make_build -C docs/ html
rm docs/build/html/{.buildinfo,.nojekyll}


%install
%py3_install


%check
pytest-%{python3_version}


%files -n python3-%{srcname}
%doc README.md
%license LICENSE
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/


%files doc
%doc docs/build/html/
%license LICENSE


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.2.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jun 26 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4
- Spec cleanup

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.2-3
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.2-2
- Rebuilt for Python 3.8

* Fri Aug 09 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2
- Add sphinx_rtd_theme build dependency for docs generation (fix by Charalampos
  Stratakis)

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Nov 10 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.0-2
- Build documentation

* Sat Nov 10 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
- Enable Python 3 support for EL
