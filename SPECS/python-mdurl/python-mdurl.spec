%global _description %{expand:
URL utilities for markdown-it parser.}
Summary:        Markdown URL utilities
Name:           python-mdurl
Version:        0.1.2
Release:        8%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/executablebooks/mdurl
Source0:        %{url}/archive/%{version}/mdurl-%{version}.tar.gz
BuildRequires:  python3-devel
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core
%if 0%{?with_check}
BuildRequires: python3-pytest
%endif
BuildArch:      noarch

%description %{_description}

%package -n     python3-mdurl
Summary:        %{summary}
Requires:       python3-flit-core

%description -n python3-mdurl %{_description}

%prep
%autosetup -p1 -n mdurl-%{version}

# Remove coverage from the test requirements
sed -i "s/pytest-cov//" tests/requirements.txt


%build
%{pyproject_wheel}


%install
%{pyproject_install}
%pyproject_save_files mdurl


%check
pip3 install iniconfig
%pytest


%files -n python3-mdurl -f %{pyproject_files}
%doc README.md
%license LICENSE

%changelog
* Mon May 13 2024 Sam Meluch <sammeluch@microsoft.com> - 0.1.2-8
- Add missing dep on pytest for check section

* Thu Mar 28 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.1.2-7
- Initial Azure Linux import from Fedora 40 (license: MIT)
- License verified

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 0.1.2-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Oct 13 2022 Karolina Surma <ksurma@redhat.com> - 0.1.2-1
- Update to 0.1.2
Resolves: rhbz#2118132

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 14 2022 Python Maint <python-maint@redhat.com> - 0.1.1-2
- Rebuilt for Python 3.11

* Tue Apr 19 2022 LumÃ­r Balhar <lbalhar@redhat.com> - 0.1.1-1
- Update to 0.1.1
Resolves: rhbz#2074703

* Mon Jan 31 2022 Karolina Surma <ksurma@redhat.com> - 0.1.0-1
- Initial package
