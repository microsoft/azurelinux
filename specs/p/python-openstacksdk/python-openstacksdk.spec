# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.


%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order statsd
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

# Disable docs until bs4 package is available
%global with_doc 0

%global pypi_name openstacksdk

%global common_desc \
A collection of libraries for building applications to work with OpenStack \
clouds.

%global common_desc_tests \
A collection of libraries for building applications to work with OpenStack \
clouds - test files

Name:           python-%{pypi_name}
Version:        4.0.0
Release:        6%{?dist}
Summary:        An SDK for building applications to work with OpenStack

License:        Apache-2.0
URL:            http://www.openstack.org/
Source0:        https://pypi.io/packages/source/o/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
BuildArch:      noarch

BuildRequires:  git-core

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:        An SDK for building applications to work with OpenStack

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
%description -n python3-%{pypi_name}
%{common_desc}

%package -n python3-%{pypi_name}-tests
Summary:        An SDK for building applications to work with OpenStack - test files

Requires: python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc_tests}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        An SDK for building applications to work with OpenStack - documentation
%description -n python-%{pypi_name}-doc
A collection of libraries for building applications to work with OpenStack
clouds - documentation.
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# This unit test requires python-prometheus, which is optional and not needed
rm -f openstack/tests/unit/test_stats.py

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
rm -f ./openstack/tests/unit/test_hacking.py
%tox -e %{default_toxenv} -- -- --exclude-regex '(openstack.tests.unit.test_connection.TestConnection.test_create_unknown_proxy|openstack.tests.unit.test_missing_version.TestMissingVersion.test_unsupported_version_override)'

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/openstack-inventory
%{python3_sitelib}/openstack
%{python3_sitelib}/%{pypi_name}-*.dist-info
%exclude %{python3_sitelib}/openstack/tests

%files -n python3-%{pypi_name}-tests
%{python3_sitelib}/openstack/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 4.0.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Joel Capitao <jcapitao@redhat.com> 4.0.0-1
- Update to upstream version 4.0.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Python Maint <python-maint@redhat.com> - 3.0.0-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 3.0.0-1
- Update to upstream version 3.0.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Alfredo Moralejo <amoralej@gmail.com> 1.5.0-1
- Update to upstream version 1.5.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Joel Capitao <jcapitao@redhat.com> - 1.0.1-3
- Skip unit test which depends on keystoneauth1

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 1.0.1-2
- Rebuilt for Python 3.12

* Fri Apr 21 2023 Karolina Kula <kkula@redhat.com> 1.0.1-1
- Update to upstream version 1.0.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.101.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 0.101.0-1
- Update to upstream version 0.101.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.61.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Alfredo Moralejo <amoralej@redhat.com> - 0.61.0-3
- Replace deprecated inspect.getargspec call

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 0.61.0-2
- Rebuilt for Python 3.11

* Mon May 23 2022 Joel Capitao <jcapitao@redhat.com> 0.61.0-1
- Update to upstream version 0.61.0

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 0.61.0-1
- Update to upstream version 0.61.0

* Wed Apr 06 2022 Karolina Kula <kkula@redhat.com> - 0.55.1-1
- Update to upstream version 0.55.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.55.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.55.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jun 17 2021 Javier Peña <jpena@redhat.com> - 0.55.0-3
- Fix auto_spec arguments passed to mock
- Skip unit tests related to dogpile.cache

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 0.55.0-2
- Rebuilt for Python 3.10

* Wed Mar 17 2021 Joel Capitao <jcapitao@redhat.com> 0.55.0-1
- Update to upstream version 0.55.0

* Mon Feb 08 2021 Javier Peña <jpena@redhat.comg> - 0.50.0-3
- Fix build on Python 3.10 (bz#1926361)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.50.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Sep 25 2020 RDO <dev@lists.rdoproject.org> 0.50.0-1
- Update to 0.50.0

* Fri Sep 18 2020 RDO <dev@lists.rdoproject.org> 0.49.0-1
- Update to 0.49.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.46.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 0.46.0-1
- Update to upstream version 0.46.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 0.36.0-5
- Rebuilt for Python 3.9

* Wed Mar 04 2020 Javier Peña <jpena@redhat.com> - 0.36.0-4
- Add patch to replace assertItemsEqual with assertCountEqual (bz#1809970)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.36.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Alfredo Moralejo <amoralej@redhat.com> 0.36.0-2
- Update to upstream version 0.36.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.27.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.27.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.27.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 05 2019 RDO <dev@lists.rdoproject.org> 0.27.0-1
- Update to 0.27.0

* Tue Mar 12 2019 RDO <dev@lists.rdoproject.org> 0.26.0-1
- Update to 0.26.0

* Mon Mar 11 2019 RDO <dev@lists.rdoproject.org> 0.25.0-1
- Update to 0.25.0
