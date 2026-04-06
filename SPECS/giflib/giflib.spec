# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          giflib
Summary:       A library and utilities for processing GIFs
Version:       5.2.2
Release:       8%{?dist}

License:       MIT
URL:           http://www.sourceforge.net/projects/%{name}/
Source:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Downstream cmake support
Source1:       CMakeLists.txt
# Move quantize.c back into libgif.so (#1750122)
Patch0:        giflib_quantize.patch
# Fix several defects found by Coverity scan
Patch1:        giflib_coverity.patch
# Generate HTML docs with consistent section IDs to avoid multilib difference
Patch2:        giflib_html-docs-consistent-ids.patch
# Rename getarg.h to gif_getarg.h
# https://sourceforge.net/p/giflib/code/merge-requests/18/
Patch3:        getarg.patch
# Proposed patch for CVE-2025-31344
Patch4:        https://raw.githubusercontent.com/OpenMandrivaAssociation/giflib/refs/heads/master/giflib-5.2.2-cve-2025-31344.patch

BuildRequires: cmake
BuildRequires: gcc
BuildRequires: xmlto

BuildRequires: mingw32-filesystem
BuildRequires: mingw32-gcc

BuildRequires: mingw64-filesystem
BuildRequires: mingw64-gcc


%description
giflib is a library for reading and writing gif images.


%package devel
Summary:       Development files for programs using the giflib library
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description devel
The giflib-devel package includes header files, libraries necessary for
developing programs which use the giflib library.


%package utils
Summary:       Programs for manipulating GIF format image files
Requires:      %{name}%{?_isa} = %{version}-%{release}

%description utils
The giflib-utils package contains various programs for manipulating GIF
format image files.

%package -n mingw32-%{name}
Summary:       MinGW Windows %{name} library
Obsoletes:     mingw32-%{name}-static
BuildArch:     noarch

%description -n mingw32-%{name}
%{summary}.


%package -n mingw32-%{name}-tools
Summary:       Tools for the MinGW Windows %{name} library
Requires:      mingw32-%{name} = %{version}-%{release}
BuildArch:     noarch

%description -n mingw32-%{name}-tools
%{summary}.


%package -n mingw64-%{name}
Summary:       MinGW Windows %{name} library
Obsoletes:     mingw64-%{name}-static
BuildArch:     noarch

%description -n mingw64-%{name}
%{summary}.


%package -n mingw64-%{name}-tools
Summary:       Tools for the MinGW Windows %{name} library
Requires:      mingw64-%{name} = %{version}-%{release}
BuildArch:     noarch

%description -n mingw64-%{name}-tools
%{summary}.


%{?mingw_debug_package}


%prep
%autosetup -p1
cp -a %{SOURCE1} .

%build
# Native build
%cmake
%cmake_build

# MinGW build
%mingw_cmake
%mingw_make_build


%install
%cmake_install
%mingw_make_install
rm -rf %{buildroot}%{mingw32_mandir}
rm -rf %{buildroot}%{mingw64_mandir}


%mingw_debug_install_post


%files
%doc ChangeLog NEWS README
%license COPYING
%{_libdir}/libgif.so.7*

%files devel
%doc doc/*
%{_libdir}/libgif.so
%{_includedir}/gif_lib.h
%{_includedir}/gif_getarg.h

%files utils
%{_bindir}/gif*
%{_mandir}/man1/*.1*

%files -n mingw32-%{name}
%license COPYING
%{mingw32_bindir}/libgif-7.dll
%{mingw32_includedir}/gif_lib.h
%{mingw32_includedir}/gif_getarg.h
%{mingw32_libdir}/libgif.dll.a

%files -n mingw32-%{name}-tools
%{mingw32_bindir}/*.exe

%files -n mingw64-%{name}
%license COPYING
%{mingw64_bindir}/libgif-7.dll
%{mingw64_includedir}/gif_lib.h
%{mingw64_includedir}/gif_getarg.h
%{mingw64_libdir}/libgif.dll.a

%files -n mingw64-%{name}-tools
%{mingw64_bindir}/*.exe


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Wed Jul 16 2025 Sandro Mani <manisandro@gmail.com> - 5.2.2-7
- Increase minimum cmake version to 3.5
- Use GnuInstallDirs

* Tue Apr 15 2025 Sandro Mani <manisandro@gmail.com> - 5.2.2-6
- Add proposed patch for CVE-2025-31334

* Wed Apr 02 2025 Benson Muite <fed500@fedoraproject.org> - 5.2.2-5
- Rename getarg.h to gif_getarg.h

* Wed Apr 02 2025 Benson Muite <fed500@fedoraproject.org> - 5.2.2-4
- Install getarg.h header file

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Mon Feb 19 2024 Sandro Mani <manisandro@gmail.com> - 5.2.2-1
- Update to 5.2.2

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Sep 14 2023 Sandro Mani <manisandro@gmail.com> - 5.2.1-17
- Add patch for CVE-2023-39742

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Sandro Mani <manisandro@gmail.com> - 5.2.1-14
- Backport fix for CVE-2022-28506

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Fri Mar 25 2022 Sandro Mani <manisandro@gmail.com> - 5.2.1-12
- Rebuild with mingw-gcc-12

* Thu Feb 24 2022 Sandro Mani <manisandro@gmail.com> - 5.2.1-11
- Make mingw subpackages noarch

* Sat Feb 19 2022 Sandro Mani <manisandro@gmail.com> - 5.2.1-10
- Add mingw subpackage

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 17 2020 Sandro Mani <manisandro@gmail.com> - 5.2.1-5
- Fix several defects found by Coverity scan
- Generate HTML docs with consistent section IDs to avoid multilib difference

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Oct 01 2019 Sandro Mani <manisandro@gmail.com> - 5.2.1-3
- Move quantize.c back into libgif.so (#1750122)

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Sandro Mani <manisandro@gmail.com> - 5.2.1-1
- Update to 5.2.1

* Mon Apr 01 2019 Sandro Mani <manisandro@gmail.com> - 5.1.9-1
- Update to 5.1.9

* Wed Mar 20 2019 Sandro Mani <manisandro@gmail.com> - 5.1.8-1
- Update to 5.1.8

* Mon Mar 11 2019 Sandro Mani <manisandro@gmail.com> - 5.1.7-1
- Update to 5.1.7

* Sat Feb 23 2019 Sandro Mani <manisandro@gmail.com> - 5.1.6-2
- Fix broken soname

* Mon Feb 18 2019 Sandro Mani <manisandro@gmail.com> - 5.1.6-1
- Update to 5.1.6

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Sun Feb 11 2018 Sandro Mani <manisandro@gmail.com> - 5.1.4-1
- Update to 5.1.4

* Thu Feb  8 2018 Florian Weimer <fweimer@redhat.com> - 4.1.6-22
- Build libungif with linker flags from redhat-rpm-config

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Feb 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 4.1.6-20
- Switch to %%ldconfig_scriptlets

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Mar 29 2017 Stephen Gallagher <sgallagh@redhat.com> - 4.1.6-17
- Fix compilation errors when -Werror=format-security

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.1.6-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Aug 14 2015 Adam Jackson <ajax@redhat.com> 4.1.6-14
- Link libungif with -z now too

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Dec 18 2013 Peter Robinson <pbrobinson@fedoraproject.org> 4.1.6-10
- Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 4.1.6-8
- Perl 5.18 rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 09 2009 Robert Scheck <robert@fedoraproject.org> 4.1.6-2
- Solved multilib problems with documentation (#465208, #474538)
- Removed static library from giflib-devel package (#225796 #c1)

* Mon Apr 13 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 4.1.6-1
- update to 4.1.6

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 4.1.3-9
- Autorebuild for GCC 4.3

* Tue Mar 13 2007 Karsten Hopp <karsten@redhat.com> 4.1.3-8
- add BR libXt-devel, otherwise X support will be disabled

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> 
- rebuild

* Mon May 22 2006 Karsten Hopp <karsten@redhat.de> 4.1.3-7
- buildrequires libICE-devel, libSM-devel

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 4.1.3-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 4.1.3-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Nov  1 2005 Matthias Clasen <mclasen@redhat.com> 4.1.3-6
- Switch requires to modular X

* Wed Sep 21 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-5
- Merge an option on the empty library link line.
- Obsolete libungif progs package.
- Rename -progs to -utils as FC packages seem to have moved in this direction
  for subpackages.
 
* Tue Sep 20 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-4
- Modify the way we provide libungif compatibility by building an empty
  library that requires libgif.
- Remove chmod in install.  It doesn't seem to be necessary.
- Add a patch to fix a problem with long being 64 bit on x86_64 but the code
  assuming it was 32 bit.
  
* Mon Sep 19 2005 Toshio Kuratomi <toshio@tiki-lounge.com> 4.1.3-1
- Port package from libungif to giflib.
