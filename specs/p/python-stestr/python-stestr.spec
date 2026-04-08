# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global pypi_name stestr
# Enable bootstrap
%bcond_without bootstrap
%global with_doc 0

%global common_desc \
stestr is a fork of the testrepository that concentrates on being a \
dedicated test runner for python projects. The generic abstraction layers \
which enabled testr to work with any subunit emitting runner are gone. \
stestr hard codes python-subunit-isms into how it works.

Name:       python-%{pypi_name}
Version:    4.1.0
Release:    11%{?dist}
Summary:    A test runner runner similar to testrepository

# Automatically converted from old format: ASL 2.0 - review is highly recommended.
License:    Apache-2.0
URL:        https://pypi.python.org/pypi/stestr
Source0:    %pypi_source
BuildArch:  noarch


%description
%{common_desc}

%package -n     python%{python3_pkgversion}-%{pypi_name}
Summary:        A test runner runner similar to testrepository
%{?python_provide:%python_provide python%{python3_pkgversion}-%{pypi_name}}

BuildRequires:    python%{python3_pkgversion}-devel
BuildRequires:    git-core

Requires:   python%{python3_pkgversion}-pbr
Requires:   python%{python3_pkgversion}-subunit >= 1.4.0
Requires:   python%{python3_pkgversion}-fixtures >= 3.0.0
Requires:   python%{python3_pkgversion}-testtools >= 2.2.0
Requires:   python%{python3_pkgversion}-PyYAML >= 3.10.0
Requires:   python%{python3_pkgversion}-cliff >= 2.8.0
Requires:   python%{python3_pkgversion}-voluptuous >= 0.8.9

%description -n python%{python3_pkgversion}-%{pypi_name}
%{common_desc}

%if %{without bootstrap}
%package -n     python%{python3_pkgversion}-%{pypi_name}-sql
Summary:        sql plugin for stestr

BuildRequires:  /usr/bin/subunit2sql-db-manage
Requires:       python%{python3_pkgversion}-%{pypi_name} = %{version}-%{release}
Requires:       python%{python3_pkgversion}-subunit2sql

%description    -n python%{python3_pkgversion}-%{pypi_name}-sql
It contains the sql plugin for stestr.
%endif

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        stestr documentation

%description -n python-%{pypi_name}-doc
%{common_desc}

It contains the documentation for stestr.
%endif

%generate_buildrequires
%pyproject_buildrequires -t %{!?with_bootstrap:-x sql}

%prep
%autosetup -n %{pypi_name}-%{version} -S git
sed -i '/doc8.*/d' test-requirements.txt
sed -i '/hacking.*/d' test-requirements.txt
sed -i '/black.*/d' test-requirements.txt
# Replace removed SafeConfigParser with ConfigParser
# Upstream: https://github.com/mtreinish/stestr/pull/344
sed -i 's/SafeConfigParser/ConfigParser/' stestr/commands/run.py

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
PYTHONPATH=%{pyproject_build_lib} sphinx-build doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install
%pyproject_save_files %{pypi_name}
# compat symlinks
ln -s stestr %{buildroot}/%{_bindir}/stestr-3
ln -s stestr-3 %{buildroot}/%{_bindir}/stestr-%{python3_version}

%check
%tox

%files -n python%{python3_pkgversion}-%{pypi_name} -f %{pyproject_files}
%license LICENSE
%{_bindir}/stestr*

%if %{without bootstrap}
%files -n python%{python3_pkgversion}-%{pypi_name}-sql
%{python3_sitelib}/%{pypi_name}/repository/sql.py
%endif

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc README.rst
%doc doc/build/html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.1.0-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.1.0-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 4.1.0-8
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 24 2024 Miroslav Suchý <msuchy@redhat.com> - 4.1.0-6
- convert license to SPDX

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 4.1.0-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Sep 19 2023 Lumír Balhar <lbalhar@redhat.com> - 4.1.0-1
- Update to 4.1.0 (rhbz#2239471)

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 4.0.1-2
- Rebuilt for Python 3.12

* Wed Feb 08 2023 Joel Capitao <jcapitao@redhat.com> - 4.0.1-1
- Update to latest upstream (#1482280)

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 3.2.0-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 05 2021 Miro Hrončok <mhroncok@redhat.com> - 3.2.0-2
- Reintroduce the Dist Tag (e.g. fc35) to the release value

* Mon Jun 28 2021 Joel Capitao <jcapitao@redhat.com> - 3.2.0-1
- Update to 3.2.0 (#1480520)

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.6.0-9
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-6
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Dec 17 2019 Chandan Kumar <raukadah@gmail.com> - 2.6.0-1
- Bumped to version 2.6.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.4.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Chandan Kumar <chkumar246@gmail.com> - 2.4.0-1
- Update to 2.4.0
- Removed patch "Discover python executable when discover is not used"

* Fri Jun 07 2019 Alfredo Moralejo <amoralej@redhat.com> - 2.3.1-1
- Update to 2.3.1
- Included patch "Discover python executable when discover is not used"

* Thu Feb 14 2019 Yatin Karel <ykarel@redhat.com> - 2.2.0-1
- Update to 2.2.0 and Enable py2 build for CentOS <= 7

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Oct 12 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.1.0-2
- Python2 binary package has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Jul 30 2018 Chandan Kumar <chkumar246@gmail.com> - 2.1.0-1
- Bump to version 2.1.0
- Synced requirements for newer version
- Closes-Bug RHBZ#1480520

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-4
- Rebuilt for Python 3.7

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.0-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 17 2017 Chandan Kumar <chkumar246@gmail.com> - 1.1.0-1
- Update the spec to 1.1.0
- Enable tests
- Moved python2-subunit2sql under docs

* Fri Sep 15 2017 Chandan Kumar <chkumar246@gmail.com> - 1.0.0-4
- Disable tests

* Fri Sep 15 2017 Chandan Kumar <chkumar246@gmail.com> - 1.0.0-3
- Fixed test requirements and enabled subunit2sql

* Fri Sep 15 2017 Chandan Kumar <chkumar246@gmail.com> - 1.0.0-2
- Disable subunit2sql

* Fri Sep 15 2017 Chandan Kumar <chkumar246@gmail.com> - 1.0.0-1
- Bumped to 1.0.0

* Thu Aug 10 2017 Chandan Kumar <chkumar246@gmail.com> - 0.5.0-4
- Added -sql subpackage

* Tue Aug 01 2017 Chandan Kumar <chkumar246@gmail.com> - 0.5.0-3
- Use sed to remove pbr>=2.0.0 dependency

* Tue Aug 01 2017 Chandan Kumar <chkumar246@gmail.com> - 0.5.0-2
- Fixed rpmlint errors

* Mon Jul 31 2017 Chandan Kumar <chkumar246@gmail.com> - 0.5.0-1
- Initial package.
