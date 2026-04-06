# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global repo_bootstrap 0

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%global sname oslo.config
%global pypi_name oslo-config
# doc and tests are enabled by default unless %%repo_bootstrap
%bcond doc %[!0%{?repo_bootstrap}]
%bcond tests %[!0%{?repo_bootstrap}]

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
%if %{without doc}
# Exclude sphinx from BRs if docs are disabled
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%if %{without tests}
# Exclude oslo.log from BRs if docs and tests are disabled
%global excluded_brs %{excluded_brs} oslo.log
%endif
%endif

Name:       python-oslo-config
Epoch:      2
Version:    9.6.0
Release:    7%{?dist}
Summary:    OpenStack common configuration library

Group:      Development/Languages
License:    Apache-2.0
URL:        https://launchpad.net/%{sname}
Source0:    https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{sname}/%{sname}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
Patch0001:  0001-Fix-test_sub_command_multiple-on-Python-3.12.5.patch

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%package -n python3-%{pypi_name}
Summary:    OpenStack common configuration library
Obsoletes: python2-%{pypi_name} < %{version}-%{release}

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core

%description -n python3-%{pypi_name}
The Oslo project intends to produce a python library containing
infrastructure code shared by OpenStack projects. The APIs provided
by the project should be high quality, stable, consistent and generally
useful.

The oslo-config library is a command line and configuration file
parsing library from the Oslo project.

%if %{with doc}
%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack common configuration library

%description -n python-%{pypi_name}-doc
Documentation for the oslo-config library.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{sname}-%{upstream_version} -S git
# Remove shebang from non executable file, it's used by the oslo-config-validator binary.
sed -i '/\/usr\/bin\/env/d' oslo_config/validator.py

# Remove tests requiring sphinx if sphinx is not available
%if %{with doc} == 0
rm oslo_config/tests/test_sphinxext.py
rm oslo_config/tests/test_sphinxconfiggen.py
%endif

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
%pyproject_buildrequires %{?with_doc:-e docs} %{?with_tests:-e %{default_toxenv}}

%build
%pyproject_wheel

%if %{with doc}
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install
pushd %{buildroot}/%{_bindir}
for i in generator validator
do
ln -s oslo-config-$i oslo-config-$i-3
done
popd

%check
%if %{with tests}
%tox -e %{default_toxenv}
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/oslo-config-generator
%{_bindir}/oslo-config-generator-3
%{_bindir}/oslo-config-validator
%{_bindir}/oslo-config-validator-3
%{python3_sitelib}/oslo_config
%{python3_sitelib}/*.dist-info

%if %{with doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2:9.6.0-7
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2:9.6.0-6
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 18 2025 Python Maint <python-maint@redhat.com> - 2:9.6.0-4
- Bootstrap for Python 3.14.0b3 bytecode

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2:9.6.0-3
- Bootstrap for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 28 2024 Joel Capitao <jcapitao@redhat.com> 2:9.6.0-1
- Update to upstream version 9.6.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Python Maint <python-maint@redhat.com> - 2:9.4.0-4
- Rebuilt for Python 3.13

* Mon Jun 10 2024 Python Maint <python-maint@redhat.com> - 2:9.4.0-3
- Bootstrap for Python 3.13

* Thu May 16 2024 Alfredo Moralejo <amoralej@redhat.com> 2:9.4.0-2
- Make it possible to bootstrap this package, use %bconds

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 2:9.4.0-1
- Update to upstream version 9.4.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Alfredo Moralejo <amoralej@gmail.com> 2:9.2.0-1
- Update to upstream version 9.2.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 2:9.1.1-2
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 2:9.1.1-1
- Update to upstream version 9.1.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 2:9.0.0-1
- Update to upstream version 9.0.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2:8.8.0-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 2:8.8.0-1
- Update to upstream version 8.8.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2:8.5.0-2
- Rebuilt for Python 3.10

* Wed Mar 17 2021 Joel Capitao <jcapitao@redhat.com> 2:8.5.0-1
- Update to upstream version 8.5.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 21 2020 Joel Capitao <jcapitao@redhat.com> 2:8.3.2-2
- Enable sources tarball validation using GPG signature.

* Thu Sep 17 2020 RDO <dev@lists.rdoproject.org> 2:8.3.2-1
- Update to 8.3.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:8.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 2:8.0.2-1
- Update to upstream version 8.0.2

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2:6.11.1-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:6.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 2:6.11.1-2
- Update to upstream version 6.11.1

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2:6.8.1-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2:6.8.1-4
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:6.8.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 16 2019 Miro Hrončok <mhroncok@redhat.com> - 2:6.8.1-2
- Rename the documentation package back to python-oslo-config-doc

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 2:6.8.1-1
- Update to 6.8.1

