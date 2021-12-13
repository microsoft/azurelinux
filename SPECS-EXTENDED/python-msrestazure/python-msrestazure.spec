Vendor:         Microsoft Corporation
Distribution:   Mariner
%global srcname msrestazure
%global common_description %{summary}.

Name:           python-%{srcname}
Version:        0.6.4
Release:        2%{?dist}
Summary:        The runtime library "msrestazure" for AutoRest generated Python clients

License:        MIT
URL:            https://github.com/Azure/msrestazure-for-python/
Source0:        %{url}/archive/v%{version}/%{srcname}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3dist(adal)
BuildRequires:  python3dist(httpretty)
BuildRequires:  python3dist(msrest)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-cov)
BuildRequires:  python3dist(setuptools)
# Required to build documentation
BuildRequires:  python3dist(pip)
BuildRequires:  python3dist(recommonmark)
BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(sphinx-rtd-theme)
BuildArch:      noarch

%description
%{common_description}


%package -n python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
%{common_description}


%package doc
Summary:        Documentation for %{name}

%description doc
This package provides documentation for %{name}.


%prep
%autosetup -n %{srcname}-for-python-%{version}

# Remove bundled egg-info
rm -rf *.egg-info


%build
%py3_build

pushd doc/
sphinx-build -b html -d _build/doctrees/ . _build/html/
rm _build/html/.buildinfo
popd


%install
%py3_install


%check
pytest-%{python3_version}


%files -n python3-%{srcname}
%doc README.rst
%license LICENSE.md
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/


%files doc
%doc doc/_build/html/
%license LICENSE.md


%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.6.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jul 01 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.6.4-1
- Update to 0.6.4

* Tue Apr 07 2020 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.6.3-1
- Update to 0.6.3

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Sep 19 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.6.2-1
- Update to 0.6.2

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.6.1-2
- Rebuilt for Python 3.8

* Fri Aug 09 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.6.1-1
- Update to 0.6.1

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 04 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.6.0-2
- Fix Python 3-only file deployment

* Mon Feb 04 2019 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.6.0-1
- Update to 0.6.0

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.5.1-2
- Rebuild for python-msrest dependency fix update

* Sun Nov 11 2018 Mohamed El Morabity <melmorabity@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1
- Build documentation
