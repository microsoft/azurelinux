# This spec file has been modified by azldev to include build configuration overlays.
# Do not edit manually; changes may be overwritten.

Name:           gt
Version:        0.4
Release: 49%{?dist}
Summary:        Modified Timidity which supportes enhanced gus format patches
# Automatically converted from old format: GPLv2+ - review is highly recommended.
License:        GPL-2.0-or-later
URL:            http://alsa.opensrc.org/GusSoundfont
# This is ftp://ling.lll.hawaii.edu/pub/greg/gt-0.4.tar.gz
# with the examples/patch and sfz directories removed as the license of the
# samples in these dirs is unclear. Also the src/ac3* files have been removed
# as these contain patented code.
Source0:        %{name}-%{version}-clean.tar.gz
Patch0:         gt-0.4-noac3.patch
Patch1:         gt-0.4-compile-fix.patch
Patch2:         gt-0.4-optflags.patch
Patch3:         gt-0.4-config-default-velocity-layer.patch
Patch4:         gt-0.4-ppc-compile-fix.patch
Patch5:         gt-0.4-unsf-bigendian-fix.patch
Patch6:         gt-0.4-unsf-tremolo.patch
Patch7:         gt-0.4-gcc10.patch
BuildRequires:  gcc
BuildRequires:  alsa-lib-devel libvorbis-devel flex
BuildRequires:  make
Requires:       timidity++-patches

%description
Modified timidity midi player which supportes enhanced gus format patches and
surround audio output.


%package -n soundfont-utils
Summary:        Utilities for converting from / to various soundfont formats

%description -n soundfont-utils
Utilities for converting from / to various soundfont formats and a midi file
disassembler.


%prep
%autosetup -p1
cp -p src/README README.timidity
# ugly hack to change DEFAULT_PATH as CONFIG_FILE setting is completely ignored
sed -i -e "s#\$(TIMID_DIR)#%{_sysconfdir}#" src/Makefile.in


%build
export CFLAGS="$CFLAGS -std=gnu89"
%global build_type_safety_c 0
%configure
make


%install
%make_install
# rename somewhat genericly named dim to midi-disasm
mv $RPM_BUILD_ROOT%{_bindir}/dim $RPM_BUILD_ROOT%{_bindir}/midi-disasm
mv $RPM_BUILD_ROOT%{_mandir}/man1/dim.1 \
   $RPM_BUILD_ROOT%{_mandir}/man1/midi-disasm.1
sed -i 's/dim/midi-disasm/g' $RPM_BUILD_ROOT%{_mandir}/man1/midi-disasm.1
touch -r utils/midifile.c $RPM_BUILD_ROOT%{_mandir}/man1/midi-disasm.1
 

%files
%doc AUTHORS COPYING ChangeLog FEATURES NEWS README*
%{_bindir}/gt
%{_mandir}/man1/gt.1*

%files -n soundfont-utils
%doc COPYING utils/README* utils/GUSSF2-SPEC
%{_bindir}/*
%exclude %{_bindir}/gt
%{_mandir}/man1/*
%exclude %{_mandir}/man1/gt.1*


%changelog
* Thu Jul 24 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_43_Mass_Rebuild

* Fri Jan 17 2025 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Jul 26 2024 Miroslav Suchý <msuchy@redhat.com> - 0.4-46
- convert license to SPDX

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-45
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Jan 20 2024 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-43
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Dec 07 2023 Karel Volný <kvolny@redhat.com> - 0.4-42
- Change path to read config provided by fluid-soundfont-lite-patches (#2253073)

* Wed Aug 16 2023 Florian Weimer <fweimer@redhat.com> - 0.4-41
- Set build_type_safety_c to 0 (#2160035)

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-39
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Wed Jan 11 2023 Florian Weimer <fweimer@redhat.com> - 0.4-38
- Build in C89 mode (#2160035)

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-33
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Fri Mar  6 2020 Hans de Goede <hdegoede@redhat.com> - 0.4-32
- Fix FTBFS (rhbz#1799498)

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jun 16 2017 Hans de Goede <hdegoede@redhat.com> - 0.4-24
- Drop smpflags from make to avoid FTBFS (rhbz#1460276)
- Minor spec-file cleanups

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.4-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Hans de Goede <hdegoede@redhat.com> - 0.4-20
- Fix 404 URL tag (rhbz#1195948)

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 27 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-13
- Rebuilt for glibc bug#747377

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Nov 16 2010 Hans de Goede <hdegoede@redhat.com> - 0.4-11
- Add COPYRIGHT file to soundfont-utils

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-9
- Add missing BR flex, fixing FTBFS (#511363)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  3 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-7
- Fix an error in unsf's tremolo settings export

* Sat Feb  2 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-6
- Fix hopefully the last endian issue in unsf

* Fri Feb  1 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-5
- And fix unsf for char being unsigned on ppc <sigh>

* Fri Feb  1 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-4
- Fix unsf running on big endian systems

* Wed Jan 30 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-3
- Correct license field from GPLv2 to GPLv2+

* Wed Jan 30 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-2
- Fix compilation on big endian archs

* Sun Jan 27 2008 Hans de Goede <j.w.r.degoede@hhs.nl> 0.4-1
- Initial Fedora Package
