# CHANGE FROM 3.0: DISABLE DEBUG PACKAGE
# The custom way we were generating debuginfo broke hmac verification.
# You can decide whether or not it's worth it to re-enable it.
%define debug_package %{nil}
Summary:        A core cryptographic library written by Microsoft
Name:           SymCrypt
Version:        103.8.0
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt
Source0:        https://github.com/microsoft/SymCrypt/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/smuellerDD/jitterentropy-library/archive/v3.3.1.tar.gz#/jitterentropy-library-3.3.1.tar.gz
# CHANGE FROM 3.0: DISABLE DEBUG PACKAGE
# No longer needed for generating debuginfo. See above.
# Source2:        find-debuginfo
# Use ./generate-env-file.sh --release-tag <git-version-tag> to generate this. For example:
#   ./generate-env-file.sh --release-tag v103.5.1
Source3:        symcrypt-build-environment-variables-v%{version}.sh
BuildRequires:  cmake
%ifarch aarch64
BuildRequires:  clang >= 12.0.1-4
%endif
BuildRequires:  gcc
# CHANGE FROM 3.0: ADD BUILD REQUIREMENTS
# The build chroot in 3.0 already had gcc-c++ and libatomic, so they we got buy without listing them, but we need them now.
BuildRequires:  gcc-c++
BuildRequires:  libatomic
BuildRequires:  make
BuildRequires:  python3
BuildRequires:  python3-pyelftools

%description
A core cryptographic library written by Microsoft

# Only x86_64 and aarch64 are currently supported
%ifarch x86_64
%define symcrypt_arch AMD64
%define symcrypt_cc gcc
%define symcrypt_c_flags "-Wno-maybe-uninitialized"
%define symcrypt_cxx g++
%endif


%ifarch aarch64
%define symcrypt_arch ARM64
# Currently SymCrypt ARM64 build requires use of clang
%define symcrypt_cc clang
%define symcrypt_c_flags "-mno-outline-atomics -Wno-conditional-uninitialized"
%define symcrypt_cxx clang++
%endif

%prep
%autosetup -a 1 -p1
# Create a symbolic link as if jitterentropy-library has been pulled in as git submodule
rm -rf 3rdparty/jitterentropy-library
ln -s ../jitterentropy-library-3.3.1 3rdparty/jitterentropy-library

%build
# CHANGE FROM 3.0: REMOVE -z pack-relative-relocs
# AZL4's default LDFLAGS include -Wl,-z,pack-relative-relocs, which makes the
# linker emit R_X86_64_RELATIVE entries in DT_RELR format instead of SHT_RELA.
# SymCrypt's FIPS post-processor (process_fips_module.py) only walks SHT_RELA,
# so RELR-packed relocations are not zeroed before the integrity HMAC is
# computed. The dynamic loader still applies them at load time, so in-memory
# bytes diverge from the hashed bytes and the FIPS self-test fails. Combined
# with -z now, the failure surfaces as a SIGSEGV the instant libsymcrypt.so
# is mapped (e.g. any LD_PRELOAD or DT_NEEDED user crashes immediately).
# Remove until process_fips_module.py learns about DT_RELR.
export LDFLAGS="${LDFLAGS//-Wl,-z,pack-relative-relocs/}"

source %{SOURCE3}
# CHANGE FROM 3.0: DISABLE DEBUG PACKAGE
# Change some cmake flags that were used for debug info generation.
# Originals here:
# cmake   -S . -B bin \
#         -DSYMCRYPT_TARGET_ARCH=%%{symcrypt_arch} \
#         -DSYMCRYPT_STRIP_BINARY=OFF \
#         -DSYMCRYPT_FIPS_POSTPROCESS=OFF \
#         -DCMAKE_BUILD_TYPE=RelWithDebInfo \
#         -DCMAKE_C_COMPILER=%%{symcrypt_cc} \
#         -DCMAKE_CXX_COMPILER=%%{symcrypt_cxx} \
#         -DCMAKE_C_FLAGS="%%{symcrypt_c_flags}" \
#         -DCMAKE_CXX_FLAGS="-Wno-unused-but-set-variable"

cmake   -S . -B bin \
        -DSYMCRYPT_TARGET_ARCH=%{symcrypt_arch} \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_C_COMPILER=%{symcrypt_cc} \
        -DCMAKE_CXX_COMPILER=%{symcrypt_cxx} \
        -DCMAKE_C_FLAGS="%{symcrypt_c_flags}" \
        -DCMAKE_CXX_FLAGS="-Wno-unused-but-set-variable"

# CHANGE FROM 3.0: Parallelize build
# Note actually necessary, but makes iteration faster.
cmake --build bin -j $(nproc)

# CHANGE FROM 3.0: DISABLE DEBUG PACKAGE
# This was all in service of generating debug info. See notes above.
# Override the default find-debuginfo script to our own custom one, which is modified
# to allow us to keep symbols.
# Also add custom options to the call to find-debuginfo.
# %%define __find_debuginfo %%{SOURCE2}
# %%define _find_debuginfo_opts \\\
#     --keep-symbol SymCryptVolatileFipsHmacKey \\\
#     --keep-symbol SymCryptVolatileFipsHmacKeyRva \\\
#     --keep-symbol SymCryptVolatileFipsBoundaryOffset \\\
#     --keep-symbol SymCryptVolatileFipsHmacDigest \\\
#     %%{nil}

# # Override the default to allow us to do custom fips post-processing after debug info/stripping is done.
# # The post-processing script writes the modified file to the same location as the original file, which
# # is subject to default permissions, so we need to set permissions manually after the script.
# %%define __spec_install_post \
#     %%{?__debug_package:%%{__debug_install_post}} \
#     %%{__arch_install_post} \
#     %%{__os_install_post} \
#     mkdir -p "bin/module/generic/processing" \
#     python3 "scripts/process_fips_module.py" "%%{buildroot}%%{_libdir}/libsymcrypt.so.%%{version}" --processing-dir "bin/module/generic/processing" --debug \
#     chmod 755 "%%{buildroot}%%{_libdir}/libsymcrypt.so.%%{version}" \
# %%{nil}

%install
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
install inc/symcrypt* %{buildroot}%{_includedir}
# Use cp -P to preserve symbolic links
cp -P bin/module/generic/libsymcrypt.so* %{buildroot}%{_libdir}
chmod 755 %{buildroot}%{_libdir}/libsymcrypt.so.%{version}

%check
./bin/exe/symcryptunittest

%files
%license LICENSE
%license NOTICE
%{_libdir}/libsymcrypt.so*
%{_includedir}/*

%changelog
* Fri Jan 31 2025 Tobias Brick <tobiasb@microsoft.com> - 103.8.0-1
- Add FIPS approved services indicator
- Add ML-DSA implementation

* Mon Nov 25 2024 Tobias Brick <tobiasb@microsoft.com> - 103.6.0-1
- Upgrde to 103.6.0

* Mon Oct 21 2024 Tobias Brick <tobiasb@microsoft.com> - 103.5.1-1
- Update 103.5.1

* Mon Oct 14 2024 Tobias Brick <tobiasb@microsoft.com> - 103.4.2-2
- Add debuginfo package

* Wed Jun 26 2024 Maxwell Moyer-McKee <mamckee@microsoft.com> - 103.4.2-1
- Update SymCrypt to v103.4.2 for FIPS certification

* Thu Apr 25 2024 Maxwell Moyer-McKee <mamckee@microsoft.com> - 103.4.1-2
- Disable outline atomics in aarch64 builds

* Thu Dec 28 2023 Maxwell Moyer-McKee <mamckee@microsoft.com> - 103.4.1-1
- Update SymCrypt to v103.4.1 for SymCrypt-OpenSSL provider.

* Mon May 22 2023 Samuel Lee <saml@microsoft.com> - 103.0.1-1
- Update SymCrypt to v103.0.1 for FIPS certification. Run unit tests in check

* Fri Oct 07 2022 Andy Caldwell <andycaldwell@microsoft.com> - 102.0.0-2
- Update `clang` on aarch64 builds to enable `-pie`

* Mon Jun 06 2022 Samuel Lee <saml@microsoft.com> - 102.0.0-1
- Update SymCrypt to v102.0.0 to improve performance of FIPS self-tests

* Tue Apr 05 2022 Cameron Baird <cameronbaird@microsoft.com> - 101.2.0-2
- BuildRequires clang in aarch64 builds

* Tue Mar 29 2022 Samuel Lee <saml@microsoft.com> - 101.2.0-1
- Update SymCrypt to v101.2.0 to include FIPS self-tests, certifiable AES-GCM, and fix aarch64 build

* Mon Feb 14 2022 Samuel Lee <saml@microsoft.com> - 101.0.0-1
- Original version for CBL-Mariner
- Verified license
