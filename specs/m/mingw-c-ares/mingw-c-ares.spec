# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-c-ares
Version:        1.17.2
Release: 13%{?dist}
Summary:        Library that performs asynchronous DNS operations

# ares_getopt.c ares_getopt.h are BSD (3 clause)
# bitncmp.c inet_net_pton.c inet_ntop.c are ISC
# rest is MIT
# Automatically converted from old format: MIT and BSD and ISC - review is highly recommended.
License:        LicenseRef-Callaway-MIT AND LicenseRef-Callaway-BSD AND ISC
URL:            http://c-ares.haxx.se/
Source0:        http://c-ares.haxx.se/download/c-ares-%{version}.tar.gz
Patch0:         0001-Use-RPM-compiler-options.patch
# Don't fail on -lssp in LDFLAGS
# It's probably true that -lxxx belongs to LIBS, but we don't have that in the mingw macros,
# and no-one else seems to care with link libs are added to LDFLAGS
Patch1:         mingw-c-ares_libs-in-ldflags.patch

BuildArch:      noarch

BuildRequires:  make
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-binutils

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-binutils

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.


%package -n mingw32-c-ares
Summary:        %{summary}

%description -n mingw32-c-ares
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

This package is MinGW compiled c-ares library for the Win32 target.


%package -n mingw64-c-ares
Summary:        %{summary}

%description -n mingw64-c-ares
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

This package is MinGW compiled c-ares library for the Win64 target.


%{?mingw_debug_package}


%prep
%setup -q -n c-ares-%{version}
%patch -P0 -p1 -b .optflags
%patch -P1 -p1 -b .ldflags


%build
autoreconf -if
%mingw_configure --enable-shared --disable-static \
                 --disable-dependency-tracking
%mingw_make %{?_smp_mflags}


%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT
# remove libtool files
rm -f ${RPM_BUILD_ROOT}%{mingw32_libdir}/libcares.la
rm -f ${RPM_BUILD_ROOT}%{mingw64_libdir}/libcares.la
# remove documentation (it's in the native version)
rm -rf ${RPM_BUILD_ROOT}%{mingw32_mandir}
rm -rf ${RPM_BUILD_ROOT}%{mingw64_mandir}


%files -n mingw32-c-ares
%license LICENSE.md
%{mingw32_bindir}/*.dll
%{mingw32_includedir}/ares.h
%{mingw32_includedir}/ares_build.h
%{mingw32_includedir}/ares_dns.h
%{mingw32_includedir}/ares_rules.h
%{mingw32_includedir}/ares_version.h
%{mingw32_libdir}/*.dll.a
%{mingw32_libdir}/pkgconfig/libcares.pc

%files -n mingw64-c-ares
%license LICENSE.md
%{mingw64_bindir}/*.dll
%{mingw64_includedir}/ares.h
%{mingw64_includedir}/ares_build.h
%{mingw64_includedir}/ares_dns.h
%{mingw64_includedir}/ares_rules.h
%{mingw64_includedir}/ares_version.h
%{mingw64_libdir}/*.dll.a
%{mingw64_libdir}/pkgconfig/libcares.pc


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.17.2-10
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.17.2-3
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Aug 10 2021 František Dvořák <valtri@civ.zcu.cz> - 1.17.2-1
- Update to 1.17.2
- Security fix for CVE-2021-3672

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Sun Feb 14 2021 František Dvořák <valtri@civ.zcu.cz> - 1.17.1-1
- Update to 1.17.1
- Security fix for CVE-2020-8277
- Patch to fix build

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-9
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Jul 23 2017 František Dvořák <valtri@civ.zcu.cz> - 1.13.0-1
- Update to 1.13.0
- Use the license text provided in source tarball
- Conversion to UTF-8 not needed anymore (the file is not used anyway)
- Security fix for CVE-2017-1000381

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 29 2016 František Dvořák <valtri@civ.zcu.cz> - 1.12.0-1
- Update to 1.12.0
- Security fix for CVE-2016-5180

* Tue Mar 08 2016 František Dvořák <valtri@civ.zcu.cz> - 1.11.0-1
- Update to 1.11.0
- Use license macro

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Jan 12 2014 František Dvořák <valtri@civ.zcu.cz> - 1.10.0-2
- Fix license field

* Tue Oct 08 2013 František Dvořák <valtri@civ.zcu.cz> - 1.10.0-1
- Repackage for MinGW

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon May 13 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.10.1-1
- New upstream release 1.10
- Obsolete upstreamed patches
- Amend the multilib patch, there's no need to patch configure since we
  are running autoreconf anyways
- https://raw.github.com/bagder/c-ares/cares-1_10_0/RELEASE-NOTES

* Thu Apr 11 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-6
- Apply an upstream patch to override AC_CONFIG_MACRO_DIR only conditionally

* Thu Apr 11 2013 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-5
- Apply a patch by Stephen Gallagher to patch autoconf, not configure to
  allow optflags to be passed in by build environment
- Run autoreconf before configure
- git rm obsolete patches
- Apply upstream patch to stop overriding AC_CONFIG_MACRO_DIR

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Aug 8 2012 Jakub Hrozek <jhrozek@redhat.com> - 1.9.1-3
- Include URL to the license text

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 25 2012 Tom Callaway <spot@fedoraproject.org> - 1.9.1-1
- update to 1.9.1

* Sat Apr 28 2012 Tom Callaway <spot@fedoraproject.org> - 1.8.0-1
- update to 1.8.0
- fix multilib patch (thanks to Paul Howarth)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 17 2011 Jakub Hrozek <jhrozek@redhat.com> - 1.7.5-1
- New upstream release 1.7.5
- Obsoletes patch #2
- Rebase patch #1 (optflags) to match the 1.7.5 code
- Fixed Source0 URL to point at the upstream tarball

* Mon Apr 11 2011 Jakub Hrozek <jhrozek@redhat.com> - 1.7.4-3
- Apply upstream patch to fix rhbz#695424

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 10 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.4-1
- update to 1.7.4

* Wed Aug 25 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.3-3
- Actually apply the patches

* Wed Aug 25 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.3-2
- apply couple of patches from upstream

* Tue Jun 15 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.3-1
- Upgrade to new upstream release 1.7.3 (obsoletes search/domain patch)
- Fix conflict of -devel packages on multilib architectures (#602880)

* Thu Jun 3 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.1-2
- Use last instance of search/domain, not the first one (#597286)

* Tue Mar 23 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.1-1
- update to 1.7.1 which contains the IPv6 nameserver patch

* Sun Mar  7 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-3
- Change IPv6 nameserver patch according to upstream changes
  (upstream revisions 1199,1201,1202)

* Wed Mar  3 2010 Jakub Hrozek <jhrozek@redhat.com> - 1.7.0-2
- Add a patch to allow usage of IPv6 nameservers

* Tue Dec  1 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.7.0-1
- update to 1.7.0

* Sat Jul 25 2009 Ville Skyttä <ville.skytta at iki.fi> - 1.6.0-3
- Patch to make upstream build system honor our CFLAGS and friends.
- Don't bother building throwaway static libs.
- Disable autotools dependency tracking for cleaner build logs and possible
  slight build speedup.
- Convert docs to UTF-8.
- Update URLs.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6.0-1
- update to 1.6.0

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5.3-1
- update to 1.5.3

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.5.1-2
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.1-1
- update to 1.5.1

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.0-2
- rebuild for ppc32

* Wed Jun 27 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.4.0-1
- bump to 1.4.0 (resolves bugzilla 243591)
- get rid of static library (.a)

* Wed Jan 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.2-1
- bump to 1.3.2

* Mon Sep 11 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-2
- FC-6 bump

* Mon Jul 10 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.1-1
- bump to 1.3.1

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.0-2
- bump for FC-5 rebuild

* Sun Sep  4 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.3.0-1
- include LICENSE text
- bump to 1.3.0

* Tue May 31 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-4
- use dist tag to prevent EVR overlap

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-2
- fix license (MIT, not LGPL)
- get rid of libcares.la

* Fri Apr 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 1.2.1-1
- initial package creation

