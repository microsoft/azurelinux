%define __perl_requires %{SOURCE98}
Summary:        The Squid proxy caching server
Name:           squid
Version:        5.7
Release:        6%{?dist}
Epoch:          7
License:        GPLv2
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.squid-cache.org
Source0:        http://www.squid-cache.org/Versions/v5/squid-%{version}.tar.xz
Source1:        squid.logrotate
Source2:        squid.sysconfig
Source3:        squid.pam
Source4:        squid.nm
Source5:        squid.service
Source6:        cache_swap.sh
Source7:        squid.sysusers
Source98:       perl-requires-squid.sh
# Upstream patches
# Backported patches
Patch101:       squid-5.7-ip-bind-address-no-port.patch
# Local patches
# Applying upstream patches first makes it less likely that local patches
# will break upstream ones.
Patch201:       squid-4.0.11-config.patch
Patch202:       squid-3.1.0.9-location.patch
Patch203:       squid-3.0.STABLE1-perlpath.patch
Patch204:       squid-3.5.9-include-guards.patch
# revert this upstream patch - https://bugzilla.redhat.com/show_bug.cgi?id=1936422
# workaround for #1934919
Patch205:       squid-5.0.5-symlink-lang-err.patch
Patch206:    CVE-2024-23638.patch
Patch207:    CVE-2024-23638-1.patch
# required for SASL authentication
BuildRequires:  cyrus-sasl-devel
# ESI support requires Expat & libxml2
BuildRequires:  expat-devel
#ip_user helper requires
BuildRequires:  gcc-c++
# For verifying downloded src tarball
BuildRequires:  gnupg2
# squid_kerb_aut requires Kerberos development libs
BuildRequires:  krb5-devel
# TPROXY requires libcap, and also increases security somewhat
BuildRequires:  libcap-devel
# eCAP support
BuildRequires:  libecap-devel
# time_quota requires TrivialDB
BuildRequires:  libtdb-devel
BuildRequires:  libtool
BuildRequires:  libtool-ltdl-devel
BuildRequires:  libxml2-devel
# squid_ldap_auth and other LDAP helpers require OpenLDAP
BuildRequires:  make
BuildRequires:  openldap-devel
# SSL support requires OpenSSL
BuildRequires:  openssl-devel
# squid_pam_auth requires PAM development libs
BuildRequires:  pam-devel
BuildRequires:  perl-generators
BuildRequires:  pkg-config
# systemd notify
BuildRequires:  systemd-devel
# for _tmpfilesdir and _unitdir macro
# see https://docs.fedoraproject.org/en-US/packaging-guidelines/Systemd/#_packaging
BuildRequires:  systemd-rpm-macros
# For test suite
BuildRequires:  pkgconfig(cppunit)
# cache_swap.sh
Requires:       bash
Requires:       gawk
# for httpd conf file - cachemgr script alias
Requires:       httpd-filesystem
# Old NetworkManager expects the dispatcher scripts in a different place
Conflicts:      NetworkManager < 1.20
%{?systemd_requires}
%{?sysusers_requires_compat}

%description
Squid is a high-performance proxy caching server for Web clients,
supporting FTP, gopher, and HTTP data objects. Unlike traditional
caching software, Squid handles all requests in a single,
non-blocking, I/O-driven process. Squid keeps meta data and especially
hot objects cached in RAM, caches DNS lookups, supports non-blocking
DNS lookups, and implements negative caching of failed requests.

Squid consists of a main server program squid, a Domain Name System
lookup program (dnsserver), a program for retrieving FTP data
(ftpget), and some management and client tools.

%prep
%setup -q

# Upstream patches

# Backported patches
%patch101 -p1 -b .ip-bind-address-no-port

# Local patches
%patch201 -p1 -b .config
%patch202 -p1 -b .location
%patch203 -p1 -b .perlpath
%patch204  -b .include-guards
%patch205 -p1 -R -b .symlink-lang-err
%patch206 -p1\n
%patch207 -p1\n# https://bugzilla.redhat.com/show_bug.cgi?id=1679526
# Patch in the vendor documentation and used different location for documentation
sed -i 's|@SYSCONFDIR@/squid.conf.documented|%{_pkgdocdir}/squid.conf.documented|' src/squid.8.in

%build

# NIS helper has been removed because of the following bug
# https://bugzilla.redhat.com/show_bug.cgi?id=1531540
%configure \
   --libexecdir=%{_libdir}/squid \
   --datadir=%{_datadir}/squid \
   --sysconfdir=%{_sysconfdir}/squid \
   --with-logdir='%{_localstatedir}/log/squid' \
   --with-pidfile='/run/squid.pid' \
   --disable-dependency-tracking \
   --enable-eui \
   --enable-follow-x-forwarded-for \
   --enable-auth \
   --enable-auth-basic="DB,fake,getpwnam,LDAP,NCSA,PAM,POP3,RADIUS,SASL,SMB,SMB_LM" \
   --enable-auth-ntlm="SMB_LM,fake" \
   --enable-auth-digest="file,LDAP" \
   --enable-auth-negotiate="kerberos" \
   --enable-external-acl-helpers="LDAP_group,time_quota,session,unix_group,wbinfo_group,kerberos_ldap_group" \
   --enable-storeid-rewrite-helpers="file" \
   --enable-cache-digests \
   --enable-cachemgr-hostname=localhost \
   --enable-delay-pools \
   --enable-epoll \
   --enable-icap-client \
   --enable-ident-lookups \
   %ifnarch %{power64} ia64 x86_64 s390x aarch64
   --with-large-files \
   %endif
   --enable-linux-netfilter \
   --enable-removal-policies="heap,lru" \
   --enable-snmp \
   --enable-ssl \
   --enable-ssl-crtd \
   --enable-storeio="aufs,diskd,ufs,rock" \
   --enable-diskio \
   --enable-wccpv2 \
   --enable-esi \
   --enable-ecap \
   --with-aio \
   --with-default-user="squid" \
   --with-dl \
   --with-openssl \
   --with-pthreads \
   --disable-arch-native \
   --disable-security-cert-validators \
   --disable-strict-error-checking \
   --with-swapdir=%{_localstatedir}/spool/squid

# workaround to build squid v5
mkdir -p src/icmp/tests
mkdir -p tools/squidclient/tests
mkdir -p tools/tests

%make_build

%check
make check

%install
%make_install

echo "
#
# This is %{_sysconfdir}/httpd/conf.d/squid.conf
#

ScriptAlias /Squid/cgi-bin/cachemgr.cgi %{_libdir}/squid/cachemgr.cgi

# Only allow access from localhost by default
<Location /Squid/cgi-bin/cachemgr.cgi>
 Require local
 # Add additional allowed hosts as needed
 # Require host example.com
</Location>" > %{buildroot}/squid.httpd.tmp


mkdir -p %{buildroot}%{_sysconfdir}/logrotate.d
mkdir -p %{buildroot}%{_sysconfdir}/sysconfig
mkdir -p %{buildroot}%{_sysconfdir}/pam.d
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d/
mkdir -p %{buildroot}%{_libdir}/NetworkManager/dispatcher.d
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_libexecdir}/squid
install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/squid
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/squid
install -m 644 %{SOURCE3} %{buildroot}%{_sysconfdir}/pam.d/squid
install -m 644 %{SOURCE5} %{buildroot}%{_unitdir}
install -m 755 %{SOURCE6} %{buildroot}%{_libexecdir}/squid
install -m 644 %{buildroot}/squid.httpd.tmp %{buildroot}%{_sysconfdir}/httpd/conf.d/squid.conf
install -m 755 %{SOURCE4} %{buildroot}%{_libdir}/NetworkManager/dispatcher.d/20-squid
mkdir -p %{buildroot}%{_localstatedir}/log/squid
mkdir -p %{buildroot}%{_localstatedir}/spool/squid
mkdir -p %{buildroot}/run/squid
chmod 644 contrib/url-normalizer.pl contrib/user-agents.pl

# install /usr/lib/tmpfiles.d/squid.conf
mkdir -p %{buildroot}%{_tmpfilesdir}
cat > %{buildroot}%{_tmpfilesdir}/squid.conf <<EOF
# See tmpfiles.d(5) for details

d /run/squid 0755 squid squid - -
EOF

# Move the MIB definition to the proper place (and name)
mkdir -p %{buildroot}%{_datadir}/snmp/mibs
mv %{buildroot}%{_datadir}/squid/mib.txt %{buildroot}%{_datadir}/snmp/mibs/SQUID-MIB.txt

# squid.conf.documented is documentation. We ship that in doc/
rm -f %{buildroot}%{_sysconfdir}/squid/squid.conf.documented

# remove unpackaged files from the buildroot
rm -f %{buildroot}/squid.httpd.tmp

# sysusers.d
install -p -D -m 0644 %{SOURCE7} %{buildroot}%{_sysusersdir}/squid.conf

%files
%license COPYING
%doc CONTRIBUTORS README ChangeLog QUICKSTART src/squid.conf.documented
%doc contrib/url-normalizer.pl contrib/user-agents.pl

%{_unitdir}/squid.service
%attr(755,root,root) %dir %{_libexecdir}/squid
%attr(755,root,root) %{_libexecdir}/squid/cache_swap.sh
%attr(755,root,root) %dir %{_sysconfdir}/squid
%attr(755,root,root) %dir %{_libdir}/squid
%attr(770,squid,root) %dir %{_localstatedir}/log/squid
%attr(750,squid,squid) %dir %{_localstatedir}/spool/squid
%attr(755,squid,squid) %dir /run/squid

%config(noreplace) %attr(644,root,root) %{_sysconfdir}/httpd/conf.d/squid.conf
%config(noreplace) %attr(640,root,squid) %{_sysconfdir}/squid/squid.conf
%config(noreplace) %attr(644,root,squid) %{_sysconfdir}/squid/cachemgr.conf
%config(noreplace) %{_sysconfdir}/squid/mime.conf
%config(noreplace) %{_sysconfdir}/squid/errorpage.css
%config(noreplace) %{_sysconfdir}/sysconfig/squid
# These are not noreplace because they are just sample config files
%config %{_sysconfdir}/squid/squid.conf.default
%config %{_sysconfdir}/squid/mime.conf.default
%config %{_sysconfdir}/squid/errorpage.css.default
%config %{_sysconfdir}/squid/cachemgr.conf.default
%config(noreplace) %{_sysconfdir}/pam.d/squid
%config(noreplace) %{_sysconfdir}/logrotate.d/squid

%dir %{_datadir}/squid
%attr(-,root,root) %{_datadir}/squid/errors
%{_libdir}/NetworkManager
%{_datadir}/squid/icons
%{_sbindir}/squid
%{_bindir}/squidclient
%{_bindir}/purge
%{_mandir}/man8/*
%{_mandir}/man1/*
%{_libdir}/squid/*
%{_datadir}/snmp/mibs/SQUID-MIB.txt
%{_tmpfilesdir}/squid.conf
%{_sysusersdir}/squid.conf

%pre
%{sysusers_create_compat} %{SOURCE7}

for i in %{_var}/log/squid %{_var}/spool/squid ; do
        if [ -d $i ] ; then
                for adir in `find $i -maxdepth 0 \! -user squid`; do
                        chown -R squid:squid $adir
                done
        fi
done

exit 0

%pretrans -p <lua>
-- temporarilly commented until https://bugzilla.redhat.com/show_bug.cgi?id=1936422 is resolved
--
-- previously %{_datadir}/squid/errors/es-mx was symlink, now it is directory since squid v5
-- see https://docs.fedoraproject.org/en-US/packaging-guidelines/Directory_Replacement/
-- Define the path to the symlink being replaced below.
--
-- path = "%{_datadir}/squid/errors/es-mx"
-- st = posix.stat(path)
-- if st and st.type == "link" then
--   os.remove(path)
-- end

-- Due to a bug #447156
paths = {"%{_datadir}/squid/errors/zh-cn", "%{_datadir}/squid/errors/zh-tw"}
for key,path in ipairs(paths)
do
  st = posix.stat(path)
  if st and st.type == "directory" then
    status = os.rename(path, path .. ".rpmmoved")
    if not status then
      suffix = 0
      while not status do
        suffix = suffix + 1
        status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
      end
      os.rename(path, path .. ".rpmmoved")
    end
  end
end

%post
%systemd_post squid.service

%preun
%systemd_preun squid.service

%postun
%systemd_postun_with_restart squid.service

%triggerin -- samba-common
if ! getent group wbpriv >/dev/null 2>&1 ; then
  %{_sbindir}/groupadd -g 88 wbpriv >/dev/null 2>&1 || :
fi
%{_sbindir}/usermod -a -G wbpriv squid >/dev/null 2>&1 || \
    chgrp squid %{_var}/cache/samba/winbindd_privileged >/dev/null 2>&1 || :
%changelog
* Thu Jun 13 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 5.7-6
- Add patch for CVE-2024-23638

* Thu Feb 09 2023 Sindhu Karri <lakarri@microsoft.com> - 7:5.7-5
- Initial CBL-Mariner import from Fedora 38 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths
- Added missing BR on 'cyrus-sasl-devel'
- License verified

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7:5.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Tomas Korbar <tkorbar@redhat.com> - 7:5.7-3
- Backport adding IP_BIND_ADDRESS_NO_PORT flag to outgoing connections

* Wed Oct 12 2022 Luboš Uhliarik <luhliari@redhat.com> - 7:5.7-2
- Provide a sysusers.d file to get user() and group() provides (#2134071)

* Tue Sep 06 2022 Luboš Uhliarik <luhliari@redhat.com> - 7:5.7-1
- new version 5.7

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7:5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 Luboš Uhliarik <luhliari@redhat.com> - 7:5.6-1
- new version 5.6

* Wed Apr 20 2022 Luboš Uhliarik <luhliari@redhat.com> - 7:5.5-1
- new version 5.5
- Resolves: #2053799 - squid-5.5 is available

* Wed Feb 09 2022 Luboš Uhliarik <luhliari@redhat.com> - 7:5.4-1
- new version 5.4

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7:5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 05 2021 Luboš Uhliarik <luhliari@redhat.com> - 7:5.2-1
- new version 5.2 (#2010109)
- Resolves: #1934559 - squid: out-of-bounds read in WCCP protocol

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 7:5.1-2
- Rebuilt with OpenSSL 3.0.0

* Thu Aug 05 2021 Luboš Uhliarik <luhliari@redhat.com> - 7:5.1-1
- new version 5.1

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7:5.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Mon May 17 2021 Lubos Uhliarik <luhliari@redhat.com> - 7:5.0.6-1
- new version 5.0.6

* Fri Apr 23 2021 Lubos Uhliarik <luhliari@redhat.com> - 7:5.0.5-4
- Related: #1934919 - squid update attempts fail with file conflicts

* Fri Mar 05 2021 Lubos Uhliarik <luhliari@redhat.com> - 7:5.0.5-3
- Resolves: #1934919 - squid update attempts fail with file conflicts

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7:5.0.5-2
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Wed Feb 10 2021 Lubos Uhliarik <luhliari@redhat.com> - 7:5.0.5-1
- new version 5.0.5

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Oct 17 2020 Jeff Law <law@redhat.com> - 7:4.13-2
- Fix missing #includes for gcc-11

* Tue Aug 25 2020 Lubos Uhliarik <luhliari@redhat.com> - 7:4.13-1
- new version 4.13

* Fri Aug 07 2020 Jeff law <law@redhat.com> - 7:4.12-4
- Disable LTO

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.12-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 15 2020 Lubos Uhliarik <luhliari@redhat.com> - 7:4.12-1
- new version 4.12

* Thu May 07 2020 Lubos Uhliarik <luhliari@redhat.com> - 7:4.11-1
- new version 4.11
- libsystemd integration
- Resolves: #1827564 - CVE-2020-11945 squid: improper access restriction upon
  Digest Authentication nonce replay could lead to remote code execution

* Thu Mar 26 2020 Lubos Uhliarik <luhliari@redhat.com> - 7:4.10-4
- Resolves: #1817208 - More cache_swap.sh optimizations

* Wed Mar 25 2020 Lubos Uhliarik <luhliari@redhat.com> - 7:4.10-3
- Resolves: #1786485 - squid.service: use ${SQUID_CONF} rather than $SQUID_CONF
- Resolves: #1798535 - CVE-2019-12528 squid: Information Disclosure issue in
  FTP Gateway
- Resolves: #1798554 - CVE-2020-8450 squid: Buffer overflow in a Squid acting
  as reverse-proxy
- Resolves: #1798541 - CVE-2020-8449 squid: Improper input validation issues 
  in HTTP Request processing

* Tue Jan 28 2020 Lubos Uhliarik <luhliari@redhat.com> - 7:4.10-1
- new version 4.10

* Tue Dec 17 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.9-3
- Resolves: #1784383 - Add BuildRequires: systemd-rpm-macros
- Resolves: #1783757 - Build with ./configure --with-pidfile=/run/squid.pid
- Resolves: #1783768 - Optimize cache_swap.sh cache_dir search

* Mon Nov 11 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.9-2
- new version 4.9
- verify src taball signature by default in prep section

* Tue Oct 08 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.8-6
- Resolves: #1741342 - Do not call autoconf at build time

* Tue Oct 08 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.8-5
- Resolves: #1716950 - Drop "sleep 1" from logrotate fragment

* Thu Aug 22 2019 Lubomir Rintel <lkundrak@v3.sk> - 7:4.8-4
- Move the NetworkManager dispatcher script out of /etc

* Mon Aug 05 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.8-3
- Resolves: #1737030 - depend on httpd-filesystem

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 10 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.8-1
- new version 4.8
- Resolves: #1727745 - squid: CVe-2019-13345 squid: XSS via user_name or auth
  parameter in cachemgr.cgi

* Tue Jul 02 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.7-6
- fix filepath to squid.conf.documented in squid's manpage
- fix path to systemctl in nm script

* Wed May 22 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.7-5
- Related: #1709299 - Use upstream squid.service

* Fri May 17 2019 Luboš Uhliarik <luhliari@redhat.com> - 7:4.7-1
- new version 4.7

* Fri May 17 2019 Luboš Uhliarik <luhliari@redhat.com> - 7:4.6-3
- Resolves: #1709299 - Use upstream squid.service

* Mon Apr 29 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.6-2
- Resolves: #1599074 - squid: 3 coredumps every day

* Wed Apr 24 2019 Lubos Uhliarik <luhliari@redhat.com> - 7:4.6-1
- new version 4.6
- disabled strict checking due to gcc warnings

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 7:4.4-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Mon Dec 10 2018 Lubos Uhliarik <luhliari@redhat.com> - 7:4.4-1
- new version 4.4

* Sun Oct 14 2018 Peter Robinson <pbrobinson@fedoraproject.org> 7:4.2-3
- Drop obsolete legacy sys-v remanents

* Mon Aug 20 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.2-2
- Resolves: #1618790 - SELinux 'dac_override' denial for cache_swap.sh

* Mon Aug 06 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.2-1
- new version 4.2
- enable back strict error checking

* Wed Aug 01 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.1-1
- new version 4.1

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jun 28 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.25-1
- new version 4.0.25

* Mon Jun 04 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.24-2
- removed obsolete BuildRequires (libdb4-devel)

* Thu Mar 08 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.24-1
- new version 4.0.24
- disabled strict checking (removed -Werror)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.0.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 23 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.23-2
- Resolves: #1481195 - squid loses some REs when optimising ACLs

* Tue Jan 23 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.23-1
- new version 4.0.23

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 7:4.0.22-2
- Rebuilt for switch to libxcrypt

* Wed Jan 17 2018 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.22-1
- new version 4.0.22
- Removed NIS helper (#1531540)

* Mon Aug 07 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.21-1
- new version 4.0.21

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 05 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.20-2
- related: new version 4.0.20

* Mon Jun 05 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.20-1
- new version 4.0.20

* Tue Apr 25 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.19-4
- Related: #1445255 - Squid SMP Mode Fails

* Tue Apr 25 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.19-3
- Resolves: #1445255 - Squid SMP Mode Fails

* Tue Apr 18 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.19-2
- Resolves: #1442375 - squid helper squid_kerb_ldap not included in package

* Mon Apr 03 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.19-1
- new version 4.0.19

* Thu Mar 30 2017 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.18-1
- new version 4.0.18

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7:4.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.17-1
- new version 4.0.17

* Mon Oct 31 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.16-1
- new version 4.0.16

* Mon Oct 10 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.15-1
- new version 4.0.15

* Mon Sep 12 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.14-1
- new version 4.0.14

* Tue Aug 09 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:4.0.13-1
- new version 4.0.13

* Mon Jul 11 2016 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:4.0.11-1
- new version 4.0.11

* Wed May 18 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.19-2
- Resolves: #1336993 - Mistyped command in dirname
  /etc/NetworkManager/dispatcher.d/20-squid

* Tue May 10 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.19-1
- new version 3.5.19

* Thu May 05 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.17-1
- new version 3.5.17

* Tue Apr 05 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.16-1
- new version 3.5.16

* Tue Mar 01 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.15-1
- new version 3.5.15
- Resolves: #1311585 - squid: Multiple Denial of Service issues in
  HTTP Response processing
- Resolves: #1312267 - squid: SQUID-2016_2 advisory, multiple DoS issues

* Tue Mar 01 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.13-3
- Resolves: #1308866 - CVE-2016-2390 squid: incorrect server error 
  handling resulting in denial of service

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7:3.5.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.13-1
- new version 3.5.13

* Thu Dec 03 2015 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.12-2
- new version 3.5.12

* Fri Sep 25 2015 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.9-3
- Resolves: #1231992

* Fri Sep 25 2015 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.9-2
- Resolves: #1230501

* Thu Sep 24 2015 Luboš Uhliarik <luhliari@redhat.com> - 7:3.5.9-1
- new version 3.5.9
- added Patch, which fixes problem with include guards 

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.5.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 7:3.5.3-4
- Rebuilt for GCC 5 C++11 ABI change

* Tue Mar 31 2015 Pavel Šimerda <psimerda@redhat.com> - 7:3.5.3-3
- Fix build by removing eDirectory support

* Tue Mar 31 2015 Pavel Šimerda <psimerda@redhat.com> - 7:3.5.3-2
- clean up defunct patches

* Tue Mar 31 2015 Pavel Šimerda <psimerda@redhat.com> - 7:3.5.3-1
- new version 3.5.3

* Mon Mar 23 2015 Pavel Šimerda <psimerda@redhat.com> - 7:3.5.2-4
- Resolves: #1145235, #1173488, #1176318 – revert a couple of recent changes

* Sun Mar 15 2015 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.5.2-3
- Correct execmod build issue caused by libtool confusion on
  required compiler flags

* Sun Mar 15 2015 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.5.2-2
- Update to latest upstream version 3.5.2
- Remove deprecated (and renamed) squid_msnt_auth basic auth helper. Only
  performs LM authentication and not considered useful in todays networks.

* Wed Feb 25 2015 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.4.12-1
- Update to latest upstream version 3.4.12
- bug #1173946: Disable -march=native compile time optimization, use Fedora defaults.

* Tue Nov 18 2014 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.4.9-3
- Update to latest upstream version 3.4.9

* Sun Oct 19 2014 Peter Robinson <pbrobinson@fedoraproject.org> 7:3.4.7-3
- Update ppc64 macro to cover little endian too

* Thu Sep 11 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.7-2
- Fixed: CVE-2014-6270

* Thu Aug 28 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.7-1
- Update to latest upstream version
- Fixed: CVE-2014-3609

* Thu Aug 21 2014 Kevin Fenzi <kevin@scrye.com> - 7:3.4.6-3
- Rebuild for rpm bug 1131960

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jul 2 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.6-1
- Update to latest upstream version 3.4.6

* Fri Jun 13 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.5-6
- Fixed #855111: set unlimited start and shutdown timeout

* Sun Jun 08 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.5-5
- Run squid under user and group squid

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.4.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue May 27 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.5-3
- Remove sysvinit subpackage 
- Enable rock store

* Fri May 23 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.5-2
- Fixed #1099970: missing /var/run/squid folder
- Reverted #1038160: breaks SMP mode

* Tue May 6 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.5-1
- Update to latest upstream version 3.4.5

* Fri Apr 25 2014 Michal Luscon <mluscon@redhat.com> - 7:3.4.4.2-1
- Update to latest upstream version 3.4.4.2

* Thu Mar 13 2014 Pavel Šimerda <psimerda@redhat.com> - 7:3.4.4-1
- bump to 3.4.4

* Tue Feb 04 2014 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.4.3-1
- Update to latest upstream bugfix version 3.4.3

* Mon Jan 06 2014 Pavel Šimerda <psimerda@redhat.com> - 7:3.4.1-2
- Resolves: #1038160 - avoid running squid's own supervisor process

* Mon Dec 30 2013 Michal Luscon <mluscon@redhat.com> - 7:3.4.1-1
- Rebase to latest stable upstream release 3.4.1
- Fixed #1034306: fails to build for AArch64
- Fixed: active ftp

* Tue Dec 03 2013 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.3.11-1
- Update to latest upstream bugfix version 3.3.11

* Fri Sep 13 2013 Michal Luscon <mluscon@redhat.com> - 7:3.3.9-1
- Update to latest upstream version 3.3.9
- Fixed #976815: file descriptors are hard coded to 16384
- Fixed: active ftp crashing
- Fixed: offset of patches

* Thu Aug 08 2013 Michal Luscon <mluscon@redhat.com> - 7:3.3.8-3
- Fixed #994814: enable time_quota helper

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.3.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 Michal Luscon <mluscon@redhat.com> - 7:3.3.8-1
- Update to latest upstream version 3.3.8
- Fixed: CVE-2013-4123
- Fixed: CVE-2013-4115

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 7:3.3.4-3
- Perl 5.18 rebuild

* Wed May  8 2013 Ville Skyttä <ville.skytta@iki.fi> - 7:3.3.4-2
- Fix basic auth and log daemon DB helper builds.
- Use xz compressed tarball, fix source URLs.
- Fix bogus dates in %%changelog.

* Fri May 3 2013 Michal Luscon <nluscon@redhat.com> - 7:3.3.4-1
- Rebase to latest upstream version 3.3.4

* Tue Apr 23 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.9-3
- Option '-k' is not stated in squidclient man
- Remove pid from service file(#913262)

* Fri Apr 19 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.9-2
- Enable full RELRO (-Wl,-z,relro -Wl,-z,now)

* Tue Mar 19 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.9-1
- Update to latest upstream version 3.2.9
- Fixed: CVE-2013-1839
- Removed: makefile-patch (+make check)

* Mon Mar 11 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.8-3
- Resolved: /usr move - squid service file

* Sat Mar 09 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.8-2
- Resolved: #896127 - basic_ncsa_auth does not work

* Fri Mar 08 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.8-1
- Update to latest upstream version 3.2.8
- Fixed rawhide build issues (-make check)

* Thu Feb 07 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.7-1
- Update to latest upstream version 3.2.7

* Thu Jan 24 2013 Michal Luscon <mluscon@redhat.com> - 7:3.2.5-2
- CVE-2013-0189: Incomplete fix for the CVE-2012-5643

* Mon Dec 17 2012 Michal Luscon <mluscon@redhat.com> - 7:3.2.5-1
- Update to latest upstream version 3.2.5

* Mon Nov 05 2012 Michal Luscon <mluscon@redhat.com> - 7:3.2.3-3
- Resolved: #71483 - httpd 2.4 requires new configuration directives

* Fri Oct 26 2012 Michal Luscon <mluscon@redhat.com> - 7:3.2.3-2
- Resolved: #854356 - squid.service use PIDFile
- Resolved: #859393 - Improve cache_swap script
- Resolved: #791129 - disk space warning
- Resolved: #862252 - reload on VPN or network up/down
- Resolved: #867531 - run test suite during build
- Resolved: #832684 - missing after dependency nss-lookup.target
- Removed obsolete configure options

* Mon Oct 22 2012 Tomas Hozza <thozza@redhat.com> - 7:3.2.3-1
- Update to latest upstream version 3.2.3

* Tue Oct 16 2012 Tomas Hozza <thozza@redhat.com> - 7:3.2.2-1
- Update to latest upstream version 3.2.2

* Fri Oct 05 2012 Tomas Hozza <thozza@redhat.com> - 7:3.2.1-2
- Introduced new systemd-rpm macros in squid spec file. (#850326)

* Wed Aug 29 2012 Michal Luscon <mluscon@redhat.com> - 7:3.2.1-1
- Update to latest upstream 3.2.1

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.2.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Apr 02 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.2.0.16-2
- Enable SSL CRTD for ssl bump

* Wed Mar 07 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.2.0.16-1
- Upstream 3.2.0.16 bugfix release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.2.0.15-2
- Rebuilt for c++ ABI breakage

* Mon Feb 06 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.2.0.15-1
- Upstream 3.2.0.15 bugfix release

* Wed Feb 01 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.2.0.14-7
- update with upstreamed patch versions

* Tue Jan 17 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.2.0.14-6
- upstream gcc-4.7 patch
- fix for bug #772483 running out of memory, mem_node growing out of bounds

* Mon Jan 16 2012 Jiri Skala <jskala@redhat.com> - 7:3.2.0.14-5
- fixes FTBFS due to gcc-4.7

* Fri Jan 13 2012 Jiri Skala <jskala@redhat.com> - 7:3.2.0.14-4
- fixes #772481 - Low number of open files for squid process
- fixes FTBFS due to gcc4.7

* Thu Jan 05 2012 Henrik Nordstrom <henrik@henriknordstrom.net> - 3.2.0.14-3
- rebuild for gcc-4.7.0

* Mon Dec 19 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.14-2
- fixes #768586 - Please enable eCAP support again

* Wed Dec 14 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.14-1
- update to latest upstream 3.2.0.14

* Mon Nov 07 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.13-5
- fixes #751679 - host_strict_verify setting inverted in squid.conf

* Thu Nov 03 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.13-4
- fixes #750550 - Squid might depend on named

* Wed Oct 26 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.13-3
- added upstream fix for #747125

* Wed Oct 26 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.13-2
- fixes #747103 - squid does not start if /var/spool/squid is empty
- fixes #747110 - squid does not start adding "memory_pools off"

* Mon Oct 17 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.13-1
- update to latest upstream 3.2.0.13

* Tue Sep 20 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.12-1
- update to latest upstream 3.2.0.12

* Mon Aug 29 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.2.0.11-3
- update to latest upstream 3.2.0.11

* Sat Aug 27 2011 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.2.0.10-3
- Fix for SQUID-2011:3 Gopher vulnerability

* Thu Aug 18 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.10-2
- rebuild for rpm

* Mon Aug 01 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.10-1
- update to latest upsteam 3.2.0.10

* Mon Aug 01 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.9-2
- rebuild for libcap

* Tue Jun 07 2011 Jiri Skala <jskala@redhat.com> - 7:3.2.0.9-1
- upgrade to squid-3.2
- fixes #720445 - Provide native systemd unit file
- SysV initscript moved to subpackage
- temproary disabled eCap

* Wed May 18 2011 Jiri Skala <jskala@redhat.com> - 7:3.1.12-3
- enabled eCAP support

* Wed May 04 2011 Jiri Skala <jskala@redhat.com> - 7:3.1.12-2
- applied corrections of unused patch (Ismail Dönmez)

* Fri Apr 15 2011 Jiri Skala <jskala@redhat.com> - 7:3.1.12-1
- Update to 3.1.12 upstream release

* Thu Feb 10 2011 Jiri Skala <jskala@redhat.com> - 7:3.1.11-1
- Update to 3.1.11 upstream release
- fixes issue with unused variale after mass rebuild (gcc-4.6)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 06 2011 Jiri Skala <jskala@redhat.com> - 7:3.1.10-1
- Update to 3.1.10 upstream release

* Fri Nov 05 2010 Jiri Skala <jskala@redhat.com> - 7:3.1.9-5
- rebuild for libxml2

* Mon Nov 01 2010 Jiri Skala <jskala@redhat.com> - 7:3.1.9-4
- fixes #647967 - build with -fPIE option back and dropped proper libltdl usage

* Sat Oct 30 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.9-3
- Bug #647967 - License clarification & spec-file cleanup

* Mon Oct 25 2010 Henrik Nordstrom <henrik@henriknordstrom.net> 7:3.1.9-2
- Upstream 3.1.9 bugfix release

* Wed Oct 13 2010 Jiri Skala <jskala@redhat.com> - 7:3.1.8-2
- fixes #584161 - squid userid not added to wbpriv group

* Sun Sep 05 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.8-1
- Bug #630445: SQUID-2010:3 Denial of service issue

* Tue Aug 24 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.7-1
- Upstream 3.1.7 bugfix release

* Fri Aug 20 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.6-1
- Upstream 3.1.6 bugfix release
- Build with system libtool-ltdl

* Thu Jul 15 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.5-2
- Upstream 3.1.5 bugfix release
- Upstream patch for Bug #614665: Squid crashes with  ident auth
- Upstream patches for various memory leaks

* Mon May 31 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.4-2
- Correct case-insensitiveness in HTTP list header parsing

* Sun May 30 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.4-1
- Upstream 3.1.4 bugfix release, issues relating to IPv6, TPROXY, Memory
  management, follow_x_forwarded_for, and stability fixes

* Fri May 14 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.3-2
- Fully fix #548903 - "comm_open: socket failure: (97) Address family not supported by protocol" if IPv6 disabled
- Various IPv6 related issues fixed, making tcp_outgoing_address behave
  as expected and no commResetFD warnings when using tproxy setups.

* Sun May 02 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.3-1
- Update to 3.1.3 Upstream bugfix release, fixing WCCPv1

* Mon Apr 19 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.1-4
- Bug #583489: Adjust logrotate script to changes in logrotate package.

* Mon Apr 19 2010 Jiri Skala <jskala@redhat.com>
- fixes #548903 - "comm_open: socket failure: (97) Address family not supported by protocol" if IPv6 disabled

* Tue Mar 30 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.1-2
- Update to 3.1.1 Squid bug #2827 crash with assertion failed:
  FilledChecklist.cc:90: "conn() != NULL" under high load.

* Mon Mar 15 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.18-1
- Upgrade to 3.1.0.18 fixing Digest authentication and improved HTTP/1.1 support

* Sun Feb 28 2010 Henrik Nordstrom <henrik@henriknordstrom.net> -  7:3.1.0.17-3
- Bug 569120, fails to open unbound ipv4 listening sockets

* Thu Feb 25 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.17-2
- Upgrade to 3.1.0.17

* Thu Feb 18 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.16-7
- Workaround for Fedora-13 build failure

* Sun Feb 14 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.16-6
- Patch for Squid security advisory SQUID-2010:2, denial of service
  issue in HTCP processing (CVE-2010-0639)

* Sun Feb 07 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.16-5
- Rebuild 3.1.0.16 with corrected upstream release.

* Wed Feb 03 2010 Jiri Skala <jskala@redhat.com> - 7:3.1.0.16-4
- spec file modified to be fedora packaging guidline compliant
- little shifting lines in init script header due to rpmlint complaint
- fixes assertion during start up

* Mon Feb 01 2010 Henrik Nordstrom <henrik@henriknordstrom.net> 7:3.1.0.16-3
- Upgrade to 3.1.0.16 for DNS related DoS fix (Squid-2010:1)

* Sat Jan 09 2010 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.15-3
- fixed #551302 PROXY needs libcap. Also increases security a little.
- merged relevant upstream bugfixes waiting for next 3.1 release

* Mon Nov 23 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.15-2
- Update to 3.1.0.15 with a number of bugfixes and a workaround for
  ICEcast/SHOUTcast streams.

* Mon Nov 23 2009 Jiri Skala <jskala@redhat.com> 7:3.1.0.14-2
- fixed #532930 Syntactic error in /etc/init.d/squid
- fixed #528453 cannot initialize cache_dir with user specified config file

* Sun Sep 27 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.14-1
- Update to 3.1.0.14

* Sat Sep 26 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.13-7
- Include upstream patches fixing important operational issues
- Enable ESI support now that it does not conflict with normal operation

* Fri Sep 18 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.13-6
- Rotate store.log if enabled

* Wed Sep 16 2009 Tomas Mraz <tmraz@redhat.com> - 7:3.1.0.13-5
- Use password-auth common PAM configuration instead of system-auth

* Tue Sep 15 2009 Jiri Skala <jskala@redhat.com> - 7:3.1.0.13-4
- fixed #521596 - wrong return code of init script

* Tue Sep 08 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.13-3
- Enable squid_kerb_auth

* Mon Sep 07 2009 Henrik Nordstrom <henrik@henriknordtrom.net> - 7:3.1.0.13-2
- Cleaned up packaging to ease future maintenance

* Fri Sep 04 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.1.0.13-1
- Upgrade to next upstream release 3.1.0.13 with many new features
  * IPv6 support
  * NTLM-passthru
  * Kerberos/Negotiate authentication scheme support
  * Localized error pages based on browser language preferences
  * Follow X-Forwarded-For capability
  * and more..

* Mon Aug 31 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 3.0.STABLE18-3
- Bug #520445 silence logrotate when Squid is not running

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 7:3.0.STABLE18-2
- rebuilt with new openssl

* Tue Aug 04 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE18-1
- Update to 3.0.STABLE18

* Sat Aug 01 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE17-3
- Squid Bug #2728: regression: assertion failed: http.cc:705: "!eof"

* Mon Jul 27 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE17-2
- Bug #514014, update to 3.0.STABLE17 fixing the denial of service issues
  mentioned in Squid security advisory SQUID-2009_2.

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.0.STABLE16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 01 2009 Jiri Skala <jskala@redhat.com> 7:3.0.STABLE16-2
- fixed patch parameter of bXXX patches

* Mon Jun 29 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE16-1
- Upgrade to 3.0.STABLE16

* Sat May 23 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE15-2
- Bug #453304 - Squid requires restart after Network Manager connection setup

* Sat May 09 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE15-1
- Upgrade to 3.0.STABLE15

* Tue Apr 28 2009 Jiri Skala <jskala@redhat.com> - 7:3.0.STABLE14-3
- fixed ambiguous condition in the init script (exit 4)

* Mon Apr 20 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE14-2
- Squid bug #2635: assertion failed: HttpHeader.cc:1196: "Headers[id].type == ftInt64"

* Sun Apr 19 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE14-1
- Upgrade to 3.0.STABLE14

* Fri Mar 06 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE13-2
- backported logfile.cc syslog parameters patch from 3.1 (b9443.patch)
- GCC-4.4 workaround in src/wccp2.cc

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7:3.0.STABLE13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 5 2009 Jonathan Steffan <jsteffan@fedoraproject.org> - 7:3.0.STABLE13-1
- upgrade to latest upstream

* Tue Jan 27 2009 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE12-1
- upgrade to latest upstream

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 7:3.0.STABLE10-4
- rebuild with new openssl

* Fri Dec 19 2008 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE10-3
- actually include the upstream bugfixes in the build

* Fri Dec 19 2008 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE10-2
- upstream bugfixes for cache corruption and access.log response size errors

* Fri Oct 24 2008 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE10-1
- upgrade to latest upstream

* Sun Oct 19 2008 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE9-2
- disable coss support, not officially supported in 3.0

* Sun Oct 19 2008 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE9-1
- update to latest upstream

* Thu Oct 09 2008 Henrik Nordstrom <henrik@henriknordstrom.net> - 7:3.0.STABLE7-4
- change logrotate to move instead of copytruncate

* Wed Oct 08 2008 Jiri Skala <jskala@redhat.com> - 7:3.0.STABLE7-3
- fix #465052 -  FTBFS squid-3.0.STABLE7-1.fc10

* Thu Aug 14 2008 Jiri Skala <jskala@redhat.com> - 7:3.0.STABLE7-2
- used ncsa_auth.8 from man-pages. there will be this file removed due to conflict
- fix #458593 noisy initscript
- fix #463129 init script tests wrong conf file
- fix #450352 - build.patch patches only generated files

* Wed Jul 02 2008 Jiri Skala <jskala@redhat.com> - 7:3.0.STABLE7-1
- update to latest upstream
- fix #453214

* Mon May 26 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE6-2
- fix bad allocation

* Wed May 21 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE6-1
- upgrade to latest upstream
- fix bad allocation

* Fri May 09 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE5-2
- fix configure detection of netfilter kernel headers (#435499),
  patch by aoliva@redhat.com
- add support for negotiate authentication (#445337)

* Fri May 02 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE5-1
- upgrade to latest upstream

* Tue Apr 08 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE4-1
- upgrade to latest upstream

* Thu Apr 03 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE2-2
- add %%{optflags} to make
- remove warnings about unused return values

* Thu Mar 13 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE2-1
- upgrade to latest upstream 3.0.STABLE2
- check config file before starting (#428998)
- whitespace unification of init script
- some minor path changes in the QUICKSTART file
- configure with the --with-filedescriptors=16384 option

* Tue Feb 26 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE1-3
- change the cache_effective_group default back to none

* Mon Feb 11 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE1-2
- rebuild for 4.3

* Wed Jan 23 2008 Martin Nagy <mnagy@redhat.com> - 7:3.0.STABLE1-1
- upgrade to latest upstream 3.0.STABLE1

* Tue Dec 04 2007 Martin Bacovsky <mbacovsk@redhat.com> - 2.6.STABLE17-1
- upgrade to latest upstream 2.6.STABLE17

* Wed Oct 31 2007 Martin Bacovsky <mbacovsk@redhat.com> - 7:2.6.STABLE16-3
- arp-acl was enabled

* Tue Sep 25 2007 Martin Bacovsky <mbacovsk@redhat.com> - 7:2.6.STABLE16-2
- our fd_config patch was replaced by upstream's version 
- Source1 (FAQ.sgml) points to local source (upstream's moved to wiki)

* Fri Sep 14 2007 Martin Bacovsky <mbacovsk@redhat.com> - 7:2.6.STABLE16-1
- upgrade to latest upstream 2.6.STABLE16

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 7:2.6.STABLE14-2
- Rebuild for selinux ppc32 issue.

* Thu Jul 19 2007 Martin Bacovsky <mbacovsk@redhat.com> - 7:2.6.STABLE14-1
- update to latest upstream 2.6.STABLE14
- resolves: #247064: Initscript Review

* Tue Mar 27 2007 Martin Bacovsky <mbacovsk@redhat.com> - 7:2.6.STABLE12-1
- update to latest upstream 2.6.STABLE12
- Resolves: #233913: squid: unowned directory

* Mon Feb 19 2007 Martin Bacovsky <mbacovsk@redhat.com> - 7:2.6.STABLE9-2
- Resolves: #226431: Merge Review: squid

* Mon Jan 29 2007 Martin Bacovsky <mbacovsk@redhat.com> - 7:2.6.STABLE9-1
- update to the latest upstream

* Sun Jan 14 2007 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE7-1
- update to the latest upstream

* Tue Dec 12 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE6-1
- update to the latest upstream

* Mon Nov  6 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE5-1
- update to the latest upstream

* Thu Oct 26 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE4-4
- added fix for #205568 - marked cachemgr.conf as world readable

* Wed Oct 25 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE4-3
- added fix for #183869 - squid can abort when getting status
- added upstream fixes:
    * Bug #1796: Assertion error HttpHeader.c:914: "str"
    * Bug #1779: Delay pools fairness, correction to first patch
    * Bug #1802: Crash on exit in certain conditions where cache.log is not writeable
    * Bug #1779: Delay pools fairness when multiple connections compete for bandwidth
    * Clarify the select/poll/kqueue/epoll configure --enable/disable options
- reworked fd patch for STABLE4

* Tue Oct 17 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE4-2
- upstream fixes:
  * Accept 00:00-24:00 as a valid time specification (upstream BZ #1794)
  * aioDone() could be called twice
  * Squid reconfiguration (upstream BZ #1800)

* Mon Oct 2 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE4-1
- new upstream
- fixes from upstream bugzilla, items #1782,#1780,#1785,#1719,#1784,#1776

* Tue Sep 5 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE3-2
- added upstream patches for ACL

* Mon Aug 21 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE3-1
- the latest stable upstream

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 7:2.6.STABLE2-3
- added some requirements for pre/post install scripts

* Fri Aug 04 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE2-2
- added patch for #198253 - squid: don't chgrp another pkg's
  files/directory

* Mon Jul 31 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE2-1
- the latest stable upstream
- reworked fd config patch

* Tue Jul 25 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE1-3
- the latest CVS upstream snapshot

* Wed Jul 19 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE1-2
- the latest CVS snapshot

* Tue Jul 18 2006 Martin Stransky <stransky@redhat.com> - 7:2.6.STABLE1-1
- new upstream + the latest CVS snapshot from 2006/07/18
- updated fd config patch
- enabled epoll
- fixed release format (#197405)
- enabled WCCPv2 support (#198642)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 7:2.5.STABLE14-2.1
- rebuild

* Thu Jun 8 2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE14-2
- fix for squid BZ#1511 - assertion failed: HttpReply.c:105: "rep"

* Tue May 30 2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE14-1
- update to new upstream

* Sun May 28 2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE13-5
- fixed libbind patch (#193298)

* Wed May 3  2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE13-4
- added extra group check (#190544)

* Wed Mar 29 2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE13-3
- improved pre script (#187217) - added group switch

* Thu Mar 23 2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE13-2
- removed "--with-large-files" on 64bit arches

* Mon Mar 13 2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE13-1
- update to new upstream

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 7:2.5.STABLE12-5.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Martin Stransky <stransky@redhat.com> - 7:2.5.STABLE12-5
- new upstream patches

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 7:2.5.STABLE12-4.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Wed Dec 28 2005  Martin Stransky <stransky@redhat.com> 7:2.5.STABLE12-4
- added follow-xff patch (#176055)
- samba path fix (#176659)

* Mon Dec 19 2005  Martin Stransky <stransky@redhat.com> 7:2.5.STABLE12-3
- fd-config.patch clean-up
- SMB_BadFetch patch from upstream

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005  Martin Stransky <stransky@redhat.com> 7:2.5.STABLE12-2
- rewriten patch squid-2.5.STABLE10-64bit.patch, it works with
  "--with-large-files" option now
- fix for #72896 - squid does not support > 1024 file descriptors,
  new "--enable-fd-config" option for it.

* Wed Nov 9 2005  Martin Stransky <stransky@redhat.com> 7:2.5.STABLE12-1
- update to STABLE12
- setenv patch

* Mon Oct 24 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE11-6
- fix for delay pool from upstream

* Thu Oct 20 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE11-5
- fix for #171213 - CVE-2005-3258 Squid crash due to malformed FTP response
- more fixes from upstream

* Fri Oct 14 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE11-4
- enabled support for large files (#167503)

* Thu Oct 13 2005 Tomas Mraz <tmraz@redhat.com> 7:2.5.STABLE11-3
- use include instead of pam_stack in pam config

* Thu Sep 29 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE11-2
- added patch for delay pools and some minor fixes

* Fri Sep 23 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE11-1
- update to STABLE11

* Mon Sep 5 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE10-4
- Three upstream patches for #167414
- Spanish and Greek messages
- patch for -D_FORTIFY_SOURCE=2 

* Tue Aug 30 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE10-3
- removed "--enable-truncate" option (#165948)
- added "--enable-cache-digests" option (#102134)
- added "--enable-ident-lookups" option (#161640)
- some clean up (#165949)

* Fri Jul 15 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE10-2
- pam_auth and ncsa_auth have setuid (#162660)

* Thu Jul 7 2005 Martin Stransky <stransky@redhat.com> 7:2.5.STABLE10-1
- new upstream version
- enabled fakeauth utility (#154020)
- enabled digest authentication scheme (#155882)
- all error pages marked as config (#127836)
- patch for 64bit statvfs interface (#153274)
- added httpd config file for cachemgr.cgi (#112725)

* Mon May 16 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE9-7
- Upgrade the upstream -dns_query patch from -4 to -5

* Wed May 11 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE9-6
- More upstream patches, including a fix for
  bz#157456 CAN-2005-1519 DNS lookups unreliable on untrusted networks

* Tue Apr 26 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE9-5
- more upstream patches, including a fix for
  CVE-1999-0710 cachemgr malicious use

* Fri Apr 22 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE9-4
- More upstream patches, including the fixed 2GB patch.
- include the -libbind patch, which prevents squid from using the optional
  -lbind library, even if it's installed.

* Tue Mar 15 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE9-2
- New upstream version, with 14 upstream patches.

* Wed Feb 16 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE8-2
- new upstream version with 4 upstream patches.
- Reorganize spec file to apply upstream patches first

* Tue Feb 1 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE7-4
- Include two more upstream patches for security vulns:
  bz#146783 Correct handling of oversized reply headers
  bz#146778 CAN-2005-0211 Buffer overflow in WCCP recvfrom() call

* Tue Jan 25 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE7-3
- Include more upstream patches, including two for security holes.

* Tue Jan 18 2005 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE7-2
- Add a triggerin on samba-common to make /var/cache/samba/winbindd_privileged
  accessable so that ntlm_auth will work.  It needs to be in this rpm,
  because the Samba RPM can't assume the squid user exists.
  Note that this will only work if the Samba RPM is recent enough to create
  that directory at install time instead of at winbindd startup time.
  That should be samba-common-3.0.0-15 or later.
  This fixes bugzilla #103726
- Clean up extra whitespace in this spec file.
- Add additional upstream patches. (Now 18 upstream patches).
- patch #112 closes CAN-2005-0096 and CAN-2005-0097, remote DOS security holes.
- patch #113 closes CAN-2005-0094, a remote buffer-overflow DOS security hole.
- patch #114 closes CAN-2005-0095, a remote DOS security hole.
- Remove the -nonbl (replaced by #104) and -close (replaced by #111) patches, since
  they're now fixed by upstream patches.

* Mon Oct 25 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE7-1
- new upstream version, with 3 upstream patches.
  Updated the -build and -config patches
- Include patch from Ulrich Drepper <frepper@redhat.com> to more
  intelligently close all file descriptors.

* Mon Oct 18 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE6-3
- include patch from Ulrich Drepper <drepper@redhat.com> to stop
  problems with O_NONBLOCK.  This closes #136049

* Tue Oct 12 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE6-2
- Include fix for CAN-2004-0918

* Tue Sep 28 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE6-1
- New upstream version, with 32 upstream patches.
  This closes #133970, #133931, #131728, #128143, #126726
- Change the permissions on /etc/squid/squid.conf to 640.  This closes
  bugzilla #125007

* Mon Jun 28 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5STABLE5-5
- Merge current upstream patches.
- Fix the -pipe patch to have the correct name of the winbind pipe.

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Apr 5 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE5-2
- Include the first 10 upstream patches
- Add a patch for the correct location of the winbindd pipe.  This closes
  bugzilla #107561
- Remove the change to ssl_support.c from squid-2.5.STABLE3-build patch
  This closes #117851
- Include /etc/pam.d/squid .  This closes #113404
- Include a patch to close #111254 (assignment in assert)
- Change squid.init to put output messages in /var/log/squid/squid.out
  This closes #104697
- Only useradd the squid user if it doesn't already exist, and error out
  if the useradd fails.  This closes #118718.

* Tue Mar 2 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE5-1
- New upstream version, obsoletes many patches.
- Fix --datadir passed to configure.  Configure automatically adds /squid
  so we shouldn't.
- Remove the problematic triggerpostun trigger, since is's broken, and FC2
  never shipped with that old version.
- add %%{?_smp_mflags} to make line.

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 23 2004 Tim Waugh <twaugh@redhat.com>
- Use ':' instead of '.' as separator for chown.

* Fri Feb 20 2004 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE4-3
- Clean up the spec file to work on 64-bit platforms (use %%{_libdir}
  instead of /usr/lib, etc)
- Make the release number in the changelog section agree with reality.
- use -fPIE rather than -fpie.  s390 fails with just -fpie

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Feb 5 2004 Jay Fenlason <fenlason@redhat.com>
- Incorporate many upstream patches
- Include many spec file changes from D.Johnson <dj@www.uk.linux.org>

* Tue Sep 23 2003 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE4-1
- New upstream version.
- Fix the Source: line in this spec file to point to the correct URL.
- redo the -location patch to work with the new upstream version.

* Mon Jun 30 2003 Jay Fenlason <fenlason@redhat.com> 7:2.5.STABLE3-0
- Spec file change to enable the nul storage module. bugzilla #74654
- Upgrade to 2.5STABLE3 with current official patches.
- Added --enable-auth="basic,ntlm": closes bugzilla #90145
- Added --with-winbind-auth-challenge: closes bugzilla #78691
- Added --enable-useragent-log and --enable-referer-log, closes
- bugzilla #91884
# - Changed configure line to enable pie
# (Disabled due to broken compilers on ia64 build machines)
#- Patched to increase the maximum number of file descriptors #72896
#- (disabled for now--needs more testing)

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Bill Nottingham <notting@redhat.com> 7:2.5.STABLE1-1
- update to 2.5.STABLE1

* Wed Nov 27 2002 Tim Powers <timp@redhat.com> 7:2.4.STABLE7-5
- remove unpackaged files from the buildroot

* Tue Aug 27 2002 Nalin Dahyabhai <nalin@redhat.com> 2.4.STABLE7-4
- rebuild

* Wed Jul 31 2002 Karsten Hopp <karsten@redhat.de>
- don't raise an error if the config file is incomplete
  set defaults instead (#69322, #70065)

* Thu Jul 18 2002 Bill Nottingham <notting@redhat.com> 2.4.STABLE7-2
- don't strip binaries

* Mon Jul  8 2002 Bill Nottingham <notting@redhat.com>
- update to 2.4.STABLE7
- fix restart (#53761)

* Tue Jun 25 2002 Bill Nottingham <notting@redhat.com>
- add various upstream bugfix patches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Mar 22 2002 Bill Nottingham <notting@redhat.com>
- 2.4.STABLE6
- turn off carp

* Mon Feb 18 2002 Bill Nottingham <notting@redhat.com>
- 2.4.STABLE3 + patches
- turn off HTCP at request of maintainers
- leave SNMP enabled in the build, but disabled in the default config

* Fri Jan 25 2002 Tim Powers <timp@redhat.com>
- rebuild against new libssl

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- require linuxdoc-tools instead of sgml-tools

* Tue Sep 25 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.STABLE2

* Mon Sep 24 2001 Bill Nottingham <notting@redhat.com>
- add patch to fix FTP crash

* Mon Aug  6 2001 Bill Nottingham <notting@redhat.com>
- fix uninstall (#50411)

* Mon Jul 23 2001 Bill Nottingham <notting@redhat.com>
- add some buildprereqs (#49705)

* Sun Jul 22 2001 Bill Nottingham <notting@redhat.com>
- update FAQ

* Tue Jul 17 2001 Bill Nottingham <notting@redhat.com>
- own /etc/squid, /usr/lib/squid

* Tue Jun 12 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment
- s/Copyright:/License:/

* Tue Apr 24 2001 Bill Nottingham <notting@redhat.com>
- update to 2.4.STABLE1 + patches
- enable some more configure options (#24981)
- oops, ship /etc/sysconfig/squid

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Tue Feb  6 2001 Trond Eivind Glomsrød <teg@redhat.com>
- improve i18n
- make the initscript use the standard OK/FAILED

* Tue Jan 23 2001 Bill Nottingham <notting@redhat.com>
- change i18n mechanism

* Fri Jan 19 2001 Bill Nottingham <notting@redhat.com>
- fix path references in QUICKSTART (#15114)
- fix initscript translations (#24086)
- fix shutdown logic (#24234), patch from <jos@xos.nl>
- add /etc/sysconfig/squid for daemon options & shutdown timeouts
- three more bugfixes from the Squid people
- update FAQ.sgml
- build and ship auth modules (#23611)

* Thu Jan 11 2001 Bill Nottingham <notting@redhat.com>
- initscripts translations

* Mon Jan  8 2001 Bill Nottingham <notting@redhat.com>
- add patch to use mkstemp (greg@wirex.com)

* Fri Dec 01 2000 Bill Nottingham <notting@redhat.com>
- rebuild because of broken fileutils

* Sat Nov 11 2000 Bill Nottingham <notting@redhat.com>
- fix the acl matching cases (only need the second patch)

* Tue Nov  7 2000 Bill Nottingham <notting@redhat.com>
- add two patches to fix domain ACLs
- add 2 bugfix patches from the squid people

* Fri Jul 28 2000 Bill Nottingham <notting@redhat.com>
- clean up init script; fix condrestart
- update to STABLE4, more bugfixes
- update FAQ

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix syntax error in init script
- finish adding condrestart support

* Fri Jul 14 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- prereq /etc/init.d
- add bugfix patch
- update FAQ

* Thu Jun 29 2000 Bill Nottingham <notting@redhat.com>
- fix init script

* Tue Jun 27 2000 Bill Nottingham <notting@redhat.com>
- don't prereq new initscripts

* Mon Jun 26 2000 Bill Nottingham <notting@redhat.com>
- initscript munging

* Sat Jun 10 2000 Bill Nottingham <notting@redhat.com>
- rebuild for exciting FHS stuff

* Wed May 31 2000 Bill Nottingham <notting@redhat.com>
- fix init script again (#11699)
- add --enable-delay-pools (#11695)
- update to STABLE3
- update FAQ

* Fri Apr 28 2000 Bill Nottingham <notting@redhat.com>
- fix init script (#11087)

* Fri Apr  7 2000 Bill Nottingham <notting@redhat.com>
- three more bugfix patches from the squid people
- buildprereq jade, sgmltools

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- make %%pre more portable

* Thu Mar 16 2000 Bill Nottingham <notting@redhat.com>
- bugfix patches
- fix dependency on /usr/local/bin/perl

* Sat Mar  4 2000 Bill Nottingham <notting@redhat.com>
- 2.3.STABLE2

* Mon Feb 14 2000 Bill Nottingham <notting@redhat.com>
- Yet More Bugfix Patches

* Tue Feb  8 2000 Bill Nottingham <notting@redhat.com>
- add more bugfix patches
- --enable-heap-replacement

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fix dependencies

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- grab some bugfix patches

* Mon Jan 10 2000 Bill Nottingham <notting@redhat.com>
- 2.3.STABLE1 (whee, another serial number)

* Tue Dec 21 1999 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix compliance with ftp RFCs
  (http://www.wu-ftpd.org/broken-clients.html)
- Work around a bug in some versions of autoconf
- BuildPrereq sgml-tools - we're using sgml2html

* Mon Oct 18 1999 Bill Nottingham <notting@redhat.com>
- add a couple of bugfix patches

* Wed Oct 13 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE5.
- update FAQ, fix URLs.

* Sat Sep 11 1999 Cristian Gafton <gafton@redhat.com>
- transform restart in reload and add restart to the init script

* Tue Aug 31 1999 Bill Nottingham <notting@redhat.com>
- add squid user as user 23.

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging
- fix conflict between logrotate & squid -k (#4562)

* Wed Jul 28 1999 Bill Nottingham <notting@redhat.com>
- put cachemgr.cgi back in /usr/lib/squid

* Wed Jul 14 1999 Bill Nottingham <notting@redhat.com>
- add webdav bugfix patch (#4027)

* Mon Jul 12 1999 Bill Nottingham <notting@redhat.com>
- fix path to config in squid.init (confuses linuxconf)

* Wed Jul  7 1999 Bill Nottingham <notting@redhat.com>
- 2.2.STABLE4

* Wed Jun 9 1999 Dale Lovelace <dale@redhat.com>
- logrotate changes
- errors from find when /var/spool/squid or
- /var/log/squid didn't exist

* Thu May 20 1999 Bill Nottingham <notting@redhat.com>
- 2.2.STABLE3

* Thu Apr 22 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE.2

* Sun Apr 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.STABLE1

* Thu Apr 15 1999 Bill Nottingham <notting@redhat.com>
- don't need to run groupdel on remove
- fix useradd

* Mon Apr 12 1999 Bill Nottingham <notting@redhat.com>
- fix effective_user (bug #2124)

* Mon Apr  5 1999 Bill Nottingham <notting@redhat.com>
- strip binaries

* Thu Apr  1 1999 Bill Nottingham <notting@redhat.com>
- duh. adduser does require a user name.
- add a serial number

* Tue Mar 30 1999 Bill Nottingham <notting@redhat.com>
- add an adduser in %%pre, too

* Thu Mar 25 1999 Bill Nottingham <notting@redhat.com>
- oog. chkconfig must be in %%preun, not %%postun

* Wed Mar 24 1999 Bill Nottingham <notting@redhat.com>
- switch to using group squid
- turn off icmp (insecure)
- update to 2.2.DEVEL3
- build FAQ docs from source

* Tue Mar 23 1999 Bill Nottingham <notting@redhat.com>
- logrotate changes

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com>
- auto rebuild in the new build environment (release 4)

* Wed Feb 10 1999 Bill Nottingham <notting@redhat.com>
- update to 2.2.PRE2

* Wed Dec 30 1998 Bill Nottingham <notting@redhat.com>
- cache & log dirs shouldn't be world readable
- remove preun script (leave logs & cache @ uninstall)

* Tue Dec 29 1998 Bill Nottingham <notting@redhat.com>
- fix initscript to get cache_dir correct

* Fri Dec 18 1998 Bill Nottingham <notting@redhat.com>
- update to 2.1.PATCH2
- merge in some changes from RHCN version

* Sat Oct 10 1998 Cristian Gafton <gafton@redhat.com>
- strip binaries
- version 1.1.22

* Sun May 10 1998 Cristian Gafton <gafton@redhat.com>
- don't make packages conflict with each other...

* Sat May 02 1998 Cristian Gafton <gafton@redhat.com>
- added a proxy auth patch from Alex deVries <adevries@engsoc.carleton.ca>
- fixed initscripts

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- rebuilt for Manhattan

* Fri Mar 20 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.21/1.NOVM.21

* Mon Mar 02 1998 Cristian Gafton <gafton@redhat.com>
- updated the init script to use reconfigure option to restart squid instead
  of shutdown/restart (both safer and quicker)

* Sat Feb 07 1998 Cristian Gafton <gafton@redhat.com>
- upgraded to 1.1.20
- added the NOVM package and tryied to reduce the mess in the spec file

* Wed Jan 7 1998 Cristian Gafton <gafton@redhat.com>
- first build against glibc
- patched out the use of setresuid(), which is available only on kernels
  2.1.44 and later
