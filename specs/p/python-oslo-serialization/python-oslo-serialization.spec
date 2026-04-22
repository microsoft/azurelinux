# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some runtime reqs from automatic generator
%global excluded_reqs tzdata
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

%global pypi_name oslo.serialization
%global pkg_name oslo-serialization
%global with_doc 1

%global common_desc \
An OpenStack library for representing objects in transmittable and \
storable formats.

Name:           python-%{pkg_name}
Version:        5.5.0
Release: 7%{?dist}
Summary:        OpenStack oslo.serialization library

License:        Apache-2.0
URL:            https://launchpad.net/oslo
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
%if %{lua:print(rpm.vercmp(rpm.expand("%{version}"), '5.2.0'));} < 0
#TODO(jcapitao): remove the line below once https://review.opendev.org/c/openstack/oslo.serialization/+/887141
# is contained in a tag.
Patch0001:        0001-Remove-extra-spaces-in-tox.ini.patch
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
%{common_desc}

%package -n python3-%{pkg_name}
Summary:        OpenStack oslo.serialization library

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
Requires:       python3-pytz

%description -n python3-%{pkg_name}
%{common_desc}


%package -n python3-%{pkg_name}-tests
Summary:   Tests for OpenStack Oslo serialization library

Requires:  python3-%{pkg_name} = %{version}-%{release}
Requires:  python3-oslotest
Requires:  python3-oslo-i18n
Requires:  python3-stestr
Requires:  python3-netaddr
Requires:  python3-simplejson

%description -n python3-%{pkg_name}-tests
Tests for OpenStack Oslo serialization library

%if 0%{?with_doc}
%package -n python-%{pkg_name}-doc
Summary:    Documentation for the Oslo serialization library

Requires:  python3-%{pkg_name} = %{version}-%{release}

%description -n python-%{pkg_name}-doc
Documentation for the Oslo serialization library.
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

# Exclude some bad-known BRs
for pkg in %{excluded_brs};do
  for reqfile in doc/requirements.txt test-requirements.txt; do
    if [ -f $reqfile ]; then
      sed -i /^${pkg}.*/d $reqfile
    fi
  done
done

# Automatic BR generation
# Exclude some bad-known runtime reqs
for pkg in %{excluded_reqs};do
  sed -i /^${pkg}.*/d requirements.txt
done

%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# doc
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
%endif

%install
%pyproject_install

%check
export OS_TEST_PATH="./oslo_serialization/tests"
%tox -e %{default_toxenv}

%files -n python3-%{pkg_name}
%doc README.rst
%license LICENSE
%{python3_sitelib}/oslo_serialization
%{python3_sitelib}/*.dist-info
%exclude %{python3_sitelib}/oslo_serialization/tests

%if 0%{?with_doc}
%files -n python-%{pkg_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%files -n python3-%{pkg_name}-tests
%{python3_sitelib}/oslo_serialization/tests

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 5.5.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 5.5.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 5.5.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 07 2024 Joel Capitao <jcapitao@redhat.com> 5.5.0-1
- Update to upstream version 5.5.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 08 2024 Python Maint <python-maint@redhat.com> - 5.4.0-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 5.4.0-1
- Update to upstream version 5.4.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Alfredo Moralejo <amoralej@gmail.com> 5.2.0-1
- Update to upstream version 5.2.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Python Maint <python-maint@redhat.com> - 5.1.1-2
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 5.1.1-1
- Update to upstream version 5.1.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 5.0.0-1
- Update to upstream version 5.0.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 4.3.0-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 4.3.0-1
- Update to upstream version 4.3.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.1.0-2
- Rebuilt for Python 3.10

* Tue Mar 16 2021 Joel Capitao <jcapitao@redhat.com> 4.1.0-1
- Update to upstream version 4.1.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 4.0.1-2
- Update to upstream version 4.0.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 03 2020 Joel Capitao <jcapitao@redhat.com> 3.1.1-1
- Update to upstream version 3.1.1

* Mon Jun 01 2020 Alfredo Moralejo <amoralej@redhat.com> - 2.29.2-5
- Remove hacking as build requirement

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.29.2-4
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.29.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 2.29.2-2
- Update to upstream version 2.29.2

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 2.28.2-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.28.2-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.28.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 2.28.2-1
- Update to 2.28.2

