Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# package options
%global with_tls	yes
%global with_sasl2	yes
%global with_milter	yes
%global with_ldap	yes
%global enable_pie	yes

%global sendmailcf %{_datadir}/sendmail-cf
%global stdir %{_localstatedir}/log/mail
%global smshell /usr/sbin/nologin
%global spooldir %{_localstatedir}/spool
%global maildir %{_sysconfdir}/mail
%global sslcert %{_sysconfdir}/pki/tls/certs/sendmail.pem
%global sslkey %{_sysconfdir}/pki/tls/private/sendmail.key

# hardened build if not overridden
%{!?_hardened_build:%global _hardened_build 1}

Summary: A widely used Mail Transport Agent (MTA)
Name: sendmail
Version: 8.15.2
Release: 46%{?dist}
License: Sendmail
URL: https://www.sendmail.org/

Source0: ftp://ftp.sendmail.org/pub/sendmail/sendmail.%{version}.tar.gz
# Systemd Service file
Source1: sendmail.service
# NetworkManager dispatch script
Source2: sendmail.nm-dispatcher
# script to generate db and cf files
Source3: sendmail.etc-mail-make
# default sysconfig file
Source4: sendmail.sysconfig
# default /etc/mail/Makefile
Source5: sendmail.etc-mail-Makefile
# default sendmail.mc
Source6: sendmail-redhat.mc
# Systemd Service file
Source7: sm-client.service
# pam config
Source8: sendmail.pam
# sasl2 config
Source11: Sendmail-sasl2.conf
# default /etc/mail/access
Source12: sendmail-etc-mail-access
# default /etc/mail/domaintable
Source13: sendmail-etc-mail-domaintable
# default /etc/mail/local-host-names
Source14: sendmail-etc-mail-local-host-names
# default /etc/mail/mailertable
Source15: sendmail-etc-mail-mailertable
# default /etc/mail/trusted-users
Source16: sendmail-etc-mail-trusted-users
# default /etc/mail/virtusertable
Source17: sendmail-etc-mail-virtusertable
# fix man path and makemap man page
Patch3: sendmail-8.14.4-makemapman.patch
# fix smrsh paths
Patch4: sendmail-8.14.3-smrsh_paths.patch
# fix sm-client.pid path
Patch7: sendmail-8.14.9-pid.patch
# fix sendmail man page
Patch10: sendmail-8.15.1-manpage.patch
# compile with -fpie
Patch11: sendmail-8.15.1-dynamic.patch
# fix cyrus path
Patch12: sendmail-8.13.0-cyrus.patch
# fix aliases.db path
Patch13: sendmail-8.15.1-aliases_dir.patch
# fix vacation Makefile
Patch14: sendmail-8.14.9-vacation.patch
# remove version information from sendmail helpfile
Patch15: sendmail-8.14.9-noversion.patch
# do not accept localhost.localdomain as valid address from SMTP
Patch16: sendmail-8.15.2-localdomain.patch
# build libmilter as DSO
Patch17: sendmail-8.14.3-sharedmilter.patch
# skip colon separator when parsing service name in ServiceSwitchFile
Patch18: sendmail-8.15.2-switchfile.patch
# silence warning about missing sasl2 config in /usr/lib*, now in /etc/sasl2
Patch23: sendmail-8.14.8-sasl2-in-etc.patch
# add QoS support, patch from Philip Prindeville <philipp@fedoraproject.org>
# upstream reserved option ID 0xe7 for testing of this new feature, #576643
Patch25: sendmail-8.15.2-qos.patch
Patch26: sendmail-8.15.2-libmilter-socket-activation.patch
# patch provided by upstream
Patch27: sendmail-8.15.2-smtp-session-reuse-fix.patch
Patch28: sendmail-8.15.2-openssl-1.1.0-fix.patch
# patch taken from Debian
# https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=807258
Patch29: sendmail-8.15.2-format-security.patch
# rhbz#1473971
Patch30: sendmail-8.15.2-openssl-1.1.0-ecdhe-fix.patch
# rhbz#1736650
Patch31: sendmail-8.15.2-gethostbyname2.patch
# upstream patch:
Patch32: sendmail-8.15.2-fix-covscan-issues.patch
# sent upstream
Patch33: sendmail-8.15.2-gcc-10-fix.patch

BuildRequires: libdb-devel
BuildRequires: libnsl2-devel
BuildRequires: groff
BuildRequires: m4
BuildRequires: systemd
BuildRequires: gcc
Provides: MTA smtpdaemon server(smtp)
Requires(post): systemd coreutils %{_sbindir}/alternatives %{_bindir}/openssl
Requires(preun): systemd %{_sbindir}/alternatives
Requires(postun): systemd coreutils %{_sbindir}/alternatives
Requires(pre): shadow-utils
Requires: procmail
Requires: bash >= 2.0
%if "%{with_tls}" == "yes"
BuildRequires: openssl-devel
%endif
%if "%{with_sasl2}" == "yes"
BuildRequires: cyrus-sasl-devel openssl-devel
Requires: %{_sbindir}/saslauthd
%endif
%if "%{with_ldap}" == "yes"
BuildRequires: openldap-devel openssl-devel
%endif
# Old NetworkManager expects the dispatcher scripts in a different place
Conflicts: NetworkManager < 1.20


%description
The Sendmail program is a very widely used Mail Transport Agent (MTA).
MTAs send mail from one machine to another. Sendmail is not a client
program, which you use to read your email. Sendmail is a
behind-the-scenes program which actually moves your email over
networks or the Internet to where you want it to go.

If you ever need to reconfigure Sendmail, you will also need to have
the sendmail-cf package installed. If you need documentation on
Sendmail, you can install the sendmail-doc package.

%package doc
Summary: Documentation about the Sendmail Mail Transport Agent program
BuildArch: noarch
Requires: sendmail = %{version}-%{release}

%description doc
This package contains the Sendmail Installation and Operation Guide (PDF),
text files containing configuration documentation, plus a number of
contributed scripts and tools for use with Sendmail.

%package milter-devel
Summary: Development files for the sendmail milter library
Requires: sendmail-milter%{?_isa} = %{version}-%{release}
# The following Provides: and Obsoletes: can be dropped in f28+
Provides: sendmail-devel%{?_isa} = %{version}-%{release}
Provides: sendmail-devel = %{version}-%{release}
Obsoletes: sendmail-devel < 8.15.2-8

%description milter-devel
Include files and devel libraries for the milter add-ons as part of sendmail.

%package cf
Summary: The files needed to reconfigure Sendmail
Requires: sendmail = %{version}-%{release}
BuildArch: noarch
Requires: m4

%description cf
This package includes the configuration files you need to generate the
sendmail.cf file distributed with the sendmail package. You will need
the sendmail-cf package if you ever need to reconfigure and rebuild
your sendmail.cf file.

%package milter
Summary: The sendmail milter library

%description milter
The sendmail Mail Filter API (Milter) is designed to allow third-party
programs access to mail messages as they are being processed in order to
filter meta-information and content.

This package includes the milter shared library.

%prep
%setup -q

%patch 3 -p1 -b .makemapman
%patch 4 -p1 -b .smrsh_paths
%patch 7 -p1 -b .pid
%patch 10 -p1 -b .manpage
%patch 11 -p1 -b .dynamic
%patch 12 -p1 -b .cyrus
%patch 13 -p1 -b .aliases_dir
%patch 14 -p1 -b .vacation
%patch 15 -p1 -b .noversion
%patch 16 -p1 -b .localdomain

cp devtools/M4/UNIX/{,shared}library.m4
%patch 17 -p1 -b .sharedmilter

%patch 18 -p1 -b .switchfile
%patch 23 -p1 -b .sasl2-in-etc
%patch 25 -p1 -b .qos
%patch 26 -p1 -b .libmilter-socket-activation
%patch 27 -p1 -b .smtp-session-reuse-fix
%patch 28 -p1 -b .openssl-1.1.0-fix
%patch 29 -p1 -b .format-security
%patch 30 -p1 -b .openssl-1.1.0-ecdhe-fix
%patch 31 -p1 -b .gethostbyname2
%patch 32 -p1 -b .fix-covscan-issues
%patch 33 -p1 -b .gcc-10-fix

for f in RELEASE_NOTES contrib/etrn.0; do
	iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
		touch -r ${f}{,_} && mv -f ${f}{_,}
done

sed -i 's|/usr/local/bin/perl|%{_bindir}/perl|' contrib/*.pl

%build
# generate redhat config file
cat > redhat.config.m4 << EOF
define(\`confMAPDEF', \`-DNEWDB -DNIS -DMAP_REGEX -DSOCKETMAP -DNAMED_BIND=1')
define(\`confOPTIMIZE', \`\`\`\`${RPM_OPT_FLAGS}'''')
define(\`confENVDEF', \`-I%{_includedir}/libdb -I%{_prefix}/kerberos/include -Wall -DXDEBUG=0 -DNETINET6 -DHES_GETMAILHOST -DUSE_VENDOR_CF_PATH=1 -D_FFR_LINUX_MHNL -D_FFR_QOS -D_FILE_OFFSET_BITS=64 -DHAS_GETHOSTBYNAME2')
define(\`confLIBDIRS', \`-L%{_prefix}/kerberos/%{_lib}')
define(\`confLIBS', \`-lnsl -lcrypt -ldb -lresolv')
%{?_hardened_build:define(\`confLDOPTS', \`-Xlinker -z -Xlinker relro -Xlinker -z -Xlinker now')}
define(\`confMANOWN', \`root')
define(\`confMANGRP', \`root')
define(\`confMANMODE', \`644')
define(\`confMAN1SRC', \`1')
define(\`confMAN5SRC', \`5')
define(\`confMAN8SRC', \`8')
define(\`confSTDIR', \`%{stdir}')
define(\`STATUS_FILE', \`%{stdir}/statistics')
define(\`confLIBSEARCH', \`db resolv 44bsd')
EOF
#'

cat >> redhat.config.m4 << EOF
%ifarch ppc %{power64} s390x
APPENDDEF(\`confOPTIMIZE', \`-DSM_CONF_SHM=0')
%else
APPENDDEF(\`confOPTIMIZE', \`')
%endif
EOF

%if "%{enable_pie}" == "yes"
%ifarch s390 s390x sparc sparcv9 sparc64
%global _fpie -fPIE
%else
%global _fpie -fpie
%endif
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confOPTIMIZE', \`%{_fpie}')
APPENDDEF(\`confLIBS', \`-pie')
EOF
%endif

%if "%{with_tls}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DSTARTTLS -D_FFR_TLS_1 -D_FFR_TLS_EC -D_FFR_TLS_USE_CERTIFICATE_CHAIN_FILE')dnl
APPENDDEF(\`conf_sendmail_LIBS', \`-lssl -lcrypto')dnl
EOF
%endif

%if "%{with_sasl2}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confENVDEF', \`-DSASL=2')dnl
APPENDDEF(\`confLIBS', \`-lsasl2 -lcrypto')dnl
EOF
%endif

%if "%{with_milter}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`conf_sendmail_ENVDEF', \`-DMILTER')dnl
APPENDDEF(\`confENVDEF', \`-D_FFR_MILTER_CHECK_REJECTIONS_TOO')dnl
EOF
%endif

%if "%{with_ldap}" == "yes"
cat >> redhat.config.m4 << EOF
APPENDDEF(\`confMAPDEF', \`-DLDAPMAP -DLDAP_DEPRECATED')dnl
APPENDDEF(\`confENVDEF', \`-DSM_CONF_LDAP_MEMFREE=1')dnl
APPENDDEF(\`confLIBS', \`-lldap -llber -lssl -lcrypto')dnl
EOF
%endif

DIRS="libsmutil sendmail mailstats rmail praliases smrsh makemap editmap"

%if "%{with_milter}" == "yes"
DIRS="libmilter $DIRS"
%endif

for i in $DIRS; do
	pushd $i
	sh Build -f ../redhat.config.m4
	popd
done

%install
# create directories
for d in %{_bindir} %{_sbindir} %{_includedir}/libmilter \
	%{_libdir} %{_mandir}/man{1,5,8} %{maildir} %{stdir} %{spooldir} \
	%{_docdir}/sendmail %{sendmailcf} %{_sysconfdir}/smrsh\
	%{spooldir}/clientmqueue %{_sysconfdir}/sysconfig %{_initrddir} \
	%{_sysconfdir}/pam.d %{_docdir}/sendmail/contrib \
	%{_prefix}/lib/NetworkManager/dispatcher.d
do
	install -m 755 -d %{buildroot}$d
done
install -m 700 -d %{buildroot}%{spooldir}/mqueue

# create /usr/lib for 64 bit architectures
%if "%{_libdir}" != "%{_prefix}/lib"
install -m 755 -d %{buildroot}%{_prefix}/lib
%endif

nameuser=`id -nu`
namegroup=`id -ng`

Make() {
	make $@ \
		DESTDIR=%{buildroot} \
		LIBDIR=%{_libdir} \
		MANROOT=%{_mandir}/man \
		LIBMODE=0755 INCMODE=0644 \
		SBINOWN=${nameuser} SBINGRP=${namegroup} \
		UBINOWN=${nameuser} UBINGRP=${namegroup} \
		MANOWN=${nameuser} MANGRP=${namegroup} \
		INCOWN=${nameuser} INCGRP=${namegroup} \
		LIBOWN=${nameuser} LIBGRP=${namegroup} \
		GBINOWN=${nameuser} GBINGRP=${namegroup} \
		CFOWN=${nameuser} CFGRP=${namegroup} \
		CFMODE=0644 MSPQOWN=${nameuser}
}

OBJDIR=obj.$(uname -s).$(uname -r).$(uname -m)

Make install -C $OBJDIR/libmilter
Make install -C $OBJDIR/sendmail
Make install -C $OBJDIR/mailstats
Make force-install -C $OBJDIR/rmail
Make install -C $OBJDIR/praliases
Make install -C $OBJDIR/smrsh
Make install -C $OBJDIR/makemap
Make install -C $OBJDIR/editmap

# replace absolute with relative symlinks
ln -sf ../sbin/makemap %{buildroot}%{_bindir}/makemap
for f in hoststat mailq newaliases purgestat ; do
	ln -sf ../sbin/sendmail.sendmail %{buildroot}%{_bindir}/${f}
done

# use /usr/lib, even for 64 bit architectures
ln -sf ../sbin/sendmail.sendmail %{buildroot}%{_prefix}/lib/sendmail.sendmail

# install docs for sendmail
install -p -m 644 FAQ %{buildroot}%{_docdir}/sendmail
install -p -m 644 KNOWNBUGS %{buildroot}%{_docdir}/sendmail
install -p -m 644 LICENSE %{buildroot}%{_docdir}/sendmail
install -p -m 644 README %{buildroot}%{_docdir}/sendmail
install -p -m 644 RELEASE_NOTES %{buildroot}%{_docdir}/sendmail
gzip -9 %{buildroot}%{_docdir}/sendmail/RELEASE_NOTES

# install docs for sendmail-doc
install -p -m 644 sendmail/README %{buildroot}%{_docdir}/sendmail/README.sendmail
install -p -m 644 sendmail/SECURITY %{buildroot}%{_docdir}/sendmail
install -p -m 644 smrsh/README %{buildroot}%{_docdir}/sendmail/README.smrsh
install -p -m 644 libmilter/README %{buildroot}%{_docdir}/sendmail/README.libmilter
install -p -m 644 cf/README %{buildroot}%{_docdir}/sendmail/README.cf
install -p -m 644 contrib/* %{buildroot}%{_docdir}/sendmail/contrib

# install the cf files for the sendmail-cf package.
cp -ar cf/* %{buildroot}%{sendmailcf}
# remove patch backup files
rm -rf %{buildroot}%{sendmailcf}/cf/Build.*
rm -rf %{buildroot}%{sendmailcf}/*/*.mc.*
rm -rf %{buildroot}%{sendmailcf}/*/*.m4.*
# remove cf/README file because it is useless for end users
rm -f %{buildroot}%{sendmailcf}/cf/README

# install sendmail.mc with proper paths
install -m 644 %{SOURCE6} %{buildroot}%{maildir}/sendmail.mc
sed -i -e 's|@@PATH@@|%{sendmailcf}|' %{buildroot}%{maildir}/sendmail.mc
touch -r %{SOURCE6} %{buildroot}%{maildir}/sendmail.mc

# create sendmail.cf
cp %{buildroot}%{maildir}/sendmail.mc cf/cf/redhat.mc
sed -i -e 's|%{sendmailcf}|\.\.|' cf/cf/redhat.mc
%if "%{stdir}" != "%{maildir}"
sed -i -e 's:%{maildir}/statistics:%{stdir}/statistics:' cf/cf/redhat.mc
%endif
(cd cf/cf && m4 redhat.mc > redhat.cf)
install -m 644 cf/cf/redhat.cf %{buildroot}%{maildir}/sendmail.cf
install -p -m 644 cf/cf/submit.mc %{buildroot}%{maildir}/submit.mc

# remove our build info as it causes multiarch conflicts
sed -i '/##### built by.*on/,+3d' %{buildroot}%{maildir}/{submit,sendmail}.cf \
	%{buildroot}%{sendmailcf}/cf/submit.cf

install -p -m 644 %{SOURCE12} %{buildroot}%{maildir}/access
install -p -m 644 %{SOURCE13} %{buildroot}%{maildir}/domaintable
install -p -m 644 %{SOURCE14} %{buildroot}%{maildir}/local-host-names
install -p -m 644 %{SOURCE15} %{buildroot}%{maildir}/mailertable
install -p -m 644 %{SOURCE16} %{buildroot}%{maildir}/trusted-users
install -p -m 644 %{SOURCE17} %{buildroot}%{maildir}/virtusertable

# create db ghosts
for map in virtusertable access domaintable mailertable ; do
	touch %{buildroot}%{maildir}/${map}.db
	chmod 0644 %{buildroot}%{maildir}/${map}.db
done

touch %{buildroot}%{maildir}/aliasesdb-stamp

touch %{buildroot}%{spooldir}/clientmqueue/sm-client.st

install -p -m 644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/sendmail
install -p -m 755 %{SOURCE2} %{buildroot}%{_prefix}/lib/NetworkManager/dispatcher.d/10-sendmail
install -p -m 755 %{SOURCE3} %{buildroot}%{maildir}/make
install -p -m 644 %{SOURCE5} %{buildroot}%{maildir}/Makefile

chmod 644 %{buildroot}%{maildir}/helpfile

# Systemd
mkdir -p %{buildroot}%{_unitdir}
install -m644 %{SOURCE1} %{buildroot}%{_unitdir}
install -m644 %{SOURCE7} %{buildroot}%{_unitdir}

# fix permissions to allow debuginfo extraction and stripping
chmod 755 %{buildroot}%{_sbindir}/{mailstats,makemap,editmap,praliases,sendmail,smrsh}
chmod 755 %{buildroot}%{_bindir}/rmail

%if "%{with_sasl2}" == "yes"
install -m 755 -d %{buildroot}%{_sysconfdir}/sasl2
install -m 644 %{SOURCE11} %{buildroot}%{_sysconfdir}/sasl2/Sendmail.conf
%endif
install -m 644 %{SOURCE8} %{buildroot}%{_sysconfdir}/pam.d/smtp.sendmail

# fix path for statistics file in man pages
%if "%{stdir}" != "%{maildir}"
sed -i -e 's:%{maildir}/statistics:%{stdir}/statistics:' %{buildroot}%{_mandir}/man*/*
%endif

# rename files for alternative usage
mv %{buildroot}%{_sbindir}/sendmail %{buildroot}%{_sbindir}/sendmail.sendmail
touch %{buildroot}%{_sbindir}/sendmail
mv %{buildroot}%{_sbindir}/makemap %{buildroot}%{_sbindir}/makemap.sendmail
touch %{buildroot}%{_sbindir}/makemap
mv %{buildroot}%{_sbindir}/editmap %{buildroot}%{_sbindir}/editmap.sendmail
touch %{buildroot}%{_sbindir}/editmap
for i in mailq newaliases rmail; do
	mv %{buildroot}%{_bindir}/$i %{buildroot}%{_bindir}/$i.sendmail
	touch %{buildroot}%{_bindir}/$i
done
mv %{buildroot}%{_mandir}/man1/mailq.1 %{buildroot}%{_mandir}/man1/mailq.sendmail.1
touch %{buildroot}%{_mandir}/man1/mailq.1
mv %{buildroot}%{_mandir}/man1/newaliases.1 %{buildroot}%{_mandir}/man1/newaliases.sendmail.1
touch %{buildroot}%{_mandir}/man1/newaliases.1
mv %{buildroot}%{_mandir}/man5/aliases.5 %{buildroot}%{_mandir}/man5/aliases.sendmail.5
touch %{buildroot}%{_mandir}/man5/aliases.5
mv %{buildroot}%{_mandir}/man8/sendmail.8 %{buildroot}%{_mandir}/man8/sendmail.sendmail.8
touch %{buildroot}%{_mandir}/man8/sendmail.8
mv %{buildroot}%{_mandir}/man8/rmail.8 %{buildroot}%{_mandir}/man8/rmail.sendmail.8
touch %{buildroot}%{_mandir}/man8/rmail.8
mv %{buildroot}%{_mandir}/man8/makemap.8 %{buildroot}%{_mandir}/man8/makemap.sendmail.8
touch %{buildroot}%{_mandir}/man8/makemap.8
mv %{buildroot}%{_mandir}/man8/editmap.8 %{buildroot}%{_mandir}/man8/editmap.sendmail.8
touch %{buildroot}%{_mandir}/man8/editmap.8
touch %{buildroot}%{_prefix}/lib/sendmail
touch %{buildroot}%{_sysconfdir}/pam.d/smtp

# create stub man pages
for m in man8/hoststat.8 man8/purgestat.8; do
	[ -f %{buildroot}%{_mandir}/$m ] || 
		echo ".so man8/sendmail.8" > %{buildroot}%{_mandir}/$m
done

%pre
getent group mailnull >/dev/null || \
  %{_sbindir}/groupadd -g 47 -r mailnull >/dev/null 2>&1
getent passwd mailnull >/dev/null || \
  %{_sbindir}/useradd -u 47 -g mailnull -d %{spooldir}/mqueue -r \
  -s %{smshell} mailnull >/dev/null 2>&1
getent group smmsp >/dev/null || \
  %{_sbindir}/groupadd -g 51 -r smmsp >/dev/null 2>&1
getent passwd smmsp >/dev/null || \
  %{_sbindir}/useradd -u 51 -g smmsp -d %{spooldir}/mqueue -r \
  -s %{smshell} smmsp >/dev/null 2>&1

# hack to turn sbin/makemap and man8/makemap.8.gz into alternatives symlink
# (part of the rhbz#1219178 fix), this could be probably dropped in f25+
[ -h %{_sbindir}/makemap ] || rm -f %{_sbindir}/makemap || :
[ -h %{_mandir}/man8/makemap.8.gz ] || rm -f %{_mandir}/man8/makemap.8.gz || :

exit 0

%postun
%systemd_postun_with_restart sendmail.service sm-client.service
if [ $1 -ge 1 ] ; then
	mta=`readlink %{_sysconfdir}/alternatives/mta`
	if [ "$mta" == "%{_sbindir}/sendmail.sendmail" ]; then
		%{_sbindir}/alternatives --set mta %{_sbindir}/sendmail.sendmail
	fi
fi
exit 0

%post
%systemd_post sendmail.service sm-client.service

# Set up the alternatives files for MTAs.
%{_sbindir}/alternatives --install %{_sbindir}/sendmail mta %{_sbindir}/sendmail.sendmail 90 \
	--slave %{_sbindir}/makemap mta-makemap %{_sbindir}/makemap.sendmail \
	--slave %{_sbindir}/editmap mta-editmap %{_sbindir}/editmap.sendmail \
	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.sendmail \
	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.sendmail \
	--slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.sendmail \
	--slave %{_prefix}/lib/sendmail mta-sendmail %{_prefix}/lib/sendmail.sendmail \
	--slave %{_sysconfdir}/pam.d/smtp mta-pam %{_sysconfdir}/pam.d/smtp.sendmail \
	--slave %{_mandir}/man8/sendmail.8.gz mta-sendmailman %{_mandir}/man8/sendmail.sendmail.8.gz \
	--slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man1/mailq.sendmail.1.gz \
	--slave %{_mandir}/man1/newaliases.1.gz mta-newaliasesman %{_mandir}/man1/newaliases.sendmail.1.gz \
	--slave %{_mandir}/man5/aliases.5.gz mta-aliasesman %{_mandir}/man5/aliases.sendmail.5.gz \
	--slave %{_mandir}/man8/rmail.8.gz mta-rmailman %{_mandir}/man8/rmail.sendmail.8.gz \
	--slave %{_mandir}/man8/makemap.8.gz mta-makemapman %{_mandir}/man8/makemap.sendmail.8.gz \
	--slave %{_mandir}/man8/editmap.8.gz mta-editmapman %{_mandir}/man8/editmap.sendmail.8.gz \
	--initscript sendmail > /dev/null 2>&1

# Rebuild maps.
{
	chown root %{_sysconfdir}/aliases.db %{maildir}/access.db \
		%{maildir}/mailertable.db %{maildir}/domaintable.db \
		%{maildir}/virtusertable.db
	SM_FORCE_DBREBUILD=1 %{maildir}/make
	SM_FORCE_DBREBUILD=1 %{maildir}/make aliases
} > /dev/null 2>&1

# Move existing SASL2 config to new location.
%if "%{with_sasl2}" == "yes"
[ -f %{_libdir}/sasl2/Sendmail.conf ] && touch -r %{_sysconfdir}/sasl2/Sendmail.conf \
  %{_libdir}/sasl2/Sendmail.conf ] && mv -f %{_libdir}/sasl2/Sendmail.conf \
  %{_sysconfdir}/sasl2 2>/dev/null || :
%endif

# Create sm-client.st if it doesn't exist
if [ ! -f %{spooldir}/clientmqueue/sm-client.st ]; then
	touch %{spooldir}/clientmqueue/sm-client.st
	chown smmsp:smmsp %{spooldir}/clientmqueue/sm-client.st
	chmod 0660 %{spooldir}/clientmqueue/sm-client.st
fi

# Create self-signed SSL certificate
if [ ! -f %{sslkey} ]; then
  umask 077
  %{_bindir}/openssl genrsa 4096 > %{sslkey} 2> /dev/null
fi

if [ ! -f %{sslcert} ]; then
  FQDN=`hostname`
  if [ "x${FQDN}" = "x" ]; then
    FQDN=localhost.localdomain
  fi

  %{_bindir}/openssl req -new -key %{sslkey} -x509 -sha256 -days 365 -set_serial $RANDOM -out %{sslcert} \
    -subj "/C=--/ST=SomeState/L=SomeCity/O=SomeOrganization/OU=SomeOrganizationalUnit/CN=${FQDN}/emailAddress=root@${FQDN}"
  chmod 600 %{sslcert}
fi

exit 0

%preun
%systemd_preun sendmail.service sm-client.service
if [ $1 = 0 ]; then
	%{_sbindir}/alternatives --remove mta %{_sbindir}/sendmail.sendmail
fi
exit 0

%ldconfig_scriptlets milter


%files
%dir %{_docdir}/sendmail
%doc %{_docdir}/sendmail/FAQ
%doc %{_docdir}/sendmail/KNOWNBUGS
%doc %{_docdir}/sendmail/LICENSE
%doc %{_docdir}/sendmail/README
%doc %{_docdir}/sendmail/RELEASE_NOTES.gz
%{_bindir}/hoststat
%{_bindir}/makemap
%{_bindir}/purgestat
%{_sbindir}/mailstats
%{_sbindir}/makemap.sendmail
%{_sbindir}/editmap.sendmail
%{_sbindir}/praliases
%attr(2755,root,smmsp) %{_sbindir}/sendmail.sendmail
%{_bindir}/rmail.sendmail
%{_bindir}/newaliases.sendmail
%{_bindir}/mailq.sendmail
%{_sbindir}/smrsh
%{_prefix}/lib/sendmail.sendmail

%{_mandir}/man8/rmail.sendmail.8.gz
%{_mandir}/man8/praliases.8.gz
%{_mandir}/man8/mailstats.8.gz
%{_mandir}/man8/makemap.sendmail.8.gz
%{_mandir}/man8/editmap.sendmail.8.gz
%{_mandir}/man8/sendmail.sendmail.8.gz
%{_mandir}/man8/smrsh.8.gz
%{_mandir}/man8/hoststat.8.gz
%{_mandir}/man8/purgestat.8.gz
%{_mandir}/man5/aliases.sendmail.5.gz
%{_mandir}/man1/newaliases.sendmail.1.gz
%{_mandir}/man1/mailq.sendmail.1.gz

# dummy attributes for rpmlint
%ghost %attr(0755,-,-) %{_sbindir}/sendmail
%ghost %attr(0755,-,-) %{_sbindir}/makemap
%ghost %attr(0755,-,-) %{_sbindir}/editmap
%ghost %attr(0755,-,-) %{_bindir}/mailq
%ghost %attr(0755,-,-) %{_bindir}/newaliases
%ghost %attr(0755,-,-) %{_bindir}/rmail
%ghost %attr(0755,-,-) %{_prefix}/lib/sendmail

%ghost %{_sysconfdir}/pam.d/smtp
%ghost %{_mandir}/man8/sendmail.8.gz
%ghost %{_mandir}/man1/mailq.1.gz
%ghost %{_mandir}/man1/newaliases.1.gz
%ghost %{_mandir}/man5/aliases.5.gz
%ghost %{_mandir}/man8/rmail.8.gz
%ghost %{_mandir}/man8/makemap.8.gz
%ghost %{_mandir}/man8/editmap.8.gz

%dir %{stdir}
%dir %{_sysconfdir}/smrsh
%dir %{maildir}
%attr(0770,smmsp,smmsp) %dir %{spooldir}/clientmqueue
%attr(0700,root,mail) %dir %{spooldir}/mqueue

%config(noreplace) %verify(not size mtime md5) %{stdir}/statistics
%config(noreplace) %{maildir}/Makefile
%config(noreplace) %{maildir}/make
%config(noreplace) %{maildir}/sendmail.cf
%config(noreplace) %{maildir}/submit.cf
%config(noreplace) %{maildir}/helpfile
%config(noreplace) %{maildir}/sendmail.mc
%config(noreplace) %{maildir}/submit.mc
%config(noreplace) %{maildir}/access
%config(noreplace) %{maildir}/domaintable
%config(noreplace) %{maildir}/local-host-names
%config(noreplace) %{maildir}/mailertable
%config(noreplace) %{maildir}/trusted-users
%config(noreplace) %{maildir}/virtusertable

%ghost %{maildir}/aliasesdb-stamp
%ghost %{maildir}/virtusertable.db
%ghost %{maildir}/access.db
%ghost %{maildir}/domaintable.db
%ghost %{maildir}/mailertable.db

%ghost %{spooldir}/clientmqueue/sm-client.st

%{_unitdir}/sendmail.service
%{_unitdir}/sm-client.service
%config(noreplace) %{_sysconfdir}/sysconfig/sendmail
%config(noreplace) %{_sysconfdir}/pam.d/smtp.sendmail
%{_prefix}/lib/NetworkManager

%if "%{with_sasl2}" == "yes"
%config(noreplace) %{_sysconfdir}/sasl2/Sendmail.conf
%endif

%files cf
%doc %{sendmailcf}/README
%dir %{sendmailcf}
%{sendmailcf}/cf
%{sendmailcf}/domain
%{sendmailcf}/feature
%{sendmailcf}/hack
%{sendmailcf}/m4
%{sendmailcf}/mailer
%{sendmailcf}/ostype
%{sendmailcf}/sendmail.schema
%{sendmailcf}/sh
%{sendmailcf}/siteconfig

%files milter-devel
%doc libmilter/docs/*
%dir %{_includedir}/libmilter
%{_includedir}/libmilter/*.h
%{_libdir}/libmilter.so

%files milter
%doc LICENSE
%doc %{_docdir}/sendmail/README.libmilter
%{_libdir}/libmilter.so.[0-9].[0-9]
%{_libdir}/libmilter.so.[0-9].[0-9].[0-9]

%files doc
%{_docdir}/sendmail/README.cf
%{_docdir}/sendmail/README.sendmail
%{_docdir}/sendmail/README.smrsh
%{_docdir}/sendmail/SECURITY
%dir %{_docdir}/sendmail/contrib
%attr(0644,root,root) %{_docdir}/sendmail/contrib/*


%changelog
* Fri Feb 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.15.2-46
- Removing dependency on 'ghostscript'.
- License verified.

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 8.15.2-45
- Making binaries paths compatible with CBL-Mariner's paths.

* Mon Mar 29 2021 Henry Li <lihl@microsoft.com> - 8.15.2-44
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Remove setup from dependency 

* Mon Feb 10 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-43
- Fixed FTBFS with gcc-10
  Resolves: rhbz#1800082
- De-fuzzified fix-covscan-issues patch

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-42
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 04 2019 Ondřej Lysoněk <olysonek@redhat.com> - 8.15.2-41
- Fix issues discovered by Coverity scan

* Thu Aug 22 2019 Lubomir Rintel <lkundrak@v3.sk> - 8.15.2-40
- Move the NetworkManager dispatcher script out of /etc

* Fri Aug  2 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-39
- Used gethostbyname2 instead of gethostbyname to fix FTBFS caused by
  glibc update dropping support for obsolete RES_USE_INET6
  Resolves: rhbz#1736650

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 8.15.2-36
- Rebuilt for libcrypt.so.2 (#1666033)

* Mon Nov 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-35
- Used _prefix macro for more hardcoded /usr directories

* Mon Nov 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-34
- Used _prefix macro for /usr

* Mon Oct 29 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-33
- Dropped hesiod support
  Resolves: rhbz#1643264

* Tue Oct 16 2018 Peter Robinson <pbrobinson@fedoraproject.org> 8.15.2-32
- Drop old pre F-23 conditionals, minor spec cleanups

* Wed Aug 29 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-31
- Added support for sendmail service reload
  Resolves: rhbz#1618552

* Mon Aug 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-30
- Fixed sendmail.pem unsafe: Group readable file

* Mon Jul 23 2018 Robert Scheck <robert@fedoraproject.org> - 8.15.2-29
- Add basic sendmail TLS configuration by default (#1607314 #c11)

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Robert Scheck <robert@fedoraproject.org> - 8.15.2-27
- Use SSL_CTX_use_certificate_chain_file() to handle intermediate
  certificates passed additionally in confSERVER_CERT (#1565341)

* Tue May 29 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-26
- Changed libnsl2 paths
  Resolves: rhbz#1543933

* Wed Mar 07 2018 Adam Williamson <awilliam@redhat.com> - 8.15.2-25
- Rebuild to fix GCC 8 mis-compilation
  See https://da.gd/YJVwk ("GCC 8 ABI change on x86_64")

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 8.15.2-24
- Add gcc to BuildRequires

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sun Jan 21 2018 Björn Esser <besser82@fedoraproject.org> - 8.15.2-22
- Explicitly BR: libnsl2-devel and add needed paths in build config

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 8.15.2-21
- Rebuilt for switch to libxcrypt

* Thu Nov 30 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-20
- Dropped tcp_wrappers support
  Resolves: rhbz#1518782

* Fri Aug 18 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-19
- Replaced compile-fix patch by format-security patch from Debian not to
  change status codes
  Resolves: rhbz#1482808

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Sun Jul 30 2017 Florian Weimer <fweimer@redhat.com> - 8.15.2-17
- Rebuild with binutils fix for ppc64le (#1475636)

* Thu Jul 27 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-16
- Fixed ECDHE to work with all curves (openssl-1.1.0-ecdhe-fix patch)
  Resolves: rhbz#1473971

* Thu Mar 23 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-15
- Explicitly enabled sm-client statistics
  Related: rhbz#890585
- Fixed compilation with -Werror=format-security which seems to be the
  default in f27+

* Thu Feb 23 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-14
- Also removed the systemd restart limit from the sm-client service
  Related: rhbz#1422771

* Tue Feb 21 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-13
- Removed systemd limit for sendmail restarts to workaround failure due to
  rapid restarts caused by NetworkManager dispatcher script
  Resolves: rhbz#1422771

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  8 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-11
- Added SASL AUTH_REALM into default configuration
  Resolves: rhbz#748279
- Fixed compilation with openssl-1.1.0
  Resolves: rhbz#1400239

* Wed Nov 30 2016 Ondřej Lysoněk <olysonek@redhat.com> - 8.15.2-10
- Enabled _FFR_MILTER_CHECK_REJECTIONS_TOO
  Resolves: rhbz#1112340

* Mon Aug 08 2016 Ondřej Lysoněk <olysonek@redhat.com> - 8.15.2-9
- Fixed Provides and Obsoletes in sendmail-milter-devel
- Made 'Requires: sendmail-milter' in sendmail-milter-devel arch specific

* Thu Jul 28 2016 Ondřej Lysoněk <olysonek@redhat.com> - 8.15.2-8
- Removed dependency for sendmail in sendmail-devel, renamed sendmail-devel
  to sendmail-milter-devel
  Resolves: rhbz#891288

* Fri Jun  3 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-7
- Enabled editmap
  Resolves: rhbz#1342393

* Tue Mar  1 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-6
- Fixed SMTP session reuse bug

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Sep 23 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-4
- Compiled all with full RELRO, including libmilter
  Resolves: rhbz#1264035

* Wed Sep 23 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-3
- Added support for socket activation to libmilter
  Resolves: rhbz#1262535

* Wed Jul 22 2015 Lubomir Rintel <lkundrak@v3.sk> - 8.15.2-2
- nm-dispacher: don't block the connection activation
  Resolves: rhbz#1237070

* Tue Jul  7 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.2-1
- New version
  Resolves: rhbz#1239185
- Dropped ipv6-bad-helo patch (upstreamed)
- Updated/defuzzified patches

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.15.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed May 27 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.1-5
- Added makemap and its manual page into alternatives
  Resolves: rhbz#1219178

* Fri Mar 20 2015 Robert Scheck <robert@fedoraproject.org> - 8.15.1-4
- Use uncompressed (new) IPv6 address format in block_bad_helo.m4

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 8.15.1-3
- Drop sysvinit subpackage from F23+

* Thu Feb 26 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.1-2
- Removed code for transition from sysv init to systemd (deprecated)

* Mon Dec  8 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 8.15.1-1
- New version
- Dropped hesiod patch (not needed)
- Dropped libdb5 patch (upstreamed)
- Rebased patches

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 8.14.9-5
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.9-2
- Dropped milterfdleaks patch (not needed)

* Wed May 21 2014 Robert Scheck <robert@fedoraproject.org> - 8.14.9-1
- Upgrade to 8.14.9

* Sun Apr 13 2014 Robert Scheck <robert@fedoraproject.org> - 8.14.8-2
- Enable ECDHE support

* Tue Feb 11 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.8-1
- New version
  Resolves: rhbz#1059665
- Updated/defuzzified patches

* Tue Aug  6 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.7-5
- Used unversioned doc directory
  Resolves: rhbz#994090

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 8.14.7-4
- Perl 5.18 rebuild

* Fri Aug  2 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.7-3
- Rebuilt with -D_FILE_OFFSET_BITS=64
  Related: rhbz#912785

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 8.14.7-2
- Perl 5.18 rebuild

* Sun Apr 21 2013 Robert Scheck <robert@fedoraproject.org> - 8.14.7-1
- Upgrade to 8.14.7

* Mon Feb 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.6-4
- Switched to systemd-rpm macros
  Resolves: rhbz#850310

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.6-2
- Fixed milter_helo regression (milter-helo-fix patch)
  Resolves: rhbz#895552
- Fixed bogus dates in changelog

* Mon Dec 24 2012 Robert Scheck <robert@fedoraproject.org> - 8.14.6-1
- Upgrade to 8.14.6

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-14
- Used power64 macro to support more subarchitectures like ppc64p7
  Resolves: rhbz#834626

* Fri Apr  6 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-13
- Rebuilt with libdb-5.2

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-11
- Added tighter bound to sm-client.service and sendmail.service
  Resolves: rhbz#756232

* Mon Oct 24 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-10
- The nm-dispatcher now uses try-restart instead of restart
  Resolves: rhbz#748416

* Tue Sep 13 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-9
- Enabled alternatives --initscript in post section
- Improved sysvinit subpackage - switched to noarch, added scriptlets
- Workarounded sm-client stop on SysV to systemd migration

* Tue Aug 30 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-8
- Enable override of hardened build settings

* Tue Aug 30 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-7
- Hardened build with full relro
- Provided SysV initscript in sysvinit subpackage for backward compatibility

* Mon Jul 25 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-6
- Fixed systemctl disable command in preun section
- Replaced reload by restart, dropped ExecReload from sendmail.service
  Resolves: rhbz#719931
- Switched to systemctl in NetworkManager dispatcher script
- Added ExecStartPre=-/etc/mail/make to sm-client.service
- Hardcoded daemon option (-bd) to sendmail.service, dropped the DAEMON var
- QUEUE var in /etc/sysconfig/sendmail replaced by SENDMAIL_OPTS var
- Added default preset (-q1h) to SENDMAIL_OPTS var

* Fri Jul 22 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-5
- Fixed SMTP AUTH over TLS in case of two AUTH lines
  Resolves: rhbz#716628

* Mon Jul 18 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-4
- Removed dots from description (there are no dots in systemd packaging
  guidelines)
- Changed service type to forking and explicitly specified PID files
- Fixed creation of sm-client.pid
- Added Wants to sm-client.service and sendmail.service
- Replaced each occurrence of /var/run by /run in config files
- More details are available in rhbz#697636

* Thu Jun 30 2011 Jóhann B. Guðmundsson <johannbg@gmail.com> - 8.14.5-3
- Introduce systemd unit file, drop SysV support

* Thu Jun 16 2011 Paul Howarth <paul@city-fan.org> - 8.14.5-2
- Rebuilt with libdb-5.2

* Tue May 17 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.5-1
- New version 8.14.5
- Removed m4-ldap-routing, milter-fix-negativeid, man-i-option-fix
  patches (upstreamed)

* Thu Mar 03 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-21
- fix negative ctx_id in milter debug output (#577558)
- fix incomplete description of the -i option in man page (#676824)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-19
- updated QoS patch, including upstream comments and AF_INET6 4-in-6 support

* Mon Jan 10 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-18
- add QoS support, patch from Philip Prindeville <philipp@fedoraproject.org>
  upstream reserved option ID 0xe7 for testing of this new feature (#576643)

* Fri Nov 26 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-17
- change LSB init header to provide $mail-transport-agent (#627413)

* Mon Nov 08 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-16
- fix m4 ldap routing macro, backport from 8.14.5.Alpha0, (#650366)

* Wed Sep 29 2010 jkeating - 8.14.4-15
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-14
- fix MAXHOSTNAMELEN (#485380)

* Mon Sep 13 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-13
- rebuilt with libdb-5.1

* Wed Aug 25 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-12
- updated sendmail.nm-dispatcher script to handle VPN connections (#577540)

* Tue Aug 17 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-11
- README.libmilter moved to milter subpackage
- updated description of doc subpackage
- README.redhat removed (not needed any more)

* Wed Aug 04 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-10
- added stub man pages for hoststat and purgestat
- rmail man page added to alternatives
- updated subpackages description
- sendmail-cf/cf/README is not packaged - it is useless for end users
- added comments about purpose of files and patches
- removed redundant license tag from milter subpackage

* Thu Jul 08 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-9
- added license to milter subpackage according to new Licensing
  Guidelines

* Mon Jun 14 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-8
- all 'define' changed to 'global' in spec
- perl interpreter path fixup moved from 'install' to 'prep'

* Fri Jun 11 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-7
- silenced warning about non-existing config in {_libdir}/sasl2

* Tue Jun 08 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-6
- sasl2 config moved from {_libdir}/sasl2 to {_sysconfdir}/sasl2
- added libdb5 patch for building with libdb-5
- rebuilt with libdb-5

* Mon May 31 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-5
- fixed user/group creation

* Tue Mar 02 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-4
- used noreplace for sasl config
- used ghost instead of explicit provides
- deffattr changed to (-,root,root,-)

* Mon Feb 15 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-3
- fixed libresolv implicit DSO linking (#564647)
- fixed initscript LSB compliance (#561040)

* Thu Feb 04 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-2
- fixed typo in spec file
- fixed aliases_dir patch

* Tue Feb 02 2010 Jaroslav Škarvada <jskarvad@redhat.com> - 8.14.4-1
- new version 8.14.4 (#552078)
- RPM attributes S, 5, T not recorded for statistics file
- adapted patches: makemapman, dynamic, switchfile (#552078)
- movefiles patch incorporated into aliases_dir patch
- drop exitpanic patch (fixed upstream)

* Sun Jan 03 2010 Robert Scheck <robert@fedoraproject.org> 8.14.3-10
- handle IPv6:::1 in block_bad_helo.m4 like 127.0.0.1 (#549217)

* Tue Dec 15 2009 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-9
- fix milter file descriptors leaks (#485426)
- skip colon separator when parsing service name in ServiceSwitchFile
- return with non-zero exit code when free space is below MinFreeBlocks
- fix service stop/restart when only smclient is running
- fix submit.cf and helpfile permissions
- more merge review fixes (#226407)

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 8.14.3-8
- Use password-auth common PAM configuration instead of system-auth

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 8.14.3-7
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.14.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Jan 20 2009 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-4
- build shared libmilter (#309281)
- drop static libraries
- convert RELEASE_NOTES to UTF-8

* Fri Dec 19 2008 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-3
- run newaliases only when necessary

* Wed Dec 03 2008 Miroslav Lichvar <mlichvar@redhat.com> 8.14.3-2
- add NM dispatcher script (#451575)
- print warning on service start when sendmail-cf is required (#447148)
- replace Makefile with shell script to avoid dependency on make (#467841)
- fix multiarch conflicts (#343161)
- preserve timestamps on config files
- gzip RELEASE_NOTES
- defuzz patches
- drop gcc2690 patch

* Tue Jul 22 2008 Thomas Woerner <twoerner@redhat.com> 8.14.3-1
- new version 8.14.3

* Thu Jul 10 2008 Tom "spot" Callaway <tcallawa@redhat.com> 8.14.2-5
- rebuild against db4-4.7

* Sat Mar 29 2008 Dennis Gilmore <dennis@ausil.us> 8.14.2-4
- add sparcv9 to the -fPIE list 

* Fri Feb  8 2008 Thomas Woerner <twoerner@redhat.com> 8.14.2-3
- added server(smtp) provide (rhbz#380621)

* Wed Dec 05 2007 Release Engineering <rel-eng at fedoraproject dot org> - 8.14.2-2
 - Rebuild for deps

* Thu Nov 22 2007 Thomas Woerner <twoerner@redhat.com> 8.14.2-1
- new version 8.14.2

* Mon Sep 17 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-4.2
- made init script fully lsb conform

* Wed Aug 29 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-4.1
- fixed condrestart in init script to use exit instead of return

* Mon Aug 27 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-4
- do not remove /etc/aliases.db on package removal (rhbz#223637)
- fixed remaining paths to certs directory in sendmail.mc file
- added contrib scripts to the doc package (rhbz#183723)
- added LSB header to init script (rhbz#247053)
- added plain login information for cyrus-sasl to access file
- fixed compile problem with glibc-2.6.90+
- fixed reoccuring m4 include problem (now using sinclude)

* Fri Jul 20 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-3
- do not accept localhost.localdomain as valid address from smtp

* Mon Apr 16 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-2
- readded chkconfig add for sendmail in post script
- dropped mysql support (useless without further patching)
- fixed executable permissions for /usr/sbin/makemap and /usr/sbin/smrsh
- dropped FFR_UNSAFE_SASL, because it has no effect anymore

* Thu Apr 12 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-1.1
- replaced prereq tags with requires() tags.

* Thu Apr 12 2007 Thomas Woerner <twoerner@redhat.com> 8.14.1-1
- new version 8.14.1
- spec file cleanup for merge review (rhbz#226407)
- dropped update support for sendmail versions prior to 8.12.0
- using pdf documentation

* Tue Feb  6 2007 Thomas Woerner <twoerner@redhat.com> 8.14.0-1
- new version 8.14.0
- adapted patches: makemapman, dynamic

* Tue Jan 23 2007 Florian La Roche <laroche@redhat.com>
- #205803 add sparc/sparc64 to -fPIE list
- change sendmail.cf reference into sendmail-cf package name

* Mon Dec  4 2006 Thomas Woerner <twoerner@redhat.com> 8.13.8-3.1
- tcp_wrappers has a new devel and libs sub package, therefore changing build
  requirement for tcp_wrappers to tcp_wrappers-devel

* Tue Nov 28 2006 Thomas Woerner <twoerner@redhat.com> 8.13.8-3
- added missing LDAP_DEPRECATED flag (#206288)

* Mon Sep 04 2006 Florian La Roche <laroche@redhat.com>
- unify sendmail.mc
- remove version information from sendmail helpfile

* Fri Sep  1 2006 Thomas Woerner <twoerner@redhat.com> 8.13.8-1
- new version 8.13.8 fixes CVE-2006-4434 (denial of service via a long header
  line)

* Thu Jul 20 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-3.1
- dropped chown of /etc/mail/authinfo.db (#199455)

* Tue Jul 18 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-3
- using new syntax for access database (#177566)
- fixed failure message while shutting down sm-client (#119429)
  resolution: stop sm-client before sendmail
- fixed method to specify persistent queue runners (#126760)
- removed patch backup files from sendmail-cf tree (#152955)
- fixed missing dnl on SMART_HOST define (#166680)
- fixed wrong location of aliases and aliases.db file in aliases man page
  (#166744)
- enabled CipherList config option for sendmail (#172352)
- added user chowns for /etc/mail/authinfo.db and move check for cf files
  (#184341)
- fixed Makefile of vacation (#191396)
  vacation is not included in this sendmail package
- /var/log/mail now belongs to sendmail (#192850)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 8.13.7-2.1
- rebuild

* Mon Jun 19 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-2
- dropped reference to Red Hat Linux in sendmail-redhat.mc (#176679)

* Mon Jun 19 2006 Thomas Woerner <twoerner@redhat.com> 8.13.7-1
- new version 8.13.7 (#195282)
- fixes CVE-2006-1173 (VU#146718): possible denial of service issue caused by
  malformed multipart messages (#195776)

* Wed Mar 22 2006 Thomas Woerner <twoerner@redhat.com> 8.13.6-1
- new version 8.13.6 (fixes VU#834865)
- dropped libmilter-sigwait patch (fixed in 8.13.6)

* Fri Feb 17 2006 Thomas Woerner <twoerner@redhat.com> 8.13.5-3
- fixed selinuxenabled path in initscript
- fixed error handling with sigwait (#137709)
  Thanks to Jonathan Kamens for the patch
- fixed prereq for cyrus-sasl: now using /usr/sbin/saslauthd
- appended 'dnl' to cert tags in sendmail.mc

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 8.13.5-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 8.13.5-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 8.13.5-2
- rebuilt against new openssl

* Mon Oct 10 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Mon Sep 19 2005 Thomas Woerner <twoerner@redhat.com> 8.13.5-1
- new version 8.13.5
- fixed email address in changelog

* Fri May  6 2005 Thomas Woerner <twoerner@redhat.com> 8.13.4-2
- using new certificates directory /etc/pki/tls/certs

* Wed Apr 27 2005 Thomas Woerner <twoerrner@redhat.com> 8.13.4-1.1
- added configuration example for Cyrus-IMAPd to sendmail.mc (#142001)
  Thanks to Alexander Dalloz

* Tue Apr 12 2005 Thomas Woerner <twoerner@redhat.com> 8.13.4-1
- new version 8.13.4
- added requires for the sendmail base package in sendmail-cf, sendmail-devel
  and sendmail-doc
- dropped upstream close_wait.p2 patch

* Thu Mar 17 2005 Thomas Woerner <twoerner@redhat.com> 8.13.3-2
- dropped direct support for bind: no bind in confLIBSEARCH anymore,
  using libresolv again

* Thu Mar 10 2005 Jason Vas Dias <jvdias@redhat.com> 8.13.3-1.2
- fix libbind include path - use /usr/include/bind/netdb.h, no
- /usr/include/netdb.h - bug: 150339

* Tue Mar  1 2005 Thomas Woerner <twoerner@redhat.com> 8.13.3-1.1
- fixed gcc4 build: use double quotes for confOPTIMIZE to avoid m4 confusion
  with ','
- fix for ppc: using tripple-quotes

* Wed Jan 26 2005 Thomas Woerner <twoerner@redhat.com> 8.13.3-1
- new version 8.13.3 with closewait.p2 patch

* Fri Dec 17 2004 Thomas Woerner <twoerner@redhat.com> 8.13.2-1
- new version 8.13.2
- thanks to Robert Scheck for adapting the patches

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 8.13.1-2.2
- rebuild against db-4.3.21.

* Tue Oct 26 2004 Thomas Woerner <twoerner@redhat.com> 8.13.1-2.1
- added missing BuildRequires for groff (#134778)
- added socketmap support (#131906)

* Wed Sep  1 2004 Thomas Woerner <twoerner@redhat.com> 8.13.1-2
- applied Sendmail Errata (2004-08-24): errata_cataddr (#131179)

* Mon Aug  2 2004 Thomas Woerner <twoerner@redhat.com> 8.13.1-1
- new version 1.13.1

* Wed Jun 30 2004 Thomas Woerner <twoerner@redhat.com> 8.13.0-1.1
- fixed init script to not complain missing sendmail-cf package (#126975)
- better message in /etc/mail/Makefile for missing sendmail-cf package.

* Mon Jun 21 2004 Thomas Woerner <twoerner@redhat.com> 8.13.0-1
- new version 8.13.0
- made /etc/mail/Makefile complain missing sendmail-cf package (#123348)
- fixed ownership of %%{_includedir}/libmilter (#73977)
- moved back to /usr/share/ssl/certs as certificate directory (see sendmail.mc)
- extended sendmail.mc for spam protection

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Apr  15 2004 Dan Walsh <dwalsh@redhat.com> 8.12.11-4.6
- Fix selinuxenabled location

* Wed Apr  7 2004 Dan Walsh <dwalsh@redhat.com> 8.12.11-4.5
- Fix security context of pid file for selinux

* Fri Apr  2 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.4
- fixed alternatives slave for sendmail.sendmail

* Thu Apr  1 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.3
- set path to cyrus-imapd deliver

* Wed Mar 31 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.2
- fixed spec file

* Wed Mar 31 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4.1
- added authinfo to possible sendmail maps: /etc/mail/Makefile (#119010)
- fixed minor version in changelog

* Wed Mar 17 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-4
- new slave in alternatives for sendmail man page

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 19 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-3.2
- removed buildreq for gdbm-devel

* Thu Feb 19 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-3
- RH3.0E version: sasl1, no pie, old_setup (provide /etc/aliases)
- new switches for pie and old_setup

* Thu Feb  5 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-2.1
- new Sendmail.conf for sasl1 (#114726)

* Wed Jan 28 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-2
- added information for saslauthd and AUTH (#113463)
- fixed STATUS_FILE in sendmail-redhat.mc (#114302)
- reset mta after update if mta was sendmail (#114257)
- enabled pie for ia64 again

* Mon Jan 26 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1.3
- removed /etc/aliases (now in setup)

* Thu Jan 22 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1.2
- /usr/lib/sendmail is in alternatives, now
- removed trailing / from stdir
- fixed define for STATUS_FILE

* Wed Jan 21 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1.1
- disabled pie for ia64

* Tue Jan 20 2004 Thomas Woerner <twoerner@redhat.com> 8.12.11-1
- new version 8.12.11
- pie

* Mon Jan 12 2004 Thomas Woerner <twoerner@redhat.com> 8.12.10-7
- fc2 version (with sasl2)

* Mon Jan 12 2004 Thomas Woerner <twoerner@redhat.com> 8.12.10-6
- reverted to sasl1 for 3.0E: added with_sasl1
- spec file cleanup
- new location for statistics file (/var/log/)

* Sun Dec 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- Fix download url.

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 8.12.10-5
- rebuild against db-4.2.52.
 
* Thu Dec 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix pam alternatives handling
- add patch from Jakub Jelinek for PIE

* Fri Dec 05 2003 Karsten Hopp <karsten@redhat.de> 8.12.10-3
- fix usage of RPM_OPT_FLAGS variable in spec file
- add makecert.sh script to -doc subpackage
- add cert paths to sendmail.mc

* Wed Nov 26 2003 Karsten Hopp <karsten@redhat.de> 
- fix alternatives (#109313)
- enable TLS

* Mon Oct 27 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add some more system account entries into /etc/aliases
- add example for a mixed IPv6/IPv4 setup

* Fri Oct 24 2003 Harald Hoyer <harald@redhat.de> 8.12.10-2
- added with_ options

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 8.12.10-1.2
- rebuild against db-4.2.42.
 
* Thu Sep 18 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.10

* Wed Sep 17 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add security patches for CAN-2003-0694 and CAN-2003-0681

* Mon Sep 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- move debug information from sendmail into debuginfo rpm
- on %%post make sure /etc/aliases.db and /etc/mail/*.db is correctly
  owned by root
- do not set confTRUSTED_USER to smmsp in sendmail-redhat.mc

* Fri Aug 08 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- run "make -C /etc/mail" (maybe generating new sendmail.cf, then newaliases
- added $SENDMAIL_OPTARG that could be set by /etc/sysconfig/sendmail #99224

* Wed Jul 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- adjust rpm license tag to say "Sendmail"

* Fri Jul 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- enable pie only for a few archs
- enable full optims for s390 again, compiler seems to be fixed

* Mon Jun 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- apply patch from Ulrich Drepper to support -pie

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat May 31 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- make init script more robust #91879

* Sun May 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sendmail-cf requires m4, #90513

* Fri May  9 2003 Nalin Dahyabhai <nalin@redhat.com> 8.12.9-6
- move Sendmail.conf from /usr/lib/sasl to /usr/lib/sasl2 and change the
  default pwcheck method to "saslauthd"

* Mon May  5 2003 Nalin Dahyabhai <nalin@redhat.com> 8.12.9-5
- configure to use libsasl2 instead of libsasl to avoid linking with both
  (we also link to libldap, which now uses libsasl2)
- link with -ldb instead of -ldb-4.0 on all releases after RHL 7.3 instead
  of just 7.3 (all versions of db4-devel thereafter are expected to provide
  the right linking setup)

* Tue Apr 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add a "umask 022" before building the *.cf files in /etc/mail/Makefile

* Fri Apr 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- mark /etc/mail/Makefile as config(noreplace) #87688
- mark /etc/pam.d/smtp as config(noreplace) #87731

* Sun Mar 30 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.9

* Wed Mar 26 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- call make with the target "all" #86005
- add start/stop/restart as Makefile targets
- add another security patch

* Wed Mar 05 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add correct db4-devel requirements for newer releases
- completely re-do many ifdef code in the spec-file
- fix some issues building for older RHL releases

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.8

* Tue Feb 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 22 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add a confTRUSTED_USER line into sendmail.mc, submit.mc is already ok
- add patch from sendmail.org for cf/m4/proto.m4

* Mon Jan 13 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not reject all numeric login names if hesiod support is
  compiled in. #80060
- remove reference to non-existing man-pages #74552

* Sun Jan 12 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sendmail-8.12.7-etrn.patch from Jos Vos <jos@xos.nl>
- submit.mc: enable "use_ct_file" by default  #80519
- add _FFR_MILTER_ROOT_UNSAFE  #78223

* Sat Jan 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.7
- hack to make lib64 version work
- downgrade s390 optims to make it compile

* Mon Jan  6 2003 Nalin Dahyabhai <nalin@redhat.com>
- add openssl-devel as a build-time requirement
- preprocess the config file to add the right version of %%{_lib}
- add kerberos -I and -L flags to build configuration, needed for newer
  versions of libssl

* Wed Dec 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- always have a queue run interval for sm-msp-queue   #81424
- Jos Vos suggests adding another variable for sm-client queue-run

* Mon Dec 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add the following changes from Adrian Havill <havill@redhat.com>
  to our default sendmail.mc file:
	- added commented-out-by-default common AUTH/SSL examples
	- updated m4 example and rpm reference
	- added more comment documentation
	- add commented out confAUTO_REBUILD example
	- improve description about MASQUERADE_AS

* Mon Nov 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add to submit.mc: define(`_MTA_HOST_', `[127.0.0.1]')
  to deliver directly to localhost IP instead of going through DNS
- submit.mc: exchange msp and use_ct_file to better enable it
- do not undefine UUCP_RELAY and BITNET_RELAY
- sendmail.mc: use LOCAL_DOMAIN instead of "Cw" directly
- sendmail.mc: add commented out MASQUERADE_AS example
- re-enable DAEMON variable for now

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com>
- remove absolute path names from the PAM configuration, allowing it to be
  used by any arch on a multilib system

* Sun Nov 03 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix mailman alias  #75129

* Sat Nov 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.6

* Fri Oct 04 2002 Phil Knirsch <pknirsch@redhat.com> 8.12.5-7.2
- Drop optflags to default to build correctly on s390(x).

* Thu Sep 12 2002 Than Ngo <than@redhat.com> 8.12.5-7.1
- Added fix to build on x86_64

* Thu Aug 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- clean up some specfile cruft
- add more pseudo accounts to /etc/aliases

* Thu Jul 25 2002 Phil Knirsch <pknirsch@redhat.com>
- Only generate new cf files if the /usr/share/sendmail-cf/m4/cf.m4 exists.

* Wed Jul 24 2002 Phil Knirsch <pknirsch@redhat.com>
- Changed the behaviour in /etc/mail/Makefile to generate the sendmail.cf and
  submit.cf from the mc files if they changed.
- Added a small README.redhat that descibed the new mc file behaviour and the
  split into sendmail.cf and submit.cf.

* Wed Jul 24 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- suggestions form Stephane Lentz:
	- add correct include statement into submit.mc (like sendmail.mc)
	- add commented out further suggestions into submit.mc
	- disable ident lookups

* Thu Jul 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix initscript for the second daemon and pidfile location #67910

* Mon Jul 01 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.5

* Thu Jun 27 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add further queue runs, slight spec-file cleanups

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Jun 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.4, adjust smrsh patch

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sat Apr 13 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.12.3

* Tue Mar 26 2002 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Mar 25 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix alternatives --remove  #61737
- add sendmail/SECURITY as docu #61870, #61545

* Wed Mar 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add libsm.a #61270
- change from /etc/sendmail.cf to /etc/mail/sendmail.cf
- add milter patch

* Wed Mar 13 2002 Bill Nottingham <notting@redhat.com>
- ignore DAEMON=no; that configuration no longer functions

* Wed Mar 13 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- make sure more version information is in the cf file #54418
- do not use "-b" flag when patching in spec file
- require newer chkconfig version #61035
- fix preun script #60880
- add TMPF to access file creation #60956

* Sat Mar 09 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- mv include files to /usr/include/libmilter/ #60795
- do not use "-f" option to virtusertable #60196
- ad an example smarthost entry to config file #58298

* Fri Mar  8 2002 Bill Nottingham <notting@redhat.com> 8.12.2-5
- use alternatives --initscript support
- run chkconfig --add before alternatives

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com> 8.12.2-3
- run alternatives --remove in %%preun
- add some prereqs

* Mon Feb 25 2002 Nalin Dahyabhai <nalin@redhat.com> 8.12.2-2
- fix smmsp useradd invocation in %%pre
- switch back to db3 for storing db files

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> 8.12.2-1
- update to 8.12.2 (adds STARTTLS support without need for sfio)
- don't forcibly strip binaries; let the build root handle it
- add creation of the smmsp account (51/51) in %%pre
- enable hesiod map support
- modify default config to use an MSP
- comment out 'O AutoRebuildAliases' in %%post, otherwise sendmail will
  fail to restart on upgrades

* Wed Feb 20 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add proper ifdefs around new alternative stuff to also be able
  to build this for older releases

* Fri Feb  1 2002 Bill Nottingham <notting@redhat.com> 8.11.6-12
- %%triggerpostun on older versions to make sure alternatives work on
  upgrades

* Thu Jan 31 2002 Bill Nottingham <notting@redhat.com> 8.11.6-11
- clean up alternatives somewhat, provide /usr/sbin/sendmail & friends

* Thu Jan 31 2002 Bernhard Rosenkraenzer <bero@redhat.com> 8.11.6-10
- Use alternatives

* Tue Jan 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix quotation in spec-file

* Thu Jan 10 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- integrate ugly logic to compile this src.rpm also on older Red Hat
  Linux releases
- clean up spec file and patches a bit
- add db4 support

* Wed Jan 09 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- fix another path to correct docu
- include sendmail/README in the docu
- compile with -D_FFR_WORKAROUND_BROKEN_NAMESERVERS, but do not
  enable this at runtime
- devel subpackage files owned by root now

* Fri Dec 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change "-q" to "-s" as option to make #57216
- move milter lib into separate "devel" sub-package
- add include files to devel sub-package #56064
- fix pointer in access file to docu #54351

* Mon Sep 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add libmilter docu
- add support for userdb to /etc/mail/Makefile
- use "btree" database files if a userdb is used
- buildrequires tcp_wrappers

* Fri Aug 31 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix libmilter support
- fix init script to use /etc/mail/Makefile #52932

* Sat Aug 25 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add libmilter library

* Thu Aug 23 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.6
- correctly use /etc/mail/statistics

* Thu Aug 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change init script back to older conventions #51297
- remove DoS patch, not needed anymore #51247

* Mon Aug 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add option '-t' to procmail for local mail delivery

* Tue Jul 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- point to the map files in sendmail.cf as pointed out by
  David Beveridge <David@beveridge.com>

* Mon Jul 23 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add build requires #49695
- do not call "userdel"

* Tue Jul 10 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change sendmail.cf to "noreplace"

* Thu Jun 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.4

* Wed May 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.3
- add "localhost.localdomain" to the list of hostnames accepted
  for local delivery "Cw" in /etc/mail/sendmail.mc
- add patches from Pekka Savola <pekkas@netcore.fi>
	- Enable IPv6 at compile time, patch for glibc 2.2 from PLD
	- Add a commented-out IPv6 daemon .mc line to sendmail.mc
	- buildrequire: openldap-devel, cyrus-sasl-devel

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb 27 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add noreplace for /etc/sysconfig/sendmail and /etc/mail/sendmail.mc

* Wed Feb 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add changes from Christopher McCrory <chrismcc@pricegrabber.com>:
	- prepare /etc/mail/Makefile for more maps not shipped with this rpm
	- changed sendmail.mc to include some more commented out options,
	  so that people are directly pointed at important options
	- add /etc/pam.d/smtp for AUTH
	- add FEATURE(use_ct_file) and /etc/mail/trusted-users

* Fri Feb 16 2001 Tim Powers <timp@redhat.com>
- don't obsolete postfix and exim, only conflict (for RHN purposes)

* Thu Feb 15 2001 Trond Eivind Glomsrød <teg@redhat.com>
- obsolete and conflict with exim and postfix

* Wed Feb 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix devision by zero bug in #20395
- mv /usr/lib/sendmail-cf /usr/share/sendmail-cf

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18n tweaks to initscript

* Wed Feb 07 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- aliases.db should be owned by group root

* Wed Jan 24 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- prepare for startup-script translation

* Tue Jan 23 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- enable daemon mode again, but only listen to the loopback device
  instead of all devices.
- do not include check.tar with old anti-spam rules 

* Fri Jan 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix configuration of /etc/aliases

* Mon Jan 08 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fix interoperation problems with communigate pro
- disable msa

* Thu Jan 04 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to (security release) 8.11.2
- build also on RHL 6.x #16061
- include smrsh man-page #17901
- use the "-f" flag for makemap to preserve case for virtusertable
  and userdb in /etc/mail/Makefile - suggested by Harald Hoyer
- fix /usr/doc -> usr/share/doc in docu #20611
- wrong path in sendmail.mc #20691
- tcp-wrapper support wasn't enabled correctly #21642
- do not expose user "root" when masquerading like in older releases #21643
- disable the VRFY and EXPN smtp commands #21801
- disable queue-runs for normal users (restrictqrun privacy flag)
- fix typo in sendmail.mc #21880, #22682
- disable daemon mode to see what needs fixing

* Mon Oct 02 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 8.11.1

* Fri Sep 08 2000 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Aug 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- apply fixes for LDAP maps being closed too soon

* Mon Aug 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- provide /usr/lib/sasl/Sendmail.conf so that people know we can use it (#16064)

* Mon Aug  7 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- enable listening on the smtp port again

* Fri Aug  4 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix "missing find_m4.sh" problem by defining M4=/usr/bin/m4 (#14767)

* Mon Jul 31 2000 Nalin Dahyabhai <nalin@redhat.com>
- okay, enable LDAP support again
- enable SMTP auth support via Cyrus SASL

* Tue Jul 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- disable the LDAP support until we can remove the sendmail->OpenLDAP->perl dep
- fix prereq

* Tue Jul 25 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to sendmail 8.11.0
- add LDAP support

* Thu Jul 20 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jul  9 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- require procmail
- add further aliases

* Sat Jul  8 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- prereq init.d
- fix typo

* Tue Jul  4 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- ignore error from useradd

* Fri Jun 30 2000 Than Ngo <than@redhat.de>
- FHS fixes
- /etc/rc.d/init.d -> /etc/init.d
- fix initscript

* Fri Jun 23 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- change to /usr/share/man

* Wed Jun 21 2000 Preston Brown <pbrown@redhat.com>
- turn off daemon behaviour by default

* Sun Jun 18 2000 Bill Nottingham <notting@redhat.com>
- rebuild, fix dependencies

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- prereq /usr/sbin/useradd

* Fri May 19 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- enable MAP_REGEX
- enable tcp_wrapper support

* Thu May 18 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- fix etc/mail/aliases -> /etc/aliases in sendmail-redhat.mc

* Wed May  3 2000 Bill Nottingham <notting@redhat.com>
- update to 8.10.1
- fix build without sendmail installed
- add 'mailnull' user

* Wed Mar 15 2000 Bill Nottingham <notting@redhat.com>
- update to 8.10.0
- remove compatiblity chkconfig links
- add a mailnull user for sendmail to use

* Thu Feb 17 2000 Cristian Gafton <gafton@redhat.com>
- break the hard link for makemap and create it as a symlnk (#8223)

* Thu Feb 17 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Fix location of mailertable (Bug #6035)

* Sat Feb  5 2000 Bill Nottingham <notting@redhat.com>
- fixes for non-root builds (#8178)

* Wed Feb  2 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- change perms on /etc/sysconfig/sendmail from 0755 to 0644
- allow compressed man-pages

* Thu Dec 02 1999 Cristian Gafton <gafton@redhat.com>
- add patch to prevent the DoS when rebuilding aliases

* Wed Sep  1 1999 Jeff Johnson <jbj@redhat.com>
- install man pages, not groff output (#3746).
- use dnl not '#' in m4 comment (#3749).
- add FEATURE(mailtertable) to the config -- example file needs this (#4649).
- use db2 not db1.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- add 127.0.0.1 to /etc/mail/access to avoid IDENT: relay problem (#3178).

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in preun, not postun (#3982)

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Fri Jul 02 1999 Cristian Gafton <gafton@redhat.com>
- fixed typo bug in comment in the default .mc file (#2812)

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- fox the awk scripts in the postinstall
- enable FEATURE(accept_unresolvable_domains) by default to make laptop
  users happy.

* Sun Apr 18 1999 Cristian Gafton <gafton@redhat.com>
- make the redhat.mc be a separate source files. Sanitize patches that used
  to touch it.
- install redhat.mc as /etc/sendmail.mc so that people can easily modify
  their sendmail.cf configurations.

* Mon Apr 05 1999 Cristian Gafton <gafton@redhat.com>
- fixed virtusertable patch
- make smrsh look into /etc/smrsh

* Mon Mar 29 1999 Jeff Johnson <jbj@redhat.com>
- remove noreplace attr from sednmail.cf.

* Thu Mar 25 1999 Cristian Gafton <gafton@redhat.com>
- provide a more sane /etc/mail/access default config file
- use makemap to initializa the empty databases, not touch
- added a small, but helpful /etc/mail/Makefile

* Mon Mar 22 1999 Jeff Johnson <jbj@redhat.com>
- correxct dangling symlinks.
- check for map file existence in %%post.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Jeff Johnson <jbj@redhat.com>
- improved 8.9.3 config from Mike McHenry <mmchen@minn.net>

* Tue Mar 16 1999 Cristian Gafton <gafton@redhat.com>
- version 8.9.3

* Tue Dec 29 1998 Cristian Gafton <gafton@redhat.com>
- build for 6.0
- use the libdb1 stuff correctly

* Mon Sep 21 1998 Michael K. Johnson <johnsonm@redhat.com>
- Allow empty QUEUE in /etc/sysconfig/sendmail for those who
  want to run sendmail in daemon mode without processing the
  queue regularly.

* Thu Sep 17 1998 Michael K. Johnson <johnsonm@redhat.com>
- /etc/sysconfig/sendmail

* Fri Aug 28 1998 Jeff Johnson <jbj@redhat.com>
- recompile statically linked binary for 5.2/sparc

* Tue May 05 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- enhanced initscripts

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- added a rmail patch

* Wed Oct 29 1997 Donnie Barnes <djb@redhat.com>
- argh!  Fixed some of the db1 handling that had to be added for glibc 2.1

* Fri Oct 24 1997 Donnie Barnes <djb@redhat.com>
- added support for db1 on SPARC

* Thu Oct 16 1997 Donnie Barnes <djb@redhat.com>
- added chkconfig support
- various spec file cleanups
- changed group to Networking/Daemons (from Daemons).  Sure, it runs on
  non networked systems, but who really *needs* it then?

* Wed Oct 08 1997 Donnie Barnes <djb@redhat.com>
- made /etc/mail/deny.db a ghost
- removed preun that used to remove deny.db (ghost handles that now)
- NOTE: upgrading from the sendmail packages in 4.8, 4.8.1, and possibly
  4.9 (all Red Hat betas between 4.2 and 5.0) could cause problems.  You
  may need to do a makemap in /etc/mail and a newaliases after upgrading
  from those packages.  Upgrading from 4.2 or prior should be fine.

* Mon Oct 06 1997 Erik Troan <ewt@redhat.com>
- made aliases.db a ghost

* Tue Sep 23 1997 Donnie Barnes <djb@redhat.com>
- fixed preuninstall script to handle aliases.db on upgrades properly

* Mon Sep 15 1997 Donnie Barnes <djb@redhat.com>
- fixed post-install output and changed /var/spool/mqueue to 755

* Thu Sep 11 1997 Donnie Barnes <djb@redhat.com>
- fixed /usr/lib/sendmail-cf paths

* Tue Sep 09 1997 Donnie Barnes <djb@redhat.com>
- updated to 8.8.7
- added some spam filtration
- combined some makefile patches
- added BuildRoot support

* Wed Sep 03 1997 Erik Troan <ewt@redhat.com>
- marked initscript symlinks as missingok
- run newalises after creating /var/spool/mqueue

* Thu Jun 12 1997 Erik Troan <ewt@redhat.com>
- built against glibc, udated release to -6 (skipped -5!)

* Tue Apr 01 1997 Erik Troan <ewt@redhat.com>
- Added -nsl on the Alpha (for glibc to provide NIS functions).

* Mon Mar 03 1997 Erik Troan <ewt@redhat.com>
- Added nis support.
