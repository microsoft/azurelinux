# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318
%global pypi_name oslotest

%bcond repo_bootstrap 0

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

%if %{without repo_bootstrap}
%global with_doc 1
%else
%global with_doc 0
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme oslo.config
%endif

%global common_desc OpenStack test framework and test fixtures.

Name:           python-%{pypi_name}
Version:        5.0.0
Release: 12%{?dist}
Summary:        OpenStack test framework

License:        Apache-2.0
URL:            http://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:  git-core

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:        OpenStack test framework

BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros


%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for the OpenStack test framework

%description -n python-%{pypi_name}-doc
%{common_desc} Documentation
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
%generate_buildrequires
%if %{without repo_bootstrap}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires
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
%if %{without repo_bootstrap}
%tox -e %{default_toxenv}
%endif

%files -n python3-%{pypi_name}
%license LICENSE
%{_bindir}/oslo_run_cross_tests
%{_bindir}/oslo_run_pre_release_tests
%{_bindir}/oslo_debug_helper
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.dist-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%doc README.rst
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.0.0-11
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.0.0-10
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.0.0-8
- Rebuilt for Python 3.14

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.0.0-7
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 5.0.0-4
- Rebuilt for Python 3.13

* Sat Jun 08 2024 Python Maint <python-maint@redhat.com> - 5.0.0-3
- Bootstrap for Python 3.13

* Tue May 07 2024 Karolina Surma <ksurma@redhat.com> 5.0.0-2
- Bring back the possibility to bootstrap the package

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 5.0.0-1
- Update to upstream version 5.0.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 4.5.0-5
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 4.5.0-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 4.5.0-1
- Update to upstream version 4.5.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.4.1-4
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 4.4.1-2
- Update to upstream version 4.4.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 4.2.0-1
- Update to upstream version 4.2.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.8.1-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 3.8.1-2
- Update to upstream version 3.8.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.7.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.7.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 3.7.1-1
- Update to 3.7.1

