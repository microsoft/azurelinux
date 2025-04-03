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

1. Build (or download) the vhdx/vhd image files for:

   - [Azure Linux 2.0 core-efi](https://github.com/microsoft/CBL-Mariner/blob/2.0/toolkit/imageconfigs/core-efi.json)
   - [Azure Linux 3.0 core-efi](https://github.com/microsoft/CBL-Mariner/blob/3.0/toolkit/imageconfigs/core-efi.json)
   - [Azure Linux 2.0 core-legacy](https://github.com/microsoft/CBL-Mariner/blob/2.0/toolkit/imageconfigs/core-legacy.json)
   - [Azure Linux 3.0 core-legacy](https://github.com/microsoft/CBL-Mariner/blob/3.0/toolkit/imageconfigs/core-legacy.json)

2. Download the test RPM files:

   ```bash
   ./toolkit/tools/pkg/imagecustomizerlib/testdata/testrpms/download-test-rpms.sh
   ```

3. Run the tests:

   ```bash
   AZURE_LINUX_2_CORE_EFI_VHDX="<core-efi-2.0.vhdx>"
   AZURE_LINUX_3_CORE_EFI_VHDX="<core-efi-3.0.vhdx>"
   AZURE_LINUX_2_CORE_LEGACY_VHD="<core-legacy-2.0.vhd>"
   AZURE_LINUX_3_CORE_LEGACY_VHD="<core-legacy-3.0.vhd>"

   sudo go test -C ./toolkit/tools ./pkg/imagecustomizerlib -args \
     --base-image-core-efi-azl2 "$AZURE_LINUX_2_CORE_EFI_VHDX"
     --base-image-core-efi-azl3 "$AZURE_LINUX_3_CORE_EFI_VHDX"
     --base-image-core-legacy-azl2 "$AZURE_LINUX_2_CORE_LEGACY_VHD"
     --base-image-core-legacy-azl3 "$AZURE_LINUX_3_CORE_LEGACY_VHD"
   ```
