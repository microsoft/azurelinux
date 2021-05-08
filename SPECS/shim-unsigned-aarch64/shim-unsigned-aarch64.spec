%global debug_package %{nil}
Summary:        First stage UEFI bootloader
Name:           shim-unsigned-aarch64
Version:        15
Release:        5%{?dist}
URL:            https://github.com/rhboot/shim
License:        BSD
Vendor:         Microsoft
Distribution:   Mariner
Source0:        https://github.com/rhboot/shim/releases/download/15/shim-%{version}.tar.bz2
Source1:        cbl-mariner-ca-20210127.der
ExclusiveArch:  aarch64

BuildRequires:  gnu-efi
BuildRequires:  gnu-efi-devel

Patch0001: 0001-Make-some-things-dprint-instead-of-console_print.patch
Patch0002: 0002-Makefiles-ensure-m32-gets-propogated-to-our-gcc-para.patch
Patch0003: 0003-Let-MokManager-follow-a-MokTimeout-var-for-timeout-l.patch
Patch0004: 0004-httpboot-return-EFI_NOT_FOUND-when-it-fails-to-find-.patch
Patch0005: 0005-httpboot-print-more-messages-when-it-fails-to-set-IP.patch
Patch0006: 0006-httpboot-allow-the-IPv4-gateway-to-be-empty.patch
Patch0007: 0007-httpboot-show-the-error-message-for-the-ChildHandle.patch
Patch0008: 0008-Fix-typo-in-debug-path-in-shim.h.patch
Patch0009: 0009-MokManager-Stop-using-EFI_VARIABLE_APPEND_WRITE.patch
Patch0010: 0010-shim-Extend-invalid-reloc-size-warning-message.patch
Patch0011: 0011-Add-GRUB-s-PCR-Usage-to-README.tpm.patch
Patch0012: 0012-Fix-the-compile-error-of-mkdir-wrong-directory.patch
Patch0013: 0013-shim-Properly-generate-absolute-paths-from-relative-.patch
Patch0014: 0014-shim-Prevent-shim-to-set-itself-as-a-second-stage-lo.patch
Patch0015: 0015-Fix-for-Section-0-has-negative-size-error-when-loadi.patch
Patch0016: 0016-Fix-apparent-typo-in-ARM-32-on-64-code.patch
Patch0017: 0017-Makefile-do-not-run-git-on-clean-if-there-s-no-.git-.patch
Patch0018: 0018-Make.default-use-correct-flags-to-disable-unaligned-.patch
Patch0019: 0019-Cryptlib-fix-build-on-32bit-ARM.patch
Patch0020: 0020-Make-sure-that-MOK-variables-always-get-mirrored.patch
Patch0021: 0021-mok-fix-the-mirroring-of-RT-variables.patch
Patch0022: 0022-mok-consolidate-mirroring-code-in-a-helper-instead-o.patch
Patch0023: 0023-shim-only-include-shim_cert.h-in-shim.c.patch
Patch0024: 0024-mok-also-mirror-the-build-cert-to-MokListRT.patch
Patch0025: 0025-mok-minor-cleanups.patch
Patch0026: 0026-Remove-call-to-TPM2-get_event_log.patch
Patch0027: 0027-Make-EFI-variable-copying-fatal-only-on-secureboot-e.patch
Patch0028: 0028-VLogError-Avoid-NULL-pointer-dereferences-in-V-Sprin.patch
Patch0029: 0029-Once-again-try-even-harder-to-get-binaries-without-t.patch
Patch0030: 0030-shim-Rework-pause-functions-and-add-read_counter.patch
Patch0031: 0031-Hook-exit-when-shim_lock-protocol-installed.patch
Patch0032: 0032-Work-around-stuff-Waddress-of-packed-member-finds.patch
Patch0033: 0033-Fix-a-use-of-strlen-instead-of-Strlen.patch
Patch0034: 0034-MokManager-Use-CompareMem-on-MokListNode.Type-instea.patch
Patch0035: 0035-OpenSSL-always-provide-OBJ_create-with-name-strings.patch
Patch0036: 0036-Use-portable-shebangs-bin-bash-usr-bin-env-bash.patch
Patch0037: 0037-tpm-Fix-off-by-one-error-when-calculating-event-size.patch
Patch0038: 0038-tpm-Define-EFI_VARIABLE_DATA_TREE-as-packed.patch
Patch0039: 0039-MokManager-console-mode-modification-for-hi-dpi-scre.patch
Patch0040: 0040-MokManager-avoid-Werror-address-of-packed-member.patch
Patch0041: 0041-tpm-Don-t-log-duplicate-identical-events.patch
Patch0042: 0042-Slightly-better-debugging-messages.patch
Patch0043: 0043-Actually-check-for-errors-from-set_second_stage.patch
Patch0044: 0044-translate_slashes-don-t-write-to-string-literals.patch
Patch0045: 0045-shim-Update-EFI_LOADED_IMAGE-with-the-second-stage-l.patch
Patch0046: 0046-tpm-Include-information-about-PE-COFF-images-in-the-.patch
Patch0047: 0047-Fix-the-license-on-our-buildid-extractor.patch
Patch0048: 0048-Update-README.tpm.patch
Patch0049: 0049-Check-PxeReplyReceived-as-fallback-in-netboot.patch
Patch0050: 0050-Remove-a-couple-of-incorrect-license-claims.patch
Patch0051: 0051-MokManager-fix-uninitialized-value.patch
Patch0052: 0052-Fix-some-volatile-usage-gcc-whines-about.patch
Patch0053: 0053-MokManager-fix-a-wrong-allocation-failure-check.patch
Patch0054: 0054-simple_file-fix-uninitialized-variable-unchecked-ret.patch
Patch0055: 0055-Fix-a-broken-tpm-type.patch
Patch0056: 0056-Make-cert.S-not-impossible-to-read.patch
Patch0057: 0057-Add-support-for-vendor_db-built-in-shim-authorized-l.patch
Patch0058: 0058-Handle-binaries-with-multiple-signatures.patch
Patch0059: 0059-Make-openssl-accept-the-right-set-of-KU-EKUs.patch
Patch0060: 0060-Improve-debug-output-some.patch
Patch0061: 0061-Also-use-a-config-table-to-mirror-mok-variables.patch
Patch0062: 0062-Implement-lennysz-s-suggestions-for-MokListRT.patch
Patch0063: 0063-hexdump.h-fix-arithmetic-error.patch

%description
shim is a trivial EFI application that, when run, attempts to open and
execute another application.
On systems with a TPM chip enabled and supported by the system firmware,
shim will extend various PCRs with the digests of the targets it is
loading.

%prep
%autosetup -n shim-%{version} -p1

%build
cp %{SOURCE1} cert.der
make shimaa64.efi VENDOR_CERT_FILE=cert.der EFI_PATH=/usr/lib/gnuefi

%install
install -vdm 755 %{buildroot}/usr/share/%{name}
install -vm 644 shimaa64.efi %{buildroot}/usr/share/%{name}/shimaa64.efi

%files
%defattr(-,root,root)
%license COPYRIGHT
/usr/share/%{name}/shimaa64.efi

%changelog
* Fri Apr 23 2021 Chris Co <chrco@microsoft.com> 15-5
- Update cert
* Tue Aug 25 2020 Chris Co <chrco@microsoft.com> 15-4
- Apply patch files (from CentOS: shim-15-8.el7)
* Thu Jul 30 2020 Chris Co <chrco@microsoft.com> 15-3
- Update binary path
* Wed Jul 29 2020 Chris Co <chrco@microsoft.com> 15-2
- Update built-in cert
* Wed Jun 24 2020 Chris Co <chrco@microsoft.com> 15-1
- Original version for CBL-Mariner.