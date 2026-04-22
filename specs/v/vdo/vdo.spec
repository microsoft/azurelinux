# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Management tools for Virtual Data Optimizer
Name: vdo
Version: 8.3.0.73
Release: 3%{?dist}

License: GPL-2.0-only
URL: https://github.com/dm-vdo/vdo
Source0: %{url}/archive/%{version}/%{name}-%{version}.tar.gz

%if 0%{?fedora}
ExcludeArch: %{ix86}
%endif
BuildRequires: device-mapper-devel
BuildRequires: device-mapper-event-devel
BuildRequires: gcc
BuildRequires: libblkid-devel
BuildRequires: libuuid-devel
BuildRequires: make
%ifarch %{valgrind_arches}
BuildRequires: valgrind-devel
%endif
BuildRequires: zlib-devel

# Disable an automatic dependency due to a file in examples/monitor.
%global __requires_exclude perl
%if 0%{?rhel}
%global bash_completions_dir %{_datadir}/bash-completion/completions
%endif

%description
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.

This package provides the user-space management tools for VDO.

%package support
Summary: Support tools for Virtual Data Optimizer
License: GPL-2.0-only

Requires: libuuid >= 2.23

%description support
Virtual Data Optimizer (VDO) is a device mapper target that delivers
block-level deduplication, compression, and thin provisioning.

This package provides the user-space support tools for VDO.

%prep
%autosetup -p1

%build
%make_build VDO_VERSION=%{version}

%install
%make_install INSTALLOWNER= name=%{name} bindir=%{_bindir} \
   mandir=%{_mandir} defaultdocdir=%{_defaultdocdir} libexecdir=%{_libexecdir} \
   presetdir=%{_presetdir} python3_sitelib=/%{python3_sitelib} \
   sysconfdir=%{_sysconfdir} unitdir=%{_unitdir}

%files
%license COPYING
%{_bindir}/vdoforcerebuild
%{_bindir}/vdoformat
%{_bindir}/vdostats
%{bash_completions_dir}/vdostats
%dir %{_defaultdocdir}/%{name}
%dir %{_defaultdocdir}/%{name}/examples
%dir %{_defaultdocdir}/%{name}/examples/monitor
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_logicalSpace.pl
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_physicalSpace.pl
%doc %{_defaultdocdir}/%{name}/examples/monitor/monitor_check_vdostats_savingPercent.pl
%{_mandir}/man8/vdoforcerebuild.8*
%{_mandir}/man8/vdoformat.8*
%{_mandir}/man8/vdostats.8*

%files support
%license COPYING
%{_bindir}/adaptlvm
%{_bindir}/vdoaudit
%{_bindir}/vdodebugmetadata
%{_bindir}/vdodumpblockmap
%{_bindir}/vdodumpmetadata
%{_bindir}/vdolistmetadata
%{_bindir}/vdoreadonly
%{_bindir}/vdorecover
%{_mandir}/man8/adaptlvm.8*
%{_mandir}/man8/vdoaudit.8*
%{_mandir}/man8/vdodebugmetadata.8*
%{_mandir}/man8/vdodumpblockmap.8*
%{_mandir}/man8/vdodumpmetadata.8*
%{_mandir}/man8/vdolistmetadata.8*
%{_mandir}/man8/vdoreadonly.8*
%{_mandir}/man8/vdorecover.8*

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 30 2025 - Chung Chung <cchung@redhat.com> - 8.3.0.73-1
- Update to 8.3.0.73 (rhbz#2342887)

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0.72-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Oct 17 2024 - Chung Chung <cchung@redhat.com> - 8.3.0.72-1
- Update to 8.3.0.72 (rhbz#2319335)

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.3.0.71-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 09 2024 - Susan LeGendre-McGhee <slegendr@redhat.com> - 8.3.0.71-2
- Unify spec for Fedora/RHEL packaging
 
* Fri Jun 07 2024 - Susan LeGendre-McGhee <slegendr@redhat.com> - 8.3.0.71-1
- Update to 8.3.0.71 (#2290537)
- Modify build command to ensure the version is reported correctly

* Thu May 09 2024 - Susan LeGendre-McGhee <slegendr@redhat.com> - 8.3.0.70-1
- Initial package

