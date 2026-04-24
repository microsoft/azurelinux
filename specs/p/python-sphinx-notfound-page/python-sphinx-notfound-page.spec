# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name sphinx-notfound-page
%global srcname sphinx_notfound_page
%global importname notfound
%global project_owner readthedocs
%global github_name sphinx-notfound-page
%global desc Create a custom 404 page with absolute URLs hardcoded

Name:           python-%{pypi_name}
Version:        1.0.4
Release: 7%{?dist}
Summary:        Create a custom 404 page with absolute URLs hardcoded

License:        MIT
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://github.com/%{project_owner}/%{github_name}/archive/%{version}.tar.gz
# Patch to remove . and no longer needed pdbpp from tox deps
# From https://github.com/readthedocs/sphinx-notfound-page/pull/225
Patch:         tox-no-dot-no-pdbpp.patch
# Already upstream patch to fix tests with sphinx 7.3.x
Patch:         https://patch-diff.githubusercontent.com/raw/readthedocs/sphinx-notfound-page/pull/245.patch
# Already upstream patch to fix tests with sphinx 8.x
Patch:         https://patch-diff.githubusercontent.com/raw/readthedocs/sphinx-notfound-page/pull/250.patch

BuildArch:      noarch

%description
%desc

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        %{summary}
BuildArch:      noarch

%description -n python%{python3_pkgversion}-%{pypi_name}
%desc


%prep
%autosetup -n %{pypi_name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files notfound

%check
%tox

%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%doc README.rst CHANGELOG.rst docs

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.4-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.4-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.4-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jan 04 2025 Kevin Fenzi <kevin@scrye.com> - 1.0.4-1
- Update to 1.0.4. Fixes rhbz#2330153

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.2-2
- Rebuilt for Python 3.13

* Sun Jun 02 2024 Miro Hrončok <mhroncok@redhat.com> - 1.0.2-1
- Update to 1.0.2
- Fixes: rhbz#2261607

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Oct 02 2023 Kevin Fenzi <kevin@scrye.com> - 1.0.0-1
- Update to 1.0.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 0.7.1-8
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Surma <ksurma@redhat.com> - 0.7.1-7
- Ensure compatibility with Sphinx 6+
Resolves: rhbz#2180484

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 0.7.1-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 15 2021 Karolina Surma <ksurma@redhat.com> - 0.7.1-1
- Update to new upstream version 0.7.1

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.6-5
- Rebuilt for Python 3.10

* Mon Mar  8 2021 Tim Landscheidt <tim@tim-landscheidt.de> - 0.6-4
- Remove obsolete requirements for %%post/%%postun scriptlets

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jan 19 2021 Charalampos Stratakis <cstratak@redhat.com> - 0.6-2
- Fix compatibility with Sphinx 3.4

* Tue Jan 12 2021 Charalampos Stratakis <cstratak@redhat.com> - 0.6-1
- Update to version 0.6

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.4-8
- Rebuilt for Python 3.9

* Tue Apr 21 2020 Charalampos Stratakis <cstratak@redhat.com> - 0.4-7
- Fix test failures with Sphinx 3 (rhbz#1823521)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.4-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 13 2019 Kevin Fenzi <kevin@scrye.com> - 0.4-2
- Use bcond for python2 support.

* Wed Jul 03 2019 Kevin Fenzi <kevin@scrye.com> - 0.4-1
- Initial version for Fedora.
