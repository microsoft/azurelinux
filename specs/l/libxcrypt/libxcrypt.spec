# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# Build with new api?
%if 0%{?fedora} || 0%{?rhel} > 8
%bcond_without new_api
%else
%bcond_with    new_api
%endif


# Build the compat package?
%if 0%{?fedora} >= 999 || (0%{?rhel} >= 11 && !0%{?eln}) || %{without new_api}
%bcond_with    compat_pkg
%else
%bcond_without compat_pkg
%endif


# Replace obsolete functions with a stub?
%if %{with new_api} && %{with compat_pkg}
%bcond_without enosys_stubs
%else
%bcond_with    enosys_stubs
%endif


# Build the static library?
%bcond_without staticlib


# When we are bootstrapping, we omit the
# verification of the source tarball with GnuPG.
%bcond_with    bootstrap


# Shared object version of libcrypt.
%if %{with new_api}
%global soc  2
%global sol  0
%global sof  0
%global sov  %{soc}.%{sol}.%{sof}
%else
%global soc  1
%global sol  1
%global sof  0
%global sov  %{soc}.%{sol}.%{sof}
%endif

%if %{with compat_pkg}
%global csoc 1
%global csol 1
%global csof 0
%global csov %{csoc}.%{csol}.%{csof}
%endif


# First version of glibc built without libcrypt.
%global glibc_minver     2.28


# Minimum version of Perl needed for some build-scripts.
%global perl_minver      5.14


# The libxcrypt-devel package conflicts with out-dated manuals
# shipped with the man-pages packages *before* this EVR.
%global man_pages_minver 4.15-3


# Need versioned requires on glibc and man-pages?
%if !(0%{?fedora} || 0%{?rhel} > 9)
%global trans_pkg        1
%endif


# Hash methods and API supported by libcrypt.
# NEVER EVER touch this, if you do NOT know what you are doing!
%global hash_methods   all

%if %{with new_api}
%global obsolete_api   no
%else
%global obsolete_api   glibc
%endif

%if %{with compat_pkg}
%global compat_methods all
%global compat_api     glibc
%endif


# Do we replace the obsolete API functions with stubs?
%if %{with enosys_stubs}
%global enosys_stubs   yes
%else
%global enosys_stubs   no
%endif


# Needed for the distribution README file.
%if 0%{?fedora}
%global distname .fedora
%else
%if 0%{?rhel}
%global distname .rhel
%else
%global distname .distribution
%endif
%endif


# Needed for out-of-tree builds.
%global _configure "$(realpath ../configure)"


# Create config.cache to speedup the run of
# the configure script for the compat package.
%global nvrt_str %{name}-%{version}-%{release}.%{_target_cpu}
%global mktemplate %{nvrt_str}-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
%global config_cache %(mktemp -tu %{mktemplate}-config.cache)


# Common configure options.
%global common_configure_options           \\\
  --cache-file=%{config_cache}             \\\
  --disable-failure-tokens                 \\\
  --disable-silent-rules                   \\\
  --enable-shared                          \\\
%if %{with staticlib}                      \
  --enable-static                          \\\
%else                                      \
  --disable-static                         \\\
%endif                                     \
  --disable-valgrind                       \\\
  --srcdir=$(realpath ..)                  \\\
  --with-pkgconfigdir=%{_libdir}/pkgconfig


# Macros for shorthand.
%global _fipsdir %{_libdir}/fipscheck


# Add generation of HMAC checksums of the final stripped
# binaries.  %%define with lazy globbing is used here
# intentionally, because using %%global does not work.
%define __spec_install_post                 \
%{?__debug_package:%{__debug_install_post}} \
%{__arch_install_post}                      \
%{__os_install_post}                        \
libdir="%{buildroot}%{_libdir}"             \
fipsdir="$libdir/fipscheck"                 \
mkdir -p $fipsdir                           \
fipshmac -d $fipsdir                        \\\
  $libdir/libcrypt.so.%{sov}                \
ln -s libcrypt.so.%{sov}.hmac               \\\
  $fipsdir/libcrypt.so.%{soc}.hmac          \
if [[ %{with staticlib} == 1 ]]; then       \
  fipshmac -d $fipsdir                      \\\
    $libdir/libcrypt.a                      \
  if [[ %{without new_api} == 1 ]]; then    \
    ln -s .libcrypt.a.hmac                  \\\
      $fipsdir/libxcrypt.a.hmac             \
  fi                                        \
fi                                          \
if [[ %{with compat_pkg} == 1 ]]; then      \
  fipshmac -d $fipsdir                      \\\
    $libdir/libcrypt.so.%{csov}             \
  ln -s libcrypt.so.%{csov}.hmac            \\\
    $fipsdir/libcrypt.so.%{csoc}.hmac       \
fi                                          \
%{nil}


# Fail linking if there are undefined symbols.
# Required for proper ELF symbol versioning support.
%global _ld_strict_symbol_defs 1


Name:           libxcrypt
Version:        4.5.2
Release:        2%{?dist}
Summary:        Extended crypt library for descrypt, md5crypt, bcrypt, and others

# For explicit license breakdown, see the
# LICENSING file in the source tarball.
License:        LGPL-2.1-or-later AND BSD-3-Clause AND BSD-2-Clause AND BSD-2-Clause-FreeBSD AND 0BSD AND CC0-1.0 AND LicenseRef-Fedora-Public-Domain
URL:            https://github.com/besser82/%{name}
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz.asc
Source2:        %{url}/releases/download/v%{version}/%{name}-gpgkey.asc
Source3:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.xz.sha256sum

# Patch 0000 - 2999: Backported patches from upstream.
Patch0000:      %{url}/commit/174c24d6e87a.patch#/%{name}-%{version}-Werror_discarded-qualifiers.patch
# Patch 3000 - 5999: Backported patches from pull requests.
Patch3000:      %{url}/commit/ba67911314f5.patch#/%{name}-%{version}-Make-crypt-and-crypt_gensalt-use-thread-local-output.patch
# Patch 6000 - 9999: Downstream patches.

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  coreutils
BuildRequires:  fipscheck
BuildRequires:  gcc
%if %{without bootstrap}
BuildRequires:  gnupg2
%endif
%if 0%{?trans_pkg}
BuildRequires:  glibc-devel                  >= %{glibc_minver}
%endif
BuildRequires:  libtool
BuildRequires:  make
BuildRequires:  perl(:VERSION)               >= %{perl_minver}
BuildRequires:  perl(Class::Struct)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(File::Spec::Functions)
BuildRequires:  perl(File::Temp)
BuildRequires:  perl(FindBin)
BuildRequires:  perl(if)
BuildRequires:  perl(IPC::Open3)
BuildRequires:  perl(lib)
BuildRequires:  perl(open)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(utf8)
BuildRequires:  perl(warnings)
BuildRequires:  perl-interpreter

# We do not need to keep this forever.
%if 0%{?trans_pkg}
# Inherited from former libcrypt package.
Obsoletes:      libcrypt-nss           < %{glibc_minver}
Provides:       libcrypt-nss           = %{glibc_minver}
Provides:       libcrypt-nss%{?_isa}   = %{glibc_minver}

# Obsolete former libcrypt properly and provide a virtual libcrypt
# package as it has been done by the former packages, which were
# built by glibc before.
Obsoletes:      libcrypt               < %{glibc_minver}
Provides:       libcrypt               = %{glibc_minver}
Provides:       libcrypt%{?_isa}       = %{glibc_minver}

# Obsolete former libxcrypt-common properly.
Obsoletes:      %{name}-common         < 4.3.3-4
Provides:       %{name}-common         = %{version}-%{release}

# We need a version of glibc, that doesn't build libcrypt anymore.
Requires:       glibc%{?_isa}         >= %{glibc_minver}
%endif

%if %{with new_api} && %{without compat_pkg}
Obsoletes:      %{name}-compat         < %{version}-%{release}
%endif

%if 0%{?fedora}
Recommends:     mkpasswd
%endif

%description
libxcrypt is a modern library for one-way hashing of passwords.
It supports a wide variety of both modern and historical hashing
methods: yescrypt, gost-yescrypt, sm3-yescrypt, scrypt, bcrypt,
sha512crypt, sha256crypt, sm3crypt, md5crypt, SunMD5, sha1crypt,
NT, bsdicrypt, bigcrypt, and descrypt.  It provides the traditional
Unix crypt and crypt_r interfaces, as well as a set of extended
interfaces pioneered by Openwall Linux, crypt_rn, crypt_ra,
crypt_gensalt, crypt_gensalt_rn, and crypt_gensalt_ra.

libxcrypt is intended to be used by login(1), passwd(1), and other
similar programs; that is, to hash a small number of passwords during
an interactive authentication dialogue with a human.  It is not suitable
for use in bulk password-cracking applications, or in any other situation
where speed is more important than careful handling of sensitive data.
However, it is intended to be fast and lightweight enough for use in
servers that must field thousands of login attempts per minute.

%if %{with new_api}
This version of the library does not provide the legacy API functions
that have been provided by glibc's libcrypt.so.1.
%endif


%if %{with compat_pkg}
%package        compat
Summary:        Compatibility library providing legacy API functions

%if %{without bootstrap}
# For testing the glibc compatibility symbols.
BuildRequires:  libxcrypt-compat
%endif

Requires:       %{name}%{?_isa}        = %{version}-%{release}

%description    compat
This package contains the library providing the compatibility API
for applications that are linked against glibc's libxcrypt, or that
are still using the unsafe and deprecated, encrypt, encrypt_r,
setkey, setkey_r, and fcrypt functions, which are still required by
recent versions of POSIX, the Single UNIX Specification, and various
other standards.

All existing binary executables linked against glibc's libcrypt should
work unmodified with the library supplied by this package.
%endif


%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa}        = %{version}-%{release}
Requires:       glibc-devel%{?_isa}
%if 0%{?trans_pkg}
Conflicts:      man-pages              < %{man_pages_minver}
Requires:       glibc-devel%{?_isa}   >= %{glibc_minver}
%endif

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%if %{with staticlib}
%package        static
Summary:        Static library for -static linking with %{name}

Requires:       %{name}-devel%{?_isa}  = %{version}-%{release}
Requires:       glibc-static%{?_isa}
%if 0%{?trans_pkg}
Requires:       glibc-static%{?_isa}  >= %{glibc_minver}
%endif

%description    static
This package contains the libxcrypt static library for -static
linking.

You don't need this, unless you link statically, which is highly
discouraged.
%endif


%prep
%if %{without bootstrap}
# Omitted during bootstrap.
%{gpgverify} --keyring=%{SOURCE2} --signature=%{SOURCE1} --data=%{SOURCE0}
pushd %{_sourcedir}
sha256sum -c %{SOURCE3}
popd
%endif

%autosetup -p 1

# Regen Autotools.
autoreconf -fiv -Wall,error

%if %{with new_api}
cat << EOF >> README%{distname}
This version of the %{name} package ships the libcrypt.so.2
library and does not provide the legacy API functions that have
been provided by glibc's libcrypt.so.1.  The removed functions
by name are encrypt, encrypt_r, setkey, setkey_r, and fcrypt.
%if %{with compat_pkg}

If you are using a third-party application that links against
those functions, or that is linked against glibc's libcrypt,
you may need to install the %{name}-compat package manually.

All existing binary executables linked against glibc's libcrypt
should work unmodified with the libcrypt.so.1 library supplied
by the %{name}-compat package.
%endif
EOF
%endif

%if %{with enosys_stubs}
cat << EOF >> README.posix
This version of the libcrypt.so.1 library has entirely removed
the functionality of the encrypt, encrypt_r, setkey, and setkey_r
functions, while keeping fully binary compatibility with existing
(third-party) applications possibly still using those funtions.
If such an application attemps to call one of these functions, the
corresponding function will indicate that it is not supported by
the system in a POSIX-compliant way.

For security reasons, the encrypt and encrypt_r functions will
also overwrite their data-block argument with random bits.

All existing binary executables linked against glibc's libcrypt
should work unmodified with the provided version of the
libcrypt.so.1 library in place.
EOF
%endif

%if %{with staticlib}
cat << EOF >> README.static
Applications that use certain legacy APIs supplied by glibc’s
libcrypt (encrypt, encrypt_r, setkey, setkey_r, and fcrypt)
cannot be compiled nor linked against the supplied build of
the object files provided in the static library libcrypt.a.
EOF
%endif


%build
touch %{config_cache}
mkdir -p %{_vpath_builddir}

# Build the default system library.
pushd %{_vpath_builddir}
%configure                                       \
  %{common_configure_options}                    \
  --enable-hashes=%{hash_methods}                \
  --enable-obsolete-api=%{obsolete_api}          \
%if %{with new_api}
  --enable-obsolete-api-enosys=%{obsolete_api}
%else
  --enable-obsolete-api-enosys=%{enosys_stubs}
%endif
%make_build
popd

%if %{with compat_pkg}
mkdir -p %{_vpath_builddir}-compat

# Build the compatibility library.
pushd %{_vpath_builddir}-compat
%configure                                       \
  %{common_configure_options}                    \
  --enable-hashes=%{compat_methods}              \
  --enable-obsolete-api=%{compat_api}            \
  --enable-obsolete-api-enosys=%{enosys_stubs}
%make_build
popd
%endif
rm -f %{config_cache}


%install
%if %{with compat_pkg}
# Install the compatibility library.
%make_install -C %{_vpath_builddir}-compat

# Cleanup everything we do not need from the compatibility library.
find %{buildroot}                                               \
  -not -type d -not -name 'libcrypt.so.%{csoc}*' -delete -print
%endif

# Install the default system library.
%make_install -C %{_vpath_builddir}

# Get rid of libtool crap.
find %{buildroot} -name '*.la' -delete -print

# Install documentation to shared %%_pkgdocdir.
install -Dpm 0644 -t %{buildroot}%{_pkgdocdir} \
  ChangeLog NEWS README* THANKS TODO

# Drop README.md as it is identical to README.
rm -f %{buildroot}%{_pkgdocdir}/README.md


%check
build_dirs="%{_vpath_builddir}"
%if %{with compat_pkg}
build_dirs="${build_dirs} %{_vpath_builddir}-compat"
%endif
for dir in ${build_dirs}; do
  %make_build -C ${dir} check || \
    {
      rc=$?;
      echo "-----BEGIN TESTLOG: ${dir}-----";
      cat ${dir}/test-suite.log;
      echo "-----END TESTLOG: ${dir}-----";
      exit $rc;
    }
done


%ldconfig_scriptlets
%if %{with compat_pkg}
%ldconfig_scriptlets compat
%endif


%files
%dir %{_fipsdir}
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/NEWS
%doc %{_pkgdocdir}/README
%if %{with new_api}
%doc %{_pkgdocdir}/README%{distname}
%endif
%if %{with enosys_stubs} && %{without compat_pkg}
%doc %{_pkgdocdir}/README.posix
%endif
%doc %{_pkgdocdir}/THANKS
%license AUTHORS COPYING.LIB LICENSING
%{_fipsdir}/libcrypt.so.%{soc}.hmac
%{_fipsdir}/libcrypt.so.%{sov}.hmac
%{_libdir}/libcrypt.so.%{soc}
%{_libdir}/libcrypt.so.%{sov}
%{_mandir}/man5/crypt.5*


%if %{with compat_pkg}
%files          compat
%dir %{_fipsdir}
%if %{with enosys_stubs}
%doc %{_pkgdocdir}/README.posix
%endif
%{_fipsdir}/libcrypt.so.%{csoc}.hmac
%{_fipsdir}/libcrypt.so.%{csov}.hmac
%{_libdir}/libcrypt.so.%{csoc}
%{_libdir}/libcrypt.so.%{csov}
%endif


%files          devel
%doc %{_pkgdocdir}/ChangeLog
%doc %{_pkgdocdir}/TODO
%{_libdir}/libcrypt.so
%if %{without new_api}
%{_libdir}/libxcrypt.so
%endif
%{_includedir}/crypt.h
%if %{without new_api}
%{_includedir}/xcrypt.h
%endif
%{_libdir}/pkgconfig/libcrypt.pc
%{_libdir}/pkgconfig/%{name}.pc
%{_mandir}/man3/crypt.3*
%{_mandir}/man3/crypt_r.3*
%{_mandir}/man3/crypt_ra.3*
%{_mandir}/man3/crypt_rn.3*
%{_mandir}/man3/crypt_checksalt.3*
%{_mandir}/man3/crypt_gensalt.3*
%{_mandir}/man3/crypt_gensalt_ra.3*
%{_mandir}/man3/crypt_gensalt_rn.3*
%{_mandir}/man3/crypt_preferred_method.3*


%if %{with staticlib}
%files          static
%dir %{_fipsdir}
%doc %{_pkgdocdir}/README.static
%{_fipsdir}/libcrypt.a.hmac
%if %{without new_api}
%{_fipsdir}/libxcrypt.a.hmac
%endif
%{_libdir}/libcrypt.a
%if %{without new_api}
%{_libdir}/libxcrypt.a
%endif
%endif


%changelog
* Wed Dec 10 2025 Björn Esser <besser82@fedoraproject.org> - 4.5.2-2
- Add upstream patch to fix FTBFS

* Mon Nov 10 2025 Björn Esser <besser82@fedoraproject.org> - 4.5.2-1
- New upstream release

* Fri Nov 07 2025 Björn Esser <besser82@fedoraproject.org> - 4.5.1-1
- New upstream release

* Tue Nov 04 2025 Björn Esser <besser82@fedoraproject.org> - 4.5.0-1
- New upstream release

* Sun Nov 02 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.38-10
- Consolidate upstream patches for sm3crypt
- Add patch fixing strcpy_or_abort with NDEBUG builds

* Fri Sep 19 2025 Yaakov Selkowitz <yselkowi@redhat.com> - 4.4.38-9
- Re-enable compat package for ELN

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.38-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Apr 04 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.38-7
- Add patch fixing manpage syntax

* Fri Feb 14 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.38-6
- Backport upstream patches to add sm3{,-yescrypt} backend and tests

* Thu Feb 13 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.38-5
- Use config.cache to speedup the build process of the compat package

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.38-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jan 16 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.38-3
- Synchronize upstream patches
- Add upstream patch to utilize C23 memset_explicit, if available

* Wed Jan 15 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.38-2
- Add patch for proper initialization and cleanup in some crypt functions

* Tue Jan 14 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.38-1
- New upstream release

* Sun Jan 12 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.37-6
- Drop all_possible_tests configuration
- Build test-programs during %%check stage

* Sun Jan 12 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.37-5
- Backport upstream patch to fix testsuite with upcoming GCC-15

* Sun Jan 05 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.37-4
- Update patch for MT-Safeness in crypt and crypt_gensalt

* Sat Jan 04 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.37-3
- Update patch for MT-Safeness in crypt and crypt_gensalt

* Fri Jan 03 2025 Björn Esser <besser82@fedoraproject.org> - 4.4.37-2
- Backport upstream patch to fix build with upcoming GCC-15
- Update patch for MT-Safeness in crypt and crypt_gensalt

* Mon Dec 30 2024 Björn Esser <besser82@fedoraproject.org> - 4.4.37-1
- New upstream release

* Fri Dec 20 2024 Björn Esser <besser82@fedoraproject.org> - 4.4.36-12
- Update patch for MT-Safeness in crypt and crypt_gensalt
- Apply small upstream patch for testsuite

* Wed Nov 27 2024 Björn Esser <besser82@fedoraproject.org> - 4.4.36-11
- Drop -Wl,--no-tls-get-addr-optimize, as binutils are fixed now
- Update patch for MT-Safeness in crypt and crypt_gensalt

* Fri Nov 08 2024 Björn Esser <besser82@fedoraproject.org> - 4.4.36-10
- Build with -Wl,--no-tls-get-addr-optimize on ppc64(le)
- Remove cludge from patch for MT-Safeness in crypt and crypt_gensalt

* Thu Nov 07 2024 Björn Esser <besser82@fedoraproject.org> - 4.4.36-9
- Update patch for MT-Safeness in crypt and crypt_gensalt

* Mon Nov 04 2024 Björn Esser <besser82@fedoraproject.org> - 4.4.36-8
- Add some upstream patches mostly fixing manpages
- Add patch to use TLS to make crypt and crypt_gensalt functions MT-Safe

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.36-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.36-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.36-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Dec 19 2023 Stanislav Zidek <szidek@redhat.com> - 4.4.36-4
- Remove -compat package from Fedora ELN / RHEL 10

* Tue Dec 19 2023 Florian Weimer <fweimer@redhat.com> - 4.4.36-3
- Fix C compatibility issue in the configure script

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.36-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jul 05 2023 Björn Esser <besser82@fedoraproject.org> - 4.4.36-1
- New upstream release

* Tue Jun 06 2023 Björn Esser <besser82@fedoraproject.org> - 4.4.35-1
- New upstream release

* Wed May 31 2023 Björn Esser <besser82@fedoraproject.org> - 4.4.34-1
- New upstream release

* Sat Jan 21 2023 Björn Esser <besser82@fedoraproject.org> - 4.4.33-7
- Run autoreconf during %%prep

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Dec 19 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.33-5
- Simplify transitional Requires and Obsoletes for legacy packages
- Drop versioned BR on perl-interpreter
- Fix README.posix file, as the fcrypt function is still available

* Tue Dec 13 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.33-4
- Add upstream patch to improve performance on SHA512 computation

* Mon Nov 28 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.33-3
- Convert License to SPDX expression
- Add upstream patch to improve performance on some type-cast operations

* Mon Nov 21 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.33-2
- Do not BR the compat package during bootstrap
- Use BR: coreutils instead of %%{_bindir}/sha256sum

* Fri Nov 18 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.33-1
- New upstream release

* Fri Nov 18 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.32-1
- New upstream release

* Wed Nov 16 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.31-5
- Add %%{perl_minver} macro and re-add BR on perl(:VERSION)

* Wed Nov 16 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.31-4
- Add BR for perl modules to run the skip-if-exec-format-error script
- Move the BR for minimum Perl version to perl-interpreter

* Tue Nov 15 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.31-3
- Explicitly list all needed build-time Perl modules

* Tue Nov 15 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.31-2
- Narrow down BuildRequires for the minimum needed Perl modules

* Sun Nov 13 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.31-1
- New upstream release

* Tue Nov 08 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.30-3
- Backport another upstream patch for a conversion fix

* Tue Nov 08 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.30-2
- Backport some upstream patches for fixes and optimizations
- Explicitly disable arc4random_buf in all_possible_tests configuration

* Tue Nov 01 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.30-1
- New upstream release

* Mon Oct 31 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.29-1
- New upstream release

* Wed Aug 10 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.28-3
- Rebuilt for arc4random_buf in glibc 2.36 (or later)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue Feb 01 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.28-1
- New upstream release

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Jan 04 2022 Björn Esser <besser82@fedoraproject.org> - 4.4.27-2
- Update Obsoletes, Provides, and Requires to glibc 2.28 (or later),
  as this was the first upstream version of glibc with an option to
  be built without shipping libcrypt
- Fix rhel version in conditional

* Fri Dec 17 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.27-1
- New upstream release

* Tue Sep 21 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.26-4
- Add some more recent distro releases to previous change

* Tue Sep 21 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.26-3
- Limit explicit versioned Requires on glibc to older distro releases

* Sat Sep 18 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.26-2
- Build from signed and verified distribution tarball

* Fri Sep 17 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.26-1
- New upstream release

* Mon Aug 30 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.25-3
- Rebuild (autoconf)

* Mon Aug 16 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.25-2
- Compile test-programs during %%build stage

* Sun Aug 08 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.25-1
- New upstream release

* Wed Aug 04 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.24-1
- New upstream release

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.23-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Jun 20 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.23-1
- New upstream release

* Wed Jun 16 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.22-3
- Add patches to fix issues with type conversion in the DES code

* Sat Jun 05 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.22-2
- Add a patch to fix o_size calculation for gensalt_yescrypt_rn

* Thu May 27 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.22-1
- New upstream release

* Wed May 26 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.21-1
- New upstream release

* Wed May 19 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.20-3
- Run test for glibc compatibility symbols
- Run a build with all possible tests enabled

* Sun May 02 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.20-2
- Add upstream patch to fix a typo in the documentation

* Sat May 01 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.20-1
- New upstream release

* Thu Apr 08 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.19-1
- New upstream release

* Sat Feb 20 2021 Björn Esser <besser82@fedoraproject.org> - 4.4.18-1
- New upstream release
- Add explicit BR: perl-core

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sun Aug 23 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.17-1
- New upstream release

* Sat Aug 15 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.16-7
- Add a patch to add support for LTO builds
- Enable LTO
- Add a patch to fix Wformat-overflow

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.16-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 30 2020 Jeff Law <law@redhat.com> - 4.4.16-5
- Disable LTO

* Fri Jun 19 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.16-4
- Trim %%changelog starting with v4.4.0
- Remove memcheck conditional

* Sat Apr 25 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.16-3
- Explicitly force linking with '-Wl,-z,defs'

* Fri Apr 24 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.16-2
- Move fipscheck hmac checksums to %%{_libdir}/fipscheck

* Sat Apr 04 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.16-1
- New upstream release

* Thu Apr 02 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.15-2
- Move library from %%_lib to %%_libdir

* Wed Feb 26 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.15-1
- New upstream release

* Mon Feb 17 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.14-1
- New upstream release

* Sun Feb 16 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.13-1
- New upstream release

* Tue Feb 11 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.12-3
- Add an upstream patch to fix a typo in the documentation

* Wed Feb 05 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.12-2
- Add two upstream patches to resolve minor bugs

* Thu Jan 30 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.12-1
- New upstream release

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Jan 18 2020 Björn Esser <besser82@fedoraproject.org> - 4.4.11-1
- New upstream release

* Sun Dec 15 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.10-2
- Add two upstream patches to fix build with upcoming GCC-10

* Wed Sep 18 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.10-1
- New upstream release

* Sat Sep 07 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.9-1
- New upstream release (#1750010)

* Sun Sep 01 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.8-1
- New upstream release

* Sat Aug 24 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.7-1
- New upstream release

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Mon Jun 24 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.6-2
- Build all hash methods for the compat package
- Add a patch to fix Wformat in crypt-kat.c

* Sun May 05 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.6-1
- New upstream release

* Sat May 04 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.5-1
- New upstream release (#1706419)
- Add patch to remove an unneeded union keyword
- Add patch to make unalignment test really unaligned

* Fri Mar 15 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.4-2
- Change Recommends: whois-mkpasswd to Fedora 30 and later (#1687870)

* Mon Mar 04 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.4-1
- New upstream release

* Tue Feb 19 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-10
- Fix versioned requirements on glibc

* Tue Feb 19 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-9
- Fix conditional in __spec_install_post

* Tue Feb 19 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-8
- Update Obsoletes, Provides, and Requires to glibc 2.27
- Add Recommends: whois-mkpasswd for Fedora
- Optimize installation of the documentation files
- Fix %%description
- Use an absolute path for the configure script and srcdir

* Tue Feb 19 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-7
- Add patch to fix the output formatting of a test

* Wed Feb 06 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-6
- Always build all supported hash methods
- Drop distcheck at the end of %%check stage

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.4.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Wed Jan 30 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-4
- Add a README.posix file with information about the stub functions
- Add a README.static file with information about the static library

* Wed Jan 30 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-3
- Replace unsafe functions in libxcrypt-compat with stubs (#1670735)

* Thu Jan 24 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-2
- Fix and simplify the conditionals for the compat package
- Add an option to replace unsafe functions in the compat lib with a stub
- Add patch to fix another possible format-overflow

* Thu Jan 24 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.3-1
- New upstream release

* Thu Jan 24 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.2-8
- Optimize file removal for compatibility library

* Mon Jan 21 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.2-7
- Add two upstream patches to fix build with GCC 9

* Mon Jan 21 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.2-6
- Add upstream patch to add proper C++-guards in <xcrypt.h>

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.2-5
- Build the compat package with glibc hashing methods only
- Add an option to disable the compat-package for future use

* Mon Jan 14 2019 Björn Esser <besser82@fedoraproject.org> - 4.4.2-4
- Bump SO-name for Fedora >= 30 and enable compat package (#1666033)
- Add distribution README file
- Update description of the compat package
- Conditionally remove non-built hashing methods from description

* Sun Dec 23 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.2-3
- Remove architecture bits from Recommends

* Sun Dec 23 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.2-2
- Update summary

* Sat Dec 22 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.2-1
- New upstream release

* Thu Dec 06 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.1-1
- New upstream release

* Tue Dec 04 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.0-5
- Sync -fno-plt patch with upstream commit

* Tue Dec 04 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.0-4
- Backport upstream commit to fix a memory leak from a static pointer

* Tue Dec 04 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.0-3
- Backport upstream PR to build with -fno-plt optimization

* Mon Nov 26 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.0-2
- Backport upstream commit to use a safer strcpy for the NT method
- Backport upstream generating base64 encoded output for NT gensalt
- Backport upstream commit to require less rbytes for NT gensalt
- Backport upstream commit to test incremental hmac-sha256 computation
- Add Recommends: mkpasswd for Fedora >= 30

* Tue Nov 20 2018 Björn Esser <besser82@fedoraproject.org> - 4.4.0-1
- New upstream release
