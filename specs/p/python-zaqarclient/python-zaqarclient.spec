# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order sphinx openstackdocstheme

%global sname zaqarclient

%global common_desc \
Python client to Zaqar messaging service API v1

Name:           python-zaqarclient
Version:        2.8.0
Release:        6%{?dist}
Summary:        Client Library for OpenStack Zaqar Queueing API

License:        Apache-2.0
URL:            http://wiki.openstack.org/zaqar
Source0:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{name}/%{name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif


%description
%{common_desc}

%package -n python3-%{sname}
Summary:        Client Library for OpenStack Zaqar Queueing API
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros

%description -n python3-%{sname}
%{common_desc}

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%setup -q -n %{name}-%{upstream_version}


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

%generate_buildrequires
%pyproject_buildrequires -t -e %{default_toxenv}

%build
%pyproject_wheel

%install
%pyproject_install


%files -n python3-%{sname}
%doc README.rst ChangeLog examples
%license LICENSE
%{python3_sitelib}/zaqarclient
%{python3_sitelib}/python_zaqarclient-*.dist-info

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.8.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.8.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jun 16 2025 Python Maint <python-maint@redhat.com> - 2.8.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 07 2024 Joel Capitao <jcapitao@redhat.com> 2.8.0-1
- Update to upstream version 2.8.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jul 13 2024 Python Maint <python-maint@redhat.com> - 2.7.0-2
- Rebuilt for Python 3.13

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 2.7.0-1
- Update to upstream version 2.7.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Oct 25 2023 Alfredo Moralejo <amoralej@gmail.com> 2.6.0-1
- Update to upstream version 2.6.0

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jun 13 2023 Python Maint <python-maint@redhat.com> - 2.5.1-2
- Rebuilt for Python 3.12

* Fri Apr 14 2023 Karolina Kula <kkula@redhat.com> 2.5.1-1
- Update to upstream version 2.5.1

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Nov 17 2022 Alfredo Moralejo <amoralej@redhat.com> 2.4.0-1
- Update to upstream version 2.4.0

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 2.3.0-2
- Rebuilt for Python 3.11

* Wed May 18 2022 Joel Capitao <jcapitao@redhat.com> 2.3.0-1
- Update to upstream version 2.3.0

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.1.0-2
- Rebuilt for Python 3.10

* Tue Mar 16 2021 Joel Capitao <jcapitao@redhat.com> 2.1.0-1
- Update to upstream version 2.1.0

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Oct 28 2020 Alfredo Moralejo <amoralej@redhat.com> 2.0.1-2
- Update to upstream version 2.0.1

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 04 2020 Joel Capitao <jcapitao@redhat.com> 1.13.1-1
- Update to upstream version 1.13.1

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.12.0-3
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 1.12.0-1
- Update to upstream version 1.12.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.11.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.11.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.11.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 RDO <dev@lists.rdoproject.org> 1.11.0-1
- Update to 1.11.0

