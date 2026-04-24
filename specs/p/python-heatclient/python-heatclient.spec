# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order tempest
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc 0

%global sname heatclient

%global common_desc \
This is a client for the OpenStack Heat API. There's a Python API (the \
heatclient module), and a command-line script (heat). Each implements 100% of \
the OpenStack Heat API.

Name:    python-heatclient
Version: 4.0.0
Release: 6%{?dist}
Summary: Python API and CLI for OpenStack Heat

License: Apache-2.0
URL:     https://launchpad.net/python-heatclient
Source0: https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch: noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
%{common_desc}

%package -n python3-%{sname}
Summary: Python API and CLI for OpenStack Heat

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros
BuildRequires: git-core

%description -n python3-%{sname}
%{common_desc}

%if 0%{?with_doc}
%package doc
Summary: Documentation for OpenStack Heat API Client

%description doc
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
echo "%{version}" > %{buildroot}%{python3_sitelib}/heatclient/versioninfo
# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s heat %{buildroot}%{_bindir}/heat-3

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 tools/heat.bash_completion \
    %{buildroot}%{_sysconfdir}/bash_completion.d/heat

# Delete tests
rm -fr %{buildroot}%{python3_sitelib}/heatclient/tests

%if 0%{?with_doc}
export PYTHONPATH="%{buildroot}/%{python3_sitelib}"
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.doctrees doc/build/html/.buildinfo

# generate man page
sphinx-build -W -b man doc/source doc/build/man
install -p -D -m 644 doc/build/man/heat.1 %{buildroot}%{_mandir}/man1/heat.1
%endif

%files -n python3-%{sname}
%doc README.rst
%license LICENSE
%{python3_sitelib}/heatclient
%{python3_sitelib}/*.dist-info
%{_sysconfdir}/bash_completion.d
%if 0%{?with_doc}
%{_mandir}/man1/heat.1.gz
%endif
%{_bindir}/heat
%{_bindir}/heat-3

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 4.0.0-5
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 4.0.0-4
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 07 2024 Joel Capitao <jcapitao@redhat.com> 4.0.0-1
- Update to upstream version 4.0.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Python Maint <python-maint@redhat.com> - 3.5.0-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 3.5.0-1
- Update to upstream version 3.5.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Alfredo Moralejo <amoralej@gmail.com> 3.3.0-1
- Update to upstream version 3.3.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Python Maint <python-maint@redhat.com> - 3.2.0-2
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 3.2.0-1
- Update to upstream version 3.2.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 3.1.0-1
- Update to upstream version 3.1.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Python Maint <python-maint@redhat.com> - 2.5.1-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 2.5.1-1
- Update to upstream version 2.5.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.3.0-2
- Rebuilt for Python 3.10

* Tue Mar 16 2021 Joel Capitao <jcapitao@redhat.com> 2.3.0-1
- Update to upstream version 2.3.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 2.2.1-2
- Update to upstream version 2.2.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Joel Capitao <jcapitao@redhat.com> 2.1.0-1
- Update to upstream version 2.1.0

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.18.0-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Alfredo Moralejo <amoralej@redhat.com> 1.18.0-1
- Update to upstream version 1.18.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.17.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.17.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 RDO <dev@lists.rdoproject.org> 1.17.0-1
- Update to 1.17.0

