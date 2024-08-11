
%global _description %{expand:
A PEP 517 build backend implementation developed for Poetry.
This project is intended to be a light weight, fully compliant, self-contained
package allowing PEP 517 compatible build frontends to build Poetry managed
projects.}
Summary:        Poetry PEP 517 Build Backend
Name:           python-poetry-core
Version:        1.9.0
Release:        3%{?dist}
# SPDX
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/python-poetry/poetry-core
Source0:        %{url}/archive/%{version}/poetry-core-%{version}.tar.gz
# This patch moves the vendored requires definition
# from vendors/pyproject.toml to pyproject.toml
# Intentionally contains the removed hunk to prevent patch aging
Patch1:         poetry-core-1.9.0-devendor.patch
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-fastjsonschema
BuildRequires:  python3-lark
BuildRequires:  python3-pip
BuildArch:      noarch

%description %{_description}

%package -n python3-poetry-core
Summary:        %{summary}
# Previous versions of poetry included poetry-core in it
Conflicts:      python%{python3_version}dist(poetry) < 1.1

%description -n python3-poetry-core %{_description}

%prep
%autosetup -p1 -n poetry-core-%{version}



%build
# we debundle the deps after we use the bundled deps in previous step to parse the deps ðŸ¤¯
rm -r src/poetry/core/_vendor

%{pyproject_wheel}


%install
%{pyproject_install}
%pyproject_save_files poetry


%files -n python3-poetry-core -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Fri Mar 29 2024 Riken Maharjan <rmaharjan@microsoft.com> - 1.9.0-1
- Initial CBL-Mariner import from Fedora 40 (license: MIT).
- License Verified

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.8.1-1
- Update to 1.8.1
- Fixes: rhbz#2247249

* Thu Jan 04 2024 Florian Weimer <fweimer@redhat.com> - 1.7.0-2
- Backport upstream patch to fix C compatibility issue

* Fri Sep 01 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.7.0-1
- Update to 1.7.0
- Fixes: rhbz#2232934

* Wed Aug 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.6.1-2
- Drop unwanted tomli dependency

* Wed Jul 26 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.6.1-1
- Update to 1.6.1
- Fixes: rhbz#2144878

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 30 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.6.0-1
- Update to 1.6.0

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.4.0-4
- Rebuilt for Python 3.12

* Mon May 29 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.4.0-3
- Disable tests in RHEL builds

* Sat Feb 25 2023 Miro Hrončok <mhroncok@redhat.com> - 1.4.0-2
- Remove unused build dependency on python3-pep517

* Mon Feb 20 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.4.0-1
- Update to 1.4.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.3.2-1
- Update to 1.3.2
- Fixes: rhbz#1944752

* Wed Nov 16 2022 Lumír Balhar <lbalhar@redhat.com> - 1.2.0-2
- Add missing buildrequire - setuptools (#2142040)

* Fri Sep 30 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.2.0-1
- Update to 1.2.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.8-2
- Rebuilt for Python 3.11

* Mon Mar 07 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.8-1
- Update to 1.0.8

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.7-1
- Update to 1.0.7

* Fri Oct 01 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 1.0.6-1
- Update to 1.0.6

* Tue Sep 07 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.4-1
- Update to 1.0.4

* Thu Aug 19 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.3-5
- Bundle vendored libraries again, to fix poetry install

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Lumír Balhar <lbalhar@redhat.com> - 1.0.3-3
- Allow newer packaging version
- Allow newer pyrsistent version

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.3-2
- Rebuilt for Python 3.10

* Thu Apr 15 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Thu Feb 25 2021 Tomas Hrnciar <thrnciar@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 02 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0.0-1
- Initial package
