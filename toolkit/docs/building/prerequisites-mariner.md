
# Build Requirements on `Mariner`

## Requirements were validated on `Mariner 2.0`

This works regardless of installing `core` or `full` version of mariner.
If you installed `full` version of mariner, some of these packages are already installed, so less packages will be downloaded.

Requirements for building images with a toolkit:

```bash
# Install required dependencies.
sudo dnf -y install git make tar rpm-build gcc glibc-devel binutils \
kernel-headers wget curl rpm qemu-img golang cdrkit python bison \
gawk parted dosfstools pigz moby-engine moby-cli

# Enable Docker daemon at boot
sudo systemctl enable --now docker.service

# Add current user to docker group
sudo usermod -aG docker $USER
```
