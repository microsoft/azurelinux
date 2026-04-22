# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global srcname cssselect2

Name:           python-%{srcname}
Version:        0.8.0
Release: 7%{?dist}
Summary:        CSS selectors for Python ElementTree
License:        BSD-3-Clause
URL:            https://doc.courtbouillon.org/cssselect2/stable/
BuildArch:      noarch
Source0:        %{pypi_source cssselect2}

BuildRequires:  python3-devel

%description
cssselect2 is a straightforward implementation of CSS4 Selectors for markup
documents (HTML, XML, etc.) that can be read by ElementTree-like parsers,
including cElementTree, lxml, html5lib, etc.


%package -n python3-%{srcname}
Summary:        %{summary}

%description -n python3-%{srcname}
cssselect2 is a straightforward implementation of CSS4 Selectors for markup
documents (HTML, XML, etc.) that can be read by ElementTree-like parsers,
including cElementTree, lxml, html5lib, etc.


%prep
%autosetup -p1 -n %{srcname}-%{version}
# Skip the flake8 plugin: linting is useful for upstream only. Also flake8 was
# not available in time for the Python 3.9 rebuild (and that might be the case
# for Python 3.10+) so let's just remove it.
# Same for isort.
# Same for ruff.
sed -i -e "s/, 'flake8'//" -e "s/, 'isort'//" -e "s/, 'ruff'//" pyproject.toml

%generate_buildrequires
%pyproject_buildrequires -x test


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{srcname}

%check
%pytest


%files -n python3-%{srcname} -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.8.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.8.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.8.0-3
- Rebuilt for Python 3.14

* Thu Mar 13 2025 Davide Cavalca <dcavalca@fedoraproject.org> - 0.8.0-2
- Drop ruff dependency

* Thu Mar 06 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 0.8.0-1
- update to 0.8.0

* Fri Jan 24 2025 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.0-11
- SPDX migration

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 04 2024 Miroslav Suchý <msuchy@redhat.com> - 0.7.0-9
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.7.0-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 04 2023 Python Maint <python-maint@redhat.com> - 0.7.0-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Sep 19 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.7.0-1
- update to 0.7.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.6.0-2
- Rebuilt for Python 3.11

* Mon Apr 18 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.6.0-1
- update to 0.6.0

* Tue Mar 01 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.5.0-1
- update to 0.5.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.3.0-7
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Aug 03 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 0.3.0-5
- add patch from upstream to fix isort test failure

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-4
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.0-2
- Rebuilt for Python 3.9

* Tue Mar 17 2020 Felix Schwarz <fschwarz@fedoraproject.org> - 0.3.0-1
- update to 0.3.0

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Felix Schwarz <fschwarz@fedoraproject.org> 0.2.2-2
- use sources from pypi, packaging fixes

* Thu Oct 24 2019 Felix Schwarz <fschwarz@fedoraproject.org> 0.2.2-1
- update to new upstream version 0.2.2

* Thu May 02 2019 Eric Smith <brouhaha@fedoraproject.org> 0.2.1-3
- Moved Requires to subpackage. Added python_provide.

* Wed May 01 2019 Eric Smith <brouhaha@fedoraproject.org> 0.2.1-2
- Added missing BuildRequires and Requires.

* Tue Apr 30 2019 Eric Smith <brouhaha@fedoraproject.org> 0.2.1-1
- Initial version.

