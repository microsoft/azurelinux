# Creating ISO images from Full Images

```bash
./toolkit/mic-iso-gen-0/_create-full-image.sh \
    -c ~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json \
    -o ~/temp/baremetal.vhdx

# the follow script can accept: .vhdx, .qcow2, and .raw.
./toolkit/mic-iso-gen-0/_create-iso-from-full-image.sh \
    -i ~/temp/baremetal.vhdx \
    -b ~/temp/iso-build-2
```

The output should be placed at `~/temp/iso-build/out/iso/baremetal-*.iso`.

