# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-curl
Version:        8.16.0
Release: 2%{?dist}
Summary:        MinGW Windows port of curl and libcurl

License:        MIT
URL:            https://curl.haxx.se/
Source0:        https://curl.haxx.se/download/curl-%{version}.tar.xz

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-gettext
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-libidn2
BuildRequires:  mingw32-libpsl
BuildRequires:  mingw32-libssh2
BuildRequires:  mingw32-openssl

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-gettext
BuildRequires:  mingw64-win-iconv
BuildRequires:  mingw64-zlib
BuildRequires:  mingw64-libidn2
BuildRequires:  mingw64-libpsl
BuildRequires:  mingw64-libssh2
BuildRequires:  mingw64-openssl


%description
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy
support, user authentication, FTP upload, HTTP post, and file transfer
resume.

This is the MinGW cross-compiled Windows library.


# Win32
%package -n mingw32-curl
Summary:        MinGW Windows port of curl and libcurl
Requires:       pkgconfig

%description -n mingw32-curl
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy
support, user authentication, FTP upload, HTTP post, and file transfer
resume.

This is the MinGW cross-compiled Windows library.

%package -n mingw32-curl-static
Summary:        Static version of the MinGW Windows Curl library
Requires:       mingw32-curl = %{version}-%{release}

%description -n mingw32-curl-static
Static version of the MinGW Windows Curl library.

# Win64
%package -n mingw64-curl
Summary:        MinGW Windows port of curl and libcurl
Requires:       pkgconfig

%description -n mingw64-curl
cURL is a tool for getting files from HTTP, FTP, FILE, LDAP, LDAPS,
DICT, TELNET and TFTP servers, using any of the supported protocols.
cURL is designed to work without user interaction or any kind of
interactivity. cURL offers many useful capabilities, like proxy
support, user authentication, FTP upload, HTTP post, and file transfer
resume.

This is the MinGW cross-compiled Windows library.

%package -n mingw64-curl-static
Summary:        Static version of the MinGW Windows Curl library
Requires:       mingw64-curl = %{version}-%{release}

%description -n mingw64-curl-static
Static version of the MinGW Windows Curl library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n curl-%{version}


%build
MINGW32_CONFIGURE_ARGS="--with-ca-bundle=%{mingw32_sysconfdir}/pki/tls/certs/ca-bundle.crt"
MINGW64_CONFIGURE_ARGS="--with-ca-bundle=%{mingw64_sysconfdir}/pki/tls/certs/ca-bundle.crt"
MINGW_CONFIGURE_ARGS="--with-ssl --enable-ipv6 --enable-threaded-resolver --enable-sspi --with-libidn2 --with-libssh2 --without-random"

MINGW_BUILDDIR_SUFFIX=_static %mingw_configure --enable-static --disable-shared
MINGW_BUILDDIR_SUFFIX=_shared %mingw_configure --disable-static --enable-shared

# It's not clear where to set the --with-ca-bundle path.  This is the
# default for CURLOPT_CAINFO.  If this doesn't exist, you'll get an
# error from all https transfers unless the program sets
# CURLOPT_CAINFO to point to the correct ca-bundle.crt file.

# --without-random disables random number collection (eg. from
# /dev/urandom).  There isn't an obvious alternative for Windows:
# Perhaps we can port EGD or use a library such as Yarrow.

# These are the original flags that we'll work towards as
# more of the dependencies get ported to Fedora MinGW.
#
#  --without-ssl --with-nss=%{mingw32_prefix} --enable-ipv6
#  --with-ca-bundle=%{mingw32_sysconfdir}/pki/tls/certs/ca-bundle.crt
#  --with-gssapi=%{mingw32_prefix}/kerberos --with-libidn
#  --enable-ldaps --disable-static --with-libssh2

MINGW_BUILDDIR_SUFFIX=_static %mingw_make_build
MINGW_BUILDDIR_SUFFIX=_shared %mingw_make_build


%install
MINGW_BUILDDIR_SUFFIX=_static %mingw_make DESTDIR=%{buildroot}/static install
MINGW_BUILDDIR_SUFFIX=_shared %mingw_make_install

# The curl-config script is hard coded to the build type. Keep a static copy.
mv %{buildroot}/static%{mingw32_bindir}/curl-config %{buildroot}%{mingw32_bindir}/curl-config-static
mv %{buildroot}/static%{mingw64_bindir}/curl-config %{buildroot}%{mingw64_bindir}/curl-config-static
# The static library from the static build is the only one of interest to us
mv %{buildroot}/static%{mingw32_libdir}/libcurl.a %{buildroot}%{mingw32_libdir}/libcurl.a
mv %{buildroot}/static%{mingw64_libdir}/libcurl.a %{buildroot}%{mingw64_libdir}/libcurl.a
rm -rf %{buildroot}/static

# Remove .la files
find %{buildroot} -name "*.la" -delete

# Remove the man pages which duplicate documentation in the
# native Fedora package.
rm -r %{buildroot}%{mingw32_mandir}/man{1,3}
rm -r %{buildroot}%{mingw64_mandir}/man{1,3}

# Remove redundant autoconf files
rm -rf %{buildroot}%{mingw32_datadir}/aclocal
rm -rf %{buildroot}%{mingw64_datadir}/aclocal

# sh wrapper not useful on windows
rm -f %{buildroot}%{mingw32_bindir}/wcurl
rm -f %{buildroot}%{mingw64_bindir}/wcurl


# Win32
%files -n mingw32-curl
%license COPYING
%{mingw32_bindir}/curl.exe
%{mingw32_bindir}/curl-config
%{mingw32_bindir}/libcurl-4.dll
%{mingw32_libdir}/libcurl.dll.a
%{mingw32_libdir}/pkgconfig/libcurl.pc
%{mingw32_includedir}/curl/

%files -n mingw32-curl-static
%{mingw32_bindir}/curl-config-static
%{mingw32_libdir}/libcurl.a

# Win64
%files -n mingw64-curl
%license COPYING
%{mingw64_bindir}/curl.exe
%{mingw64_bindir}/curl-config
%{mingw64_bindir}/libcurl-4.dll
%{mingw64_libdir}/libcurl.dll.a
%{mingw64_libdir}/pkgconfig/libcurl.pc
%{mingw64_includedir}/curl/

%files -n mingw64-curl-static
%{mingw64_bindir}/curl-config-static
%{mingw64_libdir}/libcurl.a


%changelog
* Sun Sep 14 2025 Sandro Mani <manisandro@gmail.com> - 8.16.0-1
- Update to 8.16.0

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jul 18 2025 Sandro Mani <manisandro@gmail.com> - 8.15.0-1
- Update to 8.15.0

* Sat Jun 07 2025 Sandro Mani <manisandro@gmail.com> - 8.14.1-1
- Update to 8.14.1

* Thu May 29 2025 Sandro Mani <manisandro@gmail.com> - 8.14.0-1
- Update to 8.14.0

* Wed Apr 02 2025 Sandro Mani <manisandro@gmail.com> - 8.13.0-1
- Update to 8.13.0

* Sat Feb 15 2025 Sandro Mani <manisandro@gmail.com> - 8.12.1-1
- Update to 8.12.1

* Fri Feb 07 2025 Sandro Mani <manisandro@gmail.com> - 8.12.0-1
- Update to 8.12.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 8.11.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Dec 13 2024 Sandro Mani <manisandro@gmail.com> - 8.11.1-1
- Update to 8.11.1

* Sat Nov 09 2024 Sandro Mani <manisandro@gmail.com> - 8.11.0-1
- Update to 8.11.0

* Thu Sep 19 2024 Sandro Mani <manisandro@gmail.com> - 8.10.1-1
- Update to 8.10.1

* Thu Sep 12 2024 Sandro Mani <manisandro@gmail.com> - 8.10.0-1
- Update to 8.10.0

* Thu Aug 01 2024 Sandro Mani <manisandro@gmail.com> - 8.9.1-1
- Update to 8.9.1

* Thu Jul 25 2024 Sandro Mani <manisandro@gmail.com> - 8.9.0-1
- Update to 8.9.0

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed May 22 2024 Sandro Mani <manisandro@gmail.com> - 8.8.0-1
- Update to 8.8.0

* Thu Apr 04 2024 Sandro Mani <manisandro@gmail.com> - 8.7.1-1
- Update to 8.7.1

* Fri Feb 02 2024 Sandro Mani <manisandro@gmail.com> - 8.6.0-1
- Update to 8.6.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 8.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Sandro Mani <manisandro@gmail.com> - 8.5.0-1
- Update to 8.5.0

* Sat Oct 14 2023 Sandro Mani <manisandro@gmail.com> - 8.4.0-1
- Update to 8.4.0

* Mon Sep 18 2023 Sandro Mani <manisandro@gmail.com> - 8.3.0-1
- Update to 8.3.0

* Sat Jul 29 2023 Sandro Mani <manisandro@gmail.com> - 8.2.1-1
- Update to 8.2.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 8.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue May 30 2023 Sandro Mani <manisandro@gmail.com> - 8.1.2-1
- Update to 8.1.2

* Tue May 23 2023 Sandro Mani <manisandro@gmail.com> - 8.1.1-1
- Update to 8.1.1

* Fri May 19 2023 Sandro Mani <manisandro@gmail.com> - 8.1.0-1
- Update to 8.1.0

* Mon Mar 20 2023 Sandro Mani <manisandro@gmail.com> - 8.0.1-1
- Update to 8.0.1

* Tue Feb 21 2023 Sandro Mani <manisandro@gmail.com> - 7.88.1-1
- Update to 7.88.1

* Wed Feb 15 2023 Sandro Mani <manisandro@gmail.com> - 7.88.0-1
- Update to 7.88.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 7.87.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Dec 21 2022 Sandro Mani <manisandro@gmail.com> - 7.87.0-1
- Update to 7.87.0

* Sun Oct 30 2022 Sandro Mani <manisandro@gmail.com> - 7.86.0-1
- Update to 7.86.0

* Sun Sep 04 2022 Sandro Mani <manisandro@gmail.com> - 7.85.0-1
- Update to 7.85.0

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.84.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 30 2022 Sandro Mani <manisandro@gmail.com> - 7.84.0-1
- Update to 7.84.0

* Fri May 20 2022 Sandro Mani <manisandro@gmail.com> - 7.83.1-1
- Update to 7.83.1

* Wed Apr 27 2022 Sandro Mani <manisandro@gmail.com> - 7.83.0-1
- Update to 7.83.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 7.82.0-3
- Rebuild with mingw-gcc-12

* Fri Mar 11 2022 Michael Cronenworth <mike@cchtml.com> - 7.82.0-2
- Keep a separate static curl-config (RHBZ#1946299)

* Sat Mar 05 2022 Sandro Mani <manisandro@gmail.com> - 7.82.0-1
- Update to 7.82.0

* Thu Feb 17 2022 Sandro Mani <manisandro@gmail.com> - 7.81.0-3
- Rebuild (openssl)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 7.81.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jan 05 2022 Sandro Mani <manisandro@gmail.com> - 7.81.0-1
- Update to 7.81.0

* Wed Nov 10 2021 Sandro Mani <manisandro@gmail.com> - 7.80.0-1
- Update to 7.80.0

* Wed Sep 22 2021 Sandro Mani <manisandro@gmail.com> - 7.79.1-1
- Update to 7.79.1

* Tue Sep 21 2021 Sandro Mani <manisandro@gmail.com> - 7.79.0-1
- Update to 7.79.0

* Wed Jul 21 2021 Sandro Mani <manisandro@gmail.com> - 7.78.0-1
- Update to 7.78.0

* Wed May 26 2021 Sandro Mani <manisandro@gmail.com> - 7.77.0-1
- Update to 7.77.0

* Fri Apr 16 2021 Sandro Mani <manisandro@gmail.com> - 7.76.1-1
- Update to 7.76.1

* Wed Mar 31 2021 Sandro Mani <manisandro@gmail.com> - 7.76.0-1
- Update to 7.76.0

* Thu Feb 04 2021 Sandro Mani <manisandro@gmail.com> - 7.75.0-1
- Update to 7.75.0

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 7.74.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Thu Dec 10 2020 Sandro Mani <manisandro@gmail.com> - 7.74.0-1
- Update to 7.74.0

* Tue Nov 17 2020 Sandro Mani <manisandro@gmail.com> - 7.73.0-1
- Update to 7.73.0

* Mon Sep 21 2020 Sandro Mani <manisandro@gmail.com> - 7.71.1-3
- Backport fix for NTLM proxy regression

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.71.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Jul 24 2020 Michael Cronenworth <mike@cchtml.com> - 7.71.1-1
- Update to 7.71.1, which fixes the following vulnerabilities
  CVE-2020-8169 - curl: Partial password leak over DNS on HTTP redirect
  CVE-2020-8177 - curl: overwrite local file with -J

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.65.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 7.65.3-2
- Rebuild (Changes/Mingw32GccDwarf2)

* Tue Aug 13 2019 Fabiano Fidêncio <fidencio@redhat.com> - 7.65.3-1
- Update the sources accordingly to its native counter part, rhb#z1740787

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.61.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 7.61.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Aug 24 2018 Richard W.M. Jones <rjones@redhat.com> - 7.61.0-2
- Rebuild for new mingw-openssl.

* Wed Jul 18 2018 Michael Cronenworth <mike@cchtml.com> - 7.61.0-1
- Update to 7.61.0
- Fix IDN support and debug symbols, enable SSPI support, ship user binary

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.57.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 7.57.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Dec 21 2017 Michael Cronenworth <mike@cchtml.com> - 7.57.0-1
- Update to 7.57.0
- Fixes:
    CVE-2017-8816 - curl: NTLM buffer overflow via integer overflow
    CVE-2017-8817 - curl: FTP wildcard out of bounds read
    CVE-2017-8818 - curl: SSL out of buffer access

* Mon Oct 23 2017 Michael Cronenworth <mike@cchtml.com> - 7.56.1-1
- Update to 7.56.1
- Fixes CVE-2017-1000257 CVE-2017-1000254 CVE-2017-1000099 CVE-2017-1000100
  CVE-2017-1000101

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.54.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jun 14 2017 Michael Cronenworth <mike@cchtml.com> - 7.54.1-1
- Update to 7.54.1

* Sun Jun 04 2017 Michael Cronenworth <mike@cchtml.com> - 7.54.0-1
- Update to 7.54.0

* Fri Mar 03 2017 Michael Cronenworth <mike@cchtml.com> - 7.53.1-1
- Update to 7.53.1

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 7.52.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 09 2017 Michael Cronenworth <mike@cchtml.com> - 7.52.1-1
- Update to 7.52.1
- Fixes for varies CVE's
  CVE-2016-8615 CVE-2016-8616 CVE-2016-8617 CVE-2016-8618 CVE-2016-8619
  CVE-2016-8620 CVE-2016-8621 CVE-2016-8622 CVE-2016-8623 CVE-2016-8624
  CVE-2016-8625 CVE-2016-9586 CVE-2016-7141 CVE-2016-7167

* Sat Feb  6 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.47.0-1
- Update to 7.47.0
- Fixes various CVE's (RHBZ #1217345, #1302264, #1302266)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.42.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.42.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.42.0-1
- Update to 7.42.0
- Fixes CVE-2015-3143, CVE-2015-3144, CVE-2015-3145, CVE-2015-3148 (RHBZ #1214795 #1214796)
- Fixes CVE-2014-8150 (RHBZ #1180063 #1180064)

* Tue Dec 23 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.39.0-1
- Update to 7.39.0
- Fixes CVE-2014-3707 (RHBZ #1160724)
- Fixes CVE-2014-3620 CVE-2014-3613 (RHBZ #1140037)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.37.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.37.0-1
- Update to 7.37.0
- Fixes CVE-2014-0138 and CVE-2014-0139 (RHBZ #1080880)

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.33.0-1
- Update to 7.33.0
- Fixes CVE-2013-4545, RHBZ #1031429

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.32.0-1
- Update to 7.32.0

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.31.0-1
- Update to 7.31.0

* Sun Mar 24 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.29.0-1
- Update to 7.29.0

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.28.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.28.1-1
- Update to 7.28.1
- Removed all patches as they're not needed for the mingw target

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Apr 08 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.25.0-1
- Update to 7.25.0
- Added win64 support (contributed by Marc-Andre Lureau)
- Dropped upstreamed patches
- Dropped unneeded RPM tags

* Fri Mar 09 2012 Kalev Lember <kalevlember@gmail.com> - 7.20.1-7
- Remove .la files

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.20.1-6
- Renamed the source package to mingw-curl (RHBZ #800375)
- Use mingw macros without leading underscore
- Dropped unneeded RPM tags

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.20.1-5
- Rebuild against the mingw-w64 toolchain
- Let curl use its own errno/WSA error codes
- The function ftruncate64 doesn't need to be reimplemented by curl
  as the mingw-w64 crt already contains an implementation for it

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.20.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 06 2011 Kalev Lember <kalevlember@gmail.com> - 7.20.1-3
- Rebuilt against win-iconv

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.20.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu May 13 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.20.1-1
- Update to 7.20.1
- Merged the patches of the native .spec file (7.20.1-5)
- Dropped the curl.exe
- Use the Win32 threads API instead of mingw32-pthreads
- Dropped BR: pkgconfig

* Fri Dec 11 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.19.7-1
- Update to 7.19.8
- Merged the patches of the native .spec file (7.19.7-8)
- Use %%global instead of %%define
- Automatically generate debuginfo subpackage

* Sat May  9 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.19.4-2
- Merged the patches of the native .spec file (7.19.4-10)

* Fri Apr  3 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 7.19.4-1
- Update to version 7.19.4
- Fixed %%defattr line
- Added -static subpackage. Applications which want to use this
  static library need to add -DCURL_STATICLIB to the CFLAGS
- Merged the patches of the native .spec file (7.19.4-5)

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-6
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-5
- Include license.

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-4
- Rebuild against new OpenSSH (because of soname bump).

* Fri Jan 30 2009 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-3
- Requires pkgconfig.

* Thu Nov 13 2008 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-2
- Requires mingw32-filesystem >= 35.

* Thu Nov 13 2008 Richard W.M. Jones <rjones@redhat.com> - 7.18.2-1
- Initial RPM release.
