# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%global pypi_name zopfli

Name:           python-zopfli
Version:        0.2.3
Release:        10%{?dist}
Summary:        Zopfli module for python
License:        Apache-2.0
URL:            https://github.com/obp/py-zopfli
Source0:        %{pypi_source %{pypi_name} %{version} zip}

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  zopfli-devel

%description
cPython bindings for zopfli.

%package -n python3-%{pypi_name}
Summary:        %{summary}

%description -n python3-%{pypi_name}
cPython bindings for zopfli.

%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# remove vendored zopfli
rm -rf zopfli

%generate_buildrequires
%pyproject_buildrequires -r -x test


%build
export USE_SYSTEM_ZOPFLI=1
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files zopfli

%check
export PYTHONPATH="${PYTHONPATH:-%{buildroot}%{python3_sitearch}}"
%{python3} tests/test_zopfli.py

%files -n  python3-%{pypi_name} -f %{pyproject_files}
%license COPYING
%doc README.rst

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.2.3-10
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.2.3-9
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 0.2.3-7
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 0.2.3-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 12 2023 Parag Nemade <pnemade AT redhat DOT com> - 0.2.3-1
- Update to 0.2.3 version (#2238032)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 0.2.2-4
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Nov 22 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.2.2-2
- Update license to SPDX expression

* Tue Nov 22 2022 Parag Nemade <pnemade AT redhat DOT com> - 0.2.2-1
- Update to 0.2.2 version (#2143025)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.2.1-2
- Rebuilt for Python 3.11

* Thu Mar 03 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.2.1-1
- update to 0.2.1

* Wed Mar 02 2022 Felix Schwarz <fschwarz@fedoraproject.org> - 0.2.0-1
- update to 0.2.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Nov 17 2021 Parag Nemade <pnemade@fedoraproject.org> - 0.1.9-1
- Update to 0.1.9 release

* Wed Aug 04 2021 Felix Schwarz <fschwarz@fedoraproject.org> 0.1.8-1
- initial package

