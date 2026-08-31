# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%global pypi_name keystoneauth1

%global common_desc \
Keystoneauth provides a standard way to do authentication and service requests \
within the OpenStack ecosystem. It is designed for use in conjunction with \
the existing OpenStack clients and for simplifying the process of writing \
new clients.

%global with_doc 1

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order flake8-docstrings

Name:       python-%{pypi_name}
Version:    5.8.0
Release:    6%{?dist}
Summary:    Authentication Library for OpenStack Clients
License:    Apache-2.0
URL:        https://pypi.io/pypi/%{pypi_name}
Source0:    https://tarballs.openstack.org/keystoneauth/keystoneauth1-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/keystoneauth/keystoneauth1-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        Authentication Libarary for OpenStack Identity
%{?python_provide:%python_provide python3-keystoneauth}

BuildRequires: git-core
BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack Identity Authentication Library

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Identity Authentication Library
%endif


%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git

sed -i '/sphinx.ext.intersphinx.*$/d'  doc/source/conf.py

# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove syntax tests
rm keystoneauth1/tests/unit/test_hacking_checks.py

sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
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
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif


%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
# Disabling warning-is-error because of issue with python2 giving a warning:
# "The config value `apidoc_module_dir' has type `unicode', expected to ['str']."
%tox -e docs
rm -rf doc/build/html/.buildinfo
%endif

%check
%tox -e %{default_toxenv} -- -- --exclude-regex '(.*test_keystoneauth_betamax_fixture)'

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.8.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.8.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.8.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Joel Capitao <jcapitao@redhat.com> 5.8.0-1
- Update to upstream version 5.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Alfredo Moralejo <amoralej@redhat.com> 5.6.0-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 5.6.0-1
- Update to upstream version 5.6.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Alfredo Moralejo <amoralej@gmail.com> 5.3.0-1
- Update to upstream version 5.3.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 5.1.2-2
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 5.1.2-1
- Update to upstream version 5.1.2

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 5.0.0-1
- Update to upstream version 5.0.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 4.5.0-3
- Rebuilt for Python 3.11

* Thu Jun 09 2022 Miro Hrončok <mhroncok@redhat.com> - 4.5.0-2
- Remove unused mox3 build dependency

* Thu May 19 2022 Joel Capitao <jcapitao@redhat.com> 4.5.0-1
- Update to upstream version 4.5.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.3.1-2
- Rebuilt for Python 3.10

* Wed Mar 17 2021 Joel Capitao <jcapitao@redhat.com> 4.3.1-1
- Update to upstream version 4.3.1

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 4.2.1-2
- Update to upstream version 4.2.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 4.0.0-1
- Update to upstream version 4.0.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 3.17.2-2
- Rebuilt for Python 3.9

* Mon May 04 2020 Javier Peña <jpena@redhat.com> - 3.17.2-1
- Update to upstream version 3.17.2 (bz#1830974)

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Alfredo Moralejo <amoralej@redhat.com> 3.17.1-2
- Update to upstream version 3.17.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.13.1-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.13.1-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 3.13.1-1
- Update to 3.13.1

