# Disable tests as it requires new package python-exceptiongroup
%global with_check 0
Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%undefine mariner_module_ldflags

%global pypi_name trove-classifiers
Name:           python-trove-classifiers
Version:        2024.2.23
Release:        1%{?dist}
Summary:        Canonical source for classifiers on PyPI (pypi.org)

License:        Apache-2.0
URL:            https://github.com/pypa/trove-classifiers
Source:         %{pypi_source trove-classifiers}

# [IMPORTANT] Update the patch for every new version
Patch:          001_remove_claver_dependency.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel
BuildRequires:  python3-packaging
BuildRequires:  python3-toml

%global _description %{expand:
Canonical source for classifiers on PyPI.
Classifiers categorize projects per PEP 301. Use this package to validate
classifiers in packages for PyPI upload or download.
}

%description %_description

%package -n python3-trove-classifiers
Summary:        %{summary}

%description -n python3-trove-classifiers %_description


%prep
%autosetup -p1 -n trove-classifiers-%{version}
# Replace @@VERSION@@ with %%version
#%writevars -f pyproject.toml version


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files trove_classifiers


%check
%if %{with_check}
%pytest
%endif


%files -n python3-trove-classifiers -f %{pyproject_files}
%doc README.*


%changelog
* Mon Feb 26 2024 Bala <balakumaran.kannan@microsoft.com> - 2024.2.23-1
- Initial Azure Linux import from Fedora 39 (license: MIT)
- Upgrade to latest version 2024.2.23
- Build using setup.py. So modify the patch to update version in setup.py
- License verified.

* Thu Oct 19 2023 Maxwell G <maxwell@gtmx.me> - 2023.10.18-1
- Update to 2023.10.18. Fixes rhbz#2244676.

* Wed Oct 4 2023 Maxwell G <maxwell@gtmx.me> - 2023.9.19-1
- Update to 2023.9.19. Fixes rhbz#2239555.

* Mon Aug 7 2023 Maxwell G <maxwell@gtmx.me> - 2023.8.7-1
- Update to 2023.8.7. Fixes rhbz#2229834.

* Thu Jul 27 2023 Maxwell G <maxwell@gtmx.me> - 2023.7.6-1
- Update to 2023.7.6. Fixes rhbz#2220945.

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2023.5.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2023.5.24-2
- Rebuilt for Python 3.12

* Wed Jun 7 2023 Maxwell G <maxwell@gtmx.me> - 2023.5.24-1
- Update to 2023.5.24. Fixes rhbz#2189711.

* Wed Apr 26 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 2023.4.25-1
- Update to 2023.4.25
Fixes: rhbz#2177081
Fixes: rhbz#2187710

* Tue Feb 21 2023 Tomáš Hrnčiar <thrnciar@redhat.com> - 2023.2.20-1
Initial package

