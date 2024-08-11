%global pypi_name markdown-it-py
%global _description %{expand:
Markdown parser done right. Its features:
Follows the CommonMark spec for baseline parsing.
Has configurable syntax: you can add new rules and even replace existing ones.
Pluggable: Adds syntax extensions to extend the parser.
High speed & safe by default
}
Summary:        Python port of markdown-it
Name:           python-%{pypi_name}
Version:        3.0.0
Release:        6%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/executablebooks/markdown-it-py
Source0:        %{url}/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-mdurl
%endif
BuildArch:      noarch
# The plugins extras creates a bootstrap loop
%bcond plugins 1

%description %{_description}

%package -n     python3-%{pypi_name}
Summary:        %{summary}
Requires:       python3-mdurl
Requires:       python3-flit-core

%description -n python3-%{pypi_name} %{_description}

%pyproject_extras_subpkg -n python3-%{pypi_name} linkify %{?with_plugins:plugins}

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# Remove unnecessary shebang
sed -i '1{\@^#!/usr/bin/env python@d}' markdown_it/cli/parse.py
# Remove coverage (it resides in testing extra which we want to use)
# Upstream issue to move those to another extra:
# https://github.com/executablebooks/markdown-it-py/issues/195
sed -i '/"coverage",/d' pyproject.toml
sed -i '/"pytest-cov",/d' pyproject.toml

%build
%{pyproject_wheel}

%install
%{pyproject_install}
%pyproject_save_files markdown_it

%check
pip3 install iniconfig linkify-it-py pytest-regressions
%pytest tests/

%files -n python3-%{pypi_name} -f %{pyproject_files}
%license LICENSE LICENSE.markdown-it
%doc README.md
%{_bindir}/markdown-it

%changelog
* Mon May 13 2024 Sam Meluch <sammeluch@microsoft.com> - 3.0.0-6
- Add missing dep on pytest for check section

* Thu Mar 28 2024 Riken Maharjan <rmaharjan@microsoft.com> - 3.0.0-5
- Initial CBL-Mariner import from Fedora 40 (license: MIT)
- License verified

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 07 2023 Karolina Surma <ksurma@redhat.com> - 3.0.0-1
- Update to 3.0.0
Resolves: rhbz#2212028

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 2.2.0-3
- Rebuilt for Python 3.12

* Thu Jun 29 2023 Python Maint <python-maint@redhat.com> - 2.2.0-2
- Bootstrap for Python 3.12

* Wed Mar 15 2023 Karolina Surma <ksurma@redhat.com> - 2.2.0-1
- Update to 2.2.0, includes the fix for CVE-2023-26302
Resolves: rhbz#2172373 rhbz#2177154
- Provide extra subpackages: linkify and plugins

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 2.1.0-2
- Rebuilt for Python 3.11

* Tue Apr 19 2022 LumÃ­r Balhar <lbalhar@redhat.com> - 2.1.0-1
- Update to 2.1.0
Resolves: rhbz#2075950

* Mon Jan 31 2022 Karolina Surma <ksurma@redhat.com> - 2.0.1-1
- Update to 2.0.1
Resolves: rhbz#2028769
- Generate test dependencies from upstream data instead of hardcoding them

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 Karolina Surma <ksurma@redhat.com> - 1.1.0-4
- Enable more tests in %%check using pytest-regressions

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.10

* Thu May 13 2021 Karolina Surma <ksurma@redhat.com> - 1.1.0-1
- Initial package.
