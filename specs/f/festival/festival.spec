## START: Set by rpmautospec
## (rpmautospec version 0.8.4)
## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 29;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec

# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name: festival
Summary: Speech synthesis and text-to-speech system
Version: 2.5.0
Release: %autorelease

URL: http://www.cstr.ed.ac.uk/projects/festival/
# The Emacs file is GPL+, there is one TCL-licensed source file, and
# the hts_engine module is covered by the three-clause BSD license.
License: MIT AND GPL-1.0-or-later AND TCL AND BSD-3-Clause

Obsoletes: festival-lib
Obsoletes: festival-speechtools-libs
Obsoletes: festival-speechtools-libs-devel
Obsoletes: festival-speechtools-utils

# Files needed for everything...
%global baseURL  http://festvox.org/packed/festival/2.5
Source0: %{baseURL}/festival-%{version}-release.tar.gz

### DICTIONARIES
# Generic English dictionary
Source100: %{baseURL}/festlex_POSLEX.tar.gz
# American English dictionary
Source101: %{baseURL}/festlex_CMU.tar.gz
# OALD isn't included because it's got a more restrictive (non-commercial
# only) license. OALD voices not included for same reason.

# Note on voice versions: I'm simply using the file date of the newest file
# in each set of tarballs. It happens that the dates for all files from each
# source (diphone, cmu_arctic, etc.) match, which is handy.

### DIPHONE VOICES
%global diphoneversion 0.19990610
Source200: %{baseURL}/voices/festvox_kallpc16k.tar.gz
Source202: %{baseURL}/voices/festvox_rablpc16k.tar.gz

### HTS VOICES
Source220: %{baseURL}/voices/festvox_cmu_us_awb_cg.tar.gz
Source221: %{baseURL}/voices/festvox_cmu_us_bdl_cg.tar.gz
Source222: %{baseURL}/voices/festvox_cmu_us_clb_cg.tar.gz
Source223: %{baseURL}/voices/festvox_cmu_us_jmk_cg.tar.gz
Source224: %{baseURL}/voices/festvox_cmu_us_rms_cg.tar.gz
Source225: %{baseURL}/voices/festvox_cmu_us_slt_cg.tar.gz

### Hispavoces Spanish voices left out; did they move?

### Multisyn voices left out because they're ~ 100MB each.

### MBROLA voices left out, because they require MBROLA, which ain't free.

### Systemd service file.
Source230: festival.service

Patch100: festival-2.5.0-pulseaudio.patch
Patch101: festival-2.5.0-use-system-speech-tools.patch
Patch102: festival-2.5.0-use-system-libs.patch
Patch103: festival-2.5.0-filesystem-standard.patch
Patch104: festival-2.5.0-siteinit.patch
Patch105: festival-configure-c99.patch

BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: alsa-lib-devel
BuildRequires: pulseaudio-libs-devel
BuildRequires: texi2html
BuildRequires: ncurses-devel
BuildRequires: speech-tools-libs-devel
BuildRequires: speech-tools-libs-static
BuildRequires: systemd
BuildRequires: make
%{?systemd_requires}

# Requires: festival-voice
# The hard dep below provides a festival-voice, no need to require it here.

# This is hard-coded as a requirement because it's the smallest voice (and,
# subjectively I think the most pleasant to listen to and so a good
# default).
#
# Ideally, this would be a "suggests" instead of a hard requirement.
#
# Update: with the new nitech versions of the voices, slt-arctic is no
# longer the smallest. But... AWB has a strong scottish accent, and JMK a
# kind of odd canadian one, so they're not great candidates for inclusion.
# And I find RMS a bit hard to understand. BDL isn't much smaller than SLT,
# and since I like it better, I think I'm going to keep it as the default
# for a price 12k. So, in case anyone later questions why this is the
# default, there's the answer. :)
Requires: festvox-slt-arctic-hts

# festival-2.5.0-pulseaudio.patch makes use of paplay.
Requires:  pulseaudio-utils

Requires: festival-data = %{version}-%{release}
Requires: speech-tools-libs

%package -n festvox-kal-diphone
Summary: American English male speaker "Kevin" for Festival
Version: %{diphoneversion}
Provides: festival-voice
Provides: festvox-kallpc16k
BuildArch: noarch

%package -n festvox-rab-diphone
Summary: American English male speaker "Kurt" for Festival
Version: %{diphoneversion}
Requires: festival
Provides: festival-voice
Provides: festvox-rablpc16k
BuildArch: noarch

%package -n festvox-awb-arctic-hts
Summary: Scottish-accent US English male speaker "AWB" for Festival
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-bdl-arctic-hts
Summary: US English male speaker "BDL" for Festival
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-clb-arctic-hts
Summary: US English female speaker "CLB" for Festival
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-jmk-arctic-hts
Summary: Canadian-accent US English male speaker "JMK" for Festival
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-rms-arctic-hts
Summary: US English male speaker "RMS" for Festival
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package -n festvox-slt-arctic-hts
Summary: US English female speaker "SLT" for Festival
Requires: festival
Provides: festival-voice
BuildArch: noarch

%package data
Summary: Data files for the Festival speech synthesis system
BuildArch: noarch

# This is last as a lovely hack to make sure Version gets set back
# to what it should be. Grr.
%package devel
Summary: Development files for the Festival speech synthesis system
# Note: rpmlint complains incorrectly about
# "no-dependency-on festival"
Requires: speech-tools-libs-devel
Provides: festival-static = %{version}-%{release}



%description
Festival is a general multi-lingual speech synthesis system developed
at CSTR. It offers a full text to speech system with various APIs, as
well as an environment for development and research of speech synthesis
techniques. It is written in C++ with a Scheme-based command interpreter
for general control.

%description -n festvox-kal-diphone
American English male speaker ("Kevin") for Festival.

This voice provides an American English male voice using a residual excited
LPC diphone synthesis method. It uses the CMU Lexicon pronunciations.
Prosodic phrasing is provided by a statistically trained model using part of
speech and local distribution of breaks. Intonation is provided by a CART
tree predicting ToBI accents and an F0 contour generated from a model
trained from natural speech. The duration model is also trained from data
using a CART tree.


%description -n festvox-rab-diphone
British English male speaker ("RAB") for Festival.

This voice provides a British English male voice using a residual excited
LPC diphone synthesis method. It uses the CMU Lexicon for pronunciations.
Prosodic phrasing is provided by a statistically trained model using part of
speech and local distribution of breaks. Intonation is provided by a CART
tree predicting ToBI accents and an F0 contour generated from a model
trained from natural speech. The duration model is also trained from data
using a CART tree.


%description -n festvox-awb-arctic-hts
US English male speaker ("AWB") for Festival. AWB is a native Scottish
English speaker, but the voice uses the US English front end.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1138 utterances spoken by a Scottish English male speaker. The
speaker is very experienced in building synthetic voices and matched
prompted US English, though his vowels are very different from US English
vowels. Scottish English speakers will probably find synthesizers based on
this voice strange. Unlike the other CMU_ARCTIC databases this was recorded
in 16 bit 16KHz mono without EGG, on a Dell Laptop in a quiet office. The
database was automatically labelled using CMU Sphinx using the FestVox
labelling scripts. No hand correction has been made.


%description -n festvox-bdl-arctic-hts
US English male speaker ("BDL") for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English male speaker. The speaker
is experienced in building synthetic voices. This was recorded at 16bit
32KHz, in a sound proof room, in stereo, one channel was the waveform, the
other EGG. The database was automatically labelled using CMU Sphinx using
the FestVox labelling scripts. No hand correction has been made.


%description -n festvox-clb-arctic-hts
US English female speaker ("CLB") for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English female speaker. The
speaker is experienced in building synthetic voices. This was recorded at
16bit 32KHz, in a sound proof room, in stereo, one channel was the waveform,
the other EGG. The database was automatically labelled using CMU Sphinx
using the FestVox labelling scripts. No hand correction has been made.


%description -n festvox-jmk-arctic-hts
US English male speaker ("JMK") voice for Festival. JMK is a native Canadian
English speaker, but the voice uses the US English front end.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1138 utterances spoken by a US English male speaker. The speaker
is experienced in building synthetic voices. This was recorded at 16bit
32KHz, in a sound proof room, in stereo, one channel was the waveform, the
other EGG. The database was automatically labelled using CMU Sphinx using
the FestVox labelling scripts. No hand correction has been made.

%description -n festvox-rms-arctic-hts
US English male speaker ("RMS") voice for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English male speaker. The speaker
is experienced in building synthetic voices. This was recorded at 16bit
32KHz, in a sound proof room, in stereo, one channel was the waveform, the
other EGG. The database was automatically labelled using EHMM an HMM labeler
that is included in the FestVox distribution. No hand correction has been
made.

%description -n festvox-slt-arctic-hts
US English female speaker ("SLT") voice for Festival.

This is a HMM-based Speech Synthesis System (HTS) voice from the Nagoya
Institute of Technology, trained using the CMU ARCTIC database. This voice
is based on 1132 utterances spoken by a US English female speaker. The
speaker is experienced in building synthetic voices. This was recorded at
16bit 32KHz, in a sound proof room, in stereo, one channel was the waveform,
the other EGG. The database was automatically labelled using CMU Sphinx
using the FestVox labelling scripts. No hand correction has been made.

%description data
Data files for the Festival speech synthesis system.

%description devel
Development files for the Festival speech synthesis system. Install
festival-devel if you want to use Festival's capabilities from within your
own programs, or if you intend to compile other programs using it. Note that
you can also interface with Festival in via the shell or with BSD sockets.



%prep
%setup -q -n festival

# dictionaries
%setup -q -n festival -D -T -b 100
%setup -q -n festival -D -T -b 101

# voices
%setup -q -n festival -D -T -b 200
%setup -q -n festival -D -T -b 202
%setup -q -n festival -D -T -b 220
%setup -q -n festival -D -T -b 221
%setup -q -n festival -D -T -b 222
%setup -q -n festival -D -T -b 223
%setup -q -n festival -D -T -b 224
%setup -q -n festival -D -T -b 225

%patch -P100 -p1 -b .pulseaudio
%patch -P101 -p1 -b .use-system-speech-tools
%patch -P102 -p1 -b .use-system-libs
%patch -P103 -p1 -b .filesystem-standard
%patch -P104 -p1 -b .siteinit
%patch -P105 -p1

# Create a sysusers.d config file
cat >festival.sysusers.conf <<EOF
u festival - 'festival Daemon' - -
EOF

%build

# build the main program
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$(pwd)/src/lib
# instead of doing this, maybe we should patch the make process
# so it looks in the right place explicitly:
export PATH=$(pwd)/bin:$PATH
%configure
make \
  EST=%{_libdir}/speech_tools \
  LIBDIR="%{_libdir}" \
  CFLAGS="$RPM_OPT_FLAGS -fPIC" \
  CXXFLAGS="$RPM_OPT_FLAGS -fPIC"

# build the patched CMU dictionary
make -C lib/dicts/cmu


%install
# "make install" for this package is, um, "interesting". It seems geared for
# local user-level builds. So, rather than doing that and then patching it
# up, do the right parts by hand as necessary.

# Create %{_libdir} because make install copies to it without first creating.
mkdir -p $RPM_BUILD_ROOT%{_libdir}

# install the dictionaries
TOPDIR=$( pwd )
pushd lib/dicts
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/dicts
  # we want to put the licenses in the docs...
  cp COPYING.poslex $OLDPWD/COPYING.poslex
  cp cmu/COPYING $OLDPWD/COPYING.cmudict
  for f in wsj.wp39.poslexR wsj.wp39.tri.ngrambin ; do
    install -p -m 644 $f $RPM_BUILD_ROOT%{_datadir}/festival/dicts/
  done
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/dicts/cmu
  pushd cmu
    # note I'm keeping cmudict-0.4.diff and cmudict_extensions.scm to
    # satisfy the "all changes clearly marked" part of the license -- these
    # are the changes. And yes, the ".out" file is the one actually used.
    # Sigh.
    for f in allowables.scm cmudict-0.4.diff cmudict-0.4.out \
             cmudict_extensions.scm cmulex.scm cmu_lts_rules.scm; do
      install -p -m 644 $f $RPM_BUILD_ROOT%{_datadir}/festival/dicts/cmu/
    done
  popd
popd

# install the voices
pushd lib/voices
  # get the licenses. This is probably too clever by half, but oh well.
  for f in $( find . -name COPYING ); do
    n=$( echo $f | sed 's/.*\/\(.*\)\/COPYING/COPYING.\1/' )
    mv $f $OLDPWD/$n
  done
popd
cp -a lib/voices $RPM_BUILD_ROOT%{_datadir}/festival

# okay, now install the main festival program.

# binaries:
make INSTALLED_BIN=$RPM_BUILD_ROOT%{_bindir} make_installed_bin_static
install -p -m 755 bin/text2wave $RPM_BUILD_ROOT%{_bindir}

# install the library
cp -a src/lib/libFestival.a $RPM_BUILD_ROOT%{_libdir}

# this is just nifty. and it's small.
install -p -m 755 examples/saytime $RPM_BUILD_ROOT%{_bindir}

# man pages
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
cp -a doc/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

# lib: the bulk of the program -- the scheme stuff and so on
pushd lib
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival
  for f in *.scm festival.el *.ent *.gram *.dtd *.ngrambin speech.properties ; do
    install -p -m 644 $f $RPM_BUILD_ROOT%{_datadir}/festival/
  done
  mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/multisyn/
  install -p -m 644 multisyn/*.scm $RPM_BUILD_ROOT%{_datadir}/festival/multisyn/
popd

# Remove comments that look like this:
#
# 	;;; The master copy of this file is in /usr/{lib,lib64}/speech_tools/lib/siod/cstr.scm
#
# Such comments exist in files generated by lib/Makefile and thus vary between
# builds based on the value of %_libdir. Furthermore,
# /usr/lib*/speech_tools/* might not exist on the user system.
sed -r -i '/The master copy of this file is in|and is copied here at build time/d' \
  $RPM_BUILD_ROOT%{_datadir}/festival/*.scm

# "etc" -- not in the configuration sense, but in the sense of "extra helper
# binaries".
pushd lib/etc
  mkdir -p $RPM_BUILD_ROOT%{_libexecdir}/festival
  install -p -m 755 */audsp $RPM_BUILD_ROOT%{_libexecdir}/festival
popd

# copy in the intro.text. It's small and makes (intro) work. in the future,
# we may want include more examples in an examples subpackage
mkdir -p $RPM_BUILD_ROOT%{_datadir}/festival/examples/
install -p -m 644 examples/intro.text $RPM_BUILD_ROOT%{_datadir}/festival/examples


# header files
mkdir -p $RPM_BUILD_ROOT%{_includedir}/festival
cp -a src/include/* $RPM_BUILD_ROOT%{_includedir}/festival


# systemd service
mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p -m 644 %{SOURCE230} $RPM_BUILD_ROOT%{_unitdir}/

install -m0644 -D festival.sysusers.conf %{buildroot}%{_sysusersdir}/festival.conf

%files
%doc ACKNOWLEDGMENTS NEWS README.md
%license COPYING COPYING.poslex COPYING.cmudict
%{_bindir}/default_voices
%{_bindir}/festival
%{_bindir}/festival_client
%{_bindir}/festival_server
%{_bindir}/festival_server_control
%{_bindir}/text2wave
%{_bindir}/saytime
%{_libexecdir}/festival
%{_mandir}/man1/*
%{_unitdir}/festival.service
%{_sysusersdir}/festival.conf


%post
%systemd_post festival.service

%preun
%systemd_preun festival.service

%postun
%systemd_postun_with_restart festival.service

%files -n festvox-kal-diphone
%license COPYING.kal_diphone
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/english
%{_datadir}/festival/voices/english/kal_diphone

%files -n festvox-rab-diphone
%license COPYING.rab_diphone
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/english
%{_datadir}/festival/voices/english/rab_diphone

%files -n festvox-awb-arctic-hts
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/us
%{_datadir}/festival/voices/us/cmu_us_awb_cg

%files -n festvox-bdl-arctic-hts
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/us
%{_datadir}/festival/voices/us/cmu_us_bdl_cg

%files -n festvox-clb-arctic-hts
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/us
%{_datadir}/festival/voices/us/cmu_us_clb_cg

%files -n festvox-jmk-arctic-hts
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/us
%{_datadir}/festival/voices/us/cmu_us_jmk_cg

%files -n festvox-rms-arctic-hts
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/us
%{_datadir}/festival/voices/us/cmu_us_rms_cg

%files -n festvox-slt-arctic-hts
%dir %{_datadir}/festival/voices
%dir %{_datadir}/festival/voices/us
%{_datadir}/festival/voices/us/cmu_us_slt_cg

%files data
%{_datadir}/festival
%exclude %{_datadir}/festival/voices/*
%dir %{_datadir}/festival/voices

%files devel
%license COPYING
%{_libdir}/libFestival.a
%dir %{_includedir}/festival
%{_includedir}/festival/*


%changelog
## START: Generated by rpmautospec
* Wed Apr 22 2026 azldev <azurelinux@microsoft.com> - 2.5.0-29
- Latest state for festival

* Wed Jul 23 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Tue Feb 11 2025 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.0-27
- Add sysusers.d config file to allow rpm to create users/groups
  automatically

* Thu Jan 16 2025 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Wed Jan 01 2025 W. Michael Petullo <mike@flyn.org> - 2.5.0-25
- Review and adjust license after SPDX cleanup

* Wed Aug 28 2024 Miroslav Suchý <msuchy@redhat.com> - 2.5.0-24
- convert license to SPDX

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Tue Jul 02 2024 W. Michael Petullo <mike@flyn.org> - 2.5.0-22
- Revise commentary on comment-removal line

* Mon Jul 01 2024 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.0-21
- Remove comment which makes build irreproducible

* Thu May 30 2024 Software Management Team <packaging-team-maint@redhat.com> - 2.5.0-20
- Eliminate use of obsolete %%patchN syntax (#2283636)

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Jan 30 2023 Florian Weimer <fweimer@redhat.com> - 2.5.0-16
- Port configure script to C99

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Sun Sep 11 2022 W. Michael Petullo <mike@flyn.org> - 2.5.0-14
- Avoid uname in architechture check, because "uname -p" does not work in
  mock

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Mar 02 2021 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.0-15
- Rebuilt for updated systemd-rpm-macros
  See https://pagure.io/fesco/issue/2583.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon May 18 2020 W. Michael Petullo <mike@flyn.org> - 2.5.0-12
- Require pulseaudio-utils for paplay

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Oct 21 2019 W. Michael Petullo <mike@flyn.org> - 2.5.0-10
- Obsolete four packages that would otherwise conflict with required speech-tools

* Wed Oct 16 2019 W. Michael Petullo <mike@flyn.org> - 2.5.0-9
- Fix build on s390x, ppc64le, and aarch64

* Sun Oct 13 2019 W. Michael Petullo <mike@flyn.org> - 2.5.0-8
- Remove empty lib subpackage
- Fix make command line (add missing '\')
- Use -p with install
- Do not create %{_sysconfdir}/festival
- Do not create %{_infodir}
- Simplify %files
- Note BSD license for hts_engine module
- Split data into noarch package
- The festival-devel package now provides festival-static
- Markup additional files as licenses

* Sun Jan 27 2019 W. Michael Petullo <mike@flyn.org> - 2.5.0-7
- Add more BuildRequires
- Remove use of festivalversion
- Drop Group:
- Replace define with global
- Reorder BuildRequires
- Remove deprecated post, preun, and postun statements
- Remove verbose pushd use
- Do not explicitly call ldconfig
- Label COPYING properly

* Sun Sep 09 2018 W. Michael Petullo <mike@flyn.org> - 2.5.0-6
- Apply siteinit patch
- Drop lib from %{_datadir}/festival/lib
- Move audsp
- Drop email_filter

* Thu Sep 06 2018 W. Michael Petullo <mike@flyn.org> - 2.5.0-5
- Patch to use more reasonable install locations
- Provide systemd service file

* Wed Aug 29 2018 W. Michael Petullo <mike@flyn.org> - 2.5.0-4
- Do not explicitly run ldconfig
- Remove speechtools definitions
- Make use of system-installed speech-tools
- BuildRequire speech-tools-libs-static
- Fix some URLs
- Set debug_package to null; see comment at top
- Set LIBDIR on make
- Create $RPM_BUILD_ROOT%{_libdir} before make install

* Tue Aug 28 2018 W. Michael Petullo <mike@flyn.org> - 2.5.0-3
- Remove speech-tools and use package proposed in Bugzilla #1592220

* Sun Jul 22 2018 W. Michael Petullo <mike@flyn.org> - 2.5.0-2
- Adjust soname using modification of patch from 1.96-38
- Place audsp where festival can find it
- Configure festival to use pulseaudio

* Sun Jul 22 2018 W. Michael Petullo <mike@flyn.org> - 2.5.0-1
- Update to 2.5.0
- Drop separate versions for speech_tools and docs
- Drop out-of-date patches
- Revert to Festival-distributed voices rather than NIT
- Drop Hispavoces voices for now
- Use sed to adjust config.in files
- A number of voices no longer have README files
- Build libFestival as a static library for now
- Drop siteinit.scm and sitevars.scm
- Drop info files
- Drop docs package for now
- Switch ked to rab

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.96-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.96-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jan 31 2018 Than Ngo <than@redhat.com> - 1.96-36
- add BR on texi2html instead tetex, minimal tex BR
- fix FTBS with gcc7

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.96-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.96-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.96-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.96-32
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat May 02 2015 Kalev Lember <kalevlember@gmail.com> - 1.96-30
- Rebuilt for GCC 5 C++11 ABI change

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon May 12 2014 Jaromir Capik <jcapik@redhat.com> - 1.96-27
- Fixing format security flaws (#1037060)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Mar 02 2013 Bruno Wolff III <bruno@wolff.to> - 1.96-25
- Fix typo in server script - bz 614200

* Thu Feb 07 2013 Jon Ciesla <limburgher@gmail.com> - 1.96-24
- Minor Merge review fixes, BZ 225748.

* Mon Jan  7 2013 Matthias Clasen <mclasen@redhat.com> - 1.96-23
- Add tighter inter-subpackage deps (recommended by rpmdiff)

* Mon Jan  7 2013 Matthias Clasen <mclasen@redhat.com> - 1.96-22
- Fix directory ownership for /usr/share/festival/lib/voices/es

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Feb 25 2012 Bruno Wolff III <bruno@wolff.to> - 1.96-20
- Fix to build with gcc 4.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 22 2011 Tim Niemueller <tim@niemueller.de> - 1.96-18
- Fix install paths of speech_tools includes (rhbz #242607)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Sep 29 2009 Matthias Clasen <mclasen@redhat.com> - 1.96-16
- Add native pulseaudio support (#471047)

* Thu Sep 10 2009 Bernie Innocenti <bernie@codewiz.org> - 1.96-15
- Disable esd support (resolves: rhbz#492982)

* Wed Jul 29 2009 Matthias Clasen <mclasen@redhat.com> - 1.96-14
- Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Apr 18 2009 Matthias Clasen <mclasen@redhat.com> - 1.96-12
- Add Spanish voices from the guadalinex project, in the
  hispavoces-pal-diphone and hispavoces-sfl-diphone subpackages
  (#496011)

* Tue Mar 24 2009 Jesse Keating <jkeating@redhat.com> - 1.96-11
- Drop the explicit dep on festival-voice, as it is redundant and
  causes problems with multiple providers

* Thu Feb 26 2009 Matthias Clasen  <mclasen@redhat.com> 1.96-10
- Fix build with gcc 4.4

* Tue Feb 24 2009 Matthias Clasen  <mclasen@redhat.com> 1.96-9
- Make -docs and all the festvox subpackages noarch

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.96-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 23 2008 Matthias Clasen <mclasen@redhat.com> - 1.96-7
- Tweak summaries

* Mon Oct 27 2008 Ray Strode <rstrode@redhat.com> - 1.96-6
- interoperate with other apps by using pacat for audio output
  (bug 467531)

* Fri Jul 18 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 1.96-5
- fix license tag

* Fri Feb 22 2008 Matthias Clasen  <mclasen@redhat.com> - 1.96-4
- Fix the build with gcc 4.3

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.96-3
- Autorebuild for GCC 4.3

* Wed Nov  7 2007 Stepan Kasal <skasal@redhat.com>1.96-2
- fix a typo in a summary and in festival-1.96-nitech-proclaimvoice.patch
- Resolves: #239216

* Tue Mar 20 2007 Ray Strode <rstrode@redhat.com> 1.96-1
- rebuild

* Mon Mar 19 2007 David Zeuthen <davidz@redhat.com> 1.96-0.11
- Forgot to add the .scm files

* Mon Mar 19 2007 David Zeuthen <davidz@redhat.com> 1.96-0.10
- Update to Matthew Miller's much improved package (#232105)
- Move the buildroot patch around

* Sun Mar 18 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.9
- fix the library link patch to use -lncurses instead of -ltinfo --
  the later is all that's really needed, but the former works on older
  distros too.

* Fri Mar 16 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.8
- festival-devel depends on the libraries package, not base festival. this
  raises an multilib question: need to obsolete festival.i386 on x86_64.
  Right now, there's no mechanism for doing that. Fortunately, all the
  changes in packaging happen to make it so that the current version doesn't
  conflict with the old release, so one will get unused cruft but not
  breakage when upgrading.
- Bite teh proverbial bullet and make libFestival build shared.
- update speech-tools soname patch to work in the more general case needed
  by the festival main build
- make said shared-lib a subpackage to avoid multiarching the whole thing
- split festival-devel and speechutils-devel in anticipation of future
  plan of actually decoupling these packages.
- note that rpmlint complains about "missing" deps on the devel packages. it
  should be fixed to recognize requiring a -lib/libs package is sufficent or
  better.
- add saytime script. Because, really, what else is this package *for*?
- add the intro.text so (intro) works. 196 more bytes won't kill us. :)
- remove $PATH from LD_LIBRARY_PATH used in build. (What the heck?)
- add defattr to all subpackages. I don't think it's strictly necessary
  since putting it in the first package seems sufficient, but that's
  probably not behavior to count on.
- make descriptions and summaries use more consistant language

* Thu Mar 15 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.7
- Upstream baseurl now includes version. (Thanks Alan Black @ cmu)
- Update siteinit patch to also incorporate sitevars
- Add sitevars as a config file
- Ship our own siteinit and sitevars as sources
- In default sitevars, reference /usr/local/share/festival/lib as another
  place to look for voices (it's okay if that doesn't exist). Hopefully,
  this will encourage people who want to install non-RPM-packaged voices to
  keep from doing it in /usr/share.
- Fix wrong references to slt voice in other nitech voices
- Fix wrongly commented-out (require 'f2bf0lr) in awb, clb, and rms voices.
- Stop untarring source files and use the setup macro properly.
- Get rid of silly DATA.TMP directories for installing voices and 
  dictionaries.
- Stop making ../speechtools link. Currently solved by patching to look
  in the current directory; could also do this by moving everything up
  a directory.
- TODO: festival-buildroot.patch could stand to be updated. May not
  even be needed anymore.
- Drop the 8k versions of the diphone voices, since there's not really
  any point. If you want smaller, use one of the arctic_hts voices
  instead. And overall, this saves us about 4.5M.

* Wed Mar 14 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.6
- Fix copy-paste error in JMK description (thanks Matthias Clasen)
- Remove "nitech-us-" from the names of those voice packages to make the
  package names shorter. (This will also be more convenient if we switch to
  the cmu versions in the future.)
- made aliases so old cmu_us_*_arctic_hts voice names still work.
- Look for /etc/festival/siteinit.scm (and move siteinit.scm there!)
- Mark siteinit.scm as a config file
- Remove some non-useful stuff from speech-tools-utils.
- Move main dir from /usr/share/festival to /usr/share/festival/lib at
  request of upstream. Also, we can drop the FHS (well, "fsstnd" -- it's
  old) patch and just pass FTLIBDIR to make. Which, hey, we were already
  doing. Yay redundancy.
- clean up CFLAGS and CXXFLAGS. "-fpermissive" was hiding bad stuff.
- update speech tools with patch from AWB to fix 64-bit build issue 
  with EST_DProbDist
- there's still some compiler warnings which should be addressed upstream.
- The nitech hts voices don't properly proclaim_voice, making them not
  show up for gnome-speech and thus making orca crash. See details in the
  comments in bug #232105.

* Tue Mar 13 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.5
- use festvox- instead of festival-voice for voice packages -- matches
  upstream tarballs, and is shorter. Also, use shorter form of
  the date-based version.
- get the README.htsvoice from the nitech voices -- it contains
  license info.
- build (but don't enable by default) ESD support in speech-tools (bug
  #198908)
- fix coding error noted in bug #162137 -- need to push this upstream.
- link speech tools libraries with -lm, -ltermcap, -lesd and with themselves
  (bug #198190, partially)
- holy sheesh. Use g++ for CXX, not gcc. Fixes bug #198190 completely.

* Tue Mar 13 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.4
- subpackages! Split out speech-tools, docs, voices.
- long descriptions for the individual voices, carefully gathered from
  readmes and web sites.
- ooh. replace cmu_hts voices with the updated versions from upstream
  <http://hts.sp.nitech.ac.jp/>. Two new voices, and updated versions of
  the others. (The voices packaged at festvox.org are apparently based on
  older versions of these, which in turn are from the CMU upstream.)
- TODO: make aliases for the cmu voices.
- arguably, voices should be made in to their own src.rpms. They don't need
  anything from here to build. That's for a future version. (At that time,
  the gigantic multisyn voices could be added.) The CMU dict needs festival
  installed to build, but I don't think it needs the source, so dicts could
  be subpackages too. And the docs are also a good candidate for separation.
  speech-tools, though, is incestuously used in the festival build process
  and I think it makes sense to keep that bundled.
- TODO: check through the speechtools-utils for what should actually be 
  packaged; fix the include path for siod (and anything else that needs it).
- TODO: package festival.el so it just works with emacs.
- TODO: reinvent festival_server_control as a proper init script
- TODO: put the festival server in sbin, maybe?
- Another question: should we drop the 8k diphone voices? Any point?
- Changed "X11-like" to "MIT-style" (which is what X11 is) to make rpmlint
  happy.
- make %%{festivalversion} macro to deal with all of the changes to version
  in subpackages. Kludgy, but there's RPM for you.

* Tue Mar 13 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.3
- oh! The "etc-path" is important after all. Map that into
  /usr/lib[arch]/festival via a kludge.
- make cmu_us_slt_arctic_hts the default voice, in preparation for
  splitting the voice packages. (thankfully, there's already a fallback
  mechanism -- cool!)

* Mon Mar 12 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.2
- clean up accidental backup file left in updated awb_arctic_hts 
  tarball
- remove /usr/share/festival/etc (see bug #228315)
- move unpackage voices to the prep section where it belongs
- other minor spec file readability changes
- "make install" for this package is, um, "interesting". It seems
  geared for local user-level builds. So, rather than doing that and
  then patching it up, do the right parts by hand as necessary. (The
  previous version of the spec file did a convoluted mix of both.)
- don't install static libs.
- took out the massive hack that munges EST_*.h to speech_tools/EST_*.h in
  the installed header files -- programs should instead use
  -I/usr/include/speech_tools, shouldn't they? Put this back if I'm wrong.
- TODO -- autogenerated speech_tools docs
- festvox_ellpc11k.tar.gz, the spanish voice, wasn't getting installed anyway
  due to a license question. Since it's also gone upstream, removing.

* Fri Mar 09 2007 Matthew Miller <mattdm@mattdm.org> 1.96-0.1
- Preliminary update to 1.96
- Update to new cmu_us_*_arctic files -- they're changed upstream,
  although they don't appear to be versioned. Awesome. The current
  versions are those found in the same directory with the 1.96 files.
- ditto festlex_CMU.tar.gz
- add macro for speechtoolsversion
- minor update to festival-1.96-american.patch.
- update shared build patch and rename to make more obvious that
  it applies to the speechtools portion of the package.
- gcc 4 build patches now upstream.
- localhost-connections patch now upstream.
- note that festvox_ellpc11k.tar.gz and festvox_kallpc8k.tar.gz are no longer 
  in the directory tree upstream; drop?

* Fri Jan 19 2007 Miroslav Lichvar <mlichvar@redhat.com> - 1.95-6
- link with ncurses
- add dist tag
- make scriptlets safer

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.95-5.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.95-5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.95-5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Sun Jan 22 2006 Ray Strode <rstrode@redhat.com> - 1.95-5
- get gnopernicus working again. Patch from 
  Fernando Herrera <fherrera@gmail.com> (bug 178312)
- add a lot of compiler flags and random cruft to get
  festival to build with gcc 4.1

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Oct 10 2005 Florian La Roche <laroche@redhat.com>
- another try to get it to compile again

* Tue Apr 28 2005  <johnp@redhat.com> - 1.95-3
- require info packages so the post does not fail
- remove /usr/bin/VCLocalRule from buildroot since it is
  an extranious file that does not need to be installed

* Wed Apr 27 2005 Miloslav Trmac <mitr@redhat.com> - 1.95-2
- Fix build with gcc 4 (#156132)
- Require /sbin/install-info for scriptlets (#155698)
- Don't ship %%{_bindir}/VCLocalRules (#75645)

* Fri Feb 25 2005  <jrb@redhat.com> - 1.95-1
- patch from Matthew Miller to update to 1.95.  Full changelog below

* Mon Feb  7 2005 Matthew Miller <mattdm@mattdm.org> 1.95-0.mattdm8
- put speech-tools binaries in /usr/libexec/speech-tools so as to not
  clutter /usr/bin. Another approach would be to make speech-tools a 
  separate package and to make these utilities a subpackage of that.
- macro-ize /usr/bin, /usr/lib, /usr/include

* Sun Feb  6 2005 Matthew Miller <mattdm@mattdm.org> 1.95-0.mattdm6
- worked on this some more
- made actually work -- put back rest of fsstnd patch which I had broken
- made kludge for lack of sonames in shared libraries -- I think I did the
  right thing
- put back american as the default -- british dicts are non-free.

* Wed Jan  5 2005 Matthew Miller <mattdm@mattdm.org> 1.95-0.mattdm1
- preliminary update to 1.95 beta
- add really nice CMU_ARCTIC HTS voices, which is the whole point of wanting
  to do this. (They have a free license.)
- switch to festvox.org north american upstream urls
- keep old doc files -- there's no new ones yet.
- add comment to specfile about reason for lack of OALD (British) voices --
  they've got a more restrictive license.
- change license to "X11-style", because that's how they describe it.
- remove exclusivearch. I dunno if this builds on other archs, but I
  also don't know why it wouldn't.
- fancier buildroot string, 'cause hey, why not.
- more "datadir" macros
- remove most of Patch0 (fsstnd) -- can be done by setting variables instead.
  there's some bits in speechtools still, though
- update Patch3 (shared-build)
- don't apply patches 20 and 21 -- no longer needed.
- disable adding "FreeBSD" and "OpenBSD" to the dictionary for now. Probably
  a whole list of geek words should be added. Also, the patch was applied
  in an icky kludgy way.

* Thu Jul 29 2004 Miloslav Trmac <mitr@redhat.com> - 1.4.2-25
- Update for gcc 3.4

* Wed Jul 28 2004 Miloslav Trmac <mitr@redhat.com> - 1.4.2-24
- Use shared libraries to reduce package size
- Don't ship patch backup files

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue May  4 2004 Jonathan Blandford <jrb@redhat.com> 1.4.2-21
- Remove the spanish voices until we get clarification on the license

* Sat Apr 10 2004 Warren Togami <wtogami@redhat.com>
- BR libtermcap-devel #104722

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Aug 25 2003 Bill Nottingham <notting@redhat.com> 1.4.2-19
- clean up buildroot references (#75643, #77908, #102985)
- remove some extraneous scripts
- fix build with gcc-3.3

* Thu Jun 12 2003 Elliot Lee <sopwith@redhat.com> 1.4.2-17
- Rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Jan  9 2003 Tim Powers <timp@redhat.com> 1.4.2-15
- redirect install-info spewage

* Tue Jan  7 2003 Jens Petersen <petersen@redhat.com> 1.4.2-14
- put info files in infodir
- add post and postun script to install and uninstall info dir file entry
- drop postscript and info files from docs

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 1.4.2-13
- rebuild

* Thu Aug 15 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.4.2-12
- Adapt to current libstdc++

* Tue Jul 23 2002 Tim Powers <timp@redhat.com> 1.4.2-10
- build using gcc-3.2-0.1

* Wed Jul  3 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.4.2-9
- Add some missing helpprograms (# 67698)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jun 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.4.2-7
- Fix some rpmlint errors

* Mon Jun 10 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.4.2-6
- Fix ISO C++ compliance

* Mon Mar 18 2002 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Mar 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.4.2-2
- Get rid of CVS directiories in doc dir
- Fix broken symlinks for components from speech_tools

* Wed Mar  6 2002 Trond Eivind Glomsrød <teg@redhat.com>
- 1.4.2
- Lots of fixes to make it build, more needed
- Cleanups
- Update URL
- Fix docs inclusion
- Drop prefix
- Use %%{_tmppath}

* Wed Aug  2 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Add defattr (Bug #15033)

* Tue Jul 25 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix build on current 7.0

* Mon Jul 17 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- fix build on current 7.0

* Thu Jul  6 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- FHSify

* Mon Jun 19 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build on non-x86

* Sun Apr 22 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- initial packaging

## END: Generated by rpmautospec
