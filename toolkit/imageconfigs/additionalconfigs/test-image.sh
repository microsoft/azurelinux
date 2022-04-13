cat<<EOF>> /tmp/part-include
zerombr
clearpart --drives=sda --all
# Not using RAID since DISK2 is not present
ignoredisk --only-use=/dev/sda
part biosboot --fstype=fat32 --size=1 --ondisk=/dev/sda
part / --fstype=ext4 --size=800 --grow --ondisk=/dev/sda
EOF