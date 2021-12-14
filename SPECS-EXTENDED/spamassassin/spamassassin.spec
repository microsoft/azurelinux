Vendor:         Microsoft Corporation
Distribution:   Mariner
# OVERRIDE RHEL VERSION HERE, RHEL BUILDSYSTEM DOESN'T HAVE DIST TAG
#%%define rhel 4

# Define dist tags for old RHEL releases
%if 0%{?rhel} == 4
%define dist .el4
%endif
%if 0%{?rhel} == 5
%define dist .el5
%endif
%if 0%{?rhel} == 6
%define dist .el6
%endif

# Define variables to use in conditionals
%define option_ssl 0
%define perl_devel 0
%define dkim_deps  0
%global patricia_deps 0
%global razor_deps 0
%define require_encode_detect 0
%define use_systemd 0

# SSL and IPv6 (FC6+, RHEL5+)

%define option_ssl 1


# Split perl-devel (FC7+ and RHEL-8+)

%define perl_devel 1


# Encode::Detect, not strictly required but helpful if you enable language detection (FC7+)

%define require_encode_detect 1


# Mail::DKIM by default (F11+)

%define dkim_deps 1



%define use_systemd 1


%if ! 0%{?rhel}
%global patricia_deps 1
%global razor_deps 1
%endif

%define real_name Mail-SpamAssassin
%{!?perl_vendorlib: %define perl_vendorlib %(eval "`%{__perl} -V:installvendorlib`"; echo $installvendorlib)}

%global saversion 3.004004
#%%global prerev rc2

Summary: Spam filter for email which can be invoked from mail delivery agents
Name: spamassassin
Version: 3.4.4
#Release: 0.8.%%{prerev}%%{?dist}
Release: 2%{?dist}
License: ASL 2.0
URL: https://spamassassin.apache.org/
Source0: https://www.apache.org/dist/%{name}/source/%{real_name}-%{version}.tar.bz2
#Source0: %%{real_name}-%%{version}-%%{prerev}.tar.bz2
Source1: https://www.apache.org/dist/%{name}/source/%{real_name}-rules-%{version}.r1873061.tgz
#Source1: %%{real_name}-rules-%%{version}.%%{prerev}.tgz
Source2: redhat_local.cf
Source3: spamassassin-default.rc
Source4: spamassassin-spamc.rc
Source5: spamassassin.sysconfig
Source6: sa-update.logrotate
Source7: sa-update.crontab
Source8: sa-update.cronscript
Source9: sa-update.force-sysconfig
Source10: spamassassin-helper.sh
Source11: spamassassin-official.conf
Source13: README.RHEL.Fedora
%if %{use_systemd}
Source14: spamassassin.service
%endif
Source15: spamassassin.sysconfig.el
Source16: sa-update.service
Source17: sa-update.timer

# Patches 0-99 are RH specific
# https://bugzilla.redhat.com/show_bug.cgi?id=1055593
# Switch to using gnupg2 instead of gnupg1
Patch0: spamassassin-3.3.2-gnupg2.patch
Patch1: spamassassin-3.4.1-add-logfile-homedir-options.patch
# Patches 100+ are SVN backports (DO NOT REUSE!)
# end of patches
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%if %{use_systemd} == 0
Requires: /sbin/chkconfig /sbin/service
%endif
Requires(post): diffutils

BuildRequires: gcc
BuildRequires: perl-interpreter >= 2:5.8.0
BuildRequires: perl-generators
BuildRequires: perl(Net::DNS)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(HTML::Parser)
BuildRequires: perl(NetAddr::IP)
BuildRequires: openssl-devel
# These are here for config checking, they are only really needed as Requires (runtime)
BuildRequires: perl(DB_File)
BuildRequires: perl(Mail::SPF)
BuildRequires: perl(Net::CIDR::Lite)
BuildRequires: perl(LWP::UserAgent)
BuildRequires: perl(Digest::SHA1)
BuildRequires: perl(Test::More)
# Fedora package needs fixing before we can depend on it
#BuildRequires: re2c
%if %{use_systemd}
BuildRequires: systemd-units
%endif

Requires: perl(HTTP::Date)
Requires: perl(LWP::UserAgent)
Requires: perl(Net::DNS)
Requires: perl(Time::HiRes)
Requires: perl(DB_File)
Requires: perl(Mail::SPF)
Requires: perl(Net::CIDR::Lite)
%if %{require_encode_detect}
Requires: perl(Encode::Detect)
%endif
Requires: perl(BSD::Resource)
Requires: procmail
Requires: gnupg2
Requires: perl(XSLoader)
Requires: perl(ExtUtils::MakeMaker)
# Fedora package needs fixing before we can depend on it
#Requires: re2c

# Hard requirements
BuildRequires: perl-HTML-Parser >= 3.43
Requires: perl-HTML-Parser >= 3.43
BuildRequires: perl(Archive::Tar)
Requires: perl(Archive::Tar)

# Optional requirements that might make things better/faster
%if %{patricia_deps}
Requires: perl(Net::Patricia)
BuildRequires: perl(Net::Patricia)
%endif
%if %{razor_deps}
Requires: perl-Razor-Agent
BuildRequires: perl-Razor-Agent
%endif

%if %{option_ssl}
# Needed for spamc/spamd SSL
Requires: perl(IO::Socket::SSL)
BuildRequires: perl(IO::Socket::SSL)
# Needed for IPv6
Requires: perl(IO::Socket::INET6)
BuildRequires: perl(IO::Socket::INET6)
%endif
%if %{perl_devel}
BuildRequires: perl-devel
%endif
# Mail::DKIM for F12+, works from RHEL5+ from EPEL5 but we don't require them
%if %{dkim_deps}
Requires: perl(Mail::DKIM)
BuildRequires: perl(Mail::DKIM)
%endif

%if %{use_systemd}
Requires(post): systemd-units
Requires(post): systemd-sysv
Requires(preun): systemd-units
Requires(postun): systemd-units
%endif

# For completeness, explicitly require perl modules already
# pulled in by perl-interpreter
Requires: perl(Digest::SHA)
Requires: perl(Socket)
Requires: perl(Data::Dumper)
Requires: perl(Digest::MD5)
Requires: perl(Errno)
Requires: perl(Exporter)
Requires: perl(List::Util)

%description
SpamAssassin provides you with a way to reduce if not completely eliminate
Unsolicited Commercial Email (SPAM) from your incoming email.  It can
be invoked by a MDA such as sendmail or postfix, or can be called from
a procmail script, .forward file, etc.  It uses a genetic-algorithm
evolved scoring system to identify messages which look spammy, then
adds headers to the message so they can be filtered by the user's mail
reading software.  This distribution includes the spamd/spamc components
which create a server that considerably speeds processing of mail.

To enable spamassassin, if you are receiving mail locally, simply add
this line to your ~/.procmailrc:
INCLUDERC=/etc/mail/spamassassin/spamassassin-default.rc

To filter spam for all users, add that line to /etc/procmailrc
(creating if necessary).

%prep
%setup -q -n Mail-SpamAssassin-%{version}
# Patches 0-99 are RH specific
%patch0 -p1
%patch1 -p1
# Patches 100+ are SVN backports (DO NOT REUSE!)
# end of patches

echo "RHEL=%{?rhel} FEDORA=%{?fedora}"

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="%{build_ldflags}"
%{__perl} Makefile.PL DESTDIR=$RPM_BUILD_ROOT/ SYSCONFDIR=%{_sysconfdir} INSTALLDIRS=vendor ENABLE_SSL="yes" < /dev/null
%{__make} OPTIMIZE="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall PREFIX=%buildroot/%{prefix} \
        INSTALLMAN1DIR=%buildroot/%{_mandir}/man1 \
        INSTALLMAN3DIR=%buildroot/%{_mandir}/man3 \
        LOCAL_RULES_DIR=%{buildroot}/etc/mail/spamassassin
chmod 755 %buildroot/%{_bindir}/* # allow stripping

%if %{use_systemd} == 0
install -d %buildroot/%{_initrddir}
install -m 0755 spamd/redhat-rc-script.sh %buildroot/%{_initrddir}/spamassassin
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin/local.cf
%if %{use_systemd}
install -m644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/spamassassin
%else
install -m644 %{SOURCE15} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/spamassassin
%endif

install -m 0644 %{SOURCE3} %buildroot/etc/mail/spamassassin
install -m 0644 %{SOURCE4} %buildroot/etc/mail/spamassassin
# installed mode 755 as it's executed by users. 
install -m 0755 %{SOURCE10} %buildroot/etc/mail/spamassassin
install -m 0644 %{SOURCE6} %buildroot/etc/logrotate.d/sa-update


%if %{use_systemd} == 0
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.d
install -m 0644 %{SOURCE7} %buildroot/etc/cron.d/sa-update
%endif
install -m 0644 %{SOURCE9} %buildroot%{_sysconfdir}/sysconfig/sa-update
# installed mode 744 as non root users can't run it, but can read it.
install -m 0744 %{SOURCE8} %buildroot%{_datadir}/spamassassin/sa-update.cron
%if %{use_systemd}
mkdir -p %buildroot%{_unitdir}
install -m 0644 %{SOURCE14} %buildroot%{_unitdir}/spamassassin.service
install -m 0644 %{SOURCE16} %buildroot%{_unitdir}/sa-update.service
install -m 0644 %{SOURCE17} %buildroot%{_unitdir}/sa-update.timer
%endif

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'

# Default rules from separate tarball
cd $RPM_BUILD_ROOT%{_datadir}/spamassassin/
tar xfvz %{SOURCE1}
sed -i -e 's|\@\@VERSION\@\@|%{saversion}|' *.cf
cd -

find $RPM_BUILD_ROOT/usr -type f -print |
        sed "s@^$RPM_BUILD_ROOT@@g" |
        grep -v perllocal.pod |
        grep -v "\.packlist" > %{name}-%{version}-filelist
if [ "$(cat %{name}-%{version}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi
find $RPM_BUILD_ROOT%{perl_vendorlib}/* -type d -print |
        sed "s@^$RPM_BUILD_ROOT@%dir @g" >> %{name}-%{version}-filelist

mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/spamassassin

# sa-update channels and keyring directory
mkdir   -m 0700             $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin/sa-update-keys/
mkdir   -m 0755             $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin/channel.d/
install -m 0644 %{SOURCE11} $RPM_BUILD_ROOT%{_sysconfdir}/mail/spamassassin/channel.d/

install -m 0644 %{SOURCE13} $RPM_BUILD_DIR/Mail-SpamAssassin-%{version}/
%if %{razor_deps}
mkdir   -m 0700 -p          $RPM_BUILD_ROOT%{_sharedstatedir}/razor/
%endif

%files -f %{name}-%{version}-filelist
%doc LICENSE NOTICE CREDITS Changes README TRADEMARK UPGRADE
%doc USAGE sample-nonspam.txt sample-spam.txt 
%doc README.RHEL.Fedora
%if %{use_systemd} == 0
%{_initrddir}/spamassassin
%{_sysconfdir}/cron.d/sa-update
%endif
%dir %{_sysconfdir}/mail
%config(noreplace) %{_sysconfdir}/mail/spamassassin
%config(noreplace) %{_sysconfdir}/sysconfig/spamassassin
%config(noreplace) %{_sysconfdir}/sysconfig/sa-update
%dir %{_datadir}/spamassassin
%dir %{_localstatedir}/lib/spamassassin
%if %{razor_deps}
%dir %{_sharedstatedir}/razor
%endif
%config(noreplace) %{_sysconfdir}/logrotate.d/sa-update
%if %{use_systemd}
%{_unitdir}/spamassassin.service
%{_unitdir}/sa-update.service
%{_unitdir}/sa-update.timer
%endif

%post
%if %{use_systemd} == 0
/sbin/chkconfig --add spamassassin
%endif

%if %{use_systemd}
%systemd_post spamassassin.service
%systemd_post sa-update.timer
%endif

# -a and --auto-whitelist options were removed from 3.0.0
# prevent service startup failure
TMPFILE=$(/bin/mktemp /etc/sysconfig/spamassassin.XXXXXX) || exit 1
cp /etc/sysconfig/spamassassin $TMPFILE
perl -p -i -e 's/(["\s]-\w+)a/$1/ ; s/(["\s]-)a(\w+)/$1$2/ ; s/(["\s])-a\b/$1/' $TMPFILE
perl -p -i -e 's/ --auto-whitelist//' $TMPFILE
# replace /etc/sysconfig/spamassassin only if it actually changed
cmp /etc/sysconfig/spamassassin $TMPFILE || cp $TMPFILE /etc/sysconfig/spamassassin
rm $TMPFILE

if [ -f /etc/spamassassin.cf ]; then
        %{__mv} /etc/spamassassin.cf /etc/mail/spamassassin/migrated.cf
fi
if [ -f /etc/mail/spamassassin.cf ]; then
        %{__mv} /etc/mail/spamassassin.cf /etc/mail/spamassassin/migrated.cf
fi

%postun
%if %{use_systemd} == 0
if [ "$1" -ge "1" ]; then
    /sbin/service spamassassin condrestart > /dev/null 2>&1
fi
exit 0
%endif

%if %{use_systemd}
%systemd_postun spamassassin.service
%systemd_postun sa-update.timer
%endif

%preun
%if %{razor_deps}
rm -f %{_sharedstatedir}/razor/*
%endif
%if %{use_systemd} == 0
if [ $1 = 0 ] ; then
    /sbin/service spamassassin stop >/dev/null 2>&1
    /sbin/chkconfig --del spamassassin
fi
exit 0
%endif

%if %{use_systemd}
%systemd_preun spamassassin.service
%systemd_preun sa-update.timer
%endif

%if %{use_systemd}
%triggerun -- spamassassin < 3.3.2-2
%{_bindir}/systemd-sysv-convert --save spamassassin >/dev/null 2>&1 ||:

# Run these because the SysV package being removed won't do them
/sbin/chkconfig --del spamassassin >/dev/null 2>&1 || :
/bin/systemctl try-restart spamassassin.service >/dev/null 2>&1 || :
%endif

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.4.4-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Feb 03 2020 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.4-1
- Update to 3.4.4
- Resolves: rhbz#1796196

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 04 2020 Kevin Fenzi <kevin@scrye.com> - 3.4.3-2
- Fix mistaken version in rules. Fixes bug #1787739

* Thu Dec 12 2019 Kevin Fenzi <kevin@scrye.com> - 3.4.3-1
- Update to 3.4.3. Fixes bug #1782611

* Tue Oct 01 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.2-8
- Fix issues found by Coverity Scan

* Tue Oct 01 2019 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.2-7
- Fix rawbody rules documentation

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 31 2019 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.2-5
- Perl 5.30 rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Oct 15 2018 Ondřej Lysoněk <olysonek@redhat.com> - 3.4.2-3
- Add missing dependencies of sa-compile

* Thu Sep 20 2018 Kevin Fenzi <kevin@scrye.com> - 3.4.2-2
- Misc small bug fixes and cleanups.

* Sun Sep 16 2018 Kevin Fenzi <kevin@scrye.com> - 3.4.2-1
- Update to 3.4.2
- Fixes: CVE-2017-15705, CVE-2016-1238, CVE-2018-11780 & CVE-2018-11781

* Mon Jul 23 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 3.4.1-25
- perl-Razor-Agent and perl-Net-Patricia not used on RHEL

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Tomas Korbar <tkorbar@redhat.com> - 3.4.1-23
- Fix daemonize subroutine
- See https://bz.apache.org/SpamAssassin/show_bug.cgi?id=7594

* Fri Jun 29 2018 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-22
- Perl 5.28 rebuild

* Wed Jun 20 2018 Kevin Fenzi <kevin@scrye.com> - 3.4.1-21
- Conditionalize Requires for /sbin/service and /sbin/chkconfig. Fixes bug #1592390

* Thu Jun 07 2018 Tomas Korbar <tomas.korb@seznam.cz> - 3.4.1-20
- Add razor log path and home directory option

* Tue Apr 10 2018 Rafael Santos <rdossant@redhat.com> - 3.4.1-19
- Use standard Fedora linker flags (bug #1548561)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Oct 23 2017 Kevin Fenzi <kevin@scrye.com> - 3.4.1-17
- Add upstream patch to stop sa-learn warnings. Fixes bug #1505317
- Add upstream patch to stop DNS warnings. Fixes bug #1364932

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 06 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-14
- Perl 5.26 rebuild

* Thu May 18 2017 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-13
- Fix building on Perl without '.' in @INC

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Oct 31 2016 Kevin Fenzi <kevin@scrye.com> - 3.4.1-11
- Add patch for openssl 1.1.x support. https://bz.apache.org/SpamAssassin/show_bug.cgi?id=7361

* Sat Sep 03 2016 Kevin Fenzi <kevin@scrye.com> - 3.4.1-10
- Drop perl-Mail-spamassassin obsolete that was added in 2004

* Sat Jun 11 2016 Kevin Fenzi <kevin@scrye.com> - 3.4.1-9
- Add perl-Razor-Agent and perl-Net-Patricia To Requires, they might help processing. Fixes bug #1337924
- Add patch for netdns 1.0.1+ dns lookups.

* Sun May 15 2016 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-8
- Perl 5.24 rebuild

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 3.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-5
- Perl 5.22 rebuild

* Sun Jun 07 2015 Kevin Fenzi <kevin@scrye.com> 3.4.1-4
- Fix sa-update to handle systemctl or service as the case may be.

* Sat Jun 06 2015 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.1-3
- Perl 5.22 rebuild

* Sun May 03 2015 Kevin Fenzi <kevin@scrye.com> 3.4.1-2
- Fix base rules version issue. Bug #1217990
- Drop run dir we don't use it.

* Wed Apr 29 2015 Kevin Fenzi <kevin@scrye.com> 3.4.1-1
- Update to 3.4.1

* Fri Apr 03 2015 Kevin Fenzi <kevin@scrye.com> 3.4.0-14
- Switch to systemd timer unit from cron for rules updates. Fixes bug #1064537

* Fri Apr 03 2015 Kevin Fenzi <kevin@scrye.com> 3.4.0-13
- Remove last parts of portreserve. Fixes bug #1175798
- Fix typo in Razor2 plugin. Fixes bug #1208776
- Disabled the AHBL blacklist thats no longer in service in base rules. Fixes bug #1180338

* Thu Sep 25 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-12
- Apply fix for amavisd and spampd reloading after rules updates. Fixes bug #1145654

* Thu Aug 28 2014 Jitka Plesnikova <jplesnik@redhat.com> - 3.4.0-11
- Perl 5.20 rebuild

* Tue Aug 26 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-10
- CLean up portreserve conditionals. Fixes bug #1128708

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 3.4.0-9
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-8.el6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-7
- Add patch to work with newer perl-Net-DNS. Fixes bug #1111586

* Wed Jun 18 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-6
- Adjust systemd unit to not log to syslog since spamd does it already. 
- Fixes bug #1107541

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-4
- Fix versioning on initial rules. 
- Add note to README.RHEL.Fedora to note -d option in sysconfig

* Wed Mar 19 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-3
- Cleaned up spec, added conditionals to build on el again.

* Sun Feb 16 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-2
- Simplify systemd unit file. Thanks misc. Fixes bug #1065762

* Tue Feb 11 2014 Kevin Fenzi <kevin@scrye.com> 3.4.0-1
- Update to 3.4.0

* Sun Feb 02 2014 Kevin Fenzi <kevin@scrye.com> 3.3.2-19
- Use pgrep -f for full command line. Fixes bug #1057926
- Patch to use gnupg2 instead of gnupg1. Fixes bug #1055593
- Use pgrep for spampd as well. Fixes bug #1058976

* Sat Jan 04 2014 Kevin Fenzi <kevin@scrye.com> 3.3.2-18
- Add patch to fix warning to syslog with recent perl.·
- Fixes bug #1023670

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Petr Pisar <ppisar@redhat.com> - 3.3.2-16
- Perl 5.18 rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 15 2012 Kevin Fenzi <kevin@scrye.com> 3.3.2-14
- Fix incorrect pgrep path. Fixes bug #875844

* Sat Aug 25 2012 Kevin Fenzi <kevin@scrye.com> 3.3.2-13
- Add systemd macros for presets. Fixes bug #850320

* Fri Aug 03 2012 Kevin Fenzi <kevin@scrye.com> - 3.3.2-12
- Fix sa-update not detecting spamd running. Fixes bug #755644
- Add restart=always to systemd file to work around upstream bug. Bug #812359

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Petr Pisar <ppisar@redhat.com> - 3.3.2-10
- Perl 5.16 rebuild

* Thu Jan 19 2012 Kevin Fenzi <kevin@scrye.com> - 3.3.2-9
- Fix unit file to write pid correctly. Fixes bug #783108

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Sep 12 2011 Nick Bebout <nb@fedoraproject.org> - 3.3.2-7
- Use sysvinit on F15, not systemd

* Thu Sep 08 2011 Nick Bebout <nb@fedoraproject.org> - 3.3.2-6
- Don't install sysvinit script if using systemd

* Wed Sep 07 2011 Jesse Keating <jkeating@redhat.com> - 3.3.2-5
- Add details for RHEL 7

* Sat Aug 13 2011 Nick Bebout <nb@fedoraproject.org> - 3.3.2-4
- Build with systemd unit file for f16 and f17

* Thu Jul 21 2011 Petr Sabata <contyk@redhat.com> - 3.3.2-3
- Perl mass rebuild

* Tue Jul 19 2011 Petr Sabata <contyk@redhat.com> - 3.3.2-2
- Perl mass rebuild

* Mon Jun 6 2011 Warren Togami <warren@togami.com> - 3.3.2-1
- 3.3.2

* Mon May 30 2011 Warren Togami <warren@togami.com> - 3.3.2-0.8.rc2
- 3.3.2-rc2

* Mon May 16 2011 Warren Togami <warren@togami.com> - 3.3.2-0.7.rc1
- 3.3.2-rc1

* Sun Feb 27 2011 Ville Skyttä <ville.skytta@iki.fi> - 3.3.2-0.6.svn1071394
- Own /etc/mail dir (#645035).

* Wed Feb 16 2011 Nick Bebout <nb@fedoraproject.org> - 3.3.2-0.5.svn1071394
- Oops, I left off svn in the Release of 3.3.2-0.4.svn1071394

* Wed Feb 16 2011 Nick Bebout <nb@fedoraproject.org> - 3.3.2-0.4.svn1071394
- replace @@VERSION@@ with current saversion
- restart spampd after sa-update cronjob runs
- update to svn1071394

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.3.2-0.3.svn1027144
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 29 2010 Kevin Fenzi <kevin@tummy.com> - 3.3.2-0.2.svn1027144
- Fix sa-update sysconfig script line wrapping

* Mon Oct 25 2010 Nick Bebout <nb@fedoraproject.org> - 3.3.2-0.1.svn1027144
- Update to 3.3.2 - svn1027144 to solve bug

* Sat Jul 03 2010 Dennis Gilmore <dennis@ausil.us> - 3.3.1-5
- rebuild against perl-5.12.0 again

* Wed Jun 02 2010 Nick Bebout <nb@fedoraproject.org> - 3.3.1-4
- Add perl-Mail-SPF dependency

* Wed Jun 02 2010 Marcela Maslanova <mmaslano@redhat.com> - 3.3.1-3
- Mass rebuild with perl-5.12.0

* Tue Mar 16 2010 Warren Togami <wtogami@redhat.com> - 3.3.1-2
- 3.3.1 take 2

* Mon Mar 15 2010 Warren Togami <wtogami@redhat.com> - 3.3.1-1
- 3.3.1 bug fix only release

* Wed Feb 17 2010 Warren Togami <wtogami@redhat.com> - 3.3.0-6
- Minor fix to update script

* Thu Jan 21 2010 Warren Togami <wtogami@redhat.com> - 3.3.0-2
- 3.3.0
- README.RHEL.Fedora contains notes specific to our package

* Thu Jan 14 2010 Warren Togami <wtogami@redhat.com> - 3.3.0-0.32.rc3
- 3.3.0-rc3
- if mimedefang is enabled, reload rules after sa-update

* Mon Jan 11 2010 Warren Togami <wtogami@redhat.com> - 3.3.0-0.31.rc2
- 3.3.0-rc2

* Mon Dec 28 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.29.rc1
- sa-update channels defined in /etc/mail/spamassassin/channel.d/*.conf files

* Mon Dec 28 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.27.rc1
- sa-update runs in cron automatically if spamd or amavisd is running
  If you use neither, you may force sa-update by editing /etc/sysconfig/sa-update

* Mon Dec 21 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.26.rc1
- 3.3.0-rc1.proposed2 with fixed spamc

* Fri Dec 18 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.23.rc1
- 3.3.0-rc1
- Bug #103401: portreserve protect spamd port 783 on F-10+

* Thu Dec 03 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.21.beta1
- 3.3.0-beta1

* Fri Nov 20 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.20.svn882672
- svn882672 snapshot

* Thu Nov 12 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.19.svn816416
- Encode::Detect is important to spamassassin, require for anything newer than RHEL-5

* Thu Sep 24 2009 Warren Togami <wtogami@redhat.com> - 3.3.3-0.18.svn816416
- Enable SOUGHT ruleset in nightly sa-update http://wiki.apache.org/spamassassin/SoughtRules
  You must enable the sa-update cron job manually in /etc/cron.d/sa-update
- Custom channels may be specified in these config files:
      /etc/mail/spamassassin/sa-update-channels.txt
      /etc/mail/spamassassin/sa-update-keys.txt

* Thu Sep 17 2009 Warren Togami <wtogami@redhat.com> - 3.3.3-0.14.svn816416
- 3.3.0 svn816416 snapshot, pre-alpha3
  Upstream just fixed important bug SA#6206.  Many other bugs fixed since alpha2.

* Thu Sep 17 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.13.alpha2
- F11+ requires Mail::DKIM

* Sun Sep 13 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.12.alpha2
- require perl(Mail::DKIM), useful due to USER_IN_DEF_DKIM_WL

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.3.0-0.6.alpha2
- rebuilt with new openssl

* Mon Aug 10 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.5.alpha1
- 3.3.0-alpha2

* Tue Jul 07 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.2.alpha1
- Include default rules to prevent mass confusion and complaints.
  You should really use sa-update though.  Really.
  Edit /etc/cron.d/sa-update to automate it.

* Mon Jul 06 2009 Warren Togami <wtogami@redhat.com> - 3.3.0-0.1.alpha1
- 3.3.0-alpha1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 3.2.5-4
- rebuild with new openssl

* Mon Dec 15 2008 Kevin Fenzi <kevin@tummy.com> - 3.2.5-3
- Update for merge review - bug 226426

* Thu Sep  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.2.5-2
- fix license tag

* Fri Jun 27 2008 Warren Togami <wtogami@redhat.com> - 3.2.5-1
- 3.2.5

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 3.2.4-4
- Rebuild for perl 5.10 (again)

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 3.2.4-3
- Autorebuild for GCC 4.3

* Thu Jan 31 2008 Tom "spot" Callaway <tcallawa@redhat.com> 3.2.4-2
- rebuild for new perl

* Tue Jan 01 2008 Warren Togami <wtogami@redhat.com> 3.2.4-1
- 3.2.4 major bugfix release

* Tue Aug 21 2007 Warren Togami <wtogami@redhat.com> 3.2.3-2
- rebuild

* Mon Aug 13 2007 Warren Togami <wtogami@redhat.com> 3.2.3-1
- 3.2.3 major bugfix release

* Thu Aug 2 2007 Warren Togami <wtogami@redhat.com> 3.2.2-2
- Fix SA#5574 which cripples dcc/pyzor users

* Wed Jul 25 2007 Warren Togami <wtogami@redhat.com> 3.2.2-1
- 3.2.2 minor bugfix release

* Mon Jun 11 2007 Warren Togami <wtogami@redhat.com> 3.2.1-1
- 3.2.1 CVE-2007-2873

* Wed May 02 2007 Warren Togami <wtogami@redhat.com> 3.2.0-1
- 3.2.0

* Fri Apr 13 2007 Warren Togami <wtogami@redhat.com> 3.2.0-0.5.rc3
- 3.2.0 rc3

* Fri Apr 13 2007 Warren Togami <wtogami@redhat.com> 3.2.0-0.4.rc2
- 3.2.0 rc2

* Mon Apr 02 2007 Warren Togami <wtogami@redhat.com> 3.2.0-0.3.rc1
- 3.2.0 rc1

* Tue Mar 06 2007 Warren Togami <wtogami@redhat.com> 3.2.0-0.2.pre2
- Conditional to require perl-devel during build for FC7+ (#226276)

* Fri Mar 02 2007 Warren Togami <wtogami@redhat.com> 3.2.0-0.1.pre2
- 3.2.0-pre2

* Mon Feb 19 2007 Warren Togami <wtogami@redhat.com> 3.1.8-2
- Fix sa-learn regression (#228968)

* Tue Feb 13 2007 Warren Togami <wtogami@redhat.com> 3.1.8-1
- 3.1.8 CVE-2007-0451

* Tue Feb 13 2007 Warren Togami <wtogami@redhat.com> 3.1.7-9
- silence sa-update cron script

* Wed Feb 07 2007 Warren Togami <wtogami@redhat.com> 3.1.7-8
- only restart spamd if necessary after sa-update (#227756)

* Wed Feb 07 2007 Warren Togami <wtogami@redhat.com> 3.1.7-7
- requires gnupg (#227738)

* Sun Jan 28 2007 Warren Togami <wtogami@redhat.com> 3.1.7-6
- explicit requires on perl(HTTP::Date) and perl(LWP::UserAgent) 
  (Bug #193100)

* Mon Jan 22 2007 Warren Togami <wtogami@redhat.com> 3.1.7-5
- fix typo in logrotate.d (#223817)

* Thu Jan 18 2007 Warren Togami <wtogami@redhat.com> 
- Options for RHEL4
    * spamc/spamd cannot connect over IPv6 or SSL
    * sa-update is disabled
  The above functionality requires perl modules not included in RHEL4.
  You may still use them if you get those perl modules from elsewhere.
  RHEL5 ships these perl modules.

* Thu Dec 14 2006 Warren Togami <wtogami@redhat.com> - 3.1.7-4
- add standardized sa-update cron script, disabled by default

* Thu Dec 14 2006 Warren Togami <wtogami@redhat.com> - 3.1.7-2
- own directory /var/lib/spamassassin

* Mon Nov 20 2006 Warren Togami <wtogami@redhat.com> - 3.1.7-1
- 3.1.7 maintenance release

* Wed Aug 02 2006 Warren Togami <wtogami@redhat.com> - 3.1.4-1
- 3.1.4 maintenance release

* Mon Jul 17 2006 Warren Togami <wtogami@redhat.com> - 3.1.3-5
- req perl-IO-Socket-SSL for spamc/spamd SSL communication
- req perl-IO-Socket-INET6 for IPv6

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 3.1.3-3.1
- rebuild

* Tue Jun 27 2006 Florian La Roche <laroche@redhat.com> - 3.1.3-3
- require diffutils for the post script (cmp is used)

* Wed Jun 07 2006 Warren Togami <wtogami@redhat.com> - 3.1.3-2
- start spamd before sendmail (#193818)
- require perl-Archive-Tar (#193100)

* Mon Jun 05 2006 Warren Togami <wtogami@redhat.com> - 3.1.3-1
- CVE-2006-2447

* Fri May 26 2006 Warren Togami <wtogami@redhat.com> - 3.1.2-1
- 3.1.2 bug fix release

* Tue May 09 2006 Warren Togami <wtogami@redhat.com> - 3.0.5-4
- Preserve timestamp and context of /etc/sysconfig/spamassassin (#178580)

* Sat Mar 11 2006 Warren Togami <wtogami@redhat.com> - 3.1.1-1
- 3.1.1

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 3.1.0-5
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 3.1.0-5
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Jan 18 2006 Warren Togami <wtogami@redhat.com> - 3.1.0-5
- include SPAM_PID dir (#177788)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Dec 01 2005 Warren Togami <wtogami@redhat.com> - 3.1.0-3
- #174579 nls spamd init script (Rudolf Kastl)

* Tue Nov 08 2005 Warren Togami <wtogami@redhat.com> - 3.1.0-2
- #161785 ensure that service restart works

* Tue Sep 13 2005 Warren Togami <wtogami@redhat.com> - 3.1.0-1
- 3.1.0

* Sun Aug 28 2005 Warren Togami <wtogami@redhat.com> - 3.1.0-0.rc2
- 3.1.0-rc2

* Tue Aug 16 2005 Warren Togami <wtogami@redhat.com> - 3.1.0-0.rc1
- 3.1.0-rc1

* Fri Jul 15 2005 Warren Togami <wtogami@redhat.com> - 3.1.0-0.pre4
- 3.1.0-pre4

* Sun Jun 05 2005 Warren Togami <wtogami@redhat.com> - 3.0.4-1
- 3.0.4

* Tue May 17 2005 Warren Togami <wtogami@redhat.com> - 3.0.3-4
- allow user-level disabling of subject rewriting pref (#147464)

* Wed Apr 27 2005 Warren Togami <wtogami@redhat.com> - 3.0.3-3
- 3.0.3
- SA#4287 retval fix
- allow replacement of rc service script during upgrades

* Mon Apr 25 2005 Warren Togami <wtogami@redhat.com> - 3.0.3-0.r164513
- 3.0.3-r164513 (almost final)

* Thu Apr 21 2005 Warren Togami <wtogami@redhat.com> - 3.0.2-9
- SA#4191 uri_to_domain() is broken for urls with empty port
  SA#4232 multipart message with 0 parts -> uninitialized in m//
  SA#4121 Score for user defined rules become ignored
  SA#3944 get_envelope_from not handling received header

* Sun Apr 10 2005 Ville Skyttä <ville.skytta@iki.fi> - 3.0.2-8
- Own /usr/share/spamassassin (#152534).
- Drop no longer needed dependency filter script.

* Sat Apr 02 2005 Warren Togami <wtogami@redhat.com> 3.0.2-7
- req DB_File (#143186)

* Sat Apr 02 2005 Warren Togami <wtogami@redhat.com> 3.0.2-6
- test svn 3.0 stable r122144 snapshot
  SA#3826 #4044 #4050 #4048 #4075 #4064 #4075 #4034 #3952

* Thu Mar 24 2005 Florian La Roche <laroche@redhat.com>
- add "exit 0" to postun script

* Thu Mar 24 2005 Joe Orton <jorton@redhat.com> 3.0.2-4
- package the NOTICE file

* Thu Mar 17 2005 Warren Togami <wtogami@redhat.com> - 3.0.2-3
- reinclude ia64, thanks jvdias

* Tue Mar 15 2005 Warren Togami <wtogami@redhat.com> - 3.0.2-2
- exclude ia64 for now due to Bug #151127

* Mon Dec 20 2004 Warren Togami <wtogami@redhat.com> - 3.0.2-1
- 3.0.2

* Sun Oct 31 2004 Warren Togami <wtogami@redhat.com> - 3.0.1-1
- 3.0.1

* Mon Oct 18 2004 Warren Togami <wtogami@redhat.com> - 3.0.0-3
- Fix local.cf rewrite subject option (#133355 Christof Damian)

* Sat Sep 25 2004 Warren Togami <wtogami@redhat.com> - 3.0.0-2
- Update URL, cleanup name (Robert Scheck #133622)

* Thu Sep 23 2004 Warren Togami <wtogami@redhat.com> - 3.0.0-1
- match upstream version
- #133422 Future proof krb5 back compat (Milan Kerslager)

* Wed Sep 22 2004 Warren Togami <wtogami@redhat.com> - 3.0-10 
- 3.0.0 final

* Sun Sep 12 2004 Warren Togami <wtogami@redhat.com> - 3.0-9.rc4
- 3.0 rc4
- update krb5 backcompat patch (John Lundin)

* Sat Sep 04 2004 Warren Togami <wtogami@redhat.com> - 3.0-8.rc3
- 3.0 rc3

* Sun Aug 29 2004 Warren Togami <wtogami@redhat.com> - 3.0-7.rc2
- 3.0 rc2

* Sat Aug 21 2004 Warren Togami <wtogami@redhat.com> - 3.0-6.rc1
- fix perl module syntax in req and buildreqs

* Thu Aug 19 2004 Warren Togami <wtogami@redhat.com> - 3.0-5.rc1
- 3.0 rc1

* Sat Aug 07 2004 Warren Togami <wtogami@redhat.com> - 3.0-3.pre4
- 3.0 pre4

* Wed Jul 28 2004 Warren Togami <wtogami@redhat.com> - 3.0-3.pre2
- 3.0 pre2

* Sun Jun 20 2004 Warren Togami <wtogami@redhat.com> - 3.0-2.pre1
- 3.0.0 pre1
- remove unnecessary patches applied upstream
- update krb5 backcompat patch

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon May 31 2004 Warren Togami <wtogami@redhat.com> - 3.0-svn20040530
- svn snapshot 20040530
- #124870 prevent service startup failure due to old -a option
- #124871 more docs
- #124872 unowned directories

* Mon May 24 2004 Warren Togami <wtogami@redhat.com> - 3.0-svn20040524
- #123432 do not start service by default
- #122488 remove CRLF's
- #123706 correct license
- svn snapshot 20040524
- svn snapshot 20040518

* Sun May  2 2004 Ville Skyttä <ville.skytta@iki.fi> - 2.63-8
- #122233
- Require perl(:MODULE_COMPAT_*).
- Use %%{_mandir} and %%{_initrddir}.
- Fix License tag and include License in docs.
- Backslashify multiline init script description.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb  11 2004 Warren Togami <wtogami@redhat.com> 2.63-6
- require sitelib instead

* Wed Jan  21 2004 Warren Togami <wtogami@redhat.com> 2.63-3
- krb5-backcompat.patch so older krb5-devel does not fail

* Wed Jan  21 2004 Warren Togami <wtogami@redhat.com> 2.63-2
- upgrade to 2.63

* Mon Jan  19 2004 Warren Togami <wtogami@redhat.com> 2.62-3
- Ville Skyttä's fixes from #113596 including:
- Fix buildroot traces
- enable openssl
- Trailing slash to DESTDIR (bug 90202 comment 14).
- export optflags so they're honored, affects spamc only. 

* Mon Jan  19 2004 Warren Togami <wtogami@redhat.com> 2.62-2
- upgrade to 2.62
- Prereq -> Requires, former is deprecated
- Require current version of perl
- Remove urban myth clean test
- TODO: Get rid of prefix

* Wed Dec  31 2003 Dan Walsh <dwalsh@redhat.com> 2.61-2
- Change sysconfdir to not use full path

* Tue Dec  9 2003 Chip Turner <cturner@redhat.com> 2.61-1
- upgrade to 2.61

* Fri Sep 26 2003 Chip Turner <cturner@redhat.com> 2.60-2
- update to 2.60

* Sat Jul  5 2003 Chip Turner <cturner@redhat.com> 2.55-3
- change perl dependency to more accurate versions with explicit epochs

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 31 2003 Chip Turner <cturner@redhat.com> 2.55-1
- move to upstream version 2.55

* Tue May 13 2003 Chip Turner <cturner@redhat.com>
- bump for build
- change init.d script to not default to started

* Sun May 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove Distribution: tag in spec file

* Wed Apr 16 2003 Chip Turner <cturner@redhat.com> 2.53-5
- remove SIGCHILD patch to properly return it to SIG_IGN now that
  waitpid isn't used on Linux

* Mon Apr 14 2003 Chip Turner <cturner@redhat.com> 2.53-4.8.x
- update to 2.53 from upstream

* Fri Mar 21 2003 Chip Turner <cturner@redhat.com> 2.50-3.8.x
- update patch for servicename; should fix restarting/runlevel issues (#85975)

* Thu Mar 13 2003 Chip Turner <cturner@redhat.com> 2.50-2.8.x
- update to 2.50

* Tue Feb 25 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 21 2003 Chip Turner <cturner@redhat.com>
- revert double fix for 84774

* Mon Feb 17 2003 Bill Nottingham <notting@redhat.com>
- fix startup (#84445)

* Thu Feb 13 2003 Bill Nottingham <notting@redhat.com>
- fix paths in initscript (#84216)

* Thu Feb 13 2003 Chip Turner <cturner@redhat.com>
- removing -P option since it is the default now, bug 84144

* Wed Feb 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix SIGCHLD handling

* Mon Feb 10 2003 Bill Nottingham <notting@redhat.com>
- move condrestart to %%postun

* Sun Feb  2 2003 Chip Turner <cturner@redhat.com>
- update to 2.44
- add condrestart to service script

* Thu Jan 30 2003 Chip Turner <cturner@redhat.com>
- release bump and rebuild

* Wed Jan 29 2003 Chip Turner <cturner@redhat.com>
- add upstream bsmtp off-by-one patch

* Mon Jan 20 2003 Chip Turner <cturner@redhat.com>
- add wrapper for 'spamassassin -e' for native evolution spam filtering

* Sat Jan  4 2003 Jeff Johnson <jbj@redhat.com> 2.43-10
- use internal dep generator.

* Wed Jan  1 2003 Chip Turner <cturner@redhat.com>
- rebuild

* Tue Dec 17 2002 Bill Nottingham <notting@redhat.com> 2.43-7
- don't run by default

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 2.43-6
- don't use rpms internal dep generator
- buildrequire perl-Time-HiRes instead of perl(Time:HiRes) so we can satisfy build deps in the build system

* Fri Nov 22 2002 Tim Powers <timp@redhat.com>
- rebuilt to solve broken perl deps

* Thu Aug 15 2002 Chip Turner <cturner@redhat.com>
- speedup patch from upstream

* Tue Aug  6 2002 Chip Turner <cturner@redhat.com>
- automated release bump and build

* Thu Jul 18 2002 Chip Turner <cturner@redhat.com>
- better control of service level, improvement in %%post script.
- (contribs from schirmer@taytron.net)

* Fri Jun 28 2002 Chip Turner <cturner@redhat.com>
- added proper BuildRequire

* Wed Jun 26 2002 Chip Turner <cturner@redhat.com>
- updated to 2.31, added .rc file for procmail to INCLUDERC to enable

* Fri Apr 19 2002 Theo Van Dinter <felicity@kluge.net>
- Updated for 2.20 release
- made /etc/mail/spamassassin a config directory so local.cf doesn't get wiped out
- added a patch to remove findbin stuff

* Wed Feb 27 2002 Craig Hughes <craig@hughes-family.org>
- Updated for 2.1 release

* Sat Feb 02 2002 Theo Van Dinter <felicity@kluge.net>
- Updates for 2.01 release
- Fixed rc file
- RPM now buildable as non-root
- fixed post_service errors
- fixed provides to include perl modules
- use file find instead of manually specifying files

* Tue Jan 15 2002 Craig Hughes <craig@hughes-family.org>
- Updated for 2.0 release

* Wed Dec 05 2001 Craig Hughes <craig@hughes-family.org>
- Updated for final 1.5 distribution.

* Sun Nov 18 2001 Craig Hughes <craig@hughes-family.org>
- first version of rpm.

