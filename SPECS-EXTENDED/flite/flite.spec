%bcond_with docs

Name:           flite
Version:        1.3
Release:        36%{?dist}
Summary:        Small, fast speech synthesis engine (text-to-speech)
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            http://www.speech.cs.cmu.edu/flite/

Source0:        http://www.speech.cs.cmu.edu/flite/packed/%{name}-%{version}/%{name}-%{version}-release.tar.gz
Source1:        README-ALSA.txt
Patch0:         flite-1.3-sharedlibs.patch
Patch1:         flite-1.3-doc_texinfo.patch
Patch2:         flite-1.3-alsa_support.patch
Patch3:         flite-1.3-implicit_dso_linking.patch
Patch4:         0001-auserver.c-Only-write-audio-data-to-a-file-in-debug-.patch
Patch5:         flite-0001-Fixed-texi2html-ambiguity.patch

%if %{with docs}
BuildRequires:  texi2html
# texi2pdf
# WARNING see explanation about PDF doc below.
#BuildRequires:  texinfo-tex
%endif

BuildRequires:  gcc
BuildRequires:  autoconf automake libtool
BuildRequires:  ed alsa-lib-devel


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
%setup -q -n %{name}-%{version}-release
%patch0 -p1 -b .flite-1.3-sharedlibs
%patch1 -p1 -b .flite-1.3-doc_texinfo
%patch2 -p1 -b .flite-1.3-alsa_support
%patch3 -p1 -b .flite-1.3-implicit_dso_linking
%patch4 -p1
%patch5 -p1
cp -p %{SOURCE1} .


%build
autoreconf -vif
%configure --enable-shared --with-audio=alsa
# This package fails parallel make (thus cannot be built using "_smp_flags")
make
%if %{with docs}
# Build documentation
cd doc
# WARNING "make doc" provides a huge PDF file. It was decided not to produce/package it.
#make doc
make flite.html
%endif

%install
make install INSTALLBINDIR=%{buildroot}%{_bindir} INSTALLLIBDIR=%{buildroot}%{_libdir}  INSTALLINCDIR=%{buildroot}%{_includedir}/flite


%ldconfig_scriptlets


%files
%license COPYING
%doc ACKNOWLEDGEMENTS README README-ALSA.txt
%if %{with docs}
%doc doc/html
%endif
%{_libdir}/*.so.*
%{_bindir}/*


%files devel
%{_libdir}/*.so
%{_includedir}/flite


%changelog
* Mon Jun 14 2021 Olivia Crain <oliviacrain@microsoft.com> - 1.3-36
- Initial CBL-Mariner import from Fedora 32 (license: MIT).
- Conditionally build documentation, and turn off documentation building by default

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
