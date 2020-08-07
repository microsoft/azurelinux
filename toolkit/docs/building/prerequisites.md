
# Build Requirements
---
## Basic Build
### Requirements were validated on `Ubuntu 18.04`.
Requirements for building images with a toolkit:
```bash
sudo apt -y install make tar wget curl rpm qemu-utils
```

Recommended but not required: `pigz` for faster compression operations.

---
## Rebuilding the Toolkit
Requirements for regenerating the toolkit (toolkits include pre-built Go binaries):
```bash
sudo add-apt-repository ppa:longsleep/golang-backports
sudo apt-get update
sudo apt install golang-1.13-go
```

You may need to run the following to correctly link go:
```bash
sudo ln -vs /usr/lib/go-1.13/bin/go /usr/bin/go
```



---
## Bootstrapping the Toolchain
Requirements for bootstrapping the toolchain using a docker container
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**You will need to log out and lock back in** for user changes to take effect.