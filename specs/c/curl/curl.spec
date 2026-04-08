# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# OpenSSL ENGINE support
# This is deprecated by OpenSSL since OpenSSL 3.0 and by Fedora since Fedora 41
# https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
# Change the bcond to 0 to turn off ENGINE support by default
%bcond openssl_engine_support %[%{defined fedora} || 0%{?rhel} < 10]

Summary: A utility for getting files from remote servers (FTP, HTTP, and others)
Name: curl
Version: 8.15.0
Release: 5%{?dist}
License: curl
Source0: https://curl.se/download/%{name}-%{version_no_tilde}.tar.xz
Source1: https://curl.se/download/%{name}-%{version_no_tilde}.tar.xz.asc
# The curl download page ( https://curl.se/download.html ) links
# to Daniel's address page https://daniel.haxx.se/address.html for the GPG Key,
# which points to the GPG key as of April 7th 2016 of https://daniel.haxx.se/mykey.asc
Source2: mykey.asc

# fix curl: tool_read_cb(): curl killed by SIGSEGV
Patch001: 0001-curl-8.15.0-curl-tool_read_cb-fix-of-segfault.patch

# fix broken TLS options for threaded LDAPS (CVE-2025-14017)
Patch002: 0002-curl-8.15.0-CVE-2025-14017.patch

# patch making libcurl multilib ready
Patch101: 0101-curl-7.32.0-multilib.patch

# test616: disable valgrind
Patch105: 0105-curl-8.11.1-test616.patch

Provides: curl-full = %{version}-%{release}
# do not fail when trying to install curl-minimal after drop
Provides: curl-minimal = %{version}-%{release}
Provides: webclient
URL: https://curl.se/

%if 0%{?fedora}
# instead of bundled wcurl utility, recommend wcurl package
Recommends: wcurl
%endif

# The reason for maintaining two separate packages for curl is no longer valid.
# The curl-minimal is currently almost identical to curl-full, so let's drop curl-minimal.
# For more details, see https://bugzilla.redhat.com/show_bug.cgi?id=2262096
Obsoletes: curl-minimal < 8.6.0-4

BuildRequires: automake
BuildRequires: brotli-devel
BuildRequires: coreutils
BuildRequires: gcc
BuildRequires: groff
BuildRequires: krb5-devel
BuildRequires: libidn2-devel
BuildRequires: libnghttp2-devel
BuildRequires: libpsl-devel
BuildRequires: libssh-devel
BuildRequires: libtool
BuildRequires: make
BuildRequires: openldap-devel
BuildRequires: openssh-clients
BuildRequires: openssh-server
BuildRequires: openssl
BuildRequires: openssl-devel
%if %{with openssl_engine_support} && 0%{?fedora} >= 41
BuildRequires:  openssl-devel-engine
%endif
BuildRequires: perl-interpreter
BuildRequires: pkgconfig
BuildRequires: python-unversioned-command
BuildRequires: python3-devel
BuildRequires: sed
BuildRequires: zlib-devel

# For gpg verification of source tarball
BuildRequires: gnupg2

# needed to compress content of tool_hugehelp.c after changing curl.1 man page
BuildRequires: perl(IO::Compress::Gzip)

# needed for generation of shell completions
BuildRequires: perl(Getopt::Long)
BuildRequires: perl(Pod::Usage)
BuildRequires: perl(strict)
BuildRequires: perl(warnings)

# needed for test1560 to succeed
BuildRequires: glibc-langpack-en

# gnutls-serv is used by the upstream test-suite
BuildRequires: gnutls-utils

# hostname(1) is used by the test-suite but it is missing in armv7hl buildroot
BuildRequires: hostname

# nghttpx (an HTTP/2 proxy) is used by the upstream test-suite
BuildRequires: nghttp2

# perl modules used in the test suite
BuildRequires: perl(B)
BuildRequires: perl(base)
BuildRequires: perl(constant)
BuildRequires: perl(Cwd)
BuildRequires: perl(Digest::MD5)
BuildRequires: perl(Digest::SHA)
BuildRequires: perl(Exporter)
BuildRequires: perl(File::Basename)
BuildRequires: perl(File::Copy)
BuildRequires: perl(File::Spec)
BuildRequires: perl(I18N::Langinfo)
BuildRequires: perl(IPC::Open2)
BuildRequires: perl(List::Util)
BuildRequires: perl(Memoize)
BuildRequires: perl(MIME::Base64)
BuildRequires: perl(POSIX)
BuildRequires: perl(Storable)
BuildRequires: perl(Time::HiRes)
BuildRequires: perl(Time::Local)
BuildRequires: perl(vars)

%if 0%{?fedora}
# needed for upstream test 1451
BuildRequires: python3-impacket
%endif

# The test-suite runs automatically through valgrind if valgrind is available
# on the system.  By not installing valgrind into mock's chroot, we disable
# this feature for production builds on architectures where valgrind is known
# to be less reliable, in order to avoid unnecessary build failures (see RHBZ
# #810992, #816175, and #886891).  Nevertheless developers are free to install
# valgrind manually to improve test coverage on any architecture.
%ifarch x86_64
BuildRequires: valgrind
%endif

# stunnel is used by upstream tests but it does not seem to work reliably
# on aarch64/s390x and occasionally breaks some tests (mainly 1561 and 1562)
%ifnarch aarch64 s390x
BuildRequires: stunnel
%endif

# using an older version of libcurl could result in CURLE_UNKNOWN_OPTION
Requires: libcurl%{?_isa} >= %{version}-%{release}

# Define OPENSSL_NO_ENGINE to avoid inclusion of <openssl/engine.h>
%if %{without openssl_engine_support}
%global _preprocessor_defines %{?_preprocessor_defines} -DOPENSSL_NO_ENGINE
%endif

# require at least the version of libnghttp2 that we were built against,
# to ensure that we have the necessary symbols available (#2144277)
%global libnghttp2_version %(pkg-config --modversion libnghttp2 2>/dev/null || echo 0)

# require at least the version of libpsl that we were built against,
# to ensure that we have the necessary symbols available (#1631804)
%global libpsl_version %(pkg-config --modversion libpsl 2>/dev/null || echo 0)

# require at least the version of libssh that we were built against,
# to ensure that we have the necessary symbols available (#525002, #642796)
%global libssh_version %(pkg-config --modversion libssh 2>/dev/null || echo 0)

# require at least the version of openssl-libs that we were built against,
# to ensure that we have the necessary symbols available (#1462184, #1462211)
# (we need to translate 3.0.0-alpha16 -> 3.0.0-0.alpha16 and 3.0.0-beta1 -> 3.0.0-0.beta1 though)
%global openssl_version %({ pkg-config --modversion openssl 2>/dev/null || echo 0;} | sed 's|-|-0.|')

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP.  curl supports SSL certificates, HTTP POST, HTTP PUT, FTP
uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, kerberos...), file transfer
resume, proxy tunneling and a busload of other useful tricks. 

%package -n libcurl
Summary: A library for getting files from web servers
Requires: libnghttp2%{?_isa} >= %{libnghttp2_version}
Requires: libpsl%{?_isa} >= %{libpsl_version}
Requires: libssh%{?_isa} >= %{libssh_version}
Requires: openssl-libs%{?_isa} >= 1:%{openssl_version}
Provides: libcurl-full = %{version}-%{release}
Provides: libcurl-full%{?_isa} = %{version}-%{release}

%description -n libcurl
libcurl is a free and easy-to-use client-side URL transfer library, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE, IMAP,
SMTP, POP3 and RTSP. libcurl supports SSL certificates, HTTP POST, HTTP PUT,
FTP uploading, HTTP form based upload, proxies, cookies, user+password
authentication (Basic, Digest, NTLM, Negotiate, Kerberos4), file transfer
resume, http proxy tunneling and more.

%package -n libcurl-devel
Summary: Files needed for building applications with libcurl
Requires: libcurl%{?_isa} = %{version}-%{release}

Provides: curl-devel = %{version}-%{release}
Provides: curl-devel%{?_isa} = %{version}-%{release}
Obsoletes: curl-devel < %{version}-%{release}

%description -n libcurl-devel
The libcurl-devel package includes header files and libraries necessary for
developing programs which use the libcurl library. It contains the API
documentation of the library, too.

%package -n libcurl-minimal
Summary: Conservatively configured build of libcurl for minimal installations
Requires: libnghttp2%{?_isa} >= %{libnghttp2_version}
Requires: openssl-libs%{?_isa} >= 1:%{openssl_version}
Provides: libcurl = %{version}-%{release}
Provides: libcurl%{?_isa} = %{version}-%{release}
Conflicts: libcurl%{?_isa}
RemovePathPostfixes: .minimal
# needed for RemovePathPostfixes to work with shared libraries
%undefine __brp_ldconfig

%description -n libcurl-minimal
This is a replacement of the 'libcurl' package for minimal installations.  It
comes with a limited set of features compared to the 'libcurl' package.  On the
other hand, the package is smaller and requires fewer run-time dependencies to
be installed.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -n %{name}-%{version_no_tilde} -p1

# disable test 1801
# <https://github.com/bagder/curl/commit/21e82bd6#commitcomment-12226582>
printf "1801\n" >>tests/data/DISABLED

# test3026: avoid pthread_create() failure due to resource exhaustion on i386
%ifarch %{ix86}
sed -e 's|NUM_THREADS 1000$|NUM_THREADS 256|' \
    -i tests/libtest/lib3026.c
%endif

# adapt test 323 for updated OpenSSL
sed -e 's|^35$|35,52|' -i tests/data/test323

# use localhost6 instead of ip6-localhost in the curl test-suite
(
    # avoid glob expansion in the trace output of `bash -x`
    { set +x; } 2>/dev/null
    cmd="sed -e 's|ip6-localhost|localhost6|' -i tests/data/test[0-9]*"
    printf "+ %s\n" "$cmd" >&2
    eval "$cmd"
)

# avoid unnecessary arch-dependent line in the processed file
sed -e '/# Used in @libdir@/d' \
    -i curl-config.in

%build
# regenerate the configure script and Makefile.in files
autoreconf -fiv

mkdir build-{full,minimal}
export common_configure_opts="          \
    --cache-file=../config.cache        \
    --disable-manual                    \
    --disable-static                    \
    --enable-hsts                       \
    --enable-ipv6                       \
    --enable-symbol-hiding              \
    --enable-threaded-resolver          \
    --without-zstd                      \
    --with-gssapi                       \
    --with-libidn2                      \
    --with-nghttp2                      \
    --with-ssl --with-ca-bundle=%{_sysconfdir}/pki/ca-trust/extracted/pem/tls-ca-bundle.pem \
    --with-zsh-functions-dir"

%global _configure ../configure

# configure minimal build
(
    cd build-minimal
    %configure $common_configure_opts   \
        --disable-dict                  \
        --disable-gopher                \
        --disable-imap                  \
        --disable-ldap                  \
        --disable-ldaps                 \
        --disable-mqtt                  \
        --disable-ntlm                  \
        --disable-pop3                  \
        --disable-rtsp                  \
        --disable-smb                   \
        --disable-smtp                  \
        --disable-telnet                \
        --disable-tftp                  \
        --disable-tls-srp               \
        --disable-websockets            \
        --without-brotli                \
        --without-libpsl                \
        --without-libssh
)

# configure full build
(
    cd build-full
    %configure $common_configure_opts   \
        --enable-dict                   \
        --enable-gopher                 \
        --enable-imap                   \
        --enable-ldap                   \
        --enable-ldaps                  \
        --enable-mqtt                   \
        --enable-ntlm                   \
        --enable-pop3                   \
        --enable-rtsp                   \
        --enable-smb                    \
        --enable-smtp                   \
        --enable-telnet                 \
        --enable-tftp                   \
        --enable-tls-srp                \
        --enable-websockets             \
        --with-brotli                   \
        --with-libpsl                   \
        --with-libssh
)

# avoid using rpath
sed -e 's/^runpath_var=.*/runpath_var=/' \
    -e 's/^hardcode_libdir_flag_spec=".*"$/hardcode_libdir_flag_spec=""/' \
    -i build-{full,minimal}/libtool

%make_build V=1 -C build-minimal
%make_build V=1 -C build-full

%check
# compile upstream test-cases
%make_build V=1 -C build-minimal/tests
%make_build V=1 -C build-full/tests

# relax crypto policy for the test-suite to make it pass again (#1610888)
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=XXX
export OPENSSL_CONF=

# make runtests.pl work for out-of-tree builds
export srcdir=../../tests

# prevent valgrind from being extremely slow (#1662656)
# https://fedoraproject.org/wiki/Changes/DebuginfodByDefault
unset DEBUGINFOD_URLS

# run the upstream test-suite for both curl-minimal and curl-full
for size in minimal full; do (
    cd build-${size}

    # we have to override LD_LIBRARY_PATH because we eliminated rpath
    export LD_LIBRARY_PATH="${PWD}/lib/.libs"

    cd tests
    perl -I../../tests ../../tests/runtests.pl -a -p -v '!flaky'
)
done


%install
# install and rename the library that will be packaged as libcurl-minimal
%make_install -C build-minimal/lib
rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.{la,so}
for i in ${RPM_BUILD_ROOT}%{_libdir}/*; do
    mv -v $i $i.minimal
done

# install libcurl.m4
install -d $RPM_BUILD_ROOT%{_datadir}/aclocal
install -m 644 docs/libcurl/libcurl.m4 $RPM_BUILD_ROOT%{_datadir}/aclocal

# install the executable and library that will be packaged as curl and libcurl
cd build-full
%make_install

# do not install /usr/share/fish/completions/curl.fish which is also installed
# by fish-3.0.2-1.module_f31+3716+57207597 and would trigger a conflict
rm -rf ${RPM_BUILD_ROOT}%{_datadir}/fish

rm -f ${RPM_BUILD_ROOT}%{_libdir}/libcurl.la

# do not install bundled wcurl utility
# it is provided by the wcurl package
rm -f ${RPM_BUILD_ROOT}%{_bindir}/wcurl
rm -f ${RPM_BUILD_ROOT}%{_mandir}/man1/wcurl.1*

%ldconfig_scriptlets -n libcurl

%ldconfig_scriptlets -n libcurl-minimal

%files
%doc CHANGES.md
%doc README
%doc docs/BUGS.md
%doc docs/DISTROS.md
%doc docs/FAQ
%doc docs/FEATURES.md
%doc docs/TODO
%doc docs/TheArtOfHttpScripting.md
%{_bindir}/curl
%{_mandir}/man1/curl.1*
%{_datadir}/zsh

%files -n libcurl
%license COPYING
%{_libdir}/libcurl.so.4
%{_libdir}/libcurl.so.4.[0-9].[0-9]

%files -n libcurl-devel
%doc docs/examples/*.c docs/examples/Makefile.example docs/INTERNALS.md
%doc docs/CONTRIBUTE.md docs/libcurl/ABI.md
%{_bindir}/curl-config*
%{_includedir}/curl
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man1/curl-config.1*
%{_mandir}/man3/*
%{_datadir}/aclocal/libcurl.m4

%files -n libcurl-minimal
%license COPYING
%{_libdir}/libcurl.so.4.minimal
%{_libdir}/libcurl.so.4.[0-9].[0-9].minimal

%changelog
* Mon Jan 19 2026 Jan Macku <jamacku@redhat.com> - 8.15.0-5
- fix broken TLS options for threaded LDAPS (CVE-2025-14017)

* Thu Dec 04 2025 Jan Macku <jamacku@redhat.com> - 8.15.0-4
- fix curl: tool_read_cb(): curl killed by SIGSEGV (#2417738)

* Thu Nov 13 2025 Jan Macku <jamacku@redhat.com> - 8.15.0-3
- remove bundled wcurl utility that was added in 8.14.0~rc1, use wcurl package instead

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Jan Macku <jamacku@redhat.com> - 8.15.0-1
- new upstream release

* Thu Jul 10 2025 Jan Macku <jamacku@redhat.com> - 8.15.0~rc3-1
- new upstream release candidate

* Mon Jun 30 2025 Jan Macku <jamacku@redhat.com> - 8.15.0~rc2-1
- new upstream release candidate

* Mon Jun 23 2025 Jan Macku <jamacku@redhat.com> - 8.15.0~rc1-1
- new upstream release candidate

* Wed Jun 04 2025 Jan Macku <jamacku@redhat.com> - 8.14.1-1
- new upstream release
- drop: 0001-curl-8.14.0-multi-fix-add_handle-resizing.patch (no longer needed)

* Wed May 28 2025 Jan Macku <jamacku@redhat.com> - 8.14.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2025-5025 - No QUIC certificate pinning with wolfSSL
    CVE-2025-4947 - QUIC certificate check skip with wolfSSL
- fix regression: curl_multi_add_handle() returning OOM when using more than 400 handles

* Fri May 02 2025 Jan Macku <jamacku@redhat.com> - 8.14.0~rc1-1
- new upstream release candidate
- new utility: wcurl which lets you download URLs without having to remember any parameters

* Wed Apr 02 2025 Jan Macku <jamacku@redhat.com> - 8.13.0-1
- new upstream release
- add build time dependency on openssl (required by tests)

* Wed Mar 26 2025 Jan Macku <jamacku@redhat.com> - 8.13.0~rc3-1
- new upstream release candidate
- drop: 0102-curl-7.84.0-test3026.patch (no longer needed)

* Tue Mar 18 2025 Jan Macku <jamacku@redhat.com> - 8.13.0~rc2-1
- new upstream release candidate

* Thu Mar 13 2025 Jan Macku <jamacku@redhat.com> - 8.13.0~rc1-2
- fix --cert parameter (#2351531)

* Mon Mar 10 2025 Jan Macku <jamacku@redhat.com> - 8.13.0~rc1-1
- new upstream release candidate

* Wed Feb 05 2025 Jan Macku <jamacku@redhat.com> - 8.12.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2025-0725 - gzip integer overflow
    CVE-2025-0665 - eventfd double close
    CVE-2025-0167 - netrc and default credential leak
- drop upstreamed patches

* Fri Jan 31 2025 Jan Macku <jamacku@redhat.com> - 8.11.1-4
- TLS: check connection for SSL use, not handler (#2324130#c7)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.11.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sun Dec 15 2024 Paul Howarth <paul@city-fan.org> - 8.11.1-2
- Fix crash with Unexpected error 9 on netlink descriptor 10 (rhbz#2332350)
  - https://github.com/curl/curl/issues/15725
  - https://github.com/curl/curl/pull/15727

* Wed Dec 11 2024 Jan Macku <jamacku@redhat.com> - 8.11.1-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2024-11053 - netrc and redirect credential leak

* Wed Nov 06 2024 Yaakov Selkowitz <yselkowi@redhat.com> - 8.11.0-2
- Disable engine support on RHEL 10+

* Wed Nov 06 2024 Jan Macku <jamacku@redhat.com> - 8.11.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2024-9681 - HSTS subdomain overwrites parent cache entry

* Tue Sep 24 2024 Jan Macku <jamacku@redhat.com> - 8.10.1-2
- Use tls-ca-bundle.pem instead of ca-bundle.crt (OpenSSL specific) (#2313564)

* Wed Sep 18 2024 Jan Macku <jamacku@redhat.com> - 8.10.1-1
- new upstream release

* Wed Sep 11 2024 Jan Macku <jamacku@redhat.com> - 8.10.0-1
- new upstream release

* Wed Aug 21 2024 Jacek Migacz <jmigacz@redhat.com> - 8.9.1-3
- Retire deprecated ntlm-wb configure option

* Mon Aug 5 2024 voidanix <voidanix@keyedlimepie.org> - 8.9.1-2
- Apply SIGPIPE-related patch due to upstream regression

* Wed Jul 24 2024 Jan Macku <jamacku@redhat.com> - 8.9.1-1
- new upstream release

* Wed Jul 24 2024 Jan Macku <jamacku@redhat.com> - 8.9.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2024-6874 - macidn punycode buffer overread
    CVE-2024-6197 - freeing stack buffer in utf8asn1str
- drop upstreamed patches

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jul 12 2024 Paul Howarth <paul@city-fan.org> - 8.8.0-2
- adapt for https://fedoraproject.org/wiki/Changes/OpensslDeprecateEngine
- added build condition for openssl_engine_support, true by default so as to
  not change the resulting built package (yet)
- with openssl_engine_support true, BR: openssl-devel-engine
- with openssl_engine_support false, build with -DOPENSSL_NO_ENGINE

* Wed May 22 2024 Jan Macku <jamacku@redhat.com> - 8.8.0-1
- new upstream release
- drop upstreamed patches

* Wed Mar 27 2024 Jan Macku <jamacku@redhat.com> - 8.7.1-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2024-2004 - Usage of disabled protocol
    CVE-2024-2379 - QUIC certificate check bypass with wolfSSL
    CVE-2024-2398 - HTTP/2 push headers memory-leak
    CVE-2024-2466 - TLS certificate check bypass with mbedTLS
- drop upstreamed patches
- reenable test 0313
- fix zsh completions, use --with-zsh-functions-dir
- apply upstream patches for 8.7.1 issues and regressions

* Mon Feb 19 2024 Jan Macku <jamacku@redhat.com> - 8.6.0-7
- Fix: Leftovers after chunking should not be part of the curl buffer output (#2264220)

* Mon Feb 12 2024 Jan Macku <jamacku@redhat.com> - 8.6.0-6
- revert "receive max buffer" + add test case
- temporarily disable test 0313
- remove suggests of libcurl-minimal in curl-full

* Mon Feb 12 2024 Jan Macku <jamacku@redhat.com> - 8.6.0-5
- add Provides to curl-minimal

* Wed Feb 07 2024 Jan Macku <jamacku@redhat.com> - 8.6.0-4
- drop curl-minimal subpackage in favor of curl-full (#2262096)

* Mon Feb 05 2024 Jan Macku <jamacku@redhat.com> - 8.6.0-3
- ignore response body to HEAD requests

* Fri Feb 02 2024 Jan Macku <jamacku@redhat.com> - 8.6.0-2
- don't build manual for curl-full - use man 1 curl instead (#2262373)

* Thu Feb 01 2024 Jan Macku <jamacku@redhat.com> - 8.6.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2024-0853 - OCSP verification bypass with TLS session reuse
- drop 001-dist-add-tests-errorcodes.pl-to-the-tarball.patch (replaced by upstream fix)
- remove accidentally included mk-ca-bundle.1 man page (upstream bug #12843)

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Dec 06 2023 Jan Macku <jamacku@redhat.com> - 8.5.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2023-46218 - cookie mixed case PSL bypass
    CVE-2023-46219 - HSTS long file name clears contents

* Wed Oct 11 2023 Jan Macku <jamacku@redhat.com> - 8.4.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2023-38545 - SOCKS5 heap buffer overflow
    CVE-2023-38546 - cookie injection with none file

* Wed Sep 13 2023 Jan Macku <jamacku@redhat.com> - 8.3.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2023-38039 - HTTP headers eat all memory

* Wed Aug 02 2023 Jan Macku <jamacku@redhat.com> - 8.2.1-2
- enable websockets (#2224651)

* Wed Jul 26 2023 Lukáš Zaoral <lzaoral@redhat.com> - 8.2.1-1
- new upstream release (rhbz#2226659)

* Wed Jul 19 2023 Jan Macku <jamacku@redhat.com> - 8.2.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2023-32001 - fopen race condition

* Tue May 30 2023 Jan Macku <jamacku@redhat.com> - 8.1.2-1
- new upstream release, with small bugfixes and improvements

* Tue May 23 2023 Jan Macku <jamacku@redhat.com> - 8.1.1-1
- new upstream release, with small bugfixes and improvements

* Wed May 17 2023 Kamil Dudka <kdudka@redhat.com> - 8.1.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2023-28321 - IDN wildcard match
    CVE-2023-28322 - more POST-after-PUT confusion

* Fri Apr 21 2023 Kamil Dudka <kdudka@redhat.com> - 8.0.1-3
- tests: re-enable temporarily disabled test-cases
- tests: attempt to fix a conflict on port numbers
- apply patches automatically

* Tue Mar 21 2023 Lukáš Zaoral <lzaoral@redhat.com> - 8.0.1-2
- migrated to SPDX license

* Mon Mar 20 2023 Kamil Dudka <kdudka@redhat.com> - 8.0.1-1
- new upstream release

* Mon Mar 20 2023 Kamil Dudka <kdudka@redhat.com> - 8.0.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2023-27538 - SSH connection too eager reuse still
    CVE-2023-27537 - HSTS double-free
    CVE-2023-27536 - GSS delegation too eager connection re-use
    CVE-2023-27535 - FTP too eager connection reuse
    CVE-2023-27534 - SFTP path ~ resolving discrepancy
    CVE-2023-27533 - TELNET option IAC injection

* Mon Feb 20 2023 Kamil Dudka <kdudka@redhat.com> - 7.88.1-1
- new upstream release

* Fri Feb 17 2023 Kamil Dudka <kdudka@redhat.com> - 7.88.0-2
- http2: set drain on stream end

* Wed Feb 15 2023 Kamil Dudka <kdudka@redhat.com> - 7.88.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2023-23916 - HTTP multi-header compression denial of service
    CVE-2023-23915 - HSTS amnesia with --parallel
    CVE-2023-23914 - HSTS ignored on multiple requests

* Fri Jan 20 2023 Kamil Dudka <kdudka@redhat.com> - 7.87.0-4
- fix regression in a public header file (#2162716)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.87.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Kamil Dudka <kdudka@redhat.com> - 7.87.0-2
- test3012: temporarily disable valgrind (#2143040)

* Wed Dec 21 2022 Kamil Dudka <kdudka@redhat.com> - 7.87.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2022-43552 - HTTP Proxy deny use-after-free
    CVE-2022-43551 - Another HSTS bypass via IDN

* Tue Nov 29 2022 Kamil Dudka <kdudka@redhat.com> - 7.86.0-4
- noproxy: tailmatch like in 7.85.0 and earlier (#2149224)

* Thu Nov 24 2022 Kamil Dudka <kdudka@redhat.com> - 7.86.0-3
- enforce versioned libnghttp2 dependency for libcurl (#2144277)

* Mon Oct 31 2022 Kamil Dudka <kdudka@redhat.com> - 7.86.0-2
- fix regression in noproxy matching

* Wed Oct 26 2022 Kamil Dudka <kdudka@redhat.com> - 7.86.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2022-42916 - HSTS bypass via IDN
    CVE-2022-42915 - HTTP proxy double-free
    CVE-2022-35260 - .netrc parser out-of-bounds access
    CVE-2022-32221 - POST following PUT confusion

* Thu Sep 01 2022 Kamil Dudka <kdudka@redhat.com> - 7.85.0-1
- new upstream release, which fixes the following vulnerability
    CVE-2022-35252 - control code in cookie denial of service

* Thu Aug 25 2022 Kamil Dudka <kdudka@redhat.com> - 7.84.0-3
- tests: fix http2 tests to use CRLF headers to make it work with nghttp2-1.49.0

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.84.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Mon Jun 27 2022 Kamil Dudka <kdudka@redhat.com> - 7.84.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2022-32207 - Unpreserved file permissions
    CVE-2022-32205 - Set-Cookie denial of service
    CVE-2022-32206 - HTTP compression denial of service
    CVE-2022-32208 - FTP-KRB bad message verification

* Wed May 11 2022 Kamil Dudka <kdudka@redhat.com> - 7.83.1-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2022-27782 - fix too eager reuse of TLS and SSH connections
    CVE-2022-27779 - do not accept cookies for TLD with trailing dot
    CVE-2022-27778 - do not remove wrong file on error
    CVE-2022-30115 - hsts: ignore trailing dots when comparing hosts names
    CVE-2022-27780 - reject percent-encoded path separator in URL host

* Wed Apr 27 2022 Kamil Dudka <kdudka@redhat.com> - 7.83.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2022-27774 - curl credential leak on redirect
    CVE-2022-27776 - curl auth/cookie leak on redirect
    CVE-2022-27775 - curl bad local IPv6 connection reuse
    CVE-2022-22576 - curl OAUTH2 bearer bypass in connection re-use

* Tue Mar 15 2022 Kamil Dudka <kdudka@redhat.com> - 7.82.0-2
- openssl: fix incorrect CURLE_OUT_OF_MEMORY error on CN check failure

* Sat Mar 05 2022 Kamil Dudka <kdudka@redhat.com> - 7.82.0-1
- new upstream release

* Thu Feb 24 2022 Kamil Dudka <kdudka@redhat.com> - 7.81.0-4
- enable IDN support also in libcurl-minimal

* Thu Feb 10 2022 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 7.81.0-3
- Suggest libcurl-minimal in curl-minimal

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.81.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Kamil Dudka <kdudka@redhat.com> - 7.81.0-1
- new upstream release

* Sun Nov 14 2021 Paul Howarth <paul@city-fan.org> - 7.80.0-2
- sshserver.pl (used in test suite) now requires the Digest::SHA perl module

* Wed Nov 10 2021 Kamil Dudka <kdudka@redhat.com> - 7.80.0-1
- new upstream release

* Tue Oct 26 2021 Kamil Dudka <kdudka@redhat.com> - 7.79.1-3
- re-enable HSTS in libcurl-minimal as a security feature (#2005874)

* Mon Oct 04 2021 Kamil Dudka <kdudka@redhat.com> - 7.79.1-2
- disable more protocols and features in libcurl-minimal (#2005874)

* Wed Sep 22 2021 Kamil Dudka <kdudka@redhat.com> - 7.79.1-1
- new upstream release

* Thu Sep 16 2021 Kamil Dudka <kdudka@redhat.com> - 7.79.0-4
- fix regression in http2 implementation introduced in the last release

* Thu Sep 16 2021 Sahana Prasad <sahana@redhat.com> - 7.79.0-3
- Rebuilt with OpenSSL 3.0.0

* Thu Sep 16 2021 Kamil Dudka <kdudka@redhat.com> - 7.79.0-2
- make SCP/SFTP tests work with openssh-8.7p1

* Wed Sep 15 2021 Kamil Dudka <kdudka@redhat.com> - 7.79.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2021-22947 - STARTTLS protocol injection via MITM
    CVE-2021-22946 - protocol downgrade required TLS bypassed
    CVE-2021-22945 - use-after-free and double-free in MQTT sending

* Tue Sep 14 2021 Sahana Prasad <sahana@redhat.com> - 7.78.0-4
- Rebuilt with OpenSSL 3.0.0

* Fri Jul 23 2021 Kamil Dudka <kdudka@redhat.com> - 7.78.0-3
- make explicit dependency on openssl work with alpha/beta builds of openssl

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.78.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jul 21 2021 Kamil Dudka <kdudka@redhat.com> - 7.78.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2021-22925 - TELNET stack contents disclosure again
    CVE-2021-22924 - bad connection reuse due to flawed path name checks
    CVE-2021-22923 - metalink download sends credentials
    CVE-2021-22922 - wrong content via metalink not discarded

* Wed Jun 02 2021 Kamil Dudka <kdudka@redhat.com> - 7.77.0-2
- build the curl tool without metalink support (#1967213)

* Wed May 26 2021 Kamil Dudka <kdudka@redhat.com> - 7.77.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2021-22901 - TLS session caching disaster
    CVE-2021-22898 - TELNET stack contents disclosure

* Mon May 03 2021 Kamil Dudka <kdudka@redhat.com> - 7.76.1-2
- http2: fix resource leaks detected by Coverity

* Wed Apr 14 2021 Kamil Dudka <kdudka@redhat.com> - 7.76.1-1
- new upstream release

* Wed Mar 31 2021 Kamil Dudka <kdudka@redhat.com> - 7.76.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2021-22890 - TLS 1.3 session ticket proxy host mixup
    CVE-2021-22876 - Automatic referer leaks credentials

* Wed Mar 24 2021 Kamil Dudka <kdudka@redhat.com> - 7.75.0-3
- fix SIGSEGV upon disconnect of a ldaps:// transfer

* Tue Feb 23 2021 Kamil Dudka <kdudka@redhat.com> - 7.75.0-2
- build-require python3-impacket only on Fedora

* Wed Feb 03 2021 Kamil Dudka <kdudka@redhat.com> - 7.75.0-1
- new upstream release

* Tue Jan 26 2021 Kamil Dudka <kdudka@redhat.com> - 7.74.0-4
- do not use stunnel for tests on s390x builds to avoid spurious failures

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.74.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 09 2020 Kamil Dudka <kdudka@redhat.com> - 7.74.0-2
- do not rewrite shebangs in test-suite to use python3 explicitly

* Wed Dec 09 2020 Kamil Dudka <kdudka@redhat.com> - 7.74.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2020-8286 - curl: Inferior OCSP verification
    CVE-2020-8285 - libcurl: FTP wildcard stack overflow
    CVE-2020-8284 - curl: trusting FTP PASV responses

* Wed Oct 14 2020 Kamil Dudka <kdudka@redhat.com> - 7.73.0-2
- prevent upstream test 1451 from being skipped

* Wed Oct 14 2020 Kamil Dudka <kdudka@redhat.com> - 7.73.0-1
- new upstream release

* Thu Sep 10 2020 Jinoh Kang <aurhb20@protonmail.ch> - 7.72.0-2
- fix multiarch conflicts in libcurl-minimal (#1877671)

* Wed Aug 19 2020 Kamil Dudka <kdudka@redhat.com> - 7.72.0-1
- new upstream release, which fixes the following vulnerability
    CVE-2020-8231 - libcurl: wrong connect-only connection

* Thu Aug 06 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.1-5
- setopt: unset NOBODY switches to GET if still HEAD

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.71.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 7.71.1-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Fri Jul 03 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.1-2
- curl: make the --krb option work again (#1833193)

* Wed Jul 01 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.1-1
- new upstream release

* Wed Jun 24 2020 Kamil Dudka <kdudka@redhat.com> - 7.71.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2020-8169 - curl: Partial password leak over DNS on HTTP redirect
    CVE-2020-8177 - curl: overwrite local file with -J

* Wed Apr 29 2020 Kamil Dudka <kdudka@redhat.com> - 7.70.0-1
- new upstream release

* Mon Apr 20 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.1-3
- SSH: use new ECDSA key types to check known hosts (#1824926)

* Fri Apr 17 2020 Tom Stellard <tstellar@redhat.com> - 7.69.1-2
- Prevent discarding of -g when compiling with clang

* Wed Mar 11 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.1-1
- new upstream release

* Mon Mar 09 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.0-2
- make Flatpak work again (#1810989)

* Wed Mar 04 2020 Kamil Dudka <kdudka@redhat.com> - 7.69.0-1
- new upstream release

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.68.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jan 08 2020 Kamil Dudka <kdudka@redhat.com> - 7.68.0-1
- new upstream release

* Thu Nov 14 2019 Kamil Dudka <kdudka@redhat.com> - 7.67.0-2
- fix infinite loop on upload using a glob (#1771025)

* Wed Nov 06 2019 Kamil Dudka <kdudka@redhat.com> - 7.67.0-1
- new upstream release

* Wed Sep 11 2019 Kamil Dudka <kdudka@redhat.com> - 7.66.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2019-5481 - double free due to subsequent call of realloc()
    CVE-2019-5482 - heap buffer overflow in function tftp_receive_packet()

* Tue Aug 27 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.3-4
- avoid reporting spurious error in the HTTP2 framing layer (#1690971)

* Thu Aug 01 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.3-3
- improve handling of gss_init_sec_context() failures

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.65.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Jul 20 2019 Paul Howarth <paul@city-fan.org> - 7.65.3-1
- new upstream release

* Wed Jul 17 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.2-1
- new upstream release

* Wed Jun 05 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.1-1
- new upstream release

* Thu May 30 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.0-2
- fix spurious timeout events with speed-limit (#1714893)

* Wed May 22 2019 Kamil Dudka <kdudka@redhat.com> - 7.65.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2019-5436 - TFTP receive buffer overflow
    CVE-2019-5435 - integer overflows in curl_url_set()

* Thu May 09 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.1-2
- do not treat failure of gss_init_sec_context() with --negotiate as fatal

* Wed Mar 27 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.1-1
- new upstream release

* Mon Mar 25 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-6
- remove verbose "Expire in" ... messages (#1690971)

* Thu Mar 21 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-5
- avoid spurious "Could not resolve host: [host name]" error messages

* Wed Feb 27 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-4
- fix NULL dereference if flushing cookies with no CookieInfo set (#1683676)

* Mon Feb 25 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-3
- prevent NetworkManager from leaking file descriptors (#1680198)

* Mon Feb 11 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-2
- make zsh completion work again

* Wed Feb 06 2019 Kamil Dudka <kdudka@redhat.com> - 7.64.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2019-3823 - SMTP end-of-response out-of-bounds read
    CVE-2019-3822 - NTLMv2 type-3 header stack buffer overflow
    CVE-2018-16890 - NTLM type-2 out-of-bounds buffer read

* Mon Feb 04 2019 Kamil Dudka <kdudka@redhat.com> - 7.63.0-7
- prevent valgrind from reporting false positives on x86_64

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.63.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan 21 2019 Kamil Dudka <kdudka@redhat.com> - 7.63.0-5
- xattr: strip credentials from any URL that is stored (CVE-2018-20483)

* Fri Jan 04 2019 Kamil Dudka <kdudka@redhat.com> - 7.63.0-4
- replace 0105-curl-7.63.0-libstubgss-ldadd.patch by upstream patch

* Wed Dec 19 2018 Kamil Dudka <kdudka@redhat.com> - 7.63.0-3
- curl -J: do not append to the destination file (#1658574)

* Fri Dec 14 2018 Kamil Dudka <kdudka@redhat.com> - 7.63.0-2
- revert an upstream commit that broke `fedpkg new-sources` (#1659329)

* Wed Dec 12 2018 Kamil Dudka <kdudka@redhat.com> - 7.63.0-1
- new upstream release

* Wed Oct 31 2018 Kamil Dudka <kdudka@redhat.com> - 7.62.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-16839 - SASL password overflow via integer overflow
    CVE-2018-16840 - use-after-free in handle close
    CVE-2018-16842 - warning message out-of-buffer read

* Thu Oct 11 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.1-3
- enable TLS 1.3 post-handshake auth in OpenSSL
- update the documentation of --tlsv1.0 in curl(1) man page

* Thu Oct 04 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.1-2
- enforce versioned libpsl dependency for libcurl (#1631804)
- test320: update expected output for gnutls-3.6.4
- drop 0105-curl-7.61.0-tests-ssh-keygen.patch no longer needed (#1622594)

* Wed Sep 05 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.1-1
- new upstream release, which fixes the following vulnerability
    CVE-2018-14618 - NTLM password overflow via integer overflow

* Tue Sep 04 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-8
- make the --tls13-ciphers option work

* Mon Aug 27 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-7
- tests: make ssh-keygen always produce PEM format (#1622594)

* Wed Aug 15 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-6
- scp/sftp: fix infinite connect loop on invalid private key (#1595135)

* Thu Aug 09 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-5
- ssl: set engine implicitly when a PKCS#11 URI is provided (#1219544)

* Tue Aug 07 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-4
- relax crypto policy for the test-suite to make it pass again (#1610888)

* Tue Jul 31 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-3
- disable flaky test 1900, which covers deprecated HTTP pipelining
- adapt test 323 for updated OpenSSL

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.61.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Kamil Dudka <kdudka@redhat.com> - 7.61.0-1
- new upstream release, which fixes the following vulnerability
    CVE-2018-0500 - SMTP send heap buffer overflow

* Tue Jul 10 2018 Kamil Dudka <kdudka@redhat.com> - 7.60.0-3
- enable support for brotli compression in libcurl-full

* Wed Jul 04 2018 Kamil Dudka <kdudka@redhat.com> - 7.60.0-2
- do not hard-wire path of the Python 3 interpreter

* Wed May 16 2018 Kamil Dudka <kdudka@redhat.com> - 7.60.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-1000300 - FTP shutdown response buffer overflow
    CVE-2018-1000301 - RTSP bad headers buffer over-read

* Thu Mar 15 2018 Kamil Dudka <kdudka@redhat.com> - 7.59.0-3
- make the test-suite use Python 3

* Wed Mar 14 2018 Kamil Dudka <kdudka@redhat.com> - 7.59.0-2
- ftp: fix typo in recursive callback detection for seeking

* Wed Mar 14 2018 Kamil Dudka <kdudka@redhat.com> - 7.59.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-1000120 - FTP path trickery leads to NIL byte out of bounds write
    CVE-2018-1000121 - LDAP NULL pointer dereference
    CVE-2018-1000122 - RTSP RTP buffer over-read

* Mon Mar 12 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-8
- http2: mark the connection for close on GOAWAY

* Mon Feb 19 2018 Paul Howarth <paul@city-fan.org> - 7.58.0-7
- Add explicity-used build requirements
- Fix libcurl soname version number in %%files list to avoid accidental soname
  bumps

* Thu Feb 15 2018 Paul Howarth <paul@city-fan.org> - 7.58.0-6
- switch to %%ldconfig_scriptlets
- drop legacy BuildRoot: and Group: tags
- enforce versioned libssh dependency for libcurl

* Tue Feb 13 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-5
- drop temporary workaround for #1540549

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.58.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-3
- temporarily work around internal compiler error on x86_64 (#1540549)
- disable brp-ldconfig to make RemovePathPostfixes work with shared libs again

* Wed Jan 24 2018 Andreas Schneider <asn@redhat.com> - 7.58.0-2
- use libssh (instead of libssh2) to implement SCP/SFTP in libcurl (#1531483)

* Wed Jan 24 2018 Kamil Dudka <kdudka@redhat.com> - 7.58.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2018-1000005 - curl: HTTP/2 trailer out-of-bounds read
    CVE-2018-1000007 - curl: HTTP authentication leak in redirects

* Wed Nov 29 2017 Kamil Dudka <kdudka@redhat.com> - 7.57.0-1
- new upstream release, which fixes the following vulnerabilities
    CVE-2017-8816 - curl: NTLM buffer overflow via integer overflow
    CVE-2017-8817 - curl: FTP wildcard out of bounds read
    CVE-2017-8818 - curl: SSL out of buffer access

* Mon Oct 23 2017 Kamil Dudka <kdudka@redhat.com> - 7.56.1-1
- new upstream release (fixes CVE-2017-1000257)

* Wed Oct 04 2017 Kamil Dudka <kdudka@redhat.com> - 7.56.0-1
- new upstream release (fixes CVE-2017-1000254)

* Mon Aug 28 2017 Kamil Dudka <kdudka@redhat.com> - 7.55.1-5
- apply the patch for the previous commit and fix its name (#1485702)

* Mon Aug 28 2017 Bastien Nocera <bnocera@redhat.com> - 7.55.1-4
- Fix NetworkManager connectivity check not working (#1485702)

* Tue Aug 22 2017 Kamil Dudka <kdudka@redhat.com> 7.55.1-3
- utilize system wide crypto policies for TLS (#1483972)

* Tue Aug 15 2017 Kamil Dudka <kdudka@redhat.com> 7.55.1-2
- make zsh completion work again

* Mon Aug 14 2017 Kamil Dudka <kdudka@redhat.com> 7.55.1-1
- new upstream release

* Wed Aug 09 2017 Kamil Dudka <kdudka@redhat.com> 7.55.0-1
- drop multilib fix for libcurl header files no longer needed
- new upstream release, which fixes the following vulnerabilities
    CVE-2017-1000099 - FILE buffer read out of bounds
    CVE-2017-1000100 - TFTP sends more than buffer size
    CVE-2017-1000101 - URL globbing out of bounds read

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.54.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Fri Jul 28 2017 Florian Weimer <fweimer@redhat.com> - 7.54.1-7
- Rebuild with fixed binutils (#1475636)

* Fri Jul 28 2017 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 7.54.1-6
- Enable separate debuginfo back

* Thu Jul 27 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-5
- rebuild to fix broken linkage of cmake on ppc64le

* Wed Jul 26 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-4
- avoid build failure caused broken RPM code that produces debuginfo packages

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.54.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jun 19 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-2
- enforce versioned openssl-libs dependency for libcurl (#1462184)

* Wed Jun 14 2017 Kamil Dudka <kdudka@redhat.com> 7.54.1-1
- new upstream release

* Tue May 16 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-5
- add *-full provides for curl and libcurl to make them explicitly installable

* Thu May 04 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-4
- make curl-minimal require a new enough version of libcurl

* Thu Apr 27 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-3
- switch the TLS backend back to OpenSSL (#1445153)

* Tue Apr 25 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-2
- nss: use libnssckbi.so as the default source of trust
- nss: do not leak PKCS #11 slot while loading a key (#1444860)

* Thu Apr 20 2017 Kamil Dudka <kdudka@redhat.com> 7.54.0-1
- new upstream release (fixes CVE-2017-7468)

* Thu Apr 13 2017 Paul Howarth <paul@city-fan.org> 7.53.1-7
- add %%post and %%postun scriptlets for libcurl-minimal
- libcurl-minimal provides both libcurl and libcurl%%{?_isa}
- remove some legacy spec file cruft

* Wed Apr 12 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-6
- provide (lib)curl-minimal subpackages with lightweight build of (lib)curl

* Mon Apr 10 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-5
- disable upstream test 2033 (flaky test for HTTP/1 pipelining)

* Fri Apr 07 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-4
- fix out of bounds read in curl --write-out (CVE-2017-7407)

* Mon Mar 06 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-3
- make the dependency on nss-pem arch-specific (#1428550)

* Thu Mar 02 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-2
- re-enable valgrind on ix86 because sqlite is fixed (#1428286)

* Fri Feb 24 2017 Kamil Dudka <kdudka@redhat.com> 7.53.1-1
- new upstream release

* Wed Feb 22 2017 Kamil Dudka <kdudka@redhat.com> 7.53.0-1
- do not use valgrind on ix86 until sqlite is rebuilt by patched GCC (#1423434)
- new upstream release (fixes CVE-2017-2629)

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.52.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 23 2016 Kamil Dudka <kdudka@redhat.com> 7.52.1-1
- new upstream release (fixes CVE-2016-9586)

* Mon Nov 21 2016 Kamil Dudka <kdudka@redhat.com> 7.51.0-3
- map CURL_SSLVERSION_DEFAULT to NSS default, add support for TLS 1.3 (#1396719)

* Tue Nov 15 2016 Kamil Dudka <kdudka@redhat.com> 7.51.0-2
- stricter host name checking for file:// URLs
- ssh: check md5 fingerprints case insensitively

* Wed Nov 02 2016 Kamil Dudka <kdudka@redhat.com> 7.51.0-1
- temporarily disable failing libidn2 test-cases
- new upstream release, which fixes the following vulnerabilities
    CVE-2016-8615 - Cookie injection for other servers
    CVE-2016-8616 - Case insensitive password comparison
    CVE-2016-8617 - Out-of-bounds write via unchecked multiplication
    CVE-2016-8618 - Double-free in curl_maprintf
    CVE-2016-8619 - Double-free in krb5 code
    CVE-2016-8620 - Glob parser write/read out of bounds
    CVE-2016-8621 - curl_getdate out-of-bounds read
    CVE-2016-8622 - URL unescape heap overflow via integer truncation
    CVE-2016-8623 - Use-after-free via shared cookies
    CVE-2016-8624 - Invalid URL parsing with '#'
    CVE-2016-8625 - IDNA 2003 makes curl use wrong host

* Thu Oct 20 2016 Kamil Dudka <kdudka@redhat.com> 7.50.3-3
- drop 0103-curl-7.50.0-stunnel.patch no longer needed

* Fri Oct 07 2016 Kamil Dudka <kdudka@redhat.com> 7.50.3-2
- use the just built version of libcurl while generating zsh completion

* Wed Sep 14 2016 Kamil Dudka <kdudka@redhat.com> 7.50.3-1
- new upstream release (fixes CVE-2016-7167)

* Wed Sep 07 2016 Kamil Dudka <kdudka@redhat.com> 7.50.2-1
- new upstream release

* Fri Aug 26 2016 Kamil Dudka <kdudka@redhat.com> 7.50.1-2
- work around race condition in PK11_FindSlotByName()
- fix incorrect use of a previously loaded certificate from file
  (related to CVE-2016-5420)

* Wed Aug 03 2016 Kamil Dudka <kdudka@redhat.com> 7.50.1-1
- new upstream release (fixes CVE-2016-5419, CVE-2016-5420, and CVE-2016-5421)

* Tue Jul 26 2016 Kamil Dudka <kdudka@redhat.com> 7.50.0-2
- run HTTP/2 tests on all architectures (#1360319 now worked around in nghttp2)

* Thu Jul 21 2016 Kamil Dudka <kdudka@redhat.com> 7.50.0-1
- run HTTP/2 tests only on Intel for now to work around #1358845
- require nss-pem because it is no longer included in the nss package (#1347336)
- fix HTTPS and FTPS tests (work around stunnel bug #1358810)
- new upstream release

* Fri Jun 17 2016 Kamil Dudka <kdudka@redhat.com> 7.49.1-3
- use multilib-rpm-config to install arch-dependent header files

* Fri Jun 03 2016 Kamil Dudka <kdudka@redhat.com> 7.49.1-2
- fix SIGSEGV of the curl tool while parsing URL with too many globs (#1340757)

* Mon May 30 2016 Kamil Dudka <kdudka@redhat.com> 7.49.1-1
- new upstream release

* Wed May 18 2016 Kamil Dudka <kdudka@redhat.com> 7.49.0-1
- new upstream release

* Wed Mar 23 2016 Kamil Dudka <kdudka@redhat.com> 7.48.0-1
- new upstream release

* Wed Mar 02 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-4
- do not refuse cookies for localhost (#1308791)

* Wed Feb 17 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-3
- make SCP and SFTP test-cases work with up2date OpenSSH

* Wed Feb 10 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-2
- enable support for Public Suffix List (#1305701)

* Mon Feb 08 2016 Kamil Dudka <kdudka@redhat.com> 7.47.1-1
- new upstream release

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.47.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jan 27 2016 Kamil Dudka <kdudka@redhat.com> 7.47.0-1
- new upstream release (fixes CVE-2016-0755)

* Fri Dec  4 2015 Kamil Dudka <kdudka@redhat.com> 7.46.0-2
- own /usr/share/zsh/site-functions instead of requiring zsh (#1288529)

* Wed Dec  2 2015 Kamil Dudka <kdudka@redhat.com> 7.46.0-1
- disable silent builds (suggested by Paul Howarth)
- use default port numbers when running the upstream test-suite
- install zsh completion script
- new upstream release

* Wed Oct  7 2015 Paul Howarth <paul@city-fan.org> 7.45.0-1
- new upstream release
- drop %%defattr, redundant since rpm 4.4

* Fri Sep 18 2015 Kamil Dudka <kdudka@redhat.com> 7.44.0-2
- prevent NSS from incorrectly re-using a session (#1104597)

* Wed Aug 12 2015 Kamil Dudka <kdudka@redhat.com> 7.44.0-1
- new upstream release

* Thu Jul 30 2015 Kamil Dudka <kdudka@redhat.com> 7.43.0-3
- prevent dnf from crashing when using both FTP and HTTP (#1248389)

* Thu Jul 16 2015 Kamil Dudka <kdudka@redhat.com> 7.43.0-2
- build support for the HTTP/2 protocol

* Wed Jun 17 2015 Kamil Dudka <kdudka@redhat.com> 7.43.0-1
- new upstream release (fixes CVE-2015-3236 and CVE-2015-3237)

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.42.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jun 05 2015 Kamil Dudka <kdudka@redhat.com> 7.42.1-2
- curl-config --libs now works on x86_64 without libcurl-devel.x86_64 (#1228363)

* Wed Apr 29 2015 Kamil Dudka <kdudka@redhat.com> 7.42.1-1
- new upstream release (fixes CVE-2015-3153)

* Wed Apr 22 2015 Kamil Dudka <kdudka@redhat.com> 7.42.0-1
- new upstream release (fixes CVE-2015-3143, CVE-2015-3144, CVE-2015-3145,
  and CVE-2015-3148)
- implement public key pinning for NSS backend (#1195771)
- do not run flaky test-cases in %%check

* Wed Feb 25 2015 Kamil Dudka <kdudka@redhat.com> 7.41.0-1
- new upstream release
- include extern-scan.pl to make test1135 succeed (upstream commit 1514b718)

* Mon Feb 23 2015 Kamil Dudka <kdudka@redhat.com> 7.40.0-3
- fix a spurious connect failure on dual-stacked hosts (#1187531)

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 7.40.0-2
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Thu Jan 08 2015 Kamil Dudka <kdudka@redhat.com> 7.40.0-1
- new upstream release (fixes CVE-2014-8150)

* Wed Nov 05 2014 Kamil Dudka <kdudka@redhat.com> 7.39.0-1
- new upstream release (fixes CVE-2014-3707)

* Tue Oct 21 2014 Kamil Dudka <kdudka@redhat.com> 7.38.0-2
- fix a connection failure when FTPS handle is reused

* Wed Sep 10 2014 Kamil Dudka <kdudka@redhat.com> 7.38.0-1
- new upstream release (fixes CVE-2014-3613 and CVE-2014-3620)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.37.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Aug 13 2014 Rex Dieter <rdieter@fedoraproject.org> 7.37.1-2
- include arch'd Requires/Provides

* Wed Jul 16 2014 Kamil Dudka <kdudka@redhat.com> 7.37.1-1
- new upstream release
- fix endless loop with GSSAPI proxy auth (patches by David Woodhouse, #1118751)

* Fri Jul 11 2014 Tom Callaway <spot@fedoraproject.org> 7.37.0-4
- fix license handling

* Fri Jul 04 2014 Kamil Dudka <kdudka@redhat.com> 7.37.0-3
- various SSL-related fixes (mainly crash on connection failure)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed May 21 2014 Kamil Dudka <kdudka@redhat.com> 7.37.0-1
- new upstream release

* Fri May 09 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-4
- auth failure on duplicated 'WWW-Authenticate: Negotiate' header (#1093348)

* Fri Apr 25 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-3
- nss: implement non-blocking SSL handshake

* Wed Apr 02 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-2
- extend URL parser to support IPv6 zone identifiers (#680996)

* Wed Mar 26 2014 Kamil Dudka <kdudka@redhat.com> 7.36.0-1
- new upstream release (fixes CVE-2014-0138)

* Mon Mar 17 2014 Paul Howarth <paul@city-fan.org> 7.35.0-5
- add all perl build requirements for the test suite, in a portable way

* Mon Mar 17 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-4
- add BR for perl-Digest-MD5, which is required by the test-suite

* Wed Mar 05 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-3
- avoid spurious failure of test1086 on s390(x) koji builders (#1072273)

* Tue Feb 25 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-2
- refresh expired cookie in test172 from upstream test-suite (#1068967)

* Wed Jan 29 2014 Kamil Dudka <kdudka@redhat.com> 7.35.0-1
- new upstream release (fixes CVE-2014-0015)

* Wed Dec 18 2013 Kamil Dudka <kdudka@redhat.com> 7.34.0-1
- new upstream release

* Mon Dec 02 2013 Kamil Dudka <kdudka@redhat.com> 7.33.0-2
- allow to use TLS > 1.0 if built against recent NSS

* Mon Oct 14 2013 Kamil Dudka <kdudka@redhat.com> 7.33.0-1
- new upstream release
- fix missing initialization in NTLM code causing test 906 to fail
- fix missing initialization in SSH code causing test 619 to fail

* Fri Oct 11 2013 Kamil Dudka <kdudka@redhat.com> 7.32.0-3
- do not limit the speed of SCP upload on a fast connection

* Mon Sep 09 2013 Kamil Dudka <kdudka@redhat.com> 7.32.0-2
- avoid delay if FTP is aborted in CURLOPT_HEADERFUNCTION callback (#1005686)

* Mon Aug 12 2013 Kamil Dudka <kdudka@redhat.com> 7.32.0-1
- new upstream release
- make sure that NSS is initialized prior to calling PK11_GenerateRandom()

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.31.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 Kamil Dudka <kdudka@redaht.com> 7.31.0-4
- mention all option listed in 'curl --help' in curl.1 man page

* Tue Jul 02 2013 Kamil Dudka <kdudka@redhat.com> 7.31.0-3
- restore the functionality of 'curl -u :'

* Wed Jun 26 2013 Kamil Dudka <kdudka@redhat.com> 7.31.0-2
- build the curl tool with metalink support

* Sat Jun 22 2013 Kamil Dudka <kdudka@redhat.com> 7.31.0-1
- new upstream release (fixes CVE-2013-2174)

* Fri Apr 26 2013 Kamil Dudka <kdudka@redhat.com> 7.30.0-2
- prevent an artificial timeout event due to stale speed-check data (#906031)

* Fri Apr 12 2013 Kamil Dudka <kdudka@redhat.com> 7.30.0-1
- new upstream release (fixes CVE-2013-1944)
- prevent test-suite failure due to using non-default port ranges in tests

* Tue Mar 12 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-4
- do not ignore poll() failures other than EINTR (#919127)
- curl_global_init() now accepts the CURL_GLOBAL_ACK_EINTR flag (#919127)

* Wed Mar 06 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-3
- switch SSL socket into non-blocking mode after handshake
- drop the hide_selinux.c hack no longer needed in %%check

* Fri Feb 22 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-2
- fix a SIGSEGV when closing an unused multi handle (#914411)

* Wed Feb 06 2013 Kamil Dudka <kdudka@redhat.com> 7.29.0-1
- new upstream release (fixes CVE-2013-0249)
