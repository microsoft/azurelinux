
# Build Requirements

CBL-Mariner is currently tested to build from the Desktop version of Ubuntu 18.04. It may build in other Ubuntu versions or editions, or even other distributions.

The following pre-requisites are required to build CBL-Mariner on Ubuntu 18.04


```bash
# Add a backports repo in order to install the latest version of Go.
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt-get update

# Install required dependencies.
sudo apt -y install make tar wget curl rpm qemu-utils golang-1.15-go genisoimage python-minimal bison gawk parted

# Recommended but not required: `pigz` for faster compression operations.
sudo apt -y install pigz

# Fix go 1.15 link
sudo ln -vsf /usr/lib/go-1.15/bin/go /usr/bin/go

# Install Docker.
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**You will need to log out and log back in** for user changes to take effect.
