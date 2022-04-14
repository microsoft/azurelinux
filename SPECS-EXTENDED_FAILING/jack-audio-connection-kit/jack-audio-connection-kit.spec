Vendor:         Microsoft Corporation
Distribution:   Mariner
# set bootstrap to 1 in order to break the initial libffado loop
#
# libffado -> PyQt4 -> phonon -> phonon-backend-gstreamer ->
# -> gstreamer-plugins-good -> jack-audio-connection-kit -> libffado
#
%global bootstrap 1

%global groupname jackuser
%global pagroup   pulse-rt

Summary:       The Jack Audio Connection Kit
Name:          jack-audio-connection-kit
Version:       1.9.14
Release:       4%{?dist}
# The entire source (~500 files) is a mixture of these three licenses
License:       GPLv2 and GPLv2+ and LGPLv2+
URL:           http://www.jackaudio.org
Source0:       https://github.com/jackaudio/jack2/releases/download/v%{version}/v%{version}.tar.gz#/jack2-%{version}.tar.gz
Source1:       %{name}-README.Fedora
Source2:       %{name}-script.pa
Source3:       %{name}-limits.conf
# Generate this file in the GIT repo by running ./svnversion_regenerate.sh svnversion.h
Source4:       svnversion.h
Source5:       %{name}-LICENSE.txt
# Patch doxygen documentation
Patch0:        %{name}-doxygen.patch
# Adjust default priority. RHBZ#795094
Patch1:        jack-realtime-compat.patch

BuildRequires: alsa-lib-devel
BuildRequires: dbus-devel
BuildRequires: doxygen
BuildRequires: expat-devel
BuildRequires: gcc-c++
%ifnarch s390 s390x
%if !0%{?bootstrap} && !0%{?flatpak}
BuildRequires: libffado-devel
%endif
%endif
BuildRequires: libsamplerate-devel
BuildRequires: libsndfile-devel
BuildRequires: ncurses-devel
BuildRequires: opus-devel
BuildRequires: pkgconfig
BuildRequires: python3
BuildRequires: readline-devel

Requires(pre): shadow-utils
Requires:      pam

%description
JACK is a low-latency audio server, written primarily for the Linux operating
system. It can connect a number of different applications to an audio device, as
well as allowing them to share audio between themselves. Its clients can run in
their own processes (i.e. as a normal application), or can they can run within a
JACK server (i.e. a "plugin").

JACK is different from other audio server efforts in that it has been designed
from the ground up to be suitable for professional audio work. This means that
it focuses on two key areas: synchronous execution of all clients, and low
latency operation.

%package dbus
Summary:       Jack D-Bus launcher
Requires:      %{name} = %{version}-%{release}

%description dbus
Launcher to start Jack through D-Bus.


%package devel
Summary:       Header files for Jack
Requires:      %{name} = %{version}-%{release}

%description devel
Header files for the Jack Audio Connection Kit.

%package example-clients
Summary:       Example clients that use Jack 
Requires:      %{name} = %{version}-%{release}

%description example-clients
Small example clients that use the Jack Audio Connection Kit.

%prep
%autosetup -p1 -n jack2-%{version}

%build
cp -p %{SOURCE4} .
cp %{SOURCE5} ./LICENSE.txt
%set_build_flags
export PREFIX=%{_prefix}
python3 ./waf configure \
   --mandir=%{_mandir}/man1 \
   --libdir=%{_libdir} \
   --doxygen \
   --dbus \
   --classic \
%ifnarch s390 s390x
%if !0%{?bootstrap} && !0%{?flatpak}
   --firewire \
%endif
%endif
   --alsa \
   --clients 256 \
   --ports-per-application=2048

python3 ./waf build %{?_smp_mflags} -v

%install
python3 ./waf --destdir=%{buildroot} install

# move doxygen documentation to the right place
mv %{buildroot}%{_datadir}/jack-audio-connection-kit/reference .
rm -rf %{buildroot}%{_datadir}/jack-audio-connection-kit

# install our limits to the /etc/security/limits.d
mkdir -p %{buildroot}%{_sysconfdir}/security/limits.d
sed -e 's,@groupname@,%groupname,g; s,@pagroup@,%pagroup,g;' \
    %{SOURCE3} > %{buildroot}%{_sysconfdir}/security/limits.d/95-jack.conf

# prepare README.Fedora for documentation including
install -p -m644 %{SOURCE1} README.Fedora

# install pulseaudio script for jack (as documentation part)
install -p -m644 %{SOURCE2} jack.pa

# For compatibility with jack1
mv %{buildroot}%{_bindir}/jack_rec %{buildroot}%{_bindir}/jackrec

# Fix permissions of the modules
chmod 755 %{buildroot}%{_libdir}/jack/*.so %{buildroot}%{_libdir}/libjack*.so.*.*.*

%pre
getent group %groupname > /dev/null || groupadd -r %groupname
exit 0

%files
%license LICENSE.txt
%doc ChangeLog.rst README.rst README_NETJACK2
%doc README.Fedora
%doc jack.pa
%{_bindir}/jackd
%{_bindir}/jackrec
%{_libdir}/jack/
%{_libdir}/libjack.so.*
%{_libdir}/libjacknet.so.*
%{_libdir}/libjackserver.so.*
%config(noreplace) %{_sysconfdir}/security/limits.d/*.conf

%{_mandir}/man1/jackrec.1*
%{_mandir}/man1/jackd*.1*

%files dbus
%{_bindir}/jackdbus
%{_datadir}/dbus-1/services/org.jackaudio.service
%{_bindir}/jack_control

%files devel
%doc reference/html/
%{_includedir}/jack/
%{_libdir}/libjack.so
%{_libdir}/libjacknet.so
%{_libdir}/libjackserver.so
%{_libdir}/pkgconfig/jack.pc

%files example-clients
%{_bindir}/alsa_in
%{_bindir}/alsa_out
%{_bindir}/jack_alias
%{_bindir}/jack_bufsize
%{_bindir}/jack_connect
%{_bindir}/jack_disconnect
%{_bindir}/jack_cpu_load
%{_bindir}/jack_evmon
%{_bindir}/jack_freewheel
# These are not ready yet
#{_bindir}/jack_impulse_grabber
%exclude %{_mandir}/man1/jack_impulse_grabber.1*
%{_bindir}/jack_latent_client
%{_bindir}/jack_load
%{_bindir}/jack_unload
%{_bindir}/jack_lsp
%{_bindir}/jack_metro
%{_bindir}/jack_midi_dump
%{_bindir}/jack_midi_latency_test
%{_bindir}/jack_midiseq
%{_bindir}/jack_midisine
%{_bindir}/jack_monitor_client
%{_bindir}/jack_net_master
%{_bindir}/jack_net_slave
%{_bindir}/jack_netsource
%{_bindir}/jack_property
%{_bindir}/jack_samplerate
%{_bindir}/jack_server_control
%{_bindir}/jack_session_notify
%{_bindir}/jack_showtime
%{_bindir}/jack_simple_client
%{_bindir}/jack_simple_session_client
%{_bindir}/jack_thru
%{_bindir}/jack_transport
%{_bindir}/jack_wait
%{_bindir}/jack_zombie

%{_mandir}/man1/alsa_*.1*
%{_mandir}/man1/jack_bufsize.1*
%{_mandir}/man1/jack_connect.1*
%{_mandir}/man1/jack_disconnect.1*
%{_mandir}/man1/jack_freewheel*.1*
%{_mandir}/man1/jack_load*.1*
%{_mandir}/man1/jack_unload*.1*
%{_mandir}/man1/jack_lsp.1*
%{_mandir}/man1/jack_metro.1*
%{_mandir}/man1/jack_monitor_client.1*
%{_mandir}/man1/jack_netsource.1*
%{_mandir}/man1/jack_property.1*
%{_mandir}/man1/jack_samplerate.1*
%{_mandir}/man1/jack_showtime.1*
%{_mandir}/man1/jack_simple_client.1*
%{_mandir}/man1/jack_transport.1*
%{_mandir}/man1/jack_wait.1*

# tests
%{_bindir}/jack_cpu
%{_bindir}/jack_iodelay
%{_bindir}/jack_multiple_metro
%{_bindir}/jack_simdtests
%{_bindir}/jack_test

%{_mandir}/man1/jack_iodelay.1*


%changelog
* Fri Dec 10 2021 Thomas Crain <thcrain@microsoft.com> - 1.9.14-4
- License verified

* Wed Mar 24 2021 Henry Li <lihl@microsoft.com> - 1.9.14-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Set bootstrap to 1 to disable circular dependency

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Dec 06 2019 Guido Aulisi <guido.aulisi@gmail.com> - 1.9.14-1
- Update to 1.9.14

* Tue Oct 29 2019 Jan Beran <jaberan@redhat.com> - 1.9.13-3
- Do not use libffado if building flatpak

* Thu Oct 10 2019 Guido Aulisi <guido.aulisi@gmail.com> - 1.9.13-2
- Fix compilation on arm

* Mon Oct 07 2019 Guido Aulisi <guido.aulisi@gmail.com> - 1.9.13-1
- Update to 1.9.13
- Drop python2
- Some spec cleanup

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.12-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 17 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.12-8
- Rebuild for readline 8.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.12-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 05 2018 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.12-5
- Fix unversioned Python shebangs

* Sat Feb 10 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.9.12-4
- Switch to %%ldconfig_scriptlets

* Fri Feb 09 2018 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.12-3
- Build with RPM_LD_FLAGS exported

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 26 2017 Nils Philippsen <nils@tiptoe.de> - 1.9.12-1
- version 1.9.12
- update source URL
- update nodate, outdir, nointernalapi patches
- remove broken (undocumented, non-upstreamed) portnames patch
- remove obsolete ppc64-long/mpd, gcc* patches
- remove binary junk from README
- remove additional optimization options
- add jack_simdtests executable

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.10-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Feb 13 2017 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.10-8
- fix building with gcc7

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.10-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Igor Gnatenko <ignatenko@redhat.com> - 1.9.10-6
- Rebuild for readline 7.x

* Sat Feb 13 2016 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.10-5
- fix building with gcc6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.10-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 12 2015 Nils Philippsen <nils@redhat.com> - 1.9.10-2
- fix building with gcc5

* Fri Nov 28 2014 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.10-1
- update to 1.9.10

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 04 2014 Brendan Jones <brendan.jones.it@gmail.com> 1.9.9.5-6
- Fix build on aarch64 - commit #d11bb09

* Wed Mar 26 2014 Jaromir Capik <jcapik@redhat.com> - 1.9.9.5-5
- Adding bootstrap support to break libffado dependency loops

* Mon Feb 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.9.9.5-4
- Drop celt support, should use opus by default as it's long replaced it and it has better quality
- Re-enable firewire (libffado) support on ARMv7

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 08 2013 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.9.5-2
- rebuilt with opus support on Fedora > 18

* Tue Dec 25 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.9.5-1
- update to 1.9.9.5

* Tue Nov 20 2012 Brendan Jones <brendan.jones.it@gmail.com> 1.9.8-14
- Correct build flags

* Mon Nov 19 2012 Brendan Jones <brendan.jones.it@gmail.com> 1.9.8-13
- Build with -O0. RHBZ#827748 still not resolved with gcc-4.7.2
- Update README, add jack_control to dbus package
- Add upstream sigsegv fault handling patch

* Sun Oct 28 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-12
- Seem like RHBZ#827748 is resolved. Rebuild optimized

* Tue Sep 04 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-11
- Removed libfreebob dependency as this package is retired

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-9
- Build with -O0 until RHBZ#827748 is resolved

* Sun Apr 08 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-8
- Oops. Last build was against the wrong ffado on F-17. Rebuilding against override.

* Sat Apr 07 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-7
- Compile via -DJACK_32_64 RHBZ#803865
- Adjust rtprio limit to 70. Adjust jack default priority to 60. RHBZ#795094

* Sun Mar 25 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-6
- Rename limits file from 99-jack.conf to 95-jack.conf RHBZ#795094
- Increase maximum number of ports and clients RHBZ#803871
- Backport ffado runtime buffersize change feature from upstream trunk
- Backport jack-connect executable segfault fix from upstream trunk

* Fri Mar 02 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-5
- Fix ppc64 mpd issue RHBZ#799552

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.8-4
- Rebuilt for c++ ABI breakage

* Sat Jan 07 2012 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-3
- Separate package for jackdbus RHBZ#714748

* Sun Dec 25 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-2
- Disable parallel build (on configure stage) as it stalls half of the time
- Don't exclude jack_control and jackdbus RHBZ#714748

* Sat Dec 24 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.8-1
- update to 1.9.8

* Mon Aug 15 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.7-3
- Add ARM to firewire audio excludes

* Fri May 06 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.7-2
- Update the README.Fedora file with most recent configuration information.

* Sun Apr 03 2011 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.7-1
- update to 1.9.7

* Fri Mar 11 2011 Karsten Hopp <karsten@redhat.com> 1.9.6-6
- powerpc64 doesn't have uc_regs anymore

* Sat Feb 19 2011 Michael Schwendt <mschwendt@fedoraproject.org> - 1.9.6-6
- Rawhide: Patch for CELT 0.11 API change because of current broken deps.

* Wed Feb 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.6-5
- Try again once repo has refreshed

* Wed Feb 16 2011 Peter Robinson <pbrobinson@fedoraproject.org> - 1.9.6-4
- Rebuilt for new celt

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov 12 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.6-2
- Fix the realtime compat patch so it can detect the realtime kernel better

* Sat Nov 06 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.6-1
- update to 1.9.6
- update README.Fedora file with more recent information

* Thu Aug 26 2010 Dan Horák <dan[at]danny.cz> - 1.9.5-2
- no Firewire on s390(x)
- fix building on other arches than x86 and ppc

* Mon Jul 19 2010 Orcan Ogetbil <oget[dot]fedora[at]gmail[dot]com> - 1.9.5-1
- Jack 2!

* Sat Nov 21 2009 Andy Shevchenko <andy@smile.org.ua> - 0.118.0-1
- update to 0.118.0 (should fix #533419)
- remove upstreamed patch
- append new binaries to -example-clients subpackage

* Wed Nov  4 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 0.116.2-8
- update to 0.116.2
- make sure we cleanup threads that we open, fixes segfaults (thanks to Ray Strode)

* Tue Oct 27 2009 Dennis Gilmore <dennis@ausil.us> - 0.116.1-7
- dont build libfreebob support on s390 arches

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.116.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Jun 21 2009 Andy Shevchenko <andy@smile.org.ua> - 0.116.1-5
- create file under /etc/security/limits.d instead of limits.conf hack (#506583)
- rename jack-audio-connection-kit.pa to jack.pa in the documentation part

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.116.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 04 2009 Andy Shevchenko <andy@smile.org.ua> - 0.116.1-3
- avoid creation of the LaTeX documentation (temporary fix for #477402)

* Mon Dec 29 2008 Andy Shevchenko <andy@smile.org.ua> - 0.116.1-2
- fix multiarch conflict again (#477718, #341621)

* Sun Dec 14 2008 Andy Shevchenko <andy@smile.org.ua> - 0.116.1-1
- update to last official release
- update URL tag
- update file list accordingly

* Mon Jul 28 2008 Andy Shevchenko <andy@smile.org.ua> 0.109.2-3
- add a new requirement to be ensure we have /etc/security for postinstall
  script (#359291, #456830)
- provide a pulseaudio start script from README.Fedora
- append values for pulse-rt group to the limits.conf
- update README.Fedora regarding to the recent changes

* Sun Jul 20 2008 Andy Shevchenko <andy@smile.org.ua> 0.109.2-2
- apply patch to be work on ppc64 (#451531)
- update README.Fedora to describe integration jack with pulseaudio (#455193)

* Wed Feb 13 2008 Andy Shevchenko <andy@smile.org.ua> 0.109.2-1.1
- update to the last official release

* Mon Jan 21 2008 Andy Shevchenko <andy@smile.org.ua> 0.109.0-1
- update to the last official release (#429162)
- shut up the postinstall script (#359291)

* Sat Oct 20 2007 Andy Shevchenko <andy@smile.org.ua> 0.103.0-5
- fix timestamps to avoid multiarch conflicts (#341621)

* Tue Sep 04 2007 Andy Shevchenko <andy@smile.org.ua> 0.103.0-4
- fix Source Forge's URL scheme

* Thu Aug 16 2007 Andy Shevchenko <andy@smile.org.ua> 0.103.0-3
- fix according to new guidelines:
  - License tag
  - group creation

* Wed May 23 2007 Andy Shevchenko <andy@smile.org.ua> 0.103.0-1
- update to the last official release
- append defaults to the limits.conf (#221785, #235624)

* Wed Mar 07 2007 Andy Shevchenko <andy@smile.org.ua> 0.102.20-4
- drop libtermcap-devel build requirement (#231203)
- create special jackuser group (#221785)

* Sat Oct 28 2006 Andy Shevchenko <andy@smile.org.ua> 0.102.20-3
- fix BuildRequires: libfreebob -> libfreebob-devel

* Tue Oct 24 2006 Andy Shevchenko <andy@smile.org.ua> 0.102.20-2.1
- rebuild with libfreebob (should closed #211751)

* Wed Oct 11 2006 Andy Shevchenko <andy@smile.org.ua> 0.102.20-2.0
- update to 0.102.20
- drop patch0 (already in mainstream)
- no pack jack_transport (build error)
- pack new JACK MIDI files

* Tue Aug 29 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-13
- http://fedoraproject.org/wiki/Extras/Schedule/FC6MassRebuild

* Tue Aug 01 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-12
- use install instead of cp (#200835)

* Tue Jul 04 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-11
- update URL
- add BR: libtool

* Tue Jun 20 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-10
- add BRs: autoconf, automake
  (http://fedoraproject.org/wiki/QA/FixBuildRequires)

* Sat May 27 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-9
- remove --enable-stripped-jackd and --enable-optimize (use default flags)

* Fri May 19 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-8
- uniform directories items at %%files section

* Wed May 17 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-7
- change License tag to GPL/LGPL
- remove --enable-shared (it should be default)
- add a -p flag to the line that copies README.Fedora

* Wed May 10 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-6
- apply clock fix for AMD X2 CPUs (please, refer to
  http://sourceforge.net/mailarchive/forum.php?thread_id=8085535&forum_id=3040)

* Wed May 03 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-5
- adjust spec after reviewing

* Thu Apr 27 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-4
- reformatting README.Fedora to 72 symbols width

* Wed Apr 26 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-3
- add README.Fedora
- remove useless BRs

* Mon Apr 24 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-2
- disable oss and portaudio engines
- use /dev/shm as jack tmpdir
- remove capabilities stuff

* Tue Apr 04 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-1
- update to 0.101.1

* Mon Mar 27 2006 Andy Shevchenko <andriy@asplinux.com.ua>
- update to 0.100.7 (#183912)
- adjust BR (add versions)
- replace files between examples and main packages
- own jack tmpdir

* Fri Mar 17 2006 Andy Shevchenko <andriy@asplinux.com.ua>
- no libs subpackage
- From Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>:
  - added configuration variable to build with/without capabilities
  - added --enable-optimize flag to configure script
  - disabled sse/mmx instructions in i386 build
  - create temporary directory as /var/lib/jack/tmp
  - create and erase tmp directory at install or uninstall
  - try to umount the temporary directory before uninstalling the package

* Fri Mar 03 2006 Andy Shevchenko <andriy@asplinux.com.ua>
- fix spec for extras injection

* Fri Nov 18 2005 Andy Shevchenko <andriy@asplinux.ru>
- exclude *.la files
- use dist tag

* Fri Oct 14 2005 Andy Shevchenko <andriy@asplinux.ru>
- 0.100.0
- no optimization

* Tue Sep 28 2004 Andy Shevchenko <andriy@asplinux.ru>
- 0.99.1

* Fri Aug 20 2004 Andy Shevchenko <andriy@asplinux.ru>
- rebuild from Mandrake
