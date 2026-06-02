# Verifying Pre-Built ISO Image
It is strongly recommended that the integrity of the image is verified after downloading it. This is a two-step process:
1. Ensure that the checksum file has not been tampered with by verifying the signature against Azure Linux's RPM signing public key.
1. Check that the ISO image was not corrupted during the download.

The following bash script shows the commands necessary to download the iso image and check the signature:

## x86_64 ISO Verification
```bash
# Download the necessary files
wget https://aka.ms/azurelinux-4.0-x86_64.iso -O AzureLinux-4.0-x86_64.iso
wget https://aka.ms/azurelinux-4.0-x86_64-iso-checksum
wget https://aka.ms/azurelinux-4.0-x86_64-iso-checksum-signature
wget https://raw.githubusercontent.com/microsoft/azurelinux/refs/heads/4.0/base/comps/azurelinux-repos/RPM-GPG-KEY-azurelinux-4.0-primary

# Set Variables for the checksum and signature file names
CHECKSUM_FILE="azurelinux-4.0-x86_64-iso-checksum"
SIGNATURE_FILE="azurelinux-4.0-x86_64-iso-checksum-signature"

# Import the RPM signing public key into the local GPG keystore
gpg --import RPM-GPG-KEY-azurelinux-4.0-primary

# Verify that the checksum file was produced by the Azure Linux team
# The output of this command should contain the following string:
# 'Good signature from "Mariner RPM Release Signing <marinerrpmprod@microsoft.com>"'
gpg --verify "$SIGNATURE_FILE" "$CHECKSUM_FILE"

# Verify that the ISO image checksum matches the expected checksum
# We need to fix the line endings on the signature file to get sha256sum to accept it
tr -d '\r' < "$CHECKSUM_FILE" | sha256sum --check -
```

## aarch64 ISO Verification
```bash
# Download the necessary files
wget https://aka.ms/azurelinux-4.0-aarch64.iso -O AzureLinux-4.0-aarch64.iso
wget https://aka.ms/azurelinux-4.0-aarch64-iso-checksum
wget https://aka.ms/azurelinux-4.0-aarch64-iso-checksum-signature
wget https://raw.githubusercontent.com/microsoft/azurelinux/refs/heads/4.0/base/comps/azurelinux-repos/RPM-GPG-KEY-azurelinux-4.0-primary

# Set Variables for the checksum and signature file names
CHECKSUM_FILE="azurelinux-4.0-aarch64-iso-checksum"
SIGNATURE_FILE="azurelinux-4.0-aarch64-iso-checksum-signature"

# Import the RPM signing public key into the local GPG keystore
gpg --import RPM-GPG-KEY-azurelinux-4.0-primary

# Verify that the checksum file was produced by the Azure Linux team
# The output of this command should contain the following string:
# 'Good signature from "Mariner RPM Release Signing <marinerrpmprod@microsoft.com>"'
gpg --verify "$SIGNATURE_FILE" "$CHECKSUM_FILE"

# Verify that the ISO image checksum matches the expected checksum
# We need to fix the line endings on the signature file to get sha256sum to accept it
tr -d '\r' < "$CHECKSUM_FILE" | sha256sum --check -
```
