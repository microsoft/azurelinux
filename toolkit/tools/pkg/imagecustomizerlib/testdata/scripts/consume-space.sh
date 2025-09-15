# Write out a file that consumes the rest of the space on the rootfs partition.
dd if=/dev/zero of=/bigfile bs=512 || true
