# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%define haproxy_user    haproxy
%define haproxy_group   %{haproxy_user}
%define haproxy_homedir %{_localstatedir}/lib/haproxy
%define haproxy_confdir %{_sysconfdir}/haproxy
%define haproxy_datadir %{_datadir}/haproxy

%global _hardened_build 1

Name:           haproxy
Version:        3.0.5
Release:        4%{?dist}
Summary:        HAProxy reverse proxy for high availability environments

License:        GPL-2.0-or-later

URL:            http://www.haproxy.org/
Source0:        %{url}/download/3.0/src/haproxy-%{version}.tar.gz
Source1:        %{name}.service
Source2:        %{name}.cfg
Source3:        %{name}.logrotate
Source4:        %{name}.sysconfig
Source5:        %{name}.sysusers
Source6:        halog.1

BuildRequires:  gcc
BuildRequires:  libxcrypt-devel
BuildRequires:  lua-devel
BuildRequires:  pcre2-devel
BuildRequires:  openssl-devel
BuildRequires:  systemd-devel
BuildRequires:  systemd
BuildRequires:  systemd-rpm-macros
BuildRequires:  make

Requires(pre):  shadow-utils
%{?systemd_requires}

%description
HAProxy is a TCP/HTTP reverse proxy which is particularly suited for high
availability environments. Indeed, it can:
 - route HTTP requests depending on statically assigned cookies
 - spread load among several servers while assuring server persistence
   through the use of HTTP cookies
 - switch to backup servers in the event a main one fails
 - accept connections to special ports dedicated to service monitoring
 - stop accepting connections without breaking existing ones
 - add, modify, and delete HTTP headers in both directions
 - block requests matching particular patterns
 - report detailed status to authenticated users from a URI
   intercepted from the application

%prep
%setup -q
%build

make %{?_smp_mflags} CPU="generic" TARGET="linux-glibc" USE_OPENSSL=1 USE_PCRE2=1 USE_SLZ=1 USE_LUA=1 USE_CRYPT_H=1 USE_SYSTEMD=1 USE_LINUX_TPROXY=1 USE_GETADDRINFO=1 USE_PROMEX=1 DEFINE=-DMAX_SESS_STKCTR=12 ADDINC="%{build_cflags}" ADDLIB="%{build_ldflags}"

make admin/halog/halog ADDINC="%{build_cflags}" ADDLIB="%{build_ldflags}"

pushd admin/iprange
make OPTIMIZE="%{build_cflags}" LDFLAGS="%{build_ldflags}"
popd

%install
make install-bin DESTDIR=%{buildroot} PREFIX=%{_prefix} SBINDIR=%{_sbindir} TARGET="linux2628"
make install-man DESTDIR=%{buildroot} PREFIX=%{_prefix}

install -p -D -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service
install -p -D -m 0644 %{SOURCE2} %{buildroot}%{haproxy_confdir}/%{name}.cfg
install -p -D -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -p -D -m 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
install -p -D -m 0644 %{SOURCE5} %{buildroot}%{_sysusersdir}/%{name}.conf
install -p -D -m 0644 %{SOURCE6} %{buildroot}%{_mandir}/man1/halog.1
install -d -m 0755 %{buildroot}%{haproxy_homedir}
install -d -m 0755 %{buildroot}%{haproxy_datadir}
install -d -m 0755 %{buildroot}%{haproxy_confdir}/conf.d
install -d -m 0755 %{buildroot}%{_bindir}
install -p -m 0755 ./admin/halog/halog %{buildroot}%{_bindir}/halog
install -p -m 0755 ./admin/iprange/iprange %{buildroot}%{_bindir}/iprange
install -p -m 0755 ./admin/iprange/ip6range %{buildroot}%{_bindir}/ip6range

for httpfile in $(find ./examples/errorfiles/ -type f) 
do
    install -p -m 0644 $httpfile %{buildroot}%{haproxy_datadir}
done

rm -rf ./examples/errorfiles/

find ./examples/* -type f ! -name "*.cfg" -exec rm -f "{}" \;

for textfile in $(find ./ -type f -name '*.txt')
do
    mv $textfile $textfile.old
    iconv --from-code ISO8859-1 --to-code UTF-8 --output $textfile $textfile.old
    rm -f $textfile.old
done

%pre
%sysusers_create_compat %{SOURCE5}

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun_with_restart %{name}.service

%files
%doc doc/* examples/*
%doc CHANGELOG README VERSION
%license LICENSE
%dir %{haproxy_homedir}
%dir %{haproxy_confdir}
%dir %{haproxy_confdir}/conf.d
%dir %{haproxy_datadir}
%{haproxy_datadir}/*
%config(noreplace) %{haproxy_confdir}/%{name}.cfg
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%{_unitdir}/%{name}.service
%{_sbindir}/%{name}
%{_bindir}/halog
%{_bindir}/iprange
%{_bindir}/ip6range
%{_mandir}/man1/*
%{_sysusersdir}/%{name}.conf

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Feb 01 2025 Björn Esser <besser82@fedoraproject.org> - 3.0.5-3
- Add explicit BR: libxcrypt-devel

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Oct 22 2024 Ryan O'Hara <rohara@redhat.com> - 3.0.5-1
- Update to 3.0.5 (#2313555)

* Tue Sep 03 2024 Ryan O'Hara <rohara@redhat.com> - 3.0.4-1
- Update to 3.0.4 (CVE-2024-45506, #2309472)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Ryan O'Hara <rohara@redhat.com> - 3.0.3-1
- Update to 3.0.3 (#2264456)

* Thu Feb 08 2024 Ryan O'Hara <rohara@redhat.com> - 2.9.4-1
- Update to 2.9.4 (#2250339)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Mon Sep 25 2023 Ryan O'Hara <rohara@redhat.com> - 2.8.3-1
- Update to 2.8.3 (#2219397)

* Fri Aug 04 2023 Ryan O'Hara <rohara@redhat.com> - 2.8.1-1
- Update to 2.8.1 (#2219397)

* Fri Aug 04 2023 Ryan O'Hara <rohara@redhat.com> - 2.8.0-3
- Migrate to SPDX license

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 08 2023 Ryan O'Hara <rohara@redhat.com> - 2.8.0-1
- Update to 2.8.0 (#2203868)

* Tue Apr 04 2023 Ryan O'Hara <rohara@redhat.com> - 2.7.6-1
- Update to 2.7.6 (#2182310)

* Thu Mar 23 2023 Ryan O'Hara <rohara@redhat.com> - 2.7.5-1
- Update to 2.7.5 (#2154925)

* Wed Feb 15 2023 Ryan O'Hara <rohara@redhat.com> - 2.7.3-1
- Update to 2.7.3 (#2154925)
- Reject invalid response header (CVE-2023-0056, #2161138)
- Fix request smuggling attack (CVE-2023-25725, #2169823)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 05 2022 Ryan O'Hara <rohara@redhat.com> - 2.7.0-1
- Update to 2.7.0 (#2150028)

* Tue Nov 29 2022 Ryan O'Hara <rohara@redhat.com> - 2.6.6-4
- Fix Source0 URL (#2139126)

* Tue Oct 11 2022 Ryan O'Hara <rohara@redhat.com> - 2.6.6-3
- Use systemd-sysusers (#2134206)

* Tue Oct 11 2022 Ryan O'Hara <rohara@redhat.com> - 2.6.6-2
- Remove USE_REGPARM (#2097885)

* Tue Oct 11 2022 Ryan O'Hara <rohara@redhat.com> - 2.6.6-1
- Update to 2.6.6 (#2099745)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jun 03 2022 Ryan O'Hara <rohara@redhat.com> - 2.6.0-2
- Add conf.d directory and update systemd unit file (#2093483)

* Fri Jun 03 2022 Ryan O'Hara <rohara@redhat.com> - 2.6.0-1
- Update to 2.6.0 (#2092069)

* Wed May 25 2022 Ryan O'Hara <rohara@redhat.com> - 2.5.7-1
- Update to 2.5.7 (#2026009)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Nov 15 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.8-3
- Fix OpenSSL 3.0 build (#2022031)

* Thu Nov 04 2021 Matt Raffert <mjrafferty0@gmail.com> - 2.4.8-2
- Increase available sticky counters (#2012912)

* Thu Nov 04 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.8-1
- Update to 2.4.8 (#2019823)

* Wed Oct 13 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.7-1
- Update to 2.4.7 (#2009817)

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 2.4.4-2
- Rebuilt with OpenSSL 3.0.0

* Tue Sep 07 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.4-1
- Update to 2.4.4 (#2002008)

* Tue Aug 17 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.3-1
- Update to 2.4.3 (#1960565)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.4.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 14 2021 Petr Pisar <ppisar@redhat.com> - 2.4.2-2
- Rebuild against pcre2-10.37 (bug #1965025)

* Mon Jul 12 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.2-1
- Update to 2.4.2 (#1960565)

* Thu Jun 03 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.0-5
- Fix usage of build flags

* Mon May 17 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.0-4
- Fix path of contrib/admin tools

* Mon May 17 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.0-3
- Use SLZ instead of ZLIB

* Mon May 17 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.0-2
- Add USE_PROMEX=1 for prometheus exporter

* Mon May 17 2021 Ryan O'Hara <rohara@redhat.com> - 2.4.0-1
- Update to 2.4.0 (#1960565)

* Mon Apr 26 2021 Ryan O'Hara <rohara@redhat.com> - 2.3.10-1
- Update to 2.3.10 (#1953018)

* Tue Apr 06 2021 Ryan O'Hara <rohara@redhat.com> - 2.3.9-1
- Update to 2.3.9 (#1934647)

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.3.5-3
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Mon Feb 08 2021 Ryan O'Hara <rohara@redhat.com> - 2.3.5-2
- Fix source URL

* Mon Feb 08 2021 Ryan O'Hara <rohara@redhat.com> - 2.3.5-1
- Update to 2.3.5 (#1925774)

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Jan 14 2021 Ryan O'Hara <rohara@redhat.com> - 2.3.4-1
- Update to 2.3.4 (#1914447)

* Tue Dec 08 2020 Ryan O'Hara <rohara@redhat.com> - 2.3.2-1
- Update to 2.3.2 (#1894994)

* Thu Oct 01 2020 Ryan O'Hara <rohara@redhat.com> - 2.2.4-1
- Update to 2.2.4 (#1883742)
    
* Thu Sep 17 2020 Ryan O'Hara <rohara@redhat.com> - 2.2.3-2
- Fix build for late loading of libgcc_s

* Mon Sep 14 2020 Ryan O'Hara <rohara@redhat.com> - 2.2.3-1
- Update to 2.2.3 (#1876932)
    
* Fri Jul 31 2020 Ryan O'Hara <rohara@redhat.com> - 2.2.2-1
- Update to 2.2.2 (#1862400)

* Mon Jul 27 2020 Ryan O'Hara <rohara@redhat.com> - 2.2.1-1
- Update to 2.2.1 (#1859846)

* Wed Jul 15 2020 Ryan O'Hara <rohara@redhat.com> - 2.2.0-3
- Update systemd service file

* Fri Jul 10 2020 Tom Callaway <spot@fedoraproject.org> - 2.2.0-2
- Fix build against lua 5.4

* Thu Jul 09 2020 Ryan O'Hara <rohara@redhat.com> - 2.2.0-1
- Update to 2.2.0 (#1854519)

* Mon Jun 15 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.7-1
- Update to 2.1.7 (#1845001)

* Mon Jun 08 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.6-1
- Update to 2.1.6 (#1845001)

* Mon Jun 01 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.5-1
- Update to 2.1.5 (#1841837)

* Thu Apr 02 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.4-1
- Update to 2.1.4 (CVE-2010-11100, #1820200)

* Mon Mar 16 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.3-2
- Fix invalid element address calculation (#1801109)

* Wed Feb 12 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.3-1
- Update to 2.1.3 (#1802233)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jan 02 2020 Ryan O'Hara <rohara@redhat.com> - 2.1.2-1
- Update to 2.1.2 (#1782472)

* Mon Nov 25 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.10-1
- Update to 2.0.10 (#1772961)

* Wed Nov 06 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.8-1
- Update to 2.0.8 (#1764483)

* Mon Oct 21 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.7-2
- Build with Prometheus exporter service (#1755839)

* Mon Oct 21 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.7-1
- Update to 2.0.7 (#1742544)

* Fri Sep 13 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.6-1
- Update to 2.0.6 (#1742544)

* Mon Aug 19 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.5-1
- Update to 2.0.5 (#1742544)

* Tue Jul 30 2019 Ryan O'Hara <rohara@redhat.com> - 2.0.3-1
- Update to 2.0.3 (#1690492)

* Tue Jul 30 2019 Ryan O'Hara <rohara@redhat.com> - 1.8.20-3
- Build with PCRE2 (#1669217)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri May 17 2019 Ryan O'Hara <rohara@redhat.com> - 1.8.20-1
- Update to 1.8.20

* Wed Feb 13 2019 Ryan O'Hara <rohara@redhat.com> - 1.8.19-1
- Update to 1.8.19

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jan 24 2019 Petr Pisar <ppisar@redhat.com> - 1.8.17-3
- Rebuild against patched libpcreposix library (bug #1667614)

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 1.8.17-2
- Rebuilt for libcrypt.so.2 (#1666033)

* Wed Jan 09 2019 Ryan O'Hara <rohara@redhat.com> - 1.8.17-1
- Update to 1.8.17
- Fix handling of priority flag in HEADERS frame in HTTP/2 decoder (CVE-2018-20615)

* Sat Dec 22 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.16-1
- Update to 1.8.16

* Thu Dec 13 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.15-1
- Update to 1.8.15
- Fix denial of service attack via infinite recursion (CVE-2018-20103, #1658881)
- Fix out-of-bound reads in dns_validate_dns_response (CVE-2018-20102, #1658882)

* Sat Dec 01 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.14-2
- Use of crpyt() is not thread safe (#1643941)

* Thu Sep 20 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.14-1
- Update to 1.8.14 (#1610066)

* Mon Aug 20 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.13-1
- Update to 1.8.13 (#1610066)

* Thu Aug 16 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.12-4
- Add BuildRequires gcc (#1604308)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.12-2
- Fix ownership of /var/lib/haproxy/ to avoid selinux DAC override errors (#1597076)

* Thu Jun 28 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.12-1
- Update to 1.8.12 (#1580036)

* Wed Jun 27 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.11-1
- Update to 1.8.11 (#1580036)

* Mon Jun 25 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.10-1
- Update to 1.8.10 (#1580036)

* Mon May 21 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.9-1
- Update to 1.8.9 (#1580036)

* Thu May 10 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.8-2
- Build with USE_GETADDRINFO option

* Thu Apr 19 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.8-1
- Update to 1.8.8 (#1560121)

* Mon Apr 09 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.7-1
- Update to 1.8.7 (#1560121)

* Fri Apr 06 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.6-1
- Update to 1.8.6 (#1560121)

* Mon Mar 26 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.5-1
- Update to 1.8.5 (#1560121)

* Mon Feb 26 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.4-2
- Define USE_SYSTEMD at build time (#1549027)

* Mon Feb 26 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.4-1
- Update to 1.8.4 (#1543668)

* Thu Feb 08 2018 Florian Weimer <fweimer@redhat.com> - 1.8.3-5
- Build halog and iprange with linker flags from redhat-rpm-config
- Tell build to include <crypt.h>

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.8.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 20 2018 Björn Esser <besser82@fedoraproject.org> - 1.8.3-3
- Rebuilt for switch to libxcrypt

* Fri Jan 05 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.3-2
- Remove haproxy-systemd-wrapper

* Fri Jan 05 2018 Ryan O'Hara <rohara@redhat.com> - 1.8.3-1
- Update to 1.8.3 (#1528829)

* Wed Dec 27 2017 Ryan O'Hara <rohara@redhat.com> - 1.8.2-1
- Update to 1.8.2

* Fri Dec 15 2017 Ryan O'Hara <rohara@redhat.com> - 1.8.1-1
- Update to 1.8.1

* Fri Dec 15 2017 Ryan O'Hara <rohara@redhat.com> - 1.8.0-1
- Update to 1.8.0

* Mon Sep 11 2017 Ryan O'Hara <rohara@redhat.com> - 1.7.9-1
- Update to 1.7.9 (#1485084)

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 10 2017 Ryan O'Hara <rohara@redhat.com> - 1.7.8-1
- Update to 1.7.8 (#1436669)

* Mon May 01 2017 Ryan O'Hara <rohara@redhat.com> - 1.7.3-2
- Use KillMode=mixed in systemd service file (#1447085)

* Sun Mar 26 2017 Ryan O'Hara <rohara@redhat.com> - 1.7.3-1
- Update to 1.7.3 (#1413276)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.7.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Jan 18 2017 Ryan O'Hara <rohara@redhat.com> - 1.7.2-1
- Update to 1.7.2 (#1413276)

* Thu Dec 29 2016 Ryan O'Hara <rohara@redhat.com> - 1.7.1-1
- Update to 1.7.1

* Mon Nov 28 2016 Ryan O'Hara <rohara@redhat.com> - 1.7.0-1
- Update to 1.7.0

* Mon Nov 21 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.10-1
- Update to 1.6.10 (#1397013)

* Wed Aug 31 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.9-1
- Update to 1.6.9 (#1370709)

* Thu Jul 14 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.7-2
- Fix main frontend in default config file (#1348674)

* Thu Jul 14 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.7-1
- Update to 1.6.7 (#1356578)

* Tue Jun 28 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.6-2
- Remove patch for CVE-2016-5360

* Tue Jun 28 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.6-1
- Update to 1.6.6 (#1350426)

* Wed Jun 15 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.5-3
- Fix reqdeny causing random crashes (CVE-2016-5360, #1346672)

* Fri Jun 03 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.5-2
- Utilize system-wide crypto-policies (#1256253)

* Mon May 23 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.5-1
- Update to 1.6.5 (#1317313)

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 20 2016 Ryan O'Hara <rohara@redhat.com> - 1.6.3-1
- Update to 1.6.3 (#1276288)

* Wed Nov 18 2015 Ryan O'Hara <rohara@redhat.com> - 1.6.2-3
- Enable Lua support

* Tue Nov 03 2015 Ryan O'Hara <rohara@redhat.com> - 1.6.2-2
- Update to 1.6.2 (#1276288)

* Fri Oct 30 2015 Ryan O'Hara <rohara@redhat.com> - 1.6.1-1
- Update to 1.6.1 (#1276288)

* Mon Jul 06 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.14-1
- Update to 1.5.14 (CVE-2015-3281, #1239181)

* Fri Jun 26 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.13-1
- Update to 1.5.13 (#1236056)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 05 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.12-2
- Remove unused patches

* Tue May 05 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.12-1
- Update to 1.5.12 (#1217922)

* Wed Mar 04 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.11-4
- Rework systemd service and sysconfig file

* Wed Feb 11 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.11-3
- Add sysconfig file

* Tue Feb 10 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.11-2
- Add tcp-ut bind option to set TCP_USER_TIMEOUT (#1190783)

* Sun Feb 01 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.11-1
- Update to 1.5.11 (#1188029)

* Mon Jan 05 2015 Ryan O'Hara <rohara@redhat.com> - 1.5.10-1
- Update to 1.5.10

* Mon Dec 01 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.9-1
- Update to 1.5.9

* Sat Nov 01 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.8-1
- Update to 1.5.8

* Thu Oct 30 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.7-1
- Update to 1.5.7

* Mon Oct 20 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Wed Oct 08 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.5-1
- Update to 1.5.5

* Tue Sep 02 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.4-1
- Update to 1.5.4

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 06 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.3-2
- Use haproxy-systemd-wrapper in service file (#1126955)

* Fri Jul 25 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.3-1
- Update to 1.5.3

* Tue Jul 15 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.2-1
- Update to 1.5.2

* Tue Jun 24 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.1-1
- Update to 1.5.1

* Thu Jun 19 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.0-2
- Build with zlib and openssl support

* Thu Jun 19 2014 Ryan O'Hara <rohara@redhat.com> - 1.5.0-1
- Update to 1.5.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Mar 27 2014 Ryan O'Hara <rohara@redhat.com> - 1.4.25-1
- Update to 1.4.25

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.24-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 17 2013 Ryan O'Hara <rohara@redhat.com> - 1.4.24-1
- Update to 1.4.24 (CVE-2013-2174, #975160)

* Tue Apr 30 2013 Ryan O'Hara <rohara@redhat.com> - 1.4.23-3
- Build with PIE flags (#955182)

* Mon Apr 22 2013 Ryan O'Hara <rohara@redhat.com> - 1.4.23-2
- Build with PIE flags (#955182)

* Tue Apr 02 2013 Ryan O'Hara <rohara@redhat.com> - 1.4.23-1
- Update to 1.4.23 (CVE-2013-1912, #947697)
- Drop supplementary groups after setuid/setgid (#894626)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.22-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 12 2012 Robin Lee <cheeselee@fedoraproject.org> - 1.4.22-1
- Update to 1.4.22 (CVE-2012-2942, #824544)
- Use linux2628 build target
- No separate x86_64 build target for halog
- halog build honors rpmbuild optflags
- Specfile cleanup

* Mon Sep 17 2012 Václav Pavlín <vpavlin@redhat.com> - 1.4.20-3
- Scriptlets replaced with new systemd macros (#850143)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Apr 03 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.20-1
- Update to 1.4.20

* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.19-4
- fix haproxy.services file

* Sun Feb 19 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.19-3
- Update to use systemd fixing bug #770305

* Fri Feb 10 2012 Petr Pisar <ppisar@redhat.com> - 1.4.19-2
- Rebuild against PCRE 8.30

* Sun Jan 29 2012 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.19-1
- Update to 1.4.19

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Sep 22 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.18-1
- Update to 1.4.18

* Tue Apr 26 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.15-1
- Update to 1.4.15

* Sun Feb 27 2011 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.11-1
- update to 1.4.11

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Dec 12 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.9-1
- update to 1.4.9

* Sun Jun 20 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.8-1
- update to 1.4.8

* Sun May 30 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.4.6-1
- update to 1.4.6

* Thu Feb 18 2010 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.23-1
- update to 1.3.23

* Sat Oct 17 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.22-1
- update to 1.3.22
- added logrotate configuration

* Mon Oct 12 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.21-1
- update to 1.3.21

* Sun Oct 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.20-1
- update to 1.3.20

* Sun Aug 02 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.19-1
- update to 1.3.19

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 17 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.18-1
- update to 1.3.18

* Sat Apr 11 2009 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.17-1
-  Update to 1.3.17

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.15.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec 30 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.15.7-1
- update to 1.3.15.7
- remove upstream patches, they are now part of source distribution

* Sat Nov 22 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.15.6-2
- apply upstream patches 

* Sat Nov 15 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.15.6-1
- update to 1.3.15.6
- use new build targets from upstream
- add in recommended build options for x86 from upstream

* Sat Jun 28 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.14.6-1
- update to 1.3.14.6
- remove gcc 4.3 patch, it has been applied upstream
- remove MIT license as that code has been removed from upstream

* Mon Apr 14 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.14.4-1
- update to 1.3.14.4

* Sun Mar 16 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.14.3-1
- update to 1.3.14.3

* Sat Mar 01 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.14.2-4
- apply the gcc 4.3 patch to the build process

* Sat Mar 01 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.14.2-3
- fix gcc 4.3 bug [#434144]
- update init script to properly reload configuration

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3.14.2-2
- Autorebuild for GCC 4.3

* Sun Jan 20 2008 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.14.2-1
- update to 1.3.14.2
- update make flags that changed with this upstream release
- added man page installation

* Sun Dec 16 2007 Jeremy Hinegardner <jeremy at hinegardner dot org> - 1.3.14-1
- update to 1.3.14

* Mon Nov 05 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.3.12.4-1
- update to 1.3.12.4

* Thu Nov 01 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.3.12.3-1
- update to 1.3.12.3

* Fri Sep 21 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.3.12.2-3
- fix init script 'reload' task

* Thu Sep 20 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.3.12.2-2
- update License field

* Thu Sep 20 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.3.12.2-1
- update to 1.3.12.2
- remove the upstream patch

* Tue Sep 18 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.3.12.1-1
- switch to 1.3.12.1 branch
- add patch from upstream with O'Reilly licensing updates.
- convert ISO-8859-1 doc files to UTF-8

* Sat Mar 24 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.2.17-2
- addition of haproxy user
- add license information

* Fri Mar 23 2007 Jeremy Hinegardner <jeremy@hinegardner.org> - 1.2.17-1
- initial packaging
