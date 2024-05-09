Vendor:         Microsoft Corporation
Distribution:   Azure Linux
#
# $Id: sblim-sfcb.spec,v 1.5 2010/06/23 10:31:02 vcrhonek Exp $
#
# Package spec for sblim-sfcb
#

Name: sblim-sfcb
Summary: Small Footprint CIM Broker
URL: https://sblim.wiki.sourceforge.net/
Version: 1.4.9
Release: 20%{?dist}
License: EPL-1.0
Source0: https://downloads.sourceforge.net/sblim/%{name}-%{version}.tar.bz2
Source1: sfcb.service
# Missing man pages
Source2: sfcbdump.1.gz
Source3: sfcbinst2mof.1.gz
Source4: sfcbtrace.1.gz
# Patch0: changes schema location to the path we use
Patch0: sblim-sfcb-1.3.9-sfcbrepos-schema-location.patch
# Patch1: Fix provider debugging - variable for stopping wait-for-debugger
# loop must be volatile
Patch1: sblim-sfcb-1.3.15-fix-provider-debugging.patch
# Patch2: increase default value of maxMsgLen in sfcb.cfg
Patch2: sblim-sfcb-1.3.16-maxMsgLen.patch
# Patch3: we'll install own service file
Patch3: sblim-sfcb-1.4.5-service.patch
# Patch4: fixes multilib issue with man page and config file
Patch4: sblim-sfcb-1.3.16-multilib-man-cfg.patch
# Patch5: change default ecdh curve name, as the original is not enabled
#   in openssl on Fedora, rhbz#1097794
Patch5: sblim-sfcb-1.4.8-default-ecdh-curve-name.patch
Patch6: sblim-sfcb-1.4.9-fix-ftbfs.patch
# Patch7: fix possible null pointer dereference (CVE-2015-5185), rhbz#1255802
Patch7: sblim-sfcb-1.4.9-fix-null-deref.patch
# Patch8: fix null pointer (DoS) vulnerability via POST request to /cimom
#   (CVE-2018-6644), patch by Adam Majer, rhbz#1543826
Patch8: sblim-sfcb-1.4.9-fix-null-content-type-crash.patch
# Patch9: removes decrease of optimization level to -O0 on ppc64le
Patch9: sblim-sfcb-1.4.9-fix-ppc-optimization-level.patch
# Patch10: fixes docdir name and removes install of COPYING with license
#   which is included through %%license
Patch10: sblim-sfcb-1.4.9-docdir-license.patch
# Patch11: fixes multiple definiton of variables (FTBFS with GCC 10)
Patch11: sblim-sfcb-1.4.9-fix-multiple-definition.patch

Provides: cim-server = 0
Requires: cim-schema
Requires: perl(LWP::UserAgent)
Requires: sblim-sfcCommon

BuildRequires: libcurl-devel
BuildRequires: perl-generators
BuildRequires: zlib-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: cim-schema
BuildRequires: bison flex
BuildRequires: sblim-cmpi-devel
BuildRequires: systemd
BuildRequires: sblim-sfcCommon-devel
BuildRequires: openslp-devel
BuildRequires: gcc

Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%Description
Small Footprint CIM Broker (sfcb) is a CIM server conforming to the
CIM Operations over HTTP protocol.
It is robust, with low resource consumption and therefore specifically 
suited for embedded and resource constrained environments.
sfcb supports providers written against the Common Manageability
Programming Interface (CMPI).

%prep
%setup -q -T -b 0 -n %{name}-%{version}
%patch 0 -p1 -b .sfcbrepos-schema-location
%patch 1 -p1 -b .fix-provider-debugging
%patch 2 -p1 -b .maxMsgLen
%patch 3 -p1 -b .service
%patch 4 -p1 -b .multilib-man-cfg
%patch 5 -p1 -b .default-ecdh-curve-name
%patch 6 -p1 -b .fix-ftbfs
%patch 7 -p1 -b .fix-null-deref
%patch 8 -p1 -b .fix-null-content-type-crash
%patch 9 -p1 -b .fix-ppc-optimization-level
%patch 10 -p1 -b .docdir-license
%patch 11 -p1 -b .fix-multiple-definition

%build
%configure --enable-debug --enable-uds --enable-ssl --enable-pam --enable-ipv6 \
    --enable-slp --enable-large_volume_support --enable-optimized-enumeration --enable-relax-mofsyntax \
    CFLAGS="$CFLAGS -D_GNU_SOURCE -fPIE -DPIE" LDFLAGS="$LDFLAGS -Wl,-z,now -pie"
 
make 

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT/%{_sysconfdir}/init.d/sfcb
mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
install -p -m644 %{SOURCE1} $RPM_BUILD_ROOT/%{_unitdir}/sblim-sfcb.service
# install man pages
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1/
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT/%{_mandir}/man1/
# remove unused static libraries and so files
rm -f $RPM_BUILD_ROOT/%{_libdir}/sfcb/*.la

echo "%%license COPYING" > _pkg_list
find $RPM_BUILD_ROOT/%{_datadir}/sfcb -type f | grep -v $RPM_BUILD_ROOT/%{_datadir}/sfcb/CIM >> _pkg_list
sed -i s?$RPM_BUILD_ROOT??g _pkg_list > _pkg_list_2
echo "%config(noreplace) %{_sysconfdir}/sfcb/*" >> _pkg_list
echo "%config(noreplace) %{_sysconfdir}/pam.d/*" >> _pkg_list
echo "%doc %{_datadir}/doc/sblim-sfcb/[!COPYING]*" >> _pkg_list
echo "%{_datadir}/man/man1/*" >> _pkg_list
echo "%{_unitdir}/sblim-sfcb.service" >> _pkg_list
echo "%{_localstatedir}/lib/sfcb" >> _pkg_list
echo "%{_bindir}/*" >> _pkg_list
echo "%{_sbindir}/*" >> _pkg_list
echo "%{_libdir}/sfcb/*.so.*" >> _pkg_list
echo "%{_libdir}/sfcb/*.so" >> _pkg_list

cat _pkg_list

%pre
/usr/bin/getent group sfcb >/dev/null || /usr/sbin/groupadd -r sfcb
/usr/sbin/usermod -a -G sfcb root > /dev/null 2>&1 || :

%post 
%{_datadir}/sfcb/genSslCert.sh %{_sysconfdir}/sfcb &>/dev/null || :
/sbin/ldconfig
%{_bindir}/sfcbrepos -f > /dev/null 2>1
%systemd_post sblim-sfcb.service

%preun
%systemd_preun sblim-sfcb.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart sblim-sfcb.service
if [ $1 -eq 0 ]; then
        /usr/sbin/groupdel sfcb > /dev/null 2>&1 || :;
fi;

%files -f _pkg_list

%changelog
* Tue Mar 01 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.9-20
- Explicitly mentioning a run-time dependency on "perl(LWP::UserAgent)".
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.9-19
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Feb 12 2020 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-18
- Fixes multiple definiton of variables (FTBFS with GCC 10)
  Resolves: #1800074

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Oct 11 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-14
- Don't decrease optimization level to -O0 on ppc64le
- Use %%license for file which contains the text of the license
- Change versioned docdir to unversioned and rename the docdir to match
  the package name
- Remove %%defattr

* Mon Oct 08 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-13
- Fix license tag

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 27 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-11
- Add BuildRequires gcc

* Wed Feb 14 2018 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-10
- Fix null pointer (DoS) vulnerability via POST request to /cimom (CVE-2018-6644)
  (patch by Adam Majer)
  Resolves: #1543825

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Aug 24 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-4
- Fix possible null pointer dereference (CVE-2015-5185)
  Resolves: #1255587

* Mon Jul 13 2015 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-3
- Fix sblim-sfcb FTBFS in rawhide
  Resolves: #1239986

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 02 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.9-1
- Update to sblim-sfcb-1.4.9
- Silence sfcbrepos in %%post

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 15 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.8-2
- Fix SFCB fails to start: Failure setting ECDH curve name (secp224r1)
  Resolves: #1097794

* Thu Mar 27 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.8-1
- Update to sblim-sfcb-1.4.8

* Mon Mar 24 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.7-3
- Fix multilib issue with man page and config file

* Tue Jan 21 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.7-2
- Add few configure options, build require openslp-devel

* Thu Jan 02 2014 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.7-1
- Update to sblim-sfcb-1.4.7

* Wed Oct 09 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.6-2
- Add version to cim-server virtual provides

* Mon Oct 07 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.6-1
- Update to sblim-sfcb-1.4.6

* Thu Sep 05 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.4.5-1
- Update to sblim-sfcb-1.4.5

* Tue Aug 13 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.16-9
- Build require systemd for unitdir macro
  Resolves: #988777

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 1.3.16-8
- Perl 5.18 rebuild

* Tue Jul 23 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.16-7
- Fix CIM clients are sometimes getting HTTP/1.1 501 Not Implemented
  (patch by Tomas Bzatek)
  Resolves: #968397

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.3.16-6
- Perl 5.18 rebuild

* Mon Jun 24 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.16-5
- Increase default maxMsgLen
  Resolves: #967940

* Mon Jun 17 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.16-4
- Create missing man pages
- Add support for EmbeddedInstance qualifier
  Resolves: #919377

* Mon May 20 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.16-3
- Fix indCIMXmlHandler crash in IndCIMXMLHandlerInvokeMethod with Embedded Instances 
  Resolves: #957747
- Fix sfcb creates invalid XML with embedded object inside embedded object
  Resolves: #957742

* Tue Jan 29 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.16-2
- Fix URL in the spec file
- Remove unused devel part from the spec file
- Full relro support

* Tue Jan 08 2013 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.16-1
- Update to sblim-sfcb-1.3.16
- Fix provider debugging (patch by Radek Novacek)

* Thu Nov 29 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.15-5
- Comment patches

* Thu Sep 06 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.15-4
- Fix issues found by fedora-review utility in the spec file

* Thu Aug 23 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.15-3
- Use new systemd-rpm macros
  Resolves: #850307

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Jun 19 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.15-1
- Update to sblim-sfcb-1.3.15

* Thu Jun 07 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.14-2
- Remove SysV init script

* Wed Apr 04 2012 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.14-1
- Update to sblim-sfcb-1.3.14

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.13-1
- Update to sblim-sfcb-1.3.13

* Wed Sep 07 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.12-1
- Update to sblim-sfcb-1.3.12

* Wed Jun 15 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.11-2
- Remove sfcb system group in post uninstall scriptlet
- Fix minor rpmlint warnings

* Thu May 26 2011 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.11-1
- Update to sblim-sfcb-1.3.11

* Mon May  9 2011 Bill Nottingham - 1.3.10-5
- fix systemd scriptlets for upgrade

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan  7 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.3.10-3
- Added the required scripting to manage the service with systemd

* Fri Jan  7 2011 Praveen K Paladugu <praveen_paladugu@dell.com> - 1.3.10-2
- Following the BZ#660072, added sfcb.service file for compliance with systemd
- Since sfcb's PAM authentication requires, the user to be in group sfcb, 
-    added the root user to "sfcb" group in %%pre section.

* Mon Dec  6 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.10-1
- Update to sblim-sfcb-1.3.10
- Fix CMGetCharPtr macro (patch by Kamil Dudka)

* Mon Sep  6 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.9-1
- Update to sblim-sfcb-1.3.9
- Compile with --enable-uds, i. e. enable unix domain socket local
  connect functionality
- Create sfcb system group (used by basic authentication with PAM)
  in pre install scriptlet
- Fix default location where sfcbrepos is looking for schema files
  and simplify sfcbrepos command in post install sciptlet
- Add missing soname files

* Wed Jun 23 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.8-1
- Update to sblim-sfcb-1.3.8
- Fix unmatched calls of closeLogging() and startLogging()

* Thu Apr 22 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.7-3
- Fix initscript

* Mon Mar 22 2010 Vitezslav Crhonek <vcrhonek@redhat.com> - 1.3.7-2
- Make sblim-sfcb post install scriptlet silent
- Fix value.c

* Wed Mar  3 2010 <vcrhonek@redhat.com> - 1.3.7-1
- Update to sblim-sfcb-1.3.7
- Fix dist tag in Release field

* Tue Sep 22 2009 <srinivas_ramanatha@dell.com> - 1.3.4-8
- Removed the devel package and moved the init script to right directory

* Wed Sep 16 2009 <srinivas_ramanatha@dell.com> - 1.3.4-7
- Modified the spec based on Praveen's comments

* Thu Sep 10 2009 <srinivas_ramanatha@dell.com> - 1.3.4-6
- Fixed the incoherent init script problem by renaming the init script

* Thu Sep 03 2009 <srinivas_ramanatha@dell.com> - 1.3.4-5
- added the devel package to fit in all the development files 
- Made changes to the initscript not to start the service by default

* Thu Jul 02 2009 <ratliff@austin.ibm.com> - 1.3.4-4
- added build requires for flex, bison, cim-schema suggested by Sean Swehla
- added sfcbrepos directive to post section

* Thu Jun 18 2009 <ratliff@austin.ibm.com> - 1.3.4-3
- re-ordered the top so that the name comes first
- added the la files to the package list
- removed the smp flags from make because that causes a build break
- updated spec file to remove schema and require the cim-schema package
- change provides statement to cim-server as suggested by Matt Domsch
- updated to upstream version 1.3.4 which was released Jun 15 2009

* Thu Oct 09 2008 <ratliff@austin.ibm.com> - 1.3.2-2
- updated spec file based on comments from Srini Ramanatha as below:
- updated the Release line to add dist to be consistent with sblim-sfcc
- updated the source URL

* Wed Oct 08 2008 <ratliff@austin.ibm.com> - 1.3.2-1
- updated upstream version and added CFLAGS to configure to work 
- around https://sources.redhat.com/bugzilla/show_bug.cgi?id=6545

* Fri Aug 08 2008 <ratliff@austin.ibm.com> - 1.3.0-1
- updated buildrequires to require libcurl-devel rather than curl-devel
- removed requires to allow rpm to automatically generate the requires
- removed echo to stdout
- removed paranoia check around cleaning BuildRoot per Fedora MUST requirements
- changed group to supress rpmlint complaint
- added chkconfig to enable sfcb by default when it is installed
- added patch0 to enable 1.3.0 to build on Fedora 9

* Fri Feb 09 2007  <mihajlov@dyn-9-152-143-45.boeblingen.de.ibm.com> - 1.2.1-0
- Updated for 1.2.1 content, enabled SSL, indications

* Wed Aug 31 2005  <mihajlov@dyn-9-152-143-45.boeblingen.de.ibm.com> - 0.9.0b-0
- Support for man pages added
