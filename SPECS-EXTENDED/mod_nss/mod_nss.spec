Vendor:         Microsoft Corporation
Distribution:   Mariner
%{!?_httpd_apxs:       %{expand: %%global _httpd_apxs       %%{_sbindir}/apxs}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}}

Name: mod_nss
Version: 1.0.17
Release: 11%{?dist}
Summary: SSL/TLS module for the Apache HTTP server
License: ASL 2.0
URL: https://pagure.io/mod_nss/
Source: https://releases.pagure.org/mod_nss/%{name}-%{version}.tar.gz
BuildRequires: gcc
BuildRequires: nspr-devel, nss-devel
BuildRequires: httpd-devel, apr-devel, apr-util-devel
BuildRequires: pkgconfig
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: flex
BuildRequires: bison
# Needed for make check
BuildRequires: openssl
BuildRequires: python3-nose
BuildRequires: python3-requests >= 2.7.0
BuildRequires: python3-ndg_httpsclient
BuildRequires: hostname
BuildRequires: nss-tools
Requires: httpd-mmn
Requires(post): httpd, nss-tools
Requires: nss%{?_isa} >= 3.14.0.0
# Although the following change reverses the desire of Bugzilla Bug #601939, it
# was provided to suppress the dangling symlink warning of Bugzilla Bug #906089
# as exposed via 'rpmlint'.
Requires: %{_libdir}/libnssckbi.so

# Change configuration to not conflict with mod_ssl
Patch1: mod_nss-conf.patch
# Generate a password-less NSS database
Patch2: mod_nss-gencert.patch
# Add basic support for ssl_engine_set in mod_proxy
Patch3: mod_nss-ssl_engine_set.patch
# Fixes for unit tests against openssl 1.1.1a
Patch4: 0001-Fixes-to-unit-tests-so-they-pass-with-openssl-1.1.1a.patch
Patch5: 0002-Port-to-using-python-3-for-use-in-the-test-framework.patch
Patch6: 0003-Move-the-pool-and-hash-tables-for-SNI-into-mod_nss.c.patch

%description
The mod_nss module provides strong cryptography for the Apache Web
server via the Secure Sockets Layer (SSL) and Transport Layer
Security (TLS) protocols using the Network Security Services (NSS)
security library.

%prep
%setup -q
%patch1 -p1 -b .conf
%patch2 -p1 -b .gencert
%patch3 -p1 -b .sslengineset
%patch4 -p1
%patch5 -p1
%patch6 -p1

# Touch expression parser sources to prevent regenerating it
touch nss_expr_*.[chyl]

%build

CFLAGS="$RPM_OPT_FLAGS"
APXS=%{_httpd_apxs}

export CFLAGS APXS

NSPR_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nspr`
NSPR_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nspr`

NSS_INCLUDE_DIR=`/usr/bin/pkg-config --variable=includedir nss`
NSS_LIB_DIR=`/usr/bin/pkg-config --variable=libdir nss`

NSS_BIN=`/usr/bin/pkg-config --variable=exec_prefix nss`

autoreconf -i -f
%configure \
    --with-nss-lib=$NSS_LIB_DIR \
    --with-nss-inc=$NSS_INCLUDE_DIR \
    --with-nspr-lib=$NSPR_LIB_DIR \
    --with-nspr-inc=$NSPR_INCLUDE_DIR \
    --with-apr-config --enable-ecc

make %{?_smp_mflags} all

%install
# The install target of the Makefile isn't used because that uses apxs
# which tries to enable the module in the build host httpd instead of in
# the build root.
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf
mkdir -p $RPM_BUILD_ROOT%{_httpd_confdir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}/httpd/modules
mkdir -p $RPM_BUILD_ROOT%{_libexecdir}
mkdir -p $RPM_BUILD_ROOT%{_sbindir}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man8

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# httpd >= 2.4.x
mkdir -p $RPM_BUILD_ROOT%{_httpd_modconfdir}
sed -n /^LoadModule/p nss.conf > 10-nss.conf
sed -i /^LoadModule/d nss.conf
install -m 644 10-nss.conf $RPM_BUILD_ROOT%{_httpd_modconfdir}
%endif

install -m 644 gencert.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install -m 644 nss_pcache.8 $RPM_BUILD_ROOT%{_mandir}/man8/

install -m 644 nss.conf $RPM_BUILD_ROOT%{_httpd_confdir}

install -m 755 .libs/libmodnss.so $RPM_BUILD_ROOT%{_libdir}/httpd/modules/
install -m 755 nss_pcache $RPM_BUILD_ROOT%{_libexecdir}/
# Provide a compatibility link to prevent disruption of customized deployments.
#
#     NOTE:  This link may be deprecated in a future release of 'mod_nss'.
#
ln -s %{_libexecdir}/nss_pcache $RPM_BUILD_ROOT%{_sbindir}/nss_pcache
install -m 755 gencert $RPM_BUILD_ROOT%{_sbindir}/
ln -s ../../../%{_libdir}/libnssckbi.so $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/secmod.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/cert8.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/key3.db
touch $RPM_BUILD_ROOT%{_sysconfdir}/httpd/alias/install.log

perl -pi -e "s:$NSS_LIB_DIR:$NSS_BIN:" $RPM_BUILD_ROOT%{_sbindir}/gencert

%check
make check

%post
umask 077

if [ "$1" -eq 1 ] ; then
    if [ ! -e %{_sysconfdir}/httpd/alias/key3.db -a ! -e %{_sysconfdir}/httpd/alias/key4.db ]; then
        %{_sbindir}/gencert %{_sysconfdir}/httpd/alias > %{_sysconfdir}/httpd/alias/install.log 2>&1
        echo ""
        echo "%{name} certificate database generated."
        echo ""
        /bin/chgrp apache %{_sysconfdir}/httpd/alias/*.db
        /bin/chmod g+r %{_sysconfdir}/httpd/alias/*.db

    fi

    # We used to fix existing permissions and ownership here but it isn't needed anymore
    # since mod_nss will report permission/ownership issues on startup.
fi

%files
%doc README LICENSE docs/mod_nss.html
%{_mandir}/man8/*
%config(noreplace) %{_httpd_confdir}/nss.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/10-nss.conf
%endif
%{_libdir}/httpd/modules/libmodnss.so
%dir %{_sysconfdir}/httpd/alias/
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/httpd/alias/secmod.db
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/httpd/alias/cert8.db
%ghost %attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/httpd/alias/key3.db
%ghost %config(noreplace) %{_sysconfdir}/httpd/alias/install.log
%{_sysconfdir}/httpd/alias/libnssckbi.so
%{_libexecdir}/nss_pcache
%{_sbindir}/nss_pcache
%{_sbindir}/gencert

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.17-11
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Fri Jan 31 2020 Rob Crittenden <rcritten@redhat.com> - 1.0.17-10
- Ship the patch file

* Thu Jan 30 2020 Rob Crittenden <rcritten@redhat.com> - 1.0.17-9
- Move global SNI variables into mod_nss.c from mod_nss.h

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Rob Crittenden <rcritten@redhat.com> - 1.0.17-6
- Port tests to use python 3, drop python 2 dependencies

* Tue Feb 26 2019 Rob Crittenden <rcritten@redhat.com> - 1.0.17-5
- Fix tests to work against openssl 1.1.1a
- Add BuildRequires on gcc

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Apr 12 2018 Rob Crittenden <rcritten@redhat.com> - 1.0.17-2
- Add basic support for ssl_engine_set in mod_proxy (#1566511)

* Thu Mar 29 2018 Rob Crittenden <rcritten@redhat.com> - 1.0.17-1
- Update to upstream 1.0.17
- Correct URL and Source entries to point to pagure.io

* Wed Feb 14 2018 Rob Crittenden <rcritten@redhat.com> - 1.0.16-3
- Also check for sqlite NSS databases when deciding whether to generate a
  new certdb. (#1543379)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Rob Crittenden <rcritten@redhat.com> - 1.0.16-1
- Update to upstream 1.0.16
- Add bixon and flex to BR
- Add hostname and nss-tools to BR for make check

* Fri Oct 20 2017 Rob Crittenden <rcritten@redhat.com> - 1.0.14-6
- Don't fix up NSS db permissions on every install (#1288468)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Mar 14 2017 Rob Crittenden <rcritten@redhat.com> - 1.0.14-3
- Don't set remote user in fixup hook (#1431206)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Apr 15 2016 Rob Crittenden <rcritten@redhat.com> - 1.0.14-1
- Update to upstream 1.0.14
- Includes fix for CVE-2016-3099

* Mon Mar  7 2016 Rob Crittenden <rcritten@redhat.com> - 1.0.13-1
- Update to upstream 1.0.13

* Wed Feb 24 2016 Rob Crittenden <rcritten@redhat.com> - 1.0.12-3
- Use proper shell syntax to not generate /0 in gencert (#1311392)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct  2 2015 Rob Crittenden <rcritten@redhat.com> - 1.0.12-1
- Update to upstream 1.0.12

* Mon Aug 17 2015 Rob Crittenden <rcritten@redhat.com> - 1.0.11-5
- Fix logical AND in cipher string parsing CVE-2015-3277
  (#1243518)
- Add missing BuildRequires and some other changes so that
  make check passes

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Mar  1 2015 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.11-3
- Enable make check

* Fri Feb 27 2015 Rob Crittenden <rcritten@redhat.com> - 1.0.11-2
- Fix parallel build issue (#1196222)

* Tue Dec  2 2014 Rob Crittenden <rcritten@redhat.com> - 1.0.11-1
- Rebase to upstream mod_nss-1.0.11

* Fri Oct 17 2014 Rob Crittenden <rcritten@redhat.com> - 1.0.10-1
- Rebase to upstream mod_nss-1.0.10
- Changed the URL and Source directives to point to the fedorahosted
  site.

* Thu Aug 28 2014 Rob Crittenden <rcritten@redhat.com> - 1.0.9-2
- Add explicit BuildRequires for autoconf, automake and libtool

* Wed Aug 27 2014 Rob Crittenden <rcritten@redhat.com> - 1.0.9-1
- Rebase to upstream mod_nss-1.0.9

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 1.0.8-29
- fix _httpd_mmn expansion in absence of httpd-devel

* Tue Dec  3 2013 Rob Crittenden <rcritten@redhat.com> - 1.0.8-28
- Resolves: CVE-2013-4566, bz #1036940
- [mod_nss-nssverifyclient.patch]
- Bugzilla Bug #1037722 - CVE-2013-4566 mod_nss: incorrect handling of
  NSSVerifyClient in directory context [fedora-all] (rcritten)
- Bugzilla Bug #1037761 - mod_nss does not respect `NSSVerifyClient` in
  Directory (rcritten)
- [mod_nss-usecases.patch]
- Bugzilla Bug #1036940 - [DOC] making mod_nss work in FIPS mode (mharmsen)

* Tue Nov 12 2013 Joe Orton <jorton@redhat.com> - 1.0.8-26
- [mod_nss-SSLEngine-off.patch]
- Bugzilla Bug #1029043 - Implicit SSLEngine for 443 port breaks mod_nss
  configuration (jorton)
- [mod_nss-unused-filter_ctx.patch]
- Bugzilla Bug #1023237 - Remove unused variable 'filter_ctx' (mharmsen)

* Tue Nov 12 2013 Tomas Hoger <thoger@redhat.com> - 1.0.8-25
- [mod_nss-docs-fix.patch]
- Bugzilla Bug #1025316 - mod_nss: documentation formatting fixes

* Mon Oct 21 2013 Matthew Harmsen <mharmsen@redhat.com> - 1.0.8-24
- Bugzilla Bug #961471 - Port Downstream Patches Upstream (mharmsen)
- Add '--enable-ecc' option to %%configure line under %%build section of
  this spec file (mharmsen)
- Bumped version build/runtime requirements for NSPR and NSS (mharmsen)
- [mod_nss-PK11_ListCerts_2.patch]
- Bugzilla Bug #767802 - PK11_ListCerts called to retrieve all user
  certificates for every server (rcritten)
- [mod_nss-array_overrun.patch]
- Bugzilla Bug #1022717 - overrunning array when executing nss_pcache
  (rcritten)
- [mod_nss-clientauth.patch]
- Bugzilla Bug #1017675 - mod_nss: FakeBasicAuth authentication bypass
  [fedora-all] (rcritten)
- [mod_nss-no_shutdown_if_not_init_2.patch]
- Bugzilla Bug #1022722 - File descriptor leak after "service httpd reload"
  or httpd doesn't reload (rrelyea)
- [mod_nss-proxyvariables.patch]
- Bugzilla Bug #1022726 - mod_nss insists on Required value NSSCipherSuite
  not set. (mharmsen)
- [mod_nss-tlsv1_1.patch]
- Bugzilla Bug #979798 - current nss support TLS 1.1 so mod_nss should pick
  it up (mharmsen)
- Bugzilla Bug #979718 - mod_nss documentation should mention TLS 1.1
  (mharmsen)
- [mod_nss-sslmultiproxy_2.patch]
- Fixes Bugzilla Bug #1021469 - [RFE] Support ability to share mod_proxy with
  other SSL providers (jorton, mharmsen, nkinder, & rcritten)

* Tue Jul 30 2013 Joe Orton <jorton@redhat.com> - 1.0.8-23
- add dependency on httpd-mmn

* Wed Jul  3 2013 Matthew Harmsen <mharmsen@redhat.com> - 1.0.8-22
- Moved 'nss_pcache' from %%sbindir to %%libexecdir
  (provided compatibility link)

* Tue Jul  2 2013 Matthew Harmsen <mharmsen@redhat.com> - 1.0.8-21.1
- rpmlint mod_nss.spec
  0 packages and 1 specfiles checked; 0 errors, 0 warnings.
- rpmlint mod_nss-1.0.8-21.1 (SRPM)
  W: spelling-error %%description -l en_US nss -> ass, nos, nus
  1 packages and 0 specfiles checked; 0 errors, 1 warnings.
- rpmlint mod_nss-1.0.8-21.1 (RPM)
  W: spelling-error %%description -l en_US nss -> ass, nos, nus
  E: non-readable /etc/httpd/alias/cert8.db 0640L
  E: non-readable /etc/httpd/alias/secmod.db 0640L
  E: non-readable /etc/httpd/alias/key3.db 0640L
  1 packages and 0 specfiles checked; 3 errors, 1 warnings.
- rpmlint mod_nss-debuginfo-1.0.8-21.1 (RPM)
  W: spelling-error Summary(en_US) nss -> ass, nos, nus
  W: spelling-error %%description -l en_US nss -> ass, nos, nus
  1 packages and 0 specfiles checked; 0 errors, 2 warnings.

* Tue Jun 25 2013 Matthew Harmsen <mharmsen@redhat.com> - 1.0.8-21
- Bugzilla Bug #884115 - Package mod_nss-1.0.8-18.1.el7 failed RHEL7 RPMdiff
  testing
- Bugzilla Bug #906082 - mod_nss requires manpages for gencert and nss_pcache
- Bugzilla Bug #906089 - Fix dangling symlinks in mod_nss
- Bugzilla Bug #906097 - Correct RPM Parse Warning in mod_nss.spec
- Bugzilla Bug #948601 - Man page scan results for mod_nss

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-20.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-19.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 18 2012 Joe Orton <jorton@redhat.com> - 1.0.8-18.1
- fix build for RHEL7

* Fri Jun 15 2012 Rob Crittenden <rcritten@redhat.com> - 1.0.8-18
- Actually apply the patch to use memmove in place of memcpy since the
  buffers can overlap (#669118)

* Tue Jun 12 2012 Nathan Kinder <nkinder@redhat.com> - 1.0.8-17
- Port mod_nss to work with httpd 2.4

* Mon Apr 23 2012 Joe Orton <jorton@redhat.com> - 1.0.8-16
- packaging fixes/updates (#803072)

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar  7 2011 Rob Crittenden <rcritten@redhat.com> - 1.0.8-14
- Add Requires(post) for nss-tools, gencert needs it (#652007)

* Wed Mar  2 2011 Rob Crittenden <rcritten@redhat.com> - 1.0.8-13
- Lock around the pipe to nss_pcache for retrieving the token PIN
  (#677701)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Rob Crittenden <rcritten@redhat.com> - 1.0.8-11
- Use memmove in place of memcpy since the buffers can overlap (#669118)

* Wed Sep 29 2010 jkeating - 1.0.8-10
- Rebuilt for gcc bug 634757

* Thu Sep 23 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-9
- Revert mod_nss-wouldblock patch
- Reset NSPR error before calling PR_Read(). This should fix looping
  in #620856

* Fri Sep 17 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-8
- Fix hang when handling large POST under some conditions (#620856)

* Tue Jun 22 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-7
- Remove file Requires on libnssckbi.so (#601939)

* Fri May 14 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-6
- Ignore SIGHUP in nss_pcache (#591889).

* Thu May 13 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-5
- Use remote hostname set by mod_proxy to compare to CN in peer cert (#591224)

* Thu Mar 18 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-4
- Patch to add configuration options for new NSS negotiation API (#574187)
- Add (pre) for Requires on httpd so we can be sure the user and group are
  already available
- Add file Requires on libnssckbi.so so symlink can't fail
- Use _sysconfdir macro instead of /etc
- Set minimum level of NSS to 3.12.6

* Mon Jan 25 2010 Rob Crittenden <rcritten@redhat.com> - 1.0.8-3
- The location of libnssckbi moved from /lib[64] to /usr/lib[64] (556744)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Mar  2 2009 Rob Crittenden <rcritten@redhat.com> - 1.0.8-1
- Update to 1.0.8
- Add patch that fixes NSPR layer bug

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.7-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Aug 11 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.7-10
- fix license tag

* Mon Jul 28 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-9
- rebuild to bump NVR

* Mon Jul 14 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-8
- Don't force module de-init during the configuration stage (453508)

* Thu Jul 10 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-7
- Don't inherit the MP cache in multi-threaded mode (454701)
- Don't initialize NSS in each child if SSL isn't configured

* Wed Jul  2 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-6
- Update the patch for FIPS to include fixes for nss_pcache, enforce
  the security policy and properly initialize the FIPS token.

* Mon Jun 30 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-5
- Include patch to fix NSSFIPS (446851)

* Mon Apr 28 2008 Rob Crittenden <rcritten@redhat.com> - 1.0.7-4
- Apply patch so that mod_nss calls NSS_Init() after Apache forks a child
  and not before. This is in response to a change in the NSS softtokn code
  and should have always been done this way. (444348)
- The location of libnssckbi moved from /usr/lib[64] to /lib[64]
- The NSS database needs to be readable by apache since we need to use it
  after the root priviledges are dropped.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.7-3
- Autorebuild for GCC 4.3

* Thu Oct 18 2007 Rob Crittenden <rcritten@redhat.com> 1.0.7-2
- Register functions needed by mod_proxy if mod_ssl is not loaded.

* Fri Jun  1 2007 Rob Crittenden <rcritten@redhat.com> 1.0.7-1
- Update to 1.0.7
- Remove Requires for nss and nspr since those are handled automatically
  by versioned libraries
- Updated URL and Source to reference directory.fedoraproject.org

* Mon Apr  9 2007 Rob Crittenden <rcritten@redhat.com> 1.0.6-2
- Patch to properly detect the Apache model and set up NSS appropriately
- Patch to punt if a bad password is encountered
- Patch to fix crash when password.conf is malformatted
- Don't enable ECC support as NSS doesn't have it enabled (3.11.4-0.7)

* Mon Oct 23 2006 Rob Crittenden <rcritten@redhat.com> 1.0.6-1
- Update to 1.0.6

* Fri Aug 04 2006 Rob Crittenden <rcritten@redhat.com> 1.0.3-4
- Include LogLevel warn in nss.conf and use separate log files

* Fri Aug 04 2006 Rob Crittenden <rcritten@redhat.com> 1.0.3-3
- Need to initialize ECC certificate and key variables

* Fri Aug 04 2006 Jarod Wilson <jwilson@redhat.com> 1.0.3-2
- Use %%ghost for db files and install.log

* Tue Jun 20 2006 Rob Crittenden <rcritten@redhat.com> 1.0.3-1
- Initial build
