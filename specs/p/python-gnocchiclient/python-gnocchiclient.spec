# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global sources_gpg 0
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f

%global pypi_name gnocchiclient

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order
# Exclude sphinx from BRs if docs are disabled
%if ! 0%{?with_doc}
%global excluded_brs %{excluded_brs} sphinx openstackdocstheme
%endif

# NOTE(jpena): doc build fails with recent cliff versions, and hardcodes
# a call to unversioned python in
# https://github.com/gnocchixyz/python-gnocchiclient/blob/master/doc/source/conf.py#L54
%global with_doc 0

%global common_desc \
This is a client library for Gnocchi built on the Gnocchi API. It \
provides a Python API (the gnocchiclient module) and a command-line tool.

Name:             python-gnocchiclient
Version:          7.1.0
Release: 7%{?dist}
Summary:          Python API and CLI for OpenStack Gnocchi

License:          Apache-2.0
URL:              https://github.com/openstack/%{name}
Source0:          https://pypi.io/packages/source/g/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
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
Summary:          Python API and CLI for OpenStack Gnocchi


BuildRequires:    python3-devel
BuildRequires:    pyproject-rpm-macros
%description -n python3-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:          Documentation for OpenStack Gnocchi API Client
Group:            Documentation

%description      doc
%{common_desc}

This package contains auto-generated documentation.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version}


sed -i /^[[:space:]]*-c{env:.*_CONSTRAINTS_FILE.*/d tox.ini
sed -i "s/^deps = -c{env:.*_CONSTRAINTS_FILE.*/deps =/" tox.ini
sed -i /^minversion.*/d tox.ini
sed -i /^requires.*virtualenv.*/d tox.ini
sed -i '/\.\[test,openstack\]/,+2d' tox.ini
sed -i '/\.*\[testenv\]deps/,+1d' tox.ini
sed -i '/\.\[test,doc\]/d' tox.ini

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
%tox -e docs

# Fix hidden-file-or-dir warnings
rm -rf doc/build/html/.doctrees doc/build/html/.buildinfo
%endif

%install
%pyproject_install

# Create a versioned binary for backwards compatibility until everything is pure py3
ln -s gnocchi %{buildroot}%{_bindir}/gnocchi-3

%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE
%{_bindir}/gnocchi
%{_bindir}/gnocchi-3
%{python3_sitelib}/gnocchiclient
%{python3_sitelib}/*.dist-info

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%endif

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.1.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.1.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 7.1.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 07 2024 Joel Capitao <jcapitao@redhat.com> 7.1.0-1
- Update to upstream version 7.1.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul 15 2024 Python Maint <python-maint@redhat.com> - 7.0.8-4
- Rebuilt for Python 3.13

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Alfredo Moralejo <amoralej@gmail.com> 7.0.8-1
- Update to upstream version 7.0.8

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Python Maint <python-maint@redhat.com> - 7.0.7-9
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Alfredo Moralejo <amoralej@redhat.com> - 7.0.7-7
- Rebuild for Fedora 38

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 7.0.7-3
- Rebuilt for Python 3.10

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Oct 05 2020 Matthias Runge <mrunge@redhat.com> - 7.0.7-1
- updated to 7.0.7

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 7.0.4-7
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 7.0.4-5
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Oct 28 2018 Miro Hrončok <mhroncok@redhat.com> - 7.0.4-2
- Subpackages python2-gnocchiclient, python2-gnocchiclient-tests have been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Thu Aug 09 2018 RDO <dev@lists.rdoproject.org> 7.0.4-1
- Update to 7.0.4

