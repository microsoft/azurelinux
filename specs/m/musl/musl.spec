# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# We are not using this as the system libc,
# so this remains disabled by default.
%bcond_with system_libc

# Fedora uses multilib with /usr/lib64
# This switch changes it to multiarch, with /usr/lib/[arch]-linux-musl
# This switch only has effect if system_libc is disabled.
# This switch is disabled by default.
%bcond_with multiarch

# Fedora uses glibc as the standard libc.
# This means any packages that would use musl would be treated
# as a cross-compilation target. Cross-mode sets it up for this application.
# In cross-mode, a prefix root is created with a new child FHS area.
# This switch only has effect if system_libc is disabled.
# This switch is enabled by default.
%bcond_without crossmode


# Ensure the value is set correctly
%ifarch %{x86_64}
%global _musl_target_cpu x86_64
%endif

%ifarch %{ix86}
%global _musl_target_cpu i386
%endif

%ifarch %{arm}
# ARM is... complicated...
%ifarch armv3l armv4b armv4l armv4tl armv5tl armv5tel armv5tejl armv6l armv7l
%global _musl_target_cpu arm
%else
%global _musl_target_cpu armhf
%endif
%global _musl_platform_suffix eabi
%endif

%ifarch %{mips64}
%global _musl_target_cpu mips64
%endif

%ifarch %{mips32}
%global _musl_target_cpu mips
%endif

%ifarch ppc
%global _musl_target_cpu powerpc
%endif

%ifarch %{power64}
# POWER architectures have a different name if little-endian
%ifarch ppc64le
%global _musl_target_cpu powerpc64le
%else
%global _musl_target_cpu powerpc64
%endif
%endif

%ifnarch %{x86_64} %{ix86} %{arm} %{mips} %{power64} ppc
%global _musl_target_cpu %{_target_cpu}
%endif

# Define the platform name
%global _musl_platform %{_musl_target_cpu}-linux-musl%{?_musl_platform_suffix}

# Paths to use when not set up in cross-mode
%if %{without crossmode}
# Set up alternate paths when not using as system libc
%if %{without system_libc}
# Set up libdir path for when using multilib
%if %{without multiarch}
%global _libdir %{_prefix}/%{_lib}/%{_musl_platform}
%else
# Set up libdir path for when using multiarch
%global _libdir %{_prefix}/lib/%{_musl_platform}
%endif
%global _includedir %{_prefix}/include/%{_musl_platform}
%endif
%else
# Cross-mode paths
%global _libdir %{_prefix}/%{_musl_platform}/%{_lib}
%global _includedir %{_prefix}/%{_musl_platform}/include
%endif

%if %{without multiarch}
# We need to be multilib aware
%global _syslibdir /%{_lib}
%else
%global _syslibdir /lib
%endif

Name:		musl
Version:	1.2.5
Release:	5%{?dist}
Summary:	Fully featured lightweight standard C library for Linux
License:	MIT
URL:		https://musl.libc.org
Source0:	%{url}/releases/%{name}-%{version}.tar.gz
Source1:	%{url}/releases/%{name}-%{version}.tar.gz.asc
Source2:	%{url}/musl.pub

# Fix Makefile to not use INSTALL variable so make_install macro works
Patch0:		musl-1.1.18-Makefile-rename-INSTALL-var.patch
# Support PIE with static linking
Patch1:		musl-1.2.0-Support-static-pie-with-musl-gcc-specs.patch

# From upstream to fix systemd builds on musl
Patch10:        https://git.musl-libc.org/cgit/musl/patch/?id=fde29c04adbab9d5b081bf6717b5458188647f1c#/musl-1.2.5-stdio-skip-empty-iovec-when-buffering-is-disabled.patch

# musl is only for Linux
ExclusiveOS:	linux

# s390 is not supported by musl-libc
ExcludeArch:	s390

BuildRequires:	gcc
BuildRequires:	make

# For GPG signature verification
BuildRequires:	gnupg2


%description
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

%package libc
Summary:	Fully featured lightweight standard C library for Linux

# This package provides musl dynamic libs too
Obsoletes:	%{name}-libs < %{version}-%{release}
Provides:	%{name}-libs = %{version}-%{release}
Provides:	%{name}-libs%{?_isa} = %{version}-%{release}
# Ensure the filesystem skeleton is installed if it was built
%if %{without system_libc}
Requires:	%{name}-filesystem%{?_isa} = %{version}-%{release}
%endif

%description libc
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

This package provides the system dynamic linker library.
It also provides the dynamic libraries for linking
programs and libraries against musl.

%if %{without system_libc}
%package filesystem
Summary:	Base filesystem for %{name}

%description filesystem
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

This package provides the base filesystem directories
for libraries and headers linked against musl.
%endif

%package devel
Summary:	Development files for %{name}

# This package also provides the headers for using musl
Provides:	%{name}-headers = %{version}-%{release}
Provides:	%{name}-headers%{?_isa} = %{version}-%{release}

Requires:	%{name}-libc = %{version}-%{release}
%if ! (0%{?rhel} && 0%{?rhel} < 8)
Recommends:	%{name}-libc-static = %{version}-%{release}
%endif

%description devel
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

This package provides the development files for using
musl with programs and libraries.

%package libc-static
Summary:	Static link library for %{name}
Obsoletes:	%{name}-static < %{version}-%{release}
Provides:	%{name}-static = %{version}-%{release}
Provides:	%{name}-static%{?_isa} = %{version}-%{release}
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description libc-static
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

This package provides the additional development files for
statically linking musl into programs and libraries.

%package gcc
Summary:	Wrapper for using gcc with musl
Requires:	%{name}-devel = %{version}-%{release}
Requires:	gcc

%description gcc
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

This package provides a wrapper around gcc to compile
programs and libraries with musl easily.

%package clang
Summary:	Wrapper for using clang with musl
Requires:	%{name}-devel = %{version}-%{release}
Requires:	clang

%description clang
musl is a C standard library to power a new generation
of Linux-based devices. It is lightweight, fast, simple,
free, and strives to be correct in the sense of standards
conformance and safety.

This package provides a wrapper around clang to compile
programs and libraries with musl easily.


%prep
# Verify *before* actually unpacking!
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'

# Unpack sources and apply patches
%autosetup -p1


%build
# musl is known not to work with LTO
# Disable LTO
%define _lto_cflags %{nil}

%ifarch %{power64}
# Deal with ABI mismatch on long double between glibc and musl
export CC="gcc -mlong-double-64"
%endif

# Set linker flags to get correct soname...
export LDFLAGS="%{?build_ldflags} -Wl,-soname,ld-musl-%{_musl_target_cpu}.so.1"
%configure --enable-debug --enable-wrapper=all
%make_build


%install
%make_install

# Swap the files around for libc.so, making libc.so a symlink to the real file
rm %{buildroot}/lib/ld-musl-%{_musl_target_cpu}.so.1
mv %{buildroot}%{_libdir}/libc.so %{buildroot}/lib/ld-musl-%{_musl_target_cpu}.so.1
ln -sr %{buildroot}/lib/ld-musl-%{_musl_target_cpu}.so.1 %{buildroot}%{_libdir}/ld-musl-%{_musl_target_cpu}.so.1
ln -sr %{buildroot}%{_libdir}/ld-musl-%{_musl_target_cpu}.so.1 %{buildroot}%{_libdir}/libc.so

# Write search path for dynamic linker
mkdir -p %{buildroot}%{_sysconfdir}
touch %{buildroot}%{_sysconfdir}/ld-musl-%{_musl_target_cpu}.path
cat > %{buildroot}%{_sysconfdir}/ld-musl-%{_musl_target_cpu}.path <<EOF
%{_libdir}
EOF

%if %{without multiarch}
# Write symlink for syslib to /lib64 for compatibility with Fedora standards, where applicable
mkdir -p %{buildroot}%{_syslibdir}
%if "%{_lib}" == "lib64"
ln -sr %{buildroot}/lib/ld-musl-%{_musl_target_cpu}.so.1 %{buildroot}%{_syslibdir}/ld-musl-%{_musl_target_cpu}.so.1
%endif
%endif

mkdir -p %{buildroot}%{_rpmconfigdir}/macros.d
touch %{buildroot}%{_rpmconfigdir}/macros.d/macros.musl
cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.musl <<EOF
%%_musl_libdir %{_libdir}
%%_musl_includedir %{_includedir}
EOF

%files libc
%license COPYRIGHT
/lib/ld-musl-%{_musl_target_cpu}.so.1
%if %{without multiarch}
%if "%{_lib}" == "lib64"
%{_syslibdir}/ld-musl-%{_musl_target_cpu}.so.1
%endif
%endif
%{_libdir}/ld-musl-%{_musl_target_cpu}.so.1
%config(noreplace) %{_sysconfdir}/ld-musl-%{_musl_target_cpu}.path

%if %{without system_libc}
%files filesystem
%if %{with crossmode}
%dir %{_prefix}/%{_musl_platform}
%endif
%dir %{_libdir}
%dir %{_includedir}
%endif

%files devel
%license COPYRIGHT
%doc README WHATSNEW
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/*.o
%{_libdir}/*.a
%exclude %{_libdir}/libc.a
%{_rpmconfigdir}/macros.d/macros.musl

%files libc-static
%license COPYRIGHT
%{_libdir}/libc.a

%files gcc
%license COPYRIGHT
%{_bindir}/musl-gcc
%{_libdir}/musl-gcc.specs

%files clang
%license COPYRIGHT
%{_bindir}/musl-clang
%{_bindir}/ld.musl-clang


%changelog
* Sun Nov 23 2025 Neal Gompa <ngompa@fedoraproject.org> - 1.2.5-5
- Backport fix for stdio to skip empty iovec when buffering is disabled

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr 01 2025 Eduard Abdullin <eabdullin@almalinux.org> - 1.2.5-3
- Use the x86_64 target on x86_64 microarches

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Jul 23 2024 Mary Guillemard <mary@mary.zone> - 1.2.5-1
- Update to 1.2.5

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Apr 07 2022 Neal Gompa <ngompa@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun May 30 2021 Neal Gompa <ngompa13@gmail.com> - 1.2.2-1
- Update to 1.2.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Aug 11 2020 Neal Gompa <ngompa13@gmail.com> - 1.2.1-1
- Update to 1.2.1

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul  1 2020 Jeff Law <law@redhat.com> - 1.2.0-4
- Disable LTO

* Tue Apr 14 2020 Neal Gompa <ngompa13@gmail.com> - 1.2.0-3
- Add missing symlink for dynamically linked executables to work

* Tue Apr  7 2020 Neal Gompa <ngompa13@gmail.com> - 1.2.0-2
- Clean up description

* Mon Apr  6 2020 Neal Gompa <ngompa13@gmail.com> - 1.2.0-1
- Rebase to 1.2.0
- Add patch to support PIE with static linking
- Remove obsolete Group tags
- Fix musl library locations and broken sonames
- Update URL and Source URLs
- Add filesystem subpackage for install directories

* Tue Feb  4 2020 Neal Gompa <ngompa13@gmail.com> - 1.1.24-1
- Update to 1.1.24
- Clean out conditionals referring to obsolete Fedora versions
- Verify sources with GPG

* Sun Nov  5 2017 Neal Gompa <ngompa13@gmail.com> - 1.1.18-1
- Update to 1.1.18
- Add patch to fix Makefile with make_install macro

* Sat Apr 15 2017 Neal Gompa <ngompa13@gmail.com> - 1.1.16-1
- Update to 1.1.16
- Remove block on s390x
- Add _musl_libdir and _musl_includedir macros

* Fri Aug  5 2016 Neal Gompa <ngompa13@gmail.com> - 1.1.15-1
- Update to 1.1.15
- Remove blocks on 64-bit MIPS and PowerPC

* Thu Mar  3 2016 Neal Gompa <ngompa13@gmail.com> - 1.1.14-1
- Update to 1.1.14
- Add crossmode bcond switch
- Add multiarch bcond switch
- Rename musl-libs to musl-libc
- Rename musl-static to musl-libc-static

* Tue Dec 22 2015 Neal Gompa <ngompa13@gmail.com> - 1.1.12-1
- Initial packaging
