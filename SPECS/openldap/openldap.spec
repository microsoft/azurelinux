%global _default_patch_fuzz 2
Summary:        OpenLDAP (Lightweight Directory Access Protocol)
Name:           openldap
Version:        2.4.57
Release:        8%{?dist}
License:        OpenLDAP
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Security
URL:            https://www.openldap.org/
# Using Canadian mirror. Original source link didn't work: ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{name}-%{version}.tgz
Source0:        https://gpl.savoirfairelinux.net/pub/mirrors/openldap/openldap-release/%{name}-%{version}.tgz
Patch0:         openldap-2.4.40-gssapi-1.patch
Patch1:         openldap-2.4.44-consolidated-2.patch
Patch2:         CVE-2015-3276.patch
Patch3:         CVE-2021-27212.patch
Patch4:         CVE-2022-29155.patch
BuildRequires:  cyrus-sasl-bootstrap-devel >= 2.1
BuildRequires:  e2fsprogs-devel
BuildRequires:  groff
BuildRequires:  openssl-devel >= 1.0.1
Requires:       openssl >= 1.0.1
Provides:       %{name}-clients = %{version}-%{release}
Provides:       %{name}-compat = %{version}-%{release}
Provides:       %{name}-devel = %{version}-%{release}

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools. LDAP is a set of
protocols for accessing directory services (usually phone book style
information, but other information is possible) over the Internet,
similar to the way DNS (Domain Name System) information is propagated
over the Internet. The openldap package contains configuration files,
libraries, and documentation for OpenLDAP.

%prep
%autosetup -p1

%build
autoconf
sed -i '/6.0.20/ a\\t__db_version_compat' configure
export CPPFLAGS="${CPPFLAGS} -D_REENTRANT -DLDAP_CONNECTIONLESS -D_GNU_SOURCE -D_AVL_H"
%configure \
        --disable-static    \
        --enable-dynamic    \
        --disable-debug     \
        --disable-slapd     \
        --with-tls=openssl
%make_build depend
%make_build

%install
%make_install
find %{buildroot} -type f -name "*.la" -delete -print
%{_fixperms} %{buildroot}/*

%check
%make_build test

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/*
%{_libdir}/*.so*
%{_includedir}/*
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/man8/*
%{_sysconfdir}/openldap/*

%changelog
* Fri Feb 10 2023 Sriram Nambakam <snambakam@microsoft.com> - 2.4.57-8
- Let openldap depend on cyrus-sasl.

* Wed Jun 01 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 2.4.57-7
- Fix CVE-2022-29155

* Wed Jan 05 2022 Henry Beberman <henry.beberman@microsoft.com> - 2.4.57-6
- Set --enable-dynamic to disable rpath in ldap tools
- Ensure that default CPPFLAGS are preserved

* Tue Sep 14 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.4.57-5
- Removing dependency on "cyrus-sasl".

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.4.57-4
- Add clients, compat subpackage provides from base package
- Minor macro linting

* Fri Mar 26 2021 Olivia Crain <oliviacrain@microsoft.com> - 2.4.57-3
- Merge the following releases from dev to 1.0 spec
- v-ruyche@microsoft.com, 2.4.50-2: Explicit provide -devel subpackage

* Thu Feb 25 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 2.4.57-2
- Resolve CVE-2021-27212

* Fri Jan 29 2021 Henry Li <lihl@microsoft.com> - 2.4.57-1
- Upgrade to version 2.4.57
- Resolve CVE-2020-36221, CVE-2020-36222, CVE-2020-36223, CVE-2020-36224, CVE-2020-36225
- Update openldap-2.4.44-consolidated-2.patch
- Remove patch CVE-2020-25962 because the change is included in the newer version

* Wed Dec 09 2020 Joe Schmitt <joschmit@microsoft.com> - 2.4.50-3
- Patch CVE-2020-25692.

* Mon Oct 26 2020 Henry Li <lihl@microsoft.com> 2.4.50-2
- Used autosetup.
- Added patch to resolve CVE-2015-3276.

* Wed Jun 03 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.4.50-1
- Upgrade to version 2.4.50, which resolves CVE-2020-12243.

* Tue May 12 2020 Nicolas Ontiveros <niontive@microsoft.com> 2.4.48-1
- Upgrade to version 2.4.48, which fixes CVE-2019-13057 and CVE-2019-13565.

* Sat May 09 00:20:53 PST 2020 Nick Samson <nisamson@microsoft.com> - 2.4.46-6
- Added %%license line automatically

* Thu Apr 23 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 2.4.46-5
- License verified.
- Fixed 'Source0' tag.

* Fri Mar 03 2020 Jon Slobodzian <joslobo@microsoft.com> 2.4.46-4
- Replaced incorrect URL link. Verified license. Removed incorrect version from Summary.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 2.4.46-3
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Nov 5 2018 Sriram Nambakam <snambakam@vmware.com> 2.4.46-2
- export CPPFLAGS before invoking configure

* Mon Sep 10 2018 Him Kalyan Bordoloi <bordoloih@vmware.com> 2.4.46-1
- Upgrade to 2.4.46

* Fri Oct 13 2017 Alexey Makhalov <amakhalov@vmware.com> 2.4.44-3
- Use standard configure macros

* Tue Jul 11 2017 Divya Thaluru <dthaluru@vmware.com> 2.4.44-2
- Applied patch for CVE-2017-9287

* Sat Apr 15 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.44-1
- Update to 2.4.44

* Wed Oct 05 2016 ChangLee <changlee@vmware.com> 2.4.43-3
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 2.4.43-2
- GA - Bump release of all rpms

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> 2.4.43-1
- Updated to version 2.4.43

* Fri Aug 14 2015 Vinay Kulkarni <kulkarniv@vmware.com> 2.4.40-2
- Patches for CVE-2015-1545 and CVE-2015-1546.

* Wed Oct 08 2014 Divya Thaluru <dthaluru@vmware.com> 2.4.40-1
- Initial build. First version
