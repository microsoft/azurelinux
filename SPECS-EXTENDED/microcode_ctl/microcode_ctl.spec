%define upstream_version 2.1-47
%global debug_package %{nil}

Summary:        Tool to transform and deploy CPU microcode update for x86
Name:           microcode_ctl
Version:        2.1
Release:        68%{?dist}
License:        GPL-2.0-or-later AND LicenseRef-Fedora-Firmware
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://pagure.io/microcode_ctl
Source0:        https://releases.pagure.org/microcode_ctl/%{name}-%{upstream_version}.tar.xz
Patch0:         enable-wildcards-in-tar.patch
ExclusiveArch:  %{ix86} x86_64
BuildRequires: make

%description
The microcode_ctl utility is a companion to the microcode driver written
by Tigran Aivazian <tigran@aivazian.fsnet.co.uk>.

The microcode update is volatile and needs to be uploaded on each system
boot i.e. it doesn't reflash your cpu permanently, reboot and it reverts
back to the old microcode.

%prep
%autosetup -p1 -n %{name}-%{upstream_version}
# License not extracted from nested tar by Makefile- do it manually here
tar --no-anchored --strip-components=1 -xvf microcode*.tar.gz license

%build
make CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} PREFIX=%{_prefix} INSDIR=/usr/sbin install clean

%files
%license license
/lib/firmware/*
%dir /usr/share/doc/microcode_ctl
%doc /usr/share/doc/microcode_ctl/*


%changelog
* Wed Feb 05 2025 Archana Shettigar <v-shettigara@microsoft.com> 2.1-68
- Initial Azure Linux import from Fedora 41 (license: MIT).
- License verified
- Remove epoch
- Enable wildcards for tar extraction

* Wed Nov 13 2024 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-67
- Update to upstream 2.1-47. 20241112
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode from revision 0x2b0005c0
    up to 0x2b000603;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode from revision 0x2b0005c0
    up to 0x2b000603;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode from revision
    0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0005c0 up to 0x2b000603;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode from revision
    0x2b0005c0 up to 0x2b000603;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x36 up to 0x37;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x36 up to 0x37;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x36 up to 0x37;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x36 up to 0x37;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x36 up to 0x37;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x36
    up to 0x37;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x36 up to 0x37;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x36 up to 0x37;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x434 up to 0x435;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x434 up to 0x435;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x434 up to 0x435;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x434
    up to 0x435;
  - Update of 06-aa-04/0xe6 (MTL-H/U C0) microcode from revision 0x1f
    up to 0x20;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x4122 up to 0x4123;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x4122 up to 0x4123;
  - Update of 06-ba-08/0xe0 microcode (in intel-ucode/06-ba-02) from
    revision 0x4122 up to 0x4123;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x4122 up to 0x4123;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode from revision 0x4122
    up to 0x4123;
  - Update of 06-ba-08/0xe0 microcode (in intel-ucode/06-ba-03) from
    revision 0x4122 up to 0x4123;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-08) from revision 0x4122 up to 0x4123;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-08) from revision 0x4122 up to 0x4123;
  - Update of 06-ba-08/0xe0 microcode from revision 0x4122 up to 0x4123;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x36 up to 0x37;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x36 up to 0x37;
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x36 up
    to 0x37;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x36 up to 0x37;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x36 up to 0x37;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x36 up to 0x37;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x36 up to 0x37;
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x36 up
    to 0x37;
  - Update of 06-cf-01/0x87 (EMR-SP A0) microcode from revision 0x21000230
    up to 0x21000283;
  - Update of 06-cf-02/0x87 (EMR-SP A1) microcode (in
    intel-ucode/06-cf-01) from revision 0x21000230 up to 0x21000283;
  - Update of 06-cf-01/0x87 (EMR-SP A0) microcode (in
    intel-ucode/06-cf-02) from revision 0x21000230 up to 0x21000283;
  - Update of 06-cf-02/0x87 (EMR-SP A1) microcode from revision 0x21000230
    up to 0x21000283.
- Addresses CVE-2024-21820, CVE-2024-21853, CVE-2024-23918, CVE-2024-23984

* Mon Nov 11 2024 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-66
- Update to upstream 2.1-46. 20241029
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x129 up
    to 0x12b.
- Resolves RHBZ#2324127

* Fri Sep 13 2024 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-65
- Update to upstream 2.1-45. 20240910
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x35 up to 0x36;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x35 up to 0x36;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x35 up to 0x36;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x35 up to 0x36;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x35 up to 0x36;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x35
    up to 0x36;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x35 up to 0x36;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x35 up to 0x36;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x433 up to 0x434;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x433 up to 0x434;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x433 up to 0x434;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x433
    up to 0x434;
  - Update of 06-aa-04/0xe6 (MTL-H/U C0) microcode from revision 0x1e
    up to 0x1f;
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x123 up
    to 0x129;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x4121 up to 0x4122;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x4121 up to 0x4122;
  - Update of 06-ba-08/0xe0 microcode (in intel-ucode/06-ba-02) from
    revision 0x4121 up to 0x4122;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x4121 up to 0x4122;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode from revision 0x4121
    up to 0x4122;
  - Update of 06-ba-08/0xe0 microcode (in intel-ucode/06-ba-03) from
    revision 0x4121 up to 0x4122;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-08) from revision 0x4121 up to 0x4122;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-08) from revision 0x4121 up to 0x4122;
  - Update of 06-ba-08/0xe0 microcode from revision 0x4121 up to 0x4122;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x35 up to 0x36;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x35 up to 0x36;
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x35 up
    to 0x36;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x35 up to 0x36;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x35 up to 0x36;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x35 up to 0x36;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x35 up to 0x36;
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x35 up
    to 0x36;
  - Update of 06-be-00/0x19 (ADL-N A0) microcode from revision 0x17 up
    to 0x1a (old pf 0x11).
- Addresses CVE-2024-23984, CVE-2024-24968
- Added the documentation directory to the list of files owned by the package
- Resolves RHBZ#2283214, RHBZ#2311299

* Thu Aug 29 2024 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-64
- Update to upstream 2.1-44. 20240813
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003605 up to 0x5003707;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002802
    up to 0x7002904;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd0003d1
    up to 0xd0003e7;
  - Update of 06-6c-01/0x10 (ICL-D B0) microcode from revision 0x1000290
    up to 0x10002b0;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xc4
    up to 0xc6;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode from revision
    0xb6 up to 0xb8;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x36 up
    to 0x38;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x50 up
    to 0x52;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xf4
    up to 0xf6;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode from revision
    0xf4 up to 0xf6;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode from
    revision 0xf4 up to 0xf6;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xf4 up
    to 0xf6;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xfa up to 0xfc;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x19 up
    to 0x1a;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xf6 up to 0xf8;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode from revision 0xf4
    up to 0xf6;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xf6 up to 0xf8;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xfc up to 0x100;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xfa up
    to 0xfc;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xfa
    up to 0xfc;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xfa
    up to 0xfc;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xfa
    up to 0xfe;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xfa up to 0xfc;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x5e up
    to 0x62;
  - Update of 06-aa-04/0xe6 (MTL-H/U C0) microcode from revision 0x1c
    up to 0x1e.
- Addresses CVE-2024-24853, CVE-2024-24980, CVE-2024-25939
- Resolves RHBZ#2305324

* Mon Aug 05 2024 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-63
- Update to upstream 2.1-43. 20240531
  - Addition of 06-aa-04/0xe6 (MTL-H/U C0) microcode at revision 0x1c;
  - Addition of 06-ba-08/0xe0 microcode (in intel-ucode/06-ba-02) at
    revision 0x4121;
  - Addition of 06-ba-08/0xe0 microcode (in intel-ucode/06-ba-03) at
    revision 0x4121;
  - Addition of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-08) at revision 0x4121;
  - Addition of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-08) at revision 0x4121;
  - Addition of 06-ba-08/0xe0 microcode at revision 0x4121;
  - Addition of 06-cf-01/0x87 (EMR-SP A0) microcode at revision
    0x21000230;
  - Addition of 06-cf-02/0x87 (EMR-SP A1) microcode (in
    intel-ucode/06-cf-01) at revision 0x21000230;
  - Addition of 06-cf-01/0x87 (EMR-SP A0) microcode (in
    intel-ucode/06-cf-02) at revision 0x21000230;
  - Addition of 06-cf-02/0x87 (EMR-SP A1) microcode at revision
    0x21000230;
  - Removal of 06-8f-04/0x10 microcode at revision 0x2c000290;
  - Removal of 06-8f-04/0x87 (SPR-SP E0/S1) microcode at revision
    0x2b0004d0;
  - Removal of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) at revision 0x2c000290;
  - Removal of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b0004d0;
  - Removal of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-04) at
    revision 0x2c000290;
  - Removal of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b0004d0;
  - Removal of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b0004d0;
  - Removal of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2c000290;
  - Removal of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b0004d0;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000181
    up to 0x1000191;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003604
    up to 0x4003605;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003604 up to 0x5003605;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002703
    up to 0x7002802;
  - Update of 06-56-05/0x10 (BDX-NS A0/A1, HWL A1) microcode from revision
    0xe000014 up to 0xe000015;
  - Update of 06-5f-01/0x01 (DNV B0) microcode from revision 0x38 up
    to 0x3e;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd0003b9
    up to 0xd0003d1;
  - Update of 06-6c-01/0x10 (ICL-D B0) microcode from revision 0x1000268
    up to 0x1000290;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x3e up
    to 0x42;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x22 up
    to 0x24;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xc2
    up to 0xc4;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode from revision
    0xb4 up to 0xb6;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x34 up
    to 0x36;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x4e up
    to 0x50;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xf8 up to 0xfa;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode from revision
    0x2c000290 up to 0x2c000390;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode from revision 0x2b0004d0
    up to 0x2b0005c0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) from
    revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-06/0x10 microcode from revision 0x2c000290 up to
    0x2c000390;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode from revision 0x2b0004d0
    up to 0x2b0005c0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode from revision
    0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000290 up to 0x2c000390;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode from revision
    0x2c000290 up to 0x2c000390;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode from revision
    0x2b0004d0 up to 0x2b0005c0;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x17 up
    to 0x19;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x32 up to 0x35;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x32 up to 0x35;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x32 up to 0x35;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x32 up to 0x35;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x32 up to 0x35;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x32
    up to 0x35;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x32 up to 0x35;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x32 up to 0x35;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x430 up to 0x433;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x430 up to 0x433;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x430 up to 0x433;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x430
    up to 0x433;
  - Update of 06-9a-04/0x40 (AZB A0) microcode from revision 0x5 up
    to 0x7;
  - Update of 06-9c-00/0x01 (JSL A0/A1) microcode from revision 0x24000024
    up to 0x24000026;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from
    revision 0xf4 up to 0xf8;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xf4 up to 0xf6;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xf4 up to 0xf6;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xfa up to 0xfc;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xf8 up
    to 0xfa;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xf8
    up to 0xfa;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xf8
    up to 0xfa;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xf8
    up to 0xfa;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xf8 up to 0xfa;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x5d up
    to 0x5e;
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x11d up
    to 0x123;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x411c up to 0x4121;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x411c up to 0x4121;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x411c up to 0x4121;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode from revision 0x411c
    up to 0x4121;
  - Update of 06-be-00/0x11 (ADL-N A0) microcode from revision 0x12 up
    to 0x17;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x32 up to 0x35;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x32 up to 0x35;
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x32 up
    to 0x35;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x32 up to 0x35;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x32 up to 0x35;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x32 up to 0x35;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x32 up to 0x35;
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x32 up
    to 0x35.
- Addresses CVE-2023-22655, CVE-2023-23583. CVE-2023-28746,
  CVE-2023-38575, CVE-2023-39368, CVE-2023-42667, CVE-2023-43490,
  CVE-2023-45733, CVE-2023-46103, CVE-2023-49141

* Thu Jul 18 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-62
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Thu Jan 25 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-61
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Sun Jan 21 2024 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-60
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Wed Jan 10 2024 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-59
- migrated to SPDX license

* Tue Nov 14 2023 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-58
- Update to upstream 2.1-42. 20231114
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd0003a5
    up to 0xd0003b9;
  - Update of 06-6c-01/0x10 (ICL-D B0) microcode from revision 0x1000230
    up to 0x1000268;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xbc
    up to 0xc2;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode from revision
    0xac up to 0xb4;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x2c up
    to 0x34;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x46 up
    to 0x4e;
  - Update of 06-8f-04/0x10 microcode from revision 0x2c000271 up to
    0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode from revision
    0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-04) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode from revision
    0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode from revision 0x2b0004b1
    up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode from revision 0x2c000271 up to
    0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode from revision 0x2b0004b1
    up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode from revision
    0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c000271 up to 0x2c000290;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode from revision
    0x2c000271 up to 0x2c000290;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode from revision
    0x2b0004b1 up to 0x2b0004d0;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x2e up to 0x32;
  - Update of 06-bf-02/0x07 (RPL-S 8+8 C0) microcode (in
    intel-ucode/06-97-02) from revision 0x2e up to 0x32;
  - Update of 06-bf-05/0x07 (RPL-S 6+0 C0) microcode (in
    intel-ucode/06-97-02) from revision 0x2e up to 0x32;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x2e
    up to 0x32;
  - Update of 06-bf-02/0x07 (RPL-S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x2e up to 0x32;
  - Update of 06-bf-05/0x07 (RPL-S 6+0 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x2e up to 0x32;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x42c up to 0x430;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x42c up to 0x430;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x42c up to 0x430;
  - Update of 06-9a-04/0x40 (AZB A0) microcode from revision 0x4 up
    to 0x5;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x42c
    up to 0x430;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x59 up
    to 0x5d;
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x119 up
    to 0x11d;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x4119 up to 0x411c;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x4119 up to 0x411c;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x4119 up to 0x411c;
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode from revision 0x4119
    up to 0x411c;
  - Update of 06-be-00/0x11 (ADL-N A0) microcode from revision 0x11 up
    to 0x12;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2e up to 0x32;
  - Update of 06-bf-02/0x07 (RPL-S 8+8 C0) microcode from revision 0x2e
    up to 0x32;
  - Update of 06-bf-05/0x07 (RPL-S 6+0 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2e up to 0x32;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2e up to 0x32;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2e up to 0x32;
  - Update of 06-bf-02/0x07 (RPL-S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2e up to 0x32;
  - Update of 06-bf-05/0x07 (RPL-S 6+0 C0) microcode from revision 0x2e
    up to 0x32.
- Addresses CVE-2023-23583

* Thu Aug 10 2023 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-57
- Update to upstream 2.1-41. 20230808
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000171
    up to 0x1000181;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006f05 up to 0x2007006;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003501
    up to 0x4003604;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003501 up to 0x5003604;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002601
    up to 0x7002703;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000390
    up to 0xd0003a5;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xba
    up to 0xbc;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode from revision
    0xaa up to 0xac;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x2a up
    to 0x2c;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x44 up
    to 0x46;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode from revision
    0xf2 up to 0xf4;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xf2
    up to 0xf4;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode from
    revision 0xf2 up to 0xf4;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xf2 up
    to 0xf4;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xf6 up to 0xf8;
  - Update of 06-8f-04/0x10 microcode from revision 0x2c0001d1 up to
    0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode from revision
    0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-04) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode from revision
    0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode from revision 0x2b000461
    up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-05) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode from revision 0x2c0001d1 up to
    0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode from revision 0x2b000461
    up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode from revision
    0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) from revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-06/0x10 microcode (in intel-ucode/06-8f-08) from
    revision 0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) from revision 0x2b000461 up to 0x2b0004b1;
  - Update of 06-8f-08/0x10 (SPR-HBM B3) microcode from revision
    0x2c0001d1 up to 0x2c000271;
  - Update of 06-8f-08/0x87 (SPR-SP E5/S3) microcode from revision
    0x2b000461 up to 0x2b0004b1;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x2c up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x2c up to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x2c up to 0x2e;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x2c
    up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x2c up to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x2c up to 0x2e;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x42a up to 0x42c;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x42a up to 0x42c;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x42a up to 0x42c;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x42a
    up to 0x42c;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from
    revision 0xf2 up to 0xf4;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xf2 up to 0xf4;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode from revision 0xf2
    up to 0xf4;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xf2 up to 0xf4;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xf8 up to 0xfa;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xf6 up
    to 0xf8;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xf6
    up to 0xf8;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xf6
    up to 0xf8;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xf6
    up to 0xf8;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xf6 up to 0xf8;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x58 up
    to 0x59;
  - Update of 06-b7-01/0x32 (RPL-S B0) microcode from revision 0x113 up
    to 0x119;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x2c up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x2c up
    to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x2c up to 0x2e;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2c up to 0x2e;
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x2c up to 0x2e;
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x2c up to 0x2e;
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x2c up
    to 0x2e;
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode from revision
    0x4112 up to 0x4119 (old pf 0xc0);
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) from revision 0x4112 up to 0x4119 (old pf 0xc0);
  - Update of 06-ba-02/0xe0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) from revision 0x4112 up to 0x4119 (old pf 0xc0);
  - Update of 06-ba-03/0xe0 (RPL-U 2+8 Q0) microcode from revision 0x4112
    up to 0x4119 (old pf 0xc0);
  - Update of 06-be-00/0x11 (ADL-N A0) microcode from revision 0x10 up
    to 0x11 (old pf 0x1).
- Addresses CVE-2022-21216, CVE-2022-40982, CVE-2022-41804, CVE-2023-23908

* Thu Jul 20 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-56
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Thu May 25 2023 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-55
- Update to upstream 2.1-40. 20230516
  - Addition of 06-6c-01/0x10 (ICL-D B0) microcode at revision 0x1000230;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode at revision
    0x2b000461;
  - Addition of 06-8f-04/0x10 microcode at revision 0x2c0001d1;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000461;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-04) at revision 0x2c0001d1;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000461;
  - Addition of 06-8f-06/0x10 (SPR-HBM B2) microcode (in
    intel-ucode/06-8f-04) at revision 0x2c0001d1;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000461;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2b000461;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-04) at revision 0x2c0001d1;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000461;
  - Addition of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-05) at
    revision 0x2c0001d1;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode at revision
    0x2b000461;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode at revision
    0x2c0001d1;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000461;
  - Addition of 06-8f-06/0x10 (SPR-HBM B2) microcode (in
    intel-ucode/06-8f-05) at revision 0x2c0001d1;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000461;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-05) at revision 0x2b000461;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-05) at revision 0x2c0001d1;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000461;
  - Addition of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-06) at
    revision 0x2c0001d1;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000461;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-06) at revision 0x2c0001d1;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode at revision
    0x2b000461;
  - Addition of 06-8f-06/0x10 (SPR-HBM B2) microcode at revision
    0x2c0001d1;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000461;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-06) at revision 0x2b000461;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode (in
    intel-ucode/06-8f-06) at revision 0x2c0001d1;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000461;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000461;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000461;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode at revision
    0x2b000461;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode (in
    intel-ucode/06-8f-07) at revision 0x2b000461;
  - Addition of 06-8f-04/0x87 (SPR-SP E0/S1) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000461;
  - Addition of 06-8f-04/0x10 microcode (in intel-ucode/06-8f-08) at
    revision 0x2c0001d1;
  - Addition of 06-8f-05/0x87 (SPR-SP E2) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000461;
  - Addition of 06-8f-05/0x10 (SPR-HBM B1) microcode (in
    intel-ucode/06-8f-08) at revision 0x2c0001d1;
  - Addition of 06-8f-06/0x87 (SPR-SP E3) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000461;
  - Addition of 06-8f-06/0x10 (SPR-HBM B2) microcode (in
    intel-ucode/06-8f-08) at revision 0x2c0001d1;
  - Addition of 06-8f-07/0x87 (SPR-SP E4/S2) microcode (in
    intel-ucode/06-8f-08) at revision 0x2b000461;
  - Addition of 06-8f-08/0x87 (SPR-SP E5/S3) microcode at revision
    0x2b000461;
  - Addition of 06-8f-08/0x10 (SPR-HBM B3) microcode at revision
    0x2c0001d1;
  - Addition of 06-b7-01/0x32 (RPL-S S0) microcode at revision 0x113;
  - Addition of 06-ba-02/0xc0 (RPL-H 6+8/P 6+8 J0) microcode at revision
    0x4112;
  - Addition of 06-ba-03/0xc0 (RPL-U 2+8 Q0) microcode (in
    intel-ucode/06-ba-02) at revision 0x4112;
  - Addition of 06-ba-02/0xc0 (RPL-H 6+8/P 6+8 J0) microcode (in
    intel-ucode/06-ba-03) at revision 0x4112;
  - Addition of 06-ba-03/0xc0 (RPL-U 2+8 Q0) microcode at revision 0x4112;
  - Addition of 06-be-00/0x01 (ADL-N A0) microcode at revision 0x10;
  - Addition of 06-9a-04/0x40 (AZB A0/R0) microcode at revision 0x4;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015e
    up to 0x1000171;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006e05 up to 0x2006f05;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003302
    up to 0x4003501;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003302 up to 0x5003501;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002501
    up to 0x7002601;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000375
    up to 0xd000390;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x3c up
    to 0x3e;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x20 up
    to 0x22;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xb2
    up to 0xba;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x31 up
    to 0x33;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode from revision
    0xa4 up to 0xaa;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x28 up
    to 0x2a;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x40 up
    to 0x44;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xf0
    up to 0xf2;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode from
    revision 0xf0 up to 0xf2;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xf0 up
    to 0xf2;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xf0 up to 0xf6;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x16 up
    to 0x17;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x421 up to 0x42a;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x421 up to 0x42a;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x421 up to 0x42a;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x421
    up to 0x42a;
  - Update of 06-9c-00/0x01 (JSL A0/A1) microcode from revision 0x24000023
    up to 0x24000024;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from
    revision 0xf0 up to 0xf2;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xf0 up to 0xf2;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode from revision 0xf0
    up to 0xf2;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xf0 up to 0xf2;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xf0 up to 0xf8;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xf0 up
    to 0xf6;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xf0
    up to 0xf6;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xf0
    up to 0xf6;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xf0
    up to 0xf6;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xf0 up to 0xf6;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x54 up
    to 0x58;
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode from revision
    0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode from revision 0x22
    up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode from revision 0x22 up to
    0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-02/0x07 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-97-05/0x07 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-02/0x07 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x22 up to 0x2c (old pf 0x3);
  - Update of 06-bf-05/0x07 (ADL C0) microcode from revision 0x22 up to
    0x2c (old pf 0x3).
- Addresses CVE-2022-21216, CVE-2022-33196, CVE-2022-33972, CVE-2022-38090

* Thu Jan 19 2023 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-54
- Rebuilt for https://fedoraproject.org/wiki/Fedora_38_Mass_Rebuild

* Tue Aug 09 2022 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-53
- Update to upstream 2.1-37. 20220809
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015d
    up to 0x100015e;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006d05 up to 0x2006e05;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000363
    up to 0xd000375;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x3a up
    to 0x3c;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x1e up
    to 0x20;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xb0
    up to 0xb2;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x26 up
    to 0x28;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x3e up
    to 0x40;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode from revision
    0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) from revision 0x1f up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x1f up to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    from revision 0x1f up to 0x22;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-97-05) from revision 0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode from revision 0x1f
    up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x1f up to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    from revision 0x1f up to 0x22;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode from revision
    0x41c up to 0x421;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) from revision 0x41c up to 0x421;
  - Update of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) from revision 0x41c up to 0x421;
  - Update of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode from revision 0x41c
    up to 0x421;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x53 up
    to 0x54;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-02) from revision 0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) from revision 0x1f up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode from revision 0x1f up
    to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-bf-02)
    from revision 0x1f up to 0x22;
  - Update of 06-97-02/0x03 (ADL-HX/S 8+8 C0) microcode (in
    intel-ucode/06-bf-05) from revision 0x1f up to 0x22;
  - Update of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) from revision 0x1f up to 0x22;
  - Update of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-bf-05)
    from revision 0x1f up to 0x22;
  - Update of 06-bf-05/0x03 (ADL C0) microcode from revision 0x1f up
    to 0x22.
- Addresses CVE-2022-21233

* Thu Jul 21 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-52
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild

* Tue May 10 2022 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-51
- Update to upstream 2.1-36. 20220510
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-97-02) at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-02)
    at revision 0x1f;
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode (in
    intel-ucode/06-97-05) at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-97-05)
    at revision 0x1f;
  - Addition of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode at
    revision 0x41c;
  - Addition of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode (in
    intel-ucode/06-9a-03) at revision 0x41c;
  - Addition of 06-9a-03/0x80 (ADL-P 6+8/U 9W L0/R0) microcode (in
    intel-ucode/06-9a-04) at revision 0x41c;
  - Addition of 06-9a-04/0x80 (ADL-P 2+8 R0) microcode at revision 0x41c;
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode (in
    intel-ucode/06-bf-02) at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-02) at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode (in intel-ucode/06-bf-02)
    at revision 0x1f;
  - Addition of 06-97-02/0x03 (ADL-HX C0) microcode (in
    intel-ucode/06-bf-05) at revision 0x1f;
  - Addition of 06-97-05/0x03 (ADL-S 6+0 K0) microcode (in
    intel-ucode/06-bf-05) at revision 0x1f;
  - Addition of 06-bf-02/0x03 (ADL C0) microcode (in intel-ucode/06-bf-05)
    at revision 0x1f;
  - Addition of 06-bf-05/0x03 (ADL C0) microcode at revision 0x1f;
  - Update of 06-37-09/0x0f (VLV D0) microcode from revision 0x90c up
    to 0x90d;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode from revision
    0xec up to 0xf0;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015c
    up to 0x100015d;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006c0a up to 0x2006d05;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x400320a
    up to 0x4003302;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x500320a up to 0x5003302;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002402
    up to 0x7002501;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x46 up
    to 0x48;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode from
    revision 0xec up to 0xf0;
  - Update of 06-5f-01/0x01 (DNV B0) microcode from revision 0x36 up
    to 0x38;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd000331
    up to 0xd000363;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x38 up
    to 0x3a;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x1c up
    to 0x1e;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xa8
    up to 0xb0;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x2d up
    to 0x31;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode from revision
    0x9a up to 0xa4;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x22 up
    to 0x26;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x3c up
    to 0x3e;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xec
    up to 0xf0;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode from revision
    0xec up to 0xf0;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode from
    revision 0xec up to 0xf0;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xec up
    to 0xf0;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xec up to 0xf0;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x15 up
    to 0x16;
  - Update of 06-9c-00/0x01 (JSL A0/A1) microcode from revision 0x2400001f
    up to 0x24000023;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from
    revision 0xec up to 0xf0;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xec up to 0xf0;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode from revision 0xec
    up to 0xf0;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xec up to 0xf0;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xec up to 0xf0;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xec up
    to 0xf0;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xec
    up to 0xf0;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xee
    up to 0xf0;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xea
    up to 0xf0;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xec up to 0xf0;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x50 up
    to 0x53.
- Addresses CVE-2022-0005, CVE-2022-21131, CVE-2022-21136, CVE-2022-21151

* Tue May 10 2022 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-50
- Update to upstream 2.1-35. 20220419
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x24 up
    to 0x28.

* Wed Feb 09 2022 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-49
- Update to upstream 2.1-34. 20220207
  - Removal of 06-86-04/0x01 (SNR B0) microcode at revision 0xb00000f;
  - Removal of 06-86-05/0x01 (SNR B1) microcode (in intel-ucode/06-86-04)
    at revision 0xb00000f;
  - Removal of 06-86-04/0x01 (SNR B0) microcode (in intel-ucode/06-86-05)
    at revision 0xb00000f;
  - Removal of 06-86-05/0x01 (SNR B1) microcode at revision 0xb00000f;
  - Update of 06-4f-01/0xef (BDX-E/EP/EX/ML B0/M0/R0) microcode (in
    intel-ucode-with-caveats/06-4f-01) from revision 0xb00003e up to
    0xb000040;
  - Update of 06-3f-02/0x6f (HSX-E/EN/EP/EP 4S C0/C1/M1/R2) microcode
    from revision 0x46 up to 0x49;
  - Update of 06-3f-04/0x80 (HSX-EX E0) microcode from revision 0x19 up
    to 0x1a;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode from revision
    0xea up to 0xec;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x100015b
    up to 0x100015c;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006b06 up to 0x2006c0a;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003102
    up to 0x400320a;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003102 up to 0x500320a;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x7002302
    up to 0x7002402;
  - Update of 06-56-03/0x10 (BDX-DE V2/V3) microcode from revision
    0x700001b up to 0x700001c;
  - Update of 06-56-04/0x10 (BDX-DE Y0) microcode from revision 0xf000019
    up to 0xf00001a;
  - Update of 06-56-05/0x10 (BDX-NS A0/A1, HWL A1) microcode from revision
    0xe000012 up to 0xe000014;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x44 up
    to 0x46;
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x20 up
    to 0x24;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode from
    revision 0xea up to 0xec;
  - Update of 06-5f-01/0x01 (DNV B0) microcode from revision 0x34 up
    to 0x36;
  - Update of 06-6a-06/0x87 (ICX-SP D0) microcode from revision 0xd0002a0
    up to 0xd000331;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x36 up
    to 0x38;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x1a up
    to 0x1c;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xa6
    up to 0xa8;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x2a up
    to 0x2d;
  - Update of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode from revision
    0x88 up to 0x9a;
  - Update of 06-8c-02/0xc2 (TGL-R C0) microcode from revision 0x16 up
    to 0x22;
  - Update of 06-8d-01/0xc2 (TGL-H R0) microcode from revision 0x2c up
    to 0x3c;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xea
    up to 0xec;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode from revision
    0xea up to 0xec;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode from
    revision 0xea up to 0xec;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xea up
    to 0xec;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xea up to 0xec;
  - Update of 06-96-01/0x01 (EHL B1) microcode from revision 0x11 up
    to 0x15;
  - Update of 06-9c-00/0x01 (JSL A0/A1) microcode from revision 0x1d up
    to 0x2400001f;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from
    revision 0xea up to 0xec;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xea up to 0xec;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode from revision 0xea
    up to 0xec;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xea up to 0xec;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xea up to 0xec;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xea up
    to 0xec;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xea
    up to 0xec;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xec
    up to 0xee;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xe8
    up to 0xea;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xea up to 0xec;
  - Update of 06-a7-01/0x02 (RKL-S B0) microcode from revision 0x40 up
    to 0x50.

* Thu Jan 20 2022 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-48
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Thu Jul 22 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-47
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Tue Jun 08 2021 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-46
- Update to upstream 2.1-33. 20210608
  - Addition of 06-55-05/0xb7 (CLX-SP A0) microcode at revision 0x3000010;
  - Addition of 06-6a-05/0x87 (ICX-SP C0) microcode at revision 0xc0002f0;
  - Addition of 06-6a-06/0x87 (ICX-SP D0) microcode at revision 0xd0002a0;
  - Addition of 06-86-04/0x01 (SNR B0) microcode at revision 0xb00000f;
  - Addition of 06-86-05/0x01 (SNR B1) microcode (in intel-ucode/06-86-04)
    at revision 0xb00000f;
  - Addition of 06-86-04/0x01 (SNR B0) microcode (in intel-ucode/06-86-05)
    at revision 0xb00000f;
  - Addition of 06-86-05/0x01 (SNR B1) microcode at revision 0xb00000f;
  - Addition of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode at revision 0x88;
  - Addition of 06-8c-02/0xc2 (TGL-R C0) microcode at revision 0x16;
  - Addition of 06-8d-01/0xc2 (TGL-H R0) microcode at revision 0x2c;
  - Addition of 06-96-01/0x01 (EHL B1) microcode at revision 0x11;
  - Addition of 06-9c-00/0x01 (JSL A0/A1) microcode at revision 0x1d;
  - Addition of 06-a7-01/0x02 (RKL-S B0) microcode at revision 0x40;
  - Update of 06-4f-01/0xef (BDX-E/EP/EX/ML B0/M0/R0) microcode (in
    intel-ucode-with-caveats/06-4f-01) from revision 0xb000038 up to
    0xb00003e;
  - Update of 06-3f-02/0x6f (HSX-E/EN/EP/EP 4S C0/C1/M1/R2) microcode
    from revision 0x44 up to 0x46;
  - Update of 06-3f-04/0x80 (HSX-EX E0) microcode from revision 0x16 up
    to 0x19;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode from revision
    0xe2 up to 0xea;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000159
    up to 0x100015b;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006a0a up to 0x2006b06;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003006
    up to 0x4003102;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003006 up to 0x5003102;
  - Update of 06-55-0b/0xbf (CPX-SP A1) microcode from revision 0x700001e
    up to 0x7002302;
  - Update of 06-56-03/0x10 (BDX-DE V2/V3) microcode from revision
    0x7000019 up to 0x700001b;
  - Update of 06-56-04/0x10 (BDX-DE Y0) microcode from revision 0xf000017
    up to 0xf000019;
  - Update of 06-56-05/0x10 (BDX-NS A0/A1, HWL A1) microcode from revision
    0xe00000f up to 0xe000012;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x40 up
    to 0x44;
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x1e up
    to 0x20;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode from
    revision 0xe2 up to 0xea;
  - Update of 06-5f-01/0x01 (DNV B0) microcode from revision 0x2e up
    to 0x34;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x34 up
    to 0x36;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x18 up
    to 0x1a;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0xa0
    up to 0xa6;
  - Update of 06-8a-01/0x10 (LKF B2/B3) microcode from revision 0x28 up
    to 0x2a;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xde
    up to 0xea;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode from revision
    0xde up to 0xea;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode from
    revision 0xe0 up to 0xea;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xde up
    to 0xea;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xde up to 0xea;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from
    revision 0xde up to 0xea;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xde up to 0xea;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode from revision 0xde
    up to 0xea;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xde up to 0xea;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xde up to 0xea;
  - Update of 06-a5-02/0x20 (CML-H R1) microcode from revision 0xe0 up
    to 0xea;
  - Update of 06-a5-03/0x22 (CML-S 6+2 G1) microcode from revision 0xe0
    up to 0xea;
  - Update of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode from revision 0xe0
    up to 0xec;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xe0
    up to 0xe8;
  - Update of 06-a6-01/0x80 (CML-U 6+2 v2 K1) microcode from revision
    0xe0 up to 0xea.

* Wed Feb 17 2021 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-45
- Update to upstream 2.1-32. 20210216
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006a08 up to 0x2006a0a;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4003003
    up to 0x4003006;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5003003 up to 0x5003006.

* Tue Jan 26 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-44
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Nov 20 2020 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-43
- Update to upstream 2.1-31. 20201118
  - Removal of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode at revision 0x68;
  - Update of 06-7a-01/0x01 (GLK B0) microcode from revision 0x32 up
    to 0x34.

* Wed Nov 11 2020 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-42
- Fix incorrect CVE numbers in the previous changelog entry

* Wed Nov 11 2020 Eugene Syromiatnikov <esyr@redhat.com> 2:2.1-41
- Update to upstream 2.1-30. 20201110
  - Addition of 06-55-0b/0xbf (CPX-SP A1) microcode at revision 0x700001e;
  - Addition of 06-8a-01/0x10 (LKF B2/B3) microcode at revision 0x28;
  - Addition of 06-8c-01/0x80 (TGL-UP3/UP4 B1) microcode at revision 0x68;
  - Addition of 06-a5-02/0x20 (CML-H R1) microcode at revision 0xe0;
  - Addition of 06-a5-03/0x22 (CML-S 6+2 G1) microcode at revision 0xe0;
  - Addition of 06-a5-05/0x22 (CML-S 10+2 Q0) microcode at revision 0xe0;
  - Addition of 06-a6-01/0x80 (CML-U 6+2 v2 K0) microcode at revision
    0xe0;
  - Update of 06-3f-02/0x6f (HSX-E/EN/EP/EP 4S C0/C1/M1/R2) microcode
    from revision 0x43 up to 0x44;
  - Update of 06-4e-03/0xc0 (SKL-U/U 2+3e/Y D0/K1) microcode from revision
    0xd6 up to 0xe2;
  - Update of 06-55-03/0x97 (SKX-SP B1) microcode from revision 0x1000157
    up to 0x1000159;
  - Update of 06-55-04/0xb7 (SKX-D/SP/W/X H0/M0/M1/U0) microcode from
    revision 0x2006906 up to 0x2006a08;
  - Update of 06-55-06/0xbf (CLX-SP B0) microcode from revision 0x4002f01
    up to 0x4003003;
  - Update of 06-55-07/0xbf (CLX-SP/W/X B1/L1) microcode from revision
    0x5002f01 up to 0x5003003;
  - Update of 06-5c-09/0x03 (APL D0) microcode from revision 0x38 up
    to 0x40;
  - Update of 06-5c-0a/0x03 (APL B1/F1) microcode from revision 0x16 up
    to 0x1e;
  - Update of 06-5e-03/0x36 (SKL-H/S/Xeon E3 N0/R0/S0) microcode from
    revision 0xd6 up to 0xe2;
  - Update of 06-7a-08/0x01 (GLK-R R0) microcode from revision 0x16 up
    to 0x18;
  - Update of 06-7e-05/0x80 (ICL-U/Y D1) microcode from revision 0x78
    up to 0xa0;
  - Update of 06-8e-09/0x10 (AML-Y 2+2 H0) microcode from revision 0xd6
    up to 0xde;
  - Update of 06-8e-09/0xc0 (KBL-U/U 2+3e/Y H0/J1) microcode from revision
    0xd6 up to 0xde;
  - Update of 06-8e-0a/0xc0 (CFL-U 4+3e D0, KBL-R Y0) microcode from
    revision 0xd6 up to 0xe0;
  - Update of 06-8e-0b/0xd0 (WHL-U W0) microcode from revision 0xd6 up
    to 0xde;
  - Update of 06-8e-0c/0x94 (AML-Y 4+2 V0, CML-U 4+2 V0, WHL-U V0)
    microcode from revision 0xd6 up to 0xde;
  - Update of 06-9e-09/0x2a (KBL-G/H/S/X/Xeon E3 B0) microcode from
    revision 0xd6 up to 0xde;
  - Update of 06-9e-0a/0x22 (CFL-H/S/Xeon E U0) microcode from revision
    0xd6 up to 0xde;
  - Update of 06-9e-0b/0x02 (CFL-E/H/S B0) microcode from revision 0xd6
    up to 0xde;
  - Update of 06-9e-0c/0x22 (CFL-H/S/Xeon E P0) microcode from revision
    0xd6 up to 0xde;
  - Update of 06-9e-0d/0x22 (CFL-H/S/Xeon E R0) microcode from revision
    0xd6 up to 0xde;
  - Update of 06-a6-00/0x80 (CML-U 6+2 A0) microcode from revision 0xca
    up to 0xe0.
- Addresses CVE-2020-8695, CVE-2020-8696, CVE-2020-8698

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-40
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jun 16 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-39
- Update to upstream 2.1-29. 20200616

* Wed Jun 10 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-38
- Update to upstream 2.1-28. 20200609

* Thu May 21 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-37
- Update to upstream 2.1-27. 20200520

* Mon May 11 2020 Anton Arapov <aarapov@redhat.com> 2:2.1-36
- Update to upstream 2.1-26. 20200508

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-35
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Mon Nov 18 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-34
- Update to upstream 2.1-25. 20191115

* Tue Nov 12 2019 Justin Forbes <jforbes@fedoraproject.org> 2:2.1-33
- Update to microcode-20191112 for CVE fixes

* Wed Oct 02 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-32
- Update to upstream 2.1-23. 20190918

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-31
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Thu Jun 20 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-30
- Update to upstream 2.1-22. 20190618

* Wed May 15 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-29
- Update to upstream 2.1-21. 20190514

* Thu May 09 2019 Anton Arapov <aarapov@redhat.com> 2:2.1-28
- Update to upstream 2.1-20. 20190312

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 13 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-26
- Update to upstream 2.1-19. 20180807

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-25
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-24
- Update to upstream 2.1-18. 20180703

* Wed May 16 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-23
- Update to upstream 2.1-17. 20180425

* Thu Mar 15 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-22
- Update to upstream 2.1-16. 20180312

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Tue Jan 09 2018 Anton Arapov <aarapov@redhat.com> 2:2.1-20
- Update to upstream 2.1-15. 20180108

* Tue Nov 21 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-19
- Update to upstream 2.1-14. 20171117

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-16
- Update to upstream 2.1-13. 20170707

* Tue May 23 2017 Anton Arapov <aarapov@redhat.com> 2:2.1-15
- Update to upstream 2.1-12. 20170511

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Dec 02 2016 Anton Arapov <arapov@gmail.com> 2.1-13.1
- Update to upstream 2.1-11. 20161104

* Thu Jul 21 2016 Anton Arapov <arapov@gmail.com> 2.1-13
- Update to upstream 2.1-10. 20160714
- Fixes rhbz#1353103

* Fri Jun 24 2016 Anton Arapov <arapov@gmail.com> 2.1-12
- Update to upstream 2.1-9. 20160607

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Jan 12 2016 Anton Arapov <arapov@gmail.com> 2.1-10
- Update to upstream 2.1-8. 20151106

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Feb 03 2015 Anton Arapov <arapov@gmail.com> 2.1-8.1
- Update to upstream 2.1-7. 20150121

* Sun Sep 21 2014 Anton Arapov <arapov@gmail.com> 2.1-8
- Update to upstream 2.1-6. 20140913

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 08 2014 Anton Arapov <anton@descope.org> 2.1-6
- Update to upstream 2.1-5. 20140624

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu May 01 2014 Anton Arapov <anton@redhat.com> 2.1-4
- Update to upstream 2.1-4.

* Fri Jan 24 2014 Anton Arapov <anton@redhat.com> 2.1-3
- Update to upstream 2.1-3.

* Mon Sep 09 2013 Anton Arapov <anton@redhat.com> 2.1-2
- Update to upstream 2.1-2.

* Wed Aug 14 2013 Anton Arapov <anton@redhat.com> 2.1-1
- Update to upstream 2.1-1.

* Sat Jul 27 2013 Anton Arapov <anton@redhat.com> 2.1-0
- Update to upstream 2.1. AMD microcode has been removed, find it in linux-firmware.

* Wed Apr 03 2013 Anton Arapov <anton@redhat.com> 2.0-3.1
- Update to upstream 2.0-3

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2:2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Oct 17 2012 Anton Arapov <anton@redhat.com> 2.0-2
- Update to upstream 2.0-2

* Tue Oct 02 2012 Anton Arapov <anton@redhat.com> 2.0-1
- Update to upstream 2.0-1

* Mon Aug 06 2012 Anton Arapov <anton@redhat.com> 2.0
- Update to upstream 2.0

* Wed Jul 25 2012 Anton Arapov <anton@redhat.com> 1.18-1
- Update to upstream 1.18

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Anton Arapov <anton@redhat.com> 1.17-25
- Update to microcode-20120606.dat

* Tue Feb 07 2012 Anton Arapov <anton@redhat.com> 1.17-24
- Update to amd-ucode-2012-01-17.tar

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Dec 22 2011 Anton Arapov <anton@redhat.com> 1.17-21
- Fix a segfault that may be triggered by very long parameter [#768803]

* Tue Dec 13 2011 Anton Arapov <anton@redhat.com> 1.17-20
- Update to microcode-20111110.dat

* Tue Sep 27 2011 Anton Arapov <anton@redhat.com> 1.17-19
- Update to microcode-20110915.dat

* Thu Aug 04 2011 Anton Arapov <anton@redhat.com> 1.17-18
- Ship splitted microcode for Intel CPUs [#690930]
- Include tool for splitting microcode for Intl CPUs (Kay Sievers )

* Thu Jun 30 2011 Anton Arapov <anton@redhat.com> 1.17-17
- Fix udev rules (Dave Jones ) [#690930]

* Thu May 12 2011 Anton Arapov <anton@redhat.com> 1.17-14
- Update to microcode-20110428.dat

* Thu Mar 24 2011 Anton Arapov <anton@redhat.com> 1.17-13
- fix memory leak.

* Mon Mar 07 2011 Anton Arapov <anton@redhat.com> 1.17-12
- Update to amd-ucode-2011-01-11.tar

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jan 19 2011 Anton Arapov <anton@redhat.com> 1.17-10
- manpage fix (John Bradshaw ) [#670879]

* Wed Jan 05 2011 Anton Arapov <anton@redhat.com> 1.17-9
- Update to microcode-20101123.dat

* Mon Nov 01 2010 Anton Arapov <anton@redhat.com> 1.17-8
- Update to microcode-20100914.dat

* Wed Sep 29 2010 jkeating - 1:1.17-7
- Rebuilt for gcc bug 634757

* Wed Sep 15 2010 Anton Arapov <anton@redhat.com> 1.17-6
- Update to microcode-20100826.dat

* Tue Sep 07 2010 Toshio Kuratomi <toshio@fedoraproject.org> 1.17-5
- Fix license tag: bz#450491

* Fri Aug 27 2010 Dave Jones <davej@redhat.com> 1.17-4
- Update to microcode-20100826.dat

* Tue Mar 23 2010 Anton Arapov <anton@redhat.com> 1.17-3
- Fix the udev rules (Harald Hoyer )

* Mon Mar 22 2010 Anton Arapov <anton@redhat.com> 1.17-2
- Make microcode_ctl event driven (Bill Nottingham ) [#479898]

* Thu Feb 11 2010 Dave Jones <davej@redhat.com> 1.17-1.58
- Update to microcode-20100209.dat

* Fri Dec 04 2009 Kyle McMartin <kyle@redhat.com> 1.17-1.57
- Fix duplicate message pointed out by Edward Sheldrake.

* Wed Dec 02 2009 Kyle McMartin <kyle@redhat.com> 1.17-1.56
- Add AMD x86/x86-64 microcode. (Dated: 2009-10-09)
  Doesn't need microcode_ctl modifications as it's loaded by
  request_firmware() like any other sensible driver.
- Eventually, this AMD firmware can probably live inside
  kernel-firmware once it is split out.

* Wed Sep 30 2009 Dave Jones <davej@redhat.com>
- Update to microcode-20090927.dat

* Fri Sep 11 2009 Dave Jones <davej@redhat.com>
- Remove some unnecessary code from the init script.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.52.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jun 25 2009 Dave Jones <davej@redhat.com>
- Shorten sleep time during init.
  This really needs to be replaced with proper udev hooks, but this is
  a quick interim fix.

* Wed Jun 03 2009 Kyle McMartin <kyle@redhat.com> 1:1.17-1.50
- Change ExclusiveArch to i586 instead of i386. Resolves rhbz#497711.

* Wed May 13 2009 Dave Jones <davej@redhat.com>
- update to microcode 20090330

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.17-1.46.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Sep 12 2008 Dave Jones <davej@redhat.com>
- update to microcode 20080910

* Tue Apr 01 2008 Jarod Wilson <jwilson@redhat.com>
- Update to microcode 20080401

* Sat Mar 29 2008 Dave Jones <davej@redhat.com>
- Update to microcode 20080220
- Fix rpmlint warnings in specfile.

* Mon Mar 17 2008 Dave Jones <davej@redhat.com>
- specfile cleanups.

* Fri Feb 22 2008 Jarod Wilson <jwilson@redhat.com>
- Use /lib/firmware instead of /etc/firmware

* Wed Feb 13 2008 Jarod Wilson <jwilson@redhat.com>
- Fix permissions on microcode.dat

* Thu Feb 07 2008 Jarod Wilson <jwilson@redhat.com>
- Spec cleanup and macro standardization.
- Update license
- Update microcode data file to 20080131 revision.

* Mon Jul  2 2007 Dave Jones <davej@redhat.com>
- Update to upstream 1.17

* Thu Oct 12 2006 Jon Masters <jcm@redhat.com>
- BZ209455 fixes.

* Mon Jul 17 2006 Jesse Keating <jkeating@redhat.com>
- rebuild

* Fri Jun 16 2006 Bill Nottingham <notting@redhat.com>
- remove kudzu requirement
- add prereq for coreutils, awk, grep

* Thu Feb 09 2006 Dave Jones <davej@redhat.com>
- rebuild.

* Fri Jan 27 2006 Dave Jones <davej@redhat.com>
- Update to upstream 1.13

* Fri Dec 16 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt for new gcj

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 14 2005 Dave Jones <davej@redhat.com>
- initscript tweaks.

* Tue Sep 13 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.12

* Wed Aug 17 2005 Dave Jones <davej@redhat.com>
- Check for device node *after* loading the module. (#157672)

* Tue Mar  1 2005 Dave Jones <davej@redhat.com>
- Rebuild for gcc4

* Thu Feb 17 2005 Dave Jones <davej@redhat.com>
- s/Serial/Epoch/

* Tue Jan 25 2005 Dave Jones <davej@redhat.com>
- Drop the node creation/deletion change from previous release.
  It'll cause grief with selinux, and was a hack to get around
  a udev shortcoming that should be fixed properly.

* Fri Jan 21 2005 Dave Jones <davej@redhat.com>
- Create/remove the /dev/cpu/microcode dev node as needed.
- Use correct path again for the microcode.dat.
- Remove some no longer needed tests in the init script.

* Fri Jan 14 2005 Dave Jones <davej@redhat.com>
- Only enable microcode_ctl service if the CPU is capable.
- Prevent microcode_ctl getting restarted multiple times on initlevel change (#141581)
- Make restart/reload work properly
- Do nothing if not started by root.

* Wed Jan 12 2005 Dave Jones <davej@redhat.com>
- Adjust dev node location. (#144963)

* Tue Jan 11 2005 Dave Jones <davej@redhat.com>
- Load/Remove microcode module in initscript.

* Mon Jan 10 2005 Dave Jones <davej@redhat.com>
- Update to upstream 1.11 release.

* Sat Dec 18 2004 Dave Jones <davej@redhat.com>
- Initial packaging, based upon kernel-utils.

