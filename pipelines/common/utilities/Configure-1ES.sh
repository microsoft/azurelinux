#!/bin/bash
set -ex

arch=$(uname -i)
ROOT_FOLDER=$(git rev-parse --show-toplevel)
echo "Configuring 1ES build machine"

function configure_general {
    echo "configure_general"

    # Verify proper filesystem type for /mnt
    #
    # Good: /dev/sda1      ext4      126G   94M  119G   1% /mnt
    # Bad:  /dev/sda1      fuseblk   128G  125M  128G   1% /mnt
    MNT_FILESYSTEM_TYPE=$(df -Th | grep '/mnt$' | awk '{ print $2 }')
    if [[ "$MNT_FILESYSTEM_TYPE" == "ext4" ]]; then
        echo "Detected proper /mnt filesystem type (ext4). Continuing."
    else
        echo "Error detected, /mnt filesystem is '$MNT_FILESYSTEM_TYPE' instead of 'ext4'. Failing build."
        exit 1
    fi

    # Remove extended file ACL entries from ROOT_FOLDER
    setfacl -bn $ROOT_FOLDER

    # To avoid git "fatal: unsafe repository" warning
    git config --global --add safe.directory $ROOT_FOLDER

    # Add GitHub to known hosts to avoid the "Host key verification failed" error.
    ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts
}

function configure_distro_arch_specific {
    echo "configure_distro_arch_specific"
    source /etc/os-release
    if [[ "$ID" == "mariner" ]]; then
        configure_mariner
    else
        configure_ubuntu
    fi
}

function configure_mariner {
    echo "configure_mariner"
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
    sudo usermod -aG docker $USER

    # Install architecture-specific
    if [[ $arch == "x86_64" ]]; then
        configure_mariner_x64
    else
        configure_mariner_arm64
    fi
}

function configure_mariner_x64 {
    echo "configure_mariner_x64"
    # These are only available for X64
    sudo tdnf -y install azure-cli powershell
}

function configure_mariner_arm64 {
    echo "configure_mariner_arm64"
    # Install az cli via script. This requires python3-devel
    sudo tdnf -y install python3-devel
    install_az_cli_with_script
}

function configure_ubuntu_2204_x64 {
    echo "configure_ubuntu_2204_x64"
    # Install dotnet core 6
    sudo apt install -y dotnet6
    # Install az cli
    "$ROOT_FOLDER"/.pipelines/utilities/InstallAndConfigureAzureCLI.sh
    # docker
    # Enable Docker daemon at boot
    sudo systemctl enable --now docker.service
    # Add current user to docker group
    sudo usermod -aG docker $USER
}

function configure_ubuntu_2204_arm64 {
    echo "configure_ubuntu_2204_arm64"
    # Install dotnet core 6
    pushd /tmp/
    wget -nv https://download.visualstudio.microsoft.com/download/pr/234daf6a-5e12-4fa3-a73b-b12db44a3154/df7c012e5e4e2cc510de9226425dad88/dotnet-sdk-6.0.402-linux-arm64.tar.gz -O dotnet-sdk.tar.gz
    sudo tar zxf dotnet-sdk.tar.gz -C /bin/
    popd
    # Install az cli via script. This requires python3-dev
    sudo apt -y install python3-dev
    install_az_cli_with_script
}

function configure_ubuntu_1804_x64 {
    echo "configure_ubuntu_1804_x64"
    # Install dotnet core 6
    wget -nv https://packages.microsoft.com/config/ubuntu/18.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
    sudo dpkg -i packages-microsoft-prod.deb
    rm packages-microsoft-prod.deb
    sudo apt-get update
    sudo apt-get install -y dotnet-sdk-6.0
    # Install az cli
    "$ROOT_FOLDER"/.pipelines/utilities/InstallAndConfigureAzureCLI.sh
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
    sudo ln -svf /home/$USER/bin/az /usr/bin/az | true
    az extension add --name azure-devops
    az devops configure --defaults organization="https://dev.azure.com/mariner-org" project="mariner"
    az version
    popd
}

function configure_ubuntu_1804_arm64 {
    echo "configure_ubuntu_1804_arm64"
    # To avoid "Could not canonicalize hostname" error, which cause some package fail to build
    sudo bash -c 'echo "127.0.0.1 $(hostname)" >> /etc/hosts'
    # Install utility apps
    sudo apt-get -y install make tar wget curl rpm qemu-utils genisoimage python-minimal bison gawk pigz parted git createrepo yum-utils moreutils cpio unzip libssl-dev libffi-dev python3-dev build-essential jq
    # Install docker
    if ! [ -x "$(command -v docker)" ]; then
        echo "Docker is not installed - installing now"
        curl -fsSL https://get.docker.com -o get-docker.sh
        sudo sh get-docker.sh
    else
        echo "Docker is already installed"
    fi
    # Add current user to docker group
    sudo usermod -aG docker $USER
    # Install dotnet core 6
    pushd /tmp/
    wget -nv https://download.visualstudio.microsoft.com/download/pr/234daf6a-5e12-4fa3-a73b-b12db44a3154/df7c012e5e4e2cc510de9226425dad88/dotnet-sdk-6.0.402-linux-arm64.tar.gz -O dotnet-sdk.tar.gz
    sudo tar zxf dotnet-sdk.tar.gz -C /bin/
    popd
    # Install az cli
    install_az_cli_with_script
}

function configure_ubuntu {
    echo "configure_ubuntu"

    # Accept Microsoft public keys
    sudo apt-get update || true
    sudo apt-get install -y apt-transport-https gnupg
    wget -qO - https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
    wget -qO - https://packages.microsoft.com/keys/msopentech.asc | sudo apt-key add -

    # Install golang
    sudo add-apt-repository -y ppa:longsleep/golang-backports
    sudo apt-get update
    sudo apt -y install golang-1.17-go
    sudo ln -vsf /usr/lib/go-1.17/bin/go /usr/bin/go
    go version

    # Install version and architecture-specific
    source /etc/os-release
    if [[ $VERSION_ID == "18.04" ]]; then
        echo "Installing on Ubuntu 18.04"
        if [[ $arch == "x86_64" ]]; then
            configure_ubuntu_1804_x64
        else
            configure_ubuntu_1804_arm64
        fi
    elif [[ $VERSION_ID == "22.04" ]]; then
        echo "Installing on Ubuntu 22.04"
        if [[ $arch == "x86_64" ]]; then
            configure_ubuntu_2204_x64
        else
            configure_ubuntu_2204_arm64
        fi
    else
        echo "This version of Ubuntu is not supported: $VERSION_ID"
        exit 1
    fi
}

function configure_print_app_versions {
    echo "configure_print_app_versions"

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

configure_distro_arch_specific

configure_general

configure_print_app_versions
