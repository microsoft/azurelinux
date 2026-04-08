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

%global debug_package %{nil}

# container-selinux stuff (prefix with ds_ for version/release etc.)
# Some bits borrowed from the openstack-selinux package
%global moduletype services
%global modulenames container

# Usage: _format var format
# Expand 'modulenames' into various formats as needed
# Format must contain '$x' somewhere to do anything useful
%global _format() export %1=""; for x in %{modulenames}; do %1+=%2; %1+=" "; done;

# RHEL < 10 and Fedora < 40 use file context entries in /var/run
%if %{defined rhel} && 0%{?rhel} < 10 || %{defined fedora} && 0%{?fedora} < 40
%define legacy_var_run 1
%endif

# https://github.com/containers/container-selinux/issues/203
%if %{!defined fedora} && %{!defined rhel} || %{defined rhel} && 0%{?rhel} <= 9
%define no_user_namespace 1
%endif

# set copr_build is more intuitive than copr_username
%if %{defined copr_username} && "%{copr_username}" == "rhcontainerbot" && "%{copr_projectname}" == "podman-next"
%define next_build 1
%endif

Name: container-selinux
# Set different Epoch for rhcontainerbot/podman-next copr build
%if %{defined next_build}
Epoch: 102
%else
Epoch: 4
%endif
# Keep Version in upstream specfile at 0. It will be automatically set
# to the correct value by Packit for copr and koji builds.
# IGNORE this comment if you're looking at it in dist-git.
Version: 2.246.0
Release: %autorelease
License: GPL-2.0-only
URL: https://github.com/containers/%{name}
Summary: SELinux policies for container runtimes
Source0: %{url}/archive/v%{version}.tar.gz
BuildArch: noarch
BuildRequires: make
BuildRequires: git-core
BuildRequires: pkgconfig(systemd)
BuildRequires: selinux-policy >= %_selinux_policy_version
BuildRequires: selinux-policy-devel >= %_selinux_policy_version
# RE: rhbz#1195804 - ensure min NVR for selinux-policy
Requires: selinux-policy >= %_selinux_policy_version
Requires(post): selinux-policy-base >= %_selinux_policy_version
Requires(post): selinux-policy-any >= %_selinux_policy_version
Recommends: selinux-policy-targeted >= %_selinux_policy_version
Requires(post): policycoreutils
Requires(post): libselinux-utils
Requires(post): sed
Obsoletes: %{name} <= 2:1.12.5-13
Obsoletes: docker-selinux <= 2:1.12.4-28
Provides: docker-selinux = %{?epoch:%{epoch}:}%{version}-%{release}
Conflicts: udica < 0.2.6-1
Conflicts: k3s-selinux <= 0.4-1

%description
SELinux policy modules for use with container runtimes.

%prep
%autosetup -Sgit %{name}-%{version}

sed -i 's/^man: install-policy/man:/' Makefile
sed -i 's/^install: man/install:/' Makefile

%if %{defined no_user_namespace}
sed -i '/user_namespace/d' container.te
%endif

%if %{defined legacy_var_run}
sed -i 's|^/run/|/var/run/|' container.fc
%endif

%build
make

%install
# install policy modules
%_format MODULES $x.pp.bz2
%{__make} DATADIR=%{buildroot}%{_datadir} SYSCONFDIR=%{buildroot}%{_sysconfdir} install install.udica-templates install.selinux-user

%pre
%selinux_relabel_pre

%post
# Install all modules in a single transaction
if [ $1 -eq 1 ]; then
   %{_sbindir}/setsebool -P -N virt_use_nfs=1 virt_sandbox_use_all_caps=1
fi
%_format MODULES %{_datadir}/selinux/packages/$x.pp.bz2
. %{_sysconfdir}/selinux/config
%{_sbindir}/semodule -n -s ${SELINUXTYPE} -r container 2> /dev/null
%{_sbindir}/semodule -n -s ${SELINUXTYPE} -d docker 2> /dev/null
%{_sbindir}/semodule -n -s ${SELINUXTYPE} -d gear 2> /dev/null
%selinux_modules_install -s ${SELINUXTYPE} $MODULES
sed -e "\|container_file_t|h; \${x;s|container_file_t||;{g;t};a\\" -e "container_file_t" -e "}" -i /etc/selinux/${SELINUXTYPE}/contexts/customizable_types
matchpathcon -qV %{_sharedstatedir}/containers || restorecon -R %{_sharedstatedir}/containers &> /dev/null || :

%postun
if [ $1 -eq 0 ]; then
   %selinux_modules_uninstall %{modulenames} docker
fi

%posttrans
%selinux_relabel_post

# Empty placeholder check to silence rpmlint
%check

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%doc README.md
%{_datadir}/selinux/*
%dir %{_datadir}/containers/selinux
%{_datadir}/containers/selinux/contexts
%dir %{_datadir}/udica
%dir %{_datadir}/udica/templates/
%{_datadir}/udica/templates/*
# Ref: https://bugzilla.redhat.com/show_bug.cgi?id=2209120
%{_mandir}/man8/container_selinux.8.gz
%{_sysconfdir}/selinux/targeted/contexts/users/container_u
%ghost %verify(not mode) %{_selinux_store_path}/targeted/active/modules/200/%{modulenames}
%ghost %verify(not mode) %{_selinux_store_path}/mls/active/modules/200/%{modulenames}

%triggerpostun -- container-selinux < 2:2.162.1-3
if %{_sbindir}/selinuxenabled ; then
    echo "Fixing Rootless SELinux labels in homedir"
    %{_sbindir}/restorecon -R /home/*/.local/share/containers/storage/overlay*  2> /dev/null
fi

%changelog
## START: Generated by rpmautospec
* Mon Apr 06 2026 azldev <> - 4:2.246.0-2
- Latest state for container-selinux

* Thu Feb 19 2026 Packit <hello@packit.dev> - 4:2.246.0-1
- Update to 2.246.0 upstream release

* Mon Dec 15 2025 Packit <hello@packit.dev> - 4:2.245.0-1
- Update to 2.245.0 upstream release

* Mon Dec 01 2025 Packit <hello@packit.dev> - 4:2.244.0-1
- Update to 2.244.0 upstream release

* Fri Nov 07 2025 Packit <hello@packit.dev> - 4:2.243.0-1
- Update to 2.243.0 upstream release

* Fri Sep 05 2025 Packit <hello@packit.dev> - 4:2.242.0-1
- Update to 2.242.0 upstream release

* Tue Aug 19 2025 Packit <hello@packit.dev> - 4:2.241.0-1
- Update to 2.241.0 upstream release

* Thu Aug 07 2025 Packit <hello@packit.dev> - 4:2.240.0-1
- Update to 2.240.0 upstream release

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4:2.239.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Packit <hello@packit.dev> - 4:2.239.0-1
- Update to 2.239.0 upstream release

* Fri May 30 2025 Packit <hello@packit.dev> - 4:2.238.0-1
- Update to 2.238.0 upstream release

* Mon Apr 28 2025 Packit <hello@packit.dev> - 4:2.237.0-1
- Update to 2.237.0 upstream release

* Thu Mar 13 2025 Packit <hello@packit.dev> - 4:2.236.0-1
- Update to 2.236.0 upstream release

* Mon Feb 24 2025 Lokesh Mandvekar <lsm5@fedoraproject.org> - 4:2.235.0-2
- fix gating.yaml

* Mon Feb 24 2025 Packit <hello@packit.dev> - 4:2.235.0-1
- Update to 2.235.0 upstream release

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.234.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Dec 26 2024 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.234.2-2
- TMT: sync tests with upstream

* Mon Nov 11 2024 Packit <hello@packit.dev> - 2:2.234.2-1
- Update to 2.234.2 upstream release

* Mon Nov 11 2024 Packit <hello@packit.dev> - 2:2.234.1-1
- Update to 2.234.1 upstream release

* Wed Sep 11 2024 Packit <hello@packit.dev> - 2:2.233.0-1
- Update to 2.233.0 upstream release

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.232.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Packit <hello@packit.dev> - 2:2.232.1-1
- Update to 2.232.1 upstream release

* Mon May 27 2024 Lokesh Mandvekar <lsm5@redhat.com> - 2:2.231.0-6
- sync test plans from upstream

* Mon May 20 2024 Lokesh Mandvekar <lsm5@redhat.com> - 2:2.231.0-5
- fix gating.yaml

* Mon May 20 2024 Lokesh Mandvekar <lsm5@redhat.com> - 2:2.231.0-4
- TMT: use fmf to discover tests

* Mon May 20 2024 Lokesh Mandvekar <lsm5@redhat.com> - 2:2.231.0-3
- Reuse TMT tests: remove old STI tests

* Mon May 20 2024 Lokesh Mandvekar <lsm5@redhat.com> - 2:2.231.0-2
- Attempt to use TMT plans

* Wed Apr 24 2024 Packit <hello@packit.dev> - 2:2.231.0-1
- Update to 2.231.0 upstream release
- Resolves: rhbz#2276827

* Sat Mar 02 2024 Packit <hello@packit.dev> - 2:2.230.0-1
- [packit] 2.230.0 upstream release

* Wed Feb 28 2024 Packit <hello@packit.dev> - 2:2.229.1-1
- [packit] 2.229.1 upstream release

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.229.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 22 2024 Packit <hello@packit.dev> - 2:2.229.0-1
- [packit] 2.229.0 upstream release

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.228.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 18 2024 Packit <hello@packit.dev> - 2:2.228.1-1
- [packit] 2.228.1 upstream release

* Thu Jan 11 2024 Packit <hello@packit.dev> - 2:2.228.0-1
- [packit] 2.228.0 upstream release

* Thu Dec 21 2023 Packit <hello@packit.dev> - 2:2.227.0-1
- [packit] 2.227.0 upstream release

* Thu Nov 30 2023 Packit <hello@packit.dev> - 2:2.226.0-1
- [packit] 2.226.0 upstream release

* Wed Oct 11 2023 Packit <hello@packit.dev> - 2:2.224.0-1
- [packit] 2.224.0 upstream release

* Sun Sep 17 2023 Packit <hello@packit.dev> - 2:2.222.0-1
- [packit] 2.222.0 upstream release

* Tue Aug 29 2023 Packit <hello@packit.dev> - 2:2.221.1-1
- [packit] 2.221.1 upstream release

* Tue Aug 15 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.221.0-1
- bump to v2.221.0

* Tue Aug 15 2023 Packit <hello@packit.dev> - 2:2.221-1
- 2.221 upstream release

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.219.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jul 02 2023 Packit <hello@packit.dev> - 2:2.219.0-1
- [packit] 2.219.0 upstream release

* Tue Jun 06 2023 Packit <hello@packit.dev> - 2:2.218.0-1
- [packit] 2.218.0 upstream release

* Mon Jun 05 2023 Packit <hello@packit.dev> - 2:2.217.0-1
- [packit] 2.217.0 upstream release

* Tue May 30 2023 Packit <hello@packit.dev> - 2:2.216.0-1
- [packit] 2.216.0 upstream release

* Tue May 23 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.215.0-2
- [packit] 2.215.0 upstream release

* Mon May 22 2023 Packit <hello@packit.dev> - 2:2.215.0-1
- [packit] 2.215.0 upstream release

* Tue May 16 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.213.0-1
- bump to v2.213.0

* Tue May 02 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.211.1-1
- bump to v2.211.1

* Fri Apr 28 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.211.0-3
- prepare for Packit integration, remove centos conditionals

* Fri Apr 28 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.211.0-2
- fedora spec not used for packit copr-builds

* Sat Apr 22 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.211.0-1
- auto bump to v2.211.0

* Thu Apr 06 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.210.0-1
- auto bump to v2.210.0

* Mon Apr 03 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.209.0-1
- auto bump to v2.209.0

* Fri Mar 31 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.208.0-1
- auto bump to v2.208.0

* Tue Mar 21 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.206.0-1
- auto bump to v2.206.0

* Thu Mar 16 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.205.0-1
- auto bump to v2.205.0

* Mon Mar 13 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.204.0-1
- auto bump to v2.204.0

* Tue Mar 07 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.203.0-1
- auto bump to v2.203.0

* Mon Mar 06 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.202.0-2
- migrated to SPDX license

* Fri Mar 03 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.202.0-1
- auto bump to v2.202.0

* Wed Feb 22 2023 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.201.0-1
- auto bump to v2.201.0

* Fri Feb 10 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.200.0-4
- delete systemd_chat_resolved for centos 8 packit builds

* Fri Feb 10 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.200.0-3
- dummy changelog to make packit centos 8 copr builds happy

* Fri Feb 10 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.200.0-2
- packit: include _selinux_policy_version for centos 8

* Wed Feb 08 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.200.0-1
- bump to v2.200.0

* Tue Jan 31 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.199.0-1
- bump to v2.199.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.198.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jan 06 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.198.0-1
- bump to v2.198.0

* Wed Jan 04 2023 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.197.0-1
- bump to v2.197.0

* Thu Dec 15 2022 Daniel J Walsh <dwalsh@redhat.com> - 2:2.195.1-1
- local build

* Wed Dec 14 2022 Daniel J Walsh <dwalsh@redhat.com> - 2:2.195.0-1
- local build

* Wed Nov 23 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.193.0-1
- bump to v2.193.0

* Mon Oct 31 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.191.0-1
- bump to v2.191.0

* Fri Oct 28 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.190.1-1
- bump to v2.190.1

* Mon Oct 10 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.190.0-2
- update macros to get version correctly

* Tue Sep 13 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.190.0-1
- Bump to v2.190.0

* Wed Aug 17 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.189.0-3
- Use similar macros as other podman-related packages

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.189.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jul 14 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.189.0-1
- auto bump to v2.189.0

* Thu Jun 23 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.188.0-1
- auto bump to v2.188.0

* Fri May 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.187.0-2
- update Version field per changes in rpm autobuilder

* Tue May 24 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.187.0-1
- auto bump to v2.187.0

* Tue May 24 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.186.0-1
- auto bump to v2.186.0

* Wed May 11 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.183.0-4
- empty commit for smooth upgrade path

* Wed May 11 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.183.0-3
- empty commit for smooth upgrade path

* Thu Apr 21 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.183.0-2
- remove unwanted file entries from sources

* Mon Apr 18 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.183.0-1
- auto bump to v2.183.0

* Thu Apr 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.181.0-2
- rebuild

* Fri Mar 25 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.181.0-1
- auto bump to v2.181.0

* Mon Mar 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.180.0-1
- bump to v2.180.0

* Tue Mar 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.179.1-1
- bump to v2.179.1

* Fri Feb 11 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.178.0-1
- bump to v2.178.0

* Wed Feb 09 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.177.0-1
- bump to v2.177.0

* Mon Feb 07 2022 Ed Santiago <santiago@redhat.com> - 2:2.176.0-3
- Use podman in gating tests

* Mon Feb 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.176.0-2
- bump for rebuild

* Mon Feb 07 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.176.0-1
- Revert "local build" - was just a test

* Mon Feb 07 2022 Daniel J Walsh <dwalsh@redhat.com> - 2:2.176.1-1
- local build

* Thu Feb 03 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.176.0-1
- bump to v2.176.0

* Tue Feb 01 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.174.0-1
- bup to v2.174.0

* Thu Jan 27 2022 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.173.2-2
- switch to autospec

* Wed Jan 26 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.173.2-1
- container-selinux-2:2.173.2-1

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.173.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 18 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.173.1-1
- container-selinux-2:2.173.1-1

* Tue Jan 11 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.173.0-1
- container-selinux-2:2.173.0-1

* Thu Jan 06 2022 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.172.1-1
- container-selinux-2:2.172.1-1

* Mon Nov 22 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.172.0-1
- container-selinux-2:2.172.0-1

* Wed Nov 10 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.171.0-1
- container-selinux-2:2.171.0-1

* Fri Oct 15 2021 Daniel J Walsh <dwalsh@redhat.com> - 2:2.170.0-2
- Add conflicts  k3s-selinux <= 0.4-1 to force upgrade

* Tue Oct 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.170.0-1
- container-selinux-2:2.170.0-1

* Fri Sep 24 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.169.0-1
- container-selinux-2:2.169.0-1

* Wed Sep 15 2021 Vit Mojzis <vmojzis@redhat.com> - 2:2.168.0-2
- Start shipping udica policy templates

* Mon Sep 13 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.168.0-1
- container-selinux-2:2.168.0-1

* Fri Sep 10 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.167.0-2
- container-selinux-2:2.167.0-2
- use upstream tag instead of commits, fix autobuild macros

* Thu Aug 26 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.167.0-1
- container-selinux-2:2.167.0-1

* Wed Aug 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.165.1-1
- container-selinux-2:2.165.1-1

* Wed Aug 04 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.164.2-1
- container-selinux-2:2.164.2-1

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.164.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.164.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jul 19 2021 Daniel J Walsh <dwalsh@redhat.com> - 2:2.164.1-2
- Allow spc_t domains to set bpf rules on any domain

* Mon Jul 19 2021 Daniel J Walsh <dwalsh@redhat.com> - 2:2.164.1-1
- bump to 2.163.0 autobuilt 99b40c5

* Sat Jun 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.163.0-1
- container-selinux-2:2.163.0-2.dev.git99b40c5
- bump to 2.163.0
- autobuilt 99b40c5

* Tue May 25 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.162.2-1
- container-selinux-2:2.162.2-2.dev.git61b862a
- bump to 2.162.2
- autobuilt 61b862a

* Mon May 17 2021 Daniel J Walsh <dwalsh@redhat.com> - 2:2.162.1-2
- Fix labels in users homedirs, before overlayfs is supported by default
  for non root users

* Sun May 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.162.1-1
- container-selinux-2:2.162.1-2.dev.git233e620
- bump to 2.162.1
- autobuilt 233e620

* Wed May 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.162.0-1
- container-selinux-2:2.162.0-2.dev.gitda28288
- bump to 2.162.0
- autobuilt da28288

* Fri May 07 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.161.1-1
- container-selinux-2:2.161.1-2.dev.gite1092cd
- bump to 2.161.1
- autobuilt e1092cd

* Thu May 06 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.160.0-1
- Revert "container-selinux-2:2.117.0-2.dev.gitbfde70a"

* Wed Apr 28 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.117.0-1
- container-selinux-2:2.117.0-2.dev.gitbfde70a
- bump to 2.117.0
- autobuilt bfde70a

* Tue Apr 20 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.160.0-2
- container-selinux-2:2.160.0-3.dev.git5a60716
- autobuilt 5a60716

* Wed Mar 31 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.160.0-1
- container-selinux-2:2.160.0-2.dev.gitc9f0cb6
- bump to v2.160.0

* Mon Mar 29 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.159.0-1
- container-selinux-2:2.159.0-2.dev.gitd89a599
- bump to 2.159.0
- autobuilt d89a599

* Wed Feb 17 2021 Daniel J Walsh <dwalsh@redhat.com> - 2:2.158.0-4
- Rebuilt to use latest selinux-policy interfaces

* Tue Feb 16 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.158.0-3
- container-selinux-2:2.158.0-4.dev.gite78ac4f
- autobuilt e78ac4f

* Fri Feb 12 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.158.0-2
- container-selinux-2:2.158.0-3.dev.gitaeb85c4
- autobuilt aeb85c4

* Thu Feb 11 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.158.0-1
- container-selinux-2:2.158.0-2.dev.giteb6dad0
- bump to 2.158.0
- autobuilt eb6dad0

* Mon Feb 08 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.157.0-2
- container-selinux-2:2.157.0-3.dev.git6d13bf9
- autobuilt 6d13bf9

* Tue Feb 02 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.157.0-1
- container-selinux-2:2.157.0-2.dev.gitf330e81
- bump to 2.157.0
- autobuilt f330e81

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.156.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.156.0-1
- container-selinux-2:2.156.0-2.dev.git75f193a
- bump to 2.156.0
- autobuilt 75f193a

* Wed Jan 13 2021 Tom Stellard <tstellar@redhat.com> - 2:2.155.0-4
- Add BuildRequires: make

* Mon Jan 11 2021 Ondrej Mosnacek <omosnace@redhat.com> - 2:2.155.0-3
- Depend on git-core instead of full git

* Mon Jan 11 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.155.0-2
- use built_tag macro to record latest tag

* Tue Jan 05 2021 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.155.0-1
- container-selinux-2:2.155.0-2.dev.git667f0f3
- bump to 2.155.0
- autobuilt 667f0f3

* Wed Dec 30 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.154.0-1
- container-selinux-2:2.154.0-2.dev.git54e2ac5
- bump to 2.154.0
- autobuilt 54e2ac5

* Sat Dec 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.153.0-1
- container-selinux-2:2.153.0-2.dev.git8573f8d
- bump to 2.153.0
- autobuilt 8573f8d

* Tue Dec 22 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:2.152.0-1
- container-selinux-2:2.152.0-2.dev.git1677bc4
- bump to 2.152.0
- autobuilt 1677bc4

* Wed Dec 02 2020 Jindrich Novy <jnovy@redhat.com> - 2:2.151.0-2
- container-selinux-2.151.0-4.dev.git5d3c461.fc34
- remove bogus changelog dates emitted by build bot leading to build
  failure
- Related: #1715412

* Wed Dec 02 2020 Jindrich Novy <jnovy@redhat.com> - 2:2.151.0-1
- container-selinux-2.151.0-3.dev.git5d3c461.fc34
- remove %%%%fedora Epoch conditional
- Related: #1899626

* Thu Nov 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.151.0-1
- container-selinux-2:2.151.0-2.dev.git5d3c461
- bump to 2.151.0
- autobuilt 5d3c461

* Fri Oct 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.150.0-1
- container-selinux-2:2.150.0-2.dev.git0ef4703
- bump to 2.150.0
- autobuilt 0ef4703

* Thu Oct 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.148.0-2
- container-selinux-2:2.148.0-3.dev.git9b3b66f
- autobuilt 9b3b66f

* Wed Oct 14 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.148.0-1
- container-selinux-2:2.148.0-2.dev.git3c361a2
- bump to 2.148.0
- autobuilt 3c361a2

* Mon Oct 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.147.0-1
- container-selinux-2:2.147.0-2.dev.git9fb1698
- bump to 2.147.0
- autobuilt 9fb1698

* Thu Oct 08 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.146.0-1
- container-selinux-2:2.146.0-2.dev.git2908536
- bump to 2.146.0
- autobuilt 2908536

* Thu Sep 10 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.145.0-1
- container-selinux-2:2.145.0-2.dev.git464e922
- bump to 2.145.0
- autobuilt 464e922

* Mon Aug 31 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.144.0-4
- Resolves: #1797554 - use _selinux_policy_version macro

* Fri Aug 28 2020 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2.144.0-3
- container-selinux-2:2.144.0-4.dev.git5d929d4
- Resolves: #1780129 - bump min selinux-policy

* Thu Aug 13 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.144.0-2
- container-selinux-2:2.144.0-3.dev.git5d929d4
- autobuilt 5d929d4

* Wed Aug 12 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.144.0-1
- container-selinux-2:2.144.0-2.dev.git746ea7a
- bump to 2.144.0
- autobuilt 746ea7a

* Wed Aug 05 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.143.0-1
- container-selinux-2:2.143.0-2.dev.gite2d5a9e
- bump to 2.143.0
- autobuilt e2d5a9e

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.142.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.142.0-1
- container-selinux-2:2.142.0-2.dev.gitfe6a25c
- bump to 2.142.0
- autobuilt fe6a25c

* Fri Jul 24 2020 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2.141.0-1
- container-selinux-2:2.141.0-2.dev.git2750e78
- bump to 2.141.0
- autobuilt 2750e78

* Thu Jul 23 2020 Merlin Mathesius <mmathesi@redhat.com> - 2.140.0-202
- Clean up usage of %%{epoch} macro to allow building for ELN

* Thu Jul 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.140.0-2.dev.git965c7fb
- bump to 2.140.0
- autobuilt 965c7fb

* Sat Jul 18 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.139.0-2.dev.git8c26927
- bump to 2.139.0
- autobuilt 8c26927

* Thu Jul 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.138.0-2.dev.git9884317
- bump to 2.138.0
- autobuilt 9884317

* Thu Jun 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.137.0-2.dev.git6b721da
- bump to 2.137.0
- autobuilt 6b721da

* Thu Jun 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.136.0-2.dev.git441172a
- bump to 2.136.0
- autobuilt 441172a

* Fri May 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.135.0-2.dev.git0d99e89
- bump to 2.135.0
- autobuilt 0d99e89

* Thu May 28 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.134.0-2.dev.gitff26015
- bump to 2.134.0
- autobuilt ff26015

* Thu May 21 2020 Aleksandra Fedorova <afedorova@redhat.com>
- Update gating test name

* Mon May 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.132.0-3.dev.git0a878bd
- autobuilt 0a878bd

* Wed Apr 15 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.132.0-2.dev.git448dfbf
- bump to 2.132.0
- autobuilt 448dfbf

* Thu Apr 09 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.131.0-2.dev.git9ce0dac
- bump to 2.131.0
- autobuilt 9ce0dac

* Mon Apr 06 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.130.0-2.dev.gitfd55ae0
- bump to 2.130.0
- autobuilt fd55ae0

* Sun Mar 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.129.0-2.dev.gitf00d1f4
- bump to 2.129.0
- autobuilt f00d1f4

* Sun Mar 29 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.128.0-2.dev.git363646f
- bump to 2.128.0
- autobuilt 363646f

* Fri Mar 27 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.127.0-2.dev.git6caf15d
- bump to 2.127.0
- autobuilt 6caf15d

* Thu Mar 26 2020 Daniel J Walsh <dwalsh@redhat.com>
- Install selinux contexts file into /usr/share/containers/selinux/contexts

* Thu Mar 26 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.126.0-2.dev.git867a377
- bump to 2.126.0
- autobuilt 867a377

* Mon Mar 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org>
- container-selinux-2:2.125.2-2.dev.gitae0720d
- bump release tag

* Mon Mar 23 2020 Daniel J Walsh <dwalsh@redhat.com>
- Install container_contexts file

* Mon Mar 23 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.125.0-3.1.dev.gitfde876b
- autobuilt fde876b

* Mon Mar 23 2020 Lokesh Mandvekar <lsm5@fedoraproject.org>
- container-selinux-2:2.125.0-2.1.dev.gitb321ea4
- bump release tag for smooth upgrade path

* Fri Mar 20 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.125.0-0.1.dev.gitb321ea4
- bump to 2.125.0
- autobuilt b321ea4

* Tue Feb 11 2020 Lokesh Mandvekar <lsm5@fedoraproject.org>
- keep functional upgrade path

* Tue Feb 11 2020 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.124.0-0.4.dev.git5624558
- autobuilt 5624558

* Mon Feb 03 2020 Ondrej Mosnacek <omosnace@redhat.com>
- Add smoke tests and enable gating

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jan 03 2020 Jindrich Novy <jnovy@redhat.com>
- container-selinux-2.124.0-0.2.dev.gitf958d0c.fc32
- use more current selinux policy version

* Wed Dec 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.124.0-0.1.dev.gitf958d0c
- bump to 2.124.0
- autobuilt f958d0c

* Mon Dec 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org>
- container-selinux-2:2.123.0-0.4.dev.git0b25a4a
- run selinux_relabel_pre

* Fri Nov 29 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.123.0-0.3.dev.git0b25a4a
- autobuilt 0b25a4a

* Fri Nov 29 2019 Daniel J Walsh <dwalsh@redhat.com>
- Use selinux macros in post install scripts

* Mon Nov 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.123.0-0.1.dev.git661a904
- bump to 2.123.0
- autobuilt 661a904

* Fri Nov 22 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.122.0-0.1.dev.git4560dd4
- bump to 2.122.0
- autobuilt 4560dd4

* Tue Nov 19 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.120.1-0.2.dev.gita233788
- autobuilt a233788

* Wed Nov 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.120.1-0.1.dev.git6fb6dcf
- bump to 2.120.1
- autobuilt 6fb6dcf

* Sun Oct 27 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.119.1-0.1.dev.git2ecb2a8
- bump to 2.119.1
- autobuilt 2ecb2a8

* Thu Oct 24 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.119.0-0.1.dev.gitb383f07
- bump to 2.119.0
- autobuilt b383f07

* Fri Oct 11 2019 RH Container Bot <rhcontainerbot@fedoraproject.org>
- container-selinux-2:2.118.0-0.1.dev.git79bdcb5
- bump to 2.118.0
- autobuilt 79bdcb5

* Fri Sep 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org>
- container-selinux-2:2.117.0-0.1.dev.gitbfde70a
- bump to 2.117.0
- autobuilt bfde70a

* Thu Sep 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org>
- container-selinux-2:2.116.0-0.1.dev.gitc5ef5ac
- bump to 2.116.0
- autobuilt c5ef5ac

* Wed Aug 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org>
- container-selinux-2:2.115.0-0.1.dev.gitfddfbbb
- bump to 2.115.0
- autobuilt fddfbbb

* Mon Aug 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org>
- container-selinux-2:2.114.0-0.1.dev.git028ab00
- bump to 2.114.0
- autobuilt 028ab00

* Fri Aug 09 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to name_bind to rawip_sockets.

* Thu Aug 08 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to use fusefs_t entrypoint Dontaudit attempts to setattr
  on devicenodes.

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org>
- container-selinux-2:2.111.0-2.1.dev.git9a75deb
- bump to 2.111.0
- autobuilt 9a75deb

* Wed Jul 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org>
- container-selinux-2.110.0-1.1.dev.git544d71f
- bump to v2.110.0
- hook up to autobuild

* Mon Jul 08 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to accept connections on all socket types Allow
  containers to connect to gssproxy stream sockets if added to container

* Fri Jun 14 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to manipulate Onload files.

* Tue Jun 11 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow all unconfined domains to manage unlabeled keyrings Add labeling
  for kubernetes pods

* Mon Jun 03 2019 Daniel J Walsh <dwalsh@redhat.com>
- Set proper labeling for container volumes in SilverBlue

* Fri May 17 2019 Daniel J Walsh <dwalsh@redhat.com>
- Set proper labeling for container volumes

* Fri May 17 2019 Daniel J Walsh <dwalsh@redhat.com>
- Set proper labeling for container volumes

* Sun May 12 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow all container domains to be entered from container_file_t

* Fri May 03 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to read rpm cache and rpm databse

* Tue Apr 23 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers running as spc_t to create unlabeled_t kernel keyrings

* Tue Apr 23 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers running as spc_t to create unlabeled_t kernel keyrings

* Tue Apr 23 2019 Daniel J Walsh <dwalsh@redhat.com>
- Fix labeling on /var/lib/containers/storage/overlay-layers,images to be
  sharable.

* Mon Apr 22 2019 Daniel J Walsh <dwalsh@redhat.com>
- Fix labeling on /var/lib/containers/storage/overlay-layers,images to be
  sharable.

* Mon Apr 15 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow iptables to append to container_file_t

* Fri Apr 12 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to read/write sysctl_kernel_ns_last_pid_t Allow
  containers to manage fusefs sockets and named pipes

* Mon Apr 01 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to create fusefs sockets and named pipes

* Mon Apr 01 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to create fusefs sockets and named pipes

* Thu Mar 28 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow init_t to manage container content Allow container domains to
  create fifo_files on fusefs file systems Add boolean to allow containers
  to use ceph file systems

* Tue Mar 26 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow container runtimes to create unlabeled keyrings

* Wed Mar 20 2019 Daniel J Walsh <dwalsh@redhat.com>
- Allow containers to mount and umount fuse file systems.  This will allow
  us to use buidlah within a user namespace separated container.

* Sat Mar 09 2019 Daniel J Walsh <dwalsh@redhat.com>
- RPMAUTOSPEC: unresolvable merge
## END: Generated by rpmautospec
