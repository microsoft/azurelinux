# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global mingw_build_ucrt64 1
# The mingw-w64-headers provide the headers pthread_time.h
# and pthread_unistd.h by default and are dummy headers.
# The real implementation for these headers is in a separate
# library called winpthreads. As long as winpthreads isn't
# build, the flag below needs to be set to 1. When winpthreads
# is available then this flag needs to be set to 0 to avoid
# a file conflict with the winpthreads headers.
%global bundle_dummy_pthread_headers 0

Name:           mingw-headers
Version:        13.0.0
Release: 3%{?dist}
Summary:        Win32/Win64 header files

License:        BSD-3-Clause AND LGPL-2.0-or-later AND LGPL-2.1-or-later AND GPL-2.0-or-later AND ZPL-2.1 AND MIT-Khronos-old AND LicenseRef-Fedora-Public-Domain
URL:            http://mingw-w64.sourceforge.net/
Source0:        http://downloads.sourceforge.net/mingw-w64/mingw-w64-v%{version}%{?pre:-%{pre}}.tar.bz2

# Our RPM macros automatically set the environment variable WIDL
# This confuses the mingw-headers configure scripts and causes various
# headers to be regenerated from their .idl source. Prevent this from
# happening as the .idl files shouldn't be used by default
Patch0:         mingw-headers-no-widl.patch

BuildArch:      noarch

BuildRequires: make
BuildRequires: mingw32-filesystem >= 133
BuildRequires: mingw64-filesystem >= 133
BuildRequires: ucrt64-filesystem >= 133


%description
MinGW Windows cross-compiler Win32 and Win64 header files.


%package -n mingw32-headers
Summary:        MinGW Windows cross-compiler Win32 header files
Requires:       mingw32-filesystem >= 95
%if 0%{bundle_dummy_pthread_headers} == 0
Requires:       mingw32-winpthreads
%endif

%description -n mingw32-headers
MinGW Windows cross-compiler Win32 header files.

%package -n mingw64-headers
Summary:        MinGW Windows cross-compiler Win64 header files
Requires:       mingw64-filesystem >= 95
%if 0%{bundle_dummy_pthread_headers} == 0
Requires:       mingw64-winpthreads
%endif

%description -n mingw64-headers
MinGW Windows cross-compiler Win64 header files.

%package -n ucrt64-headers
Summary:        MinGW Windows cross-compiler Win64 header files
Requires:       ucrt64-filesystem >= 133
%if 0%{bundle_dummy_pthread_headers} == 0
Requires:       ucrt64-winpthreads
%endif

%description -n ucrt64-headers
MinGW Windows cross-compiler Win64 header files.


%prep
%autosetup -p1 -n mingw-w64-v%{version}%{?pre:-%{pre}}


%build
export MINGW32_CONFIGURE_ARGS="--with-default-msvcrt=msvcrt"
export MINGW64_CONFIGURE_ARGS="--with-default-msvcrt=msvcrt"
export UCRT64_CONFIGURE_ARGS="--with-default-msvcrt=ucrt"

pushd mingw-w64-headers
    %mingw_configure --enable-sdk=all --enable-idl
popd


%install
pushd mingw-w64-headers
    %mingw_make_install
popd

# Drop the dummy pthread headers if necessary
%if 0%{?bundle_dummy_pthread_headers} == 0
rm -f %{buildroot}%{mingw32_includedir}/pthread_signal.h
rm -f %{buildroot}%{mingw32_includedir}/pthread_time.h
rm -f %{buildroot}%{mingw32_includedir}/pthread_unistd.h
rm -f %{buildroot}%{mingw64_includedir}/pthread_signal.h
rm -f %{buildroot}%{mingw64_includedir}/pthread_time.h
rm -f %{buildroot}%{mingw64_includedir}/pthread_unistd.h
rm -f %{buildroot}%{ucrt64_includedir}/pthread_signal.h
rm -f %{buildroot}%{ucrt64_includedir}/pthread_time.h
rm -f %{buildroot}%{ucrt64_includedir}/pthread_unistd.h
%endif


%files -n mingw32-headers
%license COPYING DISCLAIMER DISCLAIMER.PD
%{mingw32_includedir}/*

%files -n mingw64-headers
%license COPYING DISCLAIMER DISCLAIMER.PD
%{mingw64_includedir}/*

%files -n ucrt64-headers
%license COPYING DISCLAIMER DISCLAIMER.PD
%{ucrt64_includedir}/*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 13.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Sun Jul 13 2025 Sandro Mani <manisandro@gmail.com> - 13.0.0-1
- Update to 13.0.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 24 2024 Sandro Mani <manisandro@gmail.com> - 12.0.0-3
- Pass --with-default-msvcrt=msvcrt when building mingw32/64-headers

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Sandro Mani <manisandro@gmail.com> - 12.0.0-1
- Update to 12.0.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 17 2023 Sandro Mani <manisandro@gmail.com> - 11.0.1-1
- Update to 11.0.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 11.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 30 2023 Sandro Mani <manisandro@gmail.com> - 11.0.0-1
- Update to 11.0.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 10.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed May 04 2022 Sandro Mani <manisandro@gmail.com> - 10.0.0-3
- Rebuild (bundle_dummy_pthread_headers=0)

* Tue May 03 2022 Sandro Mani <manisandro@gmail.com> - 10.0.0-2
- Build with dummy pthread headers
- Spec cleanups

* Tue Apr 26 2022 Sandro Mani <manisandro@gmail.com> - 10.0.0-1
- Update to 10.0.0

* Wed Mar 02 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 9.0.0-6
- Add ucrt64 target (bundle_dummy_pthread_headers=0, +Requires: winpthread)

* Wed Feb 23 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 9.0.0-5
- Add ucrt64 target (bundle_dummy_pthread_headers=0, -Requires: winpthread)

* Wed Feb 23 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 9.0.0-4
- Add ucrt64 target (bundle_dummy_pthread_headers=1)

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Sandro Mani <manisandro@gmail.com> - 9.0.0-1
- Update to 9.0.0

* Mon May 17 2021 Sandro Mani <manisandro@gmail.com> - 8.0.2-1
- Update to 8.0.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Sandro Mani <manisandro@gmail.com> - 8.0.0-1
- Update to 8.0.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 20 2020 Sandro Mani <manisandro@gmail.com> - 7.0.0-1
- Update to 7.0.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue May 07 2019 Sandro Mani <manisandro@gmail.com> - 6.0.0-1
- Update to 6.0.0

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Kalev Lember <klember@redhat.com> - 5.0.4-1
- Update to 5.0.4

* Thu Jun 14 2018 Sandro Mani <manisandro@gmail.com> - 5.0.3-1
- Update to 5.0.3

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed May 17 2017 Kalev Lember <klember@redhat.com> - 5.0.2-1
- Update to 5.0.2

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Kalev Lember <klember@redhat.com> - 5.0.1-1
- Update to 5.0.1

* Wed Oct 26 2016 Kalev Lember <klember@redhat.com> - 5.0.0-1
- Update to 5.0.0
- Don't set group tags
- Use license macro

* Sat Jul 23 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0-0.2.rc2.v5.x.git65a0c3.20160723
- Update to 20160204 snapshot of the v5.x branch (git rev 65a0c3)
- Backported patch to build failure of latest wine-gecko

* Sun Mar 27 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0-0.1.rc2
- Update to 5.0rc2

* Thu Feb  4 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.999-0.3.trunk.git38410a.20160204
- Update to 20160204 snapshot (git rev 38410a)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.999-0.2.trunk.git5e2e73.20151224
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.999-0.1.trunk.git.5e2e73.20151224
- Update to 20151224 snapshot (git rev 5e2e73)

* Fri Aug 14 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.4-3
- Backport more commits which are required to build wine-gecko 2.40

* Fri Aug  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.4-2
- Backport commit 5f5e2c (duplicate defines in activscp.h)
  as it is required by mingw-qt5-qtactiveqt 5.5.0

* Wed Aug  5 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4
- Backport various commits which are required by wine-gecko 2.40-beta1

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2
- Backport fix for shlobj.h regression (RHBZ #1213843)

* Sun Mar 29 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1

* Sat Mar 21 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0

* Sat Mar  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0-0.3.rc3
- Update to 4.0rc3

* Wed Jan 28 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0-0.2.rc1
- Fix localtime_s and asctime_s compatibility issue

* Mon Jan 26 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0-0.1.rc1
- Update to 4.0rc1

* Mon Dec 22 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.5.trunk.git.f7337b.20141222
- Update to 20141222 snapshot (git rev f7337b)

* Tue Dec  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.4.trunk.git.dadc8f.20141209
- Update to 20141209 snapshot (git rev dadc8f)

* Fri Dec  5 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.3.trunk.git.63dba2.20141205
- Update to 20141205 snapshot (git rev 63dba2)

* Wed Dec  3 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.2.trunk.git.a5c151.20141203
- Update to 20141203 snapshot (git rev a5c151)

* Fri Sep 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.1.trunk.git.b08afb.20140912
- Update to 20140912 snapshot (git rev b08afb)
- Bump version as upstream released mingw-w64 v3.2.0 recently (which is not based on the trunk branch)

* Wed Jul 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.12.trunk.gitec1ff7.20140730
- Update to 20140730 snapshot (git rev ec1ff7)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.999-0.11.trunk.gitb8e816.20140530
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.10.trunk.gitb8e8160.20140530
- Update to 20140530 snapshot (git rev b8e8160)
- Fixes initializer issue in IN6ADDR macros (RHBZ #1067426)

* Sat May 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.9.trunk.git502c72.20140524
- Update to 20140524 snapshot (git rev 502c72)
- Upstream has switched from SVN to Git

* Sun Mar 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.8.trunk.r6559.20140330
- Update to r6559 (20140330 snapshot)
- Prevent headers to be regenerated from IDL
  Fixes build failure when the environment variable WIDL is set
  (which happens automatically when mingw-w64-tools is installed)

* Mon Feb 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.7.trunk.r6497.20140224
- Update to r6497 (20140224 snapshot)

* Tue Feb 11 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.6.trunk.r6479.20140211
- Update to r6479 (20140211 snapshot)
- Fixes another math.h issue

* Mon Feb 10 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.5.trunk.r6477.20140210
- Update to r6477 (20140210 snapshot)
- Fixes broken math.h when using C++ (RHBZ #1061443)

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.4.trunk.r6475.20140208
- Update to r6475 (20140208 snapshot)

* Sun Jan 26 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.3.trunk.r6469.20140126
- Update to r6469 (20140126 snapshot)

* Fri Jan 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.2.trunk.r6460.20140124
- Update to r6460 (20140124 snapshot)

* Thu Jan  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.1.trunk.r6432.20140104
- Bump version to keep working upgrade path

* Sat Jan  4 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.3.trunk.r6432.20140104
- Update to r6432 (20140104 snapshot)

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.2.trunk.r6388.20131129
- Update to r6388 (20131129 snapshot)
- Fixes compile failure in mingw-qt5-qtserialport (regarding setupapi.h header)

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.1.trunk.r6379.20131120
- Update to r6379 (20131120 snapshot)

* Fri Sep 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0
- Enable support for winpthreads (F20+)

* Sat Sep 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.38.trunk.r6284.20130914
- Update to r6284 (20130914 snapshot)
- Fixes 'VARIANT' has no member named 'bstrVal' errors (mingw-tk)
- Fixes 'VARIANT' has no member named 'vt' errors (mingw-tk)

* Wed Sep 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.37.trunk.r6277.20130911
- Update to r6277 (20130911 snapshot)
- Fixes multiple definition of IDListContainerIsConsistent failures
- Fixes unknown type name 'EXCEPTION_REGISTRATION' failures

* Mon Sep  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.36.trunk.r6258.20130909
- Update to r6258 (20130909 snapshot)
- Fixes various UOW related build failures
- Fixed multiple definition of FreeIDListArray failures

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.35.trunk.r6233.20130907
- Update to r6233 (20130907 snapshot)
- Fix compatibility with latest mingw-winpthreads

* Tue Aug 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.34.trunk.r6155.20130827
- Update to r6155 (20130827 snapshot)
- Fixes duplicate declaration of PRINTEROP_FLAGS (mingw-nsis)
- Fixes duplicate declaration of THREAD_INFORMATION_CLASS (mingw-wine-gecko)
- Fixes "unknown type name 'LPINITIALIZESPY'" failure in objbase.h

* Mon Aug 19 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.33.trunk.r6106.20130819
- Update to r6106 (20130819 snapshot)
- Resolves mingw-gettext build failure (invalid EnumResourceLanguages declaration)

* Sat Aug 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.32.trunk.r6069.20130810
- Update to r6069 (20130810 snapshot)
- Resolves unnecesary dependency on libgcc_s_sjlj-1.dll for the i686 target

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.999-0.31.trunk.r5969.20130721
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.30.trunk.r5969.20130721
- Update to r5969 (20130721 snapshot)
- Resolves mingw-boost failure for the i686 target (regarding Interlocked* symbols)

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.29.trunk.r5949.20130713
- Update to r5949 (20130713 snapshot)

* Fri Jun 28 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.28.trunk.r5915.20130628
- Update to r5915 (20130628 snapshot)

* Fri Jun 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.27.trunk.r5904.20130614
- Update to r5904 (fixes various regressions)

* Fri Jun 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.26.trunk.r5894.20130614
- Update to r5894 (20130614 snapshot)
- Updated instructions to regenerate snapshots
  (SourceForge has changed their SVN infrastructure)

* Thu May 30 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.25.trunk.20130530
- Update to 20130530 snapshot

* Mon May 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.24.trunk.20130520
- Update to 20130520 snapshot

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.23.trunk.20130509
- Regenerated 20130509 snapshot
- Contains patch from RHBZ #917400

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.22.trunk.20130509
- Update to 20130509 snapshot

* Sun Apr 28 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.21.trunk.20130428
- Update to 20130428 snapshot
- Fixes build regression in gettext regarding asprinf

* Thu Apr 25 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.20.trunk.20130425
- Update to 20130425 snapshot

* Wed Apr  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.19.trunk.20130403
- Update to 20130403 snapshot

* Sat Feb 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.18.trunk.20130216
- Update to 20130216 snapshot
- Includes improved import libraries (for setupapi, cfgmgr32 and others)

* Sun Jan 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.17.trunk.20130127
- Update to 20130127 snapshot

* Sat Jan  5 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.16.trunk.20130105
- Update to 20130105 snapshot

* Sat Nov 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.15.trunk.20121110
- Update to 20121110 snapshot
- Fixes build issue with DirectWrite support in mingw-qt5-qtbase

* Fri Nov  9 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.14.trunk.20121109
- Update to 20121109 snapshot

* Tue Oct 16 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.13.trunk.20121016
- Update to 20121016 snapshot
- Use a different source tarball which doesn't contain unrelevant code (like libiberty)
- Removed Provides: bundled(libiberty)

* Mon Oct 15 2012 Jon Ciesla <limburgher@gmail.com> - 2.0.999-0.12.trunk.20121006
- Provides: bundled(libiberty)

* Sat Oct  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.11.trunk.20121006
- Update to 20121006 snapshot

* Wed Jul 18 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.10.trunk.20120718
- Update to 20120718 snapshot

* Fri Jul 13 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.9.trunk.20120713
- Update to 20120713 snapshot

* Mon Jul 09 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.8.trunk.20120709
- Update to 20120709 snapshot (contains full Cygwin support)
- Eliminated various manual kludges as upstream now installs their
  files to the correct folders by default

* Thu Jul 05 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.7.trunk.20120705
- Update to 20120705 snapshot (contains various Cygwin changes)

* Sat Jun 02 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.6.trunk.20120601
- Update to 20120601 snapshot

* Sat Mar 03 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.5.trunk.20120224
- Bump EVR to fix upgrade path when upgrading from the testing repository

* Fri Feb 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.4.trunk.20120224
- Update to 20120224 snapshot
- Eliminated some conditionals related to snapshot builds
- Added DISCLAIMER, DISCLAIMER.PD and COPYING.LIB files
- Added ZPLv2.1 to the license tag
- Added a conditional which is needed to prevent a file conflict with winpthreads
- Bumped BR: mingw{32,64}-filesystem to >= 95

* Fri Feb 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.3.trunk.20120120
- Use smaller SourceForge source URLs
- Dropped the mingw_pkg_name global
- Dropped the quotes in the mingw_configure and mingw_make_install calls
- Improved summary of the various packages

* Fri Jan 20 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.2.trunk.20120120
- Update to mingw-w64 trunk 20120120 snapshot (fixes various errno related compile failures)

* Thu Jan 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.1.trunk.20120112
- Update to mingw-w64 trunk 20120112 snapshot

* Sat Nov 19 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-1
- Update to mingw-w64 v2.0.1

* Sat Oct 22 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-1
- Update to mingw-w64 v2.0

* Sun Sep 25 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.3.rc1
- Bumped obsoletes for mingw32-w32api
- Dropped unneeded RPM tags

* Sat Aug 13 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.2.rc1
- Rebuild because of broken mingw-find-requires.sh in the mingw-filesystem package

* Mon Aug  8 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.1.rc1
- Update to 2.0-rc1

* Tue Jul 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.12.20110711.trunk
- Backported a patch for a regression which causes CLSID_ShellLink to be defined twice
  This fixes compilation of gtk3

* Tue Jul 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.11.20110711.trunk
- Update to 20110711 snapshot of the trunk branch

* Sat Jun 25 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.10.20110625.trunk
- Update to 20110625 snapshot of the trunk branch (fixes gstreamer d3d issue)

* Thu Jun  9 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.9.20110609.trunk
- Update to 20110609 snapshot of the trunk branch

* Thu Apr 14 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.8.20110413.trunk
- Update to 20110413 snapshot of the trunk branch
- Made the package compliant with the new packaging guidelines
- Enable the secure API (required for wine-gecko)

* Wed Jan 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.7.20101003
- Update to 20101003 snapshot
- Generate per-target RPMs
- Bundle the COPYING file

* Fri Dec 24 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.6.20100914
- Replaced my patch by an upstreamed one

* Fri Oct  8 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.5.20100914
- Bundle the DDK and DirectX headers as well

* Wed Sep 29 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.4.20100914
- Update to 20100914 snapshot
- Renamed the package to mingw-headers
- Obsoletes/provides the mingw32-w32api package

* Sat May 15 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.3.20100513
- The 20100513 snapshot contains a bug where #include <malloc.h>
  doesn't result in declaring the symbols _aligned_malloc and _aligned_free
  Added a patch to fix this

* Fri May 14 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.2.20100513
- Rebuild for new mingw64-filesystem

* Fri May 14 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.1.20100513
- Update to 20100513 snapshot of the 1.0 branch
- Updated Source: URL
- Rewritten the %%build and %%install phases
- Fixed %%defattr tag
- Use the default path which GCC expects for the headers

* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.svn607.10
- Started mingw64 development.

* Mon Dec 15 2008 Richard W.M. Jones <rjones@redhat.com> - 3.13-1
- New upstream version 3.13.

* Tue Dec  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-8
- Force rebuild to get rid of the binary bootstrap package and replace
  with package built from source.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-7
- No runtime dependency on binutils or gcc.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-6
- Rebuild against latest filesystem package.
- Rewrite the summary for accuracy and brevity.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-4
- Remove obsoletes for a long dead package.
- Enable _mingw32_configure (Levente Farkas).

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-3
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-2
- Rebuild against mingw32-filesystem 36

* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 3.12-1
- New upstream version 3.12.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-7
- Rename mingw -> mingw32.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-6
- Moved ole provides to mingw-filesystem package.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-3
- Use the RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.11-2
- Initial RPM release, largely based on earlier work from several sources.
