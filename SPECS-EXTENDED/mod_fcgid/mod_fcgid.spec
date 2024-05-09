Vendor:         Microsoft Corporation
Distribution:   Azure Linux

%global httpd24 1
%global rundir /run
%global rundir_tmpfs 1
%global systemd_units systemd

Name:		mod_fcgid
Version:	2.3.9
Release:	21%{?dist}
Summary:	FastCGI interface module for Apache 2
License:	ASL 2.0
URL:		https://httpd.apache.org/mod_fcgid/
Source0:	https://www.apache.org/dist/httpd/mod_fcgid/mod_fcgid-%{version}.tar.bz2
Source1:	fcgid.conf
Source2:	mod_fcgid-2.1-README.RPM
Source3:	mod_fcgid-2.1-README.SELinux
Source4:	mod_fcgid-tmpfs.conf
Source5:	fcgid24.conf
Patch0:		mod_fcgid-2.3.4-fixconf-shellbang.patch
BuildRequires:	coreutils
BuildRequires:	gcc
BuildRequires:	httpd-devel >= 2.0
BuildRequires:	make
BuildRequires:	pkgconfig
BuildRequires:	sed
BuildRequires:	systemd-rpm-macros
Requires:	httpd-mmn
# %%systemd_units needed for ownership of %%{_tmpfilesdir}
%if %{rundir_tmpfs}
Requires:	%{systemd_units}
%endif

%description
mod_fcgid is a binary-compatible alternative to the Apache module mod_fastcgi.
mod_fcgid has a new process management strategy, which concentrates on reducing
the number of fastcgi servers, and kicking out corrupt fastcgi servers as soon
as possible.

%prep
%setup -q
cp -p %{SOURCE1} fcgid.conf
cp -p %{SOURCE2} README.RPM
cp -p %{SOURCE3} README.SELinux
cp -p %{SOURCE5} fcgid24.conf


%build
APXS=%{_httpd_apxs} ./configure.apxs
make

%install
make DESTDIR=%{buildroot} MKINSTALLDIRS="mkdir -p" install
%if %{httpd24}
mkdir -p %{buildroot}{%{_httpd_confdir},%{_httpd_modconfdir}}
echo "LoadModule fcgid_module modules/mod_fcgid.so" > %{buildroot}%{_httpd_modconfdir}/10-fcgid.conf
install -D -m 644 fcgid24.conf %{buildroot}%{_httpd_confdir}/fcgid.conf
%else
install -D -m 644 fcgid.conf %{buildroot}%{_httpd_confdir}/fcgid.conf
%endif
install -d -m 755 %{buildroot}%{rundir}/mod_fcgid

# Include the manual as %%doc, don't need it elsewhere
%if %{httpd24}
rm -rf %{buildroot}%{_httpd_contentdir}/manual
%else
rm -rf %{buildroot}%{_var}/www/manual
%endif

# Make sure %%{rundir}/mod_fcgid exists at boot time for systems
# with %%{rundir} on tmpfs (#656625)
%if %{rundir_tmpfs}
install -d -m 755 %{buildroot}%{_tmpfilesdir}
install -p -m 644 %{SOURCE4} %{buildroot}%{_tmpfilesdir}/mod_fcgid.conf
%endif

%files
%license LICENSE-FCGID
%doc README.RPM README.SELinux
# mod_fcgid.html.en is explicitly encoded as ISO-8859-1
%doc CHANGES-FCGID NOTICE-FCGID README-FCGID STATUS-FCGID
%doc docs/manual/mod/mod_fcgid.html.en modules/fcgid/ChangeLog
%doc build/fixconf.sed
%{_libdir}/httpd/modules/mod_fcgid.so
%if %{httpd24}
%config(noreplace) %{_httpd_modconfdir}/10-fcgid.conf
%endif
%config(noreplace) %{_httpd_confdir}/fcgid.conf
%if %{rundir_tmpfs}
%{_tmpfilesdir}/mod_fcgid.conf
%endif
%dir %attr(0775,root,apache) %{rundir}/mod_fcgid/

%changelog
* Tue Mar 15 2022 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.9-21
- Adding missing BR on 'systemd-rpm-macros'.
- License verified.

* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.3.9-20
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May  3 2018 Paul Howarth <paul@city-fan.org> - 2.3.9-15
- Correct mode of %%{rundir}/mod_fcgid in %%{_tmpfilesdir}/mod_fcgid.conf

* Wed May 02 2018 Luboš Uhliarik <luhliari@redhat.com> - 2.3.9-14
- Resolves: #1564219 - SELinux prevents httpd from starting when mod_fcgid
  is installed (also #1574390)

* Tue Feb 20 2018 Paul Howarth <paul@city-fan.org> - 2.3.9-13
- BR: gcc

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 26 2018 Paul Howarth <paul@city-fan.org> - 2.3.9-11
- Drop SELinux policy module: all supported targets have it in base policy now
- Update README.SELinux to current types and ship it
- Use forward-looking conditionals
- One build requirement per line
- Drop legacy Group: tag

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Mar  4 2016 Paul Howarth <paul@city-fan.org> - 2.3.9-7
- Use /usr/bin/sed rather than /bin/sed for fixconf script on modern releases
- Drop %%defattr, redundant since rpm 4.4
- Use %%license where possible

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Jan 23 2014 Joe Orton <jorton@redhat.com> 2.3.9-2
- Fix _httpd_mmn expansion in absence of httpd-devel

* Tue Oct  8 2013 Paul Howarth <paul@city-fan.org> 2.3.9-1
- Update to 2.3.9
  - SECURITY: Fix possible heap buffer overwrite (CVE-2013-4365)
  - Add experimental cmake-based build system for Windows
  - Correctly parse quotation and escaped spaces in FcgidWrapper and the AAA
    Authenticator/Authorizor/Access directives' command line argument, as
    currently documented (PR#51194)
  - Honor quoted FcgidCmdOptions arguments (notably for InitialEnv
    assignments) (PR#51657)
  - Conform script response parsing with mod_cgid and ensure no response body
    is sent when ap_meets_conditions() determines that request conditions are
    met
  - Improve logging in access control hook functions
  - Avoid making internal sub-requests and processing Location headers when in
    FCGI_AUTHORIZER mode, as the auth hook functions already treat Location
    headers returned by scripts as an error since redirections are not
    meaningful in this mode
  - Revert fix for PR#53693, added in 2.3.8 but undocumented
  - Fix issues with a minor optimization added in 2.3.8

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.3.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.3.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul  4 2012 Paul Howarth <paul@city-fan.org> 2.3.7-4
- Move tmpfiles.d config from %%{_sysconfdir} to %%{_prefix}/lib

* Wed May  2 2012 Paul Howarth <paul@city-fan.org> 2.3.7-3
- Make %%files list more explicit

* Wed May  2 2012 Joe Orton <jorton@redhat.com> 2.3.7-2
- Use 10- prefix for conf file in conf.modules.d with httpd ≥ 2.4
- Use _httpd_confdir throughout

* Mon Apr 23 2012 Paul Howarth <paul@city-fan.org> 2.3.7-1
- Update to 2.3.7
  - Introduce FcgidWin32PreventOrphans directive on Windows to use OS Job
    Control Objects to terminate all running fcgi's when the worker process
    has been abruptly terminated (PR: 51078)
  - Periodically clean out the brigades that are pulling in the request body
    for handoff to the fcgid child (PR: 51749)
  - Resolve crash during graceful restarts (PR: 50309)
  - Solve latency/congestion of resolving effective user file access rights
    when no such info is desired, for config-related filename stats (PR: 51020)
  - Fix regression in 2.3.6 that broke process controls when using
    vhost-specific configuration
  - Account for first process in class in the spawn score
- Drop patch for CVE-2012-1181, now included in upstream release

* Tue Mar 27 2012 Paul Howarth <paul@city-fan.org> 2.3.6-6
- Fix compatibility with httpd 2.4 in F-18/RHEL-7 onwards
- Use /run rather than /var/run from F-15/RHEL-7 onwards

* Sun Jan 22 2012 Paul Howarth <paul@city-fan.org> 2.3.6-5
- Fix regression in 2.3.6 that broke process controls when using vhost-specific
  configuration (upstream issue 49902, #783742, CVE-2012-1181)

* Fri Jan  6 2012 Paul Howarth <paul@city-fan.org> 2.3.6-4
- Nobody else likes macros for commands

* Tue Feb  8 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.3.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Dec  1 2010 Paul Howarth <paul@city-fan.org> 2.3.6-2
- Add /etc/tmpfiles.d/mod_fcgid.conf for builds on Fedora 15 onwards to
  support running with /var/run on tmpfs (#656625)

* Thu Nov  4 2010 Paul Howarth <paul@city-fan.org> 2.3.6-1
- Update to 2.3.6 (see CHANGES-FCGID for full details)
  - Fix possible stack buffer overwrite (CVE-2010-3872)
  - Change the default for FcgidMaxRequestLen from 1GB to 128K; administrators
    should change this to an appropriate value based on site requirements
  - Correct a problem that resulted in FcgidMaxProcesses being ignored in some
    situations
  - Return 500 instead of segfaulting when the application returns no output
- Don't include SELinux policy for RHEL-5 builds since RHEL >= 5.5 includes it
- Explicitly require /bin/sed for fixconf script

* Tue Jun  8 2010 Paul Howarth <paul@city-fan.org> 2.3.5-2
- SELinux policy module not needed for RHEL-6 onwards

* Wed Jan 27 2010 Paul Howarth <paul@city-fan.org> 2.3.5-1
- Update to 2.3.5 (see CHANGES-FCGID for details)
- Drop upstream svn patch

* Wed Oct 21 2009 Paul Howarth <paul@city-fan.org> 2.3.4-2
- Add fixes from upstream svn for a number of issues, most notably that the
  fixconf script had an error in the regexp, which resulted in a prefix of
  "FcgidFcgid" on the updated directives

* Mon Oct 12 2009 Paul Howarth <paul@city-fan.org> 2.3.4-1
- Update to 2.3.4 (configuration directives changed again)
- Add fixconf.sed script for config file directives update

* Fri Sep 25 2009 Paul Howarth <paul@city-fan.org> 2.3.1-2.20090925svn818270
- Update to svn revision 818270
- DESTDIR and header detection patches upstreamed
- Build SELinux policy module for EL-5; support in EL-5.3 is incomplete and
  will be fixed in EL-5.5 (#519369)
- Drop aliases httpd_sys_content_r{a,o,w}_t -> httpd_fastcgi_content_r{a,o,w}_t
  from pre-2.5 SElinux policy module as these types aren't defined there

* Wed Sep 23 2009 Paul Howarth <paul@city-fan.org> 2.3.1-1.20090923svn817978
- Update to post-2.3.1 svn snapshot
- Upstream moved to apache.org
- License changed to ASL 2.0
- Use FCGID-prefixed config file options (old ones deprecated)
- Lots of documentation changes
- Renumber sources
- Don't defer to mod_fastcgi if both are present
- Drop gawk buildreq
- Add patches fixing RPM build issues (DESTDIR support, header detection)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May 26 2009 Paul Howarth <paul@city-fan.org> 2.2-12
- Don't use /etc/httpd/run as basis of "run" directory as its DAC permissions
  are not permissive enough in F-11 onwards; instead, revert to
  /var/run/mod_fcgid and tweak default config accordingly (#502273)

* Sun May 17 2009 Paul Howarth <paul@city-fan.org> 2.2-11
- Follow link /etc/httpd/run and make our "run" directory a subdir of wherever
  that leads (#501123)

* Mon Apr  6 2009 Paul Howarth <paul@city-fan.org> 2.2-10
- EL 5.3 now has SELinux support in the main selinux-policy package so handle
  that release as per Fedora >= 8, except that the RHEL selinux-policy package
  doesn't Obsolete/Provide mod_fcgid-selinux like the Fedora version, so do
  the obsoletion here instead

* Thu Feb 26 2009 Paul Howarth <paul@city-fan.org> 2.2-9
- Update documentation for MoinMoin, Rails (#476658), and SELinux

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Nov 12 2008 Paul Howarth <paul@city-fan.org> 2.2-7
- SELinux policy module no longer built for Fedora 8 onwards as it is
  obsoleted by the main selinux-policy package
- Conflicts for selinux-policy packages older than the releases where mod_fcgid
  policy was incorporated have been added for Fedora 8, 9, and 10 versions, to
  ensure that SELinux support will work if installed

* Tue Oct 21 2008 Paul Howarth <paul@city-fan.org> 2.2-6
- SELinux policy module rewritten to merge fastcgi and system script domains
  in preparation for merge into main selinux-policy package (#462318)
- Try to determine supported SELinux policy types by reading /etc/selinux/config

* Thu Jul 24 2008 Paul Howarth <paul@city-fan.org> 2.2-5
- Tweak selinux-policy version detection macro to work with current Rawhide

* Thu Feb 14 2008 Paul Howarth <paul@city-fan.org> 2.2-4
- Rebuild with gcc 4.3.0 for Fedora 9

* Mon Jan 14 2008 Paul Howarth <paul@city-fan.org> 2.2-3
- Update SELinux policy to fix occasional failures on restarts
  (move shared memory file into /var/run/mod_fcgid directory)

* Thu Jan  3 2008 Paul Howarth <paul@city-fan.org> 2.2-2
- Update SELinux policy to support file transition to httpd_tmp_t for
  temporary files

* Fri Sep 14 2007 Paul Howarth <paul@city-fan.org> 2.2-1
- Update to version 2.2
- Make sure docs are encoded as UTF-8

* Mon Sep  3 2007 Joe Orton <jorton@redhat.com> 2.1-6
- rebuild for fixed 32-bit APR (#254241)

* Thu Aug 23 2007 Paul Howarth <paul@city-fan.org> 2.1-5
- Update source URL to point to downloads.sf.net rather than dl.sf.net
- Upstream released new tarball without changing version number, though the
  only change was in arch/win32/fcgid_pm_win.c, which is not used to build the
  RPM package
- Clarify license as GPL (unspecified/any version)
- Unexpand tabs in spec
- Add buildreq of gawk

* Fri Aug  3 2007 Paul Howarth <paul@city-fan.org> 2.1-4
- Add buildreq of pkgconfig, a missing dependency of both apr-devel and
  apr-util-devel on FC5

* Fri Jun 15 2007 Paul Howarth <paul@city-fan.org> 2.1-3
- Major update of SELinux policy, supporting accessing data on NFS/CIFS shares
  and a new boolean, httpd_fastcgi_can_sendmail, to allow connections to SMTP
  servers
- Fix for SELinux policy on Fedora 7, which didn't work due to changes in the
  permissions macros in the underlying selinux-policy package

* Wed Mar 21 2007 Paul Howarth <paul@city-fan.org> 2.1-2
- Add RHEL5 with SELinux support
- Rename README.Fedora to README.RPM

* Fri Feb 16 2007 Paul Howarth <paul@city-fan.org> 2.1-1
- Update to 2.1
- Update documentation and patches
- Rename some source files to reduce chances of conflicting names
- Include SharememPath directive in conf file to avoid unfortunate upstream
  default location

* Mon Oct 30 2006 Paul Howarth <paul@city-fan.org> 2.0-1
- Update to 2.0
- Source is now hosted at sourceforge.net
- Update docs

* Wed Sep  6 2006 Paul Howarth <paul@city-fan.org> 1.10-7
- Include the right README* files

* Tue Aug 29 2006 Paul Howarth <paul@city-fan.org> 1.10-6
- Buildreqs for FC5 now identical to buildreqs for FC6 onwards

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.10-5
- Split off SELinux module into separate subpackage to avoid dependency on
  the selinux-policy package for the main package

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.10-4
- SELinux policy packages moved from %%{_datadir}/selinux/packages/POLICYNAME
  to %%{_datadir}/selinux/POLICYNAME
- hardlink identical policy module packages together to avoid duplicate files

* Thu Jul 20 2006 Paul Howarth <paul@city-fan.org> 1.10-3
- Adjust buildreqs for FC6 onwards
- Figure out where top_dir is dynamically since the /etc/httpd/build
  symlink is gone in FC6

* Wed Jul  5 2006 Paul Howarth <paul@city-fan.org> 1.10-2
- SELinux policy update: allow FastCGI apps to do DNS lookups

* Tue Jul  4 2006 Paul Howarth <paul@city-fan.org> 1.10-1
- Update to 1.10
- Expand tabs to shut rpmlint up

* Tue Jul  4 2006 Paul Howarth <paul@city-fan.org> 1.09-10
- SELinux policy update:
  * allow httpd to read httpd_fastcgi_content_t without having the
  | httpd_builtin_scripting boolean set
  * allow httpd_fastcgi_script_t to read /etc/resolv.conf without
  | having the httpd_can_network_connect boolean set

* Sun Jun 18 2006 Paul Howarth <paul@city-fan.org> 1.09-9
- Discard output of semodule in %%postun
- Include some documentation from upstream

* Fri Jun  9 2006 Paul Howarth <paul@city-fan.org> 1.09-8
- Change default context type for socket directory from var_run_t to
  httpd_fastcgi_sock_t for better separation

* Thu Jun  8 2006 Paul Howarth <paul@city-fan.org> 1.09-7
- Add SELinux policy module and README.Fedora
- Conflict with selinux-policy versions older than what we're built on

* Mon May 15 2006 Paul Howarth <paul@city-fan.org> 1.09-6
- Instead of conflicting with mod_fastcgi, don't add the handler for .fcg etc.
  if mod_fastcgi is present

* Fri May 12 2006 Paul Howarth <paul@city-fan.org> 1.09-5
- Use correct handler name in fcgid.conf
- Conflict with mod_fastcgi
- Create directory %%{_localstatedir}/run/mod_fcgid for sockets

* Thu May 11 2006 Paul Howarth <paul@city-fan.org> 1.09-4
- Cosmetic tweaks (personal preferences)
- Don't include INSTALL.TXT, nothing of use to end users

* Wed May 10 2006 Thomas Antony <thomas@antony.eu> 1.09-3
- Initial release
