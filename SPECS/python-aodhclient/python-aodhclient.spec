# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%global pypi_name aodhclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif
%global with_doc 1

%global common_desc \
This is a client library for Aodh built on the Aodh API. It \
provides a Python API (the aodhclient module) and a command-line tool.

Name:             python-aodhclient
Version:          3.6.0
Release:          6%{?dist}
Summary:          Python API and CLI for OpenStack Aodh

License:          Apache-2.0
URL:              https://launchpad.net/python-aodhclient
Source0:          https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz
%if 0%{?fedora}
Patch0:           0001-Revert-Add-OSprofiler-support-for-Aodh-client.patch
%endif
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildArch:        noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:          Python API and CLI for OpenStack Aodh

BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
BuildRequires:    git-core

%description -n python3-%{pypi_name}
%{common_desc}

%if 0%{?with_doc}
%package  doc
Summary:          Documentation for OpenStack Aodh API Client


%description doc
%{common_desc}
(aodh).

This package contains auto-generated documentation.
%endif

%package -n python3-%{pypi_name}-tests
Summary:          Python API and CLI for OpenStack Aodh Tests
Requires:         python3-%{pypi_name} = %{version}-%{release}

%description -n python3-%{pypi_name}-tests
%{common_desc}

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
sed -i '/\.\[test\]/,+1d' tox.ini

# Exclude some bad-known BRs
for pkg in %{excluded_brs}; do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

%if 0%{?fedora}
# Remove osprofiler as runtime dep
sed -i /^osprofiler.*/d requirements.txt
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
ln -s aodh %{buildroot}%{_bindir}/aodh-3

%if 0%{?with_doc}
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/aodhclient
%{python3_sitelib}/*.dist-info
%{_bindir}/aodh
%{_bindir}/aodh-3
%exclude %{python3_sitelib}/aodhclient/tests

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/aodhclient/tests

%if 0%{?with_doc}
%files doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 3.6.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 3.6.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Python Maint <python-maint@redhat.com> - 3.6.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Joel Capitao <jcapitao@redhat.com> 3.6.0-1
- Update to upstream version 3.6.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Python Maint <python-maint@redhat.com> - 3.5.1-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 3.5.1-1
- Update to upstream version 3.5.1

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Alfredo Moralejo <amoralej@gmail.com> 3.3.0-1
- Update to upstream version 3.3.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 3.2.0-3
- Rebuilt for Python 3.12

* Mon Apr 17 2023 Karolina Kula <kkula@redhat.com> 3.2.0-2
- Reapply osprofiler support removal

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 3.2.0-1
- Update to upstream version 3.2.0

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Alfredo Moralejo <amoralej@redhat.com> 3.0.0-2
- Removed support for osprofiler

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 3.0.0-1
- Update to upstream version 3.0.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.4.1-4
- Rebuilt for pyparsing-3.0.9

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2.4.1-3
- Rebuilt for Python 3.11

* Thu May 19 2022 Joel Capitao <jcapitao@redhat.com> 2.4.1-2
- Removed support for osprofiler

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 2.4.1-1
- Update to upstream version 2.4.1

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.2.0-3
- Rebuilt for Python 3.10

* Mon Nov 22 2021 Joel Capitao <amoralej@redhat.com> - 2.2.0-2
- Removed support for osprofiler

* Tue Mar 16 2021 Joel Capitao <jcapitao@redhat.com> 2.2.0-1
- Update to upstream version 2.2.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 06 2020 Alfredo Moralejo <amoralej@redhat.com> - 2.1.1-3
- Removed support for osprofiler

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 2.1.1-2
- Update to upstream version 2.1.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Joel Capitao <jcapitao@redhat.com> 2.0.1-3
- Removed Requires osprofiler

* Wed Jun 24 2020 Joel Capitao <jcapitao@redhat.com> 2.0.1-2
- Removed support for osprofiler

* Thu Jun 04 2020 Joel Capitao <jcapitao@redhat.com> 2.0.1-1
- Update to upstream version 2.0.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.3.0-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 11 2019 Alfredo Moralejo <amoralej@redhat.com> 1.3.0-2
- Removed support for osprofiler

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 1.3.0-1
- Update to upstream version 1.3.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.2.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Mar 11 2019 RDO <dev@lists.rdoproject.org> 1.2.0-1
- Update to 1.2.0

