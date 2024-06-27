# Developers guide

## Build Image Customizer binary

Run:

```bash
sudo make -C ./toolkit go-imagecustomizer
```

## Run toolkit tests

Run:

```bash
sudo go test -C ./toolkit/tools ./...
```

## Run Image Customizer specific tests

1. Build (or download) the
   [core-efi](https://github.com/microsoft/CBL-Mariner/blob/2.0/toolkit/imageconfigs/core-efi.json)
   vhdx image file for Azure Linux 2.0.

2. Download the test RPM files:

   ```bash
   ./toolkit/tools/pkg/imagecustomizerlib/testdata/testrpms/download-test-rpms.sh
   ```

3. Run the tests:

   ```bash
   AZURE_LINUX_2_CORE_EFI_VHDX="<core-efi-2.0.vhdx>"

   sudo go test -C ./toolkit/tools ./pkg/imagecustomizerlib -args \
     --base-image-core-efi "$AZURE_LINUX_2_CORE_EFI_VHDX"
   ```

   Where:

   - `<core-efi-2.0.vhdx>`: The vhdx image file you acquired in step 1.
