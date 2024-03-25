# Partition Metadata JSON Format

The partition metadata JSON file contains metadata describing the extracted partitions 
of an image file. Each partition is represented as an object with the following
attributes:

partitionnum (integer):
Specifies the partition number.
Example: 1 

filename (string):
Specifies the filename of the partition image file.
Example: image_1.raw.zst

partlabel (string):
Provides the label of the partition.
Example: boot

fstype (string):
Indicates the filesystem type of the partition.
Example: vfat

parttype (string):
Specifies the partition type UUID. This uniquely identifies the type of partition.
Example: c12a7328-f81f-11d2-ba4b-00a0c93ec93b

uuid (string):
Specifies the UUID (Universally Unique Identifier) of the partition. This uniquely
identifies the partition within the filesystem.
Example: 4BD9-3A78

partuuid (string):
Specifies the PARTUUID (Partition UUID) of the partition. This uniquely identifies 
the partition within the system.
Example: 7b1367a6-5845-43f2-99b1-a742d873f590

mountpoint (string):
Indicates the mount point of the partition. 
Example: /mnt/os/boot