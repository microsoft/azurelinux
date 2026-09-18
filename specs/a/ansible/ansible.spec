# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
# Copyright (C) Fedora Project Authors
# License Text: https://spdx.org/licenses/MIT.html

# Compatibility                                                             #
#############################################################################
# This specfile should remain compatible with EPEL 9 and stable Fedoras.    #
# The EPEL 8 specfile is separately maintained,                             #
# but the ansible-prep.sh and ansible-install-license.sh scripts are shared #
# across branches.                                                          #
#############################################################################

# TODO: Re-enable docs and tests once possible
%bcond docs 0
%bcond tests 0

# disable the python -s shbang flag as we want to be able to find non system modules
# NB: We cannot use https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#_py3_shebang_S on RHEL 9.
%global py3_shebang_flags %(echo %{py3_shebang_flags} | sed 's|s||')

# Roles' files and templates should not be mangled.
# These files are installed on remote systems which may or may not have the
# same filesystem layout as Fedora.
%global __brp_mangle_shebangs_exclude_from ^%{python3_sitelib}/ansible_collections/[^/]+/[^/]+/roles/[^/]+/(files|templates)/.*$
%global __requires_exclude_from %{?__requires_exclude_from:%__requires_exclude_from|}%{__brp_mangle_shebangs_exclude_from}

%if 0%{?rhel} >= 8
# ansible-core package is built against Python 3.11 in RHEL 8 and RHEL 9 which
# is not the default version.
%global python3_pkgversion 3.11
%endif

Name:           ansible
Summary:        Curated set of Ansible collections included in addition to ansible-core
Version:        11.13.0
%global uversion %{version_no_tilde %{quote:%nil}}
Release:        1%{?dist}

# In addition to GPL-3.0-or-later, the following licenses apply.
# License text that solely exists in file headers were not considered.
# Instead, the overall license was determined by searching for license files
# This is the only the practical way to handle license scanning for a project
# of this size.
# All collections must be primarily licensed under GPL-3.0-or-later, so top
# level license files are excluded.
# find /usr/share/licenses/ansible -type f | grep -vEe '(COPYING|LICENSE)(\.(txt|md))?$' -e 'GPL' | xargs -n1 basename | sort -u
#
# Apache-2.0.txt
# Apache-license.txt
# BSD-2-Clause.txt
# BSD-3-Clause.txt
# MIT.txt
# MPL-2.0.txt
# PSF-2.0.txt
# PSF-license.txt
License:        GPL-3.0-or-later AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND MIT AND MPL-2.0 AND PSF-2.0
Source0:        %{pypi_source %{name} %{uversion}}
Source1:        ansible-prep.sh
Source2:        ansible-install-licenses.sh

Url:            https://ansible.com
BuildArch:      noarch

BuildRequires:  dos2unix
BuildRequires:  findutils
BuildRequires:  hardlink
BuildRequires:  python%{python3_pkgversion}-devel

%if %{with tests}
# TODO build-requires
%endif

%if %{with docs}
# TODO build-requires
%endif


%description
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

This package provides a curated set of Ansible collections included in addition
to ansible-core.


%prep
%autosetup -N -n %{name}-%{uversion}

# Relax ansible-core dependency to avoid FTI bugs on EPEL
#
# This is necessary, because the EPEL ansible maintainers don't have control
# over ansible-core in RHEL, and it's difficult to time updates across
# repositories. I have tried to stick to upstream's version constraints, but
# that's apparently not working too well. This change gives us a grace period
# to properly release and test new ansible major versions after RHEL rebases
# ansible-core. The lower version constraints can stay in place.

sed "s|ansible-core ~=|ansible-core >=|" setup.cfg > setup.cfg.bak
# Verify
set -o pipefail
grep -B1 "ansible-core >=" setup.cfg.bak | grep -F 'install_requires ='
%if %{defined rhel}
mv setup.cfg.bak setup.cfg
%endif

# ansible-prep.sh
%{S:1}

(
mkdir licenses docs
cd ansible_collections
# ansible-license-install.sh
%{S:2} \
    "$(readlink -f ../licenses)" \
    "$(readlink -f ../docs)" \
)


%generate_buildrequires
%pyproject_buildrequires


%build
%py3_shebang_fix ansible_collections

%pyproject_wheel


%install
%pyproject_install
# This adds over a minute to the build due to the size of the ansible package.
# It's better to manually specify the paths in %%files...
# %%pyproject_save_files ansible_collections

mkdir -p %{buildroot}%{_licensedir}/ansible %{buildroot}%{_docdir}/ansible
mv licenses %{buildroot}%{_licensedir}/ansible/ansible_collections
mv docs %{buildroot}%{_pkgdocdir}/ansible_collections

hardlink --reflink=never -v %{buildroot}%{python3_sitelib}/ansible_collections
hardlink --reflink=never -v %{buildroot}%{_licensedir}/ansible

# XXX: One of the build steps is messing with the permission.
# XXX: The file is 0755 in the source tarball.
chmod 0755 %{buildroot}%{python3_sitelib}/ansible_collections/ngine_io/cloudstack/scripts/inventory/cloudstack.py


%check
%if %{with tests}
# TODO: Run tests
%endif


%files
%license COPYING
%license %{_licensedir}/ansible/ansible_collections/
%doc README.rst PKG-INFO porting_guide_*.rst CHANGELOG-v*.rst
%doc %{_pkgdocdir}/ansible_collections/
%{_bindir}/ansible-community
# Note (dmsimard): This ansible package installs collections to the python sitelib to mirror the UX
# when installing the ansible package from PyPi.
# This allows users to install individual collections manually with ansible-galaxy (~/.ansible/collections/ansible_collections)
# or via standalone distribution packages to datadir (/usr/share).
# Both will have precedence over the collections installed in the python sitelib.
%{python3_sitelib}/ansible_collections/
%{python3_sitelib}/ansible-%{uversion}.dist-info/


%changelog
* Thu Dec 11 2025 Maxwell G <maxwell@gtmx.me> - 11.13.0-1
- Update to 11.13.0.

* Mon Nov 17 2025 Packit <hello@packit.dev> - 11.12.0-1
- Update to version 11.12.0

* Sat Sep 27 2025 Maxwell G <maxwell@gtmx.me> - 11.10.0-1
- Update to 11.10.0.

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 11.8.0-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 11.8.0-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Maxwell G <maxwell@gtmx.me> - 11.8.0-1
- Update to 11.8.0.

* Sat Jun 07 2025 Python Maint <python-maint@redhat.com> - 11.6.0-2
- Rebuilt for Python 3.14

* Sat Jun 07 2025 Maxwell G <maxwell@gtmx.me> - 11.6.0-1
- Update to 11.6.0.

* Tue Mar 25 2025 Packit <hello@packit.dev> - 11.4.0-1
- Update to version 11.4.0
- Resolves: rhbz#2354912

* Mon Mar 17 2025 Packit <hello@packit.dev> - 11.3.0-1
- Update to version 11.3.0

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 18 2024 Maxwell G <maxwell@gtmx.me> - 11.1.0-1
- Update to 11.1.0.

* Tue Nov 26 2024 Maxwell G <maxwell@gtmx.me> - 11.0.0-1
- Update to 11.0.0.

* Fri Oct 11 2024 Maxwell G <maxwell@gtmx.me> - 9.11.0-1
- Update to 9.11.0.

* Tue Sep 10 2024 Maxwell G <maxwell@gtmx.me> - 9.10.0-1
- Update to 9.10.0.

* Tue Aug 13 2024 Maxwell G <maxwell@gtmx.me> - 9.9.0-1
- Update to 9.9.0.

* Fri Jul 19 2024 Maxwell G <maxwell@gtmx.me> - 9.8.0-1
- Update to 9.8.0.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 23 2024 Maxwell G <maxwell@gtmx.me> - 9.7.0-1
- Update to 9.7.0.

* Sun Jun 09 2024 Maxwell G <maxwell@gtmx.me> - 9.6.1-1
- Update to 8.6.1.

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 9.6.0-2
- Rebuilt for Python 3.13

* Tue Jun 04 2024 Maxwell G <maxwell@gtmx.me> - 9.6.0-1
- Update to 9.6.0.

* Thu May 02 2024 Maxwell G <maxwell@gtmx.me> - 9.5.1-1
- Update to 9.5.1.

* Fri Mar 29 2024 Maxwell G <maxwell@gtmx.me> - 9.4.0-1
- Update to 9.4.0.

* Sat Mar 02 2024 Maxwell G <maxwell@gtmx.me> - 9.3.0-1
- Update to 9.3.0.
- Backport "podman pod info" patch to containers.podman

* Thu Feb 01 2024 Maxwell G <maxwell@gtmx.me> - 9.2.0-1
- Update to 9.2.0.

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Maxwell G <maxwell@gtmx.me> - 9.1.0-1
- Update to 9.1.0.

* Tue Nov 21 2023 Maxwell G <maxwell@gtmx.me> - 9.0.1-1
- Update to 9.0.1.

* Thu Oct 19 2023 Maxwell G <maxwell@gtmx.me> - 9.0.0~a3-1
- Update to 9.0.0~a3.

* Thu Oct 12 2023 Maxwell G <maxwell@gtmx.me> - 9.0.0~a2-1
- Update to 9.0.0~a2.

* Thu Sep 28 2023 Maxwell G <maxwell@gtmx.me> - 9.0.0~a1-1
- Update to 9.0.0~a1.

* Tue Sep 12 2023 Maxwell G <maxwell@gtmx.me> - 8.4.0-1
- Update to 8.4.0.

* Thu Aug 17 2023 Maxwell G <maxwell@gtmx.me> - 8.3.0-1
- Update to 8.3.0.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 03 2023 Maxwell G <maxwell@gtmx.me> - 8.1.0-2
- Rebuilt for Python 3.12

* Thu Jun 22 2023 Maxwell G <maxwell@gtmx.me> - 8.1.0-1
- Update to 8.1.0.

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 8.0.0-2
- Rebuilt for Python 3.12

* Tue May 30 2023 Maxwell G <maxwell@gtmx.me> - 8.0.0-1
- Update to 8.0.0.

* Tue May 23 2023 Maxwell G <maxwell@gtmx.me> - 8.0.0~rc1-1
- Update to 8.0.0~rc1.

* Tue May 16 2023 Maxwell G <maxwell@gtmx.me> - 8.0.0~b1-1
- Update to 8.0.0~b1.

* Wed May 03 2023 Maxwell G <maxwell@gtmx.me> - 8.0.0~a3-1
- Update to 8.0.0~a3.

* Thu Apr 27 2023 Maxwell G <maxwell@gtmx.me> - 8.0.0~a2-1
- Update to 8.0.0~a2.

* Thu Apr 20 2023 Maxwell G <maxwell@gtmx.me> - 8.0.0~a1-1
- Update to 8.0.0~a1.

* Wed Mar 29 2023 Maxwell G <maxwell@gtmx.me> - 7.4.0-1
- Update to 7.4.0.

* Wed Mar 01 2023 Maxwell G <maxwell@gtmx.me> - 7.3.0-1
- Update to 7.3.0.

* Tue Jan 31 2023 David Moreau-Simard <moi@dmsimard.com> - 7.2.0-1
- Update to 7.2.0.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 Maxwell G <gotmax@e.email> - 7.1.0-1
- Update to 7.1.0.

* Wed Nov 23 2022 Maxwell G <gotmax@e.email> - 7.0.0-1
- Update to 7.0.0.

* Fri Nov 18 2022 Maxwell G <gotmax@e.email> - 7.0.0~rc1-1
- Update to 7.0.0~rc1.

* Tue Nov 08 2022 Maxwell G <gotmax@e.email> - 7.0.0~b1-1
- Update to 7.0.0~b1.

* Fri Oct 28 2022 Maxwell G <gotmax@e.email> - 7.0.0~a2-1
- Update to 7.0.0~a2.

* Thu Oct 13 2022 Maxwell G <gotmax@e.email> - 6.5.0-1
- Update to 6.5.0.

* Thu Sep 15 2022 Maxwell G <gotmax@e.email> - 6.4.0-1
- Update to 6.4.0.

* Tue Aug 23 2022 Maxwell G <gotmax@e.email> - 6.3.0-1
- Update to 6.3.0.

* Tue Aug 02 2022 Maxwell G <gotmax@e.email> - 6.2.0-1
- Update to 6.2.0.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 6.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 15 2022 Maxwell G <gotmax@e.email> - 6.1.0-2
- Fix FTI (rhbz#2107532).

* Thu Jul 14 2022 Maxwell G <gotmax@e.email> - 6.1.0-1
- Update to 6.1.0.

* Wed Jun 22 2022 Maxwell G <gotmax@e.email> - 6.0.0-1
- Update to 6.0.0.

* Wed Jun 22 2022 Maxwell G <gotmax@e.email> - 6.0.0~rc1-1
- Update to 6.0.0~rc1.
- Stop duplicating docs and licenses.
- Don't remove tests in %%prep that are now handled by setup.py.
- Hardlink duplicated files and fix rpmlint errors

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 5.9.0-2
- Rebuilt for Python 3.11

* Wed Jun 08 2022 Maxwell G <gotmax@e.email> - 5.9.0-1
- Update to 5.9.0.

* Thu May 19 2022 Maxwell G <gotmax@e.email> - 5.8.0-1
- Update to 5.8.0.
- Remove fortinet.fortios patch.

* Wed Apr 27 2022 Maxwell G <gotmax@e.email> - 5.7.0-1
- Update to 5.7.0.
- Fix SyntaxError in fortinet.fortios collection.
- Fix rpmlint errors

* Mon Apr 25 2022 Maxwell G <gotmax@e.email> - 5.6.0-2
- Ensure correct version of ansible-core is available at buildtime.
- Implement support for epel8.

* Wed Apr 06 2022 Kevin Fenzi <kevin@scrye.com> - 5.6.0-1
- Update to 5.6.0.

* Tue Mar 15 2022 David Moreau-Simard <moi@dmsimard.com> - 5.5.0-1
- Update to latest upstream release

* Tue Feb 22 2022 David Moreau-Simard <moi@dmsimard.com> - 5.4.0-1
- Update to latest upstream release

* Wed Feb 16 2022 Maxwell G <gotmax@e.email> - 5.3.0-2
- Fix shebangs.

* Tue Feb 1 2022 David Moreau-Simard <moi@dmsimard.com> - 5.3.0-1
- Update to latest upstream release

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 12 2022 David Moreau-Simard <moi@dmsimard.com> - 5.2.0-1
- Update to latest upstream release

* Tue Jan 11 2022 David Moreau-Simard <moi@dmsimard.com> - 5.1.0-1
- Update to latest upstream release
- Refactor to take into account split from ansible-core after ansible 2.9, see: https://fedoraproject.org/wiki/Changes/Ansible5
- Remove patches intended for Ansible 2.9
- Removed packaging macros (soon included in ansible-packaging, see rhbz#2038591)
- Removed provides/obsoletes on ansible-python3

* Mon Nov 01 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.27-2
- Add patch for oracle linux Fixes rhbz#2018369

* Mon Oct 11 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.27-1
- Update to 2.9.27. Fixes rhbz#2012918

* Tue Sep 14 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.26-1
- Update to 2.9.26. Fixes rhbz#2002394

* Fri Aug 20 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.25-1
- Update to 2.9.25. Fixes rhbz#1994108

* Sun Jul 25 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.24-1
- Update to 2.9.24. Fixes rhbz#1983837

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jul 10 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.23-2
- Fix FTBFS with sphinx 4.x. Fixes rhbz#1977303

* Tue Jun 22 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.23-1
- Update to 2.9.23. Fixes rhbz#1974592
- Add patch for Rocky Linux. Fixes rhbz#1968728

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.9.22-2
- Rebuilt for Python 3.10

* Mon May 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.22-1
- Update to 2.9.22. Fixes rhbz#1964173

* Mon May 03 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.21-1
- Update to 2.9.21. Fixes rhbz#1956584

* Sat Apr 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.20-1
- Update to 2.9.20.

* Sat Feb 20 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.18-1
- Update to 2.9.18.
- Fixes: CVE-2021-20228 CVE-2021-20178 CVE-2021-20180 CVE-2021-20191

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.17-2
- Update to 2.9.17.

* Sat Jan 16 2021 Kevin Fenzi <kevin@scrye.com> - 2.9.16-2
- Conflict with ansible-base 2.10.x for now.
- Ajust generator so collections will install/work with either ansible or ansible-base.

* Tue Dec 15 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.16-1
- Update to 2.9.16.

* Tue Nov 03 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.15-1
- Update to 2.9.15.

* Tue Oct 06 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.14-1
- Update to 2.9.14.

* Tue Sep 01 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.13-1
- Update to 2.9.13. Fixes CVE-2020-14365

* Tue Aug 11 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.12-1
- Update to 2.9.12.

* Sun Aug 09 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.11-4
- Add support for generating '>=' dependencies in RPM generator

* Sat Aug 08 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.11-3
- Add very basic support for generating dependencies in RPM generator

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 21 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.11-1
- Update to 2.9.11.

* Thu Jun 18 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.10-1
- Update to 2.9.10.

* Fri May 29 2020 Charalampos Stratakis <cstratak@redhat.com> - 2.9.9-3
- Fix Python 3.9 compatibility (#1808674)
- Pin Pytest to version 4 for now

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 2.9.9-2
- Rebuilt for Python 3.9

* Tue May 12 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.9-1
- Update to 2.9.9. Fixes bug #1834582
- Fixes gathering facts on f32+ bug #1832625

* Sun Apr 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.7-3
- Own /usr/share/ansible/collections/ansible_collections

* Sun Apr 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.9.7-2
- Add macros for packaging Ansible collections

* Fri Apr 17 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.7-1
- Update to 2.9.7.
- fixes CVE-2020-1733 CVE-2020-1735 CVE-2020-1740 CVE-2020-1746 CVE-2020-1753 CVE-2020-10684 CVE-2020-10685 CVE-2020-10691
- Drop the -s from the shebang to allow ansible to use locally installed modules.

* Fri Mar 06 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.6-1
- Update to 2.9.6. Fixes bug #1810373
- fixes for CVE-2020-1737, CVE-2020-1739

* Thu Feb 13 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.5-1
- Update to 2.9.5. Fixes bug #1802725

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.4-1
- Update to 2.9.4 with one bugfix.

* Thu Jan 16 2020 Kevin Fenzi <kevin@scrye.com> - 2.9.3-1
- Update to 2.9.3.

* Sun Dec 08 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.2-1
- Update to 2.9.2.

* Thu Nov 14 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.1-2
- Add Requires for python3-pyyaml

* Wed Nov 13 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.1-1
- Update to 2.9.1.

* Fri Nov 08 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.0-2
- Supress pwsh requires added by rpm.

* Thu Oct 31 2019 Kevin Fenzi <kevin@scrye.com> - 2.9.0-1
- Update to 2.9.0.

* Thu Oct 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.6-1
- Update to 2.8.6.
- Rework spec file to drop old conditionals.

* Thu Oct 10 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.5-2
- Make python3-paramiko and python3-winrm Recommended so they install on Fedora and not RHEL8

* Fri Sep 13 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.5-1
- Update to 2.8.5.

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 2.8.4-2
- Rebuilt for Python 3.8

* Fri Aug 16 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.4-1
- Update to 2.8.4. Fixes CVE-2019-10217 and CVE-2019-10206

* Thu Jul 25 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.3-1
- Update to 2.8.3.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 03 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.2-1
- Update to 2.8.2. Fixes bug #1726846

* Sun Jun 09 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.1-1
- Update to 2.8.1. Fixes bug #1718131
- Sync up Requires/Buildrequires with upstream.
- Add patch for python 3.8 building. Fixes bug #1712531
- Add patch for CVE-2019-10156.

* Fri May 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-2
- Fixes for various releases build/test issues.

* Fri May 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-1
- Update to 2.8.0 final.
- Add datadirs for other packages to land ansible files in.

* Fri May 10 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.4rc3
- Update to 2.8.0 rc3.

* Thu May 02 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.3rc2
- Update to 2.8.0 rc2.

* Fri Apr 26 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.2rc1
- Update to 2.8.0 rc1.

* Mon Apr 22 2019 Kevin Fenzi <kevin@scrye.com> - 2.8.0-0.1b
- Update to 2.8.0 beta 1.

* Thu Apr 04 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.10-1
- Update to 2.7.10. Fixes bug #1696379

* Thu Mar 14 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.9-1
- Update to 2.7.9. Fixes bug #1688974

* Thu Feb 21 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.8-1
- Update to 2.7.8. Fixes bug #1679787
- Fix for CVE-2019-3828

* Thu Feb 07 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.7-1
- Update to 2.7.7. Fixes bug #1673761

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 17 2019 Kevin Fenzi <kevin@scrye.com> - 2.7.6-1
- Update to 2.7.6.

* Thu Dec 13 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.5-1
- Update to 2.7.5

* Mon Dec 03 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.4-1
- Update to 2.7.4

* Thu Nov 29 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.3-1
- Update to 2.7.3

* Thu Nov 15 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.2-1
- Update to 2.7.2.

* Mon Oct 29 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.1-1
- Update to 2.7.1.

* Thu Oct 04 2018 Kevin Fenzi <kevin@scrye.com> - 2.7.0-1
- Update to 2.7.0

* Fri Sep 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.5-1
- Update to 2.6.5.

* Fri Sep 07 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.4-1
- Update to 2.6.4.

* Thu Aug 16 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.3-1
- Upgrade to 2.6.3.

* Sat Jul 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.2-1
- Update to 2.6.2. Fixes bug #1609486

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.1-1
- Update to 2.6.1. Fixes bug #1598602
- Fixes CVE-2018-10874 and CVE-2018-10875

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 2.6.0-2
- Rebuilt for Python 3.7

* Thu Jun 28 2018 Kevin Fenzi <kevin@scrye.com> - 2.6.0-1
- Update to 2.6.0. Fixes bug #1596424

* Tue Jun 26 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.5-5
- Rebuilt for Python 3.7

* Mon Jun 25 2018 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.5.5-4
- Upstream patch to build docs with older jinja2 (Fedora 27)
- Build changes to build only rst docs for modules and plugins when a distro
  doesn't have modern enough packages to build the documentation. (EPEL7)

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 2.5.5-3
- Rebuilt for Python 3.7

* Fri Jun 15 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.5-2
- Stop building docs on F27 as python-jinja2 is too old there.

* Thu Jun 14 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.5-1
- Update to 2.5.5. Fixes bug #1580530 and #1584927
- Fixes 1588855,1590200 (fedora) and 1588855,1590199 (epel)
  CVE-2018-10855 (security bug with no_log handling)

* Thu May 31 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.4-1
- Update to 2.5.4. Fixes bug #1584927

* Thu May 17 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.3-1
- Update to 2.5.3. Fixes bug #1579577 and #1574221

* Thu Apr 26 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.2-1
- Update to 2.5.2 with bugfixes.

* Wed Apr 18 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.1-1
- Update to 2.5.1 with bugfixes. Fixes: #1569270 #1569153 #1566004 #1566001

* Tue Mar 27 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.0-2
- Some additional python3 fixes. Thanks churchyard!

* Sat Mar 24 2018 Kevin Fenzi <kevin@scrye.com> - 2.5.0-1
- Update to 2.5.0. Fixes bug #1559852
- Spec changes/improvements with tests, docs, and conditionals.

* Fri Mar 16 2018 Miro Hrončok <mhroncok@redhat.com> - 2.4.3.0-3
- Don't build and ship Python 2 bits on EL > 7 and Fedora > 29

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Kevin Fenzi <kevin@scrye.com> - 2.4.3.0-1
- Update to 2.4.3. See https://github.com/ansible/ansible/blob/stable-2.4/CHANGELOG.md for full changes.

* Mon Jan 08 2018 Troy Dawson <tdawson@redhat.com> - 2.4.2.0-2
- Update conditional

* Wed Nov 29 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.2.0-1
- Update to 2.4.2. See https://github.com/ansible/ansible/blob/stable-2.4/CHANGELOG.md for full changes.

* Mon Oct 30 2017 Kevin Fenzi kevin@scrye.com - 2.4.1.0-2
- Add PR to conditionalize docs building. Thanks tibbs!
- Fix up el6 patches

* Thu Oct 26 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.1.0-1
- Update to 2.4.1

* Thu Oct 12 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.4.0.0-3
- Fix Python3 subpackage to symlink to the python3 versions of the scripts
  instead of the python2 version

* Mon Sep 25 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.0.0-2
- Rebase rhel6 jinja2 patch.
- Conditionalize jmespath to work around amazon linux issues. Fixes bug #1494640

* Tue Sep 19 2017 Kevin Fenzi <kevin@scrye.com> - 2.4.0.0-1
- Update to 2.4.0.

* Tue Aug 08 2017 Kevin Fenzi <kevin@scrye.com> - 2.3.2.0-1
- Update to 2.3.2. Fixes bugs #1471017 #1461116 #1465586

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 01 2017 Kevin Fenzi <kevin@scrye.com> - 2.3.1.0-1
- Update to 2.3.1.0.

* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 2.3.0.0-3
- Update backported patch to the one actually merged upstream

* Wed Apr 19 2017 James Hogarth <james.hogarth@gmail.com> - 2.3.0.0-2
- Backport hotfix to fix ansible-galaxy regression https://github.com/ansible/ansible/issues/22572

* Wed Apr 12 2017 Toshio Kuratomi <toshio@fedoraproject.org> - 2.3.0.0-1
- Update to 2.3.0
- Remove upstreamed patches
- Remove controlpersist socket path path as a custom solution was included
  upstream
- Run the unittests from the upstream tarball now instead of having to download
  separately
- Build a documentation subpackage

* Tue Mar 28 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-3
- Deal with RHEL7 pytest vs python-pytest.
- Rebase epel6 newer jinja patch.
- Conditionalize exclude for RHEL6 rpm.

* Tue Mar 28 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-2
- Conditionalize python3 files for epel builds.

* Tue Mar 28 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-1
- 2.2.2.0 final
- Add new patch to fix unittests

* Mon Mar 27 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.4.rc1
- Add python-crypto and python3-crypto as explicit requirements

* Mon Mar 27 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.3.rc1
- Add a symlink for ansible executables to be accessed via python major version
  (ie: ansible-3) in addition to python-major-minor (ansible-3.6)

* Wed Mar  8 2017 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.2.0-0.2.rc1
- Add a python3 ansible package.  Note that upstream doesn't intend for the library
  to be used by third parties so this is really just for the executables.  It's not
  strictly required that the executables be built for both python2 and python3 but
  we do need to get testing of the python3 version to know if it's stable enough to
  go into the next Fedora.  We also want the python2 version available in case a user
  has to get something done and the python3 version is too buggy.
- Fix Ansible cli scripts to handle appended python version

* Wed Feb 22 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.2.0-0.1.rc1
- Update to 2.2.2.0 rc1. Fixes bug #1421485

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 16 2017 Kevin Fenzi <kevin@scrye.com> - 2.2.1.0-1
- Update to 2.2.1.
- Fixes: CVE-2016-9587 CVE-2016-8647 CVE-2016-9587 CVE-2016-8647
- Fixes bug #1405110

* Wed Nov 09 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-3
- Update unit tests that will skip docker related tests if docker isn't available.
- Drop docker BuildRequires. Fixes bug #1392918

* Fri Nov  4 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.2.0.0-3
- Fix for dnf group install

* Tue Nov 01 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-2
- Fix some BuildRequires to work on all branches.

* Tue Nov 01 2016 Kevin Fenzi <kevin@scrye.com> - 2.2.0.0-1
- Update to 2.2.0. Fixes #1390564 #1388531 #1387621 #1381538 #1388113 #1390646 #1388038 #1390650
- Fixes for CVE-2016-8628 CVE-2016-8614 CVE-2016-8628 CVE-2016-8614

* Thu Sep 29 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.2.0-1
- Update to 2.1.2

* Thu Jul 28 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.1.0-1
- Update to 2.1.1

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.0.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Wed Jun 15 2016 Matt Domsch <matt@domsch.com> - 2.1.0.0-2
- Force python 2.6 on EL6

* Wed May 25 2016 Kevin Fenzi <kevin@scrye.com> - 2.1.0.0-1
- Update to 2.1.0.0.
- Fixes: 1334097 1337474 1332233 1336266

* Tue Apr 19 2016 Kevin Fenzi <kevin@scrye.com> - 2.0.2.0-1
- Update to 2.0.2.0. https://github.com/ansible/ansible/blob/stable-2.0/CHANGELOG.md
- Fixes CVE-2016-3096
- Fix for failed to resolve remote temporary directory issue. bug #1328359

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-2
- Patch control_path to be not hit path length limitations (RH BZ #1311729)
- Version the test tarball

* Thu Feb 25 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.1.0-1
- Update to upstream bugfix for 2.0.x release series.

* Thu Feb  4 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-3
- Utilize the python-jinja26 package on EPEL6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jan 14 2016 Toshio Kuratomi <toshio@fedoraproject.org> - - 2.0.0.2-1
- Ansible 2.0.0.2 release from upstream.  (Minor bugfix to one callback plugin
  API).

* Tue Jan 12 2016 Toshio Kuratomi <toshio@fedoraproject.org> - 2.0.0.1-1
- Ansible 2.0.0.1 from upstream.  Rewrite with many bugfixes, rewritten code,
  and new features. See the upstream changelog for details:
  https://github.com/ansible/ansible/blob/devel/CHANGELOG.md

* Wed Oct 14 2015 Adam Williamson <awilliam@redhat.com> - 1.9.4-2
- backport upstream fix for GH #2043 (crash when pulling Docker images)

* Fri Oct 09 2015 Kevin Fenzi <kevin@scrye.com> 1.9.4-1
- Update to 1.9.4

* Sun Oct 04 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-3
- Backport dnf module from head. Fixes bug #1267018

* Tue Sep  8 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.3-2
- Pull in patch for yum module that fixes state=latest issue

* Thu Sep 03 2015 Kevin Fenzi <kevin@scrye.com> 1.9.3-1
- Update to 1.9.3
- Patch dnf as package manager. Fixes bug #1258080
- Fixes bug #1251392 (in 1.9.3 release)
- Add requires for sshpass package. Fixes bug #1258799

* Thu Jun 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.2-1
- Update to 1.9.2

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.9.1-2
- Fix for dnf

* Tue Apr 28 2015 Kevin Fenzi <kevin@scrye.com> 1.9.1-1
- Update to 1.9.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-2
- Drop upstreamed epel6 patches.

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0.1-1
- Update to 1.9.0.1

* Wed Mar 25 2015 Kevin Fenzi <kevin@scrye.com> 1.9.0-1
- Update to 1.9.0

* Thu Feb 19 2015 Kevin Fenzi <kevin@scrye.com> 1.8.4-1
- Update to 1.8.4

* Tue Feb 17 2015 Kevin Fenzi <kevin@scrye.com> 1.8.3-1
- Update to 1.8.3

* Sun Jan 11 2015 Toshio Kuratomi <toshio@fedoraproject.org> - 1.8.2-3
- Work around a bug in python2.6 by using simplejson (applies in EPEL6)

* Wed Dec 17 2014 Michael Scherer <misc@zarb.org> 1.8.2-2
- precreate /etc/ansible/roles and /usr/share/ansible_plugins

* Sun Dec 07 2014 Kevin Fenzi <kevin@scrye.com> 1.8.2-1
- Update to 1.8.2

* Thu Nov 27 2014 Kevin Fenzi <kevin@scrye.com> 1.8.1-1
- Update to 1.8.1

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-2
- Rebase el6 patch

* Tue Nov 25 2014 Kevin Fenzi <kevin@scrye.com> 1.8-1
- Update to 1.8

* Thu Oct  9 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.7.2-2
- Add /usr/bin/ansible to the rhel6 newer pycrypto patch

* Wed Sep 24 2014 Kevin Fenzi <kevin@scrye.com> 1.7.2-1
- Update to 1.7.2

* Thu Aug 14 2014 Kevin Fenzi <kevin@scrye.com> 1.7.1-1
- Update to 1.7.1

* Wed Aug 06 2014 Kevin Fenzi <kevin@scrye.com> 1.7-1
- Update to 1.7

* Fri Jul 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.10-1
- Update to 1.6.10

* Thu Jul 24 2014 Kevin Fenzi <kevin@scrye.com> 1.6.9-1
- Update to 1.6.9 with more shell quoting fixes.

* Tue Jul 22 2014 Kevin Fenzi <kevin@scrye.com> 1.6.8-1
- Update to 1.6.8 with fixes for shell quoting from previous release.
- Fixes bugs #1122060 #1122061 #1122062

* Mon Jul 21 2014 Kevin Fenzi <kevin@scrye.com> 1.6.7-1
- Update to 1.6.7
- Fixes CVE-2014-4966 and CVE-2014-4967

* Tue Jul 01 2014 Kevin Fenzi <kevin@scrye.com> 1.6.6-1
- Update to 1.6.6

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.5-1
- Update to 1.6.5

* Wed Jun 25 2014 Kevin Fenzi <kevin@scrye.com> 1.6.4-1
- Update to 1.6.4

* Mon Jun 09 2014 Kevin Fenzi <kevin@scrye.com> 1.6.3-1
- Update to 1.6.3

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 1.6.2-1
- Update to 1.6.2 release

* Wed May  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6.1-1
- Bugfix 1.6.1 release

* Mon May  5 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.6-1
- Update to 1.6
- Drop accelerate fix, merged upstream
- Refresh RHEL6 pycrypto patch.  It was half-merged upstream.

* Fri Apr 18 2014 Kevin Fenzi <kevin@scrye.com> 1.5.5-1
- Update to 1.5.5

* Mon Apr  7 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-2
- Fix setuptools requirement to apply to rhel=6, not rhel<6

* Wed Apr  2 2014 Toshio Kuratomi <toshio@fedoraproject.org> - 1.5.4-1
- Update to 1.5.4
- Add upstream patch to fix accelerator mode
- Merge fedora and el6 spec files

* Fri Mar 14 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-2
- Update to NEW 1.5.3 upstream release.
- Add missing dependency on python-setuptools (el6 build)

* Thu Mar 13 2014 Kevin Fenzi <kevin@scrye.com> 1.5.3-1
- Update to 1.5.3
- Fix ansible-vault for newer python-crypto dependency (el6 build)

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-2
- Update to redone 1.5.2 release

* Tue Mar 11 2014 Kevin Fenzi <kevin@scrye.com> 1.5.2-1
- Update to 1.5.2

* Mon Mar 10 2014 Kevin Fenzi <kevin@scrye.com> 1.5.1-1
- Update to 1.5.1

* Fri Feb 28 2014 Kevin Fenzi <kevin@scrye.com> 1.5-1
- Update to 1.5

* Wed Feb 12 2014 Kevin Fenzi <kevin@scrye.com> 1.4.5-1
- Update to 1.4.5

* Sat Dec 28 2013 Kevin Fenzi <kevin@scrye.com> 1.4.3-1
- Update to 1.4.3 with ansible galaxy commands.
- Adds python-httplib2 to requires

* Wed Nov 27 2013 Kevin Fenzi <kevin@scrye.com> 1.4.1-1
- Update to upstream 1.4.1 bugfix release

* Thu Nov 21 2013 Kevin Fenzi <kevin@scrye.com> 1.4-1
- Update to 1.4

* Tue Oct 29 2013 Kevin Fenzi <kevin@scrye.com> 1.3.4-1
- Update to 1.3.4

* Tue Oct 08 2013 Kevin Fenzi <kevin@scrye.com> 1.3.3-1
- Update to 1.3.3

* Thu Sep 19 2013 Kevin Fenzi <kevin@scrye.com> 1.3.2-1
- Update to 1.3.2 with minor upstream fixes

* Mon Sep 16 2013 Kevin Fenzi <kevin@scrye.com> 1.3.1-1
- Update to 1.3.1

* Sat Sep 14 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-2
- Merge upstream spec changes to support EPEL5
- (Still needs python26-keyczar and deps added to EPEL)

* Thu Sep 12 2013 Kevin Fenzi <kevin@scrye.com> 1.3.0-1
- Update to 1.3.0
- Drop node-fireball subpackage entirely.
- Obsolete/provide fireball subpackage.
- Add Requires python-keyczar on main package for accelerated mode.

* Wed Aug 21 2013 Kevin Fenzi <kevin@scrye.com> 1.2.3-2
- Update to 1.2.3
- Fixes CVE-2013-4260 and CVE-2013-4259

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 06 2013 Kevin Fenzi <kevin@scrye.com> 1.2.2-1
- Update to 1.2.2 with minor fixes

* Fri Jul 05 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-2
- Update to newer upstream re-release to fix a syntax error

* Thu Jul 04 2013 Kevin Fenzi <kevin@scrye.com> 1.2.1-1
- Update to 1.2.1
- Fixes CVE-2013-2233

* Mon Jun 10 2013 Kevin Fenzi <kevin@scrye.com> 1.2-1
- Update to 1.2

* Tue Apr 02 2013 Kevin Fenzi <kevin@scrye.com> 1.1-1
- Update to 1.1

* Mon Mar 18 2013 Kevin Fenzi <kevin@scrye.com> 1.0-1
- Update to 1.0

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.9-0
- Release 0.9

* Fri Oct 19 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.8-0
- Release of 0.8

* Thu Aug 9 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.7-0
- Release of 0.7

* Mon Aug 6 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.6-0
- Release of 0.6

* Wed Jul 4 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.5-0
- Release of 0.5

* Wed May 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.4-0
- Release of 0.4

* Mon Apr 23 2012 Michael DeHaan <michael.dehaan@gmail.com> - 0.3-1
- Release of 0.3

* Tue Apr  3 2012 John Eckersberg <jeckersb@redhat.com> - 0.0.2-1
- Release of 0.0.2

* Sat Mar 10 2012  <tbielawa@redhat.com> - 0.0.1-1
- Release of 0.0.1
