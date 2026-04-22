# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

# package options
%global with_portaudio no

%if "%{with_portaudio}" == "yes"
%global backend runtime
%else
%global backend pulseaudio
%endif

Name:           espeak
Version:        1.48.04
Release: 34%{?dist}
Summary:        Software speech synthesizer (text-to-speech)

# Automatically converted from old format: GPLv3+ - review is highly recommended.
License:        GPL-3.0-or-later
URL:            http://espeak.sourceforge.net
Source0:        http://downloads.sourceforge.net/%{name}/%{name}-%{version}-source.zip
# Upstream ticket: https://sourceforge.net/p/espeak/patches/10/
Source1:        espeak.1
Patch0:         espeak-1.47-makefile-nostaticlibs.patch
Patch1:         espeak-1.47-ftbs-ld-libm.patch
# Upstream ticket: https://sourceforge.net/p/espeak/patches/10/
Patch2:         espeak-1.48-help-fix.patch
# Upstream ticket: https://sourceforge.net/p/espeak/bugs/105/
Patch3:         espeak-1.47-wav-close.patch
Patch4:         espeak-1.48-gcc-6-fix.patch
# Upstream-accepted patch (to the new fork espeak-ng)
# https://github.com/espeak-ng/espeak-ng/commit/7659aaa2e88cc0401d032d04602731ca45070fab
Patch5:         espeak-1.48-read-fifo.patch
Requires(post): coreutils
%{?ldconfig:Requires(post): %ldconfig}
%if "%{with_portaudio}" == "yes"
BuildRequires:  portaudio-devel
%endif
BuildRequires:  pulseaudio-libs-devel gcc-c++
BuildRequires: make


%description
eSpeak is a software speech synthesizer for English and other languages.

eSpeak produces good quality English speech. It uses a different synthesis
method from other open source TTS engines, and sounds quite different.
It's perhaps not as natural or "smooth", but some people may find the
articulation clearer and easier to listen to for long periods. eSpeak supports
several languages, however in most cases these are initial drafts and need more
work to improve them.

It can run as a command line program to speak text from a file or from stdin.


%package devel
Summary: Development files for espeak
Requires: %{name} = %{version}-%{release}


%description devel
Development files for eSpeak, a software speech synthesizer.


%prep
%setup -q -n espeak-%{version}-source
%patch -P 0 -p1 -b .nostaticlibs
%patch -P 1 -p1 -b .ftbs-ld-libm
%patch -P 2 -p1 -b .help-fix
%patch -P 3 -p1 -b .wav-close
%patch -P 4 -p1 -b .1.48-gcc-6-fix
%patch -P 5 -p1 -b .read-fifo

# Fix file permissions
find . -type f -exec chmod 0644 {} ";"
# Prepare documentation
rm -rf docs/images/.svn
mv docs html
sed -i 's/\r//' License.txt
# Compile against portaudio v19 (see ReadMe)
cp -f src/portaudio19.h src/portaudio.h
# Don't use the included binary voice dictionaries; we compile these from source
rm -f espeak-data/*_dict


%build
# Compile espeak
cd src
%make_build CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$RPM_LD_FLAGS" DATADIR=%{_datadir}/espeak-data AUDIO=%{backend}

# Compile the TTS voice dictionaries
export ESPEAK_DATA_PATH=$RPM_BUILD_DIR/espeak-%{version}-source
cd ../dictsource
# Strange sed regex to parse ambiguous output from 'speak --voices', filled upstream BZ 3608811
for voice in $(../src/speak --voices | \
LANG=C sed -n '/Age\/Gender/ ! s/ *[0-9]\+ *\([^ ]\+\) *M\? *[^ ]\+ *\(\((\|[A-Z]\)[^ ]\+\)\? *\([^ ]\+\).*/\1 \4/ p' | \
sort | uniq); do \
    ../src/speak --compile=$voice; \
done


%install
rm -rf $RPM_BUILD_ROOT
cd $RPM_BUILD_DIR/espeak-%{version}-source/src
%make_install BINDIR=%{_bindir} INCDIR=%{_includedir}/espeak LIBDIR=%{_libdir} DATADIR=%{_datadir}/espeak-data AUDIO=%{backend}
# Install manpage
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -pf %{SOURCE1} $RPM_BUILD_ROOT%{_mandir}/man1/

%post
%{?ldconfig}

%ldconfig_postun


%files
%doc ReadMe ChangeLog.txt License.txt html
%{_mandir}/man1/espeak.1*
%{_bindir}/espeak
%{_datadir}/espeak-data
%{_libdir}/libespeak.so.*

%files devel
%{_libdir}/*.so
%{_includedir}/espeak


%changelog
* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Thu Jul  25 2024 Miroslav Suchý <msuchy@redhat.com> - 1.48.04-31
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Tue Nov 14 2023 Sandro Bonazzola <sbonazzo@redhat.com> - 1.48.04-27
- Fully drop f21 upgrade compatibility hack
  Resolves: fedora#2239803
- Fix RPM build warnings:
  %%patchN is deprecated (6 usages found), use %%patch N (or %%patch -P N)

* Tue Aug  8 2023 Jaroslav Škarvada <jskarvad@redhat.com> - 1.48.04-26
- Fixed FTBFS, added rpm bug workaround (rhbz#2229971)
  Resolves: rhbz#2225795
- Dropped f21 upgrade compatibility hack

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 22 2020 Tom Stellard <tstellar@redhat.com> - 1.48.04-18
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Aug 11 2016 Ondřej Lysoněk <olysonek@redhat.com> - 1.48.04-9
- Support reading input from named pipes
  Resolves: rhbz#1365338

* Wed Feb 17 2016 Jaroslav Škarvada <jskarvad@redhat.com> - 1.48.04-8
- Fixed FTBFS in f24, gcc-6 related (by gcc-6-fix patch)
  Resolves: rhbz#1307486

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.48.04-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.04-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.48.04-5
- Rebuilt for GCC 5 C++11 ABI change

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.48.04-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.48.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar  7 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.48.04-1
- New version
  Resolves: rhbz#1073920

* Wed Mar  5 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.48.03-1
- New version
  Resolves: rhbz#1072786

* Mon Feb 10 2014 Jaroslav Škarvada <jskarvad@redhat.com> - 1.48.02-1
- New version
  Resolves: rhbz#1060538

* Mon Aug 12 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.11-4
- Fixed truncation of wave file on multi line input
  Resolves: rhbz#967229

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.47.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 15 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.11-2
- Fixed manual page and built-in help to be up-to-date

* Tue May  7 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.11-1
- New version
  Resolves: rhbz#958146
- Defuzzifed patches

* Mon Apr 29 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.08-1
- New version
  Resolves: rhbz#957612

* Fri Apr 19 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.07-1
- New version
  Resolves: rhbz#953772

* Tue Apr 16 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.06-1
- New version
  Resolves: rhbz#952565

* Tue Apr  9 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.05-1
- New version
  Resolves: rhbz#949839, rhbz#922911, rhbz#924831

* Wed Apr  3 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.04-1
- New version
  Resolves: rhbz#947739

* Tue Mar 26 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.03-4
- Added coreutils as post requirement

* Tue Mar 26 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.03-3
- Workaround for RPM bug 924660 rewrote for post

* Sun Mar 24 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.03-2
- Workaround for RPM bug 924660 moved from pretrans to pre
  Resolves: rhbz#926004

* Fri Mar 22 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.03-1
- New version
  Resolves: rhbz#924700
- Workarounded RPM bug 924660 to allow clean update from 1.46 to 1.47
  Resolves: rhbz#924681
- Fixed script for recompilation of voices

* Wed Mar 20 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.47.01-1
- New version
  Resolves: rhbz#923689
- Dropped add-err-check patch (upstreamed)

* Wed Feb 13 2013 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.02-8
- Add err checking (by add-err-check patch)
  Resolves: rhbz#904302

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46.02-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Nov 22 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.02-6
- Reintroduced ftbs_ld_libm patch, it still links with libm

* Thu Oct  4 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.02-5
- Fixed sources URL

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46.02-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar  6 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.02-3
- Conditional portaudio support, portaudio is disabled by default
  Resolves: rhbz#799137

* Fri Jan 27 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.02-2
- Drop portaudio for RHEL

* Fri Jan 13 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.02-1
- New version
  Resolves: rhbz#781355

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.46.01-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 14 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.01-2
- Runtime detection is the default again
  Resolves: rhbz#767434

* Wed Nov 23 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.46.01-1
- New version
- Removed runtime-detection patch (upstreamed)

* Mon Sep 19 2011 Ville Skyttä <ville.skytta@iki.fi> - 1.45.05-3
- Build with $RPM_OPT_FLAGS and $RPM_LD_FLAGS.

* Fri Sep 16 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.45.05-2
- Dropped ftbs_ld_libm patch (not needed now)

* Thu Sep 15 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.45.05-1
- New version
- Updated runtime_detection patch
- Dropped gcc_no_libstdc++ patch

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.43-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 18 2010 Francois Aucamp <faucamp@fedoraproject.org> - 1.43-2
- Added patch declaring explicit libm linking dependency (RHBZ #565186)

* Sat Feb 13 2010 Francois Aucamp <faucamp@fedoraproject.org> - 1.43-1
- Update to version 1.43
- Added patch for runtime detection of pulseaudio, contributed by Kevin Kofler (RHBZ #512190)

* Thu Dec 17 2009 Francois Aucamp <faucamp@fedoraproject.org> - 1.42.04-1
- Update to version 1.42.04
- Revert: build against PortAudio instead of native PulseAudio (RHBZ #512190, #532674)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.40.02-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jun 30 2009 Francois Aucamp <faucamp@fedoraproject.org> - 1.40.02-2
- Compile against pulseaudio instead of portaudio (RHBZ #481651)

* Mon Jun 22 2009 Francois Aucamp <faucamp@fedoraproject.org> - 1.40.02-1
- Update to version 1.40.02
- Added patch to compile with GCC and not to link to libstdc++ (not needed)
- Added manpage (thanks goes to Luke Yelavich from Ubuntu for writing it)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Oct 21 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.39-1
- Update to version 1.39

* Tue Feb 26 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-5
- Export ESPEAK_DATA_PATH in %%build to allow proper compilation of voice dictionaries

* Tue Jan 29 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-4
- Removed libjack patches as they are unnecessary

* Tue Jan 29 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-3
- Added "makefile_libjack" patch to link to libjack
- Added BuildRequires: jack-audio-connection-kit-devel

* Fri Jan 25 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-2
- Removed espeakedit (and associated patches and BuildRequires) from package
  until all phoneme table compilation functions can be moved into espeak (or a
  separate commandline app without wxGTK dependencies)
- Voices are still compiled from source, but using pre-compiled phoneme table
  from upstream until the above issue is resolved

* Thu Jan 24 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.31-1
- Update to version 1.31
- Compile phoneme tables and voice dictionaries from source instead of
  packaging pre-compiled binary data
- Added espeakedit as Source1
- Added BuildRequires: wxGTK-devel for espeakedit
- Added "makefile_rpmoptflags_wxversion" espeakedit patch to enable
  RPM_OPT_FLAGS and set the correct wxWidgets version
- Added "espeak_data_path" espeakedit patch to be able to set control the
  source directory that espeakedit's compiler uses

* Tue Jan 15 2008 Francois Aucamp <faucamp@fedoraproject.org> - 1.30-1
- Update to version 1.30
- Removed local "synthdata_strlen" patch (included upstream)

* Mon Aug 20 2007 Francois Aucamp <faucamp@csir.co.za> - 1.28-1
- Update to version 1.28
- Added "synthdata_strlen" patch to fix memory allocation issue on x86_64 (RHBZ #252712)
- Modified %%prep to build against portaudio v19 for F8 and later
- Upstream license changed from GPLv2+ to GPLv3+

* Tue Jun 19 2007 Francois Aucamp <faucamp@csir.co.za> - 1.26-1
- Update to version 1.26
- Modified %%prep to build against portaudio v19

* Tue Jun 05 2007 Francois Aucamp <faucamp@csir.co.za> - 1.25-1
- Update to version 1.25

* Tue May 08 2007 Francois Aucamp <faucamp@csir.co.za> - 1.24-1
- Update to version 1.24

* Tue Apr 24 2007 Francois Aucamp <faucamp@csir.co.za> - 1.23-1
- Update to version 1.23
- Added "makefile_nostaticlibs" patch so static libraries aren't installed

* Thu Feb 08 2007 Francois Aucamp <faucamp@csir.co.za> - 1.20-1
- Update to version 1.20
- Solves stack smash bug (RHBZ #227316)

* Fri Jan 26 2007 Francois Aucamp <faucamp@csir.co.za> - 1.19-1
- Update to version 1.19
- Removed "espeak-1.18-makefile_lpthread" patch as it has been included upstream
- Removed "espeak-1.18-makefile_smp" patch as it has been included upstream
- Removed "espeak-1.18-ptr_64bit" patch as it has been solved upstream
- Fixed espeak-data file permissions

* Tue Jan 16 2007 Francois Aucamp <faucamp@csir.co.za> - 1.18-2
- Created "espeak-1.18-ptr_64bit" patch to allow compilation on x86_64 (fixes 64-bit pointer issues)
- Created "espeak-1.18-makefile_smp" patch to allow parallel make ("_smp_mflags")
- Renamed "makefile_lpthread" patch to "espeak-1.18-makefile_lpthread"

* Mon Jan 15 2007 Francois Aucamp <faucamp@csir.co.za> - 1.18-1
- Update to version 1.18
- Dropped statically-linked "speak" executable (replaced by dynamically-linked "espeak" executable)
- Removed the "espeak program name" patch as it has been included upstream
- Removed "espeak program name" patch backup file cleanup from %%install
- Minor modification to "makefile lpthread" patch to account for new lib/executable
- Removed "BIN_NAME" variable from make in %%build (implemented upstream)

* Mon Nov 20 2006 Francois Aucamp <faucamp@csir.co.za> - 1.17-1
- Update to version 1.17
- Removed "makefile install target" patch as it has been included upstream
- Removed "AMD64 sizeof(char *)" patch as it has been included upstream
- Minor modification to "espeak program name" patch to allow patching current version

* Tue Nov 07 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-4
- Modified patch steps to create backups with different suffixes
- Renamed patch file extensions to .patch
- Added step in %%install to remove patch backup files in documentation

* Sat Nov 04 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-3
- Fixed source file permissions for -debuginfo package in %%prep
- Added RPM_OPT_FLAGS to "make" command in %%build; removed RPM_OPT_FLAGS makefile patch
- Modified makefile install target patch to include general support for setting compiler optimization flags via CXXFLAGS
- Removed creation of .orig backup files during patching
- Modified patch files to have different suffixes

* Thu Nov 02 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-2
- Added "install" target to makefile (makefile_install_target.patch)
- Added patch to fix AMD64 sizeof(char *) assumption bug (upstream request ID 1588938)
- Changed "portaudio" BuildRequires to "portaudio-devel"
- Added patch to makefile to allow RPM_OPT_FLAGS
- Added patch to replace all references to "speak" binary with "espeak"
- Moved header files to /usr/include/espeak
- Added rmdir command to "install" to remove empty soundicons directory

* Wed Oct 04 2006 Francois Aucamp <faucamp@csir.co.za> - 1.16-1
- Initial RPM build
