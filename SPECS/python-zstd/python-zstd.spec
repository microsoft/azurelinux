# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name zstd

Name:           python-%{pypi_name}
Version:        1.5.7.2
# see also:
# grep "^VERSION = " zstd-*/setup.py
%global zstd_version %(echo %{version} | cut -d. -f1,2,3 --output-delimiter .)

Release:        4%{?dist}
Summary:        Zstd Bindings for Python

# original zstd bits are GPL-2.0-or-later OR BSD-2-Clause
License:        BSD-2-Clause AND (GPL-2.0-or-later OR BSD-2-Clause)
URL:            https://github.com/sergey-dryabzhinsky/python-zstd
Source:         %{pypi_source}

# Patches to fix test execution
Patch:          python-zstd-1.5.5.1-test-external.patch

BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  python3dist(setuptools)
BuildRequires:  pkgconfig(libzstd) >= %{zstd_version}

%description
Simple Python bindings for the Zstd compression library.

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
# The library does not do symbol versioning to fully match automatically on
Requires:       libzstd%{?_isa} >= %{zstd_version}

%description -n python3-%{pypi_name}
Simple Python bindings for the Zstd compression library.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf src/%{pypi_name}.egg-info
# Remove precompiled files
find . -name '*.pyc' -delete
# Remove bundled zstd library
rm -rf zstd/
# do not test the version matching, we don't really need exact version of
# zstd here
rm tests/test_version.py
sed -i -e '/tests\.test_version/d' setup.py
sed -i -e '/test_version/d' tests/__init__.py

%build
%py3_build -- --legacy --external

%install
%py3_install

%check
%{py3_test_envvars} %{python3} -m unittest -v

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{python3_sitearch}/%{pypi_name}-%{version}-py%{python3_version}.egg-info
%{python3_sitearch}/%{pypi_name}*.so

%changelog
* Sat Jan 17 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Fri Dec 05 2025 Michel Lind <salimma@fedoraproject.org> - 1.5.7.2-1
- Update to version 1.5.7.2
- Resolves: rhbz#2363254

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 1.5.6.7-2
- Rebuilt for Python 3.14

* Mon Apr 07 2025 Michel Lind <salimma@fedoraproject.org> - 1.5.6.7-1
- Update to 1.5.6.7; Fixes: RHBZ#2339003

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 03 2025 Jonathan Wright <jonathan@almalinux.org> - 1.5.6.1-1
- update to 1.5.6.1 rhbz#2335057

* Thu Nov 07 2024 Michel Lind <salimma@fedoraproject.org> - 1.5.5.1-6
- Switch test runner to unittest for setuptools 74+ compatibility
- Resolves: rhbz#2319745

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.5.5.1-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Michel Lind <salimma@fedoraproject.org> - 1.5.5.1-1
- Update to 1.5.5.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 1.4.5.1-11
- Rebuilt for Python 3.12

* Wed Feb 01 2023 Nikita Popov <npopov@redhat.com> - 1.4.5.1-10
- Port to C99

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.4.5.1-7
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.4.5.1-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Sep 21 2020 Joel Capitao <jcapitao@redhat.com> - 1.4.5.1-2
- Edit macro for CentOS interoperability

* Sun Aug 23 2020 Neal Gompa <ngompa13@gmail.com> - 1.4.5.1-1
- Initial package (#1870571)
