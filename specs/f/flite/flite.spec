# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

%ifnarch s390x
%bcond_without check
%else
# https://github.com/festvox/flite/issues/67
%bcond_with check
%endif

# https://github.com/festvox/flite/pull/92#issuecomment-1481980430
%global _smp_mflags -j1

%global abi 1

Name:           flite
Version:        2.2
Release: 13%{?dist}
Summary:        Small, fast speech synthesis engine (text-to-speech)
License:        MIT
URL:            http://cmuflite.org/

Source0:        https://github.com/festvox/flite/archive/v%{version}/flite-%{version}.tar.gz
Patch0:         flite-2.2-lto.patch
# fixes build with texinfo-7.0+, see https://lists.gnu.org/archive/html/bug-texinfo/2022-11/msg00036.html
Patch1:         flite-2.2-texinfo-7.0.patch
# https://github.com/festvox/flite/issues/86
Patch2:         flite-2.2-parallel-make.patch
# https://github.com/festvox/flite/pull/90
Patch3:         flite-2.2-tests.patch
# texi2pdf
# WARNING see explanation about PDF doc below.
#BuildRequires:  texinfo-tex
BuildRequires:  gcc
BuildRequires:  autoconf automake libtool
BuildRequires:  ed alsa-lib-devel
BuildRequires: make
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  texinfo


%description
Flite (festival-lite) is a small, fast run-time speech synthesis engine
developed at CMU and primarily designed for small embedded machines and/or
large servers. Flite is designed as an alternative synthesis engine to
Festival for voices built using the FestVox suite of voice building tools.


%package devel
Summary: Development files for flite
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for Flite, a small, fast speech synthesis engine.


%prep
%setup -q
%patch -P0 -p1 -b .lto
%patch -P1 -p1 -b .ti7
%patch -P2 -p1 -b .pmake
%patch -P3 -p1 -b .tst


%build
autoreconf -vif
%configure \
    --enable-shared \
    --with-audio=pulseaudio \

%make_build
# Build documentation
cd doc
# WARNING "make doc" provides a huge PDF file. It was decided not to produce/package it.
#make doc
make flite.html


%install
%make_install
rm %{buildroot}%{_libdir}/libflite*.a


%if %{with check}
%check
LD_LIBRARY_PATH=%{buildroot}%{_libdir} make check
%endif


%files
%license COPYING
%doc ACKNOWLEDGEMENTS
%doc doc/html
%doc README.md
%{_libdir}/libflite_cmu_{grapheme,indic}_{lang,lex}.so.{%{abi},%{version}}
%{_libdir}/libflite_cmulex.so.{%{abi},%{version}}
%{_libdir}/libflite_cmu_time_awb.so.{%{abi},%{version}}
%{_libdir}/libflite_cmu_us_{awb,kal,kal16,rms,slt}.so.{%{abi},%{version}}
%{_libdir}/libflite.so.{%{abi},%{version}}
%{_libdir}/libflite_usenglish.so.{%{abi},%{version}}
%{_bindir}/flite
%{_bindir}/flite_cmu_time_awb
%{_bindir}/flite_cmu_us_{awb,kal,kal16,rms,slt}
%{_bindir}/flite_time


%files devel
%{_libdir}/libflite_cmu_{grapheme,indic}_{lang,lex}.so
%{_libdir}/libflite_cmulex.so
%{_libdir}/libflite_cmu_time_awb.so
%{_libdir}/libflite_cmu_us_{awb,kal,kal16,rms,slt}.so
%{_libdir}/libflite.so
%{_libdir}/libflite_usenglish.so
%{_includedir}/flite


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Mon Dec 30 2024 Dominik Mierzejewski <dominik@greysector.net> - 2.2-10
- backport patch for upstream issue #86
- apply Gentoo patch and run all tests

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Tue Feb 21 2023 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.2-5
- work around FTBFS bug with make-4.4+ (resolves rhbz#2171492)
- fix HTML doc build with texinfo 7.0

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Tue Oct 05 2021 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.2-1
- update to 2.2 (#1062487)
- drop obsolete patches
- update BuildRequires
- run testsuite
- drop obsolete ldconfig_scriptlets macro
- enable parallel make
- use modern macros
- fix LTO warnings
- skip test on s390x

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Mar  7 2018 Peter Robinson <pbrobinson@fedoraproject.org> 1.3-31
- Add gcc BR, minor spec cleanups

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.3-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan  8 2016 Peter Lemenkov <lemenkov@gmail.com> - 1.3-25
- Fixed FTBFS in Rawhide
- Remove pre-EPEL6 support

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jan  6 2014 Rui Matos <rmatos@redhat.com> - 1.3-21
- Resolves: (CVE-2014-0027) flite: insecure temporary file use

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Mar 13 2011 Francois Aucamp <faucamp@fedoraproject.org> - 1.3-16
- Added patch declaring explicit libm linking dependency (RHBZ #564899)
- Updated source and URL tags

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Mar 21 2009 Robert Scheck <robert@fedoraproject.org> - 1.3-13
- Removed moving of non-existing documentation flite directory

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Oct 11 2008 Peter Lemenkov <lemenkov@gmail.com> - 1.3-11
- Fix for RHEL 4
 
* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.3-10
- fix license tag

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.3-9
- Autorebuild for GCC 4.3

* Tue Nov 14 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-8
- Added comment to %%build stating why "_smp_flags" isn't used with make

* Mon Nov 13 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-7
- Modified alsa support patch file to patch "configure.in" instead of "configure"
- Added "autoconf" step to %%build
- Added BuildRequires: autoconf
- Fixed patch backup file suffixes
- Renamed patch files to a more standard format
- Moved header files from /usr/include to /usr/include/flite
- Added -p option to all cp operations (to preserve timestamps)

* Sun Nov 12 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-6
- Recreated patch to allow shared libraries to build correctly (sharedlibs.patch)
- "flite" and "flite_time" binaries now link to flite shared libraries (sharedlibs.patch)
- Simplified the documentation patch filename
- Modified patch steps in %%prep to create backup files with different suffixes
- Removed "_smp_flags" macro from %%build for all archs

* Fri Oct 20 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-5
- Modified "build" so that "_smp_flags" is only used for i386 arch

* Mon Oct 10 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-4
- Removed "_smp_flags" macro from "build" for x86_64 arch

* Tue Sep 26 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-3
- Added README-ALSA.txt (Source1)
- Removed subpackage: flite-devel-static
- Modified shared libraries patch (Patch0) to prevent building static libraries
- Renamed patch files: Patch0, Patch1

* Tue Sep 26 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-2
- Added flite 1.3 ALSA patch (Patch2) by Lukas Loehrer - thanks Anthony Green for pointing it out
- Added configure option: --with-audio=alsa
- Added BuildRequires: alsa-lib-devel

* Fri Sep 22 2006 Francois Aucamp <faucamp@csir.co.za> - 1.3-1
- Initial RPM build
