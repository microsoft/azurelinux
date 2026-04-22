# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# This package used to be called "google-perftools", but it was renamed on 2012-02-03.

%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name:		gperftools
Version:	2.17.2
Release: 2%{?dist}
License:	BSD-3-Clause
Summary:	Very fast malloc and performance analysis tools
URL:		https://github.com/gperftools/gperftools
Source0:	https://github.com/gperftools/gperftools/releases/download/%{name}-%{version}/%{name}-%{version}.tar.gz
# Conditionalize generic dynamic tls model
Patch1:		gperftools-2.17-disable-generic-dynamic-tls.patch

ExcludeArch:	s390
BuildRequires:  gcc-c++
BuildRequires:	libunwind-devel
BuildRequires:	perl-generators
BuildRequires:	autoconf, automake, libtool
BuildRequires:	make
Requires:	gperftools-devel = %{version}-%{release}
# Requires:	pprof = %%{version}-%%{release}

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly heap-checker,
a heap profiler, and a cpu-profiler.

This is a metapackage which pulls in all of the gperftools binaries,
libraries, and development headers, so that you can use them.

%package devel
Summary:	Development libraries and headers for gperftools
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	google-perftools-devel = %{version}-%{release}
Obsoletes:	google-perftools-devel < 2.0

%description devel
Libraries and headers for developing applications that use gperftools.

%package libs
Summary:	Libraries provided by gperftools
Provides:	google-perftools-libs = %{version}-%{release}
Obsoletes:	google-perftools-libs < 2.0

%description libs
Libraries provided by gperftools, including libtcmalloc and libprofiler.

# Upstream removed pprof.

# %%package -n pprof
# Summary:	CPU and Heap Profiler tool
# Requires:	gv, graphviz
# BuildArch:	noarch
# Provides:	google-perftools = %%{version}-%%{release}
# Obsoletes:	google-perftools < 2.0

# %%description -n pprof
# Pprof is a heap and CPU profiler tool, part of the gperftools suite.

%prep
%setup -q
%autopatch -p1

# Fix end-of-line encoding
sed -i 's/\r//' README_windows.txt

# No need to have exec permissions on source code
chmod -x src/*.h src/*.cc

autoreconf -ifv

%build
CFLAGS=`echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unused-local-typedefs -DTCMALLOC_LARGE_PAGES | sed -e 's|-fexceptions||g'`
CXXFLAGS=`echo $RPM_OPT_FLAGS -fno-strict-aliasing -Wno-unused-local-typedefs -DTCMALLOC_LARGE_PAGES | sed -e 's|-fexceptions||g'`
%configure \
%ifarch aarch64
	--disable-general-dynamic-tls \
%endif
	--disable-dynamic-sized-delete-support \
	--disable-static

# Bad rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Can't build with smp_mflags
make

%install
%make_install docdir=%{_pkgdocdir}/
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

# Delete useless files
rm -rf %{buildroot}%{_pkgdocdir}/INSTALL

%check
# http://code.google.com/p/google-perftools/issues/detail?id=153
%ifnarch ppc
# Their test suite is almost always broken.
# LD_LIBRARY_PATH=./.libs make check
%endif

%ldconfig_scriptlets libs

%files

# %%files -n pprof
# %%license COPYING
# %%{_bindir}/pprof
# %%{_bindir}/pprof-symbolize
# %%{_mandir}/man1/*

%files devel
%{_pkgdocdir}/
# %%{_includedir}/google/
%{_includedir}/gperftools/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files libs
%license COPYING
%{_libdir}/*.so.*

%changelog
* Tue Aug 19 2025 Tom Callaway <spot@fedoraproject.org> - 2.17.2-1
- update to 2.17.2

* Tue Aug  5 2025 Tom Callaway <spot@fedoraproject.org> - 2.17-1
- update to 2.17
- drop pprof subpackage, code removed upstream

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Aug  7 2024 Tom Callaway <spot@fedoraproject.org> - 2.15-4
- include COPYING (bz2295840)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.15-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Fri Jun  7 2024 Tom Callaway <spot@fedoraproject.org> - 2.15-2
- enable general dynamic tls on s390x

* Mon Jun 03 2024 Ken Dreyer <kdreyer@ibm.com> - 2.15-1
- update to 2.15 (rhbz#2256996)
- drop upstreamed patch

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.14-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan  3 2024 Tom Callaway <spot@fedoraproject.org> - 2.14-1
- update to 2.14

* Thu Nov  2 2023 Ismail Doenmez <idoenmez@amazon.com> - 2.13-1
- Update to 2.13
- Add a fix for printing stack traces on recent aarch64 cpus

* Wed Aug  9 2023 Tom Callaway <spot@fedoraproject.org> - 2.10-1
- update to 2.10

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Mar  3 2021 Tom Callaway <spot@fedoraproject.org> - 2.9.1-1
- update to 2.9.1

* Mon Feb 22 2021 Tom Callaway <spot@fedoraproject.org> - 2.9.0-1
- update to 2.9.0

* Mon Feb 15 2021 Tom Callaway <spot@fedoraproject.org> - 2.8.90-1
- update to 2.8.90

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Dec 30 2020 Tom Callaway <spot@fedoraproject.org> - 2.8.1-1
- update to 2.8.1

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 14 2020 Tom Stellard <tstellar@redhat.com> - 2.8-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Thu Jul  9 2020 Tom Callaway <spot@fedoraproject.org> - 2.8-1
- update to 2.8

* Wed Apr 15 2020 Dan Horák <dan[at]danny.cz> - 2.7.90-2
- build with libunwind on s390x

* Mon Mar  9 2020 Tom Callaway <spot@fedoraproject.org> - 2.7.90-1
- update to 2.7.90

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan  8 2019 Tom Callaway <spot@fedoraproject.org> - 2.7-4
- drop rsp clobber, which breaks gcc9 (thanks to Jeff Law)

* Tue Jul 24 2018 Tom Callaway <spot@fedoraproject.org> - 2.7-3
- everyone needs BuildRequires:  gcc-c++, including s390x

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue May  1 2018 Tom Callaway <spot@fedoraproject.org> - 2.7-1
- update to 2.7

* Sun Mar 25 2018 Tom Callaway <spot@fedoraproject.org> - 2.6.90-1
- update to 2.6.90

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jan 11 2018 Tom Callaway <spot@fedoraproject.org> - 2.6.3-1
- update to 2.6.3

* Wed Oct 11 2017 Tom Callaway <spot@fedoraproject.org> - 2.6.1-5
- add aligned_alloc support

* Thu Aug 24 2017 Tom Callaway <spot@fedoraproject.org> - 2.6.1-4
- add configure option to disable generic dynamic tls model
- disable generic dynamic tls model on s390x and aarch64

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Jul 17 2017 Tom Callaway <spot@fedoraproject.org> - 2.6.1-1
- update to 2.6.1

* Tue May 23 2017 Tom Callaway <spot@fedoraproject.org> - 2.5.93-1
- update to 2.5.93
- disable dynamic sized delete (explicitly) always

* Mon May 22 2017 Tom Callaway <spot@fedoraproject.org> - 2.5.92-1
- update to 2.5.92
- disable dynamic sized delete support on powerpc64

* Mon May 22 2017 Richard W.M. Jones <rjones@redhat.com> - 2.5.91-2
- Bump release and rebuild to try to fix _ZdlPvm symbol (see RHBZ#1452813).

* Mon May 15 2017 Tom Callaway <spot@fedoraproject.org> - 2.5.91-1
- update to 2.5.91

* Tue Feb 21 2017 Dan Horák <dan[at]danny.cz> - 2.5-5
- fix s390x build

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 12 2017 Tom Callaway <spot@fedoraproject.org> - 2.5-3
- enable s390x

* Thu Apr 28 2016 Peter Robinson <pbrobinson@fedoraproject.org> 2.5-2
- Power64 has libunwind now

* Tue Apr 26 2016 Tom Callaway <spot@fedoraproject.org> - 2.5-1
- update to 2.5

* Tue Mar  8 2016 Tom Callaway <spot@fedoraproject.org> - 2.4.91-1
- update to 2.4.91
- re-enable hardened builds (upstream disabled dynamic sized delete by default)

* Fri Mar 04 2016 Than Ngo <than@redhat.com> - 2.4.90-3
- Disable hardened build on ppc64/ppc64le (RHBZ#1314483).

* Mon Feb 29 2016 Richard W.M. Jones <rjones@redhat.com> - 2.4.90-2
- Disable hardened build on 32 bit ARM (RHBZ#1312462).

* Mon Feb 22 2016 Tom Callaway <spot@fedoraproject.org> - 2.4.90-1
- update to 2.4.90

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  9 2015 Tom Callaway <spot@fedoraproject.org> - 2.4-4
- fix modern futex handling (thanks to Paolo Bonzini)

* Mon Jun  1 2015 Tom Callaway <spot@fedoraproject.org> - 2.4-3
- enable futex for ARM

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 2.4-2
- Rebuilt for GCC 5 C++11 ABI change

* Fri Mar 27 2015 Tom Callaway <spot@fedoraproject.org> 2.4-1
- update to 2.4

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Jul 10 2014 Dan Horák <dan[at]danny.cz> -  2.2.1-1
- Update to new upstream 2.2.1 release
- Fixes build on ppc arches

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Jun  4 2014 Peter Robinson <pbrobinson@fedoraproject.org> 2.2-1
- Update to new upstream 2.2 release
- Add support for new arches (aarch64, ppc64le, mips)

* Tue May 13 2014 Jaromir Capik <jcapik@redhat.com> - 2.1-5
- Replacing ppc64 with the power64 macro (#1077632)

* Sat Jan  4 2014 Tom Callaway <spot@fedoraproject.org> - 2.1-4
- re-enable FORTIFY_SOURCE

* Fri Dec  6 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.1-3
- Install docs to %%{_pkgdocdir} where available (#993798), include NEWS.
- Fix bogus date in %%changelog.

* Sat Aug 03 2013 Petr Pisar <ppisar@redhat.com> - 2.1-2
- Perl 5.18 rebuild

* Wed Jul 31 2013 Tom Callaway <spot@fedoraproject.org> - 2.1-1
- update to 2.1 (fixes arm)
- disable -fexceptions, as that breaks things on el6, possibly arm

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 2.0-12
- Perl 5.18 rebuild

* Tue Jun  4 2013 Tom Callaway <spot@fedoraproject.org> - 2.0-11
- pass -fno-strict-aliasing
- create "gperftools" metapackage.
- update to svn r218 (cleanups, some ARM fixes)

* Thu Mar 14 2013 Dan Horák <dan[at]danny.cz> - 2.0-10
- build on ppc64 as well

* Fri Mar  1 2013 Tom Callaway <spot@fedoraproject.org> - 2.0-9
- update to svn r190 (because google can't make releases)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Aug  3 2012 Tom Callaway <spot@fedoraproject.org> - 2.0-7
- fix compile with glibc 2.16

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 2.0-5
- Enable ARM as a supported arch

* Thu Feb 16 2012 Tom Callaway <spot@fedoraproject.org> - 2.0-4
- fix bug in -devel Requires

* Tue Feb 14 2012 Tom Callaway <spot@fedoraproject.org> - 2.0-3
- pprof doesn't actually need gperftools-libs

* Tue Feb 14 2012 Tom Callaway <spot@fedoraproject.org> - 2.0-2
- rework package so that pprof is a noarch subpackage, while still
  enforcing the ExclusiveArch for the libs

* Tue Feb 14 2012 Tom Callaway <spot@fedoraproject.org> - 2.0-1
- rename to gperftools
- update to 2.0

* Wed Jan  4 2012 Tom Callaway <spot@fedoraproject.org> - 1.9.1-1
- update to 1.9.1

* Mon Oct 24 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.3-3
- split libraries out into subpackage to minimize dependencies

* Wed Sep 21 2011 Remi Collet <remi@fedoraproject.org> - 1.8.3-2
- rebuild for new libunwind

* Tue Aug 30 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.3-1
- update to 1.8.3

* Mon Aug 22 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.2-1
- update to 1.8.2

* Thu Jul 28 2011 Tom Callaway <spot@fedoraproject.org> - 1.8.1-1
- update to 1.8.1

* Mon Jul 18 2011 Tom Callaway <spot@fedoraproject.org> - 1.8-1
- update to 1.8

* Wed Jun 29 2011 Tom Callaway <spot@fedoraproject.org> - 1.7-4
- fix tcmalloc compile against current glibc, fix derived from:
  http://src.chromium.org/viewvc/chrome?view=rev&revision=89800

* Thu May 12 2011 Tom Callaway <spot@fedoraproject.org> - 1.7-3
- add Requires: graphviz, gv for pprof

* Fri Mar 11 2011 Dan Horák <dan[at]danny.cz> - 1.7-2
- switch to ExclusiveArch

* Fri Feb 18 2011 Tom Callaway <spot@fedoraproject.org> - 1.7-1
- update to 1.7

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6-2
- fix pprof to work properly with jemalloc (bz 657118)

* Fri Aug  6 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.6-1
- update to 1.6

* Wed Jan 20 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.5-1
- update to 1.5
- disable broken test suite

* Sat Sep 12 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.4-1
- update to 1.4

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-2
- disable tests for ppc, upstream ticket #153

* Thu Jul  2 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-1
- update to 1.3

* Wed May 20 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 1.2-1
- update to 1.2

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.99.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep 22 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.99.1-1
- update to 0.99.1
- previous patches in 0.98-1 were taken upstream

* Mon Aug 25 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0.98-1
- update to 0.98
- fix linuxthreads.c compile (upstream issue 74)
- fix ppc compile (upstream issue 75)
- enable ppc

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.95-4
- Autorebuild for GCC 4.3

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.95-3
- re-disable ppc/ppc64

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.95-2
- ppc/ppc64 doesn't have libunwind

* Tue Feb 19 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.95-1
- 0.95 (all patches taken upstream)
- enable ppc support
- workaround broken ptrace header (no typedef for u32)

* Fri Jan  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0.94.1-1
- bump to 0.94.1
- fix for gcc4.3
- fix unittest link issue

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.93-1
- upstream merged my patch!
- rebuild for BuildID

* Wed Aug  1 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.92-1
- bump to 0.92

* Thu May 17 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-3.1
- excludearch ppc64

* Sun Apr 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-3
- The tests work fine for me locally, but some of them fail inside mock.

* Sun Apr 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-2
- no support for ppc yet

* Mon Apr 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 0.91-1
- alright, lets see if this works now.

* Wed Oct 12 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.3-2
- change group to Development/Tools

* Mon Oct 10 2005 Tom "spot" Callaway <tcallawa@redhat.com> 0.3-1
- initial package for Fedora Extras
