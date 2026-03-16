Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0x2ef3fe0ec2b075ab7458b5f8b702b20b13df2318

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

%global pypi_name debtcollector
%global with_doc 1
%global common_desc \
It is a collection of functions/decorators which is used to signal a user when \
*  a method (static method, class method, or regular instance method) or a class \
    or function is going to be removed at some point in the future. \
* to move a instance method/property/class from an existing one to a new one \
* a keyword is renamed \
* further customizing the emitted messages

Name:        python-%{pypi_name}
Version:     3.0.0
Release:     10%{?dist}
Summary:     A collection of Python deprecation patterns and strategies

License:     Apache-2.0
URL:         https://pypi.python.org/pypi/%{pypi_name}
Source0:     https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif

BuildRequires: python-pip
BuildRequires: python-pbr
BuildRequires: python-wheel
BuildRequires: python-setuptools
BuildRequires: python3-pytest
BuildRequires: python-dulwich
BuildRequires: python-openstackdocstheme
BuildRequires: python-toml
BuildRequires: python-tox
BuildRequires: python-wrapt
BuildRequires: python-extras
BuildRequires: python-sphinx
BuildRequires: python-tox-current-env
BuildRequires: python-virtualenv
BuildRequires: python3-testtools
BuildRequires: python3-fixtures

BuildArch:   noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

BuildRequires: git-core

%description
%{common_desc}

%package -n python3-%{pypi_name}
Summary:     A collection of Python deprecation patterns and strategies

BuildRequires: python3-devel
BuildRequires: pyproject-rpm-macros

%description -n python3-%{pypi_name}
%{common_desc}


%if 0%{?with_doc}
%package -n python-%{pypi_name}-doc
Summary:        Documentation for the debtcollector module

%description -n python-%{pypi_name}-doc
Documentation for the debtcollector module
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

%build
%pyproject_wheel

%install
%pyproject_install

%if 0%{?with_doc}
# doc
PYTHONPATH="%{buildroot}/%{python3_sitelib}"
%tox -e docs
# Fix hidden-file-or-dir warnings
rm -fr doc/build/html/.{doctrees,buildinfo}
rm -f doc/build/html/_static/images/docs/license.png
%endif

%files -n python3-%{pypi_name}
%doc README.rst CONTRIBUTING.rst
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}*.dist-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%if 0%{?with_doc}
%files -n python-%{pypi_name}-doc
%doc doc/build/html
%license LICENSE
%endif

%changelog
* Fri Jan 09 2026 Durga Jagadeesh Palli <v-dpalli@microsoft.com> - 3.0.0-10
- Upgrade to 3.0.0 (Reference: Fedora 44)
- License verified

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.22.0-4
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 06 2019 Alfredo Moralejo <amoralej@redhat.com> 1.22.0-2
- Update to upstream version 1.22.0

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.21.0-4
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.21.0-3
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Mar 08 2019 RDO <dev@lists.rdoproject.org> 1.21.0-1
- Update to 1.21.0
