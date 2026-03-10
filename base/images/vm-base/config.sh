
# Azure-specific configuration, from Fedora Cloud SIG, f43 branch
# https://pagure.io/fedora-kiwi-descriptions/blob/d8874b9ee71851b06aaecf43e492d1a6a4f3f164/f/config.sh#_164

cat > /etc/ssh/sshd_config.d/50-client-alive-interval.conf << EOF
ClientAliveInterval 120
EOF

cat >> /etc/chrony.conf << EOF
# Azure's virtual time source:
# https://docs.microsoft.com/en-us/azure/virtual-machines/linux/time-sync#check-for-ptp-clock-source
refclock PHC /dev/ptp_hyperv poll 3 dpoll -2 offset 0
EOF

# Support Azure's accelerated networking feature; without this the network fails
# to come up. It may need adjustments for additional drivers in the future.
cat > /etc/NetworkManager/conf.d/99-azure-unmanaged-devices.conf << EOF
# Ignore SR-IOV interface on Azure, since it's transparently bonded
# to the synthetic interface
[keyfile]
unmanaged-devices=driver:mlx4_core;driver:mlx5_core
EOF
