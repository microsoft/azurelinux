Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%global _use_internal_dependency_generator 0

%global contentdir       %{_localstatedir}/www/%{name}
%global libdir           %{_localstatedir}/lib/mrtg

Summary:   Multi Router Traffic Grapher
Name:      mrtg
Version:   2.17.7
Release:   6%{?dist}
URL:       https://oss.oetiker.ch/mrtg/
Source0:   https://oss.oetiker.ch/mrtg/pub/mrtg-%{version}.tar.gz
Source1:   https://oss.oetiker.ch/mrtg/pub/mrtg-%{version}.tar.gz.md5
# Source2: configuration file example
Source2:   mrtg.cfg
# Source3: script for filtering out false perl requires
Source3:   filter-requires-mrtg.sh
# Source4: configuration for Apache
Source5:   mrtg-httpd.conf
# Source6: script for filtering out false perl provides
Source6:   filter-provides-mrtg.sh
# Source7: tmpfiles rule
Source7:   mrtg.tmpfiles
# Source8: systemd service file
Source8:   mrtg.service
# Source9: systemd timer file
Source9:   mrtg.timer
Patch0:    mrtg-2.15.0-lib64.patch
Patch1:    mrtg-2.17.2-socket6-fix.patch
# Patch2: some devices return 2**32-2 on ifSpeed (e. g. IBM FibreChannel switches)
Patch2:    mrtg-2.17.4-cfgmaker-ifhighspeed.patch
# Patch3: fixes 'man' option in mrtg-traffic-sum, see rhbz#1612188
Patch3:    mrtg-2.17.7-traffic-sum-man-option.patch
License:   GPLv2+
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units
Requires:  perl-Socket6 perl-IO-Socket-INET6
Requires:  gd
BuildRequires: gd-devel, libpng-devel
BuildRequires: perl-generators
BuildRequires: systemd-units
BuildRequires: gcc

%global __find_requires %{SOURCE3}
%global __find_provides %{SOURCE6}

%description
The Multi Router Traffic Grapher (MRTG) is a tool to monitor the traffic
load on network-links. MRTG generates HTML pages containing PNG
images which provide a LIVE visual representation of this traffic.

%prep
%setup -q
%patch 0 -p1 -b .lib64
%patch 1 -p1 -b .socket6
%patch 2 -p1 -b .ifhighspeed
%patch 3 -p1 -b .traffic-sum-man-option

for i in doc/mrtg-forum.1 doc/mrtg-squid.1 CHANGES; do
    iconv -f iso-8859-1 -t utf-8 < "$i" > "${i}_"
    mv "${i}_" "$i"
done

# Remove contribution useful on Windows only
rm -rf contrib/nt-services

%build
%configure
# Don't link rateup statically, don't link to indirect dependencies
# LIBS derived from autodetected by removing -Wl,-B(static|dynamic), -lpng, -lz
make LIBS='-lgd -lm'
find contrib -type f -exec \
    %{__perl} -e 's,^#!/\s*\S*perl\S*,#!%{__perl},gi' -p -i \{\} \;
find contrib -name "*.pl" -exec %{__perl} -e 's;\015;;gi' -p -i \{\} \;
find contrib -type f | xargs chmod a-x

%install
rm -rf   $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/mrtg
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/mrtg
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lock/mrtg
mkdir -p $RPM_BUILD_ROOT%{contentdir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d

install -m 644 images/*   $RPM_BUILD_ROOT%{contentdir}/
sed 's,@CONTENTDIR@,%{contentdir},g; s,@LIBDIR@,%{_localstatedir}/lib/mrtg,g' \
    %{SOURCE2} > $RPM_BUILD_ROOT%{_sysconfdir}/mrtg/mrtg.cfg
chmod 644 $RPM_BUILD_ROOT%{_sysconfdir}/mrtg/mrtg.cfg

install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d/mrtg.conf

mkdir -p $RPM_BUILD_ROOT/%{_tmpfilesdir}
install -p -D -m 644 %{SOURCE7} $RPM_BUILD_ROOT/%{_tmpfilesdir}/mrtg.conf

# install systemd files
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 %{SOURCE8} $RPM_BUILD_ROOT%{_unitdir}/mrtg.service
install -p -m 644 %{SOURCE9} $RPM_BUILD_ROOT%{_unitdir}/mrtg.timer

# Add mrtg-traffic-sum here when upstream decides to install it
for i in mrtg cfgmaker indexmaker mrtg-traffic-sum; do
    sed -i 's;@@lib@@;%{_lib};g' "$RPM_BUILD_ROOT"%{_bindir}/"$i"
done

sed -i 's;@@lib@@;%{_lib};g' "$RPM_BUILD_ROOT"%{_mandir}/man1/*.1

%post
install -d -m 0755 -o root -g root /var/lock/mrtg
restorecon /var/lock/mrtg
%systemd_post mrtg.service

%preun
if [ $1 -eq 0 ]; then
  # Package removal, not upgrade
  rm -rf /var/lock/mrtg
fi
%systemd_preun mrtg.service

%postun
%systemd_postun_with_restart mrtg.service 

%files
%license COPYING
%doc contrib CHANGES COPYRIGHT README THANKS
%dir %{_sysconfdir}/mrtg
%config(noreplace) %{_sysconfdir}/mrtg/mrtg.cfg
%config(noreplace) %{_sysconfdir}/httpd/conf.d/mrtg.conf
%{contentdir}
%{_bindir}/*
%{_libdir}/mrtg2
%exclude %{_libdir}/mrtg2/Pod
%{_mandir}/*/*
%exclude %{_datadir}/mrtg2/icons
%exclude %{_datadir}/doc/mrtg2
%dir %{_localstatedir}/lib/mrtg
%{_tmpfilesdir}/mrtg.conf
%ghost /var/lock/mrtg
%{_unitdir}/mrtg.service
%{_unitdir}/mrtg.timer

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.17.7-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 18 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.7-2
- Fix mrtg-traffic-sum incorrectly ignores 'man' option
  Resolves: #1612188

* Thu Aug 09 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.7-1
- Use %%license
- Update to mrtg-2.17.7
  Resolves: #1600933

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.4-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 22 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-23
- Add BuildRequires gcc
- Remove Group tag

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.4-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.17.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 07 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-17
- Fix cfgmaker uninitialized value errors
  Resolves: #1260062

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jan 19 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-15
- Fix packaging of tmpfiles
- Fix bogus dates in the changelog

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jan 21 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-12
- Fix wrong SELinux context of /var/lock/mrtg

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.17.4-10
- Perl 5.18 rebuild

* Tue Jun 11 2013 Remi Collet <rcollet@redhat.com> - 2.17.4-9
- rebuild for new GD 2.1.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-7
- Apply patch #3

* Thu Nov 29 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-6
- Comment sources

* Wed Oct 31 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-5
- Update mrtg-httpd.conf to work with httpd 2.4
  Resolves: #871434

* Wed Aug 22 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-4
- Use new systemd-rpm macros
  Resolves: #850215

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 28 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-2
- Fix cfgmaker don't use ifHighSpeed on IBM FibreChannel switches
  (patch by Peter Bieringer)

* Thu Mar 01 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.4-1
- Update to mrtg-2.17.4
- Use unitdir macro when creating directory for systemd units

* Mon Jan 09 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.3-2
- Fix 'undefined subroutine &SNMP_Session::inet_ntop called at
  /usr/bin/../lib64/mrtg2/SNMP_Session.pm line 549.' error

* Wed Dec 07 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.3-1
- Update to mrtg-2.17.3

* Mon Oct 31 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.2-6
- Remove contribution useful on Windows only from documentation
  Resolves: #749426

* Sun Oct  2 2011 Tom Callaway <spot@fedoraproject.org> - 2.17.2-5
- Resolve bugzilla 732587

* Thu Sep  8 2011 Tom Callaway <spot@fedoraproject.org> - 2.17.2-4
- add missing systemd scriptlets
- drop cron.d config (systemd handles it now)

* Wed Aug 24 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.2-3
- Ship systemd files
  Resolves: #696147

* Thu Mar 24 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.2-2
- Use %%ghost for /var/lock/mrtg
  Resolves: #656629

* Tue Feb 22 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.2-1
- Update to mrtg-2.17.2

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.17.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec 15 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.17.0-1
- Update to mrtg-2.17.0

* Mon Dec 13 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.4-4
- Resurrect part of the previous patch lost by mistake

* Mon Dec 13 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.4-3
- Import also getaddrinfo in SNMP_Session.pm
  Resolves: #662116

* Mon Nov 22 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 2.16.4-2
- resolve conflict with Socket6 (see bz 438931, 442884, 652158)

* Mon Sep 27 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.4-1
- Update to mrtg-2.16.4

* Wed Apr  7 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.3-1
- Update to mrtg-2.16.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.16.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.2-2
- Merge Review and spec cleanup
  Resolves: #226161

* Fri Jun 27 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.2-1
- Update to 2.16.2
- Mark /etc/crond.d/mrtg file as "noreplace" to keep current setup
  during mrtg update
  Related: #391261
- Fix mrtg complains of undefined subroutine AF_UNSPEC
  Resolves: #451783

* Fri Jun  6 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.1-3
- Add gd graphic library to Requires
  Resolves: #446533

* Tue Apr 22 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.16.1-2
- Rebuild
  Resolves: #443116

* Fri Apr 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.16.1-1
- Update to 2.16.1
- fix perl noise (bz 438931, 442884)

* Mon Feb 11 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.15.1-8
- Fix Buildroot

* Fri Jan 18 2008 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.15.1-7
- Rebuild

* Mon Oct 15 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.15.1-6
- Fix another two bad perl provides

* Thu Sep 20 2007 Vitezslav Crhonek <vcrhonek@redhat.com> 2.15.1-5
- Fix bad provides

* Thu Aug 23 2007 Vitezslav Crhonek <vcrhonek@redhat.com> 2.15.1-4
- fix license
- rebuild

* Fri Jun  8 2007 Vitezslav Crhonek <vcrhonek@redhat.com> 2.15.1-3
- Rebuild

* Thu Jun  7 2007 Vitezslav Crhonek <vcrhonek@redhat.com> - 2.15.1-2
- Specfile update, because upstream decides to install mrtg-traffic-sum
  Resolves: #243112

* Mon Feb 12 2007 Miloslav Trmac <mitr@redhat.com> - 2.15.1-1
- Update to mrtg-2.15.1

* Wed Dec  6 2006 Miloslav Trmac <mitr@redhat.com> - 2.15.0-1
- Update to mrtg-2.15.0
- Don't use Prereq: for /sbin/service
- Use (sed -i) instead of perl to make the regexps more readable

* Tue Oct 24 2006 Miloslav Trmac <mitr@redhat.com> - 2.14.7-1
- Update to mrtg-2.14.7

* Wed Aug 30 2006 Miloslav Trmac <mitr@redhat.com> - 2.14.5-2
- Add Requires: perl-Socket6 perl-IO-Socket-INET6 for IPv6 support

* Sun Jul 16 2006 Miloslav Trmac <mitr@redhat.com> - 2.14.5-1
- Update to mrtg-2.14.5

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.14.4-1.1
- rebuild

* Wed Jul  5 2006 Miloslav Trmac <mitr@redhat.com> - 2.14.4-1
- Update to mrtg-2.14.4

* Mon May 15 2006 Miloslav Trmac <mitr@redhat.com> - 2.14.3-1
- Update to mrtg-2.14.3

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 2.13.2-1
- Update to mrtg-2.13.2

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.13.0-1.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.13.0-1.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Mon Jan 30 2006 Miloslav Trmac <mitr@redhat.com> - 2.13.0-1
- Update to mrtg-2.13.0

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Sep 12 2005 Miloslav Trmac <mitr@redhat.com> - 2.12.2-2
- Add LANG and LC_ALL definition to cron script for easier copying to command
  line (#167530)
- Don't ship MANIFEST and a very obsolete version of 14all.cgi
- Fix rewriting of perl paths to /usr/bin/perl in contrib scripts
- Make contrib scripts unexecutable to avoid unnecessary rpm dependencies;
  remove unnecessary entries from filter-requires-mrtg.sh

* Mon Jun 20 2005 Miloslav Trmac <mitr@redhat.com> - 2.12.2-1
- Update to mrtg-2.12.2

* Wed May 25 2005 Miloslav Trmac <mitr@redhat.com> - 2.12.1-2
- Remove included old version of PodParser (#158735)

* Tue May 17 2005 Miloslav Trmac <mitr@redhat.com> - 2.12.1-1
- Update to mrtg-2.12.1
- Remove unnecessary BuildRequires, Requires
- Don't link rateup to libpng and libz

* Sun Mar 13 2005 Miloslav Trmac <mitr@redhat.com> - 2.11.1-3
- Fix Timezone[] handling in html output (#149296)

* Fri Mar  4 2005 Miloslav Trmac <mitr@redhat.com> - 2.11.1-2
- Rebuild with gcc 4

* Thu Jan  6 2005 Miloslav Trmac <mitr@redhat.com> - 2.11.1-1
- Update to mrtg-2.11.1

* Mon Dec 13 2004 Miloslav Trmac <mitr@redhat.com> - 2.11.0-1
- Update to mrtg-2.11.0
- Don't install HTML documentation to /var/www/mrtg
- Clean up %%install a bit

* Tue Nov 23 2004 Miloslav Trmac <mitr@redhat.com> - 2.10.15-3
- Convert man pages to UTF-8

* Mon Nov 22 2004 Jindrich Novy <jnovy@redhat.com> 2.10.15-2
- remove bogus characters from man pages to prevent
  man displaying the page is in wrong encoding (#139341)

* Tue Aug 17 2004 Miloslav Trmac <mitr@redhat.com> - 2.10.15-1
- Update to 2.10.15
- Use a more generic URL
- Don't link rateup statically
- Move threshold and log files to /var/lib/mrtg, lock files to /var/lock/mrtg

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Apr 20 2004 Joe Orton <jorton@redhat.com> 2.10.5-3
- Allow/Deny by address in conf.d/mrtg.conf (#113089)

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Oct 25 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 2.10.5
- to not set LD_RUN_PATH

* Sat Aug  2 2003 Joe Orton <jorton@redhat.com> 2.9.29-5
- rebuild

* Fri Aug  1 2003 Joe Orton <jorton@redhat.com> 2.9.29-4.ent
- move default output directory to /var/www/mrtg

* Mon Jun  9 2003 Nalin Dahyabhai <nalin@redhat.com> 2.9.28-4
- disable use of RPM's internal dependency generator so that we can filter out
  requirements of the contrib scripts included in the docs directory

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun  3 2003 Jeff Johnson <jbj@redhat.com>
- add explicit epoch's where needed.

* Tue May  6 2003 Nalin Dahyabhai <nalin@redhat.com> 2.9.28-2
- rebuild

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com> 2.9.28-1
- update to 2.9.29

* Wed Mar  5 2003 Nalin Dahyabhai <nalin@redhat.com> 2.9.17-14
- fixup lib/lib64 references (#82916)

* Fri Feb  7 2003 Nalin Dahyabhai <nalin@redhat.com> 2.9.17-13
- move crontab data to /etc/cron.d
- add trigger to remove crontab data from /etc/crontab on removal of
  older versions

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Tue Dec 17 2002 Tim Powers <timp@redhat.com> 2.9.17-11
- PreReq crontabs

* Sat Dec 14 2002 Tim Powers <timp@redhat.com> 2.9.17-10
- don't use rpms internal dep generator

* Thu Dec 12 2002 Tim Powers <timp@redhat.com> 2.9.17-9
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed May 29 2002 Chip Turner <cturner@redhat.com>
- added filter for soft perl dependencies

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 2.9.17-4
- rebuild in new environment

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 2.9.17-3
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Nov  1 2001 Nalin Dahyabhai <nalin@redhat.com> 2.9.17-1
- update to 2.9.17
- use FHS macros
- install the .gif files as well
- copyright: distributable -> license: GPL

* Tue Jul  3 2001 Tim Powers <timp@redhat.com>
- changed description to indicate that it creates PNG images and not GIF images

* Mon Jun 25 2001 Nalin Dahyabhai <nalin@redhat.com>
- set LIBS=-lfreetype and LDFLAGS="-lgd -lpng -lfreetype -lm" to link the gd
  support with freetype, which it needs
- remove Packager: tag (was Packager: Tim Verhoeven <dj@sin.khk.be>)

* Mon May 21 2001 Tim Powers <timp@redhat.com>
- rebuilt for the distro

* Mon Mar  5 2001 Tim Powers <timp@redhat.com>
- fixed bad group

* Thu Dec 14 2000 Tim Powers <timp@redhat.com>
- updated to 2.9.6

* Tue Dec 12 2000 Tim Powers <timp@redhat.com>
- updated to 2.9.5

* Mon Nov 20 2000 Tim Powers <timp@redhat.com>
- rebuilt to fix bad dir perms

* Mon Nov 13 2000 Tim Powers <timp@redhat.com>
- using this new spec for 7.1 build

* Fri Oct 27 2000  Henri Gomez <hgomez@slib.fr>
 [2.9.4]
- compiled on Redhat 6.1 box plus updates with rpm-3.0.5

* Thu Oct 26 2000  Henri Gomez <hgomez@slib.fr>
 [2.9.2]
- clean up spec file for 2.9 release
  (no .gif, cfgmaker_ip removed)
- mrtg 2.9 look for .pm in /usr/lib/mrtg2, so no more need
  to relocate .pm at post time.
- mrtg config (mrtg.cfg) goes now in /etc/mrtg/
- added manual to rpm
- spec file adapted to RH 7.0

* Wed Feb 9 2000 Tim Verhoeven <dj@sin.khk.be>
 [2.8.12]
- source archiv changed back to .gz
- upgraded to mrtg version 2.8.12

* Sat Nov 13 1999 Peter Hanecak <hanecak@megaloman.sk>
 [2.8.9]
- source archiv changed to .bz2

* Fri Aug 27 1999 Henri Gomez <gomez@slib.fr>
 [2.8.8]
- important release since rrd support is added
  It came from Rainer Bawidamann work. If you have rrdtool RPM
  installed, just add UseRRDTool: Yes in your config files.
- added latest patch for mrtg-rrd.
- to convert your mrtg logs to rrd format, use log2rrd.pl
  you can found on rrdtool package.

* Mon Aug 16 1999 Henri Gomez <gomez@slib.fr>
 [2.8.6]

* Fri Jul 23 1999 Henri Gomez <gomez@slib.fr>
 [2.8.4]
- mrtg could use now png instead of gif via gd1.6.1
  but since gd1.6.1 remove all gif reference it could
  break your dependencies, so we don't use it for now.
* Tue Jun 15 1999 Henri Gomez <gomez@slib.fr>
 [2.7.5]
- removed gd-devel requires, RH5.x use libgd-devel and RH6 gd-devel.
- removed CR from perl files in contrib.
- added cfgmaker_ip in binaries.
- rework modules install/de-install for RH5.x/6.0 compat

* Wed Jun  9 1999 Henri Gomez <gomez@slib.fr>
 [2.7.4-2]
- set perl path for contribs
- set SNMP's perl to /usr/lib/perl5/site_perl (clean for RH5.x and RH6.0)

* Wed May  5 1999 Ian Macdonald <ianmacd@xs4all.nl>
  [2.7.4-1]
- changed Perl module installation to be version independent
- changed libgd dependency to gd
- changed URL
- strip binaries
- include contrib directory as documentation

* Tue Mar  2 1999 Henri Gomez <gomez@slib.fr>
  [2.6.6]

* Wed Feb 17 1999 Henri Gomez <gomez@slib.fr>
  [2.6.4]
- removed mrtg-squid (specific OIDS)
- cfgmaker and indexmaker now /usr/bin
- libgd must be >= 1.3

* Fri Jan 29 1999 Henri Gomez <gomez@slib.fr>
  [2.5.4c-3]
- Added mrtg-squid to monitor squid (specific OIDS)

* Thu Jan 28 1999 Henri Gomez <gomez@slib.fr>
  [2.5.4c-2]
- applied squid snmp patch

* Wed Jan 27 1999 Henri Gomez <gomez@slib.fr>
  [2.5.4c-1]
- upgraded to 2.5.4c.
- added require libgd-devel

* Mon Nov 30 1998 Arne Coucheron <arneco@online.no>
  [2.5.4a-1]

* Thu Jun 18 1998 Arne Coucheron <arneco@online.no>
  [2.5.3-1]
- using %%{name} and %%{version} macros
- using %%defattr macro in filelist
- using install -d in various places instead of cp
- added -q parameter to %%setup
- removed older changelogs
