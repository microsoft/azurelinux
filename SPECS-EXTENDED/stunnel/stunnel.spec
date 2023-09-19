%bcond_with libwrap
# Do not generate provides for private libraries
%global __provides_exclude_from ^%{_libdir}/stunnel/.*$

Summary:        A TLS-encrypting socket wrapper
Name:           stunnel
Version:        5.70
Release:        1%{?dist}
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.stunnel.org/
Source0:        https://www.stunnel.org/downloads/stunnel-%{version}.tar.gz
Source2:        Certificate-Creation
Source3:        sfinger.xinetd
Source4:        stunnel-sfinger.conf
Source5:        pop3-redirect.xinetd
Source6:        stunnel-pop3s-client.conf
Source7:        stunnel@.service
Patch0:         stunnel-5.50-authpriv.patch
Patch1:         stunnel-5.61-systemd-service.patch
# Use cipher configuration from crypto-policies
#
# On Fedora, CentOS and RHEL, the system's crypto policies are the best
# source to determine which cipher suites to accept in TLS. On these
# platforms, OpenSSL supports the PROFILE=SYSTEM setting to use those
# policies. Change stunnel to default to this setting.
Patch3:         stunnel-5.69-system-ciphers.patch
Patch4:         stunnel-5.56-coverity.patch
Patch5:         stunnel-5.69-default-tls-version.patch
Patch6:         stunnel-5.56-curves-doc-update.patch
# Limit curves defaults in FIPS mode
Patch8:         stunnel-5.62-disabled-curves.patch
# build test requirements
BuildRequires:  %{_bindir}/nc
BuildRequires:  %{_bindir}/pod2html
BuildRequires:  %{_bindir}/pod2man
BuildRequires:  %{_sbindir}/lsof
BuildRequires:  /bin/ps
BuildRequires:  autoconf
BuildRequires:  automake
# util-linux is needed for rename
BuildRequires:  gcc
BuildRequires:  libtool
BuildRequires:  openssl-devel
BuildRequires:  pkgconfig
BuildRequires:  systemd
BuildRequires:  util-linux
%{?systemd_requires}
%if %{with libwrap}
BuildRequires:  tcp_wrappers-devel
%endif

%description
Stunnel is a socket wrapper which can provide TLS/SSL
(Transport Layer Security/Secure Sockets Layer) support
to ordinary applications. For example, it can be used in
conjunction with imapd to create a TLS secure IMAP server.

%prep
%autosetup -S gendiff -p1

# Fix the configure script output for FIPS mode and stack protector flag
# sed -i '/yes).*result: no/,+1{s/result: no/result: yes/;s/as_echo "no"/as_echo "yes"/};s/-fstack-protector/-fstack-protector-strong/' configure

# Fix a testcase with system-ciphers support
# sed -i '/client = yes/a \\  ciphers = PSK' tests/recipes/014_PSK_secrets

%build
#autoreconf -v
CFLAGS="%{optflags} -fPIC"; export CFLAGS
if pkg-config openssl ; then
	CFLAGS="$CFLAGS `pkg-config --cflags openssl`";
	LDFLAGS="`pkg-config --libs-only-L openssl`"; export LDFLAGS
fi
%configure --enable-fips --enable-ipv6 --with-ssl=%{_prefix} \
%if %{with libwrap}
--enable-libwrap \
%else
--disable-libwrap \
%endif
	CPPFLAGS="-UPIDFILE -DPIDFILE='\"%{_localstatedir}/run/stunnel.pid\"'"
make V=1 LDADD="-pie -Wl,-z,defs,-z,relro,-z,now"

%install
make install DESTDIR=%{buildroot}
# Move the translated man pages to the right subdirectories, and strip off the
# language suffixes.
#for lang in fr pl ; do
for lang in pl ; do
	mkdir -p %{buildroot}/%{_mandir}/${lang}/man8
	mv %{buildroot}/%{_mandir}/man8/*.${lang}.8* %{buildroot}/%{_mandir}/${lang}/man8/
	rename ".${lang}" "" %{buildroot}/%{_mandir}/${lang}/man8/*
done
mkdir srpm-docs
cp %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} srpm-docs

mkdir -p %{buildroot}%{_unitdir}
cp %{buildroot}%{_docdir}/stunnel/examples/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
cp %{SOURCE7} %{buildroot}%{_unitdir}/%{name}@.service


%check
# For unknown reason the 042_inetd test fails in Koji. The failure is not reproducible
# in local build.
rm tests/recipes/042_inetd
# We override the security policy as it is too strict for the tests.
OPENSSL_SYSTEM_CIPHERS_OVERRIDE=xyz_nonexistent_file
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE
OPENSSL_CONF=
export OPENSSL_CONF
make test || (for i in tests/logs/*.log ; do echo "$i": ; cat "$i" ; done)

%files
%{!?_licensedir:%global license %%doc}
%doc AUTHORS.md BUGS.md CREDITS.md PORTS.md README.md TODO.md
%doc tools/stunnel.conf-sample
%doc srpm-docs/*
%license COPY*
%lang(en) %doc doc/en/*
%lang(pl) %doc doc/pl/*
%{_bindir}/stunnel
%exclude %{_bindir}/stunnel3
%exclude %{_docdir}/stunnel
%{_libdir}/stunnel
%exclude %{_libdir}/stunnel/libstunnel.la
%{_mandir}/man8/stunnel.8*
%lang(pl) %{_mandir}/pl/man8/stunnel.8*
%dir %{_sysconfdir}/%{name}
%exclude %{_sysconfdir}/stunnel/*

%{_unitdir}/%{name}*.service

%post
/sbin/ldconfig
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart %{name}.service

%changelog
* Mon Sep 04 2023 Muhammad Falak R Wani <mwani@microsoft.com> - 5.70-1
- Upgrade version to address CVE-2021-20230
- Lint spec
- Verified License

* Fri Mar 26 2021 Henry Li <lihl@microsoft.com> - 5.56-8
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Change /usr/bin/lsof to /usr/sbin/lsof
- Change /usr/bin/ps to /bin/ps

* Thu Apr 16 2020 Sahana Prasad <sahana@redhat.com> - 5.56-7
- Updates documentation to specify that the option "curves" can be used in server mode only.

* Wed Apr 08 2020 Sahana Prasad <sahana@redhat.com> - 5.56-6
- Fixes default tls version patch to handle default values from OpenSSL crypto policies

* Mon Apr 06 2020 Sahana Prasad <sahana@redhat.com> - 5.56-5
- Removes warnings caused by the patch

* Mon Apr 06 2020 Sahana Prasad <sahana@redhat.com> - 5.56-4
- Adds default tls version patch to comply with OpenSSL crypto policies

* Tue Mar 31 2020 Sahana Prasad <sahana@redhat.com> - 5.56-3
- Adds coverity patch

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Sahana Prasad <sahana@redhat.com> - 5.56-1
- New upstream release 5.56

* Thu Sep 19 2019 Sahana Prasad <sahana@redhat.com> - 5.55-1
- New upstream release 5.55

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Tomáš Mráz <tmraz@redhat.com> - 5.50-1
- New upstream release 5.50

* Tue Jul 24 2018 Tomáš Mráz <tmraz@redhat.com> - 5.48-1
- New upstream release 5.48

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.46-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Tomáš Mráz <tmraz@redhat.com> - 5.46-1
- New upstream release 5.46

* Fri Mar  2 2018 Tomáš Mráz <tmraz@redhat.com> - 5.44-5
- Fix bind to localhost (patch backport by Christian Kujau) (#1542361)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.44-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 25 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 5.44-3
- Fix systemd executions/requirements

* Mon Jan 15 2018 Tomáš Mráz <tmraz@redhat.com> - 5.44-2
- Make the disablement of libwrap conditional

* Thu Jan 11 2018 Tomáš Mráz <tmraz@redhat.com> - 5.44-1
- New upstream release 5.44
- Disable libwrap support (#1518789)

* Tue Aug 22 2017 Tomáš Mráz <tmraz@redhat.com> - 5.42-1
- New upstream release 5.42
- Use the system cipher list by default (#1483967)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.41-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.41-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Apr 17 2017 Neal Gompa <ngompa@datto.com> - 5.41-1
- New upstream release 5.41

* Mon Mar 20 2017 Neal Gompa <ngompa@datto.com> - 5.40-1
- New upstream release 5.40
- Properly mark license files
- Rebase patches
- Eliminate unnecessary Provides
- Small spec cleanups and fixes

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.35-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Tomáš Mráz <tmraz@redhat.com> - 5.35-1
- New upstream release 5.35 with fix for bug #1358810

* Wed Jul 13 2016 Tomáš Mráz <tmraz@redhat.com> - 5.34-1
- New upstream release 5.34

* Wed Feb  3 2016 Tomáš Mráz <tmraz@redhat.com> - 5.30-1
- New upstream release 5.30
- Add generic stunnel@.service provided by Štefan Gurský (#1195742)

* Mon Jun 22 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.18-1
- New upstream release 5.18.
- Finally deleted the patch stunnel-5-sample.patch as upstream
  has merged those changes.
- Fixes patches as per new code changes.
- Fixed systemd service file related changes.

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Jun 8 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.17-1
- New upstream release 5.17.

* Fri May 22 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.16-1
- New upstream release 5.16.

* Mon Apr 27 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.15-1
- New upstream release 5.15.
- 1155977: Fixed upstream too so removed the associated patch
- Updates other patches too.

* Mon Mar 30 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.14-1
- New upstream release 5.14.

* Sun Mar 29 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.13-1
- New upstream release 5.13.

* Sat Mar 28 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.12-1
- New upstream release 5.12.

* Fri Mar 27 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.11-1
- New upstream release 5.11.

* Wed Jan 28 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.10-1
- New upstream release 5.10.

* Thu Jan 8 2015 Avesh Agarwal <avagarwa@redhat.com> - 5.09-1
- 1163349: New upstream release 5.09.

* Thu Dec 11 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.08-1
- 1163349: New upstream release 5.08

* Sun Nov 23 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.08b6-1
- 1163349: New upstream beta release 5.08b6
- Fixed incorrect reporting of fips status in configure.ac
  at compile time, requires autoconf automake at buildtime
- Fixed default OpenSSL directory issue by using with-ssl
- Updates local patches
- 1155977: Fixes man page issues

* Tue Nov 04 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.07-1
- New upstream release 5.07

* Fri Oct 17 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.06-1
- New upstream release 5.06
- Addresses Poodle security issue

* Wed Oct 8 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.05b5-1
- rhbz #1144393: New upstream beta release
- systemd socket activation support

* Fri Sep 26 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.04-2
- Fixes packaging issues mentioned in rhbz#226439

* Mon Sep 22 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.04-1
- New upstream realease 5.04
- Updates local patches so that they apply cleanly to
  avoud hunk errors

* Thu Aug 28 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.03-1
- New upstream realease 5.03

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.02-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 14 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.02-1
- rhbz#1108818: New upstream realease 5.02
- Updated local patches
- The rhbz#530950 is tested and seems to work. STRLEN has
  been no longer allocated statically since 4.36 version.
  So it is possible that this bz might have got fixed
  around 4.36 release.
- Fixes rpmlint errors

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Apr 28 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.01-2
- Integration with systemd.
- Spec file clean up
- Patched stunnel systemd unit file to have dependency on
  network.target.
- rhbz#455815: Packaged systemd service file
- rhbz#782535: Fixed private tmp issue.
- rhbz#995831: Fixed wrong encoding of french man page.

* Thu Apr 17 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.01-1
- New upstream realease 5.01
- Supports OpenSSL DLLs 1.0.1g.
- Fixes to take care of OpenSSL,s TLS heartbeat
  read overrun (CVE-2014-0160).

* Fri Mar 7 2014 Avesh Agarwal <avagarwa@redhat.com> - 5.00-1
- New upstream realease 5.00
- Updated local patches.
- Fix for CVE-2014-0016
- Fixed changelog date errors
- Fixes rhbz #1006819

* Mon Aug 5 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.56-3
- Ftp mirrors for NA does not work, so changing source code
  URLs to the correct ones.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.56-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 1 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.56-1
- New upstream realease 4.56.
- Updated local patches.
- Fixed upstream URL in spec file.
- Sourced URL of sha256 hash file in spec file.

* Tue Mar 26 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.55-2
- Resolves: 927841 

* Mon Mar 4 2013 Avesh Agarwal <avagarwa@redhat.com> - 4.55-1
- New upstream realease 4.55
- Updated local patches
- enabled fips mode
- Fixed for pod2man as it build-requires perl-podlators

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.54-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec 10 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.54-2
- 884183: support for full relro.

* Tue Oct 16 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.54-1
- New upstream realease 4.54
- Updated local patches

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon May 14 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.53-1
- New upstream realease 4.53
- Updated local patches

* Tue Mar 6 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.52-1
- New upstream realease 4.52
- Updated local patches

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jan 3 2012 Avesh Agarwal <avagarwa@redhat.com> - 4.50-1
- New upstream realease 4.50
- Updated local patches

* Tue Sep 20 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.44-1
- New upstream realease 4.44
- Updated local patches

* Fri Aug 19 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.42-1
- New upstream realease 4.42
- Updated local patches
- Fixes #732069

* Mon Aug 1 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.41-1
- New upstream realease 4.41
- Updated local patches to match the new release

* Tue Jun 28 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.37-1
- New upstream realease 4.37
- Updated local patches to match the new release

* Mon Apr 4 2011 Avesh Agarwal <avagarwa@redhat.com> - 4.35-1
- New upstream realease 4.35
- Updated authpriv and sample patches to match the new release

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.34-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 4 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.34-1
- New upstream realease 4.34
- Updated authpriv and sample patches to match the new release

* Wed Apr 7 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.33-1
- New upstream realease 4.33
- Updated authpriv and sample patches to match the new release
- Addresses bz 580117 (inted mode support issue)

* Mon Mar 29 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.32-1
- New upstream realease 4.32
- Updated authpriv and sample patches to match the new release

* Tue Feb 16 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.31-1
- New upstream realease 4.31
- Updated authpriv and sample patches to match the new release

* Tue Jan 26 2010 Avesh Agarwal <avagarwa@redhat.com> - 4.30-1
- New upstream realease 4.30
- Updated authpriv and sample patches for the new release

* Wed Dec 09 2009 Avesh Agarwal <avagarwa@redhat.com> - 4.29-1
- New upstream realease 4.29
- Updated authpriv and sample patches for the new release
- Modified spec file to include dist tag

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 4.27-5
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.27-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May  3 2009 Miloslav Trmač <mitr@redhat.com> - 4.27-3
- Fix the previous patch.

* Wed Apr 29 2009 Miloslav Trmač <mitr@redhat.com> - 4.27-2
- Avoid aliasing undefined by ISO C

* Thu Apr 16 2009 Miloslav Trmač <mitr@redhat.com> - 4.27-1
- Update to stunnel-4.27.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 4.26-2
- disable openssl upstream fips mode

* Mon Sep 22 2008 Miloslav Trmač <mitr@redhat.com> - 4.26-1
- Update to stunnel-4.26.

* Sun Jun  8 2008 Miloslav Trmač <mitr@redhat.com> - 4.25-2
- Use a clearer error message if the service name is unknown in "accept"
  Resolves: #450344

* Mon Jun  2 2008 Miloslav Trmač <mitr@redhat.com> - 4.25-1
- Update to stunnel-4.25

* Tue May 20 2008 Miloslav Trmač <mitr@redhat.com> - 4.24-2
- Drop stunnel3
  Resolves: #442842

* Mon May 19 2008 Miloslav Trmač <mitr@redhat.com> - 4.24-1
- Update to stunnel-4.24

* Fri Mar 28 2008 Miloslav Trmač <mitr@redhat.com> - 4.22-1
- Update to stunnel-4.22

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.20-6
- Autorebuild for GCC 4.3

* Tue Dec  4 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-5
- Rebuild with openssl-0.9.8g

* Tue Oct 16 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-4
- Revert the port to NSS, wait for NSS-based stunnel 5.x instead
  Resolves: #301971
- Mark localized man pages with %%lang (patch by Ville Skyttä)
  Resolves: #322281

* Tue Aug 28 2007 Miloslav Trmač <mitr@redhat.com> - 4.20-3.nss
- Port to NSS

* Mon Dec  4 2006 Miloslav Trmac <mitr@redhat.com> - 4.20-2
- Update BuildRequires for the separate tcp_wrappers-devel package

* Thu Nov 30 2006 Miloslav Trmac <mitr@redhat.com> - 4.20-1
- Update to stunnel-4.20

* Sat Nov 11 2006 Miloslav Trmac <mitr@redhat.com> - 4.19-1
- Update to stunnel-4.19

* Wed Oct 25 2006 Miloslav Trmac <mitr@redhat.com> - 4.18-1
- Update to stunnel-4.18
- Remove unused stunnel.cnf from the src.rpm
- Fix some rpmlint warnings

* Fri Aug 18 2006 Jesse Keating <jkeating@redhat.com> - 4.15-2
- rebuilt with latest binutils to pick up 64K -z commonpagesize on ppc*
  (#203001)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 4.15-1.1
- rebuild

* Sat Mar 18 2006 Miloslav Trmac <mitr@redhat.com> - 4.15-1
- Update to stunnel-4.15

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.14-3.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.14-3.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 31 2006 Miloslav Trmac <mitr@redhat.com> - 4.14-3
- Use pthread threading to fix crash on x86_64 (#179236)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov  9 2005 Miloslav Trmac <mitr@redhat.com> - 4.14-2
- Rebuild with newer openssl

* Thu Nov  3 2005 Miloslav Trmac <mitr@redhat.com> - 4.14-1
- Update to stunnel-4.14
- Override changed default pid file location, keep it in %%{_localstatedir}/run

* Sat Oct 22 2005 Miloslav Trmac <mitr@redhat.com> - 4.13-1
- Update to stunnel-4.13

* Fri Sep 30 2005 Miloslav Trmac <mitr@redhat.com> - 4.12-1
- Update to stunnel-4.12

* Thu Sep 22 2005 Miloslav Trmac <mitr@redhat.com> - 4.11-2
- Enable IPv6 (#169050, patch by Peter Bieringer)
- Don't ship another copy of man pages in HTML

* Tue Jul 12 2005 Miloslav Trmac <mitr@redhat.com> - 4.11-1
- Update to stunnel-4.11
- Fix int/size_t mismatches in stack_info ()
- Update Certificate-Creation for /etc/pki

* Wed Jun  1 2005 Miloslav Trmac <mitr@redhat.com> - 4.10-2
- Fix inetd mode
- Remove unnecessary Requires: and BuildRequires:
- Clean up the spec file

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 4.10-1
- update to 4.10

* Tue Apr 26 2005 Nalin Dahyabhai <nalin@redhat.com> 4.08-2
- add buildprereqs on libtool, util-linux; change textutils/fileutils dep to
  coreutils (#133961)

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 4.08-1
- update to 4.08
- build stunnel as a PIE binary

* Mon Nov 22 2004 Miloslav Trmac <mitr@redhat.com> - 4.05-4
- Convert man pages to UTF-8

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu May 27 2004 Nalin Dahyabhai <nalin@redhat.com> 4.05-2
- move the sample configuration to %%doc, it shouldn't be used as-is (#124373)

* Thu Mar 11 2004 Nalin Dahyabhai <nalin@redhat.com> 4.05-1
- update to 4.05

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Aug  7 2003 Elliot Lee <sopwith@redhat.com> 4.04-6
- Fix libtool

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Mar 21 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-4
- fix xinetd configuration samples

* Mon Feb 10 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-3
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Nalin Dahyabhai <nalin@redhat.com> 4.04-1
- update to 4.04

* Tue Jan  7 2003 Nalin Dahyabhai <nalin@redhat.com> 4.03-1
- use pkgconfig for information about openssl, if available

* Fri Jan  3 2003 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.03

* Mon Oct 21 2002 Nalin Dahyabhai <nalin@redhat.com> 4.02-1
- update to 4.02

* Fri Oct  4 2002 Nalin Dahyabhai <nalin@redhat.com> 4.00-1
- don't create a dummy cert

* Wed Sep 25 2002 Nalin Dahyabhai <nalin@redhat.com>
- update to 4.00
- remove textutils and fileutils as buildreqs, add automake/autoconf

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri May 17 2002 Nalin Dahyabhai <nalin@redhat.com> 3.22-2
- rebuild in new environment

* Wed Jan  2 2002 Nalin Dahyabhai <nalin@redhat.com> 3.22-1
- update to 3.22, correcting a format-string vulnerability

* Wed Oct 31 2001 Nalin Dahyabhai <nalin@redhat.com> 3.21a-1
- update to 3.21a

* Tue Aug 28 2001 Nalin Dahyabhai <nalin@redhat.com> 3.20-1
- log using LOG_AUTHPRIV facility by default (#47289)
- make permissions on stunnel binary 0755
- implicitly trust certificates in %%{_datadir}/ssl/trusted (#24034)

* Fri Aug 10 2001 Nalin Dahyabhai <nalin@redhat.com> 3.19-1
- update to 3.19 to avoid problems with stunnel being multithreaded, but
  tcp wrappers not being thrad-safe

* Mon Jul 30 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.17

* Mon Jul 23 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.16

* Mon Jul 16 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.15
- enable tcp-wrappers support

* Tue May 29 2001 Nalin Dahyabhai <nalin@redhat.com>
- remove explicit requirement on openssl (specific version isn't enough,
  we have to depend on shared library version anyway)

* Fri Apr 27 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.14

* Mon Mar 26 2001 Preston Brown <pbrown@redhat.com>
- depend on make (#33148)

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb  6 2001 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.13 to get pthread, OOB, 64-bit fixes
- don't need sdf any more

* Thu Dec 28 2000 Nalin Dahyabhai <nalin@redhat.com>
- pull in sdf to build the man page (#22892)

* Fri Dec 22 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.11
- chuck the SIGHUP patch (went upstream)
- chuck parts of the 64-bit clean patch (went upstream)

* Thu Dec 21 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.10
- more 64-bit clean changes, hopefully the last bunch

* Wed Dec 20 2000 Nalin Dahyabhai <nalin@redhat.com>
- change piddir from the default /var/stunnel to /var/run
- clean out pid file on SIGHUP

* Fri Dec 15 2000 Nalin Dahyabhai <nalin@redhat.com>
- update to 3.9 to get a security fix

* Wed Oct 25 2000 Matt Wilson <msw@redhat.com>
- change all unsigned longs to u_int32_t when dealing with network
  addresses

* Fri Aug 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- make stunnel.pem also be (missingok)

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- move to Applications/Internet group
- clean up %%post script
- make stunnel.pem %%ghost %%config(noreplace)
- provide a sample file for use with xinetd

* Thu Jun  8 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS compliance fixes
- modify defaults

* Tue Mar 14 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.8
- do not create certificate if one already exists

* Mon Feb 21 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- update to 3.7
- add patch to find /usr/share/ssl
- change some perms

* Sat Oct 30 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Modify spec file to match Red Hat standards

* Thu Aug 12 1999 Damien Miller <damien@ibs.com.au>
- Updated to 3.4a
- Patched for OpenSSL 0.9.4
- Cleaned up files section

* Sun Jul 11 1999 Damien Miller <dmiller@ilogic.com.au>
- Updated to 3.3

* Sat Nov 28 1998 Damien Miller <dmiller@ilogic.com.au>
- Initial RPMification
