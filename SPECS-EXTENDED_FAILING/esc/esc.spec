Vendor:         Microsoft Corporation
Distribution:   Mariner
Name: esc 
Version: 1.1.2
Release: 6%{?dist}
Summary: Enterprise Security Client Smart Card Client
License: GPL+
URL: http://directory.fedora.redhat.com/wiki/CoolKey 


#BuildRequires: doxygen fontconfig-devel
BuildRequires: glib2-devel atk-devel
BuildRequires: pkgconfig
BuildRequires: nspr-devel nss-devel nss-static
#BuildRequires: libX11-devel libXt-devel

BuildRequires: pcsc-lite-devel
BuildRequires: desktop-file-utils
BuildRequires: pkgconfig(gconf-2.0)
BuildRequires: dbus-glib-devel
BuildRequires: glib2-devel
BuildRequires: opensc
BuildRequires: gobject-introspection-devel
BuildRequires: gtk3-devel
BuildRequires: gjs-devel
BuildRequires: gcc-c++


Requires: pcsc-lite nss nspr
Requires: dbus
Requires: opensc
Requires: gjs
Requires: gobject-introspection
Requires: gtk3
Requires: glib2


# 390 does not have  smartCards
ExcludeArch: s390 s390x 
#xulrunner doesn't seem to support these right now
#Temporary anyway, since xulrunner is going away soon. 

# We can't allow the internal xulrunner to leak out
AutoReqProv: 0

%define debug_build       0

%define escname %{name}-%{version}
%define escdir %{_libdir}/%{escname}
%define escbindir %{_bindir}
%define esc_chromepath   chrome/content/esc
%define appdir applications
%define icondir %{_datadir}/icons/hicolor/48x48/apps
%define esc_vendor esc 
%define autostartdir %{_sysconfdir}/xdg/autostart
%define pixmapdir  %{_datadir}/pixmaps
%define docdir    %{_defaultdocdir}/%{escname}

Source0: http://pki.fedoraproject.org/pki/sources/%name/%{escname}.tar.bz2 
Source1: http://pki.fedoraproject.org/pki/sources/%name/esc
Source2: http://pki.fedoraproject.org/pki/sources/%name/esc.desktop
Source3: http://pki.fedoraproject.org/pki/sources/%name/esc.png


%description
Enterprise Security Client allows the user to enroll and manage their
cryptographic smartcards.

%prep

%setup -q -c -n %{escname}

#patch esc 

%build

echo $RPM_BUILD_DIR

echo "build section" $PWD
cd esc 

./autogen.sh
make 
%install

echo "install section" $PWD
cd esc
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT/%{escbindir}
mkdir -p $RPM_BUILD_ROOT/%{icondir}
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/%{appdir}
mkdir -p $RPM_BUILD_ROOT/%{pixmapdir}
mkdir -p $RPM_BUILD_ROOT/%{docdir}

echo "dir: "  $RPM_BUILD_ROOT/%{escbindir}/%{name}
sed -e 's;\$LIBDIR;'%{_libdir}';g'  %{SOURCE1} > $RPM_BUILD_ROOT/%{escbindir}/%{name}
chmod 755 $RPM_BUILD_ROOT/%{escbindir}/%{name}

mkdir -p $RPM_BUILD_ROOT/%{escdir}
mkdir -p $RPM_BUILD_ROOT/%{escdir}/lib

cp $RPM_BUILD_ROOT/usr/local/bin/* $RPM_BUILD_ROOT/%{escdir}

cp -rf $RPM_BUILD_ROOT/usr/local/lib $RPM_BUILD_ROOT/%{escdir}

rm $RPM_BUILD_ROOT/%{escdir}/lib/*.a
rm $RPM_BUILD_ROOT/%{escdir}/lib/*.la


rm -rf $RPM_BUILD_ROOT/usr/local

cp %{SOURCE3} $RPM_BUILD_ROOT/%{icondir}
ln -s $RPMBUILD_ROOT%{icondir}/esc.png $RPM_BUILD_ROOT/%{pixmapdir}/esc.png

cp %{SOURCE2} $RPM_BUILD_ROOT/%{_datadir}/%{appdir}

cd %{_builddir}
cp %{escname}/esc/LICENSE $RPM_BUILD_ROOT/%{docdir}


%files
%{!?_licensedir:%global license %%doc}
%license %{docdir}/LICENSE

%{escbindir}/esc
%{escdir}/lib
%{escdir}/esc.js
%{escdir}/opensc.esc.conf


%{icondir}/esc.png
%{pixmapdir}/esc.png
%{_datadir}/%{appdir}/esc.desktop

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.1.2-6
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Aug 01 2018 Jack Magne <jmagne@redhat.com> - 1.1.2-1
- Remove uneeded Requires and no longer put in autostart directory.
* Mon Jul 30 2018 Jack Magne <jmagne@redhat.com> - 1.1.2-1
- Build bare bones esc, without xulrunner, using gjs / gobject 
- introspection.
* Thu Jun 07 2018 Jack Magne <jmagne@redhat.com> - 1.1.1-5
- Rebuild.
* Mon Apr 23 2018 Jack Magne <jmagne@redhat.com> - 1.1.1-4 
- Remove coolkey dependencies, replace with opensc.
* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.1.1-2
- Remove obsolete scriptlets

* Mon Aug 07 2017 - 1.1.1-1
- Rebuilt using internally built xulrunner, due to the xulrunner package going away.
* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sun May  8 2016 Peter Robinson <pbrobinson@fedoraproject.org> 1.1.0-30
- Secondary arch fixes
- Use %%license

* Mon Feb 08 2016 Jack Magne <jmagne@redhat.com> 1.1.0-29
- Apease latest xullrunner api changes.

* Thu Apr 09 2015 Jack Magne <jmagne@redhat.com> 1.1.0-27
- More xulrunner adjustments.
* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 23 2014 Jack Magne <jmagne@redhat.com>=1.1.0-24
- Fix minor http client error.
* Thu Apr 17 2014 Jack Maghe <jmagne@redhat.com>=1.1.0-23
- Appease more xulrunner changes.
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul  7 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.1.0-22
- Make buildable with kernels > 3.5.
- %%changelog syntax and bogus date fixes.
- Bump xulrunner version to 22.0.

* Mon Jun 17 2013 Jack Magne <jmagne@redhat.com>- 1.1.0-21
- Appease latest compiler errors and build to xulrunner 21.0.
* Wed Nov 28 2012 Jack Magne <jmagne@redhat.com>- 1.1.0-20
- Gecko no longer supports UniversalXPConnect, remove it.
* Wed Nov 21 2012 Jack Magne <jmagne@redhat.com>- 1.1.0-19
- Pick up latest fixes.
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012   Jack Magne <jmagne@redhat.com>- 1.1.0-17
- Related #688361 - Get ESC to run on Gecko 2.0, again.
* Thu May 10 2012   Jack Magne <jmagne@redhat.com>- 1.1.0-16
- Related #688361 - Get ESC to run on Gecko 2.0.
* Mon Feb 20 2012   Jack Magne <jmagne@redhat.com>- 1.1.0-15
- Related #688361 - Get ESC to run on Gecko 2.0.
* Tue Nov 29 2011   Jack Magne <jmagne@redhat.com>- 1.1.0-14
- Related #688361 - Get ESC to run on Gecko 2.0.
* Thu Apr 15 2010   Jack Magne <jmagne@redhat.com>- 1.1.0-11
- Adjust for new linking rules.
* Tue Sep 15 2009   Jack Magne <jmagne@redhat.com>- 1.1.0-10
- Pick up latest improvements.
* Mon Jun 22 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-9
- Related: #496410, also IPV6 support.
* Fri Jun 19 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-8
- Related: #496410, SSL Conn fix.
* Mon Jun 8  2009  Jack Magne <jmagne@redhat.com>- 1.1.0-7
- Releated: #496410.
* Thu Apr 23 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-6
- Related: #496410. Appease rpmdiff.
* Wed Apr 22 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-5
- Related: #496410, addresses 494981, better error message.
* Wed Apr 22 2009  Jack Magne <jmagne@redhat.com>- 1.1.0-4
- Move to latest rebased code. Related #496410.
* Thu Dec 04 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-39
- Resolves #469202 - Cert Viewer issue              
* Tue Nov 11 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-38
- Resolves  #471923 - ESC Connection issue.
* Thu Oct 16 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-37
- Resolves #467126 - Blank authentication dialog problem. 
* Fri Sep 26 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-36
- Related #200475 - Require the xulrunner package, Resolves #248493
* Thu Sep 18 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-35
- Related 200475, make rpmdiff tests happy.
* Tue Sep 16 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-34
- Resolves #200475 #253081 #437238
* Thu Jan 10 2008  Jack Magne <jmagne@redhat.com>- 1.0.0-33
- Resolves #25324a8 #253268
* Thu Jul 12 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-32
- Resolves #248071 - ESC RPM unistall failure if daemon not running.
* Fri Jun 22 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-31
- Related #208038 - Top things to put in diagnostics log
* Wed Jun 20 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-30
- Related #204021
* Fri Jun 8 2007   Jack Magne <jmagne@redhat.com>- 1.0-0-29
- Related #212010
* Fri Jun 8 2007   Jack Magne <jmagne@redhat.com>- 1.0.0-28
- Resolves #212010 
* Tue Jun 5 2007   Jack Magne <jmagne@redhat.com>- 1.0.0-27 
- Resolves #203466 Better error message strings.
* Mon May 21 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-26
- Related: #206783 Fix the launcher script to work with new logging.
* Fri May 11 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-25
- Resolves: #206783.
* Mon Apr 23 2007 Jack Magne <jmagne@redhat.com>- 1.0.0-24
- More Desktop appearance fixes.
- Related: #208749
* Mon Apr 23 2007  Jack Magne <jmagne@redhat.com>- 1.0.0-23
- Desktop appearance fixes.
- Related: #208749
* Thu Apr 19 2007 Jack Magne <jmagne@redhat.com>- 1.0.0-22
- Second drop of 5.1 fixes.
- Resolves: #203934, #203935, #204959, #206780, #206792, #207721
- Resolves: #207816, #206791
- Related:  #208749
* Wed Apr 18 2007 Jack Magne <jmagne@redhat.com>- 1.0.0-21
- First 5.1 fixes.
- Resolves: #203757, #203806, #204661, #205856, #206788, #206791
- Resolves: #208037, #208333, #210589, #210590, #213912, #226913
- Resolves: #204021, #205498, #224436
* Tue Nov 28 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-20
- fix for bug to commit config changes immediately.  Bug #210988
* Wed Nov 15 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-19
-fix for escd double free problem. Bug #209882
* Tue Oct 24 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-18
-rebuilt on RHEL-5 branch
* Wed Oct 4  2006 Jack Magne <jmagne@redhat.com>- 1.0.0-17
- Diagnostics display fixes, Mac and Window fixes.

* Sun Oct 01 2006 Jesse Keating <jkeating@redhat.com> - 1.0.0-16
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Fri Sep 22 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-15
- Fix to the build version

* Fri Sep 22 2006 Jack Magne <jmagne@redhat.com>= 1.0.0-14
- Fix to compile error in daemon

* Fri Sep 22 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-13
- Fix to include the new esc daemon.  

* Sat Sep 16 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-12
- Fix for Password Reset and minor UI revision.

* Fri Sep 15 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-11
- Further UI enhancement bug fixes

* Thu Sep 7 2006 Jack Magne <jmagne@redhat.com>- 1.0.0-10
- Further strings revisions.

* Wed Aug 30 2006 Jack Magne <jmagne@redhat.com>-  1.0.0-9
- Revision of the strings used in ESC.

* Wed Aug 30 2006 Jack Magne <jmagne@redhat.com>-  1.0.0-8
- Fixes to get libnotify working properly on FC6 systems.

* Tue Aug 22 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-7
- Fix for bug #203211, use of system NSS and NSPR for
- Xulrunner ,addressing the problem running on 64 bit.
- Overwriting 5 and 6 due to important bug #203211.

* Fri Aug  18 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-6
- Correct problem with Patch #6

* Fri Aug  18 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-5
- Build ESC's xulrunner component using system nss and nspr
- Build process creates run script based on {_libdir} variable,
  accounting for differences on 64 bit machines.
- UI enhancements

* Tue Aug  1 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.0-4
- Don't auto-generate requires either

* Mon Jul 31 2006 Matthias Clasen <mclasen@redhat.com> - 1.0.0-3
- Don't provide mozilla libraries

* Fri Jul 28 2006 Ray Strode <rstrode@redhat.com> - 1.0.0-2
- remove bogus gtk+ requires (and some others that will
  be automatic)

* Tue Jun 13 2006 Jack Magne <jmagne@redhat.com> - 1.0.0-1
- Initial revision for fedora

