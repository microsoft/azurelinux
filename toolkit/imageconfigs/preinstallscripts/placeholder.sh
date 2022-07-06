cat<<EOF> /tmp/part-include
zerombr
clearpart --drives=sda --all
# Not using RAID since DISK2 is not present
ignoredisk --only-use=/dev/sda
part biosboot --fstype=biosboot --size=1 --ondisk=/dev/sda
part / --fstype=ext4 --size=10240 --ondisk=/dev/sda
part /var --fstype=ext4 --size=10240 --ondisk=/dev/sda
part swap --fstype=swap --size=16384 --ondisk=/dev/sda
part /export --fstype=ext4 --size=1 --grow --ondisk=/dev/sda
EOF