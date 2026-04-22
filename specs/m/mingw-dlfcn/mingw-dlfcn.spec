# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%global mingw_build_ucrt64 1
%{?mingw_package_header}

%global realname dlfcn-win32

Name:          mingw-dlfcn
Version:       1.4.2
Release: 3%{?dist}
Summary:       Implements a wrapper for dlfcn (dlopen dlclose dlsym dlerror)

License:       MIT
URL:           https://github.com/%{realname}/%{realname}
Source0:       https://github.com/%{realname}/%{realname}/archive/v%{version}/%{realname}-%{version}.tar.gz

BuildArch:     noarch

BuildRequires: cmake
BuildRequires: make

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc
BuildRequires: mingw32-binutils

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc
BuildRequires: mingw64-binutils

BuildRequires: ucrt64-filesystem
BuildRequires: ucrt64-gcc
BuildRequires: ucrt64-binutils


%description
This library implements a wrapper for dlfcn, as specified in POSIX and SUS,
around the dynamic link library functions found in the Windows API.


# Win32
%package -n mingw32-dlfcn
Summary:        Implements a wrapper for dlfcn (dlopen dlclose dlsym dlerror)

%description -n mingw32-dlfcn
This library implements a wrapper for dlfcn, as specified in POSIX and SUS,
around the dynamic link library functions found in the Windows API.


%package -n mingw32-dlfcn-static
Summary:        Static version of the MinGW Windows dlfcn library
Requires:       mingw32-dlfcn = %{version}-%{release}

%description -n mingw32-dlfcn-static
Static version of the MinGW Windows dlfcn library.


# Win64
%package -n mingw64-dlfcn
Summary:        Implements a wrapper for dlfcn (dlopen dlclose dlsym dlerror)

%description -n mingw64-dlfcn
This library implements a wrapper for dlfcn, as specified in POSIX and SUS,
around the dynamic link library functions found in the Windows API.


%package -n mingw64-dlfcn-static
Summary:        Static version of the MinGW Windows dlfcn library
Requires:       mingw64-dlfcn = %{version}-%{release}

%description -n mingw64-dlfcn-static
Static version of the MinGW Windows dlfcn library.


# UCRT64
%package -n ucrt64-dlfcn
Summary:        Implements a wrapper for dlfcn (dlopen dlclose dlsym dlerror)

%description -n ucrt64-dlfcn
This library implements a wrapper for dlfcn, as specified in POSIX and SUS,
around the dynamic link library functions found in the Windows API.


%package -n ucrt64-dlfcn-static
Summary:        Static version of the MinGW Windows dlfcn library
Requires:       ucrt64-dlfcn = %{version}-%{release}

%description -n ucrt64-dlfcn-static
Static version of the MinGW Windows dlfcn library.


%{?mingw_debug_package}


%prep
%autosetup -p1 -n %{realname}-%{version}

for f in README.md COPYING; do
    %{__sed} -i 's/\r//' "${f}";
done


%build
# Shared
export MINGW_BUILDDIR_SUFFIX=-shared
%mingw_cmake
%mingw_make_build

# Static
export MINGW_BUILDDIR_SUFFIX=-static
%mingw_cmake -DBUILD_SHARED_LIBS:BOOL=OFF
%mingw_make_build


%install
# Shared
export MINGW_BUILDDIR_SUFFIX=-shared
%mingw_make_install

# Static
export MINGW_BUILDDIR_SUFFIX=-static
%mingw_make_install


# Win32
%files -n mingw32-dlfcn
%doc README.md
%license COPYING
%{mingw32_bindir}/libdl.dll
%{mingw32_libdir}/libdl.dll.a
%{mingw32_includedir}/dlfcn.h
%{mingw32_datadir}/%{realname}

%files -n mingw32-dlfcn-static
%{mingw32_libdir}/libdl.a

# Win64
%files -n mingw64-dlfcn
%doc README.md
%license COPYING
%{mingw64_bindir}/libdl.dll
%{mingw64_libdir}/libdl.dll.a
%{mingw64_includedir}/dlfcn.h
%{mingw64_datadir}/%{realname}

%files -n mingw64-dlfcn-static
%{mingw64_libdir}/libdl.a

# UCRT64
%files -n ucrt64-dlfcn
%doc README.md
%license COPYING
%{ucrt64_bindir}/libdl.dll
%{ucrt64_libdir}/libdl.dll.a
%{ucrt64_includedir}/dlfcn.h
%{ucrt64_datadir}/%{realname}

%files -n ucrt64-dlfcn-static
%{ucrt64_libdir}/libdl.a


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Apr 25 2025 Sandro Mani <manisandro@gmail.com> - 1.4.2-1
- Update to 1.4.2

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Sep 02 2024 Miroslav Suchý <msuchy@redhat.com> - 1.4.1-6
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Apr 02 2024 Jonathan Schleifer <js@nil.im> - 1.4.1-4
- Build UCRT64 package

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jul 30 2023 Sandro Mani <manisandro@gmail.com> - 1.4.1-1
- Update to 1.4.1

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jun 22 2023 Sandro Mani <manisandro@gmail.com> - 1.4.0-1
- Update to 1.4.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Mon Nov 21 2022 Sandro Mani <manisandro@gmail.com> - 1.3.1-1
- Update to 1.3.1

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 1.2.0-7
- Rebuild with mingw-gcc-12

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Aug 14 2019 Fabiano Fidêncio <fidencio@redhat.com> - 1.2.0-1
- Update to latest upstream release, rhbz#1740739

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Greg Hellings <greg.hellings@gmail.com> - 1.1.2-1
- Upstream version 1.1.2

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Jun 13 2017 Greg Hellings <greg.hellings@gmail.com> - 1.1.1-1
- Upstrema version moved to Github
- New upstream release 1.1.1
- Use CMake

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.20.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0-0.19.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.18.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.17.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.16.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.15.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.14.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Apr 14 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.13.r11
- Added win64 support

* Wed Mar 07 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.12.r11
- Renamed the source package to mingw-dlfcn (RHBZ #800861)
- Use mingw macros without leading underscore

* Mon Feb 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.11.r11
- Rebuild against the mingw-w64 toolchain

* Thu Feb 16 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.10.r11
- Make sure the static lib is compiled correctly (RHBZ #791191)
- Various cleanups

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.9.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.8.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct 30 2009 Erik van Pienbroek <epienbro@fedoraproject.org> - 0-0.7.r11
- Use %%global instead of %%define
- Automatically generate debuginfo subpackage
- Fixed %%defattr line
- Added -static subpackage
- Fixed linker error with C++ applications

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.6.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.5.r11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 0-0.4.r11
- Rebuild for mingw32-gcc 4.4

* Wed Jan 14 2009 Richard W.M. Jones <rjones@redhat.com> - 0-0.3.r11
- Use Version 0
  (https://www.redhat.com/archives/fedora-packaging/2009-January/msg00064.html)
- Revert use of dos2unix for now
  (https://www.redhat.com/archives/fedora-packaging/2009-January/msg00066.html)
- Use _smp_mflags.

* Tue Jan 13 2009 Richard W.M. Jones <rjones@redhat.com> - 0.1-0.2.r11
- Import into fedora-mingw temporary repository because there are packages
  which will depend on this.
- Fix the version/release according to packaging guidelines.
- Tidy up the spec file.
- Use dos2unix and keep the timestamps.

* Fri Jan 02 2009 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - r11-1
- Initial RPM release. 
