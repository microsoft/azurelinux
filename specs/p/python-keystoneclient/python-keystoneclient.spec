# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8 tempest
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global common_desc \
Client library and command line utility for interacting with Openstack \
Identity API.

%global sname keystoneclient
%global with_doc 1

Name:       python-keystoneclient
Epoch:      1
Version:    5.5.0
Release: 6%{?dist}
Summary:    Client library for OpenStack Identity API
License:    Apache-2.0
URL:        https://launchpad.net/python-keystoneclient
Source0:    https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:  noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires: /usr/bin/openssl

%description
%{common_desc}

%package -n python3-%{sname}
Summary:    Client library for OpenStack Identity API

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core
# keyring is a optional dep but we are maintataining as default for backwards
# compatibility
Requires: python3-keyring >= 5.5.1

%description -n python3-%{sname}
%{common_desc}

%package -n python3-%{sname}-tests
Summary:  Python API and CLI for OpenStack Keystone (tests)

Requires:  python3-%{sname} = %{epoch}:%{version}-%{release}
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-oauthlib
Requires:  python3-oslotest
Requires:  python3-stestr
Requires:  python3-testtools
Requires:  python3-testresources
Requires:  python3-testscenarios
Requires:  python3-requests-mock
Requires:  python3-lxml

%description -n python3-%{sname}-tests
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary: Documentation for OpenStack Keystone API client

%description -n python-%{sname}-doc
%{common_desc}
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini

# Disable warnint-is-error in doc build
sed -i '/sphinx-build/ s/-W//' tox.ini

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

%install
%pyproject_install

%if 0%{?with_doc}
# Build HTML docs
# Disable warning-is-error as intersphinx extension tries
# to access external network and fails.
%tox -e docs
# Drop intersphinx downloaded file objects.inv to avoid rpmlint warning
rm -fr doc/build/html/objects.inv
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

%check
%tox -e %{default_toxenv} -- -- --exclude-regex '^.*test_cms.*'

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/%{sname}/tests

%if 0%{?with_doc}
%files -n python-%{sname}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{sname}-tests
%license LICENSE
%{python3_sitelib}/%{sname}/tests

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:5.5.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:5.5.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Python Maint <python-maint@redhat.com> - 1:5.5.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 07 2024 Joel Capitao <jcapitao@redhat.com> 1:5.5.0-1
- Update to upstream version 5.5.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Python Maint <python-maint@redhat.com> - 1:5.4.0-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 1:5.4.0-1
- Update to upstream version 5.4.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Alfredo Moralejo <amoralej@gmail.com> 1:5.2.0-1
- Update to upstream version 5.2.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Python Maint <python-maint@redhat.com> - 1:5.1.0-2
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 1:5.1.0-1
- Update to upstream version 5.1.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 1:5.0.1-1
- Update to upstream version 5.0.1

* Wed Sep 28 2022 Benjamin A. Beasley <code@musicinmybrain.net> - 1:4.4.0-4
- Fix broken descriptions

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1:4.4.0-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 1:4.4.0-1
- Update to upstream version 4.4.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:4.2.0-2
- Rebuilt for Python 3.10

* Tue Mar 16 2021 Joel Capitao <jcapitao@redhat.com> 1:4.2.0-1
- Update to upstream version 4.2.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Oct 29 2020 Alfredo Moralejo <amoralej@redhat.com> 1:4.1.1-2
- Update to upstream version 4.1.1

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 1:4.1.1-2
- Update to upstream version 4.1.1

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 1:4.1.1-1
- Update to upstream version 4.1.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 1:4.0.0-1
- Update to upstream version 4.0.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:3.21.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.21.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Alfredo Moralejo <amoralej@redhat.com> 1:3.21.0-2
- Update to upstream version 3.21.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.19.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:3.19.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 RDO <dev@lists.rdoproject.org> 1:3.19.0-1
- Update to 3.19.0

