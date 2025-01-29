Vendor:         Microsoft Corporation
Distribution:   Azure Linux
# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}

Name:           mod_md
Version:        2.4.26
Release:        3%{?dist}
Summary:        Certificate provisioning using ACME for the Apache HTTP Server
License:        Apache-2.0
URL:            https://icing.github.io/mod_md/
Source0:        https://github.com/icing/mod_md/releases/download/v%{version}/mod_md-%{version}.tar.gz

BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  pkgconfig
BuildRequires:  httpd-devel >= 2.4.41
BuildRequires:  openssl-devel >= 1.1.0
BuildRequires:  jansson-devel
BuildRequires:  libcurl-devel
BuildRequires:  xmlto
Requires:       libxcrypt
Requires:       mod_ssl >= 2.4.41
Provides:       httpd-mmn = %{_httpd_mmn}
Conflicts:      httpd < 2.4.39-7

%description
This module manages common properties of domains for one or more
virtual hosts. Specifically it can use the ACME protocol to automate
certificate provisioning.  Certificates will be configured for managed
domains and their virtual hosts automatically, including at renewal.

%prep
%autosetup -p1

%build
%configure --with-apxs=%{_httpd_apxs}
# remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build V=1

%check
%make_build check

%install
%make_install
rm -rf %{buildroot}/etc/httpd/share/doc/

# remove links and rename SO files
rm -f %{buildroot}%{_httpd_moddir}/mod_md.so
mv %{buildroot}%{_httpd_moddir}/mod_md.so.0.0.0 %{buildroot}%{_httpd_moddir}/mod_md.so

# create configuration and state directory
mkdir -p %{buildroot}%{_httpd_modconfdir} %{buildroot}%{_httpd_statedir}/md
echo "LoadModule md_module modules/mod_md.so" > %{buildroot}%{_httpd_modconfdir}/01-md.conf

%files
%doc README.md ChangeLog AUTHORS
%license LICENSE
%config(noreplace) %{_httpd_modconfdir}/01-md.conf
%{_httpd_moddir}/mod_md.so
%{_bindir}/a2md
%{_mandir}/man1/*

%changelog
* Mon Dec 06 2025 Aninda Pradhan <mwaniv-anipradhan@microsft.com> - 2.4.26-3
- Initial Azure Linux import from Fedora 41 (license: MIT)
- License verified
- Removed epoch
- Removed "mod_md-2.0.8-state_dir.patch" to make the build skip sections not supported by Azure Linux.

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Joe Orton <jorton@redhat.com> - 1:2.4.26-1
- update to 2.4.26

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 28 2023 Joe Orton <jorton@redhat.com> - 1:2.4.25-1
- update to 2.4.25

* Mon Sep 11 2023 Luboš Uhliarik <luhliari@redhat.com> - 1:2.4.24-1
- new version 2.4.24

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 01 2023 Luboš Uhliarik <luhliari@redhat.com> - 1:2.4.21-1
- new version 2.4.21
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Joe Orton <jorton@redhat.com> - 1:2.4.19-2
- package the "md" directory (#2154348)

* Thu Oct  6 2022 Joe Orton <jorton@redhat.com> - 1:2.4.19-1
- update to 2.4.19

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.10-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Dec  3 2021 Joe Orton <jorton@redhat.com> - 1:2.4.10-1
- update to 2.4.10

* Fri Sep 17 2021 Joe Orton <jorton@redhat.com> - 1:2.4.7-1
- update to 2.4.7

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 1:2.4.0-3
- Rebuilt with OpenSSL 3.0.0

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar  9 2021 Joe Orton <jorton@redhat.com> - 1:2.4.0-1
- update to 2.4.0

* Tue Feb  2 2021 Joe Orton <jorton@redhat.com> - 1:2.3.7-1
- update to 2.3.7 (beta)
- use autosetup macro

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 22 2021 Joe Orton <jorton@redhat.com> - 1:2.2.8-4
- update to 2.2.8

* Fri Aug 28 2020 Joe Orton <jorton@redhat.com> - 1:2.2.7-4
- use _httpd_apxs macro

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.2.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 23 2020 Alexander Bokovoy <abokovoy@redhat.com> - 1:2.2.7-2
- mod_md does not work with ACME server that does not provide revokeCert or
  keyChange resource (#1832841)

* Tue Feb 11 2020 Joe Orton <jorton@redhat.com> - 1:2.2.7-1
- update to 2.2.7

* Fri Feb  7 2020 Joe Orton <jorton@redhat.com> - 1:2.2.6-1
- update to 2.2.6 (#1799660)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Aug 30 2019 Joe Orton <jorton@redhat.com> - 1:2.0.8-4
- require mod_ssl, update package description

* Fri Aug 30 2019 Joe Orton <jorton@redhat.com> - 1:2.0.8-3
- rebuild against 2.4.41

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jul 12 2019 Joe Orton <jorton@redhat.com> - 1:2.0.8-1
- update to 2.0.8

* Tue Jun 11 2019 Lubos Uhliarik <luhliari@redhat.com> - 2.0.3-1
- Initial import (#1719248).
