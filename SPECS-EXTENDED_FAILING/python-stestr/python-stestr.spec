Vendor:         Microsoft Corporation
Distribution:   Mariner
%global pypi_name stestr

# Note(hguemar): PyYAML provide is scheduled to be removed
%{?el7: %global pyyaml_pkg PyYAML}
%{!?el7: %global pyyaml_pkg python2-pyyaml}

%bcond_with    python2
%bcond_without python3

%global with_doc 0

%global common_desc \
stestr is a fork of the testrepository that concentrates on being a \
dedicated test runner for python projects. The generic abstraction layers \
which enabled testr to work with any subunit emitting runner are gone. \
stestr hard codes python-subunit-isms into how it works.

Name:   python-%{pypi_name}
Version:    2.6.0
Release:    6%{?dist}
Summary:    A test runner runner similar to testrepository

License:    ASL 2.0
URL:    https://pypi.python.org/pypi/stestr
Source0:    https://files.pythonhosted.org/packages/source/s/%{pypi_name}/%{pypi_name}-%{version}.tar.gz#/python-%{pypi_name}-%{version}.tar.gz
BuildArch:  noarch

BuildRequires:    git

%description
%{common_desc}

%if %{with python2}
%package -n    python2-%{pypi_name}
Summary:    A test runner runner similar to testrepository
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:    python2-devel
BuildRequires:    python2-setuptools
BuildRequires:    python2-pbr

# Test Requirements
BuildRequires:   python2-mock
BuildRequires:   python2-future
BuildRequires:   python2-subunit
BuildRequires:   python2-fixtures
BuildRequires:   python2-six
BuildRequires:   python2-testtools
BuildRequires:   %{pyyaml_pkg}
BuildRequires:   python2-ddt
BuildRequires:   python2-cliff
BuildRequires:   python2-voluptuous

Requires:   python2-pbr
Requires:   python2-future
Requires:   python2-subunit
Requires:   python2-fixtures
Requires:   python2-six
Requires:   python2-testtools
Requires:   %{pyyaml_pkg}
Requires:   python2-cliff
Requires:   python2-voluptuous

%description -n python2-%{pypi_name}
%{common_desc}

%package -n     python2-%{pypi_name}-sql
Summary:    sql plugin for stestr

Requires:       python2-%{pypi_name} = %{version}-%{release}
Requires:       python2-subunit2sql

%description    -n python2-%{pypi_name}-sql
It contains the sql plugin for stestr.
%endif

%if %{with python3}
%package -n     python3-%{pypi_name}
Summary:        A test runner runner similar to testrepository
Obsoletes:      python2-%{pypi_name} < %{version}-%{release}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:    python3-devel
BuildRequires:    python3-setuptools
BuildRequires:    python3-pbr

# Test Requirements
BuildRequires:   python3-mock
BuildRequires:   python3-future
BuildRequires:   python3-subunit
BuildRequires:   python3-fixtures
BuildRequires:   python3-six
BuildRequires:   python3-sqlalchemy
BuildRequires:   python3-testtools
BuildRequires:   python3-PyYAML
BuildRequires:   python3-ddt
BuildRequires:   python3-cliff
BuildRequires:   python3-voluptuous

Requires:   python3-pbr
Requires:   python3-future
Requires:   python3-subunit
Requires:   python3-fixtures
Requires:   python3-six
Requires:   python3-testtools
Requires:   python3-PyYAML
Requires:   python3-cliff
Requires:   python3-voluptuous

%description -n python3-%{pypi_name}
%{common_desc}
%endif

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        stestr documentation

%if %{with python2}
BuildRequires:  python2-sphinx
BuildRequires:  python2-subunit2sql
%endif
%if %{with python3}
BuildRequires:  python3-sphinx
BuildRequires:  python3-subunit2sql
%endif

%description -n python-%{pypi_name}-doc
%{common_desc}

It contains the documentation for stestr.
%endif

%prep
%autosetup -n %{pypi_name}-%{version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
rm -f test-requirements.txt requirements.txt

# Remove pbr>=2.0.0 version as it is required for pike
sed -i 's/pbr>=2.0.0/pbr/g' setup.py

%build
%if %{with python2}
%py2_build
%endif

%if %{with python3}
%py3_build
%endif

%if 0%{?with_doc}
# generate html docs
%if %{with python2}
%{__python2} setup.py build_sphinx
%endif
%if %{with python3}
%{__python3} setup.py build_sphinx
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
%endif

%install
%if %{with python3}
%py3_install
# compat symlinks
ln -s stestr %{buildroot}/%{_bindir}/stestr-3
ln -s stestr-3 %{buildroot}/%{_bindir}/stestr-%{python3_version}
%endif

%if %{with python2}
%py2_install
cp %{buildroot}/%{_bindir}/stestr %{buildroot}/%{_bindir}/stestr-2
ln -sf %{_bindir}/stestr-2 %{buildroot}/%{_bindir}/stestr-%{python2_version}
%endif


%check
export PATH=%{buildroot}/%{_bindir}:$PATH
%if %{with python2}
# currently, 3 test are failing
%{__python2} setup.py test || :
%endif
%if %{with python3}
rm -fr .stestr
# currently, 4 test are failing
PYTHON=%{__python3} %{__python3} setup.py test || :
%endif

%if %{with python2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/stestr*
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info

%files -n python2-%{pypi_name}-sql
%{python2_sitelib}/%{pypi_name}/repository/sql.py
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/stestr*
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Thu Apr 29 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.6.0-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing unbuildable subpackage "python3-stestr-sql".

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
