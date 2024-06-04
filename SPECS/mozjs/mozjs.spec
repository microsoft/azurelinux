%global major 102

# LTO - Enable in Release builds, but consider disabling for development as it increases compile time
%global build_with_lto    1

%if 0%{?build_with_lto}
# LTO is the default
%else
%define _lto_cflags %{nil}
%endif

# Disable LTO on aarch64 (borked since GCC14)
# https://bugzilla.redhat.com/show_bug.cgi?id=2260867
%ifarch aarch64
%define _lto_cflags %{nil}
%endif

# Big endian platforms
%ifarch ppc ppc64 s390 s390x
%global big_endian 1
%endif

Name:           mozjs
Version:        102.15.1
Release:        1%{?dist}
Summary:        SpiderMonkey JavaScript library

Vendor:         Microsoft Corporation
Distribution:   Azure Linux

License:        MPL-2.0 AND Apache-2.0 AND BSD-3-Clause AND BSD-2-Clause AND MIT AND GPL-3.0-or-later
URL:            https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey
Source0:        https://ftp.mozilla.org/pub/firefox/releases/%{version}esr/source/firefox-%{version}esr.source.tar.xz

# Known failures with system libicu
Source1:        known_failures.txt

# Patches from mozjs68, rebased for mozjs78:
Patch01:        fix-soname.patch
Patch02:        copy-headers.patch
Patch03:        tests-increase-timeout.patch
Patch09:        icu_sources_data.py-Decouple-from-Mozilla-build-system.patch
Patch10:        icu_sources_data-Write-command-output-to-our-stderr.patch

# Build fixes - https://hg.mozilla.org/mozilla-central/rev/ca36a6c4f8a4a0ddaa033fdbe20836d87bbfb873
Patch12:        emitter.patch
Patch13:        tests-Use-native-TemporaryDirectory.patch

# Build fixes
Patch14:        init_patch.patch
Patch15:        remove-sloppy-m4-detection-from-bundled-autoconf.patch

# tentative patch for RUSTFLAGS parsing issue, taken from firefox package:
# https://bugzilla.redhat.com/show_bug.cgi?id=2184743
# https://bugzilla.mozilla.org/show_bug.cgi?id=1474486
Patch16:        firefox-112.0-commasplit.patch

Patch17:        Replace-distutils.LooseVersion-with-looseversion.LooseVersion.patch
# This is ugly, I know, I know...
Patch18:        Hacky-workaround-for-expected-string-or-bytes-like-object.patch

# TODO: Check with mozilla for cause of these fails and re-enable spidermonkey compile time checks if needed
Patch20:        spidermonkey_checks_disable.patch

# s390x/ppc64 fixes
Patch21:        0001-Skip-failing-tests-on-ppc64-and-s390x.patch

# AzLinux CVE patches
Patch30:       CVE-2022-48285.patch

# libvpx CVE patches created by finding commits included in v1.13.1 after v1.13.0
# and modifying paths to match embedded mozjs paths
Patch40:       CVE-2023-6349-0001-VP8-disallow-thread-count-changes.patch
Patch41:       CVE-2023-6349-0002-vp9_alloccommon-clear-allocation-sizes-on-free.patch
Patch42:       CVE-2023-6349-0003-Fix-bug-with-smaller-width-bigger-size.patch

# AzLinux packages cargo and rustfmt in the rust package
%if !0%{?azl}
BuildRequires:  cargo
%endif
%if !0%{?rhel}
BuildRequires:  ccache
%endif
BuildRequires:  clang-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  m4
BuildRequires:  make
%ifarch x86_64
BuildRequires:  nasm
%endif
BuildRequires:  libicu-devel
BuildRequires:  llvm
BuildRequires:  rust
%if !0%{?azl}
BuildRequires:  rustfmt
%endif
BuildRequires:  perl-devel
BuildRequires:  pkgconfig(libffi)
BuildRequires:  pkgconfig(zlib)
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-looseversion
BuildRequires:  python3-six
BuildRequires:  readline-devel
BuildRequires:  wget
BuildRequires:  zip

Requires:       icu >= 72
Requires:       python3

%description
SpiderMonkey is the code-name for Mozilla Firefox's C++ implementation of
JavaScript. It is intended to be embedded in other applications
that provide host environments for JavaScript.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%autosetup -n firefox-%{version}/js/src -N

pushd ../..
%autopatch -p1

# Purge the bundled six library incompatible with Python 3.12
rm third_party/python/six/six.py

# Link the system six library (build tooling expects that)
ln -s /usr/lib/python%{python3_version}/site-packages/six.py third_party/python/six/six.py

# Set up looseversion
mkdir third_party/python/looseversion
ln -s /usr/lib/python%{python3_version}/site-packages/looseversion/__init__.py third_party/python/looseversion/looseversion.py
echo "vendored:third_party/python/looseversion" >>  python/sites/mach.txt

# Copy out the LICENSE file
cp LICENSE js/src/

# Copy out file containing known test failures with system libicu
cp %{SOURCE1} js/src/

# Remove zlib directory (to be sure using system version)
rm -rf modules/zlib

# Remove unneeded bundled stuff
rm -rf js/src/devtools/automation/variants/
rm -rf js/src/octane/
rm -rf js/src/ctypes/libffi/

popd

%build
%if 0%{?build_with_lto}
# https://github.com/ptomato/mozjs/commit/36bb7982b41e0ef9a65f7174252ab996cd6777bd
export CARGO_PROFILE_RELEASE_LTO=true
%endif

# Use bundled autoconf
export M4=m4
export AWK=awk
export AC_MACRODIR=../../build/autoconf/  # modified for AzL

sh ../../build/autoconf/autoconf.sh --localdir=/builddir/build/BUILD/firefox-%{version}/js/src configure.in > configure
chmod +x configure

%configure \
  --with-system-icu \
  --with-system-zlib \
%if 0%{?with_check}
  --enable-tests \
%else
  --disable-tests \
%endif
  --disable-strip \
  --with-intl-api \
  --enable-readline \
  --enable-shared-js \
  --enable-optimize \
  --disable-debug \
  --enable-pie \
  --disable-jemalloc

%make_build

%install
%make_install

# Fix permissions
chmod -x %{buildroot}%{_libdir}/pkgconfig/*.pc

# Avoid multilib conflicts
case `uname -i` in
  i386 | ppc | s390 | sparc )
    wordsize="32"
    ;;
  x86_64 | ppc64 | s390x | sparc64 )
    wordsize="64"
    ;;
  *)
    wordsize=""
    ;;
esac

if test -n "$wordsize"
then
  mv %{buildroot}%{_includedir}/mozjs-%{major}/js-config.h \
     %{buildroot}%{_includedir}/mozjs-%{major}/js-config-$wordsize.h

  cat >%{buildroot}%{_includedir}/mozjs-%{major}/js-config.h <<EOF
#ifndef JS_CONFIG_H_MULTILIB
#define JS_CONFIG_H_MULTILIB

#include <bits/wordsize.h>

#if __WORDSIZE == 32
# include "js-config-32.h"
#elif __WORDSIZE == 64
# include "js-config-64.h"
#else
# error "unexpected value for __WORDSIZE macro"
#endif

#endif
EOF

fi

# Remove unneeded files
rm %{buildroot}%{_bindir}/js%{major}-config
rm %{buildroot}%{_libdir}/libjs_static.ajs

# Rename library and create symlinks, following fix-soname.patch
mv %{buildroot}%{_libdir}/libmozjs-%{major}.so \
   %{buildroot}%{_libdir}/libmozjs-%{major}.so.0.0.0
ln -s libmozjs-%{major}.so.0.0.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so.0
ln -s libmozjs-%{major}.so.0 %{buildroot}%{_libdir}/libmozjs-%{major}.so

%check
tests_ok=true

# Run SpiderMonkey tests
%{python3} tests/jstests.py -d -s -t 2400 --exclude-file=known_failures.txt --no-progress --wpt=disabled ../../js/src/dist/bin/js%{major} || tests_ok=false

# Run basic JIT tests

# large-arraybuffers/basic.js fails on s390x
%ifarch s390 s390x
%{python3} jit-test/jit_test.py -s -t 2400 --no-progress -x large-arraybuffers/basic.js ../../js/src/dist/bin/js%{major} basic || tests_ok=false
%else
%{python3} jit-test/jit_test.py -s -t 2400 --no-progress ../../js/src/dist/bin/js%{major} basic || tests_ok=false
%endif

$tests_ok

%files
%doc README.html
%license LICENSE
%{_libdir}/libmozjs-%{major}.so.0*

%files devel
%{_bindir}/js%{major}
%{_libdir}/libmozjs-%{major}.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/mozjs-%{major}/

%changelog
* Tue Mar 12 2024 corvus-callidus <108946721+corvus-callidus@users.noreply.github.com> - 102.15.1-1
- Initial Azure Linux import from Fedora 39 (license: MIT).
- License verified
- Replaced Photon spec for v78 with Fedora spec for new version.
- Removed conditional option %%{require_tests}. This variable controlled whether the %%check section failed on failing tests or ignored failures. We always want to know if tests fail.

* Mon Mar 13 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.9.0-1
- mozjs102-102.9.0 (fixes RHBZ#2177727)

* Fri Feb 17 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.8.0-1
- mozjs102-102.8.0 (fixes RHBZ#2169721)

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 102.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Jan 16 2023 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.7.0-1
- mozjs102-102.7.0 (fixes RHBZ#2161250)

* Sat Dec 31 2022 Pete Walter <pwalter@fedoraproject.org> - 102.6.0-2
- Rebuild for ICU 72

* Mon Dec 12 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.6.0-1
- mozjs102-102.6.0 (fixes RHBZ#2152654)

* Tue Nov 15 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.5.0-1
- mozjs102-102.5.0

* Mon Oct 17 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.4.0-1
- mozjs102-102.4.0 (fixes RHBZ#2135298)

* Wed Sep 21 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.3.0-1
- mozjs102-102.3.0 (fixes RHBZ#2127989)

* Mon Aug 22 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.2.0-1
- mozjs102-102.2.0

* Wed Jul 27 2022 Frantisek Zatloukal <fzatlouk@redhat.com> - 102.1.0-1
- Initial mozjs102 package based on mozjs91
