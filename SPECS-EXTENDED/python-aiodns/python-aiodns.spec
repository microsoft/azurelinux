# All tests require network access (DNS). We can run them manually with, e.g.:
#   fedpkg mockbuild --with network_tests --enable-network
%bcond_with network_tests

Name:           python-aiodns
Version:        3.2.0
Release:        1%{?dist}
Summary:        Simple DNS resolver for asyncio

License:        MIT
URL:            https://github.com/saghul/aiodns
Source0:        %{url}/archive/v%{version}/aiodns-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
%if %{with network_tests}
BuildRequires:  %{py3_dist pytest}
# Optional uvloop integration tests:
BuildRequires:  %{py3_dist uvloop}
%endif

%global _description %{expand:
aiodns provides a simple way for doing asynchronous DNS resolutions using
pycares.}

%description %{_description}


%package     -n python3-aiodns
Summary:        %{summary}

%description -n python3-aiodns %{_description}


%prep
%autosetup -n aiodns-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l aiodns


%check
%pyproject_check_import
%if %{with network_tests}
%pytest tests.py
%endif


%files -n python3-aiodns -f %{pyproject_files}
%doc README.rst ChangeLog


%changelog
* Sat Aug 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.2.0-1
- Update to 3.2.0 (close RHBZ#2242855)

* Sat Aug 17 2024 Benjamin A. Beasley <code@musicinmybrain.net> - 3.0.0-13
- Port to current Python guidelines (pyproject-rpm-macros)

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.0.0-11
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 14 2023 Python Maint <python-maint@redhat.com> - 3.0.0-7
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 3.0.0-4
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jun 9 2021 Matthieu Saulnier <fantom@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0
- Remove Patch0 (Backport from upstream commit: 28111210)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.0.0-9
- Rebuilt for Python 3.10

* Sun Feb 14 2021 Matthieu Saulnier <fantom@fedoraproject.org> - 2.0.0-8
- Replace glob with %%{python3_version} in %%files section

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 13 2021 Matthieu Saulnier <fantom@fedoraproject.org> - 2.0.0-6
- Add Patch0 to fix epel8 installation package
  Backport from upstream commit: 28111210

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.0-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Sun Aug 25 2019 Matthieu Saulnier <fantom@fedoraproject.org> - 2.0.0-1
- Bump version to 2.0.0

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Oct 17 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.1-5
- Subpackage python2-aiodns has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.1-3
- Rebuilt for Python 3.7

* Wed Apr 18 2018 Iryna Shcherbina <shcherbina.iryna@gmail.com> - 1.1.1-2
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Wed Apr  4 2018 Matthieu Saulnier <fantom@fedoraproject.org> - 1.1.1-1
- Initial package
