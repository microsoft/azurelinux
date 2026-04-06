# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global selinuxtype targeted
%global moduletype distributed
%define semodule_version 1.1

Summary: Application Whitelisting Daemon
Name: fapolicyd
Version: 1.4.3
Release: 3%{?dist}
License: GPL-3.0-or-later
URL: https://github.com/linux-application-whitelisting/fapolicyd
Source0: https://github.com/linux-application-whitelisting/fapolicyd/releases/download/v%{version}/fapolicyd-%{version}.tar.gz
Source1: https://github.com/linux-application-whitelisting/%{name}-selinux/releases/download/v%{semodule_version}/%{name}-selinux-%{semodule_version}.tar.gz
Source2: https://github.com/bachradsusi.gpg
Source3: fapolicyd.sysusers
Source10: https://github.com/linux-application-whitelisting/fapolicyd/releases/download/v%{version}/fapolicyd-%{version}.tar.gz.asc
Source11: https://github.com/linux-application-whitelisting/%{name}-selinux/releases/download/v%{semodule_version}/%{name}-selinux-%{semodule_version}.tar.gz.asc
# we bundle uthash for eln
Source20: https://github.com/troydhanson/uthash/archive/refs/tags/v2.3.0.tar.gz#/uthash-2.3.0.tar.gz

# https://github.com/linux-application-whitelisting/fapolicyd
# $ git format-patch -N v1.4.3
# https://github.com/linux-application-whitelisting/fapolicyd-selinux
# $ git format-patch -N --start-number 100 --src-prefix=a/fapolicyd-selinux-1.1/ --dst-prefix=b/fapolicyd-selinux-1.1/ v1.1
# $ for j in [0-9]*.patch; do printf "Patch: %s\n" $j; done
# Patch list start
Patch: 0002-If-less-than-16-chars-were-read-allow-shebang-test-c.patch
Patch: 0003-Fix-binary-path-of-rpm-loader.patch
Patch: 0004-Map-file-with-MAP_SHARED-instead-of-MAP_PRIVATE.patch
Patch: 0005-Fix-segfault-when-interrupting-fapolicyd-startup.patch
# Patch list end

BuildRequires: gcc
BuildRequires: kernel-headers
BuildRequires: autoconf automake make gcc libtool
BuildRequires: systemd systemd-devel openssl-devel rpm-devel file-devel file
BuildRequires: libcap-ng-devel libseccomp-devel lmdb-devel
BuildRequires: python3-devel
%if 0%{?fedora} || 0%{?rhel} > 10
BuildRequires: gpgverify
%else
BuildRequires: gnupg
%endif

%if 0%{?rhel} == 0
BuildRequires: uthash-devel
%endif

Requires: rpm-plugin-fapolicyd
Recommends: %{name}-selinux
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
Fapolicyd (File Access Policy Daemon) implements application whitelisting
to decide file access rights. Applications that are known via a reputation
source are allowed access while unknown applications are not. The daemon
makes use of the kernel's fanotify interface to determine file access rights.

%package        selinux
Summary:        Fapolicyd selinux
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}
Requires:       selinux-policy-%{selinuxtype}
Requires(post): selinux-policy-%{selinuxtype}
BuildRequires:  selinux-policy-devel
BuildArch: noarch
%{?selinux_requires}

%description    selinux
The %{name}-selinux package contains selinux policy for the %{name} daemon.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE10}' --data='%{SOURCE0}'
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE11}' --data='%{SOURCE1}'

%setup -q

# selinux
%autosetup -D -T -a 1 -p 1

%if 0%{?rhel} != 0
%setup -q -D -T -b 20
%endif

# generate rules for python
sed -i "s|%python2_path%|`readlink -f %{__python2}`|g" rules.d/*.rules
sed -i "s|%python3_path%|`readlink -f %{__python3}`|g" rules.d/*.rules

# Detect run time linker directly from bash
interpret=`readelf -e /usr/bin/bash \
    | grep Requesting \
    | sed 's/.$//' \
    | rev | cut -d" " -f1 \
    | rev`

sed -i "s|%ld_so_path%|`realpath $interpret`|g" rules.d/*.rules

%build
cp INSTALL INSTALL.tmp

# necessary for updating CFLAGS below
%set_build_flags

%if 0%{?rhel} != 0
export CFLAGS="$CFLAGS -I%{_builddir}/uthash-2.3.0/include"
%endif

./autogen.sh
%configure \
    --with-audit \
    --with-rpm \
    --disable-shared

%make_build

# selinux
pushd %{name}-selinux-%{semodule_version}
make
popd

%check
make check

# selinux
%pre selinux
%selinux_relabel_pre -s %{selinuxtype}

%install
%make_install
install -p -m 644 -D init/%{name}-tmpfiles.conf %{buildroot}/%{_tmpfilesdir}/%{name}.conf
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysusersdir}/%{name}.conf
mkdir -p %{buildroot}/%{_localstatedir}/lib/%{name}
mkdir -p %{buildroot}/run/%{name}
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/trust.d
mkdir -p %{buildroot}%{_sysconfdir}/%{name}/rules.d
# get list of file names between known-libs and restrictive from sample-rules/README-rules
cat %{buildroot}/%{_datadir}/%{name}/sample-rules/README-rules \
  | grep -A 100 'known-libs' \
  | grep -B 100 'restrictive' \
  | grep '^[0-9]' > %{buildroot}/%{_datadir}/%{name}/default-ruleset.known-libs
chmod 644 %{buildroot}/%{_datadir}/%{name}/default-ruleset.known-libs

# selinux
install -d %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -m 0644 %{name}-selinux-%{semodule_version}/%{name}.pp.bz2 %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -m 0644 %{name}-selinux-%{semodule_version}/%{name}-hardening.cil %{buildroot}%{_datadir}/selinux/packages/%{selinuxtype}
install -d -p %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}
install -p -m 644 %{name}-selinux-%{semodule_version}/%{name}.if %{buildroot}%{_datadir}/selinux/devel/include/%{moduletype}/%{name}.if

#cleanup
find %{buildroot} \( -name '*.la' -o -name '*.a' \) -delete

%post
# if no pre-existing rule file
if [ ! -e %{_sysconfdir}/%{name}/%{name}.rules ] ; then
 files=`ls %{_sysconfdir}/%{name}/rules.d/ 2>/dev/null | wc -w`
 # Only if no pre-existing component rules
 if [ "$files" -eq 0 ] ; then
  ## Install the known libs policy
  for rulesfile in `cat %{_datadir}/%{name}/default-ruleset.known-libs`; do
    cp %{_datadir}/%{name}/sample-rules/$rulesfile  %{_sysconfdir}/%{name}/rules.d/
  done
  chgrp %{name} %{_sysconfdir}/%{name}/rules.d/*
  if [ -x /usr/sbin/restorecon ] ; then
   # restore correct label
   /usr/sbin/restorecon -F %{_sysconfdir}/%{name}/rules.d/*
  fi
  fagenrules >/dev/null
 fi
fi
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc README.md
%{!?_licensedir:%global license %%doc}
%license COPYING
%attr(755,root,root) %dir %{_datadir}/%{name}
%attr(755,root,root) %dir %{_datadir}/%{name}/sample-rules
%attr(644,root,root) %{_datadir}/%{name}/default-ruleset.known-libs
%attr(644,root,root) %{_datadir}/%{name}/sample-rules/*
%attr(644,root,root) %{_datadir}/%{name}/fapolicyd-magic.mgc
%attr(750,root,%{name}) %dir %{_sysconfdir}/%{name}
%attr(750,root,%{name}) %dir %{_sysconfdir}/%{name}/trust.d
%attr(750,root,%{name}) %dir %{_sysconfdir}/%{name}/rules.d
%attr(644,root,root) %{_sysconfdir}/bash_completion.d/*
%ghost %{_sysconfdir}/%{name}/rules.d/*
%ghost %{_sysconfdir}/%{name}/%{name}.rules
%config(noreplace) %attr(644,root,%{name}) %{_sysconfdir}/%{name}/%{name}.conf
%config(noreplace) %attr(644,root,%{name}) %{_sysconfdir}/%{name}/%{name}-filter.conf
%config(noreplace) %attr(644,root,%{name}) %{_sysconfdir}/%{name}/%{name}.trust
%ghost %attr(644,root,%{name}) %{_sysconfdir}/%{name}/compiled.rules
%attr(644,root,root) %{_unitdir}/%{name}.service
%attr(644,root,root) %{_tmpfilesdir}/%{name}.conf
%attr(644,root,root) %{_sysusersdir}/%{name}.conf
%attr(755,root,root) %{_bindir}/%{name}-rpm-loader
%attr(755,root,root) %{_sbindir}/%{name}
%attr(755,root,root) %{_sbindir}/%{name}-cli
%attr(755,root,root) %{_sbindir}/fagenrules
%attr(644,root,root) %{_mandir}/man8/*
%attr(644,root,root) %{_mandir}/man5/*
%ghost %attr(440,%{name},%{name}) %verify(not md5 size mtime) %{_localstatedir}/log/%{name}-access.log
%attr(770,root,%{name}) %dir %{_localstatedir}/lib/%{name}
%attr(770,root,%{name}) %dir /run/%{name}
%ghost %attr(660,root,%{name}) /run/%{name}/%{name}.fifo
%ghost %attr(660,%{name},%{name}) %verify(not md5 size mtime) %{_localstatedir}/lib/%{name}/data.mdb
%ghost %attr(660,%{name},%{name}) %verify(not md5 size mtime) %{_localstatedir}/lib/%{name}/lock.mdb

%files selinux
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2
%{_datadir}/selinux/packages/%{selinuxtype}/%{name}-hardening.cil
%ghost %verify(not md5 size mode mtime) %{_sharedstatedir}/selinux/%{selinuxtype}/active/modules/200/%{name}
%{_datadir}/selinux/devel

%post selinux
%selinux_modules_install -s %{selinuxtype} %{_datadir}/selinux/packages/%{selinuxtype}/%{name}.pp.bz2 %{_datadir}/selinux/packages/%{selinuxtype}/%{name}-hardening.cil
%selinux_relabel_post -s %{selinuxtype}

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall -s %{selinuxtype} %{name}-hardening %{name}
fi

%posttrans selinux
%selinux_relabel_post -s %{selinuxtype}

%changelog
* Tue Jan 27 2026 Petr Lautrbach <lautrbach@redhat.com> - 1.4.3-3
- Fix binary path of rpm-loader
- Map file with MAP_SHARED instead of MAP_PRIVATE
- Fix segfault when interrupting fapolicyd startup

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Tue Jan 13 2026 Petr Lautrbach <lautrbach@redhat.com> - 1.4.3-1
- fapolicyd-1.4.3
  https://github.com/linux-application-whitelisting/fapolicyd/releases/tag/v1.4.3
  https://github.com/linux-application-whitelisting/fapolicyd-selinux/releases/tag/v1.1

* Wed Nov 26 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.4.2-1
- fapolicyd-1.4.2
  https://github.com/linux-application-whitelisting/fapolicyd/releases/tag/v1.4.2

* Fri Nov 07 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.4.1-2
- Install SELinux policy hardening module

* Fri Oct 31 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.4.1-1
- Fix deadlock on reconfigure
- On reconfigure, update the trust list and reload the rpm filter

* Thu Oct 30 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.4-1
- fapolicyd-1.4 and fapolicyd-selinux-1.0
  https://github.com/linux-application-whitelisting/fapolicyd/releases/tag/v1.4

* Fri Oct 17 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.3.7-2
- Update magic for python 3.14rc3
- Allow daemon to change var_run_t dir attributes

* Fri Sep 19 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.3.7-1
- fapolicyd-1.3.7

* Wed Sep 03 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.3.6-1
- fapolicyd-1.3.6 and fapolicyd-selinux-0.9

* Tue Aug 26 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.3.5-2
- Modify queue to use ring buffer
- Fix memory leaks in the AVL tests
- Do not exit in do_database_reload when stop in progress
- Add /var/lib/fapolicyd to tmpfiles
- Fix owner:group of /etc/fapolicyd on boot
- Change /usr/share/fapolicyd to root:root

* Mon Aug 11 2025 Petr Lautrbach <lautrbach@redhat.com> - 1.3.5-1
- fapolicyd-1.3.5 and fapolicyd-selinux-0.8

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.3.4-3
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 28 2024 Radovan Sroka <rsroka@redhat.com> - 1.3.4-1
- rebase to v1.3.4

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 29 2024 Radovan Sroka <rsroka@redhat.com> - 1.3.3-1
- rebase to fapolicyd v1.3.3 and fapolicyd-selinux to v0.7

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jul 10 2023 Radovan Sroka <rsroka@redhat.com> - 1.3.3-1
- rebase to fapolicyd v1.3.2

* Thu Jun 15 2023 Radovan Sroka <rsroka@redhat.com> - 1.3.1-2
- rebase to fapolicyd v1.3.1 and selinux v0.6

* Tue Jun 13 2023 Radovan Sroka <rsroka@redhat.com> - 1.2-6
- migrated to SPDX license

* Fri May 19 2023 Petr Pisar <ppisar@redhat.com> - 1.2-5
- Rebuild against rpm-4.19 (https://fedoraproject.org/wiki/Changes/RPM-4.19)

* Fri Feb 10 2023 Radovan Sroka <rsroka@redhat.com> - 1.2-1
- rebase to v1.2

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Dec 02 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.7-3
- rebuild for eln

* Mon Nov 28 2022 Florian Weimer <fweimer@redhat.com> - 1.1.7-2
- Avoid implicit declaration of rpmFreeCrypto

* Mon Nov 28 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.7.1
- rebase fapolicyd to v1.1.7 and fapolicyd-selinux to v0.5

* Thu Sep 29 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.5.2
- rebase to 1.1.5

* Wed Aug 31 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.4-4
- fix bash completition definition in spec
Resolves: rhbz#2123065

* Tue Aug 30 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.4-3
- rebuild with correct openssl and systemd dependency

* Thu Aug 18 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.4-1
- rebase to 1.1.4

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jun 22 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.3-1
- rebase to 1.1.3
- removal of dnf plugin

* Wed Jun 15 2022 Python Maint <python-maint@redhat.com> - 1.1.2-2
- Rebuilt for Python 3.11

* Wed May 25 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.2-1
- rebase to v1.1.2
- fixed CVE-2022-1117
Resolves: rhbz#2089692

* Wed Mar 30 2022 Radovan Sroka <rsroka@redhat.com> - 1.1.1-2
- rebase to v1.1.1

* Tue Feb 15 2022 Radovan Sroka <rsroka@redhat.com> - 1.1-2
- old fapolicyd.rules needs to be ghost file

* Sun Jan 23 2022 Radovan Sroka <rsroka@redhat.com> - 1.1-1
- rebase to v1.1
- added rules.d folder

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec 24 2021 Björn Esser <besser82@fedoraproject.org> - 1.0.4-2
- Rebuild(uthash)

* Fri Dec 10 2021 Radovan Sroka <rsoka@redhat.com> - 1.0.4-1
- rebase to 1.0.4
- enable trust.d folder

* Wed Sep 01 2021 Radovan Sroka <rsroka@redhat.com> - 1.0.3-4
- selinux: use watch perm correctly

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri Jun 04 2021 Python Maint <python-maint@redhat.com> - 1.0.3-2
- Rebuilt for Python 3.10

* Thu Apr 01 2021 Radovan Sroka <rsroka@redhat.com> - 1.0.3-1
- rebase to 1.0.3
- sync fedora with rhel

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.0.2-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jan 06 2021 Radovan Sroka <rsroka@redhat.com> - 1.0.2-1
- rebase to 1.0.2
- enabled make check
- dnf-plugin is now required subpackage

* Mon Nov 16 2020 Radovan Sroka <rsroka@redhat.com> - 1.0.1-1
- rebase to 1.0.1
- introduced uthash dependency
- SELinux prevents the fapolicyd process from writing to /run/dbus/system_bus_socket
Resolves: rhbz#1874491
- SELinux prevents the fapolicyd process from writing to /var/lib/rpm directory
Resolves: rhbz#1876538

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 24 2020 Radovan Sroka <rsroka@redhat.com> - 1.0-3
- backported few cosmetic small patches from upstream master
- rebase selinux tarbal to v0.3
- file context pattern for /run/fapolicyd.pid is missing
Resolves: rhbz#1834674

* Tue May 26 2020 Miro Hrončok <mhroncok@redhat.com> - 1.0-2
- Rebuilt for Python 3.9

* Mon May 25 2020 Radovan Sroka <rsroka@redhat.com> - 1.0-1
- rebase fapolicyd to 1.0
- allowed sys_ptrace for user namespace

* Mon Mar 23 2020 Radovan Sroka <rsroka@redhat.com> - 0.9.4-1
- rebase fapolicyd to 0.9.4
- polished the pattern detection engine
- rpm backend now drops most of the files in /usr/share/ to dramatically reduce
  memory consumption and improve startup speed
- the commandline utility can now delete the lmdb trust database and manage
  the file trust source

* Mon Feb 24 2020 Radovan Sroka <rsroka@redhat.com> - 0.9.3-1
- rebase fapolicyd to 0.9.3
- dramatically improved startup time
- fapolicyd-cli has picked up --list and --ftype commands to help debug/write policy
- file type identification has been improved
- trust database statistics have been added to the reports

* Tue Feb 04 2020 Radovan Sroka <rsroka@redhat.com> - 0.9.2-2
- Label all fifo_file as fapolicyd_var_run_t in /var/run.
- Allow fapolicyd_t domain to create fifo files labeled as
  fapolicyd_var_run_t

* Fri Jan 31 2020 Radovan Sroka <rsroka@redhat.com> - 0.9.2-1
- rebase fapolicyd to 0.9.2
- allows watched mount points to be specified by file system types
- ELF file detection was improved
- the rules have been rewritten to express the policy based on subject
  object trust for better performance and reliability
- exceptions for dracut and ansible were added to the rules to avoid problems
  under normal system use
- adds an admin defined trust database (fapolicyd.trust)
- setting boost, queue, user, and group on the daemon
  command line are deprecated

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Nov 05 2019 Marek Tamaskovic <mtamasko@redhat.com> - 0.9-3
- Updated fapolicyd-selinux subpackage to v0.2
  Selinux subpackage is recommended for fapolicyd.

* Mon Oct 07 2019 Radovan Sroka <rsroka@redhat.com> - 0.9-2
- Added fapolicyd-selinux subpackage

* Mon Oct 07 2019 Radovan Sroka <rsroka@redhat.com> - 0.9-1
- rebase to v0.9

* Thu Oct 03 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8.10-2
- Rebuilt for Python 3.8.0rc1 (#1748018)

* Wed Aug 28 2019 Radovan Sroka <rsroka@redhat.com> - 0.8.10-1
- rebase to 0.8.10
- generate python paths dynamically

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 0.8.9-5
- Rebuilt for Python 3.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 10 22:13:18 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.9-3
- Rebuild for RPM 4.15

* Mon Jun 10 15:42:01 CET 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.8.9-2
- Rebuild for RPM 4.15

* Mon May 06 2019 Radovan Sroka <rsroka@redhat.com> - 0.8.9-1
- New upstream release

* Wed Mar 13 2019 Radovan Sroka <rsroka@redhat.com> - 0.8.8-2
- backport some patches to resolve dac_override for fapolicyd

* Mon Mar 11 2019 Radovan Sroka <rsroka@redhat.com> - 0.8.8-1
- New upstream release
- Added new DNF plugin that can update the trust database when rpms are installed
- Added support for FAN_OPEN_EXEC_PERM

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild


* Wed Oct 03 2018 Steve Grubb <sgrubb@redhat.com> 0.8.7-1
- New upstream bugfix release

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.8.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 07 2018 Steve Grubb <sgrubb@redhat.com> 0.8.6-1
- New upstream feature release

* Fri May 18 2018 Steve Grubb <sgrubb@redhat.com> 0.8.5-2
- Add dist tag (#1579362)

* Fri Feb 16 2018 Steve Grubb <sgrubb@redhat.com> 0.8.5-1
- New release
