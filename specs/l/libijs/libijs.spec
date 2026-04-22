# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# === GLOBAL MACROS ===========================================================

# According to Fedora Package Guidelines, it is advised that packages that can
# process untrusted input are build with position-independent code (PIC).
#
# Koji should override the compilation flags and add the -fPIC or -fPIE flags
# by default. This is here just in case this wouldn't happen for some reason.
# For more info: https://fedoraproject.org/wiki/Packaging:Guidelines#PIE
%global _hardened_build 1

# =============================================================================

Name:             libijs
Summary:          IJS Raster Image Transport Protocol Library
Version:          0.35
Release: 26%{?dist}

License:          AGPL-3.0-or-later

URL:              https://ghostscript.com/
Source:           https://github.com/ArtifexSoftware/ijs/archive/%{version}.tar.gz#/ijs-%{version}.tar.gz

BuildRequires:    gcc
BuildRequires:    git
BuildRequires:    autoconf
BuildRequires:    automake
BuildRequires:    libtool

# =============================================================================

# NOTE: 'autosetup' macro (below) uses 'git' for applying the patches:
#       ->> All the patches should be provided in 'git format-patch' format.
#       ->> Auxiliary repository will be created during 'fedpkg prep', you
#           can see all the applied patches there via 'git log'.

# Upstream patches -- official upstream patches released by upstream since the
# ----------------    last rebase that are necessary for any reason:
#Patch000: example000.patch
# https://git.ghostscript.com/?p=ghostpdl.git;a=commitdiff;h=eb770edd1c
Patch: 0001-Squash-compiler-warning-in-ijs-code.patch


# Downstream patches -- these should be always included when doing rebase:
# ------------------
#Patch100: example100.patch


# Downstream patches for RHEL -- patches that we keep only in RHEL for various
# ---------------------------    reasons, but are not enabled in Fedora:
%if %{defined rhel} || %{defined centos}
#Patch200: example200.patch
%endif


# Patches to be removed -- deprecated functionality which shall be removed at
# ---------------------    some point in the future:


%description
The IJS (InkJet Server) Raster Image Transport Protocol is a library, which
is no longer actively developed, and often other alternatives are used instead.

This library, however, still seem to be useful for Ghostscript application
to be able to connect to the HP IJS server to print on an HP printer.

# === SUBPACKAGES =============================================================

%package devel
Summary:          Header & pkgconfig files for %{name}
Requires:         %{name}%{?_isa} = %{version}-%{release}
BuildRequires:    pkgconfig
BuildRequires: make

%description devel
This subpackage provides /usr/include/ijs/ijs.h header file, as well as ijs.pc
pkgconfig file. Both of these files are useful for development purposes only.

# ---------------

%package doc
Summary:          Documentation for %{name}
Requires:         %{name} = %{version}-%{release}
BuildArch:        noarch

%description doc
This subpackage contains PDF documentation with IJS protocol specification,
which is useful for development purposes only.

# === BUILD INSTRUCTIONS ======================================================

# We have to override the folder name, because upstream's archive cotains the
# name 'ijs' (not 'libijs')...
%prep
%autosetup -n ijs-%{version} -S git

# ---------------

%build
autoreconf -ifv
%configure --disable-static --enable-shared
%make_build

# ---------------

%install
%make_install

# Remove files that we don't want to ship:
rm -rf %{buildroot}%{_bindir}
rm -rf %{buildroot}%{_libdir}/*.la

# Install the ijs_spec.pdf to correct location:
install -m 0755 -d %{buildroot}%{_docdir}/%{name}
install -m 0644 -p ijs_spec.pdf %{buildroot}%{_docdir}/%{name}

# === PACKAGING INSTRUCTIONS ==================================================

%files
%license COPYING
%{_libdir}/libijs-%{version}.so

# ---------------

%files devel
%dir %{_includedir}/ijs
%{_includedir}/ijs/*.h
%{_libdir}/libijs.so
%{_libdir}/pkgconfig/*.pc

# ---------------
%files doc
%dir %{_docdir}/%{name}
%doc %{_docdir}/%{name}/ijs_spec.pdf

# =============================================================================

%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Jan 09 2024 Zdenek Dohnal <zdohnal@redhat.com> - 0.35-20
- fix FTBFS with GCC 14

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Feb 16 2023 Richard Lescak <rlescak@redhat.com> - 0.35-18
- SPDX migration

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 0.35-8
- Rebuild with fixed binutils

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.35-7
- Rebuild for new binutils

* Fri Jul 27 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.35-6
- FTBFS caused by new version of aclocal fixed (bug #1604599)

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sat Mar 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.35-4
- Remove unneeded ldconfig scriptlets

* Wed Feb 28 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.35-3
- source updated to point at upstream's Github

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.35-2.gitd26d2bb
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 22 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.35-1.gitd26d2bb
- initial specfile
