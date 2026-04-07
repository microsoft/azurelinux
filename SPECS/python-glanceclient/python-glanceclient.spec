# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global sname glanceclient
%global with_doc 1
# for bootstrapping and Python bumps: with functional tests there is a
# dependency loop between os-client-config and glanceclient, turn this
# off to disable the functional tests and drop os-client-config dep
%global with_functional_tests 0

# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order tempest
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
# Exclude os-client-config from BRs if functional tests are disabled
%if ! 0%{?with_functional_tests}
%global excluded_brs %{excluded_brs} os-client-config
%endif

%global common_desc \
This is a client for the OpenStack Glance API. There's a Python API (the \
glanceclient module), and a command-line script (glance). Each implements \
100% of the OpenStack Glance API.

Name:             python-glanceclient
Epoch:            1
Version:          4.7.0
Release:          5%{?dist}
Summary:          Python API and CLI for OpenStack Glance

License:          Apache-2.0
URL:              https://launchpad.net/python-glanceclient
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires:    git-core

%description
%{common_desc}

%package -n python3-%{sname}
Summary:          Python API and CLI for OpenStack Glance

BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary:          Documentation for OpenStack Glance API Client

%description      doc
%{common_desc}

This package contains auto-generated documentation.
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
sed -i '/sphinx-build/ s/-W//' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Wipe functional tests if they're disabled
%if ! 0%{?with_functional_tests}
rm -rf glanceclient/tests/functional
%endif

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

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s glance %{buildroot}%{_bindir}/glance-3

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/glance.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/glance

# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/glanceclient/tests

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
# generate man page
sphinx-build -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/glance.1 %{buildroot}%{_mandir}/man1/glance.1
%endif

%check
# CentOS CI environment is setting "http://cache.rdu2.centos.org:8080" which breaks the unit tests.
unset http_proxy
unset https_proxy
%tox -e %{default_toxenv} -- -- --exclude-regex '(glanceclient.tests.unit.test_ssl.TestHTTPSVerifyCert*|.*test_cache_schemas_gets_when_not_exists|.*test_cache_schemas_gets_when_forced)|.*test_http_chunked_response|.*test_log_request_id_once'


%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/glanceclient
%{python3_sitelib}/*.dist-info
%{_sysconfdir}/bash_completion.d
%if 0%{?with_doc}
%{_mandir}/man1/glance.1.gz
%endif
%{_bindir}/glance
%{_bindir}/glance-3

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1:4.7.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1:4.7.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 23 2025 Alfredo Moralejo <amoralej@redhat.com> - 1:4.7.0-3
- Bootstrap for python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Joel Capitao <jcapitao@redhat.com> 1:4.7.0-1
- Update to upstream version 4.7.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Alfredo Moralejo <amoralej@redhat.com> 1:4.5.0-2
- Rebuild with python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 1:4.5.0-1
- Update to upstream version 4.5.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Alfredo Moralejo <amoralej@gmail.com> 1:4.4.0-1
- Update to upstream version 4.4.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 1:4.3.0-2
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 1:4.3.0-1
- Update to upstream version 4.3.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:4.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 1:4.1.0-1
- Update to upstream version 4.1.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 1:3.6.0-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 1:3.6.0-1
- Update to upstream version 3.6.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1:3.3.0-2
- Rebuilt for Python 3.10

* Tue Mar 16 2021 Joel Capitao <jcapitao@redhat.com> 1:3.3.0-1
- Update to upstream version 3.3.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 1:3.2.2-2
- Update to upstream version 3.2.2

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 1:3.1.1-1
- Update to upstream version 3.1.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1:2.17.0-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Alfredo Moralejo <amoralej@redhat.com> 1:2.17.0-1
- Update to upstream version 2.17.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.16.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1:2.16.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.16.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 RDO <dev@lists.rdoproject.org> 1:2.16.0-1
- Update to 2.16.0

