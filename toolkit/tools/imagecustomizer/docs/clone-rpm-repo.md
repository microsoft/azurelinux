# Cloning an RPM repo

By default, the image customizer tool uses the base image's inbuilt repo files for where
to source RPMs from. The Azure Linux default repos typically point to
packages.microsoft.com (PMC).

PMC is regularly updated with bug fixes and feature updates for packages. So, if an
image customization config includes package install or updates, then a run on one day
may produce a different result than a run on another day since PMC might have been
updated in between runs. This behavior may be perfectly fine (or even desirable) for
some users. However, other users may require more stable builds that don't change based
on the state of an external resource (e.g. PMC). For such users, it can be useful to
make a clone of PMC.

## Cloning a repo to a local directory

1. Acquire the `dnf reposync` and `dnf download` commands.

   Azure Linux 2.0 and 3.0:

   ```bash
   sudo tdnf -y install dnf-utils
   ```

   Ubuntu 24.04:

   ```bash
   sudo apt update -y
   sudo apt install -y dnf-plugins-core
   ```

2. Select the repo URL:

   | Azure Linux Version | Arch   | URL                                                               |
   | ------------------- | ------ | ----------------------------------------------------------------- |
   | 2.0                 | x86_64 | https://packages.microsoft.com/cbl-mariner/2.0/prod/base/x86_64/  |
   | 2.0                 | ARM64  | https://packages.microsoft.com/cbl-mariner/2.0/prod/base/aarch64/ |
   | 3.0                 | x86_64 | https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/   |
   | 3.0                 | ARM64  | https://packages.microsoft.com/azurelinux/3.0/prod/base/aarch64/  |

   For example:

   ```bash
   REPO_URL="https://packages.microsoft.com/azurelinux/3.0/prod/base/x86_64/"
   ```

3. Clone PMC.

   If you want to clone all of PMC, then run:

   ```bash
   dnf reposync --repofrompath "azurelinux,$REPO_URL" --repo azurelinux --newest-only
   ```

   If you want to only clone a subset of packages (and their dependencies), then run:

   ```bash
   PACKAGE_LIST="vim nano"
   dnf download --repofrompath "azurelinux,$REPO_URL" --repo azurelinux --resolve --alldeps --destdir azurelinux $PACKAGE_LIST
   ```

   This will download the RPMs into a directory named `azurelinux`.

4. Cache the downloaded RPMs somewhere.

5. Use cached RPMs with the image customizer tool.

   ```bash
    sudo ./imagecustomizer \
      --build-dir ./build \
      --image-file <base-image-file> \
      --output-image-file ./out/image.vhdx \
      --output-image-format vhdx \
      --config-file <config-file> \
      --disable-base-image-rpm-repos \
      --rpm-source <rpms-dir>
   ```

   where:

   - `<base-image-file>`: The base image file.
   - `<config-file>`: The image customizer config file.
   - `<rpms-dir>`: The local directory that contains the downloaded RPMs.

## Hosting a cloned repo

It may be desirable to host the downloaded RPMs in a common location so that it can be
used by both builds and developers.

An RPM server is simply a HTTP server that hosts static files. There is no dynamic
content. So, pretty much any HTTP server application or provider can be used. The files
served by the HTTP server are the RPM files themselves and a few metadata files that
document what RPMs are available.

Example RPM server using httpd/apache2:

1. Install prerequisites:

   Azure Linux 2.0 and 3.0:

   ```bash
   sudo tdnf -y install createrepo_c httpd
   sudo systemctl enable --now httpd
   ```

   Ubuntu 22.04:

   ```bash
   sudo apt update -y
   sudo apt install -y createrepo-c apache2
   ````

2. Download the cached RPMs to a local directory.

3. Create the metadata files:

   ```bash
   createrepo_c --compatibility --update <rpms-dir>
   ```

   where:

   - `<rpms-dir>`: The directory you downloaded the RPMs to.

4. Move the RPMs directory:

   ```bash
   sudo mkdir -p /var/www
   sudo mv -T <rpms-dir> /var/www/rpms
   ```

5. Configure the HTTP server:

   Azure Linux 2.0 and 3.0:

   ```bash
   sudo sed -i 's|"/etc/httpd/htdocs"|"/var/www/rpms"|' /etc/httpd/conf/httpd.conf
   sudo systemctl reload httpd
   ```

   Ubuntu 22.04:

   ```bash
   sudo sed -i 's|/var/www/html|/var/www/rpms|' /etc/apache2/sites-available/000-default.conf
   sudo systemctl reload httpd
   ```

6. Create a file called `rpms.repo` with the following contents:

   ```ini
   [rpmshost]
   name=rpmshost
   baseurl=http://<ip-address>
   enabled=1
   ```

   where:

   - `<ip-address>`: The IP address of the HTTP server hosting the RPM files.

7. Use the `rpms.repo` file with the image customizer tool:

   ```bash
    sudo ./imagecustomizer \
      --build-dir ./build \
      --image-file <base-image-file> \
      --output-image-file ./out/image.vhdx \
      --output-image-format vhdx \
      --config-file <config-file> \
      --disable-base-image-rpm-repos \
      --rpm-source rpms.repo
   ```

   where:

   - `<base-image-file>`: The base image file.
   - `<config-file>`: The image customizer config file.
