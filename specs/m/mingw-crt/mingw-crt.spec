# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global mingw_build_ucrt64 1

%{?mingw_package_header}

# Steps:
# - Perform (scratch) build with bootstrap=1
# - Update the standard-dlls-xxx files as documented below, and rebuild with bootstrap=0
%global bootstrap 0

Name:           mingw-crt
Version:        13.0.0
Release: 3%{?dist}
Summary:        MinGW Windows cross-compiler runtime

License:        LicenseRef-Fedora-Public-Domain AND ZPL-2.1
URL:            http://mingw-w64.sourceforge.net/
Source0:        http://downloads.sourceforge.net/mingw-w64/mingw-w64-v%{version}.tar.bz2


# Note about standard dlls
# ------------------------------------------------------------
#
# We want to be able to build & install mingw32 libraries without
# necessarily needing to install wine.  (And certainly not needing to
# install Windows!)  There is no requirement to have wine installed in
# order to use the mingw toolchain to develop software (i.e. to
# compile more stuff on top of it), so why require that?
#
# So for expediency, this base package provides the "missing" DLLs
# from Windows.  Another way to do it would be to exclude these
# proprietary DLLs in our find-requires checking script - essentially
# it comes out the same either way.
#
# (rpm -ql mingw32-crt | grep '\.a$' | while read f ; do i686-w64-mingw32-dlltool   -I $f 2>/dev/null ; done) | sort | uniq | tr A-Z a-z > standard-dlls-mingw32
Source1:       standard-dlls-mingw32
# (rpm -ql mingw64-crt | grep '\.a$' | while read f ; do x86_64-w64-mingw32-dlltool -I $f 2>/dev/null ; done) | sort | uniq | tr A-Z a-z > standard-dlls-mingw64
Source2:       standard-dlls-mingw64
# (rpm -ql ucrt64-crt | grep '\.a$' | while read f ; do x86_64-w64-mingw32ucrt-dlltool -I $f 2>/dev/null ; done) | sort | uniq | tr A-Z a-z > standard-dlls-ucrt64
Source3:       standard-dlls-ucrt64

BuildArch:      noarch

BuildRequires:  make

BuildRequires:  mingw32-filesystem >= 133
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-headers
BuildRequires:  mingw32-gcc

BuildRequires:  mingw64-filesystem >= 133
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-headers
BuildRequires:  mingw64-gcc

BuildRequires:  ucrt64-filesystem >= 133
BuildRequires:  ucrt64-binutils
BuildRequires:  ucrt64-headers
BuildRequires:  ucrt64-gcc

%description
MinGW Windows cross-compiler runtime, base libraries.


%package -n mingw32-crt
Summary:        MinGW Windows cross-compiler runtime for the win32 target
Requires:       mingw32-filesystem >= 133
%if 0%{?bootstrap:1}
Provides:       %(sed "s/\(.*\)/mingw32(\1) /g" %{SOURCE1} | tr "\n" " ")
Provides:       mingw32(mscoree.dll)
%endif

%description -n mingw32-crt
MinGW Windows cross-compiler runtime, base libraries for the win32 target.

%package -n mingw64-crt
Summary:        MinGW Windows cross-compiler runtime for the win64 target
Requires:       mingw64-filesystem >= 133
%if 0%{?bootstrap:1}
Provides:       %(sed "s/\(.*\)/mingw64(\1) /g" %{SOURCE2} | tr "\n" " ")
Provides:       mingw64(mscoree.dll)
%endif

%description -n mingw64-crt
MinGW Windows cross-compiler runtime, base libraries for the win64 target.

%package -n ucrt64-crt
Summary:        MinGW Windows cross-compiler runtime for the win64 target
Requires:       ucrt64-filesystem >= 133
%if 0%{?bootstrap:1}
Provides:       %(sed "s/\(.*\)/ucrt64(\1) /g" %{SOURCE3} | tr "\n" " ")
Provides:       ucrt64(mscoree.dll)
%endif

%description -n ucrt64-crt
MinGW Windows cross-compiler runtime, base libraries for the win64 target.


%prep
%autosetup -p1 -n mingw-w64-v%{version}


%build
pushd mingw-w64-crt
    # Filter out -fstack-protector and -lssp from LDFLAGS as libssp is not yet potentially built with the bootstrap gcc
    MINGW32_LDFLAGS="`echo %{mingw32_ldflags} | sed 's|-fstack-protector||' | sed 's|-lssp||'`"
    MINGW64_LDFLAGS="`echo %{mingw64_ldflags} | sed 's|-fstack-protector||' | sed 's|-lssp||'`"
    UCRT64_LDFLAGS="`echo %{ucrt64_ldflags} | sed 's|-fstack-protector||' | sed 's|-lssp||'`"
    MINGW32_CONFIGURE_ARGS="--with-default-msvcrt=msvcrt"
    MINGW64_CONFIGURE_ARGS="--disable-lib32 --with-default-msvcrt=msvcrt"
    UCRT64_CONFIGURE_ARGS="--disable-lib32 --with-default-msvcrt=ucrt"
    %mingw_configure
    %mingw_make_build
popd


%install
pushd mingw-w64-crt
    %mingw_make_install
popd

# Dunno what to do with these files
rm -rf %{buildroot}%{mingw32_includedir}/*.c
rm -rf %{buildroot}%{mingw64_includedir}/*.c
rm -rf %{buildroot}%{ucrt64_includedir}/*.c


%files -n mingw32-crt
%license COPYING DISCLAIMER DISCLAIMER.PD
%{mingw32_libdir}/*

%files -n mingw64-crt
%license COPYING DISCLAIMER DISCLAIMER.PD
%{mingw64_libdir}/*

%files -n ucrt64-crt
%license COPYING DISCLAIMER DISCLAIMER.PD
%{ucrt64_libdir}/*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Sandro Mani <manisandro@gmail.com>
- Update to 13.0.0

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Tue Sep 24 2024 Sandro Mani <manisandro@gmail.com> - 12.0.0-4
- Pass --with-default-msvcrt=msvcrt when building mingw32/64 crt

* Thu Jul 25 2024 Marc-André Lureau <marcandre.lureau@redhat.com> - 12.0.0-3
- Add libbcryptprimitives.dll
  Related: https://bugzilla.redhat.com/show_bug.cgi?id=2299374

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 12.0.0.2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 16 2024 Sandro Mani <manisandro@gmail.com> - 12.0.0-1
- Update to 12.0.0

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 17 2023 Sandro Mani <manisandro@gmail.com> - 11.0.1-1
- Update to 11.0.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Apr 30 2023 Sandro Mani <manisandro@gmail.com> - 11.0.0-1
- Update to 11.0.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 03 2022 Sandro Mani <manisandro@gmail.com> - 10.0.0-2
- Provide standard DLLs
- Spec cleanups

* Tue Apr 26 2022 Sandro Mani <manisandro@gmail.com> - 10.0.0-1
- Update to 10.0.0

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 9.0.0-6
- Rebuild with mingw-gcc-12

* Thu Mar 24 2022 Sandro Mani <manisandro@gmail.com> - 9.0.0-5
- Rebuild with gcc12

* Wed Feb 23 2022 Marc-André Lureau <marcandre.lureau@redhat.com> - 9.0.0-4
- Add UCRT64 target

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Jul 08 2021 Sandro Mani <manisandro@gmail.com> - 9.0.0-1
- Update to 9.0.0

* Mon May 31 2021 Sandro Mani <manisandro@gmail.com> - 8.0.2-2
- Add wincore-def.patch

* Mon May 17 2021 Sandro Mani <manisandro@gmail.com> - 8.0.2-1
- Update to 8.0.2

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 8.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Jan 16 2021 Sandro Mani <manisandro@gmail.com> - 8.0.0-1
- Update to 8.0.0

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 7.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Sat Jun 20 2020 Sandro Mani <manisandro@gmail.com> - 7.0.0-1
- Update to 7.0.0

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 6.0.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 08 2019 Sandro Mani <manisandro@gmail.com> - 6.0.0-3
- Rebuild (Changes/Mingw32GccDwarf2)

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

* Thu Jun 14 2018 Sandro Mani <manisandro@gmail.com> - 5.0.3-2
- Rebuild (mingw-headers)

* Wed May 30 2018 Sandro Mani <manisandro@gmail.com> - 5.0.3-1
- Update to 5.0.3
- Backport patch for incomplete dwmapi.a

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

* Sun Mar 27 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 5.0-0.1.rc2
- Update to 5.0rc2

* Thu Feb  4 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.999-0.3.trunk.git38410a.20160204
- Update to 20160204 snapshot (git rev 38410a)

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.999-0.2.trunk.git5e2e73.20151224
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Dec 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.999-0.1.trunk.git.5e2e73.20151224
- Update to 20151224 snapshot (git rev 5e2e73)

* Wed Aug  5 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.4-1
- Update to 4.0.4

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.2-1
- Update to 4.0.2

* Sun Mar 29 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.1-1
- Update to 4.0.1

* Sat Mar 21 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0.0-1
- Update to 4.0.0

* Sat Mar  7 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0-0.2.rc3
- Update to 4.0rc3

* Mon Jan 26 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.0-0.1.rc1
- Update to 4.0rc1

* Mon Dec 22 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.5.trunk.git.f7337b.20141222
- Update to 20141222 snapshot (git rev f7337b)

* Tue Dec  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.4.trunk.git.dadc8f.20141209
- Update to 20141209 snapshot (git rev dadc8f)

* Wed Dec  3 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.2.trunk.git.a5c151.20141203
- Update to 20141203 snapshot (git rev a5c151)

* Fri Sep 12 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.9.999-0.1.trunk.git.b08afb.20140912
- Update to 20140912 snapshot (git rev b08afb)
- Bump version as upstream released mingw-w64 v3.2.0 recently (which is not based on the trunk branch)

* Wed Jul 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.12.trunk.gitec1ff7.20140730
- Update to 20140730 snapshot (git rev ec1ff7)
- Fixes invalid value of the global variable in6addr_loopback (RHBZ #1124368)
- Fixes missing memmove_s symbol on Windows XP/Server 2003

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.999-0.11.trunk.gitb8e816.20140530
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.10.trunk.gitb8e8160.20140530
- Update to 20140530 snapshot (git rev b8e8160)

* Sat May 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.9.trunk.git502c72.20140524
- Update to 20140524 snapshot (git rev 502c72)
- Upstream has switched from SVN to Git

* Sun Mar 30 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.8.trunk.r6559.20140330
- Update to r6559 (20140330 snapshot)
- Fixes Windows XP compatibility issue in mingw-glib-networking
  and mingw-sigar (missing strerror_s symbol)

* Mon Feb 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.7.trunk.r6497.20140224
- Update to r6497 (20140224 snapshot)

* Tue Feb 11 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.6.trunk.r6479.20140211
- Update to r6479 (20140211 snapshot)

* Mon Feb 10 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.5.trunk.r6477.20140210
- Update to r6477 (20140210 snapshot)

* Sat Feb  8 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.4.trunk.r6475.20140208
- Update to r6475 (20140208 snapshot)

* Sun Jan 26 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.3.trunk.r6469.20140126
- Update to r6469 (20140126 snapshot)
- Fixes missing sprintf_s issue on Windows XP/Server 2003 (RHBZ #1054481)

* Fri Jan 24 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.2.trunk.r6460.20140124
- Update to r6460 (20140124 snapshot)
- Fixes missing vsprintf_s issue on Windows XP/Server 2003 (RHBZ #1054481)

* Thu Jan  9 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.1.999-0.1.trunk.r6432.20140104
- Bump version to keep working upgrade path

* Sat Jan  4 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.3.trunk.r6432.20140104
- Update to r6432 (20140104 snapshot)

* Fri Nov 29 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.2.trunk.r6388.20131129
- Update to r6388 (20131129 snapshot)

* Wed Nov 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.999-0.1.trunk.r6379.20131120
- Update to r6379 (20131120 snapshot)

* Fri Sep 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 3.0.0-1
- Update to 3.0.0

* Sat Sep 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.38.trunk.r6284.20130914
- Update to r6284 (20130914 snapshot)

* Wed Sep 11 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.37.trunk.r6277.20130911
- Update to r6277 (20130911 snapshot)
- Fixes undefined reference to `IID_ICustomDestinationList'
- Fixes undefined reference to `IID_IFileOpenDialog'
- Fixes undefined reference to `IID_IFileSaveDialog'

* Mon Sep  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.36.trunk.r6258.20130909
- Update to r6258 (20130909 snapshot)

* Sat Sep  7 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.35.trunk.r6233.20130907
- Update to r6233 (20130907 snapshot)

* Tue Aug 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.34.trunk.r6155.20130827
- Update to r6155 (20130827 snapshot)

* Mon Aug 19 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.33.trunk.r6106.20130819
- Update to r6106 (20130819 snapshot)

* Sat Aug 10 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.32.trunk.r6069.20130810
- Update to r6069 (20130810 snapshot)
- Resolves unnecesary dependency on libgcc_s_sjlj-1.dll for the i686 target

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.999-0.31.trunk.r5969.20130721
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jul 21 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.30.trunk.r5969.20130721
- Update to r5969 (20130721 snapshot)
- Fixes strnlen issue on Windows XP

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.29.trunk.r5949.20130713
- Update to r5949 (20130713 snapshot)
- Dropped InterlockedCompareExchange workaround, issue is resolved upstream (with r5949)

* Fri Jun 28 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.28.trunk.r5915.20130628
- Update to r5915 (20130628 snapshot)

* Fri Jun 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.27.trunk.r5904.20130614
- Update to r5904 (fixes various regressions)

* Fri Jun 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.26.trunk.r5894.20130614
- Update to r5894 (20130614 snapshot)
- Updated instructions to regenerate snapshots
  (SourceForge has changed their SVN infrastructure)
- Workaround regression introduced by r5713 where
  the symbol InterlockedCompareExchange could get
  exported in shared libraries by accident

* Thu May 30 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.25.trunk.20130530
- Update to 20130530 snapshot

* Mon May 20 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.24.trunk.20130520
- Update to 20130520 snapshot

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.23.trunk.20130509
- Regenerated 20130509 snapshot
- Dropped upstreamed vsprintf_s patch

* Thu May  9 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.22.trunk.20130509
- Update to 20130509 snapshot

* Sun Apr 28 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.21.trunk.20130428
- Update to 20130428 snapshot
- Fixes build regression in wxWidgets and tcl regarding the timezone function

* Thu Apr 25 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.20.trunk.20130425
- Update to 20130425 snapshot

* Wed Apr  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.19.trunk.20130403
- Update to 20130403 snapshot
- Added Windows XP compatibility wrapper for the vsprintf_s function (RHBZ #917323)

* Sat Feb 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.18.trunk.20130216
- Update to 20130216 snapshot
- Includes improved import libraries (for setupapi, cfgmgr32 and others)

* Sun Jan 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.17.trunk.20130127
- Update to 20130127 snapshot

* Sat Jan  5 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.16.trunk.20130105
- Update to 20130105 snapshot

* Sat Nov 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.15.trunk.20121110
- Update to 20121110 snapshot

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
- Update to 20120703 snapshot
- Fixes testsuite failure in the qt_qmake_test_static_mingw32 testcase

* Mon Jul  9 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.8.trunk.20120709
- Update to 20120709 snapshot (contains full Cygwin support)
- Eliminated various manual kludges as upstream now installs their
  files to the correct folders by default

* Thu Jul  5 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.7.trunk.20120705
- Update to 20120705 snapshot (contains various Cygwin changes)

* Sat Jun  2 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.6.trunk.20120601
- Update to 20120601 snapshot

* Tue Mar  6 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.5.trunk.20120224
- Enable support for the win64 target

* Sat Feb 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.4.trunk.20120224
- Update to mingw-w64 trunk 20120224 snapshot
- Made the win64 pieces optional for now (pending approval of the mingw-gcc/mingw-binutils package reviews)
- Dropped the use of the mingw_pkg_name macro
- Eliminated some conditionals related to snapshot builds
- Use smaller SourceForge source URLs
- Improved summary of the various packages
- Simplified the configure, make and make install calls
- Dropped upstreamed patch
- Added DISCLAIMER and DISCLAIMER.PD files
- Added ZPLv2.1 to the license tag
- Bumped obsoletes/provides version for mingw32-runtime

* Tue Jan 24 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.3.trunk.20120124
- Update to mingw-w64 trunk 20120124 snapshot
- Apply upstream r4758 to fix vsnprintf and vscanf failures

* Fri Jan 20 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.2.trunk.20120120
- Update to mingw-w64 trunk 20120120 snapshot (fixes various errno related compile failures)

* Thu Jan 12 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.999-0.1.trunk.20120112
- Update to mingw-w64 trunk 20120112 snapshot

* Sat Nov 19 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0.1-1
- Update to mingw-w64 v2.0.1

* Sat Oct 22 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-1
- Update to mingw-w64 v2.0

* Sun Sep 25 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.3.rc1
- Replaced the boilerplate code with the mingw_package_header macro
- Bumped the obsoletes mingw32-runtime
- Dropped unneeded RPM tags

* Sat Aug 13 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.2.rc1
- Rebuild because of broken mingw-find-requires.sh in the mingw-filesystem package

* Mon Aug  8 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 2.0-0.1.rc1
- Update to 2.0-rc1

* Tue Jul 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.7.20110711.trunk
- Update to 20110711 snapshot of the trunk branch

* Sat Jun 25 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.6.20110625.trunk
- Update to 20110625 snapshot of the trunk branch (fixes gstreamer d3d issue)
- Replaced the patch with one which doesn't require the autotools

* Thu Jun  9 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.5.20110609.trunk
- Update to 20110609 snapshot of the trunk branch

* Thu Apr 14 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.4.20110413.trunk
- Update to 20110413 snapshot of the trunk branch
- Made the package compliant with the new packaging guidelines

* Wed Jan 12 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.3.20101003
- Update to 20101003 snapshot
- Generate per-target RPMs
- Bundle the COPYING file

* Wed Sep 29 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.2.20100914
- Update to snapshot 20100915 (v1.0 branch)
- Renamed the package to mingw-crt
- Added support for both i686-w64-mingw32 and x86_64-w64-mingw32
- Obsoletes/provides the mingw32-runtime package

* Fri May 14 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0-0.1.20100513
- Updated to snapshot 20100513 (v1.0 branch)
- Updated Source0 tag
- Fixed %%defattr tag

* Wed Feb 11 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.svn607.3
- Started mingw64 development.

* Tue Feb 10 2009 Richard W.M. Jones <rjones@redhat.com> - 3.15.2-1
- New upstream release 3.15.2.

* Tue Dec  9 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-10
- Force rebuild to get rid of the binary bootstrap package and replace
  with package built from source.

* Wed Nov 26 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-9
- No runtime dependency on binutils or gcc.
- But it DOES BR w32api.

* Mon Nov 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-8
- Rebuild against latest filesystem package.
- MINGW_CFLAGS -> MINGW32_CFLAGS.
- Rewrite the summary for accuracy and brevity.

* Fri Nov 21 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-6
- Remove obsoletes for a long dead package.
- Reenable (and fix) _mingw32_configure (Levente Farkas).

* Thu Nov 20 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-5
- Don't use _mingw32_configure macro - doesn't work here.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-4
- Rebuild against mingw32-filesystem 37

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-3
- Remove the useconds patch, which is no longer needed (Levente Farkas).
- Use _mingw32_configure macro.

* Wed Nov 19 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-2
- Rebuild against mingw32-filesystem 36

* Thu Oct 16 2008 Richard W.M. Jones <rjones@redhat.com> - 3.15.1-1
- New upstream version 3.15.1.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-6
- Rename mingw -> mingw32.

* Thu Sep  4 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-4
- Use RPM macros from mingw-filesystem.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 3.14-2
- Initial RPM release, largely based on earlier work from several sources.
