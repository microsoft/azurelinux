# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# By default build clamav subpackage on Fedora,
# do not build on RHEL
%if 0%{?rhel}
%bcond_with clamav
%else
%bcond_without clamav
%endif

# hardened build if not overridden
%{!?_hardened_build:%global _hardened_build 1}

Summary: The exim mail transfer agent
Name: exim
Version: 4.99.1
Release: 2%{?dist}
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License: GPL-2.0-or-later
Url: https://www.exim.org/

Provides: MTA smtpd smtpdaemon server(smtp)
Requires(post): %{_sbindir}/restorecon %{_sbindir}/alternatives systemd
Requires(preun): %{_sbindir}/alternatives systemd
Requires(postun): %{_sbindir}/alternatives systemd
%if %{with clamav}
BuildRequires: clamd
%endif
Source: https://ftp.exim.org/pub/exim/exim4/exim-%{version}.tar.xz
Source1: https://ftp.exim.org/pub/exim/exim4/%{name}-%{version}.tar.xz.asc
Source2: https://downloads.exim.org/Exim-Maintainers-Keyring.asc

Source3: exim.sysconfig
Source4: exim.logrotate
Source5: exim-tidydb.sh
Source11: exim.pam
Source12: exim-clamav-tmpfiles.conf

Source20: exim-greylist.conf.inc
Source21: mk-greylist-db.sql
Source22: greylist-tidy.sh
Source23: trusted-configs
Source24: exim.service
Source25: exim-gen-cert
Source26: clamd.exim.service

Patch: exim-4.99-config.patch
Patch: exim-4.94-libdir.patch
Patch: exim-4.97-dlopen-localscan.patch
Patch: exim-4.99-pic.patch

Requires: /etc/pki/tls/certs /etc/pki/tls/private
Requires: /etc/aliases
Recommends: publicsuffix-list

%if "%{_sbindir}" == "%{_bindir}"
# Compat symlinks for Requires in other packages.
# We rely on filesystem to create the symlinks for us.
Requires:       filesystem(unmerged-sbin-symlinks)
Provides:       /usr/sbin/sendmail
%endif

BuildRequires: gcc
BuildRequires: libdb-devel
BuildRequires: openssl-devel
BuildRequires: openldap-devel
BuildRequires: pam-devel
BuildRequires: pcre2-devel
BuildRequires: sqlite-devel
BuildRequires: cyrus-sasl-devel
BuildRequires: libspf2-devel
BuildRequires: libopendmarc-devel
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: mariadb-connector-c-devel
BuildRequires: libpq-devel
BuildRequires: libxcrypt-devel
BuildRequires: libXaw-devel
BuildRequires: libXmu-devel
BuildRequires: libXext-devel
BuildRequires: libX11-devel
BuildRequires: libSM-devel
BuildRequires: libICE-devel
BuildRequires: libXpm-devel
BuildRequires: libXt-devel
BuildRequires: systemd-units
BuildRequires: libgsasl-devel
# Workaround for NIS removal from glibc, bug 1534920
BuildRequires: libnsl2-devel
BuildRequires: libtirpc-devel
BuildRequires: gnupg2
BuildRequires: grep
BuildRequires: perl-devel
BuildRequires: perl-generators
BuildRequires: perl-ExtUtils-Embed
BuildRequires: perl-experimental
BuildRequires: perl-File-FcntlLock
%if 0%{?rhel} == 8
BuildRequires:  epel-rpm-macros >= 8-5
%endif
BuildRequires: make

# i686 repo is broken, stop building it
ExcludeArch: %{ix86}

%description
Exim is a message transfer agent (MTA) developed at the University of
Cambridge for use on Unix systems connected to the Internet. It is
freely available under the terms of the GNU General Public Licence. In
style it is similar to Smail 3, but its facilities are more
general. There is a great deal of flexibility in the way mail can be
routed, and there are extensive facilities for checking incoming
mail. Exim can be installed in place of sendmail, although the
configuration of exim is quite different to that of sendmail.

%package mysql
Summary: MySQL lookup support for Exim
Requires: exim = %{version}-%{release}

%description mysql
This package contains the MySQL lookup module for Exim

%package pgsql
Summary: PostgreSQL lookup support for Exim
Requires: exim = %{version}-%{release}

%description pgsql
This package contains the PostgreSQL lookup module for Exim

%package mon
Summary: X11 monitor application for Exim

%description mon
The Exim Monitor is an optional supplement to the Exim package. It
displays information about Exim's processing in an X window, and an
administrator can perform a number of control actions from the window
interface.

%if %{with clamav}
%package clamav
Summary: Clam Antivirus scanner dæmon configuration for use with Exim
Requires: clamd exim
Obsoletes: clamav-exim <= 0.86.2

%description clamav
This package contains configuration files which invoke a copy of the
clamav dæmon for use with Exim. It can be activated by adding (or
uncommenting)

   av_scanner = clamd:%{_var}/run/clamd.exim/clamd.sock

in your exim.conf, and using the 'malware' condition in the DATA ACL,
as follows:

   deny message = This message contains malware ($malware_name)
      malware = *

For further details of Exim content scanning, see chapter 41 of the Exim
specification:
http://www.exim.org/exim-html-%{version}/doc/html/spec_html/ch41.html

%endif

%package greylist
Summary: Example configuration for greylisting using Exim
Requires: sqlite exim
Requires: crontabs

%description greylist
This package contains a simple example of how to do greylisting in Exim's
ACL configuration. It contains a cron job to remove old entries from the
greylisting database, and an ACL subroutine which needs to be included
from the main exim.conf file.

To enable greylisting, install this package and then uncomment the lines
in Exim's configuration /etc/exim.conf which enable it. You need to
uncomment at least two lines -- the '.include' directive which includes
the new ACL subroutine, and the line which invokes the new subroutine.

By default, this implementation only greylists mails which appears
'suspicious' in some way. During normal processing of the ACLs we collect
a list of 'offended' which it's committed, which may include having
SpamAssassin points, lacking a Message-ID: header, coming from a blacklisted
host, etc. There are examples of these in the default configuration file,
mostly commented out. These should be sufficient for you to you trigger
greylisting for whatever 'offences' you can dream of, or even to make
greylisting unconditional.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1

cp src/EDITME Local/Makefile
sed -i 's@^# LOOKUP_MODULE_DIR=.*@LOOKUP_MODULE_DIR=%{_libdir}/exim/%{version}-%{release}/lookups@' Local/Makefile
sed -i 's@^# AUTH_LIBS=-lsasl2@AUTH_LIBS=-lsasl2@' Local/Makefile
sed -i 's@^# SUPPORT_SRS=yes@SUPPORT_SRS=yes@' Local/Makefile
cp exim_monitor/EDITME Local/eximon.conf

# Workaround for rhbz#1791878
pushd doc
for f in $(ls -dp cve-* | grep -v '/\|\(\.txt\)$'); do
  mv "$f" "$f.txt"
done
popd

# Create a sysusers.d config file
cat >exim.sysusers.conf <<EOF
u exim 93 - %{_var}/spool/exim -
m exim mail
EOF

%build
# https://bugs.exim.org/show_bug.cgi?id=3135
export CFLAGS="%{build_cflags} -std=gnu17"
%ifnarch s390 s390x sparc sparcv9 sparcv9v sparc64 sparc64v
	export PIE=-fpie
	export PIC=-fpic
%else
	export PIE=-fPIE
	export PIC=-fPIC
%endif

export LDFLAGS="%{?__global_ldflags} %{?_hardened_build:-pie -Wl,-z,relro,-z,now}"
make _lib=%{_lib} FULLECHO=

%install
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/pam.d
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/exim

cd build-`scripts/os-type`-`scripts/arch-type`
install -m 4775 exim $RPM_BUILD_ROOT%{_sbindir}

for i in eximon eximon.bin exim_dumpdb exim_fixdb exim_tidydb \
	exinext exiwhat exim_dbmbuild exicyclog exim_lock \
	exigrep eximstats exipick exiqgrep exiqsumm \
	exim_checkaccess
do
	install -m 0755 $i $RPM_BUILD_ROOT%{_sbindir}
done

mkdir -p $RPM_BUILD_ROOT%{_libdir}/exim/%{version}-%{release}/lookups
for i in mysql pgsql
do 
	install -m755 lookups/${i}.so \
	 $RPM_BUILD_ROOT%{_libdir}/exim/%{version}-%{release}/lookups/${i}_lookup.so
done

cd ..

install -m 0644 src/configure.default $RPM_BUILD_ROOT%{_sysconfdir}/exim/exim.conf
install -m 0644 %SOURCE11 $RPM_BUILD_ROOT%{_sysconfdir}/pam.d/exim

mkdir -p $RPM_BUILD_ROOT/usr/lib
ln -sf --relative $RPM_BUILD_ROOT%{_sbindir}/exim $RPM_BUILD_ROOT/usr/lib/sendmail.exim

ln -sf exim $RPM_BUILD_ROOT%{_sbindir}/sendmail.exim

ln -sf --relative $RPM_BUILD_ROOT%{_sbindir}/exim $RPM_BUILD_ROOT%{_bindir}/mailq.exim
ln -sf --relative $RPM_BUILD_ROOT%{_sbindir}/exim $RPM_BUILD_ROOT%{_bindir}/runq.exim
ln -sf --relative $RPM_BUILD_ROOT%{_sbindir}/exim $RPM_BUILD_ROOT%{_bindir}/rsmtp.exim
ln -sf --relative $RPM_BUILD_ROOT%{_sbindir}/exim $RPM_BUILD_ROOT%{_bindir}/rmail.exim
ln -sf --relative $RPM_BUILD_ROOT%{_sbindir}/exim $RPM_BUILD_ROOT%{_bindir}/newaliases.exim

install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/db
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/input
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/spool/exim/msglog
install -d -m 0750 $RPM_BUILD_ROOT%{_var}/log/exim

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8
install -m644 doc/exim.8 $RPM_BUILD_ROOT%{_mandir}/man8/exim.8
pod2man --center=EXIM --section=8 \
	$RPM_BUILD_ROOT%{_sbindir}/eximstats \
	$RPM_BUILD_ROOT%{_mandir}/man8/eximstats.8

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m 644 %SOURCE3 $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/exim

# Systemd
mkdir -p %{buildroot}%{_unitdir}
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
install -m644 %{SOURCE24} %{buildroot}%{_unitdir}
install -m755 %{SOURCE25} %{buildroot}%{_libexecdir}

%if %{with clamav}
install -m644 %{SOURCE26} %{buildroot}%{_unitdir}
%endif

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d
install -m 0644 %SOURCE4 $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/exim

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily
install -m 0755 %SOURCE5 $RPM_BUILD_ROOT%{_sysconfdir}/cron.daily/exim-tidydb

# generate ghost .pem file
mkdir -p $RPM_BUILD_ROOT/etc/pki/tls/{certs,private}
touch $RPM_BUILD_ROOT/etc/pki/tls/{certs,private}/exim.pem
chmod 600 $RPM_BUILD_ROOT/etc/pki/tls/{certs,private}/exim.pem

# generate alternatives ghosts
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
for i in %{_sbindir}/sendmail %{_bindir}/{mailq,runq,rsmtp,rmail,newaliases} \
	/usr/lib/sendmail %{_sysconfdir}/pam.d/smtp
do
	touch $RPM_BUILD_ROOT$i
done
gzip < /dev/null > $RPM_BUILD_ROOT%{_mandir}/man1/mailq.1.gz

%if %{with clamav}
# Munge the clamav init and config files from clamav-devel. This really ought
# to be a subpackage of clamav, but this hack will have to do for now.
function clamsubst() {
	 sed -e "s!<SERVICE>!$3!g;s!<USER>!$4!g;""$5" %{_docdir}/clamd/"$1" >"$RPM_BUILD_ROOT$2"
}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/clamd.d
clamsubst clamd.conf %{_sysconfdir}/clamd.d/exim.conf exim exim \
       's!^##*\(\(LogFile\|LocalSocket\|PidFile\|User\)\s\|\(StreamSaveToDisk\|ScanMail\|LogTime\|ScanArchive\)$\)!\1!;s!^Example!#Example!;'

clamsubst clamd.logrotate %{_sysconfdir}/logrotate.d/clamd.exim exim exim ''
cat <<EOF > $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/clamd.exim
CLAMD_CONFIG='%_sysconfdir/clamd.d/exim.conf'
CLAMD_SOCKET=%{_var}/run/clamd.exim/clamd.sock
EOF
ln -sf clamd $RPM_BUILD_ROOT%{_sbindir}/clamd.exim

mkdir -p %{buildroot}%{_tmpfilesdir}
install -m 0644 %{SOURCE12} %{buildroot}%{_tmpfilesdir}/exim-clamav.conf
mkdir -p $RPM_BUILD_ROOT%{_var}/run/clamd.exim
mkdir -p $RPM_BUILD_ROOT%{_var}/log
touch $RPM_BUILD_ROOT%{_var}/log/clamd.exim

%endif

# Set up the greylist subpackage
install -m644 %{SOURCE20} $RPM_BUILD_ROOT/%_sysconfdir/exim/exim-greylist.conf.inc
install -m644 %{SOURCE21} $RPM_BUILD_ROOT/%_sysconfdir/exim/mk-greylist-db.sql
mkdir -p $RPM_BUILD_ROOT/%_sysconfdir/cron.daily
install -m755 %{SOURCE22} $RPM_BUILD_ROOT/%_sysconfdir/cron.daily/greylist-tidy.sh
install -m644 %{SOURCE23} $RPM_BUILD_ROOT/%_sysconfdir/exim/trusted-configs
touch $RPM_BUILD_ROOT/%_var/spool/exim/db/greylist.db

install -m0644 -D exim.sysusers.conf %{buildroot}%{_sysusersdir}/exim.conf

%check
build-`scripts/os-type`-`scripts/arch-type`/exim -C src/configure.default -bV

%pre
# Copy TLS certs from old location to new -- don't move them, because the
# config file may be modified and may be pointing to the old location.
if [ ! -f /etc/pki/tls/certs/exim.pem -a -f %{_datadir}/ssl/certs/exim.pem ] ; then
   cp %{_datadir}/ssl/certs/exim.pem /etc/pki/tls/certs/exim.pem
   cp %{_datadir}/ssl/private/exim.pem /etc/pki/tls/private/exim.pem
fi

exit 0

%post
%systemd_post %{name}.service

alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.exim 10 \
	--follower %{_bindir}/mailq mta-mailq %{_bindir}/mailq.exim \
	--follower %{_bindir}/runq mta-runq %{_bindir}/runq.exim \
	--follower %{_bindir}/rsmtp mta-rsmtp %{_bindir}/rsmtp.exim \
	--follower %{_bindir}/rmail mta-rmail %{_bindir}/rmail.exim \
	--follower /etc/pam.d/smtp mta-pam /etc/pam.d/exim \
	--follower %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.exim \
	--follower /usr/lib/sendmail mta-sendmail /usr/lib/sendmail.exim \
	--follower %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man8/exim.8.gz \
	--initscript exim

# Make sure that /usr/sbin/sendmail is not missing, if /usr/sbin is a
# directory. The symlink will only be created if there is no symlink
# or file already.
test -h /usr/sbin || ln -s ../bin/sendmail /usr/sbin/sendmail 2>/dev/null || :

%preun
%systemd_preun %{name}.service
if [ $1 = 0 ]; then
	alternatives --remove mta %{_sbindir}/sendmail.exim
fi

%postun
%systemd_postun_with_restart %{name}.service
if [ $1 -ge 1 ]; then
	mta=`readlink /etc/alternatives/mta`
	if [ "$mta" == "%{_sbindir}/sendmail.exim" ]; then
		alternatives --set mta %{_sbindir}/sendmail.exim
	fi
fi

%post greylist
if [ ! -r %{_var}/spool/exim/db/greylist.db ]; then
   sqlite3 %{_var}/spool/exim/db/greylist.db < %{_sysconfdir}/exim/mk-greylist-db.sql
   chown exim:exim %{_var}/spool/exim/db/greylist.db
   chmod 0660 %{_var}/spool/exim/db/greylist.db
fi

%files
%attr(4755,root,root) %{_sbindir}/exim
%{_sbindir}/exim_dumpdb
%{_sbindir}/exim_fixdb
%{_sbindir}/exim_tidydb
%{_sbindir}/exinext
%{_sbindir}/exiwhat
%{_sbindir}/exim_dbmbuild
%{_sbindir}/exicyclog
%{_sbindir}/exigrep
%{_sbindir}/eximstats
%{_sbindir}/exipick
%{_sbindir}/exiqgrep
%{_sbindir}/exiqsumm
%{_sbindir}/exim_lock
%{_sbindir}/exim_checkaccess
%{_sbindir}/sendmail.exim
%{_bindir}/mailq.exim
%{_bindir}/runq.exim
%{_bindir}/rsmtp.exim
%{_bindir}/rmail.exim
%{_bindir}/newaliases.exim
/usr/lib/sendmail.exim
%{_mandir}/man8/*
%dir %{_libdir}/exim
%dir %{_libdir}/exim/%{version}-%{release}
%dir %{_libdir}/exim/%{version}-%{release}/lookups

%defattr(-,exim,exim)
%dir %{_var}/spool/exim
%dir %{_var}/spool/exim/db
%dir %{_var}/spool/exim/input
%dir %{_var}/spool/exim/msglog
%dir %{_var}/log/exim

%defattr(-,root,root)
%dir %{_sysconfdir}/exim
%config(noreplace) %{_sysconfdir}/exim/exim.conf
%config(noreplace) %{_sysconfdir}/exim/trusted-configs
%config(noreplace) %{_sysconfdir}/sysconfig/exim
%{_unitdir}/exim.service
%{_libexecdir}/exim-gen-cert
%config(noreplace) %{_sysconfdir}/logrotate.d/exim
%config(noreplace) %{_sysconfdir}/pam.d/exim
%{_sysconfdir}/cron.daily/exim-tidydb

%license LICENCE NOTICE
%doc ACKNOWLEDGMENTS README.UPDATING README
%doc doc util/unknownuser.sh

%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) /etc/pki/tls/certs/exim.pem
%attr(0600,root,root) %ghost %config(missingok,noreplace) %verify(not md5 size mtime) /etc/pki/tls/private/exim.pem

%attr(0755,root,root) %ghost %{_sbindir}/sendmail
%attr(0755,root,root) %ghost %{_bindir}/mailq
%attr(0755,root,root) %ghost %{_bindir}/runq
%attr(0755,root,root) %ghost %{_bindir}/rsmtp
%attr(0755,root,root) %ghost %{_bindir}/rmail
%attr(0755,root,root) %ghost %{_bindir}/newaliases
%attr(0755,root,root) %ghost /usr/lib/sendmail
%ghost %{_sysconfdir}/pam.d/smtp
%ghost %{_mandir}/man1/mailq.1.gz
%{_sysusersdir}/exim.conf

%files mysql
%{_libdir}/exim/%{version}-%{release}/lookups/mysql_lookup.so

%files pgsql
%{_libdir}/exim/%{version}-%{release}/lookups/pgsql_lookup.so

%files mon
%{_sbindir}/eximon
%{_sbindir}/eximon.bin

%if %{with clamav}
%post clamav
mkdir -pm 0750 %{_var}/run/clamd.exim
chown exim:exim %{_var}/run/clamd.exim
touch %{_var}/log/clamd.exim
chown exim:exim %{_var}/log/clamd.exim
restorecon %{_var}/log/clamd.exim
if [ $1 -eq 1 ] ; then
    systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun clamav
if [ $1 = 0 ]; then
  systemctl --no-reload clamd.exim.service > /dev/null 2>&1 || :
  systemctl stop clamd.exim.service > /dev/null 2>&1 || :
fi

%postun clamav
systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    systemctl try-restart clamd.exim.service >/dev/null 2>&1 || :
fi

%files clamav
%{_sbindir}/clamd.exim
%{_unitdir}/clamd.exim.service
%config(noreplace) %verify(not mtime) %{_sysconfdir}/clamd.d/exim.conf
%config(noreplace) %verify(not mtime) %{_sysconfdir}/sysconfig/clamd.exim
%config(noreplace) %verify(not mtime) %{_sysconfdir}/logrotate.d/clamd.exim
%{_tmpfilesdir}/exim-clamav.conf
%ghost %attr(0750,exim,exim) %dir %{_var}/run/clamd.exim
%ghost %attr(0644,exim,exim) %{_var}/log/clamd.exim
%endif

%files greylist
%config %{_sysconfdir}/exim/exim-greylist.conf.inc
%ghost %{_var}/spool/exim/db/greylist.db
%{_sysconfdir}/exim/mk-greylist-db.sql
%{_sysconfdir}/cron.daily/greylist-tidy.sh

%changelog
* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 4.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Jan 03 2026 Jaroslav Škarvada  <jskarvad@redhat.com> - 4.99.1-1
- New version
  Resolves: CVE-2025-67896

* Mon Nov 17 2025 Jaroslav Škarvada  <jskarvad@redhat.com> - 4.99-2
- Fixed lookup libraries names
  Resolves: rhbz#2415008

* Tue Nov 04 2025 Jaroslav Škarvada  <jskarvad@redhat.com> - 4.99-1
- New version
  Resolves: rhbz#2406726

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.98.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Mon Jul 07 2025 Jitka Plesnikova <jplesnik@redhat.com> - 4.98.2-3
- Perl 5.42 rebuild

* Fri May 09 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.98.2-2
- Make sure the /usr/sbin/sendmail symlink exists (if /usr/sbin is a directory)

* Wed Mar 26 2025 Jaroslav Škarvada <jskarvad@redhat.com> - 4.98.2-1
- New version
  Resolves: CVE 2025-30232

* Mon Feb 24 2025 Jaroslav Škarvada <jskarvad@redhat.com> - 4.98.1-1
- New version
  Resolves: rhbz#2346977
- Fixed possible remote SQL injection
  Resolves: CVE-2025-26794
- Updated exim maintainers keyring

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.98-7
- Add sysusers.d config file to allow rpm to create users/groups automatically

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 4.98-6
- Add explicit BR: libxcrypt-devel

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.98-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 12 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.98-4
- Rebuilt for the bin-sbin merge (2nd attempt)

* Thu Jul 25 2024 Miroslav Suchý <msuchy@redhat.com> - 4.98-3
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 4.98-1
- New version
  Resolves: rhbz#2297124
- Fixed incorrect parsing of multiline rfc2231 header filename
  Resolves: CVE-2024-39929
- Dropped upstreamed patches

* Tue Jul 09 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.97.1-9
- Rebuilt for the bin-sbin merge

* Tue Jun 11 2024 Jitka Plesnikova <jplesnik@redhat.com> - 4.97.1-8
- Perl 5.40 rebuild

* Sat Jun  1 2024 Tom Hughes <tom@compton.nu> - 4.97.1-7
- Enable SRS support

* Tue Mar  5 2024 David Woodhouse <dwmw2@infradead.org> 4.97.1-6
- Use ':' instead of '.' as separator for chown

* Mon Mar  4 2024 David Woodhouse <dwmw2@infradead.org> 4.97.1-5
- Fix PCRE2 memory use explosion (Exim bug 3047)
  Resolves: rhbz#2259382

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.97.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.97.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 16 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 4.97.1-2
- Support old-format message_id spoolfiles for mailq
  Resolves: rhbz#2258027

* Wed Jan  3 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 4.97.1-1
- New version
  Resolves: rhbz#2256145
- Fixed SMTP smuggling vulnerability
  Resolves: CVE-2023-51766

* Mon Nov  6 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 4.97-1
- New version
  Resolves: rhbz#2247920

* Mon Oct 16 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 4.96.2-1
- New version
  Resolves: rhbz#2244300

* Thu Oct 12 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 4.96.1-2
- Build against the 'mariadb-connector-c-devel' package (patch by mschorm)
  Resolves: rhbz#2241091

* Mon Oct  2 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 4.96.1-1
- New version
  Resolves: rhbz#2241735
  Resolves: rhbz#2241538
  Resolves: rhbz#2241539
  Resolves: rhbz#2241525
  Resolves: rhbz#2241527
  Resolves: rhbz#2241528
  Resolves: rhbz#2241529
  Resolves: rhbz#2241531
  Resolves: rhbz#2241532
  Resolves: rhbz#2241542
  Resolves: rhbz#2241544

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.96-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Jul 11 2023 Jitka Plesnikova <jplesnik@redhat.com> - 4.96-9
- Perl 5.38 rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.96-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Dec 13 2022 Florian Weimer <fweimer@redhat.com> - 4.96-7
- Fix pointer truncation bug in DLOPEN_LOCAL_SCAN extension (#2152978)

* Tue Nov 22 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.96-6
- Fixed exit on attempt to rewrite malformed address
  Resolves: rhbz#2143283

* Tue Nov  1 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.96-5
- Fixed use after free in dmarc_dns_lookup
  Resolves: CVE-2022-3620

* Wed Oct 19 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.96-4
- Fixed use after free in regex handler
  Resolves: CVE-2022-3559

* Mon Sep 12 2022 Marcel Härry <mh+fedora@scrit.ch> - 4.96-3
- Fix "tainted search query is not properly quoted" for greylisting

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.96-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 28 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 4.96-1
- New version
  Resolves: rhbz#2101104

* Mon May 30 2022 Jitka Plesnikova <jplesnik@redhat.com> - 4.95-4
- Perl 5.36 rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.95-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 4.95-2
- Rebuild(libnsl2)
- Drop support for NISPLUS, as libnsl2 >= 2.0.0 does not support it anymore

* Mon Oct  4 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 4.95-1
- New version
  Resolves: rhbz#2008452

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 4.94.2-4
- Rebuilt with OpenSSL 3.0.0

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.94.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Fri May 21 2021 Jitka Plesnikova <jplesnik@redhat.com> - 4.94.2-2
- Perl 5.34 rebuild

* Tue May  4 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 4.94.2-1
- New version
  Resolves: rhbz#1956859

* Thu Mar 25 2021 Jaroslav Škarvada <jskarvad@redhat.com> - 4.94-7
- Fixed cname handling in TLS certificate verification
  Resolves: rhbz#1942582

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 4.94-6
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 08 2021 Pavel Raiskup <praiskup@redhat.com> - 4.94-5
- rebuild for libpq ABI fix rhbz#1908268

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.94-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.94-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 22 2020 Jitka Plesnikova <jplesnik@redhat.com> - 4.94-2
- Perl 5.32 rebuild

* Mon Jun  1 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.94-1
- New version
  Resolves: rhbz#1842590
- Used Exim maintainers keyring for GPG verification
- Dropped CVE-2020-12783 patch (upstreamed)
- Used better workaround for rhbz#1791878
  Resolves: rhbz#1842633

* Fri May 15 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.93-8
- Fixed out-of-bounds read in the SPA authenticator
  Resolves: CVE-2020-12783

* Wed Apr 29 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.93-7
- Improved the spec file not to override LDFLAGS

* Wed Apr 29 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.93-6
- Updated config to explictly link with spf2 and opendmarc
- Fixed bogus date in changelog

* Wed Apr 29 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.93-5
- Bump for rebuild with the fixed clamd requirement
  Resolves: rhbz#1801329

* Fri Mar 20 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.93-4
- Workaround for upgrade conflict
  Resolves: rhbz#1791878

* Thu Feb 20 2020 Tom Hughes <tom@compton.nu> - 4.93-3
- Enable SPF and DMARC support

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.93-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Jan 12 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.93-1
- New version
  Resolves: rhbz#1782320
- Consolidated and simplified patches
- Dropped dane-enable patch (not needed)

* Thu Jan  2 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92.3-5
- Fixed FTBFS due to changes in clamav package
  Resolves: rhbz#1787285

* Fri Nov 22 2019 Felix Schwarz <fschwarz@fedoraproject.org> - 4.92.3-4
- enable GPG-based source file verification

* Thu Oct 10 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92.3-3
- Enabled local_scan

* Thu Oct 10 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92.3-2
- Dropped sysvinit artifacts

* Mon Sep 30 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92.3-1
- New version
  Resolves: rhbz#1756656
  Resolves: CVE-2019-16928

* Fri Sep  6 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92.2-1
- New version
  Resolves: CVE-2019-15846

* Tue Aug 20 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92.1-1
- New version
  Resolves: rhbz#1742312

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.92-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu May 30 2019 Jitka Plesnikova <jplesnik@redhat.com> - 4.92-8
- Perl 5.30 rebuild

* Wed Mar 27 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92-7
- Enabled DANE support
  Resolves: rhbz#1693202

* Wed Mar 20 2019 Peter Robinson <pbrobinson@fedoraproject.org> 4.92-6
- Drop F-23 conditionals, and related obsolete bits

* Tue Mar 19 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92-5
- Processed greylist.db by cron job only if it has non zero size
  Resolves: rhbz#1689211

* Mon Mar  4 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92-4
- Fixed greylist-conf patch
  Related: rhbz#1679274

* Sat Mar  2 2019 Tim Landscheidt <tim@tim-landscheidt.de> - 4.92-3
- Fix syntax error in exim.conf (#1679274)
- Use properly compressed empty mailq.1.gz as ghost file
- Add basic check that configuration file is valid

* Wed Feb 20 2019 Marcel Härry <mh+fedora@scrit.ch> - 4.92-2
- Enable proxy and socks support
  Resolves: rhbz#1542870

* Mon Feb 11 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 4.92-1
- New version
  Resolves: rhbz#1674282

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.91-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4.91-5
- Rebuilt for libcrypt.so.2 (#1666033)

* Fri Jul 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.91-4
- Fixed FTBFS by adding gcc requirement

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.91-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jun 27 2018 Jitka Plesnikova <jplesnik@redhat.com> - 4.91-2
- Perl 5.28 rebuild

* Thu Apr 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.91-1
- New version
  Resolves: rhbz#1567670
- Dropped dec64table-read-fix patch (already upstream)
- De-fuzzified patches

* Wed Mar 14 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.90.1-4
- Fixed dec64table OOB read in b64decode
- De-fuzzified nsl-fix patch

* Fri Feb 16 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.90.1-3
- Dropped dynlookup-config patch (merged into config patch)

* Fri Feb 16 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.90.1-2
- Fixed mysql module

* Tue Feb 13 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.90.1-1
- New version
  Resolves: rhbz#1527710
- Fixed buffer overflow in utility function
  Resolves: CVE-2018-6789
- Updated and defuzzified patches
- Dropped mariadb-macro-fix patch (not needed)
- Dropped CVE-2017-1000369, calloutsize, CVE-2017-16943,
  CVE-2017-16944 patches (all upstreamed)

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.89-11
- Rebuilt for switch to libxcrypt

* Wed Jan 17 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 4.89-10
- Fixed FTBFS due to NIS removal from glibc
  Resolves: rhbz#1534920

* Fri Dec  1 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.89-9
- Fixed denial of service
  Resolves: CVE-2017-16944

* Thu Nov 30 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.89-8
- Dropped tcp_wrappers support
  Resolves: rhbz#1518763

* Mon Nov 27 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.89-7
- Fixed use-after-free
  Resolves: CVE-2017-16943

* Fri Nov 10 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.89-6
- Used mariadb-connector-c-devel instead of mysql-devel
  Resolves: rhbz#1494094

* Fri Aug 18 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.89-5
- Fixed compilation with the mariadb-10.2
  Resolves: rhbz#1467312
- Fixed multiple memory leaks
  Resolves: CVE-2017-1000369
- Fixed typo causing exim-clamav to create /0750 directory
  Resolves: rhbz#1412028
- On callout avoid SIZE option when doing recipient verification with
  caching enabled
  Resolves: rhbz#1482217
- Fixed some minor whitespace problems in the spec

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.89-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jun 04 2017 Jitka Plesnikova <jplesnik@redhat.com> - 4.89-2
- Perl 5.26 rebuild

* Wed Mar  8 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.89-1
- New version
  Resolves: rhbz#1430156
- Switched to xz archive
- Dropped DKIM-fix patch (already upstream)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.88-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 23 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 4.88-3
- Fixed DKIM
- Defuzzified patches and fixed some whitespaces

* Sat Jan 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 4.88-2
- Move tmpfiles.d config to %%{_tmpfilesdir}
- Install license files as %%license

* Sun Dec 25 2016 David Woodhouse <dwmw2@infradead.org> - 4.88-1
- Update to 4.88 (CVE-2016-9963 / rhbz#1405323)

* Thu Jun  9 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 4.87-5
- Allow configuration of user:group through sysconfig
  Resolves: rhbz#1344250

* Sat May 14 2016 Jitka Plesnikova <jplesnik@redhat.com> - 4.87-4
- Perl 5.24 rebuild

* Wed May  4 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 4.87-3
- Dropped sa-exim which has been obsoleted long time ago by the proper
  built-in ACL support
- Unconditionalized sources
  Resolves: rhbz#1332211

* Mon Apr 18 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 4.87-2
- Used sane environment defaults in default configuration
  Resolves: rhbz#1323775

* Sun Apr 10 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 4.87-1
- New version
  Resolves: rhbz#1325557

* Thu Mar  3 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 4.86.2-1
- New version
  Resolves: rhbz#1314118
- Fixed local privilege escalation for set-uid root when using perl_startup
  Resolves: CVE-2016-1531
- Defuzzified patches

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.86-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov  2 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 4.86-3
- Fixed exim-gen-cert not to output error on success

* Fri Sep 18 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 4.86-2
- Hardened build, rebuilt with the full RELRO (only the daemon)

* Mon Jul 27 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 4.86-1
- New version
  Resolves: rhbz#1246923
- Updated and defuzzified patches

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.85-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 03 2015 Jitka Plesnikova <jplesnik@redhat.com> - 4.85-4
- Perl 5.22 rebuild

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 4.85-3
- Drop sysvinit subpackages for F23+

* Tue Feb 10 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 4.85-2
- Shared objects are now compiled with PIC, not PIE, which is needed for gcc-5,
  (by pic patch)
  Resolves: rhbz#1190784

* Tue Jan 13 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 4.85-1
- New version
  Resolves: rhbz#1181479
- De-fuzzified config and dlopen-localscan patches

* Fri Oct 10 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.84-4
- Do not override LFLAGS (problem reported by Todd Lyons)

* Tue Aug 26 2014 Jitka Plesnikova <jplesnik@redhat.com> - 4.84-3
- Perl 5.20 rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.84-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.84-1
- New version
  Resolves: rhbz#1129036
- De-fuzzified dlopen-localscan patch

* Wed Jul 23 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.83-1
- New version
  Resolves: CVE-2014-2972
- De-fuzzified patches

* Wed Jul  9 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.82.1-4
- Do not build clamav on RHEL
- Fixed build without clamav

* Wed Jul  9 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.82.1-3
- Dropped support for FC6 and earlier, without sa and with clamav are
  now the defaults, they can be overriden by --with / --without

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.82.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 4.82.1-1
- New version

* Tue Oct 29 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.82-1
- New version
  Resolves: rhbz#1024196
- Fixed bogus dates in the changelog (best effort)
- De-fuzzified patches
- Fixed double packaging of mailq.1.gz

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 4.80.1-6
- Perl 5.18 rebuild

* Sat Jul 27 2013 Jóhann B. Guðmundsson <johannbg@fedoraproject.org> - 4.80.1-5
- Add a missing requirement on crontabs to spec file

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.80.1-4
- Perl 5.18 rebuild

* Tue Feb 26 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 4.80.1-3
- Switched to systemd-rpm macros
  Resolves: rhbz#850102

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.80.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.80.1-1
- New version
  Resolves: CVE-2012-5671

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.80-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 4.80-2
- Perl 5.16 rebuild

* Mon Jun  4 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.80-1
- New version
  Resolves: rhbz#827963

* Fri Apr  6 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.77-2
- Rebuilt with libdb-5.2

* Wed Feb 29 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.77-1
- New version
- Removed unused ldap-deprecated patch
- Dropped strict aliasing patch
- Built with libdb-5.2

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 4.76-9
- Rebuild against PCRE 8.30

* Mon Feb  6 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.76-8
- Workarounded wrong SELinux context of /var/log/clamd.exim

* Thu Feb  2 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.76-7
- Fixed exim-clamav to work with /var/run on tmpfs

* Mon Jan 30 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 4.76-6
- Introduced systemd unit file, thanks to Jóhann B. Guðmundsson <johannbg@gmail.com>
  Resoloves: rhbz#721354
- Provided SysV initscripts in sysvinit subpackages
- Used PrivateTmp
  Resolves: rhbz#782502

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.76-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 16 2011 Marcela Mašláňová <mmaslano@redhat.com> - 4.76-4
- Perl mass rebuild

* Mon May 09 2011 David Woodhouse <David.Woodhouse@intel.com> - 4.76-3
- Update to 4.76 (fixes CVE-2011-1407, CVE-2011-1764) (#702474)

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 4.73-3
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.73-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 05 2011 David Woodhouse <David.Woodhouse@intel.com> - 4.73-1
- Update to 4.73

* Sat Aug 07 2010 David Woodhouse <David.Woodhouse@intel.com> - 4.72-2
- Fedora infrastructure ate my package; bump release and rebuild

* Thu Jun 03 2010 David Woodhouse <David.Woodhouse@intel.com> - 4.72-1
- Update to 4.72 (fixes CVE-2010-2023, CVS-2010-2024)

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 4.71-4
- Mass rebuild with perl-5.12.0

* Thu Mar 18 2010 Miroslav Lichvar <mlichvar@redhat.com> - 4.71-3
- follow guidelines for alternatives (#570800)
- fix init script LSB compliance (#523238)
- handle undefined NETWORKING in init script (#483528)

* Tue Feb 09 2010 Adam Jackson <ajax@redhat.com> 4.71-2
- Fix FTBFS with --no-add-needed

* Thu Dec 24 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-20
- Update to 4.71

* Fri Dec  4 2009 Stepan Kasal <skasal@redhat.com> - 4.69-19
- rebuild against perl 5.10.1

* Mon Oct 05 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-18
- Fix typo in clamd %%post (#527085)

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 4.69-17
- Use password-auth common PAM configuration instead of system-auth

* Mon Aug 31 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-16
- Create group for exim with correct gid (#518706)
- Allow expansion of spamd_address

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.69-15
- rebuilt with new openssl

* Tue Aug 18 2009 Miroslav Lichvar <mlichvar@redhat.com> - 4.69-14
- Move certificate generation to init script (#517013)
- Fix strict aliasing warning

* Wed Aug 12 2009 David Woodhouse <David.Woodhouse@intel.com> - 4.69-13
- Cope with lack of /etc/sysconfig/network (#506330)
- Require /etc/pki/tls/ directories
- Provide exim-tidydb cron job (#481426)
- Provide clamd.exim log file (#452358)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.69-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 23 2009 Michael Schwendt <mschwendt@fedoraproject.org> - 4.69-11
- Add subpackage dependencies to fix unowned directories (#474869).
- Add missing defattr.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.69-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Jan 24 2009 Caolán McNamara <caolanm@redhat.com> 4.69-9
- rebuild for dependencies

* Thu Aug 28 2008 Michael Schwendt <mschwendt@fedoraproject.org> 4.69-8
- Include unowned directories.

* Wed Aug 13 2008 David Woodhouse <David.Woodhouse@intel.com> 4.69-7
- Rediff all patches to cope with new zero-fuzz policy

* Wed Aug 13 2008 David Woodhouse <David.Woodhouse@intel.com> 4.69-6
- Add $RPM_OPT_FLAGS in config instead of overriding on make command line.
  (to fix the setting of largefile options which we were killing)

* Sat Apr 19 2008 David Woodhouse <dwmw2@infradead.org> 4.69-5
- Add dynamic lookup patch, split into subpackages (#199256)

* Tue Mar 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> 4.69-4
- add Requires for versioned perl (libperl.so)

* Mon Mar 17 2008 David Woodhouse <dwmw2@infradead.org> 4.69-3
- Rebuild for new perl

* Mon Feb 04 2008 Dennis Gilmore <dennis@ausil.us> 4.69-2
- sparc needs -fPIE not -fpie

* Thu Jan 03 2008 David Woodhouse <dwmw2@infradead.org> 4.69-1
- Update to 4.69
- Provide server(smtp) (#380611)

* Wed Dec 05 2007 David Woodhouse <dwmw2@infradead.org> 4.68-3
- Rebuild for OpenSSL/OpenLDAP

* Sun Nov 25 2007 David Woodhouse <dwmw2@infradead.org> 4.68-2
- Fix handling of IPv6 addresses as "known resenders" in example greylist
  configuration

* Fri Aug 31 2007 David Woodhouse <dwmw2@infradead.org> 4.68-1
- Update to 4.68

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> 4.67-5
- Handle open() being a macro

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> 4.67-4
- Update licence

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> 4.67-3
- Rebuild

* Wed Jun 27 2007 David Woodhouse <dwmw2@infradead.org> 4.67-2
- Fix typo in config (#246799)

* Wed Jun 27 2007 David Woodhouse <dwmw2@infradead.org> 4.67-1
- Update to 4.67
- Add config example for using a smarthost, with SMTP AUTH.

* Thu Feb  8 2007 David Woodhouse <dwmw2@infradead.org> 4.66-3
- Improve documentation and error handling in greylist ACL.
- Require HELO before mail

* Wed Feb  7 2007 David Woodhouse <dwmw2@infradead.org> 4.66-2
- Add example of greylisting implementation in Exim ACLs

* Tue Feb  6 2007 David Woodhouse <dwmw2@infradead.org> 4.66-1
- Update to 4.66
- Add dovecot authenticator
- Add 'reload' in init script (#219174)

* Tue Oct 17 2006 Christian Iseli <Christian.Iseli@licr.org> 4.63-6
- Own /etc/exim directory

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> 4.63-5
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 25 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-4
- Set home_directory on lmtp_transport by default

* Sun Sep 3 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-3
- chmod +x /etc/init.d/clamd.exim
- Make exim-clamav package require exim (since it uses the same uid)

* Sun Sep 3 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-2
- Add procmail router and transport (#146848)
- Add localhost and localhost.localdomain as local domains (#198511)
- Fix mispatched authenticators (#204591)
- Other cleanups of config file and extra examples
- Add exim-clamav subpackage
- Use existing TLS cert on upgrade, even though it moved

* Sat Aug 26 2006 David Woodhouse <dwmw2@infradead.org> - 4.63-1
- Update to 4.63
- Disable sa-exim, but leave the dlopen patch in

* Wed Jul 19 2006 Thomas Woerner <twoerner@redhat.com> - 4.62-6
- final version
- changed permissions of /etc/pki/tls/*/exim.pem to 0600
- config(noreplace) for /etc/logrotate.d/exim, /etc/pam.d/exim and
  /etc/sysconfig/exim

* Mon Jul 17 2006 Thomas Woerner <twoerner@redhat.com> - 4.62-5
- fixed certs path
- fixed permissions for some binaries
- fixed pam file to use include instead of pam_stack

* Tue Jul  4 2006 David Woodhouse <dwmw2@redhat.com> 4.62-4
- Package review

* Wed Jun 28 2006 David Woodhouse <dwmw2@redhat.com> 4.62-3
- BR tcp_wrappers

* Tue May  2 2006 David Woodhouse <dwmw2@redhat.com> 4.62-2
- Bump release to work around 'make tag' error

* Tue May  2 2006 David Woodhouse <dwmw2@redhat.com> 4.62-1
- Update to 4.62

* Fri Apr  7 2006 David Woodhouse <dwmw2@redhat.com> 4.61-2
- Define LDAP_DEPRECATED to ensure ldap functions are all declared.

* Tue Apr  4 2006 David Woodhouse <dwmw2@redhat.com> 4.61-1
- Update to 4.61

* Thu Mar 23 2006 David Woodhouse <dwmw2@redhat.com> 4.60-5
- Fix eximon buffer overflow (#186303)

* Tue Mar 21 2006 David Woodhouse <dwmw2@redhat.com> 4.60-4
- Actually enable Postgres

* Tue Mar  7 2006 David Woodhouse <dwmw2@redhat.com> 4.60-3
- Rebuild

* Tue Nov 29 2005 David Woodhouse <dwmw2@redhat.com> 4.60-2
- Require libXt-devel

* Tue Nov 29 2005 David Woodhouse <dwmw2@redhat.com> 4.60-1
- Update to 4.60

* Sun Nov 13 2005 David Woodhouse <dwmw2@redhat.com> 4.54-4
- Fix 64-bit build

* Fri Nov 11 2005 David Woodhouse <dwmw2@redhat.com> 4.54-3
- Update X11 BuildRequires

* Wed Oct  5 2005 David Woodhouse <dwmw2@redhat.com> 4.54-2
- Rebuild for new OpenSSL
- Add MySQL and Postgres support to keep jgarzik happy

* Wed Oct  5 2005 David Woodhouse <dwmw2@redhat.com> 4.54-1
- Update to Exim 4.54
- Enable sqlite support

* Thu Aug 25 2005 David Woodhouse <dwmw2@redhat.com> 4.52-2
- Use system PCRE

* Fri Jul  1 2005 David Woodhouse <dwmw2@redhat.com> 4.52-1
- Update to Exim 4.52

* Thu Jun 16 2005 David Woodhouse <dwmw2@redhat.com> 4.51-3
- Rebuild for -devel

* Thu Jun 16 2005 David Woodhouse <dwmw2@redhat.com> 4.51-2
- Update CSA patch

* Wed May  4 2005 David Woodhouse <dwmw2@redhat.com> 4.51-1
- Update to Exim 4.51
- Include Tony's CSA support patch

* Tue Feb 22 2005 David Woodhouse <dwmw2@redhat.com> 4.50-2
- Move exim-doc into a separate package

* Tue Feb 22 2005 David Woodhouse <dwmw2@redhat.com> 4.50-1
- Update to Exim 4.50 and sa-exim 4.2
- Default headers_charset to utf-8
- Add sample spamd stuff to default configuration like exiscan-acl used to

* Sat Jan 15 2005 David Woodhouse <dwmw2@redhat.com> 4.44-1
- Update to Exim 4.44 and exiscan-acl-4.44-28

* Tue Jan  4 2005 David Woodhouse <dwmw2@redhat.com> 4.43-4
- Fix buffer overflows in host_aton() and SPA authentication

* Thu Dec 16 2004 David Woodhouse <dwmw2@redhat.com> 4.43-3
- Demonstrate SASL auth configuration in default config file
- Enable TLS and provide certificate if necessary
- Don't reject all GB2312 charset mail by default

* Mon Dec  6 2004 Thomas Woerner <twoerner@redhat.com> 4.43-2
- rebuild

* Thu Oct  7 2004 Thomas Woerner <twoerner@redhat.com> 4.43-1
- new version 4.43 with sasl support
- new exiscan-acl-4.43-28
- new config.samples and FAQ-html (added publication date)
- new BuildRequires for cyrus-sasl-devel openldap-devel openssl-devel
  and PreReq for cyrus-sasl openldap openssl

* Mon Sep 13 2004 Thomas Woerner <twoerner@redhat.com> 4.42-2
- update to sa-exim-4.1: fixes spamassassin's new score= string (#131796)

* Fri Aug 27 2004 Thomas Woerner <twoerner@redhat.com> 4.42-1
- new version 4.42

* Mon Aug  2 2004 Thomas Woerner <twoerner@redhat.com> 4.41-1
- new version 4.41

* Fri Jul  2 2004 Thomas Woerner <twoerner@redhat.com> 4.34-3
- added pre-definition of local_delivery using Cyrus-IMAP (#122912)
- added BuildRequires for pam-devel (#124555)
- fixed format string bugs (#125117)
- fixed sa-exim code placed wrong in spec file (#127102)
- extended postun with alternatives call

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed May 12 2004 David Woodhouse <dwmw2@redhat.com> 4.34-1
- Update to Exim 4.34, exiscan-acl 4.34-21

* Sat May 8 2004 David Woodhouse <dwmw2@redhat.com> 4.33-2
- fix buffer overflow in header_syntax check

* Wed May 5 2004 David Woodhouse <dwmw2@redhat.com> 4.33-1
- Update to Exim 4.33, exiscan-acl 4.33-20 to
  fix crashes both in exiscan-acl and Exim itself.

* Fri Apr 30 2004 David Woodhouse <dwmw2@redhat.com> 4.32-2
- Enable IPv6 support, Cyrus saslauthd support, iconv.

* Thu Apr 15 2004 David Woodhouse <dwmw2@redhat.com> 4.32-1
- update to Exim 4.32, exiscan-acl 4.32-17, sa-exim 4.0
- Fix Provides: and Source urls.
- include exiqgrep, exim_checkaccess, exipick
- require /etc/aliases instead of setup

* Tue Feb 24 2004 Thomas Woerner <twoerner@redhat.com> 4.30-6.1
- rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Thomas Woerner <twoerner@redhat.com> 4.30-5
- /usr/lib/sendmail is in alternatives, now
- /etc/alises is now in setup: new Requires for setup >= 2.5.31-1

* Tue Jan 13 2004 Thomas Woerner <twoerner@redhat.com> 4.30-4
- fixed group test in init script
- fixed config patch: use /etc/exim/exim.conf instead of /usr/exim/exim4.conf

* Wed Dec 10 2003 Nigel Metheringham <Nigel.Metheringham@InTechnology.co.uk> - 4.30-3
- Use exim.8 manpage from upstream
- Add eximstats.8 man page (from pod)
- Fixed mailq(1) man page alternatives links

* Mon Dec 08 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not package /etc/aliases. We currently require sendmail rpm until
  /etc/aliases moves into a more suitable rpm like "setup" or something else.

* Thu Dec  4 2003 Thomas Woerner <twoerner@redhat.com> 4.30-1
- new version 4.30
- new exiscan-acl-4.30-14
- disabled pie for s390 and s390x

* Wed Dec  3 2003 Tim Waugh <twaugh@redhat.com>
- Fixed PIE support to make it actually work.

* Wed Dec  3 2003 Thomas Woerner <twoerner@redhat.com> 4.24-1.2
- added -fPIE to CFLAGS

* Sat Nov 15 2003 Thomas Woerner <twoerner@redhat.com> 4.24-1.1
- fixed useradd in pre
- fixed alternatives in post

* Thu Nov 13 2003 Thomas Woerner <twoerner@redhat.com> 4.24-1
- new version 4.24 with LDAP and perl support
- added SpamAssassin sa plugin

* Mon Sep 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 3.36-1
- 3.36, fixes security bugs

* Thu Jun 21 2001 Tim Waugh <twaugh@redhat.com> 3.22-14
- Bump release number.

* Tue Jun 12 2001 Tim Waugh <twaugh@redhat.com> 3.22-13
- Remove pam-devel build dependency in order to share package between
  Guinness and Seawolf.

* Fri Jun  8 2001 Tim Waugh <twaugh@redhat.com> 3.22-12
- Fix format string bug.

* Wed May  2 2001 Tim Waugh <twaugh@redhat.com> 3.22-11
- SIGALRM patch from maintainer (bug #20908).
- There's no README.IPV6 any more (bug #32378).
- Fix logrotate entry for exim's pidfile scheme (bug #35436).
- ignore_target_hosts crash fix from maintainer.
- Make the summary start with a capital letter.
- Add reload entry to initscript; use $0 in strings.

* Sun Mar  4 2001 Tim Waugh <twaugh@redhat.com> 3.22-10
- Make sure db ownership is correct on upgrade, since we don't run as
  root when running as a daemon any more.

* Fri Mar  2 2001 Tim Powers <timp@redhat.com>
- rebuilt against openssl-0.9.6-1

* Sat Feb 17 2001 Tim Waugh <twaugh@redhat.com>
- Run as user mail, group mail when we drop privileges (bug #28193).

* Tue Feb 13 2001 Tim Powers <timp@redhat.com>
- added conflict with postfix

* Thu Jan 25 2001 Tim Waugh <twaugh@redhat.com>
- Avoid using zero-length salt in crypteq expansion.

* Tue Jan 23 2001 Tim Waugh <twaugh@redhat.com>
- Redo initscript internationalisation.
- Initscript uses bash not sh.

* Mon Jan 22 2001 Tim Waugh <twaugh@redhat.com>
- Okay, the real bug was in libident.

* Mon Jan 22 2001 Tim Waugh <twaugh@redhat.com>
- Revert the RST patch for now; if it's needed, it's a pidentd bug
  and should be fixed there.

* Mon Jan 22 2001 Tim Waugh <twaugh@redhat.com>
- 3.22.
- Build requires XFree86-devel.

* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- New-style prereqs.
- Initscript internationalisation.

* Thu Jan 11 2001 Tim Waugh <twaugh@redhat.com>
- Security patch no longer required; 3.20 and later have a hide feature
  to do the same thing.
- Mark exim.conf noreplace.
- Better libident (RST) patch.

* Wed Jan 10 2001 Tim Waugh <twaugh@redhat.com>
- Fix eximconfig so that it tells the user the correct place to look
  for documentation
- Fix configure.default to deliver mail as group mail so that local
  delivery works

* Tue Jan 09 2001 Tim Waugh <twaugh@redhat.com>
- 3.21

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Enable TLS support (bug #23196)

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- 3.20 (bug #21895).  Absorbs configure.default patch
- Put URLs in source tags where applicable
- Add build requirement on pam-devel

* Wed Oct 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix up eximconfig's header generation (we're not Debian), Bug #18068
- BuildRequires db2-devel (Bug #18089)
- Fix typo in logrotate script (Bug #18308)
- Local delivery must be setuid to work (Bug #18314)
- Don't send TCP RST packages to ident (Bug #19048)

* Wed Oct 18 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 3.16
- fix security bug
- some specfile cleanups
- fix handling of RPM_OPT_FLAGS

* Fri Aug 18 2000 Tim Powers <timp@redhat.com>
- fixed bug #16535, logrotate script changes

* Thu Aug 17 2000 Tim Powers <timp@redhat.com>
- fixed bug #16460
- fixed bug #16458
- fixed bug #16476

* Wed Aug 2 2000 Tim Powers <timp@redhat.com>
- fixed bug #15142

* Fri Jul 28 2000 Than Ngo <than@redhat.de>
- add missing restart function in startup script
- add rm -rf $RPM_BUILD_ROOT in install section
- use %%{_tmppath}

* Fri Jul 28 2000 Tim Powers <timp@redhat.com>
- fixed initscript so that condrestart doesn't return 1 when the test fails

* Mon Jul 24 2000 Prospector <prospector@redhat.com>
- rebuilt

* Mon Jul 17 2000 Tim Powers <timp@redhat.com>
- inits bakc to rc.d/init.d, using service to start inits

* Thu Jul 13 2000 Tim Powers <timp@redhat.com>
- applied patch from bug #13890

* Mon Jul 10 2000 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jul 06 2000 Tim Powers <timp@redhat.com>
- added patch submitted by <Chris.Keane@comlab.ox.ac.uk>, fixes bug #13539

* Thu Jul 06 2000 Tim Powers <timp@redhat.com>
- fixed broken prereq to require /etc/init.d

* Tue Jun 27 2000 Tim Powers <timp@redhat.com>
- PreReq initscripts >= 5.20

* Mon Jun 26 2000 Tim Powers <timp@redhat.com>
- fix init.d script location
- add condrestart to init.d script

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- migrate to system-auth setup

* Tue Jun 6 2000 Tim Powers <timp@redhat.com>
- fixed man page location

* Tue May 9 2000 Tim Powers <timp@redhat.com>
- rebuilt for 7.0

* Fri Feb 04 2000 Tim Powers <timp@redhat.com>
- fixed the groups to be in Red Hat groups.
- removed Vendor header since it is going to be marked Red Hat in our build
	system.
- quiet setups
- strip binaries
- fixed so that man pages can be auto gzipped by new RPM (in files list
	/usr/man/*/* )
- built for Powertools 6.2

* Tue Jan 18 2000 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.13
- Removed i386 specialization
- Added syslog support

* Wed Dec 8 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.12
- Procmail no longer used as the delivery agent

* Wed Dec 1 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.11

* Sat Nov 27 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added /etc/pam.d/exim

* Wed Nov 24 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to exim 3.10

* Thu Nov 11 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added eximconfig script, thanks to Mark Baker
- Exim now uses the Berkeley DB library.

* Wed Aug 4 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Upgraded to version 3.03
- Removed version number out of the spec file name.

* Fri Jul 23 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added embedded Perl support.
- Added tcp_wrappers support.
- Added extra documentation in a new doc subpackage.

* Mon Jul 12 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added /usr/sbin/sendmail as a link to exim.
- Fixed wrong filenames in logrotate entry. 

* Sun Jul 11 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Now using the '%%changelog' tag.
- Removed the SysV init links - let chkconfig handle them. 
- Replaced install -d with mkdir -p

* Sat Jul 10 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Fixed owner of the exim-mon files - the owner is now root

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Removed executable permission bits of /etc/exim.conf
- Removed setuid permission bits of all programs except exim
- Changed spool/log directory owner/groups to 'mail'
- Changed the default configuration file to make exim run
      as user and group 'mail'.

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added the /usr/bin/rmail -> /usr/sbin/exim symlink.
- Added the convert4r3 script.
- Added the transport-filter.pl script to the documentation.

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added procmail transport and director, and made that the
      default.
- Added the unknownuser.sh script to the documentation.

* Thu Jul 08 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added manpage for exim.
- Fixed symlinks pointing to targets under Buildroot.
- The exim logfiles will now only be removed when uninstalling,
      not upgrading.

* Wed Jul 07 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- Added 'Obsoletes' header.
- Added several symlinks to /usr/sbin/exim.

* Wed Jul 07 1999 Mark Bergsma <mark@mbergsma.demon.nl>
- First RPM packet release.
- Not tested on other architectures/OS'es than i386/Linux..
