# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name jmespath

Name:           python-%{pypi_name}
Version:        1.0.1
Release: 14%{?dist}
Summary:        JSON Matching Expressions

License:        MIT
URL:            https://github.com/jmespath/jmespath.py
Source0:        %{url}/archive/%{version}/jmespath.py-%{version}.tar.gz
BuildArch:      noarch

%description
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

%package -n     python3-%{pypi_name}
Summary:        JSON Matching Expressions
%{?python_provide:%python_provide python3-%{pypi_name}}
%{?python_provide:%python_provide python-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

BuildRequires:  python3-pytest
%if %{undefined rhel}
BuildRequires:  python3-hypothesis
%endif

Obsoletes: python2-jmespath < 0.9.4-2

%description -n python3-%{pypi_name}
JMESPath allows you to declaratively specify how to extract elements from
a JSON document.

%prep
%setup -q -n jmespath.py-%{version}
rm -rf %{pypi_name}.egg-info

%build
%py3_build

%install
%py3_install

%check
# RHEL does not have python3-hypothesis. Only one file in the upstream repo
# depends on hypothesis, so we can omit this dependency for RHEL.
%pytest %{?rhel:--ignore=extra/test_hypothesis.py}

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE.txt
%{_bindir}/jp.py
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.0.1-13
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.0.1-12
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.0.1-10
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.0.1-7
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.0.1-3
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Nov 12 2022 Kevin Fenzi <kevin@scrye.com> - 1.0.1-1
- Update to 1.0.1. Fixes rhbz#2098349

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.0.0-4
- Rebuilt for Python 3.11

* Tue May 03 2022 Major Hayden <major@mhtx.net> - 1.0.0-3
- Remove python3-nose from BuildRequires and skip single test file that requires nose.

* Wed Apr 06 2022 Kevin Fenzi <kevin@scrye.com> - 1.0.0-2
- Rebuild to deal with update snafu.

* Tue Mar 22 2022 Kevin Fenzi <kevin@scrye.com> - 1.0.0-1
- Update to 1.0.0. Fixes rhbz#2064951

* Tue Mar 15 2022 Tomáš Hrnčiar <thrnciar@redhat.com> - 0.10.0-6
- Use list for random.sample since using a set has been removed in Python 3.11
- Fixes: rhbz#2057520

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 29 2021 Miro Hrončok <mhroncok@redhat.com> - 0.10.0-3
- Actually run the tests in %%check

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.10.0-2
- Rebuilt for Python 3.10

* Sat Apr 3 2021 Eduardo Echeverria <echevemaster@gmail.com> - 0.10.0-1
- Bumped to the last version

* Wed Mar  3 2021 Pavel Cahyna <pcahyna@redhat.com> - 0.9.4-8
- Remove unused python-mock build dependency

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun May 24 2020 Miro Hrončok <mhroncok@redhat.com> - 0.9.4-5
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Sep  4 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 0.9.4-3
- Obsolete python2 subpackage to fix upgrade path (#1734184)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.9.4-2
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Kevin Fenzi <kevin@scrye.com> - 0.9.4-1
- Upgrade to 0.9.4.
- Drop python2 subpackage and fix unversioned command to use python3.

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Sep 08 2018 Kevin Fenzi <kevin@scrye.com> - 0.9.3-1
- Upgrade to 0.9.3. Fixes bug #1588131

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-11
- Rebuilt for Python 3.7

* Mon Feb 12 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.9.0-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.9.0-6
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-5
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Jun 27 2016 Haïkel Guémar <hguemar@fedoraproject.org> - 0.9.0-4
- Fix python2 subpackage requiring python3 (RHBZ#1342501)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 06 2016 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9.0-2
- Improve to set the Provides tag for EL6 too

* Tue Dec 29 2015 Fabio Alessandro Locati <fale@fedoraproject.org> - 0.9.0-1
- Upgrade to upstream current version
- Improve the spec file
- Make possible to build in EL6

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.5.0-1
- New version

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.4.1-1
- Initial packaging
