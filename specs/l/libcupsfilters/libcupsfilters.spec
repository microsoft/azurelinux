# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global _hardened_build 1

%global upstream_version 2.1.1

Name: libcupsfilters
Epoch: 1
Version: 2.1.1
Release: 6%{?dist}
Summary: Library for developing printing filters
# the CUPS exception text is the same as LLVM exception, so using that name with
# agreement from legal team
# https://lists.fedoraproject.org/archives/list/legal@lists.fedoraproject.org/message/A7GFSD6M3GYGSI32L2FC5KB22DUAEQI3/
License: Apache-2.0 WITH LLVM-exception
URL: https://github.com/OpenPrinting/libcupsfilters
Source0: %{URL}/releases/download/%{version}/%{name}-%{version}.tar.gz


# Patches
# https://github.com/OpenPrinting/libcupsfilters/pull/96
Patch001: 0001-configure.ac-Make-CJK-fonts-name-configurable.patch
# CVE-2025-57812
Patch002: lcf-CVE-2025-57812.patch
# CVE-2025-64503
Patch003: 0001-Fix-out-of-bounds-write-in-cfFilterPDFToRaster.patch


# for generating configure and Makefile scripts in autogen.h
BuildRequires: autoconf
# for generating configure and Makefile scripts in autogen.h
BuildRequires: automake
# font for test script
BuildRequires: dejavu-sans-fonts
# most filter functions written in C
BuildRequires: gcc
# pdftopdf written in C++
BuildRequires: gcc-c++
# for generating configure and Makefile scripts in autogen.h
BuildRequires: gettext-devel
# we use gs binary in filter functions, so it could be only runtime
# require, but there is a check in configure, which turns off GS
# support in case the binary is not found, so the binary has to be in
# buildroot
BuildRequires: ghostscript >= 10.0.0
# for autosetup
BuildRequires: git-core
# for generating configure and Makefile scripts in autogen.h
BuildRequires: libtool
# uses Makefiles
BuildRequires: make
# for pkg-config in configure and in SPEC file
BuildRequires: pkgconf-pkg-config
# CUPS and IPP API functions
BuildRequires: pkgconfig(cups) >= 2.2.2
# for communication with colord
BuildRequires: pkgconfig(dbus-1)
# font support - configuration and customization
BuildRequires: pkgconfig(fontconfig)
# color management engine in rastering filter functions
BuildRequires: pkgconfig(lcms2)
# used for getting image resolution from images - they have
# EXIF data in them and library accesses it
BuildRequires: pkgconfig(libexif)
# for jpeg file format support
BuildRequires: pkgconfig(libjpeg)
# for png file format support
BuildRequires: pkgconfig(libpng)
# for pdf filter functions
BuildRequires: pkgconfig(libqpdf) >= 10.3.2
# for tiff image support
BuildRequires: pkgconfig(libtiff-4)
# for pdftoraster filter
BuildRequires: pkgconfig(poppler-cpp)

# remove once CentOS Stream 10 is released
Obsoletes: cups-filters-libs < 2.0

# have a fallback for fonts in texttopdf filter function (bz#1070729)
# but make it weak, so other monospace font can be used if requested
Recommends: liberation-mono-fonts

# we communicate with colord regarding color profiles
Requires: colord
# for directory ownership of:
# /usr/share/cups
# /usr/share/cups/data
Requires: cups-filesystem
# we call gs command in filter functions
Requires: ghostscript >= 10.0.0


%description
Libcupsfilters provides a library, which implements common functions used
in cups-browsed daemon and printing filters, and additional files
as banner templates and character sets. The filters are used in CUPS daemon
and in printer applications.

%package devel
Summary: Development files for libcupsfilters

# remove once CentOS Stream 10 is released
Conflicts: cups-filters-devel{?_isa} < 2.0
# remove once CentOS Stream 10 is released
Obsoletes: cups-filters-devel < 2.0
# c2esp and perl-Net-CUPS requires cups-filters-devel
# remove once CentOS Stream 10 is released
Provides: cups-filters-devel = %{epoch}:%{version}-%{release}

Requires: %{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
Development files for OpenPrinting cupsfilters library.


%prep
%autosetup -S git -n %{name}-%{upstream_version}


%build
# to get configure script
./autogen.sh

%configure --disable-mutool\
 --disable-rpath\
 --disable-silent-rules\
 --disable-static\
 --enable-dbus\
 --with-cjk-fonts=droidsansfallback

# fix rpmlint error about linking to libraries, but not actually using their functions
# it happens when the required libraries uses pkgconfig - pkgconfig file doesn't know
# which specific functions our binary calls, so it tells us to link against every
# possibilities
# https://fedoraproject.org/wiki/Common_Rpmlint_issues#unused-direct-shlib-dependency
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool

%make_build


%check
make check


%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

mkdir -p %{buildroot}%{_pkgdocdir}/fontembed/
install -p -m 0644 cupsfilters/fontembed/README %{buildroot}%{_pkgdocdir}/fontembed/README

# remove .odt files (we have their .pdf versions)
rm -f %{buildroot}%{_datadir}/cups/data/*.odt

# remove redundant files
rm -f %{buildroot}%{_pkgdocdir}/{INSTALL.md,ABOUT-NLS}

# license related files are already under /usr/share/licenses
rm -f %{buildroot}%{_pkgdocdir}/{LICENSE,COPYING,NOTICE}


%{?ldconfig_scriptlets}


%files
%license COPYING LICENSE NOTICE
%dir %{_datadir}/cups/banners
%{_datadir}/cups/banners/classified
%{_datadir}/cups/banners/confidential
%{_datadir}/cups/banners/form
%{_datadir}/cups/banners/secret
%{_datadir}/cups/banners/standard
%{_datadir}/cups/banners/topsecret
%{_datadir}/cups/banners/unclassified
%dir %{_datadir}/cups/charsets
%{_datadir}/cups/charsets/pdf.utf-8
%{_datadir}/cups/charsets/pdf.utf-8.heavy
%{_datadir}/cups/charsets/pdf.utf-8.simple
%{_datadir}/cups/data/classified.pdf
%{_datadir}/cups/data/confidential.pdf
%{_datadir}/cups/data/default-testpage.pdf
%{_datadir}/cups/data/default.pdf
%{_datadir}/cups/data/form_english.pdf
%{_datadir}/cups/data/form_russian.pdf
%{_datadir}/cups/data/secret.pdf
%{_datadir}/cups/data/standard.pdf
%{_datadir}/cups/data/testprint
%{_datadir}/cups/data/topsecret.pdf
%{_datadir}/cups/data/unclassified.pdf
%doc AUTHORS CHANGES.md CHANGES-1.x.md README.md
%dir %{_docdir}/%{name}/fontembed
%{_docdir}/%{name}/fontembed/README
%{_libdir}/libcupsfilters.so.2*

%files devel
%{_docdir}/%{name}/CONTRIBUTING.md
%{_docdir}/%{name}/DEVELOPING.md
%dir %{_includedir}/cupsfilters
%{_includedir}/cupsfilters/*
%{_libdir}/libcupsfilters.so
%{_libdir}/pkgconfig/libcupsfilters.pc


%changelog
* Fri Nov 28 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-5
- fix low CVEs - CVE-2025-64503, CVE-2025-57812

* Tue Aug 05 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-4
- use Droid Sans Fallback fonts for CJK fonts

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed May 21 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-2
- rebuilt with new qpdf

* Wed Feb 19 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.1-1
- 2.1.1 (fedora#2346445)

* Wed Feb 12 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.0-6
- fix bannertopdf regression

* Tue Feb 11 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.0-5
- rebuilt with Poppler 25.02.0

* Tue Feb 11 2025 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.0-4
- fix important issues reported by OSH

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Nov 01 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1.0-1
- libcupsfilters-2.1.0 is available (fedora#2319558)

* Thu Sep 26 2024 Justin M. Forbes <jforbes@fedoraproject.org> - 1:2.1~b1-3
- Fix for CVE-2024-47076

* Thu Aug 22 2024 Marek Kasik <mkasik@redhat.com> - 1:2.1~b1-2
- Rebuild for poppler 24.08.0

* Thu Aug 15 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.1~b1-1
- 2305074 - libcupsfilters-2.1b1 is available

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Mar 11 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-7
- 2266609 - fix color printing via URF to driverless printer

* Tue Feb 20 2024 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-6
- fix several issues reported in upstream

* Mon Jan 29 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Oct 19 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-2
- rebuilt for side-tag with libppd

* Tue Oct 03 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0.0-1
- 2240388 - libcupsfilters-2.0.0 is available

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1:2.0~rc2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Wed Jun 28 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~rc2-1
- 2.0rc2

* Wed Apr 19 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~rc1-1
- 2.0rc1

* Wed Mar 01 2023 Zdenek Dohnal <zdohnal@redhat.com> - 1:2.0~b4-1
- (fedora#2173137) - libcupsfilters-2.0b4 is available
- introduce Epoch because I'm not careful reader of FPG...

* Mon Feb 20 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2.0b3-4
- rebuilt with obsoletes
- fix define in image-png.c to enable PNG support

* Mon Feb 20 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2.0b3-3
- fix double free caused by coverity fix

* Wed Feb 15 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2.0b3-2
- remove Obsoletes for now

* Tue Jan 31 2023 Zdenek Dohnal <zdohnal@redhat.com> - 2.0b3-1
- Initial import
