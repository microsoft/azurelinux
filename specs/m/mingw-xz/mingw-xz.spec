# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%{?mingw_package_header}

Name:           mingw-xz
Version:        5.2.4
Release: 16%{?dist}
Summary:        Cross-compiled LZMA compression utilities

# Scripts xz{grep,diff,less,more} and symlinks (copied from gzip) are
# GPLv2+, binaries are Public Domain (linked against LGPL getopt_long but its
# OK), documentation is Public Domain.
License:        0BSD AND GPL-2.0-or-later AND LicenseRef-Fedora-Public-Domain
URL:            http://tukaani.org/xz/
Source0:        http://tukaani.org/xz/xz-%{version}.tar.xz

BuildArch:      noarch

BuildRequires: make
BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw64-gcc
BuildRequires:  mingw32-binutils
BuildRequires:  mingw64-binutils


%description
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


# Mingw32
%package -n mingw32-xz
Summary:        Cross-compiled LZMA compression utilities
Requires:       mingw32-xz-libs = %{version}-%{release}

%description -n mingw32-xz
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


%package -n mingw32-xz-libs
Summary:        Libraries for decoding LZMA compression
License:        0BSD


%description -n mingw32-xz-libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package -n mingw32-xz-libs-static
Summary:        Static version of the xz library
License:        0BSD
Requires:       mingw32-xz-libs = %{version}-%{release}


%description -n mingw32-xz-libs-static
Static version of the xz library.


# Mingw64
%package -n mingw64-xz
Summary:        Cross-compiled LZMA compression utilities
Requires:       mingw64-xz-libs = %{version}-%{release}

%description -n mingw64-xz
XZ Utils are an attempt to make LZMA compression easy to use on free (as in
freedom) operating systems. This is achieved by providing tools and libraries
which are similar to use than the equivalents of the most popular existing
compression algorithms.

LZMA is a general purpose compression algorithm designed by Igor Pavlov as
part of 7-Zip. It provides high compression ratio while keeping the
decompression speed fast.


%package -n mingw64-xz-libs
Summary:        Libraries for decoding LZMA compression
License:        0BSD


%description -n mingw64-xz-libs
Libraries for decoding files compressed with LZMA or XZ utils.


%package -n mingw64-xz-libs-static
Summary:        Static version of the xz library
License:        0BSD
Requires:       mingw64-xz-libs = %{version}-%{release}


%description -n mingw64-xz-libs-static
Static version of the xz library.


%?mingw_debug_package


%prep
%setup -q -n xz-%{version}


%build
MINGW32_CFLAGS="%{mingw32_cflags} -D_FILE_OFFSET_BITS=64" \
MINGW64_CFLAGS="%{mingw64_cflags} -D_FILE_OFFSET_BITS=64" \
%mingw_configure --disable-nls \
                 --disable-lzmadec \
                 --disable-lzmainfo \
                 --disable-lzma-links \
                 --disable-scripts
%mingw_make %{?_smp_mflags}


%install
%mingw_make_install DESTDIR=$RPM_BUILD_ROOT

iconv -f latin1 -t utf-8 < NEWS > NEWS.utf8; cp NEWS.utf8 NEWS
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name cpio.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name mtree.5 -exec rm -f {} ';'
find $RPM_BUILD_ROOT -name tar.5 -exec rm -f {} ';'

# Remove documentation which duplicates that found in the native package.
rm -r $RPM_BUILD_ROOT/%{mingw32_prefix}/share
rm -r $RPM_BUILD_ROOT/%{mingw64_prefix}/share


# Win32
%files -n mingw32-xz
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1
%{mingw32_bindir}/unxz.exe
%{mingw32_bindir}/xz.exe
%{mingw32_bindir}/xzcat.exe
%{mingw32_bindir}/xzdec.exe

%files -n mingw32-xz-libs
%license COPYING
%{mingw32_bindir}/liblzma-5.dll
%{mingw32_includedir}/lzma
%{mingw32_includedir}/lzma.h
%{mingw32_libdir}/liblzma.dll.a
%{mingw32_libdir}/pkgconfig/liblzma.pc

%files -n mingw32-xz-libs-static
%license COPYING
%{mingw32_libdir}/liblzma.a


# Win64
%files -n mingw64-xz
%license COPYING COPYING.GPLv2 COPYING.GPLv3 COPYING.LGPLv2.1
%{mingw64_bindir}/unxz.exe
%{mingw64_bindir}/xz.exe
%{mingw64_bindir}/xzcat.exe
%{mingw64_bindir}/xzdec.exe

%files -n mingw64-xz-libs
%license COPYING
%{mingw64_bindir}/liblzma-5.dll
%{mingw64_includedir}/lzma
%{mingw64_includedir}/lzma.h
%{mingw64_libdir}/liblzma.dll.a
%{mingw64_libdir}/pkgconfig/liblzma.pc

%files -n mingw64-xz-libs-static
%license COPYING
%{mingw64_libdir}/liblzma.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 5.2.4-7
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Aug 13 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 5.2.4-1
- New upstream version.

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Apr 01 2017 Michael Cronenworth <mike@cchtml.com> - 5.2.3-1
- New upstream version.

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 05 2016 Michael Cronenworth <mike@cchtml.com> - 5.2.2-3
- Enable thread support

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Dec 28 2015 Michael Cronenworth <mike@cchtml.com> - 5.2.2-1
- New upstream version.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 02 2015 Michael Cronenworth <mike@cchtml.com> - 5.2.1-1
- New upstream version.
  http://www.mail-archive.com/xz-devel@tukaani.org/msg00226.html

* Fri Jan 30 2015 Michael Cronenworth <mike@cchtml.com> - 5.2.0-1
- New upstream version.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-5alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-4alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-3alpha
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug 26 2012 Michael Cronenworth <mike@cchtml.com> - 5.1.2-2alpha
- Fix CFLAGS.

* Sun Aug 26 2012 Michael Cronenworth <mike@cchtml.com> - 5.1.2-1alpha
- New upstream version.

* Thu Jun 07 2012 Michael Cronenworth <mike@cchtml.com> - 5.1.1-1alpha
- Initial RPM release.
