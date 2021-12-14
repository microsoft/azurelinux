Vendor:         Microsoft Corporation
Distribution:   Mariner
# Module Magic Number
%{!?_httpd_mmn: %global _httpd_mmn %(cat %{_includedir}/httpd/.mmn 2>/dev/null || echo 0-0)}

Name:           mod_md
Version:        2.2.7
Release:        4%{?dist}
Summary:        Certificate provisioning using ACME for the Apache HTTP Server
License:        ASL 2.0
URL:            https://icing.github.io/mod_md/
Source0:        https://github.com/icing/mod_md/releases/download/v%{version}/mod_md-%{version}.tar.gz
Patch2:         mod_md-2.2.6-warnfix.patch
Patch3:         mod_md-2.0.8-tolerate-missing-res.patch
BuildRequires:  gcc
BuildRequires:  pkgconfig, httpd-devel >= 2.4.41, openssl-devel >= 1.1.0, jansson-devel, libcurl-devel, xmlto
Requires:       httpd-mmn, mod_ssl
Conflicts:      httpd < 2.4.39-7

%description
This module manages common properties of domains for one or more
virtual hosts. Specifically it can use the ACME protocol to automate
certificate provisioning.  Certificates will be configured for managed
domains and their virtual hosts automatically, including at renewal.

%prep
%setup -q
%patch2 -p1 -b .warnfix
%patch3 -p1 -b .tol_missing_res

%build
%configure
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

# create configuration
mkdir -p %{buildroot}%{_httpd_modconfdir}
echo "LoadModule md_module modules/mod_md.so" > %{buildroot}%{_httpd_modconfdir}/01-md.conf

%files
%doc README.md ChangeLog AUTHORS
%license LICENSE
%config(noreplace) %{_httpd_modconfdir}/01-md.conf
%{_httpd_moddir}/mod_md.so
%{_bindir}/a2md
%{_mandir}/man1/*

%changelog
* Mon Nov 01 2021 Muhammad Falak <mwani@microsft.com> - 2.2.7-4
- Remove epoch

* Mon Sep 20 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1:2.2.7-3
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Removing "mod_md-2.0.8-state_dir.patch" to make the build skip sections not supported in CBL-Mariner.

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
