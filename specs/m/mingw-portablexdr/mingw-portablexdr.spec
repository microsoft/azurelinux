# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%?mingw_package_header

Name:		mingw-portablexdr
Version:	4.9.1
Release: 39%{?dist}
Summary:	MinGW Windows PortableXDR / RPC Library

# Automatically converted from old format: LGPLv2+ - review is highly recommended.
License:	LicenseRef-Callaway-LGPLv2+
URL:		https://people.redhat.com/~rjones/portablexdr/
Source0:	https://people.redhat.com/~rjones/portablexdr/files/portablexdr-%{version}.tar.gz
BuildArch:	noarch

BuildRequires: make
BuildRequires:	mingw32-filesystem >= 95
BuildRequires:	mingw32-gcc
BuildRequires:	mingw32-binutils

BuildRequires:	mingw64-filesystem >= 95
BuildRequires:	mingw64-gcc
BuildRequires:	mingw64-binutils

BuildRequires:  gcc
BuildRequires:  git
BuildRequires:  bison

# Remove include of config.h from public header.
Patch0:		portablexdr-4.9.1-no-config-h.patch
Patch1:		portablexdr-build-use-intptr_t-and-uintptr_t-to-cast-ptr-to-int.patch


%description
MinGW Windows PortableXDR XDR / RPC library.


# Win32
%package -n mingw32-portablexdr
Summary:	MinGW Windows PortableXDR / RPC Library

%description -n mingw32-portablexdr
MinGW Windows PortableXDR XDR / RPC library.

%package -n mingw32-portablexdr-static
Summary:       MinGW Windows PortableXDR XDR / RPC library, static version

%description -n mingw32-portablexdr-static
MinGW Windows PortableXDR XDR / RPC library, static version.

# Win64
%package -n mingw64-portablexdr
Summary:        MinGW Windows PortableXDR / RPC Library

%description -n mingw64-portablexdr
MinGW Windows PortableXDR XDR / RPC library.

%package -n mingw64-portablexdr-static
Summary:       MinGW Windows PortableXDR XDR / RPC library, static version

%description -n mingw64-portablexdr-static
MinGW Windows PortableXDR XDR / RPC library, static version.


%?mingw_debug_package


%prep
%autosetup -S git -n portablexdr-%{version}

%build
%mingw_configure --enable-static CFLAGS="-std=gnu89" 
# Force bison to generate yylex() prototype to avoid build
# failure with new GCC which is strict about missing prototypes
export POSIXLY_CORRECT=1
rm -f rpcgen_parse.c rpcgen_parse.h
%mingw_make %{?_smp_flags}


%install
%mingw_make DESTDIR=$RPM_BUILD_ROOT install

# Drop all .la files
find $RPM_BUILD_ROOT -name "*.la" -delete


# Win32
%files -n mingw32-portablexdr
%license COPYING.LIB
%{mingw32_bindir}/portable-rpcgen.exe
%{mingw32_bindir}/libportablexdr-0.dll
%{mingw32_libdir}/libportablexdr.dll.a
%{mingw32_includedir}/rpc

%files -n mingw32-portablexdr-static
%{mingw32_libdir}/libportablexdr.a

# Win64
%files -n mingw64-portablexdr
%license COPYING.LIB
%{mingw64_bindir}/portable-rpcgen.exe
%{mingw64_bindir}/libportablexdr-0.dll
%{mingw64_libdir}/libportablexdr.dll.a
%{mingw64_includedir}/rpc

%files -n mingw64-portablexdr-static
%{mingw64_libdir}/libportablexdr.a


%changelog
* Wed Jul 30 2025 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.1-38
- Fix FTBFS using gnu89.. Fixes: rhbz#2385188

* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 4.9.1-35
- convert license to SPDX

* Tue Jul 30 2024 Daniel P. Berrangé <berrange@redhat.com> - 4.9.1-34
- Re-run bison with POSIXLY_CORRECT=1 set (rhbz #2300960)

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 4.9.1-27
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Aug 12 2019 Marc-André Lureau <marcandre.lureau@redhat.com> - 4.9.1-21
- Unretire package rhbz#1740183
- Fix URL location
- Fix FTBFS rhbz#1675384

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.9.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 14 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-8
- Added win64 support (contributed by Marc-Andre Lureau)
- Added static subpackage
- Added win64 specific patch
- Automatically generate debuginfo subpackages

* Fri Mar 09 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-7
- Dropped .la files

* Wed Mar 07 2012 Kalev Lember <kalevlember@gmail.com> - 4.9.1-6
- Renamed the source package to mingw-portablexdr (#801016)
- Modernize the spec file
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.9.1-5
- Rebuild against the mingw-w64 toolchain

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul  5 2011 Richard W.M. Jones <rjones@redhat.com> - 4.9.1-3
- Remove include of config.h from public header.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jul 13 2010 Ryan O'Hara <rohara@redhat.com> - 4.9.1-1
- New upstream release 4.9.1.

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 4.0.11-4
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 4.0.11-3
- Include license file.

* Fri Jan 23 2009 Richard W.M. Jones <rjones@redhat.com> - 4.0.11-2
- Disable static libraries.
- Use _smp_flags.

* Wed Oct 15 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.11-1
- New upstream version 4.0.11.

* Wed Sep 24 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-5
- Rename mingw -> mingw32.

* Wed Sep 10 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-4
- Remove static library.

* Fri Sep  5 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-3
- Use RPM macros from mingw-filesystem.

* Tue Sep  2 2008 Daniel P. Berrange <berrange@redhat.com> - 4.0.10-2
- List files explicitly and set custom CFLAGS

* Tue Jul  8 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.10-1
- New upstream release 4.0.10.
- No need to manually install header files in this version.

* Mon Jul  7 2008 Richard W.M. Jones <rjones@redhat.com> - 4.0.9-2
- Initial RPM release, largely based on earlier work from several sources.
