Name:           python-editables
Version:        0.5
Release:        7%{?dist}
Summary:        Editable installations
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
License:        MIT
URL:            https://github.com/pfmoore/editables
Source:         %{url}/archive/%{version}/editables-%{version}.tar.gz
BuildRequires:  python3-devel
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-pip
BuildRequires:  python3-flit-core
%endif
BuildArch:      noarch

%global common_description %{expand:
A Python library for creating “editable wheels”

This library supports the building of wheels which, when installed, will expose
packages in a local directory on sys.path in “editable mode”. In other words,
changes to the package source will be reflected in the package visible to
Python, without needing a reinstall.}

%description %{common_description}


%package -n python3-editables
Summary:        %{summary}

%description -n python3-editables %{common_description}


%prep
%autosetup -n editables-%{version}

%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files editables


%check
pip3 install iniconfig
%pytest


%files -n python3-editables -f %{pyproject_files}
%license LICENSE.txt


%changelog
* Wed May 08 2024 Sam Meluch <sammeluch@microsoft.com> - 0.5-7
- Add missing dependency for %check section

* Fri Mar 29 2024 Riken Maharjan <rmaharjan@microsoft.com> - 0.5-6
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License Verified.

* Fri Mar 29 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5-5
- F41+: For simplicity, drop the -doc subpackage and PDF documentation

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jul 25 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.5-1
- Update to 0.5 (close RHBZ#2225249)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jul 08 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4-3
- When we don’t build PDF docs, don’t build a -doc subpacakge at all

* Fri Jul 07 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 0.4-2
- Disable docs by default in RHEL builds

* Thu Jul 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.4-1
- Update to 0.4 (close RHBZ#2220948)
- Upstream switched from setuptools to flit_core: pyproject-rpm-macros no
  longer handles LICENSE.txt

* Thu Jul 06 2023 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3-8
- Add a -doc subpackage with PDF documentations

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.3-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Oct 22 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3-4
- Confirm License is SPDX MIT

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.3-2
- Rebuilt for Python 3.11

* Mon Apr 11 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 0.3-1
- Update to 0.3 (close RHBZ#2073823)

