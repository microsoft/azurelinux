# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global mingw_build_ucrt64 1
%{?mingw_package_header}

# For the curious:
# 0.9.8jk + EAP-FAST soversion = 8
# 1.0.0 soversion = 10
# 1.1.0 soversion = 1.1 (same as upstream although presence of some symbols
#                        depends on build configuration options)
%global soversion 3

# Enable the tests.
# These only work some of the time, but fail randomly at other times
# (although I have had them complete a few times, so I don't think
# there is any actual problem with the binaries).
%global run_tests 0

Name:           mingw-openssl
Version:        3.2.4
Release: 4%{?dist}
Summary:        MinGW port of the OpenSSL toolkit

License:        OpenSSL
URL:            http://www.openssl.org/

Source:  openssl-%{version}.tar.gz
Source2: Makefile.certificate
Source3: genpatches
Source6: make-dummy-cert
Source7: renew-dummy-cert
Source12: ec_curve.c
Source13: ectest.c

# Patches exported from source git
# Aarch64 and ppc64le use lib64
Patch1:   0001-Aarch64-and-ppc64le-use-lib64.patch
# Use more general default values in openssl.cnf
Patch2:   0002-Use-more-general-default-values-in-openssl.cnf.patch
# Do not install html docs
Patch3:   0003-Do-not-install-html-docs.patch
# Override default paths for the CA directory tree
Patch4:   0004-Override-default-paths-for-the-CA-directory-tree.patch
# apps/ca: fix md option help text
Patch5:   0005-apps-ca-fix-md-option-help-text.patch
# Disable signature verification with totally unsafe hash algorithms
Patch6:   0006-Disable-signature-verification-with-totally-unsafe-h.patch
# Add support for PROFILE=SYSTEM system default cipherlist
Patch7:   0007-Add-support-for-PROFILE-SYSTEM-system-default-cipher.patch
# Add FIPS_mode() compatibility macro
Patch8:   0008-Add-FIPS_mode-compatibility-macro.patch
# Add check to see if fips flag is enabled in kernel
Patch9:   0009-Add-Kernel-FIPS-mode-flag-support.patch
# Instead of replacing ectest.c and ec_curve.c, add the changes as a patch so
# that new modifications made to these files by upstream are not lost.
Patch10:  0010-Add-changes-to-ectest-and-eccurve.patch
# remove unsupported EC curves
Patch11:  0011-Remove-EC-curves.patch
# Disable explicit EC curves
# https://bugzilla.redhat.com/show_bug.cgi?id=2066412
Patch12:  0012-Disable-explicit-ec.patch
# Skipped tests from former 0011-Remove-EC-curves.patch
Patch13:  0013-skipped-tests-EC-curves.patch
# Instructions to load legacy provider in openssl.cnf
Patch24:  0024-load-legacy-prov.patch
# We load FIPS provider and set FIPS properties implicitly
Patch32:  0032-Force-fips.patch
# Embed HMAC into the fips.so
# RWMJ: Remove this patch for mingw as it causes
# > link.h: No such file or directory
# Patch33:  0033-FIPS-embed-hmac.patch
# Comment out fipsinstall command-line utility
Patch34:  0034.fipsinstall_disable.patch
# Skip unavailable algorithms running `openssl speed`
Patch35:  0035-speed-skip-unavailable-dgst.patch
# Extra public/private key checks required by FIPS-140-3
Patch44:  0044-FIPS-140-3-keychecks.patch
# Minimize fips services
# Remove this patch on mingw as it causes:
# > error: 'REDHAT_FIPS_VERSION' undeclared
# Patch45:  0045-FIPS-services-minimize.patch
# Execute KATS before HMAC verification
# RWMJ: Broken by removal of 0033
# Patch47:  0047-FIPS-early-KATS.patch
# Selectively disallow SHA1 signatures rhbz#2070977
Patch49:  0049-Allow-disabling-of-SHA1-signatures.patch
# Originally from https://github.com/openssl/openssl/pull/18103
# As we rebased to 3.0.7 and used the version of the function
# not matching the upstream one, we have to use aliasing.
# When we eliminate this patch, the `-Wl,--allow-multiple-definition`
# should also be removed
Patch56: 0056-strcasecmp.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2053289
Patch58:  0058-FIPS-limit-rsa-encrypt.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2087147
Patch61:  0061-Deny-SHA-1-signature-verification-in-FIPS-provider.patch
# 0062-fips-Expose-a-FIPS-indicator.patch
Patch62:  0062-fips-Expose-a-FIPS-indicator.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2102535
Patch73:  0073-FIPS-Use-OAEP-in-KATs-support-fixed-OAEP-seed.patch
# 0074-FIPS-Use-digest_sign-digest_verify-in-self-test.patch
Patch74:  0074-FIPS-Use-digest_sign-digest_verify-in-self-test.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2102535
Patch75:  0075-FIPS-Use-FFDHE2048-in-self-test.patch
# Downstream only. Reseed DRBG using getrandom(GRND_RANDOM)
# https://bugzilla.redhat.com/show_bug.cgi?id=2102541
#Patch76:  0076-FIPS-140-3-DRBG.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2102542
Patch77:  0077-FIPS-140-3-zeroization.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=2114772
Patch78:  0078-KDF-Add-FIPS-indicators.patch
# We believe that some changes present in CentOS are not necessary
# because ustream has a check for FIPS version
Patch80:  0080-rand-Forbid-truncated-hashes-SHA-3-in-FIPS-prov.patch
# 0081-signature-Remove-X9.31-padding-from-FIPS-prov.patch
Patch81:  0081-signature-Remove-X9.31-padding-from-FIPS-prov.patch
# 0083-hmac-Add-explicit-FIPS-indicator-for-key-length.patch
Patch83:  0083-hmac-Add-explicit-FIPS-indicator-for-key-length.patch
# 0084-pbkdf2-Set-minimum-password-length-of-8-bytes.patch
Patch84:  0084-pbkdf2-Set-minimum-password-length-of-8-bytes.patch
# 0085-FIPS-RSA-disable-shake.patch
Patch85:  0085-FIPS-RSA-disable-shake.patch
# 0088-signature-Add-indicator-for-PSS-salt-length.patch
Patch88:  0088-signature-Add-indicator-for-PSS-salt-length.patch
# 0091-FIPS-RSA-encapsulate.patch
Patch91:  0091-FIPS-RSA-encapsulate.patch
# 0093-DH-Disable-FIPS-186-4-type-parameters-in-FIPS-mode.patch
Patch93:  0093-DH-Disable-FIPS-186-4-type-parameters-in-FIPS-mode.patch
# 0110-GCM-Implement-explicit-FIPS-indicator-for-IV-gen.patch
Patch110: 0110-GCM-Implement-explicit-FIPS-indicator-for-IV-gen.patch
# 0112-pbdkf2-Set-indicator-if-pkcs5-param-disabled-checks.patch
Patch112: 0112-pbdkf2-Set-indicator-if-pkcs5-param-disabled-checks.patch
# 0113-asymciphers-kem-Add-explicit-FIPS-indicator.patch
Patch113: 0113-asymciphers-kem-Add-explicit-FIPS-indicator.patch
# We believe that some changes present in CentOS are not necessary
# because ustream has a check for FIPS version
Patch114: 0114-FIPS-enforce-EMS-support.patch
# Amend tests according to Fedora/RHEL code
Patch115: 0115-skip-quic-pairwise.patch
# Add version aliasing due to
# https://github.com/openssl/openssl/issues/23534
# Patch116: 0116-version-aliasing.patch
# https://github.com/openssl/openssl/issues/23050
Patch117: 0117-ignore-unknown-sigalgorithms-groups.patch
# https://fedoraproject.org/wiki/Changes/OpenSSLDistrustSHA1SigVer
# Patch120: 0120-Allow-disabling-of-SHA1-signatures.patch
# From CentOS 9
Patch121: 0121-FIPS-cms-defaults.patch
# [PATCH 50/50] Assign IANA numbers for hybrid PQ KEX Porting the fix
#  in https://github.com/openssl/openssl/pull/22803
Patch122: 0122-Assign-IANA-numbers-for-hybrid-PQ-KEX.patch
# https://github.com/openssl/openssl/issues/24577
Patch124: 0124-PBMAC1-PKCS12-FIPS-support.patch
# Downstream patch: enforce PBMAC1 in FIPS mode
Patch125: 0125-PBMAC1-PKCS12-FIPS-default.patch
# https://github.com/openssl/openssl/issues/25127
Patch126: 0126-pkeyutl-encap.patch
# https://github.com/openssl/openssl/issues/25056
Patch127: 0127-speedup-SSL_add_cert_subjects_to_stack.patch
Patch128: 0128-SAST-findings.patch

# MinGW patches
# Attempt to compute openssl modules dir dynamically from executable path if not set by OPENSSL_MODULES
Patch1000: openssl_compute_moddir.patch

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  make
BuildRequires:  lksctp-tools-devel
BuildRequires:  perl-interpreter
BuildRequires:  perl(base)
BuildRequires:  perl(Digest::SHA)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(File::Compare)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(IPC::Cmd)
BuildRequires:  perl(lib)
BuildRequires:  perl(Pod::Html)
BuildRequires:  sed
BuildRequires:  /usr/bin/cmp
BuildRequires:  /usr/bin/rename
BuildRequires:  /usr/bin/pod2man

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-dlfcn
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-zlib

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-dlfcn
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-zlib

BuildRequires:  ucrt64-filesystem >= 95
BuildRequires:  ucrt64-dlfcn
BuildRequires:  ucrt64-binutils
BuildRequires:  ucrt64-gcc
BuildRequires:  ucrt64-zlib


%if %{run_tests}
# Required both to build, and to run the tests.
# XXX This needs to be fixed - cross-compilation should not
# require running executables.
BuildRequires:  wine

# Required to run the tests.
BuildRequires:  xorg-x11-server-Xvfb
%endif


%description
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains Windows (MinGW) libraries and development tools.


# Win32
%package -n mingw32-openssl
Summary:        MinGW port of the OpenSSL toolkit
#Requires:       ca-certificates >= 2008-5
Requires:       pkgconfig

%description -n mingw32-openssl
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains Windows (MinGW) libraries and development tools.

%package -n mingw32-openssl-static
Summary:        Static version of the MinGW port of the OpenSSL toolkit
Requires:       mingw32-openssl = %{version}-%{release}

%description -n mingw32-openssl-static
Static version of the MinGW port of the OpenSSL toolkit.

# Win64
%package -n mingw64-openssl
Summary:        MinGW port of the OpenSSL toolkit
#Requires:       ca-certificates >= 2008-5
Requires:       pkgconfig

%description -n mingw64-openssl
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains Windows (MinGW) libraries and development tools.

%package -n mingw64-openssl-static
Summary:        Static version of the MinGW port of the OpenSSL toolkit
Requires:       mingw64-openssl = %{version}-%{release}

%description -n mingw64-openssl-static
Static version of the MinGW port of the OpenSSL toolkit.

# UCRT64
%package -n ucrt64-openssl
Summary:        MinGW port of the OpenSSL toolkit
#Requires:       ca-certificates >= 2008-5
Requires:       pkgconfig

%description -n ucrt64-openssl
The OpenSSL toolkit provides support for secure communications between
machines. OpenSSL includes a certificate management tool and shared
libraries which provide various cryptographic algorithms and
protocols.

This package contains Windows (MinGW) libraries and development tools.

%package -n ucrt64-openssl-static
Summary:        Static version of the MinGW port of the OpenSSL toolkit
Requires:       ucrt64-openssl = %{version}-%{release}

%description -n ucrt64-openssl-static
Static version of the MinGW port of the OpenSSL toolkit.


%{?mingw_debug_package}


%prep
%autosetup -S git -n openssl-%{version}

cp %{SOURCE12} crypto/ec/
cp %{SOURCE13} test/


# Create two copies of the source folder as OpenSSL doesn't support out of source builds
mkdir ../build_win32
mv * ../build_win32
mv ../build_win32 .
mkdir build_win64
cp -Rp build_win32/* build_win64
mkdir build_ucrt64
cp -Rp build_win32/* build_ucrt64


%build
###############################################################################
# Win32
###############################################################################
pushd build_win32

PERL=%{__perl} \
CFLAGS="%{mingw32_cflags}" \
LDFLAGS="%{mingw32_ldflags}" \
./Configure \
  --prefix=%{mingw32_prefix} \
  --libdir=%{mingw32_libdir} \
  --openssldir=%{mingw32_sysconfdir}/pki/tls \
  zlib enable-camellia enable-seed enable-rfc3779 \
  enable-cms enable-md2 enable-rc5 enable-ktls enable-fips \
  no-mdc2 no-ec2m no-sm2 no-sm4 \
  --cross-compile-prefix=%{mingw32_target}- \
  shared mingw \
  -Dsecure_getenv=getenv

make -s %{?_smp_mflags} all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

popd

###############################################################################
# Win64
###############################################################################
pushd build_win64

PERL=%{__perl} \
CFLAGS="%{mingw64_cflags}" \
LDFLAGS="%{mingw64_ldflags}" \
./Configure \
  --prefix=%{mingw64_prefix} \
  --libdir=%{mingw64_libdir} \
  --openssldir=%{mingw64_sysconfdir}/pki/tls \
  zlib enable-camellia enable-seed enable-rfc3779 \
  enable-cms enable-md2 enable-rc5 enable-ktls enable-fips \
  no-mdc2 no-ec2m no-sm2 no-sm4 \
  --cross-compile-prefix=%{mingw64_target}- \
  shared mingw64 \
  -Dsecure_getenv=getenv

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make -s %{?_smp_mflags} all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

popd

###############################################################################
# UCRT64
###############################################################################
pushd build_ucrt64

PERL=%{__perl} \
CFLAGS="%{ucrt64_cflags}" \
LDFLAGS="%{ucrt64_ldflags}" \
./Configure \
  --prefix=%{ucrt64_prefix} \
  --libdir=%{ucrt64_libdir} \
  --openssldir=%{ucrt64_sysconfdir}/pki/tls \
  zlib enable-camellia enable-seed enable-rfc3779 \
  enable-cms enable-md2 enable-rc5 enable-ktls enable-fips \
  no-mdc2 no-ec2m no-sm2 no-sm4 \
  --cross-compile-prefix=%{ucrt64_target}- \
  shared mingw64 \
  -Dsecure_getenv=getenv

# Do not run this in a production package the FIPS symbols must be patched-in
#util/mkdef.pl crypto update

make -s %{?_smp_mflags} all

# Clean up the .pc files
for i in libcrypto.pc libssl.pc openssl.pc ; do
  sed -i '/^Libs.private:/{s/-L[^ ]* //;s/-Wl[^ ]* //}' $i
done

popd


%if %{run_tests}
%check
#----------------------------------------------------------------------
# Run some tests.

# We must revert patch4 before tests otherwise they will fail
patch -p1 -R < %{PATCH4}

# This is a bit of a hack, but the test scripts look for 'openssl'
# by name.
pushd build_win32/apps
ln -s openssl.exe openssl
popd

# This is useful for diagnosing Wine problems.
WINEDEBUG=+loaddll
export WINEDEBUG

# Make sure we can find the installed DLLs.
WINEDLLPATH=%{mingw32_bindir}
export WINEDLLPATH

# The tests run Wine and require an X server (but don't really use
# it).  Therefore we create a virtual framebuffer for the duration of
# the tests.
# XXX There is no good way to choose a random, unused display.
# XXX Setting depth to 24 bits avoids bug 458219.
unset DISPLAY
display=:21
Xvfb $display -screen 0 1024x768x24 -ac -noreset & xpid=$!
trap "kill -TERM $xpid ||:" EXIT
sleep 3
DISPLAY=$display
export DISPLAY

make test

#----------------------------------------------------------------------
%endif

# Add generation of HMAC checksum of the final stripped library
##define __spec_install_post \
#    #{?__debug_package:#{__debug_install_post}} \
#    #{__arch_install_post} \
#    #{__os_install_post} \
#    fips/fips_standalone_sha1 %%{buildroot}/#{_lib}/libcrypto.so.#{version} >%%{buildroot}/#{_lib}/.libcrypto.so.#{version}.hmac \
#    ln -sf .libcrypto.so.#{version}.hmac %%{buildroot}/#{_lib}/.libcrypto.so.#{soversion}.hmac \
##{nil}


%install
mkdir -p %{buildroot}%{mingw32_libdir}/openssl
mkdir -p %{buildroot}%{mingw32_bindir}
mkdir -p %{buildroot}%{mingw32_includedir}
mkdir -p %{buildroot}%{mingw32_mandir}

mkdir -p %{buildroot}%{mingw64_libdir}/openssl
mkdir -p %{buildroot}%{mingw64_bindir}
mkdir -p %{buildroot}%{mingw64_includedir}
mkdir -p %{buildroot}%{mingw64_mandir}

mkdir -p %{buildroot}%{ucrt64_libdir}/openssl
mkdir -p %{buildroot}%{ucrt64_bindir}
mkdir -p %{buildroot}%{ucrt64_includedir}
mkdir -p %{buildroot}%{ucrt64_mandir}

%mingw_make_install DESTDIR=%{buildroot} install

# Install the file applink.c (#499934)
install -m644 build_win32/ms/applink.c %{buildroot}%{mingw32_includedir}/openssl/applink.c
install -m644 build_win64/ms/applink.c %{buildroot}%{mingw64_includedir}/openssl/applink.c
install -m644 build_ucrt64/ms/applink.c %{buildroot}%{ucrt64_includedir}/openssl/applink.c

# Remove the man pages
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}
rm -rf %{buildroot}%{ucrt64_mandir}

# Install a makefile for generating keys and self-signed certs, and a script
# for generating them on the fly.
mkdir -p %{buildroot}%{mingw32_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} %{buildroot}%{mingw32_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} %{buildroot}%{mingw32_bindir}/make-dummy-cert
install -m755 %{SOURCE7} %{buildroot}%{mingw32_bindir}/renew-dummy-cert

mkdir -p %{buildroot}%{mingw64_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} %{buildroot}%{mingw64_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} %{buildroot}%{mingw64_bindir}/make-dummy-cert
install -m755 %{SOURCE7} %{buildroot}%{mingw64_bindir}/renew-dummy-cert

mkdir -p %{buildroot}%{ucrt64_sysconfdir}/pki/tls/certs
install -m644 %{SOURCE2} %{buildroot}%{ucrt64_sysconfdir}/pki/tls/certs/Makefile
install -m755 %{SOURCE6} %{buildroot}%{ucrt64_bindir}/make-dummy-cert
install -m755 %{SOURCE7} %{buildroot}%{ucrt64_bindir}/renew-dummy-cert

mkdir -m700 %{buildroot}%{mingw32_sysconfdir}/pki/CA
mkdir -m700 %{buildroot}%{mingw32_sysconfdir}/pki/CA/private

mkdir -m700 %{buildroot}%{mingw64_sysconfdir}/pki/CA
mkdir -m700 %{buildroot}%{mingw64_sysconfdir}/pki/CA/private

mkdir -m700 %{buildroot}%{ucrt64_sysconfdir}/pki/CA
mkdir -m700 %{buildroot}%{ucrt64_sysconfdir}/pki/CA/private


# Win32
%files -n mingw32-openssl
%doc build_win32/LICENSE.txt
%{mingw32_bindir}/c_rehash
%{mingw32_bindir}/libcrypto-%{soversion}.dll
%{mingw32_bindir}/libssl-%{soversion}.dll
%{mingw32_bindir}/make-dummy-cert
%{mingw32_bindir}/openssl.exe
%{mingw32_bindir}/renew-dummy-cert
%{mingw32_libdir}/engines-%{soversion}
%{mingw32_libdir}/ossl-modules/
%{mingw32_libdir}/pkgconfig/*.pc
%{mingw32_libdir}/libcrypto.dll.a
%{mingw32_libdir}/libssl.dll.a
%{mingw32_includedir}/openssl/
%config(noreplace) %{mingw32_sysconfdir}/pki

%files -n mingw32-openssl-static
%{mingw32_libdir}/libcrypto.a
%{mingw32_libdir}/libssl.a

# Win64
%files -n mingw64-openssl
%doc build_win64/LICENSE.txt
%{mingw64_bindir}/c_rehash
%{mingw64_bindir}/libcrypto-%{soversion}-x64.dll
%{mingw64_bindir}/libssl-%{soversion}-x64.dll
%{mingw64_bindir}/make-dummy-cert
%{mingw64_bindir}/openssl.exe
%{mingw64_bindir}/renew-dummy-cert
%{mingw64_libdir}/engines-%{soversion}
%{mingw64_libdir}/ossl-modules/
%{mingw64_libdir}/pkgconfig/*.pc
%{mingw64_libdir}/libcrypto.dll.a
%{mingw64_libdir}/libssl.dll.a
%{mingw64_includedir}/openssl/
%config(noreplace) %{mingw64_sysconfdir}/pki

%files -n mingw64-openssl-static
%{mingw64_libdir}/libcrypto.a
%{mingw64_libdir}/libssl.a

# UCRT64
%files -n ucrt64-openssl
%doc build_win64/LICENSE.txt
%{ucrt64_bindir}/c_rehash
%{ucrt64_bindir}/libcrypto-%{soversion}-x64.dll
%{ucrt64_bindir}/libssl-%{soversion}-x64.dll
%{ucrt64_bindir}/make-dummy-cert
%{ucrt64_bindir}/openssl.exe
%{ucrt64_bindir}/renew-dummy-cert
%{ucrt64_libdir}/engines-%{soversion}
%{ucrt64_libdir}/ossl-modules/
%{ucrt64_libdir}/pkgconfig/*.pc
%{ucrt64_libdir}/libcrypto.dll.a
%{ucrt64_libdir}/libssl.dll.a
%{ucrt64_includedir}/openssl/
%config(noreplace) %{ucrt64_sysconfdir}/pki

%files -n ucrt64-openssl-static
%{ucrt64_libdir}/libcrypto.a
%{ucrt64_libdir}/libssl.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Mar 05 2025 Richard W.M. Jones <rjones@redhat.com> - 3.2.4-2
- Remove downstream 0076-FIPS-140-3-DRBG.patch which breaks Windows
  (RHBZ#2349935, RHBZ#2341677)

* Wed Feb 12 2025 Sandro Mani <manisandro@gmail.com> - 3.2.4-1
- Update to 3.2.4

* Mon Jan 20 2025 Sandro Mani <manisandro@gmail.com> - 3.2.2-4
- Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Jul 07 2024 Sandro Mani <manisandro@gmail.com> - 3.2.2-1
- Update to 3.2.2

* Tue Apr 02 2024 Jonathan Schleifer <js@nil.im> - 3.1.4-4
- Build UCRT64 package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 3.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 11 2024 Richard W.M. Jones <rjones@redhat.com> - 3.1.4-2
- Update to 3.1.4

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed May 31 2023 Sandro Mani <manisandro@gmail.com> - 3.0.9-1
- Update to 3.0.9

* Mon Nov 28 2022 Sandro Mani <manisandro@gmail.com> - 3.0.7-1
- Update to 3.0.7

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jul 08 2022 Sandro Mani <manisandro@gmail.com> - 3.0.5-1
- Update to 3.0.5

* Thu Jun 02 2022 Sandro Mani <manisandro@gmail.com> - 3.0.3-1
- Update to 3.0.3

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 3.0.2-2
- Rebuild with mingw-gcc-12

* Fri Mar 18 2022 Sandro Mani <manisandro@gmail.com> - 3.0.2-1
- Update to 3.0.2

* Mon Feb 21 2022 Sandro Mani <manisandro@gmail.com> - 3.0.0-2
- Attempt to compute openssl modules dir dynamically from executable path if not set by OPENSSL_MODULES

* Sun Jan 30 2022 Sandro Mani <manisandro@gmail.com> - 3.0.0-1
- Update to 3.0.0

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1k-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1k-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 01 2021 Richard W.M. Jones <rjones@redhat.com> - 1.1.1k-1
- Synch to Fedora openssl-1.1.1k-1.fc35

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1c-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 04 2020 Sandro Mani <manisandro@gmail.com> - 1.1.1c-6
- Ensure mingw CFLAGS and LDFLAGS are used
- Add BR: perl-File-Copy

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1c-5
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Richard W.M. Jones <rjones@redhat.com> - 1.1.1c-4
- +BR perl-FindBin and perl-lib, no longer pulled in implicitly.
- +BR perl-File-Compare.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1c-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 14 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.1.1c-1
- Update the sources accordingly to its native counter part, rhbz#1740772

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0h-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0h-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 24 2018 Christophe Fergeau <cfergeau@redhat.com> - 1.1.0h-1
- Sync with f28 openssl 1.1.0h

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2h-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu May 31 2018 Richard W.M. Jones <rjones@redhat.com> - 1.0.2h-6
- Remove mktemp build dependency, part of coreutils.

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2h-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Sep 09 2017 Sandro Mani <manisandro@gmail.com> - 1.0.2h-4
- Exclude *.debug files from non-debug packages

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2h-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2h-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Sat May  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.2h-1
- Synced with native openssl-1.0.2h-1
- Fixes RHBZ #1332591 #1332589 #1330104 #1312861 #1312857 #1307773 #1302768

* Sat Feb  6 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.2f-1
- Synced with native openssl-1.0.2f-2
- Fixes RHBZ #1239685 #1290334 #1302768

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.2a-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.2a-1
- Synced with native openssl-1.0.2a-1.fc23
- Fixes various CVE's (RHBZ #1203855 #1203856)

* Mon Dec 22 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1j-1
- Synced with native openssl-1.0.1j-3.fc22
- Add support for RFC 5649
- Prevent compiler warning "Please include winsock2.h before windows.h"
  when using the OpenSSL headers
- Fixes various CVE's (RHBZ #1127889 #1127709 #1152851)

* Thu Aug 21 2014 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.0.1i-1
- Synced with native openssl-1.0.1i-3.fc21
- Fixes various flaws (RHBZ#1096234 and RHBZ#1127705)
  CVE-2014-3505 CVE-2014-3506 CVE-2014-3507 CVE-2014-3511
  CVE-2014-3510 CVE-2014-3508 CVE-2014-3509 CVE-2014-0221
  CVE-2014-0198 CVE-2014-0224 CVE-2014-0195 CVE-2010-5298
  CVE-2014-3470

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1e-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Apr  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1e-6
- Synced patches with native openssl-1.0.1e-44.fc21
- Fixes CVE-2014-0160 (RHBZ #1085066)

* Sat Jan 25 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1e-5
- Synced patches with native openssl-1.0.1e-38.fc21
- Enable ECC support (RHBZ #1037919)
- Fixes CVE-2013-6450 (RHBZ #1047844)
- Fixes CVE-2013-4353 (RHBZ #1049062)
- Fixes CVE-2013-6449 (RHBZ #1045444)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1e-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1e-3
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Fri May 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1e-2
- Fix build of manual pages with current pod2man (#959439)

* Sun Mar 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1e-1
- Update to 1.0.1e (RHBZ #920868)
- Synced patches with native openssl-1.0.1e-4.fc19

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.1c-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1c-2
- Fix FTBFS against latest pod2man

* Fri Nov  9 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.1c-1
- Update to 1.0.1c
- Synced patches with native openssl-1.0.1c-7.fc19

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.0d-6
- Added win64 support

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 1.0.0d-5
- Pass the path to perl interpreter to Configure

* Tue Mar 06 2012 Kalev Lember <kalevlember@gmail.com> - 1.0.0d-4
- Renamed the source package to mingw-openssl (#800443)
- Modernize the spec file
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.0d-3
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0d-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Apr 23 2011 Kalev Lember <kalev@smartlink.ee> - 1.0.0d-1
- Update to 1.0.0d
- Synced patches with Fedora native openssl-1.0.0d-2

* Fri Mar 04 2011 Kai Tietz <ktietz@redhat.com>
- Fixes for CVE-2011-0014 openssl: OCSP stapling vulnerability

* Thu Mar  3 2011 Kai Tietz <ktietz@redhat.com> - 1.0.0a-3
- Bump and rebuild.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.0a-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 19 2010 Kalev Lember <kalev@smartlink.ee> - 1.0.0a-1
- Updated to openssl 1.0.0a
- Synced patches with Fedora native openssl-1.0.0a-1
- Use sed to fix up cflags instead of unmaintainable patch
- Rebased mingw32 specific patches
- Disabled capieng to fix build
- Properly regenerate def files with mkdef.pl and drop linker-fix.patch

* Thu Nov 26 2009 Kalev Lember <kalev@smartlink.ee> - 1.0.0-0.6.beta4
- Merged patches from native Fedora openssl (up to 1.0.0-0.16.beta4)
- Dropped the patch to fix non-fips mingw build,
  as it's now merged into fips patch from native openssl

* Sun Nov 22 2009 Kalev Lember <kalev@smartlink.ee> - 1.0.0-0.5.beta4
- Updated to version 1.0.0 beta 4
- Merged patches from native Fedora openssl (up to 1.0.0-0.15.beta4)
- Added patch to fix build with fips disabled

* Fri Sep 18 2009 Kalev Lember <kalev@smartlink.ee> - 1.0.0-0.4.beta3
- Rebuilt to fix debuginfo

* Sun Aug 30 2009 Kalev Lember <kalev@smartlink.ee> - 1.0.0-0.3.beta3
- Simplified the lib renaming patch

* Sun Aug 30 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.0-0.2.beta3
- Fixed invalid RPM Provides

* Fri Aug 28 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.0-0.1.beta3
- Update to version 1.0.0 beta 3
- Use %%global instead of %%define
- Automatically generate debuginfo subpackage
- Merged various changes from the native Fedora package (up to 1.0.0-0.5.beta3)
- Don't use the %%{_mingw32_make} macro anymore as it's ugly and causes side-effects
- Added missing BuildRequires mingw32-dlfcn (Kalev Lember)
- Reworked patches to rename *eay32.dll to lib*.dll (Kalev Lember)
- Patch Configure script to use %%{_mingw32_cflags} (Kalev Lember)

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8j-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May  9 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.9.8j-6
- Add the file include/openssl/applink.c to the package (BZ #499934)

* Tue Apr 14 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0.9.8j-5
- Fixed %%defattr line
- Added -static subpackage

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.8j-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 0.9.8j-3
- Rebuild for mingw32-gcc 4.4

* Mon Feb  2 2009 Levente Farkas <lfarkas@lfarkas.org> - 0.9.8j-2
- Various build fixes.

* Wed Jan 28 2009 Levente Farkas <lfarkas@lfarkas.org> - 0.9.8j-1
- update to new upstream version.

* Mon Dec 29 2008 Levente Farkas <lfarkas@lfarkas.org> - 0.9.8g-2
- minor cleanup.

* Tue Sep 30 2008 Richard W.M. Jones <rjones@redhat.com> - 0.9.8g-1
- Initial RPM release.
