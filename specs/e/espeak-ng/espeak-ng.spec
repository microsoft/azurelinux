# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:          espeak-ng
Version:       1.51.1
Release: 13%{?dist}
Summary:       eSpeak NG Text-to-Speech

License:       GPL-3.0-only AND GPL-3.0-or-later AND Apache-2.0 AND BSD-2-Clause AND Unicode-DFS-2016 AND CC-BY-SA-3.0
URL:           https://github.com/espeak-ng/espeak-ng
Source0:       %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires: gcc-g++
BuildRequires: make
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: pkgconfig
BuildRequires: rubygem-ronn
BuildRequires: rubygem-kramdown
BuildRequires: pcaudiolib-devel

# Backported from:
# https://github.com/espeak-ng/espeak-ng/commit/58f1e0b6a4e6aa55621c6f01118994d01fd6f68c
Patch:        espeak-ng-1.51-CVE-2023-49990-4.patch
# backported from upstream for add-text-to-phonemes-with-terminator
Patch:        espeak-ng-1.51-add-translate-clause-with-terminator.patch
# Backported from:
# https://github.com/espeak-ng/espeak-ng/pull/2127/
Patch:        espeak-ng-1.51-add-text-to-phonemes-with-terminator.patch

%description
The eSpeak NG (Next Generation) Text-to-Speech program is an open source speech
synthesizer that supports over 70 languages. It is based on the eSpeak engine
created by Jonathan Duddington. It uses spectral formant synthesis by default
which sounds robotic, but can be configured to use Klatt formant synthesis
or MBROLA to give it a more natural sound.

%package devel
Summary: Development files for espeak-ng
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Development files for eSpeak NG, a software speech synthesizer.

%package vim
Summary: Vim syntax highlighting for espeak-ng data files
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description vim
%{summary}.

%package doc
Summary: Documentation for espeak-ng
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description doc
Documentation for eSpeak NG, a software speech synthesizer.

%prep
%autosetup -p1
# Remove unused files to make sure we've got the License tag right
rm -rf src/include/compat/endian.h src/compat/getopt.c android/

%build
./autogen.sh
%configure
%make_build src/espeak-ng src/speak-ng
make
# Force utf8 for docs building
LC_ALL=C.UTF-8 make docs

%install
%make_install
rm -vf %{buildroot}%{_libdir}/libespeak-ng-test.so*
rm -vf %{buildroot}%{_libdir}/*.{a,la}
# Remove files conflicting with espeak
rm -vf %{buildroot}%{_bindir}/{speak,espeak}
rm -vrf %{buildroot}%{_includedir}/espeak
# Move Vim files
mv %{buildroot}%{_datadir}/vim/addons %{buildroot}%{_datadir}/vim/vimfiles
rm -vrf %{buildroot}%{_datadir}/vim/registry

%check
ESPEAK_DATA_PATH=`pwd` LD_LIBRARY_PATH=src:${LD_LIBRARY_PATH} src/espeak-ng ...

%ldconfig_scriptlets

%files
%license COPYING
%license COPYING.APACHE
%license COPYING.BSD2
%license COPYING.UCD
%doc README.md
%doc CHANGELOG.md
%{_bindir}/speak-ng
%{_bindir}/espeak-ng
%{_libdir}/libespeak-ng.so.1
%{_libdir}/libespeak-ng.so.1.*
%{_datadir}/espeak-ng-data
%{_mandir}/man1/speak-ng.1.gz
%{_mandir}/man1/espeak-ng.1.gz

%files devel
%{_libdir}/pkgconfig/espeak-ng.pc
%{_libdir}/libespeak-ng.so
%{_includedir}/espeak-ng

%files vim
%{_datadir}/vim/vimfiles/ftdetect/espeakfiletype.vim
%{_datadir}/vim/vimfiles/syntax/espeaklist.vim
%{_datadir}/vim/vimfiles/syntax/espeakrules.vim

%files doc
%doc docs/*.html

%changelog
* Mon Oct 06 2025 Jaroslav Škarvada  <jskarvad@redhat.com> - 1.51.1-12
- Backported espeak_TextToPhonemesWithTerminator
  Resolves: rhbz#2393480

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan  3 2024 Jaroslav Škarvada <jskarvad@redhat.com> - 1.51.1-6
- Fixed buffer overflow in SetUpPhonemeTable function at synthdata.c
  Resolves: CVE-2023-49990
- Fixed buffer underflow in CountVowelPosition function at synthdata.c
  Resolves: CVE-2023-49991
- Fixed buffer overflow in RemoveEnding at dictionary.c
  Resolves: CVE-2023-49992
- Fixed buffer overflow in ReadClause function at readclause.c
  Resolves: CVE-2023-49993
- Fixed floating point exception in PeaksToHarmspect at wavegen.c
  Resolves: CVE-2023-49994

* Tue Jan 02 2024 Tomas Korbar <tkorbar@redhat.com> - 1.51.1-5
- Change license tag so it fully conforms to SPDX

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.51.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jun 23 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 1.51.1-1
- New version
  Resolves: rhbz#2100020

* Thu Apr  7 2022 Jaroslav Škarvada <jskarvad@redhat.com> - 1.51-1
- New version
  Resolves: rhbz#2071446

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Jul 13 2020 Tom Stellard <tstellar@redhat.com> - 1.50-3
- Use make macros
- https://fedoraproject.org/wiki/Changes/UseMakeBuildInstallMacro

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.50-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Jan 27 2020 Ondřej Lysoněk <olysonek@redhat.com> - 1.50-1
- New version
- Resolves: rhbz#1778315

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Nov 19 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.49.2-5
- Use C.UTF-8 locale
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Thu Jul 19 2018 Ondřej Lysoněk <olysonek@redhat.com> - 1.49.2-4
- Remove some unsed files in %%prep

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Oct 03 2017 Ondřej Lysoněk <olysonek@redhat.com> - 1.49.2-1
- New version

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.49.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jan 24 2017 Ondřej Lysoněk <olysonek@redhat.com> 1.49.1-2
- Corrected use of the ISA macro
- Included the COPYING.IEEE file

* Tue Jan 24 2017 Ondřej Lysoněk <olysonek@redhat.com> 1.49.1-1
- New version

* Fri Sep 16 2016 Ondřej Lysoněk <olysonek@redhat.com> 1.49.0-1
- Initial package
