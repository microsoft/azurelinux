## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 2;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global summary A set of tools for managing snapshots

Name:		snapm
Version:	0.7.0
Release:	%autorelease
Summary:	%{summary}

License:	Apache-2.0
URL:		https://github.com/snapshotmanager/%{name}
Source0:	%{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildArch:	noarch

BuildRequires:	boom-boot
BuildRequires:	lvm2
BuildRequires:	make
BuildRequires:	stratis-cli
BuildRequires:	stratisd
BuildRequires:	systemd-rpm-macros
BuildRequires:	python3-devel
BuildRequires:	python3-sphinx
%if 0%{?fedora}
BuildRequires: libfaketime
%endif

Requires: python3-snapm = %{version}-%{release}
Recommends: boom-boot
Recommends: python3-file-magic

%package -n python3-snapm
Summary: %{summary}

%package -n python3-snapm-doc
Summary: %{summary}

%description
Snapshot manager (snapm) is a tool for managing sets of snapshots on Linux
systems.  The snapm tool allows snapshots of multiple volumes to be captured at
the same time, representing the system state at the time the set was created.

%description -n python3-snapm
Snapshot manager (snapm) is a tool for managing sets of snapshots on Linux
systems.  The snapm tool allows snapshots of multiple volumes to be captured at
the same time, representing the system state at the time the set was created.

This package provides the python3 snapm module.

%description -n python3-snapm-doc
Snapshot manager (snapm) is a tool for managing sets of snapshots on Linux
systems.  The snapm tool allows snapshots of multiple volumes to be captured at
the same time, representing the system state at the time the set was created.

This package provides the python3 snapm module documentation in HTML format.

%prep
%autosetup -p1 -n %{name}-%{version}

%generate_buildrequires
%pyproject_buildrequires

%build
%pyproject_wheel

%{make_build} -C doc html
rm doc/_build/html/.buildinfo
mv doc/_build/html doc/html
rm -rf doc/html/_sources doc/_build
rm -f doc/*.rst doc/Makefile doc/conf.py

%install
%pyproject_install

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/plugins.d
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/schedule.d
%{__install} -p -m 644 etc/%{name}/snapm.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}
%{__install} -p -m 644 etc/%{name}/plugins.d/lvm2-cow.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/plugins.d
%{__install} -p -m 644 etc/%{name}/plugins.d/lvm2-thin.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/plugins.d
%{__install} -p -m 644 etc/%{name}/plugins.d/stratis.conf ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{name}/plugins.d

mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man8
mkdir -p ${RPM_BUILD_ROOT}/%{_mandir}/man5
%{__install} -p -m 644 man/man8/snapm.8 ${RPM_BUILD_ROOT}/%{_mandir}/man8
%{__install} -p -m 644 man/man5/snapm.conf.5 ${RPM_BUILD_ROOT}/%{_mandir}/man5
%{__install} -p -m 644 man/man5/snapm-plugins.d.5 ${RPM_BUILD_ROOT}/%{_mandir}/man5
%{__install} -p -m 644 man/man5/snapm-schedule.d.5 ${RPM_BUILD_ROOT}/%{_mandir}/man5

mkdir -p ${RPM_BUILD_ROOT}/%{_unitdir}
%{__install} -p -m 644 systemd/snapm-create@.service ${RPM_BUILD_ROOT}/%{_unitdir}
%{__install} -p -m 644 systemd/snapm-create@.timer ${RPM_BUILD_ROOT}/%{_unitdir}
%{__install} -p -m 644 systemd/snapm-gc@.service ${RPM_BUILD_ROOT}/%{_unitdir}
%{__install} -p -m 644 systemd/snapm-gc@.timer ${RPM_BUILD_ROOT}/%{_unitdir}

mkdir -p ${RPM_BUILD_ROOT}/%{_tmpfilesdir}
%{__install} -p -m 644 systemd/tmpfiles.d/%{name}.conf ${RPM_BUILD_ROOT}/%{_tmpfilesdir}/

%{__install} -d -m 0700 ${RPM_BUILD_ROOT}/%{_rundir}/%{name}
%{__install} -d -m 0700 ${RPM_BUILD_ROOT}/%{_rundir}/%{name}/mounts
%{__install} -d -m 0700 ${RPM_BUILD_ROOT}/%{_rundir}/%{name}/lock

%check
%pytest --log-level=debug -v tests/

%files
# Main license for snapm (Apache-2.0)
%license LICENSE
%doc README.md
%{_bindir}/snapm
%doc %{_mandir}/man*/snapm*
%attr(644, -, -) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/snapm.conf
%attr(644, -, -) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/plugins.d/*
%dir %attr(755, -, -) %{_sysconfdir}/%{name}/schedule.d
%attr(644, -, -) %{_unitdir}/snapm-create@.service
%attr(644, -, -) %{_unitdir}/snapm-create@.timer
%attr(644, -, -) %{_unitdir}/snapm-gc@.service
%attr(644, -, -) %{_unitdir}/snapm-gc@.timer
%attr(644, -, -) %{_tmpfilesdir}/%{name}.conf
%dir %{_rundir}/%{name}/
%dir %{_rundir}/%{name}/mounts
%dir %{_rundir}/%{name}/lock

%files -n python3-snapm
# license for snapm (Apache-2.0)
%license LICENSE
%doc README.md
%{python3_sitelib}/%{name}/
%{python3_sitelib}/%{name}*.dist-info/

%files -n python3-snapm-doc
# license for snapm (Apache-2.0)
%license LICENSE
%doc README.md
%doc doc

%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 0.7.0-2
- Latest state for snapm

* Thu Jan 08 2026 Bryn M. Reeves <bmr@redhat.com> - 0.7.0-1
- Update snapm to upstream version 0.7.0.

* Wed Nov 19 2025 Bryn M. Reeves <bmr@redhat.com> - 0.5.2-3
- Add fix for snapm#606 (timeline index calculation bug)

* Sun Nov 16 2025 Bryn M. Reeves <bmr@redhat.com> - 0.5.2-1
- Update snapm to upstream version 0.5.2.

* Tue Nov 04 2025 Bryn M. Reeves <bmr@redhat.com> - 0.5.1-1
- Update snapm to upstream version 0.5.1.

* Sun Nov 02 2025 Bryn M. Reeves <bmr@redhat.com> - 0.5.0-2
- Increase duration of tests/upstream/main to 90m

* Sun Nov 02 2025 Bryn M. Reeves <bmr@redhat.com> - 0.5.0-1
- Update snapm to upstream version 0.5.0.

* Fri Sep 19 2025 Python Maint <python-maint@redhat.com> - 0.4.3-9
- Rebuilt for Python 3.14.0rc3 bytecode

* Mon Aug 18 2025 Bryn M. Reeves <bmr@redhat.com> - 0.4.3-8
- Ensure SRC_DIR is defined in run-unit-tests.sh

* Mon Aug 18 2025 Bryn M. Reeves <bmr@redhat.com> - 0.4.3-7
- Fix tmt lints and path setting

* Mon Aug 18 2025 Bryn M. Reeves <bmr@redhat.com> - 0.4.3-6
- Increase tests/upstream/main.fmf duration to 30m

* Fri Aug 15 2025 Python Maint <python-maint@redhat.com> - 0.4.3-5
- Rebuilt for Python 3.14.0rc2 bytecode

* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Jun 03 2025 Python Maint <python-maint@redhat.com> - 0.4.3-3
- Rebuilt for Python 3.14

* Wed Apr 30 2025 Bryn M. Reeves <bmr@redhat.com> - 0.4.3-2
- Add TMT tests and enable gating

* Thu Apr 24 2025 Bryn M. Reeves <bmr@redhat.com> - 0.4.3-1
- Initial import (fedora#2357266)
## END: Generated by rpmautospec
