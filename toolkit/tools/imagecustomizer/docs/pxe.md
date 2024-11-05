# Azure Linux Image Customizer PXE Support

## PXE Overview

Booting a host with an OS served over the network is one of the most popular
methods for booting baremetal hosts. It requires no physical access to individual
hosts and also centralizes the deployment configuration to a single server.

One way of enabling such setup is using the PXE (Preboot eXecution Environment)
Boot protocol. The user can setup a server with all the OS artifacts, a DHCP
endpoint, and a tftp connection endpoint. When a client machine is powered on,
and its firmware will look for a DHCP server on the same network and find the
one configured by the user.

The DHCP server will serve information about the tftp endpoint to the client,
and the client firmware can then proceed with retrieving the OS artifacts over
tftp, then loading them into memory, and finally handing control over to the
loaded OS.

The tftp protocol expects certain artifacts to be present on the server:

- the boot loader (the shim and something like grub).
- the boot loader configuration (like grub.cfg).
- the kernel image.
- the initrd image.

Once retrieved, the boot loader is run. Then the boot loader reads the
boot loader configuration and then transfers control over to the kernel image
with the retrieved initrd image as its file system.

The initrd image is customized to perform the next set of tasks now that an
OS is running. The tasks can range from just running some local scripts all
the way to installing another OS.

## LiveOS ISOs and PXE Support

A LiveOS ISO image is a bootable ISO image that runs all the necessary
components from memory (i.e. does not need to install anything to the host
persistent storage).

The necessary components can be either embedded into the initrd image itself
or embedded into a separate 'rootfs' image (to allow much smaller
initrd images). If separate, then, the initrd image must be configured with an
agent that will look for the rootfs image, and transition control over to the
rootfs at boot time.

Dracut provides the `dmsquash-live` module which managed this transition from
the initrd image over to the rootfs image.

The **Azure Linux Image Customizer** produces such LiveOS ISO images. A typical
image holds the following artifacts:

- the boot loader (the shim and something like grub).
- the boot loader configuration.
- the kernel image.
- the initrd image.
- the rootfs image.
- other user defined artifacts (optional).

Note that the first 4 artifacts are what is necessary to get an OS kernel up
and running in a network boot scenario. What remains for a successful booting
of a LiveOS over the network is to make the rootfs image available for the final
transition (during the initrd phase).

Dracut enables that entire flow through the use of the `livenet` module - where
it inspects the `root=live:liveos-iso-url` kernel parameter from the boot loader
config file, and if it recognizes the `liveos-iso-url` protocol, it downloads
the ISO, and then proceeds to pivot to the embedded rootfs image.

The user can customize the rootfs using the Azure Linux Image Customizer as
usual. In case of additional artifacts that need downloading, the user can
install a daemon on the rootfs which will run when control is transferred to
the rootfs image and download any additional items.

## Creating and Deploying PXE Boot Artifacts

The Azure Linux Image Customizer produces LiveOS ISO images that are also PXE
bootable. So, the user can simply create an ISO image as usual, and the output
can be taken and deployed to a PXE server.

To make the deployment of the generated artifacts easier for the user, the
Azure Linux Image Customizer offers the following configurations:

- In the input configuration, there is a `pxe` node under which the user can
  configure PXE related properties - like the URL of the LiveOS ISO image to
  download (note that this image is the same image being built).
  See the [Azure Linux Image Customizer configuration](./configuration.md#pxe-type)
  page for more information.
- When invoking the Azure Linux Image Customizer, the user can also elect to
  export the artifacts to a local folder.
  See the [Azure Linux Image Customizer command line](./cli.md#output-pxe-artifacts-dir)
  page for more information.

Below is a list of required artifacts and where on the PXE server they should
be deployed:

```
ISO media layout           artifacts local folder      target on PXE server
-----------------------    ------------------------    ------------------------------
|- efi                      |                           <tftp-server-root>
   |- boot                  |                             |
      |- bootx64.efi        |- bootx64.efi                |- bootx64.efi
      |- grubx64.efi        |- grubx64.efi                |- grubx64.efi
|- boot                     |- boot                       |- boot
   |- grub2                    |- grub2                      |- grub2
      |- grub-pxe.cfg             |- grub.cfg                   |- grub.cfg
      |- grubenv                  |- grubenv                    |- grubenv
      |- grub.cfg
   |- vmlinuz                  |- vmlinuz                    |- vmlinuz
   |- initrd.img               |- initrd.img                 |- initrd.img

                                                        <yyyy-server-root>
|- other-user-artifacts     |- other-user-artifacts       |- other-user-artifacts
                            |- <liveos>.iso               |- <liveos>.iso
```

Notes:

- Note that the `/boot/grub2/grub.cfg` file in the ISO media is not used for
  PXE booting. Instead, the `/boot/grub2/grub-pxe.cfg` gets renamed to `grub.cfg`
  and is used instead.
- `yyyy` can be any protocol supported by Dracut's `livenet` module (i.e
  tftp, http, etc).
- The ISO image file location under the server root is customizable -
  but it must be such that its URL matches what is specified in the grub.cfg
  `root=live:<URL>`.
- While the core OS artifacts (the bootloader, its configuration, the kernel,
  initrd image, and rootfs image) will be downloaded and used automatically,
  the user will need to independently implement a way to download any
  additional artifacts. For example, the user can implement a daemon (and place
  it on the root file system) that will reach out and download the additional
  artifacts when it is up and running. The daemon can be configured with where
  to download the artifacts from, and what to do with them.
