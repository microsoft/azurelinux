Vendor:         Microsoft Corporation
Distribution:   Mariner
%global systemd 1
%global	sysvinit 0

%global systemdsysv 0

%global tmpfiles 1

%global sysvinitdir %{_initddir}

%bcond_with xmlrpc

Name:		certmonger
Version:	0.79.13
Release:	2%{?dist}
Summary:	Certificate status monitor and PKI enrollment client

License:	GPLv3+
URL:		http://pagure.io/certmonger/
Source0:	http://releases.pagure.org/certmonger/certmonger-%{version}.tar.gz
#Source1:	http://releases.pagure.org/certmonger/certmonger-%%{version}.tar.gz.sig

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gcc
BuildRequires:	openldap-devel
BuildRequires:	krb5-devel
BuildRequires:	libidn2-devel
BuildRequires:	dbus-devel, nspr-devel, nss-devel, openssl-devel
BuildRequires:	libuuid-devel
BuildRequires:	libtalloc-devel, libtevent-devel
BuildRequires:	libcurl-devel
BuildRequires:	libxml2-devel
%if %{with xmlrpc}
BuildRequires:	xmlrpc-c-devel
%endif
BuildRequires:	jansson-devel
%if 0%{?rhel} && 0%{?rhel} < 6
BuildRequires:	bind-libbind-devel
BuildRequires:	mktemp
%endif
# Required for 'make check':
#  for diff and cmp
BuildRequires:	diffutils
#  for expect
BuildRequires:	expect
#  for certutil and pk12util
BuildRequires:	nss-tools
#  for openssl
BuildRequires:	openssl
#  for dbus-launch
BuildRequires:	/usr/bin/dbus-launch
#  for dos2unix
BuildRequires:	/usr/bin/dos2unix
BuildRequires:	/usr/bin/unix2dos
#  for which
BuildRequires:	/usr/bin/which
#  for dbus tests
BuildRequires:	python3-dbus
BuildRequires:	popt-devel

# we need a running system bus
Requires:	dbus
Requires(post):	%{_bindir}/dbus-send

%if %{systemd}
BuildRequires:	systemd-units
BuildRequires:  systemd-devel
Requires(post):	systemd-units
Requires(preun):	systemd-units, dbus, sed
Requires(postun):	systemd-units
%endif

%if %{systemdsysv}
Requires(post):	systemd-sysv
%global systemdsysvsave \
# Save the current service runlevel info, in case the user wants \
# to apply the enabled status manually later, by running \
#   "systemd-sysv-convert --apply certmonger". \
%{_bindir}/systemd-sysv-convert --save certmonger >/dev/null 2>&1 ||:
%else
%global systemdsysvsave %{nil}
%endif

%if %{sysvinit}
Requires(post):	/sbin/chkconfig, /sbin/service
Requires(preun):	/sbin/chkconfig, /sbin/service, dbus, sed
%endif

# Certain versions of libtevent have incorrect internal ABI versions.
Conflicts: libtevent < 0.9.13

%description
Certmonger is a service which is primarily concerned with getting your
system enrolled with a certificate authority (CA) and keeping it enrolled.

%prep
%autosetup -p1

%if 0%{?rhel} > 0
# Enabled by default for RHEL for bug #765600, still disabled by default for
# Fedora pending a similar bug report there.
sed -i 's,^# chkconfig: - ,# chkconfig: 345 ,g' sysvinit/certmonger.in
%endif

%build
autoreconf -i -f
%configure \
%if %{systemd}
	--enable-systemd \
%endif
%if %{sysvinit}
	--enable-sysvinit=%{sysvinitdir} \
%endif
%if %{tmpfiles}
	--enable-tmpfiles \
%endif
	--with-homedir=/run/certmonger \
%if %{with xmlrpc}
	--with-xmlrpc \
%endif
	--with-tmpdir=/run/certmonger --enable-pie --enable-now
%if %{with xmlrpc}
# For some reason, some versions of xmlrpc-c-config in Fedora and RHEL just
# tell us about libxmlrpc_client, but we need more.  Work around.
make %{?_smp_mflags} XMLRPC_LIBS="-lxmlrpc_client -lxmlrpc_util -lxmlrpc"
%else
make %{?_smp_mflags}
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/lib/certmonger/{cas,requests}
install -m755 -d $RPM_BUILD_ROOT/run/certmonger
%{find_lang} %{name}

%check
make check

%post
if test $1 -eq 1 ; then
	%{_bindir}/dbus-send --system --type=method_call --dest=org.freedesktop.DBus / org.freedesktop.DBus.ReloadConfig 2>&1 || :
fi
%if %{without xmlrpc}
# remove any existing certmaster CA configuration
if test $1 -gt 1 ; then
	%{_bindir}/getcert remove-ca -c certmaster 2>&1 || :
fi
%endif
%if %{systemd}
if test $1 -eq 1 ; then
	/bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi
%endif
%if %{sysvinit}
/sbin/chkconfig --add certmonger
%endif

%triggerin -- certmonger < 0.58
if test $1 -gt 1 ; then
	# If the daemon is running, remove knowledge of the dogtag renewer.
	objpath=`dbus-send --system --reply-timeout=10000 --dest=org.fedorahosted.certmonger --print-reply=o /org/fedorahosted/certmonger org.fedorahosted.certmonger.find_ca_by_nickname string:dogtag-ipa-renew-agent 2> /dev/null | sed -r 's,^ +,,g' || true`
	if test -n "$objpath" ; then
		dbus-send --system --dest=org.fedorahosted.certmonger --print-reply /org/fedorahosted/certmonger org.fedorahosted.certmonger.remove_known_ca objpath:"$objpath" >/dev/null 2> /dev/null
	fi
	# Remove the data file, in case it isn't running.
	for cafile in %{_localstatedir}/lib/certmonger/cas/* ; do
		if grep -q '^id=dogtag-ipa-renew-agent$' "$cafile" ; then
			rm -f "$cafile"
		fi
	done
fi
exit 0

%postun
%if %{systemd}
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
	/bin/systemctl try-restart certmonger.service >/dev/null 2>&1 || :
fi
%endif
%if %{sysvinit}
if test $1 -gt 0 ; then
	/sbin/service certmonger condrestart 2>&1 > /dev/null
fi
%endif
exit 0

%preun
%if %{systemd}
if test $1 -eq 0 ; then
	/bin/systemctl --no-reload disable certmonger.service > /dev/null 2>&1 || :
	/bin/systemctl stop certmonger.service > /dev/null 2>&1 || :
fi
%endif
%if %{sysvinit}
if test $1 -eq 0 ; then
	/sbin/service certmonger stop 2>&1 > /dev/null
	/sbin/chkconfig --del certmonger
fi
%endif
exit 0

%if %{systemd}
%triggerun -- certmonger < 0.43
%{systemdsysvsave}
# Do this because the old package's %%postun doesn't know we need to do it.
/sbin/chkconfig --del certmonger >/dev/null 2>&1 || :
# Do this because the old package's %%postun wouldn't have tried.
/bin/systemctl try-restart certmonger.service >/dev/null 2>&1 || :
exit 0
%endif

%files -f %{name}.lang
%doc README.md LICENSE STATUS doc/*.txt
%config(noreplace) %{_sysconfdir}/dbus-1/system.d/*
%{_datadir}/dbus-1/services/*
%dir %{_sysconfdir}/certmonger
%config(noreplace) %{_sysconfdir}/certmonger/certmonger.conf
%dir /run/certmonger
%{_bindir}/*
%{_sbindir}/certmonger
%{_mandir}/man*/*
%{_libexecdir}/%{name}
%{_localstatedir}/lib/certmonger
%if %{sysvinit}
%{sysvinitdir}/certmonger
%endif
%if %{tmpfiles}
%attr(0644,root,root) %config(noreplace) %{_tmpfilesdir}/certmonger.conf
%endif
%if %{systemd}
%{_unitdir}/*
%{_datadir}/dbus-1/system-services/*
%endif

%changelog
* Tue Jun 22 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.79.13-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add build-time requirement on systemd-devel for systemd pkgconfig files

* Tue Oct 20 2020 Rob Crittenden <rcritten@redhat.com> - 0.79.13-1
- Update to upstream 0.79.13

* Mon Oct  5 2020 Rob Crittenden <rcritten@redhat.com> - 0.79.12-1
- Update to upstream 0.79.12

* Tue Jun 30 2020 Rob Crittenden <rcritten@redhat.com> - 0.79.11-2
- Fix for an unnecessary free() which can cause core dump.

* Tue Jun 30 2020 Rob Crittenden <rcritten@redhat.com> - 0.79.11-1
- Update to upstream 0.79.11

* Thu Jun 25 2020 Rob Crittenden <rcritten@redhat.com> - 0.79.10-1
- Update to upstream 0.79.10

* Thu Jan 30 2020 Rob Crittenden <rcritten@redhat.com> - 0.79.9-1
- Update to upstream 0.79.9

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.79.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Oct 30 2019 Rob Crittenden <rcritten@redhat.com> - 0.79.8-3
- Change python2-dbus build dependency to python3
- Convert tests to pass under python 3
- Skip DSA tests because it is disabled by default crypto policy

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.79.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Rob Crittenden <rcritten@redhat.com> - 0.79.8-1
- Update to upstream 0.79.8

* Wed May 22 2019 Rob Crittenden <rcritten@redhat.com> - 0.79.7-3
- Add BuildRequires for krb5-devel, the buildroot changed.

* Mon May 20 2019 Rob Crittenden <rcritten@redhat.com> - 0.79.7-2
- Move systemd tmpfiles from /var/run to /run (upstream #111)
- Change /var/run -> /run in systemd service file

* Mon Feb 18 2019 Rob Crittenden <rcritten@redhat.com> - 0.79.7-1
- Update to upstream 0.79.7

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.79.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct  4 2018 Rob Crittenden <rcritten@redhat.com> - 0.79.6-4
- Pull in upstream fixes discovered in coverity and clang.

* Mon Oct  1 2018 Rob Crittenden <rcritten@redhat.com> - 0.79.6-3
- Improve NSS token handling. The updated NSS crypto-policy enables all
  tokens which broke requesting certificates due to the way that tokens
  were managed.

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.79.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May  8 2018 Rob Crittenden <rcritten@redhat.com> - 0.79.6-1
- Update to upstream 0.79.6

* Wed Mar 14 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.79.5-7
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 23 2018 Rob Crittenden <rcritten@redhat.com> 0.79.5-6
- Fix unit tests. NSS crypto policy disallows keys < 1024

* Wed Feb 21 2018 Rob Crittenden <rcritten@redhat.com> 0.79.5-5
- Add BuildRequires on gcc

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.79.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 10 2018 Rob Crittenden <rcritten@redhat.com> 0.79.5-3
- Remove BR on mktemp. It is now provided by coreutils.
- Patch to fix NSS handling of keys in sqlite databases
- Patches to fix tests now that sqlite is the NSS default.

* Wed Oct  4 2017 Rob Crittenden <rcritten@redhat.com> 0.79.5-2
- Switch BR from /usr/include/popt.h to popt-devel

* Fri Sep  1 2017 Rob Crittenden <rcritten@redhat.com> 0.79.5-1
- update to 0.79.5:
   - getcert start-tracking: use issuer option when specified
   - add support for specifying the MS certificate template
   - Reformat certificates returned by Dogtag to strip extra newline

* Wed Aug 16 2017 Rob Crittenden <rcritten@redhat.com> 0.79.4-2
- Reformat certificates returned by Dogtag. Dogtag was including
  a spurious newline before -----END CERTIFICATE-----

* Mon Aug  7 2017 Rob Crittenden <rcritten@redhat.com> 0.79.4-1
- update to 0.79.4
  - fix CA option name for ipa cert-request
  - fix minor memory leak
  - fix build warnings
  - fix an incorrect date in the .spec changelog
  - bump gettext version to avoid warning

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.79.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.79.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Feb 28 2017 Nalin Dahyabhai <nalin@redhat.com> 0.79.3-1
- update to 0.79.3:
  - fix self-signing self-test cases that used DSA or EC keys

* Mon Feb 27 2017 Nalin Dahyabhai <nalin@redhat.com> 0.79.2-2
- update %%docs list because README is now README.md

* Mon Feb 27 2017 Nalin Dahyabhai <nalin@redhat.com> 0.79.2-1
- update to 0.79.2:
  - fix 'make distcheck' target

* Sun Feb 19 2017 Nalin Dahyabhai <nalin@redhat.com> 0.79.1-1
- update to 0.79.1:
  - update translations
  - fix 'make archive' target

* Sun Feb 19 2017 Nalin Dahyabhai <nalin@redhat.com> 0.79-1
- update to 0.79:
  - getcert now offers an option (-X) for requesting processing by a particular
    CA if the server we're contacting is running more than one
  - getcert also offers options (--for-ca, --not-for-ca, --ca-path-length) for
    requesting BasicConstraints values
  - getcert now displays times in local time instead of UTC, which was
    previously the only way they were displayed; the --utc option can often be
    used to switch back to its previous behavior
  - the SCEP enrollment helper now correctly issues GetCACertChain requests to
    SCEP servers, instead of issuing a GetCAChain request, which isn't part of
    the protocol; from report by Jason Garland
  - when issuing SCEP requests, the ID of the CA included in the HTTP request
    is now URL-encoded, as it should be
  - renewal or notification-of-impending-expiration logic is now triggered
    closer to TTL thresholds rather than waiting for a periodic check to pass a
    threshold
  - properly builds with OpenSSL 1.1, thanks to Lukas Slebodnik and Tomas Mraz
    for a lot of the legwork
- resync .spec file with Fedora
- upstream project migrated from fedorahosted.org to pagure.io

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.78.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat Jan 21 2017 Igor Gnatenko <ignatenko@redhat.com> - 0.78.6-5
- Rebuild for xmlrpc-c

* Wed Jul  6 2016 Nalin Dahyabhai <nalin@redhat.com> 0.78.6-4
- add backported fix to wait a reasonable amount of time after calling the
  'resubmit' method for a new certificate to be issued when we're exercising
  the D-Bus API during tests (Jan Cholasta, #1351052)

* Wed Jul  6 2016 Nalin Dahyabhai <nalin@redhat.com> 0.78.6-3
- instead of using killall to send a SIGHUP to the system bus daemon in %%post
  to get it to reload its configuration, use dbus-send to send a ReloadConfig
  request over the bus (should fix #1277573)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.78.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 13 2016 Nalin Dahyabhai <nalin@redhat.com> 0.78.6-1
- document the -R, -N, -o, and -t flags for dogtag-ipa-renew-agent-submit
- stop checking that we can generate 512 bit keys during self-tests

* Thu Nov 12 2015 Nalin Dahyabhai <nalin@redhat.com> 0.78.5-1
- fix a possible uninitialized memory read (possibly #1260871)
- log a diagnostic error when we fail to initialize libkrb5

* Tue Aug  4 2015 Nalin Dahyabhai <nalin@redhat.com> 0.78.4-1
- fix the "getcert start-tracking" -L and -l options (#1249753)
- output diagnostics about the second request when scep-submit encounters an
  error during a second request to the SCEP server

* Mon Jul 20 2015 Nalin Dahyabhai <nalin@redhat.com> 0.78.3-1
- call poptGetOptArg() correctly, to fix parsing of the -R flag to scep-submit
  and the -O and -o flags to dogtag-submit (#1244914)

* Thu Jul  9 2015 Nalin Dahyabhai <nalin@redhat.com> 0.78.2-1
- tweak initialization so that we set up for providing our D-Bus API before we
  register our name with the bus, so that we can handle any requests that
  arrive before the acknowledgement of that registration
- on systems that run systemd, add the right data file so that the service gets
  started when someone tries to talk to the daemon (ticket #38)
- correctly check for error responses when sending GetCAChain requests to SCEP
  servers

* Sun Jun 21 2015 Nalin Dahyabhai <nalin@redhat.com> 0.78.1-1
- self-tests: assume that certutil won't generate DSA keys with more than 1024
  bits, and will often short us by a few

* Sat Jun 20 2015 Nalin Dahyabhai <nalin@redhat.com> 0.78-1
- switch to using popt for parsing command line arguments, continuing to
  use old help text for now so that we can catch up with translations (print
  old text for --help, new text (with longopts!) for -H)
- add some plumbing for eventually receiving per-certificate roots in
  addition to issued certificates and chain certificates
- add a "rekey" command to getcert, for triggering enrollment using a new
  key pair (#1087932)
- scep-submit: check for the Renewal capability, and default to taking
  advantage of it during rekeying, unless the new -n flag is specified to it
- dogtag-submit: add flags for passing user names, UDNs, passwords, and PINs
  to the helper (part of ticket #12)
- dogtag-submit: add a flag for using the agent creds to do TLS client auth
  while submitting enrollment requests (more of ticket #12)
- dogtag-submit: handle cases where we submit a request and the server
  returns a success code rather than just queuing the request (#12 again)
- ipa-submit: pass requested profile names to the server as an argument
  named "profile_id"; if the server gives us an "unrecognized argument"
  error, retry without it for compatibility's sake (part of IPA ticket #57)
- keygen: fix a possible crash if keygen fails to return a key from NSS
- correct the certmonger(8) man page's description of the -c flag, which it
  used to call the -C flag
- add logic for setting ownership and permissions on certificates and keys
  when saving them to disk
- add configuration options "max_key_lifetime" and "max_key_use_count" for
  making automatic renewal prefer rekeying

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.77.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 28 2015 Nalin Dahyabhai <nalin@redhat.com> 0.77.5-1
- pass $CERTMONGER_REQ_IP_ADDRESS to enrollment helpers if the signing request
  includes IP address subjectAltName values
- correctly verify signatures on SCEP server replies when the signer is neither
  the top-level CA nor the RA (feedback in #1161768)
- correctly verify signatures on SCEP server replies when there is more than
  one certificate in the chain between the RA and the top-level CA (feedback in
  #1161768)

* Fri May 15 2015 Nalin Dahyabhai <nalin@redhat.com> 0.77.4-1
- don't display PINs in "getcert list" output (#42)
- clean up launching of a private instance in "getcert"
- expand on the don't-delete-private-key fix from 0.77.3 by letting NSS's
  own safety checks have an effect
- backport record-keeping of key generation dates and counts of how many
  times we've gotten certificates using a given key pair

* Thu May  7 2015 Nalin Dahyabhai <nalin@redhat.com> 0.77.3-1
- fix a data loss bug when saving renewed certificates to NSS databases - the
  private key could be removed in error since 0.77
- fixes for bugs found by static analysis
- fix self-tests when built with OpenSSL 1.0.2

* Tue Apr 14 2015 Nalin Dahyabhai <nalin@redhat.com> 0.77.2-1
- expose the certificate's not-valid-before and not-valid-after dates as a
  property over D-Bus (ticket #41)
- give the local signer its own configuration option to set the lifetime
  of its signing certificate, falling back to the lifetime configured for
  the self-signer as a default to match the previous behavior
- fix a potential read segfault parsing the output of an enrollment helper,
  introduced in 0.77 (thanks to Steve Neuharth)
- read the ns-certtype extension value in certificates
- request an enrollment certtype extension to CSRs if we have a profile name
  that we want to use (ticket #17, possibly part of IPA ticket #57)

* Fri Feb 27 2015 Nalin Dahyabhai <nalin@redhat.com> 0.77.1-1
- update to 0.77
  - add initial, still rough, SCEP support (#1140241,#1161768)
    - add an scep-submit helper to handle part of it
  - getcert: add add-ca/add-scep-ca/modify-ca/remove-ca commands
  - getcert: add -l, -L flags to request/resubmit/start-tracking commands
    to provide a way to set a ChallengePassword in signing requests
  - lay some groundwork for rekeying support
  - bundled dogtag enrollment helpers now output debugging info to stderr (#)
  - ipa-getcert: fix a crash when using DNS discovery to locate servers (#39)
  - getcert: fix displaying of pre-request pre-/post-save commands (#1178190,
    #1181022, patch by David Kupka)
  - use Zanata for translations
  - getcert list: list the certificate's profile name, if it contains one

* Tue Nov 18 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.8-1
- dogtag-submit: accept additional options to pass to the server when
  approving requests using agent creds (#1165155, patch by Jan Cholasta)
- getcert: print help output when 'status' isn't given any args (#1163541)

* Tue Nov 11 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.7-1
- correctly read CA not-valid-after dates on 32-bit machines (also reported by
  Natxo Asenjo), so that we don't spin on polling them (#1163023)

* Mon Nov 10 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.6-1
- don't discard the priority value in DNS SRV records

* Mon Nov 10 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.5-1
- avoid premature exit on CA data analysis failures (should fix an issue
  reported by Natxo Asenjo)

* Mon Nov 10 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.4-1
- fix a failure in self-tests

* Mon Nov 10 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.3-1
- fixes for bugs found by static analysis
- handle IDN correctly when doing service location using SRV records
- documentation updates

* Wed Nov  5 2014 Nalin Dahyabhai <nalin@redhat.com>
- rework the state machine so that we save an issued certificate's associated
  CA certificates, then re-read the certificate, then run the post hook and
  issue notifications, in that order, instead of saving CA certificates after
  running the post hook, which was always a surprising order (#1131700)
- add a generic dogtag-submit helper that doesn't include any IPA defaults,
  to make it easier to know the difference between paramenters it requires
  and parameters which are optional (#12)

* Tue Nov  4 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.2-1
- ipa-submit: when we fail to locate/contact LDAP or XML-RPC servers,
  use discovery to find them (#1136900)

* Fri Oct 31 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76.1-1
- allow for 'certmonger -P abstract:...' to work, too

* Fri Oct 31 2014 Nalin Dahyabhai <nalin@redhat.com> 0.76-1
- require a single certificate to be specified to 'getcert status' (#1148001,
  #1163541, #1163539)
- shorten the default help message which getcert prints when it's not given
  a specific command (#1131704)
- add private listener (-l, -L, -P) mode to certmonger, to allow it to listen
  for connections directly from clients running under the same UID
- add a command mode (-c) to certmonger, in which once it's started, it
  launches a specified command, and after that command exits, the daemon exits
- when getcert is invoked with no bus running, if it's running as root, run
  certmonger in private listener mode with the same invocation of getcert as
  the command to start and wait for (#1134497)

* Thu Aug 28 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.14-1
- make pathname canonicalization slightly smarter, to handle ".." in
  locations (#1131758)
- updates to self-tests (#1144082)

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 0.75.13-2
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.13-1
- add a missing test case file (whoops)

* Mon Aug 18 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.12-1
- correct encoding/decoding of variant-typed data which we receive and send
  as part of the org.freedesktop.DBus.Properties interface over the bus, and
  add some tests for them (based on patch from David Kupka, ticket #36)

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.75.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Aug 12 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.11-1
- when getcert is passed a -a flag, to indicate that CA root certificates
  should be stored in the specified database, don't ignore locations which
  don't include a storage scheme (#1129537)
- when called to 'start-tracking' with the -a or -F flags, if we have
  applicable certificates on-hand for a CA that we're either told to use
  or which we decide is the correct one, save the certificates (#1129696)

* Tue Aug  5 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.10-1
- when attempting to contact an IPA LDAP server, if no "ldap_uri" is set in
  default.conf, and no "host" is set either, try to construct the server URI
  using the "server" setting (#1126985)

* Thu Jul 31 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.9-1
- avoid potential use-after-free after a CA is removed dynamically (thanks to
  Keenan Brock) (#1125342)
- add a "external-helper" property to CA objects

* Mon Jul 21 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.8-1
- add a 'refresh' option to the getcert command
- add a '-a' flag to the getcert command's 'refresh-ca' option

* Thu Jul 17 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.7-2
- reintroduce package Requires: on systemd-sysv on F19 and EL6 and older,
  conditionalized it so that it's ignored on newer releases, and make
  whether or not we call systemd-sysv-convert in triggers depend on that,
  too (#1104138)

* Thu Jul 17 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.7-1
- fix an inconsistency in how we parse cookie values returned by CA helpers,
  in that single-line values would lose the end-of-line after a daemon
  restart, but not before
- handle timeout values and exit status values when calling CA helpers
  in non-SUBMIT, non-POLL modes (#1118468)
- rework how we save CA certificates so that we save CA certificates associated
  with end-entity certificates when we save that end-entity certificate, which
  requires running all of the involved pre- and post-save commands
- drop package Requires: on systemd-sysv (#1104138)

* Thu Jun 26 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.6-1
- avoid potential use-after-free and read overrun after a CA is added
  dynamically (thanks to Jan Cholasta)

* Fri Jun 20 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.5-1
- documentation updates

* Fri Jun 20 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.4-2
- add a %%trigger to remove knowledge of the "dogtag-ipa-renew-agent" CA
  when we detect certmonger versions prior to 0.58 being installed, to
  avoid cases where some older versions choke on CAs with nicknames that
  contain characters that can't legally be part of a D-Bus name (#948993)

* Thu Jun 19 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.4-1
- fix creation and packaging of the "local" CA's data directory

* Wed Jun 18 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.3-1
- read and cache whether or not we saw a noOCSPcheck extension in certificates
- documentation updates

* Mon Jun 16 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.2-1
- when generating keys using OpenSSL, if key generation fails, try
  again with the default key size, in case we're in FIPS mode
- documentation updates

* Sat Jun 14 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75.1-1
- log the state in 'getcert status' verbose mode

* Fri Jun 13 2014 Nalin Dahyabhai <nalin@redhat.com> 0.75-1
- add a -w (wait) flag to the getcert's request/resubmit/start-tracking
  commands, and add a non-waiting status command

* Wed Jun 11 2014 Nalin Dahyabhai <nalin@redhat.com> 0.74.96-1
- make the trust settings we apply to CA-supplied certificates while
  saving them to NSS databases run-time configurable
- fix compiling against EL5-era OpenSSL
- when saving CA certificates we pull from an IPA server, nickname
  it using the realm name with " IPA CA" appended rather than just
  naming it "IPA CA"
- fix the local signer so that when it issues itself a new certificate,
  it uses the same subject name
- add a -w flag to getcert's request, resubmit, and start-tracking
  commands, telling it to wait until either the certificate is issued,
  we get to a state where we know that we won't be able to get one, or
  we are waiting for a CA

* Mon Jun  9 2014 Nalin Dahyabhai <nalin@redhat.com> 0.74.95-1
- add the "local" signer, a local toy CA that signs anything you'll
  ask it to sign

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.74-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Jun  6 2014 Nalin Dahyabhai <nalin@redhat.com> 0.74.94-1
- fix self-test errors that we trigger with new OpenSSL
- fix a build error that would sometimes happen when we're told to
  build PIE binaries
- quiet a compile warning

* Thu Jun  5 2014 Nalin Dahyabhai <nalin@redhat.com> 0.74.93-1
- add some self-tests
- simplify the internal submit-to-CA logic
- fixes for more problems found through static analysis

* Tue Jun  3 2014 Nalin Dahyabhai <nalin@redhat.com> 0.74.92-1
- retrieve CA information from CAs, if the helpers can do so, and
  add a command to explicitly refresh that data: "getcert refresh-ca"
- offer to save CA certificates to files and databases, when specified with
  new -a and -F flags to getcert request/resubmit/start-tracking (#1098208,
  trac #31)
- add IP address subject alternate names when getcert request/resubmit
  is passed the -A option (trac #35)
- read and cache the freshestCRL extension in certificates
- properly interpret KDC-unreachable errors encountered in the IPA
  submission error as a server-unreachable error that we will retry,
  rather than a misconfiguration error which we won't
- don't let tests get tripped up by new formatting used in dos2unix status
  messages (#1099080)
- updated translations
- be explicit that we are going to use bashisms in test scripts by calling
  the shell interpreter as 'bash' rather than 'sh' (trac #27)

* Thu Apr  3 2014 Nalin Dahyabhai <nalin@redhat.com> 0.74-1
- also save state when we exit due to SIGHUP
- don't get tripped up when enrollment helpers hand us certificates which
  include CRLF line terminators (ticket #25)
- be tolerant of certificate issuer names, subject names, DNS, email, and
  Kerberos principal namem subjectAltNames, and crl distribution point URLs
  that contain newlines
- read and cache the certificate template extension in certificates
- enforce different minimum key sizes depending on the type of key we're
  trying to generate
- store DER versions of subject, issuer and template subject, if we have
  them (Jan Cholasta, ticket #26)
- when generating signing requests with subject names that don't quite parse
  as subject names, encode what we're given as PrintableString rather than
  as a UTF8String
- always chdir() to a known location at startup, even if we're not becoming
  a daemon
- fix a couple of memory leaks (static analysis)
- add missing buildrequires: on which

* Thu Feb 20 2014 Nalin Dahyabhai <nalin@redhat.com> 0.73-1
- updates to 0.73
  - getcert no longer claims to be stuck when a CA is unreachable,
    because the daemon isn't actually stuck

* Mon Feb 17 2014 Nalin Dahyabhai <nalin@redhat.com>
- updates to 0.73
  - also pass the key type to enrollment helpers in the environment as
    a the value of "CERTMONGER_KEY_TYPE"

* Mon Feb 10 2014 Nalin Dahyabhai <nalin@redhat.com>
- move the tmpfiles.d file from /etc/tmpfiles.d to %%{_tmpfilesdir},
  where it belongs (#1180978)

* Mon Feb 10 2014 Nalin Dahyabhai <nalin@redhat.com>
- updates for 0.73
  - set the flag to encode EC public key parameters using named curves
    instead of the default of all-the-details when using OpenSSL
  - don't break when NSS supports secp521r1 but OpenSSL doesn't
  - also pass the CA nickname to enrollment helpers in the environment as
    a text value in "CERTMONGER_CA_NICKNAME", so they can use that value
    when reading configuration settings
  - also pass the SPKAC value to enrollment helpers in the environment as
    a base64 value in "CERTMONGER_SPKAC"
  - also pass the request's SubjectPublicKeyInfo value to enrollment helpers
    in the environment as a base64 value in "CERTMONGER_SPKI" (part of #16)
  - when generating signing requests using NSS, be more accommodating of
    requested subject names that don't parse properly

* Mon Feb  3 2014 Nalin Dahyabhai <nalin@redhat.com> 0.72-1
- update to 0.72
  - support generating DSA parameters and keys on sufficiently-new OpenSSL
    and NSS
  - support generating EC keys when OpenSSL and NSS support it, using key
    size to select the curve to use from among secp256r1, secp384r1,
    secp521r1 (which are the ones that are usually available, though
    secp521r1 isn't always, even if the other two are)
  - stop trying to cache public key parameters at all and instead cache public
    key info properly
  - encode the friendlyName attribute in signing requests as a BMPString,
    not as a PrintableString
  - catch more filesystem permissions problems earlier (more of #996581)

* Mon Jan 27 2014 Nalin Dahyabhai <nalin@redhat.com> 0.71-1
- check for cases where we fail to allocate memory while reading a request
  or CA entry from disk (John Haxby)
- only handle one watch at a time, which should avoid abort() during
  attempts to reconnect to the message bus after losing our connection
  to it (#1055521)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.70-2
- Mass rebuild 2014-01-24

* Thu Jan  2 2014 Nalin Dahyabhai <nalin@redhat.com> 0.70-1
- add a --with-homedir option to configure, and use it, since subprocesses
  which we run and which use NSS may attempt to write to $HOME/.pki, and
  0.69's strategy of setting that to "/" was rightly hitting SELinux policy
  denials (#1047798)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.69-2
- Mass rebuild 2013-12-27

* Mon Dec  9 2013 Nalin Dahyabhai <nalin@redhat.com> 0.69-1
- tweak how we decide whether we're on the master or a minion when we're
  told to use certmaster as a CA
- clean up one of the tests so that it doesn't have to work around internal
  logging producing duplicate messages
- when logging errors while setting up to contact xmlrpc servers, explicitly
  note that the error is client-side
- don't abort() due to incorrect locking when an attempt to save an issued
  certificate to the designated location fails (part of #1032760/#1033333,
  ticket #22)
- when reading an issued certificate from an enrollment helper, ignore
  noise before or after the certificate itself (more of #1032760/1033333,
  ticket #22)
- run subprocesses in a cleaned-up environment (more of #1032760/1033333,
  ticket #22)
- clear the ca-error that we saved when we had an error talking to the CA if we
  subsequently succeed in talking to the CA
- various other static-analysis fixes

* Thu Aug 29 2013 Nalin Dahyabhai <nalin@redhat.com> 0.68-1
- notice when the OpenSSL RNG isn't seeded
- notice when saving certificates or keys fails due to filesystem-related
  permission denial (#996581)

* Tue Aug  6 2013 Nalin Dahyabhai <nalin@redhat.com> 0.67-3
- pull up a patch from master to adapt self-tests to certutil's diagnostic
  output having changed (#992050)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.67-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Mar 11 2013 Nalin Dahyabhai <nalin@redhat.com> 0.67-1
- when saving certificates to NSS databases, try to preserve the trust
  value assigned to a previously-present certificate with the same nickname
  and subject, if one is found
- when saving certificates to NSS databases, also prune certificates from
  the database which have both the same nickname and subject as the one
  we're adding, to avoid tripping up tools that only fetch one certificate
  by nickname

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.65-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jan 23 2013 Nalin Dahyabhai <nalin@redhat.com> 0.66-1
- build as position-independent executables with early binding (#883966)
- also don't tag the unit file as a configuration file (internal tooling)

* Wed Jan 23 2013 Nalin Dahyabhai <nalin@redhat.com> 0.65-2
- don't tag the D-Bus session .service file as a configuration file (internal
  tooling)

* Tue Jan  8 2013 Nalin Dahyabhai <nalin@redhat.com> 0.65-1
- fix a crash in the self-tests

* Tue Jan  8 2013 Nalin Dahyabhai <nalin@redhat.com> 0.64-1
- at startup, if we resume the state machine for a given certificate to a state
  which expects to have the newly-added lock already acquired, acquire it
  before moving on with the certificate's work (still aimed at fixing #883484)

* Tue Dec 18 2012 Nalin Dahyabhai <nalin@redhat.com> 0.63-1
- serialize access to NSS databases and the running of pre- and post-save
  commands which might also access them (possibly fixing part of #883484)

* Thu Nov 29 2012 Nalin Dahyabhai <nalin@redhat.com> 0.62-1
- add a -u flag to getcert to enable requesting a keyUsage extension value
- request subjectKeyIdentifier extensions from CAs, and include them in
  self-signed certificates
- request basicConstraints from CAs, defaulting to requests for end-entity
  certificates
- when requesting CA certificates, also request authorityKeyIdentifier
- add support for requesting CRL distribution point and authorityInfoAccess
  extensions that specify OCSP responder locations
- don't crash when OpenSSL can't build a template certificate from a request
  when we're in FIPS mode
- put NSS in FIPS mode, when the system booted that way, except when we're
  trying to write certificates to a database
- fix CSR generation and self-signing in FIPS mode with NSS
- fix self-signing in FIPS mode with OpenSSL
- new languages from the translation team: mai, ml, nn, ga

* Tue Nov 27 2012 Nalin Dahyabhai <nalin@redhat.com> 0.61-3
- backport change from git to not choke if X509_REQ_to_X509() fails when we're
  self-signing using OpenSSL
- backport another change from git to represent this as a CA-rejected error

* Mon Sep 24 2012 Nalin Dahyabhai <nalin@redhat.com> 0.61-1
- fix a regression in reading old request tracking files where the
  request was in state NEED_TO_NOTIFY or NOTIFYING

* Wed Sep  5 2012 Nalin Dahyabhai <nalin@redhat.com> 0.60-1
- adjust internals of logic for talking to dogtag to at least have a
  concept of non-agent cases
- when talking to an IPA server's internal Dogtag instance, infer which
  ports the CA is listening on from the "dogtag_version" setting in the
  IPA configuration (Ade Lee)
- send a notification (or log a message, whatever) when we save a new
  certificate (#766167)

* Mon Jul 30 2012 Nalin Dahyabhai <nalin@redhat.com>
- fix a bad %%preun scriptlet

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.59-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Nalin Dahyabhai <nalin@redhat.com> 0.59-1
- mostly documentation updates

* Fri Jun 29 2012 Nalin Dahyabhai <nalin@redhat.com> 0.58-1
- add a "dogtag-ipa-renew-agent" CA so that we can renew certificates using
  an IPA server's internal Dogtag instance
- export the requested profile and old certificate to enrollment helpers
- make libxml and libcurl into hard build-time requirements
- serialize all pre/save/post sequences to make sure that stop/save/start
  doesn't become stop1/save1/stop2/start1/save2/start2 when we're stopping
  a service while we muck with more than one of its certificates

* Fri Jun 15 2012 Nalin Dahyabhai <nalin@redhat.com>
- add a command option (-T) to getcert for specifying which enrollment
  profile to tell a CA that we're using, in case it cares (#10)

* Thu Jun 14 2012 Nalin Dahyabhai <nalin@redhat.com> 0.57-1
- clarify that the command passed to getcert -C is a "post"-save command
- add a "pre"-save command option to getcert, specified with the -B flag (#9)
- after we notify of an impending not-valid-after approaching, don't do it
  again immediately

* Sat Mar  3 2012 Nalin Dahyabhai <nalin@redhat.com> 0.56-1
- when a caller sets the is-default flag on a CA, and another CA is no longer
  the default, emit the PropertiesChanged signal on the CA which is not the
  default, instead on the new default a second time
- drop some dead code from the D-Bus message handlers (static analysis,
  #796813)
- cache public keys when we read private keys
- go back to printing an error indicating that we're missing a required
  argument when we're missing a required argument, not that the option is
  invalid (broken since 0.51, #796542)

* Wed Feb 15 2012 Nalin Dahyabhai <nalin@redhat.com> 0.55-1
- allow root to use our implementation of org.freedesktop.DBus.Properties
- take more care to not emit useless PropertiesChanged signals

* Wed Feb 15 2012 Nalin Dahyabhai <nalin@redhat.com> 0.54-1
- fix setting the group ID when spawning the post-save command

* Tue Feb 14 2012 Nalin Dahyabhai <nalin@redhat.com> 0.53-1
- large changes to the D-Bus glue, exposing a lot of data which we were
  providing via D-Bus getter methods as properties, and providing more
  accurate introspection data
- emit a signal when the daemon saves a certificate to the destination
  location, and provide an option to have the daemon spawn an arbitrary
  command at that point, too (#766167)
- enable starting the service by default on RHEL (#765600)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Dec 16 2011 Nalin Dahyabhai <nalin@redhat.com> 0.52-1
- note that SELinux usually confines us to writing only to cert_t in
  doc/getting-started.txt (#765599)
- fix crashes when we add a request during our first run when we're
  populating the hard-coded CA list
- properly deal with cases where a path is passed to us is "./XXX"
- in session mode, create our data directories as we go

* Tue Dec  6 2011 Nalin Dahyabhai <nalin@redhat.com> 0.51-1
- api: lift restrictions on characters used in request and CA nicknames by
  making their object names not incorporate their nicknames
- api: add find_request_by_nickname and find_ca_by_nickname
- certmonger-ipa-submit.8: list -k, -K, -t in the summary, document -K
- getcert: print "invalid option" error messages ourselves (#756291)
- ipa-submit: supply a Referer: header when submitting requests to IPA
  (#750617, needed for #747710)

* Fri Oct 14 2011 Nalin Dahyabhai <nalin@redhat.com> 0.50-1
- really fix these this time:
 - getcert: error out when "list -c" finds no matching CA (#743488)
 - getcert: error out when "list -i" finds no matching request (#743485)

* Wed Oct 12 2011 Nalin Dahyabhai <nalin@redhat.com> 0.49-1
- when using an NSS database, skip loading the module database (#743042)
- when using an NSS database, skip loading root certs
- generate SPKAC values when generating CSRs, though we don't do anything
  with SPKAC values yet
- internally maintain and use challenge passwords, if we have them
- behave better when certificates have shorter lifetimes
- add/recognize/handle notification type "none"
- getcert: error out when "list -c" finds no matching CA (#743488)
- getcert: error out when "list -i" finds no matching request (#743485)

* Thu Sep 29 2011 Nalin Dahyabhai <nalin@redhat.com> 0.48-1
- don't incorrectly assume that CERT_ImportCerts() returns a NULL-terminated
  array (#742348)

* Tue Sep 27 2011 Nalin Dahyabhai <nalin@redhat.com> 0.47-1
- getcert: distinguish between {stat() succeeds but isn't a directory} and
  {stat() failed} when printing an error message (#739903)
- getcert resubmit/start-tracking: when we're looking for an existing request
  by ID, and we don't find one, note that specifically (#741262)

* Mon Aug 29 2011 Stephen Gallagher <sgallagh@redhat.com> - 0.46-1.1
- Rebuild against fixed libtevent version

* Mon Aug 15 2011 Nalin Dahyabhai <nalin@redhat.com> 0.46-1
- treat the ability to access keys in an NSS database without using a PIN,
  when we've been told we need one, as an error (#692766, really this time)

* Thu Aug 11 2011 Nalin Dahyabhai <nalin@redhat.com> 0.45-1
- modify the systemd .service file to be a proper 'dbus' service (more
  of #718172)

* Thu Aug 11 2011 Nalin Dahyabhai <nalin@redhat.com> 0.44-1
- check specifically for cases where a specified token that we need to
  use just isn't present for whatever reason (#697058)

* Wed Aug 10 2011 Nalin Dahyabhai <nalin@redhat.com> 0.43-1
- add a -K option to ipa-submit, to use the current ccache, which makes
  it easier to test

* Fri Aug  5 2011 Nalin Dahyabhai <nalin@redhat.com>
- if xmlrpc-c's struct xmlrpc_curl_xportparms has a gss_delegate field, set
  it to TRUE when we're doing Negotiate auth (#727864, #727863, #727866)

* Wed Jul 13 2011 Nalin Dahyabhai <nalin@redhat.com>
- treat the ability to access keys in an NSS database without using a PIN,
  when we've been told we need one, as an error (#692766)
- when handling "getcert resubmit" requests, if we don't have a key yet,
  make sure we go all the way back to generating one (#694184)
- getcert: try to clean up tests for NSS and PEM file locations (#699059)
- don't try to set reconnect-on-exit policy unless we managed to connect
  to the bus (#712500)
- handle cases where we specify a token but the storage token isn't
  known (#699552)
- getcert: recognize -i and storage options to narrow down which requests
  the user wants to know about (#698772)
- output hints when the daemon has startup problems, too (#712075)
- add flags to specify whether we're bus-activated or not, so that we can
  exit if we have nothing to do after handling a request received over
  the bus if some specified amount of time has passed
- explicitly disallow non-root access in the D-Bus configuration (#712072)
- migrate to systemd on releases newer than Fedora 15 or RHEL 6 (#718172)
- fix a couple of incorrect calls to talloc_asprintf() (#721392)

* Wed Apr 13 2011 Nalin Dahyabhai <nalin@redhat.com> 0.42-1
- getcert: fix a buffer overrun preparing a request for the daemon when
  there are more parameters to encode than space in the array (#696185)
- updated translations: de, es, id, pl, ru, uk

* Mon Apr 11 2011 Nalin Dahyabhai <nalin@redhat.com> 0.41-1
- read information about the keys we've just generated before proceeding
  to generating a CSR (part of #694184, part of #695675)
- when processing a "resubmit" request from getcert, go back to key
  generation if we don't have keys yet, else go back to CSR generation as
  before (#694184, #695675)
- configure with --with-tmpdir=/var/run/certmonger and own /var/run/certmonger
  (#687899), and add a systemd tmpfiles.d control file for creating
  /var/run/certmonger on Fedora 15 and later
- let session instances exit when they get disconnected from the bus
- use a lock file to make sure there's only one session instance messing
  around with the user's files at a time
- fix errors saving certificates to NSS databases when there's already a
  certificate there with the same nickname (#695672)
- make key and certificate location output from 'getcert list' more properly
  translatable (#7)

* Mon Mar 28 2011 Nalin Dahyabhai <nalin@redhat.com> 0.40-1
- update to 0.40
  - fix validation check on EKU OIDs in getcert (#691351)
  - get session bus mode sorted
  - add a list of recognized EKU values to the getcert-request man page

* Fri Mar 25 2011 Nalin Dahyabhai <nalin@redhat.com> 0.39-1
- update to 0.39
  - fix use of an uninitialized variable in the xmlrpc-based submission
    helpers (#690886)

* Thu Mar 24 2011 Nalin Dahyabhai <nalin@redhat.com> 0.38-1
- update to 0.38
  - catch cases where we can't read a PIN file, but we never have to log
    in to the token to access the private key (more of #688229)

* Tue Mar 22 2011 Nalin Dahyabhai <nalin@redhat.com> 0.37-1
- update to 0.37
  - be more careful about checking if we can read a PIN file successfully
    before we even call an API that might need us to try (#688229)
  - fix strict aliasing warnings

* Tue Mar 22 2011 Nalin Dahyabhai <nalin@redhat.com> 0.36-1
- update to 0.36
  - fix some use-after-free bugs in the daemon (#689776)
  - fix a copy/paste error in certmonger-ipa-submit(8)
  - getcert now suppresses error details when not given its new -v option
    (#683926, more of #681641/#652047)
  - updated translations
    - de, es, pl, ru, uk
    - indonesian translation is now for "id" rather than "in"

* Wed Mar  2 2011 Nalin Dahyabhai <nalin@redhat.com> 0.35.1-1
- fix a self-test that broke because one-year-from-now is now a day's worth
  of seconds further out than it was a few days ago

* Mon Feb 14 2011 Nalin Dahyabhai <nalin@redhat.com> 0.35-1
- update to 0.35
  - self-test fixes to rebuild properly in mock (#670322)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 14 2011 Nalin Dahyabhai <nalin@redhat.com> 0.34-1
- update to 0.34
  - explicitly note the number of requests we're tracking in the output of
    "getcert list" (#652049)
  - try to offer some suggestions when we get certain specific errors back
    in "getcert" (#652047)
  - updated translations
    - es

* Thu Dec 23 2010 Nalin Dahyabhai <nalin@redhat.com> 0.33-1
- update to 0.33
  - new translations
    - id by Okta Purnama Rahadian!
  - updated translations
    - pl, uk
  - roll up assorted fixes for defects

* Fri Nov 12 2010 Nalin Dahyabhai <nalin@redhat.com> 0.32-2
- depend on the e2fsprogs libuuid on Fedora and RHEL releases where it's
  not part of util-linux-ng

* Wed Oct 13 2010 Nalin Dahyabhai <nalin@redhat.com> 0.32-1
- oops, rfc5280 says we shouldn't be populating unique identifiers, so
  make it a configuration option and default the behavior to off

* Tue Oct 12 2010 Nalin Dahyabhai <nalin@redhat.com> 0.31-1
- start populating the optional unique identifier fields in self-signed
  certificates

* Thu Sep 30 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30-4
- explicitly require "dbus" to try to ensure we have a running system bus
  when we get started (#639126)

* Wed Sep 29 2010 jkeating - 0.30-3
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30-2
- try to SIGHUP the messagebus daemon at first install so that it'll
  let us claim our service name if it isn't restarted before we are
  first started (#636876)

* Wed Aug 25 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30-1
- update to 0.30
  - fix errors computing the time at the end of an interval that were
    caught by self-tests

* Mon Aug 23 2010 Nalin Dahyabhai <nalin@redhat.com> 0.29-1
- update to 0.29
  - fix 64-bit cleanliness issue using libdbus
  - actually include the full set of tests in tarballs

* Tue Aug 17 2010 Nalin Dahyabhai <nalin@redhat.com> 0.28-1
- update to 0.28
  - fix self-signing certificate notBefore and notAfter values on 32-bit
    machines

* Tue Aug 17 2010 Nalin Dahyabhai <nalin@redhat.com> 0.27-1
- update to 0.27
  - portability and test fixes

* Fri Aug 13 2010 Nalin Dahyabhai <nalin@redhat.com> 0.26-1
- update to 0.26
  - when canceling a submission request that's being handled by a helper,
    reap the child process's status after killing it (#624120)

* Fri Aug 13 2010 Nalin Dahyabhai <nalin@redhat.com> 0.25-1
- update to 0.25
  - new translations
    - in by Okta Purnama Rahadian!
  - fix detection of cases where we can't access a private key in an NSS
    database because we don't have the PIN
  - teach '*getcert start-tracking' about the -p and -P options which the
    '*getcert request' commands already understand (#621670), and also
    the -U, -K, -E, and -D flags
  - double-check that the nicknames of keys we get back from
    PK11_ListPrivKeysInSlot() match the desired nickname before accepting
    them as matches, so that our tests won't all blow up on EL5
  - fix dynamic addition and removal of CAs implemented through helpers

* Mon Jun 28 2010 Nalin Dahyabhai <nalin@redhat.com> 0.24-4
- init script: ensure that the subsys lock is created whenever we're called to
  "start" when we're already running (even more of #596719)

* Tue Jun 15 2010 Nalin Dahyabhai <nalin@redhat.com> 0.24-3
- more gracefully handle manual daemon startups and cleaning up of unexpected
  crashes (still more of #596719)

* Thu Jun 10 2010 Nalin Dahyabhai <nalin@redhat.com> 0.24-2
- don't create the daemon pidfile until after we've connected to the D-Bus
  (still more of #596719)

* Tue Jun  8 2010 Nalin Dahyabhai <nalin@redhat.com> 0.24-1
- update to 0.24
  - keep the lock on the pid file, if we have one, when we fork, and cancel
    daemon startup if we can't gain ownership of the lock (the rest of #596719)
  - make the man pages note which external configuration files we consult when
    submitting requests to certmaster and ipa CAs

* Thu May 27 2010 Nalin Dahyabhai <nalin@redhat.com> 0.23-1
- update to 0.23
  - new translations
    - pl by Piotr Drąg!
  - cancel daemon startup if we can't gain ownership of our well-known
    service name on the DBus (#596719)

* Fri May 14 2010 Nalin Dahyabhai <nalin@redhat.com> 0.22-1
- update to 0.22
  - new translations
    - de by Fabian Affolter!
  - certmaster-submit: don't fall over when we can't find a certmaster.conf
    or a minion.conf (i.e., certmaster isn't installed) (#588932)
  - when reading extension values from certificates, prune out duplicate
    principal names, email addresses, and hostnames

* Tue May  4 2010 Nalin Dahyabhai <nalin@redhat.com> 0.21-1
- update to 0.21
  - getcert/*-getcert: relay the desired CA to the local service, whether
    specified on the command line (in getcert) or as a built-in hard-wired
    default (in *-getcert) (#584983)
  - flesh out the default certmonger.conf so that people can get a feel for
    the expected formatting (Jenny Galipeau)

* Wed Apr 21 2010 Nalin Dahyabhai <nalin@redhat.com> 0.20-1
- update to 0.20
  - correctly parse certificate validity periods given in years (spotted by
    Stephen Gallagher)
  - setup for translation
    - es by Héctor Daniel Cabrera!
    - ru by Yulia Poyarkova!
    - uk by Yuri Chornoivan!
  - fix unpreprocessed defaults in certmonger.conf's man page
  - tweak the IPA-specific message that indicates a principal name also needs
    to be specified if we're not using the default subject name (#579542)
  - make the validity period of self-signed certificates into a configuration
    setting and not a piece of the state information we track about the signer
  - init script: exit with status 2 instead of 1 when invoked with an
    unrecognized argument (#584517)

* Tue Mar 23 2010 Nalin Dahyabhai <nalin@redhat.com> 0.19-1
- update to 0.19
  - correctly initialize NSS databases that need to be using a PIN
  - add certmonger.conf, for customizing notification timings and settings,
    and use of digests other than the previously-hard-coded SHA256, and
    drop those settings from individual requests
  - up the default self-sign validity interval from 30 days to 365 days
  - drop the first default notification interval from 30 days to 28 days
    (these two combined to create a fun always-reissuing loop earlier)
  - record the token which contains the key or certificate when we're
    storing them in an NSS database, and report it
  - improve handling of cases where we're supposed to use a PIN but we
    either don't have one or we have the wrong one
  - teach getcert to accept a PIN file's name or a PIN value when adding
    a new entry
  - update the IPA submission helper to use the new 'request_cert' signature
    that's landing soon
  - more tests

* Fri Feb 12 2010 Nalin Dahyabhai <nalin@redhat.com> 0.18-1
- update to 0.18
  - add support for using encrypted storage for keys, using PIN values
    supplied directly or read from files whose names are supplied
  - don't choke on NSS database locations that use the "sql:" or "dbm:"
    prefix

* Mon Jan 25 2010 Nalin Dahyabhai <nalin@redhat.com> 0.17-2
- make the D-Bus configuration file (noreplace) (#541072)
- make the %%check section and the deps we have just for it conditional on
  the same macro (#541072)

* Wed Jan  6 2010 Nalin Dahyabhai <nalin@redhat.com> 0.17-1
- update to 0.17
  - fix a hang in the daemon (Rob Crittenden)
  - documentation updates
  - fix parsing of submission results from IPA (Rob Crittenden)

* Fri Dec 11 2009 Nalin Dahyabhai <nalin@redhat.com> 0.16-1
- update to 0.16
  - set a umask at startup (Dan Walsh)

* Tue Dec  8 2009 Nalin Dahyabhai <nalin@redhat.com> 0.15-1
- update to 0.15
  - notice that a directory with a trailing '/' is the same location as the
    directory without it
  - fix handling of the pid file when we write one (by actually giving it
    contents)

* Wed Nov 25 2009 Nalin Dahyabhai <nalin@redhat.com> 0.14-1
- update to 0.14
  - check key and certificate location at add-time to make sure they're
    absolute paths to files or directories, as appropriate
  - IPA: dig into the 'result' item if the named result value we're looking
    for isn't in the result struct

* Tue Nov 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.13-1
- update to 0.13
  - change the default so that we default to trying to auto-refresh
    certificates unless told otherwise
  - preemptively enforce limitations on request nicknames so that they
    make valid D-Bus object path components

* Tue Nov 24 2009 Nalin Dahyabhai <nalin@redhat.com> 0.12-1
- update to 0.12
  - add a crucial bit of error reporting when CAs reject our requests
  - count the number of configured CAs correctly

* Mon Nov 23 2009 Nalin Dahyabhai <nalin@redhat.com> 0.11-1
- update to 0.11
  - add XML-RPC submission for certmaster and IPA
  - prune entries with duplicate names from the data store

* Fri Nov 13 2009 Nalin Dahyabhai <nalin@redhat.com> 0.10-1
- update to 0.10
  - add some compiler warnings and then fix them

* Fri Nov 13 2009 Nalin Dahyabhai <nalin@redhat.com> 0.9-1
- update to 0.9
  - run external submission helpers correctly
  - fix signing of signing requests generated for keys stored in files
  - only care about new interface and route notifications from netlink,
    and ignore notifications that don't come from pid 0
  - fix logic for determining expiration status
  - correct the version number in self-signed certificates

* Tue Nov 10 2009 Nalin Dahyabhai <nalin@redhat.com> 0.8-1
- update to 0.8
  - encode windows UPN values in requests correctly
  - watch for netlink routing changes and restart stalled submission requests
  - 'getcert resubmit' can force a regeneration of the CSR and submission

* Fri Nov  6 2009 Nalin Dahyabhai <nalin@redhat.com> 0.7-1
- update to 0.7
  - first cut at a getting-started document
  - refactor some internal key handling with NSS
  - check for duplicate request nicknames at add-time

* Tue Nov  3 2009 Nalin Dahyabhai <nalin@redhat.com> 0.6-1
- update to 0.6
  - man pages
  - 'getcert stop-tracking' actually makes the server forget now
  - 'getcert request -e' was redundant, dropped the -e option
  - 'getcert request -i' now sets the request nickname
  - 'getcert start-tracking -i' now sets the request nickname

* Mon Nov  2 2009 Nalin Dahyabhai <nalin@redhat.com> 0.5-1
- update to 0.5
  - packaging fixes
  - add a selfsign-getcert client
  - self-signed certs now get basic constraints and their own serial numbers
  - accept id-ms-kp-sc-logon as a named EKU value in a request

* Thu Oct 29 2009 Nalin Dahyabhai <nalin@redhat.com> 0.4-1
- update to 0.4

* Thu Oct 22 2009 Nalin Dahyabhai <nalin@redhat.com> 0.1-1
- update to 0.1

* Sun Oct 18 2009 Nalin Dahyabhai <nalin@redhat.com> 0.0-1
- initial package
