# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%bcond_with nis

%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
%define ldap_impl openldap
%else
%define ldap_impl mozldap
%endif
%if 0%{?fedora} >= 18 || 0%{?rhel} >= 6
%define betxn_opts --enable-be-txns-by-default
%else
%define betxn_opts --disable-be-txns-by-default
%endif

Name:		slapi-nis
Version:	0.70.0
Release: 7%{?dist}
Summary:	Schema Compatibility plugins for Directory Server
License:	GPL-3.0-or-later
URL:		http://pagure.io/slapi-nis/
Source0:	https://releases.pagure.org/slapi-nis/slapi-nis-%{version}.tar.gz
Source1:	https://releases.pagure.org/slapi-nis/slapi-nis-%{version}.tar.gz.asc
Patch0:		slapi-nis-eq_once_rel.patch
Patch1:         slapi-nis-rhbz2341357-fix.patch

BuildRequires: make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:	389-ds-base-devel >= 1.3.5.6, %{ldap_impl}-devel
BuildRequires:	nspr-devel, nss-devel, /usr/bin/rpcgen
%if 0%{?fedora} > 18 || 0%{?rhel} > 6
BuildRequires:	libsss_nss_idmap-devel > 1.16.0-5
%define sss_nss_opts --with-sss-nss-idmap --with-idviews
%else
%define sss_nss_opts %{nil}
%endif
BuildRequires:	pam-devel
%if %{with nis}
%if (0%{?fedora} > 14 && 0%{?fedora} < 28) || (0%{?rhel} > 6 && 0%{?rhel} < 8)
BuildRequires:	libtirpc-devel
%else
BuildRequires:  libnsl2-devel
%endif
%endif
%if 0%{?fedora} > 27 || 0%{?rhel} >= 9
ExcludeArch: %{ix86}
%endif
Requires: 389-ds-base >= 1.3.5.6

%description
This package provides two plugins for Red Hat and 389 Directory Server.

The NIS Server plugin allows the directory server to act as a NIS server
for clients, dynamically generating and updating NIS maps according to
its configuration and the contents of the DIT, and serving the results to
clients using the NIS protocol as if it were an ordinary NIS server.

The Schema Compatibility plugin allows the directory server to provide an
alternate view of entries stored in part of the DIT, optionally adding,
dropping, or renaming attribute values, and optionally retrieving values
for attributes from multiple entries in the tree.

%prep
%setup -q
%patch -p1 -P0
%patch -p1 -P1

%build
autoconf --force
%if %{with nis}
WITH_NIS=--enable-nis=yes
%else
WITH_NIS=--disable-nis
%endif
%configure --disable-static --with-ldap=%{ldap_impl} \
	--with-nsswitch --with-pam --with-pam-service=system-auth \
	%{sss_nss_opts} %{betxn_opts} \
	$WITH_NIS
sed -i -e 's,%{_libdir}/dirsrv/plugins/,,g' -e 's,.so$,,g' doc/examples/*.ldif
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/dirsrv/plugins/*.la

%if 0
# ns-slapd doesn't want to start in koji, so no tests get run
%check
make check
%endif

%files
%doc COPYING NEWS README STATUS doc/sch-*.txt doc/examples/sch-*.ldif doc/ipa
%if %{with nis}
%doc doc/nis-*.txt doc/examples/nis-*.ldif
%{_mandir}/man1/*
%{_sbindir}/nisserver-plugin-defs
%endif
%{_libdir}/dirsrv/plugins/*.so

%triggerin -- 389-ds-base
instances=$(/usr/sbin/dsctl -l)
for inst in $instances ; do
    grep -q "cn=NIS server,cn=plugins" /etc/dirsrv/${inst}/dse.ldif
    if test $? -eq 0 ; then
	    /usr/bin/ldapdelete -Y EXTERNAL -H ldapi://%2fvar%2frun%2f${inst}.socket -r "cn=NIS Server,cn=plugins,cn=config" 2>/dev/null
	    result=$?
	    if test $result -eq 255 ; then
		echo "Cannot remove NIS server plugin from LDAP server ${inst} instance. Server will fail to start until it is removed."
		echo "Remove 'cn=NIS Server,cn=plugins,cn=config' entry from /etc/dirsrv/${inst}/dse.ldif"
	    fi
	    if test $result -eq 0 ; then
		/usr/sbin/dsctl "$inst" restart
	    fi
    fi
done


%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.70.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 23 2025 Alexander Bokovoy <abokovoy@redhat.com> - 0.70.0-5
- Fix gcc15 regression
- Resolves: rhbz#2341357

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.70.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

- Tue Aug 27 2024 Alexander Bokovoy <abokovoy@redhat.com> - 0.70.0-3
- Fixed initialization regression that caused compat tree never be populated

* Fri Aug 16 2024 Alexander Bokovoy <abokovoy@redhat.com> - 0.70.0-2
- Handle the case of a disabled 389-ds instance

* Fri Aug 16 2024 Alexander Bokovoy <abokovoy@redhat.com> - 0.70.0-1
- Release 0.70.0
- Disable NIS server by default

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 07 2023 Alexander Bokovoy <abokovoy@redhat.com> - 0.60.0-4
- Ignore updates from non-tracked subtrees during modify/modrdn/update
  to avoid deadlocks with retro changelog

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.60.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Aug 20 2022 Alexander Bokovoy <abokovoy@redhat.com> - 0.60.0-1
- new upstream release
- Change license from GPLv2 to GPLv3+ to follow 389-ds licensing
- Fix ID views integration
- Fix base scope lookups
- Bump NIS max dgram size to 8KB by default instead of 1KB

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Feb 01 2022 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.7-5
- Resolves: rhbz#2032691
- Rebuild against newer OpenLDAP version

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Nov 12 2021 Björn Esser <besser82@fedoraproject.org> - 0.56.7-3
- Rebuild(libnsl2)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue May 18 2021 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.7-1
- CVE-2021-3480: invalid bind DN crash
- New upstream release

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Dec 04 2020 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.6-1
- New upstream release
- Ignore searches which don't match any configured map

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed May 06 2020 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.5-2
- Initialize map locks in NIS plugin to prevent crash

* Mon May 04 2020 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.5-1
- New upstream release
- Resolves: rhbz#1751295: (2) When sync-repl is enabled, slapi-nis can deadlock during retrochanglog trimming
- Resolves: rhbz#1768156: ERR - schemacompat - map rdlock: old way MAP_MONITOR_DISABLED

* Fri Feb 07 2020 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.4-1
- New upstream release
- Fix build with newer gcc versions
- Resolves rhbz#1800097

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 06 2019 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.3-1
- New upstream release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May 02 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.2-6
- Force rebuild of configure

* Wed May 02 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.2-5
- Link with libnsl explicitly in Fedora 28 or later
- Require libnsl2-devel for build
- Resolves rhbz#1573636

* Thu Mar 15 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.2-4
- Remove tcpwrappers support as they aren't available in Fedora anymore

* Thu Mar 15 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.2-3
- Do not build on i686 in Fedora 28 or later as 389-ds-base is not available there anymore
- Resolves rhbz#1556448
- Remove outdated ExclusiveArch for RHEL6

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.2-1
- New upstream release
- Update links to the upstream project page and releases
- Use extended SSSD API to signal that an entry should not be cached anymore
- Add support for timeout-based NSS queries with libsss_nss_idmap

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.56.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Aug 08 2016 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.1-1
- Support querying external users by UPN alias
- Don't clobber target of the pblock for ID views

* Mon Jun 20 2016 Alexander Bokovoy <abokovoy@redhat.com> - 0.56.0-2
- Updated upstream tarball

* Mon Jun 20 2016 Alexander Bokovoy <abokovoy@redhat.com> - 0.56-1
- Add support for changing passwords for users from a primary tree
  - requires DS 1.3.5.6 or later

* Mon May 30 2016 Alexander Bokovoy <abokovoy@redhat.com> - 0.55-3
- Add support to properly shutdown priming cache from RHEL 7.2.4

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.55-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 26 2016 Alexander Bokovoy <abokovoy@redhat.com> - 0.55-1
- Support external members of IPA groups in schema compat
- Support bind over ID overrides when uid is not overridden
- Populate schema compat trees in parallel to LDAP server startup

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.54.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Mar 26 2015 Alexander Bokovoy <abokovoy@redhat.com> - 0.54.2-1
- CVE-2015-0283 slapi-nis: infinite loop in getgrnam_r() and getgrgid_r() (#1206049)
- Make sure nss_sss.so.2 module is used directly
- Allow building slapi-nis with ID views against 389-ds-base from RHEL7.0/CentOS7.0 releases

* Thu Nov  6 2014 Alexander Bokovoy <abokovoy@redhat.com> - 0.54.1-1
- support FreeIPA overrides in LDAP BIND callback
- ignore FreeIPA override searchs outside configured schema compat subtrees

* Fri Oct 10 2014 Alexander Bokovoy <abokovoy@redhat.com> - 0.54-1
- Add support for FreeIPA's ID views
- Allow searching SSSD-provided users as memberUid case-insensitevly
  Fixes bug #1130131

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.53-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Apr 22 2014 Nalin Dahyabhai <nalin@redhat.com> - 0.53-1
- correct the default NIS map settings for hosts.byname and hosts.byaddr,
  from report by Rik Megens
- fix several problems when hitting out-of-memory conditions, spotted by
  static analysis

* Mon Jan 20 2014 Nalin Dahyabhai <nalin@redhat.com> - 0.52-3
- remove ExclusiveArch if %%{rhel} is 7 or higher, because 389-ds-base gets
  built for everything now (#1055711)

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.52-2
- Mass rebuild 2013-12-27

* Mon Dec 16 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.52-1
- correctly reflect whether or not we're built with transaction support in
  the module's nsslapd-pluginVersion attribute
- fix a couple of should've-used-memmove()-instead-of-memcpy() cases which
  would hit when removing maps or groups of maps (#1043546/#1043638)

* Mon Dec  9 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.51-1
- fix another request argument memory leak in NIS server (#1040159)
- fix miscellaneous items found by static analysis

* Tue Oct  1 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.50-1
- if we get an EPIPE while registering with rpcbind, try to reconnect and
  retransmit before giving up

* Thu Sep 19 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.49-1
- add {nis,schema-compat}-ignore-subtree and -restrict-subtree settings,
  which should let us avoid deadlocks when tasks are modifying data in
  the backend database (#1007451)

* Mon Aug 12 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.48-1
- try to gracefully handle failures obtaining internal locks
- fix locating-by-name of entries with names that require escaping
- add self-tests for nsswitch and PAM functionality
- make nsswitch mode properly handle user and group names with commas in them
- handle attempts to PAM authenticate to compat groups (i.e., with failure)
- drop the "schema-compat-origin" attribute

* Wed Aug  7 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.47.7-1
- fix building against versions of directory server older than 1.3.0, which
  first introduced slapi_escape_filter_value()

* Wed Aug  7 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.47.6-1
- only buildrequire libsss_nss_idmap-devel on releases that included SSSD
  version 1.10 or later, where it first appeared

* Wed Aug  7 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.47.5-1
- merge Alexander Bokovoy's patches to
  - teach the schema compatibility plugin to optionally serve user and group
    information retrieved from libc as part of a set of compat entries
  - handle simple bind requests for those entries by calling out to PAM
  - to rewrite the DN of incoming bind requests to compat entries to point
    at the source entries, instead of returning a referral which most clients
    won't handle
- include IPA-specific docs as docs

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.47-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri May 24 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.47-1
- fix request argument memory leaks in NIS server
- add a %%sort function

* Thu Apr  4 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.46-1
- when checking if we can skip processing for a given change, pay attention to
  whether or not the changes cause the entry to need to be added or removed
  from a map (#912673)
- check SLAPI_PLUGIN_OPRETURN in post-change hooks, in case the backend failed
  to update things but the server called us anyway

* Tue Mar 19 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.45-1
- fix dispatching for multiple connected clients in the NIS plugin (#923336)

* Tue Feb  5 2013 Nalin Dahyabhai <nalin@redhat.com> - 0.44-3
- work around multilib differences in the example .ldif files (internal
  tooling)

* Tue Nov 20 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.44-2
- set betxn support to be disabled by default on Fedora 17 or EL 5 or older,
  which have versions of IPA < 3.0, per mkosek on freeipa-devel

* Wed Nov 14 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.44-1
- add missing newline to a couple of debug log messages
- note whether or not betxn support is compiled in as part of the
  nsslapd-pluginVersion value we report to the server
- register callbacks in the same order in both plugins, so that
  their log messages are logged in the same order

* Tue Nov 13 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.43-1
- reintroduce support for directory server transactions (nhosoi, IPA#3046)
- control transaction support at run-time, deciding when to do things based
  on the value of the nsslapd-pluginbetxn attribute in the plugin's entry
- NIS: add default settings for shadow.byname and passwd.adjunct.byname maps

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.42-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.42-1
- drop support for directory server transactions (richm, #766320)

* Tue May 22 2012 Nalin Dahyabhai <nalin@redhat.com>
- fix a leak due to us assuming that slapi_mods_add_smod() not taking ownership
  of an smod along with its contents, when it just keeps the contents

* Tue Apr 10 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.41-1
- log errors evaluating pad expressions in %%link rather than continuing on
  until we hit an arithmetic exception (#810258)

* Fri Mar 30 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.40-1
- treat padding values passed to the "link" function as expressions to be
  evaluated rather than simply as literal values (part of #767372)

* Wed Mar 28 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.39-1
- add a "default" function for trying to evaluate one expression, then
  another, then another... (part of #767372)
- when creating a compat entry based on a real entry, set an entryUSN based on
  the source entry or the rootDSE (freeipa #864); the "scaffolding" entries
  won't have them

* Tue Mar  6 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.38-1
- properly escape RDN values when building compat entries (#796509, #800625)

* Mon Feb 13 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.37-1
- fix a compile error on systems where LDAP_SCOPE_SUBORDINATE isn't defined
  (reported by Christian Neuhold)
- conditionalize whether we have a build dependency on tcp_wrappers (older
  releases) or tcp_wrappers-devel (newer releases)

* Tue Jan 24 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.36-1
- take steps to avoid making yp_first/yp_next clients loop indefinitely
  when a single LDAP entry produces multiple copies of the same NIS key
  for a given map

* Tue Jan 24 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.35-1
- add mmatch/mregmatch[i]/mregsub[i] formatting functions which work like
  match/regmatch[i]/regsub[i], but which can handle and return lists of
  zero or more results (part of #783274)

* Thu Jan 19 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.34-1
- do entry comparisons ourselves, albeit less throughly, to avoid the worst
  case in pathological cases (more of #771444)

* Tue Jan 17 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.33-1
- get more aggressive about skipping unnecessary calculations (most of
  the problem in #771444, though not the approach described there)

* Mon Jan 16 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.32-1
- add support for directory server transactions (#758830,#766320)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jan 11 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.31-1
- fix some memory leaks (more of #771493)

* Tue Jan 10 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.30-1
- skip recalculations when the attributes which changed don't factor into
  our calculations (part of #771493)

* Wed Jan  4 2012 Nalin Dahyabhai <nalin@redhat.com> - 0.29-1
- add regmatchi/regsubi formatting functions which work like regmatch/regsub,
  but do matching in a case-insensitive manner
- update NIS map defaults to match {CRYPT} userPassword values in a
  case-insensitive manner so that we also use {crypt} userPassword values
- fix inconsistencies in the NIS service stemming from using not-normalized DNs
  in some places where it should have used normalized DNs

* Mon Dec 19 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.28-1
- when configured with --with-ldap=openldap, link with -lldap_r rather
  than -lldap (rmeggins, #769107)

* Tue Dec  6 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.27-1
- when building for 389-ds, use Slapi_RWLocks if they appear to be available
  (the rest of #730394/#730403)

* Fri Aug 12 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.26-1
- when building for 389-ds, use libpthread's read-write locks instead of
  NSPR's (part of #730394/#730403)

* Wed Jul 27 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.25-1
- speed up building compat entries which reference thousands of other entries
  (more of #692690)
- 389-ds-base is apparently exclusive to x86_64 and %%{ix86} on EL, so we have
  to be, too

* Fri May 13 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.24-1
- carry our own yp.x, so that we don't get bitten if libc doesn't include
  yp client routines
- we need rpcgen at build-time now

* Thu Mar 31 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.23-1
- speed up building compat entries with attributes with thousands of literal
  values (#692690)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan  6 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.22-1
- fix a number of scanner-uncovered defects

* Thu Jan  6 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.21-2
- make sure we always pull in nss-devel and nspr-devel, and the right
  ldap toolkit for the Fedora or RHEL version

* Tue Nov 23 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.21-1
- update to 0.21
  - schema-compat: don't look at standalone compat containers for a search,
    since we'll already have looked at the group container

* Tue Nov 23 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.20-1
- update to 0.20
  - add a deref_f function

* Mon Nov 22 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.19-1
- fix a brown-paper-bag crash

* Mon Nov 22 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.18-1
- update to 0.18
  - add a deref_rf function
  - schema-compat: don't respond to search requests for which there's no backend
  - schema-compat: add the ability to do standalone compat containers

* Wed Nov 17 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.17-6
- revert that last change, it's unnecessary

* Thu Nov 11 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.17-5
- build against either 389-ds-base or redhat-ds-base, whichever is probably
  more appropriate here

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.17-3
- change buildreq from fedora-ds-base-devel to 389-ds-base-devel, which
  should avoid multilib conflicts from installing both arches of the new
  package (#511504)

* Tue Jul 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.17-2
- fixup changelog entries that resemble possible macro invocations

* Thu May 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.17-1
- actually send portmap registrations to the right server

* Thu May 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.16-1
- fix NIS server startup problem when no port is explicitly configured and
  we're using portmap instead of rpcbind (#500903)

* Fri May  8 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.15-1
- fix %%deref and %%referred to fail rather than return a valid-but-empty
  result when they fail to evaluate (reported by Rob Crittenden)

* Wed May  6 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.14-1
- correctly handle being loaded but disabled (#499404)

* Thu Apr 30 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.13-1
- update to 0.13, reworking %%link() to correct some bugs (#498432)

* Thu Apr 30 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.12-1
- correct test suite failures that 0.11 started triggering

* Tue Apr 28 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.11-1
- update to 0.11 (#497904)

* Wed Mar  4 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.10-1
- update to 0.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec  9 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.5-2
- make the example nsslapd-pluginpath values the same on 32- and 64-bit
  systems, because we can depend on the directory server "knowing" which
  directory to search for the plugins

* Mon Dec  8 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.5-1
- update to 0.8.5 to suppress duplicate values for attributes in the schema
  compatibility plugin

* Thu Dec  4 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.4-1
- update to 0.8.4 to fix:
  - problems updating references, particularly those for %%referred() (#474478)
  - inability to notice internal add/modify/modrdn/delete operations (really
    this time) (#474426)

* Wed Dec  3 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.3-1
- update to 0.8.3 to also notice and reflect changes caused by internal
  add/modify/modrdn/delete operations
 
* Wed Nov 19 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.2-1
- update to 0.8.2 to remove a redundant read lock in the schema-compat plugin

* Fri Nov  7 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.9-1
- update to 0.9

* Fri Oct  3 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.1-1
- update to 0.8.1 to fix a heap corruption (Rich Megginson)

* Wed Aug  6 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8-1
- update to 0.8

* Wed Aug  6 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.7-1
- update to 0.7

* Wed Jul 23 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.6-1
- rebuild (and make rpmlint happy)

* Wed Jul  9 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.2-1
- initial package
