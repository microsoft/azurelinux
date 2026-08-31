# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           speech-tools
Version:        2.5
Release:        26%{?dist}
Summary:        Edinburgh speech tools library

License:        MIT-Festival
URL:            http://festvox.org
Source0: http://festvox.org/packed/festival/%{version}/speech_tools-%{version}.0-release.tar.gz
# The license is somewhat specific and only a part of the readme, so it needs to be copied.
# The issue which could change the situation is: https://github.com/festvox/speech_tools/issues/15
Source1: LICENSE
Patch0: enable_shared.patch
Patch1: fix_editline_types.patch

BuildRequires: make
BuildRequires: gcc-c++
BuildRequires: ncurses-devel
BuildRequires: alsa-lib-devel

# Speech-tools did not fix the GCC 10 support as of now.
%define _legacy_common_support 1

%description
The Edinburgh speech tools system is a library of C++ classes, functions
and utility programs that are frequently used in speech software.
The system compiles to a single Unix library .a file
which can be linked with software.
At present, C++ classes for several useful speech and language classes
have been written, along with audio software
and some basic signal processing software.

%prep
%autosetup -n speech_tools -p 0

%build
%configure
# The following make invocation is necessary because configure does not honor the default compiler flags and ignoring those breaks the debuginfo package generation. Also, it disables problematic parallel make.
%__make CFLAGS="%{optflags} -fPIC -flto -fno-lto" CXXFLAGS="%{optflags} -fPIC -flto -fno-lto" LDFLAGS="$LDFLAGS -flto -fno-lto"

%install
mkdir -p %{buildroot}%{_bindir}
# The installation will be handled by the license macro, but it must be somewhere where the paths add up
cp -p %{SOURCE1} .
# The list of installed utilities is taken from the Debian package
install -p -m 755 main/{bcat,ch_lab,ch_track,ch_utt,ch_wave,dp,na_play,na_record,ngram_build,ngram_test,ols,ols_test,pda,pitchmark,scfg_make,scfg_parse,scfg_test,scfg_train,sig2fv,sigfilter,spectgen,tilt_analysis,tilt_synthesis,viterbi,wagon,wagon_test,wfst_build,wfst_run} %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
install -p -m 755 lib/*.so* %{buildroot}%{_libdir}
install -p -m 644 lib/*.a %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}/speech_tools
cp -dr include/* %{buildroot}%{_includedir}/speech_tools
rm -r %{buildroot}%{_includedir}/speech_tools/win32
# I would gladlylike to skip the internal details, but festival depends on them. 
mkdir -p %{buildroot}%{_libdir}/speech_tools/base_class
install -p -m 644 base_class/*.cc %{buildroot}%{_libdir}/speech_tools/base_class
install -p -m 644 base_class/*.h %{buildroot}%{_libdir}/speech_tools/base_class
mkdir -p %{buildroot}%{_libdir}/speech_tools
cp -dr config/ %{buildroot}%{_libdir}/speech_tools
mkdir -p %{buildroot}%{_libdir}/speech_tools/lib/siod
install -p -m 644 lib/siod/*.scm %{buildroot}%{_libdir}/speech_tools/lib/siod
# Note that a symlink would be nice below, but it breaks the expectations around dir traversal.
mkdir -p %{buildroot}%{_libdir}/speech_tools/include
cp -r %{buildroot}%{_includedir}/speech_tools/* %{buildroot}%{_libdir}/speech_tools/include

%files
%{_bindir}/*
%license LICENSE
    
%package libs
Summary: Edinburgh speech tools libraries
Obsoletes: festival-speechtools-libs < 1.2.96-40

%description libs
The shared libraries needed by speech-tools and other software.

%ldconfig_scriptlets libs

%files libs
%{_libdir}/*.so*
%license LICENSE

%package libs-devel
Summary: Development files for the speech-tools libraries
Requires: speech-tools-libs%{?_isa} = %{version}-%{release}
Obsoletes: festival-speechtools-devel < 1.2.96-40

%description libs-devel
This package contains the development related files for the speech-tools
libraries.

%files libs-devel
%{_includedir}/speech_tools/
%{_libdir}/speech_tools/
%{_libdir}/*.so

%package libs-static
Summary: Static libraries of speech-tools, so far needed by at least festival
Requires: speech-tools-libs-devel%{?_isa} = %{version}-%{release}

%description libs-static
This package contains the static libraries for speech-tools.
They are so far definitely needed for festival,
but they might be depended upon by some third-party developers as well.

%files libs-static
%{_libdir}/*.a

%changelog
* Fri Jul 25 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 24 2025 Lukáš Tyrychtr <lukastyrychtr@gmail.com>
- Fix compilation with Gcc 15 by fixing function types

* Sun Jan 19 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Jul 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sat Jan 27 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jul 22 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Apr 17 2023 Lukáš Tyrychtr <lukastyrychtr@gmail.com>
- Migrated to the correct SPDX license

* Sat Jan 21 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sat Jul 23 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Sat Jan 22 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Fri Jul 23 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 Lukáš Tyrychtr <lukastyrychtr@gmail.com> - 2.5-13
Fix building with the latest GCC.

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sun Oct 27 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5-11
- Add Obsoletes for the old festival-speech-tools-devel subpackage too

* Sat Oct 26 2019 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5-10
- Move Obsoletes to the -libs subpackage

* Fri Oct 25 2019 Lukáš Tyrychtr <lukastyrychtr@gmail.com> 2.5-9
- Add an obsoletes directive for the old speech-tools-libs as they're
  no longer part of the Festival package.

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sun Feb 03 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Aug 30 2018 Lukáš Tyrychtr <lukastyrychtr@gmail.com> 2.5-6
- Fix some underscores which got through, somehow.

* Tue Aug 28 2018 Lukáš Tyrychtr <lukastyrychtr@gmail.com> 2.5-5
- Use dash in package name - it makes every reviewer happier.

* Wed Jun 20 2018 Lukáš Tyrychtr <lukastyrychtr@gmail.com> 2.5-4
- Rename the library subpackages to the plural form
- Do not bundle static libraries in the devel subpackage
- Package tle LICENSE file properly

* Tue Apr 24 2018 Lukáš Tyrychtr <lukastyrychtr@gmail.com> 2.5-3
- Add the devel subpackage.

* Fri Apr 20 2018 Lukáš Tyrychtr <lukastyrychtr@gmail.com> 2.5-2
- Do not execute make in parallel.

* Wed Apr 18 2018 Lukáš Tyrychtr <lukastyrychtr@gmail.com> 2.5-1
 Initial release
