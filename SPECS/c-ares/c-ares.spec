# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global use_cmake 1

Summary: A library that performs asynchronous DNS operations
Name: c-ares
Version: 1.34.6
Release: 1%{?dist}
License: MIT
URL: http://c-ares.org/
Source0: https://github.com/c-ares/c-ares/releases/download/v%{version}/c-ares-%{version}.tar.gz
BuildRequires: gcc
%if %{use_cmake}
BuildRequires: cmake
%else
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
%endif
BuildRequires: make

%description
c-ares is a C library that performs DNS requests and name resolves
asynchronously. c-ares is a fork of the library named 'ares', written
by Greg Hudson at MIT.

%package devel
Summary: Development files for c-ares
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files and libraries needed to
compile applications or shared objects that use c-ares.

%prep
%autosetup -p1

# f=CHANGES ; iconv -f iso-8859-1 -t utf-8 $f -o $f.utf8 ; mv $f.utf8 $f

%build
# autoreconf -if
# %%configure --enable-shared --disable-static \
#            --disable-dependency-tracking
%if %{use_cmake}
%{cmake} -DCARES_BUILD_TOOLS:BOOL=OFF
%cmake_build
%else
autoreconf -if
%configure --enable-shared --disable-static \
           --disable-dependency-tracking
%{__make} %{?_smp_mflags}
%endif

%install
%if %{use_cmake}
%cmake_install
%else
%make_install
rm -f $RPM_BUILD_ROOT/%{_libdir}/libcares.la
%endif

%ldconfig_scriptlets

%files
%license LICENSE.md
%doc README.md RELEASE-NOTES.md
%{_libdir}/*.so.*

%files devel
%{_includedir}/ares.h
%{_includedir}/ares_build.h
%{_includedir}/ares_dns.h
%{_includedir}/ares_dns_record.h
%{_includedir}/ares_nameser.h
# %%{_includedir}/ares_rules.h
%{_includedir}/ares_version.h
%{_libdir}/*.so
%if %{use_cmake}
%{_libdir}/cmake/c-ares/
%endif
%{_libdir}/pkgconfig/libcares.pc
%{_mandir}/man3/ares_*

%changelog
* Wed Dec 17 2025 Tom Callaway <spot@fedoraproject.org> - 1.34.6-1
- update to 1.34.6
- fixes CVE-2025-62408 (among other fixes)

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Apr  8 2025 Tom Callaway <spot@fedoraproject.org> - 1.34.5-1
- update to 1.34.5

* Fri Feb 14 2025 Tom Callaway <spot@fedoraproject.org> - 1.34.4-3
- fix pkgconfig file (do not need to mess with cmake for libdir)

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.34.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Dec 14 2024 Tom Callaway <spot@fedoraproject.org> - 1.34.4-1
- update to 1.34.4

* Fri Oct 18 2024 Tom Callaway <spot@fedoraproject.org> - 1.34.2-1
- update to 1.34.2

* Wed Aug  7 2024 Tom Callaway <spot@fedoraproject.org> - 1.33.0-1
- update to 1.33.0

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.31.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Jul  1 2024 Tom Callaway <spot@fedoraproject.org> - 1.31.0-1
- update to 1.31.0

* Mon Jun 10 2024 Tom Callaway <spot@fedoraproject.org> - 1.30.0-1
- update to 1.30.0

* Sun Mar 31 2024 Tom Callaway <spot@fedoraproject.org> - 1.28.1-1
- update to 1.28.1

* Fri Mar 29 2024 Tom Callaway <spot@fedoraproject.org> - 1.28.0-1
- update to 1.28.0

* Tue Jan 23 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.25.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Tom Callaway <spot@fedoraproject.org> - 1.25.0-1
- update to 1.25.0

* Tue Nov 21 2023 Tom Callaway <spot@fedoraproject.org> - 1.22.1-1
- update to 1.22.1

* Sun Nov  5 2023 Tom Callaway <spot@fedoraproject.org> - 1.21.0-1
- update to 1.21.0

* Wed May 24 2023 Tom Callaway <spot@fedoraproject.org> - 1.19.1-1
- update to 1.19.1
- fixes CVE-2023-32067

* Fri Feb 17 2023 Tom Callaway <spot@fedoraproject.org> - 1.19.0-1
- update to 1.19.0
- fixes CVE-2022-4904

* Wed Jan 18 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Mon Aug 16 2021 Tom Callaway <spot@fedoraproject.org> - 1.17.2-1
- update to 1.17.2
- fixes multiple security issues including CVE-2021-3672

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.17.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 20 2020 Tom Callaway <spot@fedoraproject.org> - 1.17.1-1
- update to 1.17.1

* Tue Nov 17 2020 Tom Callaway <spot@fedoraproject.org> - 1.17.0-1
- update to 1.17.0

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.16.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.16.1-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Mon May 11 2020 Tom Callaway <spot@fedoraproject.org> - 1.16.1-1
- update to 1.16.1

* Fri Mar 13 2020 Tom Callaway <spot@fedoraproject.org> - 1.16.0-1
- update to 1.16.0

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 12 2019 Tom Callaway <spot@fedoraproject.org> - 1.15.0-3
- use cmake to build so we get cmake helpers (bz1687844)

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.15.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Nov 13 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.16.0-1
- Update to the latest upstream

* Mon Sep  3 2018 Jakub Hrozek <jhrozek@redhat.com> - 1.14.0-1
- Update to the latest upstream
- Resolves: rhbz#1624499 - RFE: New c-ares release 1.14.0 available

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.13.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 20 2017 Jakub Hrozek <jhrozek@redhat.com> - 1.13.0-1
- update to 1.13.0

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Sep 29 2016 Tom Callaway <spot@fedoraproject.org> - 1.12.0-1
- update to 1.12.0

* Fri Feb 19 2016 Jakub Hrozek <jhrozek@redhat.com> - 1.11.0
- New upstream version 1.11.0

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.10.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.10.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

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

