# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# SPDX-License-Identifier: MIT
# Copyright (C) Fedora Project Authors
# License Text: https://spdx.org/licenses/MIT.html

# several test dependencies are unwanted in RHEL
%bcond tests %{undefined rhel}

# controls whether to generate shell completions
# may be useful for bootstrapping purposes
%bcond argcomplete 1

# disable the python -s shbang flag as we want to be able to find non system modules
%undefine _py3_shebang_s

Name:           ansible-core
Version:        2.18.12
%global uversion %{version_no_tilde %{quote:%nil}}
Release:        1%{?dist}
Summary:        A radically simple IT automation system

# The main license is GPLv3+. Many of the files in lib/ansible/module_utils
# are BSD licensed. There are various files scattered throughout the codebase
# containing code under different licenses.
License:        GPL-3.0-or-later AND BSD-2-Clause AND PSF-2.0 AND MIT AND Apache-2.0
URL:            https://ansible.com

Source0:        https://github.com/ansible/ansible/archive/v%{uversion}/%{name}-%{uversion}.tar.gz
Source1:        https://github.com/ansible/ansible-documentation/archive/v%{uversion}/ansible-documentation-%{uversion}.tar.gz

# dnf5,apt: add auto_install_module_deps option (#84292)
# https://github.com/ansible/ansible/pull/84292.patch
# https://bugzilla.redhat.com/2322751
Patch:          0001-dnf5-apt-add-auto_install_module_deps-option-84292.patch
# Initial support for Python 3.14
# Downstream patch. See comments in patch file.
# https://bugzilla.redhat.com/2366307
Patch:          0002-Initial-support-for-Python-3.14.patch

BuildArch:      noarch

# Virtual provides for bundled libraries
# Search for `_BUNDLED_METADATA` to find them

# lib/ansible/module_utils/distro/*
# SPDX-License-Identifier: Apache-2.0
Provides:       bundled(python3dist(distro)) = 1.9.0

# lib/ansible/module_utils/six/*
# SPDX-License-Identifier: MIT
Provides:       bundled(python3dist(six)) = 1.16.0

Conflicts:      ansible <= 2.9.99
#
# obsoletes/provides for ansible-base
#
Provides:       ansible-base = %{version}-%{release}
Obsoletes:      ansible-base < 2.10.6-1

BuildRequires:  make
BuildRequires:  python%{python3_pkgversion}-devel
# This is only used in %%prep to relax the required setuptools version,
# which is not necessary in RHEL 10+.
# Not using it in RHEL avoids unwanted dependencies.
%if %{undefined rhel}
BuildRequires:  tomcli >= 0.3.0
%endif
# Needed to build manpages from source.
BuildRequires:  python%{python3_pkgversion}-docutils

%if %{with tests}
BuildRequires:  git-core
BuildRequires:  glibc-all-langpacks
BuildRequires:  python%{python3_pkgversion}-systemd
%endif

%if %{with argcomplete}
Requires:       python%{python3_pkgversion}-argcomplete
%endif
%if 0%{?fedora} >= 39
BuildRequires:  python3-libdnf5
Recommends:     python3-libdnf5
%endif


%global _description %{expand:
Ansible is a radically simple model-driven configuration management,
multi-node deployment, and remote task execution system. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.}

%description %_description

This is the base part of ansible (the engine).

%package doc
Summary:        Documentation for Ansible Core
Provides:       ansible-base-doc = %{version}-%{release}
Obsoletes:      ansible-base-doc < 2.10.6-1

%description doc %_description

This package installs extensive documentation for ansible-core


%prep
%autosetup -p1 -n ansible-%{uversion} -a1
# Relax setuptools constraint on Fedora
# Future RHELs have new enough setuptools
%if %{undefined rhel}
tomcli-set pyproject.toml lists replace \
    'build-system.requires' 'setuptools >=.*' 'setuptools'
%endif

sed -i -s 's|/usr/bin/env python|%{python3}|' \
    bin/ansible-test \
    test/lib/ansible_test/_util/target/cli/ansible_test_cli_stub.py


# TODO: Investigate why hostname is the only module that still has a shebang
# and file an upstream issue if needed.
sed -i -e '1{\@^#!.*@d}' lib/ansible/modules/hostname.py

sed '/^mock$/d' test/lib/ansible_test/_data/requirements/units.txt > _requirements.txt


%generate_buildrequires
%pyproject_buildrequires %{?with_tests:_requirements.txt test/units/requirements.txt}
%if %{with argcomplete}
# Shell completions
echo 'python%{python3_pkgversion}-argcomplete'
%endif


%build
%pyproject_wheel

# Build manpages
mkdir -p docs/man/man1
%{python3} packaging/cli-doc/build.py man --output-dir docs/man/man1


%if %{with argcomplete}
# Build shell completions
(
    cd bin
    for shell in bash fish; do
        mkdir -p "../${shell}_completions"
        for bin in *; do
            if grep -q PYTHON_ARGCOMPLETE_OK "${bin}"; then
                case "${shell}" in
                    bash)
                        format="${bin}"
                        ;;
                    fish)
                        format="${bin}.${shell}"
                        ;;
                esac
                register-python-argcomplete --shell "${shell}" "${bin}" > "../${shell}_completions/${format}"
            else
                echo "Skipped generating completions for ${bin}"
            fi
        done
    done
)
%endif


%install
%pyproject_install
%pyproject_save_files ansible ansible_test

# These files are executable when they shouldn't be.
# Only the actual "binaries" in %%{_bindir} need to be executable
# and have shebangs.
while read -r file; do
    sed -i -e '1{\@^#!.*@d}' "${file}"
done < <(find \
    %{buildroot}%{python3_sitelib}/ansible/cli/*.py \
    %{buildroot}%{python3_sitelib}/ansible/cli/scripts/ansible_connection_cli_stub.py \
        -type f ! -executable)

%if %{with argcomplete}
install -Dpm 0644 bash_completions/* -t %{buildroot}%{bash_completions_dir}
install -Dpm 0644 fish_completions/* -t %{buildroot}%{fish_completions_dir}
%endif

# Create system directories that Ansible defines as default locations in
# ansible/config/base.yml
DATADIR_LOCATIONS='%{_datadir}/ansible/collections
%{_datadir}/ansible/collections/ansible_collections
%{_datadir}/ansible/plugins/doc_fragments
%{_datadir}/ansible/plugins/action
%{_datadir}/ansible/plugins/become
%{_datadir}/ansible/plugins/cache
%{_datadir}/ansible/plugins/callback
%{_datadir}/ansible/plugins/cliconf
%{_datadir}/ansible/plugins/connection
%{_datadir}/ansible/plugins/filter
%{_datadir}/ansible/plugins/httpapi
%{_datadir}/ansible/plugins/inventory
%{_datadir}/ansible/plugins/lookup
%{_datadir}/ansible/plugins/modules
%{_datadir}/ansible/plugins/module_utils
%{_datadir}/ansible/plugins/netconf
%{_datadir}/ansible/roles
%{_datadir}/ansible/plugins/strategy
%{_datadir}/ansible/plugins/terminal
%{_datadir}/ansible/plugins/test
%{_datadir}/ansible/plugins/vars'

UPSTREAM_DATADIR_LOCATIONS=$(grep -ri default lib/ansible/config/base.yml| tr ':' '\n' | grep '/usr/share/ansible')

if [ "$SYSTEM_LOCATIONS" != "$UPSTREAM_SYSTEM_LOCATIONS" ] ; then
  echo "The upstream Ansible datadir locations have changed.  Spec file needs to be updated"
  exit 1
fi

mkdir -p %{buildroot}%{_datadir}/ansible/plugins/
for location in $DATADIR_LOCATIONS ; do
    mkdir %{buildroot}"$location"
done
mkdir -p %{buildroot}%{_sysconfdir}/ansible/
mkdir -p %{buildroot}%{_sysconfdir}/ansible/roles/

cp ansible-documentation-%{uversion}/examples/hosts %{buildroot}/etc/ansible/
cp ansible-documentation-%{uversion}/examples/ansible.cfg %{buildroot}/etc/ansible/
mkdir -p %{buildroot}/%{_mandir}/man1
cp -v docs/man/man1/*.1 %{buildroot}/%{_mandir}/man1/

# We install licenses in this manner so we don't miss new licenses:
  # 1. Copy all files in licenses to %%{_pkglicensedir}.
  # 2. List the files explicitly in %%files.
  # 3. The build will fail with unpackaged file errors if license
  #    files aren't accounted for.
%global _pkglicensedir %{_licensedir}/ansible-core
install -Dpm 0644 licenses/* -t %{buildroot}%{_pkglicensedir}

%check
%if %{with tests}
%{python3} bin/ansible-test \
    units --local --python-interpreter %{python3} -vv
%endif


%files -f %{pyproject_files}
%license COPYING
%license %{_pkglicensedir}/{Apache-License,MIT-license,PSF-license,simplified_bsd}.txt
%doc README.md changelogs/CHANGELOG-v2.1?.rst
%dir %{_sysconfdir}/ansible/
%config(noreplace) %{_sysconfdir}/ansible/*
%{_bindir}/ansible*
%{_datadir}/ansible/
%if %{with argcomplete}
%{bash_completions_dir}/ansible*
%{fish_completions_dir}/ansible*.fish
%endif
%{_mandir}/man1/ansible*

%files doc
%doc ansible-documentation-%{uversion}/docs/docsite/rst
%if %{with docs}
%doc ansible-documentation-%{uversion}/docs/docsite/_build/html
%endif


%changelog
* Thu Dec 11 2025 Maxwell G <maxwell@gtmx.me> - 2.18.12-1
- Update to 2.18.12.

* Mon Nov 17 2025 Packit <hello@packit.dev> - 2.18.11-1
- Update to version 2.18.11

* Sat Sep 27 2025 Maxwell G <maxwell@gtmx.me> - 2.18.9-1
- Update to 2.18.9.

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 2.18.7-4
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 2.18.7-3
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Maxwell G <maxwell@gtmx.me> - 2.18.7-1
- Update to 2.18.7. Fixes rhbz#2380244.

* Sat Jun 07 2025 Maxwell G <maxwell@gtmx.me> - 2.18.6-2
- Add initial support for Python 3.14 (rhbz#2366307)

* Sat Jun 07 2025 Maxwell G <maxwell@gtmx.me> - 2.18.6-1
- Update to 2.18.6. Fixes rhbz#2354908.

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 2.18.4-2
- Rebuilt for Python 3.14

* Tue Mar 25 2025 Packit <hello@packit.dev> - 2.18.4-1
- Update to version 2.18.4
- Resolves: rhbz#2354908

* Mon Mar 17 2025 Packit <hello@packit.dev> - 2.18.3-1
- Update to version 2.18.3
- Resolves: rhbz#2342365

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Dec 04 2024 Maxwell G <maxwell@gtmx.me> - 2.18.1-1
- Update to 2.18.1. Fixes rhbz#2330005.
- dnf5 - backport support for automatically installing python3-libdnf5 (rhbz#2322751).

* Tue Nov 26 2024 Maxwell G <maxwell@gtmx.me> - 2.18.0-1
- Update to 2.18.0. Fixes rhbz#2282011.

* Fri Oct 11 2024 Maxwell G <maxwell@gtmx.me> - 2.16.12-1
- Update to 2.16.12.

* Tue Sep 10 2024 Maxwell G <maxwell@gtmx.me> - 2.16.11-1
- Update to 2.16.11.

* Tue Aug 13 2024 Maxwell G <maxwell@gtmx.me> - 2.16.10-1
- Update to 2.16.10.

* Fri Jul 19 2024 Maxwell G <maxwell@gtmx.me> - 2.16.9-1
- Update to 2.16.9.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jun 23 2024 Maxwell G <maxwell@gtmx.me> - 2.16.8-1
- Update to 2.16.8.

* Sun Jun 09 2024 Python Maint <python-maint@redhat.com> - 2.16.7-2
- Rebuilt for Python 3.13

* Tue Jun 04 2024 Maxwell G <maxwell@gtmx.me> - 2.16.7-1
- Update to 2.16.7.

* Thu May 23 2024 Miro Hrončok <mhroncok@redhat.com> - 2.16.6-2
- Fix build with Python 3.13

* Tue Apr 16 2024 Maxwell G <maxwell@gtmx.me> - 2.16.6-1
- Update to 2.16.6. Fixes rhbz#2261507.

* Fri Mar 29 2024 Maxwell G <maxwell@gtmx.me> - 2.16.5-1
- Update to 2.16.5. Fixes rhbz#2261507.

* Fri Mar 29 2024 Maxwell G <maxwell@gtmx.me> - 2.16.5-1
- Update to 2.16.5.

* Sat Mar 02 2024 Maxwell G <maxwell@gtmx.me> - 2.16.4-1
- Update to 2.16.4. Fixes rhbz#2261507.

* Thu Feb 01 2024 Maxwell G <maxwell@gtmx.me> - 2.16.3-1
- Update to 2.16.3. Fixes rhbz#2261507.

* Mon Jan 22 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Maxwell G <maxwell@gtmx.me> - 2.16.2-2
- Mitigate CVE-2024-0690.

* Mon Dec 11 2023 Maxwell G <maxwell@gtmx.me> - 2.16.2-1
- Update to 2.16.2. Fixes rhbz#2254093.

* Wed Dec 06 2023 Maxwell G <maxwell@gtmx.me> - 2.16.1-1
- Update to 2.16.1. Fixes rhbz#2252860.

* Fri Nov 10 2023 Maxwell G <maxwell@gtmx.me> - 2.16.0-1
- Update to 2.16.0. Fixes rhbz#2248187.

* Thu Oct 19 2023 Maxwell G <maxwell@gtmx.me> - 2.16.0~rc1-1
- Update to 2.16.0~rc1.

* Tue Oct 03 2023 Maxwell G <maxwell@gtmx.me> - 2.16.0~b2-1
- Update to 2.16.0~b2.

* Mon Oct 02 2023 Miro Hrončok <mhroncok@redhat.com> - 2.16.0~b1-2
- Do not use tomcli in Fedora ELN, avoid pulling unwanted dependencies

* Wed Sep 27 2023 Maxwell G <maxwell@gtmx.me> - 2.16.0~b1-1
- Update to 2.16.0~b1.

* Tue Sep 26 2023 Kevin Fenzi <kevin@scrye.com> - 2.15.4-2
- Add patch to fix readfp with python-3.12. Fixes rhbz#2239728

* Mon Sep 11 2023 Maxwell G <maxwell@gtmx.me> - 2.15.4-1
- Update to 2.15.4. Fixes rhbz#2238445.

* Thu Aug 17 2023 Maxwell G <maxwell@gtmx.me> - 2.15.3-1
- Update to 2.15.3. Fixes rhbz#2231963.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.15.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 18 2023 Maxwell G <maxwell@gtmx.me> - 2.15.2-1
- Update to 2.15.2. Fixes rhbz#2223469.
- Use the docs sources from https://github.com/ansible/ansible-documentation.

* Mon Jul 03 2023 Maxwell G <maxwell@gtmx.me> - 2.15.1-2
- Rebuilt for Python 3.12

* Thu Jun 22 2023 Maxwell G <maxwell@gtmx.me> - 2.15.1-1
- Update to 2.15.1. Fixes rhbz#2204492.
- Add Recommends on python3-libdnf5 for Fedora 39

* Sat Jun 17 2023 Maxwell G <maxwell@gtmx.me> - 2.15.0-5
- Add patch to avoid importlib.abc.TraversableResources DeprecationWarning

* Fri Jun 16 2023 Python Maint <python-maint@redhat.com> - 2.15.0-4
- Rebuilt for Python 3.12

* Tue Jun 13 2023 Maxwell G <maxwell@gtmx.me> - 2.15.0-3
- Add support for Python 3.12. Fixes rhbz#2196539.
- Remove conditional Requires on ansible-packaging.

* Tue May 23 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 2.15.0-2
- Disable tests in RHEL builds

* Tue May 16 2023 Maxwell G <maxwell@gtmx.me> - 2.15.0-1
- Update to 2.15.0.
- Don't remove dotfiles and empty files. ansible-core actually needs these.

* Wed May 03 2023 Maxwell G <maxwell@gtmx.me> - 2.15.0~rc2-1
- Update to 2.15.0~rc2.

* Thu Apr 27 2023 Maxwell G <maxwell@gtmx.me> - 2.15.0~rc1-1
- Update to 2.15.0~rc1.

* Mon Apr 24 2023 Maxwell G <maxwell@gtmx.me> - 2.15.0~b3-1
- Update to 2.15.0~b3.
- Account for the removed Makefile

* Mon Apr 24 2023 Maxwell G <maxwell@gtmx.me> - 2.14.4-2
- Add gating

* Wed Mar 29 2023 Maxwell G <maxwell@gtmx.me> - 2.14.4-1
- Update to 2.14.4. Fixes rhbz#2173765.

* Wed Mar 01 2023 Maxwell G <maxwell@gtmx.me> - 2.14.3-1
- Update to 2.14.3.

* Tue Jan 31 2023 David Moreau-Simard <moi@dmsimard.com> - 2.14.2-1
- Update to 2.14.2. Fixes rhbz#2165629.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.14.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 09 2022 Maxwell G <gotmax@e.email> - 2.14.1-1
- Update to 2.14.1.

* Mon Nov 07 2022 Maxwell G <gotmax@e.email> - 2.14.0-1
- Update to 2.14.0.

* Wed Nov 02 2022 Maxwell G <gotmax@e.email> - 2.14.0~rc2-1
- Update to 2.14.0~rc2.

* Fri Oct 28 2022 Maxwell G <gotmax@e.email> - 2.14.0~rc1-1
- Update to 2.14.0~rc1.

* Wed Oct 12 2022 Maxwell G <gotmax@e.email> - 2.13.5-1
- Update to 2.13.5.

* Tue Sep 13 2022 Maxwell G <gotmax@e.email> - 2.13.4-1
- Update to 2.13.4.

* Wed Aug 31 2022 Maxwell G <gotmax@e.email> - 2.13.3-2
- Remove weak deps on paramiko and winrm

* Mon Aug 15 2022 Maxwell G <gotmax@e.email> - 2.13.3-1
- Update to 2.13.3.

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.13.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jul 19 2022 Maxwell G <gotmax@e.email> - 2.13.2-1
- Update to 2.13.2. Fixes rhbz#2108195.

* Thu Jul 07 2022 Miro Hrončok <mhroncok@redhat.com> - 2.13.1-2
- Don't put -- into Python shebangs

* Wed Jun 22 2022 Maxwell G <gotmax@e.email> - 2.13.1-1
- Update to 2.13.1 (rhbz#2096312).

* Thu Jun 16 2022 Maxwell G <gotmax@e.email> - 2.13.0-1
- Update to 2.13.0.
- Re-enable tests that work with newer pytest
- Patch out python3-mock
- Manually build manpages to workaround upstream issue.
- Remove unneeded BRs and switch to pyproject-rpm-macros.
- Make ansible-base* Obsoletes/Provides compliant with Packaging Guidelines
- Remove python3-jmespath dependency. json_query is part of community.general.
- Correct licensing
- Generate shell completions

* Thu Jun 16 2022 Python Maint <python-maint@redhat.com> - 2.12.6-2
- Rebuilt for Python 3.11

* Tue May 24 2022 Maxwell G <gotmax@e.email> - 2.12.6-1
- Update to 2.12.6.

* Wed Apr 27 2022 Maxwell G <gotmax@e.email> - 2.12.5-1
- Update to 2.12.5. Fixes rhbz#2078558.

* Sat Apr 02 2022 Maxwell G <gotmax@e.email> - 2.12.4-1
- Update to 2.12.4. Fixes rhbz#2069384.

* Thu Mar 10 2022 Maxwell G <gotmax@e.email> - 2.12.3-2
- Add patch to fix failing tests and FTBFS with Pytest 7.
- Resolves: rhbz#2059937

* Tue Mar 01 2022 Kevin Fenzi <kevin@scrye.com> - 2.12.3-1
- Update to 2.12.3. Fixes rhbz#2059284

* Mon Jan 31 2022 Kevin Fenzi <kevin@scrye.com> - 2.12.2-1
- Update to 2.12.2. Fixes rhbz#2048795

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jan 13 2022 Neal Gompa <ngompa@fedoraproject.org> - 2.12.1-3
- Split out packaging macros and generators to ansible-packaging

* Wed Dec 08 2021 Kevin Fenzi <kevin@scrye.com> - 2.12.1-2
- Re-enable tests

* Tue Dec 07 2021 Kevin Fenzi <kevin@scrye.com> - 2.12.1-1
- Update to 2.12.1. Fixes rhbz#2029598

* Mon Nov 08 2021 Kevin Fenzi <kevin@scrye.com> - 2.12.0-1
- Update to 2.12.0. Fixes rhbz#2022533

* Thu Oct 14 2021 Maxwell G <gotmax@e.email> - 2.11.6-1
- Update to 2.11.6.

* Tue Sep 14 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.5-1
- Update to 2.11.5. Fixes rhbz#2002393

* Thu Aug 19 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.4-1
- Update to 2.11.4. Fixes rhbz#1994107

* Sun Jul 25 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.3-1
- Update to 2.11.3. Fixes rhbz#1983836

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.11.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 22 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.2-1
- Update to 2.11.2. Fixed rhbz#1974593

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 2.11.1-2
- Rebuilt for Python 3.10

* Mon May 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.1-1
- Update to 2.11.1. Fixes rhbz#1964172

* Tue Apr 27 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.0-1
- Update to 2.11.0 final.

* Sat Apr 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.0-0.3.rc2
- Update to 2.11.0rc2.

* Sat Apr 03 2021 Kevin Fenzi <kevin@scrye.com> - 2.11.0-0.1.b4
- Rename to ansible-base, update to b4 beta version.

* Sat Feb 20 2021 Kevin Fenzi <kevin@scrye.com> - 2.10.6-1
- Update to 2.10.6.
- Fixes CVE-2021-20228

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.10.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Jan 24 2021 Kevin Fenzi <kevin@scrye.com> - 2.10.5-1
- Update to 2.10.5.

* Sat Dec 19 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.4-1
- Update to 2.10.4

* Sat Nov 07 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.3-2
- Various review fixes

* Tue Nov 03 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.3-1
- Update to 2.10.3

* Sat Oct 10 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.2-1
- Update to 2.10.2

* Sat Sep 26 2020 Kevin Fenzi <kevin@scrye.com> - 2.10.1-1
- Initial version for review.

