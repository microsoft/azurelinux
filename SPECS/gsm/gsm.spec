%global ver_major 1
%global ver_minor 0
%global ver_patch 22

Summary:        Shared libraries for GSM speech compressor
Name:           gsm
Version:        %{ver_major}.%{ver_minor}.%{ver_patch}
Release:        1%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.quut.com/gsm/
Source0:        https://www.quut.com/gsm/%{name}-%{version}.tar.gz

Patch0:         %{name}-makefile.patch
Patch1:         %{name}-warnings.patch

BuildRequires:  gcc

%description
Contains runtime shared libraries for libgsm, an implementation of
the European GSM 06.10 provisional standard for full-rate speech
transcoding, prI-ETS 300 036, which uses RPE/LTP (residual pulse
excitation/long term prediction) coding at 13 kbit/s.

GSM 06.10 compresses frames of 162 13-bit samples (8 kHz sampling
rate, i.e. a frame rate of 50 Hz) into 260 bits; for compatibility
with typical UNIX applications, our implementation turns frames of 160
16-bit linear samples into 33-byte frames (1650 Bytes/s).
The quality of the algorithm is good enough for reliable speaker
recognition; even music often survives transcoding in recognizable
form (given the bandwidth limitations of 8 kHz sampling rate).

The interfaces offered are a front end modelled after compress(1), and
a library API.  Compression and decompression run faster than realtime
on most SPARCstations.  The implementation has been verified against the
ETSI standard test patterns.

%package        tools
Summary:        GSM speech compressor tools

%description    tools
Contains command line utilities for libgsm, an implementation of
the European GSM 06.10 provisional standard for full-rate speech
transcoding, prI-ETS 300 036, which uses RPE/LTP (residual pulse
excitation/long term prediction) coding at 13 kbit/s.

%package        devel
Summary:        Header files and development libraries for libgsm

Requires:       %{name}%{_isa} = %{version}-%{release}

%description    devel
Contains header files and development libraries for libgsm, an
implementation of the European GSM 06.10 provisional standard for
full-rate speech transcoding, prI-ETS 300 036, which uses RPE/LTP
(residual pulse excitation/long term prediction) coding at 13 kbit/s.

%prep
%setup -q -n gsm-%{ver_major}.%{ver_minor}-pl%{ver_patch}
%patch0 -p1 -b .mk
%patch1 -p1 -b .warn

%build
export LDFLAGS="%{?__global_ldflags}"
%make_build all SO_MAJOR=%{ver_major} SO_MINOR=%{ver_minor} SO_PATCH=%{ver_patch}

%install
export LDFLAGS="%{?__global_ldflags}"
mkdir -p %{buildroot}{%{_bindir},%{_includedir}/gsm,%{_libdir},%{_mandir}/{man1,man3}}

make install \
	INSTALL_ROOT=%{buildroot}%{_prefix} \
	GSM_INSTALL_INC=%{buildroot}%{_includedir}/gsm \
	GSM_INSTALL_LIB=%{buildroot}%{_libdir} \
	SO_MAJOR=%{ver_major} SO_MINOR=%{ver_minor} SO_PATCH=%{ver_patch}

# some apps look for this in /usr/include
ln -s gsm/gsm.h %{buildroot}%{_includedir}

# Removing documentation
rm -r %{buildroot}%{_mandir}/man{1,3}

%check
# This is to ensure that the patch creates the proper library version.
[ -f %{buildroot}%{_libdir}/libgsm.so.%{version} ]
export LDFLAGS="%{?__global_ldflags}"
make addtst

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license COPYRIGHT
%doc ChangeLog MACHINES README
%{_libdir}/libgsm.so.*

%files tools
%{_bindir}/tcat
%{_bindir}/toast
%{_bindir}/untoast

%files devel
%dir %{_includedir}/gsm
%{_includedir}/gsm/gsm.h
%{_includedir}/gsm.h
%{_libdir}/libgsm.so

%changelog
* Mon Jan 08 2024 Muhammad Falak <mwani@microsoft.com> 1.0.22-1
- Upgrade version to 1.0.22
- Switch to https URL instead of http

* Tue Jan 19 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.0.19-4
- Initial CBL-Mariner import from Fedora 33 (license: MIT).
- License verified.
- Removed documentation.
- Replaced ldconfig scriptlets with explicit calls to ldconfig.

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.0.19-2
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Wed Apr  1 2020 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.19-1
- New version
  Resolves: rhbz#1818181

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sat Jul 14 2018 Itamar Reis Peixoto <itamar@ispbrasil.com.br> - 1.0.18-3
- include gcc into buildrequires

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon May 21 2018 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.18-1
- update to 1.0.18 (#1575372)

* Wed Mar 07 2018 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.17-5
- ensure binaries are linked with Fedora LDFLAGS (#1548532)
- use ldconfig_scriptlets macro
- add proper man links for tcat and untoast

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.17-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jun 29 2017 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.17-1
- update to 1.0.17 (#1465878)
- ease future updates by better macro use
- drop obsolete patch hunks
- fix missing prototype for fchown warning

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.16-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Nov 24 2016 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.16-1
- update to 1.0.16 (#1397242)
- use license macro
- drop obsolete stuff and simplify

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.13-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.13-8
- Defines changed to globals

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 30 2011 Jaroslav Škarvada <jskarvad@redhat.com> - 1.0.13-5
- Fixed build failure, defuzzified gsm-warnings patch
  Resolves: rhbz#757136

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 16 2010 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.13-3
- update homepage and source URLs

* Wed Jul 29 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.13-2
- Fix dangling symlinks for shared lib, thanks to Lucian Langa for pointing out the issue.

* Tue Jul 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.13-1.1
- Upload sources

* Tue Jul 28 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.13-1
- Update to 1.0.13

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.12-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.0.12-6
- Rebuild for GCC 4.3

* Sun Aug 26 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-5
- install symlinks instead of binaries in -devel

* Sat Aug 25 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-4
- rebuild for BuildID
- specfile cleanups

* Sun May 13 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-3
- fix parallel make

* Fri May 11 2007 Dominik Mierzejewski <rpm[AT]greysector.net> 1.0.12-2
- fix some warnings
- fix 64bit testsuite issue as described at gsm homepage
- add compatibility header symlink
- split off binaries into a separate package

* Sun Apr 15 2007 Michael Schwendt <mschwendt[AT]users.sf.net> 1.0.12-1
- Update to Release 1.0 Patchlevel 12.
- Build with -fPIC not just for non-ix86.
- Add check section to ensure proper library version.
- Remove static library.

* Fri Oct 06 2006 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 1.0.10-12
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Tue Sep 26 2006 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-11
- rebuild for FC6

* Thu Mar 09 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- switch to new release field

* Tue Feb 28 2006 Andreas Bierfert <andreas.bierfert[AT]lowlatency.de>
- add dist

* Mon Jun 27 2005 David Woodhouse <dwmw2@infradead.org>
- 1.0.10-0.lvn.10: Clean up installation

* Sat Jun 25 2005 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 
- 1.0.10-0.lvn.9: mv libgsm.a only when needed

* Fri Dec 31 2004 Thorsten Leemhuis <fedora[AT]leemhuis[DOT]info> 
- 1.0.10-0.lvn.8: Use -fPIC on non ix86

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.lvn.7: moved to rpm.livna.org

* Tue Mar 02 2004 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.7: applied patch from Ville, remove epoch since it's allowed

* Sat Sep 13 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.0.10-0.fdr.6: remove second makeinstall

* Sun Sep 07 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.0.10-0.fdr.5
- added back epochs, I surrender
- fix RPM_OPT_FLAGS hackery

* Fri Jul 18 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.4: remove epoch mentions

* Sat Jul 05 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.3
- pull in RPM_OPT_FLAGS in patch instead of using perl to wedge it in
- fix group
- -p'ize ldconfig

* Tue Jun 10 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 1.0.10-0.fdr.2
- Fix libgsm.so.* being files instead of symlinks

* Thu May 29 2003 Thomas Vander Stichele <thomas at apestaart dot org>
- 0:1.0.10-0.fdr.1: initial RPM release
