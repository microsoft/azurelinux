Vendor:         Microsoft Corporation
Distribution:   Azure Linux
%{!?_httpd_apxs: %{expand: %%global _httpd_apxs %%{_sbindir}/apxs}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}
# /etc/httpd/conf.d with httpd < 2.4 and defined as /etc/httpd/conf.modules.d with httpd >= 2.4
%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_confdir:    %{expand: %%global _httpd_confdir    %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir:    %{expand: %%global _httpd_moddir    %%{_libdir}/httpd/modules}}

%bcond_without mlogc

Summary: Security module for the Apache HTTP Server
Name: mod_security
Version: 2.9.4
Release: 1%{?dist}
License: ASL 2.0
URL: https://www.modsecurity.org/
Source: https://github.com/SpiderLabs/ModSecurity/releases/download/v%{version}/modsecurity-%{version}.tar.gz
Source1: mod_security.conf
Source2: 10-mod_security.conf
Source3: modsecurity_localrules.conf
Patch0: modsecurity-2.9.3-lua-54.patch
Patch1: modsecurity-2.9.3-apulibs.patch
Patch2: mod_security-2.9.3-remote-rules-timeout.patch

Requires: httpd httpd-mmn = %{_httpd_mmn}
Requires(pre): httpd-filesystem

BuildRequires: gcc, make, autoconf, automake, libtool
BuildRequires: httpd-devel
BuildRequires: perl-generators
BuildRequires: pkgconfig(libcurl)
BuildRequires: pkgconfig(libpcre)
BuildRequires: pkgconfig(libxml-2.0)
BuildRequires: pkgconfig(lua)

# Workarround for EL6
%if 0%{?el6}
BuildRequires: yajl-devel
%else
BuildRequires: pkgconfig(yajl)
%endif


%description
ModSecurity is an open source intrusion detection and prevention engine
for web applications. It operates embedded into the web server, acting
as a powerful umbrella - shielding web applications from attacks.

%if %{with mlogc}
%package        mlogc
Summary:        ModSecurity Audit Log Collector
Requires:       mod_security
Requires(pre):  httpd-filesystem

%description mlogc
This package contains the ModSecurity Audit Log Collector.
%endif

%prep
%autosetup -p1 -n modsecurity-%{version}

%build
./autogen.sh
%configure --enable-pcre-match-limit=1000000 \
           --enable-pcre-match-limit-recursion=1000000 \
           --with-apxs=%{_httpd_apxs} \
           --with-yajl \
           --disable-static

# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{_smp_mflags}

%check
# Test suite does not start because of some issue in shipped httpd config (fix upstreamed in PR #669)
# After the fix, the test suite starts but still fails
#make test
#make test-regression

%install
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_httpd_moddir}
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/activated_rules
install -d %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/local_rules

install -m0755 apache2/.libs/mod_security2.so %{buildroot}%{_httpd_moddir}/mod_security2.so

%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
# 2.4-style
install -Dp -m0644 %{SOURCE2} %{buildroot}%{_httpd_modconfdir}/10-mod_security.conf
install -Dp -m0644 %{SOURCE1} %{buildroot}%{_httpd_confdir}/mod_security.conf
sed  -i 's/Include/IncludeOptional/'  %{buildroot}%{_httpd_confdir}/mod_security.conf
%else
# 2.2-style
install -d -m0755 %{buildroot}%{_httpd_confdir}
cat %{SOURCE2} %{SOURCE1} > %{buildroot}%{_httpd_confdir}/mod_security.conf
%endif
install -m 700 -d $RPM_BUILD_ROOT%{_localstatedir}/lib/%{name}

# Local rules example
install -Dp -m0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/modsecurity.d/local_rules/

# mlogc
%if %{with mlogc}
install -d %{buildroot}%{_localstatedir}/log/mlogc
install -d %{buildroot}%{_localstatedir}/log/mlogc/data
install -m0755 mlogc/mlogc %{buildroot}%{_bindir}/mlogc
install -m0755 mlogc/mlogc-batch-load.pl %{buildroot}%{_bindir}/mlogc-batch-load
install -m0644 mlogc/mlogc-default.conf %{buildroot}%{_sysconfdir}/mlogc.conf
%endif


%files
%license LICENSE
%doc CHANGES README.* NOTICE
%{_httpd_moddir}/mod_security2.so
%config(noreplace) %{_httpd_confdir}/*.conf
%if "%{_httpd_modconfdir}" != "%{_httpd_confdir}"
%config(noreplace) %{_httpd_modconfdir}/*.conf
%endif
%dir %{_sysconfdir}/httpd/modsecurity.d
%dir %{_sysconfdir}/httpd/modsecurity.d/activated_rules
%dir %{_sysconfdir}/httpd/modsecurity.d/local_rules
%config(noreplace) %{_sysconfdir}/httpd/modsecurity.d/local_rules/*.conf
%attr(770,apache,root) %dir %{_localstatedir}/lib/%{name}

%if %{with mlogc}
%files mlogc
%doc mlogc/INSTALL
%attr(0640,root,apache) %config(noreplace) %{_sysconfdir}/mlogc.conf
%attr(0755,root,root) %dir %{_localstatedir}/log/mlogc
%attr(0770,root,apache) %dir %{_localstatedir}/log/mlogc/data
%attr(0755,root,root) %{_bindir}/mlogc
%attr(0755,root,root) %{_bindir}/mlogc-batch-load
%endif

%changelog
* Fri Mar 04 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.4-1
- Updating to version 2.9.4 using Fedora 36 spec (license: MIT) for guidance.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.9.3-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Dec 09 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 2.9.3-1
- Update to 2.9.3

* Fri Nov 16 2018 Joe Orton <jorton@redhat.com> - 2.9.2-7
- Requires(pre): httpd-filesystem to ensure apache user exists
- enable mlogc everywhere, use buildcond to disable

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 18 2018 Athmane Madjoudj <athmane@fedoraproject.org> - 2.9.2-5
- Add gcc and make as BR (minimal buildroot change)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 21 2017 Athmane Madjoudj <athmane@fedoraproject.org> - 2.9.2-1
- Update to 2.9.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Mar 09 2016 Athmane Madjoudj <athmane@fedoraproject.org> 2.9.1-1
- Update to final 2.9.1
- Minor spec fix.

* Tue Mar 08 2016 Athmane Madjoudj <athmane@fedoraproject.org> 2.9.1-0.1.rc1
- Add workaround for el6

* Tue Mar 08 2016 Athmane Madjoudj <athmane@fedoraproject.org> 2.9.1-0.rc1
- Update to 2.9.1-rc1
- Remove upstreamed patch

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Oct 02 2015 Athmane Madjoudj <athmane@fedoraproject.org> 2.9.0-5
- Update BuildRequires using pkgconfig name schema

* Tue Sep 01 2015 Athmane Madjoudj <athmane@fedoraproject.org>  2.9.0-4
- Add yajl support

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Feb 13 2015 Athmane Madjoudj <athmane@fedoraproject.org> 2.9.0-2
- Remove curl version dep. since it no longer required

* Fri Feb 13 2015 Athmane Madjoudj <athmane@fedoraproject.org>  2.9.0-1
- Update to 2.9.0
- Remove backported patch
- Add patch to fix lua 5.3 build issue (PR #837)

* Tue Nov 04 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.8.0-7
- Make sure mod_security is built with correct curl version

* Mon Nov 03 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.8.0-6
- Changes the default SSL version to TLS 1.2 since SSLv3 is vulnerable to poodle

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Aug 15 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.8.0-4
- Add support for user-provided configurations and rules (rhbz #1129843)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 16 2014  Athmane Madjoudj <athmane@fedoraproject.org> 2.8.0-1
- Update to 2.8.0 Final

* Thu Apr 03 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.8.0-0.rc1
- Update to 2.8.0-RC1

* Tue Mar 04 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.7-6
- Fix status code in the configuration file (upstream PR #666)

* Sat Mar 01 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.7-5
- Fix rpmlint warnings

* Thu Feb 27 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.7-4
- Add check section

* Sat Feb 22 2014 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.7-3
- Fix bogus date in chanelog

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> - 2.7.7-2
- fix _httpd_mmn expansion in absence of httpd-devel

* Thu Dec 19 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.7-1
- Update to 2.7.7
- Fix the spec file since upstream fixed the bugs reported.

* Tue Dec 17 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.6-2
- Add autotools deps

* Tue Dec 17 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.6-1
- Update to 2.7.6
- Fix spec since upstream will only provide tarball via Github

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.7.5-2
- Perl 5.18 rebuild

* Tue Jul 30 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.5-1
- Update to 2.7.5

* Thu Jul 18 2013 Petr Pisar <ppisar@redhat.com> - 2.7.4-2
- Perl 5.18 rebuild

* Tue May 28 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.4-1
- Update to 2.7.4
- Drop non required patch

* Tue May 28 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.3-2
- Fix NULL pointer dereference (DoS, crash) (CVE-2013-2765) (RHBZ #967615)
- Fix a possible memory leak.

* Sat Mar 30 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.3-1
- Update to 2.7.3

* Fri Jan 25 2013 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.2-1
- Update to 2.7.2
- Update source url in the spec.

* Thu Nov 22 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.1-5
- Use conditional for loading mod_unique_id (rhbz #879264)
- Fix syntax errors on httpd 2.4.x by using IncludeOptional (rhbz #879264, comment #2)

* Mon Nov 19 2012 Peter Vrabec <pvrabec@redhat.com> 2.7.1-4
- mlogc subpackage is not provided on RHEL7

* Thu Nov 15 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.1-3
- Add some missing directives RHBZ #569360
- Fix multipart/invalid part ruleset bypass issue (CVE-2012-4528)
  (RHBZ #867424, #867773, #867774)

* Thu Nov 15 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.1-2
- Fix mod_security.conf

* Thu Nov 15 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.1-1
- Update to 2.7.1
- Remove libxml2 build patch (upstreamed)
- Update spec since upstream moved to github

* Thu Oct 18 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.0-2
- Add a patch to fix failed build against libxml2 >= 2.9.0

* Wed Oct 17 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.7.0-1
- Update to 2.7.0

* Fri Sep 28 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.6.8-1
- Update to 2.6.8

* Wed Sep 12 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.6.7-2
- Re-add mlogc sub-package for epel (#856525)
 
* Sat Aug 25 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.6.7-1
- Update to 2.6.7

* Sat Aug 25 2012 Athmane Madjoudj <athmane@fedoraproject.org> 2.6.7-1
- Update to 2.6.7

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Peter Vrabec <pvrabec@redhat.com> - 2.6.6-2
- mlogc subpackage is not provided on RHEL
 
* Thu Jun 21 2012 Peter Vrabec <pvrabec@redhat.com> - 2.6.6-1
- upgrade

* Mon May  7 2012 Joe Orton <jorton@redhat.com> - 2.6.5-3
- packaging fixes

* Fri Apr 27 2012 Peter Vrabec <pvrabec@redhat.com> 2.6.5-2
- fix license tag

* Thu Apr 05 2012 Peter Vrabec <pvrabec@redhat.com> 2.6.5-1
- upgrade & move rules into new package mod_security_crs

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 2.5.13-3
- Rebuild against PCRE 8.30
- Do not install non-existing files

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue  May 3 2011 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.13-1
- Newer upstream version

* Wed Jun 30 2010 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.12-3
- Fix log dirs and files ordering per bz#569360

* Thu Apr 29 2010 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.12-2
- Fix SecDatadir and minimal config per bz #569360

* Sat Feb 13 2010 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.12-1
- Update to latest upstream release
- SECURITY: Fix potential rules bypass and denial of service (bz#563576)

* Fri Nov 6 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.10-2
- Fix rules and Apache configuration (bz#533124)

* Thu Oct 8 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> - 2.5.10-1
- Upgrade to 2.5.10 (with Core Rules v2)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Mar 12 2009 Michael Fleming <mfleming+rpm@thatfleminggent.com> 2.5.9-1
- Update to upstream release 2.5.9
- Fixes potential DoS' in multipart request and PDF XSS handling

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 29 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.5.7-1
- Update to upstream 2.5.7
- Reinstate mlogc

* Sat Aug 2 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.5.6-1
- Update to upstream 2.5.6
- Remove references to mlogc, it no longer ships in the main tarball.
- Link correctly vs. libxml2 and lua (bz# 445839)
- Remove bogus LoadFile directives as they're no longer needed.

* Sun Apr 13 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.7-1
- Update to upstream 2.1.7

* Sat Feb 23 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.6-1
- Update to upstream 2.1.6 (Extra features including SecUploadFileMode)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.1.5-3
- Autorebuild for GCC 4.3

* Sun Jan 27 2008 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.5-2
- Update to 2.1.5 (bz#425986)
- "blocking" -> "optional_rules" per tarball ;-)


* Thu Sep  13 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.3-1
- Update to 2.1.3
- Update License tag per guidelines.

* Mon Sep  3 2007 Joe Orton <jorton@redhat.com> 2.1.1-3
- rebuild for fixed 32-bit APR (#254241)

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.1.1-2
- Rebuild for selinux ppc32 issue.

* Tue Jun 19 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.1-1
- New upstream release
- Drop ASCIIZ rule (fixed upstream)
- Re-enable protocol violation/anomalies rules now that REQUEST_FILENAME
  is fixed upstream.

* Sun Apr 1 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-3
- Automagically configure correct library path for libxml2 library.
- Add LoadModule for mod_unique_id as the logging wants this at runtime

* Mon Mar 26 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-2
- Fix DSO permissions (bz#233733)

* Tue Mar 13 2007 Michael Fleming <mfleming+rpm@enlartenment.com> 2.1.0-1
- New major release - 2.1.0
- Fix CVE-2007-1359 with a local rule courtesy of Ivan Ristic
- Addition of core ruleset
- (Build)Requires libxml2 and pcre added.

* Sun Sep 3 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.4-2
- Rebuild
- Fix minor longstanding braino in included sample configuration (bz #203972)

* Mon May 15 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.4-1
- New upstream release

* Tue Apr 11 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.3-1
- New upstream release
- Trivial spec tweaks

* Wed Mar 1 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-3
- Bump for FC5

* Fri Feb 10 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-2
- Bump for newer gcc/glibc

* Wed Jan 18 2006 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.2-1
- New upstream release

* Fri Dec 16 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.1-2
- Bump for new httpd

* Thu Dec 1 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9.1-1
- New release 1.9.1 

* Wed Nov 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.9-1
- New stable upstream release 1.9

* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-4
- Add Requires: httpd-mmn to get the appropriate "module magic" version
  (thanks Ville Skytta)
- Disabled an overly-agressive rule or two..

* Sat Jul 9 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-3
- Correct Buildroot
- Some sensible and safe rules for common apps in mod_security.conf

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-2
- Don't strip the module (so we can get a useful debuginfo package)

* Thu May 19 2005 Michael Fleming <mfleming+rpm@enlartenment.com> 1.8.7-1
- Initial spin for Extras
