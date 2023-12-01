Vendor:         Microsoft Corporation
Distribution:   Mariner
%global build_sample_subpackage 0


%global dbus_send /usr/bin/dbus-send





%global systemd 1
%global sysvinit 0






%global separate_usr 0




Name: oddjob
Version: 0.34.6
Release: 2%{?dist}
Source0: https://releases.pagure.org/oddjob/oddjob-%{version}.tar.gz
Source1: https://releases.pagure.org/oddjob/oddjob-%{version}.tar.gz.sig
Summary: A D-Bus service which runs odd jobs on behalf of client applications
License: BSD
BuildRequires:  gcc
BuildRequires: dbus-devel >= 0.22, dbus-x11, libselinux-devel, libxml2-devel
BuildRequires: pam-devel, pkgconfig
BuildRequires: cyrus-sasl-devel, krb5-devel, openldap-devel
BuildRequires: docbook-dtds, xmlto
%if %{systemd}
BuildRequires:	systemd-units
BuildRequires:  systemd-devel
Requires(post):	systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units
Requires(post):	systemd-sysv
%else
Requires(post): /sbin/service
Requires(postun): /sbin/service
Requires(post): /sbin/chkconfig
Requires(pre): /sbin/chkconfig
%endif
Requires: dbus
# for "killall"
Requires(post): psmisc
Obsoletes: oddjob-devel < 0.30, oddjob-libs < 0.30, oddjob-python < 0.30
URL: https://pagure.io/oddjob

%if %{systemd}
BuildRequires:  systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires(post): systemd-sysv
%endif

%if %{sysvinit}
Requires(post): /sbin/chkconfig, /sbin/service
Requires(preun): /sbin/chkconfig, /sbin/service
%endif


%description
oddjob is a D-Bus service which performs particular tasks for clients which
connect to it and issue requests using the system-wide message bus.

%package mkhomedir
Summary: An oddjob helper which creates and populates home directories
Requires: %{name} = %{version}-%{release}
Requires(post): %{dbus_send}, grep, sed, psmisc

%description mkhomedir
This package contains the oddjob helper which can be used by the
pam_oddjob_mkhomedir module to create a home directory for a user
at login-time.

%package sample
Summary: A sample oddjob service.
Requires: %{name} = %{version}-%{release}

%description sample
This package contains a trivial sample oddjob service.

%prep
%setup -q

%build
sample_flag=
%if %{build_sample_subpackage}
sample_flag=--enable-sample
%endif
%configure \
	--disable-static \
	--enable-pie --enable-now \
	--with-selinux-acls \
	--with-selinux-labels \
	--without-python --enable-xml-docs --enable-compat-dtd \
	--disable-dependency-tracking \
%if %{systemd}
	--enable-systemd --disable-sysvinit \
%else
	--enable-sysvinit --disable-systemd \
%endif
	$sample_flag
make %{_smp_mflags}

%install
rm -fr "$RPM_BUILD_ROOT"
make install DESTDIR="$RPM_BUILD_ROOT"
rm -f "$RPM_BUILD_ROOT"/%{_libdir}/security/*.la
rm -f "$RPM_BUILD_ROOT"/%{_libdir}/security/*.a
%if %{separate_usr}
if ! test -d "$RPM_BUILD_ROOT"/%{_lib}/security ; then
	mkdir -p "$RPM_BUILD_ROOT"/%{_lib}/security
	mv "$RPM_BUILD_ROOT"/%{_libdir}/security/*.so "$RPM_BUILD_ROOT"/%{_lib}/security/
fi
%endif
# Recommended, though I disagree.
rm -f "$RPM_BUILD_ROOT"/%{_libdir}/*.la

%if ! %{build_sample_subpackage}
# Go ahead and build the sample layout.
mkdir -p sample-install-root/sample/{%{_sysconfdir}/{dbus-1/system.d,%{name}d.conf.d},%{_libdir}/%{name}}
install -m644 sample/oddjobd-sample.conf	sample-install-root/sample/%{_sysconfdir}/%{name}d.conf.d/
install -m644 sample/oddjob-sample.conf		sample-install-root/sample/%{_sysconfdir}/dbus-1/system.d/
install -m755 sample/oddjob-sample.sh		sample-install-root/sample/%{_libdir}/%{name}/
%endif

# Make sure we don't needlessly make these docs executable.
chmod -x src/reload src/mkhomedirfor src/mkmyhomedir

# Make sure the datestamps match in multilib pairs.
touch -r src/oddjobd-mkhomedir.conf.in	$RPM_BUILD_ROOT/%{_sysconfdir}/oddjobd.conf.d/oddjobd-mkhomedir.conf
touch -r src/oddjob-mkhomedir.conf.in	$RPM_BUILD_ROOT/%{_sysconfdir}/dbus-1/system.d/oddjob-mkhomedir.conf

%files
%doc *.dtd COPYING NEWS QUICKSTART doc/oddjob.html src/reload
%if ! %{build_sample_subpackage}
%doc sample-install-root/sample
%endif
%if %{systemd}
%{_unitdir}/oddjobd.service
%else
%{_initrddir}/oddjobd
%endif
%{_bindir}/*
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/dbus-*/system.d/oddjob.conf
%config(noreplace) %{_sysconfdir}/oddjobd.conf
%dir %{_sysconfdir}/oddjobd.conf.d
%config(noreplace) %{_sysconfdir}/oddjobd.conf.d/oddjobd-introspection.conf
%dir %{_sysconfdir}/%{name}
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/sanity.sh
%{_mandir}/*/oddjob.*
%{_mandir}/*/oddjob_request.*
%{_mandir}/*/oddjobd.*
%{_mandir}/*/oddjobd-introspection.*

%files mkhomedir
%doc src/mkhomedirfor src/mkmyhomedir
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/mkhomedir
%if %{separate_usr}
/%{_lib}/security/pam_oddjob_mkhomedir.so
%else
%{_libdir}/security/pam_oddjob_mkhomedir.so
%endif
%{_mandir}/*/pam_oddjob_mkhomedir.*
%{_mandir}/*/oddjob-mkhomedir.*
%{_mandir}/*/oddjobd-mkhomedir.*
%config(noreplace) %{_sysconfdir}/dbus-*/system.d/oddjob-mkhomedir.conf
%config(noreplace) %{_sysconfdir}/oddjobd.conf.d/oddjobd-mkhomedir.conf

%if %{build_sample_subpackage}
%files sample
%{_libdir}/%{name}/oddjob-sample.sh
%config %{_sysconfdir}/dbus-*/system.d/oddjob-sample.conf
%config %{_sysconfdir}/oddjobd.conf.d/oddjobd-sample.conf
%endif

%post
if test $1 -eq 1 ; then
	killall -HUP dbus-daemon 2>&1 > /dev/null
fi
%if %{systemd}
%systemd_post oddjobd.service
%endif
%if %{sysvinit}
/sbin/chkconfig --add oddjobd
%endif

%postun
%if %{systemd}
%systemd_postun_with_restart oddjobd.service
%endif
%if %{sysvinit}
if [ $1 -gt 0 ] ; then
	/sbin/service oddjobd condrestart 2>&1 > /dev/null || :
fi
%endif
exit 0

%preun
%if %{systemd}
%systemd_preun oddjobd.service
%endif
%if %{sysvinit}
if [ $1 -eq 0 ] ; then
	/sbin/service oddjobd stop > /dev/null 2>&1
	/sbin/chkconfig --del oddjobd
fi
%endif
exit 0

%if %{systemd}
%triggerun -- oddjobd < 0.31.3
# Save the current service runlevel info, in case the user wants to apply
# the enabled status manually later, by running
#   "systemd-sysv-convert --apply oddjobd".
%{_bindir}/systemd-sysv-convert --save oddjobd >/dev/null 2>&1 ||:
# Do this because the old package's %%postun doesn't know we need to do it.
/sbin/chkconfig --del oddjobd >/dev/null 2>&1 || :
# Do this because the old package's %%postun wouldn't have tried.
/bin/systemctl try-restart oddjobd.service >/dev/null 2>&1 || :
exit 0
%endif

%post mkhomedir
# Adjust older configuration files that may have been modified so that they
# point to the current location of the helper.
cfg=%{_sysconfdir}/oddjobd.conf.d/oddjobd-mkhomedir.conf
if grep -q %{_libdir}/%{name}/mkhomedir $cfg ; then
	sed -i 's^%{_libdir}/%{name}/mkhomedir^%{_libexecdir}/%{name}/mkhomedir^g' $cfg
fi
if test $1 -eq 1 ; then
	killall -HUP dbus-daemon 2>&1 > /dev/null
fi
if [ -f /var/lock/subsys/oddjobd ] ; then
	%{dbus_send} --system --dest=com.redhat.oddjob /com/redhat/oddjob com.redhat.oddjob.reload
fi
exit 0

%changelog
* Mon Jun 14 2021 Olivia Crain <oliviacrain@microsoft.com> - 0.34.6-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Add explicit build dependency on systemd-devel for systemd pkgconfig files

* Thu May  7 2020 Nalin Dahyabhai <nalin@redhat.com> - 0.34.6-1
- update license on src/buffer.h
- change /var/run -> /run in systemd service file (Orion Poplawski)

* Thu May  7 2020 Nalin Dahyabhai <nalin@redhat.com> - 0.34.5-1
- apply patch from Matthias Gerstner of the SUSE security team to fix a
  possible race condition in the mkhomedir helper (CVE-2020-10737)
- only process SELinux contexts if SELinux is not disabled (Alexander Bokovoy)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Dec  4 2018 Nalin Dahyabhai <nalin@redhat.com> - 0.34.4-7
- Drop Python 2 build-time dependency, which hasn't been used since we turned
  off building the python bindings years ago (#1595853, #1642502).

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 19 2018 Iryna Shcherbina <ishcherb@redhat.com> - 0.34.4-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Feb 26 2017 Nalin Dahyabhai <nalin@redhat.com> - 0.34.4-1
- when "prepend_user_name" is used, the user name is now added to the helper's
  command line after arguments that were specified in the helper "exec"
  attribute
- resync with Fedora packaging

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.34.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 10 2015 Nalin Dahyabhai <nalin@redhat.com> - 0.34.3-1
- tweak initialization so that we set up for providing our D-Bus APIs before we
  register our names with the bus, so that we can handle any requests that
  arrive before the acknowledgement of that registration, which should make
  system activation a viable option

* Tue Jun 30 2015 Nalin Dahyabhai <nalin@redhat.com> - 0.34.2-1
- fix a crasher in pam_oddjob_mkhomedir.so: remove an initialization step that
  should have been removed when the module was modified to accept larger
  replies (#1236970)

* Wed Jun 24 2015 Nalin Dahyabhai <nalin@redhat.com> - 0.34.1-1
- build fixes

* Wed Jun 24 2015 Nalin Dahyabhai <nalin@redhat.com> - 0.34-1
- open a connection to the bus for every service we're serving, instead of
  using just one for the lot of them, so that we can tell which service a
  client was attempting to contact if it sends a message to our unique
  connection address instead of a well-known name, like dbus-python does
- tweak the logic for guessing which interface name is right when a request
  doesn't include one, so that it has a better chance of finding the right one
- increase the initial size of the buffer that we pass to getpwnam_r in the
  pam_oddjob_mkhomedir module (#1198812)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Dec 04 2014 Nalin Dahyabhai <nalin@redhat.com>
- make that last change dependent on which release we're building for

* Thu Dec 04 2014 David King <amigadave@amigadave.com> - 0.33-4
- Update dbus-send dependency for new dbus (#1170584)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Nalin Dahyabhai <nalin@redhat.com> 0.33
- catch calls to the method invocation helper function that mistakenly
  didn't include the newly-required timeout value (#1089655,#1089656)

* Tue Apr  8 2014 Nalin Dahyabhai <nalin@redhat.com> 0.32.1-1
- stop overriding the system-wide UMASK default in our default
  oddjobd-mkhomedir.conf file (#995097)

* Tue Apr  8 2014 Nalin Dahyabhai <nalin@redhat.com> 0.32-1
- add a -t flag to oddjob_request to allow its timeout to be
  customized (#1085491)

* Tue Apr  8 2014 Nalin Dahyabhai <nalin@redhat.com> 0.31.5-2
- explicitly require "dbus" at the package level (#1085450)

* Tue Jul 30 2013 Nalin Dahyabhai <nalin@redhat.com> 0.31.5-1
- add man(5) pages for the configuration files that we include which get
  included by others, just to be tidy (#884552)

* Fri May 17 2013 Nalin Dahyabhai <nalin@redhat.com> 0.31.4-1
- add an [Install] section containing WantedBy=sysinit.target to the systemd
  unit file (#963722), allowing it to actually be "enabled"

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Nalin Dahyabhai <nalin@redhat.com> 0.31.3-2
- use %%systemd_postun_with_restart instead of plain old %%systemd_postun,
  because we can be restarted in the %%postun

* Thu Jan 17 2013 Nalin Dahyabhai <nalin@redhat.com> 0.31.3-1
- use newer systemd macros (#857375)

* Wed Nov 21 2012 Nalin Dahyabhai <nalin@redhat.com> 0.31.2-3
- add that dependency to the right subpackage

* Wed Nov 21 2012 Nalin Dahyabhai <nalin@redhat.com> 0.31.2-2
- add missing requires(post) on killall, which we use to poke the message
  bus daemon to get it to reload its configuration, spotted by rcritten

* Wed Aug 29 2012 Nalin Dahyabhai <nalin@redhat.com> 0.31.2-1
- refer to $local_fs instead of $localfs in the init script (#802719)
- install a systemd unit file instead of an init script on still-in-development
  releases (#820137,818963)
- build binaries position-independent and marked for earliest-possible symbol
  resolution (#852800)
- don't worry about moving things from /usr to / when they're the same (#852800)

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 15 2011 Nalin Dahyabhai <nalin@redhat.com> 0.31.1-1
- also tell the system message bus to reload its configuration when we install
  a subpackage with a new service in it

* Tue Feb  8 2011 Nalin Dahyabhai <nalin@redhat.com>
- make the init script exit with status 2 when given an unknown command, rather
  than with status 1 (#674534)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.31-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan 25 2011 Nalin Dahyabhai <nalin@redhat.com> 0.31-1
- require dbus-x11 so that the tests can use dbus-launch
- try to read the default umask from /etc/login.defs (more of #666418)

* Mon Jan  3 2011 Nalin Dahyabhai <nalin@redhat.com>
- when the mkhomedir helper has to create intermediate directories, don't
  apply a umask that might have been supplied on its command line (#666418)

* Fri Nov  5 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30.2-3
- rebuild with new libxml2

* Wed Sep 29 2010 jkeating - 0.30.2-2
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30.2-2
- try to SIGHUP the messagebus daemon at first install so that it'll
  let us claim our service name if it isn't restarted before we are
  first started (same as #636876)

* Thu Sep 16 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30.2-1
- don't try to "close" our shared connection to the bus when the bus
  hangs up on us -- at some point libdbus started abort()ing when we try
  that (#634356)

* Thu Apr  1 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30.1-1
- documentation tweaks for man pages

* Wed Jan 27 2010 Nalin Dahyabhai <nalin@redhat.com> 0.30-1
- drop the shared library and python bindings, which so far as i can tell
  weren't being used, obsoleting them to avoid a mess on upgrades
- move the mkhomedir helper from %%{_libdir}/%%{name} to
  %%{_libexecdir}/%%{name} to make the multilib configuration files agree
  (#559232)
- use %%global instead of %%define

* Mon Jan 25 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.29.1-5
- show that we implement force-reload and try-restart in the init script's
  help message (#522131)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.29.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 0.29.1-2
- Rebuild for Python 2.6

* Wed May 28 2008 Nalin Dahyabhai <nalin@redhat.com> 0.29.1-1
- when we install the mkhomedir subpackage, if there's a running oddjobd, ask
  it to reload its configuration
- fix missing bits from the namespace changes in configuration files
- restart the service in %%postun

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.29-2
- Autorebuild for GCC 4.3

* Wed Sep  5 2007 Nalin Dahyabhai <nalin@redhat.com> 0.29-1
- split off mkhomedir bits into a subpackage (#236820)
- take a pass at new-init-ifying the init script (#247005)

* Thu Aug 16 2007 Nalin Dahyabhai <nalin@redhat.com>
- move helpers to libexecdir, keeping pkglibdir around in the package (#237207)

* Mon Apr  9 2007 Nalin Dahyabhai <nalin@redhat.com> 0.28-1
- split off python subpackage, make -devel depend on -libs, let autodeps
  provide the main package's dependency on -libs (#228377)

* Thu Feb 15 2007 Nalin Dahyabhai <nalin@redhat.com> 0.27-8
- configure with --disable-dependency-tracking (Ville Skyttä, #228928)

* Thu Jul 27 2006 Nalin Dahyabhai <nalin@redhat.com> 0.27-7
- unmark the init script as a %%config file (part of #197182)

* Thu Jul 20 2006 Nalin Dahyabhai <nalin@redhat.com> 0.27-6
- rebuild

* Thu Jul 20 2006 Nalin Dahyabhai <nalin@redhat.com> 0.27-5
- rebuild

* Thu Jul 20 2006 Nalin Dahyabhai <nalin@redhat.com> 0.27-4
- rebuild

* Thu Jul 20 2006 Nalin Dahyabhai <nalin@redhat.com> 0.27-3
- rebuild

* Thu Jul 20 2006 Nalin Dahyabhai <nalin@redhat.com> 0.27-2
- rebuild

* Wed Jul 19 2006 Nalin Dahyabhai <nalin@redhat.com> 0.27-1
- update to 0.27-1:
  - don't attempt to subscribe to all possible messages -- the message bus
    will already route to us messages addressed to us, and if we try for
    more than that we may run afoul of SELinux policy, generating spewage
- add a build dependency on pkgconfig, for the sake of FC3
- update docs and comments because D-BUS is now called D-Bus

* Tue May  2 2006 Nalin Dahyabhai <nalin@redhat.com> 0.26-4
- rebuild

* Tue May  2 2006 Nalin Dahyabhai <nalin@redhat.com> 0.26-3
- rebuild

* Tue May  2 2006 Nalin Dahyabhai <nalin@redhat.com> 0.26-2
- rebuild

* Tue May  2 2006 Nalin Dahyabhai <nalin@redhat.com> 0.26-1
- update to 0.26-1:
  - don't get confused when ACL entries for introspection show up in the
    configuration before we add the handlers for them
  - export $ODDJOB_CALLING_USER to helpers

* Tue May  2 2006 Nalin Dahyabhai <nalin@redhat.com>
- add recommended dependency on pkgconfig in the -devel subpackage

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-8
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-7
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-6
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-5
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-4
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-3
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-2
- rebuild

* Tue Apr 11 2006 Nalin Dahyabhai <nalin@redhat.com> 0.25-1
- update to 0.25:
  - add introspection for parents of objects specified in the configuration
  - oddjobd can reload its configuration now
  - add -u (umask) and -s (skeldir) flags to the mkhomedir helper (#246681)

* Tue Feb 28 2006 Nalin Dahyabhai <nalin@redhat.com> 0.24-1
- update to 0.24, fixing some build errors against D-BUS 0.30-0.33
- require xmlto, because the generated HTML differs depending on whether
  or not we know how to enforce ACLs which include SELinux context info
- build with DocBook 4.3

* Mon Feb 27 2006 Nalin Dahyabhai <nalin@redhat.com> 0.23-3
- rebuild

* Mon Feb 27 2006 Nalin Dahyabhai <nalin@redhat.com> 0.23-2
- rebuild

* Fri Jan 27 2006 Nalin Dahyabhai <nalin@redhat.com> 0.23-1
- fix compilation against older versions of D-BUS if the
  GetConnectionSELinuxSecurityContext method turns out to be available

* Mon Jan 16 2006 Nalin Dahyabhai <nalin@redhat.com> 0.22-1
- fix some path mismatches in the sample configuration files
- don't try to set a reconnect timeout until after we've connected

* Mon Jan  9 2006 Nalin Dahyabhai <nalin@redhat.com> 0.21-3
- prefer BuildRequires: to BuildPrereq (#176452)
- require /sbin/service at uninstall-time, because we use it (#176452)
- be more specific about when we require /sbin/chkconfig (#176452)

* Fri Jan  6 2006 Nalin Dahyabhai <nalin@redhat.com> 0.21-2
- add some missing build-time requirements

* Thu Dec 22 2005 Nalin Dahyabhai <nalin@redhat.com> 0.21-1
- fix the location for the sample D-BUS configuration doc file
- own more created directories

* Thu Dec 22 2005 Nalin Dahyabhai <nalin@redhat.com> 0.20-1
- update to 0.20
- break shared libraries and modules for PAM and python into a subpackage
  for better behavior on multilib boxes
- if we're not building a sample subpackage, include the sample files in
  the right locations as %%doc files
