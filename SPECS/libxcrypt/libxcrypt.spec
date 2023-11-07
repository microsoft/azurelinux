# This macro was added in Fedora 20. Use the old version if it's undefined
# on older Fedoras and RHELs prior to RHEL 8.
# https://fedoraproject.org/wiki/Changes/UnversionedDocdirs
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}
# Build with new api?
%if 0%{?fedora} >= 30 || 0%{?rhel} >= 9
%bcond_without new_api
%else
%bcond_with    new_api
%endif
# First version of glibc built without libcrypt.
%global glibc_minver     2.27-12
# The libxcrypt-devel package conflicts with out-dated manuals
# shipped with the man-pages packages *before* this EVR.
%global man_pages_minver 4.15-3
# Hash methods and API supported by libcrypt.
# NEVER EVER touch this, if you do NOT know what you are doing!
%global hash_methods   all
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
# Common configure options.
%global common_configure_options           \\\
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
# Fail linking if there are undefined symbols.
# Required for proper ELF symbol versioning support.
%global _ld_strict_symbol_defs 1
# override_glibc and glibcversion are temporary to make libxcrypt install on top of glibc
%define glibcversion 2.38
%bcond_with override_glibc
# Build the static library?
%bcond_with new_api
%bcond_with compat_pkg
%bcond_with staticlib
%bcond_with enosys_stubs
# Build the compat package?
%if !(0%{?fedora} >= 999 || 0%{?rhel} >= 99) && %{with new_api}
%bcond_without compat_pkg
%else
%bcond_with    compat_pkg
%endif
# Replace obsolete functions with a stub?
%if (0%{?fedora} >= 30 || 0%{?rhel} >= 9) && %{with compat_pkg}
%bcond_without enosys_stubs
%else
%bcond_with    enosys_stubs
%endif
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
Summary:        Extended crypt library for descrypt, md5crypt, bcrypt, and others
Name:           libxcrypt
Version:        4.4.27
Release:        1%{?dist}
# For explicit license breakdown, see the
# LICENSING file in the source tarball.
License:        LGPLv2+ AND BSD AND Public Domain
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://github.com/besser82/%{name}
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
#BuildRequires:  fipscheck
BuildRequires:  gcc
BuildRequires:  glibc-devel
BuildRequires:  libtool

BuildRequires:  perl-open
BuildRequires:  perl-FindBin
BuildRequires:  perl-lib

BuildRequires:  perl-core
# We do not need to keep this forever.
%if !(0%{?fedora} > 31 || 0%{?rhel} > 10)
# Inherited from former libcrypt package.
Obsoletes:      libcrypt-nss < %{glibc_minver}
Provides:       libcrypt-nss = %{glibc_minver}
Provides:       libcrypt-nss%{?_isa} = %{glibc_minver}
# Obsolete former libcrypt properly and provide a virtual libcrypt
# package as it has been done by the former packages, which were
# built by glibc before.
Obsoletes:      libcrypt < %{glibc_minver}
Provides:       libcrypt = %{glibc_minver}
Provides:       libcrypt%{?_isa} = %{glibc_minver}
# Obsolete former libxcrypt-common properly.
Obsoletes:      %{name}-common < 4.3.3-4
Provides:       %{name}-common = %{version}-%{release}
%endif
%if %{with new_api} && %{without compat_pkg}
Obsoletes:      %{name}-compat < %{version}-%{release}
%endif
# We need a version of glibc, that doesn't build libcrypt anymore.
#Requires:       glibc%{?_isa}         >= %{glibc_minver}
%if %{with override_glibc}
# Require a specific glibc version so the post macro is compatible.
BuildRequires:  glibc-devel = %{glibcversion}
Requires:       glibc = %{glibcversion}
%endif
%if 0%{?fedora} >= 30
Recommends:     mkpasswd
%endif

%description
libxcrypt is a modern library for one-way hashing of passwords.  It
supports a wide variety of both modern and historical hashing methods:
yescrypt, gost-yescrypt, scrypt, bcrypt, sha512crypt, sha256crypt,
md5crypt, SunMD5, sha1crypt, NT, bsdicrypt, bigcrypt, and descrypt.
It provides the traditional Unix crypt and crypt_r interfaces, as well
as a set of extended interfaces pioneered by Openwall Linux, crypt_rn,
crypt_ra, crypt_gensalt, crypt_gensalt_rn, and crypt_gensalt_ra.

libxcrypt is intended to be used by login(1), passwd(1), and other
similar programs; that is, to hash a small number of passwords during
an interactive authentication dialogue with a human. It is not suitable
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
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glibc%{?_isa} >= %{glibc_minver}

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
#Conflicts:      man-pages              < %{man_pages_minver}
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       glibc-devel%{?_isa} >= %{glibc_minver}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%if %{with staticlib}
%package        static
Summary:        Static library for -static linking with %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
Requires:       glibc-devel%{?_isa} >= %{glibc_minver}

%description    static
This package contains the libxcrypt static library for -static
linking.

You don't need this, unless you link statically, which is highly
discouraged.
%endif


%prep
%autosetup

$(realpath ./autogen.sh)

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
the functionality of the encrypt, encrypt_r, setkey, setkey_r,
and fcrypt functions, while keeping fully binary compatibility
with existing (third-party) applications possibly still using
those funtions.  If such an application attemps to call one of
these functions, the corresponding function will indicate that
it is not supported by the system in a POSIX-compliant way.

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


%install
%if %{with compat_pkg}
# Install the compatibility library.
%make_install -C %{_vpath_builddir}-compat

# Cleanup everything we do not need from the compatibility library.
find %{buildroot} -xtype f -not -name 'libcrypt.so.%{csoc}*' -delete -print
find %{buildroot} -type l -not -name 'libcrypt.so.%{csoc}*' -delete -print
%endif

# Install the default system library.
%make_install -C %{_vpath_builddir}

# Get rid of libtool crap.
find %{buildroot} -type f -name "*.la" -delete -print

# Install documentation to shared %%_pkgdocdir.
install -Dpm 0644 -t %{buildroot}%{_pkgdocdir} \
  ChangeLog NEWS README* THANKS TODO

# Drop README.md as it is identical to README.
rm -f %{buildroot}%{_pkgdocdir}/README.md

%if %{with override_glibc}
mv %{buildroot}/%{_libdir}/libcrypt.so.%{sov} %{buildroot}/%{_libdir}/libxcrypt.so.%{sov}
%endif


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

%if %{with override_glibc}
# This posttrans section is a stopgap to allow installing
# libxcrypt on a system that already has libcrypt from glibc.
# In a future release these will be removed and libxcrypt will be default.
%posttrans
rm %{_libdir}/libcrypt.so.1
ln -s %{_libdir}/libxcrypt.so.%{sov} %{_libdir}/libcrypt.so.1
%endif

%post -p /sbin/ldconfig

%postun
# See above comments about the %%posttrans section
%if %{with override_glibc}
rm %{_libdir}/libcrypt.so.1
ln -s %{_libdir}/libcrypt-%{glibcversion}.so %{_libdir}/libcrypt.so.1
%endif
/sbin/ldconfig

%if %{with compat_pkg}
%post -n compat -p /sbin/ldconfig
%postun -n compat -p /sbin/ldconfig
%endif


%files
%license AUTHORS COPYING.LIB LICENSING
#%dir %{_fipsdir}
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
#%{_fipsdir}/libcrypt.so.%{soc}.hmac
#%{_fipsdir}/libcrypt.so.%{sov}.hmac

%if %{with override_glibc}
%exclude %{_libdir}/libcrypt.so.%{soc}
%{_libdir}/libxcrypt.so.%{sov}
%else
%{_libdir}/libcrypt.so.%{soc}
%{_libdir}/libcrypt.so.%{sov}
%endif

%{_mandir}/man5/crypt.5*

%if %{with compat_pkg}
%files compat
#%dir %{_fipsdir}
%if %{with enosys_stubs}
%doc %{_pkgdocdir}/README.posix
%endif
#%{_fipsdir}/libcrypt.so.%{csoc}.hmac
#%{_fipsdir}/libcrypt.so.%{csov}.hmac
%{_libdir}/libcrypt.so.%{csoc}
%{_libdir}/libcrypt.so.%{csov}
%endif


%files devel
%doc %{_pkgdocdir}/ChangeLog
%doc %{_pkgdocdir}/TODO
%if %{with override_glibc}
%exclude %{_libdir}/libcrypt.so
%exclude %{_includedir}/crypt.h
%else
%{_libdir}/libcrypt.so
%{_includedir}/crypt.h
%endif
%if %{without new_api}
%{_libdir}/libxcrypt.so
%endif
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
%files static
#%dir %{_fipsdir}
%doc %{_pkgdocdir}/README.static
#%{_fipsdir}/libcrypt.a.hmac
%if %{without new_api}
#%{_fipsdir}/libxcrypt.a.hmac
%endif
%{_libdir}/libcrypt.a
%if %{without new_api}
%{_libdir}/libxcrypt.a
%endif
%endif


%changelog
* Thu Apr 14 2022 Andrew Phelps <anphel@microsoft.com> - 4.4.27-2
- Update glibcversion variable to 2.35

* Wed Jan 27 2022 Henry Li <lihl@microsoft.com> - 4.4.27-1
- Upgrade to version 4.4.27
- Remove patches that no longer apply
- Add perl-core as BR

* Mon Nov 22 2021 Andrew Phelps <anphel@microsoft.com> - 4.4.17-4
- Update required glibc version to 2.34

* Sat Nov 21 2020 Thomas Crain <thcrain@microsoft.com> - 4.4.17-3
- Replace %%ldconfig_scriptlets with actual post/postun sections

* Wed Oct 21 2020 Henry Beberman <henry.beberman@microsoft.com> - 4.4.17-2
- Initial CBL-Mariner import from Fedora 31 (license: MIT).
- Remove dependency on fipscheck
- Add override_glibc to allow installs over libcrypt from glibc
- License verified.

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
