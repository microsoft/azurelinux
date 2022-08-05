Vendor:         Microsoft Corporation
Distribution:   Mariner
%global _hardened_build 1

Summary: A RFC 1413 ident protocol daemon
Name: authd
Version: 1.4.4
Release: 6%{?dist}
License: GPLv2+
URL: https://github.com/InfrastructureServices/authd
Obsoletes: pidentd < 3.2
Provides: pidentd = 3.2
Requires(post): openssl
Source0: https://github.com/InfrastructureServices/authd/releases/download/v1.4.4/authd-1.4.4.tar.gz
Source1: auth.socket
Source2: auth@.service
BuildRequires: gcc
BuildRequires: openssl-devel 
BuildRequires: gettext 
BuildRequires: help2man 
BuildRequires: systemd-units
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
authd is a small and fast RFC 1413 ident protocol daemon
with both xinetd server and interactive modes that
supports IPv6 and IPv4 as well as the more popular features
of pidentd.

%prep
%autosetup

%build
make prefix=%{_prefix} CFLAGS="%{optflags}" \
        LDFLAGS="-lcrypto %{build_ldflags}"


%install
%make_install datadir=%{buildroot}/%{_datadir} \
	sbindir=%{buildroot}/%{_sbindir}

install -d %{buildroot}%{_unitdir}/
install -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/
install -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/

install -d %{buildroot}%{_sysconfdir}/
touch %{buildroot}%{_sysconfdir}/ident.key

install -d %{buildroot}/%{_mandir}/man1/
help2man -N -v -V %{buildroot}/%{_sbindir}/in.authd -o \
         %{buildroot}/%{_mandir}/man1/in.authd.1

%find_lang %{name}

%post
/usr/sbin/adduser -s /usr/sbin/nologin -u 98 -r -d '/' ident 2>/dev/null || true
/usr/bin/openssl rand -base64 -out %{_sysconfdir}/ident.key 32
echo CHANGE THE LINE ABOVE TO A PASSPHRASE >> %{_sysconfdir}/ident.key
/bin/chown ident:ident %{_sysconfdir}/ident.key
chmod o-rw %{_sysconfdir}/ident.key
%systemd_post auth.socket

%postun
%systemd_postun_with_restart auth.socket

%preun
%systemd_preun auth.socket

%files -f authd.lang
%license COPYING
%verify(not md5 size mtime user group) %config(noreplace) %attr(640,root,root) %{_sysconfdir}/ident.key
%doc COPYING README.html rfc1413.txt
%{_sbindir}/in.authd
%{_mandir}/*/*
%{_unitdir}/*

%changelog
* Thu Jul 28 2022 Henry Li <lihl@microsoft.com> - 1.4.4-6
- Fix spec formatting
- License Verified

* Fri Apr 30 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.4.4-5
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Making binaries paths compatible with CBL-Mariner's paths.

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Feb 18 2019 Pavel Zhukov <pzhukov@redhat.com> - 1.4.4-2
- hardened build with fedora specific flags

* Tue Feb 12 2019 Pavel Zhukov <pzhukov@redhat.com> - 1.4.4-1
- New release (v1.4.4)
- New upstream URL

