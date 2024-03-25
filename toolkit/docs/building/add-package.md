# Adding package to Azure Linux

This document describes how to add a new package to `Azure Linux`.
Along this document, we will take [Inspektor Gadget]() as package example.

## The files needed

First, you need to create a directory under `SPECS`:

```bash
$ mkdir SPECS/ig
```

Each package relies on 2 different files:

1. A SPEC file: it contains information on the software and how to build and package it.
2. A signature file: this JSON file contains hashes of `tar.gz` archives used to get the sources.

We will now take a look at each of these files.

### The SPEC file

`Azure Linux` uses RPM packages, so you will need to write a [`SPEC` file](https://rpm-software-management.github.io/rpm/manual/spec.html)
You now need to write the corresponding SPEC file `SPECS/ig/ig.spec`:

```rpm
# A sentence describing the packaged software.
Summary:        The eBPF tool and systems inspection framework for Kubernetes, containers and Linux hosts.
# The name of the packaged software.
Name:           ig
# The version of the packaged software.
Version:        0.25.0
# TODO
Release:        1%{?dist}
# The license of the packaged software.
License:        Apache 2.0 and GPL 2.0 for eBPF code
# This should always be Microsoft Corporation, as Azure Linux is made by Microsoft.
Vendor:         Microsoft Corporation
# Distribution is always Azure Linux.
Distribution:   Azure Linux
# The group to which belongs the packaged software
Group:          Tools/Container
# The website of the packaged software.
URL:            https://github.com/inspektor-gadget/inspektor-gadget
# The link to the sources of the packaged software.
Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-govendor-v1.tar.gz
BuildRequires:  golang


# A small description of the packaged software.
%description
Inspektor Gadget is a collection of tools (or gadgets) to debug and inspect Kubernetes resources and applications. It manages the packaging, deployment and execution of eBPF programs in a Kubernetes cluster, including many based on BCC tools, as well as some developed specifically for use in Inspektor Gadget. It automatically maps low-level kernel primitives to high-level Kubernetes resources, making it easier and quicker to find the relevant information.

This package contains ig, the local CLI flavor of Inspektor Gadget.

# Steps run to prepare the build of the packaged software.
%prep
%autosetup -n inspektor-gadget-%{version}
%setup -q -n inspektor-gadget-%{version} -T -D -a 1

# Steps to actually build the packaged software.
%build
CGO_ENABLED=0 go build \
		-ldflags "-X github.com/inspektor-gadget/inspektor-gadget/cmd/common.version=v%{version} \
			-X github.com/inspektor-gadget/inspektor-gadget/cmd/common/image.builderImage=ghcr.io/inspektor-gadget/ebpf-builder:v%{version} \
			-extldflags '-static'" \
		-tags "netgo" \
		-o ./bin/build/ig ./cmd/ig

# Steps to install the compiled software.
# In this case, we just copy the ig binary under /bin.
%install
mkdir -p "%{buildroot}/%{_bindir}"
install -D -m0755 bin/build/ig %{buildroot}/%{_bindir}

# Steps used to check the compiled software run as expected.
%check
make gadgets-unit-tests
ig_file=$(mktemp /tmp/ig-XXXXXX.out)
sudo ./bin/build/ig trace exec --host > $ig_file &
ig_pid=$!
sleep inf &
sleep_pid=$!
kill $ig_pid
kill $sleep_pid
grep -P "${sleep_pid}\s+\d+\s+sleep" $ig_file
rm $ig_file

# Files which will be part of the resulting RPM package.
%files
%license LICENSE
%license LICENSE-bpf.txt
%{_bindir}/ig

%changelog
* Tue Mar 14 2023 Francis Laniel <flaniel@linux.microsoft.com> - 0.25.0-1
- Original version for Azure Linux
- License Verified
```

### Other files

You may need to add other files under the package directory, like:

1. Patches to apply to fix the software.
2. Script used to build the software.

## Getting the sources

So far, you should have the following in the package directory:

```bash
$ ls SPECS/ig
ig.spec
```

We first need to grab the `ig` code source:

```bash
$ wget https://github.com/inspektor-gadget/inspektor-gadget/archive/refs/tags/v0.25.0.tar.gz
...
$ mv v0.25.0.tar.gz ig-0.25.0.tar.gz
```

As `ig` is a `golang` software, we need to add the `golang` packages it uses as a `govendor` archive, we will use the following script, _i.e._ `generate_source_tarball.sh` to do so:

```bash
#!/bin/bash
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

# Quit on failure
set -e

PKG_VERSION=""
SRC_TARBALL=""
VENDOR_VERSION="1"
OUT_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# parameters:
#
# --srcTarball    : src tarball file
#                   this file contains the 'initial' source code of the component
#                   and should be replaced with the new/modified src code
# --outFolder     : folder where to copy the new tarball(s)
# --pkgVersion    : package version
# --vendorVersion : vendor version
#
PARAMS=""
while (( "$#" )); do
    case "$1" in
        --srcTarball)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            SRC_TARBALL=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --outFolder)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            OUT_FOLDER=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --pkgVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            PKG_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        --vendorVersion)
        if [ -n "$2" ] && [ ${2:0:1} != "-" ]; then
            VENDOR_VERSION=$2
            shift 2
        else
            echo "Error: Argument for $1 is missing" >&2
            exit 1
        fi
        ;;
        -*|--*=) # unsupported flags
        echo "Error: Unsupported flag $1" >&2
        exit 1
        ;;
        *) # preserve positional arguments
        PARAMS="$PARAMS $1"
        shift
        ;;
  esac
done

echo "--srcTarball      -> $SRC_TARBALL"
echo "--outFolder       -> $OUT_FOLDER"
echo "--pkgVersion      -> $PKG_VERSION"
echo "--vendorVersion   -> $VENDOR_VERSION"

if [ -z "$PKG_VERSION" ]; then
    echo "--pkgVersion parameter cannot be empty"
    exit 1
fi

echo "-- create temp folder"
tmpdir=$(mktemp -d)
function cleanup {
    echo "+++ cleanup -> remove $tmpdir"
    rm -rf $tmpdir
}
trap cleanup EXIT

TARBALL_FOLDER="$tmpdir/tarballFolder"
mkdir -p $TARBALL_FOLDER
cp $SRC_TARBALL $tmpdir

pushd $tmpdir > /dev/null

PKG_NAME="ig"
NAME_VER="$PKG_NAME-$PKG_VERSION"
VENDOR_TARBALL="$OUT_FOLDER/$NAME_VER-govendor-v$VENDOR_VERSION.tar.gz"

echo "Unpacking source tarball..."
tar -xf $SRC_TARBALL

echo "Vendor go modules..."
cd inspektor-gadget-"$PKG_VERSION"
go mod vendor

echo ""
echo "========================="
echo "Tar vendored tarball"
tar  --sort=name \
     --mtime="2021-04-26 00:00Z" \
     --owner=0 --group=0 --numeric-owner \
     --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
     -cf "$VENDOR_TARBALL" vendor

popd > /dev/null
echo "$PKG_NAME vendored modules are available at $VENDOR_TARBALL"
```

We now need to call the script:

```bash
$ bash generate_source_tarball.sh --srcTarball ig-0.25.0.tar.gz --pkgVersion 0.25.0
...
$ ls
generate_source_tarball.sh  ig-0.25.0-govendor-v1.tar.gz  ig.spec  ig-0.25.0.tar.gz
```

## Building the package

We have all the files needed to build the package, let's build it:

```bash
$ cd toolkit
# First, we need to prepare to get the toolchain:
$ ./scripts/setuplkgtoolchain.sh
...
Finished syncing toolchain to LKG ('3-0-20240227' - '7d886f3a947fb53ff3c08fd95823f1b0398e3d2f')
To download LKG toolchain, run:
        sudo make toolchain -j8 REBUILD_TOOLCHAIN=n REBUILD_TOOLS=y DAILY_BUILD_ID=3-0-20240227
# Let's get the toolchain:
$ sudo make toolchain -j8 REBUILD_TOOLCHAIN=n REBUILD_TOOLS=y DAILY_BUILD_ID=3-0-20240227
...
Downloading toolchain RPM: ...
# Let's build our package.
# NOTE, if you also changed the packages used as BuildRequires, you should add them to SRPM_PACK_LIST.
$ sudo make build-packages REBUILD_TOOLS=y SOURCE_URL='https://cblmarinerstorage.blob.core.windows.net/sources/core' PACKAGE_REBUILD_LIST='ig' SRPM_PACK_LIST='ig' RUN_CHECK=y SRPM_FILE_SIGNATURE_HANDLING=update DAILY_BUILD_ID=3-0-2024028
...
INFO[0003][srpmpacker] Packing 1/1 SPECs
...
INFO[0000][scheduler] Testing: ig-0.25.0-1.azl3.src.rpm
INFO[0000][scheduler] Building: ig-0.25.0-1.azl3.src.rpm
...
INFO[0200][scheduler] Built SRPMs:
INFO[0200][scheduler] --> ig-0.25.0-1.azl3.src.rpm
INFO[0200][scheduler] Passed SRPMs tests:
INFO[0200][scheduler] --> ig-0.25.0-1.azl3.src.rpm
```

Everything was built and tested, you should now have the package available:

```bash
$ rpm -ql ../out/RPMS/x86_64/ig-0.25.0-1.azl3.x86_64.rpm
/usr/bin/ig
/usr/share/licenses/ig
/usr/share/licenses/ig/LICENSE
/usr/share/licenses/ig/LICENSE-bpf.txt
```

The content seems good, let's test it locally:

```bash
$ rpm2cpio ../out/RPMS/x86_64/ig-0.25.0-1.azl3.x86_64.rpm | cpio -idmv
./usr/bin/ig
./usr/share/licenses/ig
./usr/share/licenses/ig/LICENSE
./usr/share/licenses/ig/LICENSE-bpf.txt
149181 blocs
$ ./usr/bin/ig --help
Collection of gadgets for containers

Usage:
  ig [command]
...
```

Congratulations! You successfully built an Azure Linux package!
## Testing in a Container

The toolkit can generate an azl containers for you, and auto launch them:
```bash
# Start the test container
$ sudo make containerized-rpmbuild MODE=test SRPM_PACK_LIST='ig' DAILY_BUILD_ID=3-0-2024028
...
.../CBL-Mariner/toolkit/scripts/containerized-build/create_container_build.sh -m test
...
Populating Intermediate SRPMs...
...
Setting up tools...
Setting up mounts...
Importing chroot into docker...
Chroot is up-to-date
Checking if build env is up-to-date...
...
 -----------------------------------------------------------------------------------------
 ----------------------------------- MARINER BUILDER ! -----------------------------------
 -----------------------------------------------------------------------------------------
******************************************************************************************
* To see this menu again, run  show_help
*
* Some tips:
*     Use local RPMs to satify dependencies:        run enable_local_repo
...

# Create a rpm repo based on the contents of ./out/RPMS/
root [ /mnt ]# enable_local_repo
-------- enabling local repo ---------
...
# Install the new package
$ tdnf install /mnt/RPMS/x86_64/ig-0.25.0-1.azl3.x86_64.rpm
...
$ ig --help
Collection of gadgets for containers
...
```

## Testing in a VM

To test your package in a VM, you will first need to create it:

```bash
# Modify the qemu-guest.json to add one root user.
$ $EDITOR ./imageconfigs/qemu-guest.json
...
$ git diff
diff --git a/toolkit/imageconfigs/qemu-guest.json b/toolkit/imageconfigs/qemu-guest.json
index 152b0330d..49d81bb5f 100644
--- a/toolkit/imageconfigs/qemu-guest.json
+++ b/toolkit/imageconfigs/qemu-guest.json
@@ -60,7 +60,14 @@
                     "Path": "scripts/cleanup.sh"
                 }
             ],
-            "Hostname": "azure-linux"
+            "Hostname": "azure-linux",
+            "Users": [
+                {
+                    "Name": "root",
+                    "UID": "1",
+                    "Password": "your_password"
+                }
+            ]
         }
     ]
 }
$ sudo make image REBUILD_TOOLS=y REBUILD_PACKAGES=n CONFIG_FILE=./imageconfigs/qemu-guest.json
...
INFO[0000][roast] [1/1] Converted (/.../CBL-Mariner/build/imagegen/qemu-guest/imager_output/disk0.raw) -> (/.../CBL-Mariner/out/images/qemu-guest/core-2.0.20240301.1447.vhdx)
# Change the user of the file to your user.
$ sudo chown $(whoami) /.../CBL-Mariner/out/images/qemu-guest/core-2.0.20240301.1453.vhdx
# Let's boot the VM:
# -bios: This option provides EFI bios to qemu, as our image is EFI. So, we use Tianocore which is packaged with qemu.
# -hda: This option uses the image as first disk.
# -net user,hostfwd=tcp::10022-:22: This option forwards host port 10022 to guest port 22. We will need to ssh from the host to the guest.
# -net nic: This option is needed since we modify the default qemu net.
$ qemu-system-x86_64 -m 4G -nographic -smp 2 -enable-kvm -bios /usr/share/ovmf/OVMF.fd -hda /.../CBL-Mariner/out/images/qemu-guest/core-2.0.20240301.1453.vhdx -net user,hostfwd=tcp::10022-:22 -net nic
...
Welcome to CBL-Mariner 2.0.20240223 (x86_64) - Kernel 5.15.148.2-1.cm2 (-)
azure-linux login: root
Password:
# Let's install openssh:
root@azure-linux [ ~ ]# tdnf install -y nano openssh-server
...
# Modify sshd config to enable root login:
root@azure-linux [ ~ ]# sed -i 's/PermitRootLogin no/PermitRootLogin yes/' /etc/ssh/sshd_config
# Now, we need to enable and start the ssh server:
root@azure-linux [ ~ ]# systemctl enable sshd
root@azure-linux [ ~ ]# systemctl start sshd
# Now, from the host, you can ssh to the guest to copy the package:
$ sftp -P 10022 root@localhost                                                                                                                                          francis/marinade-ig *% u=
Welcome to CBL-Mariner 2.0.20240223 (x86_64)
(root@localhost) Password:
Connected to localhost.
sftp> put ../out/RPMS/x86_64/ig-0.25.0-1.azl3.x86_64.rpm
Uploading ../out/RPMS/x86_64/ig-0.25.0-1.azl3.x86_64.rpm to /root/ig-0.25.0-1.azl3.x86_64.rpm
ig-0.25.0-1.azl3.x86_64.rpm                                                                                                                                                                                          100%   16MB   8.0MB/s   00:02
sftp> bye
# Go back to the VM and install the package:
root@azure-linux [ ~ ]# tdnf install -y ig-0.25.0-1.azl3.x86_64.rpm
...
Installing/Updating: ig-0.25.0-1.azl3.x86_64
# You can now test the software:
root@azure-linux [ ~ ]# ig version
v0.25.0
root@azure-linux [ ~ ]# ig --help
Collection of gadgets for containers

Usage:
  ig [command]
...
^Croot@azure-linux [ ~ ]# ig trace exec --host > /tmp/ig.log &
[1] 706
root@azure-linux [ ~ ]# ls /dev/null
ig-0.25.0-1.azl3.x86_64.rpm
root@azure-linux [ ~ ]# fg
ig trace exec --host > /tmp/ig.log
^C
root@azure-linux [ ~ ]# cat /tmp/ig.log
RUNTIME.CONTAINERNAME          PID              PPID             COMM             RET ARGS
                               717              561              ls               0   /bin/ls --color=auto
```

Congratulations! You successfully built the package and tested it in a Mariner VM.
You are now ready to open a PR to upstream your package.