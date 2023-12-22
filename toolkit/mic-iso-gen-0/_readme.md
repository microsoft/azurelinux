# Creating A Live-ISO from A Full Image

- Build/customize the image as usual.
  - Ensure that the image has the `squashfs-tools` package pre-installed.
  - You can optionally use the following script for convenience:
    ```bash
    ./toolkit/mic-iso-gen-0/_create-full-image.sh \
        -c ~/git/CBL-Mariner-POC/toolkit/imageconfigs/baremetal.json \
        -o ~/temp/baremetal-poc.vhdx
    ```
- Package it into a live-iso using the following command:
    ```bash
    # the follow script can accept: .vhdx, .qcow2, and .raw.
    ./toolkit/mic-iso-gen-0/_create-iso-from-full-image.sh \
        -i ~/temp/baremetal-poc.vhdx \
        -o ~/temp/iso-build-poc
    ```

The output should be placed under `~/temp/iso-build-poc/iso-out/iso/baremetal-*.iso`.
