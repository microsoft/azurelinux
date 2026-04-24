# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Do we want SELinux & Audit
%if 0%{?!noselinux:1}
%global WITH_SELINUX 1
%else
%global WITH_SELINUX 0
%endif

%global _hardened_build 1

# Do we want to disable building of gnome-askpass? (1=yes 0=no)
%global no_gnome_askpass 0

# Do we want to link against a static libcrypto? (1=yes 0=no)
%global static_libcrypto 0

# Use GTK3 instead of GTK2 in gnome-ssh-askpass
%global gtk3 1

# Build position-independent executables (requires toolchain support)?
%global pie 1

# Do we want kerberos5 support (1=yes 0=no)
%global kerberos5 1

# Do we want libedit support
%global libedit 1

# Reserve options to override askpass settings with:
# rpm -ba|--rebuild --define 'skip_xxx 1'
%{?skip_gnome_askpass:%global no_gnome_askpass 1}

# Add option to build without GTK2 for older platforms with only GTK+.
# Red Hat Linux <= 7.2 and Red Hat Advanced Server 2.1 are examples.
# rpm -ba|--rebuild --define 'no_gtk3 1'
%{?no_gtk3:%global gtk3 0}

# Options for static OpenSSL link:
# rpm -ba|--rebuild --define "static_openssl 1"
%{?static_openssl:%global static_libcrypto 1}

%global openssh_ver 10.0p1

Summary: An open source implementation of SSH protocol version 2
Name: openssh
Version: %{openssh_ver}
Release: 7%{?dist}
URL: http://www.openssh.com/portable.html
Source0: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz
Source1: ftp://ftp.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-%{version}.tar.gz.asc
Source2: sshd.pam
Source3: gpgkey-736060BA.gpg
Source6: ssh-keycat.pam
Source7: sshd.sysconfig
Source9: sshd@.service
Source10: sshd.socket
Source11: sshd.service
Source12: sshd-keygen@.service
Source13: sshd-keygen
Source15: sshd-keygen.target
Source16: ssh-agent.service
Source17: ssh-agent.socket
Source19: openssh-server-systemd-sysusers.conf
Source20: ssh-host-keys-migration.sh
Source21: ssh-host-keys-migration.service
Source22: parallel_test.sh
Source23: parallel_test.Makefile

#https://bugzilla.mindrot.org/show_bug.cgi?id=1641 (WONTFIX)
Patch0001: 0001-openssh-7.8p1-role-mls.patch
#https://bugzilla.redhat.com/show_bug.cgi?id=781634
Patch0002: 0002-openssh-6.6p1-privsep-selinux.patch
Patch0003: 0003-openssh-6.6p1-keycat.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1644
Patch0004: 0004-openssh-6.6p1-allow-ip-opts.patch
#(drop?) https://bugzilla.mindrot.org/show_bug.cgi?id=1925
Patch0005: 0005-openssh-5.9p1-ipv6man.patch
Patch0006: 0006-openssh-5.8p2-sigpipe.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1789
Patch0007: 0007-openssh-7.2p2-x11.patch
Patch0008: 0008-openssh-5.1p1-askpass-progress.patch
#https://bugzilla.redhat.com/show_bug.cgi?id=198332
Patch0009: 0009-openssh-4.3p2-askpass-grab-info.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1635 (WONTFIX)
Patch0010: 0010-openssh-8.7p1-redhat.patch
# warn users for unsupported UsePAM=no (#757545)
Patch0011: 0011-openssh-7.8p1-UsePAM-warning.patch
# GSSAPI Key Exchange (RFC 4462 + RFC 8732)
# from https://github.com/openssh-gsskex/openssh-gsskex/tree/fedora/master
# and
# Reenable MONITOR_REQ_GSSCHECKMIC after gssapi-with-mic failures
# upstream MR:
# https://github.com/openssh-gsskex/openssh-gsskex/pull/21
Patch0012: 0012-openssh-9.6p1-gssapi-keyex.patch
#http://www.mail-archive.com/kerberos@mit.edu/msg17591.html
Patch0013: 0013-openssh-6.6p1-force_krb.patch
# Improve ccache handling in openssh (#991186, #1199363, #1566494)
# https://bugzilla.mindrot.org/show_bug.cgi?id=2775
Patch0014: 0014-openssh-7.7p1-gssapi-new-unique.patch
# Respect k5login_directory option in krk5.conf (#1328243)
Patch0015: 0015-openssh-7.2p2-k5login_directory.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1780
Patch0016: 0016-openssh-6.6p1-kuserok.patch
# Use tty allocation for a remote scp (#985650)
Patch0017: 0017-openssh-6.4p1-fromto-remote.patch
# privsep_preauth: use SELinux context from selinux-policy (#1008580)
Patch0018: 0018-openssh-6.6.1p1-selinux-contexts.patch
# log via monitor in chroots without /dev/log (#2681)
Patch0019: 0019-openssh-6.6.1p1-log-in-chroot.patch
# scp file into non-existing directory (#1142223)
Patch0020: 0020-openssh-6.6.1p1-scp-non-existing-directory.patch
# add new option GSSAPIEnablek5users and disable using ~/.k5users by default (#1169843)
# CVE-2014-9278
Patch0021: 0021-openssh-6.6p1-GSSAPIEnablek5users.patch
# apply upstream patch and make sshd -T more consistent (#1187521)
Patch0022: 0022-openssh-6.8p1-sshdT-output.patch
# Add sftp option to force mode of created files (#1191055)
Patch0023: 0023-openssh-6.7p1-sftp-force-permission.patch
# make s390 use /dev/ crypto devices -- ignore closefrom
Patch0024: 0024-openssh-7.2p2-s390-closefrom.patch
# Move MAX_DISPLAYS to a configuration option (#1341302)
Patch0025: 0025-openssh-7.3p1-x11-max-displays.patch
# Pass inetd flags for SELinux down to openbsd compat level
Patch0026: 0026-openssh-7.6p1-cleanup-selinux.patch
# Sandbox adjustments for s390 and audit
Patch0027: 0027-openssh-7.5p1-sandbox.patch
# PKCS#11 URIs (upstream #2817, 2nd iteration)
# https://github.com/Jakuje/openssh-portable/commits/jjelen-pkcs11
# git show > ~/devel/fedora/openssh/openssh-8.0p1-pkcs11-uri.patch
Patch0028: 0028-openssh-8.0p1-pkcs11-uri.patch
# Unbreak scp between two IPv6 hosts (#1620333)
Patch0029: 0029-openssh-7.8p1-scp-ipv6.patch
# Mention crypto-policies in manual pages (#1668325)
# clarify rhbz#2068423 on the man page of ssh_config
Patch0030: 0030-openssh-8.0p1-crypto-policies.patch
# Use OpenSSL KDF (#1631761)
Patch0031: 0031-openssh-8.0p1-openssl-kdf.patch
# sk-dummy.so built with -fvisibility=hidden does not work
Patch0032: 0032-openssh-8.2p1-visibility.patch
# Do not break X11 without IPv6
Patch0033: 0033-openssh-8.2p1-x11-without-ipv6.patch
# sshd provides PAM an incorrect error code (#1879503)
Patch0034: 0034-openssh-8.0p1-preserve-pam-errors.patch
# Implement kill switch for SCP protocol
Patch0035: 0035-openssh-8.7p1-scp-kill-switch.patch
# Workaround for lack of sftp_realpath in older versions of RHEL
# https://bugzilla.redhat.com/show_bug.cgi?id=2038854
# https://github.com/openssh/openssh-portable/pull/299
# downstream only
Patch0036: 0036-openssh-8.7p1-recursive-scp.patch
# Downstream alias for MinRSABits
Patch0037: 0037-openssh-8.7p1-minrsabits.patch
# downstream only, IBMCA tentative fix
# From https://bugzilla.redhat.com/show_bug.cgi?id=1976202#c14
Patch0038: 0038-openssh-8.7p1-ibmca.patch
#https://bugzilla.mindrot.org/show_bug.cgi?id=1402
# https://bugzilla.redhat.com/show_bug.cgi?id=1171248
# record pfs= field in CRYPTO_SESSION audit event
Patch0039: 0039-openssh-7.6p1-audit.patch
# Audit race condition in forked child (#1310684)
Patch0040: 0040-openssh-7.1p2-audit-race-condition.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2049947
Patch0041: 0041-openssh-9.0p1-audit-log.patch
Patch0042: 0042-openssh-7.7p1-fips.patch
# Add missing options from ssh_config into ssh manpage
# upstream bug:
# https://bugzilla.mindrot.org/show_bug.cgi?id=3455
Patch0043: 0043-openssh-8.7p1-ssh-manpage.patch
# Don't propose disallowed algorithms during hostkey negotiation
# upstream MR:
# https://github.com/openssh/openssh-portable/pull/323
Patch0044: 0044-openssh-8.7p1-negotiate-supported-algs.patch
Patch0045: 0045-openssh-9.0p1-evp-fips-kex.patch
Patch0046: 0046-openssh-8.7p1-nohostsha1proof.patch
Patch0047: 0047-openssh-9.6p1-pam-rhost.patch
Patch0048: 0048-openssh-9.9p1-separate-keysign.patch
Patch0049: 0049-openssh-9.9p1-openssl-mlkem.patch
# https://www.openwall.com/lists/oss-security/2025/02/22/1
Patch0050: 0050-openssh-9.9p2-error_processing.patch
# https://github.com/openssh/openssh-portable/pull/564
Patch0051: 0051-Provide-better-error-for-non-supported-private-keys.patch
# https://github.com/openssh/openssh-portable/pull/567
Patch0052: 0052-Ignore-bad-hostkeys-in-known_hosts-file.patch
# https://github.com/openssh/openssh-portable/pull/500
Patch0053: 0053-support-authentication-indicators-in-GSSAPI.patch

#https://bugzilla.mindrot.org/show_bug.cgi?id=2581
Patch1000: 1000-openssh-coverity.patch

License: BSD-3-Clause AND BSD-2-Clause AND ISC AND SSH-OpenSSH AND ssh-keyscan AND sprintf AND LicenseRef-Fedora-Public-Domain AND X11-distribute-modifications-variant
Requires: /sbin/nologin
Requires: openssl-libs >= 3.5.0

%if ! %{no_gnome_askpass}
BuildRequires: libX11-devel
%if %{gtk3}
BuildRequires: gtk3-devel
%else
BuildRequires: gtk2-devel
%endif
%endif

BuildRequires: autoconf, automake, perl-interpreter, perl-generators, zlib-devel
BuildRequires: audit-libs-devel >= 2.0.5
BuildRequires: util-linux, groff
BuildRequires: pam-devel
BuildRequires: openssl-devel >= 3.5.0
BuildRequires: perl-podlators
BuildRequires: systemd-devel
BuildRequires: systemd-rpm-macros
BuildRequires: gcc make
BuildRequires: p11-kit-devel
BuildRequires: libfido2-devel
BuildRequires: libxcrypt-devel
Recommends: p11-kit
Obsoletes: openssh-ldap < 8.3p1-4
Obsoletes: openssh-cavs < 8.4p1-5

%if %{kerberos5}
BuildRequires: krb5-devel
%endif

%if %{libedit}
BuildRequires: libedit-devel ncurses-devel
%endif

%if %{WITH_SELINUX}
Requires: libselinux >= 2.3-5
BuildRequires: libselinux-devel >= 2.3-5
Requires: audit-libs >= 1.0.8
BuildRequires: audit-libs >= 1.0.8
%endif

BuildRequires: xauth
# for tarball signature verification
BuildRequires: gnupg2

%package clients
Summary: An open source SSH client applications
Requires: openssh = %{version}-%{release}
Requires: crypto-policies >= 20220824-1

%package keysign
Summary: A helper program used for host-based authentication
Requires: openssh = %{version}-%{release}

%package server
Summary: An open source SSH server daemon
Requires: openssh = %{version}-%{release}
Requires(pre): /usr/sbin/useradd
Requires: pam >= 1.0.1-3
Requires: crypto-policies >= 20220824-1
%{?systemd_requires}

%package keycat
Summary: A mls keycat backend for openssh
Requires: openssh = %{version}-%{release}

%package askpass
Summary: A passphrase dialog for OpenSSH and X
Requires: openssh = %{version}-%{release}

%package sk-dummy
Summary: OpenSSH SK driver for test purposes
Requires: openssh = %{version}-%{release}

%description
SSH (Secure SHell) is a program for logging into and executing
commands on a remote machine. SSH is intended to replace rlogin and
rsh, and to provide secure encrypted communications between two
untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's version of the last free version of SSH, bringing
it up to date in terms of security and features.

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.

%description clients
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package includes
the clients necessary to make encrypted connections to SSH servers.

%description keysign
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. ssh-keysign is a
helper program used for host-based authentication disabled by default.

%description server
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
the secure shell daemon (sshd). The sshd daemon allows SSH clients to
securely connect to your SSH server.

%description keycat
OpenSSH mls keycat is backend for using the authorized keys in the
openssh in the mls mode.

%description askpass
OpenSSH is a free version of SSH (Secure SHell), a program for logging
into and executing commands on a remote machine. This package contains
an X11 passphrase dialog for OpenSSH.

%description sk-dummy
This package contains a test SK driver used for OpenSSH test purposes

%prep
gpgv2 --quiet --keyring %{SOURCE3} %{SOURCE1} %{SOURCE0}
%autosetup -T -b 0 -p1

autoreconf

%build
%set_build_flags
%if %{pie}
%ifarch s390 s390x sparc sparcv9 sparc64
CFLAGS="$CFLAGS -fPIC"
%else
CFLAGS="$CFLAGS -fpic"
%endif
SAVE_LDFLAGS="$LDFLAGS"
LDFLAGS="$LDFLAGS -pie -z relro -z now"

export CFLAGS
export LDFLAGS

%endif
%if %{kerberos5}
if test -r /etc/profile.d/krb5-devel.sh ; then
	source /etc/profile.d/krb5-devel.sh
fi
krb5_prefix=`krb5-config --prefix`
if test "$krb5_prefix" != "%{_prefix}" ; then
	CPPFLAGS="$CPPFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I${krb5_prefix}/include -I${krb5_prefix}/include/gssapi"
	LDFLAGS="$LDFLAGS -L${krb5_prefix}/%{_lib}"; export LDFLAGS
else
	krb5_prefix=
	CPPFLAGS="-I%{_includedir}/gssapi"; export CPPFLAGS
	CFLAGS="$CFLAGS -I%{_includedir}/gssapi"
fi
%endif

%configure \
	--sysconfdir=%{_sysconfdir}/ssh \
	--libexecdir=%{_libexecdir}/openssh \
	--datadir=%{_datadir}/openssh \
	--with-default-path=/usr/local/bin:/usr/bin \
	--with-superuser-path=/usr/local/bin:/usr/bin \
	--with-privsep-path=%{_datadir}/empty.sshd \
	--disable-strip \
	--without-zlib-version-check \
	--with-ipaddr-display \
	--with-pie=no \
	--without-hardening `# The hardening flags are configured by system` \
	--with-systemd \
	--with-default-pkcs11-provider=yes \
	--with-security-key-builtin=yes \
	--with-pam \
%if %{WITH_SELINUX}
	--with-selinux --with-audit=linux \
	--with-sandbox=seccomp_filter \
%endif
%if %{kerberos5}
	--with-kerberos5${krb5_prefix:+=${krb5_prefix}} \
%else
	--without-kerberos5 \
%endif
%if %{libedit}
	--with-libedit
%else
	--without-libedit
%endif

%if %{static_libcrypto}
perl -pi -e "s|-lcrypto|%{_libdir}/libcrypto.a|g" Makefile
%endif

%make_build
make regress/misc/sk-dummy/sk-dummy.so

# Define a variable to toggle gtk2/gtk3 building.  This is necessary
# because RPM doesn't handle nested %%if statements.
%if %{gtk3}
	gtk3=yes
%else
	gtk3=no
%endif

%if ! %{no_gnome_askpass}
pushd contrib
if [ $gtk3 = yes ] ; then
	CFLAGS="$CFLAGS %{?__global_ldflags}" \
	    make gnome-ssh-askpass3
	mv gnome-ssh-askpass3 gnome-ssh-askpass
else
	CFLAGS="$CFLAGS %{?__global_ldflags}" \
	    make gnome-ssh-askpass2
	mv gnome-ssh-askpass2 gnome-ssh-askpass
fi
popd
%endif

%check
OPENSSL_CONF=/dev/null %{SOURCE22} %{SOURCE23}  # ./parallel_tests.sh parallel_tests.Makefile
#make tests

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config.d
mkdir -p -m755 $RPM_BUILD_ROOT%{_libexecdir}/openssh
%make_install

install -d $RPM_BUILD_ROOT/etc/pam.d/
install -d $RPM_BUILD_ROOT/etc/sysconfig/
install -d $RPM_BUILD_ROOT%{_libexecdir}/openssh
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/sshd
install -m644 %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/ssh-keycat
install -m644 %{SOURCE7} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install -m644 ssh_config_redhat $RPM_BUILD_ROOT%{_sysconfdir}/ssh/ssh_config.d/50-redhat.conf
install -m644 sshd_config_redhat_cp $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config.d/40-redhat-crypto-policies.conf
install -m644 sshd_config_redhat $RPM_BUILD_ROOT%{_sysconfdir}/ssh/sshd_config.d/50-redhat.conf
install -d -m755 $RPM_BUILD_ROOT/%{_unitdir}
install -m644 %{SOURCE9} $RPM_BUILD_ROOT/%{_unitdir}/sshd@.service
install -m644 %{SOURCE10} $RPM_BUILD_ROOT/%{_unitdir}/sshd.socket
install -m644 %{SOURCE11} $RPM_BUILD_ROOT/%{_unitdir}/sshd.service
install -m644 %{SOURCE12} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen@.service
install -m644 %{SOURCE15} $RPM_BUILD_ROOT/%{_unitdir}/sshd-keygen.target
install -d -m755 $RPM_BUILD_ROOT/%{_userunitdir}
install -m644 %{SOURCE16} $RPM_BUILD_ROOT/%{_userunitdir}/ssh-agent.service
install -m644 %{SOURCE17} $RPM_BUILD_ROOT/%{_userunitdir}/ssh-agent.socket
install -m744 %{SOURCE13} $RPM_BUILD_ROOT/%{_libexecdir}/openssh/sshd-keygen
install -m755 contrib/ssh-copy-id $RPM_BUILD_ROOT%{_bindir}/
install contrib/ssh-copy-id.1 $RPM_BUILD_ROOT%{_mandir}/man1/
install -d -m711 ${RPM_BUILD_ROOT}/%{_datadir}/empty.sshd
install -p -D -m 0644 %{SOURCE19} %{buildroot}%{_sysusersdir}/openssh-server.conf
# Migration service/script for Fedora 38 change to remove group ownership for standard host keys
# See https://fedoraproject.org/wiki/Changes/SSHKeySignSuidBit
install -m744 %{SOURCE20} $RPM_BUILD_ROOT/%{_libexecdir}/openssh/ssh-host-keys-migration.sh
# Pulled-in via a `Wants=` in `sshd.service` & `sshd@.service`
install -m644 %{SOURCE21} $RPM_BUILD_ROOT/%{_unitdir}/ssh-host-keys-migration.service
install -d $RPM_BUILD_ROOT/%{_localstatedir}/lib
touch $RPM_BUILD_ROOT/%{_localstatedir}/lib/.ssh-host-keys-migration

%if ! %{no_gnome_askpass}
install contrib/gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/gnome-ssh-askpass
%endif

%if ! %{no_gnome_askpass}
ln -s gnome-ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/openssh/ssh-askpass
install -m 755 -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.csh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
install -m 755 contrib/redhat/gnome-ssh-askpass.sh $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/
%endif

%if %{no_gnome_askpass}
rm -f $RPM_BUILD_ROOT/etc/profile.d/gnome-ssh-askpass.*
%endif

perl -pi -e "s|$RPM_BUILD_ROOT||g" $RPM_BUILD_ROOT%{_mandir}/man*/*

install -m 755 -d $RPM_BUILD_ROOT%{_libdir}/sshtest/
install -m 755 regress/misc/sk-dummy/sk-dummy.so $RPM_BUILD_ROOT%{_libdir}/sshtest

%pre server
%sysusers_create_compat %{SOURCE19}

%post server
if [ $1 -gt 1 ]; then
    # In the case of an upgrade (never true on OSTree systems) run the migration
    # script for Fedora 38 to remove group ownership for host keys.
    %{_libexecdir}/openssh/ssh-host-keys-migration.sh
    # Prevent the systemd unit that performs the same service (useful for
    # OSTree systems) from running.
    touch /var/lib/.ssh-host-keys-migration
fi
%systemd_post sshd.service sshd.socket
# Migration scriptlet for Fedora 31 and 32 installations to sshd_config
# drop-in directory (in F32+).
# Do this only if the file generated by anaconda exists, contains our config
# directive and sshd_config contains include directive as shipped in our package
%global sysconfig_anaconda /etc/sysconfig/sshd-permitrootlogin
test -f %{sysconfig_anaconda} && \
  test ! -f /etc/ssh/sshd_config.d/01-permitrootlogin.conf && \
  grep -q '^PERMITROOTLOGIN="-oPermitRootLogin=yes"' %{sysconfig_anaconda} && \
  grep -q '^Include /etc/ssh/sshd_config.d/\*.conf' /etc/ssh/sshd_config && \
  echo "PermitRootLogin yes" >> /etc/ssh/sshd_config.d/25-permitrootlogin.conf && \
  rm %{sysconfig_anaconda} || :

%preun server
%systemd_preun sshd.service sshd.socket

%postun server
%systemd_postun_with_restart sshd.service

%post clients
%systemd_user_post ssh-agent.service
%systemd_user_post ssh-agent.socket

%preun clients
%systemd_user_preun ssh-agent.service
%systemd_user_preun ssh-agent.socket

%files
%license LICENCE
%doc CREDITS ChangeLog OVERVIEW PROTOCOL* README README.platform README.privsep README.tun README.dns TODO
%attr(0755,root,root) %dir %{_sysconfdir}/ssh
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/moduli
%attr(0755,root,root) %{_bindir}/ssh-keygen
%attr(0644,root,root) %{_mandir}/man1/ssh-keygen.1*
%attr(0755,root,root) %dir %{_libexecdir}/openssh

%files clients
%attr(0755,root,root) %{_bindir}/ssh
%attr(0644,root,root) %{_mandir}/man1/ssh.1*
%attr(0755,root,root) %{_bindir}/scp
%attr(0644,root,root) %{_mandir}/man1/scp.1*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config
%dir %attr(0755,root,root) %{_sysconfdir}/ssh/ssh_config.d/
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/ssh/ssh_config.d/50-redhat.conf
%attr(0644,root,root) %{_mandir}/man5/ssh_config.5*
%attr(0755,root,root) %{_bindir}/ssh-agent
%attr(0755,root,root) %{_bindir}/ssh-add
%attr(0755,root,root) %{_bindir}/ssh-keyscan
%attr(0755,root,root) %{_bindir}/sftp
%attr(0755,root,root) %{_bindir}/ssh-copy-id
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-pkcs11-helper
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-sk-helper
%attr(0644,root,root) %{_mandir}/man1/ssh-agent.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-add.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-keyscan.1*
%attr(0644,root,root) %{_mandir}/man1/sftp.1*
%attr(0644,root,root) %{_mandir}/man1/ssh-copy-id.1*
%attr(0644,root,root) %{_mandir}/man8/ssh-pkcs11-helper.8*
%attr(0644,root,root) %{_mandir}/man8/ssh-sk-helper.8*
%attr(0644,root,root) %{_userunitdir}/ssh-agent.service
%attr(0644,root,root) %{_userunitdir}/ssh-agent.socket

%files keysign
%attr(4555,root,root) %{_libexecdir}/openssh/ssh-keysign
%attr(0644,root,root) %{_mandir}/man8/ssh-keysign.8*

%files server
%dir %attr(0711,root,root) %{_datadir}/empty.sshd
%attr(0755,root,root) %{_sbindir}/sshd
%attr(0755,root,root) %{_libexecdir}/openssh/sshd-session
%attr(0755,root,root) %{_libexecdir}/openssh/sshd-auth
%attr(0755,root,root) %{_libexecdir}/openssh/sftp-server
%attr(0755,root,root) %{_libexecdir}/openssh/sshd-keygen
%attr(0644,root,root) %{_mandir}/man5/sshd_config.5*
%attr(0644,root,root) %{_mandir}/man5/moduli.5*
%attr(0644,root,root) %{_mandir}/man8/sshd.8*
%attr(0644,root,root) %{_mandir}/man8/sftp-server.8*
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config
%dir %attr(0700,root,root) %{_sysconfdir}/ssh/sshd_config.d/
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config.d/40-redhat-crypto-policies.conf
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/ssh/sshd_config.d/50-redhat.conf
%attr(0644,root,root) %config(noreplace) /etc/pam.d/sshd
%attr(0640,root,root) %config(noreplace) /etc/sysconfig/sshd
%attr(0644,root,root) %{_unitdir}/sshd.service
%attr(0644,root,root) %{_unitdir}/sshd@.service
%attr(0644,root,root) %{_unitdir}/sshd.socket
%attr(0644,root,root) %{_unitdir}/sshd-keygen@.service
%attr(0644,root,root) %{_unitdir}/sshd-keygen.target
%attr(0644,root,root) %{_sysusersdir}/openssh-server.conf
%attr(0644,root,root) %{_unitdir}/ssh-host-keys-migration.service
%attr(0744,root,root) %{_libexecdir}/openssh/ssh-host-keys-migration.sh
%ghost %attr(0644,root,root) %{_localstatedir}/lib/.ssh-host-keys-migration

%files keycat
%doc HOWTO.ssh-keycat
%attr(0755,root,root) %{_libexecdir}/openssh/ssh-keycat
%attr(0644,root,root) %config(noreplace) /etc/pam.d/ssh-keycat

%if ! %{no_gnome_askpass}
%files askpass
%attr(0644,root,root) %{_sysconfdir}/profile.d/gnome-ssh-askpass.*
%attr(0755,root,root) %{_libexecdir}/openssh/gnome-ssh-askpass
%{_libexecdir}/openssh/ssh-askpass
%endif

%files sk-dummy
%attr(0755,root,root) %{_libdir}/sshtest/sk-dummy.so

%changelog
* Wed Dec 10 2025 Pavol Žáčik <pzacik@redhat.com> - 10.0p1-6
- Update gssapi-keyex patch to not abort KEX without hostkey

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 10.0p1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jun 27 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 10.0p1-4
- Update sshd@.service to follow upstream, mostly support ephemeral sshd keys
  Submitted by Allison Karlitskaya (https://src.fedoraproject.org/rpms/openssh/pull-request/101)
  Needs a SELinux counterpart.
  Related: rhbz#2374928

* Mon Jun 09 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 10.0p1-3
- Apply patches forgot in previous respin

* Mon May 19 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 10.0p1-2
- Provide better diagnostics for non-supported private keys
  (https://github.com/openssh/openssh-portable/pull/564)
- Ignore too short hostkeys in known_hosts file
  (https://github.com/openssh/openssh-portable/pull/567)
- Switch to systemd-socket activation for ssh-agent
  Resolves: rhbz#2181353

* Fri May 16 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 10.0p1-1
- Rebase to OpenSSH 10.0p1

* Thu Apr 17 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-15
- Require OpenSSL 3.5 to support PQ crypto
- Suppress systemd warning on restart sshd

* Tue Mar 18 2025 Zbigniew Jędrzejewski-Szmek  <zbyszek@in.waw.pl> - 9.9p1-14
- Remove /usr/local/sbin from the default path too

* Tue Mar 18 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-13
- Remove /usr/sbin from the default path
  Resolves: rhbz#2352387
- Export and accept COLORTERM
  Resolves: rhbz#2352653

* Thu Mar 06 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-12
- Update ssh-keysign permission for RPM linter

* Wed Mar 05 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-11
- Use OpenSSL ML-KEM implementation instead of the native one

* Tue Feb 25 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-10
- Some minor fixes from Rocky Linux
  https://www.openwall.com/lists/oss-security/2025/02/22/1

* Tue Feb 18 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-9
- Fix regression of Match directive processing
- Fix missing error codes set and invalid error code checks in OpenSSH. It
  prevents memory exhaustion attack and a MITM attack when VerifyHostKeyDNS
  is on (CVE-2025-26465, CVE-2025-26466).

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 9.9p1-8.1
- Add explicit BR: libxcrypt-devel

* Wed Jan 29 2025 FeRD (Frank Dana) <ferdnyc@gmail.com> - 9.9p1-8
- Replace deprecated (since 8.7) ChallengeResponseAuthentication
  with KbdInteractiveAuthentication, in redhat sshd config

* Mon Jan 27 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-7
- Fix regression of Match directive processing
  Resolves: rhbz#2341769

* Mon Jan 27 2025 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-6
- Remove pam-ssh-agent subcomponent
  Resolves: rhbz#2338440

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 9.9p1-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Oct 28 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-5
- Fix MLKEM for BE platforms

* Wed Oct 16 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-4
- Resolve memory management issues after rebase
- Define OPTIONS env in systemd modules (https://src.fedoraproject.org/rpms/openssh/pull-request/92)

* Fri Oct 11 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-3
- Separate ssh-keysign to a dedicated package
- Use FIPS KEX defaults in FIPS mode

* Thu Oct 10 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-2
- Update version of pam_ssh_agent_auth

* Tue Oct 08 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.9p1-1
- Update to OpenSSH 9.9p1

* Tue Sep 03 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.8p1-4
- Synchronize patches from Red Hat

* Mon Aug 05 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.8p1-3
- Sshd now proposes to enter password again when a non-existing user is specified

* Fri Jul 26 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.8p1-2
- Change default key type in FIPS mode

* Mon Jul 22 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.8p1-1
- Update to OpenSSH 9.8p1

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.6p1-1.14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.6p1-1.13
- rebuilt

* Mon Jul 01 2024 Gordon Messmer <gordon.messmer@gmail.com> - 9.6p1-12
- Patch 9.6p1 for CVE-2024-6387

* Mon Jul 01 2024 Gordon Messmer <gordon.messmer@gmail.com> - 9.6p1-11
- Shorten paths used for parallel tests to fix BZ#2295117

* Thu May 09 2024 Zoltan Fridrich <zfridric@redhat.com> - 9.6p1-10
- Correctly audit hostname and IP address
- Make default key sizes configurable in sshd-keygen

* Wed Apr 24 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.6p1-1.9
- Use OpenSSL SSH KDF implementation - s390x fixup

* Wed Apr 24 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.6p1-1.8
- Use OpenSSL SSH KDF implementation

* Wed Apr 17 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.6p1-1.7
- Only set PAM_RHOST if the remote host is not "UNKNOWN"
  https://src.fedoraproject.org/rpms/openssh/pull-request/71
  Patch by Daan De Meyer <daan.j.demeyer@gmail.com>
- Some spec cleanup
  https://src.fedoraproject.org/rpms/openssh/pull-request/74
  by Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>

* Thu Apr 04 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.6p1-1.6
- rebuilt

* Thu Apr 04 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.6p1-1.5
- rebuilt

* Tue Apr 02 2024 Gordon Messmer <gordon.messmer@gmail.com> - 9.6p1-1.4
- Build OpenSSH without libsystemd dependency, using reference implementation

* Wed Mar 13 2024 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.6p1-1.3
- Build OpenSSH without engine support
- Make tests run at build phase (using parallel run mechanism by Alexander Sosedkin)

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.6p1-1.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 9.6p1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 26 2023 Daniel Milnes <daniel@daniel-milnes.uk> - 9.6p1-1
- Update to OpenSSH 9.6
  Original patches from https://src.fedoraproject.org/rpms/openssh/pull-request/63
  Tuned by Dmitry Belyavskiy for GSS and PKCS#11 URI processing

* Fri Dec 22 2023 Florian Weimer <fweimer@redhat.com> - 9.3p1-13.1
- Fix type errors in downstream gssapi-keyex patch

* Mon Oct 16 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.3p1-13
- Fix issue with read-only ssh buffer during gssapi key exchange (rhbz#1938224)
- https://github.com/openssh-gsskex/openssh-gsskex/pull/19

* Sun Oct 15 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.3p1-12
- Fix FTBFS due to implicit declarations (rhbz#2241211)

* Tue Sep 19 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.3p1-11
- migrated to SPDX license

* Fri Sep 15 2023 Timothée Ravier <tim@siosm.fr> - 9.3p1-10
- Revert "Remove sshd.socket unit (rhbz#2025716)"

* Thu Aug 03 2023 Norbert Pocs <npocs@redhat.com> - 9.3p1-9
- pkcs11: Add support for 'serial' in PKCS#11 URI
- Apply the upstream MR related to the previous pkcs11 issue
- https://github.com/openssh/openssh-portable/pull/406

* Thu Aug 03 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.3p1-8
- Split including crypto-policies to a separate config (rhbz#1970566)
- Disable forking of ssh-agent on startup (rhbz#2148555)
- Remove sshd.socket unit (rhbz#2025716)
- Minor optimization of ssh_krb5_kuserok (rhbz#2112501)

* Tue Aug 01 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.3p1-7
- Relax checks of OpenSSL version

* Wed Jul 26 2023 Mattias Ellert <mattias.ellert@physics.uu.se> - 9.3p1-6
- Update gssapi-keyex patch for OpenSSH 9.0+

* Fri Jul 21 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.3p1-5
- Fix remote code execution in ssh-agent PKCS#11 support
  Resolves: CVE-2023-38408

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.3p1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Norbert Pocs <npocs@redhat.com> - 9.3p1-4
- Fix deprecated %patchN syntax
- Reduce the number of patches by merging related patches

* Wed Jun 07 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.3p1-3
- Fix DSS verification problem
  Resolves: rhbz#2212937

* Fri Jun 02 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.3p1-2
- Remove unused patch

* Thu Jun 01 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.3p1-1 + 0.10.4-9
- Rebase OpenSSH to 9.3p1

* Wed May 24 2023 Norbert Pocs <npocs@redhat.com> - 9.0p1-18
- Fix pkcs11 issue with the recent changes
- Clarify HostKeyAlgorithms relation with crypto-policies

* Fri Apr 14 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-17
- In case when sha1 signatures are not supported, fallback to sha2 in hostproof
- Audit logging patch was not applied (rhbz#2177471)

* Thu Apr 13 2023 Norbert Pocs <npocs@redhat.com> - 9.0p1-16
- Make the sign, dh, ecdh processes FIPS compliant by adopting to
  openssl 3.0

* Thu Apr 13 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-15
- Fix self-DoS
  Resolves: CVE-2023-25136
- Remove too aggressive coverity fix causing native tests failure

* Wed Apr 12 2023 Florian Weimer <fweimer@redhat.com> - 9.0p1-14.2
- C99 compatiblity fixes

* Tue Mar 14 2023 Timothée Ravier <tim@siosm.fr> - 9.0p1-14
- Make sshd & sshd@ units want ssh-host-keys-migration.service

* Mon Mar 13 2023 Zoltan Fridrich <zfridric@redhat.com> - 9.0p1-13
- Add sk-dummy subpackage for test purposes (rhbz#2176795)

* Mon Mar 06 2023 Dusty Mabe <dusty@dustymabe.com> - 9.0p1-12
- Mark /var/lib/.ssh-host-keys-migration as %ghost file
- Make ssh-host key migration less conditional

* Wed Mar 01 2023 Dusty Mabe <dusty@dustymabe.com> - 9.0p1-11
- Provide a systemd unit for restoring default host key permissions (rhbz#2172956)
- Co-Authored by Timothée Ravier <tim@siosm.fr>

* Mon Jan 23 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-10
- Restore upstream behaviour and default host key permissions (rhbz#2141272)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 9.0p1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 09 2023 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-9
- Fix build against updated OpenSSL (rhbz#2158966)

* Mon Oct 24 2022 Norbert Pocs <npocs@redhat.com> - 9.0p1-8
- Add additional audit logging about ssh key used to login (rhbz#2049947)

* Fri Oct 21 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-7
- Check IP opts length (rhbz#1960015)

* Wed Oct 5 2022 Anthony Rabbito <hello@anthonyrabbito.com> - 9.0p1-6
- Add a socket unit to ssh-agent user unit (rhbz#2125576)

* Thu Sep 29 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-5
- RSAMinSize => RequiredRSASize

* Fri Sep 02 2022 Luca BRUNO <lucab@lucabruno.net> - 9.0p1-4
- Move users/groups creation logic to sysusers.d fragments

* Wed Aug 24 2022 Alexander Sosedkin <asosedkin@redhat.com> - 9.0p1-3
- State in manpages that HostbasedAcceptedAlgorithms is set by crypto-policies

* Wed Aug 17 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-2
- Port patches from CentOS - RSAMinSize (rhbz#2117264)

* Thu Aug 11 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 9.0p1-1 + 0.10.4-7
- Rebase OpenSSH to 9.0p1 (rhbz#2057466)

* Wed Aug 10 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.8p1-4 + 0.10.4-6
- Port patches from CentOS (rhbz#2117264)

* Mon Aug 01 2022 Luca BRUNO <lucab@lucabruno.net> - 8.8p1-3
- Use allocated static GID for 'ssh_keys' group (rhbz#2104595)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.8p1-2.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Apr 29 2022 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.8p1-2
- Disable locale forwarding in OpenSSH (#2002739)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 8.8p1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 29 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.8p1-1 + 0.10.4-5
- New upstream release (#2007967)

* Wed Sep 29 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.7p1-3
- CVE-2021-41617 fix (#2008292)

* Thu Sep 16 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.7p1-2
- Use SFTP protocol for scp by default (#2004956)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 8.7p1-1.1
- Rebuilt with OpenSSL 3.0.0

* Wed Sep 01 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.7p1-1 + 0.10.4-4
- New upstream release (#1995893)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.6p1-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon Jun 21 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.6p1-5
- restore the blocking mode on standard output (#1942901) - upstream

* Tue May 25 2021 Timm Bäder <tbaeder@redhat.com> - 8.6p1-4
- Use %%set_build_flags to set all builds flags

* Fri May 21 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.6p1-3
- Hostbased ssh authentication fails if session ID contains a '/' (#1963059)

* Mon May 10 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.6p1-2
- restore the blocking mode on standard output (#1942901)

* Mon Apr 19 2021 Dmitry Belyavskiy <dbelyavs@redhat.com> - 8.6p1-1 + 0.10.4-3
- New upstream release (#1950819)
- ssh-keygen printing fingerprint issue with Windows keys (#1901518)
- sshd provides PAM an incorrect error code (#1879503)

* Tue Mar 09 2021 Rex Dieter <rdieter@fedoraproject.org> - 8.5p1-2
- ssh-agent.serivce is user unit (#1761817#27)

* Wed Mar 03 2021 Jakub Jelen <jjelen@redhat.com> - 8.5p1-1 + 0.10.4-2
- New upstream release (#1934336)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 8.4p1-5.2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.4p1-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Jakub Jelen <jjelen@redhat.com> - 8.4p1-5 + 0.10.4-1
- Use /usr/share/empty.sshd instead of /var/empty/sshd
- Allow emptu labels in PKCS#11 tokens (#1919007)
- Drop openssh-cavs subpackage

* Tue Dec 01 2020 Jakub Jelen <jjelen@redhat.com> - 8.4p1-4 + 0.10.4-1
- Remove "PasswordAuthentication yes" from vendor configuration as it is
  already default and it might be hard to override.
- Fix broken obsoletes for openssh-ldap (#1902084)

* Thu Nov 19 2020 Jakub Jelen <jjelen@redhat.com> - 8.4p1-3 + 0.10.4-1
- Unbreak seccomp filter on arm (#1897712)
- Add a workaround for Debian's broken OpenSSH (#1881301)

* Tue Oct 06 2020 Jakub Jelen <jjelen@redhat.com> - 8.4p1-2 + 0.10.4-1
- Unbreak ssh-copy-id after a release (#1884231)
- Remove misleading comment from sysconfig

* Tue Sep 29 2020 Jakub Jelen <jjelen@redhat.com> - 8.4p1-1 + 0.10.4-1
- New upstream release of OpenSSH and pam_ssh_agent_auth (#1882995)

* Fri Aug 21 2020 Jakub Jelen <jjelen@redhat.com> - 8.3p1-4 + 0.10.3-10
- Remove openssh-ldap subpackage (#1871025)
- pkcs11: Do not crash with invalid paths in ssh-agent (#1868996)
- Clarify documentation about sftp-server -m (#1862504)

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.3p1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jun 10 2020 Jakub Jelen <jjelen@redhat.com> - 8.3p1-3 + 0.10.3-10
- Do not lose PIN when more slots match PKCS#11 URI (#1843372)
- Update to new crypto-policies version on server (using sshd_config include)
- Move redhat configuraion files to larger number to allow simpler override
- Move sshd_config include before any other definitions (#1824913)

* Mon Jun 01 2020 Jakub Jelen <jjelen@redhat.com> - 8.3p1-2 + 0.10.3-10
- Fix crash on cleanup (#1842281)

* Wed May 27 2020 Jakub Jelen <jjelen@redhat.com> - 8.3p1-1 + 0.10.3-10
- New upstream release (#1840503)
- Unbreak corner cases of sshd_config include
- Fix order of gssapi key exchange algorithms

* Wed Apr 08 2020 Jakub Jelen <jjelen@redhat.com> - 8.2p1-3 + 0.10.3-9
- Simplify reference to crypto policies in configuration files
- Unbreak gssapi authentication with GSSAPITrustDNS over jump hosts
- Correctly print FIPS mode initialized in debug mode
- Enable SHA2-based GSSAPI key exchange methods (#1666781)
- Do not break X11 forwarding when IPv6 is disabled
- Remove fipscheck dependency as OpenSSH is no longer FIPS module
- Improve documentation about crypto policies defaults in manual pages

* Thu Feb 20 2020 Jakub Jelen <jjelen@redhat.com> - 8.2p1-2 + 0.10.3-9
- Build against libfido2 to unbreak internal u2f support

* Mon Feb 17 2020 Jakub Jelen <jjelen@redhat.com> - 8.2p1-1 + 0.10.3-9
- New upstrem reelase (#1803290)
- New /etc/ssh/sshd_config.d drop in directory
- Support for U2F security keys
- Correctly report invalid key permissions (#1801459)
- Do not write bogus information on stderr in FIPS mode (#1778224)

* Mon Feb 03 2020 Jakub Jelen <jjelen@redhat.com> - 8.1p1-4 + 0.10.3-8
- Unbreak seccomp filter on ARM (#1796267)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 8.1p1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Nov 27 2019 Jakub Jelen <jjelen@redhat.com> - 8.1p1-3 + 0.10.3-8
- Unbreak seccomp filter also on ARM (#1777054)

* Thu Nov 14 2019 Jakub Jelen <jjelen@redhat.com> - 8.1p1-2 + 0.10.3-8
- Unbreak seccomp filter with latest glibc (#1771946)

* Wed Oct 09 2019 Jakub Jelen <jjelen@redhat.com> - 8.1p1-1 + 0.10.3-8
- New upstream release (#1759750)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 8.0p1-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-8 + 0.10.3-7
- Use the upstream-accepted version of the PKCS#8 PEM support (#1722285)

* Fri Jul 12 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-7 + 0.10.3-7
- Use the environment file under /etc/sysconfig for anaconda configuration (#1722928)

* Wed Jul 03 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-6 + 0.10.3-7
- Provide the entry point for anaconda configuration in service file (#1722928)

* Wed Jun 26 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-5 + 0.10.3-7
- Disable root password logins (#1722928)
- Fix typo in manual pages related to crypto-policies
- Fix the gating test to make sure it removes the test user
- Cleanu up spec file and get rid of some rpmlint warnings

* Mon Jun 17 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-4 + 0.10.3-7
- Compatibility with ibmca engine for ECC
- Generate more modern PEM files using new OpenSSL API
- Provide correct signature types for RSA keys using SHA2 from agent

* Mon May 27 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-3 + 0.10.3-7
- Remove problematic patch updating cached pw structure
- Do not require the labels on the public objects (#1710832)

* Tue May 14 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-2 + 0.10.3-7
- Use OpenSSL KDF
- Use high-level OpenSSL API for signatures handling
- Mention crypto-policies in manual pages instead of hardcoded defaults
- Verify in package testsuite that SCP vulnerabilities are fixed
- Do not fail in FIPS mode, when unsupported algorithm is listed in configuration

* Fri Apr 26 2019 Jakub Jelen <jjelen@redhat.com> - 8.0p1-1 + 0.10.3-7
- New upstream release (#1701072)
- Removed support for VendroPatchLevel configuration option
- Significant rework of GSSAPI Key Exchange
- Significant rework of PKCS#11 URI support

* Mon Mar 11 2019 Jakub Jelen <jjelen@redhat.com> - 7.9p1-5 + 0.10.3.6
- Fix kerberos cleanup procedures with GSSAPI
- Update cached passwd structure after PAM authentication
- Do not fall back to sshd_net_t SELinux context
- Fix corner cases of PKCS#11 URI implementation
- Do not negotiate arbitrary primes with DH GEX in FIPS 

* Wed Feb 06 2019 Jakub Jelen <jjelen@redhat.com> - 7.9p1-4 + 0.10.3.6
- Log when a client requests an interactive session and only sftp is allowed
- Fix minor issues in ssh-copy-id
- Enclose redhat specific configuration with Match final block

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.9p1-3.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 7.9p1-3.1
- Rebuilt for libcrypt.so.2 (#1666033)

* Mon Jan 14 2019 Jakub Jelen <jjelen@redhat.com> - 7.9p1-3 + 0.10.3.6
- Backport Match final to unbreak canonicalization with crypto-policies (#1630166)
- gsskex: Dump correct option
- Backport several fixes from 7_9 branch, mostly related to certificate authentication (#1665611)
- Backport patch for CVE-2018-20685 (#1665786)
- Correctly initialize ECDSA key structures from PKCS#11

* Wed Nov 14 2018 Jakub Jelen <jjelen@redhat.com> - 7.9p1-2 + 0.10.3-6
- Fix LDAP configure test (#1642414)
- Avoid segfault on kerberos authentication failure
- Reference correct file in configuration example (#1643274)
- Dump missing GSSAPI configuration options
- Allow to disable RSA signatures with SHA-1

* Fri Oct 19 2018 Jakub Jelen <jjelen@redhat.com> - 7.9p1-1 + 0.10.3-6
- New upstream release OpenSSH 7.9p1 (#1632902, #1630166)
- Honor GSSAPIServerIdentity option for GSSAPI key exchange
- Do not break gsssapi-keyex authentication method when specified in
  AuthenticationMethods
- Follow the system-wide PATH settings (#1633756)
- Address some coverity issues

* Mon Sep 24 2018 Jakub Jelen <jjelen@redhat.com> - 7.8p1-3 + 0.10.3-5
- Disable OpenSSH hardening flags and use the ones provided by system
- Ignore unknown parts of PKCS#11 URI
- Do not fail with GSSAPI enabled in match blocks (#1580017)
- Fix the segfaulting cavs test (#1628962)

* Fri Aug 31 2018 Jakub Jelen <jjelen@redhat.com> - 7.8p1-2 + 0.10.3-5
- New upstream release fixing CVE 2018-15473
- Remove unused patches
- Remove reference to unused enviornment variable SSH_USE_STRONG_RNG
- Address coverity issues
- Unbreak scp between two IPv6 hosts
- Unbreak GSSAPI key exchange (#1624344)
- Unbreak rekeying with GSSAPI key exchange (#1624344)

* Thu Aug 09 2018 Jakub Jelen <jjelen@redhat.com> - 7.7p1-6 + 0.10.3-4
- Fix listing of kex algoritms in FIPS mode
- Allow aes-gcm cipher modes in FIPS mode
- Coverity fixes

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.7p1-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 03 2018 Jakub Jelen <jjelen@redhat.com> - 7.7p1-5 + 0.10.3-4
- Disable manual printing of motd by default (#1591381)

* Wed Jun 27 2018 Jakub Jelen <jjelen@redhat.com> - 7.7p1-4 + 0.10.3-4
- Better handling of kerberos tickets storage (#1566494)
- Add pam_motd to pam stack (#1591381)

* Mon Apr 16 2018 Jakub Jelen <jjelen@redhat.com> - 7.7p1-3 + 0.10.3-4
- Fix tun devices and other issues fixed after release upstream (#1567775)

* Thu Apr 12 2018 Jakub Jelen <jjelen@redhat.com> - 7.7p1-2 + 0.10.3-4
- Do not break quotes parsing in configuration file (#1566295)

* Wed Apr 04 2018 Jakub Jelen <jjelen@redhat.com> - 7.7p1-1 + 0.10.3-4
- New upstream release (#1563223)
- Add support for ECDSA keys in PKCS#11 (#1354510)
- Add support for PKCS#11 URIs

* Tue Mar 06 2018 Jakub Jelen <jjelen@redhat.com> - 7.6p1-7 + 0.10.3-3
- Require crypto-policies version and new path
- Remove bogus NSS linking

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.6p1-6.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Jakub Jelen <jjelen@redhat.com> - 7.6p1-6 + 0.10.3-3
- Rebuild for gcc bug on i386 (#1536555)

* Thu Jan 25 2018 Florian Weimer <fweimer@redhat.com> - 7.6p1-5.2
- Rebuild to work around gcc bug leading to sshd miscompilation (#1538648)

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 7.6p1-5.1.1
- Rebuilt for switch to libxcrypt

* Wed Jan 17 2018 Jakub Jelen <jjelen@redhat.com> - 7.6p1-5 + 0.10.3-3
- Drop support for TCP wrappers (#1530163)
- Do not pass hostnames to audit -- UseDNS is usually disabled (#1534577)

* Thu Dec 14 2017 Jakub Jelen <jjelen@redhat.com> - 7.6p1-4 + 0.10.3-3
- Whitelist gettid() syscall in seccomp filter (#1524392)

* Mon Dec 11 2017 Jakub Jelen <jjelen@redhat.com> - 7.6p1-3 + 0.10.3-3
- Do not segfault during audit cleanup (#1524233)
- Avoid gcc warnings about uninitialized variables

* Wed Nov 22 2017 Jakub Jelen <jjelen@redhat.com> - 7.6p1-2 + 0.10.3-3
- Do not build everything against libldap
- Do not segfault for ECC keys in PKCS#11

* Thu Oct 19 2017 Jakub Jelen <jjelen@redhat.com> - 7.6p1-1 + 0.10.3-3
- New upstream release OpenSSH 7.6
- Addressing review remarks for OpenSSL 1.1.0 patch
- Fix PermitOpen bug in OpenSSH 7.6
- Drop support for ExposeAuthenticationMethods option

* Mon Sep 11 2017 Jakub Jelen <jjelen@redhat.com> - 7.5p1-6 + 0.10.3-2
- Do not export KRB5CCNAME if the default path is used (#1199363)
- Add enablement for openssl-ibmca and openssl-ibmpkcs11 (#1477636)
- Add new GSSAPI kex algorithms with SHA-2, but leave them disabled for now
- Enforce pam_sepermit for all logins in SSH (#1492313)
- Remove pam_reauthorize, since it is not needed by cockpit anymore (#1492313)

* Mon Aug 14 2017 Jakub Jelen <jjelen@redhat.com> - 7.5p1-5 + 0.10.3-2
- Another less-intrusive approach to crypto policy (#1479271)

* Tue Aug 01 2017 Jakub Jelen <jjelen@redhat.com> - 7.5p1-4 + 0.10.3-2
- Remove SSH-1 subpackage for Fedora 27 (#1474942)
- Follow system-wide crypto policy in server (#1479271)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.5p1-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 30 2017 Jakub Jelen <jjelen@redhat.com> - 7.5p1-2 + 0.10.3-2
- Sync downstream patches with RHEL (FIPS)
- Resolve potential issues with OpenSSL 1.1.0 patch

* Wed Mar 22 2017 Jakub Jelen <jjelen@redhat.com> - 7.5p1-2 + 0.10.3-2
- Fix various after-release typos including failed build in s390x (#1434341)
- Revert chroot magic with SELinux

* Mon Mar 20 2017 Jakub Jelen <jjelen@redhat.com> - 7.5p1-1 + 0.10.3-2
- New upstream release

* Fri Mar 03 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-4 + 0.10.3-1
- Avoid sending the SD_NOTIFY messages from wrong processes (#1427526)
- Address reports by coverity

* Mon Feb 20 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-3 + 0.10.3-1
- Properly report errors from included files (#1408558)
- New pam_ssh_agent_auth 0.10.3 release
- Switch to SD_NOTIFY to make systemd happy

* Mon Feb 06 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-2 + 0.10.2-5
- Fix ssh-agent cert signing error (#1416584)
- Fix wrong path to crypto policies
- Attempt to resolve issue with systemd

* Tue Jan 03 2017 Jakub Jelen <jjelen@redhat.com> - 7.4p1-1 + 0.10.2-5
- New upstream release (#1406204)
- Cache supported OIDs for GSSAPI key exchange (#1395288)
- Fix typo causing heap corruption (use-after-free) (#1409433)
- Prevent hangs with long MOTD

* Thu Dec 08 2016 Jakub Jelen <jjelen@redhat.com> - 7.3p1-7 + 0.10.2-4
- Properly deserialize received RSA certificates in ssh-agent (#1402029)
- Move MAX_DISPLAYS to a configuration option

* Wed Nov 16 2016 Jakub Jelen <jjelen@redhat.com> - 7.3p1-6 + 0.10.2-4
- GSSAPI requires futex syscall in privsep child (#1395288)

* Thu Oct 27 2016 Jakub Jelen <jjelen@redhat.com> - 7.3p1-5 + 0.10.2-4
- Build against OpenSSL 1.1.0 with compat changes
- Recommend crypto-policies
- Fix chroot dropping capabilities (#1386755)

* Thu Sep 29 2016 Jakub Jelen <jjelen@redhat.com> - 7.3p1-4 + 0.10.2-4
- Fix NULL dereference (#1380297)
- Include client Crypto Policy (#1225752)

* Mon Aug 15 2016 Jakub Jelen <jjelen@redhat.com> - 7.3p1-3 + 0.10.2-4
- Proper content of included configuration file

* Tue Aug 09 2016 Jakub Jelen <jjelen@redhat.com> - 7.3p1-2 + 0.10.2-4
- Fix permissions on the include directory (#1365270)

* Tue Aug 02 2016 Jakub Jelen <jjelen@redhat.com> - 7.3p1-1 + 0.10.2-4
- New upstream release (#1362156)

* Tue Jul 26 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-11 + 0.10.2-3
- Remove slogin and sshd-keygen (#1359762)
- Prevent guest_t from running sudo (#1357860)

* Mon Jul 18 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-10 + 0.10.2-3
- CVE-2016-6210: User enumeration via covert timing channel (#1357443)
- Expose more information about authentication to PAM
- Make closefrom() ignore softlinks to the /dev/ devices on s390

* Fri Jul 01 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-9 + 0.10.2-3
- Fix wrong detection of UseLogin in server configuration (#1350347)

* Fri Jun 24 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-8 + 0.10.2-3
- Enable seccomp filter for MIPS architectures
- UseLogin=yes is not supported in Fedora
- SFTP server forced permissions should restore umask
- pam_ssh_agent_auth: Fix conflict bewteen two getpwuid() calls (#1349551)

* Mon Jun 06 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-7
- Fix regression in certificate-based authentication (#1333498)
- Check for real location of .k5login file (#1328243)
- Fix unchecked dereference in pam_ssh_agent_auth
- Clean up old patches
- Build with seccomp filter on ppc64(le) (#1195065)

* Fri Apr 29 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-6 + 0.10.2-3
- Add legacy sshd-keygen for anaconda (#1331077)

* Fri Apr 22 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-5 + 0.10.2-3
- CVE-2015-8325: ignore PAM environment vars when UseLogin=yes (#1328013)
- Fix typo in sysconfig/sshd (#1325535)

* Fri Apr 15 2016 Jakub Jelen <jjelen@redhat.com> - 7.2p2-4 + 0.10.2-3
- Revise socket activation and services dependencies (#1325535)
- Drop unused init script

* Wed Apr 13 2016 Jakub Jelen <jjelen@redhat.com> 7.2p2-3 + 0.10.2-3
- Make sshd-keygen comply with packaging guidelines (#1325535)
- Soft-deny socket() syscall in seccomp sandbox (#1324493)
- Remove *sha1 Kex in FIPS mode (#1324493)
- Remove *gcm ciphers in FIPS mode (#1324493)

* Wed Apr 06 2016 Jakub Jelen <jjelen@redhat.com> 7.2p2-2 + 0.10.2-3
- Fix GSSAPI Key Exchange according to RFC (#1323622)
- Remove init.d/functions dependency from sshd-keygen (#1317722)
- Do not use MD5 in pam_ssh_agent_auth in FIPS mode

* Thu Mar 10 2016 Jakub Jelen <jjelen@redhat.com> 7.2p2-1 + 0.10.2-3
- New upstream (security) release (#1316529)
- Clean up audit patch

* Thu Mar 03 2016 Jakub Jelen <jjelen@redhat.com> 7.2p1-2 + 0.10.2-2
- Restore slogin symlinks to preserve backward compatibility

* Mon Feb 29 2016 Jakub Jelen <jjelen@redhat.com> 7.2p1-1 + 0.10.2-2
- New upstream release (#1312870)

* Wed Feb 24 2016 Jakub Jelen <jjelen@redhat.com> 7.1p2-4.1 + 0.10.2-1
- Fix race condition in auditing events when using multiplexing (#1308295)
- Fix X11 forwarding CVE according to upstream
- Fix problem when running without privsep (#1303910)
- Remove hard glob limit in SFTP

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.1p2-3.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sat Jan 30 2016 Jakub Jelen <jjelen@redhat.com> 7.1p2-3 + 0.10.2-1
- Fix segfaults with pam_ssh_agent_auth (#1303036)
- Silently disable X11 forwarding on problems
- Systemd service should be forking to detect immediate failures

* Mon Jan 25 2016 Jakub Jelen <jjelen@redhat.com> 7.1p2-2 + 0.10.2-1
- Rebased to recent version of pam_ssh_agent_auth
- Upstream fix for CVE-2016-1908
- Remove useless defattr

* Thu Jan 14 2016 Jakub Jelen <jjelen@redhat.com> 7.1p2-1 + 0.9.2-9
- New security upstream release for CVE-2016-0777

* Tue Jan 12 2016 Jakub Jelen <jjelen@redhat.com> 7.1p1-7 + 0.9.2-8
- Change RPM define macros to global according to packaging guidelines
- Fix wrong handling of SSH_COPY_ID_LEGACY environment variable
- Update ssh-agent and ssh-keysign permissions (#1296724)
- Fix few problems with alternative builds without GSSAPI or openSSL
- Fix condition to run sshd-keygen

* Fri Dec 18 2015 Jakub Jelen <jjelen@redhat.com> 7.1p1-6 + 0.9.2-8
- Preserve IUTF8 tty mode flag over ssh connections (#1270248)
- Do not require sysconfig file to start service (#1279521)
- Update ssh-copy-id to upstream version
- GSSAPI Key Exchange documentation improvements
- Remove unused patches

* Wed Nov 04 2015 Jakub Jelen <jjelen@redhat.com> 7.1p1-5 + 0.9.2-8
- Do not set user context too many times for root logins (#1269072)

* Thu Oct 22 2015 Jakub Jelen <jjelen@redhat.com> 7.1p1-4 + 0.9.2-8
- Review SELinux user context handling after authentication (#1269072)
- Handle root logins the same way as other users (#1269072)
- Audit implicit mac, if mac is covered in cipher (#1271694)
- Increase size limit for remote glob over sftp

* Fri Sep 25 2015 Jakub Jelen <jjelen@redhat.com> 7.1p1-3 + 0.9.2-8
- Fix FIPS mode for DH kex (#1260253)
- Provide full RELRO and PIE form askpass helper (#1264036)
- Fix gssapi key exchange on server and client (#1261414)
- Allow gss-keyex root login when without-password is set (upstream #2456)
- Fix obsolete usage of SELinux constants (#1261496)

* Wed Sep 09 2015 Jakub Jelen <jjelen@redhat.com> 7.1p1-2 + 0.9.2-8
- Fix warnings reported by gcc related to keysign and keyAlgorithms

* Sat Aug 22 2015 Jakub Jelen <jjelen@redhat.com> 7.1p1-1 + 0.9.2-8
- New upstream release

* Wed Aug 19 2015 Jakub Jelen <jjelen@redhat.com> 7.0p1-2 + 0.9.3-7
- Fix problem with DSA keys using pam_ssh_agent_auth (#1251777)
- Add GSSAPIKexAlgorithms option for server and client application
- Possibility to validate legacy systems by more fingerprints (#1249626)

* Wed Aug 12 2015 Jakub Jelen <jjelen@redhat.com> 7.0p1-1 + 0.9.3-7
- New upstream release (#1252639)
- Fix pam_ssh_agent_auth package (#1251777)
- Security: Use-after-free bug related to PAM support (#1252853)
- Security: Privilege separation weakness related to PAM support (#1252854)
- Security: Incorrectly set TTYs to be world-writable (#1252862)

* Tue Jul 28 2015 Jakub Jelen <jjelen@redhat.com> 6.9p1-4 + 0.9.3-6
- Handle terminal control characters in scp progressmeter (#1247204)

* Thu Jul 23 2015 Jakub Jelen <jjelen@redhat.com> 6.9p1-3 + 0.9.3-6
- CVE-2015-5600: only query each keyboard-interactive device once (#1245971)

* Wed Jul 15 2015 Jakub Jelen <jjelen@redhat.com> 6.9p1-2 + 0.9.3-6
- Enable SECCOMP filter for s390* architecture (#1195065)
- Fix race condition when multiplexing connection (#1242682)

* Wed Jul 01 2015 Jakub Jelen <jjelen@redhat.com> 6.9p1-1 + 0.9.3-6
- New upstream release (#1238253)
- Increase limitation number of files which can be listed using glob in sftp
- Correctly revert "PermitRootLogin no" option from upstream sources (#89216)

* Wed Jun 24 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-9 + 0.9.3-5
- Allow socketcall(SYS_SHUTDOWN) for net_child on ix86 architecture

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.8p1-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 08 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-8 + 0.9.3-5
- Return stat syscall to seccomp filter (#1228323)

* Wed Jun 03 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-7 + 0.9.3-5
- Handle pam_ssh_agent_auth memory, buffers and variable sizes (#1225106)

* Thu May 28 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-6 + 0.9.3-5
- Resolve problem with pam_ssh_agent_auth after rebase (#1225106)
- ssh-copy-id: tcsh doesnt work with multiline strings
- Fix upstream memory problems
- Add missing options in testmode output and manual pages
- Provide LDIF version of LPK schema
- Document required selinux boolean for working ssh-ldap-helper

* Mon Apr 20 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-5 + 0.9.3-5
- Fix segfault on daemon exit caused by API change (#1213423)

* Thu Apr 02 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-4 + 0.9.3-5
- Fix audit_end_command to restore ControlPersist function (#1203900)

* Tue Mar 31 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-3 + 0.9.3-5
- Fixed issue with GSSAPI key exchange (#1207719)
- Add pam_namespace to sshd pam stack (based on #1125110)
- Remove krb5-config workaround for #1203900
- Fix handling SELinux context in MLS systems
- Regression: solve sshd segfaults if other instance already running

* Thu Mar 26 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-2 + 0.9.3-5
- Update audit and gss patches after rebase
- Fix reintroduced upstrem bug #1878

* Tue Mar 24 2015 Jakub Jelen <jjelen@redhat.com> 6.8p1-1 + 0.9.3-5
- new upstream release openssh-6.8p1 (#1203245)
- Resolve segfault with auditing commands (#1203900)
- Workaround krb5-config bug (#1204646)

* Thu Mar 12 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-11 + 0.9.3-4
- Ability to specify LDAP filter in ldap.conf for ssh-ldap-helper
- Fix auditing when using combination of ForceCommand and PTY
- Add sftp option to force mode of created files (from rhel)
- Fix tmpfiles.d entries to be more consistent (#1196807)

* Mon Mar 02 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-10 + 0.9.3-4
- Add tmpfiles.d entries (#1196807)

* Fri Feb 27 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-9 + 0.9.3-4
- Adjust seccomp filter for primary architectures and solve aarch64 issue (#1197051)
- Solve issue with ssh-copy-id and keys without trailing newline (#1093168)

* Tue Feb 24 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-8 + 0.9.3-4
- Add AArch64 support for seccomp_filter sandbox (#1195065)

* Mon Feb 23 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-7 + 0.9.3-4
- Fix seccomp filter on architectures without getuid32

* Mon Feb 23 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-6 + 0.9.3-4
- Update seccomp filter to work on i686 architectures (#1194401)
- Fix previous failing build (#1195065)

* Sun Feb 22 2015 Peter Robinson <pbrobinson@fedoraproject.org> 6.7p1-5 + 0.9.3-4
- Only use seccomp for sandboxing on supported platforms

* Fri Feb 20 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-4 + 0.9.3-4
- Move cavs tests into subpackage -cavs (#1194320)

* Wed Feb 18 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-3 + 0.9.3-4
- update coverity patch
- make output of sshd -T more consistent (#1187521)
- enable seccomp for sandboxing instead of rlimit (#1062953)
- update hardening to compile on gcc5
- Add SSH KDF CAVS test driver (#1193045)
- Fix ssh-copy-id on non-sh remote shells (#1045191)

* Tue Jan 27 2015 Jakub Jelen <jjelen@redhat.com> 6.7p1-2 + 0.9.3-4
- fixed audit patch after rebase

* Tue Jan 20 2015 Petr Lautrbach <plautrba@redhat.com> 6.7p1-1 + 0.9.3-4
- new upstream release openssh-6.7p1

* Thu Jan 15 2015 Jakub Jelen <jjelen@redhat.com> 6.6.1p1-11.1 + 0.9.3-3
- error message if scp when directory doesn't exist (#1142223)
- parsing configuration file values (#1130733)
- documentation in service and socket files for systemd (#1181593)
- updated ldap patch (#981058)
- fixed vendor-patchlevel
- add new option GSSAPIEnablek5users and disable using ~/.k5users by default CVE-2014-9278 (#1170745)

* Fri Dec 19 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-10 + 0.9.3-3
- log via monitor in chroots without /dev/log

* Wed Dec 03 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-9 + 0.9.3-3
- the .local domain example should be in ssh_config, not in sshd_config
- use different values for DH for Cisco servers (#1026430)

* Thu Nov 13 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-8 + 0.9.3-3
- fix gsskex patch to correctly handle MONITOR_REQ_GSSSIGN request (#1118005)

* Fri Nov 07 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-7 + 0.9.3-3
- correct the calculation of bytes for authctxt->krb5_ccname <ams@corefiling.com> (#1161073)

* Tue Nov 04 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-6 + 0.9.3-3
- privsep_preauth: use SELinux context from selinux-policy (#1008580)
- change audit trail for unknown users (mindrot#2245)
- fix kuserok patch which checked for the existence of .k5login
  unconditionally and hence prevented other mechanisms to be used properly
- revert the default of KerberosUseKuserok back to yes (#1153076)
- ignore SIGXFSZ in postauth monitor (mindrot#2263)
- sshd-keygen - don't generate DSA and ED25519 host keys in FIPS mode

* Mon Sep 08 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-5 + 0.9.3-3
- set a client's address right after a connection is set (mindrot#2257)
- apply RFC3454 stringprep to banners when possible (mindrot#2058)
- don't consider a partial success as a failure (mindrot#2270)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.6.1p1-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> 6.6.1p1-4 + 0.9.3-3
- fix license handling (both)

* Fri Jul 18 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-3 + 0.9.3-2
- standardise on NI_MAXHOST for gethostname() string lengths (#1051490)

* Mon Jul 14 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-2 + 0.9.3-2
- add pam_reauthorize.so to sshd.pam (#1115977)
- spec file and patches clenup

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6.6.1p1-1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Petr Lautrbach <plautrba@redhat.com> 6.6.1p1-1 + 0.9.3-2
- disable the curve25519 KEX when speaking to OpenSSH 6.5 or 6.6
- add support for ED25519 keys to sshd-keygen and sshd.sysconfig
- drop openssh-server-sysvinit subpackage
- slightly change systemd units logic - use sshd-keygen.service (#1066615)

* Tue Jun 03 2014 Petr Lautrbach <plautrba@redhat.com> 6.6p1-1 + 0.9.3-2
- new upstream release openssh-6.6p1

* Thu May 15 2014 Petr Lautrbach <plautrba@redhat.com> 6.4p1-4 + 0.9.3-1
- use SSH_COPY_ID_LEGACY variable to run ssh-copy-id in the legacy mode
- make /etc/ssh/moduli file public (#1043661)
- test existence of /etc/ssh/ssh_host_ecdsa_key in sshd-keygen.service
- don't clean up gssapi credentials by default (#1055016)
- ssh-agent - try CLOCK_BOOTTIME with fallback (#1091992)
- prevent a server from skipping SSHFP lookup - CVE-2014-2653 (#1081338)
- ignore environment variables with embedded '=' or '\0' characters - CVE-2014-2532
  (#1077843)

* Wed Dec 11 2013 Petr Lautrbach <plautrba@redhat.com> 6.4p1-3 + 0.9.3-1
- sshd-keygen - use correct permissions on ecdsa host key (#1023945)
- use only rsa and ecdsa host keys by default

* Tue Nov 26 2013 Petr Lautrbach <plautrba@redhat.com> 6.4p1-2 + 0.9.3-1
- fix fatal() cleanup in the audit patch (#1029074)
- fix parsing logic of ldap.conf file (#1033662)

* Fri Nov 08 2013 Petr Lautrbach <plautrba@redhat.com> 6.4p1-1 + 0.9.3-1
- new upstream release

* Fri Nov 01 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-5 + 0.9.3-7
- adjust gss kex mechanism to the upstream changes (#1024004)
- don't use xfree in pam_ssh_agent_auth sources <geertj@gmail.com> (#1024965)

* Fri Oct 25 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-4 + 0.9.3-6
- rebuild with the openssl with the ECC support

* Thu Oct 24 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-3 + 0.9.3-6
- don't use SSH_FP_MD5 for fingerprints in FIPS mode

* Wed Oct 23 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-2 + 0.9.3-6
- use default_ccache_name from /etc/krb5.conf for a kerberos cache (#991186)
- increase the size of the Diffie-Hellman groups (#1010607)
- sshd-keygen to generate ECDSA keys <i.grok@comcast.net> (#1019222)

* Tue Oct 15 2013 Petr Lautrbach <plautrba@redhat.com> 6.3p1-1.1 + 0.9.3-6
- new upstream release (#1007769)

* Tue Oct 08 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-9 + 0.9.3-5
- use dracut-fips package to determine if a FIPS module is installed
- revert -fips subpackages and hmac files suffixes

* Wed Sep 25 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-8 + 0.9.3-5
- sshd-keygen: generate only RSA keys by default (#1010092)
- use dist tag in suffixes for hmac checksum files

* Wed Sep 11 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-7 + 0.9.3-5
- use hmac_suffix for ssh{,d} hmac checksums
- bump the minimum value of SSH_USE_STRONG_RNG to 14 according to SP800-131A
- automatically restart sshd.service on-failure after 42s interval

* Thu Aug 29 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-6.1 + 0.9.3-5
- add -fips subpackages that contains the FIPS module files

* Wed Jul 31 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-5 + 0.9.3-5
- gssapi credentials need to be stored before a pam session opened (#987792)

* Tue Jul 23 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-4 + 0.9.3-5
- don't show Success for EAI_SYSTEM (#985964)
- make sftp's libedit interface marginally multibyte aware (#841771)

* Mon Jun 17 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-3 + 0.9.3-5
- move default gssapi cache to /run/user/<uid> (#848228)

* Tue May 21 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-2 + 0.9.3-5
- add socket activated sshd units to the package (#963268)
- fix the example in the HOWTO.ldap-keys

* Mon May 20 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p2-1 + 0.9.3-5
- new upstream release (#963582)

* Wed Apr 17 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-4 + 0.9.3-4
- don't use export in sysconfig file (#953111)

* Tue Apr 16 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-3 + 0.9.3-4
- sshd.service: use KillMode=process (#890376)
- add latest config.{sub,guess} to support aarch64 (#926284)

* Tue Apr 09 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-2 + 0.9.3-4
- keep track of which IndentityFile options were manually supplied and
  which were default options, and don't warn if the latter are missing.
  (mindrot#2084)

* Tue Apr 09 2013 Petr Lautrbach <plautrba@redhat.com> 6.2p1-1 + 0.9.3-4
- new upstream release (#924727)

* Wed Mar 06 2013 Petr Lautrbach <plautrba@redhat.com> 6.1p1-7 + 0.9.3-3
- use SELinux type sshd_net_t for [net] childs (#915085)

* Thu Feb 14 2013 Petr Lautrbach <plautrba@redhat.com> 6.1p1-6 + 0.9.3-3
- fix AuthorizedKeysCommand option

* Fri Feb 08 2013 Petr Lautrbach <plautrba@redhat.com> 6.1p1-5 + 0.9.3-3
- change default value of MaxStartups - CVE-2010-5107 (#908707)

* Mon Dec 03 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-4 + 0.9.3-3
- fix segfault in openssh-5.8p2-force_krb.patch (#882541)

* Mon Dec 03 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-3 + 0.9.3-3
- replace RequiredAuthentications2 with AuthenticationMethods based on upstream
- obsolete RequiredAuthentications[12] options
- fix openssh-6.1p1-privsep-selinux.patch

* Fri Oct 26 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-2
- add SELinux comment to /etc/ssh/sshd_config about SELinux command to modify port (#861400)
- drop required chkconfig (#865498)
- drop openssh-5.9p1-sftp-chroot.patch (#830237)

* Sat Sep 15 2012 Petr Lautrbach <plautrba@redhat.com> 6.1p1-1 + 0.9.3-3
- new upstream release (#852651)
- use DIR: kerberos type cache (#848228)
- don't use chroot_user_t for chrooted users (#830237)
- replace scriptlets with systemd macros (#850249)
- don't use /bin and /sbin paths (#856590)

* Mon Aug 06 2012 Petr Lautrbach <plautrba@redhat.com> 6.0p1-1 + 0.9.3-2
- new upstream release

* Mon Aug 06 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-26 + 0.9.3-1
- change SELinux context also for root user (#827109)

* Fri Jul 27 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-25 + 0.9.3-1
- fix various issues in openssh-5.9p1-required-authentications.patch

* Tue Jul 17 2012 Tomas Mraz <tmraz@redhat.com> 5.9p1-24 + 0.9.3-1
- allow sha256 and sha512 hmacs in the FIPS mode

* Fri Jun 22 2012 Tomas Mraz <tmraz@redhat.com> 5.9p1-23 + 0.9.3-1
- fix segfault in su when pam_ssh_agent_auth is used and the ssh-agent
  is not running, most probably not exploitable
- update pam_ssh_agent_auth to 0.9.3 upstream version

* Fri Apr 06 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-22 + 0.9.2-32
- don't create RSA1 key in FIPS mode
- don't install sshd-keygen.service (#810419)

* Fri Mar 30 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-21 + 0.9.2-32
- fix various issues in openssh-5.9p1-required-authentications.patch

* Wed Mar 21 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-20 + 0.9.2-32
- Fix dependencies in systemd units, don't enable sshd-keygen.service (#805338)

* Wed Feb 22 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-19 + 0.9.2-32
- Look for x11 forward sockets with AI_ADDRCONFIG flag getaddrinfo (#735889)

* Mon Feb 06 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-18 + 0.9.2-32
- replace TwoFactorAuth with RequiredAuthentications[12]
  https://bugzilla.mindrot.org/show_bug.cgi?id=983

* Tue Jan 31 2012 Petr Lautrbach <plautrba@redhat.com> 5.9p1-17 + 0.9.2-32
- run privsep slave process as the users SELinux context (#781634)

* Tue Dec 13 2011 Tomas Mraz <tmraz@redhat.com> 5.9p1-16 + 0.9.2-32
- add CAVS test driver for the aes-ctr ciphers

* Sun Dec 11 2011 Tomas Mraz <tmraz@redhat.com> 5.9p1-15 + 0.9.2-32
- enable aes-ctr ciphers use the EVP engines from OpenSSL such as the AES-NI

* Tue Dec 06 2011 Petr Lautrbach <plautrba@redhat.com> 5.9p1-14 + 0.9.2-32
- warn about unsupported option UsePAM=no (#757545)

* Mon Nov 21 2011 Tomas Mraz <tmraz@redhat.com> - 5.9p1-13 + 0.9.2-32
- add back the restorecon call to ssh-copy-id - it might be needed on older
  distributions (#739989)

* Fri Nov 18 2011 Tomas Mraz <tmraz@redhat.com> - 5.9p1-12 + 0.9.2-32
- still support /etc/sysconfig/sshd loading in sshd service (#754732)
- fix incorrect key permissions generated by sshd-keygen script (#754779)

* Fri Oct 14 2011 Tomas Mraz <tmraz@redhat.com> - 5.9p1-11 + 0.9.2-32
- remove unnecessary requires on initscripts
- set VerifyHostKeyDNS to ask in the default configuration (#739856)

* Mon Sep 19 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-10 + 0.9.2-32
- selinux sandbox rewrite
- two factor authentication tweaking

* Wed Sep 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-9 + 0.9.2-32
- coverity upgrade
- wipe off nonfunctional nss
- selinux sandbox tweaking

* Tue Sep 13 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-8 + 0.9.2-32
- coverity upgrade
- experimental selinux sandbox

* Tue Sep 13 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-7 + 0.9.2-32
- fully reanable auditing

* Mon Sep 12 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-6 + 0.9.2-32
- repair signedness in akc patch

* Mon Sep 12 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-5 + 0.9.2-32
- temporarily disable part of audit4 patch

* Fri Sep  9 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-3 + 0.9.2-32
- Coverity second pass
- Reenable akc patch

* Thu Sep  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-2 + 0.9.2-32
- Coverity first pass

* Wed Sep  7 2011 Jan F. Chadima <jchadima@redhat.com> - 5.9p1-1 + 0.9.2-32
- Rebase to 5.9p1
- Add chroot sftp patch
- Add two factor auth patch

* Tue Aug 23 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-21 + 0.9.2-31
- ignore SIGPIPE in ssh keyscan

* Tue Aug  9 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-20 + 0.9.2-31
- save ssh-askpass's debuginfo

* Mon Aug  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-19 + 0.9.2-31
- compile ssh-askpass with corect CFLAGS

* Mon Aug  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-18 + 0.9.2-31
- improve selinux's change context log 

* Mon Aug  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-17 + 0.9.2-31
- repair broken man pages

* Mon Jul 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-16 + 0.9.2-31
- rebuild due to broken rpmbiild

* Thu Jul 21 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-15 + 0.9.2-31
- Do not change context when run under unconfined_t

* Thu Jul 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-14 + 0.9.2-31
- Add postlogin to pam. (#718807)

* Tue Jun 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-12 + 0.9.2-31
- Systemd compatibility according to Mathieu Bridon <bochecha@fedoraproject.org>
- Split out the host keygen into their own command, to ease future migration
  to systemd. Compatitbility with the init script was kept.
- Migrate the package to full native systemd unit files, according to the Fedora
  packaging guidelines.
- Prepate the unit files for running an ondemand server. (do not add it actually)

* Tue Jun 21 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-10 + 0.9.2-31
- Mention IPv6 usage in man pages

* Mon Jun 20 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-9 + 0.9.2-31
- Improve init script

* Thu Jun 16 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-7 + 0.9.2-31
- Add possibility to compile openssh without downstream patches

* Thu Jun  9 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-6 + 0.9.2-31
- remove stale control sockets (#706396)

* Tue May 31 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-5 + 0.9.2-31
- improove entropy manuals

* Fri May 27 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-4 + 0.9.2-31
- improove entropy handling
- concat ldap patches

* Tue May 24 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-3 + 0.9.2-31
- improove ldap manuals

* Mon May 23 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-2 + 0.9.2-31
- add gssapi forced command

* Tue May  3 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p2-1 + 0.9.2-31
- update the openssh version

* Thu Apr 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-34 + 0.9.2-30
- temporarily disabling systemd units

* Wed Apr 27 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-33 + 0.9.2-30
- add flags AI_V4MAPPED and AI_ADDRCONFIG to getaddrinfo

* Tue Apr 26 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-32 + 0.9.2-30
- update scriptlets

* Fri Apr 22 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-30 + 0.9.2-30
- add systemd units

* Fri Apr 22 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-28 + 0.9.2-30
- improving sshd -> passwd transation
- add template for .local domain to sshd_config

* Thu Apr 21 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-27 + 0.9.2-30
- the private keys may be 640 root:ssh_keys ssh_keysign is sgid

* Wed Apr 20 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-26 + 0.9.2-30
- improving sshd -> passwd transation

* Tue Apr  5 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-25 + 0.9.2-30
- the intermediate context is set to sshd_sftpd_t
- do not crash in packet.c if no connection

* Thu Mar 31 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-24 + 0.9.2-30
- resolve warnings in port_linux.c

* Tue Mar 29 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-23 + 0.9.2-30
- add /etc/sysconfig/sshd

* Mon Mar 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-22 + 0.9.2-30
- improve reseeding and seed source (documentation)

* Tue Mar 22 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-20 + 0.9.2-30
- use /dev/random or /dev/urandom for seeding prng
- improve periodical reseeding of random generator

* Thu Mar 17 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-18 + 0.9.2-30
- add periodical reseeding of random generator 
- change selinux contex for internal sftp in do_usercontext
- exit(0) after sigterm

* Thu Mar 10 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-17 + 0.9.2-30
- improove ssh-ldap (documentation)

* Tue Mar  8 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-16 + 0.9.2-30
- improve session keys audit

* Mon Mar  7 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-15 + 0.9.2-30
- CVE-2010-4755

* Fri Mar  4 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-14 + 0.9.2-30
- improove ssh-keycat (documentation)

* Thu Mar  3 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-13 + 0.9.2-30
- improve audit of logins and auths

* Tue Mar  1 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-12 + 0.9.2-30
- improove ssk-keycat

* Mon Feb 28 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-11 + 0.9.2-30
- add ssk-keycat

* Fri Feb 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-10 + 0.9.2-30
- reenable auth-keys ldap backend

* Fri Feb 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-9 + 0.9.2-30
- another audit improovements

* Thu Feb 24 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-8 + 0.9.2-30
- another audit improovements
- switchable fingerprint mode

* Thu Feb 17 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-4 + 0.9.2-30
- improve audit of server key management

* Wed Feb 16 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-3 + 0.9.2-30
- improve audit of logins and auths

* Mon Feb 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.8p1-1 + 0.9.2-30
- bump openssh version to 5.8p1

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.6p1-30.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb  7 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-30 + 0.9.2-29
- clean the data structures in the non privileged process
- clean the data structures when roaming

* Wed Feb  2 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-28 + 0.9.2-29
- clean the data structures in the privileged process

* Tue Jan 25 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-25 + 0.9.2-29
- clean the data structures before exit net process

* Mon Jan 17 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-24 + 0.9.2-29
- make audit compatible with the fips mode

* Fri Jan 14 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-23 + 0.9.2-29
- add audit of destruction the server keys

* Wed Jan 12 2011 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-22 + 0.9.2-29
- add audit of destruction the session keys

* Fri Dec 10 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-21 + 0.9.2-29
- reenable run sshd as non root user
- renable rekeying

* Wed Nov 24 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-20 + 0.9.2-29
- reapair clientloop crash (#627332)
- properly restore euid in case connect to the ssh-agent socket fails

* Mon Nov 22 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-19 + 0.9.2-28
- striped read permissions from suid and sgid binaries

* Mon Nov 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-18 + 0.9.2-27
- used upstream version of the biguid patch

* Mon Nov 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-17 + 0.9.2-27
- improoved kuserok patch

* Fri Nov  5 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-16 + 0.9.2-27
- add auditing the host based key ussage
- repait X11 abstract layer socket (#648896)

* Wed Nov  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-15 + 0.9.2-27
- add auditing the kex result

* Tue Nov  2 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-14 + 0.9.2-27
- add auditing the key ussage

* Wed Oct 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-12 + 0.9.2-27
- update gsskex patch (#645389)

* Wed Oct 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-11 + 0.9.2-27
- rebase linux audit according to upstream

* Fri Oct  1 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-10 + 0.9.2-27
- add missing headers to linux audit

* Wed Sep 29 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-9 + 0.9.2-27
- audit module now uses openssh audit framevork

* Wed Sep 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-8 + 0.9.2-27
- Add the GSSAPI kuserok switch to the kuserok patch

* Wed Sep 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-7 + 0.9.2-27
- Repaired the kuserok patch

* Mon Sep 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-6 + 0.9.2-27
- Repaired the problem with puting entries with very big uid into lastlog

* Mon Sep 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-5 + 0.9.2-27
- Merging selabel patch with the upstream version. (#632914)

* Mon Sep 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-4 + 0.9.2-27
- Tweaking selabel patch to work properly without selinux rules loaded. (#632914)

* Wed Sep  8 2010 Tomas Mraz <tmraz@redhat.com> - 5.6p1-3 + 0.9.2-27
- Make fipscheck hmacs compliant with FHS - requires new fipscheck

* Fri Sep  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-2 + 0.9.2-27
- Added -z relro -z now to LDFLAGS

* Fri Sep  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.6p1-1 + 0.9.2-27
- Rebased to openssh5.6p1

* Wed Jul  7 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-18 + 0.9.2-26
- merged with newer bugzilla's version of authorized keys command patch

* Wed Jun 30 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-17 + 0.9.2-26
- improved the x11 patch according to upstream (#598671)

* Fri Jun 25 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-16 + 0.9.2-26
- improved the x11 patch (#598671)

* Thu Jun 24 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-15 + 0.9.2-26
- changed _PATH_UNIX_X to unexistent file name (#598671)

* Wed Jun 23 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-14 + 0.9.2-26
- sftp works in deviceless chroot again (broken from 5.5p1-3)

* Tue Jun  8 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-13 + 0.9.2-26
- add option to switch out krb5_kuserok

* Fri May 21 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-12 + 0.9.2-26
- synchronize uid and gid for the user sshd

* Thu May 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-11 + 0.9.2-26
- Typo in ssh-ldap.conf(5) and ssh-ladap-helper(8)

* Fri May 14 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-10 + 0.9.2-26
- Repair the reference in man ssh-ldap-helper(8)
- Repair the PubkeyAgent section in sshd_config(5)
- Provide example ldap.conf

* Thu May 13 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-9 + 0.9.2-26
- Make the Ldap configuration widely compatible
- create the aditional docs for LDAP support.

* Thu May  6 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-8 + 0.9.2-26
- Make LDAP config elements TLS_CACERT and TLS_REQCERT compatiple with pam_ldap (#589360)

* Thu May  6 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-7 + 0.9.2-26
- Make LDAP config element tls_checkpeer compatiple with nss_ldap (#589360)

* Tue May  4 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-6 + 0.9.2-26
- Comment spec.file
- Sync patches from upstream

* Mon May  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-5 + 0.9.2-26
- Create separate ldap package
- Tweak the ldap patch
- Rename stderr patch properly

* Thu Apr 29 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-4 + 0.9.2-26
- Added LDAP support

* Mon Apr 26 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-3 + 0.9.2-26
- Ignore .bashrc output to stderr in the subsystems

* Tue Apr 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-2 + 0.9.2-26
- Drop dependency on man

* Fri Apr 16 2010 Jan F. Chadima <jchadima@redhat.com> - 5.5p1-1 + 0.9.2-26
- Update to 5.5p1

* Fri Mar 12 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-3 + 0.9.2-25
- repair configure script of pam_ssh_agent
- repair error mesage in ssh-keygen

* Fri Mar 12 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-2
- source krb5-devel profile script only if exists

* Tue Mar  9 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-1
- Update to 5.4p1
- discontinued support for nss-keys
- discontinued support for scard

* Wed Mar  3 2010 Jan F. Chadima <jchadima@redhat.com> - 5.4p1-0.snap20100302.1
- Prepare update to 5.4p1

* Mon Feb 15 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-22
- ImplicitDSOLinking (#564824)

* Fri Jan 29 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-21
- Allow to use hardware crypto if awailable (#559555)

* Mon Jan 25 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-20
- optimized FD_CLOEXEC on accept socket (#541809)

* Mon Jan 25 2010 Tomas Mraz <tmraz@redhat.com> - 5.3p1-19
- updated pam_ssh_agent_auth to new version from upstream (just
  a licence change)

* Thu Jan 21 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-18
- optimized RAND_cleanup patch (#557166)

* Wed Jan 20 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-17
- add RAND_cleanup at the exit of each program using RAND (#557166)

* Tue Jan 19 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-16
- set FD_CLOEXEC on accepted socket (#541809)

* Fri Jan  8 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-15
- replaced define by global in macros

* Tue Jan  5 2010 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-14
- Update the pka patch

* Mon Dec 21 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-13
- Update the audit patch

* Fri Dec  4 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-12
- Add possibility to autocreate only RSA key into initscript (#533339)

* Fri Nov 27 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-11
- Prepare NSS key patch for future SEC_ERROR_LOCKED_PASSWORD (#537411)

* Tue Nov 24 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-10
- Update NSS key patch (#537411, #356451)

* Fri Nov 20 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-9
- Add gssapi key exchange patch (#455351)

* Fri Nov 20 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-8
- Add public key agent patch (#455350)

* Mon Nov  2 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-7
- Repair canohost patch to allow gssapi to work when host is acessed via pipe proxy (#531849)

* Thu Oct 29 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-6
- Modify the init script to prevent it to hang during generating the keys (#515145)

* Tue Oct 27 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-5
- Add README.nss

* Mon Oct 19 2009 Tomas Mraz <tmraz@redhat.com> - 5.3p1-4
- Add pam_ssh_agent_auth module to a subpackage.

* Fri Oct 16 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-3
- Reenable audit.

* Fri Oct  2 2009 Jan F. Chadima <jchadima@redhat.com> - 5.3p1-2
- Upgrade to new wersion 5.3p1

* Tue Sep 29 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-29
- Resolve locking in ssh-add (#491312)

* Thu Sep 24 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-28
- Repair initscript to be acord to guidelines (#521860)
- Add bugzilla# to application of edns and xmodifiers patch

* Wed Sep 16 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-26
- Changed pam stack to password-auth

* Fri Sep 11 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-25
- Dropped homechroot patch

* Mon Sep  7 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-24
- Add check for nosuid, nodev in homechroot

* Tue Sep  1 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-23
- add correct patch for ip-opts

* Tue Sep  1 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-22
- replace ip-opts patch by an upstream candidate version

* Mon Aug 31 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-21
- rearange selinux patch to be acceptable for upstream
- replace seftp patch by an upstream version

* Fri Aug 28 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-20
- merged xmodifiers to redhat patch
- merged gssapi-role to selinux patch
- merged cve-2007_3102 to audit patch
- sesftp patch only with WITH_SELINUX flag
- rearange sesftp patch according to upstream request

* Wed Aug 26 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-19
- minor change in sesftp patch

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-18
- rebuilt with new openssl

* Thu Jul 30 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-17
- Added dnssec support. (#205842)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2p1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jul 24 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-15
- only INTERNAL_SFTP can be home-chrooted
- save _u and _r parts of context changing to sftpd_t

* Fri Jul 17 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-14
- changed internal-sftp context to sftpd_t

* Fri Jul  3 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-13
- changed home length path patch to upstream version

* Tue Jun 30 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-12
- create '~/.ssh/known_hosts' within proper context

* Mon Jun 29 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-11
- length of home path in ssh now limited by PATH_MAX
- correct timezone with daylight processing

* Sat Jun 27 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-10
- final version chroot %%h (sftp only)

* Tue Jun 23 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-9
- repair broken ls in chroot %%h

* Fri Jun 12 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-8
- add XMODIFIERS to exported environment (#495690)

* Fri May 15 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-6
- allow only protocol 2 in the FIPS mode

* Thu Apr 30 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-5
- do integrity verification only on binaries which are part
  of the OpenSSH FIPS modules

* Mon Apr 20 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-4
- log if FIPS mode is initialized
- make aes-ctr cipher modes work in the FIPS mode

* Fri Apr  3 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-3
- fix logging after chroot
- enable non root users to use chroot %%h in internal-sftp

* Fri Mar 13 2009 Tomas Mraz <tmraz@redhat.com> - 5.2p1-2
- add AES-CTR ciphers to the FIPS mode proposal

* Mon Mar  9 2009 Jan F. Chadima <jchadima@redhat.com> - 5.2p1-1
- upgrade to new upstream release

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1p1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 12 2009 Tomas Mraz <tmraz@redhat.com> - 5.1p1-7
- drop obsolete triggers
- add testing FIPS mode support
- LSBize the initscript (#247014)

* Fri Jan 30 2009 Tomas Mraz <tmraz@redhat.com> - 5.1p1-6
- enable use of ssl engines (#481100)

* Thu Jan 15 2009 Tomas Mraz <tmraz@redhat.com> - 5.1p1-5
- remove obsolete --with-rsh (#478298)
- add pam_sepermit to allow blocking confined users in permissive mode
  (#471746)
- move system-auth after pam_selinux in the session stack

* Thu Dec 11 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-4
- set FD_CLOEXEC on channel sockets (#475866)
- adjust summary
- adjust nss-keys patch so it is applicable without selinux patches (#470859)

* Fri Oct 17 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-3
- fix compatibility with some servers (#466818)

* Thu Jul 31 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-2
- fixed zero length banner problem (#457326)

* Wed Jul 23 2008 Tomas Mraz <tmraz@redhat.com> - 5.1p1-1
- upgrade to new upstream release
- fixed a problem with public key authentication and explicitely
  specified SELinux role

* Wed May 21 2008 Tomas Mraz <tmraz@redhat.com> - 5.0p1-3
- pass the connection socket to ssh-keysign (#447680)

* Mon May 19 2008 Tomas Mraz <tmraz@redhat.com> - 5.0p1-2
- add LANGUAGE to accepted/sent environment variables (#443231)
- use pam_selinux to obtain the user context instead of doing it itself
- unbreak server keep alive settings (patch from upstream)
- small addition to scp manpage

* Mon Apr  7 2008 Tomas Mraz <tmraz@redhat.com> - 5.0p1-1
- upgrade to new upstream (#441066)
- prevent initscript from killing itself on halt with upstart (#438449)
- initscript status should show that the daemon is running
  only when the main daemon is still alive (#430882)

* Thu Mar  6 2008 Tomas Mraz <tmraz@redhat.com> - 4.7p1-10
- fix race on control master and cleanup stale control socket (#436311)
  patches by David Woodhouse

* Fri Feb 29 2008 Tomas Mraz <tmraz@redhat.com> - 4.7p1-9
- set FD_CLOEXEC on client socket
- apply real fix for window size problem (#286181) from upstream
- apply fix for the spurious failed bind from upstream
- apply open handle leak in sftp fix from upstream

* Tue Feb 12 2008 Dennis Gilmore <dennis@ausil.us> - 4.7p1-8
- we build for sparcv9 now  and it needs -fPIE

* Thu Jan  3 2008 Tomas Mraz <tmraz@redhat.com> - 4.7p1-7
- fix gssapi auth with explicit selinux role requested (#427303) - patch
  by Nalin Dahyabhai

* Tue Dec  4 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-6
- explicitly source krb5-devel profile script

* Tue Dec 04 2007 Release Engineering <rel-eng at fedoraproject dot org> - 4.7p1-5
- Rebuild for openssl bump

* Tue Nov 20 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-4
- do not copy /etc/localtime into the chroot as it is not
  necessary anymore (#193184)
- call setkeycreatecon when selinux context is established
- test for NULL privk when freeing key (#391871) - patch by
  Pierre Ossman

* Mon Sep 17 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-2
- revert default window size adjustments (#286181)

* Thu Sep  6 2007 Tomas Mraz <tmraz@redhat.com> - 4.7p1-1
- upgrade to latest upstream
- use libedit in sftp (#203009)
- fixed audit log injection problem (CVE-2007-3102)

* Thu Aug  9 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-8
- fix sftp client problems on write error (#247802)
- allow disabling autocreation of server keys (#235466)

* Wed Jun 20 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-7
- experimental NSS keys support
- correctly setup context when empty level requested (#234951)

* Tue Mar 20 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-6
- mls level check must be done with default role same as requested

* Mon Mar 19 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-5
- make profile.d/gnome-ssh-askpass.* regular files (#226218)

* Tue Feb 27 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-4
- reject connection if requested mls range is not obtained (#229278)

* Thu Feb 22 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-3
- improve Buildroot
- remove duplicate /etc/ssh from files

* Tue Jan 16 2007 Tomas Mraz <tmraz@redhat.com> - 4.5p1-2
- support mls on labeled networks (#220487)
- support mls level selection on unlabeled networks
- allow / in usernames in scp (only beginning /, ./, and ../ is special) 

* Thu Dec 21 2006 Tomas Mraz <tmraz@redhat.com> - 4.5p1-1
- update to 4.5p1 (#212606)

* Thu Nov 30 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-14
- fix gssapi with DNS loadbalanced clusters (#216857)

* Tue Nov 28 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-13
- improved pam_session patch so it doesn't regress, the patch is necessary
  for the pam_session_close to be called correctly as uid 0

* Fri Nov 10 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-12
- CVE-2006-5794 - properly detect failed key verify in monitor (#214641)

* Thu Nov  2 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-11
- merge sshd initscript patches
- kill all ssh sessions when stop is called in halt or reboot runlevel
- remove -TERM option from killproc so we don't race on sshd restart

* Mon Oct  2 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-10
- improve gssapi-no-spnego patch (#208102)
- CVE-2006-4924 - prevent DoS on deattack detector (#207957)
- CVE-2006-5051 - don't call cleanups from signal handler (#208459)

* Wed Aug 23 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-9
- don't report duplicate syslog messages, use correct local time (#189158)
- don't allow spnego as gssapi mechanism (from upstream)
- fixed memleaks found by Coverity (from upstream)
- allow ip options except source routing (#202856) (patch by HP)

* Tue Aug  8 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-8
- drop the pam-session patch from the previous build (#201341)
- don't set IPV6_V6ONLY sock opt when listening on wildcard addr (#201594)

* Thu Jul 20 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-7
- dropped old ssh obsoletes
- call the pam_session_open/close from the monitor when privsep is
  enabled so it is always called as root (patch by Darren Tucker)

* Mon Jul 17 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-6
- improve selinux patch (by Jan Kiszka)
- upstream patch for buffer append space error (#191940)
- fixed typo in configure.ac (#198986)
- added pam_keyinit to pam configuration (#198628)
- improved error message when askpass dialog cannot grab
  keyboard input (#198332)
- buildrequires xauth instead of xorg-x11-xauth
- fixed a few rpmlint warnings

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.3p2-5.1
- rebuild

* Fri Apr 14 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-5
- don't request pseudoterminal allocation if stdin is not tty (#188983)

* Thu Mar  2 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-4
- allow access if audit is not compiled in kernel (#183243)

* Fri Feb 24 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-3
- enable the subprocess in chroot to send messages to system log
- sshd should prevent login if audit call fails

* Tue Feb 21 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-2
- print error from scp if not remote (patch by Bjorn Augustsson #178923)

* Mon Feb 13 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p2-1
- new version

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.3p1-2.1
- bump again for double-long bug on ppc(64)

* Mon Feb  6 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p1-2
- fixed another place where syslog was called in signal handler
- pass locale environment variables to server, accept them there (#179851)

* Wed Feb  1 2006 Tomas Mraz <tmraz@redhat.com> - 4.3p1-1
- new version, dropped obsolete patches

* Tue Dec 20 2005 Tomas Mraz <tmraz@redhat.com> - 4.2p1-10
- hopefully make the askpass dialog less confusing (#174765)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov 22 2005 Tomas Mraz <tmraz@redhat.com> - 4.2p1-9
- drop x11-ssh-askpass from the package
- drop old build_6x ifs from spec file
- improve gnome-ssh-askpass so it doesn't reveal number of passphrase 
  characters to person looking at the display
- less hackish fix for the __USE_GNU problem

* Fri Nov 18 2005 Nalin Dahyabhai <nalin@redhat.com> - 4.2p1-8
- work around missing gccmakedep by wrapping makedepend in a local script
- remove now-obsolete build dependency on "xauth"

* Thu Nov 17 2005 Warren Togami <wtogami@redhat.com> - 4.2p1-7
- xorg-x11-devel -> libXt-devel
- rebuild for new xauth location so X forwarding works
- buildreq audit-libs-devel
- buildreq automake for aclocal
- buildreq imake for xmkmf
-  -D_GNU_SOURCE in flags in order to get it to build
   Ugly hack to workaround openssh defining __USE_GNU which is
   not allowed and causes problems according to Ulrich Drepper
   fix this the correct way after FC5test1

* Wed Nov  9 2005 Jeremy Katz <katzj@redhat.com> - 4.2p1-6
- rebuild against new openssl

* Fri Oct 28 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-5
- put back the possibility to skip SELinux patch
- add patch for user login auditing by Steve Grubb

* Tue Oct 18 2005 Dan Walsh <dwalsh@redhat.com> 4.2p1-4
- Change selinux patch to use get_default_context_with_rolelevel in libselinux.

* Thu Oct 13 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-3
- Update selinux patch to use getseuserbyname

* Fri Oct  7 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-2
- use include instead of pam_stack in pam config
- use fork+exec instead of system in scp - CVE-2006-0225 (#168167)
- upstream patch for displaying authentication errors

* Tue Sep 06 2005 Tomas Mraz <tmraz@redhat.com> 4.2p1-1
- upgrade to a new upstream version

* Tue Aug 16 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-5
- use x11-ssh-askpass if openssh-askpass-gnome is not installed (#165207)
- install ssh-copy-id from contrib (#88707)

* Wed Jul 27 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-4
- don't deadlock on exit with multiple X forwarded channels (#152432)
- don't use X11 port which can't be bound on all IP families (#163732)

* Wed Jun 29 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-3
- fix small regression caused by the nologin patch (#161956)
- fix race in getpeername error checking (mindrot #1054)

* Thu Jun  9 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-2
- use only pam_nologin for nologin testing

* Mon Jun  6 2005 Tomas Mraz <tmraz@redhat.com> 4.1p1-1
- upgrade to a new upstream version
- call pam_loginuid as a pam session module

* Mon May 16 2005 Tomas Mraz <tmraz@redhat.com> 4.0p1-3
- link libselinux only to sshd (#157678)

* Mon Apr  4 2005 Tomas Mraz <tmraz@redhat.com> 4.0p1-2
- fixed Local/RemoteForward in ssh_config.5 manpage
- fix fatal when Local/RemoteForward is used and scp run (#153258)
- don't leak user validity when using krb5 authentication

* Thu Mar 24 2005 Tomas Mraz <tmraz@redhat.com> 4.0p1-1
- upgrade to 4.0p1
- remove obsolete groups patch

* Wed Mar 16 2005 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 28 2005 Nalin Dahyabhai <nalin@redhat.com> 3.9p1-12
- rebuild so that configure can detect that krb5_init_ets is gone now

* Mon Feb 21 2005 Tomas Mraz <tmraz@redhat.com> 3.9p1-11
- don't call syslog in signal handler
- allow password authentication when copying from remote
  to remote machine (#103364)

* Wed Feb  9 2005 Tomas Mraz <tmraz@redhat.com>
- add spaces to messages in initscript (#138508)

* Tue Feb  8 2005 Tomas Mraz <tmraz@redhat.com> 3.9p1-10
- enable trusted forwarding by default if X11 forwarding is 
  required by user (#137685 and duplicates)
- disable protocol 1 support by default in sshd server config (#88329)
- keep the gnome-askpass dialog above others (#69131)

* Fri Feb  4 2005 Tomas Mraz <tmraz@redhat.com>
- change permissions on pam.d/sshd to 0644 (#64697)
- patch initscript so it doesn't kill opened sessions if
  the sshd daemon isn't running anymore (#67624)

* Mon Jan  3 2005 Bill Nottingham <notting@redhat.com> 3.9p1-9
- don't use initlog

* Mon Nov 29 2004 Thomas Woerner <twoerner@redhat.com> 3.9p1-8.1
- fixed PIE build for all architectures

* Mon Oct  4 2004 Nalin Dahyabhai <nalin@redhat.com> 3.9p1-8
- add a --enable-vendor-patchlevel option which allows a ShowPatchLevel option
  to enable display of a vendor patch level during version exchange (#120285)
- configure with --disable-strip to build useful debuginfo subpackages

* Mon Sep 20 2004 Bill Nottingham <notting@redhat.com> 3.9p1-7
- when using gtk2 for askpass, don't buildprereq gnome-libs-devel

* Tue Sep 14 2004 Nalin Dahyabhai <nalin@redhat.com> 3.9p1-6
- build

* Mon Sep 13 2004 Nalin Dahyabhai <nalin@redhat.com>
- disable ACSS support

* Thu Sep 2 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-5
- Change selinux patch to use get_default_context_with_role in libselinux.

* Thu Sep 2 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-4
- Fix patch
	* Bad debug statement.
	* Handle root/sysadm_r:kerberos

* Thu Sep 2 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-3
- Modify Colin Walter's patch to allow specifying rule during connection

* Tue Aug 31 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-2
- Fix TTY handling for SELinux

* Tue Aug 24 2004 Daniel Walsh <dwalsh@redhat.com> 3.9p1-1
- Update to upstream

* Sun Aug 1 2004 Alan Cox <alan@redhat.com> 3.8.1p1-5
- Apply buildreq fixup patch (#125296)

* Tue Jun 15 2004 Daniel Walsh <dwalsh@redhat.com> 3.8.1p1-4
- Clean up patch for upstream submission.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jun 9 2004 Daniel Walsh <dwalsh@redhat.com> 3.8.1p1-2
- Remove use of pam_selinux and patch selinux in directly.  

* Mon Jun  7 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.1p1-1
- request gssapi-with-mic by default but not delegation (flag day for anyone
  who used previous gssapi patches)
- no longer request x11 forwarding by default

* Thu Jun 3 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-36
- Change pam file to use open and close with pam_selinux

* Tue Jun  1 2004 Nalin Dahyabhai <nalin@redhat.com> 3.8.1p1-0
- update to 3.8.1p1
- add workaround from CVS to reintroduce passwordauth using pam

* Tue Jun 1 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-35
- Remove CLOSEXEC on STDERR

* Tue Mar 16 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-34

* Wed Mar 03 2004 Phil Knirsch <pknirsch@redhat.com> 3.6.1p2-33.30.1
- Built RHLE3 U2 update package.

* Wed Mar 3 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-33
- Close file descriptors on exec 

* Mon Mar  1 2004 Thomas Woerner <twoerner@redhat.com> 3.6.1p2-32
- fixed pie build

* Thu Feb 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-31
- Add restorecon to startup scripts

* Thu Feb 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-30
- Add multiple qualified to openssh

* Mon Feb 23 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-29
- Eliminate selinux code and use pam_selinux

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jan 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-27
- turn off pie on ppc

* Mon Jan 26 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-26
- fix is_selinux_enabled

* Wed Jan 14 2004 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-25
- Rebuild to grab shared libselinux

* Wed Dec 3 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-24
- turn on selinux

* Tue Nov 18 2003 Nalin Dahyabhai <nalin@redhat.com>
- un#ifdef out code for reporting password expiration in non-privsep
  mode (#83585)

* Mon Nov 10 2003 Nalin Dahyabhai <nalin@redhat.com>
- add machinery to build with/without -fpie/-pie, default to doing so

* Thu Nov 06 2003 David Woodhouse <dwmw2@redhat.com> 3.6.1p2-23
- Don't whinge about getsockopt failing (#109161)

* Fri Oct 24 2003 Nalin Dahyabhai <nalin@redhat.com>
- add missing buildprereq on zlib-devel (#104558)

* Mon Oct 13 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-22
- turn selinux off

* Mon Oct 13 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-21.sel
- turn selinux on

* Fri Sep 19 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-21
- turn selinux off

* Fri Sep 19 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-20.sel
- turn selinux on

* Fri Sep 19 2003 Nalin Dahyabhai <nalin@redhat.com>
- additional fix for apparently-never-happens double-free in buffer_free()
- extend fix for #103998 to cover SSH1

* Wed Sep 17 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-19
- rebuild

* Wed Sep 17 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-18
- additional buffer manipulation cleanups from Solar Designer

* Wed Sep 17 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-17
- turn selinux off

* Wed Sep 17 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-16.sel
- turn selinux on

* Tue Sep 16 2003 Bill Nottingham <notting@redhat.com> 3.6.1p2-15
- rebuild

* Tue Sep 16 2003 Bill Nottingham <notting@redhat.com> 3.6.1p2-14
- additional buffer manipulation fixes (CAN-2003-0695)

* Tue Sep 16 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-13.sel
- turn selinux on

* Tue Sep 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-12
- rebuild

* Tue Sep 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-11
- apply patch to store the correct buffer size in allocated buffers
  (CAN-2003-0693)
- skip the initial PAM authentication attempt with an empty password if
  empty passwords are not permitted in our configuration (#103998)

* Fri Sep 5 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-10
- turn selinux off

* Fri Sep 5 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-9.sel
- turn selinux on

* Tue Aug 26 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-8
- Add BuildPreReq gtk2-devel if gtk2

* Tue Aug 12 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-7
- rebuild

* Tue Aug 12 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-6
- modify patch which clears the supplemental group list at startup to only
  complain if setgroups() fails if sshd has euid == 0
- handle krb5 installed in %%{_prefix} or elsewhere by using krb5-config

* Mon Jul 28 2003 Daniel Walsh <dwalsh@redhat.com> 3.6.1p2-5
- Add SELinux patch

* Tue Jul 22 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-4
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-3
- rebuild

* Wed Jul 16 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-2
- rebuild

* Thu Jun  5 2003 Nalin Dahyabhai <nalin@redhat.com> 3.6.1p2-1
- update to 3.6.1p2

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
6 rebuilt

* Mon Mar 24 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch for getsockopt() call to work on bigendian 64bit archs

* Fri Feb 14 2003 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-6
- move scp to the -clients subpackage, because it directly depends on ssh
  which is also in -clients (#84329)

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-5
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-3
- rebuild

* Tue Nov 12 2002 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-2
- patch PAM configuration to use relative path names for the modules, allowing
  us to not worry about which arch the modules are built for on multilib systems

* Tue Oct 15 2002 Nalin Dahyabhai <nalin@redhat.com> 3.5p1-1
- update to 3.5p1, merging in filelist/perm changes from the upstream spec

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 3.4p1-3
- merge

* Thu Sep 12 2002  Than Ngo <than@redhat.com> 3.4p1-2.1
- fix to build on multilib systems

* Thu Aug 29 2002 Curtis Zinzilieta <curtisz@redhat.com> 3.4p1-2gss
- added gssapi patches and uncommented patch here

* Wed Aug 14 2002 Nalin Dahyabhai <nalin@redhat.com> 3.4p1-2
- pull patch from CVS to fix too-early free in ssh-keysign (#70009)

* Thu Jun 27 2002 Nalin Dahyabhai <nalin@redhat.com> 3.4p1-1
- 3.4p1
- drop anon mmap patch

* Tue Jun 25 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3p1-2
- rework the close-on-exit docs
- include configuration file man pages
- make use of nologin as the privsep shell optional

* Mon Jun 24 2002 Nalin Dahyabhai <nalin@redhat.com> 3.3p1-1
- update to 3.3p1
- merge in spec file changes from upstream (remove setuid from ssh, ssh-keysign)
- disable gtk2 askpass
- require pam-devel by filename rather than by package for erratum
- include patch from Solar Designer to work around anonymous mmap failures

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Jun  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.3p1-3
- don't require autoconf any more

* Fri May 31 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.3p1-2
- build gnome-ssh-askpass with gtk2

* Tue May 28 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.3p1-1
- update to 3.2.3p1
- merge in spec file changes from upstream

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.2.2p1-1
- update to 3.2.2p1

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-4
- drop buildreq on db1-devel
- require pam-devel by package name
- require autoconf instead of autoconf253 again

* Tue Apr  2 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-3
- pull patch from CVS to avoid printing error messages when some of the
  default keys aren't available when running ssh-add
- refresh to current revisions of Simon's patches
 
* Thu Mar 21 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-2gss
- reintroduce Simon's gssapi patches
- add buildprereq for autoconf253, which is needed to regenerate configure
  after applying the gssapi patches
- refresh to the latest version of Markus's patch to build properly with
  older versions of OpenSSL

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-2
- bump and grind (through the build system)

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-1
- require sharutils for building (mindrot #137)
- require db1-devel only when building for 6.x (#55105), which probably won't
  work anyway (3.1 requires OpenSSL 0.9.6 to build), but what the heck
- require pam-devel by file (not by package name) again
- add Markus's patch to compile with OpenSSL 0.9.5a (from
  http://bugzilla.mindrot.org/show_bug.cgi?id=141) and apply it if we're
  building for 6.x

* Thu Mar  7 2002 Nalin Dahyabhai <nalin@redhat.com> 3.1p1-0
- update to 3.1p1

* Tue Mar  5 2002 Nalin Dahyabhai <nalin@redhat.com> SNAP-20020305
- update to SNAP-20020305
- drop debug patch, fixed upstream

* Wed Feb 20 2002 Nalin Dahyabhai <nalin@redhat.com> SNAP-20020220
- update to SNAP-20020220 for testing purposes (you've been warned, if there's
  anything to be warned about, gss patches won't apply, I don't mind)

* Wed Feb 13 2002 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-3
- add patches from Simon Wilkinson and Nicolas Williams for GSSAPI key
  exchange, authentication, and named key support

* Wed Jan 23 2002 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-2
- remove dependency on db1-devel, which has just been swallowed up whole
  by gnome-libs-devel

* Sat Dec 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- adjust build dependencies so that build6x actually works right (fix
  from Hugo van der Kooij)

* Tue Dec  4 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.2p1-1
- update to 3.0.2p1

* Fri Nov 16 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0.1p1-1
- update to 3.0.1p1

* Tue Nov 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to current CVS (not for use in distribution)

* Thu Nov  8 2001 Nalin Dahyabhai <nalin@redhat.com> 3.0p1-1
- merge some of Damien Miller <djm@mindrot.org> changes from the upstream
  3.0p1 spec file and init script

* Wed Nov  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.0p1
- update to x11-ssh-askpass 1.2.4.1
- change build dependency on a file from pam-devel to the pam-devel package
- replace primes with moduli

* Thu Sep 27 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-9
- incorporate fix from Markus Friedl's advisory for IP-based authorization bugs

* Thu Sep 13 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.9p2-8
- Merge changes to rescue build from current sysadmin survival cd

* Thu Sep  6 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-7
- fix scp's server's reporting of file sizes, and build with the proper
  preprocessor define to get large-file capable open(), stat(), etc.
  (sftp has been doing this correctly all along) (#51827)
- configure without --with-ipv4-default on RHL 7.x and newer (#45987,#52247)
- pull cvs patch to fix support for /etc/nologin for non-PAM logins (#47298)
- mark profile.d scriptlets as config files (#42337)
- refer to Jason Stone's mail for zsh workaround for exit-hanging quasi-bug
- change a couple of log() statements to debug() statements (#50751)
- pull cvs patch to add -t flag to sshd (#28611)
- clear fd_sets correctly (one bit per FD, not one byte per FD) (#43221)

* Mon Aug 20 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9p2-6
- add db1-devel as a BuildPrerequisite (noted by Hans Ecke)

* Thu Aug 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- pull cvs patch to fix remote port forwarding with protocol 2

* Thu Aug  9 2001 Nalin Dahyabhai <nalin@redhat.com>
- pull cvs patch to add session initialization to no-pty sessions
- pull cvs patch to not cut off challengeresponse auth needlessly
- refuse to do X11 forwarding if xauth isn't there, handy if you enable
  it by default on a system that doesn't have X installed (#49263)

* Wed Aug  8 2001 Nalin Dahyabhai <nalin@redhat.com>
- don't apply patches to code we don't intend to build (spotted by Matt Galgoci)

* Mon Aug  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- pass OPTIONS correctly to initlog (#50151)

* Wed Jul 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- switch to x11-ssh-askpass 1.2.2

* Wed Jul 11 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- disable the gssapi patch

* Mon Jun 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.9p2
- refresh to a new version of the gssapi patch

* Thu Jun  7 2001 Nalin Dahyabhai <nalin@redhat.com>
- change Copyright: BSD to License: BSD
- add Markus Friedl's unverified patch for the cookie file deletion problem
  so that we can verify it
- drop patch to check if xauth is present (was folded into cookie patch)
- don't apply gssapi patches for the errata candidate
- clear supplemental groups list at startup

* Fri May 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- fix an error parsing the new default sshd_config
- add a fix from Markus Friedl (via openssh-unix-dev) for ssh-keygen not
  dealing with comments right

* Thu May 24 2001 Nalin Dahyabhai <nalin@redhat.com>
- add in Simon Wilkinson's GSSAPI patch to give it some testing in-house,
  to be removed before the next beta cycle because it's a big departure
  from the upstream version

* Thu May  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- finish marking strings in the init script for translation
- modify init script to source /etc/sysconfig/sshd and pass $OPTIONS to sshd
  at startup (change merged from openssh.com init script, originally by
  Pekka Savola)
- refuse to do X11 forwarding if xauth isn't there, handy if you enable
  it by default on a system that doesn't have X installed

* Wed May  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.9
- drop various patches that came from or went upstream or to or from CVS

* Wed Apr 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- only require initscripts 5.00 on 6.2 (reported by Peter Bieringer)

* Sun Apr  8 2001 Preston Brown <pbrown@redhat.com>
- remove explicit openssl requirement, fixes builddistro issue
- make initscript stop() function wait until sshd really dead to avoid 
  races in condrestart

* Mon Apr  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- mention that challengereponse supports PAM, so disabling password doesn't
  limit users to pubkey and rsa auth (#34378)
- bypass the daemon() function in the init script and call initlog directly,
  because daemon() won't start a daemon it detects is already running (like
  open connections)
- require the version of openssl we had when we were built

* Fri Mar 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- make do_pam_setcred() smart enough to know when to establish creds and
  when to reinitialize them
- add in a couple of other fixes from Damien for inclusion in the errata

* Thu Mar 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p2
- call setcred() again after initgroups, because the "creds" could actually
  be group memberships

* Tue Mar 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 2.5.2p1 (includes endianness fixes in the rijndael implementation)
- don't enable challenge-response by default until we find a way to not
  have too many userauth requests (we may make up to six pubkey and up to
  three password attempts as it is)
- remove build dependency on rsh to match openssh.com's packages more closely

* Sat Mar  3 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove dependency on openssl -- would need to be too precise

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Mon Feb 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- Revert the patch to move pam_open_session.
- Init script and spec file changes from Pekka Savola. (#28750)
- Patch sftp to recognize '-o protocol' arguments. (#29540)

* Thu Feb 22 2001 Nalin Dahyabhai <nalin@redhat.com>
- Chuck the closing patch.
- Add a trigger to add host keys for protocol 2 to the config file, now that
  configuration file syntax requires us to specify it with HostKey if we
  specify any other HostKey values, which we do.

* Tue Feb 20 2001 Nalin Dahyabhai <nalin@redhat.com>
- Redo patch to move pam_open_session after the server setuid()s to the user.
- Rework the nopam patch to use be picked up by autoconf.

* Mon Feb 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.1p1.
- Add init script mods from Pekka Savola.
- Tweak the init script to match the CVS contrib script more closely.
- Redo patch to ssh-add to try to adding both identity and id_dsa to also try
  adding id_rsa.

* Fri Feb 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- Update for 2.5.0p1.
- Use $RPM_OPT_FLAGS instead of -O when building gnome-ssh-askpass
- Resync with parts of Damien Miller's openssh.spec from CVS, including
  update of x11 askpass to 1.2.0.
- Only require openssl (don't prereq) because we generate keys in the init
  script now.

* Tue Feb 13 2001 Nalin Dahyabhai <nalin@redhat.com>
- Don't open a PAM session until we've forked and become the user (#25690).
- Apply Andrew Bartlett's patch for letting pam_authenticate() know which
  host the user is attempting a login from.
- Resync with parts of Damien Miller's openssh.spec from CVS.
- Don't expose KbdInt responses in debug messages (from CVS).
- Detect and handle errors in rsa_{public,private}_decrypt (from CVS).

* Wed Feb  7 2001 Trond Eivind Glomsrxd <teg@redhat.com>
- i18n-tweak to initscript.

* Tue Jan 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- More gettextizing.
- Close all files after going into daemon mode (needs more testing).
- Extract patch from CVS to handle auth banners (in the client).
- Extract patch from CVS to handle compat weirdness.

* Fri Jan 19 2001 Nalin Dahyabhai <nalin@redhat.com>
- Finish with the gettextizing.

* Thu Jan 18 2001 Nalin Dahyabhai <nalin@redhat.com>
- Fix a bug in auth2-pam.c (#23877)
- Gettextize the init script.

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate a switch for using PAM configs for 6.x, just in case.

* Tue Dec  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Incorporate Bero's changes for a build specifically for rescue CDs.

* Wed Nov 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Don't treat pam_setcred() failure as fatal unless pam_authenticate() has
  succeeded, to allow public-key authentication after a failure with "none"
  authentication.  (#21268)

* Tue Nov 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to x11-askpass 1.1.1. (#21301)
- Don't second-guess fixpaths, which causes paths to get fixed twice. (#21290)

* Mon Nov 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Merge multiple PAM text messages into subsequent prompts when possible when
  doing keyboard-interactive authentication.

* Sun Nov 26 2000 Nalin Dahyabhai <nalin@redhat.com>
- Disable the built-in MD5 password support.  We're using PAM.
- Take a crack at doing keyboard-interactive authentication with PAM, and
  enable use of it in the default client configuration so that the client
  will try it when the server disallows password authentication.
- Build with debugging flags.  Build root policies strip all binaries anyway.

* Tue Nov 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- Use DESTDIR instead of %%makeinstall.
- Remove /usr/X11R6/bin from the path-fixing patch.

* Mon Nov 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add the primes file from the latest snapshot to the main package (#20884).
- Add the dev package to the prereq list (#19984).
- Remove the default path and mimic login's behavior in the server itself.

* Fri Nov 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Resync with conditional options in Damien Miller's .spec file for an errata.
- Change libexecdir from %%{_libexecdir}/ssh to %%{_libexecdir}/openssh.

* Tue Nov  7 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to OpenSSH 2.3.0p1.
- Update to x11-askpass 1.1.0.
- Enable keyboard-interactive authentication.

* Mon Oct 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to ssh-askpass-x11 1.0.3.
- Change authentication related messages to be private (#19966).

* Tue Oct 10 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch ssh-keygen to be able to list signatures for DSA public key files
  it generates.

* Thu Oct  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add BuildPreReq on /usr/include/security/pam_appl.h to be sure we always
  build PAM authentication in.
- Try setting SSH_ASKPASS if gnome-ssh-askpass is installed.
- Clean out no-longer-used patches.
- Patch ssh-add to try to add both identity and id_dsa, and to error only
  when neither exists.

* Mon Oct  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update x11-askpass to 1.0.2. (#17835)
- Add BuildPreReqs for /bin/login and /usr/bin/rsh so that configure will
  always find them in the right place. (#17909)
- Set the default path to be the same as the one supplied by /bin/login, but
  add /usr/X11R6/bin. (#17909)
- Try to handle obsoletion of ssh-server more cleanly.  Package names
  are different, but init script name isn't. (#17865)

* Wed Sep  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.0p1. (#17835)
- Tweak the init script to allow proper restarting. (#18023)

* Wed Aug 23 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 20000823 snapshot.
- Change subpackage requirements from %%{version} to %%{version}-%%{release}
- Back out the pipe patch.

* Mon Jul 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p4, which includes fixes for config file parsing problems.
- Move the init script back.
- Add Damien's quick fix for wackiness.

* Wed Jul 12 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p3, which includes fixes for X11 forwarding and strtok().

* Thu Jul  6 2000 Nalin Dahyabhai <nalin@redhat.com>
- Move condrestart to server postun.
- Move key generation to init script.
- Actually use the right patch for moving the key generation to the init script.
- Clean up the init script a bit.

* Wed Jul  5 2000 Nalin Dahyabhai <nalin@redhat.com>
- Fix X11 forwarding, from mail post by Chan Shih-Ping Richard.

* Sun Jul  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.1.1p2.
- Use of strtok() considered harmful.

* Sat Jul  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- Get the build root out of the man pages.

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- Add and use condrestart support in the init script.
- Add newer initscripts as a prereq.

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- Build in new environment (release 2)
- Move -clients subpackage to Applications/Internet group

* Fri Jun  9 2000 Nalin Dahyabhai <nalin@redhat.com>
- Update to 2.2.1p1

* Sat Jun  3 2000 Nalin Dahyabhai <nalin@redhat.com>
- Patch to build with neither RSA nor RSAref.
- Miscellaneous FHS-compliance tweaks.
- Fix for possibly-compressed man pages.

* Wed Mar 15 2000 Damien Miller <djm@ibs.com.au>
- Updated for new location
- Updated for new gnome-ssh-askpass build

* Sun Dec 26 1999 Damien Miller <djm@mindrot.org>
- Added Jim Knoble's <jmknoble@pobox.com> askpass

* Mon Nov 15 1999 Damien Miller <djm@mindrot.org>
- Split subpackages further based on patch from jim knoble <jmknoble@pobox.com>

* Sat Nov 13 1999 Damien Miller <djm@mindrot.org>
- Added 'Obsoletes' directives

* Tue Nov 09 1999 Damien Miller <djm@ibs.com.au>
- Use make install
- Subpackages

* Mon Nov 08 1999 Damien Miller <djm@ibs.com.au>
- Added links for slogin
- Fixed perms on manpages

* Sat Oct 30 1999 Damien Miller <djm@ibs.com.au>
- Renamed init script

* Fri Oct 29 1999 Damien Miller <djm@ibs.com.au>
- Back to old binary names

* Thu Oct 28 1999 Damien Miller <djm@ibs.com.au>
- Use autoconf
- New binary names

* Wed Oct 27 1999 Damien Miller <djm@ibs.com.au>
- Initial RPMification, based on Jan "Yenya" Kasprzak's <kas@fi.muni.cz> spec.
