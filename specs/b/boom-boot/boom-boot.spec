# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global summary A set of libraries and tools for managing boot loader entries
%global sphinx_docs 1

Name:		boom-boot
Version:	1.6.8
Release:	2%{?dist}
Summary:	%{summary}

License:	Apache-2.0
URL:		https://github.com/snapshotmanager/boom-boot
Source0:	%{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	make
BuildRequires:	python3-devel
%if 0%{?rhel} && 0%{?rhel} < 11
BuildRequires:	python3-setuptools
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif
BuildRequires:  python3-pytest
%if 0%{?sphinx_docs}
BuildRequires:	python3-dbus
BuildRequires:	python3-sphinx
%endif
BuildRequires: make

Requires: python3-boom = %{version}-%{release}
Requires: %{name}-conf = %{version}-%{release}
Requires: python3-dbus
%if 0%{?rhel} == 9
Requires: systemd >= 252-18
%else
Requires: systemd >= 254
%endif

Obsoletes: boom-boot-grub2 <= 1.3
# boom-grub2 was not an official name of subpackage in fedora, but was used upstream:
Obsoletes: boom-grub2 <= 1.3

%package -n python3-boom
Summary: %{summary}
%{?python_provide:%python_provide python3-boom}
Requires: %{__python3}
Recommends: (lvm2 or brtfs-progs)
Recommends: %{name}-conf = %{version}-%{release}

# There used to be a boom package in fedora, and there is boom packaged in
# copr. How to tell which one is installed? We need python3-boom and no boom
# only.
Conflicts: boom

%package conf
Summary: %{summary}

%description
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

%description -n python3-boom
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides python3 boom module.

%description conf
Boom is a boot manager for Linux systems using boot loaders that support
the BootLoader Specification for boot entry configuration.

Boom requires a BLS compatible boot loader to function: either the
systemd-boot project, or Grub2 with the BLS patch (Red Hat Grub2 builds
include this support in both Red Hat Enterprise Linux 7 and Fedora).

This package provides configuration files for boom.

%prep
%autosetup -p1 -n %{name}-%{version}

%if 0%{?fedora} || 0%{?rhel} >= 11
%generate_buildrequires
%pyproject_buildrequires
%endif

%build
%if 0%{?sphinx_docs}
make %{?_smp_mflags} -C doc html
rm doc/_build/html/.buildinfo
mv doc/_build/html doc/html
rm -r doc/_build
%endif

%if 0%{?rhel} && 0%{?rhel} < 11
%py3_build
%else
%pyproject_wheel
%endif

%install
%if 0%{?rhel} && 0%{?rhel} < 11
%py3_install
%else
%pyproject_install
%endif

# Make configuration directories
# mode 0700 - in line with /boot/grub2 directory:
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/profiles
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/hosts
install -d -m 700 ${RPM_BUILD_ROOT}/boot/loader/entries
install -d -m 700 ${RPM_BUILD_ROOT}/boot/boom/cache
install -m 644 examples/boom.conf ${RPM_BUILD_ROOT}/boot/boom

mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man5
install -m 644 man/man8/boom.8 ${RPM_BUILD_ROOT}/%{_mandir}/man8
install -m 644 man/man5/boom.5 ${RPM_BUILD_ROOT}/%{_mandir}/man5

rm doc/Makefile
rm doc/conf.py

%check
pytest-3 --log-level=debug -v

%files
%license LICENSE
%doc README.md
%{_bindir}/boom
%doc %{_mandir}/man*/boom.*

%files -n python3-boom
%license LICENSE
%doc README.md
%{python3_sitelib}/boom/*
%if 0%{?rhel} && 0%{?rhel} < 11
%{python3_sitelib}/boom*.egg-info/
%else
%{python3_sitelib}/boom*.dist-info/
%endif
%doc doc
%doc examples
%doc tests

%files conf
%license LICENSE
%doc README.md
%dir /boot/boom
%config(noreplace) /boot/boom/boom.conf
%dir /boot/boom/profiles
%dir /boot/boom/hosts
%dir /boot/boom/cache
%dir /boot/loader/entries


%changelog
* Fri Oct 31 2025 Bryn M. Reeves <bmr@redhat.com> - 1.6.8-2
- Update tmt configuration to be version agnostic
- Update to release 1.6.8.

* Mon Sep 22 2025 Bryn M. Reeves <bmr@redhat.com> - 1.6.6-6
- Rebuilt for rhbz#2396678

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 1.6.6-6
- Rebuilt for Python 3.14.0rc3 bytecode

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 1.6.6-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 1.6.6-3
- Rebuilt for Python 3.14

* Tue Apr 01 2025 Bryn M. Reeves <bmr@redhat.com> - 1.6.6-2.fc43
- Rebuilt to verify new gating configuration

* Mon Mar 31 2025 Bryn M. Reeves <bmr@redhat.com> - 1.6.6-1
- tests: drop remaining Python2 compat handling
- boom.config: drop Python2 compat handling for ConfigParser
- dist: update example boom.conf
- boom: use correct option names in BoomConfig.__str__()
- boom: use write_boom_config() in boom.command.create_config()
- config: add missing [cache] section to boom.config.__make_config()
- config: add missing [cache] section handling to boom.config._sync_config()
- config: treat {boom,boot}_root and {boom,boot}_path as synonyms
- dist: enable check in boom-boot.spec
- dist: replace license classifier with SPDX expressions
- boom: replace __make_map_key() function with dictionary comprehension
- dist: clean up copyright statements and convert to SPDX license headers
- dist: update GPLv2 text in COPYING
- boom: use lazy printf formatting when logging
- boom: fix report argument formatting
- tests: drop separate coverage runs and split out reporting step
- tests: switch Fedora tests to fedora:latest
- tests: bracket test cases with log messages
- tests: fix duplicate log handlers in test suite
- report: strip trailing whitespace from report output
- legacy: use 'is' instead of explicit type comparison
- boom: clean up new OsProfile if setting uname_pattern fails
- boom: add CentOS Stream to uname heuristics table
- boom: fix license headers across tree
- dist: update spec file changelog and release
- dist: drop unused systemd-rpm-macros BuildRequires
- dist: fix Source URL and autosetup invocation

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Sep 18 2024 Bryan Gurney <bgurney@redhat.com> - 1.6.5-1
- Update to release 1.6.5.

* Fri Jul 26 2024 Bryn M. Reeves <bmr@redhat.com> - 1.6.4-1
* Update to release 1.6.4.

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jun 18 2024 Bryan Gurney <bgurney@redhat.com> - 1.6.3-1
- Update to release 1.6.3.

* Fri Jun 07 2024 Python Maint <python-maint@redhat.com> - 1.6.2-2
- Rebuilt for Python 3.13

* Thu May 30 2024 Bryan Gurney <bgurney@redhat.com> - 1.6.2-1
- Update to release 1.6.2.

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 21 2023 Marian Csontos <mcsontos@redhat.com> - 1.6.0-1
- Update to release 1.6.0.

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 15 2023 Python Maint <python-maint@redhat.com> - 1.5.1-2
- Rebuilt for Python 3.12

* Tue May 16 2023 Marian Csontos <mcsontos@redhat.com> - 1.5.1-1
- Update to release 1.5.1.

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jul 13 2022 Marian Csontos <mcsontos@redhat.com> 1.4-1
- Update to release 1.4.

* Mon Jun 13 2022 Python Maint <python-maint@redhat.com> - 1.3-5
- Rebuilt for Python 3.11

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.3-2
- Rebuilt for Python 3.10

* Fri Jan 29 2021 Marian Csontos <mcsontos@redhat.com> 1.3-1
- Update to release 1.3.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sun Jun 07 2020 Marian Csontos <mcsontos@redhat.com> 1.2-1
- Update to bug fix release 1.2.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1-4
- Rebuilt for Python 3.9

* Tue May 26 2020 Marian Csontos <mcsontos@redhat.com> 1.1-3
- Fix unicode entries handling.
- Add tracebacks when --debug is used.

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.1-2
- Rebuilt for Python 3.9

* Thu May 14 2020 Marian Csontos <mcsontos@redhat.com> 1.1-1
- Update to new upstream release 1.1.
- Add caching of kernel and init ramdisk images.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Marian Csontos <mcsontos@redhat.com> 1.0-1
- Update to new upstream release 1.0.

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-0.5.20190329git6ff3e08
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.0-0.4.20190329git6ff3e08
- Rebuilt for Python 3.8

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-0.3.20190329git6ff3e08
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 09 2019 Marian Csontos <mcsontos@redhat.com> 1.0-0.2.20190329git6ff3e08
- Fix packaging issues.

* Thu May 09 2019 Marian Csontos <mcsontos@redhat.com> 1.0-0.1.20190329git6ff3e08
- Pre-release of new version.

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 17 2018 Marian Csontos <mcsontos@redhat.com> 0.9-4
- Change dependencies.

* Mon Jul 16 2018 Marian Csontos <mcsontos@redhat.com> 0.9-3
- Split executable, python module and configuration.

* Wed Jun 27 2018 Marian Csontos <mcsontos@redhat.com> 0.9-2
- Spin off grub2 into subpackage

* Wed Jun 27 2018 Marian Csontos <mcsontos@redhat.com> 0.9-1
- Update to new upstream 0.9.
- Fix boot_id caching.

* Fri Jun 08 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6.2
- Remove example files from /boot/boom/profiles.

* Fri May 11 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6.1
- Files in /boot are treated as configuration files.

* Thu Apr 26 2018 Marian Csontos <mcsontos@redhat.com> 0.8.5-6
- Package upstream version 0.8-5.6

