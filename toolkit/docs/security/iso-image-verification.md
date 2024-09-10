# Verifying pre-built ISO image

It is strongly recommended that the integrity of the image is verified after downloading it. This is a two-step process. First, ensure that the checksum file has not been tampered with by verifying the signature against Azure Linux's RPM signing public key. Second, check that the ISO image was not corrupted during the download. The following bash script shows the commands necessary to download the iso image and check the signature:

```bash
# Download the necessary files
wget https://aka.ms/AzureLinux-3.0-x86_64.iso
wget https://aka.ms/azurelinux-3.0-x86_64-iso-checksum
wget https://aka.ms/azurelinux-3.0-x86_64-iso-checksum-signature
wget https://raw.githubusercontent.com/microsoft/azurelinux/3.0/SPECS/azurelinux-repos/MICROSOFT-RPM-GPG-KEY

# Set Variables for the checksum and signature file names
CHECKSUM_FILE="azurelinux-3.0-x86_64-iso-checksum"
SIGNATURE_FILE="azurelinux-3.0-x86_64-iso-checksum-signature"

# Import the RPM signing public key into the local GPG keystore
gpg --import MICROSOFT-RPM-GPG-KEY

# Verify that the checksum file was produced by the Azure Linux team
# The output of this command should contain the following string:
# 'Good signature from "Azure Linux RPM Release Signing <marinerrpmprod@microsoft.com>"'
gpg --verify "$SIGNATURE_FILE" "$CHECKSUM_FILE"

# Verify that the ISO image checksum matches the expected checksum
# We need to fix the line endings on the signature file to get sha256sum to accept it
dos2unix "$CHECKSUM_FILE"
sha256sum --check "$CHECKSUM_FILE"
```
