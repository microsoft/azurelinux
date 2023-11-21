Summary:        A system tool for maintaining the %{_sysconfdir}/rc*.d hierarchy
Name:           chkconfig
Version:        1.25
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Base
URL:            https://github.com/fedora-sysv/chkconfig
Source0:        https://github.com/fedora-sysv/chkconfig/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  gettext
BuildRequires:  libselinux-devel
BuildRequires:  newt-devel
BuildRequires:  pkg-config
BuildRequires:  popt-devel
Requires:       libselinux
Requires:       libsepol
Requires:       newt
Requires:       popt
Requires:       slang
Conflicts:      initscripts <= 5.30-1
Provides:       alternatives = %{version}-%{release}
Provides:       update-alternatives = %{version}-%{release}
Provides:       /sbin/chkconfig

%description
Chkconfig is a basic system utility.  It updates and queries runlevel
information for system services.  Chkconfig manipulates the numerous
symbolic links in /etc/rc.d, to relieve system administrators of some 
of the drudgery of manually editing the symbolic links.

%package -n ntsysv
Summary:        A tool to set the stop/start of system services in a runlevel
Group:          System Environment/Base
Requires:       chkconfig

%description -n ntsysv
Ntsysv provides a simple interface for setting which system services
are started or stopped in various runlevels (instead of directly
manipulating the numerous symbolic links in /etc/rc.d). Unless you
specify a runlevel or runlevels on the command line (see the man
page), ntsysv configures the current runlevel (5 if you're using X).

%package  lang
Summary:  Additional language files for chkconfig
Group:    System Environment/Base
Requires: %{name} = %{version}-%{release}

%description lang
These are the additional language files of chkconfig

%prep
%setup -q

%build
make RPM_OPT_FLAGS="%{optflags}" LDFLAGS="$RPM_LD_FLAGS" %{?_smp_mflags}

%check
# Mask the check section as it depends on beakerlib which is currently not
# provided by CBL-Mariner

# make check

%install
make DESTDIR=%{buildroot} \
     MANDIR=%{_mandir} \
     SBINDIR=%{_sbindir} \
     SYSTEMDUTILDIR=%{_libdir}/systemd \
     install

mkdir -p %{buildroot}%{_sysconfdir}/rc.d/init.d
ln -s rc.d/init.d %{buildroot}%{_sysconfdir}/init.d
for n in 0 1 2 3 4 5 6; do
    mkdir -p %{buildroot}%{_sysconfdir}/rc.d/rc${n}.d
    ln -s rc.d/rc${n}.d %{buildroot}%{_sysconfdir}/rc${n}.d
done
mkdir -p %{buildroot}%{_sysconfdir}/chkconfig.d

%find_lang %{name}

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_sbindir}/chkconfig
%{_sysconfdir}/chkconfig.d
%{_sysconfdir}/init.d
%{_sysconfdir}/rc.d
%{_sysconfdir}/rc.d/init.d
%{_sysconfdir}/rc[0-6].d
%{_sysconfdir}/rc.d/rc[0-6].d
%{_mandir}/*/chkconfig*
%{_libdir}/systemd/systemd-sysv-install

%dir %{_sysconfdir}/alternatives
%{_sbindir}/update-alternatives
%{_sbindir}/alternatives
%{_mandir}/*/update-alternatives*
%{_mandir}/*/alternatives*
%dir %{_sharedstatedir}/alternatives

%files -n ntsysv
%defattr(-,root,root)
%{_sbindir}/ntsysv
%{_mandir}/*/ntsysv.8*

%files -f %{name}.lang lang
%defattr(-,root,root)

%changelog
* Tue Nov 21 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.25-1
- Auto-upgrade to 1.25 - Azure Linux 3.0 - package upgrades

* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.20-4
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Wed Apr 13 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 1.20-3
- Create lang sub package for locales

* Thu Jan 20 2022 Muhammad Falak <mwani@microsoft.com> - 1.20-2
- Mask `check` section which depends on `beakerlib`

* Tue Jan 11 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.20-1
- Upgrade to 1.20.

* Fri Feb 05 2021 Joe Schmitt <joschmit@microsoft.com> - 1.11-3
- Replace incorrect %%{_lib} usage with %%{_libdir}

* Tue Nov 17 2020 Joe Schmitt <joschmit@microsoft.com> - 1.11-2
- Provide alternatives and update-alternatives.
- Remove sha1 define.

* Wed Mar 18 2020 Emre Girgin <mrgirgin@microsoft.com> 1.11-1
- Initial CBL-Mariner import from Photon (license: Apache2).
- Upgrade to 1.11. License verified.

* Fri Apr 07 2017 Anish Swaminathan <anishs@vmware.com> 1.9-1
- Upgrade to 1.9

* Mon Oct 31 2016 Anish Swaminathan <anishs@vmware.com> 1.5-7
- Chkconfig patch to fix interaction with systemd

* Tue Sep 13 2016 Anish Swaminathan <anishs@vmware.com> 1.5-6
- Chkconfig patch to return runlevel 3 on Photon OS

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.5-5
- GA - Bump release of all rpms

* Mon Dec 07 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Ability for chkconfig to ignore priorities.

* Tue Dec 01 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Allowing chkconfing to print service on/off status on the current runlevel.

* Fri Nov 20 2015 Sharath George <sharathg@vmware.com>
- Adding shortopt for add and delete.

* Tue Oct 27 2015 Mahmoud Bassiouny <mbassiouny@vmware.com>
- Initial build for PhotonOS.  First version

* Mon Jun 01 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 1.5-1
- add systemd-sysv-install alias
- don't create symlinks if they already exist
- fix wrongly behaving LDFLAGS

* Thu Mar 26 2015 Lukáš Nykrýn <lnykryn@redhat.com> - 1.4-1
- ntsysv: show systemd services and sockets
- fix combination --type xinetd --list service
- leveldb: restore selinux context for xinetd conf files
- alternatives: remove unused variable
- alternatives: warn if the target is not a symlink
- spec: add link to git
- lets simplify version

* Wed Nov 05 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.63-1
- alternatives: during install don't call preset on enabled services

* Tue Aug 12 2014 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.62-1
- use systemctl preset, not systemctl enable
- fix typo in manpage
- partly support socket activated services

* Wed Jul 31 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.61-1
- try to make install_initd work
- fix permission issues with xinetd services

* Tue Mar 12 2013 Lukáš Nykrýn <lnykryn@redhat.com> - 1.3.60-1
- don't completely override LDFLAGS
- pass along any rpm-configured LD flags
- make sure install_initd/remove_initd provides appropriate help output for those commands (#803818)
- check for overridden services in /etc too (#850899)
- chconfig should own /etc/rc.d (#894328)
- isXinetdEnabled should also ask systemd (#820363)
- alternatives: look for service file also in /etc
- alternatives: add --list option (#622635)
- chkconfig: add hint to call systemctl list-unit-files and list-dependencies (#800334)
- chkconfig: correctly handle unreadable init.d (#913807)
- alternatives: call systemctl enable with --force (#915667)

* Wed Mar  7 2012 Bill Nottingham <notting@redhat.com> 1.3.59-1
- translation updates
- xinetd may be a systemd service. Make sure we can still reload it (#800490)

* Fri Feb 10 2012 Bill Nottingham <notting@redhat.com> 1.3.58-1
- fix forwarding to systemctl with systemd >= 41 (#789256)
- assorted regression fixes from 1.3.57 (#782152, etc.)

* Wed Jan 04 2012 Bill Nottingham <notting@redhat.com> 1.3.57-1
- assorted cleanups to LSB dependency support (#693202 fixed properly, #701573)
- fix kill values for LSB-only scripts (#696305, <jbastian@redhat.com>)
- don't apply start deps for services that aren't starting anywhere (#750446)

* Tue Oct 11 2011 Bill Nottingham <notting@redhat.com> 1.3.56-1
- add the systemd warning when no arguments are passed (<harald@redhat.com>)

* Wed Aug 31 2011 Bill Nottingham <notting@redhat.com> 1.3.55-1
- update translations (#734631)

* Tue Jul 19 2011 Bill Nottingham <notting@redhat.com> 1.3.54-1
- alternatives: fix --initscript systemd support (#714830)
- revert forwarding of 'chkconfig --del' to 'systemctl disable'

* Fri Jul 15 2011 Bill Nottingham <notting@redhat.com> 1.3.53-1
- ntsysv: change the default to configure runlevels 2/3/4/5 (#709254)
- alternatives: check whether the --initscript param is a systemd service, act appropriately (#714830)
- forward chkconfig --del to systemctl disable where necessary

* Wed Apr 27 2011 Bill Nottingham <notting@redhat.com> 1.3.52-1
- set state before frobbing dependencies (#693202)
- ntsysv: don't list or configure service overridden by systemd (#691224)
- chkconfig: don't show services overridden by systemd in --list (#693504, #693500)
- don't forward to systemd if it's not installed (<arvidjaar@gmail.com>)
- update translations

* Wed Mar 09 2011 Bill Nottingham <notting@redhat.com> 1.3.51-1
- further fixes to systemctl integration (<lennart@poettering.net>, <arvidjaar@gmail.com>)

* Wed Feb 16 2011 Bill Nottingham <notting@redhat.com> 1.3.50-1
- forward actions to systemctl when necessary (<lennart@poettering.net>)
- assorted translation updates

* Tue Nov  9 2010 Bill Nottingham <notting@redhat.com> 1.3.49-1
- fix abort on free of uninitialized data. (#649227)

* Wed Oct 27 2010 Bill Nottingham <notting@redhat.com> 1.3.48-1
- fix install_initd invocation for services that require $local_fs (#632294)

* Tue Aug 10 2010 Bill Nottingham <notting@redhat.com> 1.3.47-1
- Fix regression introduced in 1.3.45 (#622799)

* Wed May 05 2010 Bill Nottingham <notting@redhat.com> 1.3.46-1
- translation updates: hu, kn, ko (#589187)

* Thu Mar 04 2010 Bill Nottingham <notting@redhat.com> 1.3.45-1
- add support for Should-Start, Should-Stop (#98470, <iarnell@gmail.com>)
- ntsysv: don't drop initscripts with '.' in the name (#556751)
- translation updates: el, id

* Tue Sep 29 2009 Bill Nottingham <notting@redhat.com> 1.3.44-1
- alternatives: update symlinks if they exist on installation (#104940)
- alternatives: clarify error messages with more context (#441443)
- alternatives: fix removal of manual links (#525021, <dtardon@redhat.com>)
- translation updates: ml, mr, pl, ta, uk

* Mon Sep 14 2009 Bill Nottingham <notting@redhat.com> 1.3.43-1
- ntsysv man page tweak (#516599)
- another minor LSB tweak (#474223)
- translation updates

* Fri Mar  6 2009 Bill Nottingham <notting@redhat.com> 1.3.42-1
- further LSB fixes (#474223)
- throw errors on various malformed init scripts (#481198)
- man page updates re: LSB (#487979)
- translation updates: mai, gu, pt_BR, ro, ca, pa, sr, fr, hu

* Tue Jan 20 2009 Bill Nottingham <notting@redhat.com> 1.3.41-1
- restore return code & error on unconfigured services (#480805)

* Fri Dec  5 2008 Bill Nottingham <notting@redhat.com> 1.3.40-1
- fix some overflows. (#176944)
- add --type parameter to specify either xinetd or sysv services.
  (#467863, <mschmidt@redhat.com>
- do a permissions check before add/remove/on/off/resetpriorities. (#450254)
- parse Short-Description correctly (#441813, <peter_e@gmx.net>)

* Thu Dec  4 2008 Bill Nottingham <notting@redhat.com> 1.3.39-1
- fail if dependencies fail on add/remove in LSB mode (#474223)

* Wed Oct 29 2008 Bill Nottingham <notting@redhat.com> 1.3.38-1
- Fix runlevel list in man page (#466739)
- translation updates

* Thu Nov  8 2007 Bill Nottingham <notting@redhat.com> 1.3.37-1
- make no options do --list (#290241, #176184)
- sr@Latn -> sr@latin

* Tue Sep 25 2007 Bill Nottingham <notting@redhat.com> 1.3.36-1
- buildreq popt-devel, link it dynamically (#279531)
- translation updates: kn, ko, mr, ro

* Fri Aug  3 2007 Bill Nottingham <notting@redhat.com> 1.3.35-1
- clarify licensing

* Mon Apr 16 2007 Bill Nottingham <notting@redhat.com> 1.3.34-1
- translation updates: as, bg, bn_IN, bs, ca, de, fr, hi, hu, id, ja,
  ka, ml, ms, nb, or, sk, sl
- add resetpriorities to the man page (#197399)

* Tue Feb  6 2007 Bill Nottingham <notting@redhat.com> 1.3.33-1
- various changes from review - support alternate %%{_sbindir}, fix
  summaries, add version to requires, assorted other bits

* Fri Feb  2 2007 Bill Nottingham <notting@redhat.com> 1.3.32-1
- support overriding various defaults via /etc/chkconfig.d (<johnsonm@rpath.com>)

* Thu Feb  1 2007 Bill Nottingham <notting@redhat.com> 1.3.31-1
- fix man page (#220558, <esr@thyrus.com>)
- add some more verbiage in alternatives man page (#221089)
- don't print usage message on a nonexstent service (#226804)

* Fri Dec  1 2006 Bill Nottingham <notting@redhat.com> 1.3.30.1-1
- translation updates: as, ka, lv, ml, te (#216617)

* Thu Sep  7 2006 Bill Nottingham <notting@redhat.com> 1.3.30-1
- license cleanup

* Fri Feb 24 2006 Bill Nottingham <notting@redhat.com> 1.3.29-1
- fix accidental enabling of services on --add (#182729)

* Mon Feb 13 2006 Bill Nottingham <notting@redhat.com> 1.3.27-1
- translation updates

* Thu Feb  2 2006 Bill Nottingham <notting@redhat.com> 1.3.26-1
- add support for resetting priorities without on/off status (#178864)

* Wed Nov 30 2005 Bill Nottingham <notting@redhat.com> 1.3.25-1
- return an error if changing services fails (#150235)

* Fri Nov 18 2005 Bill Nottingham <notting@redhat.com> 1.3.24-1
- when removing alternatives links, check to make sure they're
  actually links (#173685)

* Fri Nov 11 2005 Bill Nottingham <notting@redhat.com> 1.3.23-1
- fix ntsysv (#172996)

* Wed Nov  9 2005 Bill Nottingham <notting@redhat.com>
- fix doSetService call in frobOneDependencies

* Tue Nov  8 2005 Bill Nottingham <notting@redhat.com>
- for LSB scripts, use any chkconfig: priorities as a basis,
  instead of 50/50 (#172599)
- fix LSB script dependency setting when no chkconfig: line
  is present (#161870, <jean-francois.larvoire@hp.com>)
- fix LSB script dependency setting when one of Required-Stop
  or Required-Start: is missing (#168457)

* Fri Oct  7 2005 Bill Nottingham <notting@redhat.com>
- fix segfault on directories in /etc/xinetd.d (#166385)
- don't needlessly rewrite xinetd files (#81008)

* Thu May  5 2005 Bill Nottingham <notting@redhat.com> 1.3.20-1
- fix deletion of orphaned slave links (#131496, <mitr@redhat.com>)

* Fri Apr 29 2005 Bill Nottingham <notting@redhat.com> 1.3.19-1
- build with updated translations

* Thu Mar  3 2005 Bill Nottingham <notting@redhat.com> 1.3.18-1
- actually return an error code if changing a service info fails

* Tue Feb 22 2005 Bill Nottingham <notting@redhat.com> 1.3.17-1
- more chkconfig: vs. LSB fixes (#149066)

* Thu Feb 10 2005 Bill Nottingham <notting@redhat.com> 1.3.16-1
- prefer chkconfig: start/stop priorities in LSB mode unless
  Required-Start/Stop are used

* Mon Feb  7 2005 Bill Nottingham <notting@redhat.com> 1.3.15-1
- print usage when various invalid args are passed (#147393)

* Wed Feb  2 2005 Bill Nottingham <notting@redhat.com> 1.3.14-1
- resize reasonably with larger screens (#74156)
- don't error out completely on bad symlink (#74324)
- use ngettext (#106176)
- error out on invalid start/stop values (#109858)
- some man page updates
- fix return code of chkconfig for xinetd services (#63123)
- sort chkconfig --list display (#61576, <shishz@alum.rpi.edu>)

* Tue Jan 11 2005 Bill Nottingham <notting@redhat.com> 1.3.13-1
- fix LSB comment parsing some more (#144739)

* Thu Oct 28 2004 Bill Nottingham <notting@redhat.com> 1.3.11.2-1
- fix manpage reference (#137492)

* Fri Oct  1 2004 Bill Nottingham <notting@redhat.com> 1.3.11.1-1
- rebuild with updated translations

* Fri Jun  4 2004 Bill Nottingham <notting@redhat.com> 1.3.11-1
- fix LSB comment parsing (#85678)

* Wed May 29 2004 Bill Nottingham <notting@redhat.com> 1.3.10-1
- mark alternatives help output for translation (#110526)

* Wed Oct 22 2003 Bill Nottingham <notting@redhat.com> 1.3.9-1
- update translations

* Mon Jul 28 2003 Bill Nottingham <notting@redhat.com> 1.3.8-4
- rebuild

* Tue May 13 2003 Dan Walsh <dwalsh@redhat.com> 1.3.8-3
- Update for RHEL

* Thu May 8 2003 Dan Walsh <dwalsh@redhat.com> 1.3.8-2
- Fix readXinetdServiceInfo to return error on not regular files
- Fix chkconfig to not write messages if readXinetdServiceInfo gets an error

* Fri Jan 31 2003 Bill Nottingham <notting@redhat.com> 1.3.8-1
- fix some wording in alternatives (#76213)
- actually mark alternatives for translation

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 1.3.7-1
- Link to libpopt in a multilib-safe fashion.

* Thu Aug 29 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.6-3
- bump

* Thu Aug 15 2002 Bill Nottingham <notting@redhat.com> 1.3.6-2
- rebuild against new newt

* Mon Aug 12 2002 Bill Nottingham <notting@redhat.com> 1.3.6-1
- make on and off handle runlevel 2 too (#70766)

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.5-3
- Update translations

* Mon Apr 15 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.3.5-2
- Update translations

* Sun Apr  7 2002 Jeremy Katz <katzj@redhat.com> 1.3.5-1
- alternatives: handle default with --config properly (#62009)

* Thu Mar 14 2002 Bill Nottingham <notting@redhat.com> 1.3.4-1
- don't apply the dependency logic to things that already have
  start/stop priorities
- fix silly display bug in --config

* Tue Mar 12 2002 Bill Nottingham <notting@redhat.com> 1.3.2-1
- chkconfig: LSB support

* Fri Mar  8 2002 Bill Nottingham <notting@redhat.com>
- alternatives: handle initscripts too; --initscript command-line option
- chkconfig/ntsysv (and serviceconf, indirectly): services with
   *no* links in /etc/rc*.d are no longer displayed with --list, or
   available for configuration except via chkconfig command-line options
- alternatives: fix trying to enable disable a null service

* Tue Mar  5 2002 Bill Nottingham <notting@redhat.com>
- alternatives: handle things with different numbers of slave links

* Mon Mar  4 2002 Bill Nottingham <notting@redhat.com>
- minor alternatives tweaks: don't install the same thing multiple times

* Wed Jan 30 2002 Bill Nottingham <notting@redhat.com>
- actually, put the alternatives stuff back in /usr/sbin
- ship /etc/alternatives dir
- random alternatives fixes

* Sun Jan 27 2002 Erik Troan <ewt@redhat.com>
- reimplemented update-alternatives as just alternatives

* Thu Jan 25 2002 Bill Nottingham <notting@redhat.com>
- add in update-alternatives stuff (perl ATM)

* Mon Aug 27 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Update translations

* Tue Jun 12 2001 Bill Nottingham <notting@redhat.com>
- don't segfault on files that are exactly the length of a page size
  (#44199, <kmori@redhat.com>)

* Sun Mar  4 2001 Bill Nottingham <notting@redhat.com>
- don't show xinetd services in ntsysv if xinetd doesn't appear to be
  installed (#30565)

* Wed Feb 14 2001 Preston Brown <pbrown@redhat.com>
- final translation update.

* Tue Feb 13 2001 Preston Brown <pbrown@redhat.com>
- warn in ntsysv if not running as root.

* Fri Feb  2 2001 Preston Brown <pbrown@redhat.com>
- use lang finder script

* Fri Feb  2 2001 Bill Nottingham <notting@redhat.com>
- finally fix the bug Nalin keeps complaining about :)

* Wed Jan 24 2001 Preston Brown <pbrown@redhat.com>
- final i18n update before Beta.

* Wed Oct 18 2000 Bill Nottingham <notting@redhat.com>
- ignore .rpmnew files (#18915)
- fix typo in error message (#17575)

* Wed Aug 30 2000 Nalin Dahyabhai <nalin@redhat.com>
- make xinetd config files mode 0644, not 644

* Thu Aug 24 2000 Erik Troan <ewt@redhat.com>
- updated it and es translations

* Sun Aug 20 2000 Bill Nottingham <notting@redhat.com>
- get man pages in proper packages

* Sun Aug 20 2000 Matt Wilson <msw@redhat.com>
- new translations

* Tue Aug 16 2000 Nalin Dahyabhai <nalin@redhat.com>
- don't worry about extra whitespace on chkconfig: lines (#16150)

* Wed Aug 10 2000 Trond Eivind Glomsrød <teg@redhat.com>
- i18n merge

* Wed Jul 26 2000 Matt Wilson <msw@redhat.com>
- new translations for de fr it es

* Tue Jul 25 2000 Bill Nottingham <notting@redhat.com>
- change prereqs

* Sun Jul 23 2000 Bill Nottingham <notting@redhat.com>
- fix ntsysv's handling of xinetd/init files with the same name

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- fix segv when reading malformed files

* Wed Jul 19 2000 Bill Nottingham <notting@redhat.com>
- put links, rc[0-6].d dirs back, those are necessary

* Tue Jul 18 2000 Bill Nottingham <notting@redhat.com>
- add quick hack support for reading descriptions from xinetd files

* Mon Jul 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- don't own the /etc/rc[0-6].d symlinks; they're owned by initscripts

* Sat Jul 15 2000 Matt Wilson <msw@redhat.com>
- move back to old file layout

* Thu Jul 13 2000 Preston Brown <pbrown@redhat.com>
- bump copyright date

* Tue Jul 11 2000 Bill Nottingham <notting@redhat.com>
- no %%pre today. Maybe tomorrow.

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- put initscripts %%pre here too

* Mon Jul  3 2000 Bill Nottingham <notting@redhat.com>
- oops, if we don't prereq initscripts, we *need* to own /etc/rc[0-6].d

* Sun Jul  2 2000 Bill Nottingham <notting@redhat.com>
- add xinetd support

* Tue Jun 27 2000 Matt Wilson <msw@redhat.com>
- changed Prereq: initscripts >= 5.18 to Conflicts: initscripts < 5.18
- fixed sumary and description where a global string replace nuked them

* Mon Jun 26 2000 Matt Wilson <msw@redhat.com>
- what Bill said, but actually build this version

* Thu Jun 15 2000 Bill Nottingham <notting@redhat.com>
- don't own /etc/rc.*

* Fri Feb 11 2000 Bill Nottingham <notting@redhat.com>
- typo in man page

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description

* Wed Jan 12 2000 Bill Nottingham <notting@redhat.com>
- link chkconfig statically against popt

* Mon Oct 18 1999 Bill Nottingham <notting@redhat.com>
- fix querying alternate levels

* Mon Aug 23 1999 Jeff Johnson <jbj@redhat.com>
- don't use strchr to skip unwanted files, look at extension instead (#4166).

* Thu Aug  5 1999 Bill Nottingham <notting@redhat.com>
- fix --help, --verson

* Mon Aug  2 1999 Matt Wilson <msw@redhat.com>
- rebuilt ntsysv against newt 0.50

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- fix i18n problem in usage message (#4233).
- add --help and --version.

* Mon Apr 19 1999 Cristian Gafton <gafton@redhat.com>
- release for Red Hat 6.0

* Thu Apr  8 1999 Matt Wilson <msw@redhat.com>
- added support for a "hide: true" tag in initscripts that will make
  services not appear in ntsysv when run with the "--hide" flag

* Thu Apr  1 1999 Matt Wilson <msw@redhat.com>
- added --hide flag for ntsysv that allows you to hide a service from the
  user.

* Mon Mar 22 1999 Bill Nottingham <notting@redhat.com>
- fix glob, once and for all. Really. We mean it.

* Thu Mar 18 1999 Bill Nottingham <notting@redhat.com>
- revert fix for services@levels, it's broken
- change default to only edit the current runlevel

* Mon Mar 15 1999 Bill Nottingham <notting@redhat.com>
- don't remove scripts that don't support chkconfig

* Tue Mar 09 1999 Erik Troan <ewt@redhat.com>
- made glob a bit more specific so xinetd and inetd don't cause improper matches

* Thu Feb 18 1999 Matt Wilson <msw@redhat.com>
- removed debugging output when starting ntsysv

* Thu Feb 18 1999 Preston Brown <pbrown@redhat.com>
- fixed globbing error
- fixed ntsysv running services not at their specified levels.

* Tue Feb 16 1999 Matt Wilson <msw@redhat.com>
- print the value of errno on glob failures.

* Sun Jan 10 1999 Matt Wilson <msw@redhat.com>
- rebuilt for newt 0.40 (ntsysv)

* Tue Dec 15 1998 Jeff Johnson <jbj@redhat.com>
- add ru.po.

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide (slang-1.2.2)

* Wed Oct 14 1998 Cristian Gafton <gafton@redhat.com>
- translation updates

* Thu Oct 08 1998 Cristian Gafton <gafton@redhat.com>
- updated czech translation (and use cs instead of cz)

* Tue Sep 22 1998 Arnaldo Carvalho de Melo <acme@conectiva.com.br>
- added pt_BR translations
- added more translatable strings
- support for i18n init.d scripts description

* Sun Aug 02 1998 Erik Troan <ewt@redhat.com>
- built against newt 0.30
- split ntsysv into a separate package

* Thu May 07 1998 Erik Troan <ewt@redhat.com>
- added numerous translations

* Mon Mar 23 1998 Erik Troan <ewt@redhat.com>
- added i18n support

* Sun Mar 22 1998 Erik Troan <ewt@redhat.com>
- added --back
