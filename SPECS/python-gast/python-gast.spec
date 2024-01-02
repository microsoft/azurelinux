%global _description %{expand:
A generic AST to represent Python3's Abstract Syntax Tree (AST).
GAST provides a compatibility layer between the AST of various Python versions,
as produced by ast.parse from the standard ast module.}

Summary:        Python AST that abstracts the underlying Python version
Name:           python-gast
Version:        0.5.4
Release:        1%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/serge-sans-paille/gast
Source0:        %{url}/archive/%{version}/gast-%{version}.tar.gz
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildArch:      noarch

%description %{_description}

%package -n     python3-gast
Summary:        %{summary}

%description -n python3-gast %{_description}

%prep
%autosetup -p1 -n gast-%{version}

%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files gast


%check
pip3 install tox tox-current-env pytest==7.1.3
%tox


%files -n python3-gast -f %{pyproject_files}
%license LICENSE
%doc README.rst

%changelog
* Thu Nov 02 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 0.5.4-1
- Auto-upgrade to 0.5.4 - Azure Linux 3.0 - package upgrades

* Thu Oct 20 2022 Riken Maharjan <rmaharjan@microsoft.com> - 0.5.3-5
- Initial CBL-Mariner import from Fedora 37 (license: MIT).
- License verified.

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.5.3-3
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Nov 30 2021 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Thu Jul 29 2021 Tomas Hrnciar <thrnciar@redhat.com> - 0.5.2-1
- Update to 0.5.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 28 2021 Miro Hrončok <mhroncok@redhat.com> - 0.5.0-1
- Update to 0.5.0
- Fixes rhbz#1977051
- Fixes rhbz#1968986

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.4.0-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 11 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4.0-1
- Update to 0.4.0
- Fixes rhbz#1878159

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Miro Hrončok <mhroncok@redhat.com> - 0.3.3-1
- Update to 0.3.3 (#1844892)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Oct 12 2019 Miro Hrončok <mhroncok@redhat.com> - 0.3.2-1
- Update to 0.3.2

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jan 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.2.2-1
- Initial package
