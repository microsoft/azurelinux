# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Fedora spec file for libsodium
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#
%global libname libsodium
%global soname  26

%if 0%{?fedora}
%bcond_without  mingw
%else
%bcond_with     mingw
%endif

Name:           libsodium
Version:        1.0.21
Release: 3%{?dist}
Summary:        The Sodium crypto library
# Most source code is ISC, except:
# BSD-2-Clause:
#   src/libsodium/crypto_hash/sha256/cp/hash_sha256_cp.c
#   src/libsodium/crypto_hash/sha512/cp/hash_sha512_cp.c
#   src/libsodium/crypto_pwhash/scryptsalsa208sha256/crypto_scrypt.h
#   src/libsodium/crypto_pwhash/scryptsalsa208sha256/nosse/pwhash_scryptsalsa208sha256_nosse.c
#   src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.c
#   src/libsodium/crypto_pwhash/scryptsalsa208sha256/pbkdf2-sha256.h
#   src/libsodium/crypto_pwhash/scryptsalsa208sha256/sse/pwhash_scryptsalsa208sha256_sse.c
# CC0-1.0:
#   src/libsodium/crypto_pwhash/argon2/argon2-encoding.c
License:        ISC AND BSD-2-Clause AND CC0-1.0
URL:            https://libsodium.org/

Source0:        https://download.libsodium.org/libsodium/releases/%{name}-%{version}.tar.gz
Source1:        https://download.libsodium.org/libsodium/releases/%{name}-%{version}.tar.gz.sig
# https://doc.libsodium.org/installation#integrity-checking
Source2:        %{name}.pubkey

Patch0:        upstream.patch

BuildRequires: gnupg2
BuildRequires: gcc
BuildRequires: make

%if %{with mingw}
BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc

BuildRequires: mingw64-gcc
BuildRequires: mingw64-filesystem
%endif

# manage update from 3rd party repository
Obsoletes:      %{libname}%{soname} <= %{version}


%description
Sodium is a new, easy-to-use software library for encryption, decryption, 
signatures, password hashing and more. It is a portable, cross-compilable, 
installable, packageable fork of NaCl, with a compatible API, and an extended 
API to improve usability even further. Its goal is to provide all of the core 
operations needed to build higher-level cryptographic tools. The design 
choices emphasize security, and "magic constants" have clear rationales.

The same cannot be said of NIST curves, where the specific origins of certain 
constants are not described by the standards. And despite the emphasis on 
higher security, primitives are faster across-the-board than most 
implementations of the NIST standards.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Obsoletes:      %{libname}%{soname}-devel <= %{version}

%description    devel
This package contains libraries and header files for
developing applications that use %{name} libraries.

%package        static
Summary:        Static library for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Obsoletes:      %{libname}%{soname}-static <= %{version}

%description    static
This package contains the static library for statically
linking applications to use %{name}.

%if %{with mingw}
%package -n     mingw32-%{name}
Summary:        MinGW compiled %{name} library for Win32 target
BuildArch:      noarch

%description -n mingw32-%{name}
This package contains the MinGW compiled library of %{name}
for Win32 target.

%package -n     mingw64-%{name}
Summary:        MinGW compiled %{name} library for Win64 target
BuildArch:      noarch

%description -n mingw64-%{name}
This package contains the MinGW compiled library of %{name}
for Win64 target.

%{?mingw_debug_package}
%endif


%prep
%{?gpgverify:%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'}

%setup -q
%patch -P0 -p1 -b.upstream


%build
# This package has a configure test which uses ASMs, but does not link the
# resultant .o files.  As such the ASM test is always successful, even on
# architectures were the ASM is not valid when compiling with LTO.
#
# -ffat-lto-objects is sufficient to address this issue.  It is the default
# for F33, but is expected to only be enabled for packages that need it in
# F34, so we use it here explicitly
%define _lto_cflags -flto=auto -ffat-lto-objects

mkdir build_native
pushd build_native
%global _configure ../configure
%configure \
  --disable-silent-rules \
  --disable-opt

%make_build
popd

%if %{with mingw}
%mingw_configure \
  --disable-silent-rules \
  --disable-opt

%mingw_make_build
%endif


%install
%make_install -C build_native

rm %{buildroot}%{_libdir}/%{libname}.la

%if %{with mingw}
%mingw_make_install
rm %{buildroot}%{mingw32_libdir}/libsodium.a
rm %{buildroot}%{mingw64_libdir}/libsodium.a
%mingw_debug_install_post
%endif


%check
make -C build_native check


%files
%license LICENSE
%{_libdir}/%{libname}.so.%{soname}*

%files devel
%doc AUTHORS ChangeLog README.markdown THANKS
%doc test/default/*.{c,exp,h}
%doc test/quirks/quirks.h
%{_includedir}/sodium.h
%{_includedir}/sodium/
%{_libdir}/%{libname}.so
%{_libdir}/pkgconfig/%{libname}.pc

%files static
%{_libdir}/libsodium.a

%if %{with mingw}
%files -n mingw32-%{name}
%license LICENSE
%{mingw32_bindir}/*.{dll,def}
%{mingw32_includedir}/sodium.h
%{mingw32_includedir}/sodium/
%{mingw32_libdir}/pkgconfig/libsodium.pc
%{mingw32_libdir}/libsodium.dll.a

%files -n mingw64-%{name}
%license LICENSE
%{mingw64_bindir}/*.{dll,def}
%{mingw64_includedir}/sodium.h
%{mingw64_includedir}/sodium/
%{mingw64_libdir}/pkgconfig/libsodium.pc
%{mingw64_libdir}/libsodium.dll.a
%endif


%changelog
* Wed Jan  7 2026 Remi Collet <remi@remirepo.net> - 1.0.21-2
- fix aarch64 build failure using upstream patch

* Wed Jan  7 2026 Remi Collet <remi@remirepo.net> - 1.0.21-1
- update to 1.0.21
- open https://github.com/jedisct1/libsodium/discussions/1503 build failure on aarch64
- workaround build failure using -flax-vector-conversions on aarch64

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Mar 30 2025 Carl George <carlwgeorge@fedoraproject.org> - 1.0.20-5
- Add missing SPDX identifiers to license field

* Mon Jan 20 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon May 27 2024 Remi Collet <remi@remirepo.net> - 1.0.20-1
- update to 1.0.20

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Nov 08 2023 Marian Koncek <mkoncek@redhat.com> - 1.0.19-2
- Make mingw subpackages noarch

* Wed Sep 13 2023 Remi Collet <remi@remirepo.net> - 1.0.19-1
- update to 1.0.19
- soname is 26

* Mon Aug 21 2023 Marian Koncek <mkoncek@redhat.com> - 1.0.18-14
- Add mingw subpackages

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Apr 21 2023 Remi Collet <remi@remirepo.net> - 1.0.18-12
- check archive signature

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Aug 21 2020 Jeff Law <law@redhat.com> - 1.0.18-6
- Re-enable LTO

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Jeff Law <law@redhat.com> - 1.0.18-4
- Disable LTO

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun  3 2019 Remi Collet <remi@remirepo.net> - 1.0.18-1
- update to 1.0.18

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Jan  7 2019 Remi Collet <remi@remirepo.net> - 1.0.17-1
- update to 1.0.17

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Feb 20 2018 Remi Collet <remi@remirepo.net> - 1.0.16-4
- missing BR on C compiler
- drop ldconfig scriptlets

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Dec 13 2017 Remi Collet <remi@remirepo.net> - 1.0.16-1
- update to 1.0.16

* Sun Oct  1 2017 Remi Collet <remi@remirepo.net> - 1.0.15-1
- update to 1.0.15
- soname bump to 23
- manage update from libsodium23 (3rd party repository)

* Fri Sep 22 2017 Remi Collet <remi@remirepo.net> - 1.0.14-1
- update to 1.0.14
- manage update from libsodium-last (3rd party repository)

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Remi Collet <remi@fedoraproject.org> - 1.0.13-1
- update to 1.0.13

* Mon Mar 13 2017 Remi Collet <remi@fedoraproject.org> - 1.0.12-1
- update to 1.0.12

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 12 2016 Neal Gompa <ngompa13@gmail.com> - 1.0.11-2
- Add static library subpackage

* Mon Aug  1 2016 Remi Collet <remi@fedoraproject.org> - 1.0.11-1
- update to 1.0.11

* Tue Apr  5 2016 Remi Collet <remi@fedoraproject.org> - 1.0.10-1
- update to 1.0.10

* Sat Apr  2 2016 Remi Collet <remi@fedoraproject.org> - 1.0.9-1
- update to 1.0.9

* Mon Mar  7 2016 Remi Collet <remi@fedoraproject.org> - 1.0.8-1
- update to 1.0.8
- soname bump to 18
- fix license management

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Sun Oct 25 2015 Christopher Meng <rpm@cicku.me> - 1.0.5-1
- Update to 1.0.5

* Mon Jul 13 2015 Christopher Meng <rpm@cicku.me> - 1.0.3-1
- Update to 1.0.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Jan 23 2015 Christopher Meng <rpm@cicku.me> - 1.0.2-1
- Update to 1.0.2

* Sat Nov 22 2014 Christopher Meng <rpm@cicku.me> - 1.0.1-1
- Update to 1.0.1

* Sat Oct 18 2014 Christopher Meng <rpm@cicku.me> - 1.0.0-1
- Update to 1.0.0

* Sun Aug 24 2014 Christopher Meng <rpm@cicku.me> - 0.7.0-1
- Update to 0.7.0

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 17 2014 Christopher Meng <rpm@cicku.me> - 0.6.1-1
- Update to 0.6.1

* Thu Jul 03 2014 Christopher Meng <rpm@cicku.me> - 0.6.0-1
- Update to 0.6.0

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 16 2014 Christopher Meng <rpm@cicku.me> - 0.5.0-1
- Update to 0.5.0

* Mon Dec 09 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-3
- Disable silent build rules.
- Preserve the timestamp.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-2
- Add doc for devel package.
- Add support for EPEL6.

* Wed Nov 20 2013 Christopher Meng <rpm@cicku.me> - 0.4.5-1
- Update to 0.4.5

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-2
- Drop useless files.
- Improve the description.

* Wed Jul 10 2013 Christopher Meng <rpm@cicku.me> - 0.4.2-1
- Initial Package.
