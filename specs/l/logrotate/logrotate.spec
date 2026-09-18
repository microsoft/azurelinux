# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Summary: Rotates, compresses, removes and mails system log files
Name: logrotate
Version: 3.22.0
Release: 4%{?dist}
License: GPL-2.0-or-later
URL: https://github.com/logrotate/logrotate
Source0: https://github.com/logrotate/logrotate/releases/download/%{version}/logrotate-%{version}.tar.xz
Source1: https://github.com/logrotate/logrotate/releases/download/%{version}/logrotate-%{version}.tar.xz.asc

# gpg --keyserver pgp.mit.edu --recv-key 8ECCDF12100AD84DA2EE7EBFC78CE737A3C3E28E
# gpg --output cgzones.pgp --armor --export cgzones@googlemail.com
Source2: cgzones.pgp

Source3: rwtab

BuildRequires: acl
BuildRequires: automake
BuildRequires: gcc
BuildRequires: git
BuildRequires: gnupg2
BuildRequires: libacl-devel
BuildRequires: libselinux-devel
BuildRequires: make
BuildRequires: popt-devel
BuildRequires: systemd-rpm-macros
Requires: coreutils
Requires(post): systemd
Requires(preun): systemd

%description
The logrotate utility is designed to simplify the administration of
log files on a system which generates a lot of log files.  Logrotate
allows for the automatic rotation compression, removal and mailing of
log files.  Logrotate can be set to handle a log file daily, weekly,
monthly or when the log file gets to a certain size.

Install the logrotate package if you need a utility to deal with the
log files on your system.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -S git

cat >> .gitignore << EOF
/autom4te.cache
/build
/config.h.in~
EOF
git add .gitignore
git commit -m "update .gitignore"

autoreconf -fiv
git add --all
git commit -m "force autoreconf" --allow-empty

%build
mkdir build && cd build
%global _configure ../configure
%configure --with-state-file-path=%{_localstatedir}/lib/logrotate/logrotate.status
%make_build

%check
%make_build -C build -s check

%install
%make_install -C build

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/logrotate

install -p -m 644 examples/logrotate.conf $RPM_BUILD_ROOT%{_sysconfdir}/
install -p -m 644 examples/{b,w}tmp $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/
install -p -m 644 examples/logrotate.{service,timer} $RPM_BUILD_ROOT%{_unitdir}/

# Make sure logrotate is able to run on read-only root
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d
install -m644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/rwtab.d/logrotate

%pre
# If /var/lib/logrotate/logrotate.status does not exist, create it and copy
# the /var/lib/logrotate.status in it (if it exists). We have to do that in pre
# script, otherwise the /var/lib/logrotate/logrotate.status would not be there,
# because during the update, it is removed/renamed.
if [ ! -d %{_localstatedir}/lib/logrotate/ -a -f %{_localstatedir}/lib/logrotate.status ]; then
  mkdir -p %{_localstatedir}/lib/logrotate
  cp -a %{_localstatedir}/lib/logrotate.status %{_localstatedir}/lib/logrotate
fi

%post
%systemd_post logrotate.{service,timer}

# If there is any cron daemon configured, enable the systemd timer to avoid
# breaking the configuration silently when upgrading from 3.14.0-4 or
# earlier versions
%triggerin -- logrotate < 3.14.0-5
[ -e %{_sysconfdir}/crontab -o -e %{_sysconfdir}/anacrontab -o -e %{_sysconfdir}/fcrontab ] \
  && %{_bindir}/systemctl enable --now logrotate.timer &>/dev/null || :

%preun
%systemd_preun logrotate.{service,timer}

%files
%license COPYING
%doc ChangeLog.md
%{_sbindir}/logrotate
%{_unitdir}/logrotate.{service,timer}
%{_mandir}/man8/logrotate.8*
%{_mandir}/man5/logrotate.conf.5*
%config(noreplace) %{_sysconfdir}/logrotate.conf
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/{b,w}tmp
%dir %{_localstatedir}/lib/logrotate
%ghost %verify(not size md5 mtime) %attr(0640, root, root) %{_localstatedir}/lib/logrotate/logrotate.status
%config(noreplace) %{_sysconfdir}/rwtab.d/logrotate

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.22.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jun 10 2024 Jan Macku <jamacku@redhat.com> - 3.22.0-1
- new upstream version 3.22.0
- release signed with new key (cgzones.pgp)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Mar 22 2023 Lukáš Zaoral <lzaoral@redhat.com> - 3.21.0-3
- migrated to SPDX license

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.21.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Kamil Dudka <kdudka@redhat.com> - 3.21.0-1
- new upstream version 3.21.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.20.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri May 27 2022 Kamil Dudka <kdudka@redhat.com> - 3.20.1-2
- lockState: do not print `error:` when exit code is unaffected (#2090926)

* Wed May 25 2022 Kamil Dudka <kdudka@redhat.com> - 3.20.1-1
- new upstream version 3.20.1, which fixes the following security issue:
    CVE-2022-1348 - potential DoS from unprivileged users via the state file

* Tue Mar 15 2022 Kamil Dudka <kdudka@redhat.com> - 3.19.0-3
- verify GPG signature of upstream tarball when building the package

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.19.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jan 07 2022 Kamil Dudka <kdudka@redhat.com> - 3.19.0-1
- new upstream version 3.19.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Kamil Dudka <kdudka@redhat.com> - 3.18.1-1
- new upstream version 3.18.1

* Tue May 04 2021 Kamil Dudka <kdudka@redhat.com> - 3.18.0-3
- make `renamecopy` and `copytruncate` override each other (#1934601)
- unify documentation of copy/copytruncate/renamecopy (#1934629)
- fix resource leaks reported by Coverity

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 3.18.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 08 2021 Kamil Dudka <kdudka@redhat.com> - 3.18.0-1
- new upstream version 3.18.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.17.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 3.17.0-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jul 10 2020 Kamil Dudka <kdudka@redhat.com> - 3.17.0-1
- new upstream version 3.17.0

* Fri Feb 28 2020 Kamil Dudka <kdudka@redhat.com> - 3.16.0-1
- new upstream version 3.16.0

* Thu Jan 30 2020 Kamil Dudka <kdudka@redhat.com> - 3.15.1-3
- make the code compile with gcc-10

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Kamil Dudka <kdudka@redhat.com> - 3.15.1-1
- new upstream version 3.15.1

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec 04 2018 Kamil Dudka <kdudka@redhat.com> - 3.15.0-1
- new upstream version 3.15.0

* Wed Nov 21 2018 Alejandro Domínguez Muñoz <adomu@net-c.com> - 3.14.0-5
- add make as a build dependency
- replace cron job with a systemd timer unit (#1502085, #1655153)

* Fri Aug 10 2018 Kamil Dudka <kdudka@redhat.com> - 3.14.0-4
- fix programming mistakes detected by Coverity Analysis
- document the --version option in the logrotate(8) man page (#1611498)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.14.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Kamil Dudka <kdudka@redhat.com> - 3.14.0-2
- fix license tag to match the source code license

* Fri Mar 09 2018 Kamil Dudka <kdudka@redhat.com> - 3.14.0-1
- new upstream version 3.14.0

* Mon Feb 19 2018 Kamil Dudka <kdudka@redhat.com> - 3.13.0-3
- add explicit BR for the gcc compiler

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Oct 13 2017 Kamil Dudka <kdudka@redhat.com> - 3.13.0-1
- new upstream version 3.13.0

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.12.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Kamil Dudka <kdudka@redhat.com> - 3.12.3-1
- new upstream version 3.12.3

* Tue May 02 2017 Kamil Dudka <kdudka@redhat.com> - 3.12.2-1
- new upstream version 3.12.2

* Fri Apr 21 2017 Kamil Dudka <kdudka@redhat.com> - 3.12.1-1
- new upstream version 3.12.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.11.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 25 2017 Kamil Dudka <kdudka@redhat.com> - 3.11.0-3
- mark cron.daily/logrotate as config file (#1174207)

* Thu Dec 08 2016 Kamil Dudka <kdudka@redhat.com> - 3.11.0-2
- make the package build on RHEL-6, too

* Fri Dec 02 2016 Kamil Dudka <kdudka@redhat.com> - 3.11.0-1
- build out of source tree
- new upstream version 3.11.0

* Thu Nov 24 2016 Kamil Dudka <kdudka@redhat.com> - 3.10.0-4
- make /var/lib/logrotate/logrotate.status the default state file (#1381719)

* Fri Nov 11 2016 Kamil Dudka <kdudka@redhat.com> - 3.10.0-3
- fix migration of state file from its previous location (#1393247)

* Tue Aug 23 2016 Kamil Dudka <kdudka@redhat.com> - 3.10.0-2
- own /etc/cron.daily because no dependency of logrotate installs it
- do not explicitly declare mode for each single installed file

* Wed Aug 03 2016 Kamil Dudka <kdudka@redhat.com> - 3.10.0-1
- document default state file used by logrotate cron job (#1357215)
- modernize spec file
- new upstream version 3.10.0

* Wed Jul 20 2016 Kamil Dudka <kdudka@redhat.com> - 3.9.2-5
- do not log to syslog by default (#1304828)

* Thu Jul 14 2016 Kamil Dudka <kdudka@redhat.com> - 3.9.2-4
- make the /var/lib/logrotate directory owned by logrotate

* Tue Feb 16 2016 Marcin Juszkiewicz <mjuszkiewicz@redhat.com> - 3.9.2-3
- Fix code indentation to get it build with gcc6.
- Fixed dates in changelog.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Jan Kaluza <jkaluza@redhat.com> - 3.9.2-1
- new upstream version 3.9.2
- log to syslog

* Wed Jun 17 2015 Jan Kaluza <jkaluza@redhat.com> - 3.9.1-2
- move logrotate.status to /var/lib/logrotate and add it to rwtab.d (#1127415)

* Fri Apr 03 2015 Jan Kaluza <jkaluza@redhat.com> - 3.9.1-1
- new upstream version 3.9.1

* Fri Apr 03 2015 Jan Kaluza <jkaluza@redhat.com> - 3.9.0-1
- new upstream version 3.9.0

* Fri Feb 13 2015 Jan Kaluza <jkaluza@redhat.com> - 3.8.9-1
- new upstream version 3.8.9

* Thu Oct 16 2014 Jan Kaluza <jkaluza@redhat.com> - 3.8.8-1
- new upstream version 3.8.8

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 3.8.7-3
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Oct 10 2013 Jan Kaluza <jkaluza@redhat.com> - 3.8.7-1
- new usptream version 3.8.7

* Wed Jul 31 2013 Jan Kaluza <jkaluza@redhat.com> - 3.8.6-1
- new upstream version 3.8.6

* Wed Jul 10 2013 Jan Kaluza <jkaluza@redhat.com> - 3.8.5-2
- fix #982409 - do not crash when no logs are rotated and "sharedscripts" and
  "prerotate" is used

* Mon Jun 10 2013 Jan Kaluza <jkaluza@redhat.com> - 3.8.5-1
- new upstream version 3.8.5

* Tue May 14 2013 Jan Kaluza <jkaluza@redhat.com> - 3.8.4-2
- do not try to parse config files bigger than 16MB
- remove unused patches

* Tue Apr 30 2013 Jan Kaluza <jkaluza@redhat.com> - 3.8.4-1
- new upstream version 3.8.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Oct 04 2012 Jan Kaluza <jkaluza@redhat.com> 3.8.3-1
- new upstream version 3.8.3

* Thu Jul 19 2012 Jan Kaluza <jkaluza@redhat.com> 3.8.2-1
- new upstream version 3.8.2
- tests are enabled during build

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.8.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jan 04 2012 Jan Kaluza <jkaluza@redhat.com> 3.8.1-3
- fix #736054 - check for missing '{' in config file

* Mon Oct 03 2011 Jan Kaluza <jkaluza@redhat.com> 3.8.1-2
- fix #742731 - man page syntax, formatting, and spelling fixes

* Tue Sep 06 2011 Jan Kaluza <jkaluza@redhat.com> 3.8.1-1
- new upstream version 3.8.1

* Mon Aug 08 2011 Jan Kaluza <jkaluza@redhat.com> 3.8.0-5
- fix #723797 - added maxsize option

* Mon Aug 01 2011 Jan Kaluza <jkaluza@redhat.com> 3.8.0-4
- fix #726980 - work properly when acl_get_fd is supported,
  but acl_set_fd is not

* Fri Jul 22 2011 Jan Kaluza <jkaluza@redhat.com> 3.8.0-3
- fix #723547 - fixed size directive parsing

* Wed Jul 20 2011 Jan Kaluza <jkaluza@redhat.com> 3.8.0-2
- fix #722825 - do not redirect logrotate output in cron script

* Tue Jun 21 2011 Jan Kaluza <jkaluza@redhat.com> 3.8.0-1
- new upstream version 3.8.0
- removed unused patches

* Tue May 31 2011 Jan Kaluza <jkaluza@redhat.com> 3.7.9-11
- fix #709034 - work properly when ACLs are not supported

* Mon May 30 2011 Jan Kaluza <jkaluza@redhat.com> 3.7.9-10
- fix #708367 - fixed mail directive parsing

* Mon Mar 28 2011 Jan Kaluza <jkaluza@redhat.com> 3.7.9-9
- fix #689061 - added Url 

* Mon Mar 21 2011 Jan Kaluza <jkaluza@redhat.com> 3.7.9-8
- fix #688520 - fixed CVE-2011-1154, CVE-2011-1155 and CVE-2011-1098

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Feb 02 2011 Jan Kaluza <jkaluza@redhat.com> 3.7.9-6
- fix #671926 - fixed crash when tabooext is used in config file

* Wed Dec 15 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.9-5
- fix #661181 - fixed SIGBUS when config file is empty or 4096 bytes
- fix #666677 - preserve ACLs when rotating files

* Tue Oct 19 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.9-4
- fix #644309 - mention all logrotate params in man page

* Wed Sep 29 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.9-3
- fix #638629 - better size directive description

* Mon Aug 09 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.9-2
- fixed AUTHORS in man page

* Mon Jun 28 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.9-1
- new upstream version 3.7.9

* Tue Jun 22 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-12
- fix #602643 - update manpage to reflect scripts changes
- fix #606675 - pass currently rotated file as argument to
  postrotate/prerotate script in nosharedscripts mode

* Tue Jun 15 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-11
- fix #603040 - do not remove log if there is an error in
  rotate process

* Tue Apr 20 2010 Jan Kaluza <jkaluza@redhat.com> 3.7.8-10
- fix #602643 - logrotate "size" directive cannot exceed
  1895825408 bytes

* Tue Apr 20 2010 Daniel Novotny <dnovotny@redhat.com> 3.7.8-9
- revert the "create 0640 root adm" permission change (#489038)

* Tue Apr 06 2010 Daniel Novotny <dnovotny@redhat.com> 3.7.8-8
- fix #578115 - missingok problem with globs

* Mon Jan 11 2010 Daniel Novotny <dnovotny@redhat.com> 3.7.8-7
- fix #489038 -  RFE: useful permissions on log files

* Wed Dec 09 2009 Henrique Martins <bugzilla-redhat-2009@martins.cc> 3.7.8-6
- fix #545919 (rotate non-writable files when copy is set)

* Tue Sep 29 2009 Daniel Novotny <dnovotny@redhat.com> 3.7.8-5
- fix #525659 (man page for logrotate.conf)

* Thu Sep 17 2009 Daniel Novotny <dnovotny@redhat.com> 3.7.8-4
- fix #517321 (logrotate blocking anacron)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 02 2009 Daniel Novotny <dnovotny@redhat.com> 3.7.8-1
- new upstream version 3.7.8

* Fri Nov 21 2008 Daniel Novotny <dnovotny@redhat.com> 3.7.7-4
- fix #468926 (segfault with very large /var/log/messages)

* Thu Nov 20 2008 Daniel Novotny <dnovotny@redhat.com> 3.7.7-3
- less aggressive approach to the fix

* Thu Nov 20 2008 Daniel Novotny <dnovotny@redhat.com> 3.7.7-2
- fix #471463 (selinux problems with logrotate)

* Mon May 19 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.7-1
- new upstream version

* Wed Apr 23 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-4
- improve patch for #432330
- fix #437748 - don't forget to close log files

* Mon Feb 11 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-3
- fix #432330 segfault on corrupted status file

* Mon Jan 21 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-2.2
- fix #429454 - logrotate fails due to invalid pointer

* Wed Jan 09 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-2.1
- fix the selinux patch

* Wed Jan 09 2008 Tomas Smetana <tsmetana@redhat.com> 3.7.6-2
- fix #427274 - logrotate fails to preserve SELinux file contexts
- fix #427661 - SELinux stops vsftpd from working correctly

* Thu Sep 27 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1.3
- popt-devel dependency was still missing

* Thu Sep 27 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1.2
- add missing dependencies to spec file

* Thu Aug 23 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1.1
- rebuild

* Tue Aug 07 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.6-1
- new upstream version
- fix #248565 logrotate never rotates /var/log/btmp
- fix compile warnings
- tabooext accepts wildcards (related #247816)
- fix minor errors and update man page (related #250059)
- fix handling of size directive (related #247410)

* Thu May 31 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.5-5
- fix ignoring pre/postrotate arguments (related #241766)

* Wed May 23 2007 Tomas Smetana <tsmetana@redhat.com> 3.7.5-4
- use dateext in the default config file (#240292)
- add options to use shred for deleting files -- adapt patch sent by
  Peter Eckersley <pde@eff.org> (#239934)
- ignore .cfsaved files by default (#223476)

* Sat Mar 31 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.5-3
- add error checking before running prerotate and postrotate scripts

* Thu Mar 29 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.5-2
- fix error hadnling after prerotate, postrotate, firstaction 
  script failure. (http://qa.mandriva.com/show_bug.cgi?id=29979)

* Thu Mar 01 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.5-1
- new upstream release.

* Fri Feb 09 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-13
- another spec file fixes (#226104)

* Thu Feb 08 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-12
- fix problem with compress_options_list (#227706)
- fix spec file to meet Fedora standards (#226104)

* Tue Jan 23 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-11
- logrotate won't stop if there are some errors in configuration
  or glob failures (#166510, #182062)

* Wed Jan 10 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-10
- fix some rpmlint issues

* Tue Jan 09 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-9
- allow multibyte characters in readPath() (#122145)

* Fri Jan 05 2007 Peter Vrabec <pvrabec@redhat.com> 3.7.4-8
- "size" option was ignored in config files (#221341)

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-7
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-6
- fix leaking file descriptor (#205072)

* Wed Aug 09 2006 Dan Walsh <dwalsh@redhat.com> 3.7.4-5
- Use selinux raw functions

* Mon Jul 24 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-4
- make error message, about ignoring certain config files,
  a debug message instead (#196052)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.7.4-3.1
- rebuild

* Tue Jun 13 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-3
- rename ENOSUP to ENOTSUP

* Tue Jun 13 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-2
- clean up a couple of SELinux problems. Patch from Daniel J. Walsh.

* Wed May 17 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.4-1
- add new "minsize" option (#173088)

* Tue Mar 28 2006 Peter Vrabec <pvrabec@redhat.com> 3.7.3-3
- correct man page "extension" option description  (#185318)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.7.3-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.7.3-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sun Nov 13 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.3-2
- fix_free_segfaults (#172918)

* Sat Nov 12 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.3-1
- new upstream release
- indent sources

* Fri Nov 11 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-12
- fix_free_segfaults (#172918)

* Mon Nov 07 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-11
- man description for "nodateext" option (#171577)
- remove not working "pattern" option (#171577)

* Tue Oct 25 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-10
- some more clean up (#171587)

* Thu Oct 20 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-9
- fix_free_segfaults (#171093)

* Tue Oct 18 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-8
- fix leaks of tabooExts

* Sat Oct 15 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-7
- fix_free_segfaults (#170904)

* Wed Oct 12 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-6
- code clean up (#169885)

* Mon Oct 10 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-5
- fix bug introduced in logrotate 3.7.2-3(#169858)
- fix some memory leaks (#169888)

* Fri Sep 23 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-4
- do not run compression program in debug mode (#166912)

* Wed Sep 07 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-3
- even when sharedscript option used, do postrotate 
  script before compress (#167575)

* Wed Aug 17 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-2
- allow yearly rotations(#134612)

* Mon Aug 01 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.2-1
- new upstream release

* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-14
- fix some "error running script" messages

* Tue Jul 26 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-13
- fix man page (#163458,#163366)

* Wed Jun 22 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-12
- enhance logrotate with "dateext", "maxage"

* Thu Mar 31 2005 Dan Walsh <dwalsh@redhat.com> 3.7.1-10
- use security_getenforce() instead of selinux_getenforcemode

* Thu Mar 17 2005 Dan Walsh <dwalsh@redhat.com> 3.7.1-9
- Add selinux_getenforce() calls to work when not in enforcing mode

* Thu Mar 17 2005 Peter Vrabec <pvrabec@redhat.com> 3.7.1-8
- rebuild

* Tue Feb 22 2005 Peter Vrabec <pvrabec@redhat.com>
- do not use tmpfile to run script anymore (#149270)

* Fri Feb 18 2005 Peter Vrabec <pvrabec@redhat.com>
- remove logrotate-3.7.1-share.patch, it doesn't solve (#140353)

* Mon Dec 13 2004 Peter Vrabec <pvrabec@redhat.com> - 3.7.1-5
- Add section to logrotate.conf for "/var/log/btmp" (#117844)

* Mon Dec 13 2004 Peter Vrabec <pvrabec@redhat.com> - 3.7.1-4
- Typo and missing information in man page (#139346)

* Mon Dec 06 2004 Peter Vrabec <pvrabec@redhat.com> - 3.7.1-3
- compressed logfiles and logrotate (#140353)

* Tue Oct 19 2004 Miloslav Trmac <mitr@redhat.com> - 3.7.1-2
- Fix sending mails (#131583)
- Preserve file attributes when compressing files (#121523, original patch by
  Daniel Himler)

* Fri Jul 16 2004 Elliot Lee <sopwith@redhat.com> 3.7.1-1
- Fix #126490 typo

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Dan Walsh <dwalsh@redhat.com> 3.6.10-4
- fix is_selinux_enabled call

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 3.6.10-3
- Turn off selinux

* Fri Sep 5 2003 Dan Walsh <dwalsh@redhat.com> 3.6.10-2.sel
- Turn on selinux

* Wed Aug 06 2003 Erik Troan <ewt@redhat.com>
- always use compressext for the extension for compressed
  files; before compresscmd and compressext had to agree
- moved all compression to one code block
- compression, scripts don't use system() anymore
- compress and maillast didn't work together properly
- delaycompress and mailfirst didn't work properly
- don't use system() for mailing (or uncompressing) logs anymore
- use "-s" for speciying the subjected of mailed logs

* Thu Jul 24 2003 Elliot Lee <sopwith@redhat.com> 3.6.10-1
- Fix #100546, change selinux port.

* Fri Jul 18 2003 Dan Walsh <dwalsh@redhat.com> 3.6.9-2
- Port to SELinux 2.5

* Wed Jul 09 2003 Elliot Lee <sopwith@redhat.com> 3.6.9-1
- Fix #90229, #90274, #89458, #91408

* Mon Jan 20 2003 Elliot Lee <sopwith@redhat.com> 3.6.8-1
- Old patch from pm@debian.org

* Tue Jan 14 2003 Elliot Lee <sopwith@redhat.com> 3.6.7-1
- Fixes from bugzilla

* Fri Nov 15 2002 Elliot Lee <sopwith@redhat.com> 3.6.6-1
- Commit patch from Fidelis Assis <fidelis@embratel.net.br>

* Thu Jun 20 2002 Elliot Lee <sopwith@redhat.com> 3.6.5-1
- Commit fix for #65299

* Mon Apr 15 2002 Elliot Lee <sopwith@redhat.com> 3.6.4-1
- Commit fix for #62560

* Wed Mar 13 2002 Elliot Lee <sopwith@redhat.com> 3.6.3-1
- Apply various bugfix patches from the openwall people

* Tue Jan 29 2002 Elliot Lee <sopwith@redhat.com> 3.6.2-1
- Fix bug #55809 (include logrotate.status in "files")
- Fix bug #58328 (incorrect error detection when reading state file)
- Allow 'G' size specifier from bug #57242

* Mon Dec 10 2001 Preston Brown <pbrown@redhat.com>
- noreplace config file

* Wed Nov 28 2001 Preston Brown <pbrown@redhat.com> 3.6-1
- patch from Alexander Kourakos <awk@awks.org> to stop the shared
  postrotate/prerotate scripts from running if none of the log(s) need
  rotating.  All log files are now checked for rotation in one batch,
  rather than sequentially.
- more fixes from Paul Martin <pm@debian.org>

* Thu Nov  8 2001 Preston Brown <pbrown@redhat.com> 3.5.10-1
- fix from paul martin <pm@debian.org> for zero-length state files

* Tue Sep  4 2001 Preston Brown <pbrown@redhat.com>
- fix segfault when logfile is in current directory.

* Tue Aug 21 2001 Preston Brown <pbrown@redhat.com>
- fix URL for source location

* Thu Aug  2 2001 Preston Brown <pbrown@redhat.com>
- man page cleanups, check for negative rotation counts

* Mon Jul  2 2001 Preston Brown <pbrown@redhat.com>
- more minor manpage updates (#45625)

* Thu Jun 21 2001 Preston Brown <pbrown@redhat.com> 3.5.6-1
- enable LFS support (debian bug #100810)
- quote filenames for running compress commands or pre/postrotate cmds (#21348)
- deprecate "errors" directive (see bug #16544 for explanation)
- update man page
- configurable compression command by Colm Buckley <colm@tuatha.org>

* Fri Jun  1 2001 Preston Brown <pbrown@redhat.com> 3.5.5-1
- be less strict about whitespace near filenames.  Patch from Paul Martin <pm@debian.org>.

* Thu Jan  4 2001 Bill Nottingham <notting@redhat.com>
- %%defattr

* Wed Jan 03 2001 Preston Brown <pbrown@redhat.com>
- see CHANGES

* Tue Aug 15 2000 Erik Troan <ewt@redhat.com>
- see CHANGES

* Sun Jul 23 2000 Erik Troan <ewt@redhat.com>
- see CHANGES

* Tue Jul 11 2000 Erik Troan <ewt@redhat.com>
- support spaces in filenames
- added sharedscripts

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- use %%{_mandir} for man pages

* Thu Feb 24 2000 Erik Troan <ewt@redhat.com>
- don't rotate lastlog

* Thu Feb 03 2000 Erik Troan <ewt@redhat.com>
- gzipped manpages
