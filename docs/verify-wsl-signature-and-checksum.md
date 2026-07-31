# Verifying Pre-Built WSL Distribution Package
It is strongly recommended that the integrity of the `.wsl` distribution package is verified after downloading it. This is a two-step process:
1. Ensure that the checksum file has not been tampered with by verifying the signature against Azure Linux's RPM signing public key.
1. Check that the `.wsl` package was not corrupted during the download.

The following bash script shows the commands necessary to download the `.wsl` package and check the signature. Run these on any Linux machine, or from inside an existing WSL distribution, before installing the package with `wsl --install --from-file`.

## x86_64 WSL Package Verification
```bash
# Download the necessary files
# The -O flag is required: the checksum file records the package as
# 'AzureLinux-4.0-x86_64.wsl', so the saved file name has to match exactly
wget https://aka.ms/azurelinux-4.0-x86_64.wsl -O AzureLinux-4.0-x86_64.wsl
wget https://aka.ms/azurelinux-4.0-x86_64-wsl-checksum
wget https://aka.ms/azurelinux-4.0-x86_64-wsl-checksum-signature
wget https://raw.githubusercontent.com/microsoft/azurelinux/refs/heads/4.0/base/comps/azurelinux-repos/RPM-GPG-KEY-azurelinux-4.0-primary

# Set Variables for the checksum and signature file names
CHECKSUM_FILE="azurelinux-4.0-x86_64-wsl-checksum"
SIGNATURE_FILE="azurelinux-4.0-x86_64-wsl-checksum-signature"

# Import the RPM signing public key into the local GPG keystore
gpg --import RPM-GPG-KEY-azurelinux-4.0-primary

# Verify that the checksum file was produced by the Azure Linux team
# The output of this command should contain the following string:
# 'Good signature from "Mariner RPM Release Signing <marinerrpmprod@microsoft.com>"'
gpg --verify "$SIGNATURE_FILE" "$CHECKSUM_FILE"

# Verify that the .wsl package checksum matches the expected checksum
# We need to fix the line endings on the checksum file to get sha256sum to accept it
tr -d '\r' < "$CHECKSUM_FILE" | sha256sum --check -
```

## aarch64 WSL Package Verification
```bash
# Download the necessary files
# The -O flag is required: the checksum file records the package as
# 'AzureLinux-4.0-aarch64.wsl', so the saved file name has to match exactly
wget https://aka.ms/azurelinux-4.0-aarch64.wsl -O AzureLinux-4.0-aarch64.wsl
wget https://aka.ms/azurelinux-4.0-aarch64-wsl-checksum
wget https://aka.ms/azurelinux-4.0-aarch64-wsl-checksum-signature
wget https://raw.githubusercontent.com/microsoft/azurelinux/refs/heads/4.0/base/comps/azurelinux-repos/RPM-GPG-KEY-azurelinux-4.0-primary

# Set Variables for the checksum and signature file names
CHECKSUM_FILE="azurelinux-4.0-aarch64-wsl-checksum"
SIGNATURE_FILE="azurelinux-4.0-aarch64-wsl-checksum-signature"

# Import the RPM signing public key into the local GPG keystore
gpg --import RPM-GPG-KEY-azurelinux-4.0-primary

# Verify that the checksum file was produced by the Azure Linux team
# The output of this command should contain the following string:
# 'Good signature from "Mariner RPM Release Signing <marinerrpmprod@microsoft.com>"'
gpg --verify "$SIGNATURE_FILE" "$CHECKSUM_FILE"

# Verify that the .wsl package checksum matches the expected checksum
# We need to fix the line endings on the checksum file to get sha256sum to accept it
tr -d '\r' < "$CHECKSUM_FILE" | sha256sum --check -
```

## Verifying on Windows
If you downloaded the package with a browser on Windows and do not have a WSL distribution available yet, PowerShell can perform the checksum comparison. Note that this only covers step 2 — verifying the signature on the checksum file still requires `gpg`.

```powershell
# Set this to the architecture you downloaded: 'x86_64' or 'aarch64'
$Arch = "x86_64"

$Package = "AzureLinux-4.0-$Arch.wsl"
$ChecksumFile = "azurelinux-4.0-$Arch-wsl-checksum"

# Download the published checksum for the .wsl package
Invoke-WebRequest -Uri "https://aka.ms/$ChecksumFile" -OutFile $ChecksumFile

# Compare the hash of the downloaded package against the published checksum
$expected = ((Get-Content $ChecksumFile -Raw).Trim() -split '\s+')[0]
$actual = (Get-FileHash -Algorithm SHA256 $Package).Hash
if ($actual -eq $expected.ToUpper()) { "Checksum OK" } else { "CHECKSUM MISMATCH" }
```
