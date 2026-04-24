# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname mercantile

Name:           python-%{srcname}
Version:        1.2.1
Release: 20%{?dist}
Summary:        Web Mercator XYZ tile utilities

License:        BSD-3-Clause
URL:            https://github.com/mapbox/mercantile
Source0:        %{url}/archive/%{version}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3dist(click)
BuildRequires:  python3dist(hypothesis)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(setuptools)

BuildRequires:  python3dist(sphinx)
BuildRequires:  python3dist(numpydoc)

%global _description %{expand:\
Mercantile is a module of utilities for working with XYZ style Spherical
Mercator tiles (as in Google Maps, OSM, Mapbox, etc.) and includes a set of
command line programs built on these utilities.}

%description %{_description}


%package -n     python3-%{srcname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname} %{_description}


%prep
%autosetup -n %{srcname}-%{version}
# Remove bundled egg-info
rm -rf %{srcname}.egg-info

%build
%py3_build

# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 docs html

# remove the sphinx-build leftovers
rm -rf html/.{buildinfo,doctrees}

%install
%py3_install

%check
%{pytest}

%files -n python3-%{srcname}
%doc README.rst html
%license LICENSE.txt
%{_bindir}/mercantile
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-%{version}-py%{python3_version}.egg-info/

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.2.1-19
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.2.1-18
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.2.1-16
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 1.2.1-13
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Python Maint <python-maint@redhat.com> - 1.2.1-9
- Rebuilt for Python 3.12

* Sat Apr 08 2023 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.2.1-8
- Switch to SPDX license

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.2.1-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.2.1-2
- Rebuilt for Python 3.10

* Thu Apr 22 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.2.1-1
- Update to latest version (#1948656)

* Wed Apr 21 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.2.0-1
- Update to latest version (#1948656)

* Sun Mar 28 2021 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.6-2
- Remove unnecessary check-manifest BR

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 25 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.6-1
- Update to latest version (#1871899)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 21 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.5-1
- Update to latest version

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.4-2
- Rebuilt for Python 3.9

* Thu Apr 30 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.4-1
- Update to latest version

* Tue Apr 14 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.3-1
- Update to latest version

* Thu Feb 13 2020 Elliott Sales de Andrade <quantum.analyst@gmail.com> - 1.1.2-1
- Initial package.
