Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%undefine distro_module_ldflags

Name:           python-trove-classifiers
Version:        2024.3.3
Release:        1%{?dist}
Summary:        Canonical source for classifiers on PyPI (pypi.org)

License:        Apache-2.0
URL:            https://github.com/pypa/trove-classifiers
Source:         https://github.com/pypa/trove-classifiers/archive/refs/tags/2024.3.3.tar.gz#/trove-classifiers-%{version}.tar.gz


# Drop dependency on calver and use PEP 621 declarative metadata.
# This patch is rebased version of upstream PR:
# https://github.com/pypa/trove-classifiers/pull/126/commits/809156bb35852bcaa1c753e0165f1814f2bcedf6
Patch: Move-to-PEP-621-declarative-metadata.patch

BuildArch:      noarch
BuildRequires:  python3-devel
%if 0%{?with_check}
BuildRequires:  python3-pytest
#BuildRequires:  python3-iniconfig
%endif

BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-six
BuildRequires:  python3-wheel
BuildRequires:  python3-packaging

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
%writevars -f pyproject.toml version


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files trove_classifiers


%check
pip install iniconfig
%pytest


%files -n python3-trove-classifiers -f %{pyproject_files}
%doc README.*


%changelog
* Mon Mar 11 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 2024.3.3-1
- Update to 2024.3.3
- Drop dependency on calver and use PEP 621 declarative metadata as in original Fedora spec.
- Re-enable tests

* Fri Mar 01 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 2024.2.23-2
- Updating naming for 3.0 version of Azure Linux.

* Mon Feb 26 2024 Bala <balakumaran.kannan@microsoft.com> - 2024.2.23-1
- Initial CBL-Mariner import from Fedora 39 (license: MIT)
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
