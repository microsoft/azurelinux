# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{!?sources_gpg: %{!?dlrn:%global sources_gpg 1} }
%global sources_gpg_sign 0xf8675126e2411e7748dd46662fc2093e4682645f
%global pypi_name hacking

# disable tests for now, see
# https://bugs.launchpad.net/hacking/+bug/1652409
# https://bugs.launchpad.net/hacking/+bug/1607942
# https://bugs.launchpad.net/hacking/+bug/1652411
%global with_tests 0

%global with_doc 1

%global common_desc OpenStack Hacking Guideline Enforcement

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
# we are excluding some BRs from automatic generator
%global excluded_brs doc8 bandit pre-commit hacking flake8-import-order

Name:           python-%{pypi_name}
Version:        7.0.0
Release: 7%{?dist}
Summary:        OpenStack Hacking Guideline Enforcement

License:        Apache-2.0
URL:            http://github.com/openstack-dev/hacking
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
Source101:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz.asc
Source102:        https://releases.openstack.org/_static/%{sources_gpg_sign}.txt
%endif
%if 0%{?fedora}
# FIXME(apevec) patches do not apply after https://review.openstack.org/514934
# Mostly adapt tests to work with both flake8 2.x and 3.x. Note,
# local-checks feature is entirely broken with 3.x. Will send upstream
# when I find a way to do it which doesn't involve signing my
# firstborn over to the openstack foundation
#Patch0:         0001-Tests-adapt-to-flake8-3.x.patch
# Hack out the 'local-checks' feature, since it doesn't work anyway,
# to avoid the dep it introduces on pep8, and disable the test for the
# feature. Only apply on releases with flake8 3.x.
#Patch1:         0002-Disable-local-checks.patch
%endif

%if 0%{?fedora}
# FIXME(hiwkby) a patch that does not require eventlet
# Actually, eventlet is not needed for unittests
Patch1:         test-requirements.txt.patch
%endif
BuildArch:      noarch

# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
BuildRequires:  /usr/bin/gpgv2
%endif

%description
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
%endif

%package -n python3-%{pypi_name}
Summary:        OpenStack Hacking Guideline Enforcement

BuildRequires:  git-core
BuildRequires:  python3-devel
BuildRequires:  pyproject-rpm-macros
BuildRequires:  python3dist(wheel)
BuildRequires:  python3dist(pbr)
BuildRequires:  python3dist(tox-current-env)

%description -n python3-%{pypi_name}
%{common_desc}
%if 0%{?fedora}
**NOTE**: the local-check feature is DISABLED in this package! See
https://bugs.launchpad.net/hacking/+bug/1652409 for details.
%endif

%prep
# Required for tarball sources verification
%if 0%{?sources_gpg} == 1
%{gpgverify}  --keyring=%{SOURCE102} --signature=%{SOURCE101} --data=%{SOURCE0}
%endif
%autosetup -n %{pypi_name}-%{upstream_version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# remove /usr/bin/env from core.py
sed -i '1d' hacking/core.py

# remove /usr/bin/env from tests/test_doctest.py
sed -i '1d' hacking/tests/test_doctest.py


# TODO(jcapitao): remove the line below once flake8 6.1.0 is build in Fedora and
# RDO https://src.fedoraproject.org/rpms/python-flake8/pull-request/14
sed -i "s/flake8.*/flake8/" requirements.txt


sed -i /.*-c{env:TOX_CONSTRAINTS_FILE.*/d tox.ini
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
%generate_buildrequires
%if 0%{?with_doc}
  %pyproject_buildrequires -t -e %{default_toxenv},docs
%else
  %pyproject_buildrequires -t -e %{default_toxenv}
%endif

%build
%pyproject_wheel

%if 0%{?with_doc}
# generate html docs
%tox -e docs
# remove the sphinx-build-3 leftovers
rm -rf doc/build/html/.{doctrees,buildinfo} doc/build/html/objects.inv
%endif

%install
%pyproject_install

%check
%if 0%{?with_tests}
%tox -e %{default_toxenv}
%endif

%files -n python3-%{pypi_name}
%if 0%{?with_doc}
%doc doc/build/html README.rst
%else
%doc README.rst
%endif
%license LICENSE
%{python3_sitelib}/*.dist-info
%{python3_sitelib}/%{pypi_name}

%changelog
* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 7.0.0-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 7.0.0-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jun 04 2025 Python Maint <python-maint@redhat.com> - 7.0.0-3
- Rebuilt for Python 3.14

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 08 2024 Joel Capitao <jcapitao@redhat.com> 7.0.0-1
- Update to upstream version 7.0.0

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jul 10 2024 Hirotaka Wakabayashi <hiwkby@yahoo.com> 6.1.0-3
- Move patch to git rather than sources (PR#2 by churchyard)

* Wed Jul 10 2024 Hirotaka Wakabayashi <hiwkby@yahoo.com> 6.1.0-2
- Adds a workaround for a building error(eventlet)

* Mon May 06 2024 Alfredo Moralejo <amoralej@redhat.com> 6.1.0-1
- Update to upstream version 6.1.0

* Fri Jan 26 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 26 2023 Alfredo Moralejo <amoralej@gmail.com> 6.0.1-1
- Update to upstream version 6.0.1

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jul 14 2023 Python Maint <python-maint@redhat.com> - 4.0.0-8
- Rebuilt for Python 3.12

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 4.0.0-5
- Rebuilt for Python 3.11

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 4.0.0-2
- Rebuilt for Python 3.10

* Mon Feb 01 2021 Matthias Runge <mrunge@redhat.com> - 4.0.0-1
- rebase to 4.0.0 (rhbz#1893428)

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-11
- Rebuilt for Python 3.9

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-9
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-8
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Apr 25 2019 Matthias Runge <mrunge@redhat.com> - 1.1.0-6
- drop python2 package (rhbz#1701951)

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Matthias Runge <mrunge@redhat.com> - 1.1.0-4
- drop requirements pyflakes, pep8, flake8 and use pycodestyle instead

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-2
- Rebuilt for Python 3.7

* Wed May 09 2018 Matthias Runge <mrunge@redhat.com> - 1.1.0-1
- update to 1.1.0 (rhbz#1576139)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.13.0-4
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 20 2017 Matthias Runge <mrunge@redhat.com> - 0.13.0-2
- disable tests for now (see above for links to bugs)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Adam Williamson <awilliam@redhat.com> - 0.13.0-1
- Update to 0.13.0 (some fixes for flake8 3.x compat from upstream)
- Patch test suite to be compatible with flake8 2.x and 3.x
- Disable 'local-check' feature on >F25 (incompatible with flake8 3.x)
- Re-enable Python 3 tests (they seem to work again now)

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 0.10.2-5
- Rebuild for Python 3.6

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.10.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.2-2
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Sep 01 2015 Lukas Bezdicka <lbezdick@redhat.com> - 0.10.2-1
- Add python3 sub package and update to 0.10.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.10.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Mar 03 2015 Matthias Runge <mrunge@redhat.com> - 0.10.1-1
- update to 0.10.1

* Mon Oct 20 2014 Matthias Runge <mrunge@redhat.com> - 0.9.2-1
- udapte to 0.9.2

* Tue Jun 10 2014 Matthias Runge <mrunge@redhat.com> - 0.9.1-1
- update to 0.9.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Matthias Runge <mrunge@redhat.com> - 0.8.1-1
- update to 0.8.1

* Tue Nov 19 2013 Matthias Runge <mrunge@redhat.com> - 0.8.0-1
- update to 0.8.0

* Tue Sep 17 2013 Matthias Runge <mrunge@redhat.com> - 0.7.2-1
- update to 0.7.2

* Fri Jun 07 2013 Matthias Runge <mrunge@redhat.com> - 0.5.3-2
- also use checks and move requirements to rpm-requiremens

* Mon Apr 29 2013 Matthias Runge <mrunge@redhat.com> - 0.5.3-1
- Initial package.
