Vendor:         Microsoft Corporation
Distribution:   Mariner
# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}

Name:		mod_http2
Version:	1.15.14
Release:	2%{?dist}
Summary:	module implementing HTTP/2 for Apache 2
License:	ASL 2.0
URL:		https://icing.github.io/mod_h2/
Source0:	https://github.com/icing/mod_h2/releases/download/v%{version}/mod_http2-%{version}.tar.gz
Patch1:         mod_http2-1.14.1-buildfix.patch
BuildRequires:  gcc
BuildRequires:	pkgconfig, httpd-devel >= 2.4.20, libnghttp2-devel >= 1.7.0, openssl-devel >= 1.0.2
Requires:	httpd-mmn
Conflicts:      httpd < 2.4.25-8

%description
The mod_h2 Apache httpd module implements the HTTP2 protocol (h2+h2c) on
top of libnghttp2 for httpd 2.4 servers.

%prep
%setup -q
%patch1 -p1 -b .buildfix

%build
%configure
make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/etc/httpd/share/doc/

# create configuration
mkdir -p %{buildroot}%{_httpd_modconfdir}
echo "LoadModule http2_module modules/mod_http2.so" > %{buildroot}%{_httpd_modconfdir}/10-h2.conf
echo "LoadModule proxy_http2_module modules/mod_proxy_http2.so" > %{buildroot}%{_httpd_modconfdir}/10-proxy_h2.conf

%files
%doc README.md ChangeLog AUTHORS
%license LICENSE
%config(noreplace) %{_httpd_modconfdir}/10-h2.conf
%config(noreplace) %{_httpd_modconfdir}/10-proxy_h2.conf
%{_httpd_moddir}/mod_http2.so
%{_httpd_moddir}/mod_proxy_http2.so

%changelog
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.15.14-2
- Initial CBL-Mariner import from Fedora 33 (license: MIT).

* Mon Aug 17 2020 Joe Orton <jorton@redhat.com> - 1.15.14-1
- update to 1.15.14

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar  6 2020 Joe Orton <jorton@redhat.com> - 1.15.7-1
- update to 1.15.7

* Fri Feb  7 2020 Joe Orton <jorton@redhat.com> - 1.15.5-1
- update to 1.15.5

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 19 2019 Lubos Uhliarik <luhliari@redhat.com> - 1.15.3-2
- Rebuilt with newer nghttp2

* Thu Aug  8 2019 Joe Orton <jorton@redhat.com> - 1.15.3-1
- update to 1.15.3

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Wed May 29 2019 Joe Orton <jorton@redhat.com> - 1.15.1-1
- update to 1.15.1

* Wed May 22 2019 Joe Orton <jorton@redhat.com> - 1.15.0-1
- update to 1.15.0

* Thu Mar 14 2019 Joe Orton <jorton@redhat.com> - 1.14.1-1
- update to 1.14.1

* Tue Mar  5 2019 Joe Orton <jorton@redhat.com> - 1.14.0-1
- update to 1.14.0

* Tue Feb 26 2019 Joe Orton <jorton@redhat.com> - 1.13.0-1
- update to 1.13.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jan 18 2019 Joe Orton <jorton@redhat.com> - 1.12.1-1
- update to 1.12.1

* Tue Oct 09 2018 Lubos Uhliarik <luhliari@redhat.com> - 1.11.2-1
- new version 1.11.2

* Fri Oct 05 2018 Luboš Uhliarik <luhliari@redhat.com> - 1.11.1-1
- new version 1.11.1 (CVE-2018-11763)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed May  2 2018 Joe Orton <jorton@redhat.com> - 1.10.20-1
- update to 1.10.20

* Wed Apr 18 2018 Joe Orton <jorton@redhat.com> - 1.10.18-1
- update to 1.10.18

* Thu Mar 29 2018 Joe Orton <jorton@redhat.com> - 1.10.16-1
- update to 1.10.16 (CVE-2018-1302)

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Nov  7 2017 Joe Orton <jorton@redhat.com> - 1.10.13-1
- update to 1.10.13

* Fri Oct 20 2017 Joe Orton <jorton@redhat.com> - 1.10.12-1
- update to 1.10.12

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Mon Jul 31 2017 Joe Orton <jorton@redhat.com> - 1.10.10-1
- update to 1.10.10

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul  6 2017 Joe Orton <jorton@redhat.com> - 1.10.7-1
- update to 1.10.7

* Mon Jun 12 2017 Joe Orton <jorton@redhat.com> - 1.10.6-1
- update to 1.10.6

* Tue May 16 2017 Joe Orton <jorton@redhat.com> - 1.10.5-1
- update to 1.10.5

* Mon Apr 10 2017 Luboš Uhliarik <luhliari@redhat.com> - 1.10.1-1
- Initial import (#1440780).
