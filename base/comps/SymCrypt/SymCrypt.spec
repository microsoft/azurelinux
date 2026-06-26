# Standard debuginfo generation breaks the FIPS self-test, so we disable it.
%define debug_package %{nil}
Summary:        A core cryptographic library written by Microsoft
Name:           SymCrypt
Version:        103.11.0
Release:        %autorelease
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
Group:          System/Libraries
URL:            https://github.com/microsoft/SymCrypt
Source0:        https://github.com/microsoft/SymCrypt/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:        https://github.com/smuellerDD/jitterentropy-library/archive/v3.3.1.tar.gz#/jitterentropy-library-3.3.1.tar.gz
# Use ./generate-env-file.sh --release-tag <git-version-tag> to generate this. For example:
#   ./generate-env-file.sh --release-tag v103.5.1
Source3:        symcrypt-build-environment-variables-v%{version}.sh
BuildRequires:  cmake
%ifarch aarch64
BuildRequires:  clang >= 12.0.1-4
%endif
BuildRequires:  gcc
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

cmake   -S . -B bin \
        -DSYMCRYPT_TARGET_ARCH=%{symcrypt_arch} \
        -DCMAKE_BUILD_TYPE=Release \
        -DCMAKE_C_COMPILER=%{symcrypt_cc} \
        -DCMAKE_CXX_COMPILER=%{symcrypt_cxx} \
        -DCMAKE_C_FLAGS="%{symcrypt_c_flags}" \
        -DCMAKE_CXX_FLAGS="-Wno-unused-but-set-variable"

cmake --build bin -j $(nproc)

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
%license LICENSE.txt
%license NOTICE.txt
%{_libdir}/libsymcrypt.so*
%{_includedir}/*

%changelog
%autochangelog
