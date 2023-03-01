#!/bin/bash

# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

set -e

echo "Configuring CBL-Mariner build machine."

function verify_image {
    echo "verify_image"

    # Verify proper filesystem type for /mnt
    #
    # Good: /dev/sda1      ext4      126G   94M  119G   1% /mnt
    # Bad:  /dev/sda1      fuseblk   128G  125M  128G   1% /mnt
    MNT_FILESYSTEM_TYPE=$(df -Th | grep '/mnt$' | awk '{ print $2 }')
    if [[ "$MNT_FILESYSTEM_TYPE" == "ext4" ]]; then
        echo "Detected proper /mnt filesystem type is 'ext4'. Continuing."
    else
        echo "Error detected: /mnt filesystem type is '$MNT_FILESYSTEM_TYPE' instead of 'ext4'. Failing build." >&2
        return 1
    fi
}

function configure_image {
    echo "configure_image"
    # Install apps applicable to both X64 and ARM64
    sudo tdnf -y install dotnet-sdk-6.0 createrepo jq yum-utils rpm cpio dnf-utils acl
    # ensure golang 1.17 is installed
    sudo tdnf -y install "golang < 1.18"
    sudo tdnf -y install git make tar rpm-build gcc glibc-devel binutils \
        kernel-headers wget curl rpm qemu-img cdrkit python bison \
        gawk parted dosfstools pigz moby-engine moby-cli

    # Enable Docker daemon at boot
    sudo systemctl enable --now docker.service
    # Add current user to docker group
    sudo usermod -aG docker "$USER"

    # Install architecture-specific
    if [[ "$(uname -i)" == "x86_64" ]]; then
        configure_image_x64
    else
        configure_image_arm64
    fi
}

function configure_image_x64 {
    echo "configure_image_x64"
    # These are only available for X64.
    sudo tdnf -y install azure-cli powershell
}

function configure_image_arm64 {
    echo "configure_image_arm64"
    # Install Azure CLI via script. This requires python3-devel.
    sudo tdnf -y install python3-devel
    install_az_cli_with_script
}

function install_az_cli_with_script {
    echo "install_az_cli_with_script"
    pushd /tmp/
    #Work-around to make the script non-interactive and install az with default values
    cat > /tmp/non_interact.sh <<EOF
    sed -i 's/def prompt_input_with_default(msg, default):/def prompt_input_with_default(msg, default):\n    return default/g' \$1
    sed -i 's/def prompt_y_n(msg, default=None):/def prompt_y_n(msg, default=None):\n    return "y"/g' \$1
# The no-indentation is intentional. EOF with indentation is not considered as EOF.
EOF
    chmod +x /tmp/non_interact.sh
    curl -sL https://aka.ms/InstallAzureCli > /tmp/azcli_ins.sh
    sed -i 's/echo "Running install script."/echo "Running install script."\n\/tmp\/non_interact.sh \$install_script/g' /tmp/azcli_ins.sh
    sed -i "s/\$python_cmd \$install_script < \$_TTY/\$python_cmd \$install_script/g" /tmp/azcli_ins.sh
    bash /tmp/azcli_ins.sh
    sudo ln -svf /home/"$USER"/bin/az /usr/bin/az | true
    az extension add --name azure-devops
    az devops configure --defaults organization="https://dev.azure.com/mariner-org" project="mariner"
    az version
    popd
}

function print_app_versions {
    echo "print_app_versions"

    echo "Kernel version: $(uname -r)"
    echo "Architecture: $(uname -m)"
    docker --version
    go version
    echo "Dotnet version: $(dotnet --version)"
    # Note: powershell and azcli might not be available (on mariner arm64). Ignore errors
    pwsh --version || true
    echo "Az cli version: "
    az version || true
}

configure_image

verify_image

print_app_versions
