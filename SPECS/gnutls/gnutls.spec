Summary:        The GnuTLS Transport Layer Security Library
Name:           gnutls
Version:        3.7.7
Release:        3%{?dist}
License:        GPLv3+ AND LGPLv2.1+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://www.gnutls.org
Source0:        https://www.gnupg.org/ftp/gcrypt/gnutls/v3.7/%{name}-%{version}.tar.xz
Patch0:         CVE-2023-0361.patch
BuildRequires:  autogen-libopts-devel
BuildRequires:  gc-devel
BuildRequires:  guile-devel
BuildRequires:  libtasn1-devel
BuildRequires:  nettle-devel >= 3.7.2
BuildRequires:  openssl-devel
BuildRequires:  p11-kit-devel
%if %{with_check}
BuildRequires:  net-tools
BuildRequires:  which
%endif
Requires:       autogen-libopts
Requires:       gc
Requires:       gmp
Requires:       guile
Requires:       libtasn1
Requires:       nettle >= 3.7.2
Requires:       openssl
Provides:       %{name}-utils = %{version}-%{release}
Provides:       %{name}-c++ = %{version}-%{release}

%description
GnuTLS is a secure communications library implementing the SSL, TLS and DTLS protocols and technologies around them. It provides a simple C language application programming interface (API) to access the secure communications protocols as well as APIs to parse and write X.509, PKCS #12, OpenPGP and other required structures. It is aimed to be portable and efficient with focus on security and interoperability.

%package        devel
Summary:        Development libraries and header files for gnutls
Requires:       %{name} = %{version}-%{release}
Requires:       libtasn1-devel
Requires:       nettle-devel

%description devel
The package contains libraries and header files for
developing applications that use gnutls.

%prep
%autosetup -p1

%build
%configure \
    --disable-openssl-compatibility \
    --with-included-unistring \
    --with-system-priority-file=%{_sysconfdir}/gnutls/default-priorities \
    --with-default-trust-store-file=%{_sysconfdir}/ssl/certs/ca-bundle.crt \
    --with-default-trust-store-dir=%{_sysconfdir}/ssl/certs
%make_build

%install
%make_install
rm %{buildroot}%{_infodir}/*
find %{buildroot} -type f -name "*.la" -delete -print

mkdir -p %{buildroot}%{_sysconfdir}/%{name}
chmod 755 %{buildroot}%{_sysconfdir}/%{name}
cat > %{buildroot}%{_sysconfdir}/%{name}/default-priorities << "EOF"
SYSTEM=NONE:!VERS-SSL3.0:!VERS-TLS1.0:+VERS-TLS1.1:+VERS-TLS1.2:+AES-128-CBC:+RSA:+SHA1:+COMP-NULL
EOF

%check
# Disable test-ciphers-openssl.sh test, which relies on ciphers our openssl.spec has disabled.
#     Observed error: "cipher_test:50: EVP_get_cipherbyname failed for chacha20-poly1305"
sed -i 's/TESTS += test-ciphers-openssl.sh//'  tests/slow/Makefile.am
%make_build check

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license LICENSE
%{_libdir}/*.so.*
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/locale/*
%{_docdir}/gnutls/*.png
%{_libdir}/guile/2.0/extensions/*.so*
%{_libdir}/guile/2.0/site-ccache/gnutls*
%{_datadir}/guile/site/2.0/gnutls*
%config(noreplace) %{_sysconfdir}/gnutls/default-priorities

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*

%changelog
* Wed Sep 20 2023 Jon Slobodzian <joslobo@microsoft.com> - 3.7.7-3
- Recompile with stack-protection fixed gcc version (CVE-2023-4039)

* Mon Mar 06 2023 Nan Liu <liunan@microsoft.com> - 3.7.7-2
- Add patch to fix CVE-2023-0361

* Tue Aug 09 2022 Andrew Phelps <anphel@microsoft.com> - 3.7.7-1
- Update to version 3.7.7 to resolve CVE CVE-2022-2509

* Tue Feb 15 2022 Cameron Baird <cameronbaird@microsoft.com> - 3.7.3-2
- Build with p11-kit

* Mon Jan 24 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 3.7.3-1
- Upgrade to 3.7.3
- License verified

* Fri Jul 23 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.6.14-6
- Provide compatibility provides for c++ subpackage from base package
- Lint spec

* Fri Apr 02 2021 Olivia Crain <oliviacrain@microsoft.com> - 3.6.14-5
- Merge the following releases from 1.0 to dev branch
- anphel@microsoft.com, 3.6.14-4: Fix check tests.
- mmalisz@microsoft.com, 3.6.14-5: Apply patch for CVE-2021-20231 and CVE-2021-20232 from upstream.

* Thu Feb 04 2021 Joe Schmitt <joschmit@microsoft.com> - 3.6.14-4
- Provide gnutls-utils.

* Wed Oct 21 2020 Henry Beberman <henry.beberman@microsoft.com> - 3.6.14-3
- Apply patch for CVE-2020-24659 from upstream.
- Switch setup to autosetup.

* Wed Oct 07 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.14-2
- Updating certificate bundle path to include full set of trust information.

* Fri Aug 21 2020 Andrew Phelps <anphel@microsoft.com> - 3.6.14-1
- Update to version 3.6.14 for CVE-2020-13777

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 3.6.8-3
- Added %%license line automatically

* Wed May 06 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 3.6.8-2
- Removing *Requires for "ca-certificates".
- Adding a certs directory through "--with-default-trust-store-dir" at compile time.

* Mon Mar 16 2020 Henry Beberman <henry.beberman@microsoft.com> - 3.6.8-1
- Update to 3.6.8. Source0 URL updated. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 3.6.3-4
- Initial CBL-Mariner import from Photon (license: Apache2).

* Mon Apr 15 2019 Keerthana K <keerthanak@vmware.com> - 3.6.3-3
- Fix CVE-2019-3829, CVE-2019-3836

* Wed Oct 03 2018 Tapas Kundu <tkundu@vmware.com> - 3.6.3-2
- Including default-priority in the RPM packaging.

* Thu Sep 06 2018 Anish Swaminathan <anishs@vmware.com> - 3.6.3-1
- Update version to 3.6.3

* Fri Feb 09 2018 Xiaolin Li <xiaolinl@vmware.com> - 3.5.15-2
- Add default_priority.patch.

* Tue Oct 10 2017 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.5.15-1
- Update to 3.5.15. Fixes CVE-2017-7507

* Thu Apr 13 2017 Danut Moraru <dmoraru@vmware.com> - 3.5.10-1
- Update to version 3.5.10

* Sun Dec 18 2016 Alexey Makhalov <amakhalov@vmware.com> - 3.4.11-4
- configure to use default trust store file

* Wed Dec 07 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.4.11-3
- Moved man3 to devel subpackage.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 3.4.11-2
- GA - Bump release of all rpms

* Wed Apr 27 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.4.11-1
- Updated to version 3.4.11

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.4.9-1
- Updated to version 3.4.9

* Thu Jan 14 2016 Xiaolin Li <xiaolinl@vmware.com> - 3.4.8-1
- Updated to version 3.4.8

* Wed Dec 09 2015 Anish Swaminathan <anishs@vmware.com> - 3.4.2-3
- Edit post script.

* Fri Oct 9 2015 Xiaolin Li <xiaolinl@vmware.com> - 3.4.2-2
- Removing la files from packages.

* Thu Jun 18 2015 Divya Thaluru <dthaluru@vmware.com> - 3.4.2-1
- Initial build. First version
