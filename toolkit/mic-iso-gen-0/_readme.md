# Creating ISO images from Full Images

```bash
./_create-full-image.sh \
    -c ~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json \
    -o ~/temp/baremetal.vhdx

# the follow script can accept: .vhdx, .qcow2, and .raw.
./_create-iso-from-full-image.sh \
    -i ~/temp/baremetal.vhdx \
    -b ~/temp/iso-build
```

The output should be placed at `~/temp/iso-build/out/iso/baremetal-*.iso`.

