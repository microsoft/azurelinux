Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global _unitdir /usr/lib/systemd/system
Summary: A log file analysis program
Name: logwatch
Version: 7.5.3
Release: 5%{?dist}
License: MIT
URL: https://www.logwatch.org/
Source0: https://sourceforge.net/projects/%{name}/files/%{name}-%{version}/%{name}-%{version}.tar.gz
# Temporary fix for update to DNF 4.4
Source1: dnf-rpm.conf
BuildRequires: perl-generators
Requires: grep mailx
Requires: perl(Date::Manip)
Requires: perl(Sys::CPU)
Requires: perl(Sys::MemInfo)
Requires: cronie
BuildArchitectures: noarch

%description
Logwatch is a customizable, pluggable log-monitoring system.  It will go
through your logs for a given period of time and make a report in the areas
that you wish with the detail that you wish.  Easy to use - works right out
of the package on many systems.

%prep
%setup -q
cp -p %{SOURCE1} .

%build

%install
install -m 0755 -d %{buildroot}%{_var}/cache/logwatch
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/scripts
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/scripts/services
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/conf
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/conf/logfiles
install -m 0755 -d %{buildroot}%{_sysconfdir}/logwatch/conf/services
install -m 0755 -d %{buildroot}%{_sysconfdir}/cron.daily
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/default.conf/logfiles
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/default.conf/services
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/default.conf/html
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/dist.conf/logfiles
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/dist.conf/services
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/scripts/services
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/scripts/shared
install -m 0755 -d %{buildroot}%{_datadir}/logwatch/lib
install -m 0755 -d %{buildroot}%{_sbindir}
install -m 0755 -d %{buildroot}%{_mandir}/man5
install -m 0755 -d %{buildroot}%{_mandir}/man8

for i in scripts/logfiles/*; do
    if [ $(ls $i | wc -l) -ne 0 ]; then
        install -m 0755 -d %{buildroot}%{_datadir}/logwatch/$i
        install -m 0644 $i/* %{buildroot}%{_datadir}/logwatch/$i
    fi
done

install -m 0755 scripts/logwatch.pl %{buildroot}%{_datadir}/logwatch/scripts/logwatch.pl
install -m 0644 scripts/services/* %{buildroot}%{_datadir}/logwatch/scripts/services
install -m 0644 scripts/shared/* %{buildroot}%{_datadir}/logwatch/scripts/shared

install -m 0644 conf/logwatch.conf %{buildroot}%{_datadir}/logwatch/default.conf/logwatch.conf

install -m 0644 conf/logfiles/* %{buildroot}%{_datadir}/logwatch/default.conf/logfiles
install -m 0644 conf/services/* %{buildroot}%{_datadir}/logwatch/default.conf/services
install -m 0644 conf/html/* %{buildroot}%{_datadir}/logwatch/default.conf/html

install -m 0644 lib/Logwatch.pm %{buildroot}%{_datadir}/logwatch/lib/Logwatch.pm

install -m 0644 ignore.conf.5 %{buildroot}%{_mandir}/man5
install -m 0644 override.conf.5 %{buildroot}%{_mandir}/man5
install -m 0644 logwatch.conf.5 %{buildroot}%{_mandir}/man5
install -m 0644 logwatch.8 %{buildroot}%{_mandir}/man8

install -m 0755 scheduler/logwatch.cron %{buildroot}%{_sysconfdir}/cron.daily/0logwatch
mkdir -p %{buildroot}%{_unitdir}
install -m 0755 scheduler/logwatch.timer %{buildroot}%{_unitdir}/logwatch.timer
install -m 0755 scheduler/logwatch.service %{buildroot}%{_unitdir}/logwatch.service

ln -s ../../%{_datadir}/logwatch/scripts/logwatch.pl %{buildroot}/%{_sbindir}/logwatch

echo "###### REGULAR EXPRESSIONS IN THIS FILE WILL BE TRIMMED FROM REPORT OUTPUT #####" > %{buildroot}%{_sysconfdir}/logwatch/conf/ignore.conf
echo "# Local configuration options go here (defaults are in %{_datadir}/logwatch/default.conf/logwatch.conf)" > %{buildroot}%{_sysconfdir}/logwatch/conf/logwatch.conf
echo "# Configuration overrides for specific logfiles/services may be placed here." > %{buildroot}%{_sysconfdir}/logwatch/conf/override.conf

# Fix for DNF 4.4
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}/logwatch/dist.conf/logfiles

%files
%license LICENSE
%doc README HOWTO-Customize-LogWatch
%dir %{_var}/cache/logwatch
%dir %{_sysconfdir}/logwatch
%dir %{_sysconfdir}/logwatch/scripts
%dir %{_sysconfdir}/logwatch/conf
%dir %{_sysconfdir}/logwatch/conf/logfiles
%dir %{_sysconfdir}/logwatch/conf/services
%dir %{_sysconfdir}/logwatch/scripts/services
%config(noreplace) %{_sysconfdir}/cron.daily/0logwatch
%config(noreplace) %{_sysconfdir}/logwatch/conf/*.conf
%dir %{_datadir}/logwatch
%dir %{_datadir}/logwatch/dist.conf
%dir %{_datadir}/logwatch/dist.conf/services
%dir %{_datadir}/logwatch/dist.conf/logfiles
# Fix for DNF 4.4
%{_datadir}/logwatch/dist.conf/logfiles/*.conf
%{_datadir}/logwatch/scripts/logwatch.pl
%config(noreplace) %{_datadir}/logwatch/default.conf/*.conf
%{_sbindir}/logwatch
%dir %{_datadir}/logwatch/scripts
%{_datadir}/logwatch/scripts/shared
%{_datadir}/logwatch/scripts/services
%{_datadir}/logwatch/scripts/logfiles
%dir %{_datadir}/logwatch/lib
%{_datadir}/logwatch/lib/Logwatch.pm
%dir %{_datadir}/logwatch/default.conf
%dir %{_datadir}/logwatch/default.conf/services
%{_datadir}/logwatch/default.conf/services/*.conf
%dir %{_datadir}/logwatch/default.conf/logfiles
%{_datadir}/logwatch/default.conf/logfiles/*.conf
%dir %{_datadir}/logwatch/default.conf/html
%{_datadir}/logwatch/default.conf/html/*.html
%{_mandir}/man*/*
%{_unitdir}/logwatch.service
%{_unitdir}/logwatch.timer

%changelog
* Tue Jan 10 2023 Osama Esmail <osamaesmail@microsoft.com> - 7.5.3-5
- Replacing crontabs with cronie (removing crontabs rpm because of redundancy)

* Mon Apr 25 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.5.3-4
- Updating source URLs.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 7.5.3-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Nov 23 2020 Frank Crawford <frank@crawford.emu.id.au> - 7.5.3-2
- Handle changes for DNF 4.4 (#1895839)

* Tue Feb 25 2020 Jan Synáček <jsynacek@redhat.com> - 7.5.3-1
- Update to 7.5.3 (#1800953)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Oct 25 2019 Jan Synáček <jsynacek@redhat.com> - 7.5.2-1
- Update to 7.5.2 (#1765446)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 28 2019 Jan Synáček <jsynacek@redhat.com> - 7.5.1-1
- Update to 7.5.1 (#1669972)

* Fri Jan  4 2019 Jan Synáček <jsynacek@redhat.com> - 7.5.0-1
- Update to 7.5.0 (#1663428)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Jan Synáček <jsynacek@redhat.com> - 7.4.3-10
- Fix parsing of log entries produced by sendmail process with 7-digit PID (#1561587)

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.4.3-9
- Escape macros in %%changelog

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov 07 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.4.3-7
- Remove old crufty coreutils requires

* Tue Aug 29 2017 Jan Synáček <jsynacek@redhat.com> - 7.4.3-6
- refix: sshd log format changed (#1317620)

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Nov 30 2016 Jan Synáček <jsynacek@redhat.com> - 7.4.3-3
- Add systemd journal support (#864872)

* Tue May 10 2016 Jan Synáček <jsynacek@redhat.com> - 7.4.3-2
- Fix misaligned output in postfix (#1326808)

* Thu Apr 28 2016 Jan Synáček <jsynacek@redhat.com> - 7.4.3-1
- Update to 7.4.3 (#1331255)

* Tue Mar 15 2016 Jan Synáček <jsynacek@redhat.com> - 7.4.2-2
- sshd log format changed, lots of excess unmatched output showing up in logwatch (#1317620)

* Mon Feb 29 2016 Jan Synáček <jsynacek@redhat.com> - 7.4.2-1
- Update to 7.4.2 (#1312774)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.4.1-6.20150731svn293
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Aug 25 2015 Jan Synáček <jsynacek@redhat.com> - 7.4.1-5.20150731svn293
- Fix more warnings about unescaped braces (#rhbz1237339)

* Fri Jul 31 2015 Jan Synáček <jsynacek@redhat.com> - 7.4.1-4.20150731svn293
- Update to revision 293
- Fix perl warnings about unescaped braces (#rhbz1237339)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.1-3.20140924svn242
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Sep 25 2014 Jan Synacek <jsynacek@redhat.com> - 7.4.1-2.20140924svn242
- Fix xntpd patch

* Wed Sep 24 2014 Jan Synacek <jsynacek@redhat.com> - 7.4.1-1.20140924svn242
- Update to 7.4.1 (revision 242) (rhbz#1145898)
- Fix bogus dates

* Fri Jul  4 2014 Jan Synáček <jsynacek@redhat.com> - 7.4.0-33.20140704svn198
- Fix bad backport

* Fri Jul  4 2014 Jan Synáček <jsynacek@redhat.com> - 7.4.0-32.20140704svn198
- Update to revision 198

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-31.20130522svn140
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Aug 07 2013 Pierre-Yves Chibon <pingou@pingoured.fr> 7.4.0-30.20130522svn140
- Add missing requires on crontabs
- Mark cron job as config(noreplace)
- Fix RHBZ#989075

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-29.20130522svn140
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 7.4.0-28.20130522svn140
- Perl 5.18 rebuild

* Mon Jul  1 2013 Jan Synáček <jsynacek@redhat.com> - 7.4.0-27.20130522svn140
- Remove unused patch

* Thu May 23 2013 Jan Synáček <jsynacek@redhat.com> - 7.4.0-26.20130522svn140
- Add missing options to logwatch.8

* Wed May 22 2013 Jan Synáček <jsynacek@redhat.com> - 7.4.0-25.20130522svn140
- Update to revision 140 and drop upstreamed patches
- Own directories correctly

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-24.20130102svn127
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jan 22 2013 Jan Synáček <jsynacek@redhat.com> - 7.4.0-23.20130102svn127
- Improve mdadm script

* Fri Jan 11 2013 Jan Synáček <jsynacek@redhat.com> - 7.4.0-22.20130102svn127
- Add secure-username patch to properly ignore "password check failed for user"
  (rhbz#894272)
- Fix dovecot timestamp misparsing (related: rhbz#886193)

* Wed Jan 09 2013 Jan Synáček <jsynacek@redhat.com> - 7.4.0-21.20130102svn127
- Update to revision 127 and drop ustreamed patches
- Update dovecot patch

* Mon Dec 10 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-20.20120619svn110
- Comment patches

* Tue Dec 04 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-19.20120619svn110
- Don't use ApplyhttpDate (rhbz#881111)

* Mon Oct 22 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-18.20120619svn110
- Add secure-userhelper patch: Fix misparsing userhelper log entries
  (rhbz#867290)

* Thu Sep 27 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-17.20120619svn110
- Add secure patch (rhbz#836189)
- Add pam_unix patch (rhbz#836183, rhbz#846725)

* Wed Aug 29 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-16.20120619svn110
- Add applystddate patch - support rsyslog timestamps
- Add http patch - count .hdr files as archives
- Add pluto patch - update openswan parsing
- Add xvc patch - support xen virtual console logins

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.4.0-15.20120619svn110
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 19 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-14.20120619svn110
- Remove defattr to comply with Fedora Packaging Guidelines

* Wed Jun 27 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-14.20120619svn110
- Add rhhunter patch (rhbz#818926)

* Tue Jun 19 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-13.20120619svn110
- Update to revision 110
- Drop unnecessary patches
- Add proper requires

* Fri May 04 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-12.20120425svn100
- Update secure-update patch
- Update systemd-logind patch

* Fri Apr 27 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-11.20120425svn100
- Add dovecot-proxy patch (rhbz#812883)
- Add secure-update patch (rhbz#809314)
- Add mail-headers patch (rhbz#811185)
- Add systemd-logind patch (rhbz#812880)
- Add sshd-undef patch (rhbz#783528)

* Wed Apr 25 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-10.20120425svn100
- Update to revision 100
- Update logwatch-named-dnssec.patch

* Thu Mar 01 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-9.20120229svn85
- Get the release version right this time

* Thu Mar 01 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-7.20120229svn85
- Bump release version, so yum doesn't get confused when upgrading

* Wed Feb 29 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-1.20120229svn85
- Update to revision 85
- Drop sendmail patch
- Update xntpd,secure and dovecot patches

* Wed Jan 04 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-8.20110328svn50
- Updated -manpage patch (rhbz#719061)

* Wed Jan 04 2012 Jan Synáček <jsynacek@redhat.com> - 7.4.0-7.20110328svn50
- Renamed sendmail patch to match other patches' naming convention
- Added -secure-grammar patch (rhbz#716224)

* Mon Dec 19 2011 Jan Synáček <jsynacek@redhat.com> - 7.4.0-6.20110328svn50
- Added -sendmail-typo patch (rhbz#708183)

* Sat Apr 30 2011 Frank Crawford <frank@crawford.emu.id.au> - 7.4.0-5.20110328svn50
- Added -sshd patch to match more pam_systemd messages (rhbz#699558)
- Updated logwatch.spec to create empty files in /etc/logwatch/conf

* Tue Apr 26 2011 Frank Crawford <frank@crawford.emu.id.au> - 7.4.0-4.20110328svn50
- Updated -secure patch to match more pam_systemd messages

* Tue Apr 26 2011 Frank Crawford <frank@crawford.emu.id.au> - 7.4.0-3.20110328svn50
- Updated -secure patch for pam_systemd messages (rhbz#699558)
- Updated -dovecot patch for extended starting message from upstream

* Thu Mar 31 2011 Karel Klíč <kklic@redhat.com> - 7.4.0-2.20110328svn50
- Added -dovecot patch to handle directory names with whitespaces (rhbz#645962)

* Mon Mar 28 2011 Karel Klíč <kklic@redhat.com> - 7.4.0-1.20110328svn50
- Moved to the latest upstream SVN version

* Mon Mar 28 2011 Karel Klíč <kklic@redhat.com> - 7.3.6-71.20110228svn46
- Added -smartd patch to suppress copyright message for smartd module (rhbz#673758)

* Mon Mar 28 2011 Karel Klíč <kklic@redhat.com> - 7.3.6-70.20110228svn46
- Added -xntpd patch (rhbz#673756)

* Mon Mar 28 2011 Karel Klíč <kklic@redhat.com> - 7.3.6-69.20110228svn46
- Added -manpage patch fixing a typo in logwatch(8) (rhbz#664883)
- Removed `rm -rf %%{buildroot}` from %%install section

* Mon Mar 28 2011 Karel Klíč <kklic@redhat.com> - 7.3.6-68.20110228svn46
- Added -named-dnessec patch to handle DNSSEC messages in named (rhbz#666394)

* Sun Mar  6 2011 Frank Crawford <frank@crawford.emu.id.au> -  7.3.6-67.20110228svn46
- Handle additional messages in /var/log/secure (rhbz#673760)

* Mon Feb 28 2011 Karel Klic <kklic@redhat.com> -  7.3.6-66.20110228svn46
- Updated to the latest svn revision
- Fixes CVE-2011-1018: Privilege escalation due improper sanitization
  of special characters in log file names (rhbz#680237)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3.6-65.20110203svn25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb  3 2011 Karel Klic <kklic@redhat.com> - 7.3.6-64.20110203svn25
- Updated to the latest svn revision, removed dhcpd patch merged by
  upstream
- Added LICENSE file, which became available in this revision

* Wed Feb  2 2011 Karel Klic <kklic@redhat.com> - 7.3.6-63.20110201svn23
- Updated to the latest svn revision, removed patches merged by upstream

* Sun Jan 23 2011 Richard Fearn <richardfearn@gmail.com> - 7.3.6-62.20110113svn22
- Fix rhbz#671201: make /etc/cron.daily/0logwatch executable

* Tue Jan 18 2011 Karel Klic <kklic@redhat.com> - 7.3.6-61.20110113svn22
- Removed "Listening on interface .* Enabled" line in logwatch-xntpd.patch

* Mon Jan 17 2011 Karel Klic <kklic@redhat.com> - 7.3.6-60.20110113svn22
- Added logwatch-pam_unix.patch by Frank Crawford (rhbz#666586), modified

* Thu Jan 13 2011 Karel Klic <kklic@redhat.com> - 7.3.6-59.20110113svn22
- Correct date in the release number

* Thu Jan 13 2011 Karel Klic <kklic@redhat.com> - 7.3.6-59.20100113svn22
- Updated to the latest SVN upstream revision
- Removed patches merged by upstream
- Removed logwatch-7.3.6-usage.patch, because --usage works in the new
  version
- Removed logwatch-7.3.6-cron_conf.patch, because logwatch already
  handles the same problem, only differently
- Removed logwatch-7.3.6-sendmail.patch: if the log level becomes
  problem again, it should be fixed differently
- Removed Fedora-specific /etc/logwatch/conf/{logwatch,ignore}.conf,
  upstream version is used instead
- Renamed logwatch-7.3.1-vsftpd.patch to logwatch-vsftpd.patch,
  logwatch-7.3.6-oldfiles.patch to logwatch-oldfiles.patch, and
  logwatch-7.3.6-postfix.patch to logwatch-postfix.patch, because
  versioning no longer makes sense in Logwatch (the patches does not
  necessarily apply to the last officially released version);
  all patches updated to apply on the latest sources
- Added logwatch-automount.patch by Frank Crawford (rhbz#666582)
- Added logwatch-dhcpd.patch by Frank Crawford (rhbz#666393)
- Added logwatch-dovecot.patch by Frank Crawford (rhbz#666376)
- Added logwatch-smartd.patch by Frank Crawford (rhbz#666382)
- Added logwatch-xntpd.patch by Frank Crawford (rhbz#666498)
- Added logwatch-dovecot2.patch

* Sat Oct  9 2010 Richard Fearn <richardfearn@gmail.com> 7.3.6-58
- named: match "DNS format error", and variants of existing messages
  (rhbz#595222)

* Sat Oct  9 2010 Richard Fearn <richardfearn@gmail.com> 7.3.6-57
- named: match "clients-per-query increased" as well as "decreased"

* Sat Oct  9 2010 Richard Fearn <richardfearn@gmail.com> 7.3.6-56
- Update dhcpd patch so that "Information-request" messages are matched
  (rhbz#624590)

* Thu Aug 19 2010 Karel Klic <kklic@redhat.com> 7.3.6-55
- Removed BuildRoot tag and %%clean section
- Deleted trailing whitespaces in the spec file
- Updated patch upstream status
- Added fetchmail service (rhbz#528838)

* Mon Apr 19 2010 Karel Klic <kklic@redhat.com> 7.3.6-54
- Do not install zz-fortune service when %%{rhel} is defined.

* Mon Apr 19 2010 Karel Klic <kklic@redhat.com> 7.3.6-53
- Removed zz-fortune patch as zz-disk_space is run every
  time anyway.

* Fri Apr 16 2010 Karel Klic <kklic@redhat.com> 7.3.6-52
- Updated the previously added patches to apply with --fuzz=0

* Wed Apr 14 2010 Karel Klic <kklic@redhat.com> 7.3.6-51
- Re-enabled zz-fortune with a patch that prevents sending reports
  containing zz-fortune only (rhbz#573450)
- Removed obsolete chmod and touch calls from the spec file
- Added manpages for configuration files (rhbz#525644)
- Ignore broken trust chain messages in named service (rhbz#581186)

* Mon Feb  1 2010 Karel Klic <kklic@redhat.com> 7.3.6-50
- Added patch from #555750: Not all methods to deny login via sshd are reported
- Added patch from #555735: DHCPDv6 messages are not recognised
- Removed logwatch-7.3.6-dhcpd.patch, obsoleted by #555735
- Added lines from #550873 to the logwatch-7.3.6-named6.patch
- Added named7 patch from #555980
- Added dovecot3 patch from #555745
- Added sendmail2 patch from #555753

* Wed Dec  2 2009 Karel Klic <kklic@redhat.com> 7.3.6-49
- Add 802.1q subinterface support to iptables report; iptables.patch (#507743)
- Fixed error in the RE that matches "lost connection" lines in postfix script; lost-connection.patch (#525903)
- Added patches parsing several unmatched entries (from F-10);
  audit4.patch modified to make ppid optional;
  openvpn4.patch modified to make "semi-" optional;
  pam_unix4.patch modified (user name matched by \S+)

* Tue Aug 11 2009 Ivana Varekova <varekova@redhat.com> 7.3.6-48
- parse a few unmatched entries in named script (#513853)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3.6-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul  7 2009 Ivana Varekova <varekova@redhat.com> 7.3.6-46
- fix cron script

* Thu Jul  2 2009 Ivana Varekova <varekova@redhat.com> 7.3.6-45
- fix cron script

* Thu Jun 25 2009 Ivana Varekova <varekova@redhat.com> 7.3.6-44
- add the possibility to switch of cron job (#493063)

* Mon Jun 15 2009 Ivana Varekova <varekova@redhat.com> 7.3.6-43
- fix removeservice script - to decrease the number of
  perl instances running simultaneously

* Tue Mar 31 2009 Ivana Varekova <varekova@redhat.com> 7.3.6-42
- fix exim script (#492269)

* Mon Mar 30 2009 Ivana Varekova <varekova@redhta.com> 7.3.6-41
- fix sshd script (#492738)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.3.6-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan  6 2009 Ivana Varekova <varekova@redhat.com> 7.3.6-39
- fix smartd script

* Tue Dec 16 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-38
- remove obsolete patches
- fix dovecot,named and openvpn scrpts(#476620)

* Mon Dec  8 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-37
- fix zz-disk_space script (#474810)

* Thu Nov 13 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-35
- fix exim script

* Tue Nov 11 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-34
- fix pam-unix script patches

* Thu Oct 30 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-33
- mark logwatch.conf as a configure file (#468655)

* Wed Oct 29 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-32
- parse another postfix log, do postfix patches cleanup

* Fri Oct 24 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-31
- parse another bunch of postfix logs(#467378)

* Tue Oct 21 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-30
- fix secure, pam_unix and init scripts

* Fri Oct 17 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-29
- fix postfix script again (#462174)

* Mon Sep 15 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-28
- fix postfix script problem
  (#462174)

* Tue Aug 26 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-27
- fix init script problem
  (#459887)

* Fri Aug 15 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-26
- fix problem with changed logrotate suffixes (#458580)

* Wed Aug  6 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-25
- add cron service patch to parse more logs

* Fri Jun 20 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-24
- Resolves: #452044
  handle 2.6.25+ audit messages
- add init script logs parsing

* Tue Jun 10 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-23
- Resolves: #450494
  MailTo configuration parameter is ignored

* Wed Apr 30 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-22
- Resolves: #436719
  Logwatch doesn't show any usable sendmail section

* Fri Apr  4 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-21
- Resolves: #440534
  Some unmatched OpenVPN log lines
- add parsing of new logw to audit and cron service

* Wed Mar  5 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-20
- Resolves: #436058
  dovecot script for logwatch needs fix for IPv6

* Thu Feb 14 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-19
- resolves cron service problem (#432766)

* Mon Jan 28 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-18
- resolves: #429933 fix postfix script
  thanks Benjamin Gordon

* Mon Jan 21 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-17
- Resolves: #427734
  fix amavis script
- Resolves: #429452
  fix openvpn script

* Tue Jan  8 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-16
- Resolves: #427734
  fix amavis script
- Resolves: #427761
  remove *.orig scripts
- Resolves: #230974
  add no-oldfiles-log option
- remove usage option description
- Resolves: #427596
  fix mailto setting

* Wed Jan  2 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-15
- Resolves: #424171
  logwatch doesn't recognize dovecot starting up message ..

* Wed Jan  2 2008 Ivana Varekova <varekova@redhat.com> 7.3.6-14
- Resolves: #426857
  is report cdrom "disk full" necessary

* Thu Nov 22 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-13
- fix pam_unix script output (#389311)

* Tue Nov 13 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-12
- change Print configuration (#378901)

* Tue Nov  6 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-11
- Resolves: #361921
  fix clamav-milter service

* Tue Oct 30 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-10
- add perl requirement (#356481)

* Fri Oct 12 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-9
- add sshd service patch
- add sudo service patch

* Wed Oct 10 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-8
- add secure service patch

* Wed Oct 10 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-7
- add cron service patch
- add pam-unix service patch

* Thu Aug  9 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-6
- add cron patch

* Tue Jul 10 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-5
- Resolves: #247511
  add zz-disk_space patch

* Tue Jul 10 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-4
- Resolves: #246655
  add cron service patch

* Wed Jul  4 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-3
- add named, pam_unix and audit service patches

* Mon Jun  4 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-2
- fix secure script
- Resolves: #242201
  fix named service

* Tue May 22 2007 Ivana Varekova <varekova@redhat.com> 7.3.6-1
- update to 7.3.6

* Mon May  7 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-8
- add named and sshd service patches

* Fri Apr 20 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-7
- Resolves: 236618
  (add anacron setting of mailto accept)
  thanks Todd Denniston

* Fri Apr 13 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-6
- remove another xntpd service logs
- add sshd logs with two spaces after the date tag

* Tue Apr 10 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-5
- logwatch will ignore more useless secure logs

* Wed Apr  4 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-4
- Resolves 234875
  logwatch warns about ntpd startup messages

* Mon Apr  2 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-3
- Resolves: 234767
  Unmatched Entries in mails since sysklogd 1.4.2-3/#223573

* Thu Mar  8 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-2
- add pam_unix service patch

* Tue Feb 20 2007 Ivana Varekova <varekova@redhat.com> 7.3.4-1
- update to 7.3.4

* Mon Feb 12 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-9
- Resolves: 228258
  logwatch warns about dhcdbd subscripton enabled
- add xntpd, up2date and automount services

* Fri Feb  9 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-8
- incorporate the next part of package review comments
- Resolves: 227976
  logwatch warns about auditspd starting

* Thu Feb  8 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-7
- incorporate package review feedback
- Resolves: 227814
  logwatch warns about ntpd deletes interfaces on shutdown

* Mon Feb  5 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-6
- Resolves: 226999
  fix audit script

* Fri Jan 26 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-5
- add sendmail, automount, amvais and cron patch

* Wed Jan 17 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-4
- add xntpd patch

* Tue Jan 16 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-3
- Resolves: 222263
  sshd script problem

* Fri Jan  5 2007 Ivana Varekova <varekova@redhat.com> 7.3.2-2
- Resolves: 221576
  add html conf files

* Thu Dec 21 2006 Ivana Varekova <varekova@redhat.com> 7.3.2-1
- update to 7.3.2
- remove obsolete patches

* Wed Dec 20 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-9
- add cron, pam_unix, audit, init service patches

* Wed Dec 20 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-8
- add dovecot, amavis and init patch
- cleanup spec file

* Wed Nov 29 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-7
- add postfix service patch (#208909)
- add vsftpd service patch (#217226)

* Tue Nov 28 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-6
- add automount and mountd service patch

* Wed Nov  1 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-5
- fix named patch (#213267)
- add openvpn patch

* Mon Oct 30 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-4
- fix #209405 - another sendmail service problem
- fix #212812 - add service script patch
    patch created by Russell Coker

* Mon Oct 23 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-3
- fix #209405 - sendmail service problems

* Fri Oct 20 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-2
- fix #204078 - missing /etc/logwatch/scripts/services
- add yum service patch
- fix #209554 - automount service problem

* Fri Oct 20 2006 Ivana Varekova <varekova@redhat.com> 7.3.1-1
- update to 7.3.1

* Tue Aug 29 2006 Ivana Varekova <varekova@redhat.com> 7.3-5
- fix amavis problem #204432

* Mon Aug 14 2006 Marcela Maslanova <mmaslano@redhat.com> 7.3-4
- add audit patch for SElinux (#200116)
- add patch for sshd (#200105)
- add patch from bugzilla, made by Allen Kistler (#200147)

* Fri Jun 23 2006 Ivana Varekova <varekova@redhat.com> 7.3-3
- added secure-service patch

* Fri May  5 2006 Ivana Varekova <varekova@redhat.com> 7.3-2
- added tests to file creation and access, clean up
resulting files when logwatch fails (upstream change)
(#190498)

* Mon Mar 27 2006 Ivana Varekova <varekova@redhat.com> 7.3-1
- update to 7.3
- added samba, up2date

* Fri Mar 17 2006 Ivana Varekova <varekova@redhat.com> 7.2.1-1
- update to 7.2.1
- update nosegfault, pam_unix, http patches
- added sshd, smart, named, audit, secure and mountd services
  patches

* Mon Feb 20 2006 Ivana Varekova <varekova@redhat.com> 7.1-8
- fix http exploit problem #181802

* Fri Jan 20 2006 Ivana Varekova <varekova@redhat.com> 7.1-7
- extended pam_unix patch (fix sshd service)

* Wed Jan 18 2006 Ivana Varekova <varekova@redhat.com> 7.1-6
- removed nounicode patch
- added patch to fix pam_unix logs parsing (#178058)

* Fri Dec 23 2005 Ivana Varekova <varekova@redhat.com> 7.1-5
- fix http exploits problem (bug 176324 - comment 2)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec  8 2005 Ivana Varekova <varekova@redhat.com> 7.1-4
- updated /etc/.../logwatch.conf file (bug 175233)

* Tue Nov 29 2005 Ivana Varekova <varekova@redhat.com> 7.1-3
- add secure service patch
- add iptables patch created by Allen Kistler (bug 174954)
- add audit service patch

* Thu Nov 24 2005 Ivana Varekova <varekova@redhat.com> 7.1-2
- add named script patch (bug 171631)
- change autdated description

* Wed Nov 23 2005 Ivana Varekova <varekova@redhat.com> 7.1-1
- update to 7.1
- added sshd and samba patches

* Wed Nov  2 2005 Ivana Varekova <varekova@redhat.com> 7.0-2
- fix zz-disk_space problem (bug 172230)
  used michal@harddata.com patch
- fix a few inconsistencies with new directory structure
- changed previous zz-disk_space
- add secure sript patch allow case insensitivity for GID, UID)

* Thu Oct 13 2005 Ivana Varekova <varekova@redhat.com> 7.0-1
- update to 7.0 (new directory structure)
- add smartd and zz-disk_space patch

* Mon Oct  3 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-7
- add audit script patch recognized other unmatched logs
- add cron script patch
- change sshd script patch

* Fri Sep 30 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-6
- add audit script patch to recognize number of unmatched entries

* Mon Sep 26 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-5
- change secure script patch
- add sshd script patch (sshd part should not display 0.0.0.0
   in "Failed to bind" column)
- add one unmatch line to named script

* Mon Sep 19 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-4
- fixed secure script (part of bug 141116, added a few
  unknown logs)
- bug 168469 - fixed up2date script

* Mon Jul 25 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-3
- bug 162689 - add noreplace option

* Wed Jun 29 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-2
- fix bug 161973 - The logwatch yum service doesn't properly
show removed entries
- used patch created by Dean Earley (patch5)

* Thu Jun 23 2005 Ivana Varekova <varekova@redhat.com> 6.1.2-1
- update to 6.1.2-1

* Thu May 19 2005 Jiri Ryska <jryska@redhat.com> 6.0.1-2
- fixed temp dir creation #155795

* Fri Apr 15 2005 Jiri Ryska <jryska@redhat.com> 6.0.1-1
- update to 6.0.1

* Tue Nov 09 2004 Jiri Ryska <jryska@redhat.com>
- Patch for #134288, #138285

* Wed Jul 14 2004 Elliot Lee <sopwith@redhat.com> 5.2.2-1
- Update to 5.2.2
- Patch for #126558, #101744

* Wed Jul 07 2004 Elliot Lee <sopwith@redhat.com> 5.1-6
- Extra patch from #80496

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 24 2004 Joe Orton <jorton@redhat.com> 5.1-4
- stop logging access_log entries with 2xx response codes

* Wed Mar 17 2004 Elliot Lee <sopwith@redhat.com> 5.1-3
- Fix the perl(Logwatch) problem the correct way, as per #118507

* Mon Mar 15 2004 Elliot Lee <sopwith@redhat.com> 5.1-2
- Add provides perl(Logwatch)

* Fri Mar 12 2004 Elliot Lee <sopwith@redhat.com> 5.1-1
- Update (#113802)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Sep 05 2003 Elliot Lee <sopwith@redhat.com> 4.3.2-4
- Fix #103720

* Wed Aug 13 2003 Elliot Lee <sopwith@redhat.com> 4.3.2-3
- Fix a reported bug about MsgsSent/BytesTransferred stats not
  counting locally-originated traffic.

* Thu Jul 10 2003 Elliot Lee <sopwith@redhat.com> 4.3.2-2
- Fix #81144 (nounicode), #85551 and part of #97421 (nosegfault), #87483 (funkyhn)

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Elliot Lee <sopwith@redhat.com> 4.3.1-1
- Update to new upstream version

* Tue Dec 10 2002 Elliot Lee <sopwith@redhat.com> 4.0.3-3
- Apply patch from #77173

* Wed Oct 16 2002 Elliot Lee <sopwith@redhat.com> 4.0.3-2
- Update to new upstream version

* Thu Aug 08 2002 Elliot Lee <sopwith@redhat.com> 2.6-8
- Apply patch from #68804, #68806

* Mon Jul 15 2002 Elliot Lee <sopwith@redhat.com> 2.6-7
- Fix #68869 (the other half of the expandrepeats job)

* Thu Jul 11 2002 Elliot Lee <sopwith@redhat.com> 2.6-6
- Remove expandrepeats (#67606)
- Patch6 (ftpd-messages.patch) from #68243

* Thu Jun 27 2002 Elliot Lee <sopwith@redhat.com> 2.6-5
- logwatch-2.6-applydate-65655.patch to fix xferlog date parsing
- logwatch-2.6-xinetd_match-65856.patch to match more xinetd lines properly
- logwatch-2.6-confparse-65937.patch to properly parse lines with multiple
  = chars in them

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Apr 15 2002 Elliot Lee <sopwith@redhat.com> 2.6-2
- Fix #62787 (logwatch-2.6-newline-62787.patch) and #63279 (logwatch-2.6-applystddate-63279.patch)

* Sun Mar 31 2002 Elliot Lee <sopwith@redhat.com> 2.6-1
- Don't trust homebaked tempdir creation - always use mktemp.

* Thu Mar 28 2002 Elliot Lee <sopwith@redhat.com> 2.5-4
- Fix the /tmp race for real
- Merge changes from both spec files.

* Thu Mar 28 2002 Kirk Bauer <kirk@kaybee.org> 2.5-2
- Updated new changes from Red Hat's rawhide packaging

* Tue Sep 04 2001 Elliot Lee <sopwith@redhat.com> 2.1.1-3
- Fix #53077

* Thu Aug 09 2001 Elliot Lee <sopwith@redhat.com> 2.1.1-2
- Fix warning in services/init (#51305) and don't include fortune module
(#51093).

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- updated to 2.1.1
- adapted changes from Kirk Bauer's spec file into this one

* Sat Aug 5 2000 Tim Powers <timp@redhat.com>
- fix bug #15478, spelling error in the description

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jun 8 2000 Tim Powers <timp@redhat.com>
- fixed man page location to be FHS compliant
- use predefined RPM macros whenever possible

* Mon May 15 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0

* Mon Jul 19 1999 Tim Powers <timp@redhat.com>
- rebuilt for 6.1

* Thu Apr 15 1999 Michael Maher <mike@redhat.com>
- built package for 6.0
- updated source

* Wed Nov 18 1998 Kirk Bauer <kirk@kaybee.org>
- Modified to comply with RHCN standards

* Fri Oct 2 1998 Michael Maher <mike@redhat.com>
- built package

* Mon Feb 23 1998 Kirk Bauer <kirk@kaybee.org>
- Minor changes and addition of man-page

* Sun Feb 22 1998 Kirk Bauer <kirk@kaybee.org>
- initial release
