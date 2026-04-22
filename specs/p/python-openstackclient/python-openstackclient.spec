# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order whereto python-zunclient python-watcherclient python-cyborgclient python-senlinclient python-muranoclient python-saharaclient python-designateclient python-magnumclient python-barbicanclient
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
# Exclude some BRs for Fedora
%if 0%{?fedora}
%global excluded_brs %{excluded_brs} tempest osc-placement python-ironic-inspector-client osprofiler
%endif

# Command name
%global cname openstack

# library name
%global sname %{cname}client

%global with_doc 0

%global common_desc \
python-%{sname} is a unified command-line client for the OpenStack APIs. \
It is a thin wrapper to the stock python-*client modules that implement the \
actual REST API client actions.

Name:             python-%{sname}
Version:          7.1.2
Release: 10%{?dist}
Summary:          OpenStack Command-line Client

License:          Apache-2.0
URL:              http://launchpad.net/%{name}
Source0:          https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
%if %{lua:print(rpm.vercmp(rpm.expand("%{version}"), '7.1.3'));} <= 0
# Patch https://review.opendev.org/c/openstack/python-openstackclient/+/930911 on 7.1.2
Patch0001:        0001-identity-in-service-set-command-don-t-pass-the-enabl.patch
# Patch https://review.opendev.org/c/openstack/python-openstackclient/+/931031 on 7.1.2
Patch0002:        0001-Always-resolve-domain-id.patch
%endif


# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
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
Summary:    OpenStack Command-line Client

BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    python3-osc-lib-tests
# Required to compile translation files
BuildRequires:    python3-babel

Requires:         python-%{sname}-lang = %{version}-%{release}
# Dependency for auto-completion
%if 0%{?fedora} || 0%{?rhel} > 7
Recommends:         bash-completion
%endif

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package -n python-%{sname}-doc
Summary:          Documentation for OpenStack Command-line Client

Requires: python3-%{sname} = %{version}-%{release}

%description -n python-%{sname}-doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%package  -n python-%{sname}-lang
Summary:   Translation files for Openstackclient

%description -n python-%{sname}-lang
Translation files for Openstackclient

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{name}-%{upstream_version} -S git


# (TODO) Remove this sed after fix is merged upstream
# https://review.opendev.org/c/openstack/python-openstackclient/+/808079
# Replace assertItemsEqual by assertCountEqual in test_volume_messages.py file
sed -i 's/assertItemsEqual/assertCountEqual/g' ./openstackclient/tests/unit/volume/v3/test_volume_message.py

sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/sphinx-build/ s/-W//' tox.ini
sed -i '/whereto*/d' tox.ini

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

# Generate i18n files
%{__python3} setup.py compile_catalog -d %{buildroot}%{python3_sitelib}/%{sname}/locale --domain openstackclient


# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s %{cname} %{buildroot}%{_bindir}/%{cname}-3

%if 0%{?with_doc}
export PYTHONPATH=.
%tox -e docs
sphinx-build -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/%{cname}.1 %{buildroot}%{_mandir}/man1/%{cname}.1

# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo doc/build/html/.htaccess
%endif

# Install i18n .mo files (.po and .pot are not required)
install -d -m 755 %{buildroot}%{_datadir}
rm -f %{buildroot}%{python3_sitelib}/%{sname}/locale/*/LC_*/%{sname}*po
rm -f %{buildroot}%{python3_sitelib}/%{sname}/locale/*pot
mv %{buildroot}%{python3_sitelib}/%{sname}/locale %{buildroot}%{_datadir}/locale
rm -rf %{buildroot}%{python3_sitelib}/%{sname}/locale

# Find language files
%find_lang %{sname} --all-name

%post -n python3-%{sname}
mkdir -p /etc/bash_completion.d
openstack complete | sed -n '/_openstack/,$p' > /etc/bash_completion.d/osc.bash_completion

%check
export PYTHON=%{__python3}
%tox -e %{default_toxenv} -- -- --exclude-regex 'openstackclient.tests.unit.common.test_module.TestModuleList.*'

%files -n python3-%{sname}
%license LICENSE
%doc README.rst
%{_bindir}/%{cname}
%{_bindir}/%{cname}-3
%{python3_sitelib}/%{sname}
%{python3_sitelib}/*.dist-info
%if 0%{?with_doc}
%{_mandir}/man1/%{cname}.1*

%files -n python-%{sname}-doc
%license LICENSE
%doc doc/build/html
%endif

%files -n python-%{sname}-lang -f %{sname}.lang
%license LICENSE

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.1.2-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.1.2-8
- Rebuilt for Python 3.14.0rc2 bytecode

* Mon Jul 28 2025 Python Maint <python-maint@redhat.com> - 7.1.2-7
- Rebuilt for Python 3.14

* Wed Jul 23 2025 Python Maint <python-maint@redhat.com> - 7.1.2-6
- Bootstrap for Python 3.14

* Fri May 02 2025 Miro Hrončok <mhroncok@redhat.com> - 7.1.2-5
- Exclude BuildRequires for python-designateclient, python-magnumclient, python-barbicanclient

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Joel Capitao <jcapitao@redhat.com> 7.1.2-3
- Update to upstream version 7.1.2

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Python Maint <python-maint@redhat.com> - 6.6.0-3
- Rebuilt for Python 3.13

* Sat Jul 13 2024 Python Maint <python-maint@redhat.com> - 6.6.0-2
- Bootstrap for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 6.6.0-1
- Update to upstream version 6.6.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Alfredo Moralejo <amoralej@gmail.com> 6.3.0-1
- Update to upstream version 6.3.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Python Maint <python-maint@redhat.com> - 6.2.0-2
- Rebuilt for Python 3.12

* Fri Apr 21 2023 Karolina Kula <kkula@redhat.com> 6.2.0-1
- Update to upstream version 6.2.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 6.0.0-1
- Update to upstream version 6.0.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Python Maint <python-maint@redhat.com> - 5.8.0-2
- Rebuilt for Python 3.11

* Mon May 23 2022 Joel Capitao <jcapitao@redhat.com> 5.8.0-1
- Update to upstream version 5.8.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 5.5.0-2
- Rebuilt for Python 3.10

* Mon Mar 22 2021 RDO <dev@lists.rdoproject.org> 5.5.0-1
- Update to 5.5.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 5.4.0-2
- Update to upstream version 5.4.0

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Joel Capitao <jcapitao@redhat.com> 5.2.0-1
- Update to upstream version 5.2.0

* Mon Jun 01 2020 Alfredo Moralejo <amoralej@redhat.com> - 4.0.0-4
- Fix unit tests

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 4.0.0-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Nov 08 2019 Alfredo Moralejo <amoralej@redhat.com> 4.0.0-1
- Update to upstream version 4.0.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 3.18.0-5
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 3.18.0-4
- Rebuilt for Python 3.8

* Mon Jul 29 2019 Alfredo Moralejo <amoralej@redhat.com> - 3.18.0-3
- Remove unneeded osprofiler as BR.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 RDO <dev@lists.rdoproject.org> 3.18.0-1
- Update to 3.18.0

