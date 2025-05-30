Summary:        Simple program for reading/writing flash chips content
Name:           flashrom
Version:        1.4.0
Release:        2%{?dist}
License:        GPL-2.0-only
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://flashrom.org
Source0:        https://download.flashrom.org/releases/%{name}-%{version}.tar.xz
Source1:        https://download.flashrom.org/releases/%{name}-%{version}.tar.xz.asc
# Find which key was used for signing the release:
#
# $ LANG=C gpg --verify flashrom-v1.3.0.tar.bz2.asc flashrom-v1.3.0.tar.bz2
# gpg: Signature made Wed Feb  8 03:57:51 2023 CET
# gpg:                using DSA key 6E6EF9A0BA478006E2776E4CC037BB413134D111
# gpg: Can't check signature: No public key
#
# Now export the key required as follows:
#
# gpg --no-default-keyring --keyring ./keyring.gpg --keyserver keyserver.ubuntu.com --recv-key 6E6EF9A0BA478006E2776E4CC037BB413134D111
# gpg --no-default-keyring --keyring ./keyring.gpg  --output 6E6EF9A0BA478006E2776E4CC037BB413134D111.gpg --export
Source2:        6E6EF9A0BA478006E2776E4CC037BB413134D111.gpg
BuildRequires:  gcc
BuildRequires:  gnupg2
BuildRequires:  libftdi-devel
BuildRequires:  libjaylink-devel
BuildRequires:  libusb1-devel
BuildRequires:  meson
BuildRequires:  pciutils-devel
BuildRequires:  python3-sphinx
BuildRequires:  systemd
BuildRequires:  zlib-devel
Requires:       udev
# see rhbz #495226
ExcludeArch:    s390 s390x
%ifarch %{ix86} x86_64 aarch64
BuildRequires:  dmidecode
Requires:       dmidecode
%endif

%description
flashrom is a utility for identifying, reading, writing, verifying and erasing
flash chips. It is designed to flash BIOS/EFI/coreboot/firmware/optionROM
images on mainboards, network/graphics/storage controller cards, and various
other programmer devices.

%package devel
Summary:        Development package for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
Files for development with %{name}.

%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup -p1 -n %{name}-%{version}
# Replace GROUP="plugdev" specifiers with TAG+="uaccess"
sed -e 's/MODE="[0-9]*", GROUP="plugdev"/TAG+="uaccess"/g' util/flashrom_udev.rules -i

%build
%meson -Dtests=disabled -Ddocumentation=disabled
%meson_build

%install
%meson_install

install -D -p -m 0644 util/flashrom_udev.rules %{buildroot}/%{_udevrulesdir}/60_flashrom.rules
rm %{buildroot}/%{_libdir}/libflashrom.a

%files
%license COPYING
%doc README.rst doc/
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.*
%{_udevrulesdir}/60_flashrom.rules
%{_datadir}/bash-completion/completions/%{name}.bash
%{_libdir}/libflashrom.so.1
%{_libdir}/libflashrom.so.1.0.0

%files devel
%{_includedir}/libflashrom.h
%{_libdir}/libflashrom.so
%{_libdir}/pkgconfig/flashrom.pc

%changelog
* Fri Oct 18 2024 Jocelyn Berrendonner <jocelynb@microsoft.com> - 1.4.0-2
- Integrating the spec into Azure Linux
- Initial CBL-Mariner import from Fedora 42 (license: MIT).
- License verified.

* Fri Jul 26 2024 Peter Lemenkov <lemenkov@gmail.com> - 1.4.0-1
- Update to latest upstream release

* Wed Jul 17 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Wed Jan 24 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Jan 19 2024 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sat Oct 21 2023 Peter Lemenkov <lemenkov@gmail.com> - 1.3.0-4
- Check GPG signature

* Wed Jul 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Sun Jun 18 2023 Yaakov Selkowitz <yselkowi@redhat.com> - 1.3.0-2
- Drop unused libusb-0.1 dependency

* Thu Feb 09 2023 Richard Hughes <richard@hughsie.com> - 1.3.0-1
- Update to latest upstream release

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Jul 21 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Sat Dec 26 2020 Peter Lemenkov <lemenkov@gmail.com> - 1.2-5
- Added jlink support

* Tue Dec 22 2020 Robert Scheck <robert@fedoraproject.org> - 1.2-4
- Perform source file verification during %%prep

* Mon Jul 27 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Mon Feb 17 2020 Richard Hughes <richard@hughsie.com> - 1.2-2
- Build the package using meson to get the libflashrom shared library support
  required by fwupd.

* Tue Feb 11 2020 mrnuke <mr.nuke.me@gmail.com> - 1.2-1
- Update to flashrom 1.2 (Release was intended to fix #1799344)

* Tue Feb 11 2020 Robert Scheck <robert@fedoraproject.org> - 1.1-4
- Added upstream patch to declare usb_ctx as static (#1799344)

* Tue Jan 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Jun 28 2019 Peter Robinson <pbrobinson@fedoraproject.org> 1.1-1
- Update to flashrom 1.1

* Mon May 27 2019 David Hendricks <david.hendricks@gmail.com> - 1.1-0.1
- Update to flashrom 1.1-rc1
- Drop flashrom-1.0-AT25DF021A.patch since it's been merged

* Sun Apr 28 2019 Robert Scheck <robert@fedoraproject.org> - 1.0.1-1
- Corrected package version from v1.0.1 to 1.0.1

* Fri Apr 26 2019 David Hendricks <david.hendricks@gmail.com> - v1.0.1-1
- Update to flashrom 1.0.1

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Aug 28 2018 mrnuke <mr.nuke.me@gmail.com> - 1.0-6
- Fix udev rule sed-ing
- Drop the 'z' prefix of the udev rules

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 26 2018 Dan Horák <dan[at]danny.cz> - 1.0-4
- Add support for the Atmel device on the Talos II Power9 mainboard

* Fri Feb 09 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0-3
- Escape macros in %%changelog

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 2 2018 David Hendricks <david.hendricks@gmail.com> - 1.0-1
- Update to flashrom 1.0

* Fri Oct 20 2017 David Hendricks <david.hendricks@gmail.com> - 0.9.9.1-1
- Update to flashrom 0.9.9.1

* Wed Oct 04 2017 mrnuke <mr.nuke.me@gmail.com> - 0.9.9-6
- Drop uaccess.patch in favor of sed script

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 12 2017 Peter Robinson <pbrobinson@fedoraproject.org> 0.9.9-3
- Tweak arch build rules, minor spec cleanups
- Use %%license
- Build on aarch64

* Wed Mar  8 2017 Peter Lemenkov <lemenkov@gmail.com> - 0.9.9-2
- Proper udev rules

* Sun Feb 26 2017 Alexandru Gagniuc <mr.nuke.me@gmail.com> - 0.9.9-1
- Update to flashrom 0.9.9
- Drop the autotools patches (they were rejected upstream)
- Update description to match flashrom.org main page
- Use {optflags} macro to set CFLAGS

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-5.svn1850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.9.7-4.svn1850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.7-3.svn1850
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jan 13 2015 Peter Jones <pjones@redhat.com> - 0.9.7-2.svn1850
- Enable support for DediProg SF100, since it's very common.

* Thu Sep 11 2014 Peter Lemenkov <lemenkov@gmail.com> - 0.9.7-1.svn1850
- Add support for Winbond W25Q40.V chips
- Add support for Macronix MX23L1654, MX23L6454 and MX23L12854 mask ROMs
- Add support for Intel Wildcat Point PCH
- Add support for Intel Silvermont: Bay Trail, Rangeley and Avoton
- Add support for S25FL128P, S25FL129P chips
- Add support for a bunch of 29GL parallel flash chips
- Add support for Atmel AT49LH004 and AT49LH00B4
- Add new programmer for SPI EEPROMs attached to Intel 82580 NICs
- Add support for AMD Bolton chipset
- Add Board Enable for ASUS Vintage 2 PH1 (P5LD2-MQ)
- Add support for Macronix MX29F022(N)B and MX29F022(N)T
- Add support for Macronix MX25U12835F
- Add support for Sanyo LE25FW106
- Add IT8212F PCI ATA controller as programmer
- Add support for Atmel (now Adesto) AT25DL081 and AT25DL161
- Add VIA VT6421A LPC programmer driver
- Add support for ESMT F25L32PA
- Add support for Sanyo LE25FW406A
- Add support for new AMD SPI controller (SPI 100)
- Add support for Sanyo LE25FU406B
- Add support for SST25LF020A
- Add support for Spansion S25FL132K and S25FL164K
- Add support for SST25WF08
- Add support for Macronix MX23L3254 mask ROM
- Add support for TUMPA Lite
- Add support for Intel 82574L
- Add board enable for ASUS A7V8X-MX
- Add board enable for ASUS P5LD2-VM DH
- Add board enable for abit BF6
- Add support for SST25VF512A, ST25VF020, SST25VF020B chips
- Add pinout for Wiggler LPT
- Add pinout for Atmel STK200/300
- Add pinout for Altera ByteBlasterMV
- Add support for ST M50LPW080 chip
- Add an internal DMI decoder
- Add board enable for Bcom WinNET P680
- Add support for AT45CS1282 chip
- Add support for AT45DB321C
- Add support for Atmel AT45DB* chips
- Add support for Fujitsu MBM29LV160BE/TE
- Add ability to select between chips on GIGABYTE DualBIOS boards
- Temporarily disable ftdi support

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.1-7.svn1705
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.1-6.svn1705
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Jul 30 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.9.6.1-5.svn1705
- Handle active IMCs in AMD chipsets
- Rename Numonyx and ST (SGS/Thomson) chips to Micron
- Various cross-platform fixes
- Add support for remaining Numonyx (Micron) N25Q chips
- Add support for Spansion S25FL...S chips
- Add support for Spansion S25FL2 chips
- Add support for Micron/Numonyx/ST M25PX80
- Add support for AMIC A25LQ16 and A25LQ64
- Add support for more Eon EN25QH chips
- Add support for Eon EN25S series
- Add support for Numonyx M45PE series
- Add support for some GigaDevice GD25* chips
- Add support for all Sanyo LE25FW chips
- Add support for Nantronics N25 series
- Fix unlocking function for most Atmel AT2[56]D* chips
- Add W25Q...W series
- dediprog: fix SPI clock setting

* Tue May 21 2013 Peter Lemenkov <lemenkov@gmail.com> - 0.9.6.1-4.svn1673
- dediprog: add support for chip select
- Add support for PMC Pm25LD series flash chips
- Add Altera USB-Blaster SPI programmer
- Add support for Intel Lynx Point low-power and Wellsburg chipsets
- Add support for Macronix MX25U1635E, MX25U3235E/F and MX25U6435E/F chips
- Add (untested) board enable for ASUS P4PE-X/TE

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.6.1-3.svn1639
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Dec 30 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.9.6.1-2.svn1639
- Updated to the latest svn ver. 1639 (post-release snapshot for 0.9.6.1)
- Support for Atmel's AT25F series of SPI flash chips
- Support for Intel S33 series flash chips
- Add a "device" parameter for Dediprog
- (Untested) board enable for Asus DSAN-DX
- Support for Winbond W39F010/W39L010/W39L020
- Support for Atmel AT26DF041
- Support for Numonyx N25Q016 and N25Q032
- Support for SST's 25WF series of SPI flash chips
- Support for GigaDevice GD25LQ32
- Board enable for MSI K8N Neo Platinum

* Sat Sep 08 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.9.6.1-1.svn1596
- Updated to the latest svn ver. 1596 (post-release snapshot for 0.9.6.1)
- (Untested) board enable for ASUS P5LD2-VM m/b
- Support for Eon EN25F64 flashchip
- Support for AJAWe added to pony_spi
- Support for Realtek RTL8169 NIC
- (Untested) board enable for DFI AD77 m/b
- Support for Via VX800/VX820, VX855/VX875, and VX900 chipsets
- Support for Atmel AT49(H)F010, AT49F080 and AT49F080T flashchips
- Support (board enable) for Biostar M7VIQ m/b

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.5.2-5.svn1547
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.9.5.2-4.svn1547
- Enable support for USB programmers (FT2232, FT4232, etc), see rhbz #839179.
- Add board enable for MSI K9N SLI (MS-7250 VER:2.1)
- Add support for PMC Pm39LV512 flashchip
- Add support for Eon EN25QH32 flashchip
- Add Winbond W836xx SuperI/O detection
- Add ITE IT8707F/IT8710F SiperI/O detection

* Mon Jul  2 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 0.9.5.2-3.svn1530
- Enable building on ARM

* Sun May 06 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.9.5.2-2.svn1530
- Updated to latest svn ver. 1530 (post-release snapshot for 0.9.5.2)
- Support for w83697 family SuperIO chips
- Add board enable for ASUS P5BV-R
- PonyProg2000 SPI hardware support
- Add UNTESTED support for future Intel chipsets (DH89xxCC and Lynx Point)
- Add support for for the Atmel AT49F040 chip
- Add support for the Eon EN29LV640B chip
- Add GigaDevice GD25QXX series support
- Add support for the Numonyx N25Q064 chip
- Disable Linux SPI on EPEL 5 (see rhbz #808775)

* Sat Mar 31 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.9.5.2-1.svn1517
- Updated to latest svn ver. 1517 (post-release snapshot for 0.9.5.2)
- Add (untested) board enable for ASUS TUSL2-C
- Add board enable for ASUS OPLX-M.
- Add support for SFDP (JESD216)
- Support compilation for the ARM architecture (not enabled in the spec-file)
- Board enable for TriGem Anaheim-3
- Add support for RDC R6030 chipset

* Thu Feb 02 2012 Peter Lemenkov <lemenkov@gmail.com> - 0.9.4-4.svn1487
- Updated to latest svn ver. 1487 (post-release snapshot for 0.9.4)
- Add board enable for the MSC Q7 Tunnel Creek board
- Add board enable for AOpen i945GMx-VFX (used in FCS ESPRIMO Q5010)
- Mark ABIT NF-M2S, ASUS P5K-VM, ASUS M5A99X EVO, ASUS Z8PE-D12, PC Engines Alix.2d3
  boards as tested
- Mark Pm29F002T, AMIC A49LF040A, Winbond W39V040FC flashchips as tested
- Add board enable for ASUS A7N8X-VM/400
- Add board enable for ASRock ConRoeXFire-eSATA2
- Add board enable for ASUS P4GV-LA (Guppy)
- Add board enables for the ASUS P5N-D and P5N-E SLI
- Add board enable for Sun Ultra 40 M2

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.4-3.svn1455
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 21 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.9.4-2.svn1455
- Updated to latest svn ver. 1455 (post-release snapshot for 0.9.4)
- Added lots of new boards and several chipsets and flashchips
- Lots of other cleanups and enhancements

* Fri Aug 12 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.9.4-1.svn1412
- Updated to latest svn ver. 1412 (post-release snapshot for 0.9.4)
- Experimental support for Apple PowerPC Macs reflashing
- Added support for the Dangerous Prototypes Bus Blaster
- Board enable for ASUS P5GD2 Premium
- (Untested) board enable for Asus P5LD2
- Board enable for ASUS A8M2N-LA (HP OEM "NodusM3-GL8E")
- Add J-7BXAN to the list of supported boards
- Add ASUS P4S533-X to the list of supported boards
- Add ASUS M4A785TD-V EVO to the list of supported board
- Add GA-945PL-S3P (rev. 6.6) to the list of supported boards
- Add MS-7142 (K8MM-V) to the list of supported boards
- Add MS-7369 (K9N Neo V2) to the list of supported boards
- Add X7DBT-INF to the list of supported boards
- Add support for the GIGABYTE GA-8SIMLH board
- Support for EN25Q(H) series SPI flash chips
- Add satamv programmer

* Tue Jul 12 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.9.3-5.svn1368
- Updated to latest svn ver. 1368 (post-release snapshot for 0.9.3)
- Added 32 (yes, thirty-two) new boards
- Lots of other cleanups and enhancements

* Sat May 14 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.9.3-4.svn1299
- Updated to latest svn ver. 1299 (post-release snapshot for 0.9.3)
- Intel NIC with parallel flash support (Intel 8255xER/82551IT Fast Ethernet
  Controller and Intel 82557/8/9/0/1 Ethernet Pro 100)
- Fixed multiple detection of the same chip
- Added support for the Via VX855 chipset
- Added support for more than one Super I/O or EC per machine
- Board enable for Foxconn 6150K8MD-8EKRSH
- List AMD SB850 as supported (it has the same PCI ID as SB700)
- Fixed build on PowerPC (see rhbz #683414)

* Wed Mar 09 2011 Peter Lemenkov <lemenkov@gmail.com> - 0.9.3-3.svn1280
- Updated to latest svn ver. 1280 (post-release snapshot for 0.9.3)
- Board enable for Asus P4P800-VM
- Support for ST M25PX16 chip
- Support for W39L040 chip
- Board enable for Gigabyte GA-K8N51GMF
- Support for ITE IT8500/IT8502 embedded controllers
- Support for AMD Am29LV001BB, Am29LV001BT, Am29LV002BB, Am29LV002BT,
  Am29LV004BB, Am29LV004BT, Am29LV008BB, Am29LV008BT chips
- Support for Angelbird Wings PCIe SSD (Marvell 88SX7042 SATA controller)
- Fix for rhbz #680715

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.3-2.svn1250
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Jan  4 2011 Peter Lemenkov <lemenkov@gmail.com> 0.9.3-1.svn1250
- Updated to latest svn ver. 1250 (post-release snapshot for 0.9.3)
- Initial rtl8169 support (UNTESTED)
- Fix decoding of SB600 LPC ROM protection registers
- Erasing/writing of Winbond W39V040FB chips
- Support for the Open Graphics Project development card
- Support for SST SST25VF010 chip
- Board-enable for the MSI MS-6391 (845 Pro4)
- Support for Spansion S25FL004A, S25FL032A, and S25FL064A chips
- Add chunked write ability to the Dediprog SF100 driver
- Support bulk read on Dediprog SF100
- Support for the OpenMoko Neo1973/Neo FreeRunner debug board (ver, 2 or 3)
- Real partial writes were implemented
- Add SPI flash emulation capability to the dummy programmer
- Board enable for the EPoX EP-8NPA7I board
- Fixed build on EL-5

* Tue Oct 26 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.3-0.1.svn1205
- Ver. 0.9.3 (pre-release, exported from SCM)

* Wed Sep 29 2010 jkeating - 0.9.2-7.svn1180
- Rebuilt for gcc bug 634757

* Fri Sep 24 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.2-6.svn1180
- Added autotools support

* Tue Sep 21 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.2-5.svn1180
- Patch no.3 merged upstream

* Fri Sep 17 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.2-4.svn1158
- Enable building on PowerPC (only external flashers enabled so far).
  See rhbz #283491.

* Sun Sep 12 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.2-3.svn1158
- Clean up spec-file
- Updated to latest svn ver. 1158
- Doubles the number of known boards!

* Sun Jun 13 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.2-2
- Added missing Requires - dmidecode (for accurate board matching)

* Thu Jun  3 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.2-1
- Support for new external flashers
- Dozens of added flash chips, chipsets, mainboards
- Selective blockwise erase
- Improved user interface
- Reliability fixes
- Mainboard matching via DMI strings
- Laptop detection which triggers safety measures

* Wed Apr 28 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.1-4.svn995
- Updated to latest svn ver. 995
- Lots of new chips and m/b

* Fri Mar 12 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.1-3.svn931
- Updated to latest svn ver. 931
- ASUS A7V8X-X board
- MS-7202 board
- Asus M2NBP-VM CSM board
- HP Vectra VL420SFF board
- Eon EN29F010 chip
- Abit IP35 Pro board
- HP Vectra VL400 board
- Intel E28F004S5 flash chip
- Lots of bugfixes

* Mon Feb  8 2010 Peter Lemenkov <lemenkov@gmail.com> 0.9.1-2.svn893
- Updated to latest svn ver. 893
- ST M29W512B chip
- Tekram P6Pro-A5 board
- Fixed GIGABYTE GA-7ZM board
- SST39SF512 chip
- Fixed SyncMOS S29C51004T chip
- Intel NM10 chipset
- Fixed A25L40PU and A2540PT chip
- Spansion S25FL008A chip
- MSI 651M-L board
- Several Eon EN25Bxx{T,B} chips
- Fixed Sharp LHF00L04 chip
- VIA VT8233A chipset
- MSI K8N Neo4-F board
- Intel Poulsbo chipset
- ECS K7S6A board
- ASRock M3A790GXH/128M board
- Asus M2V-MX board
- Shuttle AK31 board
- Fixed MSI KT4V board
- Asus P4B266LM board
- Asrock P4i65GV board
- Intel 3400 series / 5 series chipset
- W25x32 and W25x64 chips
- Sanyo LF25FW203A chip (sometimes labeled as 25FW203T)
- Shuttle FN25 (SN25P) board
- EPoX EP-8RDA3+ board
- ASUS P5ND2-SLI Deluxe board
- nVidia nForce 4 chipset
- VIA VT82C596 chipset
- Wyse Winterm S50 board
- Dell S1850 board
- Dr. Kaiser PC-Waechter PCI devices

* Fri Sep  4 2009 Peter Lemenkov <lemenkov@gmail.com> 0.9.1-1
- Ver. 0.9.1
- See release notes at http://www.coreboot.org/Flashrom/0.9.1
- Dropped the only patch (no longer needed)
- Changed project's URL

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue May  5 2009 Peter Lemenkov <lemenkov@gmail.com> 0.9.0-1
- Ver. 0.9.0

* Tue Apr 14 2009 Peter Lemenkov <lemenkov@gmail.com> 0-0.18.20090414svn4107
- Various manpage / README fixes
- Board enable support for HP DL145 G3
- high coreboot table support
- Since now we're using ExclusiveArch

* Wed Mar 11 2009 Peter Lemenkov <lemenkov@gmail.com> 0-0.17.20090311svn3984
- MSI MS-7046 board enable
- Intel Desktop Board D201GLY
- Add Am29F080B Am29LV081B SST39VF080 support (untested)
- Board enable for GIGABYTE GA-MA78G-DS3H

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0-0.16.20090112svn3852
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Jan  8 2009 Peter Lemenkov <lemenkov@gmail.com> 0-0.15.20090112svn3852
- Changed license to GPLv2
- SST49LF020 support
- AMD-768 chipset support
- i631x LPC support
- Support the MX29LV040C
- AMD SB700 flash enable
- Support for the AMD/ATI SB600 southbridge SPI
- SST25VF080B flash chip support
- Support for 32Mbit SPI flash SST25VF032B
- Support for bunch of Fujitsu and Macronix chips

* Mon Nov  3 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.14.20081103svn3723
- Dump ICH8/ICH9/ICH10 SPI registers
- Add additional SPI sector erase and chip erase command
- Add support for the ST M50FW002 chip
- Support for some Numonyx parts (M25PE)
- SPI boot flash support on EP80579
- Support for the Intel 82371MX (MPIIX) southbridge
- Support for the Intel 82371FB PIIX and 82371SB (PIIX3) southbridges
- Support for the VIA VT82C586A/B chipset
- ICH10 support to flashrom
- Support for AM29F002(N)B[BT]

* Mon Oct  6 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.13.20080928svn3602
- More ExcludeArch

* Sun Sep 28 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.12.20080928svn3602
- Proper support for EN29F002(A)(N)[BT]
- Recognize the Intel EP80579 LPC flash interface
- Add support for MSI KT4V
- Support for Winbond W39V040C and MSI K8T Neo2-F

* Sun Jul  6 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.11.20080607svn3418
- AMIC A29002
- flashing system with Nvidia MCP67
- PCI IDs for EPIA-CN
- VIA SPI controller on VT8237S
- ICH7 SPI support
- support for AMIC Technology A49LF040A
- Board enable and autodetection for GIGABYTE GA-7VT600
- Add support for Amic Technology A29040B flash chip
- Board enable and autodetection for BioStar P4M80-M4
- Add support for the ASUS P4B266 board
- Add support for Amic A25L40P SPI flash

* Fri Jun  6 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.10.20080517svn3332
- Exclude sparc64

* Sat May 17 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.9.20080517svn3332
- Fixed %%patch0

* Sat May 17 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.8.20080517svn3332
- Support Pm49FL004/2 Block Locking Registers
- Add support for the Atmel AT25DF321 SPI flash
- Lots of new SST flash chip IDs
- Add lots of ATMEL SPI flash chips
- Add SST39VF512, SST39VF010, SST39VF040 support
- Add ICH9 detection to flashrom
- Support for the Winbond W39V080FA series of chips
- Support for flashing on the Kontron 986LCD-M board
- Add board_enable for Artec Group DBE61 and DBE62

* Sat Feb  9 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.7.20080209svn3099
- Add board enable for VIA EPIA SP
- support for devices using AMD Geode companion chip CS5536 that have the
  Boot ROM on NOR flash that is directly connected to FLASH_CS3 (Boot
  Flash Chip Select)
- Add support for the PMC Pm25LV family of SPI flash chips
- Add ids and chip entry for Spansion S25FL016A
- Support for MX25L3205D chip
- Enable MX25L8005 support

* Wed Jan  9 2008 Peter Lemenkov <lemenkov@gmail.com> 0-0.6.20080109svn3036
- support for SST25VF040B flash chip
- enable ga_2761gxdk board
- support for EN29F002(A)(N)B chips
- support for EON EN29F002AT flash chip
- support for 25VF016B flash chip
- support for ST M25P05-A, M25P10-A, M25P20, M25P40, M25P16, M25P32,
  M25P64 and M25P128 flash chips
- support for ST M25P80 flash chip
- support for AT49F002, AT49F002N, AT49F002T and AT49F002NT flash chips
- enable Acorp 6A815EPD board

* Sun Nov 18 2007 Peter Lemenkov <lemenkov@gmail.com> 0-0.5.20071118svn2967
- svn ver. 2967 (support for Intel 440MX systems, Fujitsu MBM29F400TC,
  AMD Geode CS5536)

* Sun Oct 28 2007 Peter Lemenkov <lemenkov@gmail.com> 0-0.4.20071028svn2897
- typo fix

* Sun Oct 28 2007 Peter Lemenkov <lemenkov@gmail.com> 0-0.3.20071028svn2897
- svn ver. 2897 (support for Gigabyte M61P-S3 SPI m/b, Am29LV040B chip)
- flashrom executable now sits in sbindir since it's administrator's tool

* Wed Oct  3 2007 Peter Lemenkov <lemenkov@gmail.com> 0-0.2.20071003svn2817
- Added correct BZ# for ExludeArch issue
- Preserved timestamp then installing flashrom
- svn ver. 2817 (support for IT8716F added, added COPYING)

* Thu Sep  6 2007 Peter Lemenkov <lemenkov@gmail.com> 0-0.1.20070830svn2753
- svn ver. 2753 (support for W29C040P and W29EE011 chips added)
- New naming scheme

* Wed Aug 22 2007 Peter Lemenkov <lemenkov@gmail.com> 0.0-1.2744svn
- svnver. 2744

* Sun Aug  5 2007 Peter Lemenkov <lemenkov@gmail.com> 0.0-1.2742svn
- Initial build for FC-Extras
