# Verifying pre-built ISO image

| Release Branch | ISO Image | SHA-256 Checksum File | Checksum Signature |
| -------------- | --------- | --------------------- | ------------------ |
| 1.0            | <https://aka.ms/mariner-1.0-x86_64-iso> | <https://aka.ms/mariner-1.0-x86_64-iso-checksum> | <https://aka.ms/mariner-1.0-x86_64-iso-checksum-signature> |
| 2.0            | <https://aka.ms/mariner-2.0-x86_64-iso> | <https://aka.ms/mariner-2.0-x86_64-iso-checksum> | <https://aka.ms/mariner-2.0-x86_64-iso-checksum-signature> |

Once the ISO image, the checksum, and the checksum signature files are downloaded, it is strongly recommended that the integrity of the image is verified. This is a two-step process. First, ensure that the checksum file has not been tampered with by verifying the signature against Mariner's RPM signing public key. Second, check that the ISO image was not corrupted during the download. The following bash script shows the commands necessary to check both steps:

```bash
# Assumption: we are in the directory containing the downloaded files
# Replace "1.0" in these variables with the release branch being verified
CHECKSUM_FILE="mariner-1.0-x86_64.iso.sha256"
SIGNATURE_FILE="mariner-1.0-x86_64.iso.sha256.gpg"

# Download the Mariner RPM signing public key
wget https://raw.githubusercontent.com/microsoft/CBL-Mariner/2.0/SPECS/mariner-repos/MICROSOFT-RPM-GPG-KEY

# Import the RPM signing public key into the local GPG keystore
gpg --import MICROSOFT-RPM-GPG-KEY

# Verify that the checksum file was produced by the Mariner team
# The output of this command should contain the following string:
# 'Good signature from "Mariner RPM Release Signing <marinerrpmprod@microsoft.com>"'
gpg --verify "$SIGNATURE_FILE" "$CHECKSUM_FILE"

# Verify that the ISO image checksum matches the expected checksum
# We need to fix the line endings on the signature file to get sha256sum to accept it
dos2unix "$SIGNATURE_FILE"
sha256sum --check "$CHECKSUM_FILE"
```
