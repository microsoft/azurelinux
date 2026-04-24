# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global desc This tool provides code to load WSGI applications and servers from\
URIs; these URIs can refer to Python Eggs for INI-style configuration\
files.  PasteScript provides commands to serve applications based on\
this configuration file.
%global sum Load, configure, and compose WSGI applications and servers
%global srcname PasteDeploy

Name:           python-paste-deploy
Version:        3.1.0
Release: 13%{?dist}
Summary:        %{sum}
License:        MIT
URL:            https://github.com/Pylons/pastedeploy
Source0:        %pypi_source
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-pytest
#BuildRequires:  python3-pytest-cov
BuildRequires:  python3-paste-script

%description
%{desc}


%package -n python3-paste-deploy
Summary:        %{sum}

#Requires:       python3-paste
Requires:       python3-setuptools



%description -n python3-paste-deploy
%desc



%prep
%setup -q -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires -t


%build
%pyproject_wheel
# disable coverage tests
sed -i 's/ --cov//' pytest.ini


%install
%pyproject_install
%pyproject_save_files paste
rm -rf %{buildroot}%{python3_sitelib}/test


%check
%pyproject_check_import
%pytest


%files -n python3-paste-deploy -f %{pyproject_files}
%license license.txt
%{python3_sitelib}/PasteDeploy-%{version}-py*-nspkg.pth


%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.1.0-12
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.1.0-11
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 09 2025 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.1.0-9
- Migrate from py_build/py_install to pyproject macros (bz#2377975)

* Mon Jun 02 2025 Python Maint <python-maint@redhat.com> - 3.1.0-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.1.0-6
- Coverage tests should not be run in Fedora/EPEL

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 3.1.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.1.0-1
- Update to upstream.

* Sat Nov 04 2023 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 3.0.1-4
- Remove dependency on python-paste (upstream not actively maintained)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 3.0.1-2
- Rebuilt for Python 3.12

* Sun Feb 19 2023 Kevin Fenzi <kevin@scrye.com> - 3.0.1-1
- Update to 3.0.1. Fixes rhbz#2135186

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 18 2023 Ján ONDREJ (SAL) <ondrejj(at)salstar.sk> - 2.1.1-8
- Do not use glob on python sitelib

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.1.1-6
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 03 2021 Python Maint <python-maint@redhat.com> - 2.1.1-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Nov 23 2020 Joel Capitao <jcapitao@redhat.com> - 2.1.1-1
- Update to 2.1.1 (#1887554)

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat May 23 2020 Miro Hrončok <mhroncok@redhat.com> - 2.1.0-2
- Rebuilt for Python 3.9

* Wed Feb 19 2020 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0 (#1797302).
- https://docs.pylonsproject.org/projects/pastedeploy/en/latest/news.html

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Sep 09 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-4
- Subpackage python2-paste-deploy has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Fri Aug 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2.0.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jun 05 2019 Randy Barlow <bowlofeggs@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jul 16 2018 Dan Callaghan <dcallagh@redhat.com> - 1.5.2-17
- invoke Python 2 explicitly, use modern Python RPM macros

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 1.5.2-15
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.5.2-14
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild
