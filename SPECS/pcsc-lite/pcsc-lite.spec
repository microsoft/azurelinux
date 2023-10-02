Summary:        PC/SC Lite smart card framework and applications
Name:           pcsc-lite
Version:        1.9.5
Release:        2%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://pcsclite.apdu.fr/
Source0:        https://pcsclite.apdu.fr/files/%{name}-%{version}.tar.bz2
Source1:        org.debian.pcsc-lite.policy
BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  systemd-devel
BuildRequires:  /usr/bin/pod2man
BuildRequires:  polkit-devel
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  libtool
BuildRequires:  gnupg2
BuildRequires:  gcc
BuildRequires:  python3-devel
BuildRequires:  /usr/bin/pathfix.py

Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
Requires:       pcsc-ifd-handler
Requires:       %{name}-libs = %{version}-%{release}
Requires:       polkit
Requires:       python3
Recommends:     pcsc-lite-ccid
# This is bundled in upstream withou simple way to remove
Provides:       bundled(simclist) = 1.6


%description
The purpose of PC/SC Lite is to provide a Windows(R) SCard interface
in a very small form factor for communicating to smartcards and
readers.  PC/SC Lite uses the same winscard API as used under
Windows(R).  This package includes the PC/SC Lite daemon, a resource
manager that coordinates communications with smart card readers and
smart cards that are connected to the system, as well as other command
line tools.

%package        libs
Summary:        PC/SC Lite libraries

%description    libs
PC/SC Lite libraries.

%package        devel
Summary:        PC/SC Lite development files
Requires:       %{name}-libs = %{version}-%{release}

%description    devel
PC/SC Lite development files.

%package        doc
Summary:        PC/SC Lite developer documentation
BuildArch:      noarch
Requires:       %{name}-libs = %{version}-%{release}

%description    doc
%{summary}.

%prep

%setup -q

# Convert to utf-8
for file in ChangeLog; do
    iconv -f ISO-8859-1 -t UTF-8 -o $file.new $file && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%configure \
  --disable-static \
  --enable-polkit \
  --enable-usbdropdir=%{_libdir}/pcsc/drivers
make %{?_smp_mflags}
doxygen doc/doxygen.conf ; rm -f doc/api/*.{map,md5}
pathfix.py -pni "%{__python3} %{py3_shbang_opts}" src/spy/pcsc-spy


%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/org.debian.pcsc-lite.policy

mkdir -p $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/
install -p -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/polkit-1/actions/

# Create empty directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/reader.conf.d
mkdir -p $RPM_BUILD_ROOT%{_libdir}/pcsc/drivers
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/pcscd

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%post
%systemd_post pcscd.socket pcscd.service
# If install, test if pcscd socket is enabled.
# If enabled, then attempt to start it. This will silently fail
# in chroots or other environments where services aren't expected
# to be started.
if [ $1 -eq 1 ] ; then
   if systemctl -q is-enabled pcscd.socket > /dev/null 2>&1 ; then
      systemctl start pcscd.socket > /dev/null 2>&1 || :
   fi
fi

%preun
%systemd_preun pcscd.socket pcscd.service

%postun
%systemd_postun_with_restart pcscd.socket pcscd.service

%ldconfig_scriptlets libs

%files
%doc AUTHORS ChangeLog HELP README SECURITY TODO
%doc doc/README.polkit
%dir %{_sysconfdir}/reader.conf.d/
%{_unitdir}/pcscd.service
%{_unitdir}/pcscd.socket
%{_sbindir}/pcscd
%dir %{_libdir}/pcsc/
%dir %{_libdir}/pcsc/drivers/
%{_mandir}/man5/reader.conf.5*
%{_mandir}/man8/pcscd.8*
%{_datadir}/polkit-1/actions/org.debian.pcsc-lite.policy
%ghost %dir %{_localstatedir}/run/pcscd/

%files libs
%license COPYING
%{_libdir}/libpcsclite.so.*

%files devel
%{_bindir}/pcsc-spy
%{_includedir}/PCSC/
%{_libdir}/libpcsclite.so
%{_libdir}/libpcscspy.so*
%{_libdir}/pkgconfig/libpcsclite.pc
%{_mandir}/man1/pcsc-spy.1*

%files doc
%doc doc/api/ doc/example/pcsc_demo.c

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 1.9.5-2
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Thu Feb 10 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.9.5-1
- Update to v1.9.5.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.9.0-2
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Mon Jun 15 2020 Jakub Jelen <jjelen@redhat.com> - 1.9.0-1
- New upstream release (#1846925)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 20 2020 Jakub Jelen <jjelen@redhat.com> - 1.8.26-1
- New upstream release

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Apr 05 2019 Jakub Jelen <jjelen@redhat.com> - 1.8.25-1
- New upstream release (#1692559)
- Fix memory leak in SCardEstablishContextTH() (#1684674)
- Enable socket activation after installation (#1545027)

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 20 2018 Jakub Jelen <jjelen@redhat.com> - 1.8.24-1
- New upstream release (#1651353)

* Mon Jul 23 2018 Jakub Jelen <jjelen@redhat.com> - 1.8.23-4
- Add missing dependencies (#1605389)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Dec 19 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.23-1
- New upstream release

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.22-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.22-1
- New upstream release

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan  2 2017 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.20-1
- New upstream release

* Fri Dec  9 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.19-1
- New upstream release

* Wed Nov 30 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.18-1
- New upstream release

* Thu Jun 30 2016 Ville Skyttä <ville.skytta@iki.fi> - 1.8.17-2
- Add dependency on polkit
- Mark COPYING as %%license
- Fix bogus dates in changelog

* Tue Jun 21 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.17-1
- New upstream release

* Fri Apr  1 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.16-1
- New upstream release (#1319539)
- Added gpg key verification as part of build process

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 11 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.15-1
- New upstream release (#1294262)

* Wed Nov 18 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.14-2
- Recommend pcsc-lite-ccid package (#1280447)

* Wed Aug  5 2015 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.14-1
- New upstream release

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Nov  7 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.13-1
- New upstream release

* Wed Sep 24 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.12-1
- New upstream release (#1079514)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jun 03 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.11-1
- New upstream release
- Safer usage of libudev functions

* Tue Mar 11 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.10-3
- The default installed polkit policy allows console users to access
  smart cards. Non-interactive or remote usage now requires admin
  rights, or a specific policy (see README.polkit)

* Tue Feb 11 2014 Nikos Mavrogiannopoulos <nmav@redhat.com> - 1.8.10-2
- Added upstream patch to support polkit
- Force sanity of parameters received by the client

* Sun Oct 20 2013 Kalev Lember <kalevlember@gmail.com> - 1.8.10-1
- Update to 1.8.10
- Update source URL
- Drop large ChangeLog.svn from %%doc

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 28 2013 Kalev Lember <kalevlember@gmail.com> - 1.8.8-1
- Update to 1.8.8
- Use new systemd macros (#850264)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 30 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.7-1
- Update to 1.8.7

* Tue Sep 18 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.6-1
- Update to 1.8.6

* Mon Aug 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.5-1
- Update to 1.8.5

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 26 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.4-1
- Update to 1.8.4

* Thu Jun 14 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.3-2
- Rebuild for new libudev (#831987)

* Fri Mar 30 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.3-1
- Update to 1.8.3

* Mon Feb 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.8.2-1
- Update to 1.8.2
- Drop the systemd support patches which are now upstreamed
- Package the new pcsc-spay tool in -devel subpackage

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Oct 10 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-6
- Remove the automatic card power down disabling patch again;
  no longer needed with latest libusb1 1.0.9 rc1 (#737988)

* Fri Sep 16 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-5
- Reapply the patch to disable automatic card power down (#737988)

* Sun Sep 04 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-4
- Ignore errors from 'systemctl enable' (#734852)

* Sat Aug 20 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-3
- Use /var/run/pcscd for ipc directory (#722449)

* Fri Jul 15 2011 Kalev Lember <kalevlember@gmail.com> - 1.7.4-2
- Converted initscript to systemd service file (#617330)

* Fri Jun 24 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.4-1
- Update to 1.7.4

* Wed Jun 22 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.3-1
- Update to 1.7.3
- Dropped upstreamed patches
- Dropped the lib64 rpath patch; pcsc-lite now uses system libtool
- Cleaned up the spec file for modern rpmbuild

* Wed May 25 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.2-2
- Don't fill log files with repeating messages (#657658, #707412)

* Thu Mar 31 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.2-1
- Update to 1.7.2

* Wed Mar 30 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.1-1
- Update to 1.7.1

* Thu Mar 17 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.0-2
- Explicitly create and own drivers directory

* Wed Mar 09 2011 Kalev Lember <kalev@smartlink.ee> - 1.7.0-1
- Update to 1.7.0
- Use libudev for hotplugging instead of hal

* Fri Feb 25 2011 Kalev Lember <kalev@smartlink.ee> - 1.6.7-1
- Update to 1.6.7
- Rebased noautostart patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.6-2
- Disabled automatic card power down which seems to be unreliable at this point

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.6-1
- Update to 1.6.6

* Mon Dec 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.4-2
- Disabled pcscd on-demand startup (#653903)

* Sun Aug 15 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.4-1
- Update to 1.6.4
- Buildrequire graphviz for apidoc generation

* Wed Aug 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.2-1
- Update to 1.6.2
- Dropped upstreamed patches
- Removed configure --disable-dependency-tracking option which is the
  default with configure macro.

* Thu Jul 08 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-5
- Include COPYING in libs subpackage as per new licensing guidelines

* Mon Jul 05 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-4
- Patch to fix crash with empty config directory

* Sun Jul 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-3
- Patch to fix config dir handling

* Sun Jul 04 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-2
- Removed call to non-existent update-reader.conf in init script

* Fri Jun 18 2010 Kalev Lember <kalev@smartlink.ee> - 1.6.1-1
- Update to 1.6.1

* Tue Apr 13 2010 Kalev Lember <kalev@smartlink.ee> - 1.5.5-4
- Fix init script start / stop priorities (#580322)
- Don't require pkgconfig as the dep is now automatically generated by rpm

* Wed Mar 03 2010 Kalev Lember <kalev@smartlink.ee> - 1.5.5-3
- Added patch to fix init script LSB header (#565241)
- Dropped BR: libusb-devel as configure script really picks up libhal instead
- Use %%global instead of %%define

* Mon Dec 21 2009 Kalev Lember <kalev@smartlink.ee> - 1.5.5-2
- Require -libs subpackage from main pcsc-lite package
- Build -doc subpackage as noarch
- Dropped --enable-runpid configure option which was removed in 1.4.99
- Dropped obsolete provides
- Spec file cleanup

* Wed Nov 18 2009 Kalev Lember <kalev@smartlink.ee> - 1.5.5-1
- Updated to pcsc-lite 1.5.5
- Rebased rpath64 patch
- Dropped upstreamed pcsc-lite-1.5-permissions.patch

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 17 2009 Bob Relyea <rrelyea@redhat.com> - 1.5.2-2
- Pick up security fixes from upstream

* Fri Feb 27 2009 Bob Relyea <rrelyea@redhat.com> - 1.5.2-1
- Pick up 1.5.2
- Add FD_CLOEXEC flag
- make reader.conf a noreplace config file

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.102-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Karsten Hopp <karsten@redhat.com> 1.4.102-4
- remove excludearch s390, s390x (#467788)
  even though s390 does not have libusb or smartCards, the libusb
  packages are required to build other packages.

* Thu Aug 28 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.102-3
- bump tag becaue the build system can't deal with mistakes.

* Thu Aug 28 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.102-2
- mock build changes

* Thu Aug 28 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.102-1
- Pick up 1.4.102

* Tue May 6 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.101-1
- Pick up 1.4.101

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.4.4-3
- Autorebuild for GCC 4.3

* Wed Jan 16 2008 Bob Relyea <rrelyea@redhat.com> - 1.4.4-2
- Silence libpcsc-lite even when the daemon isn't running.
- fix typo in init file which prevents the config file from being read.

* Thu Nov 22 2007 Bob Relyea <rrelyea@redhat.com> - 1.4.4-1
- Pick up 1.4.4

* Tue Feb 06 2007 Bob Relyea <rrelyea@redhat.com> - 1.3.3-1
- Pick up 1.3.3

* Thu Nov 02 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.2-1
- Pick up 1.3.2

* Thu Sep 14 2006  Bob Relyea <rrelyea@redhat.com> - 1.3.1-7
- Incorporate patch from Ludovic to stop the pcsc daemon from
  unnecessarily waking up.

* Mon Jul 31 2006 Ray Strode <rstrode@redhat.com> - 1.3.1-6
- follow packaging guidelines for setting up init service
  (bug 200778)

* Mon Jul 24 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.1-5
- start pcscd when pcsc-lite is installed

* Sun Jul 16 2006 Florian La Roche <laroche@redhat.com> - 1.3.1-4
- fix excludearch line

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.3.1-3.1
- rebuild

* Mon Jul 10 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.1-3
- remove s390 from the build

* Mon Jun 5 2006 Bob Relyea <rrelyea@redhat.com> - 1.3.1-2
- Move to Fedora Core. 
- Remove dependency on graphviz. 
- Removed %%{_dist}

* Sat Apr 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.3.1-1
- 1.3.1.

* Sun Mar  5 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.3.0-1
- 1.3.0, init script and reader.conf updater included upstream.
- Split developer docs into a -doc subpackage, include API docs.
- libmusclecard no longer included, split into separate package upstream.

* Mon Feb 13 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.2.0-14
- Avoid standard rpaths on multilib archs.
- Fine tune dependencies.

* Fri Nov 11 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.0-13
- Don't ship static libraries.
- Don't mark the init script as a config file.
- Use rm instead of %%exclude.
- Specfile cleanups.

* Thu May 19 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.2.0-12
- Rebuild.

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.2.0-11
- rebuilt

* Tue Aug 17 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-10
- Disable dependency tracking to speed up the build.
- Drop reader.conf patch, it's not needed any more.
- Rename update-reader-conf to update-reader.conf for consistency with Debian,
  and improve it a bit.

* Sat Jul 31 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.9
- Add update-reader-conf, thanks to Fritz Elfert.

* Thu Jul  1 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.8
- Own the %%{_libdir}/pcsc hierarchy.

* Thu May 13 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.7
- Make main package require pcsc-ifd-handler (idea from Debian).

* Wed May 12 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.6
- Improve package summary.
- Improvements based on suggestions from Ludovic Rousseau:
  - Don't install pcsc_demo but do include its source in -devel.
  - Sync reader.conf with current upstream CVS HEAD (better docs, less
    intrusive in USB-only setups where it's not needed).

* Fri Apr 16 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.5
- Move PDF API docs to -devel.
- Improve main package and init script descriptions.

* Thu Jan 29 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.4
- Init script fine tuning.

* Fri Jan  9 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.3
- BuildRequires libusb-devel 0.1.6 or newer.

* Thu Oct 30 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.2
- s/pkgconfi/pkgconfig/ in -devel requirements.

* Tue Oct 28 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.1
- Update to 1.2.0.
- Add libpcsc-lite and libmusclecard provides to -libs and -devel.

* Thu Oct 16 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.2.rc3
- Update to 1.2.0-rc3.
- Trivial init script improvements.
- Enable %%{_smp_mflags}.
- Don't bother trying to enable SCF.

* Sun Sep 14 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.2.rc2
- Specfile cleanups.

* Fri Sep  5 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.1.rc2
- Update to 1.2.0-rc2.

* Wed Aug 27 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.2.0-0.fdr.0.1.rc1
- Update to 1.2.0-rc1.

* Sun Jun  1 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-0.fdr.0.1.beta5
- Update to 1.1.2beta5.

* Sat May 24 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.1.2-0.fdr.0.1.beta4
- First build, based on PLD's 1.1.1-2.
