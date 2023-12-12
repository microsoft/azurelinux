# plugins have unresolvable symbols in compile time
%undefine _strict_symbol_defs_build

%bcond_without mysql
%bcond_without pgsql
%bcond_without sqlite
%bcond_without cdb
%bcond_without ldap
%bcond_without lmdb
%bcond_without pcre
%bcond_without sasl
%bcond_without tls
%bcond_without ipv6
%bcond_without pflogsumm

%global sysv2systemdnvr 2.8.12-2

# hardened build if not overrided
%{!?_hardened_build:%global _hardened_build 1}

# Postfix requires one exlusive uid/gid and a 2nd exclusive gid for its own
# use.  Let me know if the second gid collides with another package.
# Be careful: Redhat's 'mail' user & group isn't unique!
%define postfix_uid	89
%define postfix_user	postfix
%define postfix_gid	89
%define postfix_group	postfix
%define maildrop_group	postdrop
%define maildrop_gid	90

%define postfix_config_dir	%{_sysconfdir}/postfix
%define postfix_daemon_dir	%{_libexecdir}/postfix
%define postfix_shlib_dir	%{_libdir}/postfix
%define postfix_command_dir	%{_sbindir}
%define postfix_queue_dir	%{_var}/spool/postfix
%define postfix_data_dir	%{_sharedstatedir}/postfix
%define postfix_doc_dir		%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
%define postfix_sample_dir	%{postfix_doc_dir}/samples
%define postfix_readme_dir	%{postfix_doc_dir}/README_FILES

%global sslcert %{_sysconfdir}/pki/tls/certs/postfix.pem
%global sslkey  %{_sysconfdir}/pki/tls/private/postfix.key

# Filter private libraries
%global _privatelibs libpostfix-.+\.so.*
%global __provides_exclude ^(%{_privatelibs})$
%global __requires_exclude ^(%{_privatelibs})$

# Sources 50-99 are upstream [patch] contributions

%define pflogsumm_ver 1.1.5

Summary:        Postfix Mail Transport Agent
Name:           postfix
Version:        3.7.0
Release:        2%{?dist}
License:        (IBM AND GPLv2+) OR (EPL-2.0 AND GPLv2+)
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.postfix.org
Source0:        ftp://ftp.porcupine.org/mirrors/postfix-release/official/%{name}-%{version}.tar.gz
Source1:        postfix-etc-init.d-postfix
Source2:        postfix.service
Source3:        README-Postfix-SASL-RedHat.txt
Source4:        postfix.aliasesdb
Source5:        postfix-chroot-update
# Postfix Log Entry Summarizer: http://jimsun.linxnet.com/postfix_contrib.html
Source53:       http://jimsun.linxnet.com/downloads/pflogsumm-%{pflogsumm_ver}.tar.gz
# Sources >= 100 are config files
Source100:      postfix-sasl.conf
Source101:      postfix-pam.conf
# Patches
Patch1:         postfix-3.5.0-config.patch
Patch2:         postfix-3.4.0-files.patch
Patch3:         postfix-3.3.3-alternatives.patch
Patch4:         postfix-3.4.0-large-fs.patch
Patch9:         pflogsumm-1.1.5-datecalc.patch
# rhbz#1384871, sent upstream
Patch10:        pflogsumm-1.1.5-ipv6-warnings-fix.patch
Patch11:        postfix-3.4.4-chroot-example-fix.patch
# upstream patch
Patch12:        postfix-3.6.2-glibc-234-build-fix.patch
# sent upstream
Patch13:        postfix-3.6.2-whitespace-name-fix.patch
# rhbz#1931403, sent upstream
Patch14:        pflogsumm-1.1.5-syslog-name-underscore-fix.patch

BuildRequires:  findutils
BuildRequires:  gcc
BuildRequires:  libdb-devel
BuildRequires:  libicu-devel
BuildRequires:  libnsl2-devel
BuildRequires:  m4
# Optional patches - set the appropriate environment variables to include
#                    them when building the package/spec file


# Determine the different packages required for building postfix
BuildRequires:  make
BuildRequires:  perl-generators
BuildRequires:  pkg-config
BuildRequires:  systemd-units
BuildRequires:  zlib-devel

%{?with_ldap:BuildRequires: openldap-devel}
%{?with_lmdb:BuildRequires: lmdb-devel}
%{?with_sasl:BuildRequires: cyrus-sasl-devel}
%{?with_pcre:BuildRequires: pcre-devel}
%{?with_mysql:BuildRequires: mariadb-connector-c-devel}
%{?with_pgsql:BuildRequires: libpq-devel}
%{?with_sqlite:BuildRequires: sqlite-devel}
%{?with_cdb:BuildRequires: tinycdb-devel}
%{?with_tls:BuildRequires: openssl-devel}

# Required by /usr/libexec/postfix/postfix-script
Requires:       diffutils
Requires:       findutils
# for restorecon
Requires:       policycoreutils

Requires(post): %{_bindir}/openssl
Requires(post): %{_sbindir}/alternatives
Requires(post): hostname
Requires(post): systemd
Requires(post): systemd-sysv
Requires(postun): systemd
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd
Requires(preun): %{_sbindir}/alternatives
Requires(preun): systemd

Provides:       MTA
Provides:       smtpd
Provides:       smtpdaemon
Provides:       server(smtp)

%description
Postfix is a Mail Transport Agent (MTA).

%package perl-scripts
Summary:        Postfix utilities written in perl
Requires:       %{name} = %{version}-%{release}
%if %{with pflogsumm}
Provides:       postfix-pflogsumm = %{version}-%{release}
%endif

%description perl-scripts
This package contains perl scripts pflogsumm and qshape.

Pflogsumm is a log analyzer/summarizer for the Postfix MTA. It is
designed to provide an over-view of Postfix activity. Pflogsumm
generates summaries and, in some cases, detailed reports of mail
server traffic volumes, rejected and bounced email, and server
warnings, errors and panics.

qshape prints Postfix queue domain and age distribution.

%if %{with mysql}
%package mysql
Summary:        Postfix MySQL map support
Requires:       %{name} = %{version}-%{release}

%description mysql
This provides support for MySQL maps in Postfix. If you plan to use MySQL
maps with Postfix, you need this.
%endif

%if %{with pgsql}
%package pgsql
Summary:        Postfix PostgreSQL map support
Requires:       %{name} = %{version}-%{release}

%description pgsql
This provides support for PostgreSQL  maps in Postfix. If you plan to use
PostgreSQL maps with Postfix, you need this.
%endif

%if %{with sqlite}
%package sqlite
Summary:        Postfix SQLite map support
Requires:       %{name} = %{version}-%{release}

%description sqlite
This provides support for SQLite maps in Postfix. If you plan to use SQLite
maps with Postfix, you need this.
%endif

%if %{with cdb}
%package cdb
Summary:        Postfix CDB map support
Requires:       %{name} = %{version}-%{release}

%description cdb
This provides support for CDB maps in Postfix. If you plan to use CDB
maps with Postfix, you need this.
%endif

%if %{with ldap}
%package ldap
Summary:        Postfix LDAP map support
Requires:       %{name} = %{version}-%{release}

%description ldap
This provides support for LDAP maps in Postfix. If you plan to use LDAP
maps with Postfix, you need this.
%endif

%if %{with lmdb}
%package lmdb
Summary:        Postfix LDMB map support
Requires:       %{name} = %{version}-%{release}

%description lmdb
This provides support for LMDB maps in Postfix. If you plan to use LMDB
maps with Postfix, you need this.
%endif

%if %{with pcre}
%package pcre
Summary:        Postfix PCRE map support
Requires:       %{name} = %{version}-%{release}

%description pcre
This provides support for PCRE maps in Postfix. If you plan to use PCRE
maps with Postfix, you need this.
%endif

%prep
%setup -q
# Apply obligatory patches
%patch1 -p1 -b .config
%patch2 -p1 -b .files
%patch3 -p1 -b .alternatives
%patch4 -p1 -b .large-fs

# Change DEF_SHLIB_DIR according to build host
sed -i \
's|^\(\s*#define\s\+DEF_SHLIB_DIR\s\+\)"/usr/lib/postfix"|\1"%{_libdir}/postfix"|' \
src/global/mail_params.h

%if %{with pflogsumm}
gzip -dc %{SOURCE53} | tar xf -
pushd pflogsumm-%{pflogsumm_ver}
%patch9 -p1 -b .datecalc
%patch10 -p1 -b .ipv6-warnings-fix
popd
%endif
%patch11 -p1 -b .chroot-example-fix
%patch12 -p1 -b .glibc-234-build-fix
%patch13 -p1 -b .whitespace-name-fix
%patch14 -p1 -b .pflogsumm-1.1.5-syslog-name-underscore-fix

for f in README_FILES/TLS_{LEGACY_,}README TLS_ACKNOWLEDGEMENTS; do
	iconv -f iso8859-1 -t utf8 -o ${f}{_,} &&
		touch -r ${f}{,_} && mv -f ${f}{_,}
done

%build
%set_build_flags
unset AUXLIBS AUXLIBS_LDAP AUXLIBS_LMDB AUXLIBS_PCRE AUXLIBS_MYSQL AUXLIBS_PGSQL AUXLIBS_SQLITE AUXLIBS_CDB
CCARGS="-fPIC -fcommon"
AUXLIBS="-lnsl"

%ifarch s390 s390x ppc
CCARGS="${CCARGS} -fsigned-char"
%endif

%if %{with ldap}
  CCARGS="${CCARGS} -DHAS_LDAP -DLDAP_DEPRECATED=1 %{?with_sasl:-DUSE_LDAP_SASL}"
  AUXLIBS_LDAP="-lldap -llber"
%endif
%if %{with lmdb}
  CCARGS="${CCARGS} -DHAS_LMDB"
  AUXLIBS_LMDB="-llmdb"
%endif
%if %{with pcre}
  # -I option required for pcre 3.4 (and later?)
  CCARGS="${CCARGS} -DHAS_PCRE -I%{_includedir}/pcre"
  AUXLIBS_PCRE="-lpcre"
%endif
%if %{with mysql}
  CCARGS="${CCARGS} -DHAS_MYSQL -I%{_includedir}/mysql"
  AUXLIBS_MYSQL="-L%{_libdir}/mariadb -lmysqlclient -lm"
%endif
%if %{with pgsql}
  CCARGS="${CCARGS} -DHAS_PGSQL -I%{_includedir}/pgsql"
  AUXLIBS_PGSQL="-lpq"
%endif
%if %{with sqlite}
  CCARGS="${CCARGS} -DHAS_SQLITE `pkg-config --cflags sqlite3`"
  AUXLIBS_SQLITE="`pkg-config --libs sqlite3`"
%endif
%if %{with cdb}
  CCARGS="${CCARGS} -DHAS_CDB `pkg-config --cflags libcdb`"
  AUXLIBS_CDB="`pkg-config --libs libcdb`"
%endif
%if %{with sasl}
  CCARGS="${CCARGS} -DUSE_SASL_AUTH -DUSE_CYRUS_SASL -I%{_includedir}/sasl"
  AUXLIBS="${AUXLIBS} -L%{_libdir}/sasl2 -lsasl2"
  %global sasl_config_dir %{_sysconfdir}/sasl2
%endif
%if %{with tls}
  if pkg-config openssl ; then
    CCARGS="${CCARGS} -DUSE_TLS `pkg-config --cflags openssl`"
    AUXLIBS="${AUXLIBS} `pkg-config --libs openssl`"
  else
    CCARGS="${CCARGS} -DUSE_TLS -I%{_includedir}/openssl"
    AUXLIBS="${AUXLIBS} -lssl -lcrypto"
  fi
%endif
%if ! %{with ipv6}
  CCARGS="${CCARGS} -DNO_IPV6"
%endif

CCARGS="${CCARGS} -DDEF_CONFIG_DIR=\\\"%{postfix_config_dir}\\\""
CCARGS="${CCARGS} $(getconf LFS_CFLAGS)"

LDFLAGS="$LDFLAGS %{?_hardened_build:-Wl,-z,relro,-z,now}"

# SHLIB_RPATH is needed to find private libraries
# LDFLAGS are added to SHLIB_RPATH because the postfix build system
# ignores them. Adding LDFLAGS to SHLIB_RPATH is currently the only
# way how to get them in
make -f Makefile.init makefiles shared=yes dynamicmaps=yes \
  %{?_hardened_build:pie=yes} CCARGS="${CCARGS}" AUXLIBS="${AUXLIBS}" \
  AUXLIBS_LDAP="${AUXLIBS_LDAP}" AUXLIBS_LMDB="${AUXLIBS_LMDB}" \
  AUXLIBS_PCRE="${AUXLIBS_PCRE}" AUXLIBS_MYSQL="${AUXLIBS_MYSQL}" \
  AUXLIBS_PGSQL="${AUXLIBS_PGSQL}" AUXLIBS_SQLITE="${AUXLIBS_SQLITE}" \
  AUXLIBS_CDB="${AUXLIBS_CDB}" \
  DEBUG="" SHLIB_RPATH="-Wl,-rpath,%{postfix_shlib_dir} $LDFLAGS" \
  OPT="$CFLAGS -fno-strict-aliasing -Wno-comment" \
  POSTFIX_INSTALL_OPTS=-keep-build-mtime

%make_build

%install
# install postfix into $RPM_BUILD_ROOT

# Move stuff around so we don't conflict with sendmail
for i in man1/mailq.1 man1/newaliases.1 man1/sendmail.1 man5/aliases.5 man8/smtpd.8; do
  dest=$(echo $i | sed 's|\.[1-9]$|.postfix\0|')
  mv man/$i man/$dest
  sed -i "s|^\.so $i|\.so $dest|" man/man?/*.[1-9]
done

make non-interactive-package \
       install_root=%{buildroot} \
       config_directory=%{postfix_config_dir} \
       meta_directory=%{postfix_config_dir} \
       shlib_directory=%{postfix_shlib_dir} \
       daemon_directory=%{postfix_daemon_dir} \
       command_directory=%{postfix_command_dir} \
       queue_directory=%{postfix_queue_dir} \
       data_directory=%{postfix_data_dir} \
       sendmail_path=%{postfix_command_dir}/sendmail.postfix \
       newaliases_path=%{_bindir}/newaliases.postfix \
       mailq_path=%{_bindir}/mailq.postfix \
       mail_owner=%{postfix_user} \
       setgid_group=%{maildrop_group} \
       manpage_directory=%{_mandir} \
       sample_directory=%{postfix_sample_dir} \
       readme_directory=%{postfix_readme_dir} || exit 1

# Systemd
mkdir -p %{buildroot}%{_unitdir}
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}
install -m 755 %{SOURCE4} %{buildroot}%{postfix_daemon_dir}/aliasesdb
install -m 755 %{SOURCE5} %{buildroot}%{postfix_daemon_dir}/chroot-update

install -c auxiliary/rmail/rmail %{buildroot}%{_bindir}/rmail.postfix

for i in active bounce corrupt defer deferred flush incoming private saved maildrop public pid saved trace; do
    mkdir -p %{buildroot}%{postfix_queue_dir}/$i
done

# install performance benchmark and test tools by hand
for i in smtp-sink smtp-source posttls-finger ; do
  install -c -m 755 bin/$i %{buildroot}%{postfix_command_dir}/
  install -c -m 755 man/man1/$i.1 %{buildroot}%{_mandir}/man1/
done

## RPM compresses man pages automatically.
## - Edit postfix-files to reflect this, so post-install won't get confused
##   when called during package installation.
sed -i -r "s#(/man[158]/.*.[158]):f#\1.gz:f#" %{buildroot}%{postfix_config_dir}/postfix-files

cat %{buildroot}%{postfix_config_dir}/postfix-files
%if %{with sasl}
# Install the smtpd.conf file for SASL support.
mkdir -p %{buildroot}%{sasl_config_dir}
install -m 644 %{SOURCE100} %{buildroot}%{sasl_config_dir}/smtpd.conf
%endif

mkdir -p %{buildroot}%{_sysconfdir}/pam.d
install -m 644 %{SOURCE101} %{buildroot}%{_sysconfdir}/pam.d/smtp.postfix

# prepare documentation
mkdir -p %{buildroot}%{postfix_doc_dir}
cp -p %{SOURCE3} COMPATIBILITY LICENSE TLS_ACKNOWLEDGEMENTS TLS_LICENSE %{buildroot}%{postfix_doc_dir}

mkdir -p %{buildroot}%{postfix_doc_dir}/examples{,/chroot-setup}
cp -pr examples/{qmail-local,smtpd-policy} %{buildroot}%{postfix_doc_dir}/examples
cp -p examples/chroot-setup/LINUX2 %{buildroot}%{postfix_doc_dir}/examples/chroot-setup

cp conf/{main,bounce}.cf.default %{buildroot}%{postfix_doc_dir}
sed -i 's#%{postfix_config_dir}\(/bounce\.cf\.default\)#%{postfix_doc_dir}\1#' %{buildroot}%{_mandir}/man5/bounce.5
rm -f %{buildroot}%{postfix_config_dir}/{TLS_,}LICENSE

find %{buildroot}%{postfix_doc_dir} -type f | xargs chmod 644
find %{buildroot}%{postfix_doc_dir} -type d | xargs chmod 755

%if %{with pflogsumm}
install -c -m 644 pflogsumm-%{pflogsumm_ver}/pflogsumm-faq.txt %{buildroot}%{postfix_doc_dir}/pflogsumm-faq.txt
install -c -m 644 pflogsumm-%{pflogsumm_ver}/pflogsumm.1 %{buildroot}%{_mandir}/man1/pflogsumm.1
install -c pflogsumm-%{pflogsumm_ver}/pflogsumm.pl %{buildroot}%{postfix_command_dir}/pflogsumm
%endif

# install qshape
mantools/srctoman - auxiliary/qshape/qshape.pl > qshape.1
install -c qshape.1 %{buildroot}%{_mandir}/man1/qshape.1
install -c auxiliary/qshape/qshape.pl %{buildroot}%{postfix_command_dir}/qshape

# remove alias file
rm -f %{buildroot}%{postfix_config_dir}/aliases

# create /usr/lib/sendmail
mkdir -p %{buildroot}%{_libdir}
pushd %{buildroot}%{_libdir}
ln -sf ../sbin/sendmail.postfix .
popd

mkdir -p %{buildroot}%{_sharedstatedir}/misc
touch %{buildroot}%{_sharedstatedir}/misc/postfix.aliasesdb-stamp

# prepare alternatives ghosts
for i in %{postfix_command_dir}/sendmail %{_bindir}/{mailq,newaliases,rmail} \
	%{_sysconfdir}/pam.d/smtp %{_libdir}/sendmail \
	%{_mandir}/{man1/{mailq.1,newaliases.1},man5/aliases.5,man8/{sendmail.8,smtpd.8}}
do
	touch $RPM_BUILD_ROOT$i
done

# helper for splitting content of dynamicmaps.cf and postfix-files
function split_file
{
# "|| :" to silently skip non existent records
  grep "$1" "$3" >> "$3.d/$2" || :
  sed -i "\|$1| d" "$3" || :
}

# split global dynamic maps configuration to individual sub-packages
pushd %{buildroot}%{postfix_config_dir}
for map in %{?with_mysql:mysql} %{?with_pgsql:pgsql} %{?with_sqlite:sqlite} \
%{?with_cdb:cdb} %{?with_ldap:ldap} %{?with_lmdb:lmdb} %{?with_pcre:pcre}; do
  rm -f dynamicmaps.cf.d/"$map" "postfix-files.d/$map"
  split_file "^\s*$map\b" "$map" dynamicmaps.cf
  sed -i "s|postfix-$map\\.so|%{postfix_shlib_dir}/\\0|" "dynamicmaps.cf.d/$map"
  split_file "^\$shlib_directory/postfix-$map\\.so:" "$map" postfix-files
  split_file "^\$manpage_directory/man5/${map}_table\\.5" "$map" postfix-files
  map_upper=`echo $map | tr '[:lower:]' '[:upper:]'`
  split_file "^\$readme_directory/${map_upper}_README:" "$map" postfix-files
done
popd

%post -e
%systemd_post %{name}.service

# upgrade configuration files if necessary
%{_sbindir}/postfix set-permissions upgrade-configuration \
	daemon_directory=%{postfix_daemon_dir} \
	command_directory=%{postfix_command_dir} \
	mail_owner=%{postfix_user} \
	setgid_group=%{maildrop_group} \
	manpage_directory=%{_mandir} \
	sample_directory=%{postfix_sample_dir} \
	readme_directory=%{postfix_readme_dir} &> /dev/null

ALTERNATIVES_DOCS=""
[ "%%{_excludedocs}" = 1 ] || ALTERNATIVES_DOCS='--slave %{_mandir}/man1/mailq.1.gz mta-mailqman %{_mandir}/man1/mailq.postfix.1.gz
	--slave %{_mandir}/man1/newaliases.1.gz mta-newaliasesman %{_mandir}/man1/newaliases.postfix.1.gz
	--slave %{_mandir}/man8/sendmail.8.gz mta-sendmailman %{_mandir}/man1/sendmail.postfix.1.gz
	--slave %{_mandir}/man5/aliases.5.gz mta-aliasesman %{_mandir}/man5/aliases.postfix.5.gz
	--slave %{_mandir}/man8/smtpd.8.gz mta-smtpdman %{_mandir}/man8/smtpd.postfix.8.gz'

%{_sbindir}/alternatives --install %{postfix_command_dir}/sendmail mta %{postfix_command_dir}/sendmail.postfix 60 \
	--slave %{_bindir}/mailq mta-mailq %{_bindir}/mailq.postfix \
	--slave %{_bindir}/newaliases mta-newaliases %{_bindir}/newaliases.postfix \
	--slave %{_sysconfdir}/pam.d/smtp mta-pam %{_sysconfdir}/pam.d/smtp.postfix \
	--slave %{_bindir}/rmail mta-rmail %{_bindir}/rmail.postfix \
	--slave %{_libdir}/sendmail mta-sendmail %{_libdir}/sendmail.postfix \
	$ALTERNATIVES_DOCS \
	--initscript postfix

%if %{with sasl}
# Move sasl config to new location
if [ -f %{_libdir}/sasl2/smtpd.conf ]; then
	mv -f %{_libdir}/sasl2/smtpd.conf %{sasl_config_dir}/smtpd.conf
	/sbin/restorecon %{sasl_config_dir}/smtpd.conf 2> /dev/null
fi
%endif

# Create self-signed SSL certificate
if [ ! -f %{sslkey} ]; then
  umask 077
  %{_bindir}/openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:4096 -out %{sslkey} 2>/dev/null || echo "openssl genpkey failed"
fi

if [ ! -f %{sslcert} ]; then
  FQDN=`hostname`
  if [ "x${FQDN}" = "x" ]; then
    FQDN=localhost.localdomain
  fi

  req_cmd="%{_bindir}/openssl req -new -key %{sslkey} -x509 -sha256 -days 365 -set_serial $RANDOM -out %{sslcert} \
    -subj /C=--/ST=SomeState/L=SomeCity/O=SomeOrganization/OU=SomeOrganizationalUnit/CN=${FQDN}/emailAddress=root@${FQDN}"
# openssl-3.0 and fallback for backward compatibility with openssl < 3.0
  $req_cmd -noenc -copy_extensions none 2>/dev/null || $req_cmd 2>/dev/null || echo "openssl req failed"
  chmod 644 %{sslcert}
fi

exit 0

%pre
# Add user and groups if necessary
%{_sbindir}/groupadd -g %{maildrop_gid} -r %{maildrop_group} 2>/dev/null
%{_sbindir}/groupadd -g %{postfix_gid} -r %{postfix_group} 2>/dev/null
%{_sbindir}/groupadd -g 12 -r mail 2>/dev/null
%{_sbindir}/useradd -d %{postfix_queue_dir} -s %{_sbindir}/nologin -g %{postfix_group} -G mail -M -r -u %{postfix_uid} %{postfix_user} 2>/dev/null

# hack, to turn man8/smtpd.8.gz into alternatives symlink (part of the rhbz#1051180 fix)
# this could be probably dropped in f23+
if [ -e %{_mandir}/man8/smtpd.8.gz ]; then
	[ -h %{_mandir}/man8/smtpd.8.gz ] || rm -f %{_mandir}/man8/smtpd.8.gz
fi

exit 0

%preun
%systemd_preun %{name}.service

if [ "$1" = 0 ]; then
    %{_sbindir}/alternatives --remove mta %{postfix_command_dir}/sendmail.postfix
fi
exit 0

%postun
%systemd_postun_with_restart %{name}.service

%triggerun -- postfix < %{sysv2systemdnvr}
%{_bindir}/systemd-sysv-convert --save postfix >/dev/null 2>&1 ||:
%{_bindir}/systemd-sysv-convert --apply postfix >/dev/null 2>&1 ||:
/sbin/chkconfig --del postfix >/dev/null 2>&1 || :
/bin/systemctl try-restart postfix.service >/dev/null 2>&1 || :

%files

# For correct directory permissions check postfix-install script.
# It reads the file postfix-files which defines the ownership
# and permissions for all files postfix installs.

%defattr(-, root, root, -)

# Config files not part of upstream

%if %{with sasl}
%config(noreplace) %{sasl_config_dir}/smtpd.conf
%endif
%config(noreplace) %{_sysconfdir}/pam.d/smtp.postfix
%{_unitdir}/postfix.service

# Documentation
%license TLS_LICENSE LICENSE
%{postfix_doc_dir}
%if %{with pflogsumm}
%exclude %{postfix_doc_dir}/pflogsumm-faq.txt
%endif

# Exclude due to dynamic maps subpackages
%exclude %{_mandir}/man5/mysql_table.5*
%exclude %{postfix_doc_dir}/README_FILES/MYSQL_README
%exclude %{_mandir}/man5/pgsql_table.5*
%exclude %{postfix_doc_dir}/README_FILES/PGSQL_README
%exclude %{_mandir}/man5/sqlite_table.5*
%exclude %{postfix_doc_dir}/README_FILES/SQLITE_README
%exclude %{postfix_doc_dir}/README_FILES/CDB_README
%exclude %{_mandir}/man5/ldap_table.5*
%exclude %{postfix_doc_dir}/README_FILES/LDAP_README
%exclude %{_mandir}/man5/lmdb_table.5*
%exclude %{postfix_doc_dir}/README_FILES/LMDB_README
%exclude %{_mandir}/man5/pcre_table.5*
%exclude %{postfix_doc_dir}/README_FILES/PCRE_README

# Misc files

%dir %attr(0755, root, root) %{postfix_config_dir}
%dir %attr(0755, root, root) %{postfix_daemon_dir}
%dir %attr(0755, root, root) %{postfix_queue_dir}
%dir %attr(0755, root, root) %{postfix_shlib_dir}
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/active
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/bounce
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/corrupt
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/defer
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/deferred
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/flush
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/hold
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/incoming
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/saved
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/trace
%dir %attr(0730, %{postfix_user}, %{maildrop_group}) %{postfix_queue_dir}/maildrop
%dir %attr(0755, root, root) %{postfix_queue_dir}/pid
%dir %attr(0700, %{postfix_user}, root) %{postfix_queue_dir}/private
%dir %attr(0710, %{postfix_user}, %{maildrop_group}) %{postfix_queue_dir}/public
%dir %attr(0700, %{postfix_user}, root) %{postfix_data_dir}
%dir %attr(0755, root, root) %{postfix_config_dir}/dynamicmaps.cf.d
%dir %attr(0755, root, root) %{postfix_config_dir}/postfix-files.d

%attr(0644, root, root) %{_mandir}/man1/post*.1*
%attr(0644, root, root) %{_mandir}/man1/smtp*.1*
%attr(0644, root, root) %{_mandir}/man1/*.postfix.1*
%attr(0644, root, root) %{_mandir}/man5/access.5*
%attr(0644, root, root) %{_mandir}/man5/[b-v]*.5*
%attr(0644, root, root) %{_mandir}/man5/*.postfix.5*
%attr(0644, root, root) %{_mandir}/man8/[a-qt-v]*.8*
%attr(0644, root, root) %{_mandir}/man8/s[ch-lnp]*.8*
%attr(0644, root, root) %{_mandir}/man8/smtp.8*
%attr(0644, root, root) %{_mandir}/man8/smtpd.postfix.8*

%attr(0755, root, root) %{postfix_command_dir}/smtp-sink
%attr(0755, root, root) %{postfix_command_dir}/smtp-source
%attr(0755, root, root) %{postfix_command_dir}/posttls-finger

%attr(0755, root, root) %{postfix_command_dir}/postalias
%attr(0755, root, root) %{postfix_command_dir}/postcat
%attr(0755, root, root) %{postfix_command_dir}/postconf
%attr(2755, root, %{maildrop_group}) %{postfix_command_dir}/postdrop
%attr(0755, root, root) %{postfix_command_dir}/postfix
%attr(0755, root, root) %{postfix_command_dir}/postkick
%attr(0755, root, root) %{postfix_command_dir}/postlock
%attr(0755, root, root) %{postfix_command_dir}/postlog
%attr(0755, root, root) %{postfix_command_dir}/postmap
%attr(0755, root, root) %{postfix_command_dir}/postmulti
%attr(2755, root, %{maildrop_group}) %{postfix_command_dir}/postqueue
%attr(0755, root, root) %{postfix_command_dir}/postsuper
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/access
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/canonical
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/generic
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/header_checks
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/main.cf
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/main.cf.proto
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/master.cf
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/master.cf.proto
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/relocated
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/transport
%attr(0644, root, root) %config(noreplace) %{postfix_config_dir}/virtual
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf
%attr(0755, root, root) %{postfix_daemon_dir}/[^mp]*
%attr(0755, root, root) %{postfix_daemon_dir}/master
%attr(0755, root, root) %{postfix_daemon_dir}/pickup
%attr(0755, root, root) %{postfix_daemon_dir}/pipe
%attr(0755, root, root) %{postfix_daemon_dir}/post-install
%attr(0644, root, root) %{postfix_config_dir}/postfix-files
%attr(0755, root, root) %{postfix_daemon_dir}/postfix-script
%attr(0755, root, root) %{postfix_daemon_dir}/postfix-tls-script
%attr(0755, root, root) %{postfix_daemon_dir}/postfix-wrapper
%attr(0755, root, root) %{postfix_daemon_dir}/postmulti-script
%attr(0755, root, root) %{postfix_daemon_dir}/postscreen
%attr(0755, root, root) %{postfix_daemon_dir}/postlogd
%attr(0755, root, root) %{postfix_daemon_dir}/proxymap
%attr(0755, root, root) %{postfix_shlib_dir}/libpostfix-*.so
%{_bindir}/mailq.postfix
%{_bindir}/newaliases.postfix
%attr(0755, root, root) %{_bindir}/rmail.postfix
%attr(0755, root, root) %{_sbindir}/sendmail.postfix
%{_libdir}/sendmail.postfix

%ghost %{_sysconfdir}/pam.d/smtp

%ghost %{_mandir}/man1/mailq.1.gz
%ghost %{_mandir}/man1/newaliases.1.gz
%ghost %{_mandir}/man5/aliases.5.gz
%ghost %{_mandir}/man8/sendmail.8.gz
%ghost %{_mandir}/man8/smtpd.8.gz

%ghost %attr(0755, root, root) %{_bindir}/mailq
%ghost %attr(0755, root, root) %{_bindir}/newaliases
%ghost %attr(0755, root, root) %{_bindir}/rmail
%ghost %attr(0755, root, root) %{_sbindir}/sendmail
%ghost %attr(0755, root, root) %{_libdir}/sendmail

%ghost %attr(0644, root, root) %{_sharedstatedir}/misc/postfix.aliasesdb-stamp

%files perl-scripts
%attr(0755, root, root) %{postfix_command_dir}/qshape
%attr(0644, root, root) %{_mandir}/man1/qshape*
%if %{with pflogsumm}
%doc %{postfix_doc_dir}/pflogsumm-faq.txt
%attr(0644, root, root) %{_mandir}/man1/pflogsumm.1.gz
%attr(0755, root, root) %{postfix_command_dir}/pflogsumm
%endif

%if %{with mysql}
%files mysql
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/mysql
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/mysql
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-mysql.so
%attr(0644, root, root) %{_mandir}/man5/mysql_table.5*
%attr(0644, root, root) %{postfix_doc_dir}/README_FILES/MYSQL_README

%endif

%if %{with pgsql}
%files pgsql
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/pgsql
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/pgsql
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-pgsql.so
%attr(0644, root, root) %{_mandir}/man5/pgsql_table.5*
%attr(0644, root, root) %{postfix_doc_dir}/README_FILES/PGSQL_README
%endif

%if %{with sqlite}
%files sqlite
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/sqlite
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/sqlite
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-sqlite.so
%attr(0644, root, root) %{_mandir}/man5/sqlite_table.5*
%attr(0644, root, root) %{postfix_doc_dir}/README_FILES/SQLITE_README
%endif

%if %{with cdb}
%files cdb
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/cdb
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/cdb
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-cdb.so
%attr(0644, root, root) %{postfix_doc_dir}/README_FILES/CDB_README
%endif

%if %{with ldap}
%files ldap
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/ldap
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/ldap
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-ldap.so
%attr(0644, root, root) %{_mandir}/man5/ldap_table.5*
%attr(0644, root, root) %{postfix_doc_dir}/README_FILES/LDAP_README
%endif

%if %{with lmdb}
%files lmdb
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/lmdb
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/lmdb
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-lmdb.so
%attr(0644, root, root) %{_mandir}/man5/lmdb_table.5*
%attr(0644, root, root) %{postfix_doc_dir}/README_FILES/LMDB_README
%endif

%if %{with pcre}
%files pcre
%attr(0644, root, root) %{postfix_config_dir}/dynamicmaps.cf.d/pcre
%attr(0644, root, root) %{postfix_config_dir}/postfix-files.d/pcre
%attr(0755, root, root) %{postfix_shlib_dir}/postfix-pcre.so
%attr(0644, root, root) %{_mandir}/man5/pcre_table.5*
%attr(0644, root, root) %{postfix_doc_dir}/README_FILES/PCRE_README
%endif

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.7.0-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Feb 07 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.7.0-1
- Updating to version 3.7.0.
- License verified.

* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 3.5.7-4
- Remove epoch

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2:3.5.7-3
- Making binaries paths compatible with CBL-Mariner's paths.

* Wed Nov 04 2020 Joe Schmitt <joschmit@microsoft.com> - 2:3.5.7-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Drop sysvinit integration.
- Add understated dependency on perl(Date::Calc).

* Mon Aug 31 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.7-1
- New version
  Resolves: rhbz#1873857

* Thu Aug  6 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.6-2
- Minor spec cleanup
- Added posttls-finger test tool
  Resolves: rhbz#1865701

* Tue Jul 28 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.6-1
- New version
  Resolves: rhbz#1860547

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 2:3.5.4-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Jul  8 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.4-2
- Added support for LMDB maps

* Mon Jun 29 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.4-1
- New version
  Resolves: rhbz#1851650

* Mon Jun 15 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.3-1
- New version
  Resolves: rhbz#1846939

* Tue May 19 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.2-1
- New version
  Resolves: rhbz#1836653

* Fri May 15 2020 Pete Walter <pwalter@fedoraproject.org> - 2:3.5.1-2
- Rebuild for ICU 67

* Mon Apr 20 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.1-1
- New version
  Resolves: rhbz#1825547

* Mon Mar 16 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.5.0-1
- New version
  Resolves: rhbz#1813740

* Thu Mar 12 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.10-1
- New version
  Resolves: rhbz#1812987

* Mon Feb  3 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.9-1
- New version
  Resolves: rhbz#1797383
- Dropped ref-search patch (upstreamed)
- Built with -fcommon to overcome FTBFS with gcc-10, problem reported upstream

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Dec 16 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.8-2
- Fixed DNS resolver to use ref_search instead of ref_query
  Resolves: rhbz#1723950

* Mon Nov 25 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.8-1
- New version
  Resolves: rhbz#1776033

* Fri Nov 01 2019 Pete Walter <pwalter@fedoraproject.org> - 2:3.4.7-3
- Rebuild for ICU 65

* Wed Sep 25 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.7-2
- Added hostname as explicit requirement for the post scriptlet

* Mon Sep 23 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.7-1
- New version
  Resolves: rhbz#1754198

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jul  8 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.6-1
- New version
  Resolves: rhbz#1726462

* Fri May  3 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.4-4
- Fixed FTBFS with new glibc due to dropped RES macros

* Fri May  3 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.4-3
- Added findutils as explicit requirement
  Resolves: rhbz#1629057

* Tue Mar 26 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.4-2
- Fixed example chroot-update script
  Resolves: rhbz#1398910

* Fri Mar 15 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.4-1
- New version
  Resolves: rhbz#1689029

* Mon Mar 11 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.3-1
- New version
  Resolves: rhbz#1687208

* Fri Mar  8 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.1-1
- New version
  Resolves: rhbz#1686673

* Fri Mar  1 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.4.0-1
- New version
  Resolves: rhbz#1683855

* Wed Feb 27 2019 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.3.3-1
- New version
  Resolves: rhbz#1683487

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.3.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 23 2019 Pete Walter <pwalter@fedoraproject.org> - 2:3.3.1-8
- Rebuild for ICU 63

* Mon Dec  3 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.3.1-7
- Fixed posttls-finger to work with unix domains

* Mon Nov 19 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.3.1-6
- Used _prefix macro for /usr and _includedir macro for /usr/include

* Mon Aug 20 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.3.1-5
- Added m4 to BuildRequires
  Resolves: rhbz#1619111

* Tue Jul 24 2018 Robert Scheck <robert@fedoraproject.org> - 2:3.3.1-4
- Add basic postfix TLS configuration by default (#1608050)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.3.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Pete Walter <pwalter@fedoraproject.org> - 2:3.3.1-2
- Rebuild for ICU 62

* Mon Jul  9 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.3.1-1
- New version
  Resolves: rhbz#1548222
- Updated libnsl2 library and header paths
  Resolves: rhbz#1543928
- Updated license for dual licensing

* Mon Apr 30 2018 Pete Walter <pwalter@fedoraproject.org> - 2:3.2.5-5
- Rebuild for ICU 61.1

* Mon Feb 26 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.5-4
- Owned /usr/lib64/postfix directory
  Resolves: rhbz#1548686

* Mon Feb 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 2:3.2.5-3
- Add gcc to BuildRequires

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.5-1
- New version
  Resolves: rhbz#1539465
- Switched to libnsl2, because nsl is no longer provided by glibc
- Macro workaround not to check symbols during compilation, because
  plugins have symbols which are unresolvable during compile time

* Thu Nov 30 2017 Pete Walter <pwalter@fedoraproject.org> - 2:3.2.4-3
- Rebuild for ICU 60.1

* Thu Nov  2 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.4-2
- Used mariadb-connector-c-devel instead of mysql-devel
  Resolves: rhbz#1493655

* Wed Nov  1 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.4-1
- New version
  Resolves: rhbz#1508234

* Thu Oct  5 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.3-1
- New version
  Resolves: rhbz#1495033

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.2-1
- New version
  Resolves: rhbz#1461224

* Tue Jun 13 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.1-1
- New version
  Resolves: rhbz#1460474
- Updated pflogsumm to 1.1.5
- Fixed warnings if IPv6 addresses are in the log
  Resolves: rhbz#1384871

* Thu Mar  2 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.2.0-1
- New version
  Resolves: rhbz#1427860
- De-fuzzified patches
- Dropped timestamps patch (upstreamed)

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan  2 2017 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.1.4-1
- New version
  Resolves: rhbz#1409447

* Wed Oct 5 2016 Ondřej Lysoněk <olysonek@redhat.com> - 2:3.1.3-2
- Preserve timestamps during 'make install'
  Resolves: rhbz#1307064

* Mon Oct  3 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.1.3-1
- New version
  Resolves: rhbz#1381077

* Wed Aug 31 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.1.2-1
- New version
  Resolves: rhbz#1370899
- Dropped timestamps patch (upstream rejected)
- Fixed minor whitespace problem

* Thu Aug 04 2016 Ondřej Lysoněk <olysonek@redhat.com> - 2:3.1.1-3
- Preserve timestamps during 'make install'
  Patch provided by Robert Scheck
  Resolves: rhbz#1307064

* Wed Jun 29 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.1.1-2
- Hardened systemd unit file
  Resolves: rhbz#1350941

* Mon May 16 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.1.1-1
- New version
  Resolves: rhbz#1336245

* Fri Apr 15 2016 David Tardon <dtardon@redhat.com> - 2:3.1.0-2
- rebuild for ICU 57.1

* Thu Feb 25 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.1.0-1
- New version
  Resolves: rhbz#1311968
- Defuzzified files, large-fs, and alternatives patches

* Mon Feb 22 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.4-1
- New version
  Resolves: rhbz#1310481

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:3.0.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.3-4
- Increased alternatives priority, it is desirable to prefer postfix
  to e.g. ssmtp
  Resolves: rhbz#1255131

* Mon Jan 11 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.3-3
- Added support for installation with _excludedocs
  Resolves: rhbz#1227824

* Wed Oct 28 2015 David Tardon <dtardon@redhat.com> - 2:3.0.3-2
- rebuild for ICU 56.1

* Mon Oct 12 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.3-1
- New version
  Resolves: rhbz#1270577
- Dropped reset-errno-before-readdir patch (upstreamed)

* Mon Sep 14 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.2-2
- Fixed sysvinit conditionals

* Wed Jul 22 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.2-1
- New version
  Resolves: rhbz#1245183
- Dropped linux4 patch (not needed)
- Defuzzified alternatives patch

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Apr 26 2015 Dodji Seketeli <dodji@seketeli.org> - 2:3.0.1-2
- Avoid spurious errors by re-setting errno to 0 before calling that readdir()
  Resolves: rhbz#1204139
- Add a patch to support compiling on Linux 4.*

* Mon Apr 13 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.1-1
- New version

* Tue Mar 24 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.0-5
- Overriden DEF_SHLIB_DIR according to build host
  Resolves: rhbz#1202921

* Fri Mar 13 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.0-4
- Switched to dynamically loaded libraries and database plugins
- Enabled PostgreSQL support by default
- Added SQLite support
- Added CDB support

* Fri Mar 13 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.0-3
- Rebuilt with libicu for SMTPUTF8

* Tue Mar 10 2015 Adam Jackson <ajax@redhat.com> 2:3.0.0-2
- Drop sysvinit subpackage in F23+

* Thu Mar  5 2015 Jaroslav Škarvada <jskarvad@redhat.com> - 2:3.0.0-1
- New version
  Resolves: rhbz#1190797
- Defuzzified alternatives, config, large-fs patches
- Rebased files patch

* Mon Oct 20 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.11.3-1
- New version
  Resolves: rhbz#1154587

* Tue Oct 14 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.11.2-1
- New version
  Resolves: rhbz#1152488

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May  9 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.11.1-1
- New version
  Resolves: rhbz#1095655

* Fri Mar 28 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.11.0-2
- Added man8/smtpd.8.gz to alternatives
  Resolves: rhbz#1051180

* Wed Feb 12 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.11.0-1
- New version
  Resolves: rhbz#1054116
- Updated / de-fuzzified patches
- Compiled with USE_LDAP_SASL if both "ldap" and "sasl" options are enabled.
  Patch provided by Davide Principi <davide.principi@nethesis.it>
  Resolves: rhbz#1052958

* Thu Jan  2 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.2-3
- Rebuilt regarding ECDHE

* Wed Oct 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.2-2
- Rebuilt against ECDHE enabled openssl
  Resolves: rhbz#1019254

* Mon Sep 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.2-1
- New version
  Resolves: rhbz#1006005
- Defuzzified patches

* Mon Aug 12 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.1-7
- Minor changes to macros regarding hardened build

* Tue Aug  6 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.1-6
- Fixed license (pflogsumm)

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2:2.10.1-5
- Perl 5.18 rebuild

* Fri Jul 26 2013 Ville Skyttä <ville.skytta@iki.fi> - 2:2.10.1-4
- Install docs to %%{_pkgdocdir} where available.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2:2.10.1-3
- Perl 5.18 rebuild

* Thu Jul  4 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.1-2
- Added diffutils as explicit requirement
  Resolves: rhbz#830540

* Mon Jun 24 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.1-1
- New version
  Resolves: rhbz#977273

* Thu May 23 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.0-2
- Fixed systemd error message regarding chroot-update, patch provided
  by John Heidemann <johnh@isi.edu>
  Resolves: rhbz#917463

* Thu Mar 21 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.0-1
- New version
- Re-enabled IPv6 in the config
  Resolves: rhbz#863140

* Tue Feb 26 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.0-0.3.rc1
- Added systemd-sysv to requires

* Mon Feb 25 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.0-0.2.rc1
- Switched to systemd-rpm macros
  Resolves: rhbz#850276

* Fri Feb  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.10.0-0.1.rc1
- New version

* Tue Feb  5 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.6-1
- New version
  Resolves: rhbz#907803

* Tue Jan  8 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.5-2
- Rebuilt with -fno-strict-aliasing

* Thu Dec 13 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.5-1
- New version
  Resolves: rhbz#886804

* Thu Sep  6 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.4-3
- Fixed systemd error message about missing chroot-update
  Resolves: rhbz#832742

* Fri Aug  3 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.4-2
- Fixed sysv2systemd upgrade from f16

* Thu Aug  2 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.4-1
- New version
  Resolves: rhbz#845298
- Dropped biff-cloexec patch (upstreamed)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jul 03 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.3-2
- Fixed FD leak in biff

* Tue Jun  5 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.3-1
- New version
  Resolves: rhbz#828242
  Fixed sysv2systemd upgrade from f16

* Wed Apr 25 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.2-2
- Fixed sysv2systemd upgrade from f15 / f16

* Wed Apr 25 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.2-1
- New version
  Resolves: rhbz#816139

* Fri Apr  6 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.1-2
- Rebuilt with libdb-5.2

* Mon Feb 20 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.1-1
- New version
  Resolves: rhbz#794976

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2:2.9.0-2
- Rebuild against PCRE 8.30

* Fri Feb  3 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.9.0-1
- New version
  Resolves: rhbz#786792

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.8.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Nov 10 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.7-4
- Added epoch to sysvinit subpackage requires

* Tue Nov  8 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.7-3
- Fixed sysvinit preun scriptlet

* Tue Nov  8 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.7-2
- Introduce systemd unit file, thanks to Jóhann B. Guðmundsson <johannbg@hi.is>
  Resolves: rhbz#718793

* Mon Nov  7 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.7-1
- Update to 2.8.7
  Resolves: rhbz#751622

* Mon Oct 24 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.6-1
- Update to 2.8.6
  Resolves: rhbz#748389

* Mon Sep 12 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.5-1
- Update to 2.8.5
  Resolves: rhbz#735543

* Tue Aug 30 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.4-4
- Enable override of hardened build settings

* Tue Aug 30 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.4-3
- Hardened build, rebuilt with full relro

* Tue Aug 30 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.4-2
- Rebuilt with libdb-5.1
  Resolves: rhbz#734084

* Thu Jul 07 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.4-1
- update to 2.8.4

* Mon May 09 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.3-1
- update to 2.8.3
- fix CVE-2011-1720

* Wed Mar 23 2011 Dan Horák <dan@danny.cz> - 2:2.8.2-2
- rebuilt for mysql 5.5.10 (soname bump in libmysqlclient)

* Tue Mar 22 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 2:2.8.2-1
- update to 2.8.2

* Wed Feb 23 2011 Miroslav Lichvar <mlichvar@redhat.com> 2:2.8.1-1
- update to 2.8.1

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Miroslav Lichvar <mlichvar@redhat.com> 2:2.8.0-2
- don't set config_directory when upgrading configuration (#675654)

* Wed Jan 26 2011 Miroslav Lichvar <mlichvar@redhat.com> 2:2.8.0-1
- update to 2.8.0

* Fri Nov 26 2010 Miroslav Lichvar <mlichvar@redhat.com> 2:2.7.2-1
- update to 2.7.2
- change LSB init header to provide $mail-transport-agent (#627411)

* Thu Jun 10 2010 Miroslav Lichvar <mlichvar@redhat.com> 2:2.7.1-1
- update to 2.7.1
- update pflogsumm to 1.1.3

* Wed Mar 17 2010 Miroslav Lichvar <mlichvar@redhat.com> 2:2.7.0-2
- follow guidelines for alternatives (#570801)
- move sasl config to /etc/sasl2 (#574434)
- drop sasl v1 support
- remove unnecessary requirements
- use bcond macros

* Fri Feb 26 2010 Miroslav Lichvar <mlichvar@redhat.com> 2:2.7.0-1
- update to 2.7.0

* Fri Jan 29 2010 Miroslav Lichvar <mlichvar@redhat.com> 2:2.6.5-3
- fix init script LSB compliance (#528151)
- update pflogsumm to 1.1.2
- require Date::Calc for pflogsumm (#536678)
- fix some rpmlint warnings

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.6.5-2
- use password-auth common PAM configuration instead of system-auth

* Tue Sep 01 2009 Miroslav Lichvar <mlichvar@redhat.com> 2:2.6.5-1
- update to 2.6.5

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 2:2.6.2-3
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 18 2009 Miroslav Lichvar <mlichvar@redhat.com> 2:2.6.2-1
- update to 2.6.2

* Tue May 26 2009 Miroslav Lichvar <mlichvar@redhat.com> 2:2.6.1-1
- update to 2.6.1
- move non-config files out of /etc/postfix (#490983)
- fix multilib conflict in postfix-files (#502211)
- run chroot-update script in init script (#483186)
- package examples (#251677)
- provide all alternatives files
- suppress postfix output in post script

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.5.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 23 2009 Miroslav Lichvar <mlichvar@redhat.com> 2:2.5.6-2
- rebuild for new mysql

* Thu Jan 22 2009 Miroslav Lichvar <mlichvar@redhat.com> 2:2.5.6-1
- update to 2.5.6 (#479108)
- rebuild /etc/aliases.db only when necessary (#327651)
- convert doc files to UTF-8

* Thu Nov 20 2008 Miroslav Lichvar <mlichvar@redhat.com> 2:2.5.5-2
- enable Large file support on 32-bit archs (#428996)
- fix mailq(1) and newaliases(1) man pages (#429501)
- move pflogsumm and qshape to -perl-scripts subpackage (#467529)
- update pflogsumm to 1.1.1
- fix large-fs patch
- drop open_define patch
- add -Wno-comment to CFLAGS

* Wed Sep 17 2008 Thomas Woerner <twoerner@redhat.com> 2:2.5.5-1
- new version 2.5.5
  fixes CVE-2008-2936, CVE-2008-2937 and CVE-2008-3889 (rhbz#459101)

* Thu Aug 28 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2:2.5.1-4
- fix license tag

* Thu Aug 14 2008 Thomas Woerner <twoerner@redhat.com> 2:2.5.1-3
- fixed postfix privilege problem with symlinks in the mail spool directory
  (CVE-2008-2936) (rhbz#459101)

* Wed Mar 12 2008 Thomas Woerner <twoerner@redhat.com> 2:2.5.1-2
- fixed fix for enabling IPv6 support (rhbz#437024)
- added new postfix data directory (rhbz#437042)

* Thu Feb 21 2008 Thomas Woerner <twoerner@redhat.com> 2:2.5.1-1
- new verison 2.5.1

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2:2.4.6-3
- Autorebuild for GCC 4.3

* Thu Dec 06 2007 Release Engineering <rel-eng at fedoraproject dot org> - 2.4.6-2
- Rebuild for deps

* Wed Nov 28 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.6-1
- new verison 2.4.6
- added virtual server(smtp) provide (rhbz#380631)
- enabling IPv6 support (rhbz#197105)
- made the MYSQL and PGSQL defines overloadable as build argument

* Wed Nov  7 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.5-3
- fixed multilib conflict for makedefs.out: rename to makedefs.out-%%{_arch}
  (rhbz#342941)
- enabled mysql support

* Thu Oct  4 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.5-2
- made init script lsb conform (#243286, rhbz#247025)
- added link to postfix sasl readme into Postfix-SASL-RedHat readme

* Mon Aug 13 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.5-1
- new version 2.4.5
- fixed compile proplem with glibc-2.6.90+

* Fri Jun 15 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.3-3
- added missing epoch in requirement of pflogsumm sub package

* Thu Jun 14 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.3-2
- diabled mysql support again (rhbz#185515)
- added support flag for PostgreSQL build (rhbz#180579)
  Ben: Thanks for the patch
- Fixed remaining rewiew problems (rhbz#226307)

* Tue Jun  5 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.3-1
- allow to build without LDAP but SASL2 support (rhbz#216792)

* Tue Jun  5 2007 Thomas Woerner <twoerner@redhat.com> 2:2.4.3-1
- new stable version 2.4.3
- enabled mysql support (rhbz#185515)
- dropped build requirements for gawk, ed and sed

* Tue Jan 23 2007 Thomas Woerner <twoerner@redhat.com> 2:2.3.6-1
- new version 2.3.6
- limiting SASL mechanisms to plain login for sasl with saslauthd (#175259)
- dropped usage of ed in the install stage

* Tue Nov  7 2006 Thomas Woerner <twoerner@redhat.com> 2:2.3.4-1
- new version 2.3.4

* Fri Sep  1 2006 Thomas Woerner <twoerner@redhat.com> 2:2.3.3-2
- fixed upgrade procedure (#202357)

* Fri Sep  1 2006 Thomas Woerner <twoerner@redhat.com> 2:2.3.3-1
- new version 2.3.3
- fixed permissions of TLS_LICENSE file

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 2:2.3.2-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Mon Jul 31 2006 Thomas Woerner <twoerner@redhat.com> 2:2.3.2-1
- new version 2.3.2 with major upstream fixes:
  - corrupted queue file after a request to modify a short message header
  - panic after spurious Milter request when a client was rejected
  - maked the Milter more tolerant for redundant "data cleanup" requests
- applying pflogsumm-conn-delays-dsn-patch from postfix tree to pflogsumm

* Fri Jul 28 2006 Thomas Woerner <twoerner@redhat.com> 2:2.3.1-1
- new version 2.3.1
- fixes problems with TLS and Milter support

* Tue Jul 25 2006 Thomas Woerner <twoerner@redhat.com> 2:2.3.0-2
- fixed SASL build (#200079)
  thanks to Kaj J. Niemi for the patch

* Mon Jul 24 2006 Thomas Woerner <twoerner@redhat.com> 2:2.3.0-1
- new version 2.3.0
- dropped hostname-fqdn patch

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2:2.2.10-2.1
- rebuild

* Wed May 10 2006 Thomas Woerner <twoerner@redhat.com> 2:2.2.10-2
- added RELRO security protection

* Tue Apr 11 2006 Thomas Woerner <twoerner@redhat.com> 2:2.2.10-1
- new version 2.2.10
- added option LDAP_DEPRECATED to support deprecated ldap functions for now
- fixed build without pflogsumm support (#188470)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2:2.2.8-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2:2.2.8-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Florian Festi <ffesti@redhat.com> 2:2.2.8-1
- new version 2.2.8

* Tue Dec 13 2005 Thomas Woerner <twoerner@redhat.com> 2:2.2.7-1
- new version 2.2.7

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 11 2005 Thomas Woerner <twoerner@redhat.com> 2:2.2.5-2.1
- replaced postconf and postalias call in initscript with newaliases (#156358)
- fixed initscripts messages (#155774)
- fixed build problems when sasl is disabled (#164773)
- fixed pre-definition of mailbox_transport lmtp socket path (#122910)

* Thu Nov 10 2005 Tomas Mraz <tmraz@redhat.com> 2:2.2.5-2
- rebuilt against new openssl

* Fri Oct  7 2005 Tomas Mraz <tmraz@redhat.com>
- use include instead of pam_stack in pam config

* Thu Sep  8 2005 Thomas Woerner <twoerner@redhat.com> 2:2.2.5-1
- new version 2.2.5

* Thu May 12 2005 Thomas Woerner <twoerner@redhat.com> 2:2.2.3-1
- new version 2.2.3
- compiling all binaries PIE, dropped old pie patch

* Wed Apr 20 2005 Tomas Mraz <tmraz@redhat.com> 2:2.2.2-2
- fix fsspace on large filesystems (>2G blocks)

* Tue Apr 12 2005 Thomas Woerner <twoerner@redhat.com> 2:2.2.2-1
- new version 2.2.2

* Fri Mar 18 2005 Thomas Woerner <twoerner@redhat.com> 2:2.2.1-1
- new version 2.2.1
- allow to start postfix without alias_database (#149657)

* Fri Mar 11 2005 Thomas Woerner <twoerner@redhat.com> 2:2.2.0-1
- new version 2.2.0
- cleanup of spec file: removed external TLS and IPV6 patches, removed 
  smtp_sasl_proto patch
- dropped samples directory till there are good examples again (was TLS and
  IPV6)
- v2.2.0 fixes code problems: #132798 and #137858

* Fri Feb 11 2005 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-5.1
- fixed open relay bug in postfix ipv6 patch: new version 1.26 (#146731)
- fixed permissions on doc directory (#147280)
- integrated fixed fqdn patch from Joseph Dunn (#139983)

* Tue Nov 23 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-4.1
- removed double quotes from postalias call, second fix for #138354

* Thu Nov 11 2004 Jeff Johnson <jbj@jbj.org> 2:2.1.5-4
- rebuild against db-4.3.21.
- remove Requires: db4, the soname linkage dependency is sufficient.

* Thu Nov 11 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-3.1
- fixed problem with multiple alias maps (#138354)

* Tue Oct 26 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-3
- fixed wrong path for cyrus-imapd (#137074)

* Mon Oct 18 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-2.2
- automated postalias call in init script
- removed postconf call from spec file: moved changes into patch

* Fri Oct 15 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-2.1
- removed aliases from postfix-files (#135840)
- fixed postalias call in init script

* Thu Oct 14 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-2
- switched over to system aliases file and database in /etc/ (#117661)
- new reuires and buildrequires for setup >= 2.5.36-1

* Mon Oct  4 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.5-1
- new version 2.1.5
- new ipv6 and tls+ipv6 patches: 1.25-pf-2.1.5

* Thu Aug  5 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.4-1
- new version 2.1.4
- new ipv6 and tls+ipv6 patches: 1.25-pf-2.1.4
- new pfixtls-0.8.18-2.1.3-0.9.7d patch

* Mon Jun 21 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.1-3.1
- fixed directory permissions in %%doc (#125406)
- fixed missing spool dirs (#125460)
- fixed verify problem for aliases.db (#125461)
- fixed bogus upgrade warning (#125628)
- more spec file cleanup

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sun Jun 06 2004 Florian La Roche <Florian.LaRoche@redhat.de>
- make sure pflog files have same permissions even if in multiple
  sub-rpms

* Fri Jun  4 2004 Thomas Woerner <twoerner@redhat.com> 2:2.1.1-1
- new version 2.1.1
- compiling postfix PIE
- new alternatives slave for /usr/lib/sendmail

* Wed Mar 31 2004 John Dennis <jdennis@redhat.com> 2:2.0.18-4
- remove version from pflogsumm subpackage, it was resetting the
  version used in the doc directory, fixes bug 119213

* Tue Mar 30 2004 Bill Nottingham <notting@redhat.com> 2:2.0.18-3
- add %%defattr for pflogsumm package

* Tue Mar 16 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.18-2
- fix sendmail man page (again), make pflogsumm a subpackage

* Mon Mar 15 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.18-1
- bring source up to upstream release 2.0.18
- include pflogsumm, fixes bug #68799
- include smtp-sink, smtp-source man pages, fixes bug #118163

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 24 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.16-14
- fix bug 74553, make alternatives track sendmail man page

* Tue Feb 24 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.16-13
- remove /etc/sysconfig/saslauthd from rpm, fixes bug 113975

* Wed Feb 18 2004 John Dennis <jdennis@porkchop.devel.redhat.com>
- set sasl back to v2 for mainline, this is good for fedora and beyond,
  for RHEL3, we'll branch and set set sasl to v1 and turn off ipv6

* Tue Feb 17 2004 John Dennis <jdennis@porkchop.devel.redhat.com>
- revert back to v1 of sasl because LDAP still links against v1 and we can't 
- bump revision for build
  have two different versions of the sasl library loaded in one load image at
  the same time. How is that possible? Because the sasl libraries have different 
  names (libsasl.so & libsasl2.so) but export the same symbols :-(
  Fixes bugs 115249 and 111767

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 21 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.16-7
- fix bug 77216, support snapshot builds

* Tue Jan 20 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.16-6
- add support for IPv6 via Dean Strik's patches, fixes bug 112491

* Tue Jan 13 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.16-4
- remove mysqlclient prereq, fixes bug 101779
- remove md5 verification override, this fixes bug 113370. Write parse-postfix-files
  script to generate explicit list of all upstream files with ownership, modes, etc.
  carefully add back in all other not upstream files, files list is hopefully
  rock solid now.

* Mon Jan 12 2004 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.16-3
- add zlib-devel build prereq, fixes bug 112822
- remove copy of resolve.conf into chroot jail, fixes bug 111923

* Tue Dec 16 2003 John Dennis <jdennis@porkchop.devel.redhat.com>
- bump release to build 3.0E errata update

* Sat Dec 13 2003 Jeff Johnson <jbj@jbj.org> 2:2.0.16-2
- rebuild against db-4.2.52.

* Mon Nov 17 2003 John Dennis <jdennis@finch.boston.redhat.com> 2:2.0.16-1
- sync up with current upstream release, 2.0.16, fixes bug #108960

* Thu Sep 25 2003 Jeff Johnson <jbj@jbj.org> 2.0.11-6
- rebuild against db-4.2.42.

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 2.0.11-5
- rebuild

* Thu Jun 26 2003 John Dennis <jdennis@finch.boston.redhat.com>
- bug 98095, change rmail.postfix to rmail for uucp invocation in master.cf

* Wed Jun 25 2003 John Dennis <jdennis@finch.boston.redhat.com>
- add missing dependency for db3/db4

* Thu Jun 19 2003 John Dennis <jdennis@finch.boston.redhat.com>
- upgrade to new 2.0.11 upstream release
- fix authentication problems
- rewrite SASL documentation
- upgrade to use SASL version 2
- Fix bugs 75439, 81913 90412, 91225, 78020, 90891, 88131

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar  7 2003 John Dennis <jdennis@finch.boston.redhat.com>
- upgrade to release 2.0.6
- remove chroot as this is now the preferred installation according to Wietse Venema, the postfix author

* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Feb 18 2003 Bill Nottingham <notting@redhat.com> 2:1.1.11-10
- don't copy winbind/wins nss modules, fixes #84553

* Sat Feb 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- sanitize rpm scripts a bit

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Sat Jan 11 2003 Karsten Hopp <karsten@redhat.de> 2:1.1.11-8
- rebuild to fix krb5.h issue

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2:1.1.11-7
- rebuild

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- if pkgconfig knows about openssl, use its cflags and linker flags

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 2:1.1.11-6
- lib64'ize
- build on all arches

* Wed Jul 24 2002 Karsten Hopp <karsten@redhat.de>
- make aliases.db config(noreplace) (#69612)

* Tue Jul 23 2002 Karsten Hopp <karsten@redhat.de>
- postfix has its own filelist, remove LICENSE entry from it (#69069)

* Tue Jul 16 2002 Karsten Hopp <karsten@redhat.de>
- fix shell in /etc/passwd (#68373)
- fix documentation in /etc/postfix (#65858)
- Provides: /usr/bin/newaliases (#66746)
- fix autorequires by changing /usr/local/bin/perl to /usr/bin/perl in a
  script in %%doc (#68852), although I don't think this is necessary anymore

* Mon Jul 15 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed missing smtpd.conf file for SASL support and included SASL Postfix
  Red Hat HOWTO (#62505).
- Included SASL2 support patch (#68800).

* Mon Jun 24 2002 Karsten Hopp <karsten@redhat.de>
- 1.1.11, TLS 0.8.11a
- fix #66219 and #66233 (perl required for %%post)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.10-1
- 1.1.10, TLS 0.8.10
- Build with db4
- Enable SASL

* Mon Apr 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.7-2
- Fix bugs #62358 and #62783
- Make sure libdb-3.3.so is in the chroot jail (#62906)

* Mon Apr  8 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.7-1
- 1.1.7, fixes 2 critical bugs
- Make sure there's a resolv.conf in the chroot jail

* Wed Mar 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.5-3
- Add Provides: lines for alternatives stuff (#60879)

* Tue Mar 26 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.5-2
- rebuild

* Tue Mar 26 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.5-1
- 1.1.5 (bugfix release)
- Rebuild with current db

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 1.1.4-3
- remove db trigger, it's both dangerous and pointless
- clean up other triggers a little

* Wed Mar 13 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.4-2
- Some trigger tweaks to make absolutely sure /etc/services is in the
  chroot jail

* Mon Mar 11 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.4-1
- 1.1.4
- TLS 0.8.4
- Move postalias run from %%post to init script to work around
  anaconda being broken.

* Fri Mar  8 2002 Bill Nottingham <notting@redhat.com> 1.1.3-5
- use alternatives --initscript support

* Thu Feb 28 2002 Bill Nottingham <notting@redhat.com> 1.1.3-4
- run alternatives --remove in %%preun
- add various prereqs

* Thu Feb 28 2002 Nalin Dahyabhai <nalin@redhat.com> 1.1.3-3
- adjust the default postfix-files config file to match the alternatives setup
  by altering the arguments passed to post-install in the %%install phase
  (otherwise, it might point to sendmail's binaries, breaking it rather rudely)
- adjust the post-install script so that it silently uses paths which have been
  modified for use with alternatives, for upgrade cases where the postfix-files
  configuration file isn't overwritten
- don't forcefully strip files -- that's a build root policy
- remove hard requirement on openldap, library dependencies take care of it
- redirect %%postun to /dev/null
- don't remove the postfix user and group when the package is removed

* Wed Feb 20 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.3-2
- listen on 127.0.0.1 only by default (#60071)
- Put config samples in %%{_docdir}/%%{name}-%%{version} rather than
  /etc/postfix (#60072)
- Some spec file cleanups

* Tue Feb 19 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.3-1
- 1.1.3, TLS 0.8.3
- Fix updating
- Don't run the statistics cron job
- remove requirement on perl Date::Calc

* Thu Jan 31 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.2-3
- Fix up alternatives stuff

* Wed Jan 30 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.2-2
- Use alternatives

* Sun Jan 27 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.1.2-1
- Initial Red Hat Linux packaging, based on spec file from
  Simon J Mudd <sjmudd@pobox.com>
- Changes from that:
  - Set up chroot environment in triggers to make sure we catch glibc errata
  - Remove some hacks to support building on all sorts of distributions at
    the cost of specfile readability
  - Remove postdrop group on deletion
