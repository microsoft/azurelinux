Vendor:         Microsoft Corporation
Distribution:   Mariner
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
Release:          12%{?dist}

License:          AGPLv3+

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
* Fri Oct 15 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 0.35-12
- Initial CBL-Mariner import from Fedora 32 (license: MIT).

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
