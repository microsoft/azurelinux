%define debug_package %{nil}
%define __os_install_post %{nil}

# Gnulib does not produce source tarball releases, and grub's bootstrap.conf
# bakes in a specific commit id to pull (GNULIB_REVISION).
#
# Additionally, we are incorporating the F34 patchset and part of this patchset
# operates on the assumption that we use the rhboot/gnulib fork instead of the
# upstream gnulib project. So make sure this gnulibversion macro is tied to the
# correct gnulib source (i.e., bootstrap.conf after applying all patches)
%global gnulibversion fixes

Summary:        GRand Unified Bootloader
Name:           grub2
Version:        2.06
Release:        1%{?dist}
License:        GPLv3+
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/System
URL:            https://www.gnu.org/software/grub
Source0:        https://git.savannah.gnu.org/cgit/grub.git/snapshot/grub-%{version}-rc1.tar.gz
#Source1:        https://github.com/rhboot/gnulib/archive/%%{gnulibversion}.tar.gz
Source1:        gnulib-%{gnulibversion}.tar.gz
Source2:        sbat.csv.in

Patch0001: 0001-Add-support-for-Linux-EFI-stub-loading.patch
Patch0002: 0002-Rework-linux-command.patch
Patch0003: 0003-Rework-linux16-command.patch
Patch0004: 0004-Add-secureboot-support-on-efi-chainloader.patch
Patch0005: 0005-Make-any-of-the-loaders-that-link-in-efi-mode-honor-.patch
Patch0006: 0006-Handle-multi-arch-64-on-32-boot-in-linuxefi-loader.patch
Patch0007: 0007-re-write-.gitignore.patch
Patch0008: 0008-IBM-client-architecture-CAS-reboot-support.patch
Patch0009: 0009-for-ppc-reset-console-display-attr-when-clear-screen.patch
Patch0010: 0010-Disable-GRUB-video-support-for-IBM-power-machines.patch
Patch0011: 0011-Move-bash-completion-script-922997.patch
Patch0012: 0012-Allow-fallback-to-include-entries-by-title-not-just-.patch
Patch0013: 0013-Make-exit-take-a-return-code.patch
Patch0014: 0014-Make-efi-machines-load-an-env-block-from-a-variable.patch
Patch0015: 0015-Migrate-PPC-from-Yaboot-to-Grub2.patch
Patch0016: 0016-Add-fw_path-variable-revised.patch
Patch0017: 0017-Pass-x-hex-hex-straight-through-unmolested.patch
Patch0018: 0018-blscfg-add-blscfg-module-to-parse-Boot-Loader-Specif.patch
Patch0019: 0019-Add-devicetree-loading.patch
Patch0020: 0020-Don-t-write-messages-to-the-screen.patch
Patch0021: 0021-Don-t-print-GNU-GRUB-header.patch
Patch0022: 0022-Don-t-add-to-highlighted-row.patch
Patch0023: 0023-Message-string-cleanups.patch
Patch0024: 0024-Fix-border-spacing-now-that-we-aren-t-displaying-it.patch
Patch0025: 0025-Use-the-correct-indentation-for-the-term-help-text.patch
Patch0026: 0026-Indent-menu-entries.patch
Patch0027: 0027-Fix-margins.patch
Patch0028: 0028-Use-2-instead-of-1-for-our-right-hand-margin-so-line.patch
Patch0029: 0029-Enable-pager-by-default.-985860.patch
Patch0030: 0030-F10-doesn-t-work-on-serial-so-don-t-tell-the-user-to.patch
Patch0031: 0031-Don-t-say-GNU-Linux-in-generated-menus.patch
Patch0032: 0032-Don-t-draw-a-border-around-the-menu.patch
Patch0033: 0033-Use-the-standard-margin-for-the-timeout-string.patch
Patch0034: 0034-Add-.eh_frame-to-list-of-relocations-stripped.patch
Patch0035: 0035-Don-t-require-a-password-to-boot-entries-generated-b.patch
Patch0036: 0036-Don-t-emit-Booting-.-message.patch
Patch0037: 0037-Replace-a-lot-of-man-pages-with-slightly-nicer-ones.patch
Patch0038: 0038-use-fw_path-prefix-when-fallback-searching-for-grub-.patch
Patch0039: 0039-Try-mac-guid-etc-before-grub.cfg-on-tftp-config-file.patch
Patch0040: 0040-Generate-OS-and-CLASS-in-10_linux-from-etc-os-releas.patch
Patch0041: 0041-Minimize-the-sort-ordering-for-.debug-and-rescue-ker.patch
Patch0042: 0042-Try-prefix-if-fw_path-doesn-t-work.patch
Patch0043: 0043-Use-Distribution-Package-Sort-for-grub2-mkconfig-112.patch
Patch0044: 0044-Make-grub2-mkconfig-construct-titles-that-look-like-.patch
Patch0045: 0045-Add-friendly-grub2-password-config-tool-985962.patch
Patch0046: 0046-tcp-add-window-scaling-support.patch
Patch0047: 0047-efinet-and-bootp-add-support-for-dhcpv6.patch
Patch0048: 0048-Add-grub-get-kernel-settings-and-use-it-in-10_linux.patch
Patch0049: 0049-bz1374141-fix-incorrect-mask-for-ppc64.patch
Patch0050: 0050-Make-grub_fatal-also-backtrace.patch
Patch0051: 0051-Fix-up-some-man-pages-rpmdiff-noticed.patch
Patch0052: 0052-Make-our-info-pages-say-grub2-where-appropriate.patch
Patch0053: 0053-macos-just-build-chainloader-entries-don-t-try-any-x.patch
Patch0054: 0054-grub2-btrfs-Add-ability-to-boot-from-subvolumes.patch
Patch0055: 0055-export-btrfs_subvol-and-btrfs_subvolid.patch
Patch0056: 0056-grub2-btrfs-03-follow_default.patch
Patch0057: 0057-grub2-btrfs-04-grub2-install.patch
Patch0058: 0058-grub2-btrfs-05-grub2-mkconfig.patch
Patch0059: 0059-grub2-btrfs-06-subvol-mount.patch
Patch0060: 0060-Fallback-to-old-subvol-name-scheme-to-support-old-sn.patch
Patch0061: 0061-Grub-not-working-correctly-with-btrfs-snapshots-bsc-.patch
Patch0062: 0062-Add-grub_efi_allocate_pool-and-grub_efi_free_pool-wr.patch
Patch0063: 0063-Use-grub_efi_.-memory-helpers-where-reasonable.patch
Patch0064: 0064-Add-PRIxGRUB_EFI_STATUS-and-use-it.patch
Patch0065: 0065-don-t-use-int-for-efi-status.patch
Patch0066: 0066-make-GRUB_MOD_INIT-declare-its-function-prototypes.patch
Patch0067: 0067-Don-t-guess-boot-efi-as-HFS-on-ppc-machines-in-grub-.patch
Patch0068: 0068-20_linux_xen-load-xen-or-multiboot-2-modules-as-need.patch
Patch0069: 0069-Make-pmtimer-tsc-calibration-not-take-51-seconds-to-.patch
Patch0070: 0070-align-struct-efi_variable-better.patch
Patch0071: 0071-Add-BLS-support-to-grub-mkconfig.patch
Patch0072: 0072-Don-t-attempt-to-backtrace-on-grub_abort-for-grub-em.patch
Patch0073: 0073-Add-linux-and-initrd-commands-for-grub-emu.patch
Patch0074: 0074-Add-grub2-switch-to-blscfg.patch
Patch0075: 0075-make-better-backtraces.patch
Patch0076: 0076-normal-don-t-draw-our-startup-message-if-debug-is-se.patch
Patch0077: 0077-Work-around-some-minor-include-path-weirdnesses.patch
Patch0078: 0078-Make-it-possible-to-enabled-build-id-sha1.patch
Patch0079: 0079-Add-grub_qdprintf-grub_dprintf-without-the-file-line.patch
Patch0080: 0080-Make-a-gdb-dprintf-that-tells-us-load-addresses.patch
Patch0081: 0081-Fixup-for-newer-compiler.patch
Patch0082: 0082-Don-t-attempt-to-export-the-start-and-_start-symbols.patch
Patch0083: 0083-Fixup-for-newer-compiler.patch
Patch0084: 0084-Add-support-for-non-Ethernet-network-cards.patch
Patch0085: 0085-net-read-bracketed-ipv6-addrs-and-port-numbers.patch
Patch0086: 0086-bootp-New-net_bootp6-command.patch
Patch0087: 0087-efinet-UEFI-IPv6-PXE-support.patch
Patch0088: 0088-grub.texi-Add-net_bootp6-doument.patch
Patch0089: 0089-bootp-Add-processing-DHCPACK-packet-from-HTTP-Boot.patch
Patch0090: 0090-efinet-Setting-network-from-UEFI-device-path.patch
Patch0091: 0091-efinet-Setting-DNS-server-from-UEFI-protocol.patch
Patch0092: 0092-Support-UEFI-networking-protocols.patch
Patch0093: 0093-AUDIT-0-http-boot-tracker-bug.patch
Patch0094: 0094-grub-editenv-Add-incr-command-to-increment-integer-v.patch
Patch0095: 0095-Add-auto-hide-menu-support.patch
Patch0096: 0096-Add-grub-set-bootflag-utility.patch
Patch0097: 0097-docs-Add-grub-boot-indeterminate.service-example.patch
Patch0098: 0098-gentpl-add-disable-support.patch
Patch0099: 0099-gentpl-add-pc-firmware-type.patch
Patch0100: 0100-efinet-also-use-the-firmware-acceleration-for-http.patch
Patch0101: 0101-efi-http-Make-root_url-reflect-the-protocol-hostname.patch
Patch0102: 0102-Make-it-so-we-can-tell-configure-which-cflags-utils-.patch
Patch0103: 0103-module-verifier-make-it-possible-to-run-checkers-on-.patch
Patch0104: 0104-Rework-how-the-fdt-command-builds.patch
Patch0105: 0105-Disable-non-wordsize-allocations-on-arm.patch
Patch0106: 0106-Prepend-prefix-when-HTTP-path-is-relative.patch
Patch0107: 0107-Make-grub_error-more-verbose.patch
Patch0108: 0108-Make-reset-an-alias-for-the-reboot-command.patch
Patch0109: 0109-Add-a-version-command.patch
Patch0110: 0110-Add-more-dprintf-and-nerf-dprintf-in-script.c.patch
Patch0111: 0111-arm-arm64-loader-Better-memory-allocation-and-error-.patch
Patch0112: 0112-Try-to-pick-better-locations-for-kernel-and-initrd.patch
Patch0113: 0113-Attempt-to-fix-up-all-the-places-Wsign-compare-error.patch
Patch0114: 0114-Don-t-use-Wno-sign-compare-Wno-conversion-Wno-error-.patch
Patch0115: 0115-x86-efi-Use-bounce-buffers-for-reading-to-addresses-.patch
Patch0116: 0116-x86-efi-Re-arrange-grub_cmd_linux-a-little-bit.patch
Patch0117: 0117-x86-efi-Make-our-own-allocator-for-kernel-stuff.patch
Patch0118: 0118-x86-efi-Allow-initrd-params-cmdline-allocations-abov.patch
Patch0119: 0119-Fix-getroot.c-s-trampolines.patch
Patch0120: 0120-Do-not-allow-stack-trampolines-anywhere.patch
Patch0121: 0121-Reimplement-boot_counter.patch
Patch0122: 0122-Fix-menu-entry-selection-based-on-ID-and-title.patch
Patch0123: 0123-Make-the-menu-entry-users-option-argument-to-be-opti.patch
Patch0124: 0124-Add-efi-export-env-and-efi-load-env-commands.patch
Patch0125: 0125-Make-it-possible-to-subtract-conditions-from-debug.patch
Patch0126: 0126-Export-all-variables-from-the-initial-context-when-c.patch
Patch0127: 0127-grub.d-Split-out-boot-success-reset-from-menu-auto-h.patch
Patch0128: 0128-Fix-systemctl-kexec-exit-status-check.patch
Patch0129: 0129-Print-grub-emu-linux-loader-messages-as-debug.patch
Patch0130: 0130-Don-t-assume-that-boot-commands-will-only-return-on-.patch
Patch0131: 0131-Fix-undefined-references-for-fdt-when-building-with-.patch
Patch0132: 0132-Do-better-in-bootstrap.conf.patch
Patch0133: 0133-Use-git-to-apply-gnulib-patches.patch
Patch0134: 0134-Fix-build-error-with-the-fdt-module-on-risc-v.patch
Patch0135: 0135-grub-set-bootflag-Update-comment-about-running-as-ro.patch
Patch0136: 0136-grub-set-bootflag-Write-new-env-to-tmpfile-and-then-.patch
Patch0137: 0137-grub.d-Fix-boot_indeterminate-getting-set-on-boot_su.patch
Patch0138: 0138-Also-define-GRUB_EFI_MAX_ALLOCATION_ADDRESS-for-RISC.patch
Patch0139: 0139-chainloader-Define-machine-types-for-RISC-V.patch
Patch0140: 0140-Add-start-symbol-for-RISC-V.patch
Patch0141: 0141-bootstrap.conf-Force-autogen.sh-to-use-python3.patch
Patch0142: 0142-efi-http-Export-fw-http-_path-variables-to-make-them.patch
Patch0143: 0143-efi-http-Enclose-literal-IPv6-addresses-in-square-br.patch
Patch0144: 0144-efi-net-Allow-to-specify-a-port-number-in-addresses.patch
Patch0145: 0145-efi-ip4_config-Improve-check-to-detect-literal-IPv6-.patch
Patch0146: 0146-efi-net-Print-a-debug-message-if-parsing-the-address.patch
Patch0147: 0147-kern-term-Also-accept-F8-as-a-user-interrupt-key.patch
Patch0148: 0148-efi-Set-image-base-address-before-jumping-to-the-PE-.patch
Patch0149: 0149-tpm-Don-t-propagate-TPM-measurement-errors-to-the-ve.patch
Patch0150: 0150-x86-efi-Reduce-maximum-bounce-buffer-size-to-16-MiB.patch
Patch0151: 0151-http-Prepend-prefix-when-the-HTTP-path-is-relative-a.patch
Patch0152: 0152-Fix-a-missing-return-in-efi-export-env-and-efi-load-.patch
Patch0153: 0153-efi-dhcp-fix-some-allocation-error-checking.patch
Patch0154: 0154-efi-http-fix-some-allocation-error-checking.patch
Patch0155: 0155-efi-ip-46-_config.c-fix-some-potential-allocation-ov.patch
Patch0156: 0156-efilinux-Fix-integer-overflows-in-grub_cmd_initrd.patch
Patch0157: 0157-linuxefi-fail-kernel-validation-without-shim-protoco.patch
Patch0158: 0158-Fix-const-char-pointers-in-grub-core-net-bootp.c.patch
Patch0159: 0159-Fix-const-char-pointers-in-grub-core-net-efi-ip4_con.patch
Patch0160: 0160-Fix-const-char-pointers-in-grub-core-net-efi-ip6_con.patch
Patch0161: 0161-Fix-const-char-pointers-in-grub-core-net-efi-net.c.patch
Patch0162: 0162-Fix-const-char-pointers-in-grub-core-net-efi-pxe.c.patch
Patch0163: 0163-Add-systemd-integration-scripts-to-make-systemctl-re.patch
Patch0164: 0164-systemd-integration.sh-Also-set-old-menu_show_once-g.patch
Patch0165: 0165-at_keyboard-use-set-1-when-keyboard-is-in-Translate-.patch
Patch0166: 0166-grub-install-disable-support-for-EFI-platforms.patch
Patch0167: 0167-New-with-debug-timestamps-configure-flag-to-prepend-.patch
Patch0168: 0168-Added-debug-statements-to-grub_disk_open-and-grub_di.patch
Patch0169: 0169-Introduce-function-grub_debug_is_enabled-void-return.patch
Patch0170: 0170-Don-t-clear-screen-when-debugging-is-enabled.patch
Patch0171: 0171-grub_file_-instrumentation-new-file-debug-tag.patch
Patch0172: 0172-ieee1275-Avoiding-many-unecessary-open-close.patch
Patch0173: 0173-ieee1275-powerpc-implements-fibre-channel-discovery-.patch
Patch0174: 0174-ieee1275-powerpc-enables-device-mapper-discovery.patch
Patch0175: 0175-Add-at_keyboard_fallback_set-var-to-force-the-set-ma.patch
Patch0176: 0176-Add-suport-for-signing-grub-with-an-appended-signatu.patch
Patch0177: 0177-docs-grub-Document-signing-grub-under-UEFI.patch
Patch0178: 0178-docs-grub-Document-signing-grub-with-an-appended-sig.patch
Patch0179: 0179-dl-provide-a-fake-grub_dl_set_persistent-for-the-emu.patch
Patch0180: 0180-pgp-factor-out-rsa_pad.patch
Patch0181: 0181-crypto-move-storage-for-grub_crypto_pk_-to-crypto.c.patch
Patch0182: 0182-posix_wrap-tweaks-in-preparation-for-libtasn1.patch
Patch0183: 0183-libtasn1-import-libtasn1-4.16.0.patch
Patch0184: 0184-libtasn1-disable-code-not-needed-in-grub.patch
Patch0185: 0185-libtasn1-changes-for-grub-compatibility.patch
Patch0186: 0186-libtasn1-compile-into-asn1-module.patch
Patch0187: 0187-test_asn1-test-module-for-libtasn1.patch
Patch0188: 0188-grub-install-support-embedding-x509-certificates.patch
Patch0189: 0189-appended-signatures-import-GNUTLS-s-ASN.1-descriptio.patch
Patch0190: 0190-appended-signatures-parse-PKCS-7-signedData-and-X.50.patch
Patch0191: 0191-appended-signatures-support-verifying-appended-signa.patch
Patch0192: 0192-appended-signatures-verification-tests.patch
Patch0193: 0193-appended-signatures-documentation.patch
Patch0194: 0194-ieee1275-enter-lockdown-based-on-ibm-secure-boot.patch
Patch0195: 0195-Revert-templates-Properly-disable-the-os-prober-by-d.patch
Patch0196: 0196-Revert-templates-Disable-the-os-prober-by-default.patch

BuildRequires:  device-mapper-devel
BuildRequires:  systemd-devel
BuildRequires:  xz-devel
BuildRequires:  autoconf
BuildRequires:  python3

Requires:       device-mapper
Requires:       xz

%description
The GRUB package contains the GRand Unified Bootloader.

%ifarch x86_64
%package pc
Summary:        GRUB Library for BIOS
Group:          System Environment/Programming

Requires:       %{name} = %{version}

%description pc
Additional library files for grub
%endif

%package efi
Summary:        GRUB Library for UEFI
Group:          System Environment/Programming

Requires:       %{name} = %{version}

%description efi
Additional library files for grub

%package efi-unsigned
Summary:        Unsigned GRUB UEFI image
Group:          System Environment/Base

%description efi-unsigned
Unsigned GRUB UEFI image

%package efi-binary
Summary:        GRUB UEFI image
Group:          System Environment/Base

%description efi-binary
GRUB UEFI bootloader binaries

%prep
%setup -q -n grub-%{version}-rc1
cp %{SOURCE1} gnulib-%{gnulibversion}.tar.gz
tar -zxf gnulib-%{gnulibversion}.tar.gz
mv gnulib-%{gnulibversion} gnulib

# TODO: Check if I can use autosetup here instead
%patch0001 -p1
%patch0002 -p1
%patch0003 -p1
%patch0004 -p1
%patch0005 -p1
%patch0006 -p1
%patch0007 -p1
%patch0008 -p1
%patch0009 -p1
%patch0010 -p1
%patch0011 -p1
%patch0012 -p1
%patch0013 -p1
%patch0014 -p1
%patch0015 -p1
%patch0016 -p1
%patch0017 -p1
%patch0018 -p1
%patch0019 -p1
%patch0020 -p1
%patch0021 -p1
%patch0022 -p1
%patch0023 -p1
%patch0024 -p1
%patch0025 -p1
%patch0026 -p1
%patch0027 -p1
%patch0028 -p1
%patch0029 -p1
%patch0030 -p1
%patch0031 -p1
%patch0032 -p1
%patch0033 -p1
%patch0034 -p1
%patch0035 -p1
%patch0036 -p1
%patch0037 -p1
%patch0038 -p1
%patch0039 -p1
%patch0040 -p1
%patch0041 -p1
%patch0042 -p1
%patch0043 -p1
%patch0044 -p1
%patch0045 -p1
%patch0046 -p1
%patch0047 -p1
%patch0048 -p1
%patch0049 -p1
%patch0050 -p1
%patch0051 -p1
%patch0052 -p1
%patch0053 -p1
%patch0054 -p1
%patch0055 -p1
%patch0056 -p1
%patch0057 -p1
%patch0058 -p1
%patch0059 -p1
%patch0060 -p1
%patch0061 -p1
%patch0062 -p1
%patch0063 -p1
%patch0064 -p1
%patch0065 -p1
%patch0066 -p1
%patch0067 -p1
%patch0068 -p1
%patch0069 -p1
%patch0070 -p1
%patch0071 -p1
%patch0072 -p1
%patch0073 -p1
%patch0074 -p1
%patch0075 -p1
%patch0076 -p1
%patch0077 -p1
%patch0078 -p1
%patch0079 -p1
%patch0080 -p1
%patch0081 -p1
%patch0082 -p1
%patch0083 -p1
%patch0084 -p1
%patch0085 -p1
%patch0086 -p1
%patch0087 -p1
%patch0088 -p1
%patch0089 -p1
%patch0090 -p1
%patch0091 -p1
%patch0092 -p1
%patch0093 -p1
%patch0094 -p1
%patch0095 -p1
%patch0096 -p1
%patch0097 -p1
%patch0098 -p1
%patch0099 -p1
%patch0100 -p1
%patch0101 -p1
%patch0102 -p1
%patch0103 -p1
%patch0104 -p1
%patch0105 -p1
%patch0106 -p1
%patch0107 -p1
%patch0108 -p1
%patch0109 -p1
%patch0110 -p1
%patch0111 -p1
%patch0112 -p1
%patch0113 -p1
%patch0114 -p1
%patch0115 -p1
%patch0116 -p1
%patch0117 -p1
%patch0118 -p1
%patch0119 -p1
%patch0120 -p1
%patch0121 -p1
%patch0122 -p1
%patch0123 -p1
%patch0124 -p1
%patch0125 -p1
%patch0126 -p1
%patch0127 -p1
%patch0128 -p1
%patch0129 -p1
%patch0130 -p1
%patch0131 -p1
%patch0132 -p1
%patch0133 -p1
%patch0134 -p1
%patch0135 -p1
%patch0136 -p1
%patch0137 -p1
%patch0138 -p1
%patch0139 -p1
%patch0140 -p1
%patch0141 -p1
%patch0142 -p1
%patch0143 -p1
%patch0144 -p1
%patch0145 -p1
%patch0146 -p1
%patch0147 -p1
%patch0148 -p1
%patch0149 -p1
%patch0150 -p1
%patch0151 -p1
%patch0152 -p1
%patch0153 -p1
%patch0154 -p1
%patch0155 -p1
%patch0156 -p1
%patch0157 -p1
%patch0158 -p1
%patch0159 -p1
%patch0160 -p1
%patch0161 -p1
%patch0162 -p1
%patch0163 -p1
%patch0164 -p1
%patch0165 -p1
%patch0166 -p1
%patch0167 -p1
%patch0168 -p1
%patch0169 -p1
%patch0170 -p1
%patch0171 -p1
%patch0172 -p1
%patch0173 -p1
%patch0174 -p1
%patch0175 -p1
%patch0176 -p1
%patch0177 -p1
%patch0178 -p1
%patch0179 -p1
%patch0180 -p1
%patch0181 -p1
%patch0182 -p1
%patch0183 -p1
%patch0184 -p1
%patch0185 -p1
%patch0186 -p1
%patch0187 -p1
%patch0188 -p1
%patch0189 -p1
%patch0190 -p1
%patch0191 -p1
%patch0192 -p1
%patch0193 -p1
%patch0194 -p1
%patch0195 -p1
%patch0196 -p1

# We are using redhat's fork of gnulib which has the grub-core/lib/gnulib-patches
# already applied.
# The repo also hardcodes the redhat hardenening flags so we need to replace
# that pointer with ours
#
# https://github.com/rhboot/gnulib/commit/a2956cf47da2cf331b56ae81e22758bf0a4d6f10
sed -i 's,redhat/redhat-hardened-cc1,mariner/default-hardened-cc1,g' gnulib/gnulib-tool

# Our GCC does not seem to have the gcc annobin plugin. So remove references to
# it from redhat's gnulib.
sed -i 's,-specs=/usr/lib/rpm/redhat/redhat-annobin-cc1,,g' gnulib/gnulib-tool

%build
./bootstrap --no-git --gnulib-srcdir=./gnulib
%ifarch x86_64
mkdir build-for-pc
pushd build-for-pc
# Modify the default CFLAGS to support the i386 build
CFLAGS="`echo " %{build_cflags} "          | \
        sed 's/-fcf-protection//'          | \
        sed 's/-fstack-protector-strong//' | \
        sed 's/-m64//'                     | \
        sed 's/-specs.*cc1//'              | \
        sed 's/-mtune=generic//'           | \
        sed 's/-O. //'                     | \
        sed 's/-fexceptions//'             | \
        sed 's/-Wp,-D_FORTIFY_SOURCE=2//'`"
export CFLAGS

# The patches introduce HOST and TARGET versions of
# the standard CFLAGS/LDFLAGS overrides
HOST_CFLAGS=$CFLAGS
export HOST_CFLAGS
HOST_LDFLAGS=$LDFLAGS
export HOST_LDFLAGS
TARGET_CFLAGS=$CFLAGS
export TARGET_CFLAGS
TARGET_LDFLAGS=$LDFLAGS
export TARGET_LDFLAGS

../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=pc \
    --with-utils=host \
    --target=i386 \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-pc install
popd
%endif

# Disable stack-protector and PIE spec to fix compilation
CFLAGS="`echo " %{build_cflags} "              | \
         sed 's/-specs.*cc1//'                 | \
         sed 's/-fstack-protector-strong//'`"
export CFLAGS

# The patches introduce HOST and TARGET versions of
# the standard CFLAGS/LDFLAGS overrides
HOST_CFLAGS=$CFLAGS
export HOST_CFLAGS
HOST_LDFLAGS=$LDFLAGS
export HOST_LDFLAGS
TARGET_CFLAGS=$CFLAGS
export TARGET_CFLAGS
TARGET_LDFLAGS=$LDFLAGS
export TARGET_LDFLAGS

mkdir build-for-efi
pushd build-for-efi
../configure \
    --prefix=%{_prefix} \
    --sbindir=/sbin \
    --sysconfdir=%{_sysconfdir} \
    --disable-werror \
    --disable-efiemu \
    --with-grubdir=grub2 \
    --with-platform=efi \
    --with-utils=host \
    --target=%{_arch} \
    --program-transform-name=s,grub,%{name}, \
    --with-bootdir="/boot"
make %{?_smp_mflags}
make DESTDIR=$PWD/../install-for-efi install
popd

#make sure all the files are same between two configure except the /usr/lib/grub
%check
%ifarch x86_64
# Note: bin & sbin binaries are expected to differ due to different CFLAGS
# Just compare files under _sysconfdir and _datarootdir
diff -sr install-for-efi%{_sysconfdir} install-for-pc%{_sysconfdir}
diff -sr install-for-efi%{_datarootdir} install-for-pc%{_datarootdir}
%endif

%install
mkdir -p %{buildroot}
cp -a install-for-efi/. %{buildroot}/.
%ifarch x86_64
cp -a install-for-pc/. %{buildroot}/.
%endif
mkdir %{buildroot}%{_sysconfdir}/default
touch %{buildroot}%{_sysconfdir}/default/grub
mkdir %{buildroot}%{_sysconfdir}/sysconfig
ln -sf %{_sysconfdir}/default/grub %{buildroot}%{_sysconfdir}/sysconfig/grub
install -vdm 700 %{buildroot}/boot/%{name}
touch %{buildroot}/boot/%{name}/grub.cfg
chmod 600 %{buildroot}/boot/%{name}/grub.cfg
rm -rf %{buildroot}%{_infodir}

# Add SBAT
sed -e "s,@@VERSION@@,%{version}-%{release},g" %{SOURCE2} > ./sbat.csv
cat ./sbat.csv

# Generate grub efi image
install -d %{buildroot}%{_datadir}/grub2-efi
%ifarch x86_64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/x86_64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubx64.efi -p /boot/grub2 -O x86_64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop efi_uga ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512 tpm
%endif
%ifarch aarch64
./install-for-efi/usr/bin/grub2-mkimage -d ./install-for-efi/usr/lib/grub/arm64-efi/ --sbat ./sbat.csv -o %{buildroot}%{_datadir}/grub2-efi/grubaa64.efi -p /boot/grub2 -O arm64-efi fat iso9660 part_gpt part_msdos normal boot linux configfile loopback chain efifwsetup efi_gop ls search search_label search_fs_uuid search_fs_file gfxterm gfxterm_background gfxterm_menu test all_video loadenv exfat ext2 udf halt gfxmenu png tga lsefi help probe echo lvm cryptodisk luks gcry_rijndael gcry_sha512 tpm
%endif

# Install to efi directory
EFI_BOOT_DIR=%{buildroot}/boot/efi/EFI/BOOT
GRUB_MODULE_NAME=
GRUB_MODULE_SOURCE=

install -d $EFI_BOOT_DIR

%ifarch x86_64
GRUB_MODULE_NAME=grubx64.efi
GRUB_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubx64.efi
%endif

%ifarch aarch64
GRUB_MODULE_NAME=grubaa64.efi
GRUB_MODULE_SOURCE=%{buildroot}%{_datadir}/grub2-efi/grubaa64.efi
%endif

cp $GRUB_MODULE_SOURCE $EFI_BOOT_DIR/$GRUB_MODULE_NAME

%post   -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%license COPYING
%dir %{_sysconfdir}/grub.d
%dir /boot/%{name}
%config() %{_datadir}/bash-completion/completions/*
%config() %{_sysconfdir}/grub.d/00_header
%config() %{_sysconfdir}/grub.d/01_users
%config() %{_sysconfdir}/grub.d/08_fallback_counting
%config() %{_sysconfdir}/grub.d/10_linux
%config() %{_sysconfdir}/grub.d/10_reset_boot_success
%config() %{_sysconfdir}/grub.d/12_menu_auto_hide
%config() %{_sysconfdir}/grub.d/14_menu_show_once
%config() %{_sysconfdir}/grub.d/20_linux_xen
%config() %{_sysconfdir}/grub.d/20_ppc_terminfo
%config() %{_sysconfdir}/grub.d/30_os-prober
%config() %{_sysconfdir}/grub.d/30_uefi-firmware
%config(noreplace) %{_sysconfdir}/grub.d/40_custom
%config(noreplace) %{_sysconfdir}/grub.d/41_custom
%{_sysconfdir}/grub.d/README
/sbin/*
%{_bindir}/*
%{_datarootdir}/grub/*
%{_sysconfdir}/sysconfig/grub
%{_sysconfdir}/default/grub
%ghost %config(noreplace) /boot/%{name}/grub.cfg
%{_libdir}/systemd/system/grub2-systemd-integration.service
%{_libdir}/systemd/system/systemd-logind.service.d/10-grub2-logind-service.conf
%{_libexecdir}/grub2/systemd-integration.sh

%ifarch x86_64
%files pc
%{_libdir}/grub/i386-pc

%files efi
%{_libdir}/grub/x86_64-efi
%endif

%files efi-unsigned
%{_datadir}/grub2-efi/*

%files efi-binary
%ifarch x86_64
/boot/efi/EFI/BOOT/grubx64.efi
%endif
%ifarch aarch64
/boot/efi/EFI/BOOT/grubaa64.efi
%endif

%ifarch aarch64
%files efi
%{_libdir}/grub/*
%endif

%changelog
* Wed Mar 10 2021 Chris Co <chrco@microsoft.com> - 2.06-1
- Update to 2.06-rc1. Remove old out-of-tree patches. Add patches from F34
- Incorporate SBAT data
- Remove grub2-lang (locale) subpackage
- Enable tpm module to EFI binary

* Mon Dec 14 2020 Andrew Phelps <anphel@microsoft.com> - 2.02-26
- Modify check test

* Fri Oct 30 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 2.02-25
- Fix CVE-2020-15705 (BootHole cont.).

* Thu Aug 13 2020 Chris Co <chrco@microsoft.com> - 2.02-24
- Remove signed subpackage and macro

* Thu Jul 30 2020 Chris Co <chrco@microsoft.com> - 2.02-23
- Fix CVE-2020-10713 (BootHole)
- Fix CVE-2020-14308
- Fix CVE-2020-14309
- Fix CVE-2020-14310
- Fix CVE-2020-14311
- Fix CVE-2020-15706
- Fix CVE-2020-15707

* Wed Jul 22 2020 Joe Schmitt <joschmit@microsoft.com> - 2.02-22
- Always include Patch100, but conditionally apply it.
- Switch URL to https.

* Tue Jun 30 2020 Nicolas Ontiveros <niontive@microsoft.com> - 2.02-21
- Add cryptodisk, luks, gcry_rijndael and gcry_sha512 modules to EFI files.

* Fri Jun 19 2020 Chris Co <chrco@microsoft.com> - 2.02-20
- Add grub2-efi-binary subpackage
- Add grub2-efi-binary-signed subpackage and macros for adding offline signed grub binaries

* Mon Jun 01 2020 Henry Beberman <henry.beberman@microsoft.com> - 2.02-19
- Address compilation errors from hardened cflags.

* Tue May 26 2020 Emre Girgin <mrgirgin@microsoft.com> - 2.02-18
- Change /boot directory permissions to 600.

* Fri May 22 2020 Chris Co <chrco@microsoft.com> - 2.02-17
- Create grubaa64.efi as part of the grub2-efi-unsigned subpackage

* Wed May 13 2020 Nick Samson <nisamson@microsoft.com> - 2.02-16
- Added %%license line automatically

* Mon May 11 2020 Chris Co <chrco@microsoft.com> - 2.02-15
- Create new grub2-efi-unsigned subpackage containing grubx64.efi

* Thu Apr 30 2020 Chris Co <chrco@microsoft.com> - 2.02-14
- Add fdt rework patch to fix aarch64 build errors
- Enable aarch64 build

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 2.02-13
- Initial CBL-Mariner import from Photon (license: Apache2).

* Thu Feb 21 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.02-12
- Update grub version from ~rc3 to release.
- Enhance SB + TPM support (19 patches from grub2-2.02-70.fc30)
- Remove i386-pc modules from grub2-efi

* Fri Jan 25 2019 Alexey Makhalov <amakhalov@vmware.com> - 2.02-11
- Disable efinet for aarch64 to workwround NXP ls1012a frwy PFE bug.

* Tue Nov 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.02-10
- Aarch64 support

* Fri Jun 2  2017 Bo Gan <ganb@vmware.com> - 2.02-9
- Split grub2 to grub2 and grub2-pc, remove grub2-efi spec

* Fri Apr 14 2017 Alexey Makhalov <amakhalov@vmware.com> - 2.02-8
- Version update to 2.02~rc2

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 2.02-7
- Add fix for CVE-2015-8370

* Fri Nov 18 2016 Anish Swaminathan <anishs@vmware.com> - 2.02-6
- Change systemd dependency

* Thu Oct 06 2016 ChangLee <changlee@vmware.com> - 2.02-5
- Modified %check

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 2.02-4
- GA - Bump release of all rpms

* Fri Oct 02 2015 Divya Thaluru <dthaluru@vmware.com> - 2.02-3
- Adding patch to boot entries with out password.

* Wed Jul 22 2015 Divya Thaluru <dthaluru@vmware.com> - 2.02-2
- Changing program name from grub to grub2.

* Mon Jun 29 2015 Divya Thaluru <dthaluru@vmware.com> - 2.02-1
- Updating grub to 2.02

* Wed Nov 5 2014 Divya Thaluru <dthaluru@vmware.com> - 2.00-1
- Initial build.  First version
