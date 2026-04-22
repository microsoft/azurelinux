# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define VERSION %{version}

%define bind_name bind
%define bind_version 32:9.18.35-2

%if 0%{?fedora} >= 31 || 0%{?rhel} > 8
%if 0%{?fedora} >= 42 || 0%{?rhel} >= 10
    %global openssl_pkcs11_version 1.0
    %global openssl_pkcs11_name pkcs11-provider
    %global softhsm_version 2.6.1
%else
    %global openssl_pkcs11_version 0.4.10-6
    %global openssl_pkcs11_name openssl-pkcs11
    %global softhsm_version 2.5.0-4
%endif
%else
    %global with_bind_pkcs11 1
%endif

Name:           bind-dyndb-ldap
Version:        11.11
Release: 11%{?dist}
Summary:        LDAP back-end plug-in for BIND

License:        GPL-2.0-or-later
URL:            https://releases.pagure.org/bind-dyndb-ldap
Source0:        https://releases.pagure.org/%{name}/%{name}-%{VERSION}.tar.bz2
Source1:        https://releases.pagure.org/%{name}/%{name}-%{VERSION}.tar.bz2.asc

# https://pagure.io/bind-dyndb-ldap/pull-request/244
Patch1:         bind-dyndb-ldap-11.10-check-pr244.patch

BuildRequires:  bind-devel >= %{bind_version}, bind-lite-devel >= %{bind_version}
BuildRequires:  krb5-devel
BuildRequires:  openldap-devel
BuildRequires:  libuuid-devel
BuildRequires:  automake, autoconf, libtool
BuildRequires:  autoconf-archive

# https://bugzilla.redhat.com/show_bug.cgi?id=2165256
Conflicts: bind9-next

%if %{with bind_pkcs11}
BuildRequires:  bind-pkcs11-devel >= %{bind_version}
BuildRequires: make
Requires(pre): bind-pkcs11 >= %{bind_version}
Requires: bind-pkcs11 >= %{bind_version}
Requires: bind-pkcs11-utils >= %{bind_version}
%else
Requires: softhsm >= %{softhsm_version}
Requires: %{openssl_pkcs11_name} >= %{openssl_pkcs11_version}
Requires(pre): %{bind_name} >= %{bind_version}
Requires: %{bind_name} >= %{bind_version}
%endif

%description
This package provides an LDAP back-end plug-in for BIND. It features
support for dynamic updates and internal caching, to lift the load
off of your LDAP server.


%prep
%autosetup -n %{name}-%{VERSION} -p1

%build
autoreconf -fiv
export BIND9_CFLAGS='-I /usr/include/bind9 -DHAVE_TLS -DHAVE_THREAD_LOCAL'
%configure
%make_build


%install
%make_install
mkdir -m 770 -p %{buildroot}/%{_localstatedir}/named/dyndb-ldap

# Remove unwanted files
rm %{buildroot}%{_libdir}/bind/ldap.la
rm -r %{buildroot}%{_datadir}/doc/%{name}


%post
[ -f /etc/named.conf ] || exit 0

# Transform named.conf if it still has old-style API.
PLATFORM=$(uname -m)

if [ $PLATFORM == "x86_64" ] ; then
    LIBPATH=/usr/lib64
else
    LIBPATH=/usr/lib
fi

# The following sed script:
#   - scopes the named.conf changes to dynamic-db
#   - replaces arg "name value" syntax with name "value"
#   - changes dynamic-db header to dyndb
#   - uses the new way the define path to the library
#   - removes no longer supported arguments (library, cache_ttl,
#       psearch, serial_autoincrement, zone_refresh)
while read -r PATTERN
do
    SEDSCRIPT+="$PATTERN"
done <<EOF
/^\s*dynamic-db/,/};/ {

  s/\(\s*\)arg\s\+\(["']\)\([a-zA-Z_]\+\s\)/\1\3\2/g;

  s/^dynamic-db/dyndb/;

  s@\(dyndb "[^"]\+"\)@\1 "$LIBPATH/bind/ldap.so"@;
  s@\(dyndb '[^']\+'\)@\1 '$LIBPATH/bind/ldap.so'@;

  /\s*library[^;]\+;/d;
  /\s*cache_ttl[^;]\+;/d;
  /\s*psearch[^;]\+;/d;
  /\s*serial_autoincrement[^;]\+;/d;
  /\s*zone_refresh[^;]\+;/d;
}
EOF

sed -i.bak -e "$SEDSCRIPT" /etc/named.conf


%files
%doc NEWS README.md COPYING doc/{example,schema}.ldif
%dir %attr(770, root, named) %{_localstatedir}/named/dyndb-ldap
%{_libdir}/bind/ldap.so


%changelog
* Thu Jan 22 2026 Petr Menšík <pemensik@redhat.com> - 11.11-10
- Rebuilt for BIND 9.18.44 (rhbz#2431609)

* Wed Dec 17 2025 Petr Menšík <pemensik@redhat.com> - 11.11-9
- Rebuilt for BIND 9.18.43  (rhbz#2415842)
- Fix CHECK definition

* Fri Oct 24 2025 Petr Menšík <pemensik@redhat.com> - 11.11-8
- Rebuilt for BIND 9.18.41 (rhbz#2405786)

* Thu Aug 21 2025 Petr Menšík <pemensik@redhat.com> - 11.11-7
- Rebuilt for BIND 9.18.39 (rhbz#2389765)

* Thu Aug 14 2025 Petr Menšík <pemensik@redhat.com> - 11.11-6
- Rebuilt for to 9.18.38 (rhbz#2367771)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Apr 25 2025 Petr Menšík <pemensik@redhat.com> - 11.11-4
- Rebuilt for BIND 9.18.36 (rhbz#2346607)

* Tue Apr 01 2025 Alexander Bokovoy <abokovoy@redhat.com> - 11.11-3
- Rebuilt for BIND 9.18.35 and use of OpenSSL provider API

* Mon Feb 03 2025 Petr Menšík <pemensik@redhat.com> - 11.11-2
- Rebuilt for BIND 9.16.33 (rhbz#2342784)

* Thu Jan 23 2025 Thomas Woerner <twoerner@redhat.com> - 11.11-1
- Release 11.11
- Support BIND 9.18

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 11.10-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 20 2024 Adam Williamson <awilliam@redhat.com> - 11.10-34
- Really rebuild for bind 9.18.32

* Thu Dec 12 2024 Petr Menšík <pemensik@redhat.com> - 11.10-33
- Rebuilt for BIND 9.18.32 (rhbz#2331675)

* Thu Nov 14 2024 Petr Menšík <pemensik@redhat.com> - 11.10-32
- Rebuilt for BIND 9.18.31 (rhbz#2319214)

* Fri Oct 04 2024 Petr Menšík <pemensik@redhat.com> - 11.10-31
- Rebuilt for BIND 9.18.30 (rhbz#2306542)

* Wed Jul 31 2024 Petr Menšík <pemensik@redhat.com> - 11.10-30
- Rebuilt for BIND 9.18.28 (#2299467)

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.10-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Apr 22 2024 Petr Menšík <pemensik@redhat.com> - 11.10-28
- Rebuilt for BIND 9.18.25 (rhbz#2270476)

* Sat Feb 17 2024 Petr Menšík <pemensik@redhat.com> - 11.10-27
- Rebuild for BIND 9.18.24 (#2264032)

* Fri Jan 26 2024 Rafael Jeffman <rjeffman@redhat.com> - 11.10-26
- Migrated to SPDX license.

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.10-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.10-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Jan 15 2024 Petr Menšík <pemensik@redhat.com> - 11.10-23
- Rebuilt for BIND 9.18.21 (#2255407)

* Mon Nov 20 2023 Petr Menšík <pemensik@redhat.com> - 11.10-22
- Rebuilt for BIND 9.18.20 (#2249835)

* Mon Sep 25 2023 Petr Menšík <pemensik@redhat.com> - 11.10-21
- Support for bind 9.18.19 (#2232346)
- Require autoconf-archive at build time

* Wed Sep 06 2023 Petr Menšík <pemensik@redhat.com> - 11.10-20
- Rebuilt for BIND 9.18.18 (#2232346)

* Wed Jul 19 2023 Petr Menšík <pemensik@redhat.com> - 11.10-19
- Rebuild for BIND 9.18.17 (#2223913)

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.10-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 21 2023 Petr Menšík <pemensik@redhat.com> - 11.10-17
- Rebuild for BIND 9.18.16 (#2216462)

* Thu May 18 2023 Petr Menšík <pemensik@redhat.com> - 11.10-16
- Rebuild for BIND 9.18.15 (#2207908)

* Sat Apr 22 2023 Petr Menšík <pemensik@redhat.com> - 11.10-15
- Rebuilt for BIND 9.18.14 (#2187996)

* Wed Mar 22 2023 Petr Menšík <pemensik@redhat.com> - 11.10-14
- Rebuilt for BIND 9.18.13 (#2178717)

* Mon Feb 20 2023 Petr Menšík <pemensik@redhat.com> - 11.10-13
- Rebuilt for BIND 9.18.12 (#2170096)

* Sun Jan 29 2023 Adam Williamson <awilliam@redhat.com> - 11.10-12
- Rebuild for BIND 9.18.11 again (tagging mess, again see #2165256)

* Sat Jan 28 2023 Adam Williamson <awilliam@redhat.com> - 11.10-11.2
- Conflict with bind9-next (#2165256)

* Sat Jan 28 2023 Petr Menšík <pemensik@redhat.com> - 11.10-11
- Support for BIND 9.18.11 (#2164395)

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.10-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Petr Menšík <pemensik@redhat.com> - 11.10-9
- Rebuilt for BIND 9.18.10 (#2143258)
- Include changes needed to build with latest BIND9

* Mon Nov 21 2022 Petr Menšík <pemensik@redhat.com> - 11.10-8
- Rebuilt for BIND 9.18.9 (#2143258)
- Support error header change

* Sat Oct 22 2022 Petr Menšík <pemensik@redhat.com> - 11.10-7
- Rebuilt for BIND 9.18.8 (#2136100)

* Wed Sep 21 2022 Petr Menšík <pemensik@redhat.com> - 11.10-6
- Rebuild for BIND 9.18.7 (#2128609)

* Tue Sep 13 2022 Petr Menšík <pemensik@redhat.com> - 11.10-5
- Rebuild for BIND 9.18.6 with fixed PKCS11 (#2122841)

* Tue Aug 30 2022 Petr Menšík <pemensik@redhat.com> - 11.10-4
- Rebuild for BIND 9.18.6 (#2119132)

* Wed Aug 03 2022 Petr Menšík <pemensik@redhat.com> - 11.10-3
- Rebuild for BIND 9.18.5 (#2057493)

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Jun 21 2022 Alexander Bokovoy <abokovoy@redhat.com> - 11.10-1
- Release 11.10
- Support BIND 9.17+

* Mon Jun 20 2022 Petr Menšík <pemensik@redhat.com> - 11.9-17
- Rebuilt for BIND 9.16.30 (#2097312)

* Fri May 27 2022 Petr Menšík <pemensik@redhat.com> - 11.9-16
- Rebuild for BIND 9.16.29 (#2087920)

* Thu Apr 21 2022 Petr Menšík <pemensik@redhat.com> - 11.9-15
- Rebuilt for BIND 9.16.28 (#2076941)

* Fri Mar 18 2022 Petr Menšík <pemensik@redhat.com> - 11.9-14
- Rebuilt for BIND 9.16.27 (#2055120)

* Fri Jan 21 2022 Petr Menšík <pemensik@redhat.com> - 11.9-13
- Rebuild for BIND 9.16.25 (#2042504)

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 11.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Dec 30 2021 Alexander Bokovoy <abokovoy@redhat.com> - 11.9-11
- Rebuild for BIND 9.16.24 (#2035298)

* Wed Dec 15 2021 Petr Menšík <pemensik@redhat.com> - 11.9-10
- Rebuilt for BIND 9.16.23 (#2032934)

* Fri Nov 19 2021 Petr Menšík <pemensik@redhat.com> - 11.9-9
- Rebuilt for BIND 9.16.23 (#2024210)

* Thu Oct 28 2021 Petr Menšík <pemensik@redhat.com> - 11.9-8
- Rebuilt for BIND 9.16.22 (#2017912)

* Fri Sep 17 2021 Petr Menšík <pemensik@redhat.com> - 11.9-7
- Rebuilt for BIND 9.16.21 (#2004385)

* Thu Aug 19 2021 Petr Menšík <pemensik@redhat.com> - 11.9-6
- Rebuilt for BIND 9.16.20 (#1995289)

* Wed Jul 21 2021 Petr Menšík <pemensik@redhat.com> - 11.9-5
- Rebuilt for BIND 9.16.19 (#1984627)

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sat Jun 19 2021 Petr Menšík <pemensik@redhat.com> - 11.9-3
- Rebuilt for BIND 9.16.18

* Thu Jun 17 2021 Petr Menšík <pemensik@redhat.com> - 11.9-2
- Add BIND 9.16.17 support

* Mon May 24 2021 Alexander Bokovoy <abokovoy@redhat.com> - 11.9-1
- New upstream release 11.9

* Fri May 21 2021 Petr Menšík <pemensik@redhat.com> - 11.7-4
- Add BIND 9.16.16 support

* Thu Apr 29 2021 Petr Menšík <pemensik@redhat.com> - 11.7-3
- Rebuilt for BIND 9.16.15

* Fri Mar 26 2021 Petr Menšík <pemensik@redhat.com> - 11.7-2
- Support for BIND 9.16.13

* Wed Feb 24 2021 Alexander Bokovoy <abokovoy@redhat.com> - 11.7-1
- Upstream release 11.7

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 11.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Petr Menšík <pemensik@redhat.com> - 11.6-6
- Rebuilt for BIND 9.16.11

* Fri Jan 15 2021 Petr Menšík <pemensik@redhat.com> - 11.6-5
- Rebuilt for BIND 9.16.10

* Tue Jan 12 2021 Petr Menšík <pemensik@redhat.com> - 11.6-4
- Support BIND 9.16.10
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Dec 17 2020 Alexander Bokovoy <abokovoy@redhat.com> - 11.6-3
- Both require bind and require it for pre-install script
- Resolves: rhbz#1902811

* Thu Dec 17 2020 Alexander Bokovoy <abokovoy@redhat.com> - 11.6-2
- Fix requires to bind: require bind installed before bind-dyndb-ldap
  as we depend on named group

* Mon Nov 23 2020 Alexander Bokovoy <abokovoy@redhat.com> - 11.6-1
- Upstream release 11.6
- Use reference counting semantics in destructors according to BIND version

* Wed Nov 18 2020 Alexander Bokovoy <abokovoy@redhat.com> - 11.5-1
- Upstream release 11.5
- Use OpenSSL pkcs11 engine in BIND instead of native PKCS11

* Fri Oct 23 2020 Petr Menšík <pemensik@redhat.com> - 11.3-5
- Rebuilt for bind 9.11.24

* Fri Aug 21 2020 Petr Menšík <pemensik@redhat.com> - 11.3-4
- Rebuilt for bind 9.11.22

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.3-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jun 08 2020 Alexander Bokovoy <abokovoy@redhat.com> - 11.3-1
- Upstream release 11.3

* Tue Mar 31 2020 Petr Menšík <pemensik@redhat.com> - 11.2-5
- Rebuilt for bind 9.11.17

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 11.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 25 2019 Petr Menšík <pemensik@redhat.com> - 11.2-3
- Rebuilt for bind 9.11.13

* Mon Nov 11 2019 Petr Menšík <pemensik@redhat.com> - 11.2-2
- Add support for serve-stale, detected on build time

* Tue Nov 05 2019 Alexander Bokovoy <abokovoy@redhat.com> - 11.2-1
- New upstream release v11.2

* Tue Aug 27 2019 Petr Menšík <pemensik@redhat.com> - 11.1-20
- Rebuilt for bind 9.11.10

* Fri Aug 16 2019 Alexander Bokovoy <abokovoy@redhat.com> - 11.1-19
- Fix attribute templating in case of a missing default value
- Resolves: rhbz#1705072

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed Jul 17 2019 Petr Menšík <pemensik@redhat.com> - 11.1-17
- Rebuilt for bind 9.11.8

* Tue Jun 11 2019 Petr Menšík <pemensik@redhat.com> - 11.1-16
- Rebuilt for bind 9.11.7

* Fri May 03 2019 Petr Menšík <pemensik@redhat.com> - 11.1-15
- Rebuilt for bind 9.11.6

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 05 2018 Petr Menšík <pemensik@redhat.com> - 11.1-13
- Support for bind 9.11.5 headers

* Thu Jul 12 2018 Petr Menšík <pemensik@redhat.com> - 11.1-12
- Require bind with writable home, update to 9.11.4

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Mar 01 2018 Petr Menšík <pemensik@redhat.com> - 11.1-10
- Rebuild for bind 9.11.3. Minor tweaks to compile.

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 19 2018 Petr Menšík <pemensik@redhat.com> - 11.1-8
- Rebuild again against bind-9.11.2-P1

* Tue Jan 09 2018 Petr Menšík <pemensik@redhat.com> - 11.1-7
- Rebuild for bind 9.11.2

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 11.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 27 2017 Tomas Krizek <tkrizek@redhat.com> - 11.1-4
- Bump BIND version and fix library dependecies
- Coverity fixes

* Mon Jun 26 2017 Petr Menšík <pemensik@redhat.com> - 11.1-3
- Build with updated libraries

* Mon Mar 13 2017 Tomas Krizek <tkrizek@redhat.com> - 11.1-2
- Fix error poinstall sed script

* Fri Mar 10 2017 Tomas Krizek <tkrizek@redhat.com> - 11.1-1
- Update to 11.1
- Bumped required version of BIND to 9.11.0-6.P2
  (required since bind-dyndb-ldap 11.0-1 release)
- Updated source URL links to pagure

* Fri Feb 10 2017 Tomas Krizek <tkrizek@redhat.com> - 11.0-2
- Patch to fix build warnings (removed duplicate const)

* Thu Feb 09 2017 Tomas Krizek <tkrizek@redhat.com> - 11.0-2
- Added named.conf transformation script as post action

* Thu Dec 15 2016 Tomas Krizek <tkrizek@redhat.com> - 11.0-1
- Update to 11.0

* Mon Nov 21 2016 Petr Menšík <pemensik@redhat.com> - 10.1-2
- Patched to alfa 11.0 with support for BIND 9.11
- Configuration format in named.conf is different
    and incompatible with all previous versions. Please see README.md.
- Minimal BIND version is now 9.11.0rc1. Please see NEWS.

* Wed Aug 17 2016 Petr Spacek <pspacek@redhat.com> - 10.1-1
- Update to 10.1.
- Fix deletion of DNS root zone not to break global forwarding.
  https://fedorahosted.org/bind-dyndb-ldap/ticket/167

* Wed Jul 27 2016 Petr Spacek <pspacek@redhat.com> - 10.0-2
- Backport fix for crash https://fedorahosted.org/bind-dyndb-ldap/ticket/166

* Tue Jun 21 2016 Petr Spacek <pspacek@redhat.com> - 10.0-1
- Update to 10.0

* Fri May 27 2016 Tomas Hozza <thozza@redhat.com> - 9.0-3
- Resolved build issue due to changes in libdns API

* Thu May 26 2016 Tomas Hozza <thozza@redhat.com> - 9.0-2
- Rebuild against bind-9.10.4-P1

* Thu May 12 2016 Petr Spacek <pspacek@redhat.com> - 9.0-1
- Update to 9.0
- Fix for GCC 4.9+ was merged upstream

* Fri Mar 04 2016 Petr Spacek <pspacek@redhat.com> - 8.0-6
- Fix builds with GCC 4.9+

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 8.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 17 2015 Petr Spacek <pspacek@redhat.com> - 8.0-4
- Rebuild against bind 9.10.3-P2

* Fri Sep 04 2015 Tomas Hozza <thozza@redhat.com> - 8.0-3
- Rebuild against bind 9.10.3rc1

* Wed Jun 24 2015 Tomas Hozza <thozza@redhat.com> - 8.0-2
- rebuild against bind-9.10.2-P1

* Tue Jun 23 2015 Petr Spacek <pspacek@redhat.com> - 8.0-1
- update to 8.0

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 13 2015 Tomas Hozza <thozza@redhat.com> - 7.0-4
- rebuild against bind-9.10.2

* Wed Feb 25 2015 Tomas Hozza <thozza@redhat.com> - 7.0-3
- Rebuild against bind-9.10.2rc2

* Mon Feb 02 2015 Tomas Hozza <thozza@redhat.com> - 7.0-2
- rebuild against bind-9.10.2rc1

* Mon Jan 12 2015 Petr Spacek <pspacek@redhat.com> - 7.0-1
- update to 7.0 to add support for BIND 9.10

* Tue Dec 02 2014 Petr Spacek <pspacek@redhat.com> - 6.1-1
- update to 6.1
- drop patches which were merged upstream

* Tue Oct 21 2014 Petr Viktorin <pviktori@redhat.com> - 6.0-5
- use lower version of bind-pkcs11-utils for f20 and el7

* Mon Oct 20 2014 Petr Spacek <pspacek@redhat.com> - 6.0-4
- add dependency on bind-pkcs11-utils >= 32:9.9.6-2
  to help with freeipa-server upgrade

* Mon Oct 20 2014 Petr Spacek <pspacek@redhat.com> - 6.0-3
- replace dependency on bind with dependency on bind-pkcs11 >= 32:9.9.6-2
  to help with freeipa-server upgrade

* Fri Oct 03 2014 Tomas Hozza <thozza@redhat.com> - 6.0-2
- rebuild against bind-9.9.6

* Tue Sep 23 2014 Petr Spacek <pspacek redhat com> - 6.0-1
- update to 6.0

* Fri Sep 12 2014 Petr Spacek <pspacek redhat com> - 5.3-1
- update to 5.3

* Mon Sep 08 2014 Petr Spacek <pspacek redhat com> 5.2-1
- update to 5.2

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 24 2014 Petr Spacek <pspacek redhat com> 5.1-1
- update to 5.1
- fixes bug 1122393

* Tue Jun 24 2014 Petr Spacek <pspacek redhat com> 5.0-1
- update to 5.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr 09 2014 Petr Spacek <pspacek redhat com> 4.3-1
- update to 4.3

* Mon Feb 24 2014 Petr Spacek <pspacek redhat com> 4.1-2
- remove deprecated define _BSD_SOURCE

* Mon Feb 24 2014 Petr Spacek <pspacek redhat com> 4.1-1
- update to 4.1

* Thu Jul 18 2013 Petr Spacek <pspacek redhat com> 3.5-1
- update to 3.5

* Mon Jul 15 2013 Tomas Hozza <thozza@redhat.com> 3.4-2
- rebuild against new bind

* Tue Jun 25 2013 Petr Spacek <pspacek redhat com> 3.4-1
- update to 3.4

* Tue Jun 04 2013 Petr Spacek <pspacek redhat com> 3.3-1
- update to 3.3
- patch bind-dyndb-ldap-tbabej-0001-Build-fixes-for-Fedora-19.patch merged

* Tue May 14 2013 Petr Spacek <pspacek redhat com> 3.2-1
- update to 3.2

* Tue Apr 16 2013 Adam Tkac <atkac redhat com> 3.1-2
- rebuild against new bind
- build with --disable-werror

* Fri Apr 12 2013 Petr Spacek <pspacek redhat com> 3.1-1
- update to 3.1

* Tue Apr 02 2013 Petr Spacek <pspacek redhat com> 3.0-1
- update to 3.0

* Tue Mar 26 2013 Petr Spacek <pspacek redhat com> 2.6-1
- update to 2.6

* Mon Feb 04 2013 Petr Spacek <pspacek redhat com> 2.5-1
- update to 2.5

* Tue Jan 15 2013 Petr Spacek <pspacek redhat com> 2.4-1
- update to 2.4

* Thu Nov  8 2012 Petr Spacek <pspacek redhat com> 2.3-2
- rebuild with proper changelog

* Thu Nov  8 2012 Petr Spacek <pspacek redhat com> 2.3-1
- update to 2.3

* Mon Oct 29 2012 Adam Tkac <atkac redhat com> 2.1-1
- update to 2.1

* Thu Oct 11 2012 Adam Tkac <atkac redhat com> 2.0-0.3.20121009git6a86b1
- rebuild against new bind-libs

* Tue Oct  9 2012 Petr Spacek <pspacek redhat com> 2.0-0.2.20121009git6a86b1
- update to the latest master

* Fri Sep 21 2012 Adam Tkac <atkac redhat com> 2.0-0.1.20120921git7710d89
- update to the latest master
- bind-dyndb-ldap110-master.patch was merged

* Thu Aug 16 2012 Adam Tkac <atkac redhat com> 1.1.0-0.16.rc1
- update to the latest git

* Thu Aug 02 2012 Adam Tkac <atkac redhat com> 1.1.0-0.15.rc1
- update to the latest git
  - fix for CVE-2012-3429 has been merged

* Thu Aug 02 2012 Adam Tkac <atkac redhat com> 1.1.0-0.14.rc1
- fix CVE-2012-3429

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.0-0.13.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Adam Tkac <atkac redhat com> - 1.1.0-0.12.rc1
- update to the latest master (#827401)

* Thu Apr 26 2012 Adam Tkac <atkac redhat com> - 1.1.0-0.11.rc1
- update to 1.1.0rc1 (CVE-2012-2134)

* Tue Mar 27 2012 Adam Tkac <atkac redhat com> - 1.1.0-0.10.b2
- update to 1.1.0b2

* Tue Mar 06 2012 Adam Tkac <atkac redhat com> - 1.1.0-0.9.b1
- update to 1.1.0b1

* Mon Feb 13 2012 Adam Tkac <atkac redhat com> - 1.1.0-0.8.a2
- update to 1.1.0a2

* Thu Feb 02 2012 Adam Tkac <atkac redhat com> - 1.1.0-0.7.a1
- rebuild against new bind

* Wed Jan 18 2012 Adam Tkac <atkac redhat com> - 1.1.0-0.6.a1
- update to 1.1.0a1

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0-0.5.rc1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Nov 14 2011 Adam Tkac <atkac redhat com> - 1.0.0-0.4.rc1
- update to 1.0.0rc1

* Mon Nov 14 2011 Adam Tkac <atkac redhat com> - 1.0.0-0.3.b1
- rebuild against new bind

* Fri Sep 09 2011 Adam Tkac <atkac redhat com> - 1.0.0-0.2.b1
- rebuild against new bind

* Wed Aug 31 2011 Adam Tkac <atkac redhat com> - 1.0.0-0.1.b1
- update to 1.0.0b1 (psearch + bugfixes)
- bind-dyndb-ldap-rh727856.patch merged

* Wed Aug 03 2011 Adam Tkac <atkac redhat com> - 0.2.0-4
- fix race condition in semaphore_wait (#727856)

* Mon Feb 21 2011 Adam Tkac <atkac redhat com> - 0.2.0-3
- rebuild against new bind

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 12 2011 Adam Tkac <atkac redhat com> - 0.2.0-1
- update to 0.2.0
- patches merged
  - 0001-Bugfix-Improve-LDAP-schema-to-be-loadable-by-OpenLDA.patch
  - 0004-Bugfix-Fix-loading-of-child-zones-from-LDAP.patch

* Wed Dec 15 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.17.b
- fix LDAP schema (#622604)
- load child zones from LDAP correctly (#622617)

* Fri Oct 22 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.16.b
- build with correct RPM_OPT_FLAGS (#645529)

* Wed Oct 20 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.15.b
- use "isc-config.sh" utility to get correct BIND9 CFLAGS

* Thu Sep 30 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.14.b
- rebuild against new bind

* Fri Aug 27 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.13.b
- rebuild against new bind

* Tue Aug 17 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.12.b
- rebuild against new bind

* Tue Aug 03 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.11.b
- rebuild against new bind

* Mon May 31 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.10.b
- rebuild against new bind

* Wed Mar 24 2010 Martin Nagy <mnagy@redhat.com> - 0.1.0-0.9.b
- update to the latest upstream release

* Thu Jan 28 2010 Adam Tkac <atkac redhat com> - 0.1.0-0.8.a1.20091210git
- rebuild against new bind

* Tue Dec 15 2009 Adam Tkac <atkac redhat com> - 0.1.0-0.7.a1.20091210git
- rebuild against new bind

* Thu Dec 10 2009 Martin Nagy <mnagy@redhat.com> - 0.1.0-0.6.a1.20091210git
- update to the latest git snapshot
- change upstream URL, project moved to fedorahosted
- change license to GPL version 2 or later
- add epoch to versioned requires
- add krb5-devel to the list of build requires

* Tue Dec 01 2009 Adam Tkac <atkac redhat com> - 0.1.0-0.5.a1
- rebuild against new bind

* Thu Nov 26 2009 Adam Tkac <atkac redhat com> - 0.1.0-0.4.a1
- rebuild against new bind

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.0-0.3.a1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 19 2009 Caolán McNamara <caolanm@redhat.com> - 0.1.0-0.2.a1
- rebuild for dependencies

* Sun May 03 2009 Martin Nagy <mnagy@redhat.com> - 0.1.0-0.1.a1
- initial packaging
