# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%?mingw_package_header

Name:           mingw-bzip2
Version:        1.0.8
Release: 17%{?dist}
Summary:        MinGW port of bzip2 file compression utility

# Automatically converted from old format: BSD - review is highly recommended.
License:        LicenseRef-Callaway-BSD
URL:            http://www.bzip.org/
Source0:        http://www.bzip.org/%{version}/bzip2-%{version}.tar.gz

BuildArch:      noarch

Patch12:        bzip2-1.0.5-autoconfiscated.patch

# Export all symbols using the cdecl calling convention instead of
# stdcall as it is also done by various other downstream distributors
# (like mingw.org and gnuwin32) and it resolves various autoconf and
# cmake detection issues (RHBZ #811909, RHBZ #812573)
# Patch is taken from the gnuwin32 project
Patch13:        bzip2-use-cdecl-calling-convention.patch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils
BuildRequires:  autoconf, automake, libtool


%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

This package contains development tools and libraries for use when
cross-compiling Windows software in Fedora.

# Win32
%package -n mingw32-bzip2
Summary:        32 Bit version of bzip2 for Windows

%description -n mingw32-bzip2
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

This package contains development tools and libraries for use when
cross-compiling Windows software in Fedora.

%package -n mingw32-bzip2-static
Summary:        Static library for mingw32-bzip2 development
Requires:       mingw32-bzip2 = %{version}-%{release}

%description -n mingw32-bzip2-static
Static library for mingw32-bzip2 development.

# Win64
%package -n mingw64-bzip2
Summary:        64 Bit version of bzip2 for Windows

%description -n mingw64-bzip2
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

This package contains development tools and libraries for use when
cross-compiling Windows software in Fedora.

%package -n mingw64-bzip2-static
Summary:        Static library for mingw64-bzip2 development
Requires:       mingw64-bzip2 = %{version}-%{release}

%description -n mingw64-bzip2-static
Static library for mingw64-bzip2 development.


%?mingw_debug_package


%prep
%setup -q -n bzip2-%{version}

%patch -P12 -p1 -b .autoconfiscated

%patch -P13 -p1 -b .cdecl

sh ./autogen.sh


%build
%mingw_configure
%mingw_make %{?_smp_mflags}


%install
%mingw_make install DESTDIR=$RPM_BUILD_ROOT

# The binaries which are symlinks contain the full buildroot
# name in the symlink, so replace those.
for dir in $RPM_BUILD_ROOT%{mingw32_bindir} $RPM_BUILD_ROOT%{mingw64_bindir} ; do
pushd $dir
rm bzcmp.exe bzegrep.exe bzfgrep.exe bzless.exe
ln -s bzdiff bzcmp
ln -s bzgrep bzegrep
ln -s bzgrep bzfgrep
ln -s bzmore bzless
popd
done


# Remove the manpages, they're duplicates of the native package,
# and located in the wrong place anyway.
rm -r $RPM_BUILD_ROOT%{mingw32_mandir}/man1
rm -r $RPM_BUILD_ROOT%{mingw64_mandir}/man1

# Remove libtool .la files.
rm $RPM_BUILD_ROOT%{mingw32_libdir}/libbz2.la
rm $RPM_BUILD_ROOT%{mingw64_libdir}/libbz2.la

# Win32
%files -n mingw32-bzip2
%doc COPYING
%{mingw32_bindir}/libbz2-1.dll
%{mingw32_bindir}/bunzip2.exe
%{mingw32_bindir}/bzcat.exe
%{mingw32_bindir}/bzcmp
%{mingw32_bindir}/bzdiff
%{mingw32_bindir}/bzegrep
%{mingw32_bindir}/bzfgrep
%{mingw32_bindir}/bzgrep
%{mingw32_bindir}/bzip2.exe
%{mingw32_bindir}/bzip2recover.exe
%{mingw32_bindir}/bzless
%{mingw32_bindir}/bzmore
%{mingw32_includedir}/bzlib.h
%{mingw32_libdir}/libbz2.dll.a
%{mingw32_libdir}/pkgconfig/bzip2.pc

%files -n mingw32-bzip2-static
%{mingw32_libdir}/libbz2.a

# Win64
%files -n mingw64-bzip2
%doc COPYING
%{mingw64_bindir}/libbz2-1.dll
%{mingw64_bindir}/bunzip2.exe
%{mingw64_bindir}/bzcat.exe
%{mingw64_bindir}/bzcmp
%{mingw64_bindir}/bzdiff
%{mingw64_bindir}/bzegrep
%{mingw64_bindir}/bzfgrep
%{mingw64_bindir}/bzgrep
%{mingw64_bindir}/bzip2.exe
%{mingw64_bindir}/bzip2recover.exe
%{mingw64_bindir}/bzless
%{mingw64_bindir}/bzmore
%{mingw64_includedir}/bzlib.h
%{mingw64_libdir}/libbz2.dll.a
%{mingw64_libdir}/pkgconfig/bzip2.pc

%files -n mingw64-bzip2-static
%{mingw64_libdir}/libbz2.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.0.8-14
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.0.8-7
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 1.0.8-1
- New upstream version 1.0.8

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Apr 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.6-1
- Update to 1.0.6
- Export all symbols using the cdecl calling convention instead of
  stdcall as it is also done by various other downstream distributors
  (like mingw.org and gnuwin32) and it resolves various autoconf and
  cmake detection issues (RHBZ #811909, RHBZ #812573)
- Added -static subpackages (RHBZ #665539)

* Fri Mar 16 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.5-13
- Added win64 support (contributed by Jay Higley)
- Added the autoconf patch from http://ftp.suse.com/pub/people/sbrabec/bzip2/
- Dropped some unneeded patches
- Dropped the non-implementated testsuite pieces
- Bundle the pkgconfig files

* Wed Mar 07 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.5-12
- Renamed the source package to mingw-bzip2 (RHBZ #800847)
- Use mingw macros without leading underscore
- Dropped unneeded RPM tags

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 1.0.5-11
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 1.0.5-6
- Rebuild for mingw32-gcc 4.4

* Thu Dec 18 2008 Richard Jones <rjones@redhat.com> - 1.0.5-5
- Include the LICENSE file in doc section.

* Sat Nov 22 2008 Richard Jones <rjones@redhat.com> - 1.0.5-4
- Rename the implib as libbz2.dll.a so that libtool can find it.

* Wed Oct 29 2008 Richard Jones <rjones@redhat.com> - 1.0.5-3
- Fix mixed spaces/tabs in specfile.

* Fri Oct 10 2008 Richard Jones <rjones@redhat.com> - 1.0.5-2
- Allow the tests to be disabled selectively.

* Thu Sep 25 2008 Richard Jones <rjones@redhat.com> - 1.0.5-1
- Initial RPM release.
