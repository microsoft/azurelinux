%global pypi_name smartypants
Summary:        plug-in that easily translates ASCII punctuation characters into smart entities
Name:           python-%{pypi_name}
Version:        2.0.1
Release:        22%{?dist}
License:        BSD-3-Clause AND BSD-2-Clause
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/leohemsted/smartypants.py
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(sphinx)
BuildArch:      noarch

%description
SmartyPants is a free web publishing plug-in for Movable
Type, Blosxom, and BBEdit that easily translates plain ASCII
punctuation characters into “smart” typographic punctuation HTML
entities.

%package -n     python3-%{pypi_name}
%{?python_provide:%python_provide python3-%{pypi_name}}
Summary:        %{summary}
Requires:       python3dist(setuptools)

%description -n python3-%{pypi_name}
SmartyPants is a free web publishing plug-in for Movable
Type, Blosxom, and BBEdit that easily translates plain ASCII
punctuation characters into “smart” typographic punctuation HTML
entities.

%package -n python-%{pypi_name}-doc
Summary:        python-smartypants documentation

%description -n python-%{pypi_name}-doc
Documentation for python-smartypants

%prep
%autosetup -n %{pypi_name}.py-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
for lib in $(find -type f -name '*.py'); do
 sed -i.python -e '1{\@^#!@d}' $lib
done
sed -i.python -e 's|#!/usr/bin/env python|#!/usr/bin/python3|' smartypants


%build
%py3_build
# generate html documentation
cd docs
make html
# remove the sphinx-build leftovers
rm -rf _build/html/.{doctrees,buildinfo}


%install
%py3_install

%check
python3 setup.py test


%files -n python3-%{pypi_name}
%doc README.rst
%doc CHANGES.rst
%license COPYING
%{_bindir}/%{pypi_name}
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{pypi_name}.py
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%files -n python-%{pypi_name}-doc
%doc docs/_build/html
%license COPYING

%changelog
* Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 2.0.1-22
- Integrating the spec into Azure Linux
- Initial CBL-Mariner import from Fedora 41 (license: MIT).
- License verified.

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 2.0.1-20
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 2.0.1-16
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.0.1-13
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.1-10
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 11 2019 José Matos <jamatos@fedoraproject.org> - 2.0.1-2
- fix source url, license short hand, description and summary.
- remove shebang lines and make smartypants a shebang line use python3.

* Sat Sep  1 2018 José Matos <jamatos@fedoraproject.org> - 2.0.1-1
- initial package.
