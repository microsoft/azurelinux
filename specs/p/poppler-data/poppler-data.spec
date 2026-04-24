# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# =============================================================================

Name:             poppler-data
Summary:          Encoding files for use with poppler
Version:          0.4.11
Release: 11%{?dist}

# NOTE: The licensing details are explained in COPYING file in source archive.
# Makefile is HPND-sell-variant but is not included in binary package
License:          (GPL-2.0-only OR GPL-3.0-only) AND BSD-3-Clause

URL:              https://poppler.freedesktop.org/
Source:           https://poppler.freedesktop.org/poppler-data-%{version}.tar.gz

BuildArch:        noarch
BuildRequires: make
BuildRequires:    git

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
This package consists of encoding files for use with poppler. The encoding
files are optional and poppler will automatically read them if they are present.

When installed, the encoding files enables poppler to correctly render both CJK
and Cyrrilic characters properly.

# === SUBPACKAGES =============================================================

%package          devel
Summary:          Devel files for %{name}

Requires:         %{name} = %{version}-%{release}
BuildRequires:    pkgconfig

%description devel
This sub-package currently contains only pkgconfig file, which can be used with
pkgconfig utility allowing your software to be build with poppler-data.

# === BUILD INSTRUCTIONS ======================================================

%prep
%autosetup -S git

# NOTE: Nothing to do here - we are packaging the content only.
%build

%install
%make_install prefix=%{_prefix}

# === PACKAGING INSTRUCTIONS ==================================================

%files
%license COPYING COPYING.adobe COPYING.gpl2
%{_datadir}/poppler/

%files devel
%{_datadir}/pkgconfig/poppler-data.pc

# =============================================================================

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sat Jan 18 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jul 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Fri Jan 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Fri Jul 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Jan 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.11-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Sep 10 2021 Rex Dieter <rdieter@fedoraproject.org> - 0.4.11-1
- 0.4.11 (#1890347)

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jan 30 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Apr 25 2018 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.4.9-1
- rebase to latest upstream version (bug #1571487)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Nov 15 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.4.8-4
- specfile cleanup according to Fedora Packaging Guidelines
- ghostscript parts removed from specfile

* Thu Nov 09 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.4.8-3
- Rebuilt again (buildroot override was not yet in effect)

* Thu Nov 09 2017 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.4.8-2
- Rebuilt because of ghostscript-9.22 rebase

* Mon Aug 14 2017 Rex Dieter <rdieter@fedoraproject.org> - 0.4.8-1
- 0.4.8 (#1481056)

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec  8 2016 David Kaspar [Dee'Kej] <dkaspar@redhat.com> - 0.4.7-6
- Rebuild because of ghostscript-9.20 rebase (bug #1402306)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Rex Dieter <rdieter@fedoraproject.org> 0.4.7-4
- rebuild for ghostscript-9.16 (#1226627)

* Tue Feb 17 2015 Rex Dieter <rdieter@fedoraproject.org> 0.4.7-3
- rebuild (ghostscript-9.15)

* Tue Sep 23 2014 Rex Dieter <rdieter@fedoraproject.org> 0.4.7-2
- License field should contain GPLv3+ (#949515)

* Thu Aug 14 2014 Rex Dieter <rdieter@fedoraproject.org> 0.4.7-1
- 0.4.7, .spec cleanup

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Oct 21 2013 Rex Dieter <rdieter@fedoraproject.org> 0.4.6-4
- rebuild (ghostscript-9.10)

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.6-1
- poppler-data-0.4.6

* Tue Sep 18 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-6
- create ghostscript cmap symlinks (#842351)

* Sat Sep 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-5
- Identity-UTF16-H too (#842351)

* Sat Sep 15 2012 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-4
- CMap file "Identity-H" missing due to poppler-data change/cleanup (#842351)

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Rex Dieter <rdieter@fedoraproject.org> 0.4.5-1
- poppler-data-0.4.5

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Oct 28 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.4-1
- poppler-data-0.4.4

* Thu Jul 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.3-1
- poppler-data-0.4.3

* Sat May 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 0.4.2-1
- poppler-data-0.4.2

* Mon Dec 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.4.0-1
- poppler-data-0.4.0

* Mon Nov 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.3.1-1
- poppler-data-0.3.1

* Tue Sep 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.3.0-1
- poppler-data-0.3.0
- License: BSD and GPLv2

* Mon Jun 22 2009 Rex Dieter <rdieter@fedoraproject.org> - 0.2.1-1
- first try at separate poppler-data

