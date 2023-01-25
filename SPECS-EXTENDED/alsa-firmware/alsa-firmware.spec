# This is a firmware package, so binaries (which are not run on the host)
# in the end package are expected.
%define _binaries_in_noarch_packages_terminate_build   0
Summary:        Firmware for several ALSA-supported sound cards
Name:           alsa-firmware
Version:        1.2.4
Release:        8%{?dist}
# See later in the spec for a breakdown of licensing
License:        GPL+ AND BSD AND GPLv2+ AND GPLv2 AND LGPLv2+
Vendor:         Microsoft Corporation
Distribution:   Mariner
URL:            https://www.alsa-project.org/
Source:         ftp://ftp.alsa-project.org/pub/firmware/%{name}-%{version}.tar.bz2
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  make
#Requires:       alsa-tools-firmware >= 1.1.7
Requires:       systemd
# noarch, since the package is firmware
BuildArch:      noarch

%description
This package contains the firmware binaries for a number of sound cards.
Some (but not all of these) require firmware loaders which are included in
the alsa-tools-firmware package.

%prep
%autosetup -p1

%build
# Leaving this directory in place ends up with the following crazy, broken
# symlinks in the output RPM, with no sign of the actual firmware (*.bin) files
# themselves:
#
# /lib/firmware/turtlebeach:
# msndinit.bin -> /etc/sound/msndinit.bin
# msndperm.bin -> /etc/sound/msndperm.bin
# pndsperm.bin -> /etc/sound/pndsperm.bin
# pndspini.bin -> /etc/sound/pndspini.bin
#
# Probably an upstream package bug.
sed -i s#'multisound/Makefile \\'## configure.ac
sed -i s#multisound## Makefile.am
# Mixartloader elf has architecture powerpc, which is not supported in mariner.
sed -i s#'mixartloader/Makefile \\'## configure.ac
sed -i s#mixartloader## Makefile.am

autoreconf -vif
%configure --disable-loader
%make_build

# Rename README files from firmware subdirs that have them
for i in hdsploader mixartloader pcxhrloader usx2yloader vxloader ca0132
do
  mv ${i}/README README.${i}
done
mv aica/license.txt LICENSE.aica_firmware
mv aica/Dreamcast_sound.txt aica_dreamcast_sound.txt
mv ca0132/creative.txt LICENSE.creative_txt

%install
make install DESTDIR=%{buildroot}

%files
%license LICENSE* COPYING
%doc README*
%doc aica_dreamcast_sound.txt

# License: KOS (3-clause BSD)
/lib/firmware/aica_firmware.bin

# License: No explicit license; default package license is GPLv2+
/lib/firmware/asihpi

# License: GPL (undefined version)
/lib/firmware/digiface_firmware*

%dir /lib/firmware/ea
# The licenses for the Echo Audio firmware vary slightly so each is enumerated
# separately, to be really sure.
# LGPLv2.1+
/lib/firmware/ea/3g_asic.fw
# GPL (undefined version)
/lib/firmware/ea/darla20_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/darla24_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/echo3g_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_asic.fw
# GPL (undefined version)
/lib/firmware/ea/gina24_361_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dj_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_djx_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_io_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/indigo_iox_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla20_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_1_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2A_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_2S_asic.fw
# GPL (undefined version)
/lib/firmware/ea/layla24_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/loader_dsp.fw
# LGPLv2.1+
/lib/firmware/ea/mia_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_2_asic.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_301_dsp.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_48.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_1_asic_96.fw
# GPL (undefined version)
/lib/firmware/ea/mona_361_dsp.fw

%dir /lib/firmware/emu
# Licenses vary so are enumerated separately
# GPLv2
/lib/firmware/emu/audio_dock.fw
# GPLv2
/lib/firmware/emu/emu0404.fw
# GPLv2
/lib/firmware/emu/emu1010_notebook.fw
# GPLv2
/lib/firmware/emu/emu1010b.fw
# GPLv2
/lib/firmware/emu/hana.fw
# GPLv2+
/lib/firmware/emu/micro_dock.fw

# License: GPL (undefined version)
/lib/firmware/ess

# License: No explicit license; default package license is GPLv2+
/lib/firmware/korg

# License: GPL (undefined version)
/lib/firmware/multiface_firmware*

# License: GPL (undefined version)
/lib/firmware/pcxhr

# License: GPL (undefined version)
/lib/firmware/rpm_firmware.bin

# License: GPLv2+
/lib/firmware/sb16

# License: GPL (undefined version)
/lib/firmware/vx

# License: No explicit license; default package license is GPLv2+
# See ALSA bug #3412
/lib/firmware/yamaha

# Licence: Redistribution allowed, see ca0132/creative.txt
/lib/firmware/ctefx.bin
/lib/firmware/ctspeq.bin
/lib/firmware/ctefx-desktop.bin
/lib/firmware/ctefx-r3di.bin

# Licence: No explicit license; says it's copied from kernel where the cs46xx
# driver is labelled as GPLv2+
/lib/firmware/cs46xx

# Even with --disable-loader, we still get usxxx firmware here; looking at the
# alsa-tools-firmware package, it seems like these devices probably use an old-
# style hotplug loading method
# License: GPL (undefined version)
%{_datadir}/alsa/firmware

%changelog
* Fri Dec 16 2022 Sumedh Sharma <sumsharma@microsoft.com> - 1.2.4-8
- Initial CBL-Mariner import from Fedora 37 (license: MIT)
- Remove mixartloader elf files (architecture mistmatch: powerpc)
- License verified

* Wed Jul 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Wed Jan 19 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Tue Oct 20 2020 Jaroslav Kysela <perex@perex.cz> - 1.2.4-3
- Updated to 1.2.4

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Mar  3 2020 Jaroslav Kysela <perex@perex.cz> - 1.2.1-7
- Removed Intel SOF firmware files (moved to alsa-sof-firmware package)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Tue Jan 21 2020 Jaroslav Kysela <perex@perex.cz> - 1.2.1-5
- Updated Intel SOF firmware files to 1.4.2

* Mon Jan  6 2020 Jaroslav Kysela <perex@perex.cz> - 1.2.1-4
- Intel SOF firmware files to 1.4.1 fixes (symlinks)

* Thu Dec  5 2019 Jaroslav Kysela <perex@perex.cz> - 1.2.1-3
- Updated Intel SOF firmware files to 1.4.1

* Wed Nov 13 2019 Jaroslav Kysela <perex@perex.cz> - 1.2.1-2
- Updated to 1.2.1
- Added Intel SOF firmware files

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Feb 26 2015 Jaroslav Kysela <perex@perex.cz> - 1.0.29-1
- Updated to 1.0.29

* Thu Jul 24 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.28-1
- Update to 1.0.28

* Tue Jun 17 2014 Peter Robinson <pbrobinson@fedoraproject.org> 1.0.27-5
- Fix FTBFS once more with feeling
- Update spec

* Sun Jun 15 2014 Tim Jackson <rpm@timj.co.uk> - 1.0.27-4
- Fix FTBFS (rhbz#1105946)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.27-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.27-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Apr 12 2013 Jaroslav Kysela <perex@perex.cz> - 1.0.27-1
- Update to 1.0.27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb  1 2012 Jaroslav Kysela <perex@perex.cz> - 1.0.25-1
- Update to 1.0.25

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.24.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 03 2011 Tim Jackson <rpm@timj.co.uk> - 1.0.24.1-1
- Update to 1.0.24.1

* Mon May  3 2010 Tom "spot" Callaway <tcallawa@redhat.com> - 1.0.23-1
- update to 1.0.23

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.20-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun May 10 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.20-1
- Update to 1.0.20

* Sat Feb 28 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-4
- Fix build on recent RPM versions

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.19-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Feb 14 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-2
- Fix unowned directories problem (#483321)

* Tue Jan 20 2009 Tim Jackson <rpm@timj.co.uk> - 1.0.19-1
- Update to 1.0.19

* Mon Jul 21 2008 Jaroslav Kysela <jkysela@redhat.com> - 1.0.17-1
- Updated to 1.0.17

* Mon May 12 2008 Tim Jackson <rpm@timj.co.uk> - 1.0.16-1
- Update to upstream 1.0.16
- Clarify licensing conditions

* Tue Aug 14 2007 Tim Jackson <rpm@timj.co.uk> - 1.0.14-1
- Update to upstream 1.0.14, but skip turtlebeach firmware as it doesn't seem 
  to install properly
- Remove files from old-style firmware loader locations
- Spec file cosmetics, keep rpmlint quiet

* Sat Nov 25 2006 Tim Jackson <rpm@timj.co.uk> - 1.0.12-1
- Update to 1.0.12
- Add udev dep

* Fri Apr 08 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Sat Apr 03 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.4-0.fdr.1
- Update to 1.0.4

* Fri Jan 16 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.1-0.fdr.2
- add missing rm in install section

* Fri Jan 09 2004 Thorsten Leemhuis <fedora[AT]leemhuis.info> - 1.0.1-0.fdr.1
- Update to 1.0.1
- Contains now the license -- is "Distributable under GPL"

* Thu Dec 04 2003 Thorsten Leemhuis <fedora[AT]leemhuis.info> 1.0.0-0.fdr.0.1.rc1
- Initial build.
