# Creating ISO images from Full Images

```bash
./toolkit/mic-iso-gen-0/_create-full-image.sh \
    -c ~/git/CBL-Mariner/toolkit/imageconfigs/baremetal.json \
    -o ~/temp/baremetal-poc.vhdx

# the follow script can accept: .vhdx, .qcow2, and .raw.
./toolkit/mic-iso-gen-0/_create-iso-from-full-image.sh \
    -i ~/temp/baremetal-poc.vhdx \
    -b ~/temp/iso-build-poc
```

The output should be placed at `~/temp/iso-build/out/iso/baremetal-*.iso`.

