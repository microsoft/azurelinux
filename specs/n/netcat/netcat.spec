# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global commit d0cc618721a8b450997f44626c9d937245dc1b9a

%if 0%{?fedora} || 0%{?rhel} > 8
%global link_bin nc
%global link_man nc-man
%else
%global link_bin nmap
%global link_man ncman
%endif

Summary:         OpenBSD netcat to read and write data across connections using TCP or UDP
Name:            netcat
# Version from CVS revision of OpenBSD netcat.c
Version:         1.237
Release: 4%{?dist}
# BSD-3-Clause: nc.1 and netcat.c
# BSD-2-Clause: atomicio.{c,h} and socks.c
License:         BSD-3-Clause AND BSD-2-Clause
URL:             https://man.openbsd.org/nc.1
Source0:         https://raw.githubusercontent.com/openbsd/src/%{commit}/usr.bin/nc/netcat.c
Source1:         https://raw.githubusercontent.com/openbsd/src/%{commit}/usr.bin/nc/nc.1
Source2:         https://raw.githubusercontent.com/openbsd/src/%{commit}/usr.bin/nc/atomicio.c
Source3:         https://raw.githubusercontent.com/openbsd/src/%{commit}/usr.bin/nc/atomicio.h
Source4:         https://raw.githubusercontent.com/openbsd/src/%{commit}/usr.bin/nc/socks.c
Source5:         https://raw.githubusercontent.com/openbsd/src/%{commit}/usr.bin/nc/Makefile
# Port peculiarities from OpenBSD to Linux
Patch0:          https://salsa.debian.org/debian/netcat-openbsd/-/raw/3dd21269220dd746eaf4e64a17b7257eba47c2c2/debian/patches/port-to-linux-with-libbsd.patch
BuildRequires:   make
BuildRequires:   gcc
BuildRequires:   libbsd-devel
BuildRequires:   libretls-devel
Requires(post):  %{?el8:/usr/sbin/}alternatives
Requires(preun): %{?el8:/usr/sbin/}alternatives

%description
The OpenBSD nc (or netcat) utility can be used for just about anything involving
TCP, UDP, or UNIX-domain sockets. It can open TCP connections, send UDP packets,
listen on arbitrary TCP and UDP ports, do port scanning, and deal with both IPv4
and IPv6. Unlike telnet(1), nc scripts nicely, and separates error messages onto
standard error instead of sending them to standard output, as telnet(1) might do
with some.

%prep
%setup -q -T -c
cp -pf %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} .
%patch -P0 -p1 -b .port-to-linux-with-libbsd
sed -e '1i #define unveil(path, permissions) 0' \
    -e '1i #define pledge(request, paths) 0' \
    -e '1i #ifndef IPTOS_DSCP_VA\n#define IPTOS_DSCP_VA 0xb0\n#endif' \
    -i netcat.c
sed -e 's/^\(LIBS ?= .*\)/\1 -ltls/' -i Makefile

# https://fedoraproject.org/wiki/Changes/dropingOfCertPemFile
%if 0%{?fedora} >= 43 || 0%{?rhel} >= 11
sed -e 's/\(^[[:space:]]*Rflag =\) tls_default_ca_cert_file();/\1 NULL;/' \
    -i netcat.c
%endif

%build
%make_build CFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS"

%install
install -D -p -m 0755 nc $RPM_BUILD_ROOT%{_bindir}/%{name}
install -D -p -m 0644 nc.1 $RPM_BUILD_ROOT%{_mandir}/man1/%{name}.1

touch $RPM_BUILD_ROOT%{_bindir}/nc
touch $RPM_BUILD_ROOT%{_mandir}/man1/nc.1.gz

%post
alternatives --install %{_bindir}/nc %{link_bin} %{_bindir}/%{name} 10 \
  --slave %{_mandir}/man1/nc.1.gz %{link_man} %{_mandir}/man1/%{name}.1.gz

%preun
if [ $1 -eq 0 ]; then
  alternatives --remove %{link_bin} %{_bindir}/%{name}
fi

%files
%ghost %{_bindir}/nc
%ghost %{_mandir}/man1/nc.1.gz
%{_bindir}/netcat
%{_mandir}/man1/netcat.1*

%changelog
* Wed Jan 21 2026 Robert Scheck <robert@fedoraproject.org> 1.237-3
- Do not use removed /etc/pki/tls/cert.pem bundle file for
  Fedora 43 >= and RHEL >= 11 (#2430274)

* Fri Jan 16 2026 Fedora Release Engineering <releng@fedoraproject.org> - 1.237-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_44_Mass_Rebuild

* Sat Jan 03 2026 Robert Scheck <robert@fedoraproject.org> 1.237-1
- Upgrade to 1.237 (#2406149)

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.229-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.229-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Jan 05 2025 Robert Scheck <robert@fedoraproject.org> 1.229-1
- Upgrade to 1.229

* Sun Oct 20 2024 Robert Scheck <robert@fedoraproject.org> 1.228-1
- Upgrade to 1.228

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.226-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.226-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.226-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Robert Scheck <robert@fedoraproject.org> 1.226-1
- Upgrade to 1.226 (#2244540)

* Sun Nov 05 2023 Robert Scheck <robert@fedoraproject.org> 1.225-3
- Rebuilt for libretls 3.8.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.225-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 11 2023 Robert Scheck <robert@fedoraproject.org> 1.225-1
- Upgrade to 1.225 (#2214050)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.219-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Dec 24 2022 Robert Scheck <robert@fedoraproject.org> 1.219-2
- Rebuilt for libretls 3.7.0

* Sun Oct 23 2022 Robert Scheck <robert@fedoraproject.org> 1.219-1
- Upgrade to 1.219 (#2136750)

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.218-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat May 14 2022 Robert Scheck <robert@fedoraproject.org> 1.218-5
- Rebuilt for libretls 3.5.2

* Sun Feb 27 2022 Robert Scheck <robert@fedoraproject.org> 1.218-4
- Rebuilt for libretls 3.5.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.218-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Sat Oct 16 2021 Robert Scheck <robert@fedoraproject.org> 1.218-2
- Rebuilt for libretls 3.4.1

* Mon Aug 30 2021 Robert Scheck <robert@fedoraproject.org> 1.218-1
- Upgrade to 1.218 (#1993735)

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.217-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar 17 2021 Robert Scheck <robert@fedoraproject.org> 1.217-3
- Changes to match the Fedora Packaging Guidelines (#1939769 #c1)

* Wed Mar 17 2021 Robert Scheck <robert@fedoraproject.org> 1.217-2
- Changes to match the Fedora Packaging Guidelines (#1939769)

* Sun Mar 07 2021 Robert Scheck <robert@fedoraproject.org> 1.217-1
- Upgrade to 1.217
- Initial spec file for Fedora and Red Hat Enterprise Linux
