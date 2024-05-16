#
# This generates a shim-%%{efiarch} package which takes all the
# already-signed EFI binaries as source, and packages them into the
# proper locations under /boot. The shim EFI binary must be externally
# reviewed and approved (by https://github.com/rhboot/shim-review) and
# will then be externally signed. The fallback (fb) and mokmanager
# (mm) EFI binaries should be signed by the production build pipeline.
# This package does *not* sign anything.
#
# To test secure boot after making changes to this, or the
# shim-unsigned package, see the TESTING file.
#

%global debug_package %{nil}

%ifarch x86_64
%global efiarch x64
# We can't use %%{upper:...} until we get to rpm 4.19...
%global EFIARCH X64
%endif
%ifarch aarch64
%global efiarch aa64
%global EFIARCH AA64
%endif

# From shim-unsigned-%%{efiarch}
%global efidir azurelinux
%global shimrootdir %{_datadir}/shim/
%global shimversiondir %{shimrootdir}/%{version}
%global shimdir %{shimversiondir}/%{efiarch}

Summary:        First stage UEFI bootloader
Name:           shim-%{efiarch}
Version:        15.8
Release:        3%{?dist}
License:        BSD
Vendor:         Microsoft Corporation
Distribution:   Azure Linux
URL:            https://github.com/rhboot/shim

ExclusiveArch:  x86_64 aarch64

Provides:       shim = %{version}-%{release}
Obsoletes:      shim < %{version}-%{release}
Provides:       shim-signed = %{version}-%{release}
Provides:       shim-signed-%{efiarch} = %{version}-%{release}

# This is when grub was updated to use our %%{efidir} instead of BOOT
Conflicts:      grub2-efi-binary < 2.06-19

BuildRequires:  shim-unsigned-%{efiarch} = %{version}-%{release}
BuildRequires:  binutils
BuildRequires:  coreutils
BuildRequires:  efivar
BuildRequires:  openssl
BuildRequires:  pesign
BuildRequires:  util-linux

# This is the signed shim which has been reviewed upstream by
# https://github.com/rhboot/shim-review and then signed by the
# Microsoft UEFI signing key
Source0:        shim%{efiarch}.efi

# These are are FallBack and MokManager EFI binaries that have been
# signed by the Azure Linux signing cert. If these files are empty
# (the default), this build will use the unsigned binaries from the
# shim-unsigned package. If these files are not empty, they will be
# used instead. The production signing pipeline should replace the
# empty default files with the signed files for production runs.
Source1:        fb%{efiarch}.efi
Source2:        mm%{efiarch}.efi

%description
Initial UEFI bootloader that handles chaining to a trusted full bootloader
under secure boot environments. This package contains the shim EFI image
signed for secure boot. The package is specifically created for installing
on %{_arch} systems.

%prep
%setup -c -T
cp %{sources} .

# By default, mm/fb are empty, in which case we will use the unsigned
# binary from the shim-unsigned package. We do not actually check if
# the file is signed here; that will be verified in %%check.
for f in mm fb; do
    efi=${f}%{efiarch}.efi
    if [[ -s $efi ]]; then
        echo "Using signed $efi"
        touch ${f}-is-signed
    else
        echo "Using unsigned $efi"
        cp -vf %{shimdir}/$efi .
    fi
done

%build
echo "%{name}" > dnf-protected.conf

# ADD UCS-2/UTF-16 LE Byte Order Mark (BOM)
echo -ne '\xff\xfe' | cat - %{shimdir}/BOOT%{EFIARCH}.CSV > BOOT%{EFIARCH}.CSV

%install
install -D dnf-protected.conf %{buildroot}%{_sysconfdir}/dnf/protected.d/%{name}.conf

install -D shim%{efiarch}.efi %{buildroot}/boot/efi/EFI/BOOT/boot%{efiarch}.efi
install -D fb%{efiarch}.efi -t %{buildroot}/boot/efi/EFI/BOOT

install -D shim%{efiarch}.efi -t %{buildroot}/boot/efi/EFI/%{efidir}
install -D mm%{efiarch}.efi -t %{buildroot}/boot/efi/EFI/%{efidir}
install -D BOOT%{EFIARCH}.CSV -t %{buildroot}/boot/efi/EFI/%{efidir}

%check
HASH=$(cat %{shimdir}/shim%{efiarch}.hash | cut -d ' ' -f 1)
# Verify the original unsigned shim hash matches what was calculated
# during shim-unsigned build (this is also done by shim-unsigned)
[[ $HASH = $(pesign -h -i %{shimdir}/shim%{efiarch}.efi | cut -d ' ' -f 1) ]]
# Verify the signed shim hash also matches
[[ $HASH = $(pesign -h -i %{buildroot}/boot/efi/EFI/BOOT/boot%{efiarch}.efi | cut -d ' ' -f 1) ]]
[[ $HASH = $(pesign -h -i %{buildroot}/boot/efi/EFI/%{efidir}/shim%{efiarch}.efi | cut -d ' ' -f 1) ]]

# Verify the unsigned and signed mm hashes match
[[ $(pesign -h -i %{shimdir}/mm%{efiarch}.efi | cut -d ' ' -f 1) = $(pesign -h -i %{buildroot}/boot/efi/EFI/%{efidir}/mm%{efiarch}.efi | cut -d ' ' -f 1) ]]

# Verify the unsigned and signed fb hashes match
[[ $(pesign -h -i %{shimdir}/fb%{efiarch}.efi | cut -d ' ' -f 1) = $(pesign -h -i %{buildroot}/boot/efi/EFI/BOOT/fb%{efiarch}.efi | cut -d ' ' -f 1) ]]

objcopy -O binary -j .vendor_cert %{buildroot}/boot/efi/EFI/BOOT/boot%{efiarch}.efi cert.table

# There should *REALLY* be an easier tool to extract the cert(s) from
# the raw section content. Until that tool exists (and/or we find out
# about it), the format of the .vendor_cert section is (from shim
# source cert.S file):
#   (4 bytes):             size of DB
#   (4 bytes):             size of DBX
#   (4 bytes):             offset into this table to DB
#   (4 bytes):             offset into this table to DBX
#   ("size of DB" bytes):  DB
#   ("size of DBX" bytes): DBX
DB_SIZE=$(($(hexdump    -s 0  -n 4 -e '"0x%04x"' cert.table)))
DBX_SIZE=$(($(hexdump   -s 4  -n 4 -e '"0x%04x"' cert.table)))
DB_OFFSET=$(($(hexdump  -s 8  -n 4 -e '"0x%04x"' cert.table)))
DBX_OFFSET=$(($(hexdump -s 12 -n 4 -e '"0x%04x"' cert.table)))

# We *must* have something for the DB, but the DBX is optional
[[ $DB_SIZE > 0 ]]

dd if=cert.table bs=1 skip=$DB_OFFSET count=$DB_SIZE of=db.esl
dd if=cert.table bs=1 skip=$DBX_OFFSET count=$DBX_SIZE of=dbx.esl

PESIGCHECK_PARAMS="-n 0"

# The DB can be in the format of an "EFI signature list" (ESL) or can
# be a single x509 certificate. The DBX is (currently) always a ESL.
if openssl x509 -in db.esl -noout 2> /dev/null; then
    PESIGCHECK_PARAMS="$PESIGCHECK_PARAMS -c db.esl"
elif efisecdb -i db.esl --dump > /dev/null; then
    PESIGCHECK_PARAMS="$PESIGCHECK_PARAMS -D db.esl"
else
    echo "Shim vendor_cert section contains unknown cert/list"
    false
fi

if [[ $DBX_SIZE != 0 ]]; then
    PESIGCHECK_PARAMS="$PESIGCHECK_PARAMS -X dbx.esl"
fi

# Verify the signatures of the FallBack and MokManager EFI binaries.
[ -e fb-is-signed ] && pesigcheck $PESIGCHECK_PARAMS -i %{buildroot}/boot/efi/EFI/BOOT/fb%{efiarch}.efi
[ -e mm-is-signed ] && pesigcheck $PESIGCHECK_PARAMS -i %{buildroot}/boot/efi/EFI/%{efidir}/mm%{efiarch}.efi

%files
%defattr(-,root,root)
%{_sysconfdir}/dnf/protected.d/%{name}.conf
/boot/efi/EFI/BOOT/*
/boot/efi/EFI/%{efidir}/*

%changelog
* Wed Mar 13 2024 Dan Streetman <ddstreet@microsoft.com> - 15.8-1
- update to 15.8
- include mm and fb
- protect from dnf removal

* Tue Feb 08 2022 Chris Co <chrco@microsoft.com> - 15.4-2
- Update signed shim binary to newer one associated with 15.4-2 unsigned build.
- License verified

* Fri Apr 16 2021 Chris Co <chrco@microsoft.com> - 15.4-1
- Original version for CBL-Mariner.
