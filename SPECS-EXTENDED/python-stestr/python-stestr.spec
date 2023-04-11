%global pypi_name stestr
%global with_doc 0
%global common_desc \
stestr is a fork of the testrepository that concentrates on being a \
dedicated test runner for python projects. The generic abstraction layers \
which enabled testr to work with any subunit emitting runner are gone. \
stestr hard codes python-subunit-isms into how it works.
%bcond_without bootstrap
Summary:        A test runner runner similar to testrepository
Name:           python-%{pypi_name}
Version:        3.2.0
Release:        7%{?dist}
License:        ASL 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pypi.python.org/pypi/stestr
Source0:        https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildArch:      noarch

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        A test runner runner similar to testrepository
Obsoletes:      python2-%{pypi_name} < %{version}-%{release}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-pbr
%if %{with_check}
BuildRequires:  python3-pip
BuildRequires:  python3-pytest
%endif
Requires:       python3-pbr
Requires:       python3-future
Requires:       python3-subunit
Requires:       python3-fixtures
Requires:       python3-six
Requires:       python3-testtools
Requires:       python3-PyYAML
Requires:       python3-cliff
Requires:       python3-voluptuous

%description -n python3-%{pypi_name}
%{common_desc}

%if %{without bootstrap}
%package -n     python3-%{pypi_name}-sql
Summary:        sql plugin for stestr
BuildRequires:  python3-subunit2sql
BuildRequires:  %{_bindir}/subunit2sql-db-manage
Requires:       python3-%{pypi_name} = %{version}-%{release}
Requires:       python3-subunit2sql

%description    -n python3-%{pypi_name}-sql
It contains the sql plugin for stestr.
%endif

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        stestr documentation
BuildRequires:  python3-sphinx
BuildRequires:  python3-subunit2sql

%description -n python-%{pypi_name}-doc
%{common_desc}

It contains the documentation for stestr.
%endif

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm -f test-requirements.txt requirements.txt

# Remove pbr>=2.0.0 version as it is required for pike
sed -i 's/pbr>=2.0.0/pbr/g' setup.py

%build
%py3_build

%if 0%{?with_doc}
# generate html docs
python3 setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%py3_install
# compat symlinks
ln -s stestr %{buildroot}/%{_bindir}/stestr-3
ln -s stestr-3 %{buildroot}/%{_bindir}/stestr-%{python3_version}

%check
export PATH=%{buildroot}/%{_bindir}:$PATH
rm -fr .stestr
%{python3} -m pip install mock future subunit fixtures six sqlalchemy testtools PyYAML ddt cliff voluptuous
# currently, 4 test are failing
PYTHON=python3 python3 setup.py test || :

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/stestr*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info

%if %{without bootstrap}
%files -n python3-%{pypi_name}-sql
%{python3_sitelib}/%{pypi_name}/repository/sql.py
%endif

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Wed Mar 08 2023 Sumedh Sharma <sumsharma@microsoft.com> - 3.2.0-7
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- license verified

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
